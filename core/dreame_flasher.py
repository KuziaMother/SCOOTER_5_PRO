#!/usr/bin/env python3
"""
Dreame Scooter 5 Pro — firmware flasher (BLE/MCU DFU) over reversed protocol.
==============================================================================

Uses transport and security-chip login from dreame_auth.py and flashes
official firmware image via FE95/0x0018 channel.

Fully analyzed protocol — docs/dreame_dfu_protocol.md, sections 6.14–6.16.
Brief summary (little-endian):
  Commands (0x0017 W/RESP): [opcode u16][len u8][params]  ; response [01][len][opcode u16][status][data]
      2=getFragmentSize, 3=lastFragmentIndex(BLE), 5=lastFragmentIndex(MCU),
      4=switchFirmware(BLE), 6=switchFirmware(MCU)
  Data     (0x0018):
      CTR   [00 00][00][subtype=00][frameCount u16]           -> device ACK 01 (ready)
      DATA  [seq u16][data]  seq 1-based, frame = 18B data (default channel frameSize)
      ACK   [00 00][01][status][reqSeq u16]:
              05 reqSeq = "send frame reqSeq" (pull, window=1), 00 = message accepted
  After fragment reception, device sends event on 0x0017: [02][03][status][index u16]:
      status 00 = fragment ACCEPTED, else rejected (5 = same/older version etc.).

Fragment message = [index u16 LE][fragmentData(fragmentSize)], index = lastIndex+1.
switchFirmware is IRREVERSIBLE (brick risk) — sent only with --commit flag.

Usage:
    python dreame_flasher.py <ble|mcu> <firmware.bin> [MAC] [--commit] [--yes]
        (without --commit flashes all fragments, but does NOT switch firmware)

    python dreame_flasher.py <ble|mcu> <fw.bin> [--limit=K] [--burst=N] [--frame-size=N]
        --limit: flash only K fragments (speed measurement, commit is not sent)
        --burst: message frames before waiting for ACK (default ALL; 1 = old behavior)
        --frame-size: DO NOT change — 18 is fixed by device (see docs/FACTS.md)

    python dreame_flasher.py poll-mcu [MAC] [--poll-timeout SEC]
        poll MCU version only (read-only) — verify if installation was applied
"""

import os
import sys
import time
import zlib
import struct
import asyncio

from dreame_auth import (
    Transport, stage_a_pubkey_exchange, stage_b_confirm, dfu_cmd, parse_cmd_resp, sid,
    CH_DFU_CMD, CH_DFU_DATA, CH_LOGIN, PKT_CTR, PKT_MNG, PKT_MNG_ACK, MAC_DEFAULT, LTMK_HEX,
)

FRAME_SIZE = 18          # frameSize of channel 0x0018 — FIXED by device.
                         # Verified: 240B frame -> device pulls endlessly (249 times),
                         # because it reassembles message by seq*frameSize offset. Do not tune.
BURST = 0                # message frames to send before waiting for ACK; 0 = ALL.
                         # Verified: all 29 frames in a row (10ms pacing) -> 0 pulls,
                         # ACK 00 + DFU event, 3 runs in a row. ~2.7x speedup.
                         # Pull (ACK 05) is a RECOVERY mechanism, not window=1:
                         # device requests frames only when they are actually missing.
OPS = {
    "ble": {"frag": 2, "last": 3, "switch": 4},
    "mcu": {"frag": 2, "last": 5, "switch": 6},
}
# Fragment status codes (event 02 03 <status>): from MeshDfuManager.status2otaCode
FRAG_STATUS = {
    0: "OK (accepted)",
    5: "rejected (code -505: usually same/incompatible firmware version)",
}


async def login(t, ltmk):
    """connect → A4/MNG → security-chip login (Stage A+B)."""
    await t.connect()
    if not await t.a4_handshake():
        raise RuntimeError("transport handshake failed (no MNG)")
    for s, b in await t.drain(1.0):     # MNG sometimes arrives repeatedly
        if s == CH_LOGIN and len(b) >= 3 and b[2] == PKT_MNG:
            await t.write(CH_LOGIN, struct.pack("<HBB", 0, PKT_MNG_ACK, 0)
                          + bytes([t.pkg_num, t.dmtu]))
    priv, dev_pub = await stage_a_pubkey_exchange(t)
    if not (dev_pub and len(dev_pub) >= 64):
        raise RuntimeError("Stage A: device pubkey not received")
    ok = await stage_b_confirm(t, priv, dev_pub, ltmk, crc_be=False)
    if not ok:
        raise RuntimeError("login rejected (0x22) — invalid ltmk/pin")
    print("[+] LOGIN OK")


