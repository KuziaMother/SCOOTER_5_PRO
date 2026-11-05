#!/usr/bin/env python3
"""
Function reference for open (PLAIN) code in the xiaomi.scooter.5pro BLE image.

Generates research/functions_ble/*.md — one file per CONFIRMED
function:
    - metadata (offset, vaddr at base 0x01800000, size, region);
    - strings referenced by the function via literal pools (ldr/ldr.w [pc]) / movw+movt(.w);
    - all literals (peripherals, RAM, image addresses);
    - callees (bl/b) and callers (xrefs from all functions in the region);
    - disassembly (capstone, Thumb) with line-by-line annotations;
      function literal pools are rendered as word tables, not "code".

Detection (two passes):
  1. candidates = prologue `push {..,lr}` (halfword & 0xFF00 == 0xB500) OR
     `push.w {..,lr}` (T4 encoding, first halfword 0xE92D — occurs
     52 times in this image, randomly ~0.2) in PLAIN regions;
  2. epilogue: pop {..,pc} | bx lr | "pop lr" + (<=4 instr) b/b.w|bx rX |
     bx rX/ip/fp/sl (indirect tail-call) | b/b.w to trampoline. "pop lr" =
     pop {..,lr} | ldmfd sp!,{..,lr} | ldr lr,[sp],#n (armcc encoding).
  3. trampolines: address is target of >=3 branches (hot) OR its block starts with
     a valid epilogue; FIXED-POINT search over actual `b` targets
     (chains `b #U` -> U is already a trampoline/epilogue). Only real branch
     targets are considered — data never jumped to is not marked.
  4. pass 1: confirmation in baseline window [candidate, next candidate);
     pass 2: unconfirmed expand window in 256 B steps (up to +1KB), BUT
     stop before the next CONFIRMED candidate — otherwise a false
     candidate would absorb the epilogue of the subsequent real function;
  5. boundary fb = maximum reachable from prologue in verified window (BFS:
     fallthrough + b/b.w/conditionals/cbz/cbnz/tbb; bl/blx/bx are not followed,
     trampoline targets are excluded) — captures split-body/cold paths.
     Literal pools do NOT expand fb: compiler places pools far away (even past
     subsequent functions), and words are printed in tables by absolute offsets;
  6. range overlaps are resolved post-factum: between two overlapping
     confirmed candidates, the one with incoming bl/b xrefs is kept;
     on tie — the leftmost; loser is demoted to false candidates;
  7. unconfirmed candidates are false positives on data; they do NOT receive
     an md file, but are listed in README.md index.

Note: image is PURELY Thumb (no ARM code in PLAIN; "E92D" is T4 push.w, not
ARM PUSH). bl targets at 0x15xxxxxx/0x16xxxxxx/0x17xxxxxx are runtime-RAM
(code/data copied to SRAM at boot), they DO NOT exist in the raw image.

Regions and base — from docs/FACTS.md / REPORT.md:
  flash base 0x01800000; 0x00400-0x02a00 = header + bootloader (PLAIN),
  0x06000-0x0a200 = flash driver / OTA (PLAIN).

Usage:  python research/scripts/gen_functions.py   (from anywhere)
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
FW = os.path.join(RES, "images", "ble_2.7.0_0015.bin")
OUT_DIR = os.path.join(RES, "functions_ble")

BASE = 0x01800000          # RTL8762C flash base (REPORT.md, header[0x28]=0x01803000)
REGIONS = [
    (0x00400, 0x02a00, "header + bootloader (PLAIN)"),
    (0x06000, 0x0a200, "flash driver / OTA code (PLAIN)"),
]


def fname_of(off):
    return f"func_0x{off:05x}"


def load_strings(d):
    """offset -> text (ASCII strings >=4 characters)."""
    return {m.start(): m.group().decode("ascii", "ignore")
            for m in re.finditer(rb"[ -~]{4,}", d)}


def is_prologue(d, off):
    """push {..,lr} (16-bit) or push.w {..,lr} (T4, first halfword 0xE92D)."""
    w = struct.unpack_from("<H", d, off)[0]
    if (w & 0xFF00) == 0xB500:             # push {..,lr}
        return True
    return w == 0xE92D and off + 4 <= len(d)   # push.w {..,lr}


def _block_starts(d, md, t):
    """First instructions of block at vaddr t (or [] if outside file)."""
    off = t - BASE
    if not (0 <= off + 2 <= len(d)):
        return []
    return list(md.disasm(d[off:off + 16], BASE + off))


def _first_b_target(d, md, t):
    """If block at t starts with b/b.w #T — return T (vaddr), else None."""
    insns = _block_starts(d, md, t)
    if not insns or insns[0].mnemonic not in ("b", "b.w"):
        return None
    op = insns[0].op_str.strip()
    return int(op[1:], 16) & ~1 if op.startswith("#") else None


