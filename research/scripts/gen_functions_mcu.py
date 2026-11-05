#!/usr/bin/env python3
"""
Function reference for MCU image mcu_0007.bin (Dreame/Xiaomi Scooter 5 Pro,
motor controller on Cortex-M4F, GD32/STM32F1-class, HAL; UNENCRYPTED).

Generates research/functions_mcu/*.md — one file per CONFIRMED
function:
    - metadata (offset = vaddr at base 0x0; flash mirror 0x08000000,
      RAM 0x20000000, peripheral 0x40000000, SYS 0xE0000000);
    - strings referenced by the function (ldr [pc] / movw+movt) — almost
      none in this image (controller without debug logging);
    - all literals (peripherals, RAM, SYS, image addresses, mirror 0x08000000);
    - callees (bl/b) and callers (xrefs from all functions);
    - disassembly (capstone, Thumb) with line-by-line annotations;
      literal pools are rendered as word tables.

Base: file is loaded by the emulator at 0x00000000 (and mirror 0x08000000),
i.e., vaddr == file offset. No vector table is present in the OTA image
(REPORT.md §MCU): image is APP payload region only, code begins at 0x01200.

Detection (three start sources + epilogue confirmation):
  1. prologue `push {..,lr}` (B5xx, bit7 reglist = lr) — 503 items;
  2. prologue `push.w {..,lr}` (T4, first halfword 0xE92D; verified
     by capstone) — 93 items (functions missed by B5xx heuristic);
  3. `bl`/`blx` targets NOT inside confirmed functions from 1-2 —
     functions without push prologue (small leaves, ISRs): each confirmed
     by its own epilogue in the window up to the next confirmed function.
  Confirmation/boundaries — same as in gen_functions.py (BLE):
    - epilogue: pop{..,pc} | bx lr | "pop-lr"+b|bx rX | bx rX/ip/fp/sl |
      b/b.w to trampoline (hot target >=3 / block with epilogue / chains);
    - two window passes (baseline up to next candidate; expansion of
      unconfirmed — not past the next confirmed);
    - boundary fb = BFS maximum reachable from prologue in verified
      window (split-body/cold paths); literal pools not included in fb (printed
      as table by absolute offsets, may lie past subsequent functions);
    - overlaps resolved by incoming xrefs (callee remains).
  Global branch target collection uses BYTEWISE scan + capstone verification
  of each instruction in place (sequential region decoding in this image
  desynchronizes on data — sequential target collection is unreliable).

Literal pool formula: ((addr+4) & ~3) + imm — empirically verified: 97.8%
of resolved pool words fall into plausible classes (RAM/peri/sys/img),
whereas alternative (addr+4)+imm yields only 46%.

Usage:  $env:PYTHONIOENCODING="utf-8"; python research/scripts/gen_functions_mcu.py
"""
import glob
import os
import re
import struct
from collections import defaultdict
from collections import Counter

from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN

HERE = os.path.dirname(os.path.abspath(__file__))   # research/scripts/
RES = os.path.dirname(HERE)                          # research/
FW = os.path.join(RES, "images", "mcu_0007.bin")
OUT_DIR = os.path.join(RES, "functions_mcu")

BASE = 0x0                 # vaddr == offset (emulator: flash @0x0 and mirror @0x08000000)
MIRROR = 0x08000000        # flash mirror: some literals reference code/data through it
REGIONS = [
    (0x01200, 0x02400, "code A"),
    (0x02600, 0x10200, "code B (FLASH-OTA: 0x06230/0x06304)"),
    (0x10400, 0x10e00, "code C"),
    (0x11000, 0x12400, "code D (0x11894 tbb machine, 0x11cb4 OTA-init)"),
    (0x12800, 0x13e00, "code E (UART init/driver: 0x12d90/0x1302c)"),
    (0x14200, 0x14400, "code F"),
    (0x14600, 0x17a00, "code G"),
    (0x18e00, 0x19200, "code H"),
    (0x19a00, 0x24200, "code I (USART3 protocol 0x1e480/0x1e9e0/0x1f600/0x1f6b4, "
                       "HAL_UART_Transmit 0x23188, motor TIM1 0x22a48-0x22fac, "
                       "ADC 0x1a31c/0x1e298)"),
    (0x24400, 0x24600, "code J"),
]


def fname_of(off):
    return f"func_0x{off:05x}"


def in_code(off):
    return any(a <= off < b for a, b, _ in REGIONS)


def region_name(off):
    for a, b, n in REGIONS:
        if a <= off < b:
            return n
    return "?"


def load_strings(d):
    """offset -> text (ASCII strings >=4 chars)."""
    return {m.start(): m.group().decode("ascii", "ignore")
            for m in re.finditer(rb"[ -~]{4,}", d)}


