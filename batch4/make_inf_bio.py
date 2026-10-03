#!/usr/bin/env python3
"""Composite 20 Biological Psychology visual infographics (1080x1350 PNG)."""
import json, os, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
OUT = '/home/hatch/workspace/zehen/batch4/inf-bio-out'
BG1 = '/home/hatch/workspace/zehen/batch4/inf-bg/media-generation-bio-bg1-0-b9671d0a-7a68-4e6e-be0a-7bdf21d2ea77.webp'
BG2 = '/home/hatch/workspace/zehen/batch4/inf-bg/media-generation-bio-bg2-0-66ffe133-5d85-4efb-ba43-5fe50203e592.webp'
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

os.makedirs(OUT, exist_ok=True)

f_title = ImageFont.truetype(FB, 62)
f_badge = ImageFont.truetype(FB, 26)
f_point = ImageFont.truetype(FR, 31)
f_wm = ImageFont.truetype(FB, 24)

TERRA = (201, 111, 74)

TOPICS = [
 ("The Neuron in Depth", [
   "Your brain holds about 86 billion neurons — its communication units.",
   "Dendrites receive signals; the axon sends them out.",
   "The myelin sheath insulates axons and speeds signals up.",
   "Glial cells support, nourish, and protect neurons.",
   "Neurons talk through electrical and chemical signals."]),
 ("Action Potential Explained", [
   "Resting potential sits at about -70 millivolts.",
   "A stimulus must pass the -55 mV threshold to fire.",
   "Sodium rushes in, spiking the charge to +40 mV.",
   "The neuron then resets — ready to fire again.",
   "It is all-or-nothing: weak signals fire nothing."]),
 ("Synapses and Neurotransmission", [
   "The synapse is the junction between two neurons.",
   "Calcium triggers vesicles to release neurotransmitters.",
   "Chemicals cross the gap and bind like keys in locks.",
   "Each receptor accepts only specific chemicals.",
   "Unused chemicals are recycled or broken down."]),
 ("Serotonin: Mood and More", [
   "Serotonin regulates mood, sleep, appetite, and pain.",
   "Low serotonin links to depression and anxiety.",
   "SSRIs keep more serotonin active in synapses.",
   "It is made from the amino acid tryptophan.",
   "Sunlight and exercise naturally boost it."]),
 ("Dopamine: Reward and Motivation", [
   "Dopamine fires for rewards — food, praise, surprises.",
   "It responds most to unexpected rewards.",
   "It fuels \"wanting\" more than \"liking.\"",
   "This drives addiction: craving without pleasure.",
   "The mesolimbic pathway is the reward highway."]),
 ("Brain Lobes and Functions", [
   "Frontal lobe: planning, decisions, personality.",
   "Parietal lobe: touch, space, and math.",
   "Temporal lobe: hearing and memory.",
   "Occipital lobe: vision processing.",
   "Broca's area (frontal) produces speech."]),
 ("The Limbic System", [
   "A deep ring handling emotion and memory.",
   "The amygdala is the brain's threat detector.",
   "The hippocampus forms new memories.",
   "Smell connects straight to it — bypassing logic.",
   "Damage here disrupts fear and memory."]),
 ("Neuroplasticity", [
   "The brain rewires itself with experience.",
   "\"Neurons that fire together, wire together\" (Hebb).",
   "Learning physically changes brain structure.",
   "Lost senses get reallocated — the brain hates waste.",
   "It works across the whole lifespan."]),
 ("Split-Brain Research", [
   "Sperry and Gazzaniga cut the corpus callosum for epilepsy.",
   "Left hemisphere: language, logic, analysis.",
   "Right hemisphere: faces, music, spatial skills.",
   "Each half can work independently.",
   "It proved the brain has specialized halves."]),
 ("Brain Development", [
   "Neurons are born, migrate, then connect.",
   "Up to 50% of neurons are pruned away — sculpting.",
   "Adolescence prunes unused links: \"use it or lose it.\"",
   "The prefrontal cortex matures last (mid-20s).",
   "Experience literally shapes the growing brain."]),
 ("Twin and Adoption Studies", [
   "Identical twins share 100% of genes; fraternal ~50%.",
   "The Minnesota study tracked twins raised apart.",
   "Intelligence heritability: roughly 50-80%.",
   "Personality heritability: roughly 40-50%.",
   "Genes matter — but so does environment."]),
 ("The Endocrine System", [
   "Glands release hormones into the bloodstream.",
   "Slower than nerves, but longer-lasting.",
   "The pituitary is the \"master gland.\"",
   "The thyroid sets your metabolic speed.",
   "Hormones shape mood, growth, and stress."]),
 ("Hormones and Behavior", [
   "Cortisol is the main stress hormone.",
   "Chronic cortisol damages the hippocampus.",
   "Oxytocin boosts trust and bonding.",
   "Testosterone links to competitiveness.",
   "Behavior changes hormones too — both ways."]),
 ("Hunger and Eating Regulation", [
   "Ghrelin (empty stomach) signals hunger.",
   "Leptin (fat cells) signals fullness.",
   "The hypothalamus is the appetite control room.",
   "Leptin resistance drives persistent hunger in obesity.",
   "Sleep and stress both affect appetite."]),
 ("Sleep Neuroscience", [
   "The SCN is the brain's 24-hour master clock.",
   "Blue light suppresses melatonin — delays sleep.",
   "We cycle N1, N2, N3, REM 4-6 times nightly.",
   "Deep sleep restores the body; REM restores the mind.",
   "Sleep loss harms memory, mood, and immunity."]),
 ("Emotion and the Brain", [
   "The amygdala feels fear before you know why.",
   "The prefrontal cortex calms the amygdala down.",
   "James-Lange: we feel sad because we cry.",
   "Facial feedback: smiling can lift mood.",
   "Stronger prefrontal links = better control."]),
 ("Memory and the Brain", [
   "The hippocampus forms new explicit memories.",
   "H.M.'s surgery proved formation is not storage.",
   "The amygdala tags emotional memories strongly.",
   "Habits live in the basal ganglia.",
   "Skills live in the cerebellum."]),
 ("Stress Physiology (HPA Axis)", [
   "Hypothalamus, pituitary, adrenals release cortisol.",
   "Selye's stages: alarm, resistance, exhaustion.",
   "Short stress is adaptive; chronic stress harms.",
   "Cortisol frees energy and heightens alertness.",
   "The alarm must switch off to stay healthy."]),
 ("Brain Imaging Techniques", [
   "EEG: superb timing, blurry location.",
   "CT: fast 3D X-ray slices — great for trauma.",
   "MRI: exquisite detail, no radiation.",
   "fMRI tracks blood flow — shows the brain working.",
   "PET uses tracers to map brain activity."]),
 ("Psychopharmacology Basics", [
   "Agonists boost transmitters; antagonists block them.",
   "SSRIs raise serotonin fast; mood lifts in 2-6 weeks.",
   "Healing comes from downstream brain changes.",
   "Antipsychotics block dopamine D2 receptors.",
   "Newer drugs balance benefits, fewer side effects."]),
]

