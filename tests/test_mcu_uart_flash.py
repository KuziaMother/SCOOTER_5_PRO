#!/usr/bin/env python3
"""Офлайн-верификация tools/mcu_uart_flash.py против модели СТОРОНЫ MCU.

Модель повторяет живую проверенную последовательность (logs/bw_flasher_log.txt,
2026-08-21): handshake → 74 пакета(0x800) → терминирующий пустой пакет →
dfu_verify (первый ответ пустой) → dfu_active → ребут → get_ver "007".

Плюс враждебные условия, которые убивают наивный парсер:
  - push-кадры телеметрии идут непрерывно, ВКЛЮЧАЯ фазу записи чанков;
  - среди них кадры с CHK == 0x06 и CHK == 0x15 (ложный ACK / CRC-fail
    для парсера без вырезания кадров);
  - кадры рвутся на полпути (holdback-логика Reader);
  - часть чанков отвечает только на повтор (ретрай-путь).

Крипто-якорь: известный вектор из живого лога (uid=4A77..., rand=01..10 →
BLE_KEY 7049273DE6BD8383FBF33C3A128EB946). CRC-якоря wr_info: a7dfe686 (p1)
и 77f34c63 (p74/p75) — из того же лога.
"""
import binascii
import os
import queue
import random
import sys
import threading
import time
import zlib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import mcu_uart_flash as muf  # noqa: E402
from mcu_keygen import sign_rand  # noqa: E402

FW_PATH = ROOT / "firmware_ota" / "c0f78c49f322bd3d71fea19c90241882_mcu_xiaomi.scooter.5pro_v0007.bin"
LIVE_UID = bytes.fromhex("4a77555935567448353632797064474f")
LIVE_KEY_01_10 = bytes.fromhex("7049273de6bd8383fbf33c3a128eb946")


# --------------------------------------------------------------------------
# push-кадры
# --------------------------------------------------------------------------

def make_push(sub, payload, chk=None):
    """61 SUB LEN DATA CHK 9E; CHK = Σ(предшествующих) & 0xFF (или принудительно)."""
    body = bytes([0x61, sub, len(payload)]) + payload
    c = (sum(body) & 0xFF) if chk is None else chk
    return body + bytes([c, 0x9E])


PUSH_30 = make_push(0x30, bytes.fromhex("0300881aa81000000000"))
PUSH_31 = make_push(0x31, bytes.fromhex("9b62cdcb8000190000"))
# ЛОЖНЫЕ СРАСПЫ: валидные по структуре кадры с CHK 0x06 / 0x15.
# Найдем payload так, чтобы Σ&0xFF дал нужное значение (последний байт подстраиваем).
def push_with_chk(sub, base_payload, want):
    p = bytearray(base_payload)
    head = sum(bytes([0x61, sub, len(p)])) + sum(bytes(p[:-1]))
    p[-1] = (want - head) & 0xFF
    return make_push(sub, bytes(p), chk=want)


PUSH_ACK_TRAP = push_with_chk(0x30, bytes.fromhex("0300881aa81000000000"), 0x06)
PUSH_CRC_TRAP = push_with_chk(0x31, bytes.fromhex("9b62cdcb8000190000"), 0x15)

for _f in (PUSH_30, PUSH_31, PUSH_ACK_TRAP, PUSH_CRC_TRAP):
    assert _f[-1] == 0x9E and len(_f) == 5 + _f[2]
    assert sum(_f[:-2]) & 0xFF == _f[-2]


# --------------------------------------------------------------------------
# модель MCU-стороны
# --------------------------------------------------------------------------