# --------------------------------------------------------------------------
# Function entry points
# --------------------------------------------------------------------------

def find_prologues(d, md):
    """Returns (b5, t32): offsets of push {..,lr} and push.w {..,lr}."""
    b5, t32 = set(), set()
    for a, b, _ in REGIONS:
        i = a
        while i + 2 <= b:
            w = struct.unpack_from("<H", d, i)[0]
            if (w & 0xFF00) == 0xB500 and (w & 0x0100):       # push {..,lr}
                b5.add(i)
            elif (w & 0xFF80) == 0xE900 and i + 4 <= b:        # push.w?
                ins = next(md.disasm(d[i:i + 4], BASE + i), None)
                if ins is not None and ins.mnemonic == "push.w" \
                        and "lr" in ins.op_str:
                    t32.add(i)
            i += 2
    return b5, t32


def _parse_branch_target(op_str):
    """Parse Capstone's op_str for b/bl -> Thumb address (vaddr) or None.

    Capstone outputs '#0x...' and for negative displacements — sign-extended
    32-bit values (0xfffff8de); wrap within image range.
    """
    s = op_str.strip()
    if not s.startswith("#"):
        return None
    try:
        t = int(s[1:], 16)
    except ValueError:
        return None
    if t >= 0x80000000:
        t -= 0x10000000
    return t & ~1


def find_call_targets(d, md):
    """All bl/blx targets in code (bytewise scan + Capstone in place).

    Returns (targets_in_code, all_targets) — vaddrs.
    """
    targets = set()
    for a, b, _ in REGIONS:
        i = a
        while i + 4 <= b:
            w1 = struct.unpack_from("<H", d, i)[0]
            if (w1 & 0xF800) == 0xF000 and ((w1 >> 8) & 3) >= 2:   # bl/blx T4
                ins = next(md.disasm(d[i:i + 4], BASE + i), None)
                if ins is not None and ins.mnemonic in ("bl", "blx"):
                    t = _parse_branch_target(ins.op_str)
                    if t is not None:
                        targets.add(t)
                i += 4
            else:
                i += 2
    in_c = {t for t in targets if in_code(t)}
    return in_c, targets


def find_branch_targets(d, md):
    """All b/b.w (16- and 32-bit) targets in code — for trampoline detection."""
    cnt = Counter()
    for a, b, _ in REGIONS:
        i = a
        while i + 2 <= b:
            w = struct.unpack_from("<H", d, i)[0]
            is_b16 = (w & 0xF800) == 0xF000 and not (w & 0x400)     # b #imm8
            is_bw = i + 4 <= b and (w & 0xF800) == 0xE000           # b.w T3
            if is_b16 or is_bw:
                chunk = d[i:i + (4 if is_bw else 2)]
                ins = next(md.disasm(chunk, BASE + i), None)
                if ins is not None and ins.mnemonic in ("b", "b.w"):
                    t = _parse_branch_target(ins.op_str)
                    if t is not None:
                        cnt[t] += 1
            i += 2
    return cnt


# --------------------------------------------------------------------------
# Trampolines / epilogues / boundaries (same logic as gen_functions.py BLE)
# --------------------------------------------------------------------------

def _block_starts(d, md, t):
    """First instructions of block at vaddr t (or [] if outside file)."""
    off = t - BASE
    if not (0 <= off + 2 <= len(d)):
        return []
    return list(md.disasm(d[off:off + 16], BASE + off))


def _first_b_target(d, md, t):
    insns = _block_starts(d, md, t)
    if not insns or insns[0].mnemonic not in ("b", "b.w"):
        return None
    op = insns[0].op_str.strip()
    return int(op[1:], 16) & ~1 if op.startswith("#") else None


def _starts_with_epilogue(d, md, t):
    insns = _block_starts(d, md, t)
    if not insns:
        return False
    m0, op0 = insns[0].mnemonic, insns[0].op_str
    regs = [r.strip() for r in op0.strip("{}").split(",")] if "{" in op0 else []
    if m0 in ("pop", "pop.w") and "pc" in regs:
        return True
    if m0 in ("pop", "pop.w") and "lr" in regs:
        return any(j.mnemonic == "bx" and j.op_str.strip() != "lr"
                   for j in insns[1:5])
    return False


def find_thunks(d, md):
    """Trampoline addresses where b/b.w is a valid epilogue (hot targets
    >=3, block starting with epilogue, chains resolved via fixed-point)."""
    cnt = find_branch_targets(d, md)
    targets = set(cnt)
    thunks = {t for t, c in cnt.items() if c >= 3}
    for t in targets:
        if t not in thunks and _starts_with_epilogue(d, md, t):
            thunks.add(t)
    changed = True
    while changed:
        changed = False
        for t in targets:
            if t in thunks:
                continue
            u = _first_b_target(d, md, t)
            if u is not None and (u in thunks or _starts_with_epilogue(d, md, u)):
                thunks.add(t)
                changed = True
    return thunks


