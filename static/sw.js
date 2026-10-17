const CACHE_NAME = "goc-doc-v1";

const APP_FILES = [
  "/",
  "/static/style.css",
  "/static/manifest.json",
  "/static/icon-192.png",
  "/static/icon-512.png",
];

// Lưu giao diện khi service worker được cài
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(APP_FILES);
    }),
  );
});

// Xóa bộ nhớ giao diện của phiên bản cũ
self.addEventListener("activate", (event) => {
  event.waitUntil(
    (async () => {
      const names = await caches.keys();

      await Promise.all(
        names
          .filter((name) => name.startsWith("goc-doc-") && name !== CACHE_NAME)
          .map((name) => caches.delete(name)),
      );

      await self.clients.claim();
    })(),
  );
});

// Giao diện lấy từ bộ nhớ trước
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);

  if (event.request.method !== "GET") return;
  if (url.origin !== self.location.origin) return;

  // Tin tức luôn do phần JavaScript gọi qua mạng
  if (url.pathname.startsWith("/api/")) return;

  const laTrangChu = event.request.mode === "navigate" && url.pathname === "/";

  const laFileGiaoDien = APP_FILES.includes(url.pathname);

  if (!laTrangChu && !laFileGiaoDien) return;

  event.respondWith(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      const key = laTrangChu ? "/" : url.pathname;
      const saved = await cache.match(key);

      if (saved) return saved;

      const response = await fetch(event.request);

      if (response.ok) {
        await cache.put(key, response.clone());
      }

      return response;
    })(),
  );
});
