# -*- coding: utf-8 -*-
"""E2-b64: memcpy/memset, u64 signed-коррекция, boot-wait, 3-слотовые очереди
(free ×2 / producer ×2), frame-copy helper, RLE-кодировщик, const-calc, 2D-bilinear Q8."""
# ruff: noqa: F405  (имена из star-import от fv_core)
from fv_core import *  # noqa: F401,F403
from fv_core import _fresh_call, _intercept  # noqa: F401


@t(0x19A68, 'E2-b64: 0x19a68(dst,src,len) — memcpy: word-fast-path (оба ptr выровнены по 4) + byte-tail; '
            'ret = dst+len.')
def _(run, rng):
    """Emulator test @ 0x19a68: E2-b64: 0x19a68(dst,src,len) — memcpy: word-fast-path (оба ptr выровнены по 4) + byte-tail; ret = dst+len..
    Тест эмулятора @ 0x19a68: E2-b64: 0x19a68(dst,src,len) — memcpy: word-fast-path (оба ptr выровнены по 4) + byte-tail; ret = dst+len..
    """
    SRC, DST = 0x200, 0x300
    for _ in range(40):
        n = rng.randint(0, 40)
        data = bytes(rng.getrandbits(8) for _ in range(n))
        run.ram_write(SRC, data)
        run.ram_write(DST, bytes(n))
        ret, _ = run.call(0x19A68, (RAM + DST, RAM + SRC, n), max_insn=2000)
        got = run.ram_read(DST, n)
        assert got == data, f'n={n}: dst {got.hex()[:24]}… ≠ {data.hex()[:24]}…'
        assert ret == (RAM + DST + n) & M32, f'n={n}: ret={ret:#x} ≠ {(RAM+DST+n)&M32:#x}'


@t(0x19A8C, 'E2-b64: 0x19a8c(dst,count,byte) — memset: count байт = byte (uxtb); ret = dst+count.')
def _(run, rng):
    """Emulator test @ 0x19a8c: E2-b64: 0x19a8c(dst,count,byte) — memset: count байт = byte (uxtb); ret = dst+count..
    Тест эмулятора @ 0x19a8c: E2-b64: 0x19a8c(dst,count,byte) — memset: count байт = byte (uxtb); ret = dst+count..
    """
    DST = 0x300
    for _ in range(40):
        n = rng.randint(0, 40)
        b = rng.getrandbits(32)
        run.ram_write(DST, bytes(n))
        ret, _ = run.call(0x19A8C, (RAM + DST, n, b), max_insn=2000)
        got = run.ram_read(DST, n)
        exp = bytes([b & 0xFF]) * n
        assert got == exp, f'n={n} byte={b:#x}: {got.hex()[:24]}… ≠ {exp.hex()[:24]}…'
        assert ret == (RAM + DST + n) & M32, f'n={n}: ret={ret:#x}'


def ref_1a16a(lo, hi, lo2, hi2):
    """Эмпирический контракт: hi2 ≥ 0 (s32) → без изменений;
    иначе (lo,hi) += 1; (lo2,hi2) *= 2; если удвоенное == 0 (B == 2^63) → lo &= ~1."""
    if hi2 < 0x80000000:
        return lo, hi
    v = ((hi << 32) | lo) + 1
    lo_r, hi_r = v & M32, (v >> 32) & M32
    if hi2 == 0x80000000 and lo2 == 0:
        lo_r = lo_r & 0xFFFFFFFE
    return lo_r, hi_r


@t(0x1A16A, 'E2-b64: 0x1a16a(lo,hi,lo2,hi2) — u64 signed-коррекция: hi2≥0 → passthrough; иначе (lo,hi)+=1, '
            '(lo2,hi2)*=2, при B==2^63 → lo&=~1. ret=(lo,hi). (каталог «u64 sub» — контракт уточнён эмпирически)')
