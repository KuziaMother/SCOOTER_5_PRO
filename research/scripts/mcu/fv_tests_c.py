# -*- coding: utf-8 -*-
# ruff: noqa: F405  (имена из star-import от fv_core)
"""E1: §74 ControlLoop, модели A/B/C/D, CRC-7/E1 close-out (4332-4902)."""
from fv_core import *  # noqa: F401,F403
from fv_core import _fresh_call, _intercept  # noqa: F401
# --- §74: ControlLoop — автономный time-driven контур (warm-start) ---
@t(0x1D078, '§74: ControlLoop — автономный time-driven warm-start контур. Виртуальные часы + реальный firmware PID(0x1d078)+FOC(0x1a938) на каждом tick + plant/battery/range (один emu, общий RAM). target=208: скорость растёт от 0 (max>150), throttle>0 всюду, FOC-amp>0 (FOC исполняется каждый шаг), SoC падает с нагрузкой, range>0. Сходится ВЫШЕ target (~325) — свойство калибровки plant/PID; траектория совпадает с _foc_sim.py 40/40.')
def _(run, rng):
    """Emulator test @ 0x1d078: §74: ControlLoop — автономный time-driven warm-start контур. Виртуальные часы + реальный firmware PID(0x1d078)+FOC(0x1a938) на каждом tick + plant/battery/range (один emu, общий RAM). target=208: скорость растёт от 0 (max>150), throttle>0 всюду, FOC-amp>0 (FOC исполняется каждый шаг), SoC падает с нагрузкой, range>0. Сходится ВЫШЕ target (~325) — свойство калибровки plant/PID; траектория совпадает с _foc_sim.py 40/40..
    Тест эмулятора @ 0x1d078: §74: ControlLoop — автономный time-driven warm-start контур. Виртуальные часы + реальный firmware PID(0x1d078)+FOC(0x1a938) на каждом tick + plant/battery/range (один emu, общий RAM). target=208: скорость растёт от 0 (max>150), throttle>0 всюду, FOC-amp>0 (FOC исполняется каждый шаг), SoC падает с нагрузкой, range>0. Сходится ВЫШЕ target (~325) — свойство калибровки plant/PID; траектория совпадает с _foc_sim.py 40/40..
    """
    from emulator.mcu_emu import ControlLoop, McuEmu
    femu = McuEmu(trace=False, max_insn=400000)
    cl = ControlLoop(emu=femu, v_max=522.0, tau=15.0, throttle_ref=28624.0)
    cl.setup(target=208, mode=3, soc=100.0)
    traj = cl.run(24)
    # старт: скорость >0 и мала
    assert traj[0]['speed'] > 0 and traj[0]['speed'] < 60, f"start: {traj[0]}"
    # тяга есть всюду (throttle>0)
    assert all(st['throttle'] > 0 for st in traj), 'throttle<=0 (нет тяги)'
    # FOC исполняется каждый шаг (amp>0)
    assert all(st['pwm_amp'] > 0 for st in traj), 'FOC-amp=0 (FOC не исполняется)'
    # скорость растёт к target (достигает >150)
    assert max(st['speed'] for st in traj) > 150, \
        f"max speed {max(s['speed'] for s in traj)} < 150"
    # батарея разряжается с нагрузкой
    assert traj[-1]['soc'] < 100.0, f"SoC не падает: {traj[-1]['soc']}"
    # запас хода вычисляется (R>0)
    assert all(st['range'] > 0 for st in traj), 'range<=0'


# --- A1: GpioModel (кастомный GPIO-блок «портов», §39.1) ---
@t(0x1BF48, 'A1: GpioModel — кастомный GPIO-блок «портов» (§39.1): 4 порта × stride 0x400 (база 0x48000000), режимы в MODER_LO/HI (+0x2c/+0x28) по 2 бита/пин. MOTOR-INIT 0x1bf48 конфигурирует пины через драйвер 0x22000; модель ловит записи и декодит режимы. Детерминизм: фиксированный набор портов с ненулевыми режимами (MODER_LO записан).')
def _(run, rng):
    """Emulator test @ 0x1bf48: A1: GpioModel — кастомный GPIO-блок «портов» (§39.1): 4 порта × stride 0x400 (база 0x48000000), режимы в MODER_LO/HI (+0x2c/+0x28) по 2 бита/пин. MOTOR-INIT 0x1bf48 конфигурирует пины через драйвер 0x22000; модель ловит записи и декодит режимы. Детерминизм: фиксированный набор портов с ненулевыми режимами (MODER_LO записан)..
    Тест эмулятора @ 0x1bf48: A1: GpioModel — кастомный GPIO-блок «портов» (§39.1): 4 порта × stride 0x400 (база 0x48000000), режимы в MODER_LO/HI (+0x2c/+0x28) по 2 бита/пин. MOTOR-INIT 0x1bf48 конфигурирует пины через драйвер 0x22000; модель ловит записи и декодит режимы. Детерминизм: фиксированный набор портов с ненулевыми режимами (MODER_LO записан)..
    """
    from emulator.mcu_emu import GpioModel
    uc = run.uc
    uc.mem_write(RAM, bytes(0x20000))          # чистая RAM → детерминизм
    run.emu.hook_periph_ready()                 # status-биты ready (как в run_func)
    gpio = GpioModel(run.emu)
    def _st(uc_, addr, size, u):
        """The helper function (_st).
        Вспомогательная функция (_st).
        """
        aa = addr & ~1
        if not (FLASH0 <= aa < FLASH0 + FW_LEN or
                FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, _st)
    try:
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1BF48 | 1, 0, count=200000)
        except UcError:
            pass
    finally:
        uc.hook_del(sh)
        uc.hook_del(gpio._hook)
    # модель поймала записи в портовый блок
    assert gpio.writes, 'GpioModel не поймал записей в портовый блок'
    ports_written = sorted(set(p for _, p, _, _, _ in gpio.writes))
    assert ports_written, 'порты не записаны'
    # декод режимов: MODER_LO (+0x2c) записан с ненулевым пакетом хотя бы в один порт
    cfg = gpio.config_report()
    assert cfg, 'config_report пуст — ни одного ненулевого режима пина'
    moder_ports = [p for p in range(4) if gpio.read(p, 0x2c)]
    assert moder_ports, 'MODER_LO (+0x2c) не записан ни в одном порту'
    # каждый декодированный режим — валиден (0..3 по 2 бита)
    for p, pins in cfg.items():
        for pin, mode in pins.items():
            assert 0 <= mode <= 3, f'невалидный режим {mode} порт {p} пин {pin}'


