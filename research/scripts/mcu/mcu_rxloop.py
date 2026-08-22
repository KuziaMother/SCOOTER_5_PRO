#!/usr/bin/env python3
"""
Полный цикл RX: ISR-фреймер 0x1e480 + диспетчер 0x1e9e0 — всё исполнением.

Строит контрольно-корректный кадр (формат, установленный исполнением):
  class A: 74 CMD LEN D0 CHK1 8B D1..D{LEN-2} X CHK2 8B   (LEN+5 байт)
    CHK1 = (0x74 + CMD + LEN + D0) & 0xFF
    CHK2 = sum(frame[0..LEN+2]) & 0xFF
  class B: 74 CMD 4F 4B CHK1 8B   ("OK"-ответ, 6 байт)

Подаёт кадр побайтно в ISR, затем крутит диспетчер до обработки и снимает
все записи в RAM — сверка с таблицей §6.5 (поле -> адрес).

Запуск:  python research/mcu_rxloop.py [--cmd 0x42] [--len 7]
"""
import argparse
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "emulator"))

from mcu_emu import (McuEmu, RX_DESC_BASE, PERIPH, SYS, PERIPH_SIZE, SYS_SIZE,
                     STACK_TOP, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UcError)
from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC

CTX = 0x20000170
STEP_VAR = 0x200002C0   # consumer
PROD_VAR = 0x200002BF   # producer (ISR)


def build_class_a(cmd, length, data):
    """74 CMD LEN DATA[LEN] CHK2 8B; CHK2 = sum(всех предыдущих) & 0xFF."""
    assert len(data) == length, "data size"
    body = bytes([0x74, cmd, length]) + data
    chk2 = sum(body) & 0xFF
    return body + bytes([chk2, 0x8B])


def build_class_b(cmd):
    chk1 = (0x74 + cmd + 0x4F + 0x4B) & 0xFF
    return bytes([0x74, cmd, 0x4F, 0x4B, chk1, 0x8B])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cmd", default="0x42")
    ap.add_argument("--len", type=lambda s: int(s, 0), default=7)
    ap.add_argument("--class-b", action="store_true")
    a = ap.parse_args()
    cmd = int(a.cmd, 16)

    if a.class_b:
        frame = build_class_b(cmd)
    else:
        data = bytes([0x11 + i for i in range(a.len)])
        frame = build_class_a(cmd, a.len, data)
    print(f"кадр ({len(frame)} Б): {frame.hex(' ')}")

    emu = McuEmu(trace=False, max_insn=200000)
    e = emu.uc

    # --- фаза 1: побайтовый прогон ISR (чистый harness с детектом возврата) ---
    print("\n--- фаза 1: ISR-фреймер (0x1e480) ---")
    emu.feed_frame(frame, state=0, slot=0)
    prod = e.mem_read(PROD_VAR, 1)[0]
    buf = e.mem_read(RX_DESC_BASE, 150)
    print(f"producer={prod}, desc[0][:{len(frame)}] = {buf[:len(frame)].hex(' ')}")
    ok_frame = bytes(buf[:len(frame)]) == frame
    print(f"кадр в дескрипторе: {'OK' if ok_frame else 'RASHGODKLOVSIYA!'}")

    # --- фаза 2: диспетчер до обработки ---
    print("\n--- фаза 2: диспетчер (0x1e9e0) ---")
    phase_writes = []
    writes = []

    def h_w(uc, access, address, size, value, user):
        writes.append((address, size, value & ((1 << (8 * size)) - 1)))

    h = e.hook_add(UC_HOOK_MEM_WRITE, h_w)
    for i in range(20):
        cons = e.mem_read(STEP_VAR, 1)[0]
        prod = e.mem_read(PROD_VAR, 1)[0]
        step = e.mem_read(CTX + 1, 1)[0]
        if cons == prod:
            print(f"  [{i}] consumer={cons}==producer -> обработано")
            break
        writes.clear()
        e.reg_write(UC_ARM_REG_SP, STACK_TOP)
        e.reg_write(UC_ARM_REG_LR, 0xDEAD0001)
        try:
            e.emu_start(0x1E9E1, 0, count=4000)
        except UcError as ex:
            pc = e.reg_read(UC_ARM_REG_PC)
            if pc in (0xDEAD0000, 0xDEAD0001):
                pass  # чистый возврат через bx lr
            else:
                print(f"  [{i}] step={step} UcError {ex} @pc=0x{pc:08x}")
                break
        cons2 = e.mem_read(STEP_VAR, 1)[0]
        step2 = e.mem_read(CTX + 1, 1)[0]
        ram = [(x, s, v) for x, s, v in writes if x >= 0x20000000 and x < 0x20018000]
        core = [f"0x{x:06x}<-0x{v:0{s*2}x}" for x, s, v in ram
                if not (RX_DESC_BASE <= x < RX_DESC_BASE + 450)
                and not (0x20017F80 <= x <= 0x20018000)]
        print(f"  [{i}] cons {cons}->{cons2} step {step}->{step2}")
        if core:
            print("       " + " ".join(core[:20]))
        phase_writes.extend(ram)
    e.hook_del(h)

    # --- итог: куда легли поля кадра ---
    print("\n--- записи в RAM-стейт (кроме описательных/стека) ---")
    seen = {}
    for x, s, v in phase_writes:
        if RX_DESC_BASE <= x < RX_DESC_BASE + 450:
            continue
        if 0x20017F80 <= x <= 0x20018000:
            continue
        seen[x] = (s, v)
    for x in sorted(seen):
        s, v = seen[x]
        print(f"  0x{x:08x} <- 0x{v:0{s*2}x} ({s}B)")


if __name__ == "__main__":
    main()