def _(run, rng):
    """Emulator test @ 0x1a16a: E2-b64: 0x1a16a(lo,hi,lo2,hi2) — u64 signed-коррекция: hi2≥0 → passthrough; иначе (lo,hi)+=1, (lo2,hi2)*=2, при B==2^63 → lo&=~1. ret=(lo,hi). (каталог «u64 sub» — контракт уточнён эмпирически).
    Тест эмулятора @ 0x1a16a: E2-b64: 0x1a16a(lo,hi,lo2,hi2) — u64 signed-коррекция: hi2≥0 → passthrough; иначе (lo,hi)+=1, (lo2,hi2)*=2, при B==2^63 → lo&=~1. ret=(lo,hi). (каталог «u64 sub» — контракт уточнён эмпирически).
    """
    for _ in range(40):
        lo, hi = rng.getrandbits(32), rng.getrandbits(32)
        if rng.random() < 0.5:
            hi2, lo2 = rng.getrandbits(31), rng.getrandbits(32)   # ветка passthrough
        elif rng.random() < 0.1:
            hi2, lo2 = 0x80000000, 0                                # спец-кейс B == 2^63
        else:
            hi2, lo2 = 0x80000000 + rng.getrandbits(31), rng.getrandbits(32)
        ret, ret1 = run.call(0x1A16A, (lo, hi, lo2, hi2), max_insn=500)
        exp_lo, exp_hi = ref_1a16a(lo, hi, lo2, hi2)
        assert (ret, ret1) == (exp_lo, exp_hi), (
            f'lo={lo:#x} hi={hi:#x} lo2={lo2:#x} hi2={hi2:#x}: '
            f'({ret:#x},{ret1:#x}) ≠ ({exp_lo:#x},{exp_hi:#x})')


def ref_17524(v, w):
    """v = byte[RAM+0xFD3], w = u32[RAM+8]: v>0x1E → w=0, ret 0; w<0x10E0 → ret 0 (w нетронут);
    иначе w=0x10E0, ret 1."""
    if v > 0x1E:
        return 0, 0
    if w < 0x10E0:
        return 0, w
    return 1, 0x10E0


@t(0x17524, 'E2-b64: 0x17524() — boot-wait предикат (дыра данных §55): v=byte[RAM+0xFD3], w=u32[RAM+8]; '
            'v>0x1E → w:=0, ret 0; w<0x10E0 → ret 0 (w нетронут); иначе w:=0x10E0, ret 1.')
def _(run, rng):
    """Emulator test @ 0x17524: E2-b64: 0x17524() — boot-wait предикат (дыра данных §55): v=byte[RAM+0xFD3], w=u32[RAM+8]; v>0x1E → w:=0, ret 0; w<0x10E0 → ret 0 (w нетронут); иначе w:=0x10E0, ret 1..
    Тест эмулятора @ 0x17524: E2-b64: 0x17524() — boot-wait предикат (дыра данных §55): v=byte[RAM+0xFD3], w=u32[RAM+8]; v>0x1E → w:=0, ret 0; w<0x10E0 → ret 0 (w нетронут); иначе w:=0x10E0, ret 1..
    """
    cases = []
    for v in (0x1E, 0x1F, 0x20, 0x30, 0xFF):
        for w in (0x10DF, 0x10E0, 0x10E1, 0):
            cases.append((v, w))
    rng.shuffle(cases)
    for v, w in cases:
        run.ram_write(0xFD3, bytes([v]))
        run.ram_write(0x8, struct.pack('<I', w))
        ret, _ = run.call(0x17524, (), max_insn=500)
        gw = struct.unpack_from('<I', run.ram_read(0x8, 4))[0]
        exp_ret, exp_w = ref_17524(v, w)
        assert (ret, gw) == (exp_ret, exp_w), (
            f'v={v:#x} w={w:#x}: ret={ret} w={gw:#x} ждём ret={exp_ret} w={exp_w:#x}')


def _free3_ref(state, cnt0):
    """3-слотовая очередь (free): state&7==0 → ret 0; иначе скан cnt=(cnt0+1)%3…
    до первого ЗАДАННОГО бита; ret 1, cnt — найденный."""
    if (state & 7) == 0:
        return 0, None
    cnt = cnt0
    while True:
        cnt = (cnt + 1) % 3
        if state & (1 << cnt):
            return 1, cnt


