#!/usr/bin/env python3
"""
Трассировка моторного контура исполнением (Unicorn).

Цель: найти, кто реально читает таблицу коммутации @0x17d38.. и трогает TIM1
(0x40012C00) — статических ссылок на таблицу НЕТ, поэтому ищем потребителей
read/write-хуками при исполнении кандидатов:
  - 0x1dfd8 (main tick: фильтры сенсоров + подзадачи)
  - 0x1a31c (ADC ISR: выборка фазных токов)
  - 0x1a2a4 (функция с TIM1-пулом, найденная по pool-скану)

Запуск: python mcu_motor_trace.py [func]   (func = 0x1dfd8 по умолчанию)
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "emulator"))
from mcu_emu import McuEmu, STACK_TOP  # noqa: E402
from unicorn import UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UcError  # noqa: E402
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_R0  # noqa: E402

TABLE_LO = 0x08017D00      # калибровки + коммутация (flash-зеркало)
TABLE_HI = 0x08017E00
TIM1_LO = 0x40012C00
TIM1_HI = 0x40012C60


def main():
    func = int(sys.argv[1], 16) if len(sys.argv) > 1 else 0x1dfd8
    emu = McuEmu(max_insn=3_000_000)
    emu.uc.mem_write(0x40000000, bytes(0x100000))  # периферия = 0 (чистые флаги)

    table_reads = []   # (pc, addr)
    tim1_rw = []       # (pc, 'R'/'W', off, size, val)

    def h_table_read(uc, access, address, size, value, user):
        table_reads.append((uc.reg_read(UC_ARM_REG_PC), address))
        return None

    def h_tim1(uc, access, address, size, value, user):
        tim1_rw.append((uc.reg_read(UC_ARM_REG_PC), "R" if access == 1 else "W",
                        address - TIM1_LO, size, value))
        return None

    emu.uc.hook_add(UC_HOOK_MEM_READ, h_table_read, None, TABLE_LO, TABLE_HI)
    emu.uc.hook_add(UC_HOOK_MEM_READ, h_tim1, None, TIM1_LO, TIM1_HI)
    emu.uc.hook_add(UC_HOOK_MEM_WRITE, h_tim1, None, TIM1_LO, TIM1_HI)

    emu.broad = True
    emu.spin_limit = 2000
    emu.pc_hits = {}
    emu.spins = 0
    emu.mapped_pages = 0

    uc = emu.uc
    uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
    uc.reg_write(UC_ARM_REG_LR, 1)
    uc.reg_write(UC_ARM_REG_R0, 0)

    print(f"=== запуск 0x{func:05x} |1 ===")
    try:
        uc.emu_start(func | 1, 1, timeout=0, count=0)
    except UcError as e:
        print("UcError:", e)
    print(f"останов: {emu.stopped or 'нормально'}; инструкций: {emu.insn}; спинов: {emu.spins}")

    # отчёт: кто читает таблицу
    if table_reads:
        from collections import Counter
        c = Counter(pc for pc, _ in table_reads)
        print(f"\n--- ЧТЕНИЯ таблицы 0x17D00..0x17E00: {len(table_reads)} (PC-группы):")
        for pc, n in c.most_common(30):
            addrs = sorted(set(a - 0x08000000 for p, a in table_reads if p == pc))
            print(f"  pc=0x{pc:05x} x{n}: офс {addrs[:12]}")
    else:
        print("\n--- таблица НЕ читалась")

    if tim1_rw:
        from collections import Counter
        c = Counter((op, off) for _, op, off, _, _ in tim1_rw)
        print(f"\n--- TIM1 R/W: {len(tim1_rw)} (группы op/off):")
        for (op, off), n in sorted(c.items()):
            pcs = sorted(set(pc for pc, o2, off2, _, _ in tim1_rw if o2 == op and off2 == off))
            vals = sorted(set(v for _, o2, off2, _, v in tim1_rw if o2 == op and off2 == off))[:8]
            print(f"  {op} TIM1+0x{off:02x} x{n}: pc={ [f'0x{p:05x}' for p in pcs[:6]] } val~{[hex(v) for v in vals]}")
    else:
        print("\n--- TIM1 не трогался")

    # куда уходил поток (последние разные PC)
    if emu.pc_hits:
        top = sorted(emu.pc_hits.items(), key=lambda kv: -kv[1])[:15]
        print("\n--- топ-PC по частоте:")
        for pc, n in top:
            print(f"  0x{pc:05x}: {n}")


if __name__ == "__main__":
    main()
