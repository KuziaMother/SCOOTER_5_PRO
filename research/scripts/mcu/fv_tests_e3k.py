# ruff: noqa: F405
"""§95 (Phase ③) + §97 (Phase ④): cold-boot — векторная таблица + startup +
C-старт + main + task-цепь (без железа).

BootHarness (emulator/mcu_emu.py): старт с reset-вектора.
**Phase ③ (§95):** векторная таблица @0x1000 ([0]=SP_INIT, [1]=reset|1, [22]=
FOC-ISR 0x7875); цепочка reset 0x315c → stage1 0xcd0c → TRAMP1 pop@0x3166 (pc=
RAM[SP+12]) → stage2 0x3168 → TRAMP2 pop@0x31c6; детерминированно до TRAMP2
(insn=6314, final_pc=0xcd78).
**Phase ④ (§97):** initial stack [SP+12] = runtime-данные (SWD-потолок; zero-RAM →
стоп на TRAMP1, insn=3138). Реальная цепочка входа: [SP+12]=0x1149 → **C-старт
0x1148** (SP из литерала 0x1158; bl 0x14C4 конструктор-тейбл @0x1AD28: 2×16Б
{a0,a1,a2,fn}, desc1.fn=0x20000040 код в RAM (live), desc2.fn=0x9E38 flash) →
bl 0x1150 → **bx main=0x1907A** (литерал 0x1154=0x0801907B). Task-диспетч —
СТАТИЧЕСКИЙ (коррекция §74.1 «0 статических вызывающих»): ADC-ISR 0x1A31C
(системный тик) с bl-цепью 0x1A938/0x1D3D0/0x1F600/0x216E4/0x1A5C4.
"""

import struct  # noqa: E402

from fv_core import *  # noqa: F401,F403
from emulator.mcu_emu import (  # noqa: E402
    BootHarness, VEC_TABLE, SP_INIT, RESET_VECTOR,
    BOOT_STAGE1_INIT, BOOT_STAGE2, BOOT_TRAMP2, FOC_ISR_V22,
    BOOT_C_START, BOOT_MAIN, BOOT_CONSTRUCT_TABLE, BOOT_CONSTRUCT_END,
    BOOT_CONSTRUCT_FN1, BOOT_CONSTRUCT_FN2, ADC_ISR_TICK,
    ADC_TASK_FOC, ADC_TASK_D3D0, ADC_TASK_SCHED, ADC_TASK_UART4, ADC_TASK_SWSTART,
)


def _vectable(i):
    """The helper function (_vectable).
    Вспомогательная функция (_vectable).
    """
    return struct.unpack_from('<I', FW, VEC_TABLE + i * 4)[0] & ~0x08000000


@t(0x315C, 'Phase③ §95: BootHarness — cold-boot с reset-вектора: детерминированно до TRAMP2 (insn=6314, final_pc=0xcd78, reached=stage1+stage2+tramp2, periph=0xFF). Векторная таблица @0x1000 (коррекция «отсутствует»). Потолок: initial stack = C-runtime runtime RAM → полный cold-boot до main-loop = SWD-дамп RAM при reset')
def _(run, rng):
    """Emulator test @ 0x315c: Phase③ §95: BootHarness — cold-boot с reset-вектора: детерминированно до TRAMP2 (insn=6314, final_pc=0xcd78, reached=stage1+stage2+tramp2, periph=0xFF). Векторная таблица @0x1000 (коррекция «отсутствует»). Потолок: initial stack = C-runtime runtime RAM → полный cold-boot до main-loop = SWD-дамп RAM при reset.
    Тест эмулятора @ 0x315c: Phase③ §95: BootHarness — cold-boot с reset-вектора: детерминированно до TRAMP2 (insn=6314, final_pc=0xcd78, reached=stage1+stage2+tramp2, periph=0xFF). Векторная таблица @0x1000 (коррекция «отсутствует»). Потолок: initial stack = C-runtime runtime RAM → полный cold-boot до main-loop = SWD-дамп RAM при reset.
    """
    h = BootHarness()
    h.reset()
    insn, pc, reached = h.run()
    assert insn == 6314, f"insn={insn} ждём 6314 (детерминизм)"
    assert pc == 0xCD78, f"final_pc={pc:#x} ждём 0xcd78"
    assert reached == {'stage1', 'stage2', 'tramp2'}, f"reached={reached}"
    # повторный прогон идентичен (детерминизм)
    h2 = BootHarness()
    h2.reset()
    i2, p2, r2 = h2.run()
    assert (i2, p2, r2) == (insn, pc, reached), "boot не детерминирован"


