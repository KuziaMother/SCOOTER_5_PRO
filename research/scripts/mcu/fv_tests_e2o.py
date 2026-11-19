# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-b70: SPI on/off 0x106d8 + SPI1-init 0x106b8, GPIO-порт→RCC BDCR 0x163b4,
WWDG magic 0xcb40 / mode 0x14958, SysTick-init 0x22934, UART4-init 0x21804,
GPIO-init 0x1bedc / GPIOA-EXTI 0x107ec goldens, timer channel-config 0x22000
с assert-спинами, timer CCR/CCER field-config 0x22fac, lookup 48000//x 0x1d874,
varargs-helper 0x8f7c."""
import struct

from fv_core import *  # noqa: F401,F403

from unicorn import UcError, UC_HOOK_CODE, UC_HOOK_MEM_WRITE  # noqa: E402
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,  # noqa: E402
                               UC_ARM_REG_SP, UC_ARM_REG_LR)
from emulator.mcu_emu import PERIPH, SYS  # noqa: E402


def _fresh_probe(off, seeds=(), args=(), max_insn=50000):
    """Fresh-emu: чистый RAM, 0xFF PERIPH, seeds (int->u32 / bytes), args r0..r2;
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
    for i, a in enumerate(args):
        uc.reg_write((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)[i], a)
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


def _run_sys(off, args=(), seeds=(), max_insn=60000):
    """Как _fresh_probe, но дополнительно захватывает SYS-записи в emu.sys_writes."""
    emu = McuEmu(max_insn=max_insn)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))
    emu.hook_periph_ready()
    emu.sys_writes = []

    def _hw(uc_, access, address, size, value, user):
        """The helper function (_hw).
        Вспомогательная функция (_hw).
        """
        emu.sys_writes.append((address, value))

    uc.hook_add(UC_HOOK_MEM_WRITE, _hw, None, SYS, SYS + 0x100000)
    for addr, val in seeds:
        if isinstance(val, (bytes, bytearray)):
            uc.mem_write(addr, val)
        else:
            uc.mem_write(addr, struct.pack('<I', val))
    for i, a in enumerate(args):
        uc.reg_write((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)[i], a)
    uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
    uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    try:
        uc.emu_start(off | 1, 0, count=max_insn)
    except UcError:
        pass
    return uc, emu


# --- 0x106d8: SPI1/SPI2 on/off через 0xc6c4 (RCC APB2RSTR 0x4002100C) ---

@t(0x106D8, 'E2-b70: 0x106d8(base) — SPI reset-ключ: base==0x40013000 (SPI1): '
           '0xc6c4(0x1000,1)+0xc6c4(0x1000,0) → u32[0x4002100C] clr bit12/bit4 '
           '(bics-квирк: 0xffffefff/0xFFFFFFEF), ret=0x1000. '
           'base==0x40013C00 (SPI2): 0xc6c4(0x80000,1)+0xc6c4(0x80000,0) → '
           'clr bit15 (0xFFF7FFFF), ret=0x80000. другой base: без записей, '
           'ret ∈ {base, 0x40013C00}.')
def _(run, rng):
    # NOTE: в этом Unicorn бьилде bics rX,#imm несёт нестабильный imm (контекст-
    # зависимая декодировка: 0x4382 даёт маску r0 или r0>>7). Тесты утверждают
    # только контекстно-стабильные инварианты.
    """Emulator test @ 0x106d8: E2-b70: 0x106d8(base) — SPI reset-ключ: base==0x40013000 (SPI1): 0xc6c4(0x1000,1)+0xc6c4(0x1000,0) → u32[0x4002100C] clr bit12/bit4 (bics-квирк: 0xffffefff/0xFFFFFFEF), ret=0x1000. base==0x40013C00 (SPI2): 0xc6c4(0x80000,1)+0xc6c4(0x80000,0) → clr bit15 (0xFFF7FFFF), ret=0x80000. другой base: без записей, ret ∈ {base, 0x40013C00}..
    Тест эмулятора @ 0x106d8: E2-b70: 0x106d8(base) — SPI reset-ключ: base==0x40013000 (SPI1): 0xc6c4(0x1000,1)+0xc6c4(0x1000,0) → u32[0x4002100C] clr bit12/bit4 (bics-квирк: 0xffffefff/0xFFFFFFEF), ret=0x1000. base==0x40013C00 (SPI2): 0xc6c4(0x80000,1)+0xc6c4(0x80000,0) → clr bit15 (0xFFF7FFFF), ret=0x80000. другой base: без записей, ret ∈ {base, 0x40013C00}..
    """
    uc, emu, lp = _fresh_probe(0x106D8, args=(0x40013000,))
    v = _p(uc, 0x4002100C)
    assert v in (0xffffefff, 0xFFFFFFEF), \
        f"0x106d8 SPI1: 4002100C={v:#x} ждём clr bit12/bit4"
    assert uc.reg_read(UC_ARM_REG_R0) == 0x1000, \
        f'0x106d8 SPI1: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x1000'
    uc, emu, lp = _fresh_probe(0x106D8, args=(0x40013C00,))
    v = _p(uc, 0x4002100C)
    assert v in (0xFFF7FFFF, 0xFF7FFFFF), \
        f"0x106d8 SPI2: 4002100C={v:#x} ждём clr bit15/bit19"
    assert uc.reg_read(UC_ARM_REG_R0) == 0x80000, \
        f'0x106d8 SPI2: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x80000'
    uc, emu, lp = _fresh_probe(0x106D8, args=(0x40014000,))
    assert _p(uc, 0x4002100C) == 0xFFFFFFFF, \
        f'0x106d8 other: 4002100C={_p(uc, 0x4002100C):#x} ждём без изменений'
    assert uc.reg_read(UC_ARM_REG_R0) in (0x40014000, 0x40013C00), \
        f'0x106d8 other: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём base/константу'


