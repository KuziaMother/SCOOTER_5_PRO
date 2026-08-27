#!/usr/bin/env python3
"""Random-sweep: верификация P-term и 2-фазного toggle в 0x1d078 (Phase B).
Проверяем поля, НЕ трогаемые anti-windup tail: S+0x2c (err clamp 300) и
S+0x5c (= s16(S+0x2c)<<7). Плюс toggle счётчика S+0x28."""
import struct
import sys

sys.path.insert(0, 'research/scripts/mcu')
from func_verify import Run, RAM
from random import Random


def sdiv(a, b):
    if b == 0:
        return 0
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def s16(x):
    x &= 0xFFFF
    return x - 0x10000 if x >= 0x8000 else x


def main():
    run = Run(max_insn=500000)
    rng = Random(11)
    N = 400
    bad_2c = bad_5c = bad_toggle = 0
    for _ in range(N):
        V = rng.randint(10, 60000)
        F = rng.getrandbits(1)
        mode = rng.choice([2, 3, 0xb, 5, 7])
        f339 = rng.getrandbits(16)
        c326 = rng.randint(1, 0x7fff)   # positive s16 (реалистичный speed-setpoint)
        m2t = rng.randint(1, 0x7fff)
        acc1 = rng.getrandbits(32); out1 = rng.randint(-32768, 32767)
        acc2 = rng.getrandbits(32); out2 = rng.randint(-32768, 32767)

        run.ram_write(0x158, struct.pack('<I', V))
        run.ram_write(0x100, bytes([F]))
        run.ram_write(0x229, bytes([mode]))
        run.ram_write(0x339, struct.pack('<H', f339))
        run.ram_write(0x324, struct.pack('<H', m2t))
        run.ram_write(0x326, struct.pack('<H', c326))
        # working struct: контролируем интеграторы
        run.ram_write(0x1768, struct.pack('<H', 0))
        run.ram_write(0x176C, struct.pack('<I', acc2))
        run.ram_write(0x1770, struct.pack('<H', out2 & 0xFFFF))
        run.ram_write(0x1774, struct.pack('<I', acc1))
        run.ram_write(0x1778, struct.pack('<H', out1 & 0xFFFF))
        # внешние inходы = 0 (anti-windup tail сбросит S+0x58/S+0x64, не трогая 2c/5c)
        run.ram_write(0x1760, struct.pack('<I', 0))
        run.ram_write(0x1764, struct.pack('<I', 0))
        run.ram_write(0x388, struct.pack('<I', 0))
        run.ram_write(0x224, struct.pack('<I', 0))
        # structB: Phase B (counter S+0x28=1), остальное 0
        run.ram_write(0x3C8, b'\x00' * 0x70)
        run.ram_write(0x3C8 + 0x28, struct.pack('<H', 1))

        run.call(0x1D078, (), max_insn=400000)

        # --- модель ---
        val = 0 if F == 0 else s16(sdiv(48000, V))
        na1 = (acc1 + val - out1) & 0xFFFFFFFF; o1n = s16(na1 >> 5)
        na2 = (acc2 + val - out2) & 0xFFFFFFFF; o2n = max(0, s16(na2 >> 3))
        flag = f339 & 0xFF
        tgt = 522 if flag == 1 else (125 if mode == 0xb else
                                     (m2t if mode == 2 else (c326 if mode == 3 else 208)))
        tgt = (tgt if s16(tgt) <= c326 else c326) & 0xFFFF
        tsgn = s16(tgt)
        err = (tsgn - o2n) if o1n < tsgn else (o2n - tsgn)
        e_2c = min(err, 300)
        e_5c = (s16(e_2c & 0xFFFF) << 7) & 0xFFFFFFFF

        g_2c = struct.unpack('<H', run.ram_read(0x3C8 + 0x2C, 2))[0]
        g_5c = struct.unpack('<I', run.ram_read(0x3C8 + 0x5C, 4))[0]
        g_28 = struct.unpack('<H', run.ram_read(0x3C8 + 0x28, 2))[0]

        if g_2c != (e_2c & 0xFFFF):
            bad_2c += 1
            if bad_2c <= 5:
                print(f"  2c got {g_2c} exp {e_2c&0xffff} (tgt={tsgn},o1n={o1n},o2n={o2n},err={err})")
        if g_5c != e_5c:
            bad_5c += 1
            if bad_5c <= 5:
                print(f"  5c got {g_5c:#x} exp {e_5c:#x} (2c={g_2c})")
        # Phase B: counter was 1 → becomes 2 → reset to 0
        if g_28 != 0:
            bad_toggle += 1

    print(f"\n[positive-target домен] S+0x2c (P-term err clamp): {N - bad_2c}/{N}")
    print(f"[positive-target домен] S+0x5c (= s16(2c)<<7):      {N - bad_5c}/{N}")
    print(f"toggle counter→0 (Phase B): {N - bad_toggle}/{N}")


if __name__ == '__main__':
    main()
