/**
 * Scooter 5 Pro — автономный PWA-клиент (Web Bluetooth, без сервера).
 * Функции рендера (renderHero/buildGroups/updateProps/renderRideMode/...)
 * почти дословно перенесены из webui/static/app.js — там же весь дизайн
 * (hero, список свойств, ride mode) уже проверен и обкатан. Отличие только
 * в источнике данных: не fetch('/api/state'), а локальная BLE-сессия.
 */
import { Transport } from "./transport.js";
import { login } from "./login.js";
import { specGet, specSet, decodeValue } from "./spec.js";
import * as props from "./props.js";
import { hexToBytes } from "./bin.js";
import { getLang, t, onLanguageChange, applyI18n, toggleLang } from "./i18n.js";

const $ = (id) => document.getElementById(id);

// ---- локальное состояние (аналог WebState в webui/app.py) ----
const appState = {
  status: "idle", message: "", properties: {}, events: [],
  groups: props.GROUPS, groups_en: props.GROUPS_EN,
  names: props.NAMES, labels: props.LABELS, labels_en: props.LABELS_EN,
  write_enabled: false,
  writable: Object.keys(props.WRITABLE),
  writable_confirm: Object.fromEntries(
    Object.entries(props.WRITABLE).filter(([, v]) => v.confirm).map(([k, v]) => [k, v.confirm])
  ),
  writable_confirm_en: Object.fromEntries(
    Object.entries(props.WRITABLE).filter(([, v]) => v.confirm).map(([k, v]) => [k, props.WRITABLE_CONFIRM_EN[v.confirm] || v.confirm])
  ),
  writable_values: Object.fromEntries(
    Object.entries(props.WRITABLE).filter(([, v]) => v.values)
      .map(([k, v]) => [k, v.values.map((val) => [val, (props.ENUM_LABELS[k] || {})[val] ?? String(val)])])
  ),
  writable_values_en: Object.fromEntries(
    Object.entries(props.WRITABLE).filter(([, v]) => v.values)
      .map(([k, v]) => [k, v.values.map((val) => [val, (props.ENUM_LABELS_EN[k] || {})[val] ?? String(val)])])
  ),
  last_update: "—",
};

let eventSeq = 0;
function addEvent(message) {
  eventSeq += 1;
  appState.events.push({ id: eventSeq, ts: new Date().toLocaleTimeString("ru-RU"), message: String(message) });
  if (appState.events.length > 300) appState.events.splice(0, appState.events.length - 300);
}
function setStatus(status, message = "") {
  appState.status = status;
  appState.message = message;
  appState.last_update = new Date().toLocaleTimeString("ru-RU");
}

// ---- модалка подтверждения (замена нативного confirm()/prompt() для обычного
// режима; в ride mode вместо неё жест "удержать", см. ниже — модалка там не
// вписывается). С input:true работает как prompt(): резолвится строкой или
// null при отмене; без input — как confirm(): true/false. ----
function showModal(title, message, opts = {}) {
  const { danger = false, okText = "Confirm", input = false, inputPlaceholder = "", inputType = "text", inputValue = "" } = opts;
  return new Promise((resolve) => {
    const overlay = $("modal-overlay");
    const okBtn = $("modal-ok");
    const cancelBtn = $("modal-cancel");
    const inputEl = $("modal-input");
    $("modal-title").textContent = title;
    $("modal-msg").textContent = message;
    okBtn.textContent = okText;
    okBtn.classList.toggle("danger", danger);
    inputEl.hidden = !input;
    if (input) {
      inputEl.type = inputType;
      inputEl.placeholder = inputPlaceholder;
      inputEl.value = inputValue;
    }
    overlay.hidden = false;
    if (input) setTimeout(() => inputEl.focus(), 30);

    function cleanup(result) {
      overlay.hidden = true;
      okBtn.removeEventListener("click", onOk);
      cancelBtn.removeEventListener("click", onCancel);
      overlay.removeEventListener("click", onOverlay);
      document.removeEventListener("keydown", onKey);
      resolve(result);
    }
    function onOk() { cleanup(input ? (inputEl.value || null) : true); }
    function onCancel() { cleanup(input ? null : false); }
    function onOverlay(e) { if (e.target === overlay) onCancel(); }
    function onKey(e) {
      if (e.key === "Escape") onCancel();
      if (e.key === "Enter") onOk();
    }
    okBtn.addEventListener("click", onOk);
    cancelBtn.addEventListener("click", onCancel);
    overlay.addEventListener("click", onOverlay);
    document.addEventListener("keydown", onKey);
  });
}

