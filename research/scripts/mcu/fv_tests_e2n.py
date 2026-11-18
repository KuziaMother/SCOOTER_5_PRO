# -*- coding: utf-8 -*-
"""E2-b69: напряжение-хендлер 0x1984 (0x87ec()=byte[0xB82]; bit3[0xA72]/капа-3[0xA74]),
flag-хендлер 0x20d8 (bit3[0xA71] → счётчик[0xA7A] капа 5 → 0xaf94+0x2a5c+clr bit3[0xA72]),
счётчик-гейт 0x42b8 (byte[0x102]; XOR 0x87c8(GPIOB CRL, 0x800); byte[0x118] капа 5 → 0x8A=1;
u16[0x116] капа 0x3E8), permission-гейт 0x4630 (byte[0xA65]/0xA66, state 0x89 ∈ {2,3},
0x8e14()=byte[0x1378], XOR 0x100B GPIOA CRH), I2C2-poll 0x5274 (гейты 0xA65/0xF71, reg 0x93,
state 0x93), GPIO batch-конфигуратор 0x332c (u32[desc+7] ∈ 6 тегов, 0x85c8/0x2bbc/0x59a4/0xc0b4),
frame-парсеры 0x3838 (CRC-16 табл. 0x19784, BE-поле, magic 0x90) и 0x54dc (sum-гейт mod 256,
инверсия frame[2]), I2C-прединит 0x5a38 (u16[0xF10..0xF28]=0x12C), NVIC IRQ3 0x58b0
(AFIO 0x40010400..+0x14 + ISER0=8), телеметрия-init 0x51d8 (u16[0xF10..]=0xE10, zero 0xF70..0xFBB),
charger-detect 0x3668 и poll 0x4de0 (I2C-ret 0x10)."""
# ruff: noqa: F405  (имена из star-import от fv_core)
from fv_core import *  # noqa: F401,F403

import os
import struct

from emulator.mcu_emu import PERIPH  # noqa: E402
from unicorn import UcError, UC_HOOK_CODE  # noqa: E402
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP, \
    UC_ARM_REG_LR  # noqa: E402

_IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '..', '..', 'images', 'mcu_0007.bin')
_FW = open(_IMG, 'rb').read()

# --- CRC-16 (таблица 0x19784, init 0) — идентичен 0x3c4c / 0x38ec ---
_CRC_TBL = [struct.unpack_from('<H', _FW, 0x19784 + 2 * i)[0] for i in range(256)]


def _crc16(buf):
    crc = 0
    for b in buf:
        crc = (_CRC_TBL[b ^ (crc >> 8)] ^ (crc << 8)) & 0xFFFF
    return crc


def _fresh_probe(off, seeds=(), args=(), max_insn=50000):
    """Fresh-emu: чистый RAM, 0xFF PERIPH, seeds, args; возвращает (uc, emu, lastpc)."""
    emu = McuEmu(max_insn=max_insn)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))
    emu.hook_periph_ready()
    for addr, val in seeds:
        uc.mem_write(addr, bytes(val) if isinstance(val, (bytes, bytearray))
                     else struct.pack('<I', val))
    for i, a in enumerate(args):
        uc.reg_write((UC_ARM_REG_R0, UC_ARM_REG_R1)[i], a)
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


def _p(uc, off, size=4):
    return int.from_bytes(bytes(uc.mem_read(off, size)), 'little')


# --- 0x1984: напряжение-хендлер (0x87ec() = byte[0xB82]) ---

@t(0x1984, 'E2-b69: 0x1984() — напряжение-хендлер: v=0x87ec()=byte[0xB82]. v==0: '
           'byte[0xA74]=0, byte[0xA72]|=8 (set bit3). v!=0: bit3[0xA72]==0 → byte[0xA74]=0; '
           'иначе byte[0xA74]++, если >=3 → byte[0xA74]=0 и byte[0xA72]&=~8. Tail: '
           'bit3[0xA72]==0 → bl 0x8b58+0x8b10 (motor-off, ~700 insn) → ret=0; иначе ret=1. '
           '3 кейса (v=0 / inc / капа+clr).')
