"""Общий sys.path для тестов — модули проекта сами не оформлены как пакеты
(привычка проекта: скрипты добавляют root/подпапки в sys.path при запуске),
поэтому подключаем нужные директории один раз здесь."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (ROOT, os.path.join(ROOT, "core"), os.path.join(ROOT, "probes"),
           os.path.join(ROOT, "webui"), os.path.join(ROOT, "emulator"),
           os.path.join(ROOT, "research", "scripts", "ble")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
