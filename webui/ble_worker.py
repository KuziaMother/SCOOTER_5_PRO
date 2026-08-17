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

from bleak import BleakScanner

import dreame_auth as da
import spec_read as sr
import props

CH_WRITE = sr.CH_WRITE
CH_NOTIFY = sr.CH_NOTIFY

# Имена, по которым узнаём "наши" устройства среди шума эфира — показываем
# их первыми в списке скана (§4: сам скан ничего не пишет на устройство,
# только слушает рекламные пакеты — безопасен для повтора).
LIKELY_NAME_HINTS = ("scooter", "dreame", "xiaomi", "ninebot", "mi ")


async def scan_devices(timeout=5.0):
    """Пассивный скан эфира — список рядом стоящих BLE-устройств (имя+MAC+RSSI).
    Не подключается и не отправляет ничего устройству, только слушает рекламу."""
    found = await BleakScanner.discover(timeout=timeout, return_adv=True)
    devices = []
    for mac, (dev, adv) in found.items():
        name = adv.local_name or dev.name
        if not name:
            continue
        likely = any(h in name.lower() for h in LIKELY_NAME_HINTS)
        devices.append({"name": name, "mac": mac, "rssi": adv.rssi, "likely": likely})
    devices.sort(key=lambda d: (not d["likely"], -d["rssi"]))
    return devices


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
    ltmk_path = da.ltmk_path_for_mac(mac)
    try:
        with open(ltmk_path, "r", encoding="utf-8") as f:
            ltmk = bytes.fromhex(f.read().strip())
    except Exception as e:
        raise WorkerError(f"нет/не читается {ltmk_path}: {type(e).__name__}")

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
                     emit_round=False, set_queue=None):
    """Paced-чтение списка свойств по одному. Возвращает новый app_cnt.

    Если задан set_queue — подхватывает накопленные SET-команды ПЕРЕД каждым
    отдельным чтением (не только в начале батча). Иначе клик по настройке
    ждёт конца всего текущего батча чтений (~13 свойств × 0.35с ≈ 4.5с) —
    заметная и ненужная задержка между нажатием и реальной отправкой на
    самокат (проверено живьём — см. журнал реверса)."""
    vals = {}
    for key in prop_list:
        if should_stop():
            break
        if set_queue is not None and not set_queue.empty():
            app_cnt = await apply_pending_sets(t, sk, set_queue, on_event, unit_mult, app_cnt)
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


def _set_frame(siid, piid, type_code, value, tid=1):
    """SET-кадр spec: op=0, объект [siid][piid][(type<<12)|vlen][value] (docs/FACTS.md)."""
    vlen = len(value)
    obj = struct.pack("<BHH", siid & 0xFF, piid & 0xFFFF,
                      ((type_code & 0xF) << 12) | (vlen & 0xFFF)) + value
    total = 6 + len(obj)
    return struct.pack("<HHBB", (total | 0x2000) & 0xFFFF, tid & 0xFFFF, 0, 1) + obj


