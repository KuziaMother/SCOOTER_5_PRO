#!/usr/bin/env python3
"""
Проба 3: что означает status 7 — «отклонено и не буферизовано» или «буферизовано с флагом»?

Последовательность (одна сессия, без commit, чистые банки):
  frag1 -> статус A (ожидаем 7)
  frag1 ещё раз -> статус B:
      5 = «дубликат/неверный индекс»  ⇒ первый фрагмент ЛЕГ в буфер несмотря на 7;
      7 = состояние не изменилось     ⇒ 7 = чистый отказ, ничего не буферизовано.
  frag2 -> статус C:
      если B=5 и C=0 — буферизация идёт «вслепую», гейт срабатывает позже;
      если C=5 — пропуск индекса тоже виден устройству.

Печатает полные сырые события 0x0017 (без фильтрации) — вдруг в них больше байт.

Запуск:  python probes/mcu_gate_repeat.py
"""
import asyncio
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "core"))
from dreame_auth import Transport, MAC_DEFAULT, LTMK_HEX  # noqa: E402
from dreame_flasher import (login, get_fragment_size, get_last_index,
                            send_fragment, OPS)  # noqa: E402

MCU_IMG = os.path.join(ROOT, "firmware_ota",
                       "c0f78c49f322bd3d71fea19c90241882_mcu_xiaomi.scooter.5pro_v0007.bin")


async def main():
    ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
    t = Transport(MAC_DEFAULT)
    try:
        await login(t, ltmk)
        op = OPS["mcu"]
        last, crc = await get_last_index(t, op)
        if last != 0:
            print(f"[!] MCU-банк не пуст (last={last}) — тест невалиден")
            return 1
        frag_size = await get_fragment_size(t, op)
        fw = open(MCU_IMG, "rb").read()

        for idx in (1, 1, 2):
            st = await send_fragment(t, idx, fw[(idx - 1) * frag_size: idx * frag_size])
            print(f"[i] frag{idx}: status={st}")

        last2, crc2 = await get_last_index(t, op)
        print(f"[i] MCU-банк после: last={last2}, crc={'%08x' % crc2 if crc2 else '—'}")
        return 0
    finally:
        await t.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
