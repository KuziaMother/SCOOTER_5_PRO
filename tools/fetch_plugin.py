#!/usr/bin/env python3
"""Download Mi Home plugin for xiaomi.scooter.5pro from Mi Cloud.

Context: scooter telemetry is not exposed via standard MIoT spec, info channel 0x001c,
or MiBeacon advertisements (verified on hardware, see research/REPORT.md).
Plugin contains Dreame private protocol implementation over encrypted session.

Request matches PluginUpdateApi->updatePlugin (reversed DEX, classes2.dex):
    POST {api}/v2/plugin/fetch_plugin
Constants from L_m_j/bx9;-><clinit>: api_version=10116, api_level=111.

Session cached in secrets/micloud_session.json.

Usage:  python tools/fetch_plugin.py [--relogin] [--model M]
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
sys.argv = ["qr"]                      # token_extractor reads argv upon import
sys.path.insert(0, os.path.join(HERE, "xct"))
import token_extractor as tx           # noqa: E402


def flush(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------- session

def save_session(c):
    os.makedirs(os.path.dirname(SESSION_JSON), exist_ok=True)
    with open(SESSION_JSON, "w", encoding="utf-8") as f:
        json.dump({"userId": c.userId, "ssecurity": c._ssecurity,
                   "serviceToken": c._serviceToken, "agent": c._agent,
                   "device_id": c._device_id}, f)
    flush(f"[*] session saved: {os.path.relpath(SESSION_JSON, ROOT)} (in .gitignore)")


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
    flush("WAITING_SCAN — scan QR in Mi Home / Xiaomi Home app")
    if not c.login_step_3():
        flush("ERR step3 (scan timeout)")
        return None
    if not c.login_step_4():
        flush("ERR step4")
        return None
    flush("LOGGED_IN")
    save_session(c)
    return c


# ---------------------------------------------------------------- requests

def req_variants(model, region):
    """Alternative request payloads for fetch_plugin — tries all in one run."""
    plugins = [{"model": model}]
    latest = {"api_version": API_VERSION, "app_platform": "Android",
              "region": region, "plugins": plugins, "package_type": ""}
    backup = {"plugins": plugins, "api_level": API_LEVEL, "app_platform": "phone"}
    stand = {"api_version": API_VERSION, "app_platform": "Android",
             "stand_plugins": [{"model": model, "version": 0}]}
    yield "full (latest+backup+stand)", {
        "is_car_mihome": False, "latest_req": latest,
        "backup_req": backup, "stand_plugins": stand}
    yield "latest_req only", {"latest_req": latest}
    yield "stand_plugins only", {"stand_plugins": stand}
    yield "latest without region", {
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
    """Brief summary of non-empty response blocks."""
    r = resp.get("result") or {}
    bits = []
    for k, v in r.items():
        if isinstance(v, list):
            bits.append(f"{k}={len(v)}" + ("" if v else " (empty)"))
        elif v is None:
            bits.append(f"{k}=null")
        else:
            bits.append(f"{k}={type(v).__name__}")
    return "  ".join(bits)


def download(entry, out_dir):
    name = entry["url"].split("/")[-1].split("?")[0] or "plugin.mpk"
    dest = os.path.join(out_dir, name)
    flush(f"    downloading {name} ...")
    r = requests.get(entry["url"], timeout=180)
    if r.status_code != 200:
        flush(f"    HTTP {r.status_code}")
        return None
    with open(dest, "wb") as f:
        f.write(r.content)
    got = hashlib.md5(r.content).hexdigest()
    ok = "—" if not entry.get("md5") else ("MD5 OK" if got == entry["md5"]
                                           else "MD5 MISMATCH!")
    flush(f"    saved: {dest}  ({len(r.content)} B)  {ok}")
    return dest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--relogin", action="store_true", help="ignore cache, create new QR")
    ap.add_argument("--model", default=MODEL)
    a = ap.parse_args(sys.argv_backup[1:])

    os.makedirs(OUT_DIR, exist_ok=True)
    c = None if a.relogin else load_session()
    if c:
        flush("[*] using saved Mi Cloud session")
        if not c.execute_api_call_encrypted(
                c.get_api_url("ru") + "/v2/user/get_device_cnt", {"data": "{}"}):
            flush("[!] session expired — new QR required")
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
                flush(f"[{country}/{tag}] exception: {e}")
                continue
            if not resp:
                flush(f"[{country}/{tag}] empty response")
                continue
            code = resp.get("code")
            entries = find_downloads(resp.get("result", resp), [])
            flush(f"[{country}/{tag}] code={code}  {summarize(resp)}"
                  f"  urls={len(entries)}")
            with open(os.path.join(OUT_DIR, f"fp_{country}_{tag.split()[0]}.json"),
                      "w", encoding="utf-8") as f:
                json.dump(resp, f, ensure_ascii=False, indent=2)
            if entries:
                found = entries
                flush(f"\n>>> FOUND URLS on {country} ({tag})")
                break
        if found:
            break

    if not found:
        flush("\nno urls found in any request form — JSONs saved in plugins/")
        return 1

    sub = os.path.join(OUT_DIR, a.model)
    os.makedirs(sub, exist_ok=True)
    ok = False
    for e in found:
        flush(f"  [{e['field']}] model={e['model']} version={e['version']}")
        if download(e, sub):
            ok = True
    flush("\nDONE" if ok else "\ndownload failed")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