async def _cmd_value(t, opcode, params=b"", timeout=2.5):
    """
    Command 0x0017 + parsing response [01][len][opcode u16][status][value].
    Strictly matches response opcode with requested (queue may contain other packets).
    Returns (status, value_bytes) or (None, None).
    """
    frame = struct.pack("<HB", opcode, len(params)) + params
    while not t.rx.empty():
        t.rx.get_nowait()
    try:
        await t.client.write_gatt_char(t.chars[CH_DFU_CMD], frame, response=True)
    except Exception:
        return None, None
    for s, b in await t.drain(timeout):
        if s != CH_DFU_CMD or not b or b[0] != 0x01:
            continue
        op_resp, v = parse_cmd_resp(b)
        if op_resp == opcode and v is not None and len(v) >= 1:
            return v[0], v[1:]
    return None, None


async def get_fragment_size(t, op):
    st, v = await _cmd_value(t, op["frag"])
    if st != 0 or len(v) < 2:
        return None
    return struct.unpack_from("<H", v, 0)[0]


async def get_last_index(t, op):
    """Response: [status][lastIndex u16][crc32 u32 LE]. Returns (lastIndex, crc|None)."""
    st, v = await _cmd_value(t, op["last"])
    if st != 0 or len(v) < 2:
        return 0, None
    idx = struct.unpack_from("<H", v, 0)[0]
    crc = struct.unpack_from("<I", v, 2)[0] if len(v) >= 6 else None
    print(f"    [lastFragmentIndex={idx}, device-crc32={'%08x' % crc if crc is not None else '—'}]")
    return idx, crc


async def _next_pkt(t, deadline):
    try:
        return await asyncio.wait_for(t.rx.get(), timeout=max(0.01, deadline - asyncio.get_event_loop().time()))
    except asyncio.TimeoutError:
        return None


async def send_fragment(t, index, data, timeout=5.0, frame_size=None):
    """
    Upload single fragment: message [index u16][data] on 0x0018
    (CTR(fc) -> window=1: 18B frames, pull on ACK 05 reqSeq -> ACK 00), then catch
    DFU event 0x0017 [02 03 status idx].
    Returns fragment status: 0 = accepted, >0 = rejection code, None = transport failure.
    Single common raw queue reading loop to avoid losing 0x0017 event
    arriving adjacent to ACK 00 on 0x0018.
    """
    fs = frame_size or FRAME_SIZE
    msg = struct.pack("<H", index) + data
    frames = [msg[i:i + fs] for i in range(0, len(msg), fs)] or [b""]
    fc = len(frames)
    loop = asyncio.get_event_loop()
    while not t.rx.empty():
        t.rx.get_nowait()

    # CTR + wait for start-ACK
    await t.write(CH_DFU_DATA, struct.pack("<HBBH", 0, PKT_CTR, 0, fc))
    deadline = loop.time() + timeout
    started = False
    while not started:
        p = await _next_pkt(t, deadline)
        if p is None:
            return None
        s, b = p
        if s == CH_DFU_DATA and len(b) >= 4 and b[0] == 0 and b[1] == 0 and b[2] == 0x01:
            started = True

    async def send_seq(n):
        await t.write(CH_DFU_DATA, struct.pack("<H", n) + frames[n - 1], response=False)

    # Send window. MNG yields maxPackageNum (6 for us) — means device is ready
    # to accept several frames before confirmation, rather than strictly one per round-trip.
    # burst=1 — previous behavior (slow but verified).
    burst = fc if BURST in (0, None) else max(1, min(BURST, fc))
    for n in range(1, burst + 1):
        await send_seq(n)
        if burst > 1:
            await asyncio.sleep(0.01)   # pacing W/O-RESP to prevent frame loss
    transport_done = False
    deadline = loop.time() + timeout
    for _ in range((fc + 80) * 3):
        p = await _next_pkt(t, deadline)
        if p is None:
            return None
        s, b = p
        # DFU fragment event on command channel
        if s == CH_DFU_CMD and len(b) >= 3 and b[0] == 0x02 and b[1] == 0x03:
            return b[2]
        if s != CH_DFU_DATA or len(b) < 4 or b[0] != 0 or b[1] != 0 or b[2] != 0x01:
            continue
        status = b[3]
        if status == 0x00:                       # transport accepted entire message
            transport_done = True
            deadline = loop.time() + timeout     # wait for event 02 03
            continue
        if status == 0x05 and len(b) >= 6:       # pull: send reqSeq
            n = struct.unpack_from("<H", b, 4)[0]
            if 1 <= n <= fc:
                await send_seq(n)
                deadline = loop.time() + timeout
    return 0 if transport_done else None


