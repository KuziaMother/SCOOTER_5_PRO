#!/usr/bin/env python3
"""
Проверка/скачивание ОФИЦИАЛЬНОЙ прошивки Dreame Scooter 5 Pro из Mi Cloud.

Повторяет запрос Mi Home (реверс APK, PluginHostApiImpl.getBluetoothFirmwareUpdateInfoV2):
    POST {api}/v2/device/latest_ver
    data = {"did":..,"model":..,"platform":"android"}
Ответ содержит version / url / md5 для образов (BLE «upd» и MCU «mcu»).

Сессия Mi Cloud кэшируется в secrets/micloud_session.json (как в fetch_plugin.py) —
повторный QR не нужен, пока сессия валидна. Секреты не печатаются.

По умолчанию только ПРОВЕРЯЕТ версию (без скачивания) и сравнивает с уже
установленной локально (`firmware_ota/latest_ver_ru.json`). Скачивание — по
флагу --download, ТОЛЬКО если версия отличается от уже имеющейся у нас.

Запуск:  python fetch_firmware.py                # только проверка версии
         python fetch_firmware.py --download      # + скачать, если новее
         python fetch_firmware.py --relogin        # игнорировать кэш сессии
"""
import argparse
import sys
import os
import json
import hashlib

DID = "1171744422"
MODEL = "xiaomi.scooter.5pro"
SERVERS = ["ru", "de", "cn", "sg", "us", "i2", "tw", "in"]

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(ROOT, "firmware_ota")
QR_PNG = os.path.join(HERE, "qr.png")
SESSION_JSON = os.path.join(ROOT, "secrets", "micloud_session.json")

sys.argv_backup = list(sys.argv)
sys.argv = ["qr"]
sys.path.insert(0, os.path.join(HERE, "xct"))
import token_extractor as tx  # noqa: E402


def save_session(c):
    os.makedirs(os.path.dirname(SESSION_JSON), exist_ok=True)
    with open(SESSION_JSON, "w", encoding="utf-8") as f:
        json.dump({"userId": c.userId, "ssecurity": c._ssecurity,
                   "serviceToken": c._serviceToken, "agent": c._agent,
                   "device_id": c._device_id}, f)
    flush(f"[*] сессия сохранена: {os.path.relpath(SESSION_JSON, ROOT)} (в .gitignore)")


def load_session():
    if not os.path.exists(SESSION_JSON):
        return None
    try:
        d = json.load(open(SESSION_JSON, encoding="utf-8"))
    except Exception:
        return None
    c = tx.QrCodeXiaomiCloudConnector()
    c.userId = d["userId"]
    c._ssecurity = d["ssecurity"]
    c._serviceToken = d["serviceToken"]
    c._agent = d["agent"]
    c._device_id = d["device_id"]
    return c


def flush(*a):
    print(*a, flush=True)


def latest_ver(c, country, did):
    url = c.get_api_url(country) + "/v2/device/latest_ver"
    data = {"did": str(did), "model": MODEL, "platform": "android",
            "plugin_level": 0, "app_level": 0}
    return c.execute_api_call_encrypted(url, {"data": json.dumps(data)})


