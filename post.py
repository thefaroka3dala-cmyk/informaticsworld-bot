
import os, urllib.request, urllib.parse

token = os.environ["BOT_TOKEN"]
chat = "@informaticsworldar"

text = open("posts.txt", encoding="utf-8").read().replace("\r\n", "\n")
posts = [p.strip() for p in text.split("\n---\n") if p.strip()]

try:
    i = int(open("state.txt").read().strip())
except Exception:
    i = 0
i = i % len(posts)

data = urllib.parse.urlencode({"chat_id": chat, "text": posts[i]}).encode()
url = f"https://api.telegram.org/bot{token}/sendMessage"
res = urllib.request.urlopen(url, data, timeout=30).read().decode()
print("ok" if '"ok":true' in res else res)

open("state.txt", "w").write(str(i + 1))
