# -*- coding: utf-8 -*-
"""E2-b66: u64-Q20 фикс-арифметика (0x19c58/0x1346 — twins), float-нормализация
0x19bdc (евклидов-цикл → IEEE-биты), нормализованное мантиссенное сложение 0x19ab0,
TLV+CRC-16 0x38ec (таблица @0x19784), one-shot флаги u32@0x8C (8 функций,
каталог 0xd71c..0xd7e0 — реальные старты 0xd70c..0xd824)."""
# ruff: noqa: F405  (имена из star-import от fv_core)
from fv_core import *  # noqa: F401,F403
from fv_core import _fresh_call, _intercept  # noqa: F401

import struct

# --- u64 Q20 "моторная" арифметика: args (a0,a1,a2,a3) = (x_lo,x_hi,y_lo,y_hi) ---
_Q20_CASES = [
    ((0, 0, 0, 0), 0x0),
    ((1, 0, 1, 0), 0x1),
    ((2, 0, 1, 0), 0x2),
    ((1, 0, 3, 0), 0x2),
    ((0x1000000, 0, 0x800000, 0), 0xC00000),
    ((0x800000, 0, 0x1000000, 0), 0xC00000),
    ((0, 0xFFFFFFFF, 1, 0), 0x0),
    ((1, 0, 0xFFFFFFFF, 0xFFFFFFFF), 0xFFFFFFFF),
    ((0x1000000, 1, 0x1000000, 0), 0x81000000),
    ((0x12345678, 0x9ABC, 0, 0), 0x12345678),
]


def _run_q20(off):
    """The helper function (_run_q20).
    Вспомогательная функция (_run_q20).
    """
    for args, exp in _Q20_CASES:
        r1, _e1 = _fresh_call(off, args, max_insn=200000)
        r2, _e2 = _fresh_call(off, args, max_insn=200000)
        assert r1 == r2, f'{off:#x} {args}: NDET {r1:#x}/{r2:#x}'
        assert r1 == exp, f'{off:#x} {args}: ret={r1:#x} ждём {exp:#x}'


@t(0x19C58, 'E2-b66: 0x19c58(x,y) — u64 Q20 фикс-арифметика (моторная цепь, 12-bit dfrac): '
            'sign=sb(a1)^sb(a3), abs, u64-swap, zero→first-pair; mid-путь (|dfrac diff|<0x40) — '
            'сложение мантисс 21-bit с нормализацией/знаком; const-calc 10 кейсов (детерм.)')
def _(run, rng):
    """Emulator test @ 0x19c58: E2-b66: 0x19c58(x,y) — u64 Q20 фикс-арифметика (моторная цепь, 12-bit dfrac): sign=sb(a1)^sb(a3), abs, u64-swap, zero→first-pair; mid-путь (|dfrac diff|<0x40) — сложение мантисс 21-bit с нормализацией/знаком; const-calc 10 кейсов (детерм.).
    Тест эмулятора @ 0x19c58: E2-b66: 0x19c58(x,y) — u64 Q20 фикс-арифметика (моторная цепь, 12-bit dfrac): sign=sb(a1)^sb(a3), abs, u64-swap, zero→first-pair; mid-путь (|dfrac diff|<0x40) — сложение мантисс 21-bit с нормализацией/знаком; const-calc 10 кейсов (детерм.).
    """
    _run_q20(0x19C58)


@t(0x1346, 'E2-b66: 0x1346(x,y) — twin 0x19c58 с 11-bit dfrac (ubfx #0,#0xb вместо lsls/lsrs): '
            'та же семантика на 10 кейсах (разница 11/12 бит проявляется только при dfrac bit30). '
            'const-calc (детерм.)')
def _(run, rng):
    """Emulator test @ 0x1346: E2-b66: 0x1346(x,y) — twin 0x19c58 с 11-bit dfrac (ubfx #0,#0xb вместо lsls/lsrs): та же семантика на 10 кейсах (разница 11/12 бит проявляется только при dfrac bit30). const-calc (детерм.).
    Тест эмулятора @ 0x1346: E2-b66: 0x1346(x,y) — twin 0x19c58 с 11-bit dfrac (ubfx #0,#0xb вместо lsls/lsrs): та же семантика на 10 кейсах (разница 11/12 бит проявляется только при dfrac bit30). const-calc (детерм.).
    """
    _run_q20(0x1346)


