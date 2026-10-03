#!/usr/bin/env python3
"""Cheat-sheet specs for 20 Organizational Psychology infographics."""
import sys
sys.path.insert(0, '/home/hatch/workspace/zehen/batch4')
from cheatsheet import render_cheatsheet

AR = "\u2192"  # arrow, never use ->

SPECS = [
# ============ 1. What is I-O Psychology? ============
{"title": "What is I-O Psychology?", "subtitle": "Chapter 1 - The Science of People at Work",
 "sections": [
  {"title": "Definition", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Applies psychology to workplaces: hiring, training, motivation, leadership."]},
   {"type": "points", "label": "Main Goal", "items": [
    "Help employees do well.",
    "Help organizations succeed."]},
   {"type": "revision", "label": "Instant Revision", "items": [
    "I-O = psychology of people at work"]}]},
  {"title": "Two Sides", "color": "green", "blocks": [
   {"type": "points", "label": "Industrial Side", "items": [
    "Jobs and people: hiring, training, performance."]},
   {"type": "points", "label": "Organizational Side", "items": [
    "People and workplace: motivation, teams, culture."]},
   {"type": "diagram", "diagram": "venn", "labels": ["Industrial", "Organizational"], "height": 150}]},
  {"title": "History", "color": "yellow", "blocks": [
   {"type": "points", "label": "Key Moments", "items": [
    "1900s: Munsterberg matched workers to jobs.",
    "1920s-30s: Hawthorne studies - noticed workers perform better.",
    "World Wars: boom in selection and training."]}]},
  {"title": "Scientist-Practitioner", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Does research AND solves real workplace problems."]},
   {"type": "points", "label": "Key Points", "items": [
    "Everything tested with data, not guesswork.",
    "Example: testing if a new interview predicts performance."]}]},
  {"title": "Why It Matters", "color": "orange", "blocks": [
   {"type": "points", "label": "Benefits", "items": [
    "Less employee turnover.",
    "Higher productivity and satisfaction.",
    "Fairer, healthier workplaces."]}]},
  {"title": "Careers", "color": "teal", "blocks": [
   {"type": "points", "label": "Jobs", "items": [
    "HR consultant and talent manager.",
    "Training designer.",
    "Organizational development specialist."]}]},
 ],
 "footer": ["I-O Psychology definition", "Hawthorne studies", "Scientist-practitioner model"]},

# ============ 2. Recruitment Strategies ============
{"title": "Recruitment Strategies", "subtitle": "Chapter 2 - Attracting the Right Talent",
 "sections": [
  {"title": "Definition", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Attracting qualified candidates to apply for jobs."]},
   {"type": "points", "label": "Two Sources", "items": [
    "Internal: current employees.",
    "External: outside candidates."]}]},
  {"title": "Internal Recruitment", "color": "green", "blocks": [
   {"type": "points", "label": "Methods", "items": [
    "Promotions and transfers.",
    "Internal job postings."]},
   {"type": "points", "label": "Pros & Cons", "items": [
    "Pro: boosts morale, cheaper, faster.",
    "Con: limited pool, no fresh ideas."]}]},
  {"title": "External Recruitment", "color": "purple", "blocks": [
   {"type": "points", "label": "Methods", "items": [
    "Job boards and company websites.",
    "Campus hiring and referrals.",
    "Recruitment agencies."]},
   {"type": "points", "label": "Pros & Cons", "items": [
    "Pro: wider pool, fresh ideas.",
    "Con: costlier, slower, riskier."]}]},
  {"title": "Employer Branding", "color": "pink", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Company image as a great place to work."]},
   {"type": "points", "label": "Key Points", "items": [
    "Online reviews shape applications.",
    "Social media presence attracts talent."]}]},
  {"title": "Realistic Job Preview", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Honest preview of job pros AND cons."]},
   {"type": "example", "label": "Example", "items": [
    "Factory tour before accepting the job."]},
   {"type": "points", "label": "Benefit", "items": [
    "Lowers early turnover, builds trust."]}]},
  {"title": "Metrics", "color": "teal", "blocks": [
   {"type": "points", "label": "Track These", "items": [
    "Time-to-fill open roles.",
    "Cost-per-hire.",
    "Quality of hire."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Source", "Screen", "Hire"], "height": 130}]},
 ],
 "footer": ["Internal vs external", "Realistic job preview", "Time-to-fill"]},

# ============ 3. Selection Methods ============
{"title": "Selection Methods", "subtitle": "Chapter 3 - Choosing the Best Candidate",
 "sections": [
  {"title": "Definition", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Choosing the best candidate from applicants."]},
   {"type": "points", "label": "Must Be", "items": [
    "Reliable AND valid, or it is useless."]}]},
  {"title": "Reliability", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Consistent results over time and raters."]},
   {"type": "points", "label": "Key Points", "items": [
    "Same person, same test " + AR + " similar score.",
    "Test-retest and inter-rater checks."]}]},
  {"title": "Validity", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Measures what it claims; predicts job performance."]},
   {"type": "revision", "label": "Instant Revision", "items": [
    "Validity = the most important quality"]}]},
  {"title": "Common Methods", "color": "orange", "blocks": [
   {"type": "points", "label": "Methods", "items": [
    "Interviews and reference checks.",
    "Cognitive and personality tests."]},
   {"type": "diagram", "diagram": "bars", "labels": ["Interview", "Test", "Work sample"], "height": 150}]},
  {"title": "Utility", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Practical value a selection method adds."]},
   {"type": "points", "label": "Key Points", "items": [
    "Better selection " + AR + " better performance.",
    "Also " + AR + " less turnover and training cost."]}]},
  {"title": "Legal Issues", "color": "red", "blocks": [
   {"type": "points", "label": "Rules", "items": [
    "Must be job-related and fair.",
    "Avoid discrimination by race, gender, age.",
    "Document every hiring decision."]}]},
 ],
 "footer": ["Reliability vs validity", "Work sample tests", "Adverse impact"]},

