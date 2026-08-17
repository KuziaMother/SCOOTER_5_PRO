#!/usr/bin/env python3
"""
BLE-заливка прошивки — оркестрация поверх dreame_flasher.py, с прогрессом для
веб-интерфейса. Держит собственный поток+event loop, как WebState._worker в
app.py — заливка не может идти одновременно с обычной поллинг-сессией (одно
BLE-соединение на процесс), взаимное исключение обеспечивает app.py ДО
вызова start_flash() (проверка STATE.running).

commit=True — тем же вызовом flash(): если фрагменты уже загружены (резюм по
CRC, см. dreame_flasher.flash), заливка пропускается и сразу уходит в
switchFirmware. Поэтому "Прошить" и "Переключить прошивку" в UI — это ДВА
РАЗНЫХ явных запуска (start_flash(commit=False), потом start_flash(commit=True)),
каждый — новое BLE-подключение; резюм делает повторную заливку дешёвой.

switchFirmware НЕОБРАТИМ (риск кирпича) — commit=True должен запускаться
только по явному подтверждению пользователя в UI (§5 CLAUDE.md).
"""
import asyncio
import json
import os
import threading
from datetime import datetime

import dreame_auth as da
import dreame_flasher as df

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIRMWARE_DIR = os.path.join(ROOT, "firmware_ota")
LOG_FILE = os.path.join(ROOT, "logs", "flash_log.jsonl")
_log_lock = threading.Lock()


def _log_event(**fields):
    """Дописывает одну строку JSONL — переживает перезапуск сервера (FLASH_STATE
    в памяти не переживает; см. обсуждение — раньше лога не было вовсе,
    из-за этого реальная попытка прошивки была потеряна после рестарта)."""
    fields["ts"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = json.dumps(fields, ensure_ascii=False)
    with _log_lock:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def read_log(limit=200):
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    out = []
    for line in lines[-limit:]:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


class FlashError(Exception):
    """Ожидаемая отказная ветка (уже идёт заливка, файл не найден и т.п.)."""


class FlashState:
    def __init__(self):
        self.lock = threading.RLock()
        self.thread = None
        self.reset()

    def reset(self):
        with self.lock:
            self.phase = "idle"  # idle|connecting|login|starting|uploading|committing|done|error
            self.message = ""
            self.mac = None
            self.target = None
            self.filename = None
            self.commit = False   # False = просто заливка, True = запущено с переключением (switchFirmware)
            self.index = 0
            self.total = 0
            self.ok = 0
            self.bad = 0
            self.speed_kbps = 0.0
            self.eta_sec = 0.0
            self.success = None
            self.error = None

    @property
    def running(self):
        with self.lock:
            return self.thread is not None and self.thread.is_alive()

    def update(self, **kw):
        with self.lock:
            for k, v in kw.items():
                setattr(self, k, v)

    def snapshot(self):
        with self.lock:
            return {
                "phase": self.phase, "message": self.message, "mac": self.mac, "target": self.target,
                "filename": self.filename, "commit": self.commit,
                "index": self.index, "total": self.total,
                "ok": self.ok, "bad": self.bad, "speed_kbps": round(self.speed_kbps, 2),
                "eta_sec": round(self.eta_sec, 0), "success": self.success,
                "error": self.error, "running": self.running,
            }


FLASH_STATE = FlashState()


def _update_and_log(**kw):
    """Единая точка обновления состояния — каждое изменение сразу и в
    памяти (для живого поллинга UI), и на диске (переживает рестарт)."""
    if kw.get("phase") == "error" and "error" not in kw:
        kw["error"] = kw.get("message")
    FLASH_STATE.update(**kw)
    st = FLASH_STATE.snapshot()
    _log_event(mac=st["mac"], target=st["target"], filename=st["filename"], commit=st["commit"],
               phase=st["phase"], message=st["message"],
               index=st["index"], total=st["total"], ok=st["ok"], bad=st["bad"],
               success=st["success"], error=st["error"])


def _on_progress(evt):
    _update_and_log(**evt)


async def _run(mac, path, target, commit):
    ltmk_path = da.ltmk_path_for_mac(mac)
    try:
        with open(ltmk_path, "r", encoding="utf-8") as f:
            ltmk = bytes.fromhex(f.read().strip())
    except Exception as e:
        _update_and_log(phase="error", success=False,
                        error=f"нет/не читается {ltmk_path}: {type(e).__name__}")
        return

    _update_and_log(phase="connecting", message="подключение к самокату…")
    t = da.Transport(mac)
    try:
        await df.login(t, ltmk)
    except Exception as e:
        _update_and_log(phase="error", success=False, error=f"логин не удался: {e}")
        try:
            await t.close()
        except Exception:
            pass
        return

    _update_and_log(phase="login", message="LOGIN OK")
    try:
        ok = await df.flash(t, path, target, commit=commit, on_progress=_on_progress)
        if FLASH_STATE.snapshot()["phase"] not in ("done", "error"):
            _update_and_log(phase="done", success=bool(ok))
    except Exception as e:
        _update_and_log(phase="error", success=False, error=f"{type(e).__name__}: {e}")
    finally:
        try:
            await t.close()
        except Exception:
            pass


def _thread_main(mac, path, target, commit):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(_run(mac, path, target, commit))
    finally:
        loop.close()


def start_flash(mac, filename, target, commit=False):
    if FLASH_STATE.running:
        raise FlashError("заливка уже идёт")
    if target not in ("ble", "mcu"):
        raise FlashError("target должен быть ble или mcu")
    path = os.path.join(FIRMWARE_DIR, filename)
    if not os.path.isfile(path):
        raise FlashError(f"файл не найден: {filename}")

    FLASH_STATE.reset()
    FLASH_STATE.update(mac=mac, target=target, filename=filename, commit=commit)
    _update_and_log(phase="starting", message="запуск…")
    FLASH_STATE.thread = threading.Thread(
        target=_thread_main, args=(mac, path, target, commit), daemon=True)
    FLASH_STATE.thread.start()


def status():
    return FLASH_STATE.snapshot()
