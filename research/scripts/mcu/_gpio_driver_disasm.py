#!/usr/bin/env python3
"""A1 (GPIO): disassembly of port driver 0x22000 — signature + registers it writes.
Highlight all accesses to 0x48000xxx (custom GPIO block) and ldr/str with pool constants."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs

FW = os.path.join(os.path.dirname(__file__), "..", "..", "images", "mcu_0007.bin")
fw = open(FW, "rb").read()

def disasm(off, n=0x200):
    code = fw[off:off+n]
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    md.detail = True
    for i in md.disasm(code, off):
        # highlight accesses to GPIO block 0x48000xxx
        mark = "   <<<GPIO" if "0x48000" in i.op_str or "r12" in i.mnemonic else ""
        print(f"  0x{i.address:05x}: {i.mnemonic:<6} {i.op_str}{mark}")

print("=== port driver 0x22000 ===")
disasm(0x22000, 0x180)
