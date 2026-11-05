#!/usr/bin/env python3
"""
FINAL STEP: switchFirmware(MCU, opcode 6) — staged image activation over BLE.

Explicitly approved by user. Image v0007 is byte-for-byte identical to running one;
MCU target accepting same version is documented (UART dfu_active).

Expected scenario: status 0 response -> MCU flashes itself over USART3
(async, up to ~3 min, matching Mi Home) -> reboot -> version remains 0007,
staging is cleared. For same version no change is expected: correct outcome is
poll timeout without change (False) or silence+return (None = reboot occurred).

Single command; followed by read-only version polling ([01] on 0x001c).

Usage:  python probes/mcu_ble_commit.py
"""
import asyncio
import os
import struct
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "core"))
from dreame_auth import Transport, MAC_DEFAULT, LTMK_HEX, CH_DFU_CMD  # noqa: E402
from dreame_flasher import login, poll_mcu_version, OPS  # noqa: E402


async def main():
    ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
    t = Transport(MAC_DEFAULT)
    try:
        await login(t, ltmk)

        print("\n>>> switchFirmware(6) — ACTIVATION (irreversible, approved)...")
        frame = struct.pack("<HB", OPS["mcu"]["switch"], 4) + struct.pack("<I", 1)
        while not t.rx.empty():
            t.rx.get_nowait()
        await t.client.write_gatt_char(t.chars[CH_DFU_CMD], frame, response=True)

        # Response may take time (device begins relaying) — wait up to 15s.
        resp = None
        deadline = time.time() + 15.0
        while time.time() < deadline and resp is None:
            for s, b in await t.drain(1.0):
                if s == CH_DFU_CMD and len(b) >= 3 and b[0] == 0x01:
                    resp = b
                    break
        if resp:
            st = resp[4] if len(resp) >= 5 else None
            print(f"[i] response: {resp.hex()} -> status={st} "
                  f"({'accepted' if st == 0 else 'REJECTED/unknown'})")
        else:
            print("[!] no switchFirmware response within 15s — proceeding with version polling")

        res = await poll_mcu_version(t, expected_before=None, timeout=180.0, interval=3.0)
        meaning = {
            True: "version CHANGED (unexpected for same version!)",
            False: "version did not change — EXPECTED for same version reflash",
            None: "silence and return — MCU rebooted (activation occurred)",
        }[res]
        print(f"\n[i] POLL SUMMARY: {meaning}")
        return 0
    finally:
        await t.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