NUM = ['\u2460', '\u2461', '\u2462', '\u2463', '\u2464']  # ①②③④⑤

def cover_crop(im, w, h):
    sr = im.width / im.height
    tr = w / h
    if sr > tr:
        nh = h; nw = int(nh * sr)
    else:
        nw = w; nh = int(nw / sr)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = (nw - w) // 2; y = (nh - h) // 2
    return im.crop((x, y, x + w, y + h))

def gradient_overlay(w, h):
    ov = Image.new('L', (1, h), 0)
    px = ov.load()
    for y in range(h):
        a_top = max(0, 200 - int(200 * y / 420)) if y < 420 else 0
        a_bot = max(0, 215 - int(215 * (h - y) / 620)) if (h - y) < 620 else 0
        px[0, y] = max(a_top, a_bot)
    ov = ov.resize((w, h))
    black = Image.new('RGB', (w, h), (0, 0, 0))
    return Image.composite(black, Image.new('RGB', (w, h), (0, 0, 0)), ov), ov

def draw_shadow_text(d, xy, text, font, fill, anchor='la'):
    x, y = xy
    for ox, oy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1)]:
        d.text((x + ox, y + oy), text, font=font, fill=(0, 0, 0, 200), anchor=anchor)
    d.text((x, y), text, font=font, fill=fill, anchor=anchor)

def wrap(text, font, d, max_w):
    words, lines, cur = text.split(), [], ''
    for wd in words:
        t = (cur + ' ' + wd).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = wd
    if cur: lines.append(cur)
    return lines

def make_one(idx, title, points, bg_path, out_path):
    bg = Image.open(bg_path).convert('RGB')
    bg = cover_crop(bg, W, H)
    # slight darken for cohesion
    bg = Image.blend(bg, Image.new('RGB', (W, H), (10, 8, 6)), 0.12)
    ov_img, alpha = gradient_overlay(W, H)
    bg = Image.composite(ov_img, bg, alpha)

    d = ImageDraw.Draw(bg, 'RGBA')

    # badge
    label = 'BIOLOGICAL PSYCHOLOGY'
    bw = d.textlength(label, font=f_badge) + 56
    bx, by = (W - bw) // 2, 56
    d.rounded_rectangle([bx, by, bx + bw, by + 52], radius=26, fill=TERRA + (235,))
    d.text((W // 2, by + 26), label, font=f_badge, fill=(255, 255, 255), anchor='mm')

    # title
    lines = wrap(title, f_title, d, W - 160)
    ty = 150
    for ln in lines:
        draw_shadow_text(d, (W // 2, ty), ln, f_title, (255, 255, 255), anchor='ma')
        ty += 76

    # points
    py = 640
    for i, pt in enumerate(points):
        plines = wrap(pt, f_point, d, W - 220)
        # number badge
        d.ellipse([90, py - 6, 134, py + 38], fill=TERRA + (235,))
        d.text((112, py + 16), NUM[i], font=f_point, fill=(255, 255, 255), anchor='mm')
        lx = 160
        for ln in plines:
            draw_shadow_text(d, (lx, py), ln, f_point, (255, 255, 255))
            py += 44
        py += 26

    # watermark
    d.text((W // 2, H - 48), 'M Y S T E R I O U S', font=f_wm, fill=(255, 255, 255, 170), anchor='mm')

    bg.save(out_path, 'PNG')
    return out_path

for i, (title, pts) in enumerate(TOPICS):
    n = i + 1
    bg = BG1 if n % 2 == 1 else BG2
    out = os.path.join(OUT, f'bio-{n}.png')
    make_one(n, title, pts, bg, out)
    print('made', out, os.path.getsize(out) // 1024, 'KB')
print('DONE', len(TOPICS))
