#!/usr/bin/env python3
"""Живая телеметрия MCU через USB-TTL (линия UART4, push-кадры 61 …).

Проверено живым трафиком 2026-08-21 (docs/FACTS.md «Push 0x31»):
  61 30 0A P0..P9 CHK 9E   — статус-пуш (режимы/флаги, §34 REPORT)
  61 31 09 P0..P8 CHK 9E   — баттари-пуш:
      P1 = SoC% (@0x306), P2P3 = сырой замер (@0x308, high,low),
      P4P5 = флаг (@0x30a), P6..P8 = температура °C (@0x30c, low,high,low)
  CHK = Σ(все предшествующие байты кадра) & 0xFF; 0x9E = ~0x61.

Линия delivers bursts ~4 КБ с паузами — скрипт молчит, пока нет данных.

Использование:
  python tools/uart_telemetry.py --port COM3 [--baud 19200] [--jsonl out.jsonl]
"""
import argparse
import json
import sys
import time

import serial


def parse_frames(buf):
    """Генератор кадров (sub, payload, ok_chk) из буфера; возвращает consumed."""
    i = 0
    frames = []
    while i + 5 <= len(buf):
        if buf[i] == 0x61 and buf[i + 2] <= 200:
            ln = buf[i + 2]
            e = i + 4 + ln + 1
            if e <= len(buf) and buf[e - 1] == 0x9E:
                chk = sum(buf[i:e - 2]) & 0xFF
                frames.append((buf[i + 1], bytes(buf[i + 3:i + 3 + ln]),
                               chk == buf[e - 2]))
                i = e
                continue
        i += 1
    return frames, i


def decode(sub, p):
    if sub == 0x31 and len(p) >= 9:
        return {
            "soc_pct": p[1],
            "raw_batt": (p[2] << 8) | p[3],   # u16, high,low на проводе
            "flag": (p[4] << 8) | p[5],       # u16, high,low; бит15 переключается
            "temp_c": (p[7] << 8) | p[6],     # на проводе low,high,low
        }
    if sub == 0x30 and len(p) >= 10:
        return {
            "status0": p[0], "status1": p[1], "bits": p[2],
            "mode": p[5], "payload": p.hex(),
        }
    return {"payload": p.hex()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM3")
    ap.add_argument("--baud", type=int, default=19200)
    ap.add_argument("--jsonl", default="", help="дублировать кадры в JSONL-файл")
    a = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    s = serial.Serial(a.port, a.baud, timeout=0.5)
    jf = open(a.jsonl, "a", encoding="utf-8") if a.jsonl else None
    print(f"телеметрия: {a.port} @ {a.baud} — жду bursts… (Ctrl-C для выхода)", flush=True)

    last = {}
    try:
        while True:
            d = s.read(4096)
            if not d:
                continue
            frames, _ = parse_frames(d)
            for sub, p, ok in frames:
                dec = decode(sub, p)
                rec = {"t": round(time.time(), 2), "sub": f"0x{sub:02x}",
                       "chk_ok": ok, **dec}
                if jf:
                    jf.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    jf.flush()
                # печатаем только реальные изменения (джиттер raw_batt гасим)
                key = dict(dec)
                if sub == 0x31:
                    key["raw_batt"] //= 8
                    key.pop("flag", None)
                now = time.time()
                if key != last.get((sub, "k")) or now - last.get((sub, "t"), 0) > 5:
                    last[(sub, "k")] = key
                    last[(sub, "t")] = now
                    print(f"  [{time.strftime('%H:%M:%S')}] 0x{sub:02x} "
                          f"chk={'ok' if ok else 'ERR'} {dec}", flush=True)
    except KeyboardInterrupt:
        pass
    finally:
        s.close()
        if jf:
            jf.close()


if __name__ == "__main__":
    main()
