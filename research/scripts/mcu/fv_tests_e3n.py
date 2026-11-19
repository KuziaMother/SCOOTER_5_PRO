# -*- coding: utf-8 -*-
# ruff: noqa: F405  (names from the star-import of fv_core)
"""F1 (section 98): the 5+2 catalog entries with the ID status — closed (statics +
emulator).

1. **0xC6F0** — a live function (not "dead code?"): the 3-instruction setter
   `[0x42420060] = r0` (the literal 0x42420000 @0xC6F8); the callers 0x10C92
   (r0=0, disable) / 0x10CA2 (r0=1, enable) from the init sequence. The 0x4242xxxx
   block is outside the current McuEmu map (mapped in the test).
2. **0x17736** — a detector artifact: the bytes B5 77 (a push look-alike) INSIDE the
   u16 table of the giant 0x17xxx region (hi^lo=0xC0, 100% on the 48 entries
   0x17720..0x17780) — data, not code.
3. **0x177D6** — a cold-tail of the giant 0x17xxx: push{..,lr}; strh r0,[r5,#0x28];
   str r5,[sp,#0x24]; b 0x173BC (the shared epilogue) — the 4-instruction block in
   the gap 0x177DE..0x19A1C.
4. **0x178C4** — a cold-tail of the same region: push{..,lr}; adr r5,#0x32C;
   str r5,[sp,#0x2A0] (the pool pointer to the callee, the frame 0x2A0);
   strh r1,[r1,#0x2c]; then the bytes 0xF56E (the VFP block / a table — the capstone
   build quirk, not an "INVALID instruction").
5. **0x244D2** — data: the tail u16 table before the FOTA trailer (the PEM
   "-----BEGIN" @0x24845); no bl callers (the window of plus/minus 4KB) — not code.
6. **0x1893C** — the DFU command string pool (the step 0x32): "down rd_info" /
   "down get_ver" / "down dfu_active" ... (the 7 console commands, section 75).
7. **0x19810** — the model string "SZMC-ES-ZM-0283M" (data, in the gap section 55).

F1 (§98): 5+2 каталог-записи со статусом ID — закрыты (статика + эмулятор).

1. **0xC6F0** — живая функция (не «dead code?»): setter 3 инструкции
   `[0x42420060] = r0` (литерал 0x42420000 @0xC6F8); вызывающие 0x10C92 (r0=0,
   disable) / 0x10CA2 (r0=1, enable) из init-последовательности. Блок 0x4242xxxx
   вне текущей карты McuEmu (map-ится в тесте).
2. **0x17736** — артефакт детектора: байты B5 77 (похожи на push) ВНУТРИ u16-
   таблицы гигантского 0x17xxx-региона (hi^lo=0xC0, 100% на 48 записей
   0x17720..0x17780) — данные, не код.
3. **0x177D6** — cold-tail гигантского 0x17xxx: push{..,lr}; strh r0,[r5,#0x28];
   str r5,[sp,#0x24]; b 0x173BC (общий эпилог) — 4-инст. блок в дыре 0x177DE..0x19A1C.
4. **0x178C4** — cold-tail того же региона: push{..,lr}; adr r5,#0x32C;
   str r5,[sp,#0x2A0] (pool-указатель callee'ю, frame 0x2A0); strh r1,[r1,#0x2c];
   далее байт 0xF56E (VFP-блок / таблица — квид билда capstone, не «НЕВАЛИДНАЯ
   инструкция»).
5. **0x244D2** — данные: u16-таблица хвоста перед FOTA-trailer (PEM '-----BEGIN'
   @0x24845); bl-вызывающих нет (окно ±4КБ) — не код.
6. **0x1893C** — DFU-строковый пул команд (шаг 0x32): 'down rd_info' /
   'down get_ver' / 'down dfu_active' ... (7 команд консоли §75).
7. **0x19810** — строка модели 'SZMC-ES-ZM-0283M' (данные, в дыре §55).
"""

import struct  # noqa: E402

from fv_core import *  # noqa: F401,F403
from unicorn import UC_HOOK_CODE, UcError  # noqa: E402
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_SP,
                               UC_ARM_REG_LR)  # noqa: E402
