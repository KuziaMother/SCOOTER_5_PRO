#!/usr/bin/env python3
"""Полная верификация Phase B (ramp-core) 0x1d078: I-term + anti-windup tail.
Контролируем ВСЕ внешние входы: u32[0x1760/0x1764/0x388/0x224], S+0x58 (old int),
S+0x2e (counter). Проверяем S+0x58, S+0x60, S+0x64, S+0x2e."""
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


def s32(x):
    x &= 0xFFFFFFFF
    return x - 0x100000000 if x >= 0x80000000 else x


def model_phaseB(V, F, mode, f339, c326, m2t,
                 acc1, out1, acc2, out2, old_int, s2e_old,
                 u1760, u1764, u388, u224):
    """Возвращает (S58, S60, S64, S2e) после Phase B."""
    # --- common: val, out1_new, out2_new, target ---
    val = 0 if F == 0 else s16(sdiv(48000, V))
    # ВАЖНО: после asrs идёт sxth (1d098/1d0ac) → out1/out2 = s16, НЕ s32!
    o1n = s16(s32(acc1 + val - out1) >> 5)                  # asr5 + sxth
    o2n = max(0, s16(s32(acc2 + val - out2) >> 3))          # asr3 + sxth + clamp>=0
    flag = f339 & 0xFF
    tgt = 522 if flag == 1 else (125 if mode == 0xb else
                                 (m2t if mode == 2 else (c326 if mode == 3 else 208)))
    tgt = (tgt if s16(tgt) <= c326 else c326) & 0xFFFF
    tsgn = s16(tgt)

    # --- Step 1: branch out1 vs target (signed) ---
    if o1n < tsgn:   # INCREASE
        err = s16(tsgn - o2n)
        interim = (5 * err + old_int) & 0xFFFFFFFF
    else:            # DECREASE
        err = s16(o2n - tsgn)
        interim = (old_int - 5 * err) & 0xFFFFFFFF

    # --- Step 2: asr adjustment ---
    adj = s32(u1764 - u388) >> 3
    integral = s32(interim - adj)

    # --- Step 3: clamp integral to [8000, 131040] ---
    # integral>131040 → прыжок на 1d230 с r3=131040 (8000 не присваивается!);
    # integral<8000 → 1d230 с r3=8000; иначе keep. Т.е. обычный clamp.
    S58 = max(8000, min(integral, 131040))

    # --- Step 4: S+0x60 = asr(S58, 2) ---
    S60 = s32(S58 & 0xFFFFFFFF) >> 2

    # --- Step 5: output branch (same out1 vs target) ---
    if o1n < tsgn:   # INCREASE
        err2 = s16(tsgn - o2n)
        S2c = err2 if err2 <= 300 else 300
        P = s16(S2c & 0xFFFF) << 7
        output = P + S60
    else:            # DECREASE
        err2 = s16(o2n - tsgn)
        S2c = err2 if err2 <= 300 else 300
        P = s16(S2c & 0xFFFF) << 7
        output = S60 - P

    # --- Step 6: clamp output [1000, 32760] ---
    S64 = max(1000, min(32760, output))

    # --- Step 7: anti-windup tail (gated u32[0x1760]) ---
    if u1760 == 0:   # RESET path
        S58 = (u224 * 4) & 0xFFFFFFFF
        S64 = 0
        S2e = 0
    else:            # SLEW path
        new2e = s16(s16(s2e_old) + 1)
        if new2e > 2:          # counter was >= 2 → active
            S2e = 2
            if u1760 < S60:    # cmp u1760, S60; bge skip → if u1760 < S60
                S58 = (u1760 * 4) & 0xFFFFFFFF
            up = s32(u224 * 7) >> 1   # u224*7/2
            if up > s32(S58):
                S58 = up & 0xFFFFFFFF
        else:
            S2e = new2e
        if u1760 < S64:        # output clamp toward u1760
            S64 = u1760

    return (S58 & 0xFFFFFFFF), (S60 & 0xFFFFFFFF), (S64 & 0xFFFFFFFF), S2e