def _starts_with_epilogue(d, md, t):
    """Block at t starts with pop {..,pc} / pop {..,lr}+bx rX."""
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


def find_thunks(d, regions):
    """Set of trampoline addresses where b/b.w is a valid epilogue.

    In this image, functions heavily end in tail-branch to shared return code:
    0x18089f4 = pop{r4,r5,r6,pc}; 0x1808cbc = b #0x18084d0 (exit dispatcher);
    0x1809576 = pop.w{r4-r8,pc}+dispatcher; chains up to 3 hops:
    0x1808bae -> 0x1808538 -> 0x1808374 = pop.w{r4-r8,pc}.

    Rule: (a) target is 'hot' (>=3 b/b.w branches); (b) block at target
    starts with direct epilogue; (c) FIXED-POINT: target T whose block starts
    with `b #U`, where U is already a trampoline or direct epilogue. Safety: only
    REAL branch targets are considered — data never jumped to will not be marked
    as trampolines; and a label jumped to from outside whose block starts with b
    is a trampoline by definition.
    """
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
    md.skipdata = True
    cnt = Counter()
    targets = set()
    for a, b, _ in regions:
        for ins in md.disasm(d[a:b], BASE + a):
            if ins.mnemonic in ("b", "b.w") and ins.op_str.startswith("#"):
                t = int(ins.op_str[1:], 16) & ~1
                cnt[t] += 1
                targets.add(t)
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
    """First valid epilogue in program. Returns (i_start, j_end, kind) or
    None; j_end = index of LAST instruction in epilogue sequence.

    Valid terminations: pop{..,pc} | bx lr | 'pop lr' + <=4 instr b/b.w|bx rX |
    bx rX/ip/fp/sl (indirect tail-call) | b/b.w to trampoline (shared epilogue).
    'pop lr' = pop {..,lr} | ldmfd sp!,{..,lr} | ldr lr,[sp],#n (armcc encoding).
    """
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
            # pop-lr + short tail (movs/movw/ldr) + b/b.w or bx rX (tail-branch)
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
            # rX or aliases (ip=r12, fp=r11, sl=r10) — indirect tail-call
            if re.fullmatch(r"(r\d+|ip|fp|sl)", op):
                return i, i, f"bx {op} (tail-call)"
        elif mn in ("b", "b.w") and op.startswith("#"):
            if int(op[1:], 16) & ~1 in thunks:
                return i, i, f"b thunk@{op[1:]}"
    return None


def reach_end(d, md, fa, win_end, thunks):
    """Maximum offset reachable from fa within [fa, win_end).

    BFS: fallthrough (including through data entries and tbb/tbh tables — capstone
    positions decode past the table itself) + all direct/conditional branches (b/b.w,
    beq..ble, cbz/cbnz), but NOT bl/blx/bx and NOT trampoline targets (they = epilogue).
    Yields split-body function boundary: cold paths past epilogue are included in fb."""
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
        is_branch = (mn.startswith("b") and mn not in ("bl", "blx")) \
            or mn in ("cbz", "cbnz")
        if is_branch:
            if op.startswith("#"):
                t = (int(op[1:], 16) & ~1) - BASE
                if fa <= t < hi and t not in thunks:
                    stack.append(t)
            if mn not in ("b", "b.w"):        # conditional: fallthrough possible
                nxt = next_map.get(off)
                if nxt is not None:
                    stack.append(nxt)
        elif mn in ("bx",):
            pass                               # indirect — do not traverse
        else:
            # pop{..,pc} returns: fallthrough only for other instructions
            if not (mn in ("pop", "pop.w") and "pc" in op):
                nxt = next_map.get(off)
                if nxt is not None:
                    stack.append(nxt)
    return max_addr