from emulator.mcu_emu import McuEmu, RAM, FLASH0, FLASH1, STACK_TOP  # noqa: E402


def _capstone_block(start, count):
    """Decode the first `count` instructions from start (chunk decode).
    Декод первых count инструкций от start (покадрово)."""
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
    cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    out = []
    for ins in cs.disasm(FW[start:start + count * 4], start):
        out.append((ins.address, ins.mnemonic, ins.op_str))
        if len(out) >= count:
            break
    return out


@t(0xC6F0, 'F1 §98: 0xC6F0 — живой setter [0x42420060]=r0 (не «dead code»): литерал 0x42420000 @0xC6F8; вызывающие 0x10C92 (r0=0)/0x10CA2 (r0=1) — enable/disable из init. Эмулятор: map 0x42420000, r0=0x5A/0 → [0x42420060]')
def _(run, rng):
    """The F1 0xC6F0 test: the 0x42420060 setter verified in the emulator.
    Тест F1 0xC6F0: setter 0x42420060, верифицированный эмулятором."""
    # the base literal
    assert struct.unpack_from('<I', FW, 0xC6F8)[0] == 0x42420000
    # body: ldr r1,[pc,#4]; str r0,[r1,#0x60]; bx lr
    blk = _capstone_block(0xC6F0, 3)
    assert blk[0][0] == 0xC6F0 and blk[0][1] == 'ldr' and blk[0][2] == 'r1, [pc, #4]', blk[0]
    assert blk[1][1] == 'str' and blk[1][2] == 'r0, [r1, #0x60]', blk[1]
    assert blk[2][1] == 'bx', blk[2]
    # emulator: map 0x42420000, call with r0=0x5A and r0=0
    for val in (0x5A, 0):
        emu = McuEmu(max_insn=10000)
        uc = emu.uc
        uc.mem_map(0x42420000, 0x1000)
        uc.mem_write(0x42420000, bytes(0x1000))
        emu.hook_periph_ready()

        def sh(u, a, s, ud):
            """The stop when the execution leaves the code region.
            Стоп когда исполнение выходит за пределы кодовой области."""
            a2 = a & ~1
            if not (FLASH0 <= a2 < FLASH0 + 0x23680 or FLASH1 <= a2 < FLASH1 + 0x23680):
                u.emu_stop()
        uc.reg_write(UC_ARM_REG_R0, val)
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        h = uc.hook_add(UC_HOOK_CODE, sh)
        try:
            uc.emu_start(0xC6F0 | 1, 0, count=10000)
        except UcError:
            pass
        uc.hook_del(h)
        got = struct.unpack_from('<I', bytes(uc.mem_read(0x42420060, 4)))[0]
        assert got == val, f"r0={val}: [0x42420060]={got:#x}"


@t(0x17736, 'F1 §98: 0x17736 — артефакт детектора: байты B5 77 (push-подобные) внутри u16-таблицы 0x17xxx-региона (hi^lo=0xC0, 48/48 на 0x17720..0x17780) — данные, не код')
def _(run, rng):
    """The F1 0x17736 test: the hi^lo=0xC0 u16 table (data, not code).
    Тест F1 0x17736: u16-таблица hi^lo=0xC0 (данные, не код)."""
    ok = 0
    tot = 0
    for off in range(0x17720, 0x17780, 2):
        u = struct.unpack_from('<H', FW, off)[0]
        tot += 1
        if ((u >> 8) ^ (u & 0xFF)) == 0xC0:
            ok += 1
    assert tot == 48 and ok == tot, f"the hi^lo=0xC0 table: {ok}/{tot} (expect 100%)"
    # the "push" bytes at 0x17736 are part of the table
    u = struct.unpack_from('<H', FW, 0x17736)[0]
    assert ((u >> 8) ^ (u & 0xFF)) == 0xC0, f"0x17736 = {u:#x} is outside the table pattern"


