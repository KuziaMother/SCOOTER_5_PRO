#!/usr/bin/env python3
"""
Справочник по функциям открытого (PLAIN) кода BLE-образа xiaomi.scooter.5pro.

Генерирует research/functions_ble/*.md — по одному файлу на ПОДТВЕРЖДЁННУЮ
функцию:
    - метаданные (offset, vaddr при базе 0x01800000, размер, регион);
    - строки, на которые функция ссылается через literal-пулы (ldr/ldr.w [pc]) / movw+movt(.w);
    - все литералы (периферия, RAM, адреса в образе);
    - callees (bl/b) и callers (xrefs из всех функций региона);
    - дизассембляция (capstone, Thumb) с построчными аннотациями;
      literal-пул функции печатается таблицей слов, а не «кодом».

Детекция (два прохода):
  1. кандидаты = пролог `push {..,lr}` (halfword & 0xFF00 == 0xB500) ИЛИ
     `push.w {..,lr}` (T4-кодирование, первый halfword 0xE92D — встречается
     в этом образе 52 раза, случайно ~0.2) в PLAIN-регионах;
  2. эпилог: pop {..,pc} | bx lr | «pop lr» + (<=4 instr) b/b.w|bx rX |
     bx rX/ip/fp/sl (косвенный tail-call) | b/b.w на «трамплин». «pop lr» =
     pop {..,lr} | ldmfd sp!,{..,lr} | ldr lr,[sp],#n (armcc так кодит).
  3. трамплины: адрес — цель >=3 ветвлений (горячий) ИЛИ его блок начинается с
     валидного эпилога; поиск ФИКСИРОВАННОЙ ТОЧКОЙ по реальным целям `b`
     (цепочки `b #U` → U уже трамплин/эпилог). Разыскиваются только реальные
     цели ветвлений — данные, на которые никто не прыгает, не помечаются.
  4. проход 1: подтверждение в базовом окне [кандидат, следующий кандидат);
     проход 2: неподтверждённые расширяют окно шагами по 256 Б (до +1KB), НО
     останавливаются перед следующим ПОДТВЕРЖДЁННЫМ кандидатом — иначе ложный
     кандидат «поглотил бы» эпилог следующей реальной функции;
  5. граница fb = максимум, достижимый из пролога в верифицированном окне (BFS:
     fallthrough + b/b.w/условные/cbz/cbnz/tbb; bl/blx/bx не разыгрываются,
     цели-трамплины не входят) — захватывает split-body/cold-пути.
     Literal-пулы НЕ расширяют fb: компилятор кладёт пулы далеко (даже за
     следующие функции), а слова печатаются таблицей по абсолютным offset'ам;
  6. пересечения диапазонов разрешаются постфактум: из двух пересекающихся
     подтверждённых кандидатов остаётся тот, на кого есть входящие bl/b (xref),
     при равенстве — левый; проигравший списывается в ложные;
   7. неподтверждённые кандидаты — ложные срабатывания на данных; они НЕ получают
     md, а перечисляются в README.md индекса.

Примечание: образ ЧИСТО Thumb (ARM-кода в PLAIN нет; «E92D» — T4 push.w, не
ARM PUSH). Цели bl на 0x15xxxxxx/0x16xxxxxx/0x17xxxxxx — это runtime-RAM
(код/данные, скопированные в SRAM при старте), в образе их НЕТ.

Регионы и база — из docs/FACTS.md / REPORT.md:
  база флеша 0x01800000; 0x00400-0x02a00 = заголовок+bootloader (PLAIN),
  0x06000-0x0a200 = flash-драйвер/OTA (PLAIN).

Запуск:  python research/scripts/gen_functions.py   (откуда угодно)
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

BASE = 0x01800000          # база флеша RTL8762C (REPORT.md, header[0x28]=0x01803000)
REGIONS = [
    (0x00400, 0x02a00, "заголовок + bootloader (PLAIN)"),
    (0x06000, 0x0a200, "flash-драйвер / OTA-код (PLAIN)"),
]


def fname_of(off):
    return f"func_0x{off:05x}"


def load_strings(d):
    """offset -> текст (ASCII-строки >=4 символа)."""
    return {m.start(): m.group().decode("ascii", "ignore")
            for m in re.finditer(rb"[ -~]{4,}", d)}


def is_prologue(d, off):
    """push {..,lr} (16-бит) или push.w {..,lr} (T4, первый halfword 0xE92D)."""
    w = struct.unpack_from("<H", d, off)[0]
    if (w & 0xFF00) == 0xB500:             # push {..,lr}
        return True
    return w == 0xE92D and off + 4 <= len(d)   # push.w {..,lr}


def _block_starts(d, md, t):
    """Первые инструкции блока по vaddr t (или [] если вне файла)."""
    off = t - BASE
    if not (0 <= off + 2 <= len(d)):
        return []
    return list(md.disasm(d[off:off + 16], BASE + off))


def _first_b_target(d, md, t):
    """Если блок по t начинается с b/b.w #T — вернуть T (vaddr), иначе None."""
    insns = _block_starts(d, md, t)
    if not insns or insns[0].mnemonic not in ("b", "b.w"):
        return None
    op = insns[0].op_str.strip()
    return int(op[1:], 16) & ~1 if op.startswith("#") else None