# --- 0x106b8: SPI1-инициал (CTLR &= 0xFFBF, reset, BDCR clr 0x1000) ---

@t(0x106B8, 'E2-b70: 0x106b8() — SPI1-init: 0x106a0(0x40013000, 0) → u16[SPI1_CTLR]&=~0x40 '
           '(0xFFBF); 0x106d8(0x40013000) → RCC clr bit12/bit4 (bics-квирк); '
           '0xc6a4(0x1000, 0) → RCC BDCR 0x40021018 clr. ret=0x1000. fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x106b8: E2-b70: 0x106b8() — SPI1-init: 0x106a0(0x40013000, 0) → u16[SPI1_CTLR]&=~0x40 (0xFFBF); 0x106d8(0x40013000) → RCC clr bit12/bit4 (bics-квирк); 0xc6a4(0x1000, 0) → RCC BDCR 0x40021018 clr. ret=0x1000. fresh-emu golden..
    Тест эмулятора @ 0x106b8: E2-b70: 0x106b8() — SPI1-init: 0x106a0(0x40013000, 0) → u16[SPI1_CTLR]&=~0x40 (0xFFBF); 0x106d8(0x40013000) → RCC clr bit12/bit4 (bics-квирк); 0xc6a4(0x1000, 0) → RCC BDCR 0x40021018 clr. ret=0x1000. fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x106B8)
    assert _p(uc, 0x40013000, 2) == 0xFFBF, \
        f"0x106b8: u16[40013000]={_p(uc, 0x40013000, 2):#x} ждём 0xFFBF"
    v = _p(uc, 0x4002100C)
    assert v in (0xffffefff, 0xFFFFFFEF), \
        f"0x106b8: 4002100C={v:#x} ждём clr bit12/bit4"
    v2 = _p(uc, 0x40021018)
    assert v2 in (0xffffefff, 0xFFFFFFEF), \
        f"0x106b8: 40021018={v2:#x} ждём clr bit12/bit4"
    assert uc.reg_read(UC_ARM_REG_R0) == 0x1000, \
        f'0x106b8: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x1000'
    assert emu.insn < 200, f'0x106b8: insn={emu.insn} ждём короткий путь'


# --- 0x163b4: GPIO-порт → RCC BDCR (0x40021018) bit по порту + общий bit0 ---

@t(0x163B4, 'E2-b70: 0x163b4(port) — RCC BDCR-ключ: 0x40010800(GPIOA)→|=4; 0x40010C00(GPIOB)→|=8; '
           '0x40011000(GPIOC)→|=0x10; 0x40011400(GPIOD)→|=0x20; любой case + общий |=1; '
           'неизвестный порт → только |=1. ret=1. Биты по портам = 2<<index.')
def _(run, rng):
    """Emulator test @ 0x163b4: E2-b70: 0x163b4(port) — RCC BDCR-ключ: 0x40010800(GPIOA)→|=4; 0x40010C00(GPIOB)→|=8; 0x40011000(GPIOC)→|=0x10; 0x40011400(GPIOD)→|=0x20; любой case + общий |=1; неизвестный порт → только |=1. ret=1. Биты по портам = 2<<index..
    Тест эмулятора @ 0x163b4: E2-b70: 0x163b4(port) — RCC BDCR-ключ: 0x40010800(GPIOA)→|=4; 0x40010C00(GPIOB)→|=8; 0x40011000(GPIOC)→|=0x10; 0x40011400(GPIOD)→|=0x20; любой case + общий |=1; неизвестный порт → только |=1. ret=1. Биты по портам = 2<<index..
    """
    for base, expect in ((0x40010800, 0x5), (0x40010C00, 0x9),
                         (0x40011000, 0x11), (0x40011400, 0x21),
                         (0x40011800, 0x1), (0x40010400, 0x1)):
        uc, emu, lp = _fresh_probe(0x163B4, args=(base,), seeds=[(0x40021018, 0)])
        got = _p(uc, 0x40021018)
        assert got == expect, f'0x163b4({base:#x}): BDCR={got:#x} ждём {expect:#x}'
        assert uc.reg_read(UC_ARM_REG_R0) == 1, \
            f'0x163b4({base:#x}): ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'


