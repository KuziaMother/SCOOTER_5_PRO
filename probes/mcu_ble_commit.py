#!/usr/bin/env python3
"""
ФИНАЛЬНЫЙ ШАГ: switchFirmware(MCU, опкод 6) — активация staged-образа по BLE.

Явно одобрен пользователем (2026-08-22). Образ v0007 байт-в-байт идентичен
работающему; MCU-таргет принятие той же версии задокументировано (UART dfu_active).

Ожидаемый сценарий: ответ status 0 -> MCU сам прошивает себя по USART3
(асинхронно, до ~3 мин, как в Mi Home) -> ребут -> версия остаётся 0007,
staging очищается. Для той же версии «смена» НЕ ожидается: корректный исход —
таймаут опроса без смены (False) или тишина+возврат (None = ребут был).

Одна команда; далее только read-only опрос версии ([01] на 0x001c).

Запуск:  python probes/mcu_ble_commit.py
"""
import asyncio
import os
import struct
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "core"))
from dreame_auth import Transport, MAC_DEFAULT, LTMK_HEX, CH_DFU_CMD  # noqa: E402
from dreame_flasher import login, poll_mcu_version, OPS  # noqa: E402


async def main():
    ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
    t = Transport(MAC_DEFAULT)
    try:
        await login(t, ltmk)

        print("\n>>> switchFirmware(6) — АКТИВАЦИЯ (необратимо, одобрено)...")
        frame = struct.pack("<HB", OPS["mcu"]["switch"], 4) + struct.pack("<I", 1)
        while not t.rx.empty():
            t.rx.get_nowait()
        await t.client.write_gatt_char(t.chars[CH_DFU_CMD], frame, response=True)

        # Ответ может прийти не сразу (устройство начинает ретрансляцию) — ждём до 15 с.
        resp = None
        deadline = time.time() + 15.0
        while time.time() < deadline and resp is None:
            for s, b in await t.drain(1.0):
                if s == CH_DFU_CMD and len(b) >= 3 and b[0] == 0x01:
                    resp = b
                    break
        if resp:
            st = resp[4] if len(resp) >= 5 else None
            print(f"[i] ответ: {resp.hex()} -> status={st} "
                  f"({'принято' if st == 0 else 'ОТКЛОНЕНО/неизвестно'})")
        else:
            print("[!] ответа на switchFirmware за 15 с не было — продолжаю опрос версии")

        res = await poll_mcu_version(t, expected_before=None, timeout=180.0, interval=3.0)
        meaning = {
            True: "версия СМЕНИЛАСЬ (для той же версии неожиданно!)",
            False: "версия не менялась — для переустановки той же версии ЭТО ОЖИДАЕМО",
            None: "была тишина и возврат — MCU ребутнулся (активация шла)",
        }[res]
        print(f"\n[i] ИТОГ ОПРОСА: {meaning}")
        return 0
    finally:
        await t.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
