#!/usr/bin/env python3
"""Дизассемблер с резолвом literal-пулов для ручного анализа функций MCU.

python research_bin/mcu_disasm.py 0x1a938 0x1b67c [--pool]
Для каждого ldr rX,[pc,#imm] печатает слово пула; для movw/movt — значение;
подсвечивает обращения к целевым RAM-адресам RX-телеметрии.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB

FW = os.path.join(HERE, "mcu_0007.bin")
RAM = 0x20000000

# целевые поля RX (для подсветки)
FIELDS = {
    0x2b0: "41.u16BE", 0x2b2: "41.lo", 0x2b3: "41.hi", 0x2b4: "41.b6",
    0x2b5: "41.bit7", 0x2b6: "41.z", 0x2b7: "41.b7", 0x2b8: "41.b8",
    0x2b9: "41.b9",
    0x2cb: "42.b0", 0x2cc: "42.b1", 0x2cd: "42.b2", 0x2ce: "42.b3",
    0x2cf: "42.b4", 0x2d0: "42.b5", 0x2d1: "42.b6",
    0x2d2: "43.b0", 0x2d3: "43.b1", 0x2d4: "43.b2", 0x2d5: "43.b3",
    0x2d6: "43.b4", 0x2d7: "43.b5", 0x2d8: "43.b6",
    0x2da: "45.u0", 0x2dc: "45.u1", 0x2de: "45.u2", 0x2e0: "45.u3",
    0x2e2: "45.u4", 0x2e4: "45.u5", 0x2e7: "45.bf",
    0x2e6: "44.b3", 0x306: "44.b4", 0x308: "44.u16a", 0x30a: "44.u16b",
    0x30c: "44.b9", 0x30e: "44.u16c",
    0x2f2: "46.buf", 0x354: "48.b0", 0x355: "48.b1", 0x356: "48.b2",
    0x357: "48.b3", 0x36a: "49.len", 0x36c: "4A.len",
    0x1585: "49.data", 0x1607: "4A.data",
}


def field_tag(v):
    off = v - RAM
    if off in FIELDS:
        return f"  <<< {FIELDS[off]}"
    # диапазон буфера 46
    if 0x2f2 <= off < 0x306:
        return f"  <<< 46.buf[{off-0x2f2}]"
    return ""


def main():
    d = open(FW, "rb").read()
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    show_pool = "--pool" in sys.argv[1:]
    if not args:
        print(__doc__)
        return
    for spec in args:
        if "-" in spec:
            a, b = (int(x, 16) for x in spec.split("-"))
        else:
            a = int(spec, 16)
            b = a + 0x200
        print(f"\n{'='*70}\n=== 0x{a:05x}..0x{b:05x} ===")
        for ins in md.disasm(d[a:b], a):
            extra = ""
            ops = ins.op_str.replace(" ", "")
            if ins.mnemonic == "ldr" and "[pc,#" in ops:
                imm = int(ops.split("[pc,#")[1][:-1], 0)
                base = (ins.address + (4 if len(ins.bytes) == 2 else 8)) & ~3
                pool = base + imm
                if 0 <= pool < len(d) - 3:
                    v = struct.unpack_from("<I", d, pool)[0]
                    extra = f"  ; pool@0x{pool:05x} = 0x{v:08x}{field_tag(v)}"
            elif ins.mnemonic in ("movw", "movt"):
                pass
            print(f"{ins.address:06x}: {ins.mnemonic:<8s} {ins.op_str}{extra}")


if __name__ == "__main__":
    main()
