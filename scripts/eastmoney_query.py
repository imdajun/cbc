import requests
import json
import os
import gzip
import io

API_BASE = "https://mkapi2.dfcfs.com/finskillshub/api/claw"

API_KEYS = [
    "mkt_CPBQvGj2i8Oy9M6oPkG_Ybs8hwRAfH6iqBPUwrOIuEM",
    "mkt_taDEmLXdQI6rtQTd5klrWvgdFkLgGCQ6O-9D823SAIY",
    "mkt_4z-RsvQ15HqCebWX9_J9s2C3MbIYvXts4if49nW5xVk",
    "mkt_tEMdTR-CXRD8C5UOKUWohzOtGMD2-Ad1jE_FhDFw_1w",
]

def eastmoney_query(endpoint, payload):
    url = f"{API_BASE}/{endpoint}"
    for key in API_KEYS:
        try:
            resp = requests.post(
                url,
                headers={
                    "Content-Type": "application/json; charset=gbk",
                    "apikey": key,
                },
                data=json.dumps(payload).encode("gbk", errors="replace"),
                timeout=15,
            )
            try:
                return resp.json()
            except:
                try:
                    raw = resp.content
                    if raw[:2] == b'\x1f\x8b':
                        raw = gzip.decompress(raw)
                    return json.loads(raw.decode("utf-8"))
                except:
                    return {"raw": resp.text}
        except Exception as e:
            continue
    return {"error": "all keys failed"}

if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "query"
    if mode == "query":
        # Query HK market data
        result = eastmoney_query("query", {"toolQuery": "恒生指数 最新行情 港股 成交额"})
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif mode == "news":
        result = eastmoney_query("news-search", {"query": "港股", "limit": 10})
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif mode == "screen":
        query = sys.argv[2] if len(sys.argv) > 2 else "港股 成交额前10 今日"
        result = eastmoney_query("stock-screen", {"keyword": query, "pageSize": 20})
        print(json.dumps(result, ensure_ascii=False, indent=2))