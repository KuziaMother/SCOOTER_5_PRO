# BLE-сторона (RTL8762C): GATT, login, телеметрия

Тематическая справка по беспроводному чипу самоката `xiaomi.scooter.5pro`
(MAC `2C:19:5C:DE:DE:88`, BLE fw `2.7.0_0015`).

> **Источник истины — [`FACTS.md`](FACTS.md)** (проверенные константы, иерархия
> доказательств). Здесь — тематическая сводка по BLE-чипу; детали, поправки и
> доказательства — в FACTS.md и в историческом разборе
> [`dreame_dfu_protocol.md`](dreame_dfu_protocol.md). Статический реверс образа —
> `research/REPORT.md` (§1–§7, §19, §30).

---

## 1. Аппаратура

| Параметр | Значение | Как узнано |
|----------|----------|------------|
| BLE SoC | **Realtek RTL8762C** | опкод 3 на `0x001c` → `"RTL8762C"` |
| Версия BLE fw | `2.7.0_0015` | read char `0x0004` (без логина) |
| MCU fw (для справки) | `0007` | опкод 1 на `0x001c` |
| ATT MTU | 247 (max write w/o resp 244) | negotiated |
| Пропускная способность | кадры канала **18 Б** (фиксировано устройством) | проверено |

Образ BLE-чипа: открытый bootloader/OTA + **AES-зашифрованный APP** (ключ в OTP,
XIP-decrypt) + RSA/Mijia-подпись → APP из `.bin` не расшифровать (REPORT §3–§4, §6.2).
Карта образа и трейлер `MITFOTA` — в [`DFU.md`](DFU.md) §2.

**Слои:** слой спецификации Mi Home (siid/piid, GATT-свойства) живёт именно здесь,
в BLE-чипе. MCU — поставщик сырых значений; телефон читает/пишет свойства у BLE-чипа,
тот опрашивает MCU запросами `63 CMD` по USART3 (см. [`MCU.md`](MCU.md) §1 «Слои»).

## 2. GATT: сервис FE95

UUID характеристики собирается как
`String.format("0000%04x-0000-1000-8000-00805f9b34fb", n)` (дизасм, проверено).

| sid (наш код) | ATT handle | Назначение |
|---|---|---|
| `0x0004` | read (hnd≈15) | **Версия BLE открытым текстом, БЕЗ логина**: `"2.7.0_0015"` (20 Б, null-pad) |
| `0x0005` | read+notify (hnd≈17) | Mijia **combo/register**: bindkey/OOB, country code, restore/retry; молчит после привязки |
| `0x0010` | `0x0015` | CONTROL: A4, login-start (`20 00 00`), результат (`21`=ok/`22`=fail); op-коды bind (§5) |
| `0x0016` | `0x0018` | LOGIN: канальный транспорт login (MNG/CTR/DATA/ACK), канал **5** |
| `0x0017` | `0x001b` | DFU командный (W/RESP) |
| `0x0018` | `0x001e` | DFU данные (только WWR) |
| `0x001a` | `0x0021` | SPEC write (телеметрия, канал 0) |
| `0x001b` | `0x0024` | SPEC notify (ответы/пуши телеметрии) |
| `0x001c` | `0x0027` | Инфо-канал BLE-чипа (версии/железо/серийник, без логина) |

`0x0004` — самый дешёвый способ узнать версию BLE: один read без ECDH-логина и без AES.
Отдаёт только BLE-часть (`2.7.0_0015`), без MCU-суффикса `.0007`.

`0x0005` — стандартная Mijia-характеристика привязки/регистрации (write: country code,
bindkey index, APP-PWD/OOB, restore/retry; notify: `character_changed`). У нас молчит,
потому что привязка завершена и заходим через security-chip сессию; оживает только при
первичной регистрации.

## 3. Канальный транспорт (общий для всех каналов)

```
CTR   [00 00][00][channel][fc u16]     заявка на передачу fc кадров
ACK   [00 00][01][status][seq u16…]    status 01=готов, 00=принято, 05=pull (перешли seq)
DATA  [seq u16][данные]                seq начинается с 1
EVENT [00 00][02][xx] + payload        входящее сообщение от устройства
ACK2  [00 00][03][xx]                  подтверждение EVENT
```

- **frameSize = 18 Б — фиксировано устройством, не тюнится.** Устройство собирает
  сообщение по смещению `seq × frameSize`, размер должен *совпадать*.
- **«Окно = 1» — артефакт, а не ограничение:** `ACK 05 [seq]` — механизм восстановления.
  Если послать все кадры сообщения подряд (пейсинг ~10 мс), устройство принимает их без
  единого pull'а. Измерено: 29 кадров (фрагмент 512 Б) — 0.9 с, 0 pull'ов против 2.9 с /
  28 pull'ов при burst=1. `dreame_flasher.py` по умолчанию шлёт все кадры (`BURST=0`).

