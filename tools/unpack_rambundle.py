#!/usr/bin/env python3
"""Unpack React Native indexed RAM bundle (magic 0xFB0BD1E5) into separate JS modules.

Format:
    uint32 magic = 0xFB0BD1E5
    uint32 module_count
    uint32 startup_code_len
    module_count * {uint32 offset, uint32 length} — module table
    startup code, followed by module bodies

Usage:  python tools/unpack_rambundle.py <main.bundle> <out-dir>
"""
import os
import struct
import sys

MAGIC = 0xFB0BD1E5


def unpack(path, out_dir):
    d = open(path, "rb").read()
    magic, count, startup_len = struct.unpack("<III", d[:12])
    if magic != MAGIC:
        print(f"not an indexed RAM bundle: magic=0x{magic:08x}")
        return 1
    table_end = 12 + count * 8
    print(f"modules in table: {count}   startup_code_len={startup_len}")
    print(f"table: 12..{table_end}   file size: {len(d)}")

    os.makedirs(out_dir, exist_ok=True)
    written = empty = bad = 0
    sizes = []
    for i in range(count):
        off, ln = struct.unpack("<II", d[12 + i * 8: 20 + i * 8])
        if off == 0 and ln == 0:
            empty += 1
            continue
        start = table_end + off
        body = d[start:start + ln]
        if not body:
            bad += 1
            continue
        body = body.rstrip(b"\x00")
        with open(os.path.join(out_dir, f"{i:05d}.js"), "wb") as f:
            f.write(body)
        written += 1
        sizes.append(len(body))

    print(f"written: {written}   empty entries: {empty}   corrupted: {bad}")
    if sizes:
        print(f"module sizes: min={min(sizes)} max={max(sizes)} sum={sum(sizes)}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(unpack(sys.argv[1], sys.argv[2]))
