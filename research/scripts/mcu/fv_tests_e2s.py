# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-b74: 0x40003000-конфигуратор 0x9a20 (0x5555→0xAAAA→0xCCCC + 0x3004=6,
0x3008=0, ret=0xCCCC), чистые инициализаторы 0x9048 (ret=0) / 0xa788 (ret=0x10) /
0xab0c / 0xabf0 / 0xb09a / 0x63b8 / 0x5dd8 (ret=0), константный 0x85c8
(ret=0x877400B0), byte-zero-серия 0x9134 (0xA42/0xA3E×3/0xA3F×3), флаг-кейс 0x5330
(fresh: 165 insn ret=0; flag byte[0x20000086]=1: I2C-spin magic, ret=1),
SPI/I2C-спин 0x1df4 (DR: 0xAB, 0x9F, FF×3 + magic 0xCDEF89AB, ret=1),
0x40021010-пульсатор 0xaf94 (FF→FFBFFFFF ×2 + 0x21018/1C=FF, ret=0x410200)."""
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


@t(0x9A20, 'E2-b74: 0x9a20() — 0x40003000-конфигуратор (28 insn, ret=0xCCCC): '
           '0x40003000: 0x5555→0xAAAA→0xCCCC (3 записи); 0x40003004=0x6; '
           '0x40003008=0x0. fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x9A20)
    assert _pw(emu, 0x40003000) == [0x5555, 0xAAAA, 0xCCCC], \
        f"0x9a20: 40003000={_pw(emu, 0x40003000)} ждём 5555→AAAA→CCCC"
    assert _pw(emu, 0x40003004) == [0x6], \
        f"0x9a20: 40003004={_pw(emu, 0x40003004)} ждём [6]"
    assert _pw(emu, 0x40003008) == [0x0], \
        f"0x9a20: 40003008={_pw(emu, 0x40003008)} ждём [0]"
    assert len(emu.periph_writes) == 5, \
        f'0x9a20: P={len(emu.periph_writes)} ждём 5'
    assert uc.reg_read(UC_ARM_REG_R0) == 0xCCCC, \
        f'0x9a20: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0xCCCC'
    assert emu.insn == 28, f'0x9a20: insn={emu.insn} ждём 28'


@t(0x9048, 'E2-b74: 0x9048() — чистый инициализатор (326 insn, ret=0): без '
           'периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x9048)
    assert len(emu.periph_writes) == 0, \
        f'0x9048: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x9048: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 326, f'0x9048: insn={emu.insn} ждём 326'


@t(0xA788, 'E2-b74: 0xa788() — чистый инициализатор (587 insn, ret=0x10): без '
           'периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xA788)
    assert len(emu.periph_writes) == 0, \
        f'0xa788: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x10, \
        f'0xa788: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x10'
    assert emu.insn == 587, f'0xa788: insn={emu.insn} ждём 587'


@t(0xAB0C, 'E2-b74: 0xab0c() — инициализатор (241 insn, ret=0, tail в unmapped): '
           'без периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xAB0C)
    assert len(emu.periph_writes) == 0, \
        f'0xab0c: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xab0c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 241, f'0xab0c: insn={emu.insn} ждём 241'


@t(0xABF0, 'E2-b74: 0xabf0() — инициализатор (167 insn, ret=0, tail в unmapped): '
           'без периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xABF0)
    assert len(emu.periph_writes) == 0, \
        f'0xabf0: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xabf0: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 167, f'0xabf0: insn={emu.insn} ждём 167'


@t(0xB09A, 'E2-b74: 0xb09a() — инициализатор (187 insn, ret=0, tail в unmapped): '
           'без периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xB09A)
    assert len(emu.periph_writes) == 0, \
        f'0xb09a: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xb09a: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 187, f'0xb09a: insn={emu.insn} ждём 187'


@t(0x85C8, 'E2-b74: 0x85c8() — константный возвращаемый (196 insn, ret=0x877400B0, '
           'tail в unmapped): без периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x85C8)
    assert len(emu.periph_writes) == 0, \
        f'0x85c8: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x877400B0, \
        f'0x85c8: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x877400B0'
    assert emu.insn == 196, f'0x85c8: insn={emu.insn} ждём 196'


@t(0x9134, 'E2-b74: 0x9134() — byte-zero-серия (99 insn, ret=0): byte[0xA42]=0, '
           'byte[0xA3E]=0 ×3, byte[0xA3F]=0 ×3 (7 записей). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x9134)
    rw = [(a - RAM, s, v) for pc, a, s, v in getattr(emu, 'ram_writes', [])]
    assert len(rw) == 7, f'0x9134: R={len(rw)} ждём 7'
    assert rw[0] == (0xA42, 1, 0), f'0x9134: R[0]={rw[0]} ждём (0xA42, 1, 0)'
    a3e = [w for w in rw if w[0] == 0xA3E]
    a3f = [w for w in rw if w[0] == 0xA3F]
    assert len(a3e) == 3 and all(w == (0xA3E, 1, 0) for w in a3e), \
        f'0x9134: 0xA3E={a3e} ждём ×3'
    assert len(a3f) == 3 and all(w == (0xA3F, 1, 0) for w in a3f), \
        f'0x9134: 0xA3F={a3f} ждём ×3'
    assert len(emu.periph_writes) == 0, \
        f'0x9134: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x9134: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 99, f'0x9134: insn={emu.insn} ждём 99'


@t(0x63B8, 'E2-b74: 0x63b8() — инициализатор (131 insn, ret=0, tail в unmapped): '
           'без периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x63B8)
    assert len(emu.periph_writes) == 0, \
        f'0x63b8: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x63b8: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 131, f'0x63b8: insn={emu.insn} ждём 131'


@t(0x5DD8, 'E2-b74: 0x5dd8() — короткий инициализатор (19 insn, ret=0, tail в '
           'unmapped): без периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x5DD8)
    assert len(emu.periph_writes) == 0, \
        f'0x5dd8: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x5dd8: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 19, f'0x5dd8: insn={emu.insn} ждём 19'


@t(0x5330, 'E2-b74: 0x5330() — флаг-кейс (флаг byte[0x20000086]): fresh (0) → '
           '165 insn ret=0 без записей; flag=1 → I2C-spin (insn>10000, ret=1, '
           '0x40022004: 0x45670123→0xCDEF89AB, 0x4002200C=0xFFFFFFFF). 2 кейса.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x5330)
    assert len(emu.periph_writes) == 0, \
        f'0x5330 fresh: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x5330 fresh: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 165, f'0x5330 fresh: insn={emu.insn} ждём 165'
    uc, emu, lp = _fresh_probe(0x5330, seeds=[(0x20000086, 1)])
    assert emu.insn > 10000, \
        f'0x5330 flag=1: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40022004) == [0x45670123, 0xCDEF89AB], \
        f"0x5330 flag=1: 40022004={_pw(emu, 0x40022004)} ждём magic"
    assert _pw(emu, 0x4002200C) == [0xFFFFFFFF], \
        f"0x5330 flag=1: 4002200C={_pw(emu, 0x4002200C)} ждём FF"
    assert len(emu.periph_writes) == 3, \
        f'0x5330 flag=1: P={len(emu.periph_writes)} ждём 3'
    assert uc.reg_read(UC_ARM_REG_R0) in (1, 6), \
        f'0x5330 flag=1: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1/6'


@t(0x1DF4, 'E2-b74: 0x1df4() — SPI/I2C-спин (insn>10000, ret=1, 12 записей): '
           'GPIOB 0x40010828=0x10 ×2, 0x40010818=0x10 ×2; SPI1_DR: 0xAB, 0x9F, '
           '0xFF ×3; I2C: 0x40022004: 0x45670123→0xCDEF89AB, 0x4002200C=FF. '
           'fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x1DF4)
    assert emu.insn > 10000, f'0x1df4: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40010828) == [0x10, 0x10], \
        f"0x1df4: 40010828={_pw(emu, 0x40010828)} ждём [0x10, 0x10]"
    assert _pw(emu, 0x40010818) == [0x10, 0x10], \
        f"0x1df4: 40010818={_pw(emu, 0x40010818)} ждём [0x10, 0x10]"
    assert _pw(emu, 0x4001300C) == [0xAB, 0x9F, 0xFF, 0xFF, 0xFF], \
        f"0x1df4: SPI1_DR={_pw(emu, 0x4001300C)} ждём AB,9F,FF×3"
    assert _pw(emu, 0x40022004) == [0x45670123, 0xCDEF89AB], \
        f"0x1df4: 40022004={_pw(emu, 0x40022004)} ждём magic"
    assert _pw(emu, 0x4002200C) == [0xFFFFFFFF], \
        f"0x1df4: 4002200C={_pw(emu, 0x4002200C)} ждём FF"
    assert len(emu.periph_writes) == 12, \
        f'0x1df4: P={len(emu.periph_writes)} ждём 12'
    assert uc.reg_read(UC_ARM_REG_R0) in (1, 6), \
        f'0x1df4: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1/6'


@t(0xAF94, 'E2-b74: 0xaf94() — 0x40021010-пульсатор (7961 insn, ret=0x410200): '
           '0x40021010: FF→0xFFBFFFFF ×2 (4 записи); 0x40021018: FF ×2; '
           '0x4002101C: FF (7 записей). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xAF94)
    assert _pw(emu, 0x40021010) == [0xFFFFFFFF, 0xFFBFFFFF,
                                    0xFFFFFFFF, 0xFFBFFFFF], \
        f"0xaf94: 40021010={_pw(emu, 0x40021010)} ждём FF→FFB ×2"
    assert _pw(emu, 0x40021018) == [0xFFFFFFFF, 0xFFFFFFFF], \
        f"0xaf94: 40021018={_pw(emu, 0x40021018)} ждём FF×2"
    assert _pw(emu, 0x4002101C) == [0xFFFFFFFF], \
        f"0xaf94: 4002101C={_pw(emu, 0x4002101C)} ждём FF"
    assert len(emu.periph_writes) == 7, \
        f'0xaf94: P={len(emu.periph_writes)} ждём 7'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x410200, \
        f'0xaf94: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x410200'
    assert emu.insn == 7961, f'0xaf94: insn={emu.insn} ждём 7961'
