# -*- coding: utf-8 -*-
"""Genera el especial "Elecciones intermedias de EE. UU. 2026 y supply chain".
Uso: python especiales/elecciones-eeuu-2026/build.py  → escribe index.html y og.png en esta carpeta.
Para el seguimiento con resultados basta con editar RESULTADOS (abajo) y volver a correr."""
import os, sys, json, html
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(__file__))
from contenido_mundo import L, MEXICO, LATAM, MUNDO, INDICADORES, CALENDARIO, FUENTES
from contenido_eeuu import (GRID, NOMBRES, NOMBRES_EN, NOMBRES_PT, PERFILES, PERFIL, ESTADOS, PANORAMA,
                            RESUMEN, ESCENARIOS, EXPORTACIONES, CRUCES, FUENTES_EEUU)

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://mrsupplychain.ai/noticias/'
URL = SITE + 'especiales/elecciones-eeuu-2026/'
MARCA = 'Mr. Supply Chain® México'
E = html.escape
F = {**FUENTES, **FUENTES_EEUU}
LANGS = ('es', 'en', 'pt')
PUBLICADO = '2026-11-02T12:00:00-06:00'
ACTUALIZADO = PUBLICADO  # se recalcula en __main__ con la última entrada de ACTUALIZACIONES

# ------------------------------------------------------------------ Resultados (seguimiento del 4 de noviembre)
# Mientras esté vacío, la página muestra el bloque "previo a la elección".
# Para el seguimiento: llenar con texto verificado y fuentes, y poner ACTUALIZADO.
# ------------------------------------------------------------------ Bitácora "Al momento"
# Cada actualización programada AGREGA una entrada al final de esta lista (no borra las anteriores):
# {'t': '2026-11-03T08:30:00-06:00', 'titulo': L(es, en, pt), 'x': L(es, en, pt), 'f': ['clave_fuente', ...]}
# 'x' puede tener 2–4 oraciones por idioma. Las fuentes nuevas se agregan a FUENTES_EEUU (contenido_eeuu.py).
ACTUALIZACIONES = [
    {'t': '2026-11-02T21:01:00-06:00',
     'titulo': L('Víspera electoral: mercados de predicción dan 94% a los demócratas en la Cámara y 74% en el Senado',
                 'Election eve: prediction markets give Democrats 94% for the House and 74% for the Senate',
                 'Véspera eleitoral: mercados de previsão dão 94% aos democratas na Câmara e 74% no Senado'),
     'x': L('Al mediodía del lunes, Kalshi daba a los demócratas 94% de probabilidad de ganar la Cámara y 74% el Senado; el Silver Bulletin los ubica 8.9 puntos arriba en la intención de voto genérica (51.5% contra 42.6%). Las últimas encuestas de NYT/Siena los muestran adelante en Michigan, Kansas y Texas, y en empate en Carolina del Sur; son probabilidades, no resultados. El peso cerró en 18.57 por dólar (+1.19%) y el WTI en 96.46 dólares (−7.4%) por la vía diplomática con Irán; Wall Street terminó dividido (Dow +0.45%, Nasdaq −1.11%). Sin anuncio nuevo sobre los aranceles 232 a autos, acero y aluminio: lo último fue el reporte de avances de Ebrard del 23 de octubre. Para supply chain, el escenario que el mercado favorece (A) no cambia los aranceles de inmediato, pero sí la negociación del presupuesto del 11 de diciembre y la revisión del T-MEC desde enero.',
            'At midday Monday, Kalshi gave Democrats a 94% chance of winning the House and 74% for the Senate; the Silver Bulletin puts them 8.9 points ahead on the generic ballot (51.5% vs. 42.6%). The latest NYT/Siena polls show them ahead in Michigan, Kansas and Texas and tied in South Carolina; these are probabilities, not results. The peso closed at 18.57 per dollar (+1.19%) and WTI at $96.46 (−7.4%) on the diplomatic track with Iran; Wall Street ended split (Dow +0.45%, Nasdaq −1.11%). No new announcement on the Section 232 tariffs on autos, steel and aluminum: the latest was Ebrard reporting progress on October 23. For supply chain, the scenario the market favors (A) does not change tariffs right away, but it does change the December 11 budget negotiation and the USMCA review from January.',
            'Ao meio-dia de segunda, a Kalshi dava aos democratas 94% de probabilidade de ganhar a Câmara e 74% o Senado; o Silver Bulletin os coloca 8,9 pontos à frente na intenção de voto genérica (51,5% contra 42,6%). As últimas pesquisas NYT/Siena os mostram à frente em Michigan, Kansas e Texas, e empatados na Carolina do Sul; são probabilidades, não resultados. O peso fechou a 18,57 por dólar (+1,19%) e o WTI a 96,46 dólares (−7,4%) pela via diplomática com o Irã; Wall Street fechou dividida (Dow +0,45%, Nasdaq −1,11%). Sem anúncio novo sobre as tarifas 232 a autos, aço e alumínio: o último foi o relato de avanços de Ebrard em 23 de outubro. Para supply chain, o cenário que o mercado favorece (A) não muda as tarifas de imediato, mas muda a negociação do orçamento de 11 de dezembro e a revisão do T-MEC a partir de janeiro.'),
     'f': ['kalshi_final', 'forbes_final', 'infobae_cierre_1102', 'pb_crudo_1102', 'yf_1102', 'infobae_ebrard_1023']},
    {'t': '2026-11-03T08:31:00-06:00',
     'titulo': L('Abren las casillas: más de 57 millones ya votaron por anticipado y el peso amanece en 18.54',
                 'Polls open: more than 57 million have already voted early and the peso starts the day at 18.54',
                 'Abrem as urnas: mais de 57 milhões já votaram antecipadamente e o peso amanhece a 18,54'),
     'x': L('Las casillas abrieron en todo el país; antes de la jornada, más de 57 millones de personas ya habían votado por anticipado, según el Voting Lab de la Universidad de Florida citado por CBS News, que al corte de las 5:21 CDMX no reportaba incidentes relevantes. El lunes, la Suprema Corte rechazó la petición del gobierno de obligar a California a separar ciertas boletas por correo. A las 7:30 CDMX el peso cotizaba en 18.54 por dólar (+0.12%) y antes de la apertura los futuros venían mixtos (S&P 500 +0.25%, Dow −0.23%), con el crudo volátil por los ataques en la isla iraní de Qeshm. Los primeros estados cierran casillas a las 18:00 CDMX; para supply chain, el día pide cautela: ejecutar coberturas cambiarias antes de los resultados y no cerrar tarifas ni inventarios hasta conocer el control del Congreso.',
            'Polls opened nationwide; before Election Day, more than 57 million people had already voted early, according to the University of Florida Voting Lab cited by CBS News, which as of 5:21 a.m. Mexico City time reported no major incidents. On Monday, the Supreme Court rejected the administration\'s request to force California to separate certain mail ballots. At 7:30 a.m. Mexico City time the peso traded at 18.54 per dollar (+0.12%), and before the open futures were mixed (S&P 500 +0.25%, Dow −0.23%), with crude volatile after strikes on Iran\'s Qeshm Island. The first states close polls at 6:00 p.m. Mexico City time; for supply chain, the day calls for caution: execute currency hedges before the results and do not lock in rates or inventories until control of Congress is known.',
            'As urnas abriram em todo o país; antes do dia da eleição, mais de 57 milhões de pessoas já haviam votado antecipadamente, segundo o Voting Lab da Universidade da Flórida citado pela CBS News, que até as 5h21 (Cidade do México) não relatava incidentes relevantes. Na segunda, a Suprema Corte rejeitou o pedido do governo de obrigar a Califórnia a separar certas cédulas por correio. Às 7h30 (Cidade do México) o peso era cotado a 18,54 por dólar (+0,12%) e antes da abertura os futuros vinham mistos (S&P 500 +0,25%, Dow −0,23%), com o petróleo volátil pelos ataques na ilha iraniana de Qeshm. Os primeiros estados fecham as urnas às 18h (Cidade do México); para supply chain, o dia pede cautela: executar proteções cambiais antes dos resultados e não fechar tarifas nem estoques até conhecer o controle do Congresso.'),
     'f': ['cbs_1103', 'inv_peso_1103', 'yf_1103', 'grafa_1103']},
]

RESULTADOS = None  # ejemplo: {'titulo': L(...), 'parrafos': [L(...), ...], 'f': ['clave', ...]}

def sp(d, cls=''):
    c = f' class="{cls}"' if cls else ''
    return ''.join(f'<span data-lang="{l}"{c}>{E(d[l])}</span>' for l in LANGS)

def blk(d, tag='p', cls=''):
    c = f' class="{cls}"' if cls else ''
    return ''.join(f'<div data-lang="{l}"><{tag}{c}>{E(d[l])}</{tag}></div>' for l in LANGS)

