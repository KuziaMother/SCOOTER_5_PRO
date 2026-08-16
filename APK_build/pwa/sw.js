// Минимальный service worker — только для критерия устанавливаемости PWA.
// Намеренно НЕ кэширует ничего: протокол/крипта должны всегда грузиться
// свежими, подмена версии молча из кэша здесь недопустима.
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));
self.addEventListener("fetch", (event) => {
  event.respondWith(fetch(event.request));
});