# ============ 4. Employment Interviews ============
{"title": "Employment Interviews", "subtitle": "Chapter 4 - Asking the Right Questions",
 "sections": [
  {"title": "Structured Interviews", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Same questions for all, scored with a rubric."]},
   {"type": "points", "label": "Key Points", "items": [
    "Far more valid than casual chats.",
    "Reduces bias and guesswork."]}]},
  {"title": "Unstructured Interviews", "color": "yellow", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Free-flowing casual conversation."]},
   {"type": "points", "label": "Problems", "items": [
    "Low validity, high bias risk.",
    "Different questions per candidate."]}]},
  {"title": "Behavioral Questions", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "'Tell me about a time when...'"]},
   {"type": "points", "label": "Logic", "items": [
    "Past behavior predicts future behavior."]}]},
  {"title": "Situational Questions", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "'What would you do if...'"]},
   {"type": "points", "label": "Logic", "items": [
    "Tests judgment in hypothetical scenarios."]}]},
  {"title": "STAR Method", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Framework for answering interview questions."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Situation", "Task", "Action", "Result"], "height": 130}]},
  {"title": "Interviewer Biases", "color": "red", "blocks": [
   {"type": "points", "label": "Watch Out", "items": [
    "Halo effect: one good trait colors all.",
    "First impressions decide too fast.",
    "Similarity bias: favoring 'people like me'."]},
   {"type": "revision", "label": "Instant Revision", "items": [
    "Structured > unstructured, always"]}]},
 ],
 "footer": ["STAR method", "Structured interviews", "Halo effect"]},

# ============ 5. Cognitive Ability Testing at Work ============
{"title": "Cognitive Ability Testing", "subtitle": "Chapter 5 - Measuring Mental Horsepower",
 "sections": [
  {"title": "Definition", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Tests of reasoning, memory, problem-solving."]},
   {"type": "diagram", "diagram": "brain", "labels": [], "height": 150}]},
  {"title": "What It Measures", "color": "green", "blocks": [
   {"type": "points", "label": "Abilities", "items": [
    "Verbal and numerical reasoning.",
    "Abstract logic and learning speed."]}]},
  {"title": "Validity", "color": "purple", "blocks": [
   {"type": "points", "label": "Key Points", "items": [
    "Among the best predictors of job performance.",
    "Works across almost all job types."]},
   {"type": "revision", "label": "Instant Revision", "items": [
    "g factor = general mental ability"]}]},
  {"title": "Common Tests", "color": "orange", "blocks": [
   {"type": "points", "label": "Examples", "items": [
    "Wonderlic Personnel Test.",
    "Raven's Progressive Matrices.",
    "Job-specific aptitude tests."]}]},
  {"title": "Fairness Concerns", "color": "yellow", "blocks": [
   {"type": "points", "label": "Issues", "items": [
    "Group score gaps exist.",
    "Combine with other methods.",
    "Validate for each job locally."]}]},
  {"title": "Best Practice", "color": "teal", "blocks": [
   {"type": "points", "label": "Rules", "items": [
    "Keep tests job-related.",
    "Standardize administration.",
    "Use professional scoring."]}]},
 ],
 "footer": ["g factor", "Predictive validity", "Raven's matrices"]},

