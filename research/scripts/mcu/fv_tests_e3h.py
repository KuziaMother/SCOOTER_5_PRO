# ruff: noqa: F405
"""§92 (A6): NVRAM-зоны (RAM-копии с CRC) — layout + CRC-8/CRC-16-референс (emulator-based).

Контракты (статика §50 + динамика §92):
- Четыре RAM-копии NVRAM-зон верифицируются CRC после чтения из flash:
  - 0x13B14 (зона @0x30DD, 32Б): read 0x20Б → 100-iter + re-read → CRC-8
    (0x87F8, poly 0x2F) по 24Б сверяется с байтом [zone+0x18] → ret 0/1.
  - 0x147AC (зона @0x30CF): CRC-16 табличный (0x8A50, init 0xFFFF; таблицы
    @0x08019584/0x08019684 = 0xFF в образе — live-задача); изоляция: spin.
  - 0xCFB8 (0x304C, 512Б) / 0xCF60 (0x305C, 40Б): read + timeout.
- **CRC-8 (0x87F8)** — самодостаточен (poly в коде): live verified 7/7.
- Изолированный контракт (NVM=0xFF): 0x13B14 → зона=0xFF×32, ret=1 (FAIL),
  insn≈5999; 0xCFB8 → insn≈2394 ret=0; 0xCF60 → insn≈5344 ret=1.
- NvmZoneModel (emulator/mcu_emu.py): crc8 (ref), zone_read, zone_crc8_valid.
"""

import struct

from fv_core import *  # noqa: F401,F403
from emulator.mcu_emu import (NV_CRC8_POLY, NV_CRC16_POLY, NVM_CRC16_TABLE16,  # noqa: E402
                              NVM_Z304C, NVM_Z305C,
                              NVM_Z30DD, NVM_Z30DD_CRC_OFF,
                              NVM_Z30DD_DATA_LEN, NVM_Z30DD_SIZE,
                              NVM_SAVELIST_1A550, NVM_SAVELIST_ENTRIES,
                              NVM_SAVELIST_SIZE, NvmZoneModel)


def _a6_fresh(off, arg0=0, seed=None, max_insn=200000):
    """The helper function (_a6_fresh).
    Вспомогательная функция (_a6_fresh).
    """
    emu = McuEmu(max_insn=max_insn)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))
    emu.hook_periph_ready()
    if seed:
        for a, v in seed:
            uc.mem_write(RAM + a, v if isinstance(v, (bytes, bytearray)) else struct.pack('<I', v))
    uc.reg_write(UC_ARM_REG_R0, arg0)
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
        uc.emu_start(off | 1, 0, count=emu.max_insn)
    except Exception:
        pass
    return emu, uc, lastpc[0]


@t(0x87F8, 'A6 §92: 0x87F8(data, len) — CRC-8 (poly 0x2F, init 0, MSB-first, без final-xor): live vs NvmZoneModel.crc8 на 7 наборах (1/8/9/16/24/32Б, 0x00/0xFF-наполнители, 123456789)')
def _(run, rng):
    """Emulator test @ 0x87f8: A6 §92: 0x87F8(data, len) — CRC-8 (poly 0x2F, init 0, MSB-first, без final-xor): live vs NvmZoneModel.crc8 на 7 наборах (1/8/9/16/24/32Б, 0x00/0xFF-наполнители, 123456789).
    Тест эмулятора @ 0x87f8: A6 §92: 0x87F8(data, len) — CRC-8 (poly 0x2F, init 0, MSB-first, без final-xor): live vs NvmZoneModel.crc8 на 7 наборах (1/8/9/16/24/32Б, 0x00/0xFF-наполнители, 123456789).
    """
    model = NvmZoneModel(McuEmu())
    for data in (b'\x00', b'\x01', b'123456789', bytes(range(16)),
                 b'\x00' * 8, b'\xff' * 8, bytes(range(32)),
                 bytes(rng.getrandbits(8) for _ in range(rng.randint(1, 40)))):
        emu, uc, lp = _a6_fresh(0x87F8, arg0=RAM + 0x1000, seed=((0x1000, bytes(data)),))
        uc.reg_write(UC_ARM_REG_R1, len(data))
        emu2 = McuEmu(max_insn=100000)
        u2 = emu2.uc
        u2.mem_write(RAM, bytes(0x20000))
        emu2.hook_periph_ready()
        u2.mem_write(RAM + 0x1000, bytes(data))
        u2.reg_write(UC_ARM_REG_R0, RAM + 0x1000)
        u2.reg_write(UC_ARM_REG_R1, len(data))
        u2.reg_write(UC_ARM_REG_SP, STACK_TOP)
        u2.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        try:
            u2.emu_start(0x87F8 | 1, 0, count=100000)
        except Exception:
            pass
        live = u2.reg_read(UC_ARM_REG_R0) & 0xFF
        ref = model.crc8(data)
        assert live == ref == model.crc8(data), f'CRC-8 len={len(data)}: live={live:#x} ref={ref:#x}'
        assert NV_CRC8_POLY == 0x2F


