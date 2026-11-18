# -*- coding: utf-8 -*-
"""E2-b67: u64-кластер (0x19dbc fixed-point micro-engine, 0x19e8c u64→float,
0x1a184 LSL-norm), TLV-декодер 0xbe6c (CRC-16 0x19784), frame-экстрактор 0xbd50
(L1=RAM+0x1154), consumer 0x4b04 (0x4a04+0x12d04+0x4a4c), FLASH erase core 0x6230
(SCBR |= 0x7C → 0x6284-декодер → 0x6390 delay), NVIC IRQ enable 0xc0b4
(IPR 0xE000E400+irq, ISER 0xE000E100+irq>>3), timer IRQ 0x1a2a4 (гейт bit7 SR),
buffer manager 0xee48 (counter clamp 0x7F), overheat pre-stage 0x1b67c
(s16-вычисление + blx flash-таблицы 0xA8C8), response encoder 0x56bc
(0x74-кадр, «OK» ASCII, chk 0x1e34, 25B-блок из RAM+0xCB3)."""
# ruff: noqa: F405  (имена из star-import от fv_core)
from fv_core import *  # noqa: F401,F403
from fv_core import _fresh_call, _intercept  # noqa: F401

import struct

from emulator.mcu_emu import PERIPH  # noqa: E402


# --- u64 fixed-point micro-engine (16B блок на стеке + tail 0x1a184) ---
_19DBC_CASES = [
    ((1, 0, 1, 0), 0x0, 0x0, '01000000000020000000000000010000'),
    ((1, 1, 1, 1), 0x0, 0x0, '01000000020020000100200000010000'),
    ((0x1234, 0x5678, 0x9ABC, 0xDEF0), 0x0, 0x0,
     '30a6000be0d81d138b20cda113010000'),
    ((0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF), 0xFFFFFFFE, 0xC00FFFFF,
     '010000000000c0ffffffffffff030000'),
    ((0x80000001, 0x80000002, 3, 4), 0x0, 0x0,
     '030000800b0040000a00680000010000'),
    ((5, 6, 7, 8), 0x0, 0x0, '230000005200c0003000e00000010000'),
    ((1, 0, 0xFFFFFFFF, 0xFFFFFFFF), 0x0, 0xC0100000,
     'ffffffffffff0f000000000000020000'),
    ((0xFFFFFFFF, 0xFFFFFFFF, 1, 0), 0x0, 0xC0100000,
     'ffffffffffff0f000000000000020000'),
    ((2, 3, 4, 5), 0x0, 0x0, '08000000160060000f00800000010000'),
    ((0x100, 0x200, 0x300, 0x400), 0x0, 0x0,
     '0000030000000a400000086000010000'),
]


def _run_19dbc(_run, _rng):
    for args, e0, e1, blk in _19DBC_CASES:
        r0, emu = _fresh_call(0x19DBC, args, max_insn=200000)
        r1 = emu.uc.reg_read(UC_ARM_REG_R1)
        got = bytes(emu.uc.mem_read(STACK_TOP - 0x78, 16)).hex()
        assert (r0, r1) == (e0, e1), (
            f'0x19dbc {args}: ({r0:#x},{r1:#x}) ждём ({e0:#x},{e1:#x})')
        assert got == blk, f'0x19dbc {args}: блок {got} ждём {blk}'


@t(0x19DBC, 'E2-b67: 0x19dbc(a0,a1,a2,a3) — u64 fixed-point micro-engine: sign=sb(a1)^sb(a3), '
            'abs(a1)/abs(a3), гейты (a2|a3)/(a0|a1)→(0,0); 16B-блок на стеке (STACK_TOP-0x78): '
            'sign/0x0BADF001/sum(pool 0x19E88=0xFFFFFC0D)/продукт u16[2..]-слайды; tail bl 0x1a184. '
            'const-calc 10 кейсов (детерм.)')
def _(run, rng):
    _run_19dbc(run, rng)


