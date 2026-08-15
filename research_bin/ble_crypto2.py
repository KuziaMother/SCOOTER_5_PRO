#!/usr/bin/env python3
"""BLE: связь двух шифроблоков, структура блоков, заголовок как IV/ключ-кандидат."""
import struct, math, collections
d=open("ble_2.7.0_0015.bin","rb").read(); N=len(d)
def ent(b):
    if not b: return 0
    c=collections.Counter(b); n=len(b)
    return -sum((x/n)*math.log2(x/n) for x in c.values())

ENC1=(0x3000,0x5e00); ENC2=(0xa200,0x25400)
e1=d[ENC1[0]:ENC1[1]]; e2=d[ENC2[0]:ENC2[1]]
print(f"ENC1 0x{ENC1[0]:x}-0x{ENC1[1]:x} ({len(e1)}B) E={ent(e1):.3f}")
print(f"ENC2 0x{ENC2[0]:x}-0x{ENC2[1]:x} ({len(e2)}B) E={ent(e2):.3f}")
print(f"len%16: ENC1={len(e1)%16}, ENC2={len(e2)%16}  (0 => блочный шифр 16Б)")

# первые/последние 32 байта — совпадают ли начала (одинаковый IV/ключ => одинаковый префикс маловероятен, но полезно)
print(f"\nENC1[:32] {e1[:32].hex()}")
print(f"ENC2[:32] {e2[:32].hex()}")
print(f"ENC1[-16:] {e1[-16:].hex()}")
print(f"ENC2[-16:] {e2[-16:].hex()}")

# повторяющиеся 16-Б блоки внутри и МЕЖДУ регионами (ECB / общий кейстрим)
b1=[e1[i:i+16] for i in range(0,len(e1)-15,16)]
b2=[e2[i:i+16] for i in range(0,len(e2)-15,16)]
c1=collections.Counter(b1); c2=collections.Counter(b2)
inter=set(c1)&set(c2)
print(f"\nповтор 16Б внутри ENC1: {sum(v-1 for v in c1.values() if v>1)}")
print(f"повтор 16Б внутри ENC2: {sum(v-1 for v in c2.values() if v>1)}")
print(f"общих 16Б блоков между ENC1/ENC2: {len(inter)}")

# заголовок: 16-байтовый GUID @0xc — кандидат IV/key
hdr16=d[0x0c:0x1c]
print(f"\nheader[0x0c:0x1c] (16Б, IV/key-кандидат): {hdr16.hex()}")
print(f"header[0x00:0x0c]: {d[0:0x0c].hex()}")
# энтропия окон по всему файлу с шагом 256 — точные границы шифрования
print("\n=== точные границы (шаг 256Б, E) ===")
prev=None
for i in range(0,N,256):
    e=ent(d[i:i+256]); k='ENC' if e>7.4 else ('code' if e>5.0 else 'data')
    if k!=prev: print(f"  0x{i:05x}: E={e:.2f} {k}"); prev=k

# XOR соседних 16-Б блоков ENC2: если CBC, разности случайны; ищем структурные нули
z=sum(1 for i in range(0,len(e2)-16,16) if e2[i:i+16]==e2[i+16:i+32])
print(f"\nсоседние одинаковые 16Б в ENC2: {z} (>0 => участки констант/паддинга под ECB)")
