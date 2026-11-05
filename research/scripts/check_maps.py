# -*- coding: utf-8 -*-
"""Integrity check of MCU_MAP.md / BLE_MAP.md tables:
- exactly N columns in each function row (handling escaped \\|)
- size is numeric, status/% are consistent.
Run: python -X utf8 scripts/check_maps.py
"""
import os
import sys

RES = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def split_row(line):
    """Split markdown table row into cells handling \\|"""
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
    # fname -> (number of columns, size column index)
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
            if cells and cells[0] == '':   # leading '|' produces empty cell
                cells = cells[1:]
            if len(cells) != expect:
                issues.append((fname, i, 'got %d columns (expected %d)' % (len(cells), expect), l[:120]))
                continue
            size = cells[size_idx]
            st, pct = cells[-2], cells[-1]
            if not size.isdigit():
                issues.append((fname, i, 'size=%r' % size, l[:120]))
            want = {
                '\u043d\u0435 \u043d\u0430\u0447\u0430\u0442': '0%',
                'ID': '25%',
                '\u0447\u0430\u0441\u0442\u0438\u0447\u043d\u043e': '50%',
                '\u0440\u0430\u0437\u043e\u0431\u0440\u0430\u043d': '100%',
                'not started': '0%',
                'partially': '50%',
                'partial': '50%',
                'analyzed': '100%',
            }.get(st)
            if pct != want:
                issues.append((fname, i, 'incompatible status/pct: %s/%s' % (st, pct), l[:120]))
        print('%s: function rows %d' % (fname, n_rows))
    print('issues:', len(issues))
    for f, i, why, l in issues[:20]:
        print('  %s L%d: %s\n    %s' % (f, i, why, l))
    return 1 if issues else 0


if __name__ == '__main__':
    sys.exit(main())
