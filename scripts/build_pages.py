"""Genera las páginas estáticas del portal para buscadores y redes sociales.

- b/<id>.html      una página por brief (texto completo, metadatos, JSON-LD NewsArticle)
- og/<id>.png      imagen para compartir (1200x630) de cada brief; og/portada.png para la portada
- archivo.html     archivo completo de briefs
- rss.xml          feed RSS
- sitemap.xml      sitemap del portal (con etiquetas de Google News para lo reciente)

Lo corre la GitHub Action .github/workflows/pages.yml cada vez que cambian los datos.
"""
import html
import json
import os
import textwrap
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

ROOT = os.path.join(os.path.dirname(__file__), '..')
BASE = 'https://mrsupplychain.ai/noticias/'
BRAND = 'Mr. Supply Chain® México'
MES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
MES_C = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
MOM = {'apertura': 'Apertura', 'mediodia': 'Mediodía', 'cierre': 'Cierre'}
MOM_EN = {'apertura': 'Open', 'mediodia': 'Midday', 'cierre': 'Close'}
MKT = {'global': 'Global', 'latam': 'LATAM', 'mexico': 'México'}
MKT_EN = {'global': 'Global', 'latam': 'LATAM', 'mexico': 'Mexico'}
HORA_UTC = {'apertura': 14, 'mediodia': 17, 'cierre': 21}

e = html.escape


