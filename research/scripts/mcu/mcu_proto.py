#!/usr/bin/env python3
"""MCU ч.4: протокол USART3 (заголовки/парсер/CRC) + признаки типа мотор-управления."""
import os, struct, re, bisect
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN
IMG = os.path.join(os.path.dirname(__file__), "..", "..", "images", "mcu_0007.bin")
d=open(IMG,"rb").read(); N=len(d)
u16=lambda o: struct.unpack_from("<H",d,o)[0]
u32=lambda o: struct.unpack_from("<I",d,o)[0]
s16=lambda o: struct.unpack_from("<h",d,o)[0]
md=Cs(CS_ARCH_ARM,CS_MODE_THUMB|CS_MODE_LITTLE_ENDIAN)

CODE=[(0x01200,0x02400),(0x02600,0x10200),(0x10400,0x10e00),(0x11000,0x12400),
      (0x12800,0x13e00),(0x14200,0x14400),(0x14600,0x17a00),(0x18000,0x18200),
      (0x18e00,0x19200),(0x19a00,0x24200),(0x24400,0x24600)]
fstarts=sorted(o for a,b in CODE for o in range(a,b,2) if (u16(o)&0xFF00)==0xB500)
def func_of(o):
    i=bisect.bisect_right(fstarts,o)-1; return fstarts[i] if i>=0 else None
def fend(f):
    i=bisect.bisect_right(fstarts,f); return fstarts[i] if i<len(fstarts) else f+400

# ---- 1) поиск cmp с сигнатурами кадров ----
print("=== сравнения с байтами-заголовками кадра (cmp rX,#imm) ===")
HDR={0x55,0xAA,0x5A,0xA5,0x5B,0xA5,0xf5,0x3e,0x23}
hdrhits={}
for a,b in CODE:
    for ins in md.disasm(d[a:b],a):
        if ins.mnemonic in ("cmp","cmp.w") and re.search(r"#(0x[0-9a-f]+|\d+)$",ins.op_str):
            v=ins.op_str.rsplit("#",1)[1]
            v=int(v,16) if v.startswith("0x") else int(v)
            if v in HDR:
                f=func_of(ins.address)
                hdrhits.setdefault(f,[]).append((ins.address,v))
for f,hs in sorted(hdrhits.items()):
    vs=" ".join(f"0x{v:02x}@0x{a:x}" for a,v in hs)
    print(f"  func_0x{f:05x}: {vs}")

# ---- 2) поиск байтовой сигнатуры 55 AA / 5A A5 в данных ----
print("\n=== сигнатуры кадров в байтах образа ===")
for sig in (b"\x55\xab",b"\x55\xaa",b"\x5a\xa5",b"\xa5\x5a",b"\xaa\x55"):
    i=d.find(sig)
    print(f"  {sig.hex()}: {'@0x%x'%i if i>=0 else 'нет'}")

# ---- 3) таблица синуса (FOC/SVPWM)? ищем массив int16 с синус-профилем ----
print("\n=== поиск таблицы синуса (признак FOC) ===")
found_sin=False
for base in range(0, N-256, 2):
    vals=[s16(base+2*k) for k in range(64)]
    if all(-32768<=v<=32767 for v in vals):
        # монотонный рост затем спад, амплитуда большая
        mx=max(vals); mn=min(vals)
        if mx>20000 and mn<-20000:
            # проверим «гладкость»: соседние разности не скачут дико
            diffs=[abs(vals[k+1]-vals[k]) for k in range(63)]
            if max(diffs)<4000 and vals[0] and abs(vals[0])<3000:
                print(f"  возможная sin-LUT @0x{base:05x}: {vals[:8]} ... max={mx} min={mn}")
                found_sin=True
                break
if not found_sin:
    print("  явной sin-LUT (int16) не найдено -> вероятно трапеция/Холл или таблица инче")

# ---- 4) чтение датчиков Холла: частые чтения GPIO IDR ----
print("\n=== обращения к GPIO IDR (датчики Холла?) ===")
GP={0x40010800:"GPIOA",0x40010c00:"GPIOB",0x40011000:"GPIOC",0x40011400:"GPIOD"}
idr=0
for a,b in CODE:
    for ins in md.disasm(d[a:b],a):
        if ins.mnemonic=="ldr" and "[pc" in ins.op_str:
            m=re.search(r"#(0x[0-9a-f]+|\d+)",ins.op_str.split(',',1)[1])
            if m:
                imm=int(m.group(1),16) if m.group(1).startswith("0x") else int(m.group(1))
                pool=((ins.address+4)&~3)+imm
                if pool+4<=N and u32(pool) in GP: idr+=1
print(f"  ссылок на GPIO-базы: {idr} (Холл читается как IDR смещение +0x08)")
