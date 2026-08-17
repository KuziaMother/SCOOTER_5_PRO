#!/usr/bin/env python3
"""
Проверка и скачивание официальной прошивки Dreame Scooter 5 Pro из Mi Cloud.

Переиспользует уже залогиненный коннектор из micloud_ltmk.py (та же сессия,
что используется для получения LTMK) — отдельного входа не требуется.

Запрос — порт PluginHostApiImpl.getBluetoothFirmwareUpdateInfoV2 (реверс APK),
тот же, что tools/fetch_firmware.py уже использует как CLI-инструмент:

    POST {api}/v2/device/latest_ver
    data = {"did":.., "model":.., "platform":"android"}

Ответ несёт BLE-образ в url/md5 и MCU-образ в mcu_safe_url/mcu_md5 (плюс
diff_url для дельта-обновлений, которые мы не используем — заливаем только
полные образы).

Ничего не пишется на устройство — это чисто облачный HTTP + локальное
файловое хранилище (firmware_ota/). Сама заливка по BLE — firmware_worker.py.
"""
import hashlib
import json
import os

import micloud_ltmk as ml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(ROOT, "firmware_ota")
MODEL = "xiaomi.scooter.5pro"


class FirmwareError(Exception):
    """Ожидаемая отказная ветка (нет сессии, облако не ответило и т.п.)."""


def check_latest(did, country="ru"):
    """Спрашивает Mi Cloud про последнюю версию для did. Возвращает список
    записей [{type: "upd"|"mcu", version, url, md5}] — то, что реально можно
    скачать, без диффов и служебных полей."""
    c = ml.get_connector()
    if not c:
        raise FirmwareError("нет активной сессии Mi Cloud — сначала войдите по QR")

    url = c.get_api_url(country) + "/v2/device/latest_ver"
    data = {"did": str(did), "model": MODEL, "platform": "android",
            "plugin_level": 0, "app_level": 0}
    resp = c.execute_api_call_encrypted(url, {"data": json.dumps(data)})
    if not resp or resp.get("code") not in (0, None):
        raise FirmwareError(f"облако отказало (code={resp.get('code') if resp else '?'})")

    result = resp.get("result") or {}
    entries = []
    ble_url = result.get("url") or result.get("safe_url")
    if ble_url:
        entries.append({"type": "upd", "version": result.get("version"),
                        "url": ble_url, "md5": result.get("md5")})
    mcu_url = result.get("mcu_safe_url") or result.get("mcu_url")
    if mcu_url:
        entries.append({"type": "mcu", "version": result.get("mcu_version"),
                        "url": mcu_url, "md5": result.get("mcu_md5")})
    return entries


def local_firmware_list():
    """Уже скачанные образы в firmware_ota/ — имя файла кодирует md5/тип/модель
    (та же схема, что download() в tools/fetch_firmware.py), поэтому список
    строим прямо по именам файлов, без отдельного индекса."""
    if not os.path.isdir(OUT_DIR):
        return []
    items = []
    for fn in sorted(os.listdir(OUT_DIR)):
        if not fn.endswith(".bin"):
            continue
        path = os.path.join(OUT_DIR, fn)
        parts = fn[:-4].split("_", 2)
        md5_from_name = parts[0] if len(parts) >= 1 else None
        fw_type = parts[1] if len(parts) >= 2 else "?"
        items.append({
            "filename": fn,
            "type": fw_type,
            "md5": md5_from_name,
            "size": os.path.getsize(path),
        })
    return items


def download_firmware(url, md5_expected, fw_type):
    """Качает образ, проверяет MD5 против ОЖИДАЕМОГО (из ответа облака) —
    несовпадение — это повод остановиться, а не тихо принять повреждённый
    файл (§5: прошиваем только официальные образы со сверенным MD5)."""
    import requests
    os.makedirs(OUT_DIR, exist_ok=True)
    r = requests.get(url, timeout=60)
    if r.status_code != 200:
        raise FirmwareError(f"скачивание не удалось: HTTP {r.status_code}")
    data = r.content
    got_md5 = hashlib.md5(data).hexdigest()
    if md5_expected and got_md5.lower() != str(md5_expected).lower():
        raise FirmwareError(
            f"MD5 не совпал (получено {got_md5}, ожидалось {md5_expected}) — файл повреждён, не сохраняю")
    name = f"{got_md5}_{fw_type}_{MODEL}.bin"
    path = os.path.join(OUT_DIR, name)
    with open(path, "wb") as f:
        f.write(data)
    return {"filename": name, "type": fw_type, "md5": got_md5, "size": len(data)}
