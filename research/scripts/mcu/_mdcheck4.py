# -*- coding: utf-8 -*-
"""Поведенческая проверка Thumb-инструкций через Unicorn (QEMU) —
независимый от capstone декодер. Что реально делает каждый байтовый паттерн?"""
import sys, io, struct
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from unicorn import Uc
from unicorn import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R3,
                     UC_ARM_REG_R6, UC_ARM_REG_R7)

BASE = 0x10000
STACK = 0x20000
NAMES = {UC_ARM_REG_R0: 'r0', UC_ARM_REG_R1: 'r1', UC_ARM_REG_R3: 'r3',
         UC_ARM_REG_R6: 'r6', UC_ARM_REG_R7: 'r7'}

def run(hws, regs_before, readback=None):
    """hws: list of halfword ints; regs_before: {reg_const: value}"""
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE - 0x1000, 0x4000)
    uc.mem_map(STACK - 0x1000, 0x4000)
    blob = b''.join(struct.pack('<H', h) for h in hws)
    uc.mem_write(BASE, blob)
    for r, v in regs_before.items():
        uc.reg_write(r, v)
    uc.reg_write(UC_ARM_REG_SP, STACK + 0x100)
    uc.reg_write(UC_ARM_REG_LR, 0xDEAD0001)
    uc.mem_write(BASE + len(blob), struct.pack('<H', 0x4770))  # bx lr стоп
    try:
        uc.emu_start(BASE | 1, BASE + len(blob) | 1)
    except Exception as e:
        return 'EMU-ERROR %s' % e, None
    out = {}
    for r in regs_before:
        out[NAMES[r]] = uc.reg_read(r)
    memval = None
    if readback is not None:
        try:
            memval = uc.mem_read(readback, 1)[0]
        except Exception:
            memval = None
    return out, memval

tests = [
    ('4600', [0x4600], {UC_ARM_REG_R0: 0x11, UC_ARM_REG_R1: 0xDEAD}, None),
    ('7001', [0x7001], {UC_ARM_REG_R0: STACK + 0x50, UC_ARM_REG_R1: 0x99}, STACK + 0x50),
    ('003b', [0x003B], {UC_ARM_REG_R3: 0x12, UC_ARM_REG_R7: 0x77}, None),
    ('43b3', [0x43B3], {UC_ARM_REG_R3: 0xFF, UC_ARM_REG_R6: 0x66}, None),
]
for name, hws, regs, rb in tests:
    res, memval = run(hws, regs, rb)
    if isinstance(res, str):
        print('%s -> %s' % (name, res))
        continue
    mv = ('  mem[r0_start]=%02x' % memval) if memval is not None else ''
    print('%s -> %s%s' % (name, res, mv))