## 4. Login (security chip)

| Факт | Значение |
|---|---|
| Пин | `12****` |
| Схема | ECDH P-256 → HKDF-SHA256(`shared‖ltmk`) → **sessionKey 64 Б** |
| Подтверждение | AES-CCM(key=`sk[16:32]`, nonce=`10..1b`, tag 4), plaintext = CRC32(devPubKey) LE |
| Канал login | **5** на `0x0016` |
| Ответ | `21 00 00 00` = OK, `22…` = отказ |

### `ltmk` — ключ логина
Достаётся из облака: `POST /app/share/askbluetoothkey {type:own,did,keyid:0}` →
`result.{key,encrypt_type}`. `encrypt_type==0`: `ltmk = hex_decode(key)`;
`encrypt_type==1` (пин задан): `ltmk = AES-128-CBC-NoPad(key=MD5(pin), iv=7aa4c68c…3800, ct)`.

**Ротация:** отвязка — жив; factory-reset — жив; **ре-привязка через Mi Home — меняется**
(login → `0x22`), т.к. bind заново провижинит ключ (§5). Восстановление — свежий
`askbluetoothkey` по сохранённой Mi-сессии (`secrets/micloud_session.json`) + деривация PIN-ом.

## 5. Привязка (bind) — отдельная процедура, не login

Control-канал `0x0010`, опкоды bind:

```
0x10 (10800000)  BIND-REQUEST   PHONE→DEV   |  0x20  login-start
0xe1 (e1000000)  device готов   DEV→PHONE   |  0x21  login OK / 0x22 fail
0x13 (13000000)  BIND-COMMIT    PHONE→DEV
0x11 (11000000)  BIND DONE      DEV→PHONE
```

Между `0x10` и `0x13` на login-канале `0x0016` — взаимная аутентификация по X.509
cert-chain'ам (Mijia device cert + Mijia CA, та же PKI, что подпись прошивки MITFOTA) +
токен + ECDH. Внутри этой cert-аутентифицированной сессии **провижинится новый `ltmk`** —
поэтому каждый bind его ротирует. Из снупа `ltmk` не извлечь (эфемерный ключ телефона);
ключ берётся из облака, снуп даёт только протокол.

## 6. Телеметрия: MIoT-spec поверх BLE ✅

| Факт | Значение |
|---|---|
| Характеристика записи | `0x001a` (write) |
| Характеристика ответа | `0x001b` (notify) |
| **Номер канала** | **0** (НЕ 6 — дизасм вёл в заблуждение, прав снуп) |
| frameSize | 18 Б, дробить обязательно |
| CRC32 | НЕ используется |
| op-коды | GET `op=2` → ответ `op=3`; SET `op=0` → ответ `op=1`; ACTION `op=5` (siid/aiid в шапке) |
| Правило | `op_ответа = op_запроса \| 1` |
| Ответ устройства | многокадровый поток: CTR от устройства → ACK 01 → кадры → ACK 00 |

### Шифрование (`BleSecurityChipEncrypt`, проверено)
```
app->dev: key=sk[16:32], iv=sk[36:40]
dev->app: key=sk[0:16],  iv=sk[32:36]
nonce  = iv ‖ 00 00 00 00 ‖ counterBytes(4)          (32-бит LE)
провод = [u16 LE counter] ‖ AES-CCM(key, nonce, кадр) ; tag = 4 Б
```
Счётчик приложения начинается с 0 и растёт на каждое сообщение; у устройства свой.

### Формат кадра spec
```
заголовок: [u16 LE len|0x2000][u16 LE tid][u8 op][u8 count]

GET-элемент:      [u8 siid][u16 LE piid]                                   (3 Б)
SET-элемент:      [u8 siid][u16 LE piid][u16 LE (type<<12)|vlen][value]
ответ (ok):       [u8 siid][u16 LE piid][u16 LE status][u16 LE (type<<12)|len][value]
ответ (ошибка):   [u8 siid][u16 LE piid][u16 LE status]
```

Коды ошибок: `0xf05d` = **−4003** (2-й и далее объект в batch), `0xf05f` = **−4001**
(write/action-свойство на read). ⚠️ **Устройство обслуживает только ПЕРВЫЙ объект в
запросе** — читать по одному свойству.

### Типы значений (`SpecValueType`)
```
BOOL=0(1Б) UINT8=1(1) INT8=2(1) UINT16=3(2) INT16=4(2)
UINT32=5(4) INT32=6(4) UINT64=7(8) INT64=8(8) FLOAT=9(4) STRING=10(перем.)
```
type 9 = FLOAT32 — читать как целое нельзя (напряжение выглядит как 1168572416).

