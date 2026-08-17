#!/usr/bin/env python3
"""Разбор btsnoop: ATT write/notify по хендлам (какие каналы реально использует Mi Home)."""
import struct
import sys
from collections import Counter, defaultdict

path = sys.argv[1] if len(sys.argv) > 1 else "logs/btsnooz_hci.log"
data = open(path, "rb").read()
assert data[:8] == b"btsnoop\x00"
off = 16

ATT_OPS = {0x12: "WRITE_REQ", 0x52: "WRITE_CMD", 0x1b: "NOTIFY", 0x1d: "INDICATE",
           0x0a: "READ_REQ", 0x0b: "READ_RSP", 0x13: "WRITE_RSP", 0x09: "READ_BY_TYPE_RSP",
           0x08: "READ_BY_TYPE_REQ", 0x10: "READ_BY_GRP_REQ", 0x11: "READ_BY_GRP_RSP"}

per_handle = defaultdict(list)
opcount = Counter()
frames = 0

while off + 24 <= len(data):
    olen, ilen, flags, drops, ts = struct.unpack(">IIIIq", data[off:off + 24])
    off += 24
    pkt = data[off:off + ilen]
    off += ilen
    if len(pkt) < 1:
        continue
    frames += 1
    if pkt[0] != 0x02:              # только ACL
        continue
    # ACL: [02][handle+flags u16][acl_len u16][l2cap_len u16][cid u16][att...]
    if len(pkt) < 9:
        continue
    cid = struct.unpack("<H", pkt[7:9])[0]
    if cid != 4:                    # ATT
        continue
    att = pkt[9:]
    if not att:
        continue
    op = att[0]
    opcount[ATT_OPS.get(op, hex(op))] += 1
    if op in (0x12, 0x52, 0x1b, 0x1d, 0x0b) and len(att) >= 3:
        if op == 0x0b:
            continue
        h = struct.unpack("<H", att[1:3])[0]
        per_handle[h].append((ATT_OPS.get(op, hex(op)), att[3:], ts))

print(f"фреймов: {frames}")
print("ATT-опкоды:", dict(opcount))
print("\n=== трафик по хендлам ===")
for h, items in sorted(per_handle.items()):
    kinds = Counter(k for k, _, _ in items)
    print(f"\nhandle 0x{h:04x}: {len(items)} шт  {dict(kinds)}")
    for kind, payload, ts in items[:14]:
        print(f"   {kind:<10} {payload.hex()}")
