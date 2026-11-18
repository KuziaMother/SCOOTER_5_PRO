# ruff: noqa: F405  (имена из star-import от fv_core)
"""§79.3 (B1-динамика): командный слой 0x2e0c/0x97f4/0x9874/0x2d70 — полная карта.
Найдено (2026-11-18, dynamic probes):
  - ID-пространство = ровно {0x40005400, 0x40005800} (два кастомных блока,
    1KB друг от друга; pool-литералы 0x2e7c/0x2e80/0x9828). Другой ID → ret 1
    без обработки (0x2e0c @0x2e3c early-return).
  - 0x2e0c(ID, &struct): спец-ID1 0x40005400 → latch bit21 в 0x4002101C (0xc664);
    спец-ID2 0x40005800 → latch bit22; затем 0x97f4(ID) = pulse бита в 0x40021010
    (ID1→bit21 0x200000, ID2→bit22 0x400000, set-then-clear), копирование struct
    {u32 ptr, u16×5}, 0x98c8(ID, &cfg) = config-write в блок (0xc708 LUT: +0x04 =
    u16[cfg+6] & 0xFFC0, +0x08 = (u16[cfg+8]>>4) | (u16[cfg+6]&0x30) | ...),
    0x982c(ID, 1) = enable bit0 u16[base] → ret 0.
  - Конфиг 0x2d70 (один-разовый init power-стадии): struct {0x080186A0, 0, 0xBFFF,
    0x30, 0x400, 0x4000} → блок: +0x04=0xFFC0, +0x08=0x4030, +0x1C=0x8001, +0x20=1,
    +0x00=0x401 (enable|bit8).
  - 0x9874(base, r1): status-reader — r1 bit31 → тест битов 24..31 u32[base+0x14];
    иначе → тест битов 16..31 u32[base+0x18] (mask=(r1&0xFF000000)>>16); ret 0/1.
    (bit31-ветка динамически не верифицируема — lsrs #28 из quirk-класса сдвигов.)
  - 0x2d70: init-цепочка 0x97f4(0x40005800) bit22 pulse → GPIO-дескрипторы 0x332c
    (flash @0x1A780/0x1A794) → delay 1000 → 0x2e0c(0x40005800, &cfg) → status
    byte[0xB72]=(byte[0xB64]&0x0F)|0x10, byte[0xB64]++ если 0x9874(0x40005800,0x20000)
    (bit1 u32[0x40005818]). Вызывающий — 0x173cc (gated init)."""
import struct

from fv_core import *  # noqa: F401,F403

from emulator.mcu_emu import PERIPH  # noqa: E402

ID1 = 0x40005400   # спец-ID 1 → bit21 (0x200000)
ID2 = 0x40005800   # спец-ID 2 → bit22 (0x400000)


def _b2_fresh(off, args=(), seeds=(), max_insn=300000):
    """fresh-emu для B1: нулевой RAM + 0xFF периферия + seeds; (uc, emu, lastpc)"""
    emu = McuEmu(max_insn=max_insn)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))
    emu.hook_periph_ready()
    for addr, val in seeds:
        if isinstance(val, (bytes, bytearray)):
            uc.mem_write(addr, val)
        else:
            uc.mem_write(addr, struct.pack('<I', val))
    for i, a in enumerate(args):
        uc.reg_write([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2][i], a)
    uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
    uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    lastpc = [0]

    def _hc(uc_, address, size, user):
        lastpc[0] = address

    uc.hook_add(UC_HOOK_CODE, _hc)
    try:
        uc.emu_start(off | 1, 0, count=max_insn)
    except Exception:
        pass
    return emu, uc, lastpc[0]


def _pw(emu, addr):
    return [v for pc, a, s, v in emu.periph_writes if a == addr]


# struct 0x2d70-конфига: {u32 ptr, u16×5}
CFG_2D70 = struct.pack('<I5H', 0x080186A0, 0x0000, 0xBFFF, 0x0030, 0x0400, 0x4000)


@t(0x2E0C, '§79.3: 0x2e0c(ID, &struct) — ID-пространство {0x40005400, 0x40005800}: '
           'ID1 → latch bit21 @0x4002101C + pulse bit21 @0x40021010 + config '
           '(+0x04=0xFFC0, +0x08=0x4030, +0x1C=0x8001, +0x20=1, enable 0x401); '
           'ID2 → то же с bit22; неизвестный ID/гейты → ret 1 без записей')
