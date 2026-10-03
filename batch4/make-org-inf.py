#!/usr/bin/env python3
"""Composite 20 Organizational Psychology infographics: AI bg + crisp text overlay."""
import json, textwrap, os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
BASE = '/home/hatch/workspace/zehen/batch4'
BG_DIR = BASE + '/inf-bg'
OUT_DIR = BASE + '/inf-org-out'
os.makedirs(OUT_DIR, exist_ok=True)

BG1 = BG_DIR + '/media-generation-org-bg1-0-e8e87ad1-0cff-4053-abd7-98f3abbe91bb.webp'
BG2 = BG_DIR + '/media-generation-org-bg2-0-68291ddb-c244-4ecc-9339-3565fe985bc4.webp'

F_TITLE = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
F_BODY = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
F_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

PICKS = ['what-is-io-psychology','recruitment-strategies','selection-methods','employment-interviews',
'cognitive-ability-testing','training-development','performance-appraisal','360-degree-feedback',
'maslow-at-work','herzberg-two-factor-theory','expectancy-theory','goal-setting-theory',
'equity-theory','job-satisfaction','transformational-leadership','servant-leadership',
'team-dynamics','organizational-culture','change-management','burnout-at-work']

def font(path, size):
    return ImageFont.truetype(path, size)

def condense(text, maxlen=110):
    t = text.strip().replace('\n', ' ')
    idx = t.find('. ')
    if 40 < idx < maxlen:
        t = t[:idx + 1]
    if len(t) > maxlen:
        t = t[:maxlen].rsplit(' ', 1)[0] + '...'
    return t

def make_infographic(bg_path, title, takeaways, out_path):
    bg = Image.open(bg_path).convert('RGB')
    scale = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * scale), int(bg.height * scale)), Image.LANCZOS)
    x = (bg.width - W) // 2
    y = (bg.height - H) // 2
    bg = bg.crop((x, y, x + W, y + H))

    overlay = Image.new('L', (1, H))
    for i in range(H):
        if i < 420:
            v = int(205 - (i / 420) * 85)
        elif i < 900:
            v = 120
        else:
            v = int(120 + ((i - 900) / 450) * 95)
        overlay.putpixel((0, i), v)
    overlay = overlay.resize((W, H))
    black = Image.new('RGB', (W, H), (10, 8, 6))
    img = Image.composite(black, bg, overlay)

    d = ImageDraw.Draw(img, 'RGBA')

    badge = 'ORGANIZATIONAL PSYCHOLOGY'
    fb = font(F_BOLD, 30)
    bb = d.textbbox((0, 0), badge, font=fb)
    bw = bb[2] - bb[0] + 56
    bx = (W - bw) // 2
    d.rounded_rectangle([bx, 56, bx + bw, 56 + 62], radius=31, fill=(201, 111, 74, 235))
    d.text((bx + 28, 56 + 14), badge, font=fb, fill=(255, 252, 245))

    ft = font(F_TITLE, 62)
    lines = textwrap.wrap(title, width=24)
    ty = 150
    for ln in lines[:3]:
        tb = d.textbbox((0, 0), ln, font=ft)
        d.text(((W - (tb[2] - tb[0])) // 2, ty), ln, font=ft, fill=(255, 250, 240))
        ty += 78

    dy = ty + 18
    d.rounded_rectangle([(W - 120) // 2, dy, (W + 120) // 2, dy + 8], radius=4, fill=(201, 111, 74, 255))

    fnum = font(F_BOLD, 44)
    fpt = font(F_BODY, 31)
    card_h, gap, y0 = 148, 22, 400
    for i, tk in enumerate(takeaways):
        yy = y0 + i * (card_h + gap)
        d.rounded_rectangle([64, yy, W - 64, yy + card_h], radius=26, fill=(20, 16, 12, 178))
        d.rounded_rectangle([64, yy, W - 64, yy + card_h], radius=26, outline=(201, 111, 74, 120), width=2)
        cx, cy, r = 130, yy + card_h // 2, 38
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(201, 111, 74, 255))
        num = str(i + 1)
        nb = d.textbbox((0, 0), num, font=fnum)
        d.text((cx - (nb[2] - nb[0]) // 2, cy - (nb[3] - nb[1]) // 2 - 4), num, font=fnum, fill=(255, 252, 245))
        wrapped = textwrap.wrap(tk, width=44)
        tyy = yy + 22
        for wl in wrapped[:3]:
            d.text((196, tyy), wl, font=fpt, fill=(245, 238, 226))
            tyy += 40

    # footer with color emoji (NotoColorEmoji only renders at 109px; downscale)
    ff = font(F_BOLD, 34)
    fe = font('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
    eb = d.textbbox((0, 0), '\U0001F9E0', font=fe)
    ew, eh = eb[2] - eb[0] + 20, eb[3] - eb[1] + 20
    em_img = Image.new('RGBA', (ew, eh), (0, 0, 0, 0))
    em_d = ImageDraw.Draw(em_img)
    em_d.text((10, 10), '\U0001F9E0', font=fe, embedded_color=True)
    em_img = em_img.resize((46, 46), Image.LANCZOS)
    foot = 'Mysterious'
    fb2 = d.textbbox((0, 0), foot, font=ff)
    total_w = 46 + 14 + (fb2[2] - fb2[0])
    sx = (W - total_w) // 2
    img.paste(em_img, (sx, H - 96), em_img)
    d.text((sx + 46 + 14, H - 92), foot, font=ff, fill=(255, 250, 240))

    img.save(out_path, 'PNG', optimize=True)
    print('saved', out_path, os.path.getsize(out_path) // 1024, 'KB', flush=True)

def main():
    notes = json.load(open(BASE + '/organizational-psychology.json'))
    by_slug = {n['slug']: n for n in notes}
    manifest = []
    for i, slug in enumerate(PICKS):
        n = by_slug[slug]
        takes = [condense(p['point']) for p in n.get('points_json', [])[:5]]
        bg = BG1 if i % 2 == 0 else BG2
        out = '%s/org-%d.png' % (OUT_DIR, i + 1)
        make_infographic(bg, n['title'], takes, out)
        manifest.append({'slug': slug, 'title': n['title'], 'file': 'org-%d.png' % (i + 1)})
    json.dump(manifest, open(BASE + '/org-manifest.json', 'w'))
    print('DONE', len(manifest), flush=True)

main()
