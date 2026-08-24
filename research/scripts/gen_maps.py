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
    (0x0799C, "регулятор duty (вырожден: выход ≈ -275 → 0%) + slot-3 state-machine", "§39, §41", "разобран"),
    (0x0E408, "slew-лимитер → u16@RAM[0x1357] (duty% = byte@0xFD3)", "§39, §41", "разобран"),
    (0x22A48, "блок TIM1+TIM3+TIM4 (HAL-функции, регистры +0x10)", "§39.1, §41", "разобран"),
    (0x22D2C, "HAL timer (доказательство раскладки +0x10)", "§39.1", "разобран"),
    (0x1E2F8, "RCC+GPIOC AF-конфиг (MODER=0x044AA200)", "§39", "частично"),
    (0x1BF48, "МОТОР-ИНИТ: bl 0x1d640/0x1c0b0/0x1c1ac/0x1bedc", "§39", "частично"),
    # --- диспетчер/режимы (§34.2, §39.5b, §40) ---
    (0x0E658, "round-robin диспетчер 6 задач (TBB @0xE684)", "§39.5b", "разобран"),
    (0x1D0C6, "state-машина режимов (byte@0x229: 2/3/0x0B) — адрес приблизительный", "§34.2", "частично"),
    (0x23374, "3-проводная шина режима (byte@0x26b ? bl 0x23374 : 0)", "§40.7", "частично"),
    # --- NVRAM/boot (§21, §25, §26) ---
    (0x1C838, "калибровка/секвенсор: @0xF400/+4 → @0x1e8/@0x1ec", "§25", "разобран"),
    (0x21A08, "NVRAM-save таск (гейт byte@0x170==1 + бит31 common+0x14)", "§25", "разобран"),
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
