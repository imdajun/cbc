#!/usr/bin/env python3
"""Query all 7 stocks for dynamic PE and comprehensive data"""
import requests, json, sys

API_URL = "https://mkapi2.dfcfs.com/finskillshub/api/claw/query"
API_KEYS = [
    "mkt_tEMdTR-CXRD8C5UOKUWohzOtGMD2-Ad1jE_FhDFw_1w",
    "mkt_CPBQvGj2i8Oy9M6oPkG_Ybs8hwRAfH6iqBBUwrOIuEM",
    "mkt_taDEmLXdQI6rtQTd5klrWvgdFkLgGCQ6O-9D823SAIY",
    "mkt_4z-RsvQ15HqCebWX9_J9s2C3MbIYvXts4if49nW5xVk"
]

def query(payload):
    for key in API_KEYS:
        headers = {"Content-Type": "application/json; charset=gbk", "apikey": key}
        try:
            resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            data = resp.json()
            if data.get("success"):
                return data
        except:
            continue
    return None

queries = [
    # Each stock with dynamic PE + key data
    {"toolQuery": "华电辽能(SH600396) 动态市盈率,最新价,涨跌幅,换手率,总市值,流通市值,成交量,成交额,市净率,每股收益"},
    {"toolQuery": "大唐发电(SH601991) 动态市盈率,最新价,涨跌幅,换手率,总市值,流通市值,成交量,成交额,市净率,每股收益"},
    {"toolQuery": "华电能源(SH600726) 动态市盈率,最新价,涨跌幅,换手率,总市值,流通市值,成交量,成交额,市净率,每股收益"},
    {"toolQuery": "京能电力(SH600578) 动态市盈率,最新价,涨跌幅,换手率,总市值,流通市值,成交量,成交额,市净率,每股收益"},
    {"toolQuery": "华银电力(SH600744) 动态市盈率,最新价,涨跌幅,换手率,总市值,流通市值,成交量,成交额,市净率,每股收益"},
    {"toolQuery": "华能蒙电(SH600863) 动态市盈率,最新价,涨跌幅,换手率,总市值,流通市值,成交量,成交额,市净率,每股收益"},
    {"toolQuery": "粤电力A(SZ000539) 动态市盈率,最新价,涨跌幅,换手率,总市值,流通市值,成交量,成交额,市净率,每股收益"},
]

for q in queries:
    result = query(q)
    if result is None:
        print(f"\n=== {q['toolQuery'][:10]}... === FAILED")
        continue
    tables = result.get("data",{}).get("data",{}).get("searchDataResultDTO",{}).get("dataTableDTOList",[])
    for t in tables:
        name = t.get("entityName","")
        if "HK" in name or "B股" in name:
            continue
        table = t.get("table",{})
        nmap = t.get("nameMap",{})
        head = table.get("headName",[])
        print(f"\n=== {name} ===")
        for code, vals in table.items():
            if code == "headName":
                continue
            fname = nmap.get(code, code)
            print(f"  {fname}: {vals[0] if vals else 'N/A'}")