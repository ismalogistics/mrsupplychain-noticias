/* Mr. Supply Chain® México · bloque "Noticias de hoy" para el home (se monta después de la franja de cifras). */
(function () {
  'use strict';
  var BASE = '/noticias/';
  var NL = 'https://www.linkedin.com/newsletters/cadena-de-noticias-scm-7522126738555072512/';
  var T = {
    es: { k: 'Noticias', h: 'El pulso de mercados de hoy, leído para supply chain', all: 'Ver el portal de noticias', read: 'Leer', mom: { premercado: 'Premercado', apertura: 'Apertura', mediodia: 'Mediodía', cierre: 'Cierre' }, mkt: { global: 'Global', latam: 'LATAM', mexico: 'México' }, upd: 'Actualizado', nl: 'Cada viernes, los mercados de la semana leídos eslabón por eslabón para supply chain.', nlb: 'Recibir Cadena de Noticias SCM en LinkedIn' },
    en: { k: 'News', h: 'Today’s market pulse, read for supply chain', all: 'Go to the news portal', read: 'Read', mom: { premercado: 'Pre-market', apertura: 'Open', mediodia: 'Midday', cierre: 'Close' }, mkt: { global: 'Global', latam: 'LATAM', mexico: 'Mexico' }, upd: 'Updated', nl: 'Every Friday, the week’s markets read link by link for supply chain.', nlb: 'Get Cadena de Noticias SCM on LinkedIn' },
    pt: { k: 'Notícias', h: 'O pulso dos mercados de hoje, lido para supply chain', all: 'Ver o portal de notícias', read: 'Ler', mom: { premercado: 'Pré-mercado', apertura: 'Abertura', mediodia: 'Meio-dia', cierre: 'Fechamento' }, mkt: { global: 'Global', latam: 'LATAM', mexico: 'México' }, upd: 'Atualizado', nl: 'Toda sexta-feira, os mercados da semana lidos elo por elo para supply chain.', nlb: 'Receber Cadena de Noticias SCM no LinkedIn' }
  };
  var data = null, cur = null, box = null;
  // Especial destacado arriba del hero (se oculta solo después de HASTA).
  var ESP = { url: BASE + 'especiales/elecciones-eeuu-2026/?utm_source=home&utm_medium=banner&utm_campaign=elecciones2026', hasta: '2026-11-30T23:59:00-06:00',
    es: { k: 'Especial · Elecciones EE. UU. 2026', h: 'Lo que se juega supply chain, eslabón por eslabón', s: 'Estado por estado, México, cada país de LATAM y cada región del mundo: qué cambia con el resultado y qué no.', b: 'Ver el especial' },
    en: { k: 'Special · US Elections 2026', h: 'What’s at stake for supply chains, link by link', s: 'State by state, Mexico, each LATAM country and each world region: what the result changes and what it doesn’t.', b: 'See the special' },
    pt: { k: 'Especial · Eleições EUA 2026', h: 'O que está em jogo para supply chain, elo por elo', s: 'Estado por estado, México, cada país da América Latina e cada região do mundo: o que o resultado muda e o que não muda.', b: 'Ver o especial' } };
  var espBox = null, espCur = null;
  function renderEsp() {
    var l = lang(); if (!espBox || l === espCur) return; espCur = l; var E = ESP[l];
    espBox.replaceChildren();
    var w = el('div', 'mse-wrap');
    var t = el('div', 'mse-txt'); t.appendChild(el('span', 'mse-k', E.k)); t.appendChild(el('span', 'mse-h', E.h)); t.appendChild(el('span', 'mse-s', E.s)); w.appendChild(t);
    w.appendChild(el('span', 'mse-b', E.b + ' →'));
    var g = el('span', 'mse-map'); g.setAttribute('aria-hidden', 'true');
    for (var i = 0; i < 24; i++) g.appendChild(el('i', 'c' + ((i * 7) % 5)));
    w.insertBefore(g, w.firstChild);
    espBox.appendChild(w);
  }
  function initEsp() {
    if (Date.now() > Date.parse(ESP.hasta)) return;
    var hero = document.querySelector('main > header.hero') || document.querySelector('main > header');
    if (!hero || document.getElementById('msc-esp')) return;
    espBox = document.createElement('a'); espBox.id = 'msc-esp'; espBox.href = ESP.url;
    hero.parentNode.insertBefore(espBox, hero);
    renderEsp();
  }
  function lang() { if (document.documentElement.classList.contains('msc-es') && !/^\/noticias\//.test(location.pathname)) { try { if (localStorage.getItem('lang') === 'pt') return 'pt'; } catch (e) {} return 'es'; } try { var l = localStorage.getItem('lang'); if (l === 'en' || l === 'es' || l === 'pt') return l; } catch (e) {} var d = (document.documentElement.lang || navigator.language || 'es').slice(0, 2); return d === 'en' || d === 'pt' ? d : 'es'; }
  function el(t, c, x) { var n = document.createElement(t); if (c) n.className = c; if (x != null) n.textContent = x; return n; }
  function render() {
    var l = lang(); if (!data || !box || l === cur) return; cur = l;
    var L = T[l], loc = l === 'en' ? 'en-US' : l === 'pt' ? 'pt-BR' : 'es-MX';
    box.replaceChildren();
    var w = el('div', 'msn-wrap');
    var hd = el('div', 'msn-hd');
    var left = el('div'); left.appendChild(el('p', 'msn-k', L.k)); left.appendChild(el('h2', 'msn-h', L.h)); hd.appendChild(left);
    var a = el('a', 'msn-all', L.all + ' →'); a.href = BASE; hd.appendChild(a);
    w.appendChild(hd);
    var ticks = el('div', 'msn-tk');
    ['S&P 500', 'IPC BMV', 'USD/MXN', 'Petróleo WTI'].forEach(function (n) {
      var r = (data.mercados || []).filter(function (m) { return m.nombre === n; })[0]; if (!r || r.cambio == null) return;
      var s = el('span'); var nm = l === 'en' ? (r.name_en || r.nombre) : l === 'pt' ? (r.name_pt || r.name_en || r.nombre) : r.nombre;
      s.appendChild(el('b', null, nm));
      var v = r.grupo === 'divisa' ? r.valor.toLocaleString(loc, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : r.valor.toLocaleString(loc, { maximumFractionDigits: r.valor >= 1000 ? 0 : 2 });
      s.appendChild(document.createTextNode(' ' + v + ' '));
      s.appendChild(el('i', r.cambio >= 0 ? 'up' : 'down', (r.cambio > 0 ? '+' : '') + r.cambio.toLocaleString(loc, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '%'));
      ticks.appendChild(s);
    });
    var d = new Date(data.actualizado);
    ticks.appendChild(el('span', 'msn-upd', L.upd + ' ' + d.toLocaleString(loc, { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit', timeZone: 'America/Mexico_City' }) + ' CDMX'));
    w.appendChild(ticks);
    var g = el('div', 'msn-grid');
    ['global', 'latam', 'mexico'].forEach(function (k) {
      var b = data.briefs && data.briefs[k]; if (!b) return;
      var C = b[l] || b.es;
      var c = el('a', 'msn-card ' + k); c.href = BASE + 'brief/' + b.id + '/';
      c.appendChild(el('span', 'msn-m', L.mom[b.momento] + ' · ' + L.mkt[k]));
      c.appendChild(el('span', 'msn-t', C.titular));
      if (C.scm) c.appendChild(el('span', 'msn-s', C.scm.length > 150 ? C.scm.slice(0, 148).replace(/\s+\S*$/, '') + '…' : C.scm));
      c.appendChild(el('span', 'msn-r', L.read + ' →'));
      g.appendChild(c);
    });
    w.appendChild(g);
    var nl = el('div', 'msn-nl'); nl.appendChild(el('span', null, L.nl)); var nb = el('a', 'msn-nlb', L.nlb + ' →'); nb.href = NL; nb.target = '_blank'; nb.rel = 'noopener'; nl.appendChild(nb); w.appendChild(nl);
    box.appendChild(w);
  }
  function init() {
    box = document.getElementById('msc-news');
    if (!box) {
      var anchor = document.querySelector('main section.nums') || document.querySelector('main > header') || document.querySelector('main > section');
      if (!anchor) return;
      box = document.createElement('section'); box.id = 'msc-news'; box.setAttribute('aria-label', 'Noticias');
      anchor.parentNode.insertBefore(box, anchor.nextSibling);
    }
    var css = document.createElement('link'); css.rel = 'stylesheet'; css.href = BASE + 'teaser.css?v=3'; document.head.appendChild(css);
    initEsp();
    fetch(BASE + 'data/latest.json?v=' + Math.floor(Date.now() / 300000)).then(function (r) { return r.json(); }).then(function (j) { data = j; render(); }).catch(function () { box.remove(); });
    setInterval(function () { render(); renderEsp(); }, 800);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