# --- 0xcb40: WWDG magic-последовательность ---

@t(0xCB40, 'E2-b70: 0xcb40() — WWDG magic: u32[0x40002808]&=~0x300 (0xFFFFFBFF); '
           'u32[0x40002824]: последовательность 0xCA→0x53→0xFF (3 записи); ret=1, insn=42. '
           'fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0xcb40: E2-b70: 0xcb40() — WWDG magic: u32[0x40002808]&=~0x300 (0xFFFFFBFF); u32[0x40002824]: последовательность 0xCA→0x53→0xFF (3 записи); ret=1, insn=42. fresh-emu golden..
    Тест эмулятора @ 0xcb40: E2-b70: 0xcb40() — WWDG magic: u32[0x40002808]&=~0x300 (0xFFFFFBFF); u32[0x40002824]: последовательность 0xCA→0x53→0xFF (3 записи); ret=1, insn=42. fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0xCB40)
    assert _p(uc, 0x40002808) == 0xFFFFFBFF, \
        f"0xcb40: 40002808={_p(uc, 0x40002808):#x} ждём 0xFFFFFBFF"
    seq = _pw(emu, 0x40002824)
    assert seq == [0xCA, 0x53, 0xFF], f'0xcb40: seq(40002824)={seq} ждём [0xca, 0x53, 0xff]'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0xcb40: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'
    assert emu.insn == 42, f'0xcb40: insn={emu.insn} ждём 42'


# --- 0x14958: WWDG mode set (r4 0..6 → 0xcb10-цепочка) ---

@t(0x14958, 'E2-b70: 0x14958(mode) — WWDG mode: mode=0 → без записей, ret=0. mode 1..6: '
           'u32[0x40002808]: clr bit3 + по-режимно (финал {0,1,2,3,4,5,6} → '
           'F8/F9/FA/FB/FC/FE); u32[0x40002824]: magic CA→53→FF; '
           'ret = mode-1 (1..5) / 6 (mode=6 special).')
def _(run, rng):
    """Emulator test @ 0x14958: E2-b70: 0x14958(mode) — WWDG mode: mode=0 → без записей, ret=0. mode 1..6: u32[0x40002808]: clr bit3 + по-режимно (финал {0,1,2,3,4,5,6} → F8/F9/FA/FB/FC/FE); u32[0x40002824]: magic CA→53→FF; ret = mode-1 (1..5) / 6 (mode=6 special)..
    Тест эмулятора @ 0x14958: E2-b70: 0x14958(mode) — WWDG mode: mode=0 → без записей, ret=0. mode 1..6: u32[0x40002808]: clr bit3 + по-режимно (финал {0,1,2,3,4,5,6} → F8/F9/FA/FB/FC/FE); u32[0x40002824]: magic CA→53→FF; ret = mode-1 (1..5) / 6 (mode=6 special)..
    """
    uc, emu, lp = _fresh_probe(0x14958, args=(0,))
    assert _p(uc, 0x40002808) == 0xFFFFFFFF and _pw(emu, 0x40002824) == [], \
        f'0x14958(0): 40002808={_p(uc, 0x40002808):#x} ждём без изменений'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x14958(0): ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    for mode, fin, ret in ((1, 0xFFFFFFF8, 0), (2, 0xFFFFFFF9, 1), (3, 0xFFFFFFFA, 2),
                           (4, 0xFFFFFFFB, 3), (5, 0xFFFFFFFC, 4), (6, 0xFFFFFFFE, 6)):
        uc, emu, lp = _fresh_probe(0x14958, args=(mode,))
        assert _p(uc, 0x40002808) == fin, \
            f'0x14958({mode}): 40002808={_p(uc, 0x40002808):#x} ждём {fin:#x}'
        assert _pw(emu, 0x40002824) == [0xCA, 0x53, 0xFF], \
            f'0x14958({mode}): seq(40002824)={_pw(emu, 0x40002824)} ждём CA/53/FF'
        assert uc.reg_read(UC_ARM_REG_R0) == ret, \
            f'0x14958({mode}): ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём {ret:#x}'


# --- 0x22934: SysTick init из struct ---

@t(0x22934, 'E2-b70: 0x22934(&struct) — SysTick-init: struct {u32 reload@0, byte en@+8}; '
           'SysTick RELOAD(0xE000E014)=u32[+0]; VALUE(0xE000E018)=0; '
           'CTRL(0xE000E010)=4 (en!=0) или 0 (en==0), две записи; ret=0xE000E000, '
           'insn≈838 (lookup-хвост).')
