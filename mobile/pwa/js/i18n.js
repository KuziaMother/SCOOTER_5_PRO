/**
 * Scooter 5 Pro — Internationalization (i18n) module for Mobile PWA.
 */

const LANG_KEY = "scooter_lang";
const listeners = [];

export const DICT = {
  ru: {
    lang_btn: "🌐 EN",
    lang_btn_title: "Переключить на английский / Switch to English",
    pin_btn_title_on: "PIN на разблокировку включён (клик — изменить/убрать)",
    pin_btn_title_off: "PIN на разблокировку выключен (клик — включить)",
    theme_btn_title: "Светлая/тёмная тема",
    scooter_btn_title: "Мои самокаты — сохранённые профили (имя + LTMK)",
    ridemode_btn_title: "Режим езды — крупные цифры для руля",
    write_btn_readonly: "🔒 Только чтение",
    write_btn_write: "✏️ Управление разрешено",
    write_btn_title_ro: "Разрешить управление настройками (SET)",
    write_btn_title_wr: "Запретить управление настройками (только чтение)",

    // Controls
    connect_btn: "Подключиться",
    disconnect_btn: "Отключиться",
    connecting_btn: "Подключаюсь…",
    disconnecting_btn: "Отключаю…",
    stat_updated: "обновлено:",

    // Main
    events_title: "События",
    footer_text: "BLE напрямую из браузера (Web Bluetooth) · без сервера · секреты (OOB_CODE/SN) скрыты",

    // Ride Mode
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
    rm_fault_prefix: "⚠ ОШИБКА",

    // Modals & prompts
    modal_cancel: "Отмена",
    modal_ok: "Подтвердить",
    modal_done: "Готово",
    modal_close: "Закрыть",
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

    // Scooters & Keys
    scooters_title: "Мои самокаты",
    scooters_add_btn: "+ Добавить",
    scooters_no_saved: "Нет сохранённых самокатов.",
    scooters_this_device: " · это устройство",
    scooters_active_device: "активен",
    scooters_select_device: "Выбрать",
    scooters_add_title: "Добавить самокат",
    scooters_add_name: "Имя (напр. Scooter 5 Pro):",
    scooters_add_ltmk: "LTMK (64 hex-символа):",
    scooters_del_title: "Удалить профиль",
    scooters_del_confirm: "Удалить самокат ",
    ltmk_input_prompt: "LTMK этого самоката",
    ltmk_input_msg: "64 hex-символа — 32 байта ключа логина. Хранится только в этом браузере, никуда не отправляется.",
    ltmk_bad_hex: "LTMK должен быть 64 hex-символа (32 байта)",

    // QR scanner
    qrscan_title: "Сканирование QR",
    qrscan_cancel: "Отмена",

    // Statuses & Events
    status_idle: "idle",
    status_connecting: "подключение…",
    status_login: "логин…",
    status_ready: "готов",
    status_syncing: "синхронизация…",
    status_polling: "поллинг…",
    status_disconnecting: "отключение…",
    status_error: "ошибка",
    evt_connecting: "Подключение к устройству…",
    evt_connected: "GATT подключён, запуск логина…",
    evt_login_ok: "Логин успешен! Запуск синхронизации…",
    evt_disconnecting: "Отключение от устройства…",
    evt_disconnected: "Отключено",
    evt_error: "Ошибка: ",

    // Tables
    table_dur: "Длительность",
    table_dist: "Дистанция",
    table_avg: "Ср. скорость",
    table_max: "Макс.",
    no_trip_records: "нет записей о поездках",
  },

  en: {
    lang_btn: "🌐 RU",
    lang_btn_title: "Switch to Russian / Переключить на русский",
    pin_btn_title_on: "Unlock PIN enabled (click to change/disable)",
    pin_btn_title_off: "Unlock PIN disabled (click to enable)",
    theme_btn_title: "Light/dark theme",
    scooter_btn_title: "My scooters — saved profiles (name + LTMK)",
    ridemode_btn_title: "Ride mode — large HUD for handlebars",
    write_btn_readonly: "🔒 Read only",
    write_btn_write: "✏️ Control enabled",
    write_btn_title_ro: "Allow modifying settings (SET)",
    write_btn_title_wr: "Disable modifying settings (read only)",

    // Controls
    connect_btn: "Connect",
    disconnect_btn: "Disconnect",
    connecting_btn: "Connecting…",
    disconnecting_btn: "Disconnecting…",
    stat_updated: "updated:",

    // Main
    events_title: "Events",
    footer_text: "Direct BLE via Web Bluetooth in browser · serverless · secrets (OOB_CODE/SN) hidden",

    // Ride Mode
    rm_exit_label: "Exit ride mode",
    rm_trip_dist: "Trip",
    rm_trip_time: "Ride time",
    rm_speed_unit: "km/h",
    rm_battery: "Battery",
    rm_range: "Range",
    rm_chip_riding: "🛴 Riding",
    rm_chip_charging: "⚡ Charging",
    rm_chip_locked: "🔒 Locked (hold to unlock)",
    rm_chip_unlocked: "🔓 Unlocked (hold to lock)",
    rm_fault_prefix: "⚠ FAULT",

    // Modals & prompts
    modal_cancel: "Cancel",
    modal_ok: "Confirm",
    modal_done: "Done",
    modal_close: "Close",
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

    // Scooters & Keys
    scooters_title: "My Scooters",
    scooters_add_btn: "+ Add",
    scooters_no_saved: "No saved scooters.",
    scooters_this_device: " · this device",
    scooters_active_device: "active",
    scooters_select_device: "Select",
    scooters_add_title: "Add Scooter",
    scooters_add_name: "Name (e.g. Scooter 5 Pro):",
    scooters_add_ltmk: "LTMK (64 hex characters):",
    scooters_del_title: "Delete Profile",
    scooters_del_confirm: "Delete scooter ",
    ltmk_input_prompt: "Scooter LTMK Key",
    ltmk_input_msg: "64 hex characters — 32-byte login key. Stored only in this browser, never transmitted.",
    ltmk_bad_hex: "LTMK must be exactly 64 hex characters (32 bytes)",

    // QR scanner
    qrscan_title: "Scan QR Code",
    qrscan_cancel: "Cancel",

    // Statuses & Events
    status_idle: "idle",
    status_connecting: "connecting…",
    status_login: "logging in…",
    status_ready: "ready",
    status_syncing: "syncing…",
    status_polling: "polling…",
    status_disconnecting: "disconnecting…",
    status_error: "error",
    evt_connecting: "Connecting to device…",
    evt_connected: "GATT connected, initiating security-chip login…",
    evt_login_ok: "Login successful! Starting telemetry sync…",
    evt_disconnecting: "Disconnecting from device…",
    evt_disconnected: "Disconnected",
    evt_error: "Error: ",

    // Tables
    table_dur: "Duration",
    table_dist: "Distance",
    table_avg: "Avg Speed",
    table_max: "Top",
    no_trip_records: "no trip records",
  },
};

