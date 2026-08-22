#!/usr/bin/env python3
"""Диагностика: handshake, затем nvm_write БЕЗ ожидания ответа (гипотеза: молчит по
дизайну), пауза под эрейз, потом ОДИН чанк данных (128Б) — смотрим, придёт ли ACK 0x06.
Дальше (второй чанк, wr_info, dfu) не идёт — только один чанк для проверки гипотезы.

Запуск: python tools/mcu_chunk_sniff.py --port COM3 --fw firmware_ota/<mcu>.bin
"""
import argparse
import os
import struct
import sys
import time

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


def crc16_xmodem(data):
    crc = 0
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def read_until_byte(s, byte, timeout=3.0):
    end = time.time() + timeout
    while time.time() < end:
        d = s.read(1)
        if not d:
            continue
        if d[0] == byte:
            return d
    return None


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
    if not o.startswith(b"ok"):
        sys.exit(f"ABORT: rd_info не ok: {o[:20]!r}")
    log(f"rd_info: {o[:40]!r}")

    # --- ble_rand ---
    import random
    rand = bytes(random.randrange(256) for _ in range(16))
    s.reset_input_buffer()
    s.write(b"down ble_rand " + rand + b"\r")
    o = strip_push(read_for(s, 2.0))
    if not o.startswith(b"ok "):
        sys.exit(f"ABORT: ble_rand: {o[:20]!r}")
    if o[3:19] != bytes(sign_rand(bytearray(uid), bytearray(rand), fw, 0x24187, 0x24387)):
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
    log("mcu_key: принят")

    # --- nvm_write БЕЗ ожидания ответа (гипотеза: молчит по дизайну) ---
    s.reset_input_buffer()
    s.write(b"down nvm_write 00000000\r")
    log("nvm_write отправлен, НЕ жду ответа — пауза 5с под эрейз сектора...")
    time.sleep(5.0)
    leftover = strip_push(s.read(s.in_waiting or 1))
    if leftover:
        log(f"(за время паузы всё же пришло что-то небросовое: {leftover[:60]!r})")

    # --- один чанк данных (128Б), ждём ACK 0x06 ---
    chunk = fw[0:128]
    if len(chunk) < 128:
        chunk += b"\xFF" * (128 - len(chunk))
    N = (1).to_bytes(1, "big")
    frame = b"\x01" + N + bytes([0xFF - 1]) + chunk + struct.pack(">H", crc16_xmodem(chunk))
    s.reset_input_buffer()
    ack = None
    for attempt in range(3):
        s.write(frame)
        ack = read_until_byte(s, 0x06, timeout=2.0)
        if ack:
            break
        log(f"попытка {attempt+1}/3 — ACK не пришёл, повтор...")
    if ack:
        log(">>> ЕСТЬ ACK 0x06 на первый чанк! Гипотеза подтверждена: nvm_write молчит по дизайну.")
    else:
        log(">>> ACK на чанк НЕ пришёл. Гипотеза не подтверждена — проблема глубже, чем отсутствие ACK на nvm_write.")

    raw_dir = "uart_raw"
    os.makedirs(raw_dir, exist_ok=True)
    log("Диагностика завершена (только 1 чанк, дальше НЕ иду). Закрываю сессию.")
    s.close()


if __name__ == "__main__":
    main()
