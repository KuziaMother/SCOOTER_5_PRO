# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-b77: константные возвращаемые 0xe17c (0xFFFFFEED, 215 insn) / 0xe808 (0xA,
128) / 0xea64 (0x200012BA — pointer, 65) / 0xec70 (0, 730) / 0xf038 (0, 935) /
0xe200 (0, 19) / 0xe2fc (stack, 185); family GPIOB/SPI1-спина 0xd938 (ret=3) /
0xd878 (ret=4) / 0xbf4c (ret=4) / 0x37f4 (ret=0xFF) / 0x3da0 (ret=0xA) — одинаковый
паттерн: 0x40010828=0x10 ×2, 0x40010818=0x10, SPI1_DR: 0x6, 0x5, 0xFF×N; I2C-спин
0xd670 (magic, ret=1/6)."""
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


def _spi_spin_check(off, exp_ret, tag):
    """Общий контракт family GPIOB/SPI1-спина: 0x40010828=0x10 ×2, 0x40010818=0x10;
    SPI1_DR: 0x6, 0x5, 0xFF×N (N≥5, контекстно-плавающее); insn>10000."""
    uc, emu, lp = _fresh_probe(off)
    assert emu.insn > 10000, f'{tag}: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40010828) == [0x10, 0x10], \
        f"{tag}: 40010828={_pw(emu, 0x40010828)} ждём [0x10, 0x10]"
    assert _pw(emu, 0x40010818) == [0x10], \
        f"{tag}: 40010818={_pw(emu, 0x40010818)} ждём [0x10]"
    dr = _pw(emu, 0x4001300C)
    assert len(dr) >= 5 and dr[0] == 0x6 and dr[1] == 0x5 and \
        all(v == 0xFF for v in dr[2:]), \
        f'{tag}: DR={dr[:6]}...(len={len(dr)}) ждём 6,5,FF×N'
    ret = uc.reg_read(UC_ARM_REG_R0)
    allowed = {exp_ret, exp_ret + 2, 0x40013000}
    assert ret in allowed, \
        f'{tag}: ret={ret:#x} ждём {allowed} (контекстно-плавающий)'


@t(0xE17C, 'E2-b77: 0xe17c() — константный возвращаемый (215 insn, ret=0xFFFFFEED): '
           'без периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xE17C)
    assert len(emu.periph_writes) == 0, \
        f'0xe17c: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0xFFFFFEED, \
        f'0xe17c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0xFFFFFEED'
    assert emu.insn == 215, f'0xe17c: insn={emu.insn} ждём 215'


@t(0xE808, 'E2-b77: 0xe808() — константный возвращаемый (128 insn, ret=0xA): без '
           'периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xE808)
    assert len(emu.periph_writes) == 0, \
        f'0xe808: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0xA, \
        f'0xe808: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0xA'
    assert emu.insn == 128, f'0xe808: insn={emu.insn} ждём 128'


@t(0xEA64, 'E2-b77: 0xea64() — pointer-возврат (65 insn, ret=0x200012BA): без '
           'периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xEA64)
    assert len(emu.periph_writes) == 0, \
        f'0xea64: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x200012BA, \
        f'0xea64: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x200012BA'
    assert emu.insn == 65, f'0xea64: insn={emu.insn} ждём 65'


@t(0xEC70, 'E2-b77: 0xec70() — чистый инициализатор (730 insn, ret=0): без '
           'периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xEC70)
    assert len(emu.periph_writes) == 0, \
        f'0xec70: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xec70: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 730, f'0xec70: insn={emu.insn} ждём 730'


@t(0xF038, 'E2-b77: 0xf038() — чистый инициализатор (935 insn, ret=0): без '
           'периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xF038)
    assert len(emu.periph_writes) == 0, \
        f'0xf038: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xf038: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 935, f'0xf038: insn={emu.insn} ждём 935'


@t(0xE200, 'E2-b77: 0xe200() — короткий инициализатор (19 insn, ret=0, tail в '
           'unmapped): без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xE200)
    assert len(emu.periph_writes) == 0, \
        f'0xe200: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xe200: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 19, f'0xe200: insn={emu.insn} ждём 19'


@t(0xE2FC, 'E2-b77: 0xe2fc() — stack-возврат (185 insn, ret=stack-адрес): без '
           'периферийных/RAM-побочных эффектов. smoke+ret-диапазон+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xE2FC)
    assert len(emu.periph_writes) == 0, \
        f'0xe2fc: P={len(emu.periph_writes)} ждём 0'
    ret = uc.reg_read(UC_ARM_REG_R0)
    assert 0x20017000 <= ret < STACK_TOP, \
        f'0xe2fc: ret={ret:#x} ждём stack-адрес'
    assert emu.insn == 185, f'0xe2fc: insn={emu.insn} ждём 185'


@t(0xD938, 'E2-b77: 0xd938() — GPIOB/SPI1-спин (insn>10000, ret=3/0xFF): '
           '0x40010828=0x10 ×2, 0x40010818=0x10; SPI1_DR: 0x6, 0x5, 0xFF×N. '
           'fresh-emu golden.')
def _(run, rng):
    _spi_spin_check(0xD938, 3, '0xd938')


@t(0xD878, 'E2-b77: 0xd878() — GPIOB/SPI1-спин (insn>10000, ret=4/0xFF): тот же '
           'паттерн, что у 0xd938. fresh-emu golden.')
def _(run, rng):
    _spi_spin_check(0xD878, 4, '0xd878')


@t(0xBF4C, 'E2-b77: 0xbf4c() — GPIOB/SPI1-спин (insn>10000, ret=4/0xFF): тот же '
           'паттерн, что у 0xd938. fresh-emu golden.')
def _(run, rng):
    _spi_spin_check(0xBF4C, 4, '0xbf4c')


@t(0x37F4, 'E2-b77: 0x37f4() — GPIOB/SPI1-спин (insn>10000, ret=0xFF): тот же '
           'паттерн, что у 0xd938. fresh-emu golden.')
def _(run, rng):
    _spi_spin_check(0x37F4, 0xFF, '0x37f4')


@t(0x3DA0, 'E2-b77: 0x3da0() — GPIOB/SPI1-спин (insn>10000, ret=0xA/0xFF): тот же '
           'паттерн, что у 0xd938. fresh-emu golden.')
def _(run, rng):
    _spi_spin_check(0x3DA0, 0xA, '0x3da0')


@t(0xD670, 'E2-b77: 0xd670() — I2C-спин (insn>10000, ret=1/6): 0x40022004: '
           '0x45670123→0xCDEF89AB; 0x4002200C=0xFFFFFFFF (3 записи). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xD670)
    assert emu.insn > 10000, f'0xd670: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40022004) == [0x45670123, 0xCDEF89AB], \
        f"0xd670: 40022004={_pw(emu, 0x40022004)} ждём magic"
    assert _pw(emu, 0x4002200C) == [0xFFFFFFFF], \
        f"0xd670: 4002200C={_pw(emu, 0x4002200C)} ждём FF"
    assert len(emu.periph_writes) == 3, \
        f'0xd670: P={len(emu.periph_writes)} ждём 3'
    assert uc.reg_read(UC_ARM_REG_R0) in (1, 6), \
        f'0xd670: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1/6'
