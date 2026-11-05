#!/usr/bin/env python3
"""Crypto-analysis of encrypted BLE fw portion: AES vs compression, key/S-box search, mode."""
import os, sys, struct, collections, math

IMG = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ble_2.7.0_0015.bin")
FW = sys.argv[1] if len(sys.argv) > 1 else IMG
d = open(FW, "rb").read()
ENC = (0x0a200, 0x25400)     # main encrypted block
enc = d[ENC[0]:ENC[1]]
print(f"enc-block 0x{ENC[0]:x}-0x{ENC[1]:x}, {len(enc)} bytes")

# 1) AES-ECB? search for repeating 16-byte blocks
print("\n=== 1) 16-byte block repetitions (AES-ECB indicator) ===")
blocks = [enc[i:i+16] for i in range(0, len(enc)-15, 16)]
cnt = collections.Counter(blocks)
rep = [(b, c) for b, c in cnt.items() if c > 1]
print(f"  total blocks={len(blocks)}, unique={len(cnt)}, repeating={len(rep)}")
if rep:
    rep.sort(key=lambda x: -x[1])
    for b, c in rep[:3]:
        print(f"    x{c}: {b.hex()}")
print("  -> many repetitions = ECB; zero repetitions = CBC/CTR/stream/compression")

# 2) compression signatures at start of enc and across entire file
print("\n=== 2) compression signatures ===")
sigs = {b"\x1f\x8b": "gzip", b"\x5d\x00\x00": "lzma", b"\x04\x22\x4d\x18": "lz4",
        b"PK\x03\x04": "zip", b"\x28\xb5\x2f\xfd": "zstd", b"BZh": "bzip2",
        b"\x89LZO": "lzo"}
for sig, name in sigs.items():
    i = d.find(sig)
    print(f"  {name:6}: {'@0x%x'%i if i>=0 else 'none'}")

# 3) AES S-box / T-box in open portion (indicator of software AES + possible nearby key)
SBOX = bytes([0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76])
INV  = bytes([0x52,0x09,0x6a,0xd5,0x30,0x36,0xa5,0x38,0xbf,0x40,0xa3,0x9e,0x81,0xf3,0xd7,0xfb])
te0  = bytes.fromhex("c66363a5")  # start of AES T-table (common variant)
print("\n=== 3) AES tables in image ===")
for name, sig in [("S-box", SBOX), ("Inv-S-box", INV), ("Te0", te0)]:
    i = d.find(sig)
    print(f"  {name:10}: {'@0x%x'%i if i>=0 else 'none'}")

# 4) key candidates: 16/32-byte high-entropy constants in open sections
def ent(b):
    if not b: return 0
    c = collections.Counter(b); n=len(b)
    return -sum((x/n)*math.log2(x/n) for x in c.values())
plain = [(0x400,0x2a00),(0x6000,0xa200)]
print("\n=== 4) high-entropy 16/32-B constants in open code (key candidates) ===")
found=0
for a,b in plain:
    reg=d[a:b]
    for i in range(0,len(reg)-32,4):
        w=reg[i:i+32]
        if len(set(w))>=26 and ent(w)>4.3:   # nearly all bytes unique
            # exclude obvious strings
            if sum(32<=c<127 for c in w) < 20:
                print(f"  0x{a+i:05x}: {w.hex()}")
                found+=1
                if found>=8: break
    if found>=8: break
if not found: print("  (no obvious 16/32-B keys found in open code)")

# 5) distribution of first enc bytes (IV?)
print("\n=== 5) first 48 bytes of enc block ===")
print("  ", enc[:48].hex(' '))
print(f"  entropy of entire enc: {ent(enc):.3f}  (max=8.0)")
