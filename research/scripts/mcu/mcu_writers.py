# -*- coding: utf-8 -*-
"""Dynamic search for writers of u16@0x32e / u16@0x330 (get 0x36).

Sweep of all functions + target functions with various seeds;
write hook on 0x2000032C..0x20000334 (also catch u32-str at 0x32C).
"""
import os, sys, struct
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "emulator"))
from mcu_emu import McuEmu, find_func_starts, PERIPH, STACK_TOP
from unicorn import UcError, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(os.path.dirname(HERE))   # research/
BIN = os.path.join(RES, "images", "mcu_0007.bin")

TGT_LO = 0x2000032C
TGT_HI = 0x20000334   # exclusive


def main():
    global d_bytes
    d_bytes = open(BIN, "rb").read()
    emu = McuEmu()
    hits = []

    def on_w(uc, access, address, size, value, user):
        if TGT_LO <= address < TGT_HI:
            pc = uc.reg_read(UC_ARM_REG_LR)  # LR not suitable; take PC below
            hits.append((address, size, value))

    # correct PC: hook called AFTER instruction? no - before/after?
    # Unicorn: hook mem_write gets address/value; read PC as r15.
    from unicorn.arm_const import UC_ARM_REG_PC
    def on_w2(uc, access, address, size, value, user):
        if TGT_LO <= address < TGT_HI:
            pc = uc.reg_read(UC_ARM_REG_PC)
            hits.append((pc, address, size, value))

    emu.uc.hook_add(UC_HOOK_MEM_WRITE, on_w2, None, TGT_LO, TGT_HI - TGT_LO)

    starts = find_func_starts()
    # extended regions (not in REGIONS gen_functions_mcu.py): 0x17a00..0x18e00 (98% code),
    # 0x12400..0x12800 (93%), 0x10200..0x10400 (79%)
    import struct as _s
    extra = []
    for a, b in [(0x10200, 0x10400), (0x12400, 0x12800), (0x17a00, 0x18e00)]:
        for o in range(a, b, 2):
            if (_s.unpack_from("<H", d_bytes, o)[0] & 0xFF00) == 0xB500:
                extra.append(o)
    starts = list(dict.fromkeys(starts + extra))
    print(f"functions: {len(starts)} (including {len(extra)} from extended regions)")

    seeds = [
        ("base", {}),
        ("adc_state5", {0x20000248: b"\x05",
                        0x2000168A: struct.pack("<5H", 3000, 2500, 2100, 1900, 1700),
                        0x2000024C: struct.pack("<h", 2500)}),
        ("adc_state1", {0x20000248: b"\x01"}),
        ("adc_state3", {0x20000248: b"\x03"}),
        ("trig_hi", {0x2000024C: struct.pack("<h", 2500)}),
        ("task_s1", {0x200003D8: b"\x01"}),
        ("task_s2", {0x200003D8: b"\x02"}),
        ("task_s3", {0x200003D8: b"\x03", 0x2000024C: struct.pack("<h", 2500)}),
        ("task_s4", {0x200003D8: b"\x04"}),
        ("task_s5", {0x200003D8: b"\x05"}),
        ("task_s6", {0x200003D8: b"\x06"}),
        ("flash_cal", {0x0801F400: struct.pack("<2H", 2000, 1800)}),
    ]

    for sname, seed in seeds:
        emu.uc.mem_write(0x20000000, b"\x00" * 0x18000)
        for a, b in seed.items():
            emu.uc.mem_write(a, b)
        emu.uc.mem_write(PERIPH, b"\xff" * 0x100000)
        before = len(hits)
        for f in starts:
            emu.insn = 0
            emu.stopped = None
            emu.uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
            emu.uc.reg_write(UC_ARM_REG_LR, 1)
            try:
                emu.uc.emu_start(f | 1, 0, count=40005)
            except UcError:
                pass
        print(f"seed {sname}: +{len(hits)-before} writes")

    if hits:
        seen = {}
        for pc, addr, size, val in hits:
            seen.setdefault(pc, []).append((addr, size, val))
        print(f"\n=== WRITERS to 0x32C..0x334: {len(hits)} writes, {len(seen)} unique PCs ===")
        for pc in sorted(seen):
            samples = seen[pc][:6]
            print(f"  pc=0x{pc:05x}: {len(seen[pc])}x e.g. "
                  f"{[(hex(a), s, hex(v)) for a, s, v in samples]}")
    else:
        print("\n=== NO writes to 0x32C..0x334 found ===")


if __name__ == "__main__":
    main()