def _free3_case(run, off, S, state, cnt0, slots):
    """slots[cnt] = (len, data). Заполняет все 3 слота + state/counter, вызывает off,
    проверяет: ret, byte[S], byte[S+1]=cnt, u16[dst]=len, data@dst+2, бит снят."""
    DST = 0x2000
    for i in range(3):
        ln, data = slots[i]
        run.ram_write(S + 2 + 152 * i, struct.pack('<H', ln) + data)
    run.ram_write(S, bytes([state, cnt0]))
    run.ram_write(DST, bytes(0x30))
    ret, _ = run.call(off, (RAM + DST,), max_insn=2000)
    got_state = run.ram_read(S, 1)[0]
    got_cnt = run.ram_read(S + 1, 1)[0]
    got_len = struct.unpack_from('<H', run.ram_read(DST, 2))[0]
    ret_exp, cnt_exp = _free3_ref(state, cnt0)
    assert ret == ret_exp, f'S={S:#x} state={state:#04x} cnt0={cnt0}: ret={ret} ждём {ret_exp}'
    if cnt_exp is None:
        assert got_len == 0, 'ret=0: u16[dst] должен остаться 0'
        return
    ln, data = slots[cnt_exp]
    assert got_cnt == cnt_exp, f'byte[S+1]={got_cnt} ждём cnt={cnt_exp}'
    assert got_state == (state & ~(1 << cnt_exp)) & 0xFF, (
        f'byte[S]={got_state:#x} ждём {(state & ~(1 << cnt_exp)):#x}')
    assert got_len == ln, f'u16[dst]={got_len:#x} ждём len={ln:#x}'
    got_data = run.ram_read(DST + 2, ln)
    assert got_data == data[:ln], f'data {got_data.hex()} ≠ {data[:ln].hex()}'


@t(0x12D04, 'E2-b64: 0x12d04(dst) — 3-слотовая очередь: free (база P=0x190D: state=P, counter=P+1, '
            'слот cnt: u16@P+2+152cnt=len, data@P+4+152cnt). state&7==0 → ret 0; иначе скан (cnt0+1)%3.. '
            'до заданного бита: byte[P+1]=cnt, u16[dst]=len, memcpy(dst+2, data, len), byte[P]&=~bit, ret 1.')
def _(run, rng):
    """Emulator test @ 0x12d04: E2-b64: 0x12d04(dst) — 3-слотовая очередь: free (база P=0x190D: state=P, counter=P+1, слот cnt: u16@P+2+152cnt=len, data@P+4+152cnt). state&7==0 → ret 0; иначе скан (cnt0+1)%3.. до заданного бита: byte[P+1]=cnt, u16[dst]=len, memcpy(dst+2, data, len), byte[P]&=~bit, ret 1..
    Тест эмулятора @ 0x12d04: E2-b64: 0x12d04(dst) — 3-слотовая очередь: free (база P=0x190D: state=P, counter=P+1, слот cnt: u16@P+2+152cnt=len, data@P+4+152cnt). state&7==0 → ret 0; иначе скан (cnt0+1)%3.. до заданного бита: byte[P+1]=cnt, u16[dst]=len, memcpy(dst+2, data, len), byte[P]&=~bit, ret 1..
    """
    S = 0x190D
    cases = [(0x00, 0), (0b010, 0), (0b101, 0), (0b110, 2), (0b001, 0), (0b111, 1)]
    rng.shuffle(cases)
    for state, cnt0 in cases:
        slots = [(rng.randint(1, 8), bytes(rng.getrandbits(8) for _ in range(8))) for _ in range(3)]
        _free3_case(run, 0x12D04, S, state, cnt0, slots)


@t(0x12F44, 'E2-b64: 0x12f44(dst) — 3-слотовая очередь: free #2 (твин 0x12d04, база S2=0x1D38, '
            'та же layout/стрид 152). Вериф тех же 6 state/cnt-сценариев.')
def _(run, rng):
    """Emulator test @ 0x12f44: E2-b64: 0x12f44(dst) — 3-слотовая очередь: free #2 (твин 0x12d04, база S2=0x1D38, та же layout/стрид 152). Вериф тех же 6 state/cnt-сценариев..
    Тест эмулятора @ 0x12f44: E2-b64: 0x12f44(dst) — 3-слотовая очередь: free #2 (твин 0x12d04, база S2=0x1D38, та же layout/стрид 152). Вериф тех же 6 state/cnt-сценариев..
    """
    S = 0x1D38
    for state, cnt0 in [(0x00, 0), (0b010, 0), (0b101, 0),
                        (0b110, 2), (0b001, 0), (0b111, 1)]:
        slots = [(rng.randint(1, 8), bytes(rng.getrandbits(8) for _ in range(8))) for _ in range(3)]
        _free3_case(run, 0x12F44, S, state, cnt0, slots)