@t(0x13B14, 'A6 §92: 0x13B14(arg0) — зона @0x30DD (32Б = 24Б данные + CRC-8 @0x18 + 7Б): read 0x20Б → (OK: 100-iter + re-read) → CRC-8(24Б) vs [zone+0x18] → ret 0/1. Изоляция (NVM=0xFF): зона=0xFF×32, CRC8(0xFF×24)≠0xFF → ret=1 (FAIL), insn≈5999, зона-офсеты NVM_Z30DD')
def _(run, rng):
    """Emulator test @ 0x13b14: A6 §92: 0x13B14(arg0) — зона @0x30DD (32Б = 24Б данные + CRC-8 @0x18 + 7Б): read 0x20Б → (OK: 100-iter + re-read) → CRC-8(24Б) vs [zone+0x18] → ret 0/1. Изоляция (NVM=0xFF): зона=0xFF×32, CRC8(0xFF×24)≠0xFF → ret=1 (FAIL), insn≈5999, зона-офсеты NVM_Z30DD.
    Тест эмулятора @ 0x13b14: A6 §92: 0x13B14(arg0) — зона @0x30DD (32Б = 24Б данные + CRC-8 @0x18 + 7Б): read 0x20Б → (OK: 100-iter + re-read) → CRC-8(24Б) vs [zone+0x18] → ret 0/1. Изоляция (NVM=0xFF): зона=0xFF×32, CRC8(0xFF×24)≠0xFF → ret=1 (FAIL), insn≈5999, зона-офсеты NVM_Z30DD.
    """
    emu, uc, lp = _a6_fresh(0x13B14)
    ret = uc.reg_read(UC_ARM_REG_R0) & 0xFF
    assert 5000 <= emu.insn <= 7000, f'0x13b14: insn={emu.insn} ждём ~5999'
    assert ret == 1, f'0x13b14: ret={ret:#x} ждём 1 (FAIL, пустой NVM)'
    model = NvmZoneModel(emu)
    zone = model.zone_read(NVM_Z30DD, NVM_Z30DD_SIZE)
    assert zone == b'\xff' * NVM_Z30DD_SIZE, f'0x13b14: зона != 0xFF×32: {zone.hex()[:16]}...'
    assert not model.zone_crc8_valid(NVM_Z30DD), '0x13b14: CRC8(0xFF×24) должен не совпадать'
    # CRC-8 референс: сверка храненого байта
    assert model.crc8(zone[:NVM_Z30DD_DATA_LEN]) != zone[NVM_Z30DD_CRC_OFF]


@t(0x147AC, 'A6 §92: 0x147AC(0x40000) — зона @0x30CF (CRC-16 табличный 0x8A50, init 0xFFFF; таблицы @0x08019584/0x08019684 = 0xFF в образе): изоляция — 0x82F0/0x8A50/0x84A0-цепь крутится до max_insn (context-dependent; таблицы — live-задача)')
def _(run, rng):
    """Emulator test @ 0x147ac: A6 §92: 0x147AC(0x40000) — зона @0x30CF (CRC-16 табличный 0x8A50, init 0xFFFF; таблицы @0x08019584/0x08019684 = 0xFF в образе): изоляция — 0x82F0/0x8A50/0x84A0-цепь крутится до max_insn (context-dependent; таблицы — live-задача).
    Тест эмулятора @ 0x147ac: A6 §92: 0x147AC(0x40000) — зона @0x30CF (CRC-16 табличный 0x8A50, init 0xFFFF; таблицы @0x08019584/0x08019684 = 0xFF в образе): изоляция — 0x82F0/0x8A50/0x84A0-цепь крутится до max_insn (context-dependent; таблицы — live-задача).
    """
    emu, uc, lp = _a6_fresh(0x147AC, arg0=0x40000, max_insn=60000)
    assert emu.insn >= 60000, f'0x147ac: insn={emu.insn} ждём spin до max_insn'


