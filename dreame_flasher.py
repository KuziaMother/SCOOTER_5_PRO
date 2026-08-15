#!/usr/bin/env python3
"""
Dreame Scooter 5 Pro — прошивальщик (BLE/MCU DFU) поверх реверснутого протокола.
==============================================================================

Использует транспорт и security-chip login из dreame_auth.py и заливает
официальный образ прошивки через канал FE95/0x0018.

Полностью разобранный протокол — docs/dreame_dfu_protocol.md, разделы 6.14–6.16.
Кратко (little-endian):
  Команды  (0x0017 W/RESP): [opcode u16][len u8][params]  ; ответ [01][len][opcode u16][status][data]
      2=getFragmentSize, 3=lastFragmentIndex(BLE), 5=lastFragmentIndex(MCU),
      4=switchFirmware(BLE), 6=switchFirmware(MCU)
  Данные   (0x0018):
      CTR   [00 00][00][subtype=00][frameCount u16]           -> device ACK 01 (готов)
      DATA  [seq u16][data]  seq 1-based, кадр = 18Б данных (frameSize канала по умолчанию)
      ACK   [00 00][01][status][reqSeq u16]:
              05 reqSeq = «пришли кадр reqSeq» (pull, окно=1),  00 = сообщение принято
  После приёма фрагмента device шлёт на 0x0017 событие [02][03][status][index u16]:
      status 00 = фрагмент ЗАЧТЁН, иначе отклонён (5 = та же/старая версия и т.п.).

Сообщение фрагмента = [index u16 LE][fragmentData(fragmentSize)],  index = lastIndex+1.
switchFirmware НЕОБРАТИМ (риск кирпича) — шлётся только с флагом --commit.

Использование:
    python dreame_flasher.py <ble|mcu> <firmware.bin> [MAC] [--commit] [--yes]
        (без --commit заливает все фрагменты, но НЕ переключает прошивку)

    python dreame_flasher.py <ble|mcu> <fw.bin> [--limit=K] [--burst=N] [--frame-size=N]
        --limit: залить только K фрагментов (замер скорости, коммит не отправляется)
        --burst: кадров сообщения до ожидания ACK (по умолчанию ВСЕ; 1 = старое поведение)
        --frame-size: НЕ менять — 18 фиксирован устройством (см. docs/FACTS.md)

    python dreame_flasher.py poll-mcu [MAC] [--poll-timeout СЕК]
        только опрос версии MCU (read-only) — проверить, применилась ли установка
"""

import sys
import time
import zlib
import struct
import asyncio

from dreame_auth import (
    Transport, stage_a_pubkey_exchange, stage_b_confirm, dfu_cmd, parse_cmd_resp, sid,
    CH_DFU_CMD, CH_DFU_DATA, CH_LOGIN, PKT_CTR, PKT_MNG, PKT_MNG_ACK, MAC_DEFAULT, LTMK_HEX,
)

FRAME_SIZE = 18          # frameSize канала 0x0018 — ФИКСИРОВАН устройством.
                         # Проверено: кадр 240Б -> устройство бесконечно pull'ит (249 раз),
                         # т.к. собирает сообщение по смещению seq*frameSize. Не тюнится.
BURST = 0                # сколько кадров сообщения слать до ожидания ACK; 0 = ВСЕ.
                         # Проверено: все 29 кадров подряд (пейсинг 10 мс) -> 0 pull'ов,
                         # ACK 00 + событие DFU, 3 прогона подряд. Ускорение ~2.7x.
                         # Pull (ACK 05) — механизм ВОССТАНОВЛЕНИЯ, а не окно=1:
                         # устройство просит кадры лишь когда их реально не хватает.
OPS = {
    "ble": {"frag": 2, "last": 3, "switch": 4},
    "mcu": {"frag": 2, "last": 5, "switch": 6},
}
# Коды статуса фрагмента (событие 02 03 <status>): из MeshDfuManager.status2otaCode
FRAG_STATUS = {
    0: "OK (зачтён)",
    5: "отклонён (код -505: как правило — та же/несовместимая версия прошивки)",
}


