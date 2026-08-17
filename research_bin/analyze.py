#!/usr/bin/env python3
"""Статический анализ прошивки RTL8762C (ARM Cortex-M). Часть 1: структура."""
import sys, math, re, struct, collections

FW = sys.argv[1] if len(sys.argv) > 1 else "ble_2.7.0_0015.bin"
d = open(FW, "rb").read()
print(f"файл: {FW}  размер: {len(d)} байт (0x{len(d):x})\n")

# --- заголовок ---
print("=== первые 64 байта ===")
for off in range(0, 64, 16):
    row = d[off:off+16]
    print(f"  {off:04x}: {row.hex(' ')}  {''.join(chr(c) if 32<=c<127 else '.' for c in row)}")

# --- энтропия по блокам 1К ---
def entropy(b):
    if not b: return 0
    cnt = collections.Counter(b); n = len(b)
    return -sum((c/n)*math.log2(c/n) for c in cnt.values())

print("\n=== энтропия по блокам 1КБ (8.0=шум/шифр, ~6-7=код, <5=данные/паддинг) ===")
BLK = 1024
prev = None
for i in range(0, len(d), BLK):
    e = entropy(d[i:i+BLK])
    tag = "шум/crypt" if e > 7.5 else ("код?" if e > 5.5 else "данные/pad")
    # печатаем только смену режима, чтобы не заваливать
    mode = tag
    if mode != prev:
        print(f"  0x{i:05x}: E={e:.2f}  {tag}")
        prev = mode
print(f"  (всего блоков: {(len(d)+BLK-1)//BLK})")

# --- байтовая статистика хвоста (трейлер/подпись?) ---
tail = d[296*512:]
print(f"\n=== хвост после 296*512=0x{296*512:x} ({len(tail)} байт) ===")
print(f"  E(tail)={entropy(tail):.2f}")
print(f"  hex[:64]: {tail[:64].hex(' ')}")

# --- строки ---
strs = [(m.start(), m.group().decode('ascii','ignore'))
        for m in re.finditer(rb'[ -~]{4,}', d)]
print(f"\n=== строк ASCII (>=4): {len(strs)} ===")
kw = ['release','version','rtl','dreame','scooter','xiaomi','mi ','ble','ota','boot',
      'error','fail','battery','motor','speed','lock','brake','light','uart','key',
      'debug','assert','.c','build','gcc','app','stack','bms','charge']
hits = [(o,s) for o,s in strs if any(k in s.lower() for k in kw)]
for o,s in hits[:60]:
    print(f"  0x{o:05x}: {s[:80]}")
print(f"  ... (совпало {len(hits)} строк по ключевым словам)")
