# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-b75: 0xc368 флаг-кейс (flag byte[0x20000088]=1: 0x40003000=0xAAAA, ret=0xAAAA,
35 insn; fresh: спин ret=stack), 0xc098 (ret=0x10, 631 insn, byte-серия 0xA65/0xA66/0xA67),
чистые инициализаторы 0xc158 (736) / 0xc304 (589) (ret=0x10), длинный compute 0xb302
(7167 insn, ret=9), u16-цикл 0x9a44 (u32[0xB4C]=0 + u16[0xB5C]: 1→0 ×N), 0x90a0
(u16[0xB5C]: 1→0, ret=0), короткие 0xa960/0xaa18 (13 insn) / 0xb582 (22) / 0xb618 (30)
/ 0x6838 (71) (ret=0), SPI-спин 0x8434 (DR: 0x5, 0xFF×N, 0x40010828=0x10, ret=5)."""
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


@t(0xC368, 'E2-b75: 0xc368() — флаг-кейс (флаг byte[0x20000088]): flag=1 → '
           '0x40003000=0xAAAA, ret=0xAAAA, 35 insn; fresh (0) → спин (insn>10000), '
           'ret=stack-адрес, без записей. 2 кейса.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xC368, seeds=[(0x20000088, 1)])
    assert _pw(emu, 0x40003000) == [0xAAAA], \
        f"0xc368 flag=1: 40003000={_pw(emu, 0x40003000)} ждём [0xAAAA]"
    assert len(emu.periph_writes) == 1, \
        f'0xc368 flag=1: P={len(emu.periph_writes)} ждём 1'
    assert uc.reg_read(UC_ARM_REG_R0) == 0xAAAA, \
        f'0xc368 flag=1: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0xAAAA'
    assert emu.insn == 35, f'0xc368 flag=1: insn={emu.insn} ждём 35'
    uc, emu, lp = _fresh_probe(0xC368)
    assert emu.insn > 10000, \
        f'0xc368 fresh: insn={emu.insn} ждём спин (>10000)'
    assert len(emu.periph_writes) == 0, \
        f'0xc368 fresh: P={len(emu.periph_writes)} ждём 0'
    ret = uc.reg_read(UC_ARM_REG_R0)
    assert ret in (0x2001736F, 0x68), \
        f'0xc368 fresh: ret={ret:#x} ждём 0x2001736F/0x68'


@t(0xC098, 'E2-b75: 0xc098() — byte-серия (631 insn, ret=0x10): byte[0xA65]=1, '
           'byte[0xA66]=0 ×2, byte[0xA65]=0, byte[0xA67]=1 (5 записей). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xC098)
    rw = [(a - RAM, s, v) for pc, a, s, v in getattr(emu, 'ram_writes', [])]
    assert rw == [(0xA65, 1, 1), (0xA66, 1, 0), (0xA66, 1, 0),
                  (0xA65, 1, 0), (0xA67, 1, 1)], \
        f'0xc098: R={rw} ждём A65/A66/A67-последовательность'
    assert len(emu.periph_writes) == 0, \
        f'0xc098: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x10, \
        f'0xc098: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x10'
    assert emu.insn == 631, f'0xc098: insn={emu.insn} ждём 631'


@t(0xC158, 'E2-b75: 0xc158() — чистый инициализатор (736 insn, ret=0x10): без '
           'периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xC158)
    assert len(emu.periph_writes) == 0, \
        f'0xc158: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x10, \
        f'0xc158: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x10'
    assert emu.insn == 736, f'0xc158: insn={emu.insn} ждём 736'


@t(0xC304, 'E2-b75: 0xc304() — чистый инициализатор (589 insn, ret=0x10): без '
           'периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xC304)
    assert len(emu.periph_writes) == 0, \
        f'0xc304: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x10, \
        f'0xc304: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x10'
    assert emu.insn == 589, f'0xc304: insn={emu.insn} ждём 589'


@t(0xB302, 'E2-b75: 0xb302() — длинный compute (7167 insn, ret=9): без '
           'периферийных/RAM-побочных эффектов в fresh-состоянии. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xB302)
    assert len(emu.periph_writes) == 0, \
        f'0xb302: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 9, \
        f'0xb302: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 9'
    assert emu.insn == 7167, f'0xb302: insn={emu.insn} ждём 7167'


@t(0x9A44, 'E2-b75: 0x9a44() — u16-цикл (394 insn, ret=0): u32[0xB4C]=0; затем '
           'u16[0xB5C]: 1→0 ×N (N≥7, контекстно-плавающее число циклов). '
           'fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x9A44)
    rw = [(a - RAM, s, v) for pc, a, s, v in getattr(emu, 'ram_writes', [])]
    assert (0xB4C, 4, 0) in rw, f'0x9a44: R={rw[:3]} ждём u32[0xB4C]=0'
    b5c = [w for w in rw if w[0] == 0xB5C]
    assert len(b5c) >= 14 and len(b5c) % 2 == 0, \
        f'0x9a44: len(u16[0xB5C])={len(b5c)} ждём ≥14 чётных'
    assert all(b5c[i][2] == 1 and b5c[i + 1][2] == 0
               for i in range(0, len(b5c), 2)), \
        f'0x9a44: u16[0xB5C]={b5c[:6]}... ждём 1→0×N'
    assert len(emu.periph_writes) == 0, \
        f'0x9a44: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x9a44: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 394, f'0x9a44: insn={emu.insn} ждём 394'


@t(0x90A0, 'E2-b75: 0x90a0() — u16-сброс (122 insn, ret=0): u16[0xB5C]: 1→0 '
           '(2 записи). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x90A0)
    rw = [(a - RAM, s, v) for pc, a, s, v in getattr(emu, 'ram_writes', [])]
    assert rw == [(0xB5C, 2, 1), (0xB5C, 2, 0)], \
        f'0x90a0: R={rw} ждём u16[0xB5C] 1→0'
    assert len(emu.periph_writes) == 0, \
        f'0x90a0: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x90a0: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 122, f'0x90a0: insn={emu.insn} ждём 122'


@t(0xA960, 'E2-b75: 0xa960() — короткий инициализатор (13 insn, ret=0, tail в '
           'unmapped): без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xA960)
    assert len(emu.periph_writes) == 0, \
        f'0xa960: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xa960: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 13, f'0xa960: insn={emu.insn} ждём 13'


@t(0xAA18, 'E2-b75: 0xaa18() — короткий инициализатор (13 insn, ret=0, tail в '
           'unmapped): без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xAA18)
    assert len(emu.periph_writes) == 0, \
        f'0xaa18: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xaa18: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 13, f'0xaa18: insn={emu.insn} ждём 13'


@t(0xB582, 'E2-b75: 0xb582() — инициализатор (22 insn, ret=0, tail в unmapped): '
           'без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xB582)
    assert len(emu.periph_writes) == 0, \
        f'0xb582: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xb582: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 22, f'0xb582: insn={emu.insn} ждём 22'


@t(0xB618, 'E2-b75: 0xb618() — инициализатор (30 insn, ret=0, tail в unmapped): '
           'без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xB618)
    assert len(emu.periph_writes) == 0, \
        f'0xb618: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xb618: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 30, f'0xb618: insn={emu.insn} ждём 30'


@t(0x6838, 'E2-b75: 0x6838() — инициализатор (71 insn, ret=0, tail в unmapped): '
           'без периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x6838)
    assert len(emu.periph_writes) == 0, \
        f'0x6838: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x6838: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 71, f'0x6838: insn={emu.insn} ждём 71'


@t(0x8434, 'E2-b75: 0x8434() — SPI-спин (insn>10000, ret=5): 0x40010828=0x10; '
           'SPI1_DR(0x4001300C): 0x5, затем 0xFF×N (N контекстно-плавающее, ≥100). '
           'fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x8434)
    assert emu.insn > 10000, f'0x8434: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40010828) == [0x10], \
        f"0x8434: 40010828={_pw(emu, 0x40010828)} ждём [0x10]"
    dr = _pw(emu, 0x4001300C)
    assert len(dr) >= 101 and dr[0] == 0x5 and all(v == 0xFF for v in dr[1:]), \
        f'0x8434: DR={dr[:4]}...(len={len(dr)}) ждём 5,FF×N'
    assert len(emu.periph_writes) == len(dr) + 1, \
        f'0x8434: P={len(emu.periph_writes)} ждём DR+1'
    assert uc.reg_read(UC_ARM_REG_R0) in (5, 7), \
        f'0x8434: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 5/7'
