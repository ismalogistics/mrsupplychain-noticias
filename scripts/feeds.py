"""Genera data/redes.json: lo más reciente de comunidades y medios de supply chain (RSS públicos).

Lo corre la GitHub Action .github/workflows/heatmaps.yml cada hora. Sólo guarda título, fuente,
fecha, un extracto corto y el enlace al original.
"""
import html
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

import feedparser

OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'redes.json')
UA = 'MrSupplyChainNews/1.0 (+https://mrsupplychain.ai/noticias/)'

FEEDS = [
    # (grupo, red, fuente, url)
    ('comunidad', 'reddit', 'r/supplychain', 'https://www.reddit.com/r/supplychain/top/.rss?t=day'),
    ('comunidad', 'reddit', 'r/logistics', 'https://www.reddit.com/r/logistics/top/.rss?t=day'),
    ('comunidad', 'reddit', 'r/procurement', 'https://www.reddit.com/r/procurement/top/.rss?t=week'),
    ('comunidad', 'reddit', 'r/FreightBrokers', 'https://www.reddit.com/r/FreightBrokers/top/.rss?t=day'),
    ('medios', 'medio', 'Supply Chain Dive', 'https://www.supplychaindive.com/feeds/news/'),
    ('medios', 'medio', 'FreightWaves', 'https://www.freightwaves.com/news/feed'),
    ('medios', 'medio', 'The Loadstar', 'https://theloadstar.com/feed/'),
    ('medios', 'medio', 'gCaptain', 'https://gcaptain.com/feed/'),
    ('medios', 'medio', 'Talking Logistics', 'https://talkinglogistics.com/feed/'),
    ('mexico', 'medio', 'T21', 'https://t21.com.mx/feed/'),
]
MAX_POR_FUENTE = 6
# Publicaciones de carrera personal en Reddit (no son noticia de supply chain).
RUIDO = re.compile(r'\b(intern(ship)?s?|resume|cv|salary|career|job offer|new role|this role|interview|hiring me|should i|advice for me|degree|college|university|graduat)', re.I)
MAX_TOTAL = 60
VENTANA = timedelta(days=4)


def limpio(txt, n=220):
    txt = re.sub(r'<[^>]+>', ' ', txt or '')
    txt = html.unescape(re.sub(r'\s+', ' ', txt)).strip()
    txt = re.sub(r'submitted by .*$', '', txt).strip()
    return (txt[: n - 1].rstrip() + '…') if len(txt) > n else txt


def fecha(e):
    for k in ('published_parsed', 'updated_parsed'):
        v = e.get(k)
        if v:
            return datetime(*v[:6], tzinfo=timezone.utc)
    for k in ('published', 'updated'):
        if e.get(k):
            try:
                return parsedate_to_datetime(e[k]).astimezone(timezone.utc)
            except Exception:
                pass
    return None


def main():
    now = datetime.now(timezone.utc)
    items, ok = [], 0
    for grupo, red, fuente, url in FEEDS:
        if red == 'reddit':
            time.sleep(4)  # Reddit limita peticiones seguidas
        try:
            d = feedparser.parse(url, agent=UA)
            entries = d.entries or []
        except Exception as exc:
            print('falló', fuente, exc, file=sys.stderr)
            continue
        if not entries:
            print('sin entradas', fuente, getattr(d, 'status', ''), file=sys.stderr)
            continue
        ok += 1
        n = 0
        for e in entries:
            f = fecha(e)
            if not f or now - f > VENTANA or not e.get('link') or not e.get('title'):
                continue
            if red == 'reddit' and RUIDO.search(e.title):
                continue
            items.append({'grupo': grupo, 'red': red, 'fuente': fuente, 'titulo': limpio(e.title, 180),
                          'resumen': limpio(e.get('summary', '')), 'url': e.link,
                          'fecha': f.strftime('%Y-%m-%dT%H:%M:%SZ')})
            n += 1
            if n >= MAX_POR_FUENTE:
                break
        print(fuente, n, file=sys.stderr)
    if not ok:
        print('Ninguna fuente respondió; se conserva el archivo anterior.', file=sys.stderr)
        return
    items.sort(key=lambda x: x['fecha'], reverse=True)
    out = {'actualizado': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'items': items[:MAX_TOTAL]}
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, separators=(',', ':'))


if __name__ == '__main__':
    main()
