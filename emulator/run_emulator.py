#!/usr/bin/env python3
"""Run real project tools against device emulator (without BLE).

Substitutes dreame_auth.BleakClient with FakeBleakClient and runs:
1) login (dreame_auth Stage A+B) — crypto round-trip verification;
2) DFU BLE of identical version -> switchFirmware rejected (status 6), matching hardware;
3) DFU BLE of NEW version -> switchFirmware APPLIED, version incremented;
4) info channel 0x001c: version / hardware / serial;
5) spec telemetry channel (0x001a/0x001b) via spec_read.py;
6) spontaneous push notification upon property change (0x001b).

Usage:  python emulator/run_emulator.py
"""
import asyncio
import os
import struct
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "core"))
sys.path.insert(0, os.path.join(ROOT, "probes"))
sys.path.insert(0, os.path.join(ROOT, "emulator"))

import dreame_auth as da  # noqa: E402
import fake_ble  # noqa: E402
from scooter_device import ScooterDevice  # noqa: E402

# Shared emulated device instance (one per run)
DEVICE = {"obj": None}


def _load_ltmk():
    # Emulator does NOT require device's real key — both sides (client and
    # ScooterDevice) share the same value; real ECDH round-trip works with any
    # 32-byte ltmk. If secrets/ltmk.hex does not exist, use fixed test key.
    p = os.path.join(ROOT, "secrets", "ltmk.hex")
    if os.path.exists(p):
        try:
            val = open(p).read().strip()
            if len(val) == 64:
                return bytes.fromhex(val)
        except Exception:
            pass
    return bytes.fromhex("0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef")


def make_device():
    return DEVICE["obj"]


def install_fake():
    fake_ble.FakeBleakClient._device_factory = make_device
    da.BleakClient = fake_ble.FakeBleakClient


def make_fake_image(size, tag=b"EMUIMG"):
    """Synthetic firmware image of requested size (deterministic CRC)."""
    import struct
    body = bytearray()
    i = 0
    while len(body) < size:
        body += struct.pack("<I", i) + tag
        i += 1
    return bytes(body[:size])


async def scenario_login():
    print("\n" + "=" * 60)
    print("SCENARIO 1: login (crypto round-trip)")
    print("=" * 60)
    import dreame_flasher as df
    ltmk = _load_ltmk()
    t = da.Transport(da.MAC_DEFAULT)
    try:
        await df.login(t, ltmk)
        print("RESULT: login passed via emulator ✅"
              if DEVICE["obj"].logged_in else "RESULT: login FAILED ❌")
    finally:
        await t.close()


async def flash_via_tools(target, image_path, commit):
    import dreame_flasher as df
    ltmk = _load_ltmk()
    t = da.Transport(da.MAC_DEFAULT)
    try:
        await df.login(t, ltmk)
        return await df.flash(t, image_path, target, commit=commit)
    finally:
        await t.close()


async def scenario_same_version():
    print("\n" + "=" * 60)
    print("SCENARIO 2: DFU BLE SAME version -> expect REJECTION (status 6)")
    print("=" * 60)
    dev = DEVICE["obj"]
    dev.offered_ble_version = dev.ble_version
    img = make_fake_image(3000)
    path = os.path.join(tempfile.gettempdir(), "emu_same.bin")
    open(path, "wb").write(img)
    before = dev.ble_version
    await flash_via_tools("ble", path, commit=True)
    print(f"RESULT: BLE version {before} -> {dev.ble_version} "
          f"({'UNCHANGED, refusal triggered ✅' if dev.ble_version == before else 'CHANGED ❌'})")


async def scenario_296_boundary():
    print("\n" + "=" * 60)
    print("SCENARIO 2.5: accept_limit boundary (296/301 model) on SAME version")
    print("=" * 60)
    dev = DEVICE["obj"]
    dev.offered_ble_version = dev.ble_version
    dev.accept_limit = 10
    dev.ble_buf = bytearray()
    dev.ble_last = 0
    img = make_fake_image(15 * 512)
    path = os.path.join(tempfile.gettempdir(), "emu_296.bin")
    open(path, "wb").write(img)
    await flash_via_tools("ble", path, commit=False)
    capped_ok = dev.ble_last == 10
    print(f"RESULT: device stopped at lastFragmentIndex={dev.ble_last}/15 "
          f"(accept_limit=10) {'✅' if capped_ok else '❌'} "
          f"— matches physical 296/301 behavior (docs/FACTS.md).")
    dev.accept_limit = None
    dev.ble_buf = bytearray()
    dev.ble_last = 0


async def scenario_upgrade():
    print("\n" + "=" * 60)
    print("SCENARIO 3: DFU BLE NEW version -> expect SUCCESS (switchFirmware)")
    print("=" * 60)
    dev = DEVICE["obj"]
    dev.offered_ble_version = "2.8.0_0001"
    img = make_fake_image(3000)
    path = os.path.join(tempfile.gettempdir(), "emu_new.bin")
    open(path, "wb").write(img)
    before = dev.ble_version
    await flash_via_tools("ble", path, commit=True)
    ok = dev.ble_version == "2.8.0_0001"
    print(f"RESULT: BLE version {before} -> {dev.ble_version} "
          f"({'FIRMWARE APPLIED ✅' if ok else 'NOT applied ❌'})")


