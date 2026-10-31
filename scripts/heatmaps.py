"""Genera data/heatmaps.json: principales acciones de cada índice con su variación del día.

Lo corre la GitHub Action .github/workflows/heatmaps.yml. Fuente: Yahoo Finance (vía yfinance),
datos con retraso de ~15 minutos. Tamaño del mosaico = valor de mercado; color = variación del día.
"""
import json
import math
import os
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import yfinance as yf

# Acciones en circulación aproximadas, sólo para emisoras sin valor de mercado en Yahoo (tamaño del mosaico).
SHARES = {'GFNORTEO.MX': 2.88e9}

OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'heatmaps.json')

# Sectores: tec, com, cons (consumo discrecional), basic (consumo básico), fin, salud, ind, ener, mat, util, inmo
INDICES = [
    {'id': 'sp500', 'es': 'S&P 500', 'en': 'S&P 500', 'mercado': 'global', 'acciones': [
        ('AAPL', 'Apple', 'tec'), ('MSFT', 'Microsoft', 'tec'), ('NVDA', 'Nvidia', 'tec'), ('AVGO', 'Broadcom', 'tec'),
        ('ORCL', 'Oracle', 'tec'), ('AMD', 'AMD', 'tec'), ('CSCO', 'Cisco', 'tec'), ('PLTR', 'Palantir', 'tec'), ('IBM', 'IBM', 'tec'),
        ('CRM', 'Salesforce', 'tec'), ('MU', 'Micron', 'tec'),
        ('GOOGL', 'Alphabet', 'com'), ('META', 'Meta', 'com'), ('NFLX', 'Netflix', 'com'),
        ('AMZN', 'Amazon', 'cons'), ('TSLA', 'Tesla', 'cons'), ('HD', 'Home Depot', 'cons'), ('MCD', "McDonald's", 'cons'),
        ('WMT', 'Walmart', 'basic'), ('COST', 'Costco', 'basic'), ('PG', 'Procter & Gamble', 'basic'), ('KO', 'Coca-Cola', 'basic'), ('PM', 'Philip Morris', 'basic'),
        ('BRK-B', 'Berkshire', 'fin'), ('JPM', 'JPMorgan', 'fin'), ('V', 'Visa', 'fin'), ('MA', 'Mastercard', 'fin'), ('BAC', 'Bank of America', 'fin'),
        ('WFC', 'Wells Fargo', 'fin'), ('GS', 'Goldman Sachs', 'fin'), ('MS', 'Morgan Stanley', 'fin'),
        ('LLY', 'Eli Lilly', 'salud'), ('JNJ', 'Johnson & Johnson', 'salud'), ('ABBV', 'AbbVie', 'salud'), ('UNH', 'UnitedHealth', 'salud'), ('ABT', 'Abbott', 'salud'),
        ('GE', 'GE Aerospace', 'ind'), ('CAT', 'Caterpillar', 'ind'), ('RTX', 'RTX', 'ind'), ('UNP', 'Union Pacific', 'ind'), ('UPS', 'UPS', 'ind'),
        ('XOM', 'Exxon Mobil', 'ener'), ('CVX', 'Chevron', 'ener'), ('LIN', 'Linde', 'mat'), ('NEE', 'NextEra', 'util'),
    ]},
    {'id': 'nasdaq100', 'es': 'Nasdaq 100', 'en': 'Nasdaq 100', 'mercado': 'global', 'acciones': [
        ('AAPL', 'Apple', 'tec'), ('MSFT', 'Microsoft', 'tec'), ('NVDA', 'Nvidia', 'tec'), ('AVGO', 'Broadcom', 'tec'), ('AMD', 'AMD', 'tec'),
        ('PLTR', 'Palantir', 'tec'), ('ASML', 'ASML', 'tec'), ('CSCO', 'Cisco', 'tec'), ('MU', 'Micron', 'tec'), ('QCOM', 'Qualcomm', 'tec'),
        ('TXN', 'Texas Instruments', 'tec'), ('AMAT', 'Applied Materials', 'tec'), ('LRCX', 'Lam Research', 'tec'), ('KLAC', 'KLA', 'tec'),
        ('INTU', 'Intuit', 'tec'), ('ADBE', 'Adobe', 'tec'), ('PANW', 'Palo Alto', 'tec'), ('INTC', 'Intel', 'tec'), ('SHOP', 'Shopify', 'tec'),
        ('GOOGL', 'Alphabet', 'com'), ('META', 'Meta', 'com'), ('NFLX', 'Netflix', 'com'), ('TMUS', 'T-Mobile', 'com'), ('CMCSA', 'Comcast', 'com'),
        ('AMZN', 'Amazon', 'cons'), ('TSLA', 'Tesla', 'cons'), ('BKNG', 'Booking', 'cons'), ('PDD', 'PDD', 'cons'),
        ('COST', 'Costco', 'basic'), ('PEP', 'PepsiCo', 'basic'),
        ('AZN', 'AstraZeneca', 'salud'), ('ISRG', 'Intuitive Surgical', 'salud'), ('AMGN', 'Amgen', 'salud'), ('GILD', 'Gilead', 'salud'),
        ('HON', 'Honeywell', 'ind'), ('ADP', 'ADP', 'ind'), ('LIN', 'Linde', 'mat'),
    ]},
    {'id': 'dow', 'es': 'Dow Jones', 'en': 'Dow Jones', 'mercado': 'global', 'acciones': [
        ('AAPL', 'Apple', 'tec'), ('MSFT', 'Microsoft', 'tec'), ('NVDA', 'Nvidia', 'tec'), ('CSCO', 'Cisco', 'tec'), ('IBM', 'IBM', 'tec'), ('CRM', 'Salesforce', 'tec'),
        ('DIS', 'Disney', 'com'), ('VZ', 'Verizon', 'com'),
        ('AMZN', 'Amazon', 'cons'), ('HD', 'Home Depot', 'cons'), ('MCD', "McDonald's", 'cons'), ('NKE', 'Nike', 'cons'),
        ('WMT', 'Walmart', 'basic'), ('PG', 'Procter & Gamble', 'basic'), ('KO', 'Coca-Cola', 'basic'),
        ('JPM', 'JPMorgan', 'fin'), ('V', 'Visa', 'fin'), ('GS', 'Goldman Sachs', 'fin'), ('AXP', 'American Express', 'fin'), ('TRV', 'Travelers', 'fin'),
        ('UNH', 'UnitedHealth', 'salud'), ('JNJ', 'Johnson & Johnson', 'salud'), ('MRK', 'Merck', 'salud'), ('AMGN', 'Amgen', 'salud'),
        ('CAT', 'Caterpillar', 'ind'), ('BA', 'Boeing', 'ind'), ('HON', 'Honeywell', 'ind'), ('MMM', '3M', 'ind'),
        ('CVX', 'Chevron', 'ener'), ('SHW', 'Sherwin-Williams', 'mat'),
    ]},
    {'id': 'eurostoxx50', 'es': 'Euro Stoxx 50', 'en': 'Euro Stoxx 50', 'mercado': 'global', 'acciones': [
        ('ASML.AS', 'ASML', 'tec'), ('SAP.DE', 'SAP', 'tec'), ('IFX.DE', 'Infineon', 'tec'), ('ADYEN.AS', 'Adyen', 'tec'), ('NOKIA.HE', 'Nokia', 'tec'),
        ('DTE.DE', 'Deutsche Telekom', 'com'), ('PRX.AS', 'Prosus', 'cons'),
        ('MC.PA', 'LVMH', 'cons'), ('RMS.PA', 'Hermès', 'cons'), ('ITX.MC', 'Inditex', 'cons'), ('RACE.MI', 'Ferrari', 'cons'), ('MBG.DE', 'Mercedes-Benz', 'cons'),
        ('BMW.DE', 'BMW', 'cons'), ('EL.PA', 'EssilorLuxottica', 'cons'),
        ('OR.PA', "L'Oréal", 'basic'), ('ABI.BR', 'AB InBev', 'basic'),
        ('ALV.DE', 'Allianz', 'fin'), ('SAN.MC', 'Santander', 'fin'), ('UCG.MI', 'UniCredit', 'fin'), ('ISP.MI', 'Intesa Sanpaolo', 'fin'), ('BNP.PA', 'BNP Paribas', 'fin'),
        ('BBVA.MC', 'BBVA', 'fin'), ('INGA.AS', 'ING', 'fin'), ('MUV2.DE', 'Munich Re', 'fin'), ('CS.PA', 'AXA', 'fin'), ('DB1.DE', 'Deutsche Börse', 'fin'), ('NDA-FI.HE', 'Nordea', 'fin'),
        ('SAN.PA', 'Sanofi', 'salud'),
        ('SIE.DE', 'Siemens', 'ind'), ('AIR.PA', 'Airbus', 'ind'), ('SU.PA', 'Schneider Electric', 'ind'), ('SAF.PA', 'Safran', 'ind'), ('RHM.DE', 'Rheinmetall', 'ind'),
        ('TTE.PA', 'TotalEnergies', 'ener'), ('AI.PA', 'Air Liquide', 'mat'), ('BAS.DE', 'BASF', 'mat'),
        ('IBE.MC', 'Iberdrola', 'util'), ('ENEL.MI', 'Enel', 'util'),
    ]},
    {'id': 'nikkei225', 'es': 'Nikkei 225', 'en': 'Nikkei 225', 'mercado': 'global', 'acciones': [
        ('8035.T', 'Tokyo Electron', 'tec'), ('6857.T', 'Advantest', 'tec'), ('6861.T', 'Keyence', 'tec'), ('6758.T', 'Sony', 'tec'), ('6501.T', 'Hitachi', 'tec'),
        ('6762.T', 'TDK', 'tec'), ('6146.T', 'Disco', 'tec'), ('6981.T', 'Murata', 'tec'), ('6702.T', 'Fujitsu', 'tec'), ('6723.T', 'Renesas', 'tec'),
        ('9984.T', 'SoftBank Group', 'com'), ('9433.T', 'KDDI', 'com'), ('7974.T', 'Nintendo', 'com'), ('9432.T', 'NTT', 'com'),
        ('9983.T', 'Fast Retailing', 'cons'), ('7203.T', 'Toyota', 'cons'), ('7267.T', 'Honda', 'cons'), ('6902.T', 'Denso', 'cons'),
        ('8306.T', 'MUFG', 'fin'), ('8316.T', 'SMFG', 'fin'), ('8411.T', 'Mizuho', 'fin'), ('8766.T', 'Tokio Marine', 'fin'),
        ('4519.T', 'Chugai', 'salud'), ('4568.T', 'Daiichi Sankyo', 'salud'), ('4543.T', 'Terumo', 'salud'), ('7741.T', 'Hoya', 'salud'),
        ('8058.T', 'Mitsubishi Corp.', 'ind'), ('8001.T', 'Itochu', 'ind'), ('8031.T', 'Mitsui & Co.', 'ind'), ('7011.T', 'Mitsubishi Heavy', 'ind'),
        ('6367.T', 'Daikin', 'ind'), ('6954.T', 'Fanuc', 'ind'), ('6098.T', 'Recruit', 'ind'),
        ('4063.T', 'Shin-Etsu', 'mat'),
    ]},
    {'id': 'kospi', 'es': 'KOSPI', 'en': 'KOSPI', 'mercado': 'global', 'acciones': [
        ('005930.KS', 'Samsung Electronics', 'tec'), ('000660.KS', 'SK Hynix', 'tec'), ('066570.KS', 'LG Electronics', 'tec'), ('009150.KS', 'Samsung Electro-Mech.', 'tec'),
        ('035420.KS', 'Naver', 'com'), ('035720.KS', 'Kakao', 'com'), ('017670.KS', 'SK Telecom', 'com'),
        ('005380.KS', 'Hyundai Motor', 'cons'), ('000270.KS', 'Kia', 'cons'), ('012330.KS', 'Hyundai Mobis', 'cons'),
        ('033780.KS', 'KT&G', 'basic'),
        ('105560.KS', 'KB Financial', 'fin'), ('055550.KS', 'Shinhan', 'fin'), ('086790.KS', 'Hana Financial', 'fin'), ('032830.KS', 'Samsung Life', 'fin'),
        ('207940.KS', 'Samsung Biologics', 'salud'), ('068270.KS', 'Celltrion', 'salud'),
        ('012450.KS', 'Hanwha Aerospace', 'ind'), ('329180.KS', 'HD Hyundai Heavy', 'ind'), ('009540.KS', 'HD Korea Shipbuilding', 'ind'), ('042660.KS', 'Hanwha Ocean', 'ind'),
        ('034020.KS', 'Doosan Enerbility', 'ind'), ('028260.KS', 'Samsung C&T', 'ind'), ('064350.KS', 'Hyundai Rotem', 'ind'),
        ('373220.KS', 'LG Energy Solution', 'ind'), ('006400.KS', 'Samsung SDI', 'ind'),
        ('005490.KS', 'POSCO Holdings', 'mat'), ('051910.KS', 'LG Chem', 'mat'), ('010130.KS', 'Korea Zinc', 'mat'),
        ('015760.KS', 'KEPCO', 'util'),
    ]},
    {'id': 'ipc', 'es': 'IPC · BMV', 'en': 'S&P/BMV IPC', 'mercado': 'mexico', 'acciones': [
        ('AMXB.MX', 'América Móvil', 'com'), ('TLEVISACPO.MX', 'Televisa', 'com'),
        ('WALMEX.MX', 'Walmex', 'basic'), ('FEMSAUBD.MX', 'FEMSA', 'basic'), ('AC.MX', 'Arca Continental', 'basic'), ('KOFUBL.MX', 'Coca-Cola FEMSA', 'basic'),
        ('BIMBOA.MX', 'Bimbo', 'basic'), ('GRUMAB.MX', 'Gruma', 'basic'), ('KIMBERA.MX', 'Kimberly-Clark MX', 'basic'), ('CHDRAUIB.MX', 'Chedraui', 'basic'),
        ('CUERVO.MX', 'Becle (Cuervo)', 'basic'),
        ('LIVEPOLC-1.MX', 'Liverpool', 'cons'), ('ALSEA.MX', 'Alsea', 'cons'),
        ('GFNORTEO.MX', 'Banorte', 'fin'), ('GFINBURO.MX', 'Inbursa', 'fin'), ('BBAJIOO.MX', 'BanBajío', 'fin'), ('RA.MX', 'Regional', 'fin'),
        ('Q.MX', 'Quálitas', 'fin'), ('GENTERA.MX', 'Gentera', 'fin'), ('BOLSAA.MX', 'Grupo BMV', 'fin'),
        ('LABB.MX', 'Genomma Lab', 'salud'),
        ('GAPB.MX', 'GAP', 'ind'), ('ASURB.MX', 'ASUR', 'ind'), ('OMAB.MX', 'OMA', 'ind'), ('PINFRA.MX', 'Pinfra', 'ind'), ('GCARSOA1.MX', 'Grupo Carso', 'ind'),
        ('GMEXICOB.MX', 'Grupo México', 'mat'), ('CEMEXCPO.MX', 'Cemex', 'mat'), ('PE&OLES.MX', 'Peñoles', 'mat'), ('ORBIA.MX', 'Orbia', 'mat'), ('GCC.MX', 'GCC', 'mat'),
        ('VESTA.MX', 'Vesta', 'inmo'),
    ]},
]


