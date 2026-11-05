#!/usr/bin/env python3
"""
READ-ONLY decoder for MCU->BLE push frames (0x61 'a'/'a1') on UART 19200.
====================================================================
Passive observation only — sends NOTHING, listens and decodes spontaneous
push stream. Validation: §47.2 ('a0' telemetry), §47.3 ('a1' battery), §34.2 (mode).

Format (wire, without slot length prefix):  61 [sub] [len] [...data] [chk] 9E
  chk = sum(frame bytes before chk) & 0xFF, trailer = 0x9E.
'a0' (sub=0x30): [3]=mode-nibble(@0x228<<4|@0x229), [6]=biased i16@0x31c,
  [7]=|i16@0x290|, [8]=status, [9..a]=u16@0x236 (percent §69/§34.2), [b]=flag, [c]=bit3@0x244
'a1' (sub=0x31): [3]=@0x2e6, [4]=battery%, [5..6]=u16@0x308 BE, [7..8]=u16@0x30a BE,
  [9]=temperature °C, [a..b]=range BE

Usage:  python probes/mcu_push_decode.py [--port COM3] [--listen 5.0] [--max N]
"""
import argparse
import time

import serial


def collect_frames(s, secs):
    """Collect valid full push frames from stream."""
    buf = bytearray()
    frames = []
    end = time.time() + secs
    while time.time() < end:
        d = s.read(256)
        if d:
            buf += d
        i, n = 0, len(buf)
        while i < n:
            if buf[i] != 0x61:
                i += 1
                continue
            rem = n - i
            if rem < 3:
                break
            ln = buf[i + 2]
            e = i + ln + 5
            if ln > 200:
                i += 1
                continue
            if e > n:
                break  # incomplete frame — wait for more data
            if buf[e - 1] != 0x9E or (sum(buf[i:e - 2]) & 0xFF) != buf[e - 2]:
                i += 1  # not our frame / corrupt — advance
                continue
            frames.append(bytes(buf[i:e]))
            del buf[:e]
            i = 0
            n = len(buf)
    return frames


def dec_biased(raw):
    """i16@0x31c: v>=0 -> v; v<0 -> (128-v)&0xFF. Inverted."""
    return raw if raw < 128 else 128 - raw


def decode_a0(f):
    mode_hi, mode_lo = f[3] >> 4, f[3] & 0xF
    p236 = (f[9] << 8) | f[10]
    return (f"mode@0x229={mode_lo} (@0x228={mode_hi})  mask=0x{f[5]:02x}  "
            f"i16@0x31c={dec_biased(f[6]):+d}  |i16@0x290|={f[7]}  "
            f"status=0x{f[8]:02x}  **u16@0x236(%)={p236}**  flag={f[11]}")


def decode_a1(f):
    return (f"@0x2e6={f[3]}  **battery%={f[4]}**  u16@0x308={(f[5]<<8)|f[6]}  "
            f"u16@0x30a={(f[7]<<8)|f[8]}  **temperature C={f[9]}**  "
            f"range={(f[10]<<8)|f[11]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM3")
    ap.add_argument("--listen", type=float, default=5.0)
    ap.add_argument("--max", type=int, default=8, help="how many frames of each type to print")
    a = ap.parse_args()

    print(f"[*] listening {a.port} @ 19200 (READ-ONLY, monitor only)")
    s = serial.Serial(a.port, 19200, timeout=0.2)
    try:
        frames = collect_frames(s, a.listen)
        print(f"[+] collected valid push frames in {a.listen:.1f}s: {len(frames)}")
        if not frames:
            print("    [!] no frames — check connection / scooter is powered on")
            return

        n0 = sum(1 for f in frames if len(f) > 2 and f[1] == 0x30)
        n1 = sum(1 for f in frames if len(f) > 2 and f[1] == 0x31)
        nother = len(frames) - n0 - n1
        print(f"    'a0' (telemetry): {n0},  'a1' (battery): {n1},  other: {nother}\n")

        shown0 = shown1 = 0
        for f in frames:
            if len(f) < 4:
                continue
            sub = f[1]
            if sub == 0x30 and shown0 < a.max:
                print(f"  'a0' {f.hex(' ')}")
                print(f"       → {decode_a0(f)}")
                shown0 += 1
            elif sub == 0x31 and shown1 < a.max:
                print(f"  'a1' {f.hex(' ')}")
                print(f"       → {decode_a1(f)}")
                shown1 += 1
        print("\n[+] Done. Nothing was sent.")
    finally:
        s.close()


if __name__ == "__main__":
    main()
