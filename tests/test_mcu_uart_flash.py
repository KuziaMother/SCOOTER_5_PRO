#!/usr/bin/env python3
"""Offline verification of tools/mcu_uart_flash.py against MCU-side emulation.

The model reproduces the verified live hardware sequence (logs/bw_flasher_log.txt,
2026-08-21): handshake -> 74 packets (0x800) -> terminating empty packet ->
dfu_verify (first reply empty) -> dfu_active -> reboot -> get_ver "007".

Includes adversarial conditions that break naive parsers:
  - push telemetry frames arrive continuously, INCLUDING the chunk write phase;
  - frames include CHK == 0x06 and CHK == 0x15 (false ACK / CRC-fail traps
    for parsers that do not filter frames);
  - frames split mid-stream (Reader holdback logic);
  - select chunks only reply upon retransmission (retry path).

Crypto anchors: known vector from live log (uid=4A77..., rand=01..10 ->
BLE_KEY 7049273DE6BD8383FBF33C3A128EB946). wr_info CRC anchors: a7dfe686 (p1)
and 77f34c63 (p74/p75) from the same capture log.
"""
import binascii
import os
import queue
import random
import sys
import threading
import time
import zlib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import mcu_uart_flash as muf  # noqa: E402
from mcu_keygen import sign_rand  # noqa: E402

# MCU image: local firmware_ota/ (gitignored) if present, else committed fixture duplicate
_FW_LOCAL = ROOT / "firmware_ota" / "c0f78c49f322bd3d71fea19c90241882_mcu_xiaomi.scooter.5pro_v0007.bin"
FW_PATH = _FW_LOCAL if _FW_LOCAL.exists() else ROOT / "tests" / "fixtures" / "mcu_0007.bin"
LIVE_UID = bytes.fromhex("4a77555935567448353632797064474f")
LIVE_KEY_01_10 = bytes.fromhex("7049273de6bd8383fbf33c3a128eb946")


# --------------------------------------------------------------------------
# push frames
# --------------------------------------------------------------------------

def make_push(sub, payload, chk=None):
    """61 SUB LEN DATA CHK 9E; CHK = sum(preceding bytes) & 0xFF."""
    body = bytes([0x61, sub, len(payload)]) + payload
    c = (sum(body) & 0xFF) if chk is None else chk
    return body + bytes([c, 0x9E])


PUSH_30 = make_push(0x30, bytes.fromhex("0300881aa81000000000"))
PUSH_31 = make_push(0x31, bytes.fromhex("9b62cdcb8000190000"))


# Traps: validly structured frames carrying CHK 0x06 / 0x15
def push_with_chk(sub, base_payload, want):
    p = bytearray(base_payload)
    head = sum(bytes([0x61, sub, len(p)])) + sum(bytes(p[:-1]))
    p[-1] = (want - head) & 0xFF
    return make_push(sub, bytes(p), chk=want)


PUSH_ACK_TRAP = push_with_chk(0x30, bytes.fromhex("0300881aa81000000000"), 0x06)
PUSH_CRC_TRAP = push_with_chk(0x31, bytes.fromhex("9b62cdcb8000190000"), 0x15)

for _f in (PUSH_30, PUSH_31, PUSH_ACK_TRAP, PUSH_CRC_TRAP):
    assert _f[-1] == 0x9E and len(_f) == 5 + _f[2]
    assert sum(_f[:-2]) & 0xFF == _f[-2]


# --------------------------------------------------------------------------
# MCU-side model
# --------------------------------------------------------------------------

