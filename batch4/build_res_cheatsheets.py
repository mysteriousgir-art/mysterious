#!/usr/bin/env python3
"""Build 20 Research Methods & Statistics cheat-sheet infographics."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cheatsheet import render_cheatsheet

SPECS = []

# ============ 1. Variables: IV, DV and Confounds ============
SPECS.append({
 "title": "Variables: IV, DV and Confounds",
 "subtitle": "Research Methods \u2014 Core Concepts",
 "sections": [
  {"title": "Independent Variable", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["The variable the researcher changes or controls."]},
    {"type": "points", "label": "Key Points", "items": ["Has 2 or more levels (conditions)", "Example: sleep \u2192 4 hours vs 8 hours"]},
    {"type": "example", "label": "Example", "items": ["One class gets extra tuition, the other does not."]},
  ]},
  {"title": "Dependent Variable", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["What is measured to see if the IV had an effect."]},
    {"type": "points", "label": "Key Points", "items": ["Must be measured precisely", "Examples: test scores, reaction time"]},
    {"type": "example", "label": "Example", "items": ["Exam marks measured after tuition (the IV)."]},
  ]},
  {"title": "Confounding Variables", "color": "red", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Hidden variables that spoil results by varying with the IV."]},
    {"type": "points", "label": "Key Points", "items": ["Offer a rival explanation for findings", "Must be controlled or eliminated"]},
    {"type": "example", "label": "Example", "items": ["Smarter students happen to be in the tuition group."]},
  ]},
  {"title": "Extraneous Variables", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Any other variable that could affect the DV."]},
    {"type": "points", "label": "Key Points", "items": ["Kept constant across conditions", "Examples: noise, lighting, time of day"]},
    {"type": "revision", "label": "Instant Revision", "items": ["Extraneous = possible influence; Confound = actual spoiling."]},
  ]},
  {"title": "Operationalisation", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Defining variables so they can be measured exactly."]},
    {"type": "points", "label": "Key Points", "items": ["IV: 'stress' \u2192 exam with 10-min limit", "DV: 'memory' \u2192 words recalled in 2 min"]},
    {"type": "example", "label": "Example", "items": ["'Happiness' \u2192 score on a 1\u201310 scale."]},
  ]},
  {"title": "How They Link", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["IV changed", "DV measured", "Confounds controlled"], "height": 150},
    {"type": "revision", "label": "Instant Revision", "items": ["Change IV \u2192 measure DV \u2192 control the rest."]},
  ]},
 ],
 "footer": ["IV vs DV", "Confounding variables", "Operationalisation", "Levels of the IV"],
})

# ============ 2. Hypotheses and Theories ============
SPECS.append({
 "title": "Hypotheses and Theories",
 "subtitle": "Research Methods \u2014 Starting Research",
 "sections": [
  {"title": "Theory", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["A broad explanation of how things work, built from evidence."]},
    {"type": "points", "label": "Key Points", "items": ["Example: interference theory of forgetting", "Generates testable predictions"]},
  ]},
  {"title": "Hypothesis", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["A precise, testable prediction from a theory."]},
    {"type": "points", "label": "Key Points", "items": ["Must be falsifiable (can be proven wrong)", "Stated before data is collected"]},
    {"type": "example", "label": "Example", "items": ["'Students who sleep 8h recall more words than those who sleep 4h.'"]},
  ]},
  {"title": "Null Hypothesis (H0)", "color": "red", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Predicts NO effect or NO difference. The default position."]},
    {"type": "points", "label": "Key Points", "items": ["Example: 'Sleep hours make no difference to recall.'", "Researchers try to reject H0"]},
  ]},
  {"title": "Alternative (H1)", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Predicts there IS an effect or difference."]},
    {"type": "points", "label": "Key Points", "items": ["Directional: states which group is better", "Non-directional: only states a difference"]},
    {"type": "example", "label": "Example", "items": ["Directional: '8h group recalls MORE words.'"]},
  ]},
  {"title": "Falsifiability", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": ["A good hypothesis must be possible to prove wrong."]},
    {"type": "points", "label": "Key Points", "items": ["Popper: science grows by falsification", "'Invisible forces help memory' is NOT falsifiable"]},
  ]},
  {"title": "From Theory to Test", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Theory", "Hypothesis", "Test", "Conclusion"], "height": 150},
    {"type": "revision", "label": "Instant Revision", "items": ["Theory \u2192 H1 vs H0 \u2192 test \u2192 support or reject."]},
  ]},
 ],
 "footer": ["Null vs alternative", "Directional hypotheses", "Falsifiability", "Operationalised predictions"],
})

# ============ 3. Experimental Design Basics ============
SPECS.append({
 "title": "Experimental Design Basics",
 "subtitle": "Research Methods \u2014 Designs",
 "sections": [
  {"title": "Lab Experiment", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["IV is manipulated in a controlled artificial setting."]},
    {"type": "points", "label": "Key Points", "items": ["High control \u2192 strong cause-effect claims", "Low ecological validity (unnatural)"]},
  ]},
  {"title": "Field Experiment", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["IV is manipulated in a natural, real-life setting."]},
    {"type": "points", "label": "Key Points", "items": ["More natural behaviour than the lab", "Less control over extraneous variables"]},
    {"type": "example", "label": "Example", "items": ["Changing classroom lighting to test focus."]},
  ]},
  {"title": "Natural Experiment", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": ["IV changes naturally; researcher just measures the DV."]},
    {"type": "points", "label": "Key Points", "items": ["No manipulation \u2192 weaker causal claims", "Useful when manipulation is impossible"]},
    {"type": "example", "label": "Example", "items": ["Comparing stress before vs after an earthquake."]},
  ]},
  {"title": "Quasi-Experiment", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Uses pre-existing groups; no random assignment."]},
    {"type": "points", "label": "Key Points", "items": ["Example: comparing men vs women", "Participant variables may confound results"]},
  ]},
  {"title": "Cause and Effect", "color": "red", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Only true experiments can claim the IV CAUSED the DV change."]},
    {"type": "points", "label": "Key Points", "items": ["Needs: manipulation + control + random assignment", "Correlation alone never proves causation"]},
  ]},
  {"title": "Designs Compared", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "bars", "labels": ["Lab", "Field", "Natural"], "height": 150},
    {"type": "revision", "label": "Instant Revision", "items": ["More control = lab; more natural = field/natural."]},
  ]},
 ],
 "footer": ["Lab vs field", "Natural experiments", "Cause and effect", "Quasi-experiments"],
})

# ============ 4. Correlational Research ============
SPECS.append({
 "title": "Correlational Research",
 "subtitle": "Research Methods \u2014 Designs",
 "sections": [
  {"title": "What It Is", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Measures how two variables relate, without manipulating either."]},
    {"type": "points", "label": "Key Points", "items": ["Both variables are simply measured", "Result: a correlation coefficient (r)"]},
  ]},
  {"title": "Positive Correlation", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["As one variable rises, the other rises too."]},
    {"type": "example", "label": "Example", "items": ["More study hours \u2192 higher exam scores."]},
    {"type": "points", "label": "Key Points", "items": ["r is between 0 and +1"]},
  ]},
  {"title": "Negative Correlation", "color": "red", "blocks": [
    {"type": "def", "label": "Definition", "items": ["As one variable rises, the other falls."]},
    {"type": "example", "label": "Example", "items": ["More screen time \u2192 fewer hours of sleep."]},
    {"type": "points", "label": "Key Points", "items": ["r is between 0 and \u22121"]},
  ]},
  {"title": "Zero Correlation", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": ["No relationship between the two variables (r \u2248 0)."]},
    {"type": "example", "label": "Example", "items": ["Shoe size and intelligence: no link."]},
  ]},
  {"title": "Correlation \u2260 Causation", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["A link does NOT prove one variable causes the other."]},
    {"type": "points", "label": "Key Points", "items": ["Third variable may cause both", "Example: ice cream sales \u2194 drowning (heat causes both)"]},
  ]},
  {"title": "Strength Scale", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "scale", "labels": ["\u22121 strong", "+1 strong"], "height": 150},
    {"type": "revision", "label": "Instant Revision", "items": ["Closer to \u00b11 = stronger; near 0 = weaker."]},
  ]},
 ],
 "footer": ["Positive vs negative", "Correlation \u2260 causation", "Third-variable problem", "Scatterplots"],
})

# ============ 5. Survey Methods ============
SPECS.append({
 "title": "Survey Methods",
 "subtitle": "Research Methods \u2014 Data Collection",
 "sections": [
  {"title": "Questionnaires", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Written sets of questions given to many people at once."]},
    {"type": "points", "label": "Key Points", "items": ["Cheap, quick, reach large samples", "Low return rate is a problem"]},
  ]},
  {"title": "Interviews", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Face-to-face or phone conversations with set questions."]},
    {"type": "points", "label": "Key Points", "items": ["Structured: same questions, easy to compare", "Unstructured: flexible, rich detail"]},
    {"type": "example", "label": "Example", "items": ["Clinical interview about anxiety symptoms."]},
  ]},
  {"title": "Open vs Closed Qs", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Closed: fixed answers \u2192 easy to analyse", "Open: free answers \u2192 rich but hard to score"]},
    {"type": "example", "label": "Example", "items": ["Closed: 'Rate stress 1\u20135'; Open: 'Describe your stress.'"]},
  ]},
  {"title": "Response Biases", "color": "red", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Ways answers get distorted."]},
    {"type": "points", "label": "Key Points", "items": ["Social desirability: answering to look good", "Acquiescence: always agreeing"]},
  ]},
  {"title": "Pilot Studies", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Small trial run before the real study."]},
    {"type": "points", "label": "Key Points", "items": ["Spots confusing questions early", "Saves time and money"]},
  ]},
  {"title": "Survey Flow", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Pilot", "Collect", "Analyse"], "height": 150},
    {"type": "revision", "label": "Instant Revision", "items": ["Pilot \u2192 collect \u2192 watch for response bias."]},
  ]},
 ],
 "footer": ["Open vs closed questions", "Social desirability", "Pilot studies", "Structured interviews"],
})

# ============ 6. Case Studies ============
SPECS.append({
 "title": "Case Studies",
 "subtitle": "Research Methods \u2014 Designs",
 "sections": [
  {"title": "What It Is", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["In-depth study of one person, group, or rare event."]},
    {"type": "points", "label": "Key Points", "items": ["Uses interviews, tests, observations together", "Rich, detailed qualitative data"]},
  ]},
  {"title": "Strengths", "color": "green", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Deep insight into rare conditions", "Can challenge existing theories", "Generates ideas for new research"]},
  ]},
  {"title": "Weaknesses", "color": "red", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Cannot generalise from one case", "Researcher bias may creep in", "Hard to replicate exactly"]},
  ]},
  {"title": "Famous Cases", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Phineas Gage: rod through skull \u2192 personality change", "Patient HM: memory loss after brain surgery", "Genie: language without early exposure"]},
  ]},
  {"title": "When to Use", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Rare disorders or unique events", "When experiments are unethical", "As a starting point for theories"]},
  ]},
  {"title": "Case Study Cycle", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "cycle", "labels": ["Observe", "Record", "Analyse", "Theorise"], "height": 170},
    {"type": "revision", "label": "Instant Revision", "items": ["Deep but narrow: rich detail, weak generalisation."]},
  ]},
 ],
 "footer": ["Phineas Gage", "Patient HM", "Generalisation problem", "Researcher bias"],
})

# ============ 7. Naturalistic Observation ============
SPECS.append({
 "title": "Naturalistic Observation",
 "subtitle": "Research Methods \u2014 Data Collection",
 "sections": [
  {"title": "Definition", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Watching behaviour in its natural setting, without interference."]},
    {"type": "points", "label": "Key Points", "items": ["No manipulation of variables", "Behaviour is spontaneous and real"]},
    {"type": "example", "label": "Example", "items": ["Jane Goodall watching chimps in the wild."]},
  ]},
  {"title": "Overt vs Covert", "color": "blue", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Overt: people know they are watched", "Covert: people do NOT know (ethical issues!)"]},
  ]},
  {"title": "Participant vs Non", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Participant: researcher joins the group", "Non-participant: watches from outside"]},
    {"type": "example", "label": "Example", "items": ["Joining a tribe vs watching a playground."]},
  ]},
  {"title": "Strengths", "color": "teal", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["High ecological validity (real life)", "Useful when lab study is impossible"]},
  ]},
  {"title": "Weaknesses", "color": "red", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Observer effect: people act differently", "No control \u2192 cannot prove cause", "Observer bias in recording"]},
  ]},
  {"title": "Watch \u2192 Record", "color": "orange", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Observe", "Record", "Code"], "height": 150},
    {"type": "revision", "label": "Instant Revision", "items": ["Real setting, real behaviour \u2014 but watch for bias."]},
  ]},
 ],
 "footer": ["Overt vs covert", "Observer effect", "Ecological validity", "Jane Goodall"],
})

# ============ 8. Sampling Methods ============
SPECS.append({
 "title": "Sampling Methods",
 "subtitle": "Research Methods \u2014 Who Takes Part",
 "sections": [
  {"title": "Population vs Sample", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Population: everyone of interest. Sample: the few studied."]},
    {"type": "points", "label": "Key Points", "items": ["Good sample \u2192 can generalise results", "Bad sample \u2192 biased conclusions"]},
  ]},
  {"title": "Random Sampling", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Everyone has an equal chance of being picked."]},
    {"type": "points", "label": "Key Points", "items": ["Most representative method", "Example: lottery / random number generator"]},
  ]},
  {"title": "Stratified Sampling", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Population split into groups; random picks from each."]},
    {"type": "points", "label": "Key Points", "items": ["Keeps key proportions (e.g. 50% male, 50% female)", "More work than simple random"]},
  ]},
  {"title": "Opportunity Sampling", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Using whoever is available at the time."]},
    {"type": "points", "label": "Key Points", "items": ["Quick and easy", "Risk: unrepresentative sample"]},
    {"type": "example", "label": "Example", "items": ["Asking students in the canteen."]},
  ]},
  {"title": "Volunteer Sampling", "color": "red", "blocks": [
    {"type": "def", "label": "Definition", "items": ["People choose themselves to take part."]},
    {"type": "points", "label": "Key Points", "items": ["Volunteer bias: keen people differ from others", "Example: replying to an advert"]},
  ]},
  {"title": "Representativeness", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "pyramid", "labels": ["Random (best)", "Stratified", "Systematic", "Opportunity"], "height": 170},
    {"type": "revision", "label": "Instant Revision", "items": ["Random \u2192 best; opportunity/volunteer \u2192 biased."]},
  ]},
 ],
 "footer": ["Random sampling", "Stratified sampling", "Volunteer bias", "Generalisability"],
})

# ============ 9. Random Assignment ============
SPECS.append({
 "title": "Random Assignment",
 "subtitle": "Research Methods \u2014 Fair Groups",
 "sections": [
  {"title": "Definition", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Placing participants into groups purely by chance."]},
    {"type": "points", "label": "Key Points", "items": ["Coin toss, lottery, random numbers", "Used AFTER sampling, before the experiment"]},
  ]},
  {"title": "Why It Matters", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Spreads participant differences evenly across groups."]},
    {"type": "points", "label": "Key Points", "items": ["Controls participant variables (age, IQ, motivation)", "Makes groups equal at the start"]},
  ]},
  {"title": "vs Random Sampling", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Sampling: WHO is picked from the population", "Assignment: WHICH GROUP they join", "Both use chance, different jobs!"]},
    {"type": "revision", "label": "Instant Revision", "items": ["Sampling picks people; assignment splits them."]},
  ]},
  {"title": "Controls Confounds", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Stops all smart people landing in one group", "Any leftover differences are random, not systematic"]},
  ]},
  {"title": "Example", "color": "teal", "blocks": [
    {"type": "example", "label": "Example", "items": ["60 students \u2192 coin toss \u2192 30 tuition, 30 control.", "Groups now match on ability by luck."]},
  ]},
  {"title": "Fair Split Flow", "color": "red", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Sample", "Random split", "Equal groups"], "height": 150},
    {"type": "revision", "label": "Instant Revision", "items": ["Chance decides groups \u2192 fair comparison."]},
  ]},
 ],
 "footer": ["Random assignment", "Participant variables", "Sampling vs assignment", "Fair groups"],
})

# ============ 10. Internal Validity ============
SPECS.append({
 "title": "Internal Validity",
 "subtitle": "Research Methods \u2014 Can We Trust It?",
 "sections": [
  {"title": "Definition", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Did the IV really cause the DV change \u2014 nothing else?"]},
    {"type": "points", "label": "Key Points", "items": ["High = confident about cause and effect", "Low = confounds may explain results"]},
  ]},
  {"title": "Demand Characteristics", "color": "red", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Clues that tell participants the aim; they change behaviour."]},
    {"type": "points", "label": "Key Points", "items": ["Example: guessing it's a memory test \u2192 trying harder", "Fix: single-blind, cover story"]},
  ]},
  {"title": "Order Effects", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Doing tasks in order changes later performance."]},
    {"type": "points", "label": "Key Points", "items": ["Practice effect: get better with repetition", "Fatigue effect: get worse when tired", "Fix: counterbalancing (ABBA)"]},
  ]},
  {"title": "Participant Variables", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Personal differences between participants."]},
    {"type": "points", "label": "Key Points", "items": ["Age, IQ, personality, motivation", "Fix: random assignment, matched pairs"]},
  ]},
  {"title": "Investigator Effects", "color": "pink", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Researcher's behaviour unconsciously affects participants."]},
    {"type": "points", "label": "Key Points", "items": ["Tone of voice, hints, expectations", "Fix: standardised instructions, double-blind"]},
  ]},
  {"title": "Protect Validity", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Blind", "Counterbalance", "Standardise"], "height": 150},
    {"type": "revision", "label": "Instant Revision", "items": ["Blind + counterbalance + standardise = safer."]},
  ]},
 ],
 "footer": ["Demand characteristics", "Order effects", "Double-blind", "Counterbalancing"],
})

# ============ 11. External Validity ============
SPECS.append({
 "title": "External Validity",
 "subtitle": "Research Methods \u2014 Does It Apply?",
 "sections": [
  {"title": "Definition", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Can results be generalised beyond this study?"]},
    {"type": "points", "label": "Key Points", "items": ["To other people, places, and times", "Opposite of internal validity's focus"]},
  ]},
  {"title": "Ecological Validity", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Do findings apply to real-life settings?"]},
    {"type": "points", "label": "Key Points", "items": ["Lab studies often score LOW here", "Field studies score HIGHER"]},
    {"type": "example", "label": "Example", "items": ["Memory tested in a real classroom vs a lab cubicle."]},
  ]},
  {"title": "Population Validity", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Can we generalise to the wider population?"]},
    {"type": "points", "label": "Key Points", "items": ["Needs a representative sample", "Student samples limit generalisation"]},
  ]},
  {"title": "Mundane Realism", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": ["How much the study mirrors everyday life."]},
    {"type": "points", "label": "Key Points", "items": ["High: tasks feel like real life", "Low: strange artificial tasks"]},
  ]},
  {"title": "The Trade-Off", "color": "red", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Control and naturalness pull in opposite directions."]},
    {"type": "points", "label": "Key Points", "items": ["Lab: high internal, low external", "Field: lower internal, higher external"]},
  ]},
  {"title": "Validity Balance", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "scale", "labels": ["Control", "Natural"], "height": 150},
    {"type": "revision", "label": "Instant Revision", "items": ["More control \u2194 less real-life fit. Balance both!"]},
  ]},
 ],
 "footer": ["Ecological validity", "Population validity", "Lab vs field trade-off", "Mundane realism"],
})

# ============ 12. Reliability Types ============
SPECS.append({
 "title": "Reliability Types",
 "subtitle": "Research Methods \u2014 Consistency",
 "sections": [
  {"title": "What Is Reliability?", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["A measure is reliable if it gives consistent results."]},
    {"type": "points", "label": "Key Points", "items": ["Same test \u2192 same score, every time", "Reliability \u2260 validity (consistent can still be wrong!)"]},
  ]},
  {"title": "Test\u2013Retest", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Same test given twice; scores should match."]},
    {"type": "points", "label": "Key Points", "items": ["Check with correlation between the two scores", "Problem: practice effects on retest"]},
    {"type": "example", "label": "Example", "items": ["IQ test in January and again in June."]},
  ]},
  {"title": "Inter-Rater", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Two observers score the same behaviour similarly."]},
    {"type": "points", "label": "Key Points", "items": ["Important for observations and interviews", "Fix: train raters, clear categories"]},
  ]},
  {"title": "Internal Consistency", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": ["All items in a test measure the same thing."]},
    {"type": "points", "label": "Key Points", "items": ["Split-half: two halves should agree", "Cronbach's alpha: the common statistic"]},
  ]},
  {"title": "Improving Reliability", "color": "teal", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Pilot test and refine questions", "Standardise instructions and scoring", "Train all observers the same way"]},
  ]},
  {"title": "Reliability Loop", "color": "red", "blocks": [
    {"type": "diagram", "diagram": "cycle", "labels": ["Test", "Retest", "Compare"], "height": 170},
    {"type": "revision", "label": "Instant Revision", "items": ["Consistent = reliable; accurate = valid. Need both!"]},
  ]},
 ],
 "footer": ["Test-retest", "Inter-rater reliability", "Cronbach's alpha", "Reliability vs validity"],
})

# ============ 13. Central Tendency ============
SPECS.append({
 "title": "Central Tendency: Mean, Median, Mode",
 "subtitle": "Statistics \u2014 Averages",
 "sections": [
  {"title": "Mean", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Add all scores, divide by how many there are."]},
    {"type": "points", "label": "Key Points", "items": ["Uses every score \u2192 most sensitive", "Weakness: dragged by extreme scores"]},
    {"type": "example", "label": "Example", "items": ["2, 4, 6 \u2192 mean = 12 \u00f7 3 = 4."]},
  ]},
  {"title": "Median", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["The middle score when data is in order."]},
    {"type": "points", "label": "Key Points", "items": ["Not affected by extreme scores", "Best for skewed data (e.g. incomes)"]},
    {"type": "example", "label": "Example", "items": ["1, 3, 9 \u2192 median = 3."]},
  ]},
  {"title": "Mode", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["The most frequent score."]},
    {"type": "points", "label": "Key Points", "items": ["Only average for categories (nominal data)", "A data set can have two modes (bimodal)"]},
    {"type": "example", "label": "Example", "items": ["2, 3, 3, 5 \u2192 mode = 3."]},
  ]},
  {"title": "When to Use Which", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Normal data \u2192 mean", "Skewed data \u2192 median", "Categories \u2192 mode"]},
  ]},
  {"title": "Skew Effect", "color": "red", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["One billionaire in the room \u2192 mean income jumps", "Median stays sensible \u2192 use median!"]},
  ]},
  {"title": "Compare the Three", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "bars", "labels": ["Mean", "Median", "Mode"], "height": 150},
    {"type": "revision", "label": "Instant Revision", "items": ["Mean = balance point; median = middle; mode = most common."]},
  ]},
 ],
 "footer": ["Mean vs median", "Skewed data", "Bimodal", "Nominal data \u2192 mode"],
})

# ============ 14. Variability ============
SPECS.append({
 "title": "Variability: Range, Variance, SD",
 "subtitle": "Statistics \u2014 Spread of Data",
 "sections": [
  {"title": "Range", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Highest score minus lowest score."]},
    {"type": "points", "label": "Key Points", "items": ["Quick but crude", "Affected by one extreme score"]},
    {"type": "example", "label": "Example", "items": ["Scores 4\u201318 \u2192 range = 14."]},
  ]},
  {"title": "Variance", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Average of squared differences from the mean."]},
    {"type": "points", "label": "Key Points", "items": ["Step 1: each score minus mean", "Step 2: square, add up, divide by N"]},
  ]},
  {"title": "Standard Deviation", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Square root of variance \u2014 average distance from mean."]},
    {"type": "points", "label": "Key Points", "items": ["Same units as the original scores", "Small SD = scores cluster; large SD = spread out"]},
  ]},
  {"title": "Why SD Matters", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Shows how consistent the data is", "Needed for z-scores and t-tests", "Two groups can share a mean but differ in SD"]},
  ]},
  {"title": "Reading SD", "color": "teal", "blocks": [
    {"type": "example", "label": "Example", "items": ["Class A: mean 70, SD 3 \u2192 all near 70.", "Class B: mean 70, SD 15 \u2192 very mixed."]},
  ]},
  {"title": "Spread Compared", "color": "red", "blocks": [
    {"type": "diagram", "diagram": "bars", "labels": ["Range", "Variance", "SD"], "height": 150},
    {"type": "revision", "label": "Instant Revision", "items": ["Range = quick; SD = best single spread number."]},
  ]},
 ],
 "footer": ["Standard deviation", "Range", "Variance", "Interpreting spread"],
})

# ============ 15. Normal Distribution ============
SPECS.append({
 "title": "Normal Distribution",
 "subtitle": "Statistics \u2014 The Bell Curve",
 "sections": [
  {"title": "The Bell Curve", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Symmetrical curve: most scores in the middle, few at ends."]},
    {"type": "points", "label": "Key Points", "items": ["Mean = median = mode (all at centre)", "Examples: height, IQ, exam scores"]},
  ]},
  {"title": "68\u201395\u201399.7 Rule", "color": "green", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["68% of scores within \u00b11 SD of mean", "95% within \u00b12 SD", "99.7% within \u00b13 SD"]},
    {"type": "revision", "label": "Instant Revision", "items": ["Memorise: 68 \u2192 95 \u2192 99.7. MCQ favourite!"]},
  ]},
  {"title": "Positive Skew", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Tail stretches right; most scores are LOW."]},
    {"type": "points", "label": "Key Points", "items": ["Mean > median (pulled by tail)", "Example: income distribution"]},
  ]},
  {"title": "Negative Skew", "color": "red", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Tail stretches left; most scores are HIGH."]},
    {"type": "points", "label": "Key Points", "items": ["Mean < median", "Example: easy exam scores"]},
  ]},
  {"title": "Why It Matters", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Many tests (t-test) assume normality", "Lets us use z-scores and probabilities"]},
  ]},
  {"title": "Curve Zones", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "bars", "labels": ["68%", "95%", "99.7%"], "height": 150},
    {"type": "revision", "label": "Instant Revision", "items": ["Symmetrical \u2192 mean = median = mode."]},
  ]},
 ],
 "footer": ["68-95-99.7 rule", "Positive vs negative skew", "Mean = median = mode", "Normality assumption"],
})

# ============ 16. Correlation Coefficients ============
SPECS.append({
 "title": "Correlation Coefficients",
 "subtitle": "Statistics \u2014 Measuring Links",
 "sections": [
  {"title": "The r Value", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["A number from \u22121 to +1 showing link strength and direction."]},
    {"type": "points", "label": "Key Points", "items": ["Sign = direction (+ or \u2212)", "Size = strength (near 1 = strong)"]},
  ]},
  {"title": "Strength Guide", "color": "green", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["0.7\u20131.0: strong link", "0.3\u20130.7: moderate link", "0\u20130.3: weak link"]},
    {"type": "example", "label": "Example", "items": ["r = +0.85 \u2192 strong positive link."]},
  ]},
  {"title": "Pearson's r", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["For two continuous variables with a linear link."]},
    {"type": "points", "label": "Key Points", "items": ["Needs interval/ratio data", "Example: height vs weight"]},
  ]},
  {"title": "Spearman's rho", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": ["For ranked (ordinal) data or non-linear links."]},
    {"type": "points", "label": "Key Points", "items": ["Uses ranks, not raw scores", "Example: class rank vs effort rank"]},
  ]},
  {"title": "Causation Warning", "color": "red", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["r = +0.9 still does NOT prove cause!", "Third variables may drive both", "Only experiments show causation"]},
  ]},
  {"title": "Strength Scale", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "scale", "labels": ["\u22121", "0", "+1"], "height": 150},
    {"type": "revision", "label": "Instant Revision", "items": ["Pearson = continuous; Spearman = ranked."]},
  ]},
 ],
 "footer": ["Pearson vs Spearman", "Strength guide", "r = \u22121 to +1", "Correlation \u2260 causation"],
})

# ============ 17. P-Values Explained Simply ============
SPECS.append({
 "title": "P-Values Explained Simply",
 "subtitle": "Statistics \u2014 Significance",
 "sections": [
  {"title": "What Is p?", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Probability the result happened by luck alone."]},
    {"type": "points", "label": "Key Points", "items": ["p = 0.03 \u2192 3% chance it's just luck", "Small p = result looks REAL"]},
  ]},
  {"title": "p < 0.05", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["The usual cut-off: result is 'significant'."]},
    {"type": "points", "label": "Key Points", "items": ["Below 0.05 \u2192 reject the null hypothesis", "Above 0.05 \u2192 keep the null (not proven!)"]},
    {"type": "example", "label": "Example", "items": ["p = 0.02 \u2192 significant \u2713; p = 0.20 \u2192 not significant."]},
  ]},
  {"title": "Type I Error", "color": "red", "blocks": [
    {"type": "def", "label": "Definition", "items": ["False alarm: claiming an effect that isn't real."]},
    {"type": "points", "label": "Key Points", "items": ["Rejecting H0 when H0 is actually true", "Rate = alpha (usually 5%)"]},
  ]},
  {"title": "Type II Error", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Miss: failing to spot a real effect."]},
    {"type": "points", "label": "Key Points", "items": ["Keeping H0 when H1 is actually true", "Small samples raise this risk"]},
  ]},
  {"title": "Common Mistakes", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["p is NOT the chance H1 is true", "p > 0.05 does NOT prove 'no effect'", "Significant \u2260 important (check effect size!)"]},
  ]},
  {"title": "Decision Flow", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["Get p", "p<0.05?", "Decide"], "height": 150},
    {"type": "revision", "label": "Instant Revision", "items": ["p < .05 \u2192 reject H0. Type I = false alarm."]},
  ]},
 ],
 "footer": ["p < 0.05", "Type I vs Type II error", "Rejecting H0", "Significance \u2260 importance"],
})

# ============ 18. T-Tests Explained Simply ============
SPECS.append({
 "title": "T-Tests Explained Simply",
 "subtitle": "Statistics \u2014 Comparing Means",
 "sections": [
  {"title": "What Is a t-test?", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Compares two means to see if they differ significantly."]},
    {"type": "points", "label": "Key Points", "items": ["Needs: interval data, roughly normal", "Result: t value \u2192 p value"]},
  ]},
  {"title": "Independent t-test", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Compares TWO SEPARATE groups."]},
    {"type": "points", "label": "Key Points", "items": ["Between-subjects design", "Example: tuition group vs control group"]},
  ]},
  {"title": "Paired t-test", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Compares the SAME people twice."]},
    {"type": "points", "label": "Key Points", "items": ["Repeated-measures design", "Example: scores before vs after tuition"]},
  ]},
  {"title": "One vs Two Tailed", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["One-tailed: predicts direction (H1 directional)", "Two-tailed: any difference (safer, common)"]},
  ]},
  {"title": "Assumptions", "color": "red", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Data roughly normally distributed", "Similar variances in both groups", "Scores independent of each other"]},
  ]},
  {"title": "Pick the Test", "color": "teal", "blocks": [
    {"type": "diagram", "diagram": "flow", "labels": ["2 groups?", "Same people?", "Pick t"], "height": 150},
    {"type": "revision", "label": "Instant Revision", "items": ["Separate groups \u2192 independent; same people \u2192 paired."]},
  ]},
 ],
 "footer": ["Independent vs paired", "One vs two tailed", "Assumptions", "Comparing two means"],
})

# ============ 19. Effect Sizes ============
SPECS.append({
 "title": "Effect Sizes",
 "subtitle": "Statistics \u2014 How Big Is the Effect?",
 "sections": [
  {"title": "What Is It?", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["How BIG the difference or link is \u2014 not just if it's real."]},
    {"type": "points", "label": "Key Points", "items": ["p says 'is it real?'; effect size says 'does it matter?'", "Not affected by sample size like p is"]},
  ]},
  {"title": "Cohen's d", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Standardised difference between two means."]},
    {"type": "points", "label": "Key Points", "items": ["d = (mean1 \u2212 mean2) \u00f7 SD", "Lets studies be compared fairly"]},
  ]},
  {"title": "Small / Med / Large", "color": "purple", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["d \u2248 0.2 \u2192 small effect", "d \u2248 0.5 \u2192 medium effect", "d \u2248 0.8+ \u2192 large effect"]},
    {"type": "revision", "label": "Instant Revision", "items": ["0.2 small \u2192 0.5 medium \u2192 0.8 large."]},
  ]},
  {"title": "Why It Matters", "color": "orange", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["Huge samples make tiny effects 'significant'", "Effect size shows practical importance", "Always report it alongside p!"]},
    {"type": "example", "label": "Example", "items": ["p = 0.01 but d = 0.1 \u2192 real but trivial."]},
  ]},
  {"title": "Other Measures", "color": "teal", "blocks": [
    {"type": "points", "label": "Key Points", "items": ["r\u00b2: % of variance explained", "Odds ratio: for categorical outcomes", "Eta squared: used with ANOVA"]},
  ]},
  {"title": "Size Ladder", "color": "red", "blocks": [
    {"type": "diagram", "diagram": "bars", "labels": ["0.2", "0.5", "0.8+"], "height": 150},
    {"type": "revision", "label": "Instant Revision", "items": ["Significant \u2260 important. Report d!"]},
  ]},
 ],
 "footer": ["Cohen's d", "0.2 / 0.5 / 0.8", "Practical significance", "Report with p"],
})

# ============ 20. Research Ethics in Depth ============
SPECS.append({
 "title": "Research Ethics in Depth",
 "subtitle": "Research Methods \u2014 Doing It Right",
 "sections": [
  {"title": "Informed Consent", "color": "blue", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Participants agree freely, knowing what the study involves."]},
    {"type": "points", "label": "Key Points", "items": ["Must be given BEFORE the study", "Children need parental consent too"]},
  ]},
  {"title": "Deception", "color": "red", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Misleading participants about the true aim."]},
    {"type": "points", "label": "Key Points", "items": ["Only if no other way + approved", "Must debrief fully afterwards"]},
    {"type": "example", "label": "Example", "items": ["Milgram: fake 'learning' study on obedience."]},
  ]},
  {"title": "Debriefing", "color": "green", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Explaining the true aims after the study ends."]},
    {"type": "points", "label": "Key Points", "items": ["Reveals any deception used", "Checks no harm was done", "Offers right to withdraw data"]},
  ]},
  {"title": "Right to Withdraw", "color": "orange", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Leave the study any time, no penalty."]},
    {"type": "points", "label": "Key Points", "items": ["Includes withdrawing data afterwards", "Must be stated up front"]},
  ]},
  {"title": "Confidentiality", "color": "purple", "blocks": [
    {"type": "def", "label": "Definition", "items": ["Personal data kept private; identities hidden."]},
    {"type": "points", "label": "Key Points", "items": ["Use codes/numbers, not names", "Anonymity = even researcher can't identify"]},
  ]},
  {"title": "Protection from Harm", "color": "teal", "blocks": [
    {"type": "def", "label": "Definition", "items": ["No physical or psychological harm to anyone."]},
    {"type": "points", "label": "Key Points", "items": ["Risk assessed before approval", "Stop if distress appears"]},
    {"type": "diagram", "diagram": "flow", "labels": ["Consent", "Protect", "Debrief"], "height": 120},
  ]},
 ],
 "footer": ["Informed consent", "Debriefing", "Right to withdraw", "Confidentiality"],
})

# ---------------- render ----------------
if __name__ == "__main__":
    import json
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inf-res-cheat")
    os.makedirs(outdir, exist_ok=True)
    titles = [t["title"] for t in json.load(open(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "inf-res.json")))]
    assert len(SPECS) == 20, "need 20 specs, got %d" % len(SPECS)
    for i, spec in enumerate(SPECS):
        exp = titles[i]
        if spec["title"] != exp:
            print("TITLE MISMATCH %d: spec=%r json=%r" % (i + 1, spec["title"], exp))
        out = os.path.join(outdir, "res-%02d.png" % (i + 1))
        render_cheatsheet(spec, out)
        print("rendered", out, os.path.getsize(out))
    print("DONE: %d images" % len(SPECS))
