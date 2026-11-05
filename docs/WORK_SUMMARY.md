# Work Summary: Codebase English Refactoring, Localization & Documentation Enhancement

**Date:** November 5, 2026  
**Repository:** Xiaomi Scooter 5 Pro (`SCOOTER_5_PRO`)  
**Target Architecture:** Realtek RTL8762C (BLE SoC) + GigaDevice GD32F4 (Cortex-M4F MCU)

---

## 1. Executive Summary

This initiative encompassed a repository-wide refactoring to make **English the primary language** across the entire codebase, user-facing applications, diagnostic utilities, and documentation, while enhancing reliability, code quality, and bilingual capabilities:

1. **Complete Python Codebase Translation**: Every `.py` file across `core/`, `webui/`, `tools/`, `probes/`, `emulator/`, `tests/`, and `research/` was refactored so that all in-program strings, docstrings, code comments, CLI help text, error messages, and exception logs are in clean, idiomatic English (with 0 unintended Cyrillic characters remaining).
2. **Bilingual Frontend Architecture**: Preserved and expanded full English/Russian language switching for the WebUI (`webui/static/i18n.js` and `webui/props.py`) and Mobile PWA (`mobile/pwa/js/i18n.js`), defaulting to English with instant client-side switching.
3. **Comprehensive Documentation Overhaul**: Completely updated `README.md`, `emulator/README.md`, and `mobile/README.md` to place English first, complete with dual-MCU ASCII architecture diagrams, feature breakdowns, and CLI quick-start guides.
4. **Critical Bug Fixes & Protocol Hardening**: Fixed a spec-channel wire format counter issue in `probes/spec_read.py`, resolved missing import dependencies in `emulator/run_emulator.py`, and verified all 35 tests pass end-to-end.

---

## 2. WebUI & Mobile PWA Localization

### Dynamic Client-Side Internationalization (`i18n.js`)
- Created [`webui/static/i18n.js`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/webui/static/i18n.js) and [`mobile/pwa/js/i18n.js`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/mobile/pwa/js/i18n.js) providing lightweight dictionary-based translations.
- Added persistent language selection via `localStorage` (defaulting to English, with full Russian support).
- Integrated language toggle button (`EN | RU`) seamlessly into navigation bars across desktop and mobile headers.
- Translated all UI elements:
  - Hero banners, gauges, and battery percentage status.
  - Property sections (System Info, Battery & Cells, Live Telemetry, Ride Settings).
  - Modal dialogues, QR login guides, flashing confirmation warnings, and error alerts.

### Property Catalogues (`webui/props.py` & `mobile/pwa/js/props.js`)
- Set primary property labels, categories, descriptions, and units to English across all 50+ Mi Home specification properties (`siid`/`piid`).
- Maintained dedicated `_RU` dictionary mappings to enable zero-latency language switching on the client.

---

## 3. Python Repository-Wide English Refactoring

### Core Protocol & Flashing Engine (`core/`)
- [`core/dreame_auth.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/core/dreame_auth.py):
  - Translated all transport error messages, disconnection events, ECDH key exchange logging, and session counter tracking.
- [`core/dreame_flasher.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/core/dreame_flasher.py):
  - Refactored all CLI progress indicators and flasher state events (`starting`, `uploading`, `verifying`, `committing`).
  - Standardized safety prompts and warning messages regarding `--commit`.

### Web Backend Services (`webui/`)
- [`webui/app.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/webui/app.py): All Flask API endpoints, JSON error responses, server startup banners, and route docstrings.
- [`webui/ble_worker.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/webui/ble_worker.py): Worker thread lifecycle, connection state machine logs, and BLE polling telemetry.
- [`webui/firmware_worker.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/webui/firmware_worker.py): OTA upload orchestration, staging validation, and error handling.
- [`webui/firmware_ota.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/webui/firmware_ota.py): Cloud firmware check and download utilities.
- [`webui/micloud_ltmk.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/webui/micloud_ltmk.py): Xiaomi Cloud QR login flow, session polling, and token extraction.

### Diagnostic & Flashing Tools (`tools/`)
All 15 standalone CLI tools translated:
- [`tools/mcu_uart_flash.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/tools/mcu_uart_flash.py): Wired USB-TTL flasher (handshake, sync frames, sector writes, verification).
- [`tools/dump_telemetry.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/tools/dump_telemetry.py): Comprehensive property dumper to formatted tables.
- [`tools/mcu_keygen.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/tools/mcu_keygen.py): Key derivation and generator tool.
- [`tools/fetch_firmware.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/tools/fetch_firmware.py) & [`tools/fetch_plugin.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/tools/fetch_plugin.py): Cloud artifact downloaders.
- [`tools/inspect_plugin.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/tools/inspect_plugin.py) & [`tools/unpack_rambundle.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/tools/unpack_rambundle.py): React Native bundle unpackers and deobfuscators.
- [`tools/esp32_sniff.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/tools/esp32_sniff.py), [`tools/mcu_chunk_sniff.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/tools/mcu_chunk_sniff.py), [`tools/mcu_nvmwrite_sniff.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/tools/mcu_nvmwrite_sniff.py): Hardware sniffing utilities.
- [`tools/uart_baud_scan.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/tools/uart_baud_scan.py), [`tools/uart_link_check.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/tools/uart_link_check.py), [`tools/uart_logger.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/tools/uart_logger.py), [`tools/uart_telemetry.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/tools/uart_telemetry.py): UART link and diagnostic loggers.
- [`tools/xct/token_extractor.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/tools/xct/token_extractor.py): Cloud token and LTMK extraction helper.

