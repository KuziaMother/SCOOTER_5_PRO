# -*- coding: utf-8 -*-
"""Поведенческая проверка спорных Thumb-кодировок через Unicorn (QEMU) + Keystone.
Не зависит от capstone и от моей памяти о таблицах ARM ARM."""
import struct
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_PC, UC_ARM_REG_LR, UC_ARM_REG_SP,
                               UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                               UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R6,
                               UC_ARM_REG_R7)
import keystone

BASE = 0x10000
STACK = 0x30000
NAMES = {UC_ARM_REG_R0: 'r0', UC_ARM_REG_R1: 'r1', UC_ARM_REG_R2: 'r2',
         UC_ARM_REG_R3: 'r3', UC_ARM_REG_R4: 'r4', UC_ARM_REG_R6: 'r6',
         UC_ARM_REG_R7: 'r7'}

def run(hws, regs_before, readback=None):
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x18000)                  # 0x10000..0x28000: куда ни прыгнем — видно PC
    uc.mem_map(STACK, 0x4000)                  # 0x30000..0x34000
    blob = b''.join(struct.pack('<H', h) for h in hws)
    uc.mem_write(BASE, blob)
    for r, v in regs_before.items():
        uc.reg_write(r, v)
    uc.reg_write(UC_ARM_REG_SP, STACK + 0x100)
    uc.reg_write(UC_ARM_REG_LR, 0xDEAD0001)     # sentinel: BL его перезапишет, B — нет
    stop = {'pc': None}
    def cb(u, kind, val, user):
        pc = u.reg_read(UC_ARM_REG_PC)
        if not (BASE <= pc < BASE + len(blob)):
            stop['pc'] = pc | 1
            u.emu_stop()
    uc.hook_add(UC_HOOK_CODE, cb)
    try:
        uc.emu_start(BASE | 1, BASE + len(blob) | 1)
    except Exception as e:
        pass
    out = {}
    for r in regs_before:
        out[NAMES[r]] = uc.reg_read(r)
    lr = uc.reg_read(UC_ARM_REG_LR)
    pc = stop['pc'] if stop['pc'] else (uc.reg_read(UC_ARM_REG_PC))
    mv = None
    if readback is not None:
        try:
            mv = uc.mem_read(readback, 1)[0]
        except Exception:
            pass
    return out, lr, pc, mv

print('=== Unicorn (QEMU) behavioral ===')
tests = [
    # (имя, halfwords, регистры до, readback-адрес)
    ('A: 03 F0 9F F8 (capstone: bl #0x21b52, size 4)', [0xF003, 0xF89F], {}, None),
    ('B: 3A 0E   (capstone: subs r2, #0xe)',          [0x3A0E], {UC_ARM_REG_R0: 0x111, UC_ARM_REG_R2: 0x222}, None),
    ('C: 46 00   (capstone: mov r0, r0)',             [0x4600], {UC_ARM_REG_R0: 0x11, UC_ARM_REG_R1: 0xDEAD}, None),
    ('D: 70 01   (capstone: strb r1, [r0])',          [0x7001], {UC_ARM_REG_R0: STACK + 0x50, UC_ARM_REG_R1: 0x99}, STACK + 0x50),
    ('E: 3B 00   (capstone: movs r3, r7)',            [0x003B], {UC_ARM_REG_R3: 0x12, UC_ARM_REG_R7: 0x77}, None),
    ('F: B3 43   (capstone: bics r3, r6)',            [0x43B3], {UC_ARM_REG_R3: 0xFF, UC_ARM_REG_R6: 0x66}, None),
]
for name, hws, regs, rb in tests:
    out, lr, pc, mv = run(hws, regs, rb)
    extra = '  mem[r0]=%02x' % mv if mv is not None else ''
    lrnote = 'LR=0x%08x (%s)' % (lr, 'перезаписан -> BL?' if lr != 0xDEAD0001 else 'нетронут -> не BL')
    print('%s\n   regs: %s  %s  PC->0x%x%s' % (name, out, lrnote, pc - BASE, extra))

print()
print('=== Keystone (независимый ассемблер) ===')
ks = keystone.Keystone(keystone.KS_ARCH_ARM, keystone.KS_MODE_THUMB)
asm_tests = [
    ('movs r0, r1',  'какой байт? (я думал 4608)'),
    ('movs r1, r0',  'какой байт? (я думал 4601)'),
    ('subs r2, #14', 'совпадает с 3A 0E?'),
    ('lsls r4, r1, #28', 'совпадает с 0C 07?'),
    ('strb r1, [r0]', 'совпадает с 70 01?'),
    ('adds r0, r0, #1', 'какой байт?'),
    ('movs r3, #0',  '2300 или 000F?'),
]
for code, note in asm_tests:
    try:
        enc, n = ks.asm(code)
        print('  %-22s -> %s   (%s)' % (code, ''.join('%02x' % b for b in enc), note))
    except Exception as e:
        print('  %-22s -> ОШИБКА: %s' % (code, e))

# B vs BL в точке 0x1ea10: ассемблируем оба варианта с тем же целевым смещением
print()
print('--- B/BL disambiguation (pc=BASE) ---')
for code in ['b .+6', 'bl .+6']:
    try:
        enc, n = ks.asm(code)
        print('  %-10s -> %s (%d байт)' % (code, ''.join('%02x' % b for b in enc), len(enc)))
    except Exception as e:
        print('  %-10s -> ОШИБКА: %s' % (code, e))
