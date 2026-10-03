#!/usr/bin/env python3
"""Generate 20 visual infographics for Research Methods & Statistics."""
import json, os, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
BG_DIR = "/home/hatch/workspace/zehen/batch4/inf-bg"
OUT_DIR = "/home/hatch/workspace/zehen/batch4/inf-res-out"
os.makedirs(OUT_DIR, exist_ok=True)

BG1 = f"{BG_DIR}/media-generation-res-bg1-0-0114271e-d04d-440d-b6bb-1347fa788e4c.webp"
BG2 = f"{BG_DIR}/media-generation-res-bg2-0-c567da31-62ea-48d0-9fb6-f046125d6ac7.webp"

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

TERRA = (201, 111, 74)
CREAM = (253, 248, 240)
DARK = (43, 30, 24)

TOPICS = [
 ("Variables: IV, DV and Confounds", [
  "The IV is what the researcher changes; the DV is what gets measured.",
  "A confound is a hidden extra variable that ruins the experiment.",
  "Operational definitions state exactly how each variable is measured.",
  "Control variables are held constant so they cannot interfere.",
 ]),
 ("Hypotheses and Theories", [
  "A hypothesis is a clear, testable prediction about two variables.",
  "Good hypotheses can be proven wrong — that is their strength.",
  "A theory is a big, well-supported explanation, not a guess.",
  "The null hypothesis predicts no effect; research tries to reject it.",
 ]),
 ("Experimental Design Basics", [
  "Experiments manipulate one variable to test cause and effect.",
  "A control group gives a baseline to compare against.",
  "Random assignment balances out participant differences.",
  "Double-blind procedures stop bias from both sides.",
 ]),
 ("Correlational Research", [
  "Correlation shows how two variables move together — not cause.",
  "A correlation of +1.0 or -1.0 is perfect; 0 means no link.",
  "Third variables can explain a correlation away.",
  "Correlations predict well but prove cause poorly.",
 ]),
 ("Survey Methods", [
  "Surveys collect self-reported data from large groups fast.",
  "Random sampling makes results represent the whole population.",
  "Wording matters — leading questions bias answers.",
  "Low response rates can quietly distort the findings.",
 ]),
 ("Case Studies", [
  "A case study is a deep dive into one person, group, or event.",
  "They reveal rare conditions and spark new hypotheses.",
  "Findings cannot be generalized to everyone.",
  "Researcher bias is a real risk in interpretation.",
 ]),
 ("Naturalistic Observation", [
  "Behavior is watched in its natural setting, undisturbed.",
  "High ecological validity — real life, not a lab.",
  "No control over variables; cause cannot be proven.",
  "Observer presence can change behavior (reactivity).",
 ]),
 ("Sampling Methods", [
  "A sample should represent the population it comes from.",
  "Random sampling gives everyone an equal chance.",
  "Convenience samples are easy but biased.",
  "Larger samples give more trustworthy results.",
 ]),
 ("Random Assignment", [
  "Participants join groups by chance, like a coin flip.",
  "It balances age, ability and mood across groups automatically.",
  "The larger the sample, the better it works.",
  "It is what lets experiments show cause and effect.",
 ]),
 ("Internal Validity", [
  "Internal validity = can we trust the cause-effect claim?",
  "Confounds are its biggest enemy.",
  "Control groups, blinding and random assignment protect it.",
  "High control helps here but can feel artificial.",
 ]),
 ("External Validity", [
  "External validity = do findings apply to the real world?",
  "Lab studies can be too artificial to generalize.",
  "Representative samples and natural settings help.",
  "It often trades off against internal validity.",
 ]),
 ("Reliability Types", [
  "Reliability means consistent results every time.",
  "Test-retest: same test, same person, similar scores.",
  "Inter-rater: different observers agree with each other.",
  "A test can be reliable yet measure the wrong thing.",
 ]),
 ("Central Tendency: Mean, Median, Mode", [
  "The mean is the average — sensitive to extreme scores.",
  "The median is the middle value — best for skewed data.",
  "The mode is simply the most common score.",
  "Report the median when outliers distort the mean.",
 ]),
 ("Variability: Range, Variance, SD", [
  "Variability shows how spread out scores are.",
  "Range is max minus min — quick but crude.",
  "Standard deviation is the average distance from the mean.",
  "Low SD means scores cluster tightly together.",
 ]),
 ("Normal Distribution", [
  "The bell curve: most scores pile in the middle.",
  "It is symmetric — mean, median and mode are equal.",
  "About 68% of scores fall within one SD of the mean.",
  "Many traits like height and IQ roughly follow it.",
 ]),
 ("Correlation Coefficients", [
  "r ranges from -1.00 to +1.00.",
  "The sign shows direction; the number shows strength.",
  "r = .80 is strong; r = .20 is weak.",
  "Never confuse correlation with causation.",
 ]),
 ("P-Values Explained Simply", [
  "p < .05 means the result would be rare by pure chance.",
  "It does NOT mean the finding is important or large.",
  "p-values depend on sample size — big samples find tiny effects.",
  "Always pair p-values with effect sizes.",
 ]),
 ("T-Tests Explained Simply", [
  "A t-test compares the means of two groups.",
  "It asks: is this difference real or just luck?",
  "Independent t-test: two separate groups; paired: same people twice.",
  "It needs roughly normal data and similar variability.",
 ]),
 ("Effect Sizes", [
  "Effect size tells how big a difference really is.",
  "Cohen's d: 0.2 = small, 0.5 = medium, 0.8 = large.",
  "Big samples can make tiny effects 'significant' — check size!",
  "It is the most honest number in a results section.",
 ]),
 ("Research Ethics in Depth", [
  "Informed consent: participants must agree knowingly.",
  "Deception is allowed only when essential and harmless.",
  "Debriefing explains the true purpose afterward.",
  "Confidentiality protects participants' identities always.",
 ]),
]

