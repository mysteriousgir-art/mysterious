#!/usr/bin/env python3
"""Build 20 Developmental Psychology cheat-sheet infographics."""
import sys, os, json, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cheatsheet import render_cheatsheet

OUT_DIR = "/home/hatch/workspace/zehen/batch4/inf-dev-cheat"

SPECS = [
# ============ 1. Prenatal Development ============
{"title": "Prenatal Development", "subtitle": "Developmental Psychology — Before Birth",
 "sections": [
  {"title": "Conception", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Life begins when one sperm fertilizes one egg → zygote."]},
    {"type": "points", "label": "Key Points", "items": ["Zygote carries 46 chromosomes (23 + 23).", "Holds the full genetic blueprint of the baby."]}]},
  {"title": "Germinal Stage", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["First 2 weeks: zygote divides, forms blastocyst, implants."]},
    {"type": "example", "label": "Example", "items": ["By day 5 the blastocyst attaches to the uterus wall.", "If implantation fails, pregnancy never starts."]}]},
  {"title": "Embryonic Stage", "color": "pink", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Weeks 3–8: all major organs and systems form."]},
    {"type": "points", "label": "Key Points", "items": ["Heart, brain, spine, arms and legs develop.", "Most vulnerable to teratogens — damage risk highest."]}]},
  {"title": "Fetal Stage", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Week 9 to birth: organs grow and start working."]},
    {"type": "example", "label": "Example", "items": ["Week 20: mother feels kicking; fetus hears sounds.", "Brain builds billions of neurons in this stage."]}]},
  {"title": "Viability & Birth", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Viability ≈ 24–26 weeks (survive outside womb).", "Preterm = born before 37 weeks.", "Lungs mature last; full term = 40 weeks."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Germinal → Embryonic → Fetal."]}]},
  {"title": "Stage Timeline", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Germinal", "Embryonic", "Fetal"]},
    {"type": "revision", "label": "Instant Revision", "items": ["2 weeks germinal, weeks 3–8 embryonic, week 9+ fetal."]}]},
 ],
 "footer": ["three prenatal stages", "viability 24–26 weeks", "embryonic stage = highest teratogen risk"]},

# ============ 2. Newborn Reflexes and Abilities ============
{"title": "Newborn Reflexes & Abilities", "subtitle": "Developmental Psychology — The Newborn",
 "sections": [
  {"title": "Rooting & Sucking", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Rooting: cheek stroke → baby turns toward touch."]},
    {"type": "example", "label": "Example", "items": ["Touch her cheek; she opens her mouth, ready to feed.", "Sucking reflex lets her feed immediately."]}]},
  {"title": "Grasp & Moro", "color": "green", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Palmar grasp: finger in palm → tight grip.", "Moro: startled → arms fling out, then cry.", "Stepping: held upright → walking-like steps."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Stepping fades ~2 months; real walking ≈ 1 year."]}]},
  {"title": "Hearing & Taste", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Hears well; prefers mother's voice and language.", "Tells sweet from bitter from birth."]},
    {"type": "example", "label": "Example", "items": ["2-day-old turns toward mother's voice, ignores strangers."]}]},
  {"title": "Vision", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Blurry at birth; sees best 8–12 inches away.", "Born preferring faces over patterns."]},
    {"type": "example", "label": "Example", "items": ["Newborn stares longest at a face drawing."]}]},
  {"title": "Touch & Sleep", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Touch most developed sense; calms heartbeat.", "Skin-to-skin steadies breathing and warmth.", "Sleeps 16–17 hrs in short bursts."]}]},
  {"title": "Reflex Overview", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Rooting", "Moro", "Stepping"]},
    {"type": "revision", "label": "Instant Revision", "items": ["Reflexes = survival tools; most fade in months."]}]},
 ],
 "footer": ["rooting, sucking, grasp, Moro, stepping", "vision best at 8–12 inches", "prefers mother's voice"]},