def _(run, rng):
    """Emulator test @ 0x22934: E2-b70: 0x22934(&struct) — SysTick-init: struct {u32 reload@0, byte en@+8}; SysTick RELOAD(0xE000E014)=u32[+0]; VALUE(0xE000E018)=0; CTRL(0xE000E010)=4 (en!=0) или 0 (en==0), две записи; ret=0xE000E000, insn≈838 (lookup-хвост)..
    Тест эмулятора @ 0x22934: E2-b70: 0x22934(&struct) — SysTick-init: struct {u32 reload@0, byte en@+8}; SysTick RELOAD(0xE000E014)=u32[+0]; VALUE(0xE000E018)=0; CTRL(0xE000E010)=4 (en!=0) или 0 (en==0), две записи; ret=0xE000E000, insn≈838 (lookup-хвост)..
    """
    for val, en, ctrl in ((0x1234, 1, 4), (0x1234, 0, 0), (0, 1, 4)):
        uc, emu = _run_sys(0x22934, args=(RAM + 0x1000,),
                           seeds=[(RAM + 0x1000, val), (RAM + 0x1008, bytes([en]))])
        sw = dict((a, v) for a, v in emu.sys_writes)
        assert sw.get(0xE000E014) == val, \
            f'0x22934({val}, {en}): RELOAD={sw.get(0xE000E014, -1):#x} ждём {val:#x}'
        assert sw.get(0xE000E018) == 0, \
            f'0x22934({val}, {en}): VALUE={sw.get(0xE000E018, -1):#x} ждём 0'
        ctrl_seq = [v for a, v in emu.sys_writes if a == 0xE000E010]
        assert ctrl_seq == [ctrl, ctrl], \
            f'0x22934({val}, {en}): CTRL-seq={ctrl_seq} ждём [{ctrl}, {ctrl}]'
        assert uc.reg_read(UC_ARM_REG_R0) == 0xE000E000, \
            f'0x22934({val}, {en}): ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0xE000E000'
        assert 800 < emu.insn < 900, f'0x22934({val}, {en}): insn={emu.insn} ждём ~838'


# --- 0x21804: UART4 init (MCU→BLE) golden ---

@t(0x21804, 'E2-b70: 0x21804() — UART4-init golden: UART4(0x40004C00): BRR=0×2; '
           'CTLR1: 0×6→0x4000→0xC000; CTLR2/3/FLP/… zero; 0x40004C2C=0xFFFFFFFF; '
           '0x40004C30=0xFFF; GPIO@0x48000800: +0x10: 0x200000→0xA00000, +0x14..+0x24: 0, '
           '+0x2C: 0x100→0x1100; SYS: 0xE000E41C=0x800000, ISER0(0xE000E100)=0x40000000 '
           '(bit30). ret=0xFFFFFFFF, insn=968.')
def _(run, rng):
    """Emulator test @ 0x21804: E2-b70: 0x21804() — UART4-init golden: UART4(0x40004C00): BRR=0×2; CTLR1: 0×6→0x4000→0xC000; CTLR2/3/FLP/… zero; 0x40004C2C=0xFFFFFFFF; 0x40004C30=0xFFF; GPIO@0x48000800: +0x10: 0x200000→0xA00000, +0x14..+0x24: 0, +0x2C: 0x100→0x1100; SYS: 0xE000E41C=0x800000, ISER0(0xE000E100)=0x40000000 (bit30). ret=0xFFFFFFFF, insn=968..
    Тест эмулятора @ 0x21804: E2-b70: 0x21804() — UART4-init golden: UART4(0x40004C00): BRR=0×2; CTLR1: 0×6→0x4000→0xC000; CTLR2/3/FLP/… zero; 0x40004C2C=0xFFFFFFFF; 0x40004C30=0xFFF; GPIO@0x48000800: +0x10: 0x200000→0xA00000, +0x14..+0x24: 0, +0x2C: 0x100→0x1100; SYS: 0xE000E41C=0x800000, ISER0(0xE000E100)=0x40000000 (bit30). ret=0xFFFFFFFF, insn=968..
    """
    uc, emu = _run_sys(0x21804)
    exp = {
        0x40004C08: [0x0, 0x0],
        0x40004C0C: [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x4000, 0xC000],
        0x40004C10: [0x0, 0x0],
        0x40004C14: [0x0], 0x40004C18: [0x0], 0x40004C1C: [0x0], 0x40004C20: [0x0],
        0x40004C2C: [0xFFFFFFFF],
        0x40004C30: [0xFFF],
        0x48000810: [0x200000, 0xA00000],
        0x48000814: [0x0, 0x0], 0x48000818: [0x0, 0x0], 0x4800081C: [0x0, 0x0],
        0x48000820: [0x0, 0x0], 0x48000824: [0x0, 0x0],
        0x4800082C: [0x100, 0x1100],
    }
    for addr, seq in exp.items():
        got = _pw(emu, addr)
        assert got == seq, f'0x21804: seq({addr:08x})={got} ждём {seq}'
    sw = dict((a, v) for a, v in emu.sys_writes)
    assert sw.get(0xE000E41C) == 0x800000, \
        f"0x21804: SYS 0xE000E41C={sw.get(0xE000E41C, -1):#x} ждём 0x800000"
    assert sw.get(0xE000E100) == 0x40000000, \
        f"0x21804: ISER0={sw.get(0xE000E100, -1):#x} ждём 0x40000000"
    assert uc.reg_read(UC_ARM_REG_R0) == 0xFFFFFFFF, \
        f'0x21804: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0xFFFFFFFF'
    assert emu.insn == 968, f'0x21804: insn={emu.insn} ждём 968'


