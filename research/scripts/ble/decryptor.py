#!/usr/bin/env python3
"""
Попытка расшифровать зашифрованный APP-регион BLE-прошивки (RTL8762C) без SWD-дампа
OTP. См. docs/FACTS.md: `xip=1, enc=1, enc_key_select=7` -> ключ хранится в OTP, штатно
расшифровывается только аппаратно (XIP) -> из .bin программно НЕ восстановим БЕЗ ключа.
Это статически последний шанс: попробовать публично известные/дефолтные ключи демо-SDK.

Регион (docs/FACTS.md): ENC = 0x0a200..0x25400 (111104 Б), IV-кандидат = заголовок
байты [0x0c:0x1c] (16 Б, см. research/analyze_crypto.py).

Кандидаты ключей:
  * `OTA_AES_KEY` из rtl8762c-gcc-examples/config/oem_config.c — 32 Б плейсхолдер
    демо-конфига SDK (00 01 02 ... 1F), НЕ обязательно совпадает с ключом Dreame
    (BT_MAC там тоже плейсхолдер aa:bb:cc:dd:ee:ff) — но это единственный
    задокументированный "дефолтный OTA-ключ RTL8762x", доступный статически.
    Пробуем как AES-128 (первые 16 Б) и как AES-256 (все 32 Б).
  * all-zero / all-0xff — типовые "забыли сконфигурировать" дефолты.

Режимы: CBC и CTR (в CTR используем IV-кандидат как nonce||counter=0, посчитанный
как big-endian 128-бит счётчик, т.к. точный формат счётчика RTL8762x XIP неизвестен).

Проверка результата — ЭВРИСТИКИ, не доказательство:
  * энтропия (низкая = похоже на код/данные, ~8.0 = всё ещё шифртекст/мусор);
  * доля Thumb-правдоподобных 16-бит инструкций (align, топ-биты частых опкодов);
  * читаемые ASCII-строки длиннее 6 симв.
Если ни один кандидат не даёт распознаваемый результат — вывод отрицательный и
ожидаемый: ключ в OTP, статически недостижим (нужен SWD-дамп, см. todo.md §B).
"""
import collections
import math
import os
import struct
import sys

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

IMG = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ble_2.7.0_0015.bin")
FW = sys.argv[1] if len(sys.argv) > 1 else IMG
ENC = (0x0A200, 0x25400)

OEM_CONFIG_KEY32 = bytes(range(0x00, 0x20))  # oem_config.c OTA_AES_KEY (демо-плейсхолдер)

CANDIDATE_KEYS = {
    "oem_config_aes128 (первые 16Б OTA_AES_KEY)": OEM_CONFIG_KEY32[:16],
    "oem_config_aes256 (все 32Б OTA_AES_KEY)": OEM_CONFIG_KEY32,
    "zero128": bytes(16),
    "zero256": bytes(32),
    "ff128": bytes([0xFF] * 16),
    "ff256": bytes([0xFF] * 32),
}


def entropy(b):
    if not b:
        return 0.0
    c = collections.Counter(b)
    n = len(b)
    return -sum((x / n) * math.log2(x / n) for x in c.values())


def ascii_strings(b, min_len=8):
    out, cur = [], bytearray()
    for byte in b:
        if 32 <= byte < 127:
            cur.append(byte)
        else:
            if len(cur) >= min_len:
                out.append(bytes(cur).decode())
            cur = bytearray()
    if len(cur) >= min_len:
        out.append(bytes(cur).decode())
    return out


def thumb_plausibility(b):
    """Грубая эвристика: доля 16-бит халфвордов, похожих на частые Thumb-опкоды
    (push/pop/mov/bl-верхняя half и т.п. по старшим битам). НЕ дизассемблер."""
    if len(b) < 2:
        return 0.0
    n = len(b) // 2
    hits = 0
    for i in range(0, n * 2, 2):
        hw = struct.unpack_from("<H", b, i)[0]
        top5 = hw >> 11
        # частые Thumb16 префиксы: 000xx(shift) 010001(hi-reg) 0100(alu) 1011(misc/push-pop)
        # 11100(uncond b) 1101(cond b) 10110/10111(push/pop) — проверяем верхние 5 бит грубо
        if top5 in (0b00000, 0b00001, 0b00010, 0b10110, 0b10111, 0b11100, 0b01000, 0b01001):
            hits += 1
    return hits / n


