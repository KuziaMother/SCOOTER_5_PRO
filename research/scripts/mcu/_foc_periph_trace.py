#!/usr/bin/env python3
"""Трасса периферийного footprint полного входа FOC 0x1a938 (с новой диагностикой McuEmu).
Цель: увидеть, какие TIM/ADC/GPIO-регистры реально трогает FOC, до фолта/зависания."""
import struct
import sys

import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'research', 'scripts', 'mcu'))
from emulator.mcu_emu import McuEmu, FLASH0, FLASH1, RAM, STACK_TOP
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_SP, UC_ARM_REG_LR)

FW_LEN = 0x25000


def main():
    emu = McuEmu(trace=False, max_insn=200000)
    emu.uc.mem_write(RAM, bytes(0x20000))          # чистая RAM
    emu.hook_periph_ready()                        # periph = 0xFF (ready)
    emu.trace_periph = True
    r4 = RAM + 0x040
    emu.uc.mem_write(r4, bytes(0x80))              # working-struct
    emu.uc.mem_write(r4 + 2, struct.pack('<h', 16384))  # value (mid)

    def stop(uc_, addr, size, u):
        aa = addr & ~1
        if not (FLASH0 <= aa < FLASH0 + FW_LEN or FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()
    sh = emu.uc.hook_add(UC_HOOK_CODE, stop)
    emu.uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
    emu.uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    emu.uc.reg_write(UC_ARM_REG_R4, r4)
    emu.uc.reg_write(UC_ARM_REG_R0, 0)
    try:
        emu.uc.emu_start(0x1A938 | 1, 0, count=200000)
    except Exception as e:
        print("ex:", str(e)[:80])
    emu.uc.hook_del(sh)
    print(f"инструкций: {emu.insn}, останов: {emu.stopped}")
    print(f"PC: 0x{emu.uc.reg_read(11) & 0xFFFFF:05x}")
    emu.report_periph(max_addrs=60)
    print("\n=== детали записей (pc, addr, size, value) ===")
    for pc, addr, size, val in emu.periph_writes:
        print(f"  @pc=0x{pc & 0xFFFFF:05x} [0x{addr:08x}] <- 0x{val:x} ({size}B)")
    print("=== чтения (addr: [pc...]) ===")
    for addr, pcs in emu.periph_reads.items():
        print(f"  0x{addr:08x}: {[hex(p & 0xFFFFF) for p in pcs]}")
    # что FOC посчитал в RAM+0x382/384/386 (источники CCR)
    for off in (0x382, 0x384, 0x386):
        v = struct.unpack('<H', emu.uc.mem_read(RAM + off, 2))[0]
        print(f"  RAM+{off:#05x} = {v} ({v:#x})")
    # детерминизм: 2-й прогон с тем же setup
    w1 = list(emu.periph_writes)
    emu2 = McuEmu(max_insn=200000); emu2.uc.mem_write(RAM, bytes(0x20000))
    emu2.hook_periph_ready(); r4b = RAM + 0x040
    emu2.uc.mem_write(r4b, bytes(0x80)); emu2.uc.mem_write(r4b + 2, struct.pack('<h', 16384))
    def stop2(uc_, addr, size, u):
        aa = addr & ~1
        if not (FLASH0 <= aa < FLASH0 + FW_LEN or FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()
    sh2 = emu2.uc.hook_add(UC_HOOK_CODE, stop2)
    emu2.uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80); emu2.uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    emu2.uc.reg_write(UC_ARM_REG_R4, r4b); emu2.uc.reg_write(UC_ARM_REG_R0, 0)
    try:
        emu2.uc.emu_start(0x1A938 | 1, 0, count=200000)
    except Exception:
        pass
    emu2.uc.hook_del(sh2)
    print(f"\nдетерминизм: прогон1 записей={len(w1)}, прогон2={len(emu2.periph_writes)}, "
          f"совпадение={w1 == emu2.periph_writes}")


if __name__ == '__main__':
    main()
