# Dreame / Xiaomi Scooter 5 Pro — BLE tooling & firmware research

Реверс BLE-протокола, DFU-флешер и статический анализ прошивок самоката
`xiaomi.scooter.5pro` (MAC `2C:19:5C:DE:DE:88`).

> **Начинать здесь:** проверенные константы протокола — [`docs/FACTS.md`](docs/FACTS.md)
> (не выводить их заново из дизасма); рабочие правила — [`CLAUDE.md`](CLAUDE.md);
> статус и план — [`todo.md`](todo.md).

---

## Оглавление

- [Структура проекта](#структура-проекта)
- [Быстрый старт](#быстрый-старт)
- [Ключевые факты](#ключевые-факты)
- [⚠️ Безопасность](#-безопасность)

---

## Структура проекта

```
dreame_auth.py          Ядро: BLE-транспорт (A4/MNG), security-chip login, DFU-команды, сбор инфо
dreame_flasher.py       Флешер прошивки (BLE/MCU) поверх dreame_auth
docs/FACTS.md           ★ Проверенные константы протокола — единственный источник истины
CLAUDE.md               Рабочие правила проекта (иерархия доказательств, секреты, безопасность)
todo.md                 Что сделано / стены / дальнейшие шаги
docs/dreame_dfu_protocol.md  Исторический разбор протокола §6.1–6.17 (устаревшие места помечены)

firmware_ota/           Официальные образы из Mi Cloud (BLE + MCU) + latest_ver JSON
probes/                 On-device пробы (read-only): перебор опкодов, скан рекламы, прослушка сессии
tools/                  Mi Cloud + бандлы: fetch_plugin.py, fetch_firmware.py, unpack_rambundle.py, xct/
plugins/                Скачанный плагин Mi Home + распакованные JS-модули (карта телеметрии)
research_bin/           Статический реверс прошивок: REPORT.md, decryptor.py, analyze*.py, mcu_*.py,
                        functions_ble/, functions_mcu/, .bin (образы для анализа)
zip_archives/           Вендорские SDK/тулы (rtltool, rtl8762c-gcc-examples, MP Tool) — вне git
docs/                   Справка: telemetry.txt (дамп), SUMMARY.md (архив), spec/info JSON, todo.md, protocol.md
secrets/                🔒 Ключи устройства (НЕ публиковать) — см. .gitignore
emulator/               Эмулятор устройства (тест dreame_auth/dreame_flasher без BLE)
apk/                    Mi Home APK (источник DEX-анализа, 229 МБ)
logs/                   btsnoop_hci.log (снуп сессии Mi Home — ВАЖЕН) + логи прогонов флешера
```

## Быстрый старт

Зависимости: `bleak`, `cryptography` (Python 3.11+, Windows/WinRT BLE).

```bash
# Логин + сбор информации с самоката (read-only)
python dreame_auth.py

# Прошивка (БЕЗ коммита — только загрузка фрагментов, безопасно):
python dreame_flasher.py ble firmware_ota/<image>.bin
python dreame_flasher.py mcu firmware_ota/<image>.bin

# Полная прошивка с необратимым переключением (только на версии НОВЕЕ установленной!):
python dreame_flasher.py ble firmware_ota/<image>.bin --commit --yes

# Проверить, применилась ли установка MCU (read-only, ничего не шьёт):
python dreame_flasher.py poll-mcu --poll-timeout=60
```

Для MCU установка асинхронная: после `switchFirmware` флешер опрашивает версию кадром
`[01]` на `0x001c` до её смены — так же делает штатный `MeshDfuManager` в Mi Home.

On-device пробы (read-only, самокат должен быть включён):

```bash
python probes/beacon_scan.py --secs 30              # что самокат вещает в рекламе (без подключения)
python probes/mcu_opcode_sweep.py --max 255         # перебор опкодов инфо-канала 0x001c
python probes/telemetry_listen.py --secs 40         # логин + пассивная прослушка нотификаций

# ТЕЛЕМЕТРИЯ: полный дамп в docs/telemetry.txt
python tools/dump_telemetry.py                      # батарея + поездка
python tools/dump_telemetry.py --all                # + настройки, SN, версии

# одно свойство
python probes/spec_read.py --siid 1 --piid 2        # BATTERY_LEVEL, %
python probes/spec_read.py --siid 2 --piid 6        # TOTAL_MILEAGE
```

Читать надо **по одному свойству**: устройство обслуживает только первый объект
в запросе, остальным возвращает статус −4003.

Карта свойств (siid/piid) — в [`research_bin/REPORT.md`](research_bin/REPORT.md); она
извлечена из плагина Mi Home и в публичной MIoT-спеке отсутствует.

Логин требует `secrets/ltmk.hex` и `secrets/scooter_keys.json`
(извлекаются QR-логином в Mi Cloud — см. `tools/fetch_firmware.py` / `tools/xct/`).
Сессия Mi Cloud кэшируется в `secrets/micloud_session.json`, повторный QR не нужен.

## Ключевые факты

- **Login:** ECDH P-256 + HKDF + AES-CCM; пин `12****`.
- **DFU data-канал (0x0018):** окно=1, кадры 18 Б, pull по ACK `05`, `switchFirmware` — необратим.
  «Защита от дурака» срабатывает на разных этапах: BLE принимает все фрагменты и отвергает
  переключение (`status 6`), MCU отсекает на первом фрагменте (`status 5`) и закрывает сессию.
- **BLE (RTL8762C):** открытый bootloader/OTA + **AES-зашифрованный APP** (ключ в OTP, XIP-decrypt)
  + RSA/Mijia-подпись → из `.bin` не расшифровать.
- **MCU (GD32/STM32F1 Cortex-M4F):** открытый код BLDC-контроллера (TIM1+Холл, ADC, USART3↔BLE, OTA).
- **Телеметрии нет ни в одном стандартном пути:** канал `0x001c` = 4 опкода (версии/железо/серийник,
  и это канал BLE-чипа, а не проброс к MCU); в публичной MIoT-спеке свойств нет; MiBeacon-реклама
  несёт только идентификацию.
- **✅ Телеметрия читается** (`probes/spec_read.py`): приватная спека найдена в плагине Mi Home,
  протокол — **MIoT-spec поверх BLE**: `0x001a` write / `0x001b` notify, **канал 0**, кадры 18 Б,
  `op=2` для чтения, полезная нагрузка в AES-CCM с префиксом счётчика.
  Проверено на живом самокате: батарея 100 %, 53.44 В, пробег 4.4 км, остаток хода 60.5 км,
  темп. батареи 25 °C, SOH 100 %. Пробег/остаток — в 0.01 км, ток в А, мощность в Вт, напряжение в 0.01 В.

Подробности — [`docs/dreame_dfu_protocol.md`](docs/dreame_dfu_protocol.md) и [`research_bin/REPORT.md`](research_bin/REPORT.md).

## ⚠️ Безопасность

- `secrets/` содержит ltmk/token устройства — **не коммитить, не публиковать**.
- `switchFirmware` необратим (риск кирпича). На той же версии бесполезен и отвергается устройством.
- Прошивать только официальные подписанные образы (`firmware_ota/`, MD5 сверены).
