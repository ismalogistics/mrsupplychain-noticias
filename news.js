/* Mr. Supply Chain® · Noticias — portal. Lee data/*.json del mismo origen (compatible con la CSP del sitio). */
(function () {
  'use strict';
  var BASE = 'data/';
  var NS = 'http://www.w3.org/2000/svg';
  var state = { lang: 'es', tab: 'global', latest: null, index: null, series: null, world: null, heat: null, trends: null, heatIdx: { global: 'sp500', mexico: 'ipc' }, cache: {} };
  var MES = { es: ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'], en: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] };
  var MOM = { es: { apertura: 'Apertura', mediodia: 'Mediodía', cierre: 'Cierre' }, en: { apertura: 'Open', mediodia: 'Midday', cierre: 'Close' } };
  var MKT = { es: { global: 'Global', mexico: 'México' }, en: { global: 'Global', mexico: 'Mexico' } };
  var TXT = {
    es: { scm: 'Para supply chain', wk: 'Para el fin de semana', wkk: 'Edición de fin de semana', src: 'Fuentes', upd: 'Actualizado', none: 'Todavía no hay briefs anteriores.', err: 'No se pudieron cargar las noticias. Intenta de nuevo en unos minutos.', by: 'Mesa de mercados Mr. Supply Chain', read: 'Leer la nota', figG: 'Bolsas del día', figM: 'México hoy', noag: 'Sin eventos próximos registrados.', tasa: 'Tasa', infl: 'Inflación', banx: 'Tasa Banxico' },
    en: { scm: 'For supply chain', wk: 'For the weekend', wkk: 'Weekend edition', src: 'Sources', upd: 'Updated', none: 'No earlier briefs yet.', err: 'News could not be loaded. Please try again in a few minutes.', by: 'Mr. Supply Chain markets desk', read: 'Read the story', figG: 'Stock markets today', figM: 'Mexico today', noag: 'No upcoming events listed.', tasa: 'Rate', infl: 'Inflation', banx: 'Banxico rate' }
  };
  var COLORS = ['#1e5fa8', '#a83246', '#1f8a5b', '#b87514', '#5b3fb8'];
  var CITY = { 'IPC BMV': [-99.13, 19.43, 'CDMX'], 'S&P 500': [-74.0, 40.71, 'Nueva York'], 'Euro Stoxx 50': [8.68, 50.11, 'Fráncfort'], 'Nikkei 225': [139.69, 35.69, 'Tokio'], 'KOSPI': [126.98, 37.57, 'Seúl', 'left', -16] };
  var CITY_EN = { 'CDMX': 'Mexico City', 'Nueva York': 'New York', 'Fráncfort': 'Frankfurt', 'Tokio': 'Tokyo', 'Seúl': 'Seoul' };
  var HL = { '484': 1, '840': 1, '392': 1, '410': 1, '276': 1, '250': 1, '380': 1, '724': 1, '528': 1, '056': 1, '040': 1, '620': 1, '372': 1, '246': 1, '300': 1 };

  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }
  function sv(tag, attrs, text) { var n = document.createElementNS(NS, tag); for (var k in attrs) n.setAttribute(k, attrs[k]); if (text != null) n.textContent = text; return n; }
  function t(k) { return TXT[state.lang][k]; }
  function loc() { return state.lang === 'es' ? 'es-MX' : 'en-US'; }
  function fmtDate(iso) { var p = String(iso).slice(0, 10).split('-'); return state.lang === 'es' ? (+p[2]) + ' ' + MES.es[+p[1] - 1] + ' ' + p[0] : MES.en[+p[1] - 1] + ' ' + (+p[2]) + ', ' + p[0]; }
  function num(v, d) { return Number(v).toLocaleString(loc(), { minimumFractionDigits: d, maximumFractionDigits: d }); }
  function sgn(v, d) { return (v > 0 ? '+' : '') + num(v, d); }

  function getLang() { try { var l = localStorage.getItem('lang'); if (l === 'en' || l === 'es') return l; } catch (e) {} return (navigator.language || 'es').slice(0, 2) === 'en' ? 'en' : 'es'; }
  function applyLang() {
    document.documentElement.lang = state.lang;
    var spans = document.querySelectorAll('[data-lang]');
    for (var i = 0; i < spans.length; i++) spans[i].style.display = spans[i].getAttribute('data-lang') === state.lang ? 'inline' : 'none';
    var bs = document.querySelectorAll('[data-setlang]');
    for (var j = 0; j < bs.length; j++) bs[j].setAttribute('aria-pressed', String(bs[j].getAttribute('data-setlang') === state.lang));
  }
  function fetchJSON(path, long) {
    var v = long ? '1' : String(Math.floor(Date.now() / 300000));
    return fetch(BASE + path + '?v=' + v, { cache: long ? 'default' : 'no-store' }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
  }

  /* ---------- Encabezado ---------- */
  function renderToday() {
    var s = document.getElementById('nx-today'); if (!s) return;
    s.textContent = new Date().toLocaleDateString(loc(), { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', timeZone: 'America/Mexico_City' });
  }
  function renderStamp() {
    var s = document.getElementById('nx-stamp'); if (!s || !state.latest) return;
    s.replaceChildren();
    var d = new Date(state.latest.actualizado);
    var hh = d.toLocaleTimeString(loc(), { hour: '2-digit', minute: '2-digit', timeZone: 'America/Mexico_City' });
    s.appendChild(document.createTextNode(t('upd') + ' '));
    s.appendChild(el('b', null, fmtDate(state.latest.actualizado) + ' · ' + hh + ' CDMX'));
    s.appendChild(document.createTextNode(' · ' + (MOM[state.lang][state.latest.momento] || '')));
  }

  /* ---------- Cintillo ---------- */
  function fmtVal(r) { return r.grupo === 'bono' ? num(r.valor, 2) + '%' : r.grupo === 'divisa' ? num(r.valor, r.valor > 100 ? 2 : 4) : num(r.valor, r.valor >= 1000 ? 0 : 2); }
  function fmtChg(r) { return sgn(r.cambio, r.grupo === 'bono' ? 0 : 2) + (r.grupo === 'bono' ? (state.lang === 'en' ? ' bp' : ' pb') : '%'); }
  function renderTicker() {
    var box = document.getElementById('nx-ticker'); if (!box || !state.latest) return;
    box.replaceChildren();
    var track = el('div', 'nx-track');
    var rows = state.latest.mercados || [];
    [false, true].forEach(function (dup) {
      rows.forEach(function (r) {
        var c = el('div', 'nx-tk'); if (dup) c.setAttribute('aria-hidden', 'true');
        c.appendChild(el('span', 'n', state.lang === 'en' ? (r.name_en || r.nombre) : r.nombre));
        c.appendChild(el('span', 'v', fmtVal(r)));
        if (r.cambio != null) c.appendChild(el('span', r.cambio > 0 ? 'up' : r.cambio < 0 ? 'down' : 'flat', fmtChg(r)));
        track.appendChild(c);
      });
    });
    track.style.setProperty('--nx-dur', Math.max(30, rows.length * 4) + 's');
    box.appendChild(track);
  }

  /* ---------- Nota principal ---------- */
  function barsFigure(mercado) {
    var rows = (state.latest.mercados || []).filter(function (r) { return r.cambio != null && (mercado === 'global' ? r.grupo === 'bolsa' : ['IPC BMV', 'USD/MXN', 'Mezcla mexicana', 'Bono M 10 años', 'Cetes 28 días'].indexOf(r.nombre) >= 0); });
    if (!rows.length) return null;
    var pct = rows.filter(function (r) { return r.grupo !== 'bono'; });
    var max = Math.max.apply(null, pct.map(function (r) { return Math.abs(r.cambio); }).concat([0.5]));
    var fig = el('figure', 'nx-figure');
    fig.appendChild(el('div', 'fh', mercado === 'global' ? t('figG') : t('figM')));
    var g = el('div', 'nx-bars');
    rows.slice().sort(function (a, b) { return b.cambio - a.cambio; }).forEach(function (r) {
      var cls = r.cambio >= 0 ? 'up' : 'down';
      g.appendChild(el('span', 'lb', state.lang === 'en' ? (r.name_en || r.nombre) : r.nombre));
      var tr = el('span', 'tr'); var br = el('span', 'br ' + cls);
      var w = r.grupo === 'bono' ? Math.min(50, Math.abs(r.cambio) / 10 * 50) : Math.abs(r.cambio) / max * 50;
      br.style.width = w + '%'; br.style.left = r.cambio >= 0 ? '50%' : (50 - w) + '%';
      tr.appendChild(br); g.appendChild(tr);
      g.appendChild(el('span', 'vl ' + cls, fmtChg(r)));
    });
    fig.appendChild(g);
    return fig;
  }
  function briefBody(b) {
    var L = b[state.lang] || b.es; var frag = document.createDocumentFragment();
    var body = el('div', 'nx-body');
    (L.bloques || []).forEach(function (x) { var s = el('section', 'nx-sec'); s.appendChild(el('h4', null, x.t)); s.appendChild(el('p', null, x.x)); body.appendChild(s); });
    if (L.scm) { var s = el('aside', 'nx-scm' + (b.fin_de_semana ? ' wk' : '')); s.appendChild(el('h4', null, b.fin_de_semana ? t('wk') : t('scm'))); s.appendChild(el('p', null, L.scm)); body.appendChild(s); }
    if (b.fuentes && b.fuentes.length) {
      var p = el('p', 'nx-src'); p.appendChild(document.createTextNode(t('src') + ': '));
      b.fuentes.forEach(function (f, i) { var a = el('a', null, f.t); a.href = f.u; a.target = '_blank'; a.rel = 'noopener nofollow'; p.appendChild(a); if (i < b.fuentes.length - 1) p.appendChild(document.createTextNode(' · ')); });
      body.appendChild(p);
    }
    frag.appendChild(body);
    return frag;
  }
  function renderBrief() {
    var box = document.getElementById('nx-brief'); if (!box || !state.latest) return;
    box.replaceChildren();
    var b = state.latest.briefs && state.latest.briefs[state.tab]; if (!b) return;
    var L = b[state.lang] || b.es;
    var k = el('p', 'nx-kick');
    k.appendChild(document.createTextNode(MOM[state.lang][b.momento] || b.momento));
    k.appendChild(el('span', 'sep', '|'));
    k.appendChild(document.createTextNode(MKT[state.lang][b.mercado]));
    if (b.fin_de_semana) { k.appendChild(el('span', 'sep', '|')); k.appendChild(el('span', 'wk', t('wkk'))); }
    box.appendChild(k);
    box.appendChild(el('h1', 'nx-hl', L.titular));
    var by = el('div', 'nx-byline'); by.appendChild(el('b', null, t('by'))); by.appendChild(document.createTextNode('· ' + fmtDate(b.fecha) + ' · ' + b.hora)); box.appendChild(by);
    var fig = barsFigure(b.mercado); if (fig) box.appendChild(fig);
    box.appendChild(briefBody(b));
  }
  function renderOther() {
    var box = document.getElementById('nx-other'); if (!box || !state.latest) return;
    box.replaceChildren();
    var other = state.tab === 'global' ? 'mexico' : 'global';
    var b = state.latest.briefs && state.latest.briefs[other]; if (!b) { box.hidden = true; return; }
    box.hidden = false;
    var L = b[state.lang] || b.es;
    box.appendChild(el('h3', 'nx-boxh', MKT[state.lang][other]));
    var tt = el('p', 't', L.titular); box.appendChild(tt);
    if (L.scm) box.appendChild(el('p', null, L.scm));
    box.onclick = function () { var btn = document.querySelector('.nx-tabs [data-tab="' + other + '"]'); if (btn) btn.click(); window.scrollTo({ top: document.getElementById('portada').offsetTop - 10, behavior: 'smooth' }); };
  }
  function renderLatestList() {
    var ol = document.getElementById('nx-latest'); if (!ol || !state.index) return;
    ol.replaceChildren();
    (state.index.items || []).slice(0, 6).forEach(function (x) {
      var li = el('li'); var d = el('div');
      d.appendChild(el('span', 'm', fmtDate(x.fecha) + ' · ' + (MOM[state.lang][x.momento] || x.momento) + ' · ' + MKT[state.lang][x.mercado]));
      d.appendChild(el('span', 't', state.lang === 'en' ? (x.titular_en || x.titular_es) : x.titular_es));
      li.appendChild(d); ol.appendChild(li);
    });
  }
  function renderAgenda() {
    var ul = document.getElementById('nx-agenda'); if (!ul || !state.latest) return;
    ul.replaceChildren();
    var today = new Date().toISOString().slice(0, 10);
    var items = (state.latest.agenda || []).filter(function (a) { return a.fecha >= today; }).slice(0, 5);
    if (!items.length) { ul.appendChild(el('li', 'nx-empty', t('noag'))); return; }
    items.forEach(function (a) {
      var p = a.fecha.split('-'); var li = el('li');
      var d = el('div', 'd'); d.appendChild(el('b', null, String(+p[2]))); d.appendChild(el('span', null, MES[state.lang][+p[1] - 1]));
      li.appendChild(d); li.appendChild(el('div', null, a[state.lang] || a.es)); ul.appendChild(li);
    });
  }

  /* ---------- Mapa ---------- */
  function renderMap() {
    var box = document.getElementById('nx-map'); if (!box || !state.latest || !state.world || !window.d3 || !window.topojson || !d3.geoNaturalEarth1) return;
    box.replaceChildren();
    var W = 1000, H = 470;
    var svg = sv('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': state.lang === 'es' ? 'Mapa de bolsas del día' : 'Map of today’s stock markets' });
    var land = topojson.feature(state.world, state.world.objects.countries);
    var proj = d3.geoNaturalEarth1().fitExtent([[10, 10], [W - 10, H - 10]], { type: 'Sphere' });
    var path = d3.geoPath(proj);
    var g = sv('g');
    land.features.forEach(function (f) { if (f.id === '010') return; g.appendChild(sv('path', { d: path(f), 'class': 'land' + (HL[f.id] ? ' hl' : '') })); });
    svg.appendChild(g);
    var rows = (state.latest.mercados || []).filter(function (r) { return CITY[r.nombre] && r.cambio != null; });
    var max = Math.max.apply(null, rows.map(function (r) { return Math.abs(r.cambio); }).concat([0.5]));
    rows.forEach(function (r) {
      var c = CITY[r.nombre]; var p = proj([c[0], c[1]]); var cls = r.cambio >= 0 ? 'up' : 'down';
      var rad = 7 + Math.abs(r.cambio) / max * 16;
      svg.appendChild(sv('circle', { cx: p[0], cy: p[1], r: rad, 'class': 'ring ' + cls }));
      svg.appendChild(sv('circle', { cx: p[0], cy: p[1], r: rad * 0.62, 'class': 'bub ' + cls }));
      var right = c[3] ? c[3] !== 'left' : p[0] < W * 0.8; var dy = c[4] || 0; var x = p[0] + (right ? rad + 6 : -rad - 6); var anchor = right ? 'start' : 'end';
      svg.appendChild(sv('text', { x: x, y: p[1] - 3 + dy, 'text-anchor': anchor, 'class': 'lbl' }, (state.lang === 'en' ? (r.name_en || r.nombre) : r.nombre) + ' · ' + (state.lang === 'en' ? CITY_EN[c[2]] : c[2])));
      svg.appendChild(sv('text', { x: x, y: p[1] + 13 + dy, 'text-anchor': anchor, 'class': 'lbl2 ' + cls }, fmtChg(r)));
    });
    box.appendChild(svg);
  }

  /* ---------- Gráficos ---------- */
  function niceTicks(lo, hi, n) {
    var step = Math.pow(10, Math.floor(Math.log10((hi - lo) / n))); var err = (hi - lo) / n / step;
    if (err >= 7.5) step *= 10; else if (err >= 3.5) step *= 5; else if (err >= 1.5) step *= 2;
    var out = []; for (var v = Math.ceil(lo / step) * step; v <= hi + 1e-9; v += step) out.push(+v.toFixed(6)); return out;
  }
  function frame(boxId, H) {
    var box = document.getElementById(boxId); if (!box) return null;
    box.replaceChildren();
    var W = Math.max(300, box.clientWidth || 340);
    var svg = sv('svg', { viewBox: '0 0 ' + W + ' ' + H }); box.appendChild(svg);
    var tip = el('div', 'nx-tipc'); box.appendChild(tip);
    return { box: box, svg: svg, W: W, H: H, tip: tip };
  }
  function showTip(f, x, y, txt) { f.tip.textContent = txt; f.tip.style.display = 'block'; f.tip.style.left = (x / f.W * f.box.clientWidth) + 'px'; f.tip.style.top = (y / f.H * f.box.clientHeight) + 'px'; }
  function lineChart(boxId, pts, opt) {
    var f = frame(boxId, 230); if (!f || !pts.length) return;
    var m = { l: 44, r: 54, t: 12, b: 26 };
    var series = opt.series;
    var vals = []; series.forEach(function (s) { pts.forEach(function (p) { if (p[s.k] != null) vals.push(p[s.k]); }); });
    var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals); var pad = (hi - lo) * 0.15 || 0.5; lo -= pad; hi += pad;
    var x = function (i) { return m.l + i / Math.max(1, pts.length - 1) * (f.W - m.l - m.r); };
    var y = function (v) { return f.H - m.b - (v - lo) / (hi - lo) * (f.H - m.t - m.b); };
    niceTicks(lo, hi, 4).forEach(function (v) {
      f.svg.appendChild(sv('line', { x1: m.l, x2: f.W - m.r, y1: y(v), y2: y(v), 'class': 'nx-gr' }));
      f.svg.appendChild(sv('text', { x: m.l - 8, y: y(v) + 4, 'text-anchor': 'end', 'class': 'nx-ax' }, opt.fy(v)));
    });
    var every = Math.max(1, Math.ceil(pts.length / 6));
    pts.forEach(function (p, i) { if (i % every === 0 || i === pts.length - 1) f.svg.appendChild(sv('text', { x: x(i), y: f.H - 6, 'text-anchor': 'middle', 'class': 'nx-ax' }, opt.fx(p))); });
    series.forEach(function (s) {
      var d = ''; var started = false;
      pts.forEach(function (p, i) {
        if (p[s.k] == null) return;
        if (s.step && started) { var prevY = d.split(' ').pop().split(',')[1]; d += ' L' + x(i) + ',' + prevY; }
        d += (started ? ' L' : 'M') + x(i) + ',' + y(p[s.k]); started = true;
      });
      if (s.area) {
        var first = pts.findIndex(function (p) { return p[s.k] != null; });
        f.svg.appendChild(sv('path', { d: d + ' L' + x(pts.length - 1) + ',' + (f.H - m.b) + ' L' + x(first) + ',' + (f.H - m.b) + ' Z', fill: s.c, 'fill-opacity': '0.08' }));
      }
      f.svg.appendChild(sv('path', { d: d, fill: 'none', stroke: s.c, 'stroke-width': 2.5, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }));
      pts.forEach(function (p, i) {
        if (p[s.k] == null) return;
        var dot = sv('circle', { cx: x(i), cy: y(p[s.k]), r: s.dots ? 4 : 2.5, fill: s.c, stroke: '#fff', 'stroke-width': 1.5, style: s.dots ? '' : 'opacity:0' });
        var hit = sv('circle', { cx: x(i), cy: y(p[s.k]), r: 10, fill: 'transparent', style: 'cursor:default' });
        hit.addEventListener('mouseenter', function () { dot.style.opacity = 1; showTip(f, x(i), y(p[s.k]), opt.fx(p) + ' · ' + (s.name ? s.name + ' ' : '') + opt.fy(p[s.k])); });
        hit.addEventListener('mouseleave', function () { if (!s.dots) dot.style.opacity = 0; f.tip.style.display = 'none'; });
        f.svg.appendChild(dot); f.svg.appendChild(hit);
      });
      var lastI = -1; pts.forEach(function (p, i) { if (p[s.k] != null) lastI = i; });
      if (lastI >= 0) f.svg.appendChild(sv('text', { x: x(lastI) + 7, y: y(pts[lastI][s.k]) + 4, fill: s.c, 'font-weight': 700, 'class': 'nx-ax', style: 'fill:' + s.c }, opt.fy(pts[lastI][s.k])));
    });
    if (series.length > 1) {
      var leg = el('div', 'nx-leg');
      series.forEach(function (s) { var sp = el('span'); var i = el('i'); i.style.background = s.c; sp.appendChild(i); sp.appendChild(document.createTextNode(s.name)); leg.appendChild(sp); });
      f.box.appendChild(leg);
    }
  }
  function dumbbell(boxId, rows) {
    var f = frame(boxId, 230); if (!f || !rows.length) return;
    var m = { l: 96, r: 16, t: 8, b: 24 };
    var vals = []; rows.forEach(function (r) { if (r.tasa != null) vals.push(r.tasa); if (r.inflacion != null) vals.push(r.inflacion); });
    var hi = Math.max.apply(null, vals) * 1.12;
    var x = function (v) { return m.l + v / hi * (f.W - m.l - m.r); };
    var band = (f.H - m.t - m.b) / rows.length;
    niceTicks(0, hi, 4).forEach(function (v) {
      f.svg.appendChild(sv('line', { x1: x(v), x2: x(v), y1: m.t, y2: f.H - m.b, 'class': 'nx-gr' }));
      f.svg.appendChild(sv('text', { x: x(v), y: f.H - 6, 'text-anchor': 'middle', 'class': 'nx-ax' }, num(v, 0) + '%'));
    });
    rows.forEach(function (r, i) {
      var cy = m.t + band * i + band / 2;
      f.svg.appendChild(sv('text', { x: m.l - 10, y: cy + 4, 'text-anchor': 'end', 'class': 'nx-ax', style: 'fill:#15171b;font-weight:600' }, state.lang === 'en' ? r.en : r.es));
      if (r.tasa != null && r.inflacion != null) f.svg.appendChild(sv('line', { x1: x(r.tasa), x2: x(r.inflacion), y1: cy, y2: cy, stroke: '#c9ced6', 'stroke-width': 3, 'stroke-linecap': 'round' }));
      [['tasa', '#1e4f9c', t('tasa')], ['inflacion', '#b87514', t('infl')]].forEach(function (s) {
        if (r[s[0]] == null) return;
        var c = sv('circle', { cx: x(r[s[0]]), cy: cy, r: 6.5, fill: s[1], stroke: '#fff', 'stroke-width': 2 });
        c.addEventListener('mouseenter', function () { showTip(f, x(r[s[0]]), cy, (state.lang === 'en' ? r.en : r.es) + ' · ' + s[2] + ' ' + num(r[s[0]], 2) + '%'); });
        c.addEventListener('mouseleave', function () { f.tip.style.display = 'none'; });
        f.svg.appendChild(c);
      });
    });
    var leg = el('div', 'nx-leg');
    [['#1e4f9c', t('tasa')], ['#b87514', t('infl')]].forEach(function (s) { var sp = el('span'); var i = el('i'); i.style.background = s[0]; sp.appendChild(i); sp.appendChild(document.createTextNode(s[1])); leg.appendChild(sp); });
    f.box.appendChild(leg);
  }
  /* Mapa de calor de acciones (treemap por sector; tamaño = valor de mercado, color = variación del día) */
  var SECT = {
    es: { tec: 'Tecnología', com: 'Comunicaciones', cons: 'Consumo discrecional', basic: 'Consumo básico', fin: 'Financiero', salud: 'Salud', ind: 'Industrial', ener: 'Energía', mat: 'Materiales', util: 'Servicios públicos', inmo: 'Inmobiliario' },
    en: { tec: 'Technology', com: 'Communication', cons: 'Consumer discretionary', basic: 'Consumer staples', fin: 'Financials', salud: 'Health care', ind: 'Industrials', ener: 'Energy', mat: 'Materials', util: 'Utilities', inmo: 'Real estate' }
  };
  function mix(a, b, k) { var pa = [parseInt(a.slice(1, 3), 16), parseInt(a.slice(3, 5), 16), parseInt(a.slice(5, 7), 16)], pb = [parseInt(b.slice(1, 3), 16), parseInt(b.slice(3, 5), 16), parseInt(b.slice(5, 7), 16)]; return 'rgb(' + pa.map(function (v, i) { return Math.round(v + (pb[i] - v) * k); }).join(',') + ')'; }
  function heatColor(c) { var k = Math.min(1, Math.abs(c) / 3); return c >= 0 ? mix('#e4e2dc', '#13804f', Math.pow(k, 0.8)) : mix('#e4e2dc', '#b3261e', Math.pow(k, 0.8)); }
  function renderHeat() {
    var box = document.getElementById('nx-heat'), pills = document.getElementById('nx-heat-tabs'), src = document.getElementById('nx-heat-src');
    if (!box || !pills) return;
    box.replaceChildren(); pills.replaceChildren(); if (src) src.textContent = '';
    var H = state.heat;
    var list = H && H.indices ? H.indices.filter(function (x) { return x.mercado === state.tab; }) : [];
    if (!list.length || !window.d3 || !d3.treemap) { box.appendChild(el('p', 'nx-empty', state.lang === 'en' ? 'The stock heatmap is being generated; it will appear in a few minutes.' : 'El mapa de calor se está generando; aparecerá en unos minutos.')); return; }
    var cur = state.heatIdx[state.tab]; if (!list.some(function (x) { return x.id === cur; })) cur = state.heatIdx[state.tab] = list[0].id;
    if (list.length > 1) list.forEach(function (x) {
      var b = el('button', null, state.lang === 'en' ? x.en : x.es); b.type = 'button'; b.setAttribute('role', 'tab'); b.setAttribute('aria-selected', String(x.id === cur));
      b.addEventListener('click', function () { state.heatIdx[state.tab] = x.id; renderHeat(); });
      pills.appendChild(b);
    });
    var idx = list.filter(function (x) { return x.id === cur; })[0];
    var W = Math.max(300, box.clientWidth || 340), narrow = W < 560, Hh = narrow ? 460 : Math.round(Math.min(560, Math.max(380, W * 0.46)));
    var groups = {}; idx.acciones.forEach(function (a) { (groups[a.s] = groups[a.s] || []).push(a); });
    var root = d3.hierarchy({ children: Object.keys(groups).map(function (k) { return { s: k, children: groups[k] }; }) }).sum(function (d) { return d.cap || 0; }).sort(function (a, b) { return b.value - a.value; });
    d3.treemap().size([W, Hh]).paddingOuter(1).paddingTop(function (d) { return d.depth === 1 ? 17 : 0; }).paddingInner(1.5).round(true).tile(d3.treemapSquarify.ratio(1.2))(root);
    var svg = sv('svg', { viewBox: '0 0 ' + W + ' ' + Hh, role: 'img', 'aria-label': (state.lang === 'en' ? idx.en : idx.es) }); box.appendChild(svg);
    var tip = el('div', 'nx-tipc nx-tiph'); box.appendChild(tip);
    (root.children || []).forEach(function (g) {
      var gw = g.x1 - g.x0;
      svg.appendChild(sv('rect', { x: g.x0, y: g.y0, width: gw, height: g.y1 - g.y0, 'class': 'nx-hsec' }));
      if (gw > 44) {
        var name = SECT[state.lang][g.data.s] || g.data.s; var maxc = Math.floor((gw - 8) / 6.4);
        svg.appendChild(sv('text', { x: g.x0 + 4, y: g.y0 + 12, 'class': 'nx-hsl' }, name.length > maxc ? name.slice(0, Math.max(1, maxc - 1)) + '…' : name));
      }
    });
    root.leaves().forEach(function (n) {
      var a = n.data, w = n.x1 - n.x0, h = n.y1 - n.y0; if (w <= 0 || h <= 0) return;
      var g = sv('g', { 'class': 'nx-hcell' });
      g.appendChild(sv('rect', { x: n.x0, y: n.y0, width: w, height: h, fill: heatColor(a.chg) }));
      var dark = Math.abs(a.chg) >= 1.2; var col = dark ? '#fff' : '#15171b';
      if (w > 30 && h > 20) {
        var CW = 0.62, base = Math.min(20, Math.sqrt(w * h) / 5);
        var fit = function (lines) { var L = Math.max.apply(null, lines.map(function (x) { return x.length; })); return Math.min(base, (w - 8) / (L * CW), (h - 6) / (lines.length * 1.15 + 1)); };
        var lines = [a.n], fs = fit(lines);
        var sp = a.n.indexOf(' ');
        if (sp > 0) {
          var mid = a.n.length / 2, best = -1;
          for (var k = 0; k < a.n.length; k++) if (a.n[k] === ' ' && (best < 0 || Math.abs(k - mid) < Math.abs(best - mid))) best = k;
          var two = [a.n.slice(0, best), a.n.slice(best + 1)], fs2 = fit(two);
          if (fs2 > fs * 1.15) { lines = two; fs = fs2; }
        }
        if (fs < 8) { fs = 8; var maxc = Math.max(2, Math.floor((w - 8) / (fs * CW))); lines = [a.n.length > maxc ? a.n.slice(0, maxc - 1) + '…' : a.n]; }
        var showChg = h > fs * (lines.length * 1.15 + 1.3) && w > 36;
        var cx = n.x0 + w / 2, blockH = fs * 1.15 * lines.length + (showChg ? fs * 0.95 : 0);
        var y0 = n.y0 + h / 2 - blockH / 2 + fs * 0.85;
        lines.forEach(function (ln, i) { g.appendChild(sv('text', { x: cx, y: y0 + i * fs * 1.15, 'text-anchor': 'middle', 'class': 'nx-htk', style: 'font-size:' + fs.toFixed(1) + 'px;fill:' + col }, ln)); });
        if (showChg) g.appendChild(sv('text', { x: cx, y: y0 + lines.length * fs * 1.15 + fs * 0.1, 'text-anchor': 'middle', 'class': 'nx-hch', style: 'font-size:' + (fs * 0.75).toFixed(1) + 'px;fill:' + col }, sgn(a.chg, 2) + '%'));
      }
      var txt = a.n + ' · ' + sgn(a.chg, 2) + '% · ' + num(a.p, 2);
      g.addEventListener('mouseenter', function () { tip.textContent = txt; tip.style.display = 'block'; var hw = tip.offsetWidth / 2, bw = box.clientWidth; tip.style.left = Math.max(hw, Math.min(bw - hw, (n.x0 + w / 2) / W * bw)) + 'px'; tip.style.top = (n.y0 / Hh * box.clientHeight + 6) + 'px'; });
      g.addEventListener('mouseleave', function () { tip.style.display = 'none'; });
      svg.appendChild(g);
    });
    if (src) {
      src.replaceChildren();
      var up = idx.acciones.filter(function (a) { return a.chg > 0; }).length;
      var now = Date.now(), live = idx.abre && idx.cierra && now >= Date.parse(idx.abre) && now < Date.parse(idx.cierra);
      var hh = function (iso) { return new Date(iso).toLocaleTimeString(loc(), { hour: '2-digit', minute: '2-digit', timeZone: 'America/Mexico_City' }); };
      var badge = el('span', 'nx-hbadge' + (live ? ' live' : ''), live ? (state.lang === 'en' ? 'Live' : 'En vivo') : (state.lang === 'en' ? 'Close' : 'Cierre'));
      src.appendChild(badge);
      src.appendChild(document.createTextNode(' ' + (live
        ? (state.lang === 'en' ? 'Updated ' : 'Actualizado ') + hh(idx.actualizado || H.actualizado) + ' CDMX · '
        : (state.lang === 'en' ? 'Session of ' : 'Sesión del ') + fmtDate(idx.fecha) + ' · ')
        + (state.lang === 'en' ? up + ' of ' + idx.acciones.length + ' up · Data: ' : up + ' de ' + idx.acciones.length + ' suben · Datos: ') + (H.fuente || 'Yahoo Finance') + (state.lang === 'en' ? ', ~15 min delay' : ', retraso ~15 min')));
    }
  }
  function cmdChart(boxId) {
    var box = document.getElementById(boxId); if (!box || !state.latest) return;
    box.replaceChildren();
    var rows = (state.latest.mercados || []).filter(function (r) { return r.cambio != null && (r.grupo === 'materia_prima' || r.grupo === 'divisa'); });
    if (!rows.length) return;
    var max = Math.max.apply(null, rows.map(function (r) { return Math.abs(r.cambio); }).concat([0.5]));
    var g = el('div', 'nx-bars');
    rows.slice().sort(function (a, b) { return b.cambio - a.cambio; }).forEach(function (r) {
      var cls = r.cambio >= 0 ? 'up' : 'down';
      g.appendChild(el('span', 'lb', state.lang === 'en' ? (r.name_en || r.nombre) : r.nombre));
      var tr = el('span', 'tr'); var br = el('span', 'br ' + cls); var w = Math.abs(r.cambio) / max * 50;
      br.style.width = w + '%'; br.style.left = r.cambio >= 0 ? '50%' : (50 - w) + '%'; tr.appendChild(br); g.appendChild(tr);
      g.appendChild(el('span', 'vl ' + cls, fmtChg(r)));
    });
    box.appendChild(g);
  }
  function renderCharts() {
    var views = document.querySelectorAll('.nx-chgrid[data-view]');
    for (var i = 0; i < views.length; i++) views[i].hidden = views[i].getAttribute('data-view') !== state.tab;
    renderHeat();
    var S = state.series;
    if (state.tab === 'mexico') {
      if (!S) return;
      var d2 = function (iso) { var p = iso.split('-'); return (+p[2]) + ' ' + MES[state.lang][+p[1] - 1]; };
      lineChart('nx-ch-usd', S.usdmxn || [], { series: [{ k: 'v', c: '#1e4f9c', area: true }], fx: function (p) { return d2(p.fecha); }, fy: function (v) { return num(v, 2); } });
      lineChart('nx-ch-banxico', S.banxico || [], { series: [{ k: 'tasa', c: '#1e4f9c', step: true, name: t('banx') }, { k: 'inflacion', c: '#b87514', dots: true, name: t('infl') }], fx: function (p) { var q = p.mes.split('-'); return MES[state.lang][+q[1] - 1] + (q[1] === '01' || q[1] === '12' ? ' ' + q[0].slice(2) : ''); }, fy: function (v) { return num(v, 2) + '%'; } });
    } else {
      if (S) dumbbell('nx-ch-rates', S.economias || []);
      cmdChart('nx-ch-cmd');
    }
  }
  function setTab(tab) {
    state.tab = tab;
    var all = document.querySelectorAll('.nx-tabs button[data-tab]');
    for (var m = 0; m < all.length; m++) all[m].setAttribute('aria-selected', String(all[m].getAttribute('data-tab') === tab));
    renderBrief(); renderOther(); renderCharts(); renderTrends();
  }


  /* ---------- Tendencias por industria ---------- */
  function renderTrends() {
    var T = state.trends, grid = document.getElementById('nx-trends'); if (!grid) return;
    var hl = document.getElementById('nx-trhl'), note = document.getElementById('nx-trnote');
    grid.replaceChildren();
    if (!T || !T.items) { if (hl) hl.textContent = ''; return; }
    var en = state.lang === 'en';
    if (hl) hl.textContent = T.titular ? (T.titular[state.lang] || T.titular.es) : '';
    if (note) note.textContent = (en ? 'What the day\'s news says about each industry, read for supply chain · ' : 'Lo que dicen las noticias del día de cada industria, leído para supply chain · ') + fmtDate(T.fecha);
    var DIR = { up: [en ? 'Rising' : 'Al alza', '▲'], down: [en ? 'Falling' : 'A la baja', '▼'], mixed: [en ? 'Mixed' : 'Mixta', '◆'] };
    var items = T.items.slice();
    if (state.tab === 'mexico') items.sort(function (a, b) { return (b.mx ? 1 : 0) - (a.mx ? 1 : 0); });
    items.forEach(function (it) {
      var c = el('article', 'nx-tr ' + (it.dir || 'mixed'));
      var top = el('div', 'nx-trh');
      top.appendChild(el('span', 'nx-trn', en ? it.en : it.es));
      var d = DIR[it.dir] || DIR.mixed;
      var chip = el('span', 'nx-trd', d[1] + ' ' + d[0]); top.appendChild(chip);
      c.appendChild(top);
      var heat = el('div', 'nx-trheat'); heat.setAttribute('title', en ? 'Weight in today\'s news' : 'Peso en las noticias de hoy');
      for (var i = 1; i <= 3; i++) heat.appendChild(el('i', i <= (it.calor || 1) ? 'on' : null));
      heat.appendChild(el('span', null, en ? ['Low', 'Medium', 'High'][(it.calor || 1) - 1] + ' buzz' : 'Relevancia ' + ['baja', 'media', 'alta'][(it.calor || 1) - 1]));
      c.appendChild(heat);
      c.appendChild(el('h3', null, it.titular[state.lang] || it.titular.es));
      c.appendChild(el('p', null, it.x[state.lang] || it.x.es));
      var s = el('aside', 'nx-trscm'); s.appendChild(el('b', null, t('scm'))); s.appendChild(el('span', null, it.scm[state.lang] || it.scm.es)); c.appendChild(s);
      if (it.fuentes && it.fuentes.length) {
        var f = el('p', 'nx-trsrc');
        it.fuentes.forEach(function (x, j) { var a = el('a', null, x.t); a.href = x.u; a.target = '_blank'; a.rel = 'noopener nofollow'; f.appendChild(a); if (j < it.fuentes.length - 1) f.appendChild(document.createTextNode(' · ')); });
        c.appendChild(f);
      }
      grid.appendChild(c);
    });
    renderSectors();
  }
  function renderSectors() {
    var box = document.getElementById('nx-sect'), h = document.getElementById('nx-sect-h'); if (!box) return;
    box.replaceChildren();
    var H = state.heat; var id = state.tab === 'mexico' ? 'ipc' : 'sp500';
    var idx = H && H.indices ? H.indices.filter(function (x) { return x.id === id; })[0] : null;
    if (h) h.textContent = (state.lang === 'en' ? 'Sectors in the market today · ' : 'Sectores en bolsa hoy · ') + (idx ? (state.lang === 'en' ? idx.en : idx.es) : (id === 'ipc' ? 'IPC' : 'S&P 500'));
    if (!idx) return;
    var agg = {}; idx.acciones.forEach(function (a) { var g = agg[a.s] = agg[a.s] || { w: 0, v: 0 }; g.w += a.cap; g.v += a.cap * a.chg; });
    var rows = Object.keys(agg).map(function (k) { return { k: k, chg: agg[k].v / agg[k].w }; }).sort(function (a, b) { return b.chg - a.chg; });
    var max = Math.max.apply(null, rows.map(function (r) { return Math.abs(r.chg); }).concat([0.5]));
    var g = el('div', 'nx-bars');
    rows.forEach(function (r) {
      var cls = r.chg >= 0 ? 'up' : 'down';
      g.appendChild(el('span', 'lb', SECT[state.lang][r.k] || r.k));
      var tr = el('span', 'tr'), br = el('span', 'br ' + cls), w = Math.abs(r.chg) / max * 50;
      br.style.width = w + '%'; br.style.left = r.chg >= 0 ? '50%' : (50 - w) + '%'; tr.appendChild(br); g.appendChild(tr);
      g.appendChild(el('span', 'vl ' + cls, sgn(r.chg, 2) + '%'));
    });
    box.appendChild(g);
  }

  /* ---------- Lectura y archivo ---------- */
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
    if (!items.length) { ul.appendChild(el('li', 'nx-empty', t('none'))); return; }
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
          load.then(function (b) { body.replaceChildren(briefBody(b)); }).catch(function () { body.textContent = t('err'); });
        }
      });
      li.appendChild(h); li.appendChild(body); ul.appendChild(li);
    });
  }

  function renderAll() { applyLang(); renderToday(); renderStamp(); renderTicker(); renderBrief(); renderOther(); renderLatestList(); renderAgenda(); renderMap(); renderCharts(); renderTrends(); renderLectura(); renderFeed(); }

  function init() {
    state.lang = getLang();
    applyLang(); renderToday();
    var bs = document.querySelectorAll('[data-setlang]');
    for (var i = 0; i < bs.length; i++) bs[i].addEventListener('click', function (e) {
      state.lang = e.currentTarget.getAttribute('data-setlang');
      try { localStorage.setItem('lang', state.lang); } catch (err) {}
      renderAll();
    });
    var tabs = document.querySelectorAll('.nx-tabs button[data-tab]');
    for (var k = 0; k < tabs.length; k++) tabs[k].addEventListener('click', function (e) { setTab(e.currentTarget.getAttribute('data-tab')); });
    window.addEventListener('storage', function (e) { if (e.key === 'lang' && (e.newValue === 'es' || e.newValue === 'en')) { state.lang = e.newValue; renderAll(); } });
    var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(renderCharts, 200); });
    Promise.all([
      fetchJSON('latest.json'),
      fetchJSON('index.json').catch(function () { return { items: [] }; }),
      fetchJSON('series.json').catch(function () { return null; }),
      fetchJSON('world-110m.json', true).catch(function () { return null; }),
      fetchJSON('heatmaps.json').catch(function () { return null; }),
      fetchJSON('tendencias.json').catch(function () { return null; })
    ]).then(function (res) { state.latest = res[0]; state.index = res[1]; state.series = res[2]; state.world = res[3]; state.heat = res[4]; state.trends = res[5]; renderAll(); })
      .catch(function () { var b = document.getElementById('nx-brief'); if (b) b.textContent = t('err'); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