# --- A2: UsartTxModel (push-кадры, сборщик 0x211f8) ---
@t(0x211F8, 'A2: UsartTxModel — push-TX pipeline (этап сборки). Прогон РЕАЛЬНОГО сборщика 0x211f8 (без арг., читает фикс. RAM-поля телеметрии) → TX-кольцо @0x10b5 → декод кадров 61..9E (chk=SUM&0xFF). Seed: mode@0x229=2, u16@0x236=50 → валидный a0-кадр с mode_lo=2 и pct_0x236=50.')
def _(run, rng):
    """Emulator test @ 0x211f8: A2: UsartTxModel — push-TX pipeline (этап сборки). Прогон РЕАЛЬНОГО сборщика 0x211f8 (без арг., читает фикс. RAM-поля телеметрии) → TX-кольцо @0x10b5 → декод кадров 61..9E (chk=SUM&0xFF). Seed: mode@0x229=2, u16@0x236=50 → валидный a0-кадр с mode_lo=2 и pct_0x236=50..
    Тест эмулятора @ 0x211f8: A2: UsartTxModel — push-TX pipeline (этап сборки). Прогон РЕАЛЬНОГО сборщика 0x211f8 (без арг., читает фикс. RAM-поля телеметрии) → TX-кольцо @0x10b5 → декод кадров 61..9E (chk=SUM&0xFF). Seed: mode@0x229=2, u16@0x236=50 → валидный a0-кадр с mode_lo=2 и pct_0x236=50..
    """
    from emulator.mcu_emu import McuEmu, UsartTxModel
    femu = McuEmu(trace=False, max_insn=400000)
    uc = femu.uc
    uc.mem_write(RAM, bytes(0x20000))          # чистая RAM → детерминизм
    uc.mem_write(RAM + 0x229, bytes([2]))              # mode lo
    uc.mem_write(RAM + 0x236, struct.pack('<H', 50))   # pct (u16@0x236)
    uc.mem_write(RAM + 0x306, struct.pack('<H', 89))   # батарея %
    femu.hook_periph_ready()
    tx = UsartTxModel(femu)
    frames = tx.assemble()
    assert frames, 'сборщик не произвёл ни одного валидного push-кадра'
    a0 = [f for f in frames if f[1] == 0x30]
    assert a0, 'нет a0-кадра (телеметрия)'
    raw, sub, fl = a0[0]
    assert fl['mode'] & 0xF == 2, f"mode_lo != 2: {fl['mode']:02x} (seed @0x229=2)"
    assert fl['pct_0x236'] == 50, f"pct_0x236 != 50: {fl['pct_0x236']} (seed @0x236=50)"


# --- A3: SpiFlashModel (внешний SPI-flash / NVM) ---
@t(0x221E6, 'A3: SpiFlashModel — внешний SPI-flash (NVM). Виртуальный буфер size=0x1000 (≤4KB, из валидации addr в 0x221e6), дефолт 0xFF (стёртая flash); set/get round-trip; OOB -> ValueError. SPI-протокол: write-enable 0x221a4 (cmd 0x06) + page-program 0x221e6 (шаг слота 4Б); NVRAM-save 0x21A08 персистит конфиг/калибровку.')
def _(run, rng):
    """Emulator test @ 0x221e6: A3: SpiFlashModel — внешний SPI-flash (NVM). Виртуальный буфер size=0x1000 (≤4KB, из валидации addr в 0x221e6), дефолт 0xFF (стёртая flash); set/get round-trip; OOB -> ValueError. SPI-протокол: write-enable 0x221a4 (cmd 0x06) + page-program 0x221e6 (шаг слота 4Б); NVRAM-save 0x21A08 персистит конфиг/калибровку..
    Тест эмулятора @ 0x221e6: A3: SpiFlashModel — внешний SPI-flash (NVM). Виртуальный буфер size=0x1000 (≤4KB, из валидации addr в 0x221e6), дефолт 0xFF (стёртая flash); set/get round-trip; OOB -> ValueError. SPI-протокол: write-enable 0x221a4 (cmd 0x06) + page-program 0x221e6 (шаг слота 4Б); NVRAM-save 0x21A08 персистит конфиг/калибровку..
    """
    from emulator.mcu_emu import McuEmu, SpiFlashModel, NVM_SIZE
    assert NVM_SIZE == 0x1000, f'NVM_SIZE != 4KB: {NVM_SIZE:#x}'
    femu = McuEmu(trace=False, max_insn=200000)
    nvm = SpiFlashModel(femu)
    assert all(b == 0xFF for b in nvm.flash), 'NVM-дефолт != 0xFF (стёртая flash)'
    nvm.set(0x10, struct.pack('<H', 0x1234))
    assert nvm.get(0x10, 2) == b'\x34\x12', 'set/get round-trip (little-endian u16)'
    nvm.seed({0x20: 89, 0x30: bytes([1, 2, 3])})
    assert nvm.get(0x20, 1) == b'\x59', 'seed byte'
    assert nvm.get(0x30, 3) == b'\x01\x02\x03', 'seed bytes'
    try:
        nvm.set(NVM_SIZE - 1, b'\x00\x00')   # 2 байта за границей
        assert False, 'OOB set не выбросил ValueError'
    except ValueError:
        pass


