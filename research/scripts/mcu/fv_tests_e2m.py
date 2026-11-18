# -*- coding: utf-8 -*-
"""E2-b68: 16B-блок-шифр 0x1a7ac (S-box 0xA907 + перестановка + диффузия 0x1dd8c
+ key-XOR, 10 раундов + финальный), SYSCFG-флаг 0x1e480 (bit0 0x483C → 0x4840 |= 0x101),
tick-счётчики 0x1bb1c (0x7D0/0x1F40-капы + флаг RAM+0x100), clamp-регистратор 0x7494
(v2/v3 из u16[0xF9D/0xF9B], [0x3E8..0x1388], tail-расчёт), buffer-config 0x22d2c
(u32[+0x28] = (u32 & ~0x73) | byte[buf2]<<4, u32[+0x30] = (u32 & ~3) | byte[buf2+8]<<1),
descriptor-валидатор 0x23188 (magic ∈ {0x40013800,0x40004400,0x40004800}, byte-поля,
инициализация u32[TIM+0xC], hang на невалидном), delegate 0x3b2a (ret 0x10),
init-парочка 0x15758 (u32[0x27D8] = 0x800), pointer 0x9f70 (RAM+0x14CE),
двойной 20B-строковый декодер 0x1c838 (0x19a68×2 → RAM+0x844/+0x858),
gate-копира 0x21a08 (byte[0x170]+bit30 u32[TIM3+0x14]), motor-расчёт 0x6fc0,
flag-sync 0x1d3d0."""
# ruff: noqa: F405  (имена из star-import от fv_core)
from fv_core import *  # noqa: F401,F403

import os
import struct

from emulator.mcu_emu import McuEmu, PERIPH  # noqa: E402
from unicorn import UcError, UC_HOOK_CODE, UC_HOOK_MEM_WRITE  # noqa: E402
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, \
    UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_LR  # noqa: E402

_IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '..', '..', 'images', 'mcu_0007.bin')
_FW = open(_IMG, 'rb').read()

# --- общий fresh-emu пробор (чистый RAM + 0xFF PERIPH, запись-лог) ---


def _fresh_probe(off, seeds=(), args=(), max_insn=50000):
    emu = McuEmu(max_insn=max_insn)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))
    emu.hook_periph_ready()
    for addr, val in seeds:
        uc.mem_write(addr, bytes(val) if isinstance(val, (bytes, bytearray))
                     else struct.pack('<I', val))
    for i, a in enumerate(args):
        uc.reg_write((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                      UC_ARM_REG_R3)[i], a)
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


# --- 0x1a7ac: 16B-блок-шифр (S-box 0xA907, перестановка, диффузия, key-XOR) ---
_1A7AC_TBL = _FW[0xA907:0xA907 + 256]


def _xt(v):
    # 0x1dd8c-раунд: xtime в GF(2^8) с полиномом 0x1B (проверено 4/4)
    return ((v << 1) ^ ((v >> 7) * 0x1B)) & 0xFF


def _perm16(g):
    # одновременная перестановка (реестровая загрузка до стрб, эмпирика 0x1a7e0..)
    o = list(g)
    g[1] = o[5]
    g[2] = o[0xA]
    g[3] = o[0xF]
    g[5] = o[9]
    g[6] = o[0xE]
    g[7] = o[3]
    g[9] = o[0xD]
    g[0xA] = o[2]
    g[0xB] = o[7]
    g[0xD] = o[1]
    g[0xE] = o[6]
    g[0xF] = o[0xB]


