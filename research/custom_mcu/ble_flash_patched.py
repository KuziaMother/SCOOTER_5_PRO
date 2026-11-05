#!/usr/bin/env python3
"""
Flashing patched_mi5pro_firmware.bin via BLE (MCU target), state-resilient.

Model (docs/FACTS.md, 2026-08-22 + session observations):
  frag-status 0 = accepted into MCU-staging; 5 = "not accepted" (duplicate index in
  persistent staging AND/OR dirty BLE bank) — after 5 session is closed;
  7 = MCU "not ready" (transient, retry after delay passes).
  switchFirmware(4, param=1) on partial/own bank: rejected with status 6,
  OTA buffer resets (verified), followed by transient "not ready" for a few minutes.
  Staging is only probed: 5 = index already present, 0 = was absent (now accepted).

Algorithm:
  1. login -> warm-up (getFragmentSize) -> BLE bank state (display only).
  2. Probe MCU-frag1 (patched):
       0 -> staging empty -> upload 2..N -> commit switchFirmware(6). DONE.
       5 -> if bank is dirty: safe reset (switchFirmware(4), only on partial
           bank or bank == current official version) + wait for transient + retry frag1 probe;
           if still 5 -> map staging with probes 2..10 -> resume 11..N.
       7/silence -> retries with delays.
  3. commit switchFirmware(6) — ONLY after staging is guaranteed to hold
     the full image (all indices confirmed/accepted with status 0).

Usage:   python custom_mcu/ble_flash_patched.py
"""
import asyncio
import os
import struct
import sys
import time
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "core"))
from dreame_auth import Transport, MAC_DEFAULT, LTMK_HEX, dfu_cmd  # noqa: E402
from dreame_flasher import (  # noqa: E402
    login, send_fragment, poll_mcu_version, OPS, _cmd_value,
)

PATCHED = os.path.join(ROOT, "custom_mcu", "patched_mi5pro_firmware.bin")
OFFICIAL_MCU = os.path.join(ROOT, "firmware_ota",
                            "c0f78c49f322bd3d71fea19c90241882_mcu_xiaomi.scooter.5pro_v0007.bin")
OFFICIAL_BLE = os.path.join(ROOT, "firmware_ota",
                            "0d41b4df91f8d37b5f1355484e2b93c3_upd_xiaomi.scooter.5pro_v2.7.0_0015.bin")

LTMK = bytes.fromhex(open(LTMK_HEX).read().strip())
RETRY = 4            # retries on silence / status 7
WAIT_SLOW = 60.0     # pause on status 7, s
WAIT_SILENT = 30.0   # pause on silence, s
RESET_WAIT = 150.0   # transient delay after switchFirmware(4), s


def log(msg=""):
    print(msg, flush=True)


async def fresh_session(label):
    t = Transport(MAC_DEFAULT)
    await login(t, LTMK)
    log(f"[+] session \"{label}\"")
    return t


async def _cmd_value_retry(t, op, what, total=120.0):
    deadline = time.time() + total
    attempt = 0
    while time.time() < deadline:
        attempt += 1
        st, v = await _cmd_value(t, op, timeout=max(2.0, min(10.0, deadline - time.time())))
        if st == 0 and v is not None:
            return v
        log(f"[~] {what}: no response (attempt {attempt}, remaining {deadline - time.time():.0f} s)")
    return None


async def read_frag_size(t, op, total=300.0):
    v = await _cmd_value_retry(t, op["frag"], "getFragmentSize", total=total)
    if v is None or len(v) < 2:
        return None
    return struct.unpack_from("<H", v, 0)[0]


async def read_last(t, op, what="lastFragmentIndex", total=60.0):
    v = await _cmd_value_retry(t, op["last"], what, total=total)
    if v is None or len(v) < 2:
        return None, None
    idx = struct.unpack_from("<H", v, 0)[0]
    crc = struct.unpack_from("<I", v, 2)[0] if len(v) >= 6 else None
    return idx, crc


async def reset_ble_bank(t):
    """switchFirmware(4, param=1): rejected (status 6), buffer -> 0. Waiting for transient."""
    r = await dfu_cmd(t, OPS["ble"]["switch"], struct.pack("<I", 1))
    st = r[4] if r and len(r) >= 5 else None
    log(f"    switchFirmware(4) resp: {r.hex() if r else None} -> status={st}")
    if st != 6:
        log("[!] unexpected response to switchFirmware(4)")
    log(f"    transient 'not ready': waiting {RESET_WAIT:.0f} s...")
    await asyncio.sleep(RESET_WAIT)


async def send_with_retries(t, fw, frag, index):
    """send_fragment with retries on silence/7. Returns status (int/None)."""
    data = fw[(index - 1) * frag: index * frag]
    st = await send_fragment(t, index, data)
    tries = 0
    while st in (None, 7) and tries < RETRY:
        tries += 1
        wait = WAIT_SLOW if st == 7 else WAIT_SILENT
        log(f"[~] frag{index}: status={st!r} - waiting {wait:.0f} s, retry {tries}/{RETRY}")
        await asyncio.sleep(wait)
        st = await send_fragment(t, index, data)
    return st


async def upload_range(t, fw, frag, start, end, label):
    """Upload start..end (1-based). All must return status 0."""
    t0 = time.time()
    log(f"    uploading {label}: fragments {start}..{end}")
    for index in range(start, end + 1):
        st = await send_with_retries(t, fw, frag, index)
        if st != 0:
            log(f"\n[!] {label} fragment {index}/{end}: status={st!r} - stop WITHOUT commit "
                f"(last confirmed: {index - 1})")
            return False
        if index % 10 == 0 or index == end:
            spd = (index - start + 1) / max(time.time() - t0, 0.1)
            eta = (end - index) / max(spd, 0.1)
            print(f"\r    {label}: {index}/{end} ({100 * index // end}%) "
                  f"{spd:.1f} fr/s ETA {eta:.0f}s   ", end="", flush=True)
    log(f"\n[+] {label}: all fragments accepted (status 0)")
    return True