@t(0x177D6, 'F1 §98: 0x177D6 — cold-tail гигантского 0x17xxx: push{..,lr}; strh r0,[r5,#0x28]; str r5,[sp,#0x24]; b 0x173BC (общий эпилог) — 4-инст. блок в дыре 0x177DE..0x19A1C (артефакт детекции, не самостоятельная функция)')
def _(run, rng):
    """The F1 0x177D6 test: the 4-instruction cold tail with b 0x173BC.
    Тест F1 0x177D6: 4-инструкционный cold-tail с b 0x173BC."""
    blk = _capstone_block(0x177D6, 4)
    assert blk[0][1] == 'push' and 'lr' in blk[0][2], blk[0]
    assert blk[1][1] == 'strh' and blk[1][2] == 'r0, [r5, #0x28]', blk[1]
    assert blk[2][1] == 'str' and blk[2][2] == 'r5, [sp, #0x24]', blk[2]
    assert blk[3][1] == 'b' and blk[3][2] == '#0x173bc', blk[3]


@t(0x178C4, 'F1 §98: 0x178C4 — cold-tail региона 0x17xxx: push{..,lr}; adr r5,#0x32C; str r5,[sp,#0x2A0] (pool-указатель callee, frame 0x2A0); strh r1,[r1,#0x2c]; далее 0xF56E = VFP/таблица (квид билда, не «невалидная инструкция»)')
def _(run, rng):
    """The F1 0x178C4 test: the cold tail with the 0x2A0 frame pool-pointer.
    Тест F1 0x178C4: cold-tail с pool-указателем и frame 0x2A0."""
    blk = _capstone_block(0x178C4, 4)
    assert blk[0][1] == 'push' and 'lr' in blk[0][2], blk[0]
    assert blk[1][1] == 'adr' and blk[1][2] == 'r5, #0x32c', blk[1]
    assert blk[2][1] == 'str' and blk[2][2] == 'r5, [sp, #0x2a0]', blk[2]
    assert blk[3][1] == 'strh' and blk[3][2] == 'r1, [r1, #0x2c]', blk[3]
    # the bytes 0xF56E @0x178CC — the VFP block / the data (not the code tail)
    assert struct.unpack_from('<H', FW, 0x178CC)[0] == 0xF56E


@t(0x244D2, 'F1 §98: 0x244D2 — данные: u16-таблица хвоста перед FOTA-trailer (PEM "-----BEGIN" @0x24845); bl-вызывающих нет (окно ±4КБ) — не код')
def _(run, rng):
    """The F1 0x244D2 test: the trailer LUT data (before the PEM certificate).
    Тест F1 0x244D2: данные хвоста перед PEM-сертификатом."""
    assert FW[0x24845:0x2484F] == b'-----BEGIN', 'the FOTA-trailer PEM @0x24845'
    assert 0x244D2 < 0x24845, '0x244D2 in the trailer region'
    # the tail u16 values are not code: >0x1000 (the Thumb insns are 16-bit, but the
    # table is full of the big values)
    big = 0
    for off in range(0x244C0, 0x24520, 2):
        if struct.unpack_from('<H', FW, off)[0] > 0x1000:
            big += 1
    assert big >= 20, f"the share of u16>0x1000 in the window: {big}/32"


@t(0x1893C, 'F1 §98: 0x1893C — DFU-строковый пул команд (шаг 0x32=50Б): "down rd_info" / "down get_ver" / "down dfu_active" (7 команд консоли §75) — данные')
def _(run, rng):
    """The F1 0x1893C test: the DFU console command string pool.
    Тест F1 0x1893C: пул команд DFU-консоли."""
    assert FW[0x1893C:0x1893C + 12] == b'down rd_info', FW[0x1893C:0x1893C + 12]
    assert FW[0x1896E:0x1896E + 12] == b'down get_ver', FW[0x1896E:0x1896E + 12]
    assert FW[0x189A0:0x189A0 + 15] == b'down dfu_active', FW[0x189A0:0x189A0 + 15]


@t(0x19810, 'F1 §98: 0x19810 — строка модели "SZMC-ES-ZM-0283M" (данные, в дыре §55) — идентификатор контроллера в MCU-образе')
def _(run, rng):
    """The F1 0x19810 test: the model string in the MCU image.
    Тест F1 0x19810: строка модели в MCU-образе."""
    assert FW[0x19810:0x19810 + 16] == b'SZMC-ES-ZM-0283M', FW[0x19810:0x19810 + 16]
