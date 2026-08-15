"""Юнит-тесты чистых функций эмулятора устройства (emulator/scooter_device.py):
сравнение версий прошивки и кодирование spec-значений. Без BLE, без асинхронности."""
import struct

import scooter_device as sd


def test_ver_tuple_parses_dotted_and_underscore():
    assert sd.ver_tuple("2.7.0_0015") == (2, 7, 0, 15)
    assert sd.ver_tuple("0007") == (7,)


def test_ver_tuple_ordering_matches_switch_firmware_gate():
    """От этого сравнения зависит защита от дурака в _switch(): 'новее' решается
    именно так, как здесь — иначе можно случайно разрешить даунгрейд/переустановку."""
    assert sd.ver_tuple("2.8.0_0001") > sd.ver_tuple("2.7.0_0015")
    assert sd.ver_tuple("2.7.0_0015") == sd.ver_tuple("2.7.0_0015")
    assert not sd.ver_tuple("2.7.0_0015") > sd.ver_tuple("2.7.0_0015")


def test_spec_counter_bytes_roundtrip():
    for cnt in (0, 1, 0xABCD, 0x1FFFF):
        b = sd.spec_counter_bytes(cnt)
        low = b[0] | (b[1] << 8)
        high = b[2] | (b[3] << 8)
        assert (high << 16 | low) == cnt & 0xFFFFFFFF


def test_spec_encode_value_types():
    assert sd.spec_encode_value(1, 100) == bytes([100])              # UINT8
    assert sd.spec_encode_value(2, -1) == b"\xff"                    # INT8 signed
    assert sd.spec_encode_value(3, 5344) == struct.pack("<H", 5344)  # UINT16
    assert sd.spec_encode_value(9, 53.44) == struct.pack("<f", 53.44)  # FLOAT
    assert sd.spec_encode_value(10, "test") == b"test"               # STRING


def test_spec_telemetry_and_subscribable_keys_are_consistent():
    """SUBSCRIBABLE должен ссылаться на реальные siid/piid — опечатка тут тихо
    сломает пуш конкретного свойства (см. push_property)."""
    assert isinstance(sd.SUBSCRIBABLE, set)
    assert (2, 7) in sd.SUBSCRIBABLE  # IS_RIDING — используется в сценарии 6
    for key in sd.SUBSCRIBABLE:
        assert isinstance(key, tuple) and len(key) == 2
