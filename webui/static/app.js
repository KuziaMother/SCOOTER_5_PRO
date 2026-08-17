/* Scooter 5 Pro web UI — client logic (kept separate from HTML/CSS/Python). */
const $ = (id) => document.getElementById(id);

let lastHistId = 0;
let lastEventId = 0;
let groupsBuilt = false;
let writeEnabled = false;
let stateWritable = new Set();
let stateConfirm = {};
let stateWritableValues = {};
let lastState = null;
const prevValueText = {};   // key -> последний отрендеренный текст (для flash-анимации)

// ---- модалка подтверждения (замена нативного confirm()/prompt() для обычного
// режима; в ride mode вместо неё жест "удержать", см. ниже — модалка там не
// вписывается). С input:true работает как prompt(): резолвится строкой или
// null при отмене; без input — как confirm(): true/false. ----
function showModal(title, message, opts = {}) {
  const { danger = false, okText = "Подтвердить", input = false, inputPlaceholder = "", inputType = "text", inputValue = "" } = opts;
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
  btn.title = hasPin() ? "PIN на разблокировку включён (клик — изменить/убрать)" : "PIN на разблокировку выключен (клик — включить)";
}

async function verifyPin() {
  if (!hasPin()) return true;
  const entered = await showModal(
    "PIN для разблокировки", "Введите PIN, чтобы разблокировать самокат.",
    { input: true, inputPlaceholder: "PIN", inputType: "password", okText: "Разблокировать" });
  if (!entered) return false;
  if ((await sha256Hex(entered)) !== localStorage.getItem(PIN_KEY)) {
    alert("Неверный PIN.");
    return false;
  }
  return true;
}

async function managePin() {
  if (hasPin()) {
    const cur = await showModal(
      "Изменить PIN", "Введите текущий PIN, чтобы изменить или отключить защиту.",
      { input: true, inputPlaceholder: "текущий PIN", inputType: "password", okText: "Далее" });
    if (!cur) return;
    if ((await sha256Hex(cur)) !== localStorage.getItem(PIN_KEY)) { alert("Неверный PIN."); return; }
  }
  const next = await showModal(
    hasPin() ? "Новый PIN" : "Установить PIN на разблокировку",
    `Минимум 4 цифры. ${hasPin() ? "Оставьте пустым, чтобы отключить защиту." : "Потребуется при каждой разблокировке."}`,
    { input: true, inputPlaceholder: "новый PIN", inputType: "password", okText: "Далее" });
  if (next === null) return;
  if (!next) {
    if (hasPin()) {
      localStorage.removeItem(PIN_KEY);
      updatePinButton();
    }
    return;
  }
  if (!/^\d{4,}$/.test(next)) { alert("PIN должен быть числом из минимум 4 цифр."); return; }
  const repeat = await showModal(
    "Повторите PIN", "Введите тот же PIN ещё раз для подтверждения.",
    { input: true, inputPlaceholder: "повтор PIN", inputType: "password", okText: "Сохранить" });
  if (repeat !== next) { alert("PIN не совпадает — попробуйте снова."); return; }
  localStorage.setItem(PIN_KEY, await sha256Hex(next));
  updatePinButton();
}

// ---- мои самокаты (несколько сохранённых профилей: имя + MAC; LTMK для
// каждого MAC резолвится на сервере отдельно, см. dreame_auth.ltmk_path_for_mac) ----
const SELECTED_MAC_KEY = "scooter_selected_mac";
let scooters = [];
let selectedMac = localStorage.getItem(SELECTED_MAC_KEY) || "";

function isSelected(mac) {
  return (mac || "").toUpperCase() === (selectedMac || "").toUpperCase();
}

function updateScooterButton() {
  const cur = scooters.find((s) => isSelected(s.mac));
  $("scooter-toggle").textContent = "📡 " + (cur ? cur.name : "выбрать");
}

async function loadScooters() {
  const r = await fetch("/api/scooters");
  const j = await r.json();
  scooters = j.scooters || [];
  if (!scooters.some((s) => isSelected(s.mac))) {
    selectedMac = scooters[0] ? scooters[0].mac : "";
    localStorage.setItem(SELECTED_MAC_KEY, selectedMac);
  }
  updateScooterButton();
}

