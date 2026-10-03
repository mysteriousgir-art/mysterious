#!/usr/bin/env python3
"""
Cheat-sheet style infographic template v2 (white background, multi-color pastel cards).
Bigger data density + full-width diagram panel with proper visible diagrams.

Usage:
    from cheatsheet import render_cheatsheet
    render_cheatsheet(spec, "/path/out.png")

spec = {
  "title": "Health Psychology",
  "subtitle": "Chapter 1 - Introduction & Basic Concepts",
  "sections": [                       # up to 6 cards, dense bullets
    {"title": "Health Psychology", "color": "blue",
     "blocks": [
       {"type": "def", "label": "Definition", "items": ["..."]},
       {"type": "points", "label": "Main Focus", "items": ["..."]},
       {"type": "example", "label": "Example", "items": ["..."]},
       {"type": "revision", "label": "Instant Revision", "items": ["..."]},
     ]},
  ],
  "diagram_panel": {                  # full-width proper diagram
     "title": "Visual Guide: Classical vs Operant",
     "diagram": "comparison",         # comparison | flow | cycle | pyramid | bars | timeline | scale | venn | brain
     "columns": ["A", "B"],           # for comparison
     "rows": [["a1","b1"], ["a2","b2"]],
     "labels": ["x", "y", "z"],       # for flow/cycle/pyramid/bars/timeline/venn
  },
  "footer": ["item1", "item2", ...],
}
Colors: blue, green, pink, purple, yellow, orange, teal, red
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1080, 1350
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

TEAL_DARK = (13, 92, 92)
TEAL = (18, 120, 120)
INK = (30, 35, 45)
GREY = (90, 100, 115)

PALETTE = {
    "blue":   {"bg": (232, 244, 250), "bd": (150, 195, 220), "hd": (30, 110, 160)},
    "green":  {"bg": (233, 247, 239), "bd": (150, 205, 170), "hd": (25, 130, 75)},
    "pink":   {"bg": (253, 238, 242), "bd": (240, 170, 185), "hd": (190, 60, 95)},
    "purple": {"bg": (241, 234, 251), "bd": (195, 170, 230), "hd": (110, 70, 170)},
    "yellow": {"bg": (254, 249, 231), "bd": (240, 215, 140), "hd": (160, 120, 20)},
    "orange": {"bg": (254, 240, 230), "bd": (240, 190, 150), "hd": (200, 110, 40)},
    "teal":   {"bg": (230, 247, 245), "bd": (140, 205, 195), "hd": (15, 120, 115)},
    "red":    {"bg": (253, 235, 235), "bd": (235, 160, 160), "hd": (180, 50, 50)},
}
PAL_LIST = list(PALETTE.values())

# ---------------- per-category color themes ----------------
# Each category gets its own signature look: tinted page background,
# matching header/footer accent, and 6 harmonious card shades.
THEMES = {
    "biological": {  # teal / sea green
        "page_bg": (233, 247, 244), "accent_dark": (11, 92, 80),
        "accent": (20, 135, 115), "accent_light": (205, 238, 230),
        "cards": [
            {"bg": (213, 240, 233), "bd": (128, 195, 178), "hd": (12, 100, 86)},
            {"bg": (220, 244, 224), "bd": (134, 200, 158), "hd": (22, 120, 66)},
            {"bg": (208, 234, 240), "bd": (122, 188, 200), "hd": (14, 104, 124)},
            {"bg": (227, 245, 235), "bd": (148, 206, 172), "hd": (28, 114, 78)},
            {"bg": (216, 237, 242), "bd": (132, 194, 204), "hd": (16, 98, 118)},
            {"bg": (223, 246, 229), "bd": (138, 201, 162), "hd": (24, 116, 70)},
        ]},
    "clinical": {  # indigo / deep blue
        "page_bg": (236, 239, 251), "accent_dark": (38, 52, 128),
        "accent": (63, 83, 178), "accent_light": (212, 220, 246),
        "cards": [
            {"bg": (221, 227, 248), "bd": (148, 163, 220), "hd": (44, 62, 138)},
            {"bg": (227, 231, 250), "bd": (158, 173, 226), "hd": (54, 72, 148)},
            {"bg": (217, 223, 246), "bd": (143, 158, 216), "hd": (38, 56, 132)},
            {"bg": (229, 227, 250), "bd": (163, 163, 226), "hd": (68, 66, 154)},
            {"bg": (223, 229, 248), "bd": (153, 168, 222), "hd": (48, 66, 142)},
            {"bg": (225, 225, 248), "bd": (156, 156, 221), "hd": (58, 58, 146)},
        ]},
    "cognitive": {  # violet / purple
        "page_bg": (242, 236, 250), "accent_dark": (88, 48, 140),
        "accent": (120, 75, 185), "accent_light": (226, 212, 246),
        "cards": [
            {"bg": (232, 222, 248), "bd": (178, 148, 222), "hd": (96, 56, 150)},
            {"bg": (238, 228, 250), "bd": (190, 160, 228), "hd": (108, 66, 160)},
            {"bg": (228, 218, 246), "bd": (172, 142, 218), "hd": (90, 50, 144)},
            {"bg": (240, 224, 248), "bd": (194, 154, 226), "hd": (120, 60, 162)},
            {"bg": (234, 226, 249), "bd": (184, 156, 225), "hd": (102, 62, 155)},
            {"bg": (236, 220, 247), "bd": (188, 148, 224), "hd": (114, 54, 158)},
        ]},
    "counseling": {  # rose / pink
        "page_bg": (252, 238, 243), "accent_dark": (150, 45, 85),
        "accent": (195, 70, 115), "accent_light": (248, 214, 226),
        "cards": [
            {"bg": (248, 224, 232), "bd": (228, 150, 172), "hd": (158, 52, 92)},
            {"bg": (250, 230, 236), "bd": (232, 160, 180), "hd": (168, 60, 100)},
            {"bg": (246, 220, 230), "bd": (224, 144, 168), "hd": (152, 46, 88)},
            {"bg": (251, 226, 238), "bd": (234, 154, 184), "hd": (176, 58, 104)},
            {"bg": (249, 228, 234), "bd": (230, 156, 176), "hd": (162, 56, 96)},
            {"bg": (247, 222, 232), "bd": (226, 148, 170), "hd": (170, 50, 98)},
        ]},
    "developmental": {  # amber / warm orange
        "page_bg": (253, 244, 230), "accent_dark": (150, 85, 20),
        "accent": (195, 120, 35), "accent_light": (248, 228, 196),
        "cards": [
            {"bg": (250, 234, 210), "bd": (230, 180, 120), "hd": (158, 92, 24)},
            {"bg": (252, 238, 218), "bd": (234, 188, 130), "hd": (168, 100, 28)},
            {"bg": (248, 230, 204), "bd": (226, 174, 114), "hd": (152, 86, 20)},
            {"bg": (253, 236, 214), "bd": (236, 184, 124), "hd": (176, 98, 30)},
            {"bg": (250, 232, 208), "bd": (232, 178, 118), "hd": (162, 94, 26)},
            {"bg": (251, 234, 212), "bd": (233, 182, 122), "hd": (170, 90, 28)},
        ]},
    "health": {  # emerald / fresh green
        "page_bg": (234, 248, 238), "accent_dark": (18, 105, 62),
        "accent": (30, 145, 88), "accent_light": (206, 238, 218),
        "cards": [
            {"bg": (216, 240, 222), "bd": (132, 198, 152), "hd": (22, 112, 66)},
            {"bg": (222, 243, 228), "bd": (142, 204, 162), "hd": (30, 122, 74)},
            {"bg": (212, 238, 220), "bd": (128, 196, 150), "hd": (18, 108, 62)},
            {"bg": (226, 244, 230), "bd": (146, 206, 164), "hd": (34, 126, 78)},
            {"bg": (218, 241, 224), "bd": (136, 200, 156), "hd": (26, 116, 70)},
            {"bg": (220, 242, 226), "bd": (140, 202, 158), "hd": (28, 118, 72)},
        ]},
    "organizational": {  # olive / sage green
        "page_bg": (244, 246, 232), "accent_dark": (82, 92, 28),
        "accent": (117, 127, 42), "accent_light": (230, 236, 198),
        "cards": [
            {"bg": (236, 240, 214), "bd": (190, 200, 130), "hd": (90, 100, 32)},
            {"bg": (240, 243, 220), "bd": (196, 206, 140), "hd": (100, 110, 36)},
            {"bg": (232, 237, 208), "bd": (184, 194, 124), "hd": (84, 94, 28)},
            {"bg": (241, 244, 216), "bd": (198, 208, 134), "hd": (108, 118, 40)},
            {"bg": (238, 241, 212), "bd": (192, 202, 128), "hd": (94, 104, 34)},
            {"bg": (234, 238, 210), "bd": (188, 198, 126), "hd": (104, 114, 38)},
        ]},
    "personality": {  # fuchsia / magenta
        "page_bg": (250, 236, 246), "accent_dark": (140, 40, 110),
        "accent": (185, 62, 145), "accent_light": (244, 212, 232),
        "cards": [
            {"bg": (244, 220, 236), "bd": (218, 142, 188), "hd": (148, 46, 118)},
            {"bg": (247, 226, 240), "bd": (224, 152, 196), "hd": (158, 54, 126)},
            {"bg": (242, 216, 234), "bd": (214, 136, 184), "hd": (142, 40, 112)},
            {"bg": (248, 222, 238), "bd": (226, 146, 192), "hd": (166, 52, 130)},
            {"bg": (245, 224, 237), "bd": (220, 148, 190), "hd": (152, 50, 122)},
            {"bg": (246, 218, 235), "bd": (222, 140, 186), "hd": (160, 44, 124)},
        ]},
    "research": {  # cyan / ice blue
        "page_bg": (232, 245, 250), "accent_dark": (14, 95, 125),
        "accent": (22, 130, 165), "accent_light": (202, 234, 244),
        "cards": [
            {"bg": (212, 236, 244), "bd": (126, 190, 212), "hd": (18, 102, 132)},
            {"bg": (218, 239, 246), "bd": (136, 196, 216), "hd": (26, 112, 142)},
            {"bg": (208, 233, 242), "bd": (120, 186, 208), "hd": (14, 98, 128)},
            {"bg": (222, 240, 247), "bd": (140, 198, 218), "hd": (30, 116, 146)},
            {"bg": (214, 237, 245), "bd": (130, 192, 214), "hd": (22, 106, 136)},
            {"bg": (216, 238, 246), "bd": (134, 194, 216), "hd": (24, 108, 138)},
        ]},
    "social": {  # royal blue
        "page_bg": (232, 240, 252), "accent_dark": (30, 58, 138),
        "accent": (37, 99, 235), "accent_light": (205, 220, 250),
        "cards": [
            {"bg": (214, 226, 250), "bd": (140, 165, 235), "hd": (32, 64, 148)},
            {"bg": (220, 230, 252), "bd": (150, 175, 240), "hd": (40, 74, 158)},
            {"bg": (210, 222, 248), "bd": (134, 160, 232), "hd": (28, 58, 142)},
            {"bg": (224, 232, 253), "bd": (154, 178, 242), "hd": (46, 78, 162)},
            {"bg": (216, 228, 251), "bd": (144, 168, 236), "hd": (36, 68, 152)},
            {"bg": (212, 224, 249), "bd": (138, 162, 234), "hd": (42, 72, 156)},
        ]},
}

def F(path, size):
    return ImageFont.truetype(path, size)

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

BULLET = "\u2022  "

# ---------------- big diagrams (full-width panel) ----------------
def draw_big_diagram(d, name, box, spec, accent):
    x1, y1, x2, y2 = box
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    w, h = x2 - x1, y2 - y1

    if name == "comparison":
        cols = spec.get("columns", [])
        rows = spec.get("rows", [])
        n = max(len(cols), 1)
        cw = w / n
        rh = 36
        # column headers
        for i, c in enumerate(cols):
            pal = PAL_LIST[i % len(PAL_LIST)]
            d.rounded_rectangle([x1 + i * cw + 3, y1, x1 + (i + 1) * cw - 3, y1 + rh],
                                radius=10, fill=pal["hd"])
            d.text((x1 + i * cw + cw / 2, y1 + rh / 2), c[:30], font=F(FB, 20),
                   fill="white", anchor="mm")
        yy = y1 + rh + 6
        for ri, row in enumerate(rows):
            pal = PAL_LIST[ri % len(PAL_LIST)]
            maxlines = 1
            cell_lines = []
            for i in range(n):
                txt = row[i] if i < len(row) else ""
                ln = wrap(d, txt, F(FR, 17), cw - 24)
                cell_lines.append(ln)
                maxlines = max(maxlines, len(ln))
            ch = maxlines * 21 + 12
            for i in range(n):
                bg = pal["bg"] if ri % 2 == 0 else (255, 255, 255)
                d.rounded_rectangle([x1 + i * cw + 3, yy, x1 + (i + 1) * cw - 3, yy + ch],
                                    radius=8, fill=bg, outline=pal["bd"], width=2)
                for li, ln in enumerate(cell_lines[i]):
                    d.text((x1 + i * cw + 14, yy + 7 + li * 21), ln, font=F(FR, 17), fill=INK)
            yy += ch + 5
            if yy > y2 - 10:
                break

    elif name == "timeline":
        labels = spec.get("labels", [])
        n = max(len(labels), 1)
        d.line([(x1 + 40, cy - 10), (x2 - 40, cy - 10)], fill=accent, width=4)
        for i, lab in enumerate(labels):
            px = x1 + 40 + (w - 80) * (i / (n - 1) if n > 1 else 0.5)
            pal = PAL_LIST[i % len(PAL_LIST)]
            d.ellipse([px - 24, cy - 34, px + 24, cy + 14], fill=pal["bg"],
                      outline=pal["bd"], width=3)
            d.text((px, cy - 10), str(i + 1), font=F(FB, 22), fill=pal["hd"], anchor="mm")
            for li, ln in enumerate(wrap(d, lab, F(FR, 17), 150)):
                if li > 2: break
                d.text((px, cy + 32 + li * 22), ln, font=F(FR, 17), fill=INK, anchor="ma")

    elif name == "flow":
        labels = spec.get("labels", [])
        n = max(len(labels), 1)
        bw = (w - (n - 1) * 34) / n
        for i, lab in enumerate(labels):
            bx1 = x1 + i * (bw + 34)
            pal = PAL_LIST[i % len(PAL_LIST)]
            d.rounded_rectangle([bx1, cy - 52, bx1 + bw, cy + 52], radius=14,
                                fill=pal["bg"], outline=pal["bd"], width=3)
            ln = wrap(d, lab, F(FB, 19), bw - 16)
            ty = cy - (len(ln) - 1) * 13
            for li, t in enumerate(ln[:4]):
                d.text((bx1 + bw / 2, ty + li * 26), t, font=F(FB, 19),
                       fill=pal["hd"], anchor="mm")
            if i < n - 1:
                ax = bx1 + bw
                d.line([(ax + 4, cy), (ax + 30, cy)], fill=accent, width=4)
                d.polygon([(ax + 30, cy - 9), (ax + 30, cy + 9), (ax + 40, cy)], fill=accent)

    elif name == "cycle":
        labels = spec.get("labels", [])
        n = max(len(labels), 1)
        r = min(w, h) / 2 - 52
        for i, lab in enumerate(labels):
            a = -math.pi / 2 + 2 * math.pi * i / n
            px, py = cx + r * math.cos(a), cy + r * math.sin(a)
            pal = PAL_LIST[i % len(PAL_LIST)]
            d.ellipse([px - 52, py - 40, px + 52, py + 40], fill=pal["bg"],
                      outline=pal["bd"], width=3)
            ln = wrap(d, lab, F(FB, 17), 92)
            ty = py - (len(ln) - 1) * 11
            for li, t in enumerate(ln[:3]):
                d.text((px, ty + li * 22), t, font=F(FB, 17), fill=pal["hd"], anchor="mm")
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=accent)
        # direction arrows between circles
        for i in range(n):
            a1 = -math.pi / 2 + 2 * math.pi * i / n
            a2 = -math.pi / 2 + 2 * math.pi * (i + 1) / n
            am = (a1 + a2) / 2
            ax, ay = cx + (r + 52) * math.cos(am), cy + (r + 52) * math.sin(am)
            d.text((ax, ay), "\u25b6", font=F(FB, 16), fill=accent, anchor="mm")

    elif name == "pyramid":
        labels = spec.get("labels", [])
        n = max(len(labels), 1)
        top, bot = y1 + 6, y2 - 8
        for i, lab in enumerate(labels):
            ya = top + (bot - top) * i / n
            yb = top + (bot - top) * (i + 1) / n
            xa = cx - (w / 2 - 14) * (i / n)
            xb = cx + (w / 2 - 14) * (i / n)
            xc = cx - (w / 2 - 14) * ((i + 1) / n)
            xd = cx + (w / 2 - 14) * ((i + 1) / n)
            pal = PAL_LIST[i % len(PAL_LIST)]
            d.polygon([(xa, ya), (xb, ya), (xd, yb), (xc, yb)],
                      fill=pal["bg"], outline=pal["bd"], width=2)
            d.text((cx, (ya + yb) / 2), lab[:40], font=F(FB, 19), fill=pal["hd"], anchor="mm")

    elif name == "bars":
        labels = spec.get("labels", [])
        n = max(len(labels), 1)
        bw = (w - (n - 1) * 24) / n
        mx = y2 - 30
        for i, lab in enumerate(labels):
            bh = (h - 70) * (0.45 + 0.55 * (i + 1) / n)
            pal = PAL_LIST[i % len(PAL_LIST)]
            bx1 = x1 + i * (bw + 24)
            d.rectangle([bx1, mx - bh, bx1 + bw, mx], fill=pal["bg"],
                        outline=pal["bd"], width=2)
            d.text((bx1 + bw / 2, mx - bh - 12), lab[:16], font=F(FB, 17),
                   fill=pal["hd"], anchor="mm")

    elif name == "scale":
        labels = spec.get("labels", ["", ""])
        d.line([(cx, y1 + 8), (cx, y2 - 24)], fill=accent, width=5)
        d.line([(cx - 110, y1 + 24), (cx + 110, y1 + 24)], fill=accent, width=5)
        for sx in (cx - 110, cx + 110):
            lab = labels[0] if sx < cx and labels else (labels[1] if len(labels) > 1 else "")
            d.line([(sx, y1 + 24), (sx, y1 + 54)], fill=accent, width=3)
            d.arc([sx - 44, y1 + 36, sx + 44, y1 + 108], 0, 180, fill=accent, width=4)
            for li, ln in enumerate(wrap(d, lab, F(FB, 18), 170)):
                if li > 1: break
                d.text((sx, y1 + 118 + li * 24), ln, font=F(FB, 18), fill=INK, anchor="ma")
        d.polygon([(cx - 18, y2 - 24), (cx + 18, y2 - 24), (cx, y2 - 2)], fill=accent)

    elif name == "brain":
        d.ellipse([cx - 110, cy - 85, cx + 110, cy + 85], fill=(232, 244, 250),
                  outline=(150, 195, 220), width=4)
        for k in range(3):
            yy = cy - 45 + k * 45
            d.arc([cx - 85, yy - 32, cx + 85, yy + 32], 200, 340, fill=(30, 110, 160), width=4)
        d.line([(cx, cy - 85), (cx, cy + 85)], fill=(150, 195, 220), width=3)
        labels = spec.get("labels", [])
        for i, lab in enumerate(labels[:2]):
            sx = cx - 150 if i == 0 else cx + 150
            d.text((sx, cy), lab[:18], font=F(FB, 19), fill=INK, anchor="mm")

    else:  # venn / default: overlapping circles
        labels = spec.get("labels", [])
        r = min(w, h) / 3.2
        offs = [(-r * 0.9, r * 0.25), (r * 0.9, r * 0.25), (0, -r * 0.65)]
        for i in range(min(3, max(len(labels), 1))):
            ox, oy = offs[i]
            pal = PAL_LIST[i % len(PAL_LIST)]
            d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                      outline=pal["bd"], width=3)
            if i < len(labels):
                ln = wrap(d, labels[i], F(FB, 18), r * 1.5)
                ty = cy + oy - (len(ln) - 1) * 12
                for li, t in enumerate(ln[:3]):
                    d.text((cx + ox, ty + li * 24), t, font=F(FB, 18),
                           fill=pal["hd"], anchor="mm")

# ---------------- main render ----------------
def _card_fits(d, sec, x1, y1, x2, y2, fs):
    """Estimate content height for a card at font size fs. Returns (fits, lines_plan)."""
    maxw = (x2 - x1) - 34
    bf = F(FR, fs)
    lh = fs + 5
    cy = y1 + 56
    plan = []
    for blk in sec.get("blocks", []):
        label = blk.get("label", "")
        if label:
            cy += 38
        for it in blk.get("items", []):
            wlines = wrap(d, BULLET + it, bf, maxw)
            for li, ln in enumerate(wlines):
                plan.append((ln, li, bf))
                cy += lh
                if cy > y2 - 16:
                    return False, plan
        cy += 6
    return True, plan

def render_cheatsheet(spec, out_path, theme=None):
    import os as _os
    if theme is None:
        # workers set CHEATSHEET_THEME per category; no script edits needed
        theme = _os.environ.get("CHEATSHEET_THEME")
    th = THEMES.get(theme) if theme else None
    PAGE_BG = th["page_bg"] if th else "white"
    ACC_D = th["accent_dark"] if th else TEAL_DARK
    ACC = th["accent"] if th else TEAL
    ACC_L = th["accent_light"] if th else (210, 235, 235)
    THEME_CARDS = th["cards"] if th else None
    # normalize arrows everywhere: "->" becomes "→"
    def _arrows(o):
        if isinstance(o, dict):
            return {k: _arrows(v) for k, v in o.items()}
        if isinstance(o, list):
            return [_arrows(v) for v in o]
        if isinstance(o, str):
            return o.replace("->", "\u2192")
        return o
    spec = _arrows(spec)

    img = Image.new("RGB", (W, H), PAGE_BG)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 148], fill=ACC_D)
    tsize = 52
    tf = F(FB, tsize)
    while d.textlength(spec["title"], font=tf) > W - 400 and tsize > 28:
        tsize -= 4
        tf = F(FB, tsize)
    d.text((36, 30), spec["title"], font=tf, fill="white")
    d.text((38, 96), spec.get("subtitle", ""), font=F(FR, 28), fill=ACC_L)
    d.text((W - 30, 34), "Cheat Sheet", font=F(FB, 30), fill="white", anchor="ra")
    d.text((W - 30, 72), "Study Smart \u2022 Stay Healthy", font=F(FR, 20),
           fill=ACC_L, anchor="ra")

    # ---- body grid: 6 dense cards ----
    sections = spec["sections"][:6]
    n = len(sections)
    cols = 3 if n > 4 else (2 if n > 1 else 1)
    rows = math.ceil(n / cols)
    has_panel = bool(spec.get("diagram_panel"))
    panel_h = 340 if has_panel else 0
    top, bottom = 168, 1210 - panel_h
    gap = 14
    cw = (W - 36 - gap * (cols - 1)) / cols
    rh = (bottom - top - gap * (rows - 1)) / rows

    pkeys = list(PALETTE.keys())
    for idx, sec in enumerate(sections):
        r, c = divmod(idx, cols)
        x1 = 18 + c * (cw + gap)
        y1 = top + r * (rh + gap)
        x2, y2 = x1 + cw, y1 + rh
        if THEME_CARDS:
            pal = THEME_CARDS[idx % len(THEME_CARDS)]
        else:
            pal = PALETTE.get(sec.get("color"), PALETTE[pkeys[idx % len(pkeys)]])
        d.rounded_rectangle([x1, y1, x2, y2], radius=16, fill=pal["bg"],
                            outline=pal["bd"], width=2)
        # section title auto-fit so it never gets cut off
        stitle = f"{idx + 1}. {sec['title']}"
        sfs = 23
        sff = F(FB, sfs)
        while d.textlength(stitle, font=sff) > cw - 28 and sfs > 15:
            sfs -= 2
            sff = F(FB, sfs)
        d.text((x1 + 14, y1 + 12), stitle, font=sff, fill=pal["hd"])

        # auto-fit font so ALL data fits (never cut off)
        fs = 19
        fits, plan = _card_fits(d, sec, x1, y1, x2, y2, fs)
        while not fits and fs > 13:
            fs -= 1
            fits, plan = _card_fits(d, sec, x1, y1, x2, y2, fs)
        bf = F(FR, fs)
        lh = fs + 5
        maxw = cw - 34
        cy = y1 + 56
        for blk in sec.get("blocks", []):
            label = blk.get("label", "")
            if label:
                lf = F(FB, 18)
                tw = d.textlength(label, font=lf)
                icon = {"def": "\u25cf ", "points": "\u25ba ",
                        "example": "\u2713 ", "revision": "\u2605 "}.get(
                            blk.get("type", "points"), "")
                d.rounded_rectangle([x1 + 12, cy, x1 + 26 + tw + 26, cy + 30],
                                    radius=8, fill=(255, 255, 255), outline=pal["bd"])
                d.text((x1 + 20, cy + 15), icon + label, font=lf, fill=INK, anchor="lm")
                cy += 38
            for it in blk.get("items", []):
                wlines = wrap(d, BULLET + it, bf, maxw)
                for li, ln in enumerate(wlines):
                    if cy > y2 - 16:
                        break
                    xx = x1 + 18 + (0 if li == 0 else 16)
                    d.text((xx, cy), ln, font=bf, fill=INK)
                    cy += lh
            cy += 6

    # ---- full-width diagram panel ----
    if has_panel:
        dp = spec["diagram_panel"]
        px1, py1, px2, py2 = 18, 1210 - panel_h + 14, W - 18, 1210
        d.rounded_rectangle([px1, py1, px2, py2], radius=16, fill=PAGE_BG,
                            outline=ACC, width=3)
        d.text((px1 + 18, py1 + 10), "Visual Guide: " + dp.get("title", ""),
               font=F(FB, 23), fill=ACC_D)
        draw_big_diagram(d, dp.get("diagram", "flow"),
                         (px1 + 16, py1 + 52, px2 - 16, py2 - 12), dp, ACC)

    # ---- footer ----
    d.rectangle([0, 1226, W, H], fill=ACC_D)
    d.text((30, 1246), "\u2605 Most Important for MCQs & Long Questions:",
           font=F(FB, 22), fill="white")
    fitems = spec.get("footer", [])
    fx, fy = 30, 1280
    ff = F(FR, 20)
    for it in fitems:
        t = "\u2022 " + it + "   "
        tw = d.textlength(t, font=ff)
        if fx + tw > W - 210:
            fy += 28
            fx = 30
            if fy > 1320:
                break
        d.text((fx, fy), t, font=ff, fill=ACC_L)
        fx += tw
    d.text((W - 30, 1290), "Good Luck \u2661", font=F(FB, 26), fill="white", anchor="rm")

    img.save(out_path, "PNG")
