# Xiaomi Scooter 5 Pro — Protocol Reverse Engineering & Tools

Исследовательский проект по электросамокату `xiaomi.scooter.5pro`
(MAC `2C:19:5C:DE:DE:88`).

Research project for the `xiaomi.scooter.5pro` electric scooter
(MAC `2C:19:5C:DE:DE:88`).

> 📄 **Язык / Language:** [🇷🇺 Русский](#-русский) · [🇬🇧 English](#-english)

---

## 🇷🇺 Русский

Исследовательский проект по электросамокату `xiaomi.scooter.5pro`
(MAC `2C:19:5C:DE:DE:88`): реверс BLE-протокола, чтение телеметрии по
Mi Home spec, прошивка обоих чипов (RTL8762C — по воздуху, GD32 MCU —
по воздуху и по проводу), локальный веб-интерфейс и мобильный клиент.

В самокате два «мозга»:

- **BLE-чип (Realtek RTL8762C)** — GATT-сервис `FE95`, Mijia security-chip
  login, слой спецификации Mi Home (siid/piid);
- **MCU (GD32, Cortex-M4F)** — BLDC-контроллер мотора/батареи; говорит с
  BLE-чипом по UART @19200.

> **Методология реверса:** статический реверс образов прошивок (`research/`)
> проводится силами агента **Qwen 3.8 27B** — Claude (Anthropic) отказался
> выполнять эту работу, сославшись на небезопасность.

### Структура проекта

Иерархия: **код и исследования** — верхний уровень; **данные** (gitignored) —
отдельные каталоги в корне; **все логи — в `logs/`**.

| Каталог | Назначение |
|---|---|
| `core/` | **Ядро протокола**: BLE-транспорт, security-chip login (`dreame_auth.py`), BLE-DFU флешер (`dreame_flasher.py`) — основа всего остального |
| `webui/` | Локальный веб-интерфейс (Flask, 127.0.0.1): дашборд, управление, прошивка |
| `mobile/` | Мобильный клиент: Web Bluetooth PWA → TWA/APK (`mobile/README.md`) |
| `probes/` | Исследовательские пробы (BLE, read-only): spec read/push, телеметрия, MCU-гейты |
| `tools/` | CLI-утилиты: UART (logger, baud-скан, MCU-флешер), скачивание прошивок из Mi Cloud |
| `emulator/` | Софтверная модель стороны самоката — прогон настоящих инструментов без железа |
| `tests/` | Тест-сьют (pytest) |
| `docs/` | Документация: `BLE.md`, `MCU.md`, `DFU.md` |
| `research/` | Статический реверс образов прошивок: `REPORT.md`; `scripts/` — анализ (BLE/MCU), `images/` — образы и сертификаты, `functions_*/` — сгенерированные разборы функций; `custom_mcu/` — патченный MCU-образ |

Данные (в `.gitignore`, не коммитятся):

| Каталог | Назначение |
|---|---|
| `firmware_ota/` | Официальные образы прошивок |
| `secrets/` | Ключи и сессии (LTMK, Mi Cloud) |
| `logs/` | **Все логи проекта** |
| `plugins/` | Разобранные плагины/APK Mi Home |
| `tmp/`, `zip_archives/`, `uart_raw/` | Рабочие артефакты (архивы, сырые UART-захваты) |

### Документация

| Файл | Содержание |
|---|---|
| `docs/BLE.md` | BLE-сторона: GATT, login, телеметрия |
| `docs/MCU.md` | MCU: образ прошивки, UART-протокол |
| `docs/DFU.md` | Обновление прошивок (по воздуху и по проводу) |
| `research/REPORT.md` | Статический реверс образов прошивок (самый подробный разбор) |
| `mobile/README.md` | Мобильный клиент (Web Bluetooth → TWA/APK) |

### Установка

Python 3.11+ (проверено на Windows).

```bash
pip install -r requirements-dev.txt   # зависимости (вкл. pyserial) + pytest/ruff
```

#### Секреты (`secrets/`, в .gitignore)

| Файл | Назначение |
|---|---|
| `ltmk.hex` / `ltmk_<MAC>.hex` | LTMK — ключ логина конкретного самоката |
| `scooters.json` | Профили самокатов (name + MAC) для веб-интерфейса |
| `micloud_session.json` | Сессия Mi Cloud (QR-логин; общая с `tools/xct/`) |

Для нового самоката LTMK получается через Mi Cloud — страница «Мои
самокаты» в веб-интерфейсе (`webui/micloud_ltmk.py`).

### Быстрый старт

#### Веб-интерфейс (дашборд, управление, прошивка)

```bash
python webui/app.py        # http://127.0.0.1:8321  (только localhost)
```

Несколько самокатов, чтение свойств, SET по клику, режим езды, загрузка
прошивок на сервисной странице. Журнал заливок — `logs/flash_log.jsonl`.

#### Телеметрия (BLE, read-only)

```bash
python probes/spec_read.py               # быстрое чтение свойств
python tools/dump_telemetry.py           # полный дамп в таблицу (docs/telemetry.txt)
python probes/spec_listen.py --secs 120  # слушать ПУШИ: меняй состояние (газ/свет/движение)
```

#### Прошивка

```bash
# BLE-чип по воздуху (канал FE95/0x0018):
python core/dreame_flasher.py ble firmware_ota/…_upd_xiaomi.scooter.5pro_v2.7.0_0015.bin

# MCU по воздуху:
python core/dreame_flasher.py mcu firmware_ota/c0f78c49…_mcu_xiaomi.scooter.5pro_v0007.bin

# MCU по проводу (USB-TTL, 19200, протокол bw-flasher):
python tools/mcu_uart_flash.py --port COM3 \
    --fw firmware_ota/c0f78c49…_mcu_xiaomi.scooter.5pro_v0007.bin \
    --md5 c0f78c49f322bd3d71fea19c90241882
```

⚠️ `switchFirmware` необратим (риск кирпича) — флешер шлёт его только с
флагом `--commit`; без флага заливает фрагменты, но не переключает.

#### Эмулятор и тесты (без железа)

```bash
python emulator/run_emulator.py   # настоящие core/dreame_auth + dreame_flasher против софтверной модели
pytest                            # тест-сьют (вкл. полный цикл прошивки на эмуляторе)
ruff check .                      # линтер (E9+F — codebase это research-скрипты, не библиотека)
```

### Логи

Все `.log`-файлы лежат в `logs/`:

- `tools/uart_logger.py` — по умолчанию пишет в `logs/uart_activity.log`
  (сырые захваты байтов — в `uart_raw/`); анализ: `python tools/uart_logger.py --show logs/uart_activity.log`;
- `probes/spec_listen.py` — `logs/push_capture_*.txt`;
- веб-интерфейс — журнал заливок `logs/flash_log.jsonl`.

### Тесты

```bash
pytest
```

Скрипты намеренно используют `sys.path.insert` до импортов (research-код,
не пакет) — ruff настроен только на реальные ошибки (`E9`, `F`).

---

## 🇬🇧 English

Research project for the `xiaomi.scooter.5pro` electric scooter
(MAC `2C:19:5C:DE:DE:88`): BLE protocol reverse engineering, telemetry reading
via the Mi Home spec, flashing both chips (RTL8762C — over the air, GD32 MCU —
over the air and over wire), a local web interface, and a mobile client.

The scooter has two "brains":

- **BLE chip (Realtek RTL8762C)** — GATT service `FE95`, Mijia security-chip
  login, Mi Home spec layer (siid/piid);
- **MCU (GD32, Cortex-M4F)** — BLDC motor/battery controller; talks to the
  BLE chip over UART @19200.

> **Reverse methodology:** the static reverse of the firmware images
> (`research/`) is carried out by the agent **Qwen 3.8 27B** — Claude
> (Anthropic) declined to perform this work, citing safety concerns.

### Project structure

Hierarchy: **code and research** — top level; **data** (gitignored) — separate
directories at the root; **all logs — in `logs/`**.

| Directory | Purpose |
|---|---|
| `core/` | **Protocol core**: BLE transport, security-chip login (`dreame_auth.py`), BLE-DFU flasher (`dreame_flasher.py`) — the foundation of everything else |
| `webui/` | Local web interface (Flask, 127.0.0.1): dashboard, control, flashing |
| `mobile/` | Mobile client: Web Bluetooth PWA → TWA/APK (`mobile/README.md`) |
| `probes/` | Research probes (BLE, read-only): spec read/push, telemetry, MCU gates |
| `tools/` | CLI utilities: UART (logger, baud scan, MCU flasher), firmware download from Mi Cloud |
| `emulator/` | Software model of the scooter side — run the real tools without hardware |
| `tests/` | Test suite (pytest) |
| `docs/` | Documentation: `BLE.md`, `MCU.md`, `DFU.md` |
| `research/` | Static reverse of firmware images: `REPORT.md`; `scripts/` — analysis (BLE/MCU), `images/` — images and certificates, `functions_*/` — generated function breakdowns; `custom_mcu/` — patched MCU image |

Data (in `.gitignore`, not committed):

| Directory | Purpose |
|---|---|
| `firmware_ota/` | Official firmware images |
| `secrets/` | Keys and sessions (LTMK, Mi Cloud) |
| `logs/` | **All project logs** |
| `plugins/` | Disassembled Mi Home plugins/APKs |
| `tmp/`, `zip_archives/`, `uart_raw/` | Working artifacts (archives, raw UART captures) |

### Documentation

| File | Contents |
|---|---|
| `docs/BLE.md` | BLE side: GATT, login, telemetry |
| `docs/MCU.md` | MCU: firmware image, UART protocol |
| `docs/DFU.md` | Firmware updates (over the air and over wire) |
| `research/REPORT.md` | Static reverse of firmware images (the most detailed breakdown) |
| `mobile/README.md` | Mobile client (Web Bluetooth → TWA/APK) |

### Installation

Python 3.11+ (verified on Windows).

```bash
pip install -r requirements-dev.txt   # dependencies (incl. pyserial) + pytest/ruff
```

#### Secrets (`secrets/`, in .gitignore)

| File | Purpose |
|---|---|
| `ltmk.hex` / `ltmk_<MAC>.hex` | LTMK — the login key of a specific scooter |
| `scooters.json` | Scooter profiles (name + MAC) for the web interface |
| `micloud_session.json` | Mi Cloud session (QR login; shared with `tools/xct/`) |

For a new scooter, LTMK is obtained via Mi Cloud — the "My scooters" page in
the web interface (`webui/micloud_ltmk.py`).

### Quick start

#### Web interface (dashboard, control, flashing)

```bash
python webui/app.py        # http://127.0.0.1:8321  (localhost only)
```

Multiple scooters, property reads, click-to-SET, ride mode, firmware upload on
the service page. Flash log — `logs/flash_log.jsonl`.

#### Telemetry (BLE, read-only)

```bash
python probes/spec_read.py               # quick property read
python tools/dump_telemetry.py           # full dump to a table (docs/telemetry.txt)
python probes/spec_listen.py --secs 120  # listen to PUSHES: change state (throttle/lights/motion)
```

#### Flashing

```bash
# BLE chip over the air (channel FE95/0x0018):
python core/dreame_flasher.py ble firmware_ota/…_upd_xiaomi.scooter.5pro_v2.7.0_0015.bin

# MCU over the air:
python core/dreame_flasher.py mcu firmware_ota/c0f78c49…_mcu_xiaomi.scooter.5pro_v0007.bin

# MCU over wire (USB-TTL, 19200, bw-flasher protocol):
python tools/mcu_uart_flash.py --port COM3 \
    --fw firmware_ota/c0f78c49…_mcu_xiaomi.scooter.5pro_v0007.bin \
    --md5 c0f78c49f322bd3d71fea19c90241882
```

⚠️ `switchFirmware` is irreversible (bricking risk) — the flasher sends it only
with the `--commit` flag; without the flag it uploads fragments but does not
switch.

#### Emulator and tests (no hardware)

```bash
python emulator/run_emulator.py   # real core/dreame_auth + dreame_flasher against the software model
pytest                            # test suite (incl. full flashing cycle on the emulator)
ruff check .                      # linter (E9+F — the codebase is research scripts, not a library)
```

### Logs

All `.log` files live in `logs/`:

- `tools/uart_logger.py` — writes to `logs/uart_activity.log` by default
  (raw byte captures go to `uart_raw/`); analysis: `python tools/uart_logger.py --show logs/uart_activity.log`;
- `probes/spec_listen.py` — `logs/push_capture_*.txt`;
- web interface — flash log `logs/flash_log.jsonl`.

### Tests

```bash
pytest
```

The scripts intentionally use `sys.path.insert` before imports (research code,
not a package) — ruff is configured for real errors only (`E9`, `F`).
