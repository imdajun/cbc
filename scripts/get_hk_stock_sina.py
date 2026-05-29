import requests
import json

def get_hk_stock_from_sina():
    url = "https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/RS_MarketStatus.getHKStockRank"
    params = {
        "order": "amount",
        "direction": "desc",
        "num": "100",
        "page": "1"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://vip.stock.finance.sina.com.cn/",
    }
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        data = resp.json()
        results = []
        for item in data:
            name = item.get("name", "")
            code = item.get("code", "")
            price = item.get("price")
            change_pct = item.get("chg_percent")
            change_amt = item.get("chg_amount")
            volume = item.get("volume")
            amount = item.get("amount")
            high = item.get("high")
            low = item.get("low")
            open_p = item.get("open")
            pre_close = item.get("pre_close")
            turnover = item.get("turnover")
            results.append({
                "code": code,
                "name": name,
                "price": price,
                "change_pct": change_pct,
                "change_amt": change_amt,
                "volume": volume,
                "amount": amount,
                "high": high,
                "low": low,
                "open": open_p,
                "pre_close": pre_close,
                "turnover": turnover,
            })
        return results
    except Exception as e:
        return {"error": str(e), "raw": resp.text[:500] if 'resp' in dir() else ""}

if __name__ == "__main__":
    result = get_hk_stock_from_sina()
    if isinstance(result, dict):
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"\n=== Total: {len(result)} stocks ===")