#!/usr/bin/env python3
"""
Obtaining LTMK from Mi Cloud for new scooter profiles ("My Scooters").

Reuses QR login and RC4-encrypted cloud calls from tools/xct/token_extractor.py
(same code used by tools/fetch_firmware.py) — session in
secrets/micloud_session.json is shared, repeated QR is not needed while
session remains valid.

Key extraction flow — docs/FACTS.md ("ltmk = login key, origin and
rotation") and docs/dreame_dfu_protocol.md §6.5, verified on real account
2026-08-16:

    POST /app/share/askbluetoothkey {type:own, did, keyid:0}
    -> result.{key, encrypt_type}
    encrypt_type==0: ltmk = hex_decode(key)
    encrypt_type==1 (sharing PIN set in Mi Home): ltmk = AES-128-CBC-NoPad(
        key=MD5(pincode), iv=<hardcoded in APK>, ct=hex_decode(key))

Key is never logged in full and not returned via API without explicit
"reveal" request — only length/fact of receipt (§6 CLAUDE.md).

NOT VERIFIED on real account (unlike askbluetoothkey scheme itself,
which is verified — see docs/dreame_dfu_protocol.md §6.5): device list
parsing (get_homes/get_devices) follows structure used in
tools/xct/token_extractor.py and similar Xiaomi token extractor projects;
see list_devices() below for fallback logic.
"""
import hashlib
import json
import os
import sys
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SECRETS_DIR = os.path.join(ROOT, "secrets")
SESSION_JSON = os.path.join(SECRETS_DIR, "micloud_session.json")

_xct_path = os.path.join(ROOT, "tools", "xct")
if _xct_path not in sys.path:
    sys.path.insert(0, _xct_path)

_saved_argv = sys.argv
sys.argv = ["qr"]  # token_extractor parses argv upon import (argparse) — substitute during import
import token_extractor as tx  # noqa: E402
sys.argv = _saved_argv

SERVERS = ["ru", "de", "cn", "sg", "us", "i2", "tw", "in"]
LTMK_ENCRYPT_IV = bytes.fromhex("7aa4c68c590d4031b980d98b41023800")


class LtmkError(Exception):
    """Expected failure branch (not logged in, PIN needed, device not found)."""


def _save_session(c):
    os.makedirs(SECRETS_DIR, exist_ok=True)
    with open(SESSION_JSON, "w", encoding="utf-8") as f:
        json.dump({
            "userId": c.userId, "ssecurity": c._ssecurity,
            "serviceToken": c._serviceToken, "agent": c._agent,
            "device_id": c._device_id,
        }, f)


def _load_session():
    if not os.path.exists(SESSION_JSON):
        return None
    try:
        d = json.load(open(SESSION_JSON, encoding="utf-8"))
        c = tx.QrCodeXiaomiCloudConnector()
        c.userId = d["userId"]
        c._ssecurity = d["ssecurity"]
        c._serviceToken = d["serviceToken"]
        c._agent = d["agent"]
        c._device_id = d["device_id"]
        return c
    except Exception:
        return None


def _session_valid(c):
    try:
        return bool(c.execute_api_call_encrypted(
            c.get_api_url("ru") + "/v2/user/get_device_cnt", {"data": "{}"}))
    except Exception:
        return False


# ---- current QR login session state (single webui user, local) -----------------
_state_lock = threading.Lock()
_qr_state = {"status": "idle"}  # idle|waiting|done|error


def qr_login_status():
    with _state_lock:
        return dict(_qr_state)


def has_session():
    return get_connector() is not None


def start_qr_login():
    """Returns (QR code PNG, login_url) immediately; login runs in background
    thread — waiting for scan (long-polling inside token_extractor) may take
    minutes. login_url is the same link that token_extractor.login_step_2()
    prints as "Alternatively you can visit..." — visiting it in an already logged-in
    browser finishes login without phone scan."""
    with _state_lock:
        if _qr_state.get("status") == "waiting":
            raise LtmkError("login already in progress")
        _qr_state.clear()
        _qr_state["status"] = "waiting"

    c = tx.QrCodeXiaomiCloudConnector()
    if not c.login_step_1():
        with _state_lock:
            _qr_state.update(status="error", error="failed to start login (step1)")
        raise LtmkError("failed to start login (step1)")

    img = c._session.get(c._qr_image_url)
    if img.status_code != 200:
        with _state_lock:
            _qr_state.update(status="error", error="failed to get QR image")
        raise LtmkError("failed to get QR image")
    png = img.content
    login_url = c._login_url

    def _wait():
        try:
            ok = c.login_step_3() and c.login_step_4()
        except Exception as e:
            ok = False
            err = f"{type(e).__name__}: {e}"
        else:
            err = "login declined or scan timeout expired"
        with _state_lock:
            if ok:
                _save_session(c)
                _qr_state.update(status="done")
            else:
                _qr_state.update(status="error", error=err)

    threading.Thread(target=_wait, daemon=True).start()
    return png, login_url


