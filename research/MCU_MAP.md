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
| разобран | 476 | 39734 | 41.0% |
| частично | 10 | 6964 | 7.2% |
| ID | 30 | 970 | 1.0% |
| не начат | 162 | 49264 | 50.8% |
| **всего** | **678** | **96932** | **44.8% декомпилировано** |

Подробности по каждой функции: `functions_mcu/func_0x<off>.md` (дизассембляция,
литералы, callees/callers). Разделы REPORT.md — где описана семантика.

Перегенерация: `python research/scripts/gen_maps.py` (список функций — из
`functions_mcu/README.md`; каталог разобранных блоков — в gen_maps.py, ANALYZED_MCU).

| offset | размер | регион | имя / роль | разделы | статус | % |
|---|---|---|---|---|---|---|
| [`0x01218`](functions_mcu/func_0x01218.md) | 34 | код A | abs(r0) → 0x12aa(0, 0, 0x433) | §49 | разобран | 100% |
| [`0x0123e`](functions_mcu/func_0x0123e.md) | 46 | код A | **u64 масштаб 2^(r2-0x433)**: r1' = (r1&0xFFFFF)\|0x100000; r2 < 0x3FF → {r1', 0} (сентинел); [0x3FF..0x433] → u64lsr({r1':r0}, 0x433-r2) через 0x126c; > 0x433 → {r1', r0 << (r2-0x433)}; прямых callers нет | §49/§50.6 | разобран | 100% |
| [`0x0126c`](functions_mcu/func_0x0126c.md) | 32 | код A | **u64 LSR**: (r1:r0) >> r2 — логический сдвиг вправо (количество в r2); вызов из 0x123e | §49/§50.6 | разобран | 100% |
| [`0x0128c`](functions_mcu/func_0x0128c.md) | 30 | код A | u64 add (r0:r1 + r2:r3) | §49 | разобран | 100% |
| [`0x012aa`](functions_mcu/func_0x012aa.md) | 156 | код A | — | — | не начат | 0% |
| [`0x01346`](functions_mcu/func_0x01346.md) | 322 | код A | — | — | не начат | 0% |
| [`0x01494`](functions_mcu/func_0x01494.md) | 48 | код A | **сравнение g(a) vs g(b)**: a={r1:r0}, b={r3:r2}; g(x)=x при bit63(x)=1, иначе 2^63-x; флаги = cmp старших слов (+cmpeq младших при равенстве). Для бит-паттернов IEEE-double это сравнение в порядке, обратном числовому (bhs ⇔ a≤b); callers: float-код 0x16040 (§50.7) | §49/§50.7 | разобран | 100% |
| [`0x0152a`](functions_mcu/func_0x0152a.md) | 86 | код A | **RLE-декодер**: count [2:0] (или байт), бит4 → literal/backward-copy; return 0 | §50 | разобран | 100% |
| [`0x01580`](functions_mcu/func_0x01580.md) | 26 | код A | RCC-расширенный инициал: r5==0 → 0xc490(0x100)+0xc478(r4); иначе 0xc4b0/0xc4c8 | §49 | разобран | 100% |
| [`0x015aa`](functions_mcu/func_0x015aa.md) | 198 | код A | — | — | не начат | 0% |
| [`0x01670`](functions_mcu/func_0x01670.md) | 86 | код A | **DMA1 ch1 init (ADC)**: struct {0x4002084C, &u16@0xB7E, ..., 0x80, 0x100, 0x400, 0x20} → 0x4f70(DMA1); 0x4fac; 0x4f38; вызов из 0x175c (DMA enable) | §50 | разобран | 100% |
| [`0x016d4`](functions_mcu/func_0x016d4.md) | 42 | код A | **DMA1 reset**: 0x1940(); DMA on; цикл i<2: 0x4e50(0x40020030); byte@0xB82=0 | §49 | разобран | 100% |
| [`0x0170c`](functions_mcu/func_0x0170c.md) | 68 | код A | **медиан-фильтр**: 7 u16 из @0xB7E → sort (0x506a) → среднее средних 3 (0x5044) → u16@0xB84; вызов из ADC-цепи 0x3780/0x8b10 | §50 | разобран | 100% |
| [`0x0175c`](functions_mcu/func_0x0175c.md) | 42 | код A | **DMA1 enable**: 0x1940(); цикл i<2: 0x1858(i) (рег. обработчика), 0x1670(), 0x18fc(i) (конфиг канала); byte@0xB82=1 | §49 | разобран | 100% |
| [`0x0178c`](functions_mcu/func_0x0178c.md) | 98 | код A | DMA1 wait: enable (0x182a/0x1814); poll 0x189e(0x20) до 0x1388; 0x1974; poll 0x1884 до 0x3E8; 0x1840(1) | §50 | разобран | 100% |
| [`0x017f4`](functions_mcu/func_0x017f4.md) | 28 | код A | вкл/выкл DMA (база 0x40020800) через 0xc644 | §49 | разобран | 100% |
| [`0x01858`](functions_mcu/func_0x01858.md) | 40 | код A | регистратор обработчика: запись в таблицу @0x1A8D0 (индекс r0) | §49 | разобран | 100% |
| [`0x018b0`](functions_mcu/func_0x018b0.md) | 66 | код A | **DMA1-канал**: строит регистры канала из cfg-структуры (+4/+8/+0x2C, маски 0xFFF0FEFF/0xFFF1F7FD) | §50 | разобран | 100% |
| [`0x018fc`](functions_mcu/func_0x018fc.md) | 60 | код A | **DMA1-канал**: struct {1,1,0xE0000,0,2} → 0x18b0(DMA1); таблица @0x1A8D0 (шаг 8) + 0x15aa | §49 | разобран | 100% |
| [`0x01940`](functions_mcu/func_0x01940.md) | 52 | код A | **RCC-инициал расширенных регистров**: AWDCR\|=1, BDCR\|=0xE\|0x1000, 0x1580(2,0) | §49 | разобран | 100% |
| [`0x01984`](functions_mcu/func_0x01984.md) | 102 | код A | напряжение-хендлер: 0x87ec(); toggle bit3(@0xA72); счётчик @0xA74 (кап 3); если !bit3 → 0x8b58+0x8b10 (ADC→мВ) | §50 | разобран | 100% |
| [`0x019f4`](functions_mcu/func_0x019f4.md) | 100 | код A | флаг-хендлер: bit1(@0xF95+0xC) && !bit2(@0x15F7+0x11); счётчик @0xA41 (кап flash 0x19E5E+0xD); сброс флагов | §50 | разобран | 100% |
| [`0x01a68`](functions_mcu/func_0x01a68.md) | 70 | код A | порог #6: u16@0xF95+6 ≥ flash 0x19E5E+0x18; счётчик @0xA40 (кап +0x1B); clear bit4(@0xF95+0xC) | §50 | разобран | 100% |
| [`0x01abc`](functions_mcu/func_0x01abc.md) | 12 | код A | последовательность: 0x1a68 + 0x19f4 | §48 | ID | 25% |
| [`0x01ac8`](functions_mcu/func_0x01ac8.md) | 268 | код A | — | — | не начат | 0% |
| [`0x01bdc`](functions_mcu/func_0x01bdc.md) | 42 | код A | **I2C2 read**: {code16, len=2} → 0x1e72(op=8, dev=0x3E) — чтение регистра чипа I2C2 | §49 | разобран | 100% |
| [`0x01c1c`](functions_mcu/func_0x01c1c.md) | 42 | код A | **I2C2 read**: {code16, len=2} → 0x90a0(base=0x40005800) — чтение регистра чипа I2C2 | §49 | разобран | 100% |
| [`0x01c60`](functions_mcu/func_0x01c60.md) | 26 | код A | I2C2-цепочка #1: → 0x1e52 → 0x214c → 0x8f7c(I2C2=0x40005800) | §49 | разобран | 100% |
| [`0x01c7a`](functions_mcu/func_0x01c7a.md) | 52 | код A | I2C2 read: буфер {u16=0, len=2, addr=0x3E} → 0x1e72; результат → u16@0xF95+0x1E | §49 | разобран | 100% |
| [`0x01cea`](functions_mcu/func_0x01cea.md) | 12 | код A | последовательность: 0x1fe0 + 0x20d8 | §48 | ID | 25% |
| [`0x01cf6`](functions_mcu/func_0x01cf6.md) | 54 | код A | init-подблок: 0x1d06(1) + 0x1d1e(1) | §49 | разобран | 100% |
| [`0x01d78`](functions_mcu/func_0x01d78.md) | 112 | код A | I2C read reg 5 (2B) → u16@0xA7C (BE); 3 попытки | §50 | разобран | 100% |
| [`0x01dec`](functions_mcu/func_0x01dec.md) | 8 | код A | thunk → 0x29e8 | §48 | ID | 25% |
| [`0x01df4`](functions_mcu/func_0x01df4.md) | 64 | код A | **мега-инициал**: 15 последовательных bl (0x3b2a, 0x36f4, 0xced0, 0x9b44, 0x9f70, 0xc098, 0x11978, 0x119c4, 0x3034, 0x1cf6, ...) | §49 | разобран | 100% |
| [`0x01e34`](functions_mcu/func_0x01e34.md) | 30 | код A | сумма массива байтов (u8) | §49 | разобран | 100% |
| [`0x01e52`](functions_mcu/func_0x01e52.md) | 32 | код A | I2C2-цепочка #2: пересборка аргументов → 0x214c | §49 | разобран | 100% |
| [`0x01e72`](functions_mcu/func_0x01e72.md) | 32 | код A | I2C2-цепочка #3: → 0x2730 → 0x9048 → 0x8f7c(I2C2) | §49 | разобран | 100% |
| [`0x01e94`](functions_mcu/func_0x01e94.md) | 324 | код A | — | — | не начат | 0% |
| [`0x01fe0`](functions_mcu/func_0x01fe0.md) | 200 | код A | — | — | не начат | 0% |
| [`0x020c4`](functions_mcu/func_0x020c4.md) | 16 | код A | I2C2 wr reg 0x38 = u32@0x162D | §49 | разобран | 100% |
| [`0x020d8`](functions_mcu/func_0x020d8.md) | 76 | код A | флаг-хендлер: bit3(@0xA71); счётчик @0xA7A (кап 5) → 0xaf94(*(u32@RAM[0xDD8])) + delay 0x1F4; если 0x2a5c → clear bit3 | §50 | разобран | 100% |
| [`0x02138`](functions_mcu/func_0x02138.md) | 16 | код A | I2C2 wr reg 0x36 = u32@0x162B | §49 | разобран | 100% |
| [`0x0214c`](functions_mcu/func_0x0214c.md) | 36 | код A | I2C2 write: 0x8f7c(op=8, reg=r0, buf=stack) | §49 | разобран | 100% |
| [`0x0218c`](functions_mcu/func_0x0218c.md) | 76 | код A | I2C read reg 0x83 (2B) → u16@0xB42 (если != 0xFFFF); вызов из 0x8afc | §50 | разобран | 100% |
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
| [`0x02770`](functions_mcu/func_0x02770.md) | 68 | код B | **I2C2 wr**: {code16, val16, len=4} → 0x90a0(0x40005800, dev 0x3E) — запись регистра чипа | §50 | разобран | 100% |
| [`0x0280c`](functions_mcu/func_0x0280c.md) | 88 | код B | **I2C2 batch write 0x11B**: {u16 code, [r5&FF, r5>>8] + r6[0..0xF]} → 0x9048(I2C2, dev 0x3E); вызов из 0xc158 | §50 | разобран | 100% |
| [`0x029e8`](functions_mcu/func_0x029e8.md) | 104 | код B | **handler-table dispatch**: таблица @0xADC (u32 ptr), индекс u32@0xB48; пусто → 0x23c4+0x1e94; иначе blx; set/clear bit(byte@0xB48) в u32@*(u32@RAM[0xAC8]); idx++ | §50 | разобран | 100% |
| [`0x02a5c`](functions_mcu/func_0x02a5c.md) | 16 | код B | флаг 0x1bdc(0x9A) & 1 | §49 | разобран | 100% |
| [`0x02a6c`](functions_mcu/func_0x02a6c.md) | 28 | код B | UART-инициал: конфиг из flash-структуры + 0x13c5c(0x4B) (CMD 0x4B) | §49 | разобран | 100% |
| [`0x02a94`](functions_mcu/func_0x02a94.md) | 132 | код B | — | — | не начат | 0% |
| [`0x02b2c`](functions_mcu/func_0x02b2c.md) | 124 | код B | **boot-конфиг из flash @0x1A8xx**: 0xc624(1); 0x332c(flash 0x1A827, 2); [0x1A8CC] → sp; 0x307c (varargs event); ldm 0x1A878/0x1A8B0 → 0x3278/0x3220; {u32@0x1AD8, 0x96}; 0x130e0/0x12fe0/0x4f38/0x130c8 (флаги) | §50 | разобран | 100% |
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
| [`0x0310c`](functions_mcu/func_0x0310c.md) | 68 | код B | **boot clock init**: 0xc664(0x10000000); 0xc6a4/c29c/c6fc/c6e4; poll 0xc858(0x61)==0; 0xc5f0(0x200); **0xce70 (WWDG window)** | §50 | разобран | 100% |
| [`0x03150`](functions_mcu/func_0x03150.md) | 24 | код B | event {u32=0, u16=0x7F, u32=0x136} → 0xcd0c | §49 | разобран | 100% |
| [`0x03168`](functions_mcu/func_0x03168.md) | 96 | код B | счётчик: если @0x2F==1 && @0x2E==1 → u16@0xB74 += byte@0x3F; ≤ 0x258 → @0x37=1, иначе reset+@0x37=2 | §50 | разобран | 100% |
| [`0x031dc`](functions_mcu/func_0x031dc.md) | 66 | код B | event {2, 8, 0x14, 0x18} → 0xcd80(0); {0xD, 1, 1, 0x40} → 0xca3c(0) — GPIO-настройка пинов | §50 | разобран | 100% |
| [`0x032f4`](functions_mcu/func_0x032f4.md) | 54 | код B | EXTI-настройка: RCC-enable + remap(7) + 0x40010414=0x80 + 0x59a4() | §49 | разобран | 100% |
| [`0x0332c`](functions_mcu/func_0x0332c.md) | 574 | код B | — | — | не начат | 0% |
| [`0x03588`](functions_mcu/func_0x03588.md) | 84 | код B | **GPIO B/C/D/A config для NVRAM**: struct {0xFFFF, flags} → 0x85c8(GPIOB/C/D); {0x9FFF} → GPIOA; вызов из 0x2d5c (NVRAM flash write) | §50 | разобран | 100% |
| [`0x035ec`](functions_mcu/func_0x035ec.md) | 18 | код B | SysTick: выкл. TICKINT (CTRL &= ~2) | §49 | разобран | 100% |
| [`0x03600`](functions_mcu/func_0x03600.md) | 96 | код B | **SysTick период**: udiv(val, 0x3E8); SysTick LOAD(0xE000E014) = n-1; CTRL(0xE000E010) = 7; NVIC-priority по irq | §50 | разобран | 100% |
| [`0x03668`](functions_mcu/func_0x03668.md) | 88 | код B | **charger detection**: 0x8afc(); если нет флагов заряда и u32@0xF95+0xD → I2C read reg 0x9335 (8B) → byte@0xB44=1 | §50 | разобран | 100% |
| [`0x036f4`](functions_mcu/func_0x036f4.md) | 12 | код B | последовательность: 0x10900 + 0x3b00; init-подблок: 0x3700() + 0xc984() | §48, §49 | разобран | 100% |
| [`0x03700`](functions_mcu/func_0x03700.md) | 54 | код B | поиск в таблице @0x92C (0x11 записей) через 0x583c | §49 | разобран | 100% |
| [`0x03740`](functions_mcu/func_0x03740.md) | 40 | код B | event: u16@0x1048 → 0xcd80(2) + 0xcda4() | §49 | разобран | 100% |
| [`0x03780`](functions_mcu/func_0x03780.md) | 78 | код B | **расчёт напряжения**: i8@0xFC7+2 - i8@0xFC7+1 ≤ 3 → медиан-фильтр × 0xCE4/2^20 → таблица 0x12804 → -u8@0x44 → i8@0xA6; иначе 0; EEPROM 0x3da0 | §50 | разобран | 100% |
| [`0x037f4`](functions_mcu/func_0x037f4.md) | 64 | код B | инициал структуры @0x304C {0, 0x21000, 0x21000} + 0x84a0(..., 0x2000) с retry | §49 | разобран | 100% |
| [`0x03838`](functions_mcu/func_0x03838.md) | 174 | код B | — | — | не начат | 0% |
| [`0x038ec`](functions_mcu/func_0x038ec.md) | 84 | код B | **TLV + CRC-16 (таблица)**: 4B header + len=byte@+3; CRC-16(0x3c4c) → {hi, lo} в конец; *r2 = len | §50 | разобран | 100% |
| [`0x03940`](functions_mcu/func_0x03940.md) | 22 | код B | 0x3c04(0x8000000, 0x3000, 0) → u32@0xCC (чтение flash?) | §49 | разобран | 100% |
| [`0x0395c`](functions_mcu/func_0x0395c.md) | 10 | код B | thunk → 0xd298(r0=0) | §48 | ID | 25% |
| [`0x03966`](functions_mcu/func_0x03966.md) | 10 | код B | thunk → 0xd298(r0=1) (пара с 0x395c: off/on) | §48 | ID | 25% |
| [`0x03970`](functions_mcu/func_0x03970.md) | 28 | код B | доступ к структуре @0x98: +0x20 = r0 ? r2 : r1; +0x24 = r3 | §49 | разобран | 100% |
| [`0x03994`](functions_mcu/func_0x03994.md) | 52 | код B | поиск в таблице @0x5CC (0x3A записей × 8B): match по +4 → указатель | §49 | разобран | 100% |
| [`0x03a6c`](functions_mcu/func_0x03a6c.md) | 22 | код B | one-shot флаг byte@0x142: если 0 → 1 + bl 0x3a7e | §49 | разобран | 100% |
| [`0x03b20`](functions_mcu/func_0x03b20.md) | 10 | код B | thunk → 0x1bdc(r0=0x9a) | §48 | ID | 25% |
| [`0x03b2a`](functions_mcu/func_0x03b2a.md) | 20 | код B | init-подблок: 0x3b50/0x3b74/0x3b8a/0x3b9c/0x3bb2 (цепочка RCC/периферии) | §49 | разобран | 100% |
| [`0x03b42`](functions_mcu/func_0x03b42.md) | 64 | код B | CRC-16 (полином 0xA001) + mvn (двоичное дополнение) | §49 | разобран | 100% |
| [`0x03b82`](functions_mcu/func_0x03b82.md) | 66 | код B | CRC-16 (poly 0x1021, MSB-first) — пятый вариант CRC-16 | §50 | разобран | 100% |
| [`0x03bc4`](functions_mcu/func_0x03bc4.md) | 62 | код B | CRC-16 (полином 0x1021, MSB-first) — второй вариант | §49 | разобран | 100% |
| [`0x03c04`](functions_mcu/func_0x03c04.md) | 68 | код B | **CRC-32 (poly 0xEDB88320, LSB-first)** — zlib-вариант; вызов из 0x57a0/0x3940 | §50 | разобран | 100% |
| [`0x03c4c`](functions_mcu/func_0x03c4c.md) | 42 | код B | **CRC-16 табличный** (таблица @0x19784, 256 u16) — третий вариант CRC-16 | §49 | разобран | 100% |
| [`0x03c7c`](functions_mcu/func_0x03c7c.md) | 46 | код B | **CRC-7 byte-step**: r0 ^= byte; 8×: msb? ((r0<<1)&0xFF)^7 : (r0<<1)&0xFF — XOR-константа **0x07** (не 0x09!); состояние в r1, байт в r0; эмуляторно подтверждено (§50.7) | §49/§50.7 | разобран | 100% |
| [`0x03cac`](functions_mcu/func_0x03cac.md) | 232 | код B | — | — | не начат | 0% |
| [`0x03da0`](functions_mcu/func_0x03da0.md) | 58 | код B | чтение 4B из EEPROM + CRC-16 (0x8a50) с проверкой; буфер @0xC9C | §49 | разобран | 100% |
| [`0x03de4`](functions_mcu/func_0x03de4.md) | 252 | код B | — | — | не начат | 0% |
| [`0x03f00`](functions_mcu/func_0x03f00.md) | 912 | код B | — | — | не начат | 0% |
| [`0x042b8`](functions_mcu/func_0x042b8.md) | 118 | код B | счётчики: @0x118 (кап 5, гейт GPIOB+0x10 bit) → @0x8A=1; u16@0x116 (кап 0x3E8) → reset | §50 | разобран | 100% |
| [`0x04344`](functions_mcu/func_0x04344.md) | 324 | код B | — | — | не начат | 0% |
| [`0x044c0`](functions_mcu/func_0x044c0.md) | 58 | код B | **range-check**: u16@0xF95+6 ≤ 0x7D0 && u16@0xF95+8 ≥ 0x1194 && i8@0xFC8+1 > -40 && i8@0xFC8+2 < 0x64; гейт byte@0xA73 | §49 | разобран | 100% |
| [`0x04508`](functions_mcu/func_0x04508.md) | 266 | код B | — | — | не начат | 0% |
| [`0x04630`](functions_mcu/func_0x04630.md) | 146 | код B | — | — | не начат | 0% |
| [`0x048d8`](functions_mcu/func_0x048d8.md) | 32 | код B | сумма u16 + mvn (двоичное дополнение) — контрольная сумма | §49 | разобран | 100% |
| [`0x048f8`](functions_mcu/func_0x048f8.md) | 142 | код B | — | — | не начат | 0% |
| [`0x04994`](functions_mcu/func_0x04994.md) | 18 | код B | 0x49ac(); byte@0xD9=0; byte@0xD8=1 (пара флагов) | §49 | разобран | 100% |
| [`0x049b8`](functions_mcu/func_0x049b8.md) | 70 | код B | **mode switch**: r4==2 → 0x16d4 (DMA reset), 0x8348, 0x10770 (SPI1 init), 0x2a6c (UART init), 0x4e08 (poll), delay 0x186A00, 0x1bdc(0x99) | §50 | разобран | 100% |
| [`0x04a04`](functions_mcu/func_0x04a04.md) | 24 | код B | обнуление блока @0x129..0x13C (byte + 3×u32) | §49 | разобран | 100% |
| [`0x04a30`](functions_mcu/func_0x04a30.md) | 26 | код B | поиск в локальной таблице (2 записи) через 0x12f44/0x12d04 | §49 | разобран | 100% |
| [`0x04a4c`](functions_mcu/func_0x04a4c.md) | 160 | код B | — | — | не начат | 0% |
| [`0x04b04`](functions_mcu/func_0x04b04.md) | 28 | код B | поиск в локальной таблице (2 записи, вариант) | §49 | разобран | 100% |
| [`0x04b20`](functions_mcu/func_0x04b20.md) | 150 | код B | — | — | не начат | 0% |
| [`0x04bc0`](functions_mcu/func_0x04bc0.md) | 36 | код B | event queue @0x164C: push {ptr, 0} (slot++ % 6) | §49 | разобран | 100% |
| [`0x04be8`](functions_mcu/func_0x04be8.md) | 36 | код B | event queue @0x164C: push {u16, 0} (slot++ % 6) | §49 | разобран | 100% |
| [`0x04c14`](functions_mcu/func_0x04c14.md) | 100 | код B | **event-очередь wrap**: счётчик @0xB4C++; ring @0x164C (6 слотов): wrap-логика; слоты state==1 && u32@+4 ≤ counter → state=2 | §50 | разобран | 100% |
| [`0x04c84`](functions_mcu/func_0x04c84.md) | 48 | код B | event queue @0x164C: push {*(u32@RAM[0xB4C]), 0} (slot++ % 6) | §49 | разобран | 100% |
| [`0x04cbc`](functions_mcu/func_0x04cbc.md) | 122 | код B | **event-очередь consumer**: счётчик @0xB50++; критсекция (0x2d1c/0x2d34); слоты state==2: delta vs u32@*(u32@RAM[0xB4C]), min → @0xB54; **blx [u32@slot+8](arg=u32@slot+0xC)** | §50 | разобран | 100% |
| [`0x04d48`](functions_mcu/func_0x04d48.md) | 138 | код B | — | — | не начат | 0% |
| [`0x04de0`](functions_mcu/func_0x04de0.md) | 40 | код B | poll: 0x1bdc(0x93)&0x1bdc(0x94) + задержка 0x1F4 | §49 | разобран | 100% |
| [`0x04e08`](functions_mcu/func_0x04e08.md) | 32 | код B | poll: 0x1bdc(0x94) + задержка 0x1F4 | §49 | разобран | 100% |
| [`0x04e28`](functions_mcu/func_0x04e28.md) | 8 | код B | thunk → 0x5000 | §48 | ID | 25% |
| [`0x04e30`](functions_mcu/func_0x04e30.md) | 8 | код B | thunk → 0x4fc0 | §48 | ID | 25% |
| [`0x04e38`](functions_mcu/func_0x04e38.md) | 4 | код B | setter +4 (str r0,[r1,#4]) | §48 | разобран | 100% |
| [`0x04f38`](functions_mcu/func_0x04f38.md) | 24 | код B | set: *(u32@r0) \|= 1; clear: *(u32@r0) &= 0xFFFE (**трюнирует до u16!** асимметрия; mode=r1; §50.7) | §49/§50.7 | разобран | 100% |
| [`0x04f50`](functions_mcu/func_0x04f50.md) | 8 | код B | getter u16 @+4 (uxth) | §48 | разобран | 100% |
| [`0x04f58`](functions_mcu/func_0x04f58.md) | 20 | код B | проверка маски в u32: (*(u32@r1) & r0) != 0 | §49 | разобран | 100% |
| [`0x04f70`](functions_mcu/func_0x04f70.md) | 60 | код B | merge u32-флагов: struct+8/12 → \| в r0 (для SPI/UART-конфига) | §49 | разобран | 100% |
| [`0x04fac`](functions_mcu/func_0x04fac.md) | 8 | код B | условный setter *[r2+0x10] = (r3 ? r0 : 0) | §48 | разобран | 100% |
| [`0x04fba`](functions_mcu/func_0x04fba.md) | 4 | код B | setter +4 (str r1,[r0,#4]) | §48 | разобран | 100% |
| [`0x04fc0`](functions_mcu/func_0x04fc0.md) | 52 | код B | **DMA1 INTFR handler**: если бит 0x02000000 → clear + byte@0x1743 &= ~(1<<@0x1744) + @0xB76 &= ~1 | §49 | разобран | 100% |
| [`0x05000`](functions_mcu/func_0x05000.md) | 56 | код B | **DMA1 INTFR handler**: если бит 0x20000 → clear + byte@0x1B6E &= ~(1<<@0x1B6F) + @0xB76 &= ~4 | §49 | разобран | 100% |
| [`0x05044`](functions_mcu/func_0x05044.md) | 38 | код B | среднее u16-массива (сумма/длина) | §49 | разобран | 100% |
| [`0x0506a`](functions_mcu/func_0x0506a.md) | 70 | код B | bubble sort u16-массива (вызов из медиан-фильтра 0x170c) | §50 | разобран | 100% |
| [`0x050b0`](functions_mcu/func_0x050b0.md) | 128 | код B | статистика байт-потока: min/max/sum → {i8 avg, i8 max, i8 min, u8 cnt_hi, u8 cnt_lo} | §50 | разобран | 100% |
| [`0x05134`](functions_mcu/func_0x05134.md) | 162 | код B | — | — | не начат | 0% |
| [`0x051d8`](functions_mcu/func_0x051d8.md) | 106 | код B | **телеметрия init**: 0x11d6(&@0xF70, 0x25); 0x11d6(&@0xF95, 0x26); zero @0xFBB/@0xFC7; 0x11d6(&@0x1004, 0x54); 0x11d6(&@0xFE7, 0x1D); u16@0xF10[0..0xD]=0xE10; byte@0x44[0..2]=0x19; 0x9aa4(); u32@0xFD3+4=0x2710 | §50 | разобран | 100% |
| [`0x05274`](functions_mcu/func_0x05274.md) | 174 | код B | — | — | не начат | 0% |
| [`0x05330`](functions_mcu/func_0x05330.md) | 186 | код B | — | — | не начат | 0% |
| [`0x053fc`](functions_mcu/func_0x053fc.md) | 68 | код B | descriptor-lookup @0x7D5 (таблица 0x92C): match byte@r4+2; если OK → byte@r4+4 = entry+8; event 0x5dd8 | §50 | разобран | 100% |
| [`0x05448`](functions_mcu/func_0x05448.md) | 142 | код B | — | — | не начат | 0% |
| [`0x054dc`](functions_mcu/func_0x054dc.md) | 230 | код B | — | — | не начат | 0% |
| [`0x055c8`](functions_mcu/func_0x055c8.md) | 218 | код B | — | — | не начат | 0% |
| [`0x056bc`](functions_mcu/func_0x056bc.md) | 174 | код B | — | — | не начат | 0% |
| [`0x057a0`](functions_mcu/func_0x057a0.md) | 80 | код B | **flash bank select + CRC-32**: header @0x1D800 (CRC-16 check); addr = u32@hdr+0xC+0x3000 или 0x1C800; CRC-32(0x8000000, addr) → u32@0xD0 | §50 | разобран | 100% |
| [`0x057f8`](functions_mcu/func_0x057f8.md) | 26 | код B | u16@0xCB3 → байты @0xCB3/0xCB5 + отправка 0x13bb8(s) | §49 | разобран | 100% |
| [`0x05818`](functions_mcu/func_0x05818.md) | 28 | код B | байты @0xCB3/0xCB5 → u16@0xCB3 + отправка 0x13bb8(s) | §49 | разобран | 100% |
| [`0x0583c`](functions_mcu/func_0x0583c.md) | 52 | код B | поиск в таблице @0x92C (0x11 записей × 8B): match по +4 → указатель | §49 | разобран | 100% |
| [`0x05874`](functions_mcu/func_0x05874.md) | 18 | код B | bit1: если 0x597c(1) → 0x5970(1) | §49 | разобран | 100% |
| [`0x05888`](functions_mcu/func_0x05888.md) | 34 | код B | bit0x800: если 0x597c(0x800) && !byte@0x102 → @0x102=1; затем 0x5970(0x800) | §49 | разобран | 100% |
| [`0x058b0`](functions_mcu/func_0x058b0.md) | 70 | код B | **NVIC IRQ3**: 0x5970(0x100000); struct {0x100000, 0, 8, 1} → 0x59a4; {3, 0, 0, r4} → 0xc0b4 (enable) | §50 | разобран | 100% |
| [`0x058f6`](functions_mcu/func_0x058f6.md) | 18 | код B | bit0x10: если 0x597c(0x10) → 0x5970(0x10) | §49 | разобран | 100% |
| [`0x05908`](functions_mcu/func_0x05908.md) | 92 | код B | AFIO/EXTI-setup: если 0x597c(0x200) ([0x40010400]&0x200 и [0x40010414]&0x200) → byte@RAM[0x100]=1; затем последовательно 0x80/0x100/0x200 → 0x40010414 (эмуляторно подтверждено §50.7) | §49/§50.7 | разобран | 100% |
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
| [`0x061d4`](functions_mcu/func_0x061d4.md) | 12 | код B | FLASH_SR @0x4002200C \|= r0 — сброс флагов (caller OTA-код 0x06230) | §48 | разобран | 100% |
| [`0x061e4`](functions_mcu/func_0x061e4.md) | 72 | код B | **HSI-старт**: если !CTLR bit1 → HSION(bit0), poll bit1 до 0x500; return ready | §50 | разобран | 100% |
| [`0x06230`](functions_mcu/func_0x06230.md) | 78 | код B | **FLASH sector erase core**: SCBR clear(0x7C); CTLR(+0x10) \|= 2; ADDR(+0x14)=addr; CTLR \|= 0x40; wait; CTLR &= 0x3FFD | §50 | разобран | 100% |
| [`0x06284`](functions_mcu/func_0x06284.md) | 16 | код B | проверка FLASH BSY (SCBR bit0); 1=занят | §49 | разобран | 100% |
| [`0x062d4`](functions_mcu/func_0x062d4.md) | 14 | код B | FLASH_SCBR \|= 0x80 (после стирания/записи) | §49 | разобран | 100% |
| [`0x06304`](functions_mcu/func_0x06304.md) | 24 | код B | выравнивание: r0&3 ? 9 : 6 | §49 | разобран | 100% |
| [`0x06360`](functions_mcu/func_0x06360.md) | 18 | код B | FLASH_CTLR биты [5:3] = r0 (режим стирания/записи) | §49 | разобран | 100% |
| [`0x06378`](functions_mcu/func_0x06378.md) | 12 | код B | FLASH unlock: magic-ключи 0x45670123/0xCDEF89AB → FLASH_KEYR @0x40022004 | §48 | разобран | 100% |
| [`0x06390`](functions_mcu/func_0x06390.md) | 38 | код B | ожидание не-BSY; таймаут → 0xA | §49 | разобран | 100% |
| [`0x063b8`](functions_mcu/func_0x063b8.md) | 590 | код B | — | — | не начат | 0% |
| [`0x06618`](functions_mcu/func_0x06618.md) | 526 | код B | — | — | не начат | 0% |
| [`0x06838`](functions_mcu/func_0x06838.md) | 310 | код B | — | — | не начат | 0% |
| [`0x06978`](functions_mcu/func_0x06978.md) | 104 | код B | **state-машина @0x12BA**: критсекция 0x10fc8; byte@+0x68: 0→+0x69=2 + 0x16504()→u16@+0x50 + 0x164f8()→u16@+0x48; 1/2 → 0xe740(&local) | §50 | разобран | 100% |
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
| [`0x07e98`](functions_mcu/func_0x07e98.md) | 52 | код B | **sector erase**: валидация адреса (%0x800==0, диапазон 0x3000..0x1FFFF), unlock, 0x6230(erase), SCBR\|=0x80 | §49 | разобран | 100% |
| [`0x07ed4`](functions_mcu/func_0x07ed4.md) | 18 | код B | FLASH not-busy: 0x61e4()==1 → 0, иначе 1 | §49 | разобран | 100% |
| [`0x07ee8`](functions_mcu/func_0x07ee8.md) | 58 | код B | bulk erase: инициализация стекового буфера + старт цикла | §49 | разобран | 100% |
| [`0x07fb8`](functions_mcu/func_0x07fb8.md) | 28 | код B | memmove (направленный байтовый цикл) | §49 | разобран | 100% |
| [`0x07fd4`](functions_mcu/func_0x07fd4.md) | 6 | код B | getter byte (ldrb r0,[r0]) | §48 | разобран | 100% |
| [`0x07fdc`](functions_mcu/func_0x07fdc.md) | 56 | код B | bulk erase: тело цикла (указатель → 0x6230) | §49 | разобран | 100% |
| [`0x080ac`](functions_mcu/func_0x080ac.md) | 84 | код B | **flash region validator**: r7 ∈ [0x8003000, 0x801FFFF), выравнивание 4, размер ≤ 0x800 → 0x7e98 — OTA-проверка | §50 | разобран | 100% |
| [`0x081b4`](functions_mcu/func_0x081b4.md) | 212 | код B | — | — | не начат | 0% |
| [`0x082b8`](functions_mcu/func_0x082b8.md) | 44 | код B | one-shot под флагом @0xC8D: 0x8468(); 0x83e4(); результат в {0xC84014, 0xC84013, 0xA14014} → OK, иначе флаг=1 | §49 | разобран | 100% |
| [`0x082f0`](functions_mcu/func_0x082f0.md) | 12 | код B | guard: return если byte@0xC8D≠0 (r4-варинт; callers 0xd878/0x119e4/0x147ac) | §48 | разобран | 100% |
| [`0x0833c`](functions_mcu/func_0x0833c.md) | 6 | код B | getter byte@RAM[0xC8D] — флаг инициализации 0x8xxx-драйвера | §48 | разобран | 100% |
| [`0x08348`](functions_mcu/func_0x08348.md) | 10 | код B | one-time init (флаг byte@0xC8D==0): GPIOA + SPI1-команда 0xB9 + delay (продолжение — 0x8352) | §48 | разобран | 100% |
| [`0x08380`](functions_mcu/func_0x08380.md) | 26 | код B | транзакция 0x833c: если r0 → вернуть 0 (условный выход) | §49 | разобран | 100% |
| [`0x083e4`](functions_mcu/func_0x083e4.md) | 74 | код B | **SPI1 read 3B**: GPIOA pin 0x10 (0x87da); 0x10870(0x9F) + 0x10870(0xFF)×3 → u24; 0x87de; вызов из one-time init 0x82b8 | §50 | разобран | 100% |
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
| [`0x08a90`](functions_mcu/func_0x08a90.md) | 94 | код B | **WWDG decode → struct**: 0xcc1c + 0xccbc → {u32@r4, u16@+4, u8@+6}; вызов из 0x3970/0x8938 | §50 | разобран | 100% |
| [`0x08af0`](functions_mcu/func_0x08af0.md) | 6 | код B | getter byte@RAM[0xA73] | §48 | разобран | 100% |
| [`0x08afc`](functions_mcu/func_0x08afc.md) | 14 | код B | 0x218c() → u32@0xF95+0xD (сохранение результата) | §49 | разобран | 100% |
| [`0x08b10`](functions_mcu/func_0x08b10.md) | 56 | код B | **ADC→мВ**: u16@0x5E × 0xCE4 / 2^20 + i8@0xA6 → u8@0x44+1 | §49 | разобран | 100% |
| [`0x08b58`](functions_mcu/func_0x08b58.md) | 50 | код B | **ADC→мВ**: u16@0x5E × 0xCE4 / 2^20 + i8@0xA6 → i8@0xFC7+8 | §49 | разобран | 100% |
| [`0x08bec`](functions_mcu/func_0x08bec.md) | 388 | код B | — | — | не начат | 0% |
| [`0x08d90`](functions_mcu/func_0x08d90.md) | 6 | код B | getter u32@RAM[0x1344] | §48 | разобран | 100% |
| [`0x08e14`](functions_mcu/func_0x08e14.md) | 6 | код B | getter byte@RAM[0x1378] (@0x1359+0x1f) | §48 | разобран | 100% |
| [`0x08f58`](functions_mcu/func_0x08f58.md) | 26 | код B | i8@0xFC8 → u16@0x135E (sign-extend) | §49 | разобран | 100% |
| [`0x08f7c`](functions_mcu/func_0x08f7c.md) | 198 | код B | — | — | не начат | 0% |
| [`0x09048`](functions_mcu/func_0x09048.md) | 80 | код B | **I2C2-транзакция core**: 0x11d6(&buf, 0x28); 0x15640 (CRC-7-кодирование); callback *(u32@RAM[0xDD8]+0x11C) | §50 | разобран | 100% |
| [`0x090a0`](functions_mcu/func_0x090a0.md) | 60 | код B | I2C1-транзакция: проверка *(u32@RAM[0xB60])!=0; адрес из *(u32@RAM[0xB64]); 0x1c08/0x1bd8/0x1c08(1) | §49 | разобран | 100% |
| [`0x09134`](functions_mcu/func_0x09134.md) | 668 | код B | — | — | не начат | 0% |
| [`0x09482`](functions_mcu/func_0x09482.md) | 12 | код B | последовательность: 0x9134 + 0x9480 | §48 | ID | 25% |
| [`0x09678`](functions_mcu/func_0x09678.md) | 86 | код B | флаг-хендлер: bit1(@0xB65); счётчик @0xB73 (кап 3) → clear bit1(@0xB65), byte@0xB64 &= ~0xF0 | §50 | разобран | 100% |
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
| [`0x099bc`](functions_mcu/func_0x099bc.md) | 18 | код B | *(u16@r0+0x10) = (r1\|1) if r2 else (r1&~1) — **r1 = входное значение**, не чтение из памяти; §50.7 | §49/§50.7 | разобран | 100% |
| [`0x099ce`](functions_mcu/func_0x099ce.md) | 4 | код B | setter u16 @+0x10 (strh) | §48 | разобран | 100% |
| [`0x099d4`](functions_mcu/func_0x099d4.md) | 6 | код B | запись r0 в @0x40003000+8 | §48 | разобран | 100% |
| [`0x099e0`](functions_mcu/func_0x099e0.md) | 10 | код B | запись 0xCCCC в @0x40003000 | §48 | разобран | 100% |
| [`0x099f0`](functions_mcu/func_0x099f0.md) | 10 | код B | запись 0xAAAA в @0x40003000 (кластер драйвера) | §48 | разобран | 100% |
| [`0x09a00`](functions_mcu/func_0x09a00.md) | 6 | код B | запись r0 в @0x40003000+4 | §48 | разобран | 100% |
| [`0x09a0c`](functions_mcu/func_0x09a0c.md) | 6 | код B | запись r0 в @0x40003000 | §48 | разобран | 100% |
| [`0x09a18`](functions_mcu/func_0x09a18.md) | 8 | код B | thunk → 0x99f0 (запись 0xAAAA в @0x40003000) | §48 | ID | 25% |
| [`0x09a20`](functions_mcu/func_0x09a20.md) | 34 | код B | @0x40003000 cmd: 0x5555 → 0x9a0c; 0x9a00(6); uxth(r4) → 0x99d4; 0x99f0; 0x99e0 | §49 | разобран | 100% |
| [`0x09a44`](functions_mcu/func_0x09a44.md) | 80 | код B | **регистрация event-handlers**: flash-таблицы @0x14A65/0x149B5/0x148E5/0x14A79 (IDs 0-4) → очередь | §50 | разобран | 100% |
| [`0x09aa4`](functions_mcu/func_0x09aa4.md) | 86 | код B | **телеметрия reset**: zero @0x1344 (0x13B) + 0x11d6(&@0x1384, 0x4A); вызов из 0x51d8 (telemetry init) | §50 | разобран | 100% |
| [`0x09b08`](functions_mcu/func_0x09b08.md) | 54 | код B | toggle bit3 byte@0xA71 (до 3 попыток, гейт 0x2a5c) | §49 | разобран | 100% |
| [`0x09b44`](functions_mcu/func_0x09b44.md) | 24 | код B | init-подблок: 0x9b54() + 0x9b6c() | §49 | разобран | 100% |
| [`0x09f64`](functions_mcu/func_0x09f64.md) | 12 | код B | последовательность: 0x9b44 + 0x9f70 | §48 | ID | 25% |
| [`0x09f70`](functions_mcu/func_0x09f70.md) | 28 | код B | init-подблок: 0x9f80(0x10) + 0x9fa4(1) | §49 | разобран | 100% |
| [`0x0a6a4`](functions_mcu/func_0x0a6a4.md) | 6 | код B | getter byte@RAM[0x40] | §48 | разобран | 100% |
| [`0x0a788`](functions_mcu/func_0x0a788.md) | 96 | код B | I2C read reg 0x91A4 → u16@0xF95+0x1C; вне [0x7D00..0x8CA0] → запись 0x84D0; 3 попытки | §50 | разобран | 100% |
| [`0x0a7ec`](functions_mcu/func_0x0a7ec.md) | 184 | код B | — | — | не начат | 0% |
| [`0x0a8c4`](functions_mcu/func_0x0a8c4.md) | 66 | код B | **flash-скан 0x1C800/0x1D000**: count маркеров 0xAA (0x40 записей × 32B) | §50 | разобран | 100% |
| [`0x0a910`](functions_mcu/func_0x0a910.md) | 70 | код B | **flash-скан 0x1F000/0x1F800**: count маркеров 0xAA (0x24 записи × 32B) | §50 | разобран | 100% |
| [`0x0a960`](functions_mcu/func_0x0a960.md) | 170 | код B | — | — | не начат | 0% |
| [`0x0aa18`](functions_mcu/func_0x0aa18.md) | 170 | код B | — | — | не начат | 0% |
| [`0x0aad0`](functions_mcu/func_0x0aad0.md) | 58 | код B | **CRC-16/CCITT-FALSE** (полином **0x1021**, init 0, MSB-first, без xorout) по массиву байтов; эмуляторно подтверждено (§50.7; в §49 ошибочно было 0xA001) | §49/§50.7 | разобран | 100% |
| [`0x0ab0c`](functions_mcu/func_0x0ab0c.md) | 46 | код B | I2C read 0x38B + двойной poll 0xa910(0)/0xa910(1) | §49 | разобран | 100% |
| [`0x0abf0`](functions_mcu/func_0x0abf0.md) | 46 | код B | I2C read 0x20B + двойной poll 0xa8c4(0)/0xa8c4(1) | §49 | разобран | 100% |
| [`0x0acce`](functions_mcu/func_0x0acce.md) | 458 | код B | — | — | не начат | 0% |
| [`0x0af94`](functions_mcu/func_0x0af94.md) | 250 | код B | — | — | не начат | 0% |
| [`0x0b09a`](functions_mcu/func_0x0b09a.md) | 244 | код B | — | — | не начат | 0% |
| [`0x0b302`](functions_mcu/func_0x0b302.md) | 362 | код B | — | — | не начат | 0% |
| [`0x0b476`](functions_mcu/func_0x0b476.md) | 80 | код B | varargs batch: цикл по r5 байтов → 0x99ce; mask 0x70084; toggle bit'ы каждые 0x10000 | §50 | разобран | 100% |
| [`0x0b4ce`](functions_mcu/func_0x0b4ce.md) | 96 | код B | varargs batch: 0x99bc(r4, r5); mask 0x70082/0x30002; poll 0x9794; toggle bit'ы каждые 0x10000 | §50 | разобран | 100% |
| [`0x0b53a`](functions_mcu/func_0x0b53a.md) | 64 | код B | I2C-подобная транзакция с retry (poll 0x9794) | §49 | разобран | 100% |
| [`0x0b582`](functions_mcu/func_0x0b582.md) | 72 | код B | varargs: clear bit0x400 + set bit0x200 (0x97ca/0x985c); затем reset транзакции (0xb8c8/0xb968 → если пусто: +4 \|= 0x700, +0x10C=0) | §50 | разобран | 100% |
| [`0x0b618`](functions_mcu/func_0x0b618.md) | 56 | код B | инициал транзакции: 0xb8c8/0xb968; если пусто → *(u16@[r4]) &= ~1, +4 \|= 0x700, +0x10C=0 | §49 | разобран | 100% |
| [`0x0b854`](functions_mcu/func_0x0b854.md) | 10 | код B | запись 0x10000 в struct+0x108 (caller: struct@RAM[0xdd8]) | §48 | разобран | 100% |
| [`0x0b860`](functions_mcu/func_0x0b860.md) | 94 | код B | **I2C2 busy wait**: u32@0xEFC = 0x10000; poll byte@r4+0x10C (3 → reinit); затем 0x9874(I2C2, 0x20000) | §50 | разобран | 100% |
| [`0x0b8dc`](functions_mcu/func_0x0b8dc.md) | 128 | код B | state-машина byte@r4+0x10C: 1→2 (+0x9844 bit0x100); 4: poll 0x9874(0x20000) с delay; return 3 (timeout)/0 | §50 | разобран | 100% |
| [`0x0b978`](functions_mcu/func_0x0b978.md) | 32 | код B | проверка «очередь пуста»: *(u32@RAM[0x106]) == *(u32@RAM[0x10A]) | §49 | разобран | 100% |
| [`0x0bb14`](functions_mcu/func_0x0bb14.md) | 32 | код B | проверка «очередь пуста» (вариант) | §49 | разобран | 100% |
| [`0x0bc5c`](functions_mcu/func_0x0bc5c.md) | 40 | код B | сборка дескриптора {ptr, 0, 0} → 0xc0b4() | §49 | разобран | 100% |
| [`0x0bc86`](functions_mcu/func_0x0bc86.md) | 56 | код B | сборка дескриптора {ptr, 0, 0} → 0x85c8() | §49 | разобран | 100% |
| [`0x0bcc0`](functions_mcu/func_0x0bcc0.md) | 138 | код B | — | — | не начат | 0% |
| [`0x0bd50`](functions_mcu/func_0x0bd50.md) | 280 | код B | — | — | не начат | 0% |
| [`0x0be6c`](functions_mcu/func_0x0be6c.md) | 104 | код B | **TLV-декодер**: type byte@+1: 3 → {len=byte@+6, data} (0x11a4); 6/0x10 → 6B fixed; return длина | §50 | разобран | 100% |
| [`0x0befc`](functions_mcu/func_0x0befc.md) | 74 | код B | поиск в таблице @0x7C4 (2 записи): range [entry+4, entry+ptr+8] → указатель | §50 | разобран | 100% |
| [`0x0bf4c`](functions_mcu/func_0x0bf4c.md) | 12 | код B | последовательность: 0xd878 + 0xddc4 | §48 | ID | 25% |
| [`0x0bf58`](functions_mcu/func_0x0bf58.md) | 184 | код B | — | — | не начат | 0% |
| [`0x0c02c`](functions_mcu/func_0x0c02c.md) | 92 | код B | mismatch-счётчик: bit0/bit1(@0xF70+1) vs @0xA65/@0xA66 → u16@0xA68++; ≥ 0x32 → toggle bit3(@0xF70+3); вызов из 0xc098 | §50 | разобран | 100% |
| [`0x0c098`](functions_mcu/func_0x0c098.md) | 24 | код B | init-подблок: 0x5b5a() + 0xc0a0() | §49 | разобран | 100% |
| [`0x0c0b4`](functions_mcu/func_0x0c0b4.md) | 78 | код B | **NVIC IRQ enable**: приоритет-группа из SCB_CFSR(0xE000ED0C) bits 0x700; запись в [0xE000E400+irq] и [adj+0x100] — **база NVIC этого чипа = 0xE000E400** | §50 | разобран | 100% |
| [`0x0c138`](functions_mcu/func_0x0c138.md) | 26 | код B | магия: u16@0xA7C == 0xEB04 → 1 | §49 | разобран | 100% |
| [`0x0c158`](functions_mcu/func_0x0c158.md) | 164 | код B | — | — | не начат | 0% |
| [`0x0c200`](functions_mcu/func_0x0c200.md) | 12 | код B | thunk → 0x9f64 (r3=1) | §48 | ID | 25% |
| [`0x0c20c`](functions_mcu/func_0x0c20c.md) | 134 | код B | — | — | не начат | 0% |
| [`0x0c2a8`](functions_mcu/func_0x0c2a8.md) | 84 | код B | **system sleep**: poll [0x40007010]&2; [0x40007008]\|=r1; [0x40007000]=(&~7)\|2; **SCB_SCR \|= 4 (SLEEPDEEP)**; WFI или SEV+WFE×2; clear SLEEPDEEP | §50 | разобран | 100% |
| [`0x0c304`](functions_mcu/func_0x0c304.md) | 96 | код B | I2C read reg 0x91A0 → u16@0xF95+0x18; та же логика диапазона; 3 попытки | §50 | разобран | 100% |
| [`0x0c368`](functions_mcu/func_0x0c368.md) | 172 | код B | — | — | не начат | 0% |
| [`0x0c420`](functions_mcu/func_0x0c420.md) | 60 | код B | чтение 4B из EEPROM + CRC-16 (0x8a50); буфер @0xC9C (вариант 0x3da0) | §49 | разобран | 100% |
| [`0x0c464`](functions_mcu/func_0x0c464.md) | 20 | код B | запись структуры {u32=r1, +4=0, +5=0, +6=r2, +7=r3} → 1 | §49 | разобран | 100% |
| [`0x0c4b4`](functions_mcu/func_0x0c4b4.md) | 18 | код B | RCC_CFGR0[7:4] (HPRE) = r0 | §49 | разобран | 100% |
| [`0x0c4cc`](functions_mcu/func_0x0c4cc.md) | 70 | код B | **переключение источника тактирования**: CTLR &= ~0x50000; r0: 0x10000 → \|= 0x10000; 0x40000 → \|= 0x50000 | §50 | разобран | 100% |
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
| [`0x0c708`](functions_mcu/func_0x0c708.md) | 86 | код B | **расчёт частоты тактирования**: RCC_CTLR: PLLSRC bits[19:18], HSE bit0x10000; div = 2+(bits>>18) или 0x1F0-...; если HSE ready → freq = div × 0x7A1200 (20 МГц) | §50 | разобран | 100% |
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
| [`0x0cb40`](functions_mcu/func_0x0cb40.md) | 116 | код B | WWDG: 0xCA/0x53 → +0x24; +0x8 \|=/~0x400 (r1); poll +0x10&4 до 0x2000; return статус | §50 | разобран | 100% |
| [`0x0cbb8`](functions_mcu/func_0x0cbb8.md) | 68 | код B | WWDG: если !SR(+0xC) bit6 → SR=0x80, poll bit6 до 0x2000; return статус | §50 | разобран | 100% |
| [`0x0cc08`](functions_mcu/func_0x0cc08.md) | 14 | код B | WWDG @0x40002800: SR(+0xC) &= ~0x80 (EWIF?) | §49 | разобран | 100% |
| [`0x0cc1c`](functions_mcu/func_0x0cc1c.md) | 68 | код B | **WWDG CFR(+4) decode**: {bits[12:10], [12:8], [5:0], [15:13]} → 4 байта; опц. BCD-декод (0xc9a8) | §50 | разобран | 100% |
| [`0x0cc68`](functions_mcu/func_0x0cc68.md) | 76 | код B | WWDG-статус: r1 ∈ {0x20000, 0x40000, 0x80000} → [0x40002850]>>16 != 0; иначе ([0x40002808]&r1) && ([0x4000280C]&(r1>>4)) | §50 | разобран | 100% |
| [`0x0ccbc`](functions_mcu/func_0x0ccbc.md) | 72 | код B | **WWDG CR(+0) decode**: {bits[15:10], [14:8], [6:0]} → 3 байта | §50 | разобран | 100% |
| [`0x0cd0c`](functions_mcu/func_0x0cd0c.md) | 110 | код B | **WWDG refresh с данными**: 0xCA/0x53 → +0x24; RER(+0x8) = u32@r4; +0x10 = u32@r4+8 \| (u16@r4+4)<<16; 0xcc08; delay 0x2FF | §50 | разобран | 100% |
| [`0x0cd80`](functions_mcu/func_0x0cd80.md) | 136 | код B | — | — | не начат | 0% |
| [`0x0ce68`](functions_mcu/func_0x0ce68.md) | 8 | код B | thunk → 0x3168 | §48 | ID | 25% |
| [`0x0ce70`](functions_mcu/func_0x0ce70.md) | 92 | код B | **WWDG window wait**: magic 0xCA/0x53 → +0x24; clear bit5([0x4000280C]); poll bit5 до 0x8000; return статус; финал 0xFF → +0x24 | §50 | разобран | 100% |
| [`0x0ced0`](functions_mcu/func_0x0ced0.md) | 16 | код B | init-подблок: 0xcdd4(1) + 0xcdc8(1) | §49 | разобран | 100% |
| [`0x0cee0`](functions_mcu/func_0x0cee0.md) | 68 | код B | I2C read: {code16, len=2} → 0x1e72(dev 0x3E) — чтение регистра чипа I2C2 | §50 | разобран | 100% |
| [`0x0cf60`](functions_mcu/func_0x0cf60.md) | 84 | код B | **NVRAM verify @0x305C**: 0x8380(&buf, 0x28); CRC-16(0x26) == u16@+0x26 → u16@+0x24=1 | §50 | разобран | 100% |
| [`0x0cfb8`](functions_mcu/func_0x0cfb8.md) | 78 | код B | **транзакция + CRC-16 check**: 0x8380(&@0x304C, 0x2000, 0x10) ×2 (с delay); 0x8a50 == u32@+0xC | §50 | разобран | 100% |
| [`0x0d00c`](functions_mcu/func_0x0d00c.md) | 534 | код B | — | — | не начат | 0% |
| [`0x0d240`](functions_mcu/func_0x0d240.md) | 82 | код B | **EEPROM read+verify @0xC9C**: 0x8380(&buf, 0x30000, 8); CRC-16(4B) == u32@+4; вызов из 0xc420 | §50 | разобран | 100% |
| [`0x0d298`](functions_mcu/func_0x0d298.md) | 46 | код B | poll 0xcfb8 с задержкой 0x1F4; затем *(u32@*(u32@RAM[0x304C])) != 0 | §49 | разобран | 100% |
| [`0x0d33c`](functions_mcu/func_0x0d33c.md) | 84 | код B | счётчик @0xA67 (кап 5) → I2C read (0x1c60, 8B из @0x15F7); bit0/bit2(byte@+0x54) → byte@0xF70+1 bits 0/1 | §50 | разобран | 100% |
| [`0x0d39c`](functions_mcu/func_0x0d39c.md) | 202 | код B | — | — | не начат | 0% |
| [`0x0d46c`](functions_mcu/func_0x0d46c.md) | 182 | код B | — | — | не начат | 0% |
| [`0x0d534`](functions_mcu/func_0x0d534.md) | 152 | код B | — | — | не начат | 0% |
| [`0x0d5d4`](functions_mcu/func_0x0d5d4.md) | 146 | код B | — | — | не начат | 0% |
| [`0x0d670`](functions_mcu/func_0x0d670.md) | 110 | код B | **EEPROM block read**: 0x11d6(&buf, 0x30); 0x8938; retry 0xab0c ×3; CRC-16(0x8a50) → buf+0x22; memcpy 0x20B; 0xaccc; save 3×u32 | §50 | разобран | 100% |
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
| [`0x0dd2c`](functions_mcu/func_0x0dd2c.md) | 84 | код B | **clamp-умножение**: q = clamp((r3-r0)/r1, 0, r2) с округлением; return r1*q + r0 | §50 | разобран | 100% |
| [`0x0ddc4`](functions_mcu/func_0x0ddc4.md) | 58 | код B | **OTA-команда от хоста**: u16@0x124E+0x12==0xE0 && +0x14==0x5AA5 → erase @0x1D800 + 0xdd80; ==0xE2 → 0xdd80 (магия 0x5AA5) | §49 | разобран | 100% |
| [`0x0de0a`](functions_mcu/func_0x0de0a.md) | 196 | код B | — | — | не начат | 0% |
| [`0x0ded4`](functions_mcu/func_0x0ded4.md) | 54 | код B | **varargs**: если byte[1]==3 → u32 из 4 байтов → *(u32@RAM[0xFE7])+2 = value; return 1 | §49 | разобран | 100% |
| [`0x0df10`](functions_mcu/func_0x0df10.md) | 338 | код B | — | — | не начат | 0% |
| [`0x0e160`](functions_mcu/func_0x0e160.md) | 24 | код B | поиск в flash-таблице строк @0x19E98+0x140 через 0x16880/0x16aa2 | §49 | разобран | 100% |
| [`0x0e17c`](functions_mcu/func_0x0e17c.md) | 128 | код B | **fixed-point расчёт**: 0xe160 (поиск) + 0x16222 (div); (v*0x98B...)/0x2710 × ..., clamp [-0x2710, 0x2710] → u16 | §50 | разобран | 100% |
| [`0x0e200`](functions_mcu/func_0x0e200.md) | 198 | код B | — | — | не начат | 0% |
| [`0x0e2cc`](functions_mcu/func_0x0e2cc.md) | 44 | код B | range-check смещения по flash-строке @0x19F50+0x59F через 0x16d8e → byte | §49 | разобран | 100% |
| [`0x0e2fc`](functions_mcu/func_0x0e2fc.md) | 104 | код B | **мульти-интерполяция**: 0x17306(t@0x19FE6, 0x1A) + 0x1736a(\|v\|, t@0x19EB4, 3) + 0x17306(v2, t@0x19FE6+0x36, 4) → 0x16588 → u16; вызов из мотор-региона 0x69E4 | §50 | разобран | 100% |
| [`0x0e36c`](functions_mcu/func_0x0e36c.md) | 114 | код B | **fixed-point lerp с насыщением**: \|a-b\| ≥ 0x2710 → 0; иначе (b*0x2710 - (0x2710-a)*...)/0x2710, clamp [-0x8000, 0x7FFF] | §50 | разобран | 100% |
| [`0x0e3e4`](functions_mcu/func_0x0e3e4.md) | 6 | код B | setter u16 = 0 (strh #0,[r0]) | §48 | разобран | 100% |
| [`0x0e3ec`](functions_mcu/func_0x0e3ec.md) | 24 | код B | поиск в flash-таблице строк @0x19FAC+0x8A через 0x16880/0x16aa2 | §49 | разобран | 100% |
| [`0x0e408`](functions_mcu/func_0x0e408.md) | 566 | код B | slew-лимитер → u16@RAM[0x1357] (duty% = byte@0xFD3) | §39, §41 | разобран | 100% |
| [`0x0e658`](functions_mcu/func_0x0e658.md) | 136 | код B | round-robin диспетчер 6 задач (TBB @0xE684) | §39.5b | разобран | 100% |
| [`0x0e6ec`](functions_mcu/func_0x0e6ec.md) | 18 | код B | if byte@RAM[0x13C9]==1 → bl 0xf14c (не function-pointer; эмуляторно подтверждено §50.7) | §49/§50.7 | разобран | 100% |
| [`0x0e704`](functions_mcu/func_0x0e704.md) | 54 | код B | **clamp \|v\|≤0xC8**: иначе обнулить byte@0x12BA+0x56; вызов 0x1654c; вызов из 0x07A30 (§41 slot-3) | §49 | разобран | 100% |
| [`0x0e740`](functions_mcu/func_0x0e740.md) | 190 | код B | — | — | не начат | 0% |
| [`0x0e808`](functions_mcu/func_0x0e808.md) | 592 | код B | — | — | не начат | 0% |
| [`0x0ea64`](functions_mcu/func_0x0ea64.md) | 504 | код B | — | — | не начат | 0% |
| [`0x0ec70`](functions_mcu/func_0x0ec70.md) | 352 | код B | — | — | не начат | 0% |
| [`0x0eddc`](functions_mcu/func_0x0eddc.md) | 98 | код B | **верификация @0x304C**: range-check'и (0x1F4/0x21000/flash 0x25E20); сбой → reset {0, 0x21000, 0x21000} + 0x1570c | §50 | разобран | 100% |
| [`0x0ee48`](functions_mcu/func_0x0ee48.md) | 298 | код B | — | — | не начат | 0% |
| [`0x0ef78`](functions_mcu/func_0x0ef78.md) | 140 | код B | — | — | не начат | 0% |
| [`0x0f038`](functions_mcu/func_0x0f038.md) | 262 | код B | — | — | не начат | 0% |
| [`0x0f14c`](functions_mcu/func_0x0f14c.md) | 156 | код B | — | — | не начат | 0% |
| [`0x0f1ec`](functions_mcu/func_0x0f1ec.md) | 78 | код B | порог #1: u16@0xF95+6 vs flash 0x19D8E+0xA; счётчик @0xA22 (кап +0xE); toggle bit1(@0xF70+2) + 0x156ac | §50 | разобран | 100% |
| [`0x0f290`](functions_mcu/func_0x0f290.md) | 94 | код B | счётчик #8: u32@0xFBB+4 ≥ 0x3E8 && !флаги && byte@0x107==1 → u16@0xA2E++; ≥ 0x12C → toggle bit2(@0xF70+2), reset; вызов из 0x11978 | §50 | разобран | 100% |
| [`0x0f304`](functions_mcu/func_0x0f304.md) | 88 | код B | счётчик #7: u32@0xFBB+4 ≥ 0x3E8 && !флаги → u16@0xA30++; ≥ 0x12C → toggle bit3(@0xF70+2), reset; вызов из 0x11978 | §50 | разобран | 100% |
| [`0x0f36c`](functions_mcu/func_0x0f36c.md) | 80 | код B | порог #3: i8@0xFC7+8 ∈ [-0x1E, 0x64]; счётчик @0xA36 (кап 0x32); toggle bit3(@0xFC7+9) | §50 | разобран | 100% |
| [`0x0f40c`](functions_mcu/func_0x0f40c.md) | 116 | код B | порог #5: \|u16@0xF95+8 - u16@0xF95+6\| ≥ flash 0x19D8E+0x12 && u16@0xF95+6 ≤ 0xC1C; счётчик @0xA2A (кап +0x16); toggle bit4(@0xF70+2) | §50 | разобран | 100% |
| [`0x0f5c4`](functions_mcu/func_0x0f5c4.md) | 102 | код B | порог #4: i8@0x44 и i8@0x44+1 ∈ [-0x1E, 0x64]; счётчик @0xA3A (кап 0x32); toggle bit6(@0xFC7+6) | §50 | разобран | 100% |
| [`0x0f694`](functions_mcu/func_0x0f694.md) | 746 | код B | — | — | не начат | 0% |
| [`0x0f994`](functions_mcu/func_0x0f994.md) | 564 | код B | — | — | не начат | 0% |
| [`0x0fbf8`](functions_mcu/func_0x0fbf8.md) | 190 | код B | — | — | не начат | 0% |
| [`0x0fcd0`](functions_mcu/func_0x0fcd0.md) | 194 | код B | — | — | не начат | 0% |
| [`0x0fdac`](functions_mcu/func_0x0fdac.md) | 174 | код B | — | — | не начат | 0% |
| [`0x0fe74`](functions_mcu/func_0x0fe74.md) | 174 | код B | — | — | не начат | 0% |
| [`0x10468`](functions_mcu/func_0x10468.md) | 166 | код C | — | — | не начат | 0% |
| [`0x10524`](functions_mcu/func_0x10524.md) | 78 | код C | порог #2: i8@0xFC7+8 vs flash 0x19E1C+0x30; счётчик @0x9E4 (кап +0x31); toggle bit1(@0xFC7+9) | §50 | разобран | 100% |
| [`0x105c4`](functions_mcu/func_0x105c4.md) | 194 | код C | — | — | не начат | 0% |
| [`0x106a0`](functions_mcu/func_0x106a0.md) | 24 | код C | set/clear bit0x40 в *(u16@r0) | §49 | разобран | 100% |
| [`0x106b8`](functions_mcu/func_0x106b8.md) | 28 | код C | SPI1-инициал: SPI_CTLR \|= 0x10, RCC \|= 0x400, SPI+0x4=0x80, 0x5a6c() | §49 | разобран | 100% |
| [`0x106d8`](functions_mcu/func_0x106d8.md) | 54 | код C | SPI1 (0x40013000) / SPI-2 (0x40013C00): вкл/выкл через RCC+0xC биты (base>>12) | §49 | разобран | 100% |
| [`0x10718`](functions_mcu/func_0x10718.md) | 18 | код C | проверка: *(u16@r0+8) & r1 != 0 | §49 | разобран | 100% |
| [`0x1072a`](functions_mcu/func_0x1072a.md) | 6 | код C | getter u16 @+0xc (ldrh) | §48 | разобран | 100% |
| [`0x10730`](functions_mcu/func_0x10730.md) | 4 | код C | setter u16 @+0xc (strh) | §48 | разобран | 100% |
| [`0x10734`](functions_mcu/func_0x10734.md) | 60 | код C | SPI-конфиг: merge u16-флагов из структуры → SPI-регистр; вызов 0x10788 | §49 | разобран | 100% |
| [`0x10770`](functions_mcu/func_0x10770.md) | 16 | код C | SPI1-инициал: SPI_CTLR \|= 0x40, RCC \|= 0x1000, SPI+0x4=0x80, 0x5a6c() | §49 | разобран | 100% |
| [`0x10780`](functions_mcu/func_0x10780.md) | 8 | код C | thunk → 0x10788 | §48 | ID | 25% |
| [`0x10788`](functions_mcu/func_0x10788.md) | 92 | код C | **SPI1 full init**: 0x107ec (GPIOA EXTI); GPIOA pin 0x10; struct {0, 0x104, 0, 2, 1, 0x200, 8, 0, 7} → 0x10734(0x40013000); 0x106a0 — **SPI1 = 0x40013000** | §50 | разобран | 100% |
| [`0x107ec`](functions_mcu/func_0x107ec.md) | 126 | код C | **GPIOA EXTI init**: 0x87b0(&local); RCC BDCR \|= 4\|0x1001; 4× {mode u16 (0x20/0x80/0x40/0x10), byte, count} → 0x85c8(GPIOA) | §50 | разобран | 100% |
| [`0x10870`](functions_mcu/func_0x10870.md) | 98 | код C | **SPI1 read**: poll SPI1+8 bit2 (0x10718) до 0x8000; 0x10730(r5); delay 0xA; poll bit0; 0x1072a() → byte | §50 | разобран | 100% |
| [`0x1093c`](functions_mcu/func_0x1093c.md) | 118 | код C | **NVRAM→RAM копия + порог**: byte@0x4A[0..5] → @0xFC7; если i8@+2 > i8@+5: счётчик @0x60 (кап 0xA) → sync + u32@0x8C \|= 0x1000 | §50 | разобран | 100% |
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
| [`0x128e4`](functions_mcu/func_0x128e4.md) | 114 | код E | state-машина byte@0xB5A: 0x4c84(3, 0x64); 0x1238c(); states 0..3 → 0x1274c/0x12778/0x1277a/0x1277c; счётчик кап 5; TBB по @0xB59 (<0xA, таблица повреждена) | §50 | разобран | 100% |
| [`0x129b4`](functions_mcu/func_0x129b4.md) | 46 | код E | state dispatch: 0x4c84(1, 10); 0x12470(); TBB по byte@0xB58 (<0xA) — таблица повреждена/обфусцирована; затем @0xB58=0 | §49 | разобран | 100% |
| [`0x12a64`](functions_mcu/func_0x12a64.md) | 18 | код E | 0x4c84(0, 1); 0x124c0() — очередь/событие | §49 | разобран | 100% |
| [`0x12a78`](functions_mcu/func_0x12a78.md) | 110 | код E | state-машина byte@0xB5B: 0x4c84(4, 0x1F4); states 0..3 → пары (0x12680/0x126d8, 0x1269c/0x12710, 0x12680/0x12738, 0x1269c/0x1273a); счётчик кап 4 | §50 | разобран | 100% |
| [`0x12aec`](functions_mcu/func_0x12aec.md) | 96 | код E | I2C read reg 0x91A2 → u16@0xF95+0x1A; та же логика диапазона; 3 попытки | §50 | разобран | 100% |
| [`0x12b50`](functions_mcu/func_0x12b50.md) | 190 | код E | — | — | не начат | 0% |
| [`0x12c24`](functions_mcu/func_0x12c24.md) | 56 | код E | счётчик с насыщением: u16@0xB7A++, кап 0xC8; гейт bit0(u32@0xB76) | §49 | разобран | 100% |
| [`0x12d04`](functions_mcu/func_0x12d04.md) | 134 | код E | — | — | не начат | 0% |
| [`0x12d90`](functions_mcu/func_0x12d90.md) | 190 | код E | — | — | не начат | 0% |
| [`0x12e64`](functions_mcu/func_0x12e64.md) | 56 | код E | счётчик с насыщением: u16@0xB7C++, кап 0xC8; гейт bit2(u32@0xB76) | §49 | разобран | 100% |
| [`0x12f44`](functions_mcu/func_0x12f44.md) | 134 | код E | — | — | не начат | 0% |
| [`0x12fd0`](functions_mcu/func_0x12fd0.md) | 8 | код E | thunk → 0x12b50 | §48 | ID | 25% |
| [`0x12fd8`](functions_mcu/func_0x12fd8.md) | 8 | код E | thunk → 0x12d90 | §48 | ID | 25% |
| [`0x12fe0`](functions_mcu/func_0x12fe0.md) | 66 | код E | **generic u32 flag set/clear**: группа r1>>5&7 (1→+0xC, 2→+0x10, иначе +0x14); бит r1&0x1F | §50 | разобран | 100% |
| [`0x1302c`](functions_mcu/func_0x1302c.md) | 134 | код E | init/драйвер трёх USART | §6.5 | частично | 50% |
| [`0x130f2`](functions_mcu/func_0x130f2.md) | 80 | код E | **generic u32 flag check**: та же группа; оба бита (низкий + высокий r1>>8) должны быть set | §50 | разобран | 100% |
| [`0x13148`](functions_mcu/func_0x13148.md) | 168 | код E | — | — | не начат | 0% |
| [`0x131fc`](functions_mcu/func_0x131fc.md) | 130 | код E | — | — | не начат | 0% |
| [`0x13284`](functions_mcu/func_0x13284.md) | 130 | код E | — | — | не начат | 0% |
| [`0x1330c`](functions_mcu/func_0x1330c.md) | 106 | код E | **транзакция + CRC-8 check**: 0x8380(&buf, 0x50000/0x51000, 8); 0x87f8(buf, 7) == byte@buf+0xB → 0x10a5c (event) | §50 | разобран | 100% |
| [`0x1337c`](functions_mcu/func_0x1337c.md) | 1472 | код E | — | — | не начат | 0% |
| [`0x1395c`](functions_mcu/func_0x1395c.md) | 36 | код E | обработчик флага: byte@0xCAC → byte@0xA73 (сброс после обработки) | §49 | разобран | 100% |
| [`0x139ac`](functions_mcu/func_0x139ac.md) | 14 | код E | CMD: {u32=3} → 0x13c78 (отправка) | §49 | разобран | 100% |
| [`0x139fc`](functions_mcu/func_0x139fc.md) | 226 | код E | — | — | не начат | 0% |
| [`0x13b14`](functions_mcu/func_0x13b14.md) | 72 | код E | транзакция + CRC-8 check @0x30DD (0x8380(&buf, 0x20); 0x87f8(buf, 0x18) == byte@buf+0x18) | §50 | разобран | 100% |
| [`0x13b60`](functions_mcu/func_0x13b60.md) | 84 | код E | **NVRAM verify @0x30CF**: 0x8380(&buf, 0x40000, 0xE); CRC-16(0xA) == u32@+0xA | §50 | разобран | 100% |
| [`0x13bb8`](functions_mcu/func_0x13bb8.md) | 48 | код E | **retry-send**: 0x13b60-проверка + задержка 0x1F4; гейт u16@0x30CF | §49 | разобран | 100% |
| [`0x13c5c`](functions_mcu/func_0x13c5c.md) | 18 | код E | **CMD 0x4B**: 0x11d6(&@0x3084, 0x4B); byte@0xCAC=1 (флаг запроса) | §49 | разобран | 100% |
| [`0x13c78`](functions_mcu/func_0x13c78.md) | 392 | код E | — | — | не начат | 0% |
| [`0x14368`](functions_mcu/func_0x14368.md) | 66 | код F | **инициал @0x30CF**: {+2/+6=0x41000, +0=0} + 0x84a0 retry | §50 | разобран | 100% |
| [`0x147ac`](functions_mcu/func_0x147ac.md) | 78 | код G | **верификация @0x30CF**: 0x82f0(0x40000); CRC-16 → u32@+0xA; 0x84a0 retry | §50 | разобран | 100% |
| [`0x14802`](functions_mcu/func_0x14802.md) | 284 | код G | — | — | не начат | 0% |
| [`0x14924`](functions_mcu/func_0x14924.md) | 48 | код G | I2C read с 3 попытками: 0xcee0(8, 0x91B2, 2) → u16@0xF95+0x1E | §49 | разобран | 100% |
| [`0x14958`](functions_mcu/func_0x14958.md) | 76 | код G | **WWDG mode set**: r4 1..6 → 0xcb10(r4-1) (магическая последовательность с индексом) | §50 | разобран | 100% |
| [`0x14ed0`](functions_mcu/func_0x14ed0.md) | 110 | код G | state-машина byte@0x31: states 0/1/2 (условия @0x107/@0x80/0x8e14()); счётчик @0x42 (кап 0x32) | §50 | разобран | 100% |
| [`0x14f50`](functions_mcu/func_0x14f50.md) | 1572 | код G | — | — | не начат | 0% |
| [`0x155ac`](functions_mcu/func_0x155ac.md) | 64 | код G | I2C read: буфер {u16=0, len=4, addr=0x3E} → 0x1e72; результат → u16@0xF95+0x20 | §49 | разобран | 100% |
| [`0x15640`](functions_mcu/func_0x15640.md) | 108 | код G | **CRC-7 stream-кодер**: buf[2i]=byte, buf[2i+1]=CRC-7(byte, prev) — для I2C2-транзакций | §50 | разобран | 100% |
| [`0x156ac`](functions_mcu/func_0x156ac.md) | 92 | код G | **EEPROM read+save**: 0xab0c(&buf[0x20]) до 3 раз; buf[0x4D]=bit1(@0xF70+2); CRC-16 → u16@+0x4E; memcpy 0x20; ldm 4×u32 → 0xaccc; вызов из порога #1 (0xf1ec) | §50 | разобран | 100% |
| [`0x1570c`](functions_mcu/func_0x1570c.md) | 72 | код G | транзакция + CRC-16 check @0x304C (0x82f0(0x20000); 0x8a50 → u32@+0xC; 0x84a0 retry) | §50 | разобран | 100% |
| [`0x15758`](functions_mcu/func_0x15758.md) | 48 | код G | I2C-запись: 0x11d6(0x80c, &@0x1FD4); 0x11c8(0x800, &@0x27E0); 0x11c8(0x800, &@0x1FD4); @0x1FD4+0x804 = 0x800 | §49 | разобран | 100% |
| [`0x15790`](functions_mcu/func_0x15790.md) | 76 | код G | **EEPROM-верификация @0xC9C**: 0x82f0(0x30000); CRC-16(4B) → u32@+4; 0x84a0 retry; вызов из 0x3da0 | §50 | разобран | 100% |
| [`0x157e0`](functions_mcu/func_0x157e0.md) | 266 | код G | — | — | не начат | 0% |
| [`0x158f8`](functions_mcu/func_0x158f8.md) | 22 | код G | I2C-старт: byte@0xB8C=1; 0x15ffc(0xA); byte@0x1FAC+3=1 | §49 | разобран | 100% |
| [`0x15918`](functions_mcu/func_0x15918.md) | 242 | код G | — | — | не начат | 0% |
| [`0x15a1c`](functions_mcu/func_0x15a1c.md) | 58 | код G | инициал структуры @0x1FAC (~0x20B, дефолты 0/0xFFFF) + 0x15758 (I2C) | §49 | разобран | 100% |
| [`0x15a60`](functions_mcu/func_0x15a60.md) | 280 | код G | — | — | не начат | 0% |
| [`0x15b84`](functions_mcu/func_0x15b84.md) | 236 | код G | — | — | не начат | 0% |
| [`0x15c94`](functions_mcu/func_0x15c94.md) | 66 | код G | **копия строки из flash @0x1AA9A**: n = byte@0x1FAC+3; stride ~306B; длина через 0x11ec; return count | §50 | разобран | 100% |
| [`0x15ce0`](functions_mcu/func_0x15ce0.md) | 36 | код G | retry-счётчик @0xC84: инкремент до 3; при byte@0x36==1 сброс | §49 | разобран | 100% |
| [`0x15d14`](functions_mcu/func_0x15d14.md) | 216 | код G | — | — | не начат | 0% |
| [`0x15df4`](functions_mcu/func_0x15df4.md) | 242 | код G | — | — | не начат | 0% |
| [`0x15f00`](functions_mcu/func_0x15f00.md) | 116 | код G | **I2C state-машина byte@0x1FAC+3**: states → 7/2/3/1 (проверки @0x1F10+1, u16@+0xC/+8, i16 /16) | §50 | разобран | 100% |
| [`0x15ffc`](functions_mcu/func_0x15ffc.md) | 56 | код G | установка указателя @0xC80; при byte@0xB8C==1: сброс/декремент счётчика + 0x15a1c | §49 | разобран | 100% |
| [`0x16040`](functions_mcu/func_0x16040.md) | 252 | код G | — | — | не начат | 0% |
| [`0x16176`](functions_mcu/func_0x16176.md) | 40 | код G | бинарный поиск по i16-массиву (возврат индекса/0xFFFF) | §49 | разобран | 100% |
| [`0x1619e`](functions_mcu/func_0x1619e.md) | 40 | код G | бинарный поиск по u32-массиву | §49 | разобран | 100% |
| [`0x161ea`](functions_mcu/func_0x161ea.md) | 56 | код G | u32 udiv (вариант с циклической коррекцией) | §49 | разобран | 100% |
| [`0x16222`](functions_mcu/func_0x16222.md) | 68 | код G | signed div (udiv + коррекция + восстановление знака) | §50 | разобран | 100% |
| [`0x16288`](functions_mcu/func_0x16288.md) | 24 | код G | signed-подготовка к делению (знак → 0x80000000) | §49 | разобран | 100% |
| [`0x162ce`](functions_mcu/func_0x162ce.md) | 24 | код G | signed-подготовка к делению (вариант) | §49 | разобран | 100% |
| [`0x16328`](functions_mcu/func_0x16328.md) | 24 | код G | signed-подготовка к делению (вариант) | §49 | разобран | 100% |
| [`0x163b4`](functions_mcu/func_0x163b4.md) | 76 | код G | GPIOA → RCC BDCR \|= 4 (0xc6a4(4, 1)) | §50 | разобран | 100% |
| [`0x16410`](functions_mcu/func_0x16410.md) | 94 | код G | **checksum + divisibility**: sum(r1 байт) + r5 + (r3%4==0 && (r3%100==0 \|\| r3%400==0)); вызов из 0x1647c | §50 | разобран | 100% |
| [`0x1647c`](functions_mcu/func_0x1647c.md) | 86 | код G | **табличный offset**: r4 ∈ [0xBB8, 0x7D0) → условие; иначе r5 ∈ [1,0xC], r6 ∈ [1,0x1F], r7 ≤ 0x17 → 0x16410 + (res-1)*24 + r7 | §50 | разобран | 100% |
| [`0x16588`](functions_mcu/func_0x16588.md) | 558 | код G | — | — | не начат | 0% |
| [`0x167b6`](functions_mcu/func_0x167b6.md) | 202 | код G | — | — | не начат | 0% |
| [`0x16880`](functions_mcu/func_0x16880.md) | 184 | код G | — | — | не начат | 0% |
| [`0x16938`](functions_mcu/func_0x16938.md) | 184 | код G | — | — | не начат | 0% |
| [`0x169f0`](functions_mcu/func_0x169f0.md) | 178 | код G | — | — | не начат | 0% |
| [`0x16aa2`](functions_mcu/func_0x16aa2.md) | 128 | код G | **u16-табличная интерполяция**: bsearch + lerp × 0x10000 >> 16 → i16 | §50 | разобран | 100% |
| [`0x16b22`](functions_mcu/func_0x16b22.md) | 178 | код G | — | — | не начат | 0% |
| [`0x16bd4`](functions_mcu/func_0x16bd4.md) | 442 | код G | — | — | не начат | 0% |
| [`0x16d8e`](functions_mcu/func_0x16d8e.md) | 436 | код G | — | — | не начат | 0% |
| [`0x16f42`](functions_mcu/func_0x16f42.md) | 156 | код G | — | — | не начат | 0% |
| [`0x16fde`](functions_mcu/func_0x16fde.md) | 156 | код G | — | — | не начат | 0% |
| [`0x17094`](functions_mcu/func_0x17094.md) | 76 | код G | signed clamp: 0x17170(r0, r1) → насыщение [-0x80000000, ...] со спец-случаями (-1, 0); вызов из мотор-региона 0x69e4/0xe808 | §50 | разобран | 100% |
| [`0x170e0`](functions_mcu/func_0x170e0.md) | 76 | код G | signed clamp #2: 0x17214(r0, r1) → насыщение; вызов из 0xee48 | §50 | разобран | 100% |
| [`0x1712c`](functions_mcu/func_0x1712c.md) | 36 | код G | **фиксированное умножение**: P = r0*r1 (через 0x172b8); return низкие 32 бита (P >> n), n = r2; эмуляторно подтверждено (§50.7); прямых callers нет | §49/§50.6/§50.7 | разобран | 100% |
| [`0x17150`](functions_mcu/func_0x17150.md) | 32 | код G | **проверка произведения**: P = r0*r1 (через 0x172b8); return (P_hi==0) ? P_lo : -1 («умещается ли в 32 бита»); эмуляторно подтверждено (§50.7); прямых callers нет | §49/§50.6/§50.7 | разобран | 100% |
| [`0x17170`](functions_mcu/func_0x17170.md) | 164 | код G | — | — | не начат | 0% |
| [`0x17214`](functions_mcu/func_0x17214.md) | 164 | код G | — | — | не начат | 0% |
| [`0x172b8`](functions_mcu/func_0x172b8.md) | 78 | код G | **u32×u32 → u64 умножение** (школьное, 16-битные половины + переносы): **[r2]=HIGH, [r3]=LOW** (указатели «перепутаны» относительно привычного порядка!); вызов из 0x1712c/0x17150; эмуляторно подтверждено (§50.7) | §50/§50.6/§50.7 | разобран | 100% |
| [`0x17306`](functions_mcu/func_0x17306.md) | 100 | код G | **i16-табличная интерполяция**: bsearch 0x16176 + lerp × 0x10000 >> 16; вызов из 0xe2fc | §50 | разобран | 100% |
| [`0x1736a`](functions_mcu/func_0x1736a.md) | 96 | код G | **u32-табличная интерполяция**: bsearch 0x1619e + lerp / 0x10; вызов из 0xe2fc | §50 | разобран | 100% |
| [`0x173cc`](functions_mcu/func_0x173cc.md) | 294 | код G | — | — | не начат | 0% |
| [`0x17736`](functions_mcu/func_0x17736.md) | 108 | код G | **артефакт**: push + u16-таблица данных (hi^lo=0xC0, 0x40 записей) — регион гигантской функции 0x17xxx (§48.5) | §50 | ID | 25% |
| [`0x177d6`](functions_mcu/func_0x177d6.md) | 8 | код G | cold-tail гигантской функции региона 0x17xxx (b #0x173bc); артефакт детекции | §48 | ID | 25% |
| [`0x178c4`](functions_mcu/func_0x178c4.md) | 12 | код G | dead-фрагмент: после strh — НЕВАЛИДНАЯ инструкция 0x6EF5 (Unicorn: UC_ERR_INSN_INVALID); перед ним u16-таблица @0x177DE; дыра 0x177DE..0x19A1C = одна гигантская функция, пропущенная каноническим детектором | §48 | ID | 25% |
| [`0x19a1c`](functions_mcu/func_0x19a1c.md) | 76 | код I | **u64 sdiv**: знаковое деление 64-бит (знаки + 0x199bc unsigned + восстановление) | §50 | разобран | 100% |
| [`0x19a68`](functions_mcu/func_0x19a68.md) | 36 | код I | memcpy (байтовый цикл) | §49 | разобран | 100% |
| [`0x19a8c`](functions_mcu/func_0x19a8c.md) | 14 | код I | memset (байты r2, count r1) | §49 | разобран | 100% |
| [`0x19a9e`](functions_mcu/func_0x19a9e.md) | 18 | код I | memset (перестановка аргументов → 0x19a8c) | §49 | разобран | 100% |
| [`0x19ab0`](functions_mcu/func_0x19ab0.md) | 162 | код I | — | — | не начат | 0% |
| [`0x19b64`](functions_mcu/func_0x19b64.md) | 120 | код I | signed fixed-point умножение/нормализация (i16) | §50 | разобран | 100% |
| [`0x19bdc`](functions_mcu/func_0x19bdc.md) | 124 | код I | signed алгоритм (евклидов-подобный цикл) + 0x1a0e8 | §50 | разобран | 100% |
| [`0x19c58`](functions_mcu/func_0x19c58.md) | 328 | код I | — | — | не начат | 0% |
| [`0x19dbc`](functions_mcu/func_0x19dbc.md) | 202 | код I | — | — | не начат | 0% |
| [`0x19e8c`](functions_mcu/func_0x19e8c.md) | 234 | код I | — | — | не начат | 0% |
| [`0x19f7c`](functions_mcu/func_0x19f7c.md) | 44 | код I | сравнение u64 (r0:r1) с r2 со знаком (udiv-подобная подготовка) | §49 | разобран | 100% |
| [`0x19fae`](functions_mcu/func_0x19fae.md) | 16 | код I | (r0+r1) → 0x1a0f8(_, 0, 0x96) — масштабирование с deadband | §49 | разобран | 100% |
| [`0x19fbe`](functions_mcu/func_0x19fbe.md) | 14 | код I | 0x1a0f8(0, 1, 0x96) — масштабирование с deadband (инверсия) | §49 | разобран | 100% |
| [`0x19fcc`](functions_mcu/func_0x19fcc.md) | 34 | код I | abs(r0) → lookup 0x1a184(0, sign, 0x433) | §49 | разобран | 100% |
| [`0x19ff4`](functions_mcu/func_0x19ff4.md) | 24 | код I | lookup 0x1a184(0, 0, 0x433) — калибровочная таблица | §49 | разобран | 100% |
| [`0x1a010`](functions_mcu/func_0x1a010.md) | 50 | код I | **масштабирование с deadband**: \|v\|<0x7f → 0; [0x7f..0x96] → линейное; иначе (v-0x96)<<1; знак сохраняется; вызов из 0x1D898 (§22) | §49 | разобран | 100% |
| [`0x1a052`](functions_mcu/func_0x1a052.md) | 36 | код I | **u64 масштаб 2^(n-0x433)**, n = r2>>21 (твин 0x123e): n < r3 → 0; [r3..0x433] → u64lsr({r1:r0}, 0x433-n) через 0x1a0a0; > 0x433 → {r1, r0 << (n-0x433)}; пул: 0x3FF+0x34=0x433, -0x433 | §49/§50.6 | разобран | 100% |
| [`0x1a080`](functions_mcu/func_0x1a080.md) | 32 | код I | **u64 LSL**: (r1:r0) << r2 — логический сдвиг влево (количество в r2) | §49/§50.6 | разобран | 100% |
| [`0x1a0a0`](functions_mcu/func_0x1a0a0.md) | 34 | код I | **u64 LSR**: (r1:r0) >> r2 — копия 0x126c (другая точка кода) | §49/§50.6 | разобран | 100% |
| [`0x1a0c2`](functions_mcu/func_0x1a0c2.md) | 38 | код I | **u64 ASR**: (r1:r0) >>s r2 — арифметический сдвиг с расширением знака | §49/§50.6 | разобран | 100% |
| [`0x1a16a`](functions_mcu/func_0x1a16a.md) | 26 | код I | u64 sub (r0:r1 - r2:r3) | §49 | разобран | 100% |
| [`0x1a184`](functions_mcu/func_0x1a184.md) | 164 | код I | — | — | не начат | 0% |
| [`0x1a24c`](functions_mcu/func_0x1a24c.md) | 86 | код I | **RLE-декодер #2**: тот же алгоритм, что 0x152a (другая аллокация регистров) | §50 | разобран | 100% |
| [`0x1a2a4`](functions_mcu/func_0x1a2a4.md) | 90 | код I | **timer IRQ handler @0x40012C00**: если bit31(+0x1C): [0x40012C54]&=~0x8000; byte@0x218=0; [+0x20]\|=0x80; byte@0x245/0x246; byte@0x102 ∈ {0,2} → bit в @0x247 + u16@0x21E \|= 0x100/0x200 | §50 | разобран | 100% |
| [`0x1a31c`](functions_mcu/func_0x1a31c.md) | 522 | код I | ADC1: стейт-машина выборки (системный тик ~1 кГц) | §22, §40 | разобран | 100% |
| [`0x1a5c4`](functions_mcu/func_0x1a5c4.md) | 12 | код I | ADC1+0x18 \|= 8 (bit3; caller — ADC-таск 0x1A31C) | §48 | разобран | 100% |
| [`0x1a5d4`](functions_mcu/func_0x1a5d4.md) | 12 | код I | ADC1+0x18 \|= 0x20 (bit5; caller — DMA+ADC 0x1E298) | §48 | разобран | 100% |
| [`0x1a5e6`](functions_mcu/func_0x1a5e6.md) | 12 | код I | «own»: трамплин к S-box-блоку 0x1a7ac (реальный старт 0x1a5e4 `mov r2,r1` — без пролога, артефакт детекции; bl из 0x21c64) | §36.3, §37 | разобран | 100% |
| [`0x1a5f2`](functions_mcu/func_0x1a5f2.md) | 8 | код I | «own»: трамплин bl 0x1bfa0 (из 0x1a628) | §27.2, §37 | разобран | 100% |
| [`0x1a5fa`](functions_mcu/func_0x1a5fa.md) | 46 | код I | «own»: XOR двух 16-Б блоков (round, вызов из 0x1a7ac; callers=3) | §37 | разобран | 100% |
| [`0x1a628`](functions_mcu/func_0x1a628.md) | 12 | код I | трамплин к шифру: ldr r0=&0x16aa; bl 0x1bfa0 | §27.2 | разобран | 100% |
| [`0x1a638`](functions_mcu/func_0x1a638.md) | 66 | код I | **float-lookup #1**: таблица @0x734 (0x35 записей); интерполяция 0x1de5e; clamp ≤ -0.000931; default 125.0; вызов из 0x1D898 (§22) | §50 | разобран | 100% |
| [`0x1a688`](functions_mcu/func_0x1a688.md) | 266 | код I | — | — | не начат | 0% |
| [`0x1a7ac`](functions_mcu/func_0x1a7ac.md) | 136 | код I | «own»: S-box-подстановка + перестановка (16 Б, 10 раундов) | §37 | разобран | 100% |
| [`0x1a838`](functions_mcu/func_0x1a838.md) | 32 | код I | **CRC-32** (полином 0x04C11DB7, MSB-first); вызов из агрегатора 0x1F71C | §49 | разобран | 100% |
| [`0x1a894`](functions_mcu/func_0x1a894.md) | 140 | код I | — | — | не начат | 0% |
| [`0x1a938`](functions_mcu/func_0x1a938.md) | 3296 | код I | батарейные пороги (clamp 10..100) | §22 | частично | 50% |
| [`0x1b67c`](functions_mcu/func_0x1b67c.md) | 1174 | код I | флаги/статус: перегрев ≥46°C → флаг @0x318 | §22 | разобран | 100% |
| [`0x1bb1c`](functions_mcu/func_0x1bb1c.md) | 562 | код I | батарейный замер №2 (struct @0x154) | §25.4 | разобран | 100% |
| [`0x1bd88`](functions_mcu/func_0x1bd88.md) | 118 | код I | **quadrant-классификатор**: [0x40012C40+0x14]<<16 sign; линейная комбинация с flash 0x3CE4/0x2328 → код квадранта 1..6 → u16@r0+2; [0x40012C00+0x30] &= 0xDFFF; u16@0x386/0x384/0x382 → +4/+8/+0xC | §50 | разобран | 100% |
| [`0x1be1c`](functions_mcu/func_0x1be1c.md) | 174 | код I | — | — | не начат | 0% |
| [`0x1bedc`](functions_mcu/func_0x1bedc.md) | 66 | код I | GPIO init @0x48000400: zero-буфер; 0x22000(пины 0x40/0x80/0xFF); byte@r4+0x14=7 | §50 | разобран | 100% |
| [`0x1bf48`](functions_mcu/func_0x1bf48.md) | 78 | код I | МОТОР-ИНИТ: bl 0x1d640/0x1c0b0/0x1c1ac/0x1bedc | §39 | частично | 50% |
| [`0x1bfa0`](functions_mcu/func_0x1bfa0.md) | 150 | код I | табличный шифр (&table @0x16aa, src) | §27.2 | разобран | 100% |
| [`0x1c0b0`](functions_mcu/func_0x1c0b0.md) | 238 | код I | инициализация сенсоров ADC1 | §40 | ID | 25% |
| [`0x1c1ac`](functions_mcu/func_0x1c1ac.md) | 106 | код I | **DMA1 ch9 init**: DMA1+4=1; poll [base+0xFF] == 0x40012450 и == u32@0x1692; 0x2359c(DMA1, 0x5D000041); +0x28/+0x14=1, +0x70=0x19, +0x50\|=1; [0x40020100+8]\|=1; **NVIC ISER[0] \|= 1<<9** | §50 | разобран | 100% |
| [`0x1c234`](functions_mcu/func_0x1c234.md) | 228 | код I | — | — | не начат | 0% |
| [`0x1c34c`](functions_mcu/func_0x1c34c.md) | 1244 | код I | — | — | не начат | 0% |
| [`0x1c838`](functions_mcu/func_0x1c838.md) | 1466 | код I | калибровка/секвенсор: @0xF400/+4 → @0x1e8/@0x1ec | §25 | разобран | 100% |
| [`0x1ce38`](functions_mcu/func_0x1ce38.md) | 522 | код I | — | — | не начат | 0% |
| [`0x1d078`](functions_mcu/func_0x1d078.md) | 610 | код I | state-машина режимов (byte@0x229: 2/3/0x0B) — адрес приблизительный | §34.2 | частично | 50% |
| [`0x1d330`](functions_mcu/func_0x1d330.md) | 142 | код I | — | — | не начат | 0% |
| [`0x1d3d0`](functions_mcu/func_0x1d3d0.md) | 588 | код I | хвост ADC ISR: → TX → SWSTART | §22.6 | разобран | 100% |
| [`0x1d640`](functions_mcu/func_0x1d640.md) | 348 | код I | — | — | не начат | 0% |
| [`0x1d7ac`](functions_mcu/func_0x1d7ac.md) | 102 | код I | **векторная операция**: 0x1e410(r1) → {i16,i16} из таблицы @0xA6C6; 2D-интерполяция/поворот с u16-парой из @0x10C (делитель 2^15) | §50 | разобран | 100% |
| [`0x1d818`](functions_mcu/func_0x1d818.md) | 86 | код I | **2D fixed-point rotate/dot**: out[0] = (b*a' - a*b') >> 15, out[1] = (a*a' + b*b') >> 15; {a,b} из r4+4/+6, {a',b'} из @0x10C; вызов из мотор-региона 0x1a938 | §50 | разобран | 100% |
| [`0x1d874`](functions_mcu/func_0x1d874.md) | 26 | код I | lookup через 0x19994(0xBB80): результат → u16@0xF95+2/4 | §49 | разобран | 100% |
| [`0x1d898`](functions_mcu/func_0x1d898.md) | 1254 | код I | батарея/запас хода/температура (0x306/0x30c/0x30e) | §22 | разобран | 100% |
| [`0x1dd8c`](functions_mcu/func_0x1dd8c.md) | 128 | код I | «own»: вспомогательный round (bl из 0x1a814) | §37 | частично | 50% |
| [`0x1de0c`](functions_mcu/func_0x1de0c.md) | 66 | код I | **float-lookup #2**: таблица @0x610 (0x2D записей); clamp ≤ -0.000763; default 250.0 | §50 | разобран | 100% |
| [`0x1de5e`](functions_mcu/func_0x1de5e.md) | 70 | код I | **интерполяция core**: 0x19968 + abs-lookup 0x19fbe ×3 + 0x19fa8/0x19b62/0x19ab0/0x19b5a/0x19bdc (fixed-point lerp pipeline) | §50 | разобран | 100% |
| [`0x1dea4`](functions_mcu/func_0x1dea4.md) | 186 | код I | — | — | не начат | 0% |
| [`0x1df84`](functions_mcu/func_0x1df84.md) | 66 | код I | **float-lookup #3**: таблица @0x50C (0x29 записей); clamp ≤ -0.000763; default 100.0 | §50 | разобран | 100% |
| [`0x1dfd8`](functions_mcu/func_0x1dfd8.md) | 344 | код I | периодический таск: флаги → счётчик → сборщик 'a'-кадров 0x211f8 | §47 | частично | 50% |
| [`0x1e1a0`](functions_mcu/func_0x1e1a0.md) | 200 | код I | — | — | не начат | 0% |
| [`0x1e298`](functions_mcu/func_0x1e298.md) | 34 | код I | DMA+ADC (вызов из 0x1a31c) | §40 | частично | 50% |
| [`0x1e2ca`](functions_mcu/func_0x1e2ca.md) | 36 | код I | SysTick init: RVR=r0-1, CVR=0, CTRL=7 | §49 | разобран | 100% |
| [`0x1e2f8`](functions_mcu/func_0x1e2f8.md) | 164 | код I | RCC+GPIOC AF-конфиг (MODER=0x044AA200) | §39 | частично | 50% |
| [`0x1e3a4`](functions_mcu/func_0x1e3a4.md) | 50 | код I | **программный сброс**: конфиг RCC+0x40, dsb, SCB_AIRCR = 0x5FA0004 (SYSRESETREQ+VECTKEY), цикл | §49 | разобран | 100% |
| [`0x1e410`](functions_mcu/func_0x1e410.md) | 106 | код I | **табличная декодировка @0xA6C6**: индекс по bits[27:24] (4 ветви) → {i16, i16} со знаковыми инверсиями | §50 | разобран | 100% |
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
| [`0x21804`](functions_mcu/func_0x21804.md) | 96 | код I | **UART4 init** (MCU→BLE): GPIO @0x48000800 (пины 0x400/0x800); UART4(0x40004C00): struct {base, 0x4B00, 0} → 0x23188; 0x21bc8(0x1E, 2); 0x21b6c(0x1E); +0x2C \|= 0x400 | §50 | разобран | 100% |
| [`0x2186c`](functions_mcu/func_0x2186c.md) | 370 | код I | — | — | не начат | 0% |
| [`0x21a08`](functions_mcu/func_0x21a08.md) | 240 | код I | NVRAM-save таск (гейт byte@0x170==1 + бит31 common+0x14) | §25 | разобран | 100% |
| [`0x21b84`](functions_mcu/func_0x21b84.md) | 60 | код I | NVIC/SCB бит-манипуляция: r0≥0 → массив @0xE000E400; r0<0 → SCB+0x1C зона | §49 | разобран | 100% |
| [`0x21c0c`](functions_mcu/func_0x21c0c.md) | 6 | код I | getter *(u32@RAM[0x28])+4 (двойная индирекция) | §48 | разобран | 100% |
| [`0x21c18`](functions_mcu/func_0x21c18.md) | 34 | код I | NVIC-приоритеты: *(u32@RAM[0x4]) vs flash 0x2710; 0x19968/0x1e2c8; r4!=3 → 0x21b84(~0, r4) | §49 | разобран | 100% |
| [`0x21c64`](functions_mcu/func_0x21c64.md) | 12 | код I | «own»: входной шифр/проверка кадра (initiator BLE) | §36.3, §37 | разобран | 100% |
| [`0x21ca8`](functions_mcu/func_0x21ca8.md) | 364 | код I | инициализация сенсоров ADC1 | §40 | ID | 25% |
| [`0x21e18`](functions_mcu/func_0x21e18.md) | 412 | код I | — | — | не начат | 0% |
| [`0x22000`](functions_mcu/func_0x22000.md) | 406 | код I | — | — | не начат | 0% |
| [`0x221a4`](functions_mcu/func_0x221a4.md) | 66 | код I | критсекция + атомарный u32-инкремент с валидацией (0x23688/0x235d4) | §50 | разобран | 100% |
| [`0x221e6`](functions_mcu/func_0x221e6.md) | 78 | код I | критсекция + insert в список (0x2360c); только если r4>>30==0 | §50 | разобран | 100% |
| [`0x22234`](functions_mcu/func_0x22234.md) | 58 | код I | TIM-инициал: toggle RCC_CTLR bit0x10 с задержками 0x22a0c | §49 | разобран | 100% |
| [`0x22274`](functions_mcu/func_0x22274.md) | 790 | код I | — | — | не начат | 0% |
| [`0x225c4`](functions_mcu/func_0x225c4.md) | 18 | код I | set/clear битов RCC_CTLR (+0x0) | §49 | разобран | 100% |
| [`0x225dc`](functions_mcu/func_0x225dc.md) | 18 | код I | set/clear битов RCC+0x60 (расширенный регистр) | §49 | разобран | 100% |
| [`0x225f4`](functions_mcu/func_0x225f4.md) | 556 | код I | — | — | не начат | 0% |
| [`0x22824`](functions_mcu/func_0x22824.md) | 240 | код I | — | — | не начат | 0% |
| [`0x22934`](functions_mcu/func_0x22934.md) | 76 | код I | **SysTick init из struct**: r5 = u32@r4[0] (÷8 если byte@+8==0); lookup 0x19968 ×3 (0x3E8/0x2710/0x186A0) → @0x1C; SysTick LOAD/VAL/CTRL из r4 (CTRL = (byte@+8)<<2 \| byte@+9) | §50 | разобран | 100% |
| [`0x229d4`](functions_mcu/func_0x229d4.md) | 44 | код I | busy-delay: N итераций, сброс CVR=0xFFFFFF (коэфф. из *(u32@RAM[0x24])) | §49 | разобран | 100% |
| [`0x22a0c`](functions_mcu/func_0x22a0c.md) | 48 | код I | busy-delay: N итераций ожидания SysTick CVR (коэфф. из *(u32@RAM[0x10])) | §49 | разобран | 100% |
| [`0x22a48`](functions_mcu/func_0x22a48.md) | 148 | код I | блок TIM1+TIM3+TIM4 (HAL-функции, регистры +0x10) | §39.1, §41 | разобран | 100% |
| [`0x22b7c`](functions_mcu/func_0x22b7c.md) | 212 | код I | — | — | не начат | 0% |
| [`0x22c70`](functions_mcu/func_0x22c70.md) | 168 | код I | — | — | не начат | 0% |
| [`0x22d2c`](functions_mcu/func_0x22d2c.md) | 204 | код I | HAL timer (доказательство раскладки +0x10) | §39.1 | разобран | 100% |
| [`0x22e0c`](functions_mcu/func_0x22e0c.md) | 186 | код I | — | — | не начат | 0% |
| [`0x22edc`](functions_mcu/func_0x22edc.md) | 188 | код I | — | — | не начат | 0% |
| [`0x22fac`](functions_mcu/func_0x22fac.md) | 126 | код I | **timer channel config**: struct +0x30/+0x2C (CCR-like): clear [15:12]/[19:16]/[11:8] + set из byte@r1; базы {0x40012C00, 0x40014000, 0x40014400, 0x40014800, 0x40014C00}; +4 [17:16]=byte@r1+0xB; +0x50=u32@r1+4 — **кластер из 5 таймер-блоков** | §50 | разобран | 100% |
| [`0x23040`](functions_mcu/func_0x23040.md) | 296 | код I | — | — | не начат | 0% |
| [`0x23188`](functions_mcu/func_0x23188.md) | 372 | код I | HAL_UART_Transmit (валидация порта/длины, assert) | §6.5 | разобран | 100% |
| [`0x23374`](functions_mcu/func_0x23374.md) | 262 | код I | 3-проводная шина режима (byte@0x26b ? bl 0x23374 : 0) | §40.7 | частично | 50% |
| [`0x23544`](functions_mcu/func_0x23544.md) | 80 | код I | критсекция-условие + бит-операция (r4>>27) | §50 | разобран | 100% |
| [`0x2360c`](functions_mcu/func_0x2360c.md) | 94 | код I | FLASH program: проверка ADDR bit31; копирование u32-пар (tst) в страницу; старт записи | §50 | разобран | 100% |
| [`0x244d2`](functions_mcu/func_0x244d2.md) | 262 | код J | — | — | не начат | 0% |

**Известные артефакты детекции (ручная перепроверка 2026-08-24):** строка `0x1a5e6` —
тело функции, реально начинающейся в `0x1a5e4` (`mov r2,r1`, без push-пролога — детектор
ловит внутренний push); это «own»-трамплин 0x21c64→0x1a5e4→0x1a7ac. Всё остальное из
именованных функций сверено с дизассембляцией входов и разделами REPORT.md.