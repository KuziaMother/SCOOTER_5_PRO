# -*- coding: utf-8 -*-
import sys, io, struct
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import capstone
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN

print('capstone version:', capstone.__version__)
cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
cs.detail = False

# Известные эталонные кодирования (из реальной дизассембляции / ARM ARM):
tests = [
    (0x4600, 'movs r0, r1'),      # самое известное Thumb-инстр.
    (0x4601, 'movs r1, r0'),
    (0x7001, 'adds r0, r0, #1'),
    (0x4770, 'bx lr'),
    (0xBF00, 'nop'),
    (0xF000, 'b (self+4)'),       # b #0x... imm=0
    (0xB510, 'push {r4, lr}'),
    (0xBC0E, 'pop {r3, pc}'),
    (0x4800, 'ldr r0, [pc]'),     # ldr lit T1 imm=0
    (0x2300, 'movs r3, #0'),      # mov imm T2?
    (0x003B, '??? (md говорит movs r3, r7)'),
    (0x43B3, '??? (md говорит bics r3, r6)'),
]
for hw, expect in tests:
    b = struct.pack('<H', hw)
    out = []
    for ins in cs.disasm(b, 0x100):
        out.append('%s %s' % (ins.mnemonic, ins.op_str))
    got = ' | '.join(out) if out else '<data>'
    print('  %04x  capstone: %-28s expect: %s' % (hw, got, expect))

# 32-bit: BL к +0x1006 от PC
w = struct.pack('<HH', 0xF007, 0x0000)
for ins in cs.disasm(w, 0x100):
    print('  T32 %s' % (ins.mnemonic + ' ' + ins.op_str))
