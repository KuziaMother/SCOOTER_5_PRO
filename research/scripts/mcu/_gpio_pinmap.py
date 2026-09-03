#!/usr/bin/env python3
"""A1 (GPIO): статический pin-map кастомного блока «портов». Прогоняем init,
декодим MODER_LO/HI (2 бита/пин) и печатаем карту портов/пинов/режимов."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "emulator"))
from mcu_emu import McuEmu
from func_verify import Run  # noqa

MODE_NAMES = {0: "in/резо", 1: "out-одн", 2: "out-дв/AF", 3: "in-pull?"}

def pinmap(entry, label):
    run = Run(max_insn=400000)
    from emulator.mcu_emu import GpioModel, GPIO_PORT_BASE
    uc = run.uc
    uc.mem_write(0x20000000, bytes(0x20000))
    run.emu.hook_periph_ready()
    gpio = GpioModel(run.emu)
    from unicorn import UC_HOOK_CODE, UcError
    from emulator.mcu_emu import FLASH0, FLASH1
    def _st(uc_, addr, size, u):
        aa = addr & ~1
        if not (FLASH0 <= aa < FLASH0 + 0x23680 or FLASH1 <= aa < FLASH1 + 0x23680):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, _st)
    try:
        from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR
        uc.reg_write(UC_ARM_REG_SP, 0x20018000 - 0x80)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        run.emu.insn = 0
        try:
            uc.emu_start(entry | 1, 0, count=250000)
        except UcError:
            pass
    finally:
        uc.hook_del(sh); uc.hook_del(gpio._hook)
    print(f"\n===== PIN-MAP {label} (0x{entry:05x}) =====")
    for p in range(4):
        base = GPIO_PORT_BASE + p * 0x400
        lo, hi = gpio.read(p, 0x2c), gpio.read(p, 0x28)
        out = gpio.read(p, 0x10)
        if lo == hi == out == 0:
            print(f"  порт {p} (0x{base:08x}): не сконфигурирован")
            continue
        print(f"  порт {p} (0x{base:08x}): MODER=0x{lo:08x} HI=0x{hi:08x} OUTSEL=0x{out:08x}")
        for pin in range(16):
            m = gpio.pin_mode(p, pin)
            if m:
                print(f"      pin{pin:>2}: mode={m} ({MODE_NAMES.get(m,'?')})")

if __name__ == "__main__":
    pinmap(0x1BF48, "МОТОР-ИНИТ")