# --- 0x19e8c: u64 → float (r1 = IEEE-биты) ---
_19E8C_CASES = [
    ((1, 0, 0, 0), 0x0, 0x0),
    ((0x1000000, 0x1, 0x1000000, 0), 0xFFFFFFF0, 0x3FF00000),
    ((0x1000000, 0, 0x800000, 0), 0x800000, 0x3FF00000),
    ((5, 0, 0, 0), 0x0, 0x0),
    ((0x12345678, 0, 0, 0), 0x0, 0x0),
    ((0xFFFFFFFF, 0, 0, 0), 0x0, 0x0),
    ((0, 1, 0, 0), 0x0, 0x0),
    ((0, 0xFFFFFFFF, 0, 0), 0x0, 0x0),
    ((1, 0, 1, 0), 0x0, 0x3FF00000),
    ((1, 0, 0xFFFFFFFF, 0xFFFFFFFF), 0x0, 0x0),
    ((0x1000000, 0x80000000, 0x80000000, 0), 0x020007F0, 0xBFEFFFFF),
    ((0x80000000, 0x80000000, 0x1000000, 0), 0x7EFFFFF8, 0xBFF00000),
    ((0x2000000, 0x2, 0x1000000, 0), 0xFFFFE0, 0x3FF00002),
    ((0x1000000, 0x4, 0x1000000, 0), 0xFFFFFFC0, 0x3FF00003),
    ((0x1000000, 0, 0x1000000, 0), 0x0, 0x3FF00000),
]


@t(0x19E8C, 'E2-b67: 0x19e8c(a0,a1,a2,a3) — u64 → float: sign=sb(a1)^sb(a3) → IEEE-биты в r1 '
            '(0x3FF00000=2.0, 0xBFEFFFFF≈-2.0+ε, 0x3FF00002/3 — малые мантиссы); r0 = коррекция. '
            'const-calc 15 кейсов (детерм.)')
def _(run, rng):
    for args, e0, e1 in _19E8C_CASES:
        r0, emu = _fresh_call(0x19E8C, args, max_insn=200000)
        r1 = emu.uc.reg_read(UC_ARM_REG_R1)
        assert (r0, r1) == (e0, e1), (
            f'0x19e8c {args}: ({r0:#x},{r1:#x}) ждём ({e0:#x},{e1:#x})')


# --- 0x1a184: u64 LSL with normalization ---
_1A184_CASES = [
    ((1, 0), 0x0, 0x0),
    ((5, 0), 0x0, 0x0),
    ((0x12345678, 0), 0x0, 0x0),
    ((0xFFFFFFFF, 0), 0x0, 0x0),
    ((0, 1), 0x0, 0x0),
    ((0xF4240, 1), 0x0, 0x0),
    ((0x80000000, 0), 0x0, 0x0),
    ((7, 3), 0x0, 0x0),
    ((0x1000000, 0x20), 0x0, 0x0),
    ((0x1000000, 0x1F4), 0x0, 0x0),
    ((0, 0), 0x0, 0x0),
    ((0x80000000, 0x20), 0x0, 0x0),
    ((1, 0x40), 0x0, 0x0),
    ((0x40000000, 1), 0x0, 0x0),
    ((0xFFFFFFFF, 0xFFFFFFFF), 0x0, 0xC00000),
]


@t(0x1A184, 'E2-b67: 0x1a184(a0,a1) — u64 LSL с нормализацией: count=0x21b24(a1|a1==0→0x20+0x20); '
            'S=(a1:a0)<<count; zero-гейты; R=(a1:a0)>>(0x40-count) + T-перенос-гейт; tail 0x1a1ec '
            'читает стек вызывающего (fresh → 0). fresh-emu: (0,0), кроме (FFFF,FFFF)→(0,0xC00000). '
            'const-calc 15 кейсов (детерм.)')
def _(run, rng):
    for args, e0, e1 in _1A184_CASES:
        r0, emu = _fresh_call(0x1A184, args, max_insn=200000)
        r1 = emu.uc.reg_read(UC_ARM_REG_R1)
        assert (r0, r1) == (e0, e1), (
            f'0x1a184 {args}: ({r0:#x},{r1:#x}) ждём ({e0:#x},{e1:#x})')


