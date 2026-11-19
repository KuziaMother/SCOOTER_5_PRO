#!/usr/bin/env python3
"""
The READ-ONLY: it tries the `down rd_info` with the different 3-byte suffixes to
understand whether it is the reader of the NVM/DFU region by the selector (and whether
the data can be dumped so). It writes NOTHING — the rd_info = the read info. If some
selector gives a reply NOT of the "ok ..." form, we record it too (but we do not repeat
the command aggressively).

READ-ONLY: пробует `down rd_info` с разными 3-байтными суффиксами, чтобы понять,
является ли он читателем NVM/DFU-региона по селектору (и можно ли так дампит данные).
НИЧЕГО не пишет — rd_info = read info. Если какой-то селектор даст ответ НЕ вида
"ok …", это тоже фиксируем (но команду не повторяем агрессивно).
"""
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
        out = bytearray(); i, n = 0, len(self.raw)
        while i < n:
            b = self.raw[i]
            if b == 0x61:
                rem = n - i
                if rem < 3:
                    break
                ln = self.raw[i + 2]; e = i + ln + 5
                if ln <= 200 and e <= n and self.raw[e - 1] == 0x9E \
                        and (sum(self.raw[i:e - 2]) & 0xFF) == self.raw[e - 2]:
                    i = e; continue
                if ln <= 200 and e > n:
                    break
            out.append(b); i += 1
        del self.raw[:i]; self.clean += out

    def read_until(self, term, timeout=3.0):
        """The bytes up to the term (inclusive); on the timeout — everything there is.
        Байты до `term` включительно; на таймауте — всё, что есть."""
        end = time.time() + timeout
        while True:
            j = self.clean.find(term)
            if j >= 0:
                d = bytes(self.clean[:j + len(term)]); del self.clean[:j + len(term)]; return d
            if time.time() >= end:
                d = bytes(self.clean); del self.clean[:]; return d
            self._pump()

    def drain(self):
        """Take everything from the clean and return it.
        Забрать всё из clean и вернуть."""
        d = bytes(self.clean); del self.clean[:]; return d


def main():
    """The rd_info suffix sweep (the read-only run).
    Обход суффиксов rd_info (read-only прогон)."""
    s = serial.Serial("COM3", 19200, timeout=0.2)
    r = Reader(s)
    try:
        # warmup
        r.drain(); s.write(b"down get_ver\r"); s.flush()
        r.read_until(b"\r", timeout=2.0); time.sleep(0.3)

        suffixes = [b"", b"\x00\x00\x00", b"\x01\x00\x00", b"\x02\x00\x00",
                    b"\x03\x00\x00", b"\x04\x00\x00", b"\x05\x00\x00",
                    b"\x00\x01\x00", b"\x00\x00\x01", b"\xff\xff\xff"]
        for suf in suffixes:
            r.drain()
            s.write(b"down rd_info\r" + suf); s.flush()
            d = r.read_until(b"\r", timeout=2.5)
            if d.endswith(b"\r") and d.split(b"\r")[0]:
                line = d.split(b"\r")[0].decode("ascii", "replace")
            else:
                line = f"НЕТ (raw={d.hex(' ')})"
            print(f"rd_info\\r{suf.hex():>10}  ->  {line!r}")
            time.sleep(0.3)
        print("\n[+] готово.")
    finally:
        s.close()


if __name__ == "__main__":
    main()
