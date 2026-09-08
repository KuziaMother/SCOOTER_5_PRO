# -*- coding: utf-8 -*-
"""Трассировка RAM-доступов pool-функции.

Запускает функцию в свежем McuEmu (чистый RAM) и собирает все адреса RAM,
которые функция читает/пишет. Это раскрывает base-указатель (загружается из
flash literal-pool автоматически) + смещения полей — то, что нужно для
pre-populate и верификации stateful-функции.

Использование:  python -X utf8 _pool_trace.py 0xADDR [0xADDR2 ...]
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))          # research/scripts/mcu
RES = os.path.dirname(os.path.dirname(HERE))               # research
REPO = os.path.dirname(RES)                                # D:/SCOOTER_5_PRO
sys.path.insert(0, REPO)
sys.path.insert(0, HERE)
from unicorn import UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UcError, UC_HOOK_CODE
from emulator.mcu_emu import McuEmu, RAM, FLASH0, FLASH1, STACK_TOP
from func_verify import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                         UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_LR)

FW_LEN = 0x23680


def trace(off, args=(), max_insn=50000):
    emu = McuEmu(max_insn=max_insn)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))
    emu.hook_periph_ready()
    reads = set()
    writes = set()

    def hr(u, access, address, size, value, user):
        if RAM <= address < RAM + 0x20000:
            reads.add(address - RAM)

    def hw(u, access, address, size, value, user):
        if RAM <= address < RAM + 0x20000:
            writes.add(address - RAM)

    h1 = uc.hook_add(UC_HOOK_MEM_READ, hr, None, RAM, RAM + 0x20000)
    h2 = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, RAM, RAM + 0x20000)

    def _st(uc_, a, s, u):
        aa = a & ~1
        if not (FLASH0 <= aa < FLASH0 + FW_LEN or FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()

    sh = uc.hook_add(UC_HOOK_CODE, _st)
    try:
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x40)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        for r, v in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                         UC_ARM_REG_R3), args):
            uc.reg_write(r, v & 0xFFFFFFFF)
        emu.insn = 0
        try:
            uc.emu_start(off | 1, 0, count=max_insn)
        except UcError:
            pass
        r0 = uc.reg_read(UC_ARM_REG_R0)
    finally:
        for h in (h1, h2, sh):
            try:
                uc.hook_del(h)
            except Exception:
                pass
    return r0, sorted(reads), sorted(writes)


def _show(off, args=()):
    r0, reads, writes = trace(off, args=args)
    print(f'=== 0x{off:05x}  (r0={r0:#x}) ===')
    print(f'  RAM-reads  ({len(reads)}): ' +
          (', '.join(f'+0x{a:x}' for a in reads[:40]) if reads else '(none)'))
    print(f'  RAM-writes ({len(writes)}): ' +
          (', '.join(f'+0x{a:x}' for a in writes[:40]) if writes else '(none)'))


if __name__ == '__main__':
    addrs = [int(x, 0) for x in sys.argv[1:]] or [0x01A68]
    for a in addrs:
        _show(a)
