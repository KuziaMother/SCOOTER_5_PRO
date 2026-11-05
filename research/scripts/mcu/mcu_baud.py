# -*- coding: utf-8 -*-
"""""Search for MCU<->BLE UART baud rate by execution (not static analysis).

Run each function of mcu_0007.bin under Unicorn and catch writes to:
  - USART3 (0x40004800..+0x40) and UART4 (0x40004C00..+0x40): BRR=+0x0C, CR1/2/3;
  - RCC (0x40021000..+0x40): CR/CFGR - to recover PCLK.
BRR (F1) = mantissa<<4 | fraction, baud = PCLK / (mantissa + fraction/16).
From recovered BRR values, brute-force (PCLK, baud) to recover both.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "emulator"))
from mcu_emu import (McuEmu, find_func_starts, PERIPH, PERIPH_SIZE,  # noqa: E402
                    SYS, SYS_SIZE, STACK_TOP)
from unicorn import UC_HOOK_MEM_WRITE, UcError  # noqa: E402
from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR  # noqa: E402

USART3 = (0x40004800, 0x40004840)
UART4 = (0x40004C00, 0x40004C40)
RCC = (0x40021000, 0x40021040)

REG_NAMES = {
    0x00: "SR", 0x04: "DR", 0x08: "BRR", 0x0C: "CR1", 0x10: "CR2", 0x14: "CR3",
}


def sweep():
    starts = find_func_starts()
    print(f"[baud] functions: {len(starts)}")
    hits = {}   # func -> [(region, addr, size, value)]
    for idx, addr in enumerate(starts):
        emu = McuEmu(trace=False, max_insn=20000)
        emu.uc.mem_write(PERIPH, bytes(PERIPH_SIZE))
        emu.uc.mem_write(SYS, bytes(SYS_SIZE))
        rec = []

        def on_w(uc, access, address, size, value, user):
            for (lo, hi) in (USART3, UART4, RCC):
                if lo <= address < hi:
                    rec.append((lo, address - lo, size, value & 0xFFFFFFFF))
                    break

        emu.uc.hook_add(UC_HOOK_MEM_WRITE, on_w)
        emu.uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
        emu.uc.reg_write(UC_ARM_REG_LR, 1)
        try:
            emu.uc.emu_start(addr | 1, 0, count=20005)
        except UcError:
            pass
        if rec:
            hits[addr] = rec
        del emu
        if (idx + 1) % 200 == 0:
            print(f"[baud] {idx+1}/{len(starts)} functions, hits: {len(hits)}")
    return hits


def decode_brr(brr):
    """Possible (PCLK, baud) for discovered BRR."""
    m = brr >> 4
    f = brr & 0xF
    if m == 0:
        return []
    out = []
    for pclk in (36_000_000, 72_000_000, 18_000_000, 36_000_000 // 2):
        if f == 0:
            baud = pclk / m
        else:
            baud = pclk / (m + f / 16.0)
        for std in (9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600):
            if abs(baud - std) / std < 0.005:   # tolerance <0.5% (real UARTs do this)
                out.append((pclk, std))
    return out


def main():
    hits = sweep()
    print(f"\n[baud] functions writing to USART3/UART4/RCC: {len(hits)}")
    for addr, recs in sorted(hits.items(), key=lambda kv: -len(kv[1]))[:30]:
        regs = sorted(set(r[1] for r in recs))
        names = [REG_NAMES.get(r, f"+0x{r:x}") for r in regs]
        print(f"  func 0x{addr:05x}: {len(recs)} writes: {names[:10]}")
        # BRR writes - most valuable
        for lo, off, size, val in recs:
            if off == 0x08 and size == 4:
                reg = "USART3" if lo == USART3[0] else ("UART4" if lo == UART4[0] else "?")
                cands = decode_brr(val)
                print(f"    >>> {reg}_BRR <- 0x{val:08x}  candidates: {cands or 'no exact matches - inspect manually'}")
        # RCC - for PCLK
        for lo, off, size, val in recs:
            if lo == RCC[0] and off in (0x00, 0x08):
                nm = "RCC_CR" if off == 0 else "RCC_CFGR"
                print(f"    >>> {nm} <- 0x{val:08x}")


if __name__ == "__main__":
    main()
