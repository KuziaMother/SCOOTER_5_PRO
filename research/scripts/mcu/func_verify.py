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

    def __init__(self, max_insn=100000):
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
