# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-b79: короткие 0x119c4 (100 insn) / 0x119e4 (19) / 0x13148 (160) (ret=0);
флаг-кейсы 0x11de8 (flag byte[0x2000002E]: 91 insn ret=0 / 0x5bc4-инит 678 insn
ret=0x4621463A) и 0x12a78 (flag byte[0x20000B5B]: 164 insn ret=1 + 4 byte-записи
/ 709 insn ret=0x10 + u16[0xB5C] 1→0); u16-сброс 0x128e4 (632 insn, ret=0x10);
чистый 0x12aec (591 insn, ret=0x10); константы 0x12b50 (49 insn, ret=0x4621463A) /
0x12d90 (49 insn, ret=0x35F525FF); флаг-кейс 0x129b4 (fresh: ~2495 insn ret=1
+ 12 R-записей / flag byte[0x20000B58]=1: ~4324 insn ret=2, 0x40003000=0xAAAA,
36 R-записей); SPI-цикл 0x1330c (4379 insn, ret=0xFF, DR: (3,5,*,0,FF×N)×2);
clock/RCC-спин 0x11cb4 (20 записей: 0x40021004/00/08/24/2C/30/34/40, 0x40001820,
0x40022000, 0x40007000, ret=0x40007000); чистый спин 0x11c5e (ret=2)."""
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


def _ramw(emu):
    """RAM-записи как [(off_RAM, size, value), ...]."""
    return [(a - RAM, s, v) for pc, a, s, v in getattr(emu, 'ram_writes', [])]


@t(0x119C4, 'E2-b79: 0x119c4() — короткий инициализатор (100 insn, ret=0, tail в '
            'unmapped): без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x119C4)
    assert len(emu.periph_writes) == 0, \
        f'0x119c4: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x119c4: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 100, f'0x119c4: insn={emu.insn} ждём 100'


@t(0x119E4, 'E2-b79: 0x119e4() — короткий инициализатор (19 insn, ret=0, tail в '
            'unmapped): без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x119E4)
    assert len(emu.periph_writes) == 0, \
        f'0x119e4: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x119e4: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 19, f'0x119e4: insn={emu.insn} ждём 19'


@t(0x13148, 'E2-b79: 0x13148() — инициализатор (160 insn, ret=0, tail в unmapped): '
            'без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x13148)
    assert len(emu.periph_writes) == 0, \
        f'0x13148: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x13148: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 160, f'0x13148: insn={emu.insn} ждём 160'


@t(0x11DE8, 'E2-b79: 0x11de8() — флаг-кейс (флаг byte[0x2000002E]): fresh → 91 insn '
            'ret=0 без записей; flag=1 → 0x5bc4-инит (678 insn, ret=0x4621463A, 29 P, '
            'byte[0xA64]=0, byte[0xB82]=0). 2 кейса.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x11DE8)
    assert len(emu.periph_writes) == 0, \
        f'0x11de8 fresh: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x11de8 fresh: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 91, f'0x11de8 fresh: insn={emu.insn} ждём 91'
    uc, emu, lp = _fresh_probe(0x11DE8, seeds=[(0x2000002E, 1)])
    assert len(emu.periph_writes) == 29, \
        f'0x11de8 flag=1: P={len(emu.periph_writes)} ждём 29'
    assert _p(uc, 0x4002102C) == 0xFFFFFE02, \
        f"0x11de8 flag=1: 4002102C={_p(uc, 0x4002102C):#x} ждём 0xFFFFFE02"
    assert _p(uc, 0x40020004) == 0xFFFFFFFF, \
        f"0x11de8 flag=1: 40020004={_p(uc, 0x40020004):#x} ждём FF"
    assert _p(uc, 0x40010818) == 0x10 and _p(uc, 0x40010828) == 0x10, \
        f"0x11de8 flag=1: GPIOB={_p(uc, 0x40010818):#x}/{_p(uc, 0x40010828):#x}"
    assert _p(uc, 0x40013000, 2) == 0xFFBF, \
        f"0x11de8 flag=1: SPI1_CTLR={_p(uc, 0x40013000, 2):#x} ждём 0xFFBF"
    assert _p(uc, 0x4001300C, 2) == 0xB9, \
        f"0x11de8 flag=1: SPI1_DR={_p(uc, 0x4001300C, 2):#x} ждём 0xB9"
    rw = _ramw(emu)
    assert (0xA64, 1, 0) in rw and (0xB82, 1, 0) in rw, \
        f'0x11de8 flag=1: R={rw[:4]} ждём 0xA64/0xB82'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x4621463A, \
        f'0x11de8 flag=1: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x4621463A'
    assert emu.insn == 678, f'0x11de8 flag=1: insn={emu.insn} ждём 678'


@t(0x128E4, 'E2-b79: 0x128e4() — u16-сброс (632 insn, ret=0x10): u16[0xB5C]: 1→0 '
            '(2 записи). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x128E4)
    rw = _ramw(emu)
    assert rw == [(0xB5C, 2, 1), (0xB5C, 2, 0)], \
        f'0x128e4: R={rw} ждём u16[0xB5C] 1→0'
    assert len(emu.periph_writes) == 0, \
        f'0x128e4: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x10, \
        f'0x128e4: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x10'
    assert emu.insn == 632, f'0x128e4: insn={emu.insn} ждём 632'


@t(0x12A78, 'E2-b79: 0x12a78() — флаг-кейс (флаг byte[0x20000B5B]): fresh → 164 insn '
            'ret=1, u16[0xB5C] 1→0 + byte[0xB73]=0 + byte[0xB5B]=1 (4 записи); '
            'flag=1 → 709 insn ret=0x10, u16[0xB5C] 1→0 (2 записи). 2 кейса.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x12A78)
    rw = _ramw(emu)
    assert rw == [(0xB5C, 2, 1), (0xB5C, 2, 0),
                  (0xB73, 1, 0), (0xB5B, 1, 1)], \
        f'0x12a78 fresh: R={rw} ждём последовательность'
    assert len(emu.periph_writes) == 0, \
        f'0x12a78 fresh: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x12a78 fresh: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'
    assert emu.insn == 164, f'0x12a78 fresh: insn={emu.insn} ждём 164'
    uc, emu, lp = _fresh_probe(0x12A78, seeds=[(0x20000B5B, 1)])
    rw = _ramw(emu)
    assert rw == [(0xB5C, 2, 1), (0xB5C, 2, 0)], \
        f'0x12a78 flag=1: R={rw} ждём u16[0xB5C] 1→0'
    assert len(emu.periph_writes) == 0, \
        f'0x12a78 flag=1: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x10, \
        f'0x12a78 flag=1: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x10'
    assert emu.insn == 709, f'0x12a78 flag=1: insn={emu.insn} ждём 709'


@t(0x12AEC, 'E2-b79: 0x12aec() — чистый инициализатор (591 insn, ret=0x10): без '
            'периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x12AEC)
    assert len(emu.periph_writes) == 0, \
        f'0x12aec: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x10, \
        f'0x12aec: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x10'
    assert emu.insn == 591, f'0x12aec: insn={emu.insn} ждём 591'


@t(0x12B50, 'E2-b79: 0x12b50() — константный возвращаемый (49 insn, ret=0x4621463A, '
            'tail в unmapped): без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x12B50)
    assert len(emu.periph_writes) == 0, \
        f'0x12b50: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x4621463A, \
        f'0x12b50: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x4621463A'
    assert emu.insn == 49, f'0x12b50: insn={emu.insn} ждём 49'


@t(0x12D90, 'E2-b79: 0x12d90() — константный возвращаемый (49 insn, ret=0x35F525FF, '
            'tail в unmapped): без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x12D90)
    assert len(emu.periph_writes) == 0, \
        f'0x12d90: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x35F525FF, \
        f'0x12d90: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x35F525FF'
    assert emu.insn == 49, f'0x12d90: insn={emu.insn} ждём 49'


@t(0x129B4, 'E2-b79: 0x129b4() — флаг-кейс (флаг byte[0x20000B58]): fresh → ~2495 insn '
            'ret=1, 12 R-записей (u16[0xB5C] 1→0, byte[0xA51]=1, zero-блок); '
            'flag=1 → ~4324 insn ret=2, 0x40003000=0xAAAA, 36 R-записей. insn плавающие.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x129B4)
    assert 2000 < emu.insn < 3000, \
        f'0x129b4 fresh: insn={emu.insn} ждём ~2495'
    rw = _ramw(emu)
    assert (0xB5C, 2, 1) in rw and (0xB5C, 2, 0) in rw, \
        f'0x129b4 fresh: R={rw[:4]} ждём u16[0xB5C] 1→0'
    assert (0xA51, 1, 1) in rw, f'0x129b4 fresh: R={rw} ждём byte[0xA51]=1'
    assert len(rw) == 12, f'0x129b4 fresh: R={len(rw)} ждём 12'
    assert len(emu.periph_writes) == 0, \
        f'0x129b4 fresh: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x129b4 fresh: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'
    uc, emu, lp = _fresh_probe(0x129B4, seeds=[(0x20000B58, 1)])
    assert 4000 < emu.insn < 5000, \
        f'0x129b4 flag=1: insn={emu.insn} ждём ~4324'
    assert _pw(emu, 0x40003000) == [0xAAAA], \
        f"0x129b4 flag=1: 40003000={_pw(emu, 0x40003000)} ждём [0xAAAA]"
    assert len(emu.periph_writes) == 1, \
        f'0x129b4 flag=1: P={len(emu.periph_writes)} ждём 1'
    rw = _ramw(emu)
    assert (0xA51, 1, 1) in rw and len(rw) == 36, \
        f'0x129b4 flag=1: R={len(rw)} ждём 36 (с 0xA51=1)'
    assert uc.reg_read(UC_ARM_REG_R0) == 2, \
        f'0x129b4 flag=1: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 2'


@t(0x1330C, 'E2-b79: 0x1330c() — SPI-цикл ×2 (4379 insn, ret=0xFF/0x40013000, 28 записей): '
            '0x40010828=0x10 ×2, 0x40010818=0x10; SPI1_DR: (3,5,0,0)+FF×N и '
            '(3,5,0x10,0)+FF×N+0x10. fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x1330C)
    assert emu.insn > 1000, f'0x1330c: insn={emu.insn} ждём >1000'
    assert len(_pw(emu, 0x40010828)) in (1, 2) and \
        all(v == 0x10 for v in _pw(emu, 0x40010828)), \
        f"0x1330c: 40010828={_pw(emu, 0x40010828)} ждём 0x10×1/2"
    assert len(_pw(emu, 0x40010818)) in (1, 2) and \
        all(v == 0x10 for v in _pw(emu, 0x40010818)), \
        f"0x1330c: 40010818={_pw(emu, 0x40010818)} ждём 0x10×1/2"
    dr = _pw(emu, 0x4001300C)
    nonff = [v for v in dr if v != 0xFF]
    assert len(dr) >= 20 and nonff[:2] == [3, 5] and \
        all(v in (3, 5, 0, 0x10) for v in nonff) and \
        nonff.count(3) >= 2 and nonff.count(5) >= 2, \
        f'0x1330c: DR={dr[:12]}...(len={len(dr)}) ждём 2 блока 3,5,...'
    ret = uc.reg_read(UC_ARM_REG_R0)
    assert ret in (0xFF, 0x40013000), \
        f'0x1330c: ret={ret:#x} ждём 0xFF/0x40013000'


@t(0x11CB4, 'E2-b79: 0x11cb4() — clock/RCC-спин (insn>10000, ret=0/0x40007000 по фазе спина): '
            'стабильный блок: 0x40021024=FF; 0x40021004: F8FFC000→C000; 0x40021000: FEF6FFFF→'
            'FEF2FFFF...; 0x4002102C=0; 0x40021030=0x3800; 0x40021034=0; 0x40021040=0; '
            '0x40021008=0x4BF8000; 0x4002101C=FF; 0x40001820: FDFFFFFF→FF ×N; хвост: '
            '0x40022000: FF→маски, 0x40007000: маски (плавающий). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x11CB4)
    assert emu.insn > 10000, f'0x11cb4: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40021024) == [0xFFFFFFFF], \
        f"0x11cb4: 40021024={_pw(emu, 0x40021024)}"
    assert _pw(emu, 0x40021004) == [0xF8FFC000, 0xC000], \
        f"0x11cb4: 40021004={_pw(emu, 0x40021004)}"
    w00 = _pw(emu, 0x40021000)
    assert w00[:2] == [0xFEF6FFFF, 0xFEF2FFFF] and all(v in (0xFEF2FFFF, 0xFEF6FFFF) for v in w00), \
        f"0x11cb4: 40021000={w00} ждём FEF6→FEF2..."
    assert _pw(emu, 0x4002102C) == [0x0], \
        f"0x11cb4: 4002102C={_pw(emu, 0x4002102C)}"
    assert _pw(emu, 0x40021030) == [0x3800], \
        f"0x11cb4: 40021030={_pw(emu, 0x40021030)}"
    assert _pw(emu, 0x40021034) == [0x0], \
        f"0x11cb4: 40021034={_pw(emu, 0x40021034)}"
    assert _pw(emu, 0x40021040) == [0x0], \
        f"0x11cb4: 40021040={_pw(emu, 0x40021040)}"
    assert _pw(emu, 0x40021008) == [0x4BF8000], \
        f"0x11cb4: 40021008={_pw(emu, 0x40021008)}"
    assert _pw(emu, 0x4002101C) == [0xFFFFFFFF], \
        f"0x11cb4: 4002101C={_pw(emu, 0x4002101C)}"
    w18 = _pw(emu, 0x40001820)
    assert w18[:4] == [0xFDFFFFFF, 0xFFFFFFFF, 0xFDFFFFFF, 0xFFFFFFFF] and \
        all(v in (0xFDFFFFFF, 0xFFFFFFFF) for v in w18), \
        f"0x11cb4: 40001820={w18} ждём FDFFFFFF→FF ×N"
    w20 = _pw(emu, 0x40022000)
    assert w20 and w20[0] == 0xFFFFFFFF and \
        all(v in (0xFFFFFDCF, 0xFFFFF9FF, 0xFFFFFDFF) for v in w20[1:]), \
        f"0x11cb4: 40022000={w20} ждём FF→маски"
    w08 = _pw(emu, 0x40007000)
    assert w08 and w08[0] == 0xFFFFF9FF and \
        all(v in (0xFFFFF9FF, 0xFFFFFDFF, 0xFFFFFFDF) for v in w08[1:]), \
        f"0x11cb4: 40007000={w08} ждём маски"
    ret = uc.reg_read(UC_ARM_REG_R0)
    assert ret in (0, 0x40007000), \
        f'0x11cb4: ret={ret:#x} ждём 0/0x40007000 (фаза спина)'


@t(0x11C5E, 'E2-b79: 0x11c5e() — спин (insn>=50000, ret=0/2 по фазе спина): без стабильных '
            'побочных эффектов (опц. 1 запись 0x40005800=0xFFFF до лимита). smoke+spin golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x11C5E)
    assert emu.insn >= 50000, f'0x11c5e: insn={emu.insn} ждём спин (>=50000)'
    assert len(emu.periph_writes) in (0, 1), \
        f'0x11c5e: P={len(emu.periph_writes)} ждём 0/1 (фаза спина)'
    for pc, a, s, v in emu.periph_writes:
        assert (a, s, v) == (0x40005800, 2, 0xFFFF), \
            f'0x11c5e: P={[(hex(x), y, hex(z)) for _, x, y, z in emu.periph_writes]}'
    assert uc.reg_read(UC_ARM_REG_R0) in (0, 2), \
        f'0x11c5e: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0/2 (фаза спина)'
