#!/usr/bin/env python3
"""
Opcode sweep of MCU channel 0x001c (unauthenticated) searching for telemetry
(battery, speed, mileage, temperature, errors).

SAFETY: sends single-byte frames [op] ONLY — in MCU protocol
getter = [op], setter = [op][len][data]. Without len-byte device cannot
accept payload, ensuring queries are purely read operations.

Known (already decoded) opcodes: 0, 1=mcu_version, 3=hardware, 8=serial.

Usage:  python mcu_opcode_sweep.py [--max 63] [--mac 2C:19:5C:DE:DE:88]
"""
import argparse
import asyncio

import os as _os, sys as _sys
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
_sys.path.insert(0, _os.path.join(_ROOT, "core"))

from dreame_auth import Transport, MAC_DEFAULT, CH_MCU, sid

KNOWN = {0: "?", 1: "mcu_version", 3: "hardware", 8: "serial/newSN"}


def describe(payload: bytes) -> str:
    """Payload interpretation guesses."""
    hints = []
    if payload and all(32 <= c < 127 for c in payload):
        hints.append(f"ascii='{payload.decode('ascii')}'")
    if len(payload) == 1:
        v = payload[0]
        hints.append(f"u8={v}")
        if 0 <= v <= 100:
            hints.append("MAY BE %")
    if len(payload) == 2:
        le = int.from_bytes(payload, "little")
        be = int.from_bytes(payload, "big")
        hints.append(f"u16le={le} u16be={be}")
        for name, val in (("le", le), ("be", be)):
            if 3000 <= val <= 4300:
                hints.append(f"MAY BE cell mV ({name})")
            elif 30000 <= val <= 45000:
                hints.append(f"MAY BE pack mV/10 ({name})")
    if len(payload) == 4:
        hints.append(f"u32le={int.from_bytes(payload, 'little')}")
    if len(payload) >= 4 and len(payload) % 2 == 0:
        words = [int.from_bytes(payload[i:i + 2], "little")
                 for i in range(0, len(payload), 2)]
        hints.append(f"u16le[]={words}")
    return "  ".join(hints)


async def sweep(mac: str, max_op: int, repeat: int, step_wait: float = 1.0):
    t = Transport(mac)
    await t.connect()
    if CH_MCU not in t.chars:
        print("[!] characteristic 0x001c not found")
        return

    inbox = []

    def on_mcu(sender, data):
        if sid(sender) == CH_MCU:
            inbox.append(bytes(data))

    # core already subscribed in connect(); add collector
    await t.client.start_notify(t.chars[CH_MCU], on_mcu)

    async def query(op: int, wait: float = 1.0):
        inbox.clear()
        await t.client.write_gatt_char(t.chars[CH_MCU], bytes([op]), response=False)
        await asyncio.sleep(wait)
        return list(inbox)

    print(f"\n=== probing opcodes 0..{max_op} on 0x001c ===\n")
    found, silent = [], []
    # err 0x02 = opcode absent; any other code = opcode EXISTS, frame rejected
    unsupported, needs_param = [], []

    for op in range(max_op + 1):
        replies = await query(op, wait=step_wait)
        tag = f"[{KNOWN[op]}]" if op in KNOWN else ""
        if not replies:
            silent.append(op)
            print(f"op {op:>3} {tag:<14} — silence")
            continue
        for r in replies:
            if r and r[0] == 0xFF:
                err = r[3] if len(r) > 3 else None
                if err == 0x02:
                    unsupported.append(op)
                    print(f"op {op:>3} {tag:<14} no opcode     {r.hex()}")
                else:
                    needs_param.append((op, err))
                    print(f"op {op:>3} {tag:<14} EXISTS, err=0x{err:02x} <<< {r.hex()}")
                continue
            payload = r[2:2 + r[1]] if len(r) >= 2 else b""
            found.append((op, r, payload))
            print(f"op {op:>3} {tag:<14} OK   raw={r.hex()}")
            if payload:
                print(f"{'':>21}{describe(payload)}")

    # re-polling found opcodes: variable values = live telemetry
    if repeat and found:
        print(f"\n=== re-polling responsive opcodes ({repeat} passes) ===")
        history = {op: [] for op, _, _ in found}
        for _ in range(repeat):
            for op in list(history):
                replies = await query(op, wait=0.6)
                r = replies[0] if replies else b""
                history[op].append(r.hex())
            await asyncio.sleep(0.5)
        print("\n--- dynamics ---")
        for op, vals in history.items():
            uniq = len(set(vals))
            mark = "CHANGING <<<" if uniq > 1 else "static"
            print(f"op {op:>3}: {mark}  {vals}")

    print("\n=== SUMMARY ===")
    print(f"returned data      : {[op for op, _, _ in found]}")
    print(f"EXISTS, needs param: {[(op, hex(e)) for op, e in needs_param]}")
    print(f"no opcode (err 02) : {len(unsupported)} count: {unsupported}")
    print(f"silence             : {silent}")

    try:
        await t.client.stop_notify(t.chars[CH_MCU])
    except Exception:
        pass
    await t.client.disconnect()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mac", default=MAC_DEFAULT)
    ap.add_argument("--max", type=int, default=63, help="upper opcode boundary")
    ap.add_argument("--repeat", type=int, default=3,
                    help="re-polling passes for discovered opcodes (0 = disable)")
    ap.add_argument("--wait", type=float, default=1.0,
                    help="pause after each opcode, s")
    a = ap.parse_args()
    asyncio.run(sweep(a.mac, a.max, a.repeat, a.wait))


if __name__ == "__main__":
    main()
