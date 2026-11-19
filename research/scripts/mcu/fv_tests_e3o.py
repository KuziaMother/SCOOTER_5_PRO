# -*- coding: utf-8 -*-
# ruff: noqa: F405  (names from the star-import of fv_core)
"""F2 (section 99): BLE app-protocol deepening from the plugin + snoop (no hardware).

(1) The full siid/piid property table from the Mi Home plugin (modules/10724.js —
    global.SIID_DIC + global.SIID_N): SIID_1..6 (9/18/12/9/27/5 properties), the
    PROP_VALUE_TYPE dictionary. Cross-checked with the NAMES of probes/spec_read.py
    (the overlapping entries are equal) — MI_SIID_PIID in emulator/mcu_emu.py.
(2) The OTA/DFU frame format (siid=0xF5) from logs/btsnoop_hci.log (97 frames,
    handles 0x38 app->dev / 0x3A dev->app ack / 0x44 alt):
    [0xF5][piid][N][marker:2 LE][sub:4][cls:1][payload:N+1], total = 11+N;
    N=0 -> the variable payload (up to ~234B, MTU-4). marker: 0xFFFF — the small
    frames, 0x5300/0x5600/0x5501 — the 208B chunk frames, 0x005C/0x00DE/... — the
    16-32B frames. cls: 0x80/0xA0/0x90 — the data-write, 0x00/0x01/0x03 — the
    control/ack. The payload — the ciphertext (the OTA session key is in the native
    SDK, not in the RN bundle). mi_ota_decode in emulator/mcu_emu.py.

F2 (§99): углубление BLE app-протокола из плагина + snoop (без железа).

(1) Полная таблица siid/piid свойств из плагина Mi Home (modules/10724.js —
    global.SIID_DIC + global.SIID_N): SIID_1..6 (9/18/12/9/27/5 свойств),
    словарь PROP_VALUE_TYPE. Сверка с NAMES probes/spec_read.py (пересечение
    равно) — MI_SIID_PIID в emulator/mcu_emu.py.
(2) Формат OTA/DFU-фреймов (siid=0xF5) из logs/btsnoop_hci.log (97 фреймов,
    handles 0x38 app->dev / 0x3A dev->app ack / 0x44 alt):
    [0xF5][piid][N][marker:2 LE][sub:4][cls:1][payload:N+1], total = 11+N;
    N=0 → переменный payload (до ~234Б, MTU-4). marker: 0xFFFF — малые фреймы,
    0x5300/0x5600/0x5501 — чанк-фреймы 208Б, 0x005C/0x00DE/... — фреймы 16-32Б.
    cls: 0x80/0xA0/0x90 — data-write, 0x00/0x01/0x03 — control/ack. Payload —
    шифртекст (ключ OTA-сессии в native SDK, не в RN-бандле). mi_ota_decode в
    emulator/mcu_emu.py.
"""

import os  # noqa: E402

from fv_core import *  # noqa: F401,F403
from emulator.mcu_emu import (MI_BLE_SIID_OTA, MI_SIID_PIID,  # noqa: E402
                              MI_PROP_VALUE_TYPE, MI_OTA_HANDLE_APP2DEV,
                              MI_OTA_HANDLE_DEV2APP, MI_OTA_HANDLE_ALT,
                              mi_ota_decode)


def _snoop_ota_frames():
    """Parse the btsnoop (the implicit-length records, the signature 0x9E36E300)
    and return the (handle, value) pairs of the siid=0xF5 frames.
    Разобрать btsnoop (записи с неявной длиной, сигнатура 0x9E36E300) и вернуть
    пары (handle, value) фреймов siid=0xF5."""
    import struct as _st
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..',
                        'logs', 'btsnoop_hci.log')
    if not os.path.exists(path):
        return None
    d = open(path, 'rb').read()
    sig = b'\x00\xE3\x36\x9E'
    i = 0
    starts = []
    while True:
        i = d.find(sig, i)
        if i < 0:
            break
        starts.append(i - 16)
        i += 1
    starts.sort()
    out = []
    for idx in range(len(starts)):
        s = starts[idx]
        e = starts[idx + 1] if idx + 1 < len(starts) else len(d)
        p = d[s + 24:e]
        if p[0] != 0x02:
            continue
        j = 0
        while j + 3 <= len(p):
            if p[j] in (0x52, 0x1B, 0x12) and p[j + 2] == 0x00:
                h = p[j + 1]
                if h in (MI_OTA_HANDLE_APP2DEV, MI_OTA_HANDLE_DEV2APP,
                         MI_OTA_HANDLE_ALT):
                    v = p[j + 3:]
                    if v and v[0] == MI_BLE_SIID_OTA:
                        out.append((h, p[j], v))
                    j += 3
                    continue
            j += 1
    return out


