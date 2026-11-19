# -*- coding: utf-8 -*-
# ruff: noqa: F405  (names from the star-import of fv_core)
"""F3 (section 100): the RX handlers of the Group A (0x40/0x47/0x63) — closed
with the crafted frames (the retry of the TODO F3).

The old block (section 31.6.9): "the emulation of the 0x40/0x63 handlers is
blocked by a data-driven call" — after the ctx-slot cleanup method of section
80.5 (zeroing the 8 slots @0x10B5+i*0x96 before the call) all three Group-A
handlers are emulated deterministically (3/3 runs are identical):

- **'@' (0x40)** — the head-only frame: the RAM writes {0x171:0, 0x172:0,
  0x2C0:1} (the RX flag/state are cleared, the head++), the ctx-slot is
  unchanged (no response frame is built).
- **'G' (0x47)** — the frame-start (LEN=0x14): ctx-slot 0 = {6,'e',0x14,'O','K',
  0x13,0x9A} (chk5-sum 0x13 — the register quirk of this Unicorn build,
  deterministic; checksum 0x9A = 0xFF-0x65), the flag 0x310=0, the toggle 0x2C9
  0->1 and the head 0x2C0 -> 1.
- **'c' (0x63)** — the frame-start (LEN=0x53): ctx-slot 0 = {6,'e',0x53,'O','K',
  0x52,0x9A}, the flag 0x36F=0, the toggle 0x2C9 0->1, the head 0x2C0 -> 1.

The dispatch (the section 80.2 table @0x1EB38): the Group A {0x40,0x47,0x4B,0x63}
-> the direct handlers (0x40 -> the tail 0x1F0B4, 0x47 -> 0x1EBAA, 0x4B -> 0x1EBDE,
0x63 -> 0x1EC14); the Group B -> the jump-table @0x1EC5E. The 0x40 handler is a
pure exit to the shared tail (the "complement-param" code @0x1EB94 is the tail of
the second RX switch of the parser, not the 0x40 body).

F3 (§100): RX-хендлеры группы A (0x40/0x47/0x63) — закрыты crafted-кадрами
(повтор TODO F3).

Старый блок (§31.6.9): «эмуляция 0x40/0x63 заблокирована data-driven вызовом» —
после методики чистки ctx-слотов §80.5 (нуллирование 8 слотов @0x10B5+i*0x96
перед вызовом) все три хендлера группы A эмулируются детерминированно (3/3
прогона идентичны):

- **`'@' (0x40)`** — head-only кадр: RAM-записи {0x171:0, 0x172:0, 0x2C0:1}
  (RX-флаг/состояние сброшены, head++), ctx-слот не меняется (ответный кадр не
  собирается).
- **`'G' (0x47)`** — frame-start (LEN=0x14): ctx-слот 0 = {6,'e',0x14,'O','K',
  0x13,0x9A} (chk5-сумма 0x13 — регистровый квид этого Unicorn-билда,
  детерминирована; checksum 0x9A = 0xFF-0x65), флаг 0x310=0, toggle 0x2C9 0→1
  и head 0x2C0→1.
- **`'c' (0x63)`** — frame-start (LEN=0x53): ctx-слот 0 = {6,'e',0x53,'O','K',
  0x52,0x9A}, флаг 0x36F=0, toggle 0x2C9 0→1, head 0x2C0→1.

Диспатч (таблица §80.2 @0x1EB38): группа A {0x40,0x47,0x4B,0x63} -> прямые
хендлеры (0x40 -> хвост 0x1F0B4, 0x47 -> 0x1EBAA, 0x4B -> 0x1EBDE,
0x63 -> 0x1EC14); группа B -> jump-table @0x1EC5E. Хендлер 0x40 — чистый
выход в общий хвост («complement-param» @0x1EB94 — хвост второго RX-свитча
парсера, а не тело 0x40).
"""

import struct  # noqa: E402

from fv_core import *  # noqa: F401,F403

from unicorn import UC_HOOK_MEM_WRITE  # noqa: E402
from emulator.mcu_emu import (UsartRxContext, RX_STATE_OFF, RX_HEAD_OFF,  # noqa: E402
                              RX_TOGGLE_OFF, RX_RING_OFF)


def _rx_probe_f3(run, cmd, payload=b''):
    """The fresh RX context + the crafted frame; return the (off, val) RAM-write
    list (the section 80.5 method: the ctx-slots are zeroed before the call).
    Свежий RX-контекст + crafted-кадр; список RAM-записей (off, val) (методика
    §80.5: ctx-слоты нуллятся перед вызовом)."""
    uc = run.uc
    frame = UsartRxContext.craft(cmd, payload)
    uc.mem_write(RAM + RX_STATE_OFF, bytes([1]))
    uc.mem_write(RAM + RX_HEAD_OFF, bytes([0]))
    uc.mem_write(RAM + RX_TOGGLE_OFF, bytes([0]))
    # флаги G/K/c — чистим: общий Run в сьюите наследует состояния предыдущих
    # тестов (иначе записи «исчезают» при no-op-повторах)
    uc.mem_write(RAM + 0x310, bytes([0]))
    uc.mem_write(RAM + 0x369, bytes([0]))
    uc.mem_write(RAM + 0x36F, bytes([0]))
    uc.mem_write(RAM + RX_RING_OFF, frame)
    ev = []

    def hw(u_, acc, addr, size, val, usr):
        """The write hook: collect the RAM writes (without the stack region).
        Write-хук: собрать RAM-записи (без стековой области)."""
        if RAM <= addr < RAM + 0x20000 and not (0x20017F00 <= addr < 0x20018000):
            ev.append((addr - RAM, val & 0xFF))

    h = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, RAM, RAM + 0x20000)
    try:
        run.call(0x1E9E0, [], max_insn=50000)
    finally:
        uc.hook_del(h)
    return ev