# --- 0x19bdc: signed евклидов-цикл → IEEE-float биты ---
_19BDC_CASES = [
    ((1, 0), 0x0),
    ((5, 0), 0x0),
    ((0x12345678, 0), 0x0),
    ((0xFFFFFFFF, 0), 0x0),
    ((0, 1), 0x0),
    ((0xF4240, 1), 0x3F8F423F),
    ((0x80000000, 0), 0x0),
    ((0xFFFFFFFF, 0xFFFFFFFF), 0x3F800000),
    ((7, 3), 0x3F800004),
    ((3, 7), 0x3F7FFFF8),
]


@t(0x19BDC, 'E2-b66: 0x19bdc(a0,a1) — signed евклидов-подобный цикл (abs-u64, биту-по-биту '
            'деление r1/r2 с аккумулятором r3) → IEEE-float биты (0x3F800000=1.0); '
            'малые x→0. const-calc 10 кейсов (детерм.)')
def _(run, rng):
    """Emulator test @ 0x19bdc: E2-b66: 0x19bdc(a0,a1) — signed евклидов-подобный цикл (abs-u64, биту-по-биту деление r1/r2 с аккумулятором r3) → IEEE-float биты (0x3F800000=1.0); малые x→0. const-calc 10 кейсов (детерм.).
    Тест эмулятора @ 0x19bdc: E2-b66: 0x19bdc(a0,a1) — signed евклидов-подобный цикл (abs-u64, биту-по-биту деление r1/r2 с аккумулятором r3) → IEEE-float биты (0x3F800000=1.0); малые x→0. const-calc 10 кейсов (детерм.).
    """
    for (a0, a1), exp in _19BDC_CASES:
        r1, _e1 = _fresh_call(0x19BDC, (a0, a1), max_insn=200000)
        r2, _e2 = _fresh_call(0x19BDC, (a0, a1), max_insn=200000)
        assert r1 == r2, f'0x19bdc ({a0:#x},{a1:#x}): NDET {r1:#x}/{r2:#x}'
        assert r1 == exp, f'0x19bdc ({a0:#x},{a1:#x}): ret={r1:#x} ждём {exp:#x}'


# --- 0x19ab0: нормализованное мантиссенное сложение (u64-кластер §50.6) ---
_19AB0_CASES = [
    ((0, 0), 0x0), ((1, 0), 0x1), ((5, 0), 0x5), ((0x12345678, 0), 0x12345678),
    ((0xFFFFFFFF, 0), 0xFFFFFFFF), ((0, 1), 0x1), ((0, 0x800000), 0x800000),
    ((0, 0x80000000), 0x0), ((7, 3), 0x800005), ((3, 7), 0x800005),
    ((1, 1), 0x800001), ((2, 1), 0x800002), ((1, 2), 0x800002),
    ((0x800000, 0x800000), 0x1000000), ((0x1000000, 1), 0x1200000),
    ((0x1000000, 2), 0x1200000), ((0x1000000, 0x10), 0x1200004),
    ((0x800001, 1), 0xC00002), ((0x800002, 2), 0xC00003),
    ((0xFFFFFF, 1), 0x1200000), ((0xFFFFFF, 2), 0x1200000),
    ((0x1FFFFFF, 1), 0x2080000), ((0x1FFFFFF, 0x1000000), 0x2200000),
    ((0x3FFFFFF, 1), 0x4008000), ((0x800001, 0x800001), 0x1000001),
    ((0x7FFFFF, 0x7FFFFF), 0xFFFFFF),
]


