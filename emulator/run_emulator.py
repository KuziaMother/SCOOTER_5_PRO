#!/usr/bin/env python3
"""
Прогон настоящих инструментов проекта против эмулятора устройства (без BLE).

Подменяет dreame_auth.BleakClient на FakeBleakClient и запускает:
  1) login (dreame_auth Stage A+B) — проверка крипто round-trip;
  2) DFU BLE той же версии -> switchFirmware отвергнут (status 6), как на железе;
  3) DFU BLE НОВОЙ версии -> switchFirmware ПРИМЕНЁН, версия поднялась
     (то, чего живой самокат не позволяет — та же версия уже стоит);
  4) info-канал 0x001c: версии/железо/серийник.

Запуск:  python emulator/run_emulator.py
"""
import asyncio
import os
import struct
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "probes"))

import dreame_auth as da
import fake_ble
from scooter_device import ScooterDevice

# --- общий эмулируемый экземпляр устройства (один на прогон) ---
DEVICE = {"obj": None}


def make_device():
    return DEVICE["obj"]


def install_fake():
    fake_ble.FakeBleakClient._device_factory = make_device
    da.BleakClient = fake_ble.FakeBleakClient       # подмена в ядре


def make_fake_image(size, tag=b"EMUIMG"):
    """Псевдо-образ нужного размера (детерминированный, чтобы CRC совпадал)."""
    body = bytearray()
    i = 0
    while len(body) < size:
        body += struct.pack("<I", i) + tag
        i += 1
    return bytes(body[:size])


async def scenario_login():
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 1: login (крипто round-trip)")
    print("=" * 60)
    import dreame_flasher as df
    ltmk = bytes.fromhex(open(da.LTMK_HEX).read().strip())
    t = da.Transport(da.MAC_DEFAULT)
    try:
        await df.login(t, ltmk)
        print("РЕЗУЛЬТАТ: login прошёл через эмулятор ✅"
              if DEVICE["obj"].logged_in else "РЕЗУЛЬТАТ: login НЕ прошёл ❌")
    finally:
        await t.close()


async def flash_via_tools(target, image_path, commit):
    import dreame_flasher as df
    ltmk = bytes.fromhex(open(da.LTMK_HEX).read().strip())
    t = da.Transport(da.MAC_DEFAULT)
    try:
        await df.login(t, ltmk)
        return await df.flash(t, image_path, target, commit=commit)
    finally:
        await t.close()


async def scenario_same_version():
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 2: DFU BLE ТОЙ ЖЕ версии -> ожидаем ОТКАЗ (status 6)")
    print("=" * 60)
    dev = DEVICE["obj"]
    dev.offered_ble_version = dev.ble_version           # та же версия
    img = make_fake_image(3000)                          # маленький образ (быстро)
    path = os.path.join(tempfile.gettempdir(), "emu_same.bin")
    open(path, "wb").write(img)
    before = dev.ble_version
    await flash_via_tools("ble", path, commit=True)
    print(f"РЕЗУЛЬТАТ: версия BLE {before} -> {dev.ble_version} "
          f"({'НЕ изменилась, отказ сработал ✅' if dev.ble_version == before else 'изменилась ❌'})")


