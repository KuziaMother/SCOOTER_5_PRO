# -*- coding: utf-8 -*-
"""§73.x ADC: прямой вызов 0x1be1c (TIM capture) с known sector/T/C.

Подтверждает: базу T-регистров (пул @0x1be29), какие T читаются для сектора,
формулу реконструкции тока (T−C)<<4 → r0+0xc/0x10/0x14, и clamp [−30000,30000].
"""
import struct, sys
sys.path.insert(0, '.')
from emulator.mcu_emu import McuEmu, FLASH0, FLASH1, RAM, STACK_TOP
from unicorn import UC_HOOK_CODE, UcError
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR)

FW_LEN = 0x25000


def run_be1c(sector, c18, c1a, c1c, t28, t2c, t30):
    emu = McuEmu(max_insn=200000)
    emu.uc.mem_write(RAM, bytes(0x20000))
    r0 = RAM + 0x100
    emu.uc.mem_write(r0, bytes(0x40))
    emu.uc.mem_write(r0 + 2, struct.pack('<H', sector))
    emu.uc.mem_write(r0 + 0x18, struct.pack('<H', c18 & 0xFFFF))
    emu.uc.mem_write(r0 + 0x1a, struct.pack('<H', c1a & 0xFFFF))
    emu.uc.mem_write(r0 + 0x1c, struct.pack('<H', c1c & 0xFFFF))
    # гейт mode-2: STAT бит15 = 1
    emu.uc.mem_write(0x40012c54, struct.pack('<I', 0x8000))
    # T-регистры (предполагаемая база 0x40012440): +0x28/+0x2c/+0x30
    emu.uc.mem_write(0x40012440 + 0x28, struct.pack('<I', t28 & 0xFFFFFFFF))
    emu.uc.mem_write(0x40012440 + 0x2c, struct.pack('<I', t2c & 0xFFFFFFFF))
    emu.uc.mem_write(0x40012440 + 0x30, struct.pack('<I', t30 & 0xFFFFFFFF))

    def stop(uc_, addr, size, u):
        aa = addr & ~1
        if not (FLASH0 <= aa < FLASH0 + FW_LEN or
                FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()
    sh = emu.uc.hook_add(UC_HOOK_CODE, stop)
    emu.uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
    emu.uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    emu.uc.reg_write(UC_ARM_REG_R0, r0)
    try:
        emu.uc.emu_start(0x1BE1C | 1, 0, count=200000)
    except UcError:
        pass
    emu.uc.hook_del(sh)
    # результат: r0+0xc/0x10/0x14 (s32) + что скопировано в пул-блок
    out = {}
    for off, nm in ((0x0c, 'o_c'), (0x10, 'o_10'), (0x14, 'o_14')):
        out[nm] = struct.unpack('<i', emu.uc.mem_read(r0 + off, 4))[0]
    # periph reads (адреса) в регионе capture
    # (periph_reads не включён; используем periph_writes для записи результата)
    return emu, out


def classify(out):
    """По паттерну pre-clamp выходов определить handler (какие T−C использованы)."""
    oc, o10, o14 = out['o_c'], out['o_10'], out['o_14']
    # диффы: A28=T28−C18, A2C=T2C−C1A, A30=T30−C1C (все ×16)
    return (oc, o10, o14)


def main():
    # разные diff, чтобы различить handler: (T−C): 28→4000, 2c→6000, 30→8000
    c18, c1a, c1c = 1000, 2000, 3000
    t28, t2c, t30 = 5000, 8000, 11000
    d28 = (t28 - c18) << 4   # 64000
    d2c = (t2c - c1a) << 4   # 96000
    d30 = (t30 - c1c) << 4   # 128000
    print(f'diff×16: A28={d28} A2C={d2c} A30={d30}')
    handlers = {
        'A': (d28, -(d28 + d30), d30),     # o_c=A28, o_14=A30, o_10=−(A28+A30)
        'B': (-(d2c + d30), d2c, d30),      # o_c=−(A2C+A30), o_10=A2C, o_14=A30
        'C': (d28, d2c, -(d28 + d2c)),      # o_c=A28, o_10=A2C, o_14=−(A28+A2C)
    }
    for sec in range(7):
        _, out = run_be1c(sec, c18, c1a, c1c, t28, t2c, t30)
        pat = classify(out)
        match = [k for k, v in handlers.items() if v == pat]
        tag = match[0] if len(match) == 1 else ('NULL/other' if pat == (0, 0, 0) else f'?{pat}')
        print(f'sector={sec}: o_c={out["o_c"]:7d} o_10={out["o_10"]:7d} '
              f'o_14={out["o_14"]:7d}  → handler {tag}')


if __name__ == '__main__':
    main()
