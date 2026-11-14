# -*- coding: utf-8 -*-
"""Genera el especial "Paro nacional de vuelos en EE. UU. y supply chain" (13 nov 2026).
Uso: python especiales/paro-aereo-eeuu-2026/build.py  → escribe index.html y og.png en esta carpeta.
Para actualizar: agrega una entrada a ACTUALIZACIONES (contenido.py), ajusta ESTADO si cambió el panorama y vuelve a correr."""
import os, sys, json, html, re
from urllib.parse import quote
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contenido import (L, ACTUALIZACIONES, ESTADO, RESUMEN, KPIS, FALLA, CRONO, CARGA, MEXICO, CANADA, CANADA_F,
                       ACCIONES_MERCADO, MERCADOS, MERCADOS_F, ESCENARIOS, ESCENARIOS_F, CALENDARIO, ACCIONES, FUENTES)

AQUI = os.path.dirname(os.path.abspath(__file__))
SLUG = 'paro-aereo-eeuu-2026'
SITE = 'https://mrsupplychain.ai/noticias/'
URL = SITE + f'especiales/{SLUG}/'
MARCA = 'Mr. Supply Chain® México'
E = html.escape
F = FUENTES
LANGS = ('es', 'en', 'pt')
PUBLICADO = '2026-11-13T18:35:00-06:00'
ACTUALIZADO = PUBLICADO