def _(run, rng):
    # A: fresh, v=0
    uc, emu, lp = _fresh_probe(0x1984)
    assert _r(uc, 0xA72) == 8, f'0x1984 A: byte[0xA72]={_r(uc, 0xA72)} ждём 8'
    assert _r(uc, 0xA74) == 0, f'0x1984 A: byte[0xA74]={_r(uc, 0xA74)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x1984 A: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 1'
    # B: v=5, bit3=1, counter=1 → inc
    uc, emu, lp = _fresh_probe(0x1984,
                               seeds=[(RAM + 0xB82, 5), (RAM + 0xA72, 8),
                                      (RAM + 0xA74, 1)])
    assert _r(uc, 0xA74) == 2, f'0x1984 B: byte[0xA74]={_r(uc, 0xA74)} ждём 2'
    assert _r(uc, 0xA72) == 8, f'0x1984 B: byte[0xA72]={_r(uc, 0xA72)} ждём 8'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x1984 B: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 1'
    # C: v=5, bit3=1, counter=3 → капа → сброс + clr bit3 + motor-off tail
    uc, emu, lp = _fresh_probe(0x1984,
                               seeds=[(RAM + 0xB82, 5), (RAM + 0xA72, 8),
                                      (RAM + 0xA74, 3)])
    assert _r(uc, 0xA74) == 0, f'0x1984 C: byte[0xA74]={_r(uc, 0xA74)} ждём 0 (капа)'
    assert _r(uc, 0xA72) == 0, f'0x1984 C: byte[0xA72]={_r(uc, 0xA72)} ждём 0 (clr bit3)'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x1984 C: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 0 (motor-off tail)'
    assert emu.insn > 500, f'0x1984 C: tail ждём длинный, insn={emu.insn}'


# --- 0x20d8: flag-хендлер (bit3[0xA71] → счётчик[0xA7A] капа 5) ---

@t(0x20D8, 'E2-b69: 0x20d8() — flag-хендлер: bit3[0xA71]==0 → byte[0xA7A]=0, ret=0. '
           'bit3==1: c=byte[0xA7A]+1 (uxtb); c<5 → ret=c; c>=5: byte[0xA7A]=0, '
           'bl 0xaf94(0xDD8), delay 0x1F4, bl 0x2a5c (I2C, ~16K insn, ret 0x10); '
           '0x2a5c()!=0 → byte[0xA72]&=~8; ret=0x10. 4 кейса (clr/inc/capa/I2C-tail).')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x20D8)
    assert _r(uc, 0xA7A) == 0, f'0x20d8 A: byte[0xA7A]={_r(uc, 0xA7A)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x20d8 A: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 0'
    assert emu.insn < 50, f'0x20d8 A: быстрый путь ждём, insn={emu.insn}'
    uc, emu, lp = _fresh_probe(0x20D8, seeds=[(RAM + 0xA71, 8)])
    assert _r(uc, 0xA7A) == 1, f'0x20d8 B: byte[0xA7A]={_r(uc, 0xA7A)} ждём 1'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x20d8 B: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 1 (счётчик)'
    uc, emu, lp = _fresh_probe(0x20D8,
                               seeds=[(RAM + 0xA71, 8), (RAM + 0xA7A, 4),
                                      (RAM + 0xA72, 8)],
                               max_insn=50000)
    assert _r(uc, 0xA7A) == 0, f'0x20d8 C: byte[0xA7A]={_r(uc, 0xA7A)} ждём 0 (капа)'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x10, \
        f'0x20d8 C: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x10 (0x2a5c)'
    assert emu.insn > 10000, f'0x20d8 C: I2C-tail ждём, insn={emu.insn}'


# --- 0x42b8: счётчик-гейт (byte[0x102], XOR 0x87c8, капы 5/0x3E8) ---

@t(0x42B8, 'E2-b69: 0x42b8() — счётчик-гейт: byte[0x102]!=1 → u16[0x116]=0, byte[0x118]=0, '
           'ret=0. byte[0x102]==1: C=0x87c8(0x40010C00, 0x800) — чексумма 256 байт PERIPH '
           '(XOR + 8-шаговый бит-микс; 0x00×256→0, 0xFF×256→0xFA); C!=0 → byte[0x118]++, '
           '>5 → byte[0x118]=0, byte[0x8A]=1, byte[0x102]=0; u16[0x116]++, >0x3E8 → '
           'u16[0x116]=0, byte[0x8A]=0, byte[0x102]=0; ret = u16[0x116] (или 0 после капы). '
           '5 кейса (гейт off / chk=0 / chk!=0 / капы).')
