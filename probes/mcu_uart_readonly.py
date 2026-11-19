#!/usr/bin/env python3
"""
The READ-ONLY probe of the MCU DFU console over the UART (19200 8N1) — it writes
NOTHING.

The goal: the live confirmation of the section 70 (the string pool of the DFU commands)
without the risk for the device.

It does ONLY:
  1. it listens to the spontaneous push stream (the 0x61...chk 9E frames) — it confirms
     the baud/the link;
  2. the `down get_ver` -> the MCU version (the "0007" is expected);
  3. the `down rd_info` -> the state of the DFU/NVM region (the "ok ..." is expected).

It does NOT send: the nvm_write / wr_info / dfu_verify / dfu_active / the FW chunks —
nothing is written into the NVM/flash, the motor is not touched. The command terminator
= the CR (0x0d) — the same as in the pool strings of the section 70.

Usage:  python probes/mcu_uart_readonly.py [--port COM3] [--listen 2.0]

READ-ONLY зонд MCU DFU-консоли по UART (19200 8N1) — НИЧЕГО не пишет.

Цель: live-подтверждение §70 (строковый пул команд DFU) без риска для устройства.

Делает ТОЛЬКО:
  1. слушает спонтанный push-поток (кадры 0x61…chk 9E) — подтверждает baud/связь;
  2. `down get_ver` -> версия MCU (ожидается "0007");
  3. `down rd_info` -> состояние DFU/NVM-региона (ожидается "ok …").

НЕ шлёт: nvm_write / wr_info / dfu_verify / dfu_active / чанки FW — ничего не
пишется в NVM/flash, мотор не трогается. Терминатор команды = \r (0x0d) — тот же,
что в строках пула §70.

Запуск:  python probes/mcu_uart_readonly.py [--port COM3] [--listen 2.0]
"""
import argparse
import time

import serial


class Reader:
    """The copy of the push filter from tools/mcu_uart_flash.py (the valid push frames
    are cut out).
    Копия push-фильтра из tools/mcu_uart_flash.py (валидные push-кадры отбрасываются)."""

    def __init__(self, s):
        """Wrap the serial port s.
        Обёртка над последовательным портом s."""
        self.s = s
        self.raw = bytearray()
        self.clean = bytearray()
        self.push_frames = 0

    def _pump(self):
        """Read a chunk into the raw + classify.
        Прочитать чанк в raw + классифицировать."""
        d = self.s.read(256)
        if d:
            self.raw += d
        self._classify()

    def _classify(self):
        """Split the raw: cut the valid push frames into the clean (the counter++), hold
        the tail.
        Разделить raw: валидные push-кадры выкинуть (счётчик++), clean пополнить, хвост
        удержать."""
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


def listen(r, secs):
    """Слушаем push-поток; возвращаем (кол-во push-кадров, пример raw hex)."""
    end = time.time() + secs
    before = r.push_frames
    sample = bytearray()
    while time.time() < end:
        r._pump()
        if len(sample) < 64:
            sample += bytes(r.raw[:64 - len(sample)])
    return r.push_frames - before, bytes(sample)


def cmd(r, payload, timeout=3.0):
    """Drain → отправить → ждать строку до \\r (или None на таймаут)."""
    r.drain()
    r.s.write(payload)
    r.s.flush()
    d = r.read_until(b"\r", timeout=timeout)
    if not d.endswith(b"\r"):
        return None, d
    return d.split(b"\r")[0], d


def main():
    """The read-only run: the push-stream listening + the get_ver/rd_info (the --port/
    --listen options).
    READ-ONLY прогон: слушание push-потока + get_ver/rd_info (опции --port/--listen)."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM3")
    ap.add_argument("--listen", type=float, default=2.0, help="секунд слушать push-поток")
    a = ap.parse_args()

    print(f"[*] открываю {a.port} @ 19200 8N1 (READ-ONLY)")
    s = serial.Serial(a.port, 19200, timeout=0.2)
    r = Reader(s)
    try:
        # 1) push-поток (валидация baud/связи)
        npush, sample = listen(r, a.listen)
        print(f"[1] push-поток за {a.listen:.1f}с: валидных кадров 0x61…9E = {npush}")
        if sample:
            print(f"    пример raw: {sample.hex(' ')}")
        if npush == 0:
            print("    [!] push-кадров нет — проверь baud/подключение (самокат включён?). "
                  "Продолжаю с запросами…")

        # 2) get_ver
        line, raw = cmd(r, b"down get_ver\r", timeout=3.0)
        if line is None:
            print(f"[2] get_ver: НЕТ ответа (raw={raw.hex(' ')})")
        else:
            print(f"[2] down get_ver  -> {line.decode('ascii', 'replace')!r}")

        time.sleep(0.4)
        # 3) rd_info
        line, raw = cmd(r, b"down rd_info\r", timeout=3.0)
        if line is None:
            print(f"[3] rd_info: НЕТ ответа (raw={raw.hex(' ')})")
        else:
            print(f"[3] down rd_info  -> {line.decode('ascii', 'replace')!r}")

        print("\n[+] готово. Ничего не записывалось.")
    finally:
        s.close()


if __name__ == "__main__":
    main()