def _ref_1a7ac(grid16, src):
    g = bytearray(grid16)
    for i in range(16):
        g[i] ^= src[i]
    for r5 in range(1, 0xB):
        for i in range(16):
            g[i] = _1A7AC_TBL[g[i]]
        _perm16(g)
        if r5 < 0xA:
            for gi in range(4):
                b0, b1, b2, b3 = (g[gi * 4], g[gi * 4 + 1],
                                   g[gi * 4 + 2], g[gi * 4 + 3])
                s4 = b0 ^ b1 ^ b2 ^ b3
                g[gi * 4] = b0 ^ _xt(b0 ^ b1) ^ s4
                g[gi * 4 + 1] = b1 ^ _xt(b1 ^ b2) ^ s4
                g[gi * 4 + 2] = b2 ^ _xt(b2 ^ b3) ^ s4
                g[gi * 4 + 3] = b3 ^ _xt(b3 ^ b0) ^ s4
        for i in range(16):
            g[i] ^= src[r5 * 16 + i]
    return bytes(g)


@t(0x1A7AC, 'E2-b68: 0x1a7ac(grid, src) — 16B-блок-шифр in-place grid[0..15]: '
            'key0-XOR src[0..15]; 10 раундов (r5=1..0xA): S-box 0xA907, одновременная '
            'перестановка 12 байтов (1←5, 2←0xA, 3←0xF, 5←9, 6←0xE, 7←3, 9←0xD, 0xA←2, '
            '0xB←7, 0xD←1, 0xE←6, 0xF←0xB; 0/4/8/0xC — инвариантны), r5<0xA: диффузия 0x1dd8c '
            '(4 группы: b_i ^ xtime(b_i ^ next) ^ parity-4), key-XOR src[r5*16..]; r5=0xA: '
            'только финальный XOR src[0xA0..]. ret=4. Рефмодель (2 случайных + нуль-кейс).')
def _(run, rng):
    grid_off, src_off = 0x5000, 0x5100
    cases = [(bytes(256), bytes(256))]
    for _ in range(2):
        cases.append((bytes(rng.getrandbits(8) for _ in range(256)),
                      bytes(rng.getrandbits(8) for _ in range(256))))
    for grid, src in cases:
        uc, emu, _lp = _fresh_probe(0x1A7AC,
                                    seeds=[(RAM + grid_off, grid),
                                           (RAM + src_off, src)],
                                    args=(RAM + grid_off, RAM + src_off),
                                    max_insn=20000)
        g2 = bytes(uc.mem_read(RAM + grid_off, 256))
        exp = _ref_1a7ac(grid[:16], src)
        assert g2[:16] == exp, (
            f'0x1a7ac блок: {g2[:16].hex(" ")} ждём {exp.hex(" ")}')
        assert g2[16:] == grid[16:], '0x1a7ac: tail 16.. изменён'
        assert uc.reg_read(UC_ARM_REG_R0) == 4, \
            f'0x1a7ac ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 4'


# --- 0x1e480: bit0 u32[PERIPH+0x483C] → u32[PERIPH+0x4840] |= 0x101 ---

@t(0x1E480, 'E2-b68: 0x1e480() — u32[0x4000483C] (SYSCFG/AFIO-объект 0x40004800, поле +0x3C): '
            'bit0 установлен (lsl #0x1f ≠ 0 → bne) → u32[0x40004840] |= 0x101 '
            '(0xFE → 0x1FF: два str |= 1 + |= 0x100); bit0=0 → без записи (tail 0x1e4b0: '
            'lsl-катена bpl). ret — мусор tail (0x40004800). fresh-emu, 2 кейса.')
def _(run, rng):
    for val, exp in ((0x00000000, 0x000000FE), (0x00000001, 0x000001FF),
                     (0x00000003, 0x000001FF), (0x80000000, 0x000000FE)):
        uc, _emu, _lp = _fresh_probe(0x1E480,
                                     seeds=[(PERIPH + 0x483C, val),
                                            (PERIPH + 0x4840, 0x000000FE)])
        got = struct.unpack_from('<I', bytes(uc.mem_read(PERIPH + 0x4840, 4)), 0)[0]
        assert got == exp, (f'0x1e480 u32[0x483C]={val:#010x}: '
                            f'u32[0x4840]={got:#x} ждём {exp:#x}')


