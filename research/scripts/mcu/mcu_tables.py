#!/usr/bin/env python3
"""
Search for calibration/lookup tables in MCU firmware (mcu_0007.bin).

Idea: scooter controller thresholds and curves (temperature, current, speed, derating)
reside in constant tables. They appear as long MONOTONIC sequences of u16/i16 -
unlike code where values are scattered.

Found this way (see REPORT.md): block of tables around 0x17f80-0x18010, including
temperature axis -10..50 deg C and axes 0..10000 (step 500) and 0..800 (step 100).

Usage:  python research/scripts/mcu/mcu_tables.py [--min-len 6] [--bin <mcu_0007.bin>]
"""
import argparse
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(os.path.dirname(HERE))   # research/


def read_u16(d, i, signed=False):
    return struct.unpack_from("<h" if signed else "<H", d, i)[0]


def find_runs(d, min_len=6, signed=False):
    """Monotonic (strictly increasing) sequences of u16/i16."""
    runs = []
    i = 0
    n = len(d) - 2
    while i < n:
        j = i
        vals = [read_u16(d, j, signed)]
        while j + 4 <= len(d):
            nxt = read_u16(d, j + 2, signed)
            if nxt <= vals[-1]:
                break
            vals.append(nxt)
            j += 2
        if len(vals) >= min_len:
            runs.append((i, vals))
            i = j + 2
        else:
            i += 2
    return runs


def classify(vals):
    """Short characteristic of series: constant step? resembles what?"""
    diffs = [b - a for a, b in zip(vals, vals[1:])]
    uniform = len(set(diffs)) == 1
    tags = []
    if uniform:
        tags.append(f"uniform step {diffs[0]}")
    else:
        tags.append(f"steps {min(diffs)}..{max(diffs)}")
    lo, hi = vals[0], vals[-1]
    if lo >= -40 and hi <= 130 and len(vals) <= 16:
        tags.append("POSSIBLY temperature deg C")
    if hi <= 100 and lo >= 0:
        tags.append("POSSIBLY percentage")
    if 3000 <= hi <= 60000 and lo >= 0:
        tags.append("mV / mA / RPM?")
    return "; ".join(tags)


def dump_battery_curves(d, start=0x18036, lo=2500, hi=4400, drop=50):
    """Segmentation of cell voltage curves block: boundary visible by sharp drop."""
    curves, cur, off, cstart = [], [], start, start
    while off + 2 <= len(d):
        v = struct.unpack_from("<H", d, off)[0]
        if not (lo <= v <= hi):
            break
        if cur and v < cur[-1] - drop:
            curves.append((cstart, cur))
            cur, cstart = [], off
        cur.append(v)
        off += 2
    if cur:
        curves.append((cstart, cur))
    print(f"\n=== cell voltage curves block: 0x{start:05x}..0x{off:05x} "
          f"({off - start} B), curves {len(curves)} ===")
    prev = None
    for i, (o, v) in enumerate(curves):
        mark = "   <-- new group" if prev is not None and v[-1] > prev + 80 else ""
        prev = v[-1]
        print(f"  #{i:>2} @0x{o:05x} n={len(v):>2}  {v[0]:>4}..{v[-1]:>4} mV{mark}")
    return curves


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin", default=os.path.join(RES, "images", "mcu_0007.bin"))
    ap.add_argument("--min-len", type=int, default=6)
    ap.add_argument("--no-curves", action="store_true",
                    help="do not print voltage curve block analysis")
    a = ap.parse_args()

    d = open(a.bin, "rb").read()
    print(f"=== {os.path.basename(a.bin)}: {len(d)} B, monotonic series >= {a.min_len} ===\n")

    seen = set()
    total = 0
    for signed in (False, True):
        for off, vals in find_runs(d, a.min_len, signed):
            # do not print same region twice (unsigned/signed)
            key = (off // 2, len(vals))
            if key in seen:
                continue
            seen.add(key)
            # filter noise: series within code are often nearly random - require
            # either uniform step or long series
            diffs = [b - a2 for a2, b in zip(vals, vals[1:])]
            if len(set(diffs)) > 1 and len(vals) < a.min_len + 3:
                continue
            total += 1
            kind = "i16" if signed else "u16"
            print(f"@0x{off:05x} [{kind}] {len(vals)} values: {vals[:14]}"
                  f"{' …' if len(vals) > 14 else ''}")
            print(f"           {classify(vals)}")
    print(f"\ntotal series: {total}")
    if not a.no_curves:
        dump_battery_curves(d)


if __name__ == "__main__":
    raise SystemExit(main())
