"""Noticias desde la nube (sin navegador), vía Yahoo Finance.
Uso: python3 -I news.py buscar "oil" "mexico peso"   -> titulares recientes con hora y liga
     python3 -I news.py leer URL                      -> texto del artículo"""
import json, sys, re, html, urllib.request, urllib.parse, datetime
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36'}
TZ = datetime.timezone(datetime.timedelta(hours=-6))
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20).read().decode('utf-8', 'ignore')
if len(sys.argv) > 2 and sys.argv[1] == 'buscar':
    seen = set()
    for q in sys.argv[2:]:
        d = json.loads(get('https://query1.finance.yahoo.com/v1/finance/search?newsCount=12&quotesCount=0&q=' + urllib.parse.quote(q)))
        for n in sorted(d.get('news', []), key=lambda n: -n['providerPublishTime']):
            if n['link'] in seen: continue
            seen.add(n['link'])
            t = datetime.datetime.fromtimestamp(n['providerPublishTime'], TZ).strftime('%d %b %H:%M')
            print(f"{t} CDMX | {n['publisher'][:18]} | {n['title']} | {n['link']}")
elif len(sys.argv) > 2 and sys.argv[1] == 'leer':
    s = get(sys.argv[2])
    m = re.search(r'<article.*?</article>', s, re.S) or re.search(r'<body.*?</body>', s, re.S)
    t = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', m.group(0) if m else s, flags=re.S)
    t = re.sub(r'</(p|h\d|li|div)>', '\n', t); t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    print('\n'.join(l.strip() for l in t.split('\n') if len(l.strip()) > 2)[:6000])
else:
    print(__doc__)