def _ctx_f3(run, slot=0, n=13):
    """The ctx-slot bytes.
    Байты ctx-слота."""
    return bytes(run.uc.mem_read(UsartRxContext.slot_base(slot), n))


@t(0x1E9E0, 'F3 §100: RX "@" (0x40) группа A — head-only кадр: записи {0x171:0, 0x172:0, 0x2C0:1} (флаг/статус сброс, head++), ctx-слот не тронут (ответ не собирается); хендлер = чистый выход в хвост 0x1F0B4')
def _(run, rng):
    """The F3 0x40 test: the '@' head-only RX frame.
    Тест F3 0x40: head-only RX-кадр '@'.
    """
    ev = _rx_probe_f3(run, '@', bytes([0x91, 0x92]))
    got = dict(ev)
    assert got.get(0x171) == 0 and got.get(0x172) == 0, f'флаг/статус: {ev}'
    assert got.get(0x2C0) == 1, f'head++: {ev}'
    assert 0x2C1 not in got, f'0x2C1 не должен писаться: {ev}'
    assert got.get(RX_TOGGLE_OFF) is None, f'toggle не меняется: {ev}'
    ctx = _ctx_f3(run, 0)
    assert ctx == bytes(13), f'ctx-слот должен остаться нулевым: {ctx.hex(" ")}'
    # детерминизм
    ev2 = _rx_probe_f3(run, '@', bytes([0x77, 0x88]))
    assert dict(ev2).get(0x2C0) == 1 and dict(ev2).get(0x172) == 0, f'повтор: {ev2}'


@t(0x1E9E0, 'F3 §100: RX "G" (0x47) группа A — frame-start (LEN=0x14): ctx {6,\'e\',0x14,\'O\',\'K\',0x13,0x9A} (chk5-сумма 0x13 — квид билда, детерминирована; checksum 0x9A=0xFF-0x65), флаг 0x310=0, toggle 0x2C9 0→1, head 0x2C0→1')
def _(run, rng):
    """The F3 0x47 test: the 'G' frame-start RX frame (LEN=0x14).
    Тест F3 0x47: frame-start RX-кадр 'G' (LEN=0x14).
    """
    ev = _rx_probe_f3(run, 'G', bytes([0x91, 0x92]))
    got = dict(ev)
    assert got.get(0x310) == 0, f'флаг 0x310: {ev}'
    assert got.get(0x2C9) == 1 and got.get(0x2C0) == 1, f'toggle/head: {ev}'
    assert got.get(0x171) == 0 and got.get(0x172) == 0, f'флаг/статус: {ev}'
    ctx = _ctx_f3(run, 0)
    assert ctx[:7] == bytes([6, 0x65, 0x14, 0x4F, 0x4B, 0x13, 0x9A]), \
        f'ctx: {ctx.hex(" ")}'
    assert ctx[6] == 0xFF - 0x65, f'checksum: {ctx.hex(" ")}'


@t(0x1E9E0, 'F3 §100: RX "c" (0x63) группа A — frame-start (LEN=0x53): ctx {6,\'e\',0x53,\'O\',\'K\',0x52,0x9A}, флаг 0x36F=0, toggle 0x2C9 0→1, head 0x2C0→1 (повторное закрытие 0x63 с полным write-сигнатуром; §31.6.9-блок «data-driven» снят чисткой ctx-слотов §80.5)')
def _(run, rng):
    """The F3 0x63 test: the 'c' frame-start RX frame (LEN=0x53) with the full
    write signature.
    Тест F3 0x63: frame-start RX-кадр 'c' (LEN=0x53) с полным write-сигнатуром.
    """
    ev = _rx_probe_f3(run, 'c', bytes([0x91, 0x92]))
    got = dict(ev)
    assert got.get(0x36F) == 0, f'флаг 0x36F: {ev}'
    assert got.get(0x2C9) == 1 and got.get(0x2C0) == 1, f'toggle/head: {ev}'
    assert got.get(0x171) == 0 and got.get(0x172) == 0, f'флаг/статус: {ev}'
    ctx = _ctx_f3(run, 0)
    assert ctx[:7] == bytes([6, 0x65, 0x53, 0x4F, 0x4B, 0x52, 0x9A]), \
        f'ctx: {ctx.hex(" ")}'
    assert ctx[6] == 0xFF - 0x65, f'checksum: {ctx.hex(" ")}'
    # полный write-сигнатур детерминирован (chk-накопление 0x177/0x178)
    chk_writes = [(o, v) for o, v in ev if o in (0x177, 0x178)]
    assert len(chk_writes) >= 8, f'chk-накопление: {ev}'
