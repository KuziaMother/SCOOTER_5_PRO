#!/usr/bin/env python3
"""A1 (GPIO model): эмпирический поиск GPIO-конфига в init.

Прогоняем init-цепочку через run_broad и группируем periph_writes по адресу,
чтобы найти базу/оффсеты GPIO (чип кастомный — GPIO не на стандартной STM32F1-базе;
комментарий в mcu_emu.py указывает «GPIO-подобный» блок в PERIPH2 @0x48000C00).
"""
import sys, os, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "emulator"))
from mcu_emu import McuEmu, PERIPH, PERIPH_SIZE, PERIPH2, PERIPH2_SIZE, SYS, SYS_SIZE

def scan(entry, label, budget=3_000_000):
    emu = McuEmu(max_insn=budget)
    emu.run_broad(entry, budget=budget)
    print(f"\n===== {label} (entry 0x{entry:05x}) — periph-записи по адресу =====")
    by = collections.defaultdict(list)
    for pc, addr, size, val in emu.periph_writes:
        by[addr].append((pc, size, val))
    if not by:
        print("  (записей в периферию нет)")
        return
    # сгруппируем по 0x40-блоку (base & ~0xFF) чтобы увидеть кластеры
    clusters = collections.defaultdict(list)
    for addr in sorted(by):
        clusters[addr & ~0xFF].append(addr)
    for base in sorted(clusters):
        addrs = clusters[base]
        print(f"  блок 0x{base:08x}: {len(addrs)} рег. -> " +
              ", ".join(f"+0x{a-base:x}" for a in addrs))
    # детально: значения по каждому адресу (только блоки, похожие на GPIO)
    print("  --- детали записей (pc -> val) ---")
    for addr in sorted(by):
        ws = by[addr]
        vals = sorted(set(v for _, s, v in ws))
        sizes = set(s for _, s, _ in ws)
        pcs = sorted(set(p for p, _, _ in ws))
        print(f"    0x{addr:08x} (size{'/'.join(hex(s) for s in sorted(sizes))}): "
              f"W×{len(ws)} vals={vals[:8]} pc={pcs[:4]}")

if __name__ == "__main__":
    # init-цепочка §74: 0xcd0d -> 0xcc69/0xc9dd/0x5971/0xcb41
    scan(0xCD0D, "init-цепочка (0xcd0d)")
