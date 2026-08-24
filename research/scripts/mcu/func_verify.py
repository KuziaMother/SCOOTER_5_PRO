# -*- coding: utf-8 -*-
"""
Эмуляторная верификация записей каталога ANALYZED_MCU (gen_maps.py).

Для каждой разобранной функции — свой тест: исполняем РЕАЛЬНЫЙ код на Unicorn
случайными входами и сверяем результат с независимым Python-референсом
(задокументированное поведение из REPORT.md/каталога).

Запуск:  python -X utf8 research/scripts/mcu/func_verify.py [--only 0x126c] [--seed N]
         python -X utf8 research/scripts/mcu/func_verify.py --list   # покрытые функции

Добавление теста — функция в TESTS (декоратор @t(off, desc)):
    @t(0x126C, 'u64 LSR')
    def _(run, rng):
        lo, hi, n = ...
        r0, r1 = run.call(0x126C, (lo, hi, n))
        assert (r0, r1) == expected, f'...'
"""
import argparse
import os
import random
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))          # research/scripts/mcu
RES = os.path.dirname(os.path.dirname(HERE))               # research
REPO = os.path.dirname(RES)                                # D:/SCOOTER_5_PRO
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(RES, 'scripts'))

from unicorn import UcError, UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                               UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_LR,
                               UC_ARM_REG_CPSR)

from emulator.mcu_emu import McuEmu, FLASH0, FLASH1, RAM, STACK_TOP

FW = open(os.path.join(RES, 'images', 'mcu_0007.bin'), 'rb').read()
FW_LEN = len(FW)
M32 = 0xFFFFFFFF
M64 = 0xFFFFFFFFFFFFFFFF


class Run:
    """один экземпляр эмулятора на все тесты (чистые функции не портят состояние)"""

    def __init__(self, max_insn=500000):
        # 500K — запас под wait-циклы с таймаутом (0xC8A4: до ~240K инстр.)
        self.emu = McuEmu(max_insn=max_insn)
        self.uc = self.emu.uc
        # периферия/SYS — нули (чистые функции к ним не обращаются;
        # если обращение и есть — стоп по лимиту, тест упадёт с ошибкой)
        self._stop_hook = None

    def call(self, off, args=(), max_insn=50000):
        """вызвать функцию (Thumb), вернуть (r0, r1) на момент возврата"""
        uc = self.uc
        # ВАЖНО: сброс кумулятивного счётчика инструкций McuEmu —
        # иначе после ~max_insn суммарных инструкций хук _h_code
        # останавливает каждый новый вызов ДО первой инструкции
        self.emu.insn = 0
        for r, v in zip((UC_ARM_REG_R0, UC_ARM_REG_R1,
                         UC_ARM_REG_R2, UC_ARM_REG_R3), args):
            uc.reg_write(r, v & M32)
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)   # возврат в незамапленное

        def stop(uc_, addr, size, user):
            if not (FLASH0 <= addr < FLASH0 + FW_LEN or
                    FLASH1 <= addr < FLASH1 + FW_LEN):
                uc_.emu_stop()
        self._stop_hook = uc.hook_add(UC_HOOK_CODE, stop)
        try:
            uc.emu_start(off | 1, 0, count=max_insn)
        except UcError:
            pass
        uc.hook_del(self._stop_hook)
        return (uc.reg_read(UC_ARM_REG_R0) & M32, uc.reg_read(UC_ARM_REG_R1) & M32)

    def flags(self):
        """CPSR-флаги после последнего вызова: (N, Z, C, V)
        Архитектурное расположение битов ARM CPSR: N=31, Z=30, C=29, V=28"""
        cpsr = self.uc.reg_read(UC_ARM_REG_CPSR)
        return ((cpsr >> 31) & 1, (cpsr >> 30) & 1,
                (cpsr >> 29) & 1, (cpsr >> 28) & 1)

    def ram_write(self, off, data):
        self.uc.mem_write(RAM + off, data)

    def ram_read(self, off, size):
        return bytes(self.uc.mem_read(RAM + off, size))

    # --- периферия (McuEmu мапит PERIPH/SYS как обычную память) ---
    def periph_write(self, addr, val):
        self.uc.mem_write(addr, struct.pack('<I', val & M32))

    def periph_read(self, addr):
        return struct.unpack('<I', bytes(self.uc.mem_read(addr, 4)))[0]


# ---------------------------------------------------------------------------
# референсы (независимые Python-модели задокументированного поведения)
# ---------------------------------------------------------------------------

def ref_u64lsr(lo, hi, n):
    P = ((hi << 32) | lo) >> n
    return P & M32, P >> 32


def ref_u64lsl(lo, hi, n):
    P = (((hi << 32) | lo) << n) & M64
    return P & M32, P >> 32


def ref_u64asr(lo, hi, n):
    v = (hi << 32) | lo
    if v >= 1 << 63:
        v -= 1 << 64
    q = v >> n                      # арифметический (floor для отриц.)
    return q & M32, (q >> 32) & M32


def ref_scale_123e(lo, hi, r2):
    """0x123e: r1' = (r1&0xFFFFF)|0x100000; масштаб u64 {r1':lo} на 2^(r2-0x433)"""
    hp = ((hi & 0xFFFFF) | 0x100000) & M32
    V = (hp << 32) | lo             # верхнее слово уже замаскировано!
    if r2 < 0x3FF:
        return 0, hp                # сентинел {r1', 0}
    if r2 <= 0x433:
        P = V >> (0x433 - r2)
        return P & M32, P >> 32
    P = (V << (r2 - 0x433)) & M64
    return P & M32, hp              # верхнее слово не меняется


def ref_161ea(num, den, n):
    """0x161ea(num, den, n) = floor((num/den) × 2^n) — точное фикс-деление (§52.1 эмуляторно)."""
    if den == 0:
        return 0
    return (num * (1 << n)) // den & M32


def ref_seg_interp_unsigned(A, B, slope):
    """сегмент 0x16938: ветка по UNSIGNED сравнению A vs B (bhi)"""
    if A > B:
        d = (A - B) & M32
        return (A - ((d * slope) >> 31)) & M32
    d = (B - A) & M32
    return (A + ((d * slope) >> 31)) & M32


def ref_seg_interp(A, B, slope):
    """сегмент 0x16880/0x16938: ветка по SIGNED сравнению A=ys[r4], B=ys[r4+1] (bgt);
    delta — wrapped u32; result = A ± (delta*slope)>>31"""
    sA = A - 0x100000000 if A >= 0x80000000 else A
    sB = B - 0x100000000 if B >= 0x80000000 else B
    if sA > sB:
        d = (A - B) & M32
        return (A - ((d * slope) >> 31)) & M32
    d = (B - A) & M32
    return (A + ((d * slope) >> 31)) & M32


def ref_scale_1a052(lo, hi, r2, r3):
    """0x1a052: n = r2>>21; масштаб u64 на 2^(n-0x433), нижняя граница r3.
    Внимание: в lsl-ветке r1 перезаписывается смещением (n-0x433)."""
    n = (r2 & M32) >> 21
    V = (hi << 32) | lo
    if n < r3:
        return 0, hi                # сентинел {0, r1} — r1 не меняется
    if n <= 0x433:
        P = V >> (0x433 - n)
        return P & M32, P >> 32
    P = (V << (n - 0x433)) & M64
    return P & M32, (n - 0x433)     # r1 = смещение, не верхнее слово


def ref_mul64(a, b):
    P = a * b
    return P & M32, P >> 32


def ref_trunc_mul(a, b, n):
    """0x1712c: низкие 32 бита (A*B >> n) — фиксированная точка"""
    return ((a * b) >> n) & M32


def ref_prod_check(a, b):
    """0x17150: (P_hi==0) ? P_lo : -1 — «умещается ли произведение в 32 бита»"""
    P = a * b
    return (P & M32) if (P >> 32) == 0 else M32


def ref_u64add_round(a_lo, a_hi, b_lo, b_hi):
    """0x128c/0x1a16a: A += 1; B <<= 1 (если B<0); если B стало 0 → A &= ~1"""
    A = ((a_hi << 32) | a_lo) & M64
    B = ((b_hi << 32) | b_lo) & M64
    if B >= 1 << 63:                # signed < 0
        A = (A + 1) & M64
        B2 = (B * 2) & M64
        if B2 == 0:
            A &= ~1
    return A & M32, A >> 32


def ref_sdiv32(a, b):
    """0x16222: signed div u32 с округлением до ближайшего (ties up)"""
    if b == 0:
        return None
    q = abs(a) // abs(b)
    if 2 * (abs(a) % abs(b)) >= abs(b):
        q += 1
    if (a < 0) != (b < 0):
        q = -q
    return q & M32


def ref_sdiv64(d_lo, d_hi, s_lo, s_hi):
    """0x19a1c: signed u64 div → (quotient {r1:r0}, remainder {r3:r2})"""
    def s64(lo, hi):
        v = (hi << 32) | lo
        return v - (1 << 64) if v >= 1 << 63 else v
    d, s = s64(d_lo, d_hi), s64(s_lo, s_hi)
    if s == 0:
        return None
    q = abs(d) // abs(s)
    if (d < 0) != (s < 0):
        q = -q
    r = d - q * s
    q &= M64
    r &= M64
    return (q & M32, q >> 32), (r & M32, r >> 32)


def ref_avg16(buf, start, cnt):
    """0x5044: среднее u16-массива (целочисленное)"""
    s = sum(struct.unpack_from('<%dH' % cnt, buf, start * 2))
    return s // cnt & M32


def ref_grid_snap(minv, step, maxq, val):
    """0xdd2c: clamp + снап на сетку min+step*q (округление до ближайшего)"""
    mx = minv + step * maxq
    if val < minv:
        return minv
    if val > mx:
        return mx
    d = val - minv
    q, rem = divmod(d, step)
    if 2 * rem > step:              # bhi — строгое
        q += 1
    q = min(q, maxq)
    return minv + step * q


def ref_crc32_step(byte, state):
    """0x1a838: crc = (state<<24)^byte; 8 бит MSB-first, poly 0x04C11DB7"""
    crc = ((state << 24) ^ byte) & M32
    for _ in range(8):
        crc = (((crc << 1) ^ 0x04C11DB7) if crc & 0x80000000 else (crc << 1)) & M32
    return crc


def ref_crc16(buf, poly=0x1021):
    """CRC-16/CCITT-FALSE: poly 0x1021, init 0, MSB-first, без xorout
    (корректировка §50.7: в каталоге ошибочно было «poly 0xA001»)"""
    crc = 0
    for b in buf:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ poly) if crc & 0x8000 else (crc << 1)
            crc &= 0xFFFF
    return crc


def ref_crc8(buf, poly=0x2F):
    """0x87f8: CRC-8 MSB-first, init 0"""
    crc = 0
    for b in buf:
        crc ^= b
        for _ in range(8):
            crc = (((crc << 1) ^ poly) if crc & 0x80 else (crc << 1)) & 0xFF
    return crc


def ref_crc7_port(byte, state):
    """точный порт ассемблера 0x3c7c: r0 ^= byte; 8×: (r0<<1)&0xFF ^ (msb?7:0)"""
    r0 = (state ^ byte) & 0xFF
    for _ in range(8):
        if r0 & 0x80:
            r0 = ((r0 << 1) & 0xFF) ^ 7
        else:
            r0 = (r0 << 1) & 0xFF
    return r0


def ref_bcd2bin(b):
    """0xc9a8: hi*10 + lo — десятичное значение BCD-байта"""
    hi, lo = b >> 4, b & 0xF
    return hi * 10 + lo


def ref_bin2bcd(v):
    v &= M32
    n = 0
    while v >= 10:
        v -= 10
        n += 1
    return (n << 4) | v


# ---------------------------------------------------------------------------
# тесты
# ---------------------------------------------------------------------------

TESTS = []


def t(off, desc):
    def deco(fn):
        TESTS.append((off, desc, fn))
        return fn
    return deco


