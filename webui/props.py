#!/usr/bin/env python3
"""
Каталог свойств Scooter 5 Pro и безопасное форматирование для web UI.

Это НЕ протокольный модуль: здесь только имена, группы, единицы/enum-лейблы и
маскировка секретов. Протокол (кадры, AES-CCM, pull/ACK) остаётся в probes/spec_read.py
и dreame_auth.py; BLE-сессия для web вынесена в webui/ble_worker.py.

Жёсткие правила:
  * SENSITIVE свойства (OOB_CODE, SN) не показываются в UI — только «скрыто»;
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
    # SIID 1 — живая телеметрия
    (1, 1): "RIDING_MODE", (1, 2): "BATTERY_LEVEL", (1, 3): "REMAINING_BATTERY",
    (1, 4): "VOLTAGE", (1, 5): "CURRENT", (1, 6): "POWER",
    (1, 7): "REMAINING_MILEAGE", (1, 8): "FAULT", (1, 9): "CURRENT_MILEAGE",
    # SIID 2 — режимы/функции + накопители
    (2, 1): "AVERAGE_SPEED", (2, 2): "IS_LOCKED", (2, 3): "CRUISE_IS_ON",
    (2, 4): "TAIL_LIGHT_IS_ON", (2, 5): "ENERGY_RECOVERY", (2, 6): "TOTAL_MILEAGE",
    (2, 7): "IS_RIDING", (2, 8): "RIDING_TIME", (2, 9): "HIGHEST_SPEED",
    (2, 10): "ASR_IS_ON", (2, 11): "REMAINING_MILEAGE_ALGORITHM",
    (2, 12): "AUTO_LIGHT", (2, 13): "TCS", (2, 14): "INTELLIGENT_DOWNHILL",
    (2, 15): "HILL_PARKING", (2, 16): "ATMOSPHERE_LIGHT",
    (2, 17): "BLUETOOTH_SEARCH_ON", (2, 18): "FAKE_SHUTDOWN_STATUS",
    # SIID 3 — батарея/идентичность/журнальные метаданные
    (3, 1): "BATTERY_STATUS", (3, 2): "BATTERY_TEMPERATURE",
    (3, 3): "SCOOTER_TEMPERATURE", (3, 4): "LOCK_WARNING", (3, 5): "MILEAGE_UNIT",
    (3, 6): "OOB_CODE", (3, 7): "TIRE_MAINTENANCE", (3, 8): "ACTIVATION_DATE",
    (3, 9): "RIDING_RECORDS", (3, 10): "IS_CHARGING",
    (3, 11): "NUMBER_OF_CYCLES", (3, 12): "SOH",
    # SIID 4 — производство/прошивки/расширенная батарея
    (4, 1): "PRODUCTION_DATE", (4, 2): "BATTERY_SN", (4, 3): "BMS_FIRMWARE_VERSION",
    (4, 4): "SCOOTER_SN", (4, 5): "FIRMWARE_VERSION",
    (4, 6): "RESTORE_SCOOTER_SETTINGS", (4, 7): "MORE_BATTERY_INFO",
    (4, 8): "MORE_BATTERY_INFO_2", (4, 10): "BLUETOOTH_CAR_SEARCH",
    # SIID 6 — журнал поездок
    (6, 1): "LOG_1", (6, 2): "LOG_2", (6, 3): "LOG_3", (6, 4): "LOG_4", (6, 5): "LOG_5",
}

# Подтверждённые единицы (docs/FACTS.md). Живые скорости: raw * 0.01 = км/ч.
UNITS = {
    "VOLTAGE": (0.01, "В"), "CURRENT": (1.0, "А"), "POWER": (1.0, "Вт"),
    "TOTAL_MILEAGE": (0.01, "км"), "CURRENT_MILEAGE": (0.01, "км"),
    "REMAINING_MILEAGE": (0.01, "км"),
    "BATTERY_LEVEL": (1.0, "%"), "SOH": (1.0, "%"),
    "AVERAGE_SPEED": (0.01, "км/ч"), "HIGHEST_SPEED": (0.01, "км/ч"),
    "BATTERY_TEMPERATURE": (1.0, "°C"), "SCOOTER_TEMPERATURE": (1.0, "°C"),
    "RIDING_TIME": (1.0, "с"),
}

# Секреты: в web UI не печатаем вообще (AGENTS.md).
SENSITIVE = {(3, 6), (4, 2), (4, 4)}
# Опасные action-свойства: даже read-only дамп их не трогает без отдельного решения.
DANGEROUS_EXCLUDED = {(4, 6)}

BOOL_PROPS = {
    (2, 2), (2, 3), (2, 4), (2, 10), (2, 12), (2, 13),
    (2, 14), (2, 15), (2, 17), (2, 18), (3, 10), (4, 10),
}

FAULT_LABELS = {
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
    (1, 1): {11: "P — walk", 2: "D — standard", 3: "S — sport", 4: "X — performance"},
    (1, 8): FAULT_LABELS,
    (2, 5): {30: "weak", 60: "middle", 90: "strong"},
    (2, 7): {0: "не едет", 1: "переход", 2: "едет"},
    (2, 16): {0: "выкл", 1: "вкл", 2: "активна"},
    (3, 1): {1: "OK"},
    (3, 5): {1: "KM", 0: "MI"},
}

LOG_SET = [(6, i) for i in range(1, 6)]

# Динамический набор для поллинга. (3,5) MILEAGE_UNIT читается первым, чтобы
# дальнейшие расстояния/скорости могли конвертироваться в MI/MPH, если самокат в MI.
DYNAMIC_SET = [
    (3, 5),
    (1, 1), (2, 7), (2, 9), (2, 1), (1, 9), (2, 8),
    (1, 2), (3, 10), (1, 4), (1, 5), (1, 6), (3, 2), (1, 8),
]

# Медленный набор: настройки/функции/идентичность. Читаем раз в static_interval.
STATIC_SET = [
    (1, 3), (1, 7), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
    (2, 10), (2, 12), (2, 13), (2, 14), (2, 15), (2, 16), (2, 17), (2, 18),
    (3, 1), (3, 3), (3, 4), (3, 7), (3, 8), (3, 11), (3, 12),
    (4, 1), (4, 3), (4, 5), (4, 7), (4, 8), (4, 10),
]

FULL_SAFE_SET = list(dict.fromkeys(DYNAMIC_SET + STATIC_SET + LOG_SET))

GROUPS = [
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
    """Read-only безопасное свойство для web UI."""
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
    """Значение по коду типа (как в probes/spec_read.py)."""
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
    """1 = KM (множитель 1.0), иначе MI (0.6213712) — как в плагине."""
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


def _unit_text(name, v, unit_mult=1.0):
    if name not in UNITS or not _is_num(v):
        return None
    mul, unit = UNITS[name]
    base = v * mul
    if unit == "км" and unit_mult != 1.0:
        return f"{base * unit_mult:g} mi"
    if unit == "км/ч" and unit_mult != 1.0:
        return f"{base * unit_mult:g} mph"
    if mul != 1.0:
        return f"{base:g} {unit}"
    return f"{_num_str(v)} {unit}"


def _fmt_riding_time(v):
    if not _is_num(v) or v < 0:
        return str(v)
    s = int(v)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h}ч {m:02d}м {sec:02d}с"
    if m:
        return f"{m}м {sec:02d}с"
    return f"{sec} с"


def _fmt_tire(v):
    s = str(v).strip()
    if len(s) >= 7 and s.isdigit():
        state = "выкл" if s[0] == "2" else "вкл"
        interval = int(s[1:4])
        remaining = int(s[4:7])
        return f"напоминание {state}, интервал {interval} дн., остаток {remaining} дн."
    return s or "пусто"


def _fmt_more_battery(v):
    s = str(v).strip().lower()
    try:
        if len(s) >= 14 and all(c in "0123456789abcdef" for c in s):
            energy = int(s[0:6], 16) / 1000.0
            capacity = int(s[6:10], 16)
            deep = int(s[10:14], 16)
            return (f"отдача {energy:.2f} кВт·ч, ёмкость {capacity:g} А·ч, "
                    f"глубоких разрядов {deep}")
    except ValueError:
        pass
    return str(v) or "пусто"


def _fmt_more_battery2(v):
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
                return f"экстрем. темп.: нет данных, зарядка {charge} с"
            return (f"экстрем. темп.: {y:04d}-{mo:02d}-{d:02d} "
                    f"{h:02d}:{mi:02d}:{se:02d}, зарядка {charge} с")
    except ValueError:
        pass
    return str(v) or "пусто"


def _fmt_ride_record(rec, unit_mult=1.0):
    try:
        dur = int(rec[0:4]) / 10.0
        dist = int(rec[4:8]) / 10.0 * unit_mult
        avg = int(rec[8:12]) / 10.0 * unit_mult
        top = int(rec[12:16]) / 10.0 * unit_mult
    except (ValueError, IndexError):
        return None
    if dur == 0 and dist == 0 and avg == 0 and top == 0:
        return None
    dunit = "mi" if unit_mult != 1.0 else "км"
    sunit = "mph" if unit_mult != 1.0 else "км/ч"
    if dur >= 60:
        h, rem = divmod(int(round(dur)), 60)
        dtxt = f"{h}ч {rem:02d}м"
    else:
        dtxt = f"{int(dur)} мин"
    return f"{dtxt}, {dist:.1f} {dunit}, ср {avg:.1f} {sunit}, макс {top:.1f} {sunit}"


def _fmt_ride_log(v, unit_mult=1.0):
    s = str(v).strip()
    if not s:
        return "пусто"
    recs = []
    for i in range(0, len(s), 16):
        chunk = s[i:i + 16]
        if len(chunk) < 16:
            break
        txt = _fmt_ride_record(chunk, unit_mult)
        if txt:
            recs.append(txt)
    return "; ".join(recs) if recs else "пусто"


def format_property(siid, piid, tcode, val, unit_mult=1.0):
    """Безопасный человекочитаемый вид одного свойства (секреты маскируются)."""
    key = f"{siid}.{piid}"
    name = NAMES.get((siid, piid), "?")
    base = {
        "key": key, "siid": siid, "piid": piid, "name": name,
        "type": TYPES.get(tcode, f"type{tcode}"), "secret": False,
        "raw": None, "text": "пусто", "groups": PROP_GROUPS.get((siid, piid), []),
    }

    if (siid, piid) in SENSITIVE:
        base["secret"] = True
        base["text"] = f"скрыто ({len(val)} байт)" if val else "скрыто"
        return base

    if not val:
        return base

    v = decode_value(tcode, val)
    base["raw"] = val[:64].hex()
    text = None

    if (siid, piid) == (3, 7):
        text = _fmt_tire(v)
    elif (siid, piid) == (4, 7):
        text = _fmt_more_battery(v)
    elif (siid, piid) == (4, 8):
        text = _fmt_more_battery2(v)
    elif siid == 6 and 1 <= piid <= 5:
        text = _fmt_ride_log(v, unit_mult)
    elif (siid, piid) == (2, 8):
        text = _fmt_riding_time(v)
    elif (siid, piid) in ENUM_LABELS:
        k = int(v) if _is_num(v) and float(v).is_integer() else v
        label = ENUM_LABELS[(siid, piid)].get(k)
        text = f"{label} (raw {v})" if label is not None else str(v)
    elif (siid, piid) in BOOL_PROPS:
        try:
            iv = int(v)
            text = "вкл" if iv else "выкл"
        except (TypeError, ValueError):
            text = str(v)
    else:
        unit_text = _unit_text(name, v, unit_mult)
        if unit_text is not None:
            text = unit_text
        else:
            text = _num_str(v)

    base["text"] = text
    return base