// ---- PIN на разблокировку (app-level: защищает не BLE-протокол — тот уже
// защищён ECDH/LTMK-логином, — а сценарий "телефон разблокирован и лежит в
// чужих руках". Поэтому гейтит только РАЗБЛОКИРОВКУ (next=0 для IS_LOCKED),
// блокировка остаётся мгновенной без лишнего трения. ----
const PIN_KEY = "scooter_pin_hash";
async function sha256Hex(s) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
function hasPin() { return Boolean(localStorage.getItem(PIN_KEY)); }
function updatePinButton() {
  const btn = $("pin-toggle");
  btn.classList.toggle("on", hasPin());
  const isEn = getLang() === "en";
  btn.title = hasPin()
    ? (isEn ? "Unlock PIN enabled (click to change/disable)" : "PIN на разблокировку включён (клик — изменить/убрать)")
    : (isEn ? "Unlock PIN disabled (click to enable)" : "PIN на разблокировку выключен (клик — включить)");
}

async function verifyPin() {
  if (!hasPin()) return true;
  const entered = await showModal(
    "Unlock PIN", "Enter PIN to unlock the scooter.",
    { input: true, inputPlaceholder: "PIN", inputType: "password", okText: "Unlock" });
  if (!entered) return false;
  if ((await sha256Hex(entered)) !== localStorage.getItem(PIN_KEY)) {
    alert("Incorrect PIN.");
    return false;
  }
  return true;
}

async function managePin() {
  if (hasPin()) {
    const cur = await showModal(
      "Change PIN", "Enter current PIN to change or disable protection.",
      { input: true, inputPlaceholder: "current PIN", inputType: "password", okText: "Next" });
    if (!cur) return;
    if ((await sha256Hex(cur)) !== localStorage.getItem(PIN_KEY)) { alert("Неверный PIN."); return; }
  }
  const next = await showModal(
    hasPin() ? "New PIN" : "Set Unlock PIN",
    `Minimum 4 digits. ${hasPin() ? "Leave empty to disable protection." : "Required for every unlock."}`,
    { input: true, inputPlaceholder: "new PIN", inputType: "password", okText: "Next" });
  if (next === null) return;
  if (!next) {
    if (hasPin()) {
      localStorage.removeItem(PIN_KEY);
      updatePinButton();
    }
    return;
  }
  if (!/^\d{4,}$/.test(next)) { alert("PIN must be a number with at least 4 digits."); return; }
  const repeat = await showModal(
    "Confirm PIN", "Re-enter the same PIN to confirm.",
    { input: true, inputPlaceholder: "repeat PIN", inputType: "password", okText: "Save" });
  if (repeat !== next) { alert("PIN does not match — try again."); return; }
  localStorage.setItem(PIN_KEY, await sha256Hex(next));
  updatePinButton();
}

function esc(s) {
  return String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}
function shortName(key, state) {
  const isEn = getLang() === "en";
  if (isEn && (state.labels_en && state.labels_en[key])) return state.labels_en[key];
  return (state.labels && state.labels[key]) || (state.names && state.names[key]) || key;
}
function prop(state, key) { return (state.properties || {})[key] || null; }
function pnum(state, key) { const p = prop(state, key); return p && typeof p.num === "number" ? p.num : null; }
function batteryColor(pct) {
  if (pct == null) return "var(--text-faint)";
  if (pct <= 15) return "var(--bad)";
  if (pct <= 35) return "var(--warn)";
  return "var(--ok)";
}

