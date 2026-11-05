#!/usr/bin/env python3
"""MCU (ARM Cortex-M) reversing: vector table, flash/RAM base, peripherals, IRQ."""
import os, sys, struct
IMG = os.path.join(os.path.dirname(__file__), "..", "..", "images", "mcu_0007.bin")
d = open(sys.argv[1] if len(sys.argv) > 1 else IMG, "rb").read()
N = len(d)
u32 = lambda o: struct.unpack_from("<I", d, o)[0]

# --- vector table search: word0=SP (RAM), word1..=reset+handlers (odd, flash) ---
def looks_sp(v):   # SRAM Cortex-M: 0x20000000.. (or 0x10000000 CCM)
    return 0x20000000 <= v <= 0x20040000 or 0x10000000 <= v <= 0x10010000
def looks_code(v): # Thumb address in flash: odd, high byte 0x08(STM/GD)/0x00/0x01
    return (v & 1) and ((v & 0xFF000000) in (0x08000000, 0x00000000, 0x01000000, 0x02000000))

print("=== vector table search ===")
cands = []
for off in range(0, min(N, 0x2000), 4):
    sp = u32(off)
    if not looks_sp(sp): continue
    # check next 8 words as handlers
    ok = 0
    for k in range(1, 12):
        if off + 4*k + 4 > N: break
        v = u32(off + 4*k)
        if looks_code(v): ok += 1
    if ok >= 8:
        cands.append((off, sp, ok))
for off, sp, ok in cands[:6]:
    print(f"  @0x{off:04x}: SP=0x{sp:08x}, {ok}/11 valid handlers")

if not cands:
    print("  vector table not found by heuristic - trying raw reset search")
    sys.exit(0)

VT, SP, _ = cands[0]
reset = u32(VT+4)
# flash base: reset vector points to code start; determine from high byte
FLASH_BASE = reset & 0xFF000000
# file offset corresponding to FLASH_BASE = VT (table at start of flashed region)
FILE_OF_FLASHBASE = VT
def to_off(vaddr):
    o = vaddr - FLASH_BASE + FILE_OF_FLASHBASE
    return o if 0 <= o < N else None
print(f"\n[i] VT@0x{VT:x}  SP=0x{SP:08x}  reset=0x{reset:08x}  FLASH_BASE=0x{FLASH_BASE:08x}")
print(f"[i] RAM top (SP) ~ 0x{SP:08x}  ->  SRAM estimate = {(SP-0x20000000)//1024}K" if SP>=0x20000000 else "")

# --- vector list (first 32) ---
print("\n=== vector table (first 24) ===")
EXC = ["SP","Reset","NMI","HardFault","MemManage","BusFault","UsageFault","-","-","-","-",
       "SVCall","DebugMon","-","PendSV","SysTick"]
for k in range(24):
    if VT+4*k+4 > N: break
    v = u32(VT+4*k)
    name = EXC[k] if k < len(EXC) else f"IRQ{k-16}"
    fo = to_off(v) if (v&1) else None
    extra = f" -> file 0x{fo:x}" if fo else ""
    print(f"  [{k:2}] {name:10} 0x{v:08x}{extra}")

# count IRQs (how many external interrupts used)
irqs = [k-16 for k in range(16, 200) if VT+4*k+4<=N and looks_code(u32(VT+4*k))]
print(f"\n[i] active external IRQ vectors: ~{len(irqs)}")

# --- peripherals: literal-pools pointing to 0x40000000..0x5fffffff ---
print("\n=== peripheral accesses (0x4xxxxxxx addresses in literal pools) ===")
from collections import Counter
peri = Counter()
for off in range(0, N-4, 4):
    v = u32(off)
    if 0x40000000 <= v < 0x60000000:
        peri[v & 0xFFFFFF00] += 1     # group by peripheral block
top = peri.most_common(40)
for addr, c in top:
    print(f"  0x{addr:08x}  x{c}")
