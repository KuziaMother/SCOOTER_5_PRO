#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Живой захват пушей свойств (TODO B «Живой пуш-захват», §18).

Сценарий в одной сессии (Mi Home параллельно НЕ нужен — BLE single-connection):
  1. connect + login
  2. baseline: 2.4 TAIL_LIGHT, 2.2 IS_LOCKED, 1.1 RIDING_MODE
  3. SET 2.4=1 (хвостовой свет ВКЛ)  -> ждём пуш
  4. SET 2.4=0 (свет ВЫКЛ)           -> ждём пуш
  5. (опц. --lock) SET 2.2=1/0       -> пуш IS_LOCKED

Все уведомления 0x001b расшифровываются и логируются: logs/push_capture_<ts>.log

SET-формат (docs/BLE.md §6): op=0, элемент [u8 siid][u16 piid][u16 (type<<12)|vlen][value].
ОТКРЫТОСТЬ: только свет/замок — штатные управляемые свойства, ничего деструктивного.

Запуск:  python probes/push_capture.py [--no-light] [--lock] [--hold 5]
"""
import argparse
import asyncio
import contextlib
import io
import os as _os
import struct
import sys as _sys
from datetime import datetime

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
_sys.path.insert(0, _os.path.join(_ROOT, "core"))
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import dreame_auth as da
import spec_read as sr

CH_WRITE = 0x001A
CH_NOTIFY = 0x001B


def build_set(obj, value, vtype, tid=2):
    """SET-кадр: op=0, один элемент с value."""
    s, p = obj
    body = struct.pack("<BHH", s & 0xFF, p & 0xFFFF, (vtype & 0xF) << 12 | len(value)) + value
    total = 6 + len(body)
    return struct.pack("<HHBB", (total | 0x2000) & 0xFFFF, tid & 0xFFFF, 0, 1) + body


class PushWatcher:
    """Расшифровывает и печатает ВСЕ уведомления 0x001b из очереди транспорта."""

    def __init__(self, t, sk):
        self.t = t
        self.sk = sk
        self.count = 0

    async def run(self, timeout):
        loop = asyncio.get_event_loop()
        deadline = loop.time() + timeout
        while loop.time() < deadline:
            try:
                s, b = await asyncio.wait_for(self.t.rx.get(), timeout=deadline - loop.time())
            except asyncio.TimeoutError:
                break
            if s != CH_NOTIFY:
                continue
            pt = self._try_decode(b)
            if pt is None:
                print(f"  [notify {s:#06x}] нерасшифровано/транспорт: {b[:12].hex()}")
                continue
            self.count += 1
            tag = f"PUSH #{self.count}"
            print(f"  >>> {tag}: {pt.hex()}")
            for line in sr.parse_reply(pt):
                print("      " + line)
        return self.count

    def _try_decode(self, b):
        # транспорт: [u16 counter] + CCM-шифр (dev key) — как в ответе на GET
        if len(b) < 6:
            return None
        try:
            cnt = struct.unpack("<H", b[:2])[0]
            return sr.dec_dev(self.sk, cnt, b[2:])
        except Exception:
            # может быть транспортный ACK/CTR — не наш формат
            return None


async def do_read(t, sk, obj, app_cnt):
    pt = await sr.spec_request(t, sk, [obj], app_cnt)
    if pt:
        for line in sr.parse_reply(pt):
            print("   " + line)
    return app_cnt + 1


async def do_set(t, sk, obj, value, vtype, app_cnt):
    name = sr.NAMES.get(obj, f"{obj[0]}.{obj[1]}")
    print(f"=== SET {name} = {value} (app_cnt={app_cnt}) ===")
    payload = sr.enc_app(sk, app_cnt, build_set(obj, value, vtype))
    frames = [payload[i:i + 18] for i in range(0, len(payload), 18)] or [b""]
    while not t.rx.empty():
        t.rx.get_nowait()
    await t.write(CH_WRITE, struct.pack("<HBBH", 0, 0x00, 0, len(frames)))

    async def send_seq(n):
        if 1 <= n <= len(frames):
            await t.write(CH_WRITE, struct.pack("<H", n) + frames[n - 1])

    loop = asyncio.get_event_loop()
    deadline = loop.time() + 6.0
    sent_all = False
    while loop.time() < deadline:
        try:
            s, b = await asyncio.wait_for(t.rx.get(), timeout=deadline - loop.time())
        except asyncio.TimeoutError:
            break
        if len(b) >= 3 and b[0] == 0 and b[1] == 0 and b[2] == 0x01:
            st = b[3] if len(b) > 3 else None
            if st == 0x01 and not sent_all:
                sent_all = True
                for n in range(1, len(frames) + 1):
                    await send_seq(n)
                    await asyncio.sleep(0.03)
            elif st == 0x05:
                seqs = [struct.unpack_from("<H", b, 4 + i)[0]
                        for i in range(0, len(b) - 4, 2)]
                for n in seqs:
                    await send_seq(n)
                    await asyncio.sleep(0.03)
            elif st == 0x00:
                print("   запрос принят (ACK 00), ждём ответ устройства...")
                # ответ по CTR-потоку на CH_NOTIFY (как в spec_request)
                rdl = loop.time() + 6.0
                got_ctr = False
                while loop.time() < rdl:
                    try:
                        s2, b2 = await asyncio.wait_for(t.rx.get(),
                                                        timeout=rdl - loop.time())
                    except asyncio.TimeoutError:
                        break
                    if (s2 == CH_NOTIFY and len(b2) >= 6 and b2[0] == 0 and b2[1] == 0
                            and b2[2] == 0 and not got_ctr):
                        fc = struct.unpack("<H", b2[4:6])[0]
                        await t.write(CH_NOTIFY, struct.pack("<HBB", 0, 0x01, 0x01))
                        parts = {}
                        while len(parts) < fc and loop.time() < rdl:
                            try:
                                s3, b3 = await asyncio.wait_for(t.rx.get(),
                                                                timeout=rdl - loop.time())
                            except asyncio.TimeoutError:
                                break
                            if s3 == CH_NOTIFY and len(b3) >= 2:
                                seq = struct.unpack("<H", b3[:2])[0]
                                if 1 <= seq <= fc:
                                    parts[seq] = b3[2:]
                        await t.write(CH_NOTIFY, struct.pack("<HBB", 0, 0x01, 0x00))
                        if len(parts) == fc:
                            payload = b"".join(parts[i] for i in sorted(parts))
                            dev_cnt = struct.unpack("<H", payload[:2])[0]
                            try:
                                pt = sr.dec_dev(sk, dev_cnt, payload[2:])
                                print(f"   ОТВЕТ НА SET: {pt.hex()}")
                                for line in sr.parse_reply(pt):
                                    print("     " + line)
                            except Exception as e:
                                print(f"   [!] ответ не расшифровался: {e}")
                        break
                    # прочие кадры (опоздавшие ACK) — игнорируем
                return app_cnt + 1
    print("   [!] ACK на SET не получен")
    return app_cnt + 1


async def run(mac, do_light=True, do_lock=False, hold=5):
    ltmk = bytes.fromhex(open(da.LTMK_HEX).read().strip())
    t = da.Transport(mac)
    try:
        await t.connect()
        if not await t.a4_handshake():
            print("[!] транспорт не поднялся")
            return 1
        for s, b in await t.drain(1.0):
            if s == da.CH_LOGIN and len(b) >= 3 and b[2] == da.PKT_MNG:
                await t.write(da.CH_LOGIN, struct.pack("<HBB", 0, da.PKT_MNG_ACK, 0)
                              + bytes([t.pkg_num, t.dmtu]))
        priv, dev_pub = await da.stage_a_pubkey_exchange(t)
        if not (dev_pub and len(dev_pub) >= 64):
            return 1
        if not await da.stage_b_confirm(t, priv, dev_pub, ltmk, crc_be=False):
            print("[!] login отказан")
            return 1
        sk = da.LAST_SK
        print("\n[+] LOGIN OK\n")

        w = PushWatcher(t, sk)
        app_cnt = 0

        print("=== BASELINE ===")
        for obj in ((2, 4), (2, 2), (1, 1)):
            app_cnt = await do_read(t, sk, obj, app_cnt)
            await asyncio.sleep(0.2)

        async def set_and_watch(obj, value, label):
            nonlocal app_cnt
            app_cnt = await do_set(t, sk, obj, value, 0, app_cnt)
            print(f"   окно {hold}с на пуш после: {label}")
            await asyncio.sleep(1.0)
            await w.run(hold)

        if do_light:
            print("\n=== СЦЕНАРИЙ: хвостовой свет (2.4 — вне пуш-списка) ===")
            await set_and_watch((2, 4), b"\x01", "свет ВКЛ")
            await set_and_watch((2, 4), b"\x00", "свет ВЫКЛ")

        print("\n=== СЦЕНАРИЙ: ATMOSPHERE_LIGHT (2.16 — в пуш-списке) ===")
        await set_and_watch((2, 16), b"\x01", "atmo ВКЛ")
        await set_and_watch((2, 16), b"\x00", "atmo ВЫКЛ")

        print("\n=== СЦЕНАРИЙ: TCS (2.13 — в пуш-списке) ===")
        # baseline 2.13 был = 1; переключаем и обратно
        await set_and_watch((2, 13), b"\x00", "TCS ВЫКЛ")
        await set_and_watch((2, 13), b"\x01", "TCS ВКЛ")

        if do_lock:
            print("\n=== СЦЕНАРИЙ: замок ===")
            await set_and_watch((2, 2), b"\x01", "ЗАМОК ВКЛ")
            await set_and_watch((2, 2), b"\x00", "РАЗБЛОКИРОВКА")

        print(f"\n=== пушей записано: {w.count} ===")
        return 0 if w.count else 1
    except Exception:
        import traceback
        traceback.print_exc()
        return 1
    finally:
        await t.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mac", default=da.MAC_DEFAULT)
    ap.add_argument("--no-light", action="store_true")
    ap.add_argument("--lock", action="store_true")
    ap.add_argument("--hold", type=int, default=5)
    a = ap.parse_args()

    _os.makedirs(_os.path.join(_ROOT, "logs"), exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = _os.path.join(_ROOT, "logs", f"push_capture_{ts}.log")
    buf = io.StringIO()

    class Tee:
        def __init__(self, *ss):
            self.ss = ss

        def write(self, s):
            for st in self.ss:
                with contextlib.suppress(Exception):
                    st.write(s)

        def flush(self):
            for st in self.ss:
                with contextlib.suppress(Exception):
                    st.flush()

    fh = open(log_path, "w", encoding="utf-8")
    _sys.stdout = Tee(_sys.__stdout__, buf, fh)
    rc = asyncio.run(run(a.mac, do_light=not a.no_light, do_lock=a.lock, hold=a.hold))
    _sys.stdout.flush()
    fh.close()
    print(f"\n[лог: {log_path}]")
    raise SystemExit(rc)
