/**
 * Каталог свойств Scooter 5 Pro и форматирование — порт webui/props.py.
 * Ключи свойств — строки "siid.piid" (как уже принято в текущем webui/static/app.js).
 */
import { decodeValue } from "./spec.js";

export const TYPES = {
  0: "BOOL", 1: "UINT8", 2: "INT8", 3: "UINT16", 4: "INT16",
  5: "UINT32", 6: "INT32", 7: "UINT64", 8: "INT64", 9: "FLOAT", 10: "STRING",
};

export const NAMES = {
  "1.1": "RIDING_MODE", "1.2": "BATTERY_LEVEL", "1.3": "REMAINING_BATTERY",
  "1.4": "VOLTAGE", "1.5": "CURRENT", "1.6": "POWER",
  "1.7": "REMAINING_MILEAGE", "1.8": "FAULT", "1.9": "CURRENT_MILEAGE",
  "2.1": "AVERAGE_SPEED", "2.2": "IS_LOCKED", "2.3": "CRUISE_IS_ON",
  "2.4": "TAIL_LIGHT_IS_ON", "2.5": "ENERGY_RECOVERY", "2.6": "TOTAL_MILEAGE",
  "2.7": "IS_RIDING", "2.8": "RIDING_TIME", "2.9": "HIGHEST_SPEED",
  "2.10": "ASR_IS_ON", "2.11": "REMAINING_MILEAGE_ALGORITHM",
  "2.12": "AUTO_LIGHT", "2.13": "TCS", "2.14": "INTELLIGENT_DOWNHILL",
  "2.15": "HILL_PARKING", "2.16": "ATMOSPHERE_LIGHT",
  "2.17": "BLUETOOTH_SEARCH_ON", "2.18": "FAKE_SHUTDOWN_STATUS",
  "3.1": "BATTERY_STATUS", "3.2": "BATTERY_TEMPERATURE",
  "3.3": "SCOOTER_TEMPERATURE", "3.4": "LOCK_WARNING", "3.5": "MILEAGE_UNIT",
  "3.6": "OOB_CODE", "3.7": "TIRE_MAINTENANCE", "3.8": "ACTIVATION_DATE",
  "3.9": "RIDING_RECORDS", "3.10": "IS_CHARGING",
  "3.11": "NUMBER_OF_CYCLES", "3.12": "SOH",
  "4.1": "PRODUCTION_DATE", "4.2": "BATTERY_SN", "4.3": "BMS_FIRMWARE_VERSION",
  "4.4": "SCOOTER_SN", "4.5": "FIRMWARE_VERSION",
  "4.6": "RESTORE_SCOOTER_SETTINGS", "4.7": "MORE_BATTERY_INFO",
  "4.8": "MORE_BATTERY_INFO_2", "4.10": "BLUETOOTH_CAR_SEARCH",
  "6.1": "LOG_1", "6.2": "LOG_2", "6.3": "LOG_3", "6.4": "LOG_4", "6.5": "LOG_5",
};

export const LABELS = {
  "1.1": "Режим", "1.2": "Заряд", "1.3": "Остаток заряда",
  "1.4": "Напряжение", "1.5": "Ток", "1.6": "Мощность",
  "1.7": "Запас хода", "1.8": "Ошибка", "1.9": "Пробег (сессия)",
  "2.1": "Средняя скорость", "2.2": "Замок", "2.3": "Круиз",
  "2.4": "Задний фонарь", "2.5": "Рекуперация", "2.6": "Общий пробег",
  "2.7": "Движение", "2.8": "Время в пути", "2.9": "Макс. скорость",
  "2.10": "ASR", "2.11": "Алгоритм запаса", "2.12": "Автосвет",
  "2.13": "TCS", "2.14": "Умный спуск", "2.15": "Уклон-парковка",
  "2.16": "Подсветка", "2.17": "BT-поиск", "2.18": "Ложное выкл.",
  "3.1": "Статус батареи", "3.2": "Темп. батареи", "3.3": "Темп. самоката",
  "3.4": "Сигнал замка", "3.5": "Единицы", "3.6": "OOB",
  "3.7": "ТО шин", "3.8": "Активация", "3.9": "Записи поездок",
  "3.10": "Зарядка", "3.11": "Циклы заряда", "3.12": "Здоровье батареи",
  "4.1": "Дата производства", "4.2": "SN батареи", "4.3": "Прошивка BMS",
  "4.4": "SN самоката", "4.5": "Прошивка", "4.6": "Сброс настроек",
  "4.7": "Батарея (детально)", "4.8": "Батарея (экстрим)", "4.10": "Поиск самоката",
  "6.1": "Журнал 1", "6.2": "Журнал 2", "6.3": "Журнал 3",
  "6.4": "Журнал 4", "6.5": "Журнал 5",
};

