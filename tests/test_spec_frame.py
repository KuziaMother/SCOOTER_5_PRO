"""Юнит-тесты чистых функций протокола spec-канала (probes/spec_read.py) —
кодирование/декодирование кадра телеметрии, без BLE и без устройства."""
import struct

import spec_read as sr


def test_counter_bytes_roundtrip():
    for cnt in (0, 1, 0xFFFF, 0x10000, 0x12345678):
        b = sr.counter_bytes(cnt)
        assert len(b) == 4
        low = b[0] | (b[1] << 8)
        high = b[2] | (b[3] << 8)
        assert (high << 16 | low) == cnt & 0xFFFFFFFF


def test_build_frame_header_and_single_object():
    frame = sr.build_frame([(1, 2)], tid=7, type_code=0, op=2)
    lenflag, tid, op, count = struct.unpack("<HHBB", frame[:6])
    assert lenflag & 0x0FFF == len(frame)
    assert lenflag & 0xF000 == 0x2000
    assert tid == 7
    assert op == 2
    assert count == 1
    siid, piid, tl = struct.unpack("<BHH", frame[6:11])
    assert siid == 1
    assert piid == 2
    assert tl == 0  # запрос на чтение: valueLen=0, typeCode=0


def test_build_frame_multi_object_count():
    frame = sr.build_frame([(1, 2), (2, 6), (3, 12)])
    _, _, _, count = struct.unpack("<HHBB", frame[:6])
    assert count == 3
    assert len(frame) == 6 + 3 * 5  # заголовок + 3 объекта по 5Б (пустое значение)


def test_decode_value_float32():
    val = struct.pack("<f", 53.44)
    assert abs(sr.decode_value(9, val) - 53.44) < 1e-4


def test_decode_value_signed_vs_unsigned():
    # type 2 = INT8 (signed), type 1 = UINT8 (unsigned) — тот же байт 0xFF
    assert sr.decode_value(2, b"\xff") == -1
    assert sr.decode_value(1, b"\xff") == 255


def test_decode_value_string():
    assert sr.decode_value(10, b"60555/TEST") == "60555/TEST"


def test_decode_value_empty_is_none():
    assert sr.decode_value(9, b"") is None


def test_parse_reply_roundtrip_single_object():
    """Собираем ответное тело так же, как это делает устройство (см.
    REPORT.md §6.13: [siid][piid][status][type|len][value] — на 2Б больше
    запроса из-за поля статуса), затем разбираем parse_reply и сверяем."""
    siid, piid, tcode, status = 1, 2, 1, 0
    value = bytes([100])  # BATTERY_LEVEL = 100%
    body = struct.pack("<BHHH", siid, piid, status, (tcode << 12) | len(value)) + value
    total = 6 + len(body)
    pt = struct.pack("<HHBB", (total | 0x2000) & 0xFFFF, 1, 3, 1) + body

    lines = sr.parse_reply(pt)
    joined = "\n".join(lines)
    assert "BATTERY_LEVEL" in joined
    assert "100" in joined
    assert "status=" not in joined  # status=0 не должен печататься как ошибка


def test_parse_reply_reports_error_status():
    # Ошибочная запись — ровно 5 байт: [siid][piid][status], без tl/value (FACTS).
    siid, piid, status = 1, 4, 0xF05D  # -4003, multi-object
    body = struct.pack("<BHH", siid, piid, status)
    total = 6 + len(body)
    pt = struct.pack("<HHBB", (total | 0x2000) & 0xFFFF, 1, 3, 1) + body

    lines = sr.parse_reply(pt)
    joined = "\n".join(lines)
    assert "status=61533" in joined or "61533" in joined
    assert "хвост" not in joined  # 5-байтная ошибка должна разобраться без остатка


def test_parse_reply_mixed_batch_no_desync():
    """Регрессия: смешанный батч ok+ошибка+ok. Раньше parse_reply всегда читал
    7+len на объект и десинхронизировался на 5-байтных ошибочных записях."""
    def ok(siid, piid, tcode, value):
        return struct.pack("<BHHH", siid, piid, 0, (tcode << 12) | len(value)) + value

    def err(siid, piid, status=0xF05D):
        return struct.pack("<BHH", siid, piid, status)

    body = ok(2, 3, 0, b"\x00") + err(0, 0x200) + ok(2, 7, 1, b"\x05")
    total = 6 + len(body)
    pt = struct.pack("<HHBB", (total | 0x2000) & 0xFFFF, 1, 3, 3) + body

    lines = sr.parse_reply(pt)
    joined = "\n".join(lines)
    assert "CRUISE_IS_ON" in joined            # 1-й объект (ok) разобран
    assert "status=61533" in joined            # 2-й объект — ошибка
    assert "IS_RIDING" in joined and "= 5" in joined  # 3-й объект (ok) не потерян
    assert "хвост" not in joined               # точное выравнивание, без остатка
