# -*- coding: utf-8 -*-
# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-batch1..12 (4903-5264)."""
from fv_core import *  # noqa: F401,F403
from fv_core import _fresh_call, _intercept  # noqa: F401
# --- E2-batch1: пофункционная кампания — чистые/простые функции ---
@t(0x01E34, 'E2-b1: 0x01e34 — сумма байтов mod 256. 0x01e34(ptr=r0, n=r1) -> r0 = (Σ buf[i], i=0..n-1) & 0xFF. Чистая функция. Вериф 4/4.')
def _(run, rng):
    """Emulator test @ 0x1e34: E2-b1: 0x01e34 — сумма байтов mod 256. 0x01e34(ptr=r0, n=r1) -> r0 = (Σ buf[i], i=0..n-1) & 0xFF. Чистая функция. Вериф 4/4..
    Тест эмулятора @ 0x1e34: E2-b1: 0x01e34 — сумма байтов mod 256. 0x01e34(ptr=r0, n=r1) -> r0 = (Σ buf[i], i=0..n-1) & 0xFF. Чистая функция. Вериф 4/4..
    """
    from emulator.mcu_emu import RAM as _R
    ok = 0
    for buf, n in [([1, 2, 3, 4, 5], 5), ([250, 250], 2),
                   ([0] * 3, 3), ([7, 8, 9, 10], 4)]:
        p = _R + 0x3000
        r0, _emu = _fresh_call(0x01E34, args=(p, n), extra_ram=[(p, bytes(buf))])
        assert r0 == (sum(buf) & 0xFF), f'buf={buf}: got {r0} want {sum(buf) & 0xFF}'
        ok += 1
    assert ok >= 4


@t(0x015AA, 'E2-b1: 0x015aa — packed-field setter. 0x015aa(struct=r0, field_id=r1, selector=r2, value=r3): 3-бит поле (из value): id==0x12->[+0x5c]b[2:0]; id>9->[+0xc]b[(id-0xa)*3..3]; id<=9->[+0x10]b[id*3..3]. 5-бит поле (из field_id), по selector: <7->[+0x34]b[(sel-1)*5..5]; <0xd->[+0x30]b[(sel-7)*5..5]; else->[+0x2c]b[(sel-0xd)*5..5]. Чистая (struct в r0). Вериф 6/6.')
def _(run, rng):
    """Emulator test @ 0x15aa: E2-b1: 0x015aa — packed-field setter. 0x015aa(struct=r0, field_id=r1, selector=r2, value=r3): 3-бит поле (из value): id==0x12->[+0x5c]b[2:0]; id>9->[+0xc]b[(id-0xa)*3..3]; id<=9->[+0x10]b[id*3..3]. 5-бит поле (из field_id), по selector: <7->[+0x34]b[(sel-1)*5..5]; <0xd->[+0x30]b[(sel-7)*5..5]; else->[+0x2c]b[(sel-0xd)*5..5]. Чистая (struct в r0). Вериф 6/6..
    Тест эмулятора @ 0x15aa: E2-b1: 0x015aa — packed-field setter. 0x015aa(struct=r0, field_id=r1, selector=r2, value=r3): 3-бит поле (из value): id==0x12->[+0x5c]b[2:0]; id>9->[+0xc]b[(id-0xa)*3..3]; id<=9->[+0x10]b[id*3..3]. 5-бит поле (из field_id), по selector: <7->[+0x34]b[(sel-1)*5..5]; <0xd->[+0x30]b[(sel-7)*5..5]; else->[+0x2c]b[(sel-0xd)*5..5]. Чистая (struct в r0). Вериф 6/6..
    """
    import struct as _st
    from emulator.mcu_emu import RAM as _R
    S = _R + 0x3000

    def runf(r1, r5, r3):
        """The runf function of the script.
        Функция runf скрипта.
        """
        emu = _fresh_call(0x015AA, args=(S, r1, r5, r3))[1]
        u32 = lambda off: _st.unpack('<I', bytes(emu.uc.mem_read(S + off, 4)))[0]
        return u32(0x5c), u32(0xc), u32(0x10), u32(0x34), u32(0x30), u32(0x2c)
    # 3-бит: id==0x12 -> [0x5c] low3 = value
    assert runf(0x12, 1, 5)[0] == 5
    # 3-бит: id<=9 -> [0x10] bit(id*3) w3 = value
    assert runf(2, 1, 7)[2] == (7 & 7) << 6
    # 3-бит: id>9 -> [0xc] bit((id-0xa)*3) w3 = value
    assert runf(0xb, 1, 4)[1] == (4 & 7) << 3
    # 5-бит: selector<7 -> [0x34] bit((sel-1)*5) w5 = field_id
    assert runf(20, 1, 0)[3] == (20 & 0x1F)
    # 5-бит: selector in [7,0xd) -> [0x30] bit((sel-7)*5) w5 = field_id
    assert runf(30, 8, 0)[4] == (30 & 0x1F) << 5
    # 5-бит: selector>=0xd -> [0x2c] bit((sel-0xd)*5) w5 = field_id
    assert runf(9, 0xe, 0)[5] == (9 & 0x1F) << 5