# ============ 3. Infant Sensory Development ============
{"title": "Infant Sensory Development", "subtitle": "Developmental Psychology — Baby Senses",
 "sections": [
  {"title": "Vision", "color": "blue", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Blurry, color-blind at first; improves fast.", "Sees colors by 2 months; near-adult by 6 months."]},
    {"type": "example", "label": "Example", "items": ["1-month-old tracks a bright red ball, ignores grey."]}]},
  {"title": "Hearing", "color": "green", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Develops before birth; knows mother's voice.", "Prefers womb-heard lullabies."]},
    {"type": "example", "label": "Example", "items": ["3-month-old sucks faster hearing mother's voice."]}]},
  {"title": "Taste & Smell", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Work from birth; prefers sweet and mother's scent.", "Days old: picks mother's breast pad by smell."]},
    {"type": "example", "label": "Example", "items": ["Scrunches at lemon, relaxes at sugar water."]}]},
  {"title": "Touch", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Most developed sense at birth; lowers stress.", "Daily massage → faster weight gain, less crying."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Touch stays vital for bonding all life."]}]},
  {"title": "Senses Together", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["By 4–5 months vision guides reaching.", "Hand-eye coordination builds from this link.", "Loud sudden input overwhelms; gentle soothes."]}]},
  {"title": "Brain & Senses", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "brain", "labels": []},
    {"type": "revision", "label": "Instant Revision", "items": ["Preferential looking reveals what babies notice."]}]},
 ],
 "footer": ["vision adult-like by 6 months", "touch most developed at birth", "senses integrate by 4–5 months"]},

# ============ 4. Piaget: Sensorimotor Stage ============
{"title": "Piaget: Sensorimotor Stage", "subtitle": "Developmental Psychology — Birth to 2 Years",
 "sections": [
  {"title": "The Stage", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Birth–2 yrs: babies learn via senses and movement."]},
    {"type": "example", "label": "Example", "items": ["4-month-old shakes a rattle, delighted by sound."]}]},
  {"title": "Circular Reactions", "color": "green", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["4–8 mo: repeats actions affecting world.", "Shaking, banging, dropping = tiny experiments."]},
    {"type": "example", "label": "Example", "items": ["8-month-old drops spoon repeatedly, watching it fall."]}]},
  {"title": "Object Permanence", "color": "pink", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Knowing things exist even when unseen (≈8–12 mo)."]},
    {"type": "example", "label": "Example", "items": ["7-month-old acts as if hidden toy no longer exists."]}]},
  {"title": "A-not-B Error", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Searches old spot A instead of new spot B."]},
    {"type": "example", "label": "Example", "items": ["10-month-old searches first hiding place, not the new one."]}]},
  {"title": "Late Substage", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["12–18 mo: active experimenting with new ways.", "18–24 mo: mental symbols; pretend play starts."]},
    {"type": "example", "label": "Example", "items": ["18-month-old pretends to drink from empty cup."]}]},
  {"title": "Milestone Flow", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Reflexes", "Repeat", "Object perm."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Piaget may have underestimated young infants."]}]},
 ],
 "footer": ["sensorimotor = birth to 2 years", "object permanence ≈ 8–12 months", "A-not-B error"]},

# ============ 5. Piaget: Preoperational Stage ============
{"title": "Piaget: Preoperational Stage", "subtitle": "Developmental Psychology — Ages 2 to 7",
 "sections": [
  {"title": "Symbolic Thinking", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Ages 2–7: language, pretend play, drawings explode."]},
    {"type": "example", "label": "Example", "items": ["5-year-old pretends a leaf is money, box is counter."]}]},
  {"title": "Egocentrism", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Cannot imagine another's perspective — not selfishness."]},
    {"type": "example", "label": "Example", "items": ["Covers own eyes, believes you cannot see her either."]}]},
  {"title": "Conservation", "color": "pink", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Amount stays same despite shape change — they fail it."]},
    {"type": "example", "label": "Example", "items": ["Tall thin glass 'has more' than short wide one.", "Centration: focusing on one feature only."]}]},
  {"title": "Animism", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Believes lifeless things are alive.", "Moon follows me; sun sleeps at night.", "Artificialism: clouds made by someone pouring."]}]},
  {"title": "Pretend Play", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Peaks now; builds language and social skills.", "One thing stands for another = symbolic mind."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Thinking is intuitive, not logical, at this stage."]}]},
  {"title": "Three Limits", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "venn", "labels": ["Egocentrism", "Centration", "Animism"]},
    {"type": "revision", "label": "Instant Revision", "items": ["Logic arrives in concrete operations (7–11)."]}]},
 ],
 "footer": ["preoperational = ages 2–7", "egocentrism vs selfishness", "conservation failure = centration"]},

