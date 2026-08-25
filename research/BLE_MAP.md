# BLE_MAP — карта декомпиляции ble_2.7.0_0015.bin (по функциям)

Образ: `research/images/ble_2.7.0_0015.bin` (153890 Б = 153 890 Б), Realtek RTL8762C
(Cortex-M33), база флеша `0x01800000`. Файл = FOTA-пакет Mi Home побайтово (§42).

## 1. Region-карта (по энтропии + полям хедеров, §43.3)

| region | размер | статус | примечание |
|---|---|---|---|
| `0x0000..0x0400` | 1024 Б (0.7%) | разобран | полный decode: ctrl_flag, select=1 (SCEK+RTKCONST), exe_base RAM 0x203800 — §43.3 |
| `0x0400..0x3000` | 11264 Б (7.3%) | не начат | строки "Wrong Ctrl Header.", "dfuPacketWaitTimer"; функции ниже |
| `0x3000..0x5c00` | 11264 Б (7.3%) | шифр | load_len=11776 → RAM @0x203800; SWD-дамп RAM даст плейнтекст без ключа |
| `0x5c00..0x9ff4` | 17396 Б (11.3%) | не начат | функции ниже |
| `0x9ff4..0xa400` | 1036 Б (0.7%) | разобран | select=0 (SCEK), xip=1/enc=0 (флаги legacy) — §43.3 |
| `0xa400..0x2542d` | 110637 Б (71.9%) | шифр | ~110 КБ ciphertext; расшифровка только XIP/SWD |
| `0x2542d..0x25922` | 1269 Б (0.8%) | разобран | цепочка c1←c0←MijiaRoot верифицирована — §42, §44 |

**Ключевой факт:** 121901 Б (79.2%) — **шифр (per-chip SCEK из eFuse)**;
декомпиляция без SWD/XIP структурно ограничена ~21% файла. Протокол BLE-приложения реверсится по APK/плагинам,
не по этому образу (§35).

## 2. Функции PLAIN-регионов (детекция gen_functions.py)

Подтверждено: **170** функций, всего 22988 Б кода. Это низкоуровневый bootloader +
flash/OTA-драйвер; «говорящий» код — в зашифрованном APP-регионе (§62). Семантический
разбор PLAIN-кода: **1.2%** (взвешено по байтам; каталог ANALYZED_BLE, §63).

**Модель % декомпиляции:** разобран=100%, частично=50%, ID=25%, не начат=0%.

Перегенерация: `python research/scripts/gen_maps.py` (список функций — из
`functions_ble/README.md`; каталог — ANALYZED_BLE в gen_maps.py). Эмулятор: `emulator/ble_emu.py`.

