# ruff: noqa: F405  (имена из star-import от fv_core)
"""§89 (B3-динамика): агрегатор MCU→BLE — beacon 0x1F1CC + 24-состоянная машина 0x1F71C.
Найдено (2026-11-18, static + dynamic probes):
  - **0x1F1CC() = beacon 'c' builder**: таблица @0xA43 (4 слота, counter byte[0x2C1],
    wrap ≥4→0): slot = 0xA43 + 0x96·byte[0x2C1]; frame {4,'c','D',0xA7,0x9C}; ret 1;
    tail 0x1F544 → 0x1F548 (u64 «данные готовы»): {6,'c','c',<byte>,Σcrc,0x9C}
    (running-sum crc, tail 0x9C).
  - **0x1F71C() = 24-состоянная машина** (jump-table @0x1F77A, state = byte[0x2C7],
    guard: byte[0x2C8] (tail) ≠ byte[0x2C7] (head), иначе early-exit → 0x2000C;
    tail++ на каждую обработку). В изоляции индекс = 1 (byte-garbage адрес
    0x70132300 → 0 → +1 = 1) → slot = 0xC05 + 0x96 = 0xC9B. Классификатор по
    байтам слота: byte[0]: 'Q'/'R'/'S'/'T' → класс 1, 'd' → 0x0A, 'Z' → 0x14
    (byte[0x180] = 0x170+0x10); byte[1] 'Q' → 0x15; byte[2] 0x0A → 0x16;
    byte[3]: 0xA0 → билдер {0x0A,'Z','a',0x0A,0xA0,0×4,XOR-crc,0xA5} (магия 0xA5,
    XOR-crc по 9 байтам, flag byte[0x339]=1), 0xA1..0xA6 → u16[0x1E8]-ветки,
    0xAE → 0x1F900. Фреймы строятся в r4 = **0x200010B5 (TX-ring, §77)**.
    State 2 @0x1FAE0: scaling u16[0x33A] + u16[0x1E8] = (v1·v0)>>8+v1 + 0x19968
    (×0x12/10) → u16[0x1F6]. Tail 0x211AE = beacon 'a' {4,<byte>,'a',0xC4,0x9C}
    (counter wrap ≥8→0).
  - Оба вызываются периодическим task 0x1DFD8 (там же RX-парсер 0x1E9E0, B2)."""
import struct

from fv_core import *  # noqa: F401,F403

from emulator.mcu_emu import (TxAggregatorModel, TX_BCN_C, TX_BCN_TABLE_OFF,  # noqa: E402
                              TX_BCN_SLOT, TX_AGGR_SLOT_BASE, TX_RING_OFF)


def _b3_fresh(off, seeds=(), max_insn=200000):
    """The helper function (_b3_fresh).
    Вспомогательная функция (_b3_fresh).
    """
    emu = McuEmu(max_insn=max_insn)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))
    emu.hook_periph_ready()
    for a, v in seeds:
        if isinstance(v, (bytes, bytearray)):
            uc.mem_write(a, v)
        else:
            uc.mem_write(a, bytes([v & 0xFF]))
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
    except Exception:
        pass
    return emu, uc, lastpc[0]


@t(0x1F1CC, '§89: 0x1F1CC() — beacon «c» builder: slot 0xA43+0x96·byte[0x2C1] = '
           '{4,\'c\',\'D\',0xA7,0x9C}; counter++ (wrap ≥4→0); ret 1')
def _(run, rng):
    """Emulator test @ 0x1f1cc: §89: 0x1F1CC() — beacon «c» builder: slot 0xA43+0x96·byte[0x2C1] = {4,'c','D',0xA7,0x9C}; counter++ (wrap ≥4→0); ret 1.
    Тест эмулятора @ 0x1f1cc: §89: 0x1F1CC() — beacon «c» builder: slot 0xA43+0x96·byte[0x2C1] = {4,'c','D',0xA7,0x9C}; counter++ (wrap ≥4→0); ret 1.
    """
    emu, uc, lp = _b3_fresh(0x1F1CC)
    assert uc.reg_read(UC_ARM_REG_R0) == 1, f'0x1F1CC: ret={uc.reg_read(UC_ARM_REG_R0):#x}'
    tx = TxAggregatorModel(emu)
    assert tx.beacon_slot(0)[:5] == TX_BCN_C, f'beacon c: {tx.beacon_slot(0)[:8].hex()}'
    assert tx.beacon_counter == 1, f'counter: {tx.beacon_counter}'
    # counter = 3 → слот 3 + wrap в 0
    emu, uc, lp = _b3_fresh(0x1F1CC, seeds=[(RAM + 0x2C1, 3)])
    tx = TxAggregatorModel(emu)
    assert tx.beacon_slot(3)[:5] == TX_BCN_C, f'beacon c slot3: {tx.beacon_slot(3)[:8].hex()}'
    assert tx.beacon_counter == 0, f'wrap: {tx.beacon_counter}'
    assert tx.beacon_slot(0) == bytes(16), 'slot 0 не тронут'