def _starts_with_epilogue(d, md, t):
    """Блок по t начинается с pop {..,pc} / pop {..,lr}+bx rX."""
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
    """Множество адресов-«трамплинов», на которые b/b.w = валидный эпилог.

    В этом образе функции массово заканчиваются tail-branch на общий код возврата:
    0x18089f4 = pop{r4,r5,r6,pc}; 0x1808cbc = b #0x18084d0 (exit-диспетчер);
    0x1809576 = pop.w{r4-r8,pc}+dispatcher; цепочки до 3 шагов:
    0x1808bae -> 0x1808538 -> 0x1808374 = pop.w{r4-r8,pc}.

    Правило: (a) цель «горячая» (>=3 ветвлений b/b.w); (b) блок по цели
    начинается с прямого эпилога; (c) ФИКС-ПОЙНТ: цель T, чей блок начинается
    с `b #U`, где U уже трамплин или прямой эпилог. Безопасность: разыскиваем
    только РЕАЛЬНЫЕ цели ветвлений (targets) — данные, на которые никто не
    прыгает, в трамплины не попадают; а метка, на которую прыгают извне и чей
    блок начинается с b, — это трамплин по определению.
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
    """Первый валидный эпилог в программе. Возвращает (i_start, j_end, kind) или
    None; j_end = индекс ПОСЛЕДНЕЙ инструкции эпилог-последовательности.

    Валидные окончания: pop{..,pc} | bx lr | «pop lr» + <=4 instr b/b.w|bx rX |
    bx rX/ip/fp/sl (косвенный tail-call) | b/b.w на трамплин (общий эпилог).
    «pop lr» = pop {..,lr} | ldmfd sp!,{..,lr} | ldr lr,[sp],#n (armcc так кодит).
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
            pop_lr = True                       # ldr lr,[sp],#4 ≡ pop {lr}
        elif mn == "ldm" and "{" in op:         # ldmfd sp!, {..,lr}
            regs = [r.strip() for r in op.split("{", 1)[1].rstrip("}").split(",")]
            pop_lr = "lr" in regs
        if pop_lr:
            # pop-lr + короткий хвост (movs/movw/ldr) + b/b.w или bx rX (tail-branch)
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
            # rX или алиасы (ip=r12, fp=r11, sl=r10) — косвенный tail-call
            if re.fullmatch(r"(r\d+|ip|fp|sl)", op):
                return i, i, f"bx {op} (tail-call)"
        elif mn in ("b", "b.w") and op.startswith("#"):
            if int(op[1:], 16) & ~1 in thunks:
                return i, i, f"b thunk@{op[1:]}"
    return None


