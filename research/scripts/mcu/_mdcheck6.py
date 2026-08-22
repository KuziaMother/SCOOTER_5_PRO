# -*- coding: utf-8 -*-
"""Прицельная проверка инструкции в 0x1ea18 (байты 4C 41):
1) capstone detail — что именно он утверждает;
2) Unicorn + MEM_READ хук — какой адрес реально читает инструкция;
3) Keystone — какие байты он бы сгенерировал для той же инструкции.
Файловые байты исполняются по ИХ СОБСТВЕННЫМ адресам (BASE=0), чтобы
всё совпадало с адресами из md."""
import os, struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE, UC_HOOK_MEM_READ
from unicorn.arm_const import (UC_ARM_REG_PC, UC_ARM_REG_R4)

IMG = os.path.join(os.path.dirname(__file__), '..', '..', 'images', 'mcu_0007.bin')
d = open(IMG, 'rb').read()
ADDR = 0x1EA18

print('=== 1) capstone detail на 0x1ea18..0x1ea24 ===')
cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN); cs.detail = True
for ins in list(cs.disasm(d[ADDR:ADDR+12], ADDR))[:3]:
    print('  %05x size=%d  %-28s %s' % (ins.address, ins.size, ins.mnemonic, ins.op_str))

print()
print('=== 2) Unicorn: изолированное исполнение 4C 41 по адресу 0x1EA18 ===')
# Кандидатные адреса-мишени для ldr-lit:
cands = {
    'A+4 +0x104 (F1, как в md)   ': ((ADDR + 4) & ~3) + 0x104,
    'A+8 +0x104 (если T32-правило)': ((ADDR + 8) & ~3) + 0x104,
    'A+4 +0x8   (если imm4=2)    ': ((ADDR + 4) & ~3) + 8,
}
SENT = {v: i for i, v in enumerate(cands.values())}

uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
# код по собственным адресам: страница 0x1EA00
lo = (ADDR & ~0xFFF)
uc.mem_map(lo, 0x2000)                       # 0x1EA00..0x20A00
uc.mem_map(0x20000000, 0x20000)              # RAM (на всякий случай)
blob = d[ADDR:ADDR+4]                        # оба halfword'а: и Т16 и Т32 совпадут с файлом
uc.mem_write(ADDR, blob)
for a in cands.values():
    uc.mem_write(a, struct.pack('<I', 0xC0DE0000 | SENT[a]))

reads = []
def on_read(u, kind, addr, size, val, ud):
    reads.append((addr, size))
n_code = {'n': 0}
last = {}
def on_code(u, kind, addr, ud):
    n_code['n'] += 1
    last['pc'] = addr
    if n_code['n'] >= 2:                     # первая инст. уже отработала — стоп
        u.emu_stop()

uc.hook_add(UC_HOOK_MEM_READ, on_read)
uc.hook_add(UC_HOOK_CODE, on_code)
try:
    uc.emu_start(ADDR | 1, ADDR + 0x100 | 1)
except Exception as e:
    print('  emu exception: %s' % e)

print('  PC после: 0x%x (code events: %d)' % (last.get('pc', 0), n_code['n']))
if reads:
    a, s = reads[0]
    hit = [k for k, v in cands.items() if v == a]
    print('  ЧИТЕНИЕ с адреса 0x%x (%d байт) -> %s' % (a, s, hit if hit else 'НЕ совпало ни с одним кандидатом!'))
else:
    print('  чтений памяти НЕ БЫЛО (инструкция не ldr-lit? или trap)')
r4 = uc.reg_read(UC_ARM_REG_R4)
print('  r4 после = 0x%x' % r4)
for k, v in cands.items():
    try:
        w = struct.unpack('<I', uc.mem_read(v, 4))[0]
        mark = ' <== r4' if w == r4 else ''
        print('   sentinel@0x%x = 0x%x%s' % (v, w, mark))
    except Exception:
        pass

print()
print('=== 3) Keystone round-trip ===')
try:
    from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB
    ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    for code in ['ldr r4, [pc, #0x104]', 'ldr r4, [pc, #8]', 'ldr r4, [pc]']:
        try:
            enc, n = ks.asm(code)
            print('  %-24s -> %s (%d байт)%s' % (code, ''.join('%02x' % b for b in enc), len(enc),
                  '   == файлу!' if list(enc) == [0x4C, 0x41] else ''))
        except Exception as e:
            print('  %-24s -> ОШИБКА: %s' % (code, str(e)[:80]))
except ImportError as e:
    print('  keystone недоступен:', e)
