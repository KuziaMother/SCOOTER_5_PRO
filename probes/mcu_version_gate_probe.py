#!/usr/bin/env python3
"""
Probe: what does device verify on MCU fragment 1 (status 5 rejection)?

Hypothesis H1: version comparison ("image version vs installed"), version read from
image header @0x22 ("0007"). Signature/certificate is in trailer (@0x24807+),
meaning fragment 1 does not contain it.

Experiment: send ONLY fragment 1 with "0007"->"0008" in header.
  status=0 -> gate is version string (H1);
  status=5 -> verifies something else (other field / prior state).

Safety: switchFirmware is NOT sent, no other fragments. Single
fragment into staging buffer: incomplete DFU resets automatically.

Usage:  python probes/mcu_version_gate_probe.py
"""
import asyncio
import sys
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.join(_ROOT, "core"))
from dreame_auth import Transport, MAC_DEFAULT, LTMK_HEX  # noqa: E402
from dreame_flasher import login, get_fragment_size, get_last_index, send_fragment, OPS  # noqa: E402

IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "firmware_ota",
                   "c0f78c49f322bd3d71fea19c90241882_mcu_xiaomi.scooter.5pro_v0007.bin")
VER_OFF = 0x22          # ASCII version in MCU image header (FACTS.md)


async def main():
    ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
    t = Transport(MAC_DEFAULT)
    try:
        await login(t, ltmk)
        op = OPS["mcu"]
        frag_size = await get_fragment_size(t, op)
        if not frag_size:
            print("[!] getFragmentSize timed out"); return 1
        last, crc = await get_last_index(t, op)
        fw = open(IMG, "rb").read()
        assert len(fw) > frag_size
        tampered = bytearray(fw[:frag_size])
        orig_ver = bytes(tampered[VER_OFF:VER_OFF + 4])
        tampered[VER_OFF:VER_OFF + 4] = b"0008"
        print(f"[i] header: version {orig_ver!r} -> b'0008' (fragment 1 only, no commit)")
        st = await send_fragment(t, 1, bytes(tampered))
        if st is None:
            print("[!] transport failure — no ACK/event")
            return 1
        status_txt = {0: "ACCEPTED (status 0) — gate = version string",
                      5: "rejected (status 5) — checking other field"}.get(st, f"status={st}")
        print(f"[i] fragment 1 (version 0008): {status_txt}")
        last2, crc2 = await get_last_index(t, op)
        print(f"[i] buffer state after: last={last2}, crc={'%08x' % crc2 if crc2 else '—'}")
        return 0
    finally:
        await t.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
