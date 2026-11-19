"""The unit tests of the heuristics of research/decryptor.py. We check exactly what
makes this script worth it: without calibration the heuristics falsely flag the
ciphertext as "looks like the plaintext" (see the docs/todo.md section A) — the test
fixes that the basic metrics behave predictably on the control data.

Юнит-тесты эвристик research/decryptor.py. Проверяем именно то, из-за
чего этот скрипт вообще имеет смысл: без калибровки эвристики ложно флагуют
шифртекст как «похоже на плейнтекст» (см. docs/todo.md §A) — тест фиксирует,
что базовые метрики ведут себя предсказуемо на контрольных данных."""
import os

import decryptor as dec


def test_entropy_zero_for_constant_data():
    """The entropy of the constant data is 0.
    Энтропия константных данных = 0."""
    assert dec.entropy(b"\x00" * 1000) == 0.0


def test_entropy_max_for_uniform_random():
    """The entropy of the uniform random is the maximum (8 bits).
    Энтропия равномерного случайного — максимум (8 бит)."""
    # 256 разных байт по разу каждый -> максимальная энтропия (8 бит)
    data = bytes(range(256))
    assert abs(dec.entropy(data) - 8.0) < 1e-9


def test_entropy_empty():
    """The entropy of the empty data is 0.
    Энтропия пустых данных = 0."""
    assert dec.entropy(b"") == 0.0


def test_ascii_strings_finds_embedded_text():
    """The ASCII strings finds the embedded text (the min length filter works).
    ASCII-строки находят встроенный текст (фильтр мин. длины работает)."""
    data = b"\x00\x01xiaomi.scooter.5pro\x00\x02short\x03"
    found = dec.ascii_strings(data, min_len=8)
    assert "xiaomi.scooter.5pro" in found
    assert "short" not in found  # короче min_len=8


def test_ascii_strings_respects_min_len():
    """The min length filter of the ASCII strings.
    Фильтр минимальной длины ASCII-строк."""
    data = b"abcdefgh"
    assert dec.ascii_strings(data, min_len=8) == ["abcdefgh"]
    assert dec.ascii_strings(data, min_len=9) == []


def test_thumb_plausibility_range():
    """The Thumb plausibility returns the ratio in [0, 1] on any data.
    Thumb-правдоподобность возвращает долю в [0, 1] на любых данных."""
    # эвристика должна возвращать долю в [0, 1] на любых данных
    for data in (b"\x00" * 64, bytes(range(64)), os.urandom(64)):
        p = dec.thumb_plausibility(data)
        assert 0.0 <= p <= 1.0


def test_try_one_ctr_is_reversible_with_correct_key():
    """The own sanity check: the CTR mode with the CORRECT key must give exactly the
    original plaintext back — otherwise the brute-force mechanism itself is broken.
    Собственная санити-проверка: CTR-режим с ПРАВИЛЬНЫМ ключом должен давать
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