def load(path, default=None):
    try:
        with open(os.path.join(ROOT, path), encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(text)


def fecha_larga(iso):
    y, m, d = iso[:10].split('-')
    return f'{int(d)} de {MES[int(m) - 1]} de {y}'


def fecha_corta(iso):
    y, m, d = iso[:10].split('-')
    return f'{int(d)} {MES_C[int(m) - 1]} {y}'


def momento_dt(b):
    """Fecha y hora aproximada de publicación en UTC."""
    y, m, d = (int(x) for x in b['fecha'][:10].split('-'))
    hora = b.get('hora', '')
    try:
        hh, mm = (int(x) for x in hora.split()[0].split(':'))
        return datetime(y, m, d, hh, mm, tzinfo=timezone(timedelta(hours=-6))).astimezone(timezone.utc)
    except Exception:
        return datetime(y, m, d, HORA_UTC.get(b.get('momento'), 18), 0, tzinfo=timezone.utc)


# ---------- Imagen para compartir ----------
def fuente(bold=True, serif=False, size=40):
    from PIL import ImageFont
    nombres = []
    if serif:
        nombres += ['DejaVuSerif-Bold.ttf' if bold else 'DejaVuSerif.ttf']
    nombres += ['DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf']
    for carpeta in ('/usr/share/fonts/truetype/dejavu/', '/usr/share/fonts/dejavu/', ''):
        for n in nombres:
            try:
                return ImageFont.truetype(carpeta + n, size)
            except Exception:
                continue
    return ImageFont.load_default()


def og_image(path, kicker, titular, pie):
    try:
        from PIL import Image, ImageDraw
    except Exception:
        return False
    W, H = 1200, 630
    img = Image.new('RGB', (W, H), (250, 249, 246))
    dr = ImageDraw.Draw(img)
    dr.rectangle([0, 0, W, 14], fill=(30, 79, 156))
    dr.text((64, 52), 'Mr. Supply Chain® México', font=fuente(True, True, 40), fill=(21, 23, 27))
    tag = 'NOTICIAS'
    ft = fuente(True, False, 22)
    tw = dr.textlength(tag, font=ft)
    x0 = 64 + dr.textlength('Mr. Supply Chain® México', font=fuente(True, True, 40)) + 18
    dr.rounded_rectangle([x0, 58, x0 + tw + 24, 94], radius=4, fill=(30, 79, 156))
    dr.text((x0 + 12, 63), tag, font=ft, fill=(255, 255, 255))
    dr.text((64, 140), kicker.upper(), font=fuente(True, False, 24), fill=(30, 79, 156))
    size = 60
    while size >= 36:
        f = fuente(True, True, size)
        ancho = max(10, int(1070 / (size * 0.55)))
        lineas = textwrap.wrap(titular, width=ancho)
        if len(lineas) * size * 1.18 <= 330:
            break
        size -= 4
    y = 190
    for ln in lineas[:6]:
        dr.text((64, y), ln, font=f, fill=(21, 23, 27))
        y += int(size * 1.18)
    dr.line([64, 548, W - 64, 548], fill=(227, 224, 216), width=2)
    dr.text((64, 566), pie, font=fuente(False, False, 24), fill=(106, 111, 119))
    dr.text((W - 64 - dr.textlength('mrsupplychain.ai/noticias', font=fuente(True, False, 24)), 566), 'mrsupplychain.ai/noticias', font=fuente(True, False, 24), fill=(30, 79, 156))
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    img.save(full, 'PNG', optimize=True)
    return True


# ---------- Páginas ----------
CSS = """
:root{--paper:#faf9f6;--ink:#15171b;--muted:#6a6f77;--line:#e3e0d8;--accent:#1e4f9c;--serif:"Iowan Old Style","Palatino Linotype","Book Antiqua",Palatino,Georgia,serif;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,Roboto,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);line-height:1.6}
.w{max-width:760px;margin:0 auto;padding:0 20px}
header{border-bottom:1px solid var(--line);background:#fff}header .w{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 20px;flex-wrap:wrap}
.brand{font-family:var(--serif);font-weight:600;font-size:1.35rem;color:var(--ink);text-decoration:none}.brand span{font-size:.6em;font-family:var(--sans);font-weight:800;letter-spacing:.14em;color:#fff;background:var(--accent);padding:3px 7px;border-radius:3px;margin-left:8px;vertical-align:3px}
nav a{color:var(--accent);text-decoration:none;font-size:14px;font-weight:600;margin-left:14px}
.k{margin:32px 0 8px;font-size:12px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
h1{font-family:var(--serif);font-size:clamp(1.8rem,4.6vw,2.7rem);line-height:1.15;margin:0 0 12px;letter-spacing:-.01em}
.by{font-size:13px;color:var(--muted);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:8px 0;margin-bottom:24px}
h2{font-size:12px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;margin:26px 0 6px}
p{font-family:var(--serif);font-size:1.12rem;margin:0 0 14px}
.scm{background:#eef3fb;border-left:4px solid var(--accent);padding:14px 18px;margin:26px 0;border-radius:0 6px 6px 0}.scm h2{margin-top:0;color:var(--accent)}
.src{font-size:13px;color:var(--muted)}.src a{color:var(--accent)}
details{margin:30px 0;border-top:1px solid var(--line);padding-top:14px}summary{cursor:pointer;font-weight:700;color:var(--accent)}
.cta{display:inline-block;margin:10px 0 40px;background:var(--ink);color:#fff;text-decoration:none;padding:10px 16px;border-radius:4px;font-weight:700;font-size:14px}
ul.list{list-style:none;padding:0;margin:0 0 40px}ul.list li{border-bottom:1px solid var(--line);padding:12px 0}ul.list a{font-family:var(--serif);font-size:1.12rem;color:var(--ink);text-decoration:none;font-weight:600}ul.list a:hover{color:var(--accent)}ul.list small{display:block;color:var(--muted);font-size:12.5px}
footer{border-top:1px solid var(--line);font-size:12.5px;color:var(--muted);padding:20px 0 40px}
"""


def page(title, desc, url, img, body, extra_head=''):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<link rel="alternate" type="application/rss+xml" title="Noticias · {BRAND}" href="{BASE}rss.xml">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="es_MX">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@MrSupplyChainX">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{img}">
<style>{CSS}</style>
{extra_head}
</head>
<body>
<header><div class="w"><a class="brand" href="{BASE}">{BRAND}<span>NOTICIAS</span></a><nav><a href="{BASE}">Portada</a><a href="{BASE}archivo.html">Archivo</a><a href="/">mrsupplychain.ai</a></nav></div></header>
<main class="w">
{body}
</main>
<footer><div class="w">{BRAND} · Noticias. Contenido informativo elaborado con apoyo de IA a partir de las fuentes públicas citadas. No es recomendación de inversión.</div></footer>
</body>
</html>
"""


def brief_page(b):
    es, en = b.get('es', {}), b.get('en', {})
    url = f"{BASE}b/{b['id']}.html"
    img = f"{BASE}og/{b['id']}.png"
    kicker = f"{MOM.get(b['momento'], b['momento'])} · {MKT.get(b['mercado'], b['mercado'])}" + (' · Edición de fin de semana' if b.get('fin_de_semana') else '')
    titulo = es.get('titular', '')
    resumen = (es.get('bloques') or [{}])[0].get('x', '')
    desc = (resumen[:155].rsplit(' ', 1)[0] + '…') if len(resumen) > 160 else resumen
    pub = momento_dt(b)
    bloques = ''.join(f"<h2>{e(x.get('t', ''))}</h2><p>{e(x.get('x', ''))}</p>" for x in es.get('bloques', []))
    scm = f"<aside class=\"scm\"><h2>{'Para el fin de semana' if b.get('fin_de_semana') else 'Para supply chain'}</h2><p>{e(es.get('scm', ''))}</p></aside>" if es.get('scm') else ''
    fuentes = ' · '.join(f"<a href=\"{e(f['u'])}\" rel=\"nofollow noopener\" target=\"_blank\">{e(f['t'])}</a>" for f in b.get('fuentes', []))
    en_html = ''
    if en.get('titular'):
        en_html = '<details lang="en"><summary>Read in English</summary>' + f"<h2>{e(en['titular'])}</h2>" + ''.join(
            f"<h2>{e(x.get('t', ''))}</h2><p>{e(x.get('x', ''))}</p>" for x in en.get('bloques', [])) + (
            f"<aside class=\"scm\"><h2>For supply chain</h2><p>{e(en.get('scm', ''))}</p></aside>" if en.get('scm') else '') + '</details>'
    ld = {
        '@context': 'https://schema.org', '@type': 'NewsArticle', 'headline': titulo[:110], 'description': desc,
        'image': [img], 'datePublished': pub.strftime('%Y-%m-%dT%H:%M:%SZ'), 'dateModified': pub.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'inLanguage': 'es-MX', 'mainEntityOfPage': url,
        'author': {'@type': 'Organization', 'name': BRAND, 'url': 'https://mrsupplychain.ai/'},
        'publisher': {'@type': 'Organization', 'name': BRAND, 'url': 'https://mrsupplychain.ai/'},
        'about': ['Supply chain', 'Mercados financieros', 'Economía'],
    }
    body = (f"<p class=\"k\">{e(kicker)}</p><h1>{e(titulo)}</h1>"
            f"<div class=\"by\"><b>Mesa de mercados {BRAND}</b> · {fecha_larga(b['fecha'])} · {e(b.get('hora', ''))}</div>"
            f"{bloques}{scm}<p class=\"src\">Fuentes: {fuentes}</p>{en_html}"
            f"<a class=\"cta\" href=\"{BASE}\">Ver mercados, gráficos y mapa del día →</a>")
    head = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    write(f"b/{b['id']}.html", page(f"{titulo} | Noticias {BRAND}", desc, url, img, body, head))
    pie = f"{MKT.get(b['mercado'], '')} · {fecha_corta(b['fecha'])} · {b.get('hora', '')}"
    og_image(f"og/{b['id']}.png", kicker, titulo, pie)
    return {'id': b['id'], 'url': url, 'titulo': titulo, 'desc': desc, 'pub': pub, 'mercado': b['mercado'], 'momento': b['momento'], 'fecha': b['fecha']}


def main():
    idx = load('data/index.json', {'items': []}).get('items', [])
    latest = load('data/latest.json', {}) or {}
    paginas = []
    vistos = set()
    for it in idx:
        if it['id'] in vistos:
            continue
        vistos.add(it['id'])
        b = load(f"data/briefs/{it['id']}.json")
        if b:
            paginas.append(brief_page(b))
    paginas.sort(key=lambda p: p['pub'], reverse=True)

    # Archivo
    filas, dia = [], None
    for p in paginas:
        if p['fecha'] != dia:
            dia = p['fecha']
            filas.append(f"</ul><h2>{fecha_larga(dia)}</h2><ul class=\"list\">")
        filas.append(f"<li><a href=\"b/{p['id']}.html\">{e(p['titulo'])}</a><small>{MOM.get(p['momento'], '')} · {MKT.get(p['mercado'], '')}</small></li>")
    cuerpo = '<p class="k">Archivo</p><h1>Todos los briefs de mercados para supply chain</h1><ul class="list">' + ''.join(filas) + '</ul>'
    write('archivo.html', page(f'Archivo de briefs | Noticias {BRAND}', 'Archivo de los briefs diarios de mercados y economía para supply chain: apertura, mediodía y cierre, Global, LATAM y México.', f'{BASE}archivo.html', f'{BASE}og/portada.png', cuerpo))

    # Imagen de portada (brief global más reciente)
    g = (latest.get('briefs') or {}).get('global')
    if g:
        og_image('og/portada.png', f"{MOM.get(g['momento'], '')} · Global · LATAM · México", g['es']['titular'], f"Brief de mercados para supply chain · {fecha_corta(g['fecha'])}")

    # RSS
    now = datetime.now(timezone.utc)
    items = ''.join(f"""
  <item>
    <title>{e(p['titulo'])}</title>
    <link>{p['url']}</link>
    <guid isPermaLink="true">{p['url']}</guid>
    <pubDate>{format_datetime(p['pub'])}</pubDate>
    <category>{MKT.get(p['mercado'], '')}</category>
    <description>{e(p['desc'])}</description>
    <enclosure url="{BASE}og/{p['id']}.png" type="image/png" length="0"/>
  </item>""" for p in paginas[:50])
    write('rss.xml', f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Noticias · {BRAND}</title>
  <link>{BASE}</link>
  <atom:link href="{BASE}rss.xml" rel="self" type="application/rss+xml"/>
  <description>Brief diario de mercados y economía para supply chain y operaciones: Global, LATAM y México.</description>
  <language>es-mx</language>
  <lastBuildDate>{format_datetime(now)}</lastBuildDate>{items}
</channel>
</rss>
""")

    # Sitemap (Google News sólo acepta notas de los últimos 2 días)
    urls = [f"  <url><loc>{BASE}</loc><lastmod>{now.strftime('%Y-%m-%d')}</lastmod><changefreq>hourly</changefreq><priority>1.0</priority></url>",
            f"  <url><loc>{BASE}archivo.html</loc><lastmod>{now.strftime('%Y-%m-%d')}</lastmod><changefreq>daily</changefreq></url>"]
    for p in paginas:
        news = ''
        if now - p['pub'] < timedelta(days=2):
            news = (f"<news:news><news:publication><news:name>{e(BRAND)}</news:name><news:language>es</news:language></news:publication>"
                    f"<news:publication_date>{p['pub'].strftime('%Y-%m-%dT%H:%M:%SZ')}</news:publication_date><news:title>{e(p['titulo'])}</news:title></news:news>")
        urls.append(f"  <url><loc>{p['url']}</loc><lastmod>{p['pub'].strftime('%Y-%m-%d')}</lastmod>{news}</url>")
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">\n' + '\n'.join(urls) + '\n</urlset>\n')
    print(len(paginas), 'páginas')


if __name__ == '__main__':
    main()
