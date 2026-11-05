# Scooter 5 Pro Device Emulator / Эмулятор устройства Scooter 5 Pro

> 📄 **Language / Язык:** [🇬🇧 English](#-english) · [🇷🇺 Русский](#-русский)

---

## 🇬🇧 English

Software model of the **device** side implementing the reverse-engineered protocol
(see [`../docs/BLE.md`](../docs/BLE.md) and [`../docs/DFU.md`](../docs/DFU.md)). It allows running the **real**
[`dreame_auth.py`](../core/dreame_auth.py) and [`dreame_flasher.py`](../core/dreame_flasher.py) without BLE hardware or a physical scooter — simply by
replacing `dreame_auth.BleakClient` with `FakeBleakClient`.

### Why it exists
The primary goal is to verify the **complete, successful firmware flashing cycle with version increment**,
which is impossible on a live scooter (the scooter always runs the same version, and `switchFirmware`
is rejected with status 6). The emulator demonstrates the entire path: login → upload fragments →
CRC32 verify → `switchFirmware` with `status 0` → version successfully upgraded.

### Files
| File | Description |
|---|---|
| [`scooter_device.py`](scooter_device.py) | Device engine: login crypto, channel transport, BLE/MCU DFU, info channel |
| [`fake_ble.py`](fake_ble.py) | `FakeBleakClient` — Bleak API adapter delivering notifications synchronously |
| [`run_emulator.py`](run_emulator.py) | Test harness: 7 scenarios executing real tools against the model |

### Running the emulator
```bash
python emulator/run_emulator.py
```

### What is modeled accurately
- **Login:** Genuine ECDH P-256 + HKDF-SHA256 + AES-CCM. The device generates its own
  EC keypair, derives the exact same sessionKey, and verifies the CRC32 confirmation. Not a stub.
- **Channel transport:** CTR/DATA/ACK, MNG handshake, SINGLE frames, pull `ACK 05`.
- **DFU:** fragmentSize=512, 18-byte frames, lastFragmentIndex, and **real CRC32 calculation** over
  received bytes (ensuring flasher resume/verify work exactly as on physical hardware).
- **switchFirmware:** Version gating (newer version → applied, identical/older version → status 6 on BLE /
  status 5 on MCU) and **buffer reset on rejection** (matching observed hardware behavior).
- **Spec channel telemetry** (`0x001a`/`0x001b`): Multi-frame request reassembly,
  AES-CCM encryption/decryption using the authentic key derivation (`sk[16:32]`/`sk[0:16]` +
  frame counters), returning real property values (battery level, voltage, mileage, temperature,
  firmware version). Handles **only the first requested object** — identical to physical hardware.
  Verified against real `probes/spec_read.py` (Scenario 5).

### What the emulator does NOT do (model boundaries)
- ⚠️ **Does not enforce the 296 / 0x25000 boundary by default** — the emulator accepts the complete
  image for end-to-end flashing verification. Physical hardware on identical versions
  only commits 296 fragments (see `docs/DFU.md`). This behavior can be enabled via the
  `accept_limit` parameter on `ScooterDevice`.
- **Does not verify RSA/Mijia signatures** and does not decrypt the AES firmware payload — image version
  is provided by the test harness (`offered_ble_version`), because in reality it resides in the encrypted body.
- **Telemetry:** Property values are **static** (not tied to a dynamic battery/ride physics simulation,
  and state-change push events are not simulated) — only reading of fixed properties is supported.
- This is a **behavioral testing model for our tools**, not a low-level microcode emulator of the chips.

---

## 🇷🇺 Русский

Программная модель стороны **устройства**, реализующая реверснутый протокол
(см. [`../docs/BLE.md`](../docs/BLE.md) и [`../docs/DFU.md`](../docs/DFU.md)). Позволяет гонять **настоящие**
[`dreame_auth.py`](../core/dreame_auth.py) и [`dreame_flasher.py`](../core/dreame_flasher.py) без BLE и без железа — только подменой
`dreame_auth.BleakClient` на `FakeBleakClient`.

### Зачем
Главное — проверить **полный успешный цикл прошивки с повышением версии**, который
на живом самокате недостижим: там всегда стоит та же версия, и `switchFirmware`
отвергается (status 6). Эмулятор показывает путь login → заливка → CRC → switchFirmware
`status 0` → версия поднялась.

### Файлы
| Файл | Что |
|---|---|
| [`scooter_device.py`](scooter_device.py) | Движок устройства: login-крипто, канальный транспорт, DFU BLE/MCU, info-канал |
| [`fake_ble.py`](fake_ble.py) | `FakeBleakClient` — адаптер под API bleak (доставляет notify синхронно) |
| [`run_emulator.py`](run_emulator.py) | Харнесс: 7 сценариев против настоящих инструментов |

### Запуск
```bash
python emulator/run_emulator.py
```

### Что моделируется точно
- **Login:** реальный ECDH P-256 + HKDF-SHA256 + AES-CCM. Устройство генерирует свою
  EC-пару, выводит тот же sessionKey, проверяет CRC32-подтверждение. Не заглушка.
- **Канальный транспорт:** CTR/DATA/ACK, MNG-хендшейк, SINGLE, pull `ACK 05`.
- **DFU:** fragmentSize=512, кадры 18 Б, lastFragmentIndex, **реальный CRC32** по
  принятым байтам (поэтому resume/verify флешера работают как на железе).
- **switchFirmware:** версионный гейт (новее → применяется, та же/старая → status 6 BLE /
  5 MCU) и **сброс буфера при отказе** (как подтверждено на устройстве).
- **Телеметрия spec-канала** (`0x001a`/`0x001b`): реассемблинг многокадрового запроса,
  AES-CCM-дешифровка/шифровка по реальной формуле (`sk[16:32]`/`sk[0:16]` +
  счётчики), ответ с публичным набором значений (батарея/напряжение/пробег/темп/
  версия). Обслуживает **только первый объект** запроса — как на живом устройстве.
  Проверено настоящим `probes/spec_read.py` (сценарий 5).

### Чего эмулятор НЕ делает (границы модели)
- ⚠️ **Не воспроизводит границу 296/0x25000** по умолчанию — эмулятор принимает весь
  образ (для демо успешной прошивки). Настоящее устройство на той же версии
  засчитывает только 296 фрагментов (см. `docs/DFU.md`). Поведение включается параметром
  `accept_limit` у `ScooterDevice`.
- **Не проверяет RSA/Mijia-подпись** и не расшифровывает AES-тело — версия образа задаётся
  харнессом (`offered_ble_version`), т.к. реально она находится в зашифрованном теле.
- **Телеметрия:** значения **статичны** (не связаны с физической моделью батареи/поездки,
  пуш при изменении не эмулируется) — только чтение фиксированного набора свойств.
- Это **модель поведения для тестов нашего кода**, а не эмуляция микрокода самой прошивки.
