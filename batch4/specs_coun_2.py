#!/usr/bin/env python3
"""Cheat-sheet specs for 20 Counseling & Therapy infographics (part 2: 11-20)."""
import sys
sys.path.insert(0, '/home/hatch/workspace/zehen/batch4')
from cheatsheet import render_cheatsheet

AR = "\u2192"  # →

SPECS_11_20 = [
# ================= 11. Gestalt Therapy =================
{
 "title": "Gestalt Therapy",
 "subtitle": "Chapter - Here and Now",
 "sections": [
  {"title": "Here and Now", "color": "blue", "blocks": [
   {"type": "def", "label": "Focus", "items": ["Present moment, not past analysis."]},
   {"type": "points", "label": "Key", "items": ["Awareness itself creates change.", "Feel it now, not then."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Now is power."]},
  ]},
  {"title": "Empty Chair", "color": "green", "blocks": [
   {"type": "def", "label": "Technique", "items": ["Talk to an imagined person."]},
   {"type": "points", "label": "Steps", "items": ["Say the unsaid aloud.", "Then sit in their chair."]},
   {"type": "example", "label": "Example", "items": ["Tell late father the goodbye."]},
  ]},
  {"title": "Exaggeration", "color": "orange", "blocks": [
   {"type": "def", "label": "Technique", "items": ["Amplify the gesture or feeling."]},
   {"type": "points", "label": "Why", "items": ["Foot tap " + AR + " stomp it out.", "Body reveals hidden truth."]},
   {"type": "example", "label": "Example", "items": ["Stomping releases buried anger."]},
  ]},
  {"title": "Stay With Feeling", "color": "purple", "blocks": [
   {"type": "def", "label": "Skill", "items": ["Remain inside the emotion."]},
   {"type": "points", "label": "Ask", "items": ["Don't explain pain away.", "'What does the tightness say?'"]},
   {"type": "diagram", "diagram": "cycle", "labels": ["Feel", "Stay", "Express", "Free"], "height": 120},
  ]},
  {"title": "Top Dog vs Underdog", "color": "red", "blocks": [
   {"type": "def", "label": "Inner War", "items": ["Critical 'should' vs rebel voice."]},
   {"type": "points", "label": "Voices", "items": ["Top dog: 'Be perfect!'", "Underdog: 'I'll try tomorrow.'"]},
   {"type": "example", "label": "Example", "items": ["Name both, then choose freely."]},
  ]},
  {"title": "Responsibility Talk", "color": "teal", "blocks": [
   {"type": "def", "label": "Language Shift", "items": ["'I can't' " + AR + " 'I won't'."]},
   {"type": "points", "label": "Own It", "items": ["'Makes me angry' " + AR + " 'I feel angry'.", "Choice returns power."]},
   {"type": "example", "label": "Example", "items": ["'I stay in this job, feeling stuck.'"]},
  ]},
 ],
 "footer": ["Here and now", "Empty chair", "Exaggeration", "Top dog vs underdog"],
},
# ================= 12. Couples Counseling =================
{
 "title": "Couples Counseling",
 "subtitle": "Chapter - Love and Conflict",
 "sections": [
  {"title": "Gottman's Lab", "color": "blue", "blocks": [
   {"type": "def", "label": "Research", "items": ["Predicts divorce with 90%+ accuracy."]},
   {"type": "points", "label": "How", "items": ["15-minute argument analyzed.", "Contempt = top predictor."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Contempt kills love."]},
  ]},
  {"title": "Four Horsemen", "color": "red", "blocks": [
   {"type": "points", "label": "Killers", "items": ["Criticism: attacks character.", "Contempt: mockery, disgust.", "Defensiveness + stonewalling."]},
   {"type": "diagram", "diagram": "bars", "labels": ["Critic", "Contempt", "Defend", "Stone"], "height": 120},
  ]},
  {"title": "Complaint vs Criticism", "color": "green", "blocks": [
   {"type": "def", "label": "Difference", "items": ["Behavior complaint vs character attack."]},
   {"type": "points", "label": "Say", "items": ["Criticism: 'You never care.'", "Complaint: 'I felt lonely when...'"]},
   {"type": "example", "label": "Example", "items": ["Target acts, not the person."]},
  ]},
  {"title": "EFT", "color": "purple", "blocks": [
   {"type": "def", "label": "Model", "items": ["Sue Johnson: attachment needs."]},
   {"type": "points", "label": "Under Fights", "items": ["Chore fights hide fear of loss.", "'I'm terrified of failing you.'"]},
   {"type": "example", "label": "Example", "items": ["Anger melts " + AR + " closeness."]},
  ]},
  {"title": "5:1 Ratio", "color": "yellow", "blocks": [
   {"type": "def", "label": "Rule", "items": ["5 positives per 1 negative."]},
   {"type": "points", "label": "Daily", "items": ["Small kindnesses count most.", "6-second kiss, real listening."]},
   {"type": "example", "label": "Example", "items": ["Thank-yous beat grand gestures."]},
  ]},
  {"title": "Repair Attempts", "color": "teal", "blocks": [
   {"type": "def", "label": "Skill", "items": ["De-escalate mid-fight."]},
   {"type": "points", "label": "Tools", "items": ["Humor, touch, pause.", "'Same team, remember?'"]},
   {"type": "example", "label": "Example", "items": ["Repair accepted " + AR + " bond grows."]},
  ]},
 ],
 "footer": ["4 horsemen", "Complaint not criticism", "5:1 ratio", "Repair attempts"],
},
# ================= 13. Group Counseling =================
{
 "title": "Group Counseling",
 "subtitle": "Chapter - Healing Together",
 "sections": [
  {"title": "Why Groups Work", "color": "blue", "blocks": [
   {"type": "def", "label": "Format", "items": ["6-10 clients, 1-2 leaders."]},
   {"type": "points", "label": "Benefits", "items": ["Cost-effective + powerful.", "Practice real social skills."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Alone together, healing."]},
  ]},
  {"title": "Yalom Factors 1", "color": "green", "blocks": [
   {"type": "points", "label": "Healing Forces", "items": ["Universality: 'I'm not alone'.", "Altruism: helping heals helper.", "Hope: seeing others improve."]},
   {"type": "example", "label": "Example", "items": ["Widow hears her exact grief."]},
  ]},
  {"title": "Yalom Factors 2", "color": "purple", "blocks": [
   {"type": "points", "label": "More Forces", "items": ["Catharsis: emotional release.", "Social learning by watching.", "Group replays family patterns."]},
  ]},
  {"title": "Group Stages", "color": "orange", "blocks": [
   {"type": "points", "label": "Stages", "items": ["Forming: polite, anxious.", "Storming: conflict, testing.", "Norming " + AR + " performing."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Form", "Storm", "Norm", "Perform"], "height": 120},
  ]},
  {"title": "Leader's Job", "color": "teal", "blocks": [
   {"type": "points", "label": "Duties", "items": ["Set norms: privacy, attendance.", "Balance airtime fairly.", "Protect quiet members."]},
   {"type": "example", "label": "Example", "items": ["'Ali went quiet - what's up?'"]},
  ]},
  {"title": "Screening", "color": "red", "blocks": [
   {"type": "def", "label": "Rule", "items": ["Not everyone fits group."]},
   {"type": "points", "label": "Exclude", "items": ["Acute crisis or psychosis.", "Refer to individual first.", "Match needs to format."]},
  ]},
 ],
 "footer": ["Yalom factors", "Form-storm-norm-perform", "Universality", "Screen members"],
},
# ================= 14. Play Therapy =================
{
 "title": "Play Therapy",
 "subtitle": "Chapter - Children Heal Through Play",
 "sections": [
  {"title": "Core Truth", "color": "blue", "blocks": [
   {"type": "def", "label": "Idea", "items": ["Children heal through play."]},
   {"type": "points", "label": "Why", "items": ["Play = child's language.", "Best for ages 3-12."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Toys are words."]},
  ]},
  {"title": "Child-Centered", "color": "green", "blocks": [
   {"type": "def", "label": "Axline Model", "items": ["Follow the child's lead."]},
   {"type": "points", "label": "How", "items": ["Accept, don't direct.", "Narrate: 'baby doll hides, scared'."]},
   {"type": "example", "label": "Example", "items": ["Car crashes = divorce feelings."]},
  ]},
  {"title": "Directive Play", "color": "orange", "blocks": [
   {"type": "def", "label": "Model", "items": ["Structured for goals."]},
   {"type": "points", "label": "Use", "items": ["Feeling puppets for anxiety.", "Planned activities, targets."]},
   {"type": "example", "label": "Example", "items": ["Brave puppet practices courage."]},
  ]},
  {"title": "The Playroom", "color": "purple", "blocks": [
   {"type": "points", "label": "Stocked With", "items": ["Real-life: dollhouse, kitchen.", "Aggressive: bop bag, darts.", "Creative: paint, sand."]},
   {"type": "diagram", "diagram": "bars", "labels": ["Real", "Wild", "Create"], "height": 120},
  ]},
  {"title": "Sand Tray", "color": "teal", "blocks": [
   {"type": "def", "label": "Method", "items": ["Build worlds in miniature."]},
   {"type": "points", "label": "Why", "items": ["Figures + sand = story.", "Makes inner world visible."]},
   {"type": "example", "label": "Example", "items": ["Lone figure, sharks around."]},
  ]},
  {"title": "Filial Therapy", "color": "pink", "blocks": [
   {"type": "def", "label": "Model", "items": ["Parents do play sessions."]},
   {"type": "points", "label": "Format", "items": ["30 minutes weekly at home.", "Reflect feelings in play."]},
   {"type": "example", "label": "Example", "items": ["Tantrums drop within weeks."]},
  ]},
 ],
 "footer": ["Play = language", "Child-centered: follow lead", "Sand tray", "Filial therapy"],
},
# ================= 15. Crisis Intervention =================
{
 "title": "Crisis Intervention",
 "subtitle": "Chapter - When Coping Collapses",
 "sections": [
  {"title": "What Is Crisis", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Coping collapses under sudden shock."]},
   {"type": "points", "label": "Triggers", "items": ["Death, assault, failure.", "Not illness - overload."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Stabilize first."]},
  ]},
  {"title": "ABC Model", "color": "green", "blocks": [
   {"type": "def", "label": "Model", "items": ["A: rapport, B: boil down, C: cope."]},
   {"type": "points", "label": "Steps", "items": ["A: 'I'm here, you're safe.'", "B: find the core problem.", "C: plan next small steps."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Rapport", "Problem", "Cope"], "height": 120},
  ]},
  {"title": "Safety First", "color": "red", "blocks": [
   {"type": "def", "label": "Rule", "items": ["Ask about suicide directly."]},
   {"type": "points", "label": "Facts", "items": ["Asking does NOT plant ideas.", "Assess plan + means."]},
   {"type": "example", "label": "Example", "items": ["Pills admitted " + AR + " safety plan."]},
  ]},
  {"title": "Safety Plan", "color": "orange", "blocks": [
   {"type": "points", "label": "Include", "items": ["Warning signs listed.", "Coping + distracting steps.", "Trusted contacts, helpline."]},
   {"type": "example", "label": "Example", "items": ["Sister call, park walk."]},
  ]},
  {"title": "Psychological First Aid", "color": "purple", "blocks": [
   {"type": "def", "label": "WHO Model", "items": ["Look, Listen, Link."]},
   {"type": "points", "label": "Do", "items": ["Calm presence, no pressure.", "Water, quiet, helpline numbers."]},
  ]},
  {"title": "Counselor Care", "color": "teal", "blocks": [
   {"type": "points", "label": "After Crisis", "items": ["Debrief with supervisor.", "Process your own feelings.", "Walk, journal, rest."]},
   {"type": "example", "label": "Example", "items": ["Call supervisor after session."]},
  ]},
 ],
 "footer": ["ABC model", "Ask directly about suicide", "Safety plan", "Look-Listen-Link"],
},
# ================= 16. Grief Counseling =================
{
 "title": "Grief Counseling",
 "subtitle": "Chapter - Walking With Loss",
 "sections": [
  {"title": "Grief Is Normal", "color": "blue", "blocks": [
   {"type": "def", "label": "Truth", "items": ["Healthy response to loss."]},
   {"type": "points", "label": "Note", "items": ["Not just death: divorce, loss.", "Waves, not fixed order."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Grief = love remains."]},
  ]},
  {"title": "Five Stages", "color": "purple", "blocks": [
   {"type": "points", "label": "Kubler-Ross", "items": ["Denial, anger, bargaining.", "Depression, acceptance.", "Not linear - loops back."]},
   {"type": "diagram", "diagram": "bars", "labels": ["Deny", "Anger", "Bargain", "Accept"], "height": 120},
  ]},
  {"title": "Worden's Tasks", "color": "green", "blocks": [
   {"type": "def", "label": "4 Tasks", "items": ["Give grief direction."]},
   {"type": "points", "label": "Tasks", "items": ["Accept reality of loss.", "Process the pain.", "Adjust + find new meaning."]},
   {"type": "example", "label": "Example", "items": ["Scholarship in mom's name."]},
  ]},
  {"title": "Complicated Grief", "color": "red", "blocks": [
   {"type": "def", "label": "Warning", "items": ["Stuck for over a year."]},
   {"type": "points", "label": "Signs", "items": ["Intense yearning persists.", "Daily life stays impaired."]},
   {"type": "example", "label": "Example", "items": ["Sets his plate, 2 years on."]},
  ]},
  {"title": "What Helps", "color": "teal", "blocks": [
   {"type": "points", "label": "Do", "items": ["'I'm here' beats cliches.", "Let them retell stories.", "Presence over platitudes."]},
   {"type": "example", "label": "Example", "items": ["'Tell me about him.'"]},
  ]},
  {"title": "What Harms", "color": "orange", "blocks": [
   {"type": "points", "label": "Don't", "items": ["Don't rush: 'move on'.", "Don't compare losses.", "Don't spiritual-bypass."]},
   {"type": "example", "label": "Example", "items": ["Bad: 'At least you have others.'"]},
  ]},
 ],
 "footer": ["5 stages (not linear)", "Worden's 4 tasks", "Presence over platitudes", "Complicated grief"],
},
# ================= 17. Trauma-Informed Counseling =================
{
 "title": "Trauma-Informed Counseling",
 "subtitle": "Chapter - Safety Before Story",
 "sections": [
  {"title": "Core Shift", "color": "blue", "blocks": [
   {"type": "def", "label": "New Question", "items": ["'What happened?' not 'what's wrong?'"]},
   {"type": "points", "label": "Assume", "items": ["Trauma is common.", "Behavior makes sense."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Safety before story."]},
  ]},
  {"title": "Safety First", "color": "green", "blocks": [
   {"type": "def", "label": "Principle 1", "items": ["Physical + emotional safety."]},
   {"type": "points", "label": "Do", "items": ["Predictable routines.", "Explain every step."]},
   {"type": "example", "label": "Example", "items": ["'You can skip anything.'"]},
  ]},
  {"title": "Trust & Transparency", "color": "purple", "blocks": [
   {"type": "def", "label": "Principle 2", "items": ["Keep promises, explain choices."]},
   {"type": "points", "label": "Do", "items": ["Sessions start/end on time.", "Reliability heals deeply."]},
  ]},
  {"title": "Choice & Voice", "color": "orange", "blocks": [
   {"type": "def", "label": "Principle 3", "items": ["Return stolen control."]},
   {"type": "points", "label": "Do", "items": ["Offer real options.", "Collaborate, don't dictate."]},
   {"type": "example", "label": "Example", "items": ["'Breathe or talk - your pick?'"]},
  ]},
  {"title": "Empowerment", "color": "pink", "blocks": [
   {"type": "def", "label": "Principle 4", "items": ["Highlight strengths."]},
   {"type": "points", "label": "Frame", "items": ["Survivor, not victim.", "Skills over symptoms."]},
   {"type": "example", "label": "Example", "items": ["'You protected siblings - courage.'"]},
  ]},
  {"title": "Avoid Re-trauma", "color": "red", "blocks": [
   {"type": "points", "label": "Never", "items": ["Never force trauma details.", "Watch dissociation: glazed eyes.", "Pause + ground when frozen."]},
   {"type": "diagram", "diagram": "pyramid", "labels": ["Safety", "Trust", "Choice", "Power", "Culture"], "height": 130},
  ]},
 ],
 "footer": ["What happened?", "5 principles", "Choice returns control", "Never force details"],
},
# ================= 18. Addiction Counseling =================
{
 "title": "Addiction Counseling",
 "subtitle": "Chapter - Brain, Change, Recovery",
 "sections": [
  {"title": "Brain Hijack", "color": "blue", "blocks": [
   {"type": "def", "label": "Science", "items": ["Drugs flood dopamine circuits."]},
   {"type": "points", "label": "Result", "items": ["Brain adapts, needs more.", "Not weakness - wiring."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Treat brain, not blame."]},
  ]},
  {"title": "Stages of Change", "color": "green", "blocks": [
   {"type": "points", "label": "Prochaska", "items": ["Precontemplation: 'no problem'.", "Contemplation " + AR + " preparation.", "Action " + AR + " maintenance."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Deny", "Think", "Plan", "Act"], "height": 120},
  ]},
  {"title": "Motivational Interviewing", "color": "purple", "blocks": [
   {"type": "def", "label": "Style", "items": ["Meet them where they are."]},
   {"type": "points", "label": "Tools", "items": ["Open questions, affirm.", "Reflect, don't lecture."]},
   {"type": "example", "label": "Example", "items": ["'What worries you about drinking?'"]},
  ]},
  {"title": "Decisional Balance", "color": "orange", "blocks": [
   {"type": "def", "label": "Tool", "items": ["Good vs bad of using AND quitting."]},
   {"type": "points", "label": "How", "items": ["Explore ambivalence honestly.", "Client weighs, not you."]},
   {"type": "example", "label": "Example", "items": ["'Relax vs marriage + health.'"]},
  ]},
  {"title": "Relapse Prevention", "color": "red", "blocks": [
   {"type": "def", "label": "Marlatt Model", "items": ["Map high-risk situations."]},
   {"type": "points", "label": "Watch", "items": ["People, places, feelings.", "HALT: Hungry, Angry, Lonely, Tired.", "Lapse is not collapse."]},
   {"type": "example", "label": "Example", "items": ["Friday loneliness " + AR + " gym plan."]},
  ]},
  {"title": "MAT + Counseling", "color": "teal", "blocks": [
   {"type": "def", "label": "Best Combo", "items": ["Medicines + therapy together."]},
   {"type": "points", "label": "Meds", "items": ["Methadone, buprenorphine.", "Recovery with dignity."]},
   {"type": "example", "label": "Example", "items": ["Job held, counseling kept."]},
  ]},
 ],
 "footer": ["Stages of change", "Motivational interviewing", "HALT triggers", "Lapse not collapse"],
},
# ================= 19. Counseling Ethics =================
{
 "title": "Counseling Ethics",
 "subtitle": "Chapter - Trust Is Sacred",
 "sections": [
  {"title": "Why Ethics", "color": "blue", "blocks": [
   {"type": "def", "label": "Reason", "items": ["Clients are vulnerable."]},
   {"type": "points", "label": "Why", "items": ["Secrets shared, power gap.", "Codes: APA, ACA, BACP."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Trust is sacred."]},
  ]},
  {"title": "Autonomy", "color": "green", "blocks": [
   {"type": "def", "label": "Principle", "items": ["Client chooses their path."]},
   {"type": "points", "label": "Practice", "items": ["Even when you disagree.", "Explore, don't steer."]},
   {"type": "example", "label": "Example", "items": ["Stays in marriage - respected."]},
  ]},
  {"title": "Do Good, No Harm", "color": "purple", "blocks": [
   {"type": "points", "label": "Two Duties", "items": ["Beneficence: promote welfare.", "Nonmaleficence: avoid harm.", "Refer out if untrained."]},
   {"type": "example", "label": "Example", "items": ["Eating disorder " + AR + " specialist."]},
  ]},
  {"title": "Justice", "color": "orange", "blocks": [
   {"type": "def", "label": "Principle", "items": ["Fair care for everyone."]},
   {"type": "points", "label": "Practice", "items": ["Same quality, any background.", "Advocate for access."]},
   {"type": "example", "label": "Example", "items": ["Executive = street vendor care."]},
  ]},
  {"title": "Fidelity", "color": "teal", "blocks": [
   {"type": "def", "label": "Principle", "items": ["Keep promises, stay loyal."]},
   {"type": "points", "label": "Practice", "items": ["Honest about limits.", "No gossip, no fee games."]},
   {"type": "diagram", "diagram": "bars", "labels": ["Autonomy", "Benefic", "Justice", "Fidelity"], "height": 120},
  ]},
  {"title": "Dilemmas", "color": "red", "blocks": [
   {"type": "def", "label": "Reality", "items": ["Principles can collide."]},
   {"type": "points", "label": "Do", "items": ["Teen self-harm: privacy vs safety.", "Consult supervisor always.", "Document your reasoning."]},
  ]},
 ],
 "footer": ["Autonomy", "Beneficence + nonmaleficence", "Justice", "Fidelity"],
},
# ================= 20. Confidentiality & Its Limits =================
{
 "title": "Confidentiality & Its Limits",
 "subtitle": "Chapter - Private, With 3 Exceptions",
 "sections": [
  {"title": "The Foundation", "color": "blue", "blocks": [
   {"type": "def", "label": "Why", "items": ["Privacy makes honesty possible."]},
   {"type": "points", "label": "Key", "items": ["Darkest truths need safety.", "Explained at session one."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Private, with 3 exceptions."]},
  ]},
  {"title": "Informed Consent", "color": "green", "blocks": [
   {"type": "def", "label": "Rule", "items": ["Limits told upfront."]},
   {"type": "points", "label": "How", "items": ["Before sharing begins.", "Written + verbal."]},
   {"type": "example", "label": "Example", "items": ["'3 exceptions - let me explain.'"]},
  ]},
  {"title": "Limit 1: Self-Harm", "color": "red", "blocks": [
   {"type": "def", "label": "Trigger", "items": ["Imminent suicide " + AR + " act."]},
   {"type": "points", "label": "Do", "items": ["Stay with the client.", "Contact emergency help."]},
   {"type": "example", "label": "Example", "items": ["Tonight's plan " + AR + " intervene."]},
  ]},
  {"title": "Limit 2: Harm to Others", "color": "orange", "blocks": [
   {"type": "def", "label": "Tarasoff Duty", "items": ["Warn the threatened person."]},
   {"type": "points", "label": "Do", "items": ["Credible threat " + AR + " warn victim.", "Notify authorities."]},
   {"type": "example", "label": "Example", "items": ["Names ex-wife + weapon " + AR + " warn."]},
  ]},
  {"title": "Limit 3: Abuse", "color": "purple", "blocks": [
   {"type": "def", "label": "Trigger", "items": ["Child/elder abuse " + AR + " report."]},
   {"type": "points", "label": "Do", "items": ["Mandatory reporting laws.", "Report the same day."]},
   {"type": "diagram", "diagram": "bars", "labels": ["Self", "Others", "Abuse"], "height": 120},
  ]},
  {"title": "Breaking It Right", "color": "teal", "blocks": [
   {"type": "points", "label": "When You Must", "items": ["Tell client when safe.", "Explain what + why.", "Share minimum necessary."]},
   {"type": "example", "label": "Example", "items": ["'Calling your brother to keep you safe.'"]},
  ]},
 ],
 "footer": ["Consent first", "Self-harm", "Harm to others", "Abuse reporting"],
},
]

if __name__ == "__main__":
    import os
    outdir = "/home/hatch/workspace/zehen/batch4/inf-coun-cheat"
    os.makedirs(outdir, exist_ok=True)
    for i, spec in enumerate(SPECS_11_20, 11):
        out = os.path.join(outdir, f"coun-{i:02d}.png")
        render_cheatsheet(spec, out)
        print("rendered", out, flush=True)
