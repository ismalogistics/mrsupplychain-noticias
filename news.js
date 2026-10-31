/* Mr. Supply Chain® México · Noticias — portal. Lee data/*.json del mismo origen (compatible con la CSP del sitio). */
(function () {
  'use strict';
  var BASE = 'data/';
  var NS = 'http://www.w3.org/2000/svg';
  var state = { lang: 'es', tab: 'global', latest: null, index: null, series: null, world: null, heat: null, trends: null, heatIdx: { global: 'sp500', latam: 'ibovespa', mexico: 'ipc' }, cache: {} };
  var MES = { es: ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'], en: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], pt: ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'] };
  var MOM = { es: { apertura: 'Apertura', mediodia: 'Mediodía', cierre: 'Cierre' }, en: { apertura: 'Open', mediodia: 'Midday', cierre: 'Close' }, pt: { apertura: 'Abertura', mediodia: 'Meio-dia', cierre: 'Fechamento' } };
  var MKT = { es: { global: 'Global', latam: 'LATAM', mexico: 'México' }, en: { global: 'Global', latam: 'LATAM', mexico: 'Mexico' }, pt: { global: 'Global', latam: 'LATAM', mexico: 'México' } };
  var TXT = {
    es: { scm: 'Para supply chain', wk: 'Para el fin de semana', wkk: 'Edición de fin de semana', src: 'Fuentes', upd: 'Actualizado', none: 'Todavía no hay briefs anteriores.', err: 'No se pudieron cargar las noticias. Intenta de nuevo en unos minutos.', by: 'Mesa de mercados Mr. Supply Chain México', read: 'Leer la nota', figG: 'Bolsas del día', figM: 'México hoy', noag: 'Sin eventos próximos registrados.', tasa: 'Tasa', infl: 'Inflación', banx: 'Tasa Banxico' },
    en: { scm: 'For supply chain', wk: 'For the weekend', wkk: 'Weekend edition', src: 'Sources', upd: 'Updated', none: 'No earlier briefs yet.', err: 'News could not be loaded. Please try again in a few minutes.', by: 'Mr. Supply Chain México markets desk', read: 'Read the story', figG: 'Stock markets today', figM: 'Mexico today', noag: 'No upcoming events listed.', tasa: 'Rate', infl: 'Inflation', banx: 'Banxico rate' },
    pt: { scm: 'Para supply chain', wk: 'Para o fim de semana', wkk: 'Edição de fim de semana', src: 'Fontes', upd: 'Atualizado', none: 'Ainda não há briefs anteriores.', err: 'Não foi possível carregar as notícias. Tente novamente em alguns minutos.', by: 'Mesa de mercados Mr. Supply Chain México', read: 'Ler a matéria', figG: 'Bolsas do dia', figM: 'México hoje', noag: 'Nenhum evento próximo registrado.', tasa: 'Taxa', infl: 'Inflação', banx: 'Taxa do Banxico' }
  };
  var COLORS = ['#1e5fa8', '#a83246', '#1f8a5b', '#b87514', '#5b3fb8'];
  var CITY = { 'IPC BMV': [-99.13, 19.43, 'CDMX'], 'S&P 500': [-74.0, 40.71, 'Nueva York'], 'Euro Stoxx 50': [8.68, 50.11, 'Fráncfort'], 'Nikkei 225': [139.69, 35.69, 'Tokio', 'left', 22], 'KOSPI': [126.98, 37.57, 'Seúl', 'left', -24] };
  var CITY_EN = { 'CDMX': 'Mexico City', 'Nueva York': 'New York', 'Fráncfort': 'Frankfurt', 'Tokio': 'Tokyo', 'Seúl': 'Seoul' };
  var CITY_PT = { 'CDMX': 'Cidade do México', 'Nueva York': 'Nova York', 'Fráncfort': 'Frankfurt', 'Tokio': 'Tóquio', 'Seúl': 'Seul', 'Bogotá': 'Bogotá', 'Toronto': 'Toronto' };
  /* Nombres en portugués de respaldo cuando los datos no traen name_pt / pt (se usan antes que el inglés). */
  var PT_MKT = { 'Petróleo WTI': 'Petróleo WTI', 'Petróleo Brent': 'Petróleo Brent', 'Mezcla mexicana': 'Mistura mexicana', 'Oro': 'Ouro', 'Cobre': 'Cobre', 'Plata': 'Prata', 'Gas natural': 'Gás natural', 'Treasury 10 años': 'Título do Tesouro 10 anos', 'Bono M 10 años': 'Mbono 10 anos', 'Cetes 28 días': 'Cetes 28 dias', 'MSCI Perú (ETF EPU)': 'MSCI Peru (ETF EPU)' };
  var PT_NM = { 'Mexican peso': 'Peso mexicano', 'Brazilian real': 'Real brasileiro', 'Chilean peso': 'Peso chileno', 'Colombian peso': 'Peso colombiano', 'Peruvian sol': 'Sol peruano', 'Argentine peso': 'Peso argentino', 'Canadian dollar': 'Dólar canadense', 'Mexico': 'México', 'US': 'EUA', 'Euro area': 'Zona do euro', 'Japan': 'Japão', 'South Korea': 'Coreia do Sul', 'Brazil': 'Brasil', 'Canada': 'Canadá', 'China': 'China', 'MSCI Peru (EPU ETF)': 'MSCI Peru (ETF EPU)', 'MSCI Argentina (ARGT ETF)': 'MSCI Argentina (ETF ARGT)', 'MSCI Chile (ECH ETF)': 'MSCI Chile (ETF ECH)', 'MSCI COLCAP (iCOLCAP ETF)': 'MSCI COLCAP (ETF iCOLCAP)' };
  var AM_LBL = { 'S&P 500': ['right', 12], 'IPC BMV': ['left', 0], 'tsx': ['right', -12], 'bovespa': ['right', 0], 'merval': ['right', 8], 'ipsa': ['left', 0], 'colcap': ['right', 0], 'bvl': ['left', 0] };
  var HL = { '076': 1, '032': 1, '152': 1, '170': 1, '604': 1, '124': 1, '484': 1, '840': 1, '392': 1, '410': 1, '276': 1, '250': 1, '380': 1, '724': 1, '528': 1, '056': 1, '040': 1, '620': 1, '372': 1, '246': 1, '300': 1 };

  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }
  function sv(tag, attrs, text) { var n = document.createElementNS(NS, tag); for (var k in attrs) n.setAttribute(k, attrs[k]); if (text != null) n.textContent = text; return n; }
  function t(k) { return TXT[state.lang][k]; }
  /* Texto en el idioma activo: tx(español, inglés, portugués). */
  function tx(es, en, pt) { return state.lang === 'en' ? en : state.lang === 'pt' ? pt : es; }
  /* Contenido de los JSON con llaves es/en/pt; si falta pt se usa es (datos anteriores). */
  function pick(o) { if (!o) return o; return state.lang === 'pt' ? (o.pt || o.es) : (o[state.lang] || o.es); }
  /* Nombre de un renglón de mercado (nombre / name_en / name_pt). */
  function mname(r) { return state.lang === 'en' ? (r.name_en || r.nombre) : state.lang === 'pt' ? (r.name_pt || PT_MKT[r.nombre] || PT_NM[r.name_en] || r.name_en || r.nombre) : r.nombre; }
  /* Nombres con es/en (índices, monedas, economías): en portugués se usa pt, luego el respaldo, luego en. */
  function lname(o) { return state.lang === 'en' ? o.en : state.lang === 'pt' ? (o.pt || PT_NM[o.en] || o.en) : o.es; }
  function city(r) { return state.lang === 'en' ? (r.ciudad_en || r.ciudad) : state.lang === 'pt' ? (r.ciudad_pt || CITY_PT[r.ciudad] || r.ciudad_en || r.ciudad) : r.ciudad; }
  function loc() { return state.lang === 'en' ? 'en-US' : state.lang === 'pt' ? 'pt-BR' : 'es-MX'; }
  function fmtDate(iso) { var p = String(iso).slice(0, 10).split('-'); return state.lang === 'en' ? MES.en[+p[1] - 1] + ' ' + (+p[2]) + ', ' + p[0] : (+p[2]) + ' ' + MES[state.lang][+p[1] - 1] + ' ' + p[0]; }
  function num(v, d) { return Number(v).toLocaleString(loc(), { minimumFractionDigits: d, maximumFractionDigits: d }); }
  function sgn(v, d) { return (v > 0 ? '+' : '') + num(v, d); }

  function getLang() { try { var l = localStorage.getItem('lang'); if (l === 'en' || l === 'es' || l === 'pt') return l; } catch (e) {} var n = (navigator.language || 'es').slice(0, 2); return n === 'en' ? 'en' : n === 'pt' ? 'pt' : 'es'; }
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
    var txt = new Date().toLocaleDateString(loc(), { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', timeZone: 'America/Mexico_City' });
    s.textContent = txt.charAt(0).toUpperCase() + txt.slice(1);
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
  function fmtChg(r) { return sgn(r.cambio, r.grupo === 'bono' ? 0 : 2) + (r.grupo === 'bono' ? tx(' pb', ' bp', ' pb') : '%'); }
  function renderTicker() {
    var box = document.getElementById('nx-ticker'); if (!box || !state.latest) return;
    box.replaceChildren();
    var track = el('div', 'nx-track');
    var rows = state.latest.mercados || [];
    [false, true].forEach(function (dup) {
      rows.forEach(function (r) {
        var c = el('div', 'nx-tk'); if (dup) c.setAttribute('aria-hidden', 'true');
        c.appendChild(el('span', 'n', mname(r)));
        c.appendChild(el('span', 'v', fmtVal(r)));
        if (r.cambio != null) c.appendChild(el('span', r.cambio > 0 ? 'up' : r.cambio < 0 ? 'down' : 'flat', fmtChg(r)));
        track.appendChild(c);
      });
    });
    track.style.setProperty('--nx-dur', Math.max(30, rows.length * 4) + 's');
    box.appendChild(track);
  }

  /* ---------- Nota principal ---------- */
  function latamRows() {
    var out = [];
    (state.latest.mercados || []).forEach(function (r) { if (r.nombre === 'IPC BMV' && r.cambio != null) out.push({ nombre: r.nombre, name_en: r.name_en, name_pt: r.name_pt, cambio: r.cambio, grupo: 'bolsa' }); });
    ((state.heat && state.heat.mapa) || []).forEach(function (m) { if (m.cambio != null) out.push({ nombre: m.nombre, name_en: m.name_en, name_pt: m.name_pt, cambio: m.cambio, grupo: 'bolsa' }); });
    return out;
  }
  function barsFigure(mercado) {
    var rows = mercado === 'latam' ? latamRows() : (state.latest.mercados || []).filter(function (r) { return r.cambio != null && (mercado === 'global' ? r.grupo === 'bolsa' : ['IPC BMV', 'USD/MXN', 'Mezcla mexicana', 'Bono M 10 años', 'Cetes 28 días'].indexOf(r.nombre) >= 0); });
    if (!rows.length) return null;
    var pct = rows.filter(function (r) { return r.grupo !== 'bono'; });
    var max = Math.max.apply(null, pct.map(function (r) { return Math.abs(r.cambio); }).concat([0.5]));
    var fig = el('figure', 'nx-figure');
    fig.appendChild(el('div', 'fh', mercado === 'global' ? t('figG') : mercado === 'latam' ? tx('América Latina hoy', 'Latin America today', 'América Latina hoje') : t('figM')));
    var g = el('div', 'nx-bars');
    rows.slice().sort(function (a, b) { return b.cambio - a.cambio; }).forEach(function (r) {
      var cls = r.cambio >= 0 ? 'up' : 'down';
      g.appendChild(el('span', 'lb', mname(r)));
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
    var L = pick(b); var frag = document.createDocumentFragment();
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
  function shareRow(b, L) {
    var url = 'https://mrsupplychain.ai/noticias/brief/' + b.id + '/';
    var u = function (src) { return url + '?utm_source=' + src + '&utm_medium=social&utm_campaign=noticias'; };
    var e = encodeURIComponent, row = el('div', 'nx-share');
    [['LinkedIn', 'https://www.linkedin.com/sharing/share-offsite/?url=' + e(u('linkedin'))],
     ['X', 'https://x.com/intent/post?text=' + e(L.titular) + '&url=' + e(u('x')) + '&hashtags=MrSupplyChainMexico'],
     ['WhatsApp', 'https://wa.me/?text=' + e(L.titular + ' ' + u('whatsapp'))],
     ['Telegram', 'https://t.me/share/url?url=' + e(u('telegram')) + '&text=' + e(L.titular)]].forEach(function (x) {
      var a = el('a', null, x[0]); a.href = x[1]; a.target = '_blank'; a.rel = 'noopener'; row.appendChild(a);
    });
    var c = el('button', null, tx('Copiar enlace', 'Copy link', 'Copiar link')); c.type = 'button';
    c.addEventListener('click', function () { try { navigator.clipboard.writeText(u('copy')); c.textContent = tx('Copiado', 'Copied', 'Copiado'); } catch (err) {} });
    row.appendChild(c);
    var p = el('a', null, tx('Página de la nota →', 'Story page →', 'Página da matéria →')); p.href = 'brief/' + b.id + '/'; row.appendChild(p);
    return row;
  }
  function renderBrief() {
    var box = document.getElementById('nx-brief'); if (!box || !state.latest) return;
    box.replaceChildren();
    var b = state.latest.briefs && state.latest.briefs[state.tab]; if (!b) return;
    var L = pick(b);
    var k = el('p', 'nx-kick');
    k.appendChild(document.createTextNode(MOM[state.lang][b.momento] || b.momento));
    k.appendChild(el('span', 'sep', '|'));
    k.appendChild(document.createTextNode(MKT[state.lang][b.mercado]));
    if (b.fin_de_semana) { k.appendChild(el('span', 'sep', '|')); k.appendChild(el('span', 'wk', t('wkk'))); }
    box.appendChild(k);
    box.appendChild(el('h1', 'nx-hl', L.titular));
    var by = el('div', 'nx-byline'); by.appendChild(el('b', null, t('by'))); by.appendChild(document.createTextNode('· ' + fmtDate(b.fecha) + ' · ' + b.hora)); box.appendChild(by);
    box.appendChild(shareRow(b, L));
    var fig = barsFigure(b.mercado); if (fig) box.appendChild(fig);
    box.appendChild(briefBody(b));
  }
  function renderOther() {
    var box = document.getElementById('nx-other'); if (!box || !state.latest) return;
    box.replaceChildren();
    var order = ['global', 'latam', 'mexico'].filter(function (k) { return k !== state.tab && state.latest.briefs && state.latest.briefs[k]; }); var other = order[0];
    var b = other && state.latest.briefs[other]; if (!b) { box.hidden = true; return; }
    box.hidden = false;
    var L = pick(b);
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
      d.appendChild(el('span', 't', tx(x.titular_es, x.titular_en || x.titular_es, x.titular_pt || x.titular_es)));
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
      li.appendChild(d); li.appendChild(el('div', null, pick(a))); ul.appendChild(li);
    });
  }

  /* ---------- Mapa ---------- */
  function renderMap() {
    var box = document.getElementById('nx-map'); if (!box || !state.latest || !state.world || !window.d3 || !window.topojson || !d3.geoNaturalEarth1) return;
    box.replaceChildren();
    var view = state.mapView || (window.innerWidth < 700 ? 'americas' : 'mundo');
    var tabs = document.getElementById('nx-map-tabs');
    if (tabs) {
      tabs.replaceChildren();
      [['americas', tx('Américas', 'Americas', 'Américas')], ['mundo', tx('Mundo', 'World', 'Mundo')]].forEach(function (v) {
        var bt = el('button', null, v[1]); bt.type = 'button'; bt.setAttribute('aria-selected', String(v[0] === view));
        bt.addEventListener('click', function () { state.mapView = v[0]; renderMap(); }); tabs.appendChild(bt);
      });
    }
    var all = (state.latest.mercados || []).filter(function (r) { return CITY[r.nombre] && r.cambio != null; }).map(function (r) {
      var c = CITY[r.nombre]; return { key: r.nombre, nombre: r.nombre, name_en: r.name_en, name_pt: r.name_pt, cambio: r.cambio, grupo: r.grupo, lon: c[0], lat: c[1], ciudad: c[2], ciudad_en: CITY_EN[c[2]], side: c[3], dy: c[4], am: c[0] < -30 };
    });
    ((state.heat && state.heat.mapa) || []).forEach(function (m) { if (m.cambio != null) all.push({ key: m.id, nombre: m.nombre, name_en: m.name_en, name_pt: m.name_pt, cambio: m.cambio, grupo: 'bolsa', lon: m.lon, lat: m.lat, ciudad: m.ciudad, ciudad_en: m.ciudad_en, ciudad_pt: m.ciudad_pt, am: true, latam: true }); });
    var rows = view === 'americas' ? all.filter(function (r) { return r.am; }) : all;
    var W = 1000, H = view === 'americas' ? 640 : 470;
    var svg = sv('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': tx('Mapa de bolsas del día', 'Map of today’s stock markets', 'Mapa das bolsas do dia') });
    var land = topojson.feature(state.world, state.world.objects.countries);
    var proj = d3.geoNaturalEarth1();
    if (view === 'americas') proj.fitExtent([[20, 10], [W - 20, H - 10]], { type: 'MultiPoint', coordinates: [[-128, 60], [-30, -56], [-128, -56], [-30, 60]] });
    else proj.fitExtent([[10, 10], [W - 10, H - 10]], { type: 'Sphere' });
    var path = d3.geoPath(proj);
    var g = sv('g');
    land.features.forEach(function (f) { if (f.id === '010') return; g.appendChild(sv('path', { d: path(f), 'class': 'land' + (HL[f.id] ? ' hl' : '') })); });
    svg.appendChild(g);
    var max = Math.max.apply(null, rows.map(function (r) { return Math.abs(r.cambio); }).concat([0.5]));
    rows.forEach(function (r) {
      var p = proj([r.lon, r.lat]); var cls = r.cambio >= 0 ? 'up' : 'down';
      var rad = (view === 'americas' ? 8 : 7) + Math.abs(r.cambio) / max * (view === 'americas' ? 18 : 16);
      svg.appendChild(sv('circle', { cx: p[0], cy: p[1], r: rad, 'class': 'ring ' + cls }));
      svg.appendChild(sv('circle', { cx: p[0], cy: p[1], r: rad * 0.62, 'class': 'bub ' + cls }));
      if (view === 'mundo' && r.latam && ['bovespa', 'tsx'].indexOf(r.key) < 0) return;
      var side, dy;
      if (view === 'americas' && AM_LBL[r.key]) { side = AM_LBL[r.key][0]; dy = AM_LBL[r.key][1]; }
      else { side = r.side || (p[0] < W * 0.8 ? 'right' : 'left'); dy = r.dy || 0; if (view === 'mundo' && r.key === 'tsx') dy = -16; if (view === 'mundo' && r.key === 'S&P 500') dy = 10; }
      var right = side !== 'left'; var x = p[0] + (right ? rad + 6 : -rad - 6); var anchor = right ? 'start' : 'end';
      svg.appendChild(sv('text', { x: x, y: p[1] - 3 + dy, 'text-anchor': anchor, 'class': 'lbl' }, mname(r) + ' · ' + city(r)));
      svg.appendChild(sv('text', { x: x, y: p[1] + 13 + dy, 'text-anchor': anchor, 'class': 'lbl2 ' + cls }, fmtChg(r)));
    });
    box.appendChild(svg);
    if (rows.length) {
      var nm = mname;
      var srt = rows.slice().sort(function (a, b) { return b.cambio - a.cambio; }), ups = rows.filter(function (r) { return r.cambio > 0; }).length;
      var best = srt[0], worst = srt[srt.length - 1];
      var t1 = tx(ups + ' de ' + rows.length + ' regiones subieron. La mejor: ' + nm(best) + ' (' + pc(best.cambio) + '); la más débil: ' + nm(worst) + ' (' + pc(worst.cambio) + ').',
                  ups + ' of ' + rows.length + ' regions closed higher. Best: ' + nm(best) + ' (' + pc(best.cambio) + '); weakest: ' + nm(worst) + ' (' + pc(worst.cambio) + ').',
                  ups + ' de ' + rows.length + ' regiões fecharam em alta. A melhor: ' + nm(best) + ' (' + pc(best.cambio) + '); a mais fraca: ' + nm(worst) + ' (' + pc(worst.cambio) + ').');
      var t2 = ups <= rows.length / 2
        ? tx('Un día de aversión al riesgo suele traer dólar más fuerte y compradores más cautelosos: espera que tus proveedores cuiden su caja y pidan mejores plazos de pago.',
             'A broad risk-off day usually brings a stronger dollar and more cautious buyers: expect suppliers to protect cash and stretch payment terms.',
             'Um dia de aversão ao risco costuma trazer dólar mais forte e compradores mais cautelosos: espere que seus fornecedores preservem o caixa e peçam prazos de pagamento maiores.')
        : tx('Un día positivo en casi todas las regiones respalda los planes de demanda y capacidad; buen momento para cerrar compromisos de volumen.',
             'A positive day across regions supports demand and capacity plans; a good moment to close volume commitments.',
             'Um dia positivo em quase todas as regiões sustenta os planos de demanda e capacidade; bom momento para fechar compromissos de volume.');
      interp('nx-map', t1, t2);
    }
  }


  /* ---------- Interpretación bajo cada gráfico (se calcula con los datos) ---------- */
  function interp(boxId, txt, scm) {
    var box = document.getElementById(boxId); if (!box) return;
    var host = box.parentNode, p = host.querySelector(':scope > .nx-interp');
    if (!txt) { if (p) p.remove(); return; }
    if (!p) { p = el('p', 'nx-interp'); if (box.nextSibling) host.insertBefore(p, box.nextSibling); else host.appendChild(p); }
    p.replaceChildren();
    p.appendChild(el('b', null, tx('Lectura: ', 'What it means: ', 'Leitura: ')));
    p.appendChild(document.createTextNode(txt));
    if (scm) { p.appendChild(el('br')); p.appendChild(el('b', null, 'Supply chain: ')); p.appendChild(document.createTextNode(scm)); }
  }
  function pc(v) { return sgn(v, 2) + '%'; }

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
      f.svg.appendChild(sv('text', { x: m.l - 10, y: cy + 4, 'text-anchor': 'end', 'class': 'nx-ax', style: 'fill:#15171b;font-weight:600' }, lname(r)));
      if (r.tasa != null && r.inflacion != null) f.svg.appendChild(sv('line', { x1: x(r.tasa), x2: x(r.inflacion), y1: cy, y2: cy, stroke: '#c9ced6', 'stroke-width': 3, 'stroke-linecap': 'round' }));
      [['tasa', '#1e4f9c', t('tasa')], ['inflacion', '#b87514', t('infl')]].forEach(function (s) {
        if (r[s[0]] == null) return;
        var c = sv('circle', { cx: x(r[s[0]]), cy: cy, r: 6.5, fill: s[1], stroke: '#fff', 'stroke-width': 2 });
        c.addEventListener('mouseenter', function () { showTip(f, x(r[s[0]]), cy, lname(r) + ' · ' + s[2] + ' ' + num(r[s[0]], 2) + '%'); });
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
    en: { tec: 'Technology', com: 'Communication', cons: 'Consumer discretionary', basic: 'Consumer staples', fin: 'Financials', salud: 'Health care', ind: 'Industrials', ener: 'Energy', mat: 'Materials', util: 'Utilities', inmo: 'Real estate' },
    pt: { tec: 'Tecnologia', com: 'Comunicações', cons: 'Consumo discricionário', basic: 'Consumo básico', fin: 'Financeiro', salud: 'Saúde', ind: 'Industrial', ener: 'Energia', mat: 'Materiais', util: 'Serviços públicos', inmo: 'Imobiliário' }
  };
  function mix(a, b, k) { var pa = [parseInt(a.slice(1, 3), 16), parseInt(a.slice(3, 5), 16), parseInt(a.slice(5, 7), 16)], pb = [parseInt(b.slice(1, 3), 16), parseInt(b.slice(3, 5), 16), parseInt(b.slice(5, 7), 16)]; return 'rgb(' + pa.map(function (v, i) { return Math.round(v + (pb[i] - v) * k); }).join(',') + ')'; }
  function heatColor(c) { var k = Math.min(1, Math.abs(c) / 3); return c >= 0 ? mix('#e4e2dc', '#13804f', Math.pow(k, 0.8)) : mix('#e4e2dc', '#b3261e', Math.pow(k, 0.8)); }
  function renderHeat() {
    var box = document.getElementById('nx-heat'), pills = document.getElementById('nx-heat-tabs'), src = document.getElementById('nx-heat-src');
    if (!box || !pills) return;
    box.replaceChildren(); pills.replaceChildren(); if (src) src.textContent = '';
    var H = state.heat;
    var list = H && H.indices ? H.indices.filter(function (x) { return x.mercado === state.tab; }) : [];
    if (!list.length || !window.d3 || !d3.treemap) { box.appendChild(el('p', 'nx-empty', tx('El mapa de calor se está generando; aparecerá en unos minutos.', 'The stock heatmap is being generated; it will appear in a few minutes.', 'O mapa de calor está sendo gerado; aparecerá em alguns minutos.'))); return; }
    var cur = state.heatIdx[state.tab]; if (!list.some(function (x) { return x.id === cur; })) cur = state.heatIdx[state.tab] = list[0].id;
    if (list.length > 1) list.forEach(function (x) {
      var b = el('button', null, lname(x)); b.type = 'button'; b.setAttribute('role', 'tab'); b.setAttribute('aria-selected', String(x.id === cur));
      b.addEventListener('click', function () { state.heatIdx[state.tab] = x.id; renderHeat(); });
      pills.appendChild(b);
    });
    var idx = list.filter(function (x) { return x.id === cur; })[0];
    var W = Math.max(300, box.clientWidth || 340), narrow = W < 560, Hh = narrow ? 460 : Math.round(Math.min(560, Math.max(380, W * 0.46)));
    var groups = {}; idx.acciones.forEach(function (a) { (groups[a.s] = groups[a.s] || []).push(a); });
    var root = d3.hierarchy({ children: Object.keys(groups).map(function (k) { return { s: k, children: groups[k] }; }) }).sum(function (d) { return d.cap || 0; }).sort(function (a, b) { return b.value - a.value; });
    d3.treemap().size([W, Hh]).paddingOuter(1).paddingTop(function (d) { return d.depth === 1 ? 17 : 0; }).paddingInner(1.5).round(true).tile(d3.treemapSquarify.ratio(1.2))(root);
    var svg = sv('svg', { viewBox: '0 0 ' + W + ' ' + Hh, role: 'img', 'aria-label': lname(idx) }); box.appendChild(svg);
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
    (function () {
      var A = idx.acciones, SL = SECT[state.lang];
      var tot = A.reduce(function (z, a) { return z + a.cap; }, 0);
      var contrib = A.map(function (a) { return { a: a, c: a.cap * a.chg / tot }; }).sort(function (x, y) { return x.c - y.c; });
      var neg = contrib[0], pos = contrib[contrib.length - 1];
      var agg = {}; A.forEach(function (a) { var g = agg[a.s] = agg[a.s] || { w: 0, v: 0 }; g.w += a.cap; g.v += a.cap * a.chg; });
      var sec = Object.keys(agg).map(function (k) { return { k: k, c: agg[k].v / agg[k].w }; }).sort(function (x, y) { return x.c - y.c; });
      var ws = sec[0], bs = sec[sec.length - 1], ups = A.filter(function (a) { return a.chg > 0; }).length;
      var nmI = lname(idx);
      var t1 = tx('En el ' + nmI + ', ' + neg.a.n + ' (' + pc(neg.a.chg) + ') fue la que más restó y ' + pos.a.n + ' (' + pc(pos.a.chg) + ') la que más sumó; ' + ups + ' de ' + A.length + ' emisoras subieron. Sector más fuerte: ' + SL[bs.k] + ' (' + pc(bs.c) + '); más débil: ' + SL[ws.k] + ' (' + pc(ws.c) + ').',
                  'In the ' + nmI + ', ' + neg.a.n + ' (' + pc(neg.a.chg) + ') weighed most and ' + pos.a.n + ' (' + pc(pos.a.chg) + ') helped most; ' + ups + ' of ' + A.length + ' stocks rose. Strongest sector: ' + SL[bs.k] + ' (' + pc(bs.c) + '); weakest: ' + SL[ws.k] + ' (' + pc(ws.c) + ').',
                  'No ' + nmI + ', ' + neg.a.n + ' (' + pc(neg.a.chg) + ') foi a que mais pesou e ' + pos.a.n + ' (' + pc(pos.a.chg) + ') a que mais contribuiu; ' + ups + ' de ' + A.length + ' ações subiram. Setor mais forte: ' + SL[bs.k] + ' (' + pc(bs.c) + '); mais fraco: ' + SL[ws.k] + ' (' + pc(ws.c) + ').');
      var t2 = tx('Los movimientos fuertes en un sector proveedor (hoy, ' + SL[ws.k].toLowerCase() + ') suelen anticipar cambios de precio, capacidad o inversión: revisa tu exposición a proveedores clave de ese sector.',
                  'Sharp moves in a supplier sector (' + SL[ws.k].toLowerCase() + ' today) often precede price, capacity or capex changes: check exposure to your key suppliers there.',
                  'Movimentos fortes em um setor fornecedor (hoje, ' + SL[ws.k].toLowerCase() + ') costumam antecipar mudanças de preço, capacidade ou investimento: revise sua exposição a fornecedores-chave desse setor.');
      interp('nx-heat', t1, t2);
    })();
    if (src) {
      src.replaceChildren();
      var up = idx.acciones.filter(function (a) { return a.chg > 0; }).length;
      var now = Date.now(), live = idx.abre && idx.cierra && now >= Date.parse(idx.abre) && now < Date.parse(idx.cierra);
      var hh = function (iso) { return new Date(iso).toLocaleTimeString(loc(), { hour: '2-digit', minute: '2-digit', timeZone: 'America/Mexico_City' }); };
      var badge = el('span', 'nx-hbadge' + (live ? ' live' : ''), live ? tx('En vivo', 'Live', 'Ao vivo') : tx('Cierre', 'Close', 'Fechamento'));
      src.appendChild(badge);
      src.appendChild(document.createTextNode(' ' + (live
        ? tx('Actualizado ', 'Updated ', 'Atualizado ') + hh(idx.actualizado || H.actualizado) + ' CDMX · '
        : tx('Sesión del ', 'Session of ', 'Sessão de ') + fmtDate(idx.fecha) + ' · ')
        + tx(up + ' de ' + idx.acciones.length + ' suben · Datos: ', up + ' of ' + idx.acciones.length + ' up · Data: ', up + ' de ' + idx.acciones.length + ' em alta · Dados: ') + (H.fuente || 'Yahoo Finance') + tx(', retraso ~15 min', ', ~15 min delay', ', atraso de ~15 min')));
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
      g.appendChild(el('span', 'lb', mname(r)));
      var tr = el('span', 'tr'); var br = el('span', 'br ' + cls); var w = Math.abs(r.cambio) / max * 50;
      br.style.width = w + '%'; br.style.left = r.cambio >= 0 ? '50%' : (50 - w) + '%'; tr.appendChild(br); g.appendChild(tr);
      g.appendChild(el('span', 'vl ' + cls, fmtChg(r)));
    });
    box.appendChild(g);
    var nm = mname;
    var srt = rows.slice().sort(function (a, b) { return b.cambio - a.cambio; }), up = srt[0], dn = srt[srt.length - 1];
    var oil = rows.filter(function (r) { return /WTI|Brent/.test(r.nombre); })[0], mxn = rows.filter(function (r) { return r.nombre === 'USD/MXN'; })[0];
    var t1 = tx('Lo que más subió: ' + nm(up) + ' (' + fmtChg(up) + '); lo que más bajó: ' + nm(dn) + ' (' + fmtChg(dn) + ').',
                'Biggest rise: ' + nm(up) + ' (' + fmtChg(up) + '); biggest drop: ' + nm(dn) + ' (' + fmtChg(dn) + ').',
                'Maior alta: ' + nm(up) + ' (' + fmtChg(up) + '); maior queda: ' + nm(dn) + ' (' + fmtChg(dn) + ').');
    var bits = [];
    if (oil) bits.push(oil.cambio > 0 ? tx('el petróleo al alza se traslada a recargos por combustible en días', 'higher oil feeds fuel surcharges within days', 'o petróleo em alta chega às sobretaxas de combustível em poucos dias')
                                      : tx('el petróleo a la baja da margen para renegociar recargos por combustible', 'softer oil gives room to renegotiate fuel surcharges', 'o petróleo em baixa abre espaço para renegociar as sobretaxas de combustível'));
    if (mxn) bits.push(mxn.cambio > 0 ? tx('el peso más débil encarece lo que compras en dólares', 'a weaker peso makes dollar-priced imports more expensive', 'o peso mexicano mais fraco encarece o que você compra em dólares')
                                      : tx('el peso más fuerte abarata lo que compras en dólares', 'a stronger peso lowers the cost of dollar purchases', 'o peso mexicano mais forte barateia o que você compra em dólares'));
    interp('nx-ch-cmd', t1, bits.length ? bits.join('; ') + '.' : '');
  }
  function barsInto(boxId, rows, fmt) {
    var box = document.getElementById(boxId); if (!box) return;
    box.replaceChildren(); if (!rows.length) return;
    var max = Math.max.apply(null, rows.map(function (r) { return Math.abs(r.v); }).concat([0.5]));
    var g = el('div', 'nx-bars');
    rows.slice().sort(function (a, b) { return b.v - a.v; }).forEach(function (r) {
      var cls = r.good == null ? (r.v >= 0 ? 'up' : 'down') : (r.good ? 'up' : 'down');
      g.appendChild(el('span', 'lb', r.l));
      var tr = el('span', 'tr'), br = el('span', 'br ' + cls), w = Math.abs(r.v) / max * 50;
      br.style.width = w + '%'; br.style.left = r.v >= 0 ? '50%' : (50 - w) + '%'; tr.appendChild(br); g.appendChild(tr);
      g.appendChild(el('span', 'vl ' + cls, fmt ? fmt(r) : pc(r.v)));
    });
    box.appendChild(g);
  }
  function renderLatamCharts() {
    var idx = latamRows().map(function (r) { return { l: mname(r), v: r.cambio }; });
    barsInto('nx-ch-latidx', idx);
    if (idx.length) {
      var srt = idx.slice().sort(function (a, b) { return b.v - a.v; }), ups = idx.filter(function (r) { return r.v > 0; }).length;
      interp('nx-ch-latidx', tx(ups + ' de ' + idx.length + ' mercados subieron. El mejor: ' + srt[0].l + ' (' + pc(srt[0].v) + '); el más débil: ' + srt[srt.length - 1].l + ' (' + pc(srt[srt.length - 1].v) + ').',
                                ups + ' of ' + idx.length + ' markets rose. Best: ' + srt[0].l + ' (' + pc(srt[0].v) + '); weakest: ' + srt[srt.length - 1].l + ' (' + pc(srt[srt.length - 1].v) + ').',
                                ups + ' de ' + idx.length + ' mercados subiram. O melhor: ' + srt[0].l + ' (' + pc(srt[0].v) + '); o mais fraco: ' + srt[srt.length - 1].l + ' (' + pc(srt[srt.length - 1].v) + ').'),
        tx('Las bolsas de la región se mueven con materias primas y el dólar: la debilidad en mineras, petroleras o retail suele anticipar crédito más caro y plazos de pago más largos entre proveedores de la región.',
           'Regional markets move with commodities and the dollar: weakness in copper, oil-exporter or retail stocks often precedes tighter credit and stretched payment terms among suppliers in the region.',
           'As bolsas da região se movem com as commodities e o dólar: a fraqueza em mineradoras, petroleiras ou varejo costuma antecipar crédito mais caro e prazos de pagamento mais longos entre fornecedores da região.'));
    }
    var mxn = (state.latest.mercados || []).filter(function (r) { return r.nombre === 'USD/MXN' && r.cambio != null; })[0];
    var fx = ((state.heat && state.heat.divisas) || []).filter(function (d) { return d.cambio != null; }).map(function (d) {
      var v = d.par === 'USD/MXN' && mxn ? mxn.cambio : d.cambio; // el peso usa el mismo dato que el resto de la página
      return { l: lname(d) + ' (' + d.par + ')', v: v, good: v <= 0, d: d };
    });
    barsInto('nx-ch-latfx', fx, function (r) { return sgn(r.v, 2) + '%'; });
    if (fx.length) {
      var weak = fx.slice().sort(function (a, b) { return b.v - a.v; })[0], strong = fx.slice().sort(function (a, b) { return a.v - b.v; })[0];
      interp('nx-ch-latfx', tx('La moneda que más se debilitó: ' + lname(weak.d) + ' (' + pc(weak.v) + '); la que mejor se sostuvo: ' + lname(strong.d) + ' (' + pc(strong.v) + ').',
                               'Weakest against the dollar: ' + lname(weak.d) + ' (' + pc(weak.v) + '); strongest: ' + lname(strong.d) + ' (' + pc(strong.v) + ').',
                               'A moeda que mais se desvalorizou: ' + lname(weak.d) + ' (' + pc(weak.v) + '); a que melhor se sustentou: ' + lname(strong.d) + ' (' + pc(strong.v) + ').'),
        tx('Si compras o vendes entre países de la región, el tipo de cambio mueve costos y márgenes aunque el precio en dólares no cambie; revisa la moneda de facturación y las cláusulas cambiarias por país.',
           'If you buy or sell between Latin American countries, currency moves change landed costs and margins even when dollar prices stay the same; review invoicing currency and FX clauses by country.',
           'Se você compra ou vende entre países da região, o câmbio altera custos e margens mesmo quando o preço em dólares não muda; revise a moeda de faturamento e as cláusulas cambiais por país.'));
    }
  }
  function renderCharts() {
    var views = document.querySelectorAll('.nx-chgrid[data-view]');
    for (var i = 0; i < views.length; i++) views[i].hidden = views[i].getAttribute('data-view') !== state.tab;
    renderHeat();
    var S = state.series;
    if (state.tab === 'latam') { renderLatamCharts(); return; }
    if (state.tab === 'mexico') {
      if (!S) return;
      var d2 = function (iso) { var p = iso.split('-'); return (+p[2]) + ' ' + MES[state.lang][+p[1] - 1]; };
      lineChart('nx-ch-usd', S.usdmxn || [], { series: [{ k: 'v', c: '#1e4f9c', area: true }], fx: function (p) { return d2(p.fecha); }, fy: function (v) { return num(v, 2); } });
      lineChart('nx-ch-banxico', S.banxico || [], { series: [{ k: 'tasa', c: '#1e4f9c', step: true, name: t('banx') }, { k: 'inflacion', c: '#b87514', dots: true, name: t('infl') }], fx: function (p) { var q = p.mes.split('-'); return MES[state.lang][+q[1] - 1] + (q[1] === '01' || q[1] === '12' ? ' ' + q[0].slice(2) : ''); }, fy: function (v) { return num(v, 2) + '%'; } });
      var U = S.usdmxn || [];
      if (U.length > 1) {
        var f0 = U[0], f1 = U[U.length - 1], ch = (f1.v / f0.v - 1) * 100;
        var hi = U.reduce(function (a, b) { return b.v > a.v ? b : a; }), lo = U.reduce(function (a, b) { return b.v < a.v ? b : a; });
        interp('nx-ch-usd', tx(
          'El peso pasó de ' + num(f0.v, 2) + ' a ' + num(f1.v, 2) + ' por dólar (' + pc(ch) + ') entre el ' + d2(f0.fecha) + ' y el ' + d2(f1.fecha) + '; rango de ' + num(lo.v, 2) + ' a ' + num(hi.v, 2) + '.',
          'The peso went from ' + num(f0.v, 2) + ' to ' + num(f1.v, 2) + ' per dollar (' + pc(ch) + ') between ' + d2(f0.fecha) + ' and ' + d2(f1.fecha) + '; range ' + num(lo.v, 2) + '–' + num(hi.v, 2) + '.',
          'O peso mexicano passou de ' + num(f0.v, 2) + ' para ' + num(f1.v, 2) + ' por dólar (' + pc(ch) + ') entre ' + d2(f0.fecha) + ' e ' + d2(f1.fecha) + '; faixa de ' + num(lo.v, 2) + ' a ' + num(hi.v, 2) + '.'),
          ch > 0 ? tx('Cada 1% de depreciación suma cerca de 1% al costo puesto en planta de los insumos en dólares; actualiza el tipo de cambio presupuestal y evalúa cubrir pagos próximos.',
                      'Every 1% of depreciation adds roughly 1% to the landed cost of dollar-priced inputs; update budget exchange rates and consider hedging upcoming payments.',
                      'Cada 1% de depreciação acrescenta cerca de 1% ao custo posto na planta dos insumos em dólares; atualize o câmbio orçamentário e avalie fazer hedge dos próximos pagamentos.')
                 : tx('Un peso más fuerte abarata las importaciones; buena ventana para pagar o adelantar compras en dólares.',
                      'A stronger peso lowers import costs; a good window to pay or pre-buy dollar-priced inputs.',
                      'Um peso mais forte barateia as importações; boa janela para pagar ou antecipar compras em dólares.'));
      }
      var B = (S.banxico || []).filter(function (r) { return r.tasa != null; });
      if (B.length) {
        var bl = B[B.length - 1], b0 = B[0], infl = null;
        for (var j = (S.banxico || []).length - 1; j >= 0; j--) if (S.banxico[j].inflacion != null) { infl = S.banxico[j].inflacion; break; }
        var real = infl != null ? bl.tasa - infl : null;
        interp('nx-ch-banxico', tx(
          'La tasa de Banxico está en ' + num(bl.tasa, 2) + '% (' + sgn(bl.tasa - b0.tasa, 2) + ' pp en el periodo)' + (infl != null ? ' y la inflación en ' + num(infl, 2) + '%: una tasa real de ' + num(real, 2) + ' pp.' : '.'),
          'Banxico\'s rate is ' + num(bl.tasa, 2) + '% (' + sgn(bl.tasa - b0.tasa, 2) + ' pp in the period)' + (infl != null ? ' and inflation ' + num(infl, 2) + '%, a real rate of ' + num(real, 2) + ' pp.' : '.'),
          'A taxa do Banxico está em ' + num(bl.tasa, 2) + '% (' + sgn(bl.tasa - b0.tasa, 2) + ' p.p. no período)' + (infl != null ? ' e a inflação em ' + num(infl, 2) + '%: uma taxa real de ' + num(real, 2) + ' p.p.' : '.')),
          real != null && real > 2 ? tx('Financiar inventario en pesos sigue siendo caro: cada día extra de inventario cuesta más en capital de trabajo.',
                                        'Financing inventory in pesos remains expensive: every extra day of stock costs more in working capital.',
                                        'Financiar estoque em pesos continua caro: cada dia extra de estoque custa mais em capital de giro.')
                                   : tx('El crédito se abarata en términos reales, lo que alivia el costo de mantener inventario.',
                                        'Credit is getting cheaper in real terms, which eases the cost of carrying inventory.',
                                        'O crédito fica mais barato em termos reais, o que alivia o custo de manter estoque.'));
      }
    } else {
      if (S) {
        dumbbell('nx-ch-rates', S.economias || []);
        var E = (S.economias || []).filter(function (r) { return r.tasa != null && r.inflacion != null; }).map(function (r) { return { n: lname(r), r: r.tasa - r.inflacion }; }).sort(function (a, b) { return b.r - a.r; });
        if (E.length) {
          var neg = E.filter(function (e) { return e.r < 0; }).map(function (e) { return e.n; });
          interp('nx-ch-rates', tx(
            E[0].n + ' tiene la tasa real más alta (' + sgn(E[0].r, 1) + ' pp) y ' + E[E.length - 1].n + ' la más baja (' + sgn(E[E.length - 1].r, 1) + ' pp).' + (neg.length ? ' Tasa real negativa en: ' + neg.join(', ') + '.' : ''),
            E[0].n + ' has the highest real rate (' + sgn(E[0].r, 1) + ' pp) and ' + E[E.length - 1].n + ' the lowest (' + sgn(E[E.length - 1].r, 1) + ' pp).' + (neg.length ? ' Negative real rates in: ' + neg.join(', ') + '.' : ''),
            E[0].n + ' tem a maior taxa real (' + sgn(E[0].r, 1) + ' p.p.) e ' + E[E.length - 1].n + ' a menor (' + sgn(E[E.length - 1].r, 1) + ' p.p.).' + (neg.length ? ' Taxa real negativa em: ' + neg.join(', ') + '.' : '')),
            tx('Donde la tasa real es alta, mantener inventario y financiar proveedores cuesta más; donde es negativa, la moneda tiende a debilitarse, lo que cambia el costo de abastecerte de esa región.',
               'Where real rates are high, carrying inventory and supplier financing cost more; where they are negative, currencies tend to weaken, which affects sourcing from those regions.',
               'Onde a taxa real é alta, manter estoque e financiar fornecedores custa mais; onde é negativa, a moeda tende a se desvalorizar, o que muda o custo de se abastecer naquela região.'));
        }
      }
      cmdChart('nx-ch-cmd');
    }
  }
  function setTab(tab) {
    state.tab = tab;
    var all = document.querySelectorAll('.nx-tabs button[data-tab]');
    for (var m = 0; m < all.length; m++) all[m].setAttribute('aria-selected', String(all[m].getAttribute('data-tab') === tab));
    renderBrief(); renderOther(); renderCharts(); renderTrends();
    state.mapView = tab === 'global' ? 'mundo' : 'americas'; renderMap();
  }


  /* ---------- Tendencias por industria ---------- */
  function renderTrends() {
    var T = state.trends, grid = document.getElementById('nx-trends'); if (!grid) return;
    var hl = document.getElementById('nx-trhl'), note = document.getElementById('nx-trnote');
    grid.replaceChildren();
    if (!T || !T.items) { if (hl) hl.textContent = ''; return; }
    if (hl) hl.textContent = T.titular ? pick(T.titular) : '';
    if (note) note.textContent = tx('Lo que dicen las noticias del día de cada industria, leído para supply chain · ', 'What the day\'s news says about each industry, read for supply chain · ', 'O que as notícias do dia dizem sobre cada indústria, lido para supply chain · ') + fmtDate(T.fecha);
    var DIR = { up: [tx('Al alza', 'Rising', 'Em alta'), '▲'], down: [tx('A la baja', 'Falling', 'Em baixa'), '▼'], mixed: [tx('Mixta', 'Mixed', 'Misto'), '◆'] };
    var items = T.items.slice();
    if (state.tab === 'mexico') items.sort(function (a, b) { return (b.mx ? 1 : 0) - (a.mx ? 1 : 0); });
    if (state.tab === 'latam') items.sort(function (a, b) { return ((b.latam || b.mx) ? 1 : 0) - ((a.latam || a.mx) ? 1 : 0); });
    items.forEach(function (it) {
      var c = el('article', 'nx-tr ' + (it.dir || 'mixed'));
      var top = el('div', 'nx-trh');
      top.appendChild(el('span', 'nx-trn', tx(it.es, it.en || it.es, it.pt || it.es)));
      var d = DIR[it.dir] || DIR.mixed;
      var chip = el('span', 'nx-trd', d[1] + ' ' + d[0]); top.appendChild(chip);
      c.appendChild(top);
      var heat = el('div', 'nx-trheat'); heat.setAttribute('title', tx('Peso en las noticias de hoy', 'Weight in today\'s news', 'Peso nas notícias de hoje'));
      for (var i = 1; i <= 3; i++) heat.appendChild(el('i', i <= (it.calor || 1) ? 'on' : null));
      var ci = (it.calor || 1) - 1; heat.appendChild(el('span', null, tx('Relevancia ' + ['baja', 'media', 'alta'][ci], ['Low', 'Medium', 'High'][ci] + ' buzz', 'Relevância ' + ['baixa', 'média', 'alta'][ci])));
      c.appendChild(heat);
      c.appendChild(el('h3', null, pick(it.titular)));
      c.appendChild(el('p', null, pick(it.x)));
      var s = el('aside', 'nx-trscm'); s.appendChild(el('b', null, t('scm'))); s.appendChild(el('span', null, pick(it.scm))); c.appendChild(s);
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
    var H = state.heat; var id = state.tab === 'mexico' ? 'ipc' : state.tab === 'latam' ? 'ibovespa' : 'sp500';
    var idx = H && H.indices ? H.indices.filter(function (x) { return x.id === id; })[0] : null;
    if (h) h.textContent = tx('Sectores en bolsa hoy · ', 'Sectors in the market today · ', 'Setores na bolsa hoje · ') + (idx ? lname(idx) : (id === 'ipc' ? 'IPC' : id === 'ibovespa' ? 'Ibovespa' : 'S&P 500'));
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
    var SL = SECT[state.lang], b = rows[0], w = rows[rows.length - 1], upn = rows.filter(function (r) { return r.chg > 0; }).length;
    interp('nx-sect', tx(
      upn + ' de ' + rows.length + ' sectores subieron. ' + SL[b.k] + ' encabezó (' + pc(b.chg) + ') y ' + SL[w.k] + ' quedó al final (' + pc(w.chg) + ').',
      upn + ' of ' + rows.length + ' sectors rose. ' + SL[b.k] + ' led (' + pc(b.chg) + ') and ' + SL[w.k] + ' lagged (' + pc(w.chg) + ').',
      upn + ' de ' + rows.length + ' setores subiram. ' + SL[b.k] + ' liderou (' + pc(b.chg) + ') e ' + SL[w.k] + ' ficou por último (' + pc(w.chg) + ').'),
      tx('Léelo junto con las tarjetas de industria: cuando el mercado y las noticias apuntan al mismo lado, es más probable que la tendencia llegue a precios y tiempos de entrega de tus proveedores.',
         'Read it alongside the industry cards: when the market and the news point the same way, the trend is more likely to reach your suppliers\' prices and lead times.',
         'Leia junto com os cartões de indústria: quando o mercado e as notícias apontam para o mesmo lado, é mais provável que a tendência chegue aos preços e prazos de entrega dos seus fornecedores.'));
  }

  /* ---------- Lectura y archivo ---------- */
  function renderLectura() {
    var L = state.latest && state.latest.lectura && pick(state.latest.lectura);
    var v = document.getElementById('nx-verd'), box = document.getElementById('nx-themes'), ex = document.getElementById('nx-exec'), wa = document.getElementById('nx-watch');
    if (!L || !v || !box) return;
    v.textContent = L.titular;
    if (ex) ex.textContent = L.resumen || '';
    box.replaceChildren();
    var hiI = tx('Impacto alto', 'High impact', 'Impacto alto'), mdI = tx('Impacto medio', 'Medium impact', 'Impacto médio'), loI = tx('Impacto bajo', 'Low impact', 'Impacto baixo');
    var NIV = { alto: hiI, medio: mdI, bajo: loI, high: hiI, medium: mdI, low: loI, 'médio': mdI, baixo: loI };
    (L.temas || []).forEach(function (x, i) {
      var c = el('article', 'nx-th' + (x.analisis ? ' deep' : '')); c.style.setProperty('--c', COLORS[i % COLORS.length]);
      var hd = el('div', 'nx-thh'); hd.appendChild(el('b', null, x.tema)); if (x.nivel) hd.appendChild(el('span', 'nx-niv ' + x.nivel, NIV[x.nivel] || x.nivel)); c.appendChild(hd);
      if (!x.analisis) { c.appendChild(el('p', null, x.x)); box.appendChild(c); return; }
      if (x.palancas && x.palancas.length) { var pl = el('div', 'nx-pal'); x.palancas.forEach(function (p) { pl.appendChild(el('span', null, p)); }); c.appendChild(pl); }
      c.appendChild(el('p', 'nx-an', x.analisis));
      if (x.implicacion) { var im = el('p', 'nx-im'); im.appendChild(el('strong', null, tx('Implicación operativa. ', 'Operational implication. ', 'Implicação operacional. '))); im.appendChild(document.createTextNode(x.implicacion)); c.appendChild(im); }
      if (x.acciones && x.acciones.length) {
        c.appendChild(el('div', 'nx-acth', tx('Acciones recomendadas', 'Recommended actions', 'Ações recomendadas')));
        var ul = el('ul', 'nx-act'); x.acciones.forEach(function (a) { ul.appendChild(el('li', null, a)); }); c.appendChild(ul);
      }
      var ft = el('div', 'nx-thf');
      if (x.horizonte) { var h = el('span'); h.appendChild(el('em', null, tx('Horizonte: ', 'Horizon: ', 'Horizonte: '))); h.appendChild(document.createTextNode(x.horizonte)); ft.appendChild(h); }
      if (x.indicador) { var k = el('span'); k.appendChild(el('em', null, tx('Indicador a vigilar: ', 'Watch: ', 'Indicador a acompanhar: '))); k.appendChild(document.createTextNode(x.indicador)); ft.appendChild(k); }
      if (ft.firstChild) c.appendChild(ft);
      box.appendChild(c);
    });
    if (wa) {
      wa.replaceChildren();
      if (L.vigilar && L.vigilar.length) {
        wa.appendChild(el('h3', null, tx('En el radar', 'On the radar', 'No radar')));
        var ol = el('ol'); L.vigilar.forEach(function (w) { var li = el('li'); li.appendChild(el('b', null, w.cuando ? w.cuando + ' · ' + w.evento : w.evento)); li.appendChild(el('span', null, w.por_que)); ol.appendChild(li); });
        wa.appendChild(ol);
      }
    }
  }

  /* ---------- Redes y medios ---------- */
  function ago(iso) {
    var m = Math.max(1, Math.round((Date.now() - Date.parse(iso)) / 60000));
    if (m < 60) return tx('hace ' + m + ' min', m + ' min ago', 'há ' + m + ' min');
    var h = Math.round(m / 60); if (h < 24) return tx('hace ' + h + ' h', h + ' h ago', 'há ' + h + ' h');
    var d = Math.round(h / 24); return tx('hace ' + d + ' d', d + ' d ago', 'há ' + d + ' d');
  }
  function renderRedes() {
    var ul = document.getElementById('nx-rf'), tabs = document.getElementById('nx-rf-tabs'), note = document.getElementById('nx-rf-note'); if (!ul) return;
    var R = state.redes;
    ul.replaceChildren(); if (tabs) tabs.replaceChildren();
    if (!R || !R.items || !R.items.length) { ul.appendChild(el('li', 'nx-empty', tx('El feed se está preparando; se actualiza cada hora.', 'The feed is being prepared; it refreshes every hour.', 'O feed está sendo preparado; é atualizado a cada hora.'))); return; }
    var G = [['todo', tx('Todo', 'All', 'Tudo')], ['comunidad', tx('Comunidades', 'Communities', 'Comunidades')], ['medios', tx('Medios', 'Trade media', 'Mídia')], ['mexico', 'México']];
    var cur = state.rf || 'todo';
    G.forEach(function (g) {
      if (g[0] !== 'todo' && !R.items.some(function (x) { return x.grupo === g[0]; })) return;
      var b = el('button', null, g[1]); b.type = 'button'; b.setAttribute('aria-selected', String(g[0] === cur));
      b.addEventListener('click', function () { state.rf = g[0]; renderRedes(); }); tabs.appendChild(b);
    });
    if (note) note.textContent = tx('Lo más reciente de comunidades y medios especializados, actualizado cada hora · ', 'Latest from supply chain communities and trade media, updated hourly · ', 'O mais recente de comunidades e mídia especializada, atualizado a cada hora · ') + ago(R.actualizado);
    R.items.filter(function (x) { return cur === 'todo' || x.grupo === cur; }).slice(0, 24).forEach(function (x) {
      var li = el('li', 'nx-rfi ' + x.red);
      var top = el('div', 'nx-rfm');
      top.appendChild(el('span', 'nx-rfb ' + x.red, x.red === 'reddit' ? 'Reddit' : (x.grupo === 'mexico' ? 'MX' : tx('Medio', 'Media', 'Mídia'))));
      top.appendChild(el('span', 'nx-rfs', x.fuente));
      top.appendChild(el('span', 'nx-rft', ago(x.fecha)));
      li.appendChild(top);
      var a = el('a', 'nx-rfh', x.titulo); a.href = x.url; a.target = '_blank'; a.rel = 'noopener nofollow'; li.appendChild(a);
      if (x.resumen) li.appendChild(el('p', null, x.resumen));
      ul.appendChild(li);
    });
  }
  function renderFeed() {
    var ul = document.getElementById('nx-feed'); if (!ul || !state.index) return;
    ul.replaceChildren();
    var current = state.latest && state.latest.briefs ? Object.keys(state.latest.briefs).map(function (k) { return state.latest.briefs[k] && state.latest.briefs[k].id; }) : [];
    var items = (state.index.items || []).filter(function (x) { return current.indexOf(x.id) < 0; });
    if (!items.length) { ul.appendChild(el('li', 'nx-empty', t('none'))); return; }
    items.forEach(function (x) {
      var li = el('li');
      var h = el('button', 'h'); h.type = 'button'; h.setAttribute('aria-expanded', 'false');
      h.appendChild(el('span', 'd', fmtDate(x.fecha) + ' · ' + (MOM[state.lang][x.momento] || x.momento) + ' · ' + MKT[state.lang][x.mercado]));
      h.appendChild(el('span', 't', tx(x.titular_es, x.titular_en || x.titular_es, x.titular_pt || x.titular_es)));
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

  function renderAll() { applyLang(); renderToday(); renderStamp(); renderTicker(); renderBrief(); renderOther(); renderLatestList(); renderAgenda(); renderMap(); renderCharts(); renderTrends(); renderRedes(); renderLectura(); renderFeed(); }

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
    window.addEventListener('storage', function (e) { if (e.key === 'lang' && (e.newValue === 'es' || e.newValue === 'en' || e.newValue === 'pt')) { state.lang = e.newValue; renderAll(); } });
    var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(renderCharts, 200); });
    Promise.all([
      fetchJSON('latest.json'),
      fetchJSON('index.json').catch(function () { return { items: [] }; }),
      fetchJSON('series.json').catch(function () { return null; }),
      fetchJSON('world-110m.json', true).catch(function () { return null; }),
      fetchJSON('heatmaps.json').catch(function () { return null; }),
      fetchJSON('tendencias.json').catch(function () { return null; }),
      fetchJSON('redes.json').catch(function () { return null; })
    ]).then(function (res) { state.latest = res[0]; state.index = res[1]; state.series = res[2]; state.world = res[3]; state.heat = res[4]; state.trends = res[5]; state.redes = res[6]; renderAll(); })
      .catch(function () { var b = document.getElementById('nx-brief'); if (b) b.textContent = t('err'); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
