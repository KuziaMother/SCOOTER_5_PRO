#!/usr/bin/env python3
"""
Blob-конфиги #1/#2/#3 (@0x844..@0x880): кто пишет, кто читает.

1) SET-свип: для каждой Path-A подкоманды 0x10..0x1b гоняем стейт-машину
   0x1f71c с валидным кадром и ловим ВСЕ записи в RAM 0x840..0x880.
2) GET-захват: предзаполняем blob-регион паттерном, гоняем Path-B подкоманды
   0x22/0x28/0x29/0x2a и снимаем TX-кадры из кольца @0x10b5 (маппинг полей).

Запуск:  python research/scripts/mcu/mcu_blobs.py [set|get|all]
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "emulator"))
from mcu_emu import McuEmu, STACK_TOP  # noqa: E402
from unicorn import UC_HOOK_MEM_WRITE  # noqa: E402
from unicorn.arm_const import (UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC)  # noqa: E402

CTX = 0x20000170
RX_RING = 0x20000c05
TX_RING = 0x200010b5
SLOT = 0x96


def make_frame_a(hdr, sub, data):
    body = bytes([hdr, sub, len(data)]) + data
    chk = sum(body) & 0xFF
    return body + bytes([chk, 0xFF - hdr])


def make_frame_b(hdr, sub, data=b""):
    return bytes([hdr, sub, (hdr + sub) & 0xFF, 0xFF - hdr]) + data


def drive(frame, max_calls=10):
    """Гоняем 0x1f71c до стабилизации; возвращаем emu и список (pc, addr, size, val)."""
    emu = McuEmu(trace=False, max_insn=200000)
    uc = emu.uc
    uc.mem_write(0x200002c8, b"\x00")   # RX head
    uc.mem_write(0x200002c7, b"\x01")   # flag (не пусто)
    uc.mem_write(0x200002c9, b"\x00")   # TX head
    uc.mem_write(CTX + 0x180 - 0x170, b"\x00")
    uc.mem_write(CTX + 0x182 - 0x170, b"\x00")
    uc.mem_write(RX_RING, frame.ljust(SLOT, b"\x00"))

    writes = []

    def on_w(uc_, _access, address, size, value, _user):
        pc = uc_.reg_read(UC_ARM_REG_PC)
        writes.append((pc & ~1, address - 0x20000000, size, value))

    uc.hook_add(UC_HOOK_MEM_WRITE, on_w)
    for _ in range(max_calls):
        st = struct.unpack("<B", uc.mem_read(CTX + 0x180 - 0x170, 1))[0]
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
        uc.reg_write(UC_ARM_REG_LR, 1)
        try:
            uc.emu_start(0x1f71c | 1, 0, count=200005)
        except Exception:
            break
        st2 = struct.unpack("<B", uc.mem_read(CTX + 0x180 - 0x170, 1))[0]
        if st2 == st and _ > 3:
            break
    return emu, writes


def tx_frames(emu):
    """Снимаем TX-кадры из кольца @0x10b5 (сканируем все 8 слотов)."""
    uc = emu.uc
    out = []
    for i in range(8):
        raw = bytes(uc.mem_read(TX_RING + i * SLOT, 40))
        if raw[0] == 0:
            continue
        ln = raw[0]
        out.append((i, raw[:ln + 1]))
    return out


def run_set_sweep():
    print("=" * 72)
    print("SET-СВИП Path A (0x51 xx DATA): записи в RAM 0x840..0x880")
    print("=" * 72)
    for sub in list(range(0x10, 0x1c)) + [0x53]:
        # data: 20 байт паттерна (чтобы хватало для любого blob)
        data = bytes((i + 1) & 0xFF for i in range(20))
        frame = make_frame_a(0x51, sub, data)
        emu, writes = drive(frame)
        blob_w = [(pc, off, size, val) for pc, off, size, val in writes
                  if 0x840 <= off < 0x880]
        flag_w = [(pc, off, size, val) for pc, off, size, val in writes
                  if off in (0x170, 0x241, 0x243, 0x337, 0x338)]
        if blob_w or flag_w:
            print(f"\nsub 0x{sub:02x} (len=20):")
            for pc, off, size, val in blob_w[:24]:
                print(f"   {pc:05x}: RAM 0x{off:03x} <- {val:#0{(size*2)+2}x} (size={size})")
            for pc, off, size, val in flag_w[:8]:
                print(f"   {pc:05x}: FLAG 0x{off:03x} <- {val:#04x}")


def run_get_capture():
    print()
    print("=" * 72)
    print("GET-ЗАХВАТ Path B: TX-кадры при предзаполненном blob-регионе")
    print("=" * 72)
    # паттерн: RAM 0x844+i = i*7+3 (уникальный на 0x844..0x880)
    seed = bytes((i * 7 + 3) & 0xFF for i in range(0x880 - 0x844))
    for sub, name in ((0x22, "конфиг#1 формат."), (0x28, "конфиг#1 raw"),
                      (0x29, "конфиг#2 raw"), (0x2a, "конфиг#3 сид")):
        emu = McuEmu(trace=False, max_insn=200000)
        uc = emu.uc
        uc.mem_write(0x20000844, seed)
        uc.mem_write(0x200002c8, b"\x00")
        uc.mem_write(0x200002c7, b"\x01")
        uc.mem_write(0x200002c9, b"\x00")
        uc.mem_write(CTX + 0x180 - 0x170, b"\x00")
        uc.mem_write(CTX + 0x182 - 0x170, b"\x00")
        uc.mem_write(RX_RING, make_frame_b(0x51, sub).ljust(SLOT, b"\x00"))
        for _ in range(6):
            uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
            uc.reg_write(UC_ARM_REG_LR, 1)
            try:
                uc.emu_start(0x1f71c | 1, 0, count=200005)
            except Exception:
                break
        frames = tx_frames(emu)
        out = bytes(emu.usart_out) if emu.usart_out else b""
        print(f"\nsub 0x{sub:02x} ({name}):")
        if out:
            print(f"   USART3: {out.hex(' ')}")
            # маппинг: какие байты кадра = паттерну RAM 0x844+i (i*7+3)
            hits = []
            for j, b in enumerate(out):
                i = (b - 3) % 256 / 7 if False else None
                # решаем i: (7i+3) mod 256 == b  →  i = (b-3)*inv7 mod 256
                for k in range(0x40):
                    if (k * 7 + 3) & 0xFF == b:
                        hits.append((j, f"RAM0x{0x844 + k:03x}"))
                        break
            print(f"   маппинг: {hits}")
        else:
            print("   USART3 пусто")
        for slot, f in frames:
            print(f"   TX-ring slot{slot}: {f.hex(' ')}")
            hits = []
            for j, b in enumerate(f):
                for k in range(0x40):
                    if (k * 7 + 3) & 0xFF == b:
                        hits.append((j, f"RAM0x{0x844 + k:03x}"))
                        break
            print(f"   маппинг: {hits}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("set", "all"):
        run_set_sweep()
    if mode in ("get", "all"):
        run_get_capture()
