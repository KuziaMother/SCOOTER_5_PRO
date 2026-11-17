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
