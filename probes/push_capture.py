#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Live capture of property pushes (TODO B "Live push capture").

Single session scenario (Mi Home parallel connection not needed):
  1. connect + login
  2. baseline: 2.4 TAIL_LIGHT, 2.2 IS_LOCKED, 1.1 RIDING_MODE
  3. SET 2.4=1 (tail light ON)  -> wait push
  4. SET 2.4=0 (light OFF)      -> wait push
  5. (optional --lock) SET 2.2=1/0 -> push IS_LOCKED

All 0x001b notifications decrypted and logged: logs/push_capture_<ts>.log

SET format: op=0, element [u8 siid][u16 piid][u16 (type<<12)|vlen][value].
Standard controllable properties only (light/lock), nothing destructive.

Usage:  python probes/push_capture.py [--no-light] [--lock] [--hold 5]
"""
import argparse
import asyncio
import contextlib
import io
import os as _os
import struct
import sys as _sys
from datetime import datetime

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
_sys.path.insert(0, _os.path.join(_ROOT, "core"))
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import dreame_auth as da
import spec_read as sr

CH_WRITE = 0x001A
CH_NOTIFY = 0x001B


def build_set(obj, value, vtype, tid=2):
    """SET frame: op=0, single element with value."""
    s, p = obj
    body = struct.pack("<BHH", s & 0xFF, p & 0xFFFF, (vtype & 0xF) << 12 | len(value)) + value
    total = 6 + len(body)
    return struct.pack("<HHBB", (total | 0x2000) & 0xFFFF, tid & 0xFFFF, 0, 1) + body


class PushWatcher:
    """Decrypts and prints ALL 0x001b notifications from transport queue."""

    def __init__(self, t, sk):
        self.t = t
        self.sk = sk
        self.count = 0

    async def run(self, timeout):
        loop = asyncio.get_event_loop()
        deadline = loop.time() + timeout
        while loop.time() < deadline:
            try:
                s, b = await asyncio.wait_for(self.t.rx.get(), timeout=deadline - loop.time())
            except asyncio.TimeoutError:
                break
            if s != CH_NOTIFY:
                continue
            pt = self._try_decode(b)
            if pt is None:
                print(f"  [notify {s:#06x}] unencrypted/transport: {b[:12].hex()}")
                continue
            self.count += 1
            tag = f"PUSH #{self.count}"
            print(f"  >>> {tag}: {pt.hex()}")
            for line in sr.parse_reply(pt):
                print("      " + line)
        return self.count

    def _try_decode(self, b):
        # transport: [u16 counter] + CCM ciphertext (dev key) — like GET response
        if len(b) < 6:
            return None
        try:
            cnt = struct.unpack("<H", b[:2])[0]
            return sr.dec_dev(self.sk, cnt, b[2:])
        except Exception:
            # transport ACK/CTR — not target format
            return None


async def do_read(t, sk, obj, app_cnt):
    pt = await sr.spec_request(t, sk, [obj], app_cnt)
    if pt:
        for line in sr.parse_reply(pt):
            print("   " + line)
    return app_cnt + 1


async def do_set(t, sk, obj, value, vtype, app_cnt):
    name = sr.NAMES.get(obj, f"{obj[0]}.{obj[1]}")
    print(f"=== SET {name} = {value} (app_cnt={app_cnt}) ===")
    payload = sr.enc_app(sk, app_cnt, build_set(obj, value, vtype))
    frames = [payload[i:i + 18] for i in range(0, len(payload), 18)] or [b""]
    while not t.rx.empty():
        t.rx.get_nowait()
    await t.write(CH_WRITE, struct.pack("<HBBH", 0, 0x00, 0, len(frames)))

    async def send_seq(n):
        if 1 <= n <= len(frames):
            await t.write(CH_WRITE, struct.pack("<H", n) + frames[n - 1])

    loop = asyncio.get_event_loop()
    deadline = loop.time() + 6.0
    sent_all = False
    while loop.time() < deadline:
        try:
            s, b = await asyncio.wait_for(t.rx.get(), timeout=deadline - loop.time())
        except asyncio.TimeoutError:
            break
        if len(b) >= 3 and b[0] == 0 and b[1] == 0 and b[2] == 0x01:
            st = b[3] if len(b) > 3 else None
            if st == 0x01 and not sent_all:
                sent_all = True
                for n in range(1, len(frames) + 1):
                    await send_seq(n)
                    await asyncio.sleep(0.03)
            elif st == 0x05:
                seqs = [struct.unpack_from("<H", b, 4 + i)[0]
                        for i in range(0, len(b) - 4, 2)]
                for n in seqs:
                    await send_seq(n)
                    await asyncio.sleep(0.03)
            elif st == 0x00:
                print("   request accepted (ACK 00), waiting for device reply...")
                # reply via CTR stream on CH_NOTIFY (as in spec_request)
                rdl = loop.time() + 6.0
                got_ctr = False
                while loop.time() < rdl:
                    try:
                        s2, b2 = await asyncio.wait_for(t.rx.get(),
                                                        timeout=rdl - loop.time())
                    except asyncio.TimeoutError:
                        break
                    if (s2 == CH_NOTIFY and len(b2) >= 6 and b2[0] == 0 and b2[1] == 0
                            and b2[2] == 0 and not got_ctr):
                        fc = struct.unpack("<H", b2[4:6])[0]
                        await t.write(CH_NOTIFY, struct.pack("<HBB", 0, 0x01, 0x01))
                        parts = {}
                        while len(parts) < fc and loop.time() < rdl:
                            try:
                                s3, b3 = await asyncio.wait_for(t.rx.get(),
                                                                timeout=rdl - loop.time())
                            except asyncio.TimeoutError:
                                break
                            if s3 == CH_NOTIFY and len(b3) >= 2:
                                seq = struct.unpack("<H", b3[:2])[0]
                                if 1 <= seq <= fc:
                                    parts[seq] = b3[2:]
                        await t.write(CH_NOTIFY, struct.pack("<HBB", 0, 0x01, 0x00))
                        if len(parts) == fc:
                            payload = b"".join(parts[i] for i in sorted(parts))
                            dev_cnt = struct.unpack("<H", payload[:2])[0]
                            try:
                                pt = sr.dec_dev(sk, dev_cnt, payload[2:])
                                print(f"   SET RESPONSE: {pt.hex()}")
                                for line in sr.parse_reply(pt):
                                    print("     " + line)
                            except Exception as e:
                                print(f"   [!] reply decryption failed: {e}")
                        break
                    # ignore other frames (late ACKs)
                return app_cnt + 1
    print("   [!] ACK for SET not received")
    return app_cnt + 1


async def run(mac, do_light=True, do_lock=False, hold=5):
    ltmk = bytes.fromhex(open(da.LTMK_HEX).read().strip())
    t = da.Transport(mac)
    try:
        await t.connect()
        if not await t.a4_handshake():
            print("[!] transport failed to connect")
            return 1
        for s, b in await t.drain(1.0):
            if s == da.CH_LOGIN and len(b) >= 3 and b[2] == da.PKT_MNG:
                await t.write(da.CH_LOGIN, struct.pack("<HBB", 0, da.PKT_MNG_ACK, 0)
                              + bytes([t.pkg_num, t.dmtu]))
        priv, dev_pub = await da.stage_a_pubkey_exchange(t)
        if not (dev_pub and len(dev_pub) >= 64):
            return 1
        if not await da.stage_b_confirm(t, priv, dev_pub, ltmk, crc_be=False):
            print("[!] login refused")
            return 1
        sk = da.LAST_SK
        print("\n[+] LOGIN OK\n")

        w = PushWatcher(t, sk)
        app_cnt = 0

        print("=== BASELINE ===")
        for obj in ((2, 4), (2, 2), (1, 1)):
            app_cnt = await do_read(t, sk, obj, app_cnt)
            await asyncio.sleep(0.2)

        async def set_and_watch(obj, value, label):
            nonlocal app_cnt
            app_cnt = await do_set(t, sk, obj, value, 0, app_cnt)
            print(f"   window {hold}s for push after: {label}")
            await asyncio.sleep(1.0)
            await w.run(hold)

        if do_light:
            print("\n=== SCENARIO: tail light (2.4 — outside push list) ===")
            await set_and_watch((2, 4), b"\x01", "light ON")
            await set_and_watch((2, 4), b"\x00", "light OFF")

        print("\n=== SCENARIO: ATMOSPHERE_LIGHT (2.16 — in push list) ===")
        await set_and_watch((2, 16), b"\x01", "atmo ON")
        await set_and_watch((2, 16), b"\x00", "atmo OFF")

        print("\n=== SCENARIO: TCS (2.13 — in push list) ===")
        # baseline 2.13 was 1; toggle and revert
        await set_and_watch((2, 13), b"\x00", "TCS OFF")
        await set_and_watch((2, 13), b"\x01", "TCS ON")

        if do_lock:
            print("\n=== SCENARIO: lock ===")
            await set_and_watch((2, 2), b"\x01", "LOCK ON")
            await set_and_watch((2, 2), b"\x00", "UNLOCK")

        print(f"\n=== pushes recorded: {w.count} ===")
        return 0 if w.count else 1
    except Exception:
        import traceback
        traceback.print_exc()
        return 1
    finally:
        await t.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mac", default=da.MAC_DEFAULT)
    ap.add_argument("--no-light", action="store_true")
    ap.add_argument("--lock", action="store_true")
    ap.add_argument("--hold", type=int, default=5)
    a = ap.parse_args()

    _os.makedirs(_os.path.join(_ROOT, "logs"), exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = _os.path.join(_ROOT, "logs", f"push_capture_{ts}.log")
    buf = io.StringIO()

    class Tee:
        def __init__(self, *ss):
            self.ss = ss

        def write(self, s):
            for st in self.ss:
                with contextlib.suppress(Exception):
                    st.write(s)

        def flush(self):
            for st in self.ss:
                with contextlib.suppress(Exception):
                    st.flush()

    fh = open(log_path, "w", encoding="utf-8")
    _sys.stdout = Tee(_sys.__stdout__, buf, fh)
    rc = asyncio.run(run(a.mac, do_light=not a.no_light, do_lock=a.lock, hold=a.hold))
    _sys.stdout.flush()
    fh.close()
    print(f"\n[log: {log_path}]")
    raise SystemExit(rc)