# --- u64-сдвиги (кластер, скорректирован в §50.6) ---

@t(0x161EA, 'фикс-деление: floor((r0/r1) × 2^r2)')
def _(run, rng):
    num = rng.getrandbits(32)
    den = rng.getrandbits(32) or 1
    n = rng.choice([8, 15, 16, 20, 31])
    r0, _ = run.call(0x161EA, (num, den, n), max_insn=20000)
    assert r0 == ref_161ea(num, den, n), f'({num:#x},{den:#x},{n}) → {r0:#x}'


@t(0x126C, 'u64 LSR (r1:r0) >> r2')
def _(run, rng):
    lo, hi = rng.getrandbits(32), rng.getrandbits(32)
    n = rng.choice([0, 1, 7, 15, 31, 32, 33, 40, 63])
    r0, r1 = run.call(0x126C, (lo, hi, n))
    assert (r0, r1) == ref_u64lsr(lo, hi, n), \
        f'({lo:#x},{hi:#x},{n}) → ({r0:#x},{r1:#x})'


@t(0x1A0A0, 'u64 LSR — копия 0x126c')
def _(run, rng):
    lo, hi = rng.getrandbits(32), rng.getrandbits(32)
    n = rng.choice([0, 1, 31, 32, 63])
    r0, r1 = run.call(0x1A0A0, (lo, hi, n))
    assert (r0, r1) == ref_u64lsr(lo, hi, n), \
        f'({lo:#x},{hi:#x},{n}) → ({r0:#x},{r1:#x})'


@t(0x1A080, 'u64 LSL (r1:r0) << r2')
def _(run, rng):
    lo, hi = rng.getrandbits(32), rng.getrandbits(32)
    n = rng.choice([0, 1, 7, 15, 31, 32, 33, 40, 63])
    r0, r1 = run.call(0x1A080, (lo, hi, n))
    assert (r0, r1) == ref_u64lsl(lo, hi, n), \
        f'({lo:#x},{hi:#x},{n}) → ({r0:#x},{r1:#x})'


@t(0x1A0C2, 'u64 ASR (r1:r0) >>s r2')
def _(run, rng):
    lo, hi = rng.getrandbits(32), rng.getrandbits(32)
    n = rng.choice([0, 1, 7, 15, 31, 32, 33, 40, 63])
    r0, r1 = run.call(0x1A0C2, (lo, hi, n))
    assert (r0, r1) == ref_u64asr(lo, hi, n), \
        f'({lo:#x},{hi:#x},{n}) → ({r0:#x},{r1:#x})'


# --- u64-масштабирование 2^(n-0x433) ---

@t(0x123E, 'u64 масштаб 2^(r2-0x433), окно [0x3FF..]')
def _(run, rng):
    lo, hi = rng.getrandbits(32), rng.getrandbits(32)
    r2 = rng.choice([0x300, 0x3FE, 0x3FF, 0x400, 0x432, 0x433, 0x434, 0x450, 0x500])
    r0, r1 = run.call(0x123E, (lo, hi, r2))
    assert (r0, r1) == ref_scale_123e(lo, hi, r2), \
        f'({lo:#x},{hi:#x},{r2:#x}) → ({r0:#x},{r1:#x})'


@t(0x1A052, 'u64 масштаб 2^(n-0x433), n = r2>>21, floor r3')
def _(run, rng):
    lo, hi = rng.getrandbits(32), rng.getrandbits(32)
    # безопасные n: сырой сдвиг в u64lsr = (0x433-n)-32 должен быть < 256
    # или ((s&0xFF)>28) — иначе баг Unicorn со сдвигами по регистру (см. §50.7)
    n = rng.choice([0x314, 0x3FF, 0x400, 0x433, 0x434, 0x500])
    r3 = rng.choice([0, 1, 0x3FF, 0x433])
    r2 = (n << 21) | rng.getrandbits(21)
    r0, r1 = run.call(0x1A052, (lo, hi, r2, r3))
    assert (r0, r1) == ref_scale_1a052(lo, hi, r2, r3), \
        f'({lo:#x},{hi:#x},{r2:#x},{r3:#x}) → ({r0:#x},{r1:#x})'


# --- умножение u32×u32→u64 и производные ---

@t(0x172B8, 'u32×u32 → u64: [r2]=HIGH, [r3]=LOW (указатели перепутаны!)')
def _(run, rng):
    a, b = rng.getrandbits(32), rng.getrandbits(32)
    p_lo, p_hi = RAM + 0x19000, RAM + 0x19004
    run.call(0x172B8, (a, b, p_lo, p_hi))
    got = struct.unpack_from('<II', run.ram_read(0x19000, 8))
    exp_lo, exp_hi = ref_mul64(a, b)
    assert got == (exp_hi, exp_lo), \
        f'({a:#x},{b:#x}) → {[hex(x) for x in got]}, ждали hi/lo {(hex(exp_hi), hex(exp_lo))}'


@t(0x1712C, 'урезанное умножение: верх/низ (32-n) бит P')
def _(run, rng):
    a, b = rng.getrandbits(32), rng.getrandbits(32)
    n = rng.choice([1, 4, 8, 16, 24, 31])
    r0, _ = run.call(0x1712C, (a, b, n))
    assert r0 == ref_trunc_mul(a, b, n), f'({a:#x},{b:#x},{n}) → {r0:#x}'


@t(0x17150, 'проверка произведения: (P_hi==0)? P_lo : -1')
def _(run, rng):
    # микс: большие (переполнение) и малые (умещается)
    a = rng.choice([rng.getrandbits(32), rng.getrandbits(12)])
    b = rng.choice([rng.getrandbits(32), rng.getrandbits(12)])
    r0, _ = run.call(0x17150, (a, b))
    assert r0 == ref_prod_check(a, b), f'({a:#x},{b:#x}) → {r0:#x}'


# --- сравнение signed u64 (флаги) ---

@t(0x1494, 'cmp g(a) vs g(b): g(x)=x if x≥2^63 else 2^63-x (float 0x16040: bhs ⇔ a≤b)')
def _(run, rng):
    a = rng.getrandbits(64)
    b = rng.getrandbits(64)
    run.call(0x1494, (a & M32, a >> 32, b & M32, b >> 32))
    n, z, c, v = run.flags()
    def g(x):
        # отрицательные (bit63=1) — без изменения; неотрицательные — 2^63-x
        return x if x >= (1 << 63) else ((1 << 63) - x) & M64
    ga, gb = g(a), g(b)
    def cmpf(x, y):
        d = (x - y) & M32
        return ((d >> 31) & 1, d == 0, x >= y,
                (((x >> 31) ^ (y >> 31)) & ((x >> 31) ^ (d >> 31))))
    hi_a, lo_a = ga >> 32, ga & M32
    hi_b, lo_b = gb >> 32, gb & M32
    exp = cmpf(lo_a, lo_b) if hi_a == hi_b else cmpf(hi_a, hi_b)
    assert (n, z, c, v) == exp, \
        f'a={a:#x} b={b:#x} → flags {(n,z,c,v)}, ждали {exp}'


# --- u64 add с округлением ---

@t(0x128C, 'u64 add-round (B<0: A+=1, B<<=1; B==0: A&=~1)')
def _(run, rng):
    alo, ahi, blo, bhi = (rng.getrandbits(32) for _ in range(4))
    r0, r1 = run.call(0x128C, (alo, ahi, blo, bhi))
    assert (r0, r1) == ref_u64add_round(alo, ahi, blo, bhi), \
        f'({alo:#x},{ahi:#x},{blo:#x},{bhi:#x}) → ({r0:#x},{r1:#x})'


@t(0x1A16A, 'u64 add-round — копия 0x128c')
def _(run, rng):
    alo, ahi, blo, bhi = (rng.getrandbits(32) for _ in range(4))
    r0, r1 = run.call(0x1A16A, (alo, ahi, blo, bhi))
    assert (r0, r1) == ref_u64add_round(alo, ahi, blo, bhi), \
        f'({alo:#x},{ahi:#x},{blo:#x},{bhi:#x}) → ({r0:#x},{r1:#x})'


# --- деление ---

@t(0x16222, 'sdiv u32, округление до ближайшего (ties up)')
def _(run, rng):
    a = rng.randint(-(1 << 31), (1 << 31) - 1)
    b = rng.choice([1, -1, 2, -2, 3, 7, -7])
    r0, _ = run.call(0x16222, (a & M32, b & M32))
    exp = ref_sdiv32(a, b)
    assert r0 == exp, f'({a},{b}) → {r0:#x}, ждали {exp:#x}'


@t(0x19A1C, 'sdiv u64 → (q {r1:r0}, rem {r3:r2}), trunc к нулю')
def _(run, rng):
    d = rng.randint(-(1 << 63), (1 << 63) - 1)
    s = rng.choice([1, -1, 2, -2, 3, 5, -5, 1000, -1000])
    r0, r1 = run.call(0x19A1C, (d & M32, d >> 32, s & M32, s >> 32))
    # остаток читаем из r2/r3 — допишем в Run.call позже если нужно;
    # пока сверяем только частное
    exp_q, _ = ref_sdiv64(d & M32, d >> 32, s & M32, s >> 32)
    assert (r0, r1) == exp_q, f'({d},{s}) → ({r0:#x},{r1:#x}), ждали {exp_q}'


# --- среднее u16 ---

@t(0x5044, 'среднее u16-массива (целое)')
def _(run, rng):
    start = rng.randint(0, 8)
    cnt = rng.randint(1, 16)
    buf = struct.pack('<%dH' % (start + cnt), *([0] * start +
                                                 [rng.getrandbits(16) for _ in range(cnt)]))
    run.ram_write(0x19100, buf)
    r0, _ = run.call(0x5044, (RAM + 0x19100, start, cnt))
    exp = ref_avg16(buf, start, cnt)
    assert r0 == exp, f'start={start} cnt={cnt} buf={buf.hex()} → {r0}, ждали {exp}'


# --- снап на сетку ---

@t(0xDD2C, 'clamp + снап на сетку min+step*q')
def _(run, rng):
    minv = rng.getrandbits(20)
    step = rng.randint(1, 0xFFF)
    maxq = rng.randint(0, 0xFFFF)
    val = rng.randint(minv - 0x100, minv + step * maxq + 0x100)
    r0, _ = run.call(0xDD2C, (minv, step, maxq, val))
    exp = ref_grid_snap(minv, step, maxq, val)
    assert r0 == exp, f'(min={minv},step={step},maxq={maxq},val={val}) → {r0:#x}, ждали {exp:#x}'


# --- CRC-семья ---

@t(0x1A838, 'CRC-32 byte-step: (state<<24)^byte, MSB-first, poly 0x04C11DB7')
def _(run, rng):
    byte = rng.getrandbits(8)
    state = rng.getrandbits(32)
    r0, _ = run.call(0x1A838, (byte, state))
    exp = ref_crc32_step(byte, state)
    assert r0 == exp, f'(byte={byte:#x},state={state:#x}) → {r0:#x}, ждали {exp:#x}'


@t(0xAAD0, 'CRC-16/CCITT-FALSE буфер (poly 0x1021, init 0)')
def _(run, rng):
    buf = bytes(rng.getrandbits(8) for _ in range(rng.randint(1, 32)))
    run.ram_write(0x19200, buf)
    r0, _ = run.call(0xAAD0, (RAM + 0x19200, len(buf)))
    exp = ref_crc16(buf)
    assert r0 == exp, f'buf={buf.hex()} → {r0:#x}, ждали {exp:#x}'


@t(0x87F8, 'CRC-8 буфер: poly 0x2F, MSB-first, init 0')
def _(run, rng):
    buf = bytes(rng.getrandbits(8) for _ in range(rng.randint(1, 32)))
    run.ram_write(0x19200, buf)
    r0, _ = run.call(0x87F8, (RAM + 0x19200, len(buf)))
    exp = ref_crc8(buf)
    assert r0 == exp, f'buf={buf.hex()} → {r0:#x}, ждали {exp:#x}'


