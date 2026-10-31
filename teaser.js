/* Mr. Supply Chain® México · bloque "Noticias de hoy" para el home (se monta después de la franja de cifras). */
(function () {
  'use strict';
  var BASE = '/noticias/';
  var T = {
    es: { k: 'Noticias', h: 'El pulso de mercados de hoy, leído para supply chain', all: 'Ver el portal de noticias', read: 'Leer', mom: { apertura: 'Apertura', mediodia: 'Mediodía', cierre: 'Cierre' }, mkt: { global: 'Global', latam: 'LATAM', mexico: 'México' }, upd: 'Actualizado' },
    en: { k: 'News', h: 'Today’s market pulse, read for supply chain', all: 'Go to the news portal', read: 'Read', mom: { apertura: 'Open', mediodia: 'Midday', cierre: 'Close' }, mkt: { global: 'Global', latam: 'LATAM', mexico: 'Mexico' }, upd: 'Updated' },
    pt: { k: 'Notícias', h: 'O pulso dos mercados de hoje, lido para supply chain', all: 'Ver o portal de notícias', read: 'Ler', mom: { apertura: 'Abertura', mediodia: 'Meio-dia', cierre: 'Fechamento' }, mkt: { global: 'Global', latam: 'LATAM', mexico: 'México' }, upd: 'Atualizado' }
  };
  var data = null, cur = null, box = null;
  function lang() { try { var l = localStorage.getItem('lang'); if (l === 'en' || l === 'es' || l === 'pt') return l; } catch (e) {} var d = (document.documentElement.lang || navigator.language || 'es').slice(0, 2); return d === 'en' || d === 'pt' ? d : 'es'; }
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
    var css = document.createElement('link'); css.rel = 'stylesheet'; css.href = BASE + 'teaser.css?v=1'; document.head.appendChild(css);
    fetch(BASE + 'data/latest.json?v=' + Math.floor(Date.now() / 300000)).then(function (r) { return r.json(); }).then(function (j) { data = j; render(); }).catch(function () { box.remove(); });
    setInterval(render, 800);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
