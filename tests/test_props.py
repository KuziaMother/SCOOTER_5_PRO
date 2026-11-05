"""Unit tests for webui/props.py — formatting and masking secrets for web UI.
Special requirement: SENSITIVE properties (OOB_CODE, SN) must NEVER appear
in plaintext responses — mandatory project security requirement (CLAUDE.md item 6)."""
import struct

import props


def test_sensitive_properties_are_masked():
    """3.6 OOB_CODE, 4.2 BATTERY_SN, 4.4 SCOOTER_SN — secrets, text must be
    'hidden' and never display the actual value."""
    for key in ((3, 6), (4, 2), (4, 4)):
        assert key in props.SENSITIVE
        siid, piid = key
        result = props.format_property(siid, piid, 10, b"SECRET-VALUE-1234")
        assert result["secret"] is True
        assert "SECRET" not in result["text"]
        assert result["text"].startswith("hidden")
        assert result["text_en"].startswith("hidden")
        assert result["text_ru"].startswith("скрыто")


def test_is_safe_excludes_sensitive():
    assert props.is_safe((1, 2)) is True          # BATTERY_LEVEL — standard property
    assert props.is_safe((3, 6)) is False          # OOB_CODE — secret
    assert props.is_safe((99, 99)) is False        # nonexistent


def test_safe_filter_parses_string_keys_and_dedupes():
    out = props.safe_filter(["1.2", (1, 2), "3.6", "2.6"])
    assert out == [(1, 2), (2, 6)]                 # (3,6) secret is excluded, no duplicates


def test_unit_multiplier_km_vs_mi():
    assert props.unit_multiplier(1) == 1.0
    assert abs(props.unit_multiplier(2) - 0.6213712) < 1e-9
    assert props.unit_multiplier(None) == 1.0       # invalid input -> km by default


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
    assert "100" in result["text_en"]


def test_format_property_empty_value():
    result = props.format_property(1, 2, 1, b"")
    assert result["text"] == "empty"
    assert result["text_en"] == "empty"
    assert result["text_ru"] == "пусто"
    assert result["secret"] is False


def test_english_labels_and_groups_coverage():
    for key in props.LABELS:
        assert key in props.LABELS_EN, f"Missing English label for {key}"
        assert props.LABELS_EN[key], f"Empty English label for {key}"

    for code in props.FAULT_LABELS:
        assert code in props.FAULT_LABELS_EN, f"Missing English fault label for {code}"

    group_ids_ru = {g["id"] for g in props.GROUPS}
    group_ids_en = {g["id"] for g in props.GROUPS_EN}
    assert group_ids_ru == group_ids_en


def test_format_property_with_explicit_lang_en():
    result_en = props.format_property(1, 1, 1, bytes([2]), lang="en")
    assert result_en["label"] == "Ride Mode"
    assert "standard" in result_en["text"]

    result_ru = props.format_property(1, 1, 1, bytes([2]), lang="ru")
    assert result_ru["label"] == "Режим"
    assert "standard" in result_ru["text"]