def detect_functions(d, md, regions):
    """Returns (funcs, fakes):
    funcs: [(fa, fb, region_name)] — fb = CODE boundary: maximum reachable
           from prologue within verified window (BFS: split-body/cold paths/tbb);
           literal pools are NOT included in fb (may lie past subsequent functions —
           words are printed separately by absolute offsets);
    fakes: [(fa, region_name)] — unconfirmed candidates.

    Two passes: (1) baseline window up to next candidate; (2) expansion of
    unconfirmed — but NOT past the next confirmed candidate from pass 1
    (otherwise a false candidate absorbs the epilogue of a real function => overlaps).
    Confirmation runs with skipdata=True: linear decoding would otherwise abort
    on literal pools containing 'invalid' Thumb bytes and miss the epilogue."""
    md_sd = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
    md_sd.skipdata = True
    thunks = find_thunks(d, regions)
    N = len(d)
    funcs, fakes = [], []
    for a, b, name in regions:
        cands = [off for off in range(a, b, 2) if is_prologue(d, off)]

        # --- pass 1: baseline window [candidate, next candidate) ---
        p1 = {}   # fa -> epi or None
        for i, fa in enumerate(cands):
            limit = cands[i + 1] if i + 1 < len(cands) else b
            insns = list(md_sd.disasm(d[fa:limit], BASE + fa))
            p1[fa] = find_epilogue(insns, thunks)
        confirmed1 = {fa for fa, e in p1.items() if e is not None and e[0] >= 1}

        real = []
        for i, fa in enumerate(cands):
            limit = cands[i + 1] if i + 1 < len(cands) else b
            epi = p1[fa]
            win_end = limit
            if epi is None or epi[0] < 1:
                # --- pass 2: expansion, but not past the next
                # confirmed candidate (it is a real function, not our tail) ---
                stop = b
                for fc in cands[i + 1:]:
                    if fc in confirmed1:
                        stop = fc
                        break
                ext = 0
                while (epi is None or epi[0] < 1) and win_end < min(stop, b) \
                        and ext < 0x400:
                    ext += 0x100
                    win_end = min(limit + ext, stop, b)
                    insns = list(md_sd.disasm(d[fa:win_end], BASE + fa))
                    epi = find_epilogue(insns, thunks)
                if epi is None or epi[0] < 1:   # minimum prologue + >=1 instr
                    fakes.append((fa, name))
                    continue
            # boundary = maximum reachable from prologue in window (BFS);
            # literal pools are not traversed (ldr[pc] is not a branch) and are printed separately
            fb = reach_end(d, md_sd, fa, win_end, thunks)
            real.append((fa, fb))
        funcs.extend((fa, fb, name) for fa, fb in real)
    return funcs, fakes


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
    """Classification of 32-bit literal -> (cls, extra)."""
    off = v - BASE
    if off in strings:
        return ("string", off)
    if 0x40000000 <= v < 0x60000000:
        return ("peri", None)
    if 0x20000000 <= v < 0x21000000 or 0x00200000 <= v < 0x00300000:
        return ("ram", None)
    if 0 <= off < len(d):
        if off in func_starts:
            return ("func", off)
        return ("data", off)
    return ("other", None)


