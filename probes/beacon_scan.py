#!/usr/bin/env python3
"""
Scan scooter BLE advertisements and parse MiBeacon (service data FE95).

Hypothesis: telemetry (battery etc.) is broadcast via MiBeacon objects in
advertisements rather than GATT — matching Xiaomi BLE devices without MIoT properties.
Scooter 5 Pro MIoT spec lacks telemetry properties, GATT channels are silent,
and we hold the device key → primary remaining software route.

Completely passive: listens only, writes nothing, does not connect.

Usage:  python beacon_scan.py [--secs 30]
"""
import argparse
import asyncio
import struct

from bleak import BleakScanner

MAC = "2C:19:5C:DE:DE:88"
FE95 = "0000fe95-0000-1000-8000-00805f9b34fb"

# known MiBeacon object types (subset relevant to transport)
OBJ = {
    0x1001: "button/event",
    0x1004: "temperature",
    0x1006: "humidity",
    0x100A: "BATTERY %",
    0x100D: "temperature+humidity",
    0x1010: "formaldehyde",
    0x1017: "idle",
    0x1018: "illumination",
    0x1019: "door",
    0x000B: "lock",
}

def fc_bits(fctrl: int) -> dict:
    """Canonical MiBeacon frame_control fields (matching xiaomi_ble/ble_monitor)."""
    return {
        "version": fctrl >> 12,
        "auth_mode": (fctrl >> 10) & 3,
        "solicited": (fctrl >> 9) & 1,
        "registered": (fctrl >> 8) & 1,
        "mesh": (fctrl >> 7) & 1,
        "object": (fctrl >> 6) & 1,
        "capability": (fctrl >> 5) & 1,
        "mac": (fctrl >> 4) & 1,
        "encrypted": (fctrl >> 3) & 1,
        "req_timing": fctrl & 1,
    }


def parse_mibeacon(sd: bytes):
    if len(sd) < 5:
        return f"too short: {sd.hex()}"
    fctrl, pid, cnt = struct.unpack("<HHB", sd[:5])
    f = fc_bits(fctrl)
    on = ", ".join(k for k, v in f.items() if k not in ("version", "auth_mode") and v)
    out = [f"frame_ctrl=0x{fctrl:04x} version={f['version']} "
           f"auth_mode={f['auth_mode']} [{on or '-'}]",
           f"product_id=0x{pid:04x}", f"frame_cnt={cnt}"]
    i = 5
    if f["mac"]:
        out.append("mac=" + sd[i:i + 6][::-1].hex(":"))
        i += 6
    if f["capability"] and i < len(sd):
        out.append(f"capability=0x{sd[i]:02x}")
        i += 1
    rest = sd[i:]
    if not rest:
        out.append("NO payload — identification only (no telemetry in advertisement)")
        return "\n     ".join(out)
    if f["encrypted"]:
        # cipher: [ciphertext][ext_cnt 3][mic 4]
        if len(rest) >= 7:
            ct, ext, mic = rest[:-7], rest[-7:-4], rest[-4:]
            out.append(f"ENCRYPTED ct={ct.hex()} ext_cnt={ext.hex()} mic={mic.hex()}")
        else:
            out.append(f"ENCRYPTED (short) {rest.hex()}")
    elif f["object"]:
        while len(rest) >= 3:
            otype, olen = struct.unpack("<HB", rest[:3])
            val = rest[3:3 + olen]
            name = OBJ.get(otype, "?")
            extra = ""
            if olen == 1:
                extra = f" u8={val[0]}"
            elif olen == 2:
                extra = f" u16le={int.from_bytes(val, 'little')}"
            out.append(f"OBJ 0x{otype:04x} ({name}) len={olen} {val.hex()}{extra}")
            rest = rest[3 + olen:]
    else:
        out.append(f"no objects, tail={rest.hex()}")
    return "\n     ".join(out)


async def run(secs: float, mac: str):
    seen = {}
    print(f"=== listening to advertisements for {secs:.0f} s (scooter powered ON) ===\n")

    def cb(dev, adv):
        if dev.address.upper() != mac.upper():
            return
        for uuid, sd in (adv.service_data or {}).items():
            key = (uuid, bytes(sd))
            if key in seen:
                seen[key] += 1
                return
            seen[key] = 1
            print(f"[{dev.address}] rssi={adv.rssi} name={adv.local_name!r}")
            print(f"  service_data {uuid}")
            print(f"  raw: {bytes(sd).hex()}")
            if uuid.lower() == FE95:
                print("     " + parse_mibeacon(bytes(sd)))
            print()
        for cid, md in (adv.manufacturer_data or {}).items():
            key = ("md", cid, bytes(md))
            if key not in seen:
                seen[key] = 1
                print(f"  manufacturer 0x{cid:04x}: {bytes(md).hex()}\n")

    scanner = BleakScanner(detection_callback=cb)
    await scanner.start()
    await asyncio.sleep(secs)
    await scanner.stop()

    print("=== SUMMARY ===")
    if not seen:
        print("scooter is not advertising (sleeping / already connected to phone?)")
    for k, n in seen.items():
        payload = k[1] if k[0] != "md" else k[2]
        print(f"{n:>4}x  {payload.hex() if isinstance(payload, bytes) else payload}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--secs", type=float, default=30.0)
    ap.add_argument("--mac", default=MAC)
    a = ap.parse_args()
    asyncio.run(run(a.secs, a.mac))