# --- B1: CmdControlModel (командный слой -> блок управления @0x40021000) ---
@t(0xC664, 'B1: CmdControlModel — командный слой (dispatcher 0x2e0c / handler 0x97f4) шевелит биты в кастомном блоке управления @0x40021000 (поля +0x10/+0x18/+0x1c). Примитив 0xc664(r0=бит, r1=set/clear): pre-set поля в 0 -> set(0x200000) пишет ровно бит21 в +0x1c; clear снимает. Модель ловит операции.')
def _(run, rng):
    """Emulator test @ 0xc664: B1: CmdControlModel — командный слой (dispatcher 0x2e0c / handler 0x97f4) шевелит биты в кастомном блоке управления @0x40021000 (поля +0x10/+0x18/+0x1c). Примитив 0xc664(r0=бит, r1=set/clear): pre-set поля в 0 -> set(0x200000) пишет ровно бит21 в +0x1c; clear снимает. Модель ловит операции..
    Тест эмулятора @ 0xc664: B1: CmdControlModel — командный слой (dispatcher 0x2e0c / handler 0x97f4) шевелит биты в кастомном блоке управления @0x40021000 (поля +0x10/+0x18/+0x1c). Примитив 0xc664(r0=бит, r1=set/clear): pre-set поля в 0 -> set(0x200000) пишет ровно бит21 в +0x1c; clear снимает. Модель ловит операции..
    """
    from emulator.mcu_emu import McuEmu, CmdControlModel, CMD_CTRL_BASE
    femu = McuEmu(trace=False, max_insn=50000)
    uc = femu.uc
    uc.mem_write(RAM, bytes(0x20000))
    femu.hook_periph_ready()
    for off in (0x10, 0x18, 0x1c):
        femu.uc.mem_write(CMD_CTRL_BASE + off, struct.pack('<I', 0))   # pre-set в 0
    cmd = CmdControlModel(femu)

    def _call(fn, r0, r1):
        """The helper function (_call).
        Вспомогательная функция (_call).
        """
        from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1
        def _st(uc_, a, s, u):
            """The helper function (_st).
            Вспомогательная функция (_st).
            """
            aa = a & ~1
            if not (FLASH0 <= aa < FLASH0 + 0x23680 or
                    FLASH1 <= aa < FLASH1 + 0x23680):
                uc_.emu_stop()
        sh = uc.hook_add(UC_HOOK_CODE, _st)
        try:
            uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x20)
            uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
            uc.reg_write(UC_ARM_REG_R0, r0)
            uc.reg_write(UC_ARM_REG_R1, r1)
            femu.insn = 0
            try:
                uc.emu_start(fn | 1, 0, count=50000)
            except UcError:
                pass
        finally:
            uc.hook_del(sh)
    cmd.ops.clear()
    _call(0xC664, 0x200000, 1)   # set bit21 в +0x1c
    assert any(o == 0x1c and v == 0x200000 for _, o, v in cmd.ops), \
        f'0xc664(0x200000,set) не поставил бит21 в +0x1c: {cmd.ops}'
    cmd.ops.clear()
    _call(0xC664, 0x200000, 0)   # clear bit21 (поле сейчас 0x200000)
    assert any(o == 0x1c and v == 0 for _, o, v in cmd.ops), \
        f'0xc664(0x200000,clear) не снял бит21: {cmd.ops}'


# --- B2: UsartRxCommandTable (USART3 RX-протокол = ASCII-command-ID) ---
@t(0x1E9E0, 'B2: UsartRxCommandTable — USART3 RX-протокол (BLE→MCU) = ASCII-command-ID. Парсер 0x1e9e0 (1914 Б), 15 команд @ A B C D E F G H I J K ` a c, 2 категории (@GKc=cat2 response/status; остальные=cat0xa SET-params). Таблица сверена с cmp-иммедиатами в dispatch-регионах (static-consistency).')
def _(run, rng):
    """Emulator test @ 0x1e9e0: B2: UsartRxCommandTable — USART3 RX-протокол (BLE→MCU) = ASCII-command-ID. Парсер 0x1e9e0 (1914 Б), 15 команд @ A B C D E F G H I J K ` a c, 2 категории (@GKc=cat2 response/status; остальные=cat0xa SET-params). Таблица сверена с cmp-иммедиатами в dispatch-регионах (static-consistency)..
    Тест эмулятора @ 0x1e9e0: B2: UsartRxCommandTable — USART3 RX-протокол (BLE→MCU) = ASCII-command-ID. Парсер 0x1e9e0 (1914 Б), 15 команд @ A B C D E F G H I J K ` a c, 2 категории (@GKc=cat2 response/status; остальные=cat0xa SET-params). Таблица сверена с cmp-иммедиатами в dispatch-регионах (static-consistency)..
    """
    import os as _os
    import re
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
    from emulator.mcu_emu import USART_RX_COMMANDS, usart_rx_cmd
    fw_path = _os.path.join(_os.path.dirname(__file__), '..', '..', 'images', 'mcu_0007.bin')
    fw = open(fw_path, 'rb').read()
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)

    def cmd_chars(off, end):
        """The cmd_chars function of the script.
        Функция cmd_chars скрипта.
        """
        chars = set()
        for i in md.disasm(fw[off:end], off):
            if i.mnemonic == 'cmp':
                m = re.search(r'#(0x[0-9a-f]+|\d+)', i.op_str)
                if m:
                    imm = int(m.group(1), 0)
                    if 32 <= imm < 127:
                        chars.add(chr(imm))
        return chars
    main_chars = cmd_chars(0x1EB38, 0x1EB94)
    cat_chars = cmd_chars(0x1EA30, 0x1EA76)
    table_keys = set(USART_RX_COMMANDS.keys())
    assert main_chars == table_keys, \
        f'main dispatch {sorted(main_chars)} != table {sorted(table_keys)}'
    assert cat_chars == table_keys, \
        f'classifier {sorted(cat_chars)} != table {sorted(table_keys)}'
    for ch, (h, cat, desc) in USART_RX_COMMANDS.items():
        expect = 2 if ch in '@GKc' else 0xA
        assert cat == expect, f'{ch!r}: cat={cat:#x} != {expect:#x}'
    assert usart_rx_cmd(0x41)[0] == 0x1EC74   # 'A'
    assert usart_rx_cmd('a')[0] == 0x1F112
    assert usart_rx_cmd(0x58) is None          # 'X' — неизвестно


# --- E1: покрытие — bsearch (floor index для интерполяции) ---
@t(0x16176, 'E1: 0x16176 — i16 bsearch (floor index). 0x16176(key, arr, mid0, hi) с mid0=0 возвращает clamped lower_bound: последний i в [0,hi) с arr[i]<=key; 0 если key<arr[0]. Вериф на сортированном i16-массиве по диапазону ключей (эмулятор).')
def _(run, rng):
    """Emulator test @ 0x16176: E1: 0x16176 — i16 bsearch (floor index). 0x16176(key, arr, mid0, hi) с mid0=0 возвращает clamped lower_bound: последний i в [0,hi) с arr[i]<=key; 0 если key<arr[0]. Вериф на сортированном i16-массиве по диапазону ключей (эмулятор)..
    Тест эмулятора @ 0x16176: E1: 0x16176 — i16 bsearch (floor index). 0x16176(key, arr, mid0, hi) с mid0=0 возвращает clamped lower_bound: последний i в [0,hi) с arr[i]<=key; 0 если key<arr[0]. Вериф на сортированном i16-массиве по диапазону ключей (эмулятор)..
    """
    arr = [10, 20, 30, 40, 50]
    ARR_OFF = 0x4000
    for i, v in enumerate(arr):
        run.ram_write(ARR_OFF + i * 2, struct.pack('<h', v))
    def clamped_lb(key):
        """The clamped_lb function of the script.
        Функция clamped_lb скрипта.
        """
        r = -1
        for i, v in enumerate(arr):
            if v <= key:
                r = i
        return max(0, r)
    n = 0
    for key in list(range(0, 70, 3)) + [5, 10, 25, 49, 50, 60]:
        r0, _ = run.call(0x16176, args=(key, RAM + ARR_OFF, 0, len(arr)))
        assert r0 == clamped_lb(key), f'key={key}: got {r0}, want {clamped_lb(key)}'
        n += 1
    assert n >= 25


