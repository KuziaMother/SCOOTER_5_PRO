#!/usr/bin/env python3
"""UART-DFU flasher for MCU (bw-flasher protocol, verified on physical MCU 2026-08-21/22).

Phases: UID -> get_ver -> rd_info -> ble_rand (+ sign_rand check) -> mcu_rand ->
mcu_key -> [nvm_write + 16x chunk (128B) + 04 04 04 + wr_info] x N packets (0x800) ->
**terminating empty packet** (nvm_write + 04 04 04 + wr_info, without chunks) ->
dfu_verify -> dfu_active -> get_ver.

Protocol reference: official `bw-flasher` (ScooterTeam), whose complete write flow
succeeded on real hardware 2026-08-21 (log: logs/bw_flasher_log.txt). This script reproduces
its exact sequence byte-for-byte, including the terminating empty packet after the
last real packet: the reference state-machine transmits it (nvm_write at image tail,
no chunks, 04 04 04 + ACK, wr_info with UNCHANGED CRC32 and size (N+1)*0x800),
followed by dfu_verify — accepted by MCU.

Critical considerations (live findings):
  - UID responds reliably ONLY if preceded by `down get_ver\r` and a 0.4 s pause
    before sending the raw `53 2A 7D AC` frame; raw hex immediately after opening
    the port may receive no response (todo.md §B2).
  - `nvm_write` must be sent IMMEDIATELY after `ok` from mcu_key — MCU has a narrow
    "write window" after authentication; ~2 s delay leads to silence and session
    hang (recoverable only via power-cycle).
  - Telemetry push frames (`61 SUB LEN DATA CHK 9E`, CHK = sum & 0xFF, ~2.5 s /
    up to continuous stream) arrive concurrently with console traffic. They are filtered
    out after CHK validation; an INCOMPLETE trailing frame is held back rather than
    passed to the parser (preventing 0x06/0x15 in push payloads from triggering false ACK/CRC-fail).
    Synchronization is persistent: reset_input_buffer() is NOT used — it cuts frames
    in half, and the orphaned fragment corrupts startswith(b"ok").
  - After dfu_active the MCU reboots: get_ver may take several seconds to respond.
    Live run 2026-08-22: `ok` response to dfu_active MAY be lost — MCU committed
    activation and reset before replying. The script then executes a read-only check:
    version returned + rd_info shows cleared DFU region = activation committed;
    data still present in DFU region = ABORT "retry needed".

Safety: prior to dfu_active any error triggers ABORT (active firmware untouched);
chunks without ACK 0x06 are retried up to 20 times (retransmissions observed in live successful
runs); ACK 0x15 = CRC-fail -> ABORT. Retries are bounded to avoid flooding device.

Usage: python tools/mcu_uart_flash.py --port COM3 --fw firmware_ota/<mcu>.bin --md5 <hex>
"""
import argparse
import hashlib
import random
import re
import struct
import sys
import time
import zlib

import serial

from mcu_keygen import sign_rand  # vendored from bw-flasher (CC BY-NC-SA, see file)

PACKET_SIZE = 0x800
CHUNK_SIZE = 0x80
CHUNKS_PER_PACKET = PACKET_SIZE // CHUNK_SIZE   # 16
MAX_REPEATS = 20
# Verified fallback constants for v0007 (docs/FACTS.md); primary path is
# dynamic pattern scanning in image (matching bw-flasher).
OFF0_DEFAULT, OFF1_DEFAULT = 0x24187, 0x24387

# Version starts with a digit (stray bytes on reboot, e.g. 0x43='C', are skipped)
VER_RE = re.compile(rb"^[0-9]+([._][0-9A-Za-z]+)*$")


def crc16_xmodem(data):
    crc = 0
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}"
          .replace("✓", "OK").replace("…", "..."), flush=True)