export const UNITS = {
  VOLTAGE: [0.01, "В"], CURRENT: [1.0, "А"], POWER: [1.0, "Вт"],
  TOTAL_MILEAGE: [0.01, "км"], CURRENT_MILEAGE: [0.01, "км"],
  REMAINING_MILEAGE: [0.01, "км"],
  BATTERY_LEVEL: [1.0, "%"], SOH: [1.0, "%"],
  AVERAGE_SPEED: [0.01, "км/ч"], HIGHEST_SPEED: [0.01, "км/ч"],
  BATTERY_TEMPERATURE: [1.0, "°C"], SCOOTER_TEMPERATURE: [1.0, "°C"],
  RIDING_TIME: [1.0, "с"],
};

export const SENSITIVE = new Set(["3.6", "4.2", "4.4"]);
export const DANGEROUS_EXCLUDED = new Set(["4.6"]);

// Значения/типы сверены разбором setPropertys в оригинальном плагине (не угаданы).
export const WRITABLE = {
  "2.2": { type: 0, confirm: "Заблокировать/разблокировать самокат?" },
  "2.3": { type: 0 },
  "2.4": { type: 0 },
  "2.12": { type: 0 },
  "2.13": { type: 0 },
  "2.14": { type: 0 },
  "2.15": { type: 0 },
  "2.17": { type: 0 },
  "2.5": { type: 1, values: [30, 60, 90] },
  "2.16": { type: 1, values: [0, 1, 2] },
  "3.5": { type: 1, values: [1, 0] },
};

export function isWritable(key) {
  return key in WRITABLE && !DANGEROUS_EXCLUDED.has(key) && !SENSITIVE.has(key);
}

export const BOOL_PROPS = new Set([
  "2.2", "2.3", "2.4", "2.10", "2.12", "2.13", "2.14", "2.15", "2.17", "2.18", "3.10", "4.10",
]);

export const FAULT_LABELS = {
  0: "норма", 10: "ошибка связи приборной панели", 11: "перегрузка контроллера",
  12: "ошибка контроллера", 14: "ошибка кабеля акселератора", 15: "ошибка кабеля ручки тормоза",
  18: "ошибка двигателя", 21: "ошибка связи аккумулятора", 24: "избыточное давление в аккумуляторе",
  28: "ошибка контроллера", 29: "ошибка контроллера", 39: "ошибка аккумулятора",
  40: "ошибка контроллера", 45: "перегрев контроллера", 50: "ошибка из-за температуры аккумулятора",
  52: "ошибка аккумулятора",
};

export const ENUM_LABELS = {
  "1.1": { 11: "P — walk", 2: "D — standard", 3: "S — sport", 4: "X — performance" },
  "1.8": FAULT_LABELS,
  "2.5": { 30: "weak", 60: "middle", 90: "strong" },
  "2.7": { 0: "не едет", 1: "переход", 2: "едет" },
  "2.16": { 0: "выкл", 1: "вкл", 2: "активна" },
  "3.1": { 1: "OK" },
  "3.5": { 1: "KM", 0: "MI" },
};

export const LOG_SET = [1, 2, 3, 4, 5].map((i) => [6, i]);

export const DYNAMIC_SET = [
  [3, 5],
  [1, 1], [2, 7], [2, 9], [2, 1], [1, 9], [2, 8],
  [1, 2], [3, 10], [1, 4], [1, 5], [1, 6], [3, 2], [1, 8],
];

export const STATIC_SET = [
  [1, 3], [1, 7], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6],
  [2, 10], [2, 12], [2, 13], [2, 14], [2, 15], [2, 16], [2, 17], [2, 18],
  [3, 1], [3, 3], [3, 4], [3, 7], [3, 8], [3, 11], [3, 12],
  [4, 1], [4, 3], [4, 5], [4, 7], [4, 8], [4, 10],
];

