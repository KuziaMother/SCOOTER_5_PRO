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

from unicorn import UcError, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                               UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5,
                               UC_ARM_REG_R6, UC_ARM_REG_SP, UC_ARM_REG_LR,
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
        # §57: последняя ошибка исполнения (None = чистый возврат).
        # ВАЖНО: call() раньше молча глотал UcError — fault выглядел как
        # «чистый возврат» со мусором в r0 (ловушка для верификации).
        self.last_error = None

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
        self.last_error = None
        try:
            uc.emu_start(off | 1, 0, count=max_insn)
        except UcError as e:
            self.last_error = str(e)[:80]
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


@t(0x19968, 'u32/u32 floor-деление (restore, 32 ит.): (num=r0, den=r1) → r0=num//den')
def _(run, rng):
    # фиксированные краевые
    for n, d in [(10, 2), (5, 2), (7, 3), (0xFFFFFFFF, 2), (0xFFFFFFFF, 3), (1, 1), (0x12345678, 0x100)]:
        r0, _ = run.call(0x19968, [n, d])
        assert r0 == n // d, f'{n:#x}/{d}: {r0:#x} ≠ {n // d:#x}'
    # случайные (den ≥ 1)
    for _ in range(40):
        n = rng.getrandbits(32)
        d = rng.getrandbits(24) + 1
        r0, _ = run.call(0x19968, [n, d])
        assert r0 == n // d, f'{n:#x}/{d:#x}: {r0:#x} ≠ {n // d:#x}'


@t(0x19994, 'signed-деление C-style (truncation toward zero): (a=r0, b=r1) → r0')
def _(run, rng):
    for a, b in [(10, 2), (-10, 2), (10, -2), (-10, -2), (-7, 3), (7, -3), (-1, 2), (-1 << 31, -3)]:
        a32 = a if a > -(1 << 31) else a  # уже в i32
        r0, _ = run.call(0x19994, [a & 0xFFFFFFFF, b & 0xFFFFFFFF])
        got = r0 if r0 < (1 << 31) else r0 - (1 << 32)
        exp = abs(a32) // abs(b) * (-1 if (a32 < 0) != (b < 0) else 1)
        assert got == exp, f'{a}/{b}: {got} ≠ {exp}'
    for _ in range(25):
        a = rng.randint(-(1 << 30), (1 << 30))
        b = rng.choice([-1, 1]) * (rng.getrandbits(20) + 1)
        r0, _ = run.call(0x19994, [a & 0xFFFFFFFF, b & 0xFFFFFFFF])
        got = r0 if r0 < (1 << 31) else r0 - (1 << 32)
        exp = abs(a) // abs(b) * (-1 if (a < 0) != (b < 0) else 1)
        assert got == exp, f'{a}/{b}: {got} ≠ {exp}'


@t(0x199BC, 'u64/u64 → u64 unsigned-деление (64 ит., 0x1a080/0x1a0a0): (num_lo, num_hi, den_lo, den_hi) → r1:r0')
def _(run, rng):
    # ВАЖНО: 4 аргумента — den_hi обязателен (иначе мусор в R3 из прошлого вызова)
    for nlo, nhi, dlo, dhi in [(1000, 0, 3, 0), (0xFFFFFFFF, 1, 2, 0), (5, 0, 2, 0), (0, 1, 7, 0)]:
        r0, r1 = run.call(0x199BC, [nlo, nhi, dlo, dhi], max_insn=300000)
        num = (nhi << 32) | nlo
        den = (dhi << 32) | dlo
        q = num // den
        assert (r1, r0) == ((q >> 32) & 0xFFFFFFFF, q & 0xFFFFFFFF), \
            f'{num:#x}/{den}: {r1:#x}:{r0:#x} ≠ {q:#x}'
    for _ in range(5):
        num = rng.getrandbits(64)
        den = rng.getrandbits(28) + 1
        r0, r1 = run.call(0x199BC, [num & 0xFFFFFFFF, num >> 32,
                                     den & 0xFFFFFFFF, den >> 32], max_insn=300000)
        q = num // den
        assert (r1, r0) == ((q >> 32) & 0xFFFFFFFF, q & 0xFFFFFFFF), \
            f'{num:#x}/{den}: {r1:#x}:{r0:#x} ≠ {q:#x}'


# --- батч 9 (§56): window-gate 0xF010/0xF024 (motor, caller 0x7494) ----------
# Чистые функции: (a=r0, b=r1, out_u16_ptr=r2) → strh result,[r2], bx lr.
# Сравнения БЕСЗНАКОВЫЕ (cmp). Истинные таблицы:
#   0xF010: a≥b → a;  b<a+8 → b;  иначе → a
#   0xF024: a≤b → a;  a<b+8 → b;  иначе → a
_OUT = 0x100  # RAM-относительный слот вывода


def _gate(run, off, a, b):
    run.ram_write(_OUT, struct.pack('<H', 0))
    run.call(off, [a & M32, b & M32, RAM + _OUT])
    return struct.unpack('<H', run.ram_read(_OUT, 2))[0]


@t(0xF010, 'window-gate «up» (motor 0x7494): a≥b→a; b<a+8→b; иначе→a (u32-cmp)')
def _(run, rng):
    for a in (0, 1, 7, 8, 15, 300, 2550, 0xFFFF):
        for b in range(0, 24):
            exp = a if (a >= b or b >= a + 8) else b
            got = _gate(run, 0xF010, a, b)
            assert got == (exp & 0xFFFF), f'0xf010({a},{b}): {got} ≠ {exp}'
    for _ in range(20):
        a = rng.getrandbits(16)
        b = rng.choice([a - 3, a - 1, a, a + 1, a + 7, a + 8, a + 9,
                        rng.getrandbits(16)]) & M32
        exp = a if (a >= b or b >= a + 8) else b
        got = _gate(run, 0xF010, a, b)
        assert got == (exp & 0xFFFF), f'0xf010({a},{b}): {got} ≠ {exp}'


@t(0xF024, 'window-gate «down» (motor 0x7494): a≤b→a; a<b+8→b; иначе→a (u32-cmp)')
def _(run, rng):
    for a in (0, 1, 7, 8, 15, 300, 2550, 0xFFFF):
        for b in range(0, 24):
            exp = a if (a <= b or a >= b + 8) else b
            got = _gate(run, 0xF024, a, b)
            assert got == (exp & 0xFFFF), f'0xf024({a},{b}): {got} ≠ {exp}'
    for _ in range(20):
        a = rng.getrandbits(16)
        b = rng.choice([a - 3, a - 1, a, a + 1, a + 7, a + 8, a + 9,
                        rng.getrandbits(16)]) & M32
        exp = a if (a <= b or a >= b + 8) else b
        got = _gate(run, 0xF024, a, b)
        assert got == (exp & 0xFFFF), f'0xf024({a},{b}): {got} ≠ {exp}'


# cfg-байты @RAM+0xFC7: +1 → 0x8e70, +2 → 0x8e50; out-пул @RAM+0x300F (+0 / +2)
@t(0x8E50, 'cfg×10 (motor): r1=s8[RAM+0xFC9] → u16[RAM+0x300F]=r1*10, return s16; аргумент игнорируется')
def _(run, rng):
    for v in (0, 1, 5, 27, 30, 90, 128, 200, 255):
        run.ram_write(0xFC9, struct.pack('<B', v))
        r0, _ = run.call(0x8E50, [0xDEAD])  # аргумент не используется
        out = struct.unpack('<h', run.ram_read(0x300F, 2))[0]
        sv = v if v < 128 else v - 256          # s8
        assert r0 == (sv * 10) & M32 and out == sv * 10, \
            f'cfg={v}: r0={r0:#x}, out={out}'


@t(0x8E70, 'cfg×10 (motor): r1=s8[RAM+0xFC8] → u16[RAM+0x3011]=r1*10, return s16; аргумент игнорируется')
def _(run, rng):
    for v in (0, 1, 5, 27, 30, 90, 128, 200, 255):
        run.ram_write(0xFC8, struct.pack('<B', v))
        r0, _ = run.call(0x8E70, [0xDEAD])  # аргумент не используется
        out = struct.unpack('<h', run.ram_read(0x3011, 2))[0]
        sv = v if v < 128 else v - 256          # s8
        assert r0 == (sv * 10) & M32 and out == sv * 10, \
            f'cfg={v}: r0={r0:#x}, out={out}'


@t(0xE658, '§57: round-robin диспетчер BLE-задач: гейты byte[0x35]≤2 && byte[0xA49]==1; bl 0x6618; dispatch по counter byte[0xA62] (mod 10) → 6 задач + 4 пустых')
def _(run, rng):
    uc = run.uc
    tasks = {0: 0x6E50, 1: 0x63B8, 2: 0x799C, 3: 0x7A30, 4: 0x69E4, 5: 0x6838}
    # --- гейты закрыты → ранний возврат, counter не тронут
    for b35 in (3, 5):
        run.ram_write(0x35, bytes([b35]))
        run.ram_write(0xA49, b'\x01')
        run.ram_write(0xA62, b'\x05')
        run.call(0xE658, [])
        assert struct.unpack('<B', run.ram_read(0xA62, 1))[0] == 5, 'гейт 0x35 не сработал'
    run.ram_write(0x35, b'\x00')
    run.ram_write(0xA49, b'\x00')
    run.ram_write(0xA62, b'\x05')
    run.call(0xE658, [])
    assert struct.unpack('<B', run.ram_read(0xA62, 1))[0] == 5, 'гейт 0xA49 не сработал'
    # --- гейты открыты: dispatch по counter (останавливаемся на входе в task)
    from unicorn import UC_HOOK_CODE
    for cnt in range(10):
        run.ram_write(0x35, b'\x00')
        run.ram_write(0xA49, b'\x01')
        run.ram_write(0xA62, bytes([cnt]))
        hit = []
        def stopper(uc_, a, s, u_):
            a &= ~1
            if any(t <= a < t + 0x40 for t in tasks.values()):
                hit.append(a)
                uc_.emu_stop()
            elif 0xE6C4 <= a < 0xE6DE:   # хвост (пустой слот) — тоже стоп
                uc_.emu_stop()
        hook = uc.hook_add(UC_HOOK_CODE, stopper)
        run.emu.insn = 0
        uc.reg_write(UC_ARM_REG_LR, 0x08006AB1)   # валидный LR: пустые слоты доходят до pop {r4,pc}
        try:
            uc.emu_start(0xE659, 0, count=200000)
        except UcError as e:
            raise AssertionError(f'fault при dispatch cnt={cnt}: {e}')
        uc.hook_del(hook)
        exp = tasks.get(cnt)
        if exp is None:
            assert not hit, f'cnt={cnt}: ожидался пустой слот, вызван task'
        else:
            assert hit and (exp <= hit[0] < exp + 0x40), \
                f'cnt={cnt}: ожидался task {exp:#06x}, факт {hit and hex(hit[0])}'
    # --- counter инкремент + wrap (пустой слот cnt=9 → 0)
    run.ram_write(0xA62, b'\x09')
    run.call(0xE658, [], max_insn=200000)
    assert struct.unpack('<B', run.ram_read(0xA62, 1))[0] == 0, 'counter не обнулился после 9'
    # восстановление чистого состояния для следующих тестов
    run.ram_write(0x35, b'\x00')
    run.ram_write(0xA49, b'\x00')
    run.ram_write(0xA62, b'\x00')

@t(0x16BD4, '§56: hdr-аномалия — early-exit: v1≤xtab[0]=2002 → всегда константа grid[0]=0x3A08 (реальные таблицы flash)')
def _(run, rng):
    # Фрейм: bl НЕ пушит lr → callee SP = caller SP; [SP]={ygrid, hdr, stride}
    uc = run.uc
    F1 = 0x08000000
    C = STACK_TOP - 0x40
    run.ram_write(C - RAM, struct.pack('<III',
                   F1 + 0x1A4B0, F1 + 0x19F60, 5))
    from unicorn import UC_HOOK_CODE
    for v1 in (0, 100, 2002, 0xFFFFFFFB):      # s8-диапазон caller'а + граница
        for v2 in (0, 500, 0x7FFF):
            uc.reg_write(UC_ARM_REG_R0, v1)
            uc.reg_write(UC_ARM_REG_R1, v2)
            uc.reg_write(UC_ARM_REG_R2, F1 + 0x1A01C)   # xtab
            uc.reg_write(UC_ARM_REG_R3, F1 + 0x19EB4)   # ystruct
            uc.reg_write(UC_ARM_REG_SP, C)
            uc.reg_write(UC_ARM_REG_LR, 0x08006AB1)    # lr → flash (как после bl)
            run.emu.insn = 0
            ret = []
            def h(u_, a, s, usr):
                if (a & ~1) == 0x16D8A:      # эпилог: r0 = результат
                    ret.append(u_.reg_read(UC_ARM_REG_R0))
                    u_.emu_stop()
            hook = uc.hook_add(UC_HOOK_CODE, h)
            try:
                uc.emu_start(0x16BD4 | 1, 0, count=50000)
            except Exception:
                pass
            uc.hook_del(hook)
            assert ret and ret[0] == 0x3A08, \
                f'v1={v1:#x} v2={v2:#x}: {ret} ≠ [0x3a08]'