export function getLang() {
  try {
    const saved = localStorage.getItem(LANG_KEY);
    if (saved === "en" || saved === "ru") return saved;
  } catch (e) {}
  return "en";
}

export function setLang(lang) {
  if (lang !== "ru" && lang !== "en") lang = "en";
  try { localStorage.setItem(LANG_KEY, lang); } catch (e) {}
  document.documentElement.lang = lang;
  applyI18n();
  for (const fn of listeners) {
    try { fn(lang); } catch (e) { console.error("i18n listener error", e); }
  }
}

export function toggleLang() {
  setLang(getLang() === "en" ? "ru" : "en");
}

export function t(key, fallback = "") {
  const lang = getLang();
  const table = DICT[lang] || DICT.en;
  return table[key] !== undefined ? table[key] : (fallback || key);
}

export function onLanguageChange(fn) {
  if (typeof fn === "function") listeners.push(fn);
}

export function applyI18n() {
  const lang = getLang();
  const table = DICT[lang] || DICT.en;

  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const k = el.getAttribute("data-i18n");
    if (table[k] !== undefined) el.textContent = table[k];
  });

  document.querySelectorAll("[data-i18n-title]").forEach((el) => {
    const k = el.getAttribute("data-i18n-title");
    if (table[k] !== undefined) el.title = table[k];
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const k = el.getAttribute("data-i18n-placeholder");
    if (table[k] !== undefined) el.placeholder = table[k];
  });

  document.querySelectorAll("[data-i18n-aria-label]").forEach((el) => {
    const k = el.getAttribute("data-i18n-aria-label");
    if (table[k] !== undefined) el.setAttribute("aria-label", table[k]);
  });

  const langBtn = document.getElementById("lang-toggle");
  if (langBtn) {
    langBtn.textContent = table.lang_btn;
    langBtn.title = table.lang_btn_title;
  }
}