# --- 0xbe6c: TLV-декодер (hdr + payload + CRC-16 0x8a50) ---

@t(0xBE6C, 'E2-b67: 0xbe6c(src,dst) — TLV-декодер: dst[0..1]=hdr; type=byte[src+1]: '
           '3 → len=byte[src+6], 0x11a4(len, src+7→dst+3), ret=len+5; 6 → dst[2..5]={src[2],src[3],'
           'src[7],src[8]}, ret=8; 0x10 → dst[2..5]=src[2..5], ret=8; иначе ret=type (только hdr). '
           'хвост: crc=0x8a50(dst, r7) (u16) → dst[r7]=hi, dst[r7+1]=lo. Реф-модель.')
def _(run, rng):
    for _ in range(6):
        t = rng.choice((3, 6, 0x10, rng.getrandbits(8) & ~0x11 if rng.getrandbits(8) not in (3, 6, 0x10) else 5))
        ln = rng.getrandbits(4)
        src = RAM + 0x2000
        dst = RAM + 0x3000
        buf = bytearray(40)
        buf[0] = rng.getrandbits(8)
        buf[1] = t
        if t == 3:
            buf[6] = ln
            buf[7:7 + ln] = bytes(rng.getrandbits(8) for _ in range(ln))
        elif t == 6:
            for i in (2, 3, 7, 8):
                buf[i] = rng.getrandbits(8)
        elif t == 0x10:
            for i in range(2, 6):
                buf[i] = rng.getrandbits(8)
        ret, emu = _fresh_call(0xBE6C, (src, dst), extra_ram=[
            (src, bytes(buf)), (dst, bytes(40))], max_insn=50000)
        uc = emu.uc
        out = bytes(uc.mem_read(dst, 40))
        if t == 3:
            exp_len = ln + 5
            exp = bytes(buf[:2]) + bytes([ln]) + bytes(buf[7:7 + ln])
        elif t in (6, 0x10):
            exp_len = 8
            if t == 6:
                exp = bytes(buf[:2]) + bytes([buf[2], buf[3], buf[7], buf[8]])
            else:
                exp = bytes(buf[:2]) + bytes(buf[2:6])
        else:
            exp_len = t
            exp = bytes(buf[:2])
        n = exp_len - 2 if t in (3, 6, 0x10) else 2
        crc, _emu = _fresh_call(0x8A50, (dst, n), max_insn=50000)
        assert ret == exp_len, f'0xbe6c t={t:#x}: ret={ret:#x} ждём {exp_len:#x}'
        assert out[:n] == exp[:n], f'0xbe6c t={t:#x}: {out[:n].hex()} ≠ {exp[:n].hex()}'
        if t in (3, 6, 0x10):
            assert out[n] == (crc >> 8) & 0xFF, (
                f'CRC hi: {out[n]:#x} ждём {(crc >> 8):#x}')
            assert out[n + 1] == crc & 0xFF, f'CRC lo: {out[n + 1]:#x} ждём {crc:#x}'


# --- 0xbd50: frame-экстрактор (L1 = RAM+0x1154, L3 = 0xE7C34640) ---
@t(0xBD50, 'E2-b67: 0xbd50(frame, r1) — frame-экстрактор: L1=RAM+0x1154 (pool 0xBE68): '
           'L1[0..1]=byte[2..3]; type=L1[1]: 3 → L1[2..5]=byte[4..7]; 6 → L1[2]=byte[4], L1[3]=byte[5], '
           'L1[7]=byte[6], L1[8]=byte[7] (тот же pool 0xBE68); 0x10 → L1[2..6]=byte[4..8] + гейт ≤0x82. '
           'хвост: u16[frame] ∈ [8..0x82] → L1[0x9D]=byte[frame+u16], L1[0x9E]=byte[frame+u16+1]. '
           'ret=0 (fresh). Реф-модель.')
