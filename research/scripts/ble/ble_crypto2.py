#!/usr/bin/env python3
"""BLE: relation between cipher blocks, block structure, header as candidate IV/key."""
import os, struct, math, collections
d=open(os.path.join(os.path.dirname(__file__),"..","..","images","ble_2.7.0_0015.bin"),"rb").read(); N=len(d)
def ent(b):
    if not b: return 0
    c=collections.Counter(b); n=len(b)
    return -sum((x/n)*math.log2(x/n) for x in c.values())

ENC1=(0x3000,0x5e00); ENC2=(0xa200,0x25400)
e1=d[ENC1[0]:ENC1[1]]; e2=d[ENC2[0]:ENC2[1]]
print(f"ENC1 0x{ENC1[0]:x}-0x{ENC1[1]:x} ({len(e1)}B) E={ent(e1):.3f}")
print(f"ENC2 0x{ENC2[0]:x}-0x{ENC2[1]:x} ({len(e2)}B) E={ent(e2):.3f}")
print(f"len%16: ENC1={len(e1)%16}, ENC2={len(e2)%16}  (0 => 16B block cipher)")

# first/last 32 bytes - do prefixes match (same IV/key => identical prefix unlikely, but useful)
print(f"\nENC1[:32] {e1[:32].hex()}")
print(f"ENC2[:32] {e2[:32].hex()}")
print(f"ENC1[-16:] {e1[-16:].hex()}")
print(f"ENC2[-16:] {e2[-16:].hex()}")

# repeating 16-B blocks within and BETWEEN regions (ECB / shared keystream)
b1=[e1[i:i+16] for i in range(0,len(e1)-15,16)]
b2=[e2[i:i+16] for i in range(0,len(e2)-15,16)]
c1=collections.Counter(b1); c2=collections.Counter(b2)
inter=set(c1)&set(c2)
print(f"\n16B duplicates within ENC1: {sum(v-1 for v in c1.values() if v>1)}")
print(f"16B duplicates within ENC2: {sum(v-1 for v in c2.values() if v>1)}")
print(f"shared 16B blocks between ENC1/ENC2: {len(inter)}")

# header: 16-byte GUID @0xc - IV/key candidate
hdr16=d[0x0c:0x1c]
print(f"\nheader[0x0c:0x1c] (16B, IV/key candidate): {hdr16.hex()}")
print(f"header[0x00:0x0c]: {d[0:0x0c].hex()}")
# window entropy across entire file with 256 step - exact encryption boundaries
print("\n=== exact boundaries (256B step, E) ===")
prev=None
for i in range(0,N,256):
    e=ent(d[i:i+256]); k='ENC' if e>7.4 else ('code' if e>5.0 else 'data')
    if k!=prev: print(f"  0x{i:05x}: E={e:.2f} {k}"); prev=k

# XOR of adjacent 16-B blocks of ENC2: if CBC, differences are random; searching for structural zeros
z=sum(1 for i in range(0,len(e2)-16,16) if e2[i:i+16]==e2[i+16:i+32])
print(f"\nadjacent identical 16B blocks in ENC2: {z} (>0 => regions of constants/padding under ECB)")
