#!/usr/bin/env python3
"""RTL8762C fw, часть 3: дизасм открытого bootloader/DFU-кода в функции + имена по строкам."""
import sys, re, struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN

FW = sys.argv[1] if len(sys.argv) > 1 else "ble_2.7.0_0015.bin"
d = open(FW, "rb").read()
N = len(d)

# строки: offset -> текст
strings = {m.start(): m.group().decode('ascii','ignore')
           for m in re.finditer(rb'[ -~]{4,}', d)}
str_offs = set(strings)

# --- калибровка базы загрузки: перебираем литералы ldr rX,[pc] и ищем базу,
#     при которой (literal - base) попадает на смещения строк максимально часто ---
lit_vals = []
for m in re.finditer(rb'.\x48', d):           # xx 48 = ldr rX,[pc,#imm] (Thumb T1)
    off = m.start()
    if off % 2: continue
    imm = d[off] * 4
    pool = (off + 4) & ~3
    pool += imm
    if pool + 4 <= N:
        lit_vals.append(struct.unpack_from("<I", d, pool)[0])

from collections import Counter
best, best_hits = 0x01800000, -1
for base in (0x01800000, 0x01804000, 0x00000000, 0x01000000, 0x01806000):
    hits = sum(1 for v in lit_vals if (v - base) in str_offs or 0 <= (v-base) < N)
    if hits > best_hits:
        best_hits, best = hits, base
BASE = best
print(f"[i] литералов ldr: {len(lit_vals)}, выбранная база загрузки: 0x{BASE:08x} (hits={best_hits})")
def to_off(vaddr):
    o = vaddr - BASE
    return o if 0 <= o < N else None

md = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
md.detail = True

# открытые code-секции (из части 2)
regions = [(0x00400, 0x02a00), (0x06000, 0x0a200)]

report = open("functions.txt", "w", encoding="utf-8")
total_funcs = 0
for (a, b) in regions:
    report.write(f"\n===== СЕКЦИЯ 0x{a:05x}-0x{b:05x} (vaddr 0x{BASE+a:08x}) =====\n")
    # найдём границы функций по прологам push {..,lr}
    starts = []
    for off in range(a, b, 2):
        w = struct.unpack_from("<H", d, off)[0]
        if (w & 0xFF00) == 0xB500:          # push {..,lr}
            starts.append(off)
    starts.append(b)
    for i in range(len(starts)-1):
        fa, fb = starts[i], starts[i+1]
        if fb - fa < 4: continue
        total_funcs += 1
        refs = []
        for ins in md.disasm(d[fa:fb], BASE+fa):
            # ldr rX,[pc,#imm] -> литерал -> строка?
            if ins.mnemonic == "ldr" and "[pc" in ins.op_str:
                mm = re.search(r"#(0x[0-9a-f]+|\d+)", ins.op_str.split(',',1)[1])
                if mm:
                    imm = int(mm.group(1), 16) if mm.group(1).startswith("0x") else int(mm.group(1))
                    pool = ((ins.address + 4) & ~3) + imm - BASE
                    if 0 <= pool+4 <= N:
                        v = struct.unpack_from("<I", d, pool)[0]
                        so = to_off(v)
                        if so in strings:
                            refs.append(strings[so])
        fname = ""
        if refs:
            fname = " | strings: " + "; ".join(dict.fromkeys(refs))[:120]
        report.write(f"  func_0x{fa:05x} (vaddr 0x{BASE+fa:08x}, {fb-fa}B){fname}\n")
report.close()
print(f"[i] найдено функций: {total_funcs} -> functions.txt")

# сводка: функции, ссылающиеся на говорящие строки
print("\n=== функции с узнаваемыми строками (bootloader/DFU/flash) ===")
key = ['dfu','image','flash','eras','unlock','bank','ota','boot','reset','crc','valid',
       'timer','packet','write','key','sign','cert','version']
cnt = 0
for line in open("functions.txt", encoding="utf-8"):
    if "strings:" in line and any(k in line.lower() for k in key):
        print("  " + line.strip()[:150]); cnt += 1
        if cnt >= 40: break