def _(run, rng):
    for _ in range(5):
        t = rng.choice((3, 6, 0x10, 9))
        u16 = rng.choice((0, 0x0F, 0x82, 0x92))
        buf = bytearray(0x100)
        buf[0] = u16 >> 8
        buf[1] = u16 & 0xFF
        buf[2] = rng.getrandbits(8)
        buf[3] = t
        for i in range(4, 10):
            buf[i] = rng.getrandbits(8)
        bfr = RAM + 0x2000
        L1 = RAM + 0x1154
        ret, emu = _fresh_call(0xBD50, (bfr, 0), extra_ram=[(bfr, bytes(buf))], max_insn=50000)
        uc = emu.uc
        l1 = bytes(uc.mem_read(L1, 0xA0))
        assert l1[0] == buf[2] and l1[1] == buf[3], 'hdr-копия'
        if t == 3:
            assert l1[2:6] == bytes(buf[4:8]), 'type3: L1[2..5]'
        elif t == 6:
            assert l1[2] == buf[4] and l1[3] == buf[5] and l1[7] == buf[6], 'type6: L1[2]/[3]/[7]'
            assert l1[8] == buf[7], 'type6: L1[8] = byte[frame+7]'
        elif t == 0x10:
            assert l1[2:7] == bytes(buf[4:9]), 'type0x10: L1[2..6]'
        in_range = 8 <= u16 <= 0x82
        if in_range:
            assert l1[0x9D] == buf[u16] and l1[0x9E] == buf[u16 + 1], (
                f'хвост: L1[0x9D..] ждём {buf[u16]:#x}/{buf[u16 + 1]:#x}')
        else:
            assert l1[0x9D] == 0 and l1[0x9E] == 0, 'вне [8..0x82]: L1[0x9D..] не трогаются'
        assert ret == 0, f'ret={ret:#x}'


# --- 0x4b04: consumer (0x4a04 + 0x12d04 + 0x4a4c) ---
@t(0x4B04, 'E2-b67: 0x4b04() — consumer: bl 0x4a04 (локальная таблица) + bl 0x12d04(sp+4) '
           '(free-очередь 0x190D: u16[dst]=len, memcpy(dst+2, data+2, len)) + cbz → bl 0x4a4c '
           '(fresh: fn-таблицы 0 → payload-сдвиг: dst[0..len-3]=data[2..len], хвост 0). '
           'пусто → ret 0, dst 0; занято → S: бит снят, counter=найденный слот; ret 0 (детерм.)')
def _(run, rng):
    DST = STACK_TOP - 0x40 - 0x9C + 4
    S = RAM + 0x190D
    # пусто
    r0, emu = _fresh_call(0x4B04, (0,), max_insn=100000)
    assert r0 == 0 and bytes(emu.uc.mem_read(DST, 8)) == bytes(8), 'пусто: ret 0, dst 0'
    assert bytes(emu.uc.mem_read(S, 4)) == bytes(4), 'пусто: S не меняется'
    # занято: слот 1
    for ln in (2, 3, 4, 5, 8):
        data = bytes(rng.getrandbits(8) for _ in range(ln))
        extra = [(S, struct.pack('<BB', 0b010, 0)),
                 (S + 2 + 152, struct.pack('<H', ln)),
                 (S + 4 + 152, data + bytes(16 - ln))]
        r0, emu = _fresh_call(0x4B04, (0,), extra_ram=extra, max_insn=100000)
        uc = emu.uc
        assert bytes(uc.mem_read(S, 4))[:2] == b'\x00\x01', (
            f'ln={ln}: S ждём state=0 counter=1: {bytes(uc.mem_read(S, 4)).hex()}')
        exp = (data[2:] + bytes(16 - ln))[:max(ln - 2, 0)] + bytes(16 - max(ln - 2, 0))
        got = bytes(uc.mem_read(DST, 16))
        assert got == exp, f'ln={ln}: dst={got.hex()} ждём {exp.hex()}'
        assert r0 == 0, f'ln={ln}: ret={r0:#x}'