# --- E2-batch2: I2C2-wr семья (22 тонких делегатора -> 0x1c61) ---
# Контракт (вериф bl-intercept): 0x1c61(op=8, reg=r1, buf=&u32@0x16XX=r2, len=r3).
_I2C2_WR = {
    0x020c4: (0x38, 2), 0x02138: (0x36, 2), 0x021dc: (0x12, 2), 0x021f0: (0x14, 2),
    0x02204: (0x16, 2), 0x02218: (0x18, 2), 0x0222c: (0x1a, 2), 0x02240: (0x1c, 2),
    0x02254: (0x1e, 2), 0x02268: (0x20, 2), 0x0227c: (0x22, 2), 0x02290: (0x24, 2),
    0x022a4: (0x26, 2), 0x022b8: (0x28, 2), 0x022cc: (0x2a, 2), 0x022e0: (0x32, 2),
    0x022f4: (0x3a, 2), 0x02308: (0x7f, 1), 0x0231c: (0x3, 1), 0x02330: (0x5, 1),
    0x02344: (0x7, 1), 0x02358: (0x70, 2),
}


def _mk_i2c2_wr(addr, reg, ln):
    """The helper function (_mk_i2c2_wr).
    Вспомогательная функция (_mk_i2c2_wr).
    """
    def _test(run, rng):
        """The helper function (_test).
        Вспомогательная функция (_test).
        """
        from emulator.mcu_emu import RAM as _R
        cap, _emu = _intercept(addr, 0x1C61)
        assert cap.get('r0') == 8, f'0x{addr:05x}: r0={cap.get("r0"):#x} want 0x8'
        assert cap.get('r1') == reg, f'0x{addr:05x}: reg={cap.get("r1"):#x} want 0x{reg:x}'
        assert cap.get('r3') == ln, f'0x{addr:05x}: len={cap.get("r3")} want {ln}'
        assert cap.get('r2', 0) >= _R, f'0x{addr:05x}: buf не в RAM'
    return _test


for _addr, (_reg, _ln) in sorted(_I2C2_WR.items()):
    t(_addr, f'E2-b2: I2C2-wr 0x{_addr:05x} -> 0x1c61(op=8, reg=0x{_reg:x}, len={_ln}) [bl-intercept]')(_mk_i2c2_wr(_addr, _reg, _ln))


# --- E2-batch3: median (выборка) + I2C2-read делегатор ---
@t(0x0170C, 'E2-b3: 0x0170c — выборка ADC-сэмпла по индексу. 0x0170c(arg=r0) -> r0 = u16[RAM+0xB7E + arg*2] (arg<2). Копирует выбранный сэмпл в 7 слотов локального массива, sort+center (no-op на константе) -> возвращает его. Каталог «медиана из 7» неточен. Вериф 10/10.')
def _(run, rng):
    """Emulator test @ 0x170c: E2-b3: 0x0170c — выборка ADC-сэмпла по индексу. 0x0170c(arg=r0) -> r0 = u16[RAM+0xB7E + arg*2] (arg<2). Копирует выбранный сэмпл в 7 слотов локального массива, sort+center (no-op на константе) -> возвращает его. Каталог «медиана из 7» неточен. Вериф 10/10..
    Тест эмулятора @ 0x170c: E2-b3: 0x0170c — выборка ADC-сэмпла по индексу. 0x0170c(arg=r0) -> r0 = u16[RAM+0xB7E + arg*2] (arg<2). Копирует выбранный сэмпл в 7 слотов локального массива, sort+center (no-op на константе) -> возвращает его. Каталог «медиана из 7» неточен. Вериф 10/10..
    """
    import struct as _st
    from emulator.mcu_emu import RAM as _R
    for arg in (0, 1):
        for _ in range(3):
            vals = [rng.getrandbits(16) for _ in range(7)]
            r0, _emu = _fresh_call(0x0170C, args=(arg,),
                                   extra_ram=[(_R + 0xB7E, _st.pack('<7H', *vals))])
            assert r0 == vals[arg], f'arg={arg}: got {r0:#x} want {vals[arg]:#x}'


