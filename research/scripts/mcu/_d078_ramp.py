#!/usr/bin/env python3
"""Зонд v2: расшифровка ramp-машины 0x1d078 (structB@0x3c8 → r4[+0x18]).
Чистые значения интеграторов (чтобы out1/out2 не были мусором), сентинелы только
на structB, исправленная детекция базы S/W. Цель: понять P/I/D-термы контроллера."""
import struct
import sys

sys.path.insert(0, 'research/scripts/mcu')
from func_verify import Run, RAM
from unicorn import UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE

W = 0x1768   # working struct r4
S = 0x3C8    # structB


def dump(run, base, fields):
    for off, nm in fields:
        sz = 4 if off >= 0x50 else (1 if nm.startswith('b') else 2)
        fmt = '<I' if sz == 4 else ('<B' if sz == 1 else '<H')
        v = struct.unpack(fmt, run.ram_read(base + off, sz))[0]
        print(f"    [+0x{off:02x}] {nm:<7} = {v}")


def main():
    run = Run(max_insn=500000)

    V, F = 3000, 1          # val = 48000/3000 = 16
    mode, f339, c326, m2t = 3, 0, 520, 400

    run.ram_write(0x158, struct.pack('<I', V))
    run.ram_write(0x100, bytes([F]))
    run.ram_write(0x229, bytes([mode]))
    run.ram_write(0x339, struct.pack('<H', f339))
    run.ram_write(0x324, struct.pack('<H', m2t))
    run.ram_write(0x326, struct.pack('<H', c326))

    # working struct: ЧИСТЫЕ значения (интеграторы с нуля)
    run.ram_write(W + 0x00, struct.pack('<H', 0))
    run.ram_write(W + 0x04, struct.pack('<I', 0))   # acc2
    run.ram_write(W + 0x08, struct.pack('<H', 0))   # out2
    run.ram_write(W + 0x0C, struct.pack('<I', 0))   # acc1
    run.ram_write(W + 0x10, struct.pack('<H', 0))   # out1
    run.ram_write(W + 0x14, struct.pack('<H', 0))   # target (перезапишется)
    run.ram_write(W + 0x16, bytes([0]))
    run.ram_write(W + 0x18, struct.pack('<I', 0))   # OUT

    # structB: сентинелы (только здесь)
    run.ram_write(S + 0x00, bytes([0xC0]))          # state
    run.ram_write(S + 0x10, bytes([0xC1]))
    for off in (0x24, 0x26, 0x28, 0x2A, 0x2C, 0x2E):
        run.ram_write(S + off, struct.pack('<H', 0xC000 | off))
    for off in (0x58, 0x5C, 0x60, 0x64):
        run.ram_write(S + off, struct.pack('<I', 0xC0000000 | off))

    events = []

    def mk(tag):
        def h(uc, access, address, size, value, user):
            rel = address - RAM
            if S <= rel < S + 0x80:
                b, o = 'S', rel - S
            elif W <= rel < W + 0x40:
                b, o = 'W', rel - W
            else:
                return
            events.append(f"{tag} {b}+0x{o:02x}"
                          + (f" = {value:#x}" if tag == 'W' else ""))
        return h

    hr = run.uc.hook_add(UC_HOOK_MEM_READ, mk('R'), None, RAM + 0x3c8, 0x1400)
    hw = run.uc.hook_add(UC_HOOK_MEM_WRITE, mk('W'), None, RAM + 0x3c8, 0x1400)

    print("=== BEFORE (structB) ===")
    dump(run, S, [(0, 'state'), (0x10, 'b10'), (0x24, 'f24'), (0x26, 'f26'),
                  (0x28, 'f28'), (0x2A, 'f2a'), (0x2C, 'f2c'), (0x2E, 'f2e'),
                  (0x58, 'f58'), (0x5C, 'f5c'), (0x60, 'f60'), (0x64, 'f64')])

    for it in range(3):   # 3 итерации, чтобы увидеть динамику
        run.call(0x1D078, (), max_insn=400000)
        print(f"\n=== после итерации {it+1} ===")
        print("  working:")
        dump(run, W, [(0, 'val'), (4, 'acc2'), (8, 'out2'), (0xC, 'acc1'),
                      (0x10, 'out1'), (0x14, 'target'), (0x18, 'OUT')])
        print("  structB:")
        dump(run, S, [(0, 'state'), (0x24, 'f24'), (0x26, 'f26'), (0x28, 'f28'),
                      (0x2A, 'f2a'), (0x2C, 'f2c'), (0x2E, 'f2e'),
                      (0x58, 'f58'), (0x5C, 'f5c'), (0x60, 'f60'), (0x64, 'f64')])

    run.uc.hook_del(hr)
    run.uc.hook_del(hw)

    print(f"\n=== ACCESS TRACE (итерация 1: {len(events)} событий) ===")
    for e in events[:60]:
        print("  " + e)


if __name__ == '__main__':
    main()