async def flash(t, path, target, commit=False, frame_size=None, limit=None, on_progress=None):
    """on_progress(dict), if specified, is called at the same checkpoints
    printed to console — for UI progress (webui/firmware_worker.py),
    without altering existing console CLI behavior."""
    def _emit(**kw):
        if on_progress:
            on_progress(kw)

    op = OPS[target]
    fw = open(path, "rb").read()
    print(f"\n=== FLASH {target.upper()} : {path} ({len(fw)} bytes) ===")
    _emit(phase="starting", message=f"{target.upper()}: {os.path.basename(path)} ({len(fw)} bytes)")

    frag = await get_fragment_size(t, op)
    if not frag:
        print("[!] getFragmentSize did not respond — aborting")
        _emit(phase="error", success=False, message="getFragmentSize did not respond")
        return False
    last, dev_crc = await get_last_index(t, op)
    N = -(-len(fw) // frag)          # ceil
    # Resume safety (analogous to MeshDfuManager.checkLastFragmentIndex):
    # device-crc32 must match CRC of our file up to last*frag; otherwise buffer has
    # foreign/corrupted image — flash from scratch.
    if last > 0 and dev_crc is not None:
        local_crc = zlib.crc32(fw[:last * frag]) & 0xFFFFFFFF
        if local_crc != dev_crc:
            print(f"[!] resume-CRC mismatch (device={dev_crc:08x}, file={local_crc:08x}) "
                  f"— different image in buffer; flashing from fragment 1")
            last = 0
        else:
            print(f"[i] resume-CRC OK — resuming from fragment {last + 1}")
    print(f"[i] fragmentSize={frag}, lastFragmentIndex={last}, total fragments={N}")
    if last >= N:
        print("[i] device already has all fragments — proceeding to switchFirmware")
    _emit(phase="uploading", index=last, total=N, ok=0, bad=0,
          message=f"fragmentSize={frag}, already uploaded {last}/{N}")

    t0 = time.time()
    n_ok = n_bad = 0
    stop_at = N if limit is None else min(N, last + limit)
    if stop_at < N:
        print(f"[i] --limit: uploading only fragments {last+1}..{stop_at} of {N} "
              f"(speed measurement, commit disabled)")
    for index in range(last + 1, stop_at + 1):
        data = fw[(index - 1) * frag: index * frag]
        st = await send_fragment(t, index, data, frame_size=frame_size)
        if st is None:
            print(f"\n[!] fragment {index}/{N}: transport failure (no ACK 00 / no event)")
            _emit(phase="error", success=False,
                  message=f"fragment {index}/{N}: transport failure")
            return False
        if st == 0:
            n_ok += 1
        else:
            n_bad += 1
            # do not abort on status != 0: testing hypothesis that fragment is still
            # buffered (05 at session start). Outcome checked via CRC below.
            if n_bad <= 3 or index == last + 1:
                print(f"\n  [~] fragment {index}/{N}: status={st} ({FRAG_STATUS.get(st,'?')}) — continuing")
            # if MULTIPLE consecutive non-zeros and no OK — genuine failure
            if n_bad >= 8 and n_ok == 0:
                print(f"\n[!] {n_bad} consecutive fragments with status != 0 and none OK — failure, aborting")
                _emit(phase="error", success=False,
                      message=f"{n_bad} consecutive fragments rejected, none OK")
                return False
        if index % 10 == 0 or index == N:
            spd = index / max(time.time() - t0, 0.1)
            eta = (N - index) / max(spd, 0.1)
            print(f"\r  fragment {index}/{N} ({100*index//N}%) ok={n_ok} bad={n_bad} "
                  f"{spd:.1f}fr/s ETA {eta:.0f}s   ", end="", flush=True)
            _emit(phase="uploading", index=index, total=N, ok=n_ok, bad=n_bad,
                  speed_kbps=spd * frag / 1024, eta_sec=eta,
                  message=f"{index}/{N} ({100*index//N}%) ok={n_ok} bad={n_bad}")
    dt = time.time() - t0
    sent = max(stop_at - last, 0)
    kbps = (sent * frag) / max(dt, 0.001) / 1024
    print(f"\n[i] upload completed in {dt:.0f}s (ok={n_ok}, status!=0={n_bad})")
    print(f"[i] SPEED: frame={frame_size or FRAME_SIZE}B, {sent} frags in {dt:.1f}s "
          f"= {kbps:.2f} KB/s ({sent/max(dt,0.001):.2f} frags/s)")
    if stop_at < N:
        print("[i] --limit specified: image uploaded partially, not sending switchFirmware.")
        _emit(phase="done", success=True, message="partial upload (--limit)")
        return True

    # FINAL CHECK: did device actually accept the entire image?
    last2, crc2 = await get_last_index(t, op)
    full_crc = zlib.crc32(fw) & 0xFFFFFFFF
    exp_crc = zlib.crc32(fw[:last2 * frag]) & 0xFFFFFFFF if last2 else None
    crc2s = f"{crc2:08x}" if crc2 is not None else "—"
    print(f"[i] after upload: lastFragmentIndex={last2}/{N}, device-crc={crc2s}")
    accepted = (last2 >= N) and (crc2 is not None) and (crc2 == full_crc)
    if accepted:
        print(f"[+] ENTIRE IMAGE ACCEPTED by device (full file crc {full_crc:08x} matched).")
    elif last2 and exp_crc is not None and crc2 == exp_crc:
        print(f"[i] accepted {last2}/{N} fragments (crc matched up to this point) — image partially written.")
    else:
        print(f"[!] image NOT verified: lastIndex={last2}, device-crc={crc2}, "
              f"expected full {full_crc:08x}.")
        _emit(phase="error", success=False, message="image not verified by device after upload")
        return False

    if not commit:
        print("[i] --commit not specified: NOT sending switchFirmware. Image uploaded to buffer;\n"
              "    incomplete DFU will be reset by device. Rerun with --commit to complete.")
        _emit(phase="done", success=True, message="image uploaded and verified, awaiting switch")
        return True

    print("\n[!!!] switchFirmware is an IRREVERSIBLE operation (brick risk). Sending…")
    _emit(phase="committing", message="sending switchFirmware (irreversible)")
    r = await dfu_cmd(t, op["switch"], struct.pack("<I", 1))  # k81.OooOO0(1) = 01 00 00 00
    print(f"    switchFirmware resp: {r.hex() if r else None}")

    if target == "mcu":
        # MCU installation is asynchronous: BLE chip relays image to controller via USART3,
        # MCU flashes itself. Mi Home polls MCU version until it changes at this step
        # (MeshDfuManager->pollMcuVersion: frame [01] on 0x001c). We replicate this.
        _emit(phase="committing", message="switchFirmware sent — waiting for MCU version change (up to 3 min)")
        ok = await poll_mcu_version(t, expected_before=None)
        if ok is True:
            print("[+] MCU reported NEW version — firmware applied.")
            _emit(phase="done", success=True, message="MCU reported new version — firmware applied")
        elif ok is False:
            print("[!] MCU version did not change within timeout. This does NOT mean failure:\n"
                  "    installation may continue beyond timeout. Verify version later\n"
                  "    (python probes/mcu_opcode_sweep.py --max 1 --repeat 0).")
            _emit(phase="done", success=None,
                  message="switchFirmware sent, but MCU version did not change within timeout — verify later")
        else:
            print("[!] MCU did not respond to version poll (may be rebooting).")
            _emit(phase="done", success=None,
                  message="switchFirmware sent, MCU did not respond to poll (may be rebooting)")
        return True

    print("[+] Switch command sent. Device will reboot and apply firmware.")
    _emit(phase="done", success=True, message="switchFirmware sent, device will reboot")
    return True


async def poll_mcu_version(t, expected_before=None, timeout=180.0, interval=3.0):
    """Poll MCU version until it changes — like MeshDfuManager->pollMcuVersion.

    Frame is single-byte [0x01] (opcode 1 = mcu_version) on info-channel 0x001c,
    response: [01][len][ascii-version]. Read-only.

    Returns True (version changed), False (timeout without change) or None (no response).
    """
    CH_INFO = 0x001C
    if CH_INFO not in t.chars:
        print("    [!] characteristic 0x001c unavailable — polling not possible")
        return None

    inbox = []

    def on_info(sender, data):
        if sid(sender) == CH_INFO:
            inbox.append(bytes(data))

    await t.client.start_notify(t.chars[CH_INFO], on_info)

    async def read_version():
        inbox.clear()
        try:
            await t.client.write_gatt_char(t.chars[CH_INFO], b"\x01", response=False)
        except Exception as e:
            print(f"    [!] write to 0x001c: {e}")
            return None
        await asyncio.sleep(1.0)
        for b in inbox:
            if len(b) >= 2 and b[0] == 0x01:
                return b[2:2 + b[1]].decode("ascii", "replace")
        return None

    try:
        if expected_before is None:
            expected_before = await read_version()
            print(f"    MCU version before install: {expected_before!r}")
        print(f"    polling MCU version (up to {timeout:.0f} s, interval {interval:.0f} s)...")
        loop = asyncio.get_event_loop()
        deadline = loop.time() + timeout
        seen_silence = 0
        while loop.time() < deadline:
            await asyncio.sleep(interval)
            v = await read_version()
            left = int(deadline - loop.time())
            if v is None:
                seen_silence += 1
                print(f"    [{left:>3}s] no response (MCU rebooting?)")
                continue
            seen_silence = 0
            if expected_before is not None and v != expected_before:
                print(f"    [{left:>3}s] version changed: {expected_before!r} -> {v!r}")
                return True
            print(f"    [{left:>3}s] version currently {v!r}")
        return None if seen_silence and expected_before is None else False
    finally:
        try:
            await t.client.stop_notify(t.chars[CH_INFO])
        except Exception:
            pass


async def main():
    argv = sys.argv[1:]
    args = [a for a in argv if not a.startswith("--")]
    flags = {a for a in argv if a.startswith("--")}
    poll_to = 180.0
    frame_size = None
    limit = None
    for a in argv:
        if a.startswith("--poll-timeout="):
            poll_to = float(a.split("=", 1)[1])
        elif a.startswith("--frame-size="):
            frame_size = int(a.split("=", 1)[1])
        elif a.startswith("--limit="):
            limit = int(a.split("=", 1)[1])
        elif a.startswith("--burst="):
            globals()["BURST"] = int(a.split("=", 1)[1])

    # "MCU version poll only" mode — flashes nothing
    if args and args[0] == "poll-mcu":
        mac = args[1] if len(args) > 1 else MAC_DEFAULT
        ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
        t = Transport(mac)
        try:
            await login(t, ltmk)
            res = await poll_mcu_version(t, timeout=poll_to)
            print({True: "[+] version changed",
                   False: "[i] version did not change within timeout",
                   None: "[!] MCU did not respond"}[res])
            return 0
        except Exception:
            import traceback; traceback.print_exc(); return 1
        finally:
            await t.close()

    if len(args) < 2 or args[0] not in OPS:
        print(__doc__); return 2
    target, path = args[0], args[1]
    mac = args[2] if len(args) > 2 else MAC_DEFAULT
    commit = "--commit" in flags

    if commit and "--yes" not in flags:
        print("[!] --commit also requires --yes (confirmation of irreversible flashing).")
        return 2

    ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
    t = Transport(mac)
    try:
        await login(t, ltmk)
        ok = await flash(t, path, target, commit=commit,
                         frame_size=frame_size, limit=limit)
        return 0 if ok else 1
    except Exception:
        import traceback; traceback.print_exc(); return 1
    finally:
        await t.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
