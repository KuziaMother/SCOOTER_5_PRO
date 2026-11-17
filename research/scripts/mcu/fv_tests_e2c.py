# -*- coding: utf-8 -*-
# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-batch25..35 (5565-5786)."""
from fv_core import *  # noqa: F401,F403
from fv_core import _fresh_call, _intercept  # noqa: F401
# --- E2-batch25: event-очередь push (stateful) ---
@t(0x04BC0, 'E2-b25: 0x04bc0 — event-очередь push: если idx<6 -> u32@(0x164C+idx*16+8)=ptr, +0xC=val (через critsec). Вериф idx=2 (write) и idx=7 (skip).')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    r0, emu = _fresh_call(0x04BC0, args=(2, 0x1234, 0xABCD))
    uc = emu.uc
    base = _R + 0x164C + 2 * 16
    ptr = _st.unpack_from('<I', bytes(uc.mem_read(base + 8, 4)))[0]
    val = _st.unpack_from('<I', bytes(uc.mem_read(base + 0xC, 4)))[0]
    assert ptr == 0x1234 and val == 0xABCD, f'idx=2: ptr={ptr:#x} val={val:#x}'
    r0, emu2 = _fresh_call(0x04BC0, args=(7, 0x1234, 0xABCD))
    base7 = _R + 0x164C + 7 * 16
    p7 = _st.unpack_from('<I', bytes(emu2.uc.mem_read(base7 + 8, 4)))[0]
    assert p7 == 0, f'idx=7: expected skip, ptr={p7:#x}'


# --- E2-batch26: инициализация event-кольца ---
@t(0x04BE8, 'E2-b26: 0x04be8 — init event-кольца. u32@0xB4C=0; для i=0..5: byte@(0x164C+i*16)=0, u32@(0x164C+i*16+4)=0xFFFFFFFF, byte@(0x164C+i*16+1)=0. Вериф: pre-set -> все очищены.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    pre = [(_R + 0xB4C, b'\x11\x22\x33\x44'),
           (_R + 0x164C + 2 * 16, b'\xAA\xBB\xCC\xDD\xEE\xFF\x00\x00')]
    r0, emu = _fresh_call(0x04BE8, extra_ram=pre)
    uc = emu.uc
    idx = _st.unpack_from('<I', bytes(uc.mem_read(_R + 0xB4C, 4)))[0]
    assert idx == 0, f'index: got {idx:#x} want 0'
    for i in range(6):
        base = _R + 0x164C + i * 16
        f0 = uc.mem_read(base + 0, 1)[0]
        f1 = uc.mem_read(base + 1, 1)[0]
        sent = _st.unpack_from('<I', bytes(uc.mem_read(base + 4, 4)))[0]
        assert f0 == 0 and f1 == 0 and sent == 0xFFFFFFFF, \
            f'slot {i}: f0={f0:#x} f1={f1:#x} sent={sent:#x}'


# --- E2-batch27: merge struct-полей (чистые arg-указатели) ---
@t(0x04F70, 'E2-b27: 0x04f70 — merge: dst[0]=(dst[0]&~0x7FF0)|OR(src[+8,+10..+28]); dst[+4]=src[+0xC]; dst[+8]=src[0]. Вериф OR-агрегация + copy (2 init).')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    dst = _R + 0x100; src = _R + 0x200
    vals = {0x8: 1, 0x10: 2, 0x14: 4, 0x18: 8, 0x1c: 0x10, 0x20: 0x20, 0x24: 0x40, 0x28: 0x80}
    srcbuf = bytearray(0x30)
    for o, v in vals.items():
        _st.pack_into('<I', srcbuf, o, v)
    _st.pack_into('<I', srcbuf, 0x0C, 0xDEADBEEF)
    _st.pack_into('<I', srcbuf, 0x0, 0x12345678)
    for init in (0x7FF0, 0x88FF):
        dstbuf = bytearray(0x10); _st.pack_into('<I', dstbuf, 0, init)
        r0, emu = _fresh_call(0x04F70, args=(dst, src), extra_ram=[(dst, bytes(dstbuf)), (src, bytes(srcbuf))])
        uc = emu.uc
        d0 = _st.unpack_from('<I', bytes(uc.mem_read(dst + 0, 4)))[0]
        d4 = _st.unpack_from('<I', bytes(uc.mem_read(dst + 4, 4)))[0]
        d8 = _st.unpack_from('<I', bytes(uc.mem_read(dst + 8, 4)))[0]
        exp_or = sum(vals.values())
        assert d0 == (init & ~0x7FF0) | exp_or, f'init={init:#x}: dst[0]={d0:#x}'
        assert d4 == 0xDEADBEEF, f'dst[+4]={d4:#x}'
        assert d8 == 0x12345678, f'dst[+8]={d8:#x}'


