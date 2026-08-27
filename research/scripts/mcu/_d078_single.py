#!/usr/bin/env python3
"""Single-case trace Phase B 0x1d078: чистые входы, write-trace structB-полей."""
import struct
import sys

sys.path.insert(0, 'research/scripts/mcu')
from func_verify import Run, RAM


def main():
    run = Run(max_insn=500000)
    # Чистые входы: F=0 (val=0), out1_new=out2_new=0, target=150, old_int=8000
    V, F = 60000, 0
    mode, f339, c326, m2t = 2, 0, 200, 150
    acc1 = out1 = acc2 = out2 = 0
    old_int = 8000
    s2e_old = 0
    u1760, u1764, u388, u224 = 0, 0, 0, 0

    run.ram_write(0x158, struct.pack('<I', V))
    run.ram_write(0x100, bytes([F]))
    run.ram_write(0x229, bytes([mode]))
    run.ram_write(0x339, struct.pack('<H', f339))
    run.ram_write(0x333, b'\x00')
    run.ram_write(0x263, b'\x00')
    run.ram_write(0x324, struct.pack('<H', m2t))
    run.ram_write(0x326, struct.pack('<H', c326))
    run.ram_write(0x1768, struct.pack('<H', 0))
    run.ram_write(0x176C, struct.pack('<I', acc2))
    run.ram_write(0x1770, struct.pack('<H', out2 & 0xFFFF))
    run.ram_write(0x1774, struct.pack('<I', acc1))
    run.ram_write(0x1778, struct.pack('<H', out1 & 0xFFFF))
    run.ram_write(0x1760, struct.pack('<I', u1760))
    run.ram_write(0x1764, struct.pack('<I', u1764))
    run.ram_write(0x388, struct.pack('<I', u388))
    run.ram_write(0x224, struct.pack('<I', u224))
    run.ram_write(0x3C8, b'\x00' * 0x70)
    run.ram_write(0x3C8 + 0x28, struct.pack('<H', 1))
    run.ram_write(0x3C8 + 0x58, struct.pack('<I', old_int))
    run.ram_write(0x3C8 + 0x2E, struct.pack('<H', s2e_old))

    def rd(off, n=4):
        return struct.unpack('<I', run.ram_read(0x3C8 + off, n))[0] if n == 4 \
            else struct.unpack('<H', run.ram_read(0x3C8 + off, 2))[0]

    before = {o: rd(o, 2 if o in (0x2E,) else 4) for o in (0x2c, 0x58, 0x5c, 0x60, 0x64)}
    run.call(0x1D078, (), max_insn=400000)
    after = {o: rd(o, 2 if o in (0x2E,) else 4) for o in (0x2c, 0x58, 0x5c, 0x60, 0x64)}

    print("входы: V=%d F=%d mode=%d c326=%d m2t=%d old_int=%d s2e=%d u1760=%d u224=%d"
          % (V, F, mode, c326, m2t, old_int, s2e_old, u1760, u224))
    print("ожидание модели: o1n=0,o2n=0,tgt=150 → INCREASE")
    print("  err=150, interim=5*150+8000=8750, adj=0, integral=8750")
    print("  clamp[8000,131040]: keep 8750 → S58=8750; S60=asr(8750,2)=2187")
    print("  output=P+S60=19200+2187=21387 → clamp→21387; tail(u1760=0): S58=0,S64=0,S2e=0")
    print("\nполе   before  after")
    for o in (0x2c, 0x58, 0x5c, 0x60, 0x64, 0x2e):
        b = rd(o, 2 if o in (0x2E, 0x2C) else 4)
        a = after.get(o, rd(o, 2 if o in (0x2E,) else 4))
        print(f"  +{o:02x}   {b:<8} {a}")


if __name__ == '__main__':
    main()
