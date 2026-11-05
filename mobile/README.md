# Mobile Client / Мобильный клиент (Web Bluetooth PWA → TWA/APK)

> 📄 **Language / Язык:** [🇬🇧 English](#-english) · [🇷🇺 Русский](#-русский)

---

## 🇬🇧 English

Goal: Connect to the scooter **directly from a phone**, without a PC. This is achieved
by porting the BLE transport and cryptography stack from Python (`bleak` + `cryptography`,
which only run on desktop OS) to the **Web Bluetooth API**, supported natively by Chrome
on Android directly from the browser — without installing any apps.

### What is already done

#### `pwa/` — standalone web client (works without a backend server)

A complete port of the communication protocol to JavaScript (ES modules, zero build step/bundlers):

| File | Ported functionality |
|---|---|
| `js/aes-ccm.js` | AES-CCM (RFC 3610) built on top of WebCrypto (CBC-MAC + CTR — no custom AES implementations) |
| `js/bin.js` | Binary pack/unpack helpers, CRC32 |
| `js/queue.js` | Async queue (replacement for Python's `asyncio.Queue`) |
| `js/transport.js` | Port of `Transport` from `dreame_auth.py` to `navigator.bluetooth` |
| `js/login.js` | ECDH P-256 + HKDF + AES-CCM confirmation (security-chip login) |
| `js/spec.js` | MIoT-spec protocol: GET (op=2) and SET (op=0) over session encryption |
| `js/props.js` | Catalog of properties/signatures/formatting — port of `webui/props.py` |
| `js/app.js` | UI orchestration: connection lifecycle, polling, rendering (hero/list/ride mode) |
| `css/style.css` | 1:1 copy of `webui/static/style.css` (pure CSS, no Flask dependencies) |

UI follows the same modern design as `webui/`: hero summary with battery gauge ring,
clean property cards, interactive control (click-to-SET), and a full-screen **Ride Mode**
tailored for handlebar phone mounts.

#### Cryptography verified byte-for-byte BEFORE real-world testing

The greatest risk when porting low-level protocol crypto is subtle differences in AES-CCM/ECDH/HKDF,
which would silently break authentication without an obvious error. Every cryptographic primitive
was verified against Python's `cryptography` via Node.js (`mobile/test/`):

```bash
cd mobile/test
node test_ccm.mjs          # AES-CCM: 9 test vectors + corrupted tag rejection test
node test_crc_hkdf.mjs     # CRC32 + HKDF-SHA256
node test_ecdh_step1.mjs   # + separate Python verification step for ECDH shared-secret
```

All test cases matched byte-for-byte, including:
- ECDH P-256 shared secret (X-coordinate) — verified across JS and Python using shared keys;
- HKDF-SHA256(shared‖ltmk) using the exact same salt and info parameters as `dreame_auth.py`;
- AES-CCM(tag=4) encrypt/decrypt across 9 vectors (empty plaintext, block boundaries at 15/16/17 bytes,
  and real spec-frame sizes), verifying corrupted tag rejection;
- **SET response parsing** (`0b20010001010202000000`): uncovered and resolved a subtle protocol detail:
  a GET response on `status==0` includes `tl+value` (7+vlen bytes), whereas a SET response on `status==0`
  is ALWAYS exactly 5 bytes (`siid+piid+status`) with no echoed value. Without separating these formats,
  the parser dropped the SET acknowledgement entirely (see `parseSetResponse` in `spec.js`).

#### Live smoke testing

`pwa/` served via a local web server loads cleanly with zero console errors, all ES modules resolve,
and the UI renders accurately. Automated tests do not perform live over-the-air BLE connections
due to environment isolation; real hardware verification is performed directly against the scooter.

### What to note during your first live test

1. **LTMK key is entered manually:** Since mobile browsers lack access to `secrets/ltmk.hex`,
   the page will prompt for the key on first connection and store it securely in browser
   `localStorage` (strictly local to your device). Copy the key from `secrets/ltmk.hex`.
2. **Web Bluetooth requires user device selection:** Due to browser privacy policies, Web Bluetooth
   cannot connect silently to a known MAC address. Clicking "Connect" opens the Android system device picker;
   select `xiaomi.scooter.5pro` from the list.
3. **Platform compatibility:** Web Bluetooth is supported on Android in Chrome and Edge.
   iOS Safari does not support Web Bluetooth due to Apple platform restrictions.
4. **Frame pacing & timings:** Inter-frame delays (30ms between DATA frames, 350ms between property polls)
   are adopted from the Python stack. If frame drops occur on specific mobile BLE chipsets,
   these timings can be tuned in `transport.js`.
5. **Icons:** Placeholder icons are generated (`pwa/icons/*.png`). Replace them with custom brand assets
   for production deployments.

### `twa/` — Android APK Wrapper (Trusted Web Activity)

TWA is a lightweight Android wrapper around Chrome (Custom Tabs), not an ordinary WebView:
Web Bluetooth continues to function fully (whereas standard Cordova/Capacitor WebViews do not support it).

#### Status: `.apk` BUILT (2026-08-20), toolchain configured

Built: `twa/app-release-signed.apk` (946 KB, `ru.scooter5pro.app`, v1, signature verified with `apksigner verify`)
along with `twa/app-release-bundle.aab`. Both remain outside git (`.gitignore`: `mobile/twa/`).

Toolchain configuration (stored in `~/.bubblewrap/`, config `~/.bubblewrap/config.json`):
- **JDK 17** Temurin 17.0.20 x64 (`jdk/jdk17-bin`).
- **Android SDK** (`android_sdk/`): licenses accepted, `platforms;android-36`, `build-tools;34.0.0` and `build-tools;36.1.0`
  (required by bubblewrap for zipalign).

Resolved Windows + git-bash bubblewrap quirks:
- **Path/PATH issue:** `JdkHelper` writes to `Path`, while MSYS exports `PATH` → JDK binaries were missing
  from the active PATH. Workaround: Keystore was generated with `keytool`, AAB signed via `jarsigner` with absolute path;
  `gradlew.bat` natively uses `JAVA_HOME`.
- **Port validation:** `validateHost` (`domainToASCII`) rejects any `host:port` — manifest for `init` must be served on port 80/443.
- **Non-interactive terminal support:** Scripted driver `test/bw_init_driver.mjs` feeds parameters to Bubblewrap
  to avoid crashes without an interactive TTY.

Signing Keystore: `twa/android.keystore`, alias `android`; credentials stored in `secrets/apk_keystore.txt`.

**Important TWA requirement:** Content must be hosted over **genuine HTTPS** with configured
Digital Asset Links (`assetlinks.json` on the same domain) so Chrome suppresses the URL address bar.
To deploy a production APK: host `pwa/` (e.g., GitHub Pages or custom web server) and rebuild with
`BW_MANIFEST=https://<your-domain>/manifest.webmanifest`.

### Directory layout

```
mobile/
  pwa/                  — Web client (served to browser or TWA)
  twa/                  — Bubblewrap project (Android wrapper, generated)
  test/                 — Offline crypto verification + icon generator
  README.md             — Documentation (this file)
```

---

## 🇷🇺 Русский

Цель: подключаться к самокату **прямо с телефона**, без ПК. Задача решена
переносом BLE-транспорта и криптографии из Python (`bleak` + `cryptography`,
работают только на Windows/Linux/macOS) на **Web Bluetooth API**, который
поддерживает Chrome на Android напрямую из браузера — без установки чего-либо.

### Что уже готово

#### `pwa/` — автономный веб-клиент, работает без сервера

Полный порт протокола на JavaScript (ES-модули, без сборки/бандлера):

| Файл | Что переносит |
|---|---|
| `js/aes-ccm.js` | AES-CCM (RFC 3610) поверх WebCrypto (CBC-MAC + CTR — своего AES не пишем) |
| `js/bin.js` | struct.pack/unpack-хелперы, CRC32 |
| `js/queue.js` | асинхронная очередь (замена `asyncio.Queue`) |
| `js/transport.js` | порт `Transport` из `dreame_auth.py` на `navigator.bluetooth` |
| `js/login.js` | ECDH P-256 + HKDF + AES-CCM confirmation (security-chip login) |
| `js/spec.js` | MIoT-spec протокол: GET (op=2) и SET (op=0) поверх session-шифрования |
| `js/props.js` | каталог свойств/подписи/форматирование — порт `webui/props.py` |
| `js/app.js` | UI-оркестрация: подключение, поллинг, рендер (hero/список/ride mode) |
| `css/style.css` | 1:1 копия текущего `webui/static/style.css` (чистый CSS, без завязки на Flask) |

UI — тот же дизайн, что в основном `webui/`: hero-сводка с кольцом
заряда, список свойств без карточек, интерактивное управление (SET по клику),
полноэкранный **режим езды** для крепления на руль.

#### Криптография проверена побайтово ДО первого реального подключения

Ключевой риск такого переноса — тонкая ошибка в AES-CCM/ECDH/HKDF, которая
молча всё сломает и будет незаметна без осциллографа. Поэтому каждый
примитив сверен с Python `cryptography` через Node.js (`mobile/test/`):

```bash
cd mobile/test
node test_ccm.mjs          # AES-CCM: 9 векторов + проверка отклонения битого тега
node test_crc_hkdf.mjs     # CRC32 + HKDF-SHA256
node test_ecdh_step1.mjs   # + отдельный python-шаг для ECDH shared-secret
```

Все сошлись побайтово, включая:
- ECDH P-256 shared-secret (X-координата) — сравнение JS↔Python на общем ключе;
- HKDF-SHA256(shared‖ltmk) с тем же salt/info, что в `dreame_auth.py`;
- AES-CCM(tag=4) encrypt/decrypt на 9 векторах (пустой plaintext, границы
  блока 15/16/17Б, размеры реальных spec-кадров) + отклонение испорченного тега;
- **разбор SET-ответа** (`0b20010001010202000000`) — попутно нашёлся и
  починился баг: GET-ответ при `status==0` несёт ещё `tl+value` (7+vlen байт),
  а SET-ответ при `status==0` — ВСЕГДА ровно 5 байт (siid+piid+status), без
  эха значения. Если не различать эти два формата, парсер теряет объект
  SET-подтверждения целиком (см. `parseSetResponse` в `spec.js`).

#### Живой смоук-тест

`pwa/` поднят локальным http.server, страница грузится без единой ошибки в
консоли, все ES-модули резолвятся, UI рендерится.
**Реальное BLE-подключение НЕ тестировалось** в автоматических тестах — в тестовой среде нет доступа к
Bluetooth-железу. Первая проверка на реальном самокате — за пользователем.

### Чего не хватает / на что обратить внимание при первом реальном тесте

1. **LTMK вводится вручную.** На телефоне нет `secrets/ltmk.hex` — при первом
   подключении страница спросит его через `prompt()` и сохранит в
   `localStorage` браузера (только на этом устройстве, никуда не уходит).
   Скопируйте содержимое `secrets/ltmk.hex` с ПК.
2. **Web Bluetooth не даёт коннект по MAC напрямую** (приватность браузера) —
   при нажатии «Подключиться» откроется системный диалог выбора устройства,
   надо выбрать `xiaomi.scooter.5pro` из списка. Это обязательное поведение Chrome,
   не баг.
3. **Web Bluetooth работает только в Chrome/Edge на Android.** iOS Safari его
   не поддерживает вообще — это ограничение платформы Apple, обойти нельзя.
4. **Тайминги/паузы между кадрами** (30мс между DATA-фреймами, 350мс между
   опросами свойств) взяты из Python-версии как есть — на реальном Web
   Bluetooth стеке телефона могут понадобиться другие значения, если пойдут
   потери кадров/таймауты. Первое, что стоит подкрутить при проблемах.
5. **Иконки — плейсхолдеры** (`pwa/icons/*.png`, сгенерированы
   `test/gen_icons.mjs` — сплошной круг, не логотип). Заменить перед реальным
   релизом.

### `twa/` — обёртка в Android-APK (Trusted Web Activity)

TWA — тонкая обёртка вокруг Chrome (Custom Tabs), а не WebView: поэтому
Web Bluetooth продолжает работать (обычный Cordova/Capacitor WebView его
не поддерживает вообще, это была бы тупиковая ветка).

#### Статус: `.apk` СОБРАН (2026-08-20), тулчейн развёрнут на этой машине

Собрано: `twa/app-release-signed.apk` (946 КБ, `ru.scooter5pro.app`, v1,
подпись проверена `apksigner verify`) + `twa/app-release-bundle.aab`.
Всё вне git (`.gitignore`: `mobile/twa/`).

Что развёрнуто (всё в `~/.bubblewrap/`, конфиг — `~/.bubblewrap/config.json`):
- **JDK 17** Temurin 17.0.20 x64 — `jdk/jdk17-bin` (скачан вручную с Adoptium;
  встроенный скачиватель bubblewrap в этой среде обрывается).
- **Android SDK** — `android_sdk/`: лицензии приняты, `platforms;android-36`,
  `build-tools;34.0.0` + `build-tools;36.1.0` (36.1.0 требует сам bubblewrap
  для zipalign). `sdkmanager` из этой раскладки требует явный `--sdk_root`.

Подводные камни bubblewrap на Windows + git-bash (обойдены):
- **Path/PATH-баг**: `JdkHelper` пишет в `Path`, а MSYS экспортирует `PATH`
  (Node на Windows — case-insensitive, переименовать нельзя) → JDK-bin не
  попадает в действующий PATH, `keytool`/`jarsigner` «не являются командами».
  Обход: keystore создан вручную тем же `keytool`; AAB подписан `jarsigner` из
  JDK с абсолютным путём; `gradlew.bat` не страдает (берёт `JAVA_HOME`).
- **host без порта**: `validateHost` (`domainToASCII`) отклоняет ЛЮБЫЕ
  `host:port` — манифест для `init` должен отдаваться на порту 80/443
  (`python -m http.server 80 --bind 127.0.0.1` из `pwa/`).
- **Интерактивный визард без TTY падает** (`ERR_USE_AFTER_CLOSE`) — нон-интерактивный
  драйвер: `test/bw_init_driver.mjs` (зовёт реальные `init()`/`loadOrCreateConfig()`
  со scripted-промптом; ответы — по тексту вопроса, не по позиции).

Подписывающий keystore: `twa/android.keystore`, alias `android`; пароль и
координаты — в `secrets/apk_keystore.txt` (вне git). Потеря ключа =
невозможность обновлять приложение под тем же packageId.

**Важное ограничение TWA**, которого нет у обычного Cordova/Capacitor:
контент должен быть доступен по **настоящему HTTPS-адресу** с настроенным
Digital Asset Links (`assetlinks.json` на том же домене), иначе Chrome
показывает адресную строку поверх приложения (работает, но не «как родное
приложение»). Значит `pwa/` нужно захостить (например, на `gitea.entosis.ru`
или GitHub Pages) прежде чем собирать финальный подписанный APK — локальный
`http.server` для сборки TWA не годится, только для разработки/отладки.
Текущий APK собран с `host=127.0.0.1` (локальный `http.server` на порту 80) —
это сборочная проверка: на телефоне он откроет `https://127.0.0.1/...` и не
дождётся ответа. Для финального APK: захостить `pwa/` (например, на
`gitea.entosis.ru` или GitHub Pages) и пересобрать тем же драйвером с
`BW_MANIFEST=https://<домен>/manifest.webmanifest` (+ assetlinks.json — тогда
уйдёт адресная строка). Локальный FILE-путь к манифесту не работает
(bubblewrap тянет его только по HTTP).

### Структура

```
mobile/
  pwa/                  — веб-клиент (то, что грузится в TWA/браузер)
  twa/                  — проект Bubblewrap (Android-обвязка, генерируется)
  test/                 — офлайн-проверка крипты + генератор иконок
  README.md             — этот файл
```
