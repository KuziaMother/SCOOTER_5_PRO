#!/usr/bin/env python3
"""
Заливка patched_mi5pro_firmware.bin по BLE (MCU-таргет), устойчивая к состояниям.

Модель (docs/FACTS.md, 2026-08-22 + наблюдения этой сессии):
  frag-status 0 = принят в MCU-staging; 5 = «не принять» (дубликат индекса в
  персистентном staging И/или грязный BLE-банк) — после 5 сессия закрывается;
  7 = MCU «не готов» (транзиент, повтор через время проходит).
  switchFirmware(4, param=1) на неполном/своем банке: отклоняется status 6,
  OTA-буфер сбрасывается (проверено), но за ним следует транзиент «не готов»
  на несколько минут.
  Стаaging читается только пробой: 5 = индекс уже есть, 0 = его не было (и он
  теперь принят).

Алгоритм:
  1. login → warm-up (getFragmentSize) → состояние BLE-банка (только показ).
  2. Проба MCU-frag1 (патченный):
       0 → staging пуст → залить 2..N → commit switchFirmware(6). ГОТОВО.
       5 → если банк грязный: безопасный сброс (switchFirmware(4), только при
           неполном банке или банке = текущей официальной версии) + ожидание
           транзиента + повтор пробы frag1;
           если всё равно 5 → картируем staging пробами 2..10 (каждая проба
           либо подтверждает индекс, либо принимает недостающий) → resume 11..N.
       7/тишина → ретраи с паузами.
  3. commit switchFirmware(6) — ТОЛЬКО после того, как в staging гарантированно
     полный образ (все индексы подтверждены/приняты со status 0).

Запуск:  python custom_mcu/ble_flash_patched.py
"""
import asyncio
import os
import struct
import sys
import time
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "core"))
from dreame_auth import Transport, MAC_DEFAULT, LTMK_HEX, dfu_cmd  # noqa: E402
from dreame_flasher import (  # noqa: E402
    login, send_fragment, poll_mcu_version, OPS, _cmd_value,
)

PATCHED = os.path.join(ROOT, "custom_mcu", "patched_mi5pro_firmware.bin")
OFFICIAL_MCU = os.path.join(ROOT, "firmware_ota",
                            "c0f78c49f322bd3d71fea19c90241882_mcu_xiaomi.scooter.5pro_v0007.bin")
OFFICIAL_BLE = os.path.join(ROOT, "firmware_ota",
                            "0d41b4df91f8d37b5f1355484e2b93c3_upd_xiaomi.scooter.5pro_v2.7.0_0015.bin")

LTMK = bytes.fromhex(open(LTMK_HEX).read().strip())
RETRY = 4            # повторов на тишину/статус 7
WAIT_SLOW = 60.0     # пауза на статус 7, с
WAIT_SILENT = 30.0   # пауза на тишину, с
RESET_WAIT = 150.0   # ожидание транзиента после switchFirmware(4), с


def log(msg=""):
    print(msg, flush=True)


async def fresh_session(label):
    t = Transport(MAC_DEFAULT)
    await login(t, LTMK)
    log(f"[+] сессия «{label}»")
    return t


async def _cmd_value_retry(t, op, what, total=120.0):
    deadline = time.time() + total
    attempt = 0
    while time.time() < deadline:
        attempt += 1
        st, v = await _cmd_value(t, op, timeout=max(2.0, min(10.0, deadline - time.time())))
        if st == 0 and v is not None:
            return v
        log(f"[~] {what}: нет ответа (попытка {attempt}, осталось {deadline - time.time():.0f} с)")
    return None


async def read_frag_size(t, op, total=300.0):
    v = await _cmd_value_retry(t, op["frag"], "getFragmentSize", total=total)
    if v is None or len(v) < 2:
        return None
    return struct.unpack_from("<H", v, 0)[0]


async def read_last(t, op, what="lastFragmentIndex", total=60.0):
    v = await _cmd_value_retry(t, op["last"], what, total=total)
    if v is None or len(v) < 2:
        return None, None
    idx = struct.unpack_from("<H", v, 0)[0]
    crc = struct.unpack_from("<I", v, 2)[0] if len(v) >= 6 else None
    return idx, crc


