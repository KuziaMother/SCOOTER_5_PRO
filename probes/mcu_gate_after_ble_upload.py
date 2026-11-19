#!/usr/bin/env python3
"""
Probe: does the MCU gate (the status 5 on the fragment 1) open after the BLE image upload in the same session? Mi Home always flashes the BLE and the MCU in one release: first the BLE image (the opcodes 2/3/4), then the MCU (2/5/6).
Проба: открывается ли MCU-гейт (status 5 на фрагменте 1) после заливки BLE-образа
в той же сессии? Mi Home всегда шьёт BLE и MCU одним релизом: сначала BLE-образ
(опкоды 2/3/4), затем MCU (2/5/6). Наши пробы MCU шли «в одиночку» — возможно,
гейт требует предшествующей BLE-передачи в сессии.

План (ОДИН прогон, без commit):
  1. Залить ВЕСЬ BLE-образ (301 фрагмент) без switchFirmware — безопасно:
     «без --commit заливает все фрагменты, но НЕ переключает прошивку»,
     незавершённый/незакоммиченный DFU устройство сбрасывает само.
  2. Послать MCU-фрагмент 1 (чистый, версия 0007).
     status=0 -> гейт открывается после BLE-заливки (нашли, что упускали!);
     status=5 -> зависит не от передачи, а от чего-то ещё (коммита/версии).

Запуск:  python probes/mcu_gate_after_ble_upload.py
Проба: открывается ли MCU-гейт (status 5 на фрагменте 1) после заливки BLE-образа в той же сессии? Mi Home всегда шьёт BLE и MCU одним релизом: сначала BLE-образ (опкоды 2/3/4), затем MCU (2/5/6).
"""
import asyncio
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "core"))
from dreame_auth import Transport, MAC_DEFAULT, LTMK_HEX  # noqa: E402
from dreame_flasher import (login, flash, get_fragment_size, get_last_index,
                            send_fragment, OPS)  # noqa: E402

BLE_IMG = os.path.join(ROOT, "firmware_ota",
                       "0d41b4df91f8d37b5f1355484e2b93c3_upd_xiaomi.scooter.5pro_v2.7.0_0015.bin")
MCU_IMG = os.path.join(ROOT, "firmware_ota",
                       "c0f78c49f322bd3d71fea19c90241882_mcu_xiaomi.scooter.5pro_v0007.bin")


async def main():
    """The run: the BLE upload (without the commit) + the MCU fragment 1 (the gate check).
    Прогон: BLE-заливка (без commit) + MCU-фрагмент 1 (проверка гейта)."""
    ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
    t = Transport(MAC_DEFAULT)
    try:
        await login(t, ltmk)

        print("\n=== ШАГ 1: заливка BLE-образа БЕЗ commit ===")
        ok = await flash(t, BLE_IMG, "ble", commit=False)
        if not ok:
            print("[!] BLE-заливка не прошла — пробу прекращаю")
            return 1

        print("\n=== ШАГ 2: MCU-фрагмент 1 после BLE-заливки ===")
        op = OPS["mcu"]
        frag_size = await get_fragment_size(t, op)
        last, crc = await get_last_index(t, op)
        fw = open(MCU_IMG, "rb").read()
        st = await send_fragment(t, 1, fw[:frag_size])
        if st is None:
            print("[!] сбой транспорта — нет ACK/события")
            return 1
        txt = {0: "ПРИНЯТ (status 0) — ГЕЙТ ОТКРЫЛСЯ ПОСЛЕ BLE-ЗАЛИВКИ",
               5: "отклонён (status 5) — не от передачи зависит"}.get(st, f"статус={st}")
        print(f"[i] MCU-фрагмент 1: {txt}")
        return 0
    finally:
        await t.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
