#!/usr/bin/env python3
"""
Чтение телеметрии самоката по MIoT-spec поверх BLE (батарея, скорость, пробег, SOH).

Протокол подтверждён снупом реальной сессии Mi Home (logs/btsnoop_hci.log):
  запрос  -> 0x001a: CTR [0000][00][ch=0][fc u16] -> ACK [0000][01][01]
                     DATA [seq u16][counter u16 LE][ct] -> ACK [0000][01][00]
  ответ   <- 0x001b: [0000][02][00][counter u16 LE][ct]
  подтв.  -> 0x001b: [0000][03][00]

Шифрование (реверс BleSecurityChipEncrypt / _m_j/au0->OooO0OO):
  app->dev: key=sk[16:32], iv=sk[36:40]   dev->app: key=sk[0:16], iv=sk[32:36]
  nonce = iv || 00 00 00 00 || counterBytes(4);  AES-CCM, tag 4 Б

Кадр spec (реверс _m_j/n14->buildBytes):
  [u16 LE len|0x2000][u16 LE id][u8 0][u8 count]
  объект: [u8 siid][u16 LE piid][u16 LE (typeCode<<12)|valueLen][value]

ТОЛЬКО ЧТЕНИЕ: valueLen=0, ни одного set-запроса не отправляется.

Запуск:  python probes/spec_read.py                    # набор телеметрии
         python probes/spec_read.py --siid 1 --piid 2   # одно свойство
"""
import argparse
import asyncio
import os as _os
import struct
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

import dreame_auth as da
from cryptography.hazmat.primitives.ciphers.aead import AESCCM

CH_WRITE = 0x001A
CH_NOTIFY = 0x001B
SPEC_CHANNEL = 0          # подтверждено снупом (НЕ 6, как я решил по дизасму)

NAMES = {
    (1, 1): "RIDING_MODE", (1, 2): "BATTERY_LEVEL", (1, 3): "REMAINING_BATTERY",
    (1, 4): "VOLTAGE", (1, 5): "CURRENT", (1, 6): "POWER",
    (1, 7): "REMAINING_MILEAGE", (1, 8): "FAULT", (1, 9): "CURRENT_MILEAGE",
    (2, 1): "AVERAGE_SPEED", (2, 2): "IS_LOCKED", (2, 3): "CRUISE_IS_ON",
    (2, 4): "TAIL_LIGHT_IS_ON", (2, 5): "ENERGY_RECOVERY", (2, 6): "TOTAL_MILEAGE",
    (2, 7): "IS_RIDING", (2, 8): "RIDING_TIME", (2, 9): "HIGHEST_SPEED",
    (3, 1): "BATTERY_STATUS", (3, 2): "BATTERY_TEMPERATURE",
    (3, 3): "SCOOTER_TEMPERATURE", (3, 10): "IS_CHARGING",
    (3, 11): "NUMBER_OF_CYCLES", (3, 12): "SOH",
    (4, 1): "PRODUCTION_DATE", (4, 2): "BATTERY_SN", (4, 3): "BMS_FIRMWARE_VERSION",
    (4, 4): "SCOOTER_SN", (4, 5): "FIRMWARE_VERSION",
}

# 6 объектов — ровно как в снупе (ct 40Б -> 36Б открытого = 6 + 5*6)
DEFAULT_SET = [(1, 2), (1, 4), (1, 5), (1, 7), (2, 6), (3, 2)]


def counter_bytes(cnt):
    low, high = cnt & 0xFFFF, (cnt >> 16) & 0xFFFF
    return bytes([low & 0xFF, low >> 8, high & 0xFF, high >> 8])


def build_frame(objects, tid=1, type_code=0, op=2):
    """op — код операции (смещение 4): запрос чтения = 2, ответ устройства = 3."""
    body = b"".join(struct.pack("<BHH", s & 0xFF, p & 0xFFFF,
                                (type_code & 0xF) << 12) for s, p in objects)
    total = 6 + len(body)
    return struct.pack("<HHBB", (total | 0x2000) & 0xFFFF, tid & 0xFFFF,
                       op & 0xFF, len(objects)) + body


def enc_app(sk, cnt, frame):
    nonce = sk[36:40] + b"\x00\x00\x00\x00" + counter_bytes(cnt)
    ct = AESCCM(sk[16:32], tag_length=4).encrypt(nonce, frame, None)
    return struct.pack("<H", cnt & 0xFFFF) + ct


def dec_dev(sk, cnt, ct):
    nonce = sk[32:36] + b"\x00\x00\x00\x00" + counter_bytes(cnt)
    return AESCCM(sk[0:16], tag_length=4).decrypt(nonce, ct, None)


