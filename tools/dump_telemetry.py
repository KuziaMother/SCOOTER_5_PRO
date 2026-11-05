#!/usr/bin/env python3
"""Full telemetry dump for Dreame/Xiaomi Scooter 5 Pro via MIoT-spec over BLE.

Reads the complete property map (siid 1..4 + siid 6 trip logs) and prints table.
Protocol and layout details: see research/REPORT.md; implementation in probes/spec_read.py.

IMPORTANT: read properties ONE BY ONE per request. The device only services the first
object in a request and sets status 0xf05d (-4003) for subsequent objects — verified by
experimentation. Batch requests are not supported.

READ-ONLY: no set requests are executed.

Usage:  python tools/dump_telemetry.py [--out docs/telemetry.txt] [--all]
"""
import argparse
import asyncio
import os
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "core"))
sys.path.insert(0, os.path.join(ROOT, "probes"))

import dreame_auth as da                     # noqa: E402
import spec_read as sr                       # noqa: E402

# Query list: (siid, piid). Order determines output table ordering.
BATTERY = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (3, 1), (3, 2), (3, 10),
           (3, 11), (3, 12)]
RIDE = [(1, 1), (1, 7), (1, 9), (2, 1), (2, 6), (2, 7), (2, 8), (2, 9), (1, 8)]
SETTINGS = [(2, 2), (2, 3), (2, 4), (2, 5), (2, 10), (2, 12), (2, 13), (2, 14),
            (2, 15), (2, 16), (2, 17)]