# --- 0x1bb1c: tick-счётчики (u16[obj+0xC] капа 0x7D0, u16[0xDE] капа 0x1F40) ---

@t(0x1BB1C, 'E2-b68: 0x1bb1c(obj) — tick-счётчики: c=u16[obj+0xC]: c<0x7D0 → c++ и '
            'byte[0x100]=1, иначе byte[0x100]=0; u16[0xAC+0x32=0xDE]: <0x1F40 → ++, '
            'иначе u16[0xDE]=u16[0xAC+0x34=0xE0]=0; byte[obj+0x14]≠byte[0x268] → u16[0xE0]++; '
            'хвост: byte[obj+0xA] 0/1, u16[obj+0x14]=0x40, history-массив, '
            'u16[obj+0xC] сброс в 0 (strh r2=0). ret=obj. 2 кейса (инкремент/капы).')
def _(run, rng):
    obj = RAM + 0x3000
    # кейс A: инкремент обоих счётчиков + mismatch-инкремент
    uc, _emu, _lp = _fresh_probe(0x1BB1C,
                                 seeds=[(obj + 0xC, struct.pack('<H', 5)),
                                        (RAM + 0xDE, struct.pack('<H', 0x7D3)),
                                        (obj + 0x14, 0),
                                        (RAM + 0x268, 1)],
                                 args=(obj,))
    ram = bytes(uc.mem_read(RAM, 0x20000))
    assert ram[0x100] == 1, '0x1bb1c A: флаг 0x100 ждём 1'
    assert struct.unpack_from('<H', ram, 0xDE)[0] == 0x7D4, \
        '0x1bb1c A: u16[0xDE] ждём 0x7D4'
    assert struct.unpack_from('<H', ram, 0xE0)[0] == 1, \
        '0x1bb1c A: u16[0xE0] ждём 1 (mismatch)'
    assert struct.unpack_from('<H', ram, 0x300C)[0] == 0, \
        '0x1bb1c A: u16[obj+0xC] финал ждём 0 (сброс)'
    assert uc.reg_read(UC_ARM_REG_R0) == obj, '0x1bb1c A: ret ждём obj'
    # кейс B: обе капы + mismatch
    uc, _emu, _lp = _fresh_probe(0x1BB1C,
                                 seeds=[(obj + 0xC, struct.pack('<H', 0x7D0)),
                                        (RAM + 0xDE, struct.pack('<H', 0x1F40)),
                                        (obj + 0x14, 1),
                                        (RAM + 0x268, 0)],
                                 args=(obj,))
    ram = bytes(uc.mem_read(RAM, 0x20000))
    assert ram[0x100] == 0, '0x1bb1c B: флаг 0x100 ждём 0 (капа)'
    assert struct.unpack_from('<H', ram, 0xDE)[0] == 0, \
        '0x1bb1c B: u16[0xDE] ждём 0 (капа)'
    assert struct.unpack_from('<H', ram, 0xE0)[0] == 1, \
        '0x1bb1c B: u16[0xE0] ждём 1 (мismatch после сброса)'
    assert struct.unpack_from('<H', ram, 0x300C)[0] == 0, \
        '0x1bb1c B: u16[obj+0xC] финал ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == obj, '0x1bb1c B: ret ждём obj'


# --- 0x7494: clamp-регистратор (v2/v3 ∈ [0x3E8..0x1388], tail-расчёт) ---
_7494_CASES = [
    # (v2 seed, v3 seed, u16[0x135A], u16[0x135C], u16[0x3004], u16[0x3000],
    #  u16[0x3006], u32[0x2FEC], ret)
    (0x500, 0x400, 0x500, 0x400, 0x0000, 0x0000, 0x0000, 0xFFFFFD14, 0x15E802),
    (0x400, 0x500, 0x400, 0x500, 0x0000, 0x0000, 0x0000, 0xFFFFFD14, 0x15E802),
    (0x2000, 0x100, 0x2000, 0x0100, 0x0000, 0x0000, 0x0000, 0xFFFFFF74, 0x15E802),
    (0x1388, 0x3E8, 0x1388, 0x03E8, 0x0000, 0x0000, 0x0000, 0xFFFFFF74, 0x15E802),
]