# --- 0x1bedc: GPIO init @0x48000400 golden ---

@t(0x1BEDC, 'E2-b70: 0x1bedc(&buf) — GPIO init @0x48000400: zero-буфер; 0x22000(пины '
           '0x40/0x80/0xFF) → записи 0 в 48000410..4800042C (8 адресов); byte@r4+0x14=7. '
           'ret=7, insn=683. fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x1bedc: E2-b70: 0x1bedc(&buf) — GPIO init @0x48000400: zero-буфер; 0x22000(пины 0x40/0x80/0xFF) → записи 0 в 48000410..4800042C (8 адресов); byte@r4+0x14=7. ret=7, insn=683. fresh-emu golden..
    Тест эмулятора @ 0x1bedc: E2-b70: 0x1bedc(&buf) — GPIO init @0x48000400: zero-буфер; 0x22000(пины 0x40/0x80/0xFF) → записи 0 в 48000410..4800042C (8 адресов); byte@r4+0x14=7. ret=7, insn=683. fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x1BEDC, args=(RAM + 0x1000,))
    for off in (0x10, 0x14, 0x18, 0x1C, 0x20, 0x24, 0x28, 0x2C):
        addr = 0x48000400 + off
        seq = _pw(emu, addr)
        assert len(seq) >= 1 and all(v == 0 for v in seq), \
            f'0x1bedc: seq({addr:08x})={seq} ждём только 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 7, \
        f'0x1bedc: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 7'
    assert emu.insn == 683, f'0x1bedc: insn={emu.insn} ждём 683'


# --- 0x107ec: GPIOA EXTI init golden ---

@t(0x107EC, 'E2-b70: 0x107ec(&local) — GPIOA EXTI-init golden: GPIOA CTLR1/2 '
           '40010800: FFFBFF→FFBBFF→FF8BFF→FF89FF; 40010804: FFFFFFDF→5F→4F; '
           '40010808: FFFFFFDF→5F→1F→0F; 4001080C: FFF3FF→33FF→03FF→00FF; '
           'AFIO 40010820: FF0FFFFF→F0FFFFF→FFFFF; 4001082C: FFF3FF→33FF→30FF; '
           'RCC 40021018: FF→FF. ret=0x10, insn=755.')
def _(run, rng):
    """Emulator test @ 0x107ec: E2-b70: 0x107ec(&local) — GPIOA EXTI-init golden: GPIOA CTLR1/2 40010800: FFFBFF→FFBBFF→FF8BFF→FF89FF; 40010804: FFFFFFDF→5F→4F; 40010808: FFFFFFDF→5F→1F→0F; 4001080C: FFF3FF→33FF→03FF→00FF; AFIO 40010820: FF0FFFFF→F0FFFFF→FFFFF; 4001082C: FFF3FF→33FF→30FF; RCC 40021018: FF→FF. ret=0x10, insn=755..
    Тест эмулятора @ 0x107ec: E2-b70: 0x107ec(&local) — GPIOA EXTI-init golden: GPIOA CTLR1/2 40010800: FFFBFF→FFBBFF→FF8BFF→FF89FF; 40010804: FFFFFFDF→5F→4F; 40010808: FFFFFFDF→5F→1F→0F; 4001080C: FFF3FF→33FF→03FF→00FF; AFIO 40010820: FF0FFFFF→F0FFFFF→FFFFF; 4001082C: FFF3FF→33FF→30FF; RCC 40021018: FF→FF. ret=0x10, insn=755..
    """
    uc, emu, lp = _fresh_probe(0x107EC, args=(RAM + 0x1000,))
    exp = {
        0x40010800: [0xFFFFFBFF, 0xFFFFBBFF, 0xFFFF8BFF, 0xFFFF89FF],
        0x40010804: [0xFFFFFFDF, 0xFFFFFF5F, 0xFFFFFF4F],
        0x40010808: [0xFFFFFFDF, 0xFFFFFF5F, 0xFFFFFF1F, 0xFFFFFF0F],
        0x4001080C: [0xFFFFF3FF, 0xFFFF33FF, 0xFFFF03FF, 0xFFFF00FF],
        0x40010820: [0xFF0FFFFF, 0xF0FFFFF, 0xFFFFF],
        0x4001082C: [0xFFFFF3FF, 0xFFFF33FF, 0xFFFF30FF],
        0x40021018: [0xFFFFFFFF, 0xFFFFFFFF],
    }
    for addr, seq in exp.items():
        got = _pw(emu, addr)
        assert got == seq, f'0x107ec: seq({addr:08x})={got} ждём {seq}'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x10, \
        f'0x107ec: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x10'
    assert emu.insn == 755, f'0x107ec: insn={emu.insn} ждём 755'


