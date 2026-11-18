# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-b78: GPIOB+SPI1-конфигуратор 0x10788 (28 записей: CRL-каскады 6 адресов,
SPI1 0x334F/0xF7FF/0x7, ret=0x40013000), SPI1-сброс 0x10870 (DR=0, ret=0),
RCC-каскады 0x10ba0 (AHB1ENR ×3 + APB1ENR ×4 + AHB2ENR=0xF8) / 0x10cdc
(AHB1ENR ×2 + APB1ENR ×4), byte-флаг 0x11894 (byte[0xA51]=1, ~1683 insn, ret=1),
u16-серии 0x11978 (7 записей) / 0x11998 (10 записей) / 0xf994 (3 записи, ret=1),
twin 0x5bc4-инита 0x110fc (29 записей, ret=0x4621463A), короткие 0xef78 (5 insn) /
0xb476 (9) / 0x7d6c (2), I2C-спин 0x11674 (magic, ret=1/6)."""
import struct

from fv_core import *  # noqa: F401,F403

from unicorn import UcError, UC_HOOK_CODE  # noqa: E402
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,  # noqa: E402
                               UC_ARM_REG_SP, UC_ARM_REG_LR)


def _fresh_probe(off, seeds=(), args=(), max_insn=60000):
    """Fresh-emu: чистый RAM, 0xFF PERIPH, seeds (int->u32 / bytes), args r0..r3;
    возвращает (uc, emu, lastpc)."""
    emu = McuEmu(max_insn=max_insn)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))
    emu.hook_periph_ready()
    for addr, val in seeds:
        if isinstance(val, (bytes, bytearray)):
            uc.mem_write(addr, val)
        else:
            uc.mem_write(addr, struct.pack('<I', val))
    regs = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)
    for i, a in enumerate(args):
        uc.reg_write(regs[i], a)
    uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
    uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    lastpc = [0]

    def _hc(uc_, address, size, user):
        lastpc[0] = address

    uc.hook_add(UC_HOOK_CODE, _hc)
    try:
        uc.emu_start(off | 1, 0, count=max_insn)
    except UcError:
        pass
    return uc, emu, lastpc[0]


def _r(uc, off, size=1):
    return int.from_bytes(bytes(uc.mem_read(RAM + off, size)), 'little')


def _p(uc, addr, size=4):
    return int.from_bytes(bytes(uc.mem_read(addr, size)), 'little')


def _pw(emu, addr):
    """Последовательность значений записей в periph-адрес."""
    return [v for _, a, _, v in emu.periph_writes if a == addr]


@t(0x10788, 'E2-b78: 0x10788() — GPIOB+SPI1-конфигуратор (823 insn, ret=0x40013000, '
            '28 записей): 0x40021018=FF ×2; CRL-каскады: 0x40010820: FF0FFFFF→F0FFFFF→FFFFF; '
            '0x40010800: FFFFFBFF→FFFFBBFF→FFFF8BFF→FFFF89FF; 0x4001080C: FFFFF3FF→FFFF33FF→'
            'FFFF03FF→FFFF00FF; 0x4001082C: FFFFF3FF→FFFF33FF→FFFF30FF; 0x40010808: '
            'FFFFFFDF→FFFFFF5F→FFFFFF1F→FFFFFF0F; 0x40010804: FFFFFFDF→FFFFFF5F→FFFFFF4F; '
            '0x40010818=0x10; SPI1: 0x40013000=0x334F ×2, 0x4001301C=0xF7FF, 0x40013010=0x7.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x10788)
    assert len(emu.periph_writes) == 28, \
        f'0x10788: P={len(emu.periph_writes)} ждём 28'
    assert _pw(emu, 0x40021018) == [0xFFFFFFFF, 0xFFFFFFFF], \
        f"0x10788: 40021018={_pw(emu, 0x40021018)}"
    assert _pw(emu, 0x40010820) == [0xFF0FFFFF, 0xF0FFFFF, 0xFFFFF], \
        f"0x10788: 40010820={_pw(emu, 0x40010820)}"
    assert _pw(emu, 0x40010800) == [0xFFFFFBFF, 0xFFFFBBFF,
                                    0xFFFF8BFF, 0xFFFF89FF], \
        f"0x10788: 40010800={_pw(emu, 0x40010800)}"
    assert _pw(emu, 0x4001080C) == [0xFFFFF3FF, 0xFFFF33FF,
                                    0xFFFF03FF, 0xFFFF00FF], \
        f"0x10788: 4001080C={_pw(emu, 0x4001080C)}"
    assert _pw(emu, 0x4001082C) == [0xFFFFF3FF, 0xFFFF33FF, 0xFFFF30FF], \
        f"0x10788: 4001082C={_pw(emu, 0x4001082C)}"
    assert _pw(emu, 0x40010808) == [0xFFFFFFDF, 0xFFFFFF5F,
                                    0xFFFFFF1F, 0xFFFFFF0F], \
        f"0x10788: 40010808={_pw(emu, 0x40010808)}"
    assert _pw(emu, 0x40010804) == [0xFFFFFFDF, 0xFFFFFF5F, 0xFFFFFF4F], \
        f"0x10788: 40010804={_pw(emu, 0x40010804)}"
    assert _pw(emu, 0x40010818) == [0x10], \
        f"0x10788: 40010818={_pw(emu, 0x40010818)}"
    assert _pw(emu, 0x40013000) == [0x334F, 0x334F], \
        f"0x10788: SPI1_CTLR={_pw(emu, 0x40013000)}"
    assert _pw(emu, 0x4001301C) == [0xF7FF], \
        f"0x10788: SPI1_RTDR={_pw(emu, 0x4001301C)}"
    assert _pw(emu, 0x40013010) == [0x7], \
        f"0x10788: SPI1={_pw(emu, 0x40013010)}"
    assert uc.reg_read(UC_ARM_REG_R0) == 0x40013000, \
        f'0x10788: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x40013000'
    assert emu.insn == 823, f'0x10788: insn={emu.insn} ждём 823'


@t(0x10870, 'E2-b78: 0x10870() — SPI1-сброс (104 insn, ret=0): 0x4001300C=0x0 '
            '(1 запись). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x10870)
    assert _pw(emu, 0x4001300C) == [0x0], \
        f"0x10870: SPI1_DR={_pw(emu, 0x4001300C)} ждём [0]"
    assert len(emu.periph_writes) == 1, \
        f'0x10870: P={len(emu.periph_writes)} ждём 1'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x10870: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 104, f'0x10870: insn={emu.insn} ждём 104'


@t(0x10BA0, 'E2-b78: 0x10ba0() — RCC-каскад (189 insn, ret=0, 8 записей): '
            '0x40021000: FFFEFF FF→FFFAFF FF→FFFBFF FF; 0x40021004: FFFFFFFC→FFFFFF0C→'
            'FFFFC70C→FFFFC00C; 0x40022000=0xF8. fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x10BA0)
    assert _pw(emu, 0x40021000) == [0xFFFEFFFF, 0xFFFaffFF, 0xFFFBFFFF], \
        f"0x10ba0: 40021000={_pw(emu, 0x40021000)}"
    assert _pw(emu, 0x40021004) == [0xFFFFFFFC, 0xFFFFFF0C,
                                    0xFFFFC70C, 0xFFFFC00C], \
        f"0x10ba0: 40021004={_pw(emu, 0x40021004)}"
    assert _pw(emu, 0x40022000) == [0xF8], \
        f"0x10ba0: 40022000={_pw(emu, 0x40022000)}"
    assert len(emu.periph_writes) == 8, \
        f'0x10ba0: P={len(emu.periph_writes)} ждём 8'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x10ba0: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 189, f'0x10ba0: insn={emu.insn} ждём 189'


@t(0x10CDC, 'E2-b78: 0x10cdc() — RCC-каскад twin (184 insn, ret=0, 7 записей): '
            '0x40021000: FFFFFFFE→FFFFFFFF; 0x40021004: FFFFFFFC→FFFFFF0C→FFFFC70C→'
            'FFFFC00C; 0x40022000=0xF8. fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x10CDC)
    assert _pw(emu, 0x40021000) == [0xFFFFFFFE, 0xFFFFFFFF], \
        f"0x10cdc: 40021000={_pw(emu, 0x40021000)}"
    assert _pw(emu, 0x40021004) == [0xFFFFFFFC, 0xFFFFFF0C,
                                    0xFFFFC70C, 0xFFFFC00C], \
        f"0x10cdc: 40021004={_pw(emu, 0x40021004)}"
    assert _pw(emu, 0x40022000) == [0xF8], \
        f"0x10cdc: 40022000={_pw(emu, 0x40022000)}"
    assert len(emu.periph_writes) == 7, \
        f'0x10cdc: P={len(emu.periph_writes)} ждём 7'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x10cdc: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 184, f'0x10cdc: insn={emu.insn} ждём 184'


@t(0x11894, 'E2-b78: 0x11894() — byte-флаг (~1683 insn, ret=1): byte[0xA51]=1 '
            '(1 запись), без периферийных эффектов. insn плавающий (>1500).')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x11894)
    rw = [(a - RAM, s, v) for pc, a, s, v in getattr(emu, 'ram_writes', [])]
    assert rw == [(0xA51, 1, 1)], f'0x11894: R={rw} ждём (0xA51, 1, 1)'
    assert len(emu.periph_writes) == 0, \
        f'0x11894: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x11894: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'
    assert emu.insn > 1500, f'0x11894: insn={emu.insn} ждём >1500'


@t(0x11978, 'E2-b78: 0x11978() — u16-серия (1125 insn, ret=0, 7 записей): '
            'u16[0xA22]=1; u16[0xA2A]=0; u16[0xA26]=0; u16[0xA2E]=0; u16[0xA30]=0; '
            'u16[0xA3A]=0; u16[0xA36]=0. fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x11978)
    rw = [(a - RAM, s, v) for pc, a, s, v in getattr(emu, 'ram_writes', [])]
    assert rw == [(0xA22, 2, 1), (0xA2A, 2, 0), (0xA26, 2, 0),
                  (0xA2E, 2, 0), (0xA30, 2, 0), (0xA3A, 2, 0),
                  (0xA36, 2, 0)], \
        f'0x11978: R={rw} ждём u16-последовательность'
    assert len(emu.periph_writes) == 0, \
        f'0x11978: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x11978: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 1125, f'0x11978: insn={emu.insn} ждём 1125'


@t(0x11998, 'E2-b78: 0x11998() — u16-серия (267 insn, ret=0, 10 записей): '
            'u16[0xA00]=0, u16[0xA02]=0, u16[0xA08]=1, u16[0xA0E]=0, u16[0xA10]=0, '
            'u16[0xA1A]=1, u16[0xA12]=0, u16[0xA14]=0, u16[0xA16]=0, u16[0xA18]=0.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x11998)
    rw = [(a - RAM, s, v) for pc, a, s, v in getattr(emu, 'ram_writes', [])]
    assert rw == [(0xA00, 2, 0), (0xA02, 2, 0), (0xA08, 2, 1),
                  (0xA0E, 2, 0), (0xA10, 2, 0), (0xA1A, 2, 1),
                  (0xA12, 2, 0), (0xA14, 2, 0), (0xA16, 2, 0),
                  (0xA18, 2, 0)], \
        f'0x11998: R={rw} ждём u16-последовательность'
    assert len(emu.periph_writes) == 0, \
        f'0x11998: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x11998: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 267, f'0x11998: insn={emu.insn} ждём 267'


@t(0xF994, 'E2-b78: 0xf994() — u16-серия короткая (51 insn, ret=1, 3 записи): '
           'u16[0xA00]=0, u16[0xA02]=0, u16[0xA08]=1. fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xF994)
    rw = [(a - RAM, s, v) for pc, a, s, v in getattr(emu, 'ram_writes', [])]
    assert rw == [(0xA00, 2, 0), (0xA02, 2, 0), (0xA08, 2, 1)], \
        f'0xf994: R={rw} ждём u16-последовательность'
    assert len(emu.periph_writes) == 0, \
        f'0xf994: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0xf994: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'
    assert emu.insn == 51, f'0xf994: insn={emu.insn} ждём 51'


@t(0x110FC, 'E2-b78: 0x110fc() — twin 0x5bc4-инита (604 insn, ret=0x4621463A, 29 записей '
            '+ byte[0xA64]=0, byte[0xB82]=0): RCC 0x40021014/18, 0x4002102C FE0F→FE02, '
            '0x40021028 clr, UART3, GPIOB 0x10×2, SPI1 0xFFBF+0xB9, 0x4002100C/18 clr.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x110FC)
    assert len(emu.periph_writes) == 29, \
        f'0x110fc: P={len(emu.periph_writes)} ждём 29'
    assert _pw(emu, 0x4002102C) == [0xFFFFFE0F, 0xFFFFFE02], \
        f"0x110fc: 4002102C={_pw(emu, 0x4002102C)}"
    assert _p(uc, 0x40021028) in (0xFFFFEFFF, 0xFFFFFFEF), \
        f'0x110fc: 40021028={_p(uc, 0x40021028):#x} ждём clr'
    assert _p(uc, 0x40020004) == 0xFFFFFFFF, \
        f"0x110fc: 40020004={_p(uc, 0x40020004):#x} ждём FF"
    assert _p(uc, 0x40010818) == 0x10 and _p(uc, 0x40010828) == 0x10, \
        f"0x110fc: 40010818/28={_p(uc, 0x40010818):#x}/{_p(uc, 0x40010828):#x}"
    assert _p(uc, 0x40013000, 2) == 0xFFBF, \
        f"0x110fc: SPI1_CTLR={_p(uc, 0x40013000, 2):#x} ждём 0xFFBF"
    assert _p(uc, 0x4001300C, 2) == 0xB9, \
        f"0x110fc: SPI1_DR={_p(uc, 0x4001300C, 2):#x} ждём 0xB9"
    assert _p(uc, 0x4002100C) in (0xFFFFEFFF, 0xFFFFFFEF), \
        f'0x110fc: 4002100C={_p(uc, 0x4002100C):#x} ждём clr'
    assert _p(uc, 0x40021018) in (0xFFFFEFFF, 0xFFFFFFEF), \
        f'0x110fc: 40021018={_p(uc, 0x40021018):#x} ждём clr'
    rw = [(a - RAM, s, v) for pc, a, s, v in getattr(emu, 'ram_writes', [])]
    assert (0xA64, 1, 0) in rw and (0xB82, 1, 0) in rw, \
        f'0x110fc: R={rw} ждём 0xA64/0xB82'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x4621463A, \
        f'0x110fc: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x4621463A'
    assert emu.insn > 500, f'0x110fc: insn={emu.insn} ждём >500'


@t(0xEf78, 'E2-b78: 0xef78() — короткий инициализатор (5 insn, ret=0, tail в '
           'unmapped): без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xEf78)
    assert len(emu.periph_writes) == 0, \
        f'0xef78: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xef78: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 5, f'0xef78: insn={emu.insn} ждём 5'


@t(0xB476, 'E2-b78: 0xb476() — короткий инициализатор (9 insn, ret=0, tail в '
           'unmapped): без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xB476)
    assert len(emu.periph_writes) == 0, \
        f'0xb476: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xb476: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 9, f'0xb476: insn={emu.insn} ждём 9'


@t(0x7D6C, 'E2-b78: 0x7d6c() — тривиальный (2 insn, ret=0, нормальный выход): без '
           'побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x7D6C)
    assert len(emu.periph_writes) == 0, \
        f'0x7d6c: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x7d6c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 2, f'0x7d6c: insn={emu.insn} ждём 2'


@t(0x11674, 'E2-b78: 0x11674() — I2C-спин (insn>10000, ret=1/6): 0x40022004: '
            '0x45670123→0xCDEF89AB; 0x4002200C=0xFFFFFFFF (3 записи). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x11674)
    assert emu.insn > 10000, f'0x11674: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40022004) == [0x45670123, 0xCDEF89AB], \
        f"0x11674: 40022004={_pw(emu, 0x40022004)} ждём magic"
    assert _pw(emu, 0x4002200C) == [0xFFFFFFFF], \
        f"0x11674: 4002200C={_pw(emu, 0x4002200C)} ждём FF"
    assert len(emu.periph_writes) == 3, \
        f'0x11674: P={len(emu.periph_writes)} ждём 3'
    assert uc.reg_read(UC_ARM_REG_R0) in (1, 6), \
        f'0x11674: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1/6'
