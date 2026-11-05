#!/usr/bin/env python3
"""
READ-ONLY probe of MCU DFU console over UART (19200 8N1) — writes NOTHING.
====================================================================
Goal: live confirmation of §70 DFU command pool without risk to hardware.

Performs ONLY:
  1. listens to spontaneous push stream (0x61...chk 9E frames) — validates baud/link;
  2. `down get_ver`  -> MCU version (expected "0007");
  3. `down rd_info`  -> DFU/NVM state (expected "ok ...").

Does NOT send: nvm_write / wr_info / dfu_verify / dfu_active / FW chunks — nothing
is written to NVM/flash, motor untouched. Command terminator = \r (0x0d).

Usage:  python probes/mcu_uart_readonly.py [--port COM3] [--listen 2.0]
"""
import argparse
import time

import serial


class Reader:
    """Copy of push filter from tools/mcu_uart_flash.py (valid push frames discarded)."""

    def __init__(self, s):
        self.s = s
        self.raw = bytearray()
        self.clean = bytearray()
        self.push_frames = 0

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
                    self.push_frames += 1
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


def listen(r, secs):
    """Listens to push stream; returns (push frame count, sample raw hex)."""
    end = time.time() + secs
    before = r.push_frames
    sample = bytearray()
    while time.time() < end:
        r._pump()
        if len(sample) < 64:
            sample += bytes(r.raw[:64 - len(sample)])
    return r.push_frames - before, bytes(sample)


def cmd(r, payload, timeout=3.0):
    """Drain -> send -> wait line up to \\r (or None on timeout)."""
    r.drain()
    r.s.write(payload)
    r.s.flush()
    d = r.read_until(b"\r", timeout=timeout)
    if not d.endswith(b"\r"):
        return None, d
    return d.split(b"\r")[0], d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM3")
    ap.add_argument("--listen", type=float, default=2.0, help="seconds to listen to push stream")
    a = ap.parse_args()

    print(f"[*] opening {a.port} @ 19200 8N1 (READ-ONLY)")
    s = serial.Serial(a.port, 19200, timeout=0.2)
    r = Reader(s)
    try:
        # 1) push stream (baud/link validation)
        npush, sample = listen(r, a.listen)
        print(f"[1] push stream in {a.listen:.1f}s: valid frames 0x61...9E = {npush}")
        if sample:
            print(f"    sample raw: {sample.hex(' ')}")
        if npush == 0:
            print("    [!] no push frames — verify baud/connection (is scooter ON?). "
                  "Continuing with queries...")

        # 2) get_ver
        line, raw = cmd(r, b"down get_ver\r", timeout=3.0)
        if line is None:
            print(f"[2] get_ver: NO response (raw={raw.hex(' ')})")
        else:
            print(f"[2] down get_ver  -> {line.decode('ascii', 'replace')!r}")

        time.sleep(0.4)
        # 3) rd_info
        line, raw = cmd(r, b"down rd_info\r", timeout=3.0)
        if line is None:
            print(f"[3] rd_info: NO response (raw={raw.hex(' ')})")
        else:
            print(f"[3] down rd_info  -> {line.decode('ascii', 'replace')!r}")

        print("\n[+] complete. Nothing was written.")
    finally:
        s.close()


if __name__ == "__main__":
    main()