def _(run, rng):
    # A: гейт off (byte[0x102]=0) — сброс/бездействие
    uc, emu, lp = _fresh_probe(0x42B8)
    assert _r(uc, 0x116, 2) == 0 and _r(uc, 0x118) == 0, '0x42b8 A: сброс ждём'
    assert uc.reg_read(UC_ARM_REG_R0) == 0,         f'0x42b8 A: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 0'
    # B: гейт on, chk=0 (0x00*256) -> byte[0x118] не инкрементится
    uc, emu, lp = _fresh_probe(0x42B8,
                               seeds=[(RAM + 0x102, 1),
                                      (PERIPH + 0x10C00, bytes(256))])
    assert _r(uc, 0x116, 2) == 1, f'0x42b8 B: u16[0x116]={_r(uc, 0x116, 2)} ждём 1'
    assert _r(uc, 0x118) == 0, f'0x42b8 B: byte[0x118]={_r(uc, 0x118)} ждём 0 (chk=0)'
    assert uc.reg_read(UC_ARM_REG_R0) == 1,         f'0x42b8 B: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 1'
    # C: гейт on, chk=0xFA (0xFF*256, дефолт hook_periph_ready) -> byte[0x118]++
    uc, emu, lp = _fresh_probe(0x42B8, seeds=[(RAM + 0x102, 1)])
    assert _r(uc, 0x118) == 1, f'0x42b8 C: byte[0x118]={_r(uc, 0x118)} ждём 1 (chk=0xFA)'
    assert _r(uc, 0x116, 2) == 1, f'0x42b8 C: u16[0x116]={_r(uc, 0x116, 2)} ждём 1'
    assert uc.reg_read(UC_ARM_REG_R0) == 1,         f'0x42b8 C: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 1'
    # D: капа byte[0x118] (chk!=0 -> 5->6)
    uc, emu, lp = _fresh_probe(0x42B8,
                               seeds=[(RAM + 0x102, 1), (RAM + 0x118, 5)])
    assert _r(uc, 0x118) == 0, f'0x42b8 D: byte[0x118]={_r(uc, 0x118)} ждём 0 (капа)'
    assert _r(uc, 0x8A) == 1, f'0x42b8 D: byte[0x8A]={_r(uc, 0x8A)} ждём 1'
    assert _r(uc, 0x102) == 0, f'0x42b8 D: byte[0x102]={_r(uc, 0x102)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 1,         f'0x42b8 D: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 1 (u16=1)'
    # E: капа u16[0x116] 0x3E8 (chk=0, byte[0x118] без влияния)
    uc, emu, lp = _fresh_probe(0x42B8,
                               seeds=[(RAM + 0x102, 1),
                                      (RAM + 0x116, struct.pack('<H', 0x3E8)),
                                      (PERIPH + 0x10C00, bytes(256))])
    assert _r(uc, 0x116, 2) == 0,         f'0x42b8 E: u16[0x116]={_r(uc, 0x116, 2)} ждём 0 (капа 0x3E8)'
    assert _r(uc, 0x8A) == 0 and _r(uc, 0x102) == 0, '0x42b8 E: сброс флагов ждём'
    assert uc.reg_read(UC_ARM_REG_R0) == 0,         f'0x42b8 E: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 0'


# --- 0x4630: permission-гейт (0xA65/0xA66, state 0x89, 0x8e14, XOR GPIOA) ---

