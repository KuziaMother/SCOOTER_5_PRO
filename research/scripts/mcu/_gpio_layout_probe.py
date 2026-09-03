#!/usr/bin/env python3
"""A1 (GPIO): эмпирический layout портового блока. Прогоняем motor-init функции,
которые вызывают драйвер 0x22000, и ловим записи в 0x48000xxx (offset + value + pc)."""
import sys, os, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "emulator"))
from mcu_emu import McuEmu

def run_and_dump(entry, label):
    emu = McuEmu(max_insn=500_000)
    emu.run_func(entry)
    print(f"\n===== {label} (0x{entry:05x}) — записи в 0x48000xxx =====")
    by = collections.defaultdict(list)
    for pc, addr, size, val in emu.periph_writes:
        if 0x48000000 <= addr < 0x48020000:
            by[addr].append((pc, size, val))
    if not by:
        print("  (записей в портовый блок нет)")
        return
    for base in sorted(set(a & ~0x3FF for a in by)):
        addrs = [a for a in by if (a & ~0x3FF) == base]
        print(f"  порт-база 0x{base:08x}:")
        for a in sorted(addrs):
            ws = by[a]
            vals = sorted(set(v for _, s, v in ws))
            pcs = sorted(set(p for p, _, _ in ws))
            print(f"    +0x{a-base:03x} (size{'/'.join(hex(s) for s in sorted(set(s for _,s,_ in ws)))}): "
                  f"W×{len(ws)} vals={vals[:10]} pc={pcs[:5]}")

if __name__ == "__main__":
    run_and_dump(0x1BF48, "МОТОР-ИНИТ 0x1bf48")
    run_and_dump(0x1D640, "PWM-init 0x1d640")
