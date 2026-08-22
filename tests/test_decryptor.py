"""Юнит-тесты эвристик research/decryptor.py. Проверяем именно то, из-за
чего этот скрипт вообще имеет смысл: без калибровки эвристики ложно флагуют
шифртекст как «похоже на плейнтекст» (см. docs/todo.md §A) — тест фиксирует,
что базовые метрики ведут себя предсказуемо на контрольных данных."""
import os

import decryptor as dec


def test_entropy_zero_for_constant_data():
    assert dec.entropy(b"\x00" * 1000) == 0.0


def test_entropy_max_for_uniform_random():
    # 256 разных байт по разу каждый -> максимальная энтропия (8 бит)
    data = bytes(range(256))
    assert abs(dec.entropy(data) - 8.0) < 1e-9


def test_entropy_empty():
    assert dec.entropy(b"") == 0.0


def test_ascii_strings_finds_embedded_text():
    data = b"\x00\x01xiaomi.scooter.5pro\x00\x02short\x03"
    found = dec.ascii_strings(data, min_len=8)
    assert "xiaomi.scooter.5pro" in found
    assert "short" not in found  # короче min_len=8


def test_ascii_strings_respects_min_len():
    data = b"abcdefgh"
    assert dec.ascii_strings(data, min_len=8) == ["abcdefgh"]
    assert dec.ascii_strings(data, min_len=9) == []


def test_thumb_plausibility_range():
    # эвристика должна возвращать долю в [0, 1] на любых данных
    for data in (b"\x00" * 64, bytes(range(64)), os.urandom(64)):
        p = dec.thumb_plausibility(data)
        assert 0.0 <= p <= 1.0


def test_try_one_ctr_is_reversible_with_correct_key():
    """Собственная санити-проверка: CTR-режим с ПРАВИЛЬНЫМ ключом должен давать
    ровно исходный plaintext обратно — иначе сломан сам механизм подбора."""
    key = b"\x00" * 16
    iv = b"\x11" * 16
    plaintext = b"A" * 32
    # зашифровать тем же методом, что try_one использует для расшифровки (CTR симметричен)
    enc_results = dec.try_one("zero128", key, plaintext, iv)
    ctr_result = next(pt for mode, pt, err in enc_results if mode == "CTR" and err is None)
    dec_results = dec.try_one("zero128", key, ctr_result, iv)
    ctr_roundtrip = next(pt for mode, pt, err in dec_results if mode == "CTR" and err is None)
    assert ctr_roundtrip == plaintext