@t(0x3C7C, 'CRC-7 byte-step (порт ассемблера; сверка с poly 0x09)')
def _(run, rng):
    byte = rng.getrandbits(8)
    state = rng.getrandbits(8)
    r0, _ = run.call(0x3C7C, (byte, state))
    exp = ref_crc7_port(byte, state)
    assert r0 == exp, f'(byte={byte:#x},state={state:#x}) → {r0:#x}, ждали {exp:#x}'


# --- BCD-пара ---

@t(0xC9A8, 'BCD→binary (один байт: hi*5+lo)')
def _(run, rng):
    b = rng.getrandbits(8)
    r0, _ = run.call(0xC9A8, (b,))
    assert r0 == ref_bcd2bin(b), f'({b:#x}) → {r0}, ждали {ref_bcd2bin(b)}'


@t(0xC9BE, 'binary→BCD (0..99 → BCD-байт)')
def _(run, rng):
    v = rng.randint(0, 99)
    r0, _ = run.call(0xC9BE, (v,))
    assert r0 == ref_bin2bcd(v), f'({v}) → {r0:#x}, ждали {ref_bin2bcd(v):#x}'


# ===========================================================================
# БАТЧ 2: RAM-accessors, set/clear-биты, структуры, memset, периферия RCC/FLASH
# ===========================================================================

RCC = 0x40021000      # база RCC (CFGR0=+4, CTLR=+0, ext=+0x60)
FLASH = 0x40022000    # база FLASH (CTLR=+0, SR=+0xC, SCBR=+0x10)

# --- простые getter'ы/setter'ы по указателю ---

@t(0x7FD4, 'getter byte: r0 = u8@r0')
def _(run, rng):
    b = rng.getrandbits(8)
    run.ram_write(0x19400, bytes([b]))
    r0, _ = run.call(0x7FD4, (RAM + 0x19400,))
    assert r0 == b, f'({b:#x}) → {r0:#x}'


@t(0xE3E4, 'setter u16 = 0: *(u16@r0) = 0')
def _(run, rng):
    run.ram_write(0x19410, struct.pack('<H', 0xABCD))
    run.call(0xE3E4, (RAM + 0x19410,))
    assert run.ram_read(0x19410, 2) == b'\x00\x00'


@t(0x4F50, 'getter u16 @+4: r0 = u16*(base+4)')
def _(run, rng):
    v = rng.getrandbits(16)
    run.ram_write(0x19420, struct.pack('<II', 0xDEADBEEF, v))
    r0, _ = run.call(0x4F50, (RAM + 0x19420,))
    assert r0 == v, f'({v:#x}) → {r0:#x}'


@t(0x99B4, 'getter byte из u16@+0x10')
def _(run, rng):
    v = rng.getrandbits(16)
    buf = bytearray(0x12)
    struct.pack_into('<H', buf, 0x10, v)
    run.ram_write(0x19430, bytes(buf))
    r0, _ = run.call(0x99B4, (RAM + 0x19430,))
    assert r0 == (v & 0xFF), f'({v:#x}) → {r0:#x}'


@t(0x4E38, 'setter +4: *(u32*[r1+4]) = r0')
def _(run, rng):
    v = rng.getrandbits(32)
    run.ram_write(0x19440, b'\x00' * 8)
    run.call(0x4E38, (v, RAM + 0x19440))
    assert struct.unpack_from('<I', run.ram_read(0x19440, 8), 4)[0] == v


@t(0x4FBA, 'setter +4: *(u32*[r0+4]) = r1')
def _(run, rng):
    v = rng.getrandbits(32)
    run.ram_write(0x19450, b'\x00' * 8)
    run.call(0x4FBA, (RAM + 0x19450, v))
    assert struct.unpack_from('<I', run.ram_read(0x19450, 8), 4)[0] == v


@t(0x87E2, 'cond setter: r2 ? *[r0+0x18] : *[r0+0x28] = r1')
def _(run, rng):
    v = rng.getrandbits(32)
    mode = rng.getrandbits(1)
    run.ram_write(0x19460, b'\x00' * 0x30)
    run.call(0x87E2, (RAM + 0x19460, v, mode))
    off = 0x18 if mode else 0x28
    assert struct.unpack_from('<I', run.ram_read(0x19460, 0x30), off)[0] == v


@t(0x4FAC, 'cond setter: *[r2+0x10] = (r3 ? r0 : 0)')
def _(run, rng):
    v = rng.getrandbits(32)
    mode = rng.getrandbits(1)
    run.ram_write(0x19470, b'\x00' * 0x20)
    run.call(0x4FAC, (v, 0, RAM + 0x19470, mode))
    assert struct.unpack_from('<I', run.ram_read(0x19470, 0x20), 0x10)[0] == (v if mode else 0)


# --- проверка масок (return 0/1) ---

@t(0x87C8, 'mask check: (*(u32*[r0+0x10]) & r1) != 0')
def _(run, rng):
    val = rng.getrandbits(32)
    mask = rng.getrandbits(32)
    run.ram_write(0x19480, b'\x00' * 0x10 + struct.pack('<I', val))
    r0, _ = run.call(0x87C8, (RAM + 0x19480, mask))
    assert r0 == (1 if (val & mask) else 0), f'val={val:#x} mask={mask:#x} → {r0}'


@t(0x4F58, 'mask check: (*(u32*r1) & r0) != 0')
def _(run, rng):
    val = rng.getrandbits(32)
    mask = rng.getrandbits(32)
    run.ram_write(0x19490, struct.pack('<I', val))
    r0, _ = run.call(0x4F58, (mask, RAM + 0x19490))
    assert r0 == (1 if (val & mask) else 0), f'val={val:#x} mask={mask:#x} → {r0}'


# --- set/clear битов/масок ---

# таблица set/clear-функций: адрес → маска (hardcoded; аргументы: r0=ptr, r1=mode)
_SETCLR = {
    0x97CA: 0x400,
    0x982C: 0x001,
    0x9844: 0x100,
    0x985C: 0x200,
}

def _mk_setclear(off, mask):
    def _(run, rng):
        init = rng.getrandbits(16)
        mode = rng.getrandbits(1)
        run.ram_write(0x194A0, struct.pack('<H', init))
        run.call(off, (RAM + 0x194A0, mode))
        exp = (init | mask) if mode else (init & ~mask & 0xFFFF)
        got = struct.unpack_from('<H', run.ram_read(0x194A0, 2))[0]
        assert got == exp, f'init={init:#x} mode={mode} → {got:#x}, ждали {exp:#x}'
    return _

for _off, _mask in _SETCLR.items():
    globals()['_t_' + format(_off, 'x')] = t(_off, f'set/clear {_mask:#x} в u16@r0 (mode=r1)')(_mk_setclear(_off, _mask))


@t(0x97E2, 'set/clear mask в u16@+4 (mask=r1, mode=r2)')
def _(run, rng):
    init = rng.getrandbits(16)
    mask = rng.getrandbits(16)
    mode = rng.getrandbits(1)
    run.ram_write(0x194B0, struct.pack('<I', 0) + struct.pack('<H', init))
    run.call(0x97E2, (RAM + 0x194B0, mask, mode))
    exp = (init | mask) if mode else (init & ~mask)
    got = struct.unpack_from('<H', run.ram_read(0x194B0, 6), 4)[0]
    assert got == (exp & 0xFFFF), f'init={init:#x} mask={mask:#x} mode={mode} → {got:#x}'


@t(0x99BC, 'u16@+0x10 = (r1|1) if r2 else (r1&~1) — r1 = ВХОДНОЕ значение!')
def _(run, rng):
    val = rng.getrandbits(16)
    mode = rng.getrandbits(1)
    run.ram_write(0x194C0, b'\x00' * 0x12)
    run.call(0x99BC, (RAM + 0x194C0, val, mode))
    exp = (val | 1) if mode else (val & ~1 & 0xFFFF)
    got = struct.unpack_from('<H', run.ram_read(0x194C0, 0x12), 0x10)[0]
    assert got == exp, f'val={val:#x} mode={mode} → {got:#x}, ждали {exp:#x}'


@t(0x4F38, 'set: u32@r0 |= 1; clear: u32@r0 &= 0xFFFE (ТРУНКИРОВАНИЕ до u16!)')
def _(run, rng):
    init = rng.getrandbits(32)
    mode = rng.getrandbits(1)
    run.ram_write(0x194D0, struct.pack('<I', init))
    run.call(0x4F38, (RAM + 0x194D0, mode))
    # асимметрия: set — полное u32, clear — маска 0xFFFE (старшие 16 бит сбрасываются)
    exp = (init | 1) if mode else (init & 0xFFFE)
    got = struct.unpack_from('<I', run.ram_read(0x194D0, 4))[0]
    assert got == (exp & M32), f'init={init:#x} mode={mode} → {got:#x}, ждали {exp:#x}'


# --- структуры ---

@t(0xC464, 'struct write {u32=r1,+4=0,+5=0,+6=r2,+7=r3} → 1')
def _(run, rng):
    a = rng.getrandbits(32)
    b = rng.getrandbits(8)
    c = rng.getrandbits(8)
    run.ram_write(0x194E0, b'\xFF' * 8)
    r0, _ = run.call(0xC464, (RAM + 0x194E0, a, b, c))
    assert r0 == 1, f'return {r0}'
    buf = run.ram_read(0x194E0, 8)
    assert struct.unpack_from('<I', buf)[0] == a
    assert buf[4] == 0 and buf[5] == 0 and buf[6] == b and buf[7] == c, f'buf={buf.hex()}'


@t(0x87B0, 'struct init {u16=0xFFFF,+2=0,+3=0,+4=0,+8=0(u32),+0xC=0xF(u32)}')
def _(run, rng):
    run.ram_write(0x194F0, b'\xAA' * 16)
    run.call(0x87B0, (RAM + 0x194F0,))
    buf = run.ram_read(0x194F0, 16)
    assert buf[0] == 0xFF and buf[1] == 0xFF, f'[{0:02x}..{1:02x}]={buf[:2].hex()}'
    assert buf[2] == 0 and buf[3] == 0 and buf[4] == 0
    assert struct.unpack_from('<I', buf, 8)[0] == 0
    assert struct.unpack_from('<I', buf, 0xC)[0] == 0xF


# --- memset ---

@t(0x19A8C, 'memset(dst=r0, count=r1, val=r2)')
def _(run, rng):
    n = rng.randint(0, 40)
    v = rng.getrandbits(8)
    run.ram_write(0x19500, b'\x00' * 48)
    run.call(0x19A8C, (RAM + 0x19500, n, v))
    buf = run.ram_read(0x19500, 48)
    assert buf[:n] == bytes([v]) * n, f'n={n} v={v:#x} buf={buf[:n].hex()}'
    assert buf[n:] == b'\x00' * (48 - n)


@t(0x19A9E, 'memset swap (dst=r0, val=r1, count=r2) → dst')
def _(run, rng):
    n = rng.randint(0, 40)
    v = rng.getrandbits(8)
    run.ram_write(0x19520, b'\x00' * 48)
    r0, _ = run.call(0x19A9E, (RAM + 0x19520, v, n))
    assert r0 == RAM + 0x19520, f'return {r0:#x}'
    buf = run.ram_read(0x19520, 48)
    assert buf[:n] == bytes([v]) * n


# --- былые пути (без периферийных циклов) ---

@t(0x6304, 'fast path: (r0&3)!=0 → 9')
def _(run, rng):
    base = rng.getrandbits(28) << 2
    v = base + rng.choice([1, 2, 3])
    r0, _ = run.call(0x6304, (v, 0))
    assert r0 == 9, f'({v:#x}) → {r0}'


@t(0x2E0C, 'arg0==0 или arg1==0 → 1')
def _(run, rng):
    r0, _ = run.call(0x2E0C, (0, rng.getrandbits(32)))
    assert r0 == 1, f'(0, *) → {r0}'
    r0, _ = run.call(0x2E0C, (rng.getrandbits(31) + 1, 0))
    assert r0 == 1, f'(*, 0) → {r0}'


