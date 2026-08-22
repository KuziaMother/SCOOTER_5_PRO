#!/usr/bin/env python3
"""
Скачивание плагина Mi Home для xiaomi.scooter.5pro из Mi Cloud.

Зачем: телеметрии самоката нет ни в MIoT-спеке, ни в инфо-канале 0x001c, ни в
MiBeacon-рекламе (проверено на живом устройстве, см. research/REPORT.md).
Остаётся приватный протокол Dreame поверх шифрованной сессии — его логика лежит
в плагине Mi Home для этой модели, которого в базовом APK нет.

Запрос повторяет PluginUpdateApi->updatePlugin (реверс DEX, classes2.dex):
    POST {api}/v2/plugin/fetch_plugin
    data = {"is_car_mihome":.., "latest_req":{..}, "backup_req":{..}, "stand_plugins":{..}}
Константы из L_m_j/bx9;-><clinit> (НЕ угаданные): api_version=10116, api_level=111.

Сессия Mi Cloud кэшируется в secrets/micloud_session.json (gitignored), чтобы не
сканировать QR на каждой итерации. Секреты в stdout не печатаются.

Запуск:  python tools/fetch_plugin.py [--relogin] [--model M]
"""
import argparse
import hashlib
import json
import os
import sys

import requests

MODEL = "xiaomi.scooter.5pro"
SERVERS = ["ru", "de", "cn", "sg", "us", "i2", "tw", "in"]
API_VERSION = 10116          # L_m_j/bx9;->OooO0O0
API_LEVEL = 111              # L_m_j/bx9;->OooO00o

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(ROOT, "plugins")
QR_PNG = os.path.join(OUT_DIR, "qr.png")
SESSION_JSON = os.path.join(ROOT, "secrets", "micloud_session.json")

sys.argv_backup = list(sys.argv)
sys.argv = ["qr"]                      # token_extractor читает argv при импорте
sys.path.insert(0, os.path.join(HERE, "xct"))
import token_extractor as tx           # noqa: E402


def flush(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------- сессия

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


def qr_login():
    os.makedirs(OUT_DIR, exist_ok=True)
    c = tx.QrCodeXiaomiCloudConnector()
    if not c.login_step_1():
        flush("ERR step1")
        return None
    img = c._session.get(c._qr_image_url)
    if img.status_code != 200:
        flush("ERR qr image")
        return None
    with open(QR_PNG, "wb") as f:
        f.write(img.content)
    flush(f"QR_SAVED {QR_PNG}")
    flush("WAITING_SCAN — отсканируй QR в приложении Mi Home / Xiaomi Home")
    if not c.login_step_3():
        flush("ERR step3 (скан не дождался / таймаут)")
        return None
    if not c.login_step_4():
        flush("ERR step4")
        return None
    flush("LOGGED_IN")
    save_session(c)
    return c


# ---------------------------------------------------------------- запросы

def req_variants(model, region):
    """Разные формы data для fetch_plugin — пробуем все за один прогон."""
    plugins = [{"model": model}]
    latest = {"api_version": API_VERSION, "app_platform": "Android",
              "region": region, "plugins": plugins, "package_type": ""}
    backup = {"plugins": plugins, "api_level": API_LEVEL, "app_platform": "phone"}
    stand = {"api_version": API_VERSION, "app_platform": "Android",
             "stand_plugins": [{"model": model, "version": 0}]}
    yield "полный (latest+backup+stand)", {
        "is_car_mihome": False, "latest_req": latest,
        "backup_req": backup, "stand_plugins": stand}
    yield "только latest_req", {"latest_req": latest}
    yield "только stand_plugins", {"stand_plugins": stand}
    yield "latest без region", {
        "latest_req": {k: v for k, v in latest.items() if k != "region"}}


def call(c, country, data):
    url = c.get_api_url(country) + "/v2/plugin/fetch_plugin"
    return c.execute_api_call_encrypted(url, {"data": json.dumps(data)})


def find_downloads(obj, acc, path=""):
    if isinstance(obj, dict):
        for k in ("download_url", "url", "safe_url", "package_url"):
            v = obj.get(k)
            if isinstance(v, str) and v.startswith("http"):
                acc.append({"url": v, "md5": obj.get("md5") or obj.get("file_md5"),
                            "version": obj.get("version") or obj.get("plugin_version"),
                            "model": obj.get("model"), "field": k, "path": path})
        for k, v in obj.items():
            find_downloads(v, acc, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            find_downloads(v, acc, f"{path}[{i}]")
    return acc


def summarize(resp):
    """Короткая сводка непустых блоков ответа."""
    r = resp.get("result") or {}
    bits = []
    for k, v in r.items():
        if isinstance(v, list):
            bits.append(f"{k}={len(v)}" + ("" if v else " (пусто)"))
        elif v is None:
            bits.append(f"{k}=null")
        else:
            bits.append(f"{k}={type(v).__name__}")
    return "  ".join(bits)


def download(entry, out_dir):
    name = entry["url"].split("/")[-1].split("?")[0] or "plugin.mpk"
    dest = os.path.join(out_dir, name)
    flush(f"    скачиваю {name} ...")
    r = requests.get(entry["url"], timeout=180)
    if r.status_code != 200:
        flush(f"    HTTP {r.status_code}")
        return None
    with open(dest, "wb") as f:
        f.write(r.content)
    got = hashlib.md5(r.content).hexdigest()
    ok = "—" if not entry.get("md5") else ("MD5 OK" if got == entry["md5"]
                                           else "MD5 РАСХОЖДЕНИЕ!")
    flush(f"    сохранено: {dest}  ({len(r.content)} Б)  {ok}")
    return dest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--relogin", action="store_true", help="игнорировать кэш, новый QR")
    ap.add_argument("--model", default=MODEL)
    a = ap.parse_args(sys.argv_backup[1:])

    os.makedirs(OUT_DIR, exist_ok=True)
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

    found = []
    for country in SERVERS:
        for tag, data in req_variants(a.model, country):
            try:
                resp = call(c, country, data)
            except Exception as e:
                flush(f"[{country}/{tag}] исключение: {e}")
                continue
            if not resp:
                flush(f"[{country}/{tag}] пустой ответ")
                continue
            code = resp.get("code")
            entries = find_downloads(resp.get("result", resp), [])
            flush(f"[{country}/{tag}] code={code}  {summarize(resp)}"
                  f"  ссылок={len(entries)}")
            with open(os.path.join(OUT_DIR, f"fp_{country}_{tag.split()[0]}.json"),
                      "w", encoding="utf-8") as f:
                json.dump(resp, f, ensure_ascii=False, indent=2)
            if entries:
                found = entries
                flush(f"\n>>> НАШЛИСЬ ССЫЛКИ на {country} ({tag})")
                break
        if found:
            break

    if not found:
        flush("\nссылок нет ни в одной форме запроса — JSON'ы сохранены в plugins/")
        return 1

    sub = os.path.join(OUT_DIR, a.model)
    os.makedirs(sub, exist_ok=True)
    ok = False
    for e in found:
        flush(f"  [{e['field']}] model={e['model']} version={e['version']}")
        if download(e, sub):
            ok = True
    flush("\nГОТОВО" if ok else "\nне скачалось")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
