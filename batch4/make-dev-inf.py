#!/usr/bin/env python3
"""Compose 20 developmental-psychology infographics: AI bg + crisp text overlay."""
import json, os, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = '/home/hatch/workspace/zehen/batch4'
BG_DIR = BASE + '/inf-bg'
OUT_DIR = BASE + '/inf-dev-out'
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1080, 1350
TERRA = (201, 111, 74)
CREAM = (253, 246, 236)
INK = (43, 33, 24)
GOLD = (217, 164, 65)
SAGE = (125, 140, 111)

FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def font(path, size):
    return ImageFont.truetype(path, size)

def cover_resize(im, w, h):
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))

def vgrad_overlay(w, h, stops):
    """stops: list of (y_frac, (r,g,b,a)) top->bottom. Returns RGBA overlay (fast)."""
    strip = Image.new('RGBA', (1, h), (0, 0, 0, 0))
    px = strip.load()
    for y in range(h):
        f = y / max(h - 1, 1)
        for i in range(len(stops) - 1):
            f0, c0 = stops[i]
            f1, c1 = stops[i + 1]
            if f0 <= f <= f1 or (i == len(stops) - 2 and f >= f1):
                t = 0 if f1 == f0 else (f - f0) / (f1 - f0)
                t = max(0, min(1, t))
                px[0, y] = tuple(int(c0[k] + (c1[k] - c0[k]) * t) for k in range(4))
                break
    return strip.resize((w, h), Image.BILINEAR)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ''
    for wd in words:
        t = (cur + ' ' + wd).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = wd
    if cur: lines.append(cur)
    return lines

def draw_shadow_text(d, xy, text, fnt, fill, shadow=(0, 0, 0, 160), off=3):
    x, y = xy
    d.text((x + off, y + off), text, font=fnt, fill=shadow)
    d.text((x, y), text, font=fnt, fill=fill)

topics = json.load(open(BASE + '/inf-dev-topics.json'))
bgs = [
    BG_DIR + '/media-generation-dev-bg1-0-f27967ab-e0aa-48bf-b7df-f42a3f188c06.webp',
    BG_DIR + '/media-generation-dev-bg2-0-208df7b0-f561-448c-ad0f-498b4eef39e9.webp',
]

made = []
for idx, t in enumerate(topics):
    bg = Image.open(bgs[idx % 2]).convert('RGB')
    bg = cover_resize(bg, W, H)
    # gentle warm tint to unify
    tint = Image.new('RGB', (W, H), (255, 244, 230))
    bg = Image.blend(bg, tint, 0.06)

    # top dark gradient for title legibility
    grad = vgrad_overlay(W, H, [
        (0.00, (25, 12, 6, 190)),
        (0.28, (25, 12, 6, 120)),
        (0.44, (25, 12, 6, 0)),
        (1.00, (25, 12, 6, 0)),
    ])
    canvas = Image.alpha_composite(bg.convert('RGBA'), grad)

    d = ImageDraw.Draw(canvas)
    f_badge = font(FB, 30)
    f_title = font(FB, 62)
    f_num = font(FB, 40)
    f_pt = font(FR, 32)
    f_foot = font(FB, 28)

    # badge pill
    badge = 'DEVELOPMENTAL PSYCHOLOGY'
    bw = d.textlength(badge, font=f_badge)
    pad_x, pad_y = 34, 14
    bx0, by0 = 60, 64
    bx1, by1 = bx0 + bw + pad_x * 2, by0 + 30 + pad_y * 2
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=30, fill=TERRA + (255,))
    d.text((bx0 + pad_x, by0 + pad_y - 2), badge, font=f_badge, fill=(255, 252, 245, 255))

    # title
    title_lines = wrap(d, t['title'], f_title, W - 140)
    ty = by1 + 36
    for ln in title_lines[:3]:
        draw_shadow_text(d, (70, ty), ln, f_title, (255, 250, 240, 255))
        ty += 78

    # bottom cream sheet
    sheet_y = 560
    sheet = Image.new('RGBA', (W, H - sheet_y), CREAM + (246,))
    mask = Image.new('L', (W, H - sheet_y), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, W, H - sheet_y], radius=48, fill=255)
    md.rectangle([0, 48, W, H - sheet_y], fill=255)
    canvas.paste(sheet, (0, sheet_y), mask)

    d = ImageDraw.Draw(canvas)
    # thin gold divider
    d.rounded_rectangle([70, sheet_y + 26, 190, sheet_y + 32], radius=3, fill=GOLD + (255,))

    py = sheet_y + 58
    for i, pt in enumerate(t['points'][:5]):
        num = str(i + 1)
        d.text((70, py), num, font=f_num, fill=TERRA + (255,))
        lines = wrap(d, pt, f_pt, W - 200)
        lx = 130
        for li, ln in enumerate(lines[:3]):
            d.text((lx, py + (2 if li == 0 else 0)), ln, font=f_pt, fill=INK + (255,))
            py += 42
        py += 26

    # footer
    foot = 'M Y S T E R I O U S'
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, H - 78), foot, font=f_foot, fill=(120, 95, 70, 255))
    sub = 'learn the mind, one day at a time'
    f_sub = font(FR, 24)
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, H - 44), sub, font=f_sub, fill=(140, 115, 88, 255))

    out = f'{OUT_DIR}/dev-{idx + 1:02d}.png'
    if os.path.exists(out):
        made.append((out, t['title']))
        continue
    canvas.convert('RGB').save(out, 'PNG', optimize=True)
    made.append((out, t['title']))
    print('made', out, os.path.getsize(out) // 1024, 'KB')

print('TOTAL:', len(made))