function dedupePairs(pairs) {
  const seen = new Set();
  const out = [];
  for (const [s, p] of pairs) {
    const k = `${s}.${p}`;
    if (!seen.has(k)) { seen.add(k); out.push([s, p]); }
  }
  return out;
}
export const FULL_SAFE_SET = dedupePairs([...DYNAMIC_SET, ...STATIC_SET, ...LOG_SET]);

export const GROUPS = [
  { id: "ride", title: "Езда", props: [[1, 1], [2, 7], [2, 9], [2, 1], [2, 8], [1, 9], [1, 7], [2, 6]] },
  { id: "battery", title: "Батарея и электрика", props: [[1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 8], [3, 1], [3, 2], [3, 10], [3, 11], [3, 12]] },
  { id: "functions", title: "Функции и настройки", props: [[2, 2], [2, 3], [2, 4], [2, 5], [2, 10], [2, 12], [2, 13], [2, 14], [2, 15], [2, 16], [2, 17], [2, 18], [3, 4], [3, 5], [4, 10]] },
  { id: "identity", title: "Устройство", props: [[4, 5], [4, 3], [4, 1], [3, 8], [3, 3], [4, 7], [4, 8]] },
  { id: "logs", title: "Журнал поездок", props: LOG_SET },
];

export const PROP_GROUPS = {};
for (const g of GROUPS) {
  for (const [s, p] of g.props) {
    const k = `${s}.${p}`;
    (PROP_GROUPS[k] = PROP_GROUPS[k] || []).push(g.id);
  }
}

export function isSafe(key) {
  return key in NAMES && !SENSITIVE.has(key) && !DANGEROUS_EXCLUDED.has(key);
}

export function unitMultiplier(mileageUnitValue) {
  const iv = Number(mileageUnitValue);
  if (!Number.isFinite(iv)) return 1.0;
  return iv !== 1 ? 0.6213712 : 1.0;
}

function isNum(v) {
  return typeof v === "number" && Number.isFinite(v);
}

/** Грубый аналог Python `{v:g}` — компактная запись без хвостовых нулей. */
function numG(v) {
  if (Number.isInteger(v)) return String(v);
  let s = v.toPrecision(6);
  if (s.includes(".")) s = s.replace(/0+$/, "").replace(/\.$/, "");
  return s;
}

function unitText(name, v, unitMult = 1.0) {
  if (!(name in UNITS) || !isNum(v)) return null;
  const [mul, unit] = UNITS[name];
  const base = v * mul;
  if (unit === "км" && unitMult !== 1.0) return `${numG(base * unitMult)} mi`;
  if (unit === "км/ч" && unitMult !== 1.0) return `${numG(base * unitMult)} mph`;
  if (mul !== 1.0) return `${numG(base)} ${unit}`;
  return `${numG(v)} ${unit}`;
}

function fmtRidingTime(v) {
  if (!isNum(v) || v < 0) return String(v);
  const s = Math.trunc(v);
  const h = Math.floor(s / 3600);
  const rem = s % 3600;
  const m = Math.floor(rem / 60);
  const sec = rem % 60;
  if (h) return `${h}ч ${String(m).padStart(2, "0")}м ${String(sec).padStart(2, "0")}с`;
  if (m) return `${m}м ${String(sec).padStart(2, "0")}с`;
  return `${sec} с`;
}

function fmtTire(v) {
  const s = String(v).trim();
  if (s.length >= 7 && /^\d+$/.test(s)) {
    const state = s[0] === "2" ? "выкл" : "вкл";
    const interval = parseInt(s.slice(1, 4), 10);
    const remaining = parseInt(s.slice(4, 7), 10);
    return `напоминание ${state}, интервал ${interval} дн., остаток ${remaining} дн.`;
  }
  return s || "пусто";
}

function fmtMoreBattery(v) {
  const s = String(v).trim().toLowerCase();
  if (s.length >= 14 && /^[0-9a-f]+$/.test(s)) {
    const energy = parseInt(s.slice(0, 6), 16) / 1000.0;
    const capacity = parseInt(s.slice(6, 10), 16);
    const deep = parseInt(s.slice(10, 14), 16);
    return `отдача ${energy.toFixed(2)} кВт·ч, ёмкость ${numG(capacity)} А·ч, глубоких разрядов ${deep}`;
  }
  return s || "пусто";
}

