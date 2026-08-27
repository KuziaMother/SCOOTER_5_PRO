#!/usr/bin/env python3
"""Дамп ramp-core 0x1d078 с авторитетной резолвцией ldr [pc,#imm].
Считаем pool-target = ((addr+4)&~3) + imm по raw-байтам (не доверяя capstone-immediates),
cross-check с адресами из трассы: 0x263 (гейт), 0x388, 0x224."""
import capstone

D = open('research/images/mcu_0007.bin', 'rb').read()
FLASH = 0x08000000


def pool_word(off):
    return int.from_bytes(D[off:off + 4], 'little')


# literal-пул функции (из func_0x1d078.md @0x1d2dc)
POOL_BASE = 0x1d2dc
POOL = [pool_word(POOL_BASE + 4 * i) for i in range(21)]
print("=== literal-пул @0x1d2dc ===")
for i, w in enumerate(POOL):
    tag = ''
    if 0x20000000 <= w < 0x20003000:
        tag = f"RAM+0x{w - 0x20000000:03x}"
    print(f"  [{i:2d}] @0x{POOL_BASE + 4*i:05x} = {w:#010x} {tag}")

print("\n=== ramp-core дизассемблер (0x1d0f2..0x1d2cc) ===")
md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_THUMB)
start, end = 0x1d0f2, 0x1d2cc
for i in md.disasm(D[start:end], FLASH + start):
    a = i.address - FLASH
    s = f"{a:05x}: {i.mnemonic:<6} {i.op_str}"
    # резолвция ldr rX, [pc, #imm]
    if i.mnemonic == 'ldr' and '[pc' in i.op_str:
        import re
        m = re.search(r'#(0x[0-9a-f]+|\d+)', i.op_str)
        if m:
            imm = int(m.group(1), 0)
            tgt = ((i.address - FLASH + 4) & ~3) + imm
            # найди pool-индекс
            pi = (tgt - POOL_BASE) // 4
            pw = POOL[pi] if 0 <= pi < len(POOL) else None
            tag = ''
            if pw is not None and 0x20000000 <= pw < 0x20003000:
                tag = f"RAM+0x{pw - 0x20000000:03x}"
            elif pw is not None:
                tag = f"const {pw:#x} ({pw})"
            print(f"        ↳ pool[{pi}] tgt=0x{tgt:05x} word={('#%x' % pw) if pw else '?'} {tag}")
    print(s)
