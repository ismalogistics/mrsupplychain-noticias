/* Mr. Supply Chain México · service worker (alcance: todo el sitio).
   Páginas y datos: primero la red (siempre lo más reciente); si no hay señal, la última copia guardada.
   Estilos, scripts e imágenes: copia guardada y se actualiza en segundo plano. */
const V = 'msc-v1';
const OFFLINE = '/noticias/app/offline.html';
const PRE = [OFFLINE, '/noticias/app/icon-192.png'];
const MAX_PAGES = 60;

self.addEventListener('install', e => {
  e.waitUntil(caches.open(V + '-core').then(c => c.addAll(PRE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => !k.startsWith(V)).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});

async function trim(name, max) {
  const c = await caches.open(name); const ks = await c.keys();
  for (let i = 0; i < ks.length - max; i++) await c.delete(ks[i]);
}
async function networkFirst(req, name, fallback) {
  const c = await caches.open(name);
  try {
    const r = await fetch(req);
    if (r && r.ok && r.type === 'basic') { c.put(req, r.clone()); if (name.endsWith('pages')) trim(name, MAX_PAGES); }
    return r;
  } catch (err) {
    const hit = await c.match(req, { ignoreSearch: name.endsWith('pages') });
    if (hit) return hit;
    if (fallback) return (await caches.match(fallback)) || Response.error();
    return Response.error();
  }
}
async function staleWhileRevalidate(req) {
  const c = await caches.open(V + '-static');
  const hit = await c.match(req);
  const net = fetch(req).then(r => { if (r && r.ok && r.type === 'basic') c.put(req, r.clone()); return r; }).catch(() => hit);
  return hit || net;
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin || url.pathname.startsWith('/cdn-cgi/')) return;
  if (req.mode === 'navigate') { e.respondWith(networkFirst(req, V + '-pages', OFFLINE)); return; }
  if (/\/data\/.+\.json$/.test(url.pathname) || url.pathname.endsWith('.xml')) { e.respondWith(networkFirst(req, V + '-data')); return; }
  if (/\.(css|js|png|jpe?g|svg|webp|gif|woff2?|ico)$/.test(url.pathname)) { e.respondWith(staleWhileRevalidate(req)); return; }
});