# --- ADC1-кластер (§58): 0x21FB8 reset / 0x21CA8 конфигуратор / 0x21E18 секвенсор ---
ADC1 = 0x40012400


def _adc_hook(run):
    """запись в ADC1-блок: (hook, список (off, size, val))"""
    from unicorn import UC_HOOK_MEM_WRITE
    uc = run.uc
    writes = []

    def h(u_, access, addr, size, val, usr):
        if ADC1 <= addr < ADC1 + 0x100:
            writes.append((addr - ADC1, size, val))
    return uc.hook_add(UC_HOOK_MEM_WRITE, h), writes


def _adc_zero(run):
    """обнулить ADC1-блок (кроме +0x20 reset-helper НЕ трогает — RMW!)"""
    for off in range(0, 0x80, 4):
        run.periph_write(ADC1 + off, 0)


def _adc_struct(run, fields, slot=0):
    """struct @ (STACK_TOP-0x80-slot*0x40): fields = {off: int}; возвращает адрес (r0/r1-аргумент)"""
    csp = STACK_TOP - 0x80 - slot * 0x40
    rr = csp - RAM
    buf = bytearray(0x40)
    for off, val in fields.items():
        if val < 256:
            buf[off] = val & 0xFF
        else:
            struct.pack_into('<I', buf, off, val & M32)
    run.ram_write(rr, bytes(buf))
    return csp


@t(0x21FB8, '§58: ADC1 reset-helper: CR2/SMPR1/+0x7C=0, +0x3C=0x0FFF0000, блок +0x40..+0x64=0, state-байты struct+0x39/+0x3A=0')
def _(run, rng):
    from unicorn import UC_HOOK_CODE
    uc = run.uc
    _adc_zero(run)
    csp = _adc_struct(run, {0: ADC1})
    hook, writes = _adc_hook(run)
    # ВАЖНО (§58.4): в этом билде Unicorn bx lr с вручную записанным LR
    # «сквозит» на следующую инструкцию → стоп сразу после bx lr @0x21FF8,
    # чтобы fall-through в 0x22000 не испачкал состояние
    stop_at = []

    def h(u_, a, s, usr):
        if (a & ~1) == 0x21FFA:   # fall-through точка
            u_.emu_stop()
    hook2 = uc.hook_add(UC_HOOK_CODE, h)
    try:
        ret = run.call(0x21FB8, [csp])
    finally:
        uc.hook_del(hook)
        uc.hook_del(hook2)
    assert ret[0] == 0
    exp = [(0x18, 4, 0), (0x1C, 4, 0), (0x7C, 4, 0), (0x3C, 4, 0x0FFF0000),
           (0x58, 4, 0), (0x5C, 4, 0), (0x60, 4, 0), (0x64, 4, 0), (0x54, 4, 0),
           (0x40, 4, 0), (0x44, 4, 0), (0x48, 4, 0), (0x4C, 4, 0)]
    assert writes == exp, f'writes={writes}'
    # state-байты в struct
    st = run.ram_read(csp - RAM + 0x39, 2)
    assert st == b'\x00\x00', f'state={st.hex()}'


@t(0x21CA8, '§58: ADC1 validated channel-configurator: asserts (base/variant/ch-fields) → cpsid i; нормальный путь: SMPR1/SMPR2/+0x40/+0x7C поля + ADON')
def _(run, rng):
    # --- assert-пути: спин без записей в ADC
    bad = ({0: 0xDEADBEEF}, {4: 2}, {0xB: 5}, {0xC: 6}, {0xA: 4}, {6: 0x10}, {9: 8})
    for f in bad:
        d = {k: v for k, v in ((0, ADC1), (4, 0), (0xA, 0), (0xB, 0), (0xC, 0), (6, 0), (9, 0))}
        d.update(f)
        csp = _adc_struct(run, d)
        hook, writes = _adc_hook(run)
        try:
            run.call(0x21CA8, [csp], max_insn=300)
        finally:
            run.uc.hook_del(hook)
        assert not writes, f'assert {f}: были записи в ADC!'
    # --- нормальный путь, ветка cfg[8]=0
    _adc_zero(run)
    csp = _adc_struct(run, {0: ADC1, 4: 1, 5: 1, 6: 3, 8: 0, 9: 3, 0xA: 2, 0xB: 4, 0xC: 5})
    hook, writes = _adc_hook(run)
    try:
        ret = run.call(0x21CA8, [csp])
    finally:
        run.uc.hook_del(hook)
    assert ret[0] == 0
    last = {}
    for off, sz, val in writes:
        last[off] = val
    cr2_seq = [val for off, sz, val in writes if off == 0x18]
    assert 2 in cr2_seq and last[0x18] == 1, \
        f'CR2: последовательность {cr2_seq} (ждём ...2...1: SWSTART до reset, ADON в конце)'
    # SMPR1 = cfg[4]<<5 | cfg[0xA]<<3 | bit13(cfg[5])
    assert last[0x1C] == (1 << 5) | (2 << 3) | (1 << 0xD), f'SMPR1={last[0x1C]:#06x}'
    assert last[0x20] == 4, f'SMPR2={last[0x20]:#x}'                          # [2:0]=cfg[0xB]
    assert last[0x40] == 3, f'+0x40={last[0x40]:#x}'                          # [3:0]=cfg[6]
    assert last[0x7C] == 5 << 0x18, f'+0x7C={last[0x7C]:#08x}'               # [20:18]=cfg[0xC]
    # --- ветка cfg[8]=1: SMPR1 |= bit16, поле [19:17]=cfg[9]
    _adc_zero(run)
    csp = _adc_struct(run, {0: ADC1, 4: 0, 5: 0, 6: 0, 8: 1, 9: 3, 0xA: 0, 0xB: 0, 0xC: 0})
    hook, writes = _adc_hook(run)
    try:
        run.call(0x21CA8, [csp])
    finally:
        run.uc.hook_del(hook)
    last = {}
    for off, sz, val in writes:
        last[off] = val
    assert last[0x1C] == 0x10000 | (3 << 17), f'veтка1 SMPR1={last[0x1C]:#06x}'
    # --- ветка cfg[8]=2: SMPR1 |= bit18, поле [19:17]=cfg[9]
    _adc_zero(run)
    csp = _adc_struct(run, {0: ADC1, 4: 0, 5: 0, 6: 0, 8: 2, 9: 7, 0xA: 0, 0xB: 0, 0xC: 0})
    hook, writes = _adc_hook(run)
    try:
        run.call(0x21CA8, [csp])
    finally:
        run.uc.hook_del(hook)
    last = {}
    for off, sz, val in writes:
        last[off] = val
    assert last[0x1C] == 0x100000 | (7 << 17), f'veтка2 SMPR1={last[0x1C]:#06x}'


@t(0x21E18, '§58: ADC1 validated channel-sequencer: asserts (chan≤18, rank≤4, sqr≤0xFFF, low≤3); sampling-поле по диапазонам каналов; SQR[rank]; SMPR1 bit25')
def _(run, rng):
    # --- assert-пути
    def mkmain(mode=0):
        return _adc_struct(run, {0: ADC1, 8: mode})
    m = mkmain()
    bad = ({0: 19}, {1: 5}, {8: 0x1000}, {0xC: 4})
    for f in bad:
        d = {k: v for k, v in ((0, 0), (1, 1), (8, 0), (0xC, 0))}
        d.update(f)
        cc = _adc_struct(run, d, slot=1)
        hook, writes = _adc_hook(run)
        try:
            run.call(0x21E18, [m, cc], max_insn=300)
        finally:
            run.uc.hook_del(hook)
        assert not writes, f'assert {f}: были записи в ADC!'
    # --- нормальный путь: все 5 диапазонов каналов
    cases = [
        (0, 1, 4, 0x111, 3, 0),   # ch0 → +0x20 pos8;  rank1 → +0x58
        (2, 2, 5, 0x222, 2, 1),   # ch2 → +0x20 pos24; rank2 → +0x5C; bit23=1
        (3, 3, 6, 0x333, 1, 0),   # ch3 → +0x24 pos0;  rank3 → +0x60
        (6, 4, 7, 0x444, 0, 0),   # ch6 → +0x24 pos24; rank4 → +0x64
        (7, 1, 4, 0x555, 3, 0),   # ch7 → +0x28 pos0
        (10, 2, 5, 0x666, 3, 0),  # ch10 → +0x28 pos24
        (11, 3, 6, 0x777, 3, 0),  # ch11 → +0x2C pos0
        (14, 4, 7, 0x888, 3, 0),  # ch14 → +0x2C pos24
        (15, 1, 4, 0x999, 3, 0),  # ch15 → +0x30 pos0
        (18, 2, 5, 0xAAA, 3, 0),  # ch18 → +0x30 pos24
    ]
    for chan, rank, smp_val, sqr, low, d in cases:
        _adc_zero(run)
        m = mkmain()
        cc = _adc_struct(run, {0: chan, 1: rank, 4: smp_val, 8: sqr, 0xC: low, 0xD: d}, slot=1)
        hook, writes = _adc_hook(run)
        try:
            ret = run.call(0x21E18, [m, cc])
        finally:
            run.uc.hook_del(hook)
        assert ret[0] == 0
        last = {}
        for off, sz, val in writes:
            last[off] = val
        # sampling-поле: реальный сдвиг из кода (chan*8+8 для ch0-2, chan*8-24 остальным)
        if chan <= 2:
            reg, shift = 0x20, chan * 8 + 8
        elif chan <= 6:
            reg, shift = 0x24, chan * 8 - 24
        elif chan <= 10:
            reg, shift = 0x28, chan * 8 - 24
        elif chan <= 14:
            reg, shift = 0x2C, chan * 8 - 24
        else:
            reg, shift = 0x30, chan * 8 - 24
        # §58.4: RAW-shift (не mod-32!): сдвиг ≥32 → 0. Только ch0..6 достижимы;
        # ch7..18 — no-op (caller 0x1C0B0 компенсирует ch7..10 финальным
        # |= 0x04040404 в [+0x28])
        exp = (smp_val << shift) & 0xFFFFFFFF if shift < 32 else 0
        assert last.get(reg, 0) == exp, \
            f'ch{chan}: [{reg:#04x}]={last.get(reg, 0):#x} ≠ {exp:#x}'
        # SQR[rank]
        sqr_reg = (0x58, 0x5C, 0x60, 0x64)[rank - 1]
        assert last.get(sqr_reg, 0) == sqr, f'ch{chan} rank{rank}: [{sqr_reg:#04x}]={last.get(sqr_reg, 0):#x}'
        # [base+0x54] = chan << (rank*6+2) | low
        assert last.get(0x54, 0) == (chan << (rank * 6 + 2)) | low, \
            f'ch{chan} rank{rank}: [+0x54]={last.get(0x54, 0):#x}'
        # SMPR1 bit25
        exp_bit25 = 1 if d == 1 else 0
        assert (last.get(0x1C, 0) >> 25) & 1 == exp_bit25, \
            f'ch{chan} d={d}: SMPR1 bit25 ≠ {exp_bit25}'


@t(0x1C0B0, '§58: ADC1 sensor-init (caller): reset → 0x21CA8 → 4×0x21E18 (ch C/B/A/F, rank 1-4, smp=4) → финальные OR (+0x20|=0x04040403, +0x24/28/2C|=0x04040404, common +0x40|=0x0E1C6104/+0x44|=9/+0x54|=0x40) → ADON')
def _(run, rng):
    _adc_zero(run)
    csp = _adc_struct(run, {0: ADC1})   # struct строит сам 0x1C0B0 (r0 не нужен)
    hook, writes = _adc_hook(run)
    try:
        ret = run.call(0x1C0B0, [])
    finally:
        run.uc.hook_del(hook)
    last = {}
    for off, sz, val in writes:
        last[off] = val
    # финальные OR-константы caller'а (поверх значений из 0x21CA8/0x21E18)
    assert last.get(0x24, 0) & 0x04040404 == 0x04040404, f'+0x24={last.get(0x24, 0):#x}'
    assert last.get(0x28, 0) & 0x04040404 == 0x04040404, f'+0x28={last.get(0x28, 0):#x}'
    assert last.get(0x2C, 0) & 0x04040404 == 0x04040404, f'+0x2C={last.get(0x2C, 0):#x}'
    assert last.get(0x40, 0) & 0x0E1C6104 == 0x0E1C6104, f'common+0x0={last.get(0x40, 0):#x}'
    assert last.get(0x44, 0) & 9 == 9, f'common+4={last.get(0x44, 0):#x}'
    assert last.get(0x54, 0) & 0x40 == 0x40, f'common+0x14={last.get(0x54, 0):#x}'
    # ADON в самом конце
    cr2_seq = [val for off, sz, val in writes if off == 0x18]
    assert cr2_seq and cr2_seq[-1] & 1, f'CR2 последняя={cr2_seq and hex(cr2_seq[-1])}'
    # SQR rank-регистры: все 4 записаны (value = [sp+0x58] = 0 в caller'е)
    for sq in (0x58, 0x5C, 0x60, 0x64):
        assert sq in last, f'SQR [{sq:#04x}] не записан'


# ---------------------------------------------------------------------------
# §59: 3-проводная шина (0x23374) + RCC/GPIOC init (0x1E2F8)
# ---------------------------------------------------------------------------