def find_epilogue(insns, thunks):
    """First valid epilogue: (i_start, j_end, kind) or None."""
    for i, ins in enumerate(insns):
        mn, op = ins.mnemonic, ins.op_str.strip()
        pop_lr = False
        if mn in ("pop", "pop.w"):
            regs = [r.strip() for r in op.strip("{}").split(",")]
            if "pc" in regs:
                return i, i, "pop{..,pc}"
            pop_lr = "lr" in regs
        elif mn in ("ldr", "ldr.w") and op.startswith("lr,") and "[sp]" in op:
            pop_lr = True                       # ldr lr,[sp],#4 == pop {lr}
        elif mn == "ldm" and "{" in op:         # ldmfd sp!, {..,lr}
            regs = [r.strip() for r in op.split("{", 1)[1].rstrip("}").split(",")]
            pop_lr = "lr" in regs
        if pop_lr:
            for j in range(i + 1, min(i + 5, len(insns))):
                mj = insns[j].mnemonic
                if mj in ("b", "b.w"):
                    return i, j, "pop{..,lr}+b"
                if mj == "bx" and insns[j].op_str.strip() != "lr":
                    return i, j, f"pop{{..,lr}}+bx {insns[j].op_str.strip()}"
            continue
        if mn == "bx":
            if op == "lr":
                return i, i, "bx lr"
            if re.fullmatch(r"(r\d+|ip|fp|sl)", op):
                return i, i, f"bx {op} (tail-call)"
        elif mn in ("b", "b.w") and op.startswith("#"):
            if int(op[1:], 16) & ~1 in thunks:
                return i, i, f"b thunk@{op[1:]}"
    return None


def reach_end(d, md, fa, win_end, thunks):
    """Maximum offset reachable from fa within [fa, win_end) (BFS)."""
    hi = min(win_end, len(d))
    insns = [i for i in md.disasm(d[fa:hi], BASE + fa)
             if fa <= i.address - BASE < hi]
    by_off = {i.address - BASE: i for i in insns}
    offs = sorted(by_off)
    next_map = dict(zip(offs, offs[1:]))
    max_addr = fa
    seen = set()
    stack = [fa]
    while stack:
        off = stack.pop()
        if off in seen or off not in by_off:
            continue
        seen.add(off)
        ins = by_off[off]
        max_addr = max(max_addr, min(off + ins.size, hi))
        mn, op = ins.mnemonic, ins.op_str.strip()
        # IMPORTANT: bx is NOT a control-flow branch (bx lr / bx rX is return/tail-call):
        # otherwise BFS leaks past epilogue into pools / next function.
        is_branch = (mn.startswith("b") and mn not in ("bl", "blx", "bx")) \
            or mn in ("cbz", "cbnz")
        if is_branch:
            if op.startswith("#"):
                t = int(op[1:], 16) & ~1
                if fa <= t < hi and t not in thunks:
                    stack.append(t)
            if mn not in ("b", "b.w"):
                nxt = next_map.get(off)
                if nxt is not None:
                    stack.append(nxt)
        elif mn == "bx":
            pass
        else:
            if not (mn in ("pop", "pop.w") and "pc" in op):
                nxt = next_map.get(off)
                if nxt is not None:
                    stack.append(nxt)
    return max_addr


def confirm_in_window(d, md_sd, fa, limit, stop, thunks):
    """Confirm candidate fa: baseline window [fa, limit), then expand
    up to min(stop, +0x400) — but NOT past next confirmed candidate (stop).
    Returns fb or None."""
    N = len(d)
    win_end = min(limit, stop, N)
    insns = list(md_sd.disasm(d[fa:win_end], BASE + fa))
    epi = find_epilogue(insns, thunks)
    ext = 0
    while (epi is None or epi[0] < 1) and win_end < min(stop, N) and ext < 0x400:
        ext += 0x100
        win_end = min(limit + ext, stop, N)
        insns = list(md_sd.disasm(d[fa:win_end], BASE + fa))
        epi = find_epilogue(insns, thunks)
    if epi is None or epi[0] < 1:
        return None
    return reach_end(d, md_sd, fa, win_end, thunks)


