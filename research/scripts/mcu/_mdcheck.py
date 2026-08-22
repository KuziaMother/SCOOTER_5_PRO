# -*- coding: utf-8 -*-
"""Проверка: дизассембляция в md func_0x1e9e0 против СВЕЖЕГО декода тех же байтов.
Находит первую точку дессинхронизации последовательного декода."""
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN

IMG = os.path.join(os.path.dirname(__file__), '..', '..', 'images', 'mcu_0007.bin')
d = open(IMG, 'rb').read()
cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
cs.detail = False

t = open(os.path.join(os.path.dirname(__file__), '..', '..', 'functions_mcu', 'func_0x1e9e0.md'), encoding='utf-8').read()
lines = t.splitlines()
# показать fence-строки и строку 1ea0e
for i, l in enumerate(lines):
    if l.strip().startswith('```'):
        print('fence line %d: %r' % (i, l))
    if l.strip().startswith('1ea0e') or l.strip().startswith('1ea10'):
        print('sample: %r' % l)

claims = {}
in_asm = False
for l in lines:
    s = l.strip()
    if s.startswith('```asm'):
        in_asm = True
        continue
    if in_asm and s.startswith('```'):
        break
    if not in_asm:
        continue
    m = re.match(r'([0-9a-f]{5}): (.+)', s)
    if m:
        claims[int(m.group(1), 16)] = m.group(2).strip()

print('md asm lines parsed:', len(claims))
mism, skipped = [], 0
for off in sorted(claims):
    c = claims[off]
    if c.startswith('.word') or c.startswith(';'):
        skipped += 1
        continue
    claimed = c.split(' -> ')[0].strip()
    insns = list(cs.disasm(d[off:off + 4], off))
    if not insns:
        mism.append((off, claimed, '<invalid/data>'))
        continue
    fresh = (insns[0].mnemonic + ' ' + insns[0].op_str).strip()
    if claimed != fresh and not claimed.startswith(fresh):
        mism.append((off, claimed, fresh))

print('pool/comment skipped:', skipped)
print('FIRST MISMATCHES (md claim  vs  fresh decode of raw bytes @ same offset):')
for off, c, f in mism[:15]:
    print('  %05x  md: %-32s | fresh: %s' % (off, c[:32], f))
print('total mismatches:', len(mism))
