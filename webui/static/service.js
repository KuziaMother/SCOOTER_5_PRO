/* Страница «Сервис»: проверка/скачивание прошивки из Mi Cloud, заливка по BLE
   с прогрессом, переключение (switchFirmware) — отдельным явным шагом.
   Логика намеренно самостоятельная (не делит модуль с app.js), но повторяет
   те же паттерны (модалка, карточки списка) для единообразия. */
const $ = (id) => document.getElementById(id);
const SELECTED_MAC_KEY = "scooter_selected_mac";

function esc(s) {
  return String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}

// ---- модалка подтверждения (тот же паттерн, что webui/static/app.js) ----
// infoOnly:true — прячет "Отмена", один OK, как замена alert(): нативный
// alert() легко принять за "ничего не произошло" (не вписан в дизайн,
// нет истории показанных сообщений), плюс где-то может быть заблокирован.
function showModal(title, message, opts = {}) {
  const { danger = false, okText = "Confirm", infoOnly = false } = opts;
  return new Promise((resolve) => {
    const overlay = $("modal-overlay");
    const okBtn = $("modal-ok");
    const cancelBtn = $("modal-cancel");
    $("modal-title").textContent = title;
    $("modal-msg").textContent = message;
    okBtn.textContent = okText;
    okBtn.classList.toggle("danger", danger);
    cancelBtn.hidden = infoOnly;
    overlay.hidden = false;

    function cleanup(result) {
      overlay.hidden = true;
      cancelBtn.hidden = false;
      okBtn.removeEventListener("click", onOk);
      cancelBtn.removeEventListener("click", onCancel);
      overlay.removeEventListener("click", onOverlay);
      document.removeEventListener("keydown", onKey);
      resolve(result);
    }
    function onOk() { cleanup(true); }
    function onCancel() { cleanup(false); }
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

function showInfo(title, message, opts = {}) {
  return showModal(title, message, { ...opts, infoOnly: true, okText: "OK" });
}

function getTargetMac() {
  return localStorage.getItem(SELECTED_MAC_KEY) || "";
}

function renderTargetMac() {
  const isEn = window.I18N && window.I18N.getLang() === "en";
  $("fw-target-mac").textContent = getTargetMac() || (isEn ? "not selected" : "не выбран");
}

// ---- предупреждение о занятом BLE-соединении. Раньше это вылезало только
// ПОСЛЕ подтверждения модалки "Прошить" (409 от сервера) — легко принять
// за "ничего не произошло". Теперь видно заранее, ДО того как жать "Прошить". ----
let mainSessionRunning = false;

async function checkMainSession() {
  try {
    const r = await fetch("/api/state");
    const j = await r.json();
    mainSessionRunning = Boolean(j.running);
  } catch (e) {
    mainSessionRunning = false;
  }
  const isEn = window.I18N && window.I18N.getLang() === "en";
  $("fw-session-text").textContent = mainSessionRunning
    ? (isEn
        ? "⚠ Active BLE session (polling) on main page — stop it before flashing: one BLE connection per process."
        : "⚠ На главной странице активна BLE-сессия (поллинг) — остановите её, прежде чем прошивать: одно BLE-соединение на процесс.")
    : "";
  $("fw-session-banner").hidden = !mainSessionRunning;
}

$("fw-session-stop").onclick = async () => {
  const btn = $("fw-session-stop");
  btn.disabled = true;
  btn.textContent = "Stopping…";
  try {
    const r = await fetch("/api/stop", { method: "POST" });
    const j = await r.json();
    if (!j.ok && r.status !== 409) {
      await showInfo("Failed to stop", j.error || "unknown error");
    }
    // остановка не мгновенна (воркер завершается асинхронно) — подождём,
    // пока running реально станет false, вместо немедленного разового чека
    for (let i = 0; i < 10; i++) {
      await checkMainSession();
      if (!mainSessionRunning) break;
      await new Promise((res) => setTimeout(res, 500));
    }
  } catch (e) {
    await showInfo("Failed to stop", e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = "Stop polling";
  }
};

async function loadInstalled() {
  const r = await fetch("/api/firmware/installed");
  const j = await r.json();
  $("fw-installed-ble").textContent = j.ble || "—";
  $("fw-installed-bms").textContent = j.bms || "—";
}

// ---- проверка обновления в Mi Cloud ----
$("fw-check-btn").onclick = async () => {
  const mac = getTargetMac();
  if (!mac) { await showInfo("Scooter not selected", "Select a scooter on the main page first ('My Scooters')."); return; }
  const btn = $("fw-check-btn");
  const orig = btn.textContent;
  btn.disabled = true;
  btn.textContent = "Checking…";
  $("fw-check-results").innerHTML = "";
  try {
    const r = await fetch("/api/firmware/check", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mac }),
    });
    const j = await r.json();
    if (!j.ok) {
      if (String(j.error || "").includes("Mi Cloud")) {
        await showInfo("Mi Cloud login required",
          `${j.error}\n\nLog in on the main page: 'My Scooters' → 🔑 → 'Show QR for login'.`);
      } else {
        await showInfo("Failed to check", j.error || "unknown error");
      }
      return;
    }
    renderCheckResults(j.entries || []);
  } finally {
    btn.disabled = false;
    btn.textContent = orig;
  }
};

function renderCheckResults(entries) {
  const box = $("fw-check-results");
  box.innerHTML = "";
  if (!entries.length) {
    const isEn = window.I18N && window.I18N.getLang() === "en";
    box.innerHTML = `<div class="scooter-mac">${isEn ? "No cloud firmware images returned for this device." : "Облако не вернуло образов для этого устройства."}</div>`;
    return;
  }
  for (const e of entries) {
    const row = document.createElement("div");
    row.className = "scooter-row";
    const info = document.createElement("div");
    info.className = "scooter-info";
    const name = document.createElement("div");
    name.className = "scooter-name";
    name.textContent = `${e.type === "mcu" ? "MCU" : "BLE"} ${e.version || "?"}`;
    const meta = document.createElement("div");
    meta.className = "scooter-mac";
    meta.textContent = `md5 ${e.md5 || "?"}${e.downloaded ? " · already downloaded" : ""}`;
    info.append(name, meta);

    const actions = document.createElement("div");
    actions.className = "scooter-actions";
    if (e.downloaded) {
      const tag = document.createElement("span");
      tag.className = "scooter-mac";
      tag.textContent = "ready";
      actions.appendChild(tag);
    } else {
      const dlBtn = document.createElement("button");
      dlBtn.type = "button";
      dlBtn.className = "modal-btn scooter-select";
      dlBtn.textContent = "Download";
      dlBtn.onclick = async () => {
        dlBtn.disabled = true;
        dlBtn.textContent = "Downloading…";
        const r = await fetch("/api/firmware/download", {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url: e.url, md5: e.md5, type: e.type }),
        });
        const j = await r.json();
        if (!j.ok) {
          await showInfo("Failed to download", j.error || "unknown error");
          dlBtn.disabled = false; dlBtn.textContent = "Download"; return;
        }
        e.downloaded = true;
        renderCheckResults(entries);
        await loadLocalList();
      };
      actions.appendChild(dlBtn);
    }
    row.append(info, actions);
    box.appendChild(row);
  }
}

