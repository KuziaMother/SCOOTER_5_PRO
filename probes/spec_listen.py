#!/usr/bin/env python3
"""
Слушатель пуш-уведомлений об изменении свойств (MIoT-spec поверх BLE).

Подписка УЖЕ есть: `Transport.connect()` сам ставит CCCD на ВСЕ notify-характеристики
FE95, включая spec-notify `0x001b`. Доказано на том же пути — `spec_read.py` успешно
принимает ОТВЕТЫ на `0x001b` через эту подписку. Пуш идёт тем же notify-путём `0x001b`,
только БЕЗ предшествующего запроса на `0x001a`. (Плагин дополнительно вызывает
`bt.subscribeMessages("prop.s.p", …)` — это лишь локальная маршрутизация JS-колбэков по
темам, а НЕ отдельная команда устройству; см. FACTS.md «Устройство умеет ПУШИТЬ».)

⚠️ Пуш приходит ТОЛЬКО при ИЗМЕНЕНИИ свойства. На стоящем самокате с полным зарядом
меняться нечему — поэтому «тишина» сама по себе ничего не опровергает. Чтобы увидеть
трафик, надо что-то менять: пожать ручку газа, включить/выключить свет, покатить самокат.

Формат кадров от устройства — ТОТ ЖЕ, что ответ на чтение (spec_read.py):
  одиночный:    [0000][02][00][counter u16 LE][ct]   -> ACK [0000][03][00]
  многокадровый:[0000][00][ch][fc]  -> мы ACK 01 -> кадры [seq u16][data] -> мы ACK 00
Дешифровка: key=sk[0:16], iv=sk[32:36] (ключи устройства), AES-CCM, tag 4 Б.

ТОЛЬКО ЧТЕНИЕ: ничего не пишем, кроме обязательных ACK транспорта и (опц.) baseline-чтения.

Порядок прогона:
  connect -> login -> [baseline: DEFAULT_SET как «до изменений», по одному свойству]
             -> pre-roll отсчёт -> окно прослушивания (меняй состояние!) -> итог.

Запуск:
  python probes/spec_listen.py [--secs 120] [--pre 5] [--no-baseline] [--log ПУТЬ]
Всё, что печатается (включая логин), дублируется в лог-файл (по умолчанию docs/).
"""
import argparse
import asyncio
import contextlib
import os as _os
import struct
import sys as _sys
from datetime import datetime

_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import dreame_auth as da
import spec_read as sr

CH_WRITE = 0x001A
CH_NOTIFY = 0x001B

# Свойства, на которые плагин подписывается (modules/10013.js parseNotifyData):
# 1.1 1.2 1.4 1.5 1.6 1.7 1.8 1.9 2.1 2.7 2.13-2.18 3.1 3.2 3.4 3.10.
# Пуш ожидается только по ним; прочее в notify помечаем как «вне списка».
SUBSCRIBABLE = {
    (1, 1), (1, 2), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
    (2, 1), (2, 7), (2, 13), (2, 14), (2, 15), (2, 16), (2, 17), (2, 18),
    (3, 1), (3, 2), (3, 4), (3, 10),
}


class _Tee:
    """Дублирует вывод в консоль и в лог-файл."""
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
            try:
                st.flush()
            except Exception:
                pass


def parse_props(pt):
    """Разбор spec-кадра: заголовок + объекты [siid][piid][status][tl][value]."""
    out = []
    if len(pt) < 6:
        return [("?", "?", None, f"короткий кадр {pt.hex()}")]
    lenflag, tid, op, count = struct.unpack("<HHBB", pt[:6])
    off = 6
    for _ in range(count):
        if off + 7 > len(pt):
            break
        siid, piid, status, tl = struct.unpack("<BHHH", pt[off:off + 7])
        tcode, vlen = tl >> 12, tl & 0x0FFF
        val = pt[off + 7: off + 7 + vlen]
        off += 7 + vlen
        out.append((siid, piid, tcode, val, status))
    return out, op


async def read_baseline(t, sk):
    """«До изменений»-снапшот в той же сессии (CCCD уже стоит, один логин).
    Устройство обслуживает только ПЕРВЫЙ объект запроса => читаем по одному,
    счётчик app растёт. Только чтение."""
    print("\n=== БАЗА (значения ДО изменений) ===")
    got = 0
    for i, (s, p) in enumerate(sr.DEFAULT_SET):
        name = sr.NAMES.get((s, p), "?")
        pt = await sr.spec_request(t, sk, [(s, p)], app_cnt=i)
        if not pt:
            print(f"  {name}: [нет ответа]")
            continue
        for line in sr.parse_reply(pt):
            print("  " + line)
        got += 1
    print(f"=== база: прочитано {got}/{len(sr.DEFAULT_SET)} ===\n")