@t(FOC_ISR_V22, 'Phase③ §95: векторная таблица @0x1000 — [0]=SP_INIT 0x20004E40, [1]=reset|1 0x315d, [14]=PendSV 0x3173, [15]=SysTick 0x13cad, [22]=FOC-ISR 0x7875 (подтверждение примечания «вектор [22]=0x7875»). Коррекция: таблица существует (не «отсутствует/OTA»)')
def _(run, rng):
    """The helper function (_).
    Вспомогательная функция (_).
    """
    assert VEC_TABLE == 0x1000
    assert _vectable(0) == SP_INIT == 0x20004E40, f"[0]={_vectable(0):#x}"
    assert _vectable(1) == (RESET_VECTOR | 1) == 0x315D, f"[1]={_vectable(1):#x}"
    assert (_vectable(1) & ~1) == RESET_VECTOR == 0x315C
    assert _vectable(1) & 1, "[1] должен иметь Thumb-bit"
    assert _vectable(14) == 0x3173, f"[14] PendSV={_vectable(14):#x}"
    assert _vectable(15) == 0x13CAD, f"[15] SysTick={_vectable(15):#x}"
    assert _vectable(22) == FOC_ISR_V22 == 0x7875, f"[22]={_vectable(22):#x}"
    # stage-адреса когерентны (в flash1)
    for a in (BOOT_STAGE1_INIT, BOOT_STAGE2, BOOT_TRAMP2):
        assert 0x1000 <= a < 0x24000, f"{a:#x} вне кода"


def _word(off):
    """The u32 word of the image at the offset.
    u32-слово образа по смещению."""
    return struct.unpack_from('<I', FW, off)[0]


def _bl_at(off):
    """The point-decode of the 4 bytes at off: return the b/bl target or None.
    Точечный декод 4 байт по off: цель b/bl или None (bl — самодостаточный)."""
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
    cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    cs.detail = True
    for ins in cs.disasm(FW[off:off + 4], off):
        if ins.mnemonic in ('b', 'b.w', 'bl', 'bl.w') and ins.address == off:
            try:
                return ins.operands[0].imm
            except Exception:
                return None
        return None
    return None


@t(BOOT_C_START, 'Phase④ §97: C-старт 0x1148 — реконструированный cold-boot: zero-RAM стоп на TRAMP1 (insn=3138, pc=0x3166); seed [SP+12]=0x1149 + патч live RAM-callback (0x20000040) → детерминированно до main 0x1907A (insn=3282, final_pc=0x1912C, reached={stage1,cstart,main})')
def _(run, rng):
    """The Phase 4 C-start test: the zero-RAM stall at TRAMP1 + the reconstructed
    cold boot to main.
    Тест Phase ④ C-старта: zero-RAM стоп на TRAMP1 + реконструированный cold-boot
    до main."""
    # zero-RAM без сида: TRAMP1 pop pc=0 → стоп на 0x3166 (initial stack = runtime)
    h0 = BootHarness()
    h0.reset(seed_stage2=0)
    i0, p0, r0 = h0.run()
    assert i0 == 3138 and p0 == 0x3166 and r0 == {'stage1'}, \
        f"zero-RAM: {(i0, p0, r0)} ждём (3138, 0x3166, {{stage1}})"
    # C-старт + патч live RAM-callback → до main
    h = BootHarness()
    h.reset(c_start=True)
    insn, pc, reached = h.run(patch_ram_callback=True)
    assert insn == 3282, f"insn={insn} ждём 3282"
    assert pc == 0x1912C, f"final_pc={pc:#x} ждём 0x1912c (main-регион)"
    assert reached == {'stage1', 'cstart', 'main'}, f"reached={reached}"
    # детерминизм
    h2 = BootHarness()
    h2.reset(c_start=True)
    i2, p2, r2 = h2.run(patch_ram_callback=True)
    assert (i2, p2, r2) == (insn, pc, reached), "C-старт не детерминирован"