@t(0x7494, 'E2-b68: 0x7494() — v1=0x8f04()=0x1068 (→u16[0x301F]); v2=clamp(u16[0xF9D], '
            '[0x3E8,0x1388]) → u16[0x135A]; v3=clamp(u16[0xF9B], ...) → u16[0x135C]; '
            'хвост: u16[0x3004]=max(v2,v3)-v3 (s16), u16[0x3000]=0x3E8-u16[0x3004], '
            'u16[0x3006]=v3-0xC80 (s16); cbnz u16[0x3000] → smulbb/sdiv → u32[0x2FEC]; '
            'в финале u16[0x3004/0x3000/0x3006] обнуляются; ret=0x15E802 (константа). '
            '4 кейса (вкл. clamp-границы).')
def _(run, rng):
    for v2, v3, e2a, e2b, e4, e0, e6, e32, eret in _7494_CASES:
        uc, _emu, _lp = _fresh_probe(0x7494,
                                     seeds=[(RAM + 0xF9D, struct.pack('<H', v2)),
                                            (RAM + 0xF9B, struct.pack('<H', v3))])
        ram = bytes(uc.mem_read(RAM, 0x20000))
        got = (struct.unpack_from('<H', ram, 0x135A)[0],
               struct.unpack_from('<H', ram, 0x135C)[0],
               struct.unpack_from('<H', ram, 0x3004)[0],
               struct.unpack_from('<H', ram, 0x3000)[0],
               struct.unpack_from('<H', ram, 0x3006)[0],
               struct.unpack_from('<I', ram, 0x2FEC)[0])
        exp = (e2a, e2b, e4, e0, e6, e32)
        assert got == exp, (f'0x7494 v2={v2:#x} v3={v3:#x}: {tuple(hex(x) for x in got)} '
                            f'ждём {tuple(hex(x) for x in exp)}')
        assert uc.reg_read(UC_ARM_REG_R0) == eret, \
            f'0x7494 ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём {eret:#x}'


# --- 0x22d2c: buffer-config (уPACK-биты из buf2 в u32[buf1+0x28/+0x30]) ---

@t(0x22D2C, 'E2-b68: 0x22d2c(buf1, buf2) — buffer-config: u32[buf1+0x30] = (u32 & ~3) | '
            '(byte[buf2+8] << 1); u32[buf1+0x28] = (u32 & ~0x73) | (byte[buf2] << 4) '
            '(5 проходов mask/copy: >>1<<1, &~0x70, >>2<<2, &~0x70, |byte<<4; затем &~2 | '
            'byte[+8]<<1); tail: 5-way cmp buf1 с pool-указателями (иначе — путь 0x22da0: '
            'byte[buf2+0xB/+0xC] ∈ {0,1} гейты, u32[buf1+4] = (u32 & ~0xFF) | byte[+0xB]<<8); '
            'ret=buf1. Кейс: u32[+0x28]=0xABCD1278, u32[+0x30]=0x55555555, byte[buf2]=0x37, '
            'byte[buf2+8]=0x41 → 0xABCD1378 / 0x555555D6.')
