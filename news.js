/* Mr. Supply Chain® · Noticias — lee data/latest.json e data/index.json (mismo origen; compatible con la CSP del sitio). */
(function () {
  'use strict';
  var BASE = 'data/';
  var state = { lang: 'es', tab: 'global', latest: null, index: null, cache: {} };
  var MES = { es: ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'], en: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] };
  var MOM = { es: { apertura: 'Apertura', mediodia: 'Mediodía', cierre: 'Cierre' }, en: { apertura: 'Open', mediodia: 'Midday', cierre: 'Close' } };
  var MKT = { es: { global: 'Global', mexico: 'México' }, en: { global: 'Global', mexico: 'Mexico' } };
  var TXT = {
    es: { scm: 'Para supply chain', wk: 'Para el fin de semana', src: 'Fuentes', upd: 'Actualizado', none: 'Todavía no hay briefs anteriores.', err: 'No se pudieron cargar las noticias. Intenta de nuevo en unos minutos.' },
    en: { scm: 'For supply chain', wk: 'For the weekend', src: 'Sources', upd: 'Updated', none: 'No earlier briefs yet.', err: 'News could not be loaded. Please try again in a few minutes.' }
  };
  var COLORS = ['#1e5fa8', '#a83246', '#1f8a5b', '#b87514', '#5b3fb8'];

  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }
  function t(k) { return TXT[state.lang][k]; }
  function fmtDate(iso) { var p = String(iso).slice(0, 10).split('-'); return state.lang === 'es' ? (+p[2]) + ' ' + MES.es[+p[1] - 1] + ' ' + p[0] : MES.en[+p[1] - 1] + ' ' + (+p[2]) + ', ' + p[0]; }
  function num(v, d) { return Number(v).toLocaleString(state.lang === 'es' ? 'es-MX' : 'en-US', { minimumFractionDigits: d, maximumFractionDigits: d }); }

  function getLang() { try { var l = localStorage.getItem('lang'); if (l === 'en' || l === 'es') return l; } catch (e) {} return (navigator.language || 'es').slice(0, 2) === 'en' ? 'en' : 'es'; }
  function applyLang() {
    document.documentElement.lang = state.lang;
    var spans = document.querySelectorAll('[data-lang]');
    for (var i = 0; i < spans.length; i++) spans[i].style.display = spans[i].getAttribute('data-lang') === state.lang ? 'inline' : 'none';
    var bs = document.querySelectorAll('[data-setlang]');
    for (var j = 0; j < bs.length; j++) bs[j].setAttribute('aria-pressed', String(bs[j].getAttribute('data-setlang') === state.lang));
  }

  function fetchJSON(path) {
    return fetch(BASE + path + '?v=' + Math.floor(Date.now() / 300000), { cache: 'no-store' }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
  }

  function briefNode(b, withMeta) {
    var L = b[state.lang] || b.es; var frag = document.createDocumentFragment();
    if (withMeta) {
      var meta = el('div', 'nx-meta');
      meta.appendChild(el('span', 'nx-pill', MOM[state.lang][b.momento] || b.momento));
      meta.appendChild(el('span', null, MKT[state.lang][b.mercado] + ' · ' + fmtDate(b.fecha) + ' · ' + b.hora));
      frag.appendChild(meta);
      frag.appendChild(el('h3', null, L.titular));
    }
    var blocks = el('div', 'nx-blocks');
    (L.bloques || []).forEach(function (x) { var d = el('div', 'nx-blk'); d.appendChild(el('div', 'k', x.t)); d.appendChild(el('p', null, x.x)); blocks.appendChild(d); });
    frag.appendChild(blocks);
    if (L.scm) { var s = el('div', 'nx-scm'); s.appendChild(el('div', 'k', b.fin_de_semana ? t('wk') : t('scm'))); s.appendChild(el('p', null, L.scm)); frag.appendChild(s); }
    if (b.fuentes && b.fuentes.length) {
      var p = el('p', 'nx-src'); p.appendChild(document.createTextNode(t('src') + ': '));
      b.fuentes.forEach(function (f, i) { var a = el('a', null, f.t); a.href = f.u; a.target = '_blank'; a.rel = 'noopener nofollow'; p.appendChild(a); if (i < b.fuentes.length - 1) p.appendChild(document.createTextNode(' · ')); });
      frag.appendChild(p);
    }
    return frag;
  }

  function renderStamp() {
    var s = document.getElementById('nx-stamp'); if (!s || !state.latest) return;
    s.replaceChildren();
    var d = new Date(state.latest.actualizado);
    var hh = d.toLocaleTimeString(state.lang === 'es' ? 'es-MX' : 'en-US', { hour: '2-digit', minute: '2-digit', timeZone: 'America/Mexico_City' });
    s.appendChild(document.createTextNode(t('upd') + ': '));
    s.appendChild(el('b', null, fmtDate(state.latest.actualizado) + ' · ' + hh + ' CDMX'));
    s.appendChild(document.createTextNode(' · ' + (MOM[state.lang][state.latest.momento] || '')));
  }
  function renderTicker() {
    var box = document.getElementById('nx-ticker'); if (!box || !state.latest) return;
    box.replaceChildren();
    var track = el('div', 'nx-track');
    function card(r, dup) {
      var c = el('div', 'nx-tk');
      if (dup) c.setAttribute('aria-hidden', 'true');
      c.appendChild(el('span', 'n', state.lang === 'en' ? (r.name_en || r.nombre) : r.nombre));
      var v = el('span', 'v');
      var val = r.grupo === 'bono' ? num(r.valor, 2) + '%' : r.grupo === 'divisa' ? num(r.valor, r.valor > 100 ? 2 : 4) : num(r.valor, r.valor >= 1000 ? 0 : 2);
      v.appendChild(document.createTextNode(val + ' '));
      if (r.cambio != null) {
        var cls = r.cambio > 0 ? 'up' : r.cambio < 0 ? 'down' : 'flat';
        var txt = (r.cambio > 0 ? '+' : '') + (r.grupo === 'bono' ? num(r.cambio, 0) + (state.lang === 'en' ? ' bp' : ' pb') : num(r.cambio, 2) + '%');
        v.appendChild(el('span', 'nx-chg ' + cls, txt));
      }
      c.appendChild(v); return c;
    }
    var rows = state.latest.mercados || [];
    rows.forEach(function (r) { track.appendChild(card(r, false)); });
    rows.forEach(function (r) { track.appendChild(card(r, true)); });
    track.style.setProperty('--nx-dur', Math.max(30, rows.length * 4) + 's');
    box.appendChild(track);
  }
  function renderBrief() {
    var box = document.getElementById('nx-brief'); if (!box || !state.latest) return;
    box.replaceChildren();
    var b = state.latest.briefs && state.latest.briefs[state.tab];
    if (b) box.appendChild(briefNode(b, true));
  }
  function renderLectura() {
    var L = state.latest && state.latest.lectura && (state.latest.lectura[state.lang] || state.latest.lectura.es);
    var v = document.getElementById('nx-verd'), box = document.getElementById('nx-themes');
    if (!L || !v || !box) return;
    v.textContent = L.titular;
    box.replaceChildren();
    (L.temas || []).forEach(function (x, i) { var c = el('div', 'nx-th'); c.style.setProperty('--c', COLORS[i % COLORS.length]); c.appendChild(el('b', null, x.tema)); c.appendChild(el('p', null, x.x)); box.appendChild(c); });
  }
  function renderFeed() {
    var ul = document.getElementById('nx-feed'); if (!ul || !state.index) return;
    ul.replaceChildren();
    var current = state.latest && state.latest.briefs ? [state.latest.briefs.global && state.latest.briefs.global.id, state.latest.briefs.mexico && state.latest.briefs.mexico.id] : [];
    var items = (state.index.items || []).filter(function (x) { return current.indexOf(x.id) < 0; });
    if (!items.length) { ul.appendChild(el('li', 'nx-empty', t('none'))).style.padding = '14px 18px'; return; }
    items.forEach(function (x) {
      var li = el('li');
      var h = el('button', 'h'); h.type = 'button'; h.setAttribute('aria-expanded', 'false');
      h.appendChild(el('span', 'd', fmtDate(x.fecha) + ' · ' + (MOM[state.lang][x.momento] || x.momento) + ' · ' + MKT[state.lang][x.mercado]));
      h.appendChild(el('span', 't', state.lang === 'en' ? (x.titular_en || x.titular_es) : x.titular_es));
      var body = el('div', 'body'); body.hidden = true;
      h.addEventListener('click', function () {
        var open = body.hidden; body.hidden = !open; h.setAttribute('aria-expanded', String(open));
        if (open && !body.firstChild) {
          var load = state.cache[x.id] ? Promise.resolve(state.cache[x.id]) : fetchJSON('briefs/' + x.id + '.json').then(function (b) { state.cache[x.id] = b; return b; });
          load.then(function (b) { body.replaceChildren(briefNode(b, false)); }).catch(function () { body.textContent = t('err'); });
        }
      });
      li.appendChild(h); li.appendChild(body); ul.appendChild(li);
    });
  }
  function renderAll() { applyLang(); renderStamp(); renderTicker(); renderBrief(); renderLectura(); renderFeed(); }

  function init() {
    state.lang = getLang();
    applyLang();
    var bs = document.querySelectorAll('[data-setlang]');
    for (var i = 0; i < bs.length; i++) bs[i].addEventListener('click', function (e) {
      state.lang = e.currentTarget.getAttribute('data-setlang');
      try { localStorage.setItem('lang', state.lang); } catch (err) {}
      renderAll();
    });
    var tabs = document.querySelectorAll('.nx-tabs button');
    for (var k = 0; k < tabs.length; k++) tabs[k].addEventListener('click', function (e) {
      state.tab = e.currentTarget.getAttribute('data-tab');
      for (var m = 0; m < tabs.length; m++) tabs[m].setAttribute('aria-selected', String(tabs[m] === e.currentTarget));
      renderBrief();
    });
    window.addEventListener('storage', function (e) { if (e.key === 'lang' && (e.newValue === 'es' || e.newValue === 'en')) { state.lang = e.newValue; renderAll(); } });
    Promise.all([fetchJSON('latest.json'), fetchJSON('index.json').catch(function () { return { items: [] }; })])
      .then(function (res) { state.latest = res[0]; state.index = res[1]; renderAll(); })
      .catch(function () { var b = document.getElementById('nx-brief'); if (b) b.textContent = t('err'); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