# ============ 6. Training and Development ============
{"title": "Training and Development", "subtitle": "Chapter 6 - Building Skills That Stick",
 "sections": [
  {"title": "Needs Assessment", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Finding skill gaps BEFORE training starts."]},
   {"type": "points", "label": "Three Levels", "items": [
    "Organization, task, and person analysis."]}]},
  {"title": "Methods", "color": "green", "blocks": [
   {"type": "points", "label": "Options", "items": [
    "On-the-job training and coaching.",
    "Classroom, e-learning, simulations.",
    "Mentoring and job rotation."]}]},
  {"title": "Transfer of Training", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Applying learned skills on the job."]},
   {"type": "points", "label": "Key Points", "items": [
    "Manager support matters most.",
    "Practice + feedback " + AR + " real transfer."]}]},
  {"title": "Kirkpatrick Model", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Four levels of training evaluation."]},
   {"type": "diagram", "diagram": "pyramid", "labels": ["Reaction", "Learning", "Behavior", "Results"], "height": 150}]},
  {"title": "Training vs Development", "color": "teal", "blocks": [
   {"type": "points", "label": "Training", "items": [
    "Skills for the CURRENT job."]},
   {"type": "points", "label": "Development", "items": [
    "Growth for FUTURE roles."]}]},
  {"title": "Coaching", "color": "pink", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "One-on-one guidance for performance."]},
   {"type": "points", "label": "Key Points", "items": [
    "Feedback + clear goals.",
    "Builds future leaders."]}]},
 ],
 "footer": ["Kirkpatrick 4 levels", "Transfer of training", "Needs assessment"]},

# ============ 7. Performance Appraisal ============
{"title": "Performance Appraisal", "subtitle": "Chapter 7 - Evaluating Work Fairly",
 "sections": [
  {"title": "Definition", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Formal evaluation of job performance, usually yearly."]},
   {"type": "points", "label": "Uses", "items": [
    "Pay, promotion, training needs."]}]},
  {"title": "Methods", "color": "green", "blocks": [
   {"type": "points", "label": "Common Methods", "items": [
    "Graphic rating scales.",
    "BARS (behaviorally anchored).",
    "Ranking and MBO (goal-based)."]}]},
  {"title": "Rating Errors", "color": "red", "blocks": [
   {"type": "points", "label": "Classic Errors", "items": [
    "Halo: one trait colors everything.",
    "Leniency: everyone rated too high.",
    "Central tendency: all rated average.",
    "Recency: only recent work counts."]}]},
  {"title": "Giving Feedback", "color": "purple", "blocks": [
   {"type": "points", "label": "Rules", "items": [
    "Be specific and timely.",
    "Focus on behavior, not person."]},
   {"type": "example", "label": "Example", "items": [
    "'3 errors in the report' beats 'bad work.'"]}]},
  {"title": "Appraisal Cycle", "color": "orange", "blocks": [
   {"type": "diagram", "diagram": "cycle", "labels": ["Set goals", "Monitor", "Review", "Reward"], "height": 160}]},
  {"title": "Making It Fair", "color": "teal", "blocks": [
   {"type": "points", "label": "Best Practice", "items": [
    "Clear criteria shared in advance.",
    "Multiple data sources.",
    "Two-way conversation, not lecture."]}]},
 ],
 "footer": ["Halo error", "BARS", "360-degree feedback"]},

