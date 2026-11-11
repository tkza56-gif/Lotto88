#!/usr/bin/env python3
"""บทวิเคราะห์จากสถาบัน → stocks/analyst.json (รันทุกวันโดย GitHub Actions)

แหล่งข้อมูล: Yahoo Finance (รวมคำแนะนำ/ราคาเป้าหมายจากโบรกเกอร์และธนาคาร เช่น Goldman Sachs, Citigroup, Morgan Stanley)
  • ฉันทามติ: จำนวนนักวิเคราะห์ · ราคาเป้าหมายเฉลี่ย/กลาง/สูงสุด/ต่ำสุด · คำแนะนำเฉลี่ย (1 = ซื้อมาก … 5 = ขายมาก)
  • จำนวนแนะนำซื้อ/ถือ/ขาย 4 เดือนล่าสุด (ดูว่าเปลี่ยนไปทางไหน)
  • การปรับคำแนะนำ/ราคาเป้าหมายรายสถาบัน 120 วันล่าสุด
หุ้นที่ไม่มีนักวิเคราะห์ (ETF ฯลฯ) จะไม่อยู่ในไฟล์
"""
import json, sys, time, urllib.request, urllib.error, http.cookiejar
from datetime import datetime, timezone, timedelta

OUT = 'stocks/analyst.json'
REST = 'https://tlykaqoypstvdrlivwvu.supabase.co/rest/v1/'
KEY = 'sb_publishable_IAmYP1QeDb5otH0sjMZaMA_Bme1gxwG'   # คีย์สาธารณะ (อ่านอย่างเดียว) เดียวกับหน้าเว็บ
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

jar = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def get(url, headers=None):
    req = urllib.request.Request(url, headers={'User-Agent': UA, **(headers or {})})
    with op.open(req, timeout=30) as r:
        return r.read().decode()


def crumb():
    try:
        get('https://fc.yahoo.com')          # ตอบ 404 แต่ให้คุกกี้ A3 มา
    except urllib.error.HTTPError:
        pass
    return get('https://query2.finance.yahoo.com/v1/test/getcrumb').strip()


def raw(x):
    return x.get('raw') if isinstance(x, dict) else x


def pick(j):
    fd = j.get('financialData') or {}
    n = raw(fd.get('numberOfAnalystOpinions'))
    trend = [{'p': t.get('period'), 'sb': t.get('strongBuy', 0), 'b': t.get('buy', 0), 'h': t.get('hold', 0), 's': t.get('sell', 0), 'ss': t.get('strongSell', 0)}
             for t in (j.get('recommendationTrend') or {}).get('trend', [])[:4]]
    since = datetime.now(timezone.utc) - timedelta(days=120)
    acts = []
    for h in (j.get('upgradeDowngradeHistory') or {}).get('history', []):
        d = datetime.fromtimestamp(h.get('epochGradeDate', 0), timezone.utc)
        if d < since:
            break
        acts.append({'d': d.date().isoformat(), 'firm': h.get('firm'), 'act': h.get('action'), 'from': h.get('fromGrade') or '', 'to': h.get('toGrade') or '',
                     'pt': h.get('currentPriceTarget') or None, 'ptPrev': h.get('priorPriceTarget') or None, 'ptAct': h.get('priceTargetAction') or ''})
        if len(acts) >= 15:
            break
    if not n and not acts and not any(t['sb'] + t['b'] + t['h'] + t['s'] + t['ss'] for t in trend):
        return None
    return {'n': n, 'mean': raw(fd.get('targetMeanPrice')), 'median': raw(fd.get('targetMedianPrice')), 'hi': raw(fd.get('targetHighPrice')),
            'lo': raw(fd.get('targetLowPrice')), 'rec': fd.get('recommendationKey'), 'recMean': raw(fd.get('recommendationMean')),
            'price': raw(fd.get('currentPrice')), 'trend': trend, 'acts': acts}


def main():
    syms = [r['symbol'] for r in json.loads(get(REST + 'stk_symbols?select=symbol,kind&active=eq.true&order=symbol', {'apikey': KEY})) if r.get('kind') != 'etf']
    c = crumb()
    out, bad = {}, []
    for s in syms:
        try:
            j = json.loads(get(f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{urllib.request.quote(s)}?modules=financialData,recommendationTrend,upgradeDowngradeHistory&crumb={c}'))
            res = (j.get('quoteSummary') or {}).get('result') or []
            v = pick(res[0]) if res else None
            if v:
                out[s] = v
        except Exception as e:   # หุ้นบางตัวไม่มีข้อมูล → ข้าม
            bad.append(f'{s}:{e}')
        time.sleep(0.4)
    if len(out) < len(syms) * 0.3:
        sys.exit(f'ได้ข้อมูลแค่ {len(out)}/{len(syms)} ตัว ผิดปกติ · ไม่เขียนทับไฟล์เดิม · {bad[:5]}')
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump({'updated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ'), 'source': 'Yahoo Finance (รวมจากโบรกเกอร์/ธนาคาร)', 'data': out},
                  f, ensure_ascii=False, separators=(',', ':'))
    print(f'{len(out)}/{len(syms)} ตัวมีบทวิเคราะห์ · ข้าม {len(bad)}')


if __name__ == '__main__':
    main()