class McuEmulator:
    """Responds on DFU console simulating live MCU behavior."""

    def __init__(self, fw, delay=0.002):
        self.fw = fw
        self.delay = delay
        self.uid = LIVE_UID
        self.rx = queue.Queue()
        self.tx_log = bytearray()
        self.text_buf = bytearray()
        self.mcu_rand = bytes(random.randrange(256) for _ in range(16))

        # write records
        self.nvm_locs = []
        self.chunks = {}          # loc -> {n: data}
        self.chunk_sends = 0      # total chunk transmissions (for deterministic retries)
        self.wr_infos = []        # (count, crc32, size)
        self.confirmations = 0
        self.dfu_verify_calls = 0
        self.dfu_active_calls = 0
        self.get_ver_calls = 0
        self.ble_rand_val = None
        self.mcu_key_val = None
        self.rebooted = False
        self.silent_active = False  # dfu_active without 'ok' (reboot before reply)
        self._stop = threading.Event()
        self._push_thread = None

    # -- device -> script
    def _emit(self, data, split_at=None):
        """Enqueue bytes; split_at splits frame in two parts."""
        if split_at is not None and 0 < split_at < len(data):
            self.rx.put(data[:split_at])
            time.sleep(0.01)   # pause so fragment is held back
            self.rx.put(data[split_at:])
        else:
            self.rx.put(data)

    def _respond(self, data, delay=None):
        time.sleep(delay if delay is not None else self.delay)
        self._emit(data)

    # -- push stream (continuous, with CHK traps)
    def start_pushes(self, interval=0.03):
        traps = [PUSH_30, PUSH_31, PUSH_ACK_TRAP, PUSH_CRC_TRAP]
        i = 0

        def loop():
            nonlocal i
            while not self._stop.is_set():
                d = traps[i % len(traps)]
                i += 1
                self._emit(d)
                time.sleep(interval)

        self._push_thread = threading.Thread(target=loop, daemon=True)
        self._push_thread.start()

    def stop(self):
        self._stop.set()

    # -- script -> device
    def on_write(self, data):
        self.tx_log += data
        if data == bytes.fromhex("532a7dac"):
            self._respond(bytes([0x64, 0x2A, 0x10]) + self.uid +
                          bytes([(sum([0x64, 0x2A, 0x10]) + sum(self.uid)) & 0xFF], ) + b"\x9b")
            return
        if len(data) == 3 and data == b"\x04\x04\x04":
            self.confirmations += 1
            self._respond(b"\x06")
            return
        if len(data) == 133 and data[0] == 0x01:
            self._on_chunk(data)
            return
        # text: buffer until \r
        self.text_buf += data
        while True:
            line = None
            for prefix, n_raw in ((b"down ble_rand ", 16), (b"down mcu_key ", 16)):
                if self.text_buf.startswith(prefix):
                    need = len(prefix) + n_raw + 1  # + trailing \r
                    if len(self.text_buf) < need:
                        return
                    line = bytes(self.text_buf[:len(prefix) + n_raw])  # without \r
                    self.text_buf = self.text_buf[need:]
                    break
            if line is None:
                if b"\r" not in self.text_buf:
                    return
                line, self.text_buf = self.text_buf.split(b"\r", 1)
            while self.text_buf.startswith(b"\x00"):
                del self.text_buf[0]
            self._on_text(bytes(line))

    def _on_chunk(self, frame):
        n = frame[1]
        assert frame[2] == 0xFF - n
        data, crc = frame[3:-2], binascii.crc_hqx(frame[3:-2], 0)
        assert crc == (frame[-2] << 8) | frame[-1], "chunk CRC mismatch"
        loc = self.nvm_locs[-1]
        first_send = loc not in self.chunks or n not in self.chunks[loc]
        self.chunks.setdefault(loc, {})[n] = data
        # retry path: every 97th chunk is silent on FIRST transmission, responds upon retry
        if first_send and self.chunk_sends % 97 == 0:
            self.chunk_sends += 1
            return
        self.chunk_sends += 1
        self._respond(b"\x06")

    def _on_text(self, line):
        if line == b"down get_ver":
            self.get_ver_calls += 1
            if self.rebooted:
                time.sleep(0.5)   # MCU reloading after reboot
            self._respond(b"007\r")
            return
        if line == b"down rd_info":
            self._respond(b"ok 0000 00000000 00000\r")
            return
        if line.startswith(b"down ble_rand "):
            self.ble_rand_val = line[14:]
            key = sign_rand(self.uid, self.ble_rand_val, self.fw, muf.OFF0_DEFAULT, muf.OFF1_DEFAULT)
            self._respond(b"ok " + key + b"\r")
            return
        if line == b"down mcu_rand":
            self._respond(b"ok " + self.mcu_rand + b"\r")
            return
        if line.startswith(b"down mcu_key "):
            self.mcu_key_val = line[13:]
            key = sign_rand(self.uid, self.mcu_rand, self.fw, muf.OFF0_DEFAULT, muf.OFF1_DEFAULT)
            assert self.mcu_key_val == key, "mcu_key mismatch"
            self._respond(b"ok\r")
            return
        if line.startswith(b"down nvm_write "):
            loc = int(line[15:], 16)
            self.nvm_locs.append(loc)
            self._respond(b"ok\r")
            return
        if line.startswith(b"down wr_info "):
            parts = line[13:].split(b" ")
            count, crc, size = int(parts[0]), parts[1].decode(), int(parts[2])
            sent = bytearray()
            for L in sorted(self.chunks):
                for n in range(1, 17):
                    sent += self.chunks[L][n]
            expect = format(zlib.crc32(bytes(sent)) & 0xFFFFFFFF, "08x")
            assert crc == expect, f"wr_info CRC {crc} != {expect}"
            assert size == count * 0x800
            self.wr_infos.append((count, crc, size))
            self._respond(b"ok\r")
            return
        if line == b"down dfu_verify":
            self.dfu_verify_calls += 1
            if self.dfu_verify_calls == 1:
                return  # first reply empty, matching live log
            self._respond(b"ok\r")
            return
        if line == b"down dfu_active":
            self.dfu_active_calls += 1
            if not self.silent_active:
                self._respond(b"ok\r")
            time.sleep(0.2)
            self.rebooted = True
            self._emit(b"\x43")
            return
        raise AssertionError(f"unknown command: {line!r}")


