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

from emulator.mcu_emu import McuEmu, SpeedModel, FLASH0, FLASH1, RAM, STACK_TOP

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

@t(0xE740, 'drift detector: devA=|u16[RAM+0x13AB]−u16[RAM+0x130A]|; devB=min(|s16[RAM+0x13A4]−s16[RAM+0x1302]|,0x7fff) (абсолютное!); devA≥500||devB>500 → flag + refs:=текущие')
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
    devB = min(abs(B - refB), 0x7FFF)   # firmware: |B−refB| (абсолютное), clamp 32767
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
# §60.8: 0x1A938 entry (0x1a938..0x1a9d0) — prologue + setup + табличная выборка.
# (a) Табличная выборка (главный расчёт), вход s16[r4+2]=value, таблица E в flash
#     @0x9E38 (2048 u16). Треугольный mapping:
#       idx = value>>4  (value<16384)  |  1023−(value−16384)>>4  (value>=16384)
#       u16[r4+4]=idx;  u16[RAM+0x108]=tableE[idx];
#       r0 = tableE[1024−idx] (value<16384)  |  −tableE[1024−idx] (value>=16384)
#     (branch C неактивен — branch B покрывает весь верхний диапазон [16384,32767])
# (b) scaled-delta: u16[r4+0x60]=u16[poolC=RAM+0x838],
#     u16[r4+0x62]=asr16(0x93cc·(u32[poolC+4]−u32[poolC+8]))
# (bl 0x1be1c — уже верифицированная подфункция)
# ---------------------------------------------------------------------------

_ENTRY_TBL_BASE = 0x9E38   # flash-таблица E
_ENTRY_TBL = None          # кэш: список 2048 u16


def _entry_table():
    global _ENTRY_TBL
    if _ENTRY_TBL is None:
        with open(r'D:/SCOOTER_5_PRO/research/images/mcu_0007.bin', 'rb') as f:
            img = bytearray(f.read())
        _ENTRY_TBL = [struct.unpack_from('<H', img, _ENTRY_TBL_BASE + i * 2)[0]
                      for i in range(2048)]
    return _ENTRY_TBL


@t(0x1A938, '§60.8: entry 0x1A938 — табличная выборка (треугольный mapping по flash-таблице @0x9E38): idx=value>>4 | 1023−(value−16384)>>4; u16[r4+4]=idx, u16[RAM+0x108]=tableE[idx], r0=±tableE[1024−idx]; + scaled-delta u16[r4+0x62]=asr16(0x93cc·delta). Изоляция mid-function jump (r4=RAM+0x040)')
def _(run, rng):
    uc = run.uc
    tbl = _entry_table()
    # (a) табличная выборка — полный диапазон value [0, 32767]
    for _ in range(150):
        val = rng.randrange(0, 32768)
        uc.mem_write(RAM, bytes(0x20000))
        r4 = RAM + 0x040
        uc.mem_write(r4 + 2, struct.pack('<h', val))
        from unicorn import UC_HOOK_CODE as _H
        def _st(uc_, addr, size, u):
            aa = addr & ~1
            if aa >= 0x1A9D0 or not (FLASH0 <= aa < FLASH0 + FW_LEN or 0x08000000 <= aa < 0x08000000 + FW_LEN):
                uc_.emu_stop()
        sh = uc.hook_add(_H, _st)
        uc.reg_write(UC_ARM_REG_SP, 0x20017F00); uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R4, r4)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1A966 | 1, 0, count=30)
        except UcError:
            pass
        uc.hook_del(sh)
        idx_got = struct.unpack_from('<H', uc.mem_read(r4 + 4, 2), 0)[0]
        b_got = struct.unpack_from('<H', uc.mem_read(RAM + 0x108, 2), 0)[0]
        r0_got = uc.reg_read(UC_ARM_REG_R0) & 0xFFFF
        if val < 16384:
            idx = val >> 4; neg = False
        else:
            idx = 1023 - ((val - 16384) >> 4); neg = True
        e_b = tbl[idx]
        e_r0 = (-tbl[1024 - idx]) & 0xFFFF if neg else tbl[1024 - idx]
        assert (idx_got, b_got, r0_got) == (idx, e_b, e_r0), \
            f'0x1a938 table: val={val} got=({idx_got},{b_got},{r0_got}) exp=({idx},{e_b},{e_r0})'
    # (b) scaled-delta
    POOLC = RAM + 0x838; POOLD = 0x93CC
    for _ in range(50):
        c0 = rng.getrandbits(16); c4 = rng.getrandbits(32); c8 = rng.getrandbits(32)
        uc.mem_write(RAM, bytes(0x20000))
        uc.mem_write(POOLC + 0, struct.pack('<H', c0))
        uc.mem_write(POOLC + 4, struct.pack('<I', c4)); uc.mem_write(POOLC + 8, struct.pack('<I', c8))
        r4 = RAM + 0x040
        def _st2(uc_, addr, size, u):
            aa = addr & ~1
            if aa >= 0x1A966 or not (FLASH0 <= aa < FLASH0 + FW_LEN or 0x08000000 <= aa < 0x08000000 + FW_LEN):
                uc_.emu_stop()
        sh2 = uc.hook_add(_H, _st2)
        uc.reg_write(UC_ARM_REG_SP, 0x20017F00); uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R4, r4)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1A94E | 1, 0, count=12)
        except UcError:
            pass
        uc.hook_del(sh2)
        o60 = struct.unpack_from('<H', uc.mem_read(r4 + 0x60, 2), 0)[0]
        o62 = struct.unpack_from('<H', uc.mem_read(r4 + 0x62, 2), 0)[0]
        delta = (c4 - c8) & 0xFFFFFFFF
        e62 = (_s32(POOLD * delta) >> 16) & 0xFFFF
        assert (o60, o62) == (c0, e62), \
            f'0x1a938 delta: c0={c0} c4={c4:#x} c8={c8:#x} got=({o60},{o62}) exp=({c0},{e62})'


# ---------------------------------------------------------------------------
# §61: оставшиеся некаталогизированные функции (досмотр карты)
# 0x11bac — форматтер даты/времени: total-seconds → байты через цепочку остатков.
# Аргументы: arg0=r0=out-буфер, arg1=r1=total seconds. Дивизоры [31104000,2592000,
# 86400,3600,60] (≈360d-год, 30d-месяц, день, час, минута):
#   out[0]=v//31104000; out[i]=(v%D[i-1])//D[i]; out[5]=v%60
# ---------------------------------------------------------------------------

_FMT_D = [31104000, 2592000, 86400, 3600, 60]


