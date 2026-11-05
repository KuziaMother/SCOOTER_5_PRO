# -*- coding: utf-8 -*-
"""§73.x: FOC 0x1a938 trace — peripheral READS + writes (timer regions).

Goal of TIM clock model: understand which timer registers firmware POLLS (reads)
vs configures (writes), and in which regions. periph_reads provides addresses (read values
in this Unicorn are unreliable — only address is valid).
"""
import struct, sys
sys.path.insert(0, '.')
from emulator.mcu_emu import McuEmu, FLASH0, FLASH1, RAM, STACK_TOP
from unicorn import UC_HOOK_CODE, UcError
from unicorn.arm_const import (UC_ARM_REG_R4, UC_ARM_REG_SP, UC_ARM_REG_LR,
                               UC_ARM_REG_R0)

FW_LEN = 0x25000


def run_foc(val=16384):
    emu = McuEmu(max_insn=200000)
    emu.uc.mem_write(RAM, bytes(0x20000))
    r4 = RAM + 0x040
    emu.uc.mem_write(r4, bytes(0x80))
    emu.uc.mem_write(r4 + 2, struct.pack('<h', val))
    # open FOC gate (STAT bit15) + known CTRL
    emu.uc.mem_write(0x40012c54, struct.pack('<I', 0x8000))
    emu.uc.mem_write(0x40012c30, struct.pack('<I', 0xFFFF))
    emu.trace_periph = True

    def stop(uc_, addr, size, u):
        aa = addr & ~1
        if not (FLASH0 <= aa < FLASH0 + FW_LEN or
                FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()
    sh = emu.uc.hook_add(UC_HOOK_CODE, stop)
    emu.uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
    emu.uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    emu.uc.reg_write(UC_ARM_REG_R4, r4)
    emu.uc.reg_write(UC_ARM_REG_R0, 0)
    try:
        emu.uc.emu_start(0x1A938 | 1, 0, count=200000)
    except UcError:
        pass
    emu.uc.hook_del(sh)
    return emu


def region(name, lo, hi):
    def f(a):
        return lo <= a < hi
    return name, f


def main():
    emu = run_foc(16384)
    # periph_reads = {addr: [pc,...]} ; periph_writes = [(pc, addr, size, value)]
    read_addrs = set(emu.periph_reads.keys())
    writes = [(a, v) for _, a, s, v in emu.periph_writes]

    regions = [
        region('GPT 0x40002xxx', 0x40002000, 0x40002100),
        region('MOTOR 0x40012xxx', 0x40012000, 0x40013000),
        region('ADC 0x40010xxx', 0x40010000, 0x40011000),
    ]

    print('=== FOC 0x1a938: peripheral footprint (value=16384) ===')
    print(f'distinct read addresses: {len(read_addrs)}, writes: {len(writes)}\n')
    for name, f in regions:
        rs = sorted(a for a in read_addrs if f(a))
        ws = sorted(set((a, v) for a, v in writes if f(a)))
        if rs or ws:
            print(f'--- {name} ---')
            if rs:
                for a in rs:
                    pcs = emu.periph_reads[a]
                    print(f'  READ {a:#x} (off {a - 0x40012000 if f(a) else 0:#x}) '
                          f'×{len(pcs)}: pc=' + ', '.join(f'{p:#x}' for p in pcs[:6]))
            if ws:
                print('  WRITES: ' + ', '.join(f'{a:#x}<-{v:#x}' for a, v in ws))
    # all peripheral addresses (any region) for completeness
    allr = sorted(a for a in read_addrs if 0x40000000 <= a < 0x50000000)
    allw = sorted(set(a for _, a, s, v in writes if 0x40000000 <= a < 0x50000000))
    print('\n=== ALL periph addresses (0x40000000-0x50000000) ===')
    print(f'READS ({len(allr)}): {", ".join(hex(a) for a in allr) or "none"}')
    print(f'WRITES ({len(allw)}): {", ".join(hex(a) for a in allw) or "none"}')


if __name__ == '__main__':
    main()