class MockSerial:
    """pyserial-compatible wrapper over McuEmulator."""

    def __init__(self, emu, *args, **kwargs):
        self.emu = emu
        self.pending = bytearray()

    def write(self, data):
        self.emu.on_write(bytes(data))
        return len(data)

    def read(self, n=1):
        if not self.pending:
            try:
                self.pending += self.emu.rx.get(timeout=0.05)
            except queue.Empty:
                return b""
        d = bytes(self.pending[:n])
        del self.pending[:n]
        return d

    def flush(self):
        pass

    def close(self):
        self.emu.stop()

    def reset_input_buffer(self):
        pytest.fail("reset_input_buffer forbidden (splits push-frame in half)")


# --------------------------------------------------------------------------
# tests
# --------------------------------------------------------------------------

def test_reader_filters_valid_pushes_and_retains_clean():
    class FakeS:
        def __init__(self, data):
            self.data = bytearray(data)

        def read(self, n):
            d = bytes(self.data[:n])
            del self.data[:n]
            return d

    # full valid frame + reply
    s = FakeS(PUSH_30 + b"ok 1234\r" + PUSH_31)
    r = muf.Reader(s)
    assert r.read_until(b"\r") == b"ok 1234\r"

    # frame with bad CHK — not discarded (bytes retained as data)
    bad_push = bytes([0x61, 0x30, 0x02, 0x11, 0x22, 0x00, 0x9E])  # CHK 0x00 != real
    s = FakeS(bad_push + b"\r")
    r = muf.Reader(s)
    assert r.read_until(b"\r") == bad_push + b"\r"

    # incomplete trailing frame held back
    s = FakeS(PUSH_30[:8])
    r = muf.Reader(s)
    r._pump()
    assert bytes(r.clean) == b""

    # ...and confirmed when remainder arrives
    s.data += PUSH_30[8:] + b"done\r"
    assert r.read_until(b"\r") == b"done\r"


def _run_flash(capsys, silent_active=False):
    """Run mcu_uart_flash.main() against emulator; return (emu, out)."""
    fw = FW_PATH.read_bytes()
    emu = McuEmulator(fw)
    emu.silent_active = silent_active
    old_serial = muf.serial.Serial
    muf.serial.Serial = lambda *a, **k: MockSerial(emu)
    try:
        emu.start_pushes(interval=0.03)
        argv = ["mcu_uart_flash.py", "--port", "MOCK", "--fw", str(FW_PATH),
                "--md5", "c0f78c49f322bd3d71fea19c90241882", "--yes"]
        sys.argv = argv
        muf.main()
    finally:
        muf.serial.Serial = old_serial
        emu.stop()
    return emu, capsys.readouterr().out, fw


