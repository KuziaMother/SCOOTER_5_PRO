# -*- coding: utf-8 -*-
"""Покрытие известных функций + bl-таргеты как старты."""
import os, struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB

IMG = os.path.join(os.path.dirname(__file__), "..", "..", "images", "mcu_0007.bin")
d = open(IMG, "rb").read()
N = len(d)
CODE = [(0x01200, 0x02400), (0x02600, 0x10200), (0x10400, 0x10e00),
        (0x11000, 0x12400), (0x12800, 0x13e00), (0x14200, 0x14400),
        (0x14600, 0x17a00), (0x18e00, 0x19200), (0x19a00, 0x24200),
        (0x24400, 0x24600)]

b5, t32 = set(), set()
for (a, b) in CODE:
    i = a
    while i + 2 <= b:
        w = struct.unpack_from("<H", d, i)[0]
        if (w & 0xFF00) == 0xB500 and (w & 0x0100):
            b5.add(i)
        if (w & 0xFF80) == 0xE900 and i + 4 <= b:
            t32.add(i)
        i += 2

md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
bl_targets = set()
for (a, b) in CODE:
    for ins in md.disasm(d[a:b], a):
        if ins.mnemonic in ("bl", "blx") and ins.size == 4:
            try:
                t = int(ins.op_str, 16)
            except ValueError:
                continue
            # Thumb-таргет: capstone пишет без бита T; в файле адрес = t & ~1
            if any(a2 <= (t & ~1) < b2 for (a2, b2) in CODE):
                bl_targets.add(t & ~1)

print(f"B5xx={len(b5)}, T32={len(t32)}, union={len(b5|t32)}, bl_targets(in code)={len(bl_targets)}")
new_from_bl = bl_targets - b5 - t32
print(f"bl targets NOT in prologue set: {len(new_from_bl)}")

known = {0x1e9e0: "RX parser entry", 0x1e480: "ISR USART3", 0x1f600: "poll scheduler",
         0x23188: "HAL_UART_Transmit", 0x1f1c0: "usart3_send_byte", 0x06230: "flash program",
         0x1a31c: "ADC state machine", 0x22c70: "TIM PWM config", 0x1e298: "DMA+ADC",
         0x1e2f8: "RCC+TIM1 init", 0x1302c: "uart init", 0x21ca8: "adc?", 0x1c0b0: "adc?",
         0x11cb4: "OTA RCC+PWR+FLASH", 0x06304: "flash?", 0x1f6b4: "TX desc build"}
print("\n== known functions coverage (B5xx/T32/BL):")
for a, name in sorted(known.items()):
    marks = ("B" if a in b5 else "-") + ("T" if a in t32 else "-") + ("L" if a in bl_targets else "-")
    print(f"   {a:05x} {marks}  {name}")

# что за первые инструкции у 0x1e9e0 и других не-прологов?
print("\n== first bytes of non-prologue known fns:")
for a in sorted(known):
    if a not in b5 and a not in t32:
        row = d[a:a+8]
        hexs = " ".join(f"{b:02x}" for b in row)
        dec = []
        for ins in md.disasm(d[a:a+12], a):
            dec.append(f"{ins.mnemonic} {ins.op_str}")
            if len(dec) >= 3:
                break
        print(f"   {a:05x}: {hexs} | {' ; '.join(dec)}")

# топ bl-таргетов, которых нет в прологах (сколько уникальных, пример)
print(f"\n== sample new-from-bl (first 20): {[hex(x) for x in sorted(new_from_bl)[:20]]}")
