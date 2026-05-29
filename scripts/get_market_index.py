import requests
import json

def get_hk_market_index():
    url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
    params = {
        "fltt": "2",
        "invt": "2",
        "fields": "f2,f3,f4,f12,f14,f62,f104,f105",
        "secids": "1.000688,1.000001,0.000688,0.000001,100.HSI,100.HSCEI,100.HSTECH",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://quote.eastmoney.com/",
    }
    resp = requests.get(url, params=params, headers=headers, timeout=15)
    return resp.json()

if __name__ == "__main__":
    result = get_hk_market_index()
    print(json.dumps(result, ensure_ascii=False, indent=2))