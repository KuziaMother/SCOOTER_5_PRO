# -*- coding: utf-8 -*-
"""E2-batch36..48 (5787-6173)."""
from fv_core import *  # noqa: F401,F403
from fv_core import _fresh_call, _intercept  # noqa: F401
# --- E2-batch36: 0x0d39d delegate family (gated channel-service) ---
# Контракт (вериф bl-intercept): u32@(RAM+0x8C) — status-слово; если bit `channel` set,
# функция вызывает 0x0d39d(channel); если 0x0d39d вернёт 1 -> сбросить bit `channel`
# в другом status-u32 (по pool). gate-бит == channel. Вериф: bl достигнут с r0==channel.
_OD39D_FAM = {0x0D6E4: 0xE, 0x0D734: 0xD, 0x0D75C: 0x10,
              0x0D784: 0x11, 0x0D7D4: 0xF, 0x0D850: 0x12}


def _mk_od39d(addr, ch):
    def _test(run, rng):
        from emulator.mcu_emu import RAM as _R
        import struct as _st
        cap, _emu = _intercept(addr, 0x0D39D,
                               extra_ram=[(_R + 0x8C, _st.pack('<I', 1 << ch))])
        assert cap.get('r0') == ch, \
            f'0x{addr:05x}: r0={cap.get("r0"):#x} want 0x{ch:x}'
    return _test


for _addr, _ch in sorted(_OD39D_FAM.items()):
    t(_addr, f'E2-b36: 0x{_addr:05x} -> 0x0d39d(channel=0x{_ch:x}) [gate=bit {_ch} of u32@RAM+0x8C; bl-intercept]')(_mk_od39d(_addr, _ch))


# --- E2-batch37: 0x0d46d delegate family (гated channel-service, брат 0x0d39d) ---
_OD46D_FAM = {0x0D70C: 0x9, 0x0D7AC: 0xB, 0x0D7FC: 0xC, 0x0D824: 0xA}


def _mk_od46d(addr, ch):
    def _test(run, rng):
        from emulator.mcu_emu import RAM as _R
        import struct as _st
        cap, _emu = _intercept(addr, 0x0D46D,
                               extra_ram=[(_R + 0x8C, _st.pack('<I', 1 << ch))])
        assert cap.get('r0') == ch, \
            f'0x{addr:05x}: r0={cap.get("r0"):#x} want 0x{ch:x}'
    return _test


for _addr, _ch in sorted(_OD46D_FAM.items()):
    t(_addr, f'E2-b37: 0x{_addr:05x} -> 0x0d46d(channel=0x{_ch:x}) [gate=bit {_ch} of u32@RAM+0x8C; bl-intercept]')(_mk_od46d(_addr, _ch))


# --- E2-batch38: тонкие single-bl делегаторы (passthrough + fixed-arg) ---
# Контракт: функция = чистая обёртка `bl helper` (passthrough r0/r1/r2/r3) либо
# задаёт фикс. аргумент и вызывает helper. Вериф через bl-intercept (стоп на входе helper).
_PT_DELEG = {0x01DEC: 0x029E9, 0x02D14: 0x09679, 0x04E28: 0x05001, 0x04E30: 0x04FC1,
             0x09A18: 0x099F1, 0x0CE68: 0x03169, 0x10780: 0x10789, 0x10A20: 0x112BD,
             0x11CAC: 0x04C15, 0x12FD0: 0x12B51, 0x12FD8: 0x12D91, 0x1A5F2: 0x1BFA1}
_FX_DELEG = {0x0395C: (0x0D299, 0), 0x03966: (0x0D299, 1), 0x03B20: (0x01BDD, 0x9A)}


def _mk_pt(daddr, haddr):
    def _test(run, rng):
        cap, _emu = _intercept(daddr, haddr, args=(0x1234, 0x5678, 0xABCD, 0))
        assert cap.get('r0') == 0x1234 and cap.get('r1') == 0x5678, \
            f'0x{daddr:05x}: {cap}'
    return _test


def _mk_fx(daddr, haddr, val):
    def _test(run, rng):
        cap, _emu = _intercept(daddr, haddr, arg=0)
        assert cap.get('r0') == val, \
            f'0x{daddr:05x}: r0={cap.get("r0"):#x} want {val:#x}'
    return _test


