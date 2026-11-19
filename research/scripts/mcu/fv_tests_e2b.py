# -*- coding: utf-8 -*-
# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-batch13..24 (5265-5564)."""
from fv_core import *  # noqa: F401,F403
from fv_core import _fresh_call, _intercept  # noqa: F401
# --- E2-batch13: poll / I2C init / telemetry reset / GPIO init (bl-intercept) ---
@t(0x04E08, 'E2-b13: 0x04e08 — poll. 0x04e08() -> bl 0x1bdc(r0=0x94) + задержка. bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x4e08: E2-b13: 0x04e08 — poll. 0x04e08() -> bl 0x1bdc(r0=0x94) + задержка. bl-intercept..
    Тест эмулятора @ 0x4e08: E2-b13: 0x04e08 — poll. 0x04e08() -> bl 0x1bdc(r0=0x94) + задержка. bl-intercept..
    """
    cap, _emu = _intercept(0x04E08, 0x1BDD)
    assert cap.get('r0') == 0x94, f'{cap}'


@t(0x05FB4, 'E2-b13: 0x05fb4 — I2C init. 0x05fb4() -> 0x5a38() + задержка + bl 0x1c1c(r0=0x92). bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x5fb4: E2-b13: 0x05fb4 — I2C init. 0x05fb4() -> 0x5a38() + задержка + bl 0x1c1c(r0=0x92). bl-intercept..
    Тест эмулятора @ 0x5fb4: E2-b13: 0x05fb4 — I2C init. 0x05fb4() -> 0x5a38() + задержка + bl 0x1c1c(r0=0x92). bl-intercept..
    """
    cap, _emu = _intercept(0x05FB4, 0x1C1D)
    assert cap.get('r0') == 0x92, f'{cap}'


@t(0x09AA4, 'E2-b13: 0x09aa4 — телеметрия reset. zero @0x1344 + bl 0x11d6(r0=RAM+0x1384, r1=0x4a). bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x9aa4: E2-b13: 0x09aa4 — телеметрия reset. zero @0x1344 + bl 0x11d6(r0=RAM+0x1384, r1=0x4a). bl-intercept..
    Тест эмулятора @ 0x9aa4: E2-b13: 0x09aa4 — телеметрия reset. zero @0x1344 + bl 0x11d6(r0=RAM+0x1384, r1=0x4a). bl-intercept..
    """
    cap, _emu = _intercept(0x09AA4, 0x11D7)
    assert cap.get('r0') == 0x20001384 and cap.get('r1') == 0x4A, f'{cap}'


@t(0x05B98, 'E2-b13: 0x05b98 — GPIO init. @0x40003000=0xAAAA; bl 0xc20c(r0=3, r1=0x40010818 [GPIO reg]). bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x5b98: E2-b13: 0x05b98 — GPIO init. @0x40003000=0xAAAA; bl 0xc20c(r0=3, r1=0x40010818 [GPIO reg]). bl-intercept..
    Тест эмулятора @ 0x5b98: E2-b13: 0x05b98 — GPIO init. @0x40003000=0xAAAA; bl 0xc20c(r0=3, r1=0x40010818 [GPIO reg]). bl-intercept..
    """
    cap, _emu = _intercept(0x05B98, 0xC20D)
    assert cap.get('r1') == 0x40010818, f'{cap}'


# --- E2-batch14: bulk erase + u16-обмен + retry/toggle (bl-intercept) ---
@t(0x07EE8, 'E2-b14: 0x07ee8 — bulk erase init. Инициирует stack-буфер + bl 0x11d6(ptr, r1=0x800 [сектор 0x800B]). bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x7ee8: E2-b14: 0x07ee8 — bulk erase init. Инициирует stack-буфер + bl 0x11d6(ptr, r1=0x800 [сектор 0x800B]). bl-intercept..
    Тест эмулятора @ 0x7ee8: E2-b14: 0x07ee8 — bulk erase init. Инициирует stack-буфер + bl 0x11d6(ptr, r1=0x800 [сектор 0x800B]). bl-intercept..
    """
    cap, _emu = _intercept(0x07EE8, 0x11D7)
    assert cap.get('r1') == 0x800, f'{cap}'


@t(0x07FDC, 'E2-b14: 0x07fdc — bulk erase body. Тело цикла: bl 0x11d6(ptr, r1=0x800). bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x7fdc: E2-b14: 0x07fdc — bulk erase body. Тело цикла: bl 0x11d6(ptr, r1=0x800). bl-intercept..
    Тест эмулятора @ 0x7fdc: E2-b14: 0x07fdc — bulk erase body. Тело цикла: bl 0x11d6(ptr, r1=0x800). bl-intercept..
    """
    cap, _emu = _intercept(0x07FDC, 0x11D7)
    assert cap.get('r1') == 0x800, f'{cap}'


@t(0x057F8, 'E2-b14: 0x057f8 — u16@0xCB3 -> байты @0xCB3/0xCB5 + bl 0x13bb8(r0=1). bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x57f8: E2-b14: 0x057f8 — u16@0xCB3 -> байты @0xCB3/0xCB5 + bl 0x13bb8(r0=1). bl-intercept..
    Тест эмулятора @ 0x57f8: E2-b14: 0x057f8 — u16@0xCB3 -> байты @0xCB3/0xCB5 + bl 0x13bb8(r0=1). bl-intercept..
    """
    cap, _emu = _intercept(0x057F8, 0x13BB9)
    assert cap.get('r0') == 1, f'{cap}'


@t(0x05818, 'E2-b14: 0x05818 — байты @0xCB3/0xCB5 -> u16@0xCB3 + bl 0x13bb8(r0=0). bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x5818: E2-b14: 0x05818 — байты @0xCB3/0xCB5 -> u16@0xCB3 + bl 0x13bb8(r0=0). bl-intercept..
    Тест эмулятора @ 0x5818: E2-b14: 0x05818 — байты @0xCB3/0xCB5 -> u16@0xCB3 + bl 0x13bb8(r0=0). bl-intercept..
    """
    cap, _emu = _intercept(0x05818, 0x13BB9)
    assert 'r0' in cap, f'{cap}'


@t(0x0236C, 'E2-b14: 0x0236c — retry-счётчик I2C. Успех -> bl 0x21dc; @0xA76=0, @0xA75++. bl-intercept (достигает хелпера).')
def _(run, rng):
    """Emulator test @ 0x236c: E2-b14: 0x0236c — retry-счётчик I2C. Успех -> bl 0x21dc; @0xA76=0, @0xA75++. bl-intercept (достигает хелпера)..
    Тест эмулятора @ 0x236c: E2-b14: 0x0236c — retry-счётчик I2C. Успех -> bl 0x21dc; @0xA76=0, @0xA75++. bl-intercept (достигает хелпера)..
    """
    cap, _emu = _intercept(0x0236C, 0x21DD)
    assert 'r0' in cap, f'{cap}'


@t(0x09B08, 'E2-b14: 0x09b08 — toggle bit3 byte@0xA71 (до 3 попыток, гейт 0x2a5c). bl-intercept (достигает хелпера).')
def _(run, rng):
    """Emulator test @ 0x9b08: E2-b14: 0x09b08 — toggle bit3 byte@0xA71 (до 3 попыток, гейт 0x2a5c). bl-intercept (достигает хелпера)..
    Тест эмулятора @ 0x9b08: E2-b14: 0x09b08 — toggle bit3 byte@0xA71 (до 3 попыток, гейт 0x2a5c). bl-intercept (достигает хелпера)..
    """
    cap, _emu = _intercept(0x09B08, 0x2A5D)
    assert 'r0' in cap, f'{cap}'


# --- E2-batch15: I2C2 wr/read + event + struct access (bl-intercept) ---
@t(0x0214C, 'E2-b15: 0x0214c — I2C2 write op=8. 0x0214c() -> bl 0x8f7c(r0=0x40005800 [I2C2 base], reg, buf). bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x214c: E2-b15: 0x0214c — I2C2 write op=8. 0x0214c() -> bl 0x8f7c(r0=0x40005800 [I2C2 base], reg, buf). bl-intercept..
    Тест эмулятора @ 0x214c: E2-b15: 0x0214c — I2C2 write op=8. 0x0214c() -> bl 0x8f7c(r0=0x40005800 [I2C2 base], reg, buf). bl-intercept..
    """
    cap, _emu = _intercept(0x0214C, 0x8F7D)
    assert cap.get('r0') == 0x40005800, f'{cap}'


@t(0x02730, 'E2-b15: 0x02730 — I2C2 read-путь. 0x02730() -> bl 0x9048(r0=0x40005800 [I2C2 base]). bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x2730: E2-b15: 0x02730 — I2C2 read-путь. 0x02730() -> bl 0x9048(r0=0x40005800 [I2C2 base]). bl-intercept..
    Тест эмулятора @ 0x2730: E2-b15: 0x02730 — I2C2 read-путь. 0x02730() -> bl 0x9048(r0=0x40005800 [I2C2 base]). bl-intercept..
    """
    cap, _emu = _intercept(0x02730, 0x9049)
    assert cap.get('r0') == 0x40005800, f'{cap}'


@t(0x03150, 'E2-b15: 0x03150 — event {u32=0,u16=0x7F,u32=0x136}. 0x03150() -> bl 0xcd0c (event dispatch, r0=stack-буфер). bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x3150: E2-b15: 0x03150 — event {u32=0,u16=0x7F,u32=0x136}. 0x03150() -> bl 0xcd0c (event dispatch, r0=stack-буфер). bl-intercept..
    Тест эмулятора @ 0x3150: E2-b15: 0x03150 — event {u32=0,u16=0x7F,u32=0x136}. 0x03150() -> bl 0xcd0c (event dispatch, r0=stack-буфер). bl-intercept..
    """
    cap, _emu = _intercept(0x03150, 0xCD0D)
    assert 'r0' in cap, f'{cap}'


@t(0x03970, 'E2-b15: 0x03970 — доступ к структуре @0x98. 0x03970() -> bl 0x8a90 (r0=ptr). bl-intercept.')
def _(run, rng):
    """Emulator test @ 0x3970: E2-b15: 0x03970 — доступ к структуре @0x98. 0x03970() -> bl 0x8a90 (r0=ptr). bl-intercept..
    Тест эмулятора @ 0x3970: E2-b15: 0x03970 — доступ к структуре @0x98. 0x03970() -> bl 0x8a90 (r0=ptr). bl-intercept..
    """
    cap, _emu = _intercept(0x03970, 0x8A91)
    assert 'r0' in cap, f'{cap}'


# --- E2-batch16: transaction-return (условный выход по результату транзакции) ---
@t(0x08380, 'E2-b16: 0x08380 — transaction 0x833c: если r0 -> return 0 (условный выход). bl-intercept (достигает 0x833c).')
def _(run, rng):
    """Emulator test @ 0x8380: E2-b16: 0x08380 — transaction 0x833c: если r0 -> return 0 (условный выход). bl-intercept (достигает 0x833c)..
    Тест эмулятора @ 0x8380: E2-b16: 0x08380 — transaction 0x833c: если r0 -> return 0 (условный выход). bl-intercept (достигает 0x833c)..
    """
    cap, _emu = _intercept(0x08380, 0x833D)
    assert 'r0' in cap, f'{cap}'


@t(0x084A0, 'E2-b16: 0x084a0 — transaction 0x833c: если r0==0 -> return. bl-intercept (достигает 0x833c).')
def _(run, rng):
    """Emulator test @ 0x84a0: E2-b16: 0x084a0 — transaction 0x833c: если r0==0 -> return. bl-intercept (достигает 0x833c)..
    Тест эмулятора @ 0x84a0: E2-b16: 0x084a0 — transaction 0x833c: если r0==0 -> return. bl-intercept (достигает 0x833c)..
    """
    cap, _emu = _intercept(0x084A0, 0x833D)
    assert 'r0' in cap, f'{cap}'


@t(0x0851C, 'E2-b16: 0x0851c — transaction 0x833c: если r0!=0 -> return pc. bl-intercept (достигает 0x833c).')
def _(run, rng):
    """Emulator test @ 0x851c: E2-b16: 0x0851c — transaction 0x833c: если r0!=0 -> return pc. bl-intercept (достигает 0x833c)..
    Тест эмулятора @ 0x851c: E2-b16: 0x0851c — transaction 0x833c: если r0!=0 -> return pc. bl-intercept (достигает 0x833c)..
    """
    cap, _emu = _intercept(0x0851C, 0x833D)
    assert 'r0' in cap, f'{cap}'


# --- E2-batch17: one-shot флаг 0x03a6c (stateful, вериф fire/no-fire) ---
@t(0x03A6C, 'E2-b17: 0x03a6c — one-shot флаг byte@0x142. Если ==1 -> обнуляет его + bl 0xdd81; иначе return. Вериф: flag=1 достигает 0xdd81, flag=0 нет.')
def _(run, rng):
    """Emulator test @ 0x3a6c: E2-b17: 0x03a6c — one-shot флаг byte@0x142. Если ==1 -> обнуляет его + bl 0xdd81; иначе return. Вериф: flag=1 достигает 0xdd81, flag=0 нет..
    Тест эмулятора @ 0x3a6c: E2-b17: 0x03a6c — one-shot флаг byte@0x142. Если ==1 -> обнуляет его + bl 0xdd81; иначе return. Вериф: flag=1 достигает 0xdd81, flag=0 нет..
    """
    from emulator.mcu_emu import RAM as _R
    cap_fired, _emu = _intercept(0x03A6C, 0xDD81,
                                 extra_ram=[(_R + 0x142, b'\x01')])
    assert 'r0' in cap_fired, f'flag=1: не достиг 0xdd81: {cap_fired}'
    cap_idle, _emu2 = _intercept(0x03A6C, 0xDD81,
                                 extra_ram=[(_R + 0x142, b'\x00')])
    assert 'r0' not in cap_idle, f'flag=0: достиг 0xdd81 (ошибка): {cap_idle}'


# --- E2-batch18: flag-хендлер 0x09678 (stateful, полный разбор pool) ---
@t(0x09678, 'E2-b18: 0x09678 — flag-хендлер. BIT1=byte@0xB65 (bit1), COUNTER=byte@0xB73, A0=byte@0xB64. Если bit1 set и (COUNTER++)>=3 -> COUNTER=0, clear BIT1 bit1, A0=(A0&0x0f)|0xa0; затем если (A0>>4)==0xa -> bl (capstone: 0x173cd, эмулятор попадает в 0x173cc). Вериф: fire (BIT1=2,CNT=2) достигает; no-fire (BIT1=2,CNT=0) нет.')
def _(run, rng):
    """Emulator test @ 0x9678: E2-b18: 0x09678 — flag-хендлер. BIT1=byte@0xB65 (bit1), COUNTER=byte@0xB73, A0=byte@0xB64. Если bit1 set и (COUNTER++)>=3 -> COUNTER=0, clear BIT1 bit1, A0=(A0&0x0f)|0xa0; затем если (A0>>4)==0xa -> bl (capstone: 0x173cd, эмулятор попадает в 0x173cc). Вериф: fire (BIT1=2,CNT=2) достигает; no-fire (BIT1=2,CNT=0) нет..
    Тест эмулятора @ 0x9678: E2-b18: 0x09678 — flag-хендлер. BIT1=byte@0xB65 (bit1), COUNTER=byte@0xB73, A0=byte@0xB64. Если bit1 set и (COUNTER++)>=3 -> COUNTER=0, clear BIT1 bit1, A0=(A0&0x0f)|0xa0; затем если (A0>>4)==0xa -> bl (capstone: 0x173cd, эмулятор попадает в 0x173cc). Вериф: fire (BIT1=2,CNT=2) достигает; no-fire (BIT1=2,CNT=0) нет..
    """
    from emulator.mcu_emu import RAM as _R
    cap_fire, _emu = _intercept(0x09678, 0x173CC,
                                extra_ram=[(_R + 0xB65, b'\x02'),
                                           (_R + 0xB73, b'\x02')])
    assert 'r0' in cap_fire, f'fire: не достиг 0x173cc: {cap_fire}'
    cap_nofire, _emu2 = _intercept(0x09678, 0x173CC,
                                   extra_ram=[(_R + 0xB65, b'\x02')])
    assert 'r0' not in cap_nofire, f'no-fire: достиг 0x173cc (ошибка): {cap_nofire}'


# --- E2-batch19: счётчики с насыщением (stateful, inc + saturation) ---
@t(0x12C24, 'E2-b19: 0x12c24 — счётчик с насыщением. GATE=bit0(byte@0xB76), COUNTER=u16@0xB7A. Если gate set: COUNTER++; если COUNTER>0xC8 -> clear gate + COUNTER=0. Вериф inc (cnt 5->6) и sat (cnt 0xC8->0, gate clr).')
def _(run, rng):
    """Emulator test @ 0x12c24: E2-b19: 0x12c24 — счётчик с насыщением. GATE=bit0(byte@0xB76), COUNTER=u16@0xB7A. Если gate set: COUNTER++; если COUNTER>0xC8 -> clear gate + COUNTER=0. Вериф inc (cnt 5->6) и sat (cnt 0xC8->0, gate clr)..
    Тест эмулятора @ 0x12c24: E2-b19: 0x12c24 — счётчик с насыщением. GATE=bit0(byte@0xB76), COUNTER=u16@0xB7A. Если gate set: COUNTER++; если COUNTER>0xC8 -> clear gate + COUNTER=0. Вериф inc (cnt 5->6) и sat (cnt 0xC8->0, gate clr)..
    """
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    _r0, emu = _fresh_call(0x12C24, extra_ram=[(_R + 0xB76, b'\x01'),
                                                (_R + 0xB7A, _st.pack('<H', 5))])
    cnt = _st.unpack_from('<H', bytes(emu.uc.mem_read(_R + 0xB7A, 2)))[0]
    assert cnt == 6, f'inc: got {cnt} want 6'
    _r0, emu2 = _fresh_call(0x12C24, extra_ram=[(_R + 0xB76, b'\x01'),
                                                 (_R + 0xB7A, _st.pack('<H', 0xC8))])
    gate = emu2.uc.mem_read(_R + 0xB76, 1)[0]
    cnt2 = _st.unpack_from('<H', bytes(emu2.uc.mem_read(_R + 0xB7A, 2)))[0]
    assert cnt2 == 0 and gate == 0, f'sat: cnt={cnt2} gate={gate}'


@t(0x12E64, 'E2-b19: 0x12e64 — счётчик с насыщением #2. GATE=bit2(byte@0xB76), COUNTER=u16@0xB7C. Аналогично 0x12c24 (кап 0xC8). Вериф inc (cnt 5->6) и sat (cnt 0xC8->0, gate clr).')
def _(run, rng):
    """Emulator test @ 0x12e64: E2-b19: 0x12e64 — счётчик с насыщением #2. GATE=bit2(byte@0xB76), COUNTER=u16@0xB7C. Аналогично 0x12c24 (кап 0xC8). Вериф inc (cnt 5->6) и sat (cnt 0xC8->0, gate clr)..
    Тест эмулятора @ 0x12e64: E2-b19: 0x12e64 — счётчик с насыщением #2. GATE=bit2(byte@0xB76), COUNTER=u16@0xB7C. Аналогично 0x12c24 (кап 0xC8). Вериф inc (cnt 5->6) и sat (cnt 0xC8->0, gate clr)..
    """
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    _r0, emu = _fresh_call(0x12E64, extra_ram=[(_R + 0xB76, b'\x04'),
                                                (_R + 0xB7C, _st.pack('<H', 5))])
    cnt = _st.unpack_from('<H', bytes(emu.uc.mem_read(_R + 0xB7C, 2)))[0]
    assert cnt == 6, f'inc: got {cnt} want 6'
    _r0, emu2 = _fresh_call(0x12E64, extra_ram=[(_R + 0xB76, b'\x04'),
                                                 (_R + 0xB7C, _st.pack('<H', 0xC8))])
    gate = emu2.uc.mem_read(_R + 0xB76, 1)[0]
    cnt2 = _st.unpack_from('<H', bytes(emu2.uc.mem_read(_R + 0xB7C, 2)))[0]
    assert cnt2 == 0 and gate == 0, f'sat: cnt={cnt2} gate={gate}'


# --- E2-batch20: mismatch-счётчик 0x0c02c (stateful) ---
@t(0x0C02C, 'E2-b20: 0x0c02c — mismatch-счётчик. Читает bit0/bit1(0xF71) vs byte(0xA65)/byte(0xA66). Mismatch -> COUNTER(u16@0xA68)++; если >=0x32 -> toggle bit3(0xF73) + COUNTER=0x32. Match (оба равны) -> COUNTER=0 + clear bit3(0xF73). Вериф mismatch-inc / match-reset / saturation.')
def _(run, rng):
    """Emulator test @ 0xc02c: E2-b20: 0x0c02c — mismatch-счётчик. Читает bit0/bit1(0xF71) vs byte(0xA65)/byte(0xA66). Mismatch -> COUNTER(u16@0xA68)++; если >=0x32 -> toggle bit3(0xF73) + COUNTER=0x32. Match (оба равны) -> COUNTER=0 + clear bit3(0xF73). Вериф mismatch-inc / match-reset / saturation..
    Тест эмулятора @ 0xc02c: E2-b20: 0x0c02c — mismatch-счётчик. Читает bit0/bit1(0xF71) vs byte(0xA65)/byte(0xA66). Mismatch -> COUNTER(u16@0xA68)++; если >=0x32 -> toggle bit3(0xF73) + COUNTER=0x32. Match (оба равны) -> COUNTER=0 + clear bit3(0xF73). Вериф mismatch-inc / match-reset / saturation..
    """
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    def rd(emu, off, n):
        """The rd function of the script.
        Функция rd скрипта.
        """
        return bytes(emu.uc.mem_read(_R + off, n))
    _r0, emu = _fresh_call(0x0C02C, extra_ram=[(_R + 0xF71, b'\x01'),
                                                (_R + 0xA65, b'\x00')])
    cnt = _st.unpack_from('<H', rd(emu, 0xA68, 2))[0]
    assert cnt == 1, f'mismatch-inc: got {cnt} want 1'
    _r0, emu2 = _fresh_call(0x0C02C, extra_ram=[(_R + 0xA68, _st.pack('<H', 5))])
    cnt2 = _st.unpack_from('<H', rd(emu2, 0xA68, 2))[0]
    assert cnt2 == 0, f'match-reset: got {cnt2} want 0'
    _r0, emu3 = _fresh_call(0x0C02C, extra_ram=[(_R + 0xF71, b'\x01'),
                                                 (_R + 0xA65, b'\x00'),
                                                 (_R + 0xA68, _st.pack('<H', 0x31)),
                                                 (_R + 0xF73, b'\x00')])
    cnt3 = _st.unpack_from('<H', rd(emu3, 0xA68, 2))[0]
    flag3 = emu3.uc.mem_read(_R + 0xF73, 1)[0]
    assert cnt3 == 0x32 and (flag3 & 8), f'sat: cnt={cnt3:#x} flag={flag3:#x}'


# --- E2-batch21: pure-logic (checksum / критсекция / u32 из двух u16) ---
@t(0x048D8, 'E2-b21: 0x048d8 — контрольная сумма: r0 = (~sum(buf[0..len])) & 0xFF. Вериф 3 буфера.')
def _(run, rng):
    """Emulator test @ 0x48d8: E2-b21: 0x048d8 — контрольная сумма: r0 = (~sum(buf[0..len])) & 0xFF. Вериф 3 буфера..
    Тест эмулятора @ 0x48d8: E2-b21: 0x048d8 — контрольная сумма: r0 = (~sum(buf[0..len])) & 0xFF. Вериф 3 буфера..
    """
    from emulator.mcu_emu import RAM as _R
    for buf in (b'\x01\x02\x03', b'\xff\xff\xff', bytes(4)):
        r0, _e = _fresh_call(0x048D8, args=(_R + 0x100, len(buf)),
                             extra_ram=[(_R + 0x100, buf)])
        exp = (~sum(buf)) & 0xFF
        assert (r0 & 0xFF) == exp, f'buf={buf!r}: got {r0&0xff} want {exp}'


@t(0x02D1C, 'E2-b21: 0x02d1c — вход в критсекцию: COUNTER=u16@0xB5C; если ==0 -> cpsid i; затем COUNTER++. Вериф 0->1 и 5->6.')
def _(run, rng):
    """Emulator test @ 0x2d1c: E2-b21: 0x02d1c — вход в критсекцию: COUNTER=u16@0xB5C; если ==0 -> cpsid i; затем COUNTER++. Вериф 0->1 и 5->6..
    Тест эмулятора @ 0x2d1c: E2-b21: 0x02d1c — вход в критсекцию: COUNTER=u16@0xB5C; если ==0 -> cpsid i; затем COUNTER++. Вериф 0->1 и 5->6..
    """
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    for init in (0, 5):
        _r0, emu = _fresh_call(0x02D1C, extra_ram=[(_R + 0xB5C, _st.pack('<H', init))])
        cnt = _st.unpack_from('<H', bytes(emu.uc.mem_read(_R + 0xB5C, 2)))[0]
        assert cnt == init + 1, f'init={init}: got {cnt} want {init+1}'


@t(0x098AE, 'E2-b21: 0x098ae — u32 из двух u16: r0 = u16[ptr+0x14] | ((u16[ptr+0x18]&0xFF)<<16) (старший байт B сброшен). Вериф 3 пары.')
def _(run, rng):
    """Emulator test @ 0x98ae: E2-b21: 0x098ae — u32 из двух u16: r0 = u16[ptr+0x14] | ((u16[ptr+0x18]&0xFF)<<16) (старший байт B сброшен). Вериф 3 пары..
    Тест эмулятора @ 0x98ae: E2-b21: 0x098ae — u32 из двух u16: r0 = u16[ptr+0x14] | ((u16[ptr+0x18]&0xFF)<<16) (старший байт B сброшен). Вериф 3 пары..
    """
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    for A, B in ((0x1234, 0xABCD), (0x5678, 0x00FF), (0xFFFF, 0x1234)):
        r0, _e = _fresh_call(0x098AE, args=(_R + 0x200,),
                             extra_ram=[(_R + 0x214, _st.pack('<H', A)),
                                        (_R + 0x218, _st.pack('<H', B))])
        exp = (A | ((B & 0xFF) << 16)) & 0xFFFFFFFF
        assert r0 == exp, f'A={A:#x} B={B:#x}: got {r0:#x} want {exp:#x}'


# --- E2-batch22: set/clear-биты + signed-div-prep + sign-extend ---
def _setclr(off, bit, desc):
    """The helper function (_setclr).
    Вспомогательная функция (_setclr).
    """
    @t(off, desc)
    def _(run, rng):
        """The helper function (_).
        Вспомогательная функция (_).
        """
        from emulator.mcu_emu import RAM as _R
        import struct as _st
        for mode, init in ((1, 0), (0, 0xFFFF)):
            _r0, emu = _fresh_call(off, args=(_R + 0x300, mode),
                                   extra_ram=[(_R + 0x300, _st.pack('<H', init))])
            v = _st.unpack_from('<H', bytes(emu.uc.mem_read(_R + 0x300, 2)))[0]
            exp = (init | bit) if mode else (init & ~bit) & 0xFFFF
            assert v == exp, f'mode={mode} init={init:#x}: got {v:#x} want {exp:#x}'
    return _


_setclr(0x097CA, 0x400, 'E2-b22: 0x097ca — set/clear bit0x400 в *(u16@r0): mode!=0 -> |=, else &=~. Вериф set+clear.')
_setclr(0x0982C, 0x1, 'E2-b22: 0x0982c — set/clear bit0 в *(u16@r0). Вериф set+clear.')
_setclr(0x106A0, 0x40, 'E2-b22: 0x106a0 — set/clear bit0x40 в *(u16@r0). Вериф set+clear.')


@t(0x16288, 'E2-b22: 0x16288 — signed-подготовка к делению. При r1==0: возвращает 0x7FFFFFFF (если r2>=0) или 0x80000000 (если r2<0). Вериф оба знака.')
def _(run, rng):
    """Emulator test @ 0x16288: E2-b22: 0x16288 — signed-подготовка к делению. При r1==0: возвращает 0x7FFFFFFF (если r2>=0) или 0x80000000 (если r2<0). Вериф оба знака..
    Тест эмулятора @ 0x16288: E2-b22: 0x16288 — signed-подготовка к делению. При r1==0: возвращает 0x7FFFFFFF (если r2>=0) или 0x80000000 (если r2<0). Вериф оба знака..
    """
    for r2 in (5, -5):
        r0, _e = _fresh_call(0x16288, args=(r2 & 0xFFFFFFFF, 0))
        exp = 0x7FFFFFFF if r2 >= 0 else 0x80000000
        assert r0 == exp, f'r2={r2}: got {r0:#x} want {exp:#x}'


@t(0x08F58, 'E2-b22: 0x08f58 — sign-extend: читает s8@0xFC8 -> i16 -> u16@0x135E, возвращает. Вериф -1/127/-128.')
def _(run, rng):
    """Emulator test @ 0x8f58: E2-b22: 0x08f58 — sign-extend: читает s8@0xFC8 -> i16 -> u16@0x135E, возвращает. Вериф -1/127/-128..
    Тест эмулятора @ 0x8f58: E2-b22: 0x08f58 — sign-extend: читает s8@0xFC8 -> i16 -> u16@0x135E, возвращает. Вериф -1/127/-128..
    """
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    for sb, exp in ((0xFF, 0xFFFF), (0x7F, 0x7F), (0x80, 0xFF80)):
        r0, emu = _fresh_call(0x08F58, extra_ram=[(_R + 0xFC8, bytes([sb]))])
        assert (r0 & 0xFFFF) == exp, f'sb={sb:#x}: got {r0&0xffff:#x} want {exp:#x}'
        stored = _st.unpack_from('<H', bytes(emu.uc.mem_read(_R + 0x135E, 2)))[0]
        assert stored == exp, f'stored={stored:#x} want {exp:#x}'


# --- E2-batch23: set/clear-биты (прод.) + signed-prep варианты + memmove ---
_setclr(0x09844, 0x100, 'E2-b23: 0x09844 — set/clear bit0x100 в *(u16@r0). Вериф set+clear.')
_setclr(0x0985C, 0x200, 'E2-b23: 0x0985c — set/clear bit0x200 в *(u16@r0). Вериф set+clear.')


@t(0x162CE, 'E2-b23: 0x162ce — signed-подготовка к делению (вариант). r1==0 -> 0x7FFFFFFF (r2>=0) / 0x80000000 (r2<0).')
def _(run, rng):
    """Emulator test @ 0x162ce: E2-b23: 0x162ce — signed-подготовка к делению (вариант). r1==0 -> 0x7FFFFFFF (r2>=0) / 0x80000000 (r2<0)..
    Тест эмулятора @ 0x162ce: E2-b23: 0x162ce — signed-подготовка к делению (вариант). r1==0 -> 0x7FFFFFFF (r2>=0) / 0x80000000 (r2<0)..
    """
    for r2 in (5, -5):
        r0, _e = _fresh_call(0x162CE, args=(r2 & 0xFFFFFFFF, 0))
        exp = 0x7FFFFFFF if r2 >= 0 else 0x80000000
        assert r0 == exp, f'r2={r2}: got {r0:#x} want {exp:#x}'


@t(0x16328, 'E2-b23: 0x16328 — signed-подготовка к делению (вариант 2). r1==0 -> 0x7FFFFFFF / 0x80000000.')
def _(run, rng):
    """Emulator test @ 0x16328: E2-b23: 0x16328 — signed-подготовка к делению (вариант 2). r1==0 -> 0x7FFFFFFF / 0x80000000..
    Тест эмулятора @ 0x16328: E2-b23: 0x16328 — signed-подготовка к делению (вариант 2). r1==0 -> 0x7FFFFFFF / 0x80000000..
    """
    for r2 in (5, -5):
        r0, _e = _fresh_call(0x16328, args=(r2 & 0xFFFFFFFF, 0))
        exp = 0x7FFFFFFF if r2 >= 0 else 0x80000000
        assert r0 == exp, f'r2={r2}: got {r0:#x} want {exp:#x}'


@t(0x07FB8, 'E2-b23: 0x07fb8 — memmove: копирует len байт из src(r0) в dst(r1), возвращает 1. Вериф 5-байтовый буфер.')
def _(run, rng):
    """Emulator test @ 0x7fb8: E2-b23: 0x07fb8 — memmove: копирует len байт из src(r0) в dst(r1), возвращает 1. Вериф 5-байтовый буфер..
    Тест эмулятора @ 0x7fb8: E2-b23: 0x07fb8 — memmove: копирует len байт из src(r0) в dst(r1), возвращает 1. Вериф 5-байтовый буфер..
    """
    from emulator.mcu_emu import RAM as _R
    src = bytes([0x11, 0x22, 0x33, 0x44, 0x55])
    r0, emu = _fresh_call(0x07FB8, args=(_R + 0x100, _R + 0x200, len(src)),
                          extra_ram=[(_R + 0x100, src)])
    dst = bytes(emu.uc.mem_read(_R + 0x200, len(src)))
    assert r0 == 1 and dst == src, f'r0={r0} dst={dst.hex()}'


# --- E2-batch24: обнуление блока ---
@t(0x04A04, 'E2-b24: 0x04a04 — обнуление блока: byte@0x129 + u32@0x12C/0x130/0x134/0x138 (блок 0x129..0x13B). Вериф: pre-set -> все 0.')
def _(run, rng):
    """Emulator test @ 0x4a04: E2-b24: 0x04a04 — обнуление блока: byte@0x129 + u32@0x12C/0x130/0x134/0x138 (блок 0x129..0x13B). Вериф: pre-set -> все 0..
    Тест эмулятора @ 0x4a04: E2-b24: 0x04a04 — обнуление блока: byte@0x129 + u32@0x12C/0x130/0x134/0x138 (блок 0x129..0x13B). Вериф: pre-set -> все 0..
    """
    from emulator.mcu_emu import RAM as _R
    pre = [(_R + 0x129, b'\xAA'), (_R + 0x12C, b'\x11\x22\x33\x44'),
           (_R + 0x130, b'\x55\x66\x77\x88'), (_R + 0x134, b'\x99\xAA\xBB\xCC'),
           (_R + 0x138, b'\xDD\xEE\xFF\x00')]
    _r0, emu = _fresh_call(0x04A04, extra_ram=pre)
    block = bytes(emu.uc.mem_read(_R + 0x129, 0x13))
    assert block == bytes(0x13), f'block not zeroed: {block.hex()}'
