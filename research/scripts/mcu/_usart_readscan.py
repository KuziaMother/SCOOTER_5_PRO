# -*- coding: utf-8 -*-
"""Скан mcu_0007.bin: (1) все сборщики push-кадров (movs #0x61/#0x9e),
(2) функции, ссылающиеся на строки DFU-консоли (error/ok/0002 + пул команд)."""
import os, struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN

FW = os.path.join(os.path.dirname(__file__), "..", "..", "images", "mcu_0007.bin")
d = open(FW, "rb").read()
N = len(d)

CODE = [(0x01200, 0x02400), (0x02600, 0x10200), (0x10400, 0x10e00),
        (0x11000, 0x12400), (0x12800, 0x13e00), (0x14200, 0x14400),
        (0x14600, 0x17a00), (0x18e00, 0x19200), (0x19a00, 0x24200),
        (0x24400, 0x24600)]

starts = []
for a, b in CODE:
    for o in range(a, b, 2):
        if struct.unpack_from("<H", d, o)[0] & 0xFF00 == 0xB500:
            starts.append(o)

def func_of(off):
    best = None
    for s in starts:
        if s <= off:
            best = s
        else:
            break
    return best

md = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)

# --- (1) movs #0x61 / #0x9e (сборщики кадров) ---
print("=== (1) movs rX,#0x61 / #0x9e (кандидаты на сборку push-кадра) ===")
frame_hits = {}
for a, b in CODE:
    for ins in md.disasm(d[a:b], a):
        if ins.mnemonic == "movs" and ("#0x61" in ins.op_str or "#0x9e" in ins.op_str):
            f = func_of(ins.address)
            frame_hits.setdefault(f, []).append((ins.address, ins.op_str))
for f in sorted(frame_hits):
    locs = frame_hits[f]
    print(f"  func@0x{f:05x}: {len(locs)} хитов, напр. {[(hex(o), o2) for o,o2 in locs[:3]]}")

# --- (2) ссылки на строки консоли (literal-pool words + movw/movt) ---
STRINGS = {0x18acc: "error", 0x18b62: "ok 0000000000", 0x18b94: "0002",
           0x1893c: "CMD-pool base (rd_info)", 0x1896e: "get_ver",
           0x18a04: "nvm_write", 0x18a36: "dfu_verify", 0x189a0: "dfu_active"}
print("\n=== (2) literal-pool слова == адреса строк консоли ===")
for o in range(0, N - 3, 4):
    w = struct.unpack_from("<I", d, o)[0]
    if w in STRINGS:
        f = func_of(o)
        print(f"  @0x{o:05x} (func 0x{f:05x}) -> {STRINGS[w]}")

# movw/movt пары
print("\n=== (2b) movw+movt конструирующие адреса строк ===")
for a, b in CODE:
    i = 0
    words = d[a:b]
    insns = list(md.disasm(words, a))
    for k in range(len(insns) - 1):
        if insns[k].mnemonic == "movw" and insns[k+1].mnemonic in ("movt", "movw"):
            try:
                imm = int(insns[k].op_str.split(",")[1].split()[0], 16)
                reg = insns[k].op_str.split(",")[0]
                if insns[k+1].mnemonic == "movt" and reg in insns[k+1].op_str:
                    imm2 = int(insns[k+1].op_str.split(",")[1].split()[0], 16)
                    addr = (imm2 << 16) | (imm & 0xFFFF)
                    if addr in STRINGS:
                        f = func_of(insns[k].address)
                        print(f"  @0x{insns[k].address:05x} (func 0x{f:05x}) {reg} -> {STRINGS[addr]}")
            except Exception:
                pass

print("\n[done]")
