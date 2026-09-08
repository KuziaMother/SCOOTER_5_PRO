"""emu_coverage.py — пофункционный first-pass эмуляции MCU (TODO: закрыть 678 функций).

Для каждой НЕПОКРЫТОЙ @t-тестом функции из functions_mcu/README.md:
  - гоняем на нулевом RAM с R0-R3=0 (и парой паттернов аргументов),
  - ловим: чистый возврат (pop{pc}/bx lr -> LR-sentinel) vs fetch-error/timeout,
  - I/O-отпечаток: кол-во RAM-чтений/записей, затронутые periph-адреса.

Диспозиция (first-pass эвристика):
  clean   — возврат без ошибок, мало I/O  -> кандидат на @t-тест
  io      — чистый возврат, но много RAM/periph I/O -> нужен managed setup
  dirty   — fetch-error/timeout на нулевом RAM -> stateful/live/boot-blocked (нужен ручной анализ)

Результат: CSV/MD-таблица + work-queue. Обновляем по мере добавления @t-тестов.

Запуск:  python -X utf8 emu_coverage.py [--max-size N] [--min-size N] [--limit K]
"""
import sys, os, re, argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'emulator')))
from mcu_emu import McuEmu, RAM, FLASH0, FLASH1, STACK_TOP, PERIPH2  # noqa: E402
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UcError  # noqa: E402
from unicorn.arm_const import (UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_R0,  # noqa: E402
                               UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)

HERE = os.path.dirname(os.path.abspath(__file__))
README = os.path.join(HERE, '..', '..', 'functions_mcu', 'README.md')
FV = os.path.join(HERE, 'func_verify.py')
ROW = re.compile(r'^\|\s*\[\`?0x([0-9a-fA-F]+)\`?\]\([^)]*\)\s*\|\s*(\d+)\s*\|')


def load_funcs():
    out = []
    for line in open(README, encoding='utf-8'):
        m = ROW.match(line.strip())
        if m:
            out.append((int(m.group(1), 16), int(m.group(2))))
    return out


def load_tested():
    src = open(FV, encoding='utf-8').read()
    return sorted(set(int(x, 16) for x in re.findall(r'@t\(0x([0-9a-fA-F]+)', src)))


def run_func(off, size, max_insn=8000):
    """Один прогон функции на нулевом RAM. -> dict(clean, insn, rds, wrs, periph)."""
    emu = McuEmu(max_insn=max_insn)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))
    emu.hook_periph_ready()
    rds = [0]
    wrs = [0]
    periph = set()

    def _rd(uc_, acc, a, s, v, u):
        if RAM <= a < RAM + 0x20000:
            rds[0] += 1

    def _wr(uc_, acc, a, s, v, u):
        if RAM <= a < RAM + 0x20000:
            wrs[0] += 1
        elif (0x40000000 <= a < 0x40080000) or (PERIPH2 <= a < PERIPH2 + 0x20000):
            periph.add(a)

    uc.hook_add(UC_HOOK_MEM_READ, _rd)
    uc.hook_add(UC_HOOK_MEM_WRITE, _wr)
    clean = [False]

    def _st(uc_, a, s, u):
        aa = a & ~1
        if not (FLASH0 <= aa < FLASH0 + 0x23680 or FLASH1 <= aa < FLASH1 + 0x23680):
            clean[0] = True  # вышли во внешний адрес = возврат в LR-sentinel
            uc_.emu_stop()

    sh = uc.hook_add(UC_HOOK_CODE, _st)
    try:
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x40)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R0, 0)
        uc.reg_write(UC_ARM_REG_R1, 0)
        uc.reg_write(UC_ARM_REG_R2, 0)
        uc.reg_write(UC_ARM_REG_R3, 0)
        emu.insn = 0
        try:
            uc.emu_start(off | 1, 0, count=max_insn)
            # дошли до конца окна без stop-hook -> вероятно, не вернулась (dirty)
            clean[0] = False
        except UcError:
            pass  # fetch-error / unmap = dirty (если clean уже True — это возврат)
    finally:
        uc.hook_del(sh)
    return {'clean': bool(clean[0]), 'insn': emu.insn, 'rds': rds[0],
            'wrs': wrs[0], 'periph': sorted(periph)}


def disposition(res):
    if not res['clean']:
        return 'dirty'
    if res['periph'] or res['wrs'] > 32:
        return 'io'
    return 'clean'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-size', type=int, default=0)
    ap.add_argument('--min-size', type=int, default=0)
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--max-insn', type=int, default=8000)
    ap.add_argument('--out', default=os.path.join(HERE, 'emu_coverage.csv'))
    args = ap.parse_args()

    funcs = load_funcs()
    tested = load_tested()
    todo = [(o, s) for (o, s) in funcs
            if not any(o <= t < o + s for t in tested)
            and (args.min_size == 0 or s >= args.min_size)
            and (args.max_size == 0 or s <= args.max_size)]
    todo.sort()
    if args.limit:
        todo = todo[:args.limit]

    print(f'покрыто @t: {len(tested)}; в работе (фильтр): {len(todo)}')
    rows = []
    for i, (off, size) in enumerate(todo):
        res = run_func(off, size, max_insn=args.max_insn)
        disp = disposition(res)
        rows.append((off, size, disp, res['insn'], res['rds'], res['wrs'],
                     ','.join(hex(p) for p in res['periph'][:4])))
        print(f'  [{i+1}/{len(todo)}] 0x{off:05x} {size:5d}B -> {disp:6s} '
              f'(insn={res["insn"]} rd={res["rds"]} wr={res["wrs"]} periph={len(res["periph"])})')

    # сохранить (дополнить существующий CSV, если есть)
    import csv
    existing = []
    if os.path.exists(args.out):
        with open(args.out, encoding='utf-8-sig', newline='') as f:
            rd = csv.DictReader(f)
            for r in rd:
                existing.append(r)
    seen = {int(r['off'], 16) for r in existing}
    all_rows = existing + [{'off': f'0x{o:05x}', 'size': str(s), 'disp': d,
                            'insn': str(ins), 'rds': str(rds), 'wrs': str(wrs),
                            'periph': per} for (o, s, d, ins, rds, wrs, per) in rows
                           if o not in seen]
    with open(args.out, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['off', 'size', 'disp', 'insn', 'rds', 'wrs', 'periph'])
        w.writeheader()
        for r in all_rows:
            w.writerow(r)
    print(f'\nсохранено -> {args.out} (всего строк: {len(all_rows)})')

    from collections import Counter
    c = Counter(d for (_, _, d, _, _, _, _) in rows)
    print('итог батча:', dict(c))


if __name__ == '__main__':
    main()
