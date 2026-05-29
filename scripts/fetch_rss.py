import requests
import json

NEWS_URL = "https://huginn.miniflux91.xyz/users/1/web_requests"

SOURCES = {
    "baofa": f"{NEWS_URL}/491/a-secret-key.xml",
    "mingtian": f"{NEWS_URL}/518/a-secret-key.xml",
    "cls": f"{NEWS_URL}/203/a-secret-key.xml",
    "futu": f"{NEWS_URL}/382/a-secret-key.xml",
    "gelonghui": f"{NEWS_URL}/416/a-secret-key.xml",
    "investinglive": "https://investinglive.com/feed",
    "wallstreetcn": "https://feed.wallstreetcn.com/wallstreetcn/news/global",
}

def fetch_source(name, url):
    try:
        resp = requests.get(url, timeout=10)
        resp.encoding = 'utf-8'
        return resp.text
    except Exception as e:
        return None

def extract_items(xml_text):
    import re
    items = re.findall(r'<item>(.*?)</item>', xml_text, re.DOTALL)
    entries = []
    for item in items:
        title_m = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
        desc_m = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', item)
        pub_m = re.search(r'<pubDate>(.*?)</pubDate>', item)
        link_m = re.search(r'<link>(.*?)</link>', item)
        if not title_m:
            title_m = re.search(r'<title>(.*?)</title>', item)
        if not desc_m:
            desc_m = re.search(r'<description>(.*?)</description>', item)
        title = title_m.group(1) if title_m else ""
        desc = desc_m.group(1) if desc_m else ""
        pub = pub_m.group(1) if pub_m else ""
        link = link_m.group(1) if link_m else ""
        entries.append({"title": title, "description": desc, "pubdate": pub, "link": link})
    return entries

if __name__ == "__main__":
    import sys
    selected = sys.argv[1:] if len(sys.argv) > 1 else ["cls", "futu", "gelonghui", "wallstreetcn"]
    for src in selected:
        if src in SOURCES:
            xml = fetch_source(src, SOURCES[src])
            if xml:
                items = extract_items(xml)
                print(f"\n=== {src} ({len(items)} items) ===")
                for it in items[:15]:
                    print(json.dumps(it, ensure_ascii=False))
            else:
                print(f"\n=== {src} FAILED ===")