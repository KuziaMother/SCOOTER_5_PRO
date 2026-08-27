# -*- coding: utf-8 -*-
"""§73.x ISR: writer-sweep — какая функция пишет V=u32[RAM+0x158]?

Прогоняем ВСЕ начала функций (find_func_starts), ловим запись в 0x20000158.
Также проверяем F=byte[RAM+0x100] (гейт скорости).
"""
import struct, sys
sys.path.insert(0, '.')
from emulator.mcu_emu import (McuEmu, FLASH0, FLASH1, RAM, STACK_TOP,
                              find_func_starts)
from unicorn import UC_HOOK_CODE, UcError
from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR

FW_LEN = 0x25000
V_ADDR = RAM + 0x158
F_ADDR = RAM + 0x100


def run_one(emu_factory, addr, max_insn=12000):
    emu = emu_factory()
    emu.uc.mem_write(V_ADDR, struct.pack('<I', 0xDEAD))
    def stop(uc_, a, size, u):
        aa = a & ~1
        if not (FLASH0 <= aa < FLASH0 + FW_LEN or
                FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()
    sh = emu.uc.hook_add(UC_HOOK_CODE, stop)
    emu.uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
    emu.uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    try:
        emu.uc.emu_start(addr | 1, 0, count=max_insn)
    except UcError:
        pass
    emu.uc.hook_del(sh)
    v = struct.unpack('<I', emu.uc.mem_read(V_ADDR, 4))[0]
    f = struct.unpack('<B', emu.uc.mem_read(F_ADDR, 1))[0]
    return v, f


def main():
    starts = find_func_starts()
    print(f'функций: {len(starts)}; ищу запись в V={V_ADDR:#x}')
    hits = []
    for i, s in enumerate(starts):
        emu = McuEmu(max_insn=12000)
        emu.uc.mem_write(RAM, bytes(0x20000))
        emu.uc.mem_write(V_ADDR, struct.pack('<I', 0xDEAD))
        def stop(uc_, a, size, u):
            aa = a & ~1
            if not (FLASH0 <= aa < FLASH0 + FW_LEN or
                    FLASH1 <= aa < FLASH1 + FW_LEN):
                uc_.emu_stop()
        sh = emu.uc.hook_add(UC_HOOK_CODE, stop)
        emu.uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
        emu.uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        try:
            emu.uc.emu_start(s | 1, 0, count=12000)
        except UcError:
            pass
        emu.uc.hook_del(sh)
        v = struct.unpack('<I', emu.uc.mem_read(V_ADDR, 4))[0]
        if v != 0xDEAD:
            f = struct.unpack('<B', emu.uc.mem_read(F_ADDR, 1))[0]
            hits.append((s, v, f))
    print(f'--- ХИТЫ (записали V): {len(hits)} ---')
    for s, v, f in hits:
        print(f'  0x{s:05x}: V -> {v} ({v:#x}), F=byte[RAM+0x100]={f}')


if __name__ == '__main__':
    main()