# ============ 8. 360-Degree Feedback ============
{"title": "360-Degree Feedback", "subtitle": "Chapter 8 - Feedback From Every Angle",
 "sections": [
  {"title": "Definition", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Feedback from all around: boss, peers, reports, self."]},
   {"type": "points", "label": "Purpose", "items": [
    "Development, not punishment."]}]},
  {"title": "Who Rates?", "color": "green", "blocks": [
   {"type": "points", "label": "Raters", "items": [
    "Supervisor and peers.",
    "Subordinates and customers.",
    "Self-rating for comparison."]},
   {"type": "diagram", "diagram": "cycle", "labels": ["Self", "Peers", "Boss", "Staff"], "height": 140}]},
  {"title": "Benefits", "color": "purple", "blocks": [
   {"type": "points", "label": "Advantages", "items": [
    "Fuller, fairer picture of performance.",
    "Reveals blind spots.",
    "Encourages self-awareness."]}]},
  {"title": "Risks", "color": "red", "blocks": [
   {"type": "points", "label": "Dangers", "items": [
    "Inflated ratings to please.",
    "Fear of revenge without anonymity.",
    "Fails if poorly implemented."]}]},
  {"title": "Best Practice", "color": "orange", "blocks": [
   {"type": "points", "label": "Rules", "items": [
    "Keep raters anonymous.",
    "Use for development, not pay.",
    "Train raters before starting."]}]},
  {"title": "360 vs Appraisal", "color": "teal", "blocks": [
   {"type": "points", "label": "360-Degree", "items": [
    "Growth and self-development."]},
   {"type": "points", "label": "Appraisal", "items": [
    "Evaluation linked to rewards."]}]},
 ],
 "footer": ["Rater sources", "Anonymity", "Development vs evaluation"]},

# ============ 9. Maslow at Work ============
{"title": "Maslow at Work", "subtitle": "Chapter 9 - The Hierarchy of Needs",
 "sections": [
  {"title": "The Hierarchy", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Five need levels; lower needs come first."]},
   {"type": "diagram", "diagram": "pyramid", "labels": ["Self-actual.", "Esteem", "Belonging", "Safety", "Physiological"], "height": 170}]},
  {"title": "Physiological", "color": "green", "blocks": [
   {"type": "points", "label": "At Work", "items": [
    "Fair pay for basic living.",
    "Breaks, meals, decent conditions."]}]},
  {"title": "Safety", "color": "teal", "blocks": [
   {"type": "points", "label": "At Work", "items": [
    "Job security and safe workplace.",
    "Clear policies, no fear."]}]},
  {"title": "Belonging", "color": "pink", "blocks": [
   {"type": "points", "label": "At Work", "items": [
    "Teamwork and inclusion.",
    "Friendly, supportive culture."]}]},
  {"title": "Esteem", "color": "purple", "blocks": [
   {"type": "points", "label": "At Work", "items": [
    "Recognition and respect.",
    "Promotions and titles."]}]},
  {"title": "Self-Actualization", "color": "orange", "blocks": [
   {"type": "points", "label": "At Work", "items": [
    "Growth, creativity, meaningful work.",
    "Becoming your best self."]},
   {"type": "revision", "label": "Instant Revision", "items": [
    "Meet lower needs first, then higher"]}]},
 ],
 "footer": ["5 need levels", "Deficiency vs growth", "Self-actualization"]},

# ============ 10. Herzberg's Two-Factor Theory ============
{"title": "Herzberg's Two-Factor Theory", "subtitle": "Chapter 10 - What Really Motivates",
 "sections": [
  {"title": "Core Idea", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Satisfaction and dissatisfaction are separate, not opposites."]},
   {"type": "revision", "label": "Instant Revision", "items": [
    "No dissatisfaction is NOT satisfaction"]}]},
  {"title": "Hygiene Factors", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Prevent dissatisfaction but do NOT motivate."]},
   {"type": "points", "label": "Examples", "items": [
    "Pay, company policies, supervision.",
    "Working conditions, job security."]}]},
  {"title": "Motivators", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Create real satisfaction and drive."]},
   {"type": "points", "label": "Examples", "items": [
    "Achievement and recognition.",
    "Growth, responsibility, the work itself."]}]},
  {"title": "Key Insight", "color": "orange", "blocks": [
   {"type": "points", "label": "Remember", "items": [
    "Fixing hygiene stops complaints only.",
    "Only motivators inspire effort."]},
   {"type": "diagram", "diagram": "scale", "labels": ["Hygiene", "Motivators"], "height": 150}]},
  {"title": "Examples", "color": "teal", "blocks": [
   {"type": "example", "label": "Hygiene", "items": [
    "A raise stops complaints for a month."]},
   {"type": "example", "label": "Motivator", "items": [
    "Public praise inspires for a year."]}]},
  {"title": "Criticism", "color": "yellow", "blocks": [
   {"type": "points", "label": "Weaknesses", "items": [
    "Based on one interview method.",
    "Ignores individual differences.",
    "Pay can motivate some people."]}]},
 ],
 "footer": ["Hygiene vs motivators", "Job enrichment", "Critical incident method"]},

