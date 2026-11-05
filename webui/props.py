#!/usr/bin/env python3
"""
Каталог свойств Scooter 5 Pro и безопасное форматирование для web UI.

Это НЕ протокольный модуль: здесь только имена, группы, единицы/enum-лейблы и
маскировка секретов. Протокол (кадры, AES-CCM, pull/ACK) остаётся в probes/spec_read.py
и dreame_auth.py; BLE-сессия для web вынесена в webui/ble_worker.py.

Жёсткие правила:
  * SENSITIVE свойства (OOB_CODE, SN) не показываются в UI — только «скрыто» / "hidden";
  * RESTORE_SCOOTER_SETTINGS и любые action-свойства в FULL_SAFE_SET не попадают;
  * все наборы ниже — только чтение.
"""
import os
import sys
import struct

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PROBES = os.path.join(_ROOT, "probes")
for _p in (_ROOT, _PROBES):
    if _p not in sys.path:
        sys.path.insert(0, _p)


TYPES = {
    0: "BOOL", 1: "UINT8", 2: "INT8", 3: "UINT16", 4: "INT16",
    5: "UINT32", 6: "INT32", 7: "UINT64", 8: "INT64", 9: "FLOAT", 10: "STRING",
}

NAMES = {
    # SIID 1 — live telemetry
    (1, 1): "RIDING_MODE", (1, 2): "BATTERY_LEVEL", (1, 3): "REMAINING_BATTERY",
    (1, 4): "VOLTAGE", (1, 5): "CURRENT", (1, 6): "POWER",
    (1, 7): "REMAINING_MILEAGE", (1, 8): "FAULT", (1, 9): "CURRENT_MILEAGE",
    # SIID 2 — modes/functions + accumulators
    (2, 1): "AVERAGE_SPEED", (2, 2): "IS_LOCKED", (2, 3): "CRUISE_IS_ON",
    (2, 4): "TAIL_LIGHT_IS_ON", (2, 5): "ENERGY_RECOVERY", (2, 6): "TOTAL_MILEAGE",
    (2, 7): "IS_RIDING", (2, 8): "RIDING_TIME", (2, 9): "HIGHEST_SPEED",
    (2, 10): "ASR_IS_ON", (2, 11): "REMAINING_MILEAGE_ALGORITHM",
    (2, 12): "AUTO_LIGHT", (2, 13): "TCS", (2, 14): "INTELLIGENT_DOWNHILL",
    (2, 15): "HILL_PARKING", (2, 16): "ATMOSPHERE_LIGHT",
    (2, 17): "BLUETOOTH_SEARCH_ON", (2, 18): "FAKE_SHUTDOWN_STATUS",
    # SIID 3 — battery/identity/journal metadata
    (3, 1): "BATTERY_STATUS", (3, 2): "BATTERY_TEMPERATURE",
    (3, 3): "SCOOTER_TEMPERATURE", (3, 4): "LOCK_WARNING", (3, 5): "MILEAGE_UNIT",
    (3, 6): "OOB_CODE", (3, 7): "TIRE_MAINTENANCE", (3, 8): "ACTIVATION_DATE",
    (3, 9): "RIDING_RECORDS", (3, 10): "IS_CHARGING",
    (3, 11): "NUMBER_OF_CYCLES", (3, 12): "SOH",
    # SIID 4 — manufacturing/firmware/extended battery
    (4, 1): "PRODUCTION_DATE", (4, 2): "BATTERY_SN", (4, 3): "BMS_FIRMWARE_VERSION",
    (4, 4): "SCOOTER_SN", (4, 5): "FIRMWARE_VERSION",
    (4, 6): "RESTORE_SCOOTER_SETTINGS", (4, 7): "MORE_BATTERY_INFO",
    (4, 8): "MORE_BATTERY_INFO_2", (4, 10): "BLUETOOTH_CAR_SEARCH",
    # SIID 6 — ride log
    (6, 1): "LOG_1", (6, 2): "LOG_2", (6, 3): "LOG_3", (6, 4): "LOG_4", (6, 5): "LOG_5",
}

