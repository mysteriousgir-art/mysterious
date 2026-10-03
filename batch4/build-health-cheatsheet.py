#!/usr/bin/env python3
"""Regenerate 20 Health Psychology infographics in cheat-sheet style (overwrite)."""
import json, os, sys, urllib.request

sys.path.insert(0, "/home/hatch/workspace/zehen/batch4")
from cheatsheet import render_cheatsheet

OUT_DIR = "/home/hatch/workspace/zehen/batch4/inf-health-cheat"
ARROW = "\u2192"  # → always use this, never ->

def load_env():
    env = {}
    with open("/home/hatch/workspace/zehen/.env.supabase") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env

def upload_file(base_url, key, fname, path):
    with open(path, "rb") as f:
        data = f.read()
    req = urllib.request.Request(
        f"{base_url}/storage/v1/object/infographics/{fname}",
        data=data, method="POST",
        headers={"apikey": key, "Authorization": f"Bearer {key}",
                 "Content-Type": "image/png", "x-upsert": "true"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status

def check_url(url):
    req = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status

SPECS = [
# ================= 1. The Biopsychosocial Model =================
{
 "title": "The Biopsychosocial Model",
 "subtitle": "Health Psychology \u00b7 Core Models",
 "sections": [
  {"title": "The Model", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": [
      "Health = biology + psychology + social factors.",
      "Proposed by George Engel in 1977."]},
    {"type": "revision", "label": "Instant Revision", "items": [
      "Bio + Psycho + Social = whole person."]},
  ]},
  {"title": "Three Factors", "color": "green", "blocks": [
    {"type": "diagram", "diagram": "pyramid", "labels": ["Biological", "Psychological", "Social"], "height": 150},
    {"type": "points", "label": "Examples", "items": [
      "Biological: genes, viruses, brain chemistry.",
      "Psychological: stress, beliefs, emotions.",
      "Social: family, culture, income."]},
  ]},
  {"title": "Why It Matters", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Stress weakens the immune system.",
      "Poverty limits access to care.",
      "Hope and optimism speed recovery."]},
    {"type": "example", "label": "Example", "items": [
      "Same flu: rested recovers in 3 days,",
      "stressed stays sick for 2 weeks."]},
  ]},
  {"title": "Treatment", "color": "teal", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Treat all three levels together.",
      "Medicine alone often fails.",
      "Pain, cardiac, cancer teams use it."]},
    {"type": "example", "label": "Example", "items": [
      "Diabetes: insulin + stress counseling",
      "+ family meal plan."]},
  ]},
  {"title": "Prevention", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Vaccines cover the biology.",
      "Education changes beliefs.",
      "Community shifts social norms."]},
    {"type": "example", "label": "Example", "items": [
      "Quits smoking: health scare + belief",
      "+ wife's daily support."]},
  ]},
  {"title": "Patient Respect", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Mind and society cause real effects.",
      "Reduces blame and stigma.",
      "Illness is never personal failure."]},
    {"type": "example", "label": "Example", "items": [
      "'Stress worsens your real pain \u2014",
      "let's treat both.'"]},
  ]},
 ],
 "footer": ["Engel 1977", "3 interacting factors", "Beyond medical model", "Team care"],
},
# ================= 2. Health Belief Model =================
{
 "title": "Health Belief Model",
 "subtitle": "Health Psychology \u00b7 Why We Act",
 "sections": [
  {"title": "The Model", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": [
      "We act when risk feels real and",
      "the illness feels serious."]},
    {"type": "revision", "label": "Instant Revision", "items": [
      "Risk + Seriousness \u2192 Action."]},
  ]},
  {"title": "Core Beliefs", "color": "green", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Threat", "Benefits", "Barriers", "Action"], "height": 130},
    {"type": "points", "label": "Key Points", "items": [
      "Susceptibility: 'it could hit me.'",
      "Severity: 'it would be bad.'",
      "Benefits must beat barriers."]},
  ]},
  {"title": "Cues to Action", "color": "yellow", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Reminder texts and media ads.",
      "A friend's diagnosis.",
      "Doctor's direct advice."]},
    {"type": "example", "label": "Example", "items": [
      "Celebrity heart attack \u2192 thousands",
      "get cholesterol checks."]},
  ]},
  {"title": "Self-Efficacy", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": [
      "Confidence that YOU can do it.",
      "Added to the model later."]},
    {"type": "example", "label": "Example", "items": [
      "'I can say no at parties' \u2192",
      "refuses cigarettes."]},
  ]},
  {"title": "Why Warnings Fail", "color": "red", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Optimistic bias: 'not me.'",
      "Low felt risk blocks action.",
      "Emotions beat logic."]},
    {"type": "example", "label": "Example", "items": [
      "'Grandpa smoked to 90' \u2192",
      "keeps smoking."]},
  ]},
  {"title": "Campaign Design", "color": "teal", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Raise risk awareness.",
      "Show clear benefits.",
      "Cut barriers + add reminders."]},
    {"type": "example", "label": "Example", "items": [
      "Real stories + free clinic",
      "+ SMS reminders."]},
  ]},
 ],
 "footer": ["Susceptibility & severity", "Benefits vs barriers", "Cues to action", "Self-efficacy"],
},
# ================= 3. Pain Psychology =================
{
 "title": "Pain Psychology",
 "subtitle": "Health Psychology \u00b7 Understanding Pain",
 "sections": [
  {"title": "Pain Is Brain-Made", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": [
      "Pain = tissue signals + emotions",
      "+ beliefs + past experience."]},
    {"type": "example", "label": "Example", "items": [
      "Same back injury: one returns",
      "to work in a week."]},
  ]},
  {"title": "Gate Control", "color": "green", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Signal", "Gate", "Brain", "Feeling"], "height": 130},
    {"type": "points", "label": "Melzack & Wall", "items": [
      "Spinal 'gate' tunes pain up/down.",
      "Distraction closes the gate.",
      "Anxiety opens it wider."]},
  ]},
  {"title": "Fear-Avoidance", "color": "red", "blocks": [
    {"type": "diagram", "diagram": "cycle", "labels": ["Pain", "Fear", "Avoid", "Weaker"], "height": 150},
    {"type": "points", "label": "Key Points", "items": [
      "'Hurt = harm' belief disables.",
      "Avoidance \u2192 stiffness, low mood.",
      "Graded movement breaks cycle."]},
  ]},
  {"title": "Treatments", "color": "teal", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "CBT for catastrophic thoughts.",
      "Relaxation + biofeedback.",
      "Mindfulness + graded exercise."]},
    {"type": "example", "label": "Example", "items": [
      "Trigger diary + relaxation \u2192",
      "migraines halved."]},
  ]},
  {"title": "Children's Pain", "color": "yellow", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Anxious parents \u2192 more child pain.",
      "Distraction: blowing bubbles.",
      "Praise calm coping."]},
    {"type": "example", "label": "Example", "items": [
      "Sticker for brave dentist visit",
      "\u2192 less fear next time."]},
  ]},
  {"title": "Chronic Pain Care", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Fibromyalgia pain is real.",
      "Validation beats dismissal.",
      "Team: doctor + psychologist + physio."]},
    {"type": "revision", "label": "Instant Revision", "items": [
      "Pain lives in the whole person."]},
  ]},
 ],
 "footer": ["Gate control theory", "Fear-avoidance cycle", "CBT for pain", "Team care"],
},
# ================= 4. Sleep and Health =================
{
 "title": "Sleep and Health",
 "subtitle": "Health Psychology \u00b7 Rest & Repair",
 "sections": [
  {"title": "Why Sleep Matters", "color": "blue", "blocks": [
    {"type": "def", "label": "Key Fact", "items": [
      "Under 6 hours \u2192 obesity, diabetes,",
      "heart disease, depression."]},
    {"type": "example", "label": "Example", "items": [
      "Night-shift nurse: BP up,",
      "weight up, mood down."]},
  ]},
  {"title": "Memory & Study", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Deep sleep stores learning.",
      "All-nighters destroy recall.",
      "Sleep IS part of studying."]},
    {"type": "example", "label": "Example", "items": [
      "8-hour sleeper beats the",
      "all-nighter in exams."]},
  ]},
  {"title": "Sleep Stages", "color": "green", "blocks": [
    {"type": "diagram", "diagram": "cycle", "labels": ["Light", "Deep", "REM", "Wake"], "height": 150},
    {"type": "points", "label": "Key Points", "items": [
      "Cycle repeats every ~90 minutes.",
      "REM = dreaming stage."]},
  ]},
  {"title": "Screens & Sleep", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Blue light kills melatonin.",
      "Scrolling keeps brain alert.",
      "30\u201360 min screen curfew."]},
    {"type": "example", "label": "Example", "items": [
      "Scrolling to 2 AM \u2192",
      "cannot fall asleep."]},
  ]},
  {"title": "Best Fixes", "color": "teal", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Fixed wake time anchors clock.",
      "Bed = sleep only (CBT-I).",
      "Write worries down earlier."]},
    {"type": "example", "label": "Example", "items": [
      "Strict 6:30 AM wake \u2192 sleep",
      "fixed in 2 weeks."]},
  ]},
  {"title": "Sleep Apnea", "color": "red", "blocks": [
    {"type": "points", "label": "Warning Signs", "items": [
      "Loud snoring + gasping.",
      "Daytime sleepiness, BP risk.",
      "CPAP transforms lives."]},
    {"type": "example", "label": "Example", "items": [
      "Falls asleep driving \u2192",
      "apnea starved his brain."]},
  ]},
 ],
 "footer": ["7\u20139 hours needed", "CBT-I beats pills", "Fixed wake time", "Apnea signs"],
},
# ================= 5. Exercise and Mental Health =================
{
 "title": "Exercise and Mental Health",
 "subtitle": "Health Psychology \u00b7 Move to Heal",
 "sections": [
  {"title": "Natural Medicine", "color": "green", "blocks": [
    {"type": "def", "label": "Key Fact", "items": [
      "Exercise \u2248 medication for mild",
      "to moderate depression."]},
    {"type": "points", "label": "How", "items": [
      "Boosts serotonin + endorphins.",
      "Raises BDNF (brain growth).",
      "Improves sleep quality."]},
  ]},
  {"title": "Anxiety Relief", "color": "blue", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "20-min walk calms nerves fast.",
      "Burns off stress hormones.",
      "Body learns to handle arousal."]},
    {"type": "example", "label": "Example", "items": [
      "Jog before exams \u2192",
      "calmer, sharper focus."]},
  ]},
  {"title": "Benefits Compared", "color": "orange", "blocks": [
    {"type": "diagram", "diagram": "bars", "labels": ["Mood", "Anxiety", "Sleep", "Memory"], "height": 150},
    {"type": "points", "label": "Key Points", "items": [
      "Helps every age group.",
      "Protects the aging brain."]},
  ]},
  {"title": "Start Small", "color": "yellow", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Begin with 10-minute walks.",
      "Too much \u2192 injury \u2192 quit.",
      "Enjoyment beats intensity."]},
    {"type": "example", "label": "Example", "items": [
      "Intense daily start \u2192",
      "quits in 2 weeks."]},
  ]},
  {"title": "Make It Stick", "color": "teal", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Walk with a friend.",
      "Schedule like meetings.",
      "Track streaks, prep clothes."]},
    {"type": "example", "label": "Example", "items": [
      "App streaks \u2192 years",
      "of steady habit."]},
  ]},
  {"title": "Aging Brain", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Slows cognitive decline.",
      "Lowers dementia risk.",
      "Keeps balance + independence."]},
    {"type": "example", "label": "Example", "items": [
      "Twice-weekly training \u2192",
      "fewer falls, longer freedom."]},
  ]},
 ],
 "footer": ["30 min daily", "Start small", "Social exercise sticks", "BDNF boost"],
},
# ================= 6. Nutrition and Mood =================
{
 "title": "Nutrition and Mood",
 "subtitle": "Health Psychology \u00b7 Food & Feelings",
 "sections": [
  {"title": "Blood Sugar Swings", "color": "orange", "blocks": [
    {"type": "def", "label": "Key Fact", "items": [
      "Sugar crashes \u2192 irritability,",
      "anxiety, foggy brain."]},
    {"type": "points", "label": "Key Points", "items": [
      "Skipped meals = unstable mood.",
      "Caffeine overload mimics panic.",
      "Stable meals = stable mood."]},
  ]},
  {"title": "Brain Foods", "color": "green", "blocks": [
    {"type": "diagram", "diagram": "bars", "labels": ["Omega-3", "Vit D", "B12", "Folate"], "height": 150},
    {"type": "points", "label": "Key Points", "items": [
      "Mediterranean diet \u2193 depression.",
      "Fish, greens, whole grains.",
      "Supports care, not replaces it."]},
  ]},
  {"title": "Hidden Deficiencies", "color": "red", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Low B12 \u2192 confusion, depression.",
      "Low iron \u2192 fatigue, low mood.",
      "Low vitamin D \u2192 depression."]},
    {"type": "example", "label": "Example", "items": [
      "Iron treatment \u2192 'herself",
      "again' in weeks."]},
  ]},
  {"title": "Gut-Brain Axis", "color": "teal", "blocks": [
    {"type": "def", "label": "Definition", "items": [
      "Gut bacteria talk to the brain",
      "via vagus nerve."]},
    {"type": "points", "label": "Key Points", "items": [
      "Fiber + probiotics lift mood.",
      "IBS and anxiety linked."]},
  ]},
  {"title": "Food & Emotions", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Family meals protect mood.",
      "Rigid food rules harm.",
      "No 'good' vs 'bad' foods."]},
    {"type": "example", "label": "Example", "items": [
      "Screen-free dinners \u2192",
      "healthier, happier kids."]},
  ]},
  {"title": "Caffeine & Alcohol", "color": "yellow", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "6 coffees \u2192 racing heart, panic.",
      "Alcohol ruins sleep + mood.",
      "Review both in mood problems."]},
    {"type": "revision", "label": "Instant Revision", "items": [
      "Nourish, don't punish."]},
  ]},
 ],
 "footer": ["Mediterranean diet", "B12 / iron / vit D", "Gut-brain axis", "Stable blood sugar"],
},
# ================= 7. Social Support and Health =================
{
 "title": "Social Support and Health",
 "subtitle": "Health Psychology \u00b7 People Heal",
 "sections": [
  {"title": "Support Saves Lives", "color": "green", "blocks": [
    {"type": "def", "label": "Key Fact", "items": [
      "Strong ties \u2192 longer life,",
      "faster healing."]},
    {"type": "points", "label": "Key Points", "items": [
      "Loneliness \u2248 smoking 15/day.",
      "Faster surgery recovery."]},
  ]},
  {"title": "Four Types", "color": "blue", "blocks": [
    {"type": "diagram", "diagram": "pyramid", "labels": ["Emotional", "Practical", "Advice"], "height": 140},
    {"type": "points", "label": "Key Points", "items": [
      "Emotional: listening, caring.",
      "Instrumental: rides, money.",
      "Informational: advice, feedback."]},
  ]},
  {"title": "Quality Beats Many", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Critical friends raise BP.",
      "Few warm > many draining.",
      "Conflict harms like smoking."]},
    {"type": "example", "label": "Example", "items": [
      "Drama friends worse than",
      "a few kind ones."]},
  ]},
  {"title": "Belonging", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Groups protect health alone.",
      "Clubs, teams, congregations.",
      "Casual belonging adds years."]},
    {"type": "example", "label": "Example", "items": [
      "Immigrant joins center \u2192",
      "stays healthier."]},
  ]},
  {"title": "Giving Heals Too", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Volunteers live longer.",
      "Helping builds meaning.",
      "Support flows both ways."]},
    {"type": "example", "label": "Example", "items": [
      "Widow volunteers \u2192",
      "blood pressure drops."]},
  ]},
  {"title": "Ask About It", "color": "teal", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "'Who helps you at home?'",
      "Link lonely patients to groups.",
      "Family in care plans."]},
    {"type": "revision", "label": "Instant Revision", "items": [
      "Support IS medical treatment."]},
  ]},
 ],
 "footer": ["4 support types", "Loneliness kills", "Quality > quantity", "Support groups"],
},
]
SPECS += [
# ================= 8. Placebo and Nocebo Effects =================
{
 "title": "Placebo and Nocebo Effects",
 "subtitle": "Health Psychology \u00b7 Expectation Heals",
 "sections": [
  {"title": "Placebo Effect", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": [
      "Inactive pill + belief \u2192",
      "real healing."]},
    {"type": "points", "label": "Key Points", "items": [
      "Brain releases endorphins.",
      "Rivals drugs for pain, depression.",
      "Expectation is medicine."]},
  ]},
  {"title": "Nocebo Effect", "color": "red", "blocks": [
    {"type": "def", "label": "Definition", "items": [
      "Expecting harm \u2192 real harm."]},
    {"type": "points", "label": "Key Points", "items": [
      "Scary warnings create symptoms.",
      "Anxious doctors worsen outcomes.",
      "Words have drug-like power."]},
    {"type": "example", "label": "Example", "items": [
      "'May cause nausea' \u2192 nausea",
      "on a sugar pill."]},
  ]},
  {"title": "Two Sides", "color": "blue", "blocks": [
    {"type": "diagram", "diagram": "scale", "labels": ["Placebo", "Nocebo"], "height": 150},
    {"type": "points", "label": "Key Points", "items": [
      "Same brain, opposite directions.",
      "Belief tips the balance."]},
  ]},
  {"title": "Doctor as Medicine", "color": "teal", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Warmth + confidence heals.",
      "Ritual: coat, thorough exam.",
      "Bedside manner changes outcomes."]},
    {"type": "example", "label": "Example", "items": [
      "Confident reassurance \u2192",
      "same pill works better."]},
  ]},
  {"title": "Honest Hope", "color": "yellow", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "'Many patients improve.'",
      "Frame side effects positively.",
      "Build on past wins."]},
    {"type": "example", "label": "Example", "items": [
      "Hopeful patient gets more",
      "relief from same treatment."]},
  ]},
  {"title": "In Drug Trials", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "New drugs must beat placebo.",
      "40% of antidepressant gain = placebo.",
      "Open-label placebos still work."]},
    {"type": "revision", "label": "Instant Revision", "items": [
      "Every word is an intervention."]},
  ]},
 ],
 "footer": ["Expectation heals", "Nocebo harms", "Bedside manner", "Ethical hope"],
},
# ================= 9. Type A Behavior and Heart Disease =================
{
 "title": "Type A Behavior and Heart Disease",
 "subtitle": "Health Psychology \u00b7 Hurry & Heart",
 "sections": [
  {"title": "Type A Pattern", "color": "red", "blocks": [
    {"type": "def", "label": "Definition", "items": [
      "Chronic hurry + competition",
      "+ hostility."]},
    {"type": "points", "label": "Key Points", "items": [
      "Found by Friedman & Rosenman.",
      "1950s heart patients shared it."]},
    {"type": "example", "label": "Example", "items": [
      "Shouts at elevators, brags",
      "about 80-hour weeks."]},
  ]},
  {"title": "The Toxic Part", "color": "orange", "blocks": [
    {"type": "diagram", "diagram": "bars", "labels": ["Hostility", "Urgency", "Ambition"], "height": 140},
    {"type": "points", "label": "Key Points", "items": [
      "Hostility harms \u2014 not hard work.",
      "Cynicism + anger predict disease.",
      "Warm achievers stay safe."]},
  ]},
  {"title": "How It Damages", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Anger spikes BP + inflammation.",
      "Damages artery walls yearly.",
      "Fewer friends, worse habits."]},
    {"type": "example", "label": "Example", "items": [
      "BP surges in every",
      "traffic jam."]},
  ]},
  {"title": "Change It", "color": "green", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Anger management works.",
      "Slow down, delegate tasks.",
      "Restructure hostile thoughts."]},
    {"type": "example", "label": "Example", "items": [
      "Laugh at delays \u2192",
      "calmer heart."]},
  ]},
  {"title": "Keep Ambition", "color": "blue", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Goal: drop hostility, keep drive.",
      "Type B was just comparison.",
      "Target anger + cynicism."]},
    {"type": "revision", "label": "Instant Revision", "items": [
      "Ambition is fine \u2014 hostility kills."]},
  ]},
  {"title": "Workplace Hearts", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Unfair bosses strain hearts.",
      "Job strain predicts disease.",
      "Cardiac rehab uses psychology."]},
    {"type": "example", "label": "Example", "items": [
      "High demand + low control",
      "= heart risk."]},
  ]},
 ],
 "footer": ["Hostility = toxic", "Friedman & Rosenman", "Anger management", "Job strain"],
},
# ================= 10. Mindfulness for Health =================
{
 "title": "Mindfulness for Health",
 "subtitle": "Health Psychology \u00b7 Present Moment",
 "sections": [
  {"title": "What It Is", "color": "teal", "blocks": [
    {"type": "def", "label": "Definition", "items": [
      "Attention to now,",
      "without judgment."]},
    {"type": "points", "label": "Key Points", "items": [
      "Doesn't erase pain \u2014 changes it.",
      "Less suffering on top of illness."]},
    {"type": "example", "label": "Example", "items": [
      "10-min body scan \u2192",
      "pain bothers less."]},
  ]},
  {"title": "MBSR Program", "color": "green", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "8-week evidence-based course.",
      "Lowers BP, stress, pain.",
      "Practice matters, not belief."]},
    {"type": "example", "label": "Example", "items": [
      "Hypertension drops",
      "after 8 weeks."]},
  ]},
  {"title": "The Mechanism", "color": "blue", "blocks": [
    {"type": "diagram", "diagram": "cycle", "labels": ["Focus", "Notice", "Accept", "Return"], "height": 150},
    {"type": "points", "label": "Key Points", "items": [
      "Breaks rumination loops.",
      "'I'm having the thought that\u2026'",
      "Anchors in breath + body."]},
  ]},
  {"title": "Common Myths", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "NOT emptying the mind.",
      "Wandering is normal.",
      "Gently return \u2014 that's the rep."]},
    {"type": "example", "label": "Example", "items": [
      "Frustrated quitter",
      "misunderstood it."]},
  ]},
  {"title": "Small Doses Work", "color": "yellow", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "3\u201310 minutes daily is enough.",
      "Consistency beats duration.",
      "Apps make it easy."]},
    {"type": "example", "label": "Example", "items": [
      "3-min breaks between",
      "meetings."]},
  ]},
  {"title": "With Medicine", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Complements, never replaces.",
      "Improves treatment adherence.",
      "Eases chemo + diabetes stress."]},
    {"type": "example", "label": "Example", "items": [
      "Breathing during chemo",
      "\u2192 calmer patient."]},
  ]},
 ],
 "footer": ["MBSR 8 weeks", "Present, not perfect", "3 min daily counts", "Breaks rumination"],
},
# ================= 11. Biofeedback =================
{
 "title": "Biofeedback",
 "subtitle": "Health Psychology \u00b7 Mind Controls Body",
 "sections": [
  {"title": "What It Is", "color": "teal", "blocks": [
    {"type": "def", "label": "Definition", "items": [
      "Sensors mirror hidden body",
      "signals in real time."]},
    {"type": "points", "label": "Key Points", "items": [
      "Muscle tension, heart rate, temp.",
      "See it \u2192 learn to change it.",
      "A mirror for your nerves."]},
  ]},
  {"title": "Types", "color": "blue", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "EMG: muscle tension.",
      "Thermal: hand temperature.",
      "HRV: anxiety; neurofeedback: ADHD."]},
    {"type": "example", "label": "Example", "items": [
      "ADHD child trains brain",
      "waves \u2192 better focus."]},
  ]},
  {"title": "How It Works", "color": "green", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Sensor", "Signal", "Practice", "Control"], "height": 130},
    {"type": "points", "label": "Key Points", "items": [
      "Hidden becomes visible.",
      "Breathing changes the signal.",
      "Display rewards success fast."]},
  ]},
  {"title": "Strong Evidence", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Migraines + tension headaches.",
      "Raynaud's, incontinence.",
      "Anxiety, pain, BP (add-on)."]},
    {"type": "example", "label": "Example", "items": [
      "Veteran calms hyperarousal",
      "on command."]},
  ]},
  {"title": "Learn, Then Leave", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Brief training, lasting skill.",
      "Practice without machines after.",
      "Apps extend it cheaply."]},
    {"type": "example", "label": "Example", "items": [
      "6 sessions \u2192 home",
      "practice with app."]},
  ]},
  {"title": "Limits", "color": "red", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Needs daily practice.",
      "Training, not magic.",
      "Beware cure-everything claims."]},
    {"type": "example", "label": "Example", "items": [
      "Skeptic learns it",
      "takes real work."]},
  ]},
 ],
 "footer": ["EMG / thermal / HRV", "Migraines, Raynaud's", "Training not magic", "Peak performance"],
},
# ================= 12. Health Anxiety =================
{
 "title": "Health Anxiety",
 "subtitle": "Health Psychology \u00b7 Fear of Illness",
 "sections": [
  {"title": "What It Is", "color": "red", "blocks": [
    {"type": "def", "label": "Definition", "items": [
      "Fear of disease despite",
      "medical reassurance."]},
    {"type": "points", "label": "Key Points", "items": [
      "Normal sensations misread.",
      "Heartbeat \u2192 'heart attack.'"]},
    {"type": "example", "label": "Example", "items": [
      "Checks pulse 50\u00d7 daily",
      "at age 30."]},
  ]},
  {"title": "The Worry Cycle", "color": "orange", "blocks": [
    {"type": "diagram", "diagram": "cycle", "labels": ["Notice", "Worry", "Google", "Panic"], "height": 150},
    {"type": "points", "label": "Key Points", "items": [
      "Cyberchondria fuels fear.",
      "Rare diseases top results.",
      "Relief fades in hours."]},
  ]},
  {"title": "Reassurance Trap", "color": "yellow", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Tests calm for hours only.",
      "Doctor-shopping feeds fear.",
      "Next sensation restarts panic."]},
    {"type": "example", "label": "Example", "items": [
      "Weekly ER visits, normal",
      "tests, still terrified."]},
  ]},
  {"title": "Avoidance", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Some skip all checkups.",
      "Fear of bad news.",
      "Same fear, opposite face."]},
    {"type": "example", "label": "Example", "items": [
      "Avoids every doctor",
      "for years."]},
  ]},
  {"title": "CBT Treatment", "color": "green", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Anxiety \u2192 real body symptoms.",
      "Drop checking + googling.",
      "Tolerate health uncertainty."]},
    {"type": "example", "label": "Example", "items": [
      "Coffee jitters = adrenaline,",
      "not a heart attack."]},
  ]},
  {"title": "Helpful Doctors", "color": "teal", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Take fears seriously.",
      "Explain the worry loop.",
      "Refer to CBT, not more tests."]},
    {"type": "revision", "label": "Instant Revision", "items": [
      "'Your suffering is real \u2014",
      "let's treat the anxiety.'"]},
  ]},
 ],
 "footer": ["Illness anxiety disorder", "Cyberchondria", "CBT works", "Drop safety behaviors"],
},
# ================= 13. Somatization =================
{
 "title": "Somatization",
 "subtitle": "Health Psychology \u00b7 Body Speaks",
 "sections": [
  {"title": "What It Is", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": [
      "Real symptoms, no clear",
      "medical cause."]},
    {"type": "points", "label": "Key Points", "items": [
      "Pain, fatigue, dizziness.",
      "NOT faking \u2014 suffering is real.",
      "Nerves amplify signals."]},
  ]},
  {"title": "Stress to Body", "color": "orange", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Stress", "Tension", "Symptom", "Doctor"], "height": 130},
    {"type": "points", "label": "Key Points", "items": [
      "Feelings speak via the body.",
      "Back pain every Monday.",
      "Common across cultures."]},
  ]},
  {"title": "Test Merry-Go-Round", "color": "red", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "15 specialists, 8 scans.",
      "Relief fades, search resumes.",
      "Costs money and hope."]},
    {"type": "example", "label": "Example", "items": [
      "Folder of normal results \u2014",
      "still searching."]},
  ]},
  {"title": "Children Too", "color": "yellow", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Stomach aches = school fear.",
      "Vanish on weekends.",
      "Treat stress, not stomach."]},
    {"type": "example", "label": "Example", "items": [
      "Aches gone every",
      "Saturday."]},
  ]},
  {"title": "What Works", "color": "green", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "One trusted doctor.",
      "Scheduled visits, not symptoms.",
      "Validate + build function."]},
    {"type": "example", "label": "Example", "items": [
      "'Meet monthly' \u2192",
      "ER visits drop."]},
  ]},
  {"title": "Rehab Over Tests", "color": "teal", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Graded activity + sleep + CBT.",
      "Goal: live fully anyway.",
      "Treat anxiety + depression."]},
    {"type": "revision", "label": "Instant Revision", "items": [
      "Respect the body's cry for help."]},
  ]},
 ],
 "footer": ["Real, not faked", "One trusted doctor", "Function over cure", "Culture matters"],
},
# ================= 14. Treatment Adherence =================
{
 "title": "Treatment Adherence",
 "subtitle": "Health Psychology \u00b7 Taking Treatment",
 "sections": [
  {"title": "The Problem", "color": "red", "blocks": [
    {"type": "def", "label": "Key Fact", "items": [
      "Half of patients don't follow",
      "treatment as prescribed."]},
    {"type": "example", "label": "Example", "items": [
      "Pills only when remembered",
      "\u2192 BP stays high."]},
  ]},
  {"title": "Why It Fails", "color": "orange", "blocks": [
    {"type": "diagram", "diagram": "bars", "labels": ["Forget", "Beliefs", "Cost", "Side FX"], "height": 140},
    {"type": "points", "label": "Key Points", "items": [
      "Complex regimens confuse.",
      "8 pills + tiny labels = quit.",
      "Simplify: one pill daily."]},
  ]},
  {"title": "Beliefs Drive It", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "'Pills are poison' \u2192 stops.",
      "Doubt + fear beat facts.",
      "Ask concerns, don't scold."]},
    {"type": "example", "label": "Example", "items": [
      "Stops antidepressants",
      "within a week."]},
  ]},
  {"title": "Social Roots", "color": "blue", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Stigma and no support.",
      "Depression triples skipping.",
      "Teen hides insulin at school."]},
    {"type": "example", "label": "Example", "items": [
      "Skips insulin to",
      "look normal."]},
  ]},
  {"title": "What Helps", "color": "green", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Blister packs + alarms.",
      "Family involved in plan.",
      "Fix cost barriers."]},
    {"type": "example", "label": "Example", "items": [
      "Daily text reminders",
      "\u2192 +20% adherence."]},
  ]},
  {"title": "Measure Kindly", "color": "teal", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "'How many did you miss?'",
      "Pill counts, refill checks.",
      "Solve together, don't accuse."]},
    {"type": "revision", "label": "Instant Revision", "items": [
      "Adherence = systems problem."]},
  ]},
 ],
 "footer": ["50% don't adhere", "Simplify regimens", "Beliefs matter", "Non-judgmental checks"],
},
]
SPECS += [
# ================= 15. Doctor-Patient Communication =================
{
 "title": "Doctor-Patient Communication",
 "subtitle": "Health Psychology \u00b7 Talking Heals",
 "sections": [
  {"title": "Listen First", "color": "teal", "blocks": [
    {"type": "def", "label": "Key Fact", "items": [
      "Let patients speak",
      "uninterrupted."]},
    {"type": "points", "label": "Key Points", "items": [
      "Most doctors cut in at 11 sec.",
      "Open questions \u2192 better diagnosis."]},
    {"type": "example", "label": "Example", "items": [
      "'What worries you most?'",
      "\u2192 fears cancer."]},
  ]},
  {"title": "Plain Language", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "'Heart attack' not 'MI.'",
      "Jargon causes dangerous errors.",
      "Explain timing clearly."]},
    {"type": "example", "label": "Example", "items": [
      "Nods politely, then",
      "takes pills wrong."]},
  ]},
  {"title": "Empathy Works", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Respect \u2192 honest symptoms.",
      "Warm 2 min improves outcomes.",
      "Partner, don't lecture."]},
    {"type": "example", "label": "Example", "items": [
      "'Let's fix it together'",
      "wins cooperation."]},
  ]},
  {"title": "Teach-Back", "color": "blue", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Explain", "Repeat", "Check", "Recall"], "height": 130},
    {"type": "points", "label": "Key Points", "items": [
      "Patient repeats plan back.",
      "Drawings + written summaries.",
      "Sketch beats 10-min talk."]},
  ]},
  {"title": "Culture Counts", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Eye contact norms differ.",
      "Ask preferences, don't assume.",
      "Authority views vary."]},
    {"type": "example", "label": "Example", "items": [
      "Silent on side effects",
      "from respect."]},
  ]},
  {"title": "Bad News Skill", "color": "red", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "SPIKES protocol for bad news.",
      "Private, gentle, allow silence.",
      "Delivery shapes months ahead."]},
    {"type": "example", "label": "Example", "items": [
      "Hallway diagnosis",
      "traumatizes."]},
  ]},
 ],
 "footer": ["Listen 11+ seconds", "Teach-back method", "Plain language", "SPIKES protocol"],
},
# ================= 16. Coping with Chronic Illness =================
{
 "title": "Coping with Chronic Illness",
 "subtitle": "Health Psychology \u00b7 Living With Illness",
 "sections": [
  {"title": "The Adjustment", "color": "blue", "blocks": [
    {"type": "def", "label": "Key Fact", "items": [
      "Shock \u2192 grief \u2192 acceptance,",
      "on repeat."]},
    {"type": "points", "label": "Key Points", "items": [
      "Flares restart the cycle.",
      "Ongoing, not one-time."]},
    {"type": "example", "label": "Example", "items": [
      "Grieves old life, builds",
      "new routine."]},
  ]},
  {"title": "Appraisal Matters", "color": "green", "blocks": [
    {"type": "diagram", "diagram": "pyramid", "labels": ["Challenge", "Threat", "Loss"], "height": 140},
    {"type": "points", "label": "Key Points", "items": [
      "'Challenge' \u2192 active coping.",
      "'Threat' \u2192 avoidance.",
      "Reframe the meaning."]},
  ]},
  {"title": "Good Strategies", "color": "teal", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Seek info + support.",
      "Keep daily routines.",
      "Relaxation techniques."]},
    {"type": "example", "label": "Example", "items": [
      "Support group + part-time",
      "work \u2192 better life."]},
  ]},
  {"title": "Family Coping", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Supportive beats overprotective.",
      "Doing everything disables.",
      "Couples coping together win."]},
    {"type": "example", "label": "Example", "items": [
      "Wife walks with him",
      "\u2192 faster recovery."]},
  ]},
  {"title": "Pacing", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Avoid boom-bust cycle.",
      "Rest BEFORE exhaustion.",
      "Small wins, realistic goals."]},
    {"type": "example", "label": "Example", "items": [
      "MS patient plans",
      "around energy."]},
  ]},
  {"title": "Finding Meaning", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Writing heals: 15 min \u00d7 few.",
      "Helping others grows purpose.",
      "Post-traumatic growth is real."]},
    {"type": "example", "label": "Example", "items": [
      "Journaling \u2192 fewer",
      "doctor visits."]},
  ]},
 ],
 "footer": ["Challenge appraisal", "Pacing", "Family coping", "Expressive writing"],
},
# ================= 17. Smoking and Cessation =================
{
 "title": "Smoking and Cessation",
 "subtitle": "Health Psychology \u00b7 Quitting Wins",
 "sections": [
  {"title": "Why Start", "color": "orange", "blocks": [
    {"type": "def", "label": "Key Fact", "items": [
      "Peers + stress + ads;",
      "hooked fast."]},
    {"type": "points", "label": "Key Points", "items": [
      "Nicotine hits brain in 10 sec.",
      "Most start before 18."]},
    {"type": "example", "label": "Example", "items": [
      "Tries at party \u2192",
      "hourly need."]},
  ]},
  {"title": "Addiction", "color": "red", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "As addictive as heroin.",
      "Withdrawal: cravings, irritability.",
      "Relapse peaks in 2 weeks."]},
    {"type": "example", "label": "Example", "items": [
      "2\u20133 weeks of",
      "misery."]},
  ]},
  {"title": "The Quit Ladder", "color": "green", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Plan", "Quit Date", "Support", "Maintain"], "height": 130},
    {"type": "points", "label": "Key Points", "items": [
      "Willpower alone: 5% succeed.",
      "Help doubles/triples odds."]},
  ]},
  {"title": "What Works", "color": "teal", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Patches + gum + varenicline.",
      "Counseling + quitlines.",
      "Combine for best odds."]},
    {"type": "example", "label": "Example", "items": [
      "Patches + counseling",
      "= 3\u00d7 success."]},
  ]},
  {"title": "Beat Cravings", "color": "blue", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Cravings peak, then pass.",
      "Remove triggers early.",
      "Gum, walks, support."]},
    {"type": "example", "label": "Example", "items": [
      "Ashtrays out,",
      "gum in."]},
  ]},
  {"title": "One Slip \u2260 Fail", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Lapse = warning, not verdict.",
      "Restart immediately.",
      "Shame fuels relapse."]},
    {"type": "example", "label": "Example", "items": [
      "Wedding cigarette \u2192 'failed'",
      "\u2192 full relapse."]},
  ]},
 ],
 "footer": ["Nicotine in 10 sec", "Quitlines work", "Cravings pass", "Lapse \u2260 relapse"],
},
# ================= 18. Obesity Psychology =================
{
 "title": "Obesity Psychology",
 "subtitle": "Health Psychology \u00b7 Weight & Mind",
 "sections": [
  {"title": "Mind Drives Weight", "color": "orange", "blocks": [
    {"type": "def", "label": "Key Fact", "items": [
      "Emotions override",
      "fullness signals."]},
    {"type": "points", "label": "Key Points", "items": [
      "Stress and boredom eating.",
      "Cheap tasty food everywhere."]},
    {"type": "example", "label": "Example", "items": [
      "Midnight pizza for anxiety,",
      "not hunger."]},
  ]},
  {"title": "Diets Fail", "color": "red", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "80\u201395% regain in years.",
      "Restriction \u2192 binge + shame.",
      "Habits beat diets."]},
    {"type": "example", "label": "Example", "items": [
      "Loses 10 kg,",
      "regains 12."]},
  ]},
  {"title": "Mindless Eating", "color": "yellow", "blocks": [
    {"type": "diagram", "diagram": "bars", "labels": ["TV", "Big Packs", "Screens", "Stress"], "height": 140},
    {"type": "points", "label": "Key Points", "items": [
      "Distraction adds 100s of cal.",
      "Small plates, no screens.",
      "Pre-portion servings."]},
  ]},
  {"title": "What Works", "color": "green", "blocks": [
    {"type": "diagram", "diagram": "pyramid", "labels": ["Meals", "Activity", "Sleep"], "height": 130},
    {"type": "points", "label": "Key Points", "items": [
      "Goal: 0.5 kg per week.",
      "Walk 30 min daily.",
      "Weigh + food records."]},
  ]},
  {"title": "Stigma Harms", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Shame \u2192 stress \u2192 more eating.",
      "Avoids doctors and gyms.",
      "Compassion works, shame doesn't."]},
    {"type": "example", "label": "Example", "items": [
      "Bullied teen gains",
      "even more."]},
  ]},
  {"title": "CBT Skills", "color": "teal", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Spot triggers: 9 PM loneliness.",
      "Plan non-food rewards.",
      "Fix 'I blew it' thinking."]},
    {"type": "example", "label": "Example", "items": [
      "Call a friend,",
      "not ice cream."]},
  ]},
 ],
 "footer": ["Habits > diets", "0.5 kg/week", "Stigma backfires", "CBT skills"],
},
# ================= 19. Caregiver Stress =================
{
 "title": "Caregiver Stress",
 "subtitle": "Health Psychology \u00b7 Caring for Carers",
 "sections": [
  {"title": "Hidden Patients", "color": "red", "blocks": [
    {"type": "def", "label": "Key Fact", "items": [
      "Caregivers get sick too."]},
    {"type": "points", "label": "Key Points", "items": [
      "Depression, weak immunity.",
      "Chronic, unending stress.",
      "Earlier death risk."]},
    {"type": "example", "label": "Example", "items": [
      "4 years of Alzheimer's care",
      "\u2192 her BP up."]},
  ]},
  {"title": "Mixed Feelings", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Love + resentment + grief.",
      "Guilt about guilt.",
      "All normal, not shameful."]},
    {"type": "example", "label": "Example", "items": [
      "Resents demands, then",
      "feels guilty."]},
  ]},
  {"title": "Self-Neglect", "color": "orange", "blocks": [
    {"type": "diagram", "diagram": "bars", "labels": ["Sleep", "Checkups", "Breaks", "Mood"], "height": 140},
    {"type": "points", "label": "Key Points", "items": [
      "Skips own doctors.",
      "No exercise, no sleep.",
      "Respite = essential."]},
  ]},
  {"title": "What Helps", "color": "green", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Respite services + day programs.",
      "Support groups that get it.",
      "Learn care skills."]},
    {"type": "example", "label": "Example", "items": [
      "Group tips \u2192 feels",
      "understood at last."]},
  ]},
  {"title": "Policy Matters", "color": "blue", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Paid leave + flex hours.",
      "Tax credits help.",
      "Support \u2192 better outcomes."]},
    {"type": "example", "label": "Example", "items": [
      "Flex hours keeps",
      "a loyal worker."]},
  ]},
  {"title": "Rewards Too", "color": "pink", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Closeness and purpose.",
      "Growth through giving.",
      "Burden AND meaning."]},
    {"type": "example", "label": "Example", "items": [
      "50-year marriage:",
      "meaning in care."]},
  ]},
 ],
 "footer": ["Screen caregivers", "Respite is essential", "Ask: 'how are YOU?'", "Support groups"],
},
# ================= 20. Health Promotion Campaigns =================
{
 "title": "Health Promotion Campaigns",
 "subtitle": "Health Psychology \u00b7 Campaigns That Work",
 "sections": [
  {"title": "Fear Isn't Enough", "color": "red", "blocks": [
    {"type": "def", "label": "Key Fact", "items": [
      "Scare + no steps =",
      "people look away."]},
    {"type": "points", "label": "Key Points", "items": [
      "Graphic lungs < peer rejection.",
      "Pair worry with action steps."]},
    {"type": "example", "label": "Example", "items": [
      "Rejection ads beat",
      "gore ads."]},
  ]},
  {"title": "Messenger Matters", "color": "blue", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Trusted locals persuade.",
      "Imams, elders, peers.",
      "Match messenger to audience."]},
    {"type": "example", "label": "Example", "items": [
      "Local elders \u2192 vaccine",
      "uptake doubles."]},
  ]},
  {"title": "Change Places", "color": "green", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Message", "Streets", "Easy Pick", "Health"], "height": 130},
    {"type": "points", "label": "Key Points", "items": [
      "Bike lanes beat posters.",
      "Soda tax, ad bans.",
      "Make healthy easy + cheap."]},
  ]},
  {"title": "Norm Power", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "'Most people like you\u2026'",
      "Correct false beliefs.",
      "Show real compliance."]},
    {"type": "example", "label": "Example", "items": [
      "Doctors see own rates",
      "\u2192 wash hands."]},
  ]},
  {"title": "Co-Create", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Build WITH the audience.",
      "Their humor, their channels.",
      "Pre-test everything."]},
    {"type": "example", "label": "Example", "items": [
      "Teen-made vaping ads",
      "go viral."]},
  ]},
  {"title": "Measure Reality", "color": "teal", "blocks": [
    {"type": "points", "label": "Key Points", "items": [
      "Quitline calls, not views.",
      "Behavior goals upfront.",
      "Marathon, not sprint."]},
    {"type": "example", "label": "Example", "items": [
      "Decade of tobacco control",
      "\u2192 smoking halved."]},
  ]},
 ],
 "footer": ["Fear + action steps", "Trusted messengers", "Change environments", "Measure behavior"],
},
]

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    env = load_env()
    base_url, key = env["SUPABASE_URL"], env["SUPABASE_SECRET_KEY"]
    manifest = json.load(open("/home/hatch/workspace/zehen/batch4/inf-health.json"))
    assert len(SPECS) == 20, f"expected 20 specs, got {len(SPECS)}"
    assert len(manifest) == 20, f"expected 20 manifest entries, got {len(manifest)}"
    ok, fails = 0, []
    for i, spec in enumerate(SPECS, 1):
        fname = f"health-{i}.png"
        out = os.path.join(OUT_DIR, fname)
        render_cheatsheet(spec, out)
        size = os.path.getsize(out)
        try:
            st = upload_file(base_url, key, fname, out)
            pub = manifest[i-1]["file"]
            vst = check_url(pub)
            print(f"[{i}/20] {fname} rendered ({size}B) upload={st} verify={vst}")
            if st in (200, 201) and vst == 200:
                ok += 1
            else:
                fails.append(fname)
        except Exception as e:
            print(f"[{i}/20] {fname} FAILED: {e}")
            fails.append(fname)
    print(f"\nDONE: {ok}/20 overwritten and verified.")
    if fails:
        print("FAILURES:", fails)

if __name__ == "__main__":
    main()