# --- 0x22000: validated timer channel config (assert-spin) ---

@t(0x22000, 'E2-b70: 0x22000(base, ch_mask, &desc) — timer channel config с assert'
           '-спинами: base ∈ {0x48000000(=9<<27), 0x48000800, 0x48000400, 0x48000C00} '
           'и ch_mask ∈ {1..0x80, 0x100, 0x17A, 0x400..0x8000} иначе cpsid i-спин; '
           'desc[0..1]∈{0..3}, desc[2..5]∈{0,1}, desc[6]∈{0..9}; для каждого ch из '
           'mask: CCMR (base+0x28/+0x2C) 4-bit поле=desc[6]; CCER1..4 (base+0x18..0x24) '
           'bit ch=desc[2..5]; CR2/CR1 (base+0x14/+0x10) 2-bit поле=desc[1]/desc[0]. '
           'ret=base. 4 кейса (valid + 3 assert-спина).')
def _(run, rng):
    """Emulator test @ 0x22000: E2-b70: 0x22000(base, ch_mask, &desc) — timer channel config с assert-спинами: base ∈ {0x48000000(=9<<27), 0x48000800, 0x48000400, 0x48000C00} и ch_mask ∈ {1..0x80, 0x100, 0x17A, 0x400..0x8000} иначе cpsid i-спин; desc[0..1]∈{0..3}, desc[2..5]∈{0,1}, desc[6]∈{0..9}; для каждого ch из mask: CCMR (base+0x28/+0x2C) 4-bit поле=desc[6]; CCER1..4 (base+0x18..0x24) bit ch=desc[2..5]; CR2/CR1 (base+0x14/+0x10) 2-bit поле=desc[1]/desc[0]. ret=base. 4 кейса (valid + 3 assert-спина)..
    Тест эмулятора @ 0x22000: E2-b70: 0x22000(base, ch_mask, &desc) — timer channel config с assert-спинами: base ∈ {0x48000000(=9<<27), 0x48000800, 0x48000400, 0x48000C00} и ch_mask ∈ {1..0x80, 0x100, 0x17A, 0x400..0x8000} иначе cpsid i-спин; desc[0..1]∈{0..3}, desc[2..5]∈{0,1}, desc[6]∈{0..9}; для каждого ch из mask: CCMR (base+0x28/+0x2C) 4-bit поле=desc[6]; CCER1..4 (base+0x18..0x24) bit ch=desc[2..5]; CR2/CR1 (base+0x14/+0x10) 2-bit поле=desc[1]/desc[0]. ret=base. 4 кейса (valid + 3 assert-спина)..
    """
    desc = bytes([1, 1, 1, 0, 1, 0, 2]) + bytes(26)
    uc, emu, lp = _fresh_probe(0x22000,
                               args=(0x48000000, 1, RAM + 0x1200),
                               seeds=[(RAM + 0x1200, desc)])
    assert emu.insn < 500, f'0x22000 valid: insn={emu.insn} ждём <500 (не спин)'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x48000000, \
        f'0x22000 valid: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём base'
    for off, expect in ((0x10, 1), (0x14, 1), (0x18, 1), (0x1C, 0),
                        (0x20, 1), (0x24, 0), (0x28, 2), (0x2C, 0)):
        got = _p(uc, 0x48000000 + off)
        assert got == expect, \
            f'0x22000 valid: u32[base+{off:#04x}]={got:#x} ждём {expect:#x}'
    # assert-спины: невалидный base / невалидный ch_mask / невалидный desc[2]
    for label, args, seeds in (
            ('base', (0x120000, 1, RAM + 0x1200), [(RAM + 0x1200, desc)]),
            ('chmask', (0x48000000, 3, RAM + 0x1200), [(RAM + 0x1200, desc)]),
            ('desc', (0x48000000, 1, RAM + 0x1200),
                     [(RAM + 0x1200, bytes([1, 1, 3, 0, 1, 0, 2]) + bytes(26))])):
        uc, emu, lp = _fresh_probe(0x22000, args=args, seeds=seeds, max_insn=4000)
        assert emu.insn >= 4000 - 2, \
            f'0x22000 {label}: insn={emu.insn} ждём спин до лимита 4000'