BUS3_STRUCT = 0xAC   # struct @RAM+0xAC (пул 0x2347C = 0x200000AC)


def _bus3(run, a=0, b=0, c=0, sel=0, cur=0, delta=0, lim=0, old_out=0):
    """собрать struct @RAM+0xAC: u16[+8]=a, u16[+A]=b, u16[+C]=c,
    u16[+E]=sel, u32[+0x38]=cur, u32[+0x3C]=delta, u32[+0x40]=lim,
    u16[+0x30]=old_out; вернуть (mid, ...) для ожиданий"""
    buf = bytearray(0x50)
    struct.pack_into('<H', buf, 8, a)
    struct.pack_into('<H', buf, 0xA, b)
    struct.pack_into('<H', buf, 0xC, c)
    struct.pack_into('<H', buf, 0xE, sel)
    struct.pack_into('<I', buf, 0x38, cur)
    struct.pack_into('<I', buf, 0x3C, delta)
    struct.pack_into('<I', buf, 0x40, lim)
    struct.pack_into('<H', buf, 0x30, old_out)
    run.ram_write(BUS3_STRUCT, bytes(buf))
    return (cur + delta) >> 1


@t(0x23374, '§59: 3-проводная шина — полная таблица решений (эмуляторно): C==0 → A=u16[+8] (0/1/2/4), C!=0 → B=u16[+A] (3/5/6/7); mid=(cur+delta)>>1; cur обновляется только на «mid»-ветках; A==0/B==7 → r0 из аргументов; пропущенные ветки → старый out. §59.2: на этом чипе bls/CC = lim≤mid (с равенством!), bhi/HS = lim>mid строго (отклонение от ARM: CC включает Z)')
def _(run, rng):
    # mid=10 везде (cur=10, delta=10); lim: 5(<mid), 10(=mid), 100(>mid)
    cases = [
        # (a, b, c, sel, cur, delta, lim, old_out, arg_r0, exp_out, exp_cur)
        (0, 0, 0, 0, 0, 0, 0, 7, 0x1234, 0x1234, None),   # A==0 → r0 caller'а
        (5, 0, 0, 0, 0, 0, 0, 7, 0x1234, 7, None),        # A∉{0,1,2,4} → старый out
        (3, 0, 0, 4, 0, 0, 0, 9, 0, 9, None),
        # A==1
        (1, 0, 0, 1, 0, 0, 0, 0, 0, 1, None),
        (1, 0, 0, 3, 10, 10, 5, 0, 0, 2, 10),             # lim≤mid → 2
        (1, 0, 0, 3, 10, 10, 10, 0, 0, 2, 10),            # lim==mid → 2 (CC включает =)
        (1, 0, 0, 3, 10, 10, 100, 0, 0, 3, 10),           # lim>mid → 3
        (1, 0, 0, 5, 10, 10, 5, 0, 0, 5, 10),             # lim≤mid → 5
        (1, 0, 0, 5, 10, 10, 10, 0, 0, 5, 10),            # lim==mid → 5
        (1, 0, 0, 5, 10, 10, 100, 0, 0, 4, 10),           # lim>mid → 4
        (1, 0, 0, 7, 1, 1, 1, 0, 0, 6, 1),                # sel 7 → 6, cur не трогает
        (1, 0, 0, 2, 0, 0, 0, 0, 0, 2, None),             # else → out=sel
        # A==2
        (2, 0, 0, 2, 0, 0, 0, 0, 0, 2, None),
        (2, 0, 0, 3, 10, 10, 5, 0, 0, 3, 10),             # lim≤mid → 3
        (2, 0, 0, 3, 10, 10, 10, 0, 0, 3, 10),            # lim==mid → 3
        (2, 0, 0, 3, 10, 10, 100, 0, 0, 1, 10),           # lim>mid → 1
        (2, 0, 0, 6, 10, 10, 100, 0, 0, 6, 10),           # lim>mid строго (bhi) → 6
        (2, 0, 0, 6, 10, 10, 10, 0, 0, 4, 10),            # lim==mid → 4 (bhi нет)
        (2, 0, 0, 6, 10, 10, 5, 0, 0, 4, 10),             # lim<mid → 4
        (2, 0, 0, 7, 0, 0, 0, 0, 0, 5, None),
        # A==4
        (4, 0, 0, 4, 0, 0, 0, 0, 0, 4, None),
        (4, 0, 0, 5, 10, 10, 100, 0, 0, 5, 10),           # lim>mid строго → 5
        (4, 0, 0, 5, 10, 10, 10, 0, 0, 1, 10),            # lim==mid → 1
        (4, 0, 0, 5, 10, 10, 5, 0, 0, 1, 10),
        (4, 0, 0, 6, 10, 10, 5, 0, 0, 6, 10),             # lim≤mid → 6
        (4, 0, 0, 6, 10, 10, 10, 0, 0, 6, 10),            # lim==mid → 6
        (4, 0, 0, 6, 10, 10, 100, 0, 0, 2, 10),           # lim>mid → 2
        (4, 0, 0, 7, 1, 1, 1, 0, 0, 3, 1),                # sel 7 → 3, cur не трогает
        # B==3 (C!=0)
        (0, 3, 1, 0, 0, 0, 0, 0, 0, 4, None),
        (0, 3, 1, 1, 10, 10, 100, 0, 0, 5, 10),           # lim>mid строго → 5
        (0, 3, 1, 1, 10, 10, 10, 0, 0, 1, 10),            # lim==mid → 1
        (0, 3, 1, 1, 10, 10, 5, 0, 0, 1, 10),
        (0, 3, 1, 2, 10, 10, 5, 0, 0, 6, 10),             # lim≤mid → 6
        (0, 3, 1, 2, 10, 10, 10, 0, 0, 6, 10),            # lim==mid → 6
        (0, 3, 1, 2, 10, 10, 100, 0, 0, 2, 10),           # lim>mid → 2
        (0, 3, 1, 3, 0, 0, 0, 0, 0, 3, None),
        (0, 3, 1, 9, 0, 0, 0, 0, 0, 9, None),             # else → out=sel
        # B==5
        (0, 5, 1, 0, 0, 0, 0, 0, 0, 2, None),
        (0, 5, 1, 1, 10, 10, 5, 0, 0, 3, 10),             # lim≤mid → 3
        (0, 5, 1, 1, 10, 10, 10, 0, 0, 3, 10),            # lim==mid → 3
        (0, 5, 1, 1, 10, 10, 100, 0, 0, 1, 10),           # lim>mid → 1
        (0, 5, 1, 4, 10, 10, 100, 0, 0, 6, 10),           # lim>mid строго → 6
        (0, 5, 1, 4, 10, 10, 10, 0, 0, 4, 10),            # lim==mid → 4
        (0, 5, 1, 4, 10, 10, 5, 0, 0, 4, 10),
        (0, 5, 1, 5, 0, 0, 0, 0, 0, 5, None),
        # B==6
        (0, 6, 1, 0, 0, 0, 0, 0, 0, 1, None),
        (0, 6, 1, 2, 10, 10, 5, 0, 0, 2, 10),             # lim≤mid → 2
        (0, 6, 1, 2, 10, 10, 10, 0, 0, 2, 10),            # lim==mid → 2
        (0, 6, 1, 2, 10, 10, 100, 0, 0, 3, 10),           # lim>mid → 3
        (0, 6, 1, 4, 10, 10, 5, 0, 0, 5, 10),             # lim≤mid → 5
        (0, 6, 1, 4, 10, 10, 10, 0, 0, 5, 10),            # lim==mid → 5
        (0, 6, 1, 4, 10, 10, 100, 0, 0, 4, 10),           # lim>mid → 4
        (0, 6, 1, 6, 0, 0, 0, 0, 0, 6, None),
        # B==7 / пропуски
        (0, 7, 1, 0, 0, 0, 0, 7, 0x77, 0x77, None),       # B==7 → r0 caller'а
        (0, 9, 1, 0, 0, 0, 0, 8, 0x55, 8, None),          # B∉{3,5,6,7} → старый out
    ]
    for (a, b, c, sel, cur, delta, lim, old, r0arg, exp_out, exp_cur) in cases:
        _bus3(run, a=a, b=b, c=c, sel=sel, cur=cur, delta=delta,
              lim=lim, old_out=old)
        r0, _ = run.call(0x23374, [r0arg])
        tag = f'A={a} B={b} C={c} sel={sel}'
        assert r0 == exp_out, f'{tag}: out={r0:#x} ≠ {exp_out:#x}'
        if exp_cur is not None:
            got_cur = struct.unpack_from('<I', run.ram_read(BUS3_STRUCT + 0x38, 4), 0)[0]
            assert got_cur == exp_cur, f'{tag}: cur={got_cur:#x} ≠ {exp_cur:#x}'


@t(0x1E2F8, '§59: RCC/GPIOC init: RCC+0x3C |= 0xF0000 (по битам 16-19), +0x40 |= 0xE0000, +0x44 |= 0x4A00, +0x3C |= 0x8001; helper 0x19A9A(sp,0x28): RCC+0x00/04=0, +0x08|=0x900; tail 0x22824 (RCC-делители: +0x08 nibble-логика по MODER=0x44AA200, mid-ветка → 1) → +0x08=0x900; финал RCC+0x00 = 0x100000 (bit20 enable)')
def _(run, rng):
    uc = run.uc
    # RCC-регион обнуляем: OR-записи не идемпотентны (один Run на все тесты)
    uc.mem_write(0x40021000, b'\x00' * 0x100)
    writes = []
    def hw(u_, acc, addr, size, val, usr):
        if 0x40021000 <= addr < 0x40021100:
            writes.append((addr - 0x40021000, val))
    hook = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, 0x40021000, 0x40021100)
    try:
        r0, _ = run.call(0x1E2F8, [])
    finally:
        uc.hook_del(hook)
    assert r0 == 0x100000, f'r0={r0:#x}'
    seq = [(off, val) for off, val in writes]
    # RCC+0x3C: по битам 16..19 (0x80000→0xC0000→0xE0000→0xF0000)
    c3c = [v for o, v in seq if o == 0x3C]
    assert c3c[:4] == [0x80000, 0xC0000, 0xE0000, 0xF0000], f'+0x3C={ [hex(v) for v in c3c]}'
    # RCC+0x40: 0x80000 → 0xC0000 → 0xE0000
    c40 = [v for o, v in seq if o == 0x40]
    assert c40 == [0x80000, 0xC0000, 0xE0000], f'+0x40={[hex(v) for v in c40]}'
    # RCC+0x44: 0x4000 → 0x4800 → 0x4A00
    c44 = [v for o, v in seq if o == 0x44]
    assert c44 == [0x4000, 0x4800, 0x4A00], f'+0x44={[hex(v) for v in c44]}'
    # RCC+0x3C финал: |= 0x8000 → 0xF8000, |= 1 → 0xF8001
    assert c3c[-2:] == [0xF8000, 0xF8001], f'+0x3C хвост={[hex(v) for v in c3c[-2:]]}'
    # helper 0x19A9A: RCC+0x00=0, +0x04=0 (×2), +0x08=0, +0x08=0x900 (×2)
    c00 = [v for o, v in seq if o == 0x00]
    c04 = [v for o, v in seq if o == 0x04]
    c08 = [v for o, v in seq if o == 0x08]
    assert c00[0] == 0 and c04[:2] == [0, 0], f'+0x00/0x04={c00}/{c04}'
    assert 0 in c08 and 0x900 in c08, f'+0x08={c08}'
    # финал: RCC+0x00 = 0x100000 (bit20)
    assert c00[-1] == 0x100000, f'+0x00 последняя={hex(c00[-1])}'


@t(0x1302C, '§59: RCC-пульсатор USART: base → (рег, бит): 0x40013800(USART1)→+0x0C/0x4000, 0x40004400(USART2)→+0x10/0x20000, 0x40004800(USART3)→+0x10/0x40000, 0x40015000→+0x0C/0x20000, 0x40015400→+0x0C/0x40000; последовательность |=bit затем &=~bit (пульс); неизвестная base → без записей; r0 = бит')
def _(run, rng):
    uc = run.uc
    cases = [
        (0x40013800, 0x0C, 0x4000),
        (0x40004400, 0x10, 0x20000),
        (0x40004800, 0x10, 0x40000),   # USART3
        (0x40015000, 0x0C, 0x20000),
        (0x40015400, 0x0C, 0x40000),
    ]
    for base, reg, bit in cases:
        uc.mem_write(0x40021000, b'\x00' * 0x100)
        writes = []
        def hw(u_, acc, addr, size, val, usr):
            if 0x40021000 <= addr < 0x40021100:
                writes.append((addr - 0x40021000, val))
        hook = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, 0x40021000, 0x40021100)
        try:
            r0, _ = run.call(0x1302C, [base])
        finally:
            uc.hook_del(hook)
        assert r0 == bit, f'{base:#x}: r0={r0:#x} ≠ {bit:#x}'
        assert writes == [(reg, bit), (reg, 0)], \
            f'{base:#x}: записи={[(hex(o), hex(v)) for o, v in writes]}'
    # неизвестная base → без записей
    uc.mem_write(0x40021000, b'\x00' * 0x100)
    writes = []
    def hw2(u_, acc, addr, size, val, usr):
        if 0x40021000 <= addr < 0x40021100:
            writes.append(1)
    hook = uc.hook_add(UC_HOOK_MEM_WRITE, hw2, None, 0x40021000, 0x40021100)
    try:
        run.call(0x1302C, [0x40010800])
    finally:
        uc.hook_del(hook)
    assert writes == [], f'неизвестная base: записей={len(writes)}'


