#!/usr/bin/env python3
"""
Распаковка React Native indexed RAM bundle (магия 0xFB0BD1E5) на отдельные JS-модули.

Формат:
    uint32 magic = 0xFB0BD1E5
    uint32 module_count
    uint32 startup_code_len
    module_count × {uint32 offset, uint32 length}   — таблица модулей
    startup code, затем тела модулей (offset отсчитывается от конца таблицы)
Пустые записи (offset=length=0) — дырки в нумерации модулей, это норма.

Запуск:  python tools/unpack_rambundle.py <main.bundle> <out-dir>
"""
import os
import struct
import sys

MAGIC = 0xFB0BD1E5


def unpack(path, out_dir):
    d = open(path, "rb").read()
    magic, count, startup_len = struct.unpack("<III", d[:12])
    if magic != MAGIC:
        print(f"не indexed RAM bundle: magic=0x{magic:08x}")
        return 1
    table_end = 12 + count * 8
    print(f"модулей в таблице: {count}   startup_code_len={startup_len}")
    print(f"таблица: 12..{table_end}   размер файла: {len(d)}")

    os.makedirs(out_dir, exist_ok=True)
    written = empty = bad = 0
    sizes = []
    for i in range(count):
        off, ln = struct.unpack("<II", d[12 + i * 8: 20 + i * 8])
        if off == 0 and ln == 0:
            empty += 1
            continue
        start = table_end + off
        body = d[start:start + ln]
        if not body:
            bad += 1
            continue
        body = body.rstrip(b"\x00")
        with open(os.path.join(out_dir, f"{i:05d}.js"), "wb") as f:
            f.write(body)
        written += 1
        sizes.append(len(body))

    print(f"записано: {written}   пустых записей: {empty}   битых: {bad}")
    if sizes:
        print(f"размеры модулей: min={min(sizes)} max={max(sizes)} "
              f"сумма={sum(sizes)}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(unpack(sys.argv[1], sys.argv[2]))