# Human-readable labels for UI (EN)
LABELS = {
    (1, 1): "Ride Mode", (1, 2): "Battery Level", (1, 3): "Remaining Battery",
    (1, 4): "Voltage", (1, 5): "Current", (1, 6): "Power",
    (1, 7): "Estimated Range", (1, 8): "Fault Code", (1, 9): "Trip Distance",
    (2, 1): "Average Speed", (2, 2): "Lock Status", (2, 3): "Cruise Control",
    (2, 4): "Tail Light", (2, 5): "Energy Recovery", (2, 6): "Odometer",
    (2, 7): "Motion Status", (2, 8): "Riding Time", (2, 9): "Top Speed",
    (2, 10): "ASR (Anti-Slip)", (2, 11): "Range Algorithm", (2, 12): "Auto Headlight",
    (2, 13): "TCS (Traction)", (2, 14): "Smart Downhill", (2, 15): "Hill Parking",
    (2, 16): "Atmosphere Light", (2, 17): "Bluetooth Search", (2, 18): "Fake Shutdown",
    (3, 1): "Battery Status", (3, 2): "Battery Temp", (3, 3): "Scooter Temp",
    (3, 4): "Lock Alarm", (3, 5): "Distance Unit", (3, 6): "OOB Code",
    (3, 7): "Tire Maintenance", (3, 8): "Activation Date", (3, 9): "Ride Records",
    (3, 10): "Charging State", (3, 11): "Charge Cycles", (3, 12): "Battery Health (SOH)",
    (4, 1): "Manufacture Date", (4, 2): "Battery SN", (4, 3): "BMS Firmware",
    (4, 4): "Scooter SN", (4, 5): "BLE Firmware", (4, 6): "Factory Reset",
    (4, 7): "Battery Details", (4, 8): "Battery Extreme Temp", (4, 10): "Vehicle Finder",
    (6, 1): "Trip Log 1", (6, 2): "Trip Log 2", (6, 3): "Trip Log 3",
    (6, 4): "Trip Log 4", (6, 5): "Trip Log 5",
}
LABELS_EN = LABELS

LABELS_RU = {
    (1, 1): "Режим", (1, 2): "Заряд", (1, 3): "Остаток заряда",
    (1, 4): "Напряжение", (1, 5): "Ток", (1, 6): "Мощность",
    (1, 7): "Запас хода", (1, 8): "Ошибка", (1, 9): "Пробег (сессия)",
    (2, 1): "Средняя скорость", (2, 2): "Замок", (2, 3): "Круиз",
    (2, 4): "Задний фонарь", (2, 5): "Рекуперация", (2, 6): "Общий пробег",
    (2, 7): "Движение", (2, 8): "Время в пути", (2, 9): "Макс. скорость",
    (2, 10): "ASR", (2, 11): "Алгоритм запаса", (2, 12): "Автосвет",
    (2, 13): "TCS", (2, 14): "Умный спуск", (2, 15): "Уклон-парковка",
    (2, 16): "Подсветка", (2, 17): "BT-поиск", (2, 18): "Ложное выкл.",
    (3, 1): "Статус батареи", (3, 2): "Темп. батареи", (3, 3): "Темп. самоката",
    (3, 4): "Сигнал замка", (3, 5): "Единицы", (3, 6): "OOB",
    (3, 7): "ТО шин", (3, 8): "Активация", (3, 9): "Записи поездок",
    (3, 10): "Зарядка", (3, 11): "Циклы заряда", (3, 12): "Здоровье батареи",
    (4, 1): "Дата производства", (4, 2): "SN батареи", (4, 3): "Прошивка BMS",
    (4, 4): "SN самоката", (4, 5): "Прошивка", (4, 6): "Сброс настроек",
    (4, 7): "Батарея (детально)", (4, 8): "Батарея (экстрим)", (4, 10): "Поиск самоката",
    (6, 1): "Журнал 1", (6, 2): "Журнал 2", (6, 3): "Журнал 3",
    (6, 4): "Журнал 4", (6, 5): "Журнал 5",
}

