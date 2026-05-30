// Royal 888 Service Worker v3 — Champagne edition
const CACHE = 'royal888-v3';
const APP_SHELL = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png',
];

const CDN_PATTERNS = [
  /^https:\/\/cdn\.tailwindcss\.com/,
  /^https:\/\/unpkg\.com\//,
  /^https:\/\/fonts\.googleapis\.com\//,
  /^https:\/\/fonts\.gstatic\.com\//,
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(APP_SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    Promise.all([
      // Delete ALL old caches (not just non-current)
      caches.keys().then(keys =>
        Promise.all(keys.filter(k => k !== CACHE).map(k => {
          console.log('[SW] Deleting old cache:', k);
          return caches.delete(k);
        }))
      ),
      self.clients.claim()
    ])
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  const isCDN = CDN_PATTERNS.some(p => p.test(req.url));
  const isApp = url.origin === self.location.origin;
  const isIcon = /icon.*\.png$/i.test(url.pathname) || url.pathname.endsWith('manifest.json');

  if (isApp || isCDN) {
    // Network-first for icons + manifest — always grab latest
    if (isIcon) {
      e.respondWith(
        fetch(req).then(resp => {
          if (resp && resp.status === 200) {
            const copy = resp.clone();
            caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
          }
          return resp;
        }).catch(() => caches.match(req))
      );
      return;
    }
    // Cache-first for everything else (with background refresh)
    e.respondWith(
      caches.match(req).then(cached => {
        if (cached) {
          fetch(req).then(resp => {
            if (resp && resp.status === 200) {
              caches.open(CACHE).then(c => c.put(req, resp.clone())).catch(() => {});
            }
          }).catch(() => {});
          return cached;
        }
        return fetch(req).then(resp => {
          if (resp && resp.status === 200 && (resp.type === 'basic' || resp.type === 'cors')) {
            const copy = resp.clone();
            caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
          }
          return resp;
        }).catch(() => {
          if (req.mode === 'navigate') {
            return caches.match('./index.html');
          }
        });
      })
    );
  }
});

self.addEventListener('message', e => {
  if (e.data === 'skipWaiting') self.skipWaiting();
});