@t(0x1E298, '§59: DMA+ADC init: bl 0x1A5D4 (ADC1 CR2|=0x20) → validated-write 0x2359C(0x40020000, 0, 0x5D000041) в [0x40020108] c readback-retry → u32[0x40020028]=1 (enable) → ADC1 CR2|=4; возврат pop {r4,pc} (§59.3: на чипе POP всегда восстанавливает pc)')
def _(run, rng):
    uc = run.uc
    # обнуляем ADC1 и блок 0x40020000 (RMW-записи)
    uc.mem_write(0x40012400, b'\x00' * 0x100)
    uc.mem_write(0x40020000, b'\x00' * 0x200)
    writes = []
    def hw(u_, acc, addr, size, val, usr):
        if (0x40012400 <= addr < 0x40012500) or (0x40020000 <= addr < 0x40020200):
            writes.append((addr, val))
    hook = uc.hook_add(UC_HOOK_MEM_WRITE, hw,
                       None, 0x40012400, 0x40012500)
    hook2 = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, 0x40020000, 0x40020200)
    try:
        r0, _ = run.call(0x1E298, [])
    finally:
        uc.hook_del(hook); uc.hook_del(hook2)
    # §57/§59: возврат через LR-sentinel даёт FETCH_UNMAPPED — это артефакт
    # харнесса (pop {pc} → 0x0BADF001), не fault функции: все записи уже сделаны
    assert r0 == 0x40012400, f'r0={r0:#x}'
    # нормализуем: ADC1-смещения как есть, блок 0x40020000 → +0x10000
    seq = [(a - 0x40012400 if a < 0x40013000 else a - 0x40020000 + 0x10000,
            v) for a, v in writes]
    # порядок: ADC1 CR2|=0x20 → [0x40020108]=0x5D000041 → [0x40020028]=1 → ADC1 CR2|=4
    assert seq[0] == (0x18, 0x20), f'1-я запись={seq[0]}'
    assert (0x10108, 0x5D000041) in seq, f'validated-write нет: {seq}'
    assert (0x10028, 1) in seq, f'enable нет: {seq}'
    assert seq[-1] == (0x18, 0x24), f'последняя={seq[-1]}'
    i_dma = next(i for i, (o, v) in enumerate(seq) if o == 0x10108)
    i_en = next(i for i, (o, v) in enumerate(seq) if o == 0x10028)
    assert seq.index((0x18, 0x20)) < i_dma < i_en < len(seq) - 1, f'порядок: {seq}'


@t(0x1D640, '§59: мотор-TIM init (TIM @0x40012C00 + channel-блоки @0x48000000/0x48000400): детерминированная последовательность 107 записей; финал TIM: +0x3C=0x8CA (prescaler), CCR +0x44/48/4C = 0x45B→0, +0x50=0x8C9, +0x54=0x1D24, +0x30=0x1DDD, +0x28/+0x2C=0x6060, +0x04=0x2A00, +0x0C=0x80; enable +0x00=0x41 — ПОСЛЕДНИЙ; блоки 0x48: A +0x2C=0x666/+0x10=0x2A0000, B +0x2C=0x66660000/+0x10=0xAA000000; r0=0x41')
def _(run, rng):
    import struct as _st
    uc = run.uc
    for base, sz in ((0x40012c00, 0x400), (0x48000000, 0x2000)):
        uc.mem_write(base, b'\x00' * sz)
    writes = []
    def hw(u_, acc, addr, size, val, usr):
        if (0x40012C00 <= addr < 0x40012C60) or (0x48000000 <= addr < 0x48000500):
            writes.append((addr, val))
    h1 = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, 0x40012C00, 0x40012C60)
    h2 = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, 0x48000000, 0x48000500)
    try:
        r0, _ = run.call(0x1D640, [], max_insn=300000)
    finally:
        uc.hook_del(h1); uc.hook_del(h2)
    assert r0 == 0x41, f'r0={r0:#x}'
    assert len(writes) == 107, f'записей={len(writes)} (ожидалось 107)'
    # финальные состояния
    def rd(a):
        return _st.unpack_from('<I', bytes(uc.mem_read(a, 4)), 0)[0]
    tim = {off: rd(0x40012C00 + off) for off in range(0, 0x60, 4)}
    assert tim[0x00] == 0x41 and tim[0x04] == 0x2A00 and tim[0x0C] == 0x80
    assert tim[0x24] == 1 and tim[0x28] == 0x6060 and tim[0x2C] == 0x6060
    assert tim[0x30] == 0x1DDD and tim[0x3C] == 0x8CA
    assert tim[0x50] == 0x8C9 and tim[0x54] == 0x1D24
    assert all(tim[o] == 0 for o in (0x44, 0x48, 0x4C)), 'CCR не очищены'
    a = {off: rd(0x48000000 + off) for off in range(0, 0x40, 4)}
    b = {off: rd(0x48000400 + off) for off in range(0, 0x40, 4)}
    assert a[0x2C] == 0x666 and a[0x10] == 0x2A0000
    assert b[0x2C] == 0x66660000 and b[0x10] == 0xAA000000
    assert all(a[o] == 0 for o in (0x14, 0x18, 0x1C, 0x20, 0x24))
    # порядок: CCR-константы 0x45B пишутся ДО их очистки; enable — последняя запись
    i_45b = next(i for i, (ad, v) in enumerate(writes) if ad == 0x40012C44 and v == 0x45B)
    i_clr = next(i for i, (ad, v) in enumerate(writes) if ad == 0x40012C44 and v == 0)
    assert i_45b < i_clr
    assert writes[-1] == (0x40012C00, 0x41), f'последняя запись={writes[-1]}'


@t(0x1BF48, '§59: МОТОР-ИНИТ (221 запись, детерминированно): 1) bl 0x1D640 (мотор-TIM @0x40012C00 + channel-блоки 0x48000000/0x48000400; enable TIM — запись #106); 2) bl 0x1C0B0 (ADC1 sensor-init §58: финал +0x18=1 ADON, +0x54=0x3CA2CC43 SQR ch C/B/A/F); 3) bl 0x1C1AC/0x1BEDC; 4) GPIO-блок @0x48000C00: CRL(+0x04) &= ~2, validated-setter 0x22000(r4, 2, cfg7) → +0x10=4 (bit2), CRL &= ~2, 0x22000(r4, 1, cfg7) → +0x10=5 (bit0+bit2); r0=0x48000C00')
def _(run, rng):
    import struct as _st
    uc = run.uc
    for base, sz in ((0x40012400, 0x1000), (0x40012c00, 0x400), (0x48000000, 0x2000)):
        uc.mem_write(base, b'\x00' * sz)
    writes = []
    def hw(u_, acc, addr, size, val, usr):
        if (0x40012000 <= addr < 0x40013000) or (0x48000000 <= addr < 0x48002000):
            writes.append((addr, val))
    h1 = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, 0x40012000, 0x40013000)
    h2 = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, 0x48000000, 0x48002000)
    try:
        r0, _ = run.call(0x1BF48, [], max_insn=500000)
    finally:
        uc.hook_del(h1); uc.hook_del(h2)
    assert r0 == 0x48000C00, f'r0={r0:#x}'
    assert len(writes) == 221, f'записей={len(writes)} (ожидалось 221)'
    # фаза 1 (0x1D640) кончается enable TIM — запись #106
    assert writes[106] == (0x40012C00, 0x41), f'#106={writes[106]}'
    def rd(a):
        return _st.unpack_from('<I', bytes(uc.mem_read(a, 4)), 0)[0]
    # ADC1-финал (§58)
    a1 = {off: rd(0x40012400 + off) for off in range(0, 0x80, 4)}
    assert a1[0x00] == 0x40 and a1[0x18] == 1 and a1[0x1C] == 0x19
    assert a1[0x20] == 0x4040403 and a1[0x24] == a1[0x28] == a1[0x2C] == 0x4040404
    assert a1[0x3C] == 0xFFF0000 and a1[0x40] == 0xE1C6104 and a1[0x44] == 9
    assert a1[0x54] == 0x3CA2CC43, f'SQR={a1[0x54]:#x}'
    # TIM-финал (из 0x1D640)
    tim = {off: rd(0x40012C00 + off) for off in range(0, 0x60, 4)}
    assert tim[0x00] == 0x41 and tim[0x3C] == 0x8CA and tim[0x50] == 0x8C9
    # channel-блоки 0x48
    assert rd(0x4800002C) == 0x666 and rd(0x48000010) == 0x2A0000
    assert rd(0x4800042C) == 0x66660000 and rd(0x48000410) == 0xAA000000
    # GPIO-блок @0x48000C00: только +0x10 = 5, CRL очищен
    c = {off: rd(0x48000C00 + off) for off in range(0, 0x40, 4)}
    assert c[0x10] == 5 and c[0x04] == 0, f'блок C: { {hex(k): hex(v) for k, v in c.items() if v} }'
    # хвост: последовательность CRL/0x22000 на блоке C
    tail = [(a, v) for a, v in writes[107:] if 0x48000C00 <= a < 0x48000C40]
    assert tail[0] == (0x48000C04, 0), f'хвост[0]={tail[0]}'
    i_m2 = next(i for i, (a, v) in enumerate(tail) if a == 0x48000C10 and v == 4)
    i_m1 = next(i for i, (a, v) in enumerate(tail) if a == 0x48000C10 and v == 5)
    assert tail[i_m2 + 1] == (0x48000C04, 0), 'CRL &= ~2 между mode-2 и mode-1'
    assert tail[-1] == (0x48000C10, 5), f'хвост[-1]={tail[-1]}'


@t(0x1C1AC, '§59: ADC-DMA transfer setup (блок @0x40020000): validated-writes [+0x100]=**0x40012450** (src=ADC1 DR), [+0x104]=**0x20001692** (dst=RAM+0x1692), bl 0x2359C → [+0x108]=0x5D000041 (ctrl, тот же что в 0x1E298); enable: +0x28=1, +0x14=1, +0x70=0x19, +0x50|=1; IRQ-хвост: [**0xE000E100**]=0x200 (прямая запись bit9), [NVIC+0x08 (0xE000E408)] &= ~0xFF00 (clear биты 8..15); r0=0')
def _(run, rng):
    uc = run.uc
    uc.mem_write(0x40020000, b'\x00' * 0x200)
    # SYS-регион обнуляем: [0xE000E408] &= ~0xFF00 — значение зависит от предыдущего
    uc.mem_write(0xE000E000, b'\x00' * 0x1000)
    writes = []
    def hw(u_, acc, addr, size, val, usr):
        if addr >= 0x20017F00:   # стек отбрасываем
            writes.append((addr, val))
    h1 = uc.hook_add(UC_HOOK_MEM_WRITE, hw)   # всё пространство
    try:
        r0, _ = run.call(0x1C1AC, [], max_insn=100000)
    finally:
        uc.hook_del(h1)
    assert r0 == 0, f'r0={r0:#x}'
    seq = [(a, v) for a, v in writes if not (0x20017F00 <= a < 0x20018000)]
    assert len(seq) == 11, f'записей={len(seq)}: {seq}'
    # порядок: src → dst → ctrl → enable-группа → ctrl |= 1 → IRQ
    assert seq[0] == (0x40020004, 1)
    assert seq[1] == (0x40020100, 0x40012450), f'src={seq[1]}'
    assert seq[2] == (0x40020104, 0x20001692), f'dst={seq[2]}'
    assert seq[3] == (0x40020108, 0x5D000041)
    assert seq[4] == (0x40020028, 1) and seq[5] == (0x40020014, 1)
    assert seq[6] == (0x40020070, 0x19) and seq[7] == (0x40020050, 1)
    assert seq[8] == (0x40020108, 0x5D000041), 'ctrl |= 1 (bit0 уже стоит — значение не меняется)'
    # IRQ-хвост: ядро + NVIC
    assert seq[9] == (0xE000E100, 0x200), f'IRQ enable={seq[9]}'
    assert seq[10] == (0xE000E408, 0), f'NVIC+0x08={seq[10]}'


# ---------------------------------------------------------------------------
# §59.6: RX-парсер USART3 0x1E9E0 (вызывающий — периодический таск 0x1DFD8)
#
# Контракт (эмпирически):
# - state = byte[RAM+0x172]: 0 → только RAM+0x171=0; 1 → обработать 1 сообщение
# - head = byte[RAM+0x2C0] (кольцо 3 слота × 150 B @RAM+0x881), байт команды = ring[head*150+1]
# - toggle = byte[RAM+0x2C9] (0..7): индекс context-слота @RAM+0x10B5 + i*0x76
# - dispatch по ASCII: '@'→только head++; 'G'/'K'/'c'→frame-start (len 20/27/83);
#   'A'→telemetry-snapshot; 'a' и др. → response-сборщики
# - context: {6,'e',len,'O','K',crc,0x9A} (frame-start) или {'d'-кадры}
# - crc = сумма байтов context[1..] mod 256; checksum = 0xFF - context[1]
# - после обработки: state=0, head++ (wrap при ≥3), toggle++ (wrap при ≥8, frame-start)
#
# Методич. (§59.6.3): на этом чипе Bcond-кодировка D0xx = BEQ c imm8 в [7:0]
# (не стандартный ARM [11:4]); capstone декодирует цели верно, но метки cond — нет.
# ---------------------------------------------------------------------------