def reach_end(d, md, fa, win_end, thunks):
    """Максимальный offset, достижимый из fa в пределах [fa, win_end).

    BFS: fallthrough (в т.ч. через data-записи и таблицы tbb/tbh — capstone сам
    позиционирует декод за таблицей) + все прямые/условные ветвления (b/b.w,
    beq..ble, cbz/cbnz), но НЕ bl/blx/bx и НЕ цели-трамплины (они = эпилог).
    Даёт границу split-body функций: cold-пути за эпилогом входят в fb."""
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
            if mn not in ("b", "b.w"):        # условные: возможен fallthrough
                nxt = next_map.get(off)
                if nxt is not None:
                    stack.append(nxt)
        elif mn in ("bx",):
            pass                               # косвенный — не разыгрываем
        else:
            # pop{..,pc} возвращает: fallthrough только для остальных
            if not (mn in ("pop", "pop.w") and "pc" in op):
                nxt = next_map.get(off)
                if nxt is not None:
                    stack.append(nxt)
    return max_addr


def detect_functions(d, md, regions):
    """Возвращает (funcs, fakes):
    funcs: [(fa, fb, region_name)] — fb = граница КОДА: максимум, достижимый
           из пролога в верифицированном окне (BFS: split-body/cold-пути/tbb);
           literal-пулы в fb НЕ входят (могут лежать за следующими функциями —
           слова печатаются отдельно по абсолютным offset'ам);
    fakes: [(fa, region_name)] — неподтверждённые кандидаты.

    Два прохода: (1) базовое окно до следующего кандидата; (2) расширение
    неподтверждённых — но НЕ дальше следующего подтверждённого в проходе 1
    (иначе ложный кандидат поглощает эпилог реальной функции => пересечения).
    Подтверждение идёт со skipdata=True: linear-декодирование иначе обрывается
    на literal-пулах с «невалидными» Thumb-байтами и пропускает эпилог."""
    md_sd = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
    md_sd.skipdata = True
    thunks = find_thunks(d, regions)
    N = len(d)
    funcs, fakes = [], []
    for a, b, name in regions:
        cands = [off for off in range(a, b, 2) if is_prologue(d, off)]

        # --- проход 1: базовое окно [кандидат, следующий кандидат) ---
        p1 = {}   # fa -> epi или None
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
                # --- проход 2: расширение, но не дальше следующего
                # подтверждённого кандидата (он — реальная функция, не наш хвост) ---
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
                if epi is None or epi[0] < 1:   # минимум пролог+>=1 instr
                    fakes.append((fa, name))
                    continue
            # граница = максимум, достижимый из пролога в окне (BFS);
            # literal-пулы не разыгрываются (ldr[pc] — не переход) и печатаются отдельно
            fb = reach_end(d, md_sd, fa, win_end, thunks)
            real.append((fa, fb))
        funcs.extend((fa, fb, name) for fa, fb in real)
    return funcs, fakes