async def listen(mac, secs, pre=5.0, baseline=True, log_path=None, snoop=False):
    if log_path is None:
        d = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "docs")
        _os.makedirs(d, exist_ok=True)
        log_path = _os.path.join(d, f"push_capture_{datetime.now():%Y%m%d_%H%M%S}.txt")
    logf = open(log_path, "w", encoding="utf-8", buffering=1)  # line-buffered: живой tail
    tee = _Tee(_sys.stdout, logf)
    try:
        with contextlib.redirect_stdout(tee):
            print(f"[i] лог пишется в: {log_path}")
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
                print("\n[+] LOGIN OK — CCCD на 0x001b уже стоит (подписка активна)")

                if baseline:
                    await read_baseline(t, sk)

                print("=== ГОТОВНОСТЬ: СЕЙЧАС меняй состояние самоката ===")
                print("  • пожать/отпустить ручку газа   -> скорость/ток/мощность")
                print("  • включить/выключить задний свет, cruise")
                print("  • покатить                      -> пробег/время/режим езды")
                print(f"Окно прослушивания: {secs:.0f} с. Старт через отсчёт…\n")
                for k in range(int(pre), 0, -1):
                    print(f"  старт через {k}…", end="\r")
                    await asyncio.sleep(1)
                print("  >>> ПОЕХАЛИ — меняй состояние! <<<  ")
                print("[[WINDOW_OPEN]]")  # ASCII-сентинел для внешней детекции (не зависит от кодировки)

                loop = asyncio.get_event_loop()
                deadline = loop.time() + secs
                next_remind = loop.time() + 20
                n_push = 0
                ch_counts = {}

                async def handle_plain(pt, src):
                    nonlocal n_push
                    n_push += 1
                    res = parse_props(pt)
                    props, op = res if isinstance(res, tuple) else (res, None)
                    ts = datetime.now().strftime("%H:%M:%S")
                    print(f"\n  [{ts}] ПУШ #{n_push} ({src}, op={op}) {pt.hex()}")
                    for siid, piid, tcode, val, status in props:
                        mark = "" if (siid, piid) in SUBSCRIBABLE else "  [вне списка подписки]"
                        print("      " + sr.fmt_value(siid, piid, tcode, val)
                              + ("" if status == 0 else f"  [status={status}]") + mark)

                while loop.time() < deadline:
                    if loop.time() >= next_remind:
                        left = int(deadline - loop.time())
                        print(f"\n  …пушей {n_push}; RX по каналам={ch_counts or '∅'}; осталось ~{left} с — меняй состояние!")
                        next_remind = loop.time() + 20
                    try:
                        s, b = await asyncio.wait_for(t.rx.get(), timeout=1.0)
                    except asyncio.TimeoutError:
                        continue  # тик: пока кадров нет — проверяем deadline/напоминания и слушаем дальше
                    ch_counts[s] = ch_counts.get(s, 0) + 1
                    if snoop:
                        ts = datetime.now().strftime("%H:%M:%S")
                        print(f"  [{ts}] RX ch=0x{s:04X} len={len(b)}  {b.hex()}")
                    if s != CH_NOTIFY or len(b) < 4:
                        continue
                    # одиночный кадр: [0000][02][00][cnt][ct]
                    if b[0] == 0 and b[1] == 0 and b[2] == 0x02 and len(b) >= 6:
                        cnt = struct.unpack("<H", b[4:6])[0]
                        await t.write(CH_NOTIFY, struct.pack("<HBB", 0, 0x03, 0))
                        try:
                            await handle_plain(sr.dec_dev(sk, cnt, b[6:]), "одиночный")
                        except Exception as e:
                            print(f"  [!] не расшифровалось (cnt={cnt}): {e}  raw={b.hex()}")
                    # многокадровый: CTR от устройства
                    elif b[0] == 0 and b[1] == 0 and b[2] == 0x00 and len(b) >= 6:
                        fc = struct.unpack("<H", b[4:6])[0]
                        await t.write(CH_NOTIFY, struct.pack("<HBB", 0, 0x01, 0x01))
                        parts = {}
                        rdl = loop.time() + 5.0
                        while len(parts) < fc and loop.time() < rdl:
                            try:
                                s2, b2 = await asyncio.wait_for(
                                    t.rx.get(), timeout=max(0.1, rdl - loop.time()))
                            except asyncio.TimeoutError:
                                break
                            if s2 == CH_NOTIFY and len(b2) >= 2:
                                seq = struct.unpack("<H", b2[:2])[0]
                                if 1 <= seq <= fc:
                                    parts[seq] = b2[2:]
                        await t.write(CH_NOTIFY, struct.pack("<HBB", 0, 0x01, 0x00))
                        if len(parts) == fc:
                            payload = b"".join(parts[i] for i in sorted(parts))
                            cnt = struct.unpack("<H", payload[:2])[0]
                            try:
                                await handle_plain(sr.dec_dev(sk, cnt, payload[2:]), f"{fc} кадра")
                            except Exception as e:
                                print(f"  [!] не расшифровалось (cnt={cnt}): {e}")
                        else:
                            print(f"  [!] получено {len(parts)}/{fc} кадров")

                print(f"\n=== итог: пушей получено {n_push}; RX по каналам={ch_counts or '∅'} ===")
                if n_push == 0:
                    print("тишина. Это НЕ опровергает механизм: если ничего не менялось, "
                          "пушить нечего.\nПовтори, активно меняя состояние (газ/свет/движение).")
                else:
                    print(f"Лог сохранён: {log_path}")
                return 0
            except Exception:
                import traceback
                traceback.print_exc()
                return 1
            finally:
                await t.close()
    finally:
        logf.flush()
        logf.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mac", default=da.MAC_DEFAULT)
    ap.add_argument("--secs", type=float, default=120.0, help="окно прослушивания, с (по умолч. 120)")
    ap.add_argument("--pre", type=float, default=5.0, help="отсчёт до старта окна, с (по умолч. 5)")
    ap.add_argument("--no-baseline", action="store_true", help="не читать базовые значения")
    ap.add_argument("--snoop", action="store_true",
                    help="логировать ВСЕ входящие кадры на ЛЮБЫХ характеристиках (диагностика, где идёт пуш)")
    ap.add_argument("--log", default=None, help="путь к лог-файлу (по умолчанию docs/push_capture_*.txt)")
    a = ap.parse_args()
    raise SystemExit(asyncio.run(listen(a.mac, a.secs, pre=a.pre,
                                        baseline=not a.no_baseline, log_path=a.log, snoop=a.snoop)))
