#!/usr/bin/env python
"""Фоновый логгер активности UART-линии (USB-TTL): «были ли данные и когда».

Циклически слушает порт по всем бод-рейтам (по --slot с на каждый) и пишет в
JSONL-лог: HEARTBEAT (логгер жив) и DATA (пойманы байты: время, бод, hex).

Запуск (в фоне):  python tools/uart_logger.py --port COM5          # лог: logs/uart_activity.log
Остановка:        попросить ассистента убить процесс или Ctrl-C в его терминале.
Анализ:           python tools/uart_logger.py --show logs/uart_activity.log
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUT = os.path.join(ROOT, "logs", "uart_activity.log")

try:
    import serial
except ImportError:
    sys.exit("нужен pyserial: pip install pyserial")

BAUDS = [115200, 9600, 19200, 38400, 57600, 230400, 460800, 921600, 4800, 2400]


def beep():
    try:
        import winsound
        winsound.Beep(1200, 250)
    except Exception:
        print("\a", end="")
        sys.stdout.flush()


def ts():
    return datetime.now().isoformat(timespec="milliseconds")


def run(port, out_path, slot, minutes, sound=True):
    global beep
    if not sound:
        beep = lambda: None
    raw_dir = os.path.join(ROOT, "uart_raw")
    os.makedirs(raw_dir, exist_ok=True)
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    log = open(out_path, "a", encoding="utf-8")

    def w(obj):
        log.write(json.dumps(obj, ensure_ascii=False) + "\n")
        log.flush()

    w({"t": ts(), "ev": "START", "port": port, "bauds": BAUDS, "slot_s": slot})
    end = time.time() + minutes * 60 if minutes else float("inf")
    try:
        s = serial.Serial(port, BAUDS[0], timeout=1)
    except Exception as e:
        w({"t": ts(), "ev": "ERROR", "msg": f"порт не открылся: {e}"})
        return
    while time.time() < end:
        for b in BAUDS:
            if time.time() >= end:
                break
            s.baudrate = b
            time.sleep(0.2)
            s.reset_input_buffer()
            t0 = time.time()
            buf = bytearray()
            while time.time() - t0 < slot:
                buf += s.read(4096)
            if buf:
                beep()
                raw_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_b{b}.bin"
                with open(os.path.join(raw_dir, raw_name), "wb") as rf:
                    rf.write(bytes(buf))
                o = {"t": ts(), "ev": "DATA", "baud": b, "n": len(buf),
                     "raw": raw_name, "hex": bytes(buf[:64]).hex(" ")}
                w(o)
                print(f"*** ДАННЫЕ {o['t']}  baud={b}  n={len(buf)}  {o['hex'][:48]}  -> {raw_name}", flush=True)
        w({"t": ts(), "ev": "HEARTBEAT"})
        print(f"... {ts()}", flush=True)
    s.close()
    w({"t": ts(), "ev": "STOP"})
    log.close()


def show(out_path):
    data_lines = hb = 0
    first_data = last_data = None
    with open(out_path, encoding="utf-8") as f:
        for line in f:
            try:
                o = json.loads(line)
            except ValueError:
                continue
            ev = o.get("ev")
            if ev == "HEARTBEAT":
                hb += 1
            elif ev == "DATA":
                data_lines += 1
                first_data = first_data or o
                last_data = o
    print(f"лог: {out_path}")
    print(f"heartbeats: {hb}, событий DATA: {data_lines}")
    if first_data:
        print(f"первое DATA : {first_data['t']}  baud={first_data['baud']} n={first_data['n']}")
        print(f"  {first_data['hex'][:80]}")
        if last_data is not first_data:
            print(f"последнее DATA: {last_data['t']}  baud={last_data['baud']} n={last_data['n']}")
    else:
        print("данных НЕ БЫЛО (линия молчала всё время логирования)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM5")
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--slot", type=float, default=3.0, help="секунд на бод-рейт")
    ap.add_argument("--minutes", type=float, default=0, help="авто-стоп через N мин (0 = пока не убьют)")
    ap.add_argument("--no-sound", action="store_true", help="без звукового сигнала")
    ap.add_argument("--baud", type=int, default=0, help="один бод-рейт вместо sweep (напр. 19200)")
    ap.add_argument("--show", metavar="LOG", help="показать сводку по лог-файлу и выйти")
    a = ap.parse_args()
    if a.show:
        show(a.show)
    else:
        if a.baud:
            BAUDS = [a.baud]
        run(a.port, a.out, a.slot, a.minutes, sound=not a.no_sound)
