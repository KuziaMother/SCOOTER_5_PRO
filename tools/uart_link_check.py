#!/usr/bin/env python3
"""Проверка связи UART-линии: подключены ли RX и TX. Быстрый цикл ~4 с.

RX-статус:  читаем линию 1.5 с — есть байты => RX подключён (поток непрерывный,
            ~218 Б/с; read(1) показывает, что «чанки по 4 КБ» — артефакт read(4096)).
TX-статус:  две проверки:
  1) wiring: 2 с burst DE AD параллельно с чтением — ловим только ОШИБКИ проводки:
       - эхо DE AD в RX      => TX замкнут с RX (loopback)
       - повреждённые кадры  => TX на шине TX MCU (конфликт)
     Правильная проводка (TX → RX-пин MCU) здесь НЕ видна — это нормально.
  2) функциональная: раз в 5 циклов шлём `down get_ver\r` и `53 2A 7D AC`
     (DFU-консоль bw-flasher). Ответ (`ok`, версия, `64 2A … 9B`) =>
     TX реально доходит до MCU и там есть DFU-консоль.

Запуск в отдельном окне:
  powershell -Command "Start-Process python -ArgumentList 'tools\\uart_link_check.py','--port','COM3'"
"""
import argparse
import sys
import time

import serial


def parse_61(d):
    """Кадры 61 … с проверкой CHK. Возвращает (ok, bad)."""
    i = 0
    ok = bad = 0
    while i + 5 <= len(d):
        if d[i] == 0x61 and d[i + 2] <= 200:
            ln = d[i + 2]
            e = i + 4 + ln + 1
            if e <= len(d) and d[e - 1] == 0x9E:
                s = sum(d[i:e - 2]) & 0xFF
                if s == d[e - 2]:
                    ok += 1
                else:
                    bad += 1
                i = e
                continue
        i += 1
    return ok, bad


def open_port(port, baud):
    """Открывает порт, дожидаясь подключения USB-TTL."""
    while True:
        try:
            s = serial.Serial(port, baud, timeout=0.3)
            print(f"[{time.strftime('%H:%M:%S')}] >>> {port} подключён", flush=True)
            return s
        except Exception:
            print(f"[{time.strftime('%H:%M:%S')}] USB-TTL не найден — жду 2 с…", flush=True)
            time.sleep(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM3")
    ap.add_argument("--baud", type=int, default=19200)
    a = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(f"=== UART link check: {a.port} @ {a.baud} ===  (цикл ~4 с, авто-переподключение)")
    print("-" * 72)

    s = open_port(a.port, a.baud)
    n = 0
    try:
        while True:
            n += 1
            try:
                run_cycle(s, n)
            except (serial.SerialException, OSError):
                print(f"[{time.strftime('%H:%M:%S')}] !!! отсоединён — переподключение…", flush=True)
                try:
                    s.close()
                except Exception:
                    pass
                s = open_port(a.port, a.baud)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            s.close()
        except Exception:
            pass


def run_cycle(s, n):
    # --- RX-фаза: 1.5 с чистого слушания ---
    s.reset_input_buffer()
    rx_buf = bytearray()
    end = time.time() + 1.5
    while time.time() < end:
        d = s.read(256)
        if d:
            rx_buf += d
    rx_d = bytes(rx_buf)
    rx_ok, _ = parse_61(rx_d)
    rx_status = "OK" if rx_d else "НЕТ ДАННЫХ"

    # --- TX-wiring фаза: 2 с burst DE AD + параллельное чтение ---
    s.reset_input_buffer()
    tx_buf = bytearray()
    end = time.time() + 2.0
    while time.time() < end:
        for _ in range(10):
            s.write(b"\xde\xad")
        d = s.read(256)
        if d:
            tx_buf += d
    tx_d = bytes(tx_buf)
    de_n = tx_d.count(b"\xde")
    tx_ok, tx_bad = parse_61(tx_d)

    if de_n > 20:
        wire_status = "LOOPBACK (TX замкнут с RX!)"
    elif tx_bad > 3 and tx_bad > tx_ok:
        wire_status = "НА ШИНЕ TX MCU (конфликт)"
    else:
        wire_status = "ок (замыканий нет)"

    # --- функциональная DFU-проба раз в 5 циклов ---
    dfu_status = "…"
    if n % 5 == 0:
        s.reset_input_buffer()
        s.write(b"down get_ver\r")
        time.sleep(0.4)
        s.write(bytes.fromhex("53 2a 7d ac"))
        dfu_buf = bytearray()
        end = time.time() + 1.5
        while time.time() < end:
            d = s.read(256)
            if d:
                dfu_buf += d
        # ищем ответ: не push-кадры 61, а что-то другое (текст/64 2A)
        other = bytearray()
        i = 0
        while i + 5 <= len(dfu_buf):
            if dfu_buf[i] == 0x61 and dfu_buf[i + 2] <= 200:
                ln = dfu_buf[i + 2]
                e = i + 4 + ln + 1
                if e <= len(dfu_buf) and dfu_buf[e - 1] == 0x9E:
                    i = e
                    continue
            other.append(dfu_buf[i])
            i += 1
        other = bytes(other)
        if other:
            dfu_status = f"ОТВЕТ DFU: {other[:32].hex(' ')}"
        else:
            dfu_status = "без ответа (консоли на линии нет или TX не доходит)"

    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] RX: {rx_status:<12} ({len(rx_d):4d} Б, {rx_ok} кадров)")
    print(f"       TX-wiring: {wire_status} (эхо={de_n}, ok/bad={tx_ok}/{tx_bad})")
    if dfu_status != "…":
        print(f"       {dfu_status}", flush=True)


if __name__ == "__main__":
    main()
