#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сессионный свип всех siid/piid самоката по BLE (только чтение).

Цели (TODO B-класс):
  1. Живые значения телеметрии/настроек (база для корреляций §34/§31).
  2. Найти app-триггер GET sub 0x2A (сид @0x871..@0x880, 16 Б) — кандидаты:
     SIID_6 LOG_1..LOG_5 и «сырые» blob-свойства (16/18/20 Б в ответе).
  3. Зафиксировать маппинг siid/piid -> содержимое (для siid/piid <-> CMD задачи).

Всё расшифрованное (plaintext ответов) дублируется в лог: logs/prop_sweep_<ts>.log

Запуск:  python probes/prop_sweep.py [--mac 2C:19:5C:DE:DE:88] [--no-logs]
"""
import argparse
import asyncio
import contextlib
import io
import os as _os
import sys as _sys
from datetime import datetime

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
_sys.path.insert(0, _os.path.join(_ROOT, "core"))
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import dreame_auth as da
import spec_read as sr


# Полный список свойств из плагина (modules/10724.js SIID_DIC) + SIID_5/SIID_6.
PROPS = (
    [(1, p) for p in range(1, 10)]
    + [(2, p) for p in range(1, 19)]
    + [(3, p) for p in range(1, 13)]
    + [(4, p) for p in list(range(1, 10)) + [10]]
    + [(5, p) for p in range(1, 35)]
    + [(6, p) for p in range(1, 6)]
)

# размеры, интересные для blob-субкоманд (§38.3): 0x2a=16Б сид, 0x28=18Б blob#1,
# 0x29=20Б blob#2, 0x22=7Б заголовок
BLOB_HINT = {7: "заголовок @0x844 (sub 0x22)?", 16: "СИД @0x871 (sub 0x2A)??",
             18: "blob#1 @0x84b (sub 0x28)??", 20: "blob#2 @0x85d (sub 0x29)??"}


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, s):
        for st in self.streams:
            try:
                st.write(s)
            except Exception:
                pass

    def flush(self):
        for st in self.streams:
            with contextlib.suppress(Exception):
                st.flush()


async def read_one(t, sk, obj, app_cnt, out):
    s, p = obj
    name = sr.NAMES.get(obj, "?")
    print(f"--- siid={s} piid={p} [{name}] (app_cnt={app_cnt})")
    pt = await sr.spec_request(t, sk, [obj], app_cnt)
    if pt is None:
        out.append(f"{s}.{p} {name}: НЕТ ОТВЕТА")
        return None, app_cnt + 1
    out.append(f"{s}.{p} {name}: {pt.hex()}")
    for line in sr.parse_reply(pt):
        print("   " + line)
        out.append("   " + line)
    # blob-детект: ищем value с «подозрительным» размером
    try:
        off = 6
        count = pt[5]
        for _ in range(count):
            if off + 5 > len(pt):
                break
            siid, piid, status = __import__("struct").unpack("<BHH", pt[off:off + 5])
            if status != 0:
                off += 5
                continue
            tl = __import__("struct").unpack_from("<H", pt, off + 5)[0]
            vlen = tl & 0x0FFF
            val = pt[off + 7: off + 7 + vlen]
            if vlen in BLOB_HINT:
                print(f"   >>> BLOB {vlen}Б: {BLOB_HINT[vlen]}  raw={val.hex()}")
                out.append(f"   >>> BLOB {vlen}Б: {BLOB_HINT[vlen]}  raw={val.hex()}")
            off += 7 + vlen
    except Exception as e:
        print(f"   [!] blob-скан: {e}")
    return pt, app_cnt + 1


async def run(mac):
    ltmk = bytes.fromhex(open(da.LTMK_HEX).read().strip())
    t = da.Transport(mac)
    try:
        await t.connect()
        if not await t.a4_handshake():
            print("[!] транспорт не поднялся")
            return 1
        for s, b in await t.drain(1.0):
            if s == da.CH_LOGIN and len(b) >= 3 and b[2] == da.PKT_MNG:
                await t.write(da.CH_LOGIN, __import__("struct").pack("<HBB", 0, da.PKT_MNG_ACK, 0)
                              + bytes([t.pkg_num, t.dmtu]))
        priv, dev_pub = await da.stage_a_pubkey_exchange(t)
        if not (dev_pub and len(dev_pub) >= 64):
            return 1
        if not await da.stage_b_confirm(t, priv, dev_pub, ltmk, crc_be=False):
            print("[!] login отказан")
            return 1
        sk = da.LAST_SK
        print("\n[+] LOGIN OK — старт свипа\n")

        out = []
        app_cnt = 0
        ok = 0
        for obj in PROPS:
            try:
                pt, app_cnt = await read_one(t, sk, obj, app_cnt, out)
                if pt is not None:
                    ok += 1
            except Exception as e:
                print(f"   [!] ошибка: {e}")
                out.append(f"{obj[0]}.{obj[1]}: ошибка {e}")
            await asyncio.sleep(0.15)
        print(f"\n=== свип завершён: ответов {ok}/{len(PROPS)} ===")
        return 0 if ok else 1
    except Exception:
        import traceback
        traceback.print_exc()
        return 1
    finally:
        await t.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mac", default=da.MAC_DEFAULT)
    ap.add_argument("--no-logs", action="store_true")
    a = ap.parse_args()

    log_path = None
    if not a.no_logs:
        _os.makedirs(_os.path.join(_ROOT, "logs"), exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = _os.path.join(_ROOT, "logs", f"prop_sweep_{ts}.log")
    buf = io.StringIO()
    _sys.stdout = Tee(_sys.__stdout__, buf)
    if log_path:
        fh = open(log_path, "w", encoding="utf-8")
        _sys.stdout = Tee(_sys.__stdout__, buf, fh)

    rc = asyncio.run(run(a.mac))
    _sys.stdout.flush()
    if log_path:
        fh.close()
        print(f"\n[лог: {log_path}]")
    raise SystemExit(rc)
