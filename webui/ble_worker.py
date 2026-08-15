#!/usr/bin/env python3
"""
BLE-воркер для модульного web UI: login, paced read-only опрос, push-слушатель.

Правила безопасности:
  * только чтение spec-свойств (op=2 из probes/spec_read.py); set/запись здесь нет;
  * одно свойство на запрос (устройство обслуживает только первый объект);
  * паузы между запросами, без циклов перебора и спам-повторов;
  * при обрыве — максимум одна повторная попытка переподключения;
  * секреты не логируются (props.format_property маскирует SENSITIVE).
"""
import asyncio
import struct

import dreame_auth as da
import spec_read as sr
import props

CH_WRITE = sr.CH_WRITE
CH_NOTIFY = sr.CH_NOTIFY


class WorkerError(Exception):
    """Ожидаемая отказная ветка (login/refused, нет ключа и т.п.)."""


def parse_spec_payload(pt):
    """Открытый spec-кадр -> список объектов + op из заголовка."""
    if not pt or len(pt) < 6:
        return [], None
    try:
        _lenflag, _tid, op, count = struct.unpack("<HHBB", pt[:6])
    except struct.error:
        return [], None
    items = []
    off = 6
    for _ in range(count):
        if off + 7 > len(pt):
            break
        siid, piid, status, tl = struct.unpack("<BHHH", pt[off:off + 7])
        tcode, vlen = tl >> 12, tl & 0x0FFF
        val = pt[off + 7: off + 7 + vlen]
        off += 7 + vlen
        items.append({
            "siid": siid, "piid": piid, "status": status,
            "tcode": tcode, "value": val,
        })
    return items, op


async def establish(mac, on_event):
    """connect + A4 + stage A/B. Возвращает (Transport, sk)."""
    try:
        with open(da.LTMK_HEX, "r", encoding="utf-8") as f:
            ltmk = bytes.fromhex(f.read().strip())
    except Exception as e:
        raise WorkerError(f"нет/не читается {da.LTMK_HEX}: {type(e).__name__}")

    on_event({"type": "status", "status": "connecting", "message": "подключение к самокату…"})
    t = da.Transport(mac)
    try:
        await t.connect()
        if not await t.a4_handshake():
            raise WorkerError("транспорт не поднялся (A4 handshake fail)")
        for s, b in await t.drain(1.0):
            if s == da.CH_LOGIN and len(b) >= 3 and b[2] == da.PKT_MNG:
                await t.write(
                    da.CH_LOGIN,
                    struct.pack("<HBB", 0, da.PKT_MNG_ACK, 0) + bytes([t.pkg_num, t.dmtu]),
                )

        on_event({"type": "status", "status": "login", "message": "обмен ключами (stage A/B)…"})
        priv, dev_pub = await da.stage_a_pubkey_exchange(t)
        if not (dev_pub and len(dev_pub) >= 64):
            raise WorkerError("нет публичного ключа устройства")
        if not await da.stage_b_confirm(t, priv, dev_pub, ltmk, crc_be=False):
            raise WorkerError("login отказан устройством")
        sk = da.LAST_SK
        if not sk:
            raise WorkerError("session key не получен")
        on_event({"type": "status", "status": "ready", "message": "LOGIN OK — сессия готова"})
        return t, sk
    except WorkerError:
        try:
            await t.close()
        except Exception:
            pass
        raise
    except Exception as e:
        try:
            await t.close()
        except Exception:
            pass
        raise WorkerError(f"ошибка транспорта при подключении: {type(e).__name__}: {e}")