@t(0x19AB0, 'E2-b66: 0x19ab0(a0,a1) — нормализованное мантиссенное сложение (24-bit мантисса, '
            'bit23=1; a1==0 → a0, a0==0 → a1 (кроме 0x80000000→0), оба ненулевые → сумма с '
            'ренормализацией в bit23; 25-bit перенос → доп. масштаб). const-calc 26 кейсов (детерм.)')
def _(run, rng):
    """Emulator test @ 0x19ab0: E2-b66: 0x19ab0(a0,a1) — нормализованное мантиссенное сложение (24-bit мантисса, bit23=1; a1==0 → a0, a0==0 → a1 (кроме 0x80000000→0), оба ненулевые → сумма с ренормализацией в bit23; 25-bit перенос → доп. масштаб). const-calc 26 кейсов (детерм.).
    Тест эмулятора @ 0x19ab0: E2-b66: 0x19ab0(a0,a1) — нормализованное мантиссенное сложение (24-bit мантисса, bit23=1; a1==0 → a0, a0==0 → a1 (кроме 0x80000000→0), оба ненулевые → сумма с ренормализацией в bit23; 25-bit перенос → доп. масштаб). const-calc 26 кейсов (детерм.).
    """
    for (a0, a1), exp in _19AB0_CASES:
        r1, _e1 = _fresh_call(0x19AB0, (a0, a1), max_insn=200000)
        r2, _e2 = _fresh_call(0x19AB0, (a0, a1), max_insn=200000)
        assert r1 == r2, f'0x19ab0 ({a0:#x},{a1:#x}): NDET {r1:#x}/{r2:#x}'
        assert r1 == exp, f'0x19ab0 ({a0:#x},{a1:#x}): ret={r1:#x} ждём {exp:#x}'


# --- 0x38ec: TLV + CRC-16 (таблица @0x19784) ---
@t(0x38EC, 'E2-b66: 0x38ec(src,dst,len_ptr) — TLV+ CRC-16: len=byte[src+3]; header 4B → dst; '
           '0x11a4 копирует len B (src+4→dst+4); crc=CRC-16-tab(dst,len+4) (tbl@flash 0x19784, '
           'init 0, idx=b^(crc>>8), crc=tbl[idx]^(crc<<8)); dst[len+4]=crc>>8, dst[len+5]=crc; '
           '*len_ptr=strb(len+6) (1 байт); ret=len+6. Реф-модель по flash-таблице эмулятора.')
def _(run, rng):
    """Emulator test @ 0x38ec: E2-b66: 0x38ec(src,dst,len_ptr) — TLV+ CRC-16: len=byte[src+3]; header 4B → dst; 0x11a4 копирует len B (src+4→dst+4); crc=CRC-16-tab(dst,len+4) (tbl@flash 0x19784, init 0, idx=b^(crc>>8), crc=tbl[idx]^(crc<<8)); dst[len+4]=crc>>8, dst[len+5]=crc; *len_ptr=strb(len+6) (1 байт); ret=len+6. Реф-модель по flash-таблице эмулятора..
    Тест эмулятора @ 0x38ec: E2-b66: 0x38ec(src,dst,len_ptr) — TLV+ CRC-16: len=byte[src+3]; header 4B → dst; 0x11a4 копирует len B (src+4→dst+4); crc=CRC-16-tab(dst,len+4) (tbl@flash 0x19784, init 0, idx=b^(crc>>8), crc=tbl[idx]^(crc<<8)); dst[len+4]=crc>>8, dst[len+5]=crc; *len_ptr=strb(len+6) (1 байт); ret=len+6. Реф-модель по flash-таблице эмулятора..
    """
    for _ in range(8):
        ln = rng.getrandbits(5)  # 0..31
        hdr = bytes(rng.getrandbits(8) for _ in range(3)) + bytes([ln])
        payload = bytes(rng.getrandbits(8) for _ in range(ln))
        src = RAM + 0x2000
        dst = RAM + 0x3000
        ptr = RAM + 0x4000
        ret, emu = _fresh_call(0x38EC, (src, dst, ptr), extra_ram=[
            (src, hdr + payload), (dst, bytes(64)), (ptr, bytes([0xAB] * 4))], max_insn=50000)
        uc = emu.uc
        tbl = struct.unpack_from('<256H', bytes(uc.mem_read(0x19784, 512)))
        crc = 0
        for b in hdr + payload:
            crc = (tbl[b ^ (crc >> 8)] ^ (crc << 8)) & 0xFFFF
        out = bytes(uc.mem_read(dst, 64))
        assert out[:4] == hdr, f'header: {out[:4].hex()} ≠ {hdr.hex()}'
        assert out[4:4 + ln] == payload, 'payload-копия'
        assert out[ln + 4] == (crc >> 8) & 0xFF, f'CRC hi: {out[ln + 4]:#x} ждём {(crc >> 8):#x}'
        assert out[ln + 5] == crc & 0xFF, f'CRC lo: {out[ln + 5]:#x} ждём {crc:#x}'
        assert ret == ln + 6, f'ret={ret:#x} ждём {ln + 6:#x}'
        pt = bytes(uc.mem_read(ptr, 4))
        assert pt[0] == (ln + 6) & 0xFF and pt[1:] == b'\xab' * 3, (
            f'*len_ptr (strb): {pt.hex()} ждём {(ln + 6) & 0xFF:02x} ab ab ab')


