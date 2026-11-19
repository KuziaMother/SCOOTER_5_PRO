# ruff: noqa: F405
"""§90 (A4): RTC/clock model — SysTick-семейство (emulator-based).

Контракты (эмуляция, verified):
- 0x19968(a, b) — u32-деление (shift-subtract).
- 0x22934(&struct{u32 rvr, u32 cvr, b flag, b ctrl}) — clock-config:
  коэффициенты через 0x19968: u32[0x1C] = base/1000, u32[0x20] = base/10000,
  u32[0x24] = base/100000 (base = u32[0x08], ÷8 если struct[8]==0; пул-значения
  — константы 0x3E8/0x2710/0x186A0, НЕ deref) + RVR/CVR/CTRL из struct
  (CTRL = (flag<<2) | ctrl).
- 0x229D4(r0, r1) — busy-wait delay r0×u32[0x24] SysTick-counts (CVR-окно
  0x1000000−target, CVR-reset 0x00FFFFFF), u16-повторы r1; ≈ 27 + r0×coeff insn.
- 0x22A0C(r0, r1) — то же с u32[0x10] (CVR-reset via OR 0x00FFFFFF).
- 0x11C84(r0) — r0==4 → SysTick_CTRL |= 4 (TICK_REF on), иначе &= ~4.
- 0x3600(ticks) — композит: bl 0x11C84 (build-quirk: bl → r0=4 → TICK_REF on),
  reload из LUT 0xC708 (zero-контекст → 0 → skip-путь), udiv, RVR/r1−1 (<
  0x1000000) + tail CVR=0/CTRL=7 (skip-путь пропускает → CTRL = 0x4).
- 0x11BAC(&out, sec) — форматтер даты/времени (§61) — TimeModel-интеграция.
- SysTickModel: 1 insn = 1 SysTick count (CVR underflow → RVR, tick++).
"""

import struct

from fv_core import *  # noqa: F401,F403

from emulator.mcu_emu import (SYST_CSR, SYST_CVR, SYST_RVR, SysTickModel, TimeModel)  # noqa: E402


def _a4_fresh(off, seeds=(), args=(), max_insn=100000):
    """The helper function (_a4_fresh).
    Вспомогательная функция (_a4_fresh).
    """
    emu = McuEmu(max_insn=max_insn)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))
    emu.hook_periph_ready()
    for addr, val in seeds:
        if isinstance(val, (bytes, bytearray)):
            uc.mem_write(RAM + addr, bytes(val))
        else:
            uc.mem_write(RAM + addr, struct.pack('<I', val))
    for i, a in enumerate(args):
        uc.reg_write(UC_ARM_REG_R0 + i, a)
    uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
    uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    lastpc = [0]
    def _hc(uc_, address, size, user):
        """The helper function (_hc).
        Вспомогательная функция (_hc).
        """
        lastpc[0] = address
    uc.hook_add(UC_HOOK_CODE, _hc)
    return emu, uc, lastpc


def _rd(uc, off, n=4):
    """The helper function (_rd).
    Вспомогательная функция (_rd).
    """
    b = bytes(uc.mem_read(RAM + off, n))
    return struct.unpack_from('<I', b, 0)[0] if n == 4 else b


def _sys(uc, off):
    """The helper function (_sys).
    Вспомогательная функция (_sys).
    """
    return struct.unpack_from('<I', bytes(uc.mem_read(0xE000E000 + off, 4)), 0)[0]


