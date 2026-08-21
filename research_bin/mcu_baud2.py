# -*- coding: utf-8 -*-
"""Целенаправленный разбор кандидатов на UART/clock init (из mcu_baud.py sweep).

Для каждой функции печатаем ПОЛНУЮ последовательность записей в периферию
(USART3/UART4/RCC) с pc — чтобы увидеть: куда реально пишут BRR, есть ли
read-modify-write RCC, и не зависит ли BRR от прочитанного PCLK.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "emulator"))
from mcu_emu import (McuEmu, PERIPH, PERIPH_SIZE, SYS, SYS_SIZE, STACK_TOP)  # noqa: E402
from unicorn import UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ, UcError  # noqa: E402
from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC  # noqa: E402

REGIONS = [
    (0x40004800, "USART3"),
    (0x40004C00, "UART4"),
    (0x40021000, "RCC"),
]
NAMES = {0x00: "SR", 0x04: "DR", 0x08: "BRR/CFGR", 0x0C: "CR1", 0x10: "CR2",
         0x14: "CR3", 0x28: "GPR?/SR2", 0x3C: "+0x3c"}

CANDIDATES = [0x1e2f8, 0x11cb4, 0x016d4, 0x05bc4, 0x110fc, 0x0175c,
              0x01940, 0x05b98, 0x0af94, 0x10770, 0x106b8]


def run_one(addr):
    emu = McuEmu(trace=False, max_insn=50000)
    emu.uc.mem_write(PERIPH, b"\xff" * PERIPH_SIZE)   # все ready-биты = 1
    emu.uc.mem_write(SYS, bytes(SYS_SIZE))
    seq = []
    last_read = None

    def on_w(uc, access, address, size, value, user):
        for lo, nm in REGIONS:
            if lo <= address < lo + 0x40:
                pc = uc.reg_read(UC_ARM_REG_PC)
                seq.append((pc, nm, address - lo, size, value & 0xFFFFFFFF))
                break

    def on_r(uc, access, address, size, value, user):
        nonlocal last_read
        for lo, nm in REGIONS:
            if lo <= address < lo + 0x40:
                pc = uc.reg_read(UC_ARM_REG_PC)
                key = (pc, nm, address - lo)
                if key != last_read:          # дедупликация poll-циклов
                    seq.append((pc, nm, address - lo, size, None))
                last_read = key
                break

    emu.uc.hook_add(UC_HOOK_MEM_WRITE, on_w)
    emu.uc.hook_add(UC_HOOK_MEM_READ, on_r)
    emu.uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
    emu.uc.reg_write(UC_ARM_REG_LR, 1)
    print(f"\n=== func 0x{addr:05x} ===")
    try:
        emu.uc.emu_start(addr | 1, 0, count=50005)
    except UcError:
        pass
    for pc, nm, off, size, val in seq:
        if val is None:
            print(f"  [pc=0x{pc:05x}] R {nm}.{NAMES.get(off, f'+0x{off:x}')} ({size}B)")
        else:
            print(f"  [pc=0x{pc:05x}] W {nm}.{NAMES.get(off, f'+0x{off:x}')} <- 0x{val:08x}")
    if not seq:
        print("  (записей/чтений в USART3/UART4/RCC нет)")
    del emu


if __name__ == "__main__":
    for a in CANDIDATES:
        run_one(a)