# ============ 11. Expectancy Theory (Vroom) ============
{"title": "Expectancy Theory", "subtitle": "Chapter 11 - Vroom: Motivation Is a Calculation",
 "sections": [
  {"title": "The Formula", "color": "blue", "blocks": [
   {"type": "def", "label": "Formula", "items": [
    "Motivation = Expectancy x Instrumentality x Valence."]},
   {"type": "revision", "label": "Instant Revision", "items": [
    "If any factor is zero, motivation is zero"]}]},
  {"title": "Expectancy", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Effort " + AR + " performance belief."]},
   {"type": "points", "label": "Question", "items": [
    "'Can I actually do it?'",
    "Boost with training and support."]}]},
  {"title": "Instrumentality", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Performance " + AR + " reward belief."]},
   {"type": "points", "label": "Question", "items": [
    "'Will I really be rewarded?'",
    "Keep promises, link clearly."]}]},
  {"title": "Valence", "color": "pink", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "How much the person values the reward."]},
   {"type": "points", "label": "Question", "items": [
    "'Do I even want that reward?'",
    "One size does NOT fit all."]}]},
  {"title": "Example", "color": "orange", "blocks": [
   {"type": "example", "label": "Example", "items": [
    "Bonus motivates only if achievable, clearly linked, and wanted."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Effort", "Performance", "Reward"], "height": 130}]},
  {"title": "Manager Tips", "color": "teal", "blocks": [
   {"type": "points", "label": "Apply It", "items": [
    "Set clear, reachable goals.",
    "Link rewards to performance openly.",
    "Ask what each person values."]}]},
 ],
 "footer": ["M = E x I x V", "Valence", "Instrumentality"]},

# ============ 12. Goal Setting Theory ============
{"title": "Goal Setting Theory", "subtitle": "Chapter 12 - Locke on High Performance",
 "sections": [
  {"title": "Core Idea", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Specific, hard goals boost performance most (Locke)."]},
   {"type": "revision", "label": "Instant Revision", "items": [
    "'Do your best' is a weak goal"]}]},
  {"title": "SMART Goals", "color": "green", "blocks": [
   {"type": "points", "label": "SMART", "items": [
    "Specific and Measurable.",
    "Achievable and Relevant.",
    "Time-bound with a deadline."]}]},
  {"title": "Why It Works", "color": "purple", "blocks": [
   {"type": "points", "label": "Mechanisms", "items": [
    "Directs attention to what matters.",
    "Energizes effort and persistence.",
    "Encourages better strategies."]}]},
  {"title": "Moderators", "color": "orange", "blocks": [
   {"type": "points", "label": "Works Best When", "items": [
    "High goal commitment.",
    "Regular feedback given.",
    "Person has the ability."]}]},
  {"title": "Pitfalls", "color": "red", "blocks": [
   {"type": "points", "label": "Dangers", "items": [
    "Too many goals " + AR + " overload.",
    "May trigger unethical shortcuts.",
    "Can cause stress and burnout."]}]},
  {"title": "Example", "color": "teal", "blocks": [
   {"type": "example", "label": "Example", "items": [
    "'Raise sales 10% by June' beats 'do your best.'"]},
   {"type": "diagram", "diagram": "flow", "labels": ["Set goal", "Act", "Feedback", "Achieve"], "height": 130}]},
 ],
 "footer": ["SMART goals", "Goal specificity", "Feedback moderates"]},

# ============ 13. Equity Theory ============
{"title": "Equity Theory", "subtitle": "Chapter 13 - Adams on Fairness",
 "sections": [
  {"title": "Core Idea", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "People compare their input/output ratio with others (Adams)."]},
   {"type": "revision", "label": "Instant Revision", "items": [
    "Fairness is felt, not just calculated"]}]},
  {"title": "Inputs", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "What the employee gives."]},
   {"type": "points", "label": "Examples", "items": [
    "Effort, skill, time.",
    "Loyalty and experience."]}]},
  {"title": "Outputs", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "What the employee gets back."]},
   {"type": "points", "label": "Examples", "items": [
    "Pay, recognition, benefits.",
    "Promotions and perks."]}]},
  {"title": "Referents", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "The 'others' we compare with."]},
   {"type": "points", "label": "Examples", "items": [
    "Coworkers and industry peers.",
    "Our own past deals."]}]},
  {"title": "Inequity Responses", "color": "red", "blocks": [
   {"type": "points", "label": "If Underpaid", "items": [
    "Reduce effort or demand a raise.",
    "Quit, or distort the comparison."]},
   {"type": "diagram", "diagram": "scale", "labels": ["My ratio", "Their ratio"], "height": 140}]},
  {"title": "Manager Tips", "color": "teal", "blocks": [
   {"type": "points", "label": "Keep It Fair", "items": [
    "Pay fairly and transparently.",
    "Explain reward criteria.",
    "Listen to fairness concerns."]}]},
 ],
 "footer": ["Inputs vs outputs", "Underpayment inequity", "Referent others"]},