def pc_lit_pools(d, insns, N):
    """По инструкциям ldr rX,[pc,#imm] -> множество offset'ов пулов в файле."""
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
    """Классификация 32-битного литерала -> (cls, extra)."""
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
    """Анализ кода функции + слов её пула.

    Возвращает (str_refs, lit_map, callees, lines).
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
            return f"-> данные образа @0x{extra:05x}"
        if cls == "peri":
            return "(периферия)"
        if cls == "ram":
            return "(RAM)"
        return ""

    for ins in code_insns:
        comment = []
        # данные внутри кода (skipdata): печатаем как есть
        if ins.mnemonic == "data":
            text = ".h " + " ".join(f"0x{x:02x}" for x in ins.bytes)
            lines.append((ins.address, text, ""))
            continue
        # ldr rX, [pc, #imm] (16-бит и 32-бит ldr.w; imm может быть отрицательным)
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
        # movw/movt (и 32-битные mov.w/movt.w) -> 32-битный адрес
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
                comment.append(f"-> 0x{toff:05x} (вне списка функций)")

        text = f"{ins.mnemonic} {ins.op_str}".strip()
        lines.append((ins.address, text, " ; ".join(comment)))

    # слова пула тоже считаются литералами функции
    for pool_off, v in pool_words:
        note_lit(f"пул @0x{pool_off:05x}", v)

    return str_refs, lit_map, callees, lines


def main():
    d = open(FW, "rb").read()
    N = len(d)
    strings = load_strings(d)

    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
    md.detail = True

    funcs, fakes = detect_functions(d, md, REGIONS)
    func_starts = {fa for fa, _, _ in funcs}
    print(f"[i] кандидатов по прологу: подтверждено {len(funcs)}, "
          f"ложных (данные): {len(fakes)}")

    # первый проход: дизассембл кода каждой функции ([fa, fb) — только код);
    # skipdata=True — чтобы декодирование не обрывалось на данных внутри функции.
    # Literal-пулы ОТДЕЛЕНЫ от границы: слова читаются по абсолютным offset'ам
    # (компилятор кладёт пулы далеко — даже за следующие функции).
    md_sd = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
    md_sd.skipdata = True
    code_of, pool_of = {}, {}
    for fa, fb, _ in funcs:
        full = list(md_sd.disasm(d[fa:fb], BASE + fa))
        code_of[fa] = full
        refs = sorted(pc_lit_pools(d, full, N))
        pool_of[fa] = [(p, struct.unpack_from("<I", d, p)[0]) for p in refs if p + 4 <= N]

    # xrefs: кто кого зовёт (bl и b) — только по кодовым частям
    callers = defaultdict(list)   # target_off -> [(src_func, addr, mn)]
    for fa, insns in code_of.items():
        for ins in insns:
            if ins.mnemonic in ("bl", "b") and ins.op_str.startswith("#"):
                toff = (int(ins.op_str[1:], 16) & ~1) - BASE
                if toff in func_starts:
                    callers[toff].append((fa, ins.address, ins.mnemonic))

    # разрешение пересечений: из двух пересекающихся подтверждённых кандидатов
    # остаётся тот, на кого есть входящий xref (реальная функция вызывается),
    # при равенстве — левый; проигравший -> в ложные
    kept, demoted = [], []
    for fa, fb, rname in sorted(funcs):
        xr = len(callers.get(fa, []))
        clash = None
        for k in range(len(kept)):
            ka, kb, kr = kept[k]
            if fa < kb and ka < fb:      # пересечение
                clash = k
                break
        if clash is None:
            kept.append((fa, fb, rname))
            continue
        ka, kb, kr = kept[clash]
        kxr = len(callers.get(ka, []))
        if xr > 0 and kxr == 0:          # новый вызывается, старый — нет: новый реальный
            kept[clash] = (fa, fb, rname)
            demoted.append((ka, kr))
        else:                            # иначе остаётся (левый/с xref'ом)
            demoted.append((fa, rname))
    if demoted:
        print(f"[i] разрешено пересечений (демоция в ложные): {len(demoted)}")
        fakes = fakes + demoted
        code_of = {fa: v for fa, v in code_of.items() if fa in {k[0] for k in kept}}
        pool_of = {fa: v for fa, v in pool_of.items() if fa in {k[0] for k in kept}}
        funcs = kept

    os.makedirs(OUT_DIR, exist_ok=True)
    # чистим старые md предыдущих прогонов (демоции/сдвиги границ иначе
    # оставляют «призрачные» файлы)
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
                call_lines.append(f"- 0x{tgt:08x} ({mn}, вне списка функций)")

        xref_lines = [f"- `{fname_of(src)}` ({mn} @0x{addr:08x})"
                      for src, addr, mn in sorted(callers.get(fa, []))]

        str_lines = [f'- `{src}`: 0x{v:08x} — "{t}"'
                     for src, v, t in sorted(set(str_refs), key=lambda x: (x[1], x[0]))] \
            or ["- (нет)"]

        lit_lines = []
        for v, (src, cls, extra) in sorted(lit_map.items()):
            if cls == "string":
                continue  # уже в разделе «Строки»
            if cls == "func":
                lit_lines.append(f"- 0x{v:08x} — `{fname_of(extra)}` ({src})")
            elif cls == "data":
                lit_lines.append(f"- 0x{v:08x} — данные образа @0x{extra:05x} ({src})")
            elif cls == "peri":
                lit_lines.append(f"- 0x{v:08x} — периферия ({src})")
            elif cls == "ram":
                lit_lines.append(f"- 0x{v:08x} — RAM ({src})")
            else:
                lit_lines.append(f"- 0x{v:08x} — прочее ({src})")

        asm_lines = [f"  {addr:08x}:  {text:<34}{comment}" for addr, text, comment in lines]
        # пулы группируются в последовательные прогоны; если прогон лежит за
        # границей функции (компилятор кладёт пулы далеко) — помечаем
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
            asm_lines.append(f"  ; --- literal-пул @0x{p0:05x} ({pn} слов)"
                             f"{' — ВНЕ границ функции' if outside else ''} ---")
            for p, v in run:
                cls, extra = classify(v, d, strings, func_starts)
                if cls == "string":
                    tag = f'"{strings[extra]}"'
                elif cls == "func":
                    tag = fname_of(extra)
                elif cls == "data":
                    tag = f"данные @0x{extra:05x}"
                elif cls == "peri":
                    tag = "периферия"
                elif cls == "ram":
                    tag = "RAM"
                else:
                    tag = ""
                asm_lines.append(f"  {p:05x}:  .word 0x{v:08x}{'  ; ' + tag if tag else ''}")

        content = f"""# {fname}

