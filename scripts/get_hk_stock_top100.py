import requests
import json

def get_hk_stock_top100():
    # Try different API endpoints
    urls = [
        "http://push2.eastmoney.com/api/qt/clist/get",
        "https://push2.eastmoney.com/api/qt/clist/get",
    ]
    params = {
        "pn": "1",
        "pz": "100",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f62",
        "fs": "m:128+t:3,m:128+t:4,m:128+t:1,m:128+t:2",
        "fields": "f12,f14,f2,f3,f4,f5,f6,f62,f8,f15,f16,f17,f18,f9,f10,f23"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://quote.eastmoney.com/",
    }
    for url in urls:
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("data", {}).get("diff", [])
                if items:
                    results = []
                    for item in items:
                        results.append({
                            "code": item.get("f12"),
                            "name": item.get("f14"),
                            "price": item.get("f2"),
                            "change_pct": item.get("f3"),
                            "change_amt": item.get("f4"),
                            "volume": item.get("f5"),
                            "amount": item.get("f62"),
                            "turnover": item.get("f8"),
                            "high": item.get("f15"),
                            "low": item.get("f16"),
                            "open": item.get("f17"),
                            "pre_close": item.get("f18"),
                            "pe": item.get("f9"),
                        })
                    return results
        except:
            continue
    return []

if __name__ == "__main__":
    stocks = get_hk_stock_top100()
    print(json.dumps(stocks, ensure_ascii=False, indent=2))
    print(f"\n=== Total: {len(stocks)} stocks ===")