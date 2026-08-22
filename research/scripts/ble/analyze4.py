#!/usr/bin/env python3
"""RTL8762C fw ч.4: PIC-разрешение ссылок на строки (ldr pc + add pc) -> имена функций."""
import os, sys, re, struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN

IMG = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ble_2.7.0_0015.bin")
FW = sys.argv[1] if len(sys.argv) > 1 else IMG
d = open(FW, "rb").read(); N = len(d)
strings = {m.start(): m.group().decode('ascii','ignore')
           for m in re.finditer(rb'[ -~]{4,}', d)}

md = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)

def nearest_string(off):
    # строка, начинающаяся в [off-3 .. off]
    for o in (off, off-1, off-2, off-3):
        if o in strings: return strings[o]
    return None

def analyze_region(a, b, out):
    # границы функций по push {..,lr}
    starts = [o for o in range(a, b, 2)
              if (struct.unpack_from("<H", d, o)[0] & 0xFF00) == 0xB500]
    starts.append(b)
    funcs = []
    for i in range(len(starts)-1):
        fa, fb = starts[i], starts[i+1]
        if fb-fa < 4: continue
        reg = {}          # регистр -> загруженный литерал (file-offset PIC-смещение)
        refs = []
        for ins in md.disasm(d[fa:fb], fa):   # address == file offset (BASE=0)
            mn, ops = ins.mnemonic, ins.op_str
            if mn == "ldr" and "[pc" in ops:
                mm = re.search(r"(r\d+|ip|lr).*#(0x[0-9a-f]+|\d+)", ops)
                if mm:
                    imm = int(mm.group(2), 16) if mm.group(2).startswith("0x") else int(mm.group(2))
                    pool = ((ins.address + 4) & ~3) + imm
                    if pool+4 <= N:
                        reg[mm.group(1)] = struct.unpack_from("<I", d, pool)[0]
            elif mn == "add" and ops.endswith(", pc"):
                rn = ops.split(",")[0].strip()
                if rn in reg:
                    target = (ins.address + 4 + reg[rn]) & 0xFFFFFFFF
                    s = nearest_string(target)
                    if s: refs.append(s)
            elif mn in ("adr",):
                mm = re.search(r"(r\d+).*#(0x[0-9a-f]+)", ops)
        funcs.append((fa, fb-fa, list(dict.fromkeys(refs))))
    for fa, sz, refs in funcs:
        line = f"func_0x{fa:05x} ({sz}B)"
        if refs: line += "  ::  " + " | ".join(r[:50] for r in refs[:5])
        out.write(line + "\n")
    return funcs

regions = [(0x00400, 0x02a00), (0x06000, 0x0a200), (0x02e00, 0x03000), (0x25400, 0x25922)]
allf = []
with open("functions.txt", "w", encoding="utf-8") as out:
    for a, b in regions:
        out.write(f"\n===== 0x{a:05x}-0x{b:05x} =====\n")
        allf += analyze_region(a, b, out)

named = [(fa, sz, refs) for fa, sz, refs in allf if refs]
print(f"[i] функций всего: {len(allf)}, с распознанными строками: {len(named)} -> functions.txt\n")
print("=== функции bootloader/DFU/flash по строкам ===")
for fa, sz, refs in named:
    print(f"  0x{fa:05x} ({sz:4}B): " + " | ".join(r[:46] for r in refs[:4]))
