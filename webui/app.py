#!/usr/bin/env python3
"""
Модульный локальный web UI для Xiaomi Scooter 5 Pro (этап 1 — read-only dashboard).

Структура намеренно немамонолитная:
  webui/app.py          — Flask, HTTP API, тред-безопасное состояние;
  webui/ble_worker.py   — asyncio BLE-сессия (login/poll/push), только чтение;
  webui/props.py        — каталог свойств, единицы, enum'ы, маскировка секретов;
  webui/templates/*.html— разметка;
  webui/static/*        — CSS и JS отдельно.

Безопасность:
  * bind только 127.0.0.1;
  * по умолчанию read-only (set/запись в этом этапе нет);
  * paced-чтения по одному свойству, без batch/spam/sweep;
  * секреты (OOB_CODE/SN) не попадают в JSON/UI.

Запуск:
  python webui/app.py
  python probes/spec_listen_web.py   # тонкий compatibility launcher
"""
import asyncio
import base64
import io
import json
import os
import queue
import re
import sys
import threading
from datetime import datetime

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_WEBUI = os.path.dirname(os.path.abspath(__file__))
_CORE = os.path.join(_ROOT, "core")
_PROBES = os.path.join(_ROOT, "probes")
for _p in (_ROOT, _WEBUI, _CORE, _PROBES):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from flask import Flask, jsonify, render_template, request  # noqa: E402
import dreame_auth as da  # noqa: E402
import props  # noqa: E402
import ble_worker  # noqa: E402
import micloud_ltmk as ml  # noqa: E402
import firmware_ota as fo  # noqa: E402
import firmware_worker as fw  # noqa: E402


app = Flask(__name__, template_folder="templates", static_folder="static")

RUNNING_STATUSES = {
    "connecting", "login", "ready", "baseline", "reading",
    "polling", "listening", "stopping",
}

# ---- профили самокатов (§ несколько устройств) -----------------------------
# secrets/ целиком в .gitignore — файл со списком name+MAC (без ключей)
# уместно хранить там же, отдельного правила не нужно. LTMK для конкретного
# MAC резолвится отдельно, см. dreame_auth.ltmk_path_for_mac.
SCOOTERS_FILE = os.path.join(_ROOT, "secrets", "scooters.json")
MAC_RE = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")