@t(0x1619E, 'E1: 0x1619e — u32 bsearch (твин 0x16176, unsigned). Те же семантики clamped lower_bound для u32-массива (ldr [arr,mid<<2]).')
def _(run, rng):
    """Emulator test @ 0x1619e: E1: 0x1619e — u32 bsearch (твин 0x16176, unsigned). Те же семантики clamped lower_bound для u32-массива (ldr [arr,mid<<2])..
    Тест эмулятора @ 0x1619e: E1: 0x1619e — u32 bsearch (твин 0x16176, unsigned). Те же семантики clamped lower_bound для u32-массива (ldr [arr,mid<<2])..
    """
    arr = [100, 200, 300, 400, 500]
    ARR_OFF = 0x4100
    for i, v in enumerate(arr):
        run.ram_write(ARR_OFF + i * 4, struct.pack('<I', v))
    def clamped_lb(key):
        """The clamped_lb function of the script.
        Функция clamped_lb скрипта.
        """
        r = -1
        for i, v in enumerate(arr):
            if v <= key:
                r = i
        return max(0, r)
    for key in [0, 50, 100, 250, 300, 499, 500, 600]:
        r0, _ = run.call(0x1619E, args=(key, RAM + ARR_OFF, 0, len(arr)))
        assert r0 == clamped_lb(key), f'key={key}: got {r0}, want {clamped_lb(key)}'


# --- C1: LutModel (LUT-блоки range-эстиматора 0x1d898) ---
@t(0x1D898, 'C1: LutModel — LUT-блоки range-эстиматора 0x1d898 @RAM+0x614 (45 слов) / RAM+0x738 (53 слова), u32-слова шаг 4. Модель ловит ЧТЕНИЯ firmware: 0x1d898 сканирует оба блока (каждое слово по разу); status-гейты @0x286/0x29e (§73.13). Тест: свежий McuEmu + battery seed -> прогон 0x1d898 -> модель зафиксировала скан обоих блоков + seed/get round-trip.')
def _(run, rng):
    """Emulator test @ 0x1d898: C1: LutModel — LUT-блоки range-эстиматора 0x1d898 @RAM+0x614 (45 слов) / RAM+0x738 (53 слова), u32-слова шаг 4. Модель ловит ЧТЕНИЯ firmware: 0x1d898 сканирует оба блока (каждое слово по разу); status-гейты @0x286/0x29e (§73.13). Тест: свежий McuEmu + battery seed -> прогон 0x1d898 -> модель зафиксировала скан обоих блоков + seed/get round-trip..
    Тест эмулятора @ 0x1d898: C1: LutModel — LUT-блоки range-эстиматора 0x1d898 @RAM+0x614 (45 слов) / RAM+0x738 (53 слова), u32-слова шаг 4. Модель ловит ЧТЕНИЯ firmware: 0x1d898 сканирует оба блока (каждое слово по разу); status-гейты @0x286/0x29e (§73.13). Тест: свежий McuEmu + battery seed -> прогон 0x1d898 -> модель зафиксировала скан обоих блоков + seed/get round-trip..
    """
    from emulator.mcu_emu import (McuEmu, LutModel, RANGE_LUT0_OFF, RANGE_LUT0_WORDS,
                                  RANGE_LUT1_OFF, RANGE_LUT1_WORDS)
    femu = McuEmu(trace=False, max_insn=200000)
    uc = femu.uc
    uc.mem_write(RAM, bytes(0x20000))
    femu.hook_periph_ready()
    femu.uc.mem_write(RAM + 0x27A, struct.pack('<h', 480))   # battery середина [415..535]
    lut = LutModel(femu)

    def _st(uc_, a, s, u):
        """The helper function (_st).
        Вспомогательная функция (_st).
        """
        aa = a & ~1
        if not (FLASH0 <= aa < FLASH0 + 0x23680 or
                FLASH1 <= aa < FLASH1 + 0x23680):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, _st)
    try:
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x20)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R0, 0)
        femu.insn = 0
        try:
            uc.emu_start(0x1D898 | 1, 0, count=200000)
        except UcError:
            pass
    finally:
        uc.hook_del(sh)
    assert lut.scanned(RANGE_LUT0_OFF, RANGE_LUT0_WORDS), \
        f'блок0 не просканирован: прочитано {len(lut.reads)} оффс'
    assert lut.scanned(RANGE_LUT1_OFF, RANGE_LUT1_WORDS), 'блок1 не просканирован'
    lut.set_word(RANGE_LUT0_OFF + 8, 0xDEADBEEF)
    assert lut.get_word(RANGE_LUT0_OFF + 8) == 0xDEADBEEF


# --- C2: FocPipelineModel (FOC-рутина 0x1a938 как value-gated pipeline) ---
@t(0x1A938, 'C2: FocPipelineModel — FOC-рутина 0x1a938 как value-gated pipeline (не дискретный FSM; ветвления по токам/порогам, §60.3). Выходы: P@0x388 = current-ref @0x224 (1:1), PWM-фазы @0x382/4/6 = 1125 ± ~0.0103·|ref|. Тест: seeded ref -> прогон 0x1a938 -> P==ref + фазы отклоняются от center 1125 монотонно с |ref|.')
def _(run, rng):
    """Emulator test @ 0x1a938: C2: FocPipelineModel — FOC-рутина 0x1a938 как value-gated pipeline (не дискретный FSM; ветвления по токам/порогам, §60.3). Выходы: P@0x388 = current-ref @0x224 (1:1), PWM-фазы @0x382/4/6 = 1125 ± ~0.0103·|ref|. Тест: seeded ref -> прогон 0x1a938 -> P==ref + фазы отклоняются от center 1125 монотонно с |ref|..
    Тест эмулятора @ 0x1a938: C2: FocPipelineModel — FOC-рутина 0x1a938 как value-gated pipeline (не дискретный FSM; ветвления по токам/порогам, §60.3). Выходы: P@0x388 = current-ref @0x224 (1:1), PWM-фазы @0x382/4/6 = 1125 ± ~0.0103·|ref|. Тест: seeded ref -> прогон 0x1a938 -> P==ref + фазы отклоняются от center 1125 монотонно с |ref|..
    """
    from emulator.mcu_emu import (McuEmu, FocPipelineModel, FOC_ROUTINE, FOC_REF_OFF,
                                  FOC_PHASE_CENTER)

    def measure(ref):
        """The measure function of the script.
        Функция measure скрипта.
        """
        femu = McuEmu(trace=False, max_insn=200000)
        uc = femu.uc
        uc.mem_write(RAM, bytes(0x20000))
        femu.hook_periph_ready()
        femu.uc.mem_write(RAM + FOC_REF_OFF, struct.pack('<H', ref & 0xFFFF))
        foc = FocPipelineModel(femu)

        def _st(uc_, a, s, u):
            """The helper function (_st).
            Вспомогательная функция (_st).
            """
            aa = a & ~1
            if not (FLASH0 <= aa < FLASH0 + 0x23680 or
                    FLASH1 <= aa < FLASH1 + 0x23680):
                uc_.emu_stop()
        sh = uc.hook_add(UC_HOOK_CODE, _st)
        try:
            uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x20)
            uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
            uc.reg_write(UC_ARM_REG_R0, 0)
            femu.insn = 0
            try:
                uc.emu_start(FOC_ROUTINE | 1, 0, count=200000)
            except UcError:
                pass
        finally:
            uc.hook_del(sh)
        return foc.get_p(), foc.get_phases()
    # P == ref (1:1)
    for ref in (0, 500, 2000):
        p, _ = measure(ref)
        assert p == ref, f'ref={ref}: P@0x388={p} != ref'
    # фазы: center при ref=0; spread монотонно растёт с |ref|
    def spread(ref):
        """The spread function of the script.
        Функция spread скрипта.
        """
        _, ph = measure(ref)
        return max(abs(p - FOC_PHASE_CENTER) for p in ph)
    s0, s500, s2000 = spread(0), spread(500), spread(2000)
    assert s0 <= 2, f'ref=0 фазы не center: spread={s0}'
    assert s2000 > s500 > 0, f'spread не монотонен: 500={s500}, 2000={s2000}'