def ref_11bac(v):
    out = [(v // _FMT_D[0]) & 0xFF]
    for i in range(1, len(_FMT_D)):
        out.append(((v % _FMT_D[i - 1]) // _FMT_D[i]) & 0xFF)
    out.append((v % _FMT_D[-1]) & 0xFF)
    return out


@t(0x11BAC, '§61: форматтер даты/времени — total-seconds → байты (цепочка остатков, дивизоры [31104000,2592000,86400,3600,60] ≈ 360d-год/30d-месяц/день/час/мин/сек): out[0]=v//D0, out[i]=(v%D[i-1])//D[i], out[5]=v%60')
def _(run, rng):
    uc = run.uc
    OUT = RAM + 0x300
    for _ in range(100):
        v = rng.getrandbits(26)
        uc.mem_write(RAM, bytes(0x20000))
        from unicorn import UC_HOOK_CODE as _H
        def _st(uc_, addr, size, u):
            a = addr & ~1
            if a >= 0x11C2E or not (FLASH0 <= a < FLASH0 + FW_LEN or 0x08000000 <= a < 0x08000000 + FW_LEN):
                uc_.emu_stop()
        sh = uc.hook_add(_H, _st)
        uc.reg_write(UC_ARM_REG_SP, 0x20017F00); uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R0, OUT); uc.reg_write(UC_ARM_REG_R1, v)
        run.emu.insn = 0
        try:
            uc.emu_start(0x11BAC | 1, 0, count=80)
        except UcError:
            pass
        uc.hook_del(sh)
        got = list(bytes(uc.mem_read(OUT, 6)))
        exp = ref_11bac(v)
        assert got == exp, f'0x11bac: v={v} got={got} exp={exp}'


# --- 0x1d078 timer capture/period + speed-limit ramp (§69, corrected by random-sweep) ---
def _sdiv(a, b):
    if b == 0:
        return 0
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q
def _s16(x):
    x &= 0xFFFF
    return x - 0x10000 if x >= 0x8000 else x

@t(0x1D078, '§69: val=s16(sdiv(48000,V)) if F=byte[RAM+0x100]!=0 else 0; struct r4=RAM+0x1768: [+0]=u16(val), 2 leaky-интегратора (asr5 / asr3 clamp≥0) → out1=s16[+0x10], out2=s16[+8]; pct=u16[RAM+0x236]=sdiv(100*out2,208); mode-target: flag=byte[RAM+0x339]==1→522 / mode@0x229 0xb→125/2→u16@0x324/3→u16@0x326/else→208; struct[+0x14]=target if s16(target)<=u16[RAM+0x326] else u16[RAM+0x326] (signed clamp); structB@0x3c8[+0x2a]=target = setpoint замкнутого контура скорости (out2=сглаж. оценка ∝ 48000/V; вывод r4[+0x18]=structB[+0x64]=throttle/duty, НЕ скорость). Вериф. 200/200 random-sweep + setpoint 300/300')
def _(run, rng):
    V = rng.randint(50, 60000)
    F = rng.getrandbits(1)
    acc1 = rng.getrandbits(32); out1 = rng.randint(-32768, 32767)
    acc2 = rng.getrandbits(32); out2 = rng.randint(-32768, 32767)
    mode = rng.choice([2, 3, 0xb, 5, 7])
    f339 = rng.getrandbits(16)   # flag = low byte @0x339
    c326 = rng.getrandbits(16)   # u16[RAM+0x326] (clamp-значение)
    m2t  = rng.getrandbits(16)   # u16[RAM+0x324] (target при mode==2)
    run.ram_write(0x158, struct.pack('<I', V))
    run.ram_write(0x100, bytes([F]))
    run.ram_write(0x1768, struct.pack('<H', 0))
    run.ram_write(0x176c, struct.pack('<I', acc2))
    run.ram_write(0x1770, struct.pack('<h', out2))
    run.ram_write(0x1774, struct.pack('<I', acc1))
    run.ram_write(0x1778, struct.pack('<h', out1))
    run.ram_write(0x229, bytes([mode]))
    run.ram_write(0x339, struct.pack('<H', f339))
    run.ram_write(0x324, struct.pack('<H', m2t))
    run.ram_write(0x326, struct.pack('<H', c326))
    run.call(0x1D078, (), max_insn=400000)
    val = 0 if F == 0 else _s16(_sdiv(48000, V))
    na1 = (acc1 + val - out1) & 0xFFFFFFFF; e_o1 = _s16(na1 >> 5)
    na2 = (acc2 + val - out2) & 0xFFFFFFFF; e_o2 = max(0, _s16(na2 >> 3))
    e_pct = _sdiv(100 * e_o2, 208) & 0xFFFF
    flag = f339 & 0xFF
    if flag == 1: tgt = 522
    elif mode == 0xb: tgt = 125
    elif mode == 2: tgt = m2t
    elif mode == 3: tgt = c326
    else: tgt = 208
    e_tgt = (tgt if _s16(tgt) <= c326 else c326) & 0xFFFF
    g_sp0 = struct.unpack('<H', run.ram_read(0x1768, 2))[0]
    g_o1  = struct.unpack('<H', run.ram_read(0x1778, 2))[0]
    g_o2  = struct.unpack('<H', run.ram_read(0x1770, 2))[0]
    g_pct = struct.unpack('<H', run.ram_read(0x236, 2))[0]
    g_tgt = struct.unpack('<H', run.ram_read(0x177c, 2))[0]
    g_set = struct.unpack('<H', run.ram_read(0x3F2, 2))[0]   # structB@0x3c8[+0x2a] setpoint
    assert g_sp0 == val & 0xFFFF, f'sp0 {g_sp0} != {val & 0xffff} (V={V},F={F})'
    assert g_o1 == e_o1 & 0xFFFF, f'out1 {g_o1} != {e_o1}'
    assert g_o2 == e_o2 & 0xFFFF, f'out2 {g_o2} != {e_o2}'
    assert g_pct == e_pct, f'pct {g_pct} != {e_pct}'
    assert g_tgt == e_tgt, f'tgt {g_tgt} != {e_tgt} (mode={mode},flag={flag})'
    assert g_set == e_tgt, f'setpoint +0x2a {g_set} != {e_tgt} (mode={mode},flag={flag})'


# --- 0x1d078 ramp-core PI-регулятор: P-term + 2-фазный toggle (§72) ---
@t(0x1D078, '§72: ramp-core (Phase B, counter S+0x28=1) = PI-регулятор. P-term: S+0x2c=min(err,300), err=(target−out2_new) if out1_new<target else (out2_new−target); S+0x5c=s16(S+0x2c)<<7. Toggle: counter 1→2→reset 0. positive-target домен; вериф. 400/400')
def _(run, rng):
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
    run.ram_write(0x1768, struct.pack('<H', 0))
    run.ram_write(0x176C, struct.pack('<I', acc2))
    run.ram_write(0x1770, struct.pack('<H', out2 & 0xFFFF))
    run.ram_write(0x1774, struct.pack('<I', acc1))
    run.ram_write(0x1778, struct.pack('<H', out1 & 0xFFFF))
    for off in (0x1760, 0x1764, 0x388, 0x224):   # anti-windup inходы = 0
        run.ram_write(off, struct.pack('<I', 0))
    run.ram_write(0x3C8, b'\x00' * 0x70)          # Phase B: counter S+0x28=1
    run.ram_write(0x3C8 + 0x28, struct.pack('<H', 1))
    run.call(0x1D078, (), max_insn=400000)
    val = 0 if F == 0 else _s16(_sdiv(48000, V))
    o1n = _s16(((acc1 + val - out1) & 0xFFFFFFFF) >> 5)
    o2n = max(0, _s16(((acc2 + val - out2) & 0xFFFFFFFF) >> 3))
    flag = f339 & 0xFF
    tgt = 522 if flag == 1 else (125 if mode == 0xb else
                                 (m2t if mode == 2 else (c326 if mode == 3 else 208)))
    tgt = (tgt if _s16(tgt) <= c326 else c326) & 0xFFFF
    tsgn = _s16(tgt)
    err = (tsgn - o2n) if o1n < tsgn else (o2n - tsgn)
    e_2c = min(err, 300)
    e_5c = (_s16(e_2c & 0xFFFF) << 7) & 0xFFFFFFFF
    g_2c = struct.unpack('<H', run.ram_read(0x3C8 + 0x2C, 2))[0]
    g_5c = struct.unpack('<I', run.ram_read(0x3C8 + 0x5C, 4))[0]
    g_28 = struct.unpack('<H', run.ram_read(0x3C8 + 0x28, 2))[0]
    assert g_2c == (e_2c & 0xFFFF), f'S+0x2c {g_2c} != {e_2c & 0xffff} (tgt={tsgn},o1n={o1n},o2n={o2n})'
    assert g_5c == e_5c, f'S+0x5c {g_5c:#x} != {e_5c:#x}'
    assert g_28 == 0, f'toggle counter {g_28} != 0 (Phase B)'


# --- 0x1d078 Phase B полная модель: I-term + anti-windup (§72.4) ---
@t(0x1D078, '§72: Phase B полная модель — I-term clamp[8000,131040] + anti-windup tail (reset u1760==0 / slew) + sxth out1/out2. S58/S60/S64/S2e; вериф. 2000/2000')
def _(run, rng):
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
    u1764 = rng.getrandbits(24); u388 = rng.getrandbits(24); u224 = rng.getrandbits(20)
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
    run.ram_write(0x3C8, b'\x00' * 0x70)   # Phase B: counter S+0x28=1
    run.ram_write(0x3C8 + 0x28, struct.pack('<H', 1))
    run.ram_write(0x3C8 + 0x58, struct.pack('<I', old_int))
    run.ram_write(0x3C8 + 0x2E, struct.pack('<H', s2e_old))
    run.call(0x1D078, (), max_insn=400000)
    # --- модель (совпадает с _d078_fullB.model_phaseB) ---
    val = 0 if F == 0 else _s16(_sdiv(48000, V))
    o1n = _s16(_s32(acc1 + val - out1) >> 5)          # asr5 + sxth
    o2n = max(0, _s16(_s32(acc2 + val - out2) >> 3))   # asr3 + sxth + clamp>=0
    flag = f339 & 0xFF
    tgt = 522 if flag == 1 else (125 if mode == 0xb else
                                 (m2t if mode == 2 else (c326 if mode == 3 else 208)))
    tgt = (tgt if _s16(tgt) <= c326 else c326) & 0xFFFF
    tsgn = _s16(tgt)
    if o1n < tsgn:   # INCREASE
        err = _s16(tsgn - o2n); interim = (5 * err + old_int) & 0xFFFFFFFF
    else:            # DECREASE
        err = _s16(o2n - tsgn); interim = (old_int - 5 * err) & 0xFFFFFFFF
    adj = _s32(u1764 - u388) >> 3
    integral = _s32(interim - adj)
    S58 = max(8000, min(integral, 131040))            # clamp (верх → 131040!)
    S60 = _s32(S58 & 0xFFFFFFFF) >> 2
    if o1n < tsgn:   # INCREASE
        e2 = _s16(tsgn - o2n); S2c = e2 if e2 <= 300 else 300
        P = _s16(S2c & 0xFFFF) << 7; output = P + S60
    else:            # DECREASE
        e2 = _s16(o2n - tsgn); S2c = e2 if e2 <= 300 else 300
        P = _s16(S2c & 0xFFFF) << 7; output = S60 - P
    S64 = max(1000, min(32760, output))
    if u1760 == 0:   # RESET path
        S58 = (u224 * 4) & 0xFFFFFFFF; S64 = 0; S2e = 0
    else:            # SLEW path
        new2e = _s16(_s16(s2e_old) + 1)
        if new2e > 2:
            S2e = 2
            if u1760 < S60:
                S58 = (u1760 * 4) & 0xFFFFFFFF
            up = _s32(u224 * 7) >> 1
            if up > _s32(S58):
                S58 = up & 0xFFFFFFFF
        else:
            S2e = new2e
        if u1760 < S64:
            S64 = u1760
    g58 = struct.unpack('<I', run.ram_read(0x3C8 + 0x58, 4))[0]
    g60 = struct.unpack('<I', run.ram_read(0x3C8 + 0x60, 4))[0]
    g64 = struct.unpack('<I', run.ram_read(0x3C8 + 0x64, 4))[0]
    g2e = struct.unpack('<H', run.ram_read(0x3C8 + 0x2E, 2))[0]
    assert g58 == (S58 & 0xFFFFFFFF), f'S+0x58 {g58} != {S58 & 0xffffffff}'
    assert g60 == (S60 & 0xFFFFFFFF), f'S+0x60 {g60} != {S60 & 0xffffffff}'
    assert g64 == (S64 & 0xFFFFFFFF), f'S+0x64 {g64} != {S64 & 0xffffffff}'
    assert g2e == S2e, f'S+0x2e {g2e} != {S2e}'


# --- 0x1a938 FOC: конфигурация моторного таймера (§73) ---
@t(0x1A938, '§73: FOC entry конфигурирует моторный таймер @0x40012c00 — CTRL(+0x30) RMW &= 0xDFFF (clear бит 13); DATA0/1/2 (+0x44/48/4c) = u16[RAM+0x386/384/382]. Эмулятор: TimModel + periph-capture. Детерминизм: 4 записи для любого value.')
def _(run, rng):
    from emulator.mcu_emu import TimModel, MOTOR_TIM_BASE
    uc = run.uc
    uc.mem_write(RAM, bytes(0x20000))          # чистая RAM → детерминизм
    r4 = RAM + 0x040
    uc.mem_write(r4, bytes(0x80))
    val = rng.randrange(0, 32768)              # вход FOC: s16[r4+2]
    uc.mem_write(r4 + 2, struct.pack('<h', val))
    tim = TimModel(run.emu, MOTOR_TIM_BASE)
    tim.set(0x54, 0x8000)                      # STAT бит15=1 → гейт FOC открыт (иначе обход)
    tim.set(0x30, 0xFFFF)                      # known pre-value для проверки RMW
    def _st(uc_, addr, size, u):
        aa = addr & ~1
        if not (FLASH0 <= aa < FLASH0 + FW_LEN or
                FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()                      # чистый возврат (bx lr → 0x0BADF001)
    sh = uc.hook_add(UC_HOOK_CODE, _st)
    try:
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R4, r4)
        uc.reg_write(UC_ARM_REG_R0, 0)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1A938 | 1, 0, count=200000)
        except UcError:
            pass
    finally:
        uc.hook_del(sh)
        uc.hook_del(tim._hook)
    # --- проверка конфигурации таймера ---
    d0 = struct.unpack('<H', run.ram_read(0x386, 2))[0]
    d1 = struct.unpack('<H', run.ram_read(0x384, 2))[0]
    d2 = struct.unpack('<H', run.ram_read(0x382, 2))[0]
    t0 = tim.read(0x44) & 0xFFFF
    t1 = tim.read(0x48) & 0xFFFF
    t2 = tim.read(0x4c) & 0xFFFF
    ctrl = tim.read(0x30)
    assert (t0, t1, t2) == (d0, d1, d2), \
        f'FOC timer DATA {t0,t1,t2} != u16[RAM+0x386/384/382] {d0,d1,d2}'
    assert ctrl == 0xDFFF, \
        f'FOC timer CTRL 0x{ctrl:x} != 0xDFFF (RMW 0xFFFF & 0xDFFF, clear бит 13)'
    offs = sorted(set(o for _, o, _, _ in tim.writes))
    assert {0x30, 0x44, 0x48, 0x4c} <= set(offs), \
        f'FOC timer не записал все регистры: offs={offs}'


# --- 0x1a938 FOC + TIM clock model (§73.x) ---
@t(0x1A938, '§73.x: TIM clock model — такт контура (tick→update по period) управляет режимом FOC через STAT бит15: =0 → обход (0 записей таймера), event → set bit15 → config (4 записи). Свободно-ходный счётчик wrap; модель параметризована (period/step).')
def _(run, rng):
    from emulator.mcu_emu import TimModel, MOTOR_TIM_BASE
    uc = run.uc
    TIM_OFFS = (MOTOR_TIM_BASE + 0x30, MOTOR_TIM_BASE + 0x44,
                MOTOR_TIM_BASE + 0x48, MOTOR_TIM_BASE + 0x4c)

    def run_foc(stat_bit15):
        uc.mem_write(RAM, bytes(0x20000))
        uc.mem_write(MOTOR_TIM_BASE, bytes(0x100))      # чистый моторный блок
        r4 = RAM + 0x040
        uc.mem_write(r4, bytes(0x80))
        uc.mem_write(r4 + 2, struct.pack('<h', rng.randrange(0, 32768)))
        uc.mem_write(MOTOR_TIM_BASE + 0x54,
                     struct.pack('<I', 0x8000 if stat_bit15 else 0x0000))
        before = len(run.emu.periph_writes)

        def _st(uc_, addr, size, u):
            aa = addr & ~1
            if not (FLASH0 <= aa < FLASH0 + FW_LEN or
                    FLASH1 <= aa < FLASH1 + FW_LEN):
                uc_.emu_stop()
        sh = uc.hook_add(UC_HOOK_CODE, _st)
        try:
            uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
            uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
            uc.reg_write(UC_ARM_REG_R4, r4)
            uc.reg_write(UC_ARM_REG_R0, 0)
            run.emu.insn = 0
            try:
                uc.emu_start(0x1A938 | 1, 0, count=200000)
            except UcError:
                pass
        finally:
            uc.hook_del(sh)
        return sum(1 for _, a, s, v in run.emu.periph_writes[before:]
                   if a in TIM_OFFS)

    period = rng.randrange(2, 16)                        # период контура (тактов)
    tim = TimModel(run.emu, MOTOR_TIM_BASE, period=period, step=1)
    try:
        # фаза 1: STAT бит15=0 → обход (0 записей таймера)
        n_off = run_foc(stat_bit15=False)
        assert n_off == 0, f'FOC bit15=0: записей {n_off} != 0 (ожид. обход)'
        # такты до первого update-события (wrap счётчика)
        t0 = tim.ticks
        while not tim.update:
            tim.tick()
            assert (tim.ticks - t0) <= period + 2, 'clock не завернул за period'
        assert tim.cnt == 0 and tim.update, \
            f'clock: cnt={tim.cnt} update={tim.update} (ожид. wrap→0/True)'
        # фаза 2: event → модель задает STAT бит15 → config (4 записи)
        tim.set_status_bits(MOTOR_TIM_BASE + 0x54, 0x8000)
        n_on = run_foc(stat_bit15=True)
        assert n_on == 4, f'FOC bit15=1: записей {n_on} != 4 (ожид. config)'
    finally:
        uc.hook_del(tim._hook)


# --- 0x1be1c ADC/capture model (§73.x) ---
@t(0x1BE1C, '§73.x: ADC/capture model — 0x1be1c реконструирует фазные токи из T28/T2C/T30 (periph @0x40012468/6c/70): фаза=(T−C)<<4, 3-я=−сумма (Кирхгоф). sector→handler: 0→null,1→B,2/3→A,4/5→C,6→B. AdcModel.set_captures/set_currents.')
def _(run, rng):
    from emulator.mcu_emu import (AdcModel, ADC_SECTOR_HANDLER,
                                  ADC_HANDLER_MEASURED)
    uc = run.uc
    r0 = RAM + 0x100

    def setup(sector, c18, c1a, c1c):
        uc.mem_write(RAM, bytes(0x20000))
        uc.mem_write(r0, bytes(0x40))
        uc.mem_write(r0 + 2, struct.pack('<H', sector))
        uc.mem_write(r0 + 0x18, struct.pack('<h', c18))
        uc.mem_write(r0 + 0x1a, struct.pack('<h', c1a))
        uc.mem_write(r0 + 0x1c, struct.pack('<h', c1c))
        uc.mem_write(0x40012c54, struct.pack('<I', 0x8000))   # mode-2 гейт

    def run_be1c():
        def _st(uc_, addr, size, u):
            aa = addr & ~1
            if not (FLASH0 <= aa < FLASH0 + FW_LEN or
                    FLASH1 <= aa < FLASH1 + FW_LEN):
                uc_.emu_stop()
        sh = uc.hook_add(UC_HOOK_CODE, _st)
        try:
            uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
            uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
            uc.reg_write(UC_ARM_REG_R0, r0)
            run.emu.insn = 0
            try:
                uc.emu_start(0x1BE1C | 1, 0, count=200000)
            except UcError:
                pass
        finally:
            uc.hook_del(sh)
        return (struct.unpack('<i', uc.mem_read(r0 + 0xc, 4))[0],
                struct.unpack('<i', uc.mem_read(r0 + 0x10, 4))[0],
                struct.unpack('<i', uc.mem_read(r0 + 0x14, 4))[0])

    adc = AdcModel(run.emu)
    c18 = rng.randrange(500, 2000)
    c1a = rng.randrange(500, 2000)
    c1c = rng.randrange(500, 2000)
    # --- (1) set_captures: raw T → pre-clamp (T−C)<<4 + −sum по handler ---
    for sector in range(7):
        setup(sector, c18, c1a, c1c)
        t28 = rng.randrange(0, 4000)
        t2c = rng.randrange(0, 4000)
        t30 = rng.randrange(0, 4000)
        adc.set_captures(t28, t2c, t30)
        oc, o10, o14 = run_be1c()
        h = ADC_SECTOR_HANDLER[sector]
        if h is None:
            assert (oc, o10, o14) == (0, 0, 0), \
                f'sector={sector} null: got {(oc, o10, o14)} != (0,0,0)'
            continue
        d28 = (t28 - c18) << 4
        d2c = (t2c - c1a) << 4
        d30 = (t30 - c1c) << 4
        if h == 'A':
            e = (d28, d2c, -(d28 + d2c))       # A: o_c=T28, o_10=T2C, o_14=−sum
        elif h == 'B':
            e = (-(d2c + d30), d2c, d30)       # B: o_c=−sum, o_10=T2C, o_14=T30
        else:  # C
            e = (d28, -(d28 + d30), d30)       # C: o_c=T28, o_10=−sum, o_14=T30
        assert (oc, o10, o14) == e, \
            f'sector={sector} h={h}: got {(oc, o10, o14)} != exp {e}'
    # --- (2) set_currents: инжект токов → измеренные фазы совпадают (×16 квант) ---
    for sector in (1, 2, 4, 6):
        setup(sector, c18, c1a, c1c)
        h = ADC_SECTOR_HANDLER[sector]
        meas_out = [m[2] for m in ADC_HANDLER_MEASURED[h]]
        targets = {0xc: rng.randrange(-500, 500) * 16,
                   0x10: rng.randrange(-500, 500) * 16,
                   0x14: rng.randrange(-500, 500) * 16}
        adc.set_currents(r0, targets, sector)
        oc, o10, o14 = run_be1c()
        got = {0xc: oc, 0x10: o10, 0x14: o14}
        for off in meas_out:
            assert got[off] == targets[off], \
                f'set_currents sector={sector} h={h}: out{off:#x} {got[off]} != {targets[off]}'


# --- 0x1d078 closed loop: SpeedModel (замер скорости) (§73.x) ---
@t(0x1D078, '§73.x closed loop: SpeedModel — замер скорости замыкает контур. set_period(V)→PID вычисляет val=s16(48000/V); set_speed(val) (V=48000//val) → PID даёт ровно val (для делителей 48000); stop() (F=0) → val=0. V=u32[RAM+0x158], F=byte[RAM+0x100].')
def _(run, rng):
    from emulator.mcu_emu import SpeedModel
    sm = SpeedModel(run.emu)

    def run_pid():
        # минимальное безопасное состояние 0x1d078 (как §69)
        run.ram_write(0x229, bytes([3]))                 # mode=3 → target=u16[RAM+0x326]
        run.ram_write(0x326, struct.pack('<H', 200))
        run.ram_write(0x339, b'\x00')                    # flag=0
        run.ram_write(0x1768, struct.pack('<H', 0))      # чистый val
        run.ram_write(0x176c, struct.pack('<I', 0))      # acc2
        run.ram_write(0x1770, struct.pack('<h', 0))      # out2
        run.ram_write(0x1774, struct.pack('<I', 0))      # acc1
        run.ram_write(0x1778, struct.pack('<h', 0))      # out1
        run.call(0x1D078, (), max_insn=400000)

    # --- (1) set_period: V → PID val=s16(48000/V) ---
    for _ in range(6):
        V = rng.randint(1, 48000)
        sm.set_period(V)
        run_pid()
        got = sm.get_val()
        exp = _s16(_sdiv(48000, V))
        assert got == exp, f'set_period V={V}: PID val {got} != s16(48000/V)={exp}'
    # --- (2) set_speed: делители 48000 → PID даёт ровно val ---
    for val in (100, 200, 480, 1200, 4800, 12000):
        sm.set_speed(val)
        run_pid()
        got = sm.get_val()
        assert got == val, f'set_speed val={val}: PID {got} != {val}'
    # --- (3) stop: F=0 → val=0 ---
    sm.set_period(1000)
    sm.stop()
    run_pid()
    assert sm.get_val() == 0, f'stop(): val {sm.get_val()} != 0'


# --- 0x1d078 motor dynamics: АВТОНОМНЫЙ симул замкнутого контура (§73.x) ---
@t(0x1D078, '§73.x motor dynamics: MotorModel (plant) замыкает АВТОНОМНЫЙ симул. target=208 → PID 0x1d078 → throttle(u16[RAM+0x42c]) → plant(speed) → SpeedModel(V) → PID ... Скорость сходится к target: 0→overshoot~338→settle~207; throttle спадает. Детерминированно (fixed params).')
def _(run, rng):
    from emulator.mcu_emu import MotorModel, SpeedModel
    uc = run.uc
    target = 208
    # начальное состояние PID: ramp-core + гейты + мощность разрешена (u1760≠0)
    uc.mem_write(RAM, bytes(0x20000))
    uc.mem_write(RAM + 0x229, bytes([3]))                 # mode=3 → target=u16[RAM+0x326]
    uc.mem_write(RAM + 0x326, struct.pack('<H', target))
    uc.mem_write(RAM + 0x339, b'\x00')
    uc.mem_write(RAM + 0x333, b'\x00')                    # skip mode-change
    uc.mem_write(RAM + 0x263, b'\x00')                    # gate → ramp-core
    uc.mem_write(RAM + 0x1760, struct.pack('<I', 32760))  # мощность разрешена (не reset)
    uc.mem_write(RAM + 0x1764, struct.pack('<I', 0))
    uc.mem_write(RAM + 0x388, struct.pack('<I', 0))
    uc.mem_write(RAM + 0x224, struct.pack('<I', 0))
    uc.mem_write(RAM + 0x3C8 + 0x28, struct.pack('<H', 1))  # counter → ramp-core
    sm = SpeedModel(run.emu)
    mm = MotorModel(run.emu, v_max=520.0, tau=15.0, throttle_ref=4000.0)
    speeds, thrs = [], []
    for _ in range(40):
        sm.set_speed(int(mm.speed))
        run.call(0x1D078, (), max_insn=400000)
        thr = struct.unpack('<h', uc.mem_read(RAM + 0x42c, 2))[0]
        thrs.append(thr)
        mm.step(thr)
        speeds.append(mm.speed)
    # --- замкнутый контур сходится к target ---
    assert speeds[0] > 0, f'ускорение не началось: speed[0]={speeds[0]}'
    assert max(speeds) > target, \
        f'скорость не достигла target: max={max(speeds):.1f} < {target}'
    assert abs(speeds[-1] - target) < 0.5 * target, \
        f'схождение: speed_end={speeds[-1]:.1f} вне полосы ±50% от target={target}'
    assert thrs[0] > thrs[-1], \
        f'throttle не спадает при подходе к target: {thrs[0]} -> {thrs[-1]}'


# --- батарея: BatteryModel (SoC + разряд) (§73.x) ---
@t(0x1DFD8, '§73.x battery: BatteryModel — SoC%→u16[RAM+0x306] (+сырое i16@0x17a0 [415..535]). set_soc round-trip; mapping 0%→415/100%→535; разряд монотонно падает с нагрузкой, bounded [0,100], без нагрузки не меняется. Пороги FOC 90/10 гейтятся (byte@0x22e).')
def _(run, rng):
    from emulator.mcu_emu import BatteryModel, BATT_RAW_MIN, BATT_RAW_MAX
    uc = run.uc
    bm = BatteryModel(run.emu)
    # --- (1) set_soc round-trip + raw mapping [415..535] ---
    for pct in (0, 25, 50, 75, 100):
        bm.set_soc(pct)
        assert bm.get_soc() == pct, f'set_soc({pct}): get={bm.get_soc()}'
        raw = struct.unpack('<h', uc.mem_read(RAM + 0x17A0, 2))[0]
        exp_raw = BATT_RAW_MIN + round(pct * (BATT_RAW_MAX - BATT_RAW_MIN) / 100.0)
        assert raw == exp_raw, f'set_soc({pct}): raw {raw} != {exp_raw}'
    bm.set_soc(0)
    assert struct.unpack('<h', uc.mem_read(RAM + 0x17A0, 2))[0] == 415
    bm.set_soc(100)
    assert struct.unpack('<h', uc.mem_read(RAM + 0x17A0, 2))[0] == 535
    # --- (2) разряд: монотонно падает с нагрузкой, bounded [0,100] ---
    bm.set_soc(80)
    prev = 80.0
    for _ in range(20):
        thr = rng.randint(5000, 32760)          # нагрузка (прокси тока)
        s = bm.discharge(thr, dt=1.0)
        assert 0 <= s <= 100, f'разряд вне [0,100]: {s}'
        assert s <= prev, f'разряд не монотонен: {prev} -> {s}'
        prev = s
    # без нагрузки SoC не меняется
    bm.set_soc(50)
    assert bm.discharge(0, dt=1.0) == 50, 'разряд без нагрузки изменил SoC'


# --- запас хода: RangeModel (0x1d898) (§73.x) ---
@t(0x1D898, '§73.x range: RangeModel — v=i16[RAM+0x27A]→X=(8000·v)>>16, R=10000·X/(500−X) (делитель 0x19994; div-by-zero→-1, отриц. знаменатель→отриц.). Closed-form вериф. random-sweep (v≥0) против firmware 0x1d898 + edge-cases (v=0/415/535/4096).')
def _(run, rng):
    from emulator.mcu_emu import RangeModel
    rm = RangeModel(run.emu)
    def fw(v):
        rm.set_value(v)
        run.call(0x1D898, (0, 0, 0, 0), max_insn=300000)
        X = struct.unpack('<H', run.uc.mem_read(RAM + 0x3E8, 2))[0]
        R = struct.unpack('<i', run.uc.mem_read(RAM + 0x408, 4))[0]
        return X, R
    # --- random-sweep: closed-form vs firmware (v≥0) ---
    for _ in range(150):
        v = rng.randint(0, 12000)
        mx, mr = rm.estimate(v)
        fx, fr = fw(v)
        assert (fx, fr) == (mx, mr), f'v={v}: fw=({fx},{fr}) model=({mx},{mr})'
    # --- edge-cases ---
    assert rm.estimate(0) == (0, 0) and fw(0) == (0, 0)
    assert rm.estimate(415) == (50, 1111) and fw(415) == (50, 1111)
    assert rm.estimate(535) == (65, 1494) and fw(535) == (65, 1494)
    # div-by-zero: X=500 при v=4096 → R=-1
    assert rm.estimate(4096) == (500, -1) and fw(4096) == (500, -1)


# --- 0x1d898 аккумулятор (leaky integrator) (§73.x) ---
@t(0x1D898, '§73.x range-acc: аккумулятор 0x1d898 (leaky integrator) — new_0x3c=(old_0x3c+delta−prev_0x14)&0xFFFFFFFF, new_0x14=asr(new_0x3c,10)[i16]; delta=i16[RAM+0x26E]. Stateful-sweep против firmware + edge-cases.')
def _(run, rng):
    from emulator.mcu_emu import RangeModel, McuEmu
    from unicorn import UC_HOOK_CODE, UcError
    from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3
    rm = RangeModel(run.emu)
    # 0x1d898 state-зависим (поздние под-вызовы, data-driven jump) → self-contained:
    # fresh McuEmu на каждый вызов (чистый путь, как в probe 250/250). Reuse emu +
    # re-zero RAM ломает large-A итерации (нере-zeroed periph → early unmapped fetch).
    def fw_acc(A, B, D):
        femu = McuEmu(max_insn=300000)
        femu.uc.mem_write(RAM, bytes(0x20000))
        femu.uc.mem_write(RAM + 0x404, struct.pack('<I', A & 0xFFFFFFFF))  # old_0x3c
        femu.uc.mem_write(RAM + 0x3DC, struct.pack('<h', B))               # prev_0x14
        femu.uc.mem_write(RAM + 0x26E, struct.pack('<h', D))               # delta
        femu.uc.mem_write(RAM + 0x27A, struct.pack('<h', 500))             # v (не влияет на acc)
        def stop(uc_, a, s, u):
            aa = a & ~1
            if not (0 <= aa < 0x25000 or 0x08000000 <= aa < 0x08000000 + 0x25000):
                uc_.emu_stop()
        sh = femu.uc.hook_add(UC_HOOK_CODE, stop)
        femu.uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
        femu.uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3):
            femu.uc.reg_write(r, 0)
        try:
            femu.uc.emu_start(0x1D898 | 1, 0, count=300000)
        except UcError:
            pass
        femu.uc.hook_del(sh)
        n3c = struct.unpack('<I', femu.uc.mem_read(RAM + 0x404, 4))[0]
        n14 = struct.unpack('<h', femu.uc.mem_read(RAM + 0x3DC, 2))[0]
        return n3c, n14
    # --- stateful-sweep: closed-form vs firmware (fresh emu per call) ---
    for _ in range(80):
        A = rng.randint(0, 0xFFFFFFFF)
        B = rng.randint(-3000, 3000)
        D = rng.randint(-5000, 5000)
        mx, ms = rm.acc_step(A, B, D)
        fx, fs = fw_acc(A, B, D)
        assert (fx, fs) == (mx, ms), f'A={A:#x} B={B} D={D}: fw=({fx},{fs}) model=({mx},{ms})'
    # --- edge-cases ---
    assert fw_acc(0, 0, 0) == rm.acc_step(0, 0, 0) == (0, 0)
    assert fw_acc(0, 0, 1024) == rm.acc_step(0, 0, 1024) == (1024, 1)


# --- 0x1d898 state-machine: гейты статус-флагов (§73.x) ---
@t(0x1D898, '§73.x range-sm: state-machine 0x1d898 — дефолт (zeroed): (0x290,0x292,0x2a8,0x2aa)=(2,140,1,78); гейт +0x286≠0 → (0x290,0x292)=(0,0); гейт +0x29e≠0 → (0x2a8,0x2aa)=(0,0). Флаги mode/LUT-driven (LUT 0x614-0x6c4/0x738-0x808), v/SoC не влияют. Fresh emu/call.')
def _(run, rng):
    from unicorn import UC_HOOK_CODE, UcError
    from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3
    def status(extra):
        femu = McuEmu(max_insn=300000)
        femu.uc.mem_write(RAM, bytes(0x20000))
        femu.uc.mem_write(RAM + 0x27A, struct.pack('<h', 500))
        for off, val in extra.items():
            femu.uc.mem_write(RAM + off, struct.pack('<B', val))
        def stop(uc_, a, s, u):
            aa = a & ~1
            if not (0 <= aa < 0x25000 or 0x08000000 <= aa < 0x08000000 + 0x25000):
                uc_.emu_stop()
        sh = femu.uc.hook_add(UC_HOOK_CODE, stop)
        femu.uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
        femu.uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3):
            femu.uc.reg_write(r, 0)
        try:
            femu.uc.emu_start(0x1D898 | 1, 0, count=300000)
        except UcError:
            pass
        femu.uc.hook_del(sh)
        def h(o):
            return struct.unpack('<h', femu.uc.mem_read(RAM + o, 2))[0]
        return (h(0x290), h(0x292), h(0x2a8), h(0x2aa))
    # --- дефолт (zeroed state) ---
    assert status({}) == (2, 140, 1, 78)
    # --- гейт +0x286: (0x290,0x292)→(0,0), (0x2a8,0x2aa) не меняется ---
    assert status({0x286: 1}) == (0, 0, 1, 78)
    # --- гейт +0x29e: (0x2a8,0x2aa)→(0,0), (0x290,0x292) не меняется ---
    assert status({0x29E: 1}) == (2, 140, 0, 0)
    # --- оба гейта ---
    assert status({0x286: 1, 0x29E: 1}) == (0, 0, 0, 0)