# ============ 6. Vygotsky's Sociocultural Theory ============
{"title": "Vygotsky's Sociocultural Theory", "subtitle": "Developmental Psychology — Learning Is Social",
 "sections": [
  {"title": "Core Idea", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Learning is social first, then internalized."]},
    {"type": "example", "label": "Example", "items": ["Father holds hand while she writes, then lets go."]}]},
  {"title": "ZPD", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Zone of Proximal Development: gap between alone vs helped."]},
    {"type": "example", "label": "Example", "items": ["6-year-old solves puzzle with brother's hints only.", "Teach inside this zone for best results."]}]},
  {"title": "Scaffolding", "color": "pink", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Temporary support, removed as child improves."]},
    {"type": "example", "label": "Example", "items": ["Teacher demos 2 problems; student does the rest."]}]},
  {"title": "MKO", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["More Knowledgeable Other: teacher, parent, or peer."]},
    {"type": "points", "label": "Key Points", "items": ["Peer learning valued highly.", "Culture shapes thinking via tools and language."]}]},
  {"title": "Private Speech", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Talking to self during tasks = thinking out loud."]},
    {"type": "example", "label": "Example", "items": ["4-year-old whispers steps while building a tower.", "Not a bad habit — it guides actions."]}]},
  {"title": "Piaget vs Vygotsky", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "scale", "labels": ["Piaget", "Vygotsky"]},
    {"type": "revision", "label": "Instant Revision", "items": ["Piaget: lone scientist. Vygotsky: apprentice."]}]},
 ],
 "footer": ["ZPD = teachable gap", "scaffolding fades with skill", "private speech is normal"]},

# ============ 7. Language Development Milestones ============
{"title": "Language Development Milestones", "subtitle": "Developmental Psychology — Learning to Talk",
 "sections": [
  {"title": "Cooing", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["≈2 months: vowel-like ooo, aaa in happy moments."]},
    {"type": "example", "label": "Example", "items": ["Baby coos softly when mother smiles."]}]},
  {"title": "Babbling", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["≈6 months: adds consonants — ba-ba, da-da."]},
    {"type": "points", "label": "Key Points", "items": ["Starts with all languages' sounds.", "Narrows to native language by 10 months."]}]},
  {"title": "First Words", "color": "pink", "blocks": [
    {"type": "def", "label": "Definition", "items": ["≈12 months: holophrases — one word = whole sentence."]},
    {"type": "example", "label": "Example", "items": ["'Up' means pick me up; 'mama' means I want mother."]}]},
  {"title": "Word Errors", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Overextension: all men are 'dada'.", "Underextension: word kept too narrow.", "Both fix themselves with experience."]}]},
  {"title": "Grammar Growth", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Telegraphic speech ≈2 yrs: 'want cookie'.", "Overregularization: 'goed' instead of 'went'.", "Errors prove active rule-learning."]}]},
  {"title": "Milestone Flow", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Cooing", "Babbling", "Words"]},
    {"type": "revision", "label": "Instant Revision", "items": ["Responsive talk is the biggest factor."]}]},
 ],
 "footer": ["cooing 2 mo, babbling 6 mo, words 12 mo", "overextension vs underextension", "overregularization = rule learning"]},

