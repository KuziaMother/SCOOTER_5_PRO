#!/usr/bin/env python3
"""
Listener for property change push notifications (MIoT-spec over BLE).

Subscription ALREADY active: `Transport.connect()` sets CCCD on ALL notify characteristics
FE95, including spec-notify `0x001b`. Verified via `spec_read.py` successfully
receiving replies on `0x001b` via this subscription. Push follows same notify path,
without preceding request on `0x001a`. (Plugin additionally invokes
`bt.subscribeMessages("prop.s.p", …)` — local JS callback routing,
topics, not a command to the device; see FACTS.md "Device can PUSH").

⚠️ Push arrives ONLY upon property CHANGES. On a stationary scooter with full charge,
nothing changes — silence alone proves nothing. To observe traffic, change state:
traffic, change state: press throttle, toggle light, roll scooter.

Device frame format is IDENTICAL to read response (spec_read.py):
  single:      [0000][02][00][counter u16 LE][ct]   -> ACK [0000][03][00]
  multiframe:  [0000][00][ch][fc]  -> we ACK 01 -> frames [seq u16][data] -> we ACK 00
Decryption: key=sk[0:16], iv=sk[32:36] (device keys), AES-CCM, tag 4 B.

READ-ONLY: writes nothing except required transport ACKs and optional baseline reads.

Run sequence:
  connect -> login -> [baseline: DEFAULT_SET before changes, property by property]
             -> pre-roll countdown -> listening window (change state!) -> summary.

Usage:
  python probes/spec_listen.py [--secs 120] [--pre 5] [--no-baseline] [--log PATH]
All console output is duplicated to log file (default logs/).
"""
import argparse
import asyncio
import contextlib
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

# Properties subscribed by plugin (modules/10013.js parseNotifyData):
# 1.1 1.2 1.4 1.5 1.6 1.7 1.8 1.9 2.1 2.7 2.13-2.18 3.1 3.2 3.4 3.10.
# Pushes expected for these only; others in notify marked as "outside list".
SUBSCRIBABLE = {
    (1, 1), (1, 2), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
    (2, 1), (2, 7), (2, 13), (2, 14), (2, 15), (2, 16), (2, 17), (2, 18),
    (3, 1), (3, 2), (3, 4), (3, 10),
}


class _Tee:
    """Duplicates output to console and log file."""
    def __init__(self, *streams):
        self.streams = streams

    def write(self, s):
        for st in self.streams:
            try:
                st.write(s)
            except Exception:
                pass

    def flush(self):
        for st in self.streams:
            try:
                st.flush()
            except Exception:
                pass


def parse_props(pt):
    """Parse spec frame: header + objects [siid][piid][status][tl][value]."""
    out = []
    if len(pt) < 6:
        return [("?", "?", None, f"short frame {pt.hex()}")]
    lenflag, tid, op, count = struct.unpack("<HHBB", pt[:6])
    off = 6
    for _ in range(count):
        if off + 7 > len(pt):
            break
        siid, piid, status, tl = struct.unpack("<BHHH", pt[off:off + 7])
        tcode, vlen = tl >> 12, tl & 0x0FFF
        val = pt[off + 7: off + 7 + vlen]
        off += 7 + vlen
        out.append((siid, piid, tcode, val, status))
    return out, op


async def read_baseline(t, sk):
    """Baseline snapshot in the same session (CCCD already set, single login).
    Device handles ONLY first requested object => read one by one,
    app counter increments. Read-only."""
    print("\n=== BASELINE (values BEFORE changes) ===")
    got = 0
    for i, (s, p) in enumerate(sr.DEFAULT_SET):
        name = sr.NAMES.get((s, p), "?")
        pt = await sr.spec_request(t, sk, [(s, p)], app_cnt=i)
        if not pt:
            print(f"  {name}: [no response]")
            continue
        for line in sr.parse_reply(pt):
            print("  " + line)
        got += 1
    print(f"=== baseline: read {got}/{len(sr.DEFAULT_SET)} ===\n")