async def login(t, ltmk):
    """connect → A4/MNG → security-chip login (Stage A+B)."""
    await t.connect()
    if not await t.a4_handshake():
        raise RuntimeError("транспорт не поднялся (нет MNG)")
    for s, b in await t.drain(1.0):     # иногда MNG приходит повторно
        if s == CH_LOGIN and len(b) >= 3 and b[2] == PKT_MNG:
            await t.write(CH_LOGIN, struct.pack("<HBB", 0, PKT_MNG_ACK, 0)
                          + bytes([t.pkg_num, t.dmtu]))
    priv, dev_pub = await stage_a_pubkey_exchange(t)
    if not (dev_pub and len(dev_pub) >= 64):
        raise RuntimeError("Stage A: не получен pubkey устройства")
    ok = await stage_b_confirm(t, priv, dev_pub, ltmk, crc_be=False)
    if not ok:
        raise RuntimeError("login отклонён (0x22) — неверный ltmk/пин")
    print("[+] LOGIN OK")


async def _cmd_value(t, opcode, params=b"", timeout=2.5):
    """
    Команда 0x0017 + разбор ответа [01][len][opcode u16][status][value].
    Строго сверяет opcode ответа с запрошенным (в очереди бывают чужие пакеты).
    Возвращает (status, value_bytes) либо (None, None).
    """
    frame = struct.pack("<HB", opcode, len(params)) + params
    while not t.rx.empty():
        t.rx.get_nowait()
    try:
        await t.client.write_gatt_char(t.chars[CH_DFU_CMD], frame, response=True)
    except Exception:
        return None, None
    for s, b in await t.drain(timeout):
        if s != CH_DFU_CMD or not b or b[0] != 0x01:
            continue
        op_resp, v = parse_cmd_resp(b)
        if op_resp == opcode and v is not None and len(v) >= 1:
            return v[0], v[1:]
    return None, None


async def get_fragment_size(t, op):
    st, v = await _cmd_value(t, op["frag"])
    if st != 0 or len(v) < 2:
        return None
    return struct.unpack_from("<H", v, 0)[0]


async def get_last_index(t, op):
    """Ответ: [status][lastIndex u16][crc32 u32 LE]. Возвращает (lastIndex, crc|None)."""
    st, v = await _cmd_value(t, op["last"])
    if st != 0 or len(v) < 2:
        return 0, None
    idx = struct.unpack_from("<H", v, 0)[0]
    crc = struct.unpack_from("<I", v, 2)[0] if len(v) >= 6 else None
    print(f"    [lastFragmentIndex={idx}, device-crc32={'%08x' % crc if crc is not None else '—'}]")
    return idx, crc


async def _next_pkt(t, deadline):
    try:
        return await asyncio.wait_for(t.rx.get(), timeout=max(0.01, deadline - asyncio.get_event_loop().time()))
    except asyncio.TimeoutError:
        return None