# Horario de cada bolsa (hora local). Sólo se actualiza un índice mientras su bolsa está abierta
# y durante la hora siguiente al cierre (para dejar el dato de cierre). La BMV opera en el horario de Nueva York.
SESIONES = {
    'sp500': ('America/New_York', (9, 30), (16, 0)),
    'nasdaq100': ('America/New_York', (9, 30), (16, 0)),
    'dow': ('America/New_York', (9, 30), (16, 0)),
    'ipc': ('America/New_York', (9, 30), (16, 0)),
    'eurostoxx50': ('Europe/Berlin', (9, 0), (17, 30)),
    'nikkei225': ('Asia/Tokyo', (9, 0), (15, 30)),
    'kospi': ('Asia/Seoul', (9, 0), (15, 30)),
}
GRACIA = timedelta(minutes=60)

# Bolsas del continente americano para el mapa del día (sólo el índice, sin emisoras).
MAPA = [
    {'id': 'tsx', 'nombre': 'S&P/TSX', 'name_en': 'S&P/TSX', 'ciudad': 'Toronto', 'ciudad_en': 'Toronto', 'lon': -79.38, 'lat': 43.65,
     'tickers': ['^GSPTSE'], 'tz': 'America/Toronto', 'h': ((9, 30), (16, 0))},
    {'id': 'bovespa', 'nombre': 'Ibovespa', 'name_en': 'Ibovespa', 'ciudad': 'São Paulo', 'ciudad_en': 'São Paulo', 'lon': -46.63, 'lat': -23.55,
     'tickers': ['^BVSP'], 'tz': 'America/Sao_Paulo', 'h': ((10, 0), (17, 0))},
    {'id': 'merval', 'nombre': 'S&P Merval', 'name_en': 'S&P Merval', 'ciudad': 'Buenos Aires', 'ciudad_en': 'Buenos Aires', 'lon': -58.38, 'lat': -34.60,
     'tickers': ['^MERV'], 'tz': 'America/Argentina/Buenos_Aires', 'h': ((11, 0), (17, 0))},
    {'id': 'ipsa', 'nombre': 'S&P IPSA', 'name_en': 'S&P IPSA', 'ciudad': 'Santiago', 'ciudad_en': 'Santiago', 'lon': -70.65, 'lat': -33.45,
     'tickers': ['^IPSA', '^SPIPSA'], 'tz': 'America/Santiago', 'h': ((9, 30), (16, 0))},
    {'id': 'colcap', 'nombre': 'MSCI COLCAP', 'name_en': 'MSCI COLCAP', 'ciudad': 'Bogotá', 'ciudad_en': 'Bogotá', 'lon': -74.07, 'lat': 4.71,
     'tickers': ['^COLCAP', 'ICOLCAP.CL'], 'tz': 'America/Bogota', 'h': ((9, 30), (16, 0))},
    {'id': 'bvl', 'nombre': 'S&P/BVL Perú', 'name_en': 'S&P/BVL Peru', 'ciudad': 'Lima', 'ciudad_en': 'Lima', 'lon': -77.04, 'lat': -12.05,
     'tickers': ['^SPBLPGPT'], 'tz': 'America/Lima', 'h': ((9, 0), (16, 0))},
]