// ---- hero-сводка ----
function renderHero(state) {
  const host = $("hero");
  const p = state.properties || {};
  if (!Object.keys(p).length) { host.hidden = true; return; }
  host.hidden = false;

  const bat = pnum(state, "1.2"), soh = pnum(state, "3.12"), speed = pnum(state, "2.1");
  const range = pnum(state, "1.7"), power = pnum(state, "1.6"), volt = pnum(state, "1.4"), curr = pnum(state, "1.5");
  const modeP = prop(state, "1.1");
  const fault = pnum(state, "1.8"), locked = pnum(state, "2.2"), riding = pnum(state, "2.7"), charging = pnum(state, "3.10");

  const R = 52, C = 2 * Math.PI * R;
  const pct = bat == null ? 0 : Math.max(0, Math.min(100, bat));
  const dash = (pct / 100) * C;
  const col = batteryColor(bat);

  const isEn = getLang() === "en";
  const tiles = [
    [isEn ? "Avg speed" : "Ср. скорость", speed == null ? "—" : `${speed.toFixed(1)}`, isEn ? "km/h" : "км/ч"],
    [isEn ? "Range" : "Запас хода", range == null ? "—" : `${range.toFixed(1)}`, isEn ? "km" : "км"],
    [isEn ? "Power" : "Мощность", power == null ? "—" : `${Math.round(power)}`, isEn ? "W" : "Вт"],
    [isEn ? "Voltage" : "Напряжение", volt == null ? "—" : `${volt.toFixed(1)}`, isEn ? "V" : "В"],
    [isEn ? "Current" : "Ток", curr == null ? "—" : `${curr.toFixed(1)}`, isEn ? "A" : "А"],
  ].map(([l, v, u]) => `<div class="stat-item"><div class="sl">${l}</div><div class="sv">${v}<span class="su">${u}</span></div></div>`).join("");

  const chips = [];
  const rawMode = modeP ? ((isEn && modeP.text_en) ? modeP.text_en : modeP.text) : null;
  const modeTxt = rawMode ? esc(String(rawMode).replace(/\s*\(raw.*\)/, "")) : null;
  if (modeTxt) chips.push(`<span class="chip mode">${modeTxt}</span>`);
  if (locked != null) chips.push(`<span class="chip ${locked ? "bad" : "ok"}">${locked ? (isEn ? "🔒 Locked" : "🔒 Заблокирован") : (isEn ? "🔓 Unlocked" : "🔓 Разблокирован")}</span>`);
  if (riding) chips.push(`<span class="chip ok">${isEn ? "🛴 Riding" : "🛴 Движение"}</span>`);
  if (charging) chips.push(`<span class="chip warn">${isEn ? "⚡ Charging" : "⚡ Зарядка"}</span>`);
  if (fault != null) chips.push(`<span class="chip ${fault ? "bad" : "ok"}">${fault ? (isEn ? "⚠ Fault " + fault : "⚠ Ошибка " + fault) : (isEn ? "✓ No faults" : "✓ Без ошибок")}</span>`);

  host.innerHTML = `
    <div class="hero-battery">
      <svg viewBox="0 0 120 120" class="ring">
        <circle cx="60" cy="60" r="${R}" class="ring-bg"/>
        <circle cx="60" cy="60" r="${R}" class="ring-fg" stroke="${col}"
          stroke-dasharray="${dash.toFixed(1)} ${C.toFixed(1)}" transform="rotate(-90 60 60)"/>
      </svg>
      <div class="ring-label">
        <div class="ring-pct" style="color:${col}">${bat == null ? "—" : Math.round(bat)}<span>%</span></div>
        <div class="ring-sub">${soh == null ? "" : "SOH " + Math.round(soh) + "%"}</div>
      </div>
    </div>
    <div class="hero-right">
      <div class="hero-chips">${chips.join("")}</div>
      <div class="stat-row">${tiles}</div>
    </div>`;
}

// ---- режим езды ----
let rideModeOn = false;
let wakeLock = null;

async function enterRideMode() {
  rideModeOn = true;
  $("ridemode").hidden = false;
  try {
    if ("wakeLock" in navigator) wakeLock = await navigator.wakeLock.request("screen");
  } catch (e) { /* best-effort */ }
  renderRideMode(appState);
}
function exitRideMode() {
  rideModeOn = false;
  $("ridemode").hidden = true;
  if (wakeLock) { wakeLock.release().catch(() => {}); wakeLock = null; }
}
document.addEventListener("visibilitychange", async () => {
  if (rideModeOn && document.visibilityState === "visible" && "wakeLock" in navigator && !wakeLock) {
    try { wakeLock = await navigator.wakeLock.request("screen"); } catch (e) { /* ignore */ }
  }
});

function renderRideMode(state) {
  if (!rideModeOn) return;
  const speed = pnum(state, "2.1"), bat = pnum(state, "1.2"), range = pnum(state, "1.7");
  const fault = pnum(state, "1.8"), locked = pnum(state, "2.2"), modeP = prop(state, "1.1");

  // Пока самокат заблокирован — кнопку выхода прячем (страховка от случайного
  // выхода из ride mode, пока самокат заперт); разблокирован — возвращаем.
  $("ridemode-exit").hidden = locked === 1;

  $("rm-speed-val").textContent = speed == null ? "—" : speed.toFixed(1);
  const batEl = $("rm-battery");
  batEl.textContent = bat == null ? "—" : `${Math.round(bat)}%`;
  batEl.style.color = bat == null ? "#fff" : batteryColor(bat);
  const isEn = getLang() === "en";
  $("rm-range").textContent = range == null ? "—" : `${range.toFixed(1)} ${isEn ? "km" : "км"}`;

  const tripDist = pnum(state, "1.9");
  $("rm-trip-dist").textContent = tripDist == null ? "—" : `${tripDist.toFixed(1)} ${isEn ? "km" : "км"}`;
  const tripTimeP = prop(state, "2.8");
  $("rm-trip-time").textContent = tripTimeP ? ((isEn && tripTimeP.text_en) ? tripTimeP.text_en : tripTimeP.text) : "—";

  const modeTxt = modeP && modeP.text ? esc(String(modeP.text).replace(/\s*\(raw.*\)/, "")) : null;
  const modeEl = $("rm-mode");
  if (modeTxt) { modeEl.textContent = modeTxt; modeEl.hidden = false; } else { modeEl.hidden = true; }

  // Кнопку замка НЕ пересоздаём через innerHTML каждый тик — иначе жест
  // "удержания" (см. ниже) обрывался бы на середине при случайном ре-рендере.
  let lockBtn = document.getElementById("rm-lock-btn");
  if (locked == null) {
    if (lockBtn) lockBtn.remove();
  } else {
    if (!lockBtn) {
      lockBtn = document.createElement("button");
      lockBtn.type = "button";
      lockBtn.id = "rm-lock-btn";
      lockBtn.className = "rm-chip rm-lock-btn";
      $("rm-chips").appendChild(lockBtn);
    }
    lockBtn.dataset.locked = locked ? "1" : "0";
    lockBtn.classList.toggle("bad", Boolean(locked));
    lockBtn.classList.toggle("ok", !locked);
    if (!lockBtn.classList.contains("holding")) {
      lockBtn.textContent = locked ? (isEn ? "🔒 Locked" : "🔒 Заблокирован") : (isEn ? "🔓 Unlocked" : "🔓 Разблокирован");
    }
  }

  const banner = $("rm-fault-banner");
  if (fault) { banner.hidden = false; banner.textContent = isEn ? `⚠ FAULT ${fault}` : `⚠ ОШИБКА ${fault}`; }
  else banner.hidden = true;
}