function renderScootersList() {
  const box = $("scooters-list");
  box.innerHTML = "";
  if (!scooters.length) {
    const empty = document.createElement("div");
    empty.className = "scooter-mac";
    empty.textContent = "Пока нет сохранённых самокатов — добавьте сканом рядом или вручную.";
    box.appendChild(empty);
    return;
  }
  for (const s of scooters) {
    const row = document.createElement("div");
    row.className = "scooter-row" + (isSelected(s.mac) ? " active" : "");

    const info = document.createElement("div");
    info.className = "scooter-info";
    const name = document.createElement("div");
    name.className = "scooter-name";
    name.textContent = s.name;
    const mac = document.createElement("div");
    mac.className = "scooter-mac";
    mac.textContent = s.mac;
    info.append(name, mac);

    const actions = document.createElement("div");
    actions.className = "scooter-actions";

    const selectBtn = document.createElement("button");
    selectBtn.type = "button";
    selectBtn.className = "modal-btn scooter-select";
    const active = isSelected(s.mac);
    selectBtn.textContent = active ? "Активен" : "Выбрать";
    selectBtn.disabled = active;
    selectBtn.onclick = () => {
      selectedMac = s.mac;
      localStorage.setItem(SELECTED_MAC_KEY, selectedMac);
      updateScooterButton();
      renderScootersList();
    };
    actions.appendChild(selectBtn);

    const ltmkBtn = document.createElement("button");
    ltmkBtn.type = "button";
    ltmkBtn.className = "modal-btn scooter-ltmk";
    ltmkBtn.textContent = "🔑";
    ltmkBtn.title = "Получить LTMK через Mi Cloud";
    ltmkBtn.onclick = () => openLtmkFlow(s.mac, s.name);
    actions.appendChild(ltmkBtn);

    const delBtn = document.createElement("button");
    delBtn.type = "button";
    delBtn.className = "modal-btn scooter-del";
    delBtn.textContent = "✕";
    delBtn.title = "Удалить";
    delBtn.onclick = async () => {
      if (!(await showModal("Удалить самокат?", `«${s.name}» (${s.mac}) будет удалён из списка сохранённых.`, { danger: true, okText: "Удалить" }))) return;
      const r = await fetch("/api/scooters/delete", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mac: s.mac }),
      });
      const j = await r.json();
      if (!j.ok) { alert(j.error || "не удалось удалить"); return; }
      scooters = j.scooters;
      if (isSelected(s.mac)) {
        selectedMac = scooters[0] ? scooters[0].mac : "";
        localStorage.setItem(SELECTED_MAC_KEY, selectedMac);
      }
      updateScooterButton();
      renderScootersList();
    };
    actions.appendChild(delBtn);

    row.append(info, actions);
    box.appendChild(row);
  }
}

$("scooter-toggle").onclick = async () => {
  await loadScooters();
  renderScootersList();
  $("scooters-scan-results").hidden = true;
  $("scooters-scan-results").innerHTML = "";
  $("scooters-overlay").hidden = false;
};
$("scooters-close").onclick = () => { $("scooters-overlay").hidden = true; };
$("scooters-overlay").addEventListener("click", (e) => {
  if (e.target === $("scooters-overlay")) $("scooters-overlay").hidden = true;
});

/** Сохраняет новый профиль на сервере и обновляет локальный список/выбор. */
async function addScooterProfile(name, mac) {
  const r = await fetch("/api/scooters", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, mac }),
  });
  const j = await r.json();
  if (!j.ok) { alert(j.error || "не удалось добавить"); return false; }
  scooters = j.scooters;
  selectedMac = mac.toUpperCase();
  localStorage.setItem(SELECTED_MAC_KEY, selectedMac);
  updateScooterButton();
  renderScootersList();
  return true;
}

$("scooters-add").onclick = async () => {
  const name = await showModal("Новый самокат", "Название для удобства (например «мой» или «рабочий»).", { input: true, inputPlaceholder: "название", okText: "Далее" });
  if (!name) return;
  const mac = await showModal("MAC самоката", "Формат AA:BB:CC:DD:EE:FF.", { input: true, inputPlaceholder: "AA:BB:CC:DD:EE:FF", okText: "Сохранить" });
  if (!mac) return;
  await addScooterProfile(name, mac);
};