# --- RCC (предзапись значений в PERIPH) ---

@t(0xC894, 'RCC_CFGR0 & 0xC (AHB-прескалер)')
def _(run, rng):
    v = rng.getrandbits(32)
    run.periph_write(RCC + 4, v)
    r0, _ = run.call(0xC894, ())
    assert r0 == (v & 0xC), f'({v:#x}) → {r0:#x}'


@t(0xC4B4, 'RCC_CFGR0[7:4] = r0 (HPRE)')
def _(run, rng):
    init = rng.getrandbits(32)
    new = rng.getrandbits(4) << 4
    run.periph_write(RCC + 4, init)
    run.call(0xC4B4, (new,))
    exp = (init & ~0xF0) | new
    assert run.periph_read(RCC + 4) == exp, f'init={init:#x} new={new:#x}'


@t(0xC580, 'RCC_CFGR0[10:8] = r0 (PPRE1)')
def _(run, rng):
    init = rng.getrandbits(32)
    new = rng.getrandbits(3) << 8
    run.periph_write(RCC + 4, init)
    run.call(0xC580, (new,))
    exp = (init & ~0x700) | new
    assert run.periph_read(RCC + 4) == exp


@t(0xC60C, 'RCC_CFGR0[1:0] = r0 (SW)')
def _(run, rng):
    init = rng.getrandbits(32)
    new = rng.getrandbits(2)
    run.periph_write(RCC + 4, init)
    run.call(0xC60C, (new,))
    exp = (init & ~3) | new
    assert run.periph_read(RCC + 4) == exp


@t(0xC598, 'RCC_CFGR0[14:11] = r0<<3 (PPRE2)')
def _(run, rng):
    init = rng.getrandbits(32)
    new = rng.getrandbits(4)
    run.periph_write(RCC + 4, init)
    run.call(0xC598, (new,))
    exp = (init & ~0x3800) | ((new & 0xF) << 3)
    assert run.periph_read(RCC + 4) == exp


@t(0x225C4, 'set/clear mask в RCC_CTLR (mode=r1)')
def _(run, rng):
    init = rng.getrandbits(32)
    mask = rng.getrandbits(32)
    mode = rng.getrandbits(1)
    run.periph_write(RCC + 0, init)
    run.call(0x225C4, (mask, mode))
    exp = (init | mask) if mode else (init & ~mask)
    assert run.periph_read(RCC + 0) == (exp & M32)


@t(0x225DC, 'set/clear mask в RCC+0x60 (mode=r1)')
def _(run, rng):
    init = rng.getrandbits(32)
    mask = rng.getrandbits(32)
    mode = rng.getrandbits(1)
    run.periph_write(RCC + 0x60, init)
    run.call(0x225DC, (mask, mode))
    exp = (init | mask) if mode else (init & ~mask)
    assert run.periph_read(RCC + 0x60) == (exp & M32)


# --- FLASH (предзапись значений в PERIPH) ---

@t(0x62D4, 'FLASH_SCBR |= 0x80')
def _(run, rng):
    init = rng.getrandbits(32)
    run.periph_write(FLASH + 0x10, init)
    run.call(0x62D4, ())
    assert run.periph_read(FLASH + 0x10) == (init | 0x80)


@t(0x6360, 'FLASH_CTLR: keep[6:3], [5:3]=r0, clear[2:0]')
def _(run, rng):
    init = rng.getrandbits(32)
    new = rng.getrandbits(32)
    run.periph_write(FLASH + 0, init)
    run.call(0x6360, (new,))
    exp = (init & 0xF8) | new
    assert run.periph_read(FLASH + 0) == (exp & M32), f'init={init:#x} new={new:#x}'


@t(0x61D4, 'FLASH_SR |= r0')
def _(run, rng):
    init = rng.getrandbits(32)
    v = rng.getrandbits(32)
    run.periph_write(FLASH + 0xC, init)
    run.call(0x61D4, (v,))
    assert run.periph_read(FLASH + 0xC) == (init | v)


def ref_flash_sr_code(sr):
    if sr & 1:
        return 1
    if sr & 4:
        return 3
    if sr & 8:
        return 4
    if sr & 0x10:
        return 5
    if sr & 0x40:
        return 7
    return 6


@t(0x6284, 'FLASH_SR → status code (1/3/4/5/7/6)')
def _(run, rng):
    sr = rng.getrandbits(32)
    run.periph_write(FLASH + 0xC, sr)
    r0, _ = run.call(0x6284, ())
    assert r0 == ref_flash_sr_code(sr), f'sr={sr:#x} → {r0}'


# ===========================================================================
# БАТЧ 3: fixed-address getter'ы, RCC-семья, wait-циклы, драйвер @0x40003000
# ===========================================================================

DRV = 0x40003000      # таинственный драйвер (§48/§49)
AFIO_EXTI = 0x40010414  # AFIO-зона (0x5970)

# --- fixed-address getter'ы (пул = константа RAM, НЕ двойная индирекция) ---

@t(0x8878, 'getter byte@RAM[0x128]')
def _(run, rng):
    b = rng.getrandbits(8)
    run.ram_write(0x128, bytes([b]))
    r0, _ = run.call(0x8878, ())
    assert r0 == b, f'({b:#x}) → {r0:#x}'


@t(0x8AF0, 'getter byte@RAM[0xA73]')
def _(run, rng):
    b = rng.getrandbits(8)
    run.ram_write(0xA73, bytes([b]))
    r0, _ = run.call(0x8AF0, ())
    assert r0 == b, f'({b:#x}) → {r0:#x}'


@t(0x8D90, 'getter u32@RAM[0x1344]')
def _(run, rng):
    v = rng.getrandbits(32)
    run.ram_write(0x1344, struct.pack('<I', v))
    r0, _ = run.call(0x8D90, ())
    assert r0 == v, f'({v:#x}) → {r0:#x}'


@t(0x8E14, 'getter byte@RAM[0x1378] (пул 0x20001359 + 0x1F)')
def _(run, rng):
    b = rng.getrandbits(8)
    run.ram_write(0x1378, bytes([b]))
    r0, _ = run.call(0x8E14, ())
    assert r0 == b, f'({b:#x}) → {r0:#x}'


@t(0xA6A4, 'getter byte@RAM[0x40]')
def _(run, rng):
    b = rng.getrandbits(8)
    run.ram_write(0x40, bytes([b]))
    r0, _ = run.call(0xA6A4, ())
    assert r0 == b, f'({b:#x}) → {r0:#x}'


@t(0x833C, 'getter byte@RAM[0xC8D] (флаг 0x8xxx-драйвера)')
def _(run, rng):
    b = rng.getrandbits(8)
    run.ram_write(0xC8D, bytes([b]))
    r0, _ = run.call(0x833C, ())
    assert r0 == b, f'({b:#x}) → {r0:#x}'


@t(0x21C0C, 'getter u32@RAM[0x2C] (пул 0x20000028 + 4; НЕ двойная индирекция!)')
def _(run, rng):
    v = rng.getrandbits(32)
    run.ram_write(0x2C, struct.pack('<I', v))
    r0, _ = run.call(0x21C0C, ())
    assert r0 == v, f'({v:#x}) → {r0:#x}'


@t(0x8A44, 'getter u32@RAM[0xF6A] (пул 0x20000F64 + 6; НЕ *(u32)+6!)')
def _(run, rng):
    v = rng.getrandbits(32)
    run.ram_write(0xF6A, struct.pack('<I', v))
    r0, _ = run.call(0x8A44, ())
    assert r0 == v, f'({v:#x}) → {r0:#x}'


# --- u16-accessors по указателю ---

@t(0x1072A, 'getter u16 @+0xC')
def _(run, rng):
    v = rng.getrandbits(16)
    run.ram_write(0x19540, b'\x00' * 12 + struct.pack('<H', v))
    r0, _ = run.call(0x1072A, (RAM + 0x19540,))
    assert r0 == v, f'({v:#x}) → {r0:#x}'


@t(0x10730, 'setter u16 @+0xC: *(u16*[r0+0xC]) = r1')
def _(run, rng):
    v = rng.getrandbits(16)
    run.ram_write(0x19550, b'\x00' * 0x10)
    run.call(0x10730, (RAM + 0x19550, v))
    assert struct.unpack_from('<H', run.ram_read(0x19550, 0x10), 0xC)[0] == v


@t(0x99CE, 'setter u16 @+0x10: *(u16*[r0+0x10]) = r1')
def _(run, rng):
    v = rng.getrandbits(16)
    run.ram_write(0x19560, b'\x00' * 0x14)
    run.call(0x99CE, (RAM + 0x19560, v))
    assert struct.unpack_from('<H', run.ram_read(0x19560, 0x14), 0x10)[0] == v


# --- RCC set/clear (mask=r0, mode=r1) ---

def _mk_rcc_setclear(off, reg_off):
    def _(run, rng):
        init = rng.getrandbits(32)
        mask = rng.getrandbits(32)
        mode = rng.getrandbits(1)
        run.periph_write(RCC + reg_off, init)
        run.call(off, (mask, mode))
        exp = (init | mask) if mode else (init & ~mask)
        got = run.periph_read(RCC + reg_off)
        assert got == (exp & M32), f'reg+{reg_off:#x} init={init:#x} mask={mask:#x} mode={mode} → {got:#x}'
    return _

for _off, _ro in ((0xC6C4, 0xC), (0xC684, 0x10), (0xC624, 0x14), (0xC6A4, 0x18)):
    globals()['_t_rcc_' + format(_off, 'x')] = t(
        _off, f'set/clear mask в RCC+{_ro:#x} (mode=r1)')(_mk_rcc_setclear(_off, _ro))


@t(0xC518, 'RCC_CTLR bit0 (HSI/HSE-ON) := (r0==1) — сначала always-clear')
def _(run, rng):
    init = rng.getrandbits(32)
    mode = rng.getrandbits(1)
    run.periph_write(RCC + 0, init)
    run.call(0xC518, (mode,))
    exp = (init & ~1) | mode
    assert run.periph_read(RCC + 0) == exp, f'init={init:#x} mode={mode}'


# --- RCC flag check: group=r0>>5 (1=CTLR, 2=+0x20, иначе +0x24), bit=r0&0x1F ---

@t(0xC858, 'RCC flag check: group/bit decode')
def _(run, rng):
    regs = {0: rng.getrandbits(32), 0x20: rng.getrandbits(32), 0x24: rng.getrandbits(32)}
    run.periph_write(RCC + 0, regs[0])
    run.periph_write(RCC + 0x20, regs[0x20])
    run.periph_write(RCC + 0x24, regs[0x24])
    group = rng.choice([1, 2, 0, 3])
    bit = rng.randint(0, 31)
    arg = (group << 5) | bit
    roff = {1: 0, 2: 0x20}.get(group, 0x24)
    exp = 1 if (regs[roff] >> bit) & 1 else 0
    r0, _ = run.call(0xC858, (arg,))
    assert r0 == exp, f'group={group} bit={bit} arg={arg:#x} → {r0}, ждали {exp}'


# --- wait-циклы с таймаутом (флаг предзаписан или нет) ---

# Аргумент 0xc858: (group<<5 | bit), group: 1=CTLR(+0), 2=+0x20, иначе +0x24.
# 0xC8A4: arg 0x31 = 49 → group 49>>5 = 1 (CTLR), bit 49&0x1F = 17
# 0xC8DC: arg 0x21 = 33 → group 33>>5 = 1 (CTLR!), bit 1 — это HSERDY, НЕ +0x24!
# 0xC914: arg 0x63 = 99 → group 99>>5 = 3 (+0x24), bit 3

@t(0xC8A4, 'wait CTLR bit17 (arg 0x31), timeout 0x2000 → 0/1')
def _(run, rng):
    flag = rng.getrandbits(1)
    run.periph_write(RCC + 0, (rng.getrandbits(32) & ~0x20000) | (flag << 17))
    # таймаут-ветка: 8192 итерации × ~29 инстр ≈ 240K — нужен большой бюджет
    r0, _ = run.call(0xC8A4, (), max_insn=300000)
    assert r0 == flag, f'flag={flag} → {r0}'