# Verified engineering units (EN primary)
UNITS = {
    "VOLTAGE": (0.01, "V"), "CURRENT": (1.0, "A"), "POWER": (1.0, "W"),
    "TOTAL_MILEAGE": (0.01, "km"), "CURRENT_MILEAGE": (0.01, "km"),
    "REMAINING_MILEAGE": (0.01, "km"),
    "BATTERY_LEVEL": (1.0, "%"), "SOH": (1.0, "%"),
    "AVERAGE_SPEED": (0.01, "km/h"), "HIGHEST_SPEED": (0.01, "km/h"),
    "BATTERY_TEMPERATURE": (1.0, "°C"), "SCOOTER_TEMPERATURE": (1.0, "°C"),
    "RIDING_TIME": (1.0, "s"),
}
UNITS_EN = UNITS

UNITS_RU = {
    "VOLTAGE": (0.01, "В"), "CURRENT": (1.0, "А"), "POWER": (1.0, "Вт"),
    "TOTAL_MILEAGE": (0.01, "км"), "CURRENT_MILEAGE": (0.01, "км"),
    "REMAINING_MILEAGE": (0.01, "км"),
    "BATTERY_LEVEL": (1.0, "%"), "SOH": (1.0, "%"),
    "AVERAGE_SPEED": (0.01, "км/ч"), "HIGHEST_SPEED": (0.01, "км/ч"),
    "BATTERY_TEMPERATURE": (1.0, "°C"), "SCOOTER_TEMPERATURE": (1.0, "°C"),
    "RIDING_TIME": (1.0, "с"),
}

# Secrets: never printed in web UI.
SENSITIVE = {(3, 6), (4, 2), (4, 4)}
# Dangerous action properties: omitted even from read-only dumps without explicit override.
DANGEROUS_EXCLUDED = {(4, 6)}

# Writable (SET, op=0) switches — safe settings only.
WRITABLE = {
    (2, 2): {"type": 0, "confirm": "Lock / unlock the scooter?"},
    (2, 3): {"type": 0},
    (2, 4): {"type": 0},
    (2, 12): {"type": 0},
    (2, 13): {"type": 0},
    (2, 14): {"type": 0},
    (2, 15): {"type": 0},
    (2, 17): {"type": 0},
    (2, 5): {"type": 1, "values": [30, 60, 90]},
    (2, 16): {"type": 1, "values": [0, 1, 2]},
    (3, 5): {"type": 1, "values": [1, 0]},
}
WRITABLE_CONFIRM = {
    (2, 2): "Lock / unlock the scooter?",
}
WRITABLE_CONFIRM_EN = WRITABLE_CONFIRM
WRITABLE_CONFIRM_RU = {
    (2, 2): "Заблокировать/разблокировать самокат?",
}


def is_writable(key):
    """Whether property is permitted to be modified from UI (SET op=0)."""
    if isinstance(key, str) and "." in key:
        a, b = key.split(".", 1)
        key = (int(a), int(b))
    return key in WRITABLE and key not in DANGEROUS_EXCLUDED and key not in SENSITIVE


BOOL_PROPS = {
    (2, 2), (2, 3), (2, 4), (2, 10), (2, 12), (2, 13),
    (2, 14), (2, 15), (2, 17), (2, 18), (3, 10), (4, 10),
}

FAULT_LABELS = {
    0: "normal",
    10: "dashboard communication error",
    11: "controller overload",
    12: "controller failure",
    14: "accelerator throttle cable error",
    15: "brake lever cable error",
    18: "motor failure",
    21: "battery communication error",
    24: "battery overpressure",
    28: "controller error",
    29: "controller error",
    39: "battery error",
    40: "controller error",
    45: "controller overheat",
    50: "battery temperature fault",
    52: "battery fault",
}
FAULT_LABELS_EN = FAULT_LABELS