# SpecValueType.bitValue -> имя (из com/miot/spec/entity/SpecValueType.<clinit>)
TYPES = {0: "BOOL", 1: "UINT8", 2: "INT8", 3: "UINT16", 4: "INT16",
         5: "UINT32", 6: "INT32", 7: "UINT64", 8: "INT64", 9: "FLOAT",
         10: "STRING"}

# единицы: подтверждено измерением (пробег вышел ровным 440.0 км)
# Проверка согласованности: 53.44 В x 1.0 А = 53.4 Вт, а POWER вернул ровно 53 —
# значит ток в амперах, мощность в ваттах, напряжение в 0.01 В.
UNITS = {
    "VOLTAGE": (0.01, "В"), "CURRENT": (1.0, "А"), "POWER": (1.0, "Вт"),
    "TOTAL_MILEAGE": (0.01, "км"), "CURRENT_MILEAGE": (0.01, "км"),
    "REMAINING_MILEAGE": (0.01, "км"),
    "BATTERY_LEVEL": (1.0, "%"), "SOH": (1.0, "%"),
    # Живые скорости: сырое FLOAT * 0.01 = км/ч (плагин 10451.js: value / 100;
    # подтверждено живым поллингом: пик 2540 -> 25.4 км/ч при региональном лимите 25).
    "AVERAGE_SPEED": (0.01, "км/ч"), "HIGHEST_SPEED": (0.01, "км/ч"),
    "BATTERY_TEMPERATURE": (1.0, "°C"), "SCOOTER_TEMPERATURE": (1.0, "°C"),
    "RIDING_TIME": (1.0, "с"),
}


def decode_value(tcode, val):
    """Значение по коду типа. type 9 = FLOAT32 (иначе целое читается мусором)."""
    if not val:
        return None
    if tcode == 9 and len(val) == 4:
        return struct.unpack("<f", val)[0]
    if tcode == 10:
        return val.decode("utf-8", "replace")
    if tcode in (2, 4, 6, 8):
        return int.from_bytes(val, "little", signed=True)
    return int.from_bytes(val, "little")


def fmt_value(siid, piid, tcode, val):
    name = NAMES.get((siid, piid), "?")
    tname = TYPES.get(tcode, f"type{tcode}")
    if not val:
        return f"siid={siid} piid={piid:<3} [{name:<22}] пусто"
    v = decode_value(tcode, val)
    shown = f"{v:g}" if isinstance(v, float) else str(v)
    if name in UNITS:
        mul, unit = UNITS[name]
        scaled = (v * mul) if isinstance(v, (int, float)) else v
        if mul != 1.0:
            shown = f"{scaled:g} {unit}   (сырое {v:g})"
        else:
            shown = f"{shown} {unit}"
    return (f"siid={siid} piid={piid:<3} [{name:<22}] {tname:<6} = {shown}"
            f"   raw={val.hex()}")


def parse_reply(pt):
    if len(pt) < 6:
        return [f"кадр короче заголовка: {pt.hex()}"]
    lenflag, tid, b2, count = struct.unpack("<HHBB", pt[:6])
    out = [f"заголовок: len={lenflag & 0x0FFF} flag=0x{lenflag & 0xF000:04x} "
           f"id={tid} b2={b2} объектов={count}"]
    # В ОТВЕТЕ у объекта на 2 байта больше, чем в запросе — есть поле статуса:
    #   [u8 siid][u16 LE piid][u16 LE status][u16 LE (type<<12)|len][value]
    off = 6
    for _ in range(count):
        if off + 7 > len(pt):
            out.append(f"  обрыв на {off}")
            break
        siid, piid, status, tl = struct.unpack("<BHHH", pt[off:off + 7])
        tcode, vlen = tl >> 12, tl & 0x0FFF
        val = pt[off + 7: off + 7 + vlen]
        off += 7 + vlen
        err = "" if status == 0 else f"  [status={status}]"
        out.append("  " + fmt_value(siid, piid, tcode, val) + err)
    if off < len(pt):
        out.append(f"  хвост: {pt[off:].hex()}")
    return out