@t(0x22934, 'A4 §90: 0x22934(&struct{rvr,cvr,flag,ctrl}) — clock-config: u32[0x1C]=base/1000, u32[0x20]=base/10000, u32[0x24]=base/100000 (base=u32[0x08], ÷8 если flag==0; пул-константы НЕ deref) + RVR/CVR/CTRL из struct (CTRL=(flag<<2)|ctrl)')
def _(run, rng):
    """Emulator test @ 0x22934: A4 §90: 0x22934(&struct{rvr,cvr,flag,ctrl}) — clock-config: u32[0x1C]=base/1000, u32[0x20]=base/10000, u32[0x24]=base/100000 (base=u32[0x08], ÷8 если flag==0; пул-константы НЕ deref) + RVR/CVR/CTRL из struct (CTRL=(flag<<2)|ctrl).
    Тест эмулятора @ 0x22934: A4 §90: 0x22934(&struct{rvr,cvr,flag,ctrl}) — clock-config: u32[0x1C]=base/1000, u32[0x20]=base/10000, u32[0x24]=base/100000 (base=u32[0x08], ÷8 если flag==0; пул-константы НЕ deref) + RVR/CVR/CTRL из struct (CTRL=(flag<<2)|ctrl).
    """
    for base in (72000000, 96000000, rng.getrandbits(26)):
        for flag, ctrl in ((1, 0x05), (0, 0x03), (1, 0x01)):
            rvr, cvr = rng.getrandbits(24), rng.getrandbits(24)
            s = struct.pack('<II', rvr, cvr) + bytes([flag, ctrl])
            emu, uc, lp = _a4_fresh(0x22934, seeds=((0x500, s), (0x08, base)), args=(RAM + 0x500,), max_insn=200000)
            try:
                uc.emu_start(0x22934 | 1, 0, count=emu.max_insn)
            except Exception:
                pass
            b8 = base >> 3 if flag == 0 else base
            exp = (b8 // 1000, b8 // 10000, b8 // 100000)
            got = (_rd(uc, 0x1C), _rd(uc, 0x20), _rd(uc, 0x24))
            assert lp[0] == 0x2297E, f'lastpc={lp[0]:#x} base={base} flag={flag}'
            assert got == exp, f'коэффициенты: base={base} flag={flag} got={tuple(hex(x) for x in got)} exp={tuple(hex(x) for x in exp)}'
            assert _sys(uc, 0x14) == (rvr & 0x00FFFFFF), f'RVR={_sys(uc, 0x14):#x} exp={rvr:#x}'
            assert _sys(uc, 0x18) == (cvr & 0x00FFFFFF), f'CVR={_sys(uc, 0x18):#x} exp={cvr:#x}'
            assert _sys(uc, 0x10) == ((flag << 2) | ctrl), f'CTRL={_sys(uc, 0x10):#x} exp={((flag << 2) | ctrl):#x}'


@t(0x229D4, 'A4 §90: 0x229D4(r0, r1) — SysTick-busy-wait delay r0×u32[0x24] counts (CVR-окно 0x1000000−T, reset 0x00FFFFFF), u16-повторы r1: с SysTickModel (1 insn = 1 count) ≈ 27 + T insn (r1=1), повторы складываются')
def _(run, rng):
    """Emulator test @ 0x229d4: A4 §90: 0x229D4(r0, r1) — SysTick-busy-wait delay r0×u32[0x24] counts (CVR-окно 0x1000000−T, reset 0x00FFFFFF), u16-повторы r1: с SysTickModel (1 insn = 1 count) ≈ 27 + T insn (r1=1), повторы складываются.
    Тест эмулятора @ 0x229d4: A4 §90: 0x229D4(r0, r1) — SysTick-busy-wait delay r0×u32[0x24] counts (CVR-окно 0x1000000−T, reset 0x00FFFFFF), u16-повторы r1: с SysTickModel (1 insn = 1 count) ≈ 27 + T insn (r1=1), повторы складываются.
    """
    for coeff in (0, 50, 100, rng.getrandbits(8)):
        for r0 in (1, 5, rng.getrandbits(8)):
            tgt = coeff * r0
            emu, uc, lp = _a4_fresh(0x229D4, seeds=((0x24, coeff),), args=(r0, 1), max_insn=max(10000, tgt + 200))
            st = SysTickModel(emu)
            try:
                uc.emu_start(0x229D4 | 1, 0, count=emu.max_insn)
            except Exception:
                pass
            st.close()
            assert lp[0] == 0x229FE, f'lastpc={lp[0]:#x} coeff={coeff} r0={r0}'
            lo, hi = 20 + tgt, 40 + tgt
            assert lo <= emu.insn <= hi, f'insn={emu.insn} ∉ [{lo}, {hi}] coeff={coeff} r0={r0}'
            assert _sys(uc, 0x18) <= 0x00FFFFFF, 'CVR overflow'
    # u16-повторы r1=3: три цикла ожидания
    emu, uc, lp = _a4_fresh(0x229D4, seeds=((0x24, 100),), args=(5, 3), max_insn=200000)
    st = SysTickModel(emu)
    try:
        uc.emu_start(0x229D4 | 1, 0, count=emu.max_insn)
    except Exception:
        pass
    st.close()
    assert lp[0] == 0x229FE and 1300 <= emu.insn <= 1700, f'повторы: insn={emu.insn}'


@t(0x22A0C, 'A4 §90: 0x22A0C(r0, r1) — SysTick-busy-wait delay r0×u32[0x10] counts (CVR-reset via OR 0x00FFFFFF), u16-повторы r1: ≈ 27 + r0×coeff insn (r1=1)')
def _(run, rng):
    """Emulator test @ 0x22a0c: A4 §90: 0x22A0C(r0, r1) — SysTick-busy-wait delay r0×u32[0x10] counts (CVR-reset via OR 0x00FFFFFF), u16-повторы r1: ≈ 27 + r0×coeff insn (r1=1).
    Тест эмулятора @ 0x22a0c: A4 §90: 0x22A0C(r0, r1) — SysTick-busy-wait delay r0×u32[0x10] counts (CVR-reset via OR 0x00FFFFFF), u16-повторы r1: ≈ 27 + r0×coeff insn (r1=1).
    """
    for coeff in (0, 25, 50, rng.getrandbits(8)):
        for r0 in (2, 4, rng.getrandbits(7)):
            tgt = coeff * r0
            emu, uc, lp = _a4_fresh(0x22A0C, seeds=((0x10, coeff),), args=(r0, 1), max_insn=max(10000, tgt + 200))
            st = SysTickModel(emu)
            try:
                uc.emu_start(0x22A0C | 1, 0, count=emu.max_insn)
            except Exception:
                pass
            st.close()
            assert lp[0] == 0x22A3A, f'lastpc={lp[0]:#x} coeff={coeff} r0={r0}'
            lo, hi = 20 + tgt, 40 + tgt
            assert lo <= emu.insn <= hi, f'insn={emu.insn} ∉ [{lo}, {hi}] coeff={coeff} r0={r0}'
    # крупная задержка: 10×1000 counts
    emu, uc, lp = _a4_fresh(0x22A0C, seeds=((0x10, 1000),), args=(10, 1), max_insn=200000)
    st = SysTickModel(emu)
    try:
        uc.emu_start(0x22A0C | 1, 0, count=emu.max_insn)
    except Exception:
        pass
    st.close()
    assert lp[0] == 0x22A3A and 9950 <= emu.insn <= 10100, f'большая задержка: insn={emu.insn}'


@t(0x11C84, 'A4 §90: 0x11C84(r0) — SysTick_CTRL bit2 (TICK_REF): r0==4 → CTRL |= 4 (on), r0!=4 → CTRL &= ~4 (off)')
def _(run, rng):
    """Emulator test @ 0x11c84: A4 §90: 0x11C84(r0) — SysTick_CTRL bit2 (TICK_REF): r0==4 → CTRL |= 4 (on), r0!=4 → CTRL &= ~4 (off).
    Тест эмулятора @ 0x11c84: A4 §90: 0x11C84(r0) — SysTick_CTRL bit2 (TICK_REF): r0==4 → CTRL |= 4 (on), r0!=4 → CTRL &= ~4 (off).
    """
    for v in (4, 5, 0, 0x6A00, rng.getrandbits(24)):
        emu, uc, lp = _a4_fresh(0x11C84, args=(v,), max_insn=1000)
        try:
            uc.emu_start(0x11C84 | 1, 0, count=emu.max_insn)
        except Exception:
            pass
        c = _sys(uc, 0x10)
        if v == 4:
            assert c & 0x04, f'v={v}: CTRL={c:#x} (bit2 должен быть set)'
        else:
            assert not (c & 0x04), f'v={v}: CTRL={c:#x} (bit2 должен быть clear)'


@t(0x3600, 'A4 §90: 0x3600(ticks) — композит SysTick-периода: bl 0x11C84 (build-quirk: bl → r0=4 → TICK_REF on), reload из LUT 0xC708 (zero-контекст → 0 → skip-путь), udiv(r1, 1000), RVR=r1−1 (если < 0x1000000) + tail CVR=0/CTRL=7 (skip-путь пропускает): в изоляции CTRL ∈ {0x4, 7}, RVR < 0x1000000, функция завершается')
def _(run, rng):
    """Emulator test @ 0x3600: A4 §90: 0x3600(ticks) — композит SysTick-периода: bl 0x11C84 (build-quirk: bl → r0=4 → TICK_REF on), reload из LUT 0xC708 (zero-контекст → 0 → skip-путь), udiv(r1, 1000), RVR=r1−1 (если < 0x1000000) + tail CVR=0/CTRL=7 (skip-путь пропускает): в изоляции CTRL ∈ {0x4, 7}, RVR < 0x1000000, функция завершается.
    Тест эмулятора @ 0x3600: A4 §90: 0x3600(ticks) — композит SysTick-периода: bl 0x11C84 (build-quirk: bl → r0=4 → TICK_REF on), reload из LUT 0xC708 (zero-контекст → 0 → skip-путь), udiv(r1, 1000), RVR=r1−1 (если < 0x1000000) + tail CVR=0/CTRL=7 (skip-путь пропускает): в изоляции CTRL ∈ {0x4, 7}, RVR < 0x1000000, функция завершается.
    """
    for ticks in (73088000, 10000, 2000000000, rng.getrandbits(31)):
        emu, uc, lp = _a4_fresh(0x3600, args=(ticks,), max_insn=200000)
        try:
            uc.emu_start(0x3600 | 1, 0, count=emu.max_insn)
        except Exception:
            pass
        assert lp[0] == 0x365E, f'lastpc={lp[0]:#x} ticks={ticks}'
        c = _sys(uc, 0x10)
        rvr = _sys(uc, 0x14)
        assert c in (0x04, 0x07), f'CTRL={c:#x} ∉ {{0x4, 7}} ticks={ticks}'
        assert rvr < 0x1000000, f'RVR={rvr:#x} ≥ 0x1000000'


@t(0x11BAC, 'A4 §90: TimeModel-интеграция — format_datetime(v) (живой код 0x11BAC) == ref_datetime(v) (reference-модель) для случайных total-seconds (§61 контракт: дивизоры 31104000/2592000/86400/3600/60)')
def _(run, rng):
    """Emulator test @ 0x11bac: A4 §90: TimeModel-интеграция — format_datetime(v) (живой код 0x11BAC) == ref_datetime(v) (reference-модель) для случайных total-seconds (§61 контракт: дивизоры 31104000/2592000/86400/3600/60).
    Тест эмулятора @ 0x11bac: A4 §90: TimeModel-интеграция — format_datetime(v) (живой код 0x11BAC) == ref_datetime(v) (reference-модель) для случайных total-seconds (§61 контракт: дивизоры 31104000/2592000/86400/3600/60).
    """
    emu = McuEmu()
    tm = TimeModel(emu)
    for _ in range(25):
        v = rng.getrandbits(26)
        emu.uc.mem_write(RAM, bytes(0x20000))
        got = tm.format_datetime(v)
        exp = bytes(TimeModel.ref_datetime(v))
        assert got == exp, f'v={v}: got={list(got)} exp={list(exp)}'
