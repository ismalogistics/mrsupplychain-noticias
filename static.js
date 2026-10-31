/* Mr. Supply Chain® México · Noticias — idioma en páginas estáticas (brief y archivo). */
(function () {
  'use strict';
  function get() { try { var l = localStorage.getItem('lang'); if (l === 'en' || l === 'es') return l; } catch (e) {} return (navigator.language || 'es').slice(0, 2) === 'en' ? 'en' : 'es'; }
  function apply(l) {
    document.documentElement.lang = l;
    var n = document.querySelectorAll('[data-lang]');
    for (var i = 0; i < n.length; i++) n[i].style.display = n[i].getAttribute('data-lang') === l ? (n[i].tagName === 'DIV' ? 'block' : 'inline') : 'none';
    var b = document.querySelectorAll('[data-setlang]');
    for (var j = 0; j < b.length; j++) b[j].setAttribute('aria-pressed', String(b[j].getAttribute('data-setlang') === l));
  }
  function init() {
    apply(get());
    var b = document.querySelectorAll('[data-setlang]');
    for (var j = 0; j < b.length; j++) b[j].addEventListener('click', function (e) { var l = e.currentTarget.getAttribute('data-setlang'); try { localStorage.setItem('lang', l); } catch (err) {} apply(l); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
