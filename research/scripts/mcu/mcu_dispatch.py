#!/usr/bin/env python3
"""
Run MCU RX frame dispatcher (0x1e9e0) by execution.

Dispatcher is a stepping machine: each call advances step [0x200002c0] by one.
Script places ready frame in slot 0 RX descriptor, producer=1, step=0 and runs
0x1e9e0 until step returns to producer, capturing ALL RAM writes at each step.

Result: execution-verified "frame field -> RAM address" table + checksum
algorithm (what static analysis in §6.5 gave with caveats).

Usage:  python research/mcu_dispatch.py [--frame "74 42 05 aa bb cc dd ee 9c 0d"]
"""
import argparse
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "emulator"))

from mcu_emu import (McuEmu, RX_DESC_BASE, PERIPH, SYS, PERIPH_SIZE, SYS_SIZE,
                     STACK_TOP, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UcError)
from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR

STEP = 0x200002C0      # step/consumer
PROD = 0x200002BF      # producer (ISR slot)


class Dispatcher:
    def __init__(self):
        self.emu = McuEmu(trace=False, max_insn=200000)
        e = self.emu.uc
        e.mem_write(PERIPH, bytes(PERIPH_SIZE))
        e.mem_write(SYS, bytes(SYS_SIZE))
        self.writes = []
        self.stopped = None

    def _h_write(self, uc, access, address, size, value, user):
        self.writes.append((address, size, value & ((1 << (8 * size)) - 1)))

    def seed(self, frame):
        e = self.emu.uc
        e.mem_write(RX_DESC_BASE, frame + bytes(150 - len(frame)))
        e.mem_write(PROD, bytes([1]))          # one frame in queue
        e.mem_write(STEP, bytes([0]))
        e.mem_write(0x20000038, struct.pack("<H", 0))

    def call_once(self):
        """Single dispatcher call. Return: bx lr into unmapped 0xDEAD0001 ->
        base unmapped hook stops emulation; all writes have been made."""
        e = self.emu.uc
        self.writes = []
        self.stopped = None
        h2 = e.hook_add(UC_HOOK_MEM_WRITE, self._h_write)
        e.reg_write(UC_ARM_REG_SP, STACK_TOP)
        e.reg_write(UC_ARM_REG_LR, 0xDEAD0001)   # return to unmapped -> stop
        try:
            e.emu_start(0x1E9E1, 0, count=4000)
        except UcError as err:
            self.stopped = f"UcError {err}"
        finally:
            e.hook_del(h2)
        return self.writes, self.stopped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame", default="74 42 05 aa bb cc dd ee 9c 0d")
    a = ap.parse_args()
    frame = bytes.fromhex(a.frame.replace(" ", ""))

    d = Dispatcher()
    d.seed(frame)
    print(f"frame: {frame.hex(' ')}")
    for step_no in range(30):
        step_before = d.emu.uc.mem_read(STEP, 1)[0]
        if step_before == d.emu.uc.mem_read(PROD, 1)[0]:
            print(f"[{step_no}] step={step_before} == producer -> queue empty, stop")
            break
        writes, err = d.call_once()
        step_after = d.emu.uc.mem_read(STEP, 1)[0]
        prod = d.emu.uc.mem_read(PROD, 1)[0]
        ram = [(a_, s, v) for a_, s, v in writes if a_ >= 0x20000000]
        desc = [(a_ - RX_DESC_BASE, v) for a_, s, v in ram
                if RX_DESC_BASE <= a_ < RX_DESC_BASE + 450 and s == 1]
        others = [f"0x{a_:08x}<-0x{v:0{s*2}x}" for a_, s, v in ram if (a_, s) not in
                  [(X, 1) for X, _ in desc]]
        print(f"[{step_no}] step {step_before}->{step_after} (prod={prod})")
        if err:
            print(f"       !! {err}")
        if desc:
            print("       desc: " + ", ".join(f"[{o}]=0x{v:02x}" for o, v in desc))
        if others:
            print("       ram : " + " ".join(others[:16]))
        if step_after == step_before and not writes:
            print("       (no change - exit)")
            break


if __name__ == "__main__":
    main()
