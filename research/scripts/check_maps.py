# -*- coding: utf-8 -*-
"""Проверка целостности таблиц MCU_MAP.md / BLE_MAP.md:
- ровно N колонок в каждой строке функции (с учётом экранированных \\|)
- размер — число, статус/% согласованы.
Запуск: python -X utf8 scripts/check_maps.py
"""
import os
import sys

RES = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def split_row(line):
    """разбивка строки markdown-таблицы на ячейки с учётом \\|"""
    cells, cur, i = [], '', 0
    while i < len(line):
        c = line[i]
        if c == '\\' and i + 1 < len(line) and line[i + 1] == '|':
            cur += '|'
            i += 2
            continue
        if c == '|':
            cells.append(cur)
            cur = ''
            i += 1
            continue
        cur += c
        i += 1
    return [c.strip() for c in cells]


def main():
    # fname → (кол-во колонок, индекс размера)
    layouts = [('MCU_MAP.md', 7, 1), ('BLE_MAP.md', 8, 2)]
    issues = []
    for fname, expect, size_idx in layouts:
        path = os.path.join(RES, fname)
        n_rows = 0
        for i, l in enumerate(open(path, encoding='utf-8'), 1):
            if not l.startswith('| [`0x'):
                continue
            n_rows += 1
            cells = split_row(l.rstrip('\n'))
            if cells and cells[0] == '':   # ведущий '|' даёт пустую ячейку
                cells = cells[1:]
            if len(cells) != expect:
                issues.append((fname, i, 'колонок %d (ждём %d)' % (len(cells), expect), l[:120]))
                continue
            size = cells[size_idx]
            st, pct = cells[-2], cells[-1]
            if not size.isdigit():
                issues.append((fname, i, 'size=%r' % size, l[:120]))
            want = {'не начат': '0%', 'ID': '25%', 'частично': '50%', 'разобран': '100%'}.get(st)
            if pct != want:
                issues.append((fname, i, 'status/pct несовместимы: %s/%s' % (st, pct), l[:120]))
        print('%s: строк функций %d' % (fname, n_rows))
    print('проблем:', len(issues))
    for f, i, why, l in issues[:20]:
        print('  %s L%d: %s\n    %s' % (f, i, why, l))
    return 1 if issues else 0


if __name__ == '__main__':
    sys.exit(main())
