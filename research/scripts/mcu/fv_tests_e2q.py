# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-b72: UART3-структура 0x1670 (BRR=0xFFFFFFFF, struct 0x40020030..0x40020040,
ret=0x40020030), AFIO-клейм 0x593c (0x40010414: 0x80→0x100→0x200, ret=0x200),
0x5c9c (0x40003000=0xAAAA + RCC BDCR, ret=0), WWDG/AFIO-инит 0x5cd0 (magic
CA→53→FF ×3, CTR 0x2808, AFIO 0x40010400..0x14, 0x40021010 FFBFFFFF, 0x40003000=AAAA,
0x40007000=0xFFFFFFFA, ret=0xFFFFFFFA), SPI/UART-init twin 0x5bc4 (=0x49b8(mode=1),
29 записей, ret=0x4621463A), чистые инициализаторы 0x5ee0 (ret=0x10) / 0x6618 (ret=1)
/ 0x6080 (ret=0), u16*10-калькулятор 0x4344 (u32[0x20000110]=u16[0x2000162B]*10),
флаг-диспетчеры 0x3de4/0x4508/0x3cac/0x55c8 (короткие пути + I2C-spin с magic
0x40022004: 0x45670123→0xCDEF89AB)."""
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


@t(0x1670, 'E2-b72: 0x1670() — UART3-структура (108 insn, ret=0x40020030): '
           '0x40020030: 0xFFFE→0→0x5A0→0x5A1 (BRR); 0x40020034=0x2; '
           '0x40020038=0x4002084C; 0x4002003C=0x20000B7E; 0x40020040=0; '
           '0x40020004=0xFFFFFFFF (BRR=FF). Возвращает указатель на struct. '
           'fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x1670: E2-b72: 0x1670() — UART3-структура (108 insn, ret=0x40020030): 0x40020030: 0xFFFE→0→0x5A0→0x5A1 (BRR); 0x40020034=0x2; 0x40020038=0x4002084C; 0x4002003C=0x20000B7E; 0x40020040=0; 0x40020004=0xFFFFFFFF (BRR=FF). Возвращает указатель на struct. fresh-emu golden..
    Тест эмулятора @ 0x1670: E2-b72: 0x1670() — UART3-структура (108 insn, ret=0x40020030): 0x40020030: 0xFFFE→0→0x5A0→0x5A1 (BRR); 0x40020034=0x2; 0x40020038=0x4002084C; 0x4002003C=0x20000B7E; 0x40020040=0; 0x40020004=0xFFFFFFFF (BRR=FF). Возвращает указатель на struct. fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x1670)
    # поле 0x40020030: 0xFFFE, затем 0×k (k контекстно-плавающий), 0x5A0, 0x5A1
    s30 = _pw(emu, 0x40020030)
    assert s30[0] == 0xFFFE and s30[-1] == 0x5A1 and s30[-2] == 0x5A0 and \
        all(v == 0 for v in s30[1:-2]), \
        f"0x1670: 40020030={s30} ждём FFFE→0×k→5A0→5A1"
    s34 = _pw(emu, 0x40020034)
    assert s34[-1] == 0x2 and all(v in (0, 2) for v in s34), \
        f"0x1670: 40020034={s34} ждём финал 2"
    s38 = _pw(emu, 0x40020038)
    assert s38[-1] == 0x4002084C and all(v in (0, 0x4002084C) for v in s38), \
        f"0x1670: 40020038={s38} ждём финал 0x4002084C"
    s3c = _pw(emu, 0x4002003C)
    assert s3c[-1] == 0x20000B7E and all(v in (0, 0x20000B7E) for v in s3c), \
        f"0x1670: 4002003C={s3c} ждём финал 0x20000B7E"
    assert _pw(emu, 0x40020040)[-1] == 0, \
        f"0x1670: 40020040={_pw(emu, 0x40020040)} ждём финал 0"
    assert _pw(emu, 0x40020004) == [0xFFFFFFFF], \
        f"0x1670: 40020004={_pw(emu, 0x40020004)} ждём FF"
    assert 9 <= len(emu.periph_writes) <= 16, \
        f'0x1670: P={len(emu.periph_writes)} ждём 9..16'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x40020030, \
        f'0x1670: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x40020030'
    assert emu.insn == 108, f'0x1670: insn={emu.insn} ждём 108'


@t(0x593C, 'E2-b72: 0x593c() — AFIO-клейм (37 insn, ret=0x200): 0x40010414: '
           '0x80→0x100→0x200 (3 записи). fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x593c: E2-b72: 0x593c() — AFIO-клейм (37 insn, ret=0x200): 0x40010414: 0x80→0x100→0x200 (3 записи). fresh-emu golden..
    Тест эмулятора @ 0x593c: E2-b72: 0x593c() — AFIO-клейм (37 insn, ret=0x200): 0x40010414: 0x80→0x100→0x200 (3 записи). fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x593C)
    assert _pw(emu, 0x40010414) == [0x80, 0x100, 0x200], \
        f"0x593c: 40010414={_pw(emu, 0x40010414)} ждём 80→100→200"
    assert len(emu.periph_writes) == 3, \
        f'0x593c: P={len(emu.periph_writes)} ждём 3'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x200, \
        f'0x593c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x200'
    assert emu.insn == 37, f'0x593c: insn={emu.insn} ждём 37'


@t(0x5C9C, 'E2-b72: 0x5c9c() — 0x40003000=0xAAAA + RCC BDCR (166 insn, ret=0): '
           '2 записи (0x40003000=0xAAAA, 0x40021018=0xFFFFFFFF). fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x5c9c: E2-b72: 0x5c9c() — 0x40003000=0xAAAA + RCC BDCR (166 insn, ret=0): 2 записи (0x40003000=0xAAAA, 0x40021018=0xFFFFFFFF). fresh-emu golden..
    Тест эмулятора @ 0x5c9c: E2-b72: 0x5c9c() — 0x40003000=0xAAAA + RCC BDCR (166 insn, ret=0): 2 записи (0x40003000=0xAAAA, 0x40021018=0xFFFFFFFF). fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x5C9C)
    assert _pw(emu, 0x40003000) == [0xAAAA], \
        f"0x5c9c: 40003000={_pw(emu, 0x40003000)} ждём [0xAAAA]"
    assert _pw(emu, 0x40021018) == [0xFFFFFFFF], \
        f"0x5c9c: 40021018={_pw(emu, 0x40021018)} ждём FF"
    assert len(emu.periph_writes) == 2, \
        f'0x5c9c: P={len(emu.periph_writes)} ждём 2'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x5c9c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 166, f'0x5c9c: insn={emu.insn} ждём 166'


@t(0x5CD0, 'E2-b72: 0x5cd0() — WWDG/AFIO-инит (460 insn, ret=0xFFFFFFFA): '
           '0x40002824: CA→53→FF ×3 (9 записей); 0x40002808: F8→FC ×4; '
           '0x40002814=0; 0x4000280C=0xFFFFFBFF; AFIO: 0x40010414=0x100000 ×2, '
           '0x40010400/04/08/0C: 0xFFEFFFFF→FF; 0x40021010: FF→0xFFBFFFFF; '
           '0x40003000=0xAAAA; 0x40007008=0xFFFFDFFF; 0x40007000=0xFFFFFFFA; '
           'u32[0x20000A4C]=0. 31 записей. fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x5cd0: E2-b72: 0x5cd0() — WWDG/AFIO-инит (460 insn, ret=0xFFFFFFFA): 0x40002824: CA→53→FF ×3 (9 записей); 0x40002808: F8→FC ×4; 0x40002814=0; 0x4000280C=0xFFFFFBFF; AFIO: 0x40010414=0x100000 ×2, 0x40010400/04/08/0C: 0xFFEFFFFF→FF; 0x40021010: FF→0xFFBFFFFF; 0x40003000=0xAAAA; 0x40007008=0xFFFFDFFF; 0x40007000=0xFFFFFFFA; u32[0x20000A4C]=0. 31 записей. fresh-emu golden..
    Тест эмулятора @ 0x5cd0: E2-b72: 0x5cd0() — WWDG/AFIO-инит (460 insn, ret=0xFFFFFFFA): 0x40002824: CA→53→FF ×3 (9 записей); 0x40002808: F8→FC ×4; 0x40002814=0; 0x4000280C=0xFFFFFBFF; AFIO: 0x40010414=0x100000 ×2, 0x40010400/04/08/0C: 0xFFEFFFFF→FF; 0x40021010: FF→0xFFBFFFFF; 0x40003000=0xAAAA; 0x40007008=0xFFFFDFFF; 0x40007000=0xFFFFFFFA; u32[0x20000A4C]=0. 31 записей. fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x5CD0)
    pw = emu.periph_writes
    assert len(pw) in (31, 34), f'0x5cd0: P={len(pw)} ждём 31/34'
    m = _pw(emu, 0x40002824)
    assert len(m) in (9, 12) and all(
        m[j:j+3] == [0xCA, 0x53, 0xFF] for j in range(0, len(m), 3)), \
        f"0x5cd0: 40002824={m} ждём (CA,53,FF)×3/×4"
    c = _pw(emu, 0x40002808)
    assert len(c) in (3, 4) and c[0] == 0xFFFFFFF8 and \
        all(v == 0xFFFFFFFC for v in c[1:]), \
        f"0x5cd0: 40002808={c} ждём F8→FC×2/3"
    assert _pw(emu, 0x40002814) == [0x0], \
        f"0x5cd0: 40002814={_pw(emu, 0x40002814)} ждём [0]"
    assert _pw(emu, 0x4000280C) == [0xFFFFFBFF], \
        f"0x5cd0: 4000280C={_pw(emu, 0x4000280C)} ждём [0xFFFFFBFF]"
    assert _pw(emu, 0x40010414) == [0x100000, 0x100000], \
        f"0x5cd0: 40010414={_pw(emu, 0x40010414)} ждём 0x100000×2"
    assert _pw(emu, 0x40010400) == [0xFFEFFFFF, 0xFFFFFFFF], \
        f"0x5cd0: 40010400={_pw(emu, 0x40010400)} ждём FFEFFFFF→FF"
    assert _pw(emu, 0x40010404) == [0xFFEFFFFF], \
        f"0x5cd0: 40010404={_pw(emu, 0x40010404)}"
    assert _pw(emu, 0x40010408) == [0xFFEFFFFF, 0xFFFFFFFF], \
        f"0x5cd0: 40010408={_pw(emu, 0x40010408)}"
    assert _pw(emu, 0x4001040C) == [0xFFEFFFFF], \
        f"0x5cd0: 4001040C={_pw(emu, 0x4001040C)}"
    assert _pw(emu, 0x40021010) == [0xFFFFFFFF, 0xFFBFFFFF], \
        f"0x5cd0: 40021010={_pw(emu, 0x40021010)} ждём FF→FFBFFFFF"
    assert _pw(emu, 0x40003000) == [0xAAAA], \
        f"0x5cd0: 40003000={_pw(emu, 0x40003000)} ждём [0xAAAA]"
    assert _pw(emu, 0x40007008) == [0xFFFFDFFF], \
        f"0x5cd0: 40007008={_pw(emu, 0x40007008)}"
    assert _pw(emu, 0x40007000) == [0xFFFFFFFA], \
        f"0x5cd0: 40007000={_pw(emu, 0x40007000)}"
    assert _r(uc, 0xA4C, 4) == 0, f'0x5cd0: u32[0xA4C]={_r(uc, 0xA4C, 4):#x} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0xFFFFFFFA, \
        f'0x5cd0: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0xFFFFFFFA'
    assert emu.insn == 460, f'0x5cd0: insn={emu.insn} ждём 460'


@t(0x5BC4, 'E2-b72: 0x5bc4() — SPI/UART-init twin 0x49b8(mode=1) (592 insn, '
           'ret=0x4621463A): 29 записей идентичны 0x49b8(1): RCC 0x40021014/18, '
           '0x4002102C FE0F→FE02, 0x40021028 clr, UART3 0x40020004/30..3C, '
           'GPIOB 0x40010818/28=0x10, SPI1 0x40013000=0xFFBF + 0x4001300C=0xB9, '
           '0x4002100C/0x40021018 clr (bics-квирк), byte[0xB82]=0. fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x5bc4: E2-b72: 0x5bc4() — SPI/UART-init twin 0x49b8(mode=1) (592 insn, ret=0x4621463A): 29 записей идентичны 0x49b8(1): RCC 0x40021014/18, 0x4002102C FE0F→FE02, 0x40021028 clr, UART3 0x40020004/30..3C, GPIOB 0x40010818/28=0x10, SPI1 0x40013000=0xFFBF + 0x4001300C=0xB9, 0x4002100C/0x40021018 clr (bics-квирк), byte[0xB82]=0. fresh-emu golden..
    Тест эмулятора @ 0x5bc4: E2-b72: 0x5bc4() — SPI/UART-init twin 0x49b8(mode=1) (592 insn, ret=0x4621463A): 29 записей идентичны 0x49b8(1): RCC 0x40021014/18, 0x4002102C FE0F→FE02, 0x40021028 clr, UART3 0x40020004/30..3C, GPIOB 0x40010818/28=0x10, SPI1 0x40013000=0xFFBF + 0x4001300C=0xB9, 0x4002100C/0x40021018 clr (bics-квирк), byte[0xB82]=0. fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x5BC4)
    pw = emu.periph_writes
    assert len(pw) == 29, f'0x5bc4: P={len(pw)} ждём 29'
    assert _pw(emu, 0x4002102C) == [0xFFFFFE0F, 0xFFFFFE02], \
        f"0x5bc4: 4002102C={_pw(emu, 0x4002102C)} ждём FE0F→FE02"
    assert _p(uc, 0x40021028) in (0xFFFFEFFF, 0xFFFFFFEF), \
        f'0x5bc4: 40021028={_p(uc, 0x40021028):#x} ждём clr bit12/bit4'
    assert _p(uc, 0x40020004) == 0xFFFFFFFF, \
        f"0x5bc4: 40020004={_p(uc, 0x40020004):#x} ждём FF"
    for off in (0x30, 0x34, 0x38, 0x3C):
        assert _p(uc, 0x40020000 + off) == 0, \
            f"0x5bc4: 40020000+{off:#x}={_p(uc, 0x40020000 + off):#x} ждём 0"
    assert _p(uc, 0x40010818) == 0x10 and _p(uc, 0x40010828) == 0x10, \
        f"0x5bc4: 40010818/28={_p(uc, 0x40010818):#x}/{_p(uc, 0x40010828):#x}"
    assert _p(uc, 0x40013000, 2) == 0xFFBF, \
        f"0x5bc4: SPI1_CTLR={_p(uc, 0x40013000, 2):#x} ждём 0xFFBF"
    assert _p(uc, 0x4001300C, 2) == 0xB9, \
        f"0x5bc4: SPI1_DR={_p(uc, 0x4001300C, 2):#x} ждём 0xB9"
    assert _p(uc, 0x4002100C) in (0xFFFFEFFF, 0xFFFFFFEF), \
        f'0x5bc4: 4002100C={_p(uc, 0x4002100C):#x} ждём clr bit12/bit4'
    assert _p(uc, 0x40021018) in (0xFFFFEFFF, 0xFFFFFFEF), \
        f'0x5bc4: 40021018={_p(uc, 0x40021018):#x} ждём clr bit12/bit4'
    assert _r(uc, 0xB82) == 0, f'0x5bc4: byte[0xB82]={_r(uc, 0xB82):#x} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x4621463A, \
        f'0x5bc4: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x4621463A'
    assert emu.insn == 592, f'0x5bc4: insn={emu.insn} ждём 592'


@t(0x5EE0, 'E2-b72: 0x5ee0() — чистый инициализатор (574 insn, ret=0x10): без '
           'периферийных/RAM-побочных эффектов в fresh-состоянии. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x5ee0: E2-b72: 0x5ee0() — чистый инициализатор (574 insn, ret=0x10): без периферийных/RAM-побочных эффектов в fresh-состоянии. smoke+ret+insn golden..
    Тест эмулятора @ 0x5ee0: E2-b72: 0x5ee0() — чистый инициализатор (574 insn, ret=0x10): без периферийных/RAM-побочных эффектов в fresh-состоянии. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x5EE0)
    assert len(emu.periph_writes) == 0, \
        f'0x5ee0: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x10, \
        f'0x5ee0: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x10'
    assert emu.insn == 574, f'0x5ee0: insn={emu.insn} ждём 574'


@t(0x6618, 'E2-b72: 0x6618() — инициализатор (262 insn, ret=1, tail в unmapped): '
           'без периферийных/RAM-эффектов в fresh-состоянии. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x6618: E2-b72: 0x6618() — инициализатор (262 insn, ret=1, tail в unmapped): без периферийных/RAM-эффектов в fresh-состоянии. smoke+ret+insn golden..
    Тест эмулятора @ 0x6618: E2-b72: 0x6618() — инициализатор (262 insn, ret=1, tail в unmapped): без периферийных/RAM-эффектов в fresh-состоянии. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x6618)
    assert len(emu.periph_writes) == 0, \
        f'0x6618: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x6618: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'
    assert emu.insn == 262, f'0x6618: insn={emu.insn} ждём 262'


@t(0x6080, 'E2-b72: 0x6080() — инициализатор (76 insn, ret=0, tail в unmapped): '
           'без периферийных/RAM-эффектов в fresh-состоянии. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x6080: E2-b72: 0x6080() — инициализатор (76 insn, ret=0, tail в unmapped): без периферийных/RAM-эффектов в fresh-состоянии. smoke+ret+insn golden..
    Тест эмулятора @ 0x6080: E2-b72: 0x6080() — инициализатор (76 insn, ret=0, tail в unmapped): без периферийных/RAM-эффектов в fresh-состоянии. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x6080)
    assert len(emu.periph_writes) == 0, \
        f'0x6080: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x6080: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 76, f'0x6080: insn={emu.insn} ждём 76'


@t(0x4344, 'E2-b72: 0x4344() — u16*10-калькулятор: v = u16[0x2000162B] * 10 '
           '(ldrh+add lsl #2+lsl #1) → u32[0x20000110]=v; затем флаг byte[0x20000107] '
           'bit2 выбирает ветку (insn 40/57); ret=0. 4 кейса u16 × fresh-флаг.')
def _(run, rng):
    """Emulator test @ 0x4344: E2-b72: 0x4344() — u16*10-калькулятор: v = u16[0x2000162B] * 10 (ldrh+add lsl #2+lsl #1) → u32[0x20000110]=v; затем флаг byte[0x20000107] bit2 выбирает ветку (insn 40/57); ret=0. 4 кейса u16 × fresh-флаг..
    Тест эмулятора @ 0x4344: E2-b72: 0x4344() — u16*10-калькулятор: v = u16[0x2000162B] * 10 (ldrh+add lsl #2+lsl #1) → u32[0x20000110]=v; затем флаг byte[0x20000107] bit2 выбирает ветку (insn 40/57); ret=0. 4 кейса u16 × fresh-флаг..
    """
    for val in (0, 1, 0x1234, 0x7FFF):
        uc, emu, lp = _fresh_probe(0x4344, seeds=[(0x2000162B, val)])
        assert _r(uc, 0x110, 4) == (val * 10) & 0xFFFFFFFF, \
            (f'0x4344 u16={val:#x}: u32[0x110]={_r(uc, 0x110, 4):#x} '
             f'ждём {(val * 10):#x}')
        assert uc.reg_read(UC_ARM_REG_R0) == 0, \
            f'0x4344 u16={val:#x}: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
        assert emu.insn > 20, f'0x4344 u16={val:#x}: insn={emu.insn} ждём >20'


@t(0x3DE4, 'E2-b72: 0x3de4() — флаг-диспетчер (флаг byte[0x20000107]): b=0 → '
           '123 insn ret=0; b=1 → 26 insn ret=0; b=2 → 21 insn ret=2; все пути — '
           'без записей, tail в unmapped. 3 кейса.')
def _(run, rng):
    """Emulator test @ 0x3de4: E2-b72: 0x3de4() — флаг-диспетчер (флаг byte[0x20000107]): b=0 → 123 insn ret=0; b=1 → 26 insn ret=0; b=2 → 21 insn ret=2; все пути — без записей, tail в unmapped. 3 кейса..
    Тест эмулятора @ 0x3de4: E2-b72: 0x3de4() — флаг-диспетчер (флаг byte[0x20000107]): b=0 → 123 insn ret=0; b=1 → 26 insn ret=0; b=2 → 21 insn ret=2; все пути — без записей, tail в unmapped. 3 кейса..
    """
    for val, exp_insn, exp_ret in ((0, 123, 0), (1, 26, 0), (2, 21, 2)):
        uc, emu, lp = _fresh_probe(0x3DE4, seeds=[(0x20000107, val)])
        assert len(emu.periph_writes) == 0, \
            f'0x3de4 b={val}: P={len(emu.periph_writes)} ждём 0'
        assert uc.reg_read(UC_ARM_REG_R0) == exp_ret, \
            f'0x3de4 b={val}: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём {exp_ret}'
        assert emu.insn == exp_insn, \
            f'0x3de4 b={val}: insn={emu.insn} ждём {exp_insn}'


@t(0x4508, 'E2-b72: 0x4508() — флаг-диспетчер (флаг byte[0x2000011D]): b=0 → '
           '21 insn ret=0; b=1 → 29 insn ret=0; b=2 → I2C-spin (insn>10000, ret=1, '
           '0x40022004: 0x45670123→0xCDEF89AB, 0x4002200C=0xFFFFFFFF). 3 кейса.')
def _(run, rng):
    """Emulator test @ 0x4508: E2-b72: 0x4508() — флаг-диспетчер (флаг byte[0x2000011D]): b=0 → 21 insn ret=0; b=1 → 29 insn ret=0; b=2 → I2C-spin (insn>10000, ret=1, 0x40022004: 0x45670123→0xCDEF89AB, 0x4002200C=0xFFFFFFFF). 3 кейса..
    Тест эмулятора @ 0x4508: E2-b72: 0x4508() — флаг-диспетчер (флаг byte[0x2000011D]): b=0 → 21 insn ret=0; b=1 → 29 insn ret=0; b=2 → I2C-spin (insn>10000, ret=1, 0x40022004: 0x45670123→0xCDEF89AB, 0x4002200C=0xFFFFFFFF). 3 кейса..
    """
    uc, emu, lp = _fresh_probe(0x4508, seeds=[(0x2000011D, 0)])
    assert len(emu.periph_writes) == 0, \
        f'0x4508 b=0: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x4508 b=0: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 21, f'0x4508 b=0: insn={emu.insn} ждём 21'
    uc, emu, lp = _fresh_probe(0x4508, seeds=[(0x2000011D, 1)])
    assert len(emu.periph_writes) == 0, \
        f'0x4508 b=1: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x4508 b=1: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 29, f'0x4508 b=1: insn={emu.insn} ждём 29'
    uc, emu, lp = _fresh_probe(0x4508, seeds=[(0x2000011D, 2)])
    assert emu.insn > 10000, f'0x4508 b=2: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40022004) == [0x45670123, 0xCDEF89AB], \
        f"0x4508 b=2: 40022004={_pw(emu, 0x40022004)} ждём magic"
    assert _pw(emu, 0x4002200C) == [0xFFFFFFFF], \
        f"0x4508 b=2: 4002200C={_pw(emu, 0x4002200C)} ждём FF"
    assert len(emu.periph_writes) == 3, \
        f'0x4508 b=2: P={len(emu.periph_writes)} ждём 3'
    assert uc.reg_read(UC_ARM_REG_R0) in (1, 6), \
        f'0x4508 b=2: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1/6'


@t(0x3CAC, 'E2-b72: 0x3cac() — флаг-реадер (флаг byte[0x20000084] & 1): b=0 → '
           '30 insn ret=0; b=1 → 46 insn ret=0; b=2 → I2C-spin (insn>10000, ret=1, '
           '0x40022004: 0x45670123→0xCDEF89AB, 0x4002200C=0xFFFFFFFF). 3 кейса.')
def _(run, rng):
    """Emulator test @ 0x3cac: E2-b72: 0x3cac() — флаг-реадер (флаг byte[0x20000084] & 1): b=0 → 30 insn ret=0; b=1 → 46 insn ret=0; b=2 → I2C-spin (insn>10000, ret=1, 0x40022004: 0x45670123→0xCDEF89AB, 0x4002200C=0xFFFFFFFF). 3 кейса..
    Тест эмулятора @ 0x3cac: E2-b72: 0x3cac() — флаг-реадер (флаг byte[0x20000084] & 1): b=0 → 30 insn ret=0; b=1 → 46 insn ret=0; b=2 → I2C-spin (insn>10000, ret=1, 0x40022004: 0x45670123→0xCDEF89AB, 0x4002200C=0xFFFFFFFF). 3 кейса..
    """
    uc, emu, lp = _fresh_probe(0x3CAC, seeds=[(0x20000084, 0)])
    assert len(emu.periph_writes) == 0, \
        f'0x3cac b=0: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x3cac b=0: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 30, f'0x3cac b=0: insn={emu.insn} ждём 30'
    uc, emu, lp = _fresh_probe(0x3CAC, seeds=[(0x20000084, 1)])
    assert len(emu.periph_writes) == 0, \
        f'0x3cac b=1: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x3cac b=1: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 46, f'0x3cac b=1: insn={emu.insn} ждём 46'
    uc, emu, lp = _fresh_probe(0x3CAC, seeds=[(0x20000084, 2)])
    assert emu.insn > 10000, f'0x3cac b=2: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40022004) == [0x45670123, 0xCDEF89AB], \
        f"0x3cac b=2: 40022004={_pw(emu, 0x40022004)} ждём magic"
    assert _pw(emu, 0x4002200C) == [0xFFFFFFFF], \
        f"0x3cac b=2: 4002200C={_pw(emu, 0x4002200C)} ждём FF"
    assert len(emu.periph_writes) == 3, \
        f'0x3cac b=2: P={len(emu.periph_writes)} ждём 3'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x3cac b=2: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'


@t(0x55C8, 'E2-b72: 0x55c8() — флаг-диспетчер (флаг byte[0x200000F8]): b=0 → '
           '6 insn ret=0; b=1 → I2C-spin (insn>10000, ret=1, 0x40022004: '
           '0x45670123→0xCDEF89AB, 0x4002200C=0xFFFFFFFF); b=2 → 6 insn ret=2. '
           '3 кейса.')
def _(run, rng):
    """Emulator test @ 0x55c8: E2-b72: 0x55c8() — флаг-диспетчер (флаг byte[0x200000F8]): b=0 → 6 insn ret=0; b=1 → I2C-spin (insn>10000, ret=1, 0x40022004: 0x45670123→0xCDEF89AB, 0x4002200C=0xFFFFFFFF); b=2 → 6 insn ret=2. 3 кейса..
    Тест эмулятора @ 0x55c8: E2-b72: 0x55c8() — флаг-диспетчер (флаг byte[0x200000F8]): b=0 → 6 insn ret=0; b=1 → I2C-spin (insn>10000, ret=1, 0x40022004: 0x45670123→0xCDEF89AB, 0x4002200C=0xFFFFFFFF); b=2 → 6 insn ret=2. 3 кейса..
    """
    uc, emu, lp = _fresh_probe(0x55C8, seeds=[(0x200000F8, 0)])
    assert len(emu.periph_writes) == 0, \
        f'0x55c8 b=0: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x55c8 b=0: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 6, f'0x55c8 b=0: insn={emu.insn} ждём 6'
    uc, emu, lp = _fresh_probe(0x55C8, seeds=[(0x200000F8, 1)])
    assert emu.insn > 10000, f'0x55c8 b=1: insn={emu.insn} ждём спин (>10000)'
    assert _pw(emu, 0x40022004) == [0x45670123, 0xCDEF89AB], \
        f"0x55c8 b=1: 40022004={_pw(emu, 0x40022004)} ждём magic"
    assert _pw(emu, 0x4002200C) == [0xFFFFFFFF], \
        f"0x55c8 b=1: 4002200C={_pw(emu, 0x4002200C)} ждём FF"
    assert len(emu.periph_writes) == 3, \
        f'0x55c8 b=1: P={len(emu.periph_writes)} ждём 3'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x55c8 b=1: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'
    uc, emu, lp = _fresh_probe(0x55C8, seeds=[(0x200000F8, 2)])
    assert len(emu.periph_writes) == 0, \
        f'0x55c8 b=2: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 2, \
        f'0x55c8 b=2: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 2'
    assert emu.insn == 6, f'0x55c8 b=2: insn={emu.insn} ждём 6'
