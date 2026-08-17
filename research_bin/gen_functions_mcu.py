#!/usr/bin/env python3
"""
Справочник по функциям MCU-образа mcu_0007.bin (Dreame/Xiaomi Scooter 5 Pro,
контроллер мотора на Cortex-M4F, GD32/STM32F1-class, HAL; НЕ зашифрован).

Генерирует research_bin/functions_mcu/*.md — по одному файлу на ПОДТВЕРЖДЁННУЮ
функцию:
    - метаданные (offset = vaddr при базе 0x0; зеркало флеша 0x08000000,
      RAM 0x20000000, периферия 0x40000000, SYS 0xE0000000);
    - строки, на которые функция ссылается (ldr [pc] / movw+movt) — в этом
      образе их почти нет (контроллер без логирования);
    - все литералы (периферия, RAM, SYS, адреса в образе, mirror 0x08000000);
    - callees (bl/b) и callers (xrefs из всех функций);
    - дизассембляция (capstone, Thumb) с построчными аннотациями;
      literal-пулы печатаются таблицей слов.

База: файл загружается эмулятором по 0x00000000 (и зеркалу 0x08000000),
т.е. vaddr == offset в файле. Векторной таблицы в OTA-образе нет
(REPORT.md §MCU): образ = только APP-регион, код начинается с 0x01200.

Детекция (три источника стартов + подтверждение эпилогом):
  1. пролог `push {..,lr}` (B5xx, бит7 reglist = lr) — 503 шт.;
  2. пролог `push.w {..,lr}` (T4, первый halfword 0xE92D; верифицирован
     capstone'ом) — 93 шт. (функции, которые эвристика B5xx пропускала);
  3. цели `bl`/`blx`, НЕ лежащие внутри подтверждённой функции из 1–2 —
     функции без push-пролога (маленькие leaf'ы, ISR): каждая подтверждается
     собственным эпилогом в окне до следующей подтверждённой функции.
  Подтверждение/границы — как в gen_functions.py (BLE):
    - эпилог: pop{..,pc} | bx lr | «pop-lr»+b|bx rX | bx rX/ip/fp/sl |
      b/b.w на трамплин (горячая цель >=3 / блок с эпилогом / цепочки);
    - два прохода окон (базовое до следующего кандидата; расширение
      неподтверждённых — не дальше следующего подтверждённого);
    - граница fb = BFS-максимум, достижимый из пролога в верифицированном
      окне (split-body/cold-пути); literal-пулы в fb не входят (печатаются
      таблицей по абсолютным offset'ам, могут лежать за следующими функциями);
    - пересечения разрешаются по входящим xref (вызываемый остаётся).
  Глобальный сбор целей ветвлений идёт ПОБАЙТНЫМ сканом + capstone-верификация
  каждой инструкции на месте (последовательный декод регионов в этом образе
  десинхронизируется на данных — sequential-сбор целей ненадёжен).

Формула literal-пула: ((addr+4) & ~3) + imm — проверена эмпирически: 97.8%
резолвлённых слов пулов попадают в правдоподобные классы (RAM/peri/sys/img),
альтернатива (addr+4)+imm — только 46%.

Запуск:  $env:PYTHONIOENCODING="utf-8"; python gen_functions_mcu.py
"""
import glob
import os
import re
import struct
from collections import defaultdict
from collections import Counter

from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN

HERE = os.path.dirname(os.path.abspath(__file__))
FW = os.path.join(HERE, "mcu_0007.bin")
OUT_DIR = os.path.join(HERE, "functions_mcu")

