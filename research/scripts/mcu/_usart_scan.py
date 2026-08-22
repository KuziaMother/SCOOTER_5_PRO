# -*- coding: utf-8 -*-
"""Скан mcu_0007.bin: какие функции ссылаются на регистры USART/UART (0x4000xxxx).

Два источника ссылок:
  1. literal-пулы: 4-байтные слова в [0x40004000, 0x40005000) (ldr rX,[pc,#k]);
  2. movw+movt пары, конструирующие такой адрес.
Каждое попадание атрибутируется функции (ближайшее начало не правее).
"""
import os, struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN

FW = os.path.join(os.path.dirname(__file__), "..", "..", "images", "mcu_0007.bin")
d = open(FW, "rb").read()
N = len(d)

# --- начала функций (как в emulator/mcu_emu.py) ---
CODE = [(0x01200, 0x02400), (0x02600, 0x10200), (0x10400, 0x10e00),
        (0x11000, 0x12400), (0x12800, 0x13e00), (0x14200, 0x14400),
        (0x14600, 0x17a00), (0x18e00, 0x19200), (0x19a00, 0x24200),
        (0x24400, 0x24600)]
starts = []
for a, b in CODE:
    for o in range(a, b, 2):
        if struct.unpack_from("<H", d, o)[0] & 0xFF00 == 0xB500:
            starts.append(o)
print(f"функций: {len(starts)}")

def func_of(off):
    best = None
    for s in starts:
        if s <= off:
            best = s
        else:
            break
    return best

# --- 1. literal-пулы (4-байтные слова по всему файлу) ---
hits = {}   # func -> {addr_value: [offsets]}
for o in range(0, N - 3, 4):
    w = struct.unpack_from("<I", d, o)[0]
    if 0x40004000 <= w < 0x40005000:
        f = func_of(o)
        hits.setdefault(f, {}).setdefault(w, []).append(o)

# --- 2. movw+movt пары ---
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
md.skipdata = True
for i, ins in enumerate(md.disasm(d, 0)):
    if ins.mnemonic == "movw":
        # ищем следующую инструкцию movt в тот же регистр
        op = ins.op_str.strip()
        if "," in op:
            reg, imm = [x.strip() for x in op.split(",", 1)]
            for ins2 in md.disasm(d[ins.address + ins.size:ins.address + ins.size + 8],
                                  ins.address + ins.size):
                if ins2.mnemonic == "movt" and ins2.op_str.strip().startswith(reg + ","):
                    try:
                        hi = int(ins2.op_str.split(",")[1].strip(), 16)
                        lo = int(imm, 16)
                        val = (hi << 16) | lo
                    except ValueError:
                        break
                    if 0x40004000 <= val < 0x40005000:
                        f = func_of(ins.address)
                        hits.setdefault(f, {}).setdefault(val, []).append(ins.address)
                break

print(f"\nфункций, ссылающихся на 0x40004xxx: {len(hits)}")
for f in sorted(hits):
    addrs = sorted(hits[f])
    print(f"  func 0x{f:05x}: {[hex(a) for a in addrs]}")

# --- дизассемблер каждой такой функции (до следующего начала) ---
import sys
only = [int(x, 16) for x in sys.argv[1:]] if len(sys.argv) > 1 else sorted(hits)
for f in only:
    end = None
    for s in starts:
        if s > f:
            end = s
            break
    end = min(end or N, f + 0x400)
    print(f"\n{'='*70}\nfunc 0x{f:05x} .. 0x{end:05x}")
    md2 = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
    md2.skipdata = True
    for ins in md2.disasm(d[f:end], f):
        op = ins.op_str
        mark = ""
        if 0x40004000 <= (ins.address & ~1) < 0x40005000:
            mark = "   <<ADDR>>"
        # подсветить литералы из пула, попадающие в диапазон
        if ins.mnemonic in ("ldr", "ldr.w") and "[pc" in op:
            try:
                k = int(op.split("#")[1].split("]")[0], 16)
                base = (ins.address + 4) & ~3
                w = struct.unpack_from("<I", d, base + k)[0] if base + k + 4 <= N else 0
                if 0x40004000 <= w < 0x40005000:
                    mark = f"   <<LIT {w:#010x}>>"
            except (ValueError, IndexError):
                pass
        print(f"  {ins.address:05x}: {ins.mnemonic:<8} {op}{mark}")