@t(0xC8DC, 'wait CTLR bit1 (HSERDY!) (arg 0x21: group=1), timeout 0x500 → 0/1')
def _(run, rng):
    flag = rng.getrandbits(1)
    run.periph_write(RCC + 0, (rng.getrandbits(32) & ~2) | (flag << 1))
    r0, _ = run.call(0xC8DC, (), max_insn=100000)
    assert r0 == flag, f'flag={flag} → {r0}'


@t(0xC914, 'wait RCC+0x24 bit3 (arg 0x63: group3→+0x24!), timeout 0x500 → 0/1')
def _(run, rng):
    flag = rng.getrandbits(1)
    run.periph_write(RCC + 0x24, (rng.getrandbits(32) & ~8) | (flag << 3))
    r0, _ = run.call(0xC914, (), max_insn=100000)
    assert r0 == flag, f'flag={flag} → {r0}'


# --- HSE enable: failure path (HSERDY не появился за 0x500) ---

@t(0x10ABC, 'HSE on + wait; timeout → fallback 0x003D0900 в RAM[0xB88], return константа')
def _(run, rng):
    run.periph_write(RCC + 0, rng.getrandbits(32) & ~2)  # без HSERDY (bit1)
    run.ram_write(0xB88, struct.pack('<I', 0))
    r0, _ = run.call(0x10ABC, ())
    assert run.periph_read(RCC + 0) & 1, 'CTLR bit0 (HSEON) должен быть установлен'
    assert run.ram_read(0xB88, 4) == struct.pack('<I', 0x003D0900), \
        f'fallback: {run.ram_read(0xB88, 4).hex()}'
    assert r0 == 0x003D0900, f'return {r0:#x}'


# --- RCC-сеттеры ---

@t(0xC5B0, 'combined setter: CFGR0=(CFGR0&0xF7C0FFFF)|X; +0x40=((+0x40)&~3)|Y')
def _(run, rng):
    a1 = rng.getrandbits(32)
    a2 = rng.getrandbits(32)
    mode = rng.choice([0, 1, 2])
    cfgr0 = rng.getrandbits(32)
    r40 = rng.getrandbits(32)
    run.periph_write(RCC + 4, cfgr0)
    run.periph_write(RCC + 0x40, r40)
    if mode in (0, 1):
        x, y = a1, mode | a2
    else:
        x, y = mode | a1, a2
    run.call(0xC5B0, (mode, a1, a2))
    exp0 = (cfgr0 & 0xF7C0FFFF) | x
    exp40 = (r40 & ~3) | y
    assert run.periph_read(RCC + 4) == (exp0 & M32), f'CFGR0: {run.periph_read(RCC+4):#x} ≠ {exp0:#x}'
    assert run.periph_read(RCC + 0x40) == (exp40 & M32), f'+0x40: {run.periph_read(RCC+0x40):#x} ≠ {exp40:#x}'


@t(0xC540, 'RCC+0x24: clear[6:4], |= r1; mode==0 → clear bit2, mode==4 → set bit2')
def _(run, rng):
    init = rng.getrandbits(32)
    a1 = rng.getrandbits(32)
    mode = rng.choice([0, 1, 4])
    run.periph_write(RCC + 0x24, init)
    run.call(0xC540, (mode, a1))
    exp = ((init & ~0x70) | a1) & M32
    if mode == 0:
        exp &= ~4
    elif mode == 4:
        exp |= 4
    assert run.periph_read(RCC + 0x24) == exp, f'init={init:#x} a1={a1:#x} mode={mode}'


# --- драйвер @0x40003000 (магические записи) ---

@t(0x99F0, 'запись 0xAAAA в @0x40003000')
def _(run, rng):
    run.periph_write(DRV + 0, 0)
    run.call(0x99F0, ())
    assert run.periph_read(DRV + 0) == 0xAAAA


@t(0x99E0, 'запись 0xCCCC в @0x40003000')
def _(run, rng):
    run.periph_write(DRV + 0, 0)
    run.call(0x99E0, ())
    assert run.periph_read(DRV + 0) == 0xCCCC


@t(0x9A0C, 'запись r0 в @0x40003000')
def _(run, rng):
    v = rng.getrandbits(32)
    run.periph_write(DRV + 0, 0)
    run.call(0x9A0C, (v,))
    assert run.periph_read(DRV + 0) == v


@t(0x9A00, 'запись r0 в @0x40003000+4')
def _(run, rng):
    v = rng.getrandbits(32)
    run.periph_write(DRV + 4, 0)
    run.call(0x9A00, (v,))
    assert run.periph_read(DRV + 4) == v


@t(0x99D4, 'запись r0 в @0x40003000+8')
def _(run, rng):
    v = rng.getrandbits(32)
    run.periph_write(DRV + 8, 0)
    run.call(0x99D4, (v,))
    assert run.periph_read(DRV + 8) == v


# --- AFIO + struct ---

@t(0x5970, 'запись r0 в @0x40010414 (AFIO/EXTI-зона)')
def _(run, rng):
    v = rng.getrandbits(32)
    run.periph_write(AFIO_EXTI, 0)
    run.call(0x5970, (v,))
    assert run.periph_read(AFIO_EXTI) == v


@t(0xB854, '*(u32*[r0+0x108]) = 0x10000')
def _(run, rng):
    run.ram_write(0x19570, b'\x00' * 0x110)
    run.call(0xB854, (RAM + 0x19570,))
    assert struct.unpack_from('<I', run.ram_read(0x19570, 0x110), 0x108)[0] == 0x10000


# ===========================================================================
# БАТЧ 4: FLASH unlock/wait, SysTick/NVIC/SCB, busy-delay, AFIO, GPIO, reset
# ===========================================================================

SYS = 0xE0000000        # SYS-регион (NVIC 0xE000E400, SCB 0xE000ED00, SysTick)
AFIO_MAPR = 0x40010004  # AFIO_MAPR (таблица remap)

# --- FLASH unlock / wait-BSY ---

@t(0x6378, 'FLASH unlock: KEYR=0x45670123 → KEYR=0xCDEF89AB')
def _(run, rng):
    run.periph_write(FLASH + 4, 0)
    run.call(0x6378, ())
    assert run.periph_read(FLASH + 4) == 0xCDEF89AB, \
        f'KEYR = {run.periph_read(FLASH+4):#x}'


@t(0x6390, 'wait не-BSY (code!=1); timeout → 0xA')
def _(run, rng):
    # A: SR без bit0 → сразу возвращает code
    sr = rng.getrandbits(32) & ~1
    run.periph_write(FLASH + 0xC, sr)
    r0, _ = run.call(0x6390, (rng.randint(1, 5),))
    assert r0 == ref_flash_sr_code(sr), f'sr={sr:#x} → {r0}'
    # B: SR с bit0 (busy) → N+1 проверок → 0xA
    run.periph_write(FLASH + 0xC, 1 | (rng.getrandbits(32) & ~1))
    n = rng.randint(1, 5)
    r0, _ = run.call(0x6390, (n,))
    assert r0 == 0xA, f'n={n} → {r0:#x}'


# --- I2C/DMA clock: set-then-clear (проверка net-эффекта) ---

# set-then-clear = ВЫНУЖДЕННЫЙ CLEAR бита (x |= m; x &= ~m → бит всегда 0)

@t(0x97F4, 'I2C clock OFF: base==I2C1 → RCC+0x10 &= ~(1<<21); иначе &= ~(1<<22)')
def _(run, rng):
    init = rng.getrandbits(32)
    base = rng.choice([0x40005400, 0x40005800, rng.getrandbits(32)])
    run.periph_write(RCC + 0x10, init)
    run.call(0x97F4, (base,))
    exp = init & ~(1 << 21) if base == 0x40005400 else init & ~(1 << 22)
    got = run.periph_read(RCC + 0x10)
    assert got == (exp & M32), f'base={base:#x}: {init:#x} → {got:#x}, ждали {exp:#x}'


@t(0x17F4, 'DMA clock OFF: base==0x40020800 → RCC+0x28 &= ~0x1000 (base>>18 = бит12); иначе нетто')
def _(run, rng):
    init = rng.getrandbits(32)
    base = rng.choice([0x40020800, rng.getrandbits(32)])
    run.periph_write(RCC + 0x28, init)
    run.call(0x17F4, (base,))
    exp = (init & ~0x1000) if base == 0x40020800 else init
    got = run.periph_read(RCC + 0x28)
    assert got == (exp & M32), f'base={base:#x}: {init:#x} → {got:#x}, ждали {exp:#x}'


@t(0xC644, 'set/clear mask в RCC+0x28 (mode=r1)')
def _(run, rng):
    init = rng.getrandbits(32)
    mask = rng.getrandbits(32)
    mode = rng.getrandbits(1)
    run.periph_write(RCC + 0x28, init)
    run.call(0xC644, (mask, mode))
    exp = (init | mask) if mode else (init & ~mask)
    assert run.periph_read(RCC + 0x28) == (exp & M32)


# --- SysTick / NVIC / SCB ---

@t(0x35EC, 'SysTick_CTRL &= ~2 (TICKINT off)')
def _(run, rng):
    init = rng.getrandbits(32)
    run.periph_write(SYS + 0xE010, init)
    run.call(0x35EC, ())
    assert run.periph_read(SYS + 0xE010) == (init & ~2)


def ref_sign_ext8(v):
    v &= 0xFF
    return v - 0x100 if v & 0x80 else v


# 0x21b84 (подтверждено тресом):
#   p0 = r0&3, shift = p0*8: mask = 0xFF<<shift (байт), value = (r1&3) << (6+shift)
#   r0>=0: addr = 0xE000E400 + (r0&~3)          (NVIC-блок, байт r0>>2)
#   r0<0:  addr = 0xE000ED00 + (s32(r0)&~3) + 0x24  (SCB-блок, байты 0..5 = 0xE000ED00..ED1C)
#   reg[addr] = (v & ~mask) | value
#   (lsrs #0x1b/#0x18 — ЛОГИЧЕСКИЕ трёхоперандные; пул 0x21BC0=0xE000E400, 0x21BC4=0xE000ED00)

@t(0x21B84, 'NVIC/SCB: поле [7:6] байта (r0>>2): r0>=0 → 0xE000E400+(r0&~3); r0<0 → 0xE000ED00+(s32&~3)+0x24;'
            ' reg = (v & ~(0xFF<<(8*(r0&3)))) | ((r1&3) << (6+8*(r0&3)))')
def _(run, rng):
    from unicorn import UC_HOOK_MEM_WRITE
    zone = rng.choice(['NVIC', 'SCB'])
    if zone == 'NVIC':
        r0 = rng.randint(0, 63)
        exp_addr = 0xE000E400 + (r0 & ~3)
    else:
        sb = rng.randint(-28, -1)               # s32; адрес останется в SYS-регионе
        r0 = sb & M32
        # firmware: t = r0&0xF (только младший ниббл! <<28/>>28); off = ((t-8)>>2)*4
        t = r0 & 0xF
        exp_addr = 0xE000ED00 + (((t - 8) >> 2) * 4) + 0x1C
    r1 = rng.getrandbits(32)
    writes = []
    def hw(uc, access, address, size, value, user):
        if address >= SYS:
            writes.append((address, value & M32))
    h = run.uc.hook_add(UC_HOOK_MEM_WRITE, hw)
    init = rng.getrandbits(32)
    run.periph_write(exp_addr, init)
    run.call(0x21B84, (r0, r1))
    run.uc.hook_del(h)
    assert len(writes) == 1, f'writes={writes}, ожидали адрес {exp_addr:#x}'
    waddr, _ = writes[0]
    assert waddr == exp_addr, f'r0={r0:#x} → запись {waddr:#x}, ждали {exp_addr:#x}'
    shift = (r0 & 3) * 8
    mask = (0xFF << shift) & M32
    setv = ((r1 & 3) << (6 + shift)) & M32
    exp_val = (init & ~mask | setv) & M32
    got = run.periph_read(exp_addr)
    assert got == exp_val, f'({init:#x}, r0={r0:#x}, r1={r1:#x}) → {got:#x}, ждали {exp_val:#x}'


