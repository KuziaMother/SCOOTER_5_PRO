# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-b76: WWDG/AFIO-инит 0xc94c (26 записей, magic (CA,53,FF)×3/×4, AFIO-блок,
ret=1, 232 insn), WWDG-спины 0xca3c (0x2800=0x264) / 0xcd80 (0x2804=0x224),
RCC-ключ 0xced0 (0x40021018/1C=FF, ret=1, 29 insn), чистый 0xcee0 (573, ret=0),
SPI-циклы 0xc420 (DR 3,3,0,0×2 + FF, ret=0xFFFFFFFF) / 0xcf60 (DR 3,0,0,0 + FF,
ret=1) / 0xcfb8 (DR 3,2,0,0 + FF, ret=0) / 0xd240 (DR 3,3,0,0 + FF, ret=0),
короткие 0x6978/0x6e50/0x7a30 (ret=0), I2C-спин 0xacce (magic, ret=1)."""
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


def _dr_split(emu):
    """DR-записи: (не-FF префикс, количество FF-хвоста)."""
    dr = _pw(emu, 0x4001300C)
    i = 0
    while i < len(dr) and dr[i] != 0xFF:
        i += 1
    return dr[:i], len(dr) - i


@t(0xC94C, 'E2-b76: 0xc94c() — WWDG/AFIO-инит (232 insn, ret=1, 23/26 записей): '
           '0x40002824: (CA,53,FF)×3/×4; 0x40002808: F8→FC×2/3; 0x40002814=0; '
           '0x4000280C=0xFFFFFBFF; AFIO: 0x40010414=0x100000 ×2, 0x40010400/08: '
           'FFEFF FF→FF, 0x40010404/0C: FFEFFFFF. fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xC94C)
    pw = emu.periph_writes
    assert len(pw) in (23, 26), f'0xc94c: P={len(pw)} ждём 23/26'
    m = _pw(emu, 0x40002824)
    assert len(m) in (9, 12) and all(
        m[j:j+3] == [0xCA, 0x53, 0xFF] for j in range(0, len(m), 3)), \
        f"0xc94c: 40002824={m} ждём (CA,53,FF)×3/×4"
    c = _pw(emu, 0x40002808)
    assert len(c) in (3, 4) and c[0] == 0xFFFFFFF8 and \
        all(v == 0xFFFFFFFC for v in c[1:]), \
        f"0xc94c: 40002808={c} ждём F8→FC×2/3"
    assert _pw(emu, 0x40002814) == [0x0], \
        f"0xc94c: 40002814={_pw(emu, 0x40002814)} ждём [0]"
    assert _pw(emu, 0x4000280C) == [0xFFFFFBFF], \
        f"0xc94c: 4000280C={_pw(emu, 0x4000280C)} ждём [0xFFFFFBFF]"
    assert _pw(emu, 0x40010414) == [0x100000, 0x100000], \
        f"0xc94c: 40010414={_pw(emu, 0x40010414)} ждём 0x100000×2"
    assert _pw(emu, 0x40010400) == [0xFFEFFFFF, 0xFFFFFFFF], \
        f"0xc94c: 40010400={_pw(emu, 0x40010400)}"
    assert _pw(emu, 0x40010404) == [0xFFEFFFFF], \
        f"0xc94c: 40010404={_pw(emu, 0x40010404)}"
    assert _pw(emu, 0x40010408) == [0xFFEFFFFF, 0xFFFFFFFF], \
        f"0xc94c: 40010408={_pw(emu, 0x40010408)}"
    assert _pw(emu, 0x4001040C) == [0xFFEFFFFF], \
        f"0xc94c: 4001040C={_pw(emu, 0x4001040C)}"
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0xc94c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'
    assert emu.insn == 232, f'0xc94c: insn={emu.insn} ждём 232'


@t(0xCA3C, 'E2-b76: 0xca3c() — WWDG-спин (insn>10000, ret=0, 8 записей): '
           '0x40002824: CA→53→FF→CA→53; 0x40002800=0x264; '
           '0x4000280C: 0xFFFFFF7F→0xFFFFFF5F. fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xCA3C)
    assert emu.insn > 10000, f'0xca3c: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40002824) == [0xCA, 0x53, 0xFF, 0xCA, 0x53], \
        f"0xca3c: 40002824={_pw(emu, 0x40002824)} ждём CA,53,FF,CA,53"
    assert _pw(emu, 0x40002800) == [0x264], \
        f"0xca3c: 40002800={_pw(emu, 0x40002800)} ждём [0x264]"
    assert _pw(emu, 0x4000280C) == [0xFFFFFF7F, 0xFFFFFF5F], \
        f"0xca3c: 4000280C={_pw(emu, 0x4000280C)} ждём 7F→5F"
    assert len(emu.periph_writes) == 8, \
        f'0xca3c: P={len(emu.periph_writes)} ждём 8'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xca3c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'


@t(0xCD80, 'E2-b76: 0xcd80() — WWDG-спин (insn>10000, ret=0, 8 записей): '
           '0x40002824: CA→53→FF→CA→53; 0x40002804=0x224; '
           '0x4000280C: 0xFFFFFF7F→0xFFFFFF5F. fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xCD80)
    assert emu.insn > 10000, f'0xcd80: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40002824) == [0xCA, 0x53, 0xFF, 0xCA, 0x53], \
        f"0xcd80: 40002824={_pw(emu, 0x40002824)} ждём CA,53,FF,CA,53"
    assert _pw(emu, 0x40002804) == [0x224], \
        f"0xcd80: 40002804={_pw(emu, 0x40002804)} ждём [0x224]"
    assert _pw(emu, 0x4000280C) == [0xFFFFFF7F, 0xFFFFFF5F], \
        f"0xcd80: 4000280C={_pw(emu, 0x4000280C)} ждём 7F→5F"
    assert len(emu.periph_writes) == 8, \
        f'0xcd80: P={len(emu.periph_writes)} ждём 8'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xcd80: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'


@t(0xCEE0, 'E2-b76: 0xcee0() — чистый инициализатор (573 insn, ret=0): без '
           'периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xCEE0)
    assert len(emu.periph_writes) == 0, \
        f'0xcee0: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xcee0: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 573, f'0xcee0: insn={emu.insn} ждём 573'


@t(0xC420, 'E2-b76: 0xc420() — SPI-цикл ×2 (7914 insn, ret=0xFFFFFFFF): '
           '0x40010828=0x10 ×2, 0x40010818=0x10 ×2; SPI1_DR: 0x3,0x3,0,0 + '
           '0xFF×N (N≥4) ×2 блока. fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xC420)
    assert emu.insn > 1000, f'0xc420: insn={emu.insn} ждём >1000'
    d28 = _pw(emu, 0x40010828)
    assert len(d28) in (1, 2) and all(v == 0x10 for v in d28), \
        f"0xc420: 40010828={d28} ждём [0x10]×1/2"
    d18 = _pw(emu, 0x40010818)
    assert len(d18) in (1, 2) and all(v == 0x10 for v in d18), \
        f"0xc420: 40010818={d18} ждём [0x10]×1/2"
    dr = _pw(emu, 0x4001300C)
    nonff = [v for v in dr if v != 0xFF]
    assert nonff and len(nonff) % 4 == 0 and \
        all(nonff[k:k+4] == [3, 3, 0, 0] for k in range(0, len(nonff), 4)) and \
        len(dr) > len(nonff), \
        f'0xc420: DR={dr[:10]}...(len={len(dr)}) ждём (3,3,0,0)+FF×N ×1/2 блока'
    assert uc.reg_read(UC_ARM_REG_R0) == 0xFFFFFFFF, \
        f'0xc420: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0xFFFFFFFF'


@t(0xCF60, 'E2-b76: 0xcf60() — SPI-цикл (5344 insn, ret=1): 0x40010828=0x10, '
           '0x40010818=0x10; SPI1_DR: 0x3,0,0,0 + 0xFF×N (N≥4). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xCF60)
    assert emu.insn > 1000, f'0xcf60: insn={emu.insn} ждём >1000'
    assert _pw(emu, 0x40010828) == [0x10], \
        f"0xcf60: 40010828={_pw(emu, 0x40010828)} ждём [0x10]"
    assert _pw(emu, 0x40010818) == [0x10], \
        f"0xcf60: 40010818={_pw(emu, 0x40010818)} ждём [0x10]"
    dr = _pw(emu, 0x4001300C)
    pref = [3, 0, 0, 0]
    assert dr[:len(pref)] == pref and dr[len(pref):] and \
        all(v == 0xFF for v in dr[len(pref):]), \
        f'0xcf60: DR={dr[:8]}...(len={len(dr)}) ждём 3,0,0,0+FF×N'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0xcf60: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'


@t(0xCFB8, 'E2-b76: 0xcfb8() — SPI-цикл (2394 insn, ret=0): 0x40010828=0x10, '
           '0x40010818=0x10; SPI1_DR: 0x3,0x2,0,0 + 0xFF×N (N≥4). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xCFB8)
    assert emu.insn > 1000, f'0xcfb8: insn={emu.insn} ждём >1000'
    assert _pw(emu, 0x40010828) == [0x10], \
        f"0xcfb8: 40010828={_pw(emu, 0x40010828)} ждём [0x10]"
    assert _pw(emu, 0x40010818) == [0x10], \
        f"0xcfb8: 40010818={_pw(emu, 0x40010818)} ждём [0x10]"
    dr = _pw(emu, 0x4001300C)
    pref = [3, 2, 0, 0]
    assert dr[:len(pref)] == pref and dr[len(pref):] and \
        all(v == 0xFF for v in dr[len(pref):]), \
        f'0xcfb8: DR={dr[:8]}...(len={len(dr)}) ждём 3,2,0,0+FF×N'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xcfb8: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'


@t(0xD240, 'E2-b76: 0xd240() — SPI-цикл (1418 insn, ret=0): 0x40010828=0x10, '
           '0x40010818=0x10; SPI1_DR: 0x3,0x3,0,0 + 0xFF×N (N≥4). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xD240)
    assert emu.insn > 1000, f'0xd240: insn={emu.insn} ждём >1000'
    assert _pw(emu, 0x40010828) == [0x10], \
        f"0xd240: 40010828={_pw(emu, 0x40010828)} ждём [0x10]"
    assert _pw(emu, 0x40010818) == [0x10], \
        f"0xd240: 40010818={_pw(emu, 0x40010818)} ждём [0x10]"
    dr = _pw(emu, 0x4001300C)
    pref = [3, 3, 0, 0]
    assert dr[:len(pref)] == pref and dr[len(pref):] and \
        all(v == 0xFF for v in dr[len(pref):]), \
        f'0xd240: DR={dr[:8]}...(len={len(dr)}) ждём 3,3,0,0+FF×N'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0xd240: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'


@t(0x6978, 'E2-b76: 0x6978() — короткий инициализатор (43 insn, ret=0, tail в '
           'unmapped): без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x6978)
    assert len(emu.periph_writes) == 0, \
        f'0x6978: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x6978: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 43, f'0x6978: insn={emu.insn} ждём 43'


@t(0x6E50, 'E2-b76: 0x6e50() — инициализатор (90 insn, ret=0, tail в unmapped): '
           'без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x6E50)
    assert len(emu.periph_writes) == 0, \
        f'0x6e50: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x6e50: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 90, f'0x6e50: insn={emu.insn} ждём 90'


@t(0x7A30, 'E2-b76: 0x7a30() — инициализатор (89 insn, ret=0, tail в unmapped): '
           'без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x7A30)
    assert len(emu.periph_writes) == 0, \
        f'0x7a30: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x7a30: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 89, f'0x7a30: insn={emu.insn} ждём 89'


@t(0xACCE, 'E2-b76: 0xacce() — I2C-спин (insn>10000, ret=1): 0x40022004: '
           '0x45670123→0xCDEF89AB; 0x4002200C=0xFFFFFFFF (3 записи). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xACCE)
    assert emu.insn > 10000, f'0xacce: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40022004) == [0x45670123, 0xCDEF89AB], \
        f"0xacce: 40022004={_pw(emu, 0x40022004)} ждём magic"
    assert _pw(emu, 0x4002200C) == [0xFFFFFFFF], \
        f"0xacce: 4002200C={_pw(emu, 0x4002200C)} ждём FF"
    assert len(emu.periph_writes) == 3, \
        f'0xacce: P={len(emu.periph_writes)} ждём 3'
    assert uc.reg_read(UC_ARM_REG_R0) in (1, 6), \
        f'0xacce: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1/6'


@t(0xced0, 'E2-b76: 0xced0() — RCC-ключ (29 insn, ret=1): 0x4002101C=0xFFFFFFFF, '
           '0x40021018=0xFFFFFFFF (2 записи). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0xced0)
    assert _pw(emu, 0x4002101C) == [0xFFFFFFFF], \
        f"0xced0: 4002101C={_pw(emu, 0x4002101C)} ждём FF"
    assert _pw(emu, 0x40021018) == [0xFFFFFFFF], \
        f"0xced0: 40021018={_pw(emu, 0x40021018)} ждём FF"
    assert len(emu.periph_writes) == 2, \
        f'0xced0: P={len(emu.periph_writes)} ждём 2'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0xced0: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'
    assert emu.insn == 29, f'0xced0: insn={emu.insn} ждём 29'