# --- 0x6230: FLASH sector erase core (SCBR |= 0x7C → 0x6284 → 0x6390) ---
def _flash_call(off, arg0, scbr, ctrl=0, addr=0, max_insn=30000000):
    """0x6230-путь: чистый emu (у shared-Run лимит 500K — delay-цикл 0xb0000 не дойдёт)."""
    emu = McuEmu(max_insn=max_insn)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))
    emu.hook_periph_ready()
    uc.mem_write(PERIPH + 0x2200C, struct.pack('<I', scbr))
    uc.mem_write(PERIPH + 0x22010, struct.pack('<I', ctrl))
    uc.mem_write(PERIPH + 0x22014, struct.pack('<I', addr))
    uc.reg_write(UC_ARM_REG_R0, arg0)
    uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
    uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    from unicorn import UcError  # noqa: PLC0415
    try:
        uc.emu_start(off | 1, 0, count=max_insn)
    except UcError:
        pass
    return uc.reg_read(UC_ARM_REG_R0), emu


@t(0x6230, 'E2-b67: 0x6230(addr) — FLASH sector erase core: 0x61d4(0x7C) → [0x4002200C] |= 0x7C; '
           'r5=0x6390(0xb0000): 0x6284-декодер SCBR (bit0→1, bit2→3, bit3→4, bit4→5, bit6→7, иначе 6) '
           '→ если 1: delay-цикл ×0xb0000 → 0xA (10.8M инстр.); иначе 3 (быстро). cmp r5, #6 → erase-блок '
           '(в fresh недостижим: bit2 всегда set) → ret=r5. SCBR=0 → ret 3; SCBR=1 → ret 0xA (delay). Чистый emu.')
def _(run, rng):
    CTRL = 0x40022010
    ADDR = 0x40022014
    # быстрый путь: SCBR = 0 → |= 0x7C → 0x7C → 0x6284 = 3 → ret 3
    for arg0 in (0x08010000, 0x08014000):
        r0, emu = _flash_call(0x6230, arg0, 0, max_insn=100000)
        assert r0 == 3, f'SCBR=0: ret={r0:#x} ждём 3 (bit2 → 0x6284=3, 0x6390→3)'
    assert struct.unpack_from('<I', bytes(emu.uc.mem_read(PERIPH + 0x2200C, 4)))[0] == 0x7C, (
        'SCBR |= 0x7C')
    r0, emu = _flash_call(0x6230, 0x08014000, 0, ctrl=0x1234, addr=0xAAAA5555, max_insn=100000)
    assert struct.unpack_from('<I', bytes(emu.uc.mem_read(ADDR, 4)))[0] == 0xAAAA5555, (
        'ADDR не трогается (erase-блок недостижим)')
    assert struct.unpack_from('<I', bytes(emu.uc.mem_read(CTRL, 4)))[0] == 0x1234, 'CTRL не трогается'
    # SCBR bit0 → 0x6284=1 → 0x6390: delay-цикл ×0xb0000 → 0xA (~10.8M инстр., ~20 c)
    r0, emu = _flash_call(0x6230, 0x08014000, 1)
    assert r0 == 0xA, f'SCBR=1: ret={r0:#x} ждём 0xA (delay-цикл завершён, insn={emu.insn})'
    assert struct.unpack_from('<I', bytes(emu.uc.mem_read(PERIPH + 0x2200C, 4)))[0] == 0x7D, (
        'SCBR |= 0x7C (0x7D)')


# --- 0xc0b4: NVIC IRQ enable (IPR + ISER) ---
def _prio_byte(p1, p2, ctrl):
    n = (0x700 - (ctrl & 0x700)) >> 8
    r3 = (4 - n) & 0xFF  # rsb mod 256; сдвиг ≥32 → 0
    t = (p1 << r3) if r3 < 32 else 0
    t |= p2 & (0xF >> n)
    return (t << 4) & 0xFF


@t(0xC0B4, 'E2-b67: 0xc0b4({irq,p1,p2,en}) — NVIC IRQ enable: n=(0x700−(CTRL&0x700))>>8; '
           'en=0 → только ISER[0xE000E100+irq>>3]=1<<(irq&0x1F); en=1 → IPR[0xE000E400+irq] = '
           '(((p1<<r3)|(p2&(n>>1)))<<4)&0xFF (r3=(4−n)&0xFF, сдвиг≥32→0) + ISER (en=1: 0xE000E100, '
           'en=0: 0xE000E180) [word irq>>5] = 1<<(irq&0x1F). ret=struct. '
           'Реф-модель по register-trace (11/11 кейсов).')
