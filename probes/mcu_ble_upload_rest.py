#!/usr/bin/env python3
"""
Проба 4: завершить заливку MCU-образа по BLE с фрагмента 3 (1–2 уже в staging).

Модель (проверена пробами 1–3):
  status 0 = фрагмент принят и лёг в MCU-staging;
  status 5 = дубликат индекса (уже в staging) + закрытие сессии;
  status 7 = MCU временно «не готов» (транзиент после ребута);
  lastFragmentIndex(5) НЕ отражает реальное состояние staging (отдаёт 0).

Безопасность: switchFirmware(6) НЕ отправляется. При любом статусе != 0 на
новом индексе — стоп и отчёт (модель неверна, не спамим дальше).

Запуск:  python probes/mcu_ble_upload_rest.py [START]   (START по умолчанию 3)
"""
import asyncio
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "core"))
from dreame_auth import Transport, MAC_DEFAULT, LTMK_HEX  # noqa: E402
from dreame_flasher import login, get_fragment_size, get_last_index, send_fragment, OPS  # noqa: E402

MCU_IMG = os.path.join(ROOT, "firmware_ota",
                       "c0f78c49f322bd3d71fea19c90241882_mcu_xiaomi.scooter.5pro_v0007.bin")


async def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
    t = Transport(MAC_DEFAULT)
    try:
        await login(t, ltmk)
        op = OPS["mcu"]
        frag_size = await get_fragment_size(t, op)
        fw = open(MCU_IMG, "rb").read()
        N = -(-len(fw) // frag_size)
        print(f"[i] фрагменты {start}..{N} (всего {N}), без commit")

        t0 = time.time()
        n_ok = n_bad = 0
        for idx in range(start, N + 1):
            data = fw[(idx - 1) * frag_size: idx * frag_size]
            st = await send_fragment(t, idx, data)
            if st is None:
                print(f"\n[!] frag{idx}: сбой транспорта — стоп (ok={n_ok}, bad={n_bad})")
                return 1
            if st == 0:
                n_ok += 1
            else:
                n_bad += 1
                print(f"\n[~] frag{idx}: статус={st} (не 0!) — стоп, модель неверна "
                      f"(ok={n_ok}, bad={n_bad})")
                return 1
            if idx % 10 == 0 or idx == N:
                spd = (idx - start + 1) / max(time.time() - t0, 0.1)
                eta = (N - idx) / max(spd, 0.1)
                print(f"\r  frag {idx}/{N} ok={n_ok} bad={n_bad} "
                      f"{spd:.1f}фр/с ETA {eta:.0f}s   ", end="", flush=True)
        dt = time.time() - t0
        print(f"\n[i] завершено за {dt:.0f}s: ok={n_ok}, bad={n_bad}")
        last, crc = await get_last_index(t, op)
        print(f"[i] lastFragmentIndex(5) после: last={last}, crc={'%08x' % crc if crc else '—'} "
              f"(известно: не отражает staging)")
        print("[i] switchFirmware(6) НЕ отправлен — образ в staging, ждёт решения")
        return 0
    finally:
        await t.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