IDENT = [(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (3, 3), (3, 5), (3, 8)]

GROUPS = [("BATTERY", BATTERY), ("RIDE", RIDE),
          ("SETTINGS", SETTINGS), ("IDENTIFICATION / OTHER", IDENT)]

EXTRA_NAMES = {
    (2, 10): "ASR_IS_ON", (2, 11): "REMAINING_MILEAGE_ALGORITHM",
    (2, 12): "AUTO_LIGHT", (2, 13): "TCS", (2, 14): "INTELLIGENT_DOWNHILL",
    (2, 15): "HILL_PARKING", (2, 16): "ATMOSPHERE_LIGHT",
    (2, 17): "BLUETOOTH_SEARCH_ON", (2, 18): "FAKE_SHUTDOWN_STATUS",
    (3, 4): "LOCK_WARNING", (3, 5): "MILEAGE_UNIT", (3, 6): "OOB_CODE",
    (3, 7): "TIRE_MAINTENANCE", (3, 8): "ACTIVATION_DATE", (3, 9): "RIDING_RECORDS",
    (4, 6): "RESTORE_SCOOTER_SETTINGS", (4, 7): "MORE_BATTERY_INFO",
    (4, 8): "MORE_BATTERY_INFO_2", (4, 10): "BLUETOOTH_CAR_SEARCH",
    (6, 1): "LOG_1", (6, 2): "LOG_2", (6, 3): "LOG_3", (6, 4): "LOG_4",
    (6, 5): "LOG_5",
}
sr.NAMES.update(EXTRA_NAMES)


async def login(mac):
    """Establish transport and complete login. Returns (transport, sessionKey)."""
    import struct
    ltmk = bytes.fromhex(open(da.LTMK_HEX).read().strip())
    t = da.Transport(mac)
    await t.connect()
    if not await t.a4_handshake():
        raise RuntimeError("transport failed to connect")
    for s, b in await t.drain(1.0):
        if s == da.CH_LOGIN and len(b) >= 3 and b[2] == da.PKT_MNG:
            await t.write(da.CH_LOGIN, struct.pack("<HBB", 0, da.PKT_MNG_ACK, 0)
                          + bytes([t.pkg_num, t.dmtu]))
    priv, dev_pub = await da.stage_a_pubkey_exchange(t)
    if not (dev_pub and len(dev_pub) >= 64):
        raise RuntimeError("Stage A did not return pubkey")
    if not await da.stage_b_confirm(t, priv, dev_pub, ltmk, crc_be=False):
        raise RuntimeError("login refused")
    return t, da.LAST_SK


def parse_one(pt):
    """Parse single property reply -> (siid, piid, tcode, value, status) or None."""
    import struct
    if not pt or len(pt) < 11 or pt[5] < 1:
        return None
    if len(pt) < 13:                       # error record only (5 bytes)
        siid, piid, status = struct.unpack("<BHH", pt[6:11])
        return siid, piid, 0, b"", status
    siid, piid, status, tl = struct.unpack("<BHHH", pt[6:13])
    tcode, vlen = tl >> 12, tl & 0x0FFF
    return siid, piid, tcode, pt[13:13 + vlen], status


async def read_all(mac, props, out_path):
    t, sk = await login(mac)
    print("[+] LOGIN OK — reading properties one by one\n")
    rows, cnt = [], 0
    try:
        for siid, piid in props:
            name = sr.NAMES.get((siid, piid), "?")
            pt = None
            for attempt in range(2):
                pt = await sr.spec_request(t, sk, [(siid, piid)], cnt,
                                           frame_size=18, op=2, timeout=6.0)
                cnt += 1
                if pt:
                    break
                await asyncio.sleep(0.6)
            if not pt:
                # Session hung — reconnect and resume
                print(f"  {siid}.{piid:<3} {name:<26} no response, reconnecting")
                try:
                    await t.close()
                except Exception:
                    pass
                t, sk = await login(mac)
                cnt = 0
                rows.append((siid, piid, name, "no response", ""))
                continue
            got = parse_one(pt)
            if not got:
                rows.append((siid, piid, name, "unparsed", pt.hex()))
                print(f"  {siid}.{piid:<3} {name:<26} unparsed  {pt.hex()}")
                continue
            g_siid, g_piid, tcode, val, status = got
            if status != 0 or not val:
                sstr = f"error {status - 0x10000 if status > 0x7fff else status}"
                rows.append((siid, piid, name, sstr, ""))
                print(f"  {siid}.{piid:<3} {name:<26} {sstr}")
                continue
            line = sr.fmt_value(g_siid, g_piid, tcode, val)
            shown = line.split("] ", 1)[1] if "] " in line else line
            shown = shown.split("   raw=")[0].strip()
            rows.append((siid, piid, name, shown, val.hex()))
            print(f"  {siid}.{piid:<3} {name:<26} {shown}")
            await asyncio.sleep(0.35)
    finally:
        try:
            await t.close()
        except Exception:
            pass

    # Report
    lines = [f"Dreame/Xiaomi Scooter 5 Pro — telemetry ({mac})",
             f"captured: {datetime.now():%Y-%m-%d %H:%M:%S}",
             "source: MIoT-spec over BLE (private spec from Mi Home plugin)", ""]
    by_key = {(s, p): (n, v, r) for s, p, n, v, r in rows}
    for title, group in GROUPS:
        picked = [(s, p) for s, p in group if (s, p) in by_key]
        if not picked:
            continue
        lines.append(f"--- {title} ---")
        for s, p in picked:
            n, v, r = by_key[(s, p)]
            lines.append(f"  {s}.{p:<3} {n:<28} {v}" + (f"   raw={r}" if r else ""))
        lines.append("")
    text = "\n".join(lines)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"\n[*] saved: {out_path}")
    print("\n" + text)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mac", default=da.MAC_DEFAULT)
    ap.add_argument("--out", default=os.path.join(ROOT, "docs", "telemetry.txt"))
    ap.add_argument("--all", action="store_true",
                    help="include settings, identification and logs (takes longer)")
    ap.add_argument("--props", help='custom property list: "6:1,6:2,4:7"')
    a = ap.parse_args()
    if a.props:
        props = [tuple(int(x) for x in pr.split(":")) for pr in a.props.split(",")]
        GROUPS[:] = [("SELECTED PROPERTIES", props)]
    else:
        props = BATTERY + RIDE + (SETTINGS + IDENT if a.all else [])
    return asyncio.run(read_all(a.mac, props, a.out))


if __name__ == "__main__":
    raise SystemExit(main())
