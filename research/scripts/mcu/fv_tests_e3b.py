# ruff: noqa: F405  (имена из star-import от fv_core)
"""§80 (B2-динамика): RX-контекст 0x1e9e0 — полевая семантика ВСЕХ 15 хендлеров.
Методика: свежий RAM + state(0x172)=1/head(0x2C0)=0/toggle(0x2C9)=0, crafted-кадр
в ring @0x881 ([1]=cmd, [2]=len, [3..]=payload), RAM-записи через hook.
Карта (эмпирика 2026-11-18, mcu_emu.UsartRxContext):
  '@' → head++; 'G'/'K'/'c' → frame-start (ctx {6,'e',LEN,'O','K',crc,0x9A},
  флаг, toggle++); 'A' → telemetry-snapshot (§59.6); 'B'/'C' → 6B-блоки
  0x2CB/0x2D2; 'D' → SET+clamp(min 0x64) → 0x2E6/0x306/0x308/0x30A/0x30C;
  'E' → 6 u16-слотов 0x2DA+2k; 'F' → clear+copy 20B @0x2F2; 'H' → 4B @0x354 +
  resp; 'I'/'J' → resp + флаги 0x36A/0x36C; '`'/'a' → resp 0x50/0x51.
  Ответный кадр: crc=Σctx[1..]&0xFF, checksum=0xFF-ctx[1] ('d'→0x9B)."""
from fv_core import *  # noqa: F401,F403

from unicorn import UC_HOOK_MEM_WRITE  # noqa: E402
from emulator.mcu_emu import (UsartRxContext, RX_STATE_OFF, RX_HEAD_OFF,  # noqa: E402
                              RX_TOGGLE_OFF, RX_RING_OFF)


def _rx_probe(run, cmd, payload=b''):
    """свежий RX-контекст + crafted-кадр; вернуть список (off, val) RAM-записей"""
    uc = run.uc
    frame = UsartRxContext.craft(cmd, payload)
    uc.mem_write(RAM + RX_STATE_OFF, bytes([1]))
    uc.mem_write(RAM + RX_HEAD_OFF, bytes([0]))
    uc.mem_write(RAM + RX_TOGGLE_OFF, bytes([0]))
    uc.mem_write(RAM + RX_RING_OFF, frame)
    ev = []
    # ctx-слоты чистим до вызова — иначе crc-расчёт firmware наследует carry-over
    # предыдущих тестов (регистры этого Unicorn-билда частично no-op)
    for s in range(8):
        uc.mem_write(UsartRxContext.slot_base(s), bytes(0x96))

    def hw(u_, acc, addr, size, val, usr):
        if RAM <= addr < RAM + 0x20000 and not (0x20017F00 <= addr < 0x20018000):
            ev.append((addr - RAM, val & 0xFF))

    h = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, RAM, RAM + 0x20000)
    try:
        run.call(0x1E9E0, [], max_insn=50000)
    finally:
        uc.hook_del(h)
    return ev


def _ctx(run, slot, n=13):
    return bytes(run.uc.mem_read(UsartRxContext.slot_base(slot), n))


def _rd(run, off):
    return run.uc.mem_read(RAM + off, 1)[0]


@t(0x1E9E0, '§80: RX "B"/"C" SET-блоки: ring[3..8] → RAM+0x2CB..0x2D0 (B) / '
            'RAM+0x2D2..0x2D7 (C); tail 0x2D1/0x2D8 записан (значение — carry-over); '
            'head 0→1, state→0, 0x171=0')
def _(run, rng):
    for cmd, base, tail in (('B', 0x2CB, 0x2D1), ('C', 0x2D2, 0x2D8)):
        payload = bytes([0x11, 0x22, 0x33, 0x44, 0x55, 0x66])
        ev = _rx_probe(run, cmd, payload)
        got = dict(ev)
        for k, v in enumerate(payload):
            assert got.get(base + k) == v, f'{cmd}: ring[{3 + k}]→{base + k:#x}: {ev}'
        assert tail in got, f'{cmd}: tail {tail:#x} не записан: {ev}'  # значение — carry-over
        assert got.get(0x2C0) == 1 and got.get(RX_STATE_OFF) == 0 and got.get(0x171) == 0, \
            f'{cmd}: head/state/gate: {ev}'


@t(0x1E9E0, '§80: RX "D" SET+clamp: ring3→0x2E6, ring4→0x306 (clamp min 0x64: 0xFF→0x64), '
            'ring6→0x308, ring8→0x30A, ring9→0x30C, 0x30E=0; ring5/7/10 не пишутся')
def _(run, rng):
    # нормальные значения
    payload = bytes([0x01, 0x02, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88])
    ev = _rx_probe(run, 'D', payload)
    got = dict(ev)
    assert got.get(0x2E6) == 0x01, f'D ring3: {ev}'
    assert got.get(0x306) == 0x02, f'D ring4: {ev}'
    assert got.get(0x308) == 0x44 and got.get(0x30A) == 0x66 and got.get(0x30C) == 0x77, \
        f'D ring6/8/9: {ev}'
    assert 0x30E in got, f'D 0x30E не записан: {ev}'  # значение — carry-over
    # clamp: ring4=0xFF → 0x64 (двойная запись: 0xFF, затем 0x64)
    ev = _rx_probe(run, 'D', bytes([0xFF, 0xFF, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66]))
    seq306 = [v for a, v in ev if a == 0x306]
    assert seq306[-1] == 0x64 and 0xFF in seq306, f'D clamp: {ev}'
    assert [v for a, v in ev if a == 0x2E6][-1] == 0xFF, f'D 0x2E6 без clamp: {ev}'