function renderScanResults(devices) {
  const box = $("scooters-scan-results");
  box.innerHTML = "";
  box.hidden = false;
  if (!devices.length) {
    const empty = document.createElement("div");
    empty.className = "scooter-mac";
    empty.textContent = "Рядом ничего не найдено — самокат должен быть включён и не подключён к телефону/другому устройству.";
    box.appendChild(empty);
    return;
  }
  const savedMacs = new Set(scooters.map((s) => s.mac.toUpperCase()));
  for (const d of devices) {
    const row = document.createElement("div");
    row.className = "scooter-row";

    const info = document.createElement("div");
    info.className = "scooter-info";
    const name = document.createElement("div");
    name.className = "scooter-name";
    name.textContent = (d.likely ? "🛴 " : "") + d.name;
    const meta = document.createElement("div");
    meta.className = "scooter-mac";
    meta.textContent = `${d.mac} · RSSI ${d.rssi} дБм`;
    info.append(name, meta);

    const actions = document.createElement("div");
    actions.className = "scooter-actions";
    if (savedMacs.has(d.mac.toUpperCase())) {
      const tag = document.createElement("span");
      tag.className = "scooter-mac";
      tag.textContent = "уже сохранён";
      actions.appendChild(tag);
    } else {
      const addBtn = document.createElement("button");
      addBtn.type = "button";
      addBtn.className = "modal-btn scooter-select";
      addBtn.textContent = "+ Добавить";
      addBtn.onclick = async () => {
        const name2 = await showModal("Название самоката", `MAC ${d.mac}`, { input: true, inputValue: d.name, okText: "Сохранить" });
        if (!name2) return;
        if (await addScooterProfile(name2, d.mac)) renderScanResults(devices);
      };
      actions.appendChild(addBtn);
    }

    row.append(info, actions);
    box.appendChild(row);
  }
}

$("scooters-scan-btn").onclick = async () => {
  const btn = $("scooters-scan-btn");
  const orig = btn.textContent;
  btn.disabled = true;
  btn.textContent = "Сканирую (5с)…";
  $("scooters-scan-results").hidden = false;
  $("scooters-scan-results").innerHTML = "";
  try {
    const r = await fetch("/api/scooters/scan", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ timeout: 5 }),
    });
    const j = await r.json();
    if (!j.ok) { alert(j.error || "скан не удался"); return; }
    renderScanResults(j.devices || []);
  } catch (e) {
    alert(`скан не удался: ${e.message}`);
  } finally {
    btn.disabled = false;
    btn.textContent = orig;
  }
};

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

// ---- получение LTMK через Mi Cloud (QR-логин, без пароля) и перенос на
// телефон QR-кодом (PWA его сканирует камерой — см. resolveProfile в
// APK_build/pwa/js/app.js). Сам ключ никогда не попадает в alert/console —
// только факт успеха и длина (§6 CLAUDE.md). ----
function ltmkSetBody(html) { $("ltmk-body").innerHTML = html; }

function openLtmkFlow(mac, name) {
  $("ltmk-overlay").hidden = false;
  ltmkStepLogin(mac, name);
}
$("ltmk-close").onclick = () => { $("ltmk-overlay").hidden = true; };
$("ltmk-overlay").addEventListener("click", (e) => {
  if (e.target === $("ltmk-overlay")) $("ltmk-overlay").hidden = true;
});

async function ltmkStepLogin(mac, name) {
  ltmkSetBody(`<div class="scooter-mac">Проверяю сессию Mi Cloud…</div>`);
  const st = await (await fetch("/api/ltmk/status")).json();
  if (st.logged_in) { await ltmkStepDevices(mac, name); return; }

  ltmkSetBody(
    `<div class="scooter-mac">Вход в Mi Cloud нужен один раз — сессия сохранится локально (без пароля, по QR).</div>
     <button id="ltmk-qr-start" type="button" class="modal-btn scooter-select">Показать QR для входа</button>
     <div id="ltmk-qr-box"></div>`);
  $("ltmk-qr-start").onclick = async () => {
    $("ltmk-qr-start").disabled = true;
    const r = await fetch("/api/ltmk/qr_start", { method: "POST" });
    const j = await r.json();
    if (!j.ok) { alert(j.error || "не удалось начать вход"); $("ltmk-qr-start").disabled = false; return; }
    const linkHtml = j.login_url
      ? `<div class="scooter-mac">Или, если в браузере на этом компьютере уже открыт аккаунт Xiaomi:
           <a href="${esc(j.login_url)}" target="_blank" rel="noopener">войти по ссылке</a>, без сканирования.</div>`
      : "";
    $("ltmk-qr-box").innerHTML =
      `<img class="ltmk-qr-img" src="data:image/png;base64,${j.qr_png_b64}" alt="QR для входа в Mi Cloud">
       <div class="scooter-mac">Отсканируйте в приложении Mi Home / Xiaomi Home…</div>
       ${linkHtml}`;
    pollLtmkQrLogin(mac, name);
  };
}