# --- FOC-интеграция в автономный контур (§73.x) ---
FW_LEN = 0x25000

def _foc_amp(ccr):
    center = sum(ccr) / 3.0
    return max(abs(c - center) for c in ccr), center


def _foc_run(uc, current_ref):
    """Полный FOC 0x1a938 на данном uc (общий RAM): current-ref u16[RAM+0x224] → CCR (RAM+0x382/384/386)."""
    from unicorn import UC_HOOK_CODE
    from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_SP, UC_ARM_REG_LR
    r4 = RAM + 0x040
    uc.mem_write(r4, bytes(0x80))
    uc.mem_write(r4 + 2, struct.pack('<h', 16384))          # value (mid) — не управляет PWM
    uc.mem_write(RAM + 0x224, struct.pack('<H', current_ref & 0xFFFF))
    def stop(uc_, a, s, u):
        aa = a & ~1
        if not (FLASH0 <= aa < FLASH0 + FW_LEN or FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, stop)
    uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
    uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    uc.reg_write(UC_ARM_REG_R4, r4)
    uc.reg_write(UC_ARM_REG_R0, 0)
    try:
        uc.emu_start(0x1A938 | 1, 0, count=200000)
    except Exception:
        pass
    uc.hook_del(sh)
    return tuple(struct.unpack('<H', uc.mem_read(RAM + o, 2))[0] for o in (0x382, 0x384, 0x386))


@t(0x1A938, '§73.x FOC-интеграция: transfer-функция current-ref u16[RAM+0x224]→PWM CCR (RAM+0x382/384/386): amp монотонно растёт с ref (0→~0, 4000→~41, 8000→~83, 16384→~169, 28624→~296), center≈1125..1131; CCR_A↑/CCR_B↓ (2-фазная FOC-модуляция). Интегрир. контур: PID(0x1d078)→throttle 0x42c→0x224→FOC→PWM, скорость растёт от 0.')
def _(run, rng):
    # --- transfer-функция FOC: amp монотонна в current-ref (fresh emu/call для чистоты) ---
    refs = (0, 4000, 8000, 16384, 28624)
    amps = []; centers = []
    for ref in refs:
        femu = McuEmu(trace=False, max_insn=200000)
        femu.uc.mem_write(RAM, bytes(0x20000))
        femu.hook_periph_ready()
        ccr = _foc_run(femu.uc, ref)
        amp, center = _foc_amp(ccr)
        amps.append(amp); centers.append(center)
    assert amps[0] < 1.0, f'ref=0 → amp должен ≈0, got {amps[0]}'
    for i in range(1, len(refs)):
        assert amps[i] > amps[i - 1], f'amp не монотонен: {amps}'
    for c in centers:
        assert 1120.0 <= c <= 1135.0, f'center вне [1120,1135]: {centers}'
    # CCR_A растёт, CCR_B падает с ref (2-фазная модуляция)
    femu = McuEmu(trace=False, max_insn=200000); femu.uc.mem_write(RAM, bytes(0x20000)); femu.hook_periph_ready()
    ccr_lo = _foc_run(femu.uc, 4000)
    femu = McuEmu(trace=False, max_insn=200000); femu.uc.mem_write(RAM, bytes(0x20000)); femu.hook_periph_ready()
    ccr_hi = _foc_run(femu.uc, 28624)
    assert ccr_hi[0] > ccr_lo[0], f'CCR_A не растёт: {ccr_lo} -> {ccr_hi}'
    assert ccr_hi[1] < ccr_lo[1], f'CCR_B не падает: {ccr_lo} -> {ccr_hi}'


# --- интегрированный контур: PID → throttle → FOC → PWM → plant (ОДИН emu, общий RAM) ---
@t(0x1D078, '§73.x FOC-контур (интегрир.): ОДИН McuEmu, общий RAM. Шаги: SpeedModel(speed→V)→PID 0x1d078→throttle s16[RAM+0x42c]→u16[RAM+0x224]=throttle→FOC 0x1a938 (тот же emu)→PWM CCR→plant(throttle→speed). За 6 шагов скорость монотонно растёт от 0, throttle>0, FOC-amp>0 (полная цепочка прошивки — PID+FOC — исполняется каждый шаг на общем RAM).')
def _(run, rng):
    from unicorn import UC_HOOK_CODE
    from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_SP, UC_ARM_REG_LR
    emu = McuEmu(max_insn=400000)
    uc = emu.uc
    sm = SpeedModel(emu)
    uc.mem_write(RAM, bytes(0x20000))
    uc.mem_write(RAM + 0x229, bytes([3]))
    uc.mem_write(RAM + 0x326, struct.pack('<H', 208))   # target
    uc.mem_write(RAM + 0x339, b'\x00'); uc.mem_write(RAM + 0x333, b'\x00'); uc.mem_write(RAM + 0x263, b'\x00')
    uc.mem_write(RAM + 0x1760, struct.pack('<I', 32760))
    uc.mem_write(RAM + 0x1764, struct.pack('<I', 0))
    uc.mem_write(RAM + 0x388, struct.pack('<I', 0))
    uc.mem_write(RAM + 0x3C8 + 0x28, struct.pack('<H', 1))
    def stop(uc_, a, s, u):
        aa = a & ~1
        if not (0 <= aa < FW_LEN or FLASH0 <= aa < FLASH0 + FW_LEN or FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()
    speed = 0.0; v_max = 522.0; tau = 15.0; tref = 28624.0
    speeds = []
    for it in range(6):
        sm.set_speed(int(speed))
        sh = uc.hook_add(UC_HOOK_CODE, stop)
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80); uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        for r in (UC_ARM_REG_R0, UC_ARM_REG_R4): uc.reg_write(r, 0)
        try: uc.emu_start(0x1D078 | 1, 0, count=400000)
        except Exception: pass
        uc.hook_del(sh)
        thr = struct.unpack('<h', uc.mem_read(RAM + 0x42c, 2))[0]
        ccr = _foc_run(uc, thr & 0xFFFF)   # FOC на ТОМ ЖЕ emu (общий RAM)
        amp, center = _foc_amp(ccr)
        if it == 0:
            assert thr > 0, f'PID не дал throttle: {thr}'
            assert amp > 10.0, f'FOC не дал PWM из throttle: amp={amp}'
        tnorm = max(0.0, min(1.0, thr / tref)) if tref else 0.0
        speed += (1.0 / tau) * (v_max * tnorm - speed)
        speeds.append(speed)
    assert speeds[-1] > speeds[0], f'скорость не растёт: {speeds}'
    assert all(speeds[i + 1] >= speeds[i] for i in range(len(speeds) - 1)), f'скорость не монотонна в рост: {speeds}'


# --- FOC current-ref→P copy + электро-контур (§73.x) ---
def _foc_run_pp(uc, current_ref, xlo=0, xhi=0, gate=False):
    """FOC 0x1a938: возвращает (ccr_a,ccr_b,ccr_c, P). current-ref u16[RAM+0x224], вектор 0x108/0x10a."""
    from unicorn import UC_HOOK_CODE
    from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_SP, UC_ARM_REG_LR
    r4 = RAM + 0x040
    uc.mem_write(r4, bytes(0x80))
    uc.mem_write(r4 + 2, struct.pack('<h', 16384))
    uc.mem_write(RAM + 0x224, struct.pack('<H', current_ref & 0xFFFF))
    uc.mem_write(RAM + 0x108, struct.pack('<h', xlo))
    uc.mem_write(RAM + 0x10a, struct.pack('<h', xhi))
    if gate:
        uc.mem_write(0x40012C54, struct.pack('<I', 0x8000))   # STAT bit15=1
    def stop(uc_, a, s, u):
        aa = a & ~1
        if not (FLASH0 <= aa < FLASH0 + FW_LEN or FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, stop)
    uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
    uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    uc.reg_write(UC_ARM_REG_R4, r4)
    uc.reg_write(UC_ARM_REG_R0, 0)
    try:
        uc.emu_start(0x1A938 | 1, 0, count=200000)
    except Exception:
        pass
    uc.hook_del(sh)
    ccr = tuple(struct.unpack('<H', uc.mem_read(RAM + o, 2))[0] for o in (0x382, 0x384, 0x386))
    P = struct.unpack('<I', uc.mem_read(RAM + 0x388, 4))[0]
    return ccr, P


@t(0x1A938, '§73.x FOC current-ref→P: P=u32[RAM+0x388]=[u16 RAM+0x224] (1:1, PC 0x1aae4) — current-ref идёт в cross+dot (§60.4) как P. Электро-контур НЕАКТИВЕН в изолированном FOC: measured vector s16[RAM+0x108/0x10a] не меняет PWM CCR (ни с gate=0, ни с STAT bit15=1) — feedback требует полного state-machine (сектор+реконструкция из ADC+PI) и live-gains мотора.')
def _(run, rng):
    # --- P = [0x224] (1:1 copy), для нескольких ref ---
    for ref in (4000, 8000, 16384):
        femu = McuEmu(trace=False, max_insn=200000)
        femu.uc.mem_write(RAM, bytes(0x20000))
        femu.hook_periph_ready()
        ccr, P = _foc_run_pp(femu.uc, ref)
        assert P == (ref & 0xFFFF), f'P({P:#x}) != [0x224]({ref:#x})'
    # --- электро-контур неактивен: вектор 0x108/0x10a не меняет CCR ---
    femu = McuEmu(trace=False, max_insn=200000); femu.uc.mem_write(RAM, bytes(0x20000)); femu.hook_periph_ready()
    ccr_base, _ = _foc_run_pp(femu.uc, 8000, 0, 0)
    for (xlo, xhi) in ((1000, 0), (0, 2000), (3000, -3000)):
        femu = McuEmu(trace=False, max_insn=200000); femu.uc.mem_write(RAM, bytes(0x20000)); femu.hook_periph_ready()
        ccr, _ = _foc_run_pp(femu.uc, 8000, xlo, xhi)
        assert ccr == ccr_base, f'veктор ({xlo},{xhi}) изменил CCR: {ccr} != {ccr_base}'
    # --- даже с активным гейтом (STAT bit15=1) feedback не включается в изоляции ---
    femu = McuEmu(trace=False, max_insn=200000); femu.uc.mem_write(RAM, bytes(0x20000)); femu.hook_periph_ready()
    ccr_g, _ = _foc_run_pp(femu.uc, 8000, 3000, -3000, gate=True)
    assert ccr_g == ccr_base, f'гейт включил feedback: {ccr_g} != {ccr_base}'