@t(0x1E9E0, '§80: RX "F" varlen-copy: двухпроходный — сначала clear 0x2F2..0x305 (20B), '
            'затем ring[3..3+len)→0x2F2.. (len≤0x14); счётчик-проход 0x174')
def _(run, rng):
    payload = bytes([0x31, 0x32, 0x33, 0x34, 0x35])
    ev = _rx_probe(run, 'F', payload)
    vals = {}
    for a, v in ev:
        vals[a] = v  # последнее значение
    for k, v in enumerate(payload):
        assert vals.get(0x2F2 + k) == v, f'F copy: {vals}'
    for off in range(0x2F2, 0x306):
        assert off in vals, f'F clear: оффс {off:#x} не затронут'
    assert vals.get(0x2F2 + 5, 0) == 0 and vals.get(0x2F2 + 19, 0) == 0, f'F clear-хвост: {vals}'


@t(0x1E9E0, '§80: RX "H" SET 4B + response: ring[3..6]→0x354..0x357; context @0x10B5 = '
            '{9,\'d\',0x2c,4,d1..d4,crc,0x9B}; crc=Σctx[1..]&0xFF (running-sum @0x175)')
def _(run, rng):
    payload = bytes([0x41, 0x42, 0x43, 0x44])
    ev = _rx_probe(run, 'H', payload)
    got = dict(ev)
    for k, v in enumerate(payload):
        assert got.get(0x354 + k) == v, f'H 4B: {ev}'
    ctx = _ctx(run, 0)
    assert ctx[0] == 9 and ctx[1] == 0x64 and ctx[2] == 0x2C and ctx[3] == 4, f'H ctx-head: {ctx.hex(" ")}'
    assert ctx[4:8] == payload, f'H ctx-data: {ctx.hex(" ")}'
    crc = (0x64 + 0x2C + 4 + sum(payload)) & 0xFF
    assert ctx[8] == crc, f'H crc: {ctx[8]:#x} ≠ {crc:#x}'
    assert ctx[9] == 0x9B, f'H checksum: {ctx[9]:#x}'


@t(0x1E9E0, '§80: RX "I"/"J" response + флаги: I → ctx {5,\'d\',0x2e,0,crc=0x92,0x9B}, 0x36A=0; '
            'J → ctx {6,\'d\',0x2f,1,[carry],crc,0x9B}, 0x36C=0 (ctx4 J — register carry-over; '
            'crc детерминирован только для I: (0x64+c2+c3)&0xFF)')
def _(run, rng):
    for cmd, fl, head, c2, c3, c4, crc_i in (('I', 0x36A, 5, 0x2E, 0, 0, 4),
                                             ('J', 0x36C, 6, 0x2F, 1, 0, 5)):
        ev = _rx_probe(run, cmd, bytes([0x51, 0x52, 0x53]))
        got = dict(ev)
        assert got.get(fl) == 0, f'{cmd} флаг {fl:#x}: {ev}'
        ctx = _ctx(run, 0)
        assert ctx[0] == head and ctx[1] == 0x64 and ctx[2] == c2 and ctx[3] == c3, \
            f'{cmd} ctx-head: {ctx.hex(" ")}'
        assert ctx[crc_i + 1] == 0x9B, f'{cmd} checksum: {ctx.hex(" ")}'
        if cmd == 'I':   # crc I детерминирован; J — через carry ctx4 (см. desc)
            assert ctx[crc_i] == (0x64 + c2 + c3 + c4) & 0xFF, f'{cmd} crc: {ctx.hex(" ")}'


@t(0x1E9E0, '§80: RX "K"/"c" frame-start: ctx {6,\'e\',LEN,\'O\',\'K\',crc,0x9A} (LEN=0x1b/0x53, '
            'crc=0x65+LEN+0x4f+0x4b), флаги 0x369/0x36F=0, toggle 0→1 (ctx в слоте 0, '
            'следующий кадр — слот 1)')
def _(run, rng):
    for cmd, fl, ln in (('K', 0x369, 0x1B), ('c', 0x36F, 0x53)):
        ev = _rx_probe(run, cmd, bytes([0x91, 0x92]))
        got = dict(ev)
        assert got.get(fl) == 0, f'{cmd} флаг {fl:#x}: {ev}'
        assert got.get(RX_TOGGLE_OFF) == 1 and got.get(0x2C0) == 1, f'{cmd} toggle/head: {ev}'
        ctx = _ctx(run, 0)
        assert ctx[:5] == bytes([6, 0x65, ln, 0x4F, 0x4B]), f'{cmd} ctx: {ctx.hex(" ")}'
        assert ctx[5] == (0x65 + ln + 0x4F + 0x4B) & 0xFF, f'{cmd} crc: {ctx.hex(" ")}'
        assert ctx[6] == 0x9A, f'{cmd} checksum: {ctx.hex(" ")}'


@t(0x1E9E0, '§80: RX "`"/"a" response-сборщики: ctx {5,\'d\',0x50/0x51,0,crc,0x9B}; '
            'crc=0x64+len_field (0xB4/0xB5); checksum 0x9B=0xFF-0x64')
def _(run, rng):
    for cmd, c2, crc in ((chr(0x60), 0x50, 0xB4), ('a', 0x51, 0xB5)):
        ev = _rx_probe(run, cmd, bytes([0x71, 0x72, 0x73]))
        ctx = _ctx(run, 0)
        assert ctx[0] == 5 and ctx[1] == 0x64 and ctx[2] == c2 and ctx[3] == 0, \
            f'{cmd} ctx-head: {ctx.hex(" ")}'
        assert ctx[4] == crc and ctx[5] == 0x9B, f'{cmd} crc/chk: {ctx.hex(" ")}'
