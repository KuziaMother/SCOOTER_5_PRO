#!/usr/bin/env python3
"""
Эмулятор устройства Dreame/Xiaomi Scooter 5 Pro — сторона УСТРОЙСТВА.

Реализует протокол, реверснутый в проекте (см. docs/FACTS.md):
  - security-chip login (ECDH P-256 + HKDF + AES-CCM, пин через ltmk);
  - канальный транспорт CTR/DATA/ACK (login-каналы 3/5, DFU-канал 0);
  - DFU BLE (opcode 2/3/4) и MCU (opcode 2/5/6): fragmentSize=512, кадры,
    lastFragmentIndex, CRC32, switchFirmware с версионным гейтом;
  - инфо-канал 0x001c (опкоды 0/1/3/8);
  - spec-канал 0x001a/0x001b (телеметрия) — базовый ответ.

Класс без BLE: on_write(sid, data) -> список (sid, notify_bytes).
BLE-обёртка — в fake_ble.py. Это НЕ прошивка, а модель поведения для тестов
наших же инструментов (dreame_auth.py / dreame_flasher.py) без железа.
"""
import os
import struct
import sys
import zlib

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.join(_ROOT, "core"))

import dreame_auth as da
from cryptography.hazmat.primitives.ciphers.aead import AESCCM

# sid каналов
CH_CONTROL = 0x0010
CH_LOGIN = 0x0016
CH_DFU_CMD = 0x0017
CH_DFU_DATA = 0x0018
CH_SPEC_WRITE = 0x001A
CH_SPEC_NOTIFY = 0x001B
CH_INFO = 0x001C
CH_VERSION = 0x0004

# типы канальных пакетов
PKT_CTR, PKT_ACK, PKT_SINGLE, PKT_SINGLE_ACK, PKT_MNG, PKT_MNG_ACK = range(6)

FRAGMENT_SIZE = 512
PKG_NUM = 6
DMTU = 242
SPEC_CHANNEL = 0            # подтверждено снупом (probes/spec_read.py)
SPEC_FRAME_SIZE = 18        # frameSize канала фиксирован устройством
STATUS_NO_DATA = (0x10000 - 4003) & 0xFFFF   # -4003 как u16 (61533), см. docs/FACTS.md

# Телеметрия для эмуляции spec-канала (0x001a/0x001b) — публичные значения из
# живого прогона (README.md/docs/FACTS.md), НЕ секреты (OOB_CODE/SN исключены).
# (siid, piid): (type_code, value)  — типы см. probes/spec_read.py TYPES.
SPEC_TELEMETRY = {
    (1, 1): (1, 2),          # RIDING_MODE: 2=стандарт(D)
    (1, 2): (1, 100),        # BATTERY_LEVEL: 100%
    (1, 3): (3, 9700),       # REMAINING_BATTERY: raw (единицы не установлены)
    (1, 4): (3, 5344),       # VOLTAGE: 53.44 В (raw*0.01)
    (1, 5): (3, 0),          # CURRENT: 0 А (не в движении)
    (1, 6): (3, 0),          # POWER: 0 Вт
    (1, 7): (3, 6050),       # REMAINING_MILEAGE: 60.50 км (raw*0.01)
    (1, 8): (1, 0),          # FAULT: 0
    (1, 9): (3, 440),        # CURRENT_MILEAGE: 4.40 км (raw*0.01)
    (2, 1): (9, 0.0),        # AVERAGE_SPEED: 0.0 км/ч (raw*0.01)
    (2, 2): (0, 0),          # IS_LOCKED
    (2, 3): (0, 0),          # CRUISE_IS_ON
    (2, 4): (0, 0),          # TAIL_LIGHT_IS_ON
    (2, 5): (0, 0),          # ENERGY_RECOVERY
    (2, 6): (3, 440),        # TOTAL_MILEAGE: 4.40 км
    (2, 7): (1, 0),          # IS_RIDING: 0
    (2, 8): (5, 0),          # RIDING_TIME: 0 с
    (2, 9): (9, 0.0),        # HIGHEST_SPEED: 0.0 км/ч
    (2, 10): (0, 1),         # ASR_IS_ON
    (3, 1): (1, 1),          # BATTERY_STATUS: 1=норма
    (3, 2): (2, 25),         # BATTERY_TEMPERATURE: 25 °C
    (3, 3): (2, 25),         # SCOOTER_TEMPERATURE: 25 °C
    (3, 10): (0, 0),         # IS_CHARGING
    (3, 11): (3, 0),         # NUMBER_OF_CYCLES
    (3, 12): (1, 100),       # SOH: 100%
    # (4, 5) FIRMWARE_VERSION собирается динамически из self.ble_version/mcu_version
}