# --- §74: ControlLoop — автономный time-driven контур (warm-start) ---
@t(0x1D078, '§74: ControlLoop — автономный time-driven warm-start контур. Виртуальные часы + реальный firmware PID(0x1d078)+FOC(0x1a938) на каждом tick + plant/battery/range (один emu, общий RAM). target=208: скорость растёт от 0 (max>150), throttle>0 всюду, FOC-amp>0 (FOC исполняется каждый шаг), SoC падает с нагрузкой, range>0. Сходится ВЫШЕ target (~325) — свойство калибровки plant/PID; траектория совпадает с _foc_sim.py 40/40.')
def _(run, rng):
    from emulator.mcu_emu import ControlLoop, McuEmu
    femu = McuEmu(trace=False, max_insn=400000)
    cl = ControlLoop(emu=femu, v_max=522.0, tau=15.0, throttle_ref=28624.0)
    cl.setup(target=208, mode=3, soc=100.0)
    traj = cl.run(24)
    # старт: скорость >0 и мала
    assert traj[0]['speed'] > 0 and traj[0]['speed'] < 60, f"start: {traj[0]}"
    # тяга есть всюду (throttle>0)
    assert all(st['throttle'] > 0 for st in traj), 'throttle<=0 (нет тяги)'
    # FOC исполняется каждый шаг (amp>0)
    assert all(st['pwm_amp'] > 0 for st in traj), 'FOC-amp=0 (FOC не исполняется)'
    # скорость растёт к target (достигает >150)
    assert max(st['speed'] for st in traj) > 150, \
        f"max speed {max(s['speed'] for s in traj)} < 150"
    # батарея разряжается с нагрузкой
    assert traj[-1]['soc'] < 100.0, f"SoC не падает: {traj[-1]['soc']}"
    # запас хода вычисляется (R>0)
    assert all(st['range'] > 0 for st in traj), 'range<=0'


# --- A1: GpioModel (кастомный GPIO-блок «портов», §39.1) ---
@t(0x1BF48, 'A1: GpioModel — кастомный GPIO-блок «портов» (§39.1): 4 порта × stride 0x400 (база 0x48000000), режимы в MODER_LO/HI (+0x2c/+0x28) по 2 бита/пин. MOTOR-INIT 0x1bf48 конфигурирует пины через драйвер 0x22000; модель ловит записи и декодит режимы. Детерминизм: фиксированный набор портов с ненулевыми режимами (MODER_LO записан).')
def _(run, rng):
    from emulator.mcu_emu import GpioModel
    uc = run.uc
    uc.mem_write(RAM, bytes(0x20000))          # чистая RAM → детерминизм
    run.emu.hook_periph_ready()                 # status-биты ready (как в run_func)
    gpio = GpioModel(run.emu)
    def _st(uc_, addr, size, u):
        aa = addr & ~1
        if not (FLASH0 <= aa < FLASH0 + FW_LEN or
                FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, _st)
    try:
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1BF48 | 1, 0, count=200000)
        except UcError:
            pass
    finally:
        uc.hook_del(sh)
        uc.hook_del(gpio._hook)
    # модель поймала записи в портовый блок
    assert gpio.writes, 'GpioModel не поймал записей в портовый блок'
    ports_written = sorted(set(p for _, p, _, _, _ in gpio.writes))
    assert ports_written, 'порты не записаны'
    # декод режимов: MODER_LO (+0x2c) записан с ненулевым пакетом хотя бы в один порт
    cfg = gpio.config_report()
    assert cfg, 'config_report пуст — ни одного ненулевого режима пина'
    moder_ports = [p for p in range(4) if gpio.read(p, 0x2c)]
    assert moder_ports, 'MODER_LO (+0x2c) не записан ни в одном порту'
    # каждый декодированный режим — валиден (0..3 по 2 бита)
    for p, pins in cfg.items():
        for pin, mode in pins.items():
            assert 0 <= mode <= 3, f'невалидный режим {mode} порт {p} пин {pin}'


# --- A2: UsartTxModel (push-кадры, сборщик 0x211f8) ---
@t(0x211F8, 'A2: UsartTxModel — push-TX pipeline (этап сборки). Прогон РЕАЛЬНОГО сборщика 0x211f8 (без арг., читает фикс. RAM-поля телеметрии) → TX-кольцо @0x10b5 → декод кадров 61..9E (chk=SUM&0xFF). Seed: mode@0x229=2, u16@0x236=50 → валидный a0-кадр с mode_lo=2 и pct_0x236=50.')
def _(run, rng):
    from emulator.mcu_emu import McuEmu, UsartTxModel
    femu = McuEmu(trace=False, max_insn=400000)
    uc = femu.uc
    uc.mem_write(RAM, bytes(0x20000))          # чистая RAM → детерминизм
    uc.mem_write(RAM + 0x229, bytes([2]))              # mode lo
    uc.mem_write(RAM + 0x236, struct.pack('<H', 50))   # pct (u16@0x236)
    uc.mem_write(RAM + 0x306, struct.pack('<H', 89))   # батарея %
    femu.hook_periph_ready()
    tx = UsartTxModel(femu)
    frames = tx.assemble()
    assert frames, 'сборщик не произвёл ни одного валидного push-кадра'
    a0 = [f for f in frames if f[1] == 0x30]
    assert a0, 'нет a0-кадра (телеметрия)'
    raw, sub, fl = a0[0]
    assert fl['mode'] & 0xF == 2, f"mode_lo != 2: {fl['mode']:02x} (seed @0x229=2)"
    assert fl['pct_0x236'] == 50, f"pct_0x236 != 50: {fl['pct_0x236']} (seed @0x236=50)"


# --- A3: SpiFlashModel (внешний SPI-flash / NVM) ---
@t(0x221E6, 'A3: SpiFlashModel — внешний SPI-flash (NVM). Виртуальный буфер size=0x1000 (≤4KB, из валидации addr в 0x221e6), дефолт 0xFF (стёртая flash); set/get round-trip; OOB -> ValueError. SPI-протокол: write-enable 0x221a4 (cmd 0x06) + page-program 0x221e6 (шаг слота 4Б); NVRAM-save 0x21A08 персистит конфиг/калибровку.')
def _(run, rng):
    from emulator.mcu_emu import McuEmu, SpiFlashModel, NVM_SIZE
    assert NVM_SIZE == 0x1000, f'NVM_SIZE != 4KB: {NVM_SIZE:#x}'
    femu = McuEmu(trace=False, max_insn=200000)
    nvm = SpiFlashModel(femu)
    assert all(b == 0xFF for b in nvm.flash), 'NVM-дефолт != 0xFF (стёртая flash)'
    nvm.set(0x10, struct.pack('<H', 0x1234))
    assert nvm.get(0x10, 2) == b'\x34\x12', 'set/get round-trip (little-endian u16)'
    nvm.seed({0x20: 89, 0x30: bytes([1, 2, 3])})
    assert nvm.get(0x20, 1) == b'\x59', 'seed byte'
    assert nvm.get(0x30, 3) == b'\x01\x02\x03', 'seed bytes'
    try:
        nvm.set(NVM_SIZE - 1, b'\x00\x00')   # 2 байта за границей
        assert False, 'OOB set не выбросил ValueError'
    except ValueError:
        pass


# --- B1: CmdControlModel (командный слой -> блок управления @0x40021000) ---
@t(0xC664, 'B1: CmdControlModel — командный слой (dispatcher 0x2e0c / handler 0x97f4) шевелит биты в кастомном блоке управления @0x40021000 (поля +0x10/+0x18/+0x1c). Примитив 0xc664(r0=бит, r1=set/clear): pre-set поля в 0 -> set(0x200000) пишет ровно бит21 в +0x1c; clear снимает. Модель ловит операции.')
def _(run, rng):
    from emulator.mcu_emu import McuEmu, CmdControlModel, CMD_CTRL_BASE
    femu = McuEmu(trace=False, max_insn=50000)
    uc = femu.uc
    uc.mem_write(RAM, bytes(0x20000))
    femu.hook_periph_ready()
    for off in (0x10, 0x18, 0x1c):
        femu.uc.mem_write(CMD_CTRL_BASE + off, struct.pack('<I', 0))   # pre-set в 0
    cmd = CmdControlModel(femu)

    def _call(fn, r0, r1):
        from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1
        def _st(uc_, a, s, u):
            aa = a & ~1
            if not (FLASH0 <= aa < FLASH0 + 0x23680 or
                    FLASH1 <= aa < FLASH1 + 0x23680):
                uc_.emu_stop()
        sh = uc.hook_add(UC_HOOK_CODE, _st)
        try:
            uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x20)
            uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
            uc.reg_write(UC_ARM_REG_R0, r0)
            uc.reg_write(UC_ARM_REG_R1, r1)
            femu.insn = 0
            try:
                uc.emu_start(fn | 1, 0, count=50000)
            except UcError:
                pass
        finally:
            uc.hook_del(sh)
    cmd.ops.clear()
    _call(0xC664, 0x200000, 1)   # set bit21 в +0x1c
    assert any(o == 0x1c and v == 0x200000 for _, o, v in cmd.ops), \
        f'0xc664(0x200000,set) не поставил бит21 в +0x1c: {cmd.ops}'
    cmd.ops.clear()
    _call(0xC664, 0x200000, 0)   # clear bit21 (поле сейчас 0x200000)
    assert any(o == 0x1c and v == 0 for _, o, v in cmd.ops), \
        f'0xc664(0x200000,clear) не снял бит21: {cmd.ops}'


# --- B2: UsartRxCommandTable (USART3 RX-протокол = ASCII-command-ID) ---
@t(0x1E9E0, 'B2: UsartRxCommandTable — USART3 RX-протокол (BLE→MCU) = ASCII-command-ID. Парсер 0x1e9e0 (1914 Б), 15 команд @ A B C D E F G H I J K ` a c, 2 категории (@GKc=cat2 response/status; остальные=cat0xa SET-params). Таблица сверена с cmp-иммедиатами в dispatch-регионах (static-consistency).')
def _(run, rng):
    import os as _os
    import re
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
    from emulator.mcu_emu import USART_RX_COMMANDS, usart_rx_cmd
    fw_path = _os.path.join(_os.path.dirname(__file__), '..', '..', 'images', 'mcu_0007.bin')
    fw = open(fw_path, 'rb').read()
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)

    def cmd_chars(off, end):
        chars = set()
        for i in md.disasm(fw[off:end], off):
            if i.mnemonic == 'cmp':
                m = re.search(r'#(0x[0-9a-f]+|\d+)', i.op_str)
                if m:
                    imm = int(m.group(1), 0)
                    if 32 <= imm < 127:
                        chars.add(chr(imm))
        return chars
    main_chars = cmd_chars(0x1EB38, 0x1EB94)
    cat_chars = cmd_chars(0x1EA30, 0x1EA76)
    table_keys = set(USART_RX_COMMANDS.keys())
    assert main_chars == table_keys, \
        f'main dispatch {sorted(main_chars)} != table {sorted(table_keys)}'
    assert cat_chars == table_keys, \
        f'classifier {sorted(cat_chars)} != table {sorted(table_keys)}'
    for ch, (h, cat, desc) in USART_RX_COMMANDS.items():
        expect = 2 if ch in '@GKc' else 0xA
        assert cat == expect, f'{ch!r}: cat={cat:#x} != {expect:#x}'
    assert usart_rx_cmd(0x41)[0] == 0x1EC74   # 'A'
    assert usart_rx_cmd('a')[0] == 0x1F112
    assert usart_rx_cmd(0x58) is None          # 'X' — неизвестно


# --- E1: покрытие — bsearch (floor index для интерполяции) ---
@t(0x16176, 'E1: 0x16176 — i16 bsearch (floor index). 0x16176(key, arr, mid0, hi) с mid0=0 возвращает clamped lower_bound: последний i в [0,hi) с arr[i]<=key; 0 если key<arr[0]. Вериф на сортированном i16-массиве по диапазону ключей (эмулятор).')
def _(run, rng):
    arr = [10, 20, 30, 40, 50]
    ARR_OFF = 0x4000
    for i, v in enumerate(arr):
        run.ram_write(ARR_OFF + i * 2, struct.pack('<h', v))
    def clamped_lb(key):
        r = -1
        for i, v in enumerate(arr):
            if v <= key:
                r = i
        return max(0, r)
    n = 0
    for key in list(range(0, 70, 3)) + [5, 10, 25, 49, 50, 60]:
        r0, _ = run.call(0x16176, args=(key, RAM + ARR_OFF, 0, len(arr)))
        assert r0 == clamped_lb(key), f'key={key}: got {r0}, want {clamped_lb(key)}'
        n += 1
    assert n >= 25


@t(0x1619E, 'E1: 0x1619e — u32 bsearch (твин 0x16176, unsigned). Те же семантики clamped lower_bound для u32-массива (ldr [arr,mid<<2]).')
def _(run, rng):
    arr = [100, 200, 300, 400, 500]
    ARR_OFF = 0x4100
    for i, v in enumerate(arr):
        run.ram_write(ARR_OFF + i * 4, struct.pack('<I', v))
    def clamped_lb(key):
        r = -1
        for i, v in enumerate(arr):
            if v <= key:
                r = i
        return max(0, r)
    for key in [0, 50, 100, 250, 300, 499, 500, 600]:
        r0, _ = run.call(0x1619E, args=(key, RAM + ARR_OFF, 0, len(arr)))
        assert r0 == clamped_lb(key), f'key={key}: got {r0}, want {clamped_lb(key)}'


# --- C1: LutModel (LUT-блоки range-эстиматора 0x1d898) ---
@t(0x1D898, 'C1: LutModel — LUT-блоки range-эстиматора 0x1d898 @RAM+0x614 (45 слов) / RAM+0x738 (53 слова), u32-слова шаг 4. Модель ловит ЧТЕНИЯ firmware: 0x1d898 сканирует оба блока (каждое слово по разу); status-гейты @0x286/0x29e (§73.13). Тест: свежий McuEmu + battery seed -> прогон 0x1d898 -> модель зафиксировала скан обоих блоков + seed/get round-trip.')
def _(run, rng):
    from emulator.mcu_emu import (McuEmu, LutModel, RANGE_LUT0_OFF, RANGE_LUT0_WORDS,
                                  RANGE_LUT1_OFF, RANGE_LUT1_WORDS)
    femu = McuEmu(trace=False, max_insn=200000)
    uc = femu.uc
    uc.mem_write(RAM, bytes(0x20000))
    femu.hook_periph_ready()
    femu.uc.mem_write(RAM + 0x27A, struct.pack('<h', 480))   # battery середина [415..535]
    lut = LutModel(femu)

    def _st(uc_, a, s, u):
        aa = a & ~1
        if not (FLASH0 <= aa < FLASH0 + 0x23680 or
                FLASH1 <= aa < FLASH1 + 0x23680):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, _st)
    try:
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x20)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R0, 0)
        femu.insn = 0
        try:
            uc.emu_start(0x1D898 | 1, 0, count=200000)
        except UcError:
            pass
    finally:
        uc.hook_del(sh)
    assert lut.scanned(RANGE_LUT0_OFF, RANGE_LUT0_WORDS), \
        f'блок0 не просканирован: прочитано {len(lut.reads)} оффс'
    assert lut.scanned(RANGE_LUT1_OFF, RANGE_LUT1_WORDS), 'блок1 не просканирован'
    lut.set_word(RANGE_LUT0_OFF + 8, 0xDEADBEEF)
    assert lut.get_word(RANGE_LUT0_OFF + 8) == 0xDEADBEEF


# --- C2: FocPipelineModel (FOC-рутина 0x1a938 как value-gated pipeline) ---
@t(0x1A938, 'C2: FocPipelineModel — FOC-рутина 0x1a938 как value-gated pipeline (не дискретный FSM; ветвления по токам/порогам, §60.3). Выходы: P@0x388 = current-ref @0x224 (1:1), PWM-фазы @0x382/4/6 = 1125 ± ~0.0103·|ref|. Тест: seeded ref -> прогон 0x1a938 -> P==ref + фазы отклоняются от center 1125 монотонно с |ref|.')
def _(run, rng):
    from emulator.mcu_emu import (McuEmu, FocPipelineModel, FOC_ROUTINE, FOC_REF_OFF,
                                  FOC_PHASE_CENTER)

    def measure(ref):
        femu = McuEmu(trace=False, max_insn=200000)
        uc = femu.uc
        uc.mem_write(RAM, bytes(0x20000))
        femu.hook_periph_ready()
        femu.uc.mem_write(RAM + FOC_REF_OFF, struct.pack('<H', ref & 0xFFFF))
        foc = FocPipelineModel(femu)

        def _st(uc_, a, s, u):
            aa = a & ~1
            if not (FLASH0 <= aa < FLASH0 + 0x23680 or
                    FLASH1 <= aa < FLASH1 + 0x23680):
                uc_.emu_stop()
        sh = uc.hook_add(UC_HOOK_CODE, _st)
        try:
            uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x20)
            uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
            uc.reg_write(UC_ARM_REG_R0, 0)
            femu.insn = 0
            try:
                uc.emu_start(FOC_ROUTINE | 1, 0, count=200000)
            except UcError:
                pass
        finally:
            uc.hook_del(sh)
        return foc.get_p(), foc.get_phases()
    # P == ref (1:1)
    for ref in (0, 500, 2000):
        p, _ = measure(ref)
        assert p == ref, f'ref={ref}: P@0x388={p} != ref'
    # фазы: center при ref=0; spread монотонно растёт с |ref|
    def spread(ref):
        _, ph = measure(ref)
        return max(abs(p - FOC_PHASE_CENTER) for p in ph)
    s0, s500, s2000 = spread(0), spread(500), spread(2000)
    assert s0 <= 2, f'ref=0 фазы не center: spread={s0}'
    assert s2000 > s500 > 0, f'spread не монотонен: 500={s500}, 2000={s2000}'


