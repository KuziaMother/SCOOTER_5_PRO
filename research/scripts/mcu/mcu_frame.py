#!/usr/bin/env python3
"""MCU ч.5: декодирование протокола 55AA — sync-слово, TX-сборка, checksum, дескрипторы."""
import os, struct, re, bisect
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN
IMG = os.path.join(os.path.dirname(__file__), "..", "..", "images", "mcu_0007.bin")
d=open(IMG,"rb").read(); N=len(d)
u16=lambda o: struct.unpack_from("<H",d,o)[0]; u32=lambda o: struct.unpack_from("<I",d,o)[0]
md=Cs(CS_ARCH_ARM,CS_MODE_THUMB|CS_MODE_LITTLE_ENDIAN); md.detail=False

CODE=[(0x01200,0x02400),(0x02600,0x10200),(0x10400,0x10e00),(0x11000,0x12400),
      (0x12800,0x13e00),(0x14200,0x14400),(0x14600,0x17a00),(0x18000,0x18200),
      (0x18e00,0x19200),(0x19a00,0x24200),(0x24400,0x24600)]
fstarts=sorted(o for a,b in CODE for o in range(a,b,2) if (u16(o)&0xFF00)==0xB500)
def func_of(o):
    i=bisect.bisect_right(fstarts,o)-1; return fstarts[i] if i>=0 else None

# 1) поиск immediate 0x55/0xAA/0x55AA/0xAA55 в cmp/movw/movs
print("=== immediate 0x55/0xAA/0x55AA/0xAA55 в коде ===")
targets={0x55:'0x55',0xAA:'0xAA',0x55AA:'0x55AA',0xAA55:'0xAA55'}
for a,b in CODE:
    for ins in md.disasm(d[a:b],a):
        m=re.search(r"#(0x[0-9a-f]+|\d+)$",ins.op_str)
        if not m: continue
        v=int(m.group(1),16) if m.group(1).startswith('0x') else int(m.group(1))
        if v in targets and ins.mnemonic in ("cmp","cmp.w","movs","mov.w","movw","subs"):
            print(f"  func_0x{func_of(ins.address):05x} 0x{ins.address:05x}: {ins.mnemonic} {ins.op_str}")

# 2) кто ссылается на TX-шаблон/таблицы 0x17d3a (55 aa ...)
print("\n=== ссылки на блок 0x17d20-0x17d80 (конфиг+55AA+коммутация) ===")
lo,hi=0x17d20,0x17d80
for a,b in CODE:
    for ins in md.disasm(d[a:b],a):
        if ins.mnemonic=="ldr" and "[pc" in ins.op_str:
            m=re.search(r"#(0x[0-9a-f]+|\d+)",ins.op_str.split(',',1)[1])
            if m:
                imm=int(m.group(1),16) if m.group(1).startswith('0x') else int(m.group(1))
                pool=((ins.address+4)&~3)+imm
                if pool+4<=N and lo<=u32(pool)<hi:
                    print(f"  func_0x{func_of(ins.address):05x} @0x{ins.address:05x} -> 0x{u32(pool):05x}")

# 3) поиск checksum-паттернов: сумма байт (add в цикле) или CRC-таблицы рядом с USART3
print("\n=== таблицы CRC16 (0x1021/0xA001 poly) ===")
for poly_name,first in [("CRC16-CCITT",b"\x00\x00\x21\x10"),("CRC16-MODBUS",b"\x00\x00\x01\xc0")]:
    i=d.find(first); print(f"  {poly_name}: {'@0x%x'%i if i>=0 else 'нет'}")

# 4) дизасм TX-сборки 0x1f6b4 подробнее (какие байты кладёт в кадр)
print("\n=== TX-сборка func_0x1f6b4 (какие поля пишет) ===")
n=0
for ins in md.disasm(d[0x1f6b4:0x1f6b4+120],0x1f6b4):
    print(f"   0x{ins.address:05x}: {ins.mnemonic:8} {ins.op_str}")
    n+=1
    if n>=52: break