def _parser_probe(run, state=1, head=0, toggle=0, byte=0, slot_data=None):
    """засеять состояние парсера и прогнать; вернуть список записей (off, val) в RAM"""
    uc = run.uc
    uc.mem_write(RAM + 0x172, bytes([state]))
    uc.mem_write(RAM + 0x2C0, bytes([head]))
    uc.mem_write(RAM + 0x2C9, bytes([toggle]))
    uc.mem_write(RAM + 0x882 + head * 150, bytes([byte]))
    if slot_data:
        for off, v in slot_data.items():
            uc.mem_write(RAM + 0x881 + head * 150 + off, bytes([v]))
    ev = []
    def hw(u_, acc, addr, size, val, usr):
        if RAM <= addr < RAM + 0x20000 and not (0x20017F00 <= addr < 0x20018000):
            ev.append((addr - RAM, val))
    h = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, RAM, RAM + 0x20000)
    try:
        run.call(0x1E9E0, [], max_insn=50000)
    finally:
        uc.hook_del(h)
    return ev


def _ctx(run, slot, n=13):
    """context-слот @RAM+0x10B5 + slot*0x96 (n байтов; stride = размер ring-слота)"""
    base = RAM + 0x10B5 + slot * 0x96
    return bytes(run.uc.mem_read(base, n))


@t(0x1E9E0, '§59.6: RX-парсер USART3 — dispatch-каркас: state=0 → только RAM+0x171=0; state=1 + неизвестный байт → RAM+0x171=0, state→0, head 0→1; "G" frame-start (toggle=0): context @0x10B5 = {6,"e",20,"O","K",0x13,0x9A}, CRC-структ {idx=5,crc=0x13,sum=0x9A}, флаг RAM+0x310=0, toggle 0→1, head 0→1; "G" (toggle=7): context @0x14CF, toggle 8→0 (wrap)')
def _(run, rng):
    # state=0: только RAM+0x171=0
    ev = _parser_probe(run, state=0, byte=0x47)
    assert ev == [(0x171, 0)], f'state=0: {ev}'
    # неизвестный байт (0x00): минимальные записи
    ev = _parser_probe(run, state=1, head=0, byte=0x00)
    assert ev == [(0x171, 0), (0x172, 0), (0x2C0, 1)], f'неизв. байт: {ev}'
    # "G" frame-start, toggle=0
    ev = _parser_probe(run, state=1, head=0, toggle=0, byte=0x47)
    got = dict(ev)
    assert got.get(0x310) == 0, f'флаг G: {ev}'
    assert got.get(0x2C9) == 1, f'toggle: {ev}'
    assert got.get(0x2C0) == 1, f'head: {ev}'
    assert got.get(0x172) == 0, f'state: {ev}'
    ctx = _ctx(run, 0)
    assert ctx[:7] == bytes([6, 0x65, 20, 0x4F, 0x4B, 0x13, 0x9A]), f'context G: {ctx.hex(" ")}'
    # CRC-структ @RAM+0x177: idx=5, crc=0x13, sum=0x9A
    assert got.get(0x177) == 5 and got.get(0x178) == 0x13 and got.get(0x179) == 0x9A, f'crc-структ: {ev}'
    # "G" frame-start, toggle=7 → слот 7, wrap toggle 8→0
    ev = _parser_probe(run, state=1, head=0, toggle=7, byte=0x47)
    tw = [v for a, v in ev if a == 0x2C9]
    assert tw == [8, 0], f'toggle wrap: {tw}'
    ctx7 = _ctx(run, 7)
    assert ctx7[:7] == bytes([6, 0x65, 20, 0x4F, 0x4B, 0x13, 0x9A]), f'context G slot7: {ctx7.hex(" ")}'


@t(0x1E9E0, '§59.6: RX-парсер — "A" telemetry-snapshot: ring[3..9] → RAM+0x2E8/9 (rev16(ring4<<8|ring3)), 0x2EA/EB (нибблы ring5), 0x2EC=ring6, ring7 → {bit7→0x2ED, bit6→0x2EE, [5:0]→0x2EF}, 0x2F0=ring8, 0x2F1=ring9; context = {0xC,"d",0x20,7,ring3..9,crc,0x9B}; crc=(0x64+0x20+7+Σring[3..9])&0xFF')
def _(run, rng):
    data = {i: 0x10 + i for i in range(3, 10)}   # ring[3..9] = 0x13..0x19
    ev = _parser_probe(run, state=1, head=0, byte=0x41, slot_data=data)
    uc = run.uc
    def rd(off):
        return uc.mem_read(RAM + off, 1)[0]
    # rev16: u16 LE @0x2E8 = rev16((ring4<<8)|ring3) = rev16(0x1413) = 0x1314
    assert (rd(0x2E8), rd(0x2E9)) == (0x14, 0x13), f'rev16: {rd(0x2E8):#x},{rd(0x2E9):#x}'
    assert rd(0x2EA) == 5 and rd(0x2EB) == 1, f'нибблы ring5: {rd(0x2EA):#x},{rd(0x2EB):#x}'
    assert rd(0x2EC) == 0x16, f'ring6: {rd(0x2EC):#x}'
    # ring7 = 0x17: bit7=0, bit6=0, [5:0]=0x17
    assert rd(0x2ED) == 0 and rd(0x2EE) == 0 and rd(0x2EF) == 0x17, f'ring7-сплит: {rd(0x2ED):#x},{rd(0x2EE):#x},{rd(0x2EF):#x}'
    assert rd(0x2F0) == 0x18 and rd(0x2F1) == 0x19, f'ring8/9: {rd(0x2F0):#x},{rd(0x2F1):#x}'
    # context: {0xC,'d',0x20,7,data[0..6],crc,checksum}
    ctx = _ctx(run, 0)
    assert ctx[0] == 0x0C and ctx[1] == 0x64 and ctx[2] == 0x20 and ctx[3] == 7
    assert ctx[4:11] == bytes([0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19]), f'data: {ctx.hex(" ")}'
    crc = (0x64 + 0x20 + 7 + sum(range(0x13, 0x1A))) & 0xFF   # = 0x25
    assert ctx[11] == crc == 0x25, f'crc: {ctx[11]:#x} (ожидалось {crc:#x})'
    assert ctx[12] == 0x9B, f'checksum: {ctx[12]:#x}'
    # toggle и head
    got = dict(ev)
    assert got.get(0x2C9) == 1 and got.get(0x2C0) == 1 and got.get(0x172) == 0


# ---------------------------------------------------------------------------
# §59.7: «own» round 0x1DD8C (128 B, bl из 0x1a814) — один раунд шифра «own»
#
# Буфер 16 B = 4 группы × 4 байта; каждая группа [A,B,C,D] смешивается
# независимо через CRC-8 (полином 0x1B, MSB-first) как Feistel:
#   X  = A^B^C^D
#   A' = A ^ crc8(A^B) ^ X
#   B' = B ^ crc8(B^C) ^ X
#   C' = C ^ crc8(C^D) ^ X
#   D' = D ^ crc8(D^A) ^ X
# где crc8(x) = ((x<<1) ^ (0x1B & -(x>>7))) & 0xFF (один шаг CRC-8).
# Чистая функция: все обращения к памяти — относительно r0 (буфер),
# без pool/абсолютных RAM-адресов.
# ---------------------------------------------------------------------------

def ref_crc8_step(x):
    return ((x << 1) ^ (0x1B & -(x >> 7))) & 0xFF


def ref_own_round(buf16):
    b = bytearray(buf16)
    for i in range(4):
        g = i * 4
        A, B, C, D = b[g], b[g + 1], b[g + 2], b[g + 3]
        X = A ^ B ^ C ^ D
        b[g + 0] = A ^ ref_crc8_step(A ^ B) ^ X
        b[g + 1] = B ^ ref_crc8_step(B ^ C) ^ X
        b[g + 2] = C ^ ref_crc8_step(C ^ D) ^ X
        b[g + 3] = D ^ ref_crc8_step(D ^ A) ^ X
    return bytes(b)


@t(0x1DD8C, '§59.7: «own» round — 16 B = 4×4 байта; каждая группа [A,B,C,D]: X=A^B^C^D; A''=A^crc8(A^B)^X, B''=B^crc8(B^C)^X, C''=C^crc8(C^D)^X, D''=D^crc8(D^A)^X; crc8(x)=((x<<1)^(0x1B&-(x>>7)))&0xFF (CRC-8 poly 0x1B MSB-first); чистая функция от буфера в r0')
def _(run, rng):
    buf_off = 0x1F000
    for _ in range(32):
        data = bytes(rng.randrange(256) for _ in range(16))
        exp = ref_own_round(data)
        run.ram_write(buf_off, data)
        run.call(0x1DD8C, (RAM + buf_off,), max_insn=20000)
        got = run.ram_read(buf_off, 16)
        assert got == exp, f'own_round:\n in : {data.hex(" ")}\n exp: {exp.hex(" ")}\n got: {got.hex(" ")}'
    # детерминированный якорь: все нули → все нули (X=0, crc8(0)=0)
    run.ram_write(buf_off, b'\x00' * 16)
    run.call(0x1DD8C, (RAM + buf_off,), max_insn=20000)
    assert run.ram_read(buf_off, 16) == b'\x00' * 16, 'нули должны остаться нулями'


# ---------------------------------------------------------------------------
# §59.8: периодический таск USART3 0x1DFD8 (344 B) — inline-логика верифицирована
#
# Тело: u16 tick-счётчик @RAM+0x2BA++ → 3 «утечных интегратора» с обратной
# связью → расчёт % батареи (линейная карта) → вызовы 0x1E9E0/0x1F1CC/
# 0x1F71C/0x211F8 (+ 0x1B67C/0x2186C на старте) → главный u32-счётчик @RAM+0x314++.
#
# Верификация изолирует INLINE-логику: 6 `bl` патчатся в NOP (свежий Run —
# общий не портится). Подфункции верифицируются отдельно (0x1E9E0 — §59.6).
#
# Интегратор (3 шт, пары acc/delta/out):
#   new_acc = (acc + delta - old_out) & 0xFFFFFFFF
#   new_out = asr(new_acc, 5)  (s16)
#   пары: (0x298/0x278/0x27A), (0x288/0x284/0x286), (0x2A0/0x29C/0x29E)
#
# % батареи: level = s16[RAM+0x1794 + 12] (элемент 6 массива @RAM+0x1794):
#   level >= 535 → 100;  level < 415 → 0;  иначе (level-415)*100/120 (signed div)
#   (активный диапазон [415,535] → [0,100]); результат в byte[RAM+0x306].
#   Гейт: вычисляется если flag byte[RAM+0x321]==1 ИЛИ u16[RAM+0x312] >= 30000
#   (тогда flag:=1); иначе — только инкремент u16[RAM+0x312].
# ---------------------------------------------------------------------------

DFD8_BLS = [0x1dfda, 0x1dfe6, 0x1e0ae, 0x1e0b2, 0x1e0cc, 0x1e0d0]
DFD8_NOP4 = b'\x00\xbf\x00\xbf'


def _dfd8_asr(v, n):
    """арифметический сдвиг u32 вправо на n, результат как signed s16"""
    v &= 0xFFFFFFFF
    if v & 0x80000000:
        v -= 0x100000000
    r = (v >> n) & 0xFFFF
    return r - 0x10000 if r >= 0x8000 else r


def ref_dfd8_integ(acc, delta_s16, out_s16):
    na = (acc + delta_s16 - out_s16) & 0xFFFFFFFF
    return na, _dfd8_asr(na, 5)


def ref_dfd8_batpct(level):
    if level >= 535:
        return 100
    if level < 415:
        return 0
    return ((level - 415) * 100) // 120