FAULT_LABELS_RU = {
    0: "норма",
    10: "ошибка связи приборной панели",
    11: "перегрузка контроллера",
    12: "ошибка контроллера",
    14: "ошибка кабеля акселератора",
    15: "ошибка кабеля ручки тормоза",
    18: "ошибка двигателя",
    21: "ошибка связи аккумулятора",
    24: "избыточное давление в аккумуляторе",
    28: "ошибка контроллера",
    29: "ошибка контроллера",
    39: "ошибка аккумулятора",
    40: "ошибка контроллера",
    45: "перегрев контроллера",
    50: "ошибка из-за температуры аккумулятора",
    52: "ошибка аккумулятора",
}

ENUM_LABELS = {
    (1, 1): {11: "P — pedestrian", 2: "D — standard", 3: "S — sport", 4: "X — performance"},
    (1, 8): FAULT_LABELS,
    (2, 5): {30: "weak", 60: "medium", 90: "strong"},
    (2, 7): {0: "stopped", 1: "transition", 2: "riding"},
    (2, 16): {0: "off", 1: "on", 2: "active"},
    (3, 1): {1: "OK"},
    (3, 5): {1: "KM", 0: "MI"},
}
ENUM_LABELS_EN = ENUM_LABELS

ENUM_LABELS_RU = {
    (1, 1): {11: "P — walk", 2: "D — standard", 3: "S — sport", 4: "X — performance"},
    (1, 8): FAULT_LABELS_RU,
    (2, 5): {30: "weak", 60: "middle", 90: "strong"},
    (2, 7): {0: "не едет", 1: "переход", 2: "едет"},
    (2, 16): {0: "выкл", 1: "вкл", 2: "активна"},
    (3, 1): {1: "OK"},
    (3, 5): {1: "KM", 0: "MI"},
}

LOG_SET = [(6, i) for i in range(1, 6)]

# Dynamic set for polling.
DYNAMIC_SET = [
    (3, 5),
    (1, 1), (2, 7), (2, 9), (2, 1), (1, 9), (2, 8),
    (1, 2), (3, 10), (1, 4), (1, 5), (1, 6), (3, 2), (1, 8),
]

# Slow set: settings/functions/identity.
STATIC_SET = [
    (1, 3), (1, 7), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
    (2, 10), (2, 12), (2, 13), (2, 14), (2, 15), (2, 16), (2, 17), (2, 18),
    (3, 1), (3, 3), (3, 4), (3, 7), (3, 8), (3, 11), (3, 12),
    (4, 1), (4, 3), (4, 5), (4, 7), (4, 8), (4, 10),
]

FULL_SAFE_SET = list(dict.fromkeys(DYNAMIC_SET + STATIC_SET + LOG_SET))

GROUPS = [
    {
        "id": "ride", "title": "Ride",
        "props": [(1, 1), (2, 7), (2, 9), (2, 1), (2, 8), (1, 9), (1, 7), (2, 6)],
    },
    {
        "id": "battery", "title": "Battery & Power",
        "props": [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 8),
                  (3, 1), (3, 2), (3, 10), (3, 11), (3, 12)],
    },
    {
        "id": "functions", "title": "Functions & Settings",
        "props": [(2, 2), (2, 3), (2, 4), (2, 5), (2, 10), (2, 12), (2, 13),
                  (2, 14), (2, 15), (2, 16), (2, 17), (2, 18),
                  (3, 4), (3, 5), (4, 10)],
    },
    {
        "id": "identity", "title": "Device Info",
        "props": [(4, 5), (4, 3), (4, 1), (3, 8), (3, 3), (4, 7), (4, 8)],
    },
    {
        "id": "logs", "title": "Ride Logs",
        "props": LOG_SET,
    },
]
GROUPS_EN = GROUPS

