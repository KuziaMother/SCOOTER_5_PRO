#!/usr/bin/env python3
"""A1 (GPIO): дизасм драйвера портов 0x22000 — сигнатура + регистры, которые он пишет.
Подсвечиваем все обращения к 0x48000xxx (кастомный GPIO-блок) и ldr/str с pool-константами."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from capstone import *

FW = os.path.join(os.path.dirname(__file__), "..", "..", "images", "mcu_0007.bin")
fw = open(FW, "rb").read()

def disasm(off, n=0x200):
    code = fw[off:off+n]
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    md.detail = True
    for i in md.disasm(code, off):
        # подсветка обращений к GPIO-блоку 0x48000xxx
        mark = "   <<<GPIO" if "0x48000" in i.op_str or "r12" in i.mnemonic else ""
        print(f"  0x{i.address:05x}: {i.mnemonic:<6} {i.op_str}{mark}")

print("=== драйвер портов 0x22000 ===")
disasm(0x22000, 0x180)
