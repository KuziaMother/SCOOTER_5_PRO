# Xiaomi Scooter 5 Pro — реверс протоколов и инструменты

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

## Структура проекта

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

## Документация

| Файл | Содержание |
|---|---|
| `docs/BLE.md` | BLE-сторона: GATT, login, телеметрия |
| `docs/MCU.md` | MCU: образ прошивки, UART-протокол |
| `docs/DFU.md` | Обновление прошивок (по воздуху и по проводу) |
| `research/REPORT.md` | Статический реверс образов прошивок (самый подробный разбор) |
| `mobile/README.md` | Мобильный клиент (Web Bluetooth → TWA/APK) |

## Установка

Python 3.11+ (проверено на Windows).

```bash
pip install -r requirements-dev.txt   # зависимости (вкл. pyserial) + pytest/ruff
```

### Секреты (`secrets/`, в .gitignore)

| Файл | Назначение |
|---|---|
| `ltmk.hex` / `ltmk_<MAC>.hex` | LTMK — ключ логина конкретного самоката |
| `scooters.json` | Профили самокатов (name + MAC) для веб-интерфейса |
| `micloud_session.json` | Сессия Mi Cloud (QR-логин; общая с `tools/xct/`) |

Для нового самоката LTMK получается через Mi Cloud — страница «Мои
самокаты» в веб-интерфейсе (`webui/micloud_ltmk.py`).

## Быстрый старт

### Веб-интерфейс (дашборд, управление, прошивка)

```bash
python webui/app.py        # http://127.0.0.1:8321  (только localhost)
```

Несколько самокатов, чтение свойств, SET по клику, режим езды, загрузка
прошивок на сервисной странице. Журнал заливок — `logs/flash_log.jsonl`.

### Телеметрия (BLE, read-only)

```bash
python probes/spec_read.py               # быстрое чтение свойств
python tools/dump_telemetry.py           # полный дамп в таблицу (docs/telemetry.txt)
python probes/spec_listen.py --secs 120  # слушать ПУШИ: меняй состояние (газ/свет/движение)
```

### Прошивка

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

### Эмулятор и тесты (без железа)

```bash
python emulator/run_emulator.py   # настоящие core/dreame_auth + dreame_flasher против софтверной модели
pytest                            # тест-сьют (вкл. полный цикл прошивки на эмуляторе)
ruff check .                      # линтер (E9+F — codebase это research-скрипты, не библиотека)
```

## Логи

Все `.log`-файлы лежат в `logs/`:

- `tools/uart_logger.py` — по умолчанию пишет в `logs/uart_activity.log`
  (сырые захваты байтов — в `uart_raw/`); анализ: `python tools/uart_logger.py --show logs/uart_activity.log`;
- `probes/spec_listen.py` — `logs/push_capture_*.txt`;
- веб-интерфейс — журнал заливок `logs/flash_log.jsonl`.

## Тесты

```bash
pytest
```

Скрипты намеренно используют `sys.path.insert` до импортов (research-код,
не пакет) — ruff настроен только на реальные ошибки (`E9`, `F`).