# Свойства, на которые подписывается плагин (modules/10013.js parseNotifyData) —
# те же 20, что в probes/spec_listen.py SUBSCRIBABLE. Пуш идёт ТОЛЬКО по ним.
SUBSCRIBABLE = {
    (1, 1), (1, 2), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
    (2, 1), (2, 7), (2, 13), (2, 14), (2, 15), (2, 16), (2, 17), (2, 18),
    (3, 1), (3, 2), (3, 4), (3, 10),
}


def spec_counter_bytes(cnt):
    low, high = cnt & 0xFFFF, (cnt >> 16) & 0xFFFF
    return bytes([low & 0xFF, low >> 8, high & 0xFF, high >> 8])


def spec_encode_value(tcode, val):
    if tcode == 0 or tcode == 1 or tcode == 2:      # BOOL/UINT8/INT8
        return struct.pack("<b" if tcode == 2 else "<B", val)
    if tcode == 3:
        return struct.pack("<H", val & 0xFFFF)
    if tcode == 4:
        return struct.pack("<h", val)
    if tcode == 5:
        return struct.pack("<I", val & 0xFFFFFFFF)
    if tcode == 6:
        return struct.pack("<i", val)
    if tcode == 9:
        return struct.pack("<f", float(val))
    if tcode == 10:
        return val.encode("utf-8")
    return struct.pack("<I", val & 0xFFFFFFFF)


def ver_tuple(v):
    """'2.7.0_0015' -> кортеж для сравнения; '0007' -> (7,)."""
    v = v.replace("_", ".")
    out = []
    for part in v.split("."):
        try:
            out.append(int(part))
        except ValueError:
            out.append(0)
    return tuple(out)


class ChannelReassembler:
    """Сборка канального сообщения: CTR(fc) -> DATA×fc -> готово."""
    def __init__(self):
        self.reset()

    def reset(self):
        self.channel = None
        self.fc = None
        self.frames = {}

    def start(self, channel, fc):
        self.channel = channel
        self.fc = fc
        self.frames = {}

    def add(self, seq, chunk):
        self.frames[seq] = chunk

    def complete(self):
        return self.fc is not None and len(self.frames) >= self.fc

    def missing(self):
        if self.fc is None:
            return []
        return [i for i in range(1, self.fc + 1) if i not in self.frames]

    def assemble(self):
        return b"".join(self.frames[i] for i in sorted(self.frames))


