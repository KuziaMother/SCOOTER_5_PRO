#!/usr/bin/env python3
"""
READ-ONLY complete suite of safe MCU DFU console queries over USART3 (19200 8N1).
================================================================================
Writes NOTHING to NVM/flash, does not affect motor. Read-only commands only:
  1. UID        — binary handshake `53 2A 7D AC` (warmup: get_ver + 0.4s pause);
                   frame `64 2A 10 <UID 16B> <chk> 9B`. Secrets masked.
  2. get_ver    — MCU version (expected "0007").
  3. rd_info    — DFU/NVM region state (`down rd_info\\r\\x00\\x00\\x00`).
  4. mcu_rand   — 16-byte nonce (`ok <16B>\\r`). Secret masked.

Does NOT send: nvm_write / wr_info / dfu_verify / dfu_active / mcu_key / ble_key /
FW chunks / ble_rand (key material). UID and mcu_rand are MASKED in output.

Usage:  python probes/mcu_console_read.py [--port COM3]
"""
import argparse
import time

import serial


class Reader:
    """Push-filter (frames 0x61...chk 9E are dropped from clean buffer)."""

    def __init__(self, s):
        self.s = s
        self.raw = bytearray()
        self.clean = bytearray()

    def _pump(self):
        d = self.s.read(256)
        if d:
            self.raw += d
        self._classify()

    def _classify(self):
        out = bytearray()
        i, n = 0, len(self.raw)
        while i < n:
            b = self.raw[i]
            if b == 0x61:
                rem = n - i
                if rem < 3:
                    break
                ln = self.raw[i + 2]
                e = i + ln + 5
                if ln <= 200 and e <= n and self.raw[e - 1] == 0x9E \
                        and (sum(self.raw[i:e - 2]) & 0xFF) == self.raw[e - 2]:
                    i = e
                    continue
                if ln <= 200 and e > n:
                    break
            out.append(b)
            i += 1
        del self.raw[:i]
        self.clean += out

    def read_until(self, term, timeout=3.0):
        end = time.time() + timeout
        while True:
            j = self.clean.find(term)
            if j >= 0:
                d = bytes(self.clean[:j + len(term)])
                del self.clean[:j + len(term)]
                return d
            if time.time() >= end:
                d = bytes(self.clean)
                del self.clean[:]
                return d
            self._pump()

    def drain(self):
        d = bytes(self.clean)
        del self.clean[:]
        return d


def mask(b, n=4):
    if len(b) <= 2 * n:
        return b.hex()
    return f"{b[:n].hex()}…{b[-2:].hex()} ({len(b)}B)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM3")
    a = ap.parse_args()

    print(f"[*] {a.port} @ 19200 8N1 (READ-ONLY)")
    s = serial.Serial(a.port, 19200, timeout=0.2)
    r = Reader(s)
    try:
        # --- 1) UID (warmup + hex frame) ---
        uid = None
        for attempt in range(1, 4):
            r.drain()
            s.write(b"down get_ver\r")
            s.flush()
            time.sleep(0.4)
            r.drain()
            s.write(bytes.fromhex("53 2A 7D AC"))
            s.flush()
            acc = bytearray()
            end = time.time() + 2.0
            while True:
                acc += r.read_until(b"\x9b", timeout=max(0.1, end - time.time()))
                i = acc.find(b"\x64\x2a\x10")
                if i >= 0 and i + 21 <= len(acc) and acc[i + 20] == 0x9B \
                        and (sum(acc[i:i + 19]) & 0xFF) == acc[i + 19]:
                    uid = bytes(acc[i + 3:i + 19])
                    break
                if time.time() >= end:
                    break
            if uid:
                break
        if uid:
            print(f"[1] UID (16B, masked): {mask(uid)}")
        else:
            print("[1] UID: no response (warmup needed; retry?)")

        def show(tag, payload, suffix=b"", tries=3):
            for _ in range(tries):
                r.drain()
                s.write(payload + suffix); s.flush()
                d = r.read_until(b"\r", timeout=2.5)
                if d.endswith(b"\r") and d.split(b"\r")[0]:
                    line = d.split(b"\r")[0].decode("ascii", "replace")
                    print(f"{tag}: {line!r}")
                    return
                time.sleep(0.4)
            print(f"{tag}: NO response (raw={d.hex(' ')})")

        time.sleep(0.6)  # pause after binary handshake before text commands
        # --- 2) get_ver ---
        show("[2] get_ver", b"down get_ver")

        time.sleep(0.3)
        # --- 3) rd_info (with suffix \x00\x00\x00 as in flasher) ---
        show("[3] rd_info", b"down rd_info", suffix=b"\x00\x00\x00")

        time.sleep(0.3)
        # --- 4) mcu_rand (nonce, masked) ---
        r.drain()
        s.write(b"down mcu_rand\r"); s.flush()
        end = time.time() + 3.0
        acc = bytearray()
        while time.time() < end:
            acc += r.read_until(b"\r", timeout=0.2)
            if acc.endswith(b"\r"):
                break
        line = bytes(acc).split(b"\r")[0]
        if line.startswith(b"ok ") and len(line) >= 3 + 16:
            nonce = line[3:3 + 16]
            print(f"[4] mcu_rand (16B, masked): {mask(nonce)}")
        else:
            print(f"[4] mcu_rand: raw={bytes(acc)[:24].hex(' ')}")

        print("\n[+] Done. Nothing was written.")
    finally:
        s.close()


if __name__ == "__main__":
    main()