| offset | vaddr | размер | регион | имя / роль | разделы | статус | % |
|---|---|---|---|---|---|---|---|
| [`0x00400`](functions_ble/func_0x00400.md) | `0x01800400` | 34 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x00438`](functions_ble/func_0x00438.md) | `0x01800438` | 146 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x004e0`](functions_ble/func_0x004e0.md) | `0x018004e0` | 32 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x00500`](functions_ble/func_0x00500.md) | `0x01800500` | 116 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x00592`](functions_ble/func_0x00592.md) | `0x01800592` | 84 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x005f8`](functions_ble/func_0x005f8.md) | `0x018005f8` | 68 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x0063c`](functions_ble/func_0x0063c.md) | `0x0180063c` | 98 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x0069e`](functions_ble/func_0x0069e.md) | `0x0180069e` | 476 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x0087a`](functions_ble/func_0x0087a.md) | `0x0180087a` | 80 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x008f4`](functions_ble/func_0x008f4.md) | `0x018008f4` | 70 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x0093a`](functions_ble/func_0x0093a.md) | `0x0180093a` | 60 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x00976`](functions_ble/func_0x00976.md) | `0x01800976` | 156 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x00a12`](functions_ble/func_0x00a12.md) | `0x01800a12` | 210 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x00ae4`](functions_ble/func_0x00ae4.md) | `0x01800ae4` | 156 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x00b80`](functions_ble/func_0x00b80.md) | `0x01800b80` | 30 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x00b9e`](functions_ble/func_0x00b9e.md) | `0x01800b9e` | 44 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x00bd4`](functions_ble/func_0x00bd4.md) | `0x01800bd4` | 52 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x00c08`](functions_ble/func_0x00c08.md) | `0x01800c08` | 52 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x00c3c`](functions_ble/func_0x00c3c.md) | `0x01800c3c` | 74 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x00c8c`](functions_ble/func_0x00c8c.md) | `0x01800c8c` | 92 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x00ce8`](functions_ble/func_0x00ce8.md) | `0x01800ce8` | 62 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x00d64`](functions_ble/func_0x00d64.md) | `0x01800d64` | 524 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x00f70`](functions_ble/func_0x00f70.md) | `0x01800f70` | 492 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x0115c`](functions_ble/func_0x0115c.md) | `0x0180115c` | 60 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x01198`](functions_ble/func_0x01198.md) | `0x01801198` | 20 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x011ac`](functions_ble/func_0x011ac.md) | `0x018011ac` | 20 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x011c0`](functions_ble/func_0x011c0.md) | `0x018011c0` | 236 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x012ac`](functions_ble/func_0x012ac.md) | `0x018012ac` | 174 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x0135a`](functions_ble/func_0x0135a.md) | `0x0180135a` | 164 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x013fe`](functions_ble/func_0x013fe.md) | `0x018013fe` | 464 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x015d0`](functions_ble/func_0x015d0.md) | `0x018015d0` | 562 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x0189e`](functions_ble/func_0x0189e.md) | `0x0180189e` | 46 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x018cc`](functions_ble/func_0x018cc.md) | `0x018018cc` | 162 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x0196e`](functions_ble/func_0x0196e.md) | `0x0180196e` | 34 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x01990`](functions_ble/func_0x01990.md) | `0x01801990` | 106 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x01b2a`](functions_ble/func_0x01b2a.md) | `0x01801b2a` | 218 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x01d34`](functions_ble/func_0x01d34.md) | `0x01801d34` | 28 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x01d50`](functions_ble/func_0x01d50.md) | `0x01801d50` | 26 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x01e20`](functions_ble/func_0x01e20.md) | `0x01801e20` | 22 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x01e38`](functions_ble/func_0x01e38.md) | `0x01801e38` | 60 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x01e74`](functions_ble/func_0x01e74.md) | `0x01801e74` | 66 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x01ee0`](functions_ble/func_0x01ee0.md) | `0x01801ee0` | 48 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x01f10`](functions_ble/func_0x01f10.md) | `0x01801f10` | 58 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x01f4a`](functions_ble/func_0x01f4a.md) | `0x01801f4a` | 110 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x02058`](functions_ble/func_0x02058.md) | `0x01802058` | 492 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x0228c`](functions_ble/func_0x0228c.md) | `0x0180228c` | 108 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x022f8`](functions_ble/func_0x022f8.md) | `0x018022f8` | 144 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x02388`](functions_ble/func_0x02388.md) | `0x01802388` | 78 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x023d8`](functions_ble/func_0x023d8.md) | `0x018023d8` | 20 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x023f0`](functions_ble/func_0x023f0.md) | `0x018023f0` | 106 | заголовок + bootloader | **CTR length-gate**: r1=кадр, r2=u16[r1+2]=длина. Доп. длины: {5} ∪ [0x12c..0x12e] (контрольный 5Б + data-кадры 300-302Б); остальные → return 0. Гейт: валидная длина → callee (0x2e24 для len==5, 0x2388/0x2e1a для data) — полная валидация = гейт+содержимое | §64 | частично | 50% |
| [`0x0245a`](functions_ble/func_0x0245a.md) | `0x0180245a` | 70 | заголовок + bootloader | **DFU event dispatcher**: арг (r1=тип события, r3=подсост). type==4&&[r3]==1 или type==2 → таймер: [base+0x1c0]×0x3e8(1000) → bl 0x2df2; type==4&&[r3]==3 → bl 0x2e2e. Управляет dfuPacketWaitTimer | §64 | частично | 50% |
| [`0x024a4`](functions_ble/func_0x024a4.md) | `0x018024a4` | 42 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x0256c`](functions_ble/func_0x0256c.md) | `0x0180256c` | 300 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x02698`](functions_ble/func_0x02698.md) | `0x01802698` | 110 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x02706`](functions_ble/func_0x02706.md) | `0x01802706` | 78 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x02754`](functions_ble/func_0x02754.md) | `0x01802754` | 46 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x02782`](functions_ble/func_0x02782.md) | `0x01802782` | 84 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x027d6`](functions_ble/func_0x027d6.md) | `0x018027d6` | 504 | заголовок + bootloader | — | — | не начат | 0% |
| [`0x06008`](functions_ble/func_0x06008.md) | `0x01806008` | 44 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x06034`](functions_ble/func_0x06034.md) | `0x01806034` | 44 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x06060`](functions_ble/func_0x06060.md) | `0x01806060` | 44 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x0608c`](functions_ble/func_0x0608c.md) | `0x0180608c` | 44 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x060b8`](functions_ble/func_0x060b8.md) | `0x018060b8` | 44 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x060e4`](functions_ble/func_0x060e4.md) | `0x018060e4` | 44 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x06110`](functions_ble/func_0x06110.md) | `0x01806110` | 16 | flash-драйвер / OTA-код | **SPIC base getter/init**: возвращает SPIC base (0x40080000), трогает ctrlr0 | §64 | ID | 25% |
| [`0x06120`](functions_ble/func_0x06120.md) | `0x01806120` | 118 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x061a2`](functions_ble/func_0x061a2.md) | `0x018061a2` | 38 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x061c8`](functions_ble/func_0x061c8.md) | `0x018061c8` | 112 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x06272`](functions_ble/func_0x06272.md) | `0x01806272` | 64 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x062ce`](functions_ble/func_0x062ce.md) | `0x018062ce` | 194 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x063a4`](functions_ble/func_0x063a4.md) | `0x018063a4` | 46 | flash-драйвер / OTA-код | **SPIC config**: [base+8]=0 → bl 0x639a → [base+8]=1; затем read-modify-write [r0+0x300] (SPIC-регистр, bic #0xff \| byte); r0=PERIPH base | §63 | частично | 50% |
| [`0x063d2`](functions_ble/func_0x063d2.md) | `0x018063d2` | 136 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x0645e`](functions_ble/func_0x0645e.md) | `0x0180645e` | 272 | flash-драйвер / OTA-код | **memory init/copy**: 22 RAM-writes, r0=RAM-указатель (0x2007fbb8); читает u16[base+8]; инициализация буфера/структуры | §63 | ID | 25% |
| [`0x06570`](functions_ble/func_0x06570.md) | `0x01806570` | 126 | flash-драйвер / OTA-код | **SPIC ctrl setup**: настраивает ctrlr0 (126Б) | §64 | ID | 25% |
| [`0x065f6`](functions_ble/func_0x065f6.md) | `0x018065f6` | 192 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x066b6`](functions_ble/func_0x066b6.md) | `0x018066b6` | 56 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x066ee`](functions_ble/func_0x066ee.md) | `0x018066ee` | 90 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x06748`](functions_ble/func_0x06748.md) | `0x01806748` | 18 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x067a8`](functions_ble/func_0x067a8.md) | `0x018067a8` | 74 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x067f2`](functions_ble/func_0x067f2.md) | `0x018067f2` | 184 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x068aa`](functions_ble/func_0x068aa.md) | `0x018068aa` | 210 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x0697c`](functions_ble/func_0x0697c.md) | `0x0180697c` | 150 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x06a12`](functions_ble/func_0x06a12.md) | `0x01806a12` | 170 | flash-драйвер / OTA-код | **SPIC op → RAM buffer**: ctrlr0, r0=RAM-указатель (0x2007fbe0); flash-операция с буфером (170Б) | §64 | ID | 25% |
| [`0x06abc`](functions_ble/func_0x06abc.md) | `0x01806abc` | 42 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x06ae6`](functions_ble/func_0x06ae6.md) | `0x01806ae6` | 548 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x06d0a`](functions_ble/func_0x06d0a.md) | `0x01806d0a` | 12 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x06d16`](functions_ble/func_0x06d16.md) | `0x01806d16` | 180 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x06dca`](functions_ble/func_0x06dca.md) | `0x01806dca` | 144 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x06e5a`](functions_ble/func_0x06e5a.md) | `0x01806e5a` | 140 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x06ee6`](functions_ble/func_0x06ee6.md) | `0x01806ee6` | 66 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x06f28`](functions_ble/func_0x06f28.md) | `0x01806f28` | 280 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07040`](functions_ble/func_0x07040.md) | `0x01807040` | 30 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07060`](functions_ble/func_0x07060.md) | `0x01807060` | 48 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07092`](functions_ble/func_0x07092.md) | `0x01807092` | 24 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x070f0`](functions_ble/func_0x070f0.md) | `0x018070f0` | 246 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x071e6`](functions_ble/func_0x071e6.md) | `0x018071e6` | 60 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07222`](functions_ble/func_0x07222.md) | `0x01807222` | 94 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07280`](functions_ble/func_0x07280.md) | `0x01807280` | 168 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07328`](functions_ble/func_0x07328.md) | `0x01807328` | 436 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x074de`](functions_ble/func_0x074de.md) | `0x018074de` | 64 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x0758c`](functions_ble/func_0x0758c.md) | `0x0180758c` | 152 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07634`](functions_ble/func_0x07634.md) | `0x01807634` | 168 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x076dc`](functions_ble/func_0x076dc.md) | `0x018076dc` | 146 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x0778c`](functions_ble/func_0x0778c.md) | `0x0180778c` | 132 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07810`](functions_ble/func_0x07810.md) | `0x01807810` | 54 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07848`](functions_ble/func_0x07848.md) | `0x01807848` | 34 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x078bc`](functions_ble/func_0x078bc.md) | `0x018078bc` | 68 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07900`](functions_ble/func_0x07900.md) | `0x01807900` | 142 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x0798e`](functions_ble/func_0x0798e.md) | `0x0180798e` | 122 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07a08`](functions_ble/func_0x07a08.md) | `0x01807a08` | 110 | flash-драйвер / OTA-код | **SPIC ctrl op**: ctrlr0, r0=0xffc00000 (110Б) | §64 | ID | 25% |
| [`0x07ac0`](functions_ble/func_0x07ac0.md) | `0x01807ac0` | 272 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07c24`](functions_ble/func_0x07c24.md) | `0x01807c24` | 10 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07c64`](functions_ble/func_0x07c64.md) | `0x01807c64` | 24 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07c7c`](functions_ble/func_0x07c7c.md) | `0x01807c7c` | 42 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07d0c`](functions_ble/func_0x07d0c.md) | `0x01807d0c` | 64 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07d4c`](functions_ble/func_0x07d4c.md) | `0x01807d4c` | 112 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07dc0`](functions_ble/func_0x07dc0.md) | `0x01807dc0` | 42 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x07dea`](functions_ble/func_0x07dea.md) | `0x01807dea` | 990 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x081c8`](functions_ble/func_0x081c8.md) | `0x018081c8` | 62 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x08206`](functions_ble/func_0x08206.md) | `0x01808206` | 70 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x0824c`](functions_ble/func_0x0824c.md) | `0x0180824c` | 96 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x082ac`](functions_ble/func_0x082ac.md) | `0x018082ac` | 204 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x08378`](functions_ble/func_0x08378.md) | `0x01808378` | 26 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x08408`](functions_ble/func_0x08408.md) | `0x01808408` | 88 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x08468`](functions_ble/func_0x08468.md) | `0x01808468` | 26 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x0848e`](functions_ble/func_0x0848e.md) | `0x0180848e` | 72 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x084f4`](functions_ble/func_0x084f4.md) | `0x018084f4` | 70 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x08588`](functions_ble/func_0x08588.md) | `0x01808588` | 846 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x088d6`](functions_ble/func_0x088d6.md) | `0x018088d6` | 164 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x089c6`](functions_ble/func_0x089c6.md) | `0x018089c6` | 172 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x08a72`](functions_ble/func_0x08a72.md) | `0x01808a72` | 250 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x08b6c`](functions_ble/func_0x08b6c.md) | `0x01808b6c` | 68 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x08bb6`](functions_ble/func_0x08bb6.md) | `0x01808bb6` | 68 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x08bfa`](functions_ble/func_0x08bfa.md) | `0x01808bfa` | 126 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x08c78`](functions_ble/func_0x08c78.md) | `0x01808c78` | 70 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x08cbe`](functions_ble/func_0x08cbe.md) | `0x01808cbe` | 102 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x08d24`](functions_ble/func_0x08d24.md) | `0x01808d24` | 124 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x08da0`](functions_ble/func_0x08da0.md) | `0x01808da0` | 130 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x08e5c`](functions_ble/func_0x08e5c.md) | `0x01808e5c` | 90 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x08eb6`](functions_ble/func_0x08eb6.md) | `0x01808eb6` | 172 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x08f62`](functions_ble/func_0x08f62.md) | `0x01808f62` | 258 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x09098`](functions_ble/func_0x09098.md) | `0x01809098` | 80 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x090e8`](functions_ble/func_0x090e8.md) | `0x018090e8` | 34 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x0910a`](functions_ble/func_0x0910a.md) | `0x0180910a` | 84 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x0915e`](functions_ble/func_0x0915e.md) | `0x0180915e` | 40 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x09186`](functions_ble/func_0x09186.md) | `0x01809186` | 28 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x091a2`](functions_ble/func_0x091a2.md) | `0x018091a2` | 86 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x09210`](functions_ble/func_0x09210.md) | `0x01809210` | 74 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x092a2`](functions_ble/func_0x092a2.md) | `0x018092a2` | 42 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x092cc`](functions_ble/func_0x092cc.md) | `0x018092cc` | 104 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x093a0`](functions_ble/func_0x093a0.md) | `0x018093a0` | 102 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x09480`](functions_ble/func_0x09480.md) | `0x01809480` | 132 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x09504`](functions_ble/func_0x09504.md) | `0x01809504` | 118 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x09592`](functions_ble/func_0x09592.md) | `0x01809592` | 26 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x095ac`](functions_ble/func_0x095ac.md) | `0x018095ac` | 206 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x0967a`](functions_ble/func_0x0967a.md) | `0x0180967a` | 64 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x096ba`](functions_ble/func_0x096ba.md) | `0x018096ba` | 58 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x096f4`](functions_ble/func_0x096f4.md) | `0x018096f4` | 398 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x09882`](functions_ble/func_0x09882.md) | `0x01809882` | 82 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x098d4`](functions_ble/func_0x098d4.md) | `0x018098d4` | 292 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x099f8`](functions_ble/func_0x099f8.md) | `0x018099f8` | 170 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x09b60`](functions_ble/func_0x09b60.md) | `0x01809b60` | 74 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x09baa`](functions_ble/func_0x09baa.md) | `0x01809baa` | 66 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x09bec`](functions_ble/func_0x09bec.md) | `0x01809bec` | 190 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x09caa`](functions_ble/func_0x09caa.md) | `0x01809caa` | 150 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x09d40`](functions_ble/func_0x09d40.md) | `0x01809d40` | 142 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x09dce`](functions_ble/func_0x09dce.md) | `0x01809dce` | 250 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x09ec8`](functions_ble/func_0x09ec8.md) | `0x01809ec8` | 132 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x09f4c`](functions_ble/func_0x09f4c.md) | `0x01809f4c` | 52 | flash-драйвер / OTA-код | — | — | не начат | 0% |
| [`0x09f80`](functions_ble/func_0x09f80.md) | `0x01809f80` | 488 | flash-драйвер / OTA-код | — | — | не начат | 0% |
