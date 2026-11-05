#!/usr/bin/env python3
"""Inspect downloaded Mi Home plugin bundle for telemetry protocol logic.

Classifies bundle contents (RN JS bundle vs native .so) and searches for
protocol signatures: BLE characteristics, channel transports, opcodes, battery.

Usage:  python tools/inspect_plugin.py <bundle-file> [--extract-dir DIR]
"""
import argparse
import os
import re
import zipfile

# what to search for in text/binary resources
PATTERNS = [
    (rb"0000fe95|fe95", "FE95 service UUID"),
    (rb"0000001[0-9a-f]-0000-1000", "Mijia char UUID"),
    (rb"battery|batteryLevel|soc|remainCapacity", "BATTERY"),
    (rb"mileage|odometer|totalMileage|speed|rpm", "MILEAGE/SPEED"),
    (rb"securitychipauth|securityChip", "security-chip login"),
    (rb"writeCharacteristic|readCharacteristic|notifyChar", "BLE operations"),
    (rb"spec_?value|siid|piid|miotSpec", "MIoT spec"),
    (rb"55\s*aa|0x55AA|P4v2", "serial protocol 55AA/P4"),
    (rb"channel|Channel", "channel transport"),
    (rb"opcode|opCode|cmdId|command_id", "opcodes/commands"),
]

TEXTY = (".js", ".jsx", ".json", ".bundle", ".txt", ".xml", ".html", ".ts", ".map")


def classify(names):
    kinds = {"RN/JS": [], "native .so": [], "resources": [], "other": []}
    for n in names:
        low = n.lower()
        if low.endswith((".js", ".jsx", ".bundle", ".map", ".ts")):
            kinds["RN/JS"].append(n)
        elif low.endswith(".so"):
            kinds["native .so"].append(n)
        elif low.endswith((".png", ".jpg", ".webp", ".gif", ".ttf", ".json", ".xml")):
            kinds["resources"].append(n)
        else:
            kinds["other"].append(n)
    return kinds


def scan_blob(data, label, out):
    for pat, name in PATTERNS:
        hits = list(re.finditer(pat, data, re.I))
        if hits:
            out.setdefault(name, []).append((label, len(hits), hits[0].start()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bundle")
    ap.add_argument("--extract-dir", default=None)
    a = ap.parse_args()

    if not zipfile.is_zipfile(a.bundle):
        size = os.path.getsize(a.bundle)
        head = open(a.bundle, "rb").read(64)
        print(f"NOT a zip archive ({size} B). First bytes: {head[:32].hex()}")
        print("Possible standalone JS bundle or encrypted container.")
        data = open(a.bundle, "rb").read()
        found = {}
        scan_blob(data, os.path.basename(a.bundle), found)
        for k, v in found.items():
            print(f"  [{k}] {v}")
        return 0

    zf = zipfile.ZipFile(a.bundle)
    names = zf.namelist()
    print(f"=== {a.bundle}: {len(names)} entries ===\n")
    for kind, items in classify(names).items():
        print(f"{kind}: {len(items)}")
        for n in items[:15]:
            info = zf.getinfo(n)
            print(f"   {n}  ({info.file_size} B)")
        if len(items) > 15:
            print(f"   ... and {len(items) - 15} more")
        print()

    print("=== scanning for protocol traces ===")
    found = {}
    for n in names:
        info = zf.getinfo(n)
        if info.file_size > 40 * 1024 * 1024:
            continue
        try:
            data = zf.read(n)
        except Exception:
            continue
        scan_blob(data, n, found)
    if not found:
        print("none of the target patterns found")
    for name, hits in sorted(found.items()):
        print(f"\n[{name}]")
        for label, cnt, pos in hits[:8]:
            print(f"   {label}: {cnt} match(es) (first @{pos})")

    if a.extract_dir:
        os.makedirs(a.extract_dir, exist_ok=True)
        zf.extractall(a.extract_dir)
        print(f"\nextracted to {a.extract_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