def _(run, rng):
    b1, b2 = RAM + 0x3000, RAM + 0x3040
    uc, _emu, _lp = _fresh_probe(0x22D2C,
                                 seeds=[(b1 + 0x28, 0xABCD1278),
                                        (b1 + 0x30, 0x55555555),
                                        (b2, 0x37),
                                        (b2 + 8, 0x41)],
                                 args=(b1, b2))
    r28 = struct.unpack_from('<I', bytes(uc.mem_read(b1 + 0x28, 4)), 0)[0]
    r30 = struct.unpack_from('<I', bytes(uc.mem_read(b1 + 0x30, 4)), 0)[0]
    assert r28 == ((0xABCD1278 & ~0x73) | (0x37 << 4)) & 0xFFFFFFFF, \
        f'0x22d2c u32[+0x28]={r28:#x} ждём {((0xABCD1278 & ~0x73) | (0x37 << 4)):#x}'
    assert r30 == ((0x55555555 & ~3) | (0x41 << 1)) & 0xFFFFFFFF, \
        f'0x22d2c u32[+0x30]={r30:#x} ждём {((0x55555555 & ~3) | (0x41 << 1)):#x}'
    assert uc.reg_read(UC_ARM_REG_R0) == b1, \
        f'0x22d2c ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём buf1'


# --- 0x23188: descriptor-валидатор (magic + byte-поля → init u32[TIM+0xC]) ---

@t(0x23188, 'E2-b68: 0x23188(obj) — descriptor-валидатор: u32[obj] ∈ '
            '{0x40013800, 0x40004400, 0x40004800} (иначе cpsid i; b . — hang); '
            'u32[obj+4] < pool (иначе hang); byte[obj+8]∈{0..3}, [+9]∈{0,1}, [+0xA]∈{0,1,3}, '
            '[+0xB]∈{0..5}, [+0xC]∈{0,1} (иначе hang); валидный: bl 0x23314 + init '
            'u32[u32[obj]+0xC] (для 0x40004400 с 0xFF-периферией: 0xC000) + byte[+0x70..72]; '
            'ret=0. 2 кейса (валидный golden / invalid hang).')
def _(run, rng):
    obj = RAM + 0x3000
    uc, _emu, _lp = _fresh_probe(0x23188,
                                 seeds=[(obj, 0x40004400), (obj + 4, 5)],
                                 args=(obj,))
    p = struct.unpack_from('<I', bytes(uc.mem_read(PERIPH + 0x440C, 4)), 0)[0]
    assert p == 0xC000, f'0x23188 valid: u32[0x440C]={p:#x} ждём 0xC000'
    ram = bytes(uc.mem_read(RAM, 0x20000))
    assert ram[0x3070] == 0 and ram[0x3071] == 1 and ram[0x3072] == 0, \
        '0x23188 valid: byte[obj+0x70]=0/0x71=1/0x72=0 ждём'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x23188 valid: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    uc, emu, lp = _fresh_probe(0x23188, seeds=[(obj, 0x1234)], args=(obj,),
                               max_insn=1000)
    assert emu.insn >= 1000, f'0x23188 invalid: hang ждём, insn={emu.insn}'
    assert lp in (0x231A6, 0x231A8), f'0x23188 invalid: lastpc={lp:#x} ждём spin'


# --- 0x3b2a: delegate (bl 0xc304/0x12aec/0xa788/0x14924 → ret 0x10) ---

@t(0x3B2A, 'E2-b68: 0x3b2a() — delegate: bl 0xc304 → bl 0x12aec → bl 0xa788 → bl 0x14924 '
           '→ pop; ret=0x10 (0x14924). fresh-emu.')
def _(run, rng):
    uc, _emu, _lp = _fresh_probe(0x3B2A, max_insn=5000)
    assert uc.reg_read(UC_ARM_REG_R0) == 0x10, \
        f'0x3b2a ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x10'


# --- 0x15758: init-парочка (0x11d6 + 2×0x11c8 + u32[0x27D8] = 0x800) ---

@t(0x15758, 'E2-b68: 0x15758() — init-парочка: 0x11d6(0x80C, pool1), 0x11c8(0x800, '
            'pool2=0x200027E0, 0xFF)×2, затем u32[0x20001FD4+0x804=0x27D8] = 0x800; '
            'ret=0x800. fresh-emu.')
