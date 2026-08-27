#!/usr/bin/env python3
"""Зонд v4: две фазы 0x1d078 (mod-2 toggle по S+0x28).
Вызов 2 раза подряд: call1 (counter=0 → короткий путь), call2 (counter=1 → ramp-core).
Лог write-значений (надёжны) + read-адресов. Входы известны, т.ч. значения вычисляемы."""
import struct
import sys

sys.path.insert(0, 'research/scripts/mcu')
from func_verify import Run, RAM
from unicorn import UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE

W = 0x1768
S = 0x3C8


def name(rel):
    if S <= rel < S + 0x80:
        return f"S+0x{rel - S:02x}"
    if W <= rel < W + 0x40:
        return f"W+0x{rel - W:02x}"
    return f"@0x{rel:03x}"


def trace_call(run, label):
    events = []

    def mk(tag):
        def h(uc, access, address, size, value, user):
            rel = address - RAM
            if rel < 0x150 or rel > 0x450:
                return
            events.append(f"{tag} {name(rel):<12}"
                          + (f"= {value:#x}" if tag == 'W' else ""))
        return h

    hr = run.uc.hook_add(UC_HOOK_MEM_READ, mk('R'), None, RAM + 0x150, 0x320)
    hw = run.uc.hook_add(UC_HOOK_MEM_WRITE, mk('W'), None, RAM + 0x150, 0x320)
    run.call(0x1D078, (), max_insn=400000)
    run.uc.hook_del(hr)
    run.uc.hook_del(hw)
    print(f"\n=== {label} ({len(events)} событий) ===")
    for e in events:
        print("  " + e)


def main():
    run = Run(max_insn=500000)
    V, F = 3000, 1          # val=16 → out1=0, out2=2 после обновления
    mode, f339, c326, m2t = 3, 0, 520, 400
    run.ram_write(0x158, struct.pack('<I', V))
    run.ram_write(0x100, bytes([F]))
    run.ram_write(0x229, bytes([mode]))
    run.ram_write(0x339, struct.pack('<H', f339))
    run.ram_write(0x324, struct.pack('<H', m2t))
    run.ram_write(0x326, struct.pack('<H', c326))
    run.ram_write(W, b'\x00' * 0x28)
    run.ram_write(S, b'\x00' * 0x70)   # counter S+0x28=0 → Phase A

    trace_call(run, "PHASE A (counter=0 → короткий путь)")
    trace_call(run, "PHASE B (counter=1 → ramp-core PID)")


if __name__ == '__main__':
    main()