# --- one-shot флаги u32@0x8C: (каталог, реальный старт, бит, маска, callee) ---
_ONESHOT = [
    (0xD71C, 0xD70C, 0x9, 0x200, 0x1),      # 0xd41c(9) → ret 1 (fresh-emu)
    (0xD738, 0xD734, 0xD, 0x2000, 0x6),     # 0xd39c(0xD) → ret 6
    (0xD754, 0xD75C, 0x10, 0x10000, 0x6),   # 0xd39c(0x10)
    (0xD770, 0xD784, 0x11, 0x20000, 0x6),   # 0xd39c(0x11)
    (0xD78C, 0xD7AC, 0xB, 0x800, 0x1),      # 0xd46c(0xB)
    (0xD7A8, 0xD7D4, 0xF, 0x8000, 0x6),     # 0xd39c(0xF)
    (0xD7C4, 0xD7FC, 0xC, 0x1000, 0x1),     # 0xd46c(0xC)
    (0xD7E0, 0xD824, 0xA, 0x400, 0x1),      # 0xd46c(0xA)
]


def _t_oneshot(cat, start, bit, mask, callee_ret, _run, _rng):
    """The helper function (_t_oneshot).
    Вспомогательная функция (_t_oneshot).
    """
    for v in (0, 1 << bit):
        seeds = [(RAM + 0x8C, struct.pack('<I', v))]
        ret, emu = _fresh_call(start, (0,), extra_ram=seeds, max_insn=200000)
        uc = emu.uc
        got = struct.unpack_from('<I', bytes(uc.mem_read(RAM + 0x8C, 4)))[0]
        exp_ret = 0 if v == 0 else callee_ret
        assert ret == exp_ret, (
            f'0x{cat:x}: v={v:#x}: ret={ret:#x} ждём {exp_ret:#x}')
        assert got == v, (
            f'0x{cat:x}: v={v:#x}: u32[0x8C]={got:#x} ждём {v:#x} (clear только при callee==1)')


for _cat, _start, _bit, _mask, _cret in _ONESHOT:
    @t(_cat, f'E2-b66: 0x{_cat:x}() — one-shot флаг u32@0x8C (реальный старт 0x{_start:x}): '
             f'бит {_bit:#x} u16/u32[0x8C]: сброшен → ret 0, слово не меняется; '
             f'выставлен → bl (0xd39c/0xd46c/0xd41c)({_bit:#x}) → fresh-emu ret {_cret}, '
             f'бит не сбрасывается (clear при callee==1, в fresh-контексте не достигается).')
    def _(run, rng, _cat=_cat, _start=_start, _bit=_bit, _mask=_mask, _cret=_cret):
        """The helper function (_).
        Вспомогательная функция (_).
        """
        _t_oneshot(_cat, _start, _bit, _mask, _cret, run, rng)