@t(0x01BDC, 'E2-b3: 0x01bdc — I2C2 read (code16). 0x01bdc(code=r0) -> bl 0x1e73(op=8, dev=0x3e, r2=1, buf=[sp+4]); buf = [code&0xFF, code>>8] (LE). Вериф bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x1bdc: E2-b3: 0x01bdc — I2C2 read (code16). 0x01bdc(code=r0) -> bl 0x1e73(op=8, dev=0x3e, r2=1, buf=[sp+4]); buf = [code&0xFF, code>>8] (LE). Вериф bl-intercept..
    Тест эмулятора @ 0x1bdc: E2-b3: 0x01bdc — I2C2 read (code16). 0x01bdc(code=r0) -> bl 0x1e73(op=8, dev=0x3e, r2=1, buf=[sp+4]); buf = [code&0xFF, code>>8] (LE). Вериф bl-intercept..
    """
    for code in (0x1234, 0xABCD, 0x00FF):
        cap, emu = _intercept(0x01BDC, 0x1E73, arg=code)
        assert cap.get('r0') == 8 and cap.get('r1') == 0x3e and cap.get('r2') == 1, \
            f'code={code:#06x}: {cap}'
        buf = bytes(emu.uc.mem_read(cap['r3'], 2))
        assert buf == code.to_bytes(2, 'little'), f'code={code:#06x}: buf={buf.hex()}'


@t(0x01C1C, 'E2-b4: 0x01c1c — I2C2 read (code16, base). 0x01c1c(code=r0) -> bl 0x90a1(r0=0x40005800 [I2C2 base], op=8, dev=0x3e, buf=[sp+4]); buf=LE code. Вериф bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x1c1c: E2-b4: 0x01c1c — I2C2 read (code16, base). 0x01c1c(code=r0) -> bl 0x90a1(r0=0x40005800 [I2C2 base], op=8, dev=0x3e, buf=[sp+4]); buf=LE code. Вериф bl-intercept..
    Тест эмулятора @ 0x1c1c: E2-b4: 0x01c1c — I2C2 read (code16, base). 0x01c1c(code=r0) -> bl 0x90a1(r0=0x40005800 [I2C2 base], op=8, dev=0x3e, buf=[sp+4]); buf=LE code. Вериф bl-intercept..
    """
    for code in (0x1234, 0xABCD):
        cap, emu = _intercept(0x01C1C, 0x90A1, arg=code)
        assert cap.get('r0') == 0x40005800 and cap.get('r1') == 8 \
            and cap.get('r2') == 0x3e, f'code={code:#06x}: {cap}'
        buf = bytes(emu.uc.mem_read(cap['r3'], 2))
        assert buf == code.to_bytes(2, 'little'), f'code={code:#06x}: buf={buf.hex()}'


@t(0x01C7A, 'E2-b4: 0x01c7a — I2C2 read (arg0, code16). 0x01c7a(a0=r0, code=r1) -> bl 0x1e73(r0=a0, dev=0x3e, r2=1, buf=[sp+4]); buf=LE code. Вериф bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x1c7a: E2-b4: 0x01c7a — I2C2 read (arg0, code16). 0x01c7a(a0=r0, code=r1) -> bl 0x1e73(r0=a0, dev=0x3e, r2=1, buf=[sp+4]); buf=LE code. Вериф bl-intercept..
    Тест эмулятора @ 0x1c7a: E2-b4: 0x01c7a — I2C2 read (arg0, code16). 0x01c7a(a0=r0, code=r1) -> bl 0x1e73(r0=a0, dev=0x3e, r2=1, buf=[sp+4]); buf=LE code. Вериф bl-intercept..
    """
    for a0, code in ((0x55, 0x1234), (0xAA, 0xBE01)):
        cap, emu = _intercept(0x01C7A, 0x1E73, args=(a0, code))
        assert cap.get('r0') == a0 and cap.get('r1') == 0x3e \
            and cap.get('r2') == 1, f'a0={a0:#x} code={code:#06x}: {cap}'
        buf = bytes(emu.uc.mem_read(cap['r3'], 2))
        assert buf == code.to_bytes(2, 'little'), f'code={code:#06x}: buf={buf.hex()}'


@t(0x0218C, 'E2-b5: 0x0218c — I2C read reg 0x83. 0x0218c() -> bl 0x1c7b(op=8, reg=0x83, buf=&RAM, len=2); результат -> u16@0xB42 (если != 0xFFFF). Вериф bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x218c: E2-b5: 0x0218c — I2C read reg 0x83. 0x0218c() -> bl 0x1c7b(op=8, reg=0x83, buf=&RAM, len=2); результат -> u16@0xB42 (если != 0xFFFF). Вериф bl-intercept..
    Тест эмулятора @ 0x218c: E2-b5: 0x0218c — I2C read reg 0x83. 0x0218c() -> bl 0x1c7b(op=8, reg=0x83, buf=&RAM, len=2); результат -> u16@0xB42 (если != 0xFFFF). Вериф bl-intercept..
    """
    from emulator.mcu_emu import RAM as _R
    cap, emu = _intercept(0x0218C, 0x1C7B)
    assert cap.get('r0') == 8 and cap.get('r1') == 0x83 and cap.get('r3') == 2, f'{cap}'
    assert cap.get('r2', 0) >= _R, f'buf не в RAM: {cap}'


# --- E2-batch6: I2C2-read цепочки (тонкие делегаторы) ---
@t(0x01C60, 'E2-b6: 0x01c60 — I2C2-цепочка #1. 0x01c60() -> bl 0x1e53(r0=0, r1=0, r2=1, r3=0) [нулевой RAM-state]. Вериф bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x1c60: E2-b6: 0x01c60 — I2C2-цепочка #1. 0x01c60() -> bl 0x1e53(r0=0, r1=0, r2=1, r3=0) [нулевой RAM-state]. Вериф bl-intercept..
    Тест эмулятора @ 0x1c60: E2-b6: 0x01c60 — I2C2-цепочка #1. 0x01c60() -> bl 0x1e53(r0=0, r1=0, r2=1, r3=0) [нулевой RAM-state]. Вериф bl-intercept..
    """
    cap, _emu = _intercept(0x01C60, 0x1E53)
    assert (cap.get('r0'), cap.get('r1'), cap.get('r2'), cap.get('r3')) == (0, 0, 1, 0), f'{cap}'


@t(0x01E52, 'E2-b6: 0x01e52 — I2C2-цепочка #2. 0x01e52() -> bl 0x214d(r0=0, r1=0, r2=0, r3=0) [нулевой RAM-state]. Вериф bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x1e52: E2-b6: 0x01e52 — I2C2-цепочка #2. 0x01e52() -> bl 0x214d(r0=0, r1=0, r2=0, r3=0) [нулевой RAM-state]. Вериф bl-intercept..
    Тест эмулятора @ 0x1e52: E2-b6: 0x01e52 — I2C2-цепочка #2. 0x01e52() -> bl 0x214d(r0=0, r1=0, r2=0, r3=0) [нулевой RAM-state]. Вериф bl-intercept..
    """
    cap, _emu = _intercept(0x01E52, 0x214D)
    assert (cap.get('r0'), cap.get('r1'), cap.get('r2'), cap.get('r3')) == (0, 0, 0, 0), f'{cap}'


@t(0x01E72, 'E2-b6: 0x01e72 — I2C2-цепочка #3. 0x01e72() -> bl 0x2731(r0=0, r1=0, r2=0, r3=0) [нулевой RAM-state]. Вериф bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x1e72: E2-b6: 0x01e72 — I2C2-цепочка #3. 0x01e72() -> bl 0x2731(r0=0, r1=0, r2=0, r3=0) [нулевой RAM-state]. Вериф bl-intercept..
    Тест эмулятора @ 0x1e72: E2-b6: 0x01e72 — I2C2-цепочка #3. 0x01e72() -> bl 0x2731(r0=0, r1=0, r2=0, r3=0) [нулевой RAM-state]. Вериф bl-intercept..
    """
    cap, _emu = _intercept(0x01E72, 0x2731)
    assert (cap.get('r0'), cap.get('r1'), cap.get('r2'), cap.get('r3')) == (0, 0, 0, 0), f'{cap}'


# --- E2-batch7: CRC-семья (чистые чексаумы, вериф по Python-референсу) ---
def _crc32z(b):
    """The helper function (_crc32z).
    Вспомогательная функция (_crc32z).
    """
    import zlib
    return zlib.crc32(b) & 0xFFFFFFFF


def _crc16_1021(b, init=0):
    """The helper function (_crc16_1021).
    Вспомогательная функция (_crc16_1021).
    """
    c = init
    for x in b:
        c ^= x << 8
        for _ in range(8):
            c = ((c << 1) ^ 0x1021) & 0xFFFF if c & 0x8000 else (c << 1) & 0xFFFF
    return c


def _crc16_a001(b):
    """The helper function (_crc16_a001).
    Вспомогательная функция (_crc16_a001).
    """
    c = 0xFFFF
    for x in b:
        c ^= x
        for _ in range(8):
            c = (c >> 1) ^ 0xA001 if c & 1 else c >> 1
    return (~c) & 0xFFFF


_CRC_BUFS = [b'', b'123456789', b'\x00\x01\x02', b'hello world', bytes(range(20))]


@t(0x03C04, 'E2-b7: 0x03c04 — CRC-32/zlib. 0x03c04(buf=r0, len=r1, init=r2) -> r0 = crc32 (init=0 -> 0xFFFFFFFF). Вериф по zlib 5/5.')
def _(run, rng):
    """Emulator test @ 0x3c04: E2-b7: 0x03c04 — CRC-32/zlib. 0x03c04(buf=r0, len=r1, init=r2) -> r0 = crc32 (init=0 -> 0xFFFFFFFF). Вериф по zlib 5/5..
    Тест эмулятора @ 0x3c04: E2-b7: 0x03c04 — CRC-32/zlib. 0x03c04(buf=r0, len=r1, init=r2) -> r0 = crc32 (init=0 -> 0xFFFFFFFF). Вериф по zlib 5/5..
    """
    from emulator.mcu_emu import RAM as _R
    P = _R + 0x3000
    for b in _CRC_BUFS:
        r0, _emu = _fresh_call(0x03C04, args=(P, len(b), 0), extra_ram=[(P, b)])
        assert (r0 & 0xFFFFFFFF) == _crc32z(b), f'{b!r}: got {r0:#x} want {_crc32z(b):#x}'


@t(0x03B82, 'E2-b7: 0x03b82 — CRC-16 0x1021 MSB-first (init=0). 0x03b82(buf=r0, len=r1) -> r0 = u16 crc. Вериф 5/5.')
def _(run, rng):
    """Emulator test @ 0x3b82: E2-b7: 0x03b82 — CRC-16 0x1021 MSB-first (init=0). 0x03b82(buf=r0, len=r1) -> r0 = u16 crc. Вериф 5/5..
    Тест эмулятора @ 0x3b82: E2-b7: 0x03b82 — CRC-16 0x1021 MSB-first (init=0). 0x03b82(buf=r0, len=r1) -> r0 = u16 crc. Вериф 5/5..
    """
    from emulator.mcu_emu import RAM as _R
    P = _R + 0x3000
    for b in _CRC_BUFS:
        r0, _emu = _fresh_call(0x03B82, args=(P, len(b)), extra_ram=[(P, b)])
        assert (r0 & 0xFFFF) == _crc16_1021(b), f'{b!r}: got {r0:#x} want {_crc16_1021(b):#x}'


@t(0x03BC4, 'E2-b7: 0x03bc4 — CRC-16 0x1021 MSB-first (init в r0). 0x03bc4(init=r0, buf=r1, len=r2) -> r0 = u16 crc. Вериф 5/5.')
def _(run, rng):
    """Emulator test @ 0x3bc4: E2-b7: 0x03bc4 — CRC-16 0x1021 MSB-first (init в r0). 0x03bc4(init=r0, buf=r1, len=r2) -> r0 = u16 crc. Вериф 5/5..
    Тест эмулятора @ 0x3bc4: E2-b7: 0x03bc4 — CRC-16 0x1021 MSB-first (init в r0). 0x03bc4(init=r0, buf=r1, len=r2) -> r0 = u16 crc. Вериф 5/5..
    """
    from emulator.mcu_emu import RAM as _R
    P = _R + 0x3000
    for b in _CRC_BUFS:
        r0, _emu = _fresh_call(0x03BC4, args=(0, P, len(b)), extra_ram=[(P, b)])
        assert (r0 & 0xFFFF) == _crc16_1021(b), f'{b!r}: got {r0:#x} want {_crc16_1021(b):#x}'


@t(0x03B42, 'E2-b7: 0x03b42 — CRC-16 отражённый (poly 0xA001, init 0xFFFF, xorout ~). 0x03b42(buf=r0, len=r1) -> r0 = u16 crc. Вериф 5/5.')
def _(run, rng):
    """Emulator test @ 0x3b42: E2-b7: 0x03b42 — CRC-16 отражённый (poly 0xA001, init 0xFFFF, xorout ~). 0x03b42(buf=r0, len=r1) -> r0 = u16 crc. Вериф 5/5..
    Тест эмулятора @ 0x3b42: E2-b7: 0x03b42 — CRC-16 отражённый (poly 0xA001, init 0xFFFF, xorout ~). 0x03b42(buf=r0, len=r1) -> r0 = u16 crc. Вериф 5/5..
    """
    from emulator.mcu_emu import RAM as _R
    P = _R + 0x3000
    for b in _CRC_BUFS:
        r0, _emu = _fresh_call(0x03B42, args=(P, len(b)), extra_ram=[(P, b)])
        assert (r0 & 0xFFFF) == _crc16_a001(b), f'{b!r}: got {r0:#x} want {_crc16_a001(b):#x}'


# --- E2-batch8: табличные CRC-16 (референс из flash-памяти emu) ---
@t(0x03C4C, 'E2-b8: 0x03c4c — CRC-16 табличный. 0x03c4c(buf=r0,len=r1)->u16; tbl@flash 0x19784 (256 u16); idx=byte^(crc>>8); crc=(tbl[idx]^(crc<<8))&0xFFFF. Вериф по flash-таблице 5/5.')
def _(run, rng):
    """Emulator test @ 0x3c4c: E2-b8: 0x03c4c — CRC-16 табличный. 0x03c4c(buf=r0,len=r1)->u16; tbl@flash 0x19784 (256 u16); idx=byte^(crc>>8); crc=(tbl[idx]^(crc<<8))&0xFFFF. Вериф по flash-таблице 5/5..
    Тест эмулятора @ 0x3c4c: E2-b8: 0x03c4c — CRC-16 табличный. 0x03c4c(buf=r0,len=r1)->u16; tbl@flash 0x19784 (256 u16); idx=byte^(crc>>8); crc=(tbl[idx]^(crc<<8))&0xFFFF. Вериф по flash-таблице 5/5..
    """
    import struct as _st
    from emulator.mcu_emu import RAM as _R, FLASH0 as _F0
    P = _R + 0x3000
    tbl = _st.unpack('<256H', bytes(run.emu.uc.mem_read(_F0 + 0x19784, 512)))
    for b in _CRC_BUFS:
        r0, _emu = _fresh_call(0x03C4C, args=(P, len(b)), extra_ram=[(P, b)])
        c = 0
        for x in b:
            c = (tbl[x ^ (c >> 8)] ^ (c << 8)) & 0xFFFF
        assert (r0 & 0xFFFF) == c, f'{b!r}: got {r0:#x} want {c:#x}'


@t(0x08A50, 'E2-b8: 0x08a50 — dual-table CRC-16. 0x08a50(buf=r0,len=r1)->u16; t1@flash 0x19584 (high), t2@0x19684 (low); hi=lo=0xFF; idx=byte^hi; hi=t1[idx]^lo; lo=t2[idx]; crc=(hi<<8)|lo. Вериф по flash-таблицам 5/5.')
def _(run, rng):
    """Emulator test @ 0x8a50: E2-b8: 0x08a50 — dual-table CRC-16. 0x08a50(buf=r0,len=r1)->u16; t1@flash 0x19584 (high), t2@0x19684 (low); hi=lo=0xFF; idx=byte^hi; hi=t1[idx]^lo; lo=t2[idx]; crc=(hi<<8)|lo. Вериф по flash-таблицам 5/5..
    Тест эмулятора @ 0x8a50: E2-b8: 0x08a50 — dual-table CRC-16. 0x08a50(buf=r0,len=r1)->u16; t1@flash 0x19584 (high), t2@0x19684 (low); hi=lo=0xFF; idx=byte^hi; hi=t1[idx]^lo; lo=t2[idx]; crc=(hi<<8)|lo. Вериф по flash-таблицам 5/5..
    """
    from emulator.mcu_emu import RAM as _R, FLASH0 as _F0
    P = _R + 0x3000
    t1 = bytes(run.emu.uc.mem_read(_F0 + 0x19584, 256))
    t2 = bytes(run.emu.uc.mem_read(_F0 + 0x19684, 256))
    for b in _CRC_BUFS:
        r0, _emu = _fresh_call(0x08A50, args=(P, len(b)), extra_ram=[(P, b)])
        hi = lo = 0xFF
        for x in b:
            i = x ^ hi
            hi = t1[i] ^ lo
            lo = t2[i]
        c = ((hi << 8) & 0xFF00) | lo
        assert (r0 & 0xFFFF) == c, f'{b!r}: got {r0:#x} want {c:#x}'


# --- E2-batch9: byte bit-permutation + NOT ---
@t(0x0BF58, 'E2-b9: 0x0bf58 — byte bit-permutation + NOT. 0x0bf58(ptr=r0, sel=r1, mode=r2), mode=1: out=RAM+0x17F9C = ~((b1<<3)|(b0<<2)|(b3<<1)|b2)&0xFF, затем маска по sel (0->0xFE,1->0xFD,2->0xFB,3->0xF7; иначе 0xFF); bN=бит N байта [ptr]. Функция также инициализирует соседний struct. Вериф по формуле.')
def _(run, rng):
    """Emulator test @ 0xbf58: E2-b9: 0x0bf58 — byte bit-permutation + NOT. 0x0bf58(ptr=r0, sel=r1, mode=r2), mode=1: out=RAM+0x17F9C = ~((b1<<3)|(b0<<2)|(b3<<1)|b2)&0xFF, затем маска по sel (0->0xFE,1->0xFD,2->0xFB,3->0xF7; иначе 0xFF); bN=бит N байта [ptr]. Функция также инициализирует соседний struct. Вериф по формуле..
    Тест эмулятора @ 0xbf58: E2-b9: 0x0bf58 — byte bit-permutation + NOT. 0x0bf58(ptr=r0, sel=r1, mode=r2), mode=1: out=RAM+0x17F9C = ~((b1<<3)|(b0<<2)|(b3<<1)|b2)&0xFF, затем маска по sel (0->0xFE,1->0xFD,2->0xFB,3->0xF7; иначе 0xFF); bN=бит N байта [ptr]. Функция также инициализирует соседний struct. Вериф по формуле..
    """
    from emulator.mcu_emu import RAM as _R
    P = _R + 0x3000

    def bitperm(b, sel):
        """The bitperm function of the script.
        Функция bitperm скрипта.
        """
        p = (~(((b >> 1) & 1) << 3 | (b & 1) << 2 | ((b >> 3) & 1) << 1
               | ((b >> 2) & 1))) & 0xFF
        m = {0: 0xFE, 1: 0xFD, 2: 0xFB, 3: 0xF7}
        return p & m[sel] if sel in m else 0xFF
    for b in (0x00, 0xFF, 0x5A, 0xA5, 0x12):
        for sel in range(4):
            _r0, emu = _fresh_call(0x0BF58, args=(P, sel, 1),
                                   extra_ram=[(P, bytes([b]))])
            out = emu.uc.mem_read(_R + 0x17F9C, 1)[0]
            assert out == bitperm(b, sel), \
                f'b={b:#04x} sel={sel}: got {out:#x} want {bitperm(b, sel):#x}'


# --- E2-batch10: RCC/DMA init-делегаторы (bl-intercept первого хелпера) ---
@t(0x01580, 'E2-b10: 0x01580 — RCC ext init. Первый вызов -> 0xc491(r0=0x100). bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x1580: E2-b10: 0x01580 — RCC ext init. Первый вызов -> 0xc491(r0=0x100). bl-intercept..
    Тест эмулятора @ 0x1580: E2-b10: 0x01580 — RCC ext init. Первый вызов -> 0xc491(r0=0x100). bl-intercept..
    """
    cap, _emu = _intercept(0x01580, 0xC491)
    assert cap.get('r0') == 0x100, f'{cap}'


@t(0x01940, 'E2-b10: 0x01940 — RCC ext init #2. Первый вызов -> 0xc625(r0=1, r1=1). bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x1940: E2-b10: 0x01940 — RCC ext init #2. Первый вызов -> 0xc625(r0=1, r1=1). bl-intercept..
    Тест эмулятора @ 0x1940: E2-b10: 0x01940 — RCC ext init #2. Первый вызов -> 0xc625(r0=1, r1=1). bl-intercept..
    """
    cap, _emu = _intercept(0x01940, 0xC625)
    assert cap.get('r0') == 1 and cap.get('r1') == 1, f'{cap}'


@t(0x016D4, 'E2-b10: 0x016d4 — DMA1 reset. Первый вызов -> 0x1941(r0=0) [RCC clock-enable пролог]. bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x16d4: E2-b10: 0x016d4 — DMA1 reset. Первый вызов -> 0x1941(r0=0) [RCC clock-enable пролог]. bl-intercept..
    Тест эмулятора @ 0x16d4: E2-b10: 0x016d4 — DMA1 reset. Первый вызов -> 0x1941(r0=0) [RCC clock-enable пролог]. bl-intercept..
    """
    cap, _emu = _intercept(0x016D4, 0x1941)
    assert cap.get('r0') == 0, f'{cap}'


@t(0x0175C, 'E2-b10: 0x0175c — DMA1 enable. Первый вызов -> 0x1941(r0=0) [пролог]; затем цикл i<2: 0x1859/0x1671/0x18fd. bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x175c: E2-b10: 0x0175c — DMA1 enable. Первый вызов -> 0x1941(r0=0) [пролог]; затем цикл i<2: 0x1859/0x1671/0x18fd. bl-intercept..
    Тест эмулятора @ 0x175c: E2-b10: 0x0175c — DMA1 enable. Первый вызов -> 0x1941(r0=0) [пролог]; затем цикл i<2: 0x1859/0x1671/0x18fd. bl-intercept..
    """
    cap, _emu = _intercept(0x0175C, 0x1941)
    assert cap.get('r0') == 0, f'{cap}'


# --- E2-batch11: flash region validator + I2C2 wr ---
@t(0x080AC, 'E2-b11: 0x080ac — flash region validator. 0x080ac(base=r0, buf=r1, len=r2): return 0 если base не по align 0x800, buf==0, len==0, len>0x800, len%4!=0, или base вне [lo,hi). Вериф гейтов (5 невалидных -> 0).')
def _(run, rng):
    """Emulator test @ 0x80ac: E2-b11: 0x080ac — flash region validator. 0x080ac(base=r0, buf=r1, len=r2): return 0 если base не по align 0x800, buf==0, len==0, len>0x800, len%4!=0, или base вне [lo,hi). Вериф гейтов (5 невалидных -> 0)..
    Тест эмулятора @ 0x80ac: E2-b11: 0x080ac — flash region validator. 0x080ac(base=r0, buf=r1, len=r2): return 0 если base не по align 0x800, buf==0, len==0, len>0x800, len%4!=0, или base вне [lo,hi). Вериф гейтов (5 невалидных -> 0)..
    """
    from emulator.mcu_emu import RAM as _R
    P = _R + 0x4000
    for base, ln in ((0x8003000, 0), (0x8003000, 0x1000), (0x8003000, 6),
                     (0x8003001, 4)):
        r0, _emu = _fresh_call(0x080AC, args=(base, P, ln))
        assert r0 == 0, f'base={base:#x} len={ln:#x}: got {r0:#x} want 0'
    r0, _emu = _fresh_call(0x080AC, args=(0x8003000, 0, 4))
    assert r0 == 0, 'buf=0: got non-zero'


@t(0x02770, 'E2-b11: 0x02770 — I2C2 wr (code16,val16,len=4). 0x02770() -> bl 0x90a1(r0=0x40005800 [I2C2 base], dev=0x3e, buf). bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x2770: E2-b11: 0x02770 — I2C2 wr (code16,val16,len=4). 0x02770() -> bl 0x90a1(r0=0x40005800 [I2C2 base], dev=0x3e, buf). bl-intercept..
    Тест эмулятора @ 0x2770: E2-b11: 0x02770 — I2C2 wr (code16,val16,len=4). 0x02770() -> bl 0x90a1(r0=0x40005800 [I2C2 base], dev=0x3e, buf). bl-intercept..
    """
    cap, _emu = _intercept(0x02770, 0x90A1)
    assert cap.get('r0') == 0x40005800 and cap.get('r2') == 0x3E, f'{cap}'


# --- E2-batch12: CRC-32-обёртка + I2C-like + event varargs ---
@t(0x03940, 'E2-b12: 0x03940 — CRC-32 обёртка. 0x03940() -> bl 0x3c04(r0=0x8000000 [flash addr], r1=0x3000 [len], r2=0) -> u32@0xCC. bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x3940: E2-b12: 0x03940 — CRC-32 обёртка. 0x03940() -> bl 0x3c04(r0=0x8000000 [flash addr], r1=0x3000 [len], r2=0) -> u32@0xCC. bl-intercept..
    Тест эмулятора @ 0x3940: E2-b12: 0x03940 — CRC-32 обёртка. 0x03940() -> bl 0x3c04(r0=0x8000000 [flash addr], r1=0x3000 [len], r2=0) -> u32@0xCC. bl-intercept..
    """
    cap, _emu = _intercept(0x03940, 0x3C05)
    assert cap.get('r0') == 0x8000000 and cap.get('r1') == 0x3000, f'{cap}'


@t(0x02E84, 'E2-b12: 0x02e84 — I2C-подобный запрос. 0x02e84() -> bl 0x9874(r1=0x20000). bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x2e84: E2-b12: 0x02e84 — I2C-подобный запрос. 0x02e84() -> bl 0x9874(r1=0x20000). bl-intercept..
    Тест эмулятора @ 0x2e84: E2-b12: 0x02e84 — I2C-подобный запрос. 0x02e84() -> bl 0x9874(r1=0x20000). bl-intercept..
    """
    cap, _emu = _intercept(0x02E84, 0x9875)
    assert cap.get('r1') == 0x20000, f'{cap}'


@t(0x0307C, 'E2-b12: 0x0307c — event varargs {b,b,b,1}. 0x0307c() -> bl 0xc0b4 (event dispatch, r0=указатель на stack-буфер). bl-intercept (достигает хелпера).')
def _(run, rng):
    """Emulator test @ 0x307c: E2-b12: 0x0307c — event varargs {b,b,b,1}. 0x0307c() -> bl 0xc0b4 (event dispatch, r0=указатель на stack-буфер). bl-intercept (достигает хелпера)..
    Тест эмулятора @ 0x307c: E2-b12: 0x0307c — event varargs {b,b,b,1}. 0x0307c() -> bl 0xc0b4 (event dispatch, r0=указатель на stack-буфер). bl-intercept (достигает хелпера)..
    """
    cap, _emu = _intercept(0x0307C, 0xC0B5)
    assert 'r0' in cap, f'не достиг 0xc0b4: {cap}'
