const CACHE_PREFIX = 'ttod-pwa-stub-';
const CACHE_NAME = `${CACHE_PREFIX}v2`;
const PROOF_ASSET = '/visual-system/tokens.css';

self.addEventListener('install', (event) => {
  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      await cache.add(PROOF_ASSET);

      // Activate this minimal worker without waiting for tabs to close.
      await self.skipWaiting();
    })()
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      const cacheNames = await caches.keys();

      // Remove previous PWA cache versions, preserving unrelated caches.
      await Promise.all(
        cacheNames
          .filter(
            (name) =>
              name.startsWith(CACHE_PREFIX) && name !== CACHE_NAME
          )
          .map((name) => caches.delete(name))
      );

      // Let the activated worker control already-open pages.
      await self.clients.claim();
    })()
  );
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  if (
    event.request.method !== 'GET' ||
    url.origin !== self.location.origin ||
    url.pathname !== PROOF_ASSET
  ) {
    return;
  }

  event.respondWith(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      const cachedResponse = await cache.match(event.request);

      return cachedResponse ?? fetch(event.request);
    })()
  );
});