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
import os
import sys
import threading
from datetime import datetime

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_WEBUI = os.path.dirname(os.path.abspath(__file__))
_PROBES = os.path.join(_ROOT, "probes")
for _p in (_ROOT, _WEBUI, _PROBES):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from flask import Flask, jsonify, render_template, request  # noqa: E402
import dreame_auth as da  # noqa: E402
import props  # noqa: E402
import ble_worker  # noqa: E402


app = Flask(__name__, template_folder="templates", static_folder="static")

RUNNING_STATUSES = {
    "connecting", "login", "ready", "baseline", "reading",
    "polling", "listening", "stopping",
}


def _ts():
    return datetime.now().strftime("%H:%M:%S")


class WebState:
    """Тред-безопасное состояние: BLE-поток пишет, HTTP-запросы читают."""

    def __init__(self):
        self.lock = threading.RLock()
        self.thread = None
        self.stop_event = threading.Event()
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
                self._add_event(f"{data.get('name', key)} = {data.get('text', '—')}{push_mark}")

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
                "history": list(self.history[-100:]),
                "events": list(self.events[-200:]),
                "counters": dict(self.counters),
                "last_update": self.last_update,
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


@app.get("/api/state")
def api_state():
    return jsonify(STATE.snapshot())


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


def main():
    port = int(os.environ.get("SCOOTER_WEB_PORT", os.environ.get("PUSH_WEB_PORT", "8321")))
    debug = os.environ.get("SCOOTER_WEB_DEBUG") == "1"
    print(f"[scooter-web] UI: http://127.0.0.1:{port}  (только localhost; read-only)")
    app.run(host="127.0.0.1", port=port, debug=debug, use_reloader=False, threaded=True)


if __name__ == "__main__":
    main()
