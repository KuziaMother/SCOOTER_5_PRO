"""Unit tests for pure spec-channel protocol functions (probes/spec_read.py) —
encoding and decoding telemetry frames without BLE or physical hardware."""
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
    assert tl == 0  # read request: valueLen=0, typeCode=0


def test_build_frame_multi_object_count():
    frame = sr.build_frame([(1, 2), (2, 6), (3, 12)])
    _, _, _, count = struct.unpack("<HHBB", frame[:6])
    assert count == 3
    assert len(frame) == 6 + 3 * 5  # header + 3 objects of 5B (empty value)


def test_decode_value_float32():
    val = struct.pack("<f", 53.44)
    assert abs(sr.decode_value(9, val) - 53.44) < 1e-4


def test_decode_value_signed_vs_unsigned():
    # type 2 = INT8 (signed), type 1 = UINT8 (unsigned) — same byte 0xFF
    assert sr.decode_value(2, b"\xff") == -1
    assert sr.decode_value(1, b"\xff") == 255


def test_decode_value_string():
    assert sr.decode_value(10, b"60555/TEST") == "60555/TEST"


def test_decode_value_empty_is_none():
    assert sr.decode_value(9, b"") is None


def test_parse_reply_roundtrip_single_object():
    """Build response body identical to device response format (see
    REPORT.md §6.13: [siid][piid][status][type|len][value] — 2B larger than
    request due to status field), then parse via parse_reply and verify."""
    siid, piid, tcode, status = 1, 2, 1, 0
    value = bytes([100])  # BATTERY_LEVEL = 100%
    body = struct.pack("<BHHH", siid, piid, status, (tcode << 12) | len(value)) + value
    total = 6 + len(body)
    pt = struct.pack("<HHBB", (total | 0x2000) & 0xFFFF, 1, 3, 1) + body

    lines = sr.parse_reply(pt)
    joined = "\n".join(lines)
    assert "BATTERY_LEVEL" in joined
    assert "100" in joined
    assert "status=" not in joined  # status=0 should not be printed as error


def test_parse_reply_reports_error_status():
    # Error record is exactly 5 bytes: [siid][piid][status], no tl/value (FACTS).
    siid, piid, status = 1, 4, 0xF05D  # -4003, multi-object
    body = struct.pack("<BHH", siid, piid, status)
    total = 6 + len(body)
    pt = struct.pack("<HHBB", (total | 0x2000) & 0xFFFF, 1, 3, 1) + body

    lines = sr.parse_reply(pt)
    joined = "\n".join(lines)
    assert "status=61533" in joined or "61533" in joined
    assert "tail" not in joined  # 5-byte error record must parse cleanly without leftover


def test_parse_reply_mixed_batch_no_desync():
    """Regression test: mixed batch of ok + error + ok. Previously parse_reply always
    read 7+len per object and desynchronized on 5-byte error entries."""
    def ok(siid, piid, tcode, value):
        return struct.pack("<BHHH", siid, piid, 0, (tcode << 12) | len(value)) + value

    def err(siid, piid, status=0xF05D):
        return struct.pack("<BHH", siid, piid, status)

    body = ok(2, 3, 0, b"\x00") + err(0, 0x200) + ok(2, 7, 1, b"\x05")
    total = 6 + len(body)
    pt = struct.pack("<HHBB", (total | 0x2000) & 0xFFFF, 1, 3, 3) + body

    lines = sr.parse_reply(pt)
    joined = "\n".join(lines)
    assert "CRUISE_IS_ON" in joined            # 1st object (ok) parsed
    assert "status=61533" in joined            # 2nd object is error
    assert "IS_RIDING" in joined and "= 5" in joined  # 3rd object (ok) preserved
    assert "tail" not in joined               # exact alignment, no leftover