# --- E2-batch28: u16-merge struct-полей (чистые arg-указатели) ---
@t(0x10734, 'E2-b28: 0x10734 — u16-merge: dst[0]=(dst[0]&0x3040)|OR(src[+0..+0xe]); dst[+0x1C]&=0xF7FF; dst[+0x10]=src[+0x10]. Вериф (2 init).')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    dst = _R + 0x100; src = _R + 0x200
    srcbuf = bytearray(0x20)
    for i in range(8):
        _st.pack_into('<H', srcbuf, i * 2, 1 << i)
    _st.pack_into('<H', srcbuf, 0x10, 0xBEEF)
    exp_or = 0xFF
    for init0, init1c in [(0x3040, 0xFFFF), (0xFFFF, 0x0200)]:
        dstbuf = bytearray(0x20)
        _st.pack_into('<H', dstbuf, 0, init0)
        _st.pack_into('<H', dstbuf, 0x1C, init1c)
        r0, emu = _fresh_call(0x10734, args=(dst, src), extra_ram=[(dst, bytes(dstbuf)), (src, bytes(srcbuf))])
        uc = emu.uc
        d0 = _st.unpack_from('<H', bytes(uc.mem_read(dst + 0, 2)))[0]
        d1c = _st.unpack_from('<H', bytes(uc.mem_read(dst + 0x1C, 2)))[0]
        d10 = _st.unpack_from('<H', bytes(uc.mem_read(dst + 0x10, 2)))[0]
        assert d0 == (init0 & 0x3040) | exp_or, f'init0={init0:#x}: dst[0]={d0:#x}'
        assert d1c == init1c & 0xF7FF, f'dst[+0x1C]={d1c:#x} want {init1c & 0xF7FF:#x}'
        assert d10 == 0xBEEF, f'dst[+0x10]={d10:#x}'


# --- E2-batch29: memcpy (word-fast-path + byte-tail) ---
@t(0x19A68, 'E2-b29: 0x19a68 — memcpy(dst,src,len): word-copy если оба 4-aligned, else byte; tail по байтам. Вериф len=0..64 (aligned+unaligned).')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    for ln in (0, 1, 3, 4, 5, 7, 16, 17, 64):
        src = _R + 0x100; dst = _R + 0x300
        buf = bytes((i * 7 + 3) & 0xFF for i in range(ln))
        dstpre = bytes([0xAA] * (ln + 4))
        r0, emu = _fresh_call(0x19A68, args=(dst, src, ln), extra_ram=[(src, buf), (dst, dstpre)])
        got = bytes(emu.uc.mem_read(dst, ln)) if ln else b''
        assert got == buf, f'len={ln}: got={got.hex()} want={buf.hex()}'


