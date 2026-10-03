#!/usr/bin/env python3
"""
Pinterest-style study infographic engine.
Cream background, Noto Serif headings, drawn icons, doodles, soft shadows,
and illustrated diagram types: pyramid, brain, cycle, timeline, compare, flow.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1080, 1350
SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-BoldItalic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BG = (252, 247, 238)
INK = (74, 64, 56)
BROWN = (120, 100, 85)
GOLD = (198, 164, 110)
CARD = (255, 253, 248)
SHADOW = (232, 220, 200)
WHITE = (255, 255, 255)

def F(p, s):
    return ImageFont.truetype(p, s)

def shade(color, f=0.88):
    return tuple(int(c * f) for c in color)

# ---------------- icons ----------------
def _star(d, cx, cy, r, color):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=color)

def _heart(d, cx, cy, s, color):
    r = s / 2
    d.ellipse([cx - r, cy - r * 0.9, cx, cy + r * 0.3], fill=color)
    d.ellipse([cx, cy - r * 0.9, cx + r, cy + r * 0.3], fill=color)
    d.polygon([(cx - r, cy), (cx + r, cy), (cx, cy + r)], fill=color)

def _shield(d, cx, cy, s, color):
    w, h = s, s * 1.15
    d.polygon([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2),
               (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)], fill=color)
    d.line([(cx - w * 0.22, cy - h * 0.05), (cx - w * 0.02, cy + h * 0.18),
            (cx + w * 0.28, cy - h * 0.22)], fill="white", width=3)

def _sun(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    for i in range(8):
        a = i * math.pi / 4
        d.line([(cx + (r + 4) * math.cos(a), cy + (r + 4) * math.sin(a)),
                (cx + (r + 13) * math.cos(a), cy + (r + 13) * math.sin(a))],
               fill=color, width=3)

def _apple(d, cx, cy, s, color):
    r = s / 2
    d.ellipse([cx - r, cy - r * 0.85, cx + r, cy + r * 0.85], fill=color)
    d.line([(cx, cy - r * 0.85), (cx + 2, cy - r * 1.25)], fill=(110, 85, 60), width=3)
    d.polygon([(cx + 2, cy - r * 1.25), (cx + r * 0.7, cy - r * 1.15),
               (cx + 2, cy - r * 0.95)], fill=(143, 154, 136))

def _book(d, cx, cy, s, color):
    w, h = s, s * 0.75
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                        radius=4, fill=color)
    d.line([(cx, cy - h / 2), (cx, cy + h / 2)], fill=WHITE, width=3)
    d.line([(cx - w / 2 + 8, cy - h / 4), (cx - 6, cy - h / 4)], fill=WHITE, width=2)
    d.line([(cx + 6, cy - h / 4), (cx + w / 2 - 8, cy - h / 4)], fill=WHITE, width=2)

def _chat(d, cx, cy, s, color):
    w, h = s, s * 0.7
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                        radius=10, fill=color)
    d.polygon([(cx - w / 4, cy + h / 2), (cx - w / 4, cy + h / 2 + 10),
               (cx - w / 8, cy + h / 2)], fill=color)
    for yy in (-6, 4):
        d.line([(cx - w / 2 + 10, cy + yy), (cx + w / 2 - 10, cy + yy)],
               fill=WHITE, width=3)

def _scale(d, cx, cy, s, color):
    d.line([(cx, cy - s / 2), (cx, cy + s / 2)], fill=color, width=4)
    d.line([(cx - s / 2, cy - s / 4), (cx + s / 2, cy - s / 4)], fill=color, width=4)
    for sx in (cx - s / 2, cx + s / 2):
        d.line([(sx, cy - s / 4), (sx, cy)], fill=color, width=3)
        d.arc([sx - 14, cy - 16, sx + 14, cy + 12], 0, 180, fill=color, width=3)
    d.line([(cx - 14, cy + s / 2), (cx + 14, cy + s / 2)], fill=color, width=4)

def _clock(d, cx, cy, s, color):
    r = s / 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    d.line([(cx, cy), (cx, cy - r * 0.55)], fill=color, width=4)
    d.line([(cx, cy), (cx + r * 0.4, cy)], fill=color, width=4)

def _people(d, cx, cy, s, color):
    r = s * 0.22
    d.ellipse([cx - r - 14, cy - r - 8, cx - 14 + r, cy - 8 + r], fill=color)
    d.ellipse([cx - 14, cy + 2, cx + 14 - 28 + 28, cy + 2], fill=color)  # noop keep
    d.chord([cx - r - 14, cy - 4, cx + r - 14, cy + r * 2], 180, 360, fill=color)
    d.ellipse([cx - r + 14, cy - r - 8, cx + 14 + r, cy - 8 + r], fill=color)
    d.chord([cx - r + 14, cy - 4, cx + r + 14, cy + r * 2], 180, 360, fill=color)

def _check(d, cx, cy, s, color):
    d.ellipse([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], fill=color)
    d.line([(cx - s * 0.22, cy), (cx - s * 0.05, cy + s * 0.18),
            (cx + s * 0.25, cy - s * 0.2)], fill="white", width=4)

def _alert(d, cx, cy, s, color):
    d.polygon([(cx, cy - s / 2), (cx + s / 2, cy + s / 2),
               (cx - s / 2, cy + s / 2)], fill=color)
    d.text((cx, cy + 2), "!", font=F(SANS_B, int(s * 0.5)), fill="white", anchor="mm")

def _bulb(d, cx, cy, s, color):
    r = s * 0.32
    d.ellipse([cx - r, cy - r - 6, cx + r, cy + r - 6], fill=color)
    d.rectangle([cx - 8, cy + r - 8, cx + 8, cy + r + 8], fill=shade(color))
    for i in range(6):
        a = -math.pi / 2 + i * math.pi / 3 + 0.3
        d.line([(cx + (r + 5) * math.cos(a), cy - 6 + (r + 5) * math.sin(a)),
                (cx + (r + 11) * math.cos(a), cy - 6 + (r + 11) * math.sin(a))],
               fill=color, width=3)

def _lock(d, cx, cy, s, color):
    w = s * 0.62
    d.rounded_rectangle([cx - w / 2, cy - w / 4, cx + w / 2, cy + w / 2],
                        radius=6, fill=color)
    d.arc([cx - w / 3, cy - w * 0.62, cx + w / 3, cy + w * 0.05],
          180, 360, fill=color, width=5)

def _doc(d, cx, cy, s, color):
    w, h = s * 0.62, s * 0.8
    d.polygon([(cx - w / 2, cy - h / 2), (cx + w / 4, cy - h / 2),
               (cx + w / 2, cy - h / 4), (cx + w / 2, cy + h / 2),
               (cx - w / 2, cy + h / 2)], fill=color)
    for yy in (-8, 2, 12):
        d.line([(cx - w / 2 + 8, cy + yy), (cx + w / 2 - 8, cy + yy)],
               fill=WHITE, width=2)

def _beaker(d, cx, cy, s, color):
    d.polygon([(cx - s * 0.18, cy - s / 2), (cx + s * 0.18, cy - s / 2),
               (cx + s * 0.32, cy + s / 2), (cx - s * 0.32, cy + s / 2)],
              outline=color, width=4)
    d.polygon([(cx - s * 0.24, cy + s * 0.08), (cx + s * 0.24, cy + s * 0.08),
               (cx + s * 0.28, cy + s / 2 - 4), (cx - s * 0.28, cy + s / 2 - 4)],
              fill=color)

def _brain(d, cx, cy, s, color):
    r = s / 2
    d.ellipse([cx - r, cy - r * 0.85, cx + r, cy + r * 0.85], fill=color)
    for k in range(3):
        yy = cy - r * 0.45 + k * r * 0.45
        d.arc([cx - r * 0.7, yy - r * 0.3, cx + r * 0.7, yy + r * 0.3],
              200, 340, fill=WHITE, width=3)
    d.line([(cx, cy - r * 0.85), (cx, cy + r * 0.85)], fill=WHITE, width=2)

def _smile(d, cx, cy, s, color):
    r = s / 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    for ex in (-r * 0.35, r * 0.35):
        d.ellipse([cx + ex - 4, cy - r * 0.2 - 4, cx + ex + 4, cy - r * 0.2 + 4],
                  fill=WHITE)
    d.arc([cx - r * 0.5, cy - r * 0.1, cx + r * 0.5, cy + r * 0.7],
          20, 160, fill=WHITE, width=4)

def _leaf(d, cx, cy, s, color):
    d.polygon([(cx - s / 2, cy), (cx, cy - s / 2), (cx + s / 2, cy),
               (cx, cy + s / 2)], fill=color)
    d.line([(cx - s / 2, cy), (cx + s / 2, cy)], fill=shade(color), width=2)

ICONS = {"apple": _apple, "shield": _shield, "heart": _heart, "star": _star,
         "sun": _sun, "book": _book, "chat": _chat, "scale": _scale,
         "clock": _clock, "people": _people, "check": _check, "alert": _alert,
         "bulb": _bulb, "lock": _lock, "doc": _doc, "beaker": _beaker,
         "brain": _brain, "smile": _smile, "leaf": _leaf}

def draw_icon(d, kind, cx, cy, s, color):
    fn = ICONS.get(kind, _star)
    if kind == "star":
        fn(d, cx, cy, s / 1.6, color)
    elif kind == "sun":
        fn(d, cx, cy, s / 2.4, color)
    else:
        fn(d, cx, cy, s, color)

# ---------------- chrome ----------------
def new_canvas():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # doodles
    for (x, y, r) in [(70, 250, 9), (1010, 260, 7), (940, 1140, 8), (90, 1170, 7),
                      (1000, 640, 6), (60, 700, 6)]:
        _star(d, x, y, r, (232, 214, 180))
    for (x, y, r) in [(130, 190, 4), (950, 190, 4), (150, 1250, 4), (930, 1270, 4)]:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(222, 200, 170))
    return img, d

def header(d, kicker, title, subtitle, tsize=54):
    d.text((W / 2, 50), kicker, font=F(SANS, 20), fill=BROWN, anchor="ma")
    tf = F(SERIF, tsize)
    while d.textlength(title, font=tf) > W - 120 and tsize > 34:
        tsize -= 4
        tf = F(SERIF, tsize)
    d.text((W / 2, 88), title, font=tf, fill=INK, anchor="ma")
    d.text((W / 2, 88 + tsize + 18), subtitle, font=F(SERIF_I, 25),
           fill=BROWN, anchor="ma")
    dy = 88 + tsize + 52
    d.line([(300, dy), (505, dy)], fill=GOLD, width=2)
    d.line([(575, dy), (780, dy)], fill=GOLD, width=2)
    d.polygon([(540, dy - 9), (549, dy), (540, dy + 9), (531, dy)], fill=GOLD)
    return dy + 40  # content starts here

def footer(d, text):
    fy = 1292
    d.line([(300, fy - 28), (505, fy - 28)], fill=GOLD, width=2)
    d.line([(575, fy - 28), (780, fy - 28)], fill=GOLD, width=2)
    d.polygon([(540, fy - 37), (549, fy - 28), (540, fy - 19), (531, fy - 28)],
              fill=GOLD)
    # DejaVu Sans for full glyph coverage (→ ♡ – render as boxes in Noto Serif)
    tf = F(SANS, 22)
    while d.textlength(text, font=tf) > W - 120:
        tf = F(SANS, tf.size - 1)
    d.text((W / 2, fy), text, font=tf, fill=BROWN, anchor="ma")

def card(d, x, y, w, h, color, icon, title, points, num=None):
    d.rounded_rectangle([x + 4, y + 5, x + w, y + h + 5], radius=18, fill=SHADOW)
    d.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=CARD)
    d.rounded_rectangle([x, y, x + 12, y + h], radius=6, fill=color)
    d.ellipse([x + 28, y + 20, x + 88, y + 80], fill=color)
    draw_icon(d, icon, x + 58, y + 50, 34, WHITE)
    t = f"{num}. {title}" if num else title
    d.text((x + 104, y + 10), t, font=F(SERIF, 24), fill=INK)
    yy = y + 46
    for p in points:
        for ln in _wrap(d, "•  " + p, F(SANS, 18), w - 130):
            d.text((x + 104, yy), ln, font=F(SANS, 18), fill=INK)
            yy += 24
            if yy > y + h - 10:
                return

def _wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w_
    if cur: lines.append(cur)
    return lines

# ---------------- diagrams ----------------
def diagram_pyramid(d, box, levels, label_side="right"):
    """levels: [{name, desc, color, icon}] bottom->top."""
    x1, y1, x2, y2 = box
    pcx = (x1 + x2) / 2 - (120 if label_side == "right" else 0)
    ptop, pbot = y1 + 10, y2 - 10
    phw = (x2 - x1) / 2 - (140 if label_side == "right" else 20)
    ph = pbot - ptop
    n = len(levels)
    lh = ph / n
    def hw(y): return phw * (y - ptop) / ph
    for i, lv in enumerate(levels):
        ya, yb = pbot - (i + 1) * lh, pbot - i * lh
        col = lv["color"]
        d.polygon([(pcx - hw(ya), ya), (pcx + hw(ya), ya),
                   (pcx + hw(yb), yb), (pcx - hw(yb), yb)], fill=col)
        d.polygon([(pcx - hw(ya), ya), (pcx, ya), (pcx, yb), (pcx - hw(yb), yb)],
                  fill=shade(col))
        d.line([(pcx - hw(ya), ya), (pcx + hw(ya), ya)], fill=BG, width=4)
        midy = (ya + yb) / 2
        if label_side == "right":
            sx = pcx + hw(midy) + 10
            lx = sx + 130
            d.line([(sx, midy), (lx - 16, midy)], fill=BROWN, width=2)
            d.ellipse([sx - 5, midy - 5, sx + 5, midy + 5], fill=col, outline=BROWN)
            d.text((lx, midy - 15), lv["name"], font=F(SERIF, 26), fill=INK, anchor="la")
            d.text((lx, midy + 15), lv.get("desc", ""), font=F(SANS, 18), fill=BROWN, anchor="la")
        else:
            draw_icon(d, lv.get("icon", "star"), pcx - hw(midy) * 0.5, midy, 30, WHITE)
            d.text((pcx + hw(midy) * 0.1, midy), lv["name"], font=F(SERIF, 22),
                   fill=WHITE, anchor="lm")

def diagram_brain(d, box, regions):
    """regions: [{name, desc, color}] — stylized brain with leader labels."""
    x1, y1, x2, y2 = box
    cx, cy = (x1 + x2) / 2 - 110, (y1 + y2) / 2
    rx, ry = 200, 150
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(232, 214, 196))
    d.ellipse([cx - rx + 12, cy - ry + 12, cx + rx - 12, cy + ry - 12],
              fill=(240, 226, 210))
    for k in range(4):
        yy = cy - 80 + k * 52
        d.arc([cx - 150, yy - 40, cx + 150, yy + 40], 195, 345, fill=(200, 175, 150), width=5)
    d.line([(cx, cy - ry + 12), (cx, cy + ry - 12)], fill=(200, 175, 150), width=3)
    n = len(regions)
    for i, rg in enumerate(regions):
        a = -0.9 + 1.8 * i / max(n - 1, 1)
        px, py = cx + 150 * math.cos(a), cy + 110 * math.sin(a)
        lx = cx + 300
        ly = y1 + 30 + i * ((y2 - y1 - 60) / max(n - 1, 1))
        d.line([(px, py), (lx - 14, ly)], fill=BROWN, width=2)
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=rg["color"], outline=BROWN)
        d.ellipse([lx - 24, ly - 24, lx + 24, ly + 24], fill=rg["color"])
        draw_icon(d, rg.get("icon", "brain"), lx, ly, 28, WHITE)
        d.text((lx + 34, ly - 14), rg["name"], font=F(SERIF, 24), fill=INK, anchor="la")
        d.text((lx + 34, ly + 12), rg.get("desc", ""), font=F(SANS, 17), fill=BROWN, anchor="la")

def diagram_cycle(d, box, nodes):
    """nodes: [{label, desc, color, icon}] arranged in a circle."""
    x1, y1, x2, y2 = box
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    n = len(nodes)
    r = min(x2 - x1, y2 - y1) / 2 - 90
    pts = []
    for i, nd in enumerate(nodes):
        a = -math.pi / 2 + 2 * math.pi * i / n
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        pts.append((px, py))
        d.ellipse([px - 62, py - 62, px + 62, py + 62], fill=nd["color"])
        d.ellipse([px - 62, py - 62, px + 62, py + 62], outline=shade(nd["color"]), width=3)
        draw_icon(d, nd.get("icon", "star"), px, py - 12, 40, WHITE)
        d.text((px, py + 32), nd["label"][:16], font=F(SANS_B, 17), fill=WHITE, anchor="mm")
    for i in range(n):
        x1p, y1p = pts[i]
        x2p, y2p = pts[(i + 1) % n]
        mx, my = (x1p + x2p) / 2, (y1p + y2p) / 2
        ang = math.atan2(y2p - y1p, x2p - x1p)
        d.line([(x1p + 66 * math.cos(ang), y1p + 66 * math.sin(ang)),
                (x2p - 66 * math.cos(ang), y2p - 66 * math.sin(ang))],
               fill=BROWN, width=3)
        d.polygon([(mx + 14 * math.cos(ang), my + 14 * math.sin(ang)),
                   (mx + 2 * math.cos(ang + 2.6), my + 2 * math.sin(ang + 2.6)),
                   (mx + 2 * math.cos(ang - 2.6), my + 2 * math.sin(ang - 2.6))],
                  fill=BROWN)

def diagram_timeline(d, box, steps):
    """steps: [{label, desc, color, icon}] horizontal timeline."""
    x1, y1, x2, y2 = box
    cy = (y1 + y2) / 2 - 20
    n = len(steps)
    d.line([(x1 + 60, cy), (x2 - 60, cy)], fill=BROWN, width=4)
    for i, st in enumerate(steps):
        px = x1 + 60 + (x2 - x1 - 120) * (i / (n - 1) if n > 1 else 0.5)
        d.ellipse([px - 40, cy - 40, px + 40, cy + 40], fill=st["color"])
        d.ellipse([px - 40, cy - 40, px + 40, cy + 40],
                  outline=shade(st["color"]), width=3)
        draw_icon(d, st.get("icon", "star"), px, cy, 44, WHITE)
        d.text((px, cy + 58), st["label"][:22], font=F(SERIF, 22), fill=INK, anchor="ma")
        for li, ln in enumerate(_wrap(d, st.get("desc", ""), F(SANS, 16), 190)):
            if li > 1: break
            d.text((px, cy + 88 + li * 22), ln, font=F(SANS, 16), fill=BROWN, anchor="ma")

def diagram_compare(d, box, columns):
    """columns: [{title, color, icon, rows:[str]}] as styled cards."""
    x1, y1, x2, y2 = box
    n = len(columns)
    gap = 18
    cw = (x2 - x1 - gap * (n - 1)) / n
    for i, col in enumerate(columns):
        cx1 = x1 + i * (cw + gap)
        cx2 = cx1 + cw
        d.rounded_rectangle([cx1 + 3, y1 + 5, cx2, y2], radius=18, fill=SHADOW)
        d.rounded_rectangle([cx1, y1, cx2, y2 - 5], radius=18, fill=CARD)
        d.rounded_rectangle([cx1, y1, cx2, y1 + 86], radius=14, fill=col["color"])
        d.rounded_rectangle([cx1, y1 + 60, cx2, y1 + 86], fill=col["color"])
        draw_icon(d, col.get("icon", "star"), cx1 + 44, y1 + 43, 44, WHITE)
        d.text((cx1 + 72, y1 + 43), col["title"][:24], font=F(SERIF, 23),
               fill=WHITE, anchor="lm")
        yy = y1 + 108
        rf = F(SANS, 18)
        for r_ in col["rows"]:
            for ln in _wrap(d, "•  " + r_, rf, cw - 36):
                if yy > y2 - 24: break
                d.text((cx1 + 18, yy), ln, font=rf, fill=INK)
                yy += 26
            yy += 4

def diagram_flow(d, box, steps):
    """steps: [{label, desc, color, icon}] horizontal flow with arrows."""
    x1, y1, x2, y2 = box
    cy = (y1 + y2) / 2
    n = len(steps)
    bw = (x2 - x1 - (n - 1) * 46) / n
    for i, st in enumerate(steps):
        bx1 = x1 + i * (bw + 46)
        d.rounded_rectangle([bx1 + 3, cy - 88, bx1 + bw, cy + 92], radius=18, fill=SHADOW)
        d.rounded_rectangle([bx1, cy - 93, bx1 + bw, cy + 87], radius=18, fill=CARD, outline=st["color"], width=3)
        d.ellipse([bx1 + bw / 2 - 32, cy - 80, bx1 + bw / 2 + 32, cy - 16], fill=st["color"])
        draw_icon(d, st.get("icon", "star"), bx1 + bw / 2, cy - 48, 36, WHITE)
        d.text((bx1 + bw / 2, cy + 2), st["label"][:20], font=F(SERIF, 21), fill=INK, anchor="ma")
        for li, ln in enumerate(_wrap(d, st.get("desc", ""), F(SANS, 15), bw - 24)):
            if li > 2: break
            d.text((bx1 + bw / 2, cy + 30 + li * 21), ln, font=F(SANS, 15), fill=BROWN, anchor="ma")
        if i < n - 1:
            ax = bx1 + bw
            d.line([(ax + 4, cy), (ax + 42, cy)], fill=BROWN, width=4)
            d.polygon([(ax + 42, cy - 10), (ax + 42, cy + 10), (ax + 54, cy)], fill=BROWN)

# ---------------- orchestrator ----------------
DIAGRAM_FN = {
    "pyramid": diagram_pyramid, "brain": diagram_brain, "cycle": diagram_cycle,
    "timeline": diagram_timeline, "compare": diagram_compare, "flow": diagram_flow,
}

def render(spec, out_path):
    """spec = {kicker, title, subtitle, diagram:{type, height, ...type_args},
               cards:[{icon,color,title,points}], footer}"""
    img, d = new_canvas()
    y = header(d, spec.get("kicker", "PSYCHOLOGY • STUDY NOTES"),
               spec["title"], spec.get("subtitle", ""))
    dg = spec.get("diagram")
    if dg:
        dtype = dg["type"]
        dh = dg.get("height", 440)
        box = (54, y, W - 54, y + dh)
        kwargs = {k: v for k, v in dg.items() if k not in ("type", "height")}
        DIAGRAM_FN[dtype](d, box, **kwargs)
        y += dh + 26
    cards = spec.get("cards", [])
    if cards:
        n = len(cards)
        # card height: fit remaining space (leave 110 for footer)
        avail = (H - 110) - y
        ch = min(108, (avail - (n - 1) * 14) / n)
        cw = W - 108
        cy = y
        for i, c in enumerate(cards):
            card(d, 54, cy, cw, ch, c["color"], c.get("icon", "star"),
                 c["title"], c["points"], num=c.get("num"))
            cy += ch + 14
    footer(d, spec.get("footer", "Save this for your exams ♡ Good luck!"))
    img.save(out_path, "PNG")
    return out_path
