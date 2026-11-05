"""Unit tests for research/decryptor.py heuristics. Validates key behaviors:
without calibration, heuristics may falsely flag ciphertext as "looks like plaintext"
(see docs/todo.md §A) — this test ensures baseline metrics behave predictably on control data."""
import os

import decryptor as dec


def test_entropy_zero_for_constant_data():
    assert dec.entropy(b"\x00" * 1000) == 0.0


def test_entropy_max_for_uniform_random():
    # 256 unique bytes once each -> maximum entropy (8 bits)
    data = bytes(range(256))
    assert abs(dec.entropy(data) - 8.0) < 1e-9


def test_entropy_empty():
    assert dec.entropy(b"") == 0.0


def test_ascii_strings_finds_embedded_text():
    data = b"\x00\x01xiaomi.scooter.5pro\x00\x02short\x03"
    found = dec.ascii_strings(data, min_len=8)
    assert "xiaomi.scooter.5pro" in found
    assert "short" not in found  # shorter than min_len=8


def test_ascii_strings_respects_min_len():
    data = b"abcdefgh"
    assert dec.ascii_strings(data, min_len=8) == ["abcdefgh"]
    assert dec.ascii_strings(data, min_len=9) == []


def test_thumb_plausibility_range():
    # heuristic must return ratio in [0, 1] on any data
    for data in (b"\x00" * 64, bytes(range(64)), os.urandom(64)):
        p = dec.thumb_plausibility(data)
        assert 0.0 <= p <= 1.0


def test_try_one_ctr_is_reversible_with_correct_key():
    """Sanity check: CTR mode with CORRECT key must return exactly the original
    plaintext back — otherwise the key candidate testing mechanism itself is broken."""
    key = b"\x00" * 16
    iv = b"\x11" * 16
    plaintext = b"A" * 32
    # Encrypt using the same method that try_one uses for decryption (CTR is symmetric)
    enc_results = dec.try_one("zero128", key, plaintext, iv)
    ctr_result = next(pt for mode, pt, err in enc_results if mode == "CTR" and err is None)
    dec_results = dec.try_one("zero128", key, ctr_result, iv)
    ctr_roundtrip = next(pt for mode, pt, err in dec_results if mode == "CTR" and err is None)
    assert ctr_roundtrip == plaintext
