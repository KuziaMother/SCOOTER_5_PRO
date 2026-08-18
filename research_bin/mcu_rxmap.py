#!/usr/bin/env python3
"""
Карта переходов RX-фреймера MCU (ISR 0x1e480) — исполнением, не статикой.

Для каждой пары (state, byte) подаём байт в USART3 RX и снимаем:
  - новый (state, slot, idx)
  - куда записан байт (адрес в RAM / периферия)
Это даёт полную таблицу стейт-машины — то, что статика не смогла из-за
jump-table с вычисляемой геометрией.

Запуск:  python research_bin/mcu_rxmap.py [--states 0-40] [--out rxmap.tsv]
"""
import argparse
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "emulator"))

from mcu_emu import (McuEmu, RX_STATE, RX_SLOT, RX_IDX, RX_TO, RX_DESC_BASE,
                     USART3_SR, USART3_BASE, STACK_TOP, ISR_RET, PERIPH, SYS,
                     PERIPH_SIZE, SYS_SIZE, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UcError)
from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR
import struct

POP = (0x1E4D6, 0x1E5DC, 0x1E614)


class RMapper:
    def __init__(self):
        self.emu = McuEmu(trace=False, max_insn=200000)
        self.emu.uc.mem_write(PERIPH, bytes(PERIPH_SIZE))
        self.emu.uc.mem_write(SYS, bytes(SYS_SIZE))
        self.writes = []
        self.stopped = None
        self.h1 = self.emu.uc.hook_add(UC_HOOK_CODE, self._h_code)
        self.h2 = self.emu.uc.hook_add(UC_HOOK_MEM_WRITE, self._h_write)

    def _h_code(self, uc, address, size, user):
        if getattr(self, "_ret", False):
            uc.emu_stop()
            return
        if address in POP:
            self._ret = True
        if user is not None and user[0] > 2000:
            self.stopped = f"no-return pc=0x{address:05x}"
            uc.emu_stop()

    def _h_write(self, uc, access, address, size, value, user):
        self.writes.append((address, size, value & ((1 << (8 * size)) - 1)))

    def reset(self, state, slot=0, idx=0):
        e = self.emu.uc
        e.mem_write(RX_STATE, bytes([state]))
        e.mem_write(RX_SLOT, bytes([slot]))
        e.mem_write(RX_IDX, struct.pack("<H", idx))
        e.mem_write(RX_TO, b"\x00\x00")
        e.mem_write(RX_DESC_BASE, bytes(3 * 150))
        e.mem_write(USART3_SR, struct.pack("<I", 0))
        e.mem_write(USART3_BASE, b"\x00" * 0x20)
        self.writes = []
        self.stopped = None

    def step(self, state, byte):
        self.reset(state)
        e = self.emu.uc
        e.mem_write(USART3_SR, struct.pack("<I", 0x400))
        e.mem_write(USART3_BASE, bytes([byte]))
        self._ret = False
        e.reg_write(UC_ARM_REG_SP, STACK_TOP)
        e.reg_write(UC_ARM_REG_LR, ISR_RET | 1)
        try:
            e.emu_start(0x1E481, 0, count=2500)
        except UcError as err:
            self.stopped = f"UcError {err}"
        st = e.mem_read(RX_STATE, 1)[0]
        sl = e.mem_read(RX_SLOT, 1)[0]
        ix = struct.unpack("<H", e.mem_read(RX_IDX, 2))[0]
        return st, sl, ix, list(self.writes), self.stopped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--states", default="0-40",
                    help="диапазон состояний 'a-b' или список '1,2,3'")
    ap.add_argument("--out", default="rxmap.tsv")
    a = ap.parse_args()

    if "-" in a.states:
        lo, hi = (int(x) for x in a.states.split("-"))
        states = list(range(lo, hi + 1))
    else:
        states = [int(x) for x in a.states.split(",")]

    rm = RMapper()
    t0 = time.time()
    rows = []
    for st in states:
        for b in range(256):
            nst, nsl, nix, writes, err = rm.step(st, b)
            # куда ушёл байт? ищем запись, равную байту, в RAM-области
            where = []
            for addr, size, val in writes:
                if addr >= 0x20000000 and val == (b if size == 1 else None):
                    off = addr - 0x20000000
                    tag = ""
                    if RX_DESC_BASE <= addr < RX_DESC_BASE + 450:
                        d = addr - RX_DESC_BASE
                        tag = f"desc[{d//150}][{d%150}]"
                    where.append(f"0x20000{off:03x}{(':'+tag) if tag else ''}")
            rows.append((st, b, nst, nsl, nix, ";".join(where[:4]), err or ""))
        print(f"  state {st}: готово ({time.time()-t0:.1f}s)", flush=True)

    out = os.path.join(HERE, a.out)
    with open(out, "w", encoding="utf-8") as f:
        f.write("state\tbyte\tnew_state\tnew_slot\tnew_idx\tbyte_written_to\tnote\n")
        for r in rows:
            f.write("\t".join(str(x) for x in r) + "\n")
    print(f"записано {len(rows)} переходов -> {out}")

    # компактная сводка: для каждого состояния — какие байты принимались
    print("\nСВОДКА (state: принимаемые байты -> new_state):")
    from collections import defaultdict
    by_st = defaultdict(list)
    for st, b, nst, nsl, nix, where, err in rows:
        if (nst, nsl, nix) != (st, 0, 0) or where:
            by_st[st].append((b, nst, where))
    for st in sorted(by_st):
        items = by_st[st]
        # группируем по new_state
        groups = defaultdict(list)
        for b, nst, where in items:
            groups[nst].append(b)
        desc = ", ".join(f"{{{','.join(hex(x) for x in bs[:8])}{'...' if len(bs)>8 else ''}}}>={ns}"
                         for ns, bs in sorted(groups.items()))
        print(f"  {st:3d}: {desc}")


if __name__ == "__main__":
    main()