### Hardware & Protocol Probes (`probes/`)
All 20 probe utilities translated:
- `spec_read.py`, `spec_listen_web.py`, `spec_listen.py`, `beacon_scan.py`, `channel_probe.py`, `telemetry_listen.py`, `prop_sweep.py`, `push_capture.py`.
- `mcu_console_read.py`, `mcu_gate_after_ble_upload.py`, `mcu_gate_bank_reset.py`, `mcu_gate_clean_version.py`, `mcu_gate_repeat.py`, `mcu_live_telem.py`, `mcu_opcode_sweep.py`, `mcu_push_decode.py`, `mcu_rdinfo_probe.py`, `mcu_uart_probe.py`, `mcu_diag_probe.py`, `mcu_sniff_probe.py`.

### Emulation & Testing Framework (`emulator/` & `tests/`)
- [`emulator/scooter_device.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/emulator/scooter_device.py): Device state machine logs, packet counters, and switchFirmware gating.
- [`emulator/fake_ble.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/emulator/fake_ble.py): Synchronous in-memory adapter mimicking BleakClient.
- [`emulator/mcu_emu.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/emulator/mcu_emu.py): Unicorn ARM Thumb instruction emulator; translated all comments and behavioral models:
  - `TimerModel`, `AdcCurrentModel`, `SpeedModel`, `MotorModel`, `BatteryModel`, `RangeModel`, `GpioModel`, `PushPipelineModel`, `SpiFlashModel`, `DispatcherModel`, `ControlLoop`.
- [`emulator/ble_emu.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/emulator/ble_emu.py): RTL8762C instruction emulator comments and CLI help.
- [`emulator/run_emulator.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/emulator/run_emulator.py): All 7 test scenario outputs, banners, and assertions.
- [`tests/`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/tests/): All test docstrings and assertions updated across `test_decryptor.py`, `test_emulator_smoke.py`, `test_mcu_uart_flash.py`, `test_props.py`, `test_scooter_device.py`, and `test_spec_frame.py`.

### Research & Reverse Engineering Suite (`research/`)
- [`research/custom_mcu/ble_flash_patched.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/research/custom_mcu/ble_flash_patched.py) & [`research/custom_mcu/preflight_emu.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/research/custom_mcu/preflight_emu.py).
- All BLE analysis scripts in `research/scripts/ble/` (`analyze.py`, `analyze2.py`, `analyze3.py`, `analyze4.py`, `analyze_crypto.py`, `ble_crypto2.py`, `decryptor.py`, `fota_header_decode.py`).
- All 60 MCU diagnostic/analysis scripts in `research/scripts/mcu/`.
- [`research/scripts/gen_maps.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/research/scripts/gen_maps.py): Fully translated table generators and all 703 entries in `ANALYZED_MCU`.
- [`research/scripts/mcu/func_verify.py`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/research/scripts/mcu/func_verify.py): Fully translated all 248 test descriptions, inline comments, and assertion outputs.

---

## 4. Documentation Overhaul (English First)

1. **Root [`README.md`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/README.md)**:
   - Placed the **English** section first, followed by the **Russian** section.
   - Added an ASCII architecture diagram detailing the dual-MCU communication model:
     - Client Layer (WebUI, Mobile PWA, CLI)
     - Realtek RTL8762C BLE SoC (`FE95`, ECDH P-256, Mi Home spec)
     - Internal Serial Bus (`UART @ 19200 baud, 8N1`)
     - GigaDevice GD32F4 Controller MCU (BLDC motor, BMS, FOC, speed PID)
   - Added comprehensive feature lists, repository maps, secrets configuration, and CLI quick-start guides with explicit `--commit` safety notices.
2. **[`emulator/README.md`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/emulator/README.md)**:
   - English placed first; detailed explanation of device behavioral simulation, accurate cryptographic emulation, and model boundaries.
