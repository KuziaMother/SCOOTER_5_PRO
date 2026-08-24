#!/usr/bin/env python3
"""
gen_maps.py — генератор research/MCU_MAP.md и research/BLE_MAP.md.

Карта декомпиляции ПО ФУНКЦИЯМ:
  - список функций берётся из таблиц functions_mcu/README.md (678) и
    functions_ble/README.md (170) — канонический результат детекции
    gen_functions_mcu.py / gen_functions.py;
  - к каждой функции подвязан каталог разобранных блоков из REPORT.md
    (ANALYZED_MCU): имя, разделы, статус → % декомпиляции;
  - BLE: region-карта (§43.3) + все функции PLAIN-регионов.

Модель % (на функцию):
  100% — разобран: логика полностью декодирована и описана в REPORT.md
   50% — частично: роль/вход определены, часть логики декодирована
   25% — ID: адрес и роль известны только из контекста вызовов (xref)
    0% — не начат: есть только авто-дизассембляция в functions_*/

Общий % = Σ(size_i × pct_i) / Σ(size_i) (взвешено по байтам кода).

Запуск:  python research/scripts/gen_maps.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))   # research/scripts/
RES = os.path.dirname(HERE)                          # research/

# ----------------------------------------------------------------------
# каталог разобранных блоков MCU (REPORT.md §6..§45)
# (start, имя, разделы, статус) — start привязывается к содержащей функции
PCT = {'разобран': 100, 'частично': 50, 'ID': 25}
ANALYZED_MCU = [
    # --- «own»-handshake и шифры (§27, §36, §37) ---
    (0x21C64, "«own»: входной шифр/проверка кадра (initiator BLE)", "§36.3, §37", "разобран"),
    (0x1A7AC, "«own»: S-box-подстановка + перестановка (16 Б, 10 раундов)", "§37", "разобран"),
    (0x1A5F2, "«own»: трамплин bl 0x1bfa0 (из 0x1a628)", "§27.2, §37", "разобран"),
    (0x1A5FA, "«own»: XOR двух 16-Б блоков (round, вызов из 0x1a7ac; callers=3)", "§37", "разобран"),
    (0x1A5E6, "«own»: трамплин к S-box-блоку 0x1a7ac (реальный старт 0x1a5e4 `mov r2,r1` — без пролога, артефакт детекции; bl из 0x21c64)", "§36.3, §37", "разобран"),
    (0x1DD8C, "«own»: вспомогательный round (bl из 0x1a814)", "§37", "частично"),
    (0x1A628, "трамплин к шифру: ldr r0=&0x16aa; bl 0x1bfa0", "§27.2", "разобран"),
    (0x1BFA0, "табличный шифр (&table @0x16aa, src)", "§27.2", "разобран"),
    # --- USART3/UART4 ↔ BLE (§6.5-6.7, §28.3, §32) ---
    (0x1F600, "RX USART3: кольцо + диспетчер по таблице дескрипторов", "§6.7", "разобран"),
    (0x1E480, "ISR USART3 (линк к BLE-чипу): статус, сброс PE/FE/ORE", "§6.5", "разобран"),
    (0x1E9E0, "RX-парсер протокола USART3", "§6.5", "частично"),
    (0x1F6B4, "TX: сборка дескриптора [type=2][len][data]", "§6.5", "разобран"),
    (0x1F1CC, "MCU→BLE: сборщик запросов `63 CMD` (шаблон кадра)", "§32", "разобран"),
    (0x216E4, "TX-кольцо @0x10b5 отправитель (UART4)", "§28.3", "разобран"),
    (0x23188, "HAL_UART_Transmit (валидация порта/длины, assert)", "§6.5", "разобран"),
    (0x1302C, "init/драйвер трёх USART", "§6.5", "частично"),
    # --- агрегатор/телеметрия (§18, §22, §34) ---
    (0x1F71C, "агрегатор: 24-состоянная машина (jump-table по CTX[0x10])", "§22.5", "разобран"),
    (0x1D898, "батарея/запас хода/температура (0x306/0x30c/0x30e)", "§22", "разобран"),
    (0x1A938, "батарейные пороги (clamp 10..100)", "§22", "частично"),
    (0x1B67C, "флаги/статус: перегрев ≥46°C → флаг @0x318", "§22", "разобран"),
    (0x1BB1C, "батарейный замер №2 (struct @0x154)", "§25.4", "разобран"),
    # --- ADC (§22, §40) ---
    (0x1A31C, "ADC1: стейт-машина выборки (системный тик ~1 кГц)", "§22, §40", "разобран"),
    (0x1E298, "DMA+ADC (вызов из 0x1a31c)", "§40", "частично"),
    (0x1D3D0, "хвост ADC ISR: → TX → SWSTART", "§22.6", "разобран"),
    (0x1C0B0, "инициализация сенсоров ADC1", "§40", "ID"),
    (0x21CA8, "инициализация сенсоров ADC1", "§40", "ID"),
    # --- мотор (§39, §41) ---
    (0x0799C, "регулятор duty (вырожден: выход ≈ -275 → 0%)", "§39, §41", "разобран"),
    (0x07A30, "slot-3 state-machine мотора (TBB @0x7AA4)", "§39, §41", "разобран"),
    (0x0E408, "slew-лимитер → u16@RAM[0x1357] (duty% = byte@0xFD3)", "§39, §41", "разобран"),
    (0x22A48, "блок TIM1+TIM3+TIM4 (HAL-функции, регистры +0x10)", "§39.1, §41", "разобран"),
    (0x22D2C, "HAL timer (доказательство раскладки +0x10)", "§39.1", "разобран"),
    (0x1E2F8, "RCC+GPIOC AF-конфиг (MODER=0x044AA200)", "§39", "частично"),
    (0x1BF48, "МОТОР-ИНИТ: bl 0x1d640/0x1c0b0/0x1c1ac/0x1bedc", "§39", "частично"),
    # --- диспетчер/режимы (§34.2, §39.5b, §40) ---
    (0x0E658, "round-robin диспетчер 6 задач (TBB @0xE684)", "§39.5b", "разобран"),
    (0x1D0C6, "state-машина режимов (byte@0x229: 2/3/0x0B) — адрес приблизительный", "§34.2", "частично"),
    (0x23374, "3-проводная шина режима (byte@0x26b ? bl 0x23374 : 0)", "§40.7", "частично"),
    # --- телеметрия MCU→BLE (§47) ---
    (0x211F8, "сборщик кадров 'a'/'a1' в TX-кольцо @0x10b5 (state byte@0x18A: 0→1→2→0; рейт-лимиты 1920/3200 тиков)", "§47", "разобран"),
    (0x1DFD8, "периодический таск: флаги → счётчик → сборщик 'a'-кадров 0x211f8", "§47", "частично"),
    # --- NVRAM/boot (§21, §25, §26) ---
    (0x1C838, "калибровка/секвенсор: @0xF400/+4 → @0x1e8/@0x1ec", "§25", "разобран"),
    (0x21A08, "NVRAM-save таск (гейт byte@0x170==1 + бит31 common+0x14)", "§25", "разобран"),
    # --- мелкие функции ≤12 Б: getters/setters/периферия (§48) ---
    (0x6378, "FLASH unlock: magic-ключи 0x45670123/0xCDEF89AB → FLASH_KEYR @0x40022004", "§48", "разобран"),
    (0x61D4, "FLASH_SR @0x4002200C |= r0 — сброс флагов (caller OTA-код 0x06230)", "§48", "разобран"),
    (0xC894, "(RCC_CFGR0 @0x40021004) & 0xC — биты AHB-прескалера", "§48", "разобран"),
    (0x5970, "запись r0 в регистр @0x40010414 (зона AFIO; EXTI-mapping?)", "§48", "разобран"),
    (0xB854, "запись 0x10000 в struct+0x108 (caller: struct@RAM[0xdd8])", "§48", "разобран"),
    (0x1F1C0, "setter USART3+4 (вызов из TX-кольца 0x1F600)", "§48", "разобран"),
    (0x211EC, "setter UART4+4 (вызов из TX-кольца 0x216E4)", "§48", "разобран"),
    (0x99F0, "запись 0xAAAA в @0x40003000 (кластер драйвера)", "§48", "разобран"),
    (0x99E0, "запись 0xCCCC в @0x40003000", "§48", "разобран"),
    (0x5CC0, "запись 0xAAAA в @0x40003000 (дубль 0x99f0)", "§48", "разобран"),
    (0x9A0C, "запись r0 в @0x40003000", "§48", "разобран"),
    (0x9A00, "запись r0 в @0x40003000+4", "§48", "разобран"),
    (0x99D4, "запись r0 в @0x40003000+8", "§48", "разобран"),
    (0x833C, "getter byte@RAM[0xC8D] — флаг инициализации 0x8xxx-драйвера", "§48", "разобран"),
    (0x8348, "one-time init (флаг byte@0xC8D==0): GPIOA + SPI1-команда 0xB9 + delay (продолжение — 0x8352)", "§48", "разобран"),
    (0x8468, "guard: return если byte@0xC8D≠0 (вариант №2, паттерн как 0x8348)", "§48", "разобран"),
    (0x82F0, "guard: return если byte@0xC8D≠0 (r4-варинт; callers 0xd878/0x119e4/0x147ac)", "§48", "разобран"),
    (0x87E2, "условный setter: r2 ? *(r0+0x18) : *(r0+0x28) = r1", "§48", "разобран"),
    (0x123C0, "запись 0x10000 в struct@RAM[0xdd8]+0x108 (через 0xb854)", "§48", "разобран"),
    (0x1A5C4, "ADC1+0x18 |= 8 (bit3; caller — ADC-таск 0x1A31C)", "§48", "разобран"),
    (0x1A5D4, "ADC1+0x18 |= 0x20 (bit5; caller — DMA+ADC 0x1E298)", "§48", "разобран"),
    (0x87DE, "setter +0x18 (в init: GPIOA+0x18 = 0x10)", "§48", "разобран"),
    (0x1072A, "getter u16 @+0xc (ldrh)", "§48", "разобран"),
    (0x10730, "setter u16 @+0xc (strh)", "§48", "разобран"),
    (0x99CE, "setter u16 @+0x10 (strh)", "§48", "разобран"),
    (0x99B4, "getter byte из u16@+0x10 (uxtb ldrh)", "§48", "разобран"),
    (0x4F50, "getter u16 @+4 (uxth)", "§48", "разобран"),
    (0x4E38, "setter +4 (str r0,[r1,#4])", "§48", "разобран"),
    (0x4FBA, "setter +4 (str r1,[r0,#4])", "§48", "разобран"),
    (0x4FAC, "условный setter *[r2+0x10] = (r3 ? r0 : 0)", "§48", "разобран"),
    (0x7FD4, "getter byte (ldrb r0,[r0])", "§48", "разобран"),
    (0x8878, "getter byte@RAM[0x128]", "§48", "разобран"),
    (0x8AF0, "getter byte@RAM[0xA73]", "§48", "разобран"),
    (0x8D90, "getter u32@RAM[0x1344]", "§48", "разобран"),
    (0x8E14, "getter byte@RAM[0x1378] (@0x1359+0x1f)", "§48", "разобран"),
    (0xA6A4, "getter byte@RAM[0x40]", "§48", "разобран"),
    (0xE3E4, "setter u16 = 0 (strh #0,[r0])", "§48", "разобран"),
    (0x21C0C, "getter *(u32@RAM[0x28])+4 (двойная индирекция)", "§48", "разобран"),
    (0x8A44, "getter *(u32@RAM[0xF64])+6", "§48", "разобран"),
    (0xC6F0, "запись в 0x42420060 — несуществующий адрес (dead code?)", "§48", "ID"),
    # --- мелкие функции: thunk/обёртки (§48) ---
    (0x1DEC, "thunk → 0x29e8", "§48", "ID"),
    (0x2D14, "thunk → 0x9678", "§48", "ID"),
    (0x4E28, "thunk → 0x5000", "§48", "ID"),
    (0x4E30, "thunk → 0x4fc0", "§48", "ID"),
    (0x9A18, "thunk → 0x99f0 (запись 0xAAAA в @0x40003000)", "§48", "ID"),
    (0xCE68, "thunk → 0x3168", "§48", "ID"),
    (0x10780, "thunk → 0x10788", "§48", "ID"),
    (0x10A20, "thunk → 0x112bc", "§48", "ID"),
    (0x11CAC, "thunk → 0x4c14", "§48", "ID"),
    (0x12FD0, "thunk → 0x12b50", "§48", "ID"),
    (0x12FD8, "thunk → 0x12d90", "§48", "ID"),
    (0x395C, "thunk → 0xd298(r0=0)", "§48", "ID"),
    (0x3966, "thunk → 0xd298(r0=1) (пара с 0x395c: off/on)", "§48", "ID"),
    (0x3B20, "thunk → 0x1bdc(r0=0x9a)", "§48", "ID"),
    (0x5B8C, "thunk → 0x4de0", "§48", "ID"),
    (0x110F0, "thunk → 0x5b8c(r0=0)", "§48", "ID"),
    (0x1ABC, "последовательность: 0x1a68 + 0x19f4", "§48", "ID"),
    (0x1CEA, "последовательность: 0x1fe0 + 0x20d8", "§48", "ID"),
    (0x36F4, "последовательность: 0x10900 + 0x3b00", "§48", "ID"),
    (0x9482, "последовательность: 0x9134 + 0x9480", "§48", "ID"),
    (0x9F64, "последовательность: 0x9b44 + 0x9f70", "§48", "ID"),
    (0xBF4C, "последовательность: 0xd878 + 0xddc4", "§48", "ID"),
    (0xC200, "thunk → 0x9f64 (r3=1)", "§48", "ID"),
    (0x11668, "thunk → 0x10e5c", "§48", "ID"),
    (0x11888, "thunk → 0x10f18", "§48", "ID"),
    # --- артефакты детекции в регионе 0x17xxx (§48) ---
    (0x177D6, "cold-tail гигантской функции региона 0x17xxx (b #0x173bc); артефакт детекции", "§48", "ID"),
    (0x178C4, "dead-фрагмент: после strh — НЕВАЛИДНАЯ инструкция 0x6EF5 (Unicorn: UC_ERR_INSN_INVALID); перед ним u16-таблица @0x177DE; дыра 0x177DE..0x19A1C = одна гигантская функция, пропущенная каноническим детектором", "§48", "ID"),
]

# ----------------------------------------------------------------------
# парсинг таблиц README
ROW = re.compile(r'^\|\s*\[`0x([0-9a-f]+)`\]\(func_0x[0-9a-f]+\.md\)\s*\|(.+)\|$')

def parse_readme(path, has_vaddr):
    """→ [(offset, size, region)]"""
    out = []
    for line in open(path, encoding='utf-8'):
        m = ROW.match(line.strip())
        if not m:
            continue
        off = int(m.group(1), 16)
        cells = [c.strip() for c in m.group(2).split('|')]
        # cells: [size, region, strings, callers]  или  [vaddr, size, region, strings, callers]
        if has_vaddr:
            size, region = int(cells[1]), cells[2]
        else:
            size, region = int(cells[0]), cells[1]
        out.append((off, size, region))
    return out

def attach_catalog(funcs, catalog):
    """funcs: [(off, size, region)] → dict off → (имя|None, разделы|None, статус|None)"""
    att = {}
    for off, size, region in funcs:
        end = off + size
        hits = [(s, n, sec, st) for s, n, sec, st in catalog if off <= s < end]
        if hits:
            # несколько подблоков в одной функции — объединить
            names = '; '.join(h[1] for h in hits)
            secs = ', '.join(dict.fromkeys(h[2] for h in hits))
            best = max(hits, key=lambda h: PCT[h[3]])
            att[off] = (names, secs, best[3])
        else:
            att[off] = (None, None, None)
    return att

def stats(funcs, att):
    n = len(funcs)
    total = sum(s for _, s, _ in funcs)
    by = {}
    for off, size, _ in funcs:
        st = att[off][2] or 'не начат'
        c, b = by.get(st, (0, 0))
        by[st] = (c + 1, b + size)
    wsum = sum(s * PCT[att[off][2]] for off, s, _ in funcs if att[off][2])
    return n, total, by, (wsum / total if total else 0.0)

def write_mcu(path):
    funcs = parse_readme(os.path.join(RES, 'functions_mcu', 'README.md'), has_vaddr=False)
    att = attach_catalog(funcs, ANALYZED_MCU)
    n, total, by, pct = stats(funcs, att)

    L = []
    A = L.append
    A("# MCU_MAP — карта декомпиляции mcu_0007.bin (по функциям)")
    A("")
    A(f"Образ: `research/images/mcu_0007.bin` (150 841 Б), Cortex-M4F, **не зашифрован**.")
    A(f"Функций подтверждено детекцией: **{n}**; байт кода в функциях: **{total}** ({total/1024:.1f} КБ из ~132.6 КБ")
    A("code-секций A–J; остальное — literal-пулы и данные между функциями).")
    A("")
    A("**Модель % декомпиляции (на функцию):**")
    A("")
    A("| % | статус | смысл |")
    A("|---|---|---|")
    A("| 100% | разобран | логика полностью декодирована и описана в REPORT.md |")
    A("| 50% | частично | роль/вход определены, часть логики декодирована |")
    A("| 25% | ID | адрес и роль известны только из контекста вызовов (xref) |")
    A("| 0% | не начат | есть только авто-дизассембляция в `functions_mcu/func_0x*.md` |")
    A("")
    A("**Итог (взвешено по байтам кода):**")
    A("")
    A("| статус | функций | байт | % байт |")
    A("|---|---|---|---|")
    for st in ('разобран', 'частично', 'ID', 'не начат'):
        if st in by:
            c, b = by[st]
            A(f"| {st} | {c} | {b} | {100.0*b/total:.1f}% |")
    A(f"| **всего** | **{n}** | **{total}** | **{pct:.1f}% декомпилировано** |")
    A("")
    A("Подробности по каждой функции: `functions_mcu/func_0x<off>.md` (дизассембляция,")
    A("литералы, callees/callers). Разделы REPORT.md — где описана семантика.")
    A("")
    A("Перегенерация: `python research/scripts/gen_maps.py` (список функций — из")
    A("`functions_mcu/README.md`; каталог разобранных блоков — в gen_maps.py, ANALYZED_MCU).")
    A("")
    A("| offset | размер | регион | имя / роль | разделы | статус | % |")
    A("|---|---|---|---|---|---|---|")
    for off, size, region in funcs:
        name, secs, st = att[off]
        if st:
            A(f"| [`0x{off:05x}`](functions_mcu/func_0x{off:05x}.md) | {size} | {region} | {name} | {secs} | {st} | {PCT[st]}% |")
        else:
            A(f"| [`0x{off:05x}`](functions_mcu/func_0x{off:05x}.md) | {size} | {region} | — | — | не начат | 0% |")
    A("")
    A("**Известные артефакты детекции (ручная перепроверка 2026-08-24):** строка `0x1a5e6` —")
    A("тело функции, реально начинающейся в `0x1a5e4` (`mov r2,r1`, без push-пролога — детектор")
    A("ловит внутренний push); это «own»-трамплин 0x21c64→0x1a5e4→0x1a7ac. Всё остальное из")
    A("именованных функций сверено с дизассембляцией входов и разделами REPORT.md.")
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))
    print(f"MCU_MAP.md: функций {n}, байт {total}, декомпилировано {pct:.1f}%")

# ----------------------------------------------------------------------
# BLE: region-карта (§43.3) + функции PLAIN-регионов
BLE_TOTAL = 0x25922
BLE_REGIONS = [
    # (start, end, имя, статус, примечание)
    (0x0000, 0x0400, "RomPatch-хедер (1 КБ)", "разобран", "полный decode: ctrl_flag, select=1 (SCEK+RTKCONST), exe_base RAM 0x203800 — §43.3"),
    (0x0400, 0x3000, "PLAIN-код #1: bootloader + DFU", "не начат", "строки \"Wrong Ctrl Header.\", \"dfuPacketWaitTimer\"; функции ниже"),
    (0x3000, 0x5C00, "RomPatch «load» (ШИФР, SCEK+RTKCONST)", "шифр", "load_len=11776 → RAM @0x203800; SWD-дамп RAM даст плейнтекст без ключа"),
    (0x5C00, 0x9FF4, "PLAIN-код #2: flash/OTA-драйвер", "не начат", "функции ниже"),
    (0x9FF4, 0xA400, "AppPatch-хедер (~1 КБ)", "разобран", "select=0 (SCEK), xip=1/enc=0 (флаги legacy) — §43.3"),
    (0xA400, 0x2542D, "AppPatch payload (ШИФР, SCEK)", "шифр", "~110 КБ ciphertext; расшифровка только XIP/SWD"),
    (0x2542D, BLE_TOTAL, "FOTA-трейлер: PEM + ECDSA-SHA256", "разобран", "цепочка c1←c0←MijiaRoot верифицирована — §42, §44"),
]

def write_ble(path):
    funcs = parse_readme(os.path.join(RES, 'functions_ble', 'README.md'), has_vaddr=True)
    att = attach_catalog(funcs, [])   # BLE-функции семантически не разбирались
    n, total, by, pct = stats(funcs, att)

    L = []
    A = L.append
    A("# BLE_MAP — карта декомпиляции ble_2.7.0_0015.bin (по функциям)")
    A("")
    A(f"Образ: `research/images/ble_2.7.0_0015.bin` ({BLE_TOTAL} Б = 153 890 Б), Realtek RTL8762C")
    A("(Cortex-M33), база флеша `0x01800000`. Файл = FOTA-пакет Mi Home побайтово (§42).")
    A("")
    A("## 1. Region-карта (по энтропии + полям хедеров, §43.3)")
    A("")
    A("| region | размер | статус | примечание |")
    A("|---|---|---|---|")
    for s, e, name, st, note in BLE_REGIONS:
        A(f"| `{s:#06x}..{e:#06x}` | {e-s} Б ({100.0*(e-s)/BLE_TOTAL:.1f}%) | {st} | {note} |")
    enc = sum(e - s for s, e, _, st, _ in BLE_REGIONS if st == 'шифр')
    plain_code = sum(e - s for s, e, _, st, _ in BLE_REGIONS if st == 'не начат')
    done = sum(e - s for s, e, _, st, _ in BLE_REGIONS if st == 'разобран')
    A("")
    A(f"**Ключевой факт:** {enc} Б ({100.0*enc/BLE_TOTAL:.1f}%) — **шифр (per-chip SCEK из eFuse)**;")
    A("декомпиляция без SWD/XIP структурно ограничена ~"
      f"{100.0*(BLE_TOTAL-enc)/BLE_TOTAL:.0f}% файла. Протокол BLE-приложения реверсится по APK/плагинам,")
    A("не по этому образу (§35).")
    A("")
    A("## 2. Функции PLAIN-регионов (детекция gen_functions.py)")
    A("")
    A(f"Подтверждено: **{n}** функций, всего {total} Б кода. Семантический разбор — **0%**")
    A("(есть только авто-дизассембляция в `functions_ble/func_0x*.md`); это низкоуровневый")
    A("bootloader + flash/OTA-драйвер, «говорящий» код — в зашифрованном APP-регионе.")
    A("")
    A("Перегенерация: `python research/scripts/gen_maps.py` (список функций — из")
    A("`functions_ble/README.md`).")
    A("")
    A("| offset | vaddr | размер | регион | статус | % |")
    A("|---|---|---|---|---|---|")
    for off, size, region in funcs:
        A(f"| [`0x{off:05x}`](functions_ble/func_0x{off:05x}.md) | `0x{0x01800000+off:08x}` | {size} | {region} | не начат | 0% |")
    A("")
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))
    print(f"BLE_MAP.md: функций {n}, байт кода {total}; шифр {enc} Б ({100.0*enc/BLE_TOTAL:.1f}%)")

if __name__ == '__main__':
    write_mcu(os.path.join(RES, 'MCU_MAP.md'))
    write_ble(os.path.join(RES, 'BLE_MAP.md'))
