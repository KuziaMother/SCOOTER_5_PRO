#!/usr/bin/env python3
"""
Пассивное прослушивание после логина: ищем телеметрию (батарея/скорость/пробег).

Read-only: ничего не пишем в устройство, кроме обязательного login-хендшейка.
Всё пойманное на 0x001a/0x001b/0x0016 пробуем расшифровать сессионным ключом.

Раскладка sessionKey (40 Б, схема Mijia):
    [0:16] dev_key   (device -> app)   [16:32] app_key (app -> device)
    [32:36] dev_iv                     [36:40] app_iv

Запуск:  python telemetry_listen.py [--secs 40]
"""
import argparse
import asyncio
import struct

import os as _os, sys as _sys
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
_sys.path.insert(0, _os.path.join(_ROOT, "core"))

import dreame_auth as da
from cryptography.hazmat.primitives.ciphers.aead import AESCCM


def try_decrypt(sk: bytes, blob: bytes, direction: str = "dev"):
    """Перебор counter'ов и раскладок кадра для CCM-расшифровки."""
    key = sk[0:16] if direction == "dev" else sk[16:32]
    iv = sk[32:36] if direction == "dev" else sk[36:40]
    ccm = AESCCM(key, tag_length=4)
    out = []
    # кандидаты: (полезная часть, счётчик) при разных вариантах хвоста кадра
    variants = []
    if len(blob) >= 4:
        # counter в конце (2 Б) — стандарт mible: [ct][mac4]... либо [ct+mac4][cnt2]
        variants.append(("cnt2-tail", blob[:-2], int.from_bytes(blob[-2:], "little")))
    variants.append(("cnt-brute", blob, None))
    for tag, body, cnt in variants:
        counters = [cnt] if cnt is not None else range(0, 64)
        for c in counters:
            nonce = iv + b"\x00\x00\x00\x00" + struct.pack("<I", c)
            try:
                pt = ccm.decrypt(nonce, body, None)
            except Exception:
                continue
            out.append((tag, c, pt))
    return out


def annotate(pt: bytes) -> str:
    hints = []
    if all(32 <= b < 127 for b in pt) and pt:
        hints.append(f"ascii='{pt.decode()}'")
    for i, b in enumerate(pt):
        if 1 <= b <= 100:
            hints.append(f"[{i}]={b}(?%)")
    for i in range(0, max(0, len(pt) - 1)):
        w = int.from_bytes(pt[i:i + 2], "little")
        if 3000 <= w <= 4300:
            hints.append(f"[{i}:2]={w}(?мВ)")
        elif 30000 <= w <= 45000:
            hints.append(f"[{i}:2]={w}(?мВ пакета)")
    return "  ".join(hints[:12])


async def run(mac: str, secs: float):
    ltmk = bytes.fromhex(open(da.LTMK_HEX).read().strip())
    t = da.Transport(mac)
    try:
        await t.connect()
        if not await t.a4_handshake():
            print("[!] транспорт не поднялся")
            return 1
        for s, b in await t.drain(1.0):
            if s == da.CH_LOGIN and len(b) >= 3 and b[2] == da.PKT_MNG:
                await t.write(da.CH_LOGIN,
                              struct.pack("<HBB", 0, da.PKT_MNG_ACK, 0)
                              + bytes([t.pkg_num, t.dmtu]))

        print("\n=== Stage A ===")
        priv, dev_pub = await da.stage_a_pubkey_exchange(t)
        if not (dev_pub and len(dev_pub) >= 64):
            return 1
        print("\n=== Stage B ===")
        ok = await da.stage_b_confirm(t, priv, dev_pub, ltmk, crc_be=False)
        if not ok:
            print("[!] login отказан")
            return 1
        sk = da.LAST_SK
        print(f"\n[+] LOGIN OK. sessionKey {len(sk)}Б, dev_key[:4]={sk[0:4].hex()} "
              f"dev_iv={sk[32:36].hex()} app_iv={sk[36:40].hex()}")

        print(f"\n=== пассивное прослушивание {secs:.0f} с (самокат должен быть ВКЛЮЧЁН) ===")
        print("    покрути колесо / пожми ручку — ищем меняющиеся байты\n")
        seen = []
        deadline = asyncio.get_event_loop().time() + secs
        while asyncio.get_event_loop().time() < deadline:
            try:
                s, b = await asyncio.wait_for(t.rx.get(), timeout=1.0)
            except asyncio.TimeoutError:
                continue
            seen.append((s, b))

        print(f"\n=== поймано {len(seen)} нотификаций ===")
        if not seen:
            print("тишина: устройство само телеметрию не пушит — нужен запрос.")
        by_ch = {}
        for s, b in seen:
            by_ch.setdefault(s, []).append(b)
        for s, blobs in sorted(by_ch.items()):
            print(f"\n--- 0x{s:04x}: {len(blobs)} кадров ---")
            for b in blobs[:20]:
                print(f"  {b.hex()}")
            if s in (0x001A, 0x001B):
                for b in blobs[:8]:
                    for tag, c, pt in try_decrypt(sk, b, "dev"):
                        print(f"  [DECRYPT {tag} cnt={c}] {pt.hex()}  {annotate(pt)}")
        return 0
    except Exception:
        import traceback
        traceback.print_exc()
        return 1
    finally:
        await t.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mac", default=da.MAC_DEFAULT)
    ap.add_argument("--secs", type=float, default=40.0)
    a = ap.parse_args()
    raise SystemExit(asyncio.run(run(a.mac, a.secs)))