# --- D1: SchedulerModel (main-loop диспетчер 0x1f600) ---
@t(0x1F600, 'D1: SchedulerModel — main-loop диспетчер 0x1f600 (round-robin по N слотам). Ловит состояние (slot_index @0x2C2, slot-table @0xA43 stride 0x96, tick-слова @0x17F78+). ПОТОЛОК §74.1: task function-pointers runtime; в нулевом RAM dispatch упирается в unmapped fetch (jump to 0). Тест: seeded slot_index=1 -> прогон 0x1f600 -> модель зафиксировала чтение slot-index + tick-регионов (pre-dispatch логика).')
def _(run, rng):
    from emulator.mcu_emu import (McuEmu, SchedulerModel, SCHEDULER_FN,
                                  SCHED_SLOT_INDEX_OFF, SCHED_TICK_WORDS_OFF)
    femu = McuEmu(trace=False, max_insn=50000)
    uc = femu.uc
    uc.mem_write(RAM, bytes(0x20000))
    femu.hook_periph_ready()
    sch = SchedulerModel(femu)
    sch.set_slot_index(1)   # != compare-byte 0 -> dispatch path

    def _st(uc_, a, s, u):
        aa = a & ~1
        if not (FLASH0 <= aa < FLASH0 + 0x23680 or
                FLASH1 <= aa < FLASH1 + 0x23680):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, _st)
    try:
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x20)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R0, 0)
        femu.insn = 0
        try:
            uc.emu_start(SCHEDULER_FN | 1, 0, count=50000)
        except UcError:
            pass
    finally:
        uc.hook_del(sh)
    # ядро состояния: диспетчер прочитал slot-index @0x2C2 (стабильно в zeroed и
    # dispatch-path; tick/state-регионы path-dependent — 0x17F78+ / 0x1E0+ по ветке)
    assert sch.touched(SCHED_SLOT_INDEX_OFF) or \
        sch.touched(SCHED_SLOT_INDEX_OFF - 1), \
        f'slot-index не прочитан: {sorted(hex(o) for o in sch.reads if 0x2C0 <= o < 0x2D0)}'


# --- E1: CRC-7 примитив 0x3c7c (ядро §50 I2C stream-кодека) ---
@t(0x3C7C, 'E1: 0x3c7c — CRC-7 примитив (ядро §50 I2C stream-кодека). 0x3c7c(byte=r0, prev=r1) -> r0: crc=(prev^byte)&0xFF; 8 бит MSB-first: if MSB -> ((crc<<1)&0xFF)^0x07 else (crc<<1)&0xFF. Poly=0x07, no reflect/xorout, init=prev. Вериф sweep byte×prev vs независимая реализация.')
def _(run, rng):
    def crc7(b, prev):
        crc = (prev ^ b) & 0xFF
        for _ in range(8):
            crc = ((crc << 1) & 0xFF) ^ 0x07 if (crc & 0x80) else (crc << 1) & 0xFF
        return crc
    n = 0
    for b in range(0, 256, 3):
        for prev in (0, 0x11, 0x7F, 0xB2, 0xFF):
            r0, _ = run.call(0x3C7C, args=(b, prev))
            assert r0 == crc7(b, prev), \
                f'b={b:#04x} prev={prev:#04x}: got {r0:#04x} want {crc7(b, prev):#04x}'
            n += 1
    assert n >= 40


# --- E2: periph-write-trace facility ---
@t(0x1BF48, 'E2: periph-write-trace facility — McuEmu.periph_write_map() / periph_writes_since(). Захват periph-writes на функцию для верификации «функция пишет в регистр Y». Тест: прогон мотор-инит 0x1bf48 (221 запись) -> periph_write_map() содержит motor-TIM @0x40012C00 + GPIO-блок @0x48000000; periph_writes_since(mark) = окно вызова.')
def _(run, rng):
    from emulator.mcu_emu import McuEmu, RAM, FLASH0, FLASH1, STACK_TOP
    femu = McuEmu(trace=False, max_insn=500000)
    uc = femu.uc
    uc.mem_write(RAM, bytes(0x20000))
    femu.hook_periph_ready()
    mark = len(femu.periph_writes)

    def _st(uc_, a, s, u):
        aa = a & ~1
        if not (FLASH0 <= aa < FLASH0 + 0x23680 or
                FLASH1 <= aa < FLASH1 + 0x23680):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, _st)
    try:
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x20)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        femu.insn = 0
        try:
            uc.emu_start(0x1BF48 | 1, 0, count=500000)
        except UcError:
            pass
    finally:
        uc.hook_del(sh)
    wm = femu.periph_write_map()
    assert any(0x40012C00 <= a < 0x40012D00 for a in wm), \
        f'motor-TIM @0x40012C00 не в map: {sorted(hex(a) for a in wm)[:8]}'
    assert any(0x48000000 <= a < 0x48001000 for a in wm), 'GPIO-блок @0x48000000 не в map'
    tail = femu.periph_writes_since(mark)
    assert len(tail) == len(femu.periph_writes) - mark and len(tail) >= 100, \
        f'periph_writes_since: {len(tail)} (ожидал >=100)'


# --- E1 continuation: checksum + divisibility 0x16410 ---
@t(0x16410, 'E1: 0x16410 — checksum + divisibility. 0x16410(arg0=r0, arg1=r1, arg2=r2) -> r0 = sum(block[:arg1]) + arg2 + flag; block=00 1f 1c 1f 1e 1f 1e 1f 1f 1e 1f 1e (embedded 12B из пула); flag добавляется только если arg1>2: a0%4!=0->0, a0%100!=0->1, a0%400!=0->0, else->1. Вериф sweep (arg0,arg1,arg2).')
def _(run, rng):
    BLOCK = bytes([0x00, 0x1f, 0x1c, 0x1f, 0x1e, 0x1f, 0x1e, 0x1f, 0x1f, 0x1e, 0x1f, 0x1e])

    def flag(a0):
        if a0 % 4 != 0:
            return 0
        if a0 % 100 != 0:
            return 1
        if a0 % 400 != 0:
            return 0
        return 1
    n = 0
    for a0 in (0, 2, 3, 4, 8, 96, 99, 100, 196, 200, 300, 396, 400, 500, 796, 800):
        for a1 in (1, 2, 3, 5, 12):
            for a2 in (0, 7, 123):
                exp = (sum(BLOCK[:a1]) + a2 + (flag(a0) if a1 > 2 else 0)) & 0xFFFFFFFF
                r0, _ = run.call(0x16410, args=(a0, a1, a2))
                assert r0 == exp, f'a0={a0} a1={a1} a2={a2}: got {r0:#x} want {exp:#x}'
                n += 1
    assert n >= 100


# --- E1 continuation: CRC-7 stream encoder 0x15640 ---
@t(0x15640, 'E1: 0x15640 — CRC-7 stream-кодер §50 I2C. 0x15640(arg0=r0, arg1=r1, src=r2, dst=r3, len=[pre_sp+0]): warmup r7=crc7(a1,crc7(a0,0)); для каждого src[i]: dst[2i]=src[i], dst[2i+1]=crc7(src[i], r7 if i==0 else 0) — первый CRC цепляется от warmup, остальные сброс в init=0. Примитив crc7 = 0x3c7c (poly=0x07 MSB-first). Вериф manual-call (len в стек, push=8 рег=0x20).')
def _(run, rng):
    from emulator.mcu_emu import McuEmu as _M, RAM as _R, FLASH0 as _F0, \
        FLASH1 as _F1, STACK_TOP as _ST

    def crc7(b, prev):
        crc = (prev ^ b) & 0xFF
        for _ in range(8):
            crc = ((crc << 1) & 0xFF) ^ 0x07 if (crc & 0x80) else (crc << 1) & 0xFF
        return crc

    def encode(a0, a1, src):
        r7 = crc7(a1 & 0xFF, crc7(a0 & 0xFF, 0))
        out = []
        for i, b in enumerate(src):
            out.append(b)
            r7 = crc7(b, r7 if i == 0 else 0)
            out.append(r7)
        return bytes(out)

    def run_enc(a0, a1, src):
        emu = _M(max_insn=50000)
        uc = emu.uc
        uc.mem_write(_R, bytes(0x20000))
        emu.hook_periph_ready()
        SRC = _R + 0x4000
        DST = _R + 0x4100
        for i, b in enumerate(src):
            uc.mem_write(SRC + i, bytes([b]))
        pre_sp = _ST - 0x40
        uc.mem_write(pre_sp, struct.pack('<I', len(src)))

        def _st(uc_, a, s, u):
            aa = a & ~1
            if not (_F0 <= aa < _F0 + 0x23680 or _F1 <= aa < _F1 + 0x23680):
                uc_.emu_stop()
        sh = uc.hook_add(UC_HOOK_CODE, _st)
        try:
            uc.reg_write(UC_ARM_REG_SP, pre_sp)
            uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
            uc.reg_write(UC_ARM_REG_R0, a0)
            uc.reg_write(UC_ARM_REG_R1, a1)
            uc.reg_write(UC_ARM_REG_R2, SRC)
            uc.reg_write(UC_ARM_REG_R3, DST)
            emu.insn = 0
            try:
                uc.emu_start(0x15640 | 1, 0, count=50000)
            except UcError:
                pass
        finally:
            uc.hook_del(sh)
        return bytes(uc.mem_read(DST, 2 * len(src)))
    n = 0
    for (a0, a1, src) in [(0xAA, 0xBB, [1, 2, 3]), (0x11, 0x22, [0xDE, 0xAD]),
                           (0x00, 0x00, [5, 6, 7, 8]), (0xFF, 0x01, [0x41]),
                           (0x3C, 0x7D, [0x12, 0x34, 0x56])]:
        exp = encode(a0, a1, src)
        got = run_enc(a0, a1, src)
        assert got == exp, f'a0={a0:#04x} a1={a1:#04x}: got {got.hex()} want {exp.hex()}'
        n += 1
    assert n >= 5


# --- E1: 0x15a60 close-out — helpers strlen/memcmp + buffer processor ---
def _fresh_call(off, args=(), extra_ram=None, max_insn=50000, extra_mem=None):
    """Свежий McuEmu + ручной call (чистый RAM, без shared-state). Возвращает (r0, emu).
    extra_ram: [(RAM_abs_addr, bytes)] — pre-set в RAM.
    extra_mem: [(any_abs_addr, bytes)] — pre-set в ЛЮБОЙ адрес (periph и т.п.)."""
    from emulator.mcu_emu import McuEmu as _M, RAM as _R, FLASH0 as _F0, \
        FLASH1 as _F1, STACK_TOP as _ST
    emu = _M(max_insn=max_insn)
    uc = emu.uc
    uc.mem_write(_R, bytes(0x20000))
    emu.hook_periph_ready()
    if extra_ram:
        for (addr, data) in extra_ram:
            uc.mem_write(addr, data)
    if extra_mem:
        for (addr, data) in extra_mem:
            uc.mem_write(addr, data)

    def _st(uc_, a, s, u):
        aa = a & ~1
        if not (_F0 <= aa < _F0 + 0x23680 or _F1 <= aa < _F1 + 0x23680):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, _st)
    try:
        uc.reg_write(UC_ARM_REG_SP, _ST - 0x40)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        for r, v in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                         UC_ARM_REG_R3), args):
            uc.reg_write(r, v)
        emu.insn = 0
        try:
            uc.emu_start(off | 1, 0, count=max_insn)
        except UcError:
            pass
        r0 = uc.reg_read(UC_ARM_REG_R0)
    finally:
        uc.hook_del(sh)
    return r0, emu


@t(0x11EC, 'E1: 0x11ec — strlen (null-terminated). 0x11ec(src=r0) -> r0 = число байтов до первого null. Помощник 0x15a60 (§87). Вериф sweep.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    ok = 0
    for s in (b'', b'a', b'abc', b'hello', b'ab\x00cd'):
        p = _R + 0x3000
        r0, _emu = _fresh_call(0x11EC, args=(p,), extra_ram=[(p, s + b'\x00')])
        exp = s.find(b'\x00') if b'\x00' in s else len(s)
        assert r0 == exp, f'{s!r}: got {r0} want {exp}'
        ok += 1
    assert ok >= 5


@t(0x11FA, 'E1: 0x11fa — bounded-memcmp. 0x11fa(A=r0, B=r1, n=r2) -> r0 = A[i]-B[i] на первом несовпадении (i<n); 0 на полное совпадение или когда ОБА null на той же позиции (ранний выход). Помощник 0x15a60 (§87). Вериф sweep.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    cases = [(b'abc', b'abc', 3, 0), (b'abc', b'abd', 3, -1),
             (b'ab', b'abc', 2, 0), (b'a\x00z', b'a\x00w', 3, 0),
             (b'a\x00x', b'ayz', 3, -ord('y')), (b'abcd', b'abce', 4, -1),
             (b'zyx', b'abc', 3, ord('z') - ord('a'))]
    for A, B, n, exp in cases:
        pa = _R + 0x3100
        pb = _R + 0x3200
        r0, _emu = _fresh_call(0x11FA, args=(pa, pb, n),
                               extra_ram=[(pa, A + b'\x00\x00'), (pb, B + b'\x00\x00')])
        got = r0 if r0 < 0x80000000 else r0 - 0x100000000
        assert got == exp, f'A={A!r} B={B!r} n={n}: got {got} want {exp}'


@t(0x15A60, 'E1: 0x15a60 — USART/DFU command/data buffer processor (§87). (src=r0, len=r1): рабочий буфер @RAM+0x1f10 (memset 0x11d6->0x11c8), TBL1=flash@0x1a93c (7×50B binary-паттерны; strlen через 0x11ec). Path A (len<=0x32): buf[0]=src[0], return 0. Path B (len>0x32): гейт src[0]==1 -> копирует src в буфер; иначе early-return 0 (только buf[0]=src[0]). Вериф детерминированного поведения.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    SRC = _R + 0x4000
    src_a = bytes([0x11, 0x22, 0x33, 0x44])
    r0, emu = _fresh_call(0x15A60, args=(SRC, len(src_a)),
                          extra_ram=[(SRC, src_a)])
    buf = bytes(emu.uc.mem_read(_R + 0x1F10, 8))
    assert r0 == 0 and buf[0] == 0x11 and buf[1] == 0, \
        f'pathA: return={r0:#x} buf={buf.hex()}'
    src_b = bytes([0x05, 0x22, 0x33] + [0x55] * 60 + [0x77, 0x88])
    r0, emu = _fresh_call(0x15A60, args=(SRC, len(src_b)),
                          extra_ram=[(SRC, src_b)])
    buf = bytes(emu.uc.mem_read(_R + 0x1F10, 8))
    assert r0 == 0 and buf[0] == 0x05 and buf[1] == 0, \
        f'pathB gate-fail: return={r0:#x} buf={buf.hex()}'
    src_c = bytes([0x01, 0x22, 0x33] + [0x55] * 60 + [0x77, 0x88])
    r0, emu = _fresh_call(0x15A60, args=(SRC, len(src_c)),
                          extra_ram=[(SRC, src_c)])
    buf = bytes(emu.uc.mem_read(_R + 0x1F10, 8))
    assert r0 == 0 and buf[:4] == src_c[:4], \
        f'pathB gate-pass: return={r0:#x} buf={buf.hex()} want {src_c[:4].hex()}'


# --- E2-batch1: пофункционная кампания — чистые/простые функции ---
@t(0x01E34, 'E2-b1: 0x01e34 — сумма байтов mod 256. 0x01e34(ptr=r0, n=r1) -> r0 = (Σ buf[i], i=0..n-1) & 0xFF. Чистая функция. Вериф 4/4.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    ok = 0
    for buf, n in [([1, 2, 3, 4, 5], 5), ([250, 250], 2),
                   ([0] * 3, 3), ([7, 8, 9, 10], 4)]:
        p = _R + 0x3000
        r0, _emu = _fresh_call(0x01E34, args=(p, n), extra_ram=[(p, bytes(buf))])
        assert r0 == (sum(buf) & 0xFF), f'buf={buf}: got {r0} want {sum(buf) & 0xFF}'
        ok += 1
    assert ok >= 4


@t(0x015AA, 'E2-b1: 0x015aa — packed-field setter. 0x015aa(struct=r0, field_id=r1, selector=r2, value=r3): 3-бит поле (из value): id==0x12->[+0x5c]b[2:0]; id>9->[+0xc]b[(id-0xa)*3..3]; id<=9->[+0x10]b[id*3..3]. 5-бит поле (из field_id), по selector: <7->[+0x34]b[(sel-1)*5..5]; <0xd->[+0x30]b[(sel-7)*5..5]; else->[+0x2c]b[(sel-0xd)*5..5]. Чистая (struct в r0). Вериф 6/6.')
def _(run, rng):
    import struct as _st
    from emulator.mcu_emu import RAM as _R
    S = _R + 0x3000

    def runf(r1, r5, r3):
        emu = _fresh_call(0x015AA, args=(S, r1, r5, r3))[1]
        u32 = lambda off: _st.unpack('<I', bytes(emu.uc.mem_read(S + off, 4)))[0]
        return u32(0x5c), u32(0xc), u32(0x10), u32(0x34), u32(0x30), u32(0x2c)
    # 3-бит: id==0x12 -> [0x5c] low3 = value
    assert runf(0x12, 1, 5)[0] == 5
    # 3-бит: id<=9 -> [0x10] bit(id*3) w3 = value
    assert runf(2, 1, 7)[2] == (7 & 7) << 6
    # 3-бит: id>9 -> [0xc] bit((id-0xa)*3) w3 = value
    assert runf(0xb, 1, 4)[1] == (4 & 7) << 3
    # 5-бит: selector<7 -> [0x34] bit((sel-1)*5) w5 = field_id
    assert runf(20, 1, 0)[3] == (20 & 0x1F)
    # 5-бит: selector in [7,0xd) -> [0x30] bit((sel-7)*5) w5 = field_id
    assert runf(30, 8, 0)[4] == (30 & 0x1F) << 5
    # 5-бит: selector>=0xd -> [0x2c] bit((sel-0xd)*5) w5 = field_id
    assert runf(9, 0xe, 0)[5] == (9 & 0x1F) << 5


def _intercept(off, target, max_insn=20000, arg=None, args=None, extra_ram=None):
    """Свежий McuEmu; стоп на входе bl-цели `target`, снимаем R0-R3. -> (dict, emu).

    Для тонких делегаторов: верифицируем, что функция вызывает хелпер с нужными аргументами.
    `args` — кортеж для R0-R3; иначе `arg` — только R0 (по умолчанию 0).
    `extra_ram` — [(addr, bytes)], досев RAM перед запуском (для stateful-гейтов)."""
    from emulator.mcu_emu import McuEmu as _M, RAM as _R, FLASH0 as _F0, \
        FLASH1 as _F1, STACK_TOP as _ST
    emu = _M(max_insn=max_insn)
    uc = emu.uc
    uc.mem_write(_R, bytes(0x20000))
    emu.hook_periph_ready()
    if extra_ram:
        for (addr, data) in extra_ram:
            uc.mem_write(addr, data)
    cap = {}

    def _code(uc_, a, s, u):
        if a == target or a == (target & ~1):
            for nm, r in (('r0', UC_ARM_REG_R0), ('r1', UC_ARM_REG_R1),
                          ('r2', UC_ARM_REG_R2), ('r3', UC_ARM_REG_R3)):
                cap[nm] = uc_.reg_read(r)
            uc_.emu_stop()
            return
        aa = a & ~1
        if not (_F0 <= aa < _F0 + 0x23680 or _F1 <= aa < _F1 + 0x23680):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, _code)
    try:
        uc.reg_write(UC_ARM_REG_SP, _ST - 0x40)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3):
            uc.reg_write(r, 0)
        if args is not None:
            for r, v in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                             UC_ARM_REG_R3), args):
                uc.reg_write(r, v)
        elif arg is not None:
            uc.reg_write(UC_ARM_REG_R0, arg)
        emu.insn = 0
        try:
            uc.emu_start(off | 1, 0, count=max_insn)
        except UcError:
            pass
    finally:
        uc.hook_del(sh)
    return cap, emu


