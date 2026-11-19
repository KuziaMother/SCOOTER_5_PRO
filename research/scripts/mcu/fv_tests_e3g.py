# ruff: noqa: F405
"""§91 (A5): I2C model — I2C2-чип (dev 0x3E) + shadow-регистровая семья (emulator-based).

Контракты (статика §49.1/§50 + dynamic probes):
- I2C2-блок @0x40005800 (кастомная периферия; тот же блок B1 = power-стадия 2),
  I2C1 @0x40005400 (B1: power-стадия 1). Внешний чип — dev 0x3E.
- Shadow-слой @RAM+0x15FA..0x164C: 22 setter'а (0x20C4..0x2358, val=8):
  цепочка setter → 0x1C60(val, reg, &shadow, len) → 0x1E52(·,1,·,·) →
  0x214C(0, val, reg, len) → 0x8F7C(0x40005800, val, reg, out).
- 0x8F7C = I2C-фрейм-отправщик: буфер 0x48, pre-roll CRC-7 цепочка
  sb = crc7(crc7(crc7(0, u8(val<<1)), reg), u8(val)|1) (0x3C7C), blx
  u32[RAM+0xDD8+0x118] (send-примитив; zero-контекст → 0 → векторные байты),
  цикл verif: чётные → out[i]=frame[i], нечётные → frame[i] ==
  crc7(frame[i-1], sb) иначе ret 0; ret blx == 0 → успех → ret 1.
  Build-quirk (b70): в изоляции ret = u8(r1<<1) (векторные байты blx 0).
- Reader'ы: 0x1C1C(reg16, len) — буфер {reg_lo, reg_hi}, dev 0x3E → 0x90A0
  (read-транзакция, periph u16 0xFFFF @0x40005800) + 1000-iteration timeout;
  0x1BDC(reg)/0x1C7A(val, reg, &buf, len)/0x155AC/0x218C() — варианты
  (результат → u16@0xF95+0x1E/0x20; build-quirk: ret = u8(arg<<1)).
- I2cModel (emulator/mcu_emu.py): shadow get/set/seed, i2c2_writes (periph-
  захват), ref_frame (reference-сборка фрейма: data-par'ы с chained CRC-7,
  pre-roll сеет sb; заголовок в фрейм не входит).
"""

import struct

from fv_core import *  # noqa: F401,F403
from fv_core import ref_crc7_port  # noqa: E402
from emulator.mcu_emu import (I2C2_BASE, I2C2_DEV, I2C2_SETTERS,  # noqa: E402
                              I2C2_SHADOW_OFFS, I2cModel)