GROUPS_RU = [
    {
        "id": "ride", "title": "Езда",
        "props": [(1, 1), (2, 7), (2, 9), (2, 1), (2, 8), (1, 9), (1, 7), (2, 6)],
    },
    {
        "id": "battery", "title": "Батарея и электрика",
        "props": [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 8),
                  (3, 1), (3, 2), (3, 10), (3, 11), (3, 12)],
    },
    {
        "id": "functions", "title": "Функции и настройки",
        "props": [(2, 2), (2, 3), (2, 4), (2, 5), (2, 10), (2, 12), (2, 13),
                  (2, 14), (2, 15), (2, 16), (2, 17), (2, 18),
                  (3, 4), (3, 5), (4, 10)],
    },
    {
        "id": "identity", "title": "Устройство",
        "props": [(4, 5), (4, 3), (4, 1), (3, 8), (3, 3), (4, 7), (4, 8)],
    },
    {
        "id": "logs", "title": "Журнал поездок",
        "props": LOG_SET,
    },
]

PROP_GROUPS = {}
for _g in GROUPS:
    for _p in _g["props"]:
        PROP_GROUPS.setdefault(_p, []).append(_g["id"])


def is_safe(key):
    """Read-only safe property for web UI."""
    return key in NAMES and key not in SENSITIVE and key not in DANGEROUS_EXCLUDED


def safe_filter(keys):
    out = []
    for k in keys:
        if isinstance(k, str) and "." in k:
            a, b = k.split(".", 1)
            k = (int(a), int(b))
        if is_safe(k) and k not in out:
            out.append(k)
    return out


def decode_value(tcode, val):
    """Value parsed by type code (matching probes/spec_read.py)."""
    if not val:
        return None
    if tcode == 9 and len(val) == 4:
        return struct.unpack("<f", val)[0]
    if tcode == 10:
        return val.decode("utf-8", "replace")
    if tcode in (2, 4, 6, 8):
        return int.from_bytes(val, "little", signed=True)
    return int.from_bytes(val, "little")


def unit_multiplier(mileage_unit_value):
    """1 = KM (multiplier 1.0), else MI (0.6213712) — matching plugin behavior."""
    try:
        iv = int(mileage_unit_value)
    except (TypeError, ValueError):
        return 1.0
    return 0.6213712 if iv != 1 else 1.0


def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _num_str(v):
    if isinstance(v, float):
        return f"{v:g}"
    return str(v)


def _unit_text(name, v, unit_mult=1.0, lang="en"):
    table = UNITS_EN if lang == "en" else UNITS
    if name not in table or not _is_num(v):
        return None
    mul, unit = table[name]
    base = v * mul
    if unit in ("км", "km") and unit_mult != 1.0:
        return f"{base * unit_mult:g} mi"
    if unit in ("км/ч", "km/h") and unit_mult != 1.0:
        return f"{base * unit_mult:g} mph"
    if mul != 1.0:
        return f"{base:g} {unit}"
    return f"{_num_str(v)} {unit}"


def _fmt_riding_time(v, lang="en"):
    if not _is_num(v) or v < 0:
        return str(v)
    s = int(v)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if lang == "en":
        if h:
            return f"{h}h {m:02d}m {sec:02d}s"
        if m:
            return f"{m}m {sec:02d}s"
        return f"{sec} s"
    if h:
        return f"{h}ч {m:02d}м {sec:02d}с"
    if m:
        return f"{m}м {sec:02d}с"
    return f"{sec} с"


def _fmt_tire(v, lang="en"):
    s = str(v).strip()
    if len(s) >= 7 and s.isdigit():
        interval = int(s[1:4])
        remaining = int(s[4:7])
        if lang == "en":
            state = "off" if s[0] == "2" else "on"
            return f"reminder {state}, interval {interval} days, remaining {remaining} days"
        state = "выкл" if s[0] == "2" else "вкл"
        return f"напоминание {state}, интервал {interval} дн., остаток {remaining} дн."
    return s or ("empty" if lang == "en" else "пусто")