# --- E2-batch30: bit-field containment check ---
@t(0x09874, 'E2-b30: 0x09874 — bit-field check: top-nibble(r1)==0 -> поле u32@(ptr+0x18), mask=r1>>16; else поле u32@(ptr+0x14), mask=r1&0xFFFFFF. Вериф: 1 если (*field & mask)!=0 (7 кейсов).')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    ptr = _R + 0x200
    def chk(r1, f14, f18):
        pre = [(ptr + 0x14, _st.pack('<I', f14)), (ptr + 0x18, _st.pack('<I', f18))]
        r0, _e = _fresh_call(0x09874, args=(ptr, r1), extra_ram=pre)
        return r0 & 1
    cases = [
        (0x00010000, 0, 0x01, 1), (0x00010000, 0, 0x00, 0),
        (0x00FF0000, 0, 0x80, 1), (0xF00000FF, 0x01, 0, 1),
        (0xF00000FF, 0x00, 0, 0), (0x100000F0, 0xF0, 0, 1),
        (0x100000F0, 0x0F, 0, 0),
    ]
    for r1, f14, f18, exp in cases:
        got = chk(r1, f14, f18)
        assert got == exp, f'r1={r1:#x} f14={f14:#x} f18={f18:#x}: got {got} want {exp}'


# --- E2-batch31: two-part bit check ---
@t(0x130F2, 'E2-b31: 0x130f2 — two-part bit check. group=(code>>5)&7: 1->+0xC, 2->+0x10, else->+0x14; maskA=1<<(code&0x1F). PartB: ptr[0], maskB=1<<(code>>8). Вериф: 1 если оба бита set (6 кейсов).')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    ptr = _R + 0x200
    def chk(code, f0, fc, f10, f14):
        pre = [(ptr + 0, _st.pack('<H', f0)), (ptr + 0xC, _st.pack('<H', fc)),
               (ptr + 0x10, _st.pack('<H', f10)), (ptr + 0x14, _st.pack('<H', f14))]
        r0, _e = _fresh_call(0x130F2, args=(ptr, code), extra_ram=pre)
        return r0 & 1
    cases = [
        (0x124, 0x02, 0x10, 0, 0, 1), (0x124, 0x02, 0x00, 0, 0, 0),
        (0x124, 0x00, 0x10, 0, 0, 0), (0x144, 0x02, 0, 0x10, 0, 1),
        (0x144, 0x02, 0, 0x00, 0, 0), (0x104, 0x02, 0, 0, 0x10, 1),
    ]
    for code, f0, fc, f10, f14, exp in cases:
        got = chk(code, f0, fc, f10, f14)
        assert got == exp, f'code={code:#x} f0={f0:#x} fc={fc:#x} f10={f10:#x} f14={f14:#x}: got {got} want {exp}'