async function toggleLockFromRideMode(locked, btn) {
  const next = locked ? 0 : 1;
  if (btn) btn.disabled = true;
  try {
    if (locked && !(await verifyPin())) return;   // locked=true -> next=0 -> разблокировка
    appState.write_enabled = true;
    await doSet("2.2", 0, next);
  } finally {
    if (btn) btn.disabled = false;
  }
}

// Вместо модального confirm() (не вписывается в полноэкранный ride mode) —
// жест "удержать ~0.8с". Защищает от случайного тапа, не блокируя интерфейс.
const LOCK_HOLD_MS = 800;
let lockHoldTimer = null;
let lockHoldBtn = null;

function startLockHold(btn, locked) {
  if (lockHoldTimer) return;
  lockHoldBtn = btn;
  btn.classList.add("holding");
  lockHoldTimer = setTimeout(() => {
    lockHoldTimer = null;
    btn.classList.remove("holding");
    toggleLockFromRideMode(locked, btn);
  }, LOCK_HOLD_MS);
}
function cancelLockHold() {
  if (lockHoldTimer) { clearTimeout(lockHoldTimer); lockHoldTimer = null; }
  if (lockHoldBtn) { lockHoldBtn.classList.remove("holding"); lockHoldBtn = null; }
}

$("rm-chips").addEventListener("pointerdown", (e) => {
  const btn = e.target.closest(".rm-lock-btn");
  if (!btn || btn.disabled) return;
  e.preventDefault();
  startLockHold(btn, btn.dataset.locked === "1");
});
$("rm-chips").addEventListener("pointerup", cancelLockHold);
$("rm-chips").addEventListener("pointerleave", cancelLockHold);
$("rm-chips").addEventListener("pointercancel", cancelLockHold);

// ---- список свойств ----
const GROUP_ICONS = { ride: "🛴", battery: "🔋", functions: "⚙️", identity: "🪪", logs: "🗒️" };
let groupsBuilt = false;
const prevValueText = {};

function buildGroups(state) {
  const container = $("groups");
  container.innerHTML = "";
  const isEn = getLang() === "en";
  const groupsList = (isEn && state.groups_en) ? state.groups_en : (state.groups || []);
  for (const g of groupsList) {
    const sec = document.createElement("section");
    sec.className = "panel group";
    const h = document.createElement("h2");
    h.textContent = g.title;
    h.dataset.icon = GROUP_ICONS[g.id] || "▪";
    sec.appendChild(h);

    if (g.id === "logs") {
      const wrap = document.createElement("div");
      wrap.className = "ridelog";
      wrap.dataset.group = "logs";
      sec.appendChild(wrap);
      container.appendChild(sec);
      continue;
    }

    const cards = document.createElement("div");
    cards.className = "cards";
    for (const [s, pnr] of g.props || []) {
      const key = `${s}.${pnr}`;
      const card = document.createElement("div");
      card.className = "prop";
      card.dataset.key = key;
      const name = document.createElement("div");
      name.className = "name";
      name.textContent = shortName(key, state);
      const value = document.createElement("div");
      value.className = "value";
      value.textContent = "—";
      const meta = document.createElement("div");
      meta.className = "meta";
      card.append(name, value, meta);
      cards.appendChild(card);
    }
    sec.appendChild(cards);
    container.appendChild(sec);
  }
  groupsBuilt = true;
}