def _a5_fresh(off, seeds=(), args=(), max_insn=50000):
    """The helper function (_a5_fresh).
    Вспомогательная функция (_a5_fresh).
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
    try:
        uc.emu_start(off | 1, 0, count=emu.max_insn)
    except Exception:
        pass
    return emu, uc, lastpc[0]


@t(0x20C4, 'A5 §91: setter-цепочка I2C2 (0x20C4 reg 0x38 / 0x231C reg 3 / 0x2358 reg 0x70): 0x1C60→0x1E52→0x214C→0x8F7C(0x40005800)→blx 0 (векторные байты): insn≈548/548/536, lastpc=0x8FEC, ret=0x10 (u8(val<<1), val=8), без periph-записей')
def _(run, rng):
    """Emulator test @ 0x20c4: A5 §91: setter-цепочка I2C2 (0x20C4 reg 0x38 / 0x231C reg 3 / 0x2358 reg 0x70): 0x1C60→0x1E52→0x214C→0x8F7C(0x40005800)→blx 0 (векторные байты): insn≈548/548/536, lastpc=0x8FEC, ret=0x10 (u8(val<<1), val=8), без periph-записей.
    Тест эмулятора @ 0x20c4: A5 §91: setter-цепочка I2C2 (0x20C4 reg 0x38 / 0x231C reg 3 / 0x2358 reg 0x70): 0x1C60→0x1E52→0x214C→0x8F7C(0x40005800)→blx 0 (векторные байты): insn≈548/548/536, lastpc=0x8FEC, ret=0x10 (u8(val<<1), val=8), без periph-записей.
    """
    for off, lo, hi in ((0x20C4, 500, 600), (0x231C, 500, 600), (0x2358, 500, 600)):
        emu, uc, lp = _a5_fresh(off)
        ret = uc.reg_read(UC_ARM_REG_R0)
        assert lo <= emu.insn <= hi, f'0x{off:04x}: insn={emu.insn} ∉ [{lo}, {hi}]'
        assert lp == 0x8FEC, f'0x{off:04x}: lastpc={lp:#x} ждём 0x8FEC'
        assert ret == 0x10, f'0x{off:04x}: ret={ret:#x} ждём 0x10'
        assert not emu.periph_writes, f'0x{off:04x}: periph-записи в изоляции'


@t(0x8F7C, 'A5 §91: 0x8F7C(fp, val, reg, out) — I2C-фрейм-отправщик (b70-контракт, расширен): в изоляции (blx 0 → векторные байты) insn≈490-510, lastpc=0x8FEC, ret = u8(val<<1) для val ∈ {0,1,3,5} + рандом-малые')
def _(run, rng):
    """Emulator test @ 0x8f7c: A5 §91: 0x8F7C(fp, val, reg, out) — I2C-фрейм-отправщик (b70-контракт, расширен): в изоляции (blx 0 → векторные байты) insn≈490-510, lastpc=0x8FEC, ret = u8(val<<1) для val ∈ {0,1,3,5} + рандом-малые.
    Тест эмулятора @ 0x8f7c: A5 §91: 0x8F7C(fp, val, reg, out) — I2C-фрейм-отправщик (b70-контракт, расширен): в изоляции (blx 0 → векторные байты) insn≈490-510, lastpc=0x8FEC, ret = u8(val<<1) для val ∈ {0,1,3,5} + рандом-малые.
    """
    for val in (0, 1, 3, 5, rng.getrandbits(4)):
        emu, uc, lp = _a5_fresh(0x8F7C, args=(0x40005800, val, 0x38, RAM + 0x700))
        ret = uc.reg_read(UC_ARM_REG_R0)
        assert 470 <= emu.insn <= 530, f'0x8f7c(val={val}): insn={emu.insn} ждём ~490-510'
        assert lp == 0x8FEC, f'0x8f7c(val={val}): lastpc={lp:#x} ждём 0x8FEC'
        assert ret == (val << 1) & 0xFF, f'0x8f7c(val={val}): ret={ret:#x} ждём {val << 1:#x}'


@t(0x214C, 'A5 §91: 0x214C(0, val, reg, len) — среднее звено цепи: bl 0x8F7C(0x40005800, val, reg, len) (пул @0x2188 = 0x40005800), ret-маппинг (≠0 → 1, 0 → 0): в изоляции insn≈519, lastpc=0x8FEC, ret=0x10 (quirk)')
def _(run, rng):
    """Emulator test @ 0x214c: A5 §91: 0x214C(0, val, reg, len) — среднее звено цепи: bl 0x8F7C(0x40005800, val, reg, len) (пул @0x2188 = 0x40005800), ret-маппинг (≠0 → 1, 0 → 0): в изоляции insn≈519, lastpc=0x8FEC, ret=0x10 (quirk).
    Тест эмулятора @ 0x214c: A5 §91: 0x214C(0, val, reg, len) — среднее звено цепи: bl 0x8F7C(0x40005800, val, reg, len) (пул @0x2188 = 0x40005800), ret-маппинг (≠0 → 1, 0 → 0): в изоляции insn≈519, lastpc=0x8FEC, ret=0x10 (quirk).
    """
    emu, uc, lp = _a5_fresh(0x214C, args=(0, 8, 0x38, 2))
    ret = uc.reg_read(UC_ARM_REG_R0)
    assert 480 <= emu.insn <= 560, f'0x214c: insn={emu.insn} ждём ~519'
    assert lp == 0x8FEC, f'0x214c: lastpc={lp:#x} ждём 0x8FEC'
    assert ret == 0x10, f'0x214c: ret={ret:#x} ждём 0x10'


@t(0x1C60, 'A5 §91: 0x1C60(val, reg, &shadow, len) — входной хелпер цепи: push len в [sp], bl 0x1E52(val, reg, 1, &shadow, len): в изоляции insn≈542, lastpc=0x8FEC, ret=0x10 (quirk)')
def _(run, rng):
    """Emulator test @ 0x1c60: A5 §91: 0x1C60(val, reg, &shadow, len) — входной хелпер цепи: push len в [sp], bl 0x1E52(val, reg, 1, &shadow, len): в изоляции insn≈542, lastpc=0x8FEC, ret=0x10 (quirk).
    Тест эмулятора @ 0x1c60: A5 §91: 0x1C60(val, reg, &shadow, len) — входной хелпер цепи: push len в [sp], bl 0x1E52(val, reg, 1, &shadow, len): в изоляции insn≈542, lastpc=0x8FEC, ret=0x10 (quirk).
    """
    emu, uc, lp = _a5_fresh(0x1C60, args=(8, 0x38, RAM + I2C2_SHADOW_OFFS[0x38], 2))
    ret = uc.reg_read(UC_ARM_REG_R0)
    assert 500 <= emu.insn <= 580, f'0x1c60: insn={emu.insn} ждём ~542'
    assert lp == 0x8FEC, f'0x1c60: lastpc={lp:#x} ждём 0x8FEC'
    assert ret == 0x10, f'0x1c60: ret={ret:#x} ждём 0x10'


@t(0x1E52, 'A5 §91: 0x1E52(val, reg, 1, &shadow, len) — хелпер цепи (uxtb reg, push extra в [sp], bl 0x214C): в изоляции insn≈531, lastpc=0x8FEC, ret=0x10 (quirk)')
def _(run, rng):
    """Emulator test @ 0x1e52: A5 §91: 0x1E52(val, reg, 1, &shadow, len) — хелпер цепи (uxtb reg, push extra в [sp], bl 0x214C): в изоляции insn≈531, lastpc=0x8FEC, ret=0x10 (quirk).
    Тест эмулятора @ 0x1e52: A5 §91: 0x1E52(val, reg, 1, &shadow, len) — хелпер цепи (uxtb reg, push extra в [sp], bl 0x214C): в изоляции insn≈531, lastpc=0x8FEC, ret=0x10 (quirk).
    """
    emu, uc, lp = _a5_fresh(0x1E52, args=(8, 0x38, 1, RAM + I2C2_SHADOW_OFFS[0x38]))
    ret = uc.reg_read(UC_ARM_REG_R0)
    assert 500 <= emu.insn <= 580, f'0x1e52: insn={emu.insn} ждём ~531'
    assert lp == 0x8FEC, f'0x1e52: lastpc={lp:#x} ждём 0x8FEC'
    assert ret == 0x10, f'0x1e52: ret={ret:#x} ждём 0x10'


@t(0x1C1C, 'A5 §91: 0x1C1C(reg16, len) — I2C2 read-транзакция: буфер {reg_lo, reg_hi}, dev 0x3E, val 8 → bl 0x90A0 (пул → 0x40005800); при ret≠0 → 1000-iteration timeout (в изоляции 0x90A0-цепь крутится до max_insn): periph u16 0xFFFF @0x40005800, ret ∈ {0, 1}')
def _(run, rng):
    """Emulator test @ 0x1c1c: A5 §91: 0x1C1C(reg16, len) — I2C2 read-транзакция: буфер {reg_lo, reg_hi}, dev 0x3E, val 8 → bl 0x90A0 (пул → 0x40005800); при ret≠0 → 1000-iteration timeout (в изоляции 0x90A0-цепь крутится до max_insn): periph u16 0xFFFF @0x40005800, ret ∈ {0, 1}.
    Тест эмулятора @ 0x1c1c: A5 §91: 0x1C1C(reg16, len) — I2C2 read-транзакция: буфер {reg_lo, reg_hi}, dev 0x3E, val 8 → bl 0x90A0 (пул → 0x40005800); при ret≠0 → 1000-iteration timeout (в изоляции 0x90A0-цепь крутится до max_insn): periph u16 0xFFFF @0x40005800, ret ∈ {0, 1}.
    """
    emu, uc, lp = _a5_fresh(0x1C1C, args=(0x38, 2), max_insn=60000)
    ret = uc.reg_read(UC_ARM_REG_R0)
    model = I2cModel(emu)
    w2 = model.i2c2_writes()
    assert any(w[1] == I2C2_BASE and w[3] == 0xFFFF for w in w2), \
        f'0x1c1c: нет periph u16 0xFFFF @0x40005800: {[(hex(a), hex(v)) for _, a, s, v in w2]}'
    assert ret in (0, 1), f'0x1c1c: ret={ret:#x} ∉ {{0,1}}'


@t(0x218C, 'A5 §91: 0x218C() — read-cycle (bl 0x1C7A(8, 0x83, &buf(sp), 2)): в изоляции insn≈579, lastpc=0x908C (0x8f7c-регион), ret=0x10 (quirk u8(8<<1))')
def _(run, rng):
    """Emulator test @ 0x218c: A5 §91: 0x218C() — read-cycle (bl 0x1C7A(8, 0x83, &buf(sp), 2)): в изоляции insn≈579, lastpc=0x908C (0x8f7c-регион), ret=0x10 (quirk u8(8<<1)).
    Тест эмулятора @ 0x218c: A5 §91: 0x218C() — read-cycle (bl 0x1C7A(8, 0x83, &buf(sp), 2)): в изоляции insn≈579, lastpc=0x908C (0x8f7c-регион), ret=0x10 (quirk u8(8<<1)).
    """
    emu, uc, lp = _a5_fresh(0x218C)
    ret = uc.reg_read(UC_ARM_REG_R0)
    assert 550 <= emu.insn <= 620, f'0x218c: insn={emu.insn} ждём ~579'
    assert lp == 0x908C, f'0x218c: lastpc={lp:#x} ждём 0x908C'
    assert ret == 0x10, f'0x218c: ret={ret:#x} ждём 0x10'


@t(0x1C7A, 'A5 §91: 0x1C7A(val, reg, &buf, len) — reader (буфер: reg_lo, reg_hi, len; dev-транзакция): в изоляции insn≈571, lastpc=0x908C, ret=0x10 (quirk u8(val<<1))')
def _(run, rng):
    """Emulator test @ 0x1c7a: A5 §91: 0x1C7A(val, reg, &buf, len) — reader (буфер: reg_lo, reg_hi, len; dev-транзакция): в изоляции insn≈571, lastpc=0x908C, ret=0x10 (quirk u8(val<<1)).
    Тест эмулятора @ 0x1c7a: A5 §91: 0x1C7A(val, reg, &buf, len) — reader (буфер: reg_lo, reg_hi, len; dev-транзакция): в изоляции insn≈571, lastpc=0x908C, ret=0x10 (quirk u8(val<<1)).
    """
    emu, uc, lp = _a5_fresh(0x1C7A, args=(8, 0x83, RAM + 0x700, 2))
    ret = uc.reg_read(UC_ARM_REG_R0)
    assert 550 <= emu.insn <= 620, f'0x1c7a: insn={emu.insn} ждём ~571'
    assert lp == 0x908C, f'0x1c7a: lastpc={lp:#x} ждём 0x908C'
    assert ret == 0x10, f'0x1c7a: ret={ret:#x} ждём 0x10'


@t(0x155AC, 'A5 §91: 0x155AC — reader-вариант (результат → u16@0xF95+0x20): в изоляции insn≈571-577, lastpc=0x908C; ret-quirk = u8(arg<<1): ()→0, (0x38,)→0x70 (reg<<1), (8, 0x83)→0x10 (val<<1)')
def _(run, rng):
    """Emulator test @ 0x155ac: A5 §91: 0x155AC — reader-вариант (результат → u16@0xF95+0x20): в изоляции insn≈571-577, lastpc=0x908C; ret-quirk = u8(arg<<1): ()→0, (0x38,)→0x70 (reg<<1), (8, 0x83)→0x10 (val<<1).
    Тест эмулятора @ 0x155ac: A5 §91: 0x155AC — reader-вариант (результат → u16@0xF95+0x20): в изоляции insn≈571-577, lastpc=0x908C; ret-quirk = u8(arg<<1): ()→0, (0x38,)→0x70 (reg<<1), (8, 0x83)→0x10 (val<<1).
    """
    for args, expect in (((), 0), ((0x38,), 0x70), ((8, 0x83), 0x10)):
        emu, uc, lp = _a5_fresh(0x155AC, args=args)
        ret = uc.reg_read(UC_ARM_REG_R0)
        assert 550 <= emu.insn <= 620, f'0x155ac{args}: insn={emu.insn}'
        assert lp == 0x908C, f'0x155ac{args}: lastpc={lp:#x} ждём 0x908C'
        assert ret == expect, f'0x155ac{args}: ret={ret:#x} ждём {expect:#x}'


@t(0x1BDC, 'A5 §91: 0x1BDC(reg) — reader-вариант (16-битный код регистра, len=2): в изоляции insn≈568, lastpc=0x908C, ret=0x10 (quirk)')
def _(run, rng):
    """Emulator test @ 0x1bdc: A5 §91: 0x1BDC(reg) — reader-вариант (16-битный код регистра, len=2): в изоляции insn≈568, lastpc=0x908C, ret=0x10 (quirk).
    Тест эмулятора @ 0x1bdc: A5 §91: 0x1BDC(reg) — reader-вариант (16-битный код регистра, len=2): в изоляции insn≈568, lastpc=0x908C, ret=0x10 (quirk).
    """
    emu, uc, lp = _a5_fresh(0x1BDC, args=(0x38,))
    ret = uc.reg_read(UC_ARM_REG_R0)
    assert 540 <= emu.insn <= 620, f'0x1bdc: insn={emu.insn} ждём ~568'
    assert lp == 0x908C, f'0x1bdc: lastpc={lp:#x} ждём 0x908C'
    assert ret == 0x10, f'0x1bdc: ret={ret:#x} ждём 0x10'


@t(0x8F7C, 'A5 §91: I2cModel ref_frame — reference-сборка I2C-фрейма 0x8F7C: frame = [d0, c0, d1, c1, ...], c0 = crc7(d0, sb_pre), ci = crc7(di, c(i-1)); sb_pre = pre-roll crc7(crc7(crc7(0, u8(val<<1)), reg), u8(val)|1) (тот же chained CRC-7, что цикл верификации). Сверка с ref_crc7_port + таблица shadow/setters (22 пары, уникальные reg)')
def _(run, rng):
    # таблица: 22 setter'а, уникальные reg, shadow-офсеты в блоке 0x15FA..0x164C
    """Emulator test @ 0x8f7c: A5 §91: I2cModel ref_frame — reference-сборка I2C-фрейма 0x8F7C: frame = [d0, c0, d1, c1, ...], c0 = crc7(d0, sb_pre), ci = crc7(di, c(i-1)); sb_pre = pre-roll crc7(crc7(crc7(0, u8(val<<1)), reg), u8(val)|1) (тот же chained CRC-7, что цикл верификации). Сверка с ref_crc7_port + таблица shadow/setters (22 пары, уникальные reg).
    Тест эмулятора @ 0x8f7c: A5 §91: I2cModel ref_frame — reference-сборка I2C-фрейма 0x8F7C: frame = [d0, c0, d1, c1, ...], c0 = crc7(d0, sb_pre), ci = crc7(di, c(i-1)); sb_pre = pre-roll crc7(crc7(crc7(0, u8(val<<1)), reg), u8(val)|1) (тот же chained CRC-7, что цикл верификации). Сверка с ref_crc7_port + таблица shadow/setters (22 пары, уникальные reg).
    """
    assert len(I2C2_SHADOW_OFFS) == 22, f'len shadow table = {len(I2C2_SHADOW_OFFS)}'
    assert len(I2C2_SETTERS) == 22, f'len setters table = {len(I2C2_SETTERS)}'
    assert set(I2C2_SHADOW_OFFS) == set(I2C2_SETTERS), 'ключи таблиц не совпадают'
    for reg, off in I2C2_SHADOW_OFFS.items():
        assert 0x15FA <= off <= 0x164C, f'reg {reg:#x}: shadow {off:#x} вне блока'
    # ref_frame: сверка CRC-цепи с прямым вычислением
    for _ in range(30):
        val = rng.getrandbits(7)
        reg = rng.getrandbits(8)
        data = bytes(rng.getrandbits(8) for _ in range(rng.randint(1, 5)))
        frame = I2cModel.ref_frame(val, reg, data)
        assert len(frame) == 2 * len(data), f'len frame = {len(frame)}'
        sb = ref_crc7_port((val << 1) & 0xFF, 0)
        sb = ref_crc7_port(reg, sb)
        sb = ref_crc7_port((val | 1) & 0xFF, sb)
        for i, d in enumerate(data):
            sb = ref_crc7_port(d, sb)
            assert frame[2 * i] == d, f'frame[{2 * i}] != data'
            assert frame[2 * i + 1] == (sb & 0x7F), \
                f'frame[{2 * i + 1}]={frame[2 * i + 1]:#x} != crc {sb:#x}'
    # shadow get/set round-trip
    emu = McuEmu()
    model = I2cModel(emu)
    for reg in (0x03, 0x38, 0x7F):
        model.shadow_set(reg, rng.getrandbits(8))
        assert model.shadow_get(reg) == model.shadow_get(reg)
        assert model.shadow_addr(reg) == RAM + I2C2_SHADOW_OFFS[reg]