def _prod_case(off, S, tail_w, state0, cnt0, ln, buf):
    """producer-кейс на СВЕЖЕМ emu (fresh, zero-RAM + явные сиды — shared-Run не детерминирован
    из-за внутренних сканов узла 0x12e64/0x12c24). Возвращает (ret, emu)."""
    DST, BUF = 0x2000, 0x2010
    seed = [(RAM + S, bytes([state0, cnt0])),
            (RAM + tail_w, bytes(8)),
            (RAM + BUF, buf)]
    ret, emu = _fresh_call(off, (RAM + DST, RAM + BUF, ln), extra_ram=seed, max_insn=60000)
    return ret, emu


def _prd(emu, off, n):
    """The helper function (_prd).
    Вспомогательная функция (_prd).
    """
    return emu.uc.mem_read(RAM + off, n)


@t(0x13284, 'E2-b64: 0x13284(arg0,buf,len) — 3-слотовая очередь: producer #1 (S=0x1B6E, стрид 152, '
            'узел 0x12e64). len>0x96 → ret=arg0; state&7==7 → ret=byte[S] (ldrb); иначе аллокация '
            'свободного бита (скан от (cnt0+1)%3): byte[S]|=bit, byte[S+1]=cnt, u16[S+2+152cnt]=len, '
            'memcpy(S+4+152cnt, buf, len), bl 0x12e64. Эмпирика (SP=STACK_TOP−0x40): zero-RAM → '
            'byte[S]=2, byte[S+1]=1, byte[0xB76]=4, u16[0xB7C]=0, ret=0x2501491F; '
            'state0=0b001 → byte[S]=3, byte[S+1]=1, то же tail.')
def _(run, rng):
    """Emulator test @ 0x13284: E2-b64: 0x13284(arg0,buf,len) — 3-слотовая очередь: producer #1 (S=0x1B6E, стрид 152, узел 0x12e64). len>0x96 → ret=arg0; state&7==7 → ret=byte[S] (ldrb); иначе аллокация свободного бита (скан от (cnt0+1)%3): byte[S]|=bit, byte[S+1]=cnt, u16[S+2+152cnt]=len, memcpy(S+4+152cnt, buf, len), bl 0x12e64. Эмпирика (SP=STACK_TOP−0x40): zero-RAM → byte[S]=2, byte[S+1]=1, byte[0xB76]=4, u16[0xB7C]=0, ret=0x2501491F; state0=0b001 → byte[S]=3, byte[S+1]=1, то же tail..
    Тест эмулятора @ 0x13284: E2-b64: 0x13284(arg0,buf,len) — 3-слотовая очередь: producer #1 (S=0x1B6E, стрид 152, узел 0x12e64). len>0x96 → ret=arg0; state&7==7 → ret=byte[S] (ldrb); иначе аллокация свободного бита (скан от (cnt0+1)%3): byte[S]|=bit, byte[S+1]=cnt, u16[S+2+152cnt]=len, memcpy(S+4+152cnt, buf, len), bl 0x12e64. Эмпирика (SP=STACK_TOP−0x40): zero-RAM → byte[S]=2, byte[S+1]=1, byte[0xB76]=4, u16[0xB7C]=0, ret=0x2501491F; state0=0b001 → byte[S]=3, byte[S+1]=1, то же tail..
    """
    S = 0x1B6E
    buf = bytes(rng.getrandbits(8) for _ in range(8))
    # ранние выходы
    ret, r = _prod_case(0x13284, S, 0xB76, 0, 0, 0x97, buf)
    assert ret == (RAM + 0x2000) & M32, f'len>0x96: ret={ret:#x}'
    assert _prd(r, S, 1)[0] == 0, 'len>0x96: byte[S] должен остаться 0'
    ret, r = _prod_case(0x13284, S, 0xB76, 0b111, 0, 4, buf)
    assert ret == (0b111 & M32), f'state&7==7: ret={ret:#x} ждём byte[S] (ldrb)'
    assert _prd(r, S, 1)[0] == 0b111, 'state&7==7: byte[S] не должен меняться'
    # full: zero RAM (в контексте _fresh_call, SP=STACK_TOP−0x40 — tail 0x12e64 детерминирован)
    ret, r = _prod_case(0x13284, S, 0xB76, 0, 0, 4, buf)
    assert (_prd(r, S, 2), struct.unpack_from('<H', _prd(r, 0xB7C, 2))[0]) == (b'\x02\x01', 0), (
        f'zero: S={_prd(r, S, 2).hex()} u16[0xB7C]≠0')
    assert ret == 0x2501491F, f'zero: ret={ret:#x} ждём 0x2501491f'
    assert _prd(r, 0xB76, 1)[0] == 0x04, 'zero: byte[0xB76]≠4'
    assert _prd(r, S + 0x9C, 4) == buf[:4], 'zero: data memcpy'
    assert struct.unpack_from('<H', _prd(r, S + 0x9A, 2))[0] == 4, 'zero: u16[len]'
    # full: state0=0b001
    ret, r = _prod_case(0x13284, S, 0xB76, 0b001, 0, 4, buf)
    assert _prd(r, S, 2) == b'\x03\x01', f'state0=1: S={_prd(r, S, 2).hex()} ждём 03 01'
    assert _prd(r, 0xB76, 1)[0] == 0x04, f"state0=1: byte[0xB76]={_prd(r, 0xB76, 1)[0]:#x}"
    assert ret == 0x2501491F, f'state0=1: ret={ret:#x} ждём 0x2501491f'