# ============ 8. Temperament in Infancy ============
{"title": "Temperament in Infancy", "subtitle": "Developmental Psychology — Born This Way",
 "sections": [
  {"title": "What Is It", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Built-in style of reacting: activity, mood, adaptability."]},
    {"type": "example", "label": "Example", "items": ["One baby giggles at strangers; another screams."]}]},
  {"title": "Easy (40%)", "color": "green", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Cheerful, regular habits, adapts well.", "Usually the smoothest outcomes."]},
    {"type": "example", "label": "Example", "items": ["Smiles at new people; tries new foods happily."]}]},
  {"title": "Difficult (10%)", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Intense, irregular, slow to adapt.", "Higher risk — but patient parenting helps hugely."]},
    {"type": "example", "label": "Example", "items": ["Cries intensely, sleeps irregularly, protests change."]}]},
  {"title": "Slow-to-Warm (15%)", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Shy, cautious at first; adapts gradually."]},
    {"type": "example", "label": "Example", "items": ["Hides at parties, joins in after 20 minutes."]}]},
  {"title": "Goodness of Fit", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Outcome = match between parenting and temperament."]},
    {"type": "example", "label": "Example", "items": ["Calm mother soothes intense baby instead of punishing."]}]},
  {"title": "Three Types", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "bars", "labels": ["Easy", "Slow", "Difficult"]},
    {"type": "revision", "label": "Instant Revision", "items": ["Stable but not fixed; genes set the range."]}]},
 ],
 "footer": ["Thomas & Chess: 3 types", "goodness of fit", "easy 40%, difficult 10%, slow 15%"]},

# ============ 9. Play and Development ============
{"title": "Play and Development", "subtitle": "Developmental Psychology — Work of Childhood",
 "sections": [
  {"title": "Solitary Play", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Under 2: playing alone, absorbed in own world."]},
    {"type": "example", "label": "Example", "items": ["Toddler bangs pots alone in the kitchen."]}]},
  {"title": "Parallel Play", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["≈3 yrs: beside, not with, others — social stepping stone."]},
    {"type": "example", "label": "Example", "items": ["Two 3-year-olds build separate towers side by side."]}]},
  {"title": "Cooperative Play", "color": "pink", "blocks": [
    {"type": "def", "label": "Definition", "items": ["≈4–5 yrs: shared goals, teamwork, roles."]},
    {"type": "example", "label": "Example", "items": ["Sandbox crew shares shovels to build one castle."]}]},
  {"title": "Pretend Play", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Peaks ages 3–6; builds language and empathy.", "Negotiating rules = learning social thinking."]},
    {"type": "example", "label": "Example", "items": ["Cops-and-robbers: you be robber, I'll chase."]}]},
  {"title": "Games & Rough Play", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Rule games (6+): fairness, turn-taking, losing well.", "Rough-and-tumble builds strength and bounds."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Free play shrinking → child anxiety rising."]}]},
  {"title": "Play Stages", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Solitary", "Parallel", "Coop."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Physical play → bodies; social play → bonds."]}]},
 ],
 "footer": ["Parten's play stages", "pretend play peaks 3–6", "play is the work of childhood"]},

# ============ 10. Theory of Mind ============
{"title": "Theory of Mind", "subtitle": "Developmental Psychology — Reading Minds",
 "sections": [
  {"title": "What Is It", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Knowing others have different thoughts and feelings."]},
    {"type": "example", "label": "Example", "items": ["5-year-old sees friend is sad though she is happy."]}]},
  {"title": "False-Belief Task", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Classic test: under 4 fail; 4–5 most pass."]},
    {"type": "example", "label": "Example", "items": ["Candy box full of pencils: 3-year-old says friend expects candy."]}]},
  {"title": "Sally-Anne Test", "color": "pink", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Where will Sally look? Tracks false belief."]},
    {"type": "example", "label": "Example", "items": ["Sally's marble moved; where will she search?"]}]},
  {"title": "Why It Matters", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Foundation of empathy and friendship.", "Earlier TOM → more sharing, kinder fights."]},
    {"type": "example", "label": "Example", "items": ["6-year-old comforts crying classmate with words."]}]},
  {"title": "Autism Link", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Autism: TOM difficulties — faces, jokes, sarcasm.", "Explains social struggles, not intelligence."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Mind-minded parenting speeds TOM up."]}]},
  {"title": "TOM Growth", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["No TOM", "False belief", "Empathy"]},
    {"type": "revision", "label": "Instant Revision", "items": ["Keeps refining through adulthood."]}]},
 ],
 "footer": ["false-belief task ≈ age 4–5", "Sally-Anne test", "TOM = base of empathy"]},

