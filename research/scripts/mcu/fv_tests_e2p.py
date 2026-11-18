# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-b71: инициализаторы-конструкторы и RCC-ключи: 0x1d78/0x48f8 (I2C-ret 0x10,
чистые), 0x30e0/0x3034 (RCC APB2ENR 0x40021000/0x40021004 cascade + 0x40022000=0xF8),
0x310c (BDCR/BDCR2 enable), 0x2a94/0x2b2c (RCC 0x40021014/18 + GPIOA ODR 0x40010008
clr bit13/14), GPIO batch-конфигуратор 0x3588 (GPIOA..D CRL/CRH/AFIO, 248 записей,
ret=0x1009FFF), SPI/UART-dispatcher 0x49b8 (mode 0→0, 1/2→init+ret 0x4621463A,
3→3), I2C-машина 0x280c (ret=0x80), 0x4a4c (2 аргумента, ret=0), spin 0x1cf6
(0x40005800=0xFFFF + 3 stack-записи) и WWDG-spin 0x31dc (magic CA→53→FF + CTR 0x244820)."""
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
    return [(a, s, v) for _, a, s, v in getattr(emu, 'ram_writes', [])]


@t(0x1D78, 'E2-b71: 0x1d78() — init-конструктор (579 insn, ret=0x10, tail 0x908c '
           'I2C-машина): fresh-emu — без периферийных/RAM-побочных эффектов. '
           'smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x1D78)
    assert len(emu.periph_writes) == 0, \
        f'0x1d78: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x10, \
        f'0x1d78: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x10'
    assert emu.insn == 579, f'0x1d78: insn={emu.insn} ждём 579'


@t(0x48F8, 'E2-b71: 0x48f8() — init (560 insn, ret=0x10, tail 0x8fec): без '
           'периферийных/RAM-побочных эффектов в fresh-состоянии. smoke+ret+insn golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x48F8)
    assert len(emu.periph_writes) == 0, \
        f'0x48f8: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x10, \
        f'0x48f8: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x10'
    assert emu.insn == 560, f'0x48f8: insn={emu.insn} ждём 560'


@t(0x30E0, 'E2-b71: 0x30e0() — RCC APB2-ключ (188 insn, ret=0): 0x40021000: '
           'FE→FF; 0x40021004: FC→0C→C70C→C00C (cascade); 0x40022000=0xF8. '
           'fresh-emu golden по последовательности записей.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x30E0)
    assert _pw(emu, 0x40021000) == [0xFFFFFFFE, 0xFFFFFFFF], \
        f"0x30e0: 40021000={_pw(emu, 0x40021000)} ждём FE→FF"
    assert _pw(emu, 0x40021004) == [0xFFFFFFFC, 0xFFFFFF0C, 0xFFFFC70C,
                                    0xFFFFC00C], \
        f"0x30e0: 40021004={_pw(emu, 0x40021004)} ждём FC→0C→C70C→C00C"
    assert _pw(emu, 0x40022000) == [0xF8], \
        f"0x30e0: 40022000={_pw(emu, 0x40022000)} ждём [0xF8]"
    assert len(emu.periph_writes) == 7, \
        f'0x30e0: P={len(emu.periph_writes)} ждём 7'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x30e0: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 188, f'0x30e0: insn={emu.insn} ждём 188'


@t(0x310C, 'E2-b71: 0x310c() — RCC BDCR-enable (27 insn, ret=1): 0x4002101C=0xFFFFFFFF, '
           '0x40021018=0xFFFFFFFF (2 записи). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x310C)
    assert _pw(emu, 0x4002101C) == [0xFFFFFFFF], \
        f"0x310c: 4002101C={_pw(emu, 0x4002101C)} ждём FF"
    assert _pw(emu, 0x40021018) == [0xFFFFFFFF], \
        f"0x310c: 40021018={_pw(emu, 0x40021018)} ждём FF"
    assert len(emu.periph_writes) == 2, \
        f'0x310c: P={len(emu.periph_writes)} ждём 2'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x310c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'
    assert emu.insn == 27, f'0x310c: insn={emu.insn} ждём 27'


@t(0x3034, 'E2-b71: 0x3034() — композит (190 insn, ret=0): 0x30e0() + 0x3600(); '
           'RCC-записи идентичны 0x30e0 (7: 0x40021000 FE→FF, 0x40021004 cascade, '
           '0x40022000=0xF8). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x3034)
    assert _pw(emu, 0x40021000) == [0xFFFFFFFE, 0xFFFFFFFF], \
        f"0x3034: 40021000={_pw(emu, 0x40021000)} ждём FE→FF"
    assert _pw(emu, 0x40021004) == [0xFFFFFFFC, 0xFFFFFF0C, 0xFFFFC70C,
                                    0xFFFFC00C], \
        f"0x3034: 40021004={_pw(emu, 0x40021004)} ждём cascade"
    assert _pw(emu, 0x40022000) == [0xF8], \
        f"0x3034: 40022000={_pw(emu, 0x40022000)} ждём [0xF8]"
    assert len(emu.periph_writes) == 7, \
        f'0x3034: P={len(emu.periph_writes)} ждём 7'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x3034: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 190, f'0x3034: insn={emu.insn} ждём 190'


@t(0x2A94, 'E2-b71: 0x2a94() — GPIOA-ODR + RCC (1372 insn, ret=0, tail 0x85fc→0x864e): '
           '0x40021014=FF; 0x40010008: 0xFFFFCFFF→0xFFFFDFFF (clr bit13→bit14); '
           '0x40021018=FF×2. fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x2A94)
    assert _pw(emu, 0x40021014) == [0xFFFFFFFF], \
        f"0x2a94: 40021014={_pw(emu, 0x40021014)} ждём FF"
    assert _pw(emu, 0x40010008) == [0xFFFFCFFF, 0xFFFFDFFF], \
        f"0x2a94: 40010008={_pw(emu, 0x40010008)} ждём CFFF→DFFF"
    assert _pw(emu, 0x40021018) == [0xFFFFFFFF, 0xFFFFFFFF], \
        f"0x2a94: 40021018={_pw(emu, 0x40021018)} ждём FF×2"
    assert len(emu.periph_writes) == 5, \
        f'0x2a94: P={len(emu.periph_writes)} ждём 5'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x2a94: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 1372, f'0x2a94: insn={emu.insn} ждём 1372'


@t(0x2B2C, 'E2-b71: 0x2b2c() — RCC-only twin 0x2a94 (175 insn, ret=0, tail 0x864e): '
           '0x40021014=FF, 0x40021018=FF; без GPIOA ODR-записи. fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x2B2C)
    assert _pw(emu, 0x40021014) == [0xFFFFFFFF], \
        f"0x2b2c: 40021014={_pw(emu, 0x40021014)} ждём FF"
    assert _pw(emu, 0x40021018) == [0xFFFFFFFF], \
        f"0x2b2c: 40021018={_pw(emu, 0x40021018)} ждём FF"
    assert len(emu.periph_writes) == 2, \
        f'0x2b2c: P={len(emu.periph_writes)} ждём 2'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x2b2c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 175, f'0x2b2c: insn={emu.insn} ждём 175'


@t(0x3588, 'E2-b71: 0x3588(&buf) — GPIO batch-конфигуратор (5851 insn, ret=0x1009FFF): '
           '248 записей по GPIOA..D (0x40010800..0x40011424): CRL-clr-loop '
           '(0x40010C0C: FC→F0→C0→0) + CRH set (0x4001080C финал 0x3C000000) + '
           'AFIO (0x40010820/24, 0x40010C20/24). fresh-emu golden (subset).')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x3588, args=(RAM + 0x100,),
                               seeds=[(RAM + 0x100, 0x1234)])
    pw = emu.periph_writes
    assert len(pw) == 248, f'0x3588: P={len(pw)} ждём 248'
    assert (pw[0][1], pw[0][3]) == (0x40010C20, 0xFFFFFFFF), \
        f"0x3588: first={pw[0]} ждём 40010C20=FF"
    assert (pw[1][1], pw[1][3]) == (0x40010C00, 0xFFFFFFFF), \
        f"0x3588: second={pw[1]} ждём 40010C00=FF"
    assert _p(uc, 0x4001080C) == 0x3C000000, \
        f"0x3588: 4001080C={_p(uc, 0x4001080C):#x} ждём 0x3C000000"
    assert _p(uc, 0x40010C0C) == 0, \
        f"0x3588: 40010C0C={_p(uc, 0x40010C0C):#x} ждём 0 (clr-loop финал)"
    assert _p(uc, 0x40010800) == 0xFFFFFFFF, \
        f"0x3588: 40010800={_p(uc, 0x40010800):#x} ждём FF"
    assert uc.reg_read(UC_ARM_REG_R0) == 0x1009FFF, \
        f'0x3588: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x1009FFF'
    assert emu.insn == 5851, f'0x3588: insn={emu.insn} ждём 5851'


@t(0x49B8, 'E2-b71: 0x49b8(mode) — SPI/UART-init-dispatcher: mode=0 → ret=0 (6 insn, '
           'no writes); mode=1 → 29 записей (RCC 0x40021014/18/2C/28, 0x40020004/30..3C, '
           'GPIOB 0x40010818/28=0x10, SPI1 0x40013000=0xFFBF + 0x4001300C=0xB9, '
           '0x4002100C/0x40021018 clr bit12 — bics-квирк), byte[0xB82]=0, '
           'ret=0x4621463A (585 insn); mode=2 → то же (587 insn); mode=3 → ret=3. '
           '4 кейса.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x49B8, args=(0,))
    assert len(emu.periph_writes) == 0, \
        f'0x49b8(0): P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x49b8(0): ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 6, f'0x49b8(0): insn={emu.insn} ждём 6'
    uc, emu, lp = _fresh_probe(0x49B8, args=(1,))
    pw = emu.periph_writes
    assert len(pw) == 29, f'0x49b8(1): P={len(pw)} ждём 29'
    assert _pw(emu, 0x4002102C) == [0xFFFFFE0F, 0xFFFFFE02], \
        f"0x49b8(1): 4002102C={_pw(emu, 0x4002102C)} ждём FE0F→FE02"
    assert _p(uc, 0x40021028) in (0xFFFFEFFF, 0xFFFFFFEF), \
        f'0x49b8(1): 40021028={_p(uc, 0x40021028):#x} ждём clr bit12/bit4'
    assert _p(uc, 0x40020004) == 0xFFFFFFFF, \
        f"0x49b8(1): 40020004={_p(uc, 0x40020004):#x} ждём FF"
    for off in (0x30, 0x34, 0x38, 0x3C):
        assert _p(uc, 0x40020000 + off) == 0, \
            f"0x49b8(1): 40020000+{off:#x}={_p(uc, 0x40020000 + off):#x} ждём 0"
    assert _p(uc, 0x40010818) == 0x10 and _p(uc, 0x40010828) == 0x10, \
        f"0x49b8(1): 40010818/28={_p(uc, 0x40010818):#x}/{_p(uc, 0x40010828):#x}"
    assert _p(uc, 0x40013000, 2) == 0xFFBF, \
        f"0x49b8(1): SPI1_CTLR={_p(uc, 0x40013000, 2):#x} ждём 0xFFBF"
    assert _p(uc, 0x4001300C, 2) == 0xB9, \
        f"0x49b8(1): SPI1_DR={_p(uc, 0x4001300C, 2):#x} ждём 0xB9"
    assert _p(uc, 0x4002100C) in (0xFFFFEFFF, 0xFFFFFFEF), \
        f'0x49b8(1): 4002100C={_p(uc, 0x4002100C):#x} ждём clr bit12/bit4'
    assert _p(uc, 0x40021018) in (0xFFFFEFFF, 0xFFFFFFEF), \
        f'0x49b8(1): 40021018={_p(uc, 0x40021018):#x} ждём clr bit12/bit4'
    assert _r(uc, 0xB82) == 0, f'0x49b8(1): byte[0xB82]={_r(uc, 0xB82):#x} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x4621463A, \
        f'0x49b8(1): ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x4621463A'
    assert emu.insn == 585, f'0x49b8(1): insn={emu.insn} ждём 585'
    uc, emu, lp = _fresh_probe(0x49B8, args=(2,))
    assert len(emu.periph_writes) == 29, \
        f'0x49b8(2): P={len(emu.periph_writes)} ждём 29'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x4621463A, \
        f'0x49b8(2): ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x4621463A'
    assert emu.insn == 587, f'0x49b8(2): insn={emu.insn} ждём 587'
    uc, emu, lp = _fresh_probe(0x49B8, args=(3,))
    assert len(emu.periph_writes) == 0, \
        f'0x49b8(3): P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 3, \
        f'0x49b8(3): ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 3'
    assert emu.insn == 10, f'0x49b8(3): insn={emu.insn} ждём 10'


@t(0x280C, 'E2-b71: 0x280c(&a, &b) — I2C-машина (2112 insn, ret=0x80, tail 0x908c): '
           'fresh 0xFF-периферия → детерминированный путь, все записи — только '
           'локальный стек; без периферийных эффектов. 4-регистровый args (a, b).')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x280C, args=(RAM + 0x500, RAM + 0x540),
                               seeds=[(RAM + 0x500, 0x33), (RAM + 0x540, 0x44)])
    assert len(emu.periph_writes) == 0, \
        f'0x280c: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x80, \
        f'0x280c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x80'
    assert emu.insn == 2112, f'0x280c: insn={emu.insn} ждём 2112'


@t(0x4A4C, 'E2-b71: 0x4a4c(&a, &b) — 2-аргументный обработчик (1562 insn, ret=0, '
           'tail 0x4aea): без периферийных эффектов в fresh-состоянии. '
           'args (a, b) + seeds.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x4A4C, args=(RAM + 0x300, RAM + 0x340),
                               seeds=[(RAM + 0x300, 0x11), (RAM + 0x340, 0x22)])
    assert len(emu.periph_writes) == 0, \
        f'0x4a4c: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x4a4c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 1562, f'0x4a4c: insn={emu.insn} ждём 1562'


@t(0x1CF6, 'E2-b71: 0x1cf6() — deterministic-spin (insn>10000, ret=0): u16[0x40005800]='
           '0xFFFF (1 запись); 3 RAM-записи c относительным паттерном (A-8: u16=1, '
           'A: byte=0x30, A+13: byte=1; A — контекстно-плавающий). smoke+ret+patтерн.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x1CF6)
    assert emu.insn > 10000, f'0x1cf6: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40005800) == [0xFFFF], \
        f"0x1cf6: 40005800={_pw(emu, 0x40005800)} ждём [0xFFFF]"
    rw = _ramw(emu)
    assert len(rw) == 3, f'0x1cf6: R={len(rw)} ждём 3'
    # паттерн: byte=0x30 на A; u16=1 на A-8; третья запись byte=1 (адрес —
    # контекстно-плавающий, относим только к значению/размеру)
    a30 = [a for a, s, v in rw if (s, v) == (1, 0x30)]
    assert len(a30) == 1, f'0x1cf6: 0x30-записей={len(a30)} ждём 1'
    a = a30[0]
    assert (a - 8, 2, 1) in rw, f'0x1cf6: у (A-8, 2, 1) нет в {rw}'
    rest = [w for w in rw if w != (a, 1, 0x30) and w != (a - 8, 2, 1)]
    assert len(rest) == 1 and rest[0][1] == 1 and rest[0][2] == 1, \
        f'0x1cf6: rest={rest} ждём [(A+?, 1, 1)]'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x1cf6: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'


@t(0x31DC, 'E2-b71: 0x31dc(&buf, n) — WWDG-spin (insn>10000, ret=0): 0x40002824: '
           'CA→53→FF→CA→53 (magic); 0x40002804=0x244820 (CTR); 0x4000280C: '
           '0xFFFFFF7F→0xFFFFFF5F. args (buf, 8), buf=0xA5. smoke+ret+WWDG-golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x31DC, args=(RAM + 0x400, 8),
                               seeds=[(RAM + 0x400, 0xA5)])
    assert emu.insn > 10000, f'0x31dc: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40002824) == [0xCA, 0x53, 0xFF, 0xCA, 0x53], \
        f"0x31dc: 40002824={_pw(emu, 0x40002824)} ждём CA→53→FF→CA→53"
    assert _pw(emu, 0x40002804) == [0x244820], \
        f"0x31dc: 40002804={_pw(emu, 0x40002804)} ждём [0x244820]"
    assert _pw(emu, 0x4000280C) == [0xFFFFFF7F, 0xFFFFFF5F], \
        f"0x31dc: 4000280C={_pw(emu, 0x4000280C)} ждём 7F→5F"
    assert len(emu.periph_writes) == 8, \
        f'0x31dc: P={len(emu.periph_writes)} ждём 8'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x31dc: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