def _(run, rng):
    uc, _emu, _lp = _fresh_probe(0x15758)
    got = struct.unpack_from('<I', bytes(uc.mem_read(RAM + 0x27D8, 4)), 0)[0]
    assert got == 0x800, f'0x15758 u32[0x27D8]={got:#x} ждём 0x800'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x800, \
        f'0x15758 ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x800'


# --- 0x9f70: pointer (bl 0xa39c → ret RAM+0x14CE) ---

@t(0x9F70, 'E2-b68: 0x9f70() — delegate: bl 0xa39c → ret=0x200014CE (RAM+0x14CE). '
           'fresh-emu.')
def _(run, rng):
    uc, _emu, _lp = _fresh_probe(0x9F70)
    assert uc.reg_read(UC_ARM_REG_R0) == 0x200014CE, \
        f'0x9f70 ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x200014CE'


# --- 0x1c838: двойной 20B-строковый декодер (0x19a68×2) ---
_1C838_S1 = bytes.fromhex('09a4a5a6c274f8000099c30103c260a0a000a020')
_1C838_S2 = bytes.fromhex('e96272160930303030302f30303030')


@t(0x1C838, 'E2-b68: 0x1c838() — двойной строковый декодер: 0x19a68(20, adr 0x1CC06) → '
            '20B в RAM+0x844 (UTF-8-строка), 0x19a68(20, adr 0x1CC1E) → 15B-строка в '
            'RAM+0x858 + overwrite 0x85D..0x861 = 0x30×5; ret=1. 5834 insn. '
            'fresh-emu golden.')
def _(run, rng):
    uc, _emu, _lp = _fresh_probe(0x1C838, max_insn=20000)
    ram = bytes(uc.mem_read(RAM, 0x20000))
    assert ram[0x844:0x858] == _1C838_S1, \
        f'0x1c838 строка1: {ram[0x844:0x858].hex(" ")} ждём {_1C838_S1.hex(" ")}'
    assert ram[0x858:0x867] == _1C838_S2, \
        f'0x1c838 строка2: {ram[0x858:0x867].hex(" ")} ждём {_1C838_S2.hex(" ")}'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x1c838 ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'


# --- 0x21a08: gate-копира (byte[0x170] + bit30 u32[TIM3+0x14]) ---

@t(0x21A08, 'E2-b68: 0x21a08() — gate-копира: gate=byte[0x170]; gate==1 и '
            '(u32[0x40012C40+0x14=0x40012C54] lsl #0x10) bit31==0 (т.е. bit15 исходного) → '
            '7×0x221a4/0x221e6-копирование (SPI-пины, ~7.6K insn, byte[0x170] сбрасывается '
            'в 0); иначе — быстрый выход. 3 кейса (gate=0 / sign / pos).')
def _(run, rng):
    # (a) gate = 0
    uc, _emu, _lp = _fresh_probe(0x21A08)
    ram = bytes(uc.mem_read(RAM, 0x20000))
    assert ram[0x170] == 0 and uc.reg_read(UC_ARM_REG_R0) == 0, \
        '0x21a08 gate=0: ждём ret=0'
    # (b) gate = 1, u32 = 0x8000 (bit15 → после lsl #0x10 bit31 → skip)
    uc, _emu, _lp = _fresh_probe(0x21A08,
                                 seeds=[(RAM + 0x170, 1),
                                        (PERIPH + 0x12C54, 0x8000)])
    assert _emu.insn < 100, \
        f'0x21a08 skip: быстрый выход ждём, insn={_emu.insn}'
    ram = bytes(uc.mem_read(RAM, 0x20000))
    assert ram[0x170] == 1, '0x21a08 skip: byte[0x170] не сбрасывается (1)'
    # (c) gate = 1, u32 = 0x10000 (bit15=0 → proceed)
    uc, _emu, _lp = _fresh_probe(0x21A08,
                                 seeds=[(RAM + 0x170, 1),
                                        (PERIPH + 0x12C54, 0x10000)],
                                 max_insn=200000)
    ram = bytes(uc.mem_read(RAM, 0x20000))
    assert ram[0x170] == 0, '0x21a08 pos: byte[0x170] ждём 0 (сброс)'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x21a08 pos: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert _emu.insn > 7000, f'0x21a08 pos: длинный путь ждём, insn={_emu.insn}'