# --- busy-delay: проверка порога через hook на CMP ---

@t(0x22A0C, 'busy-delay: порог = 0x1000000 - *(u32@RAM[0x10])*N; CVR |= 0xFFFFFF')
def _(run, rng):
    from unicorn import UC_HOOK_CODE
    coeff = rng.randint(1, 1000)
    n = rng.randint(1, 50)
    iters = rng.randint(1, 5)
    run.ram_write(0x10, struct.pack('<I', coeff))
    run.periph_write(SYS + 0xE018, rng.getrandbits(24))
    captured = {}
    def hc(uc, address, size, user):
        if (address & ~1) == 0x22A2C:   # cmp r4, r2
            captured['thr'] = uc.reg_read(UC_ARM_REG_R2) & M32
    h = run.uc.hook_add(UC_HOOK_CODE, hc)
    run.call(0x22A0C, (n, iters), max_insn=100000)
    run.uc.hook_del(h)
    exp_thr = (0x1000000 - coeff * n) & M32
    assert captured.get('thr') == exp_thr, \
        f'coeff={coeff} N={n}: порог {captured.get("thr"):#x}, ждали {exp_thr:#x}'
    assert run.periph_read(SYS + 0xE018) == 0xFFFFFF, 'CVR должен стать 0xFFFFFF'


@t(0x229D4, 'busy-delay: порог = 0x1000000 - *(u32@RAM[0x24])*N; CVR := 0xFFFFFF')
def _(run, rng):
    from unicorn import UC_HOOK_CODE
    coeff = rng.randint(1, 1000)
    n = rng.randint(1, 50)
    iters = rng.randint(1, 5)
    run.ram_write(0x24, struct.pack('<I', coeff))   # пул 0x2000001C + 8!
    run.periph_write(SYS + 0xE018, rng.getrandbits(32))
    captured = {}
    def hc(uc, address, size, user):
        if (address & ~1) == 0x229F0:   # cmp r3, r2
            captured['thr'] = uc.reg_read(UC_ARM_REG_R2) & M32
    h = run.uc.hook_add(UC_HOOK_CODE, hc)
    run.call(0x229D4, (n, iters), max_insn=100000)
    run.uc.hook_del(h)
    exp_thr = (0x1000000 - coeff * n) & M32
    assert captured.get('thr') == exp_thr, \
        f'coeff={coeff} N={n}: порог {captured.get("thr"):#x}, ждали {exp_thr:#x}'
    assert run.periph_read(SYS + 0xE018) & 0xFFFFFF == 0xFFFFFF


# --- AFIO remap ---

# 0x8588: idx = arg1>>2 (арифм.), pair = arg1&3, shift = pair*4:
#   MAPR[idx] = (MAPR & ~(3<<shift)) | ((val<<shift) & M32)
#   (lsrs r5,r4,#0x1c — ЛОГИЧЕСКИЙ: b1→bit3, b0→bit2 → r5 = pair*4; val не маскируется!)

@t(0x8588, 'AFIO remap: поле [4p+1:4p] = (MAPR & ~(3<<4p)) | val<<4p, p=arg1&3, idx=arg1>>2')
def _(run, rng):
    val = rng.getrandbits(8)
    arg1_s = rng.randint(-127, 63) if rng.getrandbits(1) else rng.randint(0, 63)
    idx = arg1_s >> 2
    pair = arg1_s & 3
    shift = pair * 4
    addr = AFIO_MAPR + idx * 4
    init = rng.getrandbits(32)
    run.periph_write(addr, init)
    run.call(0x8588, (val, arg1_s & M32))
    exp = (init & ~(3 << shift)) | ((val << shift) & M32)
    got = run.periph_read(addr)
    assert got == (exp & M32), f'idx={idx} pair={pair} val={val:#x} arg1={arg1_s}: {got:#x} ≠ {exp:#x}'


# --- номер порта по GPIO-базе (PC-трассировка) ---

@t(0x2BBC, 'порт по GPIO-базе: A=0,B=1,C=2,D=3 (проверка точки детекции)')
def _(run, rng):
    from unicorn import UC_HOOK_CODE
    cases = [(0x40010800, 0x2BCC), (0x40010C00, 0x2BD6),
             (0x40011000, 0x2BE0), (0x40011400, 0x2BEA)]
    base, expect_pc = cases[rng.randint(0, 3)]
    hits = []
    def hc(uc, address, size, user):
        a = address & ~1
        if a in (0x2BCC, 0x2BD6, 0x2BE0, 0x2BEA, 0x2BEE):
            hits.append(a)
    h = run.uc.hook_add(UC_HOOK_CODE, hc)
    # mode=0x100 — длинный путь; dispatch завершается общим return через 0x2BEE
    run.call(0x2BBC, (base, 0x100, 0), max_insn=20000)
    run.uc.hook_del(h)
    assert expect_pc in hits, \
        f'base={base:#x}: детекция {expect_pc:#x} не найдена, hits={[hex(h) for h in hits]}'


# --- программный сброс (бюджетный вызов: функция зацикливается) ---

@t(0x1E3A4, 'soft reset: [0x40021400] &= ~0xC; &= ~0x1F0; |= 1; AIRCR=0x5FA0004; b .')
def _(run, rng):
    init = rng.getrandbits(32)
    run.periph_write(0x40021400, init)
    run.periph_write(0xE000ED0C, 0)
    run.call(0x1E3A4, (), max_insn=500)   # остановится в цикле b .
    exp_rcc = ((init & ~0xC) & ~0x1F0) | 1
    got = run.periph_read(0x40021400)
    assert got == (exp_rcc & M32), f'{init:#x} → {got:#x}, ждали {exp_rcc:#x}'
    assert run.periph_read(0xE000ED0C) == 0x5FA0004, \
        f'AIRCR = {run.periph_read(0xE000ED0C):#x}'


# ===========================================================================
# Батч 5 (§51): полка 132–256 B
# ===========================================================================

# --- MSB-normalization shift (gap-функция, артефакт детектора) ---
# трассировка: шаги 16/8/4/2 бита; финал: r0∈{1,2} → r1−r0; x=1<<p → 0x1F−p

@t(0x21B24, 'MSB-normalization: x==0 → 0x20; иначе 0x1F − msb_pos(x)')
def _(run, rng):
    for _ in range(30):
        if rng.getrandbits(2) == 0:
            x = rng.choice([0, 1, 2, 3, 0x8000, 0x80000000, 0xFFFFFFFF])
        else:
            x = rng.getrandbits(32)
        r0, _ = run.call(0x21B24, (x,))
        exp = 0x20 if x == 0 else 0x1F - (x.bit_length() - 1)
        assert r0 == exp, f'x={x:#x}: {r0:#x} ≠ {exp:#x}'


# --- i16 × i16 → u32 (запись в *out_lo/*out_hi) ---

@t(0x17170, 'i16×i16→u64 (sign-extended): *out_hi = 0/0xFFFFFFFF, *out_lo = a*b')
def _(run, rng):
    a = rng.randint(-32768, 32767)
    b = rng.randint(-32768, 32767)
    run.ram_write(0x100, struct.pack('<II', 0xDEAD, 0xBEEF))
    run.call(0x17170, (a & M32, b & M32, RAM + 0x100, RAM + 0x104))
    hi, lo = struct.unpack('<II', run.ram_read(0x100, 8))
    p = a * b
    exp_lo, exp_hi = p & M32, (0xFFFFFFFF if p < 0 else 0)
    assert lo == exp_lo and hi == exp_hi, f'{a}×{b}: {hi:#x}:{lo:#x} ≠ {exp_hi:#x}:{exp_lo:#x}'


@t(0x17214, 'i16×i16→u64 #2 (twin 0x17170)')
def _(run, rng):
    a = rng.randint(-32768, 32767)
    b = rng.randint(-32768, 32767)
    run.ram_write(0x100, struct.pack('<II', 0xDEAD, 0xBEEF))
    run.call(0x17214, (a & M32, b & M32, RAM + 0x100, RAM + 0x104))
    hi, lo = struct.unpack('<II', run.ram_read(0x100, 8))
    p = a * b
    exp_lo, exp_hi = p & M32, (0xFFFFFFFF if p < 0 else 0)
    assert lo == exp_lo and hi == exp_hi, f'{a}×{b}: {hi:#x}:{lo:#x} ≠ {exp_hi:#x}:{exp_lo:#x}'


# --- u16-массив: статистика + in-place clamp ---

