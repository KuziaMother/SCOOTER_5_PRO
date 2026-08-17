#!/usr/bin/env python3
"""
FakeBleakClient — адаптер эмулятора под интерфейс bleak.BleakClient.

Позволяет запускать НАСТОЯЩИЕ dreame_auth.py / dreame_flasher.py против
ScooterDevice без железа: подменяется dreame_auth.BleakClient на этот класс.

Уведомления доставляются синхронно во время write_gatt_char (устройство
обрабатывает кадр и сразу вызывает notify-callback), что совпадает с моделью
ожидания в Transport (пишем -> ждём rx).
"""
import asyncio

FE95 = "0000fe95-0000-1000-8000-00805f9b34fb"
CHARS = [0x0004, 0x0005, 0x0010, 0x0016, 0x0017, 0x0018, 0x001a, 0x001b, 0x001c]


class FakeChar:
    def __init__(self, sid):
        self.sid = sid
        self.uuid = f"0000{sid:04x}-0000-1000-8000-00805f9b34fb"
        # набор свойств: notify для входящих каналов, write для команд
        props = {"write", "write-without-response"}
        if sid in (0x0010, 0x0016, 0x0017, 0x0018, 0x001a, 0x001b, 0x001c):
            props |= {"notify"}
        if sid in (0x0004, 0x0005):
            props = {"read"}
        self.properties = sorted(props)


class FakeService:
    def __init__(self):
        self.uuid = FE95
        self.characteristics = [FakeChar(s) for s in CHARS]


class FakeBleakClient:
    """Минимальная реализация API bleak поверх ScooterDevice."""
    _device_factory = None      # ставится извне: () -> ScooterDevice

    def __init__(self, mac, timeout=20.0, **kw):
        self.mac = mac
        self.mtu_size = 247
        self._service = FakeService()
        self._char_by_sid = {c.sid: c for c in self._service.characteristics}
        self._notify = {}       # sid -> callback
        self.device = (FakeBleakClient._device_factory or (lambda: None))()
        self._connected = False

    # -- lifecycle --
    @property
    def is_connected(self):
        return self._connected

    async def connect(self):
        self._connected = True
        return True

    async def disconnect(self):
        self._connected = False
        return True

    @property
    def services(self):
        return [self._service]

    # -- notifications --
    async def start_notify(self, char, callback):
        sid = char.sid if isinstance(char, FakeChar) else int(str(char)[:6], 16)
        self._notify[sid] = callback

    async def stop_notify(self, char):
        sid = char.sid if isinstance(char, FakeChar) else None
        self._notify.pop(sid, None)

    # -- io --
    async def write_gatt_char(self, char, data, response=False):
        sid = char.sid
        outs = self.device.on_write(sid, bytes(data))
        # доставляем уведомления через зарегистрированные callback'и
        for out_sid, out_bytes in outs:
            cb = self._notify.get(out_sid)
            if cb is not None:
                sender = self._char_by_sid[out_sid]
                cb(sender, bytearray(out_bytes))
        await asyncio.sleep(0)      # уступить циклу

    async def read_gatt_char(self, char):
        sid = char.sid
        return self.device.on_read(sid)

    def notify_now(self, outs):
        """Доставить уведомления БЕЗ предшествующего write_gatt_char — эмуляция
        спонтанного пуша устройства (device.push_property(...) -> outs той же
        формы [(sid, bytes), ...], что возвращает on_write)."""
        for out_sid, out_bytes in outs:
            cb = self._notify.get(out_sid)
            if cb is not None:
                sender = self._char_by_sid[out_sid]
                cb(sender, bytearray(out_bytes))