# ============ 11. Childhood Friendships ============
{"title": "Childhood Friendships", "subtitle": "Developmental Psychology — Friends Matter",
 "sections": [
  {"title": "Early Basis", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Young friends = convenience + shared activities."]},
    {"type": "example", "label": "Example", "items": ["7-year-old's best friend lives next door."]}]},
  {"title": "Deepening", "color": "green", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Middle childhood: intimacy, secrets, loyalty.", "Betraying a secret can end it."]},
    {"type": "example", "label": "Example", "items": ["Two 10-year-olds share secrets with no one else."]}]},
  {"title": "Peer Status", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Popular kids: kind and cooperative.", "Rejected-aggressive kids: painful exclusion cycle."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Social pain = brain pain (same areas)."]}]},
  {"title": "One Good Friend", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Quality beats quantity — one loyal friend protects."]},
    {"type": "example", "label": "Example", "items": ["Shy boy + one close friend > popular + 20 shallow."]}]},
  {"title": "Peer Influence", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Friends shape behavior both ways.", "Good friends → school success and kindness."]},
    {"type": "example", "label": "Example", "items": ["Friends who study together lift each other up."]}]},
  {"title": "Bonding Path", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Contact", "Trust", "Intimacy"]},
    {"type": "revision", "label": "Instant Revision", "items": ["Schools help via mixing and teamwork."]}]},
 ],
 "footer": ["friendship deepens with age", "quality beats quantity", "rejection = real brain pain"]},

# ============ 12. Parenting Styles (Baumrind) ============
{"title": "Parenting Styles", "subtitle": "Developmental Psychology — Baumrind's Four Styles",
 "sections": [
  {"title": "Authoritative", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Warm + firm: high expectations, high responsiveness."]},
    {"type": "example", "label": "Example", "items": ["9 PM bedtime explained for health + goodnight hug.", "Best outcomes across cultures."]}]},
  {"title": "Authoritarian", "color": "pink", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Strict + cold: high demands, low warmth."]},
    {"type": "example", "label": "Example", "items": ["My word is law — no questions, punishment for disobedience.", "Obedient but lower self-esteem."]}]},
  {"title": "Permissive", "color": "yellow", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Warm + undemanding: few rules, little discipline."]},
    {"type": "example", "label": "Example", "items": ["Never says no; buys every demanded toy.", "Impulsive; struggles with authority."]}]},
  {"title": "Uninvolved", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Low warmth + low control: the worst combination."]},
    {"type": "example", "label": "Example", "items": ["Unaware of child's friends, grades, feelings.", "Poorest outcomes: attachment and behavior."]}]},
  {"title": "Culture & Age", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Core finding holds globally: love + control.", "Adapts with age: explain more, control less."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Pattern matters, not income or structure."]}]},
  {"title": "Four Styles", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "bars", "labels": ["Authorit.", "Authorn.", "Permis.", "Uninvol."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Authoritative = warm + firm wins."]}]},
 ],
 "footer": ["Baumrind's 4 styles", "authoritative = best outcomes", "uninvolved = poorest outcomes"]},

# ============ 13. Puberty and the Adolescent Brain ============
{"title": "Puberty & the Adolescent Brain", "subtitle": "Developmental Psychology — Teen Brain",
 "sections": [
  {"title": "Puberty Start", "color": "blue", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Growth spurt: girls ≈10–11, boys ≈12–13.", "Hormones: estrogen, testosterone.", "Timing 8–14 is all normal."]}]},
  {"title": "Brain Remodel", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Limbic (emotion) matures early; prefrontal (judgment) late."]},
    {"type": "example", "label": "Example", "items": ["Plans party brilliantly, then takes a roof dare."]}]},
  {"title": "Peer Effect", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Risks rise with peers watching.", "Reward centers fire harder for peer approval.", "Biology, not just bad choices."]}]},
  {"title": "Pruning", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Weak connections pruned; used ones myelinated."]},
    {"type": "example", "label": "Example", "items": ["Like trimming a garden: use it or lose it."]}]},
  {"title": "Sleep Shift", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Melatonin releases later in teens.", "Need 8–10 hours; early school fights biology."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Mood swings are normal remodeling signs."]}]},
  {"title": "Brain Under Work", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "brain", "labels": []},
    {"type": "revision", "label": "Instant Revision", "items": ["Most teens emerge healthy and fine."]}]},
 ],
 "footer": ["limbic early, prefrontal late", "peer presence raises risk", "teens need 8–10 hrs sleep"]},