for _d, _h in sorted(_PT_DELEG.items()):
    t(_d, f'E2-b38: 0x{_d:05x} passthrough -> 0x{_h:05x} [bl-intercept r0/r1]')(_mk_pt(_d, _h))
for _d, (_h, _v) in sorted(_FX_DELEG.items()):
    t(_d, f'E2-b38: 0x{_d:05x} -> 0x{_h:05x}({hex(_v)}) [fixed-arg bl-intercept]')(_mk_fx(_d, _h, _v))


# --- E2-batch39: тонкие делегаторы 2 (passthrough / fixed-arg / shuffle / r3-fix) ---
_PT2 = {0x05B8C: 0x04DE1, 0x11668: 0x10E5D, 0x11888: 0x10F19, 0x07ED4: 0x061E5,
        0x082F0: 0x0833D, 0x08348: 0x0833D, 0x08468: 0x0833D}
_FX2 = {0x110F0: (0x05B8D, 0)}
_SHUF = {0x1A5E6: 0x1A7AD, 0x1A628: 0x1A5F3, 0x21C64: 0x1A5E5}  # helper r1 = orig r0
_R3FIX = {0x0C200: 0x09F65}  # helper r3=1, r0 passthrough


def _mk_pt2(daddr, haddr):
    def _test(run, rng):
        cap, _emu = _intercept(daddr, haddr, args=(0x1234, 0, 0, 0))
        assert cap.get('r0') == 0x1234, f'0x{daddr:05x}: {cap}'
    return _test


def _mk_fx2(daddr, haddr, val):
    def _test(run, rng):
        cap, _emu = _intercept(daddr, haddr, arg=0)
        assert cap.get('r0') == val, f'0x{daddr:05x}: r0={cap.get("r0"):#x} want {val:#x}'
    return _test


def _mk_shuf(daddr, haddr):
    def _test(run, rng):
        cap, _emu = _intercept(daddr, haddr, args=(0x1111, 0, 0, 0))
        assert cap.get('r1') == 0x1111, f'0x{daddr:05x}: r1={cap.get("r1"):#x} want 0x1111'
    return _test


def _mk_r3fix(daddr, haddr):
    def _test(run, rng):
        cap, _emu = _intercept(daddr, haddr, args=(0x1234, 0, 0, 0))
        assert cap.get('r0') == 0x1234 and cap.get('r3') == 1, f'0x{daddr:05x}: {cap}'
    return _test


for _d, _h in sorted(_PT2.items()):
    t(_d, f'E2-b39: 0x{_d:05x} passthrough -> 0x{_h:05x} [bl-intercept r0]')(_mk_pt2(_d, _h))
for _d, (_h, _v) in sorted(_FX2.items()):
    t(_d, f'E2-b39: 0x{_d:05x} -> 0x{_h:05x}({hex(_v)}) [fixed-arg]')(_mk_fx2(_d, _h, _v))
for _d, _h in sorted(_SHUF.items()):
    t(_d, f'E2-b39: 0x{_d:05x} -> 0x{_h:05x}(pool_ptr, orig_r0) [r1=orig_r0]')(_mk_shuf(_d, _h))
for _d, _h in sorted(_R3FIX.items()):
    t(_d, f'E2-b39: 0x{_d:05x} -> 0x{_h:05x}(r0, r3=1) [r3-fix]')(_mk_r3fix(_d, _h))


# --- E2-batch40: толстые fixed-point обёртки -> 0x1a0f9 / 0x1a185 ---
# 0x19fbe(a)  -> 0x1a0f9(a, 0, 0, 0x96)
# 0x19fae(a,b)-> 0x1a0f9(a+b, 0, b<<31, 0x96)   (b<<31 = 0x80000000 если b<0)
# 0x19fcc(x)  -> 0x1a185(abs(x), 0, 0, 0)       (abs: sign/pool на стек, регистры чистые)
# (0x19ab0 отложен: 50-инст fixed-point normalize, нет ручной модели)