def fuentes_html(keys):
    vis = []
    for k in keys:
        if k in F and k not in vis:
            vis.append(k)
    return ' · '.join(f'<a href="{E(F[k][1])}" target="_blank" rel="noopener nofollow">{E(F[k][0])}</a>' for k in vis)

def tr_carrera(txt, l):
    if l == 'en':
        return txt.replace('posible segunda vuelta 1 dic', 'possible runoff Dec 1').replace('abierto', 'open').replace('especial', 'special')
    if l == 'pt':
        return txt.replace('posible segunda vuelta 1 dic', 'possível 2º turno em 1º dez').replace('abierto', 'aberto')
    return txt

CARGO = {'S': L('Senado', 'Senate', 'Senado'), 'G': L('Gubernatura', 'Governor', 'Governo estadual'), 'H': L('Cámara', 'House', 'Câmara')}

def datos_mapa():
    out = {}
    for s, c, r in GRID:
        d = ESTADOS.get(s, {})
        nombre = {'es': NOMBRES[s], 'en': NOMBRES_EN.get(s, NOMBRES[s]), 'pt': NOMBRES_PT.get(s, NOMBRES[s])}
        carreras = {l: [[CARGO[k][l], tr_carrera(n, l), tr_carrera(cal, l)] for k, n, cal in d.get('c', [])] for l in LANGS}
        out[s] = {'c': c, 'r': r, 'p': PERFIL[s], 'n': nombre, 'k': bool(d.get('reñida')), 'w': bool(d.get('c')),
                  'car': carreras, 'x': d.get('x') or None,
                  'f': [[F[k][0], F[k][1]] for k in d.get('f', []) if k in F]}
    return out

def mapa_html():
    tiles = []
    for s, c, r in GRID:
        d = ESTADOS.get(s, {})
        cls = 'tile p-' + PERFIL[s] + (' k' if d.get('reñida') else '') + (' w' if d.get('c') and not d.get('reñida') else '')
        tiles.append(f'<button type="button" class="{cls}" style="grid-column:{c + 1};grid-row:{r + 1}" data-st="{s}" aria-label="{E(NOMBRES[s])}">{s}</button>')
    ley = ''.join(f'<li><i style="background:{col}"></i>{sp(nom)}</li>' for k, (nom, col) in PERFILES.items())
    ley += f'<li><i class="lk"></i>{sp(L("Contienda reñida (Toss Up de Cook al Senado o gubernatura)", "Tight race (Cook Toss Up for Senate or governor)", "Disputa acirrada (Toss Up do Cook para Senado ou governo)"))}</li>'
    ley += f'<li><i class="lw"></i>{sp(L("Otra contienda a vigilar", "Another race to watch", "Outra disputa a acompanhar"))}</li>'
    return f'''<div class="ex-map">
      <div class="ex-tiles" role="group" aria-label="Mapa por estado">{''.join(tiles)}</div>
      <div class="ex-panel" id="ex-panel" aria-live="polite"></div>
    </div>
    <ul class="ex-leg">{ley}</ul>
    <p class="ex-note">{sp(L("Color: perfil principal de supply chain de cada estado (clasificación editorial). Toca un estado para ver contiendas y exposición.", "Color: each state’s main supply chain profile (editorial classification). Tap a state to see races and exposure.", "Cor: perfil principal de supply chain de cada estado (classificação editorial). Toque um estado para ver disputas e exposição."))}</p>'''

def estados_clave_html():
    filas = []
    for s, c, r in GRID:
        d = ESTADOS.get(s)
        if not d or not d.get('reñida'):
            continue
        def fmt(l):
            return '; '.join(f'{CARGO[k][l]}: ' + (f'{tr_carrera(n, l)} ({tr_carrera(cal, l)})' if n else tr_carrera(cal, l)) for k, n, cal in d['c'])
        car, car_en, car_pt = fmt('es'), fmt('en'), fmt('pt')
        nombre = L(NOMBRES[s], NOMBRES_EN.get(s, NOMBRES[s]), NOMBRES_PT.get(s, NOMBRES[s]))
        filas.append(f'<li><b>{sp(nombre)}</b> <span class="ex-car">{sp(L(car, car_en, car_pt))}</span>{blk(d["x"]) if d.get("x") else ""}</li>')
    return '<ul class="ex-keys">' + ''.join(filas) + '</ul>'

def barras_html():
    mx = max(v for _, v, _ in EXPORTACIONES)
    filas = ''.join(f'<li><span class="n">{sp(L(NOMBRES[s], NOMBRES_EN.get(s, NOMBRES[s]), NOMBRES_PT.get(s, NOMBRES[s])))}</span><span class="b"><i style="width:{v / mx * 100:.1f}%"></i></span><span class="v">US${v:,.1f}B · {pct:.0f}%</span></li>' for s, v, pct in EXPORTACIONES)
    mx2 = max(v for _, v in CRUCES)
    filas2 = ''.join(f'<li><span class="n">{E(n)}</span><span class="b"><i style="width:{v / mx2 * 100:.1f}%"></i></span><span class="v">US${v:,.1f}B</span></li>' for n, v in CRUCES)
    return f'''<div class="ex-bars2">
      <figure><figcaption>{sp(L("Exportaciones a Canadá y México, 2025 (y % del total del estado)", "Exports to Canada and Mexico, 2025 (and % of state total)", "Exportações para Canadá e México, 2025 (e % do total do estado)"))}</figcaption><ul class="ex-bars">{filas}</ul><p class="ex-src">PIIE con datos del Census Bureau</p></figure>
      <figure><figcaption>{sp(L("Cruces terrestres con más comercio, 2025", "Land crossings with the most trade, 2025", "Travessias terrestres com mais comércio, 2025"))}</figcaption><ul class="ex-bars c2">{filas2}</ul><p class="ex-src">BTS, TransBorder Freight Data</p></figure>
    </div>'''

def escenarios_html():
    out = []
    for e in ESCENARIOS:
        out.append(f'''<article class="ex-esc">
        <p class="ex-k">{sp(e["k"])}</p>
        <h3>{sp(e["t"])}</h3>
        <p class="ex-p">{sp(e["p"])}</p>
        <h4>{sp(L("Qué cambia", "What changes", "O que muda"))}</h4>{blk(e["si"])}
        <h4>{sp(L("Qué no cambia", "What doesn’t", "O que não muda"))}</h4>{blk(e["no"])}
        <div class="ex-scm"><h4>{sp(L("Lectura para supply chain", "Supply chain read", "Leitura para supply chain"))}</h4>{blk(e["scm"])}</div>
      </article>''')
    return '<div class="ex-escs">' + ''.join(out) + '</div>'

def cifras_html(items, cls='ex-kpis'):
    out = []
    for lab, val, *rest in items:
        v = sp(val) if isinstance(val, dict) else E(val)
        sub = f'<span class="s">{sp(rest[0])}</span>' if rest and isinstance(rest[0], dict) else ''
        out.append(f'<div class="ex-kpi"><span class="l">{sp(lab)}</span><b>{v}</b>{sub}</div>')
    return f'<div class="{cls}">' + ''.join(out) + '</div>'

def tarjetas_html(lista, key):
    out = []
    for x in lista:
        tasa = f'<span class="ex-rate">{E(x["tasa"])}</span>' if x.get('tasa') and x['tasa'] != '—' else ''
        out.append(f'<article class="ex-card"><h3>{sp(x[key])}{tasa}</h3>{blk(x["x"])}<p class="ex-src">{fuentes_html(x["f"])}</p></article>')
    return '<div class="ex-cards">' + ''.join(out) + '</div>'

