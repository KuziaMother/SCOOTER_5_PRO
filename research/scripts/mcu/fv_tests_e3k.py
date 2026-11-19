# ruff: noqa: F405
"""§95 (Phase ③): cold-boot — векторная таблица @0x1000 + startup-цепочка.

BootHarness (emulator/mcu_emu.py): старт с reset-вектора (без железа).
**Векторная таблица существует @0x1000** (коррекция «отсутствует»): [0]=SP_INIT
0x20004E40, [1]=reset|1=0x315d, [14]=PendSV, [15]=SysTick, [22]=FOC-ISR 0x7875.
**Startup-цепочка (live verified):** reset 0x315c → bl 0xcd0c (stage1: init+
busy-wait 0x2ff) → TRAMP1 pop@0x3166 (pc=RAM[SP+12]=stage2|Thumb) → stage2 0x3168
(init-цепочка 0xcc68/0xc9dc/0x5970/0xcb40) → TRAMP2 pop@0x31c6. Детерминированно
до TRAMP2: insn=6314, final_pc=0xcd78, periph=0xFF. **Потолок (live):** initial
stack = данные C-runtime (runtime RAM); полный cold-boot до main-loop — SWD-дамп
RAM при reset. Main-loop dispatch — runtime function-pointer (потолок §74.1).
"""

import struct  # noqa: E402

from fv_core import *  # noqa: F401,F403
from emulator.mcu_emu import (  # noqa: E402
    BootHarness, VEC_TABLE, SP_INIT, RESET_VECTOR,
    BOOT_STAGE1_INIT, BOOT_STAGE2, BOOT_TRAMP2, FOC_ISR_V22,
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
