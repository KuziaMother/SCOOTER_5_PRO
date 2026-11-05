#!/usr/bin/env python3
"""Baud rate scanner for scooter UART lines (GD32 MCU <-> RTL8762C BLE).

Usage:
  python tools/uart_baud_scan.py --port COM5 [--seconds 3]
  python tools/uart_baud_scan.py --port COM5 --baud 921600 --sniff out.bin
"""
import argparse
import sys
import time

import serial
import serial.tools.list_ports

BAUDS = [921600, 460800, 230400, 115200, 57600, 38400, 19200, 9600]


def score_63(buf: bytes) -> int:
    """MCU->BLE request frames: 63 CMD CHK 9C."""
    n = 0
    for i in range(len(buf) - 3):
        if buf[i] == 0x63 and buf[i + 3] == 0x9C:
            if (buf[i] + buf[i + 1]) & 0xFF == buf[i + 2]:
                n += 1
    return n


def score_74(buf: bytes) -> int:
    """BLE->MCU telemetry frames: 74 CMD LEN DATA CHK 8B."""
    n = 0
    i = 0
    while i < len(buf) - 5:
        if buf[i] == 0x74 and buf[i + 1] in (0x41, 0x42, 0x43, 0x44, 0x45, 0x46,
                                             0x48, 0x49, 0x4A, 0x60, 0x61):
            ln = buf[i + 2]
            if i + 5 + ln <= len(buf) and ln < 150:
                s = sum(buf[i:i + 3 + ln]) & 0xFF
                if s == buf[i + 3 + ln] and buf[i + 4 + ln] == 0x8B:
                    n += 1
                    i += 5 + ln
                    continue
        i += 1
    return n


def score_61(buf: bytes) -> int:
    """MCU->BLE push status frames (UART4): 61 30 0A <10B> CHK 9E."""
    n = 0
    for i in range(len(buf) - 14):
        if buf[i:i + 3] == b"\x61\x30\x0a":
            s = sum(buf[i:i + 13]) & 0xFF
            if s == buf[i + 13] and buf[i + 14] == 0x9E:
                n += 1
    return n


def sanity(buf: bytes) -> float:
    """General frame structural quality metric (0..1, higher is better)."""
    if not buf:
        return 0.0
    live = sum(1 for b in buf if b not in (0x00, 0xFF)) / len(buf)
    freq = [0] * 256
    for b in buf:
        freq[b] += 1
    import math
    ent = -sum((c / len(buf)) * math.log2(c / len(buf)) for c in freq if c)
    # proper UART: moderate entropy (3..7 bits), noise on incorrect baud —
    # either ~0 (all 0x00/0xFF), or >7.5
    ent_score = max(0.0, 1.0 - abs(ent - 5.5) / 4.0)
    return 0.5 * live + 0.5 * ent_score


def capture(port: str, baud: int, seconds: float) -> bytes:
    with serial.Serial(port, baud, timeout=1) as s:
        end = time.time() + seconds
        out = bytearray()
        while time.time() < end:
            out += s.read(4096)
    return bytes(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--port", help="USB-TTL COM port (list available if omitted)")
    ap.add_argument("--seconds", type=float, default=3.0,
                    help="capture duration per baud rate (default: 3 s)")
    ap.add_argument("--bauds", default=",".join(str(b) for b in BAUDS))
    ap.add_argument("--baud", type=int, help="--sniff mode: specific baud rate")
    ap.add_argument("--sniff", metavar="FILE",
                    help="capture to FILE with decoding (instead of scan)")
    a = ap.parse_args()

    if a.port is None:
        ports = [p.device for p in serial.tools.list_ports.comports()]
        print("Available COM ports:")
        for p in ports:
            print(f"  {p}")
        if not ports:
            sys.exit("No ports found — connect USB-TTL adapter.")
        sys.exit("Run with --port COMx")

    if a.sniff:
        buf = capture(a.port, a.baud, max(a.seconds, 10.0))
        with open(a.sniff, "wb") as f:
            f.write(buf)
        n63, n74, n61 = score_63(buf), score_74(buf), score_61(buf)
        print(f"Captured {len(buf)} B in {a.seconds:.0f} s @ {a.baud}")
        print(f"  frames 63..9C: {n63}, 74-telemetry: {n74}, 61-30-0A push: {n61}")
        print(f"  saved: {a.sniff}")
        if buf:
            print(f"  first 64 B: {buf[:64].hex(' ')}")
        return

    print(f"Scanning baud on {a.port} ({a.seconds:.0f} s per rate), scooter POWERED ON?")
    results = []
    for baud in [int(b) for b in a.bauds.split(",")]:
        buf = capture(a.port, baud, a.seconds)
        s63, s74, s61 = score_63(buf), score_74(buf), score_61(buf)
        san = sanity(buf)
        total = max(s63, s74, s61)
        results.append((total, san, baud, len(buf), s63, s74, s61))
        print(f"  {baud:>7}: bytes={len(buf):>6}  63-frames={s63:<4} 74-frames={s74:<4} 61-push={s61:<3} sanity={san:.2f}")
    results.sort(reverse=True)
    best = results[0]
    print(f"\nBest candidate: {best[2]} baud (frames: {best[4]+best[5]+best[6]}, sanity={best[1]:.2f})")
    if best[4] + best[5] + best[6] == 0:
        print("No valid frames detected on any baud rate. Please verify:")
        print("  - scooter is turned on (and Mi Home app is open for active traffic);")
        print("  - USB-TTL GND is shared with scooter board;")
        print("  - probe is connected to the correct line (TX of monitored chip).")


if __name__ == "__main__":
    main()
