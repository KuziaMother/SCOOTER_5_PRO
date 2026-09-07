#!/usr/bin/env python3
"""A2 (USART TX): эмпирика — прогоняем сборщик 0x211f8 (без аргументов, читает
фикс. RAM-поля) с seeded-RAM и ищем собранные кадры 61..9E в usart_out / TX-кольце."""
import sys, os, struct
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "emulator"))
from mcu_emu import McuEmu, RAM, FLASH0, FLASH1, STACK_TOP
from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR

def find_frames(data):
    """61 [sub] [len] data[len] chk 9E; chk=SUM&0xFF."""
    frames = []
    i, n = 0, len(data)
    while i < n:
        if data[i] != 0x61:
            i += 1; continue
        if n - i < 3: break
        ln = data[i + 2]
        e = i + ln + 5
        if ln > 200 or e > n: 
            i += 1; continue
        if data[e-1] != 0x9E or (sum(data[i:e-2]) & 0xFF) != data[e-2]:
            i += 1; continue
        frames.append(bytes(data[i:e])); i = e
    return frames

def run_and_scan(seed):
    emu = McuEmu(max_insn=400_000)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))     # чистая RAM
    for off, val in seed.items():
        sz = (val.bit_length() + 7) // 8 or 1
        uc.mem_write(RAM + off, struct.pack('<%dI' % (sz//4 or 1), *([val] + [0]*(sz//4-1)))[:sz])
    emu.hook_periph_ready()
    def _st(uc_, addr, size, u):
        aa = addr & ~1
        if not (FLASH0 <= aa < FLASH0 + 0x23680 or FLASH1 <= aa < FLASH1 + 0x23680):
            uc_.emu_stop()
    from unicorn import UC_HOOK_CODE
    sh = uc.hook_add(UC_HOOK_CODE, _st)
    try:
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        emu.insn = 0
        try: uc.emu_start(0x211F8 | 1, 0, count=300_000)
        except Exception as ex: print("   stop:", emu.stopped or ex)
    finally:
        uc.hook_del(sh)
    print(f"   usart_out ({len(emu.usart_out)} Б): {bytes(emu.usart_out).hex(' ')[:120]}")
    uf = find_frames(bytes(emu.usart_out))
    print(f"   кадров в usart_out: {len(uf)}")
    # TX-кольцо @0x10b5 + окрестности
    ring = bytes(uc.mem_read(RAM + 0x1080, 0x120))
    rf = find_frames(ring)
    print(f"   кадров в районе кольца @0x1080..+0x120: {len(rf)}")
    for f in (uf or rf)[:6]:
        print(f"     {f.hex(' ')}  sub=0x{f[1]:02x} len={f[2]}")
    return uf, rf

if __name__ == "__main__":
    print("=== seed: батарея 89% (@0x306), mode @0x229=2, u16@0x236=50 ===")
    run_and_scan({0x306: 89, 0x229: 2, 0x236: 50})