function fmtMoreBattery2(v) {
  const s = String(v).trim().toLowerCase();
  if (s.length >= 16 && /^[0-9a-f]+$/.test(s)) {
    const y = parseInt(s.slice(0, 2), 16);
    const mo = parseInt(s.slice(2, 4), 16);
    const d = parseInt(s.slice(4, 6), 16);
    const h = parseInt(s.slice(6, 8), 16);
    const mi = parseInt(s.slice(8, 10), 16);
    const se = parseInt(s.slice(10, 12), 16);
    const charge = parseInt(s.slice(12, 16), 16);
    if (y === 0 && mo === 0 && d === 0) return `экстрем. темп.: нет данных, зарядка ${charge} с`;
    const p2 = (n) => String(n).padStart(2, "0");
    const p4 = (n) => String(n).padStart(4, "0");
    return `экстрем. темп.: ${p4(y)}-${p2(mo)}-${p2(d)} ${p2(h)}:${p2(mi)}:${p2(se)}, зарядка ${charge} с`;
  }
  return s || "пусто";
}

export function rideRecords(v, unitMult = 1.0) {
  const s = String(v).trim();
  const out = [];
  for (let i = 0; i + 16 <= s.length; i += 16) {
    const chunk = s.slice(i, i + 16);
    const dur = parseInt(chunk.slice(0, 4), 10) / 10.0;
    const dist = (parseInt(chunk.slice(4, 8), 10) / 10.0) * unitMult;
    const avg = (parseInt(chunk.slice(8, 12), 10) / 10.0) * unitMult;
    const top = (parseInt(chunk.slice(12, 16), 10) / 10.0) * unitMult;
    if ([dur, dist, avg, top].some(Number.isNaN)) continue;
    if (dur === 0 && dist === 0 && avg === 0 && top === 0) continue;
    const dunit = unitMult !== 1.0 ? "mi" : "км";
    const sunit = unitMult !== 1.0 ? "mph" : "км/ч";
    let dtxt;
    if (dur >= 60) {
      const h = Math.floor(Math.round(dur) / 60);
      const rem = Math.round(dur) % 60;
      dtxt = `${h}ч ${String(rem).padStart(2, "0")}м`;
    } else {
      dtxt = `${Math.trunc(dur)} мин`;
    }
    out.push({
      dur: dtxt, dist: `${dist.toFixed(1)} ${dunit}`,
      avg: `${avg.toFixed(1)} ${sunit}`, top: `${top.toFixed(1)} ${sunit}`,
    });
  }
  return out;
}

/** Безопасный человекочитаемый вид одного свойства (секреты маскируются). */
export function formatProperty(siid, piid, tcode, val, unitMult = 1.0) {
  const key = `${siid}.${piid}`;
  const name = NAMES[key] || "?";
  const base = {
    key, siid, piid, name,
    type: TYPES[tcode] || `type${tcode}`, secret: false,
    raw: null, text: "пусто", groups: PROP_GROUPS[key] || [],
  };

  if (SENSITIVE.has(key)) {
    base.secret = true;
    base.text = val && val.length ? `скрыто (${val.length} байт)` : "скрыто";
    return base;
  }

  if (!val || !val.length) return base;

  const v = decodeValue(tcode, val);
  base.raw = Array.from(val.slice(0, 64)).map((b) => b.toString(16).padStart(2, "0")).join("");
  if (isNum(v)) {
    if (name in UNITS) {
      const [mul, unit] = UNITS[name];
      base.num = v * mul * (unit === "км" || unit === "км/ч" ? unitMult : 1.0);
    } else {
      base.num = v;
    }
  }

  let text;
  if (key === "3.7") text = fmtTire(v);
  else if (key === "4.7") text = fmtMoreBattery(v);
  else if (key === "4.8") text = fmtMoreBattery2(v);
  else if (siid === 6 && piid >= 1 && piid <= 5) {
    const recs = rideRecords(v, unitMult);
    base.rides = recs;
    text = recs.length ? `${recs.length} поездк(и)` : "пусто";
  } else if (key === "2.8") text = fmtRidingTime(v);
  else if (key in ENUM_LABELS) {
    const label = ENUM_LABELS[key][v];
    text = label !== undefined ? `${label} (raw ${v})` : String(v);
  } else if (BOOL_PROPS.has(key)) {
    const iv = Number(v);
    text = Number.isFinite(iv) ? (iv ? "вкл" : "выкл") : String(v);
  } else {
    const ut = unitText(name, v, unitMult);
    text = ut !== null ? ut : (isNum(v) ? numG(v) : String(v));
  }

  base.text = text;
  return base;
}