class Reader:
    """Port reader with persistent synchronization and filtering of `61 SUB LEN DATA CHK 9E` push frames.

    Two buffers: raw (unclassified bytes) and clean (console bytes pending caller
    consumption). Complete push frames are discarded ONLY upon valid CHK (sum of preceding
    bytes & 0xFF) and 0x9E trailer; incomplete trailing frames are held in raw until
    sufficient data arrives to confirm or reject them.

    Known limitation: if a console byte (ACK 0x06/0x15) physically arrives IN THE MIDDLE
    of a split push frame, frame validation fails and all bytes (including ACK) enter
    clean as data. No such interleaving has been observed in live captures (push stream
    is quiet during write phase, see logs/bw_flasher_log.txt).
    """

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
        """Split raw into (discarded valid push frames) + clean; hold back incomplete tail."""
        out = bytearray()
        i, n = 0, len(self.raw)
        while i < n:
            b = self.raw[i]
            if b == 0x61:
                rem = n - i
                if rem < 3:
                    break  # potential frame start — awaiting more bytes
                ln = self.raw[i + 2]
                e = i + ln + 5  # index right after 9E trailer
                if ln <= 200 and e <= n and self.raw[e - 1] == 0x9E \
                        and (sum(self.raw[i:e - 2]) & 0xFF) == self.raw[e - 2]:
                    i = e       # complete valid push frame — discard
                    continue
                if ln <= 200 and e > n:
                    break       # potential incomplete frame — hold back
            out.append(b)
            i += 1
        del self.raw[:i]
        self.clean += out

    def read_until(self, term, timeout=3.0):
        """Read bytes up to and including `term`; on timeout, return all available bytes."""
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

    def read_exact(self, n, timeout=3.0):
        """Read exactly n bytes (binary reply); on timeout, return whatever accumulated."""
        end = time.time() + timeout
        while len(self.clean) < n and time.time() < end:
            self._pump()
        d = bytes(self.clean[:n])
        del self.clean[:len(d)]
        return d


def cmd(r, payload, label, timeout=3.0, fatal=True):
    """Drain -> send -> await line until \\r. Returns line without \\r (or None)."""
    r.drain()
    r.s.write(payload)
    r.s.flush()
    d = r.read_until(b"\r", timeout=timeout)
    if not d.endswith(b"\r"):
        if not fatal:
            return None
        log(f"RAW {label}: {d[:64].hex(' ')}")
        sys.exit(f"ABORT: {label}: no response (console hung — power-cycle "
                 f"and wait ~3 min before retry)")
    line = d.split(b"\r")[0]
    if not line:
        if not fatal:
            return None
        log(f"RAW {label}: {d[:64].hex(' ')}")
        sys.exit(f"ABORT: {label}: empty response")
    return line


def ok_cmd(r, payload, label, timeout=3.0):
    """Command that must return `ok` (optionally with trailing data)."""
    line = cmd(r, payload, label, timeout)
    if not line.startswith(b"ok"):
        sys.exit(f"ABORT: {label}: unexpected response {line[:24]!r}")
    return line


def find_offsets(fw):
    """Locate crypto table offsets in image (matching bw-flasher).

    S-box is identified by unique pattern `63 7C`; GF(2^8) power table is the first
    `01 02` following it (off1 = hit - 1). Fallback to v0007 constants from docs/FACTS.md
    if matches are ambiguous.
    """
    hits0, start = [], 0
    while True:
        i = fw.find(b"\x63\x7c", start)
        if i < 0:
            break
        hits0.append(i)
        start = i + 1
    if len(hits0) == 1:
        off0 = hits0[0]
    else:
        off0 = OFF0_DEFAULT
        log(f"WARNING: pattern 637C found {len(hits0)} times — "
            f"using verified fallback off0=0x{off0:X}")
    hits1, start = [], off0
    while True:
        i = fw.find(b"\x01\x02", start)
        if i < 0:
            break
        hits1.append(i)
        start = i + 1
    if len(hits1) == 1:
        off1 = hits1[0] - 1
    else:
        off1 = OFF1_DEFAULT
        log(f"WARNING: pattern 0102 after off0 found {len(hits1)} times — "
            f"using verified fallback off1=0x{off1:X}")
    return off0, off1


def get_uid(r):
    """Query UID with warmup (live finding 2026-08-21): `down get_ver\r`, 0.4 s pause, then hex frame."""
    for attempt in range(1, 4):
        r.drain()
        r.s.write(b"down get_ver\r")
        r.s.flush()
        time.sleep(0.4)          # warmup pause
        r.drain()                # consume "0007\r" response if present
        r.s.write(bytes.fromhex("53 2A 7D AC"))
        r.s.flush()
        acc = bytearray()
        end = time.time() + 2.0
        while True:
            # accumulate up to 9B trailer (or chunk timeout); validate frame as whole
            acc += r.read_until(b"\x9b", timeout=max(0.1, end - time.time()))
            i = acc.find(b"\x64\x2a\x10")
            if i >= 0 and i + 21 <= len(acc) and acc[i + 20] == 0x9B \
                    and (sum(acc[i:i + 19]) & 0xFF) == acc[i + 19]:
                return bytes(acc[i + 3:i + 19])
            if time.time() >= end:
                break
        log(f"UID attempt {attempt}/3 — no response")
    sys.exit("ABORT: UID not received (check line/TX)")


