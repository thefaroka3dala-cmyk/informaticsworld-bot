import html, os, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
import gate

gate.check("last_news.txt", 4, 9, 21)

token = os.environ["BOT_TOKEN"]
chat = "@informaticsworldar"
q = urllib.parse.quote("ذكاء اصطناعي OR تقنية OR برمجة when:2d")
feeds = [
    ("AITnews", "https://aitnews.com/feed/"),
    ("Google News", f"https://news.google.com/rss/search?q={q}&hl=ar&gl=SA&ceid=SA:ar"),
]
H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
    "Accept-Language": "ar,en;q=0.8",
}

items = []
for name, f in feeds:
    try:
        req = urllib.request.Request(f, headers=H)
        root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
        for it in root.iter("item"):
            title = (it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
            src = (it.findtext("source") or name).strip()
            if title.endswith(" - " + src):
                title = title[: -len(src) - 3]
            if title and link:
                items.append((title, link, src))
        if items:
            break
    except Exception as e:
        print("feed failed:", name, e)

try:
    seen = open("seen.txt", encoding="utf-8").read().split("\n")
except Exception:
    seen = []

fresh = [i for i in items if i[1] not in seen]
if fresh:
    title, link, src = fresh[0]
    text = (f"📰 {html.escape(title)}\n\nالمصدر: {html.escape(src)}\n"
            f'🔗 <a href="{html.escape(link)}">اقرأ الخبر كاملاً</a>\n\n#أخبار_تقنية')
    data = urllib.parse.urlencode(
        {"chat_id": chat, "text": text, "parse_mode": "HTML"}).encode()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    print(urllib.request.urlopen(url, data, timeout=30).read().decode())
    seen += [l for _, l, _ in fresh]
    gate.mark("last_news.txt")
else:
    print("no new items")

open("seen.txt", "w", encoding="utf-8").write("\n".join(seen[-300:]))
