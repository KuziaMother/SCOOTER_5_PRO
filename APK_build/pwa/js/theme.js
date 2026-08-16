/* Переключатель светлой/тёмной темы. По умолчанию — системная тема
   (prefers-color-scheme, см. style.css); явный выбор кнопкой сохраняется
   в localStorage и переопределяет систему при следующих визитах. */
(function () {
  const KEY = "scooter_theme";
  const btn = document.getElementById("theme-toggle");
  const root = document.documentElement;

  function systemPrefersLight() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches;
  }

  function effectiveTheme() {
    return root.getAttribute("data-theme") || (systemPrefersLight() ? "light" : "dark");
  }

  function paintIcon() {
    btn.textContent = effectiveTheme() === "light" ? "☀️" : "🌙";
  }

  btn.addEventListener("click", () => {
    const next = effectiveTheme() === "light" ? "dark" : "light";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem(KEY, next); } catch (e) {}
    paintIcon();
  });

  paintIcon();
})();