def get_ver(r, label="get_ver", timeout=3.0, tries=6, fatal=True):
    """Send `down get_ver` -> version string; noise (push tails) lines are retried."""
    for _ in range(tries):
        line = cmd(r, b"down get_ver\r", label, timeout, fatal=fatal)
        if line is None:
            continue
        if VER_RE.match(line):
            return line.decode()
        log(f"{label}: noise line {line[:16]!r} — retrying")
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM3")
    ap.add_argument("--fw", required=True)
    ap.add_argument("--md5", default="", help="expected MD5 (required for writing)")
    ap.add_argument("--yes", action="store_true", help="confirm write operation")
    a = ap.parse_args()

    fw = open(a.fw, "rb").read()
    md5 = hashlib.md5(fw).hexdigest()
    log(f"image: {a.fw} ({len(fw)} B), MD5={md5}")
    if not a.md5 or a.md5.lower() != md5:
        sys.exit("ABORT: specify --md5 matching image MD5 (safety check)")

    off0, off1 = find_offsets(fw)
    log(f"crypto tables: off0=0x{off0:X}, off1=0x{off1:X}")

    n_packets = -(-len(fw) // PACKET_SIZE)
    log(f"packets: {n_packets} (+1 terminating empty), "
        f"chunks: {n_packets * CHUNKS_PER_PACKET}")

    s = serial.Serial(a.port, 19200, timeout=0.2)
    time.sleep(0.3)
    r = Reader(s)
    r.drain()

    # --- 1) UID (up to 3 attempts with warmup) ---
    uid = get_uid(r)
    log(f"UID: {uid[:4].hex()}...{uid[-2:].hex()}")

    # --- 2) get_ver ---
    ver_before = get_ver(r, "get_ver", fatal=True)
    if ver_before is None:
        sys.exit("ABORT: get_ver: no valid version before flash")
    log(f"version BEFORE: {ver_before!r}")

    # --- 3) rd_info ---
    line = ok_cmd(r, b"down rd_info\r\x00\x00\x00", "rd_info")
    log(f"rd_info: {line[:40]!r}")

    # --- 4) ble_rand + crypto verification ---
    # Raw bytes in \r-delimited channel are length-checked by MCU:
    # "ok " + key(16) + "\r" = 20 B.
    rand = bytes(random.randrange(256) for _ in range(16))
    r.drain()
    r.s.write(b"down ble_rand " + rand + b"\r")
    r.s.flush()
    resp = r.read_exact(20, timeout=3.0)
    mcu_key = resp[3:19]
    if len(mcu_key) < 16 or not resp.startswith(b"ok ") or resp[-1:] != b"\r":
        sys.exit(f"ABORT: ble_rand: short or invalid response {resp[:24]!r}")
    local_key = sign_rand(uid, rand, fw, off0, off1)
    if mcu_key != local_key:
        sys.exit("ABORT: sign_rand MISMATCH with MCU (wrong image or UID)")
    log("ble_rand: crypto MATCHED ✓")

    # --- 5) mcu_rand ---
    r.drain()
    r.s.write(b"down mcu_rand\r")
    r.s.flush()
    resp = r.read_exact(20, timeout=3.0)   # "ok " + rand(16) + "\r"
    mcu_rand = resp[3:19]
    if len(mcu_rand) < 16 or not resp.startswith(b"ok ") or resp[-1:] != b"\r":
        sys.exit(f"ABORT: mcu_rand: short or invalid response {resp[:24]!r}")
    log(f"mcu_rand: {mcu_rand[:4].hex()}...")

    # --- 6) mcu_key -> IMMEDIATE nvm_write (write window!) ---
    key = sign_rand(uid, mcu_rand, fw, off0, off1)
    ok_cmd(r, b"down mcu_key " + key + b"\r", "mcu_key")
    log("mcu_key: accepted ✓ — starting write (no delay)")

    # --- 7) packets ---
    data_sent = bytearray()
    t_start = time.time()
    for p in range(n_packets):
        loc = p * PACKET_SIZE
        ok_cmd(r, f"down nvm_write {loc:08X}\r".encode(),
               f"nvm_write @{loc:08X}", timeout=3.0)

        packet = fw[loc:loc + PACKET_SIZE]
        if len(packet) < PACKET_SIZE:
            packet += b"\xFF" * (PACKET_SIZE - len(packet))
        for n in range(CHUNKS_PER_PACKET):
            chunk = packet[n * CHUNK_SIZE:(n + 1) * CHUNK_SIZE]
            frame = b"\x01" + bytes([(n + 1), 0xFF - (n + 1)]) + chunk \
                + struct.pack(">H", crc16_xmodem(chunk))
            acked = False
            for _rep in range(MAX_REPEATS):
                r.drain()
                s.write(frame)
                s.flush()
                d = r.read_until(b"\x06", timeout=1.0)
                if b"\x15" in d:
                    sys.exit(f"ABORT: CRC-fail chunk p={p} n={n + 1}")
                if b"\x06" in d:
                    acked = True
                    break
            if not acked:
                sys.exit(f"ABORT: chunk p={p} n={n + 1} — no ACK after {MAX_REPEATS} attempts")
            data_sent += chunk
        # packet confirmation (non-fatal, matching reference)
        s.write(b"\x04\x04\x04")
        s.flush()
        r.read_until(b"\x06", timeout=2.0)

        crc32 = zlib.crc32(bytes(data_sent)) & 0xFFFFFFFF
        ok_cmd(r, f"down wr_info {p + 1} {crc32:08x} {(p + 1) * PACKET_SIZE}\r".encode(),
               f"wr_info p={p + 1}")
        el = time.time() - t_start
        rate = (p + 1) / el * 100 / n_packets
        eta = (n_packets - p - 1) / max(el / (p + 1), 0.01)
        log(f"packet {p + 1}/{n_packets} ok ({rate:.0f}%, ETA ~{eta:.0f} s)")

    # --- 7b) terminating empty packet (matching verified live run) ---
    loc = n_packets * PACKET_SIZE
    ok_cmd(r, f"down nvm_write {loc:08X}\r".encode(), "nvm_write (terminating)",
           timeout=3.0)
    s.write(b"\x04\x04\x04")
    s.flush()
    r.read_until(b"\x06", timeout=2.0)
    crc32 = zlib.crc32(bytes(data_sent)) & 0xFFFFFFFF
    ok_cmd(r, f"down wr_info {n_packets + 1} {crc32:08x} {(n_packets + 1) * PACKET_SIZE}\r".encode(),
           "wr_info (terminating)")

    # --- 8) dfu_verify (up to 3 attempts, MCU may be busy on first) ---
    line = None
    for _ in range(3):
        line = cmd(r, b"down dfu_verify\r", "dfu_verify", timeout=5.0, fatal=False)
        if line is not None:
            break
    if line is None or not line.startswith(b"ok"):
        sys.exit(f"ABORT: verify FAILED ({line!r}) — firmware NOT switched")
    log("dfu_verify: OK")

    # --- 9) dfu_active (irreversible step) ---
    log(">>> dfu_active — switching firmware...")
    line = cmd(r, b"down dfu_active\r", "dfu_active", timeout=5.0, fatal=False)
    active_ok = line is not None and line.startswith(b"ok")
    if line is not None and not active_ok:
        sys.exit(f"ABORT: dfu_active: {line!r}")
    if active_ok:
        log("dfu_active: OK — MCU rebooting")

    # --- 10) post-check (MCU rebooting — multiple attempts) ---
    time.sleep(3)
    ver_after = get_ver(r, "get_ver#after", timeout=3.0, tries=8, fatal=False)
    if not active_ok:
        # No reply to active. Live run 2026-08-22: MCU committed and rebooted
        # before replying with 'ok'. Discriminator (read-only): rd_info after reboot.
        log("dfu_active: no response — checking reboot and DFU region state...")
        time.sleep(5)
        ver_after = get_ver(r, "get_ver#after", timeout=3.0, tries=8, fatal=False)
        if ver_after is None:
            sys.exit("ABORT: dfu_active unconfirmed and console did not return — check device")
        r.drain()
        s.write(b"down rd_info\r\x00\x00\x00")
        s.flush()
        d = r.read_until(b"\r", timeout=3.0)
        rd = d.split(b"\r")[0] if d.endswith(b"\r") else b""
        region_cleared = bool(re.match(rb"^ok 0000 00000000 [0-9A-Fa-f]*$", rd))
        log(f"rd_info after: {rd!r}")
        if not region_cleared:
            sys.exit("ABORT: activation NOT committed (data still in DFU region) — retry needed")
        log("dfu_active: ok not received, but MCU rebooted and DFU region cleared — "
            "considering activation committed")
    # push telemetry stream — verify MCU is active
    end = time.time() + 3.0
    raw = bytearray()
    while time.time() < end:
        raw += s.read(4096)
    n61 = raw.count(b"\x61\x30") + raw.count(b"\x61\x31")
    log(f"version AFTER: {ver_after!r}")
    log(f"push stream after: {n61} frames in 3 s {'OK' if n61 > 5 else '- CHECK LINE!'}")
    log(f"Done. Total flash time: {time.time() - t_start:.0f} s")
    s.close()
    if ver_after is None:
        sys.exit("WARNING: dfu_active accepted, but console did not return — check device (version/behavior)")


if __name__ == "__main__":
    main()
