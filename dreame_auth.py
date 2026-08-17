#!/usr/bin/env python3
LAST_SK=None
"""
Dreame Scooter 5 Pro — security-chip login, ЭТАП A (проба транспорта).
======================================================================

Цель этапа A: поднять канальный транспорт (A4 → MNG) на FE95/0x0016,
подписаться на notify, отправить кандидаты первой login-команды и
залогировать ЛЮБУЮ реакцию устройства. Ничего во flash не пишется.

Транспорт (из DEX-анализа, раздел 3 docs/dreame_dfu_protocol.md), little-endian:
    A4:        write 0xA4 -> 0x0010; устройство отвечает MNG на 0x0016
    MNG:       [seq=0000][04][subtype][maxPkgNum][maxDMTU]
    MNG_ACK:   [seq=0000][05][subtype][maxPkgNum][maxDMTU]
    SINGLE:    [seq=0000][02][channel][data...]
    CTR:       [seq=0000][00][subtype][frameCount u16]
    DATA:      [seq u16>=1][payload...]
    ACK:       [seq=0000][01][status][seq u16...]

Использование:
    python dreame_auth.py [MAC]
"""

import os
import sys
import asyncio
import struct
import zlib
import json
from bleak import BleakClient

BASE = os.path.dirname(os.path.abspath(__file__))   # корень проекта
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.ciphers.aead import AESCCM

MAC_DEFAULT = "2C:19:5C:DE:DE:88"

CH_CONTROL = 0x0010     # A4, прямые login-команды
CH_LOGIN   = 0x0016     # канальный notify/data для login (securitychipauth)
CH_MCU     = 0x001C

A4 = 0xA4
PKT_CTR, PKT_ACK, PKT_SINGLE, PKT_SINGLE_ACK, PKT_MNG, PKT_MNG_ACK = range(6)
PKT_NAMES = {0: "CTR", 1: "ACK", 2: "SINGLE", 3: "SINGLE_ACK", 4: "MNG", 5: "MNG_ACK"}


def sid(ch_or_uuid):
    u = str(getattr(ch_or_uuid, "uuid", ch_or_uuid)).replace("-", "")
    return int(u[:8], 16) & 0xFFFF


def gen_ec_keypair():
    """P-256 пара. Возвращает (priv, raw_pub 64 байта X||Y без 0x04)."""
    priv = ec.generate_private_key(ec.SECP256R1())
    raw = priv.public_key().public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)
    return priv, raw[1:]          # обрезаем 0x04, как getRawPublicKey в APK


def decode(data: bytes) -> str:
    if len(data) < 3:
        return f"raw={data.hex()}"
    seq = struct.unpack_from("<H", data, 0)[0]
    if seq != 0:
        return f"DATA seq={seq} payload={data[2:].hex()}"
    t = data[2]
    name = PKT_NAMES.get(t, f"type{t}")
    return f"{name} rest={data[3:].hex()}"