def detect_functions(d, md):
    """Returns (funcs, fakes, thunks): funcs=[(fa, fb, region)], fakes=[(fa, kind)].

    Tier 1: prologues (B5xx | push.w) — two window passes, as in BLE version.
    Tier 2: bl targets outside confirmed Tier 1 — confirmed by own epilogue
    in window up to next confirmed function."""
    md_sd = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
    md_sd.skipdata = True
    thunks = find_thunks(d, md)
    N = len(d)

    b5, t32 = find_prologues(d, md)
    bl_in, _ = find_call_targets(d, md)

    # --- Tier 1: prologues ---
    cands = sorted((b5 | t32))
    # grouping by regions (windows do not cross region boundaries)
    by_region = defaultdict(list)
    for fa in cands:
        if in_code(fa):
            by_region[region_name(fa)].append(fa)

    funcs, fakes = [], []
    confirmed_spans = []     # [(fa, fb)] — for Tier 2 and stop rules
    for _, _, name in REGIONS:
        rc = by_region.get(name, [])
        if not rc:
            continue
        a, b = next((x, y) for x, y, n in REGIONS if n == name)
        # pass 1: baseline window up to next candidate
        p1 = {}
        for i, fa in enumerate(rc):
            limit = rc[i + 1] if i + 1 < len(rc) else b
            fb = confirm_in_window(d, md_sd, fa, limit, b, thunks)
            p1[fa] = fb
        confirmed1 = {fa for fa, fb in p1.items() if fb is not None}
        # pass 2 (expansion) is inside confirm_in_window via stop:
        # for unconfirmed — stop = next confirmed candidate
        real = []
        for i, fa in enumerate(rc):
            if p1[fa] is not None:
                real.append((fa, p1[fa]))
                continue
            stop = b
            for fc in rc[i + 1:]:
                if fc in confirmed1:
                    stop = fc
                    break
            limit = rc[i + 1] if i + 1 < len(rc) else b
            fb = confirm_in_window(d, md_sd, fa, min(limit, stop), stop, thunks)
            if fb is None:
                fakes.append((fa, "prologue"))
            else:
                real.append((fa, fb))
        for fa, fb in real:
            funcs.append((fa, fb, name))
            confirmed_spans.append((fa, fb))

    # --- Tier 2: bl targets outside confirmed functions ---
    confirmed_spans.sort()
    def inside_confirmed(t):
        for fa, fb in confirmed_spans:
            if fa <= t < fb:
                return True
            if fa > t:
                break
        return False

    tier2 = sorted(t for t in bl_in if not inside_confirmed(t))
    for t in tier2:
        name = region_name(t)
        a, b = next((x, y) for x, y, n in REGIONS if n == name)
        # stop = next confirmed function after t (in same region)
        stop = b
        for fa, fb in confirmed_spans:
            if fa > t and a <= fa < b:
                stop = fa
                break
        limit = b  # tier 2: window up to region boundary (expansion limited by stop)
        fb = confirm_in_window(d, md_sd, t, limit, stop, thunks)
        if fb is None:
            fakes.append((t, "bl target"))
        else:
            funcs.append((t, fb, name))
            confirmed_spans.append((t, fb))

    return funcs, fakes, thunks


# Capstone branch mnemonics (ARM/Thumb). IMPORTANT: do not use
# startswith("b") — false friends bfi/bic/bics/bkpt also start with "b".
UNCOND_BR = {"b", "b.w"}
COND_BR = {"beq", "bne", "bge", "bgt", "bgt.w", "bhi", "bhs", "ble", "blo",
           "bls", "blt", "blt.w", "bmi", "bpl", "bvc", "bvs", "cbz", "cbnz"}


def writes_pc(mn, op):
    """Instruction writes to PC => return/branch, fall-through cannot be traversed
    (otherwise BFS will leak into trailing literal pool).
      - bx rX / bx lr
      - ldr pc, [..]  / mov pc, rX / add|sub pc, ..  (pc = FIRST operand)
      - pop {.., pc}
    Note: `ldr r0, [pc, #imm]` is NOT a return (pc is base in brackets, not dest).
    """
    if mn == "bx":
        return True
    if mn in ("pop", "pop.w"):
        return "pc" in op
    first = op.split(",")[0].strip()
    return first == "pc"


def find_internal_blocks(insns, fa, fb):
    """Map internal blocks of function: b/b.w/b.cond/cbz/cbnz targets inside
    [fa, fb) that have NO backwards references (loop headers excluded —
    their sources lie above the target). Exposes internal dispatch branches
    (e.g., case blocks in RX parser 0x1e9e0, invoked via `b` in shared frame)
    as a distinct navigation list.

    Returns [(t, end, srcs)] — t = block start, end = next block or fb.
    """
    srcs = defaultdict(set)
    for ins in insns:
        mn, op = ins.mnemonic, ins.op_str.strip()
        is_br = (mn in UNCOND_BR) or (mn in COND_BR)
        if not is_br or not op.startswith("#"):
            continue
        t = int(op[1:], 16) & ~1
        if fa < t < fb:
            srcs[t].add(ins.address - BASE)
    blocks = [t for t in sorted(srcs) if all(s < t for s in srcs[t])]
    out = []
    for i, t in enumerate(blocks):
        end = blocks[i + 1] if i + 1 < len(blocks) else fb
        out.append((t, end, sorted(srcs[t])))
    return out