@t(0x5134, 'u16 статистика: s16≤0 → 300 (in-place); out={sum,avg,min,max,idx_min,idx_max} (1-based)')
def _(run, rng):
    n = rng.randint(1, 24)
    vals = []
    for _ in range(n):
        k = rng.getrandbits(2)
        if k == 0:
            vals.append(rng.getrandbits(16))
        elif k == 1:
            vals.append(0)
        else:
            vals.append(0x8000 + rng.getrandbits(15))   # s16 < 0
    run.ram_write(0x200, struct.pack(f'<{n}H', *vals))
    run.ram_write(0x300, b'\x00' * 16)
    run.call(0x5134, (RAM + 0x200, n, RAM + 0x300), max_insn=20000)
    cl = []
    for v in vals:
        s = v - 65536 if v >= 0x8000 else v
        cl.append(300 if s <= 0 else v)
    got_arr = struct.unpack(f'<{n}H', run.ram_read(0x200, 2 * n))
    assert list(got_arr) == cl, f'in-place clamp: {got_arr} ≠ {cl}'
    total = sum(cl) & M32
    avg = (total // n) & 0xFFFF
    mn, mx = min(cl), max(cl)
    idx_min = cl.index(mn) + 1          # первое вхождение (обновление строго <)
    idx_max = cl.index(mx) + 1          # первое вхождение (обновление строго >: равные не обновляют)
    out = struct.unpack('<IHHHBB', run.ram_read(0x300, 12))
    assert out[0] == total, f'sum: {out[0]:#x} ≠ {total:#x}'
    assert out[1] == avg, f'avg: {out[1]} ≠ {avg}'
    assert out[2] == mn and out[3] == mx, f'min/max: {out[2]}/{out[3]} ≠ {mn}/{mx}'
    assert out[4] == idx_min and out[5] == idx_max, \
        f'idx: {out[4]}/{out[5]} ≠ {idx_min}/{idx_max}'


# --- интерполяция Q31 (u32 y-таблица, доп. слот) ---

@t(0x16880, 'Q31-интерполяция: args (v, xtab_u16, ytab_u32, last_idx=n−1); slope=((v−x0)<<16)/dx через 0x161ea(…,15); y=y0+(y1−y0)*slope>>31; v≥xs[last] → mid-экстраполяция с последнего сегмента')
def _(run, rng):
    n = rng.randint(2, 8)
    xs = sorted(rng.sample(range(-400, 400), n))
    ys = [rng.getrandbits(32) for _ in range(n)]     # без доп. слота
    base = 0x400
    case = rng.getrandbits(2)
    if case == 0:
        value = xs[0] - rng.randint(0, 50)          # до начала: r4=0, slope=0
        exp = ys[0]
    elif case == 1:
        value = xs[-1] + rng.randint(0, 50)         # за конец: sentinel=Q31 1.0 → полный шаг к ys[n−1]
        exp = ys[n - 1]
    elif case == 2:
        k = rng.randint(0, n - 2)
        while (xs[k + 1] - xs[k]) % 2:               # чётный dx → точная середина
            xs = sorted(rng.sample(range(-400, 400), n))
            k = rng.randint(0, n - 2)
        value = (xs[k] + xs[k + 1]) // 2             # slope = 0x40000000 точный
        exp = ref_seg_interp(ys[k], ys[k + 1], 0x40000000)
    else:
        k = rng.randint(0, n - 2)
        value = xs[k]                                # точно на узле: slope=0
        exp = ys[k]
    run.ram_write(base, struct.pack(f'<{n}h', *xs))
    run.ram_write(base + 0x100, struct.pack(f'<{n}I', *ys))
    r0, _ = run.call(0x16880, (value & M32, RAM + base,
                               RAM + base + 0x100, n - 1), max_insn=5000)
    assert r0 == exp, f'case={case} v={value}: {r0:#x} ≠ {exp:#x}'


# --- интерполяция Q8 (u8 y-таблица, доп. слот) ---

@t(0x167B6, 'Q8-интерполяция: args (v, xtab_u16, ytab_u8, last_idx=n−1); slope=((v−x0)<<8)/dx (udiv); y=(y0 ± dy*slope>>8)&0xFF; v≥xs[last] → slope=1.0 с последнего сегмента')
def _(run, rng):
    n = rng.randint(2, 8)
    xs = sorted(rng.sample(range(-400, 400), n))
    ys = [rng.getrandbits(8) for _ in range(n)]      # без доп. слота
    base = 0x600
    case = rng.getrandbits(2)
    if case == 0:
        value = xs[0] - rng.randint(0, 50)
        exp = ys[0]
    elif case == 1:
        value = xs[-1] + rng.randint(0, 50)         # r1=n−2, slope = 0x100 (1.0) → полный шаг к ys[n−1]
        exp = ys[n - 1]
    elif case == 2:
        k = rng.randint(0, n - 2)
        while (xs[k + 1] - xs[k]) % 2:
            xs = sorted(rng.sample(range(-400, 400), n))
            k = rng.randint(0, n - 2)
        value = (xs[k] + xs[k + 1]) // 2             # slope = 128 точный
        dy = (ys[k + 1] - ys[k]) & 0xFF if ys[k + 1] >= ys[k] else (ys[k] - ys[k + 1]) & 0xFF
        exp = (ys[k] + dy // 2) & 0xFF if ys[k + 1] >= ys[k] else (ys[k] - dy // 2) & 0xFF
    else:
        k = rng.randint(0, n - 2)
        value = xs[k]
        exp = ys[k]
    run.ram_write(base, struct.pack(f'<{n}h', *xs))
    run.ram_write(base + 0x100, bytes(ys))
    r0, _ = run.call(0x167B6, (value & M32, RAM + base,
                               RAM + base + 0x100, n - 1), max_insn=5000)
    assert r0 == exp, f'case={case} v={value}: {r0:#x} ≠ {exp:#x}'


@t(0x16938, 'Q31-интерполяция #2: twin 0x16880, но ветка по UNSIGNED cmp (bhi)')
def _(run, rng):
    n = rng.randint(2, 8)
    xs = sorted(rng.sample(range(-400, 400), n))
    # y: иногда с битом31 (разница signed/unsigned веток)
    ys = [rng.getrandbits(32) if rng.getrandbits(2) else
          (0x80000000 + rng.getrandbits(31)) for _ in range(n)]
    base = 0x500
    case = rng.getrandbits(2)
    if case == 0:
        value = xs[0] - rng.randint(0, 50)
        exp = ys[0]
    elif case == 1:
        value = xs[-1] + rng.randint(0, 50)         # полный шаг к ys[n−1]
        exp = ys[n - 1]
    elif case == 2:
        k = rng.randint(0, n - 2)
        while (xs[k + 1] - xs[k]) % 2:
            xs = sorted(rng.sample(range(-400, 400), n))
            k = rng.randint(0, n - 2)
        value = (xs[k] + xs[k + 1]) // 2
        exp = ref_seg_interp_unsigned(ys[k], ys[k + 1], 0x40000000)
    else:
        k = rng.randint(0, n - 2)
        value = xs[k]
        exp = ys[k]
    run.ram_write(base, struct.pack(f'<{n}h', *xs))
    run.ram_write(base + 0x100, struct.pack(f'<{n}I', *ys))
    r0, _ = run.call(0x16938, (value & M32, RAM + base,
                               RAM + base + 0x100, n - 1), max_insn=5000)
    assert r0 == exp, f'case={case} v={value}: {r0:#x} ≠ {exp:#x}'


@t(0x16BD4, '2D-билинейная интерполяция u16: (v1, v2, xtab1_u16, ystruct_u32, [STK]ygrid, [STK]{c1,c2}, [STK]stride)')
def _(run, rng):
    n1 = rng.randint(2, 6)
    n2 = rng.randint(2, 5)
    xtab1 = sorted(rng.sample(range(-300, 300), n1))
    ystruct = sorted(rng.getrandbits(31) for _ in range(n2))   # u32, без бит31
    stride = rng.randint(4, 8)
    grid = [rng.getrandbits(16) for _ in range((n2 + 1) * stride + 1)]
    base = 0x700
    run.ram_write(base, struct.pack(f'<{n1}h', *xtab1))          # xtab1
    yst = base + 0x80
    run.ram_write(yst, struct.pack(f'<{n2}I', *ystruct))         # ystruct (flat)
    hdr = base + 0x180
    run.ram_write(hdr, struct.pack('<II', n1 - 1, n2 - 1))       # {count1, count2}
    grd = base + 0x200
    run.ram_write(grd, struct.pack(f'<{len(grid)}H', *grid))     # ygrid
    # caller-стек: SP call = STACK_TOP − 0x200; слоты [SP+0]=ygrid, +4=hdr, +8=stride
    csp = STACK_TOP - 0x200
    run.ram_write(csp - RAM, struct.pack('<3I',
                   RAM + grd, RAM + hdr, stride))
    case = rng.getrandbits(2)
    if case == 0:
        v1 = xtab1[rng.randint(0, n1 - 1)]
        v2 = ystruct[rng.randint(0, n2 - 1)]
    else:
        k1 = rng.randint(0, n1 - 2)
        while (xtab1[k1 + 1] - xtab1[k1]) % 2:
            xtab1 = sorted(rng.sample(range(-300, 300), n1))
            k1 = rng.randint(0, n1 - 2)
            run.ram_write(base, struct.pack(f'<{n1}h', *xtab1))
        v1 = (xtab1[k1] + xtab1[k1 + 1]) // 2
        k2 = rng.randint(0, n2 - 2)
        while (ystruct[k2 + 1] - ystruct[k2]) % 2:
            ystruct = sorted(rng.getrandbits(31) for _ in range(n2))
            k2 = rng.randint(0, n2 - 2)
            run.ram_write(yst, struct.pack(f'<{n2}I', *ystruct))
        v2 = (ystruct[k2] + ystruct[k2 + 1]) // 2
    # референс
    def seg(u16_a, u16_b, slope):
        if u16_a > u16_b:                       # unsigned bgt → descending
            return (u16_a - (((u16_a - u16_b) * slope) >> 16)) & 0xFFFF
        return (u16_a + (((u16_b - u16_a) * slope) >> 16)) & 0xFFFF
    if v1 <= xtab1[0]:
        idx1, s1 = 0, 0
    elif v1 >= xtab1[n1 - 1]:
        idx1, s1 = n1 - 2, 0x10000
    else:
        idx1 = max(i for i in range(n1) if xtab1[i] <= v1)
        dx = (xtab1[idx1 + 1] - xtab1[idx1]) & 0xFFFF
        s1 = (((v1 - xtab1[idx1]) << 16) // dx) & M32
    if v2 <= ystruct[0]:
        idx2, s2 = 0, 0
    elif v2 >= ystruct[n2 - 1]:
        idx2, s2 = n2 - 2, 0x10000
    else:
        idx2 = max(i for i in range(n2) if ystruct[i] <= v2)
        s2 = ref_161ea((v2 - ystruct[idx2]) & M32,
                       (ystruct[idx2 + 1] - ystruct[idx2]) & M32, 16)
    # примечание: s2 — unsigned udiv-результат (0x161ea с положительными аргументами)
    iA = idx2 * stride + idx1
    yA = seg(grid[iA], grid[iA + 1], s1)
    yB = seg(grid[iA + stride], grid[iA + stride + 1], s1)
    if yB >= yA:
        exp = (yA + (((yB - yA) * s2) >> 16)) & 0xFFFF
    else:
        exp = (yA - (((yA - yB) * s2) >> 16)) & 0xFFFF
    # ручной call (Run.call ставит SP=STACK_TOP — не хватает места на caller-слоты)
    uc = run.uc
    from unicorn import UC_HOOK_CODE, UcError
    from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                                   UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_LR)
    uc.reg_write(UC_ARM_REG_R0, v1 & M32)
    uc.reg_write(UC_ARM_REG_R1, v2 & M32)
    uc.reg_write(UC_ARM_REG_R2, RAM + base)
    uc.reg_write(UC_ARM_REG_R3, RAM + yst)
    uc.reg_write(UC_ARM_REG_SP, csp)
    uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    run.emu.insn = 0
    stop_h = uc.hook_add(UC_HOOK_CODE, lambda u, a, s, usr: u.emu_stop()
                         if not (FLASH0 <= a < FLASH0 + FW_LEN or
                                 FLASH1 <= a < FLASH1 + FW_LEN) else None)
    try:
        uc.emu_start(0x16BD4 | 1, 0, count=5000)
    except UcError:
        pass
    uc.hook_del(stop_h)
    r0 = uc.reg_read(UC_ARM_REG_R0) & M32
    assert r0 == exp, f'case={case} v1={v1} v2={v2}: {r0:#x} ≠ {exp:#x}'


def _interp16(a, b, slope):
    """один шаг интерполяции 0x16588/0x16bd4: unsigned cmp, Q16-наклон, u16"""
    if a > b:
        d = (a - b) & 0xFFFF
        return (a - ((d * slope) >> 16)) & 0xFFFF
    d = (b - a) & 0xFFFF
    return (a + ((d * slope) >> 16)) & 0xFFFF


def ref_16588(ix, iy, iz, sx, sy, sz, grid, syy, szz):
    """3D-трилинейная интерполяция на плоской u16-сетке (§52.1 эмуляторно).
    base = ix + syy*iy + szz*iz; x-шаг — соседний элемент (stride 1)."""
    b = ix + syy * iy + szz * iz
    a0 = _interp16(grid[b], grid[b + 1], sx)
    a1 = _interp16(grid[b + syy], grid[b + syy + 1], sx)
    c0 = _interp16(a0, a1, sy)
    b2 = b + szz
    d0 = _interp16(grid[b2], grid[b2 + 1], sx)
    d1 = _interp16(grid[b2 + syy], grid[b2 + syy + 1], sx)
    e0 = _interp16(d0, d1, sy)
    return _interp16(c0, e0, sz)


@t(0x16588, '3D-трилинейная интерполяция u16: (idx{3}, slope{3}Q16, grid_u16, stride{3})')
def _(run, rng):
    nx, ny, nz = rng.randint(2, 4), rng.randint(2, 3), rng.randint(2, 3)
    syy, szz = rng.randint(1, nx + 1), rng.randint(ny, ny * nx + 1)
    ix, iy, iz = (rng.randint(0, n - 1) for n in (nx, ny, nz))
    sx, sy, sz = (rng.getrandbits(16) for _ in range(3))
    size = (nx - 1) + syy * (ny - 1) + szz * nz + syy + 2
    grid = [rng.getrandbits(16) for _ in range(size)]
    base = 0x700
    run.ram_write(base, struct.pack('<3I', ix, iy, iz))
    run.ram_write(base + 0x40, struct.pack('<3I', sx, sy, sz))
    gbase = base + 0x80
    run.ram_write(gbase, struct.pack(f'<{len(grid)}H', *grid))
    stride_p = base + 0x400   # НЕ в gbase — иначе перетрёт начало сетки!
    run.ram_write(stride_p, struct.pack('<3I', 1, syy, szz))
    r0, _ = run.call(0x16588, (RAM + base, RAM + base + 0x40,
                               RAM + gbase, RAM + stride_p), max_insn=20000)
    exp = ref_16588(ix, iy, iz, sx, sy, sz, grid, syy, szz)
    assert r0 == exp, f'ix={ix} iy={iy} iz={iz}: {r0:#x} ≠ {exp:#x}'


# --- duty/throttle shaping (чистый RAM) ---

@t(0x1D330, 'duty shaping: v>580→flags|=2,st=0; v<196→flags|=4,st=0; [196,400): st=max(0,st−100), 0→flags|=4; >431: flags&=~4, st=min(0x7FF8,st+1000); clamp; byte[RAM+0x3C8+0x10]=4')
def _(run, rng):
    v = rng.randint(-32768, 32767)
    flags = rng.getrandbits(16)
    state = rng.randint(-500, 32767)
    run.ram_write(0x1794 + 0xC, struct.pack('<h', v))
    run.ram_write(0x220, struct.pack('<H', flags))
    run.ram_write(0x1794 + 0xA, struct.pack('<h', state))
    run.ram_write(0x3C8 + 0x10, b'\x00')
    run.call(0x1D330, (), max_insn=5000)
    f2 = struct.unpack('<H', run.ram_read(0x220, 2))[0]
    st = struct.unpack('<h', run.ram_read(0x1794 + 0xA, 2))[0]
    # референс (внимание: все сравнения v — UNSIGNED u16!)
    vu = v & 0xFFFF
    if vu > 580:
        f2e, ste = flags | 2, 0
    else:
        f2e = flags & ~2
        if vu < 196:
            f2e, ste = f2e | 4, 0
        else:
            ste = state
            if vu < 400:
                ste = max(0, ste - 100)
                if ste == 0:
                    f2e |= 4
            if vu > 431:
                f2e &= ~4
                ste = min(0x7FF8, ste + 1000)
    ste = max(0, min(0x7FF8, ste))
    assert f2 == (f2e & 0xFFFF), f'v={v} flags={flags:#x}: {f2:#x} ≠ {f2e:#x}'
    assert st == ste, f'v={v} state={state}: {st} ≠ {ste}'
    assert run.ram_read(0x3C8 + 0x10, 1)[0] == 4


# --- drift detector (адаптивный базлайн) ---

@t(0xE740, 'drift detector: devA=|u16[RAM+0x13AB]−u16[RAM+0x130A]|; devB=clamp(s16[RAM+0x13A4]−s16[RAM+0x1302],±0x8000); devA≥500||devB>500 → flag + refs:=текущие')
def _(run, rng):
    A = rng.getrandbits(16)
    B = rng.randint(-32768, 32767)
    refA = rng.getrandbits(16)
    refB = rng.randint(-32768, 32767)
    run.ram_write(0x13AB, struct.pack('<H', A))
    run.ram_write(0x13A4, struct.pack('<h', B))
    run.ram_write(0x130A, struct.pack('<H', refA))
    run.ram_write(0x1302, struct.pack('<h', refB))
    run.ram_write(0x500, b'\x7F')
    run.call(0xE740, (RAM + 0x500,), max_insn=5000)
    devA = abs(A - refA)
    devB = B - refB
    devB = max(-0x8000, min(0x7FFF, devB))
    flag = 1 if (devA >= 500 or devB > 500) else 0
    got = run.ram_read(0x500, 1)[0]
    assert got == flag, f'A={A} refA={refA} B={B} refB={refB}: flag {got} ≠ {flag}'
    gA = struct.unpack('<H', run.ram_read(0x130A, 2))[0]
    gB = struct.unpack('<h', run.ram_read(0x1302, 2))[0]
    if flag:
        assert gA == A and gB == B, f'refs не обновлены: {gA}/{gB} ≠ {A}/{B}'
    else:
        assert gA == refA and gB == refB, 'refs должны остаться нетронутыми'


# --- PB15 latch с гистерезисом (flash-калибровка @0x19E1C) ---
# 0xfdac: lo=i8@+0=1, N=u16@+1=5264, hi=i8@+3=70, M=u16@+4=17936
#         gate: mode@RAM[0x80]==0 && !bit0[RAM+0xFC7+6]; v=i8[RAM+0xFC7+2]
#         ON:  v≥lo && (cnt++≤N) → ODR|=0x8000, bit0=1, cnt=0
#         OFF: bit0 && v≤hi && (cnt2++>M) → BRR|=0x8000, bit0=0, cnt2=0
# 0xfe74: то же с bit1, v=i8[RAM+0xFC7+1], пороги @+6..+0xA (lo=5,N=224,hi=32,M=17921)

@t(0xFDAC, 'PB15 latch #1: gate mode==0&&!bit0[RAM+0xFC7+6]; v=i8[RAM+0xFC7+2]; flash @0x19E1C {lo=1,N=5264,hi=70,M=17936}')
def _(run, rng):
    mode = rng.getrandbits(2)
    bit0 = rng.getrandbits(1)
    v = rng.randint(-128, 127)
    cnt = rng.choice([0, 1, 5263, 17936])
    cnt2 = rng.choice([0, 1, 17936])
    run.ram_write(0x80, struct.pack('<B', mode))
    run.ram_write(0xFC7 + 6, struct.pack('<B', bit0))
    run.ram_write(0xFC7 + 2, struct.pack('<b', v))
    run.ram_write(0x9F4, struct.pack('<H', cnt))
    run.ram_write(0x9F6, struct.pack('<H', cnt2))
    run.periph_write(0x40010C18, rng.getrandbits(32) & ~0x8000)
    run.periph_write(0x40010C28, 0)
    run.call(0xFDAC, (), max_insn=5000)
    # часть 1 (ON): mode==0 && !bit0 && v≥lo(1) && cnt++≤N(5264) → ODR|=
    # часть 2 (OFF): bit0 (любой mode) && v≤hi(70) && cnt2++≤M(17936) → BRR|
    exp_odr = 0x8000 if (mode == 0 and not bit0 and v >= 1 and cnt + 1 >= 5264) else 0   # cmp N,cnt; bgt=skip → ON при cnt_new≥N
    exp_brr = 0x8000 if (bit0 and v <= 70 and cnt2 + 1 >= 17936) else 0   # cmp M,cnt; bgt=skip → OFF при cnt_new≥M
    got_odr = run.periph_read(0x40010C18) & 0x8000
    got_brr = run.periph_read(0x40010C28) & 0x8000
    assert got_odr == exp_odr, f'mode={mode} bit0={bit0} v={v}: ODR {got_odr:#x} ≠ {exp_odr:#x}'
    assert got_brr == exp_brr, f'cnt2={cnt2} v={v}: BRR {got_brr:#x} ≠ {exp_brr:#x}'
    gbit = run.ram_read(0xFC7 + 6, 1)[0] & 1
    gc = struct.unpack('<H', run.ram_read(0x9F4, 2))[0]
    if mode == 0 and not bit0:
        on = (v >= 1 and cnt + 1 >= 5264)
        exp_bit, exp_cnt = (1, 0) if on else (0, (cnt + 1 if v >= 1 else 0))
    else:
        # часть 2 может снять bit0 (OFF при v≤70 && cnt2_new≥M)
        off = (bit0 and v <= 70 and cnt2 + 1 >= 17936)
        exp_bit, exp_cnt = (0 if off else bit0), cnt
    assert gbit == exp_bit and gc == exp_cnt, \
        f'bit {gbit}≠{exp_bit}, cnt {gc}≠{exp_cnt}'


@t(0xFE74, 'PB15 latch #2: gate mode==0&&!bit1[RAM+0xFC7+6]; v=i8[RAM+0xFC7+1]; flash @0x19E1C+6 {lo=5,N=224,hi=32,M=17921}')
def _(run, rng):
    mode = rng.getrandbits(2)
    bit1 = rng.getrandbits(1)
    v = rng.randint(-128, 127)
    cnt = rng.choice([0, 1, 223])
    cnt2 = rng.choice([0, 1, 17921])
    run.ram_write(0x80, struct.pack('<B', mode))
    run.ram_write(0xFC7 + 6, struct.pack('<B', bit1 << 1))
    run.ram_write(0xFC7 + 1, struct.pack('<b', v))
    run.ram_write(0x9F0, struct.pack('<H', cnt))
    run.ram_write(0x9F2, struct.pack('<H', cnt2))
    run.periph_write(0x40010C18, rng.getrandbits(32) & ~0x8000)
    run.periph_write(0x40010C28, 0)
    run.call(0xFE74, (), max_insn=5000)
    # часть 1 (ON): mode==0 && !bit1 && v≤lo(5) && cnt++≤N(224) → ODR|
    # часть 2 (OFF): bit1 (любой mode) && v≥hi(32) && cnt2++≤M(17921) → BRR|
    exp_odr = 0x8000 if (mode == 0 and not bit1 and v <= 5 and cnt + 1 >= 224) else 0   # cmp N,cnt; bgt=skip → ON при cnt_new≥N
    exp_brr = 0x8000 if (bit1 and v >= 32 and cnt2 + 1 >= 17921) else 0   # cmp M,cnt; bgt=skip → OFF при cnt_new≥M
    got_odr = run.periph_read(0x40010C18) & 0x8000
    got_brr = run.periph_read(0x40010C28) & 0x8000
    assert got_odr == exp_odr, f'mode={mode} bit1={bit1} v={v}: ODR {got_odr:#x} ≠ {exp_odr:#x}'
    assert got_brr == exp_brr, f'cnt2={cnt2} v={v}: BRR {got_brr:#x} ≠ {exp_brr:#x}'
    gbit = (run.ram_read(0xFC7 + 6, 1)[0] >> 1) & 1
    gc = struct.unpack('<H', run.ram_read(0x9F0, 2))[0]
    if mode == 0 and not bit1:
        on = (v <= 5 and cnt + 1 >= 224)      # v≤lo! и debounce N=224
        exp_bit, exp_cnt = (1, 0) if on else (0, (cnt + 1 if v <= 5 else 0))
    else:
        # часть 2 может снять bit1 (OFF при v≥32 && cnt2_new≥M)
        off = (bit1 and v >= 32 and cnt2 + 1 >= 17921)
        exp_bit, exp_cnt = (0 if off else bit1), cnt
    assert gbit == exp_bit and gc == exp_cnt, \
        f'bit {gbit}≠{exp_bit}, cnt {gc}≠{exp_cnt}'


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', help='только функции с этим префиксом адреса (0x126c)')
    ap.add_argument('--seed', type=int, default=42)
    ap.add_argument('--iters', type=int, default=30, help='итераций на тест')
    ap.add_argument('--list', action='store_true', help='показать покрытые функции')
    a = ap.parse_args()

    only = int(a.only, 16) if a.only else None
    sel = [(o, d, f) for o, d, f in TESTS if only is None or o == only]

    if a.list:
        # покрытие каталога
        import gen_maps
        cat = {s for s, _, _, st in gen_maps.ANALYZED_MCU if st == 'разобран'}
        tested = {o for o, _, _ in TESTS}
        print(f'тестов: {len(TESTS)}; каталог «разобран»: {len(cat)}')
        print(f'покрыто эмуляцией: {len(tested & cat)}/{len(cat)} '
              f'({100.0 * len(tested & cat) / max(1, len(cat)):.1f}%)')
        print('список тестов:')
        for o, d, _ in TESTS:
            mark = '✓' if o in cat else '?'
            print(f'  {mark} {o:#06x}  {d}')
        return

    rng = random.Random(a.seed)
    run = Run()
    passed, failed = [], []
    for off, desc, fn in sel:
        ok, err = True, ''
        for i in range(a.iters):
            try:
                fn(run, rng)
            except AssertionError as e:
                ok, err = False, str(e)[:200]
                break
            except Exception as e:
                ok, err = False, f'{type(e).__name__}: {e}'[:200]
                break
        (passed if ok else failed).append((off, desc))
        print(f'  {"PASS" if ok else "FAIL"} {off:#06x}  {desc}'
              + ('' if ok else f'\n         {err}'))

    print(f'\nитого: PASS {len(passed)} / FAIL {len(failed)} из {len(sel)}')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
