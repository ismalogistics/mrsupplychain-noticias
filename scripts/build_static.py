"""Genera las páginas estáticas del portal para buscadores y redes sociales.

- brief/<id>/index.html : una página por brief (NewsArticle, Open Graph, bilingüe).
- brief/<id>/og.png     : imagen para compartir (1200x630).
- archivo/index.html    : archivo navegable de todos los briefs.
- feed.xml              : RSS 2.0 con los últimos briefs.
- sitemap.xml           : sitemap del portal con etiquetas de Google News para lo reciente.

Lo corre la GitHub Action. Sólo lee data/; no modifica datos.
"""
import html
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

ROOT = os.path.join(os.path.dirname(__file__), '..')
DATA = os.path.join(ROOT, 'data')
SITE = 'https://mrsupplychain.ai/noticias/'
MARCA = 'Mr. Supply Chain® México'
MOM = {'es': {'apertura': 'Apertura', 'mediodia': 'Mediodía', 'cierre': 'Cierre'},
       'en': {'apertura': 'Open', 'mediodia': 'Midday', 'cierre': 'Close'}}
MKT = {'es': {'global': 'Global', 'latam': 'LATAM', 'mexico': 'México'},
       'en': {'global': 'Global', 'latam': 'LATAM', 'mexico': 'Mexico'}}
MES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
MES_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
E = html.escape


def fecha_es(f):
    y, m, d = f.split('-')
    return f'{int(d)} {MES[int(m) - 1]} {y}'


def fecha_en(f):
    y, m, d = f.split('-')
    return f'{MES_EN[int(m) - 1]} {int(d)}, {y}'


def iso_pub(b):
    """Fecha y hora de publicación aproximada (hora CDMX del brief, UTC-6)."""
    h = (b.get('hora') or '12:00').split()[0]
    try:
        hh, mm = [int(x) for x in h.split(':')]
    except Exception:
        hh, mm = 12, 0
    dt = datetime.fromisoformat(b['fecha']).replace(hour=hh, minute=mm, tzinfo=timezone(timedelta(hours=-6)))
    return dt


def utm(url, medio):
    return f'{url}?utm_source={medio}&utm_medium=social&utm_campaign=noticias'


def cargar_briefs():
    out = {}
    d = os.path.join(DATA, 'briefs')
    for fn in sorted(os.listdir(d)):
        if fn.endswith('.json'):
            try:
                b = json.load(open(os.path.join(d, fn), encoding='utf-8'))
                out[b['id']] = b
            except Exception as exc:
                print('brief ilegible', fn, exc, file=sys.stderr)
    return out


def og_png(b, path):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return False
    W, H = 1200, 630
    img = Image.new('RGB', (W, H), '#faf9f6')
    d = ImageDraw.Draw(img)
    fdir = '/usr/share/fonts/truetype/dejavu/'

    def font(name, size):
        try:
            return ImageFont.truetype(fdir + name, size)
        except Exception:
            return ImageFont.load_default()

    accent = {'global': '#1e4f9c', 'latam': '#1f8a5b', 'mexico': '#a83246'}.get(b['mercado'], '#1e4f9c')
    d.rectangle([0, 0, W, 14], fill=accent)
    d.text((64, 52), 'Mr. Supply Chain® México', font=font('DejaVuSerif-Bold.ttf', 34), fill='#15171b')
    tag = ' NOTICIAS '
    tf = font('DejaVuSans-Bold.ttf', 22)
    tw = d.textlength(tag, font=tf)
    d.rectangle([W - 64 - tw - 8, 54, W - 64, 90], fill=accent)
    d.text((W - 64 - tw - 4, 58), tag, font=tf, fill='#ffffff')
    kicker = f"{MOM['es'][b['momento']].upper()} · {MKT['es'][b['mercado']].upper()} · {fecha_es(b['fecha'])}"
    d.text((64, 140), kicker, font=font('DejaVuSans-Bold.ttf', 24), fill=accent)
    # Titular con ajuste de línea
    t = b['es']['titular']
    size = 58
    while size > 34:
        f = font('DejaVuSerif-Bold.ttf', size)
        lines, line = [], ''
        for w in t.split():
            test = (line + ' ' + w).strip()
            if d.textlength(test, font=f) <= W - 128:
                line = test
            else:
                lines.append(line)
                line = w
        lines.append(line)
        if len(lines) * size * 1.18 <= 300:
            break
        size -= 4
    y = 190
    for ln in lines:
        d.text((64, y), ln, font=f, fill='#15171b')
        y += int(size * 1.18)
    d.line([64, H - 92, W - 64, H - 92], fill='#e3e0d8', width=2)
    d.text((64, H - 70), 'Mercados leídos para supply chain', font=font('DejaVuSans.ttf', 24), fill='#6a6f77')
    d.text((W - 64 - d.textlength('mrsupplychain.ai/noticias', font=font('DejaVuSans-Bold.ttf', 24)), H - 70),
           'mrsupplychain.ai/noticias', font=font('DejaVuSans-Bold.ttf', 24), fill=accent)
    img.save(path, 'PNG', optimize=True)
    return True