async def spec_request(t, sk, objects, app_cnt, tid=1, frame_size=18, timeout=8.0, type_code=0, op=2):
    """Один запрос с pull-циклом (ACK 05 = «пришли кадр N», как в DFU).

    ВАЖНО: ровно одна попытка, без повторов — чтобы не спамить устройство.
    """
    payload = enc_app(sk, app_cnt, build_frame(objects, tid, type_code, op))
    frames = [payload[i:i + frame_size]
              for i in range(0, len(payload), frame_size)] or [b""]
    print(f"    payload {len(payload)}Б -> {len(frames)} кадр(ов) по {frame_size}Б")
    while not t.rx.empty():
        t.rx.get_nowait()

    ctr = struct.pack("<HBBH", 0, 0x00, SPEC_CHANNEL, len(frames))
    await t.write(CH_WRITE, ctr)

    async def send_seq(n):
        if 1 <= n <= len(frames):
            await t.write(CH_WRITE, struct.pack("<H", n) + frames[n - 1])

    loop = asyncio.get_event_loop()
    deadline = loop.time() + timeout
    sent_all = False
    while loop.time() < deadline:
        try:
            s, b = await asyncio.wait_for(t.rx.get(), timeout=deadline - loop.time())
        except asyncio.TimeoutError:
            break
        if len(b) >= 3 and b[0] == 0 and b[1] == 0 and b[2] == 0x01:
            st = b[3] if len(b) > 3 else None
            if st == 0x01 and not sent_all:            # готов принимать
                sent_all = True
                for n in range(1, len(frames) + 1):
                    await send_seq(n)
                    await asyncio.sleep(0.03)
            elif st == 0x05:                           # pull: пришли эти кадры
                seqs = [struct.unpack_from("<H", b, 4 + i)[0]
                        for i in range(0, len(b) - 4, 2)]
                for n in seqs:
                    await send_seq(n)
                    await asyncio.sleep(0.03)
            elif st == 0x00:
                print("    сообщение принято (ACK 00)")
        elif len(b) >= 6 and b[0] == 0 and b[1] == 0 and b[2] == 0x00 and s == CH_NOTIFY:
            # CTR ОТ УСТРОЙСТВА: принимай ответ из fc кадров
            fc = struct.unpack("<H", b[4:6])[0]
            print(f"    <<< CTR от устройства: fc={fc} — принимаем ответ")
            await t.write(CH_NOTIFY, struct.pack("<HBB", 0, 0x01, 0x01))  # готов
            parts = {}
            rdl = loop.time() + 6.0
            while len(parts) < fc and loop.time() < rdl:
                try:
                    s2, b2 = await asyncio.wait_for(t.rx.get(),
                                                    timeout=rdl - loop.time())
                except asyncio.TimeoutError:
                    break
                if s2 == CH_NOTIFY and len(b2) >= 2:
                    seq = struct.unpack("<H", b2[:2])[0]
                    if 1 <= seq <= fc:
                        parts[seq] = b2[2:]
            await t.write(CH_NOTIFY, struct.pack("<HBB", 0, 0x01, 0x00))  # принято
            if len(parts) != fc:
                print(f"    [!] получено {len(parts)}/{fc} кадров")
                return None
            payload = b"".join(parts[i] for i in sorted(parts))
            dev_cnt = struct.unpack("<H", payload[:2])[0]
            ct = payload[2:]
            print(f"    ответ собран: cnt={dev_cnt}, ct={len(ct)}Б")
            try:
                return dec_dev(sk, dev_cnt, ct)
            except Exception as e:
                print(f"    [!] не расшифровалось (dev cnt={dev_cnt}): {e}")
                print(f"        payload={payload.hex()}")
                return None
    print("    [!] ответа нет")
    return None


async def run(mac, objects, frame_size=18, app_cnt=0, op=2, type_code=0):
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
        print(f"=== запрос: {objects} ===")
        pt = await spec_request(t, sk, objects, app_cnt,
                                frame_size=frame_size, type_code=type_code, op=op)
        if pt:
            print(f"  ОТКРЫТЫЙ ОТВЕТ ({len(pt)}Б): {pt.hex()}")
            lines = parse_reply(pt)
            for line in lines:
                print("  " + line)
            if "пусто" not in "".join(lines):
                print("\n  >>> ЗНАЧЕНИЯ ПОЛУЧЕНЫ!")
                return 0
        return 1
    except Exception:
        import traceback
        traceback.print_exc()
        return 1
    finally:
        await t.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mac", default=da.MAC_DEFAULT)
    ap.add_argument("--siid", type=int)
    ap.add_argument("--piid", type=int)
    ap.add_argument("--frame-size", type=int, default=18,
                    help="размер кадра канала (DFU-канал = 18)")
    ap.add_argument("--counter", type=int, default=0, help="app counter")
    ap.add_argument("--op", type=int, default=2, help="байт по смещению 4 (операция)")
    ap.add_argument("--type", type=int, default=0, help="typeCode в объекте")
    ap.add_argument("--props", help='список свойств "siid:piid,siid:piid"')
    a = ap.parse_args()
    if a.props:
        objs = [tuple(int(x) for x in pr.split(":")) for pr in a.props.split(",")]
    elif a.siid and a.piid:
        objs = [(a.siid, a.piid)]
    else:
        objs = DEFAULT_SET
    raise SystemExit(asyncio.run(run(a.mac, objs, a.frame_size, a.counter, a.op, a.type)))
