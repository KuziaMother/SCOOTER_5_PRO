# -*- coding: utf-8 -*-
"""Аннотированный дизассемблер окна MCU-образа: ldr rX,[pc,#imm] -> значение слова пула.

Использование: python mcu_annot.py <start> <end> [start end ...]
"""
import os, struct, sys
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(os.path.dirname(HERE))
BIN = os.path.join(RES, "images", "mcu_0007.bin")


def main():
    d = open(BIN, "rb").read()
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    md.detail = False
    args = sys.argv[1:]
    if not args:
        print(__doc__); return
    ranges = [(int(args[i], 16), int(args[i + 1], 16)) for i in range(0, len(args), 2)]
    for a, b in ranges:
        print(f"===== {a:05x}..{b:05x} =====")
        for ins in md.disasm(d[a:b], a):
            extra = ""
            ops = ins.op_str.replace(" ", "")
            if ins.mnemonic == "ldr" and "[pc,#" in ops:
                try:
                    imm_s = ops.split("[pc,#")[1].rstrip("]")
                    imm = int(imm_s, 16) if imm_s.lower().startswith("0x") else int(imm_s)
                    base = (ins.address + (4 if len(ins.bytes) == 2 else 8)) & ~3
                    pool = base + imm
                    if 0 <= pool < len(d) - 3:
                        v = struct.unpack_from("<I", d, pool)[0]
                        tag = ""
                        if 0x20000000 <= v < 0x20001000:
                            tag = f"  RAM off=0x{v-0x20000000:x}"
                        elif 0x40000000 <= v < 0x40030000:
                            tag = "  PERIPH"
                        elif 0x08000000 <= v < 0x08100000:
                            tag = f"  flash-mirror off=0x{v-0x08000000:x}"
                        extra = f"   ; pool@{pool:05x} = 0x{v:08x}{tag}"
                except Exception as e:
                    extra = f"   ; ? {e}"
            print(f"  {ins.address:06x}: {ins.mnemonic:<5s} {ins.op_str}{extra}")


if __name__ == "__main__":
    main()
