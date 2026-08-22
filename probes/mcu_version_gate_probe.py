#!/usr/bin/env python3
"""
Проба: что именно устройство проверяет на MCU-фрагменте 1 (отказ status 5)?

Гипотеза H1: сравнение «версия образа vs установленная», версия читается из
заголовка образа @0x22 ("0007"). Подпись/сертификат в трейлере (@0x24807+),
т.е. в фрагменте 1 НЕТ — проверить её на этом этапе устройство не может.

Эксперимент: отправить ТОЛЬКО фрагмент 1 с "0007"->"0008" в заголовке.
  status=0 -> гейт = версионная строка (H1), нам нечего упускать;
  status=5 -> проверяется что-то ещё (другое поле / предварительное состояние).

Безопасность: switchFirmware НЕ отправляется, других фрагментов нет. Один
фрагмент в staging-буфер: незавершённый DFU устройство сбрасывает само, а
будущая легитимная заливка начнётся с нуля (resume-CRC не совпадёт —
dreame_flasher это обрабатывает). Одна попытка за прогон.

Запуск:  python probes/mcu_version_gate_probe.py
"""
import asyncio
import sys
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.join(_ROOT, "core"))
from dreame_auth import Transport, MAC_DEFAULT, LTMK_HEX  # noqa: E402
from dreame_flasher import login, get_fragment_size, get_last_index, send_fragment, OPS  # noqa: E402

IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "firmware_ota",
                   "c0f78c49f322bd3d71fea19c90241882_mcu_xiaomi.scooter.5pro_v0007.bin")
VER_OFF = 0x22          # ASCII-версия в заголовке MCU-образа (FACTS.md)


async def main():
    ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
    t = Transport(MAC_DEFAULT)
    try:
        await login(t, ltmk)
        op = OPS["mcu"]
        frag_size = await get_fragment_size(t, op)
        if not frag_size:
            print("[!] getFragmentSize не ответил"); return 1
        last, crc = await get_last_index(t, op)
        fw = open(IMG, "rb").read()
        assert len(fw) > frag_size
        tampered = bytearray(fw[:frag_size])
        orig_ver = bytes(tampered[VER_OFF:VER_OFF + 4])
        tampered[VER_OFF:VER_OFF + 4] = b"0008"
        print(f"[i] заголовок: версия {orig_ver!r} -> b'0008' (только фрагмент 1, без commit)")
        st = await send_fragment(t, 1, bytes(tampered))
        if st is None:
            print("[!] сбой транспорта — нет ACK/события")
            return 1
        status_txt = {0: "ПРИНЯТ (status 0) — гейт = версионная строка",
                      5: "отклонён (status 5) — проверяется что-то ещё"}.get(st, f"статус={st}")
        print(f"[i] фрагмент 1 (версия 0008): {status_txt}")
        last2, crc2 = await get_last_index(t, op)
        print(f"[i] состояние буфера после: last={last2}, crc={'%08x' % crc2 if crc2 else '—'}")
        return 0
    finally:
        await t.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
