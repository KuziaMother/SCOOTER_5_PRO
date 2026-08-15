#!/usr/bin/env python3
"""MCU реверс ч.2: xref функция->периферия, дизасм мотор/ADC-функций, поиск параметров."""
import sys, struct, bisect
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN
d = open("mcu_0007.bin", "rb").read(); N = len(d)
u32 = lambda o: struct.unpack_from("<I", d, o)[0]
u16 = lambda o: struct.unpack_from("<H", d, o)[0]

# code-секции (из части 1)
CODE = [(0x01200,0x02400),(0x02600,0x10200),(0x10400,0x10e00),(0x11000,0x12400),
        (0x12800,0x13e00),(0x14200,0x14400),(0x14600,0x17a00),(0x18000,0x18200),
        (0x18e00,0x19200),(0x19a00,0x24200),(0x24400,0x24600)]
def in_code(o): return any(a<=o<b for a,b in CODE)

# границы функций = push {..,lr}
fstarts = sorted(o for a,b in CODE for o in range(a,b,2) if (u16(o)&0xFF00)==0xB500)
def func_of(o):
    i = bisect.bisect_right(fstarts, o) - 1
    return fstarts[i] if i>=0 else None

PERI = {0x40012c00:"TIM1(motor-PWM)",0x40012400:"ADC1(sense)",0x40021000:"RCC(clock)",
        0x40022000:"FLASH(OTA)",0x40013800:"USART1",0x40004400:"USART2",0x40004800:"USART3",
        0x40005400:"I2C1",0x40013000:"SPI1",0x40000400:"TIM3",0x40000800:"TIM4",
        0x40020000:"DMA1",0x40010800:"GPIOA",0x40010c00:"GPIOB",0x40011000:"GPIOC",
        0x40011400:"GPIOD",0x40006400:"CAN1",0x40007000:"PWR/DAC",0x40003000:"TIM/WDG"}

# xref: для каждого вхождения периф-базы как u32 в коде -> функция
func_peri = {}
for o in range(0,N-4,4):
    if not in_code(o): continue
    v = u32(o)
    if v in PERI:
        f = func_of(o)
        if f is not None:
            func_peri.setdefault(f,{}).setdefault(PERI[v],0)
            func_peri[f][PERI[v]] += 1

print(f"[i] функций в коде: {len(fstarts)};  функций, трогающих известную периферию: {len(func_peri)}\n")
print("=== функции по периферии (motor/sense/comms/flash) ===")
def has(f,sub): return any(sub in k for k in func_peri[f])
for label,key in [("МОТОР (TIM1)","TIM1"),("ДАТЧИКИ (ADC1)","ADC1"),
                  ("СВЯЗЬ (USART)","USART"),("OTA (FLASH)","FLASH"),("CAN","CAN")]:
    fs=[f for f in func_peri if has(f,key)]
    print(f"\n-- {label}: {len(fs)} функц.")
    for f in sorted(fs)[:10]:
        peris=", ".join(f"{k}x{v}" for k,v in func_peri[f].items())
        print(f"   func_0x{f:05x}: {peris}")

# ---------- дизасм самой «мотор-ёмкой» функции (макс TIM1+ADC) ----------
def score(f): return sum(v for k,v in func_peri[f].items() if "TIM1" in k or "ADC" in k)
motor = max(func_peri, key=score) if func_peri else None
if motor and score(motor)>0:
    end = fstarts[bisect.bisect_right(fstarts,motor)] if bisect.bisect_right(fstarts,motor)<len(fstarts) else motor+256
    end = min(end, motor+400)
    print(f"\n=== дизасм мотор-функции func_0x{motor:05x} (периф: {func_peri[motor]}) ===")
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB|CS_MODE_LITTLE_ENDIAN)
    n=0
    for ins in md.disasm(d[motor:end], motor):
        print(f"   0x{ins.address:05x}: {ins.mnemonic:8} {ins.op_str}")
        n+=1
        if n>=48: break