@t(0x1DFD8, '§59.8: периодический таск USART3 — inline-логика (6 bl патч в NOP, save/restore): u16 tick @0x2BA++; 3 интегратора new_acc=(acc+delta-out)&0xFFFFFFFF, new_out=asr(new_acc,5) s16 (пары 0x298/0x278/0x27A, 0x288/0x284/0x286, 0x2A0/0x29C/0x29E); % батареи из level=s16[0x1794+12]: >=535→100, <415→0, иначе (level-415)*100//120 в byte[0x306]; главный u32 @0x314++')
def _(run, rng):
    uc = run.uc
    S16 = {0x278, 0x284, 0x29C, 0x27A, 0x286, 0x29E}
    INTEG = [(0x298, 0x278, 0x27A), (0x288, 0x284, 0x286), (0x2A0, 0x29C, 0x29E)]
    # сохранить оригинальные байты 6 bl и патчить в NOP (изоляция inline-логики)
    orig = [bytes(uc.mem_read(FLASH0 + b, 4)) for b in DFD8_BLS]
    try:
        for b in DFD8_BLS:
            uc.mem_write(FLASH0 + b, DFD8_NOP4)

        def seed(off, fmt, v):
            uc.mem_write(RAM + off, struct.pack(fmt, v))

        # --- 20 случайных наборов: интеграторы + счётчики ---
        for _ in range(20):
            seeds = {
                0x2BA: rng.randrange(0, 0xFFFF),
                0x314: rng.randrange(0, 0x1D4CA),
                0x312: rng.randrange(0, 30000),
            }
            for acc_o, del_o, out_o in INTEG:
                seeds[acc_o] = rng.getrandbits(32)
                seeds[del_o] = rng.randrange(-32768, 32767)
                seeds[out_o] = rng.randrange(-32768, 32767)
            for off, v in seeds.items():
                if off in S16:
                    seed(off, '<h', v)
                elif off in (0x2BA, 0x312):
                    seed(off, '<H', v)
                else:
                    seed(off, '<I', v)
            uc.mem_write(RAM + 0x321, b'\x00')   # flag=0 → только инкремент u16[0x312]
            run.call(0x1DFD8, [], max_insn=200000)
            got_tick = struct.unpack_from('<H', uc.mem_read(RAM + 0x2BA, 2), 0)[0]
            assert got_tick == (seeds[0x2BA] + 1) & 0xFFFF, f'tick: {got_tick:#x}'
            got_u32 = struct.unpack_from('<I', uc.mem_read(RAM + 0x314, 4), 0)[0]
            assert got_u32 == seeds[0x314] + 1, f'u32: {got_u32:#x}'
            got_bat = struct.unpack_from('<H', uc.mem_read(RAM + 0x312, 2), 0)[0]
            assert got_bat == seeds[0x312] + 1, f'bat-cnt: {got_bat:#x}'
            for acc_o, del_o, out_o in INTEG:
                ea, eo = ref_dfd8_integ(seeds[acc_o], seeds[del_o], seeds[out_o])
                ga = struct.unpack_from('<I', uc.mem_read(RAM + acc_o, 4), 0)[0]
                go = struct.unpack_from('<h', uc.mem_read(RAM + out_o, 2), 0)[0]
                assert (ga, go) == (ea, eo), (
                    f'integ acc@{acc_o:#x}: exp ({ea},{eo}) got ({ga},{go}) '
                    f'from acc={seeds[acc_o]:#x} d={seeds[del_o]} o={seeds[out_o]}')

        # --- % батареи: принудительный compute (flag=1), линейная карта ---
        for level in [0, 300, 414, 415, 416, 417, 435, 500, 511, 534, 535, 700, 1000, -50]:
            uc.mem_write(RAM + 0x312, struct.pack('<H', 100))   # < 30000
            uc.mem_write(RAM + 0x321, b'\x01')                    # flag=1 → compute
            uc.mem_write(RAM + 0x1794 + 12, struct.pack('<h', level))
            run.call(0x1DFD8, [], max_insn=200000)
            got = uc.mem_read(RAM + 0x306, 1)[0]
            exp = ref_dfd8_batpct(level) & 0xFF
            assert got == exp, f'bat% level={level}: exp {exp} got {got}'
    finally:
        for b, o in zip(DFD8_BLS, orig):
            uc.mem_write(FLASH0 + b, o)


# ---------------------------------------------------------------------------
# §60: 0x1be1c — TIM capture → FOC реконструкция фазных токов (подфункция 0x1A938)
#
# Аргумент: r0 = указатель на struct. Гейт: бит15 низких 16 бит u32[0x40012C54]
# (= TIMER_A+0x14): ==0 → режим 1, ==1 → режим 2.
#
# Режим 1 (гейт положит.): OUT @RAM+0x838/0x83C/0x840 = clamp(r0[+0xc/+0x10/+0x14]).
#
# Режим 2 (гейт отрицат.): dispatch по u16[r0+2] (сектор) через computed-goto
# 0x21b52 (byte jump-table, count=7, idx≥7 → table[7]=null):
#   0→null, 1→B, 2/3→C, 4/5→A, 6→B, ≥7→null.
# Хендлеры (T28/T2C/T30 = u32[0x40012440+0x28/0x2c/0x30], C18/C1A/C1C = u16[r0+0x18/0x1a/0x1c]):
#   A: o_c=(T28-C18)<<4, o_10=(T2C-C1A)<<4, o_14=-(o_c+o_10)
#   B: o_10=(T2C-C1A)<<4, o_14=(T30-C1C)<<4, o_c=-(o_10+o_14)
#   C: o_c=(T28-C18)<<4, o_14=(T30-C1C)<<4, o_10=-(o_c+o_14)
# null: r0[+0xc..] не меняются. Затем OUT = clamp(o_c,o_10,o_14) в [-30000,30000].
# ---------------------------------------------------------------------------

TIMER_A_GATE = 0x40012C54      # u32[0x40012C40+0x14] — гейт (бит15 низких 16)
TIMER_B = 0x40012440           # база таблицы capture (+0x28/+0x2c/+0x30)
FOC_OUT = 0x838                # OUT @RAM+0x838/0x83C/0x840


def ref_foc_clamp(v):
    return max(-30000, min(30000, v))


def ref_1be1c(gate_low16, r0vals, sector, T, C):
    """r0vals=(o_c,o_10,o_14) начальные; T=(T28,T2C,T30); C=(C18,C1A,C1C)"""
    if (gate_low16 & 0x8000) == 0:
        return tuple(ref_foc_clamp(v) for v in r0vals)
    i = sector if sector < 7 else 7
    h = [None, 'B', 'C', 'C', 'A', 'A', 'B', None][i]
    oc, o10, o14 = r0vals
    if h == 'A':
        oc = (T[0] - C[0]) << 4; o10 = (T[1] - C[1]) << 4; o14 = -(oc + o10)
    elif h == 'B':
        o10 = (T[1] - C[1]) << 4; o14 = (T[2] - C[2]) << 4; oc = -(o10 + o14)
    elif h == 'C':
        oc = (T[0] - C[0]) << 4; o14 = (T[2] - C[2]) << 4; o10 = -(oc + o14)
    return ref_foc_clamp(oc), ref_foc_clamp(o10), ref_foc_clamp(o14)


@t(0x1BE1C, '§60: TIM capture → FOC реконструкция фазных токов (подфункция 0x1A938): гейт = бит15 низких16 u32[0x40012C54]; режим1(=0) OUT@RAM+0x838=clamp(r0[+0xc/+0x10/+0x14]); режим2(=1) dispatch u16[r0+2] (0→null,1→B,2/3→C,4/5→A,6→B,≥7→null), хендлер A/B/C: две фазы (T-C)<<4 из u32[0x40012440+{28,2c,30}]-u16[r0+{18,1a,1c}], третья=-(сумма), clamp [-30000,30000]')
def _(run, rng):
    uc = run.uc
    S = 0x1F000   # r0-структ в RAM
    # --- режим 1: гейт положит. (бит15=0), clamp+copy ---
    for _ in range(16):
        gate = rng.getrandbits(16) & 0x7FFF   # бит15=0
        vals = tuple(rng.randrange(-40000, 40000) for _ in range(3))
        uc.mem_write(TIMER_A_GATE, struct.pack('<I', gate & 0xFFFFFFFF))
        uc.mem_write(RAM + S + 0x0c, struct.pack('<i', vals[0]))
        uc.mem_write(RAM + S + 0x10, struct.pack('<i', vals[1]))
        uc.mem_write(RAM + S + 0x14, struct.pack('<i', vals[2]))
        run.call(0x1BE1C, (RAM + S,), max_insn=50000)
        got = tuple(struct.unpack_from('<i', uc.mem_read(RAM + FOC_OUT + i * 4, 4), 0)[0] for i in range(3))
        exp = ref_1be1c(gate, vals, 0, (0, 0, 0), (0, 0, 0))
        assert got == exp, f'режим1: gate={gate:#x} vals={vals} got={got} exp={exp}'
    # --- режим 2: гейт отрицат. (бит15=1), dispatch + хендлеры ---
    for _ in range(40):
        gate = 0x8000 | (rng.getrandbits(16) & 0x7FFF)   # бит15=1
        T = tuple(rng.randrange(0, 2000) for _ in range(3))
        C = tuple(rng.randrange(0, 500) for _ in range(3))
        init = tuple(rng.randrange(-40000, 40000) for _ in range(3))   # для null-кейса
        sector = rng.randrange(0, 9)
        uc.mem_write(TIMER_A_GATE, struct.pack('<I', gate & 0xFFFFFFFF))
        uc.mem_write(TIMER_B + 0x28, struct.pack('<I', T[0]))
        uc.mem_write(TIMER_B + 0x2c, struct.pack('<I', T[1]))
        uc.mem_write(TIMER_B + 0x30, struct.pack('<I', T[2]))
        uc.mem_write(RAM + S + 0x18, struct.pack('<H', C[0] & 0xFFFF))
        uc.mem_write(RAM + S + 0x1a, struct.pack('<H', C[1] & 0xFFFF))
        uc.mem_write(RAM + S + 0x1c, struct.pack('<H', C[2] & 0xFFFF))
        uc.mem_write(RAM + S + 0x0c, struct.pack('<i', init[0]))
        uc.mem_write(RAM + S + 0x10, struct.pack('<i', init[1]))
        uc.mem_write(RAM + S + 0x14, struct.pack('<i', init[2]))
        uc.mem_write(RAM + S + 0x02, struct.pack('<H', sector & 0xFFFF))
        run.call(0x1BE1C, (RAM + S,), max_insn=50000)
        got = tuple(struct.unpack_from('<i', uc.mem_read(RAM + FOC_OUT + i * 4, 4), 0)[0] for i in range(3))
        exp = ref_1be1c(gate, init, sector, T, C)
        assert got == exp, f'режим2: sector={sector} T={T} C={C} init={init} got={got} exp={exp}'


# ---------------------------------------------------------------------------
# §60.1: 0x1e410 — табличная декодировка Q15-вектора (подфункция FOC)
# Аргумент r0 = u32 A. Ветвь b=A[15:14]; i1=(A>>6)&0xFF; i2=(0xFF−i1)&0xFF.
# t1=s16[TBL[i1]], t2=s16[TBL[i2]] (TBL = 256×u16 @flash 0xA6C6). По ветви:
#   b0: lo=−t2, hi=−t1   b1: lo=t1, hi=−t2   b2: lo=t2, hi=t1   b3: lo=−t1, hi=t2
# Возврат u32 = (hi<<16)|lo. (4-квадрантная знаковая инверсия одной пары.)
# ---------------------------------------------------------------------------

FOC_TBL_OFF = 0xA6C6   # flash-offset таблицы 256×u16 (FLASH0 base)


def _foc_tbl(uc):
    raw = uc.mem_read(FLASH0 + FOC_TBL_OFF, 512)
    return list(struct.unpack('<256h', raw))


def ref_1e410(A, tbl):
    b = (A >> 14) & 3
    i1 = (A >> 6) & 0xFF
    i2 = (0xFF - i1) & 0xFF
    t1, t2 = tbl[i1], tbl[i2]
    if b == 0: lo, hi = -t2, -t1
    elif b == 1: lo, hi = t1, -t2
    elif b == 2: lo, hi = t2, t1
    else: lo, hi = -t1, t2
    return ((hi & 0xFFFF) << 16) | (lo & 0xFFFF)


def _s16(v):
    v &= 0xFFFF
    return v - 0x10000 if (v & 0x8000) else v


def _asr32(v, n):
    s = v if (v & 0x80000000) == 0 else (v - 0x100000000)
    return s >> n


def _div15(p):
    """значное деление /2^15 с округлением: if p<0 → p+=0x7FFF; asr 15"""
    pu = p & 0xFFFFFFFF
    if p < 0:
        pu = (pu + 0x7FFF) & 0xFFFFFFFF
    return _asr32(pu, 15)


def ref_1d7ac(arg0, arg1, tbl):
    """cross+dot двух Q15-векторов: X=0x1e410(arg1), A=arg0."""
    X = ref_1e410(arg1, tbl)
    X_lo, X_hi = _s16(X), _s16(X >> 16)
    a_lo, a_hi = _s16(arg0), _s16(arg0 >> 16)
    P = _div15(X_hi * a_lo)   # a_lo·X_hi
    Q = _div15(X_lo * a_hi)   # a_hi·X_lo
    R = _div15(X_lo * a_lo)   # a_lo·X_lo
    S = _div15(X_hi * a_hi)   # a_hi·X_hi
    out_lo = (Q - P) & 0xFFFF   # cross: a_hi·X_lo − a_lo·X_hi
    out_hi = (R + S) & 0xFFFF   # dot:   a_lo·X_lo + a_hi·X_hi
    return (out_hi << 16) | out_lo


@t(0x1E410, '§60.1: табличная декодировка Q15-вектора (подфункция FOC): ветвь=A[15:14], i1=(A>>6)&0xFF, i2=~i1&0xFF; t1/t2=s16[TBL@flash0xA6C6[i]]; b0:(−t2,−t1) b1:(t1,−t2) b2:(t2,t1) b3:(−t1,t2) → u32=(hi<<16)|lo')
def _(run, rng):
    tbl = _foc_tbl(run.uc)
    for _ in range(60):
        A = rng.getrandbits(32)
        r0, _ = run.call(0x1E410, (A,), max_insn=50000)
        exp = ref_1e410(A, tbl)
        assert r0 == exp, f'0x1e410: A={A:#010x} got={r0:#010x} exp={exp:#010x}'


