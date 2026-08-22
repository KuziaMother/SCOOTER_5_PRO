#!/usr/bin/env python3
"""UART-DFU флешер MCU (протокол bw-flasher, проверен живым MCU 2026-08-21/22).

Фазы: UID → get_ver → rd_info → ble_rand(+сверка sign_rand) → mcu_rand →
mcu_key → [nvm_write + 16×чанк(128Б) + 04 04 04 + wr_info] × N пакетов(0x800) →
**терминирующий пустой пакет** (nvm_write + 04 04 04 + wr_info, без чанков) →
dfu_verify → dfu_active → get_ver.

Референс протокола — настоящий `bw-flasher` (ScooterTeam), чей полный write-флоу
прошёл на живом железе 2026-08-21 (лог: logs/bw_flasher_log.txt). Скрипт повторяет его
последовательность байт-в-байт, включая терминирующий пустой пакет после
последнего реального: стейт-машина референса шлёт его (nvm_write на конце образа,
без чанков, 04 04 04 + ACK, wr_info с НЕИЗМЕННЫМ CRC32 и размером (N+1)×0x800),
и только потом dfu_verify — MCU это принял.

Критичные моменты (живые находки):
  - UID отвечает надёжно ТОЛЬКО если перед сырым кадром `53 2A 7D AC` сначала
    послать `down get_ver\r` и выдержать паузу 0.4 с; голый hex сразу после
    открытия порта может не получить ответа (todo.md §B2).
  - `nvm_write` должен улететь СРАЗУ после `ok` от mcu_key — у MCU короткое
    «окно записи» после аутентификации; задержка ~2 с приводит к молчанию и
    зависанию сессии (лечится только power-cycle).
  - Push-кадры телеметрии (`61 SUB LEN DATA CHK 9E`, CHK = Σ&0xFF, ~2.5 с /
    до непрерывного потока) идут параллельно консоли. Они убираются с
    проверкой CHK; НЕПОЛНЫЙ хвостовой кадр удерживается, а не показывается
    парсеру (иначе 0x06/0x15 внутри push-пейлоада = ложный ACK/CRC-fail).
    Синхронизация постоянная: reset_input_buffer() НЕ используется — он
    рвёт кадр пополам, и «чужая» половина ломает startswith(b"ok").
  - После dfu_active MCU ребутится: get_ver может не отвечать несколько секунд.
    Живой прогон 2026-08-22: «ok» на dfu_active МОЖЕТ потеряться — MCU закоммитил
    активацию и сбросился до ответа. Тогда скрипт делает read-only проверку: версия
    вернулась + rd_info показывает очищенный DFU-регион = активация закоммичена;
    данные в регионе ещё на месте = ABORT «нужен повтор».

Безопасность: до dfu_active любой сбой = ABORT (работающая прошивка не тронута);
чанк без ACK 0x06 ретраится до 20 раз (ретрансмиссии наблюдались в живом успешном
прогоне); ACK 0x15 = CRC-fail → ABORT. Повторы ограничены — устройство не спамим.

Запуск: python tools/mcu_uart_flash.py --port COM3 --fw firmware_ota/<mcu>.bin --md5 <hex>
"""
import argparse
import hashlib
import random
import re
import struct
import sys
import time
import zlib

import serial

from mcu_keygen import sign_rand  # vendored из bw-flasher (CC BY-NC-SA, см. файл)

PACKET_SIZE = 0x800
CHUNK_SIZE = 0x80
CHUNKS_PER_PACKET = PACKET_SIZE // CHUNK_SIZE   # 16
MAX_REPEATS = 20
# Проверенные константы для v0007 (docs/FACTS.md) — FALLBACK; основной путь —
# динамический поиск паттернов в образе (как у bw-flasher).
OFF0_DEFAULT, OFF1_DEFAULT = 0x24187, 0x24387

# версия начинается с цифры (страйные байты при ребуте, напр. 0x43='C', не пропустим)
VER_RE = re.compile(rb"^[0-9]+([._][0-9A-Za-z]+)*$")


def crc16_xmodem(data):
    crc = 0
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}"
          .replace("✓", "OK").replace("…", "..."), flush=True)