# ============ 14. Identity Formation (Marcia) ============
{"title": "Identity Formation (Marcia)", "subtitle": "Developmental Psychology — Who Am I?",
 "sections": [
  {"title": "Erikson's Task", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Identity vs role confusion: build a stable self."]},
    {"type": "example", "label": "Example", "items": ["Teen years ask one big question: who am I?"]}]},
  {"title": "Diffusion", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["No exploration, no commitment — drifting."]},
    {"type": "example", "label": "Example", "items": ["Never thinks about careers; follows friends."]}]},
  {"title": "Foreclosure", "color": "pink", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Commitment without exploration — adopted values."]},
    {"type": "example", "label": "Example", "items": ["Becomes doctor because father demanded it."]}]},
  {"title": "Moratorium", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Active exploring, not yet committed — healthy."]},
    {"type": "example", "label": "Example", "items": ["Tries majors, religions, groups; still unsure."]}]},
  {"title": "Achievement", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Exploration → real commitment. Healthiest outcome."]},
    {"type": "example", "label": "Example", "items": ["Chose teaching freely after exploring careers."]}]},
  {"title": "Four Statuses", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Diffusion", "Foreclosure", "Moratorium", "Achieve."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Identity forms domain by domain."]}]},
 ],
 "footer": ["Marcia's 4 identity statuses", "moratorium = healthy searching", "achievement = explore then commit"]},

# ============ 15. Peer Pressure in Adolescence ============
{"title": "Peer Pressure in Adolescence", "subtitle": "Developmental Psychology — Fitting In",
 "sections": [
  {"title": "Peak Pressure", "color": "blue", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Peaks around age 14.", "Conform to win acceptance: dress, talk, risks."]},
    {"type": "example", "label": "Example", "items": ["Tries smoking because 3 best friends do."]}]},
  {"title": "Unspoken Pull", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Mostly silent — you just feel the pull."]},
    {"type": "example", "label": "Example", "items": ["Laughs at jokes she doesn't find funny."]}]},
  {"title": "Cliques & Crowds", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Cliques: small tight groups (intimacy).", "Crowds: big reputation groups (belonging)."]}]},
  {"title": "Not All Bad", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Friends boost effort, kindness, healthy habits.", "Choosing good friends = choosing good influence."]},
    {"type": "example", "label": "Example", "items": ["Friends who study hard → she studies more."]}]},
  {"title": "Resisting", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Ready responses + alternatives work.", "Keep one sober friend nearby.", "Close family bonds = best shield."]}]},
  {"title": "Conform → Resist", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Belong", "Conform", "Resist"]},
    {"type": "revision", "label": "Instant Revision", "items": ["Fades as identity solidifies."]}]},
 ],
 "footer": ["peaks at age 14", "cliques vs crowds", "family bonds = best shield"]},

# ============ 16. Risk Taking in Teens ============
{"title": "Risk Taking in Teens", "subtitle": "Developmental Psychology — Why Teens Dare",
 "sections": [
  {"title": "The Reality", "color": "blue", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Car crashes = top killer of teens worldwide.", "Same teen cautious alone, wild with peers."]},
    {"type": "example", "label": "Example", "items": ["Drives carefully with mother, speeds with friends."]}]},
  {"title": "Dual Systems", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Reward system matures early; control system late."]},
    {"type": "example", "label": "Example", "items": ["Reward center fires 2x harder for exciting rewards."]}]},
  {"title": "They Know Risks", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Teens overestimate dangers like smoking.", "They weigh social rewards higher instead."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Not ignorance — different priorities."]}]},
  {"title": "Hot vs Cold", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Hot: emotional, rushed, with peers.", "Cold: calm, alone — teens decide well here."]},
    {"type": "example", "label": "Example", "items": ["Party drink offer decided in 3 emotional seconds."]}]},
  {"title": "Sensation Seeking", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Hunger for intense experiences; peaks 15–19."]},
    {"type": "example", "label": "Example", "items": ["Channel it: sports, travel, performance — not crush it."]}]},
  {"title": "Hot vs Cold", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "scale", "labels": ["Hot", "Cold"]},
    {"type": "revision", "label": "Instant Revision", "items": ["Prefrontal wiring done ≈ mid-20s; risks drop."]}]},
 ],
 "footer": ["dual systems model", "hot vs cold decisions", "sensation seeking peaks 15–19"]},