async def scenario_296_boundary():
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 2.5: граница accept_limit (модель 296/301) на ТОЙ ЖЕ версии")
    print("=" * 60)
    # Реальная аномалия — устройство САМО держит счётчик на 296/301 (см. docs/FACTS.md),
    # не зависит от буфера/длины файла. Тот же механизм в accept_limit; чтобы прогон не
    # занимал минуты, проверяем на пропорционально малом образе (limit=10 из 15), а не на
    # реалистичных 296/301 — сам механизм (счётчик не растёт после limit) идентичен.
    dev = DEVICE["obj"]
    dev.offered_ble_version = dev.ble_version            # та же версия, как на живом устройстве
    dev.accept_limit = 10
    dev.ble_buf = bytearray()
    dev.ble_last = 0
    img = make_fake_image(15 * 512)
    path = os.path.join(tempfile.gettempdir(), "emu_296.bin")
    open(path, "wb").write(img)
    # commit=False намеренно: switchFirmware (даже отклонённый) сбрасывает буфер
    # (docs/FACTS.md «switchFirmware СБРАСЫВАЕТ OTA-буфер даже при отказе») — это
    # отдельный, уже проверенный факт (сценарий 2), здесь же смотрим именно на сам
    # счётчик приёма фрагментов, поэтому коммит не отправляем.
    await flash_via_tools("ble", path, commit=False)
    capped_ok = dev.ble_last == 10
    print(f"РЕЗУЛЬТАТ: устройство остановилось на lastFragmentIndex={dev.ble_last}/15 "
          f"(accept_limit=10) {'✅' if capped_ok else '❌'} "
          f"— на живом самокате тот же эффект даёт 296/301 (docs/FACTS.md).")
    dev.accept_limit = None                               # вернуть дефолт для дальнейших сценариев
    dev.ble_buf = bytearray()                             # т.к. commit=False не сбросил буфер
    dev.ble_last = 0                                      # сам (в отличие от switchFirmware) —
                                                            # иначе следующий сценарий увидит
                                                            # чужой resume-CRC и рассинхронизируется


async def scenario_upgrade():
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 3: DFU BLE НОВОЙ версии -> ожидаем УСПЕХ (switchFirmware)")
    print("=" * 60)
    dev = DEVICE["obj"]
    dev.offered_ble_version = "2.8.0_0001"              # новее установленной
    img = make_fake_image(3000)
    path = os.path.join(tempfile.gettempdir(), "emu_new.bin")
    open(path, "wb").write(img)
    before = dev.ble_version
    await flash_via_tools("ble", path, commit=True)
    ok = dev.ble_version == "2.8.0_0001"
    print(f"РЕЗУЛЬТАТ: версия BLE {before} -> {dev.ble_version} "
          f"({'ПРОШИВКА ПРИМЕНЕНА ✅ (недостижимо на железе)' if ok else 'не применилась ❌'})")


async def scenario_info():
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 4: инфо-канал 0x001c")
    print("=" * 60)
    dev = DEVICE["obj"]
    t = da.Transport(da.MAC_DEFAULT)
    try:
        await t.connect()
        for op, name in ((1, "mcu_version"), (3, "hardware")):
            t.rx = asyncio.Queue()
            outs = dev.on_write(0x001C, bytes([op]))
            for s, b in outs:
                val = b[2:2 + b[1]]
                print(f"  opcode {op} ({name}): {val.decode('ascii','replace')}")
    finally:
        await t.close()


async def scenario_telemetry():
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 5: телеметрия spec-канала (0x001a/0x001b), настоящий probes/spec_read.py")
    print("=" * 60)
    import dreame_flasher as df
    import spec_read as sr
    ltmk = bytes.fromhex(open(da.LTMK_HEX).read().strip())
    t = da.Transport(da.MAC_DEFAULT)
    try:
        await df.login(t, ltmk)
        sk = da.LAST_SK
        # читаем ПО ОДНОМУ свойству — устройство (и наш эмулятор) обслуживает
        # только первый объект запроса, batch не работает (см. docs/FACTS.md).
        single = [(1, 2), (1, 4), (1, 7), (2, 6), (3, 2), (4, 5)]
        all_ok = True
        for i, obj in enumerate(single):
            pt = await sr.spec_request(t, sk, [obj], app_cnt=i)
            lines = sr.parse_reply(pt) if pt else ["[!] ответа нет"]
            got = pt is not None and "пусто" not in "".join(lines)
            all_ok &= got
            print("  " + lines[-1] if len(lines) > 1 else "  " + lines[0])
        print(f"РЕЗУЛЬТАТ: телеметрия эмулятора прочитана настоящим spec_read.py "
              f"(по одному свойству) {'✅' if all_ok else '❌'}")

        # multi-object В ОДНОМ запросе: устройство должно обслужить ТОЛЬКО первый
        pt2 = await sr.spec_request(t, sk, [(1, 2), (1, 4)], app_cnt=len(single))
        lines2 = sr.parse_reply(pt2) if pt2 else []
        first_ok = any("BATTERY_LEVEL" in ln and "пусто" not in ln for ln in lines2)
        second_no_data = any("VOLTAGE" in ln and "status=61533" in ln for ln in lines2)
        print(f"РЕЗУЛЬТАТ: multi-object эмулируется как на железе "
              f"(первый объект есть, второй -> status) "
              f"{'✅' if first_ok and second_no_data else '❌'}")
    finally:
        await t.close()


