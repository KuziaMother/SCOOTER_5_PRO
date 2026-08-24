# MCU_MAP — карта декомпиляции mcu_0007.bin (по функциям)

Образ: `research/images/mcu_0007.bin` (150 841 Б), Cortex-M4F, **не зашифрован**.
Функций подтверждено детекцией: **678**; байт кода в функциях: **96932** (94.7 КБ из ~132.6 КБ
code-секций A–J; остальное — literal-пулы и данные между функциями).

**Модель % декомпиляции (на функцию):**

| % | статус | смысл |
|---|---|---|
| 100% | разобран | логика полностью декодирована и описана в REPORT.md |
| 50% | частично | роль/вход определены, часть логики декодирована |
| 25% | ID | адрес и роль известны только из контекста вызовов (xref) |
| 0% | не начат | есть только авто-дизассембляция в `functions_mcu/func_0x*.md` |

**Итог (взвешено по байтам кода):**

| статус | функций | байт | % байт |
|---|---|---|---|
| разобран | 336 | 27324 | 28.2% |
| частично | 10 | 6964 | 7.2% |
| ID | 29 | 862 | 0.9% |
| не начат | 303 | 61782 | 63.7% |
| **всего** | **678** | **96932** | **32.0% декомпилировано** |

Подробности по каждой функции: `functions_mcu/func_0x<off>.md` (дизассембляция,
литералы, callees/callers). Разделы REPORT.md — где описана семантика.

Перегенерация: `python research/scripts/gen_maps.py` (список функций — из
`functions_mcu/README.md`; каталог разобранных блоков — в gen_maps.py, ANALYZED_MCU).