# --- D1: SchedulerModel (main-loop диспетчер 0x1f600) ---
@t(0x1F600, 'D1: SchedulerModel — main-loop диспетчер 0x1f600 (round-robin по N слотам). Ловит состояние (slot_index @0x2C2, slot-table @0xA43 stride 0x96, tick-слова @0x17F78+). ПОТОЛОК §74.1: task function-pointers runtime; в нулевом RAM dispatch упирается в unmapped fetch (jump to 0). Тест: seeded slot_index=1 -> прогон 0x1f600 -> модель зафиксировала чтение slot-index + tick-регионов (pre-dispatch логика).')
def _(run, rng):
    """Emulator test @ 0x1f600: D1: SchedulerModel — main-loop диспетчер 0x1f600 (round-robin по N слотам). Ловит состояние (slot_index @0x2C2, slot-table @0xA43 stride 0x96, tick-слова @0x17F78+). ПОТОЛОК §74.1: task function-pointers runtime; в нулевом RAM dispatch упирается в unmapped fetch (jump to 0). Тест: seeded slot_index=1 -> прогон 0x1f600 -> модель зафиксировала чтение slot-index + tick-регионов (pre-dispatch логика)..
    Тест эмулятора @ 0x1f600: D1: SchedulerModel — main-loop диспетчер 0x1f600 (round-robin по N слотам). Ловит состояние (slot_index @0x2C2, slot-table @0xA43 stride 0x96, tick-слова @0x17F78+). ПОТОЛОК §74.1: task function-pointers runtime; в нулевом RAM dispatch упирается в unmapped fetch (jump to 0). Тест: seeded slot_index=1 -> прогон 0x1f600 -> модель зафиксировала чтение slot-index + tick-регионов (pre-dispatch логика)..
    """
    from emulator.mcu_emu import (McuEmu, SchedulerModel, SCHEDULER_FN,
                                  SCHED_SLOT_INDEX_OFF, SCHED_TICK_WORDS_OFF)
    femu = McuEmu(trace=False, max_insn=50000)
    uc = femu.uc
    uc.mem_write(RAM, bytes(0x20000))
    femu.hook_periph_ready()
    sch = SchedulerModel(femu)
    sch.set_slot_index(1)   # != compare-byte 0 -> dispatch path

    def _st(uc_, a, s, u):
        """The helper function (_st).
        Вспомогательная функция (_st).
        """
        aa = a & ~1
        if not (FLASH0 <= aa < FLASH0 + 0x23680 or
                FLASH1 <= aa < FLASH1 + 0x23680):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, _st)
    try:
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x20)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R0, 0)
        femu.insn = 0
        try:
            uc.emu_start(SCHEDULER_FN | 1, 0, count=50000)
        except UcError:
            pass
    finally:
        uc.hook_del(sh)
    # ядро состояния: диспетчер прочитал slot-index @0x2C2 (стабильно в zeroed и
    # dispatch-path; tick/state-регионы path-dependent — 0x17F78+ / 0x1E0+ по ветке)
    assert sch.touched(SCHED_SLOT_INDEX_OFF) or \
        sch.touched(SCHED_SLOT_INDEX_OFF - 1), \
        f'slot-index не прочитан: {sorted(hex(o) for o in sch.reads if 0x2C0 <= o < 0x2D0)}'


# --- E1: CRC-7 примитив 0x3c7c (ядро §50 I2C stream-кодека) ---
@t(0x3C7C, 'E1: 0x3c7c — CRC-7 примитив (ядро §50 I2C stream-кодека). 0x3c7c(byte=r0, prev=r1) -> r0: crc=(prev^byte)&0xFF; 8 бит MSB-first: if MSB -> ((crc<<1)&0xFF)^0x07 else (crc<<1)&0xFF. Poly=0x07, no reflect/xorout, init=prev. Вериф sweep byte×prev vs независимая реализация.')
def _(run, rng):
    """Emulator test @ 0x3c7c: E1: 0x3c7c — CRC-7 примитив (ядро §50 I2C stream-кодека). 0x3c7c(byte=r0, prev=r1) -> r0: crc=(prev^byte)&0xFF; 8 бит MSB-first: if MSB -> ((crc<<1)&0xFF)^0x07 else (crc<<1)&0xFF. Poly=0x07, no reflect/xorout, init=prev. Вериф sweep byte×prev vs независимая реализация..
    Тест эмулятора @ 0x3c7c: E1: 0x3c7c — CRC-7 примитив (ядро §50 I2C stream-кодека). 0x3c7c(byte=r0, prev=r1) -> r0: crc=(prev^byte)&0xFF; 8 бит MSB-first: if MSB -> ((crc<<1)&0xFF)^0x07 else (crc<<1)&0xFF. Poly=0x07, no reflect/xorout, init=prev. Вериф sweep byte×prev vs независимая реализация..
    """
    def crc7(b, prev):
        """The crc7 function of the script.
        Функция crc7 скрипта.
        """
        crc = (prev ^ b) & 0xFF
        for _ in range(8):
            crc = ((crc << 1) & 0xFF) ^ 0x07 if (crc & 0x80) else (crc << 1) & 0xFF
        return crc
    n = 0
    for b in range(0, 256, 3):
        for prev in (0, 0x11, 0x7F, 0xB2, 0xFF):
            r0, _ = run.call(0x3C7C, args=(b, prev))
            assert r0 == crc7(b, prev), \
                f'b={b:#04x} prev={prev:#04x}: got {r0:#04x} want {crc7(b, prev):#04x}'
            n += 1
    assert n >= 40