MES = {'es': ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'],
       'en': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
       'pt': ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']}


def sp(d, cls=''):
    c = f' class="{cls}"' if cls else ''
    return ''.join(f'<span data-lang="{l}"{c}>{E(d[l])}</span>' for l in LANGS)


_SENT = re.compile(r'([.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿¡"“])')


def _oraciones(txt):
    out, last = [], 0
    for m in _SENT.finditer(txt):
        prev = txt[last:m.start() + 1]
        w = prev.split()[-1] if prev.split() else ''
        _l = re.sub(r'[^A-Za-zÁÉÍÓÚÑáéíóúñ]', '', w)
        if (0 < len(_l) <= 3 and not re.search(r'\d', w)) or re.search(r'[A-Za-z]\.[A-Za-z]', w):
            continue
        out.append(prev.strip()); last = m.end()
    out.append(txt[last:].strip())
    return [o for o in out if o]


def blk_cortos(d, n=2):
    def ps(t):
        o = _oraciones(t)
        return ''.join('<p>' + E(' '.join(o[i:i + n])) + '</p>' for i in range(0, len(o), n))
    return ''.join(f'<div data-lang="{l}">{ps(d[l])}</div>' for l in LANGS)


def blk(d, tag='p', cls=''):
    c = f' class="{cls}"' if cls else ''
    return ''.join(f'<div data-lang="{l}"><{tag}{c}>{E(d[l])}</{tag}></div>' for l in LANGS)


LEADS = ('Qué pasó.', 'Por qué importa.', 'Qué sigue.', 'What happened.', 'Why it matters.', 'What comes next.',
         'O que aconteceu.', 'Por que importa.', 'O que vem.')


def blk_lead(d):
    out = []
    for l in LANGS:
        t = d[l]
        lead = next((x for x in LEADS if t.startswith(x)), None)
        if lead:
            out.append(f'<div data-lang="{l}"><p><strong class="ex-lead">{E(lead)}</strong> {E(t[len(lead):].strip())}</p></div>')
        else:
            out.append(f'<div data-lang="{l}"><p>{E(t)}</p></div>')
    return ''.join(out)


def fuentes_html(keys):
    vis = [k for i, k in enumerate(keys) if k in F and k not in keys[:i]]
    return ' · '.join(f'<a href="{E(F[k][1])}" target="_blank" rel="noopener nofollow">{E(F[k][0])}</a>' for k in vis)


def fecha_hora(iso):
    d = datetime.fromisoformat(iso)
    m = d.month - 1
    h = d.strftime('%H:%M')
    return L(f'{d.day} {MES["es"][m]}, {h} h (CDMX)', f'{MES["en"][m]} {d.day}, {h} (Mexico City)', f'{d.day} {MES["pt"][m]}, {h} (Cidade do México)')


def fecha_corta(f):
    p = f.split('-')
    y, m = p[0], int(p[1])
    if len(p) == 2:
        return L(f'{MES["es"][m - 1]} {y}', f'{MES["en"][m - 1]} {y}', f'{MES["pt"][m - 1]} {y}')
    d = int(p[2])
    return L(f'{d} {MES["es"][m - 1]}', f'{MES["en"][m - 1]} {d}', f'{d} {MES["pt"][m - 1]}')


def bloque_vivo():
    items = []
    for a in sorted(ACTUALIZACIONES, key=lambda a: a['t'], reverse=True):
        items.append(f'<li><time datetime="{a["t"]}">{sp(fecha_hora(a["t"]))}</time><h3>{sp(a["titulo"])}</h3>{blk_cortos(a["x"])}<p class="ex-src">{fuentes_html(a.get("f", []))}</p></li>')
    return (f'<section class="ex-vivo" id="al-momento"><p class="ex-vk"><span class="dot"></span>{sp(L("Al momento", "Live updates", "Ao vivo"))}</p>'
            f'<ol>{"".join(items)}</ol></section>')


def bloque_estado():
    ess = (f'<aside class="nx-ess"><p class="nx-essh"><span class="ic">⏱</span>{sp(L("Lo esencial en 30 segundos", "The essentials in 30 seconds", "O essencial em 30 segundos"))}</p>'
           f'<ul>{"".join(f"<li>{sp(x)}</li>" for x in ESTADO["esencial"])}</ul></aside>')
    ps = ESTADO['parrafos']
    pars = blk_lead(ps[0]) + (f'<details class="nx-moreblk"><summary>{sp(L("Leer el análisis completo", "Read the full analysis", "Ler a análise completa"))}</summary>'
                         f'{"".join(blk_lead(p) for p in ps[1:])}</details>')
    return f'<section class="ex-res" id="estado"><h2 class="nx-h2">{sp(ESTADO["titulo"])}</h2>{ess}<div class="nx-body ex-prose">{pars}</div><p class="ex-src">{fuentes_html(ESTADO["f"])}</p></section>'


def cifras_html(items, cls='ex-kpis'):
    out = []
    for lab, val, sub in items:
        out.append(f'<div class="ex-kpi"><span class="l">{sp(lab)}</span><b>{E(val)}</b><span class="s">{sp(sub)}</span></div>')
    return f'<div class="{cls}">' + ''.join(out) + '</div>'


def crono_html():
    return ('<div class="ex-panelc"><p class="ex-ct">' + sp(L('Cronología del viernes (hora CDMX)', 'Friday timeline (Mexico City time)', 'Cronologia de sexta (hora da Cidade do México)')) + '</p>'
            '<ol class="ex-tl">' + ''.join(f'<li><b>{E(h)}</b>{blk(t)}</li>' for h, t in CRONO) + '</ol>'
            '<p class="ex-src">' + fuentes_html(['yahoo_adv', 'duffy_x', 'cbs_main', 'ef_afac', 'abc_live', 'fox_live', 'cbsphl', 'efe_infobae']) + '</p></div>')


def tarjetas_html(lista):
    out = []
    for x in lista:
        tag = x['tag']
        tg = sp(tag) if isinstance(tag, dict) else E(tag)
        out.append(f'<article class="ex-card"><h3>{sp(x["t"])}<span class="ex-rate">{tg}</span></h3>{blk(x["x"])}<p class="ex-src">{fuentes_html(x["f"])}</p></article>')
    return '<div class="ex-cards">' + ''.join(out) + '</div>'


def mercado_html():
    mx = max(abs(v) for _, v in ACCIONES_MERCADO)
    rows = []
    for n, v in ACCIONES_MERCADO:
        w = abs(v) / mx * 50
        col = '#a83246' if v < 0 else '#1f8a5b'
        pos = f'right:50%' if v < 0 else 'left:50%'
        rows.append(f'<li><span class="n">{E(n)}</span><span class="b"><i style="{pos};width:{w:.1f}%;background:{col}"></i><em></em></span><span class="v">{v:+.2f}%</span></li>')
    return (f'<figure class="ex-fig"><figcaption>{sp(L("Cambio al cierre del viernes 13 de noviembre (%)", "Change at Friday, November 13 close (%)", "Variação no fechamento de sexta, 13 de novembro (%)"))}</figcaption>'
            f'<ul class="ex-dv">{"".join(rows)}</ul>'
            f'<p class="ex-src">{sp(L("El paro nacional se ordenó 6 minutos antes del cierre. Fuente: Yahoo Finance.", "The nationwide stop was ordered 6 minutes before the close. Source: Yahoo Finance.", "A paralisação nacional foi ordenada 6 minutos antes do fechamento. Fonte: Yahoo Finance."))}</p></figure>')


def escenarios_html():
    out = []
    for e in ESCENARIOS:
        out.append(f'<article class="ex-esc"><p class="ex-k">{sp(L("Escenario", "Scenario", "Cenário"))} {E(e["k"])}</p><h3>{sp(e["t"])}</h3><p class="ex-p">{sp(e["p"])}</p>{blk(e["x"])}'
                   f'<div class="ex-scm"><h4>{sp(L("Para supply chain", "For supply chains", "Para supply chain"))}</h4>{blk(e["scm"])}</div></article>')
    return '<div class="ex-escs">' + ''.join(out) + '</div>'


def calendario_html():
    return '<ol class="ex-cal">' + ''.join(f'<li{" class=hoy" if f == "2026-11-14" else ""}><time datetime="{f}">{sp(fecha_corta(f))}</time>{blk(t)}</li>' for f, t in CALENDARIO) + '</ol>'


def todas_fuentes():
    usadas = []
    def add(keys):
        for k in keys:
            if k in F and k not in usadas:
                usadas.append(k)
    for a in ACTUALIZACIONES:
        add(a.get('f', []))
    add(ESTADO['f']); add(['wsvn', 'fr24', 'aljaz', 'cnbc', 'foxwx']); add(FALLA['f'])
    for c in CARGA:
        add(c['f'])
    add(MEXICO['f']); add(CANADA_F); add(MERCADOS_F); add(ESCENARIOS_F); add(list(F))
    return '<ol class="ex-fuentes">' + ''.join(f'<li><a href="{E(F[k][1])}" target="_blank" rel="noopener nofollow">{E(F[k][0])}</a></li>' for k in usadas) + '</ol>'


TITULO = L('EE. UU. detiene sus vuelos: qué significa el paro aéreo nacional para supply chain',
           'The US grounds its flights: what the nationwide stop means for supply chains',
           'Os EUA param seus voos: o que a paralisação aérea nacional significa para supply chain')
DEK = L('Qué falló, cuánto se detuvo, cómo pega a la carga aérea, a México y a Canadá, tres escenarios y qué hacer en tu operación este fin de semana.',
        'What failed, how much stopped, how it hits air cargo, Mexico and Canada, three scenarios and what to do in your operation this weekend.',
        'O que falhou, quanto parou, como afeta a carga aérea, o México e o Canadá, três cenários e o que fazer na sua operação neste fim de semana.')
DESC = 'Especial: el paro nacional de vuelos de la FAA del 13 de noviembre de 2026 y su impacto en supply chain, carga aérea, México y Canadá, con escenarios y acciones.'

CSS = r'''
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
.ex-60 p{margin:0;font-family:var(--sans);font-size:1.04rem;line-height:1.6}
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
.ex-prose p{font-family:var(--sans);font-size:1.05rem;line-height:1.75;margin:0 0 16px;color:#2a2e35}
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
.ex-toc{display:flex;gap:18px;overflow-x:auto;scrollbar-width:none;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:10px 0;margin:6px 0 0;background:var(--paper)}
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

.ex-hero .nx-hl{max-width:26ch}
.ex-kpis.six .ex-kpi .s{font-size:11.5px}
.ex-tl{list-style:none;margin:0;padding:0;border-left:2px solid var(--line)}
.ex-tl li{position:relative;padding:0 0 12px 18px}
.ex-tl li::before{content:"";position:absolute;left:-6px;top:6px;width:10px;height:10px;border-radius:50%;background:#a83246}
.ex-tl b{font-family:var(--serif);font-size:1.05rem;color:var(--accent);font-variant-numeric:tabular-nums}
.ex-tl p{margin:2px 0 0;font-size:14px;line-height:1.5}
.ex-dv{list-style:none;padding:0;margin:0}
.ex-dv li{display:grid;grid-template-columns:minmax(0,11em) minmax(0,1fr) 5em;gap:10px;align-items:center;font-size:13.5px;padding:5px 0}
.ex-dv .b{position:relative;height:16px;background:var(--soft);border-radius:4px}
.ex-dv .b i{position:absolute;top:0;bottom:0;border-radius:3px}
.ex-dv .b em{position:absolute;left:50%;top:-3px;bottom:-3px;width:1px;background:#15171b}
.ex-dv .v{font-weight:700;font-variant-numeric:tabular-nums;text-align:right}
.ex-ca{margin-top:22px}
.ex-lead{font-weight:800;color:var(--accent);text-transform:uppercase;letter-spacing:.04em;font-size:.82em;margin-right:4px}
@media (max-width:599px){.ex-dv li{grid-template-columns:minmax(0,8.5em) minmax(0,1fr) 4.4em;font-size:12.5px}}
'''


def pagina():
    share = f'{URL}?utm_source=%s&utm_medium=social&utm_campaign=paroaereo2026'
    t_es = TITULO['es']
    ld = {'@context': 'https://schema.org', '@type': 'NewsArticle', 'headline': t_es[:110], 'alternativeHeadline': TITULO['en'][:110],
          'description': DESC, 'inLanguage': ['es-MX', 'en-US', 'pt-BR'], 'datePublished': PUBLICADO, 'dateModified': ACTUALIZADO,
          'url': URL, 'mainEntityOfPage': URL, 'image': [URL + 'og.png'], 'articleSection': 'Especial',
          'author': {'@type': 'Organization', 'name': f'Mesa de mercados {MARCA}', 'url': SITE},
          'publisher': {'@type': 'Organization', 'name': MARCA, 'url': 'https://mrsupplychain.ai/'}}
    toc = [('al-momento', L('Al momento', 'Live', 'Ao vivo')), ('resumen', L('En 60 segundos', 'In 60 seconds', 'Em 60 segundos')),
           ('falla', L('Qué falló', 'What failed', 'O que falhou')), ('carga', L('Carga aérea', 'Air cargo', 'Carga aérea')),
           ('mexico', L('México', 'Mexico', 'México')), ('canada', L('Canadá', 'Canada', 'Canadá')),
           ('mercados', L('Mercados', 'Markets', 'Mercados')), ('escenarios', L('Escenarios', 'Scenarios', 'Cenários')),
           ('calendario', L('Calendario', 'Calendar', 'Calendário')), ('acciones', L('Qué hacer', 'What to do', 'O que fazer')),
           ('fuentes', L('Fuentes', 'Sources', 'Fontes'))]
    toc_html = ''.join(f'<a href="#{i}">{sp(t)}</a>' for i, t in toc)
    acciones = ''.join(f'<li>{blk(a)}</li>' for a in ACCIONES)
    has_img = os.path.exists(os.path.join(AQUI, 'hero.jpg'))
    fecha_lbl = (lambda f: L('Actualizado: ' + f['es'], 'Updated: ' + f['en'], 'Atualizado: ' + f['pt']))(fecha_hora(ACTUALIZADO))
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
  <link rel="stylesheet" href="../../news.css?v=22">
  <style>{CSS}</style>
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
  <script src="../../static.js?v=4" defer></script>
  <script src="../../ui.js?v=2" defer></script>
</head>
<body class="nx-static ex-page">
  <div class="nx-util"><div class="nx-wrap nx-utilin"><a class="nx-back" href="../../"><span data-lang="es">← Portada de Noticias</span><span data-lang="en">← News front page</span><span data-lang="pt">← Capa de Notícias</span></a><span></span>
    <nav class="nx-lang" aria-label="Idioma / Language / Idioma"><button type="button" data-setlang="es">ES</button><button type="button" data-setlang="en">EN</button><button type="button" data-setlang="pt">PT</button></nav></div></div>
  <header class="nx-mast"><div class="nx-wrap"><div class="nx-plate"><a class="nx-brand" href="/">Mr. Supply Chain<sup>®</sup> <span class="nx-mx">México</span></a><a class="nx-name" href="../../"><span data-lang="es">Noticias</span><span data-lang="en">News</span><span data-lang="pt">Notícias</span></a></div></div></header>
  <main class="nx-wrap nx-article">
    <article>
      <div class="ex-hero{' has-img' if has_img else ''}">
        {'<figure class="ex-himg"><img src="hero.jpg?v=1" width="1232" height="941" alt="" fetchpriority="high"></figure>' if has_img else ''}
        <p class="ex-tagline">{sp(L("Especial · Paro aéreo en EE. UU.", "Special · US air shutdown", "Especial · Paralisação aérea nos EUA"))}</p>
        <h1 class="nx-hl">{sp(TITULO)}</h1>
        <p class="nx-dek">{sp(DEK)}</p>
        <div class="nx-byline"><b><span data-lang="es">Mesa de mercados {E(MARCA)}</span><span data-lang="en">{E(MARCA)} markets desk</span><span data-lang="pt">Mesa de mercados {E(MARCA)}</span></b> · <time datetime="{ACTUALIZADO}">{sp(fecha_lbl)}</time></div>
        <div class="nx-share" aria-label="Compartir / Share / Compartilhar">
          <a href="https://www.linkedin.com/sharing/share-offsite/?url={quote(share % 'linkedin', safe='')}" target="_blank" rel="noopener">LinkedIn</a>
          <a href="https://x.com/intent/post?text={quote(t_es, safe='')}&url={quote(share % 'x', safe='')}&hashtags=MrSupplyChainMexico" target="_blank" rel="noopener">X</a>
          <a href="https://wa.me/?text={quote(t_es + ' ' + share % 'whatsapp', safe='')}" target="_blank" rel="noopener">WhatsApp</a>
          <a href="https://t.me/share/url?url={quote(share % 'telegram', safe='')}&text={quote(t_es, safe='')}" target="_blank" rel="noopener">Telegram</a>
        </div>
        {bloque_estado()}
        {bloque_vivo()}
      </div>
      <nav class="ex-toc" aria-label="Contenido">{toc_html}</nav>

      <section class="ex-sec" id="resumen">
        <h2 class="nx-h2">{sp(L("En 60 segundos", "In 60 seconds", "Em 60 segundos"))}</h2>
        <div class="ex-two"><ol class="ex-60">{''.join(f"<li>{blk(r)}</li>" for r in RESUMEN)}</ol>{crono_html()}</div>
        {cifras_html(KPIS, cls='ex-kpis six')}
        <p class="ex-src">{fuentes_html(['abc_sat', 'cbsphl', 'autonoc', 'cronista', 'cnbc', 'wsvn', 'efe_unitel'])}</p>
      </section>

      <section class="ex-sec" id="falla">
        <h2 class="nx-h2">{sp(L("Qué falló: la red que conecta al control aéreo", "What failed: the network that links air traffic control", "O que falhou: a rede que conecta o controle aéreo"))}</h2>
        <div class="ex-two mx"><div class="ex-prose">{''.join(blk(p) for p in FALLA['parrafos'])}</div><div class="ex-side"><div class="ex-vig">{blk(FALLA["vigilar"])}</div></div></div>
        <p class="ex-src">{fuentes_html(FALLA['f'])}</p>
      </section>

      <section class="ex-sec" id="carga">
        <h2 class="nx-h2">{sp(L("Carga aérea y paquetería: un día menos de red", "Air cargo and parcels: one day less of network", "Carga aérea e encomendas: um dia a menos de rede"))}</h2>
        {blk(L("El paro aplicó a todos los despegues, de pasajeros y de carga. Estos son los eslabones que más lo resienten.", "The stop applied to all departures, passenger and cargo alike. These are the links that feel it most.", "A paralisação valeu para todas as decolagens, de passageiros e de carga. Estes são os elos que mais a sentem."), cls='ex-intro')}
        {tarjetas_html(CARGA)}
      </section>

      <section class="ex-sec" id="mexico">
        <h2 class="nx-h2">{sp(L("México: aviones en tierra y la frontera como válvula", "Mexico: aircraft grounded and the border as a release valve", "México: aviões em solo e a fronteira como válvula"))}</h2>
        <div class="ex-two mx"><div class="ex-prose">{''.join(blk(p) for p in MEXICO['parrafos'])}</div><div class="ex-side"><div class="ex-vig">{blk(MEXICO["vigilar"])}</div></div></div>
        <p class="ex-src">{fuentes_html(MEXICO['f'])}</p>
      </section>

      <section class="ex-sec" id="canada">
        <h2 class="nx-h2">{sp(L("Canadá: el corredor transfronterizo, detenido", "Canada: the cross-border corridor, halted", "Canadá: o corredor transfronteiriço, parado"))}</h2>
        <div class="ex-prose">{blk(CANADA)}</div>
        <p class="ex-src">{fuentes_html(CANADA_F)}</p>
      </section>

      <section class="ex-sec" id="mercados">
        <h2 class="nx-h2">{sp(L("Mercados: la prueba llega el lunes", "Markets: the test comes Monday", "Mercados: o teste vem na segunda"))}</h2>
        <div class="ex-two"><div class="ex-prose">{blk(MERCADOS)}</div>{mercado_html()}</div>
        <p class="ex-src">{fuentes_html(MERCADOS_F)}</p>
      </section>

      <section class="ex-sec" id="escenarios">
        <h2 class="nx-h2">{sp(L("Tres escenarios y lo que significan", "Three scenarios and what they mean", "Três cenários e o que significam"))}</h2>
        {blk(L("Lo que define el impacto no es el paro del viernes, sino la causa: si fue un error puntual o una falla de diseño en la red de comunicaciones. Son escenarios, no pronósticos.", "What defines the impact is not Friday\'s stop but its cause: a one-off error or a design flaw in the communications network. These are scenarios, not forecasts.", "O que define o impacto não é a paralisação de sexta, mas a causa: um erro pontual ou uma falha de projeto na rede de comunicações. São cenários, não previsões."), cls='ex-intro')}
        {escenarios_html()}
        <p class="ex-src">{fuentes_html(ESCENARIOS_F)}</p>
      </section>

      <section class="ex-sec" id="calendario">
        <h2 class="nx-h2">{sp(L("Fechas que vigilar", "Dates to watch", "Datas para acompanhar"))}</h2>
        {calendario_html()}
        <p class="ex-src">{fuentes_html(['fox_live', 'pbs_shutdown', 'wh_cr', 'reuters_bedford'])}</p>
      </section>

      <section class="ex-sec" id="acciones">
        <h2 class="nx-h2">{sp(L("Qué hacer en tu cadena este fin de semana", "What to do in your supply chain this weekend", "O que fazer na sua cadeia neste fim de semana"))}</h2>
        <ol class="ex-acc">{acciones}</ol>
      </section>

      <aside class="nx-nl" aria-label="Cadena de Noticias SCM">
        <img class="nx-nl-logo" src="../../newsletter/cadena-logo-192.jpg" width="96" height="96" alt="" loading="lazy">
        <div class="nx-nl-txt">
          <p class="nx-nl-k"><span data-lang="es">Newsletter semanal en LinkedIn</span><span data-lang="en">Weekly newsletter on LinkedIn</span><span data-lang="pt">Newsletter semanal no LinkedIn</span></p>
          <p class="nx-nl-h">Cadena de Noticias SCM</p>
          <p class="nx-nl-p"><span data-lang="es">Recibe la lectura de cada viernes, eslabón por eslabón.</span><span data-lang="en">Get every Friday’s read, link by link.</span><span data-lang="pt">Receba a leitura de toda sexta-feira, elo por elo.</span></p>
        </div>
        <a class="nx-nl-btn" href="https://www.linkedin.com/newsletters/cadena-de-noticias-scm-7522126738555072512/" target="_blank" rel="noopener"><span data-lang="es">Recibirlo en LinkedIn →</span><span data-lang="en">Get it on LinkedIn →</span><span data-lang="pt">Receber no LinkedIn →</span></a>
      </aside>

      <section class="ex-sec" id="fuentes">
        <h2 class="nx-h2">{sp(L("Fuentes", "Sources", "Fontes"))}</h2>
        {blk(L("Cifras al 14 de noviembre de 2026, 08:07 h CDMX; las horas están en hora de la Ciudad de México (la hora del Este es una hora más). Los conteos de vuelos cambian minuto a minuto: usamos el corte más reciente con hora. La causa técnica es la que explicaron Duffy y Mullin; el informe formal de la FAA aún no se publica.", "Figures as of November 14, 2026, 8:07 a.m. Mexico City time; times are Mexico City time (Eastern is one hour later). Flight counts change by the minute: we used the latest time-stamped count. The technical cause is the one Duffy and Mullin described; the FAA's formal report has not been published yet.", "Dados de 14 de novembro de 2026, 08h07 (Cidade do México); os horários estão na hora da Cidade do México (o horário do Leste é uma hora a mais). As contagens de voos mudam a cada minuto: usamos o corte mais recente com horário. A causa técnica é a explicada por Duffy e Mullin; o relatório formal da FAA ainda não foi publicado."), cls='ex-method')}
        {todas_fuentes()}
      </section>
    </article>
  </main>
  <footer class="nx-foot"><div class="nx-wrap"><p><a href="/">{E(MARCA)}</a> · <a href="../../archivo/"><span data-lang="es">Archivo</span><span data-lang="en">Archive</span><span data-lang="pt">Arquivo</span></a> · <a href="../../feed.xml">RSS</a></p>
    <p class="nx-disc"><span data-lang="es">Contenido informativo y de carácter general, elaborado con apoyo de IA a partir de las fuentes públicas citadas. Las recomendaciones para supply chain son sugerencias generales: no constituyen asesoría profesional, financiera, legal, fiscal ni de inversión, y cada lector debe evaluarlas según su propia situación y bajo su responsabilidad. Mr. Supply Chain México no se hace responsable de las decisiones que se tomen con base en este contenido.</span><span data-lang="en">General informational content prepared with AI assistance from the public sources cited. Supply chain recommendations are general suggestions: they are not professional, financial, legal, tax or investment advice, and each reader should assess them against their own situation and at their own risk. Mr. Supply Chain México is not responsible for decisions made based on this content.</span><span data-lang="pt">Conteúdo informativo e de caráter geral, elaborado com apoio de IA a partir das fontes públicas citadas. As recomendações para supply chain são sugestões gerais: não constituem assessoria profissional, financeira, jurídica, fiscal nem de investimento, e cada leitor deve avaliá-las conforme sua própria situação e sob sua responsabilidade. Mr. Supply Chain México não se responsabiliza pelas decisões tomadas com base neste conteúdo.</span></p><p class="nx-sp"><span data-lang="es">¿Quieres apoyar o patrocinar este sitio? Ayuda a que los briefs y el portal sigan siendo gratis. <a href="/contact/">Platiquemos →</a> Todo patrocinio está sujeto a revisión previa de mi empleador para evitar conflictos de interés.</span><span data-lang="en">Want to support or sponsor this site? It helps keep the briefs and the portal free. <a href="/contact/">Let’s talk →</a> Any sponsorship is subject to prior review by my employer to avoid conflicts of interest.</span><span data-lang="pt">Quer apoiar ou patrocinar este site? Isso ajuda a manter os briefs e o portal gratuitos. <a href="/contact/">Vamos conversar →</a> Todo patrocínio está sujeito à revisão prévia do meu empregador para evitar conflitos de interesse.</span></p><p class="nx-tm"><span data-lang="es">Mr. Supply Chain® es una marca registrada ante el Instituto Mexicano de la Propiedad Industrial (IMPI) y se usa exclusivamente en los Estados Unidos Mexicanos. No está afiliada ni tiene relación con marcas, personas o empresas que usen nombres similares en otros países.</span><span data-lang="en">Mr. Supply Chain® is a trademark registered with the Mexican Institute of Industrial Property (IMPI) and is used exclusively in Mexico. It is not affiliated with brands, people or companies using similar names in other countries.</span><span data-lang="pt">Mr. Supply Chain® é uma marca registrada no Instituto Mexicano da Propriedade Industrial (IMPI) e é usada exclusivamente nos Estados Unidos Mexicanos. Não é afiliada nem tem relação com marcas, pessoas ou empresas que usem nomes semelhantes em outros países.</span></p></div></footer>
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
    im = Image.new('RGB', (W, H), '#0b1f47')
    src = os.path.join(AQUI, 'hero-full.jpg')
    if os.path.exists(src):
        h = Image.open(src).convert('RGB')
        h = h.resize((int(h.size[0] * H / h.size[1]), H))
        im.paste(h, (W - h.size[0] + 160, 0))
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ov).rectangle([0, 0, 640, H], fill=(11, 31, 71, 225))
    im = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')
    d = ImageDraw.Draw(im)
    d.rectangle([60, 60, 400, 96], fill='#a83246')
    d.text((74, 66), 'ESPECIAL · 13 NOV 2026', font=font('DejaVuSans-Bold', 22), fill='#ffffff')
    f1 = font('DejaVuSerif-Bold', 46)
    y = 128
    for line in ['EE. UU. detiene', 'sus vuelos:', 'qué significa', 'para supply chain']:
        d.text((60, y), line, font=f1, fill='#ffffff'); y += 58
    d.text((60, y + 16), 'Carga aérea · México · Canadá', font=font('DejaVuSans', 22), fill='#9fc0ff')
    d.text((60, y + 46), 'Escenarios · Qué hacer', font=font('DejaVuSans', 22), fill='#9fc0ff')
    d.text((60, 566), 'Mr. Supply Chain® México · Noticias', font=font('DejaVuSans-Bold', 20), fill='#ffffff')
    im.save(os.path.join(AQUI, 'og.png'), optimize=True)


if __name__ == '__main__':
    if ACTUALIZACIONES:
        ACTUALIZADO = max([ACTUALIZADO] + [a['t'] for a in ACTUALIZACIONES])
    with open(os.path.join(AQUI, 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(pagina())
    og()
    print('ok', URL)