| | |
|---|---|
| offset в файле | `0x{fa:05x}` |
| vaddr (база 0x01800000) | `0x{BASE + fa:08x}` |
 | размер кода | {fb - fa} Б |
| регион | {rname} |

## Строки (ссылки через literal-пулы / movw+movt)

{chr(10).join(str_lines)}

## Литералы и адреса

{chr(10).join(lit_lines) if lit_lines else "- (нет)"}

## Вызовы (callees)

{chr(10).join(call_lines) if call_lines else "- (нет)"}

## Кто вызывает (callers / xrefs)

{chr(10).join(xref_lines) if xref_lines else "- (не найден в открытых регионах)"}

## Дизассембляция

```asm
{chr(10).join(asm_lines)}
```
"""
        with open(os.path.join(OUT_DIR, f"{fname}.md"), "w", encoding="utf-8") as f:
            f.write(content)

        top_str = "; ".join(dict.fromkeys(t for _, _, t in str_refs))[:60]
        index_rows.append((fa, fb - fa, rname, top_str, len(callers.get(fa, []))))

    # где лежат строки образа (для вывода в README)
    str_by_region = Counter()
    for off in strings:
        if 0x00400 <= off < 0x02a00:
            str_by_region["0x00400-0x02a00 (PLAIN bootloader)"] += 1
        elif 0x06000 <= off < 0x0a200:
            str_by_region["0x06000-0x0a200 (PLAIN flash/OTA)"] += 1
        elif 0x0a200 <= off < 0x25400:
            str_by_region["0x0a200-0x25400 (ENC APP)"] += 1
        else:
            str_by_region["прочее"] += 1

    # индекс
    idx = ["# Справочник по функциям BLE-образа (PLAIN-регионы)",
            "",
             f"Образ: `ble_2.7.0_0015.bin` ({N} Б), база флеша `0x{BASE:08x}`.",
              "Детекция (два прохода): пролог `push {..,lr}` / `push.w {..,lr}` (T4) + "
              "подтверждение эпилогом (`pop {..,pc}` / `bx lr` / «pop-lr»+b|bx — pop-lr = "
              "`pop {..,lr}` | `ldmfd sp!,{..,lr}` | `ldr lr,[sp]`; косвенный `bx rX`; "
              "`b` на трамплин — горячая цель >=3 или блок, начинающийся с эпилога; "
              "цепочки трамплинов разрешаются фиксированной точкой по реальным целям "
              "ветвлений). Проход 2 расширяет окно только через НЕподтверждённых кандидатов. "
              "Граница функции = максимум, достижимый из пролога в верифицированном окне "
              "(BFS: fallthrough + ветвления, в т.ч. tbb; bl/bx не разыгрываются) — "
              "захватывает split-body/cold-пути. «Размер кода» не включает literal-пулы: "
              "компилятор кладёт их далеко (вплоть до следующих функций), поэтому слова "
              "пулов печатаются таблицей по абсолютным offset'ам с пометкой «ВНЕ границ».",
             "",
            "> **Режим кода:** PLAIN-регионы — ЧИСТО Thumb (ARM-инструкций нет; "
            "паттерн `E92D` — это 32-битный T4 `push.w`, не ARM PUSH). Цели bl на "
            "`0x15xxxxxx`/`0x16xxxxxx`/`0x17xxxxxx` — runtime-RAM (код, скопированный "
            "в SRAM при старте), в файле образа их нет — md для них сгенерировать нельзя.",
           "",
           f"Подтверждено функций: **{len(funcs)}**; "
           f"ложных срабатываний на данных: {len(fakes)}.",
           "",
           "> **Вывод:** PLAIN-регионы — низкоуровневый код (bootloader + flash/OTA-драйвер): "
           "в коде функций НЕТ ни одной ссылки на строки — все ldr[pc]/movw-movt литералы "
           "это периферия (0x4xxxxxxx), RAM (0x2xxxxxxx / 0x002xxxxx) и внутренние адреса "
           "образа. «Строки», попадающиеся regex'ом в этих регионах, — шум случайных байтов "
           "(проверено выборкой). Настоящие строки и «говорящий» код — только в зашифрованном "
           "APP-регионе 0x0a200-0x25400 (расшифровывается только XIP/SWD, см. REPORT.md).",
           "",
           "Распределение «строк» по регионам (для справки; в PLAIN — шум):"]
    for k, v in str_by_region.most_common():
        idx.append(f"- {k}: {v}")
    idx += ["",
            "Перегенерация: `python research/scripts/gen_functions.py`.",
            "",
            "| offset | vaddr | размер | регион | строки | callers |",
            "|---|---|---|---|---|---|"]
    for fa, size, rname, top_str, ncall in index_rows:
        idx.append(f"| [`0x{fa:05x}`](func_0x{fa:05x}.md) | `0x{BASE + fa:08x}` | {size} | "
                   f"{rname.split(' (')[0]} | {top_str or '—'} | {ncall} |")
    idx += ["",
            "## Ложные срабатывания детектора (данные, не код)",
            ""]
    for fa, name in fakes:
        note = ""
        for a, b, _ in REGIONS:
            if a <= fa < b and b - fa < 0x60:
                note = (" — пролог у края PLAIN-региона: тело, вероятно, продолжается "
                        "в зашифрованной области (эпилог недостижим)")
        idx.append(f"- `0x{fa:05x}` ({name.split(' (')[0]}){note}")

    with open(os.path.join(OUT_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx) + "\n")

    n_str = sum(1 for r in index_rows if r[3])
    print(f"[+] функций: {len(funcs)}, со строками: {n_str} -> {OUT_DIR}")


if __name__ == "__main__":
    main()
