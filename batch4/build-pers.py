#!/usr/bin/env python3
"""Build 20 visual infographics for Personality Psychology."""
import json, textwrap, io, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
BG1 = "/home/hatch/workspace/zehen/batch4/inf-bg/media-generation-pers-bg1-0-b9944b45-f63d-4950-8180-071b63c4b23b.webp"
BG2 = "/home/hatch/workspace/zehen/batch4/inf-bg/media-generation-pers-bg2-0-296f81d8-106c-4fa8-ac63-188a401f5357.webp"
OUT = "/home/hatch/workspace/zehen/batch4/inf-out/"
os.makedirs(OUT, exist_ok=True)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

TERRA = (201, 111, 74)
CREAM = (253, 248, 240)
INK = (58, 46, 38)
SAGE = (122, 141, 118)
GOLD = (196, 158, 90)

TOPICS = [
 ("Big Five: Openness", BG1, [
   "Openness means how curious, creative, and imaginative you are.",
   "High openness: loves art, new ideas, and deep conversations.",
   "Low openness: prefers routine, familiar things, and practical facts.",
   "It is the strongest Big Five predictor of creativity.",
 ]),
 ("Big Five: Conscientiousness", BG2, [
   "Conscientiousness means being organized, responsible, and disciplined.",
   "Facets: orderliness, dutifulness, self-discipline, careful planning.",
   "It predicts job success better than any other Big Five trait.",
   "Too much can look like rigidity; too little like carelessness.",
 ]),
 ("Big Five: Extraversion", BG1, [
   "Extraversion means how outgoing, energetic, and sociable you are.",
   "Facets: gregariousness, assertiveness, warmth, excitement-seeking.",
   "Eysenck: introverts have higher baseline brain arousal, so they need less stimulation.",
   "Ambiverts sit in the middle and flex with the situation.",
 ]),
 ("Big Five: Agreeableness", BG2, [
   "Agreeableness means being kind, cooperative, and trusting.",
   "High scorers volunteer more and help others generously.",
   "Facets: trust, altruism, modesty, sympathy.",
   "Very high agreeableness can turn into people-pleasing.",
 ]),
 ("Big Five: Neuroticism", BG1, [
   "Neuroticism means how easily you feel anxiety, sadness, and anger.",
   "The brain's threat system reacts strongly; small problems feel big.",
   "Low neuroticism = calm, resilient, emotionally stable.",
   "It is the trait most linked to stress and mental-health risk.",
 ]),
 ("Freud's Structural Model", BG2, [
   "The id wants pleasure now — impulsive, childlike, demanding.",
   "The ego works on reality — plans, waits, and negotiates.",
   "The superego holds morals and ideals — the inner judge.",
   "A healthy personality = a strong ego balancing all three.",
 ]),
 ("Defense Mechanisms", BG1, [
   "Repression pushes painful memories out of awareness.",
   "Denial refuses to accept a hard reality.",
   "Projection sees your own feelings in other people.",
   "Mature defenses (humor, sublimation) protect without distorting reality.",
 ]),
 ("Jung: Archetypes", BG2, [
   "The Persona is the social mask we wear in public.",
   "The Shadow holds the parts of ourselves we reject.",
   "The collective unconscious stores shared human symbols.",
   "Individuation = integrating all parts into a whole self.",
 ]),
 ("Humanistic Personality", BG1, [
   "Rogers: we all need unconditional positive regard — love without conditions.",
   "The gap between real self and ideal self creates anxiety.",
   "Maslow: self-actualization is becoming your fullest self.",
   "Growth happens in acceptance, not judgment.",
 ]),
 ("Bandura: Social-Cognitive", BG2, [
   "Reciprocal determinism: person, behavior, and environment shape each other.",
   "The Bobo doll experiment proved we learn by watching others.",
   "We copy models who are similar, admired, and rewarded.",
   "You are shaped by your world — and you shape it back.",
 ]),
 ("Locus of Control", BG1, [
   "Internal locus: 'My effort decides my outcomes.'",
   "External locus: 'Luck and fate decide for me.'",
   "Internal locus predicts achievement and better health habits.",
   "Good news: an internal locus can be learned and strengthened.",
 ]),
 ("Self-Efficacy", BG2, [
   "Self-efficacy = belief you can succeed at a specific task.",
   "Strongest builder: mastery — past wins after real effort.",
   "Also built by role models, encouragement, and calm body states.",
   "High self-efficacy people persist longer and recover faster.",
 ]),
 ("The Dark Triad", BG1, [
   "Three overlapping dark traits: narcissism, Machiavellianism, psychopathy.",
   "Narcissists crave admiration and attention.",
   "Machiavellians manipulate strategically and stay cynical.",
   "Psychopathy adds impulsivity and low empathy.",
 ]),
 ("Narcissism: Two Faces", BG2, [
   "Grandiose narcissism: arrogant, dominant, exhibitionist.",
   "Vulnerable narcissism: shy, hypersensitive, secretly entitled.",
   "Both share a fragile self that needs constant validation.",
   "Confidence seeks no applause; narcissism cannot live without it.",
 ]),
 ("Healthy vs Fragile Self-Esteem", BG1, [
   "Healthy self-esteem is stable: 'I have strengths and flaws.'",
   "Fragile self-esteem depends on the latest win or compliment.",
   "Fragile self-esteem predicts defensiveness after criticism.",
   "Build it on values and effort, not on applause.",
 ]),
 ("MBTI: Uses and Criticisms", BG2, [
   "MBTI sorts people into 16 types from 4 letter pairs.",
   "Why popular? Flattering descriptions and a fun social experience.",
   "Problem: low test-retest reliability — many retest as a new type.",
   "Psychologists prefer the Big Five: traits as a spectrum, not boxes.",
 ]),
 ("Identity and Self-Concept", BG1, [
   "Identity answers 'Who am I?' Self-concept is all your self-beliefs.",
   "Marcia's statuses: diffusion, foreclosure, moratorium, achievement.",
   "Achievement — explored and committed — links to well-being.",
   "Identity is built by exploring, not by waiting.",
 ]),
 ("Culture and Personality", BG2, [
   "Individualist cultures praise standing out; collectivist cultures praise fitting in.",
   "Independent self: express inner traits. Interdependent self: honor relationships.",
   "The Big Five structure appears across cultures — a human universal.",
   "Culture shapes how traits are expressed, not whether they exist.",
 ]),
 ("Can Personality Change?", BG1, [
   "Yes — research shows traits shift gradually across life.",
   "Therapy reliably lowers neuroticism and raises extraversion.",
   "Behavior first: acting the trait consistently reshapes it.",
   "Change is slow and intentional — but real.",
 ]),
 ("Projective Tests", BG2, [
   "Rorschach inkblots: 'What do you see?' reveals inner patterns.",
   "TAT: telling stories about pictures exposes motives and fears.",
   "Modern scoring (R-PAS) made results more reliable.",
   "Fascinating tools — but debated as clinical evidence.",
 ]),
]