def actualizar_mapa(prev_doc, now, force):
    prev = {m['id']: m for m in prev_doc.get('mapa', [])}
    out, cambios = [], 0
    for m in MAPA:
        loc = now.astimezone(ZoneInfo(m['tz']))
        (h1, m1), (h2, m2) = m['h']
        abre = loc.replace(hour=h1, minute=m1, second=0, microsecond=0)
        cierra = loc.replace(hour=h2, minute=m2, second=0, microsecond=0)
        activa = loc.weekday() < 5 and abre <= loc < cierra + GRACIA
        if not (activa or force or m['id'] not in prev):
            if m['id'] in prev:
                out.append(prev[m['id']])
            continue
        rec = None
        for tk in m['tickers']:
            try:
                c = yf.Ticker(tk).history(period='10d', interval='1d', auto_adjust=False)['Close'].dropna()
            except Exception:
                continue
            if len(c) < 2:
                continue
            last, before = float(c.iloc[-1]), float(c.iloc[-2])
            fecha = c.index[-1].strftime('%Y-%m-%d')
            rec = {k: m[k] for k in ('id', 'nombre', 'name_en', 'ciudad', 'ciudad_en', 'lon', 'lat')}
            rec.update({'valor': round(last, 2), 'cambio': round((last / before - 1) * 100, 2), 'fecha': fecha, 'actualizado': iso(now)})
            if fecha == loc.strftime('%Y-%m-%d'):
                rec['abre'], rec['cierra'] = iso(abre), iso(cierra)
            break
        if rec:
            out.append(rec)
            cambios += 1
            print('mapa', m['id'], rec['cambio'], file=sys.stderr)
        elif m['id'] in prev:
            out.append(prev[m['id']])
        else:
            print('mapa sin datos', m['id'], file=sys.stderr)
    return out, cambios