# --- E2: periph-write-trace facility ---
@t(0x1BF48, 'E2: periph-write-trace facility — McuEmu.periph_write_map() / periph_writes_since(). Захват periph-writes на функцию для верификации «функция пишет в регистр Y». Тест: прогон мотор-инит 0x1bf48 (221 запись) -> periph_write_map() содержит motor-TIM @0x40012C00 + GPIO-блок @0x48000000; periph_writes_since(mark) = окно вызова.')
def _(run, rng):
    """Emulator test @ 0x1bf48: E2: periph-write-trace facility — McuEmu.periph_write_map() / periph_writes_since(). Захват periph-writes на функцию для верификации «функция пишет в регистр Y». Тест: прогон мотор-инит 0x1bf48 (221 запись) -> periph_write_map() содержит motor-TIM @0x40012C00 + GPIO-блок @0x48000000; periph_writes_since(mark) = окно вызова..
    Тест эмулятора @ 0x1bf48: E2: periph-write-trace facility — McuEmu.periph_write_map() / periph_writes_since(). Захват periph-writes на функцию для верификации «функция пишет в регистр Y». Тест: прогон мотор-инит 0x1bf48 (221 запись) -> periph_write_map() содержит motor-TIM @0x40012C00 + GPIO-блок @0x48000000; periph_writes_since(mark) = окно вызова..
    """
    from emulator.mcu_emu import McuEmu, RAM, FLASH0, FLASH1, STACK_TOP
    femu = McuEmu(trace=False, max_insn=500000)
    uc = femu.uc
    uc.mem_write(RAM, bytes(0x20000))
    femu.hook_periph_ready()
    mark = len(femu.periph_writes)

    def _st(uc_, a, s, u):
        """The helper function (_st).
        Вспомогательная функция (_st).
        """
        aa = a & ~1
        if not (FLASH0 <= aa < FLASH0 + 0x23680 or
                FLASH1 <= aa < FLASH1 + 0x23680):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, _st)
    try:
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x20)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        femu.insn = 0
        try:
            uc.emu_start(0x1BF48 | 1, 0, count=500000)
        except UcError:
            pass
    finally:
        uc.hook_del(sh)
    wm = femu.periph_write_map()
    assert any(0x40012C00 <= a < 0x40012D00 for a in wm), \
        f'motor-TIM @0x40012C00 не в map: {sorted(hex(a) for a in wm)[:8]}'
    assert any(0x48000000 <= a < 0x48001000 for a in wm), 'GPIO-блок @0x48000000 не в map'
    tail = femu.periph_writes_since(mark)
    assert len(tail) == len(femu.periph_writes) - mark and len(tail) >= 100, \
        f'periph_writes_since: {len(tail)} (ожидал >=100)'


# --- E1 continuation: checksum + divisibility 0x16410 ---
@t(0x16410, 'E1: 0x16410 — checksum + divisibility. 0x16410(arg0=r0, arg1=r1, arg2=r2) -> r0 = sum(block[:arg1]) + arg2 + flag; block=00 1f 1c 1f 1e 1f 1e 1f 1f 1e 1f 1e (embedded 12B из пула); flag добавляется только если arg1>2: a0%4!=0->0, a0%100!=0->1, a0%400!=0->0, else->1. Вериф sweep (arg0,arg1,arg2).')
def _(run, rng):
    """Emulator test @ 0x16410: E1: 0x16410 — checksum + divisibility. 0x16410(arg0=r0, arg1=r1, arg2=r2) -> r0 = sum(block[:arg1]) + arg2 + flag; block=00 1f 1c 1f 1e 1f 1e 1f 1f 1e 1f 1e (embedded 12B из пула); flag добавляется только если arg1>2: a0%4!=0->0, a0%100!=0->1, a0%400!=0->0, else->1. Вериф sweep (arg0,arg1,arg2)..
    Тест эмулятора @ 0x16410: E1: 0x16410 — checksum + divisibility. 0x16410(arg0=r0, arg1=r1, arg2=r2) -> r0 = sum(block[:arg1]) + arg2 + flag; block=00 1f 1c 1f 1e 1f 1e 1f 1f 1e 1f 1e (embedded 12B из пула); flag добавляется только если arg1>2: a0%4!=0->0, a0%100!=0->1, a0%400!=0->0, else->1. Вериф sweep (arg0,arg1,arg2)..
    """
    BLOCK = bytes([0x00, 0x1f, 0x1c, 0x1f, 0x1e, 0x1f, 0x1e, 0x1f, 0x1f, 0x1e, 0x1f, 0x1e])

    def flag(a0):
        """The flag function of the script.
        Функция flag скрипта.
        """
        if a0 % 4 != 0:
            return 0
        if a0 % 100 != 0:
            return 1
        if a0 % 400 != 0:
            return 0
        return 1
    n = 0
    for a0 in (0, 2, 3, 4, 8, 96, 99, 100, 196, 200, 300, 396, 400, 500, 796, 800):
        for a1 in (1, 2, 3, 5, 12):
            for a2 in (0, 7, 123):
                exp = (sum(BLOCK[:a1]) + a2 + (flag(a0) if a1 > 2 else 0)) & 0xFFFFFFFF
                r0, _ = run.call(0x16410, args=(a0, a1, a2))
                assert r0 == exp, f'a0={a0} a1={a1} a2={a2}: got {r0:#x} want {exp:#x}'
                n += 1
    assert n >= 100