@t(0x211F8, 'F2 §99(1): полная таблица siid/piid из плагина Mi Home (modules/10724.js): SIID_1..6 (9/18/12/9/27/5 свойств) + PROP_VALUE_TYPE; сверка с NAMES spec_read (пересечение равно) — MI_SIID_PIID/MI_PROP_VALUE_TYPE')
def _(run, rng):
    """The F2 siid/piid table test: the plugin table vs the spec_read NAMES.
    Тест F2 таблицы siid/piid: таблица плагина vs NAMES spec_read."""
    # размеры таблицы
    assert len(MI_SIID_PIID[1]) == 9, "SIID_1: 9 свойств"
    assert len(MI_SIID_PIID[2]) == 18, "SIID_2: 18 свойств"
    assert len(MI_SIID_PIID[3]) == 12, "SIID_3: 12 свойств"
    assert len(MI_SIID_PIID[4]) == 9, "SIID_4: 9 свойств"
    assert len(MI_SIID_PIID[6]) == 5, "SIID_6: LOG_1..5"
    # ключевые свойства
    assert MI_SIID_PIID[3][6] == "OOB_CODE"
    assert MI_SIID_PIID[4][2] == "BATTERY_SN" and MI_SIID_PIID[4][4] == "SCOOTER_SN"
    assert MI_SIID_PIID[2][13] == "TCS" and MI_SIID_PIID[2][16] == "ATMOSPHERE_LIGHT"
    # PROP_VALUE_TYPE
    assert MI_PROP_VALUE_TYPE[9] == "FLOAT" and MI_PROP_VALUE_TYPE[10] == "STRING"
    # сверка с NAMES spec_read (пересечение должно быть равно)
    import probes.spec_read as sr  # noqa: F401  (может быть недоступен — тогда skip)
    for siid, table in MI_SIID_PIID.items():
        for piid, name in table.items():
            if (siid, piid) in sr.NAMES:
                assert sr.NAMES[(siid, piid)] == name, \
                    f"расхождение {(siid, piid)}: {sr.NAMES[(siid, piid)]} != {name}"


@t(0x211F8, 'F2 §99(2): OTA-формат siid=0xF5 из snoop (logs/btsnoop_hci.log, 97 фреймов): [F5][piid][N][marker:2 LE][sub:4][cls:1][payload:N+1]; handles 0x38/0x3A/0x44; marker 0xFFFF/0x5300..; cls 0x80/0xA0/0x90 (write) и 0x00/0x01/0x03 (ack) — mi_ota_decode сверен с реальными фреймами')
def _(run, rng):
    """The F2 OTA-format test: mi_ota_decode verified on the real snoop frames.
    Тест F2 OTA-формата: mi_ota_decode сверен с реальными snoop-фреймами."""
    frames = _snoop_ota_frames()
    if frames is None:
        return  # snoop-лог отсутствует — статика пропущена
    assert len(frames) >= 90, f"ожидается >=90 OTA-фреймов, получено {len(frames)}"
    handles = set()
    markers = set()
    classes = set()
    ns = set()
    for h, op, v in frames:
        handles.add(h)
        r = mi_ota_decode(v)
        assert r is not None, f"не декодировался: {v[:12].hex()}"
        assert r['siid'] == 0xF5
        markers.add(r['marker'])
        classes.add(r['cls'])
        ns.add(r['n'])
    assert handles <= {0x38, 0x3A, 0x44}, f"handles: {handles}"
    assert 0x38 in handles and 0x3A in handles, "каналы 0x38/0x3A отсутствуют"
    assert 0xFFFF in markers, "маркер 0xFFFF (малые фреймы) отсутствует"
    # cls: data-write + control/ack
    assert classes <= {0x00, 0x01, 0x02, 0x03, 0x80, 0x90, 0xA0, 0x90}, \
        f"cls: {classes}"
    assert 0x80 in classes or 0x90 in classes, "data-write cls не найден"
    # N: малые (16/32/48) + переменный (0) + чанк 208 (0xD0)
    assert 0x10 in ns or 0x20 in ns, f"малые N: {ns}"
    # piid=1 встречается (rec1416)
    piids = {mi_ota_decode(v)['piid'] for _, _, v in frames}
    assert piids <= {0, 1}, f"piid: {piids}"
    assert 1 in piids, "piid=1 не найден"
