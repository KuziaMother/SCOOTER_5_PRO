#!/usr/bin/env python3
"""
Check and download official Dreame Scooter 5 Pro firmware from Mi Cloud.

Reuses authenticated connector from micloud_ltmk.py (same session
used for obtaining LTMK) — separate login not required.

Request is a port of PluginHostApiImpl.getBluetoothFirmwareUpdateInfoV2 (APK reverse),
same as tools/fetch_firmware.py already uses as CLI tool:

    POST {api}/v2/device/latest_ver
    data = {"did":.., "model":.., "platform":"android"}

Response contains BLE image in url/md5 and MCU image in mcu_safe_url/mcu_md5 (plus
diff_url for delta updates, which we do not use — we flash full images only).

Nothing is written to the device — purely cloud HTTP + local file
storage (firmware_ota/). BLE flashing itself is handled by firmware_worker.py.
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
    """Expected failure branch (no session, cloud did not respond, etc.)."""


def check_latest(did, country="ru"):
    """Queries Mi Cloud for latest version for did. Returns list of
    records [{type: "upd"|"mcu", version, url, md5}] — downloadable images,
    without diffs or internal fields."""
    c = ml.get_connector()
    if not c:
        raise FirmwareError("no active Mi Cloud session — log in via QR first")

    url = c.get_api_url(country) + "/v2/device/latest_ver"
    data = {"did": str(did), "model": MODEL, "platform": "android",
            "plugin_level": 0, "app_level": 0}
    resp = c.execute_api_call_encrypted(url, {"data": json.dumps(data)})
    if not resp or resp.get("code") not in (0, None):
        raise FirmwareError(f"cloud request rejected (code={resp.get('code') if resp else '?'})")

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
    """Already downloaded images in firmware_ota/ — filename encodes md5/type/model
    (same scheme as download() in tools/fetch_firmware.py), so list
    is built directly from filenames without separate index."""
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
    """Downloads image and verifies MD5 against EXPECTED (from cloud response) —
    mismatch stops the process rather than silently accepting corrupted
    file (§5: flash official images with verified MD5 only)."""
    import requests
    os.makedirs(OUT_DIR, exist_ok=True)
    r = requests.get(url, timeout=60)
    if r.status_code != 200:
        raise FirmwareError(f"download failed: HTTP {r.status_code}")
    data = r.content
    got_md5 = hashlib.md5(data).hexdigest()
    if md5_expected and got_md5.lower() != str(md5_expected).lower():
        raise FirmwareError(
            f"MD5 mismatch (got {got_md5}, expected {md5_expected}) — file corrupted, aborting save")
    name = f"{got_md5}_{fw_type}_{MODEL}.bin"
    path = os.path.join(OUT_DIR, name)
    with open(path, "wb") as f:
        f.write(data)
    return {"filename": name, "type": fw_type, "md5": got_md5, "size": len(data)}