// ---- локальное хранилище скачанных образов ----
async function loadLocalList() {
  const r = await fetch("/api/firmware/local");
  const j = await r.json();
  renderLocalList(j.items || []);
}

function renderLocalList(items) {
  const box = $("fw-local-list");
  box.innerHTML = "";
  if (!items.length) {
    const isEn = window.I18N && window.I18N.getLang() === "en";
    box.innerHTML = `<div class="scooter-mac">${isEn ? "Nothing downloaded yet." : "Пока ничего не скачано."}</div>`;
    return;
  }
  for (const it of items) {
    const row = document.createElement("div");
    row.className = "scooter-row";
    const info = document.createElement("div");
    info.className = "scooter-info";
    const name = document.createElement("div");
    name.className = "scooter-name";
    name.textContent = `${it.type === "mcu" ? "MCU" : "BLE"} · ${it.filename}`;
    const meta = document.createElement("div");
    meta.className = "scooter-mac";
    meta.textContent = `${(it.size / 1024).toFixed(0)} KB · md5 ${it.md5}`;
    info.append(name, meta);

    const actions = document.createElement("div");
    actions.className = "scooter-actions";
    const flashBtn = document.createElement("button");
    flashBtn.type = "button";
    flashBtn.className = "modal-btn danger";
    flashBtn.textContent = "Flash";
    flashBtn.onclick = () => startFlashFlow(it);
    actions.appendChild(flashBtn);

    row.append(info, actions);
    box.appendChild(row);
  }
}

// ---- заливка (upload) + отдельное переключение (commit) ----
let pollTimer = null;

async function startFlashFlow(item) {
  const mac = getTargetMac();
  if (!mac) { await showInfo("No scooter selected", "Please select a scooter on the main page first (\"My Scooters\")."); return; }
  await checkMainSession();
  if (mainSessionRunning) {
    await showInfo("Stop polling first",
      "Active BLE session on main page — stop it with 'Stop' button before flashing (one BLE connection per process).");
    return;
  }
  const ok = await showModal(
    "Flash scooter?",
    `Uploading ${item.type === "mcu" ? "MCU" : "BLE"} firmware image (md5 ${item.md5}) to ${mac}.\n\n` +
    "This is only an UPLOAD into the device buffer — firmware will NOT switch yet until explicitly triggered. Ensure battery is charged and connection is stable.",
    { danger: true, okText: "Flash" });
  if (!ok) return;

  const r = await fetch("/api/firmware/flash/start", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mac, filename: item.filename, target: item.target }),
  });
  const j = await r.json();
  if (!j.ok) { await showInfo("Failed to start flashing", j.error || "unknown error"); return; }
  $("fw-progress-panel").hidden = false;
  resetFlashLog();
  pollFlashStatus(mac, item);
}

function pollFlashStatus(mac, item) {
  if (pollTimer) clearInterval(pollTimer);
  pollTimer = setInterval(async () => {
    const st = await (await fetch("/api/firmware/flash/status")).json();
    renderProgress(st, mac, item);
    if (!st.running && (st.phase === "done" || st.phase === "error")) {
      clearInterval(pollTimer);
      pollTimer = null;
    }
  }, 1000);
}