async def send_fragment(t, index, data, timeout=5.0, frame_size=None):
    """
    Заливка одного фрагмента: сообщение [index u16][data] на 0x0018
    (CTR(fc) → окно=1: кадры 18Б, pull по ACK 05 reqSeq → ACK 00), затем ловим
    DFU-событие 0x0017 [02 03 status idx].
    Возвращает статус фрагмента: 0 = зачтён, >0 = код отказа, None = сбой транспорта.
    Один общий цикл сырого чтения очереди — чтобы не потерять событие 0x0017,
    приходящее рядом с ACK 00 на 0x0018.
    """
    fs = frame_size or FRAME_SIZE
    msg = struct.pack("<H", index) + data
    frames = [msg[i:i + fs] for i in range(0, len(msg), fs)] or [b""]
    fc = len(frames)
    loop = asyncio.get_event_loop()
    while not t.rx.empty():
        t.rx.get_nowait()

    # CTR + ждём start-ACK
    await t.write(CH_DFU_DATA, struct.pack("<HBBH", 0, PKT_CTR, 0, fc))
    deadline = loop.time() + timeout
    started = False
    while not started:
        p = await _next_pkt(t, deadline)
        if p is None:
            return None
        s, b = p
        if s == CH_DFU_DATA and len(b) >= 4 and b[0] == 0 and b[1] == 0 and b[2] == 0x01:
            started = True

    async def send_seq(n):
        await t.write(CH_DFU_DATA, struct.pack("<H", n) + frames[n - 1], response=False)

    # Окно отправки. MNG отдаёт maxPackageNum (у нас 6) — значит устройство готово
    # принять несколько кадров до подтверждения, а не строго один на round-trip.
    # burst=1 — прежнее поведение (медленно, но проверено).
    burst = fc if BURST in (0, None) else max(1, min(BURST, fc))
    for n in range(1, burst + 1):
        await send_seq(n)
        if burst > 1:
            await asyncio.sleep(0.01)   # пейсинг W/O-RESP, чтобы не терять кадры
    transport_done = False
    deadline = loop.time() + timeout
    for _ in range((fc + 80) * 3):
        p = await _next_pkt(t, deadline)
        if p is None:
            return None
        s, b = p
        # DFU-событие фрагмента на командном канале
        if s == CH_DFU_CMD and len(b) >= 3 and b[0] == 0x02 and b[1] == 0x03:
            return b[2]
        if s != CH_DFU_DATA or len(b) < 4 or b[0] != 0 or b[1] != 0 or b[2] != 0x01:
            continue
        status = b[3]
        if status == 0x00:                       # транспорт принял сообщение целиком
            transport_done = True
            deadline = loop.time() + timeout     # ждём событие 02 03
            continue
        if status == 0x05 and len(b) >= 6:       # pull: пришли reqSeq
            n = struct.unpack_from("<H", b, 4)[0]
            if 1 <= n <= fc:
                await send_seq(n)
                deadline = loop.time() + timeout
    return 0 if transport_done else None