async def spec_write(t, sk, siid, piid, type_code, value, app_cnt, timeout=8.0):
    """SET одного свойства (op=0). Возвращает (ok, status). Один кадр, без повторов."""
    frame = _set_frame(siid, piid, type_code, value)
    payload = sr.enc_app(sk, app_cnt, frame)
    fs = 18
    frames = [payload[i:i + fs] for i in range(0, len(payload), fs)] or [b""]
    while not t.rx.empty():
        t.rx.get_nowait()
    await t.write(CH_WRITE, struct.pack("<HBBH", 0, 0x00, sr.SPEC_CHANNEL, len(frames)))

    async def send_seq(n):
        if 1 <= n <= len(frames):
            await t.write(CH_WRITE, struct.pack("<H", n) + frames[n - 1])

    loop = asyncio.get_event_loop()
    deadline = loop.time() + timeout
    sent = False
    while loop.time() < deadline:
        try:
            s, b = await asyncio.wait_for(t.rx.get(), timeout=deadline - loop.time())
        except asyncio.TimeoutError:
            break
        if len(b) >= 3 and b[0] == 0 and b[1] == 0 and b[2] == 0x01:
            st = b[3] if len(b) > 3 else None
            if st == 0x01 and not sent:
                sent = True
                for n in range(1, len(frames) + 1):
                    await send_seq(n)
                    await asyncio.sleep(0.03)
            elif st == 0x05:
                for i in range(0, len(b) - 4, 2):
                    await send_seq(struct.unpack_from("<H", b, 4 + i)[0])
                    await asyncio.sleep(0.03)
        elif len(b) >= 6 and b[0] == 0 and b[1] == 0 and b[2] == 0x00 and s == CH_NOTIFY:
            fc = struct.unpack("<H", b[4:6])[0]
            await t.write(CH_NOTIFY, struct.pack("<HBB", 0, 0x01, 0x01))
            parts = {}
            rdl = loop.time() + 6.0
            while len(parts) < fc and loop.time() < rdl:
                try:
                    s2, b2 = await asyncio.wait_for(t.rx.get(), timeout=max(0.1, rdl - loop.time()))
                except asyncio.TimeoutError:
                    break
                if s2 == CH_NOTIFY and len(b2) >= 2:
                    seq = struct.unpack("<H", b2[:2])[0]
                    if 1 <= seq <= fc:
                        parts[seq] = b2[2:]
            await t.write(CH_NOTIFY, struct.pack("<HBB", 0, 0x01, 0x00))
            if len(parts) != fc:
                return False, None
            pl = b"".join(parts[i] for i in sorted(parts))
            try:
                rpt = sr.dec_dev(sk, struct.unpack("<H", pl[:2])[0], pl[2:])
            except Exception:
                return False, None
            # ответ op=1: заголовок(6) + [siid][piid][status u16]
            status = struct.unpack_from("<H", rpt, 9)[0] if len(rpt) >= 11 else None
            return (status == 0), status
    return False, None


async def apply_pending_sets(t, sk, set_queue, on_event, unit_mult, app_cnt):
    """Выполнить накопленные SET-команды из очереди (тред-безопасно). §5 — только whitelist."""
    if set_queue is None:
        return app_cnt
    while True:
        try:
            cmd = set_queue.get_nowait()
        except Exception:
            break
        key = (cmd["siid"], cmd["piid"])
        if not props.is_writable(key):
            on_event({"type": "log", "message": f"SET {key} отклонён (не в whitelist)"})
            continue
        value = cmd["value"]
        name = props.LABELS.get(key, f"{key[0]}.{key[1]}")
        vtxt = "вкл" if value == b"\x01" else "выкл"
        ok, status = await spec_write(t, sk, key[0], key[1], cmd["type"], value, app_cnt)
        app_cnt += 1
        if ok:
            on_event({"type": "log", "message": f"SET {name} → {vtxt}: принято (status 0)"})
            await read_one(t, sk, key, app_cnt, on_event, unit_mult)  # перечитать реальное состояние
            app_cnt += 1
        else:
            on_event({"type": "log", "message": f"SET {name} → {vtxt}: ОТКАЗ (status={status})"})
        await asyncio.sleep(0.3)
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


async def _run_once(mac, mode, interval, static_interval, on_event, should_stop, set_queue=None):
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
                app_cnt = await apply_pending_sets(
                    t, sk, set_queue, on_event, unit_mult, app_cnt
                )
                app_cnt = await read_props(
                    t, sk, dynamic_no_unit, on_event, unit_mult, app_cnt, should_stop,
                    emit_round=True, set_queue=set_queue
                )
                if loop.time() - last_static >= static_interval:
                    app_cnt = await read_props(
                        t, sk, props.STATIC_SET, on_event, unit_mult, app_cnt, should_stop,
                        set_queue=set_queue
                    )
                    last_static = loop.time()
                elapsed = loop.time() - round_start
                wait = max(0.2, interval - elapsed)
                end = loop.time() + wait
                while not should_stop() and loop.time() < end:
                    # простой между раундами — не ждать сложа руки, если за это
                    # время накопился клик: сразу отправляем и завершаем простой.
                    if set_queue is not None and not set_queue.empty():
                        app_cnt = await apply_pending_sets(
                            t, sk, set_queue, on_event, unit_mult, app_cnt
                        )
                        break
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


async def run_session(mac, mode, interval, static_interval, on_event, should_stop, set_queue=None):
    """Внешняя обёртка: одна попытка переподключения при необработанном обрыве."""
    if mode not in {"once", "poll", "push"}:
        raise WorkerError(f"неизвестный режим: {mode}")

    for attempt in range(2):
        if should_stop():
            return
        try:
            await _run_once(mac, mode, interval, static_interval, on_event, should_stop, set_queue)
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
