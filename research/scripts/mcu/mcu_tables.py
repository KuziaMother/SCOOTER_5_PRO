#!/usr/bin/env python3
"""
Поиск калибровочных/lookup-таблиц в прошивке MCU (mcu_0007.bin).

Идея: у контроллера самоката пороги и кривые (температура, ток, скорость, дерейтинг)
лежат таблицами констант. Их видно как длинные МОНОТОННЫЕ последовательности u16/i16 —
в отличие от кода, где значения идут вразнобой.

Найдено этим способом (см. REPORT.md): блок таблиц около 0x17f80–0x18010, включая
температурную ось -10..50 °C и оси 0..10000 (шаг 500) и 0..800 (шаг 100).

Запуск:  python research/scripts/mcu/mcu_tables.py [--min-len 6] [--bin <mcu_0007.bin>]
"""
import argparse
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(os.path.dirname(HERE))   # research/


def read_u16(d, i, signed=False):
    return struct.unpack_from("<h" if signed else "<H", d, i)[0]


def find_runs(d, min_len=6, signed=False):
    """Монотонные (строго возрастающие) последовательности u16/i16."""
    runs = []
    i = 0
    n = len(d) - 2
    while i < n:
        j = i
        vals = [read_u16(d, j, signed)]
        while j + 4 <= len(d):
            nxt = read_u16(d, j + 2, signed)
            if nxt <= vals[-1]:
                break
            vals.append(nxt)
            j += 2
        if len(vals) >= min_len:
            runs.append((i, vals))
            i = j + 2
        else:
            i += 2
    return runs


def classify(vals):
    """Короткая характеристика ряда: постоянный шаг? похоже на что?"""
    diffs = [b - a for a, b in zip(vals, vals[1:])]
    uniform = len(set(diffs)) == 1
    tags = []
    if uniform:
        tags.append(f"равномерный шаг {diffs[0]}")
    else:
        tags.append(f"шаги {min(diffs)}..{max(diffs)}")
    lo, hi = vals[0], vals[-1]
    if lo >= -40 and hi <= 130 and len(vals) <= 16:
        tags.append("МОЖЕТ БЫТЬ температура °C")
    if hi <= 100 and lo >= 0:
        tags.append("МОЖЕТ БЫТЬ проценты")
    if 3000 <= hi <= 60000 and lo >= 0:
        tags.append("мВ / мА / об-мин?")
    return "; ".join(tags)


def dump_battery_curves(d, start=0x18036, lo=2500, hi=4400, drop=50):
    """Сегментация блока кривых напряжения ячейки: границу видно по резкому падению."""
    curves, cur, off, cstart = [], [], start, start
    while off + 2 <= len(d):
        v = struct.unpack_from("<H", d, off)[0]
        if not (lo <= v <= hi):
            break
        if cur and v < cur[-1] - drop:
            curves.append((cstart, cur))
            cur, cstart = [], off
        cur.append(v)
        off += 2
    if cur:
        curves.append((cstart, cur))
    print(f"\n=== блок кривых напряжения ячейки: 0x{start:05x}..0x{off:05x} "
          f"({off - start} Б), кривых {len(curves)} ===")
    prev = None
    for i, (o, v) in enumerate(curves):
        mark = "   <-- новая группа" if prev is not None and v[-1] > prev + 80 else ""
        prev = v[-1]
        print(f"  #{i:>2} @0x{o:05x} n={len(v):>2}  {v[0]:>4}..{v[-1]:>4} мВ{mark}")
    return curves


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin", default=os.path.join(RES, "images", "mcu_0007.bin"))
    ap.add_argument("--min-len", type=int, default=6)
    ap.add_argument("--no-curves", action="store_true",
                    help="не печатать разбор блока кривых напряжения")
    a = ap.parse_args()

    d = open(a.bin, "rb").read()
    print(f"=== {os.path.basename(a.bin)}: {len(d)} Б, монотонные ряды >= {a.min_len} ===\n")

    seen = set()
    total = 0
    for signed in (False, True):
        for off, vals in find_runs(d, a.min_len, signed):
            # не печатать один и тот же регион дважды (unsigned/signed)
            key = (off // 2, len(vals))
            if key in seen:
                continue
            seen.add(key)
            # отсечь мусор: ряды внутри кода часто «почти случайны» — требуем,
            # чтобы либо шаг был равномерным, либо ряд был длинным
            diffs = [b - a2 for a2, b in zip(vals, vals[1:])]
            if len(set(diffs)) > 1 and len(vals) < a.min_len + 3:
                continue
            total += 1
            kind = "i16" if signed else "u16"
            print(f"@0x{off:05x} [{kind}] {len(vals)} знач.: {vals[:14]}"
                  f"{' …' if len(vals) > 14 else ''}")
            print(f"           {classify(vals)}")
    print(f"\nвсего рядов: {total}")
    if not a.no_curves:
        dump_battery_curves(d)


if __name__ == "__main__":
    raise SystemExit(main())
