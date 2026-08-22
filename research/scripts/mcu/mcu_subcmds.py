#!/usr/bin/env python3
"""
Динамический маппинг подкоманд данных-канала (кадры 0x51..0x54).

Форматы (выведены из состояний 0..5 агрегатора 0x1f71c):
  Path A (subcmd 0x10..0x1b, 0x53):
      HDR SUB LEN DATA×LEN CHK TRAILER
      CHK = sum(frame[0..LEN+2]) & FF          (проверка в state 2)
      TRAILER = 0xFF - HDR                     (frame[LEN+4], state 3)
  Path B (subcmd 0x20..0x2f, 0x35, 0x36, 0x50, 0x51):
      HDR SUB CHK TRAILER [DATA...]
      CHK = (HDR + SUB) & FF                   (frame[2], state 4)
      TRAILER = 0xFF - HDR                     (frame[3], state 5)

Для каждой подкоманды: строим валидный кадр, гоняем 0x1f71c по циклу
состояний, ловим ВСЕ записи в RAM → получаем «subcmd → поля».

Запуск:  python research/mcu_subcmds.py [--hdr 51] [--data 0102030405060708]
"""
import argparse
import struct
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "emulator"))
from mcu_emu import McuEmu, STACK_TOP, PERIPH, PERIPH_SIZE, SYS, SYS_SIZE  # noqa: E402
from unicorn import UC_HOOK_MEM_WRITE  # noqa: E402
from unicorn.arm_const import (UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC)  # noqa: E402

CTX = 0x20000170
RX_RING = 0x20000c05
LOG_RING = 0x200010b5
SLOT = 0x96


def make_frame_a(hdr, sub, data):
    """Path A: HDR SUB LEN DATA CHK TRAILER"""
    body = bytes([hdr, sub, len(data)]) + data
    chk = sum(body) & 0xFF
    trailer = 0xFF - hdr
    return body + bytes([chk, trailer])


def make_frame_b(hdr, sub, data=b""):
    """Path B: HDR SUB CHK TRAILER DATA"""
    chk = (hdr + sub) & 0xFF
    trailer = 0xFF - hdr
    return bytes([hdr, sub, chk, trailer]) + data


def run_subcmd(frame, max_calls=8):
    emu = McuEmu(trace=False, max_insn=100000)
    uc = emu.uc
    uc.mem_write(PERIPH, b"\xff" * PERIPH_SIZE)
    uc.mem_write(SYS, bytes(SYS_SIZE))
    uc.mem_write(0x200002c8, b"\x00")   # slot A = 0
    uc.mem_write(0x200002c7, b"\x01")   # flag B = 1 (гейт открыт)
    uc.mem_write(0x200002c9, b"\x00")   # slot B = 0
    uc.mem_write(0x20000180, b"\x00")   # state = 0
    uc.mem_write(0x20000182, b"\x00")   # off = 0
    uc.mem_write(0x200001e0, struct.pack("<Q", 0x00100000))
    uc.mem_write(RX_RING, frame.ljust(SLOT, b"\x00"))

    writes = []

    def on_w(uc_, access, address, size, value, user):
        if 0x20000000 <= address < 0x20010000:
            pc = uc_.reg_read(UC_ARM_REG_PC)
            writes.append((pc, address - 0x20000000, size, value))

    uc.hook_add(UC_HOOK_MEM_WRITE, on_w)

    states_seen = []
    for call in range(max_calls):
        st_in = struct.unpack("<B", uc.mem_read(CTX + 0x180 - 0x170, 1))[0]
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
        uc.reg_write(UC_ARM_REG_LR, 1)
        try:
            uc.emu_start(0x1f71c | 1, 0, count=100005)
        except Exception:
            break
        st_out = struct.unpack("<B", uc.mem_read(CTX + 0x180 - 0x170, 1))[0]
        states_seen.append((st_in, st_out))
        # если слот сдвинули (0x2c8 стал == 0x2c7) — кадр обработан
        s = struct.unpack("<B", uc.mem_read(0x200002c8, 1))[0]
        if s == 1:
            break

    # записи в RAM (кроме CTX-служебных 0x170..0x190 и счётчиков слотов)
    data_w = {}
    for pc, a, sz, v in writes:
        if 0x180 <= a <= 0x190:      # CTX служебные
            continue
        if a in (0x2c7, 0x2c8, 0x2c9):
            continue
        data_w.setdefault(a, []).append((pc, sz, v))

    print(f"frame={frame.hex(' ')}")
    print(f"  states: {states_seen}")
    if data_w:
        for a in sorted(data_w):
            recs = data_w[a]
            vals = " ".join(f"0x{v:0{sz*2}x}" for _, sz, v in recs[:8])
            pcs = sorted(set(hex(p) for p, _, _ in recs))
            print(f"  [0x{a:05x}] {vals}   (pc={','.join(pcs[:4])})")
    else:
        print("  записей в RAM-поля: НЕТ")
    if emu.usart_out:
        print(f"  USART3: {bytes(emu.usart_out).hex(' ')}")
    return data_w


PATH_A_SUBS = [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x18, 0x19, 0x1a, 0x1b, 0x53]
PATH_B_SUBS = [0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29,
               0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f, 0x35, 0x36, 0x50, 0x51]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hdr", type=lambda x: int(x, 16), default=0x51)
    ap.add_argument("--data", default="0102030405060708",
                    help="payload для path A (hex)")
    a = ap.parse_args()
    data = bytes.fromhex(a.data)

    print(f"### PATH A (hdr=0x{a.hdr:02x}, data={data.hex(' ')})")
    for sub in PATH_A_SUBS:
        fr = make_frame_a(a.hdr, sub, data)
        run_subcmd(fr)
        print()

    print(f"### PATH B (hdr=0x{a.hdr:02x})")
    for sub in PATH_B_SUBS:
        fr = make_frame_b(a.hdr, sub)
        run_subcmd(fr)
        print()


if __name__ == "__main__":
    main()
