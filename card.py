import glob, os, re, unicodedata
from PIL import Image, ImageDraw, ImageFont, features

W = H = 1080
TOP = (9, 16, 38)
BOTTOM = (28, 14, 64)
ACCENT = (0, 200, 255)
WHITE = (245, 248, 255)
SOFT = (176, 190, 220)
MARGIN = 90
LINK = "t.me/informaticsworldar"


def find_font():
    for pat in (
        "/usr/share/fonts/**/NotoSansArabic*.ttf",
        "/usr/share/fonts/**/DejaVuSans.ttf",
        "**/DejaVuSans.ttf",
    ):
        found = sorted(glob.glob(pat, recursive=True))
        if found:
            return found[0]
    raise RuntimeError("no Arabic-capable font found")


def clean(line):
    out = []
    for ch in line:
        if unicodedata.category(ch) in ("So", "Cs", "Cn") or ch in "\ufe0f\u200d":
            continue
        out.append(ch)
    s = re.sub(r"#\S+", "", "".join(out))
    return re.sub(r"\s+", " ", s).strip()


def measure(draw, text, font):
    return draw.textlength(text, font=font, direction="rtl", language="ar")


def wrap(draw, text, font, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if measure(draw, trial, font) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def put(draw, xy, text, font, fill, anchor="ra"):
    draw.text(xy, text, font=font, fill=fill, anchor=anchor,
              direction="rtl", language="ar")


def make_card(text, path="card.png"):
    if not features.check("raqm"):
        raise RuntimeError("raqm (Arabic shaping) not available")
    font_path = find_font()

    img = Image.new("RGB", (W, H), TOP)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        c = tuple(int(TOP[i] + (BOTTOM[i] - TOP[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)

    f_brand = ImageFont.truetype(font_path, 40)
    f_small = ImageFont.truetype(font_path, 28)
    f_title = ImageFont.truetype(font_path, 66)
    f_body = ImageFont.truetype(font_path, 42)
    f_link = ImageFont.truetype(font_path, 34)

    # header: brand (right) and optional logo (left)
    put(d, (W - MARGIN, 70), "عالم المعلوماتية", f_brand, WHITE)
    put(d, (W - MARGIN, 124), "INFORMATICS WORLD", f_small, ACCENT)
    if os.path.exists("logo.png"):
        logo = Image.open("logo.png").convert("RGBA").resize((110, 110))
        mask = Image.new("L", (110, 110), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, 109, 109), fill=255)
        img.paste(logo, (MARGIN, 60), mask)
    d.rectangle([MARGIN, 190, W - MARGIN, 196], fill=ACCENT)

    lines = [clean(l) for l in text.split("\n")]
    lines = [l for l in lines if l]
    title = lines[0] if lines else ""
    body = lines[1:]
    maxw = W - 2 * MARGIN

    y = 250
    for ln in wrap(d, title, f_title, maxw)[:3]:
        put(d, (W - MARGIN, y), ln, f_title, WHITE)
        y += 92
    y += 24

    limit = H - 190
    chosen = None
    for size in (42, 38, 34, 31, 28):
        fb = ImageFont.truetype(font_path, size)
        lh, gap = int(size * 1.48), int(size * 0.33)
        h = 0
        for para in body:
            h += len(wrap(d, para, fb, maxw)) * lh + gap
        if y + h <= limit or size == 28:
            chosen = (fb, lh, gap)
            break
    f_body, lh, gap = chosen
    stop = False
    for para in body:
        if stop:
            break
        for ln in wrap(d, para, f_body, maxw):
            if y + lh > limit:
                put(d, (W - MARGIN, y), "…", f_body, SOFT)
                stop = True
                break
            put(d, (W - MARGIN, y), ln, f_body, SOFT)
            y += lh
        y += gap

    d.rectangle([MARGIN, H - 140, W - MARGIN, H - 135], fill=ACCENT)
    d.text((W // 2, H - 80), LINK, font=f_link, fill=ACCENT, anchor="mm")
    img.save(path)
    return path
