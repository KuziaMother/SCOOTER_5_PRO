# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-b82 (финальный): чистые спины 0x8884 (ret=stack/малое) / 0xb4ce / 0xb53a /
0xb8dc (ret<0x10000) / 0x22274 (ret=0/2) — insn>=50000 без записей; I2C-magic-
спины 0xd39c / 0xd46c / 0xd534 / 0xd5d4 / 0xf14c / 0x11724 / 0x117d4 / 0x156ac
(0x40022004: 0x45670123→0xCDEF89AB, 0x4002200C=FF, ret=1/6); GPIOB/DR-циклы
0xeddc (DR head=(3,2,0,0)) / 0x13b60 (head=(3,4,0,0), ~2150 insn) / 0x13c78 /
0x14368 / 0x147ac / 0x14802 / 0x1570c / 0x15790 / 0x157e0 (head=(6,5)) — DR из
повторяющихся блоков {3,2,0,0}/{3,4,0,0}/{6,5} с FF-прослойками, 0x40010818/28=
0x10, ret по фазе. После батча покрытие каталога — 100%."""
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


def _i2c_spin_check(off, exp_rets, tag):
    """I2C-magic-семейство: спин + 0x40022004 magic + 0x4002200C=FF, ret∈exp_rets."""
    uc, emu, lp = _fresh_probe(off)
    assert emu.insn > 10000, f'{tag}: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40022004) == [0x45670123, 0xCDEF89AB], \
        f'{tag}: 40022004={_pw(emu, 0x40022004)} ждём magic'
    assert _pw(emu, 0x4002200C) == [0xFFFFFFFF], \
        f"{tag}: 4002200C={_pw(emu, 0x4002200C)} ждём FF"
    assert len(emu.periph_writes) == 3, \
        f'{tag}: P={len(emu.periph_writes)} ждём 3'
    ret = uc.reg_read(UC_ARM_REG_R0)
    assert ret in exp_rets, f'{tag}: ret={ret:#x} ждём {exp_rets}'


def _spi_spin_check(off, head, exp_ret, tag):
    """GPIOB/DR-семейство: спин, 0x40010818/28=0x10, DR=head+повторяющиеся
    блоки (3,2,0,0)/(3,4,0,0)/(6,5) с FF-прослойками, ret по фазе."""
    uc, emu, lp = _fresh_probe(off)
    assert emu.insn > 1000, f'{tag}: insn={emu.insn} ждём цикл (>1000)'
    w28 = _pw(emu, 0x40010828)
    w18 = _pw(emu, 0x40010818)
    assert w28 and all(v == 0x10 for v in w28), \
        f'{tag}: 40010828={w28} ждём 0x10×N'
    assert w18 and all(v == 0x10 for v in w18), \
        f'{tag}: 40010818={w18} ждём 0x10×N'
    dr = _pw(emu, 0x4001300C)
    assert len(dr) >= len(head) + 8 and dr[:len(head)] == list(head), \
        f'{tag}: DR={dr[:8]}...(len={len(dr)}) ждём head={head}'
    nonff = [v for v in dr if v != 0xFF]
    assert all(v in (0, 2, 3, 4, 5, 6) for v in nonff) and \
        len(dr) - len(nonff) >= 8, \
        f'{tag}: DR nonFF={nonff[:12]} ждём блоки из {{0,2,3,4,5,6}} + FF×N'
    ret = uc.reg_read(UC_ARM_REG_R0)
    allowed = {exp_ret, exp_ret + 2, 0xFF, 0x40013000}
    assert ret in allowed, f'{tag}: ret={ret:#x} ждём {allowed}'


@t(0x8884, 'E2-b82: 0x8884() — чистый спин (insn>=50000, ret=stack-адрес или '
           'малое значение по фазе): без периферийных/RAM-побочных эффектов.')
def _(run, rng):
    """Emulator test @ 0x8884: E2-b82: 0x8884() — чистый спин (insn>=50000, ret=stack-адрес или малое значение по фазе): без периферийных/RAM-побочных эффектов..
    Тест эмулятора @ 0x8884: E2-b82: 0x8884() — чистый спин (insn>=50000, ret=stack-адрес или малое значение по фазе): без периферийных/RAM-побочных эффектов..
    """
    uc, emu, lp = _fresh_probe(0x8884)
    assert emu.insn >= 50000, f'0x8884: insn={emu.insn} ждём спин (>=50000)'
    assert len(emu.periph_writes) == 0, \
        f'0x8884: P={len(emu.periph_writes)} ждём 0'
    ret = uc.reg_read(UC_ARM_REG_R0)
    assert ret < 0x400 or 0x20017000 <= ret < STACK_TOP, \
        f'0x8884: ret={ret:#x} ждём stack/малое значение'


@t(0xB4CE, 'E2-b82: 0xb4ce() — чистый спин (insn>=50000, ret=0/2 по фазе): без '
           'побочных эффектов. smoke+spin golden.')
def _(run, rng):
    """Emulator test @ 0xb4ce: E2-b82: 0xb4ce() — чистый спин (insn>=50000, ret=0/2 по фазе): без побочных эффектов. smoke+spin golden..
    Тест эмулятора @ 0xb4ce: E2-b82: 0xb4ce() — чистый спин (insn>=50000, ret=0/2 по фазе): без побочных эффектов. smoke+spin golden..
    """
    uc, emu, lp = _fresh_probe(0xB4CE)
    assert emu.insn >= 50000, f'0xb4ce: insn={emu.insn} ждём спин (>=50000)'
    assert len(emu.periph_writes) == 0, \
        f'0xb4ce: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) in (0, 2), \
        f'0xb4ce: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0/2'


@t(0xB53A, 'E2-b82: 0xb53a() — чистый спин (insn>=50000, ret=0/2 по фазе): без '
           'побочных эффектов. smoke+spin golden.')
def _(run, rng):
    """Emulator test @ 0xb53a: E2-b82: 0xb53a() — чистый спин (insn>=50000, ret=0/2 по фазе): без побочных эффектов. smoke+spin golden..
    Тест эмулятора @ 0xb53a: E2-b82: 0xb53a() — чистый спин (insn>=50000, ret=0/2 по фазе): без побочных эффектов. smoke+spin golden..
    """
    uc, emu, lp = _fresh_probe(0xB53A)
    assert emu.insn >= 50000, f'0xb53a: insn={emu.insn} ждём спин (>=50000)'
    assert len(emu.periph_writes) == 0, \
        f'0xb53a: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) in (0, 2), \
        f'0xb53a: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0/2'


@t(0xB8DC, 'E2-b82: 0xb8dc() — чистый спин (insn>=50000, ret=малое значение по фазе, '
           'напр. 0xFF/0xEAB3): без побочных эффектов. smoke+spin golden.')
def _(run, rng):
    """Emulator test @ 0xb8dc: E2-b82: 0xb8dc() — чистый спин (insn>=50000, ret=малое значение по фазе, напр. 0xFF/0xEAB3): без побочных эффектов. smoke+spin golden..
    Тест эмулятора @ 0xb8dc: E2-b82: 0xb8dc() — чистый спин (insn>=50000, ret=малое значение по фазе, напр. 0xFF/0xEAB3): без побочных эффектов. smoke+spin golden..
    """
    uc, emu, lp = _fresh_probe(0xB8DC)
    assert emu.insn >= 50000, f'0xb8dc: insn={emu.insn} ждём спин (>=50000)'
    assert len(emu.periph_writes) == 0, \
        f'0xb8dc: P={len(emu.periph_writes)} ждём 0'
    ret = uc.reg_read(UC_ARM_REG_R0)
    assert ret < 0x10000, \
        f'0xb8dc: ret={ret:#x} ждём <0x10000 (фаза спина)'


@t(0x22274, 'E2-b82: 0x22274() — чистый спин (insn>=50000, ret=0/2 по фазе): без '
            'побочных эффектов. smoke+spin golden.')
def _(run, rng):
    """Emulator test @ 0x22274: E2-b82: 0x22274() — чистый спин (insn>=50000, ret=0/2 по фазе): без побочных эффектов. smoke+spin golden..
    Тест эмулятора @ 0x22274: E2-b82: 0x22274() — чистый спин (insn>=50000, ret=0/2 по фазе): без побочных эффектов. smoke+spin golden..
    """
    uc, emu, lp = _fresh_probe(0x22274)
    assert emu.insn >= 50000, f'0x22274: insn={emu.insn} ждём спин (>=50000)'
    assert len(emu.periph_writes) == 0, \
        f'0x22274: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) in (0, 2), \
        f'0x22274: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0/2'


@t(0xD39C, 'E2-b82: 0xd39c() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, '
           'ret=1/6. семейство-контракт.')
def _(run, rng):
    """Emulator test @ 0xd39c: E2-b82: 0xd39c() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, ret=1/6. семейство-контракт..
    Тест эмулятора @ 0xd39c: E2-b82: 0xd39c() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, ret=1/6. семейство-контракт..
    """
    _i2c_spin_check(0xD39C, (1, 6), '0xd39c')


@t(0xD46C, 'E2-b82: 0xd46c() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, '
           'ret=1/6. семейство-контракт.')
def _(run, rng):
    """Emulator test @ 0xd46c: E2-b82: 0xd46c() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, ret=1/6. семейство-контракт..
    Тест эмулятора @ 0xd46c: E2-b82: 0xd46c() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, ret=1/6. семейство-контракт..
    """
    _i2c_spin_check(0xD46C, (1, 6), '0xd46c')


@t(0xD534, 'E2-b82: 0xd534() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, '
           'ret=1/6. семейство-контракт.')
def _(run, rng):
    """Emulator test @ 0xd534: E2-b82: 0xd534() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, ret=1/6. семейство-контракт..
    Тест эмулятора @ 0xd534: E2-b82: 0xd534() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, ret=1/6. семейство-контракт..
    """
    _i2c_spin_check(0xD534, (1, 6), '0xd534')


@t(0xD5D4, 'E2-b82: 0xd5d4() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, '
           'ret=1/6. семейство-контракт.')
def _(run, rng):
    """Emulator test @ 0xd5d4: E2-b82: 0xd5d4() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, ret=1/6. семейство-контракт..
    Тест эмулятора @ 0xd5d4: E2-b82: 0xd5d4() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, ret=1/6. семейство-контракт..
    """
    _i2c_spin_check(0xD5D4, (1, 6), '0xd5d4')


@t(0xF14C, 'E2-b82: 0xf14c() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, '
           'ret=1/6. семейство-контракт.')
def _(run, rng):
    """Emulator test @ 0xf14c: E2-b82: 0xf14c() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, ret=1/6. семейство-контракт..
    Тест эмулятора @ 0xf14c: E2-b82: 0xf14c() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, ret=1/6. семейство-контракт..
    """
    _i2c_spin_check(0xF14C, (1, 6), '0xf14c')


@t(0x11724, 'E2-b82: 0x11724() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, '
            'ret=1/6. семейство-контракт.')
def _(run, rng):
    """Emulator test @ 0x11724: E2-b82: 0x11724() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, ret=1/6. семейство-контракт..
    Тест эмулятора @ 0x11724: E2-b82: 0x11724() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, ret=1/6. семейство-контракт..
    """
    _i2c_spin_check(0x11724, (1, 6), '0x11724')


@t(0x117D4, 'E2-b82: 0x117d4() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, '
            'ret=1/6. семейство-контракт.')
def _(run, rng):
    """Emulator test @ 0x117d4: E2-b82: 0x117d4() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, ret=1/6. семейство-контракт..
    Тест эмулятора @ 0x117d4: E2-b82: 0x117d4() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, ret=1/6. семейство-контракт..
    """
    _i2c_spin_check(0x117D4, (1, 6), '0x117d4')


@t(0x156AC, 'E2-b82: 0x156ac() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, '
            'ret=1/6. семейство-контракт.')
def _(run, rng):
    """Emulator test @ 0x156ac: E2-b82: 0x156ac() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, ret=1/6. семейство-контракт..
    Тест эмулятора @ 0x156ac: E2-b82: 0x156ac() — I2C-magic-спин: 0x40022004 magic, 0x4002200C=FF, ret=1/6. семейство-контракт..
    """
    _i2c_spin_check(0x156AC, (1, 6), '0x156ac')


@t(0xEDDC, 'E2-b82: 0xeddc() — GPIOB/DR-цикл (insn>1000): DR head=(3,2,0,0) + '
           'повторяющиеся блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт.')
def _(run, rng):
    """Emulator test @ 0xeddc: E2-b82: 0xeddc() — GPIOB/DR-цикл (insn>1000): DR head=(3,2,0,0) + повторяющиеся блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт..
    Тест эмулятора @ 0xeddc: E2-b82: 0xeddc() — GPIOB/DR-цикл (insn>1000): DR head=(3,2,0,0) + повторяющиеся блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт..
    """
    _spi_spin_check(0xEDDC, (3, 2, 0, 0), 0, '0xeddc')


@t(0x13B60, 'E2-b82: 0x13b60() — GPIOB/DR-цикл короткий (~2150 insn): '
            'DR head=(3,4,0,0) + блоки/FF, 0x40010818/28=0x10, ret по фазе.')
def _(run, rng):
    """Emulator test @ 0x13b60: E2-b82: 0x13b60() — GPIOB/DR-цикл короткий (~2150 insn): DR head=(3,4,0,0) + блоки/FF, 0x40010818/28=0x10, ret по фазе..
    Тест эмулятора @ 0x13b60: E2-b82: 0x13b60() — GPIOB/DR-цикл короткий (~2150 insn): DR head=(3,4,0,0) + блоки/FF, 0x40010818/28=0x10, ret по фазе..
    """
    _spi_spin_check(0x13B60, (3, 4, 0, 0), 0, '0x13b60')


@t(0x13C78, 'E2-b82: 0x13c78() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + '
            'блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт.')
def _(run, rng):
    """Emulator test @ 0x13c78: E2-b82: 0x13c78() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт..
    Тест эмулятора @ 0x13c78: E2-b82: 0x13c78() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт..
    """
    _spi_spin_check(0x13C78, (6, 5), 0, '0x13c78')


@t(0x14368, 'E2-b82: 0x14368() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + '
            'блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт.')
def _(run, rng):
    """Emulator test @ 0x14368: E2-b82: 0x14368() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт..
    Тест эмулятора @ 0x14368: E2-b82: 0x14368() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт..
    """
    _spi_spin_check(0x14368, (6, 5), 0xFF, '0x14368')


@t(0x147AC, 'E2-b82: 0x147ac() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + '
            'блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт.')
def _(run, rng):
    """Emulator test @ 0x147ac: E2-b82: 0x147ac() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт..
    Тест эмулятора @ 0x147ac: E2-b82: 0x147ac() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт..
    """
    _spi_spin_check(0x147AC, (6, 5), 9, '0x147ac')


@t(0x14802, 'E2-b82: 0x14802() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + '
            'блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт.')
def _(run, rng):
    """Emulator test @ 0x14802: E2-b82: 0x14802() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт..
    Тест эмулятора @ 0x14802: E2-b82: 0x14802() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт..
    """
    _spi_spin_check(0x14802, (6, 5), 1, '0x14802')


@t(0x1570C, 'E2-b82: 0x1570c() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + '
            'блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт.')
def _(run, rng):
    """Emulator test @ 0x1570c: E2-b82: 0x1570c() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт..
    Тест эмулятора @ 0x1570c: E2-b82: 0x1570c() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт..
    """
    _spi_spin_check(0x1570C, (6, 5), 9, '0x1570c')


@t(0x15790, 'E2-b82: 0x15790() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + '
            'блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт.')
def _(run, rng):
    """Emulator test @ 0x15790: E2-b82: 0x15790() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт..
    Тест эмулятора @ 0x15790: E2-b82: 0x15790() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт..
    """
    _spi_spin_check(0x15790, (6, 5), 9, '0x15790')


@t(0x157E0, 'E2-b82: 0x157e0() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + '
            'блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт.')
def _(run, rng):
    """Emulator test @ 0x157e0: E2-b82: 0x157e0() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт..
    Тест эмулятора @ 0x157e0: E2-b82: 0x157e0() — GPIOB/DR-цикл (insn>1000): DR head=(6,5) + блоки/FF, 0x40010818/28=0x10, ret по фазе. семейство-контракт..
    """
    _spi_spin_check(0x157E0, (6, 5), 1, '0x157e0')
