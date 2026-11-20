"""Cotizaciones desde la nube (sin navegador): API de gráficas de Yahoo Finance.
Uso: python3 -I quotes.py [simbolos...]  -> tabla con último, cambio % vs cierre previo y hora (CDMX).
BRENT o BZ=F se traducen al contrato de Brent más próximo (p. ej. BZF27.NYM)."""
import json, sys, urllib.request, datetime, concurrent.futures as cf
DEF = ['^GSPC','^DJI','^IXIC','^RUT','ES=F','NQ=F','YM=F','^VIX','^N225','^KS11','^HSI','000001.SS','^STOXX50E','^GDAXI','^FCHI','^FTSE',
       '^MXX','^BVSP','^GSPTSE','MXN=X','EURUSD=X','JPY=X','KRW=X','BRL=X','CLP=X','COP=X','DX-Y.NYB','CL=F','BRENT','GC=F','SI=F','HG=F','NG=F','^TNX','BTC-USD','ETH-USD']
TZ = datetime.timezone(datetime.timedelta(hours=-6))
def brent_front(d=None):
    """Contrato de Brent más próximo (el que cita Reuters). BZ=F de Yahoo rueda antes del vencimiento.
    El contrato del mes M vence el último día hábil del mes M-2."""
    d = d or datetime.datetime.now(TZ).date()
    nxt = (d.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
    last = nxt - datetime.timedelta(days=1)
    while last.weekday() > 4: last -= datetime.timedelta(days=1)
    k = 2 if d <= last else 3
    y, m = d.year + (d.month - 1 + k) // 12, (d.month - 1 + k) % 12 + 1
    return 'BZ' + 'FGHJKMNQUVXZ'[m - 1] + f'{y % 100:02d}.NYM'
def q(s):
    u = 'https://query1.finance.yahoo.com/v8/finance/chart/' + urllib.parse.quote(s) + '?range=1d&interval=5m'
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=15)
        m = json.load(r)['chart']['result'][0]['meta']
        p, pc = m.get('regularMarketPrice'), m.get('chartPreviousClose') or m.get('previousClose')
        t = datetime.datetime.fromtimestamp(m['regularMarketTime'], TZ)
        if pc and abs(p - pc) < 1e-9:  # mercado cerrado: compara contra el cierre anterior
            d = json.load(urllib.request.urlopen(urllib.request.Request(u.replace('range=1d&interval=5m', 'range=10d&interval=1d'), headers={'User-Agent': 'Mozilla/5.0'}), timeout=15))
            cl = [c for c in d['chart']['result'][0]['indicators']['quote'][0]['close'] if c]
            if len(cl) >= 2: pc = cl[-2]
        return s, p, (p / pc - 1) * 100 if pc else None, t.strftime('%a %d %H:%M'), m.get('marketState', '')
    except Exception as e:
        return s, None, None, str(e)[:40], ''
import urllib.parse
syms = [brent_front() if x.upper() in ('BRENT', 'BZ=F') else x for x in (sys.argv[1:] or DEF)]
with cf.ThreadPoolExecutor(8) as ex:
    for s, p, c, t, st in ex.map(q, syms):
        print(f"{s:11} {'n/d' if p is None else round(p, 4):>12} {'' if c is None else f'{c:+.2f}%':>8}  {t} CDMX")
