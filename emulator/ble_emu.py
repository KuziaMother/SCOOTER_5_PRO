#!/usr/bin/env python3
"""
Инструкционный эмулятор BLE-образа (Realtek RTL8762C, Cortex-M33) — Unicorn.

Исполняет РЕАЛЬНЫЙ код плейн-регионов ble_2.7.0_0015.bin (bootloader + flash/OTA-
драйвер). Как и MCU-эмулятор: ФУНКЦИОНАЛЬНАЯ эмуляция (вызов конкретной функции с
поднятым состоянием), а не boot-from-reset (нет вектор-таблицы в плейне, main-app
зашифрован). Периферия заглушена (chitae): status-регистры читаются как 0xFFFFFFFF
(все ready), записи логируются.

Память RTL8762C (по firmware-адресам + SDK OpenOCD cfg):
  FLASH @0x01800000 (образ), RAM @0x20000000, PERIPH @0x40000000, SYS @0xE0000000.

Запуск:  python -X utf8 emulator/ble_emu.py --func 0x7dea [--max 200000] [--trace]
"""
import argparse
import os
import struct

from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE,
                     UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ,
                     UC_HOOK_MEM_UNMAPPED, UcError)
from unicorn.arm_const import (UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC,
                               UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                               UC_ARM_REG_R3)

HERE = os.path.dirname(os.path.abspath(__file__))
FW = os.path.join(os.path.dirname(HERE), "research", "images", "ble_2.7.0_0015.bin")

FLASH = 0x01800000           # база флеша (адрес == 0x01800000 + смещение в файле)
RAM = 0x20000000
RAM_SIZE = 0x80000           # 512K (exe_base 0x203800 здесь)
PERIPH = 0x40000000
PERIPH_SIZE = 0x00100000     # 1MB loose
SYS = 0xE0000000
SYS_SIZE = 0x00100000
STACK_TOP = RAM + RAM_SIZE   # 0x20080000


def align(x, a=0x1000):
    return (x + a - 1) & ~(a - 1)


class BleEmu:
    def __init__(self, trace=False, max_insn=300000):
        self.trace = trace
        self.max_insn = max_insn
        self.insn = 0
        self.ram_writes = []       # (pc, addr, size, val) в RAM
        self.periph_writes = []    # (pc, addr, size, val) в PERIPH/SYS
        self.flash_writes = []     # (pc, addr, size, val) в FLASH (OTA-установка!)
        self.stopped = None
        self.uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
        self._map()
        self._hooks()

    def _map(self):
        fw = open(FW, "rb").read()
        fsz = align(len(fw))
        self.uc.mem_map(FLASH, fsz)
        self.uc.mem_write(FLASH, fw)
        self.uc.mem_map(RAM, RAM_SIZE)
        self.uc.mem_map(PERIPH, PERIPH_SIZE)
        self.uc.mem_map(SYS, SYS_SIZE)
        self.fw_len = len(fw)

    def _hooks(self):
        self.uc.hook_add(UC_HOOK_CODE, self._h_code)
        self.uc.hook_add(UC_HOOK_MEM_WRITE, self._h_write)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self._h_unmapped)

    def _h_code(self, uc, address, size, user):
        self.insn += 1
        if self.insn > self.max_insn:
            self.stopped = f"лимит инструкций {self.max_insn}"
            uc.emu_stop()
            return
        if self.trace and self.insn <= 80:
            print(f"    [{self.insn:>5}] pc=0x{address:06x}")

    def _h_write(self, uc, access, address, size, value, user):
        pc = uc.reg_read(UC_ARM_REG_PC)
        if FLASH <= address < FLASH + self.fw_len:
            self.flash_writes.append((pc, address - FLASH, size, value))
        elif RAM <= address < RAM + RAM_SIZE:
            self.ram_writes.append((pc, address, size, value))
        elif PERIPH <= address < PERIPH + PERIPH_SIZE or SYS <= address < SYS + SYS_SIZE:
            self.periph_writes.append((pc, address, size, value))

    def _h_unmapped(self, uc, access, address, size, value, user):
        # по требованию маппим нулевую страницу (для обращений за пределы карты)
        page = address & ~0xFFF
        try:
            uc.mem_map(page, 0x1000)
            return True
        except UcError:
            pc = uc.reg_read(UC_ARM_REG_PC)
            self.stopped = f"незамапленное 0x{address:08x} @pc=0x{pc:06x}"
            return False

    def periph_ready(self):
        """Чтение периферии как 0xFFFFFFFF (все ready-биты) — poll-циклы не виснут."""
        def h(uc, access, addr, size, value, user):
            uc.mem_write(addr, struct.pack('<' + {1: 'B', 2: 'H', 4: 'I'}[size], (1 << (8 * size)) - 1))
            return True
        self.uc.hook_add(UC_HOOK_MEM_READ, h, None, PERIPH, PERIPH + PERIPH_SIZE)

    def run_func(self, addr, args=(), sp=None, max_insn=None):
        """Вызвать функцию addr с аргументами в R0-R3; вернуть (r0, stopped)."""
        if max_insn:
            self.max_insn = max_insn
        self.insn = 0
        self.ram_writes.clear(); self.periph_writes.clear(); self.flash_writes.clear()
        sp = sp or (STACK_TOP - 0x400)
        uc = self.uc
        uc.reg_write(UC_ARM_REG_SP, sp)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)   # sentinel: остановимся на bx lr
        for i, a in enumerate(args):
            uc.reg_write([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3][i], a)

        def stop(uc_, a, size, u):
            a &= ~1
            if a == 0x0BADF000 or a == 0x0BADF001:   # bx lr к sentinel
                uc_.emu_stop()
        sh = uc.hook_add(UC_HOOK_CODE, stop)
        try:
            uc.emu_start(FLASH + addr | 1, 0, count=max_insn or self.max_insn)
        except UcError as e:
            self.stopped = f"UcError: {e}"
        finally:
            uc.hook_del(sh)
        r0 = uc.reg_read(UC_ARM_REG_R0)
        return r0, self.stopped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--func', required=True, help='оффсет функции в файле (0x7dea)')
    ap.add_argument('--args', default='', help='через запятую: 0x20001000,0x100,4')
    ap.add_argument('--max', type=int, default=300000)
    ap.add_argument('--trace', action='store_true')
    a = ap.parse_args()
    args = [int(x, 0) for x in a.args.split(',') if x.strip()] if a.args else []
    emu = BleEmu(trace=a.trace, max_insn=a.max)
    r0, stopped = emu.run_func(int(a.func, 0), args)
    print(f"\nr0=0x{r0:08x}  stopped={stopped}")
    print(f"RAM-writes: {len(emu.ram_writes)}, PERIPH-writes: {len(emu.periph_writes)}, FLASH-writes: {len(emu.flash_writes)}")
    for pc, off, sz, v in emu.flash_writes[:20]:
        print(f"  FLASH+{off:#06x} = {v:#x} (sz={sz}) @pc=0x{pc - FLASH:06x}")
    for pc, addr, sz, v in emu.periph_writes[:20]:
        print(f"  PERIPH {addr:#010x} = {v:#x} (sz={sz}) @pc=0x{pc - FLASH:06x}")


if __name__ == '__main__':
    main()