def _assert_write_flow(emu, out, fw):
    # -- handshake
    assert emu.get_ver_calls >= 2          # warmup + explicit get_ver (+ post-check)
    assert emu.ble_rand_val is not None and len(emu.ble_rand_val) == 16
    assert emu.mcu_key_val is not None

    # -- packets: 74 real + 1 terminating empty
    n = -(-len(fw) // muf.PACKET_SIZE)
    expect_locs = [i * muf.PACKET_SIZE for i in range(n + 1)]
    assert emu.nvm_locs == expect_locs, "nvm_write sequence incorrect"

    # -- chunks: all 74x16, data = image (last packet padded with 0xFF)
    assert len(emu.chunks) == n
    reassembled = bytearray()
    for i in range(n):
        loc = i * muf.PACKET_SIZE
        for c in range(1, 17):
            reassembled += emu.chunks[loc][c]
    assert bytes(reassembled[:len(fw)]) == fw
    assert all(b == 0xFF for b in reassembled[len(fw):])

    # -- confirmations and wr_info: count matches packets + 1 terminating
    assert emu.confirmations == n + 1
    assert len(emu.wr_infos) == n + 1
    assert emu.wr_infos[0][1] == "a7dfe686"      # anchor from live log
    assert emu.wr_infos[-1][1] == emu.wr_infos[-2][1] == "77f34c63"  # terminating: CRC unchanged
    assert [w[0] for w in emu.wr_infos] == list(range(1, n + 2))

    # -- verify/active
    assert emu.dfu_verify_calls == 2             # first reply was empty
    assert emu.dfu_active_calls == 1

    # -- summary
    assert "version AFTER: '007'" in out
    assert "dfu_verify: OK" in out
    assert "ABORT" not in out


def test_full_flash_flow(capsys):
    emu, out, fw = _run_flash(capsys)
    _assert_write_flow(emu, out, fw)


def test_full_flash_flow_silent_active(capsys):
    """Live scenario 2026-08-22: 'ok' on dfu_active lost in reboot.

    Script performs read-only check: version returned + DFU region cleared (rd_info)
    and treats activation as committed.
    """
    emu, out, fw = _run_flash(capsys, silent_active=True)
    _assert_write_flow(emu, out, fw)
    assert "checking reboot and DFU region state" in out
    assert "considering activation committed" in out
    # -- handshake
    assert emu.get_ver_calls >= 2
    assert emu.ble_rand_val is not None and len(emu.ble_rand_val) == 16
    assert emu.mcu_key_val is not None

    # -- packets: 74 real + 1 terminating empty
    n = -(-len(fw) // muf.PACKET_SIZE)
    expect_locs = [i * muf.PACKET_SIZE for i in range(n + 1)]
    assert emu.nvm_locs == expect_locs, "nvm_write sequence incorrect"

    # -- chunks: all 74x16
    assert len(emu.chunks) == n
    reassembled = bytearray()
    for i in range(n):
        loc = i * muf.PACKET_SIZE
        for c in range(1, 17):
            reassembled += emu.chunks[loc][c]
    assert bytes(reassembled[:len(fw)]) == fw
    assert all(b == 0xFF for b in reassembled[len(fw):])

    # -- confirmations and wr_info
    assert emu.confirmations == n + 1
    assert len(emu.wr_infos) == n + 1
    assert emu.wr_infos[0][1] == "a7dfe686"
    assert emu.wr_infos[-1][1] == emu.wr_infos[-2][1] == "77f34c63"
    assert [w[0] for w in emu.wr_infos] == list(range(1, n + 2))

    # -- verify/active
    assert emu.dfu_verify_calls == 2
    assert emu.dfu_active_calls == 1

    # -- summary
    assert "version AFTER: '007'" in out
    assert "dfu_verify: OK" in out
    assert "ABORT" not in out


if __name__ == "__main__":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.exit(pytest.main([__file__, "-v", "-s"]))
