import os, urllib.request, urllib.parse
import xml.etree.ElementTree as ET

token = os.environ["BOT_TOKEN"]
chat = "@informaticsworldar"
feed = "https://aitnews.com/feed/"

req = urllib.request.Request(feed, headers={"User-Agent": "Mozilla/5.0"})
root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
items = []
for it in root.iter("item"):
    title = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    if title and link:
        items.append((title, link))

try:
    seen = open("seen.txt", encoding="utf-8").read().split("\n")
except Exception:
    seen = []

fresh = [i for i in items if i[1] not in seen]
if fresh:
    title, link = fresh[0]
    text = f"📰 {title}\n\nالمصدر: AITnews\n{link}\n\n#أخبار_تقنية"
    data = urllib.parse.urlencode({"chat_id": chat, "text": text}).encode()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    print(urllib.request.urlopen(url, data, timeout=30).read().decode())
    seen += [l for _, l in fresh]

open("seen.txt", "w", encoding="utf-8").write("\n".join(seen[-300:]))
