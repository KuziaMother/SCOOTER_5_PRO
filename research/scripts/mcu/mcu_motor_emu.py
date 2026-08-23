#!/usr/bin/env python3
"""
Эмуляция кандидатов на моторный контур с хуками на:
  - TIM1: CCER(+0x30), CCR1/2/3(+0x44/48/4C) — layout с оффсетом +0x10 (см. §39)
  - таблица коммутации flash 0x17D36..0x17D7A
  - виртуальный порт-блок 0x48000000..0x48000E00
Кандидаты: ADC ISR 0x1a31c, SysTick 0x13CAC, main tick 0x1dfd8.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "emulator"))
from mcu_emu import McuEmu, STACK_TOP  # noqa: E402
from unicorn import UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UcError  # noqa: E402
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_R0  # noqa: E402

CANDS = {"adc_isr": 0x1a31c, "systick": 0x13CAC, "main_tick": 0x1dfd8}


def run(name, func, budget=8_000_000):
    emu = McuEmu(max_insn=budget)
    uc = emu.uc
    uc.mem_write(0x40000000, bytes(0x100000))   # периферия = 0
    try:
        uc.mem_map(0x48000000, 0x1000)          # порт-блок
    except UcError:
        pass

    events = []

    def h_tim1_write(uc, access, address, size, value, user):
        events.append((uc.reg_read(UC_ARM_REG_PC), "TIM1W", address - 0x40012C00, value))

    def h_port_write(uc, access, address, size, value, user):
        events.append((uc.reg_read(UC_ARM_REG_PC), "PORT_W", address - 0x48000000, value))

    def h_tim1_read(uc, access, address, size, value, user):
        events.append((uc.reg_read(UC_ARM_REG_PC), "TIM1R", address - 0x40012C00))

    def h_tbl_read(uc, access, address, size, value, user):
        events.append((uc.reg_read(UC_ARM_REG_PC), "TBL_R", address - 0x08000000))

    uc.hook_add(UC_HOOK_MEM_READ, h_tim1_read, None, 0x40012C30, 0x40012C50)
    uc.hook_add(UC_HOOK_MEM_READ, h_tbl_read, None, 0x08017D36, 0x08017D7A)
    uc.hook_add(UC_HOOK_MEM_WRITE, h_tim1_write, None, 0x40012C30, 0x40012C50)
    uc.hook_add(UC_HOOK_MEM_WRITE, h_port_write, None, 0x48000000, 0x48000E00)

    emu.broad = True
    emu.spin_limit = 3000
    emu.pc_hits = {}
    emu.spins = 0
    emu.mapped_pages = 0

    uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
    uc.reg_write(UC_ARM_REG_LR, 1)
    uc.reg_write(UC_ARM_REG_R0, 0)

    print(f"=== {name} (0x{func:05x}) ===")
    try:
        uc.emu_start(func | 1, 1, timeout=0, count=0)
    except UcError as e:
        print("UcError:", e)
    print(f"останов: {emu.stopped or 'нормально'}; insn={emu.insn}; spins={emu.spins}")

    from collections import Counter
    c = Counter(ev[1] for ev in events)
    print("события:", dict(c))
    # детали TIM1 и таблицы
    for ev in events:
        if ev[1] in ("TIM1W", "TIM1R", "TBL_R") and len(events) < 2000:
            pass
    tim1 = [ev for ev in events if ev[1].startswith("TIM1")]
    tbl = [ev for ev in events if ev[1] == "TBL_R"]
    port_w = [ev for ev in events if ev[1] == "PORT_W"]
    if tim1:
        c2 = Counter((op, off) for _, op, off in [(e[0], e[1], e[2]) for e in tim1])
        print("TIM1 детали (top):")
        for (op, off), n in sorted(c2.items())[:20]:
            pcs = sorted(set(e[0] for e in tim1 if e[1] == op and e[2] == off))
            print(f"  {op} +0x{off:02x} x{n}: pc={[f'0x{p:05x}' for p in pcs[:5]]}")
    if tbl:
        c3 = Counter(e[0] for e in tbl)
        print("TBL_R pc:", {f'0x{p:05x}': n for p, n in c3.most_common(10)})
    if port_w:
        c4 = Counter((e[2], ) for e in port_w)
        print("PORT_W (top):")
        for (off,), n in sorted(c4.items())[:20]:
            pcs = sorted(set(e[0] for e in port_w if e[2] == off))
            vals = sorted(set(e[3] for e in port_w if e[2] == off))[:6]
            print(f"  +0x{off:03x} x{n}: pc={[f'0x{p:05x}' for p in pcs[:5]]} val={[hex(v) for v in vals]}")
    print()


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which == "all":
        for k, v in CANDS.items():
            run(k, v)
    else:
        run(which, CANDS[which])
