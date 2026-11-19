# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-b80: I2C1-инит 0x1a31c (166 insn, ret=0x40012400, 0x40012414/18=FF +
0x48000C04=0); флаг-кейс 0x1ce38 (flag byte[0x2000026A]: fresh 15 insn
ret=0x2000169A / flag 48 insn ret=0xFFFF7FFF, 0x40012C54=0xFFFF7FFF);
константы-указатели 0x1de0c (410 insn, ret=0x430C0000) / 0x1df84 (374 insn,
ret=0x42F80000); 6×FF-пальтер 0x1e658 (39 insn, 0x40004C40=FF×6,
ret=0x40004C40); RCC 0x221a4 (64 insn, 0x40022004=0xFF000001,
0x40022000=0xFFFFFFF1); тривиал 0x225f4 (6 insn, ret=1); спин 0x22824
(insn>=50000, 0x40021000=0xFFEFFFFF, ret=0x40000000); чистые 0x1337c
(2922 insn) / 0x14f50 (~242 insn) / 0x1c34c (1159 insn, ret=2) / 0x21c18
(310 insn) / 0x21b52 (4 insn)."""
import struct

from fv_core import *  # noqa: F401,F403

from unicorn import UcError, UC_HOOK_CODE  # noqa: E402
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,  # noqa: E402
                               UC_ARM_REG_SP, UC_ARM_REG_LR)


def _fresh_probe(off, seeds=(), args=(), max_insn=60000):
    """Fresh-emu: чистый RAM, 0xFF PERIPH, seeds (int->u32 / bytes), args r0..r3;
    возвращает (uc, emu, lastpc)."""
    emu = McuEmu(max_insn=max_insn)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))
    emu.hook_periph_ready()
    for addr, val in seeds:
        if isinstance(val, (bytes, bytearray)):
            uc.mem_write(addr, val)
        else:
            uc.mem_write(addr, struct.pack('<I', val))
    regs = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)
    for i, a in enumerate(args):
        uc.reg_write(regs[i], a)
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
    except UcError:
        pass
    return uc, emu, lastpc[0]


def _r(uc, off, size=1):
    """The helper function (_r).
    Вспомогательная функция (_r).
    """
    return int.from_bytes(bytes(uc.mem_read(RAM + off, size)), 'little')


def _p(uc, addr, size=4):
    """The helper function (_p).
    Вспомогательная функция (_p).
    """
    return int.from_bytes(bytes(uc.mem_read(addr, size)), 'little')


def _pw(emu, addr):
    """Последовательность значений записей в periph-адрес."""
    return [v for _, a, _, v in emu.periph_writes if a == addr]


@t(0x1A31C, 'E2-b80: 0x1a31c() — I2C1-инит (166 insn, ret=0x40012400, 3 записи): '
            '0x40012414=0xFFFFFFFF; 0x48000C04=0; 0x40012418=0xFFFFFFFF. fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x1a31c: E2-b80: 0x1a31c() — I2C1-инит (166 insn, ret=0x40012400, 3 записи): 0x40012414=0xFFFFFFFF; 0x48000C04=0; 0x40012418=0xFFFFFFFF. fresh-emu golden..
    Тест эмулятора @ 0x1a31c: E2-b80: 0x1a31c() — I2C1-инит (166 insn, ret=0x40012400, 3 записи): 0x40012414=0xFFFFFFFF; 0x48000C04=0; 0x40012418=0xFFFFFFFF. fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x1A31C)
    assert len(emu.periph_writes) == 3, \
        f'0x1a31c: P={len(emu.periph_writes)} ждём 3'
    assert _pw(emu, 0x40012414) == [0xFFFFFFFF], \
        f"0x1a31c: 40012414={_pw(emu, 0x40012414)} ждём [FF]"
    assert _pw(emu, 0x48000C04) == [0x0], \
        f"0x1a31c: 48000C04={_pw(emu, 0x48000C04)} ждём [0]"
    assert _pw(emu, 0x40012418) == [0xFFFFFFFF], \
        f"0x1a31c: 40012418={_pw(emu, 0x40012418)} ждём [FF]"
    assert uc.reg_read(UC_ARM_REG_R0) == 0x40012400, \
        f'0x1a31c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x40012400'
    assert emu.insn == 166, f'0x1a31c: insn={emu.insn} ждём 166'


@t(0x1CE38, 'E2-b80: 0x1ce38() — флаг-кейс (флаг byte[0x2000026A]): fresh → 15 insn '
            'ret=0x2000169A (stack) без записей; flag=1 → 48 insn ret=0xFFFF7FFF, '
            '0x40012C54=0xFFFF7FFF. 2 кейса.')
def _(run, rng):
    """Emulator test @ 0x1ce38: E2-b80: 0x1ce38() — флаг-кейс (флаг byte[0x2000026A]): fresh → 15 insn ret=0x2000169A (stack) без записей; flag=1 → 48 insn ret=0xFFFF7FFF, 0x40012C54=0xFFFF7FFF. 2 кейса..
    Тест эмулятора @ 0x1ce38: E2-b80: 0x1ce38() — флаг-кейс (флаг byte[0x2000026A]): fresh → 15 insn ret=0x2000169A (stack) без записей; flag=1 → 48 insn ret=0xFFFF7FFF, 0x40012C54=0xFFFF7FFF. 2 кейса..
    """
    uc, emu, lp = _fresh_probe(0x1CE38)
    assert len(emu.periph_writes) == 0, \
        f'0x1ce38 fresh: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x2000169A, \
        f'0x1ce38 fresh: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x2000169A'
    assert emu.insn == 15, f'0x1ce38 fresh: insn={emu.insn} ждём 15'
    uc, emu, lp = _fresh_probe(0x1CE38, seeds=[(0x2000026A, 1)])
    assert _pw(emu, 0x40012C54) == [0xFFFF7FFF], \
        f"0x1ce38 flag=1: 40012C54={_pw(emu, 0x40012C54)} ждём [0xFFFF7FFF]"
    assert len(emu.periph_writes) == 1, \
        f'0x1ce38 flag=1: P={len(emu.periph_writes)} ждём 1'
    assert uc.reg_read(UC_ARM_REG_R0) == 0xFFFF7FFF, \
        f'0x1ce38 flag=1: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0xFFFF7FFF'
    assert emu.insn == 48, f'0x1ce38 flag=1: insn={emu.insn} ждём 48'


@t(0x1DE0C, 'E2-b80: 0x1de0c() — константный указатель (410 insn, ret=0x430C0000, '
            'tail в unmapped): без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x1de0c: E2-b80: 0x1de0c() — константный указатель (410 insn, ret=0x430C0000, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    Тест эмулятора @ 0x1de0c: E2-b80: 0x1de0c() — константный указатель (410 insn, ret=0x430C0000, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x1DE0C)
    assert len(emu.periph_writes) == 0, \
        f'0x1de0c: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x430C0000, \
        f'0x1de0c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x430C0000'
    assert emu.insn == 410, f'0x1de0c: insn={emu.insn} ждём 410'


@t(0x1DF84, 'E2-b80: 0x1df84() — константный указатель (374 insn, ret=0x42F80000, '
            'tail в unmapped): без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x1df84: E2-b80: 0x1df84() — константный указатель (374 insn, ret=0x42F80000, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    Тест эмулятора @ 0x1df84: E2-b80: 0x1df84() — константный указатель (374 insn, ret=0x42F80000, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x1DF84)
    assert len(emu.periph_writes) == 0, \
        f'0x1df84: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x42F80000, \
        f'0x1df84: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x42F80000'
    assert emu.insn == 374, f'0x1df84: insn={emu.insn} ждём 374'


@t(0x1E658, 'E2-b80: 0x1e658() — 6×FF-пульс (39 insn, ret=0x40004C40): '
            '0x40004C40=0xFFFFFFFF ×6. fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x1e658: E2-b80: 0x1e658() — 6×FF-пульс (39 insn, ret=0x40004C40): 0x40004C40=0xFFFFFFFF ×6. fresh-emu golden..
    Тест эмулятора @ 0x1e658: E2-b80: 0x1e658() — 6×FF-пульс (39 insn, ret=0x40004C40): 0x40004C40=0xFFFFFFFF ×6. fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x1E658)
    assert _pw(emu, 0x40004C40) == [0xFFFFFFFF] * 6, \
        f"0x1e658: 40004C40={_pw(emu, 0x40004C40)} ждём FF×6"
    assert len(emu.periph_writes) == 6, \
        f'0x1e658: P={len(emu.periph_writes)} ждём 6'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x40004C40, \
        f'0x1e658: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x40004C40'
    assert emu.insn == 39, f'0x1e658: insn={emu.insn} ждём 39'


@t(0x221A4, 'E2-b80: 0x221a4() — RCC/AHB2 (64 insn, ret=0, 2 записи): '
            '0x40022004=0xFF000001; 0x40022000=0xFFFFFFF1. fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x221a4: E2-b80: 0x221a4() — RCC/AHB2 (64 insn, ret=0, 2 записи): 0x40022004=0xFF000001; 0x40022000=0xFFFFFFF1. fresh-emu golden..
    Тест эмулятора @ 0x221a4: E2-b80: 0x221a4() — RCC/AHB2 (64 insn, ret=0, 2 записи): 0x40022004=0xFF000001; 0x40022000=0xFFFFFFF1. fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x221A4)
    assert _pw(emu, 0x40022004) == [0xFF000001], \
        f"0x221a4: 40022004={_pw(emu, 0x40022004)} ждём [0xFF000001]"
    assert _pw(emu, 0x40022000) == [0xFFFFFFF1], \
        f"0x221a4: 40022000={_pw(emu, 0x40022000)} ждём [0xFFFFFFF1]"
    assert len(emu.periph_writes) == 2, \
        f'0x221a4: P={len(emu.periph_writes)} ждём 2'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x221a4: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 64, f'0x221a4: insn={emu.insn} ждём 64'


@t(0x225F4, 'E2-b80: 0x225f4() — тривиальный (6 insn, ret=1, tail в unmapped): без '
            'побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x225f4: E2-b80: 0x225f4() — тривиальный (6 insn, ret=1, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    Тест эмулятора @ 0x225f4: E2-b80: 0x225f4() — тривиальный (6 insn, ret=1, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x225F4)
    assert len(emu.periph_writes) == 0, \
        f'0x225f4: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 1, \
        f'0x225f4: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 1'
    assert emu.insn == 6, f'0x225f4: insn={emu.insn} ждём 6'


@t(0x22824, 'E2-b80: 0x22824() — спин (insn>=50000, ret=0x40000000, 1 запись): '
            '0x40021000=0xFFEFFFFF до начала спина. fresh-emu golden.')
def _(run, rng):
    """Emulator test @ 0x22824: E2-b80: 0x22824() — спин (insn>=50000, ret=0x40000000, 1 запись): 0x40021000=0xFFEFFFFF до начала спина. fresh-emu golden..
    Тест эмулятора @ 0x22824: E2-b80: 0x22824() — спин (insn>=50000, ret=0x40000000, 1 запись): 0x40021000=0xFFEFFFFF до начала спина. fresh-emu golden..
    """
    uc, emu, lp = _fresh_probe(0x22824)
    assert emu.insn >= 50000, f'0x22824: insn={emu.insn} ждём спин (>=50000)'
    assert _pw(emu, 0x40021000) == [0xFFEFFFFF], \
        f"0x22824: 40021000={_pw(emu, 0x40021000)} ждём [0xFFEFFFFF]"
    assert len(emu.periph_writes) == 1, \
        f'0x22824: P={len(emu.periph_writes)} ждём 1'
    assert uc.reg_read(UC_ARM_REG_R0) == 0x40000000, \
        f'0x22824: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x40000000'


@t(0x1337C, 'E2-b80: 0x1337c() — чистый вычислительный блок (2922 insn, ret=0, '
            'tail в unmapped): без периферийных/RAM-побочных эффектов.')
def _(run, rng):
    """Emulator test @ 0x1337c: E2-b80: 0x1337c() — чистый вычислительный блок (2922 insn, ret=0, tail в unmapped): без периферийных/RAM-побочных эффектов..
    Тест эмулятора @ 0x1337c: E2-b80: 0x1337c() — чистый вычислительный блок (2922 insn, ret=0, tail в unmapped): без периферийных/RAM-побочных эффектов..
    """
    uc, emu, lp = _fresh_probe(0x1337C)
    assert len(emu.periph_writes) == 0, \
        f'0x1337c: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x1337c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 2922, f'0x1337c: insn={emu.insn} ждём 2922'


@t(0x14F50, 'E2-b80: 0x14f50() — чистый блок (~242 insn, ret=0, tail в unmapped): '
            'без побочных эффектов; insn плавающий (200..300).')
def _(run, rng):
    """Emulator test @ 0x14f50: E2-b80: 0x14f50() — чистый блок (~242 insn, ret=0, tail в unmapped): без побочных эффектов; insn плавающий (200..300)..
    Тест эмулятора @ 0x14f50: E2-b80: 0x14f50() — чистый блок (~242 insn, ret=0, tail в unmapped): без побочных эффектов; insn плавающий (200..300)..
    """
    uc, emu, lp = _fresh_probe(0x14F50)
    assert len(emu.periph_writes) == 0, \
        f'0x14f50: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x14f50: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert 200 <= emu.insn <= 300, \
        f'0x14f50: insn={emu.insn} ждём 200..300'


@t(0x1C34C, 'E2-b80: 0x1c34c() — чистый блок (1159 insn, ret=2, tail в unmapped): '
            'без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x1c34c: E2-b80: 0x1c34c() — чистый блок (1159 insn, ret=2, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    Тест эмулятора @ 0x1c34c: E2-b80: 0x1c34c() — чистый блок (1159 insn, ret=2, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x1C34C)
    assert len(emu.periph_writes) == 0, \
        f'0x1c34c: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 2, \
        f'0x1c34c: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 2'
    assert emu.insn == 1159, f'0x1c34c: insn={emu.insn} ждём 1159'


@t(0x21C18, 'E2-b80: 0x21c18() — чистый блок (310 insn, ret=0, tail в unmapped): '
            'без побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x21c18: E2-b80: 0x21c18() — чистый блок (310 insn, ret=0, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    Тест эмулятора @ 0x21c18: E2-b80: 0x21c18() — чистый блок (310 insn, ret=0, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x21C18)
    assert len(emu.periph_writes) == 0, \
        f'0x21c18: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x21c18: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 310, f'0x21c18: insn={emu.insn} ждём 310'


@t(0x21B52, 'E2-b80: 0x21b52() — тривиальный (4 insn, ret=0, tail в unmapped): без '
            'побочных эффектов. smoke+ret+insn golden.')
def _(run, rng):
    """Emulator test @ 0x21b52: E2-b80: 0x21b52() — тривиальный (4 insn, ret=0, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    Тест эмулятора @ 0x21b52: E2-b80: 0x21b52() — тривиальный (4 insn, ret=0, tail в unmapped): без побочных эффектов. smoke+ret+insn golden..
    """
    uc, emu, lp = _fresh_probe(0x21B52)
    assert len(emu.periph_writes) == 0, \
        f'0x21b52: P={len(emu.periph_writes)} ждём 0'
    assert uc.reg_read(UC_ARM_REG_R0) == 0, \
        f'0x21b52: ret={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0'
    assert emu.insn == 4, f'0x21b52: insn={emu.insn} ждём 4'
