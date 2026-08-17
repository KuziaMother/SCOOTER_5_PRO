#!/usr/bin/env python3
"""
Получение LTMK из Mi Cloud для новых профилей самокатов ("Мои самокаты").

Переиспользует QR-логин и RC4-шифрованные вызовы облака из tools/xct/token_extractor.py
(тем же кодом уже пользуется tools/fetch_firmware.py) — сессия в
secrets/micloud_session.json общая для обоих, повторный QR не нужен, пока
сессия валидна.

Схема получения ключа — docs/FACTS.md ("ltmk = ключ логина, происхождение и
ротация") и docs/dreame_dfu_protocol.md §6.5, проверено на реальном аккаунте
2026-08-16:

    POST /app/share/askbluetoothkey {type:own, did, keyid:0}
    -> result.{key, encrypt_type}
    encrypt_type==0: ltmk = hex_decode(key)
    encrypt_type==1 (задан PIN шаринга в Mi Home): ltmk = AES-128-CBC-NoPad(
        key=MD5(pincode), iv=<зашитый в APK>, ct=hex_decode(key))

Ключ никогда не логируется целиком и не возвращается по API без явного
запроса "reveal" — только длина/факт получения (§6 CLAUDE.md).

НЕ ПРОВЕРЕНО на реальном аккаунте (в отличие от самой схемы askbluetoothkey,
которая проверена — см. docs/dreame_dfu_protocol.md §6.5): разбор списка
устройств (get_homes/get_devices) списан по структуре, использованной в
tools/xct/token_extractor.py и аналогичных Xiaomi-cloud-tokens-extractor
проектах, но конкретные ключи ответа (homelist/device_info/mac) на этом
аккаунте вживую не сверялись — при расхождении см. list_devices() ниже,
там есть fallback на альтернативные имена полей и понятная ошибка.
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
sys.argv = ["qr"]  # token_extractor разбирает argv при импорте (argparse) — подменяем на время импорта
import token_extractor as tx  # noqa: E402
sys.argv = _saved_argv

SERVERS = ["ru", "de", "cn", "sg", "us", "i2", "tw", "in"]
LTMK_ENCRYPT_IV = bytes.fromhex("7aa4c68c590d4031b980d98b41023800")


class LtmkError(Exception):
    """Ожидаемая отказная ветка (не залогинен, нужен PIN, устройство не найдено)."""


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


# ---- состояние текущей QR-сессии логина (один пользователь webui, локально) ----
_state_lock = threading.Lock()
_qr_state = {"status": "idle"}  # idle|waiting|done|error


def qr_login_status():
    with _state_lock:
        return dict(_qr_state)


def has_session():
    return get_connector() is not None


def start_qr_login():
    """Возвращает (PNG QR-кода, login_url) сразу; сам логин идёт в фоновом
    потоке — ожидание скана (long-polling внутри token_extractor) может занять
    минуты. login_url — та же ссылка, что token_extractor.login_step_2()
    печатает как "Alternatively you can visit..." — если на этом же
    компьютере уже открыт браузер, залогиненный в аккаунт Xiaomi, переход по
    ней завершает вход сам, без сканирования телефоном вообще."""
    with _state_lock:
        if _qr_state.get("status") == "waiting":
            raise LtmkError("логин уже идёт")
        _qr_state.clear()
        _qr_state["status"] = "waiting"

    c = tx.QrCodeXiaomiCloudConnector()
    if not c.login_step_1():
        with _state_lock:
            _qr_state.update(status="error", error="не удалось начать логин (step1)")
        raise LtmkError("не удалось начать логин (step1)")

    img = c._session.get(c._qr_image_url)
    if img.status_code != 200:
        with _state_lock:
            _qr_state.update(status="error", error="не удалось получить QR-картинку")
        raise LtmkError("не удалось получить QR-картинку")
    png = img.content
    login_url = c._login_url

    def _wait():
        try:
            ok = c.login_step_3() and c.login_step_4()
        except Exception as e:
            ok = False
            err = f"{type(e).__name__}: {e}"
        else:
            err = "логин отклонён/истёк таймаут ожидания скана"
        with _state_lock:
            if ok:
                _save_session(c)
                _qr_state.update(status="done")
            else:
                _qr_state.update(status="error", error=err)

    threading.Thread(target=_wait, daemon=True).start()
    return png, login_url


def get_connector():
    """Готовый залогиненный коннектор или None."""
    c = _load_session()
    if c and _session_valid(c):
        return c
    return None


def list_devices():
    """Список устройств аккаунта (все дома, все сервера, до первого непустого) —
    для ручного выбора нужного самоката. [{name, model, did, mac, country}],
    mac может быть None если облако его не отдаёт под известными нам именами."""
    c = get_connector()
    if not c:
        raise LtmkError("нет активной сессии Mi Cloud — сначала войдите по QR")

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
            break  # нашли дом(а) на этом сервере — остальные сервера не пробуем
    return devices


def _decrypt_ltmk(key_hex, pincode):
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    aes_key = hashlib.md5(pincode.encode("utf-8")).digest()
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(LTMK_ENCRYPT_IV))
    dec = cipher.decryptor()
    return dec.update(bytes.fromhex(key_hex)) + dec.finalize()


def fetch_ltmk(did, country="ru", pincode=None):
    """Тянет LTMK из облака для конкретного did. Если ключ на этом аккаунте
    зашифрован PIN'ом шаринга (encrypt_type==1) и pincode не передан — бросает
    LtmkError('PIN_REQUIRED'), вызывающий код должен переспросить PIN."""
    c = get_connector()
    if not c:
        raise LtmkError("нет активной сессии Mi Cloud — сначала войдите по QR")

    url = c.get_api_url(country) + "/share/askbluetoothkey"
    params = {"data": json.dumps({"type": "own", "did": str(did), "keyid": 0})}
    resp = c.execute_api_call_encrypted(url, params)
    if not resp or resp.get("code") not in (0, None):
        raise LtmkError(f"облако отказало (code={resp.get('code') if resp else '?'})")
    result = resp.get("result") or {}
    key_hex = result.get("key")
    encrypt_type = result.get("encrypt_type", 0)
    if not key_hex:
        raise LtmkError("облако не вернуло key")

    if encrypt_type == 0:
        ltmk = bytes.fromhex(key_hex)
    elif encrypt_type == 1:
        if not pincode:
            raise LtmkError("PIN_REQUIRED")
        ltmk = _decrypt_ltmk(key_hex, pincode)
    else:
        raise LtmkError(f"неизвестный encrypt_type={encrypt_type}")

    if len(ltmk) != 32:
        raise LtmkError(f"неожиданная длина ltmk: {len(ltmk)} байт (ожидалось 32)")
    return ltmk


def save_ltmk(mac, ltmk_bytes):
    safe = mac.upper().replace(":", "")
    path = os.path.join(SECRETS_DIR, f"ltmk_{safe}.hex")
    os.makedirs(SECRETS_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(ltmk_bytes.hex())
    return path


def load_saved_ltmk_hex_exact(mac):
    """Только точный per-MAC файл (secrets/ltmk_<MAC>.hex) — НЕ падает на общий
    secrets/ltmk.hex, в отличие от dreame_auth.ltmk_path_for_mac. Для "показать
    QR" это важно: иначе для нового MAC без своего файла показался бы ключ
    ДРУГОГО (дефолтного) самоката — тихая и опасная путаница."""
    safe = mac.upper().replace(":", "")
    path = os.path.join(SECRETS_DIR, f"ltmk_{safe}.hex")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()