async def reset_ble_bank(t):
    """switchFirmware(4, param=1): отклоняется (status 6), буфер → 0. Ждём транзиент."""
    r = await dfu_cmd(t, OPS["ble"]["switch"], struct.pack("<I", 1))
    st = r[4] if r and len(r) >= 5 else None
    log(f"    switchFirmware(4) resp: {r.hex() if r else None} -> status={st}")
    if st != 6:
        log("[!] неожиданный ответ на switchFirmware(4)")
    log(f"    транзиент «не готов»: жду {RESET_WAIT:.0f} с…")
    await asyncio.sleep(RESET_WAIT)


async def send_with_retries(t, fw, frag, index):
    """send_fragment с ретраями на тишину/7. Возвращает статус (int/None)."""
    data = fw[(index - 1) * frag: index * frag]
    st = await send_fragment(t, index, data)
    tries = 0
    while st in (None, 7) and tries < RETRY:
        tries += 1
        wait = WAIT_SLOW if st == 7 else WAIT_SILENT
        log(f"[~] frag{index}: status={st!r} — жду {wait:.0f} с, повтор {tries}/{RETRY}")
        await asyncio.sleep(wait)
        st = await send_fragment(t, index, data)
    return st


async def upload_range(t, fw, frag, start, end, label):
    """Залить start..end (1-based). Все должны дать status 0."""
    t0 = time.time()
    log(f"    заливка {label}: фрагменты {start}..{end}")
    for index in range(start, end + 1):
        st = await send_with_retries(t, fw, frag, index)
        if st != 0:
            log(f"\n[!] {label} фрагмент {index}/{end}: status={st!r} — стоп БЕЗ коммита "
                f"(последний подтверждённый: {index - 1})")
            return False
        if index % 10 == 0 or index == end:
            spd = (index - start + 1) / max(time.time() - t0, 0.1)
            eta = (end - index) / max(spd, 0.1)
            print(f"\r    {label}: {index}/{end} ({100 * index // end}%) "
                  f"{spd:.1f} фр/с ETA {eta:.0f}s   ", end="", flush=True)
    log(f"\n[+] {label}: все фрагменты приняты (status 0)")
    return True


async def commit_mcu(t, label):
    """switchFirmware(6, param=1) + опрос версии MCU до 3 мин."""
    log(f"\n[!!!] {label}: switchFirmware(6) — АКТИВАЦИЯ (необратимо)…")
    r = await dfu_cmd(t, OPS["mcu"]["switch"], struct.pack("<I", 1))
    st = r[4] if r and len(r) >= 5 else None
    log(f"    switchFirmware(6) resp: {r.hex() if r else None} -> status={st}")
    res = await poll_mcu_version(t, expected_before=None, timeout=180.0, interval=3.0)
    meaning = {True: "версия сменилась",
               False: "версия не менялась (ожидается для переустановки 0007)",
               None: "тишина+возврат — MCU ребутнулся (активация шла)"}
    log(f"[i] опрос версии: {meaning[res]}")
    return st


async def finish_upload(t, patched, frag, start, N, label):
    if not await upload_range(t, patched, frag, start, N, label):
        return False
    await commit_mcu(t, "патченный образ")
    log("\n[===] ГОТОВО: патченный MCU-образ активирован по BLE")
    return True


