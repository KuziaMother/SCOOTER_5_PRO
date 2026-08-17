#!/usr/bin/env python3
"""
Перебор опкодов MCU-канала 0x001c (без логина) в поисках телеметрии
(батарея, скорость, пробег, температура, ошибки).

БЕЗОПАСНОСТЬ: отправляются ТОЛЬКО однобайтовые кадры [op] — в протоколе MCU
геттер = [op], сеттер = [op][len][data]. Без len-байта устройство не может
принять полезную нагрузку, поэтому перебор смещён в сторону чтения.

Известные (уже разобранные) опкоды: 0, 1=mcu_version, 3=hardware, 8=serial.

Запуск:  python mcu_opcode_sweep.py [--max 63] [--mac 2C:19:5C:DE:DE:88]
"""
import argparse
import asyncio

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

from dreame_auth import Transport, MAC_DEFAULT, CH_MCU, sid

KNOWN = {0: "?", 1: "mcu_version", 3: "hardware", 8: "serial/newSN"}


def describe(payload: bytes) -> str:
    """Догадки о смысле полезной нагрузки."""
    hints = []
    if payload and all(32 <= c < 127 for c in payload):
        hints.append(f"ascii='{payload.decode('ascii')}'")
    if len(payload) == 1:
        v = payload[0]
        hints.append(f"u8={v}")
        if 0 <= v <= 100:
            hints.append("МОЖЕТ БЫТЬ %")
    if len(payload) == 2:
        le = int.from_bytes(payload, "little")
        be = int.from_bytes(payload, "big")
        hints.append(f"u16le={le} u16be={be}")
        for name, val in (("le", le), ("be", be)):
            if 3000 <= val <= 4300:
                hints.append(f"МОЖЕТ БЫТЬ мВ ячейки ({name})")
            elif 30000 <= val <= 45000:
                hints.append(f"МОЖЕТ БЫТЬ мВ пакета/10 ({name})")
    if len(payload) == 4:
        hints.append(f"u32le={int.from_bytes(payload, 'little')}")
    if len(payload) >= 4 and len(payload) % 2 == 0:
        words = [int.from_bytes(payload[i:i + 2], "little")
                 for i in range(0, len(payload), 2)]
        hints.append(f"u16le[]={words}")
    return "  ".join(hints)


async def sweep(mac: str, max_op: int, repeat: int, step_wait: float = 1.0):
    t = Transport(mac)
    await t.connect()
    if CH_MCU not in t.chars:
        print("[!] характеристика 0x001c не найдена")
        return

    inbox = []

    def on_mcu(sender, data):
        if sid(sender) == CH_MCU:
            inbox.append(bytes(data))

    # ядро уже подписалось в connect(); добавим свой сборщик
    await t.client.start_notify(t.chars[CH_MCU], on_mcu)

    async def query(op: int, wait: float = 1.0):
        inbox.clear()
        await t.client.write_gatt_char(t.chars[CH_MCU], bytes([op]), response=False)
        await asyncio.sleep(wait)
        return list(inbox)

    print(f"\n=== перебор опкодов 0..{max_op} на 0x001c ===\n")
    found, silent = [], []
    # err 0x02 = опкода нет; любой другой код = опкод ЕСТЬ, но кадр не подошёл
    unsupported, needs_param = [], []

    for op in range(max_op + 1):
        replies = await query(op, wait=step_wait)
        tag = f"[{KNOWN[op]}]" if op in KNOWN else ""
        if not replies:
            silent.append(op)
            print(f"op {op:>3} {tag:<14} — тишина")
            continue
        for r in replies:
            if r and r[0] == 0xFF:
                err = r[3] if len(r) > 3 else None
                if err == 0x02:
                    unsupported.append(op)
                    print(f"op {op:>3} {tag:<14} нет опкода   {r.hex()}")
                else:
                    needs_param.append((op, err))
                    print(f"op {op:>3} {tag:<14} ЕСТЬ, err=0x{err:02x} <<<  {r.hex()}")
                continue
            payload = r[2:2 + r[1]] if len(r) >= 2 else b""
            found.append((op, r, payload))
            print(f"op {op:>3} {tag:<14} OK   raw={r.hex()}")
            if payload:
                print(f"{'':>21}{describe(payload)}")

    # повторный опрос найденных: что меняется = живая телеметрия
    if repeat and found:
        print(f"\n=== повторный опрос отвечающих опкодов ({repeat} проходов) ===")
        history = {op: [] for op, _, _ in found}
        for _ in range(repeat):
            for op in list(history):
                replies = await query(op, wait=0.6)
                r = replies[0] if replies else b""
                history[op].append(r.hex())
            await asyncio.sleep(0.5)
        print("\n--- динамика ---")
        for op, vals in history.items():
            uniq = len(set(vals))
            mark = "ИЗМЕНЯЕТСЯ <<<" if uniq > 1 else "статично"
            print(f"op {op:>3}: {mark}  {vals}")

    print("\n=== ИТОГ ===")
    print(f"отдали данные      : {[op for op, _, _ in found]}")
    print(f"ЕСТЬ, нужен параметр: {[(op, hex(e)) for op, e in needs_param]}")
    print(f"нет опкода (err 02) : {len(unsupported)} шт: {unsupported}")
    print(f"тишина              : {silent}")

    try:
        await t.client.stop_notify(t.chars[CH_MCU])
    except Exception:
        pass
    await t.client.disconnect()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mac", default=MAC_DEFAULT)
    ap.add_argument("--max", type=int, default=63, help="верхняя граница опкода")
    ap.add_argument("--repeat", type=int, default=3,
                    help="проходов повторного опроса найденных (0 = выключить)")
    ap.add_argument("--wait", type=float, default=1.0,
                    help="пауза после каждого опкода, с")
    a = ap.parse_args()
    asyncio.run(sweep(a.mac, a.max, a.repeat, a.wait))


if __name__ == "__main__":
    main()
