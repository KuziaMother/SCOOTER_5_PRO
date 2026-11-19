# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-b81: byte-флаг 0x15b84 (45 insn, ret=1, byte[0xB8C]=1); короткие чистые
0x15df4 (48 insn) / 0x16040 (2 insn, нормальный выход) / 0x173cc (77) / 0x1a688
(12) / 0x1de5e (627) / 0x1f71c (~22) / 0x216e4 (~10) / 0xc20c (9); magic-байты
0x1f1cc (65 insn, ret=1, byte[0xA43..0xA47]=04 63 44 A7 9C); GPIOB/DR-спин 0x13b14
(~5999 insn, DR=[3,0,0,0]+FF×N, 0x40010818/28=0x10); I2C-magic-спин 0xd00c
(insn>=50000, 0x40022004: 0x45670123→0xCDEF89AB, 0x4002200C=FF); чистый спин
0x57a0 (insn>=50000, ret=0x249)."""
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
        """The helper function (_hc).
        Вспомогательная функция (_hc).
        """
        lastpc[0] = address

    uc.hook_add(UC_HOOK_CODE, _hc)
    try:
        uc.emu_start(off | 1, 0, count=max_insn)
    except UcError:
        pass
    return uc, emu, lastpc[0]


def _r(uc, off, size=1):
    """The helper function (_r).
    Вспомогательная функция (_r).
    """
    return int.from_bytes(bytes(uc.mem_read(RAM + off, size)), 'little')


def _p(uc, addr, size=4):
    """The helper function (_p).
    Вспомогательная функция (_p).
    """
    return int.from_bytes(bytes(uc.mem_read(addr, size)), 'little')


def _pw(emu, addr):
    """Последовательность значений записей в periph-адрес."""
    return [v for _, a, _, v in emu.periph_writes if a == addr]


def _ramw(emu):
    """RAM-записи как [(off_RAM, size, value), ...]."""
    return [(a - RAM, s, v) for pc, a, s, v in getattr(emu, 'ram_writes', [])]


@t(0x15B84, 'E2-b81: 0x15b84() — byte-флаг (45 insn, ret=1): byte[0xB8C]=1 '
            '(1 запись). fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x15b84: E2-b81: 0x15b84() — byte-флаг (45 insn, ret=1): byte[0xB8C]=1 (1 запись). fresh-emu golden..
    Тест эмулятора @ 0x15b84: E2-b81: 0x15b84() — byte-флаг (45 insn, ret=1): byte[0xB8C]=1 (1 запись). fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x15B84)
    rw = _ramw(emu)
    assert rw == [(0xB8C, 1, 1)], \
        f'0x15b84: R={rw} ждём (0xB8C, 1, 1)'
    assert len(emu.periph_writes) == 0, \
        f'0x15b84: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x15b84: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'
    assert emu.insn == 45, f'0x15b84: insn={emu.insn} ждём 45'


@t(0x15DF4, 'E2-b81: 0x15df4() — короткий инициализатор (48 insn, ret=0, tail в '
            'unmapped): без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x15df4: E2-b81: 0x15df4() — короткий инициализатор (48 insn, ret=0, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    Тест эмулятора @ 0x15df4: E2-b81: 0x15df4() — короткий инициализатор (48 insn, ret=0, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x15DF4)
    assert len(emu.periph_writes) == 0, \
        f'0x15df4: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x15df4: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 48, f'0x15df4: insn={emu.insn} ждём 48'


@t(0x16040, 'E2-b81: 0x16040() — тривиальный (2 insn, ret=0, нормальный выход): '
            'без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x16040: E2-b81: 0x16040() — тривиальный (2 insn, ret=0, нормальный выход): без побочных эффектов. smoke+ret+insn golden..
    Тест эмулятора @ 0x16040: E2-b81: 0x16040() — тривиальный (2 insn, ret=0, нормальный выход): без побочных эффектов. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x16040)
    assert len(emu.periph_writes) == 0, \
        f'0x16040: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x16040: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 2, f'0x16040: insn={emu.insn} ждём 2'


@t(0x173CC, 'E2-b81: 0x173cc() — короткий инициализатор (77 insn, ret=0, tail в '
            'unmapped): без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x173cc: E2-b81: 0x173cc() — короткий инициализатор (77 insn, ret=0, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    Тест эмулятора @ 0x173cc: E2-b81: 0x173cc() — короткий инициализатор (77 insn, ret=0, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x173CC)
    assert len(emu.periph_writes) == 0, \
        f'0x173cc: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x173cc: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 77, f'0x173cc: insn={emu.insn} ждём 77'


@t(0x1A688, 'E2-b81: 0x1a688() — короткий инициализатор (12 insn, ret=0, tail в '
            'unmapped): без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x1a688: E2-b81: 0x1a688() — короткий инициализатор (12 insn, ret=0, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    Тест эмулятора @ 0x1a688: E2-b81: 0x1a688() — короткий инициализатор (12 insn, ret=0, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x1A688)
    assert len(emu.periph_writes) == 0, \
        f'0x1a688: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x1a688: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 12, f'0x1a688: insn={emu.insn} ждём 12'


@t(0x1DE5E, 'E2-b81: 0x1de5e() — чистый блок (627 insn, ret=0, tail в unmapped): '
            'без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x1de5e: E2-b81: 0x1de5e() — чистый блок (627 insn, ret=0, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    Тест эмулятора @ 0x1de5e: E2-b81: 0x1de5e() — чистый блок (627 insn, ret=0, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x1DE5E)
    assert len(emu.periph_writes) == 0, \
        f'0x1de5e: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x1de5e: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 627, f'0x1de5e: insn={emu.insn} ждём 627'


@t(0x1F1CC, 'E2-b81: 0x1f1cc() — magic-байты (65 insn, ret=1): '
            'byte[0xA43]=0x04, byte[0xA44]=0x63, byte[0xA45]=0x44, '
            'byte[0xA46]=0xA7, byte[0xA47]=0x9C (5 записей). fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x1f1cc: E2-b81: 0x1f1cc() — magic-байты (65 insn, ret=1): byte[0xA43]=0x04, byte[0xA44]=0x63, byte[0xA45]=0x44, byte[0xA46]=0xA7, byte[0xA47]=0x9C (5 записей). fresh-emu golden..
    Тест эмулятора @ 0x1f1cc: E2-b81: 0x1f1cc() — magic-байты (65 insn, ret=1): byte[0xA43]=0x04, byte[0xA44]=0x63, byte[0xA45]=0x44, byte[0xA46]=0xA7, byte[0xA47]=0x9C (5 записей). fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x1F1CC)
    rw = _ramw(emu)
    assert rw == [(0xA43, 1, 0x04), (0xA44, 1, 0x63), (0xA45, 1, 0x44),
                  (0xA46, 1, 0xA7), (0xA47, 1, 0x9C)], \
        f'0x1f1cc: R={rw} ждём magic-последовательность'
    assert len(emu.periph_writes) == 0, \
        f'0x1f1cc: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x1f1cc: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'
    assert emu.insn == 65, f'0x1f1cc: insn={emu.insn} ждём 65'


@t(0x1F71C, 'E2-b81: 0x1f71c() — короткий чистый блок (~22 insn, ret=0, tail в '
            'unmapped): без побочных эффектов; insn плавающий (20..100).')
def _(run, rng):
    """Emulator test @ 0x1f71c: E2-b81: 0x1f71c() — короткий чистый блок (~22 insn, ret=0, tail в unmapped): без побочных эффектов; insn плавающий (20..100)..
    Тест эмулятора @ 0x1f71c: E2-b81: 0x1f71c() — короткий чистый блок (~22 insn, ret=0, tail в unmapped): без побочных эффектов; insn плавающий (20..100)..
    """
    uc, emu, lp = _fresh_probe(0x1F71C)
    assert len(emu.periph_writes) == 0, \
        f'0x1f71c: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x1f71c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert 20 <= emu.insn <= 100, \
        f'0x1f71c: insn={emu.insn} ждём 20..100'


@t(0x216E4, 'E2-b81: 0x216e4() — короткий чистый блок (~10 insn, ret=0, tail в '
            'unmapped): без побочных эффектов; insn плавающий (5..60).')
def _(run, rng):
    """Emulator test @ 0x216e4: E2-b81: 0x216e4() — короткий чистый блок (~10 insn, ret=0, tail в unmapped): без побочных эффектов; insn плавающий (5..60)..
    Тест эмулятора @ 0x216e4: E2-b81: 0x216e4() — короткий чистый блок (~10 insn, ret=0, tail в unmapped): без побочных эффектов; insn плавающий (5..60)..
    """
    uc, emu, lp = _fresh_probe(0x216E4)
    assert len(emu.periph_writes) == 0, \
        f'0x216e4: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x216e4: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert 5 <= emu.insn <= 60, \
        f'0x216e4: insn={emu.insn} ждём 5..60'


@t(0xC20C, 'E2-b81: 0xc20c() — тривиальный (9 insn, ret=0, tail в unmapped): без '
           'побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0xc20c: E2-b81: 0xc20c() — тривиальный (9 insn, ret=0, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    Тест эмулятора @ 0xc20c: E2-b81: 0xc20c() — тривиальный (9 insn, ret=0, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0xC20C)
    assert len(emu.periph_writes) == 0, \
        f'0xc20c: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xc20c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 9, f'0xc20c: insn={emu.insn} ждём 9'


@t(0x13B14, 'E2-b81: 0x13b14() — GPIOB/DR-цикл (~5999 insn, ret=0/1 по фазе, 38 записей): '
            '0x40010828=[0x10], 0x40010818=[0x10]; SPI1_DR=[3,0,0,0]+0xFF×N (N>=10). '
            'fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x13b14: E2-b81: 0x13b14() — GPIOB/DR-цикл (~5999 insn, ret=0/1 по фазе, 38 записей): 0x40010828=[0x10], 0x40010818=[0x10]; SPI1_DR=[3,0,0,0]+0xFF×N (N>=10). fresh-emu golden..
    Тест эмулятора @ 0x13b14: E2-b81: 0x13b14() — GPIOB/DR-цикл (~5999 insn, ret=0/1 по фазе, 38 записей): 0x40010828=[0x10], 0x40010818=[0x10]; SPI1_DR=[3,0,0,0]+0xFF×N (N>=10). fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x13B14)
    assert 5000 <= emu.insn <= 6500, \
        f'0x13b14: insn={emu.insn} ждём ~5999'
    assert _pw(emu, 0x40010828) == [0x10], \
        f"0x13b14: 40010828={_pw(emu, 0x40010828)} ждём [0x10]"
    assert _pw(emu, 0x40010818) == [0x10], \
        f"0x13b14: 40010818={_pw(emu, 0x40010818)} ждём [0x10]"
    dr = _pw(emu, 0x4001300C)
    assert len(dr) >= 14 and dr[:4] == [3, 0, 0, 0] and \
        all(v == 0xFF for v in dr[4:]), \
        f'0x13b14: DR={dr[:10]}...(len={len(dr)}) ждём [3,0,0,0]+FF×N'
    ret = uc.reg_read(UC_ARM_REG_R0)
    assert ret in (0, 1), \
        f'0x13b14: ret={ret:#x} ждём 0/1 (фаза)'


@t(0xD00C, 'E2-b81: 0xd00c() — I2C-magic-спин (insn>=50000, ret=1/6, 3 записи): '
           '0x40022004: 0x45670123→0xCDEF89AB; 0x4002200C=0xFFFFFFFF. fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0xd00c: E2-b81: 0xd00c() — I2C-magic-спин (insn>=50000, ret=1/6, 3 записи): 0x40022004: 0x45670123→0xCDEF89AB; 0x4002200C=0xFFFFFFFF. fresh-emu golden..
    Тест эмулятора @ 0xd00c: E2-b81: 0xd00c() — I2C-magic-спин (insn>=50000, ret=1/6, 3 записи): 0x40022004: 0x45670123→0xCDEF89AB; 0x4002200C=0xFFFFFFFF. fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0xD00C)
    assert emu.insn >= 50000, f'0xd00c: insn={emu.insn} ждём спин (>=50000)'
    assert _pw(emu, 0x40022004) == [0x45670123, 0xCDEF89AB], \
        f"0xd00c: 40022004={_pw(emu, 0x40022004)} ждём magic"
    assert _pw(emu, 0x4002200C) == [0xFFFFFFFF], \
        f"0xd00c: 4002200C={_pw(emu, 0x4002200C)} ждём FF"
    assert len(emu.periph_writes) == 3, \
        f'0xd00c: P={len(emu.periph_writes)} ждём 3'
    assert uc.reg_read(UC_ARM_REG_R0) in (1, 6), \
        f'0xd00c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1/6'


@t(0x57A0, 'E2-b81: 0x57a0() — чистый спин (insn>=50000, ret=маленькое значение по фазе '
           'спина, напр. 0x249/0x2BE): без периферийных/RAM-побочных эффектов.')
def _(run, rng):
    """Emulator test @ 0x57a0: E2-b81: 0x57a0() — чистый спин (insn>=50000, ret=маленькое значение по фазе спина, напр. 0x249/0x2BE): без периферийных/RAM-побочных эффектов..
    Тест эмулятора @ 0x57a0: E2-b81: 0x57a0() — чистый спин (insn>=50000, ret=маленькое значение по фазе спина, напр. 0x249/0x2BE): без периферийных/RAM-побочных эффектов..
    """
    uc, emu, lp = _fresh_probe(0x57A0)
    assert emu.insn >= 50000, f'0x57a0: insn={emu.insn} ждём спин (>=50000)'
    assert len(emu.periph_writes) == 0, \
        f'0x57a0: P={len(emu.periph_writes)} ждём 0'
    ret = uc.reg_read(UC_ARM_REG_R0)
    assert ret < 0x400, \
        f'0x57a0: ret={ret:#x} ждём <0x400 (фаза спина)'
