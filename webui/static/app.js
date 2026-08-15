/* Scooter 5 Pro web UI — client logic (kept separate from HTML/CSS/Python). */
const $ = (id) => document.getElementById(id);

let lastHistId = 0;
let lastEventId = 0;
let groupsBuilt = false;

function esc(s) {
  return String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}

function shortName(key, state) {
  return (state.names && state.names[key]) || key;
}

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

function updateProps(state) {
  if (!groupsBuilt) buildGroups(state);

  document.querySelectorAll(".prop").forEach((card) => {
    const key = card.dataset.key;
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
    value.textContent = p.text || "—";
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

  updateControls(state);
  updateProps(state);
  updateHistory(state);
  updateEvents(state);
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

setInterval(tick, 1000);
tick();
