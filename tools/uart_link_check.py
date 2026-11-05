#!/usr/bin/env python3
"""UART link verification: tests RX and TX connectivity (~4 s rapid cycle).

Usage:
  python tools/uart_link_check.py --port COM3
"""
import argparse
import sys
import time

import serial


def parse_61(d):
    """Frames 61 ... with CHK verification. Returns (ok, bad)."""
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
    """Opens port, waiting for USB-TTL connection."""
    while True:
        try:
            s = serial.Serial(port, baud, timeout=0.3)
            print(f"[{time.strftime('%H:%M:%S')}] >>> {port} connected", flush=True)
            return s
        except Exception:
            print(f"[{time.strftime('%H:%M:%S')}] USB-TTL not found — waiting 2 s...", flush=True)
            time.sleep(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM3")
    ap.add_argument("--baud", type=int, default=19200)
    a = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(f"=== UART link check: {a.port} @ {a.baud} ===  (~4 s cycle, auto-reconnect)")
    print("-" * 72)

    s = open_port(a.port, a.baud)
    n = 0
    try:
        while True:
            n += 1
            try:
                run_cycle(s, n)
            except (serial.SerialException, OSError):
                print(f"[{time.strftime('%H:%M:%S')}] !!! disconnected — reconnecting...", flush=True)
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
    # --- RX-phase: 1.5s pure listening ---
    s.reset_input_buffer()
    rx_buf = bytearray()
    end = time.time() + 1.5
    while time.time() < end:
        d = s.read(256)
        if d:
            rx_buf += d
    rx_d = bytes(rx_buf)
    rx_ok, _ = parse_61(rx_d)
    rx_status = "OK" if rx_d else "NO DATA"

    # --- TX-wiring phase: 2s burst DE AD + parallel reading ---
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
        wire_status = "LOOPBACK (TX shorted to RX!)"
    elif tx_bad > 3 and tx_bad > tx_ok:
        wire_status = "ON MCU TX BUS (contention)"
    else:
        wire_status = "ok (no shorts)"

    # --- functional DFU probe every 5 cycles ---
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
        # search for response: not push-frames 61, but something else (text/64 2A)
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
            dfu_status = f"DFU REPLY: {other[:32].hex(' ')}"
        else:
            dfu_status = "no response (no console on line or TX not reaching MCU)"

    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] RX: {rx_status:<12} ({len(rx_d):4d} B, {rx_ok} frames)")
    print(f"       TX-wiring: {wire_status} (echo={de_n}, ok/bad={tx_ok}/{tx_bad})")
    if dfu_status != "…":
        print(f"       {dfu_status}", flush=True)


if __name__ == "__main__":
    main()
