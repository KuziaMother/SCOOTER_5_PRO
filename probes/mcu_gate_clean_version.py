#!/usr/bin/env python3
"""
Probe 2: MCU version gate on CLEAN BLE bank.

Previous probe revealed two-stage gate:
  - dirty BLE bank (last!=0)  -> MCU fragment 1: status 5 (session conflict);
  - clean BLE bank (last=0)     -> MCU-fragment 1: status 7 (real gate).

Early test "0008 in header" was invalid (bank was dirty -> 5).
Repeating with a clean bank:
  - status=0 -> gate = header version comparison @0x22; all explained;
  - status=7 -> check also uses other fields (or not version).

Safety: without switchFirmware(6); one fragment; check banks and
reset BLE bank when needed via standard mechanism (switchFirmware(4) on same
version = status 6 reject + bank reset, verified).

Usage:   python probes/mcu_gate_clean_version.py
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
VER_OFF = 0x22


async def ensure_clean_ble_bank(t):
    last, crc = await get_last_index(t, OPS["ble"])
    if last == 0:
        print("[i] BLE bank is clean (last=0)")
        return True
    print(f"[i] BLE bank is dirty (last={last}) — resetting via switchFirmware(4)...")
    r = await dfu_cmd(t, OPS["ble"]["switch"], struct.pack("<I", 1))
    st = r[4] if r and len(r) >= 5 else None
    print(f"[i] response: {r.hex() if r else None} status={st}")
    last2, _ = await get_last_index(t, OPS["ble"])
    print(f"[i] BLE bank after reset: last={last2}")
    return last2 == 0


async def main():
    ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
    t = Transport(MAC_DEFAULT)
    try:
        await login(t, ltmk)

        if not await ensure_clean_ble_bank(t):
            print("[!] failed to obtain clean BLE bank — stopping")
            return 1

        op = OPS["mcu"]
        lastm, crcm = await get_last_index(t, op)
        if lastm != 0:
            print(f"[!] MCU bank NOT empty (last={lastm}) — auto-reset/reboot needed, "
                  f"otherwise test is invalid")
            return 1

        frag_size = await get_fragment_size(t, op)
        fw = open(MCU_IMG, "rb").read()
        tampered = bytearray(fw[:frag_size])
        tampered[VER_OFF:VER_OFF + 4] = b"0008"
        print("[i] MCU-fragment 1 with version b'0008' (clean banks)")
        st = await send_fragment(t, 1, bytes(tampered))
        if st is None:
            print("[!] transport failure")
            return 1
        txt = {0: "ACCEPTED — gate = header version string",
               7: "status 7 — version read not only from @0x22 / verified differently"}.get(
            st, f"status={st} (new code)")
        print(f"[i] result: {txt}")
        return 0
    finally:
        await t.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