def _t_19fbe(run, rng):
    for a in (5, 123456, -7):
        cap, _ = _intercept(0x19FBE, 0x1A0F9, args=(a & 0xFFFFFFFF, 0, 0, 0))
        assert cap.get('r0') == (a & 0xFFFFFFFF) and cap.get('r1') == 0 \
            and cap.get('r2') == 0 and cap.get('r3') == 0x96, f'a={a}: {cap}'


def _t_19fae(run, rng):
    for a, b in ((100, 200), (-50, 30), (100, -5), (0x40000000, 0x10000000)):
        cap, _ = _intercept(0x19FAE, 0x1A0F9, args=(a & 0xFFFFFFFF, b & 0xFFFFFFFF, 0, 0))
        exp_r0 = (a + b) & 0xFFFFFFFF
        exp_r2 = (b << 31) & 0xFFFFFFFF
        assert cap.get('r0') == exp_r0 and cap.get('r1') == 0 \
            and cap.get('r2') == exp_r2 and cap.get('r3') == 0x96, f'a={a},b={b}: {cap}'


def _t_19fcc(run, rng):
    for x in (5, -5, 0, 123456, -123456):
        cap, _ = _intercept(0x19FCC, 0x1A185, args=(x & 0xFFFFFFFF, 0, 0, 0))
        assert cap.get('r0') == (abs(x) & 0xFFFFFFFF) and cap.get('r1') == 0 \
            and cap.get('r2') == 0 and cap.get('r3') == 0, f'x={x}: {cap}'


t(0x19FBE, 'E2-b40: 0x19fbe(a) -> 0x1a0f9(a,0,0,0x96) [fixed-point wrapper]')(_t_19fbe)
t(0x19FAE, 'E2-b40: 0x19fae(a,b) -> 0x1a0f9(a+b,0,b<<31,0x96) [fixed-point wrapper]')(_t_19fae)
t(0x19FCC, 'E2-b40: 0x19fcc(x) -> 0x1a185(abs(x),0,0,0) [abs wrapper]')(_t_19fcc)


# --- E2-batch41: periph-config init 0x0cb10 ---
# 0x0cb10 = init таймера/периферии (регистры 0x400028xx): последовательность записи
#   [0x40002824] = 0xca -> 0x53 -> 0xff (финал 0xff); [0x40002808] = base|r0.
# Детерминированное (не зависит от state): финальный константный [0x40002824]==0xff.


def _t_0cb10(run, rng):
    import struct as _st
    r0, emu = _fresh_call(0x0CB10, args=(0,))
    a = _st.unpack('<I', bytes(emu.uc.mem_read(0x40002824, 4)))[0]
    assert a == 0xFF, f'[0x40002824]={a:#x} want 0xff'


t(0x0CB10, 'E2-b41: 0x0cb10 periph-init -> [0x40002824]=0xff (seq ca->53->ff)')(_t_0cb10)


# --- E2-batch42: stateful делегаторы (gate / fixed-ptr / stack-arg) ---
def _t_0e6ec(run, rng):
    from emulator.mcu_emu import RAM as _R
    cap, _ = _intercept(0x0E6EC, 0x0F14D, extra_ram=[(_R + 0x13C9, b'\x01')])
    assert cap.get('r0') == 1, f'gate=1: {cap}'
    cap2, _ = _intercept(0x0E6EC, 0x0F14D, extra_ram=[(_R + 0x13C9, b'\x00')])
    assert not cap2, f'gate=0 should not reach bl: {cap2}'


def _t_123c0(run, rng):
    cap, _ = _intercept(0x123C0, 0x0B855, arg=0)
    assert cap.get('r0') == 0x20000DD8, f'{cap}'


def _t_139ac(run, rng):
    import struct as _st
    cap, emu = _intercept(0x139AC, 0x13C79, arg=0)
    r0v = cap.get('r0')
    val = _st.unpack('<I', bytes(emu.uc.mem_read(r0v, 4)))[0]
    assert val == 3, f'[r0]={val:#x} want 3'


t(0x0E6EC, 'E2-b42: 0x0e6ec gated -> 0xf14d(gate) [gate=byte@0x13c9==1]')(_t_0e6ec)
t(0x123C0, 'E2-b42: 0x123c0 -> 0xb855(0x20000dd8) [fixed struct-ptr]')(_t_123c0)
t(0x139AC, 'E2-b42: 0x139ac -> 0x13c79(sp) [writes 3 to stack, passes ptr]')(_t_139ac)