def _fmt_more_battery(v, lang="en"):
    s = str(v).strip().lower()
    try:
        if len(s) >= 14 and all(c in "0123456789abcdef" for c in s):
            energy = int(s[0:6], 16) / 1000.0
            capacity = int(s[6:10], 16)
            deep = int(s[10:14], 16)
            if lang == "en":
                return (f"output {energy:.2f} kWh, capacity {capacity:g} Ah, "
                        f"deep discharges {deep}")
            return (f"отдача {energy:.2f} кВт·ч, ёмкость {capacity:g} А·ч, "
                    f"глубоких разрядов {deep}")
    except ValueError:
        pass
    return str(v) or ("empty" if lang == "en" else "пусто")


def _fmt_more_battery2(v, lang="en"):
    s = str(v).strip().lower()
    try:
        if len(s) >= 16 and all(c in "0123456789abcdef" for c in s):
            y = int(s[0:2], 16)
            mo = int(s[2:4], 16)
            d = int(s[4:6], 16)
            h = int(s[6:8], 16)
            mi = int(s[8:10], 16)
            se = int(s[10:12], 16)
            charge = int(s[12:16], 16)
            if y == 0 and mo == 0 and d == 0:
                if lang == "en":
                    return f"extreme temp: no data, charging {charge} s"
                return f"экстрем. темп.: нет данных, зарядка {charge} с"
            if lang == "en":
                return (f"extreme temp: {y:04d}-{mo:02d}-{d:02d} "
                        f"{h:02d}:{mi:02d}:{se:02d}, charging {charge} s")
            return (f"экстрем. темп.: {y:04d}-{mo:02d}-{d:02d} "
                    f"{h:02d}:{mi:02d}:{se:02d}, зарядка {charge} с")
    except ValueError:
        pass
    return str(v) or ("empty" if lang == "en" else "пусто")


def _fmt_ride_record(rec, unit_mult=1.0, lang="en"):
    try:
        dur = int(rec[0:4]) / 10.0
        dist = int(rec[4:8]) / 10.0 * unit_mult
        avg = int(rec[8:12]) / 10.0 * unit_mult
        top = int(rec[12:16]) / 10.0 * unit_mult
    except (ValueError, IndexError):
        return None
    if dur == 0 and dist == 0 and avg == 0 and top == 0:
        return None
    dunit = "mi" if unit_mult != 1.0 else ("km" if lang == "en" else "км")
    sunit = "mph" if unit_mult != 1.0 else ("km/h" if lang == "en" else "км/ч")
    if dur >= 60:
        h, rem = divmod(int(round(dur)), 60)
        dtxt = f"{h}h {rem:02d}m" if lang == "en" else f"{h}ч {rem:02d}м"
    else:
        dtxt = f"{int(dur)} min" if lang == "en" else f"{int(dur)} мин"
    if lang == "en":
        return f"{dtxt}, {dist:.1f} {dunit}, avg {avg:.1f} {sunit}, max {top:.1f} {sunit}"
    return f"{dtxt}, {dist:.1f} {dunit}, ср {avg:.1f} {sunit}, макс {top:.1f} {sunit}"


def ride_records(v, unit_mult=1.0, lang="en"):
    """Structured ride records (for UI list). Each is dict of column strings."""
    s = str(v).strip()
    out = []
    for i in range(0, len(s), 16):
        chunk = s[i:i + 16]
        if len(chunk) < 16:
            break
        try:
            dur = int(chunk[0:4]) / 10.0
            dist = int(chunk[4:8]) / 10.0 * unit_mult
            avg = int(chunk[8:12]) / 10.0 * unit_mult
            top = int(chunk[12:16]) / 10.0 * unit_mult
        except (ValueError, IndexError):
            continue
        if dur == 0 and dist == 0 and avg == 0 and top == 0:
            continue
        dunit = "mi" if unit_mult != 1.0 else ("km" if lang == "en" else "км")
        sunit = "mph" if unit_mult != 1.0 else ("km/h" if lang == "en" else "км/ч")
        if dur >= 60:
            h, rem = divmod(int(round(dur)), 60)
            dtxt = f"{h}h {rem:02d}m" if lang == "en" else f"{h}ч {rem:02d}м"
        else:
            dtxt = f"{int(dur)} min" if lang == "en" else f"{int(dur)} мин"
        out.append({
            "dur": dtxt, "dist": f"{dist:.1f} {dunit}",
            "avg": f"{avg:.1f} {sunit}", "top": f"{top:.1f} {sunit}",
        })
    return out


