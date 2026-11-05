#!/usr/bin/env python3
"""
Probe: is MCU gate closed while BLE OTA bank is dirty?

Facts:
  - Mi Home: BLE image -> switchFirmware(4) [commit/bank reset] -> MCU image — works.
  - Our MCU probes: BLE bank was at 296 (persistent state, survives
    sessions and power cycle, see todo.md §C) — MCU fragment 1 always returned status 5.
  - todo.md: "switchFirmware RESETS OTA buffer even on reject (status 6 -> bank to 0)".

Plan (single session, safe):
  1. BLE bank state (opcode 3) — expected 296.
  2. switchFirmware(BLE, opcode 4), param=1 — on same version REJECTED (status 6),
     but resets bank to 0 (verified mechanism; no firmware switch occurs).
  3. BLE bank state — expected 0.
  4. MCU fragment 1 (clean 0007):
     status=0 -> gate = "no active OTA session of another target" (found missing link!);
     status=5 -> hypothesis incorrect.

Usage:  python probes/mcu_gate_bank_reset.py
"""
import asyncio
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "core"))
from dreame_auth import Transport, MAC_DEFAULT, LTMK_HEX, dfu_cmd  # noqa: E402
from dreame_flasher import (login, get_fragment_size, get_last_index,
                            send_fragment, OPS)  # noqa: E402

MCU_IMG = os.path.join(ROOT, "firmware_ota",
                       "c0f78c49f322bd3d71fea19c90241882_mcu_xiaomi.scooter.5pro_v0007.bin")


async def main():
    ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
    t = Transport(MAC_DEFAULT)
    try:
        await login(t, ltmk)

        print("\n=== STEP 1: BLE bank state BEFORE ===")
        last, crc = await get_last_index(t, OPS["ble"])
        print(f"[i] BLE bank: last={last}, crc={'%08x' % crc if crc else '—'}")

        print("\n=== STEP 2: switchFirmware(BLE) — bank reset (rejection expected on same version) ===")
        r = await dfu_cmd(t, OPS["ble"]["switch"], struct.pack("<I", 1))
        if r:
            # response [01][len][opcode u16][status][data]
            st = r[4] if len(r) >= 5 else None
            print(f"[i] response: {r.hex()} -> status={st} (6 = rejected, bank resets anyway)")
        else:
            print("[!] no response to switchFirmware")

        print("\n=== STEP 3: BLE bank state AFTER ===")
        last2, crc2 = await get_last_index(t, OPS["ble"])
        print(f"[i] BLE bank: last={last2}, crc={'%08x' % crc2 if crc2 else '—'} "
              f"{'(reset)' if last2 == 0 else '(NOT reset!)'}")

        print("\n=== STEP 4: MCU fragment 1 with clean BLE bank ===")
        op = OPS["mcu"]
        frag_size = await get_fragment_size(t, op)
        lastm, crcm = await get_last_index(t, op)
        fw = open(MCU_IMG, "rb").read()
        st = await send_fragment(t, 1, fw[:frag_size])
        if st is None:
            print("[!] transport failure — no ACK/event")
            return 1
        txt = {0: "ACCEPTED (status 0) — GATE = CLEAN BLE BANK, FOUND MISSING LINK!",
               5: "rejected (status 5) — bank hypothesis incorrect"}.get(st, f"status={st}")
        print(f"[i] MCU fragment 1: {txt}")
        return 0
    finally:
        await t.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