def bloques_html(L):
    out = []
    for x in L.get('bloques', []):
        out.append(f'<section class="nx-sec"><h4>{E(x["t"])}</h4><p>{E(x["x"])}</p></section>')
    return '\n'.join(out)


def pagina_brief(b, prev_b, next_b):
    url = f'{SITE}brief/{b["id"]}/'
    es, en = b['es'], b.get('en', b['es'])
    pub = iso_pub(b)
    desc = (es.get('scm') or (es.get('bloques') or [{'x': ''}])[0]['x'])[:200]
    titulo = f'{es["titular"]} | Noticias {MARCA}'
    ld = {
        '@context': 'https://schema.org', '@type': 'NewsArticle', 'headline': es['titular'][:110],
        'alternativeHeadline': en['titular'][:110], 'description': desc, 'inLanguage': ['es-MX', 'en-US'],
        'datePublished': pub.isoformat(), 'dateModified': pub.isoformat(), 'url': url, 'mainEntityOfPage': url,
        'image': [url + 'og.png'], 'articleSection': f"{MOM['es'][b['momento']]} · {MKT['es'][b['mercado']]}",
        'author': {'@type': 'Organization', 'name': f'Mesa de mercados {MARCA}', 'url': SITE},
        'publisher': {'@type': 'Organization', 'name': MARCA, 'url': 'https://mrsupplychain.ai/'},
        'isPartOf': {'@type': 'CollectionPage', '@id': SITE + '#page'},
        'citation': [f['u'] for f in b.get('fuentes', [])],
    }
    fuentes = ' · '.join(f'<a href="{E(f["u"])}" target="_blank" rel="noopener nofollow">{E(f["t"])}</a>' for f in b.get('fuentes', []))
    sc_es = f'<aside class="nx-scm{" wk" if b.get("fin_de_semana") else ""}"><h4>{"Para el fin de semana" if b.get("fin_de_semana") else "Para supply chain"}</h4><p>{E(es.get("scm", ""))}</p></aside>' if es.get('scm') else ''
    sc_en = f'<aside class="nx-scm{" wk" if b.get("fin_de_semana") else ""}"><h4>{"For the weekend" if b.get("fin_de_semana") else "For supply chain"}</h4><p>{E(en.get("scm", ""))}</p></aside>' if en.get('scm') else ''
    share_t = E(es['titular'])
    nav = []
    if prev_b:
        nav.append(f'<a class="prev" href="../{prev_b["id"]}/">← {E(prev_b["es"]["titular"])}</a>')
    if next_b:
        nav.append(f'<a class="next" href="../{next_b["id"]}/">{E(next_b["es"]["titular"])} →</a>')
    from urllib.parse import quote
    return f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{E(titulo)}</title>
  <meta name="description" content="{E(desc)}">
  <link rel="canonical" href="{url}">
  <link rel="alternate" type="application/rss+xml" title="Noticias {E(MARCA)}" href="{SITE}feed.xml">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="{E(MARCA)}">
  <meta property="og:title" content="{E(es['titular'])}">
  <meta property="og:description" content="{E(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{url}og.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="es_MX">
  <meta property="og:locale:alternate" content="en_US">
  <meta property="article:published_time" content="{pub.isoformat()}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@MrSupplyChainX">
  <meta name="twitter:title" content="{E(es['titular'])}">
  <meta name="twitter:description" content="{E(desc)}">
  <meta name="twitter:image" content="{url}og.png">
  <link rel="stylesheet" href="../../news.css">
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
  <script src="../../static.js" defer></script>
