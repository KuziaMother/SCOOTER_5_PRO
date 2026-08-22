#!/usr/bin/env python3
"""Диагностика: полное рукопожатие (как mcu_uart_flash.py фазы 1-6), затем
nvm_write с СЫРЫМ (без strip_push) захватом ответа на 8 с. Только диагностика —
дальше nvm_write не идёт, чанки не шлются, флеш не трогается.

Запуск: python tools/mcu_nvmwrite_sniff.py --port COM3 --fw firmware_ota/<mcu>.bin
"""
import argparse
import os
import sys
import time
from datetime import datetime

import serial

sys.path.insert(0, "D:/tmp/bw-flasher")
from bwflasher.keygen import sign_rand  # noqa: E402


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def read_for(s, secs):
    buf = bytearray()
    end = time.time() + secs
    while time.time() < end:
        d = s.read(256)
        if d:
            buf += d
    return bytes(buf)


def strip_push(d):
    out = bytearray()
    i = 0
    n = len(d)
    while i < n:
        if i + 5 <= n and d[i] == 0x61 and d[i + 2] <= 200:
            ln = d[i + 2]
            e = i + 4 + ln + 1
            if e <= n and d[e - 1] == 0x9E:
                i = e
                continue
        out.append(d[i])
        i += 1
    return bytes(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM3")
    ap.add_argument("--fw", required=True)
    a = ap.parse_args()

    fw = open(a.fw, "rb").read()
    log(f"образ: {a.fw} ({len(fw)} Б)")

    s = serial.Serial(a.port, 19200, timeout=0.3)
    time.sleep(0.3)
    s.reset_input_buffer()

    # --- UID ---
    uid = None
    for _ in range(3):
        s.reset_input_buffer()
        s.write(b"down get_ver\r")
        time.sleep(0.4)
        s.write(bytes.fromhex("53 2a 7d ac"))
        d = read_for(s, 2.0)
        i = d.find(b"\x64\x2a\x10")
        if i >= 0 and i + 19 <= len(d):
            uid = d[i + 3:i + 3 + 16]
            break
    if uid is None:
        sys.exit("ABORT: UID не получен")
    log(f"UID: {uid.hex()}")

    # --- rd_info ---
    s.reset_input_buffer()
    s.write(b"down rd_info\r\x00\x00\x00")
    o = strip_push(read_for(s, 2.0))
    log(f"rd_info: {o[:40]!r}")
    if not o.startswith(b"ok"):
        sys.exit("ABORT: rd_info не ok")

    # --- ble_rand ---
    import random
    rand = bytes(random.randrange(256) for _ in range(16))
    s.reset_input_buffer()
    s.write(b"down ble_rand " + rand + b"\r")
    o = strip_push(read_for(s, 2.0))
    if not o.startswith(b"ok "):
        sys.exit(f"ABORT: ble_rand: {o[:20]!r}")
    mcu_key_resp = o[3:19]
    local_key = bytes(sign_rand(bytearray(uid), bytearray(rand), fw, 0x24187, 0x24387))
    if mcu_key_resp != local_key:
        sys.exit("ABORT: sign_rand не совпал")
    log("ble_rand: крипто совпала")

    # --- mcu_rand ---
    s.reset_input_buffer()
    s.write(b"down mcu_rand\r")
    o = strip_push(read_for(s, 2.0))
    if not o.startswith(b"ok "):
        sys.exit(f"ABORT: mcu_rand: {o[:20]!r}")
    mcu_rand = o[3:19]
    log(f"mcu_rand: {mcu_rand.hex()}")

    # --- mcu_key ---
    key = bytes(sign_rand(bytearray(uid), bytearray(mcu_rand), fw, 0x24187, 0x24387))
    s.reset_input_buffer()
    s.write(b"down mcu_key " + key + b"\r")
    o = strip_push(read_for(s, 2.0))
    if not o.startswith(b"ok"):
        sys.exit(f"ABORT: mcu_key отклонён: {o[:20]!r}")
    log("mcu_key: принят — держим сессию, готовлюсь к сырому захвату nvm_write")

    # --- ДИАГНОСТИКА: nvm_write, сырой захват до 25 с, ОДНА отправка, без повтора ---
    # (повтор команды рестартит erase сектора на MCU — не шлём второй раз, просто ждём дольше)
    s.reset_input_buffer()
    t0 = time.time()
    cmd = b"down nvm_write 00000000\r"
    s.write(cmd)
    raw = bytearray()
    found = False
    while time.time() - t0 < 25.0:
        raw += read_for(s, 1.0)
        stripped_live = strip_push(bytes(raw))
        if stripped_live.startswith(b"ok") or b"k\r" in stripped_live:
            found = True
            break
    raw = bytes(raw)
    el = time.time() - t0
    raw_dir = "uart_raw"
    os.makedirs(raw_dir, exist_ok=True)
    fname = os.path.join(raw_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_nvmwrite_raw.bin")
    with open(fname, "wb") as f:
        f.write(raw)
    log(f"nvm_write отправлен ({cmd!r}), ждал {el:.1f} с, получил {len(raw)} Б -> {fname}")
    log(f"RAW (первые 200Б): {raw[:200].hex(' ')}")
    stripped = strip_push(raw)
    log(f"после strip_push осталось {len(stripped)} Б: {stripped[:100]!r}")
    if found:
        log(">>> ЕСТЬ ответ на nvm_write, диагностика окончена успешно.")
    else:
        log(">>> ответа на nvm_write НЕ получено за 25 с одной отправки.")

    log("Диагностика завершена. Дальше (чанки/dfu) НЕ отправляю — сессию закрываю.")
    s.close()


if __name__ == "__main__":
    main()