function renderRideLog(state) {
  const wrap = document.querySelector('.ridelog[data-group="logs"]');
  if (!wrap) return;
  const rides = [];
  const isEn = getLang() === "en";
  for (let i = 1; i <= 5; i++) {
    const p = (state.properties || {})[`6.${i}`];
    if (p) {
      const list = (isEn && p.rides_en) ? p.rides_en : p.rides;
      if (Array.isArray(list)) rides.push(...list);
    }
  }
  const isEn = getLang() === "en";
  if (!rides.length) { wrap.innerHTML = `<div class="ride-empty">${t("no_trip_records")}</div>`; return; }
  const head = `<div class="ride-row ride-head"><span>#</span><span>${t("table_dur")}</span><span>${t("table_dist")}</span><span>${t("table_avg")}</span><span>${t("table_max")}</span></div>`;
  const rows = rides.map((r, i) => `<div class="ride-row"><span class="ride-idx">${i + 1}</span><span>${esc(r.dur)}</span><span>${esc(r.dist)}</span><span>${esc(r.avg)}</span><span>${esc(r.top)}</span></div>`).join("");
  wrap.innerHTML = head + rows;
}

function updateProps(state) {
  if (!groupsBuilt) buildGroups(state);
  document.querySelectorAll(".prop").forEach((card) => {
    const key = card.dataset.key;
    card.classList.toggle("writable", state.writable.includes(key));
    const p = (state.properties || {})[key];
    const value = card.querySelector(".value");
    const meta = card.querySelector(".meta");
    card.classList.toggle("secret", Boolean(p && p.secret));
    if (!p) { value.textContent = "—"; meta.textContent = ""; card.classList.remove("has-data"); return; }
    card.classList.add("has-data");
    const isEn = getLang() === "en";
    const newText = (isEn && p.text_en) ? p.text_en : (p.text || "—");
    value.textContent = newText;
    card.classList.toggle("bool-on", p.text === "вкл" || p.text === "on");
    card.classList.toggle("bool-off", p.text === "выкл" || p.text === "off");
    value.classList.toggle("val-text", Boolean(p.text) && p.text.length > 14);
    if (prevValueText[key] !== undefined && prevValueText[key] !== newText) {
      card.classList.remove("flash"); void card.offsetWidth; card.classList.add("flash");
    }
    prevValueText[key] = newText;
    const bits = [];
    if (p.type) bits.push(p.type);
    if (p.ts) bits.push(p.ts);
    if (p.status) bits.push("status=" + p.status);
    if (p.secret) bits.push("скрыто");
    meta.textContent = bits.join(" · ");
  });
}

let lastEventId = 0;
function updateEvents(state) {
  const box = $("events");
  for (const e of state.events || []) {
    if (e.id > lastEventId) {
      lastEventId = e.id;
      const line = document.createElement("div");
      line.className = "line";
      const ts = document.createElement("span");
      ts.className = "ts";
      ts.textContent = e.ts;
      line.append(ts, document.createTextNode(" " + (e.message || "")));
      box.appendChild(line);
    }
  }
  while (box.children.length > 200) box.removeChild(box.firstChild);
  box.scrollTop = box.scrollHeight;
}

function updateControls(state) {
  const badge = $("badge");
  badge.className = "badge " + (state.status || "idle");
  badge.textContent = state.status || "idle";
  $("msg").textContent = state.message || "";
  $("updated").textContent = state.last_update || "—";

  const isEn = getLang() === "en";
  const wb = $("write-toggle");
  wb.textContent = state.write_enabled
    ? (isEn ? "🔓 Control on" : "🔓 Управление вкл")
    : (isEn ? "🔒 Read only" : "🔒 Только чтение");
  wb.classList.toggle("on", state.write_enabled);
  document.body.classList.toggle("write-on", state.write_enabled);
}

function render() {
  updateControls(appState);
  renderHero(appState);
  updateProps(appState);
  renderRideLog(appState);
  updateEvents(appState);
  renderRideMode(appState);
}

$("ridemode-toggle").onclick = () => { if (rideModeOn) exitRideMode(); else enterRideMode(); };
$("ridemode-exit").onclick = exitRideMode;

$("write-toggle").onclick = async () => {
  const enabled = !appState.write_enabled;
  if (enabled && !(await showModal(
    "Enable control mode?",
    "Clicking a setting will change scooter configuration (SET) until toggled off."))) return;
  appState.write_enabled = enabled;
  addEvent(`control mode: ${enabled ? "ON" : "off"}`);
  render();
};