# ============ 17. Emerging Adulthood ============
{"title": "Emerging Adulthood", "subtitle": "Developmental Psychology — Ages 18 to 25",
 "sections": [
  {"title": "Arnett's Stage", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Ages 18–25: distinct stage in modern societies."]},
    {"type": "example", "label": "Example", "items": ["22-year-old graduate: dating, interning, figuring out."]}]},
  {"title": "Five Features", "color": "green", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Identity exploration (love and work).", "Instability: moving, changing plans.", "Self-focus, feeling in-between, possibilities."]}]},
  {"title": "Why It Exists", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Longer education, later marriage.", "Tougher job markets delay adult roles."]},
    {"type": "example", "label": "Example", "items": ["24-year-old living with parents, saving up."]}]},
  {"title": "Dark Side", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Highest anxiety/depression of any age group.", "Freedom + uncertainty = stressful."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Strongest in wealthy, educated societies."]}]},
  {"title": "Bright Side", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Freest period for self-discovery.", "Exploring now prevents midlife regret."]},
    {"type": "example", "label": "Example", "items": ["Travels, volunteers, freelances before committing."]}]},
  {"title": "Path to Adult", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Explore", "Unstable", "Commit"]},
    {"type": "revision", "label": "Instant Revision", "items": ["Ends with career, partner, independence."]}]},
 ],
 "footer": ["Arnett: ages 18–25", "5 features of emerging adulthood", "highest anxiety of any age group"]},

# ============ 18. Transition to Parenthood ============
{"title": "Transition to Parenthood", "subtitle": "Developmental Psychology — Baby Arrives",
 "sections": [
  {"title": "The Shock", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Joy mixed with exhaustion — a major transition."]},
    {"type": "example", "label": "Example", "items": ["8-hour sleepers now sleep in shifts, argue at 3 AM."]}]},
  {"title": "The Dip", "color": "green", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Marital satisfaction dips after first baby.", "Less time, more conflict, divided attention.", "Recovers as children grow."]}]},
  {"title": "Fair Sharing", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Involved fathers → happier mothers, thriving babies.", "Fairness matters more than hours."]},
    {"type": "example", "label": "Example", "items": ["Dad does half the night feeds; marriage stays strong."]}]},
  {"title": "Postpartum", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["≈1 in 7 mothers (and some fathers) affected.", "Medical condition, not weakness.", "Hormones + sleep loss + stress."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Support is the top buffer — build a village."]}]},
  {"title": "What Protects", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Friendship, appreciation, gentle conflict.", "Realistic expectations about the chaos."]},
    {"type": "example", "label": "Example", "items": ["Laughing together over diaper disasters."]}]},
  {"title": "The Paradox", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "scale", "labels": ["Stress", "Meaning"]},
    {"type": "revision", "label": "Instant Revision", "items": ["High daily stress, yet life meaning soars."]}]},
 ],
 "footer": ["satisfaction dip is normal", "postpartum ≈ 1 in 7", "support buffers everything"]},