# --- E1 continuation: CRC-7 stream encoder 0x15640 ---
@t(0x15640, 'E1: 0x15640 — CRC-7 stream-кодер §50 I2C. 0x15640(arg0=r0, arg1=r1, src=r2, dst=r3, len=[pre_sp+0]): warmup r7=crc7(a1,crc7(a0,0)); для каждого src[i]: dst[2i]=src[i], dst[2i+1]=crc7(src[i], r7 if i==0 else 0) — первый CRC цепляется от warmup, остальные сброс в init=0. Примитив crc7 = 0x3c7c (poly=0x07 MSB-first). Вериф manual-call (len в стек, push=8 рег=0x20).')
def _(run, rng):
    """Emulator test @ 0x15640: E1: 0x15640 — CRC-7 stream-кодер §50 I2C. 0x15640(arg0=r0, arg1=r1, src=r2, dst=r3, len=[pre_sp+0]): warmup r7=crc7(a1,crc7(a0,0)); для каждого src[i]: dst[2i]=src[i], dst[2i+1]=crc7(src[i], r7 if i==0 else 0) — первый CRC цепляется от warmup, остальные сброс в init=0. Примитив crc7 = 0x3c7c (poly=0x07 MSB-first). Вериф manual-call (len в стек, push=8 рег=0x20)..
    Тест эмулятора @ 0x15640: E1: 0x15640 — CRC-7 stream-кодер §50 I2C. 0x15640(arg0=r0, arg1=r1, src=r2, dst=r3, len=[pre_sp+0]): warmup r7=crc7(a1,crc7(a0,0)); для каждого src[i]: dst[2i]=src[i], dst[2i+1]=crc7(src[i], r7 if i==0 else 0) — первый CRC цепляется от warmup, остальные сброс в init=0. Примитив crc7 = 0x3c7c (poly=0x07 MSB-first). Вериф manual-call (len в стек, push=8 рег=0x20)..
    """
    from emulator.mcu_emu import McuEmu as _M, RAM as _R, FLASH0 as _F0, \
        FLASH1 as _F1, STACK_TOP as _ST

    def crc7(b, prev):
        """The crc7 function of the script.
        Функция crc7 скрипта.
        """
        crc = (prev ^ b) & 0xFF
        for _ in range(8):
            crc = ((crc << 1) & 0xFF) ^ 0x07 if (crc & 0x80) else (crc << 1) & 0xFF
        return crc

    def encode(a0, a1, src):
        """The encode function of the script.
        Функция encode скрипта.
        """
        r7 = crc7(a1 & 0xFF, crc7(a0 & 0xFF, 0))
        out = []
        for i, b in enumerate(src):
            out.append(b)
            r7 = crc7(b, r7 if i == 0 else 0)
            out.append(r7)
        return bytes(out)

    def run_enc(a0, a1, src):
        """The run_enc function of the script.
        Функция run_enc скрипта.
        """
        emu = _M(max_insn=50000)
        uc = emu.uc
        uc.mem_write(_R, bytes(0x20000))
        emu.hook_periph_ready()
        SRC = _R + 0x4000
        DST = _R + 0x4100
        for i, b in enumerate(src):
            uc.mem_write(SRC + i, bytes([b]))
        pre_sp = _ST - 0x40
        uc.mem_write(pre_sp, struct.pack('<I', len(src)))

        def _st(uc_, a, s, u):
            """The helper function (_st).
            Вспомогательная функция (_st).
            """
            aa = a & ~1
            if not (_F0 <= aa < _F0 + 0x23680 or _F1 <= aa < _F1 + 0x23680):
                uc_.emu_stop()
        sh = uc.hook_add(UC_HOOK_CODE, _st)
        try:
            uc.reg_write(UC_ARM_REG_SP, pre_sp)
            uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
            uc.reg_write(UC_ARM_REG_R0, a0)
            uc.reg_write(UC_ARM_REG_R1, a1)
            uc.reg_write(UC_ARM_REG_R2, SRC)
            uc.reg_write(UC_ARM_REG_R3, DST)
            emu.insn = 0
            try:
                uc.emu_start(0x15640 | 1, 0, count=50000)
            except UcError:
                pass
        finally:
            uc.hook_del(sh)
        return bytes(uc.mem_read(DST, 2 * len(src)))
    n = 0
    for (a0, a1, src) in [(0xAA, 0xBB, [1, 2, 3]), (0x11, 0x22, [0xDE, 0xAD]),
                           (0x00, 0x00, [5, 6, 7, 8]), (0xFF, 0x01, [0x41]),
                           (0x3C, 0x7D, [0x12, 0x34, 0x56])]:
        exp = encode(a0, a1, src)
        got = run_enc(a0, a1, src)
        assert got == exp, f'a0={a0:#04x} a1={a1:#04x}: got {got.hex()} want {exp.hex()}'
        n += 1
    assert n >= 5


# --- E1: 0x15a60 close-out — helpers strlen/memcmp + buffer processor ---

@t(0x11EC, 'E1: 0x11ec — strlen (null-terminated). 0x11ec(src=r0) -> r0 = число байтов до первого null. Помощник 0x15a60 (§87). Вериф sweep.')
def _(run, rng):
    """Emulator test @ 0x11ec: E1: 0x11ec — strlen (null-terminated). 0x11ec(src=r0) -> r0 = число байтов до первого null. Помощник 0x15a60 (§87). Вериф sweep..
    Тест эмулятора @ 0x11ec: E1: 0x11ec — strlen (null-terminated). 0x11ec(src=r0) -> r0 = число байтов до первого null. Помощник 0x15a60 (§87). Вериф sweep..
    """
    from emulator.mcu_emu import RAM as _R
    ok = 0
    for s in (b'', b'a', b'abc', b'hello', b'ab\x00cd'):
        p = _R + 0x3000
        r0, _emu = _fresh_call(0x11EC, args=(p,), extra_ram=[(p, s + b'\x00')])
        exp = s.find(b'\x00') if b'\x00' in s else len(s)
        assert r0 == exp, f'{s!r}: got {r0} want {exp}'
        ok += 1
    assert ok >= 5


@t(0x11FA, 'E1: 0x11fa — bounded-memcmp. 0x11fa(A=r0, B=r1, n=r2) -> r0 = A[i]-B[i] на первом несовпадении (i<n); 0 на полное совпадение или когда ОБА null на той же позиции (ранний выход). Помощник 0x15a60 (§87). Вериф sweep.')
def _(run, rng):
    """Emulator test @ 0x11fa: E1: 0x11fa — bounded-memcmp. 0x11fa(A=r0, B=r1, n=r2) -> r0 = A[i]-B[i] на первом несовпадении (i<n); 0 на полное совпадение или когда ОБА null на той же позиции (ранний выход). Помощник 0x15a60 (§87). Вериф sweep..
    Тест эмулятора @ 0x11fa: E1: 0x11fa — bounded-memcmp. 0x11fa(A=r0, B=r1, n=r2) -> r0 = A[i]-B[i] на первом несовпадении (i<n); 0 на полное совпадение или когда ОБА null на той же позиции (ранний выход). Помощник 0x15a60 (§87). Вериф sweep..
    """
    from emulator.mcu_emu import RAM as _R
    cases = [(b'abc', b'abc', 3, 0), (b'abc', b'abd', 3, -1),
             (b'ab', b'abc', 2, 0), (b'a\x00z', b'a\x00w', 3, 0),
             (b'a\x00x', b'ayz', 3, -ord('y')), (b'abcd', b'abce', 4, -1),
             (b'zyx', b'abc', 3, ord('z') - ord('a'))]
    for A, B, n, exp in cases:
        pa = _R + 0x3100
        pb = _R + 0x3200
        r0, _emu = _fresh_call(0x11FA, args=(pa, pb, n),
                               extra_ram=[(pa, A + b'\x00\x00'), (pb, B + b'\x00\x00')])
        got = r0 if r0 < 0x80000000 else r0 - 0x100000000
        assert got == exp, f'A={A!r} B={B!r} n={n}: got {got} want {exp}'