@t(0x131FC, 'E2-b64: 0x131fc(arg0,buf,len) — 3-слотовая очередь: producer #2 (S=0x1743, стрид 152, '
            'узел 0x12c24). Те же gates (len>0x96 → ret=arg0, state&7==7 → ret=byte[S]). Эмпирика: zero-RAM → '
            'byte[S]=2, byte[S+1]=1, byte[0xB76]=1 (bit0), u16[0xB7A]=0, ret=0x78e073a0; '
            'state0=0b001 → byte[S]=3, остальное то же, ret=0x78e073a0.')
def _(run, rng):
    """Emulator test @ 0x131fc: E2-b64: 0x131fc(arg0,buf,len) — 3-слотовая очередь: producer #2 (S=0x1743, стрид 152, узел 0x12c24). Те же gates (len>0x96 → ret=arg0, state&7==7 → ret=byte[S]). Эмпирика: zero-RAM → byte[S]=2, byte[S+1]=1, byte[0xB76]=1 (bit0), u16[0xB7A]=0, ret=0x78e073a0; state0=0b001 → byte[S]=3, остальное то же, ret=0x78e073a0..
    Тест эмулятора @ 0x131fc: E2-b64: 0x131fc(arg0,buf,len) — 3-слотовая очередь: producer #2 (S=0x1743, стрид 152, узел 0x12c24). Те же gates (len>0x96 → ret=arg0, state&7==7 → ret=byte[S]). Эмпирика: zero-RAM → byte[S]=2, byte[S+1]=1, byte[0xB76]=1 (bit0), u16[0xB7A]=0, ret=0x78e073a0; state0=0b001 → byte[S]=3, остальное то же, ret=0x78e073a0..
    """
    S = 0x1743
    buf = bytes(rng.getrandbits(8) for _ in range(8))
    ret, r = _prod_case(0x131FC, S, 0xB76, 0, 0, 0x97, buf)
    assert ret == (RAM + 0x2000) & M32, f'len>0x96: ret={ret:#x}'
    assert _prd(r, S, 1)[0] == 0, 'len>0x96: byte[S] нетронут'
    ret, r = _prod_case(0x131FC, S, 0xB76, 0b111, 0, 4, buf)
    assert ret == (0b111 & M32) and _prd(r, S, 1)[0] == 0b111, 'state&7==7'
    ret, r = _prod_case(0x131FC, S, 0xB76, 0, 0, 4, buf)
    assert _prd(r, S, 2) == b'\x02\x01', f"zero: S={_prd(r, S, 2).hex()} ждём 02 01"
    assert _prd(r, 0xB76, 1)[0] == 0x01, 'zero: byte[0xB76]≠1'
    assert struct.unpack_from('<H', _prd(r, 0xB7A, 2))[0] == 0, 'zero: u16[0xB7A]≠0'
    assert ret == 0x78E073A0, f'zero: ret={ret:#x} ждём 0x78e073a0'
    assert struct.unpack_from('<H', _prd(r, S + 0x9A, 2))[0] == 4 and _prd(r, S + 0x9C, 4) == buf[:4]
    ret, r = _prod_case(0x131FC, S, 0xB76, 0b001, 0, 4, buf)
    assert _prd(r, S, 2) == b'\x03\x01' and _prd(r, 0xB76, 1)[0] == 0x01, 'state0=1'
    assert ret == 0x78E073A0, f'state0=1: ret={ret:#x}'