def reachable_addrs(insns, fa, fb):
    """Set of instruction addresses genuinely reachable from function entry.

    Direct BFS: entry fa -> fall-through + branch targets. Rules:
      - normal instr / data   -> fall-through (next address);
      - unconditional b       -> target only (fall-through dead);
      - conditional b.* / cbz -> both target and fall-through;
      - bl / blx              -> fall-through only (call returns);
      - write to PC           -> terminal (bx / ldr pc,[..] / pop {..,pc} /
                                 mov|add|sub pc,..): do not proceed on fall-through,
                                 otherwise BFS drops into trailing literal pool.
    Targets outside [fa, fb) are dropped (other functions).

    Purpose: true literal pools CANNOT overlap with reachable code —
    execution does not jump into data. If a pool candidate lands on a
    reachable instruction/branch target, it is code, not pool (false ldr match).
    """
    by_addr = {i.address: i for i in insns}
    if fa not in by_addr:
        return set()
    reach = set()
    stack = [fa]
    while stack:
        a = stack.pop()
        if a in reach or a not in by_addr:
            continue
        reach.add(a)
        ins = by_addr[a]
        nxt = a + ins.size
        mn = ins.mnemonic
        if mn in UNCOND_BR:
            if ins.op_str.startswith("#"):
                stack.append(int(ins.op_str[1:], 16) & ~1)
            # unconditional: fall-through dead
        elif mn in COND_BR:
            if ins.op_str.startswith("#"):
                stack.append(int(ins.op_str[1:], 16) & ~1)
            stack.append(nxt)          # conditional: target and fall-through
        elif mn in ("bl", "blx"):
            stack.append(nxt)          # call returns
        elif writes_pc(mn, ins.op_str.strip()):
            pass                        # return (ldr pc / pop {pc} / mov pc / bx) — terminal
        else:
            stack.append(nxt)
    return reach


def pool_overlaps_code(p, words, reach, size_of):
    """True if pool of `words` words @p overlaps any reachable instruction.

    Exact size overlap: instr [a, a+size) vs pool [p, p+4w).
    """
    lo, hi = p, p + 4 * words
    for a in reach:
        s = size_of.get(a, 2)
        if a < hi and (a + s) > lo:
            return True
    return False


# --------------------------------------------------------------------------
# Literals / pools / analysis
# --------------------------------------------------------------------------

def pc_lit_pools(d, insns, N):
    """From ldr rX,[pc,#imm] instructions -> set of pool offsets in file."""
    pools = set()
    for ins in insns:
        if ins.mnemonic not in ("ldr", "ldr.w") or "[pc" not in ins.op_str:
            continue
        m = re.search(r"#(-?0x[0-9a-f]+|-?\d+)", ins.op_str.split(",", 1)[1])
        if not m:
            continue
        imm = int(m.group(1), 16) if "x" in m.group(1) else int(m.group(1))
        pool = ((ins.address + 4) & ~3) + imm - BASE
        if 0 <= pool + 4 <= N:
            pools.add(pool)
    return pools


def classify(v, d, strings, func_starts):
    """Classification of 32-bit literal -> (cls, extra).

    Classes: string | func | data | data-mirror | peri | ram | sys | other.
    """
    N = len(d)
    # flash mirror 0x08000000: reference to code/data via mirror base
    if MIRROR <= v < MIRROR + N:
        off = v - MIRROR
        if off in strings:
            return ("string", off)
        if off in func_starts:
            return ("func", off)
        return ("data-mirror", off)
    off = v - BASE
    if off in strings:
        return ("string", off)
    if 0x40000000 <= v < 0x60000000:
        return ("peri", None)
    if 0x20000000 <= v < 0x21000000:
        return ("ram", None)
    if 0xE0000000 <= v < 0xE0100000:
        return ("sys", None)
    if 0 <= off < N:
        if off in func_starts:
            return ("func", off)
        return ("data", off)
    return ("other", None)


def _lit_tag(cls, extra, strings):
    if cls == "string":
        return f'"{strings[extra]}"'
    if cls == "func":
        return fname_of(extra)
    if cls == "data":
        return f"data @0x{extra:05x}"
    if cls == "data-mirror":
        return f"flash-mirror @0x{extra:05x}"
    if cls == "peri":
        return "peripheral"
    if cls == "ram":
        return "RAM"
    if cls == "sys":
        return "Cortex-M (NVIC/SCB/SysTick)"
    return ""


