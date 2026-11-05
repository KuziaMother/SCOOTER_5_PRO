#!/usr/bin/env python3
"""
Probe 4: finish uploading MCU image over BLE starting from fragment 3.

Model (verified by probes 1-3):
  status 0 = fragment accepted into MCU staging;
  status 5 = duplicate index (already staged) + session closure;
  status 7 = MCU temporarily not ready (transient post-reboot);
  lastFragmentIndex(5) does NOT reflect real staging state (returns 0).

Safety: switchFirmware(6) is NOT transmitted. On any status != 0
on a new index — abort and report.

Usage:  python probes/mcu_ble_upload_rest.py [START]   (default START=3)
"""
import asyncio
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "core"))
from dreame_auth import Transport, MAC_DEFAULT, LTMK_HEX  # noqa: E402
from dreame_flasher import login, get_fragment_size, get_last_index, send_fragment, OPS  # noqa: E402

MCU_IMG = os.path.join(ROOT, "firmware_ota",
                       "c0f78c49f322bd3d71fea19c90241882_mcu_xiaomi.scooter.5pro_v0007.bin")


async def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
    t = Transport(MAC_DEFAULT)
    try:
        await login(t, ltmk)
        op = OPS["mcu"]
        frag_size = await get_fragment_size(t, op)
        fw = open(MCU_IMG, "rb").read()
        N = -(-len(fw) // frag_size)
        print(f"[i] fragments {start}..{N} (total {N}), without commit")

        t0 = time.time()
        n_ok = n_bad = 0
        for idx in range(start, N + 1):
            data = fw[(idx - 1) * frag_size: idx * frag_size]
            st = await send_fragment(t, idx, data)
            if st is None:
                print(f"\n[!] frag{idx}: transport failure — aborting (ok={n_ok}, bad={n_bad})")
                return 1
            if st == 0:
                n_ok += 1
            else:
                n_bad += 1
                print(f"\n[~] frag{idx}: status={st} (non-zero!) — stop, model invalid "
                      f"(ok={n_ok}, bad={n_bad})")
                return 1
            if idx % 10 == 0 or idx == N:
                spd = (idx - start + 1) / max(time.time() - t0, 0.1)
                eta = (N - idx) / max(spd, 0.1)
                print(f"\r  frag {idx}/{N} ok={n_ok} bad={n_bad} "
                      f"{spd:.1f}fr/s ETA {eta:.0f}s   ", end="", flush=True)
        dt = time.time() - t0
        print(f"\n[i] finished in {dt:.0f}s: ok={n_ok}, bad={n_bad}")
        last, crc = await get_last_index(t, op)
        print(f"[i] lastFragmentIndex(5) after: last={last}, crc={'%08x' % crc if crc else '—'} "
              f"(known: does not reflect staging)")
        print("[i] switchFirmware(6) NOT sent — image in staging, awaiting decision")
        return 0
    finally:
        await t.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
