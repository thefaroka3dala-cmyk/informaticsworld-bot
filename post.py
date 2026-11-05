import os, uuid, urllib.request, urllib.parse

token = os.environ["BOT_TOKEN"]
chat = "@informaticsworldar"

text = open("posts.txt", encoding="utf-8").read().replace("\r\n", "\n")
posts = [p.strip() for p in text.split("\n---\n") if p.strip()]

try:
    i = int(open("state.txt").read().strip())
except Exception:
    i = 0
i = i % len(posts)
post = posts[i]


def tg(method, fields, photo=None):
    url = f"https://api.telegram.org/bot{token}/{method}"
    if photo is None:
        req = urllib.request.Request(url, urllib.parse.urlencode(fields).encode())
    else:
        b = uuid.uuid4().hex
        body = b""
        for k, v in fields.items():
            body += (f'--{b}\r\nContent-Disposition: form-data; name="{k}"'
                     f"\r\n\r\n{v}\r\n").encode()
        body += (f'--{b}\r\nContent-Disposition: form-data; name="photo"; '
                 f'filename="card.png"\r\nContent-Type: image/png\r\n\r\n').encode()
        body += photo + b"\r\n" + f"--{b}--\r\n".encode()
        req = urllib.request.Request(
            url, body, {"Content-Type": f"multipart/form-data; boundary={b}"})
    return urllib.request.urlopen(req, timeout=60).read().decode()


try:
    from card import make_card
    make_card(post, "card.png")
    img = open("card.png", "rb").read()
    if len(post) <= 1000:
        res = tg("sendPhoto", {"chat_id": chat, "caption": post}, img)
    else:
        res = tg("sendPhoto", {"chat_id": chat}, img)
        tg("sendMessage", {"chat_id": chat, "text": post})
except Exception as e:
    print("card failed, sending text only:", e)
    res = tg("sendMessage", {"chat_id": chat, "text": post})

print("ok" if '"ok":true' in res else res)
open("state.txt", "w").write(str(i + 1))