# --- E2-batch2: I2C2-wr семья (22 тонких делегатора -> 0x1c61) ---
# Контракт (вериф bl-intercept): 0x1c61(op=8, reg=r1, buf=&u32@0x16XX=r2, len=r3).
_I2C2_WR = {
    0x020c4: (0x38, 2), 0x02138: (0x36, 2), 0x021dc: (0x12, 2), 0x021f0: (0x14, 2),
    0x02204: (0x16, 2), 0x02218: (0x18, 2), 0x0222c: (0x1a, 2), 0x02240: (0x1c, 2),
    0x02254: (0x1e, 2), 0x02268: (0x20, 2), 0x0227c: (0x22, 2), 0x02290: (0x24, 2),
    0x022a4: (0x26, 2), 0x022b8: (0x28, 2), 0x022cc: (0x2a, 2), 0x022e0: (0x32, 2),
    0x022f4: (0x3a, 2), 0x02308: (0x7f, 1), 0x0231c: (0x3, 1), 0x02330: (0x5, 1),
    0x02344: (0x7, 1), 0x02358: (0x70, 2),
}


def _mk_i2c2_wr(addr, reg, ln):
    def _test(run, rng):
        from emulator.mcu_emu import RAM as _R
        cap, _emu = _intercept(addr, 0x1C61)
        assert cap.get('r0') == 8, f'0x{addr:05x}: r0={cap.get("r0"):#x} want 0x8'
        assert cap.get('r1') == reg, f'0x{addr:05x}: reg={cap.get("r1"):#x} want 0x{reg:x}'
        assert cap.get('r3') == ln, f'0x{addr:05x}: len={cap.get("r3")} want {ln}'
        assert cap.get('r2', 0) >= _R, f'0x{addr:05x}: buf не в RAM'
    return _test


for _addr, (_reg, _ln) in sorted(_I2C2_WR.items()):
    t(_addr, f'E2-b2: I2C2-wr 0x{_addr:05x} -> 0x1c61(op=8, reg=0x{_reg:x}, len={_ln}) [bl-intercept]')(_mk_i2c2_wr(_addr, _reg, _ln))


# --- E2-batch3: median (выборка) + I2C2-read делегатор ---
@t(0x0170C, 'E2-b3: 0x0170c — выборка ADC-сэмпла по индексу. 0x0170c(arg=r0) -> r0 = u16[RAM+0xB7E + arg*2] (arg<2). Копирует выбранный сэмпл в 7 слотов локального массива, sort+center (no-op на константе) -> возвращает его. Каталог «медиана из 7» неточен. Вериф 10/10.')
def _(run, rng):
    import struct as _st
    from emulator.mcu_emu import RAM as _R
    for arg in (0, 1):
        for _ in range(3):
            vals = [rng.getrandbits(16) for _ in range(7)]
            r0, _emu = _fresh_call(0x0170C, args=(arg,),
                                   extra_ram=[(_R + 0xB7E, _st.pack('<7H', *vals))])
            assert r0 == vals[arg], f'arg={arg}: got {r0:#x} want {vals[arg]:#x}'


@t(0x01BDC, 'E2-b3: 0x01bdc — I2C2 read (code16). 0x01bdc(code=r0) -> bl 0x1e73(op=8, dev=0x3e, r2=1, buf=[sp+4]); buf = [code&0xFF, code>>8] (LE). Вериф bl-intercept.')
def _(run, rng):
    for code in (0x1234, 0xABCD, 0x00FF):
        cap, emu = _intercept(0x01BDC, 0x1E73, arg=code)
        assert cap.get('r0') == 8 and cap.get('r1') == 0x3e and cap.get('r2') == 1, \
            f'code={code:#06x}: {cap}'
        buf = bytes(emu.uc.mem_read(cap['r3'], 2))
        assert buf == code.to_bytes(2, 'little'), f'code={code:#06x}: buf={buf.hex()}'


@t(0x01C1C, 'E2-b4: 0x01c1c — I2C2 read (code16, base). 0x01c1c(code=r0) -> bl 0x90a1(r0=0x40005800 [I2C2 base], op=8, dev=0x3e, buf=[sp+4]); buf=LE code. Вериф bl-intercept.')
def _(run, rng):
    for code in (0x1234, 0xABCD):
        cap, emu = _intercept(0x01C1C, 0x90A1, arg=code)
        assert cap.get('r0') == 0x40005800 and cap.get('r1') == 8 \
            and cap.get('r2') == 0x3e, f'code={code:#06x}: {cap}'
        buf = bytes(emu.uc.mem_read(cap['r3'], 2))
        assert buf == code.to_bytes(2, 'little'), f'code={code:#06x}: buf={buf.hex()}'


@t(0x01C7A, 'E2-b4: 0x01c7a — I2C2 read (arg0, code16). 0x01c7a(a0=r0, code=r1) -> bl 0x1e73(r0=a0, dev=0x3e, r2=1, buf=[sp+4]); buf=LE code. Вериф bl-intercept.')
def _(run, rng):
    for a0, code in ((0x55, 0x1234), (0xAA, 0xBE01)):
        cap, emu = _intercept(0x01C7A, 0x1E73, args=(a0, code))
        assert cap.get('r0') == a0 and cap.get('r1') == 0x3e \
            and cap.get('r2') == 1, f'a0={a0:#x} code={code:#06x}: {cap}'
        buf = bytes(emu.uc.mem_read(cap['r3'], 2))
        assert buf == code.to_bytes(2, 'little'), f'code={code:#06x}: buf={buf.hex()}'