def analyze_function(d, strings, func_starts, code_insns, pool_words, valid_pools=None):
    """Analysis of function code + its pool words. Returns (str_refs, lit_map,
    callees, lines). valid_pools — set of verified pool offsets; if specified,
    ldr[pc] literal is annotated only when its pool was not filtered out as false
    (overlapping reachable code)."""
    N = len(d)
    str_refs = []
    lit_map = {}
    callees = []
    lines = []
    pending_movw = {}

    def note_lit(src, v):
        if v in lit_map:
            return
        cls, extra = classify(v, d, strings, func_starts)
        lit_map[v] = (src, cls, extra)
        if cls == "string":
            str_refs.append((src, v, strings[extra]))

    def lit_comment(v):
        cls, extra = lit_map[v][1], lit_map[v][2]
        tag = _lit_tag(cls, extra, strings)
        return f"-> {tag}" if tag else ""

    for ins in code_insns:
        comment = []
        if ins.mnemonic == "data":
            text = ".h " + " ".join(f"0x{x:02x}" for x in ins.bytes)
            lines.append((ins.address, text, ""))
            continue
        if ins.mnemonic in ("ldr", "ldr.w") and "[pc" in ins.op_str:
            m = re.search(r"#(-?0x[0-9a-f]+|-?\d+)", ins.op_str.split(",", 1)[1])
            if m:
                imm = int(m.group(1), 16) if "x" in m.group(1) else int(m.group(1))
                pool = ((ins.address + 4) & ~3) + imm - BASE
                if 0 <= pool + 4 <= N and (valid_pools is None or pool in valid_pools):
                    v = struct.unpack_from("<I", d, pool)[0]
                    note_lit(ins.op_str.split(",")[0].strip(), v)
                    c = lit_comment(v)
                    if c:
                        comment.append(c)
        m = re.match(r"(mov\.?[wt]) (r\d+), #(0x[0-9a-f]+|\d+)", ins.op_str)
        if m:
            mn, reg, imm = m.group(1).replace(".", ""), m.group(2), int(m.group(3), 16)
            if mn == "movw":
                pending_movw[reg] = imm
            elif mn == "movt" and reg in pending_movw:
                v = (imm << 16) | pending_movw.pop(reg)
                note_lit(f"movw/movt {reg}", v)
                c = lit_comment(v)
                if c:
                    comment.append(c)
        if (ins.mnemonic in ("bl", "blx") or ins.mnemonic in UNCOND_BR) \
                and ins.op_str.startswith("#"):
            tgt = int(ins.op_str[1:], 16) & ~1
            callees.append((tgt, ins.mnemonic))
            toff = tgt - BASE
            if toff in func_starts:
                comment.append(f"-> {fname_of(toff)}")
            elif 0 <= toff < N:
                comment.append(f"-> 0x{toff:05x} (outside function list)")

        text = f"{ins.mnemonic} {ins.op_str}".strip()
        lines.append((ins.address, text, " ; ".join(comment)))

    for pool_off, v in pool_words:
        note_lit(f"pool @0x{pool_off:05x}", v)

    return str_refs, lit_map, callees, lines