# --- E2-batch32: XOR 16-байт блоков ---
@t(0x1A5FA, 'E2-b32: 0x1a5fa — XOR-блок: dst[r3*4+i] ^= src[(4*idx+r3)*4+i], r3,i=0..3 (16 байт). Вериф idx=0,1,2.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    dst = _R + 0x100; src = _R + 0x300
    srcbuf = bytes((i * 5 + 1) & 0xFF for i in range(64))
    for idx in (0, 1, 2):
        dstpre = bytes([0xFF] * 20)
        r0, emu = _fresh_call(0x1A5FA, args=(idx, dst, src), extra_ram=[(dst, dstpre), (src, srcbuf)])
        got = bytes(emu.uc.mem_read(dst, 16))
        exp = bytearray(16)
        for r3 in range(4):
            for i in range(4):
                exp[r3 * 4 + i] = (0xFF ^ srcbuf[(4 * idx + r3) * 4 + i]) & 0xFF
        assert got == bytes(exp), f'idx={idx}: got={got.hex()} want={bytes(exp).hex()}'


# --- E2-batch33: exponent-ramp (2^(t-0x7F)) ---
@t(0x1A010, 'E2-b33: 0x1a010 — exponent-ramp: для r0=(t<<23): t<0x7F -> 0; else 1<<(t-0x7F) (линейный рост 2^0..2^23). Вериф sweep t=0x78..0x96.')
def _(run, rng):
    for t in range(0x78, 0x97):
        r0 = t << 23
        r, _e = _fresh_call(0x1A010, args=(r0,))
        exp = 0 if t < 0x7F else (1 << (t - 0x7F))
        assert r == exp, f't={t:#x}: got {r:#x} want {exp:#x}'


# --- E2-batch34: u16 bit-check + 24-bit field all-set check ---
@t(0x10718, 'E2-b34: 0x10718 — u16 bit-check: 1 если (u16@(ptr+8) & mask)!=0. Вериф 3 кейса.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    ptr = _R + 0x200
    def a(mask, val):
        r0, _e = _fresh_call(0x10718, args=(ptr, mask), extra_ram=[(ptr + 8, _st.pack('<H', val))])
        return r0 & 1
    for mask, val, exp in [(0x0001, 0x0001, 1), (0x0001, 0x0000, 0), (0x0100, 0xFF00, 1)]:
        got = a(mask, val)
        assert got == exp, f'mask={mask:#x} val={val:#x}: got {got} want {exp}'

@t(0x09794, 'E2-b34: 0x09794 — 24-битное поле (u16@+0x14 | u16@+0x18<<16)&0xFFFFFF; 1 если (field&mask)==mask. Вериф 4 кейса.')
def _(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    ptr = _R + 0x200
    def b(mask, f14, f18):
        r0, _e = _fresh_call(0x09794, args=(ptr, mask),
                             extra_ram=[(ptr + 0x14, _st.pack('<H', f14)), (ptr + 0x18, _st.pack('<H', f18))])
        return r0 & 1
    for mask, f14, f18, exp in [(0x00FF, 0x00FF, 0, 1), (0x0100, 0x00FF, 0, 0),
                                 (0x00FF0000, 0xFFFF, 0xFF, 1), (0x00FF00FF, 0xFFFF, 0xFF, 1)]:
        got = b(mask, f14, f18)
        assert got == exp, f'mask={mask:#x} f14={f14:#x} f18={f18:#x}: got {got} want {exp}'


# --- E2-batch35: periph const-write / bit-set via pool pointers ---
@t(0x05CC0, 'E2-b35: 0x05cc0 — пишет константу 0xAAAA в periph[0x40003000] (pool-указатель). Вериф значение после вызова.')
def _(run, rng):
    import struct as _st
    r0, emu = _fresh_call(0x05CC0)
    got = _st.unpack('<I', bytes(emu.uc.mem_read(0x40003000, 4)))[0]
    assert got == 0xAAAA, f'periph[0x40003000]={got:#x} want 0xaaaa'

@t(0x1A5C4, 'E2-b35: 0x1a5c4 — ставит бит3 (0x8) в u32@periph[0x40012418] (pool-base 0x40012400). Вериф pre=0/0xFF.')
def _(run, rng):
    import struct as _st
    for pre, exp in [(0, 0x8), (0xFF, 0xFF)]:
        r0, emu = _fresh_call(0x1A5C4, extra_mem=[(0x40012418, _st.pack('<I', pre))])
        got = _st.unpack('<I', bytes(emu.uc.mem_read(0x40012418, 4)))[0]
        assert got == exp, f'pre={pre:#x}: got {got:#x} want {exp:#x}'

@t(0x1A5D4, 'E2-b35: 0x1a5d4 — ставит бит5 (0x20) в u32@periph[0x40012418]. Вериф pre=0/0x0F.')
def _(run, rng):
    import struct as _st
    for pre, exp in [(0, 0x20), (0x0F, 0x2F)]:
        r0, emu = _fresh_call(0x1A5D4, extra_mem=[(0x40012418, _st.pack('<I', pre))])
        got = _st.unpack('<I', bytes(emu.uc.mem_read(0x40012418, 4)))[0]
        assert got == exp, f'pre={pre:#x}: got {got:#x} want {exp:#x}'