def analyze_function(d, strings, func_starts, code_insns, pool_words):
    """Analysis of function code + its pool words.

    Returns (str_refs, lit_map, callees, lines).
    """
    N = len(d)
    str_refs = []          # (src, vaddr, text)
    lit_map = {}           # vaddr -> (src, cls, extra)
    callees = []           # (vaddr, 'bl'|'b')
    lines = []             # (vaddr, text, comment)
    pending_movw = {}      # reg -> low16

    def note_lit(src, v):
        if v in lit_map:
            return
        cls, extra = classify(v, d, strings, func_starts)
        lit_map[v] = (src, cls, extra)
        if cls == "string":
            str_refs.append((src, v, strings[extra]))

    def lit_comment(v):
        cls, extra = lit_map[v][1], lit_map[v][2]
        if cls == "string":
            return f'-> "{strings[extra]}"'
        if cls == "func":
            return f"-> {fname_of(extra)}"
        if cls == "data":
            return f"-> image data @0x{extra:05x}"
        if cls == "peri":
            return "(periph)"
        if cls == "ram":
            return "(RAM)"
        return ""

    for ins in code_insns:
        comment = []
        # data inside code (skipdata): print as is
        if ins.mnemonic == "data":
            text = ".h " + " ".join(f"0x{x:02x}" for x in ins.bytes)
            lines.append((ins.address, text, ""))
            continue
        # ldr rX, [pc, #imm] (16-bit and 32-bit ldr.w; imm may be negative)
        if ins.mnemonic in ("ldr", "ldr.w") and "[pc" in ins.op_str:
            m = re.search(r"#(-?0x[0-9a-f]+|-?\d+)", ins.op_str.split(",", 1)[1])
            if m:
                imm = int(m.group(1), 16) if "x" in m.group(1) else int(m.group(1))
                pool = ((ins.address + 4) & ~3) + imm - BASE
                if 0 <= pool + 4 <= N:
                    v = struct.unpack_from("<I", d, pool)[0]
                    note_lit(ins.op_str.split(",")[0].strip(), v)
                    c = lit_comment(v)
                    if c:
                        comment.append(c)
        # movw/movt (and 32-bit mov.w/movt.w) -> 32-bit address
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
        # bl / b -> callee
        if ins.mnemonic in ("bl", "b") and ins.op_str.startswith("#"):
            tgt = int(ins.op_str[1:], 16) & ~1
            callees.append((tgt, ins.mnemonic))
            toff = tgt - BASE
            if toff in func_starts:
                comment.append(f"-> {fname_of(toff)}")
            elif 0 <= toff < N:
                comment.append(f"-> 0x{toff:05x} (outside function list)")

        text = f"{ins.mnemonic} {ins.op_str}".strip()
        lines.append((ins.address, text, " ; ".join(comment)))

    # pool words are also considered literals of the function
    for pool_off, v in pool_words:
        note_lit(f"pool @0x{pool_off:05x}", v)

    return str_refs, lit_map, callees, lines