def _(run, rng):
    ST = 0x2000
    for _ in range(5):
        irq = rng.getrandbits(5)
        p1 = rng.getrandbits(8)
        p2 = rng.getrandbits(8)
        en = rng.getrandbits(1)
        ctrl = rng.choice((0x700, 0x500, 0x300, 0x100, 0))
        run.ram_write(ST, struct.pack('<BBBB', irq, p1, p2, en))
        run.periph_write(0xE000ED0C, ctrl)
        run.periph_write(0xE000E400 + irq, 0x55)
        iser_base = 0xE000E100 if en else 0xE000E180
        run.periph_write(iser_base + (irq >> 5) * 4, 0xAA)
        r0, _ = run.call(0xC0B4, (RAM + ST,), max_insn=100000)
        assert r0 == RAM + ST, f'ret={r0:#x} ждём struct-указатель'
        exp_en = 1 << (irq & 0x1F)
        got_en = run.periph_read(iser_base + (irq >> 5) * 4)
        assert got_en == exp_en, (
            f'ISER[{irq >> 5}]={got_en:#x} ждём {exp_en:#x} (irq={irq} en={en})')
        if en:
            exp_prio = _prio_byte(p1, p2, ctrl)
            got_prio = run.periph_read(0xE000E400 + irq)
            assert got_prio == exp_prio, (
                f'IPR[{irq}]={got_prio:#x} ждём {exp_prio:#x} (p1={p1:#x} p2={p2:#x} ctrl={ctrl:#x})')
        else:
            assert run.periph_read(0xE000E400 + irq) == 0x55, 'en=0: IPR не меняется'


# --- 0x1a2a4: timer IRQ handler (гейт bit7 SR) ---
@t(0x1A2A4, 'E2-b67: 0x1a2a4() — timer IRQ @0x40012C00: гейт = bit7(+0x1C) (lsls #0x18 + bpl); '
            'bit7=0 → ret=0x40012C00, без записей; bit7=1 → [+0x54]&=~0x8000, byte[0x218]=0, '
            '[+0x20]|=0x80, byte[0x245]=1, byte[0x246]=0; byte[0x102]: 0 → byte[0x247]|=1, '
            'u16[0x21E]|=8, ret=8; 1/≥3 → ret=0x20000247; 2 → byte[0x247]|=2, u16[0x21E]|=0x2000, ret=0x2000.')
def _(run, rng):
    SR = 0x40012C1C
    R54 = 0x40012C54
    R20 = 0x40012C20
    for _ in range(4):
        b102 = rng.getrandbits(2)
        bit7 = rng.getrandbits(1)
        run.periph_write(SR, (bit7 << 7) | rng.getrandbits(7))
        run.periph_write(R54, 0x80008001)
        run.periph_write(R20, 0x01)
        run.ram_write(0x218, bytes([0x77]))
        run.ram_write(0x21E, struct.pack('<H', 0))
        run.ram_write(0x245, bytes([0x99]))
        run.ram_write(0x246, bytes([0x77]))
        run.ram_write(0x247, bytes([0x00]))
        run.ram_write(0x102, bytes([b102]))
        r0, _ = run.call(0x1A2A4, (), max_insn=200000)
        if not bit7:
            assert r0 == 0x40012C00, f'bit7=0: ret={r0:#x}'
            assert run.periph_read(R54) == 0x80008001, 'bit7=0: [+0x54] не меняется'
            assert run.periph_read(R20) == 0x01, 'bit7=0: [+0x20] не меняется'
            assert run.ram_read(0x245, 1)[0] == 0x99 and run.ram_read(0x247, 1)[0] == 0, (
                'bit7=0: RAM не меняется')
        else:
            assert run.periph_read(R54) == 0x80000001, '[+0x54] &= ~0x8000'
            assert run.periph_read(R20) == 0x81, '[+0x20] |= 0x80'
            assert run.ram_read(0x218, 1)[0] == 0, 'byte[0x218] = 0'
            assert run.ram_read(0x245, 1)[0] == 1 and run.ram_read(0x246, 1)[0] == 0, (
                'byte[0x245]=1, byte[0x246]=0')
            if b102 == 0:
                assert r0 == 8, f'b102=0: ret={r0:#x}'
                assert run.ram_read(0x247, 1)[0] == 1, 'byte[0x247] |= 1'
                assert struct.unpack('<H', run.ram_read(0x21E, 2))[0] == 8, 'u16[0x21E] |= 8'
            elif b102 == 2:
                assert r0 == 0x2000, f'b102=2: ret={r0:#x}'
                assert run.ram_read(0x247, 1)[0] == 2, 'byte[0x247] |= 2'
                assert struct.unpack('<H', run.ram_read(0x21E, 2))[0] == 0x2000, 'u16[0x21E] |= 0x2000'
            else:
                assert r0 == 0x20000247, f'b102={b102}: ret={r0:#x}'
                assert run.ram_read(0x247, 1)[0] == 0, 'byte[0x247] не меняется'