BASE = 0x0                 # vaddr == offset (эмулятор: flash @0x0 и mirror @0x08000000)
MIRROR = 0x08000000        # зеркало флеша: часть литералов ссылается на код/данные через него
REGIONS = [
    (0x01200, 0x02400, "код A"),
    (0x02600, 0x10200, "код B (FLASH-OTA: 0x06230/0x06304)"),
    (0x10400, 0x10e00, "код C"),
    (0x11000, 0x12400, "код D (0x11894 tbb-машина, 0x11cb4 OTA-init)"),
    (0x12800, 0x13e00, "код E (UART init/драйвер: 0x12d90/0x1302c)"),
    (0x14200, 0x14400, "код F"),
    (0x14600, 0x17a00, "код G"),
    (0x18e00, 0x19200, "код H"),
    (0x19a00, 0x24200, "код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, "
                       "HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, "
                       "ADC 0x1a31c/0x1e298)"),
    (0x24400, 0x24600, "код J"),
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
    """offset -> текст (ASCII-строки >=4 символа)."""
    return {m.start(): m.group().decode("ascii", "ignore")
            for m in re.finditer(rb"[ -~]{4,}", d)}


# --------------------------------------------------------------------------
# старты функций
# --------------------------------------------------------------------------

def find_prologues(d, md):
    """Возвращает (b5, t32): offset'ы push {..,lr} и push.w {..,lr}."""
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
    """'op_str' capstone'а для b/bl -> Thumb-адрес (vaddr) или None.

    Capstone пишет '#0x...' и для отрицательных смещений — sign-extended
    32-битное значение (0xfffff8de); сворачиваем в диапазон образа."""
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
    """Все цели bl/blx в коде (побайтовый скан + capstone на месте).

    Возвращает (targets_in_code, all_targets) — vaddr'ы."""
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
    """Все цели b/b.w (16- и 32-бит) в коде — для детекции трамплинов."""
    cnt = Counter()
    i16 = {}
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
# трамплины / эпилоги / границы (логика та же, что в gen_functions.py BLE)
# --------------------------------------------------------------------------

def _block_starts(d, md, t):
    """Первые инструкции блока по vaddr t (или [] если вне файла)."""
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
    """Адреса-«трамплины», на которые b/b.w = валидный эпилог (горячие цели
    >=3, блок с эпилогом, цепочки через фиксированную точку)."""
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
    """Первый валидный эпилог: (i_start, j_end, kind) или None."""
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
    """Максимальный offset, достижимый из fa в пределах [fa, win_end) (BFS)."""
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
        # ВАЖНО: bx НЕ ветвление по потоку (bx lr / bx rX — возврат/tail-call):
        # иначе BFS просачивается за эпилог в пулы/следующую функцию.
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
    """Подтверждение кандидата fa: базовое окно [fa, limit), затем расширение
    до min(stop, +0x400) — но НЕ дальше следующего подтверждённого (stop).
    Возвращает fb или None."""
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
    """Возвращает (funcs, fakes): funcs=[(fa, fb, region)], fakes=[(fa, kind)].

    Тир 1: прологи (B5xx ∪ push.w) — два прохода окон, как в BLE-версии.
    Тир 2: цели bl вне подтверждённых тир-1 — подтверждаются своим эпилогом
    в окне до следующей подтверждённой функции."""
    md_sd = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
    md_sd.skipdata = True
    thunks = find_thunks(d, md)
    N = len(d)

    b5, t32 = find_prologues(d, md)
    bl_in, _ = find_call_targets(d, md)

    # --- тир 1: прологи ---
    cands = sorted((b5 | t32))
    # группировка по регионам (окна не пересекают границы регионов)
    by_region = defaultdict(list)
    for fa in cands:
        if in_code(fa):
            by_region[region_name(fa)].append(fa)

    funcs, fakes = [], []
    confirmed_spans = []     # [(fa, fb)] — для тир-2 и stop-правил
    for _, _, name in REGIONS:
        rc = by_region.get(name, [])
        if not rc:
            continue
        a, b = next((x, y) for x, y, n in REGIONS if n == name)
        # проход 1: базовое окно до следующего кандидата
        p1 = {}
        for i, fa in enumerate(rc):
            limit = rc[i + 1] if i + 1 < len(rc) else b
            fb = confirm_in_window(d, md_sd, fa, limit, b, thunks)
            p1[fa] = fb
        confirmed1 = {fa for fa, fb in p1.items() if fb is not None}
        # проход 2 (расширение) уже внутри confirm_in_window через stop:
        # для неподтверждённых — stop = следующий подтверждённый кандидат
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
                fakes.append((fa, "пролог"))
            else:
                real.append((fa, fb))
        for fa, fb in real:
            funcs.append((fa, fb, name))
            confirmed_spans.append((fa, fb))

    # --- тир 2: цели bl вне подтверждённых функций ---
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
        # stop = следующая подтверждённая функция после t (в том же регионе)
        stop = b
        for fa, fb in confirmed_spans:
            if fa > t and a <= fa < b:
                stop = fa
                break
        limit = b  # тир-2: окно до края региона (расширение ограничено stop)
        fb = confirm_in_window(d, md_sd, t, limit, stop, thunks)
        if fb is None:
            fakes.append((t, "цель bl"))
        else:
            funcs.append((t, fb, name))
            confirmed_spans.append((t, fb))

    return funcs, fakes, thunks


# Мнемоники ветвлений capstone (ARM/Thumb). ВАЖНО: нельзя использовать
# startswith("b") — ложные друзья bfi/bic/bics/bkpt тоже начинаются на "b".
UNCOND_BR = {"b", "b.w"}
COND_BR = {"beq", "bne", "bge", "bgt", "bgt.w", "bhi", "bhs", "ble", "blo",
           "bls", "blt", "blt.w", "bmi", "bpl", "bvc", "bvs", "cbz", "cbnz"}


def writes_pc(mn, op):
    """Инструкция записывает в PC => возврат/переход, дальше по fall-through
    идти нельзя (иначе BFS «провалится» в trailing literal-пул).
      - bx rX / bx lr
      - ldr pc, [..]  / mov pc, rX / add|sub pc, ..  (pc = ПЕРВЫЙ операнд)
      - pop {.., pc}
    Важно: `ldr r0, [pc, #imm]` НЕ возврат (pc — база в скобках, не dest)."""
    if mn == "bx":
        return True
    if mn in ("pop", "pop.w"):
        return "pc" in op
    first = op.split(",")[0].strip()
    return first == "pc"


def find_internal_blocks(insns, fa, fb):
    """Карта внутренних блоков функции: цели b/b.w/b.cond/cbz/cbnz внутри
    [fa, fb), на которые НЕТ обратных ссылок (заголовки циклов исключаются —
    их источники лежат выше цели). Показывает внутренние dispatch-ветви
    (например, case-блоки RX-парсера 0x1e9e0, вызываемые через `b` в общем
    фрейме) как отдельный навигационный список.

    Возвращает [(t, end)] — t = старт блока, end = следующий блок или fb."""
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
    """Множество адресов инструкций, реально достижимых от входа функции.

    Прямой BFS: вход fa -> fall-through + цели ветвлений. Правила:
      - обычная инст. / data  -> fall-through (следующий адрес);
      - безусловный b          -> только цель (fall-through мёртв);
      - условный b.* / cbz/cbnz -> и цель, и fall-through;
       - bl / blx              -> только fall-through (возврат из вызова);
       - запись в PC           -> терминально (bx / ldr pc,[..] / pop {..,pc} /
                                   mov|add|sub pc,..): дальше по fall-through не идём,
                                   иначе BFS провалится в trailing literal-пул.
    Цели вне [fa, fb) отбрасываются (это другие функции).

    Зачем: настоящий literal-пул НЕВОЗМОЖНО пересечь с достижимым кодом —
    в данные не переходят. Если кандидат пула ложится на достижимую
    инструкцию/цель ветвления, это код, а не пул (ложное срабатывание ldr).
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
            # безусловный: fall-through не жив
        elif mn in COND_BR:
            if ins.op_str.startswith("#"):
                stack.append(int(ins.op_str[1:], 16) & ~1)
            stack.append(nxt)          # условный: и цель, и fall-through
        elif mn in ("bl", "blx"):
            stack.append(nxt)          # вызов возвращается
        elif writes_pc(mn, ins.op_str.strip()):
            pass                        # return (ldr pc / pop {pc} / mov pc / bx) — терминально
        else:
            stack.append(nxt)
    return reach


def pool_overlaps_code(p, words, reach, size_of):
    """True, если пул из `words` слов @p пересекает хоть одну достижимую инст.

    Пересечение по точным размерам: инст. [a, a+size) против пула [p, p+4w)."""
    lo, hi = p, p + 4 * words
    for a in reach:
        s = size_of.get(a, 2)
        if a < hi and (a + s) > lo:
            return True
    return False


# --------------------------------------------------------------------------
# литералы / пулы / анализ
# --------------------------------------------------------------------------

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
    """Классификация 32-битного литерала -> (cls, extra).

    Classes: string | func | data | data-mirror | peri | ram | sys | other.
    """
    N = len(d)
    # зеркало флеша 0x08000000: ссылка на код/данные образа через mirror-базу
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
        return f"данные @0x{extra:05x}"
    if cls == "data-mirror":
        return f"flash-mirror @0x{extra:05x}"
    if cls == "peri":
        return "периферия"
    if cls == "ram":
        return "RAM"
    if cls == "sys":
        return "Cortex-M (NVIC/SCB/SysTick)"
    return ""


def analyze_function(d, strings, func_starts, code_insns, pool_words, valid_pools=None):
    """Анализ кода функции + слов её пула. Возвращает (str_refs, lit_map,
    callees, lines). valid_pools — множество offset'ов ПРОВЕРЕННЫХ пулов; если
    задано, литерал ldr[pc] аннотируется только когда его пул не отфильтрован
    как ложный (пересечение с достижимым кодом)."""
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
                comment.append(f"-> 0x{toff:05x} (вне списка функций)")

        text = f"{ins.mnemonic} {ins.op_str}".strip()
        lines.append((ins.address, text, " ; ".join(comment)))

    for pool_off, v in pool_words:
        note_lit(f"пул @0x{pool_off:05x}", v)

    return str_refs, lit_map, callees, lines


def main():
    d = open(FW, "rb").read()
    N = len(d)
    strings = load_strings(d)

    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
    md.detail = True

    funcs, fakes, thunks = detect_functions(d, md)
    func_starts = {fa for fa, _, _ in funcs}
    print(f"[i] функций подтверждено: {len(funcs)}; "
          f"ложных кандидатов: {len(fakes)}; трамплинов: {len(thunks)}")

    # разрешение пересечений (xref-демоция) — как в BLE-версии
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
        print(f"[i] разрешено пересечений (демоция): {len(demoted)}")
        fakes = fakes + [(a, "демоция(пересечение)") for a, _ in demoted]
        keep_set = {k[0] for k in kept}
        code_of = {fa: v for fa, v in code_of.items() if fa in keep_set}
        funcs = kept

    # literal-пулы: вычисляем после демоции и ОТБРАСЫВАЕМ ложные — те, что
    # пересекаются с достижимым кодом (в данные не переходят; пул на месте
    # живых инструкций/целей ветвления = мёртвый/недокодированный ldr).
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
        print(f"[i] подавлено ложных пулов (пересечение с достижимым кодом): {n_suppr}")

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
                call_lines.append(f"- 0x{toff:05x} ({mn}, вне списка функций)")
            else:
                call_lines.append(f"- 0x{tgt:08x} ({mn}, вне образа — runtime/внешний)")

        xref_lines = [f"- `{fname_of(src)}` ({mn} @0x{addr:08x})"
                      for src, addr, mn in sorted(callers.get(fa, []))]

        blocks = find_internal_blocks(code_of[fa], fa, fb)
        block_lines = []
        if len(blocks) >= 3:
            for t, end, src_list in blocks:
                srcs_txt = ", ".join(f"0x{s:05x}" for s in src_list[:4]) \
                    + ("…" if len(src_list) > 4 else "")
                block_lines.append(f"- `0x{t:05x}..0x{end:05x}` ({end - t} Б); "
                                   f"цели из: {srcs_txt}")

        str_lines = [f'- `{src}`: 0x{v:08x} — "{t}"'
                     for src, v, t in sorted(set(str_refs), key=lambda x: (x[1], x[0]))] \
            or ["- (нет)"]

        lit_lines = []
        for v, (src, cls, extra) in sorted(lit_map.items()):
            if cls == "string":
                continue
            tag = _lit_tag(cls, extra, strings)
            lit_lines.append(f"- 0x{v:08x} — {tag} ({src})" if tag
                             else f"- 0x{v:08x} — прочее ({src})")

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
            asm_lines.append(f"  ; --- literal-пул @0x{p0:05x} ({pn} слов)"
                             f"{' — ВНЕ границ функции' if outside else ''} ---")
            for p, v in run:
                cls, extra = classify(v, d, strings, func_starts)
                tag = _lit_tag(cls, extra, strings)
                asm_lines.append(f"  {p:05x}:  .word 0x{v:08x}{'  ; ' + tag if tag else ''}")

        content = f"""# {fname}

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800{fa:05x}) | `0x{fa:08x}` |
| размер кода | {fb - fa} Б |
| регион | {rname} |

