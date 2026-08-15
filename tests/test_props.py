"""Юнит-тесты webui/props.py — форматирование и маскировка секретов для web UI.
Особое внимание: SENSITIVE-свойства (OOB_CODE, SN) НИКОГДА не должны попадать
в текст ответа — это прямое требование безопасности проекта (CLAUDE.md п.6)."""
import struct

import props


def test_sensitive_properties_are_masked():
    """3.6 OOB_CODE, 4.2 BATTERY_SN, 4.4 SCOOTER_SN — секреты, текст должен
    быть 'скрыто', а не реальное значение."""
    for key in ((3, 6), (4, 2), (4, 4)):
        assert key in props.SENSITIVE
        siid, piid = key
        result = props.format_property(siid, piid, 10, b"SECRET-VALUE-1234")
        assert result["secret"] is True
        assert "SECRET" not in result["text"]
        assert result["text"].startswith("скрыто")


def test_is_safe_excludes_sensitive():
    assert props.is_safe((1, 2)) is True          # BATTERY_LEVEL — обычное свойство
    assert props.is_safe((3, 6)) is False          # OOB_CODE — секрет
    assert props.is_safe((99, 99)) is False        # несуществующее


def test_safe_filter_parses_string_keys_and_dedupes():
    out = props.safe_filter(["1.2", (1, 2), "3.6", "2.6"])
    assert out == [(1, 2), (2, 6)]                 # (3,6) секрет — исключён, дублей нет


def test_unit_multiplier_km_vs_mi():
    assert props.unit_multiplier(1) == 1.0
    assert abs(props.unit_multiplier(2) - 0.6213712) < 1e-9
    assert props.unit_multiplier(None) == 1.0       # некорректный ввод -> км по умолчанию


def test_decode_value_matches_spec_read_semantics():
    assert props.decode_value(9, struct.pack("<f", 1.5)) == 1.5
    assert props.decode_value(2, b"\xff") == -1      # INT8 signed
    assert props.decode_value(1, b"\xff") == 255     # UINT8 unsigned
    assert props.decode_value(0, b"") is None


def test_format_property_battery_level():
    result = props.format_property(1, 2, 1, bytes([100]))
    assert result["secret"] is False
    assert result["name"] == "BATTERY_LEVEL"
    assert "100" in result["text"]


def test_format_property_empty_value():
    result = props.format_property(1, 2, 1, b"")
    assert result["text"] == "пусто"
    assert result["secret"] is False
