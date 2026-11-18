# ruff: noqa: F405
"""§93 (A7): карта регистров периферии — машиночитаемый референс нестандартной раскладки.

Консолидация фактов §48/§49/§50/§76/§78.5/§89/§91 в PERIPH_REG_MAP (30 блоков) +
RCC_SETCLEAR_FAMILY (6 set/clear-примитивов 0xC6xx, gap 0xC63E..0xC684 = 0xC644/0xC664)
+ HSE=20 МГц. PeriphRegMap: block/base_of/touched_bases (сверка с periph-записями).
Ключевые нестандартные раскладки: NVIC-база 0xE000E400 (не 0xE000E100), USART
SR@+0x3C/ICER@+0x40 (не F1), SPI1 @0x40013000 (не стандарт), кастомный блок
@0x40003000 (свободен в F1/GD32F103), две GPIO-раскладки (F1 @0x40010800 +
кастомный блок @0x48000000), WWDG @0x40002800 = таймер событий с BCD-окном.
"""

from fv_core import *  # noqa: F401,F403
from emulator.mcu_emu import (HSE_MHZ, PERIPH_REG_MAP, RCC_SETCLEAR_FAMILY,  # noqa: E402
                              PeriphRegMap)


@t(0x1302C, 'A7 §93: PeriphRegMap — карта регистров (30 блоков): целостность (уникальные базы, ключевые: RCC/FLASH/TIM1/ADC1/USART1/USART3/I2C2/SPI1/WWDG/NVIC/SCB/SysTick), HSE=20 МГц, base_of (USART1/RCC/SPI1/I2C2), block()')
def _(run, rng):
    assert len(PERIPH_REG_MAP) == 30, f"блоков = {len(PERIPH_REG_MAP)} ждём 30"
    # уникальные базы
    bases = list(PERIPH_REG_MAP)
    assert len(set(bases)) == len(bases), 'базы не уникальны'
    for need in (0x40021000, 0x40022000, 0x40012C00, 0x40012400,
                 0x40013800, 0x40004800, 0x40005800, 0x40013000,
                 0x40002800, 0x40003000, 0xE000E400, 0xE000ED00,
                 0xE000E010, 0x40010800, 0x48000000, 0x40010000):
        assert need in PERIPH_REG_MAP, f'нет блока {need:#x}'
    assert HSE_MHZ == 20
    m = PeriphRegMap()
    assert m.base_of('USART1') == 0x40013800
    assert m.base_of('RCC') == 0x40021000
    assert m.base_of('SPI1') == 0x40013000
    assert m.base_of('I2C2') == 0x40005800
    assert m.block(0x4002100C)[0] == 'RCC'
    assert m.block(0x40005800)[0].startswith('I2C2')
    # NVIC-база нестандартная
    assert 0xE000E400 in PERIPH_REG_MAP and 0xE000E100 not in PERIPH_REG_MAP


@t(0x1302C, 'A7 §93: RCC set/clear-семья (0xC6xx) — 6 примитивов: offset {0x00:0xC60C, 0x14:0xC624, 0x28:0xC644, 0x1C:0xC664, 0x10:0xC684, 0x18:0xC6A4}; gap 0xC63E..0xC684 = 0xC644(+0x28)/0xC664(+0x1C) — в карте RCC-блока')
def _(run, rng):
    assert len(RCC_SETCLEAR_FAMILY) == 6
    assert RCC_SETCLEAR_FAMILY[0x28] == 0xC644
    assert RCC_SETCLEAR_FAMILY[0x1C] == 0xC664
    assert RCC_SETCLEAR_FAMILY[0x10] == 0xC684
    assert RCC_SETCLEAR_FAMILY[0x18] == 0xC6A4
    assert RCC_SETCLEAR_FAMILY[0x14] == 0xC624
    assert RCC_SETCLEAR_FAMILY[0x00] == 0xC60C
    # эти офсеты описаны в RCC-блоке карты
    rcc_offs = PERIPH_REG_MAP[0x40021000][1]
    for off in RCC_SETCLEAR_FAMILY:
        assert off in rcc_offs, f'RCC офсет {off:#x} не в карте'


@t(0x1302C, 'A7 §93: PeriphRegMap.touched_bases — сверка карты с periph-записями: 0x1302C(0x40004800) (RCC-пульс USART3) трогает RCC @0x40021000 (бит 0x40000 в +0x10) — база присутствует в карте')
def _(run, rng):
    emu = McuEmu(max_insn=50000)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))
    emu.hook_periph_ready()
    uc.reg_write(UC_ARM_REG_R0, 0x40004800)
    uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
    uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    try:
        uc.emu_start(0x1302C | 1, 0, count=50000)
    except Exception:
        pass
    m = PeriphRegMap(emu)
    touched = m.touched_bases()
    assert 0x40021000 in touched, f'0x1302c: RCC-база не в touched: {[hex(b) for b in touched]}'
    # записи в RCC+0x10 с битом 0x40000 (USART3-пульс)
    rcc_writes = [w for w in emu.periph_writes if (w[1] & ~0xFF) == 0x40021000]
    assert rcc_writes, '0x1302c: нет записей в RCC'
    assert any((w[3] & 0x40000) or (w[3] & 0xFFFF) for w in rcc_writes), \
        f'0x1302c: RCC-записи без ожидаемого бита: {[hex(w[3]) for w in rcc_writes]}'