async def scenario_push():
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 6: спонтанный пуш при изменении свойства (0x001b), без запроса")
    print("=" * 60)
    import dreame_flasher as df
    import spec_read as sr
    dev = DEVICE["obj"]
    ltmk = bytes.fromhex(open(da.LTMK_HEX).read().strip())
    t = da.Transport(da.MAC_DEFAULT)
    try:
        await df.login(t, ltmk)
        sk = da.LAST_SK

        # свойство ВНЕ списка подписки — пуш не должен уйти вообще
        out = dev.push_property(4, 5, "unused")   # (4,5) не в SUBSCRIBABLE
        print(f"  push вне SUBSCRIBABLE -> {'ничего не отправлено ✅' if not out else 'ОШИБКА, ушёл пуш ❌'}")

        # IS_RIDING: 0 -> 2 (в списке подписки) — устройство должно САМО прислать CTR
        while not t.rx.empty():
            t.rx.get_nowait()
        t.client.notify_now(dev.push_property(2, 7, 2))

        s, b = await asyncio.wait_for(t.rx.get(), timeout=2.0)
        is_ctr = s == 0x001B and len(b) >= 6 and b[0] == 0 and b[1] == 0 and b[2] == 0x00
        print(f"  CTR от устройства без запроса: {'получен ✅' if is_ctr else 'НЕ получен ❌'}")
        if not is_ctr:
            print("РЕЗУЛЬТАТ: пуш не работает ❌")
            return
        fc = struct.unpack("<H", b[4:6])[0]
        await t.write(0x001B, struct.pack("<HBB", 0, 0x01, 0x01))   # готовы принимать
        parts = {}
        for _ in range(fc):
            s2, b2 = await asyncio.wait_for(t.rx.get(), timeout=2.0)
            seq = struct.unpack("<H", b2[:2])[0]
            parts[seq] = b2[2:]
        await t.write(0x001B, struct.pack("<HBB", 0, 0x01, 0x00))   # приняли всё
        payload = b"".join(parts[i] for i in sorted(parts))
        cnt = struct.unpack("<H", payload[:2])[0]
        pt = sr.dec_dev(sk, cnt, payload[2:])
        lines = sr.parse_reply(pt)
        for line in lines:
            print("  " + line)
        ok = any("IS_RIDING" in ln and "пусто" not in ln for ln in lines)
        print(f"РЕЗУЛЬТАТ: пуш IS_RIDING расшифрован настоящим spec_read.dec_dev "
              f"{'✅' if ok else '❌'}")
    finally:
        await t.close()


async def main():
    install_fake()
    # устройство на СТАРОЙ версии, чтобы можно было показать апгрейд
    ltmk = bytes.fromhex(open(da.LTMK_HEX).read().strip())
    DEVICE["obj"] = ScooterDevice(ltmk, ble_version="2.7.0_0015",
                                  mcu_version="0007", verbose=True)
    await scenario_login()
    DEVICE["obj"].logged_in = False
    await scenario_same_version()
    await scenario_296_boundary()
    await scenario_upgrade()
    await scenario_info()
    DEVICE["obj"].logged_in = False
    await scenario_telemetry()
    DEVICE["obj"].logged_in = False
    await scenario_push()
    print("\n" + "=" * 60)
    print("ГОТОВО. Эмулятор прогнал настоящие dreame_auth/dreame_flasher без BLE.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
