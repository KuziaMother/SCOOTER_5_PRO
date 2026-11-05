#!/usr/bin/env python3
"""A1 (GPIO model): empirical search for GPIO config in init.

Run init chain through run_broad and group periph_writes by address
to find GPIO base/offsets (chip is custom — GPIO is not on standard STM32F1 base;
comment in mcu_emu.py indicates "GPIO-like" block in PERIPH2 @0x48000C00).
"""
import sys, os, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "emulator"))
from mcu_emu import McuEmu, PERIPH, PERIPH_SIZE, PERIPH2, PERIPH2_SIZE, SYS, SYS_SIZE

def scan(entry, label, budget=3_000_000):
    emu = McuEmu(max_insn=budget)
    emu.run_broad(entry, budget=budget)
    print(f"\n===== {label} (entry 0x{entry:05x}) — periph writes by address =====")
    by = collections.defaultdict(list)
    for pc, addr, size, val in emu.periph_writes:
        by[addr].append((pc, size, val))
    if not by:
        print("  (no writes to peripherals)")
        return
    # group by 0x40-block (base & ~0xFF) to see clusters
    clusters = collections.defaultdict(list)
    for addr in sorted(by):
        clusters[addr & ~0xFF].append(addr)
    for base in sorted(clusters):
        addrs = clusters[base]
        print(f"  block 0x{base:08x}: {len(addrs)} reg. -> " +
              ", ".join(f"+0x{a-base:x}" for a in addrs))
    # detailed: values for each address (only blocks resembling GPIO)
    print("  --- write details (pc -> val) ---")
    for addr in sorted(by):
        ws = by[addr]
        vals = sorted(set(v for _, s, v in ws))
        sizes = set(s for _, s, _ in ws)
        pcs = sorted(set(p for p, _, _ in ws))
        print(f"    0x{addr:08x} (size{'/'.join(hex(s) for s in sorted(sizes))}): "
              f"W×{len(ws)} vals={vals[:8]} pc={pcs[:4]}")

if __name__ == "__main__":
    # init chain §74: 0xcd0d -> 0xcc69/0xc9dd/0x5971/0xcb41
    scan(0xCD0D, "init chain (0xcd0d)")