class Reader:
    """Порт с постоянной синхронизацией и вырезанием push-кадров `61 SUB LEN DATA CHK 9E`.

    Два буфера: raw (не классифицированные байты) и clean (консольные байты,
    ещё не consumed вызывающим). Полные push-кадры выбрасываются ТОЛЬКО при
    валидном CHK (Σ всех предшествующих байт кадра & 0xFF) и трейлере 0x9E;
    неполный хвостовой кадр удерживается в raw, пока не придёт достаточно
    данных, чтобы его подтвердить/опровергнуть.

    Известное ограничение: если консольный байт (ACK 0x06/0x15) физически
    влезет В СЕРЕДИНУ рваного push-кадра, валидация кадра провалится и все
    эти байты (включая ACK) попадут в clean как данные. В живых захватах
    такого интерливинга не наблюдалось (в фазе записи push-поток молчал,
    см. logs/bw_flasher_log.txt); референс bw-flasher уязвим к тому же сильнее.
    """

    def __init__(self, s):
        self.s = s
        self.raw = bytearray()
        self.clean = bytearray()

    def _pump(self):
        d = self.s.read(256)
        if d:
            self.raw += d
        self._classify()

    def _classify(self):
        """Разделить raw на (выбросить валидные push-кадры) + clean; хвост удержать."""
        out = bytearray()
        i, n = 0, len(self.raw)
        while i < n:
            b = self.raw[i]
            if b == 0x61:
                rem = n - i
                if rem < 3:
                    break  # возможное начало кадра — данных пока мало
                ln = self.raw[i + 2]
                e = i + ln + 5  # индекс сразу после трейлера 9E
                if ln <= 200 and e <= n and self.raw[e - 1] == 0x9E \
                        and (sum(self.raw[i:e - 2]) & 0xFF) == self.raw[e - 2]:
                    i = e       # полный валидный push-кадр — выбросить
                    continue
                if ln <= 200 and e > n:
                    break       # возможный неполный кадр — удержать
            out.append(b)
            i += 1
        del self.raw[:i]
        self.clean += out

    def read_until(self, term, timeout=3.0):
        """Байты до `term` включительно; на таймауте — всё, что есть."""
        end = time.time() + timeout
        while True:
            j = self.clean.find(term)
            if j >= 0:
                d = bytes(self.clean[:j + len(term)])
                del self.clean[:j + len(term)]
                return d
            if time.time() >= end:
                d = bytes(self.clean)
                del self.clean[:]
                return d
            self._pump()

    def drain(self):
        d = bytes(self.clean)
        del self.clean[:]
        return d

    def read_exact(self, n, timeout=3.0):
        """Ровно n байтов (бинарный ответ); на таймауте — сколько накопилось."""
        end = time.time() + timeout
        while len(self.clean) < n and time.time() < end:
            self._pump()
        d = bytes(self.clean[:n])
        del self.clean[:len(d)]
        return d


def cmd(r, payload, label, timeout=3.0, fatal=True):
    """Drain → отправить → ждать строку до \\r. Возвращает строку без \\r (или None)."""
    r.drain()
    r.s.write(payload)
    r.s.flush()
    d = r.read_until(b"\r", timeout=timeout)
    if not d.endswith(b"\r"):
        if not fatal:
            return None
        log(f"RAW {label}: {d[:64].hex(' ')}")
        sys.exit(f"ABORT: {label}: нет ответа (консоль зависла — power-cycle, "
                 f"и пауза ~3 мин перед повторным заходом)")
    line = d.split(b"\r")[0]
    if not line:
        if not fatal:
            return None
        log(f"RAW {label}: {d[:64].hex(' ')}")
        sys.exit(f"ABORT: {label}: пустой ответ")
    return line


def ok_cmd(r, payload, label, timeout=3.0):
    """Команда, отвечающая `ok` (возможно с хвостом)."""
    line = cmd(r, payload, label, timeout)
    if not line.startswith(b"ok"):
        sys.exit(f"ABORT: {label}: неожиданный ответ {line[:24]!r}")
    return line