class ScooterDevice:
    def __init__(self, ltmk, ble_version="2.5.3_0011", mcu_version="0006",
                 serial="60555/EMULATED0001", accept_limit=None, verbose=True):
        self.ltmk = ltmk
        self.ble_version = ble_version
        self.mcu_version = mcu_version
        self.serial = serial
        self.hardware = "RTL8762C"
        self.verbose = verbose
        # accept_limit — сколько фрагментов устройство ЗАСЧИТЫВАЕТ (эмуляция границы
        # 296; None = принимать весь образ). Для демо успешной прошивки — None.
        self.accept_limit = accept_limit

        # login
        self.dev_priv, self.dev_pub = da.gen_ec_keypair()
        self.session_key = None
        self.logged_in = False
        self.login_re = ChannelReassembler()

        # DFU
        self.dfu_re = ChannelReassembler()
        self.ble_buf = bytearray()
        self.ble_last = 0
        self.mcu_buf = bytearray()
        self.mcu_last = 0
        # версия образа, который заливают (устройство «узнаёт» её через harness,
        # т.к. реально она в зашифрованном теле). None = не задано -> считать как same.
        self.offered_ble_version = None
        self.offered_mcu_version = None

        # spec-канал (телеметрия 0x001a/0x001b)
        self.spec_re = ChannelReassembler()
        self.spec_dev_cnt = 0            # счётчик устройства (dev->app AES-CCM nonce)
        self.spec_pending_frames = []    # готовые кадры ответа, ждут ready-ack приложения

        self.log(f"[dev] создан: BLE {ble_version}, MCU {mcu_version}")

    def log(self, *a):
        if self.verbose:
            print(*a)

    # ---------- маршрутизация входящих записей ----------
    def on_write(self, s, data):
        if s == CH_CONTROL:
            return self._on_control(data)
        if s == CH_LOGIN:
            return self._on_login_channel(data)
        if s == CH_DFU_CMD:
            return self._on_dfu_cmd(data)
        if s == CH_DFU_DATA:
            return self._on_dfu_data(data)
        if s == CH_INFO:
            return self._on_info(data)
        if s == CH_SPEC_WRITE:
            return self._on_spec(data)
        if s == CH_SPEC_NOTIFY:
            return self._on_spec_notify_ack(data)
        return []

    def on_read(self, s):
        if s == CH_VERSION:
            return self.ble_version.encode()
        return b""

    # ---------- 0x0010 CONTROL ----------
    def _on_control(self, data):
        if data == bytes([da.A4]):                      # A4 -> MNG на 0x0016
            mng = struct.pack("<HBB", 0, PKT_MNG, 0) + bytes([PKG_NUM, DMTU])
            return [(CH_LOGIN, mng)]
        if len(data) >= 1 and data[0] == 0x20:          # login-start
            self.login_re.reset()
            return []
        return []

    # ---------- 0x0016 login-канал ----------
    def _on_login_channel(self, data):
        if len(data) < 3:
            return []
        seq = struct.unpack_from("<H", data, 0)[0]
        if seq == 0:
            t = data[2]
            if t == PKT_MNG_ACK:
                return []
            if t == PKT_SINGLE_ACK:
                return []
            if t == PKT_CTR:
                channel = data[3]
                fc = struct.unpack_from("<H", data, 4)[0] if len(data) >= 6 else data[4]
                self.login_re.start(channel, fc)
                return [(CH_LOGIN, struct.pack("<HBB", 0, PKT_ACK, 1))]     # готов
            return []
        # DATA-кадр
        self.login_re.add(seq, data[2:])
        if not self.login_re.complete():
            return []
        payload = self.login_re.assemble()
        channel = self.login_re.channel
        out = [(CH_LOGIN, struct.pack("<HBB", 0, PKT_ACK, 0))]              # принято
        if channel == 3:
            out += self._login_stage_a(payload)
        elif channel == 5:
            out += self._login_stage_b(payload)
        return out

    def _login_stage_a(self, app_pub_raw):
        """Получили pubkey приложения -> считаем sessionKey, шлём свой pubkey."""
        try:
            _, sk = da.derive_session_key(self.dev_priv, app_pub_raw, self.ltmk)
            self.session_key = sk
            self.log(f"[dev] Stage A: sessionKey[:8]={sk[:8].hex()}")
        except Exception as e:
            self.log(f"[dev] Stage A ошибка ECDH: {e}")
            return []
        single = struct.pack("<HBB", 0, PKT_SINGLE, 3) + self.dev_pub
        return [(CH_LOGIN, single)]

    def _login_stage_b(self, enc):
        """Проверяем app-confirmation, отвечаем 0x21/0x22 на 0x0010."""
        if not self.session_key:
            return [(CH_CONTROL, b"\x22\x00\x00\x00")]
        aes_key = self.session_key[16:32]
        try:
            pt = AESCCM(aes_key, tag_length=4).decrypt(da.CCM_NONCE, enc, None)
        except Exception as e:
            self.log(f"[dev] Stage B: дешифровка не удалась: {e}")
            return [(CH_CONTROL, b"\x22\x00\x00\x00")]
        expect = struct.pack("<I", zlib.crc32(self.dev_pub) & 0xFFFFFFFF)
        if pt == expect:
            self.logged_in = True
            self.log("[dev] Stage B: LOGIN OK -> 0x21")
            return [(CH_CONTROL, b"\x21\x00\x00\x00")]
        self.log(f"[dev] Stage B: CRC не совпал ({pt.hex()} != {expect.hex()}) -> 0x22")
        return [(CH_CONTROL, b"\x22\x00\x00\x00")]

    # ---------- 0x0017 DFU-команды ----------
    def _cmd_resp(self, opcode, status, data=b""):
        body = struct.pack("<H", opcode) + bytes([status]) + data
        return [(CH_DFU_CMD, bytes([0x01, len(body)]) + body)]

    def _on_dfu_cmd(self, data):
        if len(data) < 3:
            return []
        opcode = struct.unpack_from("<H", data, 0)[0]
        if opcode == 2:                                  # getFragmentSize
            return self._cmd_resp(2, 0, struct.pack("<H", FRAGMENT_SIZE))
        if opcode == 3:                                  # lastFragmentIndex BLE
            crc = zlib.crc32(self.ble_buf) & 0xFFFFFFFF if self.ble_buf else 0
            return self._cmd_resp(3, 0, struct.pack("<HI", self.ble_last, crc))
        if opcode == 5:                                  # lastFragmentIndex MCU
            crc = zlib.crc32(self.mcu_buf) & 0xFFFFFFFF if self.mcu_buf else 0
            return self._cmd_resp(5, 0, struct.pack("<HI", self.mcu_last, crc))
        if opcode == 4:                                  # switchFirmware BLE
            return self._switch("ble")
        if opcode == 6:                                  # switchFirmware MCU
            return self._switch("mcu")
        return self._cmd_resp(opcode, 2)                 # неизвестный опкод

    def _switch(self, target):
        installed = self.ble_version if target == "ble" else self.mcu_version
        offered = (self.offered_ble_version if target == "ble"
                   else self.offered_mcu_version) or installed
        buf = self.ble_buf if target == "ble" else self.mcu_buf
        opcode = 4 if target == "ble" else 6
        reject_status = 6 if target == "ble" else 5

        newer = ver_tuple(offered) > ver_tuple(installed)
        complete = len(buf) > 0
        if newer and complete:
            # применяем: версия обновляется, буфер сбрасывается
            if target == "ble":
                self.ble_version = offered
                self.ble_buf = bytearray()
                self.ble_last = 0
            else:
                self.mcu_version = offered
                self.mcu_buf = bytearray()
                self.mcu_last = 0
            self.log(f"[dev] switchFirmware {target}: ПРИМЕНЕНО -> {offered}")
            return self._cmd_resp(opcode, 0)
        # отказ + сброс буфера (как на реальном устройстве)
        if target == "ble":
            self.ble_buf = bytearray(); self.ble_last = 0
        else:
            self.mcu_buf = bytearray(); self.mcu_last = 0
        why = "та же/старая версия" if not newer else "образ неполон"
        self.log(f"[dev] switchFirmware {target}: ОТКАЗ status={reject_status} ({why}), буфер сброшен")
        return self._cmd_resp(opcode, reject_status)

    # ---------- 0x0018 DFU-данные ----------
    def _on_dfu_data(self, data):
        if len(data) < 3:
            return []
        seq = struct.unpack_from("<H", data, 0)[0]
        if seq == 0 and data[2] == PKT_CTR:
            fc = struct.unpack_from("<H", data, 4)[0] if len(data) >= 6 else data[4]
            self.dfu_re.start(0, fc)
            return [(CH_DFU_DATA, struct.pack("<HBB", 0, PKT_ACK, 1))]
        if seq == 0:
            return []
        # DATA-кадр фрагмента
        self.dfu_re.add(seq, data[2:])
        if not self.dfu_re.complete():
            miss = self.dfu_re.missing()
            if miss:                                     # pull первого недостающего
                return [(CH_DFU_DATA, struct.pack("<HBBH", 0, PKT_ACK, 5, miss[0]))]
            return []
        msg = self.dfu_re.assemble()
        self.dfu_re.reset()
        return self._accept_fragment(msg)

    def _accept_fragment(self, msg):
        """msg = [index u16][fragmentData]. Определяем BLE/MCU по контексту нельзя,
        поэтому эмулятор ведёт ОБА буфера синхронно по индексу текущей заливки.
        Для простоты решаем по тому, какой буфер сейчас «в игре» — трекаем через
        last-команду. Здесь используем эвристику: тот буфер, чей ожидаемый индекс
        совпадает. Практически заливка идёт по одному target за прогон."""
        index = struct.unpack_from("<H", msg, 0)[0]
        frag = msg[2:]
        out_ack = [(CH_DFU_DATA, struct.pack("<HBB", 0, PKT_ACK, 0))]      # транспорт принял

        # выбираем целевой буфер: тот, чей last+1 == index
        if self.ble_last + 1 == index:
            target = "ble"
        elif self.mcu_last + 1 == index:
            target = "mcu"
        else:
            target = "ble" if index > self.mcu_last else "mcu"

        if target == "ble":
            last, buf = self.ble_last, self.ble_buf
        else:
            last, buf = self.mcu_last, self.mcu_buf

        status = 0
        if index == last + 1:
            over_limit = (self.accept_limit is not None and index > self.accept_limit)
            if not over_limit:
                buf.extend(frag)
                if target == "ble":
                    self.ble_last = index
                else:
                    self.mcu_last = index
            # если over_limit — транспорт принял (status 0 в событии), но счётчик не двигаем
        else:
            status = 0                                    # дубликат/резюме — тоже 0
        event = (CH_DFU_CMD, bytes([0x02, 0x03, status]) + struct.pack("<H", index))
        return out_ack + [event]

    # ---------- 0x001c инфо-канал ----------
    def _on_info(self, data):
        if len(data) < 1:
            return []
        op = data[0]
        def frame(op, val):
            return [(CH_INFO, bytes([op, len(val)]) + val)]
        if op == 0:
            return frame(0, b"\x01\x03")
        if op == 1:
            return frame(1, self.mcu_version.encode())
        if op == 3:
            return frame(3, self.hardware.encode())
        if op == 8:
            offset = data[2] if len(data) >= 3 else 0
            chunk = self.serial.encode()[offset:offset + 16]
            if not chunk:
                return [(CH_INFO, bytes([0xFF, 2, 8, 8]))]
            return frame(8, chunk)
        return [(CH_INFO, bytes([0xFF, 2, op, 2]))]       # нет такого опкода

    # ---------- 0x001a spec write (запрос телеметрии от приложения) ----------
    def _on_spec(self, data):
        if len(data) < 3:
            return []
        seq = struct.unpack_from("<H", data, 0)[0]
        if seq == 0 and data[2] == PKT_CTR:
            fc = struct.unpack_from("<H", data, 4)[0] if len(data) >= 6 else data[4]
            self.spec_re.start(data[3] if len(data) >= 4 else SPEC_CHANNEL, fc)
            return [(CH_SPEC_WRITE, struct.pack("<HBB", 0, PKT_ACK, 1))]     # готов принимать
        if seq == 0:
            return []
        self.spec_re.add(seq, data[2:])
        if not self.spec_re.complete():
            return []
        payload = self.spec_re.assemble()
        self.spec_re.reset()
        out = [(CH_SPEC_WRITE, struct.pack("<HBB", 0, PKT_ACK, 0))]          # сообщение принято

        try:
            app_cnt = struct.unpack_from("<H", payload, 0)[0]
            ct = payload[2:]
            nonce = self.session_key[36:40] + b"\x00\x00\x00\x00" + spec_counter_bytes(app_cnt)
            pt = AESCCM(self.session_key[16:32], tag_length=4).decrypt(nonce, ct, None)
        except Exception as e:
            self.log(f"[dev] spec: запрос не расшифровался: {e}")
            return out

        objects = self._parse_spec_request(pt)
        if objects is None:
            return out
        resp_pt = self._build_spec_response(objects)
        resp_ct = self._encrypt_spec_response(resp_pt)
        frames = [resp_ct[i:i + SPEC_FRAME_SIZE] for i in range(0, len(resp_ct), SPEC_FRAME_SIZE)] or [b""]
        self.spec_pending_frames = frames
        self.log(f"[dev] spec: запрошено {len(objects)} объект(ов), ответ {len(resp_ct)}Б -> {len(frames)} кадр(ов)")
        ctr = struct.pack("<HBBH", 0, 0x00, SPEC_CHANNEL, len(frames))
        out.append((CH_SPEC_NOTIFY, ctr))
        return out

    def _parse_spec_request(self, pt):
        """[u16 len|flag][u16 tid][u8 op][u8 count] + [u8 siid][u16 piid][u16 typeLen]..."""
        if len(pt) < 6:
            return None
        _lenflag, _tid, _op, count = struct.unpack_from("<HHBB", pt, 0)
        objects = []
        off = 6
        for _ in range(count):
            if off + 5 > len(pt):
                break
            siid, piid, _tl = struct.unpack_from("<BHH", pt, off)
            objects.append((siid, piid))
            off += 5
        return objects

    def _build_spec_response(self, objects):
        """Устройство обслуживает ТОЛЬКО первый объект в запросе (подтверждено снупом,
        см. docs/FACTS.md) — остальным, как и неизвестным siid/piid, ставит
        status=-4003 (multi-object/нет данных) и пустое значение."""
        body = b""
        for i, (siid, piid) in enumerate(objects):
            tcode, vbytes, status = 0, b"", STATUS_NO_DATA
            if i == 0:
                if (siid, piid) in SPEC_TELEMETRY:
                    tcode, val = SPEC_TELEMETRY[(siid, piid)]
                    vbytes, status = spec_encode_value(tcode, val), 0
                elif (siid, piid) == (4, 5):
                    tcode = 10
                    vbytes = f"{self.ble_version}.{self.mcu_version}".encode()
                    status = 0
            body += struct.pack("<BHHH", siid & 0xFF, piid & 0xFFFF, status & 0xFFFF,
                                 ((tcode & 0xF) << 12) | len(vbytes)) + vbytes
        total = 6 + len(body)
        return struct.pack("<HHBB", (total | 0x2000) & 0xFFFF, 1, 3, len(objects)) + body

    def _encrypt_spec_response(self, pt):
        self.spec_dev_cnt = (self.spec_dev_cnt + 1) & 0xFFFFFFFF
        nonce = self.session_key[32:36] + b"\x00\x00\x00\x00" + spec_counter_bytes(self.spec_dev_cnt)
        ct = AESCCM(self.session_key[0:16], tag_length=4).encrypt(nonce, pt, None)
        return struct.pack("<H", self.spec_dev_cnt & 0xFFFF) + ct

    # ---------- 0x001b spec notify (ack'и приложения на CTR/DATA устройства) ----------
    def _on_spec_notify_ack(self, data):
        if len(data) < 4 or not (data[0] == 0 and data[1] == 0 and data[2] == PKT_ACK):
            return []
        status = data[3]
        if status == 0x01 and self.spec_pending_frames:      # приложение готово принимать
            frames = self.spec_pending_frames
            out = [(CH_SPEC_NOTIFY, struct.pack("<H", n) + frames[n - 1])
                   for n in range(1, len(frames) + 1)]
            return out
        if status == 0x00:                                    # приложение подтвердило приём
            self.spec_pending_frames = []
        return []

    # ---------- пуш при изменении свойства (parseNotifyData) ----------
    def push_property(self, siid, piid, value):
        """Эмуляция спонтанного пуша: устройство САМО отправляет изменившееся
        свойство на 0x001b, без предшествующего запроса на 0x001a (см.
        docs/FACTS.md «Устройство умеет ПУШИТЬ», probes/spec_listen.py).
        Пуш идёт только по свойствам из SUBSCRIBABLE — иначе тихо игнорируется
        (как и на живом устройстве, которое не подписывает остальные siid/piid).
        Возвращает [] или [(CH_SPEC_NOTIFY, ctr_bytes)] — CTR той же формы, что
        и ответ на чтение; дальше цикл ready-ack/DATA/done-ack идёт через уже
        существующий _on_spec_notify_ack, независимо от того, что его начало."""
        if (siid, piid) not in SUBSCRIBABLE:
            return []
        if not self.session_key:
            return []
        tcode = SPEC_TELEMETRY.get((siid, piid), (0, 0))[0]
        SPEC_TELEMETRY[(siid, piid)] = (tcode, value)
        resp_pt = self._build_spec_response([(siid, piid)])
        resp_ct = self._encrypt_spec_response(resp_pt)
        frames = [resp_ct[i:i + SPEC_FRAME_SIZE] for i in range(0, len(resp_ct), SPEC_FRAME_SIZE)] or [b""]
        self.spec_pending_frames = frames
        self.log(f"[dev] push: {('siid=%d piid=%d' % (siid, piid))} -> {value} "
                 f"({len(frames)} кадр(ов))")
        ctr = struct.pack("<HBBH", 0, 0x00, SPEC_CHANNEL, len(frames))
        return [(CH_SPEC_NOTIFY, ctr)]
