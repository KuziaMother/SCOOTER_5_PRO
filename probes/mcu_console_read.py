#!/usr/bin/env python3
"""
The READ-ONLY full set of the safe reads of the MCU DFU console over the USART3
(19200 8N1).

It writes NOTHING into the NVM/flash, it does not touch the motor. Only the read-only
commands:
  1. The UID — the binary handshake `53 2A 7D AC` (the warmup: the get_ver + the 0.4s
     pause); the frame `64 2A 10 <UID 16B> <chk> 9B`. The secret is masked.
  2. The get_ver — the MCU version (the "0007" is expected).
  3. The rd_info — the state of the DFU/NVM region.
  4. The mcu_rand — the 16-byte nonce. The secret is masked.

It does NOT send: the nvm_write / wr_info / dfu_verify / dfu_active / mcu_key / ble_key /
the FW chunks / ble_rand (the key material). The UID and the mcu_rand are printed MASKED.

Usage:  python probes/mcu_console_read.py [--port COM3]

READ-ONLY полный набор безопасных чтений MCU DFU-консоли по USART3 (19200 8N1).
================================================================================
НИЧЕГО не пишет в NVM/flash, не трогает мотор. Только read-only команды:
  1. UID        — бинарный handshake `53 2A 7D AC` (warmup: get_ver + пауза 0.4с);
                   кадр `64 2A 10 <UID 16Б> <chk> 9B`. Секрет маскируется.
  2. get_ver    — версия MCU (ожидается "0007").
  3. rd_info    — состояние DFU/NVM-региона (`down rd_info\\r\\x00\\x00\\x00`).
  4. mcu_rand   — 16-байтовый nonce (`ok <16Б>\\r`). Секрет маскируется.

НЕ шлёт: nvm_write / wr_info / dfu_verify / dfu_active / mcu_key / ble_key /
чанки FW / ble_rand (key-материал). UID и mcu_rand печатаются МАСТИРОВАННО.

Запуск:  python probes/mcu_console_read.py [--port COM3]
"""
import argparse
import time

import serial


class Reader:
    """The push filter (the 0x61...chk 9E frames are cut out of the clean buffer).
    Push-фильтр (кадры 0x61…chk 9E отбрасываются из clean-буфера)."""

    def __init__(self, s):
        """Wrap the serial port s.
        Обёртка над последовательным портом s."""
        self.s = s
        self.raw = bytearray()
        self.clean = bytearray()

    def _pump(self):
        """Read a chunk into the raw + classify.
        Прочитать чанк в raw + классифицировать."""
        d = self.s.read(256)
        if d:
            self.raw += d
        self._classify()

    def _classify(self):
        """Split the raw: cut the valid push frames into the clean, hold the tail.
        Разделить raw: валидные push-кадры выкинуть, clean пополнить, хвост удержать."""
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
        """The bytes up to the term (inclusive); on the timeout — everything there is.
        Байты до `term` включительно; на таймауте — всё, что есть."""
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
        """Take everything from the clean and return it.
        Забрать всё из clean и вернуть."""
        d = bytes(self.clean)
        del self.clean[:]
        return d


def mask(b, n=4):
    """The hex of the secret with the mask (the head…tail + the length).
    Hex секрета с маскировкой (голова…хвост + длина)."""
    if len(b) <= 2 * n:
        return b.hex()
    return f"{b[:n].hex()}…{b[-2:].hex()} ({len(b)}B)"


def main():
    """The read-only console run (the --port option): the UID/get_ver/rd_info/mcu_rand.
    READ-ONLY прогон консоли (опция --port): UID/get_ver/rd_info/mcu_rand."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM3")
    a = ap.parse_args()

    print(f"[*] {a.port} @ 19200 8N1 (READ-ONLY)")
    s = serial.Serial(a.port, 19200, timeout=0.2)
    r = Reader(s)
    try:
        # --- 1) UID (warmup + hex-кадр) ---
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
            print("[1] UID: нет ответа (нужен warmup; повторить?)")

        def show(tag, payload, suffix=b"", tries=3):
            """Send the payload, wait for the line, print it (the retries).
            Отправить payload, ждать строку, напечатать (повторы)."""
            for _ in range(tries):
                r.drain()
                s.write(payload + suffix); s.flush()
                d = r.read_until(b"\r", timeout=2.5)
                if d.endswith(b"\r") and d.split(b"\r")[0]:
                    line = d.split(b"\r")[0].decode("ascii", "replace")
                    print(f"{tag}: {line!r}")
                    return
                time.sleep(0.4)
            print(f"{tag}: НЕТ ответа (raw={d.hex(' ')})")

        time.sleep(0.6)  # пауза после бинарного handshake перед текстовыми командами
        # --- 2) get_ver ---
        show("[2] get_ver", b"down get_ver")

        time.sleep(0.3)
        # --- 3) rd_info (с суффиксом \x00\x00\x00 как во флешере) ---
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

        print("\n[+] готово. Ничего не записывалось.")
    finally:
        s.close()


if __name__ == "__main__":
    main()