async def scenario_info():
    print("\n" + "=" * 60)
    print("SCENARIO 4: info channel 0x001c")
    print("=" * 60)
    dev = DEVICE["obj"]
    t = da.Transport(da.MAC_DEFAULT)
    try:
        await t.connect()
        for op, name in ((1, "mcu_version"), (3, "hardware")):
            t.rx = asyncio.Queue()
            outs = dev.on_write(0x001C, bytes([op]))
            for s, b in outs:
                val = b[2:2 + b[1]]
                print(f"  opcode {op} ({name}): {val.decode('ascii','replace')}")
    finally:
        await t.close()


async def scenario_telemetry():
    print("\n" + "=" * 60)
    print("SCENARIO 5: spec telemetry channel (0x001a/0x001b), real probes/spec_read.py")
    print("=" * 60)
    import dreame_flasher as df
    import spec_read as sr
    ltmk = _load_ltmk()
    t = da.Transport(da.MAC_DEFAULT)
    try:
        await df.login(t, ltmk)
        sk = da.LAST_SK
        single = [(1, 2), (1, 4), (1, 7), (2, 6), (3, 2), (4, 5)]
        all_ok = True
        for i, obj in enumerate(single):
            pt = await sr.spec_request(t, sk, [obj], app_cnt=i)
            lines = sr.parse_reply(pt) if pt else ["[!] no response"]
            got = pt is not None and "empty" not in "".join(lines)
            all_ok &= got
            print("  " + lines[-1] if len(lines) > 1 else "  " + lines[0])
        print(f"RESULT: emulator telemetry read by real spec_read.py "
              f"(per property) {'✅' if all_ok else '❌'}")

        pt2 = await sr.spec_request(t, sk, [(1, 2), (1, 4)], app_cnt=len(single))
        lines2 = sr.parse_reply(pt2) if pt2 else []
        first_ok = any("BATTERY_LEVEL" in ln and "empty" not in ln for ln in lines2)
        second_no_data = any("VOLTAGE" in ln and "status=61533" in ln for ln in lines2)
        print(f"RESULT: multi-object emulated matching hardware "
              f"(first object present, second -> status) "
              f"{'✅' if first_ok and second_no_data else '❌'}")
    finally:
        await t.close()


async def scenario_push():
    print("\n" + "=" * 60)
    print("SCENARIO 6: spontaneous push on property change (0x001b), unsolicited")
    print("=" * 60)
    import dreame_flasher as df
    import spec_read as sr
    dev = DEVICE["obj"]
    ltmk = _load_ltmk()
    t = da.Transport(da.MAC_DEFAULT)
    try:
        await df.login(t, ltmk)
        sk = da.LAST_SK

        out = dev.push_property(4, 5, "unused")
        print(f"  push outside SUBSCRIBABLE -> {'nothing sent ✅' if not out else 'ERROR, push sent ❌'}")

        while not t.rx.empty():
            t.rx.get_nowait()
        t.client.notify_now(dev.push_property(2, 7, 2))

        s, b = await asyncio.wait_for(t.rx.get(), timeout=2.0)
        is_ctr = s == 0x001B and len(b) >= 6 and b[0] == 0 and b[1] == 0 and b[2] == 0x00
        print(f"  unsolicited CTR from device: {'received ✅' if is_ctr else 'NOT received ❌'}")
        if not is_ctr:
            print("RESULT: push not working ❌")
            return
        fc = struct.unpack("<H", b[4:6])[0]
        await t.write(0x001B, struct.pack("<HBB", 0, 0x01, 0x01))   # ready to receive
        parts = {}
        for _ in range(fc):
            s2, b2 = await asyncio.wait_for(t.rx.get(), timeout=2.0)
            seq = struct.unpack("<H", b2[:2])[0]
            parts[seq] = b2[2:]
        await t.write(0x001B, struct.pack("<HBB", 0, 0x01, 0x00))   # accepted all
        payload = b"".join(parts[i] for i in sorted(parts))
        cnt = struct.unpack("<H", payload[:2])[0]
        pt = sr.dec_dev(sk, cnt, payload[2:])
        lines = sr.parse_reply(pt)
        for line in lines:
            print("  " + line)
        ok = any("IS_RIDING" in ln and "empty" not in ln for ln in lines)
        print(f"RESULT: IS_RIDING push decrypted by real spec_read.dec_dev "
              f"{'✅' if ok else '❌'}")
    finally:
        await t.close()


async def main():
    install_fake()
    ltmk = _load_ltmk()
    DEVICE["obj"] = ScooterDevice(ltmk, ble_version="2.7.0_0015",
                                  mcu_version="0007", verbose=True)
    await scenario_login()
    DEVICE["obj"].logged_in = False
    await scenario_same_version()
    await scenario_296_boundary()
    await scenario_upgrade()
    await scenario_info()
    DEVICE["obj"].logged_in = False
    await scenario_telemetry()
    DEVICE["obj"].logged_in = False
    await scenario_push()
    print("\n" + "=" * 60)
    print("DONE. Emulator completed test run against real dreame_auth/dreame_flasher without BLE.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