MES = {'es': ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'],
       'en': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
       'pt': ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']}

def fecha_corta(f):
    p = f.split('-')
    y, m = p[0], int(p[1])
    if len(p) == 2:
        return L(f'{MES["es"][m - 1]} {y}', f'{MES["en"][m - 1]} {y}', f'{MES["pt"][m - 1]} {y}')
    d = int(p[2])
    return L(f'{d} {MES["es"][m - 1]}', f'{MES["en"][m - 1]} {d}', f'{d} {MES["pt"][m - 1]}')

def calendario_html():
    return '<ol class="ex-cal">' + ''.join(f'<li{" class=hoy" if f in ("2026-11-03", "2026-11-04") else ""}><time datetime="{f}">{sp(fecha_corta(f))}</time>{blk(t)}</li>' for f, t in CALENDARIO) + '</ol>'

ACCIONES = [
    L('No planees con una baja de aranceles: el resultado no cambia la 232 ni la 301. Usa las tasas actuales como escenario base para 2027.',
      'Don’t plan on tariff cuts: the result doesn’t change Section 232 or 301. Use current rates as the 2027 base case.',
      'Não planeje com redução de tarifas: o resultado não muda a 232 nem a 301. Use as tarifas atuais como cenário-base para 2027.'),
    L('Asegura el cumplimiento de origen T-MEC: hoy es lo que te exenta del arancel general de la Sección 301.',
      'Lock in USMCA origin compliance: today it is what exempts you from the general Section 301 tariff.',
      'Garanta o cumprimento de origem do USMCA: hoje é o que isenta da tarifa geral da Seção 301.'),
    L('Corre tu costo con el peso en 19 y 20 por dólar: octubre ya mostró la volatilidad.',
      'Run your costs with the peso at 19 and 20 per dollar: October already showed the volatility.',
      'Rode seus custos com o peso a 19 e 20 por dólar: outubro já mostrou a volatilidade.'),
    L('Ten colchón para el 11 de diciembre: un cierre de gobierno en 2026 ya golpeó a DHS, que incluye a la aduana (CBP).',
      'Build buffer for December 11: a 2026 shutdown already hit DHS, which includes customs (CBP).',
      'Tenha folga para 11 de dezembro: uma paralisação em 2026 já atingiu o DHS, que inclui a alfândega (CBP).'),
    L('Pregunta a tus proveedores de imanes y motores por tierras raras: la suspensión china vence el 10 de noviembre.',
      'Ask your magnet and motor suppliers about rare earths: China’s suspension expires November 10.',
      'Pergunte aos seus fornecedores de ímãs e motores sobre terras raras: a suspensão chinesa vence em 10 de novembro.'),
    L('Revisa recargos de combustible y fletes: Brent en US$118 y Asia–Costa Este en máximo del año.',
      'Review fuel surcharges and freight: Brent at US$118 and Asia–US East Coast at a year high.',
      'Revise sobretaxas de combustível e fretes: Brent a US$118 e Ásia–Costa Leste na máxima do ano.'),
]

TITULO = L('Elecciones en EE. UU.: lo que se juega supply chain, eslabón por eslabón',
           'US midterms: what’s at stake for supply chains, link by link',
           'Eleições nos EUA: o que está em jogo para supply chain, elo por elo')
DEK = L('Estado por estado en EE. UU., México, cada país de LATAM y cada región del mundo: qué cambia con el resultado del 3 de noviembre, qué no, y qué vigilar en tu operación.',
        'State by state in the US, Mexico, each LATAM country and each world region: what changes with the November 3 result, what doesn’t, and what to watch in your operation.',
        'Estado por estado nos EUA, México, cada país da América Latina e cada região do mundo: o que muda com o resultado de 3 de novembro, o que não muda e o que acompanhar na sua operação.')
DESC = 'Especial: qué se juega supply chain en las elecciones intermedias de EE. UU. del 3 de noviembre de 2026, por estado, en México, LATAM y el mundo.'

def fecha_hora(iso):
    from datetime import datetime
    d = datetime.fromisoformat(iso)
    m = d.month - 1
    h = d.strftime('%H:%M')
    return L(f'{d.day} {MES["es"][m]}, {h} h (CDMX)', f'{MES["en"][m]} {d.day}, {h} (Mexico City)', f'{d.day} {MES["pt"][m]}, {h} (Cidade do México)')

def bloque_vivo():
    if not ACTUALIZACIONES:
        return ''
    items = []
    for a in sorted(ACTUALIZACIONES, key=lambda a: a['t'], reverse=True):
        items.append(f'<li><time datetime="{a["t"]}">{sp(fecha_hora(a["t"]))}</time><h3>{sp(a["titulo"])}</h3>{blk(a["x"])}<p class="ex-src">{fuentes_html(a.get("f", []))}</p></li>')
    return (f'<section class="ex-vivo" id="al-momento"><p class="ex-vk"><span class="dot"></span>{sp(L("Al momento", "Live updates", "Ao vivo"))}</p>'
            f'<ol>{"".join(items)}</ol></section>')

def bloque_resultados():
    if not RESULTADOS:
        return f'<aside class="ex-pend"><b>{sp(L("Previo a la elección.", "Before the vote.", "Antes da eleição."))}</b> {sp(L("Este especial se actualiza el lunes 2 en la noche; el martes 3 en la mañana, a mediodía, en la tarde y en la noche; y el miércoles 4 en la mañana con los resultados finales y las conclusiones para supply chain.", "This special is updated on Monday the 2nd at night; on Tuesday the 3rd in the morning, at midday, in the afternoon and at night; and on Wednesday the 4th in the morning with final results and conclusions for supply chains.", "Este especial é atualizado na segunda, dia 2, à noite; na terça, dia 3, de manhã, ao meio-dia, à tarde e à noite; e na quarta, dia 4, pela manhã, com os resultados finais e as conclusões para supply chain."))}</aside>'
    pars = ''.join(blk(p) for p in RESULTADOS['parrafos'])
    return f'<section class="ex-res" id="resultados"><h2 class="nx-h2">{sp(RESULTADOS["titulo"])}</h2><div class="nx-body ex-prose">{pars}</div><p class="ex-src">{fuentes_html(RESULTADOS.get("f", []))}</p></section>'

def todas_fuentes():
    usadas = []
    def add(keys):
        for k in keys:
            if k in F and k not in usadas:
                usadas.append(k)
    add(['alj_map', 'forbes', 'sabato', 'rollcall', 'silver', 'wion', 'spectrum', 'epoch', 'newsweek', 'star', 'wita', 'wh', 'pwbm', 'crs232', 'cargo', 'ustr301', 'wc301', 'wh_cr'])
    add(MEXICO['fuentes'])
    for x in LATAM + MUNDO:
        add(x['f'])
    for d in ESTADOS.values():
        add(d.get('f', []))
    add(['piie', 'bts', 'drewry', 'ajot', 'fortune', 'nrf', 'wto', 'opencount', 'ff', 'thine', 'jbh'])
    if RESULTADOS:
        add(RESULTADOS.get('f', []))
    return '<ol class="ex-fuentes">' + ''.join(f'<li><a href="{E(F[k][1])}" target="_blank" rel="noopener nofollow">{E(F[k][0])}</a></li>' for k in usadas) + '</ol>'

def hbar(rows, unit='', cls='', maxv=None, fmt='{:,.1f}'):
    """rows: [(label_dict_or_str, value, color, extra_label_or_None)]"""
    mx = maxv or max(r[1] for r in rows)
    out = []
    for lab, v, col, extra in rows:
        lb = sp(lab) if isinstance(lab, dict) else E(lab)
        ex = f' <span class="x">{sp(extra) if isinstance(extra, dict) else E(extra)}</span>' if extra else ''
        out.append(f'<li><span class="n">{lb}</span><span class="b"><i style="width:{max(v / mx * 100, 1.5):.1f}%;background:{col}"></i></span><span class="v">{E(fmt.format(v))}{unit}{ex}</span></li>')
    return f'<ul class="ex-hb {cls}">' + ''.join(out) + '</ul>'

def congreso_html():
    def barra(nombre, segs, total, linea, nota):
        x = 0; partes = []
        for n, col, lab in segs:
            partes.append(f'<i style="left:{x / total * 100:.2f}%;width:{n / total * 100:.2f}%;background:{col}" title="{n}"></i>')
            x += n
        leg = ''.join(f'<span><b style="background:{col}"></b>{sp(lab)} <strong>{n}</strong></span>' for n, col, lab in segs)
        return (f'<div class="ex-seat"><div class="h"><b>{sp(nombre)}</b><span>{sp(nota)}</span></div>'
                f'<div class="bar">{"".join(partes)}<em style="left:{linea / total * 100:.2f}%"></em></div><div class="leg">{leg}</div></div>')
    R, D, O = '#c0392b', '#1e4f9c', '#c9ccd1'
    camara = barra(L('Cámara de Representantes', 'House of Representatives', 'Câmara dos Representantes'),
                   [(218, R, L('Republicanos', 'Republicans', 'Republicanos')), (214, D, L('Demócratas', 'Democrats', 'Democratas')), (3, O, L('Indep. y vacantes', 'Indep. and vacant', 'Indep. e vagas'))],
                   435, 218, L('mayoría: 218 · en juego: 435', 'majority: 218 · up: 435', 'maioria: 218 · em disputa: 435'))
    senado = barra(L('Senado', 'Senate', 'Senado'),
                   [(53, R, L('Republicanos', 'Republicans', 'Republicanos')), (47, D, L('Demócratas e indep.', 'Democrats and indep.', 'Democratas e indep.'))],
                   100, 50, L('control: 51 (o 50 + vicepresidente) · en juego: 35', 'control: 51 (or 50 + VP) · up: 35', 'controle: 51 (ou 50 + vice) · em disputa: 35'))
    def gauge(lab, lo, hi):
        return (f'<div class="ex-g"><div class="ring" style="--p:{(lo + hi) / 2:.1f}"><span>{lo}–{hi}%</span></div>'
                f'<p>{sp(lab)}</p></div>')
    g = gauge(L('Probabilidad de mayoría demócrata en la Cámara (Kalshi / Polymarket)', 'Odds of a Democratic House majority (Kalshi / Polymarket)', 'Probabilidade de maioria democrata na Câmara (Kalshi / Polymarket)'), 93, 95) + \
        gauge(L('Probabilidad de mayoría demócrata en el Senado (Kalshi / Polymarket)', 'Odds of a Democratic Senate majority (Kalshi / Polymarket)', 'Probabilidade de maioria democrata no Senado (Kalshi / Polymarket)'), 71, 72)
    return (f'<div class="ex-panelc"><p class="ex-ct">{sp(L("El Congreso hoy y lo que dicen los mercados", "Congress today and what markets say", "O Congresso hoje e o que dizem os mercados"))}</p>'
            f'{camara}{senado}<div class="ex-gs">{g}</div>'
            f'<p class="ex-src">Al Jazeera (26 oct) · WION (2 nov 2026)</p></div>')

def comercio_mx_html():
    rows = [(L('México', 'Mexico', 'México'), 682.8, '#1e4f9c', '+17.5%'), (L('Canadá', 'Canada', 'Canadá'), 503.8, '#5b3fb8', None), (L('China', 'China', 'China'), 257.4, '#a3a8b0', '−12%')]
    return (f'<figure class="ex-fig"><figcaption>{sp(L("Comercio con EE. UU., enero–agosto 2026 (US$ mil millones)", "Trade with the US, January–August 2026 (US$ bn)", "Comércio com os EUA, janeiro–agosto 2026 (US$ bi)"))}</figcaption>'
            f'{hbar(rows)}<p class="ex-src">Census vía FreightWaves (7 oct 2026)</p></figure>')

def aranceles_latam_html():
    A, B = '#a83246', '#d98a97'
    rows = [(L('Brasil*', 'Brazil*', 'Brasil*'), 12.5, A, L('+25% en parte', '+25% on some', '+25% em parte')), ('Colombia', 12.5, A, None), ('Chile', 12.5, A, None), (L('Perú', 'Peru', 'Peru'), 12.5, A, None),
            ('Venezuela', 12.5, A, None), (L('Rep. Dominicana', 'Dominican Rep.', 'Rep. Dominicana'), 12.5, A, None), ('Uruguay', 12.5, A, None), ('Costa Rica · Nicaragua', 12.5, A, None),
            ('Argentina', 10, B, None), (L('Ecuador', 'Ecuador', 'Equador'), 10, B, None), ('Guatemala · El Salvador · Honduras', 10, B, None),
            (L('México (no T-MEC)', 'Mexico (non-USMCA)', 'México (não USMCA)'), 10, B, L('T-MEC: 0%', 'USMCA: 0%', 'USMCA: 0%'))]
    return (f'<figure class="ex-fig wide"><figcaption>{sp(L("Arancel general de EE. UU. (Sección 301), desde el 24 de julio de 2026", "General US tariff (Section 301), since July 24, 2026", "Tarifa geral dos EUA (Seção 301), desde 24 de julho de 2026"))}</figcaption>'
            f'{hbar(rows, unit="%", maxv=15, fmt="{:g}", cls="cols2")}'
            f'<p class="ex-src">{sp(L("* Brasil paga además 25% (Sección 301 específica) en ~18% de sus ventas. Productos ya sujetos a la Sección 232 quedan fuera. Fuentes: CargoTrans, EY, Reuters.", "* Brazil also pays 25% (country-specific Section 301) on ~18% of its sales. Goods already under Section 232 are excluded. Sources: CargoTrans, EY, Reuters.", "* O Brasil paga também 25% (Seção 301 específica) sobre ~18% de suas vendas. Produtos já sujeitos à Seção 232 ficam de fora. Fontes: CargoTrans, EY, Reuters."))}</p></figure>')

def fletes_html():
    C1, C2 = '#0e7490', '#1e4f9c'
    rows = [(L('Asia → Costa Este EE. UU. (FBX)', 'Asia → US East Coast (FBX)', 'Ásia → Costa Leste EUA (FBX)'), 10565, C1, L('+9% · máx. del año', '+9% · year high', '+9% · máx. do ano')),
            (L('Shanghái → Nueva York (WCI)', 'Shanghai → New York (WCI)', 'Xangai → Nova York (WCI)'), 9631, C2, '−5%'),
            (L('Asia → Costa Oeste EE. UU. (FBX)', 'Asia → US West Coast (FBX)', 'Ásia → Costa Oeste EUA (FBX)'), 8368, C1, '+3%'),
            (L('Shanghái → Los Ángeles (WCI)', 'Shanghai → Los Angeles (WCI)', 'Xangai → Los Angeles (WCI)'), 7514, C2, '−6%'),
            (L('Shanghái → Génova (WCI)', 'Shanghai → Genoa (WCI)', 'Xangai → Gênova (WCI)'), 4151, C2, '0%'),
            (L('Shanghái → Rotterdam (WCI)', 'Shanghai → Rotterdam (WCI)', 'Xangai → Roterdã (WCI)'), 3686, C2, '+1%')]
    return (f'<figure class="ex-fig"><figcaption>{sp(L("Flete por contenedor de 40 pies (US$), última semana de octubre", "Freight per 40-ft container (US$), last week of October", "Frete por contêiner de 40 pés (US$), última semana de outubro"))}</figcaption>'
            f'{hbar(rows, fmt="{:,.0f}")}<p class="ex-src">Drewry WCI (30 oct) · Freightos FBX vía AJOT (28 oct 2026)</p></figure>')

CSS = '''
.ex-page .nx-article{max-width:1120px}
.ex-hero{padding:8px 0 4px}
.ex-hero.has-img{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);column-gap:36px;align-items:start}
.ex-hero.has-img>*{grid-column:1}
.ex-himg{grid-column:2!important;grid-row:1/span 6;margin:0;align-self:center}
.ex-himg img{display:block;width:100%;height:auto;border-radius:14px;box-shadow:0 12px 40px rgba(11,31,71,.25)}
@media (max-width:900px){.ex-hero.has-img{display:block}.ex-himg{margin:0 0 18px}}
.ex-hero .nx-hl{max-width:24ch}
.ex-tagline{display:inline-block;background:#a83246;color:#fff;font-size:11.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;padding:4px 9px;border-radius:3px;margin:0 0 12px}
.ex-sec{margin:44px 0 0}
.ex-sec>.nx-h2{margin-bottom:18px}
.ex-intro{font-family:var(--serif);font-size:1.12rem;line-height:1.6;max-width:68ch;margin:0 0 18px;color:#23262c}
.ex-60{margin:0;padding:0;list-style:none;counter-reset:n;max-width:72ch}
.ex-60 li{counter-increment:n;display:grid;grid-template-columns:34px 1fr;gap:10px;padding:12px 0;border-bottom:1px solid var(--line)}
.ex-60 li::before{content:counter(n);font-family:var(--serif);font-size:1.6rem;line-height:1;color:var(--accent);font-weight:600}
.ex-60 p{margin:0;font-family:var(--serif);font-size:1.1rem;line-height:1.55}
.ex-kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:18px 0 0}
.ex-kpi{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:14px 16px;display:flex;flex-direction:column;gap:4px;min-width:0}
.ex-kpi .l{font-size:12px;color:var(--muted);font-weight:600;line-height:1.3}
.ex-kpi b{font-family:var(--serif);font-size:1.45rem;line-height:1.15;font-weight:600;font-variant-numeric:tabular-nums}
.ex-kpi .s{font-size:12px;color:var(--muted)}
.ex-escs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.ex-esc{background:var(--panel);border:1px solid var(--line);border-top:4px solid var(--accent);border-radius:8px;padding:18px 18px 16px;min-width:0}
.ex-esc:nth-child(2){border-top-color:#5b3fb8}.ex-esc:nth-child(3){border-top-color:#a83246}
.ex-k{margin:0;font-size:11.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.ex-esc h3{font-family:var(--serif);font-size:1.3rem;line-height:1.2;margin:4px 0 6px}
.ex-p{margin:0 0 10px;font-size:13px;color:var(--muted)}
.ex-esc h4,.ex-card h4{margin:12px 0 4px;font-size:11.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase}
.ex-esc p,.ex-card p{margin:0;font-size:15px;line-height:1.55}
.ex-scm{margin-top:14px;background:var(--soft);border-radius:6px;padding:10px 12px}
.ex-scm h4{margin-top:0;color:var(--accent)}
.ex-map{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:22px;align-items:start}
.ex-tiles{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));grid-template-rows:repeat(8,auto);gap:4px}
.tile{aspect-ratio:1;border:0;border-radius:5px;color:#fff;font:700 clamp(9px,1.25vw,13px)/1 var(--sans);cursor:pointer;padding:0;position:relative;opacity:.9;min-width:0}
.tile:hover,.tile[aria-pressed="true"]{opacity:1;outline:3px solid var(--ink);outline-offset:1px;z-index:1}
.tile.k::after{content:"";position:absolute;inset:3px;border:2px solid #fff;border-radius:3px}
.tile.w::before{content:"";position:absolute;top:4px;right:4px;width:6px;height:6px;border-radius:50%;background:#fff}
.p-frontera{background:#1e4f9c}.p-manufactura{background:#5b3fb8}.p-agro{background:#1f8a5b}.p-puertos{background:#0e7490}.p-energia{background:#b87514}.p-otros{background:#a3a8b0}
.ex-panel{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px;min-height:240px}
.ex-panel h3{font-family:var(--serif);font-size:1.5rem;margin:0 0 4px}
.ex-panel .pf{display:inline-block;font-size:11.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#fff;padding:3px 8px;border-radius:3px;margin:0 0 12px}
.ex-panel ul{list-style:none;margin:0 0 12px;padding:0}
.ex-panel li{padding:8px 0;border-bottom:1px solid var(--line);font-size:14px;line-height:1.45}
.ex-panel li b{display:block;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.ex-panel p{margin:0 0 10px;font-family:var(--serif);font-size:1.05rem;line-height:1.55}
.ex-panel .ex-src{font-family:var(--sans);font-size:12.5px;line-height:1.5}
.ex-panel .none{color:var(--muted);font-size:14px}
.ex-leg{list-style:none;padding:0;margin:14px 0 0;display:flex;flex-wrap:wrap;gap:8px 16px;font-size:12.5px}
.ex-leg li{display:flex;align-items:center;gap:6px}
.ex-leg i{width:14px;height:14px;border-radius:3px;display:inline-block}
.ex-leg i.lk{background:#5f6670;box-shadow:inset 0 0 0 2px #5f6670,inset 0 0 0 4px #fff}
.ex-leg i.lw{background:#5f6670;position:relative}.ex-leg i.lw::after{content:"";position:absolute;top:2px;right:2px;width:4px;height:4px;border-radius:50%;background:#fff}
.ex-note,.ex-src{font-size:12.5px;color:var(--muted);margin:8px 0 0}
.ex-src a{color:var(--accent);text-decoration:none}.ex-src a:hover{text-decoration:underline}
.ex-keys{list-style:none;padding:0;margin:22px 0 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
.ex-keys li{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:14px 16px;min-width:0}
.ex-keys li>b{font-family:var(--serif);font-size:1.15rem}
.ex-car{display:block;font-size:13px;color:var(--muted);margin:4px 0 8px}
.ex-keys p{margin:0;font-size:14.5px;line-height:1.5}
.ex-bars2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin:26px 0 0}
.ex-bars2 figure{margin:0;min-width:0}
.ex-bars2 figcaption{font-size:13px;font-weight:700;margin:0 0 10px}
.ex-bars{list-style:none;padding:0;margin:0}
.ex-bars li{display:grid;grid-template-columns:minmax(0,9em) minmax(0,1fr) auto;gap:10px;align-items:center;font-size:13px;padding:4px 0}
.ex-bars .n{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ex-bars .b{height:12px;background:var(--soft);border-radius:3px;overflow:hidden}
.ex-bars .b i{display:block;height:100%;background:var(--accent);border-radius:3px}
.ex-bars.c2 .b i{background:#0e7490}
.ex-bars .v{font-variant-numeric:tabular-nums;color:var(--muted);white-space:nowrap}
.ex-prose{max-width:68ch}
.ex-prose p{font-family:var(--serif);font-size:1.12rem;line-height:1.62;margin:0 0 16px;color:#23262c}
.ex-vig{background:var(--soft);border-left:4px solid var(--accent);padding:14px 18px;border-radius:0 6px 6px 0;max-width:68ch}
.ex-vig p{margin:0;font-size:15.5px;line-height:1.55}
.ex-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.ex-card{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px 18px;display:flex;flex-direction:column;gap:6px;min-width:0}
.ex-card h3{margin:0;font-family:var(--serif);font-size:1.2rem;display:flex;justify-content:space-between;align-items:baseline;gap:10px}
.ex-rate{font-family:var(--sans);font-size:12px;font-weight:800;color:#a83246;background:#fbecef;padding:3px 8px;border-radius:999px;white-space:nowrap}
.ex-card .ex-src{margin-top:auto;padding-top:6px}
.ex-cal{list-style:none;padding:0;margin:0;border-left:2px solid var(--line);max-width:68ch}
.ex-cal li{position:relative;padding:0 0 14px 20px}
.ex-cal li::before{content:"";position:absolute;left:-6px;top:5px;width:10px;height:10px;border-radius:50%;background:var(--accent)}
.ex-cal time{font-weight:800;font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--accent)}
.ex-cal p{margin:2px 0 0;font-size:15px;line-height:1.5}
.ex-acc{margin:0;padding-left:20px;max-width:70ch}
.ex-acc li{margin:0 0 10px;font-size:15.5px;line-height:1.55}
.ex-acc li p{margin:0}
.ex-pend{margin:18px 0 0;background:#fbf4ea;border-left:4px solid var(--com);padding:12px 16px;border-radius:0 6px 6px 0;font-size:14.5px;max-width:72ch}
.ex-res{margin:30px 0 0;border:2px solid var(--accent);border-radius:10px;padding:20px 22px;background:var(--panel)}
.ex-fuentes{font-size:12.5px;color:var(--muted);columns:2;column-gap:28px;padding-left:20px;margin:0}
.ex-fuentes li{break-inside:avoid;margin:0 0 4px}
.ex-fuentes a{color:var(--accent);text-decoration:none}
.ex-toc{display:flex;gap:18px;overflow-x:auto;scrollbar-width:none;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:10px 0;margin:6px 0 0;position:sticky;top:0;background:var(--paper);z-index:5}
.ex-toc::-webkit-scrollbar{display:none}
.ex-toc a{font-size:13px;font-weight:700;text-decoration:none;white-space:nowrap;color:var(--ink)}
.ex-toc a:hover{color:var(--accent)}
.ex-method{font-size:13px;color:var(--muted);max-width:72ch;line-height:1.55}

.ex-intro{max-width:none}
.ex-two{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:28px;align-items:start}
.ex-two.mx{grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);margin-top:22px}
.ex-two.fl{grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);margin-top:22px}
.ex-60{max-width:none}
.ex-panelc{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px 20px}
.ex-ct{margin:0 0 12px;font-size:12px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
.ex-seat{margin:0 0 16px}
.ex-seat .h{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:13px;margin:0 0 6px}
.ex-seat .h span{color:var(--muted);font-size:12px}
.ex-seat .bar{position:relative;height:26px;border-radius:6px;overflow:hidden;background:#eee}
.ex-seat .bar i{position:absolute;top:0;bottom:0}
.ex-seat .bar em{position:absolute;top:-3px;bottom:-3px;width:2px;background:#15171b;box-shadow:0 0 0 2px #fff}
.ex-seat .leg{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:12.5px;margin-top:6px;color:#3d4148}
.ex-seat .leg b{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px}
.ex-gs{display:grid;grid-template-columns:1fr 1fr;gap:12px;border-top:1px solid var(--line);padding-top:14px}
.ex-g{display:flex;gap:12px;align-items:center}
.ex-g .ring{--p:50;flex:none;width:76px;height:76px;border-radius:50%;background:conic-gradient(#1e4f9c calc(var(--p)*1%),#e9e7e1 0);display:grid;place-items:center}
.ex-g .ring span{width:58px;height:58px;border-radius:50%;background:var(--panel);display:grid;place-items:center;font:700 13px/1 var(--sans);font-variant-numeric:tabular-nums}
.ex-g p{margin:0;font-size:12.5px;line-height:1.4;color:#3d4148}
.ex-kpis.six{grid-template-columns:repeat(6,minmax(0,1fr))}.ex-kpis.six .ex-kpi b{font-size:1.2rem}
.ex-kpis.stack{grid-template-columns:minmax(0,1fr);margin:0}
.ex-kpis.stack .ex-kpi b{font-size:1.8rem}
.ex-side{display:flex;flex-direction:column;gap:18px}
.ex-side .ex-vig{max-width:none}
.ex-fig{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px 18px;min-width:0}
.ex-fig.wide{margin:0 0 20px}
.ex-fig figcaption{font-size:13px;font-weight:800;margin:0 0 12px;line-height:1.35}
.ex-hb{list-style:none;padding:0;margin:0}
.ex-hb li{display:grid;grid-template-columns:minmax(0,13em) minmax(0,1fr) 11em;gap:10px;align-items:center;font-size:13.5px;padding:5px 0}
.ex-hb .n{line-height:1.25}
.ex-hb .b{height:16px;background:var(--soft);border-radius:4px;overflow:hidden}
.ex-hb .b i{display:block;height:100%;border-radius:4px}
.ex-hb .v{font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap}
.ex-hb .v .x{font-weight:500;color:var(--muted);font-size:12px;margin-left:4px}
.ex-hb.cols2{columns:2;column-gap:32px}
.ex-hb.cols2 li{break-inside:avoid;grid-template-columns:minmax(0,10em) minmax(0,1fr) 9.5em}
.ex-cal{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;border:0;max-width:none}
.ex-cal li{padding:14px 16px;background:var(--panel);border:1px solid var(--line);border-top:4px solid var(--accent);border-radius:10px}
.ex-cal li::before{display:none}
.ex-cal li.hoy{border-top-color:#a83246;background:#fbf4f5}
.ex-cal li.hoy time{color:#a83246}
.ex-cal time{font-family:var(--serif);font-size:1.3rem;letter-spacing:0;text-transform:none;display:block;margin-bottom:4px}
.ex-acc{list-style:none;padding:0;max-width:none;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;counter-reset:a}
.ex-acc li{counter-increment:a;margin:0;background:var(--soft);border-radius:10px;padding:16px 18px 16px 58px;position:relative;font-size:15px}
.ex-acc li::before{content:counter(a);position:absolute;left:16px;top:12px;font-family:var(--serif);font-size:2rem;font-weight:600;color:var(--accent);line-height:1}
.ex-keys{grid-template-columns:repeat(3,minmax(0,1fr))}
.ex-esc{display:flex;flex-direction:column}.ex-esc .ex-scm{margin-top:auto}
@media (max-width:1100px){.ex-kpis.six{grid-template-columns:repeat(3,minmax(0,1fr))}.ex-keys{grid-template-columns:repeat(2,minmax(0,1fr))}.ex-acc{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:900px){.ex-two,.ex-two.mx,.ex-two.fl{grid-template-columns:minmax(0,1fr)}.ex-cal{grid-template-columns:repeat(2,minmax(0,1fr))}.ex-hb.cols2{columns:1}.ex-kpis.stack{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (min-width:600px) and (max-width:900px){.ex-escs{grid-template-columns:repeat(2,minmax(0,1fr))}.ex-escs .ex-esc:last-child{grid-column:1/-1}.ex-tiles{max-width:620px}}
@media (max-width:600px){.ex-kpis.six,.ex-kpis.stack{grid-template-columns:repeat(2,minmax(0,1fr))}.ex-keys,.ex-acc{grid-template-columns:minmax(0,1fr)}.ex-cal{grid-template-columns:minmax(0,1fr)}.ex-gs{grid-template-columns:minmax(0,1fr)}.ex-hb li,.ex-hb.cols2 li{grid-template-columns:minmax(0,1fr) auto;row-gap:3px}.ex-hb .b{grid-column:1/-1;grid-row:2}.ex-kpi b{font-size:1.2rem}.ex-panelc,.ex-fig{padding:14px}.ex-esc{padding:16px}}
@media (max-width:760px){.ex-map{grid-template-columns:minmax(0,1fr)}}
@media (max-width:900px){.ex-escs{grid-template-columns:repeat(2,minmax(0,1fr))}.ex-escs .ex-esc:last-child{grid-column:1/-1}.ex-bars2{grid-template-columns:minmax(0,1fr)}.ex-fuentes{columns:1}}
@media (max-width:520px){.ex-tiles{gap:2px}.tile{border-radius:3px}.tile.k::after{inset:2px;border-width:1.5px}.tile.w::before{width:4px;height:4px;top:2px;right:2px}.ex-bars li{grid-template-columns:minmax(0,7em) minmax(0,1fr) auto;font-size:12px}}
@media (max-width:599px){.ex-60 p{font-size:1rem}.ex-60 li{grid-template-columns:26px 1fr;padding:10px 0}.ex-prose p{font-size:1.02rem}.ex-escs{grid-template-columns:minmax(0,1fr)}.ex-escs .ex-esc:last-child{grid-column:auto}}

.ex-vivo{margin:22px 0 0;border:2px solid #a83246;border-radius:12px;background:var(--panel);padding:16px 20px;max-width:none}
.ex-vk{margin:0 0 6px;font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#a83246;display:flex;align-items:center;gap:8px}
.ex-vk .dot{width:9px;height:9px;border-radius:50%;background:#a83246;animation:exp 1.6s infinite}
@keyframes exp{0%{box-shadow:0 0 0 0 rgba(168,50,70,.6)}70%{box-shadow:0 0 0 9px rgba(168,50,70,0)}100%{box-shadow:0 0 0 0 rgba(168,50,70,0)}}
.ex-vivo ol{list-style:none;margin:0;padding:0;max-height:560px;overflow:auto}
.ex-vivo li{padding:12px 0;border-top:1px solid var(--line)}
.ex-vivo li:first-child{border-top:0}
.ex-vivo time{font-size:12px;font-weight:700;color:var(--muted)}
.ex-vivo h3{margin:2px 0 4px;font-family:var(--serif);font-size:1.2rem;line-height:1.25}
.ex-vivo p{margin:0;font-size:15px;line-height:1.55}
.ex-hero.has-img .ex-vivo,.ex-hero.has-img .ex-res{grid-column:1/-1}
'''

JS = r'''
(function(){
  var D=JSON.parse(document.getElementById('ex-data').textContent);
  var P=JSON.parse(document.getElementById('ex-perf').textContent);
  var T={es:{pf:'Perfil',none:'Sin contienda clave para supply chain en este especial.',src:'Fuentes'},en:{pf:'Profile',none:'No key supply-chain race in this special.',src:'Sources'},pt:{pf:'Perfil',none:'Sem disputa-chave para supply chain neste especial.',src:'Fontes'}};
  var panel=document.getElementById('ex-panel'),cur='TX';
  function lang(){var l=document.documentElement.lang;return (l==='en'||l==='pt')?l:'es';}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function show(st){
    cur=st;var d=D[st],l=lang(),h='';
    h+='<h3>'+esc(d.n[l])+'</h3>';
    h+='<span class="pf" style="background:'+P[d.p][1]+'">'+esc(P[d.p][0][l])+'</span>';
    if(d.car[l].length){h+='<ul>';d.car[l].forEach(function(c){h+='<li><b>'+esc(c[0])+'</b>'+(c[1]?esc(c[1])+' · ':'')+esc(c[2])+'</li>';});h+='</ul>';}
    if(d.x){h+='<p>'+esc(d.x[l])+'</p>';}
    if(!d.car[l].length&&!d.x){h+='<p class="none">'+T[l].none+'</p>';}
    if(d.f.length){h+='<p class="ex-src">'+T[l].src+': '+d.f.map(function(f){return '<a href="'+esc(f[1])+'" target="_blank" rel="noopener nofollow">'+esc(f[0])+'</a>';}).join(' · ')+'</p>';}
    panel.innerHTML=h;
    var b=document.querySelectorAll('.tile');for(var i=0;i<b.length;i++)b[i].setAttribute('aria-pressed',String(b[i].getAttribute('data-st')===st));
  }
  document.querySelector('.ex-tiles').addEventListener('click',function(e){var t=e.target.closest('.tile');if(!t)return;show(t.getAttribute('data-st'));if(window.innerWidth<900){var r=panel.getBoundingClientRect();if(r.top>window.innerHeight*0.6||r.bottom<0)panel.scrollIntoView({behavior:'smooth',block:'start'});}});
  var lb=document.querySelectorAll('[data-setlang]');for(var j=0;j<lb.length;j++)lb[j].addEventListener('click',function(){setTimeout(function(){show(cur);},0);});
  if(document.readyState==='complete')show(cur);else window.addEventListener('load',function(){show(cur);});
  show(cur);
})();
'''

def pagina():
    share = f'{URL}?utm_source=%s&utm_medium=social&utm_campaign=elecciones2026'
    t_es = TITULO['es']
    ld = {'@context': 'https://schema.org', '@type': 'NewsArticle', 'headline': t_es[:110], 'alternativeHeadline': TITULO['en'][:110],
          'description': DESC, 'inLanguage': ['es-MX', 'en-US', 'pt-BR'], 'datePublished': PUBLICADO, 'dateModified': ACTUALIZADO,
          'url': URL, 'mainEntityOfPage': URL, 'image': [URL + 'og.png'], 'articleSection': 'Especial',
          'author': {'@type': 'Organization', 'name': f'Mesa de mercados {MARCA}', 'url': SITE},
          'publisher': {'@type': 'Organization', 'name': MARCA, 'url': 'https://mrsupplychain.ai/'}}
    perf = {k: [v[0], v[1]] for k, v in PERFILES.items()}
    toc = [('resumen', L('En 60 segundos', 'In 60 seconds', 'Em 60 segundos')), ('escenarios', L('Escenarios', 'Scenarios', 'Cenários')),
           ('estados', L('Por estado', 'By state', 'Por estado')), ('mexico', L('México', 'Mexico', 'México')),
           ('latam', L('LATAM', 'LATAM', 'América Latina')), ('mundo', L('Mundo', 'World', 'Mundo')),
           ('calendario', L('Calendario', 'Calendar', 'Calendário')), ('acciones', L('Qué hacer', 'What to do', 'O que fazer')),
           ('fuentes', L('Fuentes', 'Sources', 'Fontes'))]
    if ACTUALIZACIONES:
        toc = [('al-momento', L('Al momento', 'Live', 'Ao vivo'))] + toc
    toc_html = ''.join(f'<a href="#{i}">{sp(t)}</a>' for i, t in toc)
    acciones = ''.join(f'<li>{blk(a)}</li>' for a in ACCIONES)
    mx_pars = ''.join(blk(p) for p in MEXICO['parrafos'])
    return f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{E(t_es)} | Noticias {E(MARCA)}</title>
  <meta name="description" content="{E(DESC)}">
  <link rel="canonical" href="{URL}">
  <link rel="alternate" type="application/rss+xml" title="Noticias {E(MARCA)}" href="{SITE}feed.xml">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="{E(MARCA)}">
  <meta property="og:title" content="{E(t_es)}">
  <meta property="og:description" content="{E(DESC)}">
  <meta property="og:url" content="{URL}">
  <meta property="og:image" content="{URL}og.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="es_MX">
  <meta property="og:locale:alternate" content="en_US">
  <meta property="og:locale:alternate" content="pt_BR">
  <meta property="article:published_time" content="{PUBLICADO}">
  <meta property="article:modified_time" content="{ACTUALIZADO}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@MrSupplyChainX">
  <meta name="twitter:title" content="{E(t_es)}">
  <meta name="twitter:description" content="{E(DESC)}">
  <meta name="twitter:image" content="{URL}og.png">
  <link rel="manifest" href="/manifest.webmanifest">
  <meta name="theme-color" content="#163e86">
  <link rel="apple-touch-icon" href="/noticias/app/apple-touch-icon.png">
  <meta name="apple-mobile-web-app-title" content="MSC México">
  <link rel="stylesheet" href="../../news.css?v=14">
  <style>{CSS}</style>
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
  <script src="../../static.js?v=3" defer></script>
</head>
<body class="nx-static ex-page">
  <div class="nx-util"><div class="nx-wrap nx-utilin"><a class="nx-back" href="../../"><span data-lang="es">← Portada de Noticias</span><span data-lang="en">← News front page</span><span data-lang="pt">← Capa de Notícias</span></a><span></span>
    <nav class="nx-lang" aria-label="Idioma / Language / Idioma"><button type="button" data-setlang="es">ES</button><button type="button" data-setlang="en">EN</button><button type="button" data-setlang="pt">PT</button></nav></div></div>
  <header class="nx-mast"><div class="nx-wrap"><div class="nx-plate"><a class="nx-brand" href="/">Mr. Supply Chain<sup>®</sup> <span class="nx-mx">México</span></a><a class="nx-name" href="../../"><span data-lang="es">Noticias</span><span data-lang="en">News</span><span data-lang="pt">Notícias</span></a></div></div></header>
  <main class="nx-wrap nx-article">
    <article>
      <div class="ex-hero{' has-img' if os.path.exists(os.path.join(AQUI, 'hero.jpg')) else ''}">
        {'<figure class="ex-himg"><img src="hero.jpg?v=1" width="1232" height="941" alt="" fetchpriority="high"></figure>' if os.path.exists(os.path.join(AQUI, 'hero.jpg')) else ''}
        <p class="ex-tagline">{sp(L("Especial · Elecciones EE. UU. 2026", "Special · US Elections 2026", "Especial · Eleições EUA 2026"))}</p>
        <h1 class="nx-hl">{sp(TITULO)}</h1>
        <p class="nx-dek">{sp(DEK)}</p>
        <div class="nx-byline"><b><span data-lang="es">Mesa de mercados {E(MARCA)}</span><span data-lang="en">{E(MARCA)} markets desk</span><span data-lang="pt">Mesa de mercados {E(MARCA)}</span></b> · <time datetime="{ACTUALIZADO}">{sp(L("2 de noviembre de 2026", "November 2, 2026", "2 de novembro de 2026") if ACTUALIZADO == PUBLICADO else (lambda f: L("Actualizado: " + f["es"], "Updated: " + f["en"], "Atualizado: " + f["pt"]))(fecha_hora(ACTUALIZADO)))}</time></div>
        <div class="nx-share" aria-label="Compartir / Share / Compartilhar">
          <a href="https://www.linkedin.com/sharing/share-offsite/?url={quote(share % 'linkedin', safe='')}" target="_blank" rel="noopener">LinkedIn</a>
          <a href="https://x.com/intent/post?text={quote(t_es, safe='')}&url={quote(share % 'x', safe='')}&hashtags=MrSupplyChainMexico" target="_blank" rel="noopener">X</a>
          <a href="https://wa.me/?text={quote(t_es + ' ' + share % 'whatsapp', safe='')}" target="_blank" rel="noopener">WhatsApp</a>
          <a href="https://t.me/share/url?url={quote(share % 'telegram', safe='')}&text={quote(t_es, safe='')}" target="_blank" rel="noopener">Telegram</a>
        </div>
        {bloque_resultados()}
        {bloque_vivo()}
      </div>
      <nav class="ex-toc" aria-label="Contenido">{toc_html}</nav>

      <section class="ex-sec" id="resumen">
        <h2 class="nx-h2">{sp(L("En 60 segundos", "In 60 seconds", "Em 60 segundos"))}</h2>
        <div class="ex-two"><ol class="ex-60">{''.join(f"<li>{blk(r)}</li>" for r in RESUMEN)}</ol>{congreso_html()}</div>
        <p class="ex-src">{fuentes_html(['alj_map', 'forbes', 'sabato', 'rollcall', 'silver', 'wion', 'star', 'pwbm'])}</p>
      </section>

      <section class="ex-sec" id="escenarios">
        <h2 class="nx-h2">{sp(L("Tres escenarios y lo que significan", "Three scenarios and what they mean", "Três cenários e o que significam"))}</h2>
        {blk(L("Un dato ordena todo: ningún partido tendrá dos tercios para superar un veto, así que el resultado mueve la supervisión, el presupuesto y el tono, no los aranceles vigentes.", "One fact frames everything: no party will have two-thirds to override a veto, so the result moves oversight, budgets and tone, not the tariffs in force.", "Um dado organiza tudo: nenhum partido terá dois terços para derrubar um veto, então o resultado move a supervisão, o orçamento e o tom, não as tarifas vigentes."), cls='ex-intro')}
        {escenarios_html()}
        <p class="ex-src">{fuentes_html(['star', 'wita', 'wion', 'silver', 'wh_cr'])}</p>
      </section>

      <section class="ex-sec" id="estados">
        <h2 class="nx-h2">{sp(L("Estados Unidos, estado por estado", "The United States, state by state", "Estados Unidos, estado por estado"))}</h2>
        {blk(L("Las contiendas que definen el Congreso caen justo en estados clave para el comercio con México: Texas, Míchigan, Ohio e Iowa tienen elecciones al Senado en empate técnico.", "The races that decide Congress fall right on states key to trade with Mexico: Texas, Michigan, Ohio and Iowa all have toss-up Senate races.", "As disputas que definem o Congresso caem justamente em estados-chave para o comércio com o México: Texas, Michigan, Ohio e Iowa têm disputas empatadas para o Senado."), cls='ex-intro')}
        {mapa_html()}
        <h3 class="ex-subh" style="font-family:var(--serif);font-size:1.35rem;margin:30px 0 0">{sp(L("Las contiendas reñidas y su exposición", "The tight races and their exposure", "As disputas acirradas e sua exposição"))}</h3>
        {estados_clave_html()}
        {barras_html()}
        <p class="ex-src">{fuentes_html(['spectrum', 'sabato', 'epoch', 'newsweek', 'rollcall', 'piie', 'bts', 'pmsa'])}</p>
      </section>

      <section class="ex-sec" id="mexico">
        <h2 class="nx-h2">{sp(MEXICO["titulo"])}</h2>
        {cifras_html([(a, b) for a, b, _ in MEXICO['datos']], cls='ex-kpis six')}
        <div class="ex-two mx"><div class="ex-prose">{mx_pars}</div><div class="ex-side">{comercio_mx_html()}<div class="ex-vig">{blk(MEXICO["vigilar"])}</div></div></div>
        <p class="ex-src">{fuentes_html(MEXICO['fuentes'])}</p>
      </section>

      <section class="ex-sec" id="latam">
        <h2 class="nx-h2">{sp(L("América Latina, país por país", "Latin America, country by country", "América Latina, país por país"))}</h2>
        {blk(L("Desde el 24 de julio, unas 60 economías pagan 10% o 12.5% adicional bajo la Sección 301 (lo que ya paga 232 queda fuera). La etiqueta de cada tarjeta muestra esa tasa general.", "Since July 24, about 60 economies pay an extra 10% or 12.5% under Section 301 (goods already under 232 are excluded). Each card’s tag shows that general rate.", "Desde 24 de julho, cerca de 60 economias pagam 10% ou 12,5% adicionais pela Seção 301 (o que já paga a 232 fica de fora). A etiqueta de cada cartão mostra essa tarifa geral."), cls='ex-intro')}
        {aranceles_latam_html()}
        {tarjetas_html(LATAM, 'pais')}
      </section>

      <section class="ex-sec" id="mundo">
        <h2 class="nx-h2">{sp(L("El mundo, región por región", "The world, region by region", "O mundo, região por região"))}</h2>
        {tarjetas_html(MUNDO, 'reg')}
        <h3 style="font-family:var(--serif);font-size:1.35rem;margin:30px 0 0">{sp(L("Termómetros logísticos al cierre de octubre", "Logistics gauges at the end of October", "Termômetros logísticos no fim de outubro"))}</h3>
        <div class="ex-two fl">{fletes_html()}{cifras_html([INDICADORES[3], INDICADORES[4], INDICADORES[5]], cls='ex-kpis stack')}</div>
        <p class="ex-src">{fuentes_html(['drewry', 'ajot', 'fortune', 'nrf', 'wto'])}</p>
      </section>

      <section class="ex-sec" id="calendario">
        <h2 class="nx-h2">{sp(L("Calendario que importa más que la noche electoral", "The calendar that matters more than election night", "O calendário que importa mais que a noite eleitoral"))}</h2>
        {calendario_html()}
        <p class="ex-src">{fuentes_html(['opencount', 'carra', 'ff', 'wh_cr', 'bhfs', 'ec', 'scd_cn', 'ajot'])}</p>
      </section>

      <section class="ex-sec" id="acciones">
        <h2 class="nx-h2">{sp(L("Qué hacer en tu cadena esta semana", "What to do in your supply chain this week", "O que fazer na sua cadeia esta semana"))}</h2>
        <ol class="ex-acc">{acciones}</ol>
      </section>

      <aside class="nx-nl" aria-label="Cadena de Noticias SCM">
        <img class="nx-nl-logo" src="../../newsletter/cadena-logo-192.jpg" width="96" height="96" alt="" loading="lazy">
        <div class="nx-nl-txt">
          <p class="nx-nl-k"><span data-lang="es">Newsletter semanal en LinkedIn</span><span data-lang="en">Weekly newsletter on LinkedIn</span><span data-lang="pt">Newsletter semanal no LinkedIn</span></p>
          <p class="nx-nl-h">Cadena de Noticias SCM</p>
          <p class="nx-nl-p"><span data-lang="es">Recibe el seguimiento con resultados y la lectura de cada viernes, eslabón por eslabón.</span><span data-lang="en">Get the results follow-up and every Friday’s read, link by link.</span><span data-lang="pt">Receba o acompanhamento com resultados e a leitura de toda sexta-feira, elo por elo.</span></p>
        </div>
        <a class="nx-nl-btn" href="https://www.linkedin.com/newsletters/cadena-de-noticias-scm-7522126738555072512/" target="_blank" rel="noopener"><span data-lang="es">Recibirlo en LinkedIn →</span><span data-lang="en">Get it on LinkedIn →</span><span data-lang="pt">Receber no LinkedIn →</span></a>
      </aside>

      <section class="ex-sec" id="fuentes">
        <h2 class="nx-h2">{sp(L("Fuentes", "Sources", "Fontes"))}</h2>
        {blk(L("Cifras al 2 de noviembre de 2026. Calificaciones de contiendas de Cook Political Report salvo que se indique otra. Los escenarios describen efectos institucionales; no son pronóstico ni postura política. Donde las fuentes difieren, usamos la más reciente o la oficial.", "Figures as of November 2, 2026. Race ratings from the Cook Political Report unless noted. Scenarios describe institutional effects; they are not a forecast or a political stance. Where sources differ, we used the most recent or the official one.", "Dados de 2 de novembro de 2026. Classificações de disputas do Cook Political Report, salvo indicação. Os cenários descrevem efeitos institucionais; não são previsão nem posição política. Onde as fontes divergem, usamos a mais recente ou a oficial."), cls='ex-method')}
        {todas_fuentes()}
      </section>
    </article>
  </main>
  <footer class="nx-foot"><div class="nx-wrap"><p><a href="/">{E(MARCA)}</a> · <a href="../../archivo/"><span data-lang="es">Archivo</span><span data-lang="en">Archive</span><span data-lang="pt">Arquivo</span></a> · <a href="../../feed.xml">RSS</a></p>
    <p class="nx-disc"><span data-lang="es">Contenido informativo elaborado con apoyo de IA a partir de las fuentes públicas citadas. No es recomendación de inversión ni postura política.</span><span data-lang="en">Informational content prepared with AI assistance from the public sources cited. Not investment advice or a political stance.</span><span data-lang="pt">Conteúdo informativo elaborado com apoio de IA a partir das fontes públicas citadas. Não é recomendação de investimento nem posição política.</span></p><p class="nx-sp"><span data-lang="es">¿Quieres apoyar o patrocinar este sitio? Ayuda a que los briefs y el portal sigan siendo gratis. <a href="/contact/">Platiquemos →</a> Todo patrocinio está sujeto a revisión previa de mi empleador para evitar conflictos de interés.</span><span data-lang="en">Want to support or sponsor this site? It helps keep the briefs and the portal free. <a href="/contact/">Let’s talk →</a> Any sponsorship is subject to prior review by my employer to avoid conflicts of interest.</span><span data-lang="pt">Quer apoiar ou patrocinar este site? Isso ajuda a manter os briefs e o portal gratuitos. <a href="/contact/">Vamos conversar →</a> Todo patrocínio está sujeito à revisão prévia do meu empregador para evitar conflitos de interesse.</span></p><p class="nx-tm"><span data-lang="es">Mr. Supply Chain® es una marca registrada ante el Instituto Mexicano de la Propiedad Industrial (IMPI) y se usa exclusivamente en los Estados Unidos Mexicanos. No está afiliada ni tiene relación con marcas, personas o empresas que usen nombres similares en otros países.</span><span data-lang="en">Mr. Supply Chain® is a trademark registered with the Mexican Institute of Industrial Property (IMPI) and is used exclusively in Mexico. It is not affiliated with brands, people or companies using similar names in other countries.</span><span data-lang="pt">Mr. Supply Chain® é uma marca registrada no Instituto Mexicano da Propriedade Industrial (IMPI) e é usada exclusivamente nos Estados Unidos Mexicanos. Não é afiliada nem tem relação com marcas, pessoas ou empresas que usem nomes semelhantes em outros países.</span></p></div></footer>
  <script type="application/json" id="ex-data">{json.dumps(datos_mapa(), ensure_ascii=False).replace("</", "<\\/")}</script>
  <script type="application/json" id="ex-perf">{json.dumps(perf, ensure_ascii=False)}</script>
  <script>{JS}</script>
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "83d3c28484e44c21b9d87b1a9228f95c"}}'></script>
</body>
</html>
'''

def og():
    from PIL import Image, ImageDraw, ImageFont
    W, H = 1200, 630
    def font(name, size):
        for p in (f'/usr/share/fonts/truetype/dejavu/{name}.ttf', f'/usr/share/fonts/dejavu/{name}.ttf'):
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
        return ImageFont.load_default()
    src = os.path.join(AQUI, 'hero-full.jpg')
    im = Image.new('RGB', (W, H), '#0b1f47')
    if os.path.exists(src):
        h = Image.open(src).convert('RGB')
        h = h.resize((W, int(h.size[1] * W / h.size[0])))
        im.paste(h, (0, (H - h.size[1]) // 2))
    d = ImageDraw.Draw(im)
    d.rectangle([60, 60, 380, 96], fill='#a83246')
    d.text((74, 66), 'ESPECIAL · 3 NOV 2026', font=font('DejaVuSans-Bold', 22), fill='#ffffff')
    f1 = font('DejaVuSerif-Bold', 44)
    y = 128
    for line in ['Elecciones', 'en EE. UU.:', 'lo que se juega', 'supply chain']:
        d.text((60, y), line, font=f1, fill='#ffffff'); y += 56
    d.text((60, y + 16), 'Por estado · México', font=font('DejaVuSans', 22), fill='#9fc0ff')
    d.text((60, y + 46), 'LATAM · Mundo', font=font('DejaVuSans', 22), fill='#9fc0ff')
    d.text((60, 566), 'Mr. Supply Chain® México · Noticias', font=font('DejaVuSans-Bold', 20), fill='#ffffff')
    im.save(os.path.join(AQUI, 'og.png'), optimize=True)

if __name__ == '__main__':
    if ACTUALIZACIONES:
        ACTUALIZADO = max([ACTUALIZADO] + [a['t'] for a in ACTUALIZACIONES])
    with open(os.path.join(AQUI, 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(pagina())
    og()
    print('ok', URL)