def main():
    run = Run(max_insn=500000)
    rng = Random(23)
    N = 2000
    bad = {f: 0 for f in ('S58', 'S60', 'S64', 'S2e')}
    shown = 0
    for _ in range(N):
        V = rng.randint(10, 60000)
        F = rng.getrandbits(1)
        mode = rng.choice([2, 3, 0xb, 5, 7])
        f339 = rng.getrandbits(16)
        c326 = rng.randint(1, 0x7fff)
        m2t = rng.randint(1, 0x7fff)
        acc1 = rng.getrandbits(32); out1 = rng.randint(-32768, 32767)
        acc2 = rng.getrandbits(32); out2 = rng.randint(-32768, 32767)
        old_int = rng.getrandbits(32)
        s2e_old = rng.randint(0, 5)
        u1760 = rng.choice([0, 0, rng.getrandbits(16), rng.getrandbits(20)])
        u1764 = rng.getrandbits(24)
        u388 = rng.getrandbits(24)
        u224 = rng.getrandbits(20)

        run.ram_write(0x158, struct.pack('<I', V))
        run.ram_write(0x100, bytes([F]))
        run.ram_write(0x229, bytes([mode]))
        run.ram_write(0x339, struct.pack('<H', f339))
        run.ram_write(0x333, b'\x00')          # skip mode-change block
        run.ram_write(0x263, b'\x00')          # gate → ramp-core
        run.ram_write(0x324, struct.pack('<H', m2t))
        run.ram_write(0x326, struct.pack('<H', c326))
        run.ram_write(0x1768, struct.pack('<H', 0))
        run.ram_write(0x176C, struct.pack('<I', acc2))
        run.ram_write(0x1770, struct.pack('<H', out2 & 0xFFFF))
        run.ram_write(0x1774, struct.pack('<I', acc1))
        run.ram_write(0x1778, struct.pack('<H', out1 & 0xFFFF))
        run.ram_write(0x1760, struct.pack('<I', u1760))
        run.ram_write(0x1764, struct.pack('<I', u1764))
        run.ram_write(0x388, struct.pack('<I', u388))
        run.ram_write(0x224, struct.pack('<I', u224))
        # structB: Phase B (counter S+0x28=1), old integral, counter S+0x2e
        run.ram_write(0x3C8, b'\x00' * 0x70)
        run.ram_write(0x3C8 + 0x28, struct.pack('<H', 1))
        run.ram_write(0x3C8 + 0x58, struct.pack('<I', old_int))
        run.ram_write(0x3C8 + 0x2E, struct.pack('<H', s2e_old))

        run.call(0x1D078, (), max_insn=400000)

        e58, e60, e64, e2e = model_phaseB(V, F, mode, f339, c326, m2t,
                                          acc1, out1, acc2, out2, old_int, s2e_old,
                                          u1760, u1764, u388, u224)
        g58 = struct.unpack('<I', run.ram_read(0x3C8 + 0x58, 4))[0]
        g60 = struct.unpack('<I', run.ram_read(0x3C8 + 0x60, 4))[0]
        g64 = struct.unpack('<I', run.ram_read(0x3C8 + 0x64, 4))[0]
        g2e = struct.unpack('<H', run.ram_read(0x3C8 + 0x2E, 2))[0]

        if g64 != e64 and not getattr(main, '_dumped', False):
            main._dumped = True
            val = 0 if F == 0 else s16(sdiv(48000, V))
            o1n = s32(((acc1 + val - out1) & 0xFFFFFFFF) >> 5)
            o2n = max(0, s32(((acc2 + val - out2) & 0xFFFFFFFF) >> 3))
            flag = f339 & 0xFF
            tgt = 522 if flag == 1 else (125 if mode == 0xb else
                                         (m2t if mode == 2 else (c326 if mode == 3 else 208)))
            tgt = (tgt if s16(tgt) <= c326 else c326) & 0xFFFF
            tsgn = s16(tgt)
            br = 'INC' if o1n < tsgn else 'DEC'
            err2 = s16((tsgn - o2n) if br == 'INC' else (o2n - tsgn))
            S2c = err2 if err2 <= 300 else 300
            P = s16(S2c & 0xFFFF) << 7
            step6 = (P + e60) if br == 'INC' else (e60 - P)
            print("=== ПЕРВЫЙ S64-СБОЙ: полные входы ===")
            print(f"V={V} F={F} mode={mode} f339={f339} c326={c326} m2t={m2t}")
            print(f"acc1={acc1} out1={out1} acc2={acc2} out2={out2}")
            print(f"old_int={old_int} s2e_old={s2e_old}")
            print(f"u1760={u1760} u1764={u1764} u388={u388} u224={u224}")
            print(f"модель: o1n={o1n} o2n={o2n} tgt={tsgn} br={br}")
            print(f"  err2={err2} S2c={S2c} P={P} S60={e60} step6={step6} "
                  f"clamp[1000,32760]={max(1000,min(32760,step6))}")
            print(f"  S64 got={g64} exp={e64} (slew-clamp u1760={u1760})")

        for name, g, e in (('S58', g58, e58), ('S60', g60, e60),
                           ('S64', g64, e64), ('S2e', g2e, e2e)):
            if g != e:
                bad[name] += 1
                if shown < 8:
                    print(f"  {name} got {g} exp {e} "
                          f"(u1760={u1760},s2e_old={s2e_old},old_int={old_int},"
                          f"o1n/o2n/tgt via V={V},F={F},mode={mode})")
                    shown += 1

    print(f"\nPhase B полная модель ({N} итер):")
    for f in ('S58', 'S60', 'S64', 'S2e'):
        print(f"  {f}: {N - bad[f]}/{N}")


if __name__ == '__main__':
    main()