# ============ 14. Job Satisfaction ============
{"title": "Job Satisfaction", "subtitle": "Chapter 14 - Liking Your Work",
 "sections": [
  {"title": "Definition", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Positive feeling about one's job."]},
   {"type": "points", "label": "Note", "items": [
    "An attitude, not a behavior."]}]},
  {"title": "Facets", "color": "green", "blocks": [
   {"type": "points", "label": "Five Facets", "items": [
    "Pay, promotion, coworkers.",
    "Supervision, the work itself."]}]},
  {"title": "Measurement", "color": "purple", "blocks": [
   {"type": "points", "label": "Tools", "items": [
    "JDI: Job Descriptive Index.",
    "Minnesota Satisfaction Questionnaire."]},
   {"type": "diagram", "diagram": "bars", "labels": ["Pay", "Peers", "Work", "Boss"], "height": 140}]},
  {"title": "Causes", "color": "orange", "blocks": [
   {"type": "points", "label": "What Raises It", "items": [
    "Fair rewards and good job fit.",
    "Supportive culture and autonomy."]}]},
  {"title": "Outcomes", "color": "teal", "blocks": [
   {"type": "points", "label": "Results", "items": [
    "Less absenteeism and turnover.",
    "Better customer service.",
    "Slightly higher performance."]}]},
  {"title": "Boosting It", "color": "pink", "blocks": [
   {"type": "points", "label": "Actions", "items": [
    "Recognize effort publicly.",
    "Enrich boring jobs.",
    "Treat people fairly, always."]}]},
 ],
 "footer": ["JDI facets", "Satisfaction-performance link", "Facet satisfaction"]},

# ============ 15. Transformational Leadership ============
{"title": "Transformational Leadership", "subtitle": "Chapter 15 - Inspiring Real Change",
 "sections": [
  {"title": "Definition", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Inspires change through vision and charisma."]},
   {"type": "points", "label": "Effect", "items": [
    "Lifts followers beyond self-interest."]}]},
  {"title": "The Four I's", "color": "green", "blocks": [
   {"type": "points", "label": "Four I's", "items": [
    "Idealized influence (role model).",
    "Inspirational motivation (vision).",
    "Intellectual stimulation (new ideas).",
    "Individualized consideration (coaching)."]}]},
  {"title": "Vs Transactional", "color": "purple", "blocks": [
   {"type": "points", "label": "Transformational", "items": [
    "Inspires with vision and meaning."]},
   {"type": "points", "label": "Transactional", "items": [
    "Exchanges rewards for effort."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Vision", "Inspire", "Change"], "height": 120}]},
  {"title": "Effects", "color": "orange", "blocks": [
   {"type": "points", "label": "Results", "items": [
    "Higher commitment and trust.",
    "More creativity and innovation.",
    "Performance beyond expectations."]}]},
  {"title": "When It Works", "color": "teal", "blocks": [
   {"type": "points", "label": "Best For", "items": [
    "Times of change and crisis.",
    "Growth phases and turnarounds."]}]},
  {"title": "Example", "color": "pink", "blocks": [
   {"type": "example", "label": "Example", "items": [
    "CEO paints a bold vision; the team works late willingly."]},
   {"type": "revision", "label": "Instant Revision", "items": [
    "Transform = change hearts, not just deals"]}]},
 ],
 "footer": ["Four I's", "Charisma", "Transactional contrast"]},

# ============ 16. Servant Leadership ============
{"title": "Servant Leadership", "subtitle": "Chapter 16 - Leading by Serving (Greenleaf)",
 "sections": [
  {"title": "Definition", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "The leader serves first; team growth is the goal (Greenleaf)."]},
   {"type": "revision", "label": "Instant Revision", "items": [
    "'Do those served grow as persons?'"]}]},
  {"title": "Core Traits", "color": "green", "blocks": [
   {"type": "points", "label": "Traits", "items": [
    "Deep listening and empathy.",
    "Healing, humility, stewardship.",
    "Commitment to people's growth."]}]},
  {"title": "Vs Traditional", "color": "purple", "blocks": [
   {"type": "points", "label": "Traditional", "items": [
    "Power OVER people; top-down."]},
   {"type": "points", "label": "Servant", "items": [
    "Power WITH people; support-first."]},
   {"type": "diagram", "diagram": "cycle", "labels": ["Listen", "Empathize", "Grow", "Serve"], "height": 140}]},
  {"title": "Effects", "color": "orange", "blocks": [
   {"type": "points", "label": "Results", "items": [
    "High trust and engagement.",
    "Ethical culture, better retention."]}]},
  {"title": "When It Works", "color": "teal", "blocks": [
   {"type": "points", "label": "Best For", "items": [
    "Service and nonprofit organizations.",
    "Long-term healthy cultures."]}]},
  {"title": "Example", "color": "pink", "blocks": [
   {"type": "example", "label": "Example", "items": [
    "Manager asks daily: 'How can I help you succeed?'"]}]},
 ],
 "footer": ["Greenleaf", "Stewardship", "Empathy first"]},

