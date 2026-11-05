#!/usr/bin/env python3
"""
Modular local web UI for Xiaomi Scooter 5 Pro (stage 1 — read-only dashboard).

Intentionally non-monolithic structure:
  webui/app.py          — Flask, HTTP API, thread-safe state;
  webui/ble_worker.py   — asyncio BLE session (login/poll/push), read-only;
  webui/props.py        — properties catalog, units, enums, secret masking;
  webui/templates/*.html— markup;
  webui/static/*        — CSS and JS separate.

Security:
  * bind to 127.0.0.1 only;
  * read-only by default (no set/write at this stage);
  * paced reads property-by-property, no batch/spam/sweep;
  * secrets (OOB_CODE/SN) excluded from JSON/UI.

Launch:
  python webui/app.py
  python probes/spec_listen_web.py   # thin compatibility launcher
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

# ---- scooter profiles (§ multiple devices) -----------------------------------
# secrets/ is entirely gitignored — name+MAC list (without keys) is stored
# there as well. LTMK for specific MAC is resolved separately, see
# dreame_auth.ltmk_path_for_mac.
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
    """Thread-safe state: BLE worker thread writes, HTTP requests read."""

    def __init__(self):
        self.lock = threading.RLock()
        self.thread = None
        self.stop_event = threading.Event()
        self.set_queue = queue.Queue()
        self.write_enabled = False   # control mode (SET) disabled by default (§5)
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
        """ble_worker event handler (invoked from BLE thread)."""
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
                "groups_en": [
                    {"id": g["id"], "title": g["title"], "props": [[s, p] for s, p in g["props"]]}
                    for g in props.GROUPS_EN
                ],
                "names": {f"{s}.{p}": n for (s, p), n in props.NAMES.items()},
                "labels": {f"{s}.{p}": n for (s, p), n in props.LABELS.items()},
                "labels_en": {f"{s}.{p}": n for (s, p), n in props.LABELS_EN.items()},
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
                "writable_confirm_en": {
                    f"{s}.{p}": props.WRITABLE_CONFIRM_EN.get((s, p), props.WRITABLE[(s, p)].get("confirm", ""))
                    for (s, p) in props.WRITABLE if props.WRITABLE[(s, p)].get("confirm")
                },
                "writable_values": {
                    f"{s}.{p}": [
                        [v, props.ENUM_LABELS.get((s, p), {}).get(v, str(v))]
                        for v in props.WRITABLE[(s, p)]["values"]
                    ]
                    for (s, p) in props.WRITABLE if "values" in props.WRITABLE[(s, p)]
                },
                "writable_values_en": {
                    f"{s}.{p}": [
                        [v, props.ENUM_LABELS_EN.get((s, p), {}).get(v, str(v))]
                        for v in props.WRITABLE[(s, p)]["values"]
                    ]
                    for (s, p) in props.WRITABLE if "values" in props.WRITABLE[(s, p)]
                },
            }


STATE = WebState()


def _worker(mac, mode, interval, static_interval):
    """BLE session in separate thread with own event loop (bleak/WinRT)."""
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
        return jsonify(ok=False, error="name cannot be empty"), 400
    if not MAC_RE.match(mac):
        return jsonify(ok=False, error="MAC must be in format AA:BB:CC:DD:EE:FF"), 400

    scooters = load_scooters()
    if any(s["mac"].upper() == mac for s in scooters):
        return jsonify(ok=False, error="scooter with this MAC already exists"), 409
    scooters.append({"name": name, "mac": mac})
    save_scooters(scooters)
    return jsonify(ok=True, scooters=scooters)


def _scan_worker(timeout, result):
    """Scan in separate thread with own event loop (same pattern as _worker)."""
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
    """Passive air scan (§4: listens to advertisements only, writes nothing to device)."""
    if STATE.running:
        return jsonify(ok=False, error="session already running — stop it first"), 409

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
        return jsonify(ok=False, error="scan timed out"), 504
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
        return jsonify(ok=False, error="not found"), 404
    save_scooters(remaining)
    return jsonify(ok=True, scooters=remaining)


@app.get("/api/ltmk/status")
def api_ltmk_status():
    return jsonify(ok=True, logged_in=ml.has_session(), qr=ml.qr_login_status())


@app.post("/api/ltmk/qr_start")
def api_ltmk_qr_start():
    """Starts QR login into Mi Cloud — login proceeds in background thread (waiting
    for scan may take minutes), endpoint immediately returns QR code image and
    alternative URL (if browser on this machine is already logged into Xiaomi
    account, navigating to it completes login without scanning)."""
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
    """Fetches LTMK from cloud and saves to secrets/ltmk_<MAC>.hex. The key itself
    is NEVER returned in JSON — only success status and key length (§6)."""
    data = request.get_json(silent=True) or {}
    did = str(data.get("did", "")).strip()
    country = str(data.get("country", "ru")).strip() or "ru"
    mac = str(data.get("mac", "")).strip().upper()
    pincode = data.get("pin") or None
    if not did or not MAC_RE.match(mac):
        return jsonify(ok=False, error="did and valid mac required"), 400
    try:
        ltmk = ml.fetch_ltmk(did, country=country, pincode=pincode)
    except ml.LtmkError as e:
        if str(e) == "PIN_REQUIRED":
            return jsonify(ok=False, error="PIN_REQUIRED"), 428
        return jsonify(ok=False, error=str(e)), 502
    path = ml.save_ltmk(mac, ltmk)
    STATE.handle({"type": "log", "message":
                  f"LTMK received and saved for {mac} ({os.path.relpath(path, _ROOT)}), {len(ltmk)} B"})
    return jsonify(ok=True, mac=mac, length=len(ltmk))


@app.post("/api/ltmk/reveal_qr")
def api_ltmk_reveal_qr():
    """QR image with LTMK for transfer to phone (scanned in PWA) — only
    on explicit user request; key itself is never logged or written to
    STATE.events. Returns EXACT per-MAC file only, without fallback to
    secrets/ltmk.hex to avoid exposing another device key."""
    data = request.get_json(silent=True) or {}
    mac = str(data.get("mac", "")).strip().upper()
    if not MAC_RE.match(mac):
        return jsonify(ok=False, error="invalid MAC"), 400
    hex_ltmk = ml.load_saved_ltmk_hex_exact(mac)
    if not hex_ltmk:
        return jsonify(ok=False, error="LTMK for this MAC not found locally — fetch it first"), 404
    import qrcode
    img = qrcode.make(hex_ltmk)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return jsonify(ok=True, qr_png_b64=base64.b64encode(buf.getvalue()).decode("ascii"))


# mapping between record type in firmware_ota (cloud response) and dreame_flasher target
FW_TYPE_TO_TARGET = {"upd": "ble", "mcu": "mcu"}


@app.get("/api/firmware/installed")
def api_firmware_installed():
    """Last known version from main dashboard telemetry (if polling was active)
    — this page does not open a dedicated BLE session."""
    with STATE.lock:
        ble = STATE.properties.get("4.5")   # FIRMWARE_VERSION
        bms = STATE.properties.get("4.3")   # BMS_FIRMWARE_VERSION
    return jsonify(ok=True,
                   ble=(ble or {}).get("text"),
                   bms=(bms or {}).get("text"))


@app.post("/api/firmware/check")
def api_firmware_check():
    """Finds did by MAC among account devices (same session as LTMK) and
    queries Mi Cloud for latest version. Flags each entry whether it is
    already downloaded locally (by MD5)."""
    data = request.get_json(silent=True) or {}
    mac = str(data.get("mac", "")).strip().upper()
    if not MAC_RE.match(mac):
        return jsonify(ok=False, error="invalid MAC"), 400
    try:
        devices = ml.list_devices()
    except ml.LtmkError as e:
        return jsonify(ok=False, error=str(e)), 409
    dev = next((d for d in devices if d.get("mac") == mac), None)
    if not dev:
        return jsonify(ok=False, error="device with this MAC not found in Mi Cloud account"), 404
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
        return jsonify(ok=False, error="url and type (upd|mcu) required"), 400
    try:
        item = fo.download_firmware(url, md5, fw_type)
    except fo.FirmwareError as e:
        return jsonify(ok=False, error=str(e)), 502
    item["target"] = FW_TYPE_TO_TARGET.get(item["type"])
    STATE.handle({"type": "log", "message": f"firmware downloaded: {item['filename']} ({item['size']} B)"})
    return jsonify(ok=True, item=item)


@app.post("/api/firmware/flash/start")
def api_firmware_flash_start():
    """Flashing firmware image (without switch) — commit=False. §5: irreversible
    step (switchFirmware) is in dedicated /commit endpoint, executed only
    upon explicit subsequent user request."""
    if STATE.running:
        return jsonify(ok=False, error="stop polling session on main page first "
                                        "— one BLE connection per process"), 409
    data = request.get_json(silent=True) or {}
    mac = str(data.get("mac", "")).strip().upper()
    filename = str(data.get("filename", "")).strip()
    target = str(data.get("target", "")).strip()
    if not MAC_RE.match(mac) or not filename or target not in ("ble", "mcu"):
        return jsonify(ok=False, error="mac, filename and target (ble|mcu) required"), 400
    try:
        fw.start_flash(mac, filename, target, commit=False)
    except fw.FlashError as e:
        return jsonify(ok=False, error=str(e)), 409
    return jsonify(ok=True)


@app.post("/api/firmware/flash/commit")
def api_firmware_flash_commit():
    """switchFirmware is an IRREVERSIBLE operation (brick risk). CRC resume
    inside dreame_flasher.flash verifies all fragments are intact before
    switching; if anything is missing — downloads remaining fragments first.
    Called only upon explicit user confirmation in UI (modal)."""
    if STATE.running:
        return jsonify(ok=False, error="stop polling session on main page first "
                                        "— one BLE connection per process"), 409
    data = request.get_json(silent=True) or {}
    mac = str(data.get("mac", "")).strip().upper()
    filename = str(data.get("filename", "")).strip()
    target = str(data.get("target", "")).strip()
    if not MAC_RE.match(mac) or not filename or target not in ("ble", "mcu"):
        return jsonify(ok=False, error="mac, filename and target (ble|mcu) required"), 400
    try:
        fw.start_flash(mac, filename, target, commit=True)
    except fw.FlashError as e:
        return jsonify(ok=False, error=str(e)), 409
    STATE.handle({"type": "log", "message": f"switchFirmware ({target}, {filename}) — initiated by user"})
    return jsonify(ok=True)


@app.get("/api/firmware/flash/status")
def api_firmware_flash_status():
    # no ok=True wrapper: FLASH_STATE already carries its own "ok" field (count of successful
    # fragments) — jsonify(ok=True, **fw.status()) crashed with "got multiple values
    # for keyword argument 'ok'" (500, not JSON). Frontend reads fields directly
    # (st.phase/st.ok/...), no wrapper required.
    return jsonify(fw.status())


@app.get("/api/firmware/flash/log")
def api_firmware_flash_log():
    """Persistent log of flashes/switches (logs/flash_log.jsonl) — survives
    server restarts, unlike FLASH_STATE (memory only)."""
    return jsonify(ok=True, entries=fw.read_log(limit=300))


@app.post("/api/start")
def api_start():
    if STATE.running:
        return jsonify(ok=False, error="already running"), 409

    data = request.get_json(silent=True) or {}

    def param(name, dflt):
        if name in data and data[name] not in (None, ""):
            return data[name]
        return request.args.get(name, dflt)

    mode = str(param("mode", "poll")).lower()
    if mode not in {"once", "poll", "push"}:
        return jsonify(ok=False, error="mode must be once|poll|push"), 400

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
    STATE.handle({"type": "status", "status": "connecting", "message": "starting…"})

    STATE.thread = threading.Thread(
        target=_worker, args=(mac, mode, interval, static_interval), daemon=True
    )
    STATE.thread.start()
    return jsonify(ok=True, status="started", mode=mode)


@app.post("/api/stop")
def api_stop():
    if not STATE.running:
        return jsonify(ok=False, error="not running"), 409
    STATE.stop_event.set()
    STATE.handle({"type": "status", "status": "stopping", "message": "stopping on request…"})
    return jsonify(ok=True, status="stopping")


@app.post("/api/write_mode")
def api_write_mode():
    data = request.get_json(silent=True) or {}
    enabled = bool(data.get("enabled"))
    with STATE.lock:
        STATE.write_enabled = enabled
    STATE.handle({"type": "log", "message": f"control mode: {'ON' if enabled else 'OFF'}"})
    return jsonify(ok=True, write_enabled=enabled)


@app.post("/api/set")
def api_set():
    """SET single allowed property (§5: only when control mode is active)."""
    if not STATE.running:
        return jsonify(ok=False, error="session not running"), 409
    with STATE.lock:
        if not STATE.write_enabled:
            return jsonify(ok=False, error="control mode is disabled"), 403
        if STATE.mode != "poll":
            return jsonify(ok=False, error="control is only available in poll mode"), 409

    data = request.get_json(silent=True) or {}
    key = str(data.get("key", ""))
    if not props.is_writable(key):
        return jsonify(ok=False, error="property is not writable"), 403
    try:
        siid, piid = (int(x) for x in key.split("."))
    except ValueError:
        return jsonify(ok=False, error="invalid key"), 400

    spec = props.WRITABLE[(siid, piid)]
    tcode = spec["type"]
    val = data.get("value")
    if tcode == 0:                                   # BOOL
        if val not in (0, 1, True, False):
            return jsonify(ok=False, error="value must be 0/1"), 400
        iv = 1 if val in (1, True) else 0
        value = bytes([iv])
    elif tcode == 1:                                 # UINT8 (enum level)
        try:
            iv = int(val)
        except (TypeError, ValueError):
            return jsonify(ok=False, error="value must be a number"), 400
        allowed = spec.get("values")
        if allowed and iv not in allowed:
            return jsonify(ok=False, error=f"value must be one of {allowed}"), 400
        if not (0 <= iv <= 255):
            return jsonify(ok=False, error="UINT8 out of range"), 400
        value = bytes([iv])
    else:
        return jsonify(ok=False, error="unsupported type"), 400

    STATE.set_queue.put({"siid": siid, "piid": piid, "type": tcode, "value": value})
    STATE.handle({"type": "log", "message": f"SET {key} = {iv} — enqueued"})
    return jsonify(ok=True, queued=key)


def main():
    port = int(os.environ.get("SCOOTER_WEB_PORT", os.environ.get("PUSH_WEB_PORT", "8321")))
    debug = os.environ.get("SCOOTER_WEB_DEBUG") == "1"
    print(f"[scooter-web] UI: http://127.0.0.1:{port}  (localhost only; read-only)")
    app.run(host="127.0.0.1", port=port, debug=debug, use_reloader=False, threaded=True)


if __name__ == "__main__":
    main()