@t(0x1D7AC, '§60.1: cross+dot двух Q15-векторов (подфункция FOC): X=0x1e410(arg1), A=arg0; lo=cross(a_hi·X_lo−a_lo·X_hi), hi=dot(a_lo·X_lo+a_hi·X_hi); каждое произведение /2^15 с округлением (p<0→+0x7FFF)')
def _(run, rng):
    tbl = _foc_tbl(run.uc)
    for _ in range(60):
        a0 = rng.getrandbits(32); a1 = rng.getrandbits(32)
        r0, _ = run.call(0x1D7AC, (a0, a1), max_insn=50000)
        exp = ref_1d7ac(a0, a1, tbl)
        assert r0 == exp, f'0x1d7ac: a0={a0:#010x} a1={a1:#010x} got={r0:#010x} exp={exp:#010x}'


# ---------------------------------------------------------------------------
# §60.2: 0x1bd88 — 6-секторный FOC-классификатор (подфункция 0x1A938)
# Аргументы: arg0=r0 = struct вывода (u16[r0+2]=сектор), arg1=r1 = указатель на
# два s16: x0=s16[r1+0], x2=s16[r1+2]. Гейт: бит15 низких16 u32[0x40012C54]
# (TIMER_A+0x14, тот же что в 0x1be1c): ==0 → обход (сектор не пишется).
# A=0x3ce4, B=0x2328 (pool). S=rnd((B·x2+A·x0)/2), D=rnd((B·x2−A·x0)/2),
# rnd(V)=(V−1 if V<0 else V)>>1; r2=B·x2. Сектор по знакам:
#   S<0,D<0→5 ; S<0,D≥0→(3 if r2>0 else 4) ; S≥0,D<0→(1 if r2>0 else 6) ; S≥0,D≥0→2
# ---------------------------------------------------------------------------

BD88_GATE = 0x40012C54   # TIMER_A + 0x14 (гейт, бит15 низких 16)
BD88_A = 0x3CE4
BD88_B = 0x2328


def _rnd2(V):
    if V < 0:
        V -= 1
    return _asr32(V & 0xFFFFFFFF, 1)


def ref_1bd88(gate_low16, x0, x2):
    """вернёт сектор (1..6) или None если гейт положит. (обход)"""
    if (gate_low16 & 0x8000) == 0:
        return None
    S = _rnd2(BD88_B * x2 + BD88_A * x0)
    D = _rnd2(BD88_B * x2 - BD88_A * x0)
    r2 = BD88_B * x2
    if S < 0:
        return 5 if D < 0 else (3 if r2 > 0 else 4)
    else:
        return 1 if (D < 0 and r2 > 0) else (6 if D < 0 else 2)


@t(0x1BD88, '§60.2: 6-секторный FOC-классификатор (подфункция 0x1A938): гейт=бит15 низких16 u32[0x40012C54] (=0→обход); x0=s16[r1+0], x2=s16[r1+2]; S=rnd((B·x2+A·x0)/2), D=rnd((B·x2−A·x0)/2) A=0x3ce4 B=0x2328 rnd(V)=(V−1 if V<0 else V)>>1; u16[r0+2]=сектор: S<0,D<0→5 / S<0,D≥0→(r2>0?3:4) / S≥0,D<0→(r2>0?1:6) / S≥0,D≥0→2, r2=B·x2')
def _(run, rng):
    uc = run.uc
    S_IN = 0x1F000; S_OUT = 0x1F100
    for _ in range(60):
        gate = rng.getrandbits(16)
        x0 = rng.randrange(-400, 400); x2 = rng.randrange(-400, 400)
        uc.mem_write(BD88_GATE, struct.pack('<I', gate))
        uc.mem_write(RAM + S_IN + 0, struct.pack('<h', x0))
        uc.mem_write(RAM + S_IN + 2, struct.pack('<h', x2))
        uc.mem_write(RAM + S_OUT + 2, struct.pack('<H', 0xEEEE))   # sentinel
        run.call(0x1BD88, (RAM + S_OUT, RAM + S_IN), max_insn=50000)
        got = struct.unpack_from('<H', uc.mem_read(RAM + S_OUT + 2, 2), 0)[0]
        exp = ref_1bd88(gate, x0, x2)
        if exp is None:
            assert got == 0xEEEE, f'обход: gate={gate:#06x} x0={x0} x2={x2} got={got:#06x}'
        else:
            assert got == exp, f'сектор: gate={gate:#06x} x0={x0} x2={x2} got={got} exp={exp}'


# ---------------------------------------------------------------------------
# §60.3: 0x1d818 — cross+dot (двойник 0x1d7ac, но X из RAM, не из таблицы)
# Аргумент: arg0=r0 = A=(a_lo,a_hi) Q15. Вектор X = (X_lo,X_hi) из RAM:
#   X_lo=s16[RAM+0x10c], X_hi=s16[RAM+0x10e] (база r6 = pool @flash 0x1d870).
# Вычисление идентично 0x1d7ac: lo=cross(a_hi·X_lo−a_lo·X_hi), hi=dot(a_lo·X_lo
# +a_hi·X_hi); каждое произведение /2^15 с округлением (p<0→+0x7FFF).
# ---------------------------------------------------------------------------

D818_XLO = 0x10C   # RAM-offset X_lo
D818_XHI = 0x10E   # RAM-offset X_hi


def ref_1d818(arg0, X_lo, X_hi):
    a_lo, a_hi = _s16(arg0), _s16(arg0 >> 16)
    P = _div15(X_hi * a_lo); Q = _div15(X_lo * a_hi)
    R = _div15(X_lo * a_lo); S = _div15(X_hi * a_hi)
    return ((R + S) & 0xFFFF) << 16 | ((Q - P) & 0xFFFF)


@t(0x1D818, '§60.3: cross+dot (двойник 0x1d7ac, X из RAM): A=arg0 Q15, X=(s16[RAM+0x10c], s16[RAM+0x10e]); lo=cross(a_hi·X_lo−a_lo·X_hi), hi=dot(a_lo·X_lo+a_hi·X_hi); каждое /2^15 с округлением')
def _(run, rng):
    uc = run.uc
    for _ in range(60):
        arg0 = rng.getrandbits(32)
        X_lo = rng.randrange(-300, 300); X_hi = rng.randrange(-300, 300)
        uc.mem_write(RAM + D818_XLO, struct.pack('<h', X_lo))
        uc.mem_write(RAM + D818_XHI, struct.pack('<h', X_hi))
        r0, _ = run.call(0x1D818, (arg0,), max_insn=50000)
        exp = ref_1d818(arg0, X_lo, X_hi)
        assert r0 == exp, f'0x1d818: arg0={arg0:#010x} X=({X_lo},{X_hi}) got={r0:#010x} exp={exp:#010x}'


# ---------------------------------------------------------------------------
# §60.4: 0x1b3f2..0x1b460 — inline-блок FOC (inlined cross+dot) внутри 0x1A938
# Входы (по трассировке, НЕ capstone pool-offsets): P=u32[RAM+0x388],
# X_lo=s16[RAM+0x108], X_hi=s16[RAM+0x10a], R6=u32[RAM+0x3ac]. r4=RAM+0x040 (struct).
# Вычисления (muls + asrs#15):
#   cross = asr15(R6·X_hi) − asr15(P·X_lo)      → RAM+0x3b8
#   dot   = asr15(R6·X_lo) + asr15(P·X_hi)      → RAM+0x3bc
#   t1 = −(dot<<14)
#   r4+0x1c = asr15(t1 + 0x6ed9·cross)
#   r4+0x20 = asr15(t1 − 0x6ed9·cross)
#   r4+0x28 = dot>>1
#   r4+0x24 = asr15(0x376d·cross + (dot<<13))
# (тот же комплексный произведение, что 0x1d7ac/0x1d818, но inline)
# Верификация: mid-function jump в 0x1b3f2 с r4=RAM+0x040, stop в 0x1b48a.
# ---------------------------------------------------------------------------


def _asr15(v):
    s = v if (v & 0x80000000) == 0 else (v - 0x100000000)
    return s >> 15


def ref_1b3f2(P, X_lo, X_hi, R6):
    cross = _asr15((R6 * X_hi) & 0xFFFFFFFF) - _asr15((P * X_lo) & 0xFFFFFFFF)
    dot = _asr15((R6 * X_lo) & 0xFFFFFFFF) + _asr15((P * X_hi) & 0xFFFFFFFF)
    t1 = -(dot << 14)
    out = [cross, dot,
           _asr15((t1 + 0x6ED9 * cross) & 0xFFFFFFFF),
           _asr15((t1 - 0x6ED9 * cross) & 0xFFFFFFFF),
           dot >> 1,
           _asr15((0x376D * cross + (dot << 13)) & 0xFFFFFFFF)]
    return out


@t(0x1B3F2, '§60.4: inline-блок FOC в 0x1A938 (inlined cross+dot): P=u32[RAM+0x388], X_lo=s16[RAM+0x108], X_hi=s16[RAM+0x10a], R6=u32[RAM+0x3ac]; cross=asr15(R6·Xhi)−asr15(P·Xlo)→RAM+0x3b8, dot=asr15(R6·Xlo)+asr15(P·Xhi)→RAM+0x3bc; r4+0x1c/0x20=asr15(∓t1±0x6ed9·cross), r4+0x28=dot>>1, r4+0x24=asr15(0x376d·cross+dot<<13); верификация mid-function jump (r4=RAM+0x040, stop 0x1b48a)')
def _(run, rng):
    uc = run.uc
    for _ in range(40):
        P = rng.getrandbits(32) & 0x7FFFFFFF
        X_lo = rng.randrange(-500, 500); X_hi = rng.randrange(-500, 500)
        R6 = rng.getrandbits(20)
        uc.mem_write(RAM, bytes(0x20000))
        uc.mem_write(RAM + 0x388, struct.pack('<I', P))
        uc.mem_write(RAM + 0x108, struct.pack('<h', X_lo))
        uc.mem_write(RAM + 0x10a, struct.pack('<h', X_hi))
        uc.mem_write(RAM + 0x3ac, struct.pack('<i', R6))
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R4, RAM + 0x040)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1B3F2 | 1, 0x1B48A | 1, count=200)
        except UcError:
            pass
        got = [struct.unpack_from('<i', uc.mem_read(RAM + o, 4), 0)[0]
               for o in (0x3b8, 0x3bc, 0x5c, 0x60, 0x68, 0x64)]
        exp = ref_1b3f2(P, X_lo, X_hi, R6)
        assert got == exp, f'0x1b3f2: P={P} Xlo={X_lo} Xhi={X_hi} R6={R6} got={got} exp={exp}'


# ---------------------------------------------------------------------------
# §60.5: 0x1aa08..0x1aae6 — inline-блок FOC в 0x1A938: обработка/кламп моторных
# параметров + leaky-интегратор. Зависит от live-in регистров (r4=RAM+0x040 base,
# r5=RAM+0x108, r6=0x2033) и stack-frame ([sp+0x18]=base). Изоляция: mid-function
# jump в 0x1aa08 с этими регистрами + [sp+0x18]=RAM+0x040, stop в 0x1abd4.
# Верифицированные операции (ключевые из ~13 выходов):
#   (1) u16[RAM+0x044] = lo16(r0)          — store результата cross+dot (из bl 0x1d7ac)
#   (2) u16[RAM+0x38c] = clamp(−s16[RAM+0x0a6], ±s16[RAM+0x390])  — симм. кламп
#   (3) leaky-интегратор: acc=u32[RAM+0x094] (new=acc+delta−old_out),
#       u16[RAM+0x046] = asr(acc_new, 5)   — тот же паттерн, что 0x1DFD8 (§59.8)
# ---------------------------------------------------------------------------


def _asr5(v):
    s = v if (v & 0x80000000) == 0 else (v - 0x100000000)
    return s >> 5


