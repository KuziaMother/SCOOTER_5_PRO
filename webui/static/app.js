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

  const chips = [];
  if (locked != null) {
    chips.push(`<button type="button" class="rm-chip rm-lock-btn ${locked ? "bad" : "ok"}"
        data-locked="${locked ? 1 : 0}">${locked ? "🔒 Заблокирован" : "🔓 Разблокирован"}</button>`);
  }
  $("rm-chips").innerHTML = chips.join("");

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
  if (!confirm(next ? "Заблокировать самокат?" : "Разблокировать самокат?")) return;
  if (btn) btn.disabled = true;
  try {
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

$("rm-chips").addEventListener("click", (e) => {
  const btn = e.target.closest(".rm-lock-btn");
  if (!btn) return;
  toggleLockFromRideMode(btn.dataset.locked === "1", btn);
});

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
  if (enabled && !confirm(
    "Включить режим управления?\nКлик по функции будет МЕНЯТЬ настройку самоката (SET, необратимо до обратного клика).")) {
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
  if (!card || !writeEnabled) return;
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
  if (confirmMsg && !confirm(confirmMsg)) return;
  if (!confirm(`${label}: ${curLabel} → ${nextLabel}?`)) return;
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

setInterval(tick, 1000);
tick();
