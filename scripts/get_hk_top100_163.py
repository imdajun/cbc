import requests
import json
import re

def get_hk_top100():
    url = "http://quotes.money.163.com/service/rankhot.html"
    params = {
        "type": "hk",
        "sort": "amount",
        "order": "desc",
        "page": "0",
        "size": "100"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    resp = requests.get(url, params=params, headers=headers, timeout=15)
    data = resp.json()
    return data.get("list", [])

if __name__ == "__main__":
    stocks = get_hk_top100()
    print(json.dumps(stocks, ensure_ascii=False, indent=2))
    print(f"\n=== Total: {len(stocks)} stocks ===")