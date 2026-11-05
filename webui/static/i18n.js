/* Scooter 5 Pro — Internationalization (i18n) module for Web UI */
(function (global) {
  const LANG_KEY = "scooter_lang";
  const listeners = [];

  const DICT = {
    ru: {
      lang_btn: "🌐 EN",
      lang_btn_title: "Переключить на английский / Switch to English",
      pin_btn_title_on: "PIN на разблокировку включён (клик — изменить/убрать)",
      pin_btn_title_off: "PIN на разблокировку выключен (клик — включить)",
      theme_btn_title: "Светлая/тёмная тема",
      scooter_btn_title: "Мои самокаты — выбор устройства для подключения",
      ridemode_btn_title: "Режим езды — крупные цифры для руля",
      service_link_title: "Сервис — прошивка",
      service_link_text: "🔧 Сервис",
      back_link_text: "← Панель",
      write_btn_readonly: "🔒 Только чтение",
      write_btn_write: "✏️ Управление",
      write_btn_title_ro: "Разрешить управление настройками (SET)",
      write_btn_title_wr: "Запретить управление настройками (только чтение)",

      // Controls
      mode_label: "Режим",
      interval_label: "Интервал, с",
      static_interval_label: "Static-интервал, с",
      start_btn: "Старт",
      stop_btn: "Стоп",
      stopping_btn: "Останавливаю…",
      stat_mode: "режим:",
      stat_pushes: "пуши:",
      stat_rx: "rx:",
      stat_updated: "обновлено:",

      // Sections
      history_title: "История (раунды)",
      events_title: "События",
      footer_text: "Только чтение · bind 127.0.0.1 · секреты (OOB_CODE/SN) скрыты",

      // Ride mode
      rm_exit_label: "Выйти из режима езды",
      rm_trip_dist: "Пробег",
      rm_trip_time: "Время в пути",
      rm_speed_unit: "км/ч",
      rm_battery: "Заряд",
      rm_range: "Запас хода",
      rm_chip_riding: "🛴 Движение",
      rm_chip_charging: "⚡ Зарядка",
      rm_chip_locked: "🔒 Заблокирован (удержите для разблокировки)",
      rm_chip_unlocked: "🔓 Разблокирован (удержите для блокировки)",

      // Modals
      modal_cancel: "Отмена",
      modal_ok: "Подтвердить",
      modal_done: "Готово",
      modal_close: "Закрыть",
      modal_understood: "Понятно",
      modal_next: "Далее",
      modal_save: "Сохранить",
      modal_delete: "Удалить",
      modal_pin_title: "PIN для разблокировки",
      modal_pin_msg: "Введите PIN, чтобы разблокировать самокат.",
      modal_pin_unlock: "Разблокировать",
      modal_pin_wrong: "Неверный PIN.",
      modal_pin_change_title: "Изменить PIN",
      modal_pin_change_msg: "Введите текущий PIN, чтобы изменить или отключить защиту.",
      modal_pin_new_title: "Новый PIN",
      modal_pin_set_title: "Установить PIN на разблокировку",
      modal_pin_hint_has: "Минимум 4 цифры. Оставьте пустым, чтобы отключить защиту.",
      modal_pin_hint_none: "Минимум 4 цифры. Потребуется при каждой разблокировке.",

      // Scooters Modal
      scooters_title: "Мои самокаты",
      scooters_scan_btn: "🔍 Сканировать",
      scooters_scanning: "🔍 Сканирую (5с)…",
      scooters_add_btn: "+ Вручную",
      scooters_no_saved: "Нет сохранённых самокатов.",
      scooters_found_count: "Найдено устройств: ",
      scooters_no_devices: "Устройств поблизости не найдено (проверьте BLE и включён ли самокат).",
      scooters_this_device: " · это устройство",
      scooters_active_device: "активен",
      scooters_select_device: "Выбрать",
      scooters_add_title: "Добавить самокат",
      scooters_add_name: "Имя (напр. Scooter 5 Pro):",
      scooters_add_mac: "MAC-адрес (напр. 2C:19:5C:DE:DE:88):",
      scooters_bad_mac: "Некорректный MAC-адрес (нужен формат XX:XX:XX:XX:XX:XX)",
      scooters_del_title: "Удалить профиль",
      scooters_del_confirm: "Удалить самокат ",

      // LTMK Modal
      ltmk_title: "Получить LTMK",
      ltmk_qr_btn: "🔑 Показать QR для входа",
      ltmk_qr_wait: "Ожидаю подтверждения входа через Mi Home…",
      ltmk_qr_expired: "Срок действия QR-кода истёк. Нажмите кнопку, чтобы получить новый.",
      ltmk_qr_success: "Вход выполнен успешно!",
      ltmk_extract_btn: "⚡ Извлечь LTMK из облака",
      ltmk_extracted_success: "LTMK успешно получен и сохранён!",

      // Service page
      service_title: "Сервис — прошивка",
      fw_session_warn: "⚠ На главной странице активна BLE-сессия (поллинг) — остановите её, прежде чем прошивать: одно BLE-соединение на процесс.",
      fw_session_stop: "Остановить поллинг",
      fw_session_stopping: "Останавливаю…",
      fw_current_title: "Текущая прошивка",
      fw_target_scooter: "Целевой самокат:",
      fw_target_change: "(сменить — «Мои самокаты» на главной странице)",
      fw_target_none: "не выбран",
      fw_check_title: "Проверить обновление",
      fw_check_btn: "Проверить в Mi Cloud",
      fw_checking: "Проверяю…",
      fw_downloaded_title: "Скачанные образы",
      fw_flashing_title: "Заливка",
      fw_history_title: "История заливок/переключений",
      fw_history_hint: "Пишется в файл (logs/flash_log.jsonl) — переживает перезапуск сервера.",
      fw_btn_download: "Скачать",
      fw_btn_downloading: "Скачиваю…",
      fw_btn_flash: "Прошить",
      fw_btn_switch: "Переключить (switch)",
      fw_ready: "готово",
      fw_no_cloud_entries: "Облако не вернуло образов для этого устройства.",
      fw_no_local_files: "Нет скачанных образов в firmware_ota/",
      fw_login_needed: "Нужен вход в Mi Cloud",
      fw_check_failed: "Не удалось проверить",
      fw_select_scooter_first: "Сначала выберите самокат на главной странице («Мои самокаты»).",

      // Props tables / values
      rounds_count: "раунд(ов)",
      comm_ok: "связь OK",
      empty_value: "пусто",
      hidden_value: "скрыто",
      trip_history_title: "История поездок",
      no_trip_records: "нет записей о поездках",
      table_dur: "Длительность",
      table_dist: "Дистанция",
      table_avg: "Ср. скорость",
      table_max: "Макс.",
    },

    en: {
      lang_btn: "🌐 RU",
      lang_btn_title: "Switch to Russian / Переключить на русский",
      pin_btn_title_on: "Unlock PIN enabled (click to change/disable)",
      pin_btn_title_off: "Unlock PIN disabled (click to enable)",
      theme_btn_title: "Light/dark theme",
      scooter_btn_title: "My scooters — select device to connect",
      ridemode_btn_title: "Ride mode — large HUD for handlebars",
      service_link_title: "Service — Firmware Flashing",
      service_link_text: "🔧 Service",
      back_link_text: "← Dashboard",
      write_btn_readonly: "🔒 Read only",
      write_btn_write: "✏️ Control enabled",
      write_btn_title_ro: "Allow modifying settings (SET)",
      write_btn_title_wr: "Disable modifying settings (read only)",

      // Controls
      mode_label: "Mode",
      interval_label: "Interval, s",
      static_interval_label: "Static interval, s",
      start_btn: "Start",
      stop_btn: "Stop",
      stopping_btn: "Stopping…",
      stat_mode: "mode:",
      stat_pushes: "pushes:",
      stat_rx: "rx:",
      stat_updated: "updated:",

      // Sections
      history_title: "History (rounds)",
      events_title: "Events",
      footer_text: "Read only · bind 127.0.0.1 · secrets (OOB_CODE/SN) hidden",

      // Ride mode
      rm_exit_label: "Exit ride mode",
      rm_trip_dist: "Trip",
      rm_trip_time: "Ride time",
      rm_speed_unit: "km/h",
      rm_battery: "Battery",
      rm_range: "Range",
      rm_chip_riding: "🛴 Moving",
      rm_chip_charging: "⚡ Charging",
      rm_chip_locked: "🔒 Locked (hold to unlock)",
      rm_chip_unlocked: "🔓 Unlocked (hold to lock)",

      // Modals
      modal_cancel: "Cancel",
      modal_ok: "Confirm",
      modal_done: "Done",
      modal_close: "Close",
      modal_understood: "Understood",
      modal_next: "Next",
      modal_save: "Save",
      modal_delete: "Delete",
      modal_pin_title: "Unlock PIN",
      modal_pin_msg: "Enter PIN to unlock the scooter.",
      modal_pin_unlock: "Unlock",
      modal_pin_wrong: "Incorrect PIN.",
      modal_pin_change_title: "Change PIN",
      modal_pin_change_msg: "Enter current PIN to change or disable protection.",
      modal_pin_new_title: "New PIN",
      modal_pin_set_title: "Set Unlock PIN",
      modal_pin_hint_has: "Minimum 4 digits. Leave empty to disable protection.",
      modal_pin_hint_none: "Minimum 4 digits. Required for every unlock.",

      // Scooters Modal
      scooters_title: "My Scooters",
      scooters_scan_btn: "🔍 Scan",
      scooters_scanning: "🔍 Scanning (5s)…",
      scooters_add_btn: "+ Manual",
      scooters_no_saved: "No saved scooters.",
      scooters_found_count: "Found devices: ",
      scooters_no_devices: "No devices found nearby (verify BLE is on and scooter is awake).",
      scooters_this_device: " · this device",
      scooters_active_device: "active",
      scooters_select_device: "Select",
      scooters_add_title: "Add Scooter",
      scooters_add_name: "Name (e.g. Scooter 5 Pro):",
      scooters_add_mac: "MAC Address (e.g. 2C:19:5C:DE:DE:88):",
      scooters_bad_mac: "Invalid MAC address (must be format XX:XX:XX:XX:XX:XX)",
      scooters_del_title: "Delete Profile",
      scooters_del_confirm: "Delete scooter ",

      // LTMK Modal
      ltmk_title: "Retrieve LTMK",
      ltmk_qr_btn: "🔑 Show QR for Login",
      ltmk_qr_wait: "Waiting for login confirmation in Mi Home…",
      ltmk_qr_expired: "QR code expired. Click the button to generate a new one.",
      ltmk_qr_success: "Login successful!",
      ltmk_extract_btn: "⚡ Extract LTMK from Cloud",
      ltmk_extracted_success: "LTMK successfully retrieved and saved!",

      // Service page
      service_title: "Service — Firmware",
      fw_session_warn: "⚠ Active BLE session (polling) on main page — stop it before flashing: one BLE connection per process.",
      fw_session_stop: "Stop polling",
      fw_session_stopping: "Stopping…",
      fw_current_title: "Installed Firmware",
      fw_target_scooter: "Target scooter:",
      fw_target_change: "(change via «My scooters» on main page)",
      fw_target_none: "not selected",
      fw_check_title: "Check for Updates",
      fw_check_btn: "Check in Mi Cloud",
      fw_checking: "Checking…",
      fw_downloaded_title: "Downloaded Images",
      fw_flashing_title: "Flashing",
      fw_history_title: "Flashing & Switch History",
      fw_history_hint: "Written to file (logs/flash_log.jsonl) — persists across server restarts.",
      fw_btn_download: "Download",
      fw_btn_downloading: "Downloading…",
      fw_btn_flash: "Flash",
      fw_btn_switch: "Switch Firmware",
      fw_ready: "ready",
      fw_no_cloud_entries: "No cloud firmware images returned for this device.",
      fw_no_local_files: "No downloaded images found in firmware_ota/",
      fw_login_needed: "Mi Cloud Login Required",
      fw_check_failed: "Update Check Failed",
      fw_select_scooter_first: "Please select a scooter on the main page first («My scooters»).",

      // Props tables / values
      rounds_count: "round(s)",
      comm_ok: "comm OK",
      empty_value: "empty",
      hidden_value: "hidden",
      trip_history_title: "Trip History",
      no_trip_records: "no trip records",
      table_dur: "Duration",
      table_dist: "Distance",
      table_avg: "Avg Speed",
      table_max: "Top",
    },
  };

  function getLang() {
    try {
      const saved = localStorage.getItem(LANG_KEY);
      if (saved === "en" || saved === "ru") return saved;
    } catch (e) {}
    return "en";
  }

  function setLang(lang) {
    if (lang !== "ru" && lang !== "en") lang = "en";
    try { localStorage.setItem(LANG_KEY, lang); } catch (e) {}
    document.documentElement.lang = lang;
    applyI18n();
    for (const fn of listeners) {
      try { fn(lang); } catch (e) { console.error("i18n listener error", e); }
    }
  }

  function toggleLang() {
    setLang(getLang() === "en" ? "ru" : "en");
  }

  function t(key, fallback = "") {
    const lang = getLang();
    const table = DICT[lang] || DICT.en;
    return table[key] !== undefined ? table[key] : (fallback || key);
  }

  function onLanguageChange(fn) {
    if (typeof fn === "function") listeners.push(fn);
  }

  function applyI18n() {
    const lang = getLang();
    const table = DICT[lang] || DICT.en;

    // Apply to elements with data-i18n
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const k = el.getAttribute("data-i18n");
      if (table[k] !== undefined) el.textContent = table[k];
    });

    // Apply to elements with data-i18n-title
    document.querySelectorAll("[data-i18n-title]").forEach((el) => {
      const k = el.getAttribute("data-i18n-title");
      if (table[k] !== undefined) el.title = table[k];
    });

    // Apply to elements with data-i18n-placeholder
    document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
      const k = el.getAttribute("data-i18n-placeholder");
      if (table[k] !== undefined) el.placeholder = table[k];
    });

    // Apply to elements with data-i18n-aria-label
    document.querySelectorAll("[data-i18n-aria-label]").forEach((el) => {
      const k = el.getAttribute("data-i18n-aria-label");
      if (table[k] !== undefined) el.setAttribute("aria-label", table[k]);
    });

    // Update lang button itself
    const langBtn = document.getElementById("lang-toggle");
    if (langBtn) {
      langBtn.textContent = table.lang_btn;
      langBtn.title = table.lang_btn_title;
    }
  }

  // Setup toggle click listener once DOM is ready
  document.addEventListener("DOMContentLoaded", () => {
    document.documentElement.lang = getLang();
    const langBtn = document.getElementById("lang-toggle");
    if (langBtn) {
      langBtn.addEventListener("click", toggleLang);
    }
    applyI18n();
  });

  global.I18N = {
    getLang,
    setLang,
    toggleLang,
    t,
    onLanguageChange,
    applyI18n,
    DICT,
  };
})(window);

