#!/usr/bin/env python3
"""
Статический поиск доступов «RAM-база + смещение» к полям RX-телеметрии.

Дополнение к mcu_consumers.py: ловит паттерн, который пропускает чистый
pool-скан —
    ldr rB, [pc,#imm]      ; rB = 0x20000000 (RAM-база из пула)
    ...
    ldrb/ldrh/ldr rX, [rB, #off]   или  [rB, rO] (rO = movw #off)
    add rT, rB, #off;  ldr ... [rT]
Мини-константный пропэгатор по окнам функций (skipdata).

python research_bin/mcu_baseoff.py [--only C42,C43]
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB

FW = os.path.join(HERE, "mcu_0007.bin")
RAM = 0x20000000

TARGETS = [
    ("C41", 0x2b0, 0x2ba), ("C41M", 0x2e8, 0x2f2),
    ("C42", 0x2cb, 0x2d2), ("C43", 0x2d2, 0x2d9),
    ("C45", 0x2da, 0x2e6), ("C44a", 0x2e6, 0x2e8),
    ("C46", 0x2f2, 0x306), ("C44b", 0x306, 0x310),
    ("C48", 0x354, 0x358), ("C49", 0x36a, 0x36c),
    ("C4A", 0x36c, 0x36e), ("B49", 0x1585, 0x1607),
    ("B4A", 0x1607, 0x1690),
]


def target_of(off):
    for name, lo, hi in TARGETS:
        if lo <= off < hi:
            return name
    return None


REGS = {f"r{i}" for i in range(8)} | {"r0", "ip", "lr", "pc", "sl", "fp", "sb"}


def main():
    d = open(FW, "rb").read()
    import importlib.util
    spec = importlib.util.spec_from_file_location("gen_fm", os.path.join(HERE, "gen_functions_mcu.py"))
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    md.skipdata = True
    flist, _, _ = gen.detect_functions(d, md)

    only = None
    for a in sys.argv[1:]:
        if a.startswith("--only"):
            only = set(a.split("=", 1)[1].split(","))

    hits = []
    for fa, fb, _r in flist:
        insns = list(md.disasm(d[fa:fb], fa))
        val = {}   # reg -> constant
        for ins in insns:
            mn = ins.mnemonic
            ops = ins.op_str.replace(" ", "")
            addr = ins.address
            # --- константные присваивания ---
            if mn == "ldr" and "[pc,#" in ops:
                reg = ops.split(",")[0]
                imm = int(ops.split("[pc,#")[1][:-1], 0)
                base = (addr + (4 if len(ins.bytes) == 2 else 8)) & ~3
                pool = base + imm
                v = struct.unpack_from("<I", d, pool)[0] if 0 <= pool < len(d) - 3 else None
                val[reg] = v
            elif mn in ("movw", "movt", "mov.w"):
                reg, imm_s = ops.split(",")
                imm = int(imm_s.lstrip("#"), 16)
                if mn in ("movw", "mov.w"):
                    val[reg] = imm
                else:
                    lo = val.get(reg)
                    if lo is not None:
                        val[reg] = ((imm << 16) | (lo & 0xFFFF))
            elif mn in ("movs", "mov"):
                parts = ops.split(",")
                if len(parts) == 2 and parts[1].startswith("#"):
                    try:
                        v = int(parts[1][1:], 0)
                        val[parts[0]] = v & 0xFFFFFFFF
                    except ValueError:
                        pass
            elif mn in ("adds", "add", "sub", "subs"):
                parts = ops.split(",")
                if len(parts) == 3 and parts[2].startswith("#"):
                    try:
                        imm = int(parts[2][1:], 0)
                        src = val.get(parts[1])
                        if src is not None:
                            v = (src + imm) & 0xFFFFFFFF if mn in ("adds", "add") \
                                else (src - imm) & 0xFFFFFFFF
                            val[parts[0]] = v
                    except ValueError:
                        pass
                elif len(parts) == 3 and parts[1] in val and parts[2] in val:
                    a_, b_ = val[parts[1]], val[parts[2]]
                    val[parts[0]] = (a_ + b_) & 0xFFFFFFFF if mn in ("adds", "add") \
                        else (a_ - b_) & 0xFFFFFFFF
            elif mn in ("ands", "bics", "orrs", "eor"):
                # сбросим, если операнд не константа (грубо)
                parts = ops.split(",")
                if len(parts) == 3 and not parts[2].startswith("#"):
                    val.pop(parts[0], None)
            elif mn in ("ldrb", "ldrh", "ldrsh", "ldr", "strb", "strh", "str",
                        "ldrb.w", "ldrh.w", "ldrsh.w", "ldr.w", "strb.w", "strh.w", "str.w"):
                # память: [base] / [base,#imm] / [base,reg] / [base,reg,#imm]
                if ops.startswith("["):
                    body = ops[1:-1]
                    parts = body.split(",")
                    breg = parts[0].strip()
                    off = 0
                    known_off = True
                    if len(parts) >= 2:
                        p1 = parts[1].strip()
                        if p1.startswith("#"):
                            try:
                                off = int(p1[1:], 0)
                            except ValueError:
                                known_off = False
                        elif p1 in val:
                            off = val[p1]
                        else:
                            known_off = False
                        if len(parts) >= 3 and parts[2].strip().startswith("#"):
                            try:
                                off += int(parts[2].strip()[1:], 0)
                            except ValueError:
                                known_off = False
                    bv = val.get(breg)
                    if bv is not None and known_off and 0 <= off < 0x40000:
                        tgt = (bv + off) & 0xFFFFFFFF
                        tname = target_of(tgt - RAM) if RAM <= tgt < RAM + 0x20000 else None
                        if tname is not None:
                            hits.append((addr, fa, mn, ops, tgt, tname))
                    # load из памяти сбрасывает константность регистра-приёмника
                    if mn.startswith("ldr") and not ops.endswith("]"):
                        pass
                    dst = ins.op_str.split(",")[0].strip()
                    if mn.startswith(("ldr", "ldrb", "ldrh")):
                        val.pop(dst, None)
            else:
                # прочие инструкции — грубо сбрасываем всё (консервативно)
                if mn not in ("nop", "b", "b.w", "cbz", "cbnz", "cmp", "cmn",
                              "tst", "it", "push", "push.w", "pop", "pop.w",
                              "bx", "bl", "blx", "svc"):
                    val = {}

    if only:
        hits = [h for h in hits if h[5] in only]
    print(f"доступов «база+смещение» в целевые диапазоны: {len(hits)}")
    by_t = {}
    for pc, f, mn, ops, tgt, tname in hits:
        by_t.setdefault(tname, []).append((pc, f, mn, ops, tgt))
    for name, lo, hi in TARGETS:
        if only and name not in only:
            continue
        hs = by_t.get(name, [])
        fs = sorted(set(f for _, f, _, _, _ in hs))
        print(f"\n[{name}] 0x{RAM+lo:08x}..0x{RAM+hi:08x}: {len(hs)} доступов; функций: "
              + ", ".join(f"0x{x:05x}" for x in fs))
        for pc, f, mn, ops, tgt in sorted(hs):
            print(f"    0x{pc:05x} (func 0x{f:05x}) {mn} {ops} -> 0x{tgt:08x}")


if __name__ == "__main__":
    main()