async function pollLtmkQrLogin(mac, name) {
  for (;;) {
    await sleep(2000);
    if ($("ltmk-overlay").hidden) return;   // модалку закрыли — прекращаем поллинг
    const j = await (await fetch("/api/ltmk/qr_status")).json();
    if (j.status === "done") { await ltmkStepDevices(mac, name); return; }
    if (j.status === "error") { ltmkSetBody(`<div class="scooter-mac">Ошибка входа: ${esc(j.error || "?")}</div>`); return; }
  }
}

async function ltmkStepDevices(mac, name) {
  ltmkSetBody(`<div class="scooter-mac">Загружаю список устройств аккаунта…</div>`);
  const r = await fetch("/api/ltmk/devices");
  const j = await r.json();
  if (!j.ok) { ltmkSetBody(`<div class="scooter-mac">Ошибка: ${esc(j.error || "?")}</div>`); return; }
  const devices = j.devices || [];
  if (!devices.length) { ltmkSetBody(`<div class="scooter-mac">В аккаунте не нашлось устройств.</div>`); return; }

  const box = document.createElement("div");
  box.className = "scooters-list";
  for (const d of devices) {
    const match = Boolean(mac && d.mac && d.mac.toUpperCase() === mac.toUpperCase());
    const row = document.createElement("div");
    row.className = "scooter-row" + (match ? " active" : "");
    const info = document.createElement("div");
    info.className = "scooter-info";
    const dname = document.createElement("div");
    dname.className = "scooter-name";
    dname.textContent = d.name + (match ? " · это устройство" : "");
    const dmeta = document.createElement("div");
    dmeta.className = "scooter-mac";
    dmeta.textContent = [d.model, d.mac].filter(Boolean).join(" · ");
    info.append(dname, dmeta);
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "modal-btn scooter-select";
    btn.textContent = "Выбрать";
    btn.onclick = () => ltmkStepFetch(d.did, d.country, mac || d.mac);
    row.append(info, btn);
    box.appendChild(row);
  }
  $("ltmk-body").innerHTML = "";
  $("ltmk-body").appendChild(box);
}

async function ltmkStepFetch(did, country, mac, pin) {
  ltmkSetBody(`<div class="scooter-mac">Получаю ключ…</div>`);
  const r = await fetch("/api/ltmk/fetch", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ did, country, mac, pin: pin || undefined }),
  });
  const j = await r.json();
  if (r.status === 428 || j.error === "PIN_REQUIRED") {
    const enteredPin = await showModal(
      "Нужен PIN",
      "На этом аккаунте ключ защищён PIN'ом шаринга Bluetooth (задан в Mi Home при привязке самоката). Введите его.",
      { input: true, inputType: "password", inputPlaceholder: "PIN", okText: "Далее" });
    if (!enteredPin) { ltmkSetBody(`<div class="scooter-mac">Отменено.</div>`); return; }
    await ltmkStepFetch(did, country, mac, enteredPin);
    return;
  }
  if (!j.ok) { ltmkSetBody(`<div class="scooter-mac">Ошибка: ${esc(j.error || "?")}</div>`); return; }

  ltmkSetBody(
    `<div class="scooter-mac">Готово: LTMK сохранён для ${esc(mac)} (${j.length} байт).</div>
     <button id="ltmk-reveal" type="button" class="modal-btn scooter-select">Показать QR для телефона</button>
     <div id="ltmk-reveal-box"></div>`);
  $("ltmk-reveal").onclick = async () => {
    const rr = await fetch("/api/ltmk/reveal_qr", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mac }),
    });
    const jj = await rr.json();
    if (!jj.ok) { alert(jj.error || "не удалось показать QR"); return; }
    $("ltmk-reveal-box").innerHTML =
      `<img class="ltmk-qr-img" src="data:image/png;base64,${jj.qr_png_b64}" alt="QR с LTMK">
       <div class="scooter-mac">Отсканируйте в PWA при добавлении этого самоката. Не показывайте этот экран посторонним.</div>`;
  };
}