def main():
    d = open(FW, "rb").read()
    N = len(d)
    strings = load_strings(d)

    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
    md.detail = True

    funcs, fakes = detect_functions(d, md, REGIONS)
    func_starts = {fa for fa, _, _ in funcs}
    print(f"[i] prologue candidates: confirmed {len(funcs)}, "
          f"false (data): {len(fakes)}")

    # first pass: disassemble code of each function ([fa, fb) — code only);
    # skipdata=True — prevent decoding from aborting on data inside function.
    # Literal pools are SEPARATED from boundary: words read by absolute offsets
    # (compiler places pools far away — even past subsequent functions).
    md_sd = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
    md_sd.skipdata = True
    code_of, pool_of = {}, {}
    for fa, fb, _ in funcs:
        full = list(md_sd.disasm(d[fa:fb], BASE + fa))
        code_of[fa] = full
        refs = sorted(pc_lit_pools(d, full, N))
        pool_of[fa] = [(p, struct.unpack_from("<I", d, p)[0]) for p in refs if p + 4 <= N]

    # xrefs: caller graph (bl and b) — code parts only
    callers = defaultdict(list)   # target_off -> [(src_func, addr, mn)]
    for fa, insns in code_of.items():
        for ins in insns:
            if ins.mnemonic in ("bl", "b") and ins.op_str.startswith("#"):
                toff = (int(ins.op_str[1:], 16) & ~1) - BASE
                if toff in func_starts:
                    callers[toff].append((fa, ins.address, ins.mnemonic))

    # overlap resolution: between two overlapping confirmed candidates,
    # the one with incoming xrefs (real called function) is kept;
    # on tie — leftmost; loser demoted to false candidates
    kept, demoted = [], []
    for fa, fb, rname in sorted(funcs):
        xr = len(callers.get(fa, []))
        clash = None
        for k in range(len(kept)):
            ka, kb, kr = kept[k]
            if fa < kb and ka < fb:      # overlap
                clash = k
                break
        if clash is None:
            kept.append((fa, fb, rname))
            continue
        ka, kb, kr = kept[clash]
        kxr = len(callers.get(ka, []))
        if xr > 0 and kxr == 0:          # new is called, old is not: new is real
            kept[clash] = (fa, fb, rname)
            demoted.append((ka, kr))
        else:                            # otherwise keep (leftmost / with xref)
            demoted.append((fa, rname))
    if demoted:
        print(f"[i] resolved overlaps (demoted to false candidates): {len(demoted)}")
        fakes = fakes + demoted
        code_of = {fa: v for fa, v in code_of.items() if fa in {k[0] for k in kept}}
        pool_of = {fa: v for fa, v in pool_of.items() if fa in {k[0] for k in kept}}
        funcs = kept

    os.makedirs(OUT_DIR, exist_ok=True)
    # clean old md files from previous runs (demotions/boundary shifts otherwise leave orphan files)
    for old in glob.glob(os.path.join(OUT_DIR, "func_*.md")):
        os.remove(old)
    index_rows = []
    for fa, fb, rname in funcs:
        str_refs, lit_map, callees, lines = analyze_function(
            d, strings, func_starts, code_of[fa], pool_of[fa])
        pool_words = pool_of[fa]

        fname = fname_of(fa)
        uniq_callees = sorted(set(callees))
        call_lines = []
        for tgt, mn in uniq_callees:
            toff = tgt - BASE
            if toff in func_starts:
                call_lines.append(f"- `{fname_of(toff)}` (0x{tgt:08x}, {mn})")
            else:
                call_lines.append(f"- 0x{tgt:08x} ({mn}, outside function list)")

        xref_lines = [f"- `{fname_of(src)}` ({mn} @0x{addr:08x})"
                      for src, addr, mn in sorted(callers.get(fa, []))]

        str_lines = [f'- `{src}`: 0x{v:08x} — "{t}"'
                     for src, v, t in sorted(set(str_refs), key=lambda x: (x[1], x[0]))] \
            or ["- (none)"]

        lit_lines = []
        for v, (src, cls, extra) in sorted(lit_map.items()):
            if cls == "string":
                continue  # already in "Strings" section
            if cls == "func":
                lit_lines.append(f"- 0x{v:08x} — `{fname_of(extra)}` ({src})")
            elif cls == "data":
                lit_lines.append(f"- 0x{v:08x} — image data @0x{extra:05x} ({src})")
            elif cls == "peri":
                lit_lines.append(f"- 0x{v:08x} — peripheral ({src})")
            elif cls == "ram":
                lit_lines.append(f"- 0x{v:08x} — RAM ({src})")
            else:
                lit_lines.append(f"- 0x{v:08x} — other ({src})")

        asm_lines = [f"  {addr:08x}:  {text:<34}{comment}" for addr, text, comment in lines]
        # pools are grouped into sequential runs; if run lies outside function boundary
        # (compiler places pools far away) — mark it
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
                if cls == "string":
                    tag = f'"{strings[extra]}"'
                elif cls == "func":
                    tag = fname_of(extra)
                elif cls == "data":
                    tag = f"data @0x{extra:05x}"
                elif cls == "peri":
                    tag = "peripheral"
                elif cls == "ram":
                    tag = "RAM"
                else:
                    tag = ""
                asm_lines.append(f"  {p:05x}:  .word 0x{v:08x}{'  ; ' + tag if tag else ''}")

        content = f"""# {fname}

| | |
|---|---|
| file offset | `0x{fa:05x}` |
| vaddr (base 0x01800000) | `0x{BASE + fa:08x}` |
| code size | {fb - fa} B |
| region | {rname} |

## Strings (referenced via literal pools / movw+movt)

{chr(10).join(str_lines)}

## Literals and addresses

{chr(10).join(lit_lines) if lit_lines else "- (none)"}

## Callees

{chr(10).join(call_lines) if call_lines else "- (none)"}

## Callers / xrefs

{chr(10).join(xref_lines) if xref_lines else "- (not found in open regions)"}

## Disassembly

```asm
{chr(10).join(asm_lines)}
```
"""
        with open(os.path.join(OUT_DIR, f"{fname}.md"), "w", encoding="utf-8") as f:
            f.write(content)

        top_str = "; ".join(dict.fromkeys(t for _, _, t in str_refs))[:60]
        index_rows.append((fa, fb - fa, rname, top_str, len(callers.get(fa, []))))

    # where image strings reside (for README output)
    str_by_region = Counter()
    for off in strings:
        if 0x00400 <= off < 0x02a00:
            str_by_region["0x00400-0x02a00 (PLAIN bootloader)"] += 1
        elif 0x06000 <= off < 0x0a200:
            str_by_region["0x06000-0x0a200 (PLAIN flash/OTA)"] += 1
        elif 0x0a200 <= off < 0x25400:
            str_by_region["0x0a200-0x25400 (ENC APP)"] += 1
        else:
            str_by_region["other"] += 1

    # index
    idx = ["# BLE Firmware Function Reference (PLAIN regions)",
           "",
           f"Image: `ble_2.7.0_0015.bin` ({N} B), flash base `0x{BASE:08x}`.",
           "Detection (two passes): prologue `push {..,lr}` / `push.w {..,lr}` (T4) + "
           "epilogue verification (`pop {..,pc}` / `bx lr` / 'pop-lr'+b|bx — where pop-lr = "
           "`pop {..,lr}` | `ldmfd sp!,{..,lr}` | `ldr lr,[sp]`; indirect `bx rX`; "
           "`b` to trampoline — hot target >=3 or block beginning with an epilogue; "
           "trampoline chains resolved by fixed-point iteration over branch targets). "
           "Pass 2 expands the window only through unconfirmed candidates. "
           "Function boundary = maximum reachable from prologue within verified window "
           "(BFS: fallthrough + branches including tbb; bl/bx are not expanded) — "
           "capturing split-body and cold paths. 'Code size' does not include literal pools: "
           "the compiler places them distantly (sometimes across subsequent functions), so pool "
           "words are printed as an absolute-offset table marked 'OUTSIDE bounds'.",
           "",
           "> **Code mode:** PLAIN regions are STRICTLY Thumb mode (no ARM instructions; "
           "pattern `E92D` is 32-bit T4 `push.w`, not ARM PUSH). Branch-link (`bl`) targets to "
           "`0x15xxxxxx`/`0x16xxxxxx`/`0x17xxxxxx` are runtime-RAM (code copied into SRAM "
           "at boot) and do not exist in the raw binary image — md files cannot be generated for them.",
           "",
           f"Confirmed functions: **{len(funcs)}**; "
           f"false positives on data: {len(fakes)}.",
           "",
           "> **Takeaway:** PLAIN regions contain low-level code (bootloader + flash/OTA driver): "
           "the disassembled functions contain ZERO string references — all ldr[pc]/movw-movt literals "
           "address peripherals (0x4xxxxxxx), RAM (0x2xxxxxxx / 0x002xxxxx), and internal image addresses. "
           "Any 'strings' matched via regex in these regions are random byte noise (verified by sampling). "
           "Genuine strings and readable logic reside exclusively in the encrypted APP region "
           "0x0a200-0x25400 (decrypted only via XIP/SWD on hardware, see REPORT.md).",
           "",
           "Distribution of regex 'strings' across regions (for reference; in PLAIN regions these are noise):"]
    for k, v in str_by_region.most_common():
        idx.append(f"- {k}: {v}")
    idx += ["",
            "Regeneration: `python research/scripts/gen_functions.py`.",
            "",
            "| offset | vaddr | size | region | strings | callers |",
            "|---|---|---|---|---|---|"]
    for fa, size, rname, top_str, ncall in index_rows:
        idx.append(f"| [`0x{fa:05x}`](func_0x{fa:05x}.md) | `0x{BASE + fa:08x}` | {size} | "
                   f"{rname.split(' (')[0]} | {top_str or '—'} | {ncall} |")
    idx += ["",
            "## False Positives (data, not code)",
            ""]
    for fa, name in fakes:
        note = ""
        for a, b, _ in REGIONS:
            if a <= fa < b and b - fa < 0x60:
                note = (" — prologue at edge of PLAIN region: body likely continues "
                        "in encrypted area (epilogue unreachable)")
        idx.append(f"- `0x{fa:05x}` ({name.split(' (')[0]}){note}")

    with open(os.path.join(OUT_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx) + "\n")

    n_str = sum(1 for r in index_rows if r[3])
    print(f"[+] functions: {len(funcs)}, with strings: {n_str} -> {OUT_DIR}")


if __name__ == "__main__":
    main()
