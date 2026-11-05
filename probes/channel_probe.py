#!/usr/bin/env python3
"""
Channel number enumeration of channel transport post-login.

Logic: CTR frame [00 00][03][channel][fc u16] — transmit request. Device
replies with ACK ONLY for EXISTING channels. Channel 5 is known (securitychipauth/login).

SAFE: transmits CTR with fc=0 only, no DATA frames — zero commands
sent to device. Pure channel map reconnaissance.

Usage:  python channel_probe.py [--chars 0x0016,0x001a] [--max 31]
"""
import argparse
import asyncio
import struct

import os as _os, sys as _sys
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
_sys.path.insert(0, _os.path.join(_ROOT, "core"))

import dreame_auth as da


async def probe_char(t, char_sid: int, max_ch: int, fc: int = 1):
    print(f"\n=== characteristic 0x{char_sid:04x} ===")
    if char_sid not in t.chars:
        print("   characteristic not found")
        return {}
    props = {str(p).lower() for p in t.chars[char_sid].properties}
    print(f"   props={sorted(props)}")
    alive = {}
    for ch in range(max_ch + 1):
        while not t.rx.empty():
            t.rx.get_nowait()
        ctr = struct.pack("<HBBH", 0, da.PKT_CTR, ch, fc)
        try:
            await t.client.write_gatt_char(t.chars[char_sid], ctr, response=False)
        except Exception as e:
            print(f"   ch {ch:>2}: write err {e}")
            continue
        got = await t.drain(1.2)
        if not got:
            print(f"   ch {ch:>2}: silence")
            continue
        tag = " <<< ACTIVE" if ch != 5 else " (login, known)"
        alive[ch] = got
        print(f"   ch {ch:>2}: RESPONSE{tag}")
        for s, b in got:
            print(f"        0x{s:04x} {b.hex()}  [{da.decode(b)}]")
    return alive


async def run(mac: str, char_list, max_ch: int, fc: int = 1):
    ltmk = bytes.fromhex(open(da.LTMK_HEX).read().strip())
    t = da.Transport(mac)
    try:
        await t.connect()
        if not await t.a4_handshake():
            print("[!] transport failed to connect")
            return 1
        for s, b in await t.drain(1.0):
            if s == da.CH_LOGIN and len(b) >= 3 and b[2] == da.PKT_MNG:
                await t.write(da.CH_LOGIN,
                              struct.pack("<HBB", 0, da.PKT_MNG_ACK, 0)
                              + bytes([t.pkg_num, t.dmtu]))
        priv, dev_pub = await da.stage_a_pubkey_exchange(t)
        if not (dev_pub and len(dev_pub) >= 64):
            return 1
        if not await da.stage_b_confirm(t, priv, dev_pub, ltmk, crc_be=False):
            print("[!] login refused")
            return 1
        print("\n[+] LOGIN OK — scanning channel map")

        summary = {}
        for cs in char_list:
            summary[cs] = await probe_char(t, cs, max_ch, fc)

        print("\n=== SUMMARY: active channels ===")
        for cs, alive in summary.items():
            print(f"0x{cs:04x}: {sorted(alive)}")
        return 0
    except Exception:
        import traceback
        traceback.print_exc()
        return 1
    finally:
        await t.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mac", default=da.MAC_DEFAULT)
    ap.add_argument("--chars", default="0x0016,0x001a")
    ap.add_argument("--max", type=int, default=31)
    ap.add_argument("--fc", type=int, default=1, help="frame count in CTR (1 = like login)")
    a = ap.parse_args()
    chars = [int(x, 16) for x in a.chars.split(",")]
    raise SystemExit(asyncio.run(run(a.mac, chars, a.max, a.fc)))