async def main():
    patched = open(PATCHED, "rb").read()
    official_ble = open(OFFICIAL_BLE, "rb").read()
    log(f"патченный: {len(patched)} Б crc32={zlib.crc32(patched) & 0xFFFFFFFF:08x}")

    t = await fresh_session("разведка")
    try:
        frag = await read_frag_size(t, OPS["mcu"])
        if not frag:
            log("[!] getFragmentSize(MCU) не ответил — устройство в транзиенте. "
                "Подожди несколько минут и запусти заново.")
            return 1
        N = -(-len(patched) // frag)
        log(f"[i] MCU fragmentSize={frag}, всего фрагментов={N}")

        idx_ble, crc_ble = await read_last(t, OPS["ble"], "BLE-банк")
        log(f"[i] BLE-банк: lastFragmentIndex={idx_ble}, "
            f"crc={'%08x' % crc_ble if crc_ble is not None else '—'} (только показ)")

        # ---------- 2. проба frag1 ----------
        st1 = await send_with_retries(t, patched, frag, 1)
        if st1 is None:
            log("[~] frag1: сбой транспорта — reconnect и повтор")
            await t.close()
            t = await fresh_session("повтор frag1")
            frag = await read_frag_size(t, OPS["mcu"]) or frag
            st1 = await send_with_retries(t, patched, frag, 1)
        log(f"[i] MCU-frag1 (патченный): status={st1!r}")

        if st1 == 0:
            # ---------- staging пуст: полная заливка ----------
            return 0 if await finish_upload(t, patched, frag, 2, N, "патченный") else 1

        if st1 == 5:
            # ---------- дубликат/гейт ----------
            if idx_ble is not None and idx_ble > 0:
                frag_ble = await read_frag_size(t, OPS["ble"], total=60.0) or 512
                N_ble = -(-len(official_ble) // frag_ble)
                local_crc = zlib.crc32(official_ble[:idx_ble * frag_ble]) & 0xFFFFFFFF
                safe = (idx_ble < N_ble) or (crc_ble is not None and crc_ble == local_crc)
                log(f"[i] BLE-банк грязный ({idx_ble}/{N_ble}); содержимое совпадает с "
                    f"официальным: {crc_ble is not None and crc_ble == local_crc}")
                if safe:
                    log("[i] сброс банка безопасен (неполный или та же версия)")
                    await reset_ble_bank(t)
                    await t.close()
                    t = await fresh_session("после сброса банка")
                    frag = await read_frag_size(t, OPS["mcu"]) or frag
                    st1 = await send_with_retries(t, patched, frag, 1)
                    log(f"[i] MCU-frag1 после сброса банка: status={st1!r}")
                else:
                    log("[!] банк полный с неизвестным содержимым — стоп, решение вручную")
                    return 1

            if st1 == 0:
                return 0 if await finish_upload(t, patched, frag, 2, N, "патченный (после сброса)") else 1

            if st1 != 5:
                log(f"[!] неожиданный статус frag1: {st1!r} — стоп без коммита")
                return 1

            # ---------- картируем staging: пробы 2..N-? (здесь 2..10+ по факту до N) ----------
            log("[i] frag1 всё ещё 5 → картирую staging пробами (5 = есть, 0 = принял)")
            last_confirmed = 1
            for index in range(2, N + 1):
                stp = await send_with_retries(t, patched, frag, index)
                if stp == 5:
                    log(f"    проба {index}: 5 (уже в staging) — сессия закрыта, reconnect")
                    last_confirmed = index
                    await t.close()
                    t = await fresh_session(f"проба {index + 1}")
                    frag = await read_frag_size(t, OPS["mcu"]) or frag
                elif stp == 0:
                    last_confirmed = index
                    if index % 25 == 0:
                        log(f"    проба {index}: 0 (принят)")
                else:
                    log(f"[!] проба {index}: неожиданный статус {stp!r} — стоп без коммита")
                    return 1
            log(f"[i] staging картирован: подтверждено 1..{last_confirmed}")

            # ---------- resume ----------
            if last_confirmed >= N:
                log("[i] весь образ уже в staging — сразу commit")
                await commit_mcu(t, "патченный образ (уже полностью в staging)")
                log("\n[===] ГОТОВО: патченный MCU-образ активирован по BLE")
                return 0
            return 0 if await finish_upload(t, patched, frag, last_confirmed + 1, N,
                                            f"патченный (resume с {last_confirmed + 1})") else 1

        log(f"[!] неожиданный статус frag1: {st1!r} — стоп без коммита")
        return 1
    finally:
        try:
            await t.close()
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