function esc(s) {
  return String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}

function shortName(key, state) {
  return (state.labels && state.labels[key]) || (state.names && state.names[key]) || key;
}

// ---- hero-сводка ----
function prop(state, key) { return (state.properties || {})[key] || null; }
function pnum(state, key) { const p = prop(state, key); return p && typeof p.num === "number" ? p.num : null; }

function batteryColor(pct) {
  if (pct == null) return "var(--text-faint)";
  if (pct <= 15) return "var(--bad)";
  if (pct <= 35) return "var(--warn)";
  return "var(--ok)";
}

function renderHero(state) {
  const host = $("hero");
  const props = state.properties || {};
  if (!Object.keys(props).length) { host.hidden = true; return; }
  host.hidden = false;

  const bat = pnum(state, "1.2");                 // BATTERY_LEVEL %
  const soh = pnum(state, "3.12");                // SOH %
  const speed = pnum(state, "2.1");               // AVERAGE_SPEED (живая) км/ч
  const range = pnum(state, "1.7");               // REMAINING_MILEAGE км
  const power = pnum(state, "1.6");               // POWER Вт
  const volt = pnum(state, "1.4");                // VOLTAGE В
  const curr = pnum(state, "1.5");                // CURRENT А
  const modeP = prop(state, "1.1");
  const fault = pnum(state, "1.8");
  const locked = pnum(state, "2.2");
  const riding = pnum(state, "2.7");
  const charging = pnum(state, "3.10");

  const R = 52, C = 2 * Math.PI * R;
  const pct = bat == null ? 0 : Math.max(0, Math.min(100, bat));
  const dash = (pct / 100) * C;
  const col = batteryColor(bat);

  const tiles = [
    ["Ср. скорость", speed == null ? "—" : `${speed.toFixed(1)}`, "км/ч"],
    ["Запас хода", range == null ? "—" : `${range.toFixed(1)}`, "км"],
    ["Мощность", power == null ? "—" : `${Math.round(power)}`, "Вт"],
    ["Напряжение", volt == null ? "—" : `${volt.toFixed(1)}`, "В"],
    ["Ток", curr == null ? "—" : `${curr.toFixed(1)}`, "А"],
  ].map(([l, v, u]) => `<div class="stat-item">
      <div class="sl">${l}</div>
      <div class="sv">${v}<span class="su">${u}</span></div>
    </div>`).join("");

  const chips = [];
  const modeTxt = modeP && modeP.text ? esc(String(modeP.text).replace(/\s*\(raw.*\)/, "")) : null;
  if (modeTxt) chips.push(`<span class="chip mode">${modeTxt}</span>`);
  if (locked != null) chips.push(`<span class="chip ${locked ? "bad" : "ok"}">${locked ? "🔒 Заблокирован" : "🔓 Разблокирован"}</span>`);
  if (riding) chips.push(`<span class="chip ok">🛴 Движение</span>`);
  if (charging) chips.push(`<span class="chip warn">⚡ Зарядка</span>`);
  if (fault != null) chips.push(`<span class="chip ${fault ? "bad" : "ok"}">${fault ? "⚠ Ошибка " + fault : "✓ Без ошибок"}</span>`);

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

// ---- режим езды (полноэкранный, для крепления на руль) ----
let rideModeOn = false;
let wakeLock = null;

async function enterRideMode() {
  rideModeOn = true;
  $("ridemode").hidden = false;
  try {
    if ("wakeLock" in navigator) {
      wakeLock = await navigator.wakeLock.request("screen");
    }
  } catch (e) { /* best-effort: если недоступно (нет HTTPS/платформа), просто без wake lock */ }
  renderRideMode(lastState || {});
}

function exitRideMode() {
  rideModeOn = false;
  $("ridemode").hidden = true;
  if (wakeLock) { wakeLock.release().catch(() => {}); wakeLock = null; }
}

document.addEventListener("visibilitychange", async () => {
  // wake lock снимается системой при уходе со страницы — переберём при возврате
  if (rideModeOn && document.visibilityState === "visible" && "wakeLock" in navigator && !wakeLock) {
    try { wakeLock = await navigator.wakeLock.request("screen"); } catch (e) { /* ignore */ }
  }
});

function renderRideMode(state) {
  if (!rideModeOn) return;
  const speed = pnum(state, "2.1");
  const bat = pnum(state, "1.2");
  const range = pnum(state, "1.7");
  const fault = pnum(state, "1.8");
  const locked = pnum(state, "2.2");
  const modeP = prop(state, "1.1");

  // Пока самокат заблокирован — кнопку выхода прячем (страховка от случайного
  // выхода из ride mode, пока самокат заперт); разблокирован — возвращаем.
  $("ridemode-exit").hidden = locked === 1;

  $("rm-speed-val").textContent = speed == null ? "—" : speed.toFixed(1);

  const batEl = $("rm-battery");
  batEl.textContent = bat == null ? "—" : `${Math.round(bat)}%`;
  batEl.style.color = bat == null ? "#fff" : batteryColor(bat);

  $("rm-range").textContent = range == null ? "—" : `${range.toFixed(1)} км`;

  const tripDist = pnum(state, "1.9");                 // CURRENT_MILEAGE (сессия)
  $("rm-trip-dist").textContent = tripDist == null ? "—" : `${tripDist.toFixed(1)} км`;
  const tripTimeP = prop(state, "2.8");                 // RIDING_TIME — берём уже отформатированный текст
  $("rm-trip-time").textContent = tripTimeP && tripTimeP.text ? tripTimeP.text : "—";

  const modeTxt = modeP && modeP.text ? esc(String(modeP.text).replace(/\s*\(raw.*\)/, "")) : null;
  const modeEl = $("rm-mode");
  if (modeTxt) { modeEl.textContent = modeTxt; modeEl.hidden = false; } else { modeEl.hidden = true; }

  // Кнопку замка НЕ пересоздаём через innerHTML каждый тик (renderRideMode
  // вызывается ~раз в секунду) — иначе жест "удержания" (см. ниже) обрывался
  // бы на середине при случайном ре-рендере. Обновляем существующий элемент.
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
      lockBtn.textContent = locked ? "🔒 Заблокирован" : "🔓 Разблокирован";
    }
  }

  const banner = $("rm-fault-banner");
  if (fault) {
    banner.hidden = false;
    banner.textContent = `⚠ ОШИБКА ${fault}`;
  } else {
    banner.hidden = true;
  }
}

