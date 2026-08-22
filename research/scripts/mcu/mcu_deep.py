#!/usr/bin/env python3
"""MCU ч.3: дизасм PWM-мотора и USART3-протокола + поиск констант-лимитов."""
import os, sys, struct, bisect, re
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN
IMG = os.path.join(os.path.dirname(__file__), "..", "..", "images", "mcu_0007.bin")
d = open(IMG,"rb").read(); N=len(d)
u16=lambda o: struct.unpack_from("<H",d,o)[0]
u32=lambda o: struct.unpack_from("<I",d,o)[0]
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB|CS_MODE_LITTLE_ENDIAN)

CODE=[(0x01200,0x02400),(0x02600,0x10200),(0x10400,0x10e00),(0x11000,0x12400),
      (0x12800,0x13e00),(0x14200,0x14400),(0x14600,0x17a00),(0x18000,0x18200),
      (0x18e00,0x19200),(0x19a00,0x24200),(0x24400,0x24600)]
fstarts=sorted(o for a,b in CODE for o in range(a,b,2) if (u16(o)&0xFF00)==0xB500)
def fend(f):
    i=bisect.bisect_right(fstarts,f)
    return min(fstarts[i] if i<len(fstarts) else f+300, f+300)

def dis(f, lim=42, title=""):
    print(f"\n=== {title} func_0x{f:05x} ===")
    n=0
    for ins in md.disasm(d[f:fend(f)], f):
        # аннотация периф-адресов из literal-пула
        note=""
        if ins.mnemonic=="ldr" and "[pc" in ins.op_str:
            m=re.search(r"#(0x[0-9a-f]+|\d+)",ins.op_str.split(',',1)[1])
            if m:
                imm=int(m.group(1),16) if m.group(1).startswith("0x") else int(m.group(1))
                pool=((ins.address+4)&~3)+imm
                if pool+4<=N:
                    v=u32(pool)
                    P={0x40012c00:"TIM1",0x40012400:"ADC1",0x40013800:"USART1",0x40004800:"USART3",
                       0x40021000:"RCC",0x40022000:"FLASH",0x40010800:"GPIOA",0x40010c00:"GPIOB"}
                    if v in P: note=f"  ; {P[v]}"
                    elif 0x40000000<=v<0x50000000: note=f"  ; PERIPH 0x{v:08x}"
                    elif 0x20000000<=v<0x20040000: note=f"  ; RAM 0x{v:08x}"
        print(f"   0x{ins.address:05x}: {ins.mnemonic:8} {ins.op_str}{note}")
        n+=1
        if n>=lim: break

dis(0x22c70, 44, "МОТОР PWM (TIM1)")
dis(0x1e480, 40, "USART3-обработчик (протокол с BLE)")
dis(0x06230, 40, "FLASH запись (OTA)")

# ---------- поиск констант-лимитов: movw/mov.w с «человеческими» значениями ----------
print("\n=== movw-константы в мотор/лимит-функциях (км/ч×10, мВ, мА, %) ===")
INTEREST=set()
# правдоподобные лимиты самоката
def plausible(v):
    return (v in (5,6,20,25,32) or 40<=v<=320 or   # км/ч, км/ч×10
            v in (250,200,300,150,100) or
            3000<=v<=5500 or 30000<=v<=55000 or     # мВ ячейка / АКБ
            1000<=v<=60000)
cnt=0
for a,b in CODE:
    for ins in md.disasm(d[a:b], a):
        if ins.mnemonic in ("movw","mov.w","movs","mov") and "#" in ins.op_str:
            m=re.search(r"#(0x[0-9a-f]+|\d+)$",ins.op_str)
            if m:
                v=int(m.group(1),16) if m.group(1).startswith("0x") else int(m.group(1))
                if plausible(v) and v not in (0,1):
                    INTEREST.add((ins.address,v))
# сгруппируем часто встречающиеся значения
from collections import Counter
vals=Counter(v for _,v in INTEREST)
print("  частые «осмысленные» immediate-значения:")
for v,c in vals.most_common(30):
    hint=""
    if 200<=v<=320: hint="~км/ч×10? (25.0=250)"
    if 3200<=v<=4300: hint="~мВ ячейки Li-ion"
    if 30000<=v<=44000: hint="~мВ батареи"
    print(f"    {v:6}  x{c:<3} {hint}")