# --- 0xee48: buffer/queue manager @0x2FFA (counter clamp) ---
@t(0xEE48, 'E2-b67: 0xee48(src,dst,r2) — buffer manager: r6=u16[src]−0xF (underflow→0); '
           'u16[dst] < r6 → counter=s8[0x2FFA+0x14]+1 (clamp 0x7F), иначе 0; u16[src] не меняется; '
           'fixed-point хвост (udiv 0x3E8) → fresh ret 0. Реф-модель.')
def _(run, rng):
    SRC = 0x2000
    DST = 0x3000
    B = 0x2FFA
    for _ in range(6):
        lens = rng.choice((0x5, 0x10, 0x20, 0x1FF))
        r6 = (lens - 0xF) & 0xFFFF
        underflow = lens < 0xF
        exp_r6 = 0 if underflow else r6
        dstv = rng.getrandbits(16)
        cnt0 = rng.choice((0, 5, 0x7E, 0xFF))
        run.ram_write(SRC, struct.pack('<H', lens))
        run.ram_write(DST, struct.pack('<H', dstv))
        run.ram_write(B + 0x14, bytes([cnt0]))
        r0, _ = run.call(0xEE48, (RAM + SRC, RAM + DST, 0), max_insn=200000)
        s8c = cnt0 - 0x100 if cnt0 >= 0x80 else cnt0
        if dstv < exp_r6:
            exp = min(s8c + 1, 0x7F) & 0xFF
        else:
            exp = 0
        got = run.ram_read(B + 0x14, 1)[0]
        assert got == exp, (
            f'lens={lens:#x} dst={dstv:#x} cnt0={cnt0:#x}: counter={got:#x} ждём {exp:#x}')
        assert struct.unpack('<H', run.ram_read(SRC, 2))[0] == lens, 'u16[src] не меняется'
        assert r0 == 0, f'ret={r0:#x}'


# --- 0x1b67c: overheat pre-stage (s16-вычисление + blx flash-таблицы) ---
@t(0x1B67C, 'E2-b67: 0x1b67c() — overheat pre-stage: u32[0x3C8+0x68] = s16[0x24A] + u32[0x430] '
            '− s16[0x24C]; s16[0x24C] = результат >> 5 (арифм.); blx [flash-табл 0xA8C8][byte[0x3C8+0x10]] '
            '→ fresh: table[0]=0x26004605 (незамапленный) → останов fetch, r0=0x26004605, last_error. '
            'Реф-модель.')
