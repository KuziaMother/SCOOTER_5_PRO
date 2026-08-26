#!/usr/bin/env python3
"""Random-sweep: связка target (setpoint) / out2 (оценка скорости) → structB.
Чистое состояние интеграторов (acc=out=0) + structB state=0 (init-путь).
Цель: эмпирически определить structB[+0x2a] и structB[+0x2c] как функцию
(target_clamped, out2_after), чтобы добавить перманентный тест."""
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


def run_once(run, V, F, mode, f339, c326, m2t):
    run.ram_write(0x158, struct.pack('<I', V))
    run.ram_write(0x100, bytes([F]))
    run.ram_write(0x229, bytes([mode]))
    run.ram_write(0x339, struct.pack('<H', f339))
    run.ram_write(0x324, struct.pack('<H', m2t))
    run.ram_write(0x326, struct.pack('<H', c326))
    # чистые интеграторы + init-состояние structB
    for off in range(0x1768, 0x1790):
        pass
    run.ram_write(0x1768, b'\x00' * 0x28)
    run.ram_write(0x3C8, b'\x00' * 0x70)   # structB: state=0, всё 0
    run.call(0x1D078, (), max_insn=400000)

    val = 0 if F == 0 else s16(sdiv(48000, V))
    out2 = max(0, s16((val) >> 3))   # acc2: 0+val-0=val → asr(val,3), clamp>=0
    flag = f339 & 0xFF
    if flag == 1:
        tgt = 522
    elif mode == 0xb:
        tgt = 125
    elif mode == 2:
        tgt = m2t
    elif mode == 3:
        tgt = c326
    else:
        tgt = 208
    clamped = (tgt if s16(tgt) <= c326 else c326) & 0xFFFF

    g_2a = struct.unpack('<H', run.ram_read(0x3C8 + 0x2A, 2))[0]
    g_2c = struct.unpack('<H', run.ram_read(0x3C8 + 0x2C, 2))[0]
    g_58 = struct.unpack('<I', run.ram_read(0x3C8 + 0x58, 4))[0]
    g_out = struct.unpack('<I', run.ram_read(0x1768 + 0x18, 4))[0]
    return val, out2, clamped, g_2a, g_2c, g_58, g_out


def main():
    run = Run(max_insn=500000)
    rng = Random(7)
    N = 300
    bad_2a = bad_2c = 0
    samples = []
    for _ in range(N):
        V = rng.randint(10, 60000)
        F = rng.getrandbits(1)
        mode = rng.choice([2, 3, 0xb, 5, 7])
        f339 = rng.getrandbits(16)
        c326 = rng.getrandbits(16)
        m2t = rng.getrandbits(16)
        val, out2, clamped, g_2a, g_2c, g_58, g_out = run_once(
            run, V, F, mode, f339, c326, m2t)
        if g_2a != clamped:
            bad_2a += 1
            if bad_2a <= 5:
                print(f"  МISMATCH +0x2a: got {g_2a} exp {clamped} "
                      f"(mode={mode},flag={f339&0xFF},c326={c326},m2t={m2t})")
        # ошибка = target - out2 (signed), ожидаем кламп к 300 сверху
        err = s16(clamped) - out2
        samples.append((s16(clamped), out2, g_2c, err))

    print(f"\n[+0x2a == clamped target]: {N - bad_2a}/{N} совпало")

    # эмпирика по +0x2c: как g_2c зависит от (target, out2)
    print("\n=== выборка (target_s16, out2, got_2c, err=target-out2) ===")
    for t, o, g, e in samples[:40]:
        print(f"  tgt={t:>6} out2={o:>5}  +0x2c={g:>5}   err={e:>6}")

    # гипотеза: +0x2c = clamp(err, lo, 300)? проверим диапазон got
    vals = [s for _, _, s, _ in samples]
    print(f"\n  min(+0x2c)={min(vals)}  max(+0x2c)={max(vals)}")
    # проверка: когда err в (0..300), +0x2c должен = err; когда err>300 → 300
    chk = sum(1 for t, o, g, e in samples if 0 < e <= 300 and g == e)
    tot = sum(1 for _, _, _, e in samples if 0 < e <= 300)
    print(f"  err∈(0,300] → +0x2c==err: {chk}/{tot}")
    chk2 = sum(1 for t, o, g, e in samples if e > 300 and g == 300)
    tot2 = sum(1 for _, _, _, e in samples if e > 300)
    print(f"  err>300 → +0x2c==300: {chk2}/{tot2}")


if __name__ == '__main__':
    main()
