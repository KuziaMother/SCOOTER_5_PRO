#!/usr/bin/env python3
"""
Проба 2: версионный гейт MCU при ЧИСТОМ BLE-банке.

Предыдущая проба показала двухступенчатый гейт:
  - грязный BLE-банк (last!=0)  -> MCU-фрагмент 1: status 5 (конфликт сессий);
  - чистый BLE-банк (last=0)    -> MCU-фрагмент 1: status 7 (реальный гейт).

Ранний тест «0008 в заголовке» был невалиден (банк был грязен -> 5).
Повторяем его при чистом банке:
  - status=0 -> гейт = сравнение версий из заголовка @0x22; всё объяснено;
  - status=7 -> проверка использует и другие поля (или не версию).

Безопасность: без switchFirmware(6); один фрагмент; банки проверяем и при
нужном сбрасываем BLE-банк штатным механизмом (switchFirmware(4) на той же
версии = отказ status 6 + сброс банка, проверено).

Запуск:  python probes/mcu_gate_clean_version.py
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
VER_OFF = 0x22


async def ensure_clean_ble_bank(t):
    last, crc = await get_last_index(t, OPS["ble"])
    if last == 0:
        print("[i] BLE-банк чист (last=0)")
        return True
    print(f"[i] BLE-банк грязен (last={last}) — сброс штатным switchFirmware(4)...")
    r = await dfu_cmd(t, OPS["ble"]["switch"], struct.pack("<I", 1))
    st = r[4] if r and len(r) >= 5 else None
    print(f"[i] ответ: {r.hex() if r else None} status={st}")
    last2, _ = await get_last_index(t, OPS["ble"])
    print(f"[i] BLE-банк после сброса: last={last2}")
    return last2 == 0


async def main():
    ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
    t = Transport(MAC_DEFAULT)
    try:
        await login(t, ltmk)

        if not await ensure_clean_ble_bank(t):
            print("[!] не удалось получить чистый BLE-банк — прекращаю")
            return 1

        op = OPS["mcu"]
        lastm, crcm = await get_last_index(t, op)
        if lastm != 0:
            print(f"[!] MCU-банк НЕ пуст (last={lastm}) — нужен авто-сброс/перезагрузка, "
                  f"иначе тест невалиден")
            return 1

        frag_size = await get_fragment_size(t, op)
        fw = open(MCU_IMG, "rb").read()
        tampered = bytearray(fw[:frag_size])
        tampered[VER_OFF:VER_OFF + 4] = b"0008"
        print("[i] MCU-фрагмент 1 с версией b'0008' (чистые банки)")
        st = await send_fragment(t, 1, bytes(tampered))
        if st is None:
            print("[!] сбой транспорта")
            return 1
        txt = {0: "ПРИНЯТ — гейт = версионная строка заголовка",
               7: "status 7 — версия читается не только из @0x22 / проверяется иначе"}.get(
            st, f"статус={st} (новый код)")
        print(f"[i] результат: {txt}")
        return 0
    finally:
        await t.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