def _(run, rng):
    for _ in range(5):
        v = rng.getrandbits(16) - 0x8000
        old = rng.getrandbits(16) - 0x8000
        run.ram_write(0x24A, struct.pack('<h', v))
        run.ram_write(0x24C, struct.pack('<h', old))
        run.ram_write(0x430, struct.pack('<I', 0))
        r0, r1 = run.call(0x1B67C, (), max_insn=200000)
        assert r0 == 0x26004605, (
            f'blx table[0]: r0={r0:#x} ждём 0x26004605')
        assert run.last_error is not None, 'last_error: unmapped fetch на blx'
        run.last_error = None
        res = (v + 0 - old) & 0xFFFFFFFF
        got = struct.unpack('<I', run.ram_read(0x430, 4))[0]
        assert got == res, f'u32[0x430]={got:#x} ждём {res:#x} (v={v} old={old})'
        s32 = res - 0x100000000 if res >= 0x80000000 else res
        exp_s = s32 >> 5
        got_s = struct.unpack('<h', run.ram_read(0x24C, 2))[0]
        assert got_s == exp_s, f's16[0x24C]={got_s} ждём {exp_s}'


# --- 0x56bc: response encoder (0x74-кадр, «OK», 25B-блок, chk 0x1e34) ---
@t(0x56BC, 'E2-b67: 0x56bc(cs,out,len_ptr) — response encoder: out[0]=0x74, out[1]=byte[cs+2]; '
           'byte[cs]==0x10: byte[cs+2]==0x81 → out[2]=0x1B, out[3]=byte[0xCB3], out[4]=byte[0xCB3+1], '
           '0x11a4(25B: RAM+0x30DD→out+3, перезаписывает 3..4) (30B-кадр); иначе «OK»: out[2..3]=0x4F 0x4B (6B-кадр). '
           'byte[cs]≠0x10: len=byte[cs+4], out[2]=len, 0x11a4(len, cs+5→out+3) (2+len+2 кадра). '
           'chk=0x1e34(out, r4) → out[r4], out[r4+1]=0x8B; *len_ptr=strb(длина); ret=длина−1.')
def _(run, rng):
    CS = 0x2000
    OUT = 0x3000
    LP = 0x4000
    for _ in range(6):
        kind = rng.choice(('ok', 'block25', 'copy', 'copy0'))
        buf = bytearray(40)
        buf[0] = 0x10 if kind in ('ok', 'block25') else rng.getrandbits(8) & 0xEF | 0x1
        buf[2] = 0x81 if kind == 'block25' else rng.getrandbits(8) & 0x7F
        if kind == 'copy':
            ln = rng.getrandbits(4) & 0x0F
            buf[4] = ln
            for i in range(5, 5 + ln):
                buf[i] = rng.getrandbits(8)
        elif kind == 'copy0':
            buf[4] = 0
        run.ram_write(CS, bytes(buf))
        run.ram_write(OUT, bytes(48))
        run.ram_write(0x30DD, bytes(rng.getrandbits(8) for _ in range(25)))
        run.ram_write(0xCB3, bytes(rng.getrandbits(8) for _ in range(2)))
        run.ram_write(LP, struct.pack('<I', 0))
        r0, _ = run.call(0x56BC, (RAM + CS, RAM + OUT, RAM + LP), max_insn=200000)
        out = run.ram_read(OUT, 48)
        lp0 = run.ram_read(LP, 1)[0]
        if kind == 'ok':
            frame = bytes([0x74, buf[2], 0x4F, 0x4B])
            n = 4
        elif kind == 'block25':
            cb3 = run.ram_read(0xCB3, 2)
            blk = run.ram_read(0x30DD, 25)
            frame = bytes([0x74, 0x81, 0x1B, cb3[0], cb3[1]]) + blk
            n = 30
        elif kind == 'copy':
            frame = bytes([0x74, buf[2], ln]) + bytes(buf[5:5 + ln])
            n = 2 + ln
        else:
            frame = bytes([0x74, buf[2], 0])
            n = 3
        n = len(frame)
        run.ram_write(0x5000, frame[:n])
        chk, _ = run.call(0x1E34, (RAM + 0x5000, n), max_insn=10000)
        exp = frame + bytes([chk, 0x8B])
        assert out[:len(exp)] == exp, (
            f'kind={kind}: {out[:len(exp)].hex()} ждём {exp.hex()}')
        assert lp0 == len(exp), (
            f'kind={kind}: *len_ptr={lp0} ждём {len(exp)}')
        assert r0 == len(exp) - 1, (
            f'kind={kind}: ret={r0} ждём {len(exp) - 1}')
