#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A1: живая эмуляция round-robin диспетчера (0xE658) с seed live-state.

Цель: найти, где duty из регулятора (цепочка §39/§39.5b: 0x799C -> slew 0xE408
-> u16@RAM[0x1357]) применяется к периферии (TIM1 CCR / GPIO / DMA).

Хуки на все записи в:
  - таймеры 0x40012C00..0x40015000 (5 баз)
  - ADC1 0x40012400..0x40012440
  - DMA1 0x40020000..0x40020060
  - GPIO-блок 0x48000400..0x48009100
"""
import os, sys, struct as st

sys.path.insert(0, 'D:/SCOOTER_5_PRO/emulator')
from mcu_emu import McuEmu, STACK_TOP
from unicorn import UC_HOOK_MEM_WRITE, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

PERIPH_RANGES = [
    (0x40012C00, 0x40015000, 'TIMER'),
    (0x40012400, 0x40012440, 'ADC1'),
    (0x40020000, 0x40020060, 'DMA1'),
    (0x48000400, 0x48009100, 'GPIO'),
]


def seed_live(uc, mode=0, sensor=5000):
    """Seed live-state: гейты диспетчера, рукопожатие, конфиг, сенсор."""
    # гейты round-robin (§39.5b)
    uc.mem_write(0x20000A49, bytes([1]))   # byte@RAM[0xA49] = 1
    uc.mem_write(0x20000035, bytes([0]))   # byte@RAM[0x35] = 0
    uc.mem_write(0x20000A62, bytes([0]))   # счётчик слотов = 0
    # рукопожатие (§36.2)
    uc.mem_write(0x20000319, bytes([3]))   # M[0x319] = 3
    uc.mem_write(0x20000358, bytes([1]))   # RAM[0x358] = 1
    # конфиг-структ @RAM+0xFC7 (копия blob @RAM+0x4A, писатель 0x1093C)
    cfg = bytes([0, mode, 0, 0, 0, 0, 0, 0])
    uc.mem_write(0x2000004A, cfg)          # источник
    uc.mem_write(0x20000FC7, cfg)          # и сама копия (mode = +1)
    # сенсор регулятора: i16@st+0x20 = RAM[0x13A4]
    uc.mem_write(0x200013A4, st.pack('<h', sensor))
    # выход регулятора из прошлого цикла (для slew)
    uc.mem_write(0x200012A7, st.pack('<H', 0))   # u16@RAM[0x12A7] prev
    # NVRAM-калибровки (§26.3): u16@[0x128/0x12A/0x12C/0x14C]
    for off, v in ((0x128, 2000), (0x12A, 2000), (0x12C, 2000), (0x14C, 2000)):
        uc.mem_write(0x20000000 + off, st.pack('<H', v))


def run(emu, iterations=30):
    """Запуск диспетчера N итераций; возврат списка записей в периферию."""
    uc = emu.uc
    writes = []
    code_trace = {}

    def on_write(uc_, access, address, size, value, user):
        for lo, hi, name in PERIPH_RANGES:
            if lo <= address < hi:
                writes.append((name, address - lo, size, value,
                               uc_.reg_read(UC_ARM_REG_PC)))
                break

    def on_code(uc_, addr, size, user):
        code_trace[addr] = code_trace.get(addr, 0) + 1

    h1 = uc.hook_add(UC_HOOK_MEM_WRITE, on_write)
    h2 = uc.hook_add(UC_HOOK_CODE, on_code)
    try:
        for i in range(iterations):
            uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x40 * i)
            uc.reg_write(UC_ARM_REG_LR, 1)
            try:
                uc.emu_start(0xE658 | 1, 1, timeout=0, count=200_000)
            except Exception:
                pass
    finally:
        uc.hook_del(h1)
        uc.hook_del(h2)
    return writes, code_trace


def main():
    emu = McuEmu(max_insn=500_000)
    # маппим периферийные диапазоны как RAM (заглушки), чтобы хуки срабатывали
    uc = emu.uc
    from unicorn import UC_PROT_ALL
    for lo, hi, _ in PERIPH_RANGES:
        try:
            uc.mem_map(lo, hi - lo, UC_PROT_ALL)
        except Exception:
            pass

    results = {}
    for mode in (0, 1, 5):
        emu2 = McuEmu(max_insn=500_000)
        uc2 = emu2.uc
        for lo, hi, _ in PERIPH_RANGES:
            try:
                uc2.mem_map(lo, hi - lo, UC_PROT_ALL)
            except Exception:
                pass
        seed_live(uc2, mode=mode, sensor=5000)
        writes, trace = run(emu2, iterations=30)
        results[mode] = (writes, trace)
        print(f'=== mode={mode}: записей в периферию: {len(writes)}')
        for w in writes[:40]:
            name, off, size, val, pc = w
            print(f'  {name:6s} +{off:#05x} ({size}Б) = {val:#010x}  (pc={pc:#x})')

    # итог по коду: какие функции исполнялись
    for mode, (writes, trace) in results.items():
        if not trace:
            continue
        top = sorted(trace.items(), key=lambda kv: -kv[1])[:15]
        print(f'--- mode={mode} топ-PC: ' + ', '.join(f'{a:#x}×{c}' for a, c in top))


if __name__ == '__main__':
    main()