</head>
<body class="nx-static">
  <div class="nx-util"><div class="nx-wrap nx-utilin"><a class="nx-back" href="../../"><span data-lang="es">← Portada de Noticias</span><span data-lang="en">← News front page</span></a><span></span>
    <nav class="nx-lang" aria-label="Idioma / Language"><button type="button" data-setlang="es">ES</button><button type="button" data-setlang="en">EN</button></nav></div></div>
  <header class="nx-mast"><div class="nx-wrap"><div class="nx-plate"><a class="nx-brand" href="/">Mr. Supply Chain<sup>®</sup> <span class="nx-mx">México</span></a><a class="nx-name" href="../../"><span data-lang="es">Noticias</span><span data-lang="en">News</span></a></div></div></header>
  <main class="nx-wrap nx-article">
    <article>
      <p class="nx-kick"><span data-lang="es">{MOM['es'][b['momento']]}</span><span data-lang="en">{MOM['en'][b['momento']]}</span><span class="sep">|</span><span data-lang="es">{MKT['es'][b['mercado']]}</span><span data-lang="en">{MKT['en'][b['mercado']]}</span></p>
      <h1 class="nx-hl"><span data-lang="es">{E(es['titular'])}</span><span data-lang="en">{E(en['titular'])}</span></h1>
      <div class="nx-byline"><b><span data-lang="es">Mesa de mercados {E(MARCA)}</span><span data-lang="en">{E(MARCA)} markets desk</span></b> · <time datetime="{pub.isoformat()}"><span data-lang="es">{fecha_es(b['fecha'])}</span><span data-lang="en">{fecha_en(b['fecha'])}</span> · {E(b.get('hora', ''))}</time></div>
      <div class="nx-share" aria-label="Compartir">
        <a href="https://www.linkedin.com/sharing/share-offsite/?url={quote(utm(url, 'linkedin'), safe='')}" target="_blank" rel="noopener">LinkedIn</a>
        <a href="https://x.com/intent/post?text={quote(es['titular'], safe='')}&url={quote(utm(url, 'x'), safe='')}&hashtags=MrSupplyChainMexico" target="_blank" rel="noopener">X</a>
        <a href="https://wa.me/?text={quote(es['titular'] + ' ' + utm(url, 'whatsapp'), safe='')}" target="_blank" rel="noopener">WhatsApp</a>
        <a href="https://t.me/share/url?url={quote(utm(url, 'telegram'), safe='')}&text={quote(es['titular'], safe='')}" target="_blank" rel="noopener">Telegram</a>
      </div>
      <div data-lang="es"><div class="nx-body">{bloques_html(es)}{sc_es}</div></div>
      <div data-lang="en"><div class="nx-body">{bloques_html(en)}{sc_en}</div></div>
      <p class="nx-src"><span data-lang="es">Fuentes</span><span data-lang="en">Sources</span>: {fuentes}</p>
      <p class="nx-cta"><a href="../../"><span data-lang="es">Ver el portal completo: mercados en vivo, mapa de calor, tendencias por industria y lectura para supply chain →</span><span data-lang="en">See the full portal: live markets, heatmap, industry trends and the supply chain read →</span></a></p>
      <nav class="nx-pn">{''.join(nav)}</nav>
    </article>
  </main>
  <footer class="nx-foot"><div class="nx-wrap"><p><a href="/">{E(MARCA)}</a> · <a href="../../archivo/"><span data-lang="es">Archivo</span><span data-lang="en">Archive</span></a> · <a href="../../feed.xml">RSS</a></p>
    <p class="nx-disc"><span data-lang="es">Contenido informativo elaborado con apoyo de IA a partir de las fuentes públicas citadas. No es recomendación de inversión.</span><span data-lang="en">Informational content prepared with AI assistance from the public sources cited. Not investment advice.</span></p></div></footer>
</body>
</html>
'''


def pagina_archivo(lista):
    filas = []
    fecha_act = None
    for b in lista:
        if b['fecha'] != fecha_act:
            if fecha_act:
                filas.append('</ul>')
            fecha_act = b['fecha']
            filas.append(f'<h2 class="nx-arch-d"><span data-lang="es">{fecha_es(b["fecha"])}</span><span data-lang="en">{fecha_en(b["fecha"])}</span></h2><ul class="nx-arch">')
        filas.append(f'<li><a href="../brief/{b["id"]}/"><span class="m"><span data-lang="es">{MOM["es"][b["momento"]]} · {MKT["es"][b["mercado"]]}</span><span data-lang="en">{MOM["en"][b["momento"]]} · {MKT["en"][b["mercado"]]}</span></span><span class="t"><span data-lang="es">{E(b["es"]["titular"])}</span><span data-lang="en">{E(b.get("en", b["es"])["titular"])}</span></span></a></li>')
    if fecha_act:
        filas.append('</ul>')
    return f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Archivo de briefs de mercados para supply chain | Noticias {E(MARCA)}</title>
  <meta name="description" content="Todos los briefs de apertura, mediodía y cierre de mercados, global, LATAM y México, con lectura para supply chain y operaciones.">
  <link rel="canonical" href="{SITE}archivo/">
  <link rel="alternate" type="application/rss+xml" title="Noticias {E(MARCA)}" href="{SITE}feed.xml">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Archivo de briefs · Noticias {E(MARCA)}">
  <meta property="og:url" content="{SITE}archivo/">
  <meta property="og:image" content="{SITE}og.png">
  <link rel="stylesheet" href="../news.css">
  <script src="../static.js" defer></script>
</head>
<body class="nx-static">
  <div class="nx-util"><div class="nx-wrap nx-utilin"><a class="nx-back" href="../"><span data-lang="es">← Portada de Noticias</span><span data-lang="en">← News front page</span></a><span></span>
    <nav class="nx-lang" aria-label="Idioma / Language"><button type="button" data-setlang="es">ES</button><button type="button" data-setlang="en">EN</button></nav></div></div>
  <header class="nx-mast"><div class="nx-wrap"><div class="nx-plate"><a class="nx-brand" href="/">Mr. Supply Chain<sup>®</sup> <span class="nx-mx">México</span></a><a class="nx-name" href="../"><span data-lang="es">Noticias</span><span data-lang="en">News</span></a></div></div></header>
  <main class="nx-wrap nx-article">
    <h1 class="nx-h2"><span data-lang="es">Archivo de briefs</span><span data-lang="en">Brief archive</span></h1>
    {''.join(filas)}
  </main>
  <footer class="nx-foot"><div class="nx-wrap"><p><a href="/">{E(MARCA)}</a> · <a href="../feed.xml">RSS</a></p></div></footer>
</body>
</html>
'''