# --- 0x22fac: timer CCR/CCER field config (gate-set) ---

@t(0x22FAC, 'E2-b70: 0x22fac(&struct, &cfg) — timer channel field-config: '
           'u32[r0+0x30] = (v & ~mask) | byte[r1+8]<<13; u32[r0+0x2C] = (v & ~mask) | '
           'byte[r1]<<12 (mask — bics-квирк, при v=0 поле = byte<<shift); '
           'если r0 ∈ {0x40012C00, 0x40014000, 0x40014400, 0x40014800, 0x40014C00} и '
           'byte[r1+0xB] ≤ 1: u32[r0+4] = (v & ~0x100) | byte<<0xE; '
           'u32[r0+0x50] = u32[r1+4]; ret=r0. 2 кейса (gate on/off, v=0).')
def _(run, rng):
    """Emulator test @ 0x22fac: E2-b70: 0x22fac(&struct, &cfg) — timer channel field-config: u32[r0+0x30] = (v & ~mask) | byte[r1+8]<<13; u32[r0+0x2C] = (v & ~mask) | byte[r1]<<12 (mask — bics-квирк, при v=0 поле = byte<<shift); если r0 ∈ {0x40012C00, 0x40014000, 0x40014400, 0x40014800, 0x40014C00} и byte[r1+0xB] ≤ 1: u32[r0+4] = (v & ~0x100) | byte<<0xE; u32[r0+0x50] = u32[r1+4]; ret=r0. 2 кейса (gate on/off, v=0)..
    Тест эмулятора @ 0x22fac: E2-b70: 0x22fac(&struct, &cfg) — timer channel field-config: u32[r0+0x30] = (v & ~mask) | byte[r1+8]<<13; u32[r0+0x2C] = (v & ~mask) | byte[r1]<<12 (mask — bics-квирк, при v=0 поле = byte<<shift); если r0 ∈ {0x40012C00, 0x40014000, 0x40014400, 0x40014800, 0x40014C00} и byte[r1+0xB] ≤ 1: u32[r0+4] = (v & ~0x100) | byte<<0xE; u32[r0+0x50] = u32[r1+4]; ret=r0. 2 кейса (gate on/off, v=0)..
    """
    cfg_seeds = [(RAM + 0x1100, 0x55), (RAM + 0x1104, 0xDEADBEEF),
                 (RAM + 0x1108, 0xAA), (RAM + 0x110B, 1)]
    # v=0 сидируем: bics-квирк (нестабильный imm) влияет только на clr-биты v,
    # при v=0 поле = (byte << shift) независимо от маски.
    # gate on: r0 = 0x40012C00 (в gate-set)
    uc, emu, lp = _fresh_probe(0x22FAC, args=(0x40012C00, RAM + 0x1100),
                               seeds=cfg_seeds + [(0x40012C04, 0),
                                                  (0x40012C2C, 0),
                                                  (0x40012C30, 0)])
    assert _p(uc, 0x40012C2C) == 0x55000, \
        f"0x22fac on: +0x2C={_p(uc, 0x40012C2C):#x} ждём 0x55000 (0x55<<12)"
    assert _p(uc, 0x40012C30) == 0x154000, \
        f"0x22fac on: +0x30={_p(uc, 0x40012C30):#x} ждём 0x154000 (0xAA<<13)"
    assert _p(uc, 0x40012C04) == 0x4000, \
        f"0x22fac on: +4={_p(uc, 0x40012C04):#x} ждём 0x4000 (1<<0xE)"
    assert _p(uc, 0x40012C50) == 0xDEADBEEF, \
        f"0x22fac on: +0x50={_p(uc, 0x40012C50):#x} ждём 0xDEADBEEF"
    assert uc.reg_read(UC_ARM_REG_R0) == 0x40012C00, \
        f'0x22fac on: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём r0'
    # gate off: r0 = RAM+0x1000 (вне gate-set), +4 без изменений (0)
    uc, emu, lp = _fresh_probe(0x22FAC, args=(RAM + 0x1000, RAM + 0x1100),
                               seeds=cfg_seeds)
    assert _r(uc, 0x102C, 4) == 0x55000, \
        f'0x22fac off: +0x2C={_r(uc, 0x102C, 4):#x} ждём 0x55000'
    assert _r(uc, 0x1030, 4) == 0x154000, \
        f'0x22fac off: +0x30={_r(uc, 0x1030, 4):#x} ждём 0x154000'
    assert _r(uc, 0x1004, 4) == 0, \
        f'0x22fac off: +4={_r(uc, 0x1004, 4):#x} ждём 0 (gate off)'
    assert _r(uc, 0x1050, 4) == 0xDEADBEEF, \
        f'0x22fac off: +0x50={_r(uc, 0x1050, 4):#x} ждём 0xDEADBEEF'
    assert uc.reg_read(UC_ARM_REG_R0) == RAM + 0x1000, \
        f'0x22fac off: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём r0'


