"""The unit tests of the webui/props.py — the formatting and the masking of the
secrets for the web UI. The special attention: the SENSITIVE properties (the
OOB_CODE, the SN) must NEVER get into the response text — this is the direct
security requirement of the project (the CLAUDE.md item 6).

Юнит-тесты webui/props.py — форматирование и маскировка секретов для web UI.
Особое внимание: SENSITIVE-свойства (OOB_CODE, SN) НИКОГДА не должны попадать
в текст ответа — это прямое требование безопасности проекта (CLAUDE.md п.6)."""
import struct

import props


def test_sensitive_properties_are_masked():
    """The 3.6 OOB_CODE, the 4.2 BATTERY_SN, the 4.4 SCOOTER_SN — the secrets, the
    text must be "hidden" and not the real value.
    3.6 OOB_CODE, 4.2 BATTERY_SN, 4.4 SCOOTER_SN — секреты, текст должен быть
    «скрыто», а не реальное значение."""
    for key in ((3, 6), (4, 2), (4, 4)):
        assert key in props.SENSITIVE
        siid, piid = key
        result = props.format_property(siid, piid, 10, b"SECRET-VALUE-1234")
        assert result["secret"] is True
        assert "SECRET" not in result["text"]
        assert result["text"].startswith("скрыто")


def test_is_safe_excludes_sensitive():
    """The is_safe: the normal property is True, the sensitive/unknown is False.
    is_safe: обычное свойство — True, секретное/неизвестное — False."""
    assert props.is_safe((1, 2)) is True          # BATTERY_LEVEL — обычное свойство
    assert props.is_safe((3, 6)) is False          # OOB_CODE — секрет
    assert props.is_safe((99, 99)) is False        # несуществующее


def test_safe_filter_parses_string_keys_and_dedupes():
    """The safe_filter: the string keys parse, the sensitive are excluded, the
    duplicates are removed.
    safe_filter: строковые ключи парсятся, секретные исключаются, дубли уходят."""
    out = props.safe_filter(["1.2", (1, 2), "3.6", "2.6"])
    assert out == [(1, 2), (2, 6)]                 # (3,6) секрет — исключён, дублей нет


def test_unit_multiplier_km_vs_mi():
    """The unit multiplier: the km=1.0, the mi=0.6213712, the invalid -> the km.
    Множитель единиц: км=1.0, миля=0.6213712, некорректное -> км."""
    assert props.unit_multiplier(1) == 1.0
    assert abs(props.unit_multiplier(2) - 0.6213712) < 1e-9
    assert props.unit_multiplier(None) == 1.0       # некорректный ввод -> км по умолчанию


def test_decode_value_matches_spec_read_semantics():
    """The decode_value matches the spec_read semantics (the float/signed/unsigned/
    empty).
    decode_value соответствует семантике spec_read (float/signed/unsigned/пусто)."""
    assert props.decode_value(9, struct.pack("<f", 1.5)) == 1.5
    assert props.decode_value(2, b"\xff") == -1      # INT8 signed
    assert props.decode_value(1, b"\xff") == 255     # UINT8 unsigned
    assert props.decode_value(0, b"") is None


def test_format_property_battery_level():
    """The format_property of the BATTERY_LEVEL (the 100% value).
    format_property для BATTERY_LEVEL (значение 100%)."""
    result = props.format_property(1, 2, 1, bytes([100]))
    assert result["secret"] is False
    assert result["name"] == "BATTERY_LEVEL"
    assert "100" in result["text"]


def test_format_property_empty_value():
    """The format_property of the empty value ("empty" text).
    format_property для пустого значения (текст «пусто»)."""
    result = props.format_property(1, 2, 1, b"")
    assert result["text"] == "пусто"
    assert result["secret"] is False
