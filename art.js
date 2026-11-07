/* Mr. Supply Chain® México · Noticias — ilustraciones propias (SVG), sin fotos de terceros.
   NXArt.hero(momento, mercado) → portada del brief; NXArt.tile(clave) → tarjetas.
   NXArt.key(texto) adivina la clave a partir de un tema o titular. */
(function () {
  var uid = 0;
  var W = 'rgba(255,255,255,', ST = ' fill="none" stroke="#fff" stroke-linecap="round" stroke-linejoin="round" ';

  var SKY = {
    premercado: ['#14244d', '#3b4f8f', '#e9925f', 'dawn'],
    apertura: ['#1d58b8', '#4f8fe0', '#bfe0ff', 'morning'],
    mediodia: ['#0f4aa0', '#2f7fd6', '#9fd2ff', 'noon'],
    cierre: ['#231a48', '#7a3d6e', '#f0915a', 'dusk']
  };
  var TINT = {
    semis: ['#3a2a8c', '#5b3fb8'], electricidad: ['#0d4f6e', '#1f8aa8'], laboral: ['#164a8a', '#1e5fa8'],
    puertos: ['#0b3a6b', '#1e6fb8'], energia: ['#5a2a12', '#b8641f'], software: ['#20306b', '#4a5fc4'],
    retail: ['#7a2246', '#b83f6a'], fletes: ['#1d4d3a', '#1f8a5b'], divisas: ['#0f4d3a', '#1f8a5b'],
    comercio: ['#6b3d0c', '#b87514'], inventario: ['#1d4d3a', '#2f8f6a'], metales: ['#3d4652', '#6b7787'], red: ['#163e86', '#2a63c4']
  };

  function grad(id, a, b, vertical) {
    return '<linearGradient id="' + id + '" x1="0" y1="0" x2="' + (vertical ? 0 : 1) + '" y2="1"><stop offset="0" stop-color="' + a + '"/><stop offset="1" stop-color="' + b + '"/></linearGradient>';
  }
  function dots(id) {
    return '<pattern id="' + id + '" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="' + W + '.14)"/></pattern>';
  }

  /* Silueta de puerto + ciudad para la portada */
  function skyline() {
    var s = '<g fill="#081631" fill-opacity=".82">';
    s += '<path d="M0 232 L0 206 L40 206 L40 190 L70 190 L70 206 L96 206 L96 170 L120 170 L120 206 L150 206 L150 186 L176 186 L176 150 L196 150 L196 206 L230 206 L230 178 L252 178 L252 206 L800 206 L800 232 Z"/>';
    /* grúas de puerto */
    s += '<path d="M520 206 L520 120 L528 120 L528 206 Z M500 124 L640 124 L640 132 L500 132 Z M600 132 L604 160 L596 160 Z"/>';
    s += '<path d="M660 206 L660 132 L667 132 L667 206 Z M642 136 L760 136 L760 143 L642 143 Z M730 143 L733 166 L727 166 Z"/>';
    /* contenedores */
    var c = ['#c0392b', '#1e5fa8', '#b87514', '#1f8a5b', '#5b3fb8'];
    s += '</g>';
    for (var r = 0; r < 3; r++) for (var i = 0; i < 6 - r; i++) {
      s += '<rect x="' + (300 + i * 30 + r * 15) + '" y="' + (192 - r * 14) + '" width="28" height="13" rx="1" fill="' + c[(i + r * 2) % 5] + '" fill-opacity=".85"/>';
    }
    /* barco */
    s += '<path d="M560 214 L780 214 L760 236 L580 236 Z" fill="#081631" fill-opacity=".9"/>';
    for (var j = 0; j < 6; j++) s += '<rect x="' + (590 + j * 28) + '" y="201" width="26" height="12" rx="1" fill="' + c[j % 5] + '" fill-opacity=".9"/>';
    s += '<rect x="0" y="232" width="800" height="48" fill="#081631" fill-opacity=".55"/>';
    s += '<path d="M0 248 Q 40 244 80 248 T 160 248 T 240 248 T 320 248 T 400 248 T 480 248 T 560 248 T 640 248 T 720 248 T 800 248" stroke="' + W + '.18)" fill="none"/>';
    return s;
  }

  function hero(momento, mercado) {
    var k = SKY[momento] || SKY.apertura, id = 'nxh' + (++uid);
    var sunY = { dawn: 200, morning: 120, noon: 62, dusk: 196 }[k[3]], sunX = { dawn: 140, morning: 210, noon: 400, dusk: 640 }[k[3]];
    var sunC = { dawn: '#ffc18a', morning: '#fff4c7', noon: '#fffbe6', dusk: '#ffb36b' }[k[3]];
    var s = '<svg viewBox="0 0 800 280" preserveAspectRatio="xMidYMid slice" role="img" aria-hidden="true" focusable="false"><defs>' +
      '<linearGradient id="' + id + 'g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="' + k[0] + '"/><stop offset=".6" stop-color="' + k[1] + '"/><stop offset="1" stop-color="' + k[2] + '"/></linearGradient>' +
      '<radialGradient id="' + id + 's"><stop offset="0" stop-color="' + sunC + '" stop-opacity=".95"/><stop offset=".35" stop-color="' + sunC + '" stop-opacity=".35"/><stop offset="1" stop-color="' + sunC + '" stop-opacity="0"/></radialGradient>' +
      dots(id + 'd') + '</defs>';
    s += '<rect width="800" height="280" fill="url(#' + id + 'g)"/><rect width="800" height="280" fill="url(#' + id + 'd)"/>';
    s += '<circle cx="' + sunX + '" cy="' + sunY + '" r="150" fill="url(#' + id + 's)"/><circle cx="' + sunX + '" cy="' + sunY + '" r="30" fill="' + sunC + '"/>';
    /* motivo por región: globo (global) o rutas (LATAM / México) */
    if (mercado === 'global') {
      s += '<g' + ST + 'stroke-opacity=".28" stroke-width="1.4"><circle cx="690" cy="70" r="58"/><ellipse cx="690" cy="70" rx="24" ry="58"/><ellipse cx="690" cy="70" rx="46" ry="58"/><path d="M632 70 H748 M640 42 H740 M640 98 H740"/></g>';
    }
    var arcs = mercado === 'mexico' ? [[80, 120, 360, 90], [200, 150, 470, 70], [60, 170, 300, 60]] : [[60, 150, 420, 60], [180, 120, 520, 90], [300, 170, 740, 100]];
    arcs.forEach(function (a) {
      var mx = (a[0] + a[2]) / 2;
      s += '<path d="M' + a[0] + ' ' + a[1] + ' Q ' + mx + ' ' + (a[1] - a[3]) + ' ' + a[2] + ' ' + (a[1] - 10) + '"' + ST + 'stroke-opacity=".55" stroke-width="2" stroke-dasharray="2 7"/>';
      s += '<circle cx="' + a[0] + '" cy="' + a[1] + '" r="4" fill="#fff" fill-opacity=".85"/><circle cx="' + a[2] + '" cy="' + (a[1] - 10) + '" r="4" fill="#fff" fill-opacity=".85"/>';
    });
    s += skyline() + '</svg>';
    return s;
  }

  /* Dibujos de línea por tema (centrados en ~ x 300, y 100 de un lienzo 400×200) */
  var ICON = {
    semis: '<rect x="250" y="50" width="100" height="100" rx="10"/><rect x="275" y="75" width="50" height="50" rx="4"/>' +
      [70, 90, 110, 130].map(function (y) { return '<path d="M250 ' + y + ' H226 M350 ' + y + ' H374"/><path d="M' + (y + 200) + ' 50 V26 M' + (y + 200) + ' 150 V174"/>'; }).join('') +
      '<path d="M120 160 H180 L200 140 M110 50 H170 L190 70 M60 110 H140"/><circle cx="56" cy="110" r="5"/><circle cx="104" cy="50" r="5"/><circle cx="114" cy="160" r="5"/>',
    electricidad: '<path d="M300 22 L262 178 M300 22 L338 178 M276 120 H324 M284 86 H316 M270 150 H330 M250 60 H350 M262 178 L324 120 M338 178 L276 120 M284 86 L316 86"/><path d="M250 60 L250 72 M350 60 L350 72"/><path d="M150 40 L120 104 H150 L130 164 L196 84 H164 L186 40 Z"/><path d="M350 60 Q 400 90 420 80 M250 60 Q 200 92 170 86" stroke-opacity=".6"/>',
    laboral: '<circle cx="230" cy="76" r="22"/><path d="M190 160 Q 190 112 230 112 Q 270 112 270 160"/><circle cx="310" cy="66" r="26"/><path d="M262 166 Q 262 108 310 108 Q 358 108 358 166"/><circle cx="388" cy="80" r="20"/><path d="M352 160 Q 354 116 388 116 Q 422 116 424 160"/><path d="M284 54 Q 310 28 336 54 Z M280 56 H340"/><path d="M60 150 L100 110 L130 130 L170 80" /><path d="M150 80 H170 V100"/>',
    puertos: '<path d="M210 176 V40 H380 M210 40 L170 62 H210 M330 40 V70 M318 70 H342 V86 H318 Z M210 80 L250 40 M210 120 L290 40"/>' +
      '<rect x="250" y="122" width="44" height="22" rx="2"/><rect x="298" y="122" width="44" height="22" rx="2"/><rect x="274" y="98" width="44" height="22" rx="2"/><rect x="250" y="146" width="44" height="22" rx="2"/><rect x="298" y="146" width="44" height="22" rx="2"/><rect x="346" y="146" width="44" height="22" rx="2"/>' +
      '<path d="M40 176 Q 70 168 100 176 T 160 176" stroke-opacity=".6"/>',
    energia: '<path d="M200 170 H330 M226 170 L262 92 L298 170 M262 92 L262 70 M190 70 L340 52 M190 70 Q 176 74 178 92 L188 120 M340 52 L346 64"/><circle cx="262" cy="70" r="7"/><path d="M188 120 V170"/><rect x="344" y="110" width="50" height="62" rx="6"/><path d="M344 128 H394 M344 154 H394"/><path d="M110 60 Q 80 104 110 120 Q 140 104 110 60 Z"/>',
    software: '<path d="M210 132 Q 180 132 180 106 Q 180 80 210 82 Q 214 46 256 46 Q 290 46 300 74 Q 340 66 350 100 Q 380 104 376 128 Q 372 140 350 140 H210" /><path d="M250 98 L232 112 L250 126 M310 98 L328 112 L310 126 M292 92 L268 132"/><rect x="200" y="152" width="170" height="26" rx="4"/><circle cx="216" cy="165" r="3"/><path d="M60 70 H130 M60 92 H110 M60 114 H140" stroke-opacity=".6"/>',
    retail: '<path d="M220 80 H330 L320 172 H230 Z"/><path d="M248 80 Q 248 44 275 44 Q 302 44 302 80"/><path d="M120 70 H146 L170 140 H230 M154 92 H240" stroke-opacity=".7"/><circle cx="178" cy="160" r="8" stroke-opacity=".7"/><circle cx="222" cy="160" r="8" stroke-opacity=".7"/><path d="M360 60 L372 84 L398 88 L379 106 L384 132 L360 120 L336 132 L341 106 L322 88 L348 84 Z"/>',
    fletes: '<path d="M150 70 H290 V156 H150 Z M290 96 H340 L370 126 V156 H290"/><circle cx="190" cy="160" r="15"/><circle cx="330" cy="160" r="15"/><path d="M302 104 H336 L356 124 H302 Z"/><path d="M40 100 H120 M60 124 H128 M80 148 H120" stroke-opacity=".6"/>',
    divisas: '<circle cx="250" cy="100" r="54"/><path d="M262 76 Q 250 68 238 72 Q 226 78 232 90 Q 238 98 252 102 Q 268 108 266 120 Q 262 132 246 130 Q 234 128 228 120 M250 60 V140"/><circle cx="350" cy="74" r="30"/><path d="M350 58 V90 M340 66 H360 M338 82 H362" stroke-opacity=".8"/><path d="M90 150 L140 120 L170 136 L220 96 M196 96 H220 V120" stroke-opacity=".7"/>',
    comercio: '<rect x="160" y="100" width="70" height="60" rx="3"/><path d="M160 120 H230 M195 100 V120"/><rect x="240" y="70" width="60" height="50" rx="3"/><path d="M240 88 H300 M270 70 V88"/><rect x="236" y="124" width="64" height="36" rx="3"/><path d="M340 40 V176" stroke-dasharray="6 8"/><path d="M60 120 H140 M120 104 L140 120 L120 136"/><path d="M356 110 H410 M390 94 L410 110 L390 126" stroke-opacity=".8"/>',
    metales: '<path d="M170 150 L196 110 H290 L316 150 Z M210 110 L234 72 H320 L346 110 M234 72 L210 110 M300 150 L330 110"/><path d="M200 150 L226 110"/><path d="M80 60 L100 80 M100 60 L80 80 M360 160 L376 176 M376 160 L360 176" stroke-opacity=".6"/>',
    inventario: '<path d="M170 176 V70 L280 30 L390 70 V176"/><path d="M196 176 V96 H364 V176 M196 124 H364 M196 150 H364"/><rect x="214" y="102" width="30" height="20" rx="2"/><rect x="252" y="102" width="30" height="20" rx="2"/><rect x="306" y="128" width="30" height="20" rx="2"/><rect x="230" y="154" width="30" height="20" rx="2"/><rect x="290" y="154" width="30" height="20" rx="2"/><path d="M50 150 V110 M80 150 V80 M110 150 V96 M36 150 H124" stroke-opacity=".7"/>',
    red: '<circle cx="200" cy="100" r="14"/><circle cx="290" cy="56" r="11"/><circle cx="300" cy="146" r="11"/><circle cx="370" cy="96" r="9"/><circle cx="110" cy="66" r="9"/><circle cx="120" cy="150" r="9"/><path d="M214 94 L280 60 M213 106 L290 140 M301 66 L364 92 M310 140 L363 102 M186 94 L118 70 M188 108 L128 144 M290 67 L299 135"/>'
  };

  function tile(key) {
    key = ICON[key] ? key : 'red';
    var t = TINT[key] || TINT.red, id = 'nxt' + (++uid);
    /* fondo que llena cualquier proporción + dibujo que se ajusta sin recortarse */
    return '<svg width="100%" height="100%" role="img" aria-hidden="true" focusable="false"><defs>' + grad(id + 'g', t[0], t[1]) + dots(id + 'd') + '</defs>' +
      '<rect width="100%" height="100%" fill="url(#' + id + 'g)"/><rect width="100%" height="100%" fill="url(#' + id + 'd)"/>' +
      '<circle cx="92%" cy="8%" r="90" fill="' + W + '.06)"/><circle cx="6%" cy="96%" r="70" fill="' + W + '.05)"/>' +
      '<svg viewBox="0 0 440 200" preserveAspectRatio="xMidYMid meet" width="100%" height="100%"><g transform="translate(22 14) scale(.9)"' + ST + 'stroke-width="3.4" stroke-opacity=".92">' + ICON[key] + '</g></svg></svg>';
  }

  var RULES = [
    ['divisas', /^(peso|tasas|d[oó]lar|tipo de cambio|currency|fx|rates?)\b|peso y tasas|peso and rates|peso e juros/i],
    ['inventario', /inventari|inventor|insumo|input|almac[eé]n|warehouse|bodega|stock de seg|safety stock/i],
    ['metales', /metal|cobre|copper|acero|steel|alumin|galvaniz|oro|gold|lithium|litio/i],
    ['semis', /chip|semicond|micron|nvidia|memori|electr[oó]n|dram|tsmc|wafer/i],
    ['electricidad', /el[eé]ctric|power|data ?cent|centros? de datos|energ[ií]a el|grid|red el/i],
    ['puertos', /puert|\bports?\b|naviera|shipping|vessel|buque|container|contenedor|maritim|marítim|ocean|ilwu|long beach/i],
    ['energia', /crudo|oil|petr[oó]le|brent|wti|gas|energ|combustib|fuel|diesel|di[eé]sel/i],
    ['fletes', /flete|freight|truck|cami[oó]n|transport|carrier|trucking|autotransp|rail|ferro|aviation|avia|drone|dron/i],
    ['divisas', /peso|d[oó]lar|dollar|fx|tipo de cambio|exchange|moneda|currency|tasa|rate|banxico|fed\b|bono|treasury|inflaci/i],
    ['laboral', /empleo|jobs|labor|trabaj|payroll|n[oó]mina|union|sindic|huelga|strike|workforce|hiring/i],
    ['software', /software|saas|cloud|nube|ai\b|\bia\b|inteligencia artificial|tech|tecnolog|atlassian|data\b/i],
    ['retail', /retail|consum|tienda|store|e-?commerce|airbnb|ventas|sales|holiday|navidad|peak/i],
    ['comercio', /comercio|trade|arancel|tariff|aduana|customs|frontera|border|t-?mec|usmca|export|import|nearshor|demand/i]
  ];
  function key(text) {
    text = String(text || '');
    for (var i = 0; i < RULES.length; i++) if (RULES[i][1].test(text)) return RULES[i][0];
    return 'red';
  }
  /* Las claves de tendencias.json ya son de industria */
  var IND = { semis: 'semis', electricidad: 'electricidad', laboral: 'laboral', puertos: 'puertos', energia: 'energia', software: 'software', retail: 'retail' };

  window.NXArt = { hero: hero, tile: tile, key: key, theme: function (title, rest) { var k = key(title); return k !== 'red' ? k : key(rest); }, ind: function (id, fallbackText) { return IND[id] || key(fallbackText || id); } };
})();