@t(0x4630, 'E2-b69: 0x4630() — permission-гейт: byte[0xA65]=1; если byte[0x89] ∈ {2,3} и '
           'byte[0x107]==1 и 0x8e14()=byte[0x1378]==0 → byte[0xA66]=1, иначе 0; затем '
           '0xA66==1|byte[0x3E]==1|byte[0x36]==0|0xa6a4()==1 → 0xA66=0; и '
           'byte[0x3D]==1|byte[0x3E]==1|byte[0x36]==0|flash[0x2000]==1 → 0xA65=0, '
           'иначе 0x87c8(0x40010800, 0x100)!=0 (XOR PERIPH) → 0xA65 остаётся 1, ret=1; '
           'иначе 0xA65=0, ret=0. 3 кейса (fresh / step2-проход / keep-1).')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x4630)
    assert _r(uc, 0xA65) == 0 and _r(uc, 0xA66) == 0, '0x4630 A: сброс ждём'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x4630 A: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 0'
    assert emu.insn == 44, f'0x4630 A: insn={emu.insn} ждём 44'
    uc, emu, lp = _fresh_probe(0x4630,
                               seeds=[(RAM + 0x89, 2), (RAM + 0x107, 1),
                                      (RAM + 0x1378, 0)])
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x4630 B: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 0'
    assert emu.insn == 50, \
        f'0x4630 B: insn={emu.insn} ждём 50 (step2-ветка, 0xA66=1 транз.)'
    assert _r(uc, 0xA66) == 0, '0x4630 B: финал 0xA66=0 (group3-сброс)'
    uc, emu, lp = _fresh_probe(0x4630,
                               seeds=[(RAM + 0x36, 1), (PERIPH + 0x10800, 0xFE)])
    assert _r(uc, 0xA65) == 1, f'0x4630 C: byte[0xA65]={_r(uc, 0xA65)} ждём 1 (keep)'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x4630 C: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 1'


# --- 0x5274: I2C2-poll reg 0x93 (гейты 0xA65/0xF71) ---

@t(0x5274, 'E2-b69: 0x5274() — I2C2-poll (dev 0x3E, reg 0x93): r4=1; если byte[0xA65]==1 '
           'и byte[0xF71]&1==0 → 0x9438 + 0xbf58 + delay 0x1F4 + 0x1c60(0x7F, 8) + '
           'bfi → byte[0xF71]=0x93, ret=0x10; иначе если byte[0xF71]&1 → 0x1bdc(0x93) + '
           'delay → u16[0xF70]=0, ret=r4=... (0x10); иначе ret=0. 3 кейса (off/on/state).')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x5274)
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x5274 A: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 0'
    assert emu.insn < 50, f'0x5274 A: быстрый путь ждём, insn={emu.insn}'
    uc, emu, lp = _fresh_probe(0x5274, seeds=[(RAM + 0xA65, 1)], max_insn=20000)
    assert uc.reg_read(UC_ARM_REG_R0) == 0x10, \
        f'0x5274 B: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x10'
    assert emu.insn > 500, f'0x5274 B: I2C-путь ждём, insn={emu.insn}'
    uc, emu, lp = _fresh_probe(0x5274, seeds=[(RAM + 0xF71, 1)], max_insn=20000)
    assert uc.reg_read(UC_ARM_REG_R0) == 0x10, \
        f'0x5274 C: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x10'
    assert emu.insn > 500, f'0x5274 C: 0x1bdc-путь ждём, insn={emu.insn}'


# --- 0x332c: GPIO batch-конфигуратор (descriptor 24B) ---