$("groups").addEventListener("click", async (e) => {
  const card = e.target.closest(".prop.writable");
  if (!card || !appState.write_enabled) return;
  const key = card.dataset.key;
  const p = appState.properties[key];
  const label = shortName(key, appState);
  const vals = appState.writable_values[key];
  let next, curLabel, nextLabel;
  if (Array.isArray(vals) && vals.length) {
    const cur = p && typeof p.num === "number" ? p.num : vals[0][0];
    const idx = vals.findIndex(([v]) => v === cur);
    const [nv, nl] = vals[(idx + 1) % vals.length];
    next = nv; nextLabel = nl;
    curLabel = (vals.find(([v]) => v === cur) || [, String(cur)])[1];
  } else {
    const cur = p && p.text === "вкл" ? 1 : 0;
    next = cur ? 0 : 1;
    curLabel = cur ? "вкл" : "выкл"; nextLabel = next ? "вкл" : "выкл";
  }
  const confirmMsg = appState.writable_confirm[key];
  const msg = confirmMsg
    ? `${confirmMsg}\n\n${curLabel} → ${nextLabel}`
    : `${curLabel} → ${nextLabel}`;
  if (!(await showModal(label, msg, { danger: Boolean(confirmMsg) }))) return;
  if (key === "2.2" && next === 0 && !(await verifyPin())) return;   // IS_LOCKED -> 0 = разблокировка
  const spec = props.WRITABLE[key];
  await doSet(key, spec.type, next);
});

// ============================================================
// BLE-оркестрация: подключение, логин, поллинг, SET.
// ============================================================
let transport = null;
let sk = null;
let appCnt = 0;
let unitMult = 1.0;
let pollAbort = null;

// ---- мои самокаты (несколько сохранённых профилей). Web Bluetooth не даёт
// подключиться по MAC напрямую (приватность браузера) — единственный
// стабильный идентификатор конкретного физического устройства на этом
// origin это device.id, который выдаёт сам requestDevice(). Поэтому профиль
// привязан не к MAC, а к нему: при первом подключении к новому device.id
// спрашиваем имя+LTMK и запоминаем, при повторных — подставляем автоматически. ----
const PROFILES_KEY = "scooter_profiles";
let currentProfile = null;

function loadProfiles() {
  try { return JSON.parse(localStorage.getItem(PROFILES_KEY) || "[]"); } catch (e) { return []; }
}
function saveProfiles(list) { localStorage.setItem(PROFILES_KEY, JSON.stringify(list)); }

function updateScooterButton() {
  const isEn = getLang() === "en";
  $("scooter-toggle").textContent = "📡 " + (currentProfile ? currentProfile.name : (isEn ? "not connected" : "не подключён"));
}

/** Находит сохранённый профиль по device.id или создаёт новый (спрашивает имя+LTMK). */
// ---- сканирование QR камерой (для переноса LTMK с webui — "Мои самокаты" →
// 🔑 → "Показать QR для телефона" — без ручного набора 64 hex-символов).
// BarcodeDetector — нативный Chrome API, без внешних библиотек; если браузер
// его не поддерживает (не Chrome/Edge на Android), просто откатываемся на
// ручной ввод, ничего не ломая. ----
function scanQrCode() {
  return new Promise((resolve) => {
    if (!("BarcodeDetector" in window)) { resolve(null); return; }
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
      .then((stream) => {
        const video = $("qrscan-video");
        video.srcObject = stream;
        $("qrscan-overlay").hidden = false;
        video.play().catch(() => {});
        const detector = new BarcodeDetector({ formats: ["qr_code"] });
        let stopped = false;
        const stop = (result) => {
          if (stopped) return;
          stopped = true;
          stream.getTracks().forEach((t) => t.stop());
          video.srcObject = null;
          $("qrscan-overlay").hidden = true;
          resolve(result);
        };
        $("qrscan-cancel").onclick = () => stop(null);
        (async function tick() {
          while (!stopped) {
            try {
              const codes = await detector.detect(video);
              if (codes.length) { stop(codes[0].rawValue); return; }
            } catch (e) { /* нечитаемый кадр — пробуем следующий */ }
            await sleep(250);
          }
        })();
      })
      .catch(() => resolve(null));   // камера недоступна/отказано — тихий откат на ручной ввод
  });
}

/** LTMK для нового профиля: сначала предлагает сканировать QR (если поддерживается), иначе/по отказу — ручной ввод. */
async function promptLtmk() {
  let hex = null;
  if ("BarcodeDetector" in window) {
    const wantScan = await showModal(
      "LTMK for this scooter",
      "You can scan the QR code with your camera (webui → 'My Scooters' → 🔑 → 'Show QR for phone') or enter it manually.",
      { okText: "📷 Scan" });
    if (wantScan) {
      const scanned = await scanQrCode();
      if (scanned) hex = scanned.trim().toLowerCase();
    }
  }
  if (!hex) {
    hex = (await showModal(
      "LTMK for this scooter",
      "64 hex characters — 32 bytes of the login key. Stored only in this browser.",
      { input: true, inputPlaceholder: "LTMK hex", okText: "Save" })) || "";
  }
  return hex;
}

async function resolveProfile(device) {
  const profiles = loadProfiles();
  let profile = profiles.find((p) => p.id === device.id);
  if (!profile) {
    const name = (await showModal(
      "New scooter",
      `Device "${device.name || "unnamed"}" is connecting for the first time. Enter friendly name (e.g. 'mine').`,
      { input: true, inputPlaceholder: "name", inputValue: device.name || "", okText: "Next" }));
    if (!name) throw new Error("connection canceled (no name provided)");
    const hex = await promptLtmk();
    if (!/^[0-9a-fA-F]{64}$/.test(hex)) throw new Error("LTMK must be 64 hex characters (32 bytes)");
    profile = { id: device.id, name, ltmkHex: hex.toLowerCase() };
    profiles.push(profile);
    saveProfiles(profiles);
  }
  return profile;
}

