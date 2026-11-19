# -*- coding: utf-8 -*-
"""
Эмуляторная верификация записей каталога ANALYZED_MCU (gen_maps.py).

Для каждой разобранной функции — свой тест: исполняем РЕАЛЬНЫЙ код на Unicorn
случайными входами и сверяем результат с независимым Python-референсом
(задокументированное поведение из REPORT.md/каталога).

Разделение (2026-11-17): ядро (Run, регистр TESTS, main, _intercept/_fresh_call)
— в fv_core.py; тесты — в модулях fv_tests_*.py (порядок импортов = порядок
регистрации). Тесты регистрируются при импорте через t(off, desc).

Запуск:  python -X utf8 research/scripts/mcu/func_verify.py [--only 0x126c] [--seed N] [--iters N]
         python -X utf8 research/scripts/mcu/func_verify.py --list   # покрытые функции

Добавление теста — функция-тест в любом fv_tests_*.py:
    @t(0x126C, 'u64 LSR')
    def _(run, rng):
        lo, hi, n = ...
        r0, r1 = run.call(0x126C, (lo, hi, n))
        assert (r0, r1) == expected, f'...'
"""
import sys

from fv_core import main  # noqa: F401

# порядок импортов = порядок регистрации тестов (как в исходном моно-файле)
import fv_tests_a    # noqa: F401,E402  (332-2325)
import fv_tests_b    # noqa: F401,E402  (2326-4331)
import fv_tests_c    # noqa: F401,E402  (4332-4902)
import fv_tests_e2a  # noqa: F401,E402  (E2-batch1..12)
import fv_tests_e2b  # noqa: F401,E402  (E2-batch13..24)
import fv_tests_e2c  # noqa: F401,E402  (E2-batch25..35)
import fv_tests_e2d  # noqa: F401,E402  (E2-batch36..48)
import fv_tests_e2e  # noqa: F401,E402  (E2-batch49..53)
import fv_tests_e2f  # noqa: F401,E402  (E2-batch54..56)
import fv_tests_e2g  # noqa: F401,E402  (E2-batch57 + пороговые счётчики)
import fv_tests_e2h  # noqa: F401,E402  (E2-b61..63)
import fv_tests_e2i  # noqa: F401,E402  (E2-b64)
import fv_tests_e2j  # noqa: F401,E402  (E2-b65)
import fv_tests_e2k  # noqa: F401,E402  (E2-b66)
import fv_tests_e2l  # noqa: F401,E402  (E2-b67)
import fv_tests_e2m  # noqa: F401,E402  (E2-b68)
import fv_tests_e2n  # noqa: F401,E402  (E2-b69)
import fv_tests_e2o  # noqa: F401,E402  (E2-b70)
import fv_tests_e2p  # noqa: F401,E402  (E2-b71)
import fv_tests_e2q  # noqa: F401,E402  (E2-b72)
import fv_tests_e2r  # noqa: F401,E402  (E2-b73)
import fv_tests_e2s  # noqa: F401,E402  (E2-b74)
import fv_tests_e2t  # noqa: F401,E402  (E2-b75)
import fv_tests_e2u  # noqa: F401,E402  (E2-b76)
import fv_tests_e2v  # noqa: F401,E402  (E2-b77)
import fv_tests_e2w  # noqa: F401,E402  (E2-b78)
import fv_tests_e2x  # noqa: F401,E402  (E2-b79)
import fv_tests_e2y  # noqa: F401,E402  (E2-b80)
import fv_tests_e2z  # noqa: F401,E402  (E2-b81)
import fv_tests_e3a  # noqa: F401,E402  (E2-b82)
import fv_tests_e3b  # noqa: F401,E402  (§80 B2-динамика RX)
import fv_tests_e3c  # noqa: F401,E402  (§79.3 B1-динамика командного слоя)
import fv_tests_e3d  # noqa: F401,E402  (§78.5 A3-динамика SPI-flash)
import fv_tests_e3e  # noqa: F401,E402  (§89 B3-динамика агрегатора MCU→BLE)
import fv_tests_e3f  # noqa: F401,E402  (§90 A4-динамика RTC/clock SysTick)
import fv_tests_e3g  # noqa: F401,E402  (§91 A5-динамика I2C-модель)
import fv_tests_e3h  # noqa: F401,E402  (§92 A6-динамика NVRAM-зоны/CRC)
import fv_tests_e3i  # noqa: F401,E402  (§93 A7-карта регистров периферии)
import fv_tests_e3j  # noqa: F401,E402  (§94 Phase② main-loop tick-harness)
import fv_tests_e3k  # noqa: F401,E402  (§95 Phase③ cold-boot: векторная таблица + startup)
import fv_tests_e3m  # noqa: F401,E402  (§96 BLE: app-протокол Mi Home + co-proc статик)
import fv_tests_e3n  # noqa: F401,E402  (§98 F1: 5+2 ID-записи каталога закрыты)
import fv_tests_e3o  # noqa: F401,E402  (§99 F2: siid/piid-таблица + OTA-формат)
import fv_tests_e3p  # noqa: F401,E402  (§100 F3: RX группа A 0x40/0x47/0x63)

if __name__ == '__main__':
    sys.exit(main())