def main():
    d = open(FW, "rb").read()
    N = len(d)
    strings = load_strings(d)

    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
    md.detail = True

    funcs, fakes, thunks = detect_functions(d, md)
    func_starts = {fa for fa, _, _ in funcs}
    print(f"[i] functions confirmed: {len(funcs)}; "
          f"false candidates: {len(fakes)}; trampolines: {len(thunks)}")

    # overlap resolution (xref-demotion) — as in BLE version
    md_sd = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
    md_sd.skipdata = True
    code_of = {}
    for fa, fb, _ in funcs:
        code_of[fa] = list(md_sd.disasm(d[fa:fb], BASE + fa))

    callers = defaultdict(list)
    for fa, insns in code_of.items():
        for ins in insns:
            if (ins.mnemonic in ("bl", "blx") or ins.mnemonic in UNCOND_BR) \
                    and ins.op_str.startswith("#"):
                toff = int(ins.op_str[1:], 16) & ~1
                if toff in func_starts:
                    callers[toff].append((fa, ins.address, ins.mnemonic))

    kept, demoted = [], []
    for fa, fb, rname in sorted(funcs):
        xr = len(callers.get(fa, []))
        clash = None
        for k in range(len(kept)):
            ka, kb, kr = kept[k]
            if fa < kb and ka < fb:
                clash = k
                break
        if clash is None:
            kept.append((fa, fb, rname))
            continue
        ka, kb, kr = kept[clash]
        kxr = len(callers.get(ka, []))
        if xr > 0 and kxr == 0:
            kept[clash] = (fa, fb, rname)
            demoted.append((ka, kr))
        else:
            demoted.append((fa, rname))
    if demoted:
        print(f"[i] resolved overlaps (demoted): {len(demoted)}")
        fakes = fakes + [(a, "demoted (overlap)") for a, _ in demoted]
        keep_set = {k[0] for k in kept}
        code_of = {fa: v for fa, v in code_of.items() if fa in keep_set}
        funcs = kept

    # literal pools: compute after demotion and DROP false ones — those
    # overlapping reachable code (execution does not jump into data; pool
    # over live instructions/branch targets = dead/unresolved ldr).
    global_reach, size_of = set(), {}
    for fa, fb, _ in funcs:
        global_reach |= reachable_addrs(code_of[fa], fa, fb)
        for i in code_of[fa]:
            size_of[i.address] = i.size
    pool_of, n_suppr = {}, 0
    for fa, fb, _ in funcs:
        kept_refs = []
        for p in sorted(pc_lit_pools(d, code_of[fa], N)):
            if not (0 <= p + 4 <= N):
                continue
            if pool_overlaps_code(p, 1, global_reach, size_of):
                n_suppr += 1
                continue
            kept_refs.append(p)
        pool_of[fa] = [(p, struct.unpack_from("<I", d, p)[0]) for p in kept_refs]
    if n_suppr:
        print(f"[i] suppressed false pools (overlapping reachable code): {n_suppr}")

    os.makedirs(OUT_DIR, exist_ok=True)
    for old in glob.glob(os.path.join(OUT_DIR, "func_*.md")):
        os.remove(old)
    index_rows = []
    for fa, fb, rname in funcs:
        valid_pools = {p for p, _ in pool_of[fa]}
        str_refs, lit_map, callees, lines = analyze_function(
            d, strings, func_starts, code_of[fa], pool_of[fa], valid_pools)
        pool_words = pool_of[fa]

        fname = fname_of(fa)
        uniq_callees = sorted(set(callees))
        call_lines = []
        for tgt, mn in uniq_callees:
            toff = tgt - BASE
            if toff in func_starts:
                call_lines.append(f"- `{fname_of(toff)}` (0x{tgt:08x}, {mn})")
            elif 0 <= toff < N:
                call_lines.append(f"- 0x{toff:05x} ({mn}, outside function list)")
            else:
                call_lines.append(f"- 0x{tgt:08x} ({mn}, outside image — runtime/external)")

        xref_lines = [f"- `{fname_of(src)}` ({mn} @0x{addr:08x})"
                      for src, addr, mn in sorted(callers.get(fa, []))]

        blocks = find_internal_blocks(code_of[fa], fa, fb)
        block_lines = []
        if len(blocks) >= 3:
            for t, end, src_list in blocks:
                srcs_txt = ", ".join(f"0x{s:05x}" for s in src_list[:4]) \
                    + ("..." if len(src_list) > 4 else "")
                block_lines.append(f"- `0x{t:05x}..0x{end:05x}` ({end - t} B); "
                                   f"targets from: {srcs_txt}")

        str_lines = [f'- `{src}`: 0x{v:08x} — "{t}"'
                     for src, v, t in sorted(set(str_refs), key=lambda x: (x[1], x[0]))] \
            or ["- (none)"]

        lit_lines = []
        for v, (src, cls, extra) in sorted(lit_map.items()):
            if cls == "string":
                continue
            tag = _lit_tag(cls, extra, strings)
            lit_lines.append(f"- 0x{v:08x} — {tag} ({src})" if tag
                             else f"- 0x{v:08x} — other ({src})")

        asm_lines = [f"  {addr:05x}:  {text:<34}{comment}" for addr, text, comment in lines]
        runs, cur = [], []
        for p, v in pool_words:
            if cur and p == cur[-1][0] + 4:
                cur.append((p, v))
            else:
                if cur:
                    runs.append(cur)
                cur = [(p, v)]
        if cur:
            runs.append(cur)
        for run in runs:
            p0, pn = run[0][0], len(run)
            outside = p0 < fa or p0 + 4 * pn > fb
            asm_lines.append(f"  ; --- literal pool @0x{p0:05x} ({pn} words)"
                             f"{' — OUTSIDE function bounds' if outside else ''} ---")
            for p, v in run:
                cls, extra = classify(v, d, strings, func_starts)
                tag = _lit_tag(cls, extra, strings)
                asm_lines.append(f"  {p:05x}:  .word 0x{v:08x}{'  ; ' + tag if tag else ''}")

        content = f"""# {fname}

| | |
|---|---|
| offset = vaddr (base 0x0; mirror 0x0800{fa:05x}) | `0x{fa:08x}` |
| code size | {fb - fa} B |
| region | {rname} |

## Strings (referenced via literal pools / movw+movt)

{chr(10).join(str_lines)}

## Literals and addresses

{chr(10).join(lit_lines) if lit_lines else "- (none)"}

## Callees

{chr(10).join(call_lines) if call_lines else "- (none)"}

## Callers / xrefs

{chr(10).join(xref_lines) if xref_lines else "- (not found in image code)"}
{chr(10) + chr(10) + "## Internal blocks (b/b.w/cbz targets inside function; loop headers excluded)" + chr(10) + chr(10) + chr(10).join(block_lines) if block_lines else ""}

## Disassembly

```asm
{chr(10).join(asm_lines)}
```
"""
        with open(os.path.join(OUT_DIR, f"{fname}.md"), "w", encoding="utf-8") as f:
            f.write(content)

        top_str = "; ".join(dict.fromkeys(t for _, _, t in str_refs))[:60]
        index_rows.append((fa, fb - fa, rname, top_str, len(callers.get(fa, []))))

    # index
    idx = ["# MCU Firmware Function Reference (mcu_0007.bin)",
           "",
           f"Image: `mcu_0007.bin` ({N} B) — scooter BLDC motor controller, "
           "**Cortex-M4F** (GD32/STM32F1-class), HAL-based, **unencrypted** "
           "(Mijia signature in trailer). No vector table is present (OTA APP payload region only).",
           "",
           "**Memory map:** Flash @ `0x00000000` (mirror `0x08000000` — part of "
           f"literals reference via mirror: {sum(1 for v in set(w for fl in pool_of.values() for _, w in fl) if MIRROR <= v < MIRROR + N)} pool words), "
           "RAM @ `0x20000000` (128 KB), Peripherals @ `0x40000000`, SYS @ `0xE0000000`. "
           "vaddr == file offset.",
           "",
           "**Detection algorithm:** starts = prologue `push {..,lr}` (B5xx) | `push.w {..,lr}` (T4, "
           "Capstone-verified) | `bl` targets outside confirmed functions (no-prologue "
           "leafs/ISRs). Epilogue confirmation (`pop {..,pc}` / `bx lr` / 'pop-lr'+b|bx / "
           "`bx rX` tail-call / `b` to trampoline — hot target >=3, block with epilogue, chains; "
           "trampolines detected via bytewise scan + Capstone because sequential decoding of regions "
           "desynchronizes). Boundary = BFS maximum in verified window (split-body/"
           "cold paths); literal pools excluded from boundary (may lie past subsequent functions — "
           "printed in tables marked 'OUTSIDE bounds'). Overlaps resolved via incoming xrefs.",
           "",
           f"Confirmed functions: **{len(funcs)}**; "
           f"false candidates: {len(fakes)}; trampolines: {len(thunks)}.",
           "",
           "> **Virtually no strings in image** (controller without debug logging) — understanding of functions "
           "relies on literals (peripherals/RAM), xrefs, and manual tracing. Known anchors: "
           "USART3 protocol <-> BLE `0x1e480`/`0x1e9e0`/`0x1f600`/`0x1f6b4`, HAL_UART_Transmit "
           "`0x23188`, FLASH-OTA `0x06230`, ADC `0x1a31c`, motor TIM1 `0x22a48`-`0x22fac`.",
           "",
           "Regions (code sections; gaps are data/tables):"]
    for a, b, n in REGIONS:
        idx.append(f"- `0x{a:05x}-0x{b:05x}` ({b - a} B) — {n}")
    idx += ["",
            "Regeneration: `$env:PYTHONIOENCODING=\"utf-8\"; python research/scripts/gen_functions_mcu.py`.",
            "",
            "| offset | size | region | strings | callers |",
            "|---|---|---|---|---|"]
    for fa, size, rname, top_str, ncall in index_rows:
        idx.append(f"| [`0x{fa:05x}`](func_0x{fa:05x}.md) | {size} | "
                   f"{rname.split(' (')[0]} | {top_str or '—'} | {ncall} |")
    if fakes:
        idx += ["",
                "## False Candidates (data/labels, not functions)",
                ""]
        for fa, kind in fakes[:100]:
            idx.append(f"- `0x{fa:05x}` ({kind}, {region_name(fa)})")
        if len(fakes) > 100:
            idx.append(f"- ... {len(fakes) - 100} more")

    with open(os.path.join(OUT_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx) + "\n")

    n_str = sum(1 for r in index_rows if r[3])
    print(f"[+] functions: {len(funcs)}, with strings: {n_str} -> {OUT_DIR}")


if __name__ == "__main__":
    main()