| offset | размер | регион | имя / роль | разделы | статус | % |
|---|---|---|---|---|---|---|
| [`0x01218`](functions_mcu/func_0x01218.md) | 34 | код A | abs(r0) → 0x12aa(0, 0, 0x433) | §49 | разобран | 100% |
| [`0x0123e`](functions_mcu/func_0x0123e.md) | 46 | код A | range [0x3FF..0x433]: r1&0x3FFF|0x100000; зона → asr(r2-0x433); иначе lsl(r2-0x433) | §49 | разобран | 100% |
| [`0x0126c`](functions_mcu/func_0x0126c.md) | 32 | код A | u32 lsl на r1 битов (r1<32) | §49 | разобран | 100% |
| [`0x0128c`](functions_mcu/func_0x0128c.md) | 30 | код A | u64 add (r0:r1 + r2:r3) | §49 | разобран | 100% |
| [`0x012aa`](functions_mcu/func_0x012aa.md) | 156 | код A | — | — | не начат | 0% |
| [`0x01346`](functions_mcu/func_0x01346.md) | 322 | код A | — | — | не начат | 0% |
| [`0x01494`](functions_mcu/func_0x01494.md) | 48 | код A | сравнение signed u64 (r0:r1) vs (r2:r3) | §49 | разобран | 100% |
| [`0x0152a`](functions_mcu/func_0x0152a.md) | 86 | код A | — | — | не начат | 0% |
| [`0x01580`](functions_mcu/func_0x01580.md) | 26 | код A | RCC-расширенный инициал: r5==0 → 0xc490(0x100)+0xc478(r4); иначе 0xc4b0/0xc4c8 | §49 | разобран | 100% |
| [`0x015aa`](functions_mcu/func_0x015aa.md) | 198 | код A | — | — | не начат | 0% |
| [`0x01670`](functions_mcu/func_0x01670.md) | 86 | код A | — | — | не начат | 0% |
| [`0x016d4`](functions_mcu/func_0x016d4.md) | 42 | код A | **DMA1 reset**: 0x1940(); DMA on; цикл i<2: 0x4e50(0x40020030); byte@0xB82=0 | §49 | разобран | 100% |
| [`0x0170c`](functions_mcu/func_0x0170c.md) | 68 | код A | — | — | не начат | 0% |
| [`0x0175c`](functions_mcu/func_0x0175c.md) | 42 | код A | **DMA1 enable**: 0x1940(); цикл i<2: 0x1858(i) (рег. обработчика), 0x1670(), 0x18fc(i) (конфиг канала); byte@0xB82=1 | §49 | разобран | 100% |
| [`0x0178c`](functions_mcu/func_0x0178c.md) | 98 | код A | — | — | не начат | 0% |
| [`0x017f4`](functions_mcu/func_0x017f4.md) | 28 | код A | вкл/выкл DMA (база 0x40020800) через 0xc644 | §49 | разобран | 100% |
| [`0x01858`](functions_mcu/func_0x01858.md) | 40 | код A | регистратор обработчика: запись в таблицу @0x1A8D0 (индекс r0) | §49 | разобран | 100% |
| [`0x018b0`](functions_mcu/func_0x018b0.md) | 66 | код A | — | — | не начат | 0% |
| [`0x018fc`](functions_mcu/func_0x018fc.md) | 60 | код A | **DMA1-канал**: struct {1,1,0xE0000,0,2} → 0x18b0(DMA1); таблица @0x1A8D0 (шаг 8) + 0x15aa | §49 | разобран | 100% |
| [`0x01940`](functions_mcu/func_0x01940.md) | 52 | код A | **RCC-инициал расширенных регистров**: AWDCR|=1, BDCR|=0xE|0x1000, 0x1580(2,0) | §49 | разобран | 100% |
| [`0x01984`](functions_mcu/func_0x01984.md) | 102 | код A | — | — | не начат | 0% |
| [`0x019f4`](functions_mcu/func_0x019f4.md) | 100 | код A | — | — | не начат | 0% |
| [`0x01a68`](functions_mcu/func_0x01a68.md) | 70 | код A | — | — | не начат | 0% |
| [`0x01abc`](functions_mcu/func_0x01abc.md) | 12 | код A | последовательность: 0x1a68 + 0x19f4 | §48 | ID | 25% |
| [`0x01ac8`](functions_mcu/func_0x01ac8.md) | 268 | код A | — | — | не начат | 0% |
| [`0x01bdc`](functions_mcu/func_0x01bdc.md) | 42 | код A | **I2C2 read**: {code16, len=2} → 0x1e72(op=8, dev=0x3E) — чтение регистра чипа I2C2 | §49 | разобран | 100% |
| [`0x01c1c`](functions_mcu/func_0x01c1c.md) | 42 | код A | **I2C2 read**: {code16, len=2} → 0x90a0(base=0x40005800) — чтение регистра чипа I2C2 | §49 | разобран | 100% |
| [`0x01c60`](functions_mcu/func_0x01c60.md) | 26 | код A | I2C2-цепочка #1: → 0x1e52 → 0x214c → 0x8f7c(I2C2=0x40005800) | §49 | разобран | 100% |
| [`0x01c7a`](functions_mcu/func_0x01c7a.md) | 52 | код A | I2C2 read: буфер {u16=0, len=2, addr=0x3E} → 0x1e72; результат → u16@0xF95+0x1E | §49 | разобран | 100% |
| [`0x01cea`](functions_mcu/func_0x01cea.md) | 12 | код A | последовательность: 0x1fe0 + 0x20d8 | §48 | ID | 25% |
| [`0x01cf6`](functions_mcu/func_0x01cf6.md) | 54 | код A | init-подблок: 0x1d06(1) + 0x1d1e(1) | §49 | разобран | 100% |
| [`0x01d78`](functions_mcu/func_0x01d78.md) | 112 | код A | — | — | не начат | 0% |
| [`0x01dec`](functions_mcu/func_0x01dec.md) | 8 | код A | thunk → 0x29e8 | §48 | ID | 25% |
| [`0x01df4`](functions_mcu/func_0x01df4.md) | 64 | код A | **мега-инициал**: 15 последовательных bl (0x3b2a, 0x36f4, 0xced0, 0x9b44, 0x9f70, 0xc098, 0x11978, 0x119c4, 0x3034, 0x1cf6, ...) | §49 | разобран | 100% |
| [`0x01e34`](functions_mcu/func_0x01e34.md) | 30 | код A | сумма массива байтов (u8) | §49 | разобран | 100% |
| [`0x01e52`](functions_mcu/func_0x01e52.md) | 32 | код A | I2C2-цепочка #2: пересборка аргументов → 0x214c | §49 | разобран | 100% |
| [`0x01e72`](functions_mcu/func_0x01e72.md) | 32 | код A | I2C2-цепочка #3: → 0x2730 → 0x9048 → 0x8f7c(I2C2) | §49 | разобран | 100% |
| [`0x01e94`](functions_mcu/func_0x01e94.md) | 324 | код A | — | — | не начат | 0% |
| [`0x01fe0`](functions_mcu/func_0x01fe0.md) | 200 | код A | — | — | не начат | 0% |
| [`0x020c4`](functions_mcu/func_0x020c4.md) | 16 | код A | I2C2 wr reg 0x38 = u32@0x162D | §49 | разобран | 100% |
| [`0x020d8`](functions_mcu/func_0x020d8.md) | 76 | код A | — | — | не начат | 0% |
| [`0x02138`](functions_mcu/func_0x02138.md) | 16 | код A | I2C2 wr reg 0x36 = u32@0x162B | §49 | разобран | 100% |
| [`0x0214c`](functions_mcu/func_0x0214c.md) | 36 | код A | I2C2 write: 0x8f7c(op=8, reg=r0, buf=stack) | §49 | разобран | 100% |
| [`0x0218c`](functions_mcu/func_0x0218c.md) | 76 | код A | — | — | не начат | 0% |
| [`0x021dc`](functions_mcu/func_0x021dc.md) | 16 | код A | I2C2 wr reg 0x12 = u32@0x1607 | §49 | разобран | 100% |
| [`0x021f0`](functions_mcu/func_0x021f0.md) | 16 | код A | I2C2 wr reg 0x14 = u32@0x1609 | §49 | разобран | 100% |
| [`0x02204`](functions_mcu/func_0x02204.md) | 16 | код A | I2C2 wr reg 0x16 = u32@0x160B | §49 | разобран | 100% |
| [`0x02218`](functions_mcu/func_0x02218.md) | 16 | код A | I2C2 wr reg 0x18 = u32@0x160D | §49 | разобран | 100% |
| [`0x0222c`](functions_mcu/func_0x0222c.md) | 16 | код A | I2C2 wr reg 0x1A = u32@0x160F | §49 | разобран | 100% |
| [`0x02240`](functions_mcu/func_0x02240.md) | 16 | код A | I2C2 wr reg 0x1C = u32@0x1611 | §49 | разобран | 100% |
| [`0x02254`](functions_mcu/func_0x02254.md) | 16 | код A | I2C2 wr reg 0x1E = u32@0x1613 | §49 | разобран | 100% |
| [`0x02268`](functions_mcu/func_0x02268.md) | 16 | код A | I2C2 wr reg 0x20 = u32@0x1615 | §49 | разобран | 100% |
| [`0x0227c`](functions_mcu/func_0x0227c.md) | 16 | код A | I2C2 wr reg 0x22 = u32@0x1617 | §49 | разобран | 100% |
| [`0x02290`](functions_mcu/func_0x02290.md) | 16 | код A | I2C2 wr reg 0x24 = u32@0x1619 | §49 | разобран | 100% |
| [`0x022a4`](functions_mcu/func_0x022a4.md) | 16 | код A | I2C2 wr reg 0x26 = u32@0x161B | §49 | разобран | 100% |
| [`0x022b8`](functions_mcu/func_0x022b8.md) | 16 | код A | I2C2 wr reg 0x28 = u32@0x161D | §49 | разобран | 100% |
| [`0x022cc`](functions_mcu/func_0x022cc.md) | 16 | код A | I2C2 wr reg 0x2A = u32@0x161F | §49 | разобран | 100% |
| [`0x022e0`](functions_mcu/func_0x022e0.md) | 16 | код A | I2C2 wr reg 0x32 = u32@0x1621 | §49 | разобран | 100% |
| [`0x022f4`](functions_mcu/func_0x022f4.md) | 16 | код A | I2C2 wr reg 0x3A = u32@0x162F | §49 | разобран | 100% |
| [`0x02308`](functions_mcu/func_0x02308.md) | 16 | код A | I2C2 wr reg 0x7F = u32@0x164B (len 1) | §49 | разобран | 100% |
| [`0x0231c`](functions_mcu/func_0x0231c.md) | 16 | код A | I2C2 wr reg 3 = u32@0x15FA (len 1) | §49 | разобран | 100% |
| [`0x02330`](functions_mcu/func_0x02330.md) | 16 | код A | I2C2 wr reg 5 = u32@0x15FC (len 1) | §49 | разобран | 100% |
| [`0x02344`](functions_mcu/func_0x02344.md) | 16 | код A | I2C2 wr reg 7 = u32@0x15FE (len 1) | §49 | разобран | 100% |
| [`0x02358`](functions_mcu/func_0x02358.md) | 16 | код A | I2C2 wr reg 0x70 = u32@0x163F (len 2) | §49 | разобран | 100% |
| [`0x0236c`](functions_mcu/func_0x0236c.md) | 42 | код A | retry-счётчик I2C: успех 0x21dc → @0xA76=0, @0xA75++; ≥4 → сброс + @0xA73=1 | §49 | разобран | 100% |
| [`0x02730`](functions_mcu/func_0x02730.md) | 36 | код B | I2C2 read-путь: → 0x9048 | §49 | разобран | 100% |
| [`0x02770`](functions_mcu/func_0x02770.md) | 68 | код B | — | — | не начат | 0% |
| [`0x0280c`](functions_mcu/func_0x0280c.md) | 88 | код B | — | — | не начат | 0% |
| [`0x029e8`](functions_mcu/func_0x029e8.md) | 104 | код B | — | — | не начат | 0% |
| [`0x02a5c`](functions_mcu/func_0x02a5c.md) | 16 | код B | флаг 0x1bdc(0x9A) & 1 | §49 | разобран | 100% |
| [`0x02a6c`](functions_mcu/func_0x02a6c.md) | 28 | код B | UART-инициал: конфиг из flash-структуры + 0x13c5c(0x4B) (CMD 0x4B) | §49 | разобран | 100% |
| [`0x02a94`](functions_mcu/func_0x02a94.md) | 132 | код B | — | — | не начат | 0% |
| [`0x02b2c`](functions_mcu/func_0x02b2c.md) | 124 | код B | — | — | не начат | 0% |
| [`0x02bbc`](functions_mcu/func_0x02bbc.md) | 50 | код B | номер порта по GPIO-базе: A=0, B=1, C=2, D=3 | §49 | разобран | 100% |
| [`0x02d14`](functions_mcu/func_0x02d14.md) | 8 | код B | thunk → 0x9678 | §48 | ID | 25% |
| [`0x02d1c`](functions_mcu/func_0x02d1c.md) | 20 | код B | **вход в критсекцию**: u32@RAM[0xB5C]++ | §49 | разобран | 100% |
| [`0x02d34`](functions_mcu/func_0x02d34.md) | 36 | код B | **выход из критсекции**: u32@RAM[0xB5C]-- | §49 | разобран | 100% |
| [`0x02d5c`](functions_mcu/func_0x02d5c.md) | 16 | код B | **flash write**: 0x3588(); 0x332c(flash 0x1A550, 0x1A) — запись 26B в NVRAM-зону | §49 | разобран | 100% |
| [`0x02d70`](functions_mcu/func_0x02d70.md) | 130 | код B | — | — | не начат | 0% |
| [`0x02e0c`](functions_mcu/func_0x02e0c.md) | 16 | код B | проверка «оба нуля»: u16@0x38 == 0 && u16@0x3A == 0 | §49 | разобран | 100% |
| [`0x02e84`](functions_mcu/func_0x02e84.md) | 54 | код B | I2C-подобный запрос: 0x9874 (проверка структуры) + счётчик @0xB71 | §49 | разобран | 100% |
| [`0x03034`](functions_mcu/func_0x03034.md) | 62 | код B | init-подблок: 0x3044(1) + 0x305c() | §49 | разобран | 100% |
| [`0x0307c`](functions_mcu/func_0x0307c.md) | 42 | код B | **varargs**: {b,b,b,1} → 0xc0b4 (event) | §49 | разобран | 100% |
| [`0x030a6`](functions_mcu/func_0x030a6.md) | 58 | код B | EXTI-настройка: RCC-enable + remap(0xB) + 0x40010414=0x80 + 0x59a4() | §49 | разобран | 100% |
| [`0x030e0`](functions_mcu/func_0x030e0.md) | 44 | код B | RCC: 0xc664(0x10000000) + 0xc124(0x400) — PLL/часы | §49 | разобран | 100% |
| [`0x0310c`](functions_mcu/func_0x0310c.md) | 68 | код B | — | — | не начат | 0% |
| [`0x03150`](functions_mcu/func_0x03150.md) | 24 | код B | event {u32=0, u16=0x7F, u32=0x136} → 0xcd0c | §49 | разобран | 100% |
| [`0x03168`](functions_mcu/func_0x03168.md) | 96 | код B | — | — | не начат | 0% |
| [`0x031dc`](functions_mcu/func_0x031dc.md) | 66 | код B | — | — | не начат | 0% |
| [`0x032f4`](functions_mcu/func_0x032f4.md) | 54 | код B | EXTI-настройка: RCC-enable + remap(7) + 0x40010414=0x80 + 0x59a4() | §49 | разобран | 100% |
| [`0x0332c`](functions_mcu/func_0x0332c.md) | 574 | код B | — | — | не начат | 0% |
| [`0x03588`](functions_mcu/func_0x03588.md) | 84 | код B | — | — | не начат | 0% |
| [`0x035ec`](functions_mcu/func_0x035ec.md) | 18 | код B | SysTick: выкл. TICKINT (CTRL &= ~2) | §49 | разобран | 100% |
| [`0x03600`](functions_mcu/func_0x03600.md) | 96 | код B | — | — | не начат | 0% |
| [`0x03668`](functions_mcu/func_0x03668.md) | 88 | код B | — | — | не начат | 0% |
| [`0x036f4`](functions_mcu/func_0x036f4.md) | 12 | код B | последовательность: 0x10900 + 0x3b00; init-подблок: 0x3700() + 0xc984() | §48, §49 | разобран | 100% |
| [`0x03700`](functions_mcu/func_0x03700.md) | 54 | код B | поиск в таблице @0x92C (0x11 записей) через 0x583c | §49 | разобран | 100% |
| [`0x03740`](functions_mcu/func_0x03740.md) | 40 | код B | event: u16@0x1048 → 0xcd80(2) + 0xcda4() | §49 | разобран | 100% |
| [`0x03780`](functions_mcu/func_0x03780.md) | 78 | код B | — | — | не начат | 0% |
| [`0x037f4`](functions_mcu/func_0x037f4.md) | 64 | код B | инициал структуры @0x304C {0, 0x21000, 0x21000} + 0x84a0(..., 0x2000) с retry | §49 | разобран | 100% |
| [`0x03838`](functions_mcu/func_0x03838.md) | 174 | код B | — | — | не начат | 0% |
| [`0x038ec`](functions_mcu/func_0x038ec.md) | 84 | код B | — | — | не начат | 0% |
| [`0x03940`](functions_mcu/func_0x03940.md) | 22 | код B | 0x3c04(0x8000000, 0x3000, 0) → u32@0xCC (чтение flash?) | §49 | разобран | 100% |
| [`0x0395c`](functions_mcu/func_0x0395c.md) | 10 | код B | thunk → 0xd298(r0=0) | §48 | ID | 25% |
| [`0x03966`](functions_mcu/func_0x03966.md) | 10 | код B | thunk → 0xd298(r0=1) (пара с 0x395c: off/on) | §48 | ID | 25% |
| [`0x03970`](functions_mcu/func_0x03970.md) | 28 | код B | доступ к структуре @0x98: +0x20 = r0 ? r2 : r1; +0x24 = r3 | §49 | разобран | 100% |
| [`0x03994`](functions_mcu/func_0x03994.md) | 52 | код B | поиск в таблице @0x5CC (0x3A записей × 8B): match по +4 → указатель | §49 | разобран | 100% |
| [`0x03a6c`](functions_mcu/func_0x03a6c.md) | 22 | код B | one-shot флаг byte@0x142: если 0 → 1 + bl 0x3a7e | §49 | разобран | 100% |
| [`0x03b20`](functions_mcu/func_0x03b20.md) | 10 | код B | thunk → 0x1bdc(r0=0x9a) | §48 | ID | 25% |
| [`0x03b2a`](functions_mcu/func_0x03b2a.md) | 20 | код B | init-подблок: 0x3b50/0x3b74/0x3b8a/0x3b9c/0x3bb2 (цепочка RCC/периферии) | §49 | разобран | 100% |
| [`0x03b42`](functions_mcu/func_0x03b42.md) | 64 | код B | CRC-16 (полином 0xA001) + mvn (двоичное дополнение) | §49 | разобран | 100% |
| [`0x03b82`](functions_mcu/func_0x03b82.md) | 66 | код B | — | — | не начат | 0% |
| [`0x03bc4`](functions_mcu/func_0x03bc4.md) | 62 | код B | CRC-16 (полином 0x1021, MSB-first) — второй вариант | §49 | разобран | 100% |
| [`0x03c04`](functions_mcu/func_0x03c04.md) | 68 | код B | — | — | не начат | 0% |
| [`0x03c4c`](functions_mcu/func_0x03c4c.md) | 42 | код B | **CRC-16 табличный** (таблица @0x19784, 256 u16) — третий вариант CRC-16 | §49 | разобран | 100% |
| [`0x03c7c`](functions_mcu/func_0x03c7c.md) | 46 | код B | **CRC-7** (полином 0x09, MSB-first) по массиву байтов | §49 | разобран | 100% |
| [`0x03cac`](functions_mcu/func_0x03cac.md) | 232 | код B | — | — | не начат | 0% |
| [`0x03da0`](functions_mcu/func_0x03da0.md) | 58 | код B | чтение 4B из EEPROM + CRC-16 (0x8a50) с проверкой; буфер @0xC9C | §49 | разобран | 100% |
| [`0x03de4`](functions_mcu/func_0x03de4.md) | 252 | код B | — | — | не начат | 0% |
| [`0x03f00`](functions_mcu/func_0x03f00.md) | 912 | код B | — | — | не начат | 0% |
| [`0x042b8`](functions_mcu/func_0x042b8.md) | 118 | код B | — | — | не начат | 0% |
| [`0x04344`](functions_mcu/func_0x04344.md) | 324 | код B | — | — | не начат | 0% |
| [`0x044c0`](functions_mcu/func_0x044c0.md) | 58 | код B | **range-check**: u16@0xF95+6 ≤ 0x7D0 && u16@0xF95+8 ≥ 0x1194 && i8@0xFC8+1 > -40 && i8@0xFC8+2 < 0x64; гейт byte@0xA73 | §49 | разобран | 100% |
| [`0x04508`](functions_mcu/func_0x04508.md) | 266 | код B | — | — | не начат | 0% |
| [`0x04630`](functions_mcu/func_0x04630.md) | 146 | код B | — | — | не начат | 0% |
| [`0x048d8`](functions_mcu/func_0x048d8.md) | 32 | код B | сумма u16 + mvn (двоичное дополнение) — контрольная сумма | §49 | разобран | 100% |
| [`0x048f8`](functions_mcu/func_0x048f8.md) | 142 | код B | — | — | не начат | 0% |
| [`0x04994`](functions_mcu/func_0x04994.md) | 18 | код B | 0x49ac(); byte@0xD9=0; byte@0xD8=1 (пара флагов) | §49 | разобран | 100% |
| [`0x049b8`](functions_mcu/func_0x049b8.md) | 70 | код B | — | — | не начат | 0% |
| [`0x04a04`](functions_mcu/func_0x04a04.md) | 24 | код B | обнуление блока @0x129..0x13C (byte + 3×u32) | §49 | разобран | 100% |
| [`0x04a30`](functions_mcu/func_0x04a30.md) | 26 | код B | поиск в локальной таблице (2 записи) через 0x12f44/0x12d04 | §49 | разобран | 100% |
| [`0x04a4c`](functions_mcu/func_0x04a4c.md) | 160 | код B | — | — | не начат | 0% |
| [`0x04b04`](functions_mcu/func_0x04b04.md) | 28 | код B | поиск в локальной таблице (2 записи, вариант) | §49 | разобран | 100% |
| [`0x04b20`](functions_mcu/func_0x04b20.md) | 150 | код B | — | — | не начат | 0% |
| [`0x04bc0`](functions_mcu/func_0x04bc0.md) | 36 | код B | event queue @0x164C: push {ptr, 0} (slot++ % 6) | §49 | разобран | 100% |
| [`0x04be8`](functions_mcu/func_0x04be8.md) | 36 | код B | event queue @0x164C: push {u16, 0} (slot++ % 6) | §49 | разобран | 100% |
| [`0x04c14`](functions_mcu/func_0x04c14.md) | 100 | код B | — | — | не начат | 0% |
| [`0x04c84`](functions_mcu/func_0x04c84.md) | 48 | код B | event queue @0x164C: push {*(u32@RAM[0xB4C]), 0} (slot++ % 6) | §49 | разобран | 100% |
| [`0x04cbc`](functions_mcu/func_0x04cbc.md) | 122 | код B | — | — | не начат | 0% |
| [`0x04d48`](functions_mcu/func_0x04d48.md) | 138 | код B | — | — | не начат | 0% |
| [`0x04de0`](functions_mcu/func_0x04de0.md) | 40 | код B | poll: 0x1bdc(0x93)&0x1bdc(0x94) + задержка 0x1F4 | §49 | разобран | 100% |
| [`0x04e08`](functions_mcu/func_0x04e08.md) | 32 | код B | poll: 0x1bdc(0x94) + задержка 0x1F4 | §49 | разобран | 100% |
| [`0x04e28`](functions_mcu/func_0x04e28.md) | 8 | код B | thunk → 0x5000 | §48 | ID | 25% |
| [`0x04e30`](functions_mcu/func_0x04e30.md) | 8 | код B | thunk → 0x4fc0 | §48 | ID | 25% |
| [`0x04e38`](functions_mcu/func_0x04e38.md) | 4 | код B | setter +4 (str r0,[r1,#4]) | §48 | разобран | 100% |
| [`0x04f38`](functions_mcu/func_0x04f38.md) | 24 | код B | set/clear bit0 в *(u32@r0) | §49 | разобран | 100% |
| [`0x04f50`](functions_mcu/func_0x04f50.md) | 8 | код B | getter u16 @+4 (uxth) | §48 | разобран | 100% |
| [`0x04f58`](functions_mcu/func_0x04f58.md) | 20 | код B | проверка маски в u32: (*(u32@r1) & r0) != 0 | §49 | разобран | 100% |
| [`0x04f70`](functions_mcu/func_0x04f70.md) | 60 | код B | merge u32-флагов: struct+8/12 → | в r0 (для SPI/UART-конфига) | §49 | разобран | 100% |
| [`0x04fac`](functions_mcu/func_0x04fac.md) | 8 | код B | условный setter *[r2+0x10] = (r3 ? r0 : 0) | §48 | разобран | 100% |
| [`0x04fba`](functions_mcu/func_0x04fba.md) | 4 | код B | setter +4 (str r1,[r0,#4]) | §48 | разобран | 100% |
| [`0x04fc0`](functions_mcu/func_0x04fc0.md) | 52 | код B | **DMA1 INTFR handler**: если бит 0x02000000 → clear + byte@0x1743 &= ~(1<<@0x1744) + @0xB76 &= ~1 | §49 | разобран | 100% |
| [`0x05000`](functions_mcu/func_0x05000.md) | 56 | код B | **DMA1 INTFR handler**: если бит 0x20000 → clear + byte@0x1B6E &= ~(1<<@0x1B6F) + @0xB76 &= ~4 | §49 | разобран | 100% |
| [`0x05044`](functions_mcu/func_0x05044.md) | 38 | код B | среднее u16-массива (сумма/длина) | §49 | разобран | 100% |
| [`0x0506a`](functions_mcu/func_0x0506a.md) | 70 | код B | — | — | не начат | 0% |
| [`0x050b0`](functions_mcu/func_0x050b0.md) | 128 | код B | — | — | не начат | 0% |
| [`0x05134`](functions_mcu/func_0x05134.md) | 162 | код B | — | — | не начат | 0% |
| [`0x051d8`](functions_mcu/func_0x051d8.md) | 106 | код B | — | — | не начат | 0% |
| [`0x05274`](functions_mcu/func_0x05274.md) | 174 | код B | — | — | не начат | 0% |
| [`0x05330`](functions_mcu/func_0x05330.md) | 186 | код B | — | — | не начат | 0% |
| [`0x053fc`](functions_mcu/func_0x053fc.md) | 68 | код B | — | — | не начат | 0% |
| [`0x05448`](functions_mcu/func_0x05448.md) | 142 | код B | — | — | не начат | 0% |
| [`0x054dc`](functions_mcu/func_0x054dc.md) | 230 | код B | — | — | не начат | 0% |
| [`0x055c8`](functions_mcu/func_0x055c8.md) | 218 | код B | — | — | не начат | 0% |
| [`0x056bc`](functions_mcu/func_0x056bc.md) | 174 | код B | — | — | не начат | 0% |
| [`0x057a0`](functions_mcu/func_0x057a0.md) | 80 | код B | — | — | не начат | 0% |
| [`0x057f8`](functions_mcu/func_0x057f8.md) | 26 | код B | u16@0xCB3 → байты @0xCB3/0xCB5 + отправка 0x13bb8(s) | §49 | разобран | 100% |
| [`0x05818`](functions_mcu/func_0x05818.md) | 28 | код B | байты @0xCB3/0xCB5 → u16@0xCB3 + отправка 0x13bb8(s) | §49 | разобран | 100% |
| [`0x0583c`](functions_mcu/func_0x0583c.md) | 52 | код B | поиск в таблице @0x92C (0x11 записей × 8B): match по +4 → указатель | §49 | разобран | 100% |
| [`0x05874`](functions_mcu/func_0x05874.md) | 18 | код B | bit1: если 0x597c(1) → 0x5970(1) | §49 | разобран | 100% |
| [`0x05888`](functions_mcu/func_0x05888.md) | 34 | код B | bit0x800: если 0x597c(0x800) && !byte@0x102 → @0x102=1; затем 0x5970(0x800) | §49 | разобран | 100% |
| [`0x058b0`](functions_mcu/func_0x058b0.md) | 70 | код B | — | — | не начат | 0% |
| [`0x058f6`](functions_mcu/func_0x058f6.md) | 18 | код B | bit0x10: если 0x597c(0x10) → 0x5970(0x10) | §49 | разобран | 100% |
| [`0x05908`](functions_mcu/func_0x05908.md) | 92 | код B | merge u32-флагов: struct+8/12 → | в r0 (вариант 0x4f70) | §49 | разобран | 100% |
| [`0x05970`](functions_mcu/func_0x05970.md) | 6 | код B | запись r0 в регистр @0x40010414 (зона AFIO; EXTI-mapping?) | §48 | разобран | 100% |
| [`0x05a38`](functions_mcu/func_0x05a38.md) | 30 | код B | I2C-прединициал: 0x15588() + 0x5134() + 0x109c4() | §49 | разобран | 100% |
| [`0x05a68`](functions_mcu/func_0x05a68.md) | 32 | код B | u32 udiv (аппаратный + коррекция переполнения) | §49 | разобран | 100% |
| [`0x05b5a`](functions_mcu/func_0x05b5a.md) | 50 | код B | задержка 0x2F + 0x1c1c(0x90) (init-подблок) | §49 | разобран | 100% |
| [`0x05b8c`](functions_mcu/func_0x05b8c.md) | 10 | код B | thunk → 0x4de0 | §48 | ID | 25% |
| [`0x05b98`](functions_mcu/func_0x05b98.md) | 30 | код B | @0x40003000 = 0xAAAA; GPIOB+0x18 = 0x40003000>>7; GPIOA+0x18 = 4; 0xc20c(3) | §49 | разобран | 100% |
| [`0x05bc4`](functions_mcu/func_0x05bc4.md) | 202 | код B | — | — | не начат | 0% |
| [`0x05c9c`](functions_mcu/func_0x05c9c.md) | 26 | код B | @0x40003000 = 0xAAAA; 0x332c(flash 0x19B14, 2); 0xc20c(1) | §49 | разобран | 100% |
| [`0x05cc0`](functions_mcu/func_0x05cc0.md) | 10 | код B | запись 0xAAAA в @0x40003000 (дубль 0x99f0) | §48 | разобран | 100% |
| [`0x05cd0`](functions_mcu/func_0x05cd0.md) | 194 | код B | — | — | не начат | 0% |
| [`0x05dbc`](functions_mcu/func_0x05dbc.md) | 22 | код B | @0x40003000 = 0xAAAA; 0x2d5c (flash wr @0x1A550); 0xc20c(4) | §49 | разобран | 100% |
| [`0x05dd8`](functions_mcu/func_0x05dd8.md) | 262 | код B | — | — | не начат | 0% |
| [`0x05ee0`](functions_mcu/func_0x05ee0.md) | 146 | код B | — | — | не начат | 0% |
| [`0x05fb4`](functions_mcu/func_0x05fb4.md) | 32 | код B | I2C init: 0x5a38() + задержка 0x2710 + 0x1c1c(0x1F4) | §49 | разобран | 100% |
| [`0x06080`](functions_mcu/func_0x06080.md) | 312 | код B | — | — | не начат | 0% |
| [`0x061d4`](functions_mcu/func_0x061d4.md) | 12 | код B | FLASH_SR @0x4002200C |= r0 — сброс флагов (caller OTA-код 0x06230) | §48 | разобран | 100% |
| [`0x061e4`](functions_mcu/func_0x061e4.md) | 72 | код B | — | — | не начат | 0% |
| [`0x06230`](functions_mcu/func_0x06230.md) | 78 | код B | — | — | не начат | 0% |
| [`0x06284`](functions_mcu/func_0x06284.md) | 16 | код B | проверка FLASH BSY (SCBR bit0); 1=занят | §49 | разобран | 100% |
| [`0x062d4`](functions_mcu/func_0x062d4.md) | 14 | код B | FLASH_SCBR |= 0x80 (после стирания/записи) | §49 | разобран | 100% |
| [`0x06304`](functions_mcu/func_0x06304.md) | 24 | код B | выравнивание: r0&3 ? 9 : 6 | §49 | разобран | 100% |
| [`0x06360`](functions_mcu/func_0x06360.md) | 18 | код B | FLASH_CTLR биты [5:3] = r0 (режим стирания/записи) | §49 | разобран | 100% |
| [`0x06378`](functions_mcu/func_0x06378.md) | 12 | код B | FLASH unlock: magic-ключи 0x45670123/0xCDEF89AB → FLASH_KEYR @0x40022004 | §48 | разобран | 100% |
| [`0x06390`](functions_mcu/func_0x06390.md) | 38 | код B | ожидание не-BSY; таймаут → 0xA | §49 | разобран | 100% |
| [`0x063b8`](functions_mcu/func_0x063b8.md) | 590 | код B | — | — | не начат | 0% |
| [`0x06618`](functions_mcu/func_0x06618.md) | 526 | код B | — | — | не начат | 0% |
| [`0x06838`](functions_mcu/func_0x06838.md) | 310 | код B | — | — | не начат | 0% |
| [`0x06978`](functions_mcu/func_0x06978.md) | 104 | код B | — | — | не начат | 0% |
| [`0x069e4`](functions_mcu/func_0x069e4.md) | 722 | код B | — | — | не начат | 0% |
| [`0x06ccc`](functions_mcu/func_0x06ccc.md) | 378 | код B | — | — | не начат | 0% |
| [`0x06e50`](functions_mcu/func_0x06e50.md) | 358 | код B | — | — | не начат | 0% |
| [`0x06fc0`](functions_mcu/func_0x06fc0.md) | 130 | код B | — | — | не начат | 0% |
| [`0x070d8`](functions_mcu/func_0x070d8.md) | 944 | код B | — | — | не начат | 0% |
| [`0x07494`](functions_mcu/func_0x07494.md) | 1282 | код B | — | — | не начат | 0% |
| [`0x0799c`](functions_mcu/func_0x0799c.md) | 144 | код B | регулятор duty (вырожден: выход ≈ -275 → 0%) | §39, §41 | разобран | 100% |
| [`0x07a30`](functions_mcu/func_0x07a30.md) | 820 | код B | slot-3 state-machine мотора (TBB @0x7AA4) | §39, §41 | разобран | 100% |
| [`0x07d6c`](functions_mcu/func_0x07d6c.md) | 148 | код B | — | — | не начат | 0% |
| [`0x07e70`](functions_mcu/func_0x07e70.md) | 40 | код B | **bulk erase**: цикл по 0x800-байтовым секторам (буфер на стеке 0x804) | §49 | разобран | 100% |
| [`0x07e98`](functions_mcu/func_0x07e98.md) | 52 | код B | **sector erase**: валидация адреса (%0x800==0, диапазон 0x3000..0x1FFFF), unlock, 0x6230(erase), SCBR|=0x80 | §49 | разобран | 100% |
| [`0x07ed4`](functions_mcu/func_0x07ed4.md) | 18 | код B | FLASH not-busy: 0x61e4()==1 → 0, иначе 1 | §49 | разобран | 100% |
| [`0x07ee8`](functions_mcu/func_0x07ee8.md) | 58 | код B | bulk erase: инициализация стекового буфера + старт цикла | §49 | разобран | 100% |
| [`0x07fb8`](functions_mcu/func_0x07fb8.md) | 28 | код B | memmove (направленный байтовый цикл) | §49 | разобран | 100% |
| [`0x07fd4`](functions_mcu/func_0x07fd4.md) | 6 | код B | getter byte (ldrb r0,[r0]) | §48 | разобран | 100% |
| [`0x07fdc`](functions_mcu/func_0x07fdc.md) | 56 | код B | bulk erase: тело цикла (указатель → 0x6230) | §49 | разобран | 100% |
| [`0x080ac`](functions_mcu/func_0x080ac.md) | 84 | код B | — | — | не начат | 0% |
| [`0x081b4`](functions_mcu/func_0x081b4.md) | 212 | код B | — | — | не начат | 0% |
| [`0x082b8`](functions_mcu/func_0x082b8.md) | 44 | код B | one-shot под флагом @0xC8D: 0x8468(); 0x83e4(); результат в {0xC84014, 0xC84013, 0xA14014} → OK, иначе флаг=1 | §49 | разобран | 100% |
| [`0x082f0`](functions_mcu/func_0x082f0.md) | 12 | код B | guard: return если byte@0xC8D≠0 (r4-варинт; callers 0xd878/0x119e4/0x147ac) | §48 | разобран | 100% |
| [`0x0833c`](functions_mcu/func_0x0833c.md) | 6 | код B | getter byte@RAM[0xC8D] — флаг инициализации 0x8xxx-драйвера | §48 | разобран | 100% |
| [`0x08348`](functions_mcu/func_0x08348.md) | 10 | код B | one-time init (флаг byte@0xC8D==0): GPIOA + SPI1-команда 0xB9 + delay (продолжение — 0x8352) | §48 | разобран | 100% |
| [`0x08380`](functions_mcu/func_0x08380.md) | 26 | код B | транзакция 0x833c: если r0 → вернуть 0 (условный выход) | §49 | разобран | 100% |
| [`0x083e4`](functions_mcu/func_0x083e4.md) | 74 | код B | — | — | не начат | 0% |
| [`0x08434`](functions_mcu/func_0x08434.md) | 46 | код B | GPIOA: 0x87da(GPIOA, 0x10); 0x10870(5); poll 0x10870(0xFF) до bit0==0; 0x87de(GPIOA, 0x10) | §49 | разобран | 100% |
| [`0x08468`](functions_mcu/func_0x08468.md) | 10 | код B | guard: return если byte@0xC8D≠0 (вариант №2, паттерн как 0x8348) | §48 | разобран | 100% |
| [`0x084a0`](functions_mcu/func_0x084a0.md) | 22 | код B | транзакция 0x833c: если r0==0 → return (из 0x37f4/0x851c) | §49 | разобран | 100% |
| [`0x084fc`](functions_mcu/func_0x084fc.md) | 26 | код B | GPIOA: 0x87da(GPIOA, 0x10); 0x10870(6); 0x87de(GPIOA, 0x10) | §49 | разобран | 100% |
| [`0x0851c`](functions_mcu/func_0x0851c.md) | 24 | код B | транзакция 0x833c: если r0!=0 → return pc (из 0x37f4) | §49 | разобран | 100% |
| [`0x08588`](functions_mcu/func_0x08588.md) | 58 | код B | **AFIO remap**: таблица @0x40010004 (AFIO_MAPR); очистка 2 битов + запись value<<bit | §49 | разобран | 100% |
| [`0x085c8`](functions_mcu/func_0x085c8.md) | 484 | код B | — | — | не начат | 0% |
| [`0x087b0`](functions_mcu/func_0x087b0.md) | 24 | код B | инициал структуры {u16=0xFFFF, +2=0, +3=0, +8=0, +0xC=0xF} | §49 | разобран | 100% |
| [`0x087c8`](functions_mcu/func_0x087c8.md) | 18 | код B | проверка: *(u32@r0+0x10) & r1 != 0 | §49 | разобран | 100% |
| [`0x087de`](functions_mcu/func_0x087de.md) | 4 | код B | setter +0x18 (в init: GPIOA+0x18 = 0x10) | §48 | разобран | 100% |
| [`0x087e2`](functions_mcu/func_0x087e2.md) | 10 | код B | условный setter: r2 ? *(r0+0x18) : *(r0+0x28) = r1 | §48 | разобран | 100% |
| [`0x087f8`](functions_mcu/func_0x087f8.md) | 60 | код B | CRC-8 (полином 0x2F) по массиву байтов | §49 | разобран | 100% |
| [`0x08834`](functions_mcu/func_0x08834.md) | 50 | код B | **проверка «все условия»**: @0x107==1 && @0x35==1 && @0x40!=1 && @0x3C!=1 && @0x3E!=1 | §49 | разобран | 100% |
| [`0x08878`](functions_mcu/func_0x08878.md) | 6 | код B | getter byte@RAM[0x128] | §48 | разобран | 100% |
| [`0x08884`](functions_mcu/func_0x08884.md) | 168 | код B | — | — | не начат | 0% |
| [`0x08938`](functions_mcu/func_0x08938.md) | 260 | код B | — | — | не начат | 0% |
| [`0x08a44`](functions_mcu/func_0x08a44.md) | 8 | код B | getter *(u32@RAM[0xF64])+6 | §48 | разобран | 100% |
| [`0x08a50`](functions_mcu/func_0x08a50.md) | 54 | код B | CRC-16 табличный (таблицы @0x19584/@0x19684 по 256 u16); вызов из 0x3da0/0xc420 — **верификация чтения EEPROM** | §49 | разобран | 100% |
| [`0x08a90`](functions_mcu/func_0x08a90.md) | 94 | код B | — | — | не начат | 0% |
| [`0x08af0`](functions_mcu/func_0x08af0.md) | 6 | код B | getter byte@RAM[0xA73] | §48 | разобран | 100% |
| [`0x08afc`](functions_mcu/func_0x08afc.md) | 14 | код B | 0x218c() → u32@0xF95+0xD (сохранение результата) | §49 | разобран | 100% |
| [`0x08b10`](functions_mcu/func_0x08b10.md) | 56 | код B | **ADC→мВ**: u16@0x5E × 0xCE4 / 2^20 + i8@0xA6 → u8@0x44+1 | §49 | разобран | 100% |
| [`0x08b58`](functions_mcu/func_0x08b58.md) | 50 | код B | **ADC→мВ**: u16@0x5E × 0xCE4 / 2^20 + i8@0xA6 → i8@0xFC7+8 | §49 | разобран | 100% |
| [`0x08bec`](functions_mcu/func_0x08bec.md) | 388 | код B | — | — | не начат | 0% |
| [`0x08d90`](functions_mcu/func_0x08d90.md) | 6 | код B | getter u32@RAM[0x1344] | §48 | разобран | 100% |
| [`0x08e14`](functions_mcu/func_0x08e14.md) | 6 | код B | getter byte@RAM[0x1378] (@0x1359+0x1f) | §48 | разобран | 100% |
| [`0x08f58`](functions_mcu/func_0x08f58.md) | 26 | код B | i8@0xFC8 → u16@0x135E (sign-extend) | §49 | разобран | 100% |
| [`0x08f7c`](functions_mcu/func_0x08f7c.md) | 198 | код B | — | — | не начат | 0% |
| [`0x09048`](functions_mcu/func_0x09048.md) | 80 | код B | — | — | не начат | 0% |
| [`0x090a0`](functions_mcu/func_0x090a0.md) | 60 | код B | I2C1-транзакция: проверка *(u32@RAM[0xB60])!=0; адрес из *(u32@RAM[0xB64]); 0x1c08/0x1bd8/0x1c08(1) | §49 | разобран | 100% |
| [`0x09134`](functions_mcu/func_0x09134.md) | 668 | код B | — | — | не начат | 0% |
| [`0x09482`](functions_mcu/func_0x09482.md) | 12 | код B | последовательность: 0x9134 + 0x9480 | §48 | ID | 25% |
| [`0x09678`](functions_mcu/func_0x09678.md) | 86 | код B | — | — | не начат | 0% |
| [`0x096dc`](functions_mcu/func_0x096dc.md) | 52 | код B | вызов callback из структуры @0xDD8+0x114 (дефолт 0x11a4) | §49 | разобран | 100% |
| [`0x09714`](functions_mcu/func_0x09714.md) | 52 | код B | вызов callback из структуры @0xDD8+0x110 (дефолт 0x11a4) | §49 | разобран | 100% |
| [`0x09794`](functions_mcu/func_0x09794.md) | 42 | код B | проверка: u32 из u16(+0x14/+0x18) содержит все биты r1 (без знака) | §49 | разобран | 100% |
| [`0x097ca`](functions_mcu/func_0x097ca.md) | 24 | код B | set/clear bit0x400 в *(u16@r0) | §49 | разобран | 100% |
| [`0x097e2`](functions_mcu/func_0x097e2.md) | 18 | код B | set/clear маски r1 в *(u16@r0+4) | §49 | разобран | 100% |
| [`0x097f4`](functions_mcu/func_0x097f4.md) | 50 | код B | вкл/выкл тактирования I2C1 (RCC bit21) / I2C2 (bit22) через 0xc684 | §49 | разобран | 100% |
| [`0x0982c`](functions_mcu/func_0x0982c.md) | 24 | код B | set/clear bit0 в *(u16@r0) | §49 | разобран | 100% |
| [`0x09844`](functions_mcu/func_0x09844.md) | 24 | код B | set/clear bit0x100 в *(u16@r0) | §49 | разобран | 100% |
| [`0x0985c`](functions_mcu/func_0x0985c.md) | 24 | код B | set/clear bit0x200 в *(u16@r0) | §49 | разобран | 100% |
| [`0x09874`](functions_mcu/func_0x09874.md) | 54 | код B | проверка флага в структуре: r1<<28 ? +0x14 : +0x18; (val & r1) != 0 | §49 | разобран | 100% |
| [`0x098ae`](functions_mcu/func_0x098ae.md) | 26 | код B | u32 из двух u16 (+0x14/+0x18), старший байт = 0 | §49 | разобран | 100% |
| [`0x098c8`](functions_mcu/func_0x098c8.md) | 222 | код B | — | — | не начат | 0% |
| [`0x099b4`](functions_mcu/func_0x099b4.md) | 8 | код B | getter byte из u16@+0x10 (uxtb ldrh) | §48 | разобран | 100% |
| [`0x099bc`](functions_mcu/func_0x099bc.md) | 18 | код B | set/clear bit0 в *(u16@r0+0x10) | §49 | разобран | 100% |
| [`0x099ce`](functions_mcu/func_0x099ce.md) | 4 | код B | setter u16 @+0x10 (strh) | §48 | разобран | 100% |
| [`0x099d4`](functions_mcu/func_0x099d4.md) | 6 | код B | запись r0 в @0x40003000+8 | §48 | разобран | 100% |
| [`0x099e0`](functions_mcu/func_0x099e0.md) | 10 | код B | запись 0xCCCC в @0x40003000 | §48 | разобран | 100% |
| [`0x099f0`](functions_mcu/func_0x099f0.md) | 10 | код B | запись 0xAAAA в @0x40003000 (кластер драйвера) | §48 | разобран | 100% |
| [`0x09a00`](functions_mcu/func_0x09a00.md) | 6 | код B | запись r0 в @0x40003000+4 | §48 | разобран | 100% |
| [`0x09a0c`](functions_mcu/func_0x09a0c.md) | 6 | код B | запись r0 в @0x40003000 | §48 | разобран | 100% |
| [`0x09a18`](functions_mcu/func_0x09a18.md) | 8 | код B | thunk → 0x99f0 (запись 0xAAAA в @0x40003000) | §48 | ID | 25% |
| [`0x09a20`](functions_mcu/func_0x09a20.md) | 34 | код B | @0x40003000 cmd: 0x5555 → 0x9a0c; 0x9a00(6); uxth(r4) → 0x99d4; 0x99f0; 0x99e0 | §49 | разобран | 100% |
| [`0x09a44`](functions_mcu/func_0x09a44.md) | 80 | код B | — | — | не начат | 0% |
| [`0x09aa4`](functions_mcu/func_0x09aa4.md) | 86 | код B | — | — | не начат | 0% |
| [`0x09b08`](functions_mcu/func_0x09b08.md) | 54 | код B | toggle bit3 byte@0xA71 (до 3 попыток, гейт 0x2a5c) | §49 | разобран | 100% |
| [`0x09b44`](functions_mcu/func_0x09b44.md) | 24 | код B | init-подблок: 0x9b54() + 0x9b6c() | §49 | разобран | 100% |
| [`0x09f64`](functions_mcu/func_0x09f64.md) | 12 | код B | последовательность: 0x9b44 + 0x9f70 | §48 | ID | 25% |
| [`0x09f70`](functions_mcu/func_0x09f70.md) | 28 | код B | init-подблок: 0x9f80(0x10) + 0x9fa4(1) | §49 | разобран | 100% |
| [`0x0a6a4`](functions_mcu/func_0x0a6a4.md) | 6 | код B | getter byte@RAM[0x40] | §48 | разобран | 100% |
| [`0x0a788`](functions_mcu/func_0x0a788.md) | 96 | код B | — | — | не начат | 0% |
| [`0x0a7ec`](functions_mcu/func_0x0a7ec.md) | 184 | код B | — | — | не начат | 0% |
| [`0x0a8c4`](functions_mcu/func_0x0a8c4.md) | 66 | код B | — | — | не начат | 0% |
| [`0x0a910`](functions_mcu/func_0x0a910.md) | 70 | код B | — | — | не начат | 0% |
| [`0x0a960`](functions_mcu/func_0x0a960.md) | 170 | код B | — | — | не начат | 0% |
| [`0x0aa18`](functions_mcu/func_0x0aa18.md) | 170 | код B | — | — | не начат | 0% |
| [`0x0aad0`](functions_mcu/func_0x0aad0.md) | 58 | код B | CRC-16 (полином 0xA001, MSB-first) по массиву байтов | §49 | разобран | 100% |
| [`0x0ab0c`](functions_mcu/func_0x0ab0c.md) | 46 | код B | I2C read 0x38B + двойной poll 0xa910(0)/0xa910(1) | §49 | разобран | 100% |
| [`0x0abf0`](functions_mcu/func_0x0abf0.md) | 46 | код B | I2C read 0x20B + двойной poll 0xa8c4(0)/0xa8c4(1) | §49 | разобран | 100% |
| [`0x0acce`](functions_mcu/func_0x0acce.md) | 458 | код B | — | — | не начат | 0% |
| [`0x0af94`](functions_mcu/func_0x0af94.md) | 250 | код B | — | — | не начат | 0% |
| [`0x0b09a`](functions_mcu/func_0x0b09a.md) | 244 | код B | — | — | не начат | 0% |
| [`0x0b302`](functions_mcu/func_0x0b302.md) | 362 | код B | — | — | не начат | 0% |
| [`0x0b476`](functions_mcu/func_0x0b476.md) | 80 | код B | — | — | не начат | 0% |
| [`0x0b4ce`](functions_mcu/func_0x0b4ce.md) | 96 | код B | — | — | не начат | 0% |
| [`0x0b53a`](functions_mcu/func_0x0b53a.md) | 64 | код B | I2C-подобная транзакция с retry (poll 0x9794) | §49 | разобран | 100% |
| [`0x0b582`](functions_mcu/func_0x0b582.md) | 72 | код B | — | — | не начат | 0% |
| [`0x0b618`](functions_mcu/func_0x0b618.md) | 56 | код B | инициал транзакции: 0xb8c8/0xb968; если пусто → *(u16@[r4]) &= ~1, +4 |= 0x700, +0x10C=0 | §49 | разобран | 100% |
| [`0x0b854`](functions_mcu/func_0x0b854.md) | 10 | код B | запись 0x10000 в struct+0x108 (caller: struct@RAM[0xdd8]) | §48 | разобран | 100% |
| [`0x0b860`](functions_mcu/func_0x0b860.md) | 94 | код B | — | — | не начат | 0% |
| [`0x0b8dc`](functions_mcu/func_0x0b8dc.md) | 128 | код B | — | — | не начат | 0% |
| [`0x0b978`](functions_mcu/func_0x0b978.md) | 32 | код B | проверка «очередь пуста»: *(u32@RAM[0x106]) == *(u32@RAM[0x10A]) | §49 | разобран | 100% |
| [`0x0bb14`](functions_mcu/func_0x0bb14.md) | 32 | код B | проверка «очередь пуста» (вариант) | §49 | разобран | 100% |
| [`0x0bc5c`](functions_mcu/func_0x0bc5c.md) | 40 | код B | сборка дескриптора {ptr, 0, 0} → 0xc0b4() | §49 | разобран | 100% |
| [`0x0bc86`](functions_mcu/func_0x0bc86.md) | 56 | код B | сборка дескриптора {ptr, 0, 0} → 0x85c8() | §49 | разобран | 100% |
| [`0x0bcc0`](functions_mcu/func_0x0bcc0.md) | 138 | код B | — | — | не начат | 0% |
| [`0x0bd50`](functions_mcu/func_0x0bd50.md) | 280 | код B | — | — | не начат | 0% |
| [`0x0be6c`](functions_mcu/func_0x0be6c.md) | 104 | код B | — | — | не начат | 0% |
| [`0x0befc`](functions_mcu/func_0x0befc.md) | 74 | код B | — | — | не начат | 0% |
| [`0x0bf4c`](functions_mcu/func_0x0bf4c.md) | 12 | код B | последовательность: 0xd878 + 0xddc4 | §48 | ID | 25% |
| [`0x0bf58`](functions_mcu/func_0x0bf58.md) | 184 | код B | — | — | не начат | 0% |
| [`0x0c02c`](functions_mcu/func_0x0c02c.md) | 92 | код B | — | — | не начат | 0% |
| [`0x0c098`](functions_mcu/func_0x0c098.md) | 24 | код B | init-подблок: 0x5b5a() + 0xc0a0() | §49 | разобран | 100% |
| [`0x0c0b4`](functions_mcu/func_0x0c0b4.md) | 78 | код B | — | — | не начат | 0% |
| [`0x0c138`](functions_mcu/func_0x0c138.md) | 26 | код B | магия: u16@0xA7C == 0xEB04 → 1 | §49 | разобран | 100% |
| [`0x0c158`](functions_mcu/func_0x0c158.md) | 164 | код B | — | — | не начат | 0% |
| [`0x0c200`](functions_mcu/func_0x0c200.md) | 12 | код B | thunk → 0x9f64 (r3=1) | §48 | ID | 25% |
| [`0x0c20c`](functions_mcu/func_0x0c20c.md) | 134 | код B | — | — | не начат | 0% |
| [`0x0c2a8`](functions_mcu/func_0x0c2a8.md) | 84 | код B | — | — | не начат | 0% |
| [`0x0c304`](functions_mcu/func_0x0c304.md) | 96 | код B | — | — | не начат | 0% |
| [`0x0c368`](functions_mcu/func_0x0c368.md) | 172 | код B | — | — | не начат | 0% |
| [`0x0c420`](functions_mcu/func_0x0c420.md) | 60 | код B | чтение 4B из EEPROM + CRC-16 (0x8a50); буфер @0xC9C (вариант 0x3da0) | §49 | разобран | 100% |
| [`0x0c464`](functions_mcu/func_0x0c464.md) | 20 | код B | запись структуры {u32=r1, +4=0, +5=0, +6=r2, +7=r3} → 1 | §49 | разобран | 100% |
| [`0x0c4b4`](functions_mcu/func_0x0c4b4.md) | 18 | код B | RCC_CFGR0[7:4] (HPRE) = r0 | §49 | разобран | 100% |
| [`0x0c4cc`](functions_mcu/func_0x0c4cc.md) | 70 | код B | — | — | не начат | 0% |
| [`0x0c518`](functions_mcu/func_0x0c518.md) | 34 | код B | HSION on/off (RCC_CTLR bit0) | §49 | разобран | 100% |
| [`0x0c540`](functions_mcu/func_0x0c540.md) | 58 | код B | setter битов RCC+0x24 (режимы r0 0/1/4) | §49 | разобран | 100% |
| [`0x0c580`](functions_mcu/func_0x0c580.md) | 18 | код B | RCC_CFGR0[10:8] (PPRE1) = r0 | §49 | разобран | 100% |
| [`0x0c598`](functions_mcu/func_0x0c598.md) | 20 | код B | RCC_CFGR0[14:11] (PPRE2) = r0<<3 | §49 | разобран | 100% |
| [`0x0c5b0`](functions_mcu/func_0x0c5b0.md) | 56 | код B | комбинированный setter RCC CFGR0/CFGR2 (PLL-конфиг?) | §49 | разобран | 100% |
| [`0x0c60c`](functions_mcu/func_0x0c60c.md) | 18 | код B | RCC_CFGR0[1:0] (SW — источник тактирования) = r0 | §49 | разобран | 100% |
| [`0x0c624`](functions_mcu/func_0x0c624.md) | 26 | код B | set/clear битов RCC+0x14 (AWDCR?) | §49 | разобран | 100% |
| [`0x0c684`](functions_mcu/func_0x0c684.md) | 26 | код B | set/clear битов RCC+0x10 (вкл. тактирование I2C1/I2C2: биты 21/22 из 0x97f4) | §49 | разобран | 100% |
| [`0x0c6a4`](functions_mcu/func_0x0c6a4.md) | 26 | код B | set/clear битов RCC+0x18 (BDCR?) | §49 | разобран | 100% |
| [`0x0c6c4`](functions_mcu/func_0x0c6c4.md) | 26 | код B | set/clear битов RCC+0xC (INTENR?) | §49 | разобран | 100% |
| [`0x0c6f0`](functions_mcu/func_0x0c6f0.md) | 6 | код B | запись в 0x42420060 — несуществующий адрес (dead code?) | §48 | ID | 25% |
| [`0x0c708`](functions_mcu/func_0x0c708.md) | 86 | код B | — | — | не начат | 0% |
| [`0x0c858`](functions_mcu/func_0x0c858.md) | 52 | код B | проверка RCC-флага: группа 1=CTLR, 2=CFGR2(+0x20), иначе +0x24; бит r1&0x1f | §49 | разобран | 100% |
| [`0x0c894`](functions_mcu/func_0x0c894.md) | 10 | код B | (RCC_CFGR0 @0x40021004) & 0xC — биты AHB-прескалера | §48 | разобран | 100% |
| [`0x0c8a4`](functions_mcu/func_0x0c8a4.md) | 56 | код B | ожидание HSERDY (CTLR bit17), таймаут 0x2000 | §49 | разобран | 100% |
| [`0x0c8dc`](functions_mcu/func_0x0c8dc.md) | 56 | код B | ожидание RCC(+0x24) bit1, таймаут 0x500 | §49 | разобран | 100% |
| [`0x0c914`](functions_mcu/func_0x0c914.md) | 56 | код B | ожидание RCC_CTLR bit3, таймаут 0x500 | §49 | разобран | 100% |
| [`0x0c94c`](functions_mcu/func_0x0c94c.md) | 54 | код B | AFIO/EXTI-блок: 0x14958(5); 0xce4c; 0x58b0(1); 0x40010414=0x100000; 0xc9fc(1<<14); 0xc9dc(0x4000); 0xcb40(1) | §49 | разобран | 100% |
| [`0x0c984`](functions_mcu/func_0x0c984.md) | 30 | код B | поиск в таблице @0x5CC (0x3A записей) через 0x3994 | §49 | разобран | 100% |
| [`0x0c9a8`](functions_mcu/func_0x0c9a8.md) | 22 | код B | BCD → binary (по байтам) | §49 | разобран | 100% |
| [`0x0c9be`](functions_mcu/func_0x0c9be.md) | 28 | код B | binary → BCD (по байтам) | §49 | разобран | 100% |
| [`0x0ca3c`](functions_mcu/func_0x0ca3c.md) | 144 | код B | — | — | не начат | 0% |
| [`0x0cb10`](functions_mcu/func_0x0cb10.md) | 42 | код B | WWDG+0x24: последовательность 0xCA → 0x53 (магия?) | §49 | разобран | 100% |
| [`0x0cb40`](functions_mcu/func_0x0cb40.md) | 116 | код B | — | — | не начат | 0% |
| [`0x0cbb8`](functions_mcu/func_0x0cbb8.md) | 68 | код B | — | — | не начат | 0% |
| [`0x0cc08`](functions_mcu/func_0x0cc08.md) | 14 | код B | WWDG @0x40002800: SR(+0xC) &= ~0x80 (EWIF?) | §49 | разобран | 100% |
| [`0x0cc1c`](functions_mcu/func_0x0cc1c.md) | 68 | код B | — | — | не начат | 0% |
| [`0x0cc68`](functions_mcu/func_0x0cc68.md) | 76 | код B | — | — | не начат | 0% |
| [`0x0ccbc`](functions_mcu/func_0x0ccbc.md) | 72 | код B | — | — | не начат | 0% |
| [`0x0cd0c`](functions_mcu/func_0x0cd0c.md) | 110 | код B | — | — | не начат | 0% |
| [`0x0cd80`](functions_mcu/func_0x0cd80.md) | 136 | код B | — | — | не начат | 0% |
| [`0x0ce68`](functions_mcu/func_0x0ce68.md) | 8 | код B | thunk → 0x3168 | §48 | ID | 25% |
| [`0x0ce70`](functions_mcu/func_0x0ce70.md) | 92 | код B | — | — | не начат | 0% |
| [`0x0ced0`](functions_mcu/func_0x0ced0.md) | 16 | код B | init-подблок: 0xcdd4(1) + 0xcdc8(1) | §49 | разобран | 100% |
| [`0x0cee0`](functions_mcu/func_0x0cee0.md) | 68 | код B | — | — | не начат | 0% |
| [`0x0cf60`](functions_mcu/func_0x0cf60.md) | 84 | код B | — | — | не начат | 0% |
| [`0x0cfb8`](functions_mcu/func_0x0cfb8.md) | 78 | код B | — | — | не начат | 0% |
| [`0x0d00c`](functions_mcu/func_0x0d00c.md) | 534 | код B | — | — | не начат | 0% |
| [`0x0d240`](functions_mcu/func_0x0d240.md) | 82 | код B | — | — | не начат | 0% |
| [`0x0d298`](functions_mcu/func_0x0d298.md) | 46 | код B | poll 0xcfb8 с задержкой 0x1F4; затем *(u32@*(u32@RAM[0x304C])) != 0 | §49 | разобран | 100% |
| [`0x0d33c`](functions_mcu/func_0x0d33c.md) | 84 | код B | — | — | не начат | 0% |
| [`0x0d39c`](functions_mcu/func_0x0d39c.md) | 202 | код B | — | — | не начат | 0% |
| [`0x0d46c`](functions_mcu/func_0x0d46c.md) | 182 | код B | — | — | не начат | 0% |
| [`0x0d534`](functions_mcu/func_0x0d534.md) | 152 | код B | — | — | не начат | 0% |
| [`0x0d5d4`](functions_mcu/func_0x0d5d4.md) | 146 | код B | — | — | не начат | 0% |
| [`0x0d670`](functions_mcu/func_0x0d670.md) | 110 | код B | — | — | не начат | 0% |
| [`0x0d6e4`](functions_mcu/func_0x0d6e4.md) | 36 | код B | one-shot флаг u32@0x8C bit0xA: если не стоит — поставить и bl 0xd75c; one-shot флаг u32@0x8C bit0xB: если не стоит — поставить и bl 0xd75c | §49 | разобран | 100% |
| [`0x0d70c`](functions_mcu/func_0x0d70c.md) | 36 | код B | one-shot флаг u32@0x8C bit0xC: если не стоит — поставить и bl 0xd75c | §49 | разобран | 100% |
| [`0x0d734`](functions_mcu/func_0x0d734.md) | 36 | код B | one-shot флаг u32@0x8C bit0xD: если не стоит — поставить и bl 0xd75c; one-shot флаг u32@0x8C bit0xE: если не стоит — поставить и bl 0xd75c | §49 | разобран | 100% |
| [`0x0d75c`](functions_mcu/func_0x0d75c.md) | 36 | код B | one-shot флаг u32@0x8C bit0xF: если не стоит — поставить и bl 0xd75c | §49 | разобран | 100% |
| [`0x0d784`](functions_mcu/func_0x0d784.md) | 36 | код B | one-shot флаг u32@0x8C bit0x10: если не стоит — поставить и bl 0xd75c | §49 | разобран | 100% |
| [`0x0d7ac`](functions_mcu/func_0x0d7ac.md) | 36 | код B | one-shot флаг u32@0x8C bit0x12: если не стоит — поставить и bl 0xd75c | §49 | разобран | 100% |
| [`0x0d7d4`](functions_mcu/func_0x0d7d4.md) | 36 | код B | one-shot флаг u32@0x8C bit0x13: если не стоит — поставить и bl 0xd75c | §49 | разобран | 100% |
| [`0x0d7fc`](functions_mcu/func_0x0d7fc.md) | 36 | код B | clear bit0xC u32@0x8C если 0xd46c(0xC)==1 | §49 | разобран | 100% |
| [`0x0d824`](functions_mcu/func_0x0d824.md) | 36 | код B | clear bit0xA u32@0x8C если 0xd46c(0xA)==1 | §49 | разобран | 100% |
| [`0x0d850`](functions_mcu/func_0x0d850.md) | 36 | код B | clear bit0x12 u32@0x8C если 0xd39c(0x12)==1 | §49 | разобран | 100% |
| [`0x0d878`](functions_mcu/func_0x0d878.md) | 190 | код B | — | — | не начат | 0% |
| [`0x0d938`](functions_mcu/func_0x0d938.md) | 970 | код B | — | — | не начат | 0% |
| [`0x0dd2c`](functions_mcu/func_0x0dd2c.md) | 84 | код B | — | — | не начат | 0% |
| [`0x0ddc4`](functions_mcu/func_0x0ddc4.md) | 58 | код B | **OTA-команда от хоста**: u16@0x124E+0x12==0xE0 && +0x14==0x5AA5 → erase @0x1D800 + 0xdd80; ==0xE2 → 0xdd80 (магия 0x5AA5) | §49 | разобран | 100% |
| [`0x0de0a`](functions_mcu/func_0x0de0a.md) | 196 | код B | — | — | не начат | 0% |
| [`0x0ded4`](functions_mcu/func_0x0ded4.md) | 54 | код B | **varargs**: если byte[1]==3 → u32 из 4 байтов → *(u32@RAM[0xFE7])+2 = value; return 1 | §49 | разобран | 100% |
| [`0x0df10`](functions_mcu/func_0x0df10.md) | 338 | код B | — | — | не начат | 0% |
| [`0x0e160`](functions_mcu/func_0x0e160.md) | 24 | код B | поиск в flash-таблице строк @0x19E98+0x140 через 0x16880/0x16aa2 | §49 | разобран | 100% |
| [`0x0e17c`](functions_mcu/func_0x0e17c.md) | 128 | код B | — | — | не начат | 0% |
| [`0x0e200`](functions_mcu/func_0x0e200.md) | 198 | код B | — | — | не начат | 0% |
| [`0x0e2cc`](functions_mcu/func_0x0e2cc.md) | 44 | код B | range-check смещения по flash-строке @0x19F50+0x59F через 0x16d8e → byte | §49 | разобран | 100% |
| [`0x0e2fc`](functions_mcu/func_0x0e2fc.md) | 104 | код B | — | — | не начат | 0% |
| [`0x0e36c`](functions_mcu/func_0x0e36c.md) | 114 | код B | — | — | не начат | 0% |
| [`0x0e3e4`](functions_mcu/func_0x0e3e4.md) | 6 | код B | setter u16 = 0 (strh #0,[r0]) | §48 | разобран | 100% |
| [`0x0e3ec`](functions_mcu/func_0x0e3ec.md) | 24 | код B | поиск в flash-таблице строк @0x19FAC+0x8A через 0x16880/0x16aa2 | §49 | разобран | 100% |
| [`0x0e408`](functions_mcu/func_0x0e408.md) | 566 | код B | slew-лимитер → u16@RAM[0x1357] (duty% = byte@0xFD3) | §39, §41 | разобран | 100% |
| [`0x0e658`](functions_mcu/func_0x0e658.md) | 136 | код B | round-robin диспетчер 6 задач (TBB @0xE684) | §39.5b | разобран | 100% |
| [`0x0e6ec`](functions_mcu/func_0x0e6ec.md) | 18 | код B | условный вызов: *(u32@RAM[0x1C]) != 0 → bl [r0] (function pointer) | §49 | разобран | 100% |
| [`0x0e704`](functions_mcu/func_0x0e704.md) | 54 | код B | **clamp |v|≤0xC8**: иначе обнулить byte@0x12BA+0x56; вызов 0x1654c; вызов из 0x07A30 (§41 slot-3) | §49 | разобран | 100% |
| [`0x0e740`](functions_mcu/func_0x0e740.md) | 190 | код B | — | — | не начат | 0% |
| [`0x0e808`](functions_mcu/func_0x0e808.md) | 592 | код B | — | — | не начат | 0% |
| [`0x0ea64`](functions_mcu/func_0x0ea64.md) | 504 | код B | — | — | не начат | 0% |
| [`0x0ec70`](functions_mcu/func_0x0ec70.md) | 352 | код B | — | — | не начат | 0% |
| [`0x0eddc`](functions_mcu/func_0x0eddc.md) | 98 | код B | — | — | не начат | 0% |
| [`0x0ee48`](functions_mcu/func_0x0ee48.md) | 298 | код B | — | — | не начат | 0% |
| [`0x0ef78`](functions_mcu/func_0x0ef78.md) | 140 | код B | — | — | не начат | 0% |
| [`0x0f038`](functions_mcu/func_0x0f038.md) | 262 | код B | — | — | не начат | 0% |
| [`0x0f14c`](functions_mcu/func_0x0f14c.md) | 156 | код B | — | — | не начат | 0% |
| [`0x0f1ec`](functions_mcu/func_0x0f1ec.md) | 78 | код B | — | — | не начат | 0% |
| [`0x0f290`](functions_mcu/func_0x0f290.md) | 94 | код B | — | — | не начат | 0% |
| [`0x0f304`](functions_mcu/func_0x0f304.md) | 88 | код B | — | — | не начат | 0% |
| [`0x0f36c`](functions_mcu/func_0x0f36c.md) | 80 | код B | — | — | не начат | 0% |
| [`0x0f40c`](functions_mcu/func_0x0f40c.md) | 116 | код B | — | — | не начат | 0% |
| [`0x0f5c4`](functions_mcu/func_0x0f5c4.md) | 102 | код B | — | — | не начат | 0% |
| [`0x0f694`](functions_mcu/func_0x0f694.md) | 746 | код B | — | — | не начат | 0% |
| [`0x0f994`](functions_mcu/func_0x0f994.md) | 564 | код B | — | — | не начат | 0% |
| [`0x0fbf8`](functions_mcu/func_0x0fbf8.md) | 190 | код B | — | — | не начат | 0% |
| [`0x0fcd0`](functions_mcu/func_0x0fcd0.md) | 194 | код B | — | — | не начат | 0% |
| [`0x0fdac`](functions_mcu/func_0x0fdac.md) | 174 | код B | — | — | не начат | 0% |
| [`0x0fe74`](functions_mcu/func_0x0fe74.md) | 174 | код B | — | — | не начат | 0% |
| [`0x10468`](functions_mcu/func_0x10468.md) | 166 | код C | — | — | не начат | 0% |
| [`0x10524`](functions_mcu/func_0x10524.md) | 78 | код C | — | — | не начат | 0% |
| [`0x105c4`](functions_mcu/func_0x105c4.md) | 194 | код C | — | — | не начат | 0% |
| [`0x106a0`](functions_mcu/func_0x106a0.md) | 24 | код C | set/clear bit0x40 в *(u16@r0) | §49 | разобран | 100% |
| [`0x106b8`](functions_mcu/func_0x106b8.md) | 28 | код C | SPI1-инициал: SPI_CTLR |= 0x10, RCC |= 0x400, SPI+0x4=0x80, 0x5a6c() | §49 | разобран | 100% |
| [`0x106d8`](functions_mcu/func_0x106d8.md) | 54 | код C | SPI1 (0x40013000) / SPI-2 (0x40013C00): вкл/выкл через RCC+0xC биты (base>>12) | §49 | разобран | 100% |
| [`0x10718`](functions_mcu/func_0x10718.md) | 18 | код C | проверка: *(u16@r0+8) & r1 != 0 | §49 | разобран | 100% |
| [`0x1072a`](functions_mcu/func_0x1072a.md) | 6 | код C | getter u16 @+0xc (ldrh) | §48 | разобран | 100% |
| [`0x10730`](functions_mcu/func_0x10730.md) | 4 | код C | setter u16 @+0xc (strh) | §48 | разобран | 100% |
| [`0x10734`](functions_mcu/func_0x10734.md) | 60 | код C | SPI-конфиг: merge u16-флагов из структуры → SPI-регистр; вызов 0x10788 | §49 | разобран | 100% |
| [`0x10770`](functions_mcu/func_0x10770.md) | 16 | код C | SPI1-инициал: SPI_CTLR |= 0x40, RCC |= 0x1000, SPI+0x4=0x80, 0x5a6c() | §49 | разобран | 100% |
| [`0x10780`](functions_mcu/func_0x10780.md) | 8 | код C | thunk → 0x10788 | §48 | ID | 25% |
| [`0x10788`](functions_mcu/func_0x10788.md) | 92 | код C | — | — | не начат | 0% |
| [`0x107ec`](functions_mcu/func_0x107ec.md) | 126 | код C | — | — | не начат | 0% |
| [`0x10870`](functions_mcu/func_0x10870.md) | 98 | код C | — | — | не начат | 0% |
| [`0x1093c`](functions_mcu/func_0x1093c.md) | 118 | код C | — | — | не начат | 0% |
| [`0x10a20`](functions_mcu/func_0x10a20.md) | 8 | код C | thunk → 0x112bc | §48 | ID | 25% |
| [`0x10a5c`](functions_mcu/func_0x10a5c.md) | 50 | код C | event: u16@0x1048 → 0xcd80(1) + 0xcda4() | §49 | разобран | 100% |
| [`0x10abc`](functions_mcu/func_0x10abc.md) | 60 | код C | включение HSE (CTLR bit0) + ожидание HSERDY (bit1), таймаут 0x500; fallback-константа 0x3D0900 → @0xB88 | §49 | разобран | 100% |
| [`0x10ba0`](functions_mcu/func_0x10ba0.md) | 160 | код C | — | — | не начат | 0% |
| [`0x10cdc`](functions_mcu/func_0x10cdc.md) | 152 | код C | — | — | не начат | 0% |
| [`0x110f0`](functions_mcu/func_0x110f0.md) | 10 | код D | thunk → 0x5b8c(r0=0) | §48 | ID | 25% |
| [`0x110fc`](functions_mcu/func_0x110fc.md) | 400 | код D | — | — | не начат | 0% |
| [`0x11350`](functions_mcu/func_0x11350.md) | 30 | код D | обнуление кластера счётчиков @0xA55..; гейт bit7(u16@0xF95+0xC) | §49 | разобран | 100% |
| [`0x11668`](functions_mcu/func_0x11668.md) | 12 | код D | thunk → 0x10e5c | §48 | ID | 25% |
| [`0x11674`](functions_mcu/func_0x11674.md) | 168 | код D | — | — | не начат | 0% |
| [`0x11724`](functions_mcu/func_0x11724.md) | 166 | код D | — | — | не начат | 0% |
| [`0x117d4`](functions_mcu/func_0x117d4.md) | 172 | код D | — | — | не начат | 0% |
| [`0x11888`](functions_mcu/func_0x11888.md) | 12 | код D | thunk → 0x10f18 | §48 | ID | 25% |
| [`0x11894`](functions_mcu/func_0x11894.md) | 204 | код D | — | — | не начат | 0% |
| [`0x11978`](functions_mcu/func_0x11978.md) | 32 | код D | init-подблок: 0x11988(0x80) + 0x119a0() | §49 | разобран | 100% |
| [`0x11998`](functions_mcu/func_0x11998.md) | 44 | код D | **инициал-цепочка из 10 вызовов** (0xfbf8..0xff3c) | §49 | разобран | 100% |
| [`0x119c4`](functions_mcu/func_0x119c4.md) | 32 | код D | init-подблок: 0x119d4() + 0x119ec() | §49 | разобран | 100% |
| [`0x119e4`](functions_mcu/func_0x119e4.md) | 434 | код D | — | — | не начат | 0% |
| [`0x11bac`](functions_mcu/func_0x11bac.md) | 130 | код D | — | — | не начат | 0% |
| [`0x11c3c`](functions_mcu/func_0x11c3c.md) | 34 | код D | I2C init: 0x5a38() + задержка 0x29BC + 0x1c1c(0x1F4) | §49 | разобран | 100% |
| [`0x11c5e`](functions_mcu/func_0x11c5e.md) | 38 | код D | I2C init: 0x5a38() + задержка 0x9239 + 0x1c1c(0x1F4) | §49 | разобран | 100% |
| [`0x11cac`](functions_mcu/func_0x11cac.md) | 8 | код D | thunk → 0x4c14 | §48 | ID | 25% |
| [`0x11cb4`](functions_mcu/func_0x11cb4.md) | 188 | код D | — | — | не начат | 0% |
| [`0x11d98`](functions_mcu/func_0x11d98.md) | 58 | код D | state machine byte@0x2E: 0→1+инициал; 2/3/4/5→сброс в 0 с вызовами; копия в @0xF70+5/6 | §49 | разобран | 100% |
| [`0x11de8`](functions_mcu/func_0x11de8.md) | 1410 | код D | — | — | не начат | 0% |
| [`0x1238c`](functions_mcu/func_0x1238c.md) | 48 | код D | state machine byte@0x35: 0→1+инициал; 2/3/4/5→сброс в 0 с вызовами | §49 | разобран | 100% |
| [`0x123c0`](functions_mcu/func_0x123c0.md) | 10 | код D | запись 0x10000 в struct@RAM[0xdd8]+0x108 (через 0xb854) | §48 | разобран | 100% |
| [`0x12804`](functions_mcu/func_0x12804.md) | 40 | код E | поиск в flash-таблице @0x19B3C (u16, шаг 2): код 0x82/0xE/0x65 | §49 | разобран | 100% |
| [`0x128c8`](functions_mcu/func_0x128c8.md) | 18 | код E | EEPROM-запись: 0x50b0(&@0x44, 2); 0x1093c() | §49 | разобран | 100% |
| [`0x128e4`](functions_mcu/func_0x128e4.md) | 114 | код E | — | — | не начат | 0% |
| [`0x129b4`](functions_mcu/func_0x129b4.md) | 46 | код E | state dispatch: 0x4c84(1, 10); 0x12470(); TBB по byte@0xB58 (<0xA) — таблица повреждена/обфусцирована; затем @0xB58=0 | §49 | разобран | 100% |
| [`0x12a64`](functions_mcu/func_0x12a64.md) | 18 | код E | 0x4c84(0, 1); 0x124c0() — очередь/событие | §49 | разобран | 100% |
| [`0x12a78`](functions_mcu/func_0x12a78.md) | 110 | код E | — | — | не начат | 0% |
| [`0x12aec`](functions_mcu/func_0x12aec.md) | 96 | код E | — | — | не начат | 0% |
| [`0x12b50`](functions_mcu/func_0x12b50.md) | 190 | код E | — | — | не начат | 0% |
| [`0x12c24`](functions_mcu/func_0x12c24.md) | 56 | код E | счётчик с насыщением: u16@0xB7A++, кап 0xC8; гейт bit0(u32@0xB76) | §49 | разобран | 100% |
| [`0x12d04`](functions_mcu/func_0x12d04.md) | 134 | код E | — | — | не начат | 0% |
| [`0x12d90`](functions_mcu/func_0x12d90.md) | 190 | код E | — | — | не начат | 0% |
| [`0x12e64`](functions_mcu/func_0x12e64.md) | 56 | код E | счётчик с насыщением: u16@0xB7C++, кап 0xC8; гейт bit2(u32@0xB76) | §49 | разобран | 100% |
| [`0x12f44`](functions_mcu/func_0x12f44.md) | 134 | код E | — | — | не начат | 0% |
| [`0x12fd0`](functions_mcu/func_0x12fd0.md) | 8 | код E | thunk → 0x12b50 | §48 | ID | 25% |
| [`0x12fd8`](functions_mcu/func_0x12fd8.md) | 8 | код E | thunk → 0x12d90 | §48 | ID | 25% |
| [`0x12fe0`](functions_mcu/func_0x12fe0.md) | 66 | код E | — | — | не начат | 0% |
| [`0x1302c`](functions_mcu/func_0x1302c.md) | 134 | код E | init/драйвер трёх USART | §6.5 | частично | 50% |
| [`0x130f2`](functions_mcu/func_0x130f2.md) | 80 | код E | — | — | не начат | 0% |
| [`0x13148`](functions_mcu/func_0x13148.md) | 168 | код E | — | — | не начат | 0% |
| [`0x131fc`](functions_mcu/func_0x131fc.md) | 130 | код E | — | — | не начат | 0% |
| [`0x13284`](functions_mcu/func_0x13284.md) | 130 | код E | — | — | не начат | 0% |
| [`0x1330c`](functions_mcu/func_0x1330c.md) | 106 | код E | — | — | не начат | 0% |
| [`0x1337c`](functions_mcu/func_0x1337c.md) | 1472 | код E | — | — | не начат | 0% |
| [`0x1395c`](functions_mcu/func_0x1395c.md) | 36 | код E | обработчик флага: byte@0xCAC → byte@0xA73 (сброс после обработки) | §49 | разобран | 100% |
| [`0x139ac`](functions_mcu/func_0x139ac.md) | 14 | код E | CMD: {u32=3} → 0x13c78 (отправка) | §49 | разобран | 100% |
| [`0x139fc`](functions_mcu/func_0x139fc.md) | 226 | код E | — | — | не начат | 0% |
| [`0x13b14`](functions_mcu/func_0x13b14.md) | 72 | код E | — | — | не начат | 0% |
| [`0x13b60`](functions_mcu/func_0x13b60.md) | 84 | код E | — | — | не начат | 0% |
| [`0x13bb8`](functions_mcu/func_0x13bb8.md) | 48 | код E | **retry-send**: 0x13b60-проверка + задержка 0x1F4; гейт u16@0x30CF | §49 | разобран | 100% |
| [`0x13c5c`](functions_mcu/func_0x13c5c.md) | 18 | код E | **CMD 0x4B**: 0x11d6(&@0x3084, 0x4B); byte@0xCAC=1 (флаг запроса) | §49 | разобран | 100% |
| [`0x13c78`](functions_mcu/func_0x13c78.md) | 392 | код E | — | — | не начат | 0% |
| [`0x14368`](functions_mcu/func_0x14368.md) | 66 | код F | — | — | не начат | 0% |
| [`0x147ac`](functions_mcu/func_0x147ac.md) | 78 | код G | — | — | не начат | 0% |
| [`0x14802`](functions_mcu/func_0x14802.md) | 284 | код G | — | — | не начат | 0% |
| [`0x14924`](functions_mcu/func_0x14924.md) | 48 | код G | I2C read с 3 попытками: 0xcee0(8, 0x91B2, 2) → u16@0xF95+0x1E | §49 | разобран | 100% |
| [`0x14958`](functions_mcu/func_0x14958.md) | 76 | код G | — | — | не начат | 0% |
| [`0x14ed0`](functions_mcu/func_0x14ed0.md) | 110 | код G | — | — | не начат | 0% |
| [`0x14f50`](functions_mcu/func_0x14f50.md) | 1572 | код G | — | — | не начат | 0% |
| [`0x155ac`](functions_mcu/func_0x155ac.md) | 64 | код G | I2C read: буфер {u16=0, len=4, addr=0x3E} → 0x1e72; результат → u16@0xF95+0x20 | §49 | разобран | 100% |
| [`0x15640`](functions_mcu/func_0x15640.md) | 108 | код G | — | — | не начат | 0% |
| [`0x156ac`](functions_mcu/func_0x156ac.md) | 92 | код G | — | — | не начат | 0% |
| [`0x1570c`](functions_mcu/func_0x1570c.md) | 72 | код G | — | — | не начат | 0% |
| [`0x15758`](functions_mcu/func_0x15758.md) | 48 | код G | I2C-запись: 0x11d6(0x80c, &@0x1FD4); 0x11c8(0x800, &@0x27E0); 0x11c8(0x800, &@0x1FD4); @0x1FD4+0x804 = 0x800 | §49 | разобран | 100% |
| [`0x15790`](functions_mcu/func_0x15790.md) | 76 | код G | — | — | не начат | 0% |
| [`0x157e0`](functions_mcu/func_0x157e0.md) | 266 | код G | — | — | не начат | 0% |
| [`0x158f8`](functions_mcu/func_0x158f8.md) | 22 | код G | I2C-старт: byte@0xB8C=1; 0x15ffc(0xA); byte@0x1FAC+3=1 | §49 | разобран | 100% |
| [`0x15918`](functions_mcu/func_0x15918.md) | 242 | код G | — | — | не начат | 0% |
| [`0x15a1c`](functions_mcu/func_0x15a1c.md) | 58 | код G | инициал структуры @0x1FAC (~0x20B, дефолты 0/0xFFFF) + 0x15758 (I2C) | §49 | разобран | 100% |
| [`0x15a60`](functions_mcu/func_0x15a60.md) | 280 | код G | — | — | не начат | 0% |
| [`0x15b84`](functions_mcu/func_0x15b84.md) | 236 | код G | — | — | не начат | 0% |
| [`0x15c94`](functions_mcu/func_0x15c94.md) | 66 | код G | — | — | не начат | 0% |
| [`0x15ce0`](functions_mcu/func_0x15ce0.md) | 36 | код G | retry-счётчик @0xC84: инкремент до 3; при byte@0x36==1 сброс | §49 | разобран | 100% |
| [`0x15d14`](functions_mcu/func_0x15d14.md) | 216 | код G | — | — | не начат | 0% |
| [`0x15df4`](functions_mcu/func_0x15df4.md) | 242 | код G | — | — | не начат | 0% |
| [`0x15f00`](functions_mcu/func_0x15f00.md) | 116 | код G | — | — | не начат | 0% |
| [`0x15ffc`](functions_mcu/func_0x15ffc.md) | 56 | код G | установка указателя @0xC80; при byte@0xB8C==1: сброс/декремент счётчика + 0x15a1c | §49 | разобран | 100% |
| [`0x16040`](functions_mcu/func_0x16040.md) | 252 | код G | — | — | не начат | 0% |
| [`0x16176`](functions_mcu/func_0x16176.md) | 40 | код G | бинарный поиск по i16-массиву (возврат индекса/0xFFFF) | §49 | разобран | 100% |
| [`0x1619e`](functions_mcu/func_0x1619e.md) | 40 | код G | бинарный поиск по u32-массиву | §49 | разобран | 100% |
| [`0x161ea`](functions_mcu/func_0x161ea.md) | 56 | код G | u32 udiv (вариант с циклической коррекцией) | §49 | разобран | 100% |
| [`0x16222`](functions_mcu/func_0x16222.md) | 68 | код G | — | — | не начат | 0% |
| [`0x16288`](functions_mcu/func_0x16288.md) | 24 | код G | signed-подготовка к делению (знак → 0x80000000) | §49 | разобран | 100% |
| [`0x162ce`](functions_mcu/func_0x162ce.md) | 24 | код G | signed-подготовка к делению (вариант) | §49 | разобран | 100% |
| [`0x16328`](functions_mcu/func_0x16328.md) | 24 | код G | signed-подготовка к делению (вариант) | §49 | разобран | 100% |
| [`0x163b4`](functions_mcu/func_0x163b4.md) | 76 | код G | — | — | не начат | 0% |
| [`0x16410`](functions_mcu/func_0x16410.md) | 94 | код G | — | — | не начат | 0% |
| [`0x1647c`](functions_mcu/func_0x1647c.md) | 86 | код G | — | — | не начат | 0% |
| [`0x16588`](functions_mcu/func_0x16588.md) | 558 | код G | — | — | не начат | 0% |
| [`0x167b6`](functions_mcu/func_0x167b6.md) | 202 | код G | — | — | не начат | 0% |
| [`0x16880`](functions_mcu/func_0x16880.md) | 184 | код G | — | — | не начат | 0% |
| [`0x16938`](functions_mcu/func_0x16938.md) | 184 | код G | — | — | не начат | 0% |
| [`0x169f0`](functions_mcu/func_0x169f0.md) | 178 | код G | — | — | не начат | 0% |
| [`0x16aa2`](functions_mcu/func_0x16aa2.md) | 128 | код G | — | — | не начат | 0% |
| [`0x16b22`](functions_mcu/func_0x16b22.md) | 178 | код G | — | — | не начат | 0% |
| [`0x16bd4`](functions_mcu/func_0x16bd4.md) | 442 | код G | — | — | не начат | 0% |
| [`0x16d8e`](functions_mcu/func_0x16d8e.md) | 436 | код G | — | — | не начат | 0% |
| [`0x16f42`](functions_mcu/func_0x16f42.md) | 156 | код G | — | — | не начат | 0% |
| [`0x16fde`](functions_mcu/func_0x16fde.md) | 156 | код G | — | — | не начат | 0% |
| [`0x17094`](functions_mcu/func_0x17094.md) | 76 | код G | — | — | не начат | 0% |
| [`0x170e0`](functions_mcu/func_0x170e0.md) | 76 | код G | — | — | не начат | 0% |
| [`0x1712c`](functions_mcu/func_0x1712c.md) | 36 | код G | u64 shift: (r0:r1) << r2 / >> (32-r2) комбинация | §49 | разобран | 100% |
| [`0x17150`](functions_mcu/func_0x17150.md) | 32 | код G | u64 знак: если старший бит → -1, иначе значение [sp+4] | §49 | разобран | 100% |
| [`0x17170`](functions_mcu/func_0x17170.md) | 164 | код G | — | — | не начат | 0% |
| [`0x17214`](functions_mcu/func_0x17214.md) | 164 | код G | — | — | не начат | 0% |
| [`0x172b8`](functions_mcu/func_0x172b8.md) | 78 | код G | — | — | не начат | 0% |
| [`0x17306`](functions_mcu/func_0x17306.md) | 100 | код G | — | — | не начат | 0% |
| [`0x1736a`](functions_mcu/func_0x1736a.md) | 96 | код G | — | — | не начат | 0% |
| [`0x173cc`](functions_mcu/func_0x173cc.md) | 294 | код G | — | — | не начат | 0% |
| [`0x17736`](functions_mcu/func_0x17736.md) | 108 | код G | — | — | не начат | 0% |
| [`0x177d6`](functions_mcu/func_0x177d6.md) | 8 | код G | cold-tail гигантской функции региона 0x17xxx (b #0x173bc); артефакт детекции | §48 | ID | 25% |
| [`0x178c4`](functions_mcu/func_0x178c4.md) | 12 | код G | dead-фрагмент: после strh — НЕВАЛИДНАЯ инструкция 0x6EF5 (Unicorn: UC_ERR_INSN_INVALID); перед ним u16-таблица @0x177DE; дыра 0x177DE..0x19A1C = одна гигантская функция, пропущенная каноническим детектором | §48 | ID | 25% |
| [`0x19a1c`](functions_mcu/func_0x19a1c.md) | 76 | код I | — | — | не начат | 0% |
| [`0x19a68`](functions_mcu/func_0x19a68.md) | 36 | код I | memcpy (байтовый цикл) | §49 | разобран | 100% |
| [`0x19a8c`](functions_mcu/func_0x19a8c.md) | 14 | код I | memset (байты r2, count r1) | §49 | разобран | 100% |
| [`0x19a9e`](functions_mcu/func_0x19a9e.md) | 18 | код I | memset (перестановка аргументов → 0x19a8c) | §49 | разобран | 100% |
| [`0x19ab0`](functions_mcu/func_0x19ab0.md) | 162 | код I | — | — | не начат | 0% |
| [`0x19b64`](functions_mcu/func_0x19b64.md) | 120 | код I | — | — | не начат | 0% |
| [`0x19bdc`](functions_mcu/func_0x19bdc.md) | 124 | код I | — | — | не начат | 0% |
| [`0x19c58`](functions_mcu/func_0x19c58.md) | 328 | код I | — | — | не начат | 0% |
| [`0x19dbc`](functions_mcu/func_0x19dbc.md) | 202 | код I | — | — | не начат | 0% |
| [`0x19e8c`](functions_mcu/func_0x19e8c.md) | 234 | код I | — | — | не начат | 0% |
| [`0x19f7c`](functions_mcu/func_0x19f7c.md) | 44 | код I | сравнение u64 (r0:r1) с r2 со знаком (udiv-подобная подготовка) | §49 | разобран | 100% |
| [`0x19fae`](functions_mcu/func_0x19fae.md) | 16 | код I | (r0+r1) → 0x1a0f8(_, 0, 0x96) — масштабирование с deadband | §49 | разобран | 100% |
| [`0x19fbe`](functions_mcu/func_0x19fbe.md) | 14 | код I | 0x1a0f8(0, 1, 0x96) — масштабирование с deadband (инверсия) | §49 | разобран | 100% |
| [`0x19fcc`](functions_mcu/func_0x19fcc.md) | 34 | код I | abs(r0) → lookup 0x1a184(0, sign, 0x433) | §49 | разобран | 100% |
| [`0x19ff4`](functions_mcu/func_0x19ff4.md) | 24 | код I | lookup 0x1a184(0, 0, 0x433) — калибровочная таблица | §49 | разобран | 100% |
| [`0x1a010`](functions_mcu/func_0x1a010.md) | 50 | код I | **масштабирование с deadband**: |v|<0x7f → 0; [0x7f..0x96] → линейное; иначе (v-0x96)<<1; знак сохраняется; вызов из 0x1D898 (§22) | §49 | разобран | 100% |
| [`0x1a052`](functions_mcu/func_0x1a052.md) | 36 | код I | range-check r2>>21 vs r3; зона 0x3FF+0x34 → asr; иначе (r2-0x3CD)<<1 | §49 | разобран | 100% |
| [`0x1a080`](functions_mcu/func_0x1a080.md) | 32 | код I | u32 lsl на r1 битов (полный) | §49 | разобран | 100% |
| [`0x1a0a0`](functions_mcu/func_0x1a0a0.md) | 34 | код I | u32 asr на r1 битов (полный) | §49 | разобран | 100% |
| [`0x1a0c2`](functions_mcu/func_0x1a0c2.md) | 38 | код I | u32 lsr на r1 битов (полный) | §49 | разобран | 100% |
| [`0x1a16a`](functions_mcu/func_0x1a16a.md) | 26 | код I | u64 sub (r0:r1 - r2:r3) | §49 | разобран | 100% |
| [`0x1a184`](functions_mcu/func_0x1a184.md) | 164 | код I | — | — | не начат | 0% |
| [`0x1a24c`](functions_mcu/func_0x1a24c.md) | 86 | код I | — | — | не начат | 0% |
| [`0x1a2a4`](functions_mcu/func_0x1a2a4.md) | 90 | код I | — | — | не начат | 0% |
| [`0x1a31c`](functions_mcu/func_0x1a31c.md) | 522 | код I | ADC1: стейт-машина выборки (системный тик ~1 кГц) | §22, §40 | разобран | 100% |
| [`0x1a5c4`](functions_mcu/func_0x1a5c4.md) | 12 | код I | ADC1+0x18 |= 8 (bit3; caller — ADC-таск 0x1A31C) | §48 | разобран | 100% |
| [`0x1a5d4`](functions_mcu/func_0x1a5d4.md) | 12 | код I | ADC1+0x18 |= 0x20 (bit5; caller — DMA+ADC 0x1E298) | §48 | разобран | 100% |
| [`0x1a5e6`](functions_mcu/func_0x1a5e6.md) | 12 | код I | «own»: трамплин к S-box-блоку 0x1a7ac (реальный старт 0x1a5e4 `mov r2,r1` — без пролога, артефакт детекции; bl из 0x21c64) | §36.3, §37 | разобран | 100% |
| [`0x1a5f2`](functions_mcu/func_0x1a5f2.md) | 8 | код I | «own»: трамплин bl 0x1bfa0 (из 0x1a628) | §27.2, §37 | разобран | 100% |
| [`0x1a5fa`](functions_mcu/func_0x1a5fa.md) | 46 | код I | «own»: XOR двух 16-Б блоков (round, вызов из 0x1a7ac; callers=3) | §37 | разобран | 100% |
| [`0x1a628`](functions_mcu/func_0x1a628.md) | 12 | код I | трамплин к шифру: ldr r0=&0x16aa; bl 0x1bfa0 | §27.2 | разобран | 100% |
| [`0x1a638`](functions_mcu/func_0x1a638.md) | 66 | код I | — | — | не начат | 0% |
| [`0x1a688`](functions_mcu/func_0x1a688.md) | 266 | код I | — | — | не начат | 0% |
| [`0x1a7ac`](functions_mcu/func_0x1a7ac.md) | 136 | код I | «own»: S-box-подстановка + перестановка (16 Б, 10 раундов) | §37 | разобран | 100% |
| [`0x1a838`](functions_mcu/func_0x1a838.md) | 32 | код I | **CRC-32** (полином 0x04C11DB7, MSB-first); вызов из агрегатора 0x1F71C | §49 | разобран | 100% |
| [`0x1a894`](functions_mcu/func_0x1a894.md) | 140 | код I | — | — | не начат | 0% |
| [`0x1a938`](functions_mcu/func_0x1a938.md) | 3296 | код I | батарейные пороги (clamp 10..100) | §22 | частично | 50% |
| [`0x1b67c`](functions_mcu/func_0x1b67c.md) | 1174 | код I | флаги/статус: перегрев ≥46°C → флаг @0x318 | §22 | разобран | 100% |
| [`0x1bb1c`](functions_mcu/func_0x1bb1c.md) | 562 | код I | батарейный замер №2 (struct @0x154) | §25.4 | разобран | 100% |
| [`0x1bd88`](functions_mcu/func_0x1bd88.md) | 118 | код I | — | — | не начат | 0% |
| [`0x1be1c`](functions_mcu/func_0x1be1c.md) | 174 | код I | — | — | не начат | 0% |
| [`0x1bedc`](functions_mcu/func_0x1bedc.md) | 66 | код I | — | — | не начат | 0% |
| [`0x1bf48`](functions_mcu/func_0x1bf48.md) | 78 | код I | МОТОР-ИНИТ: bl 0x1d640/0x1c0b0/0x1c1ac/0x1bedc | §39 | частично | 50% |
| [`0x1bfa0`](functions_mcu/func_0x1bfa0.md) | 150 | код I | табличный шифр (&table @0x16aa, src) | §27.2 | разобран | 100% |
| [`0x1c0b0`](functions_mcu/func_0x1c0b0.md) | 238 | код I | инициализация сенсоров ADC1 | §40 | ID | 25% |
| [`0x1c1ac`](functions_mcu/func_0x1c1ac.md) | 106 | код I | — | — | не начат | 0% |
| [`0x1c234`](functions_mcu/func_0x1c234.md) | 228 | код I | — | — | не начат | 0% |
| [`0x1c34c`](functions_mcu/func_0x1c34c.md) | 1244 | код I | — | — | не начат | 0% |
| [`0x1c838`](functions_mcu/func_0x1c838.md) | 1466 | код I | калибровка/секвенсор: @0xF400/+4 → @0x1e8/@0x1ec | §25 | разобран | 100% |
| [`0x1ce38`](functions_mcu/func_0x1ce38.md) | 522 | код I | — | — | не начат | 0% |
| [`0x1d078`](functions_mcu/func_0x1d078.md) | 610 | код I | state-машина режимов (byte@0x229: 2/3/0x0B) — адрес приблизительный | §34.2 | частично | 50% |
| [`0x1d330`](functions_mcu/func_0x1d330.md) | 142 | код I | — | — | не начат | 0% |
| [`0x1d3d0`](functions_mcu/func_0x1d3d0.md) | 588 | код I | хвост ADC ISR: → TX → SWSTART | §22.6 | разобран | 100% |
| [`0x1d640`](functions_mcu/func_0x1d640.md) | 348 | код I | — | — | не начат | 0% |
| [`0x1d7ac`](functions_mcu/func_0x1d7ac.md) | 102 | код I | — | — | не начат | 0% |
| [`0x1d818`](functions_mcu/func_0x1d818.md) | 86 | код I | — | — | не начат | 0% |
| [`0x1d874`](functions_mcu/func_0x1d874.md) | 26 | код I | lookup через 0x19994(0xBB80): результат → u16@0xF95+2/4 | §49 | разобран | 100% |
| [`0x1d898`](functions_mcu/func_0x1d898.md) | 1254 | код I | батарея/запас хода/температура (0x306/0x30c/0x30e) | §22 | разобран | 100% |
| [`0x1dd8c`](functions_mcu/func_0x1dd8c.md) | 128 | код I | «own»: вспомогательный round (bl из 0x1a814) | §37 | частично | 50% |
| [`0x1de0c`](functions_mcu/func_0x1de0c.md) | 66 | код I | — | — | не начат | 0% |
| [`0x1de5e`](functions_mcu/func_0x1de5e.md) | 70 | код I | — | — | не начат | 0% |
| [`0x1dea4`](functions_mcu/func_0x1dea4.md) | 186 | код I | — | — | не начат | 0% |
| [`0x1df84`](functions_mcu/func_0x1df84.md) | 66 | код I | — | — | не начат | 0% |
| [`0x1dfd8`](functions_mcu/func_0x1dfd8.md) | 344 | код I | периодический таск: флаги → счётчик → сборщик 'a'-кадров 0x211f8 | §47 | частично | 50% |
| [`0x1e1a0`](functions_mcu/func_0x1e1a0.md) | 200 | код I | — | — | не начат | 0% |
| [`0x1e298`](functions_mcu/func_0x1e298.md) | 34 | код I | DMA+ADC (вызов из 0x1a31c) | §40 | частично | 50% |
| [`0x1e2ca`](functions_mcu/func_0x1e2ca.md) | 36 | код I | SysTick init: RVR=r0-1, CVR=0, CTRL=7 | §49 | разобран | 100% |
| [`0x1e2f8`](functions_mcu/func_0x1e2f8.md) | 164 | код I | RCC+GPIOC AF-конфиг (MODER=0x044AA200) | §39 | частично | 50% |
| [`0x1e3a4`](functions_mcu/func_0x1e3a4.md) | 50 | код I | **программный сброс**: конфиг RCC+0x40, dsb, SCB_AIRCR = 0x5FA0004 (SYSRESETREQ+VECTKEY), цикл | §49 | разобран | 100% |
| [`0x1e410`](functions_mcu/func_0x1e410.md) | 106 | код I | — | — | не начат | 0% |
| [`0x1e480`](functions_mcu/func_0x1e480.md) | 180 | код I | ISR USART3 (линк к BLE-чипу): статус, сброс PE/FE/ORE | §6.5 | разобран | 100% |
| [`0x1e658`](functions_mcu/func_0x1e658.md) | 218 | код I | — | — | не начат | 0% |
| [`0x1e9e0`](functions_mcu/func_0x1e9e0.md) | 1914 | код I | RX-парсер протокола USART3 | §6.5 | частично | 50% |
| [`0x1f1c0`](functions_mcu/func_0x1f1c0.md) | 6 | код I | setter USART3+4 (вызов из TX-кольца 0x1F600) | §48 | разобран | 100% |
| [`0x1f1cc`](functions_mcu/func_0x1f1cc.md) | 114 | код I | MCU→BLE: сборщик запросов `63 CMD` (шаблон кадра) | §32 | разобран | 100% |
| [`0x1f600`](functions_mcu/func_0x1f600.md) | 156 | код I | RX USART3: кольцо + диспетчер по таблице дескрипторов | §6.7 | разобран | 100% |
| [`0x1f6b4`](functions_mcu/func_0x1f6b4.md) | 94 | код I | TX: сборка дескриптора [type=2][len][data] | §6.5 | разобран | 100% |
| [`0x1f71c`](functions_mcu/func_0x1f71c.md) | 6860 | код I | агрегатор: 24-состоянная машина (jump-table по CTX[0x10]) | §22.5 | разобран | 100% |
| [`0x211ec`](functions_mcu/func_0x211ec.md) | 6 | код I | setter UART4+4 (вызов из TX-кольца 0x216E4) | §48 | разобран | 100% |
| [`0x211f8`](functions_mcu/func_0x211f8.md) | 1246 | код I | сборщик кадров 'a'/'a1' в TX-кольцо @0x10b5 (state byte@0x18A: 0→1→2→0; рейт-лимиты 1920/3200 тиков) | §47 | разобран | 100% |
| [`0x216e4`](functions_mcu/func_0x216e4.md) | 256 | код I | TX-кольцо @0x10b5 отправитель (UART4) | §28.3 | разобран | 100% |
| [`0x21804`](functions_mcu/func_0x21804.md) | 96 | код I | — | — | не начат | 0% |
| [`0x2186c`](functions_mcu/func_0x2186c.md) | 370 | код I | — | — | не начат | 0% |
| [`0x21a08`](functions_mcu/func_0x21a08.md) | 240 | код I | NVRAM-save таск (гейт byte@0x170==1 + бит31 common+0x14) | §25 | разобран | 100% |
| [`0x21b84`](functions_mcu/func_0x21b84.md) | 60 | код I | NVIC/SCB бит-манипуляция: r0≥0 → массив @0xE000E400; r0<0 → SCB+0x1C зона | §49 | разобран | 100% |
| [`0x21c0c`](functions_mcu/func_0x21c0c.md) | 6 | код I | getter *(u32@RAM[0x28])+4 (двойная индирекция) | §48 | разобран | 100% |
| [`0x21c18`](functions_mcu/func_0x21c18.md) | 34 | код I | NVIC-приоритеты: *(u32@RAM[0x4]) vs flash 0x2710; 0x19968/0x1e2c8; r4!=3 → 0x21b84(~0, r4) | §49 | разобран | 100% |
| [`0x21c64`](functions_mcu/func_0x21c64.md) | 12 | код I | «own»: входной шифр/проверка кадра (initiator BLE) | §36.3, §37 | разобран | 100% |
| [`0x21ca8`](functions_mcu/func_0x21ca8.md) | 364 | код I | инициализация сенсоров ADC1 | §40 | ID | 25% |
| [`0x21e18`](functions_mcu/func_0x21e18.md) | 412 | код I | — | — | не начат | 0% |
| [`0x22000`](functions_mcu/func_0x22000.md) | 406 | код I | — | — | не начат | 0% |
| [`0x221a4`](functions_mcu/func_0x221a4.md) | 66 | код I | — | — | не начат | 0% |
| [`0x221e6`](functions_mcu/func_0x221e6.md) | 78 | код I | — | — | не начат | 0% |
| [`0x22234`](functions_mcu/func_0x22234.md) | 58 | код I | TIM-инициал: toggle RCC_CTLR bit0x10 с задержками 0x22a0c | §49 | разобран | 100% |
| [`0x22274`](functions_mcu/func_0x22274.md) | 790 | код I | — | — | не начат | 0% |
| [`0x225c4`](functions_mcu/func_0x225c4.md) | 18 | код I | set/clear битов RCC_CTLR (+0x0) | §49 | разобран | 100% |
| [`0x225dc`](functions_mcu/func_0x225dc.md) | 18 | код I | set/clear битов RCC+0x60 (расширенный регистр) | §49 | разобран | 100% |
| [`0x225f4`](functions_mcu/func_0x225f4.md) | 556 | код I | — | — | не начат | 0% |
| [`0x22824`](functions_mcu/func_0x22824.md) | 240 | код I | — | — | не начат | 0% |
| [`0x22934`](functions_mcu/func_0x22934.md) | 76 | код I | — | — | не начат | 0% |
| [`0x229d4`](functions_mcu/func_0x229d4.md) | 44 | код I | busy-delay: N итераций, сброс CVR=0xFFFFFF (коэфф. из *(u32@RAM[0x24])) | §49 | разобран | 100% |
| [`0x22a0c`](functions_mcu/func_0x22a0c.md) | 48 | код I | busy-delay: N итераций ожидания SysTick CVR (коэфф. из *(u32@RAM[0x10])) | §49 | разобран | 100% |
| [`0x22a48`](functions_mcu/func_0x22a48.md) | 148 | код I | блок TIM1+TIM3+TIM4 (HAL-функции, регистры +0x10) | §39.1, §41 | разобран | 100% |
| [`0x22b7c`](functions_mcu/func_0x22b7c.md) | 212 | код I | — | — | не начат | 0% |
| [`0x22c70`](functions_mcu/func_0x22c70.md) | 168 | код I | — | — | не начат | 0% |
| [`0x22d2c`](functions_mcu/func_0x22d2c.md) | 204 | код I | HAL timer (доказательство раскладки +0x10) | §39.1 | разобран | 100% |
| [`0x22e0c`](functions_mcu/func_0x22e0c.md) | 186 | код I | — | — | не начат | 0% |
| [`0x22edc`](functions_mcu/func_0x22edc.md) | 188 | код I | — | — | не начат | 0% |
| [`0x22fac`](functions_mcu/func_0x22fac.md) | 126 | код I | — | — | не начат | 0% |
| [`0x23040`](functions_mcu/func_0x23040.md) | 296 | код I | — | — | не начат | 0% |
| [`0x23188`](functions_mcu/func_0x23188.md) | 372 | код I | HAL_UART_Transmit (валидация порта/длины, assert) | §6.5 | разобран | 100% |
| [`0x23374`](functions_mcu/func_0x23374.md) | 262 | код I | 3-проводная шина режима (byte@0x26b ? bl 0x23374 : 0) | §40.7 | частично | 50% |
| [`0x23544`](functions_mcu/func_0x23544.md) | 80 | код I | — | — | не начат | 0% |
| [`0x2360c`](functions_mcu/func_0x2360c.md) | 94 | код I | — | — | не начат | 0% |
| [`0x244d2`](functions_mcu/func_0x244d2.md) | 262 | код J | — | — | не начат | 0% |

**Известные артефакты детекции (ручная перепроверка 2026-08-24):** строка `0x1a5e6` —
тело функции, реально начинающейся в `0x1a5e4` (`mov r2,r1`, без push-пролога — детектор
ловит внутренний push); это «own»-трамплин 0x21c64→0x1a5e4→0x1a7ac. Всё остальное из
именованных функций сверено с дизассембляцией входов и разделами REPORT.md.