function renderScootersList() {
  const box = $("scooters-list");
  const profiles = loadProfiles();
  box.innerHTML = "";
  if (!profiles.length) {
    const empty = document.createElement("div");
    empty.className = "scooter-mac";
    empty.textContent = "No saved profiles yet — they will appear automatically after connecting.";
    box.appendChild(empty);
    return;
  }
  for (const p of profiles) {
    const row = document.createElement("div");
    row.className = "scooter-row" + (currentProfile && currentProfile.id === p.id ? " active" : "");

    const info = document.createElement("div");
    info.className = "scooter-info";
    const name = document.createElement("div");
    name.className = "scooter-name";
    name.textContent = p.name;
    const hint = document.createElement("div");
    hint.className = "scooter-mac";
    hint.textContent = `LTMK ${p.ltmkHex.slice(0, 4)}…`;
    info.append(name, hint);

    const actions = document.createElement("div");
    actions.className = "scooter-actions";

    const renameBtn = document.createElement("button");
    renameBtn.type = "button";
    renameBtn.className = "modal-btn scooter-select";
    renameBtn.textContent = "Rename";
    renameBtn.onclick = async () => {
      const next = await showModal("Rename scooter", "New name.", { input: true, inputValue: p.name, okText: "Save" });
      if (!next) return;
      const list = loadProfiles();
      const idx = list.findIndex((x) => x.id === p.id);
      if (idx >= 0) { list[idx].name = next; saveProfiles(list); }
      if (currentProfile && currentProfile.id === p.id) { currentProfile = list[idx]; updateScooterButton(); }
      renderScootersList();
    };
    actions.appendChild(renameBtn);

    const delBtn = document.createElement("button");
    delBtn.type = "button";
    delBtn.className = "modal-btn scooter-del";
    delBtn.textContent = "✕";
    delBtn.title = "Delete";
    delBtn.onclick = async () => {
      if (!(await showModal("Delete scooter?", `"${p.name}" will be removed from the list.`, { danger: true, okText: "Delete" }))) return;
      saveProfiles(loadProfiles().filter((x) => x.id !== p.id));
      if (currentProfile && currentProfile.id === p.id) { currentProfile = null; updateScooterButton(); }
      renderScootersList();
    };
    actions.appendChild(delBtn);

    row.append(info, actions);
    box.appendChild(row);
  }
}

$("scooter-toggle").onclick = () => {
  renderScootersList();
  $("scooters-overlay").hidden = false;
};
$("scooters-close").onclick = () => { $("scooters-overlay").hidden = true; };
$("scooters-overlay").addEventListener("click", (e) => {
  if (e.target === $("scooters-overlay")) $("scooters-overlay").hidden = true;
});
$("scooters-add").textContent = "+ Connect New";
$("scooters-add").onclick = () => {
  $("scooters-overlay").hidden = true;
  connect();
};

async function readOne(siid, piid) {
  const obj = await specGet(transport, sk, siid, piid, appCnt);
  appCnt += 1;
  const key = `${siid}.${piid}`;
  if (!obj) {
    appState.properties[key] = { key, siid, piid, name: props.NAMES[key] || "?", text: "no response", type: null, secret: false, groups: props.PROP_GROUPS[key] || [] };
    return null;
  }
  if (key === "3.5" && obj.status === 0) {
    unitMult = props.unitMultiplier(decodeValue(obj.tcode, obj.value));
  }
  const fmt = props.formatProperty(siid, piid, obj.tcode, obj.value || new Uint8Array(0), unitMult);
  if (obj.status && obj.status !== 0) fmt.text += ` [status=${obj.status}]`;
  fmt.ts = new Date().toLocaleTimeString();
  appState.properties[key] = fmt;
  if (!fmt.secret) addEvent(`${props.LABELS[key] || fmt.name} = ${fmt.text}`);
  return fmt;
}

// SET не выполняется напрямую из клика — только кладётся в очередь. BLE
// (Web Bluetooth GATT) не терпит двух одновременных транзакций на одном
// соединении: если бы doSet() дёргал specSet() прямо во время того, как
// pollLoop ждёт ответ на свой readOne(), оба вызова specTxn/specGet чистят
// transport.rx в начале — они бы затирали друг другу ответы. Поэтому SET
// выполняет ТОЛЬКО pollLoop (тот же поток BLE-операций), а applyPendingSets()
// вызывается между каждым отдельным чтением — иначе клик ждал бы окончания
// всего текущего батча чтений (секунды), как было до этого исправления
// (аналогичный фикс сделан в webui/ble_worker.py:read_props).
const pendingSets = [];

