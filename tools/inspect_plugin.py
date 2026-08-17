#!/usr/bin/env python3
"""
Разбор скачанного бандла плагина Mi Home: что внутри и есть ли логика телеметрии.

Плагин бывает двух видов:
  * RN-бандл (JS) — читается, это удачный случай;
  * нативный .so — придётся дизассемблировать (или путь опять упирается).

Скрипт: распаковывает архив, классифицирует содержимое и ищет следы приватного
протокола — обращения к BLE-характеристикам, каналам, опкодам, батарее.

Запуск:  python tools/inspect_plugin.py <файл-бандла> [--extract-dir DIR]
"""
import argparse
import os
import re
import zipfile

# что ищем в текстовых/бинарных ресурсах
PATTERNS = [
    (rb"0000fe95|fe95", "UUID сервиса FE95"),
    (rb"0000001[0-9a-f]-0000-1000", "UUID характеристики Mijia"),
    (rb"battery|batteryLevel|soc|remainCapacity", "БАТАРЕЯ"),
    (rb"mileage|odometer|totalMileage|speed|rpm", "ПРОБЕГ/СКОРОСТЬ"),
    (rb"securitychipauth|securityChip", "security-chip login"),
    (rb"writeCharacteristic|readCharacteristic|notifyChar", "BLE-операции"),
    (rb"spec_?value|siid|piid|miotSpec", "MIoT spec"),
    (rb"55\s*aa|0x55AA|P4v2", "серийный протокол 55AA/P4"),
    (rb"channel|Channel", "канальный транспорт"),
    (rb"opcode|opCode|cmdId|command_id", "опкоды/команды"),
]

TEXTY = (".js", ".jsx", ".json", ".bundle", ".txt", ".xml", ".html", ".ts", ".map")


def classify(names):
    kinds = {"RN/JS": [], "нативные .so": [], "ресурсы": [], "прочее": []}
    for n in names:
        low = n.lower()
        if low.endswith((".js", ".jsx", ".bundle", ".map", ".ts")):
            kinds["RN/JS"].append(n)
        elif low.endswith(".so"):
            kinds["нативные .so"].append(n)
        elif low.endswith((".png", ".jpg", ".webp", ".gif", ".ttf", ".json", ".xml")):
            kinds["ресурсы"].append(n)
        else:
            kinds["прочее"].append(n)
    return kinds


def scan_blob(data, label, out):
    for pat, name in PATTERNS:
        hits = list(re.finditer(pat, data, re.I))
        if hits:
            out.setdefault(name, []).append((label, len(hits), hits[0].start()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bundle")
    ap.add_argument("--extract-dir", default=None)
    a = ap.parse_args()

    if not zipfile.is_zipfile(a.bundle):
        size = os.path.getsize(a.bundle)
        head = open(a.bundle, "rb").read(64)
        print(f"НЕ zip-архив ({size} Б). Первые байты: {head[:32].hex()}")
        print("Возможно, это одиночный JS-бандл или зашифрованный контейнер.")
        data = open(a.bundle, "rb").read()
        found = {}
        scan_blob(data, os.path.basename(a.bundle), found)
        for k, v in found.items():
            print(f"  [{k}] {v}")
        return 0

    zf = zipfile.ZipFile(a.bundle)
    names = zf.namelist()
    print(f"=== {a.bundle}: {len(names)} записей ===\n")
    for kind, items in classify(names).items():
        print(f"{kind}: {len(items)}")
        for n in items[:15]:
            info = zf.getinfo(n)
            print(f"   {n}  ({info.file_size} Б)")
        if len(items) > 15:
            print(f"   ... ещё {len(items) - 15}")
        print()

    print("=== поиск следов протокола ===")
    found = {}
    for n in names:
        info = zf.getinfo(n)
        if info.file_size > 40 * 1024 * 1024:
            continue
        try:
            data = zf.read(n)
        except Exception:
            continue
        scan_blob(data, n, found)
    if not found:
        print("ничего из искомого не найдено")
    for name, hits in sorted(found.items()):
        print(f"\n[{name}]")
        for label, cnt, pos in hits[:8]:
            print(f"   {label}: {cnt} совпад. (первое @{pos})")

    if a.extract_dir:
        os.makedirs(a.extract_dir, exist_ok=True)
        zf.extractall(a.extract_dir)
        print(f"\nраспаковано в {a.extract_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