def _format_text_for_lang(siid, piid, tcode, val, v, unit_mult, lang="en"):
    name = NAMES.get((siid, piid), "?")
    if (siid, piid) in SENSITIVE:
        if lang == "en":
            return f"hidden ({len(val)} bytes)" if val else "hidden"
        return f"скрыто ({len(val)} байт)" if val else "скрыто"

    if not val:
        return "empty" if lang == "en" else "пусто"

    if (siid, piid) == (3, 7):
        return _fmt_tire(v, lang)
    if (siid, piid) == (4, 7):
        return _fmt_more_battery(v, lang)
    if (siid, piid) == (4, 8):
        return _fmt_more_battery2(v, lang)
    if siid == 6 and 1 <= piid <= 5:
        recs = ride_records(v, unit_mult, lang)
        if lang == "en":
            return f"{len(recs)} trip(s)" if recs else "empty"
        return f"{len(recs)} поездк(и)" if recs else "пусто"
    if (siid, piid) == (2, 8):
        return _fmt_riding_time(v, lang)

    enums = ENUM_LABELS_EN if lang == "en" else ENUM_LABELS
    if (siid, piid) in enums:
        k = int(v) if _is_num(v) and float(v).is_integer() else v
        label = enums[(siid, piid)].get(k)
        return f"{label} (raw {v})" if label is not None else str(v)

    if (siid, piid) in BOOL_PROPS:
        try:
            iv = int(v)
            if lang == "en":
                return "on" if iv else "off"
            return "вкл" if iv else "выкл"
        except (TypeError, ValueError):
            return str(v)

    unit_text = _unit_text(name, v, unit_mult, lang)
    if unit_text is not None:
        return unit_text
    return _num_str(v)


def format_property(siid, piid, tcode, val, unit_mult=1.0, lang="en"):
    """Safe human-readable view of a single property (masks secrets)."""
    key = f"{siid}.{piid}"
    name = NAMES.get((siid, piid), "?")
    base = {
        "key": key, "siid": siid, "piid": piid, "name": name,
        "type": TYPES.get(tcode, f"type{tcode}"), "secret": False,
        "raw": None, "text": "empty", "text_en": "empty", "text_ru": "пусто",
        "label": LABELS.get((siid, piid), name),
        "label_en": LABELS_EN.get((siid, piid), name),
        "label_ru": LABELS_RU.get((siid, piid), name),
        "groups": PROP_GROUPS.get((siid, piid), []),
    }

    if (siid, piid) in SENSITIVE:
        base["secret"] = True
        base["text"] = f"hidden ({len(val)} bytes)" if val else "hidden"
        base["text_en"] = f"hidden ({len(val)} bytes)" if val else "hidden"
        base["text_ru"] = f"скрыто ({len(val)} байт)" if val else "скрыто"
        return base

    if not val:
        return base

    v = decode_value(tcode, val)
    base["raw"] = val[:64].hex()
    if _is_num(v):
        if name in UNITS:
            mul, unit = UNITS[name]
            base["num"] = v * mul * (unit_mult if unit in ("km", "km/h", "км", "км/ч") else 1.0)
        else:
            base["num"] = v

    if siid == 6 and 1 <= piid <= 5:
        base["rides"] = ride_records(v, unit_mult, "ru")
        base["rides_en"] = ride_records(v, unit_mult, "en")

    base["text"] = _format_text_for_lang(siid, piid, tcode, val, v, unit_mult, lang)
    base["text_en"] = _format_text_for_lang(siid, piid, tcode, val, v, unit_mult, "en")
    base["text_ru"] = _format_text_for_lang(siid, piid, tcode, val, v, unit_mult, "ru")

    if lang == "ru":
        base["label"] = base["label_ru"]

    return base
