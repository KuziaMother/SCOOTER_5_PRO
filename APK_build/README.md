# APK_build — мобильный клиент (Web Bluetooth PWA → TWA/APK)

Цель: подключаться к самокату **прямо с телефона**, без ПК. Задача решена
переносом BLE-транспорта и криптографии из Python (`bleak` + `cryptography`,
работают только на Windows/Linux/macOS) на **Web Bluetooth API**, который
поддерживает Chrome на Android напрямую из браузера — без установки чего-либо.

## Что уже готово

### `pwa/` — автономный веб-клиент, работает без сервера

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

UI — тот же дизайн, что в основном `webui/` этой сессии: hero-сводка с кольцом
заряда, список свойств без карточек, интерактивное управление (SET по клику),
полноэкранный **режим езды** для крепления на руль.

### Криптография проверена побайтово ДО первого реального подключения

Ключевой риск такого переноса — тонкая ошибка в AES-CCM/ECDH/HKDF, которая
молча всё сломает и будет незаметна без осциллографа. Поэтому каждый
примитив сверен с Python `cryptography` через Node.js (`APK_build/test/`):

```bash
cd APK_build/test
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

### Живой смоук-тест

`pwa/` поднят локальным http.server, страница грузится без единой ошибки в
консоли, все ES-модули резолвятся, UI рендерится (проверено в этой сессии).
**Реальное BLE-подключение НЕ тестировалось** — в песочнице нет доступа к
Bluetooth-железу. Первая проверка на реальном самокате — за пользователем.

## Чего не хватает / на что обратить внимание при первом реальном тесте

1. **LTMK вводится вручную.** На телефоне нет `secrets/ltmk.hex` — при первом
   подключении страница спросит его через `prompt()` и сохранит в
   `localStorage` браузера (только на этом устройстве, никуда не уходит).
   Скопируйте содержимое `secrets/ltmk.hex` с ПК.
2. **Web Bluetooth не даёт коннект по MAC напрямую** (приватность браузера) —
   при нажатии «Подключиться» откроется системный диалог выбора устройства,
   надо выбрать `xiaomi.scooter.5pro` из списка. Это обязательный шаг Chrome,
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

## `twa/` — обёртка в Android-APK (Trusted Web Activity)

TWA — тонкая обёртка вокруг Chrome (Custom Tabs), а не WebView: поэтому
Web Bluetooth продолжает работать (обычный Cordova/Capacitor WebView его
не поддерживает вообще, это была бы тупиковая ветка).

### Статус: `.apk` СОБРАН (2026-08-20), тулчейн развёрнут на этой машине

Собрано: `twa/app-release-signed.apk` (946 КБ, `ru.scooter5pro.app`, v1,
подпись проверена `apksigner verify`) + `twa/app-release-bundle.aab`.
Всё вне git (`.gitignore`: `APK_build/twa/`).

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

## Структура

```
APK_build/
  pwa/                  — веб-клиент (то, что грузится в TWA/браузер)
  twa/                  — проект Bubblewrap (Android-обвязка, генерируется)
  test/                 — офлайн-проверка крипты + генератор иконок
  README.md             — этот файл
```