async def flash(t, path, target, commit=False, frame_size=None, limit=None):
    op = OPS[target]
    fw = open(path, "rb").read()
    print(f"\n=== FLASH {target.upper()} : {path} ({len(fw)} байт) ===")

    frag = await get_fragment_size(t, op)
    if not frag:
        print("[!] getFragmentSize не ответил — прерываю"); return False
    last, dev_crc = await get_last_index(t, op)
    N = -(-len(fw) // frag)          # ceil
    # Безопасность резюма (аналог MeshDfuManager.checkLastFragmentIndex):
    # device-crc32 должен совпасть с CRC нашего файла до last*frag; иначе в буфере
    # чужой/битый образ — заливаем с нуля.
    if last > 0 and dev_crc is not None:
        local_crc = zlib.crc32(fw[:last * frag]) & 0xFFFFFFFF
        if local_crc != dev_crc:
            print(f"[!] resume-CRC не совпал (device={dev_crc:08x}, file={local_crc:08x}) "
                  f"— в буфере другой образ; заливаю с фрагмента 1")
            last = 0
        else:
            print(f"[i] resume-CRC OK — докачиваю с фрагмента {last + 1}")
    print(f"[i] fragmentSize={frag}, lastFragmentIndex={last}, всего фрагментов={N}")
    if last >= N:
        print("[i] устройство уже имеет все фрагменты — сразу к switchFirmware")

    t0 = time.time()
    n_ok = n_bad = 0
    stop_at = N if limit is None else min(N, last + limit)
    if stop_at < N:
        print(f"[i] --limit: заливаю только фрагменты {last+1}..{stop_at} из {N} "
              f"(замер скорости, коммит невозможен)")
    for index in range(last + 1, stop_at + 1):
        data = fw[(index - 1) * frag: index * frag]
        st = await send_fragment(t, index, data, frame_size=frame_size)
        if st is None:
            print(f"\n[!] фрагмент {index}/{N}: сбой транспорта (нет ACK 00 / нет события)")
            return False
        if st == 0:
            n_ok += 1
        else:
            n_bad += 1
            # статус != 0 не прерываем: проверяем гипотезу, что фрагмент всё равно
            # буферизуется (05 на старте сессии). Итог сверим по CRC ниже.
            if n_bad <= 3 or index == last + 1:
                print(f"\n  [~] фрагмент {index}/{N}: статус={st} ({FRAG_STATUS.get(st,'?')}) — продолжаю")
            # если ПОДРЯД много не-нулевых и ни одного OK — это реальный отказ
            if n_bad >= 8 and n_ok == 0:
                print(f"\n[!] {n_bad} фрагментов подряд со статусом !=0 и ни одного OK — отказ, прерываю")
                return False
        if index % 10 == 0 or index == N:
            spd = index / max(time.time() - t0, 0.1)
            eta = (N - index) / max(spd, 0.1)
            print(f"\r  фрагмент {index}/{N} ({100*index//N}%) ok={n_ok} bad={n_bad} "
                  f"{spd:.1f}фр/с ETA {eta:.0f}s   ", end="", flush=True)
    dt = time.time() - t0
    sent = max(stop_at - last, 0)
    kbps = (sent * frag) / max(dt, 0.001) / 1024
    print(f"\n[i] загрузка завершена за {dt:.0f}s (ok={n_ok}, статус!=0={n_bad})")
    print(f"[i] СКОРОСТЬ: кадр={frame_size or FRAME_SIZE}Б, {sent} фрагм. за {dt:.1f}s "
          f"= {kbps:.2f} КБ/с ({sent/max(dt,0.001):.2f} фрагм/с)")
    if stop_at < N:
        print("[i] --limit задан: образ залит частично, switchFirmware не отправляю.")
        return True

    # ФИНАЛЬНАЯ ПРОВЕРКА: устройство реально приняло весь образ?
    last2, crc2 = await get_last_index(t, op)
    full_crc = zlib.crc32(fw) & 0xFFFFFFFF
    exp_crc = zlib.crc32(fw[:last2 * frag]) & 0xFFFFFFFF if last2 else None
    crc2s = f"{crc2:08x}" if crc2 is not None else "—"
    print(f"[i] после загрузки: lastFragmentIndex={last2}/{N}, device-crc={crc2s}")
    accepted = (last2 >= N) and (crc2 is not None) and (crc2 == full_crc)
    if accepted:
        print(f"[+] ВЕСЬ ОБРАЗ ПРИНЯТ устройством (crc всего файла {full_crc:08x} совпал).")
    elif last2 and exp_crc is not None and crc2 == exp_crc:
        print(f"[i] принято {last2}/{N} фрагментов (crc до этого места совпал) — образ лёг частично.")
    else:
        print(f"[!] образ НЕ подтверждён: lastIndex={last2}, device-crc={crc2}, "
              f"ожидали полный {full_crc:08x}.")
        return False

    if not commit:
        print("[i] --commit не задан: switchFirmware НЕ отправляю. Образ загружен в буфер;\n"
              "    незавершённый DFU устройство сбросит само. Перезапуск с --commit завершит.")
        return True

    print("\n[!!!] switchFirmware — НЕОБРАТИМАЯ операция (риск кирпича). Отправляю…")
    r = await dfu_cmd(t, op["switch"], struct.pack("<I", 1))  # k81.OooOO0(1) = 01 00 00 00
    print(f"    switchFirmware resp: {r.hex() if r else None}")

    if target == "mcu":
        # Установка MCU асинхронная: BLE-чип ретранслирует образ в контроллер по USART3,
        # MCU прошивает себя сам. Mi Home на этом шаге опрашивает версию MCU до её смены
        # (MeshDfuManager->pollMcuVersion: кадр [01] на 0x001c). Повторяем это же.
        ok = await poll_mcu_version(t, expected_before=None)
        if ok is True:
            print("[+] MCU сообщил НОВУЮ версию — прошивка применена.")
        elif ok is False:
            print("[!] версия MCU не изменилась за отведённое время. Это НЕ значит провал:\n"
                  "    установка могла продолжаться дольше таймаута. Проверь версию позже\n"
                  "    (python probes/mcu_opcode_sweep.py --max 1 --repeat 0).")
        else:
            print("[!] MCU не отвечал на опрос версии (мог перезагружаться).")
        return True

    print("[+] Команда переключения отправлена. Устройство перезагрузится и применит прошивку.")
    return True


async def poll_mcu_version(t, expected_before=None, timeout=180.0, interval=3.0):
    """Опрос версии MCU до её смены — как MeshDfuManager->pollMcuVersion.

    Кадр — однобайтовый [0x01] (опкод 1 = mcu_version) на инфо-канал 0x001c,
    ответ: [01][len][ascii-версия]. Только чтение.

    Возвращает True (версия сменилась), False (таймаут без смены) или None (нет ответа).
    """
    CH_INFO = 0x001C
    if CH_INFO not in t.chars:
        print("    [!] характеристика 0x001c недоступна — опрос невозможен")
        return None

    inbox = []

    def on_info(sender, data):
        if sid(sender) == CH_INFO:
            inbox.append(bytes(data))

    await t.client.start_notify(t.chars[CH_INFO], on_info)

    async def read_version():
        inbox.clear()
        try:
            await t.client.write_gatt_char(t.chars[CH_INFO], b"\x01", response=False)
        except Exception as e:
            print(f"    [!] запись на 0x001c: {e}")
            return None
        await asyncio.sleep(1.0)
        for b in inbox:
            if len(b) >= 2 and b[0] == 0x01:
                return b[2:2 + b[1]].decode("ascii", "replace")
        return None

    try:
        if expected_before is None:
            expected_before = await read_version()
            print(f"    версия MCU до установки: {expected_before!r}")
        print(f"    опрос версии MCU (до {timeout:.0f} с, интервал {interval:.0f} с)…")
        loop = asyncio.get_event_loop()
        deadline = loop.time() + timeout
        seen_silence = 0
        while loop.time() < deadline:
            await asyncio.sleep(interval)
            v = await read_version()
            left = int(deadline - loop.time())
            if v is None:
                seen_silence += 1
                print(f"    [{left:>3}с] нет ответа (MCU перезагружается?)")
                continue
            seen_silence = 0
            if expected_before is not None and v != expected_before:
                print(f"    [{left:>3}с] версия сменилась: {expected_before!r} -> {v!r}")
                return True
            print(f"    [{left:>3}с] версия пока {v!r}")
        return None if seen_silence and expected_before is None else False
    finally:
        try:
            await t.client.stop_notify(t.chars[CH_INFO])
        except Exception:
            pass


async def main():
    argv = sys.argv[1:]
    args = [a for a in argv if not a.startswith("--")]
    flags = {a for a in argv if a.startswith("--")}
    poll_to = 180.0
    frame_size = None
    limit = None
    for a in argv:
        if a.startswith("--poll-timeout="):
            poll_to = float(a.split("=", 1)[1])
        elif a.startswith("--frame-size="):
            frame_size = int(a.split("=", 1)[1])
        elif a.startswith("--limit="):
            limit = int(a.split("=", 1)[1])
        elif a.startswith("--burst="):
            globals()["BURST"] = int(a.split("=", 1)[1])

    # режим «только опрос версии MCU» — ничего не прошивает
    if args and args[0] == "poll-mcu":
        mac = args[1] if len(args) > 1 else MAC_DEFAULT
        ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
        t = Transport(mac)
        try:
            await login(t, ltmk)
            res = await poll_mcu_version(t, timeout=poll_to)
            print({True: "[+] версия сменилась",
                   False: "[i] версия не менялась за отведённое время",
                   None: "[!] MCU не отвечал"}[res])
            return 0
        except Exception:
            import traceback; traceback.print_exc(); return 1
        finally:
            await t.close()

    if len(args) < 2 or args[0] not in OPS:
        print(__doc__); return 2
    target, path = args[0], args[1]
    mac = args[2] if len(args) > 2 else MAC_DEFAULT
    commit = "--commit" in flags

    if commit and "--yes" not in flags:
        print("[!] --commit требует также --yes (подтверждение необратимой заливки).")
        return 2

    ltmk = bytes.fromhex(open(LTMK_HEX).read().strip())
    t = Transport(mac)
    try:
        await login(t, ltmk)
        ok = await flash(t, path, target, commit=commit,
                         frame_size=frame_size, limit=limit)
        return 0 if ok else 1
    except Exception:
        import traceback; traceback.print_exc(); return 1
    finally:
        await t.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