async def commit_mcu(t, label):
    """switchFirmware(6, param=1) + poll MCU version up to 3 min."""
    log(f"\n[!!!] {label}: switchFirmware(6) - ACTIVATION (irreversible)...")
    r = await dfu_cmd(t, OPS["mcu"]["switch"], struct.pack("<I", 1))
    st = r[4] if r and len(r) >= 5 else None
    log(f"    switchFirmware(6) resp: {r.hex() if r else None} -> status={st}")
    res = await poll_mcu_version(t, expected_before=None, timeout=180.0, interval=3.0)
    meaning = {True: "version changed",
               False: "version unchanged (expected for reinstalling 0007)",
               None: "silence+return - MCU rebooted (activation in progress)"}
    log(f"[i] version poll: {meaning[res]}")
    return st


async def finish_upload(t, patched, frag, start, N, label):
    if not await upload_range(t, patched, frag, start, N, label):
        return False
    await commit_mcu(t, "patched image")
    log("\n[===] DONE: patched MCU image activated via BLE")
    return True


async def main():
    patched = open(PATCHED, "rb").read()
    official_ble = open(OFFICIAL_BLE, "rb").read()
    log(f"patched: {len(patched)} B crc32={zlib.crc32(patched) & 0xFFFFFFFF:08x}")

    t = await fresh_session("recon")
    try:
        frag = await read_frag_size(t, OPS["mcu"])
        if not frag:
            log("[!] getFragmentSize(MCU) did not respond - device in transient state. "
                "Wait a few minutes and run again.")
            return 1
        N = -(-len(patched) // frag)
        log(f"[i] MCU fragmentSize={frag}, total fragments={N}")

        idx_ble, crc_ble = await read_last(t, OPS["ble"], "BLE bank")
        log(f"[i] BLE bank: lastFragmentIndex={idx_ble}, "
            f"crc={'%08x' % crc_ble if crc_ble is not None else '-'} (display only)")

        # ---------- 2. probe frag1 ----------
        st1 = await send_with_retries(t, patched, frag, 1)
        if st1 is None:
            log("[~] frag1: transport failure - reconnect and retry")
            await t.close()
            t = await fresh_session("retry frag1")
            frag = await read_frag_size(t, OPS["mcu"]) or frag
            st1 = await send_with_retries(t, patched, frag, 1)
        log(f"[i] MCU-frag1 (patched): status={st1!r}")

        if st1 == 0:
            # ---------- staging empty: full upload ----------
            return 0 if await finish_upload(t, patched, frag, 2, N, "patched") else 1

        if st1 == 5:
            # ---------- duplicate/gate ----------
            if idx_ble is not None and idx_ble > 0:
                frag_ble = await read_frag_size(t, OPS["ble"], total=60.0) or 512
                N_ble = -(-len(official_ble) // frag_ble)
                local_crc = zlib.crc32(official_ble[:idx_ble * frag_ble]) & 0xFFFFFFFF
                safe = (idx_ble < N_ble) or (crc_ble is not None and crc_ble == local_crc)
                log(f"[i] BLE bank dirty ({idx_ble}/{N_ble}); contents match "
                    f"official: {crc_ble is not None and crc_ble == local_crc}")
                if safe:
                    log("[i] bank reset is safe (incomplete or same version)")
                    await reset_ble_bank(t)
                    await t.close()
                    t = await fresh_session("after bank reset")
                    frag = await read_frag_size(t, OPS["mcu"]) or frag
                    st1 = await send_with_retries(t, patched, frag, 1)
                    log(f"[i] MCU-frag1 after bank reset: status={st1!r}")
                else:
                    log("[!] bank is full with unknown contents - stop, manual intervention required")
                    return 1

            if st1 == 0:
                return 0 if await finish_upload(t, patched, frag, 2, N, "patched (after reset)") else 1

            if st1 != 5:
                log(f"[!] unexpected frag1 status: {st1!r} - stop without commit")
                return 1

            # ---------- map staging: probes 2..N-? (here 2..10+ effectively up to N) ----------
            log("[i] frag1 still 5 -> mapping staging with probes (5 = present, 0 = accepted)")
            last_confirmed = 1
            for index in range(2, N + 1):
                stp = await send_with_retries(t, patched, frag, index)
                if stp == 5:
                    log(f"    probe {index}: 5 (already in staging) - session closed, reconnect")
                    last_confirmed = index
                    await t.close()
                    t = await fresh_session(f"probe {index + 1}")
                    frag = await read_frag_size(t, OPS["mcu"]) or frag
                elif stp == 0:
                    last_confirmed = index
                    if index % 25 == 0:
                        log(f"    probe {index}: 0 (accepted)")
                else:
                    log(f"[!] probe {index}: unexpected status {stp!r} - stop without commit")
                    return 1
            log(f"[i] staging mapped: confirmed 1..{last_confirmed}")

            # ---------- resume ----------
            if last_confirmed >= N:
                log("[i] full image already in staging - commit immediately")
                await commit_mcu(t, "patched image (already completely in staging)")
                log("\n[===] DONE: patched MCU image activated via BLE")
                return 0
            return 0 if await finish_upload(t, patched, frag, last_confirmed + 1, N,
                                            f"patched (resume from {last_confirmed + 1})") else 1

        log(f"[!] unexpected frag1 status: {st1!r} - stop without commit")
        return 1
    finally:
        try:
            await t.close()
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