# --- E2-batch43: последние тонкие делегаторы (класс исчерпан) ---
def _t_02a5c(run, rng):
    cap, _ = _intercept(0x02A5C, 0x01BDD, arg=0)
    assert cap.get('r0') == 0x9A, f'{cap}'


def _t_08afc(run, rng):
    for arg in (0x1234, 7):
        cap, _ = _intercept(0x08AFC, 0x0218D, args=(arg, 0, 0, 0))
        assert cap.get('r0') == arg, f'arg={arg}: {cap}'


t(0x02A5C, 'E2-b43: 0x02a5c -> 0x1bdd(0x9a) [query bit, returns res&1]')(_t_02a5c)
t(0x08AFC, 'E2-b43: 0x08afc -> 0x218d(r0) [passthrough, stores result]')(_t_08afc)


# --- E2-batch44: setters (RAM/periph) + init-группы (2-3 bl) ---
def _t_087de(run, rng):
    import struct as _st
    from emulator.mcu_emu import RAM as _R
    scratch = _R + 0x1000
    for val in (0x12345678, 0xDEADBEEF, 0):
        r0, emu = _fresh_call(0x087DE, args=(scratch, val))
        got = _st.unpack('<I', bytes(emu.uc.mem_read(scratch + 0x18, 4)))[0]
        assert got == val, f'val={val:#x}: {got:#x}'


def _t_1f1c0(run, rng):
    import struct as _st
    sent = 0xC0FFEE11
    r0, emu = _fresh_call(0x1F1C0, args=(sent,))
    got = _st.unpack('<I', bytes(emu.uc.mem_read(0x40004804, 4)))[0]
    assert got == sent, f'{got:#x}'


def _t_211ec(run, rng):
    import struct as _st
    sent = 0xC0FFEE11
    r0, emu = _fresh_call(0x211EC, args=(sent,))
    got = _st.unpack('<I', bytes(emu.uc.mem_read(0x40004C04, 4)))[0]
    assert got == sent, f'{got:#x}'


def _mk_init_group(fn, last):
    def _t(run, rng, _fn=fn, _last=last):
        cap, _ = _intercept(_fn, _last, arg=0)
        assert cap, f'0x{_fn:x} did not reach last bl 0x{_last:x}'
    return _t


t(0x087DE, 'E2-b44: 0x087de [r0+0x18]=r1 [RAM field setter]')(_t_087de)
t(0x1F1C0, 'E2-b44: 0x1f1c0 [USART3 0x40004804]=r0 [periph setter]')(_t_1f1c0)
t(0x211EC, 'E2-b44: 0x211ec [0x40004c04]=r0 [periph setter]')(_t_211ec)
t(0x01ABC, 'E2-b44: 0x01abc init-group (bl 0x1a69 -> 0x19f5)')(_mk_init_group(0x01ABC, 0x19F5))
t(0x01CEA, 'E2-b44: 0x01cea init-group (bl 0x1fe1 -> 0x20d9)')(_mk_init_group(0x01CEA, 0x20D9))
t(0x036F4, 'E2-b44: 0x036f4 init-group (bl 0x10901 -> 0x3b01)')(_mk_init_group(0x036F4, 0x3B01))
t(0x09482, 'E2-b44: 0x09482 init-group (bl 0x9135 -> 0x9481)')(_mk_init_group(0x09482, 0x9481))
t(0x09F64, 'E2-b44: 0x09f64 init-group (bl 0x9b45 -> 0x9f71)')(_mk_init_group(0x09F64, 0x9F71))
# NOTE: 0x0bf4c (bl 0xd879->0xddc5) и 0x0ced0 (bl 0x310d->0x3151->0x31dd) НЕ доходят
# до последнего bl в изоляции: первый sub-init не возвращается чисто при нулевом RAM.
# Классифицированы как «не изолируются» (см. PROGRAM.md).


# --- E2-batch45: init-group 0x09b44 + protocol-parser magic-gate 0x0df10 ---
t(0x09B44, 'E2-b45: 0x09b44 init-group (5 bl: 0x9ddd->...->0x9db5)')(_mk_init_group(0x09B44, 0x9DB5))