def sesion(idx_id, now):
    tz, (h1, m1), (h2, m2) = SESIONES[idx_id]
    loc = now.astimezone(ZoneInfo(tz))
    abre = loc.replace(hour=h1, minute=m1, second=0, microsecond=0)
    cierra = loc.replace(hour=h2, minute=m2, second=0, microsecond=0)
    activa = loc.weekday() < 5 and abre <= loc < cierra + GRACIA
    return activa, loc.strftime('%Y-%m-%d'), abre, cierra


def iso(d):
    return d.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def load_prev():
    try:
        with open(OUT, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def main():
    now = datetime.now(timezone.utc)
    force = os.environ.get('FORZAR') == '1'
    prev_doc = load_prev()
    prev_idx = {i['id']: i for i in prev_doc.get('indices', [])}
    prev = {(i['id'], a['t']): a for i in prev_doc.get('indices', []) for a in i.get('acciones', [])}
    vivos = {}
    for idx in INDICES:
        activa, hoy, abre, cierra = sesion(idx['id'], now)
        if activa or force or idx['id'] not in prev_idx:
            vivos[idx['id']] = (hoy, abre, cierra, activa)
    mapa, cambios_mapa = actualizar_mapa(prev_doc, now, force)
    if not vivos:
        if cambios_mapa:
            prev_doc['mapa'] = mapa
            prev_doc['actualizado'] = iso(now)
            with open(OUT, 'w', encoding='utf-8') as f:
                json.dump(prev_doc, f, ensure_ascii=False, separators=(',', ':'))
        else:
            print('Ninguna bolsa abierta; no hay nada que actualizar.', file=sys.stderr)
        return
    tickers = sorted({a[0] for idx in INDICES if idx['id'] in vivos for a in idx['acciones']})
    hist = yf.download(tickers, period='10d', interval='1d', group_by='ticker', auto_adjust=False, threads=True, progress=False)

    quotes = {}
    for t in tickers:
        try:
            closes = hist[t]['Close'].dropna()
        except Exception:
            continue
        if len(closes) < 2:
            continue
        last, before = float(closes.iloc[-1]), float(closes.iloc[-2])
        if not before or math.isnan(last) or math.isnan(before):
            continue
        quotes[t] = {'p': round(last, 2), 'chg': round((last / before - 1) * 100, 2), 'fecha': closes.index[-1].strftime('%Y-%m-%d')}

    def ok(v):
        try:
            return v is not None and not math.isnan(float(v)) and float(v) > 0
        except Exception:
            return False

    caps = {}
    for t in quotes:
        tk = yf.Ticker(t)
        mc = None
        try:
            mc = tk.fast_info['market_cap']
        except Exception:
            pass
        if not ok(mc):
            try:
                mc = tk.info.get('marketCap')
            except Exception:
                mc = None
        if not ok(mc):
            try:
                mc = float(tk.fast_info['shares']) * quotes[t]['p']
            except Exception:
                mc = None
        if not ok(mc) and t in SHARES:
            mc = SHARES[t] * quotes[t]['p']
        if ok(mc):
            caps[t] = float(mc)
        else:
            print('sin valor de mercado:', t, file=sys.stderr)

    out = {'actualizado': iso(now), 'fuente': 'Yahoo Finance', 'indices': [], 'mapa': mapa}
    cambios = 0
    for idx in INDICES:
        if idx['id'] not in vivos:
            if idx['id'] in prev_idx:
                out['indices'].append(prev_idx[idx['id']])
            continue
        hoy, abre, cierra, activa = vivos[idx['id']]
        rows, fechas = [], []
        for t, n, s in idx['acciones']:
            q = quotes.get(t)
            if not q:
                continue
            cap = caps.get(t) or (prev.get((idx['id'], t.split('.')[0])) or {}).get('cap')
            if cap and t in caps:
                cap = round(cap / 1e6)
            if not cap:
                continue
            rows.append({'t': t.split('.')[0], 'n': n, 's': s, 'cap': cap, 'p': q['p'], 'chg': q['chg']})
            fechas.append(q['fecha'])
        fecha = max(fechas) if fechas else None
        # Feriado o sin datos del día: se conserva lo anterior.
        if not rows or (activa and not force and fecha != hoy and idx['id'] in prev_idx):
            print(idx['id'], 'sin sesión hoy; se conserva el dato anterior', file=sys.stderr)
            if idx['id'] in prev_idx:
                out['indices'].append(prev_idx[idx['id']])
            continue
        tz = SESIONES[idx['id']][0]
        rec = {'id': idx['id'], 'es': idx['es'], 'en': idx['en'], 'mercado': idx['mercado'], 'fecha': fecha,
               'actualizado': iso(now), 'acciones': rows}
        if fecha == hoy:
            rec['abre'], rec['cierra'] = iso(abre), iso(cierra)
        out['indices'].append(rec)
        cambios += 1
        print(idx['id'], len(rows), 'de', len(idx['acciones']), file=sys.stderr)

    if not cambios and not cambios_mapa:
        print('Sin cambios que escribir.', file=sys.stderr)
        return
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))

if __name__ == '__main__':
    main()