@t(0x1F71C, '§89: 0x1F71C() — 24-состоянная машина (агрегатор MCU→BLE): guard '
           'byte[0x2C8]≠byte[0x2C7] (иначе early-exit 22 insn → 0x2000C); классификатор '
           'slot 0xC05+0x96 (изоляция: idx=1 → 0xC9B): \'Q\'-\'T\'→класс 1, \'d\'→0x0A, '
           '\'Z\'→0x14 (byte[0x180]); tail++ на обработку')
def _(run, rng):
    # guard: tail == head → early-exit
    """Emulator test @ 0x1f71c: §89: 0x1F71C() — 24-состоянная машина (агрегатор MCU→BLE): guard byte[0x2C8]≠byte[0x2C7] (иначе early-exit 22 insn → 0x2000C); классификатор slot 0xC05+0x96 (изоляция: idx=1 → 0xC9B): 'Q'-'T'→класс 1, 'd'→0x0A, 'Z'→0x14 (byte[0x180]); tail++ на обработку.
    Тест эмулятора @ 0x1f71c: §89: 0x1F71C() — 24-состоянная машина (агрегатор MCU→BLE): guard byte[0x2C8]≠byte[0x2C7] (иначе early-exit 22 insn → 0x2000C); классификатор slot 0xC05+0x96 (изоляция: idx=1 → 0xC9B): 'Q'-'T'→класс 1, 'd'→0x0A, 'Z'→0x14 (byte[0x180]); tail++ на обработку.
    """
    emu, uc, lp = _b3_fresh(0x1F71C, seeds=[(RAM + 0x2C7, 2), (RAM + 0x2C8, 2)])
    assert emu.insn == 22, f'guard: insn={emu.insn}'
    # изоляция: head=0, tail=1 (non-empty), slot idx=1 → байты @0xC9B..0xC9E
    for b, cls in ((0x51, 1), (0x52, 1), (0x64, 0x0A), (0x5A, 0x14)):
        emu, uc, lp = _b3_fresh(0x1F71C, seeds=[(RAM + 0x2C7, 0), (RAM + 0x2C8, 1),
                                                (RAM + 0xC9B, b)])
        tx = TxAggregatorModel(emu)
        assert tx.aggr_class() == cls, f'класс {chr(b)}: {tx.aggr_class():#x} ждём {cls:#x}'
        # insn: quirk-класс (dead-lsls блок 0x1F790) — контекстно-плавающий (65/67 для
        # 'Q'/'R', 73/75 для 'd'/'Z' в изоляции) — инвариант: класс + tail++
        assert 60 <= emu.insn <= 90, f'insn {chr(b)}: {emu.insn}'
        assert tx.tx_ring()[0] == 0, 'TX-ring не тронут (фрейм-билдеры — runtime r4)'
    # byte[3] = 0xA0 → ветка 0x1F878 (u64-константа → bhs), класс 0
    emu, uc, lp = _b3_fresh(0x1F71C, seeds=[(RAM + 0x2C7, 0), (RAM + 0x2C8, 1),
                                            (RAM + 0xC9E, 0xA0)])
    assert TxAggregatorModel(emu).aggr_class() == 0, '0xA0: класс'
    # tail++ на каждую обработку
    assert emu.uc.mem_read(RAM + 0x2C8, 1)[0] == 2, 'tail не инкрементирован'


@t(0x211AE, '§89: tail 0x211AE (общий exit 0x1F71C) — beacon «a» builder {4,<byte>,«a»,0xC4,'
           '0x9C}: запись веткозависима (в изоляции default-path обходит её: 0x20BC6 → '
           'эпилог 0x211E4); контракт: exit через pop @0x211E6, counter ∈ {0,1}')
def _(run, rng):
    """Emulator test @ 0x211ae: §89: tail 0x211AE (общий exit 0x1F71C) — beacon «a» builder {4,<byte>,«a»,0xC4,0x9C}: запись веткозависима (в изоляции default-path обходит её: 0x20BC6 → эпилог 0x211E4); контракт: exit через pop @0x211E6, counter ∈ {0,1}.
    Тест эмулятора @ 0x211ae: §89: tail 0x211AE (общий exit 0x1F71C) — beacon «a» builder {4,<byte>,«a»,0xC4,0x9C}: запись веткозависима (в изоляции default-path обходит её: 0x20BC6 → эпилог 0x211E4); контракт: exit через pop @0x211E6, counter ∈ {0,1}.
    """
    emu, uc, lp = _b3_fresh(0x1F71C, seeds=[(RAM + 0x2C7, 0), (RAM + 0x2C8, 1)])
    assert lp == 0x211E6, f'exit tail: lastpc={lp:#x}'
    tx = TxAggregatorModel(emu)
    assert tx.beacon_counter in (0, 1), f'beacon-a counter: {tx.beacon_counter}'
    if tx.beacon_counter == 1:  # ветка срабатывает → золoto 'a'-фрейма
        slot = tx.beacon_slot(0)
        assert slot[0] == 4 and slot[2] == 0x61 and slot[3] == 0xC4 and slot[4] == 0x9C, \
            f"beacon 'a': {slot[:8].hex()}"