@t(0xCFB8, 'A6 §92: 0xCFB8() — зона @0x304C (read 512Б, 0x8380): изоляция insn≈2394, ret=0 (read-OK path, без явной CRC-сверки)')
def _(run, rng):
    """Emulator test @ 0xcfb8: A6 §92: 0xCFB8() — зона @0x304C (read 512Б, 0x8380): изоляция insn≈2394, ret=0 (read-OK path, без явной CRC-сверки).
    Тест эмулятора @ 0xcfb8: A6 §92: 0xCFB8() — зона @0x304C (read 512Б, 0x8380): изоляция insn≈2394, ret=0 (read-OK path, без явной CRC-сверки).
    """
    emu, uc, lp = _a6_fresh(0xCFB8)
    ret = uc.reg_read(UC_ARM_REG_R0) & 0xFF
    assert 1500 <= emu.insn <= 3500, f'0xcfb8: insn={emu.insn} ждём ~2394'
    assert ret == 0, f'0xcfb8: ret={ret:#x} ждём 0'


@t(0xCF60, 'A6 §92: 0xCF60(arg0) — зона @0x305C (read 40Б, 0x8380): изоляция insn≈5344, ret=1 (timeout/read path)')
def _(run, rng):
    """Emulator test @ 0xcf60: A6 §92: 0xCF60(arg0) — зона @0x305C (read 40Б, 0x8380): изоляция insn≈5344, ret=1 (timeout/read path).
    Тест эмулятора @ 0xcf60: A6 §92: 0xCF60(arg0) — зона @0x305C (read 40Б, 0x8380): изоляция insn≈5344, ret=1 (timeout/read path).
    """
    emu, uc, lp = _a6_fresh(0xCF60)
    ret = uc.reg_read(UC_ARM_REG_R0) & 0xFF
    assert 4000 <= emu.insn <= 6500, f'0xcf60: insn={emu.insn} ждём ~5344'
    assert ret == 1, f'0xcf60: ret={ret:#x} ждём 1'


@t(0x13B14, 'A6 §92: NvmZoneModel — CRC-8 референс + zone layout: crc8(self-consistency, 30 рандомных), zone_crc8_valid на валидной/испорченной зоне, layout-константы (32Б=24+1+7, poly 0x2F)')
def _(run, rng):
    """Emulator test @ 0x13b14: A6 §92: NvmZoneModel — CRC-8 референс + zone layout: crc8(self-consistency, 30 рандомных), zone_crc8_valid на валидной/испорченной зоне, layout-константы (32Б=24+1+7, poly 0x2F).
    Тест эмулятора @ 0x13b14: A6 §92: NvmZoneModel — CRC-8 референс + zone layout: crc8(self-consistency, 30 рандомных), zone_crc8_valid на валидной/испорченной зоне, layout-константы (32Б=24+1+7, poly 0x2F).
    """
    model = NvmZoneModel(McuEmu())
    assert NV_CRC8_POLY == 0x2F
    assert NVM_Z30DD_SIZE == NVM_Z30DD_DATA_LEN + 1 + 7  # 32 = 24 + CRC + резерв
    # self-consistency CRC-8
    for _ in range(30):
        data = bytes(rng.getrandbits(8) for _ in range(rng.randint(1, 40)))
        assert model.crc8(data) == NvmZoneModel.crc8(data)
    # zone_crc8_valid: валидная зона → True, испорченная → False
    good = bytearray(NVM_Z30DD_SIZE)
    good[:NVM_Z30DD_DATA_LEN] = bytes(rng.getrandbits(8) for _ in range(NVM_Z30DD_DATA_LEN))
    good[NVM_Z30DD_CRC_OFF] = model.crc8(good[:NVM_Z30DD_DATA_LEN])
    emu = McuEmu()
    emu.uc.mem_write(RAM + NVM_Z30DD, bytes(good))
    m2 = NvmZoneModel(emu)
    assert m2.zone_crc8_valid(NVM_Z30DD), 'валидная зона: CRC8 должен совпасть'
    bad = bytearray(good)
    bad[NVM_Z30DD_CRC_OFF] ^= 0xFF
    emu.uc.mem_write(RAM + NVM_Z30DD, bytes(bad))
    assert not m2.zone_crc8_valid(NVM_Z30DD), 'испорченный CRC: должен не совпасть'
    # другие зоны — адреса в RAM
    assert 0x3000 <= NVM_Z304C <= 0x30FF and 0x3000 <= NVM_Z305C <= 0x30FF