# --- 0x6fc0: motor-расчёт (0x10ff8/0x8e90/0x8ecc/0x8ee8/0xe3ec/0xe36c/0x11098) ---

@t(0x6FC0, 'E2-b68: 0x6fc0() — motor-расчёт: 0x10ff8(1) (flag 0x1384), 0x8e90 (не 0 → '
            'tail 0x7034), 0x8ecc/0x8ee8-копии (u16[0x135A/0x135C/0x135E]), 0xe3ec×2 '
            '(s16-стек), 0xe36c(сравнение), u16[0x1385]=0x4050, u32[0x128F..0x129B]=0, '
            'u16[0x12AB/0x12AD]=0, byte[0x12B6]=0, flag 0x1384 сброс; ret=0. '
            '432 insn. fresh-emu golden.')
def _(run, rng):
    uc, _emu, _lp = _fresh_probe(0x6FC0)
    ram = bytes(uc.mem_read(RAM, 0x20000))
    assert ram[0x1384] == 0, '0x6fc0: flag 0x1384 финал ждём 0'
    assert struct.unpack_from('<H', ram, 0x1385)[0] == 0x4050, \
        '0x6fc0: u16[0x1385] ждём 0x4050'
    assert struct.unpack_from('<H', ram, 0x1387)[0] == 0, \
        '0x6fc0: u16[0x1387] ждём 0'
    for off in (0x135A, 0x135C, 0x135E, 0x12AB, 0x12AD):
        assert struct.unpack_from('<H', ram, off)[0] == 0, \
            f'0x6fc0: u16[{off:#x}] ждём 0'
    for off in (0x128F, 0x1293, 0x1297, 0x129B):
        assert struct.unpack_from('<I', ram, off)[0] == 0, \
            f'0x6fc0: u32[{off:#x}] ждём 0'
    assert ram[0x12B6] == 0, '0x6fc0: byte[0x12B6] ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x6fc0 ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'


# --- 0x1d3d0: flag-sync (byte[0x3C8] → byte[0x3D6], u32[0x498..0x4A4] сброс) ---

@t(0x1D3D0, 'E2-b68: 0x1d3d0() — flag-sync: A=0x200003C8, B=0x20000444: '
            'byte[A] ≠ byte[B+0xF=0x453] → byte[0x3D6] = 1, byte[0x31E] = 0, '
            'u32[0x498/0x49C/0x4A0/0x4A4] = 0 (4 слова); ret=0. 53 insn. '
            'fresh-emu golden (seed: byte[0x3C8]=0xAB, byte[0x453]=0, u32[0x444]=0x1234).')
def _(run, rng):
    uc, _emu, _lp = _fresh_probe(0x1D3D0,
                                 seeds=[(RAM + 0x3C8, 0xAB),
                                        (RAM + 0x453, 0),
                                        (RAM + 0x444, 0x1234)])
    ram = bytes(uc.mem_read(RAM, 0x20000))
    assert ram[0x3D6] == 1, '0x1d3d0: byte[0x3D6] ждём 1'
    assert ram[0x31E] == 0, '0x1d3d0: byte[0x31E] ждём 0'
    for off in (0x498, 0x49C, 0x4A0, 0x4A4):
        assert struct.unpack_from('<I', ram, off)[0] == 0, \
            f'0x1d3d0: u32[{off:#x}] ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x1d3d0 ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