def fit_font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def build(title, bg_path, points, idx):
    bg = Image.open(bg_path).convert("RGB")
    # cover-resize to 1080x1350
    r = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * r) + 1, int(bg.height * r) + 1), Image.LANCZOS)
    x = (bg.width - W) // 2; y = (bg.height - H) // 2
    img = bg.crop((x, y, x + W, y + H))

    # top gradient for title legibility
    grad = Image.new("L", (1, 520))
    for i in range(520):
        grad.putpixel((0, i), int(150 * (1 - i / 520) ** 1.4))
    grad = grad.resize((W, 520))
    dark = Image.new("RGB", (W, 520), (24, 18, 12))
    img.paste(dark, (0, 0), grad)

    d = ImageDraw.Draw(img, "RGBA")
    f_badge = fit_font(FB, 30)
    f_title = fit_font(FB, 62)
    f_pt = fit_font(FR, 29)
    f_brand = fit_font(FB, 26)

    # badge pill
    badge = "PERSONALITY PSYCHOLOGY"
    bw = d.textlength(badge, font=f_badge) + 56
    d.rounded_rectangle([60, 64, 60 + bw, 64 + 62], radius=31, fill=TERRA + (255,))
    d.text((60 + 28, 64 + 14), badge, font=f_badge, fill=CREAM + (255,))

    # title (2 lines max)
    lines = wrap(d, title, f_title, W - 120)
    ty = 160
    for ln in lines[:2]:
        d.text((60, ty), ln, font=f_title, fill=CREAM + (255,))
        ty += 76

    # bottom cream panel
    panel_top = 600
    d.rounded_rectangle([0, panel_top, W, H], radius=0, fill=CREAM + (242,))
    # gold accent bar
    d.rectangle([0, panel_top, W, panel_top + 10], fill=GOLD + (255,))

    py = panel_top + 56
    for i, pt in enumerate(points):
        # number circle
        d.ellipse([60, py, 116, py + 56], fill=TERRA + (255,))
        num = str(i + 1)
        nw = d.textlength(num, font=fit_font(FB, 30))
        d.text((60 + (56 - nw) / 2, py + 10), num, font=fit_font(FB, 30), fill=CREAM + (255,))
        plines = wrap(d, pt, f_pt, W - 240)
        ly = py + 2
        for ln in plines[:2]:
            d.text((140, ly), ln, font=f_pt, fill=INK + (255,))
            ly += 40
        py = ly + 30

    # brand footer
    brand = "M Y S T E R I O U S"
    bw2 = d.textlength(brand, font=f_brand)
    d.text(((W - bw2) / 2, H - 76), brand, font=f_brand, fill=SAGE + (255,))

    out = os.path.join(OUT, f"pers-{idx}.png")
    img.save(out, "PNG")
    return out

made = []
for i, (title, bg, pts) in enumerate(TOPICS, start=1):
    p = build(title, bg, pts, i)
    made.append(p)
    print("built", p)

print("DONE", len(made))