async def read_one(t, sk, key, app_cnt, on_event, unit_mult):
    """Одно read-only spec-свойство. Возвращает текст для round или None."""
    siid, piid = key
    pt = await sr.spec_request(t, sk, [key], app_cnt=app_cnt)
    if not pt:
        fmt = props.format_property(siid, piid, 0, b"", unit_mult[0])
        fmt["text"] = "нет ответа"
        on_event({"type": "property", "push": False, "data": fmt})
        return None

    items, _op = parse_spec_payload(pt)
    item = next((x for x in items if x["siid"] == siid and x["piid"] == piid), None)
    if item is None and items:
        item = items[0]
    if item is None:
        fmt = props.format_property(siid, piid, 0, b"", unit_mult[0])
        fmt["text"] = "пустой ответ"
        on_event({"type": "property", "push": False, "data": fmt})
        return None

    if key == (3, 5):
        unit_mult[0] = props.unit_multiplier(props.decode_value(item["tcode"], item["value"]))

    fmt = props.format_property(siid, piid, item["tcode"], item["value"], unit_mult[0])
    if item.get("status") not in (0, None):
        fmt["text"] += f" [status={item['status']}]"
    on_event({"type": "property", "push": False, "data": fmt})
    return fmt["text"]


async def read_props(t, sk, prop_list, on_event, unit_mult, app_cnt, should_stop,
                     emit_round=False):
    """Paced-чтение списка свойств по одному. Возвращает новый app_cnt."""
    vals = {}
    for key in prop_list:
        if should_stop():
            break
        if not props.is_safe(key):
            continue
        text = await read_one(t, sk, key, app_cnt, on_event, unit_mult)
        app_cnt += 1
        if text is not None:
            vals[f"{key[0]}.{key[1]}"] = text
        await asyncio.sleep(0.35)
    if emit_round and vals:
        on_event({"type": "round", "vals": vals})
    return app_cnt


async def _emit_push_items(t, sk, pt, pushes, rx_counts, on_event, unit_mult):
    items, _op = parse_spec_payload(pt)
    if not items:
        return pushes
    pushes += 1
    for item in items:
        fmt = props.format_property(
            item["siid"], item["piid"], item["tcode"], item["value"], unit_mult[0]
        )
        if item.get("status") not in (0, None):
            fmt["text"] += f" [status={item['status']}]"
        on_event({"type": "property", "push": True, "data": fmt})
    on_event({
        "type": "counters",
        "pushes": pushes,
        "rx": {f"0x{k:04X}": v for k, v in rx_counts.items()},
    })
    return pushes


async def listen_push(t, sk, on_event, unit_mult, should_stop):
    """Слушать notify 0x001b до СТОП (пуш приходит при изменении свойства)."""
    loop = asyncio.get_event_loop()
    pushes = 0
    rx_counts = {}

    while not should_stop():
        try:
            s, b = await asyncio.wait_for(t.rx.get(), timeout=1.0)
        except asyncio.TimeoutError:
            continue

        rx_counts[s] = rx_counts.get(s, 0) + 1
        on_event({
            "type": "counters",
            "pushes": pushes,
            "rx": {f"0x{k:04X}": v for k, v in rx_counts.items()},
        })

        if s != CH_NOTIFY or len(b) < 4:
            continue

        # одиночный notify-кадр: [0000][02][00][cnt u16][ct]
        if b[0] == 0 and b[1] == 0 and b[2] == 0x02 and len(b) >= 6:
            cnt = struct.unpack("<H", b[4:6])[0]
            await t.write(CH_NOTIFY, struct.pack("<HBB", 0, 0x03, 0))
            try:
                pt = sr.dec_dev(sk, cnt, b[6:])
            except Exception as e:
                on_event({"type": "log", "message": f"push не расшифрован (cnt={cnt}): {type(e).__name__}"})
                continue
            pushes = await _emit_push_items(t, sk, pt, pushes, rx_counts, on_event, unit_mult)

        # многокадровый notify: CTR от устройства [0000][00][ch][fc]
        elif b[0] == 0 and b[1] == 0 and b[2] == 0x00 and len(b) >= 6:
            fc = struct.unpack("<H", b[4:6])[0]
            if fc == 0:
                continue
            await t.write(CH_NOTIFY, struct.pack("<HBB", 0, 0x01, 0x01))
            parts = {}
            rdl = loop.time() + 5.0
            while len(parts) < fc and loop.time() < rdl and not should_stop():
                try:
                    s2, b2 = await asyncio.wait_for(
                        t.rx.get(), timeout=max(0.1, rdl - loop.time())
                    )
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
                    pt = sr.dec_dev(sk, cnt, payload[2:])
                except Exception as e:
                    on_event({"type": "log", "message": f"многокадровый push не расшифрован: {type(e).__name__}"})
                    continue
                pushes = await _emit_push_items(t, sk, pt, pushes, rx_counts, on_event, unit_mult)
            else:
                on_event({"type": "log", "message": f"push: получено {len(parts)}/{fc} кадров"})


