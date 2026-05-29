import requests, json

def get_hk_stock_top100():
    params = {
        "pn": "1", "pz": "100", "po": "1", "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281", "fltt": "2", "invt": "2",
        "fid": "f62",
        "fs": "m:128+t:3,m:128+t:4,m:128+t:1,m:128+t:2",
        "fields": "f12,f14,f2,f3,f4,f5,f6,f62,f8,f15,f16,f17,f18,f9,f10,f23"
    }
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://quote.eastmoney.com/"}
    resp = requests.get("https://push2.eastmoney.com/api/qt/clist/get", params=params, headers=headers, timeout=15)
    data = resp.json()
    items = data.get("data", {}).get("diff", [])
    results = []
    for item in items:
        results.append({
            "code": item.get("f12"), "name": item.get("f14"),
            "price": item.get("f2"), "change_pct": item.get("f3"),
            "amount": item.get("f62"), "volume": item.get("f5"),
            "turnover": item.get("f8"),
            "high": item.get("f15"), "low": item.get("f16"),
            "pe": item.get("f9"),
        })
    return results

stocks = get_hk_stock_top100()

# Top 20 by amount
print("=== TOP 20 BY AMOUNT ===")
for i, s in enumerate(stocks[:20], 1):
    chg = s['change_pct']
    chg_str = f"+{chg}%" if chg and chg > 0 else f"{chg}%"
    amount_hk = s['amount'] / 100000000 if s['amount'] else 0
    print(f"{i}. {s['name']}({s['code']})  ${s['price']}  {chg_str}  成交额: {amount_hk:.2f}亿")

# Count gainers/losers
up = sum(1 for s in stocks if s['change_pct'] and s['change_pct'] > 0)
down = sum(1 for s in stocks if s['change_pct'] and s['change_pct'] < 0)
flat = sum(1 for s in stocks if s['change_pct'] and s['change_pct'] == 0)
print(f"\n=== 涨跌分布 ===")
print(f"上涨: {up} | 下跌: {down} | 平盘: {flat}")

# Biggest gainers
sorted_stocks = sorted(stocks, key=lambda x: x['change_pct'] or 0, reverse=True)
print(f"\n=== TOP 5 涨幅 ===")
for s in sorted_stocks[:5]:
    print(f"{s['name']}({s['code']})  {s['change_pct']:+.2f}%  ${s['price']}")

# Biggest losers
print(f"\n=== TOP 5 跌幅 ===")
for s in sorted_stocks[-5:]:
    print(f"{s['name']}({s['code']})  {s['change_pct']:+.2f}%  ${s['price']}")

# Sector grouping
sectors = {}
for s in stocks:
    name = s['name'] or ""
    amount = s['amount'] or 0
    if any(x in name for x in ['银行', '中国银行', '工商', '建设', '农业', '交通', '招商银行', '中银']):
        sec = '银行'
    elif any(x in name for x in ['腾讯', '阿里', '百度', '美团', '京东', '网易', '快手', '哔哩', '携程', '贝壳']):
        sec = '科网'
    elif any(x in name for x in ['平安', '人寿', '保险', '新华', '中国太保']):
        sec = '保险'
    elif any(x in name for x in ['电力', '华电', '龙源', '中广核', '中国电力']):
        sec = '电力'
    elif any(x in name for x in ['生物', '医药', '药明', '信达', '百济', '康方', '三生', '再鼎', '来凯', '恒瑞']):
        sec = '医药'
    elif any(x in name for x in ['地产', '新鸿基', '碧桂园', '融创', '万科', '华润']):
        sec = '地产'
    elif any(x in name for x in ['石油', '中海油', '中石油', '中石化']):
        sec = '能源'
    elif any(x in name for x in ['神华', '兖矿', '中国铝业', '中煤']):
        sec = '资源'
    elif any(x in name for x in ['汽车', '比亚迪', '理想', '小鹏', '吉利']):
        sec = '汽车'
    elif any(x in name for x in ['芯片', '中芯', '华虹', '澜起', '兆易', '半导体']):
        sec = '半导体'
    elif any(x in name for x in ['消费', '泡泡玛特', '农夫山泉', '安踏', '李宁', '茅台', '五粮液', '中免', '华润啤酒', '鸣鸣']):
        sec = '消费'
    elif any(x in name for x in ['中信证券', '中国银河', '国泰君安', '中信']):
        sec = '券商'
    elif any(x in name for x in ['联想', '小米', '瑞声', '创科']):
        sec = '科技硬件'
    else:
        sec = '其他'
    sectors[sec] = sectors.get(sec, 0) + (amount or 0)

print(f"\n=== 板块成交额分布（亿港元） ===")
for sec, amt in sorted(sectors.items(), key=lambda x: -x[1]):
    print(f"{sec}: {amt/100000000:.2f}亿")