# ============ 19. Midlife: Crisis or Myth? ============
{"title": "Midlife: Crisis or Myth?", "subtitle": "Developmental Psychology — The Middle Years",
 "sections": [
  {"title": "The Myth", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Dramatic meltdown at 40 — largely a myth."]},
    {"type": "example", "label": "Example", "items": ["Only 10–20% report a true crisis.", "Quitting accounting for a bakery: crisis or courage?"]}]},
  {"title": "Generativity", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Erikson: contributing vs stagnating."]},
    {"type": "example", "label": "Example", "items": ["Mentoring young colleagues beats chasing promotions."]}]},
  {"title": "Sandwich Gen", "color": "pink", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Caring for kids + parents at once."]},
    {"type": "example", "label": "Example", "items": ["Raising teens while caring for aging mother."]}]},
  {"title": "U-Bend", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Happiness dips in 40s–50s, rises after.", "Peak responsibilities + health scares.", "Knowing it is normal helps."]}]},
  {"title": "Prime Time", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Wisdom and expertise peak.", "Speed slows slightly; knowledge more than compensates."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Turning point, not a cliff."]}]},
  {"title": "Crisis or Myth?", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "scale", "labels": ["Crisis", "Myth"]},
    {"type": "revision", "label": "Instant Revision", "items": ["Invest in health + bonds → sail through."]}]},
 ],
 "footer": ["crisis = mostly myth (10–20%)", "generativity vs stagnation", "U-bend of happiness"]},

# ============ 20. Successful Aging ============
{"title": "Successful Aging", "subtitle": "Developmental Psychology — Aging Well",
 "sections": [
  {"title": "Rowe & Kahn", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Three parts: avoid disease, stay active, stay engaged."]},
    {"type": "example", "label": "Example", "items": ["80-year-old swims daily, volunteers, laughs with friends."]}]},
  {"title": "SOC Model", "color": "green", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Selection: choose meaningful goals.", "Optimization: practice what matters.", "Compensation: new ways (hearing aid, notes)."]}]},
  {"title": "Mindset Power", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Positive age beliefs add years to life.", "Negative stereotypes speed decline."]},
    {"type": "revision", "label": "Instant Revision", "items": ["Mindset shapes biology."]}]},
  {"title": "Lifestyle", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Move daily, eat plants, sleep 7–8 hrs.", "Manage stress; never smoke."]},
    {"type": "example", "label": "Example", "items": ["Blue Zones: move naturally, belong, have purpose."]}]},
  {"title": "Bonds First", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Warm relationships = top predictor of health.", "Loneliness harms as much as smoking."]},
    {"type": "example", "label": "Example", "items": ["Harvard study: bonds keep 80-year-olds healthy."]}]},
  {"title": "Three Pillars", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "pyramid", "labels": ["Avoid disease", "Stay active", "Stay engaged"]},
    {"type": "revision", "label": "Instant Revision", "items": ["Purpose protects: mentor, create, care."]}]},
 ],
 "footer": ["Rowe & Kahn's 3 parts", "SOC: select, optimize, compensate", "relationships = top predictor"]},
]

# ---------- render + upload ----------
def load_env():
    env = {}
    with open("/home/hatch/workspace/zehen/.env.supabase") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env

def upload_file(url, key, path):
    with open(path, "rb") as f:
        data = f.read()
    req = urllib.request.Request(
        f"{url}/storage/v1/object/infographics/{path.split('/')[-1]}",
        data=data, method="POST",
        headers={"apikey": key, "Authorization": f"Bearer {key}",
                 "Content-Type": "image/png", "x-upsert": "true"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status

def check(url):
    req = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    env = load_env()
    url, key = env["SUPABASE_URL"], env["SUPABASE_SECRET_KEY"]
    assert len(SPECS) == 20, f"expected 20 specs, got {len(SPECS)}"
    ok, fails = 0, []
    for i, spec in enumerate(SPECS, 1):
        fname = f"dev-{i:02d}.png"
        out = os.path.join(OUT_DIR, fname)
        render_cheatsheet(spec, out)
        try:
            st = upload_file(url, key, out)
            pub = f"{url}/storage/v1/object/public/infographics/{fname}"
            hs = check(pub)
            print(f"{fname}: upload={st} verify={hs} title={spec['title'][:40]}", flush=True)
            if st in (200, 201) and hs == 200:
                ok += 1
            else:
                fails.append(fname)
        except Exception as e:
            print(f"{fname}: FAILED {e}", flush=True)
            fails.append(fname)
    print(f"\nDONE: {ok}/20 overwritten and verified")
    if fails:
        print("FAILURES:", fails)

if __name__ == "__main__":
    main()