async def _run_once(mac, mode, interval, static_interval, on_event, should_stop):
    t, sk = await establish(mac, on_event)
    unit_mult = [1.0]
    app_cnt = 0
    loop = asyncio.get_event_loop()

    try:
        while not t.rx.empty():
            t.rx.get_nowait()

        # Сначала единицы — чтобы дальнейшие расстояния конвертировались правильно.
        if not should_stop():
            app_cnt = await read_props(
                t, sk, [(3, 5)], on_event, unit_mult, app_cnt, should_stop, emit_round=False
            )

        dynamic_no_unit = [k for k in props.DYNAMIC_SET if k != (3, 5)]
        full_no_unit = [k for k in props.FULL_SAFE_SET if k != (3, 5)]

        if mode == "once":
            on_event({"type": "status", "status": "reading", "message": "полный read-only снимок…"})
            app_cnt = await read_props(
                t, sk, full_no_unit, on_event, unit_mult, app_cnt, should_stop, emit_round=True
            )
            on_event({"type": "status", "status": "done", "message": "снимок готов"})

        elif mode == "poll":
            if not should_stop():
                on_event({"type": "status", "status": "baseline", "message": "читаю журнал поездок один раз…"})
                app_cnt = await read_props(
                    t, sk, props.LOG_SET, on_event, unit_mult, app_cnt, should_stop
                )
            on_event({
                "type": "status", "status": "polling",
                "message": f"поллинг каждые ~{interval:.0f} с; медленный набор ~{static_interval:.0f} с",
            })
            last_static = 0.0
            while not should_stop():
                round_start = loop.time()
                app_cnt = await read_props(
                    t, sk, dynamic_no_unit, on_event, unit_mult, app_cnt, should_stop,
                    emit_round=True
                )
                if loop.time() - last_static >= static_interval:
                    app_cnt = await read_props(
                        t, sk, props.STATIC_SET, on_event, unit_mult, app_cnt, should_stop
                    )
                    last_static = loop.time()
                elapsed = loop.time() - round_start
                wait = max(0.2, interval - elapsed)
                end = loop.time() + wait
                while not should_stop() and loop.time() < end:
                    await asyncio.sleep(0.2)
            on_event({"type": "status", "status": "done", "message": "поллинг остановлен"})

        elif mode == "push":
            if not should_stop():
                on_event({"type": "status", "status": "baseline",
                          "message": "baseline: полный read-only снимок…"})
                app_cnt = await read_props(
                    t, sk, full_no_unit, on_event, unit_mult, app_cnt, should_stop
                )
            if not should_stop():
                while not t.rx.empty():
                    t.rx.get_nowait()
                on_event({
                    "type": "status", "status": "listening",
                    "message": "слушаю notify: пожайте газ / включите свет / покатитесь",
                })
                await listen_push(t, sk, on_event, unit_mult, should_stop)
            on_event({"type": "status", "status": "done", "message": "прослушивание остановлено"})

        else:
            raise WorkerError(f"неизвестный режим: {mode}")

    finally:
        try:
            await t.close()
        except Exception:
            pass


async def run_session(mac, mode, interval, static_interval, on_event, should_stop):
    """Внешняя обёртка: одна попытка переподключения при необработанном обрыве."""
    if mode not in {"once", "poll", "push"}:
        raise WorkerError(f"неизвестный режим: {mode}")

    for attempt in range(2):
        if should_stop():
            return
        try:
            await _run_once(mac, mode, interval, static_interval, on_event, should_stop)
            return
        except WorkerError as e:
            on_event({"type": "status", "status": "error", "message": str(e)})
            return
        except Exception as e:
            msg = f"{type(e).__name__}: {e}"
            on_event({"type": "status", "status": "error", "message": msg})
            if attempt == 0 and not should_stop():
                on_event({"type": "log", "message": "обрыв сессии — одна попытка переподключения…"})
                await asyncio.sleep(2.0)
                continue
            return