def _t_0df10(run, rng):
    import struct as _st
    from emulator.mcu_emu import RAM as _R
    buf = _R + 0x5000
    # 0x0df10 = protocol parser: magic-gate byte[struct+2]==0xaa.
    # Ветка magic-mismatch (детерминированная, вериф): возвращает byte[struct+2].
    for b2 in (0x55, 0x01, 0xFF):
        data = _st.pack('<H', 10) + bytes([b2, 0, 0]) + bytes(20)
        r0, emu = _fresh_call(0x0DF10, args=(buf,), extra_ram=[(buf, data)])
        assert r0 == b2, f'b2={b2:#x}: r0={r0:#x} want {b2:#x}'


t(0x0DF10, 'E2-b45: 0x0df10 protocol-parser magic-gate [s+2]==0xaa (mismatch->ret byte[2])')(_t_0df10)


# --- E2-batch46: чистый compute 0x19f7c (gate-контракт первого возврата) ---
# 0x19f7c(r0,r1,r2) -> (r0_out, r1_out). Первый возврат (вериф 206/206 sweep):
#   r0_out = r0, если (signed)r2 > 0; иначе 0.
# Второй возврат r1_out = сложная multi-word операция от (r1,r2) — не моделируется чисто
# (см. PROGRAM.md); тестируем только детерминированный gate по первому возврату.

def _t_19f7c(run, rng):
    cases = [
        (1, 0, 5), (5, 0, 3), (3, 0x1234, 0x1000),   # r2>0 -> r0_out=r0
        (1, 0, 0), (1, 0, -5), (5, 7, 0x80000000),   # r2<=0 -> r0_out=0
        (0, 0, 5), (0, 0x80000000, 0),               # r0==0 -> r0_out=0
    ]
    for r0, r1, r2 in cases:
        rr, _emu = _fresh_call(0x19F7C, args=(r0, r1, r2 & 0xFFFFFFFF))
        s2 = r2 if r2 < 0x80000000 else r2 - 0x100000000
        exp = r0 if s2 > 0 else 0
        assert rr == exp, f'r0={r0} r1={r1:#x} r2={r2:#x}: got {rr:#x} want {exp:#x}'


t(0x19F7C, 'E2-b46: 0x19f7c compute gate: r0_out = r0 if (signed)r2>0 else 0')(_t_19f7c)


# --- E2-batch47: тонкие делегаторы + init-группы (цепочки 0xc625/0x8589/0x5971/0x59a5) ---
def _t_05874(run, rng):
    cap, _emu = _intercept(0x05874, 0x597D)
    assert cap.get('r0') == 1, f'r0={cap.get("r0"):#x} want 1'

def _t_058f6(run, rng):
    cap, _emu = _intercept(0x058F6, 0x597D)
    assert cap.get('r0') == 0x10, f'r0={cap.get("r0"):#x} want 0x10'

def _t_030a6(run, rng):
    import struct as _st
    cap, emu = _intercept(0x030A6, 0x59A5, max_insn=30000)
    assert cap, 'last bl 0x59a5 not reached'
    raw = bytes(emu.uc.mem_read(cap['r0'], 8))
    u32, b4, b5, b6 = _st.unpack('<I', raw[0:4])[0], raw[4], raw[5], raw[6]
    assert (u32, b4, b5, b6) == (0x800, 0, 8, 0), f'struct={u32:#x},{b4},{b5},{b6}'

def _t_032f4(run, rng):
    import struct as _st
    cap, emu = _intercept(0x032F4, 0x59A5, max_insn=30000)
    assert cap, 'last bl 0x59a5 not reached'
    raw = bytes(emu.uc.mem_read(cap['r0'], 8))
    u32, b4, b5, b6 = _st.unpack('<I', raw[0:4])[0], raw[4], raw[5], raw[6]
    assert (u32, b4, b5, b6) == (0x80, 0, 12, 0), f'struct={u32:#x},{b4},{b5},{b6}'

def _t_03168(run, rng):
    cap, _emu = _intercept(0x03168, 0x5971, max_insn=30000)
    assert cap, 'bl 0x5971 not reached (gate 0xcc69 failed)'
    assert cap.get('r0') == 0x100000, f'r0={cap.get("r0"):#x} want 0x100000'