**Карта свойств (siid/piid), единицы, перечисления и журналы поездок** — в
[`FACTS.md`](FACTS.md) «Телеметрия» (полные таблицы) и в `research/REPORT.md`
§6.13–6.14. Карта извлечена из плагина Mi Home (`plugins/modules/*.js`) и в публичной
MIoT-спеке отсутствует.

### SET / factory reset (проверено live)
- `SET IS_LOCKED(2,2)=1/0` — работает; ответ `op=1`, объект `[siid][piid][status]`.
- Factory reset: `SET RESTORE_SCOOTER_SETTINGS (4,6) BOOL=1` — трогает только
  пользовательские настройки; прошивка и `ltmk` не затронуты. Вручную: газ + 5× кнопка питания.

### Пуши свойств
Плагин имеет `parseNotifyData` с ветками `prop.<siid>.<piid>` ⇒ существует подписка на
изменения (CCCD на `0x001b`, ставится `Transport.connect()`). Готовый слушатель:
`probes/spec_listen.py`.

## 7. Инфо-канал `0x001c` (обслуживается BLE-чипом, БЕЗ логина)

Ровно 4 опкода; остальные 252 → `err 0x02`.
Формат ошибки: `ff [len] [echo_op] [errcode]`; `0x02` = опкода нет, `0x08` = нужен параметр.

```
0 -> 0103                 (версия протокола?)
1 -> mcu_version '0007'   (используется и как poll MCU-установки, см. DFU.md)
3 -> hardware 'RTL8762C'
8 -> serial (нужен параметр offset; серийник постранично)
```

## 8. MiBeacon (реклама, пассивно)

`1055 d350 00 88dede5c192c` — 11 Б, полностью учтены:
`fctrl=0x5510` (version 5, registered, mac), `product_id=0x50d3` (= 20691, Scooter 5 Pro),
`frame_cnt=0`, MAC. Биты `object=0`, `encrypted=0` ⇒ **телеметрии в рекламе нет**.

## 9. Проводной доступ к BLE-чипу (UART)

Серийник **записывается** по UART на сам BLE-чип (community-инструмент
`scooterteam/bw-flasher`, `scripts/set_serialnumber.py`):

```
5A 12 97 [len] 30 [19 ASCII серийника] [CRC16-H][CRC16-L]   (19200 8N1, CRC-16/XMODEM)
```

UART ведёт к бутлоадеру чипа НИЖЕ уровня приложения: Mijia-подпись защищает только
беспроводной OTA (`switchFirmware`), физический бутлоадер её не проверяет.
⚠️ Границы проекта — см. FACTS.md «Серийник»: документируем механизм, рецепт подмены
серийника ради снятия лимита скорости НЕ делаем.

BLE-модуль DFU по 5A-кадрам (CMD `0x02` DeviceInfo / `0x03` start / `0x04` data(128) /
`0x05` end / `0x97` set-serial) — в [`DFU.md`](DFU.md) §7.

## 10. Облачный API (Mi Cloud)

| Endpoint | Параметры |
|---|---|
| `/v2/device/latest_ver` | прошивки BLE (`url`/`md5`) и MCU (`mcu_safe_url`/`mcu_md5`) — см. DFU.md |
| `/app/share/askbluetoothkey` | `{type:own,did,keyid:0}` → `ltmk` (§4) |
| `/v2/plugin/fetch_plugin` | RN-бандл плагина (магия `FB0BD1E5`, распаковка `tools/unpack_rambundle.py`) |

Константы **только из DEX** (`L_m_j/bx9;-><clinit>`): `api_version=10116`, `api_level=111`.
Константы API не угадывать никогда (реальный случай: выдуманный 10056 → пустой ответ).

## 11. Инструменты

| Скрипт | Назначение |
|---|---|
| `dreame_auth.py` | логин + сбор информации (read-only); транспорт A4/MNG, DFU-команды |
| `probes/spec_read.py --siid N --piid M` | чтение одного свойства MIoT-spec |
| `probes/spec_listen.py` / `spec_listen_web.py` | подписка на пуши свойств |
| `probes/telemetry_listen.py` | логин + пассивная прослушка нотификаций |
| `probes/beacon_scan.py` | пассивный скан MiBeacon-рекламы (без подключения) |
| `probes/mcu_opcode_sweep.py` | перебор опкодов инфо-канала `0x001c` |
| `tools/dump_telemetry.py [--all]` | полный дамп телеметрии в `docs/telemetry.txt` |
| `webui/app.py` | дашборд: живая телеметрия, SET, профили самокатов, `/service` (DFU) |

⚠️ `docs/telemetry.txt` содержит серийники и OOB-код привязки — в `.gitignore`, не публиковать.