function doSet(key, typeCode, value) {
  return new Promise((resolve) => {
    pendingSets.push({ key, typeCode, value, resolve });
  });
}

async function applyPendingSets() {
  while (pendingSets.length) {
    const { key, typeCode, value, resolve } = pendingSets.shift();
    const [siid, piid] = key.split(".").map(Number);
    const valBytes = typeCode === 0 ? new Uint8Array([value ? 1 : 0]) : new Uint8Array([value & 0xff]);
    const label = props.LABELS[key] || key;
    addEvent(`SET ${label} = ${value} — sending`);
    try {
      const { ok, status } = await specSet(transport, sk, siid, piid, typeCode, valBytes, appCnt);
      appCnt += 1;
      if (ok) {
        addEvent(`SET ${label} → ${value}: accepted (status 0)`);
        await sleep(300);
        await readOne(siid, piid);
      } else {
        addEvent(`SET ${label} → ${value}: REFUSED (status=${status})`);
      }
    } catch (e) {
      addEvent(`SET ${label}: error ${e.message}`);
    }
    render();
    resolve();
  }
}

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

async function pollLoop(signal) {
  // сначала единицы — дальнейшие расстояния/скорости конвертируются верно
  await readOne(3, 5);
  render();
  // журнал поездок — один раз в начале (как в ble_worker.py poll mode)
  for (const [s, p] of props.LOG_SET) {
    if (signal.aborted) return;
    await readOne(s, p);
    render();
    await sleep(350);
  }

  let lastStatic = 0;
  const dynamicNoUnit = props.DYNAMIC_SET.filter(([s, p]) => !(s === 3 && p === 5));
  setStatus("polling", "polling live telemetry ~every 3s; slow set ~60s");
  render();

  while (!signal.aborted) {
    for (const [s, p] of dynamicNoUnit) {
      if (signal.aborted) return;
      if (pendingSets.length) await applyPendingSets();
      await readOne(s, p);
      render();
      await sleep(350);
    }
    if (Date.now() - lastStatic >= 60000) {
      for (const [s, p] of props.STATIC_SET) {
        if (signal.aborted) return;
        if (pendingSets.length) await applyPendingSets();
        await readOne(s, p);
        render();
        await sleep(350);
      }
      lastStatic = Date.now();
    }
    // простой между раундами — не ждать сложа руки, если накопился клик
    const idleUntil = Date.now() + 1000;
    while (Date.now() < idleUntil) {
      if (signal.aborted) return;
      if (pendingSets.length) { await applyPendingSets(); break; }
      await sleep(150);
    }
  }
}

async function connect() {
  $("connect").disabled = true;
  try {
    setStatus("connecting", "selecting device…"); render();
    transport = new Transport();
    transport.onLog = (msg) => { /* технический BLE-лог — не в UI, слишком шумно */ };
    await transport.requestDevice();

    currentProfile = await resolveProfile(transport.device);
    updateScooterButton();
    const ltmk = hexToBytes(currentProfile.ltmkHex);

    await transport.connect();

    setStatus("login", "key exchange (ECDH + AES-CCM)…"); render();
    sk = await login(transport, ltmk);
    appCnt = 0;

    setStatus("ready", "LOGIN OK"); addEvent("LOGIN OK"); render();
    $("disconnect").disabled = false;

    const controller = new AbortController();
    pollAbort = controller;
    await pollLoop(controller.signal);
  } catch (e) {
    setStatus("error", e.message || String(e));
    addEvent(`Error: ${e.message || e}`);
    render();
  } finally {
    $("connect").disabled = false;
  }
}

async function disconnect() {
  if (pollAbort) pollAbort.abort();
  setStatus("stopping", "stopping…"); render();
  try { if (transport) await transport.disconnect(); } catch (e) { /* ignore */ }
  transport = null; sk = null;
  $("disconnect").disabled = true;
  setStatus("idle", ""); render();
}

$("connect").onclick = connect;
$("disconnect").onclick = disconnect;
$("pin-toggle").onclick = managePin;
updatePinButton();
updateScooterButton();

if (!("bluetooth" in navigator)) {
  setStatus("error", "Web Bluetooth is not supported in this browser (Chrome/Edge on Android required, not Safari/iOS).");
  addEvent("Web Bluetooth API unavailable — navigator.bluetooth not found.");
}

render();

const langBtn = $("lang-toggle");
if (langBtn) {
  langBtn.addEventListener("click", () => {
    toggleLang();
  });
}
applyI18n();

onLanguageChange(() => {
  groupsBuilt = false;
  updateControls(appState);
  renderHero(appState);
  renderRideMode(appState);
  buildGroups(appState);
  updateProps(appState);
  renderRideLog(appState);
  updatePinButton();
  updateScooterButton();
});