class McuEmulator:
    """Отвечает на DFU-консоль как живой MCU из проверенного прогона."""

    def __init__(self, fw, delay=0.002):
        self.fw = fw
        self.delay = delay
        self.uid = LIVE_UID
        self.rx = queue.Queue()
        self.tx_log = bytearray()
        self.text_buf = bytearray()
        self.mcu_rand = bytes(random.randrange(256) for _ in range(16))

        # учёт записанного
        self.nvm_locs = []
        self.chunks = {}          # loc -> {n: data}
        self.chunk_sends = 0      # всего отправок чанков (для детерминированных ретраев)
        self.wr_infos = []        # (count, crc32, size)
        self.confirmations = 0
        self.dfu_verify_calls = 0
        self.dfu_active_calls = 0
        self.get_ver_calls = 0
        self.ble_rand_val = None
        self.mcu_key_val = None
        self.rebooted = False
        self.silent_active = False  # dfu_active без «ok» (ребут раньше ответа)
        self._stop = threading.Event()
        self._push_thread = None

    # -- устройство -> скрипт
    def _emit(self, data, split_at=None):
        """Поставить байты в очередь; split_at — разорвать кадр на полпути."""
        if split_at is not None and 0 < split_at < len(data):
            self.rx.put(data[:split_at])
            time.sleep(0.01)   # пауза, чтобы половина реально «повисла»
            self.rx.put(data[split_at:])
        else:
            self.rx.put(data)

    def _respond(self, data, delay=None):
        time.sleep(delay if delay is not None else self.delay)
        self._emit(data)

    # -- push-поток (враждебный: и в фазе записи, с ловушками CHK)
    def start_pushes(self, interval=0.03):
        # Кадры_emitятся атомарно (одним элементом очереди): байтовый интерливинг
        # ACKа ВНУТРИ рваного push-кадра — неоднозначный случай, в живых захватах
        # не наблюдался (в фазе записи push вообще молчал); holdback рваных кадров
        # покрывает отдельный unit-тест.
        traps = [PUSH_30, PUSH_31, PUSH_ACK_TRAP, PUSH_CRC_TRAP]
        i = 0

        def loop():
            nonlocal i
            while not self._stop.is_set():
                d = traps[i % len(traps)]
                i += 1
                self._emit(d)
                time.sleep(interval)

        self._push_thread = threading.Thread(target=loop, daemon=True)
        self._push_thread.start()

    def stop(self):
        self._stop.set()

    # -- скрипт -> устройство
    def on_write(self, data):
        self.tx_log += data
        if data == bytes.fromhex("532a7dac"):
            self._respond(bytes([0x64, 0x2A, 0x10]) + self.uid +
                          bytes([(sum([0x64, 0x2A, 0x10]) + sum(self.uid)) & 0xFF], ) + b"\x9b")
            return
        if len(data) == 3 and data == b"\x04\x04\x04":
            self.confirmations += 1
            self._respond(b"\x06")
            return
        if len(data) == 133 and data[0] == 0x01:
            self._on_chunk(data)
            return
        # текст: буферизуем до \r (хвостовые NUL от `rd_info\r\x00\x00\x00` — мусор).
        # Исключение — команды с вложенными сырыми байтами (ble_rand/mcu_key):
        # реальный MCU парсит их ПО ДЛИНЕ, а сырые байты могут содержать 0x0D
        # (референс bw-flasher шлёт range(1,17) — там есть 0x0D, и живое железо OK).
        self.text_buf += data
        while True:
            line = None
            for prefix, n_raw in ((b"down ble_rand ", 16), (b"down mcu_key ", 16)):
                if self.text_buf.startswith(prefix):
                    need = len(prefix) + n_raw + 1  # + завершающий \r
                    if len(self.text_buf) < need:
                        return  # кадр ещё не дописан — ждём продолжения
                    line = bytes(self.text_buf[:len(prefix) + n_raw])  # без \r
                    self.text_buf = self.text_buf[need:]
                    break
            if line is None:
                if b"\r" not in self.text_buf:
                    return
                line, self.text_buf = self.text_buf.split(b"\r", 1)
            while self.text_buf.startswith(b"\x00"):
                del self.text_buf[0]
            self._on_text(bytes(line))

    def _on_chunk(self, frame):
        n = frame[1]
        assert frame[2] == 0xFF - n
        data, crc = frame[3:-2], binascii.crc_hqx(frame[3:-2], 0)
        assert crc == (frame[-2] << 8) | frame[-1], "chunk CRC mismatch"
        loc = self.nvm_locs[-1]
        first_send = loc not in self.chunks or n not in self.chunks[loc]
        self.chunks.setdefault(loc, {})[n] = data
        # ретрай-путь: каждый 97-й чанк молчит на ПЕРВУЮ отправку, отвечает на повтор
        if first_send and self.chunk_sends % 97 == 0:
            self.chunk_sends += 1
            return
        self.chunk_sends += 1
        self._respond(b"\x06")

    def _on_text(self, line):
        if line == b"down get_ver":
            self.get_ver_calls += 1
            if self.rebooted:
                time.sleep(0.5)   # MCU ещё догружается после ребута
            self._respond(b"007\r")
            return
        if line == b"down rd_info":
            self._respond(b"ok 0000 00000000 00000\r")
            return
        if line.startswith(b"down ble_rand "):
            self.ble_rand_val = line[14:]
            key = sign_rand(self.uid, self.ble_rand_val, self.fw, muf.OFF0_DEFAULT, muf.OFF1_DEFAULT)
            self._respond(b"ok " + key + b"\r")
            return
        if line == b"down mcu_rand":
            self._respond(b"ok " + self.mcu_rand + b"\r")
            return
        if line.startswith(b"down mcu_key "):
            self.mcu_key_val = line[13:]
            key = sign_rand(self.uid, self.mcu_rand, self.fw, muf.OFF0_DEFAULT, muf.OFF1_DEFAULT)
            assert self.mcu_key_val == key, "mcu_key не совпал"
            self._respond(b"ok\r")
            return
        if line.startswith(b"down nvm_write "):
            loc = int(line[15:], 16)
            self.nvm_locs.append(loc)
            self._respond(b"ok\r")
            return
        if line.startswith(b"down wr_info "):
            parts = line[13:].split(b" ")
            count, crc, size = int(parts[0]), parts[1].decode(), int(parts[2])
            sent = bytearray()
            for L in sorted(self.chunks):
                for n in range(1, 17):
                    sent += self.chunks[L][n]
            expect = format(zlib.crc32(bytes(sent)) & 0xFFFFFFFF, "08x")
            assert crc == expect, f"wr_info CRC {crc} != {expect}"
            assert size == count * 0x800
            self.wr_infos.append((count, crc, size))
            self._respond(b"ok\r")
            return
        if line == b"down dfu_verify":
            self.dfu_verify_calls += 1
            if self.dfu_verify_calls == 1:
                return  # первый ответ пустой — как в живом логе
            self._respond(b"ok\r")
            return
        if line == b"down dfu_active":
            self.dfu_active_calls += 1
            if not self.silent_active:
                self._respond(b"ok\r")
            time.sleep(0.2)
            self.rebooted = True
            # мусор при старте (как в живом логе: 43, хвосты push-кадров)
            self._emit(b"\x43")
            return
        raise AssertionError(f"неизвестная команда: {line!r}")


