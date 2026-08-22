#!/usr/bin/env python3
"""
Префлайт patched_mi5pro_firmware.bin в эмуляторе (Unicorn, реальный код).

Запускает ТОЧНО патченные базовые блоки в официальном и патченном бинарниках
с одинаковым синтетическим состоянием и сравнивает:
  - не падает ли патченный блок (fault на самом патче);
  - значение [r4+0x14] — поведение clamp-логики.

Блоки:
  A) 0x1d0e4 (default-case): off: [r4+0x14]=min(0xD0,*r0); pat: всегда 0xD0.
  B) 0x1d140 (case 3):       off: ldrh r1,[r0]; pat: ldrb r1,[r0] (младший байт).

Это НЕ полная проверка прошивки (нет boot/векторов), но ловит грубые поломки
патча и показывает семантику. Запуск: python custom_mcu/preflight_emu.py
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "emulator"))
import mcu_emu  # noqa: E402
from unicorn import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R4,  # noqa: E402
                     UC_ARM_REG_SP, UC_ARM_REG_LR)

OFF = os.path.join(ROOT, "firmware_ota",
                   "c0f78c49f322bd3d71fea19c90241882_mcu_xiaomi.scooter.5pro_v0007.bin")
PAT = os.path.join(HERE, "patched_mi5pro_firmware.bin")

CTX = 0x20001000      # r4: контекст
PTR = 0x20001100      # r0: указатель на u16


def run_case(fw, start, u16_val, label):
    mcu_emu.FW = fw
    e = mcu_emu.McuEmu(max_insn=5000)
    e.uc.mem_write(CTX, b"\x00" * 0x100)
    e.uc.mem_write(PTR, struct.pack("<H", u16_val))
    e.uc.reg_write(UC_ARM_REG_SP, mcu_emu.STACK_TOP)
    e.uc.reg_write(UC_ARM_REG_LR, 1)          # bx lr -> стоп
    e.uc.reg_write(UC_ARM_REG_R0, PTR)
    e.uc.reg_write(UC_ARM_REG_R1, 0)
    e.uc.reg_write(UC_ARM_REG_R4, CTX)
    try:
        e.uc.emu_start(start | 1, 0, count=5005)
    except Exception as ex:
        e.stopped = f"UcError {ex}"
    v = struct.unpack("<H", e.uc.mem_read(CTX + 0x14, 2))[0]
    pc = e.uc.reg_read(mcuc_pc())
    return v, e.insn, pc


def mcuc_pc():
    from unicorn import UC_ARM_REG_PC
    return UC_ARM_REG_PC


CASES = [
    # (start, u16_val, описание)
    (0x1d0e4, 80,   "A1: default, *r0=80  (<208): off должен дать 80, pat — 208"),
    (0x1d0e4, 300,  "A2: default, *r0=300 (>208): оба — 208"),
    (0x1d140, 464,  "B1: case3,  *r0=464 (0x01D0): off — 464, pat — 208 (ldrb)"),
]

for start, val, desc in CASES:
    print(f"== {desc}")
    for name, fw in (("OFF", OFF), ("PAT", PAT)):
        v, insn, pc = run_case(fw, start, val, f"{name}")
        print(f"   {name}: [r4+0x14]={v:#06x}  insn={insn}  stop_pc=0x{pc:05x}")
    print()
