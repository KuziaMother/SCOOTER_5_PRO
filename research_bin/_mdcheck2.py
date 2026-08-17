# -*- coding: utf-8 -*-
import sys, io, struct
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN

d = open('mcu_0007.bin', 'rb').read()
cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
cs.detail = False

print('bytes @1ea0e..1ea14:', d[0x1ea0e:0x1ea14].hex(' '))
print('halfwords:', struct.unpack_from('<5H', d, 0x1ea0e))

# 1) isolated decode of the exact 2 bytes
for ins in cs.disasm(d[0x1ea0e:0x1ea10], 0x1ea0e):
    print('isolated 2B @1ea0e: %s %s' % (ins.mnemonic, ins.op_str))

# 2) isolated decode of 4 bytes
for ins in cs.disasm(d[0x1ea0e:0x1ea12], 0x1ea0e):
    print('isolated 4B @1ea0e: %s %s' % (ins.mnemonic, ins.op_str))

# 3) what does capstone say for raw 0x003b and 0x43b3?
for hw in (0x003b, 0x43b3):
    b = struct.pack('<H', hw)
    for ins in cs.disasm(b, 0x1ea0e):
        print('synthetic %04x -> %s %s' % (hw, ins.mnemonic, ins.op_str))

# 4) sequential from function start, show what lands on 1ea0e/1ea10
insns = list(cs.disasm(d[0x1e9e0:0x1f15a], 0x1e9e0))
for ins in insns:
    if 0x1ea08 <= ins.address <= 0x1ea14:
        print('sequential @%05x: %s %s (size %d)' % (ins.address, ins.mnemonic, ins.op_str, ins.size))