def find_offsets(fw):
    """Смещения крипто-таблиц в образе (как у bw-flasher).

    S-box — уникальный паттерн `63 7C`; таблица степеней GF(2^8) — первый
    `01 02` после него (off1 = hit - 1). Если паттерны неоднозначны —
    проверенные константы v0007 из docs/FACTS.md.
    """
    hits0, start = [], 0
    while True:
        i = fw.find(b"\x63\x7c", start)
        if i < 0:
            break
        hits0.append(i)
        start = i + 1
    if len(hits0) == 1:
        off0 = hits0[0]
    else:
        off0 = OFF0_DEFAULT
        log(f"ВНИМАНИЕ: паттерн 637C найден {len(hits0)} раз — "
            f"использован проверенный off0=0x{off0:X}")
    hits1, start = [], off0
    while True:
        i = fw.find(b"\x01\x02", start)
        if i < 0:
            break
        hits1.append(i)
        start = i + 1
    if len(hits1) == 1:
        off1 = hits1[0] - 1
    else:
        off1 = OFF1_DEFAULT
        log(f"ВНИМАНИЕ: паттерн 0102 после off0 найден {len(hits1)} раз — "
            f"использован проверенный off1=0x{off1:X}")
    return off0, off1


def get_uid(r):
    """UID с warmup (живая находка 2026-08-21): `down get_ver\r`, пауза 0.4 с, потом hex-кадр."""
    for attempt in range(1, 4):
        r.drain()
        r.s.write(b"down get_ver\r")
        r.s.flush()
        time.sleep(0.4)          # пауза — часть проверенного рецепта
        r.drain()                # съесть ответ "0007\r", если пришёл
        r.s.write(bytes.fromhex("53 2A 7D AC"))
        r.s.flush()
        acc = bytearray()
        end = time.time() + 2.0
        while True:
            # accumulate до трейлера 9B (или таймаут куска); кадр валидируем целиком
            acc += r.read_until(b"\x9b", timeout=max(0.1, end - time.time()))
            i = acc.find(b"\x64\x2a\x10")
            if i >= 0 and i + 21 <= len(acc) and acc[i + 20] == 0x9B \
                    and (sum(acc[i:i + 19]) & 0xFF) == acc[i + 19]:
                return bytes(acc[i + 3:i + 19])
            if time.time() >= end:
                break
        log(f"UID попытка {attempt}/3 — нет ответа")
    sys.exit("ABORT: UID не получен (линия/TX?)")