// Замок в режиме езды — рабочая кнопка (не просто индикатор): включает режим
// управления (если выключен) и сразу шлёт SET, чтобы не выходить из ride mode.
async function toggleLockFromRideMode(locked, btn) {
  const next = locked ? 0 : 1;
  if (btn) btn.disabled = true;
  try {
    if (locked && !(await verifyPin())) return;   // locked=true -> next=0 -> разблокировка
    await fetch("/api/write_mode", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ enabled: true }),
    });
    const r = await fetch("/api/set", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key: "2.2", value: next }),
    });
    if (!r.ok) {
      const j = await r.json().catch(() => ({}));
      alert(j.error || `не удалось изменить: ${r.status}`);
    }
  } finally {
    if (btn) btn.disabled = false;
  }
}

// Вместо модального confirm() (не вписывается в полноэкранный ride mode,
// выбивается визуально) — жест "удержать ~0.8с". Защищает от случайного
// тапа (тряска/палец в перчатке), не блокируя интерфейс диалогом.
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
  if (lockHoldTimer) {
    clearTimeout(lockHoldTimer);
    lockHoldTimer = null;
  }
  if (lockHoldBtn) {
    lockHoldBtn.classList.remove("holding");
    lockHoldBtn = null;
  }
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

const GROUP_ICONS = {
  ride: "🛴", battery: "🔋", functions: "⚙️", identity: "🪪", logs: "🗒️",
};