@t(0x0218C, 'E2-b5: 0x0218c — I2C read reg 0x83. 0x0218c() -> bl 0x1c7b(op=8, reg=0x83, buf=&RAM, len=2); результат -> u16@0xB42 (если != 0xFFFF). Вериф bl-intercept.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    cap, emu = _intercept(0x0218C, 0x1C7B)
    assert cap.get('r0') == 8 and cap.get('r1') == 0x83 and cap.get('r3') == 2, f'{cap}'
    assert cap.get('r2', 0) >= _R, f'buf не в RAM: {cap}'


# --- E2-batch6: I2C2-read цепочки (тонкие делегаторы) ---
@t(0x01C60, 'E2-b6: 0x01c60 — I2C2-цепочка #1. 0x01c60() -> bl 0x1e53(r0=0, r1=0, r2=1, r3=0) [нулевой RAM-state]. Вериф bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x01C60, 0x1E53)
    assert (cap.get('r0'), cap.get('r1'), cap.get('r2'), cap.get('r3')) == (0, 0, 1, 0), f'{cap}'


@t(0x01E52, 'E2-b6: 0x01e52 — I2C2-цепочка #2. 0x01e52() -> bl 0x214d(r0=0, r1=0, r2=0, r3=0) [нулевой RAM-state]. Вериф bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x01E52, 0x214D)
    assert (cap.get('r0'), cap.get('r1'), cap.get('r2'), cap.get('r3')) == (0, 0, 0, 0), f'{cap}'


@t(0x01E72, 'E2-b6: 0x01e72 — I2C2-цепочка #3. 0x01e72() -> bl 0x2731(r0=0, r1=0, r2=0, r3=0) [нулевой RAM-state]. Вериф bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x01E72, 0x2731)
    assert (cap.get('r0'), cap.get('r1'), cap.get('r2'), cap.get('r3')) == (0, 0, 0, 0), f'{cap}'


# --- E2-batch7: CRC-семья (чистые чексаумы, вериф по Python-референсу) ---
def _crc32z(b):
    import zlib
    return zlib.crc32(b) & 0xFFFFFFFF


def _crc16_1021(b, init=0):
    c = init
    for x in b:
        c ^= x << 8
        for _ in range(8):
            c = ((c << 1) ^ 0x1021) & 0xFFFF if c & 0x8000 else (c << 1) & 0xFFFF
    return c


def _crc16_a001(b):
    c = 0xFFFF
    for x in b:
        c ^= x
        for _ in range(8):
            c = (c >> 1) ^ 0xA001 if c & 1 else c >> 1
    return (~c) & 0xFFFF


_CRC_BUFS = [b'', b'123456789', b'\x00\x01\x02', b'hello world', bytes(range(20))]


@t(0x03C04, 'E2-b7: 0x03c04 — CRC-32/zlib. 0x03c04(buf=r0, len=r1, init=r2) -> r0 = crc32 (init=0 -> 0xFFFFFFFF). Вериф по zlib 5/5.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    P = _R + 0x3000
    for b in _CRC_BUFS:
        r0, _emu = _fresh_call(0x03C04, args=(P, len(b), 0), extra_ram=[(P, b)])
        assert (r0 & 0xFFFFFFFF) == _crc32z(b), f'{b!r}: got {r0:#x} want {_crc32z(b):#x}'


@t(0x03B82, 'E2-b7: 0x03b82 — CRC-16 0x1021 MSB-first (init=0). 0x03b82(buf=r0, len=r1) -> r0 = u16 crc. Вериф 5/5.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    P = _R + 0x3000
    for b in _CRC_BUFS:
        r0, _emu = _fresh_call(0x03B82, args=(P, len(b)), extra_ram=[(P, b)])
        assert (r0 & 0xFFFF) == _crc16_1021(b), f'{b!r}: got {r0:#x} want {_crc16_1021(b):#x}'


@t(0x03BC4, 'E2-b7: 0x03bc4 — CRC-16 0x1021 MSB-first (init в r0). 0x03bc4(init=r0, buf=r1, len=r2) -> r0 = u16 crc. Вериф 5/5.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    P = _R + 0x3000
    for b in _CRC_BUFS:
        r0, _emu = _fresh_call(0x03BC4, args=(0, P, len(b)), extra_ram=[(P, b)])
        assert (r0 & 0xFFFF) == _crc16_1021(b), f'{b!r}: got {r0:#x} want {_crc16_1021(b):#x}'


@t(0x03B42, 'E2-b7: 0x03b42 — CRC-16 отражённый (poly 0xA001, init 0xFFFF, xorout ~). 0x03b42(buf=r0, len=r1) -> r0 = u16 crc. Вериф 5/5.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    P = _R + 0x3000
    for b in _CRC_BUFS:
        r0, _emu = _fresh_call(0x03B42, args=(P, len(b)), extra_ram=[(P, b)])
        assert (r0 & 0xFFFF) == _crc16_a001(b), f'{b!r}: got {r0:#x} want {_crc16_a001(b):#x}'


# --- E2-batch8: табличные CRC-16 (референс из flash-памяти emu) ---
@t(0x03C4C, 'E2-b8: 0x03c4c — CRC-16 табличный. 0x03c4c(buf=r0,len=r1)->u16; tbl@flash 0x19784 (256 u16); idx=byte^(crc>>8); crc=(tbl[idx]^(crc<<8))&0xFFFF. Вериф по flash-таблице 5/5.')
def _(run, rng):
    import struct as _st
    from emulator.mcu_emu import RAM as _R, FLASH0 as _F0
    P = _R + 0x3000
    tbl = _st.unpack('<256H', bytes(run.emu.uc.mem_read(_F0 + 0x19784, 512)))
    for b in _CRC_BUFS:
        r0, _emu = _fresh_call(0x03C4C, args=(P, len(b)), extra_ram=[(P, b)])
        c = 0
        for x in b:
            c = (tbl[x ^ (c >> 8)] ^ (c << 8)) & 0xFFFF
        assert (r0 & 0xFFFF) == c, f'{b!r}: got {r0:#x} want {c:#x}'


@t(0x08A50, 'E2-b8: 0x08a50 — dual-table CRC-16. 0x08a50(buf=r0,len=r1)->u16; t1@flash 0x19584 (high), t2@0x19684 (low); hi=lo=0xFF; idx=byte^hi; hi=t1[idx]^lo; lo=t2[idx]; crc=(hi<<8)|lo. Вериф по flash-таблицам 5/5.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R, FLASH0 as _F0
    P = _R + 0x3000
    t1 = bytes(run.emu.uc.mem_read(_F0 + 0x19584, 256))
    t2 = bytes(run.emu.uc.mem_read(_F0 + 0x19684, 256))
    for b in _CRC_BUFS:
        r0, _emu = _fresh_call(0x08A50, args=(P, len(b)), extra_ram=[(P, b)])
        hi = lo = 0xFF
        for x in b:
            i = x ^ hi
            hi = t1[i] ^ lo
            lo = t2[i]
        c = ((hi << 8) & 0xFF00) | lo
        assert (r0 & 0xFFFF) == c, f'{b!r}: got {r0:#x} want {c:#x}'


# --- E2-batch9: byte bit-permutation + NOT ---
@t(0x0BF58, 'E2-b9: 0x0bf58 — byte bit-permutation + NOT. 0x0bf58(ptr=r0, sel=r1, mode=r2), mode=1: out=RAM+0x17F9C = ~((b1<<3)|(b0<<2)|(b3<<1)|b2)&0xFF, затем маска по sel (0->0xFE,1->0xFD,2->0xFB,3->0xF7; иначе 0xFF); bN=бит N байта [ptr]. Функция также инициализирует соседний struct. Вериф по формуле.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    P = _R + 0x3000

    def bitperm(b, sel):
        p = (~(((b >> 1) & 1) << 3 | (b & 1) << 2 | ((b >> 3) & 1) << 1
               | ((b >> 2) & 1))) & 0xFF
        m = {0: 0xFE, 1: 0xFD, 2: 0xFB, 3: 0xF7}
        return p & m[sel] if sel in m else 0xFF
    for b in (0x00, 0xFF, 0x5A, 0xA5, 0x12):
        for sel in range(4):
            _r0, emu = _fresh_call(0x0BF58, args=(P, sel, 1),
                                   extra_ram=[(P, bytes([b]))])
            out = emu.uc.mem_read(_R + 0x17F9C, 1)[0]
            assert out == bitperm(b, sel), \
                f'b={b:#04x} sel={sel}: got {out:#x} want {bitperm(b, sel):#x}'


# --- E2-batch10: RCC/DMA init-делегаторы (bl-intercept первого хелпера) ---
@t(0x01580, 'E2-b10: 0x01580 — RCC ext init. Первый вызов -> 0xc491(r0=0x100). bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x01580, 0xC491)
    assert cap.get('r0') == 0x100, f'{cap}'


@t(0x01940, 'E2-b10: 0x01940 — RCC ext init #2. Первый вызов -> 0xc625(r0=1, r1=1). bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x01940, 0xC625)
    assert cap.get('r0') == 1 and cap.get('r1') == 1, f'{cap}'


@t(0x016D4, 'E2-b10: 0x016d4 — DMA1 reset. Первый вызов -> 0x1941(r0=0) [RCC clock-enable пролог]. bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x016D4, 0x1941)
    assert cap.get('r0') == 0, f'{cap}'


@t(0x0175C, 'E2-b10: 0x0175c — DMA1 enable. Первый вызов -> 0x1941(r0=0) [пролог]; затем цикл i<2: 0x1859/0x1671/0x18fd. bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x0175C, 0x1941)
    assert cap.get('r0') == 0, f'{cap}'


# --- E2-batch11: flash region validator + I2C2 wr ---
@t(0x080AC, 'E2-b11: 0x080ac — flash region validator. 0x080ac(base=r0, buf=r1, len=r2): return 0 если base не по align 0x800, buf==0, len==0, len>0x800, len%4!=0, или base вне [lo,hi). Вериф гейтов (5 невалидных -> 0).')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    P = _R + 0x4000
    for base, ln in ((0x8003000, 0), (0x8003000, 0x1000), (0x8003000, 6),
                     (0x8003001, 4)):
        r0, _emu = _fresh_call(0x080AC, args=(base, P, ln))
        assert r0 == 0, f'base={base:#x} len={ln:#x}: got {r0:#x} want 0'
    r0, _emu = _fresh_call(0x080AC, args=(0x8003000, 0, 4))
    assert r0 == 0, 'buf=0: got non-zero'


@t(0x02770, 'E2-b11: 0x02770 — I2C2 wr (code16,val16,len=4). 0x02770() -> bl 0x90a1(r0=0x40005800 [I2C2 base], dev=0x3e, buf). bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x02770, 0x90A1)
    assert cap.get('r0') == 0x40005800 and cap.get('r2') == 0x3E, f'{cap}'


# --- E2-batch12: CRC-32-обёртка + I2C-like + event varargs ---
@t(0x03940, 'E2-b12: 0x03940 — CRC-32 обёртка. 0x03940() -> bl 0x3c04(r0=0x8000000 [flash addr], r1=0x3000 [len], r2=0) -> u32@0xCC. bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x03940, 0x3C05)
    assert cap.get('r0') == 0x8000000 and cap.get('r1') == 0x3000, f'{cap}'


@t(0x02E84, 'E2-b12: 0x02e84 — I2C-подобный запрос. 0x02e84() -> bl 0x9874(r1=0x20000). bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x02E84, 0x9875)
    assert cap.get('r1') == 0x20000, f'{cap}'


@t(0x0307C, 'E2-b12: 0x0307c — event varargs {b,b,b,1}. 0x0307c() -> bl 0xc0b4 (event dispatch, r0=указатель на stack-буфер). bl-intercept (достигает хелпера).')
def _(run, rng):
    cap, _emu = _intercept(0x0307C, 0xC0B5)
    assert 'r0' in cap, f'не достиг 0xc0b4: {cap}'


# --- E2-batch13: poll / I2C init / telemetry reset / GPIO init (bl-intercept) ---
@t(0x04E08, 'E2-b13: 0x04e08 — poll. 0x04e08() -> bl 0x1bdc(r0=0x94) + задержка. bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x04E08, 0x1BDD)
    assert cap.get('r0') == 0x94, f'{cap}'


@t(0x05FB4, 'E2-b13: 0x05fb4 — I2C init. 0x05fb4() -> 0x5a38() + задержка + bl 0x1c1c(r0=0x92). bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x05FB4, 0x1C1D)
    assert cap.get('r0') == 0x92, f'{cap}'


@t(0x09AA4, 'E2-b13: 0x09aa4 — телеметрия reset. zero @0x1344 + bl 0x11d6(r0=RAM+0x1384, r1=0x4a). bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x09AA4, 0x11D7)
    assert cap.get('r0') == 0x20001384 and cap.get('r1') == 0x4A, f'{cap}'


@t(0x05B98, 'E2-b13: 0x05b98 — GPIO init. @0x40003000=0xAAAA; bl 0xc20c(r0=3, r1=0x40010818 [GPIO reg]). bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x05B98, 0xC20D)
    assert cap.get('r1') == 0x40010818, f'{cap}'


# --- E2-batch14: bulk erase + u16-обмен + retry/toggle (bl-intercept) ---
@t(0x07EE8, 'E2-b14: 0x07ee8 — bulk erase init. Инициирует stack-буфер + bl 0x11d6(ptr, r1=0x800 [сектор 0x800B]). bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x07EE8, 0x11D7)
    assert cap.get('r1') == 0x800, f'{cap}'


@t(0x07FDC, 'E2-b14: 0x07fdc — bulk erase body. Тело цикла: bl 0x11d6(ptr, r1=0x800). bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x07FDC, 0x11D7)
    assert cap.get('r1') == 0x800, f'{cap}'


@t(0x057F8, 'E2-b14: 0x057f8 — u16@0xCB3 -> байты @0xCB3/0xCB5 + bl 0x13bb8(r0=1). bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x057F8, 0x13BB9)
    assert cap.get('r0') == 1, f'{cap}'


@t(0x05818, 'E2-b14: 0x05818 — байты @0xCB3/0xCB5 -> u16@0xCB3 + bl 0x13bb8(r0=0). bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x05818, 0x13BB9)
    assert 'r0' in cap, f'{cap}'


@t(0x0236C, 'E2-b14: 0x0236c — retry-счётчик I2C. Успех -> bl 0x21dc; @0xA76=0, @0xA75++. bl-intercept (достигает хелпера).')
def _(run, rng):
    cap, _emu = _intercept(0x0236C, 0x21DD)
    assert 'r0' in cap, f'{cap}'


@t(0x09B08, 'E2-b14: 0x09b08 — toggle bit3 byte@0xA71 (до 3 попыток, гейт 0x2a5c). bl-intercept (достигает хелпера).')
def _(run, rng):
    cap, _emu = _intercept(0x09B08, 0x2A5D)
    assert 'r0' in cap, f'{cap}'


# --- E2-batch15: I2C2 wr/read + event + struct access (bl-intercept) ---
@t(0x0214C, 'E2-b15: 0x0214c — I2C2 write op=8. 0x0214c() -> bl 0x8f7c(r0=0x40005800 [I2C2 base], reg, buf). bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x0214C, 0x8F7D)
    assert cap.get('r0') == 0x40005800, f'{cap}'


@t(0x02730, 'E2-b15: 0x02730 — I2C2 read-путь. 0x02730() -> bl 0x9048(r0=0x40005800 [I2C2 base]). bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x02730, 0x9049)
    assert cap.get('r0') == 0x40005800, f'{cap}'


@t(0x03150, 'E2-b15: 0x03150 — event {u32=0,u16=0x7F,u32=0x136}. 0x03150() -> bl 0xcd0c (event dispatch, r0=stack-буфер). bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x03150, 0xCD0D)
    assert 'r0' in cap, f'{cap}'


@t(0x03970, 'E2-b15: 0x03970 — доступ к структуре @0x98. 0x03970() -> bl 0x8a90 (r0=ptr). bl-intercept.')
def _(run, rng):
    cap, _emu = _intercept(0x03970, 0x8A91)
    assert 'r0' in cap, f'{cap}'


# --- E2-batch16: transaction-return (условный выход по результату транзакции) ---
@t(0x08380, 'E2-b16: 0x08380 — transaction 0x833c: если r0 -> return 0 (условный выход). bl-intercept (достигает 0x833c).')
def _(run, rng):
    cap, _emu = _intercept(0x08380, 0x833D)
    assert 'r0' in cap, f'{cap}'


@t(0x084A0, 'E2-b16: 0x084a0 — transaction 0x833c: если r0==0 -> return. bl-intercept (достигает 0x833c).')
def _(run, rng):
    cap, _emu = _intercept(0x084A0, 0x833D)
    assert 'r0' in cap, f'{cap}'


@t(0x0851C, 'E2-b16: 0x0851c — transaction 0x833c: если r0!=0 -> return pc. bl-intercept (достигает 0x833c).')
def _(run, rng):
    cap, _emu = _intercept(0x0851C, 0x833D)
    assert 'r0' in cap, f'{cap}'


# --- E2-batch17: one-shot флаг 0x03a6c (stateful, вериф fire/no-fire) ---
@t(0x03A6C, 'E2-b17: 0x03a6c — one-shot флаг byte@0x142. Если ==1 -> обнуляет его + bl 0xdd81; иначе return. Вериф: flag=1 достигает 0xdd81, flag=0 нет.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    cap_fired, _emu = _intercept(0x03A6C, 0xDD81,
                                 extra_ram=[(_R + 0x142, b'\x01')])
    assert 'r0' in cap_fired, f'flag=1: не достиг 0xdd81: {cap_fired}'
    cap_idle, _emu2 = _intercept(0x03A6C, 0xDD81,
                                 extra_ram=[(_R + 0x142, b'\x00')])
    assert 'r0' not in cap_idle, f'flag=0: достиг 0xdd81 (ошибка): {cap_idle}'


# --- E2-batch18: flag-хендлер 0x09678 (stateful, полный разбор pool) ---
@t(0x09678, 'E2-b18: 0x09678 — flag-хендлер. BIT1=byte@0xB65 (bit1), COUNTER=byte@0xB73, A0=byte@0xB64. Если bit1 set и (COUNTER++)>=3 -> COUNTER=0, clear BIT1 bit1, A0=(A0&0x0f)|0xa0; затем если (A0>>4)==0xa -> bl (capstone: 0x173cd, эмулятор попадает в 0x173cc). Вериф: fire (BIT1=2,CNT=2) достигает; no-fire (BIT1=2,CNT=0) нет.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    cap_fire, _emu = _intercept(0x09678, 0x173CC,
                                extra_ram=[(_R + 0xB65, b'\x02'),
                                           (_R + 0xB73, b'\x02')])
    assert 'r0' in cap_fire, f'fire: не достиг 0x173cc: {cap_fire}'
    cap_nofire, _emu2 = _intercept(0x09678, 0x173CC,
                                   extra_ram=[(_R + 0xB65, b'\x02')])
    assert 'r0' not in cap_nofire, f'no-fire: достиг 0x173cc (ошибка): {cap_nofire}'


# --- E2-batch19: счётчики с насыщением (stateful, inc + saturation) ---
@t(0x12C24, 'E2-b19: 0x12c24 — счётчик с насыщением. GATE=bit0(byte@0xB76), COUNTER=u16@0xB7A. Если gate set: COUNTER++; если COUNTER>0xC8 -> clear gate + COUNTER=0. Вериф inc (cnt 5->6) и sat (cnt 0xC8->0, gate clr).')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    _r0, emu = _fresh_call(0x12C24, extra_ram=[(_R + 0xB76, b'\x01'),
                                                (_R + 0xB7A, _st.pack('<H', 5))])
    cnt = _st.unpack_from('<H', bytes(emu.uc.mem_read(_R + 0xB7A, 2)))[0]
    assert cnt == 6, f'inc: got {cnt} want 6'
    _r0, emu2 = _fresh_call(0x12C24, extra_ram=[(_R + 0xB76, b'\x01'),
                                                 (_R + 0xB7A, _st.pack('<H', 0xC8))])
    gate = emu2.uc.mem_read(_R + 0xB76, 1)[0]
    cnt2 = _st.unpack_from('<H', bytes(emu2.uc.mem_read(_R + 0xB7A, 2)))[0]
    assert cnt2 == 0 and gate == 0, f'sat: cnt={cnt2} gate={gate}'


@t(0x12E64, 'E2-b19: 0x12e64 — счётчик с насыщением #2. GATE=bit2(byte@0xB76), COUNTER=u16@0xB7C. Аналогично 0x12c24 (кап 0xC8). Вериф inc (cnt 5->6) и sat (cnt 0xC8->0, gate clr).')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    _r0, emu = _fresh_call(0x12E64, extra_ram=[(_R + 0xB76, b'\x04'),
                                                (_R + 0xB7C, _st.pack('<H', 5))])
    cnt = _st.unpack_from('<H', bytes(emu.uc.mem_read(_R + 0xB7C, 2)))[0]
    assert cnt == 6, f'inc: got {cnt} want 6'
    _r0, emu2 = _fresh_call(0x12E64, extra_ram=[(_R + 0xB76, b'\x04'),
                                                 (_R + 0xB7C, _st.pack('<H', 0xC8))])
    gate = emu2.uc.mem_read(_R + 0xB76, 1)[0]
    cnt2 = _st.unpack_from('<H', bytes(emu2.uc.mem_read(_R + 0xB7C, 2)))[0]
    assert cnt2 == 0 and gate == 0, f'sat: cnt={cnt2} gate={gate}'


# --- E2-batch20: mismatch-счётчик 0x0c02c (stateful) ---
@t(0x0C02C, 'E2-b20: 0x0c02c — mismatch-счётчик. Читает bit0/bit1(0xF71) vs byte(0xA65)/byte(0xA66). Mismatch -> COUNTER(u16@0xA68)++; если >=0x32 -> toggle bit3(0xF73) + COUNTER=0x32. Match (оба равны) -> COUNTER=0 + clear bit3(0xF73). Вериф mismatch-inc / match-reset / saturation.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    def rd(emu, off, n):
        return bytes(emu.uc.mem_read(_R + off, n))
    _r0, emu = _fresh_call(0x0C02C, extra_ram=[(_R + 0xF71, b'\x01'),
                                                (_R + 0xA65, b'\x00')])
    cnt = _st.unpack_from('<H', rd(emu, 0xA68, 2))[0]
    assert cnt == 1, f'mismatch-inc: got {cnt} want 1'
    _r0, emu2 = _fresh_call(0x0C02C, extra_ram=[(_R + 0xA68, _st.pack('<H', 5))])
    cnt2 = _st.unpack_from('<H', rd(emu2, 0xA68, 2))[0]
    assert cnt2 == 0, f'match-reset: got {cnt2} want 0'
    _r0, emu3 = _fresh_call(0x0C02C, extra_ram=[(_R + 0xF71, b'\x01'),
                                                 (_R + 0xA65, b'\x00'),
                                                 (_R + 0xA68, _st.pack('<H', 0x31)),
                                                 (_R + 0xF73, b'\x00')])
    cnt3 = _st.unpack_from('<H', rd(emu3, 0xA68, 2))[0]
    flag3 = emu3.uc.mem_read(_R + 0xF73, 1)[0]
    assert cnt3 == 0x32 and (flag3 & 8), f'sat: cnt={cnt3:#x} flag={flag3:#x}'


# --- E2-batch21: pure-logic (checksum / критсекция / u32 из двух u16) ---
@t(0x048D8, 'E2-b21: 0x048d8 — контрольная сумма: r0 = (~sum(buf[0..len])) & 0xFF. Вериф 3 буфера.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    for buf in (b'\x01\x02\x03', b'\xff\xff\xff', bytes(4)):
        r0, _e = _fresh_call(0x048D8, args=(_R + 0x100, len(buf)),
                             extra_ram=[(_R + 0x100, buf)])
        exp = (~sum(buf)) & 0xFF
        assert (r0 & 0xFF) == exp, f'buf={buf!r}: got {r0&0xff} want {exp}'


@t(0x02D1C, 'E2-b21: 0x02d1c — вход в критсекцию: COUNTER=u16@0xB5C; если ==0 -> cpsid i; затем COUNTER++. Вериф 0->1 и 5->6.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    for init in (0, 5):
        _r0, emu = _fresh_call(0x02D1C, extra_ram=[(_R + 0xB5C, _st.pack('<H', init))])
        cnt = _st.unpack_from('<H', bytes(emu.uc.mem_read(_R + 0xB5C, 2)))[0]
        assert cnt == init + 1, f'init={init}: got {cnt} want {init+1}'


@t(0x098AE, 'E2-b21: 0x098ae — u32 из двух u16: r0 = u16[ptr+0x14] | ((u16[ptr+0x18]&0xFF)<<16) (старший байт B сброшен). Вериф 3 пары.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    for A, B in ((0x1234, 0xABCD), (0x5678, 0x00FF), (0xFFFF, 0x1234)):
        r0, _e = _fresh_call(0x098AE, args=(_R + 0x200,),
                             extra_ram=[(_R + 0x214, _st.pack('<H', A)),
                                        (_R + 0x218, _st.pack('<H', B))])
        exp = (A | ((B & 0xFF) << 16)) & 0xFFFFFFFF
        assert r0 == exp, f'A={A:#x} B={B:#x}: got {r0:#x} want {exp:#x}'


# --- E2-batch22: set/clear-биты + signed-div-prep + sign-extend ---
def _setclr(off, bit, desc):
    @t(off, desc)
    def _(run, rng):
        from emulator.mcu_emu import RAM as _R
        import struct as _st
        for mode, init in ((1, 0), (0, 0xFFFF)):
            _r0, emu = _fresh_call(off, args=(_R + 0x300, mode),
                                   extra_ram=[(_R + 0x300, _st.pack('<H', init))])
            v = _st.unpack_from('<H', bytes(emu.uc.mem_read(_R + 0x300, 2)))[0]
            exp = (init | bit) if mode else (init & ~bit) & 0xFFFF
            assert v == exp, f'mode={mode} init={init:#x}: got {v:#x} want {exp:#x}'
    return _


_setclr(0x097CA, 0x400, 'E2-b22: 0x097ca — set/clear bit0x400 в *(u16@r0): mode!=0 -> |=, else &=~. Вериф set+clear.')
_setclr(0x0982C, 0x1, 'E2-b22: 0x0982c — set/clear bit0 в *(u16@r0). Вериф set+clear.')
_setclr(0x106A0, 0x40, 'E2-b22: 0x106a0 — set/clear bit0x40 в *(u16@r0). Вериф set+clear.')


@t(0x16288, 'E2-b22: 0x16288 — signed-подготовка к делению. При r1==0: возвращает 0x7FFFFFFF (если r2>=0) или 0x80000000 (если r2<0). Вериф оба знака.')
def _(run, rng):
    for r2 in (5, -5):
        r0, _e = _fresh_call(0x16288, args=(r2 & 0xFFFFFFFF, 0))
        exp = 0x7FFFFFFF if r2 >= 0 else 0x80000000
        assert r0 == exp, f'r2={r2}: got {r0:#x} want {exp:#x}'


@t(0x08F58, 'E2-b22: 0x08f58 — sign-extend: читает s8@0xFC8 -> i16 -> u16@0x135E, возвращает. Вериф -1/127/-128.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    for sb, exp in ((0xFF, 0xFFFF), (0x7F, 0x7F), (0x80, 0xFF80)):
        r0, emu = _fresh_call(0x08F58, extra_ram=[(_R + 0xFC8, bytes([sb]))])
        assert (r0 & 0xFFFF) == exp, f'sb={sb:#x}: got {r0&0xffff:#x} want {exp:#x}'
        stored = _st.unpack_from('<H', bytes(emu.uc.mem_read(_R + 0x135E, 2)))[0]
        assert stored == exp, f'stored={stored:#x} want {exp:#x}'


# --- E2-batch23: set/clear-биты (прод.) + signed-prep варианты + memmove ---
_setclr(0x09844, 0x100, 'E2-b23: 0x09844 — set/clear bit0x100 в *(u16@r0). Вериф set+clear.')
_setclr(0x0985C, 0x200, 'E2-b23: 0x0985c — set/clear bit0x200 в *(u16@r0). Вериф set+clear.')


@t(0x162CE, 'E2-b23: 0x162ce — signed-подготовка к делению (вариант). r1==0 -> 0x7FFFFFFF (r2>=0) / 0x80000000 (r2<0).')
def _(run, rng):
    for r2 in (5, -5):
        r0, _e = _fresh_call(0x162CE, args=(r2 & 0xFFFFFFFF, 0))
        exp = 0x7FFFFFFF if r2 >= 0 else 0x80000000
        assert r0 == exp, f'r2={r2}: got {r0:#x} want {exp:#x}'


@t(0x16328, 'E2-b23: 0x16328 — signed-подготовка к делению (вариант 2). r1==0 -> 0x7FFFFFFF / 0x80000000.')
def _(run, rng):
    for r2 in (5, -5):
        r0, _e = _fresh_call(0x16328, args=(r2 & 0xFFFFFFFF, 0))
        exp = 0x7FFFFFFF if r2 >= 0 else 0x80000000
        assert r0 == exp, f'r2={r2}: got {r0:#x} want {exp:#x}'


@t(0x07FB8, 'E2-b23: 0x07fb8 — memmove: копирует len байт из src(r0) в dst(r1), возвращает 1. Вериф 5-байтовый буфер.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    src = bytes([0x11, 0x22, 0x33, 0x44, 0x55])
    r0, emu = _fresh_call(0x07FB8, args=(_R + 0x100, _R + 0x200, len(src)),
                          extra_ram=[(_R + 0x100, src)])
    dst = bytes(emu.uc.mem_read(_R + 0x200, len(src)))
    assert r0 == 1 and dst == src, f'r0={r0} dst={dst.hex()}'


# --- E2-batch24: обнуление блока ---
@t(0x04A04, 'E2-b24: 0x04a04 — обнуление блока: byte@0x129 + u32@0x12C/0x130/0x134/0x138 (блок 0x129..0x13B). Вериф: pre-set -> все 0.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    pre = [(_R + 0x129, b'\xAA'), (_R + 0x12C, b'\x11\x22\x33\x44'),
           (_R + 0x130, b'\x55\x66\x77\x88'), (_R + 0x134, b'\x99\xAA\xBB\xCC'),
           (_R + 0x138, b'\xDD\xEE\xFF\x00')]
    _r0, emu = _fresh_call(0x04A04, extra_ram=pre)
    block = bytes(emu.uc.mem_read(_R + 0x129, 0x13))
    assert block == bytes(0x13), f'block not zeroed: {block.hex()}'


# --- E2-batch25: event-очередь push (stateful) ---
@t(0x04BC0, 'E2-b25: 0x04bc0 — event-очередь push: если idx<6 -> u32@(0x164C+idx*16+8)=ptr, +0xC=val (через critsec). Вериф idx=2 (write) и idx=7 (skip).')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    r0, emu = _fresh_call(0x04BC0, args=(2, 0x1234, 0xABCD))
    uc = emu.uc
    base = _R + 0x164C + 2 * 16
    ptr = _st.unpack_from('<I', bytes(uc.mem_read(base + 8, 4)))[0]
    val = _st.unpack_from('<I', bytes(uc.mem_read(base + 0xC, 4)))[0]
    assert ptr == 0x1234 and val == 0xABCD, f'idx=2: ptr={ptr:#x} val={val:#x}'
    r0, emu2 = _fresh_call(0x04BC0, args=(7, 0x1234, 0xABCD))
    base7 = _R + 0x164C + 7 * 16
    p7 = _st.unpack_from('<I', bytes(emu2.uc.mem_read(base7 + 8, 4)))[0]
    assert p7 == 0, f'idx=7: expected skip, ptr={p7:#x}'


# --- E2-batch26: инициализация event-кольца ---
@t(0x04BE8, 'E2-b26: 0x04be8 — init event-кольца. u32@0xB4C=0; для i=0..5: byte@(0x164C+i*16)=0, u32@(0x164C+i*16+4)=0xFFFFFFFF, byte@(0x164C+i*16+1)=0. Вериф: pre-set -> все очищены.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    pre = [(_R + 0xB4C, b'\x11\x22\x33\x44'),
           (_R + 0x164C + 2 * 16, b'\xAA\xBB\xCC\xDD\xEE\xFF\x00\x00')]
    r0, emu = _fresh_call(0x04BE8, extra_ram=pre)
    uc = emu.uc
    idx = _st.unpack_from('<I', bytes(uc.mem_read(_R + 0xB4C, 4)))[0]
    assert idx == 0, f'index: got {idx:#x} want 0'
    for i in range(6):
        base = _R + 0x164C + i * 16
        f0 = uc.mem_read(base + 0, 1)[0]
        f1 = uc.mem_read(base + 1, 1)[0]
        sent = _st.unpack_from('<I', bytes(uc.mem_read(base + 4, 4)))[0]
        assert f0 == 0 and f1 == 0 and sent == 0xFFFFFFFF, \
            f'slot {i}: f0={f0:#x} f1={f1:#x} sent={sent:#x}'


# --- E2-batch27: merge struct-полей (чистые arg-указатели) ---
@t(0x04F70, 'E2-b27: 0x04f70 — merge: dst[0]=(dst[0]&~0x7FF0)|OR(src[+8,+10..+28]); dst[+4]=src[+0xC]; dst[+8]=src[0]. Вериф OR-агрегация + copy (2 init).')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    dst = _R + 0x100; src = _R + 0x200
    vals = {0x8: 1, 0x10: 2, 0x14: 4, 0x18: 8, 0x1c: 0x10, 0x20: 0x20, 0x24: 0x40, 0x28: 0x80}
    srcbuf = bytearray(0x30)
    for o, v in vals.items():
        _st.pack_into('<I', srcbuf, o, v)
    _st.pack_into('<I', srcbuf, 0x0C, 0xDEADBEEF)
    _st.pack_into('<I', srcbuf, 0x0, 0x12345678)
    for init in (0x7FF0, 0x88FF):
        dstbuf = bytearray(0x10); _st.pack_into('<I', dstbuf, 0, init)
        r0, emu = _fresh_call(0x04F70, args=(dst, src), extra_ram=[(dst, bytes(dstbuf)), (src, bytes(srcbuf))])
        uc = emu.uc
        d0 = _st.unpack_from('<I', bytes(uc.mem_read(dst + 0, 4)))[0]
        d4 = _st.unpack_from('<I', bytes(uc.mem_read(dst + 4, 4)))[0]
        d8 = _st.unpack_from('<I', bytes(uc.mem_read(dst + 8, 4)))[0]
        exp_or = sum(vals.values())
        assert d0 == (init & ~0x7FF0) | exp_or, f'init={init:#x}: dst[0]={d0:#x}'
        assert d4 == 0xDEADBEEF, f'dst[+4]={d4:#x}'
        assert d8 == 0x12345678, f'dst[+8]={d8:#x}'


# --- E2-batch28: u16-merge struct-полей (чистые arg-указатели) ---
@t(0x10734, 'E2-b28: 0x10734 — u16-merge: dst[0]=(dst[0]&0x3040)|OR(src[+0..+0xe]); dst[+0x1C]&=0xF7FF; dst[+0x10]=src[+0x10]. Вериф (2 init).')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    dst = _R + 0x100; src = _R + 0x200
    srcbuf = bytearray(0x20)
    for i in range(8):
        _st.pack_into('<H', srcbuf, i * 2, 1 << i)
    _st.pack_into('<H', srcbuf, 0x10, 0xBEEF)
    exp_or = 0xFF
    for init0, init1c in [(0x3040, 0xFFFF), (0xFFFF, 0x0200)]:
        dstbuf = bytearray(0x20)
        _st.pack_into('<H', dstbuf, 0, init0)
        _st.pack_into('<H', dstbuf, 0x1C, init1c)
        r0, emu = _fresh_call(0x10734, args=(dst, src), extra_ram=[(dst, bytes(dstbuf)), (src, bytes(srcbuf))])
        uc = emu.uc
        d0 = _st.unpack_from('<H', bytes(uc.mem_read(dst + 0, 2)))[0]
        d1c = _st.unpack_from('<H', bytes(uc.mem_read(dst + 0x1C, 2)))[0]
        d10 = _st.unpack_from('<H', bytes(uc.mem_read(dst + 0x10, 2)))[0]
        assert d0 == (init0 & 0x3040) | exp_or, f'init0={init0:#x}: dst[0]={d0:#x}'
        assert d1c == init1c & 0xF7FF, f'dst[+0x1C]={d1c:#x} want {init1c & 0xF7FF:#x}'
        assert d10 == 0xBEEF, f'dst[+0x10]={d10:#x}'


# --- E2-batch29: memcpy (word-fast-path + byte-tail) ---
@t(0x19A68, 'E2-b29: 0x19a68 — memcpy(dst,src,len): word-copy если оба 4-aligned, else byte; tail по байтам. Вериф len=0..64 (aligned+unaligned).')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    for ln in (0, 1, 3, 4, 5, 7, 16, 17, 64):
        src = _R + 0x100; dst = _R + 0x300
        buf = bytes((i * 7 + 3) & 0xFF for i in range(ln))
        dstpre = bytes([0xAA] * (ln + 4))
        r0, emu = _fresh_call(0x19A68, args=(dst, src, ln), extra_ram=[(src, buf), (dst, dstpre)])
        got = bytes(emu.uc.mem_read(dst, ln)) if ln else b''
        assert got == buf, f'len={ln}: got={got.hex()} want={buf.hex()}'


# --- E2-batch30: bit-field containment check ---
@t(0x09874, 'E2-b30: 0x09874 — bit-field check: top-nibble(r1)==0 -> поле u32@(ptr+0x18), mask=r1>>16; else поле u32@(ptr+0x14), mask=r1&0xFFFFFF. Вериф: 1 если (*field & mask)!=0 (7 кейсов).')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    ptr = _R + 0x200
    def chk(r1, f14, f18):
        pre = [(ptr + 0x14, _st.pack('<I', f14)), (ptr + 0x18, _st.pack('<I', f18))]
        r0, _e = _fresh_call(0x09874, args=(ptr, r1), extra_ram=pre)
        return r0 & 1
    cases = [
        (0x00010000, 0, 0x01, 1), (0x00010000, 0, 0x00, 0),
        (0x00FF0000, 0, 0x80, 1), (0xF00000FF, 0x01, 0, 1),
        (0xF00000FF, 0x00, 0, 0), (0x100000F0, 0xF0, 0, 1),
        (0x100000F0, 0x0F, 0, 0),
    ]
    for r1, f14, f18, exp in cases:
        got = chk(r1, f14, f18)
        assert got == exp, f'r1={r1:#x} f14={f14:#x} f18={f18:#x}: got {got} want {exp}'


# --- E2-batch31: two-part bit check ---
@t(0x130F2, 'E2-b31: 0x130f2 — two-part bit check. group=(code>>5)&7: 1->+0xC, 2->+0x10, else->+0x14; maskA=1<<(code&0x1F). PartB: ptr[0], maskB=1<<(code>>8). Вериф: 1 если оба бита set (6 кейсов).')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    ptr = _R + 0x200
    def chk(code, f0, fc, f10, f14):
        pre = [(ptr + 0, _st.pack('<H', f0)), (ptr + 0xC, _st.pack('<H', fc)),
               (ptr + 0x10, _st.pack('<H', f10)), (ptr + 0x14, _st.pack('<H', f14))]
        r0, _e = _fresh_call(0x130F2, args=(ptr, code), extra_ram=pre)
        return r0 & 1
    cases = [
        (0x124, 0x02, 0x10, 0, 0, 1), (0x124, 0x02, 0x00, 0, 0, 0),
        (0x124, 0x00, 0x10, 0, 0, 0), (0x144, 0x02, 0, 0x10, 0, 1),
        (0x144, 0x02, 0, 0x00, 0, 0), (0x104, 0x02, 0, 0, 0x10, 1),
    ]
    for code, f0, fc, f10, f14, exp in cases:
        got = chk(code, f0, fc, f10, f14)
        assert got == exp, f'code={code:#x} f0={f0:#x} fc={fc:#x} f10={f10:#x} f14={f14:#x}: got {got} want {exp}'


# --- E2-batch32: XOR 16-байт блоков ---
@t(0x1A5FA, 'E2-b32: 0x1a5fa — XOR-блок: dst[r3*4+i] ^= src[(4*idx+r3)*4+i], r3,i=0..3 (16 байт). Вериф idx=0,1,2.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    dst = _R + 0x100; src = _R + 0x300
    srcbuf = bytes((i * 5 + 1) & 0xFF for i in range(64))
    for idx in (0, 1, 2):
        dstpre = bytes([0xFF] * 20)
        r0, emu = _fresh_call(0x1A5FA, args=(idx, dst, src), extra_ram=[(dst, dstpre), (src, srcbuf)])
        got = bytes(emu.uc.mem_read(dst, 16))
        exp = bytearray(16)
        for r3 in range(4):
            for i in range(4):
                exp[r3 * 4 + i] = (0xFF ^ srcbuf[(4 * idx + r3) * 4 + i]) & 0xFF
        assert got == bytes(exp), f'idx={idx}: got={got.hex()} want={bytes(exp).hex()}'


# --- E2-batch33: exponent-ramp (2^(t-0x7F)) ---
@t(0x1A010, 'E2-b33: 0x1a010 — exponent-ramp: для r0=(t<<23): t<0x7F -> 0; else 1<<(t-0x7F) (линейный рост 2^0..2^23). Вериф sweep t=0x78..0x96.')
def _(run, rng):
    for t in range(0x78, 0x97):
        r0 = t << 23
        r, _e = _fresh_call(0x1A010, args=(r0,))
        exp = 0 if t < 0x7F else (1 << (t - 0x7F))
        assert r == exp, f't={t:#x}: got {r:#x} want {exp:#x}'


# --- E2-batch34: u16 bit-check + 24-bit field all-set check ---
@t(0x10718, 'E2-b34: 0x10718 — u16 bit-check: 1 если (u16@(ptr+8) & mask)!=0. Вериф 3 кейса.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    ptr = _R + 0x200
    def a(mask, val):
        r0, _e = _fresh_call(0x10718, args=(ptr, mask), extra_ram=[(ptr + 8, _st.pack('<H', val))])
        return r0 & 1
    for mask, val, exp in [(0x0001, 0x0001, 1), (0x0001, 0x0000, 0), (0x0100, 0xFF00, 1)]:
        got = a(mask, val)
        assert got == exp, f'mask={mask:#x} val={val:#x}: got {got} want {exp}'

@t(0x09794, 'E2-b34: 0x09794 — 24-битное поле (u16@+0x14 | u16@+0x18<<16)&0xFFFFFF; 1 если (field&mask)==mask. Вериф 4 кейса.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    ptr = _R + 0x200
    def b(mask, f14, f18):
        r0, _e = _fresh_call(0x09794, args=(ptr, mask),
                             extra_ram=[(ptr + 0x14, _st.pack('<H', f14)), (ptr + 0x18, _st.pack('<H', f18))])
        return r0 & 1
    for mask, f14, f18, exp in [(0x00FF, 0x00FF, 0, 1), (0x0100, 0x00FF, 0, 0),
                                 (0x00FF0000, 0xFFFF, 0xFF, 1), (0x00FF00FF, 0xFFFF, 0xFF, 1)]:
        got = b(mask, f14, f18)
        assert got == exp, f'mask={mask:#x} f14={f14:#x} f18={f18:#x}: got {got} want {exp}'


# --- E2-batch35: periph const-write / bit-set via pool pointers ---
@t(0x05CC0, 'E2-b35: 0x05cc0 — пишет константу 0xAAAA в periph[0x40003000] (pool-указатель). Вериф значение после вызова.')
def _(run, rng):
    import struct as _st
    r0, emu = _fresh_call(0x05CC0)
    got = _st.unpack('<I', bytes(emu.uc.mem_read(0x40003000, 4)))[0]
    assert got == 0xAAAA, f'periph[0x40003000]={got:#x} want 0xaaaa'

@t(0x1A5C4, 'E2-b35: 0x1a5c4 — ставит бит3 (0x8) в u32@periph[0x40012418] (pool-base 0x40012400). Вериф pre=0/0xFF.')
def _(run, rng):
    import struct as _st
    for pre, exp in [(0, 0x8), (0xFF, 0xFF)]:
        r0, emu = _fresh_call(0x1A5C4, extra_mem=[(0x40012418, _st.pack('<I', pre))])
        got = _st.unpack('<I', bytes(emu.uc.mem_read(0x40012418, 4)))[0]
        assert got == exp, f'pre={pre:#x}: got {got:#x} want {exp:#x}'

@t(0x1A5D4, 'E2-b35: 0x1a5d4 — ставит бит5 (0x20) в u32@periph[0x40012418]. Вериф pre=0/0x0F.')
def _(run, rng):
    import struct as _st
    for pre, exp in [(0, 0x20), (0x0F, 0x2F)]:
        r0, emu = _fresh_call(0x1A5D4, extra_mem=[(0x40012418, _st.pack('<I', pre))])
        got = _st.unpack('<I', bytes(emu.uc.mem_read(0x40012418, 4)))[0]
        assert got == exp, f'pre={pre:#x}: got {got:#x} want {exp:#x}'


# --- E2-batch36: 0x0d39d delegate family (gated channel-service) ---
# Контракт (вериф bl-intercept): u32@(RAM+0x8C) — status-слово; если bit `channel` set,
# функция вызывает 0x0d39d(channel); если 0x0d39d вернёт 1 -> сбросить bit `channel`
# в другом status-u32 (по pool). gate-бит == channel. Вериф: bl достигнут с r0==channel.
_OD39D_FAM = {0x0D6E4: 0xE, 0x0D734: 0xD, 0x0D75C: 0x10,
              0x0D784: 0x11, 0x0D7D4: 0xF, 0x0D850: 0x12}


def _mk_od39d(addr, ch):
    def _test(run, rng):
        from emulator.mcu_emu import RAM as _R
        import struct as _st
        cap, _emu = _intercept(addr, 0x0D39D,
                               extra_ram=[(_R + 0x8C, _st.pack('<I', 1 << ch))])
        assert cap.get('r0') == ch, \
            f'0x{addr:05x}: r0={cap.get("r0"):#x} want 0x{ch:x}'
    return _test


for _addr, _ch in sorted(_OD39D_FAM.items()):
    t(_addr, f'E2-b36: 0x{_addr:05x} -> 0x0d39d(channel=0x{_ch:x}) [gate=bit {_ch} of u32@RAM+0x8C; bl-intercept]')(_mk_od39d(_addr, _ch))


# --- E2-batch37: 0x0d46d delegate family (гated channel-service, брат 0x0d39d) ---
_OD46D_FAM = {0x0D70C: 0x9, 0x0D7AC: 0xB, 0x0D7FC: 0xC, 0x0D824: 0xA}


def _mk_od46d(addr, ch):
    def _test(run, rng):
        from emulator.mcu_emu import RAM as _R
        import struct as _st
        cap, _emu = _intercept(addr, 0x0D46D,
                               extra_ram=[(_R + 0x8C, _st.pack('<I', 1 << ch))])
        assert cap.get('r0') == ch, \
            f'0x{addr:05x}: r0={cap.get("r0"):#x} want 0x{ch:x}'
    return _test


for _addr, _ch in sorted(_OD46D_FAM.items()):
    t(_addr, f'E2-b37: 0x{_addr:05x} -> 0x0d46d(channel=0x{_ch:x}) [gate=bit {_ch} of u32@RAM+0x8C; bl-intercept]')(_mk_od46d(_addr, _ch))


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