# ============ 17. Team Dynamics ============
{"title": "Team Dynamics", "subtitle": "Chapter 17 - How Teams Grow and Work",
 "sections": [
  {"title": "Tuckman Stages", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Five stages every team passes through."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Forming", "Storming", "Norming", "Perform"], "height": 130}]},
  {"title": "Stage Meanings", "color": "green", "blocks": [
   {"type": "points", "label": "Stages", "items": [
    "Forming: polite, getting to know.",
    "Storming: conflict over roles.",
    "Norming: rules and trust build.",
    "Performing: smooth high output."]}]},
  {"title": "Team Roles", "color": "purple", "blocks": [
   {"type": "points", "label": "Roles", "items": [
    "Task roles: drive the work forward.",
    "Social roles: keep people united.",
    "Balance both for success."]}]},
  {"title": "Social Loafing", "color": "red", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "People try less hard in groups."]},
   {"type": "points", "label": "Fix It", "items": [
    "Clear individual roles.",
    "Make contributions visible."]}]},
  {"title": "High-Performing Teams", "color": "orange", "blocks": [
   {"type": "points", "label": "Signs", "items": [
    "Clear goals everyone owns.",
    "Trust + healthy debate.",
    "Focus on results, not egos."]}]},
  {"title": "Virtual Teams", "color": "teal", "blocks": [
   {"type": "points", "label": "Keys", "items": [
    "Over-communicate on purpose.",
    "Build trust without hallways.",
    "Right tech + clear norms."]}]},
 ],
 "footer": ["Tuckman 5 stages", "Social loafing", "Team cohesion"]},

# ============ 18. Organizational Culture ============
{"title": "Organizational Culture", "subtitle": "Chapter 18 - How We Do Things Here",
 "sections": [
  {"title": "Definition", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Shared values and norms guiding behavior."]},
   {"type": "revision", "label": "Instant Revision", "items": [
    "Culture = 'how we do things here'"]}]},
  {"title": "Schein's 3 Levels", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Three layers, from visible to deep."]},
   {"type": "diagram", "diagram": "pyramid", "labels": ["Assumptions", "Values", "Artifacts"], "height": 150}]},
  {"title": "Level Meanings", "color": "purple", "blocks": [
   {"type": "points", "label": "Levels", "items": [
    "Artifacts: dress, office, rituals.",
    "Espoused values: stated beliefs.",
    "Basic assumptions: deep, taken-for-granted."]}]},
  {"title": "Culture Types", "color": "orange", "blocks": [
   {"type": "points", "label": "Four Types", "items": [
    "Clan: family-like, collaborative.",
    "Adhocracy: creative, risk-taking.",
    "Market: competitive, results-first.",
    "Hierarchy: structured, controlled."]}]},
  {"title": "Strong vs Weak", "color": "teal", "blocks": [
   {"type": "points", "label": "Strong", "items": [
    "Clear values most members share."]},
   {"type": "points", "label": "Weak", "items": [
    "Fragmented, everyone on their own."]}]},
  {"title": "Changing Culture", "color": "pink", "blocks": [
   {"type": "points", "label": "How", "items": [
    "Slow process, needs leader modeling.",
    "Reward the new values.",
    "Hire for cultural fit."]}]},
 ],
 "footer": ["Schein 3 levels", "Strong culture", "Culture change"]},