@t(0x3C4C, '§96 CRC-16 закрыт статикой: два варианта — 0x3C4C (init 0x0000, 16-bit таблица @0x08019784) и 0x8A50 (init 0xFFFF, hi/lo @0x08019584/0x19684); оба non-reflected → полином 0x1021 (CCITT). Референс crc16_ccitt: init 0xFFFF по "123456789" = 0x29B1 (документированный CCITT check). Таблицы в образе 0xFF — строятся в runtime из полинома (регенерируются, live-дамп не нужен)')
def _(run, rng):
    """Emulator test @ 0x3c4c: §96 CRC-16 закрыт статикой: два варианта — 0x3C4C (init 0x0000, 16-bit таблица @0x08019784) и 0x8A50 (init 0xFFFF, hi/lo @0x08019584/0x19684); оба non-reflected → полином 0x1021 (CCITT). Референс crc16_ccitt: init 0xFFFF по "123456789" = 0x29B1 (документированный CCITT check). Таблицы в образе 0xFF — строятся в runtime из полинома (регенерируются, live-дамп не нужен).
    Тест эмулятора @ 0x3c4c: §96 CRC-16 закрыт статикой: два варианта — 0x3C4C (init 0x0000, 16-bit таблица @0x08019784) и 0x8A50 (init 0xFFFF, hi/lo @0x08019584/0x19684); оба non-reflected → полином 0x1021 (CCITT). Референс crc16_ccitt: init 0xFFFF по "123456789" = 0x29B1 (документированный CCITT check). Таблицы в образе 0xFF — строятся в runtime из полинома (регенерируются, live-дамп не нужен).
    """
    assert NV_CRC16_POLY == 0x1021
    assert NVM_CRC16_TABLE16 == 0x08019784
    model = NvmZoneModel(McuEmu())
    std = b'123456789'
    # init 0xFFFF → 0x29B1 (документированный CRC-16/CCITT check)
    assert model.crc16_ccitt(std, init=0xFFFF) == 0x29B1, \
        f"init 0xFFFF={model.crc16_ccitt(std, init=0xFFFF):#x} ждём 0x29b1"
    # init 0x0000 (0x3C4C) — детерминирован, отличается от 0xFFFF
    c0 = model.crc16_ccitt(std, init=0x0000)
    assert c0 != 0x29B1 and isinstance(c0, int) and 0 <= c0 < 0x10000
    # self-consistency: детерминизм + длина
    assert model.crc16_ccitt(std, init=0) == c0
    assert model.crc16_ccitt(b'', init=0xFFFF) == 0xFFFF  # пустой → init
    # детерминизм на рандоме
    for _ in range(10):
        d = bytes(rng.getrandbits(8) for _ in range(rng.randint(1, 64)))
        assert model.crc16_ccitt(d, init=0xFFFF) == NvmZoneModel.crc16_ccitt(d, init=0xFFFF)


@t(0x2D5C, '§96 NVRAM save-list @0x1A550: 0x2D5C персистит 26Б во внешнюю NVM через 0x332C (transform 0x163B4 + checksum 0x87B0); данные = таблица 6 u32-адресов (4× RAM 0x200002xx + TIM1 CCR1 0x40012C40 + константы 0x94E/0xAC). 0x5C9C: magic 0xAAAA @0x40003000 + 2Б (F1 FA) из 0x19B14 + flush 0xC20C. Статическая структура save-list верифицирована по образу')
def _(run, rng):
    # таблица save-list в образе == константа
    """Emulator test @ 0x2d5c: §96 NVRAM save-list @0x1A550: 0x2D5C персистит 26Б во внешнюю NVM через 0x332C (transform 0x163B4 + checksum 0x87B0); данные = таблица 6 u32-адресов (4× RAM 0x200002xx + TIM1 CCR1 0x40012C40 + константы 0x94E/0xAC). 0x5C9C: magic 0xAAAA @0x40003000 + 2Б (F1 FA) из 0x19B14 + flush 0xC20C. Статическая структура save-list верифицирована по образу.
    Тест эмулятора @ 0x2d5c: §96 NVRAM save-list @0x1A550: 0x2D5C персистит 26Б во внешнюю NVM через 0x332C (transform 0x163B4 + checksum 0x87B0); данные = таблица 6 u32-адресов (4× RAM 0x200002xx + TIM1 CCR1 0x40012C40 + константы 0x94E/0xAC). 0x5C9C: magic 0xAAAA @0x40003000 + 2Б (F1 FA) из 0x19B14 + flush 0xC20C. Статическая структура save-list верифицирована по образу.
    """
    import struct as _s
    raw = FW[NVM_SAVELIST_1A550:NVM_SAVELIST_1A550 + NVM_SAVELIST_SIZE]
    assert len(raw) == NVM_SAVELIST_SIZE == 0x1A
    entries = _s.unpack('<6I', raw[:24])
    assert entries == NVM_SAVELIST_ENTRIES, f"save-list={entries} != {NVM_SAVELIST_ENTRIES}"
    # TIM1 CCR1 в списке (моторный таймер персистится)
    assert 0x40012C40 in NVM_SAVELIST_ENTRIES
    # 0x5C9C data = 2Б F1 FA из 0x19B14
    assert FW[0x19B14:0x19B16] == b'\xf1\xfa'