class MockSerial:
    """pyserial-совместимая обёртка над McuEmulator."""

    def __init__(self, emu, *args, **kwargs):
        self.emu = emu
        self.pending = bytearray()

    def write(self, data):
        self.emu.on_write(bytes(data))
        return len(data)

    def read(self, n=1):
        if not self.pending:
            try:
                self.pending += self.emu.rx.get(timeout=0.05)
            except queue.Empty:
                return b""
        d = bytes(self.pending[:n])
        del self.pending[:n]
        return d

    def flush(self):
        pass

    def close(self):
        self.emu.stop()

    def reset_input_buffer(self):  # pragma: no cover — наш скрипт её не вызывает
        pytest.fail("reset_input_buffer запрещён (рвёт push-кадр пополам)")


# --------------------------------------------------------------------------
# тесты
# --------------------------------------------------------------------------

def test_keygen_known_vector():
    fw = FW_PATH.read_bytes()
    assert sign_rand(LIVE_UID, bytes(range(1, 17)), fw, 0x24187, 0x24387) == LIVE_KEY_01_10


def test_reader_strips_valid_frames_only():
    s = muf.Reader.__new__(muf.Reader)
    s.raw = bytearray()
    s.clean = bytearray()
    # полный валидный кадр + ответ
    s.raw += PUSH_30 + b"ok\r"
    s._classify()
    assert s.clean == b"ok\r" and not s.raw
    # кадр с битым CHK — НЕ вырезается (байты остаются как данные)
    bad = bytearray(PUSH_30)
    bad[-2] ^= 0xFF
    s.raw += bytes(bad) + b"ok\r"
    s._classify()
    assert bytes(bad) in s.clean and s.clean.endswith(b"ok\r")
    # неполный хвостовой кадр удерживается
    s.raw = bytearray(PUSH_30[:6])
    s.clean = bytearray()
    s._classify()
    assert not s.clean and len(s.raw) == 6
    # ...и подтверждается, когда доходит остаток
    s.raw += PUSH_30[6:] + b"ok\r"
    s._classify()
    assert s.clean == b"ok\r" and not s.raw


def _run_flash(capsys, silent_active=False):
    """Прогнать mcu_uart_flash.main() над эмулятором; вернуть (emu, out)."""
    fw = FW_PATH.read_bytes()
    emu = McuEmulator(fw)
    emu.silent_active = silent_active
    old_serial = muf.serial.Serial
    muf.serial.Serial = lambda *a, **k: MockSerial(emu)
    try:
        emu.start_pushes(interval=0.03)
        argv = ["mcu_uart_flash.py", "--port", "MOCK", "--fw", str(FW_PATH),
                "--md5", "c0f78c49f322bd3d71fea19c90241882"]
        sys.argv = argv
        muf.main()
    finally:
        muf.serial.Serial = old_serial
        emu.stop()
    return emu, capsys.readouterr().out, fw