def feed(lista, ahora):
    items = []
    for b in lista[:40]:
        url = f'{SITE}brief/{b["id"]}/'
        es = b['es']
        desc = ' '.join(x['x'] for x in es.get('bloques', [])[:2])
        if es.get('scm'):
            desc += ' — ' + es['scm']
        items.append(f'''  <item>
    <title>{E(es["titular"])}</title>
    <link>{url}</link>
    <guid isPermaLink="true">{url}</guid>
    <pubDate>{format_datetime(iso_pub(b))}</pubDate>
    <category>{MOM["es"][b["momento"]]} · {MKT["es"][b["mercado"]]}</category>
    <description>{E(desc)}</description>
    <enclosure url="{url}og.png" type="image/png" length="0"/>
  </item>''')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Noticias · {E(MARCA)}</title>
  <link>{SITE}</link>
  <atom:link href="{SITE}feed.xml" rel="self" type="application/rss+xml"/>
  <description>Briefs diarios de mercados (apertura, mediodía y cierre), global, LATAM y México, leídos para supply chain y operaciones.</description>
  <language>es-MX</language>
  <lastBuildDate>{format_datetime(iso_pub(lista[0]) if lista else ahora)}</lastBuildDate>
{chr(10).join(items)}
</channel>
</rss>
'''


def sitemap(lista, ahora):
    ult = iso_pub(lista[0]).isoformat() if lista else ahora.isoformat()
    urls = [f'  <url><loc>{SITE}</loc><lastmod>{ult}</lastmod><changefreq>hourly</changefreq></url>',
            f'  <url><loc>{SITE}archivo/</loc><lastmod>{ult}</lastmod><changefreq>daily</changefreq></url>']
    limite = ahora - timedelta(days=2)
    for b in lista:
        pub = iso_pub(b)
        news = ''
        if pub >= limite:
            news = (f'<news:news><news:publication><news:name>Noticias {E(MARCA)}</news:name><news:language>es</news:language></news:publication>'
                    f'<news:publication_date>{pub.isoformat()}</news:publication_date><news:title>{E(b["es"]["titular"])}</news:title></news:news>')
        urls.append(f'  <url><loc>{SITE}brief/{b["id"]}/</loc><lastmod>{pub.isoformat()}</lastmod>{news}</url>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">\n' + '\n'.join(urls) + '\n</urlset>\n')


def main():
    ahora = datetime.now(timezone.utc)
    briefs = cargar_briefs()
    lista = sorted(briefs.values(), key=lambda b: (iso_pub(b), b['mercado']), reverse=True)
    for i, b in enumerate(lista):
        d = os.path.join(ROOT, 'brief', b['id'])
        os.makedirs(d, exist_ok=True)
        prev_b = lista[i + 1] if i + 1 < len(lista) else None
        next_b = lista[i - 1] if i > 0 else None
        with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as fh:
            fh.write(pagina_brief(b, prev_b, next_b))
        png = os.path.join(d, 'og.png')
        if not os.path.exists(png):
            og_png(b, png)
    os.makedirs(os.path.join(ROOT, 'archivo'), exist_ok=True)
    with open(os.path.join(ROOT, 'archivo', 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(pagina_archivo(lista))
    with open(os.path.join(ROOT, 'feed.xml'), 'w', encoding='utf-8') as fh:
        fh.write(feed(lista, ahora))
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as fh:
        fh.write(sitemap(lista, ahora))
    print('páginas', len(lista), file=sys.stderr)


if __name__ == '__main__':
    main()
