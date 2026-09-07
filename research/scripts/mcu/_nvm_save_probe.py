#!/usr/bin/env python3
"""A3 (SPI-flash/NVM): эмпирика NVRAM-save 0x21a08. Ловим RAM-чтения (NVM-source
буфер) + SPI1 (0x40013000) записи, чтобы понять layout NVM и механику SPI."""
import sys, os, struct, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "emulator"))
from mcu_emu import McuEmu, RAM, FLASH0, FLASH1, STACK_TOP
from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE

SPI1 = 0x40013000

def run_save():
    emu = McuEmu(max_insn=200_000)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))
    # distinctive pattern в RAM, чтобы увидеть какой буфер уходит в NVM
    for off in range(0, 0x400, 1):
        pass
    # seed gate byte@0x170 = 1
    uc.mem_write(RAM + 0x170, bytes([1]))
    emu.hook_periph_ready()

    ram_reads = []
    def _rd(uc_, access, addr, size, value, user):
        if RAM <= addr < RAM + 0x20000:
            ram_reads.append((addr - RAM, size))
    rh = uc.hook_add(UC_HOOK_MEM_READ, _rd, None, RAM, RAM + 0x20000)

    def _st(uc_, addr, size, u):
        aa = addr & ~1
        if not (FLASH0 <= aa < FLASH0 + 0x23680 or FLASH1 <= aa < FLASH1 + 0x23680):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, _st)
    try:
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x40)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        emu.insn = 0
        try: uc.emu_start(0x21A08 | 1, 0, count=150_000)
        except Exception as e: print("   stop:", emu.stopped or e)
    finally:
        uc.hook_del(sh); uc.hook_del(rh)

    # SPI1-записи
    spi = [(a - SPI1, s, v) for pc, a, s, v in emu.periph_writes if SPI1 <= a < SPI1 + 0x40]
    print(f"   SPI1 (0x{SPI1:08x}) записей: {len(spi)}")
    by = collections.defaultdict(list)
    for off, s, v in spi:
        by[off].append(v)
    for off in sorted(by):
        vals = by[off]
        print(f"     +0x{off:02x}: W×{len(vals)} last={vals[-1]:#x} seq={vals[:8]}")
    # RAM-чтения (NVM-source буфер) — сгруппируем по близости
    addrs = sorted(set(a for a, s in ram_reads))
    print(f"   RAM-чтений: {len(ram_reads)}, уникальных адресов: {len(addrs)}")
    # покажем кластеры (последовательные адреса)
    if addrs:
        clusters = []
        cur = [addrs[0]]
        for a in addrs[1:]:
            if a - cur[-1] <= 4: cur.append(a)
            else: clusters.append(cur); cur = [a]
        clusters.append(cur)
        for c in clusters[:20]:
            print(f"     кластер 0x{c[0]:03x}..0x{c[-1]:03x} ({len(c)} адр)")

if __name__ == "__main__":
    run_save()
