# Xiaomi Scooter 5 Pro — Protocol Reverse Engineering, Flasher & Tools

Research, reverse engineering, and tooling suite for the `xiaomi.scooter.5pro` electric scooter (target MAC `2C:19:5C:DE:DE:88`).

> 📄 **Language / Язык:** [🇬🇧 English](#-english) · [🇷🇺 Русский](#-русский)

---

## 🇬🇧 English

Comprehensive reverse engineering project for the **Xiaomi Scooter 5 Pro** (`xiaomi.scooter.5pro`, model code `0x1928`). This repository provides complete protocol specifications, security authentication mechanisms, over-the-air (OTA) and wired UART firmware flashers, a local web dashboard, a mobile Web Bluetooth client, an offline device emulator, and static firmware analysis artifacts.

### Architecture Overview

The scooter utilizes a dual-processor architecture communicating over an internal serial bus:

```
┌─────────────────────────────────────────────────────────────┐
│                       Client Layer                          │
│  WebUI (Flask)  │  Mobile PWA (Web Bluetooth)  │  CLI Tools │
└──────────────────────────────┬──────────────────────────────┘
                               │ BLE (GATT FE95 / P-256 + AES-CCM)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               Realtek RTL8762C (BLE SoC)                   │
│   • GATT Service 0xFE95                                     │
│   • Mijia Security Chip Authentication (ECDH P-256)         │
│   • Mi Home Spec Framing (siid / piid read/write/notify)    │
│   • BLE-DFU OTA Target 0                                    │
└──────────────────────────────┬──────────────────────────────┘
                               │ UART @ 19200 baud (8N1)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│             GigaDevice GD32F4 (Cortex-M4F MCU)              │
│   • BLDC Motor Controller (Field-Oriented Control / FOC)    │
│   • Battery Management & Power Sequencing (BMS)             │
│   • Speed PID Regulation & Telemetry Aggregator             │
│   • MCU-DFU Target 1 (OTA staging & wired bootloader)       │
└─────────────────────────────────────────────────────────────┘
```

---

### Key Features

- **Protocol Core & Cryptography (`core/`)**:
  - Full Mijia Security Chip authentication: ECDH P-256 key exchange, HKDF-SHA256 session key derivation, and AES-CCM frame encryption with monotonic packet counters.
  - Channel-based fragmentation layer (`CTR`/`DATA`/`ACK`) supporting reliable large-payload transfer over BLE.
  - Dual-target DFU flasher (`core/dreame_flasher.py`) supporting both BLE SoC (target 0) and MCU (target 1) with fragment verification and resume support.
- **Local Web Dashboard (`webui/`)**:
  - Standalone Flask server running locally on `http://127.0.0.1:8321`.
  - Live telemetry monitor: speed, battery %, voltage, current, motor temperature, odometer, ride modes (Walk, Drive, Sport).
  - One-click parameter control: speed limit, cruise control, taillight, regenerative braking level.
  - Multi-scooter profile management and automated Xiaomi Cloud token retrieval (LTMK).
  - Firmware upload & flashing orchestration with safety guardrails.
  - Bilingual UI with dynamic language switcher (English / Russian).
- **Mobile Client (`mobile/`)**:
  - Lightweight Web Bluetooth Progressive Web App (PWA).
  - Runs directly inside Chrome on Android without cloud dependency, APK installation, or root privileges.
  - Complete client-side JavaScript implementation of ECDH P-256, HKDF-SHA256, and AES-CCM.
  - Includes full-screen dashboard "Ride Mode" optimized for phone handlebar mounts.
- **Offline Software Emulator (`emulator/`)**:
  - Software implementation of the scooter's BLE and spec protocol stack (`ScooterDevice`).
  - End-to-end smoke test suite (`emulator/run_emulator.py`) validating authentication, property reads, telemetry streaming, and full OTA flashing lifecycles without physical hardware.
- **Hardware & Protocol Probes (`probes/`)**:
  - Non-destructive CLI scripts to sweep spec properties, capture push notifications, analyze telemetry channels, and inspect MCU gate conditions.
- **Diagnostic & Flashing Tools (`tools/`)**:
  - Direct wired MCU firmware flasher (`tools/mcu_uart_flash.py`) communicating over USB-TTL UART.
  - Firmware unpackers, telemetry dumpers, baud rate scanners, and Xiaomi Cloud OTA fetchers.
- **Firmware Research & Disassembly (`research/`)**:
  - Detailed static reverse engineering report ([`research/REPORT.md`](research/REPORT.md)).
  - Complete memory maps, Ghidra/IDA disassemblies, annotated function catalogues, and verified custom firmware patches ([`research/custom_mcu/`](research/custom_mcu/)).

---

### Repository Structure

```
SCOOTER_5_PRO/
├── core/            # Protocol core: BLE transport, authentication, DFU flashing engine
├── webui/           # Local web interface (Flask): dashboard, telemetry, scooter management
├── mobile/          # Mobile client: Web Bluetooth PWA (Android / Chrome)
├── emulator/        # Software device model for offline simulation and automated tests
├── tools/           # Diagnostic and utility CLIs: UART flasher, loggers, cloud extractors
├── probes/          # Read-only exploration and inspection scripts
├── tests/           # Automated test suite (pytest unit & integration tests)
├── docs/            # Protocol specifications: BLE.md, MCU.md, DFU.md
├── research/        # Reverse engineering reports, disassemblies, custom firmware patches
└── logs/            # Project runtime logs, flash audits, and telemetry dumps (gitignored)
```

#### Directory Overview

| Directory | Purpose |
|---|---|
| [`core/`](core/) | **Protocol Foundation**: BLE transport, security-chip auth ([`dreame_auth.py`](core/dreame_auth.py)), BLE/MCU DFU flasher ([`dreame_flasher.py`](core/dreame_flasher.py)). |
| [`webui/`](webui/) | **Local Web Application**: Dashboard, interactive controls, telemetry polling, firmware service interface. |
| [`mobile/`](mobile/) | **Mobile PWA**: Client-side Web Bluetooth app; runs directly in Chrome on Android ([`mobile/README.md`](mobile/README.md)). |
| [`probes/`](probes/) | **Diagnostic Probes**: Read-only scripts for spec inspection, telemetry monitoring, and MCU staging verification. |
| [`tools/`](tools/) | **CLI Utilities**: Wired UART flasher ([`mcu_uart_flash.py`](tools/mcu_uart_flash.py)), telemetry dumpers, token extractors. |
| [`emulator/`](emulator/) | **Hardware Emulator**: Real-time virtual scooter device for offline testing ([`emulator/README.md`](emulator/README.md)). |
| [`tests/`](tests/) | **Automated Tests**: Unit and end-to-end integration tests using `pytest`. |
| [`docs/`](docs/) | **Documentation**: Protocol specifications, UART framing, memory layouts, DFU workflows. |
| [`research/`](research/) | **Reverse Engineering**: Static analysis report ([`REPORT.md`](research/REPORT.md)), function maps, and custom MCU patch. |

#### Working Artifacts (Ignored by Git)

| Directory | Purpose |
|---|---|
| `firmware_ota/` | Official and custom firmware binary images (`.bin`). |
| `secrets/` | Authentication keys, LTMK tokens, and cloud session cache (`*.hex`, `*.json`). |
| `logs/` | Runtime logs, communication traces, and flashing history (`flash_log.jsonl`). |
| `plugins/` | Extracted and decompiled Mi Home Android application packages. |
| `uart_raw/` | Raw serial byte captures from hardware sniffers. |

---

### Documentation Index

| Document | Description |
|---|---|
| [`docs/BLE.md`](docs/BLE.md) | BLE GATT architecture, security-chip login protocol, and Mi Home spec mapping (siid/piid). |
| [`docs/MCU.md`](docs/MCU.md) | GD32 MCU architecture, internal UART frame format, and BLDC motor control registers. |
| [`docs/DFU.md`](docs/DFU.md) | Firmware update procedures, memory staging, CRC verification, and `switchFirmware` gates. |
| [`research/REPORT.md`](research/REPORT.md) | In-depth static reverse engineering analysis of both BLE and MCU binaries. |
| [`mobile/README.md`](mobile/README.md) | Mobile Web Bluetooth PWA architecture, test vectors, and TWA packaging guide. |
| [`emulator/README.md`](emulator/README.md) | Software emulator design, simulated state machines, and test scenario coverage. |

---

### Installation & Prerequisites

- **Python**: Version 3.11 or higher (tested on Windows and Linux).
- **Bluetooth**: BLE 4.2+ adapter supporting Windows BLE APIs or Linux BlueZ.
- **Hardware (Optional for wired flashing)**: USB to 3.3V TTL UART adapter (FTDI / CH340 / CP2102).

#### Setup Virtual Environment

```bash
# Clone the repository
git clone https://github.com/your-repo/scooter-5-pro.git
cd scooter-5-pro

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies (bleak, cryptography, flask, pyserial, pytest, ruff)
pip install -r requirements-dev.txt
```

#### Secrets Configuration (`secrets/`)

Place required credentials in the `secrets/` directory (gitignored):

| File | Purpose |
|---|---|
| `secrets/ltmk.hex` | 16-byte hex LTMK key for the primary scooter (or `ltmk_<MAC>.hex` for multi-scooter setups). |
| `secrets/scooters.json` | Scooter profile database (display names and MAC addresses) used by the WebUI. |
| `secrets/micloud_session.json` | Cached Xiaomi Cloud session tokens (generated via WebUI QR login). |

> 💡 **Retrieving LTMK**: If you do not have your scooter's LTMK, start the WebUI (`python webui/app.py`), navigate to **My Scooters**, log in with your Xiaomi account via QR code, and click **Import Token**.

---

### Quick Start Guide

#### 1. Web Dashboard (Recommended)

Start the local web interface:

```bash
python webui/app.py
```
Open [http://127.0.0.1:8321](http://127.0.0.1:8321) in your browser. From the dashboard you can monitor live telemetry, toggle lights and locks, configure ride parameters, or flash firmware images. Flashing activity is automatically logged to `logs/flash_log.jsonl`.

#### 2. Live Telemetry & Probes (Read-Only)

Connect to the scooter via BLE and inspect properties:

```bash
# Quick property query (battery, speed, odometer, temperatures)
python probes/spec_read.py

# Full telemetry dump saved to docs/telemetry.txt
python tools/dump_telemetry.py

# Monitor live push telemetry events for 120 seconds
python probes/spec_listen.py --secs 120
```

#### 3. Firmware Flashing

> ⚠️ **CRITICAL SAFETY WARNING**: Flashing modified or incorrect firmware carries a risk of bricking your device. The flasher runs in **dry-run / staging-only mode by default** (uploading fragments without activating). To permanently apply firmware, the `--commit` flag must be explicitly passed.

##### Over-The-Air (BLE Target):
```bash
# Upload and activate official or patched BLE firmware
python core/dreame_flasher.py ble firmware_ota/0d41b4df..._upd_xiaomi.scooter.5pro_v2.7.0_0015.bin --commit
```

##### Over-The-Air (MCU Target):
```bash
# Upload MCU firmware over BLE staging
python core/dreame_flasher.py mcu firmware_ota/c0f78c49..._mcu_xiaomi.scooter.5pro_v0007.bin --commit
```

##### Wired Flashing (MCU via USB-TTL UART):
Connect USB-TTL RX/TX/GND to the dashboard/controller UART port @ 19200 baud:
```bash
python tools/mcu_uart_flash.py --port COM3 \
    --fw firmware_ota/c0f78c49..._mcu_xiaomi.scooter.5pro_v0007.bin \
    --md5 c0f78c49f322bd3d71fea19c90241882
```

#### 4. Running the Offline Emulator & Tests

Verify tools, protocol handlers, and flashing pipelines without physical hardware:

```bash
# Run the 7 end-to-end emulator scenarios against real core modules
python emulator/run_emulator.py

# Run the automated pytest suite (35 tests)
pytest

# Code style and syntax check
ruff check .
```

---

## 🇷🇺 Русский

Исследовательский проект по электросамокату **Xiaomi Scooter 5 Pro** (`xiaomi.scooter.5pro`, код модели `0x1928`). Репозиторий содержит полную спецификацию протокола, механизмы безопасности и аутентификации, флешеры для прошивки обоих чипов (по воздуху и по проводу), локальный веб-интерфейс, мобильный клиент Web Bluetooth, программный эмулятор устройства и материалы статического анализа прошивок.

### Архитектура устройства

Самокат построен на двухпроцессорной архитектуре с внутренним межпроцессорным интерфейсом:

```
┌─────────────────────────────────────────────────────────────┐
│                     Клиентский уровень                      │
│   Веб-интерфейс (Flask) │ Мобильный PWA │ Скрипты CLI       │
└──────────────────────────────┬──────────────────────────────┘
                               │ BLE (GATT FE95 / P-256 + AES-CCM)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 Realtek RTL8762C (BLE SoC)                  │
│   • Сервис GATT 0xFE95                                      │
│   • Аутентификация чипа безопасности Mijia (ECDH P-256)     │
│   • Протокол Mi Home Spec (чтение/запись siid/piid)         │
│   • Таргет 0 обновления прошивки BLE-DFU                    │
└──────────────────────────────┬──────────────────────────────┘
                               │ UART @ 19200 бод (8N1)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│             GigaDevice GD32F4 (MCU Cortex-M4F)              │
│   • BLDC-контроллер мотора (векторное управление / FOC)     │
│   • Управление батареей и питанием (BMS)                    │
│   • ПИД-регулятор скорости и агрегатор телеметрии           │
│   • Таргет 1 обновления прошивки MCU-DFU                    │
└─────────────────────────────────────────────────────────────┘
```

---

### Ключевые возможности

- **Ядро протокола и криптография (`core/`)**:
  - Полная реализация протокола Mijia Security Chip: выработка общего секрета ECDH P-256, вывод сессионных ключей HKDF-SHA256, шифрование кадров AES-CCM с контролем монотонных счетчиков.
  - Транспортный уровень фрагментации (`CTR`/`DATA`/`ACK`), обеспечивающий надежную передачу больших пакетов по BLE.
  - Двухцелевой DFU-флешер (`core/dreame_flasher.py`) для BLE-чипа (таргет 0) и MCU (таргет 1) с контролем CRC и докачкой.
- **Локальный веб-интерфейс (`webui/`)**:
  - Автономный сервер Flask на `http://127.0.0.1:8321`.
  - Мониторинг телеметрии в реальном времени: скорость, процент заряда, напряжение, ток, температура, одометр, режимы (Пешеходный, Драйв, Спорт).
  - Управление параметрами в один клик: лимит скорости, круиз-контроль, задний фонарь, рекуперация.
  - Управление профилями нескольких самокатов и получение ключей (LTMK) через QR-код Mi Cloud.
  - Сервисный интерфейс загрузки и прошивки с защитными блокировками.
  - Двуязычный интерфейс с мгновенным переключением языка (Русский / English).
- **Мобильный клиент (`mobile/`)**:
  - Легковесное PWA-приложение на базе Web Bluetooth API.
  - Работает в браузере Chrome на Android без установки APK, серверов или root-прав.
  - Полный перенос криптографии (ECDH P-256, HKDF, AES-CCM) на клиентский JavaScript.
  - Полноэкранный «Режим езды», адаптированный для держателя на руле.
- **Программный эмулятор устройства (`emulator/`)**:
  - Полная программная модель стека самоката (`ScooterDevice`).
  - Комплекс сквозных тестов (`emulator/run_emulator.py`), проверяющий аутентификацию, чтение параметров, телеметрию и полный цикл прошивки без подключения к реальному самокату.
- **Диагностические пробы (`probes/`)**:
  - Набор read-only утилит для исследования спецификаций, захвата push-уведомлений, анализа каналов телеметрии и проверки гейтов MCU.
- **Инструменты и утилиты (`tools/`)**:
  - Прошивальщик MCU по проводу (`tools/mcu_uart_flash.py`) через USB-TTL адаптер.
  - Инструменты распаковки, дамперы телеметрии, сканеры скорости UART и загрузчики прошивок из Mi Cloud.
- **Исследования и реверс (`research/`)**:
  - Подробный отчет о статическом реверсе прошивок ([`research/REPORT.md`](research/REPORT.md)).
  - Карты памяти, дизассемблерные листинги, каталоги функций и верифицированные патчи прошивки ([`research/custom_mcu/`](research/custom_mcu/)).

---

### Структура проекта

```
SCOOTER_5_PRO/
├── core/            # Ядро протокола: BLE-транспорт, аутентификация, движок DFU-прошивки
├── webui/           # Локальный веб-интерфейс (Flask): дашборд, телеметрия, управление
├── mobile/          # Мобильный клиент: Web Bluetooth PWA (Android / Chrome)
├── emulator/        # Модель устройства для офлайн-симуляции и автотестов
├── tools/           # Утилиты: проводной UART-флешер, логгеры, загрузчики ключей
├── probes/          # Исследовательские read-only скрипты
├── tests/           # Автоматизированный тест-сьют (pytest)
├── docs/            # Документация протокола: BLE.md, MCU.md, DFU.md
├── research/        # Отчеты реверса, дизассемблер, патчи прошивки
└── logs/            # Логи работы, аудиты прошивки и дампы телеметрии (gitignored)
```

#### Документация

| Документ | Описание |
|---|---|
| [`docs/BLE.md`](docs/BLE.md) | Архитектура BLE GATT, протокол входа с чипом безопасности, маппинг свойств Mi Home (siid/piid). |
| [`docs/MCU.md`](docs/MCU.md) | Архитектура MCU GD32, формат внутренних UART-кадров, регистры управления BLDC-мотором. |
| [`docs/DFU.md`](docs/DFU.md) | Процедура обновления прошивки, буферизация фрагментов, проверка CRC, гейты `switchFirmware`. |
| [`research/REPORT.md`](research/REPORT.md) | Исчерпывающий отчет о статическом анализе бинарных образов BLE и MCU. |
| [`mobile/README.md`](mobile/README.md) | Архитектура мобильного Web Bluetooth PWA, тестовые векторы, упаковка в TWA. |
| [`emulator/README.md`](emulator/README.md) | Конструкция эмулятора, моделируемые конечные автоматы, сценарии тестирования. |

---

### Установка и настройка

- **Python**: Версия 3.11 или выше (проверено на Windows и Linux).
- **Bluetooth**: Адаптер BLE 4.2+ с поддержкой Windows BLE API или Linux BlueZ.
- **Оборудование (для проводной прошивки)**: Адаптер USB-TTL 3.3V (FTDI / CH340 / CP2102).

#### Настройка виртуального окружения

```bash
# Клонирование репозитория
git clone https://github.com/your-repo/scooter-5-pro.git
cd scooter-5-pro

# Создание и активация venv
python -m venv .venv
# В Windows:
.venv\Scripts\activate
# В Linux/macOS:
source .venv/bin/activate

# Установка зависимостей
pip install -r requirements-dev.txt
```

#### Настройка секретов (`secrets/`)

Поместите необходимые ключи в каталог `secrets/` (входит в `.gitignore`):

| Файл | Назначение |
|---|---|
| `secrets/ltmk.hex` | 16-байтный hex-ключ LTMK для основного самоката (или `ltmk_<MAC>.hex`). |
| `secrets/scooters.json` | Профили самокатов (имена и MAC-адреса) для веб-интерфейса. |
| `secrets/micloud_session.json` | Сохраненная сессия Mi Cloud для автоматического извлечения ключей. |

> 💡 **Как получить LTMK**: Запустите веб-интерфейс (`python webui/app.py`), перейдите на страницу **«Мои самокаты»**, войдите в аккаунт Xiaomi по QR-коду и нажмите кнопку импорта токена.

---

### Быстрый старт

#### 1. Веб-интерфейс (рекомендуемый способ)

Запуск локального сервера:

```bash
python webui/app.py
```
Откройте [http://127.0.0.1:8321](http://127.0.0.1:8321) в браузере. В интерфейсе доступен мониторинг телеметрии, переключение режимов, управление светом и замком, а также прошивка устройств. Лог операций записывается в `logs/flash_log.jsonl`.

#### 2. Телеметрия и диагностика (BLE, read-only)

```bash
# Быстрое чтение параметров (батарея, скорость, одометр, температуры)
python probes/spec_read.py

# Полный дамп свойств в файл docs/telemetry.txt
python tools/dump_telemetry.py

# Прослушивание входящих push-сообщений в течение 120 секунд
python probes/spec_listen.py --secs 120
```

#### 3. Обновление прошивки

> ⚠️ **ПРЕДУПРЕЖДЕНИЕ О БЕЗОПАСНОСТИ**: Прошивка сторонних или поврежденных образов сопряжена с риском выхода устройства из строя. По умолчанию флешер работает в **режиме симуляции / проверки** (заливает фрагменты в staging без применения). Для окончательного переключения на новую прошивку необходимо явно указать флаг `--commit`.

##### Обновление BLE по воздуху:
```bash
python core/dreame_flasher.py ble firmware_ota/0d41b4df..._upd_xiaomi.scooter.5pro_v2.7.0_0015.bin --commit
```

##### Обновление MCU по воздуху:
```bash
python core/dreame_flasher.py mcu firmware_ota/c0f78c49..._mcu_xiaomi.scooter.5pro_v0007.bin --commit
```

##### Проводная прошивка MCU (USB-TTL UART):
Подключите адаптер к линиям UART контроллера (19200 бод, 8N1):
```bash
python tools/mcu_uart_flash.py --port COM3 \
    --fw firmware_ota/c0f78c49..._mcu_xiaomi.scooter.5pro_v0007.bin \
    --md5 c0f78c49f322bd3d71fea19c90241882
```

#### 4. Эмулятор и тестирование (без реального самоката)

Проверка работоспособности инструментов и стека без оборудования:

```bash
# Запуск 7 сквозных сценариев эмулятора против реальных модулей core
python emulator/run_emulator.py

# Запуск полного набора автотестов pytest (35 тестов)
pytest

# Проверка линтером ruff
ruff check .
```

---

### License & Safety Notice

This project is intended strictly for educational and security research purposes under fair use. Operating electric scooters with modified speed limits or custom firmware may violate local traffic regulations, void manufacturer warranties, and affect vehicle stability. The maintainers assume no liability for personal injury, hardware damage, or legal consequences arising from the use of this software.
