#!/usr/bin/env python3
"""
Probe 3: what does status 7 mean — "rejected and unbuffered" or "buffered with flag"?

Sequence (single session, no commit, clean banks):
  frag1 -> status A (expect 7)
  frag1 again -> status B:
      5 = "duplicate/invalid index" => first fragment buffered despite 7;
      7 = state unchanged           => 7 = clean reject, nothing buffered.
  frag2 -> status C:
      if B=5 and C=0 — buffering is "blind", gate triggers later;
      if C=5 — index skip is also detected by device.

Prints full raw 0x0017 events (unfiltered) in case they contain more bytes.

Usage:  python probes/mcu_gate_repeat.py
"""
import asyncio
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "core"))
from dreame_auth import Transport, MAC_DEFAULT, LTMK_HEX  # noqa: E402
from dreame_flasher import (login, get_fragment_size, get_last_index,
                            send_fragment, OPS)  # noqa: E402

MCU_IMG = os.path.join(ROOT, "firmware_ota",
                       "c0f78c49f322bd3d71fea19c90241882_mcu_xiaomi.scooter.5pro_v0007.bin")


async def main():
    ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
    t = Transport(MAC_DEFAULT)
    try:
        await login(t, ltmk)
        op = OPS["mcu"]
        last, crc = await get_last_index(t, op)
        if last != 0:
            print(f"[!] MCU bank not empty (last={last}) — test is invalid")
            return 1
        frag_size = await get_fragment_size(t, op)
        fw = open(MCU_IMG, "rb").read()

        for idx in (1, 1, 2):
            st = await send_fragment(t, idx, fw[(idx - 1) * frag_size: idx * frag_size])
            print(f"[i] frag{idx}: status={st}")

        last2, crc2 = await get_last_index(t, op)
        print(f"[i] MCU bank after: last={last2}, crc={'%08x' % crc2 if crc2 else '—'}")
        return 0
    finally:
        await t.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