@t(0xBefC, 'E2-b64: 0xbefc(thr, dst) — frame-copy helper: база B=RAM+0x7C4 (2×8-байт узлов). '
            'byte[dst]=0; for i in 0..1: v=byte[B+8i+4]; if v>thr → skip; w=byte[u32[B+8i]+8]; '
            'if v+w<=thr → skip; иначе byte[dst]=1, ret=B+8i. Ничего не найдено → ret=0.')
def _(run, rng):
    """Emulator test @ 0xbefc: E2-b64: 0xbefc(thr, dst) — frame-copy helper: база B=RAM+0x7C4 (2×8-байт узлов). byte[dst]=0; for i in 0..1: v=byte[B+8i+4]; if v>thr → skip; w=byte[u32[B+8i]+8]; if v+w<=thr → skip; иначе byte[dst]=1, ret=B+8i. Ничего не найдено → ret=0..
    Тест эмулятора @ 0xbefc: E2-b64: 0xbefc(thr, dst) — frame-copy helper: база B=RAM+0x7C4 (2×8-байт узлов). byte[dst]=0; for i in 0..1: v=byte[B+8i+4]; if v>thr → skip; w=byte[u32[B+8i]+8]; if v+w<=thr → skip; иначе byte[dst]=1, ret=B+8i. Ничего не найдено → ret=0..
    """
    B = 0x7C4
    DST = 0x500
    for _ in range(30):
        v0, v1 = rng.getrandbits(8), rng.getrandbits(8)
        d0, d1 = rng.getrandbits(8), rng.getrandbits(8)
        # u32[B+8i] → указатели на blob: p+8 = RAM+DST+8i
        run.ram_write(DST, bytes(16))
        run.ram_write(DST + 8, bytes([d0]))
        run.ram_write(DST + 16, bytes([d1]))
        blob0 = RAM + DST       # p0+8 = RAM+DST+8
        blob1 = RAM + DST + 8   # p1+8 = RAM+DST+16
        run.ram_write(B, struct.pack('<IB3x', blob0, v0) + struct.pack('<IB3x', blob1, v1))
        thr = rng.getrandbits(9)
        ret, _ = run.call(0xBefC, (thr, RAM + 0x600), max_insn=2000)
        got_flag = run.ram_read(0x600, 1)[0]
        # референс
        exp_ret, exp_flag = 0, 0
        for i, (v, d) in enumerate(((v0, d0), (v1, d1))):
            if v > thr:
                continue
            if v + d <= thr:
                continue
            exp_ret, exp_flag = (RAM + B + 8 * i) & M32, 1
            break
        assert (ret, got_flag) == (exp_ret, exp_flag), (
            f'v0={v0} d0={d0} v1={v1} d1={d1} thr={thr}: ({ret:#x},{got_flag}) '
            f'≠ ({exp_ret:#x},{exp_flag})')


@t(0xF694, 'E2-b64: 0xf694() — RLE-кодировщик (12-слотовый, state byte[0xFA1], табл. u16@0xF20, '
            'bytes @0x1264). Эмпирика zero-RAM: ret=0xC; byte[0xFA1]=0; bytes[0x1264..0x1279] = '
            '01 00×11 01 01 00×6 (индекс0=1, индексы 12/13=1).')