def find_fw_entries(obj, acc):
    """Рекурсивно ищем компоненты прошивки. latest_ver кладёт BLE в url/md5,
    а MCU — в mcu_safe_url/mcu_md5 (и есть diff_url для дельта-обновления)."""
    if isinstance(obj, dict):
        # BLE / основной образ
        url = obj.get("url") or obj.get("safe_url") or obj.get("download_url")
        md5 = obj.get("md5") or obj.get("md5sum")
        if url and isinstance(url, str) and url.startswith("http"):
            acc.append({"url": url, "md5": md5,
                        "version": obj.get("version") or obj.get("ver"), "type": "upd"})
        # MCU-образ
        murl = obj.get("mcu_safe_url") or obj.get("mcu_url")
        if murl and isinstance(murl, str) and murl.startswith("http"):
            acc.append({"url": murl, "md5": obj.get("mcu_md5"),
                        "version": obj.get("mcu_version"), "type": "mcu"})
        for v in obj.values():
            find_fw_entries(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            find_fw_entries(v, acc)
    return acc


def download(entry, idx):
    import requests
    os.makedirs(OUT_DIR, exist_ok=True)
    r = requests.get(entry["url"], timeout=60)
    if r.status_code != 200:
        flush(f"   [!] HTTP {r.status_code}"); return
    data = r.content
    got_md5 = hashlib.md5(data).hexdigest()
    name = f"{got_md5}_{(entry.get('type') or 'fw')}_{MODEL}.bin"
    path = os.path.join(OUT_DIR, name)
    with open(path, "wb") as f:
        f.write(data)
    ok = (entry["md5"] and got_md5.lower() == str(entry["md5"]).lower())
    flush(f"   -> {path}")
    flush(f"      {len(data)} байт, md5={got_md5}, "
          f"ожидалось={entry['md5']}, MD5 {'OK' if ok else 'MISMATCH' if entry['md5'] else '(не задан)'}")


def local_versions():
    """Версии, что уже лежат у нас в firmware_ota/ (по прошлой проверке latest_ver)."""
    path = os.path.join(OUT_DIR, "latest_ver_ru.json")
    if not os.path.exists(path):
        return {}
    try:
        r = json.load(open(path, encoding="utf-8")).get("result", {})
    except Exception:
        return {}
    return {"upd": r.get("version"), "mcu": r.get("mcu_version")}


def qr_login():
    os.makedirs(HERE, exist_ok=True)
    c = tx.QrCodeXiaomiCloudConnector()
    if not c.login_step_1():
        flush("ERR step1"); return None
    img = c._session.get(c._qr_image_url)
    if img.status_code != 200:
        flush("ERR qr image"); return None
    with open(QR_PNG, "wb") as f:
        f.write(img.content)
    flush("QR_SAVED", QR_PNG)
    flush("WAITING_SCAN — отсканируй QR в приложении Mi Home / Xiaomi Home")
    if not c.login_step_3():
        flush("ERR step3 (скан/таймаут)"); return None
    if not c.login_step_4():
        flush("ERR step4"); return None
    flush("LOGGED_IN")
    save_session(c)
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--download", action="store_true",
                     help="скачать образ(ы), ТОЛЬКО если версия новее уже имеющейся")
    ap.add_argument("--relogin", action="store_true", help="игнорировать кэш сессии, новый QR")
    a = ap.parse_args(sys.argv_backup[1:])

    c = None if a.relogin else load_session()
    if c:
        flush("[*] использую сохранённую сессию Mi Cloud")
        if not c.execute_api_call_encrypted(
                c.get_api_url("ru") + "/v2/user/get_device_cnt", {"data": "{}"}):
            flush("[!] сессия недействительна — нужен новый QR")
            c = None
    if not c:
        c = qr_login()
        if not c:
            return 1

    have = local_versions()
    if have:
        flush(f"[*] уже установлено/скачано: BLE {have.get('upd')}  MCU {have.get('mcu')}")

    os.makedirs(OUT_DIR, exist_ok=True)
    for country in SERVERS:
        resp = latest_ver(c, country, DID)
        if not resp:
            continue
        code = resp.get("code")
        if code not in (0, None):
            continue
        flush(f"\n=== latest_ver @ {country} (code={code}) ===")
        with open(os.path.join(OUT_DIR, f"latest_ver_{country}.json"), "w", encoding="utf-8") as f:
            json.dump(resp, f, ensure_ascii=False, indent=2)
        entries = find_fw_entries(resp.get("result", resp), [])
        if not entries:
            flush("   (в ответе нет url/md5 — полный JSON сохранён)")
            flush("   result keys:", list((resp.get("result") or {}).keys()))
            continue
        any_newer = False
        for i, e in enumerate(entries):
            is_newer = have.get(e["type"]) is not None and e["version"] != have.get(e["type"])
            any_newer |= is_newer
            flush(f"  [{i}] type={e['type']} version={e['version']} md5={e['md5']}"
                  + ("  <-- ОТЛИЧАЕТСЯ от локальной!" if is_newer else "  (совпадает с уже имеющейся)"))
            flush(f"      url={e['url'][:90]}...")
        if a.download and any_newer:
            for i, e in enumerate(entries):
                if have.get(e["type"]) is not None and e["version"] != have.get(e["type"]):
                    download(e, i)
        elif a.download and not any_newer:
            flush("\n[*] версия не изменилась — скачивание пропущено (--download не имеет смысла)")
        elif any_newer:
            flush("\n[!] Найдена ДРУГАЯ версия. Для скачивания запусти с флагом --download")
        else:
            flush("\n[*] Версия та же, что уже у нас. Новых образов нет.")
        return 0
    flush("[!] latest_ver не вернул прошивку ни на одном сервере "
          "(проверь did/аккаунт или устройство уже на последней версии)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