// ---- построчный лог заливки (аналог "Событий" на главной странице) —
// новая строка добавляется только когда сообщение реально изменилось,
// иначе за секундные тики один и тот же статус дублировался бы. ----
let lastLoggedKey = null;

function resetFlashLog() {
  $("fw-log").innerHTML = "";
  lastLoggedKey = null;
}

function appendFlashLog(st) {
  const key = `${st.phase}|${st.message}`;
  if (key === lastLoggedKey) return;
  lastLoggedKey = key;
  const box = $("fw-log");
  const line = document.createElement("div");
  line.className = "line";
  const ts = new Date().toLocaleTimeString("ru-RU");
  line.textContent = `${ts}  [${st.phase}] ${st.message || ""}`;
  box.appendChild(line);
  box.scrollTop = box.scrollHeight;
  loadHistoryLog();
}

function renderProgress(st, mac, item) {
  appendFlashLog(st);

  const body = $("fw-progress-body");
  const pct = st.total ? Math.round((100 * st.index) / st.total) : 0;
  let html = `<div class="scooter-mac">${esc(st.phase)} — ${esc(st.message || "")}</div>`;
  if (st.total) {
    html += `<div style="background:var(--bg-elev);border-radius:8px;overflow:hidden;height:10px;margin:8px 0;">
      <div style="width:${pct}%;height:100%;background:var(--accent);"></div>
    </div>
    <div class="scooter-mac">${st.index}/${st.total} (${pct}%) ok=${st.ok} bad=${st.bad} ${st.speed_kbps} KB/s</div>`;
  }
  if (st.error) html += `<div class="scooter-mac" style="color:var(--bad);">Error: ${esc(st.error)}</div>`;
  body.innerHTML = html;

  // Кнопка "Переключить" — только после успешной ЗАЛИВКИ (commit:false), не
  // после самого переключения: то же phase="done"+success срабатывает и на
  // финише commit-прогона, а второй раз switchFirmware слать незачем и
  // небезопасно приглашать к этому пользователя.
  if (!st.running && !st.commit && st.phase === "done" && st.success) {
    const commitBtn = document.createElement("button");
    commitBtn.id = "fw-commit-btn";
    commitBtn.type = "button";
    commitBtn.className = "modal-btn danger";
    commitBtn.textContent = "⚠ Switch firmware (irreversible)";
    commitBtn.style.marginTop = "12px";
    commitBtn.onclick = () => startCommitFlow(mac, item);
    body.appendChild(commitBtn);
  }
}

async function startCommitFlow(mac, item) {
  await checkMainSession();
  if (mainSessionRunning) {
    await showInfo("Stop polling first",
      "Active BLE session on main page — stop it with 'Stop' button before flashing (one BLE connection per process).");
    return;
  }
  const ok = await showModal(
    "Switch firmware?",
    "IRREVERSIBLE operation (risk of bricking if disconnected during switch) — device will reboot and apply new firmware. Ensure battery level is sufficient and connection is stable before continuing.",
    { danger: true, okText: "Switch" });
  if (!ok) return;
  const r = await fetch("/api/firmware/flash/commit", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mac, filename: item.filename, target: item.target }),
  });
  const j = await r.json();
  if (!j.ok) { await showInfo("Failed to trigger firmware switch", j.error || "unknown error"); return; }
  pollFlashStatus(mac, item);
}

async function resumeIfFlashing() {
  const st = await (await fetch("/api/firmware/flash/status")).json();
  if (st.phase !== "idle") {
    $("fw-progress-panel").hidden = false;
    const mac = getTargetMac();
    const item = { filename: st.filename, target: st.target };
    renderProgress(st, mac, item);
    if (st.running) pollFlashStatus(mac, item);
  }
}

async function loadHistoryLog() {
  const r = await fetch("/api/firmware/flash/log");
  const j = await r.json();
  const box = $("fw-history-log");
  box.innerHTML = "";
  for (const e of j.entries || []) {
    const line = document.createElement("div");
    line.className = "line";
    const mac = e.mac ? ` ${e.mac}` : "";
    const target = e.target ? ` ${e.target === "mcu" ? "MCU" : "BLE"}` : "";
    const commit = e.commit ? " commit" : "";
    const progress = e.total ? ` ${e.index}/${e.total} ok=${e.ok} bad=${e.bad}` : "";
    const err = e.error ? ` error: ${e.error}` : "";
    line.textContent = `${e.ts}${mac}${target}${commit} [${e.phase}] ${e.message || ""}${progress}${err}`;
    box.appendChild(line);
  }
  box.scrollTop = box.scrollHeight;
}

renderTargetMac();
loadInstalled();
loadLocalList();
loadHistoryLog();
resumeIfFlashing();
checkMainSession();
setInterval(checkMainSession, 3000);

if (window.I18N) {
  window.I18N.onLanguageChange(() => {
    renderTargetMac();
    checkMainSession();
    loadLocalList();
  });
}