def try_one(name, key, data, iv):
    results = []
    for mode_name in ("CBC", "CTR"):
        try:
            if mode_name == "CBC":
                if len(data) % 16 != 0:
                    continue
                cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            else:
                cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
            dec = cipher.decryptor()
            pt = dec.update(data) + dec.finalize()
        except Exception as e:
            results.append((mode_name, None, str(e)))
            continue
        results.append((mode_name, pt, None))
    return results


def main():
    d = open(FW, "rb").read()
    enc = d[ENC[0]:ENC[1]]
    iv = d[0x0C:0x1C]

    # Калибровка эвристик: известный ПЛЕЙНТЕКСТ-регион кода (0x6000..0xa200, из
    # analyze_crypto.py) как позитивный baseline и сам шифртекст (без расшифровки)
    # как отрицательный контроль — иначе пороги "на глаз" ловят случайные ASCII-
    # подстроки в шуме (проверено: без калибровки ЛОЖНО флагуются ВСЕ кандидаты).
    plain_sample = d[0x6000:0x6000 + 4096]
    plain_strs = len(ascii_strings(d[0x6000:0x6000 + 65536]))
    plain_e = entropy(plain_sample)
    plain_plaus = thumb_plausibility(plain_sample)
    neg_e = entropy(enc[:4096])
    neg_strs = len(ascii_strings(enc[:65536]))
    neg_plaus = thumb_plausibility(enc[:4096])

    print(f"[decryptor] файл={FW}  enc-регион=0x{ENC[0]:x}..0x{ENC[1]:x} ({len(enc)} Б)")
    print(f"[decryptor] IV-кандидат (header[0x0c:0x1c]) = {iv.hex()}")
    print(f"[decryptor] калибровка: plaintext-код(0x6000) энтропия={plain_e:.3f} "
          f"Thumb={plain_plaus:.2f} строк={plain_strs}  |  "
          f"raw-шифртекст энтропия={neg_e:.3f} Thumb={neg_plaus:.2f} строк={neg_strs}\n")

    # Порог: заметно ближе к plaintext-профилю, чем к шифртекстовому.
    e_thresh = (plain_e + neg_e) / 2
    strs_thresh = max(plain_strs * 0.3, neg_strs * 3)

    best = []
    for name, key in CANDIDATE_KEYS.items():
        for mode_name, pt, err in try_one(name, key, enc, iv):
            if err:
                print(f"  [{name:45}] {mode_name}: ошибка ({err})")
                continue
            e = entropy(pt[:4096])
            strs = ascii_strings(pt[:65536])
            plaus = thumb_plausibility(pt[:4096])
            flag = "  <-- похоже на плейнтекст?" if (e < e_thresh and len(strs) > strs_thresh) else ""
            print(f"  [{name:45}] {mode_name}: энтропия={e:.3f}  Thumb={plaus:.2f}  "
                  f"строк(>=8)={len(strs)}{flag}")
            best.append((e, plaus, name, mode_name))

    best.sort(key=lambda x: (x[0], -x[1]))
    print("\n[decryptor] лучший кандидат по минимальной энтропии:",
          best[0][2], best[0][3], f"энтропия={best[0][0]:.3f}" if best else "(нет)")
    print(f"[decryptor] порог отсечки: энтропия<{e_thresh:.3f} И строк>{strs_thresh:.0f}")
    print("[decryptor] если ни один кандидат не помечен '<-- похоже на плейнтекст?' —")
    print("            результат ОТРИЦАТЕЛЬНЫЙ: ключ в OTP, статически не восстановим")
    print("            (см. todo.md §B — нужен SWD-дамп XIP-региона).")


if __name__ == "__main__":
    main()
