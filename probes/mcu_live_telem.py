#!/usr/bin/env python3
"""
The READ-ONLY live telemetry of the MCU via the USART3 push stream (0x61...chk 9E),
19200 8N1.

It sends NOTHING — it only listens to the spontaneous push stream and decodes the 'a0'
(sub=0x30) and the 'a1' (sub=0x31) frames. The field mapping per the RE of the
aggregator 0x211f8 + the section 47.

The goal: to take the TEMPORARY dynamics in the stationary mode (without the BLE,
without the movement):
  - the battery % (the u16@0x306) — the drift/the discharge;
  - the u16@0x308 — the counter (the increment frequency -> the tick period);
  - the temperature in degrees C;
  - the u16@0x236 (%) — the speed percent (the 0 in place);
  - the status byte of the 'a0' (the multi-flag, the codes 0x10/0x11/0x18/0x24/0x27/
    0x28/0x29/0x45).

Usage:  python probes/mcu_live_telem.py [--port COM3] [--listen 30.0]

READ-ONLY live-телеметрия MCU по USART3 push-потоку (0x61…chk 9E), 19200 8N1.

НИЧЕГО не отправляем — только слушаем спонтанный push-поток и декодируем кадры
'a0' (sub=0x30) и 'a1' (sub=0x31). Поле-маппинг по RE сборщика 0x211f8 + §47.

Цель: снять ВРЕМЕННУЮ динамику в стационарном режиме (без BLE, без движения):
  - батарея % (u16@0x306) — дрейф/разряд;
  - u16@0x308 — счётчик (частота инкремента → период тика);
  - температура °C;
  - u16@0x236 (%) — скорость-процент (0 на месте);
  - status-байт 'a0' (мульти-флаг, код 0x10/0x11/0x18/0x24/0x27/0x28/0x29/0x45).

Запуск:  python probes/mcu_live_telem.py [--port COM3] [--listen 30.0]
"""
import argparse
import time

import serial


def collect_frames(s, secs):
    """Collect the full valid push frames [(t_sec, frame), ...].
    Собираем полные валидные push-кадры [(t_sec, frame), ...]."""
    buf = bytearray()
    frames = []
    t0 = time.time()
    end = t0 + secs
    while time.time() < end:
        d = s.read(256)
        if d:
            buf += d
        i, n = 0, len(buf)
        while i < n:
            if buf[i] != 0x61:
                i += 1
                continue
            rem = n - i
            if rem < 3:
                break
            ln = buf[i + 2]
            e = i + ln + 5
            if ln > 200:
                i += 1
                continue
            if e > n:
                break
            if buf[e - 1] != 0x9E or (sum(buf[i:e - 2]) & 0xFF) != buf[e - 2]:
                i += 1
                continue
            frames.append((time.time() - t0, bytes(buf[i:e])))
            del buf[:e]
            i = 0
            n = len(buf)
    return frames


def dec_biased(raw):
    """The signed byte decoding (the biased representation of the scooter firmware):
    the raw < 128 -> the value, otherwise 128 - raw (the negative).
    Декодирование знакового байта (biased-представление прошивки самоката): raw < 128
    -> значение, иначе 128 - raw (отрицательное)."""
    return raw if raw < 128 else 128 - raw


STATUS_NAMES = {
    0x10: "st=0x10", 0x11: "st=0x11", 0x18: "st=0x18", 0x24: "st=0x24",
    0x27: "st=0x27", 0x28: "st=0x28", 0x29: "st=0x29", 0x45: "st=0x45",
}


def main():
    """The read-only telemetry run (the --port/--listen options).
    READ-ONLY прогон телеметрии (опции --port/--listen)."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM3")
    ap.add_argument("--listen", type=float, default=30.0)
    a = ap.parse_args()

    print(f"[*] слушаю {a.port} @ 19200 (READ-ONLY) {a.listen:.0f}с…")
    s = serial.Serial(a.port, 19200, timeout=0.2)
    try:
        frames = collect_frames(s, a.listen)
    finally:
        s.close()

    a0 = [(t, f) for t, f in frames if len(f) > 2 and f[1] == 0x30]
    a1 = [(t, f) for t, f in frames if len(f) > 2 and f[1] == 0x31]
    other = len(frames) - len(a0) - len(a1)
    print(f"[+] кадров: всего {len(frames)}, 'a0'={len(a0)}, 'a1'={len(a1)}, других={other}")
    if not frames:
        print("    [!] кадров нет — проверь подключение/самокат включён")
        return

    # --- 'a1' (батарея) временна́я серия ---
    print("\n=== 'a1' батарея/энергия (каждый ~2-3с) ===")
    print(f"  {'t':>5}  batt%  u16@0x308   u16@0x30a(s16)  temp°C  range  @0x2e6")
    prev308 = None
    dts = []
    vals308 = []
    for t, f in a1:
        batt = f[4]
        v308 = (f[5] << 8) | f[6]
        v30a = (f[7] << 8) | f[8]
        if v30a & 0x8000:
            v30a -= 0x10000
        temp = f[9]
        rng = (f[10] << 8) | f[11]
        d308 = "" if prev308 is None else f"  (+{v308 - prev308})"
        if prev308 is not None:
            dts.append(t - a1[0][0])
            vals308.append(v308)
        prev308 = v308
        print(f"  {t:5.1f}  {batt:5d}  {v308:9d}{d308}  {v30a:12d}  {temp:6d}  {rng:5d}  {f[3]:6d}")

    # --- 'a0' телеметрия: статистика по статусу и скорости ---
    print("\n=== 'a0' телеметрия (сводка) ===")
    if a0:
        speeds = [(f[9] << 8) | f[10] for _, f in a0]
        statuses = {}
        currs = []
        for _, f in a0:
            st = f[8]
            statuses[st] = statuses.get(st, 0) + 1
            currs.append(dec_biased(f[6]))
        print(f"  u16@0x236(скорость %): min={min(speeds)} max={max(speeds)} (0 = на месте)")
        print(f"  i16@0x31c (ток, biased): min={min(currs)} max={max(currs)}")
        ststr = ", ".join(f"0x{k:02x}×{v}" for k, v in sorted(statuses.items()))
        print(f"  status-байт распределение: {ststr}")

    # --- частота счётчика u16@0x308 ---
    if len(vals308) >= 2 and dts:
        span = dts[-1] - dts[0]
        if span > 0:
            rate = (vals308[-1] - vals308[0]) / span
            print(f"\n=== счётчик u16@0x308: Δ={vals308[-1]-vals308[0]} за {span:.1f}с → {rate:.2f}/с ===")
    print("\n[+] готово. Ничего не отправлялось.")


if __name__ == "__main__":
    main()