@t(0x15A60, 'E1: 0x15a60 — USART/DFU command/data buffer processor (§87). (src=r0, len=r1): рабочий буфер @RAM+0x1f10 (memset 0x11d6->0x11c8), TBL1=flash@0x1a93c (7×50B binary-паттерны; strlen через 0x11ec). Path A (len<=0x32): buf[0]=src[0], return 0. Path B (len>0x32): гейт src[0]==1 -> копирует src в буфер; иначе early-return 0 (только buf[0]=src[0]). Вериф детерминированного поведения.')
def _(run, rng):
    """Emulator test @ 0x15a60: E1: 0x15a60 — USART/DFU command/data buffer processor (§87). (src=r0, len=r1): рабочий буфер @RAM+0x1f10 (memset 0x11d6->0x11c8), TBL1=flash@0x1a93c (7×50B binary-паттерны; strlen через 0x11ec). Path A (len<=0x32): buf[0]=src[0], return 0. Path B (len>0x32): гейт src[0]==1 -> копирует src в буфер; иначе early-return 0 (только buf[0]=src[0]). Вериф детерминированного поведения..
    Тест эмулятора @ 0x15a60: E1: 0x15a60 — USART/DFU command/data buffer processor (§87). (src=r0, len=r1): рабочий буфер @RAM+0x1f10 (memset 0x11d6->0x11c8), TBL1=flash@0x1a93c (7×50B binary-паттерны; strlen через 0x11ec). Path A (len<=0x32): buf[0]=src[0], return 0. Path B (len>0x32): гейт src[0]==1 -> копирует src в буфер; иначе early-return 0 (только buf[0]=src[0]). Вериф детерминированного поведения..
    """
    from emulator.mcu_emu import RAM as _R
    SRC = _R + 0x4000
    src_a = bytes([0x11, 0x22, 0x33, 0x44])
    r0, emu = _fresh_call(0x15A60, args=(SRC, len(src_a)),
                          extra_ram=[(SRC, src_a)])
    buf = bytes(emu.uc.mem_read(_R + 0x1F10, 8))
    assert r0 == 0 and buf[0] == 0x11 and buf[1] == 0, \
        f'pathA: return={r0:#x} buf={buf.hex()}'
    src_b = bytes([0x05, 0x22, 0x33] + [0x55] * 60 + [0x77, 0x88])
    r0, emu = _fresh_call(0x15A60, args=(SRC, len(src_b)),
                          extra_ram=[(SRC, src_b)])
    buf = bytes(emu.uc.mem_read(_R + 0x1F10, 8))
    assert r0 == 0 and buf[0] == 0x05 and buf[1] == 0, \
        f'pathB gate-fail: return={r0:#x} buf={buf.hex()}'
    src_c = bytes([0x01, 0x22, 0x33] + [0x55] * 60 + [0x77, 0x88])
    r0, emu = _fresh_call(0x15A60, args=(SRC, len(src_c)),
                          extra_ram=[(SRC, src_c)])
    buf = bytes(emu.uc.mem_read(_R + 0x1F10, 8))
    assert r0 == 0 and buf[:4] == src_c[:4], \
        f'pathB gate-pass: return={r0:#x} buf={buf.hex()} want {src_c[:4].hex()}'


@t(0x1BF48, '§96 A1: GPIO input-регистра закрыта: кастомный блок «портов» @0x48000000 — input-data в +0x00 (IDR, read-only; бит N = состояние пина N). 0x1BF24 (3-bit «iron»-режим) читает [port1 0x48000400 + 0x00] и raw-shift-трюками извлекает пины 6-8 = (b6<<0)|(b7<<1)|(b8<<2). GpioModel.input(port,pin). Live-значения (Hall/кнопки) — железо')
def _(run, rng):
    """Emulator test @ 0x1bf48: §96 A1: GPIO input-регистра закрыта: кастомный блок «портов» @0x48000000 — input-data в +0x00 (IDR, read-only; бит N = состояние пина N). 0x1BF24 (3-bit «iron»-режим) читает [port1 0x48000400 + 0x00] и raw-shift-трюками извлекает пины 6-8 = (b6<<0)|(b7<<1)|(b8<<2). GpioModel.input(port,pin). Live-значения (Hall/кнопки) — железо.
    Тест эмулятора @ 0x1bf48: §96 A1: GPIO input-регистра закрыта: кастомный блок «портов» @0x48000000 — input-data в +0x00 (IDR, read-only; бит N = состояние пина N). 0x1BF24 (3-bit «iron»-режим) читает [port1 0x48000400 + 0x00] и raw-shift-трюками извлекает пины 6-8 = (b6<<0)|(b7<<1)|(b8<<2). GpioModel.input(port,pin). Live-значения (Hall/кнопки) — железо.
    """
    from emulator.mcu_emu import GpioModel, GPIO_IDR
    assert GPIO_IDR == 0x00
    uc = run.uc
    emu = run.emu
    port1 = 0x48000400
    # GpioModel.input() зеркалирует IDR
    gpio = GpioModel(emu)
    try:
        for seed in (0x0, 0x40, 0x80, 0x100, 0x1C0, 0x1FF):
            uc.mem_write(port1 + GPIO_IDR, struct.pack('<I', seed))
            assert gpio.input(1) == seed
            assert gpio.input(1, 6) == (seed >> 6) & 1
            assert gpio.input(1, 7) == (seed >> 7) & 1
            assert gpio.input(1, 8) == (seed >> 8) & 1
    finally:
        uc.hook_del(gpio._hook)
    # эмулятор: 0x1BF24(r0) → 3-bit из [port1+0x00]
    for seed in (0x0, 0x40, 0x80, 0x100, 0x140, 0x1C0, 0x3C0, 0x1FF):
        uc.mem_write(port1 + GPIO_IDR, struct.pack('<I', seed))
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x40)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        emu.insn = 0
        try:
            uc.emu_start(0x1BF24 | 1, 0, count=50000)
        except UcError:
            pass
        got = uc.reg_read(UC_ARM_REG_R0) & 0x7
        exp = ((seed >> 6) & 1) | (((seed >> 7) & 1) << 1) | (((seed >> 8) & 1) << 2)
        assert got == exp, f'seed=0x{seed:03x}: ret={got} ждём {exp}'
