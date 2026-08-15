# -*- coding: utf-8 -*-
"""Капстон-декод T32 push.w кандидатов + их позиция относительно B5xx-стартов."""
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB

d = open("mcu_0007.bin", "rb").read()
N = len(d)
CODE = [(0x01200, 0x02400), (0x02600, 0x10200), (0x10400, 0x10e00),
        (0x11000, 0x12400), (0x12800, 0x13e00), (0x14200, 0x14400),
        (0x14600, 0x17a00), (0x18e00, 0x19200), (0x19a00, 0x24200),
        (0x24400, 0x24600)]

starts = []
for (a, b) in CODE:
    i = a
    while i + 2 <= b:
        w = struct.unpack_from("<H", d, i)[0]
        if (w & 0xFF00) == 0xB500 and (w & 0x0100):
            starts.append(i)
        i += 2
starts.sort()

md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)

def prev_start(t):
    best = None
    for s in starts:
        if s <= t:
            best = s
        else:
            break
    return best

cands = []
for (a, b) in CODE:
    i = a
    while i + 4 <= b:
        w1 = struct.unpack_from("<H", d, i)[0]
        if (w1 & 0xFF80) == 0xE900:
            cands.append(i)
        i += 2

print(f"B5xx starts={len(starts)}, T32 cands={len(cands)}")
inside = at_start = new_like = 0
decoded = {}
for t in cands:
    code = d[t:t+4]
    try:
        ins = next(md.disasm(code, t))
        dec = f"{ins.mnemonic} {ins.op_str}"
    except StopIteration:
        dec = "(undecodable)"
    decoded.setdefault(dec, 0)
    decoded[dec] += 1
    ps = prev_start(t)
    if ps is None or t - ps > 8:
        new_like += 1
        print(f"  NEW?  {t:05x} (prev B5xx at {ps and hex(ps)}, dist={None if ps is None else t-ps}): {dec}")
    elif t == ps:
        at_start += 1
    else:
        inside += 1

print(f"\n== T32 cands: at B5xx start={at_start}, inside fn (dist<=8)={inside}, new-like (dist>8 or none)={new_like}")
print("== capstone decode distribution:")
for k, v in sorted(decoded.items(), key=lambda x: -x[1]):
    print(f"   x{v:<3} {k}")
