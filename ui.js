/* Mr. Supply Chain® México · Noticias — navegación común a todas las páginas del portal.
   1) Barra fija arriba al bajar: marca + menú de secciones (copia de .nx-sections) + selector de región si existe.
   2) Botón "Arriba". Se carga al final, con defer, en la portada, los briefs, el archivo y los especiales. */
(function () {
  'use strict';
  function el(tag, cls) { var n = document.createElement(tag); if (cls) n.className = cls; return n; }
  function lang() { var l = document.documentElement.lang || 'es'; return l.slice(0, 2); }
  function txt(es, en, pt) { var l = lang(); return l === 'en' ? en : l === 'pt' ? pt : es; }
  function trilingual(es, en, pt) {
    var f = document.createDocumentFragment();
    [['es', es], ['en', en], ['pt', pt]].forEach(function (x) { var s = el('span'); s.setAttribute('data-lang', x[0]); s.textContent = x[1]; s.style.display = lang() === x[0] ? 'inline' : 'none'; f.appendChild(s); });
    return f;
  }

  function init() {
    var mast = document.querySelector('.nx-mast');
    var bar = el('div', 'nx-bar'); bar.setAttribute('aria-hidden', 'true');
    var wrap = el('div', 'nx-wrap nx-barin'); bar.appendChild(wrap);

    var home = /\/noticias\/?$/.test(location.pathname.replace(/index\.html$/, '')) || !!document.getElementById('portada');
    var brand = el('a', 'nx-barbrand'); brand.href = home ? '#' : (document.querySelector('.nx-name[href]') ? document.querySelector('.nx-name[href]').getAttribute('href') : '/noticias/');
    brand.innerHTML = 'MSC <span>México</span><i>·</i>';
    brand.appendChild(trilingual('Noticias', 'News', 'Notícias'));
    if (home) brand.addEventListener('click', function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); });
    wrap.appendChild(brand);

    /* selector de región (sólo portada): botones espejo que activan los originales */
    var tabs = document.querySelector('.nx-lead .nx-tabs');
    if (tabs) {
      var mini = el('div', 'nx-tabs nx-barreg'); mini.setAttribute('role', 'tablist');
      Array.prototype.forEach.call(tabs.querySelectorAll('button[data-tab]'), function (b) {
        var c = b.cloneNode(true);
        c.addEventListener('click', function () {
          b.click();
          var lead = document.getElementById('portada');
          if (lead) window.scrollTo({ top: lead.getBoundingClientRect().top + window.pageYOffset - bar.offsetHeight - 8, behavior: 'smooth' });
        });
        mini.appendChild(c);
      });
      wrap.appendChild(mini);
      /* mantener sincronizado el estado seleccionado */
      new MutationObserver(function () {
        Array.prototype.forEach.call(mini.querySelectorAll('button[data-tab]'), function (c) {
          var o = tabs.querySelector('[data-tab="' + c.getAttribute('data-tab') + '"]'); if (o) c.setAttribute('aria-selected', o.getAttribute('aria-selected'));
        });
      }).observe(tabs, { attributes: true, subtree: true, attributeFilter: ['aria-selected'] });
    }

    var secs = document.querySelector('.nx-mast .nx-sections') || document.querySelector('.ex-toc');
    if (secs) {
      var nav = el('nav', 'nx-barnav'); nav.setAttribute('aria-label', txt('Secciones', 'Sections', 'Seções'));
      Array.prototype.forEach.call(secs.querySelectorAll('a'), function (a) { if (a.getAttribute('href') === '/') return; nav.appendChild(a.cloneNode(true)); });
      wrap.appendChild(nav);
      /* resaltar la sección visible */
      var links = Array.prototype.filter.call(nav.querySelectorAll('a'), function (a) { return /^#/.test(a.getAttribute('href')); });
      var targets = links.map(function (a) { return document.querySelector(a.getAttribute('href')); });
      var spy = function () {
        var y = window.pageYOffset + bar.offsetHeight + 140, cur = -1;
        targets.forEach(function (t, i) { if (t && t.getBoundingClientRect().top + window.pageYOffset <= y) cur = i; });
        links.forEach(function (a, i) { a.classList.toggle('on', i === cur); });
      };
      window.addEventListener('scroll', spy, { passive: true });
    }
    document.body.appendChild(bar);

    /* compensar la barra al saltar a un ancla */
    document.documentElement.style.scrollPaddingTop = '96px';

    var up = el('button', 'nx-top'); up.type = 'button';
    up.setAttribute('aria-label', txt('Volver arriba', 'Back to top', 'Voltar ao topo'));
    up.innerHTML = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    up.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
    document.body.appendChild(up);

    var limit = function () { return mast ? mast.getBoundingClientRect().bottom + window.pageYOffset : 200; };
    var onScroll = function () {
      var y = window.pageYOffset, show = y > limit();
      bar.classList.toggle('on', show); bar.setAttribute('aria-hidden', String(!show));
      up.classList.toggle('on', y > window.innerHeight * 1.2);
    };
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