@t(0x332C, 'E2-b69: 0x332c(descs, count) — GPIO batch-конфигуратор: ret=1; для каждого '
           'desc: u32[desc+7] ∈ {0x10110000..0x10320000} (6 тегов) → bl 0x163b4(port), '
           'u16[desc+4]==0x800 и port==0x40010C00 → sp14=byte[desc+6] (иначе 0), '
           'bl 0x85c8(port, val) — GPIO config (CR/ODR), bl 0x2bbc (EXTI), '
           'тег 0x10x1 → prio 8 / 0x10x2 → 0xC / иначе 0x10, bl 0x59a4(sp+8) — NVIC, '
           'byte[sp+4..6]=desc[0x11..0x13], bl 0xc0b4 (ISER0 |= 1<<(irq>>5)); '
           'иначе else-ветка (sp13/14, 0x85c8, 0x87e2 для тегов 1/0x11). Кейс B: '
           'desc = GPIOB CRL + 0x0800 + tег 0x10110000 + IRQ3 → ISER0=0x8, '
           'CRL=0xFF3FFFFF, ODR=0xFFFFF7FF, CRH=0xFF7FFFFF, APB2RSTR|=0x2000. ret=1.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x332C, args=(RAM + 0x3000, 0))
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x332c A: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 1 (count=0)'
    desc = bytearray(24)
    struct.pack_into('<I', desc, 0, 0x40010C00)
    struct.pack_into('<H', desc, 4, 0x0800)
    desc[6] = 0x05
    struct.pack_into('<I', desc, 7, 0x10110000)
    desc[0x11] = 3
    uc, emu, lp = _fresh_probe(0x332C, seeds=[(RAM + 0x3000, bytes(desc))],
                               args=(RAM + 0x3000, 1))
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x332c B: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 1'
    assert _p(uc, 0xE000E100) == 0x8, \
        f'0x332c B: ISER0={_p(uc, 0xE000E100):#x} ждём 0x8 (IRQ3)'
    assert _p(uc, 0x40010C00) == 0xFF3FFFFF, \
        f'0x332c B: CRL={_p(uc, 0x40010C00):#x} ждём 0xFF3FFFFF'
    assert _p(uc, 0x40010C08) == 0xFFFFF7FF, \
        f'0x332c B: ODR={_p(uc, 0x40010C08):#x} ждём 0xFFFFF7FF'
    assert _p(uc, 0x40010C0C) == 0xFF7FFFFF, \
        f'0x332c B: CRH={_p(uc, 0x40010C0C):#x} ждём 0xFF7FFFFF'
    assert _p(uc, 0x4001000C) == 0xFFFFDFFF, \
        f'0x332c B: APB2RSTR={_p(uc, 0x4001000C):#x} ждём 0xFFFFDFFF'


# --- 0x3838: frame-парсер (CRC-16 0x19784, magic 0x90) ---

@t(0x3838, 'E2-b69: 0x3838(frame, len) — frame-парсер: u16 len ∈ [6, 0x82] (иначе 0); '
           'frame[2..5] → RAM+0x10B8..+0x10BB (P); target16 = (frame[len]<<8)|frame[len+1] '
           '(BE-поле, хранится hi→lo); crc = 0x3c4c(frame+2, len-2) = CRC-16 (табл. 0x19784, '
           'init 0); accept при crc==target16 и frame[5]<0x96 и frame[2]==0x90 и '
           'frame[3] ∈ {0x10, 3} → memcpy count=frame[5] из frame+6 → P+4, ret=1; '
           'иначе ret=0. 3 кейса (accept/badcrc/len).')
def _(run, rng):
    def mk(crc_ok=True):
        f = bytearray(12)
        f[0] = 8
        f[2], f[3], f[4], f[5] = 0x90, 0x10, 0x00, 0x01
        f[6], f[7] = 0xAA, 0xBB
        c = _crc16(f[2:8])
        f[8], f[9] = (c >> 8) & 0xFF, c & 0xFF
        if not crc_ok:
            f[9] ^= 0xFF
        return bytes(f)
    good, bad = mk(True), mk(False)
    uc, emu, lp = _fresh_probe(0x3838, seeds=[(RAM + 0x4000, good)],
                               args=(RAM + 0x4000, 8))
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x3838 A: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 1'
    P = 0x10B8
    got = bytes(uc.mem_read(RAM + P, 7))
    assert got[:7] == bytes([0x90, 0x10, 0x00, 0x01, 0xAA, 0x00, 0x00]), \
        f'0x3838 A: P+0..6={got.hex(" ")} ждём 90 10 00 01 aa 00 00'
    uc, emu, lp = _fresh_probe(0x3838, seeds=[(RAM + 0x4000, bad)],
                               args=(RAM + 0x4000, 8))
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x3838 B: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 0 (badcrc)'
    uc, emu, lp = _fresh_probe(0x3838, args=(RAM + 0x4000, 5))
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x3838 C: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 0 (len=5)'


# --- 0x54dc: frame-парсер-вариант (sum mod 256 + инверсия) ---

@t(0x54DC, 'E2-b69: 0x54dc(frame, len) — frame-парсер-вариант: u16 len ∈ [4, 0x28] '
           '(иначе 0); 0x11d6(P=RAM+0x11F3, 0x2F) zero; frame[2..4] → P+1..P+3, '
           'len!=4 → P+0=0x10; count=frame[4] ≤ 0x28; memcpy count из frame+5 → P+5; '
           'tail: frame[7] → P+0x2D, frame[8] → P+0x2E; r7=0x1e34(frame+2, len-2)='
           'sum(frame[2..len-1]) mod 256; accept при byte[P+0x2D]==r7 (т.е. '
           'sum(frame[2..6])≡0, frame[7]==r7) и byte[P+0x2E]==0xFF-frame[2] → ret=1, '
           'иначе 0. 3 кейса (accept/len<4/len>0x28).')
def _(run, rng):
    g = bytearray(10)
    g[0] = 8
    g[2], g[3], g[4], g[5], g[6] = 0x10, 0x20, 0x02, 0x30, 0x9E
    assert (sum(g[2:7]) & 0xFF) == 0
    g[7] = 0x55
    g[8] = 0xEF
    uc, emu, lp = _fresh_probe(0x54DC, seeds=[(RAM + 0x4100, bytes(g))],
                               args=(RAM + 0x4100, 8))
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x54dc A: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 1'
    Pg = 0x11F3
    got = bytes(uc.mem_read(RAM + Pg, 9))
    assert got == bytes([0x10, 0x10, 0x20, 0x02, 0x00, 0x30, 0x9E, 0x00, 0x00]), \
        f'0x54dc A: Pg+0..8={got.hex(" ")}'
    assert _r(uc, Pg + 0x2D) == 0x55 and _r(uc, Pg + 0x2E) == 0xEF, \
        f'0x54dc A: tail={_r(uc, Pg + 0x2D):#x}/{_r(uc, Pg + 0x2E):#x} ждём 55/EF'
    uc, emu, lp = _fresh_probe(0x54DC, args=(RAM + 0x4100, 3))
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x54dc B: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 0 (len=3)'
    uc, emu, lp = _fresh_probe(0x54DC, args=(RAM + 0x4100, 0x29))
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x54dc C: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 0 (len=0x29)'


# --- 0x5a38: I2C-прединит (0x15588 + 0x5134 + 0x109c4) ---

@t(0x5A38, 'E2-b69: 0x5a38() — I2C-прединит (396 insn, ret=1): byte[0x80]=2; '
           'u16[0xF10..0xF28]=0x12C×13; u32[0xF2C]=0xF3C; u16[0xF30..0xF34]=0x12C×3; '
           'byte[0xF36]=byte[0xF37]=1; u32[0xF95]=0xF3C; u16[0xF99..0xF9D]=0x12C×3; '
           'byte[0xF9F]=byte[0xFA0]=1. fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x5A38)
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x5a38: ret={uc.reg_read(UC_ARM_REG_R0)} ждём 1'
    assert _r(uc, 0x80) == 2, f'0x5a38: byte[0x80]={_r(uc, 0x80)} ждём 2'
    for off in range(0xF10, 0xF2A, 2):
        assert _r(uc, off, 2) == 0x12C, \
            f'0x5a38: u16[{off:#x}]={_r(uc, off, 2):#x} ждём 0x12C'
    assert _p(uc, RAM + 0xF2C) == 0xF3C, \
        f'0x5a38: u32[0xF2C]={_p(uc, RAM + 0xF2C):#x} ждём 0xF3C'
    for off in (0xF30, 0xF32, 0xF34):
        assert _r(uc, off, 2) == 0x12C, \
            f'0x5a38: u16[{off:#x}] ждём 0x12C'
    assert _r(uc, 0xF36) == 1 and _r(uc, 0xF37) == 1, '0x5a38: byte[0xF36/0xF37] ждём 1'
    assert _p(uc, RAM + 0xF95) == 0xF3C, \
        f'0x5a38: u32[0xF95]={_p(uc, RAM + 0xF95):#x} ждём 0xF3C'
    for off in (0xF99, 0xF9B, 0xF9D):
        assert _r(uc, off, 2) == 0x12C, \
            f'0x5a38: u16[{off:#x}] ждём 0x12C'
    assert _r(uc, 0xF9F) == 1 and _r(uc, 0xFA0) == 1, '0x5a38: byte[0xF9F/0xFA0] ждём 1'


# --- 0x58b0: NVIC IRQ3 (AFIO + ISER) ---

@t(0x58B0, 'E2-b69: 0x58b0() — NVIC IRQ3-setup (91 insn): 0x5970(0x100000) + struct '
           '{0x100000, 0, 8, 1} → 0x59a4; golden: AFIO 0x40010400=0xFFFFFFFF, '
           '0x40010404=0xFFEFFFFF, 0x40010408=0xFFFFFFFF, 0x4001040C=0xFFEFFFFF, '
           '0x40010414=0x100000; ICER0(0xE000E180) str 0x8; ret=0x20017FE8 '
           '(STACK_TOP-0x18, mусорный tail). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x58B0)
    assert _p(uc, 0x40010400) == 0xFFFFFFFF, \
        f'0x58b0: [0x40010400]={_p(uc, 0x40010400):#x} ждём 0xFFFFFFFF'
    assert _p(uc, 0x40010404) == 0xFFEFFFFF, \
        f'0x58b0: [0x40010404]={_p(uc, 0x40010404):#x} ждём 0xFFEFFFFF'
    assert _p(uc, 0x40010408) == 0xFFFFFFFF, \
        f'0x58b0: [0x40010408]={_p(uc, 0x40010408):#x} ждём 0xFFFFFFFF'
    assert _p(uc, 0x4001040C) == 0xFFEFFFFF, \
        f'0x58b0: [0x4001040C]={_p(uc, 0x4001040C):#x} ждём 0xFFEFFFFF'
    assert _p(uc, 0x40010414) == 0x100000, \
        f'0x58b0: [0x40010414]={_p(uc, 0x40010414):#x} ждём 0x100000'
    assert _p(uc, 0xE000E180) == 0x8, \
        f'0x58b0: ICER0={_p(uc, 0xE000E180):#x} ждём 0x8'
    assert uc.reg_read(UC_ARM_REG_R0) == STACK_TOP - 0x18, \
        f'0x58b0: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём {STACK_TOP - 0x18:#x}'


# --- 0x51d8: телеметрия-init ---

@t(0x51D8, 'E2-b69: 0x51d8() — телеметрия-init (994 insn, ret=0x2710): '
           'byte[0x44]=byte[0x45]=0x19; u16[0xF10..0xF28]=0xE10×13; zero-clear '
           'byte[0xF70..0xFBB] (108 B, финал — str 4B @0xFBB). fresh-emu golden.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x51D8)
    assert uc.reg_read(UC_ARM_REG_R0) == 0x2710, \
        f'0x51d8: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x2710'
    assert _r(uc, 0x44) == 0x19 and _r(uc, 0x45) == 0x19, \
        f'0x51d8: byte[0x44/0x45]={_r(uc, 0x44):#x}/{_r(uc, 0x45):#x} ждём 0x19'
    for off in range(0xF10, 0xF2A, 2):
        assert _r(uc, off, 2) == 0xE10, \
            f'0x51d8: u16[{off:#x}]={_r(uc, off, 2):#x} ждём 0xE10'
    z = bytes(uc.mem_read(RAM + 0xF70, 0xFBB - 0xF70 + 1))
    assert all(b == 0 for b in z), '0x51d8: zero-clear 0xF70..0xFBB ждём'


# --- 0x3668: charger-detection (I2C ret 0x10) ---

@t(0x3668, 'E2-b69: 0x3668() — charger-detection (584 insn): 0x8afc() + I2C-машина '
           '0x908c против 0xFF-периферии → det=0x10; все записи — только локальный '
           'стек (I2C-структуры), без RAM/PERIPH-побочных эффектов в fresh-состоянии. '
           'ret=0x10. fresh-emu smoke+ret.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x3668)
    assert uc.reg_read(UC_ARM_REG_R0) == 0x10, \
        f'0x3668: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x10'
    assert emu.insn == 584, f'0x3668: insn={emu.insn} ждём 584'


# --- 0x4de0: poll 0x1bdc(0x93)&0x1bdc(0x94) (I2C ret 0x10) ---

@t(0x4DE0, 'E2-b69: 0x4de0() — poll (574 insn): 0x1bdc(0x93) & 0x1bdc(0x94) + delay 0x1F4 '
           'через I2C-машину 0x908c (dev 0x3E); fresh 0xFF-периферия → детерминированный '
           'путь, все записи — только локальный стек; ret=0x10. fresh-emu smoke+ret.')
def _(run, rng):
    uc, emu, lp = _fresh_probe(0x4DE0)
    assert uc.reg_read(UC_ARM_REG_R0) == 0x10, \
        f'0x4de0: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x10'
    assert emu.insn == 574, f'0x4de0: insn={emu.insn} ждём 574'