def _(run, rng):
    # fresh-emu (shared-Run не детерминирован: результат зависит от остатков u16@0xF20/byte[0xFA1])
    """Emulator test @ 0xf694: E2-b64: 0xf694() — RLE-кодировщик (12-слотовый, state byte[0xFA1], табл. u16@0xF20, bytes @0x1264). Эмпирика zero-RAM: ret=0xC; byte[0xFA1]=0; bytes[0x1264..0x1279] = 01 00×11 01 01 00×6 (индекс0=1, индексы 12/13=1)..
    Тест эмулятора @ 0xf694: E2-b64: 0xf694() — RLE-кодировщик (12-слотовый, state byte[0xFA1], табл. u16@0xF20, bytes @0x1264). Эмпирика zero-RAM: ret=0xC; byte[0xFA1]=0; bytes[0x1264..0x1279] = 01 00×11 01 01 00×6 (индекс0=1, индексы 12/13=1)..
    """
    ret, emu = _fresh_call(0xF694, (), extra_ram=[
        (RAM + 0xFA1, bytes([0])),
        (RAM + 0x1264, bytes(0x20)),
        (RAM + 0xF20, struct.pack('<13H', *([0] * 13))),
    ], max_insn=100000)
    uc = emu.uc
    assert ret == 0xC, f'ret={ret:#x} ждём 0xc'
    assert uc.mem_read(RAM + 0xFA1, 1)[0] == 0, 'byte[0xFA1]'
    got = bytes(uc.mem_read(RAM + 0x1264, 0x16))
    exp = bytes([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0])
    assert got == exp, f'0x1264..: {got.hex()} ≠ {exp.hex()}'


@t(0x1A638, 'E2-b64: 0x1a638() — const-calc: читает 13 u32 @RAM+0x738..0x764, но ret = 0x429C0000 '
            'НЕЗАВИСИМО от содержимого (проверено на 3 разных сидах, 482 insn).')
def _(run, rng):
    """Emulator test @ 0x1a638: E2-b64: 0x1a638() — const-calc: читает 13 u32 @RAM+0x738..0x764, но ret = 0x429C0000 НЕЗАВИСИМО от содержимого (проверено на 3 разных сидах, 482 insn)..
    Тест эмулятора @ 0x1a638: E2-b64: 0x1a638() — const-calc: читает 13 u32 @RAM+0x738..0x764, но ret = 0x429C0000 НЕЗАВИСИМО от содержимого (проверено на 3 разных сидах, 482 insn)..
    """
    for _ in range(3):
        words = [rng.getrandbits(32) for _ in range(13)]
        seed = [(RAM + 0x738 + 4 * i, struct.pack('<I', w)) for i, w in enumerate(words)]
        ret, emu = _fresh_call(0x1A638, (), extra_ram=seed, max_insn=20000)
        assert ret == 0x429C0000, f'ret={ret:#x} ждём 0x429c0000 (sids={words[:3]})'


def ref_16d8e(v1, v2, xtab, ytab, grid, stride):
    """2D-билиней (u32 x/y-таблицы, byte-grid, Q8-наклоны n=8, 0x161ea).
    iA = idx2*stride + idx1; x-шаг: сосед (стрид 1) с s1; y-шаг: stride с s2; result byte."""
    n1, n2 = len(xtab), len(ytab)

    def slope(val, tab, i):
        """The slope function of the script.
        Функция slope скрипта.
        """
        num, den = val - tab[i], tab[i + 1] - tab[i]
        return (num * 256) // den & 0xFFFF

    def interp(a, b, s):
        """The interp function of the script.
        Функция interp скрипта.
        """
        if a > b:
            return (a - (((a - b) * s) >> 8)) & 0xFF
        return (a + (((b - a) * s) >> 8)) & 0xFF

    if v1 <= xtab[0]:
        idx1, s1 = 0, 0
    elif v1 >= xtab[n1 - 1]:
        idx1, s1 = n1 - 2, 0x100
    else:
        idx1 = max(i for i in range(n1) if xtab[i] <= v1)
        s1 = slope(v1, xtab, idx1)
    if v2 <= ytab[0]:
        idx2, s2 = 0, 0
    elif v2 >= ytab[n2 - 1]:
        idx2, s2 = n2 - 2, 0x100
    else:
        idx2 = max(i for i in range(n2) if ytab[i] <= v2)
        s2 = slope(v2, ytab, idx2)
    iA = idx2 * stride + idx1
    a0 = interp(grid[iA], grid[iA + 1], s1)
    a1 = interp(grid[iA + stride], grid[iA + stride + 1], s1)
    if a1 < a0:
        return (a0 - (((a0 - a1) * s2) >> 8)) & 0xFF
    return (a0 + (((a1 - a0) * s2) >> 8)) & 0xFF


