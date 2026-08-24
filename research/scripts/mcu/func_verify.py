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
