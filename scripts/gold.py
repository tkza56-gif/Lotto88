#!/usr/bin/env python3
"""ราคาทองสูงสุดรายเดือน → stocks/gold.json (รันทุกวันโดย GitHub Actions)

ทองโลก = ราคาสูงสุดรายวันของ GC=F (USD/ออนซ์) จาก Yahoo Finance
ทองไทย = ทองคำแท่ง 96.5% บาทละ โดยประมาณ = ทองโลก × USD/THB วันเดียวกัน × 0.47295
(ทอง 1 บาท = 15.244 กรัม · 1 ออนซ์ = 31.1035 กรัม · ความบริสุทธิ์ 96.5%)
"""
import json, sys, urllib.request
from datetime import datetime, timezone, timedelta

OUT = 'stocks/gold.json'
K = 15.244 / 31.1035 * 0.965
NY, BKK = timedelta(hours=-5), timedelta(hours=7)   # ใช้แยกวันของตลาด (คลาดเคลื่อนช่วงเปลี่ยนเวลาฤดูร้อนได้เล็กน้อย ไม่กระทบค่าสูงสุดรายเดือน)


def chart(sym):
    req = urllib.request.Request(f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=10y&interval=1d', headers={'User-Agent': 'Mozilla/5.0'})
    j = json.load(urllib.request.urlopen(req, timeout=30))['chart']['result'][0]
    q = j['indicators']['quote'][0]
    return j['timestamp'], q['high'], q['close']


def day(ts, off):
    return (datetime.fromtimestamp(ts, timezone.utc) + off).date().isoformat()


def main():
    gt, gh, _ = chart('GC=F')
    ft, _, fc = chart('THB=X')
    gold = {}
    for t, h in zip(gt, gh):
        if h is not None:
            d = day(t, NY); gold[d] = max(gold.get(d, 0), h)
    fx = {}
    for t, c in zip(ft, fc):
        if c is not None:
            fx[day(t, BKK)] = c
    mon = {}
    for d, h in gold.items():
        m = d[:7]; u, b = mon.get(m, (0, 0))
        mon[m] = (max(u, h), max(b, h * fx[d] * K) if d in fx else b)
    months = sorted(mon)[1:]   # เดือนแรกมีข้อมูลไม่ครบเดือน ตัดทิ้ง
    rows = [[m, round(mon[m][0]), int(round(mon[m][1], -1))] for m in months if mon[m][1]]
    if len(rows) < 100:
        sys.exit(f'ข้อมูลน้อยผิดปกติ ({len(rows)} เดือน) · ไม่เขียนทับไฟล์เดิม')
    out = {'updated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ'), 'last_day': max(gold),
           'source': 'Yahoo Finance GC=F, THB=X · ทองไทยโดยประมาณ = ทองโลก × USD/THB × 0.47295', 'rows': rows}
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    print(f'{len(rows)} เดือน · ล่าสุด {rows[-1]}')


if __name__ == '__main__':
    main()
