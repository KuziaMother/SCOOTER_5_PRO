# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-b73: overlap-checker битовых масок 0x12aa (clz+orr, ret=0, без записей),
byte-zero-хвост 0x1fe0 (byte[0xA77..0xA79]=0, ret=0), чистые инициализаторы
0x3f00 (ret=1) / 0x70d8 (ret=0), u16-счётчик 0x4cbc (u32[0xB50]=1, u16[0xB5C]:
1→0), константные возвращаемые 0x69e4 (0x98001053) / 0x6ccc (-2) / 0x8938
(0x1611F0, 2248 insn), GPIOB+SPI1-инициалы 0x84fc (DR=0x6, ret=GPIOB-base) /
0x83e4 (DR: 0x9F→FF×3, ret=0xFFFFFF), WWDG-спины 0x3740 (0x2804=0) / 0x5448
(0x2804=0x480000, twin), SPI-спин 0x3780 (DR: 0x6, 0x5, 0xFF×N, N плавающий)."""
import struct

from fv_core import *  # noqa: F401,F403

from unicorn import UcError, UC_HOOK_CODE  # noqa: E402
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,  # noqa: E402
                               UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_LR)


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
    regs = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)
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


@t(0x12AA, 'E2-b73: 0x12aa(len, alt, mask1, mask2) — overlap-checker битовых масок: '
           'clz(alt|len)+0x20 → bl 0x14e8; orr r0, sl; orr r1, fp; (m1&m2)==0 → 0x1302; '
           '(m1|m2)==0 → 0x1316. В fresh-состоянии обе ветки сходятся: ret=0, '
           '69-72 insn, без периферийных/RAM-записей. 4 комбинации масок.')
def _(run, rng):
    """Emulator test @ 0x12aa: E2-b73: 0x12aa(len, alt, mask1, mask2) — overlap-checker битовых масок: clz(alt|len)+0x20 → bl 0x14e8; orr r0, sl; orr r1, fp; (m1&m2)==0 → 0x1302; (m1|m2)==0 → 0x1316. В fresh-состоянии обе ветки сходятся: ret=0, 69-72 insn, без периферийных/RAM-записей. 4 комбинации масок..
    Тест эмулятора @ 0x12aa: E2-b73: 0x12aa(len, alt, mask1, mask2) — overlap-checker битовых масок: clz(alt|len)+0x20 → bl 0x14e8; orr r0, sl; orr r1, fp; (m1&m2)==0 → 0x1302; (m1|m2)==0 → 0x1316. В fresh-состоянии обе ветки сходятся: ret=0, 69-72 insn, без периферийных/RAM-записей. 4 комбинации масок..
    """
    for r0, r1, r2, r3 in ((0x10, 0, 0x0F, 0x03), (0x10, 0, 0x0F, 0x30),
                           (0x01, 0, 0x03, 0x01), (0x40, 0x0F, 0x30, 0x0C)):
        uc, emu, lp = _fresh_probe(0x12AA, args=(r0, r1, r2, r3))
        assert uc.reg_read(UC_ARM_REG_R0) == 0, \
            f'0x12aa({r0:#x},{r1:#x},{r2:#x},{r3:#x}): ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
        assert 69 <= emu.insn <= 72, \
            f'0x12aa({r0:#x},{r1:#x},{r2:#x},{r3:#x}): insn={emu.insn} ждём 69..72'
        assert len(emu.periph_writes) == 0, \
            f'0x12aa: P={len(emu.periph_writes)} ждём 0'


@t(0x1FE0, 'E2-b73: 0x1fe0() — byte-zero-хвост (24 insn, ret=0): byte[0xA79]=0, '
           'byte[0xA78]=0, byte[0xA77]=0 (3 записи). fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x1fe0: E2-b73: 0x1fe0() — byte-zero-хвост (24 insn, ret=0): byte[0xA79]=0, byte[0xA78]=0, byte[0xA77]=0 (3 записи). fresh-emu golden..
    Тест эмулятора @ 0x1fe0: E2-b73: 0x1fe0() — byte-zero-хвост (24 insn, ret=0): byte[0xA79]=0, byte[0xA78]=0, byte[0xA77]=0 (3 записи). fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x1FE0)
    rw = [(a - RAM, s, v) for pc, a, s, v in getattr(emu, 'ram_writes', [])]
    assert (0xA79, 1, 0) in rw and (0xA78, 1, 0) in rw and (0xA77, 1, 0) in rw, \
        f'0x1fe0: R={rw} ждём zero 0xA77/0xA78/0xA79'
    assert len(rw) == 3, f'0x1fe0: R={len(rw)} ждём 3'
    assert len(emu.periph_writes) == 0, \
        f'0x1fe0: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x1fe0: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 24, f'0x1fe0: insn={emu.insn} ждём 24'


@t(0x3F00, 'E2-b73: 0x3f00() — чистый инициализатор (282 insn, ret=1, tail в '
           'unmapped): без периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x3f00: E2-b73: 0x3f00() — чистый инициализатор (282 insn, ret=1, tail в unmapped): без периферийных/RAM-побочных эффектов. smoke+ret+insn golden..
    Тест эмулятора @ 0x3f00: E2-b73: 0x3f00() — чистый инициализатор (282 insn, ret=1, tail в unmapped): без периферийных/RAM-побочных эффектов. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x3F00)
    assert len(emu.periph_writes) == 0, \
        f'0x3f00: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x3f00: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'
    assert emu.insn == 282, f'0x3f00: insn={emu.insn} ждём 282'


@t(0x4CBC, 'E2-b73: 0x4cbc() — u16-счётчик (87 insn, ret=0): u32[0xB50]=1, '
           'u16[0xB5C]: 1→0 (2 записи). fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x4cbc: E2-b73: 0x4cbc() — u16-счётчик (87 insn, ret=0): u32[0xB50]=1, u16[0xB5C]: 1→0 (2 записи). fresh-emu golden..
    Тест эмулятора @ 0x4cbc: E2-b73: 0x4cbc() — u16-счётчик (87 insn, ret=0): u32[0xB50]=1, u16[0xB5C]: 1→0 (2 записи). fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x4CBC)
    rw = [(a - RAM, s, v) for pc, a, s, v in getattr(emu, 'ram_writes', [])]
    assert (0xB50, 4, 1) in rw, f'0x4cbc: R={rw} ждём u32[0xB50]=1'
    s16 = [w for w in rw if w[0] == 0xB5C]
    assert len(s16) == 2 and s16[0][2] == 1 and s16[1][2] == 0, \
        f'0x4cbc: u16[0xB5C]={s16} ждём 1→0'
    assert len(emu.periph_writes) == 0, \
        f'0x4cbc: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x4cbc: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 87, f'0x4cbc: insn={emu.insn} ждём 87'


@t(0x69E4, 'E2-b73: 0x69e4() — константный возвращаемый (217 insn, ret=0x98001053): '
           'без периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x69e4: E2-b73: 0x69e4() — константный возвращаемый (217 insn, ret=0x98001053): без периферийных/RAM-побочных эффектов. smoke+ret+insn golden..
    Тест эмулятора @ 0x69e4: E2-b73: 0x69e4() — константный возвращаемый (217 insn, ret=0x98001053): без периферийных/RAM-побочных эффектов. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x69E4)
    assert len(emu.periph_writes) == 0, \
        f'0x69e4: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x98001053, \
        f'0x69e4: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x98001053'
    assert emu.insn == 217, f'0x69e4: insn={emu.insn} ждём 217'


@t(0x6CCC, 'E2-b73: 0x6ccc() — константный возвращаемый (44 insn, ret=0xFFFFFFFE=-2): '
           'без периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x6ccc: E2-b73: 0x6ccc() — константный возвращаемый (44 insn, ret=0xFFFFFFFE=-2): без периферийных/RAM-побочных эффектов. smoke+ret+insn golden..
    Тест эмулятора @ 0x6ccc: E2-b73: 0x6ccc() — константный возвращаемый (44 insn, ret=0xFFFFFFFE=-2): без периферийных/RAM-побочных эффектов. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x6CCC)
    assert len(emu.periph_writes) == 0, \
        f'0x6ccc: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0xFFFFFFFE, \
        f'0x6ccc: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0xFFFFFFFE'
    assert emu.insn == 44, f'0x6ccc: insn={emu.insn} ждём 44'


@t(0x70D8, 'E2-b73: 0x70d8() — чистый инициализатор (278 insn, ret=0, tail в '
           'unmapped): без периферийных/RAM-побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x70d8: E2-b73: 0x70d8() — чистый инициализатор (278 insn, ret=0, tail в unmapped): без периферийных/RAM-побочных эффектов. smoke+ret+insn golden..
    Тест эмулятора @ 0x70d8: E2-b73: 0x70d8() — чистый инициализатор (278 insn, ret=0, tail в unmapped): без периферийных/RAM-побочных эффектов. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x70D8)
    assert len(emu.periph_writes) == 0, \
        f'0x70d8: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x70d8: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 278, f'0x70d8: insn={emu.insn} ждём 278'


@t(0x84FC, 'E2-b73: 0x84fc() — GPIOB+SPI1-инициал (118 insn, ret=0x40010800 — база '
           'GPIOB): 0x40010828=0x10, SPI1_DR(0x4001300C)=0x6, 0x40010818=0x10 '
           '(3 записи). fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x84fc: E2-b73: 0x84fc() — GPIOB+SPI1-инициал (118 insn, ret=0x40010800 — база GPIOB): 0x40010828=0x10, SPI1_DR(0x4001300C)=0x6, 0x40010818=0x10 (3 записи). fresh-emu golden..
    Тест эмулятора @ 0x84fc: E2-b73: 0x84fc() — GPIOB+SPI1-инициал (118 insn, ret=0x40010800 — база GPIOB): 0x40010828=0x10, SPI1_DR(0x4001300C)=0x6, 0x40010818=0x10 (3 записи). fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x84FC)
    assert _pw(emu, 0x40010828) == [0x10], \
        f"0x84fc: 40010828={_pw(emu, 0x40010828)} ждём [0x10]"
    assert _pw(emu, 0x4001300C) == [0x6], \
        f"0x84fc: SPI1_DR={_pw(emu, 0x4001300C)} ждём [0x6]"
    assert _pw(emu, 0x40010818) == [0x10], \
        f"0x84fc: 40010818={_pw(emu, 0x40010818)} ждём [0x10]"
    assert len(emu.periph_writes) == 3, \
        f'0x84fc: P={len(emu.periph_writes)} ждём 3'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x40010800, \
        f'0x84fc: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x40010800'
    assert emu.insn == 118, f'0x84fc: insn={emu.insn} ждём 118'


@t(0x83E4, 'E2-b73: 0x83e4() — GPIOB+SPI1-инициал (447 insn, ret=0xFFFFFF): '
           '0x40010828=0x10, SPI1_DR: 0x9F→0xFF×3, 0x40010818=0x10 (6 записей). '
           'fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x83e4: E2-b73: 0x83e4() — GPIOB+SPI1-инициал (447 insn, ret=0xFFFFFF): 0x40010828=0x10, SPI1_DR: 0x9F→0xFF×3, 0x40010818=0x10 (6 записей). fresh-emu golden..
    Тест эмулятора @ 0x83e4: E2-b73: 0x83e4() — GPIOB+SPI1-инициал (447 insn, ret=0xFFFFFF): 0x40010828=0x10, SPI1_DR: 0x9F→0xFF×3, 0x40010818=0x10 (6 записей). fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x83E4)
    assert _pw(emu, 0x40010828) == [0x10], \
        f"0x83e4: 40010828={_pw(emu, 0x40010828)} ждём [0x10]"
    assert _pw(emu, 0x4001300C) == [0x9F, 0xFF, 0xFF, 0xFF], \
        f"0x83e4: SPI1_DR={_pw(emu, 0x4001300C)} ждём 9F→FF×3"
    assert _pw(emu, 0x40010818) == [0x10], \
        f"0x83e4: 40010818={_pw(emu, 0x40010818)} ждём [0x10]"
    assert len(emu.periph_writes) == 6, \
        f'0x83e4: P={len(emu.periph_writes)} ждём 6'
    assert uc.reg_read(UC_ARM_REG_R0) == 0xFFFFFF, \
        f'0x83e4: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0xFFFFFF'
    assert emu.insn == 447, f'0x83e4: insn={emu.insn} ждём 447'


@t(0x3740, 'E2-b73: 0x3740() — WWDG-спин (insn>10000, ret=0): 0x40002824: CA→53→FF→CA→53; '
           '0x40002804=0x0; 0x4000280C: 0xFFFFFF7F→0xFFFFFF5F (8 записей). '
           'fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x3740: E2-b73: 0x3740() — WWDG-спин (insn>10000, ret=0): 0x40002824: CA→53→FF→CA→53; 0x40002804=0x0; 0x4000280C: 0xFFFFFF7F→0xFFFFFF5F (8 записей). fresh-emu golden..
    Тест эмулятора @ 0x3740: E2-b73: 0x3740() — WWDG-спин (insn>10000, ret=0): 0x40002824: CA→53→FF→CA→53; 0x40002804=0x0; 0x4000280C: 0xFFFFFF7F→0xFFFFFF5F (8 записей). fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x3740)
    assert emu.insn > 10000, f'0x3740: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40002824) == [0xCA, 0x53, 0xFF, 0xCA, 0x53], \
        f"0x3740: 40002824={_pw(emu, 0x40002824)} ждём CA,53,FF,CA,53"
    assert _pw(emu, 0x40002804) == [0x0], \
        f"0x3740: 40002804={_pw(emu, 0x40002804)} ждём [0]"
    assert _pw(emu, 0x4000280C) == [0xFFFFFF7F, 0xFFFFFF5F], \
        f"0x3740: 4000280C={_pw(emu, 0x4000280C)} ждём 7F→5F"
    assert len(emu.periph_writes) == 8, \
        f'0x3740: P={len(emu.periph_writes)} ждём 8'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x3740: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'


@t(0x5448, 'E2-b73: 0x5448() — WWDG-спин twin 0x3740 (insn>10000, ret=0): те же 8 '
           'записей, но 0x40002804=0x480000 (не 0). fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x5448: E2-b73: 0x5448() — WWDG-спин twin 0x3740 (insn>10000, ret=0): те же 8 записей, но 0x40002804=0x480000 (не 0). fresh-emu golden..
    Тест эмулятора @ 0x5448: E2-b73: 0x5448() — WWDG-спин twin 0x3740 (insn>10000, ret=0): те же 8 записей, но 0x40002804=0x480000 (не 0). fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x5448)
    assert emu.insn > 10000, f'0x5448: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40002824) == [0xCA, 0x53, 0xFF, 0xCA, 0x53], \
        f"0x5448: 40002824={_pw(emu, 0x40002824)} ждём CA,53,FF,CA,53"
    assert _pw(emu, 0x40002804) == [0x480000], \
        f"0x5448: 40002804={_pw(emu, 0x40002804)} ждём [0x480000]"
    assert _pw(emu, 0x4000280C) == [0xFFFFFF7F, 0xFFFFFF5F], \
        f"0x5448: 4000280C={_pw(emu, 0x4000280C)} ждём 7F→5F"
    assert len(emu.periph_writes) == 8, \
        f'0x5448: P={len(emu.periph_writes)} ждём 8'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x5448: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'


@t(0x3780, 'E2-b73: 0x3780() — SPI-спин (insn>10000, ret=1/0xFF): GPIOB 0x40010828=0x10 ×2, '
           '0x40010818=0x10; SPI1_DR(0x4001300C): 0x6, 0x5, затем 0xFF×N (N '
           'контекстно-плавающее, ≥5); u16[0xB84]=0. fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x3780: E2-b73: 0x3780() — SPI-спин (insn>10000, ret=1/0xFF): GPIOB 0x40010828=0x10 ×2, 0x40010818=0x10; SPI1_DR(0x4001300C): 0x6, 0x5, затем 0xFF×N (N контекстно-плавающее, ≥5); u16[0xB84]=0. fresh-emu golden..
    Тест эмулятора @ 0x3780: E2-b73: 0x3780() — SPI-спин (insn>10000, ret=1/0xFF): GPIOB 0x40010828=0x10 ×2, 0x40010818=0x10; SPI1_DR(0x4001300C): 0x6, 0x5, затем 0xFF×N (N контекстно-плавающее, ≥5); u16[0xB84]=0. fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x3780)
    assert emu.insn > 10000, f'0x3780: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40010828) == [0x10, 0x10], \
        f"0x3780: 40010828={_pw(emu, 0x40010828)} ждём [0x10, 0x10]"
    assert _pw(emu, 0x40010818) == [0x10], \
        f"0x3780: 40010818={_pw(emu, 0x40010818)} ждём [0x10]"
    dr = _pw(emu, 0x4001300C)
    assert len(dr) >= 5 and dr[0] == 0x6 and dr[1] == 0x5 and \
        all(v == 0xFF for v in dr[2:]), \
        f'0x3780: DR={dr[:6]}...(len={len(dr)}) ждём 6,5,FF×N'
    rw = [(a - RAM, s, v) for pc, a, s, v in getattr(emu, 'ram_writes', [])]
    assert (0xB84, 2, 0) in rw, f'0x3780: R={rw} ждём u16[0xB84]=0'
    assert uc.reg_read(UC_ARM_REG_R0) in (1, 0xFF), \
        f'0x3780: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1/0xFF'


@t(0x8938, 'E2-b73: 0x8938() — константный возвращаемый (2248 insn, ret=0x1611F0): '
           'без периферийных/RAM-побочных эффектов в fresh-состоянии. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x8938: E2-b73: 0x8938() — константный возвращаемый (2248 insn, ret=0x1611F0): без периферийных/RAM-побочных эффектов в fresh-состоянии. smoke+ret+insn golden..
    Тест эмулятора @ 0x8938: E2-b73: 0x8938() — константный возвращаемый (2248 insn, ret=0x1611F0): без периферийных/RAM-побочных эффектов в fresh-состоянии. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x8938)
    assert len(emu.periph_writes) == 0, \
        f'0x8938: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x1611F0, \
        f'0x8938: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x1611F0'
    assert emu.insn == 2248, f'0x8938: insn={emu.insn} ждём 2248'