def get_ver(r, label="get_ver", timeout=3.0, tries=6, fatal=True):
    """`down get_ver` → строка версии; мусорные (push-хвосты) строки переспрашиваются."""
    for _ in range(tries):
        line = cmd(r, b"down get_ver\r", label, timeout, fatal=fatal)
        if line is None:
            continue
        if VER_RE.match(line):
            return line.decode()
        log(f"{label}: шумовая строка {line[:16]!r} — переспрашиваю")
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM3")
    ap.add_argument("--fw", required=True)
    ap.add_argument("--md5", default="", help="ожидаемый MD5 (обязательно для записи)")
    a = ap.parse_args()

    fw = open(a.fw, "rb").read()
    md5 = hashlib.md5(fw).hexdigest()
    log(f"образ: {a.fw} ({len(fw)} Б), MD5={md5}")
    if not a.md5 or a.md5.lower() != md5:
        sys.exit("ABORT: укажите --md5, совпадающий с MD5 образа (безопасность)")

    off0, off1 = find_offsets(fw)
    log(f"крипто-таблицы: off0=0x{off0:X}, off1=0x{off1:X}")

    n_packets = -(-len(fw) // PACKET_SIZE)
    log(f"пакетов: {n_packets} (+1 терминирующий пустой), "
        f"чанков: {n_packets * CHUNKS_PER_PACKET}")

    s = serial.Serial(a.port, 19200, timeout=0.2)
    time.sleep(0.3)
    r = Reader(s)
    r.drain()

    # --- 1) UID (до 3 попыток, с warmup) ---
    uid = get_uid(r)
    log(f"UID: {uid[:4].hex()}...{uid[-2:].hex()}")

    # --- 2) get_ver ---
    ver_before = get_ver(r, "get_ver", fatal=True)
    if ver_before is None:
        sys.exit("ABORT: get_ver: нет валидной версии до записи")
    log(f"версия ДО: {ver_before!r}")

    # --- 3) rd_info ---
    line = ok_cmd(r, b"down rd_info\r\x00\x00\x00", "rd_info")
    log(f"rd_info: {line[:40]!r}")

    # --- 4) ble_rand + сверка крипто ---
    # Сырые байты в \r-разделённом канале неоднозначны (0x0D в данных): MCU парсит
    # поле ПО ДЛИНЕ (референс bw-flasher шлёт range(1,17) — с 0x0D внутри — и живое
    # железо OK), поэтому ответ читаем ТОЖЕ по длине: "ok " + ключ(16) + "\r" = 20 Б.
    rand = bytes(random.randrange(256) for _ in range(16))
    r.drain()
    r.s.write(b"down ble_rand " + rand + b"\r")
    r.s.flush()
    resp = r.read_exact(20, timeout=3.0)
    mcu_key = resp[3:19]
    if len(mcu_key) < 16 or not resp.startswith(b"ok ") or resp[-1:] != b"\r":
        sys.exit(f"ABORT: ble_rand: короткий/чужой ответ {resp[:24]!r}")
    local_key = sign_rand(uid, rand, fw, off0, off1)
    if mcu_key != local_key:
        sys.exit("ABORT: sign_rand НЕ совпал с MCU (образ/UID не те)")
    log("ble_rand: крипто СОВПАЛА ✓")

    # --- 5) mcu_rand ---
    r.drain()
    r.s.write(b"down mcu_rand\r")
    r.s.flush()
    resp = r.read_exact(20, timeout=3.0)   # "ok " + rand(16) + "\r"
    mcu_rand = resp[3:19]
    if len(mcu_rand) < 16 or not resp.startswith(b"ok ") or resp[-1:] != b"\r":
        sys.exit(f"ABORT: mcu_rand: короткий/чужой ответ {resp[:24]!r}")
    log(f"mcu_rand: {mcu_rand[:4].hex()}...")

    # --- 6) mcu_key → СРАЗУ nvm_write (окно записи!) ---
    key = sign_rand(uid, mcu_rand, fw, off0, off1)
    ok_cmd(r, b"down mcu_key " + key + b"\r", "mcu_key")
    log("mcu_key: принят ✓ — начинаю запись (без задержки)")

    # --- 7) пакеты ---
    data_sent = bytearray()
    t_start = time.time()
    for p in range(n_packets):
        loc = p * PACKET_SIZE
        # таймаут короткий: если «окно записи» уже потеряно, ответ не придёт никогда —
        # лучше быстро ABORT, чем висеть (сессия лечится только power-cycle)
        ok_cmd(r, f"down nvm_write {loc:08X}\r".encode(),
               f"nvm_write @{loc:08X}", timeout=3.0)

        packet = fw[loc:loc + PACKET_SIZE]
        if len(packet) < PACKET_SIZE:
            packet += b"\xFF" * (PACKET_SIZE - len(packet))
        for n in range(CHUNKS_PER_PACKET):
            chunk = packet[n * CHUNK_SIZE:(n + 1) * CHUNK_SIZE]
            frame = b"\x01" + bytes([(n + 1), 0xFF - (n + 1)]) + chunk \
                + struct.pack(">H", crc16_xmodem(chunk))
            acked = False
            for _rep in range(MAX_REPEATS):
                r.drain()   # не давать чужим байтам предыдущего обмена мешать поиску ACK
                s.write(frame)
                s.flush()
                d = r.read_until(b"\x06", timeout=1.0)
                if b"\x15" in d:
                    sys.exit(f"ABORT: CRC-fail чанк p={p} n={n + 1}")
                if b"\x06" in d:
                    acked = True
                    break
            if not acked:
                sys.exit(f"ABORT: чанк p={p} n={n + 1} — нет ACK после {MAX_REPEATS}")
            data_sent += chunk
        # подтверждение пакета (не фатально — как в референсе)
        s.write(b"\x04\x04\x04")
        s.flush()
        r.read_until(b"\x06", timeout=2.0)

        crc32 = zlib.crc32(bytes(data_sent)) & 0xFFFFFFFF
        ok_cmd(r, f"down wr_info {p + 1} {crc32:08x} {(p + 1) * PACKET_SIZE}\r".encode(),
               f"wr_info p={p + 1}")
        el = time.time() - t_start
        rate = (p + 1) / el * 100 / n_packets
        eta = (n_packets - p - 1) / max(el / (p + 1), 0.01)
        log(f"пакет {p + 1}/{n_packets} ok ({rate:.0f}%, ETA ~{eta:.0f} с)")

    # --- 7b) терминирующий пустой пакет (как в живом проверенном прогоне) ---
    loc = n_packets * PACKET_SIZE
    ok_cmd(r, f"down nvm_write {loc:08X}\r".encode(), "nvm_write (терминирующий)",
           timeout=3.0)
    s.write(b"\x04\x04\x04")
    s.flush()
    r.read_until(b"\x06", timeout=2.0)
    crc32 = zlib.crc32(bytes(data_sent)) & 0xFFFFFFFF  # не изменился — данных нет
    ok_cmd(r, f"down wr_info {n_packets + 1} {crc32:08x} {(n_packets + 1) * PACKET_SIZE}\r".encode(),
           "wr_info (терминирующий)")

    # --- 8) dfu_verify (первый ответ может быть пустым — MCU занят; до 3 попыток) ---
    line = None
    for _ in range(3):
        line = cmd(r, b"down dfu_verify\r", "dfu_verify", timeout=5.0, fatal=False)
        if line is not None:
            break
    if line is None or not line.startswith(b"ok"):
        sys.exit(f"ABORT: verify FAILED ({line!r}) — прошивка НЕ переключена")
    log("dfu_verify: OK")

    # --- 9) dfu_active (необратимый шаг) ---
    log(">>> dfu_active — переключение...")
    line = cmd(r, b"down dfu_active\r", "dfu_active", timeout=5.0, fatal=False)
    active_ok = line is not None and line.startswith(b"ok")
    if line is not None and not active_ok:
        sys.exit(f"ABORT: dfu_active: {line!r}")
    if active_ok:
        log("dfu_active: OK — MCU ребутится")

    # --- 10) проверка после (MCU ребутится — несколько попыток) ---
    time.sleep(3)
    ver_after = get_ver(r, "get_ver#after", timeout=3.0, tries=8, fatal=False)
    if not active_ok:
        # ответа на active не было. Живой прогон 2026-08-22: MCU закоммитил и
        # ребутнулся ДО «ok» — ответ потерян в сбросе. Дискриминатор (read-only):
        # rd_info после ребута. Регион очищен = активация закоммичена; данные на месте
        # = не активирована (нужен повтор). Дождёмся дольше — ребут может затянуться.
        log("dfu_active: нет ответа — проверяю ребут и состояние DFU-региона...")
        time.sleep(5)
        ver_after = get_ver(r, "get_ver#after", timeout=3.0, tries=8, fatal=False)
        if ver_after is None:
            sys.exit("ABORT: dfu_active не подтверждён и консоль не вернулась — "
                     "проверить устройство")
        r.drain()
        s.write(b"down rd_info\r\x00\x00\x00")
        s.flush()
        d = r.read_until(b"\r", timeout=3.0)
        rd = d.split(b"\r")[0] if d.endswith(b"\r") else b""
        region_cleared = bool(re.match(rb"^ok 0000 00000000 [0-9A-Fa-f]*$", rd))
        log(f"rd_info после: {rd!r}")
        if not region_cleared:
            sys.exit("ABORT: активация НЕ закоммичена (данные ещё в DFU-регионе) — "
                     "нужен повторный прогон")
        log("dfu_active: ok не пришёл, но MCU ребутнулся и DFU-регион очищен — "
            "считаю активацию закоммиченной")
    # push-поток телеметрии — живой ли MCU?
    end = time.time() + 3.0
    raw = bytearray()
    while time.time() < end:
        raw += s.read(4096)
    n61 = raw.count(b"\x61\x30") + raw.count(b"\x61\x31")
    log(f"версия ПОСЛЕ: {ver_after!r}")
    log(f"push-поток после: {n61} кадров за 3 с {'OK' if n61 > 5 else '- ПРОВЕРИТЬ ЛИНИЮ!'}")
    log(f"Готово. Общее время записи: {time.time() - t_start:.0f} с")
    s.close()
    if ver_after is None:
        sys.exit("ВНИМАНИЕ: dfu_active принят, но консоль не вернулась — "
                 "проверить устройство (версия/поведение)")


if __name__ == "__main__":
    main()