t(0x05874, 'E2-b47: 0x05874 delegate -> bl 0x597d(r0=1)')(_t_05874)
t(0x058F6, 'E2-b47: 0x058f6 delegate -> bl 0x597d(r0=0x10)')(_t_058f6)
t(0x030A6, 'E2-b47: 0x030a6 init-group -> bl 0x59a5(sp) [sp]={0x800,0,8,0}')(_t_030a6)
t(0x032F4, 'E2-b47: 0x032f4 init-group -> bl 0x59a5(sp) [sp]={0x80,0,12,0}')(_t_032f4)
t(0x03168, 'E2-b47: 0x03168 init-group (gate 0xcc69) -> bl 0x5971(r0=0x100000)')(_t_03168)


# --- E2-batch48: одиночные тонкие делегаторы (скан по частоте bl-целей) ---
def _t_5dbc(run, rng):
    cap, _emu = _intercept(0x5DBC, 0x2D5D, max_insn=30000)
    assert cap.get('r0') == 0xAAAA, f'r0={cap.get("r0"):#x} want 0xaaaa'

def _t_10770(run, rng):
    cap, _emu = _intercept(0x10770, 0xC625, max_insn=30000)
    assert cap.get('r0') == 1, f'r0={cap.get("r0"):#x} want 1'

def _t_128c8(run, rng):
    cap, _emu = _intercept(0x128C8, 0x50B1, max_insn=30000)
    assert cap.get('r0') == 0x20000044 and cap.get('r1') == 2, \
        f'r0={cap.get("r0"):#x} r1={cap.get("r1")} want (0x20000044, 2)'

def _t_12a64(run, rng):
    cap, _emu = _intercept(0x12A64, 0x4C85, max_insn=30000)
    assert cap.get('r0') == 0 and cap.get('r1') == 1, f'r0={cap.get("r0")} r1={cap.get("r1")}'

def _t_13c5c(run, rng):
    cap, _emu = _intercept(0x13C5C, 0x11D7, max_insn=30000)
    assert cap.get('r1') == 0x4B, f'r1={cap.get("r1"):#x} want 0x4b'

t(0x5DBC, 'E2-b48: 0x5dbc delegate -> bl 0x2d5d(r0=0xaaaa) [IR TX cfg]')(_t_5dbc)
t(0x10770, 'E2-b48: 0x10770 delegate -> bl 0xc625(r0=1)')(_t_10770)
t(0x128C8, 'E2-b48: 0x128c8 delegate -> bl 0x50b1(r0=RAM+0x44, r1=2)')(_t_128c8)
t(0x12A64, 'E2-b48: 0x12a64 delegate -> bl 0x4c85(r0=0, r1=1)')(_t_12a64)
t(0x13C5C, 'E2-b48: 0x13c5c delegate -> bl 0x11d7(r1=0x4b)')(_t_13c5c)


# --- E2-batch49: stateful single-base gate + оставшиеся делегаторы ---
def _t_2d5c(run, rng):
    cap, _emu = _intercept(0x2D5C, 0x332C, max_insn=30000)
    assert cap.get('r1') == 0x1A, f'r1={cap.get("r1"):#x} want 0x1a'

def _t_02a6c(run, rng):
    cap, _emu = _intercept(0x02A6C, 0x4E50, max_insn=30000)
    assert cap, 'bl 0x4e50 not reached (init-group incomplete)'

def _t_0178c(run, rng):
    cap, _emu = _intercept(0x178C, 0x182B, max_insn=30000)
    assert cap, 'bl 0x182b not reached'
    cap2, _ = _intercept(0x178C, 0x1815, max_insn=30000)
    assert cap2, 'bl 0x1815 not reached'

t(0x2D5C, 'E2-b49: 0x2d5c delegate -> bl 0x332c(r1=0x1a)')(_t_2d5c)
t(0x02A6C, 'E2-b49: 0x02a6c init-group -> bl 0x4e50 (complete)')(_t_02a6c)
t(0x178C, 'E2-b49: 0x0178c init-group -> bl 0x182b + bl 0x1815 (r1=0x1)')(_t_0178c)
