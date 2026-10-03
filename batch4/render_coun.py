#!/usr/bin/env python3
"""Render 20 Counseling & Therapy visual infographics (1080x1350 PNG)."""
import json, os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
FD = '/usr/share/fonts/truetype/dejavu/'
F_TITLE = ImageFont.truetype(FD + 'DejaVuSans-Bold.ttf', 62)
F_BADGE = ImageFont.truetype(FD + 'DejaVuSans-Bold.ttf', 30)
F_POINT = ImageFont.truetype(FD + 'DejaVuSans.ttf', 29)
F_FOOT = ImageFont.truetype(FD + 'DejaVuSans-Bold.ttf', 26)

TERRA = (201, 111, 74)
GOLD = (212, 175, 105)
CREAM = (253, 248, 240)
BASE = '/home/hatch/workspace/zehen/batch4'
BG1 = os.path.join(BASE, 'inf-bg/media-generation-coun-bg1-0-9aede702-02f4-4a17-a768-b53d103bf768.webp')
BG2 = os.path.join(BASE, 'inf-bg/media-generation-coun-bg2-0-a6267a43-b4f0-431e-af02-a25148608078.webp')
OUTDIR = os.path.join(BASE, 'inf-coun-png')
os.makedirs(OUTDIR, exist_ok=True)

def cover(im, w, h):
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x = (im.width - w) // 2; y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))

def vgrad(w, h, top_alpha, bot_alpha):
    g = Image.new('L', (1, h))
    px = g.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        px[0, y] = int(top_alpha + (bot_alpha - top_alpha) * t)
    return g.resize((w, h))

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ''
    for wd in words:
        t = (cur + ' ' + wd).strip()
        if draw.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = wd
    if cur: lines.append(cur)
    return lines

def bullet(draw, xy, r, color):
    x, y = xy
    draw.polygon([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], fill=color)

items = json.load(open(os.path.join(BASE, 'coun-takeaways.json')))
assert len(items) == 20, len(items)

for i, it in enumerate(items):
    bg = Image.open(BG1 if i % 2 == 0 else BG2).convert('RGB')
    base = cover(bg, W, H)

    scrim = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    top = Image.new('RGBA', (W, 560), (10, 8, 6, 255))
    top.putalpha(vgrad(W, 560, 200, 0))
    scrim.alpha_composite(top, (0, 0))
    bot = Image.new('RGBA', (W, 780), (10, 8, 6, 255))
    bot.putalpha(vgrad(W, 780, 0, 215))
    scrim.alpha_composite(bot, (0, H - 780))
    base = Image.alpha_composite(base.convert('RGBA'), scrim)
    d = ImageDraw.Draw(base)

    label = 'COUNSELING & THERAPY'
    bw = d.textlength(label, font=F_BADGE) + 56
    bx = (W - bw) / 2
    d.rounded_rectangle([bx, 64, bx + bw, 64 + 58], 29, fill=TERRA + (255,))
    d.text((W / 2, 93), label, font=F_BADGE, fill=(255, 255, 255, 255), anchor='mm')

    lines = wrap(d, it['title'], F_TITLE, W - 140)
    y = 150
    for ln in lines[:2]:
        d.text((W / 2, y), ln, font=F_TITLE, fill=(255, 255, 255, 255), anchor='ma',
               stroke_width=2, stroke_fill=(20, 14, 10, 160))
        y += 74

    py = 560
    for p in it['points'][:5]:
        plines = wrap(d, p, F_POINT, W - 260)
        ph = 34 + len(plines) * 40
        d.rounded_rectangle([70, py, W - 70, py + ph], 22, fill=(18, 14, 11, 165))
        bullet(d, (118, py + 34), 11, GOLD)
        ty = py + 22
        for ln in plines:
            d.text((152, ty), ln, font=F_POINT, fill=CREAM + (255,), anchor='la')
            ty += 40
        py += ph + 18

    d.text((W / 2, H - 56), 'M Y S T E R I O U S', font=F_FOOT,
           fill=(240, 228, 210, 230), anchor='mm')

    out = os.path.join(OUTDIR, f'coun-{i+1:02d}.png')
    base.convert('RGB').save(out, quality=92)
    print('rendered', out, flush=True)

print('ALL DONE')