## Строки (ссылки через literal-пулы / movw+movt)

{chr(10).join(str_lines)}

## Литералы и адреса

{chr(10).join(lit_lines) if lit_lines else "- (нет)"}

## Вызовы (callees)

{chr(10).join(call_lines) if call_lines else "- (нет)"}

## Кто вызывает (callers / xrefs)

{chr(10).join(xref_lines) if xref_lines else "- (не найден в коде образа)"}
{chr(10) + chr(10) + "## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)" + chr(10) + chr(10) + chr(10).join(block_lines) if block_lines else ""}

## Дизассембляция

```asm
{chr(10).join(asm_lines)}
```
"""
        with open(os.path.join(OUT_DIR, f"{fname}.md"), "w", encoding="utf-8") as f:
            f.write(content)

        top_str = "; ".join(dict.fromkeys(t for _, _, t in str_refs))[:60]
        index_rows.append((fa, fb - fa, rname, top_str, len(callers.get(fa, []))))

    # индекс
    idx = ["# Справочник по функциям MCU-образа (mcu_0007.bin)",
           "",
           f"Образ: `mcu_0007.bin` ({N} Б) — контроллер мотора самоката, "
           "**Cortex-M4F** (GD32/STM32F1-class), HAL, **не зашифрован** "
           "(Mijia-подпись в хвосте). Векторной таблицы нет (только APP-регион OTA).",
           "",
           "**Карта памяти:** флеш @ `0x00000000` (зеркало `0x08000000` — часть "
           f"литералов ссылается через mirror: {sum(1 for v in set(w for fl in pool_of.values() for _, w in fl) if MIRROR <= v < MIRROR + N)} слов пулов), "
           "RAM @ `0x20000000` (128 КБ), периферия @ `0x40000000`, SYS @ `0xE0000000`. "
           "vaddr == offset в файле.",
           "",
           "**Детекция:** старты = пролог `push {..,lr}` (B5xx) ∪ `push.w {..,lr}` (T4, "
           "capstone-верифицирован) ∪ цели `bl` вне подтверждённых функций (no-prologue "
           "leaf'ы/ISR). Подтверждение эпилогом (`pop {..,pc}` / `bx lr` / «pop-lr»+b|bx / "
           "`bx rX` tail-call / `b` на трамплин — горячая цель >=3, блок с эпилогом, цепочки; "
           "трамплины собираются побайтовым сканом + capstone, т.к. sequential-декод регионов "
           "десинхронизируется). Граница = BFS-максимум в верифицированном окне (split-body/"
           "cold-пути); literal-пулы в границу не входят (могут лежать за следующими функциями — "
           "печатаются таблицей с пометкой «ВНЕ границ»). Пересечения разрешаются по входящим xref.",
           "",
           f"Подтверждено функций: **{len(funcs)}**; "
           f"ложных кандидатов: {len(fakes)}; трамплинов: {len(thunks)}.",
           "",
           "> **Строк в образе почти нет** (контроллер без логирования) — понимание функций "
           "идёт через литералы (периферия/RAM), xref и ручной трассирование. Известные якоря: "
           "USART3-протокол ↔ BLE `0x1e480`/`0x1e9e0`/`0x1f600`/`0x1f6b4`, HAL_UART_Transmit "
           "`0x23188`, FLASH-OTA `0x06230`, ADC `0x1a31c`, мотор TIM1 `0x22a48`–`0x22fac`.",
           "",
           "Регионы (code-секции; промежутки — данные/таблицы):"]
    for a, b, n in REGIONS:
        idx.append(f"- `0x{a:05x}–0x{b:05x}` ({b - a} Б) — {n}")
    idx += ["",
            "Перегенерация: `$env:PYTHONIOENCODING=\"utf-8\"; python gen_functions_mcu.py`.",
            "",
            "| offset | размер | регион | строки | callers |",
            "|---|---|---|---|---|"]
    for fa, size, rname, top_str, ncall in index_rows:
        idx.append(f"| [`0x{fa:05x}`](func_0x{fa:05x}.md) | {size} | "
                   f"{rname.split(' (')[0]} | {top_str or '—'} | {ncall} |")
    if fakes:
        idx += ["",
                "## Ложные кандидаты (данные/ярлыки, не функции)",
                ""]
        for fa, kind in fakes[:100]:
            idx.append(f"- `0x{fa:05x}` ({kind}, {region_name(fa)})")
        if len(fakes) > 100:
            idx.append(f"- … ещё {len(fakes) - 100}")

    with open(os.path.join(OUT_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx) + "\n")

    n_str = sum(1 for r in index_rows if r[3])
    print(f"[+] функций: {len(funcs)}, со строками: {n_str} -> {OUT_DIR}")


if __name__ == "__main__":
    main()
