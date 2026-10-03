#!/usr/bin/env python3
"""Build 20 visual infographics for Cognitive Psychology."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import textwrap, os

W, H = 1080, 1350
BG_DIR = "/home/hatch/workspace/zehen/batch4/inf-bg"
OUT_DIR = "/home/hatch/workspace/zehen/batch4/inf-out"
os.makedirs(OUT_DIR, exist_ok=True)
BG1 = f"{BG_DIR}/media-generation-cog-bg1-0-6da6a5da-f1be-493c-936e-b91652a2eeda.webp"
BG2 = f"{BG_DIR}/media-generation-cog-bg2-0-e09a74d8-4013-4820-b379-3d042a27c027.webp"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

GOLD = (232, 184, 109)
WHITE = (255, 255, 255)
CREAM = (253, 246, 236)

TOPICS = [
 ("Attention and Selective Focus", [
   "Selective attention: focus on one input, ignore the rest (Cherry, 1953)",
   "Cocktail party effect: your name cuts through any crowd noise",
   "Multitasking is a myth — divided attention tanks performance",
   "Inattentional blindness: we miss the obvious when focused elsewhere",
   "Vigilance fades — focus drops during long, boring tasks"]),
 ("Working Memory in Depth", [
   "Working memory is your mental workspace — active for seconds",
   "Baddeley's model (1974): sketchpad, loop, central executive",
   "Miller's 7±2: chunking beats the capacity limit",
   "Without rehearsal it fades in 15–30 seconds (Peterson & Peterson)",
   "The central executive directs attention and switches tasks"]),
 ("Long-Term Memory Systems", [
   "Explicit memory: conscious facts (semantic) and events (episodic)",
   "Implicit memory: unconscious skills like riding a bike",
   "Priming: recent exposure quietly shapes what you notice next",
   "Encoding specificity (Tulving): match learning and test conditions",
   "Deep processing (Craik & Lockhart, 1972) builds stronger memories"]),
 ("Forgetting: Theories and Research", [
   "Ebbinghaus (1885): the forgetting curve drops steeply within hours",
   "Interference: old learning blocks new, and new blocks old",
   "Retrieval failure: the memory exists — the cue is missing",
   "Decay: unused memories fade like unwalked paths",
   "Motivated forgetting: painful memories get pushed away"]),
 ("False Memories and Eyewitness Testimony", [
   "Misinformation effect (Loftus, 1978): false details weave into real memories",
   "Leading questions distort what witnesses 'remember'",
   "Entire false memories can be implanted by suggestion",
   "Source misattribution: remembering the fact, forgetting the source",
   "Confidence does NOT equal accuracy in eyewitness testimony"]),
 ("Amnesia: Case Studies (H.M.)", [
   "H.M. lost the ability to form new memories after brain surgery",
   "His procedural memory survived — skills without remembering learning",
   "Clive Wearing lives in a permanent present of seconds",
   "Infantile amnesia: the maturing hippocampus can't store early childhood",
   "Different amnesias prove memory is many systems, not one"]),
 ("Language Acquisition", [
   "Universal stages: cooing → babbling → first words → sentences",
   "Overregularization ('goed') proves children learn rules, not imitation",
   "Critical period: language needs childhood for full mastery",
   "Chomsky's Language Acquisition Device: an inborn grammar capacity",
   "Motherese (child-directed speech) appears in every culture"]),
 ("Bilingualism and the Brain", [
   "Code-switching follows strict rules — a sign of skill, not confusion",
   "Early bilinguals process both languages in overlapping brain areas",
   "Cognitive reserve: bilingualism may delay dementia symptoms",
   "Trade-off: smaller vocabularies per language, slower retrieval",
   "Managing two languages exercises executive control daily"]),
 ("Concepts and Categories", [
   "Prototype theory (Rosch, 1975): categories center on a 'best example'",
   "Real categories are fuzzy — is a tomato a fruit or a vegetable?",
   "Exemplar theory: we judge by similarity to stored examples",
   "Basic-level categories (dog) are learned first and used most",
   "Children overextend categories, then narrow them with experience"]),
 ("Cognitive Biases Collection", [
   "Confirmation bias: we seek what supports what we already believe",
   "Anchoring: the first number drags every later judgment (Tversky & Kahneman)",
   "Availability heuristic: vivid examples feel more common than they are",
   "All three spring from fast, automatic System 1 thinking (Kahneman)",
   "Checklists and structure fight bias in medicine and beyond"]),
 ("Creativity and Divergent Thinking", [
   "Divergent thinking generates many answers; convergent narrows to one",
   "Wallas (1926): preparation → incubation → illumination → verification",
   "Functional fixedness: familiar uses block creative solutions",
   "Intrinsic motivation fuels creativity; expected rewards can crush it",
   "Deliberate practice builds the expertise creativity needs"]),
 ("Mental Imagery", [
   "Mental images work like real pictures (Kosslyn's scanning studies)",
   "Mental rotation time grows with angle (Shepard & Metzler, 1971)",
   "Method of loci: bizarre images along a route supercharge memory",
   "Athletes improve by vividly imagining perfect performance",
   "Aphantasia: some people form no voluntary mental images at all"]),
 ("Executive Functions", [
   "The brain's control panel: inhibition, shifting, updating",
   "The prefrontal cortex matures into the mid-twenties",
   "Marshmallow test: childhood self-control predicted later outcomes",
   "Executive dysfunction is central to ADHD",
   "Phineas Gage (1848): prefrontal damage changed his personality"]),
 ("Metacognition: Thinking About Thinking", [
   "Metacognition monitors and controls your own learning",
   "Tip-of-the-tongue states show we sense what we 'know'",
   "Dunning-Kruger: the least skilled are the most overconfident",
   "Testing effect: retrieval practice beats re-reading",
   "Study what you don't know — not what's comfortable"]),
 ("Cognitive Load Theory", [
   "Working memory is tiny — teaching must respect its limits (Sweller, 1988)",
   "Worked examples beat unguided struggle for novices",
   "Split-attention: separated information wastes mental effort",
   "Spoken words + visuals expand effective capacity",
   "Expertise reversal: novice techniques can hinder experts"]),
 ("Decision Making Under Risk", [
   "Prospect Theory (Kahneman & Tversky, 1979): losses loom larger than gains",
   "Framing effects: wording flips choices on identical options",
   "Diminishing sensitivity: we judge by proportions, not amounts",
   "Endowment effect: owning something inflates its value",
   "Status quo bias: we cling to the current state"]),
 ("Face Perception and Recognition", [
   "The fusiform face area (FFA) specializes in faces",
   "Prosopagnosia: face blindness, separate from object vision",
   "Inversion effect: upside-down faces are uniquely hard to recognize",
   "Own-race bias is one of psychology's most replicated findings",
   "Babies prefer faces from birth — an inborn bias"]),
 ("Visual Illusions Explained", [
   "Müller-Lyer: arrow fins distort perceived length",
   "Ebbinghaus illusion: size is judged relative to surroundings",
   "Waterfall aftereffect reveals direction-selective neurons",
   "Shepard's tables: 3D interpretation overrides 2D reality",
   "Ames room: one peephole makes a trapezoid look rectangular"]),
 ("Memory Improvement Techniques", [
   "Method of loci: the ancient memory palace technique",
   "Testing effect: retrieval strengthens more than restudying",
   "Spacing effect (Ebbinghaus): distribute practice over time",
   "Elaborative encoding: ask 'why' and 'how' to build connections",
   "Protégé effect: teaching forces true understanding"]),
 ("Artificial Intelligence and Human Thinking", [
   "Turing test (1950): can a machine converse indistinguishably?",
   "Chinese Room: symbol manipulation isn't understanding",
   "Neural networks loosely copy brain architecture",
   "Children learn from tiny data and ask 'why' — AI needs mountains",
   "AI inherits human biases from its training data"]),
]

def wrap(text, font, max_w, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def shadow_text(draw, xy, text, font, fill, anchor="la"):
    x, y = xy
    draw.text((x+2, y+3), text, font=font, fill=(0,0,0,180), anchor=anchor)
    draw.text((x, y), text, font=font, fill=fill, anchor=anchor)

def build(idx, title, points, bg_path, out_path):
    bg = Image.open(bg_path).convert("RGB")
    # cover 1080x1350
    scale = W / bg.width
    bg = bg.resize((W, int(bg.height * scale)), Image.LANCZOS)
    top = max(0, (bg.height - H) // 2)
    bg = bg.crop((0, top, W, top + H))
    # slight dim for cohesion
    bg = ImageEnhance.Brightness(bg).enhance(0.92)

    img = bg.convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")
    # top gradient (title zone) — light, lets artwork show
    for y in range(0, 420):
        a = int(105 * (1 - y/420) ** 1.3)
        draw.line([(0, y), (W, y)], fill=(10, 8, 14, a))
    # bottom gradient (points zone) — starts lower, artwork visible in middle
    for y in range(760, H):
        t = (y - 760) / (H - 760)
        a = int(185 * t ** 0.85)
        draw.line([(0, y), (W, y)], fill=(8, 6, 12, a))

    f_badge = ImageFont.truetype(FB, 30)
    f_title = ImageFont.truetype(FB, 62)
    f_pt = ImageFont.truetype(FR, 30)
    f_foot = ImageFont.truetype(FB, 30)

    # badge
    badge = "C O G N I T I V E   P S Y C H O L O G Y"
    bw = draw.textlength(badge, font=f_badge)
    shadow_text(draw, ((W-bw)/2, 64), badge, f_badge, GOLD, anchor="la")
    # gold rule under badge
    draw.line([(W/2-120, 118), (W/2+120, 118)], fill=GOLD+(255,), width=3)

    # title (wrapped, centered)
    lines = wrap(title, f_title, W-140, draw)
    y = 150
    for ln in lines:
        lw = draw.textlength(ln, font=f_title)
        shadow_text(draw, ((W-lw)/2, y), ln, f_title, WHITE)
        y += 76

    # points
    y = max(y + 40, 790)
    bullet = "✦ "
    for p in points:
        plines = wrap(bullet + p, f_pt, W-170, draw)
        for j, ln in enumerate(plines):
            if j == 0:
                # gold bullet
                shadow_text(draw, (85, y), "✦", f_pt, GOLD)
                shadow_text(draw, (125, y), ln[len(bullet):], f_pt, WHITE)
            else:
                shadow_text(draw, (125, y), ln, f_pt, WHITE)
            y += 42
        y += 14

    # footer watermark (below points, clear of text)
    y = max(y + 26, H - 72)
    foot = "·  M Y S T E R I O U S  ·"
    fw = draw.textlength(foot, font=f_foot)
    shadow_text(draw, ((W-fw)/2, y), foot, f_foot, CREAM)

    img.convert("RGB").save(out_path, "PNG", optimize=True)
    print("saved", out_path)

for i, (title, points) in enumerate(TOPICS):
    n = i + 1
    bg = BG1 if i % 2 == 0 else BG2
    build(i, title, points, bg, f"{OUT_DIR}/cog-{n}.png")
print("DONE: 20 images")