class Transport:
    def __init__(self, mac):
        self.mac = mac
        self.client = None
        self.chars = {}
        self.rx = asyncio.Queue()          # (sid, bytes)
        self.last_ctrl = None              # последний ответ на 0x0010 (login result)
        self.dmtu = 242
        self.pkg_num = 6

    async def connect(self):
        self.client = BleakClient(self.mac, timeout=20.0)
        await self.client.connect()
        fe95 = next(s for s in self.client.services
                    if "fe95" in str(s.uuid).replace("-", "").lower())
        self.chars = {sid(c): c for c in fe95.characteristics}
        print(f"[+] connected mtu={self.client.mtu_size} "
              f"chars={[f'0x{k:04x}' for k in sorted(self.chars)]}")
        for s, c in sorted(self.chars.items()):
            props = {str(p).lower() for p in c.properties}
            if "notify" in props or "indicate" in props:
                try:
                    await self.client.start_notify(c, self._on_notify)
                except Exception as e:
                    print(f"    [notify fail 0x{s:04x}] {e}")

    def _on_notify(self, sender, data):
        s = sid(sender)
        b = bytes(data)
        if s == CH_CONTROL:
            self.last_ctrl = b             # login-result (0x21 ok / 0x22 fail)
        self.rx.put_nowait((s, b))
        print(f"    <<< 0x{s:04x} {b.hex():<30} [{decode(b)}]")

    async def write(self, ch_sid, data, response=False):
        await self.client.write_gatt_char(self.chars[ch_sid], data, response=response)

    async def drain(self, timeout=2.5):
        """Собрать все notify в течение окна тишины."""
        out = []
        try:
            while True:
                out.append(await asyncio.wait_for(self.rx.get(), timeout=timeout))
        except asyncio.TimeoutError:
            pass
        return out

    async def a4_handshake(self):
        print("\n=== A4 handshake ===")
        while not self.rx.empty():
            self.rx.get_nowait()
        await self.write(CH_CONTROL, bytes([A4]))
        for s, b in await self.drain(3.0):
            if len(b) >= 6 and b[0] == 0 and b[1] == 0 and b[2] == PKT_MNG:
                self.pkg_num, self.dmtu = b[4], b[5]
                print(f"    MNG: maxPackageNum={self.pkg_num} maxDMTU={self.dmtu}")
                # ответить MNG_ACK на 0x0016
                ack = struct.pack("<HBB", 0, PKT_MNG_ACK, b[3]) + bytes([self.pkg_num, self.dmtu])
                await self.write(CH_LOGIN, ack)
                print(f"    >>> 0x0016 MNG_ACK {ack.hex()}")
                await self.drain(1.0)
                return True
        print("    [!] MNG не получен")
        return False

    async def send_stream(self, channel, payload, timeout=4.0, char=CH_LOGIN, crc=False,
                          resp_data=False, chunk=None):
        """
        Отправка сообщения как отправитель (по snoop телефона):
            CTR [00 00][00][channel][fc u16] -> ждём ACK -> DATA×fc -> ждём ACK
        char — характеристика канала (0x0016 login / 0x0018 dfu).
        crc=True — добавить CRC32(payload) LE в конец (useCrc32Verify канала DFU;
            подтверждено реверсом vw1.OooOO0o + z81/k81).
        chunk — размер данных в DATA-кадре. ВАЖНО: устройство собирает сообщение по
            смещению seq*chunk, поэтому chunk обязан совпадать с frameSize канала
            (DFU=242), иначе reassembly сдвигается и CRC не сходится -> NAK 05.
        resp_data=True — DATA-кадры Write-With-Response.
        """
        if crc:
            payload = payload + struct.pack("<I", zlib.crc32(payload) & 0xFFFFFFFF)
        if chunk is None:
            chunk = self.dmtu - 2  # кадр = [seq u16][chunk] должен влезать в dmtu
        frames = [payload[i:i+chunk] for i in range(0, len(payload), chunk)] or [b""]
        fc = len(frames)
        ctr = struct.pack("<HBBH", 0, PKT_CTR, channel, fc)
        while not self.rx.empty():
            self.rx.get_nowait()
        await self.write(char, ctr)
        st = await self._wait_ack_status(timeout, char)
        if st is None:
            print("    [!] нет start-ACK на CTR"); return False

        async def send_frames(seqs):
            for i in seqs:
                dp = struct.pack("<H", i) + frames[i - 1]
                await self.write(char, dp, response=resp_data)
                if not resp_data:
                    await asyncio.sleep(0.02)  # пейсинг W/O-RESP, чтобы не терять фреймы

        await send_frames(range(1, fc + 1))
        # reliable-цикл: 00=готово, 05=resend списка seq, иное — ждём дальше
        for _ in range(40):
            st, seqs = await self._wait_ack_full(timeout, char)
            if st is None:
                print("    [!] нет ACK после DATA"); return False
            if st == 0x00:
                return True
            if st == 0x05 and seqs:
                await send_frames(seqs)
            # прочие статусы (03 и т.п.) — просто ждём следующий
        print("    [!] reliable-цикл не завершился (много resend)"); return False

    async def _wait_ack(self, timeout, char=CH_LOGIN):
        return (await self._wait_ack_status(timeout, char)) is not None

    async def _wait_ack_status(self, timeout, char=CH_LOGIN):
        st, _ = await self._wait_ack_full(timeout, char)
        return st

    async def _wait_ack_full(self, timeout, char=CH_LOGIN):
        """Ждёт ACK на char. Возвращает (status, [seq...]) или (None, []).
        ACK = [00 00][01][status][seq u16...]."""
        loop = asyncio.get_event_loop()
        deadline = loop.time() + timeout
        while loop.time() < deadline:
            try:
                s, b = await asyncio.wait_for(self.rx.get(), timeout=deadline - loop.time())
            except asyncio.TimeoutError:
                return None, []
            if s == char and len(b) >= 4 and b[0] == 0 and b[1] == 0 and b[2] == PKT_ACK:
                status = b[3]
                seqs = [struct.unpack_from("<H", b, 4 + i)[0] for i in range(0, len(b) - 4, 2)]
                return status, seqs
        return None, []

    async def recv_message_v2(self, timeout=6.0, char=CH_LOGIN):
        """Приём сообщения. char — sid или кортеж sid'ов (напр. пара write/notify)."""
        chars = char if isinstance(char, (tuple, list, set)) else (char,)
        ack_char = chars[0]
        loop = asyncio.get_event_loop()
        deadline = loop.time() + timeout
        fc = None
        frames = {}
        while loop.time() < deadline:
            try:
                s, b = await asyncio.wait_for(self.rx.get(), timeout=deadline - loop.time())
            except asyncio.TimeoutError:
                break
            if s not in chars or len(b) < 3:
                continue
            char = ack_char
            seq = struct.unpack_from("<H", b, 0)[0]
            if seq == 0:
                t = b[2]
                if t == PKT_SINGLE:
                    data = b[4:]
                    await self.write(char, struct.pack("<HBB", 0, PKT_SINGLE_ACK, 0))
                    print(f"    <<< SINGLE ch={b[3]} ({len(data)}B) -> SINGLE_ACK")
                    return data
                if t == PKT_CTR:
                    fc = struct.unpack_from("<H", b, 4)[0] if len(b) >= 6 else b[4]
                    await self.write(char, struct.pack("<HBB", 0, PKT_ACK, 1))
                    print(f"    <<< CTR fc={fc} -> start-ACK(01)")
            else:
                frames[seq] = b[2:]
                print(f"    <<< DATA seq={seq} ({len(b)-2}B)")
                if fc and len(frames) >= fc:
                    await self.write(char, struct.pack("<HBB", 0, PKT_ACK, 0))
                    break
        if frames:
            return b"".join(frames[i] for i in sorted(frames))
        return None

    async def recv_message(self, timeout=6.0):
        """
        Приём канального сообщения: CTR(frameCount) -> N DATA(seq) -> ACK.
        Возвращает склеенный payload (без seq-заголовков) или None.
        Также обрабатывает одиночный SINGLE.
        """
        frame_count = None
        frames = {}
        loop = asyncio.get_event_loop()
        deadline = loop.time() + timeout
        while True:
            rem = deadline - loop.time()
            if rem <= 0:
                break
            try:
                s, b = await asyncio.wait_for(self.rx.get(), timeout=rem)
            except asyncio.TimeoutError:
                break
            if s != CH_LOGIN or len(b) < 3:
                continue
            seq = struct.unpack_from("<H", b, 0)[0]
            if seq == 0:
                t = b[2]
                if t == PKT_CTR:
                    # [00 00 00 subtype frameCount u16]
                    frame_count = struct.unpack_from("<H", b, 4)[0] if len(b) >= 6 else b[4]
                    frames = {}
                    print(f"    [recv] CTR frameCount={frame_count}")
                elif t == PKT_SINGLE:
                    # одиночный: [00 00 02 channel data]
                    print(f"    [recv] SINGLE ch={b[3]} data={b[4:].hex()}")
                    return b[4:]
                elif t == PKT_MNG:
                    print(f"    [recv] MNG {b[3:].hex()}")
                # прочие служебные игнорируем
            else:
                frames[seq] = b[2:]
                if frame_count and len(frames) >= frame_count:
                    break

        if not frames:
            return None
        payload = b"".join(frames[i] for i in sorted(frames))
        # ACK: [00 00 01 status=00] + список принятых seq
        seqs = b"".join(struct.pack("<H", i) for i in sorted(frames))
        ack = struct.pack("<HBB", 0, PKT_ACK, 0) + seqs
        try:
            await self.write(CH_LOGIN, ack)
            print(f"    >>> ACK {ack.hex()}")
        except Exception as e:
            print(f"    [ack fail] {e}")
        return payload

    async def close(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            print("[*] disconnected")


def single_pkt(channel, data):
    """Канальный SINGLE-пакет: [seq=0000][02][channel][data]."""
    return struct.pack("<HBB", 0, PKT_SINGLE, channel) + data


async def stage_a_pubkey_exchange(t: Transport):
    """
    Обмен публичными ключами по реальному потоку из snoop телефона:
        TX 0x0010: 20 00 00              (login-start)
        TX 0x0016: CTR+DATA (наш pubkey, channel=3)
        RX 0x0016: SINGLE (device pubkey) -> SINGLE_ACK
    Возвращает (priv, device_pub_raw) или (priv, None).
    """
    priv, raw_pub = gen_ec_keypair()
    print(f"  app pubkey (raw X||Y, {len(raw_pub)}B): {raw_pub.hex()}")

    # login-start команда 0x20 (3 байта, как в snoop)
    while not t.rx.empty():
        t.rx.get_nowait()
    await t.write(CH_CONTROL, bytes([0x20, 0x00, 0x00]))
    print("  >>> 0x0010: 20 00 00 (login-start)")
    await asyncio.sleep(0.2)

    # наш pubkey потоком CTR+DATA на channel=3
    ok = await t.send_stream(3, raw_pub)
    if not ok:
        print("  [!] отправка pubkey (CTR+DATA) не подтверждена")

    # приём device pubkey
    dev = await t.recv_message_v2(timeout=6.0)
    if dev:
        print(f"\n  [DEVICE PUBKEY] {len(dev)}B: {dev.hex()}")
        return priv, dev
    print("\n  [!] device pubkey не получен")
    return priv, None


LTMK_HEX = os.path.join(BASE, "secrets", "ltmk.hex")


def ltmk_path_for_mac(mac):
    """Путь к LTMK для конкретного MAC — secrets/ltmk_<MAC без ':'>.hex, если
    есть, иначе legacy secrets/ltmk.hex (единственный самокат проекта до
    появления поддержки нескольких профилей)."""
    safe = (mac or "").upper().replace(":", "")
    per_mac = os.path.join(BASE, "secrets", f"ltmk_{safe}.hex")
    return per_mac if os.path.exists(per_mac) else LTMK_HEX


LOGIN_SALT = b"smartcfg-login-salt"
LOGIN_INFO = b"smartcfg-login-info"
CCM_NONCE = bytes(range(0x10, 0x1c))     # 10 11 ... 1b (12 байт)


def derive_session_key(priv, dev_pub_raw, ltmk):
    dev_pub = ec.EllipticCurvePublicKey.from_encoded_point(
        ec.SECP256R1(), b"\x04" + dev_pub_raw)
    shared = priv.exchange(ec.ECDH(), dev_pub)          # 32B X-coord
    keymix = shared + ltmk                              # 64B
    session_key = HKDF(algorithm=SHA256(), length=64,
                       salt=LOGIN_SALT, info=LOGIN_INFO).derive(keymix)
    return shared, session_key


async def stage_b_confirm(t, priv, dev_pub, ltmk, crc_be=False):
    global LAST_SK
    shared, sk = derive_session_key(priv, dev_pub, ltmk)
    LAST_SK = sk
    aes_key = sk[16:32]
    # plaintext = CRC32(device_pubkey) (z81.OooO00o), 4 байта
    crc = zlib.crc32(dev_pub) & 0xFFFFFFFF
    plaintext = struct.pack(">I" if crc_be else "<I", crc)
    print(f"  shared[:8]={shared[:8].hex()} sessionKey[:8]={sk[:8].hex()} aes_key={aes_key.hex()}")
    ccm = AESCCM(aes_key, tag_length=4)
    enc = ccm.encrypt(CCM_NONCE, plaintext, None)       # ciphertext||mac4
    print(f"  confirmation enc ({len(enc)}B): {enc.hex()}  (plaintext={plaintext.hex() or 'empty'})")

    # отправляем app-confirmation потоком на channel=5
    t.last_ctrl = None
    await t.send_stream(5, enc)
    await t.drain(3.0)                    # дать устройству ответить

    res = t.last_ctrl
    print(f"  --- ответ устройства на 0x0010: {res.hex() if res else 'нет'} ---")
    if res and res[:1] == b"\x21":
        return True
    if res and res[:1] == b"\x22":
        return False
    return None


async def collect_info(t, report):
    """Read-only сбор телеметрии. Пишет строки в список report."""
    def line(s):
        print("  " + s); report.append(s)

    # 1. GATT READ характеристики
    line("--- GATT reads ---")
    for sidx, name in ((0x0004, "version"), (0x0005, "0x0005")):
        if sidx in t.chars and "read" in {str(p).lower() for p in t.chars[sidx].properties}:
            try:
                v = await t.client.read_gatt_char(t.chars[sidx])
                txt = v.decode("ascii", "replace").rstrip("\x00")
                line(f"{name} (0x{sidx:04x}): '{txt}'  hex={v.hex()}")
            except Exception as e:
                line(f"{name}: err {e}")

    # 2. MCU-канал 0x001c (без авторизации) — событийный сбор
    line("--- MCU channel 0x001c ---")
    if 0x001C in t.chars:
        results = {}

        def on_c(sender, data):
            if sid(sender) == 0x001C:
                results.setdefault("last", []).append(bytes(data))
        await t.client.start_notify(t.chars[0x001C], on_c)

        async def q(op, param=None):
            results["last"] = []
            fr = bytes([op]) if param is None else bytes([op, len(param)]) + param
            await t.client.write_gatt_char(t.chars[0x001C], fr, response=False)
            await asyncio.sleep(1.2)
            return results["last"][0] if results["last"] else None

        for op, nm in ((1, "mcu_version"), (3, "hardware")):
            r = await q(op)
            if r and r[0] != 0xFF:
                val = r[2:2 + r[1]]
                txt = val.decode("ascii", "replace") if all(32 <= c < 127 for c in val) else val.hex()
                line(f"opcode {op} ({nm}): '{txt}'")
            else:
                line(f"opcode {op} ({nm}): {'err '+hex(r[3]) if r else 'no reply'}")

        # opcode 8 — серийник постранично (offset)
        sn = b""
        offset = 0
        for _ in range(16):
            r = await q(8, bytes([offset & 0xFF]))
            if not r or r[0] == 0xFF:
                break
            chunk = r[2:2 + r[1]]
            if not chunk:
                break
            sn += chunk
            offset += len(chunk)
            if len(chunk) < 16:
                break
        if sn:
            txt = sn.decode("ascii", "replace") if all(32 <= c < 127 for c in sn) else sn.hex()
            line(f"opcode 8 (serial/newSN): '{txt}'")
        try:
            await t.client.stop_notify(t.chars[0x001C])
        except Exception:
            pass

    # 3. DFU командный канал 0x0017 (после login) — только query-опкоды
    line("--- DFU query 0x0017 (после login, read-only) ---")
    if 0x0017 in t.chars:
        for op, nm in ((2, "getFragmentSize"), (3, "lastFragmentIndex(BLE)"),
                       (5, "lastFragmentIndex(MCU)")):
            while not t.rx.empty():
                t.rx.get_nowait()
            cmd = struct.pack("<HB", op, 0)
            try:
                await t.client.write_gatt_char(t.chars[0x0017], cmd, response=True)
            except Exception as e:
                line(f"opcode {op} ({nm}): write err {e}"); continue
            rep = None
            for s, b in await t.drain(2.0):
                if s == 0x0017:
                    rep = b
            line(f"opcode {op} ({nm}): {rep.hex() if rep else 'no reply'}")

    # 4. Свод облачных данных (scooter_keys.json)
    line("--- Cloud (scooter_keys.json) ---")
    try:
        cj = json.load(open(os.path.join(BASE, "secrets", "scooter_keys.json"), encoding="utf-8"))
        dev = cj.get("device", {})
        for k in ("did", "uid", "mac", "model", "name"):
            if k in dev:
                line(f"{k}: {dev[k]}")
        ex = dev.get("extra", {})
        for k in ("fw_version", "mcu_version", "isSetPincode", "pincodeType"):
            if k in ex:
                line(f"extra.{k}: {ex[k]}")
        line(f"server: {cj.get('server')}")
    except Exception as e:
        line(f"cloud read err: {e}")


def ccm_encrypt(sk, counter, plaintext):
    key = sk[16:32]
    nonce = sk[36:40] + b"\x00\x00\x00\x00" + struct.pack("<I", counter)
    return AESCCM(key, tag_length=4).encrypt(nonce, plaintext, None)


def ccm_decrypt(sk, counter, data):
    from cryptography.exceptions import InvalidTag
    key = sk[0:16]
    nonce = sk[32:36] + b"\x00\x00\x00\x00" + struct.pack("<I", counter)
    try:
        return AESCCM(key, tag_length=4).decrypt(nonce, data, None)
    except InvalidTag:
        return None


def spec_get_frame(props, txn=1):
    """MiOT property-get кадр: [len|0x2000 u16][txn u16][00][count][siid u8,piid u16]*."""
    body = b"".join(struct.pack("<BH", s, p) for s, p in props)
    hdr = struct.pack("<HHBB", (len(body) | 0x2000) & 0xFFFF, txn, 0, len(props))
    return hdr + body


async def stage_telemetry(t, sk):
    """
    Чтение MiOT-свойств поверх session-шифрования. Сначала верификация на
    device-info firmware (siid=1,piid=4 → ждём '2.5.3_0011'), затем перебор.
    Пробуем характеристику/канал-байт эмпирически.
    """
    print("\n=== Stage T: telemetry (encrypted MiOT prop-get) ===")
    known = spec_get_frame([(1, 4)], txn=1)   # device-info firmware
    print(f"  plaintext prop-get(siid1,piid4): {known.hex()}")

    # варианты плейнтекст-кадра property-get(siid=1,piid=4)
    body = struct.pack("<BH", 1, 4)
    variants = {
        "len|0x2000,txn1,00": struct.pack("<HHBB", (len(body) | 0x2000) & 0xFFFF, 1, 0, 1) + body,
        "len,txn1,00":        struct.pack("<HHBB", len(body), 1, 0, 1) + body,
        "len|0x2000,txn0,00": struct.pack("<HHBB", (len(body) | 0x2000) & 0xFFFF, 0, 0, 1) + body,
        "raw siid,piid":      body,
    }
    for name, frame in variants.items():
        for ectr in (0, 1):
            enc = ccm_encrypt(sk, ectr, frame)
            print(f"\n  -- variant '{name}' encctr={ectr}: plain={frame.hex()} enc={enc.hex()} --")
            while not t.rx.empty():
                t.rx.get_nowait()
            # CTR ch0 fc1 на 0x001a
            await t.write(0x001A, struct.pack("<HBBH", 0, PKT_CTR, 0, 1))
            await asyncio.sleep(0.15)
            # DATA seq1 (дважды, как телефон)
            await t.write(0x001A, struct.pack("<H", 1) + enc)
            await t.write(0x001A, struct.pack("<H", 1) + enc)
            # слушаем ответ на 0x001a/0x001b
            resp = None
            for s, b in await t.drain(3.0):
                if s == 0x001B or (s == 0x001A and struct.unpack_from("<H", b, 0)[0] != 0):
                    payload = b[4:] if (s == 0x001B and len(b) >= 4 and b[2] == PKT_SINGLE) else b[2:]
                    resp = payload
                    print(f"    <<< ответ 0x{s:04x}: {b.hex()}")
            if not resp:
                continue
            for dctr in (0, 1, ectr):
                dec = ccm_decrypt(sk, dctr, resp)
                if dec is not None:
                    print(f"    *** DECRYPTED devctr={dctr}: {dec.hex()} ***")
                    asc = dec.decode("ascii", "replace")
                    if "2.5.3" in asc:
                        print(f"    [+++] FIRMWARE прочитан — пайплайн работает! variant='{name}'")
                        return name
    print("  [!] property-ответ не получен ни на одном варианте")
    return None


DFU_DO_UPLOAD = False   # health-check; True = проба заливки одного фрагмента
FW_PATH = os.path.join(BASE, "firmware_ota",
                       "0d41b4df91f8d37b5f1355484e2b93c3_upd_xiaomi.scooter.5pro_v2.7.0_0015.bin")
CH_DFU_CMD = 0x0017
CH_DFU_DATA = 0x0018


async def dfu_cmd(t, opcode, params=b""):
    """Команда DFU на 0x0017 (W/RESP), ответ notify [01][len][opcode u16][status][data]."""
    frame = struct.pack("<HB", opcode, len(params)) + params
    while not t.rx.empty():
        t.rx.get_nowait()
    try:
        await t.client.write_gatt_char(t.chars[CH_DFU_CMD], frame, response=True)
    except Exception:
        return None
    for s, b in await t.drain(2.5):
        if s == CH_DFU_CMD and len(b) >= 3 and b[0] == 0x01:
            return b
    return None


def parse_cmd_resp(b):
    """[01][len][opcode u16 LE][... value]. Возвращает (opcode, value_bytes)."""
    if not b or len(b) < 4 or b[0] != 0x01:
        return None, None
    ln = b[1]
    body = b[2:2 + ln]
    opcode = struct.unpack_from("<H", body, 0)[0]
    return opcode, body[2:]


async def stage_d_probe(t):
    """
    БЕЗОПАСНАЯ проба DFU: команды-запросы + загрузка ОДНОГО фрагмента,
    проверка сдвига lastFragmentIndex. switchFirmware НЕ шлём.
    Неудачная загрузка не коммитится устройством — вреда нет.
    """
    print("\n=== Stage D (probe, БЕЗ switchFirmware) ===")
    # 1. getFragmentSize
    r = await dfu_cmd(t, 2)
    op, val = parse_cmd_resp(r)
    frag = struct.unpack_from("<H", val, 1)[0] if val and len(val) >= 3 else None
    print(f"  getFragmentSize: resp={r.hex() if r else None} -> fragmentSize={frag}")
    if frag not in (512, 256, 128, 244):
        print(f"  [!] неожиданный fragmentSize={frag}; прерываю пробу")
        return
    # 2. lastFragmentIndex (до)
    r3 = await dfu_cmd(t, 3)
    r5 = await dfu_cmd(t, 5)
    print(f"  lastFragmentIndex(BLE op3): {r3.hex() if r3 else None}")
    print(f"  lastFragmentIndex(MCU op5): {r5.hex() if r5 else None}")
    try:
        ver = await t.client.read_gatt_char(t.chars[0x0004])
        print(f"  version 0x0004: {ver.decode('ascii','replace').rstrip(chr(0))}")
    except Exception:
        pass

    if not DFU_DO_UPLOAD:
        print("  [read-only] загрузка фрагмента ОТКЛЮЧЕНА — оцениваем состояние ('UP' на экране)")
        return

    # --- индекс из ответа lastFragmentIndex(BLE, op3): value=[status][idx u32 LE...] ---
    _op, lv = parse_cmd_resp(r3)
    last_idx = 0
    if lv and len(lv) >= 5 and lv[0] == 0:
        last_idx = struct.unpack_from("<I", lv, 1)[0]
    # APK: skip = lastIdx*frag; header index = lastIdx+1 (1-based нумерация фрагментов)
    frag_index = last_idx + 1
    skip = last_idx * frag
    print(f"  parsed lastFragmentIndex={last_idx} -> шлём фрагмент index={frag_index}, skip={skip}B")

    # 3. Загрузка фрагмента. Реверс транспорта vw1/ChannelManager:
    #    frameSize(OooOo00)=18 по умолчанию (нет MNG на 0x0018) -> maxPackageNum=1.
    #    => окно = 1 кадр: CTR(fc), затем шлём кадр seq=N, ждём ACK (05 seq=N+1 = «дай след.»),
    #    до status 00. DATA-кадр = [seq u16 LE][18 данных]. CRC (useCrc32Verify) — пробуем оба.
    dfu_ok = False
    for use_crc in (False, True):
        with open(FW_PATH, "rb") as f:
            fw = f.read()
        chunk0 = fw[skip:skip + frag]
        msg = struct.pack("<H", frag_index) + chunk0
        if use_crc:
            msg = msg + struct.pack("<I", zlib.crc32(msg) & 0xFFFFFFFF)
        FS = 18
        dframes = [msg[i:i+FS] for i in range(0, len(msg), FS)]
        fc = len(dframes)
        print(f"\n  [crc={use_crc}] сообщение {len(msg)}B -> {fc} кадров по {FS}Б, CTR fc={fc}")
        await t.drain(1.0)
        ctr = struct.pack("<HBBH", 0, PKT_CTR, 0, fc)
        await t.write(CH_DFU_DATA, ctr)
        st0 = await t._wait_ack_status(3.0, CH_DFU_DATA)
        print(f"    CTR -> start-ACK={st0}")
        if st0 is None:
            continue
        # window=1: шлём seq=1, дальше следуем запрошенному seq
        seq = 1
        ok = False
        max_seq_seen = 0
        for step in range(fc + 40):
            await t.write(CH_DFU_DATA, struct.pack("<H", seq) + dframes[seq - 1], response=False)
            stt, seqs = await t._wait_ack_full(3.0, CH_DFU_DATA)
            if stt == 0x00:
                print(f"    [✓] transport ACK 00 после seq={seq} — канальное сообщение принято!")
                ok = True
                # ловим DFU-событие 0x0017 [02 03 status idx] (в snoop успех = 02 03 00)
                ev_status = None
                for s2, b2 in await t.drain(1.5):
                    if s2 == CH_DFU_CMD and len(b2) >= 3 and b2[0] == 0x02 and b2[1] == 0x03:
                        ev_status = b2[2]
                        print(f"    DFU-событие: {b2.hex()} -> статус фрагмента={ev_status}"
                              f" ({'OK, ЗАЧТЁН' if ev_status == 0 else 'отклонён'})")
                if ev_status == 0:
                    dfu_ok = True
                break
            if stt == 0x05 and seqs:
                nxt = seqs[0]
                if nxt > max_seq_seen:
                    max_seq_seen = nxt
                    if nxt % 20 == 0 or nxt <= 3:
                        print(f"    прогресс: device просит seq={nxt}")
                if not (1 <= nxt <= fc):
                    print(f"    [!] запрошен seq={nxt} вне диапазона 1..{fc}"); break
                seq = nxt
            else:
                print(f"    [!] неожиданный ACK status={stt} seqs={seqs} на seq={seq}"); break
        else:
            print(f"    [!] не завершилось; макс. запрошенный seq={max_seq_seen}")
        if max_seq_seen >= 2 or ok:
            print(f"    >>> ПРОДВИЖЕНИЕ: транспорт принял кадры (макс seq={max_seq_seen}), crc={use_crc}")
        if dfu_ok:
            print(f"    [✓✓] ФРАГМЕНТ ЗАЧТЁН DFU-слоем при crc={use_crc}!")
            break
    if not ok:
        print("  [!] окно=1/frameSize=18 не сошлось — см. лог прогресса")
    # 4. lastFragmentIndex (после) — сдвинулся ли (ретраи: канал занят после burst)
    new_idx = None
    for attempt in range(5):
        await asyncio.sleep(0.6)
        await t.drain(0.4)
        r3b = await dfu_cmd(t, 3)
        _op2, lv2 = parse_cmd_resp(r3b)
        if lv2 and len(lv2) >= 5 and lv2[0] == 0:
            new_idx = struct.unpack_from("<I", lv2, 1)[0]
            print(f"  lastFragmentIndex(BLE) после [try {attempt}]: raw={r3b.hex()} parsed={new_idx}")
            break
        print(f"  lastFragmentIndex(BLE) после [try {attempt}]: raw={r3b.hex() if r3b else None}")
    if new_idx is not None and new_idx > last_idx:
        print("  [✓✓] ИНДЕКС СДВИНУЛСЯ — фрагмент ЗАЧТЁН устройством! Заливка реальна.")
    else:
        print("  [i] индекс не сдвинулся — транспорт принял (ACK 00), но device не зачёл "
              "(вероятно, контент 2.5.3 на 2.7.0 / нужен верный FW_PATH)")


async def stage_c_probe(t):
    """
    Безопасная проверка, что авторизация открыла путь к DFU. Прошивку НЕ пишем.
    По snoop: после login DFU идёт на канале 0x001a. Проверяем:
      - чтение версии 0x0004 (сессия жива);
      - изменился ли Insufficient Authorization на 0x0017 (W/RESP) после login;
      - отвечает ли device на служебный кадр канала 0x001a.
    """
    print("\n=== Stage C: проверка доступа к DFU (без записи flash) ===")
    # версия
    try:
        v = await t.client.read_gatt_char(t.chars[0x0004])
        print(f"  version 0x0004: {v.decode('ascii','replace').rstrip(chr(0))}")
    except Exception as e:
        print(f"  version read err: {e}")

    # проба 0x0017 W/RESP getFragmentSize [opcode=2 u16][len=0]
    if 0x0017 in t.chars:
        cmd = struct.pack("<HB", 2, 0)
        for resp in (True, False):
            try:
                await t.client.write_gatt_char(t.chars[0x0017], cmd, response=resp)
                print(f"  0x0017 W{'/RESP' if resp else '/O'} [{cmd.hex()}]: OK")
                break
            except Exception as e:
                print(f"  0x0017 W{'/RESP' if resp else '/O'}: {e}")

    # служебный кадр на канал 0x001a — оживает ли DFU-канал после login
    if 0x001a in t.chars:
        while not t.rx.empty():
            t.rx.get_nowait()
        # A4-подобный/CTR служебный: пробуем CTR ch=0 fc=0 (безопасно, не данные)
        probe = struct.pack("<HBBH", 0, PKT_CTR, 0, 0)
        try:
            await t.client.write_gatt_char(t.chars[0x001a], probe, response=False)
            print(f"  >>> 0x001a CTR-probe {probe.hex()}")
        except Exception as e:
            print(f"  0x001a write err: {e}")
        got = await t.drain(3.0)
        if got:
            for s, b in got:
                print(f"    <<< 0x{s:04x} {b.hex()}")
        else:
            print("    (0x001a тишина — вероятно нужен зашифрованный сессией кадр, это Stage D)")


async def main():
    mac = sys.argv[1] if len(sys.argv) > 1 else MAC_DEFAULT
    ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
    t = Transport(mac)
    try:
        await t.connect()
        if not await t.a4_handshake():
            print("[!] транспорт не поднялся"); return 1
        # устройство иногда шлёт MNG повторно — подтвердим ещё раз
        for s, b in await t.drain(1.0):
            if s == CH_LOGIN and len(b) >= 3 and b[2] == PKT_MNG:
                await t.write(CH_LOGIN, struct.pack("<HBB", 0, PKT_MNG_ACK, 0) + bytes([t.pkg_num, t.dmtu]))
        print("\n=== Stage A: pubkey exchange ===")
        priv, dev_pub = await stage_a_pubkey_exchange(t)
        if not (dev_pub and len(dev_pub) >= 64):
            return 1
        print("\n[+++] Stage A OK: device pubkey получен!")
        print("\n=== Stage B: confirmation (ltmk pin=[masked], CRC LE) ===")
        ok = await stage_b_confirm(t, priv, dev_pub, ltmk, crc_be=False)
        print(f"\n[Stage B] {'LOGIN OK — пин верный!' if ok else 'отказ (0x22) — CRC byte-order/пин'}")
        if ok:
            await stage_d_probe(t)
            print("\n=== Сбор информации (read-only) ===")
            report = [f"Dreame Scooter 5 Pro — info dump ({mac})"]
            await collect_info(t, report)
            with open(os.path.join(BASE, "docs", "scooter_info.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(report) + "\n")
            print("\n[*] отчёт сохранён: D:\\MIJIA\\scooter_info.txt")
        return 0 if ok else 1
    except Exception:
        import traceback
        traceback.print_exc()
        return 1
    finally:
        await t.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
