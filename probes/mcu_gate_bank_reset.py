#!/usr/bin/env python3
"""
Проба: MCU-гейт закрыт, пока BLE OTA-банк «грязный»?

Факты:
  - Mi Home: BLE-образ → switchFirmware(4) [коммит/сброс банка] → MCU-образ — работает.
  - Наши пробы MCU: BLE-банк стоял на 296 (персистентное состояние, переживает
    сессии и питание, см. todo.md §C) — MCU-фрагмент 1 всегда status 5.
  - todo.md: «switchFirmware СБРАСЫВАЕТ OTA-буфер даже при отказе (status 6 → банк в 0)».

План (одна сессия, безопасно):
  1. Состояние BLE-банка (опкод 3) — ожидается 296.
  2. switchFirmware(BLE, опкод 4), param=1 — на той же версии ОТКЛОНЯЕТСЯ (status 6),
     но сбрасывает банк в 0 (проверенный механизм; переключения прошивки не происходит).
  3. Состояние BLE-банка — ожидается 0.
  4. MCU-фрагмент 1 (чистый 0007):
     status=0 -> гейт = «нет активной OTA-сессии другого таргета» (нашли упущенное!);
     status=5 -> гипотеза неверна.

Запуск:  python probes/mcu_gate_bank_reset.py
"""
import asyncio
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "core"))
from dreame_auth import Transport, MAC_DEFAULT, LTMK_HEX, dfu_cmd  # noqa: E402
from dreame_flasher import (login, get_fragment_size, get_last_index,
                            send_fragment, OPS)  # noqa: E402

MCU_IMG = os.path.join(ROOT, "firmware_ota",
                       "c0f78c49f322bd3d71fea19c90241882_mcu_xiaomi.scooter.5pro_v0007.bin")


async def main():
    ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
    t = Transport(MAC_DEFAULT)
    try:
        await login(t, ltmk)

        print("\n=== ШАГ 1: состояние BLE-банка ДО ===")
        last, crc = await get_last_index(t, OPS["ble"])
        print(f"[i] BLE-банк: last={last}, crc={'%08x' % crc if crc else '—'}")

        print("\n=== ШАГ 2: switchFirmware(BLE) — сброс банка (на той же версии будет отказ) ===")
        r = await dfu_cmd(t, OPS["ble"]["switch"], struct.pack("<I", 1))
        if r:
            # ответ [01][len][opcode u16][status][data]
            st = r[4] if len(r) >= 5 else None
            print(f"[i] ответ: {r.hex()} -> status={st} (6 = отклонено, банк всё равно сбрасывается)")
        else:
            print("[!] нет ответа на switchFirmware")

        print("\n=== ШАГ 3: состояние BLE-банка ПОСЛЕ ===")
        last2, crc2 = await get_last_index(t, OPS["ble"])
        print(f"[i] BLE-банк: last={last2}, crc={'%08x' % crc2 if crc2 else '—'} "
              f"{'(сброшен)' if last2 == 0 else '(НЕ сброшен!)'}")

        print("\n=== ШАГ 4: MCU-фрагмент 1 при чистом BLE-банке ===")
        op = OPS["mcu"]
        frag_size = await get_fragment_size(t, op)
        lastm, crcm = await get_last_index(t, op)
        fw = open(MCU_IMG, "rb").read()
        st = await send_fragment(t, 1, fw[:frag_size])
        if st is None:
            print("[!] сбой транспорта — нет ACK/события")
            return 1
        txt = {0: "ПРИНЯТ (status 0) — ГЕЙТ = ЧИСТОТА BLE-БАНКА, НАШЛИ УПУЩЕННОЕ!",
               5: "отклонён (status 5) — гипотеза о банке неверна"}.get(st, f"статус={st}")
        print(f"[i] MCU-фрагмент 1: {txt}")
        return 0
    finally:
        await t.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