def load_scooters():
    if os.path.exists(SCOOTERS_FILE):
        try:
            with open(SCOOTERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
        except (OSError, json.JSONDecodeError):
            pass
    return [{"name": "Scooter 5 Pro", "mac": da.MAC_DEFAULT}]


def save_scooters(lst):
    os.makedirs(os.path.dirname(SCOOTERS_FILE), exist_ok=True)
    with open(SCOOTERS_FILE, "w", encoding="utf-8") as f:
        json.dump(lst, f, ensure_ascii=False, indent=2)


def _ts():
    return datetime.now().strftime("%H:%M:%S")


class WebState:
    """Тред-безопасное состояние: BLE-поток пишет, HTTP-запросы читают."""

    def __init__(self):
        self.lock = threading.RLock()
        self.thread = None
        self.stop_event = threading.Event()
        self.set_queue = queue.Queue()
        self.write_enabled = False   # управление (SET) выключено по умолчанию (§5)
        self.reset()

    def reset(self):
        with self.lock:
            self.status = "idle"
            self.message = ""
            self.mode = None
            self.mac = da.MAC_DEFAULT
            self.properties = {}
            self.history = []
            self.events = []
            self.counters = {"pushes": 0, "rx": {}}
            self.error = None
            self.last_update = _ts()
            self._hid = 0
            self._eid = 0

    def _add_event(self, msg):
        if not msg:
            return
        self._eid += 1
        self.events.append({"id": self._eid, "ts": _ts(), "message": str(msg)})
        if len(self.events) > 300:
            del self.events[:len(self.events) - 300]

    def handle(self, evt):
        """Обработчик событий ble_worker (вызывается из BLE-потока)."""
        if not isinstance(evt, dict):
            return
        with self.lock:
            typ = evt.get("type")
            ts = _ts()

            if typ == "status":
                self.status = evt.get("status", "idle")
                self.message = evt.get("message", "")
                if self.status == "error":
                    self.error = self.message

            elif typ == "property":
                data = evt.get("data") or {}
                key = data.get("key") or f"{data.get('siid', '?')}.{data.get('piid', '?')}"
                data["ts"] = ts
                self.properties[key] = data
                push_mark = " [push]" if evt.get("push") else ""
                label = props.LABELS.get((data.get("siid"), data.get("piid"))) or data.get("name", key)
                self._add_event(f"{label} = {data.get('text', '—')}{push_mark}")

            elif typ == "round":
                self._hid += 1
                self.history.append({"id": self._hid, "ts": ts, "vals": evt.get("vals", {})})
                if len(self.history) > 300:
                    del self.history[:len(self.history) - 300]

            elif typ == "log":
                self._add_event(evt.get("message", ""))

            elif typ == "counters":
                self.counters = {
                    "pushes": evt.get("pushes", self.counters.get("pushes", 0)),
                    "rx": evt.get("rx", {}),
                }

            self.last_update = ts

    @property
    def running(self):
        with self.lock:
            return self.thread is not None and self.thread.is_alive()

    def snapshot(self):
        with self.lock:
            return {
                "status": self.status,
                "message": self.message,
                "mode": self.mode,
                "mac": self.mac,
                "error": self.error,
                "running": self.thread is not None and self.thread.is_alive(),
                "properties": dict(self.properties),
                "groups": [
                    {"id": g["id"], "title": g["title"], "props": [[s, p] for s, p in g["props"]]}
                    for g in props.GROUPS
                ],
                "names": {f"{s}.{p}": n for (s, p), n in props.NAMES.items()},
                "labels": {f"{s}.{p}": n for (s, p), n in props.LABELS.items()},
                "history": list(self.history[-100:]),
                "events": list(self.events[-200:]),
                "counters": dict(self.counters),
                "last_update": self.last_update,
                "write_enabled": self.write_enabled,
                "writable": [f"{s}.{p}" for (s, p) in props.WRITABLE],
                "writable_confirm": {
                    f"{s}.{p}": props.WRITABLE[(s, p)]["confirm"]
                    for (s, p) in props.WRITABLE if props.WRITABLE[(s, p)].get("confirm")
                },
                "writable_values": {
                    f"{s}.{p}": [
                        [v, props.ENUM_LABELS.get((s, p), {}).get(v, str(v))]
                        for v in props.WRITABLE[(s, p)]["values"]
                    ]
                    for (s, p) in props.WRITABLE if "values" in props.WRITABLE[(s, p)]
                },
            }


STATE = WebState()


def _worker(mac, mode, interval, static_interval):
    """BLE-сессия в отдельном потоке со своим event loop (bleak/WinRT)."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(ble_worker.run_session(
            mac=mac,
            mode=mode,
            interval=interval,
            static_interval=static_interval,
            on_event=STATE.handle,
            should_stop=STATE.stop_event.is_set,
            set_queue=STATE.set_queue,
        ))
    except Exception as e:
        STATE.handle({"type": "status", "status": "error",
                      "message": f"{type(e).__name__}: {e}"})
    finally:
        with STATE.lock:
            if STATE.status in RUNNING_STATUSES:
                STATE.status = "idle"
                STATE.message = ""
        loop.close()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/service")
def service_page():
    return render_template("service.html")


@app.get("/api/state")
def api_state():
    return jsonify(STATE.snapshot())


@app.get("/api/scooters")
def api_scooters():
    return jsonify(ok=True, scooters=load_scooters())


@app.post("/api/scooters")
def api_scooters_add():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    mac = str(data.get("mac", "")).strip().upper()
    if not name:
        return jsonify(ok=False, error="имя не может быть пустым"), 400
    if not MAC_RE.match(mac):
        return jsonify(ok=False, error="MAC должен быть в формате AA:BB:CC:DD:EE:FF"), 400

    scooters = load_scooters()
    if any(s["mac"].upper() == mac for s in scooters):
        return jsonify(ok=False, error="самокат с таким MAC уже сохранён"), 409
    scooters.append({"name": name, "mac": mac})
    save_scooters(scooters)
    return jsonify(ok=True, scooters=scooters)


def _scan_worker(timeout, result):
    """Скан в отдельном потоке со своим event loop (тот же паттерн, что _worker)."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result["devices"] = loop.run_until_complete(ble_worker.scan_devices(timeout))
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"
    finally:
        loop.close()


@app.post("/api/scooters/scan")
def api_scooters_scan():
    """Пассивный скан эфира (§4: только слушает рекламу, ничего не пишет на устройство)."""
    if STATE.running:
        return jsonify(ok=False, error="сессия уже запущена — сначала остановите"), 409

    data = request.get_json(silent=True) or {}
    try:
        timeout = float(data.get("timeout", 5))
    except (TypeError, ValueError):
        timeout = 5.0
    timeout = min(15.0, max(2.0, timeout))

    result = {}
    t = threading.Thread(target=_scan_worker, args=(timeout, result), daemon=True)
    t.start()
    t.join(timeout + 5.0)
    if t.is_alive():
        return jsonify(ok=False, error="скан завис (таймаут)"), 504
    if "error" in result:
        return jsonify(ok=False, error=result["error"]), 500
    return jsonify(ok=True, devices=result.get("devices", []))


@app.post("/api/scooters/delete")
def api_scooters_delete():
    data = request.get_json(silent=True) or {}
    mac = str(data.get("mac", "")).strip().upper()
    scooters = load_scooters()
    remaining = [s for s in scooters if s["mac"].upper() != mac]
    if len(remaining) == len(scooters):
        return jsonify(ok=False, error="не найден"), 404
    save_scooters(remaining)
    return jsonify(ok=True, scooters=remaining)


@app.get("/api/ltmk/status")
def api_ltmk_status():
    return jsonify(ok=True, logged_in=ml.has_session(), qr=ml.qr_login_status())


@app.post("/api/ltmk/qr_start")
def api_ltmk_qr_start():
    """Начинает QR-логин в Mi Cloud — сам вход идёт в фоновом потоке (ожидание
    скана может занять минуты), эндпоинт сразу отдаёт картинку QR-кода и
    альтернативную ссылку (если браузер на этом же компьютере уже залогинен
    в аккаунт Xiaomi, переход по ней завершает вход без сканирования)."""
    try:
        png, login_url = ml.start_qr_login()
    except ml.LtmkError as e:
        return jsonify(ok=False, error=str(e)), 409
    return jsonify(ok=True, qr_png_b64=base64.b64encode(png).decode("ascii"), login_url=login_url)


@app.get("/api/ltmk/qr_status")
def api_ltmk_qr_status():
    return jsonify(ok=True, **ml.qr_login_status())


@app.get("/api/ltmk/devices")
def api_ltmk_devices():
    try:
        devices = ml.list_devices()
    except ml.LtmkError as e:
        return jsonify(ok=False, error=str(e)), 409
    return jsonify(ok=True, devices=devices)


@app.post("/api/ltmk/fetch")
def api_ltmk_fetch():
    """Тянет LTMK из облака и сохраняет в secrets/ltmk_<MAC>.hex. Сам ключ
    НИКОГДА не возвращается в JSON — только факт успеха и длина (§6)."""
    data = request.get_json(silent=True) or {}
    did = str(data.get("did", "")).strip()
    country = str(data.get("country", "ru")).strip() or "ru"
    mac = str(data.get("mac", "")).strip().upper()
    pincode = data.get("pin") or None
    if not did or not MAC_RE.match(mac):
        return jsonify(ok=False, error="нужны did и корректный mac"), 400
    try:
        ltmk = ml.fetch_ltmk(did, country=country, pincode=pincode)
    except ml.LtmkError as e:
        if str(e) == "PIN_REQUIRED":
            return jsonify(ok=False, error="PIN_REQUIRED"), 428
        return jsonify(ok=False, error=str(e)), 502
    path = ml.save_ltmk(mac, ltmk)
    STATE.handle({"type": "log", "message":
                  f"LTMK получен и сохранён для {mac} ({os.path.relpath(path, _ROOT)}), {len(ltmk)} Б"})
    return jsonify(ok=True, mac=mac, length=len(ltmk))


@app.post("/api/ltmk/reveal_qr")
def api_ltmk_reveal_qr():
    """QR-картинка с LTMK для переноса на телефон (сканируется в PWA) — только
    по явному запросу пользователя, сам ключ не логируется и не пишется в
    STATE.events. Отдаёт ТОЛЬКО точный per-MAC файл, без fallback на общий
    secrets/ltmk.hex — иначе для нового устройства без своего файла можно
    было бы случайно показать чужой ключ."""
    data = request.get_json(silent=True) or {}
    mac = str(data.get("mac", "")).strip().upper()
    if not MAC_RE.match(mac):
        return jsonify(ok=False, error="неверный MAC"), 400
    hex_ltmk = ml.load_saved_ltmk_hex_exact(mac)
    if not hex_ltmk:
        return jsonify(ok=False, error="LTMK для этого MAC не найден локально — сначала получите его"), 404
    import qrcode
    img = qrcode.make(hex_ltmk)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return jsonify(ok=True, qr_png_b64=base64.b64encode(buf.getvalue()).decode("ascii"))


# соответствие типа записи в firmware_ota (как в облачном ответе) и target'а dreame_flasher
FW_TYPE_TO_TARGET = {"upd": "ble", "mcu": "mcu"}


@app.get("/api/firmware/installed")
def api_firmware_installed():
    """Последняя известная версия из телеметрии главной страницы (если там
    шёл поллинг) — своей BLE-сессии эта страница не открывает."""
    with STATE.lock:
        ble = STATE.properties.get("4.5")   # FIRMWARE_VERSION
        bms = STATE.properties.get("4.3")   # BMS_FIRMWARE_VERSION
    return jsonify(ok=True,
                   ble=(ble or {}).get("text"),
                   bms=(bms or {}).get("text"))


@app.post("/api/firmware/check")
def api_firmware_check():
    """Ищет did по MAC среди устройств аккаунта (та же сессия, что LTMK) и
    спрашивает Mi Cloud про последнюю версию. Помечает каждую запись,
    скачана ли она уже локально (по MD5)."""
    data = request.get_json(silent=True) or {}
    mac = str(data.get("mac", "")).strip().upper()
    if not MAC_RE.match(mac):
        return jsonify(ok=False, error="неверный MAC"), 400
    try:
        devices = ml.list_devices()
    except ml.LtmkError as e:
        return jsonify(ok=False, error=str(e)), 409
    dev = next((d for d in devices if d.get("mac") == mac), None)
    if not dev:
        return jsonify(ok=False, error="устройство с этим MAC не найдено в аккаунте Mi Cloud"), 404
    try:
        entries = fo.check_latest(dev["did"], country=dev["country"])
    except fo.FirmwareError as e:
        return jsonify(ok=False, error=str(e)), 502
    local = {it["md5"]: it for it in fo.local_firmware_list() if it.get("md5")}
    for e in entries:
        e["downloaded"] = bool(e.get("md5") and e["md5"].lower() in local)
        e["target"] = FW_TYPE_TO_TARGET.get(e["type"])
    return jsonify(ok=True, entries=entries)


@app.get("/api/firmware/local")
def api_firmware_local():
    items = fo.local_firmware_list()
    for it in items:
        it["target"] = FW_TYPE_TO_TARGET.get(it["type"])
    return jsonify(ok=True, items=items)


@app.post("/api/firmware/download")
def api_firmware_download():
    data = request.get_json(silent=True) or {}
    url = str(data.get("url", "")).strip()
    md5 = str(data.get("md5", "")).strip()
    fw_type = str(data.get("type", "")).strip()
    if not url or fw_type not in FW_TYPE_TO_TARGET:
        return jsonify(ok=False, error="нужны url и type (upd|mcu)"), 400
    try:
        item = fo.download_firmware(url, md5, fw_type)
    except fo.FirmwareError as e:
        return jsonify(ok=False, error=str(e)), 502
    item["target"] = FW_TYPE_TO_TARGET.get(item["type"])
    STATE.handle({"type": "log", "message": f"прошивка скачана: {item['filename']} ({item['size']} Б)"})
    return jsonify(ok=True, item=item)


@app.post("/api/firmware/flash/start")
def api_firmware_flash_start():
    """Заливка образа (без переключения) — commit=False. §5: необратимая
    часть (switchFirmware) в отдельном эндпоинте /commit, только по явному
    следующему запросу пользователя."""
    if STATE.running:
        return jsonify(ok=False, error="сначала остановите поллинг-сессию на главной странице "
                                        "— одно BLE-соединение на процесс"), 409
    data = request.get_json(silent=True) or {}
    mac = str(data.get("mac", "")).strip().upper()
    filename = str(data.get("filename", "")).strip()
    target = str(data.get("target", "")).strip()
    if not MAC_RE.match(mac) or not filename or target not in ("ble", "mcu"):
        return jsonify(ok=False, error="нужны mac, filename и target (ble|mcu)"), 400
    try:
        fw.start_flash(mac, filename, target, commit=False)
    except fw.FlashError as e:
        return jsonify(ok=False, error=str(e)), 409
    return jsonify(ok=True)


@app.post("/api/firmware/flash/commit")
def api_firmware_flash_commit():
    """switchFirmware — НЕОБРАТИМАЯ операция (риск кирпича). Резюм по CRC
    внутри dreame_flasher.flash сам проверит, что все фрагменты на месте,
    прежде чем реально переключать; если чего-то не хватает — сначала
    докачает. Вызывается только по явному подтверждению в UI (модалка)."""
    if STATE.running:
        return jsonify(ok=False, error="сначала остановите поллинг-сессию на главной странице "
                                        "— одно BLE-соединение на процесс"), 409
    data = request.get_json(silent=True) or {}
    mac = str(data.get("mac", "")).strip().upper()
    filename = str(data.get("filename", "")).strip()
    target = str(data.get("target", "")).strip()
    if not MAC_RE.match(mac) or not filename or target not in ("ble", "mcu"):
        return jsonify(ok=False, error="нужны mac, filename и target (ble|mcu)"), 400
    try:
        fw.start_flash(mac, filename, target, commit=True)
    except fw.FlashError as e:
        return jsonify(ok=False, error=str(e)), 409
    STATE.handle({"type": "log", "message": f"switchFirmware ({target}, {filename}) — запущено пользователем"})
    return jsonify(ok=True)


@app.get("/api/firmware/flash/status")
def api_firmware_flash_status():
    # без ok=True-обёртки: FLASH_STATE уже несёт своё поле "ok" (счётчик удачных
    # фрагментов) — jsonify(ok=True, **fw.status()) падал с "got multiple values
    # for keyword argument 'ok'" (500, не JSON). Фронтенд читает поля напрямую
    # (st.phase/st.ok/...), обёртка ему не нужна.
    return jsonify(fw.status())


@app.get("/api/firmware/flash/log")
def api_firmware_flash_log():
    """Постоянный лог заливок/переключений (logs/flash_log.jsonl) — переживает
    перезапуск сервера, в отличие от FLASH_STATE (только память)."""
    return jsonify(ok=True, entries=fw.read_log(limit=300))


@app.post("/api/start")
def api_start():
    if STATE.running:
        return jsonify(ok=False, error="уже запущено"), 409

    data = request.get_json(silent=True) or {}

    def param(name, dflt):
        if name in data and data[name] not in (None, ""):
            return data[name]
        return request.args.get(name, dflt)

    mode = str(param("mode", "poll")).lower()
    if mode not in {"once", "poll", "push"}:
        return jsonify(ok=False, error="mode должен быть once|poll|push"), 400

    try:
        interval = float(param("interval", 3))
    except (TypeError, ValueError):
        interval = 3.0
    interval = min(60.0, max(1.0, interval))

    try:
        static_interval = float(param("static_interval", 60))
    except (TypeError, ValueError):
        static_interval = 60.0
    static_interval = min(600.0, max(10.0, static_interval))

    mac = str(param("mac", da.MAC_DEFAULT))

    STATE.reset()
    with STATE.lock:
        STATE.mode = mode
        STATE.mac = mac
    STATE.stop_event.clear()
    STATE.handle({"type": "status", "status": "connecting", "message": "запуск…"})

    STATE.thread = threading.Thread(
        target=_worker, args=(mac, mode, interval, static_interval), daemon=True
    )
    STATE.thread.start()
    return jsonify(ok=True, status="started", mode=mode)


@app.post("/api/stop")
def api_stop():
    if not STATE.running:
        return jsonify(ok=False, error="не запущено"), 409
    STATE.stop_event.set()
    STATE.handle({"type": "status", "status": "stopping", "message": "остановка по запросу…"})
    return jsonify(ok=True, status="stopping")


@app.post("/api/write_mode")
def api_write_mode():
    data = request.get_json(silent=True) or {}
    enabled = bool(data.get("enabled"))
    with STATE.lock:
        STATE.write_enabled = enabled
    STATE.handle({"type": "log", "message": f"режим управления: {'ВКЛ' if enabled else 'выкл'}"})
    return jsonify(ok=True, write_enabled=enabled)


@app.post("/api/set")
def api_set():
    """SET одного разрешённого свойства (§5: только при включённом режиме управления)."""
    if not STATE.running:
        return jsonify(ok=False, error="сессия не запущена"), 409
    with STATE.lock:
        if not STATE.write_enabled:
            return jsonify(ok=False, error="режим управления выключен"), 403
        if STATE.mode != "poll":
            return jsonify(ok=False, error="управление доступно только в режиме poll"), 409

    data = request.get_json(silent=True) or {}
    key = str(data.get("key", ""))
    if not props.is_writable(key):
        return jsonify(ok=False, error="свойство не разрешено для записи"), 403
    try:
        siid, piid = (int(x) for x in key.split("."))
    except ValueError:
        return jsonify(ok=False, error="неверный key"), 400

    spec = props.WRITABLE[(siid, piid)]
    tcode = spec["type"]
    val = data.get("value")
    if tcode == 0:                                   # BOOL
        if val not in (0, 1, True, False):
            return jsonify(ok=False, error="value должен быть 0/1"), 400
        iv = 1 if val in (1, True) else 0
        value = bytes([iv])
    elif tcode == 1:                                 # UINT8 (enum-уровень)
        try:
            iv = int(val)
        except (TypeError, ValueError):
            return jsonify(ok=False, error="value должен быть числом"), 400
        allowed = spec.get("values")
        if allowed and iv not in allowed:
            return jsonify(ok=False, error=f"value должен быть один из {allowed}"), 400
        if not (0 <= iv <= 255):
            return jsonify(ok=False, error="UINT8 вне диапазона"), 400
        value = bytes([iv])
    else:
        return jsonify(ok=False, error="неподдерживаемый тип"), 400

    STATE.set_queue.put({"siid": siid, "piid": piid, "type": tcode, "value": value})
    STATE.handle({"type": "log", "message": f"SET {key} = {iv} — в очереди"})
    return jsonify(ok=True, queued=key)


def main():
    port = int(os.environ.get("SCOOTER_WEB_PORT", os.environ.get("PUSH_WEB_PORT", "8321")))
    debug = os.environ.get("SCOOTER_WEB_DEBUG") == "1"
    print(f"[scooter-web] UI: http://127.0.0.1:{port}  (только localhost; read-only)")
    app.run(host="127.0.0.1", port=port, debug=debug, use_reloader=False, threaded=True)


if __name__ == "__main__":
    main()
