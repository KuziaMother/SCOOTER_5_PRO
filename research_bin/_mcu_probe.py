# -*- coding: utf-8 -*-
"""Эмпирика для gen_functions_mcu: прологи, формула ldr-пула, база 0x08000000."""
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB

d = open("mcu_0007.bin", "rb").read()
N = len(d)
print(f"image: {N} bytes (0x{N:x})")

CODE = [(0x01200, 0x02400), (0x02600, 0x10200), (0x10400, 0x10e00),
        (0x11000, 0x12400), (0x12800, 0x13e00), (0x14200, 0x14400),
        (0x14600, 0x17a00), (0x18e00, 0x19200), (0x19a00, 0x24200),
        (0x24400, 0x24600)]

# --- 1. что в 0x0000..0x1200 (до первого CODE-региона) ---
print("\n== head 0x0000..0x0040 ==")
for i in range(0, 0x40, 16):
    row = d[i:i+16]
    hexs = " ".join(f"{b:02x}" for b in row)
    asc = "".join(chr(b) if 32 <= b < 127 else "." for b in row)
    print(f"{i:05x}: {hexs:<48} {asc}")

def prologues(a, b):
    b5 = []
    i = a
    while i + 2 <= b:
        w = struct.unpack_from("<H", d, i)[0]
        if (w & 0xFF00) == 0xB500 and (w & 0x0100):
            b5.append(i)
        i += 2
    return b5

tot_b5 = 0
for (a, b) in CODE:
    tot_b5 += len(prologues(a, b))
b5_h = prologues(0x0, 0x1200)
print(f"\n== prologues B5xx{{..,lr}} in CODE: {tot_b5}; head 0x0..0x1200: {len(b5_h)} {b5_h[:16]}")

# эмпирика T32 push.w: какие наборы (w1,w2) с w1&0xFF80==0xE900 реально есть?
from collections import Counter
pairs = Counter()
for (a, b) in CODE:
    i = a
    while i + 4 <= b:
        w1 = struct.unpack_from("<H", d, i)[0]
        if (w1 & 0xFF80) == 0xE900:
            w2 = struct.unpack_from("<H", d, i + 2)[0]
            pairs[(w1, w2)] += 1
        i += 2
print(f"== pairs with w1&0xFF80==0xE900: total={sum(pairs.values())}, uniq={len(pairs)}")
for (p, c) in pairs.most_common(15):
    print(f"   {p[0]:#06x} {p[1]:#06x}  x{c}")

# --- 2. формула ldr-пула: F1=(A+4)&~3 + imm  vs  F2=(A+4)+imm ---
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
md.detail = False

def plausible(v):
    if v is None: return "none"
    if 0x20000000 <= v < 0x20020000: return "ram"
    if 0x40000000 <= v < 0x40100000: return "peri"
    if 0xE0000000 <= v < 0xE0100000: return "sys"
    if 0 <= v < N: return "img"
    if 0x08000000 <= v < 0x08000000 + N: return "img8"
    return "out"

def word(off):
    if 0 <= off + 4 <= N:
        return struct.unpack_from("<I", d, off)[0]
    return None

stats = {"f1": {}, "f2": {}}
gtruth = {  # addr: (imm, expected) — из проверенных дампов
    0x1e9e2: (0x3fc, 0x200002c0),
    0x1ea00: (0x3e8, 0x20000881),
    0x1e9f4: (0x3e8, 0x200002c0),
    0x1ea22: (0x3c8, 0x20000881),
    0x1ed90: (0xb8, 0x200002cb),
}
gt_res = {}
n16 = n32 = 0
for (a, b) in CODE:
    for ins in md.disasm(d[a:b], a):
        if ins.mnemonic in ("ldr", "ldr.w") and "[pc" in ins.op_str:
            try:
                imm = int(ins.op_str.split("#")[1].split("]")[0], 16)
            except (ValueError, IndexError):
                continue
            n32 += 1 if ins.size == 4 else 0
            n16 += 1 if ins.size == 2 else 0
            f1 = word(((ins.address + 4) & ~3) + imm)
            f2 = word((ins.address + 4) + imm)
            stats["f1"][plausible(f1)] = stats["f1"].get(plausible(f1), 0) + 1
            stats["f2"][plausible(f2)] = stats["f2"].get(plausible(f2), 0) + 1
            if ins.address in gtruth:
                exp = gtruth[ins.address][1]
                gt_res[ins.address] = (imm == gtruth[ins.address][0],
                                       f1 == exp, f2 == exp)

print(f"\n== ldr-lit in CODE: total={sum(stats['f1'].values())} (16b={n16}, 32b={n32})")
print(f"== F1 ((A+4)&~3 + imm): {stats['f1']}")
print(f"== F2 ((A+4)    + imm): {stats['f2']}")
print("== ground truth (imm_ok, F1_ok, F2_ok):")
for a in sorted(gt_res):
    print(f"   {a:05x}: {gt_res[a]}")

# --- 3. литералы с базой 0x08000000 ---
n_img8 = sum(1 for v in stats["f1"].keys() if False)  # placeholder
cnt = {"ram": 0, "peri": 0, "sys": 0, "img": 0, "img8": 0, "out": 0, "none": 0}
for (a, b) in CODE:
    for ins in md.disasm(d[a:b], a):
        if ins.mnemonic in ("ldr", "ldr.w") and "[pc" in ins.op_str:
            try:
                imm = int(ins.op_str.split("#")[1].split("]")[0], 16)
            except (ValueError, IndexError):
                continue
            v = word(((ins.address + 4) & ~3) + imm)
            cnt[plausible(v)] += 1
print(f"\n== resolved-pool value classes (F1): {cnt}")
print(f"   -> img8 (база 0x08000000): {cnt['img8']} из {sum(cnt.values())}")
