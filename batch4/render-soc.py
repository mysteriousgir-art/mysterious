#!/usr/bin/env python3
"""Render 20 Social Psychology visual infographics (1080x1350 PNG)."""
import json, os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
FD = '/usr/share/fonts/truetype/dejavu/'
TERRA = (201, 111, 74)
GOLD = (217, 164, 65)
CREAM = (253, 246, 236)

F_TITLE = ImageFont.truetype(FD + 'DejaVuSans-Bold.ttf', 62)
F_BADGE = ImageFont.truetype(FD + 'DejaVuSans-Bold.ttf', 30)
F_PT = ImageFont.truetype(FD + 'DejaVuSans.ttf', 35)
F_NUM = ImageFont.truetype(FD + 'DejaVuSans-Bold.ttf', 30)
F_FOOT = ImageFont.truetype(FD + 'DejaVuSans-Bold.ttf', 26)

def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def letterspace(draw, xy, text, font, fill, spacing=6):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing
    return x

def vgrad(size, top_alpha, bot_alpha, color=(18, 12, 9)):
    w, h = size
    ov = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for yy in range(h):
        t = yy / h
        a = int(top_alpha + (bot_alpha - top_alpha) * t)
        d.line([(0, yy), (w, yy)], fill=color + (a,))
    return ov

def crop_fit(im, w, h):
    sw, sh = im.size
    scale = max(w / sw, h / sh)
    im = im.resize((int(sw * scale) + 1, int(sh * scale) + 1), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))

def rounded(draw, box, r, fill):
    draw.rounded_rectangle(box, radius=r, fill=fill)

def tshadow(draw, pos, text, font, fill=(255, 255, 255)):
    x, y = pos
    draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, 170))
    draw.text((x, y), text, font=font, fill=fill)

BASE = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(os.path.join(BASE, 'soc-takeaways.json')))['items']
bgs = [
    os.path.join(BASE, 'inf-bg', 'media-generation-soc-bg1-0-f69407ae-629b-4325-ab4c-5535321d9527.webp'),
    os.path.join(BASE, 'inf-bg', 'media-generation-soc-bg2-0-c22140cb-9a22-4ad4-b851-20319aecd3a3.webp'),
]
bg_imgs = [crop_fit(Image.open(p).convert('RGB'), W, H) for p in bgs]

outdir = os.path.join(BASE, 'inf-soc-out')
os.makedirs(outdir, exist_ok=True)

for n, it in enumerate(items, 1):
    base = bg_imgs[(n - 1) % 2].copy()
    base = Image.blend(base, Image.new('RGB', (W, H), (12, 9, 7)), 0.18)
    base = base.convert('RGBA')
    base.alpha_composite(vgrad((W, H), 40, 215))
    d = ImageDraw.Draw(base)

    badge_txt = 'SOCIAL PSYCHOLOGY'
    bw = int(d.textlength(badge_txt, font=F_BADGE) + len(badge_txt) * 6 + 56)
    bx, by = 70, 64
    rounded(d, [bx, by, bx + bw, by + 62], 31, TERRA + (255,))
    letterspace(d, (bx + 30, by + 15), badge_txt, F_BADGE, (255, 255, 255))

    y = by + 112
    for line in wrap(d, it['title'], F_TITLE, W - 140):
        tshadow(d, (70, y), line, F_TITLE)
        y += 78

    y += 12
    d.rounded_rectangle([70, y, 70 + 130, y + 7], radius=3, fill=GOLD + (255,))
    y += 36

    for i, pt in enumerate(it['points'], 1):
        cx, cy, r = 96, y + 22, 26
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD + (255,))
        num = str(i)
        nw = d.textlength(num, font=F_NUM)
        d.text((cx - nw / 2, cy - 21), num, font=F_NUM, fill=(30, 20, 12))
        ty = y
        for line in wrap(d, pt, F_PT, W - 140 - 92):
            tshadow(d, (150, ty), line, F_PT)
            ty += 46
        y = ty + 26
        if y > H - 190:
            break

    d.rounded_rectangle([70, H - 96, 70 + 300, H - 96 + 6], radius=3, fill=TERRA + (255,))
    letterspace(d, (70, H - 78), 'MYSTERIOUS', F_FOOT, CREAM + (255,), spacing=8)

    base.convert('RGB').save(os.path.join(outdir, 'soc-%d.png' % n))
    print('soc-%d.png  %s' % (n, it['title'][:45]), flush=True)

print('DONE', len(items))
