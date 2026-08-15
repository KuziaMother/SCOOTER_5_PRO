#!/usr/bin/env python3
"""Крипто-анализ зашифрованной части BLE fw: AES vs сжатие, поиск ключа/S-box, режим."""
import sys, struct, collections, math

FW = sys.argv[1] if len(sys.argv) > 1 else "ble_2.7.0_0015.bin"
d = open(FW, "rb").read()
ENC = (0x0a200, 0x25400)     # главный зашифрованный блок
enc = d[ENC[0]:ENC[1]]
print(f"enc-блок 0x{ENC[0]:x}-0x{ENC[1]:x}, {len(enc)} байт")

# 1) AES-ECB? ищем повторяющиеся 16-байтовые блоки
print("\n=== 1) повтор 16-байтовых блоков (признак AES-ECB) ===")
blocks = [enc[i:i+16] for i in range(0, len(enc)-15, 16)]
cnt = collections.Counter(blocks)
rep = [(b, c) for b, c in cnt.items() if c > 1]
print(f"  всего блоков={len(blocks)}, уникальных={len(cnt)}, повторяющихся={len(rep)}")
if rep:
    rep.sort(key=lambda x: -x[1])
    for b, c in rep[:3]:
        print(f"    x{c}: {b.hex()}")
print("  -> много повторов = ECB; ноль повторов = CBC/CTR/поток/сжатие")

# 2) сигнатуры сжатия в начале enc и по всему файлу
print("\n=== 2) сигнатуры сжатия ===")
sigs = {b"\x1f\x8b": "gzip", b"\x5d\x00\x00": "lzma", b"\x04\x22\x4d\x18": "lz4",
        b"PK\x03\x04": "zip", b"\x28\xb5\x2f\xfd": "zstd", b"BZh": "bzip2",
        b"\x89LZO": "lzo"}
for sig, name in sigs.items():
    i = d.find(sig)
    print(f"  {name:6}: {'@0x%x'%i if i>=0 else 'нет'}")

# 3) AES S-box / T-box в открытой части (признак программного AES + возможного ключа рядом)
SBOX = bytes([0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76])
INV  = bytes([0x52,0x09,0x6a,0xd5,0x30,0x36,0xa5,0x38,0xbf,0x40,0xa3,0x9e,0x81,0xf3,0xd7,0xfb])
te0  = bytes.fromhex("c66363a5")  # начало T-таблицы AES (частый вариант)
print("\n=== 3) таблицы AES в образе ===")
for name, sig in [("S-box", SBOX), ("Inv-S-box", INV), ("Te0", te0)]:
    i = d.find(sig)
    print(f"  {name:10}: {'@0x%x'%i if i>=0 else 'нет'}")

# 4) кандидаты ключей: 16/32-байтовые высокоэнтропийные константы в открытых секциях
def ent(b):
    if not b: return 0
    c = collections.Counter(b); n=len(b)
    return -sum((x/n)*math.log2(x/n) for x in c.values())
plain = [(0x400,0x2a00),(0x6000,0xa200)]
print("\n=== 4) высокоэнтропийные 16/32-б константы в открытом коде (кандидаты в ключи) ===")
found=0
for a,b in plain:
    reg=d[a:b]
    for i in range(0,len(reg)-32,4):
        w=reg[i:i+32]
        if len(set(w))>=26 and ent(w)>4.3:   # почти все байты уникальны
            # исключим явные строки
            if sum(32<=c<127 for c in w) < 20:
                print(f"  0x{a+i:05x}: {w.hex()}")
                found+=1
                if found>=8: break
    if found>=8: break
if not found: print("  (не найдено очевидных 16/32-б ключей в открытом коде)")

# 5) распределение первых байт enc (IV?)
print("\n=== 5) первые 48 байт enc-блока ===")
print("  ", enc[:48].hex(' '))
print(f"  энтропия всего enc: {ent(enc):.3f}  (16.0 макс.=8.0)")