function buildGroups(state) {
  const container = $("groups");
  container.innerHTML = "";
  for (const g of state.groups || []) {
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

    for (const pair of g.props || []) {
      const key = pair[0] + "." + pair[1];
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

      card.appendChild(name);
      card.appendChild(value);
      card.appendChild(meta);
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
  for (let i = 1; i <= 5; i++) {
    const p = (state.properties || {})["6." + i];
    if (p && Array.isArray(p.rides)) rides.push(...p.rides);
  }
  if (!rides.length) {
    wrap.innerHTML = '<div class="ride-empty">нет записей о поездках</div>';
    return;
  }
  const head = '<div class="ride-row ride-head"><span>#</span><span>Длительность</span>'
    + '<span>Дистанция</span><span>Ср. скорость</span><span>Макс.</span></div>';
  const rows = rides.map((r, i) =>
    `<div class="ride-row"><span class="ride-idx">${i + 1}</span>`
    + `<span>${esc(r.dur)}</span><span>${esc(r.dist)}</span>`
    + `<span>${esc(r.avg)}</span><span>${esc(r.top)}</span></div>`).join("");
  wrap.innerHTML = head + rows;
}

function updateProps(state) {
  if (!groupsBuilt) buildGroups(state);

  document.querySelectorAll(".prop").forEach((card) => {
    const key = card.dataset.key;
    card.classList.toggle("writable", stateWritable.has(key));
    const p = (state.properties || {})[key];
    const value = card.querySelector(".value");
    const meta = card.querySelector(".meta");

    card.classList.toggle("secret", Boolean(p && p.secret));

    if (!p) {
      value.textContent = "—";
      meta.textContent = "";
      card.classList.remove("has-data");
      return;
    }

    card.classList.add("has-data");
    const newText = p.text || "—";
    value.textContent = newText;
    card.classList.toggle("bool-on", p.text === "вкл");
    card.classList.toggle("bool-off", p.text === "выкл");
    // длинные/описательные строки — мельче и с переносом, числа остаются крупными
    value.classList.toggle("val-text", Boolean(p.text) && p.text.length > 14);
    // живой индикатор: вспышка при РЕАЛЬНОЙ смене значения (не при первом заполнении)
    if (prevValueText[key] !== undefined && prevValueText[key] !== newText) {
      card.classList.remove("flash");
      void card.offsetWidth; // форсируем reflow, чтобы анимация перезапустилась
      card.classList.add("flash");
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

function updateHistory(state) {
  const box = $("history");
  for (const h of state.history || []) {
    if (h.id > lastHistId) {
      lastHistId = h.id;
      const line = document.createElement("div");
      line.className = "line";

      const ts = document.createElement("span");
      ts.className = "ts";
      ts.textContent = h.ts;
      line.appendChild(ts);
      line.appendChild(document.createTextNode("  "));

      const entries = Object.entries(h.vals || {});
      for (const [k, v] of entries.slice(0, 8)) {
        const span = document.createElement("span");
        span.className = "kv";
        span.textContent = `${shortName(k, state)}=${v}`;
        line.appendChild(span);
        line.appendChild(document.createTextNode("  "));
      }
      if (entries.length > 8) {
        const more = document.createElement("span");
        more.className = "dim";
        more.textContent = `+${entries.length - 8}`;
        line.appendChild(more);
      }

      box.appendChild(line);
    }
  }

  while (box.children.length > 150) box.removeChild(box.firstChild);
  box.scrollTop = box.scrollHeight;
  $("histcount").textContent = (state.history || []).length ? `${lastHistId} раунд(ов)` : "";
}

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
      line.appendChild(ts);
      line.appendChild(document.createTextNode(" "));
      line.appendChild(document.createTextNode(e.message || ""));

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

  const running = Boolean(state.running);
  $("start").disabled = running;
  $("stop").disabled = !running;

  $("mode-val").textContent = state.mode || "—";
  $("updated").textContent = state.last_update || "—";
  $("pushes").textContent = String((state.counters && state.counters.pushes) || 0);

  const rx = (state.counters && state.counters.rx) || {};
  const rxEntries = Object.entries(rx);
  $("rx").textContent = rxEntries.length
    ? rxEntries.map(([k, v]) => `${k}:${v}`).join("  ")
    : "∅";

  writeEnabled = Boolean(state.write_enabled);
  stateWritable = new Set(state.writable || []);
  stateConfirm = state.writable_confirm || {};
  stateWritableValues = state.writable_values || {};
  const wb = $("write-toggle");
  wb.textContent = writeEnabled ? "🔓 Управление вкл" : "🔒 Только чтение";
  wb.classList.toggle("on", writeEnabled);
  document.body.classList.toggle("write-on", writeEnabled);
}

async function tick() {
  let state;
  try {
    const r = await fetch("/api/state", { cache: "no-store" });
    state = await r.json();
  } catch (e) {
    $("conn").textContent = "нет связи с сервером";
    $("conn").className = "conn bad";
    return;
  }

  $("conn").textContent = `связь OK · ${state.last_update}`;
  $("conn").className = "conn";

  lastState = state;
  updateControls(state);
  renderHero(state);
  updateProps(state);
  renderRideLog(state);
  updateHistory(state);
  updateEvents(state);
  renderRideMode(state);
}

$("start").onclick = async () => {
  const body = {
    mode: $("mode").value,
    interval: parseFloat($("interval").value),
    static_interval: parseFloat($("static_interval").value),
    mac: selectedMac || undefined,
  };
  lastHistId = 0;
  lastEventId = 0;
  $("history").innerHTML = "";
  $("events").innerHTML = "";

  const r = await fetch("/api/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) {
    const j = await r.json().catch(() => ({}));
    alert(j.error || `start failed: ${r.status}`);
  }
  tick();
};

$("stop").onclick = async () => {
  await fetch("/api/stop", { method: "POST" });
  tick();
};

$("ridemode-toggle").onclick = () => {
  if (rideModeOn) exitRideMode(); else enterRideMode();
};
$("ridemode-exit").onclick = exitRideMode;

$("write-toggle").onclick = async () => {
  const enabled = !writeEnabled;
  if (enabled && !(await showModal(
    "Включить режим управления?",
    "Клик по функции будет менять настройку самоката (SET), пока не выключите обратно."))) {
    return;
  }
  await fetch("/api/write_mode", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ enabled }),
  });
  tick();
};

// клик по разрешённой булевой карточке — переключить настройку (только в режиме управления)
$("groups").addEventListener("click", async (e) => {
  const card = e.target.closest(".prop.writable");
  if (!card) return;
  if (!writeEnabled) {
    alert("Сначала включите режим управления (кнопка «🔒 Только чтение» вверху справа) — иначе клики по настройкам ничего не делают.");
    return;
  }
  const key = card.dataset.key;
  const p = lastState && lastState.properties ? lastState.properties[key] : null;
  const label = shortName(key, lastState || {});
  const vals = stateWritableValues[key];
  let next, curLabel, nextLabel;
  if (Array.isArray(vals) && vals.length) {          // enum-уровень: циклим дальше
    const cur = p && typeof p.num === "number" ? p.num : vals[0][0];
    const idx = vals.findIndex(([v]) => v === cur);
    const [nv, nl] = vals[(idx + 1) % vals.length];
    next = nv;
    nextLabel = nl;
    curLabel = (vals.find(([v]) => v === cur) || [, String(cur)])[1];
  } else {                                            // булев переключатель
    const cur = p && p.text === "вкл" ? 1 : 0;
    next = cur ? 0 : 1;
    curLabel = cur ? "вкл" : "выкл";
    nextLabel = next ? "вкл" : "выкл";
  }
  const confirmMsg = stateConfirm[key];
  const msg = confirmMsg
    ? `${confirmMsg}\n\n${curLabel} → ${nextLabel}`
    : `${curLabel} → ${nextLabel}`;
  if (!(await showModal(label, msg, { danger: Boolean(confirmMsg) }))) return;
  if (key === "2.2" && next === 0 && !(await verifyPin())) return;   // IS_LOCKED -> 0 = разблокировка
  const r = await fetch("/api/set", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ key, value: next }),
  });
  if (!r.ok) {
    const j = await r.json().catch(() => ({}));
    alert(j.error || `set failed: ${r.status}`);
  }
  tick();
});

$("pin-toggle").onclick = managePin;
updatePinButton();
loadScooters();

setInterval(tick, 1000);
tick();