async def listen(mac, secs, pre=5.0, baseline=True, log_path=None, snoop=False):
    if log_path is None:
        d = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "logs")
        _os.makedirs(d, exist_ok=True)
        log_path = _os.path.join(d, f"push_capture_{datetime.now():%Y%m%d_%H%M%S}.txt")
    logf = open(log_path, "w", encoding="utf-8", buffering=1)  # line-buffered: live tail
    tee = _Tee(_sys.stdout, logf)
    try:
        with contextlib.redirect_stdout(tee):
            print(f"[i] logging to: {log_path}")
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
                print("\n[+] LOGIN OK — CCCD on 0x001b enabled (subscription active)")

                if baseline:
                    await read_baseline(t, sk)

                print("=== READY: change scooter state now ===")
                print("  • press/release throttle        -> speed/current/power")
                print("  • toggle tail light / cruise")
                print("  • roll the wheel                -> mileage/time/riding mode")
                print(f"Listening window: {secs:.0f} s. Starting after countdown...\n")
                for k in range(int(pre), 0, -1):
                    print(f"  starting in {k}...", end="\r")
                    await asyncio.sleep(1)
                print("  >>> LISTENING ACTIVE — change scooter state! <<<  ")
                print("[[WINDOW_OPEN]]")  # ASCII sentinel for external detection

                loop = asyncio.get_event_loop()
                deadline = loop.time() + secs
                next_remind = loop.time() + 20
                n_push = 0
                ch_counts = {}

                async def handle_plain(pt, src):
                    nonlocal n_push
                    n_push += 1
                    res = parse_props(pt)
                    props, op = res if isinstance(res, tuple) else (res, None)
                    ts = datetime.now().strftime("%H:%M:%S")
                    print(f"\n  [{ts}] PUSH #{n_push} ({src}, op={op}) {pt.hex()}")
                    for siid, piid, tcode, val, status in props:
                        mark = "" if (siid, piid) in SUBSCRIBABLE else "  [outside subscription list]"
                        print("      " + sr.fmt_value(siid, piid, tcode, val)
                              + ("" if status == 0 else f"  [status={status}]") + mark)

                while loop.time() < deadline:
                    if loop.time() >= next_remind:
                        left = int(deadline - loop.time())
                        print(f"\n  ...pushes {n_push}; RX channels={ch_counts or '∅'}; remaining ~{left} s — change state!")
                        next_remind = loop.time() + 20
                    try:
                        s, b = await asyncio.wait_for(t.rx.get(), timeout=1.0)
                    except asyncio.TimeoutError:
                        continue  # tick: no frames yet — check deadline and continue listening
                    ch_counts[s] = ch_counts.get(s, 0) + 1
                    if snoop:
                        ts = datetime.now().strftime("%H:%M:%S")
                        print(f"  [{ts}] RX ch=0x{s:04X} len={len(b)}  {b.hex()}")
                    if s != CH_NOTIFY or len(b) < 4:
                        continue
                    # single frame: [0000][02][00][cnt][ct]
                    if b[0] == 0 and b[1] == 0 and b[2] == 0x02 and len(b) >= 6:
                        cnt = struct.unpack("<H", b[4:6])[0]
                        await t.write(CH_NOTIFY, struct.pack("<HBB", 0, 0x03, 0))
                        try:
                            await handle_plain(sr.dec_dev(sk, cnt, b[6:]), "single")
                        except Exception as e:
                            print(f"  [!] decryption failed (cnt={cnt}): {e}  raw={b.hex()}")
                    # multiframe: CTR from device
                    elif b[0] == 0 and b[1] == 0 and b[2] == 0x00 and len(b) >= 6:
                        fc = struct.unpack("<H", b[4:6])[0]
                        await t.write(CH_NOTIFY, struct.pack("<HBB", 0, 0x01, 0x01))
                        parts = {}
                        rdl = loop.time() + 5.0
                        while len(parts) < fc and loop.time() < rdl:
                            try:
                                s2, b2 = await asyncio.wait_for(
                                    t.rx.get(), timeout=max(0.1, rdl - loop.time()))
                            except asyncio.TimeoutError:
                                break
                            if s2 == CH_NOTIFY and len(b2) >= 2:
                                seq = struct.unpack("<H", b2[:2])[0]
                                if 1 <= seq <= fc:
                                    parts[seq] = b2[2:]
                        await t.write(CH_NOTIFY, struct.pack("<HBB", 0, 0x01, 0x00))
                        if len(parts) == fc:
                            payload = b"".join(parts[i] for i in sorted(parts))
                            cnt = struct.unpack("<H", payload[:2])[0]
                            try:
                                await handle_plain(sr.dec_dev(sk, cnt, payload[2:]), f"{fc} frames")
                            except Exception as e:
                                print(f"  [!] decryption failed (cnt={cnt}): {e}")
                        else:
                            print(f"  [!] received {len(parts)}/{fc} frames")

                print(f"\n=== summary: pushes received {n_push}; RX channels={ch_counts or '∅'} ===")
                if n_push == 0:
                    print("silence. This does NOT disprove the mechanism: if nothing changed, "
                          "there was nothing to push.\nRetry while actively changing state (throttle/light/motion).")
                else:
                    print(f"Log saved: {log_path}")
                return 0
            except Exception:
                import traceback
                traceback.print_exc()
                return 1
            finally:
                await t.close()
    finally:
        logf.flush()
        logf.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mac", default=da.MAC_DEFAULT)
    ap.add_argument("--secs", type=float, default=120.0, help="listening window, seconds (default 120)")
    ap.add_argument("--pre", type=float, default=5.0, help="pre-roll countdown, seconds (default 5)")
    ap.add_argument("--no-baseline", action="store_true", help="do not read baseline values")
    ap.add_argument("--snoop", action="store_true",
                    help="log ALL incoming frames on ANY characteristics (diagnostics)")
    ap.add_argument("--log", default=None, help="path to log file (default logs/push_capture_*.txt)")
    a = ap.parse_args()
    raise SystemExit(asyncio.run(listen(a.mac, a.secs, pre=a.pre,
                                        baseline=not a.no_baseline, log_path=a.log, snoop=a.snoop)))