def get_connector():
    """Ready authenticated connector or None."""
    c = _load_session()
    if c and _session_valid(c):
        return c
    return None


def list_devices():
    """List of account devices (all homes, all servers, until first non-empty) —
    for manual scooter selection. [{name, model, did, mac, country}],
    mac may be None if cloud omits it."""
    c = get_connector()
    if not c:
        raise LtmkError("no active Mi Cloud session — log in via QR first")

    devices = []
    seen_did = set()
    for country in SERVERS:
        homes_resp = c.get_homes(country)
        if not homes_resp or homes_resp.get("code") not in (0, None):
            continue
        result = homes_resp.get("result") or {}
        homelist = result.get("homelist") or result.get("homeList") or []
        for home in homelist:
            home_id = home.get("id") or home.get("home_id")
            owner_id = home.get("uid", c.userId)
            if home_id is None:
                continue
            dev_resp = c.get_devices(country, home_id, owner_id)
            if not dev_resp or dev_resp.get("code") not in (0, None):
                continue
            dresult = dev_resp.get("result") or {}
            dev_list = dresult.get("device_info") or dresult.get("list") or dresult.get("devices") or []
            for d in dev_list:
                did = d.get("did")
                if not did or did in seen_did:
                    continue
                seen_did.add(did)
                mac = d.get("mac") or d.get("bt_mac") or d.get("bleMac") or d.get("bt_mac_str")
                devices.append({
                    "name": d.get("name") or d.get("model") or did,
                    "model": d.get("model"),
                    "did": did,
                    "mac": mac.upper() if isinstance(mac, str) else None,
                    "country": country,
                })
        if devices:
            break  # found home(s) on this server — do not probe remaining servers
    return devices


def _decrypt_ltmk(key_hex, pincode):
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    aes_key = hashlib.md5(pincode.encode("utf-8")).digest()
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(LTMK_ENCRYPT_IV))
    dec = cipher.decryptor()
    return dec.update(bytes.fromhex(key_hex)) + dec.finalize()


def fetch_ltmk(did, country="ru", pincode=None):
    """Fetches LTMK from cloud for specific did. If key on this account
    is encrypted with sharing PIN (encrypt_type==1) and pincode not provided — raises
    LtmkError('PIN_REQUIRED'); caller must prompt for PIN."""
    c = get_connector()
    if not c:
        raise LtmkError("no active Mi Cloud session — log in via QR first")

    url = c.get_api_url(country) + "/share/askbluetoothkey"
    params = {"data": json.dumps({"type": "own", "did": str(did), "keyid": 0})}
    resp = c.execute_api_call_encrypted(url, params)
    if not resp or resp.get("code") not in (0, None):
        raise LtmkError(f"cloud request rejected (code={resp.get('code') if resp else '?'})")
    result = resp.get("result") or {}
    key_hex = result.get("key")
    encrypt_type = result.get("encrypt_type", 0)
    if not key_hex:
        raise LtmkError("cloud returned no key")

    if encrypt_type == 0:
        ltmk = bytes.fromhex(key_hex)
    elif encrypt_type == 1:
        if not pincode:
            raise LtmkError("PIN_REQUIRED")
        ltmk = _decrypt_ltmk(key_hex, pincode)
    else:
        raise LtmkError(f"unknown encrypt_type={encrypt_type}")

    if len(ltmk) != 32:
        raise LtmkError(f"unexpected ltmk length: {len(ltmk)} bytes (expected 32)")
    return ltmk


def save_ltmk(mac, ltmk_bytes):
    safe = mac.upper().replace(":", "")
    path = os.path.join(SECRETS_DIR, f"ltmk_{safe}.hex")
    os.makedirs(SECRETS_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(ltmk_bytes.hex())
    return path


def load_saved_ltmk_hex_exact(mac):
    """Exact per-MAC file only (secrets/ltmk_<MAC>.hex) — does NOT fall back to
    secrets/ltmk.hex, unlike dreame_auth.ltmk_path_for_mac. For "show QR"
    this prevents displaying the default scooter key for a new MAC."""
    safe = mac.upper().replace(":", "")
    path = os.path.join(SECRETS_DIR, f"ltmk_{safe}.hex")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()