3. **[`mobile/README.md`](file:///c:/Users/ginca/Desktop/SCOOTER_5_PRO/mobile/README.md)**:
   - English placed first; detailed Web Bluetooth PWA design, cryptographic verification vectors (JS vs Python), and Trusted Web Activity (TWA) Android APK build instructions.

---

## 5. Xiaomi Cloud Authentication & LTMK Key Fixes

### 1. Root Cause Analysis
Users reported that the Xiaomi Cloud QR code and login link in the WebUI modal failed to work:
- **QR Rejection in Mi Home**: The QR code encodes a Xiaomi Passport login ticket (`https://eu.account.xiaomi.com/longPolling/login?ticket=...`). When scanned inside the Mi Home app, Mi Home rejects it as an unrecognized device QR code (Mi Home only recognizes device-pairing URLs, whereas Passport codes must be scanned via Xiaomi phone Settings → Xiaomi Account scanner, standard Camera / browser, or opened on desktop).
- **Socket Drop & Timeout Crashes in Long Polling**: In `tools/xct/token_extractor.py`, `login_step_3()` enforced a `timeout=10` on `self._session.get(url)`. Because Xiaomi's long-poll server holds connections for 60–70 seconds, Python timed out every 10 seconds, breaking the long-poll socket and triggering an `UnboundLocalError: local variable 'response' referenced before assignment`.
- **Missing Cookie Propagation**: In `login_step_4()`, `serviceToken` extraction directly accessed `response.cookies["serviceToken"]`, which raised a `KeyError` when set via redirect on `.sts.api.io.mi.com`, and neglected to install the cookies on `.api.io.mi.com`.
- **No Alternative Login or Manual Key Path**: Users without Xiaomi phones or with active long-poll issues had no way to log in via Username/Password or paste an existing LTMK key into the WebUI.

### 2. Backend Engine & API Fixes
- **`tools/xct/token_extractor.py`**:
  - Rewrote `QrCodeXiaomiCloudConnector.login_step_3()` with `timeout=(10, 75)` and robust polling logic that handles server keepalives, non-zero error codes, and ticket expiration without crashing.
  - Hardened `login_step_4()` to extract `serviceToken` from redirect cookies and call `install_service_token_cookies()`.
  - Upgraded `PasswordXiaomiCloudConnector` with `__init__(username, password)` and programmatic login support without CLI blocking.
- **`webui/micloud_ltmk.py`**:
  - Implemented `login_with_password(username, password)`.
  - Implemented `save_manual_ltmk(mac, hex_str)` with hex validation for 32-byte (64 hex) and 16-byte keys.
  - Implemented `logout()` to clear stored sessions.
- **`webui/app.py`**:
  - Added `POST /api/ltmk/password_login`.
  - Added `POST /api/ltmk/save_manual`.
  - Added `POST /api/ltmk/logout`.

### 3. WebUI Modal Redesign & Localization
- **`webui/static/app.js` & `style.css`**:
  - Added tabbed interface:
    1. **📱 QR & Link**: Accurate instructions for Xiaomi phone Settings, standard phone camera, and direct browser login with working live status and automatic refresh.
    2. **🔑 Account Login**: Username/Email and Password input fields with real-time authentication feedback.
    3. **✍ Manual Key**: Direct LTMK hex input with validation, instant save, and phone transfer QR generator.
  - Added device list footer actions allowing manual key entry or account switching.
- **`webui/static/i18n.js`**: Updated English and Russian strings to remove misleading Mi Home scan instructions.

### 4. Verification
- Added `tests/test_ltmk_api.py` covering status check, manual LTMK input validation (MAC format, hex encoding, key length 16B/32B), password login validation, and session logout.
- All test suites passing cleanly.

---

## 6. Bug Fixes & Technical Improvements

1. **`probes/spec_read.py` Spec Frame Counter**:
   - Fixed encryption routine `enc_app`: corrected the nonce key slice to `sk[36:40]` and prepended the 2-byte little-endian application counter header `struct.pack("<H", cnt & 0xFFFF)` required by `ScooterDevice._on_spec`.
2. **`emulator/run_emulator.py` Missing Import**:
   - Added missing `import struct` at module top-level to eliminate runtime `NameError` during frame unpacks.
3. **Syntax & Quote Repair**:
   - Corrected triple-quote and parameter closures in `emulator/mcu_emu.py` and `probes/mcu_opcode_sweep.py`.

---

## 7. Verification & Quality Gates

| Verification Gate | Result | Notes |
|---|---|---|
| **Cyrillic Character Audit** | **0 lines** | All `.py` files across the repository have 0 unintended non-English characters. (Only the intentional `_RU` dictionary in `webui/props.py` and its verification test `tests/test_props.py` are retained). |
| **Python Syntax Compilation** | **100% Passed** | `python -m py_compile` executed across every single Python file in the repository with 0 syntax errors. |
| **Ruff Linter Check** | **Passed** | `python -m ruff check core/ emulator/ probes/ tools/ webui/ tests/` completed with 0 errors. |
| **Unit & Integration Tests** | **35 / 35 Passed** | `pytest tests/` passed in full (including the end-to-end emulator smoke tests). |