@t(BOOT_MAIN, 'Phase④ §97: main=0x1907A — литералы C-старта: [0x1154]=0x0801907B (main), [0x1158]=0x20004E40 (SP); конструктор-тейбл @0x1AD28..0x1AD48 (2×16Б): desc1.fn=0x20000040 (код в RAM, live), desc2.fn=0x9E38 (flash)')
def _(run, rng):
    """The Phase 4 main-literals test: the C-start literal pool + the constructor
    table.
    Тест Phase ④ main-литералов: лит-пул C-старта + конструктор-тейбл."""
    assert _word(0x1154) == 0x0801907B, f"[0x1154]={_word(0x1154):#x} ждём 0x0801907B"
    assert _word(0x1158) == SP_INIT == 0x20004E40, f"[0x1158]={_word(0x1158):#x}"
    # конструктор-тейбл: граница и fn-поля
    assert BOOT_CONSTRUCT_END - BOOT_CONSTRUCT_TABLE == 0x20  # 2 дескриптора по 16Б
    assert _word(BOOT_CONSTRUCT_TABLE + 0xC) == BOOT_CONSTRUCT_FN1 == 0x20000040, \
        f"desc1.fn={_word(BOOT_CONSTRUCT_TABLE + 0xC):#x}"
    assert _word(BOOT_CONSTRUCT_TABLE + 0x10 + 0xC) == BOOT_CONSTRUCT_FN2 == 0x9E38, \
        f"desc2.fn={_word(BOOT_CONSTRUCT_TABLE + 0x1C):#x}"


@t(ADC_ISR_TICK, 'Phase④ §97: ADC-ISR 0x1A31C (системный тик) — СТАТИЧЕСКАЯ task-цепь (коррекция §74.1 «0 статических вызывающих»): bl 0x1A49E→0x1A938 (FOC), 0x1A514→0x1D3D0, 0x1A518→0x1F600 (планировщик/TX), 0x1A51C→0x216E4 (UART4), 0x1A520→0x1A5C4 (SWSTART ADC). «Потолок §74.1» — артефакт раннего декода capstone (остановка на первом нераскодированном байте)')
def _(run, rng):
    """The Phase 4 task-chain test: the ADC-ISR static bl chain (the section 74.1
    correction).
    Тест Phase ④ task-цепи: статическая bl-цепь ADC-ISR (коррекция §74.1)."""
    assert _bl_at(0x1A49E) == ADC_TASK_FOC == 0x1A938, f"0x1A49E → {_bl_at(0x1A49E)}"
    assert _bl_at(0x1A514) == ADC_TASK_D3D0 == 0x1D3D0, f"0x1A514 → {_bl_at(0x1A514)}"
    assert _bl_at(0x1A518) == ADC_TASK_SCHED == 0x1F600, f"0x1A518 → {_bl_at(0x1A518)}"
    assert _bl_at(0x1A51C) == ADC_TASK_UART4 == 0x216E4, f"0x1A51C → {_bl_at(0x1A51C)}"
    assert _bl_at(0x1A520) == ADC_TASK_SWSTART == 0x1A5C4, f"0x1A520 → {_bl_at(0x1A520)}"
    # сам планировщик вызывает TX-байт 0x1F1C0
    assert _bl_at(0x1F67E) == 0x1F1C0, f"0x1F67E → {_bl_at(0x1F67E)}"