# ============ 19. Organizational Change Management ============
{"title": "Change Management", "subtitle": "Chapter 19 - Leading Change (Kotter)",
 "sections": [
  {"title": "Why Change Fails", "color": "red", "blocks": [
   {"type": "points", "label": "Top Reasons", "items": [
    "No sense of urgency.",
    "Weak or unclear vision.",
    "Poor communication."]}]},
  {"title": "Kotter Steps 1-3", "color": "blue", "blocks": [
   {"type": "points", "label": "Start", "items": [
    "1. Create urgency.",
    "2. Build a guiding coalition.",
    "3. Form a clear vision."]}]},
  {"title": "Kotter Steps 4-6", "color": "green", "blocks": [
   {"type": "points", "label": "Move", "items": [
    "4. Communicate the vision.",
    "5. Empower people to act.",
    "6. Create quick wins."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Urgency", "Vision", "Wins", "Anchor"], "height": 120}]},
  {"title": "Kotter Steps 7-8", "color": "purple", "blocks": [
   {"type": "points", "label": "Sustain", "items": [
    "7. Consolidate gains, keep pushing.",
    "8. Anchor change in culture."]}]},
  {"title": "Resistance", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "People push back against change."]},
   {"type": "points", "label": "Causes", "items": [
    "Fear of loss, habit, mistrust.",
    "Fix: involve people early."]}]},
  {"title": "Communication", "color": "teal", "blocks": [
   {"type": "points", "label": "Rules", "items": [
    "Repeat the message often.",
    "Two-way, honest about pain.",
    "Show what stays the same too."]}]},
 ],
 "footer": ["Kotter 8 steps", "Resistance causes", "Quick wins"]},

# ============ 20. Burnout at Work ============
{"title": "Burnout at Work", "subtitle": "Chapter 20 - When Work Drains You",
 "sections": [
  {"title": "Definition", "color": "red", "blocks": [
   {"type": "def", "label": "Definition", "items": [
    "Chronic workplace stress that is not managed (WHO)."]},
   {"type": "points", "label": "Note", "items": [
    "An occupational issue, not a personal failure."]}]},
  {"title": "3 Dimensions", "color": "orange", "blocks": [
   {"type": "def", "label": "Maslach", "items": [
    "Three signs measured together."]},
   {"type": "diagram", "diagram": "bars", "labels": ["Exhaustion", "Cynicism", "Efficacy"], "height": 140}]},
  {"title": "Dimension Meanings", "color": "yellow", "blocks": [
   {"type": "points", "label": "Three D's", "items": [
    "Exhaustion: energy fully drained.",
    "Cynicism: detached, negative attitude.",
    "Low efficacy: feeling ineffective."]}]},
  {"title": "Causes", "color": "purple", "blocks": [
   {"type": "points", "label": "Drivers", "items": [
    "Work overload, no control.",
    "Unfair treatment, value clashes.",
    "No recognition or support."]}]},
  {"title": "Warning Signs", "color": "pink", "blocks": [
   {"type": "points", "label": "Watch For", "items": [
    "Constant fatigue, dreading Monday.",
    "Detachment from coworkers.",
    "More mistakes, less patience."]}]},
  {"title": "Prevention & Recovery", "color": "teal", "blocks": [
   {"type": "points", "label": "Prevent", "items": [
    "Balance workload, allow autonomy."]},
   {"type": "points", "label": "Recover", "items": [
    "Real time off, firm boundaries.",
    "Support; sometimes a job change."]},
   {"type": "revision", "label": "Instant Revision", "items": [
    "Burnout = energy + attitude + efficacy crisis"]}]},
 ],
 "footer": ["Maslach 3 dimensions", "Exhaustion", "Recovery steps"]},
]

if __name__ == "__main__":
    import os
    outdir = "/home/hatch/workspace/zehen/batch4/inf-org-cheat"
    os.makedirs(outdir, exist_ok=True)
    assert len(SPECS) == 20, f"expected 20 specs, got {len(SPECS)}"
    for i, spec in enumerate(SPECS, 1):
        out = os.path.join(outdir, f"org-{i}.png")
        render_cheatsheet(spec, out)
        print("rendered", out, flush=True)
    print("DONE: 20 rendered")
