#!/usr/bin/env python3
"""MCU part 5: decoding 55AA protocol - sync word, TX assembly, checksum, descriptors."""
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

# 1) search for immediate 0x55/0xAA/0x55AA/0xAA55 in cmp/movw/movs
print("=== immediate 0x55/0xAA/0x55AA/0xAA55 in code ===")
targets={0x55:'0x55',0xAA:'0xAA',0x55AA:'0x55AA',0xAA55:'0xAA55'}
for a,b in CODE:
    for ins in md.disasm(d[a:b],a):
        m=re.search(r"#(0x[0-9a-f]+|\d+)$",ins.op_str)
        if not m: continue
        v=int(m.group(1),16) if m.group(1).startswith('0x') else int(m.group(1))
        if v in targets and ins.mnemonic in ("cmp","cmp.w","movs","mov.w","movw","subs"):
            print(f"  func_0x{func_of(ins.address):05x} 0x{ins.address:05x}: {ins.mnemonic} {ins.op_str}")

# 2) who references TX template/tables 0x17d3a (55 aa ...)
print("\n=== references to block 0x17d20-0x17d80 (config+55AA+commutation) ===")
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

# 3) search for checksum patterns: byte sum (add in loop) or CRC tables near USART3
print("\n=== CRC16 tables (0x1021/0xA001 poly) ===")
for poly_name,first in [("CRC16-CCITT",b"\x00\x00\x21\x10"),("CRC16-MODBUS",b"\x00\x00\x01\xc0")]:
    i=d.find(first); print(f"  {poly_name}: {'@0x%x'%i if i>=0 else 'none'}")

# 4) disassemble TX assembly 0x1f6b4 in detail (which bytes placed in frame)
print("\n=== TX assembly func_0x1f6b4 (which fields written) ===")
n=0
for ins in md.disasm(d[0x1f6b4:0x1f6b4+120],0x1f6b4):
    print(f"   0x{ins.address:05x}: {ins.mnemonic:8} {ins.op_str}")
    n+=1
    if n>=52: break