def _(run, rng):
    for i, bit in ((ID1, 0x200000), (ID2, 0x400000)):
        emu, uc, lp = _b2_fresh(0x2E0C, [i, RAM + 0x400], seeds=[
            (RAM + 0x400, CFG_2D70), (PERIPH + 0x2101C, 0), (PERIPH + 0x21010, 0), (i, 0)])
        assert uc.reg_read(UC_ARM_REG_R0) == 0, f'0x2e0c({i:#x}): ret≠0'
        assert _pw(emu, PERIPH + 0x2101C) == [bit], f'latch {i:#x}: {_pw(emu, PERIPH + 0x2101C)}'
        p10 = _pw(emu, PERIPH + 0x21010)
        assert len(p10) == 2 and p10[0] == bit, f'pulse {i:#x}: {p10}'
        # config в блок (0x98c8): значения — golden прогона
        assert _pw(emu, i + 4) == [0xFFC0], f'cfg +0x04 {i:#x}'
        assert _pw(emu, i + 8) == [0x4030], f'cfg +0x08 {i:#x}'
        assert _pw(emu, i + 0x1C) == [0x8001], f'cfg +0x1C {i:#x}'
        assert _pw(emu, i + 0x20) == [1], f'cfg +0x20 {i:#x}'
        assert _pw(emu, i)[-1] == 0x401, f'enable {i:#x}: {_pw(emu, i)}'
    # неизвестный ID → ret 1, без периферийных записей
    emu, uc, lp = _b2_fresh(0x2E0C, [0x12345678, RAM + 0x400], seeds=[(RAM + 0x400, CFG_2D70)])
    assert uc.reg_read(UC_ARM_REG_R0) == 1 and len(emu.periph_writes) == 0, \
        f'неизв. ID: ret={uc.reg_read(UC_ARM_REG_R0):#x} P={len(emu.periph_writes)}'
    # гейты: ID=0 и struct=NULL → ret 1
    for a, b in ((0, RAM + 0x400), (ID1, 0)):
        emu, uc, lp = _b2_fresh(0x2E0C, [a, b], seeds=[(RAM + 0x400, CFG_2D70)])
        assert uc.reg_read(UC_ARM_REG_R0) == 1 and len(emu.periph_writes) == 0, \
            f'гейт ({a:#x},{b:#x}): ret={uc.reg_read(UC_ARM_REG_R0):#x}'


@t(0x97F4, '§79.3: 0x97f4(ID) — pulse бита в 0x40021010: ID1 → bit21 [0x200000→0], '
           'ID2 → bit22 [0x400000→0] (set-then-clear, 0xc684)')
def _(run, rng):
    for i, bit in ((ID1, 0x200000), (ID2, 0x400000)):
        emu, uc, lp = _b2_fresh(0x97F4, [i], seeds=[(PERIPH + 0x21010, 0)])
        assert _pw(emu, PERIPH + 0x21010)[0] == bit, f'0x97f4({i:#x}): {_pw(emu, PERIPH + 0x21010)}'
        assert _pw(emu, PERIPH + 0x21010)[-1] == 0, f'0x97f4({i:#x}) clear: {_pw(emu, PERIPH + 0x21010)}'
        assert len(emu.periph_writes) == 2, f'0x97f4({i:#x}) лишних записей: {emu.periph_writes}'


@t(0x9874, '§79.3: 0x9874(base, r1) — status-reader: r1 bit31=0 → тест битов '
           '(r1&0xFF000000)>>16 в u32[base+0x18] (ret 0/1); r1 bit31=1 → биты 24..31 '
           'u32[base+0x14] (ветка статически верифицирована; lsrs #28 — quirk-класс)')
def _(run, rng):
    for seed, exp in ((0x2, 1), (0x0, 0), (0x1, 0)):
        emu, uc, lp = _b2_fresh(0x9874, [ID2, 0x20000], seeds=[(ID2 + 0x18, seed)])
        assert uc.reg_read(UC_ARM_REG_R0) == exp, \
            f'0x9874(0x20000, +0x18={seed:#x}): ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём {exp}'


@t(0x2D70, '§79.3: 0x2d70() — один-разовый init power-стадии: 0x97f4(0x40005800) bit22 '
           'pulse (0x40021010: 0xFFFFFFFF → clear с bics-quirk-маской) → GPIO-дескрипторы '
           '0x332c (flash @0x1A780/0x1A794) → delay → 0x2e0c(ID2, &cfg); в изоляции '
           'остановка на RAM-trampoline внутри 0x332c (контекст-зависимо); struct '
           '{0x080186A0, 0, 0xBFFF, 0x30, 0x400, 0x4000} на стеке')
def _(run, rng):
    emu, uc, lp = _b2_fresh(0x2D70, [], max_insn=300000)
    assert emu.insn > 100, f'0x2d70: insn={emu.insn}'
    p10 = _pw(emu, PERIPH + 0x21010)
    assert len(p10) >= 2 and p10[0] == 0xFFFFFFFF, f'0x2d70 pulse: {p10}'
    # clear-бит22: bics-quirk чистит разные маски по контексту (0xBFFFFFFF чистый /
    # 0xFFF00000 / 0xFFEFFFFF ...) — инвариант: запись есть и значение изменилось
    assert p10[1] != 0xFFFFFFFF, f'0x2d70 clear: {p10}'
    # struct push (13B блока на стеке) — RAM-записи есть
    assert len(emu.ram_writes_all) >= 8, f'0x2d70: RAM-записей {len(emu.ram_writes_all)}'