@t(0x16D8E, 'E2-b64: 0x16d8e — 2D-bilinear #2 (твин 0x16bd4): u32 x/y-таблицы (r2/r3), BYTE-grid, '
            'Q8-наклоны (0x161ea n=8), clamp → slope 0x100; аргументы caller-стек (SP=entry): '
            'clamp → slope 0x100; v1/v2 — регистры r0/r1 (функция читает их из push-зон), '
            'iA = idx2*stride+idx1; ret = result (byte).')
def _(run, rng):
    """Emulator test @ 0x16d8e: E2-b64: 0x16d8e — 2D-bilinear #2 (твин 0x16bd4): u32 x/y-таблицы (r2/r3), BYTE-grid, Q8-наклоны (0x161ea n=8), clamp → slope 0x100; аргументы caller-стек (SP=entry): clamp → slope 0x100; v1/v2 — регистры r0/r1 (функция читает их из push-зон), iA = idx2*stride+idx1; ret = result (byte)..
    Тест эмулятора @ 0x16d8e: E2-b64: 0x16d8e — 2D-bilinear #2 (твин 0x16bd4): u32 x/y-таблицы (r2/r3), BYTE-grid, Q8-наклоны (0x161ea n=8), clamp → slope 0x100; аргументы caller-стек (SP=entry): clamp → slope 0x100; v1/v2 — регистры r0/r1 (функция читает их из push-зон), iA = idx2*stride+idx1; ret = result (byte)..
    """
    for _ in range(20):
        n1 = rng.randint(2, 6)
        n2 = rng.randint(2, 5)
        xtab = sorted(rng.sample(range(0, 1000), n1))
        ytab = sorted(rng.sample(range(0, 1000), n2))
        stride = rng.randint(2, 8)
        grid = [rng.getrandbits(8) for _ in range((n2 + 1) * stride + 2)]
        base = 0x700
        run.ram_write(base, struct.pack(f'<{n1}I', *xtab))
        yst = base + 0x80
        run.ram_write(yst, struct.pack(f'<{n2}I', *ytab))
        hdr = base + 0x180
        run.ram_write(hdr, struct.pack('<II', n1 - 1, n2 - 1))
        grd = base + 0x200
        run.ram_write(grd, bytes(grid))
        case = rng.getrandbits(2)
        if case == 0:
            v1 = xtab[rng.randint(0, n1 - 1)]
            v2 = ytab[rng.randint(0, n2 - 1)]
        elif case == 1:
            v1 = xtab[0] + rng.randint(0, xtab[n1 - 1] - xtab[0])
            v2 = ytab[0] + rng.randint(0, ytab[n2 - 1] - ytab[0])
        else:
            v1 = rng.randint(0, xtab[n1 - 1] + 5)
            v2 = rng.randint(0, ytab[n2 - 1] + 5)
        csp = STACK_TOP - 0x200   # SP на входе; push (52B) кладёт r0/r1 в [SP−52]/[SP−48] —
        # функция читает v1/v2 оттуда (т.е. из регистров r0/r1)
        run.ram_write(csp - RAM, struct.pack('<3I', RAM + grd, RAM + hdr, stride))
        uc = run.uc
        uc.reg_write(UC_ARM_REG_R0, v1 & M32)
        uc.reg_write(UC_ARM_REG_R1, v2 & M32)
        uc.reg_write(UC_ARM_REG_R2, RAM + base)
        uc.reg_write(UC_ARM_REG_R3, RAM + yst)
        uc.reg_write(UC_ARM_REG_SP, csp)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        run.emu.insn = 0

        def stop(uc_, a, s, usr):
            """The stop function of the script.
            Функция stop скрипта.
            """
            if not (FLASH0 <= a < FLASH0 + FW_LEN or FLASH1 <= a < FLASH1 + FW_LEN):
                uc_.emu_stop()
        sh = uc.hook_add(UC_HOOK_CODE, stop)
        try:
            uc.emu_start(0x16D8E | 1, 0, count=5000)
        except UcError:
            pass
        uc.hook_del(sh)
        r0 = uc.reg_read(UC_ARM_REG_R0) & M32
        exp = ref_16d8e(v1, v2, xtab, ytab, grid, stride)
        assert r0 == exp, f'case={case} v1={v1} v2={v2}: {r0:#x} ≠ {exp:#x}'