def _assert_write_flow(emu, out, fw):
    # -- handshake
    assert emu.get_ver_calls >= 2          # warmup + явный get_ver (+ после)
    assert emu.ble_rand_val is not None and len(emu.ble_rand_val) == 16
    assert emu.mcu_key_val is not None

    # -- пакеты: 74 реальных + 1 терминирующий пустой
    n = -(-len(fw) // muf.PACKET_SIZE)
    expect_locs = [i * muf.PACKET_SIZE for i in range(n + 1)]
    assert emu.nvm_locs == expect_locs, "последовательность nvm_write неверна"

    # -- чанки: все 74×16, данные = образ (последний пакет до 0xFF)
    assert len(emu.chunks) == n
    reassembled = bytearray()
    for i in range(n):
        loc = i * muf.PACKET_SIZE
        for c in range(1, 17):
            reassembled += emu.chunks[loc][c]
    assert bytes(reassembled[:len(fw)]) == fw
    assert all(b == 0xFF for b in reassembled[len(fw):])

    # -- подтверждения и wr_info: по числу пакетов + терминирующий
    assert emu.confirmations == n + 1
    assert len(emu.wr_infos) == n + 1
    assert emu.wr_infos[0][1] == "a7dfe686"      # якорь из живого лога
    assert emu.wr_infos[-1][1] == emu.wr_infos[-2][1] == "77f34c63"  # терминирующий: CRC не изменился
    assert [w[0] for w in emu.wr_infos] == list(range(1, n + 2))

    # -- verify/active
    assert emu.dfu_verify_calls == 2             # первый ответ был пустым
    assert emu.dfu_active_calls == 1

    # -- итог
    assert "версия ПОСЛЕ: '007'" in out
    assert "dfu_verify: OK" in out
    assert "ABORT" not in out


def test_full_flash_flow(capsys):
    emu, out, fw = _run_flash(capsys)
    _assert_write_flow(emu, out, fw)
    print(out)


def test_full_flash_flow_silent_active(capsys):
    """Живой сценарий 2026-08-22: «ok» на dfu_active потерян в ребуте.

    Скрипт должен не падать, а проверить read-only: версия вернулась +
    DFU-регион очищен (rd_info) — и засчитать активацию закоммиченной.
    """
    emu, out, fw = _run_flash(capsys, silent_active=True)
    _assert_write_flow(emu, out, fw)
    assert "проверяю ребут и состояние DFU-региона" in out
    assert "считаю активацию закоммиченной" in out
    print(out)
    # -- handshake
    assert emu.get_ver_calls >= 2          # warmup + явный get_ver (+ после)
    assert emu.ble_rand_val is not None and len(emu.ble_rand_val) == 16
    assert emu.mcu_key_val is not None

    # -- пакеты: 74 реальных + 1 терминирующий пустой
    n = -(-len(fw) // muf.PACKET_SIZE)
    expect_locs = [i * muf.PACKET_SIZE for i in range(n + 1)]
    assert emu.nvm_locs == expect_locs, "последовательность nvm_write неверна"

    # -- чанки: все 74×16, данные = образ (последний пакет до 0xFF)
    assert len(emu.chunks) == n
    reassembled = bytearray()
    for i in range(n):
        loc = i * muf.PACKET_SIZE
        for c in range(1, 17):
            reassembled += emu.chunks[loc][c]
    assert bytes(reassembled[:len(fw)]) == fw
    assert all(b == 0xFF for b in reassembled[len(fw):])

    # -- подтверждения и wr_info: по числу пакетов + терминирующий
    assert emu.confirmations == n + 1
    assert len(emu.wr_infos) == n + 1
    assert emu.wr_infos[0][1] == "a7dfe686"      # якорь из живого лога
    assert emu.wr_infos[-1][1] == emu.wr_infos[-2][1] == "77f34c63"  # терминирующий: CRC не изменился
    assert [w[0] for w in emu.wr_infos] == list(range(1, n + 2))

    # -- verify/active
    assert emu.dfu_verify_calls == 2             # первый ответ был пустым
    assert emu.dfu_active_calls == 1

    # -- итог
    assert "версия ПОСЛЕ: '007'" in out
    assert "dfu_verify: OK" in out
    assert "ABORT" not in out
    print(out)


if __name__ == "__main__":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.exit(pytest.main([__file__, "-v", "-s"]))
