#!/usr/bin/env python3
"""
Probe: does MCU gate open after uploading BLE image
in same session? Mi Home always flashes BLE and MCU together in one release: BLE image first
(opcodes 2/3/4), then MCU (2/5/6). Our MCU probes ran standalone — possibly,
the gate requires a preceding BLE upload in the session.

Plan (ONE run, without commit):
  1. Upload ENTIRE BLE image (301 fragments) without switchFirmware — safe:
     "without --commit uploads all fragments, but does NOT switch firmware",
     uncompleted/uncommitted DFU is reset by the device itself.
  2. Send MCU fragment 1 (clean, version 0007).
     status=0 -> gate opens after BLE upload (found what was missing!);
     status=5 -> depends not on upload, but on something else (commit/version).

Usage:  python probes/mcu_gate_after_ble_upload.py
"""
import asyncio
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "core"))
from dreame_auth import Transport, MAC_DEFAULT, LTMK_HEX  # noqa: E402
from dreame_flasher import (login, flash, get_fragment_size, get_last_index,
                            send_fragment, OPS)  # noqa: E402

BLE_IMG = os.path.join(ROOT, "firmware_ota",
                       "0d41b4df91f8d37b5f1355484e2b93c3_upd_xiaomi.scooter.5pro_v2.7.0_0015.bin")
MCU_IMG = os.path.join(ROOT, "firmware_ota",
                       "c0f78c49f322bd3d71fea19c90241882_mcu_xiaomi.scooter.5pro_v0007.bin")


async def main():
    ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
    t = Transport(MAC_DEFAULT)
    try:
        await login(t, ltmk)

        print("\n=== STEP 1: BLE image upload WITHOUT commit ===")
        ok = await flash(t, BLE_IMG, "ble", commit=False)
        if not ok:
            print("[!] BLE upload failed — stopping probe")
            return 1

        print("\n=== STEP 2: MCU fragment 1 after BLE upload ===")
        op = OPS["mcu"]
        frag_size = await get_fragment_size(t, op)
        last, crc = await get_last_index(t, op)
        fw = open(MCU_IMG, "rb").read()
        st = await send_fragment(t, 1, fw[:frag_size])
        if st is None:
            print("[!] transport failure — no ACK/event")
            return 1
        txt = {0: "ACCEPTED (status 0) — GATE OPENED AFTER BLE UPLOAD",
               5: "rejected (status 5) — does not depend on upload"}.get(st, f"status={st}")
        print(f"[i] MCU fragment 1: {txt}")
        return 0
    finally:
        await t.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