@t(0x1AA08, '§60.5: inline-блок FOC в 0x1A938 — обработка/кламп параметров + leaky-интегратор. (1) u16[RAM+0x044]=lo16(r0=cross+dot); (2) u16[RAM+0x38c]=clamp(−s16[RAM+0x0a6],±s16[RAM+0x390]); (3) интегратор acc=u32[RAM+0x094]: u16[RAM+0x046]=asr(acc_new,5) (паттерн 0x1DFD8). Изоляция mid-function jump (r4=RAM+0x040, r5=RAM+0x108, r6=0x2033, [sp+0x18]=RAM+0x040, stop 0x1abd4)')
def _(run, rng):
    uc = run.uc
    for _ in range(60):
        r0val = rng.getrandbits(32)
        a0a6 = rng.randrange(-1000, 1000); limit = rng.randrange(1, 800); acc0 = rng.getrandbits(24)
        uc.mem_write(RAM, bytes(0x20000))
        uc.mem_write(RAM + 0x0a6, struct.pack('<h', a0a6))
        uc.mem_write(RAM + 0x390, struct.pack('<h', limit))
        uc.mem_write(RAM + 0x094, struct.pack('<i', acc0))
        SP = 0x20017F00
        uc.mem_write(SP + 0x18, struct.pack('<I', RAM + 0x040))
        uc.reg_write(UC_ARM_REG_SP, SP)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R0, r0val)
        uc.reg_write(UC_ARM_REG_R4, RAM + 0x040)
        uc.reg_write(UC_ARM_REG_R5, RAM + 0x108)
        uc.reg_write(UC_ARM_REG_R6, 0x2033)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1AA08 | 1, 0x1ABD4 | 1, count=200)
        except UcError:
            pass
        o44 = struct.unpack_from('<H', uc.mem_read(RAM + 0x044, 2), 0)[0]
        o38c = struct.unpack_from('<H', uc.mem_read(RAM + 0x38c, 2), 0)[0]
        o94 = struct.unpack_from('<i', uc.mem_read(RAM + 0x094, 4), 0)[0]
        o46 = struct.unpack_from('<H', uc.mem_read(RAM + 0x046, 2), 0)[0]
        assert o44 == (r0val & 0xFFFF), f'0x1aa08(1): r0={r0val:#x} got={o44} exp={r0val&0xFFFF}'
        cv = max(-limit, min(limit, -a0a6))
        assert o38c == (cv & 0xFFFF), f'0x1aa08(2): a0a6={a0a6} limit={limit} got={o38c} exp={cv&0xFFFF}'
        assert o46 == (_asr5(o94) & 0xFFFF), f'0x1aa08(3): acc={o94} got_out={o46} exp={_asr5(o94)&0xFFFF}'


# ---------------------------------------------------------------------------
# §60.6: 0x1b48a..0x1b5f4 — inline-блок FOC в 0x1A938: коммутация/классификатор
# секторов. Входы: v2c=u32[r4+0x2c], v30=u32[r4+0x30], v34=u32[r4+0x34] (значения из
# блока 0x1b3f2). Порог = 16383 (0x3fff): если все ≤ порога — pass-through
# (r4+0x38=v2c, r4+0x3c=v30, r4+0x40=v34); иначе секторная логика: определяется
# максимум из (v2c,v30,v34) = сектор, считается switching-функция.
# Верифицировано: default pass-through + v2c-max сектор:
#   r4+0x38 = 16383, r4+0x3c = min(v30 − asr(v2c,1) + 8192, 16383), r4+0x40 = r1
# Изоляция: mid-function jump (r4=RAM+0x040, r7=RAM+0x3b8, [sp+0x18]=base, stop 0x1b584).
# ---------------------------------------------------------------------------


@t(0x1B48A, '§60.6: inline-блок FOC в 0x1A938 — коммутация/классификатор секторов. Входы v2c/v30/v34=u32[r4+0x2c/0x30/0x34]; порог 16383. Default (все≤порога): pass-through r4+0x38=v2c,0x3c=v30,0x40=v34. v2c-max сектор: r4+0x38=16383, r4+0x3c=min(v30−asr(v2c,1)+8192,16383), r4+0x40=r1. Изоляция mid-function jump (stop 0x1b584)')
def _(run, rng):
    uc = run.uc
    def run_sector(v2c, v30, v34, r1):
        uc.mem_write(RAM, bytes(0x20000))
        r4 = RAM + 0x040
        for o, v in ((0x2c, v2c), (0x30, v30), (0x34, v34)):
            uc.mem_write(r4 + o, struct.pack('<i', v))
        SP = 0x20017F00
        uc.mem_write(SP + 0x18, struct.pack('<I', r4))
        uc.reg_write(UC_ARM_REG_SP, SP)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R4, r4)
        uc.reg_write(UC_ARM_REG_R1, r1)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1B48A | 1, 0x1B584 | 1, count=200)
        except UcError:
            pass
        return (struct.unpack_from('<i', uc.mem_read(r4 + 0x38, 4), 0)[0],
                struct.unpack_from('<i', uc.mem_read(r4 + 0x3c, 4), 0)[0],
                struct.unpack_from('<i', uc.mem_read(r4 + 0x40, 4), 0)[0])
    for _ in range(40):
        # default path: все значения ≤ порога
        v2c = rng.randrange(-16000, 16000); v30 = rng.randrange(-16000, 16000)
        v34 = rng.randrange(-16000, 16000)
        a, b, c = run_sector(v2c, v30, v34, 0)
        assert (a, b, c) == (v2c, v30, v34), f'0x1b48a default: ({v2c},{v30},{v34})->({a},{b},{c})'
    for _ in range(40):
        # v2c-max сектор: v2c > порога и v2c>=v30>=v34
        v2c = rng.randrange(17000, 30000); v30 = v2c - rng.randrange(0, 4000)
        v34 = v30 - rng.randrange(0, 4000); r1 = rng.getrandbits(16)
        a, b, c = run_sector(v2c, v30, v34, r1)
        e38 = 16383; e3c = min(v30 - (v2c >> 1) + 8192, 16383); e40 = r1
        assert (a, b, c) == (e38, e3c, e40), f'0x1b48a v2cmax: ({v2c},{v30},{v34},r1={r1})->({a},{b},{c}) exp=({e38},{e3c},{e40})'


# ---------------------------------------------------------------------------
# §60.7: мелкие inline-фрагменты 0x1A938 (между крупными блоками)
# (a) 0x1b470..0x1b488 — вычисление v2c/v30/v34 (входы блока 3) из r0/r1/r2:
#       if r0<=r2: (v2c,v30,v34)=(r1, r2−r0, −r0)  else: (r0−r2, r1, −r2)
#     (связка блок 1 cross+dot → блок 3 коммутация)
# (b) 0x1b584..0x1b5e2 — хвост: масштабирование выходов блока 3 + offset + фазы:
#       svX=asr15(4500·vX) → r4+0x44/0x48/0x4c (V38/V3C/V40); pool-константа 4500
#       offset=r4+0x50=asr1(2250−max(sv)); фазы u16[RAM+0x382/0x384/0x386]=2250−(svX+offset)
# ---------------------------------------------------------------------------


def _s32(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if (v & 0x80000000) else v


def _asr(v, n):
    return _s32(v) >> n


@t(0x1B470, '§60.7a: inline-фрагмент 0x1A938 — вычисление v2c/v30/v34 (входы блока 3) из r0/r1/r2: if r0<=r2: (v2c,v30,v34)=(r1,r2−r0,−r0) else: (r0−r2,r1,−r2). Изоляция mid-function jump (r4=RAM+0x040, stop 0x1b492)')
def _(run, rng):
    uc = run.uc
    for _ in range(80):
        r0 = rng.randrange(-50000, 50000); r1 = rng.randrange(-50000, 50000)
        r2 = rng.randrange(-50000, 50000)
        uc.mem_write(RAM, bytes(0x20000))
        r4 = RAM + 0x040
        SP = 0x20017F00
        uc.mem_write(SP + 0x18, struct.pack('<I', r4))
        from unicorn import UC_HOOK_CODE as _H
        def _st(uc_, addr, size, u):
            a = addr & ~1
            if a >= 0x1B492 or not (FLASH0 <= a < FLASH0 + FW_LEN or 0x08000000 <= a < 0x08000000 + FW_LEN):
                uc_.emu_stop()
        sh = uc.hook_add(_H, _st)
        uc.reg_write(UC_ARM_REG_SP, SP); uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R4, r4)
        uc.reg_write(UC_ARM_REG_R0, r0 & 0xFFFFFFFF); uc.reg_write(UC_ARM_REG_R1, r1 & 0xFFFFFFFF)
        uc.reg_write(UC_ARM_REG_R2, r2 & 0xFFFFFFFF)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1B470 | 1, 0, count=15)
        except UcError:
            pass
        uc.hook_del(sh)
        got = (struct.unpack_from('<i', uc.mem_read(r4 + 0x2c, 4), 0)[0],
               struct.unpack_from('<i', uc.mem_read(r4 + 0x30, 4), 0)[0],
               struct.unpack_from('<i', uc.mem_read(r4 + 0x34, 4), 0)[0])
        exp = (r1, r2 - r0, -r0) if _s32(r0) <= _s32(r2) else (r0 - r2, r1, -r2)
        assert got == exp, f'0x1b470: r0={r0} r1={r1} r2={r2} got={got} exp={exp}'


@t(0x1B584, '§60.7b: inline-фрагмент 0x1A938 — хвост: svX=asr15(4500·vX)→r4+0x44/0x48/0x4c; offset=r4+0x50=asr1(2250−max(sv)); фазы u16[RAM+0x382/0x384/0x386]=2250−(svX+offset). Изоляция mid-function jump (r4=RAM+0x040, stop 0x1b5e4)')
def _(run, rng):
    uc = run.uc
    for _ in range(80):
        v38 = rng.randrange(-20000, 20000); v3c = rng.randrange(-20000, 20000)
        v40 = rng.randrange(-20000, 20000)
        uc.mem_write(RAM, bytes(0x20000))
        r4 = RAM + 0x040
        for o, v in ((0x38, v38), (0x3c, v3c), (0x40, v40)):
            uc.mem_write(r4 + o, struct.pack('<i', v))
        SP = 0x20017F00
        uc.mem_write(SP + 0x18, struct.pack('<I', r4))
        from unicorn import UC_HOOK_CODE as _H
        def _st(uc_, addr, size, u):
            a = addr & ~1
            if a >= 0x1B5E4 or not (FLASH0 <= a < FLASH0 + FW_LEN or 0x08000000 <= a < 0x08000000 + FW_LEN):
                uc_.emu_stop()
        sh = uc.hook_add(_H, _st)
        uc.reg_write(UC_ARM_REG_SP, SP); uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R4, r4)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1B584 | 1, 0, count=60)
        except UcError:
            pass
        uc.hook_del(sh)
        o44 = struct.unpack_from('<i', uc.mem_read(r4 + 0x44, 4), 0)[0]
        o48 = struct.unpack_from('<i', uc.mem_read(r4 + 0x48, 4), 0)[0]
        o4c = struct.unpack_from('<i', uc.mem_read(r4 + 0x4c, 4), 0)[0]
        o50 = struct.unpack_from('<i', uc.mem_read(r4 + 0x50, 4), 0)[0]
        qa = struct.unpack_from('<H', uc.mem_read(RAM + 0x382, 2), 0)[0]
        qb = struct.unpack_from('<H', uc.mem_read(RAM + 0x384, 2), 0)[0]
        qc = struct.unpack_from('<H', uc.mem_read(RAM + 0x386, 2), 0)[0]
        sv38 = _asr(4500 * v38, 15); sv3c = _asr(4500 * v3c, 15); sv40 = _asr(4500 * v40, 15)
        e50 = _asr(2250 - max(sv38, sv3c, sv40), 1)
        assert (o44, o48, o4c, o50) == (sv38, sv3c, sv40, e50), \
            f'0x1b584 scale: v=({v38},{v3c},{v40}) got=({o44},{o48},{o4c},{o50}) exp=({sv38},{sv3c},{sv40},{e50})'
        exp_q = ((2250 - (sv38 + e50)) & 0xFFFF, (2250 - (sv3c + e50)) & 0xFFFF, (2250 - (sv40 + e50)) & 0xFFFF)
        assert (qa, qb, qc) == exp_q, \
            f'0x1b584 phase: v=({v38},{v3c},{v40}) got=({qa},{qb},{qc}) exp={exp_q}'


@t(0x1A9F2, '§60.7c: inline-фрагмент 0x1A938 — pre-block-2 frame setup: base=pool(RAM+0x40), [sp+0x18]=base+0x60=RAM+0xa0, [sp+4]=u16[RAM+0xa0], [sp+6]=u16[RAM+0xa2] (затем bl 0x1d7ac). Изоляция mid-function jump (stop 0x1aa04)')
def _(run, rng):
    uc = run.uc
    for _ in range(50):
        a = rng.getrandbits(16); b = rng.getrandbits(16)
        uc.mem_write(RAM, bytes(0x20000))
        uc.mem_write(RAM + 0xa0, struct.pack('<H', a)); uc.mem_write(RAM + 0xa2, struct.pack('<H', b))
        SP = 0x20017F00
        from unicorn import UC_HOOK_CODE as _H
        def _st(uc_, addr, size, u):
            aa = addr & ~1
            if aa >= 0x1AA04 or not (FLASH0 <= aa < FLASH0 + FW_LEN or 0x08000000 <= aa < 0x08000000 + FW_LEN):
                uc_.emu_stop()
        sh = uc.hook_add(_H, _st)
        uc.reg_write(UC_ARM_REG_SP, SP); uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1A9F2 | 1, 0, count=12)
        except UcError:
            pass
        uc.hook_del(sh)
        s18 = struct.unpack_from('<I', uc.mem_read(SP + 0x18, 4), 0)[0]
        s4 = struct.unpack_from('<H', uc.mem_read(SP + 4, 2), 0)[0]
        s6 = struct.unpack_from('<H', uc.mem_read(SP + 6, 2), 0)[0]
        assert (s18, s4, s6) == (RAM + 0xa0, a, b), \
            f'0x1a9f2: a={a} b={b} got=({s18:#x},{s4},{s6}) exp={(RAM+0xa0,a,b)}'


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
