#!/usr/bin/env python3
"""Cheat-sheet specs for 20 Counseling & Therapy infographics (part 1: 1-10)."""
import sys
sys.path.insert(0, '/home/hatch/workspace/zehen/batch4')
from cheatsheet import render_cheatsheet

AR = "\u2192"  # →

SPECS_1_10 = [
# ================= 1. Counseling vs Clinical vs Psychiatry =================
{
 "title": "Counseling vs Clinical vs Psychiatry",
 "subtitle": "Chapter - Helping Professions",
 "sections": [
  {"title": "Counseling Psychology", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Helps everyday problems, growth, relationships.", "Strength-based: builds on client strengths."]},
   {"type": "example", "label": "Example", "items": ["Student seeks help for exam stress."]},
  ]},
  {"title": "Clinical Psychology", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Diagnoses and treats mental disorders."]},
   {"type": "points", "label": "Focus", "items": ["Depression, anxiety, panic disorders.", "Uses tests plus therapy."]},
  ]},
  {"title": "Psychiatry", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Medical doctors (MBBS + specialization)."]},
   {"type": "points", "label": "Key Power", "items": ["Can prescribe medicines.", "Treats bipolar, schizophrenia."]},
  ]},
  {"title": "Training Paths", "color": "orange", "blocks": [
   {"type": "points", "label": "How They Train", "items": ["Counselors: psychology degrees (MS/MPhil).", "Psychiatrists: medical degree first.", "All need supervised practice hours."]},
  ]},
  {"title": "Teamwork & Referral", "color": "teal", "blocks": [
   {"type": "points", "label": "Working Together", "items": ["Referral is a skill, not a failure.", "Mild issues: counselor; severe: psychiatrist.", "Hospital teams include all three."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Right helper for the right problem."]},
  ]},
  {"title": "Shared Ethics", "color": "pink", "blocks": [
   {"type": "points", "label": "Common Ground", "items": ["Confidentiality for all.", "Informed consent required.", "Do no harm - always."]},
   {"type": "diagram", "diagram": "bars", "labels": ["Growth", "Disorder", "Medical"], "height": 120},
  ]},
 ],
 "footer": ["Counseling = growth", "Clinical = disorders", "Psychiatry = medicines", "Refer when needed"],
},
# ================= 2. Active Listening =================
{
 "title": "Active Listening",
 "subtitle": "Chapter - Microskills",
 "sections": [
  {"title": "What It Is", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Listening to understand, not to reply."]},
   {"type": "points", "label": "Core", "items": ["Full attention on the client.", "Hear words plus feelings."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Understand first, respond later."]},
  ]},
  {"title": "Paraphrasing", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Restate in your own shorter words."]},
   {"type": "points", "label": "Rules", "items": ["Use fresh words, not parroting.", "Check: 'Did I get that right?'"]},
   {"type": "example", "label": "Example", "items": ["Client: boss shamed me " + AR + " 'You felt humiliated.'"]},
  ]},
  {"title": "Summarizing", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Pull key themes together."]},
   {"type": "points", "label": "When", "items": ["Use at session transitions.", "Connects scattered pieces."]},
  ]},
  {"title": "Listening Cycle", "color": "orange", "blocks": [
   {"type": "diagram", "diagram": "flow", "labels": ["Attend", "Listen", "Check", "Confirm"], "height": 130},
   {"type": "revision", "label": "Instant Revision", "items": ["Repeat until client says 'exactly!'"]},
  ]},
  {"title": "Hear the Unsaid", "color": "pink", "blocks": [
   {"type": "points", "label": "Watch For", "items": ["Pauses and sudden topic changes.", "Nervous laughter hides pain.", "Contradictions reveal truth."]},
   {"type": "example", "label": "Example", "items": ["Laughs while describing father's death."]},
  ]},
  {"title": "Mistakes to Avoid", "color": "red", "blocks": [
   {"type": "points", "label": "Don't", "items": ["Don't interrupt with advice.", "Don't plan next question early.", "Don't say 'you should just...'."]},
  ]},
 ],
 "footer": ["Paraphrase", "Summarize", "Listening cycle", "Hear the unsaid"],
},
# ================= 3. Reflecting Feelings =================
{
 "title": "Reflecting Feelings",
 "subtitle": "Chapter - Microskills",
 "sections": [
  {"title": "What It Is", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Name the emotion beneath the words."]},
   {"type": "points", "label": "Why", "items": ["Shows deep understanding.", "Validates client experience."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Feelings named = feelings tamed."]},
  ]},
  {"title": "The Formula", "color": "green", "blocks": [
   {"type": "def", "label": "Formula", "items": ["'You feel ___ because ___.'"]},
   {"type": "points", "label": "Rules", "items": ["Feeling first, reason second.", "Keep it tentative, not certain."]},
   {"type": "example", "label": "Example", "items": ["'You feel drained; everyone demands help.'"]},
  ]},
  {"title": "Rich Vocabulary", "color": "purple", "blocks": [
   {"type": "points", "label": "Go Beyond", "items": ["Beyond sad/angry: overwhelmed, ashamed.", "Guilty, lonely, relieved, proud.", "Precise words heal deeper."]},
  ]},
  {"title": "Go Deeper", "color": "orange", "blocks": [
   {"type": "points", "label": "Layers", "items": ["Anger often covers hurt.", "Anxiety often covers fear of loss.", "Reflect the deeper layer."]},
   {"type": "example", "label": "Example", "items": ["'Under the anger, I sense hurt.'"]},
  ]},
  {"title": "Body Mismatch", "color": "pink", "blocks": [
   {"type": "def", "label": "Signal", "items": ["Words say fine, body says pain."]},
   {"type": "points", "label": "Clues", "items": ["Tears, shaking, flushed face.", "Gently name what you see."]},
   {"type": "example", "label": "Example", "items": ["'You say fine, but I see tears.'"]},
  ]},
  {"title": "Reflect Positives", "color": "teal", "blocks": [
   {"type": "points", "label": "Don't Forget", "items": ["Notice pride, relief, hope.", "Strengthens good feelings.", "Don't over-reflect every line."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Listen", "Reflect", "Confirm"], "height": 120},
  ]},
 ],
 "footer": ["Formula: feel + because", "Deeper layer", "Body mismatch", "Positives too"],
},
# ================= 4. Stages of the Counseling Process =================
{
 "title": "Stages of the Counseling Process",
 "subtitle": "Chapter - How Therapy Flows",
 "sections": [
  {"title": "Stage 1: Relationship", "color": "blue", "blocks": [
   {"type": "def", "label": "Goal", "items": ["Build safety with warmth + empathy."]},
   {"type": "points", "label": "Do", "items": ["Explain confidentiality first.", "Listen to their full story."]},
  ]},
  {"title": "Stage 2: Assessment", "color": "green", "blocks": [
   {"type": "def", "label": "Goal", "items": ["Map the problem together."]},
   {"type": "points", "label": "Ask", "items": ["When did it start?", "What makes it worse or better?"]},
   {"type": "example", "label": "Example", "items": ["'Panic began after accident, while driving.'"]},
  ]},
  {"title": "Stage 3: Goal Setting", "color": "yellow", "blocks": [
   {"type": "def", "label": "Goal", "items": ["Vague wishes " + AR + " clear goals."]},
   {"type": "points", "label": "Rules", "items": ["Goals must be measurable.", "Client owns the goals."]},
   {"type": "example", "label": "Example", "items": ["'Drive highway twice a week.'"]},
  ]},
  {"title": "Stage 4: Intervention", "color": "orange", "blocks": [
   {"type": "def", "label": "Goal", "items": ["Active work with techniques."]},
   {"type": "points", "label": "Tools", "items": ["CBT, exposure, skills practice.", "Homework between sessions."]},
  ]},
  {"title": "Stage 5: Termination", "color": "purple", "blocks": [
   {"type": "def", "label": "Goal", "items": ["Planned ending, not sudden."]},
   {"type": "points", "label": "Do", "items": ["Review progress + tools.", "Agree on follow-up check."]},
  ]},
  {"title": "Flexible Process", "color": "teal", "blocks": [
   {"type": "points", "label": "Remember", "items": ["Stages loop back in crisis.", "New problems can emerge.", "Document all stages (SOAP)."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Relate", "Assess", "Goals", "Work", "End"], "height": 120},
  ]},
 ],
 "footer": ["5 stages", "Goals must be measurable", "Termination is planned", "SOAP notes"],
},
# ================= 5. Therapeutic Alliance =================
{
 "title": "Therapeutic Alliance",
 "subtitle": "Chapter - Relationship Heals",
 "sections": [
  {"title": "What It Is", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Counselor-client partnership."]},
   {"type": "points", "label": "Why It Matters", "items": ["Best predictor of success.", "Beats techniques alone."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Relationship heals."]},
  ]},
  {"title": "Bordin's 3 Parts", "color": "green", "blocks": [
   {"type": "points", "label": "Three Parts", "items": ["Bond: trust, warmth, respect.", "Goals: agree on targets.", "Tasks: agree on methods."]},
   {"type": "diagram", "diagram": "venn", "labels": ["Bond", "Goals", "Tasks"], "height": 130},
  ]},
  {"title": "Empathy vs Sympathy", "color": "purple", "blocks": [
   {"type": "points", "label": "Difference", "items": ["Empathy: 'Makes sense you feel torn.'", "Sympathy: 'Oh you poor thing!'", "Empathy connects; sympathy distances."]},
  ]},
  {"title": "Ruptures Happen", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Tension moments are normal."]},
   {"type": "points", "label": "Signs", "items": ["Client: 'You don't get it.'", "Invite honest feedback."]},
   {"type": "example", "label": "Example", "items": ["'Help me understand what I missed.'"]},
  ]},
  {"title": "Repair Skills", "color": "pink", "blocks": [
   {"type": "points", "label": "How to Repair", "items": ["Notice withdrawal early.", "Own your mistakes openly.", "Ask: 'Is something off between us?'"]},
  ]},
  {"title": "Cultural Humility", "color": "teal", "blocks": [
   {"type": "points", "label": "Across Differences", "items": ["Stay curious, not expert.", "Ask about their norms.", "Respect family decision styles."]},
   {"type": "example", "label": "Example", "items": ["'How does your family handle problems?'"]},
  ]},
 ],
 "footer": ["Bond + goals + tasks", "Empathy not sympathy", "Repair ruptures", "Cultural humility"],
},
# ================= 6. CBT Techniques =================
{
 "title": "CBT Techniques",
 "subtitle": "Chapter - Cognitive Behavioral Therapy",
 "sections": [
  {"title": "The CBT Model", "color": "blue", "blocks": [
   {"type": "def", "label": "Model", "items": ["Thoughts " + AR + " feelings " + AR + " behaviors loop."]},
   {"type": "points", "label": "Key", "items": ["Change one, shift the others.", "Present-focused, practical."]},
   {"type": "diagram", "diagram": "cycle", "labels": ["Thoughts", "Feelings", "Actions"], "height": 130},
  ]},
  {"title": "Thought Records", "color": "green", "blocks": [
   {"type": "def", "label": "Tool", "items": ["Write: situation " + AR + " thought " + AR + " evidence."]},
   {"type": "points", "label": "Steps", "items": ["Catch automatic thoughts.", "Challenge with real evidence."]},
   {"type": "example", "label": "Example", "items": ["'She hates me' " + AR + " 'She replied late before.'"]},
  ]},
  {"title": "Thinking Traps", "color": "red", "blocks": [
   {"type": "points", "label": "Common Traps", "items": ["All-or-nothing: 'total failure'.", "Catastrophizing: worst case always.", "Mind reading: 'they judge me'."]},
  ]},
  {"title": "Behavioral Experiments", "color": "orange", "blocks": [
   {"type": "def", "label": "Method", "items": ["Test scary predictions like a scientist."]},
   {"type": "points", "label": "Steps", "items": ["Predict " + AR + " test " + AR + " learn.", "Small steps, real data."]},
   {"type": "example", "label": "Example", "items": ["Ask one class question; observe."]},
  ]},
  {"title": "Exposure Ladder", "color": "purple", "blocks": [
   {"type": "def", "label": "Method", "items": ["Face fears: easiest " + AR + " hardest."]},
   {"type": "points", "label": "Steps", "items": ["Photos " + AR + " videos " + AR + " real thing.", "Anxiety fades with practice."]},
  ]},
  {"title": "Behavioral Activation", "color": "teal", "blocks": [
   {"type": "def", "label": "Rule", "items": ["Act first, mood follows."]},
   {"type": "points", "label": "Do", "items": ["Schedule valued activities.", "Fights depression's inertia."]},
   {"type": "example", "label": "Example", "items": ["Daily 10-min walk + one call."]},
  ]},
 ],
 "footer": ["Thought-feeling-behavior loop", "Thought records", "Exposure ladder", "Act first"],
},
# ================= 7. DBT Skills =================
{
 "title": "DBT Skills",
 "subtitle": "Chapter - Dialectical Behavior Therapy",
 "sections": [
  {"title": "What Is DBT", "color": "blue", "blocks": [
   {"type": "def", "label": "Origin", "items": ["By Marsha Linehan for intense emotions."]},
   {"type": "points", "label": "For", "items": ["BPD, self-harm, emotional chaos.", "Skills beat willpower."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Skills over impulses."]},
  ]},
  {"title": "Mindfulness", "color": "green", "blocks": [
   {"type": "def", "label": "Core Skill", "items": ["Observe now, without judgment."]},
   {"type": "points", "label": "How", "items": ["'What': observe, describe.", "'How': non-judgmentally."]},
   {"type": "example", "label": "Example", "items": ["'Anger rising in chest' - pause."]},
  ]},
  {"title": "Distress Tolerance", "color": "orange", "blocks": [
   {"type": "def", "label": "Goal", "items": ["Survive crisis without damage."]},
   {"type": "points", "label": "TIPP", "items": ["Temperature: cold water, ice.", "Intense exercise, paced breathing.", "Paired muscle relaxation."]},
  ]},
  {"title": "ACCEPTS + Self-Soothe", "color": "yellow", "blocks": [
   {"type": "points", "label": "Distract Wisely", "items": ["ACCEPTS: activities, helping others.", "Self-soothe with 5 senses.", "Warm tea, music, soft blanket."]},
   {"type": "diagram", "diagram": "bars", "labels": ["Mindful", "Tolerate", "Regulate", "Relate"], "height": 120},
  ]},
  {"title": "Emotion Regulation", "color": "purple", "blocks": [
   {"type": "def", "label": "Goal", "items": ["Understand + change emotions."]},
   {"type": "points", "label": "Tools", "items": ["PLEASE: sleep, food, exercise.", "Opposite action: do the reverse."]},
   {"type": "example", "label": "Example", "items": ["Depressed " + AR + " call a friend."]},
  ]},
  {"title": "DEAR MAN", "color": "pink", "blocks": [
   {"type": "def", "label": "Ask Skill", "items": ["Describe, Express, Assert..."]},
   {"type": "points", "label": "Steps", "items": ["Reinforce, stay Mindful.", "Appear confident, Negotiate."]},
   {"type": "example", "label": "Example", "items": ["'Shift changed (D), I'm drained (E)...'"]},
  ]},
 ],
 "footer": ["Linehan = DBT", "TIPP for crisis", "Opposite action", "DEAR MAN asks"],
},
# ================= 8. ACT =================
{
 "title": "ACT: Acceptance & Commitment",
 "subtitle": "Chapter - Acceptance and Commitment Therapy",
 "sections": [
  {"title": "Core Idea", "color": "blue", "blocks": [
   {"type": "def", "label": "Radical Idea", "items": ["Struggle with pain IS the problem."]},
   {"type": "points", "label": "Key", "items": ["Fighting anxiety feeds it.", "Accept, then act."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Drop the rope."]},
  ]},
  {"title": "Defusion", "color": "green", "blocks": [
   {"type": "def", "label": "Skill", "items": ["Unhook from thoughts."]},
   {"type": "points", "label": "How", "items": ["'I am a failure' " + AR + " 'I notice the thought...'.", "Thoughts are words, not facts."]},
   {"type": "example", "label": "Example", "items": ["Say the thought in a silly voice."]},
  ]},
  {"title": "Acceptance", "color": "purple", "blocks": [
   {"type": "def", "label": "Skill", "items": ["Make room for feelings."]},
   {"type": "points", "label": "Not", "items": ["Not liking pain - allowing it.", "Waves pass faster when allowed."]},
  ]},
  {"title": "Being Present", "color": "orange", "blocks": [
   {"type": "def", "label": "Skill", "items": ["Contact the here and now."]},
   {"type": "points", "label": "Anchors", "items": ["Feet, breath, senses.", "Watch panic like weather."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Notice", "Anchor", "Allow"], "height": 120},
  ]},
  {"title": "Self-as-Context", "color": "teal", "blocks": [
   {"type": "def", "label": "Metaphor", "items": ["You are the sky, not the weather."]},
   {"type": "points", "label": "Shift", "items": ["'I experience anxiety' vs 'I am anxious'.", "Perspective frees identity."]},
  ]},
  {"title": "Values + Action", "color": "pink", "blocks": [
   {"type": "def", "label": "Core", "items": ["Values = chosen life directions."]},
   {"type": "points", "label": "Do", "items": ["Act despite discomfort.", "Values never 'finish'."]},
   {"type": "example", "label": "Example", "items": ["Value: presence " + AR + " phone away at dinner."]},
  ]},
 ],
 "footer": ["Defusion unhooks thoughts", "Acceptance allows pain", "Sky not weather", "Values guide action"],
},
# ================= 9. Solution-Focused Brief Therapy =================
{
 "title": "Solution-Focused Brief Therapy",
 "subtitle": "Chapter - Brief Therapies",
 "sections": [
  {"title": "Core Belief", "color": "blue", "blocks": [
   {"type": "def", "label": "Focus", "items": ["Solutions and strengths, not history."]},
   {"type": "points", "label": "Belief", "items": ["Clients already have strengths.", "Small changes snowball."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Future over past."]},
  ]},
  {"title": "Miracle Question", "color": "green", "blocks": [
   {"type": "def", "label": "Question", "items": ["'Miracle tonight - morning looks like?'"]},
   {"type": "points", "label": "Why", "items": ["Reveals the true goal.", "Makes hope concrete."]},
   {"type": "example", "label": "Example", "items": ["'I'd wake calm, smile at kids.'"]},
  ]},
  {"title": "Exceptions", "color": "purple", "blocks": [
   {"type": "def", "label": "Question", "items": ["Times the problem was absent."]},
   {"type": "points", "label": "Why", "items": ["Exceptions prove ability.", "Do more of what works."]},
   {"type": "example", "label": "Example", "items": ["'Which day had less arguing?'"]},
  ]},
  {"title": "Scaling", "color": "yellow", "blocks": [
   {"type": "def", "label": "Tool", "items": ["Rate 1-10, track change."]},
   {"type": "points", "label": "Ask", "items": ["'You're at 4 - what is a 5?'", "'How did you reach 4 from 3?'"]},
   {"type": "diagram", "diagram": "bars", "labels": ["1", "4", "7", "10"], "height": 120},
  ]},
  {"title": "Coping Questions", "color": "orange", "blocks": [
   {"type": "def", "label": "Question", "items": ["'How did you keep going?'"]},
   {"type": "points", "label": "Why", "items": ["Honors hidden resilience.", "Builds confidence."]},
  ]},
  {"title": "Compliments", "color": "pink", "blocks": [
   {"type": "def", "label": "Skill", "items": ["Notice real strengths sincerely."]},
   {"type": "points", "label": "Rules", "items": ["Not flattery - facts.", "Client hears own competence."]},
   {"type": "example", "label": "Example", "items": ["'You showed up in your hardest week.'"]},
  ]},
 ],
 "footer": ["Miracle question", "Exceptions", "Scaling 1-10", "Coping questions"],
},
# ================= 10. Person-Centered Counseling =================
{
 "title": "Person-Centered Counseling",
 "subtitle": "Chapter - Carl Rogers",
 "sections": [
  {"title": "Actualizing Tendency", "color": "blue", "blocks": [
   {"type": "def", "label": "Belief", "items": ["Inner drive toward growth."]},
   {"type": "points", "label": "Key", "items": ["People heal themselves.", "Therapist provides conditions."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Growth is natural."]},
  ]},
  {"title": "Unconditional Regard", "color": "green", "blocks": [
   {"type": "def", "label": "Condition 1", "items": ["Accept client fully, no judgment."]},
   {"type": "points", "label": "Why", "items": ["Prizing the person, not acts.", "Safety unlocks honesty."]},
   {"type": "example", "label": "Example", "items": ["Cheating confessed - warmth stays."]},
  ]},
  {"title": "Empathic Understanding", "color": "purple", "blocks": [
   {"type": "def", "label": "Condition 2", "items": ["Sense their inner world."]},
   {"type": "points", "label": "How", "items": ["'As if' it were yours.", "Reflect, don't interpret."]},
  ]},
  {"title": "Congruence", "color": "orange", "blocks": [
   {"type": "def", "label": "Condition 3", "items": ["Therapist is genuine."]},
   {"type": "points", "label": "Why", "items": ["No fake professional mask.", "Realness builds trust."]},
   {"type": "example", "label": "Example", "items": ["'Your story moves me.'"]},
  ]},
  {"title": "No Labels", "color": "pink", "blocks": [
   {"type": "points", "label": "Rogers Opposed", "items": ["Avoid diagnosis boxes.", "Client is expert on self.", "Reflection over interpretation."]},
  ]},
  {"title": "Conditions of Worth", "color": "teal", "blocks": [
   {"type": "def", "label": "Concept", "items": ["'Lovable only if...' messages."]},
   {"type": "points", "label": "Source", "items": ["Absorbed in childhood.", "Therapy: all feelings welcome."]},
   {"type": "diagram", "diagram": "venn", "labels": ["Regard", "Empathy", "Realness"], "height": 120},
  ]},
 ],
 "footer": ["Rogers = 3 conditions", "No labels", "Client is expert", "Conditions of worth"],
},
]

if __name__ == "__main__":
    import os
    outdir = "/home/hatch/workspace/zehen/batch4/inf-coun-cheat"
    os.makedirs(outdir, exist_ok=True)
    titles = ["Counseling vs Clinical vs Psychiatry","Active Listening","Reflecting Feelings",
              "Stages of the Counseling Process","Therapeutic Alliance","CBT Techniques",
              "DBT Skills","ACT: Acceptance & Commitment","Solution-Focused Brief Therapy",
              "Person-Centered Counseling"]
    for i, spec in enumerate(SPECS_1_10, 1):
        out = os.path.join(outdir, f"coun-{i:02d}.png")
        render_cheatsheet(spec, out)
        print("rendered", out, flush=True)
