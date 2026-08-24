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
| разобран | 26 | 15412 | 15.9% |
| частично | 9 | 6620 | 6.8% |
| ID | 2 | 602 | 0.6% |
| не начат | 641 | 74298 | 76.6% |
| **всего** | **678** | **96932** | **19.5% декомпилировано** |

Подробности по каждой функции: `functions_mcu/func_0x<off>.md` (дизассембляция,
литералы, callees/callers). Разделы REPORT.md — где описана семантика.

Перегенерация: `python research/scripts/gen_maps.py` (список функций — из
`functions_mcu/README.md`; каталог разобранных блоков — в gen_maps.py, ANALYZED_MCU).

| offset | размер | регион | имя / роль | разделы | статус | % |
|---|---|---|---|---|---|---|
| [`0x01218`](functions_mcu/func_0x01218.md) | 34 | код A | — | — | не начат | 0% |
| [`0x0123e`](functions_mcu/func_0x0123e.md) | 46 | код A | — | — | не начат | 0% |
| [`0x0126c`](functions_mcu/func_0x0126c.md) | 32 | код A | — | — | не начат | 0% |
| [`0x0128c`](functions_mcu/func_0x0128c.md) | 30 | код A | — | — | не начат | 0% |
| [`0x012aa`](functions_mcu/func_0x012aa.md) | 156 | код A | — | — | не начат | 0% |
| [`0x01346`](functions_mcu/func_0x01346.md) | 322 | код A | — | — | не начат | 0% |
| [`0x01494`](functions_mcu/func_0x01494.md) | 48 | код A | — | — | не начат | 0% |
| [`0x0152a`](functions_mcu/func_0x0152a.md) | 86 | код A | — | — | не начат | 0% |
| [`0x01580`](functions_mcu/func_0x01580.md) | 26 | код A | — | — | не начат | 0% |
| [`0x015aa`](functions_mcu/func_0x015aa.md) | 198 | код A | — | — | не начат | 0% |
| [`0x01670`](functions_mcu/func_0x01670.md) | 86 | код A | — | — | не начат | 0% |
| [`0x016d4`](functions_mcu/func_0x016d4.md) | 42 | код A | — | — | не начат | 0% |
| [`0x0170c`](functions_mcu/func_0x0170c.md) | 68 | код A | — | — | не начат | 0% |
| [`0x0175c`](functions_mcu/func_0x0175c.md) | 42 | код A | — | — | не начат | 0% |
| [`0x0178c`](functions_mcu/func_0x0178c.md) | 98 | код A | — | — | не начат | 0% |
| [`0x017f4`](functions_mcu/func_0x017f4.md) | 28 | код A | — | — | не начат | 0% |
| [`0x01858`](functions_mcu/func_0x01858.md) | 40 | код A | — | — | не начат | 0% |
| [`0x018b0`](functions_mcu/func_0x018b0.md) | 66 | код A | — | — | не начат | 0% |
| [`0x018fc`](functions_mcu/func_0x018fc.md) | 60 | код A | — | — | не начат | 0% |
| [`0x01940`](functions_mcu/func_0x01940.md) | 52 | код A | — | — | не начат | 0% |
| [`0x01984`](functions_mcu/func_0x01984.md) | 102 | код A | — | — | не начат | 0% |
| [`0x019f4`](functions_mcu/func_0x019f4.md) | 100 | код A | — | — | не начат | 0% |
| [`0x01a68`](functions_mcu/func_0x01a68.md) | 70 | код A | — | — | не начат | 0% |
| [`0x01abc`](functions_mcu/func_0x01abc.md) | 12 | код A | — | — | не начат | 0% |
| [`0x01ac8`](functions_mcu/func_0x01ac8.md) | 268 | код A | — | — | не начат | 0% |
| [`0x01bdc`](functions_mcu/func_0x01bdc.md) | 42 | код A | — | — | не начат | 0% |
| [`0x01c1c`](functions_mcu/func_0x01c1c.md) | 42 | код A | — | — | не начат | 0% |
| [`0x01c60`](functions_mcu/func_0x01c60.md) | 26 | код A | — | — | не начат | 0% |
| [`0x01c7a`](functions_mcu/func_0x01c7a.md) | 52 | код A | — | — | не начат | 0% |
| [`0x01cea`](functions_mcu/func_0x01cea.md) | 12 | код A | — | — | не начат | 0% |
| [`0x01cf6`](functions_mcu/func_0x01cf6.md) | 54 | код A | — | — | не начат | 0% |
| [`0x01d78`](functions_mcu/func_0x01d78.md) | 112 | код A | — | — | не начат | 0% |
| [`0x01dec`](functions_mcu/func_0x01dec.md) | 8 | код A | — | — | не начат | 0% |
| [`0x01df4`](functions_mcu/func_0x01df4.md) | 64 | код A | — | — | не начат | 0% |
| [`0x01e34`](functions_mcu/func_0x01e34.md) | 30 | код A | — | — | не начат | 0% |
| [`0x01e52`](functions_mcu/func_0x01e52.md) | 32 | код A | — | — | не начат | 0% |
| [`0x01e72`](functions_mcu/func_0x01e72.md) | 32 | код A | — | — | не начат | 0% |
| [`0x01e94`](functions_mcu/func_0x01e94.md) | 324 | код A | — | — | не начат | 0% |
| [`0x01fe0`](functions_mcu/func_0x01fe0.md) | 200 | код A | — | — | не начат | 0% |
| [`0x020c4`](functions_mcu/func_0x020c4.md) | 16 | код A | — | — | не начат | 0% |
| [`0x020d8`](functions_mcu/func_0x020d8.md) | 76 | код A | — | — | не начат | 0% |
| [`0x02138`](functions_mcu/func_0x02138.md) | 16 | код A | — | — | не начат | 0% |
| [`0x0214c`](functions_mcu/func_0x0214c.md) | 36 | код A | — | — | не начат | 0% |
| [`0x0218c`](functions_mcu/func_0x0218c.md) | 76 | код A | — | — | не начат | 0% |
| [`0x021dc`](functions_mcu/func_0x021dc.md) | 16 | код A | — | — | не начат | 0% |
| [`0x021f0`](functions_mcu/func_0x021f0.md) | 16 | код A | — | — | не начат | 0% |
| [`0x02204`](functions_mcu/func_0x02204.md) | 16 | код A | — | — | не начат | 0% |
| [`0x02218`](functions_mcu/func_0x02218.md) | 16 | код A | — | — | не начат | 0% |
| [`0x0222c`](functions_mcu/func_0x0222c.md) | 16 | код A | — | — | не начат | 0% |
| [`0x02240`](functions_mcu/func_0x02240.md) | 16 | код A | — | — | не начат | 0% |
| [`0x02254`](functions_mcu/func_0x02254.md) | 16 | код A | — | — | не начат | 0% |
| [`0x02268`](functions_mcu/func_0x02268.md) | 16 | код A | — | — | не начат | 0% |
| [`0x0227c`](functions_mcu/func_0x0227c.md) | 16 | код A | — | — | не начат | 0% |
| [`0x02290`](functions_mcu/func_0x02290.md) | 16 | код A | — | — | не начат | 0% |
| [`0x022a4`](functions_mcu/func_0x022a4.md) | 16 | код A | — | — | не начат | 0% |
| [`0x022b8`](functions_mcu/func_0x022b8.md) | 16 | код A | — | — | не начат | 0% |
| [`0x022cc`](functions_mcu/func_0x022cc.md) | 16 | код A | — | — | не начат | 0% |
| [`0x022e0`](functions_mcu/func_0x022e0.md) | 16 | код A | — | — | не начат | 0% |
| [`0x022f4`](functions_mcu/func_0x022f4.md) | 16 | код A | — | — | не начат | 0% |
| [`0x02308`](functions_mcu/func_0x02308.md) | 16 | код A | — | — | не начат | 0% |
| [`0x0231c`](functions_mcu/func_0x0231c.md) | 16 | код A | — | — | не начат | 0% |
| [`0x02330`](functions_mcu/func_0x02330.md) | 16 | код A | — | — | не начат | 0% |
| [`0x02344`](functions_mcu/func_0x02344.md) | 16 | код A | — | — | не начат | 0% |
| [`0x02358`](functions_mcu/func_0x02358.md) | 16 | код A | — | — | не начат | 0% |
| [`0x0236c`](functions_mcu/func_0x0236c.md) | 42 | код A | — | — | не начат | 0% |
| [`0x02730`](functions_mcu/func_0x02730.md) | 36 | код B | — | — | не начат | 0% |
| [`0x02770`](functions_mcu/func_0x02770.md) | 68 | код B | — | — | не начат | 0% |
| [`0x0280c`](functions_mcu/func_0x0280c.md) | 88 | код B | — | — | не начат | 0% |
| [`0x029e8`](functions_mcu/func_0x029e8.md) | 104 | код B | — | — | не начат | 0% |
| [`0x02a5c`](functions_mcu/func_0x02a5c.md) | 16 | код B | — | — | не начат | 0% |
| [`0x02a6c`](functions_mcu/func_0x02a6c.md) | 28 | код B | — | — | не начат | 0% |
| [`0x02a94`](functions_mcu/func_0x02a94.md) | 132 | код B | — | — | не начат | 0% |
| [`0x02b2c`](functions_mcu/func_0x02b2c.md) | 124 | код B | — | — | не начат | 0% |
| [`0x02bbc`](functions_mcu/func_0x02bbc.md) | 50 | код B | — | — | не начат | 0% |
| [`0x02d14`](functions_mcu/func_0x02d14.md) | 8 | код B | — | — | не начат | 0% |
| [`0x02d1c`](functions_mcu/func_0x02d1c.md) | 20 | код B | — | — | не начат | 0% |
| [`0x02d34`](functions_mcu/func_0x02d34.md) | 36 | код B | — | — | не начат | 0% |
| [`0x02d5c`](functions_mcu/func_0x02d5c.md) | 16 | код B | — | — | не начат | 0% |
| [`0x02d70`](functions_mcu/func_0x02d70.md) | 130 | код B | — | — | не начат | 0% |
| [`0x02e0c`](functions_mcu/func_0x02e0c.md) | 16 | код B | — | — | не начат | 0% |
| [`0x02e84`](functions_mcu/func_0x02e84.md) | 54 | код B | — | — | не начат | 0% |
| [`0x03034`](functions_mcu/func_0x03034.md) | 62 | код B | — | — | не начат | 0% |
| [`0x0307c`](functions_mcu/func_0x0307c.md) | 42 | код B | — | — | не начат | 0% |
| [`0x030a6`](functions_mcu/func_0x030a6.md) | 58 | код B | — | — | не начат | 0% |
| [`0x030e0`](functions_mcu/func_0x030e0.md) | 44 | код B | — | — | не начат | 0% |
| [`0x0310c`](functions_mcu/func_0x0310c.md) | 68 | код B | — | — | не начат | 0% |
| [`0x03150`](functions_mcu/func_0x03150.md) | 24 | код B | — | — | не начат | 0% |
| [`0x03168`](functions_mcu/func_0x03168.md) | 96 | код B | — | — | не начат | 0% |
| [`0x031dc`](functions_mcu/func_0x031dc.md) | 66 | код B | — | — | не начат | 0% |
| [`0x032f4`](functions_mcu/func_0x032f4.md) | 54 | код B | — | — | не начат | 0% |
| [`0x0332c`](functions_mcu/func_0x0332c.md) | 574 | код B | — | — | не начат | 0% |
| [`0x03588`](functions_mcu/func_0x03588.md) | 84 | код B | — | — | не начат | 0% |
| [`0x035ec`](functions_mcu/func_0x035ec.md) | 18 | код B | — | — | не начат | 0% |
| [`0x03600`](functions_mcu/func_0x03600.md) | 96 | код B | — | — | не начат | 0% |
| [`0x03668`](functions_mcu/func_0x03668.md) | 88 | код B | — | — | не начат | 0% |
| [`0x036f4`](functions_mcu/func_0x036f4.md) | 12 | код B | — | — | не начат | 0% |
| [`0x03700`](functions_mcu/func_0x03700.md) | 54 | код B | — | — | не начат | 0% |
| [`0x03740`](functions_mcu/func_0x03740.md) | 40 | код B | — | — | не начат | 0% |
| [`0x03780`](functions_mcu/func_0x03780.md) | 78 | код B | — | — | не начат | 0% |
| [`0x037f4`](functions_mcu/func_0x037f4.md) | 64 | код B | — | — | не начат | 0% |
| [`0x03838`](functions_mcu/func_0x03838.md) | 174 | код B | — | — | не начат | 0% |
| [`0x038ec`](functions_mcu/func_0x038ec.md) | 84 | код B | — | — | не начат | 0% |
| [`0x03940`](functions_mcu/func_0x03940.md) | 22 | код B | — | — | не начат | 0% |
| [`0x0395c`](functions_mcu/func_0x0395c.md) | 10 | код B | — | — | не начат | 0% |
| [`0x03966`](functions_mcu/func_0x03966.md) | 10 | код B | — | — | не начат | 0% |
| [`0x03970`](functions_mcu/func_0x03970.md) | 28 | код B | — | — | не начат | 0% |
| [`0x03994`](functions_mcu/func_0x03994.md) | 52 | код B | — | — | не начат | 0% |
| [`0x03a6c`](functions_mcu/func_0x03a6c.md) | 22 | код B | — | — | не начат | 0% |
| [`0x03b20`](functions_mcu/func_0x03b20.md) | 10 | код B | — | — | не начат | 0% |
| [`0x03b2a`](functions_mcu/func_0x03b2a.md) | 20 | код B | — | — | не начат | 0% |
| [`0x03b42`](functions_mcu/func_0x03b42.md) | 64 | код B | — | — | не начат | 0% |
| [`0x03b82`](functions_mcu/func_0x03b82.md) | 66 | код B | — | — | не начат | 0% |
| [`0x03bc4`](functions_mcu/func_0x03bc4.md) | 62 | код B | — | — | не начат | 0% |
| [`0x03c04`](functions_mcu/func_0x03c04.md) | 68 | код B | — | — | не начат | 0% |
| [`0x03c4c`](functions_mcu/func_0x03c4c.md) | 42 | код B | — | — | не начат | 0% |
| [`0x03c7c`](functions_mcu/func_0x03c7c.md) | 46 | код B | — | — | не начат | 0% |
| [`0x03cac`](functions_mcu/func_0x03cac.md) | 232 | код B | — | — | не начат | 0% |
| [`0x03da0`](functions_mcu/func_0x03da0.md) | 58 | код B | — | — | не начат | 0% |
| [`0x03de4`](functions_mcu/func_0x03de4.md) | 252 | код B | — | — | не начат | 0% |
| [`0x03f00`](functions_mcu/func_0x03f00.md) | 912 | код B | — | — | не начат | 0% |
| [`0x042b8`](functions_mcu/func_0x042b8.md) | 118 | код B | — | — | не начат | 0% |
| [`0x04344`](functions_mcu/func_0x04344.md) | 324 | код B | — | — | не начат | 0% |
| [`0x044c0`](functions_mcu/func_0x044c0.md) | 58 | код B | — | — | не начат | 0% |
| [`0x04508`](functions_mcu/func_0x04508.md) | 266 | код B | — | — | не начат | 0% |
| [`0x04630`](functions_mcu/func_0x04630.md) | 146 | код B | — | — | не начат | 0% |
| [`0x048d8`](functions_mcu/func_0x048d8.md) | 32 | код B | — | — | не начат | 0% |
| [`0x048f8`](functions_mcu/func_0x048f8.md) | 142 | код B | — | — | не начат | 0% |
| [`0x04994`](functions_mcu/func_0x04994.md) | 18 | код B | — | — | не начат | 0% |
| [`0x049b8`](functions_mcu/func_0x049b8.md) | 70 | код B | — | — | не начат | 0% |
| [`0x04a04`](functions_mcu/func_0x04a04.md) | 24 | код B | — | — | не начат | 0% |
| [`0x04a30`](functions_mcu/func_0x04a30.md) | 26 | код B | — | — | не начат | 0% |
| [`0x04a4c`](functions_mcu/func_0x04a4c.md) | 160 | код B | — | — | не начат | 0% |
| [`0x04b04`](functions_mcu/func_0x04b04.md) | 28 | код B | — | — | не начат | 0% |
| [`0x04b20`](functions_mcu/func_0x04b20.md) | 150 | код B | — | — | не начат | 0% |
| [`0x04bc0`](functions_mcu/func_0x04bc0.md) | 36 | код B | — | — | не начат | 0% |
| [`0x04be8`](functions_mcu/func_0x04be8.md) | 36 | код B | — | — | не начат | 0% |
| [`0x04c14`](functions_mcu/func_0x04c14.md) | 100 | код B | — | — | не начат | 0% |
| [`0x04c84`](functions_mcu/func_0x04c84.md) | 48 | код B | — | — | не начат | 0% |
| [`0x04cbc`](functions_mcu/func_0x04cbc.md) | 122 | код B | — | — | не начат | 0% |
| [`0x04d48`](functions_mcu/func_0x04d48.md) | 138 | код B | — | — | не начат | 0% |
| [`0x04de0`](functions_mcu/func_0x04de0.md) | 40 | код B | — | — | не начат | 0% |
| [`0x04e08`](functions_mcu/func_0x04e08.md) | 32 | код B | — | — | не начат | 0% |
| [`0x04e28`](functions_mcu/func_0x04e28.md) | 8 | код B | — | — | не начат | 0% |
| [`0x04e30`](functions_mcu/func_0x04e30.md) | 8 | код B | — | — | не начат | 0% |
| [`0x04e38`](functions_mcu/func_0x04e38.md) | 4 | код B | — | — | не начат | 0% |
| [`0x04f38`](functions_mcu/func_0x04f38.md) | 24 | код B | — | — | не начат | 0% |
| [`0x04f50`](functions_mcu/func_0x04f50.md) | 8 | код B | — | — | не начат | 0% |
| [`0x04f58`](functions_mcu/func_0x04f58.md) | 20 | код B | — | — | не начат | 0% |
| [`0x04f70`](functions_mcu/func_0x04f70.md) | 60 | код B | — | — | не начат | 0% |
| [`0x04fac`](functions_mcu/func_0x04fac.md) | 8 | код B | — | — | не начат | 0% |
| [`0x04fba`](functions_mcu/func_0x04fba.md) | 4 | код B | — | — | не начат | 0% |
| [`0x04fc0`](functions_mcu/func_0x04fc0.md) | 52 | код B | — | — | не начат | 0% |
| [`0x05000`](functions_mcu/func_0x05000.md) | 56 | код B | — | — | не начат | 0% |
| [`0x05044`](functions_mcu/func_0x05044.md) | 38 | код B | — | — | не начат | 0% |
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
| [`0x057f8`](functions_mcu/func_0x057f8.md) | 26 | код B | — | — | не начат | 0% |
| [`0x05818`](functions_mcu/func_0x05818.md) | 28 | код B | — | — | не начат | 0% |
| [`0x0583c`](functions_mcu/func_0x0583c.md) | 52 | код B | — | — | не начат | 0% |
| [`0x05874`](functions_mcu/func_0x05874.md) | 18 | код B | — | — | не начат | 0% |
| [`0x05888`](functions_mcu/func_0x05888.md) | 34 | код B | — | — | не начат | 0% |
| [`0x058b0`](functions_mcu/func_0x058b0.md) | 70 | код B | — | — | не начат | 0% |
| [`0x058f6`](functions_mcu/func_0x058f6.md) | 18 | код B | — | — | не начат | 0% |
| [`0x05908`](functions_mcu/func_0x05908.md) | 92 | код B | — | — | не начат | 0% |
| [`0x05970`](functions_mcu/func_0x05970.md) | 6 | код B | — | — | не начат | 0% |
| [`0x05a38`](functions_mcu/func_0x05a38.md) | 30 | код B | — | — | не начат | 0% |
| [`0x05a68`](functions_mcu/func_0x05a68.md) | 32 | код B | — | — | не начат | 0% |
| [`0x05b5a`](functions_mcu/func_0x05b5a.md) | 50 | код B | — | — | не начат | 0% |
| [`0x05b8c`](functions_mcu/func_0x05b8c.md) | 10 | код B | — | — | не начат | 0% |
| [`0x05b98`](functions_mcu/func_0x05b98.md) | 30 | код B | — | — | не начат | 0% |
| [`0x05bc4`](functions_mcu/func_0x05bc4.md) | 202 | код B | — | — | не начат | 0% |
| [`0x05c9c`](functions_mcu/func_0x05c9c.md) | 26 | код B | — | — | не начат | 0% |
| [`0x05cc0`](functions_mcu/func_0x05cc0.md) | 10 | код B | — | — | не начат | 0% |
| [`0x05cd0`](functions_mcu/func_0x05cd0.md) | 194 | код B | — | — | не начат | 0% |
| [`0x05dbc`](functions_mcu/func_0x05dbc.md) | 22 | код B | — | — | не начат | 0% |
| [`0x05dd8`](functions_mcu/func_0x05dd8.md) | 262 | код B | — | — | не начат | 0% |
| [`0x05ee0`](functions_mcu/func_0x05ee0.md) | 146 | код B | — | — | не начат | 0% |
| [`0x05fb4`](functions_mcu/func_0x05fb4.md) | 32 | код B | — | — | не начат | 0% |
| [`0x06080`](functions_mcu/func_0x06080.md) | 312 | код B | — | — | не начат | 0% |
| [`0x061d4`](functions_mcu/func_0x061d4.md) | 12 | код B | — | — | не начат | 0% |
| [`0x061e4`](functions_mcu/func_0x061e4.md) | 72 | код B | — | — | не начат | 0% |
| [`0x06230`](functions_mcu/func_0x06230.md) | 78 | код B | — | — | не начат | 0% |
| [`0x06284`](functions_mcu/func_0x06284.md) | 16 | код B | — | — | не начат | 0% |
| [`0x062d4`](functions_mcu/func_0x062d4.md) | 14 | код B | — | — | не начат | 0% |
| [`0x06304`](functions_mcu/func_0x06304.md) | 24 | код B | — | — | не начат | 0% |
| [`0x06360`](functions_mcu/func_0x06360.md) | 18 | код B | — | — | не начат | 0% |
| [`0x06378`](functions_mcu/func_0x06378.md) | 12 | код B | — | — | не начат | 0% |
| [`0x06390`](functions_mcu/func_0x06390.md) | 38 | код B | — | — | не начат | 0% |
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
| [`0x0799c`](functions_mcu/func_0x0799c.md) | 144 | код B | регулятор duty (вырожден: выход ≈ -275 → 0%) + slot-3 state-machine | §39, §41 | разобран | 100% |
| [`0x07a30`](functions_mcu/func_0x07a30.md) | 820 | код B | — | — | не начат | 0% |
| [`0x07d6c`](functions_mcu/func_0x07d6c.md) | 148 | код B | — | — | не начат | 0% |
| [`0x07e70`](functions_mcu/func_0x07e70.md) | 40 | код B | — | — | не начат | 0% |
| [`0x07e98`](functions_mcu/func_0x07e98.md) | 52 | код B | — | — | не начат | 0% |
| [`0x07ed4`](functions_mcu/func_0x07ed4.md) | 18 | код B | — | — | не начат | 0% |
| [`0x07ee8`](functions_mcu/func_0x07ee8.md) | 58 | код B | — | — | не начат | 0% |
| [`0x07fb8`](functions_mcu/func_0x07fb8.md) | 28 | код B | — | — | не начат | 0% |
| [`0x07fd4`](functions_mcu/func_0x07fd4.md) | 6 | код B | — | — | не начат | 0% |
| [`0x07fdc`](functions_mcu/func_0x07fdc.md) | 56 | код B | — | — | не начат | 0% |
| [`0x080ac`](functions_mcu/func_0x080ac.md) | 84 | код B | — | — | не начат | 0% |
| [`0x081b4`](functions_mcu/func_0x081b4.md) | 212 | код B | — | — | не начат | 0% |
| [`0x082b8`](functions_mcu/func_0x082b8.md) | 44 | код B | — | — | не начат | 0% |
| [`0x082f0`](functions_mcu/func_0x082f0.md) | 12 | код B | — | — | не начат | 0% |
| [`0x0833c`](functions_mcu/func_0x0833c.md) | 6 | код B | — | — | не начат | 0% |
| [`0x08348`](functions_mcu/func_0x08348.md) | 10 | код B | — | — | не начат | 0% |
| [`0x08380`](functions_mcu/func_0x08380.md) | 26 | код B | — | — | не начат | 0% |
| [`0x083e4`](functions_mcu/func_0x083e4.md) | 74 | код B | — | — | не начат | 0% |
| [`0x08434`](functions_mcu/func_0x08434.md) | 46 | код B | — | — | не начат | 0% |
| [`0x08468`](functions_mcu/func_0x08468.md) | 10 | код B | — | — | не начат | 0% |
| [`0x084a0`](functions_mcu/func_0x084a0.md) | 22 | код B | — | — | не начат | 0% |
| [`0x084fc`](functions_mcu/func_0x084fc.md) | 26 | код B | — | — | не начат | 0% |
| [`0x0851c`](functions_mcu/func_0x0851c.md) | 24 | код B | — | — | не начат | 0% |
| [`0x08588`](functions_mcu/func_0x08588.md) | 58 | код B | — | — | не начат | 0% |
| [`0x085c8`](functions_mcu/func_0x085c8.md) | 484 | код B | — | — | не начат | 0% |
| [`0x087b0`](functions_mcu/func_0x087b0.md) | 24 | код B | — | — | не начат | 0% |
| [`0x087c8`](functions_mcu/func_0x087c8.md) | 18 | код B | — | — | не начат | 0% |
| [`0x087de`](functions_mcu/func_0x087de.md) | 4 | код B | — | — | не начат | 0% |
| [`0x087e2`](functions_mcu/func_0x087e2.md) | 10 | код B | — | — | не начат | 0% |
| [`0x087f8`](functions_mcu/func_0x087f8.md) | 60 | код B | — | — | не начат | 0% |
| [`0x08834`](functions_mcu/func_0x08834.md) | 50 | код B | — | — | не начат | 0% |
| [`0x08878`](functions_mcu/func_0x08878.md) | 6 | код B | — | — | не начат | 0% |
| [`0x08884`](functions_mcu/func_0x08884.md) | 168 | код B | — | — | не начат | 0% |
| [`0x08938`](functions_mcu/func_0x08938.md) | 260 | код B | — | — | не начат | 0% |
| [`0x08a44`](functions_mcu/func_0x08a44.md) | 8 | код B | — | — | не начат | 0% |
| [`0x08a50`](functions_mcu/func_0x08a50.md) | 54 | код B | — | — | не начат | 0% |
| [`0x08a90`](functions_mcu/func_0x08a90.md) | 94 | код B | — | — | не начат | 0% |
| [`0x08af0`](functions_mcu/func_0x08af0.md) | 6 | код B | — | — | не начат | 0% |
| [`0x08afc`](functions_mcu/func_0x08afc.md) | 14 | код B | — | — | не начат | 0% |
| [`0x08b10`](functions_mcu/func_0x08b10.md) | 56 | код B | — | — | не начат | 0% |
| [`0x08b58`](functions_mcu/func_0x08b58.md) | 50 | код B | — | — | не начат | 0% |
| [`0x08bec`](functions_mcu/func_0x08bec.md) | 388 | код B | — | — | не начат | 0% |
| [`0x08d90`](functions_mcu/func_0x08d90.md) | 6 | код B | — | — | не начат | 0% |
| [`0x08e14`](functions_mcu/func_0x08e14.md) | 6 | код B | — | — | не начат | 0% |
| [`0x08f58`](functions_mcu/func_0x08f58.md) | 26 | код B | — | — | не начат | 0% |
| [`0x08f7c`](functions_mcu/func_0x08f7c.md) | 198 | код B | — | — | не начат | 0% |
| [`0x09048`](functions_mcu/func_0x09048.md) | 80 | код B | — | — | не начат | 0% |
| [`0x090a0`](functions_mcu/func_0x090a0.md) | 60 | код B | — | — | не начат | 0% |
| [`0x09134`](functions_mcu/func_0x09134.md) | 668 | код B | — | — | не начат | 0% |
| [`0x09482`](functions_mcu/func_0x09482.md) | 12 | код B | — | — | не начат | 0% |
| [`0x09678`](functions_mcu/func_0x09678.md) | 86 | код B | — | — | не начат | 0% |
| [`0x096dc`](functions_mcu/func_0x096dc.md) | 52 | код B | — | — | не начат | 0% |
| [`0x09714`](functions_mcu/func_0x09714.md) | 52 | код B | — | — | не начат | 0% |
| [`0x09794`](functions_mcu/func_0x09794.md) | 42 | код B | — | — | не начат | 0% |
| [`0x097ca`](functions_mcu/func_0x097ca.md) | 24 | код B | — | — | не начат | 0% |
| [`0x097e2`](functions_mcu/func_0x097e2.md) | 18 | код B | — | — | не начат | 0% |
| [`0x097f4`](functions_mcu/func_0x097f4.md) | 50 | код B | — | — | не начат | 0% |
| [`0x0982c`](functions_mcu/func_0x0982c.md) | 24 | код B | — | — | не начат | 0% |
| [`0x09844`](functions_mcu/func_0x09844.md) | 24 | код B | — | — | не начат | 0% |
| [`0x0985c`](functions_mcu/func_0x0985c.md) | 24 | код B | — | — | не начат | 0% |
| [`0x09874`](functions_mcu/func_0x09874.md) | 54 | код B | — | — | не начат | 0% |
| [`0x098ae`](functions_mcu/func_0x098ae.md) | 26 | код B | — | — | не начат | 0% |
| [`0x098c8`](functions_mcu/func_0x098c8.md) | 222 | код B | — | — | не начат | 0% |
| [`0x099b4`](functions_mcu/func_0x099b4.md) | 8 | код B | — | — | не начат | 0% |
| [`0x099bc`](functions_mcu/func_0x099bc.md) | 18 | код B | — | — | не начат | 0% |
| [`0x099ce`](functions_mcu/func_0x099ce.md) | 4 | код B | — | — | не начат | 0% |
| [`0x099d4`](functions_mcu/func_0x099d4.md) | 6 | код B | — | — | не начат | 0% |
| [`0x099e0`](functions_mcu/func_0x099e0.md) | 10 | код B | — | — | не начат | 0% |
| [`0x099f0`](functions_mcu/func_0x099f0.md) | 10 | код B | — | — | не начат | 0% |
| [`0x09a00`](functions_mcu/func_0x09a00.md) | 6 | код B | — | — | не начат | 0% |
| [`0x09a0c`](functions_mcu/func_0x09a0c.md) | 6 | код B | — | — | не начат | 0% |
| [`0x09a18`](functions_mcu/func_0x09a18.md) | 8 | код B | — | — | не начат | 0% |
| [`0x09a20`](functions_mcu/func_0x09a20.md) | 34 | код B | — | — | не начат | 0% |
| [`0x09a44`](functions_mcu/func_0x09a44.md) | 80 | код B | — | — | не начат | 0% |
| [`0x09aa4`](functions_mcu/func_0x09aa4.md) | 86 | код B | — | — | не начат | 0% |
| [`0x09b08`](functions_mcu/func_0x09b08.md) | 54 | код B | — | — | не начат | 0% |
| [`0x09b44`](functions_mcu/func_0x09b44.md) | 24 | код B | — | — | не начат | 0% |
| [`0x09f64`](functions_mcu/func_0x09f64.md) | 12 | код B | — | — | не начат | 0% |
| [`0x09f70`](functions_mcu/func_0x09f70.md) | 28 | код B | — | — | не начат | 0% |
| [`0x0a6a4`](functions_mcu/func_0x0a6a4.md) | 6 | код B | — | — | не начат | 0% |
| [`0x0a788`](functions_mcu/func_0x0a788.md) | 96 | код B | — | — | не начат | 0% |
| [`0x0a7ec`](functions_mcu/func_0x0a7ec.md) | 184 | код B | — | — | не начат | 0% |
| [`0x0a8c4`](functions_mcu/func_0x0a8c4.md) | 66 | код B | — | — | не начат | 0% |
| [`0x0a910`](functions_mcu/func_0x0a910.md) | 70 | код B | — | — | не начат | 0% |
| [`0x0a960`](functions_mcu/func_0x0a960.md) | 170 | код B | — | — | не начат | 0% |
| [`0x0aa18`](functions_mcu/func_0x0aa18.md) | 170 | код B | — | — | не начат | 0% |
| [`0x0aad0`](functions_mcu/func_0x0aad0.md) | 58 | код B | — | — | не начат | 0% |
| [`0x0ab0c`](functions_mcu/func_0x0ab0c.md) | 46 | код B | — | — | не начат | 0% |
| [`0x0abf0`](functions_mcu/func_0x0abf0.md) | 46 | код B | — | — | не начат | 0% |
| [`0x0acce`](functions_mcu/func_0x0acce.md) | 458 | код B | — | — | не начат | 0% |
| [`0x0af94`](functions_mcu/func_0x0af94.md) | 250 | код B | — | — | не начат | 0% |
| [`0x0b09a`](functions_mcu/func_0x0b09a.md) | 244 | код B | — | — | не начат | 0% |
| [`0x0b302`](functions_mcu/func_0x0b302.md) | 362 | код B | — | — | не начат | 0% |
| [`0x0b476`](functions_mcu/func_0x0b476.md) | 80 | код B | — | — | не начат | 0% |
| [`0x0b4ce`](functions_mcu/func_0x0b4ce.md) | 96 | код B | — | — | не начат | 0% |
| [`0x0b53a`](functions_mcu/func_0x0b53a.md) | 64 | код B | — | — | не начат | 0% |
| [`0x0b582`](functions_mcu/func_0x0b582.md) | 72 | код B | — | — | не начат | 0% |
| [`0x0b618`](functions_mcu/func_0x0b618.md) | 56 | код B | — | — | не начат | 0% |
| [`0x0b854`](functions_mcu/func_0x0b854.md) | 10 | код B | — | — | не начат | 0% |
| [`0x0b860`](functions_mcu/func_0x0b860.md) | 94 | код B | — | — | не начат | 0% |
| [`0x0b8dc`](functions_mcu/func_0x0b8dc.md) | 128 | код B | — | — | не начат | 0% |
| [`0x0b978`](functions_mcu/func_0x0b978.md) | 32 | код B | — | — | не начат | 0% |
| [`0x0bb14`](functions_mcu/func_0x0bb14.md) | 32 | код B | — | — | не начат | 0% |
| [`0x0bc5c`](functions_mcu/func_0x0bc5c.md) | 40 | код B | — | — | не начат | 0% |
| [`0x0bc86`](functions_mcu/func_0x0bc86.md) | 56 | код B | — | — | не начат | 0% |
| [`0x0bcc0`](functions_mcu/func_0x0bcc0.md) | 138 | код B | — | — | не начат | 0% |
| [`0x0bd50`](functions_mcu/func_0x0bd50.md) | 280 | код B | — | — | не начат | 0% |
| [`0x0be6c`](functions_mcu/func_0x0be6c.md) | 104 | код B | — | — | не начат | 0% |
| [`0x0befc`](functions_mcu/func_0x0befc.md) | 74 | код B | — | — | не начат | 0% |
| [`0x0bf4c`](functions_mcu/func_0x0bf4c.md) | 12 | код B | — | — | не начат | 0% |
| [`0x0bf58`](functions_mcu/func_0x0bf58.md) | 184 | код B | — | — | не начат | 0% |
| [`0x0c02c`](functions_mcu/func_0x0c02c.md) | 92 | код B | — | — | не начат | 0% |
| [`0x0c098`](functions_mcu/func_0x0c098.md) | 24 | код B | — | — | не начат | 0% |
| [`0x0c0b4`](functions_mcu/func_0x0c0b4.md) | 78 | код B | — | — | не начат | 0% |
| [`0x0c138`](functions_mcu/func_0x0c138.md) | 26 | код B | — | — | не начат | 0% |
| [`0x0c158`](functions_mcu/func_0x0c158.md) | 164 | код B | — | — | не начат | 0% |
| [`0x0c200`](functions_mcu/func_0x0c200.md) | 12 | код B | — | — | не начат | 0% |
| [`0x0c20c`](functions_mcu/func_0x0c20c.md) | 134 | код B | — | — | не начат | 0% |
| [`0x0c2a8`](functions_mcu/func_0x0c2a8.md) | 84 | код B | — | — | не начат | 0% |
| [`0x0c304`](functions_mcu/func_0x0c304.md) | 96 | код B | — | — | не начат | 0% |
| [`0x0c368`](functions_mcu/func_0x0c368.md) | 172 | код B | — | — | не начат | 0% |
| [`0x0c420`](functions_mcu/func_0x0c420.md) | 60 | код B | — | — | не начат | 0% |
| [`0x0c464`](functions_mcu/func_0x0c464.md) | 20 | код B | — | — | не начат | 0% |
| [`0x0c4b4`](functions_mcu/func_0x0c4b4.md) | 18 | код B | — | — | не начат | 0% |
| [`0x0c4cc`](functions_mcu/func_0x0c4cc.md) | 70 | код B | — | — | не начат | 0% |
| [`0x0c518`](functions_mcu/func_0x0c518.md) | 34 | код B | — | — | не начат | 0% |
| [`0x0c540`](functions_mcu/func_0x0c540.md) | 58 | код B | — | — | не начат | 0% |
| [`0x0c580`](functions_mcu/func_0x0c580.md) | 18 | код B | — | — | не начат | 0% |
| [`0x0c598`](functions_mcu/func_0x0c598.md) | 20 | код B | — | — | не начат | 0% |
| [`0x0c5b0`](functions_mcu/func_0x0c5b0.md) | 56 | код B | — | — | не начат | 0% |
| [`0x0c60c`](functions_mcu/func_0x0c60c.md) | 18 | код B | — | — | не начат | 0% |
| [`0x0c624`](functions_mcu/func_0x0c624.md) | 26 | код B | — | — | не начат | 0% |
| [`0x0c684`](functions_mcu/func_0x0c684.md) | 26 | код B | — | — | не начат | 0% |
| [`0x0c6a4`](functions_mcu/func_0x0c6a4.md) | 26 | код B | — | — | не начат | 0% |
| [`0x0c6c4`](functions_mcu/func_0x0c6c4.md) | 26 | код B | — | — | не начат | 0% |
| [`0x0c6f0`](functions_mcu/func_0x0c6f0.md) | 6 | код B | — | — | не начат | 0% |
| [`0x0c708`](functions_mcu/func_0x0c708.md) | 86 | код B | — | — | не начат | 0% |
| [`0x0c858`](functions_mcu/func_0x0c858.md) | 52 | код B | — | — | не начат | 0% |
| [`0x0c894`](functions_mcu/func_0x0c894.md) | 10 | код B | — | — | не начат | 0% |
| [`0x0c8a4`](functions_mcu/func_0x0c8a4.md) | 56 | код B | — | — | не начат | 0% |
| [`0x0c8dc`](functions_mcu/func_0x0c8dc.md) | 56 | код B | — | — | не начат | 0% |
| [`0x0c914`](functions_mcu/func_0x0c914.md) | 56 | код B | — | — | не начат | 0% |
| [`0x0c94c`](functions_mcu/func_0x0c94c.md) | 54 | код B | — | — | не начат | 0% |
| [`0x0c984`](functions_mcu/func_0x0c984.md) | 30 | код B | — | — | не начат | 0% |
| [`0x0c9a8`](functions_mcu/func_0x0c9a8.md) | 22 | код B | — | — | не начат | 0% |
| [`0x0c9be`](functions_mcu/func_0x0c9be.md) | 28 | код B | — | — | не начат | 0% |
| [`0x0ca3c`](functions_mcu/func_0x0ca3c.md) | 144 | код B | — | — | не начат | 0% |
| [`0x0cb10`](functions_mcu/func_0x0cb10.md) | 42 | код B | — | — | не начат | 0% |
| [`0x0cb40`](functions_mcu/func_0x0cb40.md) | 116 | код B | — | — | не начат | 0% |
| [`0x0cbb8`](functions_mcu/func_0x0cbb8.md) | 68 | код B | — | — | не начат | 0% |
| [`0x0cc08`](functions_mcu/func_0x0cc08.md) | 14 | код B | — | — | не начат | 0% |
| [`0x0cc1c`](functions_mcu/func_0x0cc1c.md) | 68 | код B | — | — | не начат | 0% |
| [`0x0cc68`](functions_mcu/func_0x0cc68.md) | 76 | код B | — | — | не начат | 0% |
| [`0x0ccbc`](functions_mcu/func_0x0ccbc.md) | 72 | код B | — | — | не начат | 0% |
| [`0x0cd0c`](functions_mcu/func_0x0cd0c.md) | 110 | код B | — | — | не начат | 0% |
| [`0x0cd80`](functions_mcu/func_0x0cd80.md) | 136 | код B | — | — | не начат | 0% |
| [`0x0ce68`](functions_mcu/func_0x0ce68.md) | 8 | код B | — | — | не начат | 0% |
| [`0x0ce70`](functions_mcu/func_0x0ce70.md) | 92 | код B | — | — | не начат | 0% |
| [`0x0ced0`](functions_mcu/func_0x0ced0.md) | 16 | код B | — | — | не начат | 0% |
| [`0x0cee0`](functions_mcu/func_0x0cee0.md) | 68 | код B | — | — | не начат | 0% |
| [`0x0cf60`](functions_mcu/func_0x0cf60.md) | 84 | код B | — | — | не начат | 0% |
| [`0x0cfb8`](functions_mcu/func_0x0cfb8.md) | 78 | код B | — | — | не начат | 0% |
| [`0x0d00c`](functions_mcu/func_0x0d00c.md) | 534 | код B | — | — | не начат | 0% |
| [`0x0d240`](functions_mcu/func_0x0d240.md) | 82 | код B | — | — | не начат | 0% |
| [`0x0d298`](functions_mcu/func_0x0d298.md) | 46 | код B | — | — | не начат | 0% |
| [`0x0d33c`](functions_mcu/func_0x0d33c.md) | 84 | код B | — | — | не начат | 0% |
| [`0x0d39c`](functions_mcu/func_0x0d39c.md) | 202 | код B | — | — | не начат | 0% |
| [`0x0d46c`](functions_mcu/func_0x0d46c.md) | 182 | код B | — | — | не начат | 0% |
| [`0x0d534`](functions_mcu/func_0x0d534.md) | 152 | код B | — | — | не начат | 0% |
| [`0x0d5d4`](functions_mcu/func_0x0d5d4.md) | 146 | код B | — | — | не начат | 0% |
| [`0x0d670`](functions_mcu/func_0x0d670.md) | 110 | код B | — | — | не начат | 0% |
| [`0x0d6e4`](functions_mcu/func_0x0d6e4.md) | 36 | код B | — | — | не начат | 0% |
| [`0x0d70c`](functions_mcu/func_0x0d70c.md) | 36 | код B | — | — | не начат | 0% |
| [`0x0d734`](functions_mcu/func_0x0d734.md) | 36 | код B | — | — | не начат | 0% |
| [`0x0d75c`](functions_mcu/func_0x0d75c.md) | 36 | код B | — | — | не начат | 0% |
| [`0x0d784`](functions_mcu/func_0x0d784.md) | 36 | код B | — | — | не начат | 0% |
| [`0x0d7ac`](functions_mcu/func_0x0d7ac.md) | 36 | код B | — | — | не начат | 0% |
| [`0x0d7d4`](functions_mcu/func_0x0d7d4.md) | 36 | код B | — | — | не начат | 0% |
| [`0x0d7fc`](functions_mcu/func_0x0d7fc.md) | 36 | код B | — | — | не начат | 0% |
| [`0x0d824`](functions_mcu/func_0x0d824.md) | 36 | код B | — | — | не начат | 0% |
| [`0x0d850`](functions_mcu/func_0x0d850.md) | 36 | код B | — | — | не начат | 0% |
| [`0x0d878`](functions_mcu/func_0x0d878.md) | 190 | код B | — | — | не начат | 0% |
| [`0x0d938`](functions_mcu/func_0x0d938.md) | 970 | код B | — | — | не начат | 0% |
| [`0x0dd2c`](functions_mcu/func_0x0dd2c.md) | 84 | код B | — | — | не начат | 0% |
| [`0x0ddc4`](functions_mcu/func_0x0ddc4.md) | 58 | код B | — | — | не начат | 0% |
| [`0x0de0a`](functions_mcu/func_0x0de0a.md) | 196 | код B | — | — | не начат | 0% |
| [`0x0ded4`](functions_mcu/func_0x0ded4.md) | 54 | код B | — | — | не начат | 0% |
| [`0x0df10`](functions_mcu/func_0x0df10.md) | 338 | код B | — | — | не начат | 0% |
| [`0x0e160`](functions_mcu/func_0x0e160.md) | 24 | код B | — | — | не начат | 0% |
| [`0x0e17c`](functions_mcu/func_0x0e17c.md) | 128 | код B | — | — | не начат | 0% |
| [`0x0e200`](functions_mcu/func_0x0e200.md) | 198 | код B | — | — | не начат | 0% |
| [`0x0e2cc`](functions_mcu/func_0x0e2cc.md) | 44 | код B | — | — | не начат | 0% |
| [`0x0e2fc`](functions_mcu/func_0x0e2fc.md) | 104 | код B | — | — | не начат | 0% |
| [`0x0e36c`](functions_mcu/func_0x0e36c.md) | 114 | код B | — | — | не начат | 0% |
| [`0x0e3e4`](functions_mcu/func_0x0e3e4.md) | 6 | код B | — | — | не начат | 0% |
| [`0x0e3ec`](functions_mcu/func_0x0e3ec.md) | 24 | код B | — | — | не начат | 0% |
| [`0x0e408`](functions_mcu/func_0x0e408.md) | 566 | код B | slew-лимитер → u16@RAM[0x1357] (duty% = byte@0xFD3) | §39, §41 | разобран | 100% |
| [`0x0e658`](functions_mcu/func_0x0e658.md) | 136 | код B | round-robin диспетчер 6 задач (TBB @0xE684) | §39.5b | разобран | 100% |
| [`0x0e6ec`](functions_mcu/func_0x0e6ec.md) | 18 | код B | — | — | не начат | 0% |
| [`0x0e704`](functions_mcu/func_0x0e704.md) | 54 | код B | — | — | не начат | 0% |
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
| [`0x106a0`](functions_mcu/func_0x106a0.md) | 24 | код C | — | — | не начат | 0% |
| [`0x106b8`](functions_mcu/func_0x106b8.md) | 28 | код C | — | — | не начат | 0% |
| [`0x106d8`](functions_mcu/func_0x106d8.md) | 54 | код C | — | — | не начат | 0% |
| [`0x10718`](functions_mcu/func_0x10718.md) | 18 | код C | — | — | не начат | 0% |
| [`0x1072a`](functions_mcu/func_0x1072a.md) | 6 | код C | — | — | не начат | 0% |
| [`0x10730`](functions_mcu/func_0x10730.md) | 4 | код C | — | — | не начат | 0% |
| [`0x10734`](functions_mcu/func_0x10734.md) | 60 | код C | — | — | не начат | 0% |
| [`0x10770`](functions_mcu/func_0x10770.md) | 16 | код C | — | — | не начат | 0% |
| [`0x10780`](functions_mcu/func_0x10780.md) | 8 | код C | — | — | не начат | 0% |
| [`0x10788`](functions_mcu/func_0x10788.md) | 92 | код C | — | — | не начат | 0% |
| [`0x107ec`](functions_mcu/func_0x107ec.md) | 126 | код C | — | — | не начат | 0% |
| [`0x10870`](functions_mcu/func_0x10870.md) | 98 | код C | — | — | не начат | 0% |
| [`0x1093c`](functions_mcu/func_0x1093c.md) | 118 | код C | — | — | не начат | 0% |
| [`0x10a20`](functions_mcu/func_0x10a20.md) | 8 | код C | — | — | не начат | 0% |
| [`0x10a5c`](functions_mcu/func_0x10a5c.md) | 50 | код C | — | — | не начат | 0% |
| [`0x10abc`](functions_mcu/func_0x10abc.md) | 60 | код C | — | — | не начат | 0% |
| [`0x10ba0`](functions_mcu/func_0x10ba0.md) | 160 | код C | — | — | не начат | 0% |
| [`0x10cdc`](functions_mcu/func_0x10cdc.md) | 152 | код C | — | — | не начат | 0% |
| [`0x110f0`](functions_mcu/func_0x110f0.md) | 10 | код D | — | — | не начат | 0% |
| [`0x110fc`](functions_mcu/func_0x110fc.md) | 400 | код D | — | — | не начат | 0% |
| [`0x11350`](functions_mcu/func_0x11350.md) | 30 | код D | — | — | не начат | 0% |
| [`0x11668`](functions_mcu/func_0x11668.md) | 12 | код D | — | — | не начат | 0% |
| [`0x11674`](functions_mcu/func_0x11674.md) | 168 | код D | — | — | не начат | 0% |
| [`0x11724`](functions_mcu/func_0x11724.md) | 166 | код D | — | — | не начат | 0% |
| [`0x117d4`](functions_mcu/func_0x117d4.md) | 172 | код D | — | — | не начат | 0% |
| [`0x11888`](functions_mcu/func_0x11888.md) | 12 | код D | — | — | не начат | 0% |
| [`0x11894`](functions_mcu/func_0x11894.md) | 204 | код D | — | — | не начат | 0% |
| [`0x11978`](functions_mcu/func_0x11978.md) | 32 | код D | — | — | не начат | 0% |
| [`0x11998`](functions_mcu/func_0x11998.md) | 44 | код D | — | — | не начат | 0% |
| [`0x119c4`](functions_mcu/func_0x119c4.md) | 32 | код D | — | — | не начат | 0% |
| [`0x119e4`](functions_mcu/func_0x119e4.md) | 434 | код D | — | — | не начат | 0% |
| [`0x11bac`](functions_mcu/func_0x11bac.md) | 130 | код D | — | — | не начат | 0% |
| [`0x11c3c`](functions_mcu/func_0x11c3c.md) | 34 | код D | — | — | не начат | 0% |
| [`0x11c5e`](functions_mcu/func_0x11c5e.md) | 38 | код D | — | — | не начат | 0% |
| [`0x11cac`](functions_mcu/func_0x11cac.md) | 8 | код D | — | — | не начат | 0% |
| [`0x11cb4`](functions_mcu/func_0x11cb4.md) | 188 | код D | — | — | не начат | 0% |
| [`0x11d98`](functions_mcu/func_0x11d98.md) | 58 | код D | — | — | не начат | 0% |
| [`0x11de8`](functions_mcu/func_0x11de8.md) | 1410 | код D | — | — | не начат | 0% |
| [`0x1238c`](functions_mcu/func_0x1238c.md) | 48 | код D | — | — | не начат | 0% |
| [`0x123c0`](functions_mcu/func_0x123c0.md) | 10 | код D | — | — | не начат | 0% |
| [`0x12804`](functions_mcu/func_0x12804.md) | 40 | код E | — | — | не начат | 0% |
| [`0x128c8`](functions_mcu/func_0x128c8.md) | 18 | код E | — | — | не начат | 0% |
| [`0x128e4`](functions_mcu/func_0x128e4.md) | 114 | код E | — | — | не начат | 0% |
| [`0x129b4`](functions_mcu/func_0x129b4.md) | 46 | код E | — | — | не начат | 0% |
| [`0x12a64`](functions_mcu/func_0x12a64.md) | 18 | код E | — | — | не начат | 0% |
| [`0x12a78`](functions_mcu/func_0x12a78.md) | 110 | код E | — | — | не начат | 0% |
| [`0x12aec`](functions_mcu/func_0x12aec.md) | 96 | код E | — | — | не начат | 0% |
| [`0x12b50`](functions_mcu/func_0x12b50.md) | 190 | код E | — | — | не начат | 0% |
| [`0x12c24`](functions_mcu/func_0x12c24.md) | 56 | код E | — | — | не начат | 0% |
| [`0x12d04`](functions_mcu/func_0x12d04.md) | 134 | код E | — | — | не начат | 0% |
| [`0x12d90`](functions_mcu/func_0x12d90.md) | 190 | код E | — | — | не начат | 0% |
| [`0x12e64`](functions_mcu/func_0x12e64.md) | 56 | код E | — | — | не начат | 0% |
| [`0x12f44`](functions_mcu/func_0x12f44.md) | 134 | код E | — | — | не начат | 0% |
| [`0x12fd0`](functions_mcu/func_0x12fd0.md) | 8 | код E | — | — | не начат | 0% |
| [`0x12fd8`](functions_mcu/func_0x12fd8.md) | 8 | код E | — | — | не начат | 0% |
| [`0x12fe0`](functions_mcu/func_0x12fe0.md) | 66 | код E | — | — | не начат | 0% |
| [`0x1302c`](functions_mcu/func_0x1302c.md) | 134 | код E | init/драйвер трёх USART | §6.5 | частично | 50% |
| [`0x130f2`](functions_mcu/func_0x130f2.md) | 80 | код E | — | — | не начат | 0% |
| [`0x13148`](functions_mcu/func_0x13148.md) | 168 | код E | — | — | не начат | 0% |
| [`0x131fc`](functions_mcu/func_0x131fc.md) | 130 | код E | — | — | не начат | 0% |
| [`0x13284`](functions_mcu/func_0x13284.md) | 130 | код E | — | — | не начат | 0% |
| [`0x1330c`](functions_mcu/func_0x1330c.md) | 106 | код E | — | — | не начат | 0% |
| [`0x1337c`](functions_mcu/func_0x1337c.md) | 1472 | код E | — | — | не начат | 0% |
| [`0x1395c`](functions_mcu/func_0x1395c.md) | 36 | код E | — | — | не начат | 0% |
| [`0x139ac`](functions_mcu/func_0x139ac.md) | 14 | код E | — | — | не начат | 0% |
| [`0x139fc`](functions_mcu/func_0x139fc.md) | 226 | код E | — | — | не начат | 0% |
| [`0x13b14`](functions_mcu/func_0x13b14.md) | 72 | код E | — | — | не начат | 0% |
| [`0x13b60`](functions_mcu/func_0x13b60.md) | 84 | код E | — | — | не начат | 0% |
| [`0x13bb8`](functions_mcu/func_0x13bb8.md) | 48 | код E | — | — | не начат | 0% |
| [`0x13c5c`](functions_mcu/func_0x13c5c.md) | 18 | код E | — | — | не начат | 0% |
| [`0x13c78`](functions_mcu/func_0x13c78.md) | 392 | код E | — | — | не начат | 0% |
| [`0x14368`](functions_mcu/func_0x14368.md) | 66 | код F | — | — | не начат | 0% |
| [`0x147ac`](functions_mcu/func_0x147ac.md) | 78 | код G | — | — | не начат | 0% |
| [`0x14802`](functions_mcu/func_0x14802.md) | 284 | код G | — | — | не начат | 0% |
| [`0x14924`](functions_mcu/func_0x14924.md) | 48 | код G | — | — | не начат | 0% |
| [`0x14958`](functions_mcu/func_0x14958.md) | 76 | код G | — | — | не начат | 0% |
| [`0x14ed0`](functions_mcu/func_0x14ed0.md) | 110 | код G | — | — | не начат | 0% |
| [`0x14f50`](functions_mcu/func_0x14f50.md) | 1572 | код G | — | — | не начат | 0% |
| [`0x155ac`](functions_mcu/func_0x155ac.md) | 64 | код G | — | — | не начат | 0% |
| [`0x15640`](functions_mcu/func_0x15640.md) | 108 | код G | — | — | не начат | 0% |
| [`0x156ac`](functions_mcu/func_0x156ac.md) | 92 | код G | — | — | не начат | 0% |
| [`0x1570c`](functions_mcu/func_0x1570c.md) | 72 | код G | — | — | не начат | 0% |
| [`0x15758`](functions_mcu/func_0x15758.md) | 48 | код G | — | — | не начат | 0% |
| [`0x15790`](functions_mcu/func_0x15790.md) | 76 | код G | — | — | не начат | 0% |
| [`0x157e0`](functions_mcu/func_0x157e0.md) | 266 | код G | — | — | не начат | 0% |
| [`0x158f8`](functions_mcu/func_0x158f8.md) | 22 | код G | — | — | не начат | 0% |
| [`0x15918`](functions_mcu/func_0x15918.md) | 242 | код G | — | — | не начат | 0% |
| [`0x15a1c`](functions_mcu/func_0x15a1c.md) | 58 | код G | — | — | не начат | 0% |
| [`0x15a60`](functions_mcu/func_0x15a60.md) | 280 | код G | — | — | не начат | 0% |
| [`0x15b84`](functions_mcu/func_0x15b84.md) | 236 | код G | — | — | не начат | 0% |
| [`0x15c94`](functions_mcu/func_0x15c94.md) | 66 | код G | — | — | не начат | 0% |
| [`0x15ce0`](functions_mcu/func_0x15ce0.md) | 36 | код G | — | — | не начат | 0% |
| [`0x15d14`](functions_mcu/func_0x15d14.md) | 216 | код G | — | — | не начат | 0% |
| [`0x15df4`](functions_mcu/func_0x15df4.md) | 242 | код G | — | — | не начат | 0% |
| [`0x15f00`](functions_mcu/func_0x15f00.md) | 116 | код G | — | — | не начат | 0% |
| [`0x15ffc`](functions_mcu/func_0x15ffc.md) | 56 | код G | — | — | не начат | 0% |
| [`0x16040`](functions_mcu/func_0x16040.md) | 252 | код G | — | — | не начат | 0% |
| [`0x16176`](functions_mcu/func_0x16176.md) | 40 | код G | — | — | не начат | 0% |
| [`0x1619e`](functions_mcu/func_0x1619e.md) | 40 | код G | — | — | не начат | 0% |
| [`0x161ea`](functions_mcu/func_0x161ea.md) | 56 | код G | — | — | не начат | 0% |
| [`0x16222`](functions_mcu/func_0x16222.md) | 68 | код G | — | — | не начат | 0% |
| [`0x16288`](functions_mcu/func_0x16288.md) | 24 | код G | — | — | не начат | 0% |
| [`0x162ce`](functions_mcu/func_0x162ce.md) | 24 | код G | — | — | не начат | 0% |
| [`0x16328`](functions_mcu/func_0x16328.md) | 24 | код G | — | — | не начат | 0% |
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
| [`0x1712c`](functions_mcu/func_0x1712c.md) | 36 | код G | — | — | не начат | 0% |
| [`0x17150`](functions_mcu/func_0x17150.md) | 32 | код G | — | — | не начат | 0% |
| [`0x17170`](functions_mcu/func_0x17170.md) | 164 | код G | — | — | не начат | 0% |
| [`0x17214`](functions_mcu/func_0x17214.md) | 164 | код G | — | — | не начат | 0% |
| [`0x172b8`](functions_mcu/func_0x172b8.md) | 78 | код G | — | — | не начат | 0% |
| [`0x17306`](functions_mcu/func_0x17306.md) | 100 | код G | — | — | не начат | 0% |
| [`0x1736a`](functions_mcu/func_0x1736a.md) | 96 | код G | — | — | не начат | 0% |
| [`0x173cc`](functions_mcu/func_0x173cc.md) | 294 | код G | — | — | не начат | 0% |
| [`0x17736`](functions_mcu/func_0x17736.md) | 108 | код G | — | — | не начат | 0% |
| [`0x177d6`](functions_mcu/func_0x177d6.md) | 8 | код G | — | — | не начат | 0% |
| [`0x178c4`](functions_mcu/func_0x178c4.md) | 12 | код G | — | — | не начат | 0% |
| [`0x19a1c`](functions_mcu/func_0x19a1c.md) | 76 | код I | — | — | не начат | 0% |
| [`0x19a68`](functions_mcu/func_0x19a68.md) | 36 | код I | — | — | не начат | 0% |
| [`0x19a8c`](functions_mcu/func_0x19a8c.md) | 14 | код I | — | — | не начат | 0% |
| [`0x19a9e`](functions_mcu/func_0x19a9e.md) | 18 | код I | — | — | не начат | 0% |
| [`0x19ab0`](functions_mcu/func_0x19ab0.md) | 162 | код I | — | — | не начат | 0% |
| [`0x19b64`](functions_mcu/func_0x19b64.md) | 120 | код I | — | — | не начат | 0% |
| [`0x19bdc`](functions_mcu/func_0x19bdc.md) | 124 | код I | — | — | не начат | 0% |
| [`0x19c58`](functions_mcu/func_0x19c58.md) | 328 | код I | — | — | не начат | 0% |
| [`0x19dbc`](functions_mcu/func_0x19dbc.md) | 202 | код I | — | — | не начат | 0% |
| [`0x19e8c`](functions_mcu/func_0x19e8c.md) | 234 | код I | — | — | не начат | 0% |
| [`0x19f7c`](functions_mcu/func_0x19f7c.md) | 44 | код I | — | — | не начат | 0% |
| [`0x19fae`](functions_mcu/func_0x19fae.md) | 16 | код I | — | — | не начат | 0% |
| [`0x19fbe`](functions_mcu/func_0x19fbe.md) | 14 | код I | — | — | не начат | 0% |
| [`0x19fcc`](functions_mcu/func_0x19fcc.md) | 34 | код I | — | — | не начат | 0% |
| [`0x19ff4`](functions_mcu/func_0x19ff4.md) | 24 | код I | — | — | не начат | 0% |
| [`0x1a010`](functions_mcu/func_0x1a010.md) | 50 | код I | — | — | не начат | 0% |
| [`0x1a052`](functions_mcu/func_0x1a052.md) | 36 | код I | — | — | не начат | 0% |
| [`0x1a080`](functions_mcu/func_0x1a080.md) | 32 | код I | — | — | не начат | 0% |
| [`0x1a0a0`](functions_mcu/func_0x1a0a0.md) | 34 | код I | — | — | не начат | 0% |
| [`0x1a0c2`](functions_mcu/func_0x1a0c2.md) | 38 | код I | — | — | не начат | 0% |
| [`0x1a16a`](functions_mcu/func_0x1a16a.md) | 26 | код I | — | — | не начат | 0% |
| [`0x1a184`](functions_mcu/func_0x1a184.md) | 164 | код I | — | — | не начат | 0% |
| [`0x1a24c`](functions_mcu/func_0x1a24c.md) | 86 | код I | — | — | не начат | 0% |
| [`0x1a2a4`](functions_mcu/func_0x1a2a4.md) | 90 | код I | — | — | не начат | 0% |
| [`0x1a31c`](functions_mcu/func_0x1a31c.md) | 522 | код I | ADC1: стейт-машина выборки (системный тик ~1 кГц) | §22, §40 | разобран | 100% |
| [`0x1a5c4`](functions_mcu/func_0x1a5c4.md) | 12 | код I | — | — | не начат | 0% |
| [`0x1a5d4`](functions_mcu/func_0x1a5d4.md) | 12 | код I | — | — | не начат | 0% |
| [`0x1a5e6`](functions_mcu/func_0x1a5e6.md) | 12 | код I | «own»: трамплин к S-box-блоку 0x1a7ac (реальный старт 0x1a5e4 `mov r2,r1` — без пролога, артефакт детекции; bl из 0x21c64) | §36.3, §37 | разобран | 100% |
| [`0x1a5f2`](functions_mcu/func_0x1a5f2.md) | 8 | код I | «own»: трамплин bl 0x1bfa0 (из 0x1a628) | §27.2, §37 | разобран | 100% |
| [`0x1a5fa`](functions_mcu/func_0x1a5fa.md) | 46 | код I | «own»: XOR двух 16-Б блоков (round, вызов из 0x1a7ac; callers=3) | §37 | разобран | 100% |
| [`0x1a628`](functions_mcu/func_0x1a628.md) | 12 | код I | трамплин к шифру: ldr r0=&0x16aa; bl 0x1bfa0 | §27.2 | разобран | 100% |
| [`0x1a638`](functions_mcu/func_0x1a638.md) | 66 | код I | — | — | не начат | 0% |
| [`0x1a688`](functions_mcu/func_0x1a688.md) | 266 | код I | — | — | не начат | 0% |
| [`0x1a7ac`](functions_mcu/func_0x1a7ac.md) | 136 | код I | «own»: S-box-подстановка + перестановка (16 Б, 10 раундов) | §37 | разобран | 100% |
| [`0x1a838`](functions_mcu/func_0x1a838.md) | 32 | код I | — | — | не начат | 0% |
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
| [`0x1d874`](functions_mcu/func_0x1d874.md) | 26 | код I | — | — | не начат | 0% |
| [`0x1d898`](functions_mcu/func_0x1d898.md) | 1254 | код I | батарея/запас хода/температура (0x306/0x30c/0x30e) | §22 | разобран | 100% |
| [`0x1dd8c`](functions_mcu/func_0x1dd8c.md) | 128 | код I | «own»: вспомогательный round (bl из 0x1a814) | §37 | частично | 50% |
| [`0x1de0c`](functions_mcu/func_0x1de0c.md) | 66 | код I | — | — | не начат | 0% |
| [`0x1de5e`](functions_mcu/func_0x1de5e.md) | 70 | код I | — | — | не начат | 0% |
| [`0x1dea4`](functions_mcu/func_0x1dea4.md) | 186 | код I | — | — | не начат | 0% |
| [`0x1df84`](functions_mcu/func_0x1df84.md) | 66 | код I | — | — | не начат | 0% |
| [`0x1dfd8`](functions_mcu/func_0x1dfd8.md) | 344 | код I | — | — | не начат | 0% |
| [`0x1e1a0`](functions_mcu/func_0x1e1a0.md) | 200 | код I | — | — | не начат | 0% |
| [`0x1e298`](functions_mcu/func_0x1e298.md) | 34 | код I | DMA+ADC (вызов из 0x1a31c) | §40 | частично | 50% |
| [`0x1e2ca`](functions_mcu/func_0x1e2ca.md) | 36 | код I | — | — | не начат | 0% |
| [`0x1e2f8`](functions_mcu/func_0x1e2f8.md) | 164 | код I | RCC+GPIOC AF-конфиг (MODER=0x044AA200) | §39 | частично | 50% |
| [`0x1e3a4`](functions_mcu/func_0x1e3a4.md) | 50 | код I | — | — | не начат | 0% |
| [`0x1e410`](functions_mcu/func_0x1e410.md) | 106 | код I | — | — | не начат | 0% |
| [`0x1e480`](functions_mcu/func_0x1e480.md) | 180 | код I | ISR USART3 (линк к BLE-чипу): статус, сброс PE/FE/ORE | §6.5 | разобран | 100% |
| [`0x1e658`](functions_mcu/func_0x1e658.md) | 218 | код I | — | — | не начат | 0% |
| [`0x1e9e0`](functions_mcu/func_0x1e9e0.md) | 1914 | код I | RX-парсер протокола USART3 | §6.5 | частично | 50% |
| [`0x1f1c0`](functions_mcu/func_0x1f1c0.md) | 6 | код I | — | — | не начат | 0% |
| [`0x1f1cc`](functions_mcu/func_0x1f1cc.md) | 114 | код I | MCU→BLE: сборщик запросов `63 CMD` (шаблон кадра) | §32 | разобран | 100% |
| [`0x1f600`](functions_mcu/func_0x1f600.md) | 156 | код I | RX USART3: кольцо + диспетчер по таблице дескрипторов | §6.7 | разобран | 100% |
| [`0x1f6b4`](functions_mcu/func_0x1f6b4.md) | 94 | код I | TX: сборка дескриптора [type=2][len][data] | §6.5 | разобран | 100% |
| [`0x1f71c`](functions_mcu/func_0x1f71c.md) | 6860 | код I | агрегатор: 24-состоянная машина (jump-table по CTX[0x10]) | §22.5 | разобран | 100% |
| [`0x211ec`](functions_mcu/func_0x211ec.md) | 6 | код I | — | — | не начат | 0% |
| [`0x211f8`](functions_mcu/func_0x211f8.md) | 1246 | код I | — | — | не начат | 0% |
| [`0x216e4`](functions_mcu/func_0x216e4.md) | 256 | код I | TX-кольцо @0x10b5 отправитель (UART4) | §28.3 | разобран | 100% |
| [`0x21804`](functions_mcu/func_0x21804.md) | 96 | код I | — | — | не начат | 0% |
| [`0x2186c`](functions_mcu/func_0x2186c.md) | 370 | код I | — | — | не начат | 0% |
| [`0x21a08`](functions_mcu/func_0x21a08.md) | 240 | код I | NVRAM-save таск (гейт byte@0x170==1 + бит31 common+0x14) | §25 | разобран | 100% |
| [`0x21b84`](functions_mcu/func_0x21b84.md) | 60 | код I | — | — | не начат | 0% |
| [`0x21c0c`](functions_mcu/func_0x21c0c.md) | 6 | код I | — | — | не начат | 0% |
| [`0x21c18`](functions_mcu/func_0x21c18.md) | 34 | код I | — | — | не начат | 0% |
| [`0x21c64`](functions_mcu/func_0x21c64.md) | 12 | код I | «own»: входной шифр/проверка кадра (initiator BLE) | §36.3, §37 | разобран | 100% |
| [`0x21ca8`](functions_mcu/func_0x21ca8.md) | 364 | код I | инициализация сенсоров ADC1 | §40 | ID | 25% |
| [`0x21e18`](functions_mcu/func_0x21e18.md) | 412 | код I | — | — | не начат | 0% |
| [`0x22000`](functions_mcu/func_0x22000.md) | 406 | код I | — | — | не начат | 0% |
| [`0x221a4`](functions_mcu/func_0x221a4.md) | 66 | код I | — | — | не начат | 0% |
| [`0x221e6`](functions_mcu/func_0x221e6.md) | 78 | код I | — | — | не начат | 0% |
| [`0x22234`](functions_mcu/func_0x22234.md) | 58 | код I | — | — | не начат | 0% |
| [`0x22274`](functions_mcu/func_0x22274.md) | 790 | код I | — | — | не начат | 0% |
| [`0x225c4`](functions_mcu/func_0x225c4.md) | 18 | код I | — | — | не начат | 0% |
| [`0x225dc`](functions_mcu/func_0x225dc.md) | 18 | код I | — | — | не начат | 0% |
| [`0x225f4`](functions_mcu/func_0x225f4.md) | 556 | код I | — | — | не начат | 0% |
| [`0x22824`](functions_mcu/func_0x22824.md) | 240 | код I | — | — | не начат | 0% |
| [`0x22934`](functions_mcu/func_0x22934.md) | 76 | код I | — | — | не начат | 0% |
| [`0x229d4`](functions_mcu/func_0x229d4.md) | 44 | код I | — | — | не начат | 0% |
| [`0x22a0c`](functions_mcu/func_0x22a0c.md) | 48 | код I | — | — | не начат | 0% |
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