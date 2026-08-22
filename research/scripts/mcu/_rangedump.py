# -*- coding: utf-8 -*-
"""Дизассемблер произвольного диапазона mcu_0007.bin с резолвом literal-пулов."""
import os, struct, sys
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB

IMG = os.path.join(os.path.dirname(__file__), "..", "..", "images", "mcu_0007.bin")
d = open(IMG, "rb").read()
N = len(d)
a, b = int(sys.argv[1], 16), int(sys.argv[2], 16)
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
md.skipdata = True

def lit_at(ins):
    """Если инструкция ldr rX,[pc,#k] — вернуть значение из пула."""
    if ins.mnemonic in ("ldr", "ldr.w") and "[pc" in ins.op_str:
        try:
            k = int(ins.op_str.split("#")[1].split("]")[0], 16)
            base = (ins.address + 4) & ~3
            off = base + k
            if 0 <= off + 4 <= N:
                return struct.unpack_from("<I", d, off)[0]
        except (ValueError, IndexError):
            pass
    return None

for ins in md.disasm(d[a:b], a):
    extra = ""
    v = lit_at(ins)
    if v is not None:
        tag = ""
        if 0x20000000 <= v < 0x20020000:
            tag = "RAM"
        elif 0x40000000 <= v < 0x40100000:
            tag = "PERIPH"
        elif a - 0x800 <= v < b + 0x800:
            tag = "CODE?"
        extra = f"   <<{v:#010x} {tag}>>"
    print(f"{ins.address:05x}: {ins.mnemonic:<8} {ins.op_str}{extra}")