def fit_font(text, path, start, max_w, draw):
    size = start
    while size > 20:
        f = ImageFont.truetype(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 4
    return ImageFont.truetype(path, 20)

def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def gradient(size, top_alpha, bot_alpha, color=DARK):
    g = Image.new("L", (1, size[1]), 0)
    px = g.load()
    for y in range(size[1]):
        t = y / max(1, size[1] - 1)
        px[0, y] = int(top_alpha + (bot_alpha - top_alpha) * t)
    g = g.resize(size)
    solid = Image.new("RGB", size, color)
    return solid, g

def round_rect(d, xy, r, fill):
    d.rounded_rectangle(xy, radius=r, fill=fill)

def make(title, points, bg_path, out_path):
    bg = Image.open(bg_path).convert("RGB")
    # cover-crop to 1080x1350
    sr, tr = bg.width / bg.height, W / H
    if sr > tr:
        nh = H; nw = int(bg.width * H / bg.height)
    else:
        nw = W; nh = int(bg.height * W / bg.width)
    bg = bg.resize((nw, nh), Image.LANCZOS)
    x = (nw - W) // 2; y = (nh - H) // 2
    bg = bg.crop((x, y, x + W, y + H))

    # warm dark gradient: strong at top, medium at bottom
    ov = Image.new("RGB", (W, H), DARK)
    mask = Image.new("L", (1, H), 0); px = mask.load()
    for yy in range(H):
        t = yy / (H - 1)
        # top 0-40%: 200->150, mid: 150->90, bottom: 90->170
        if t < 0.42: a = 205 - 60 * (t / 0.42)
        elif t < 0.75: a = 145 - 60 * ((t - 0.42) / 0.33)
        else: a = 85 + 95 * ((t - 0.75) / 0.25)
        px[0, yy] = int(max(0, min(255, a)))
    mask = mask.resize((W, H))
    img = Image.composite(ov, bg, mask)
    d = ImageDraw.Draw(img)

    # badge
    badge_txt = "RESEARCH METHODS & STATISTICS"
    fb_badge = ImageFont.truetype(FB, 30)
    bw = d.textlength(badge_txt, font=fb_badge) + 56
    bx = (W - bw) // 2; by = 64
    round_rect(d, [bx, by, bx + bw, by + 58], 29, TERRA + (255,))
    d.text((W / 2, by + 29), badge_txt, font=fb_badge, fill=CREAM, anchor="mm")

    # title
    ty = by + 110
    ft = fit_font(title, FB, 68, W - 140, d)
    lines = wrap(d, title, ft, W - 140)
    for ln in lines:
        d.text((W / 2, ty), ln, font=ft, fill=CREAM, anchor="ma")
        ty += ft.size + 12
    # accent line
    d.rounded_rectangle([W/2 - 60, ty + 6, W/2 + 60, ty + 12], radius=3, fill=TERRA)

    # points cards
    py = ty + 44
    card_h = 148
    fb_num = ImageFont.truetype(FB, 34)
    fp = ImageFont.truetype(FR, 30)
    for i, pt in enumerate(points):
        # card bg: translucent dark
        card = Image.new("RGB", (W - 120, card_h), (58, 40, 32))
        cmask = Image.new("L", (W - 120, card_h), 165)
        img.paste(card, (60, py), cmask)
        dd = ImageDraw.Draw(img)
        dd.rounded_rectangle([60, py, W - 60, py + card_h], radius=22, outline=TERRA, width=3)
        # number circle
        cx, cy = 60 + 52, py + card_h // 2
        dd.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=TERRA)
        dd.text((cx, cy), str(i + 1), font=fb_num, fill=CREAM, anchor="mm")
        # point text wrapped
        plines = wrap(dd, pt, fp, W - 120 - 150)
        sty = py + (card_h - len(plines) * 40) // 2 + 8
        for ln in plines[:3]:
            dd.text((60 + 118, sty), ln, font=fp, fill=CREAM, anchor="la")
            sty += 40
        py += card_h + 22

    # footer
    ff = ImageFont.truetype(FB, 34)
    d.text((W / 2, H - 78), "M Y S T E R I O U S", font=ff, fill=CREAM, anchor="mm")
    d.text((W / 2, H - 40), "learn the mind, one day at a time", font=ImageFont.truetype(FR, 24), fill=(220, 200, 180), anchor="mm")

    img.save(out_path, "PNG")
    return out_path

made = []
for i, (title, pts) in enumerate(TOPICS):
    bg = BG1 if i % 2 == 0 else BG2
    out = f"{OUT_DIR}/res-{i+1:02d}.png"
    make(title, pts, bg, out)
    made.append((f"res-{i+1:02d}.png", title))
    print("made", out)

print("TOTAL", len(made))