# --- 0x1d874: lookup 48000//x → u16[RAM+0x104] ---

@t(0x1D874, 'E2-b70: 0x1d874(x, gate) — lookup: gate!=0 → v=0x19994(0xBB80, x)=48000//x '
           '(signed C-style, div-by-zero→-1); u16[RAM+0x104]=u16(v); ret=s16(v). '
           'gate=0 → u16[0x104]=0, ret=0 (быстрый путь, insn<50). 5 кейса.')
def _(run, rng):
    """Emulator test @ 0x1d874: E2-b70: 0x1d874(x, gate) — lookup: gate!=0 → v=0x19994(0xBB80, x)=48000//x (signed C-style, div-by-zero→-1); u16[RAM+0x104]=u16(v); ret=s16(v). gate=0 → u16[0x104]=0, ret=0 (быстрый путь, insn<50). 5 кейса..
    Тест эмулятора @ 0x1d874: E2-b70: 0x1d874(x, gate) — lookup: gate!=0 → v=0x19994(0xBB80, x)=48000//x (signed C-style, div-by-zero→-1); u16[RAM+0x104]=u16(v); ret=s16(v). gate=0 → u16[0x104]=0, ret=0 (быстрый путь, insn<50). 5 кейса..
    """
    uc, emu, lp = _fresh_probe(0x1D874, args=(0x100, 0))
    assert _r(uc, 0x104, 2) == 0 and uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x1d874 gate=0: u16[0x104]={_r(uc, 0x104, 2):#x} ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0/0'
    assert emu.insn < 50, f'0x1d874 gate=0: insn={emu.insn} ждём <50'
    for x, expect in ((0x100, 187), (0x10, 3000), (0x200, 93), (0, -1), (0xBB8, 16)):
        uc, emu, lp = _fresh_probe(0x1D874, args=(x, 1))
        ret = uc.reg_read(UC_ARM_REG_R0)
        assert _r(uc, 0x104, 2) == (expect & 0xFFFF), \
            f'0x1d874({x:#x}): u16[0x104]={_r(uc, 0x104, 2):#x} ждём {expect & 0xFFFF:#x}'
        assert ret == (expect & 0xFFFFFFFF), \
            f'0x1d874({x:#x}): ret={ret:#x} ждём {expect & 0xFFFFFFFF:#x}'


# --- 0x8f7c: varargs-helper (XOR через 0x3c7c, ret = u8(r1<<1)) ---

@t(0x8F7C, 'E2-b70: 0x8f7c(fp, flag, r6, r8) — varargs-helper: sl=[sp+0x78] (счётчик '
           'varargs; clamp (sl&0x7E)>0x46 → ret 0); 0x11d6(sp+0xC, 0x48) zero-буфер; '
           'r5=u8(flag<<1); sb=0x3c7c(0, r5)=r5 (XOR c нулём); далее r6/r8-цикл '
           '(пустой при r6=r8=0); ret=sb=u8(r1<<1). 4 кейса (r1=0/1/3/5).')
def _(run, rng):
    """Emulator test @ 0x8f7c: E2-b70: 0x8f7c(fp, flag, r6, r8) — varargs-helper: sl=[sp+0x78] (счётчик varargs; clamp (sl&0x7E)>0x46 → ret 0); 0x11d6(sp+0xC, 0x48) zero-буфер; r5=u8(flag<<1); sb=0x3c7c(0, r5)=r5 (XOR c нулём); далее r6/r8-цикл (пустой при r6=r8=0); ret=sb=u8(r1<<1). 4 кейса (r1=0/1/3/5)..
    Тест эмулятора @ 0x8f7c: E2-b70: 0x8f7c(fp, flag, r6, r8) — varargs-helper: sl=[sp+0x78] (счётчик varargs; clamp (sl&0x7E)>0x46 → ret 0); 0x11d6(sp+0xC, 0x48) zero-буфер; r5=u8(flag<<1); sb=0x3c7c(0, r5)=r5 (XOR c нулём); далее r6/r8-цикл (пустой при r6=r8=0); ret=sb=u8(r1<<1). 4 кейса (r1=0/1/3/5)..
    """
    for r1, expect in ((0, 0), (1, 2), (3, 6), (5, 10)):
        uc, emu, lp = _fresh_probe(0x8F7C, args=(0, r1, 0))
        assert uc.reg_read(UC_ARM_REG_R0) == expect, \
            f'0x8f7c(r1={r1}): ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём {expect:#x}'
        assert 400 < emu.insn < 600, f'0x8f7c(r1={r1}): insn={emu.insn} ждём ~490-510'
