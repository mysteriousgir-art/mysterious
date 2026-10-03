#!/usr/bin/env python3
"""Generate 20 Biological Psychology cheat-sheet infographics."""
import sys, os
sys.path.insert(0, '/home/hatch/workspace/zehen/batch4')
from cheatsheet import render_cheatsheet

SPECS = []

# ---------------- 1. The Neuron in Depth ----------------
SPECS.append({
 "title": "The Neuron in Depth", "subtitle": "Chapter 1 \u2013 The Brain's Building Blocks",
 "sections": [
  {"title": "The Neuron", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Nerve cell \u2014 basic communication unit of the nervous system.", "Brain has about 86 billion neurons, trillions of connections."]},
   {"type": "diagram", "diagram": "brain", "labels": [], "height": 120},
   {"type": "revision", "label": "Instant Revision", "items": ["Neuron = messenger cell of the brain."]}]},
  {"title": "Three Main Parts", "color": "teal", "blocks": [
   {"type": "points", "label": "Key Points", "items": ["Dendrites receive signals from other neurons.", "Cell body (soma) processes incoming signals.", "Axon carries the message away to other neurons."]},
   {"type": "example", "label": "Example", "items": ["Dendrites catch messages like tree branches catch sunlight."]}]},
  {"title": "Myelin Sheath", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Fatty layer by glial cells wrapping the axon.", "Insulates the axon \u2192 signals travel much faster."]},
   {"type": "example", "label": "Example", "items": ["MS damages myelin \u2192 weakness and numbness."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Myelin = insulation \u2192 speed."]}]},
  {"title": "Glial Cells", "color": "orange", "blocks": [
   {"type": "points", "label": "Key Points", "items": ["Feed neurons, clean waste, form myelin.", "Fight infections in the brain.", "Outnumber neurons about 10 to 1."]},
   {"type": "example", "label": "Example", "items": ["Astrocytes clean extra chemicals around neurons."]}]},
  {"title": "Neuron Types", "color": "purple", "blocks": [
   {"type": "points", "label": "Key Points", "items": ["Sensory (afferent): senses \u2192 brain and spinal cord.", "Motor (efferent): brain \u2192 muscles.", "Interneurons: connect neurons inside the CNS."]},
   {"type": "example", "label": "Example", "items": ["Hot stove: sensory in, motor pulls hand back."]}]},
  {"title": "Neurogenesis", "color": "pink", "blocks": [
   {"type": "def", "label": "Definition", "items": ["New neurons can grow in the hippocampus.", "Most neurons do not divide or replace themselves."]},
   {"type": "revision", "label": "Instant Revision", "items": ["New neurons = mainly in hippocampus."]}]},
 ],
 "footer": ["Neuron parts", "Myelin sheath", "Glial cells", "Neuron types", "Neurogenesis"],
})

# ---------------- 2. Action Potential Explained ----------------
SPECS.append({
 "title": "Action Potential Explained", "subtitle": "Chapter 2 \u2013 How Neurons Fire",
 "sections": [
  {"title": "Resting Potential", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["At rest the neuron sits at about -70 mV.", "Inside is negative; sodium crowds outside, potassium inside."]},
   {"type": "example", "label": "Example", "items": ["Like a sprinter waiting in the starting blocks."]}]},
  {"title": "Threshold", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["About -55 mV \u2014 the firing line.", "Weak stimulus below threshold = nothing happens."]},
   {"type": "example", "label": "Example", "items": ["Light tap = no pain; hard pinch = pain signal fires."]},
   {"type": "revision", "label": "Instant Revision", "items": ["No threshold crossed \u2192 no firing."]}]},
  {"title": "Depolarization", "color": "red", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Sodium channels open \u2192 Na+ rushes in.", "Charge spikes up to about +40 mV."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Rest -70", "Threshold -55", "Peak +40"], "height": 130}]},
  {"title": "Repolarization", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Potassium flows out \u2192 charge falls back to rest.", "Briefly dips below -70 mV = hyperpolarization."]},
   {"type": "example", "label": "Example", "items": ["Like dominoes falling one after another down the axon."]}]},
  {"title": "Refractory Period", "color": "purple", "blocks": [
   {"type": "points", "label": "Key Points", "items": ["Absolute: neuron cannot fire again at all.", "Relative: needs a stronger push to fire.", "Keeps signals traveling one way only."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Refractory = brief recovery pause."]}]},
  {"title": "All-or-None Law", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Neuron fires at full strength or not at all.", "Stronger stimulus = faster firing, not bigger signal."]},
   {"type": "example", "label": "Example", "items": ["A gun fires or it does not \u2014 no half-shots."]}]},
 ],
 "footer": ["Resting -70 mV", "Threshold -55 mV", "Depolarization", "All-or-none law", "Refractory period"],
})

# ---------------- 3. Synapses and Neurotransmission ----------------
SPECS.append({
 "title": "Synapses and Neurotransmission", "subtitle": "Chapter 3 \u2013 How Neurons Talk",
 "sections": [
  {"title": "The Synapse", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Junction where one neuron passes its message on.", "Three parts: presynaptic terminal, cleft, postsynaptic side."]},
   {"type": "example", "label": "Example", "items": ["Two neurons never touch \u2014 they whisper across a gap."]}]},
  {"title": "Release Process", "color": "orange", "blocks": [
   {"type": "points", "label": "Key Points", "items": ["Action potential reaches the terminal.", "Calcium enters \u2192 vesicles burst open.", "Neurotransmitters spill into the cleft."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Release", "Cross gap", "Bind"], "height": 120}]},
  {"title": "Receptors", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Key-and-lock binding on the next neuron.", "Each receptor accepts only specific transmitters."]},
   {"type": "example", "label": "Example", "items": ["Serotonin cannot open a dopamine receptor."]}]},
  {"title": "Excite vs Inhibit", "color": "teal", "blocks": [
   {"type": "points", "label": "Key Points", "items": ["EPSP: excitatory \u2192 pushes toward firing.", "IPSP: inhibitory \u2192 pushes away from firing.", "Neuron sums all inputs before deciding."]},
   {"type": "diagram", "diagram": "scale", "labels": ["Excite", "Inhibit"], "height": 130}]},
  {"title": "Cleanup", "color": "green", "blocks": [
   {"type": "points", "label": "Key Points", "items": ["Reuptake: sucked back into the sender.", "Enzymes break the transmitter down.", "Some simply drifts away."]},
   {"type": "example", "label": "Example", "items": ["Prozac blocks serotonin reuptake \u2192 mood lifts."]}]},
  {"title": "Drugs Hijack Synapses", "color": "red", "blocks": [
   {"type": "points", "label": "Key Points", "items": ["Botox blocks transmitter release.", "Curare blocks receptors \u2192 paralysis."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Drugs target: release, binding, or reuptake."]}]},
 ],
 "footer": ["Synapse parts", "Vesicle release", "Receptors", "EPSP vs IPSP", "Reuptake"],
})

# ---------------- 4. Serotonin: Mood and More ----------------
SPECS.append({
 "title": "Serotonin: Mood and More", "subtitle": "Chapter 4 \u2013 The Mood Chemical",
 "sections": [
  {"title": "What Is Serotonin?", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Neurotransmitter made from amino acid tryptophan.", "Produced mainly in the raphe nuclei of the brainstem."]},
   {"type": "example", "label": "Example", "items": ["Turkey has tryptophan \u2014 the sleepy effect is mostly myth."]}]},
  {"title": "What It Regulates", "color": "teal", "blocks": [
   {"type": "points", "label": "Key Points", "items": ["Mood, sleep, appetite, aggression, pain perception."]},
   {"type": "diagram", "diagram": "cycle", "labels": ["Mood", "Sleep", "Appetite"], "height": 150}]},
  {"title": "Low Serotonin", "color": "purple", "blocks": [
   {"type": "points", "label": "Key Points", "items": ["Linked to depression, anxiety, OCD.", "Also impulsivity and aggression."]},
   {"type": "example", "label": "Example", "items": ["Feeling flat, worried, unable to enjoy old pleasures."]}]},
  {"title": "SSRIs", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Block serotonin reuptake \u2192 more stays in synapses.", "First-line treatment for depression."]},
   {"type": "example", "label": "Example", "items": ["Prozac (fluoxetine) was the first famous SSRI."]},
   {"type": "revision", "label": "Instant Revision", "items": ["SSRI = more serotonin in the gap."]}]},
  {"title": "Gut-Brain Surprise", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["About 90% of serotonin is in the gut.", "Controls digestion \u2014 the \u2018second brain\u2019 in your belly."]},
   {"type": "example", "label": "Example", "items": ["Stomach problems often come with low mood."]}]},
  {"title": "Caution", "color": "red", "blocks": [
   {"type": "points", "label": "Key Points", "items": ["Serotonin syndrome: drug combos \u2192 fever, agitation.", "SSRIs take 2\u20136 weeks \u2014 receptors need time.", "Sunlight boosts serotonin production."]}]},
 ],
 "footer": ["Serotonin functions", "SSRIs", "Gut serotonin 90%", "Serotonin syndrome", "Low serotonin effects"],
})

# ---------------- 5. Dopamine: Reward and Motivation ----------------
SPECS.append({
 "title": "Dopamine: Reward and Motivation", "subtitle": "Chapter 5 \u2013 The Motivation Molecule",
 "sections": [
  {"title": "Reward Pathway", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Mesolimbic pathway: VTA \u2192 nucleus accumbens.", "Fires when we get rewards \u2014 food, praise, wins."]},
   {"type": "example", "label": "Example", "items": ["First bite of cake after a long diet feels amazing."]}]},
  {"title": "Wanting vs Liking", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Berridge: dopamine = wanting (craving), not liking.", "Explains addiction: craving without pleasure."]},
   {"type": "diagram", "diagram": "scale", "labels": ["Wanting", "Liking"], "height": 130}]},
  {"title": "Surprise Effect", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Dopamine spikes most for unexpected rewards.", "Prediction error signal \u2014 surprises thrill us."]},
   {"type": "example", "label": "Example", "items": ["Slot machines pay unpredictably \u2192 highly addictive."]}]},
  {"title": "Movement", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Parkinson\u2019s: dopamine neurons die \u2192 tremor, rigidity.", "L-DOPA treatment replaces lost dopamine."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Low dopamine \u2192 Parkinson\u2019s disease."]}]},
  {"title": "Schizophrenia Link", "color": "red", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Excess dopamine in some pathways \u2192 hallucinations.", "Antipsychotics block D2 receptors to calm them."]},
   {"type": "example", "label": "Example", "items": ["Hallucinations fade, but stiffness can appear."]}]},
  {"title": "ADHD", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Dopamine dysregulation in attention circuits.", "Stimulants raise dopamine \u2192 paradoxical calm focus."]},
   {"type": "example", "label": "Example", "items": ["Hyperactive child can suddenly sit still and focus."]}]},
 ],
 "footer": ["Reward pathway", "Wanting vs liking", "Parkinson's", "Schizophrenia", "ADHD", "Addiction"],
})

# ---------------- 6. Brain Lobes and Functions ----------------
SPECS.append({
 "title": "Brain Lobes and Functions", "subtitle": "Chapter 6 \u2013 Mapping the Cortex",
 "sections": [
  {"title": "Frontal Lobe", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Planning, decision-making, judgment, personality.", "Contains the motor cortex directing voluntary movement."]},
   {"type": "example", "label": "Example", "items": ["Phineas Gage: rod through frontal lobe \u2192 personality changed."]}]},
  {"title": "Broca\u2019s Area", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Speech production, in the left frontal lobe.", "Broca\u2019s aphasia: understands, but halting speech."]},
   {"type": "diagram", "diagram": "brain", "labels": [], "height": 120}]},
  {"title": "Parietal Lobe", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Touch, temperature, pain, body position.", "Spatial awareness and math live here too."]},
   {"type": "example", "label": "Example", "items": ["Feeling fabric texture without looking."]}]},
  {"title": "Temporal Lobe", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Hearing; hippocampus (memory), amygdala (emotion).", "Wernicke\u2019s area: language comprehension."]},
   {"type": "example", "label": "Example", "items": ["Recognizing a friend\u2019s face in a crowd."]}]},
  {"title": "Occipital Lobe", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Devoted to vision processing.", "Damage \u2192 visual deficits matching the injured spot."]},
   {"type": "example", "label": "Example", "items": ["Back-of-head blow \u2192 blindness with healthy eyes."]}]},
  {"title": "Crossover Rule", "color": "pink", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Left hemisphere controls the right body side.", "Right hemisphere controls the left body side."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Left brain \u2192 right body (contralateral)."]}]},
 ],
 "footer": ["4 lobes", "Broca's area", "Wernicke's area", "Phineas Gage", "Contralateral control"],
})

# ---------------- 7. The Limbic System ----------------
SPECS.append({
 "title": "The Limbic System", "subtitle": "Chapter 7 \u2013 The Emotional Brain",
 "sections": [
  {"title": "Overview", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Ring of deep structures for emotion + memory.", "Smell connects straight to it, bypassing logic."]},
   {"type": "example", "label": "Example", "items": ["Grandma\u2019s perfume floods you with childhood memories."]}]},
  {"title": "Amygdala", "color": "red", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Brain\u2019s threat detector.", "\u2018Low road\u2019 fear in milliseconds \u2014 before conscious thought."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Threat", "Amygdala", "Fear"], "height": 120},
   {"type": "example", "label": "Example", "items": ["Jump at a rustle before knowing what it was."]}]},
  {"title": "Hippocampus", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Forms new explicit (declarative) memories.", "H.M. lost it \u2192 could never form new memories."]},
   {"type": "example", "label": "Example", "items": ["Taxi drivers grow larger hippocampi with practice."]}]},
  {"title": "Hypothalamus", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Body\u2019s control center: hunger, thirst, temperature.", "Sleep and hormones too; links brain + endocrine system."]}]},
  {"title": "Top-Down Control", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Prefrontal cortex calms the limbic system.", "Meditation strengthens this control."]},
   {"type": "example", "label": "Example", "items": ["Heartbreak registers like physical pain (cingulate)."]}]},
  {"title": "Damage Clues", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Kluver-Bucy (amygdala damage) = fearlessness.", "Shows how much the amygdala normally restrains."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Amygdala = fear; hippocampus = memory."]}]},
 ],
 "footer": ["Amygdala", "Hippocampus", "Hypothalamus", "H.M. case", "Low road fear"],
})

# ---------------- 8. Neuroplasticity ----------------
SPECS.append({
 "title": "Neuroplasticity", "subtitle": "Chapter 8 \u2013 The Rewiring Brain",
 "sections": [
  {"title": "Definition", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Brain\u2019s ability to rewire itself with experience.", "Learning a hard skill physically changes brain structure."]},
   {"type": "example", "label": "Example", "items": ["Cab drivers memorizing streets grow bigger hippocampi."]}]},
  {"title": "Hebb\u2019s Rule", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Neurons that fire together wire together.", "Repeated co-activation strengthens synapses (LTP)."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Fire together", "Wire together", "Stronger"], "height": 120}]},
  {"title": "Reallocation", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Lost sense \u2192 brain reassigns the area.", "Brain hates wasted space."]},
   {"type": "example", "label": "Example", "items": ["Blind readers use visual cortex to read Braille."]}]},
  {"title": "Stroke Recovery", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Surviving neurons sprout new connections.", "Neighboring areas adopt lost functions."]},
   {"type": "example", "label": "Example", "items": ["Intensive therapy helps patients regain speech."]}]},
  {"title": "Enriched Brains", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Toys, exercise, social contact build thicker cortex.", "Practice reshapes matching brain areas."]},
   {"type": "example", "label": "Example", "items": ["Violinists: enlarged brain areas for left-hand fingers."]}]},
  {"title": "Limits", "color": "red", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Critical periods: vision, language windows narrow.", "Adult plasticity is slower \u2014 but real."]},
   {"type": "example", "label": "Example", "items": ["Phantom limb: cortex remaps after amputation."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Use it or lose it \u2014 literally."]}]},
 ],
 "footer": ["Hebb's rule", "LTP", "Stroke recovery", "Critical periods", "Phantom limb"],
})

# ---------------- 9. Split-Brain Research ----------------
SPECS.append({
 "title": "Split-Brain Research", "subtitle": "Chapter 9 \u2013 Two Halves, Two Minds",
 "sections": [
  {"title": "The Surgery", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Corpus callosum cut to treat severe epilepsy (1960s).", "Bridge between hemispheres severed \u2014 Sperry, Gazzaniga."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Nobel Prize 1981 \u2192 Roger Sperry."]}]},
  {"title": "Left Hemisphere", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Language, logic, analysis (in right-handers).", "Names pictures shown to the right visual field easily."]}]},
  {"title": "Right Hemisphere", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Spatial skills, faces, music, emotional tone.", "Cannot name objects \u2014 but left hand can pick them."]},
   {"type": "diagram", "diagram": "brain", "labels": [], "height": 120}]},
  {"title": "The Interpreter", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Left brain invents stories for right-brain actions.", "Creates explanations even for unknown causes."]},
   {"type": "example", "label": "Example", "items": ["Like a press secretary making up stories."]}]},
  {"title": "Daily Life", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Patients seem almost normal outside the lab.", "Each hemisphere adapts and finds workarounds."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Consciousness is not perfectly unified."]}]},
  {"title": "Myth Busting", "color": "red", "blocks": [
   {"type": "def", "label": "Definition", "items": ["\u2018Left logical / right creative\u2019 types oversimplified.", "200 million fibers: both sides collaborate constantly."]}]},
 ],
 "footer": ["Corpus callosum", "Left = language", "Right = spatial", "The interpreter", "Sperry Nobel 1981"],
})

# ---------------- 10. Brain Development ----------------
SPECS.append({
 "title": "Brain Development", "subtitle": "Chapter 10 \u2013 Building a Brain",
 "sections": [
  {"title": "Construction", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Neural tube \u2192 neuron birth, migration, connection.", "Mostly complete before birth."]},
   {"type": "example", "label": "Example", "items": ["At peak: ~250,000 new neurons per minute."]}]},
  {"title": "Pruning", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Up to 50% of neurons die (apoptosis).", "Not damage \u2014 sculpting weak connections away."]},
   {"type": "example", "label": "Example", "items": ["Teen gray-matter loss = streamlining, not shrinking."]}]},
  {"title": "Myelination", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Continues into the mid-20s.", "Prefrontal cortex finishes last \u2192 teen impulsivity."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Birth", "Pruning", "Myelination"], "height": 120}]},
  {"title": "Sensitive Periods", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Windows when the brain must receive input.", "Vision and language need early stimulation."]},
   {"type": "example", "label": "Example", "items": ["Cataracts must be removed within months of birth."]}]},
  {"title": "Vulnerability", "color": "red", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Alcohol, drugs, malnutrition, severe stress harm it.", "Damage during pregnancy can last a lifetime."]},
   {"type": "example", "label": "Example", "items": ["Fetal alcohol syndrome is preventable brain damage."]}]},
  {"title": "Hope", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Early rescue can reverse much neglect damage.", "Adult neurogenesis continues in the hippocampus."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Timing matters most in development."]}]},
 ],
 "footer": ["Pruning", "Myelination", "Sensitive periods", "Prefrontal last", "Fetal alcohol syndrome"],
})

# ---------------- 11. Twin and Adoption Studies ----------------
SPECS.append({
 "title": "Twin and Adoption Studies", "subtitle": "Chapter 11 \u2013 Nature vs Nurture Tested",
 "sections": [
  {"title": "Twin Design", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["MZ (identical): 100% shared genes.", "DZ (fraternal): ~50% shared genes, like siblings."]},
   {"type": "diagram", "diagram": "bars", "labels": ["MZ 100%", "DZ 50%"], "height": 130}]},
  {"title": "Minnesota Study", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Identical twins raised in different families.", "Showed striking similarities in personality, habits."]},
   {"type": "example", "label": "Example", "items": ["Separated twins with eerily similar tastes."]}]},
  {"title": "Heritability Numbers", "color": "purple", "blocks": [
   {"type": "points", "label": "Key Points", "items": ["Intelligence: roughly 50\u201380%.", "Personality traits: roughly 40\u201350%.", "Schizophrenia risk: strongly genetic."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Heritability = population variation, not personal recipe."]}]},
  {"title": "Adoption Studies", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Children raised by non-relatives studied.", "Traits match biological relatives more with age."]},
   {"type": "example", "label": "Example", "items": ["Adoptee IQ resembles biological parents as they grow."]}]},
  {"title": "Environment Types", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Shared family environment: modest personality effect.", "Non-shared (friends, experiences) matters more."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Same home \u2260 same personality."]}]},
  {"title": "Gene-Environment", "color": "pink", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Correlation: genes steer chosen environments.", "Interaction: same gene, different outcome by home."]},
   {"type": "example", "label": "Example", "items": ["Risk gene + loving home \u2192 child thrives."]}]},
 ],
 "footer": ["MZ vs DZ twins", "Minnesota study", "Heritability", "Adoption studies", "Gene-environment"],
})

# ---------------- 12. The Endocrine System ----------------
SPECS.append({
 "title": "The Endocrine System", "subtitle": "Chapter 12 \u2013 Chemical Messengers",
 "sections": [
  {"title": "Overview", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Glands release hormones into the bloodstream.", "Slower than nerves, but longer-lasting messages."]},
   {"type": "example", "label": "Example", "items": ["Hormones = slow mail; nerves = express delivery."]}]},
  {"title": "Command Axis", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Hypothalamus tells the pituitary what to release.", "Pituitary (master gland) directs other glands."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Hypothalamus", "Pituitary", "Glands"], "height": 120}]},
  {"title": "Thyroid", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Sets the body\u2019s metabolic speed.", "Low \u2192 fatigue, depression-like; high \u2192 anxiety-like."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Low thyroid often mistaken for depression."]}]},
  {"title": "Adrenals", "color": "red", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Medulla \u2192 adrenaline (fast fight-or-flight).", "Cortex \u2192 cortisol (sustained stress)."]},
   {"type": "example", "label": "Example", "items": ["Sit atop the kidneys, ready for emergencies."]}]},
  {"title": "Pancreas", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Insulin lowers blood sugar; glucagon raises it.", "Low sugar \u2192 shaky, irritable, foggy thinking."]},
   {"type": "example", "label": "Example", "items": ["Skipping meals \u2192 irritable and unfocused."]}]},
  {"title": "Pineal + Gonads", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Pineal \u2192 melatonin in darkness (screens disrupt it).", "Gonads \u2192 sex hormones driving puberty."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Darkness \u2192 melatonin \u2192 sleepiness."]}]},
 ],
 "footer": ["Pituitary master gland", "Thyroid", "Adrenals", "Insulin", "Melatonin"],
})

# ---------------- 13. Hormones and Behavior ----------------
SPECS.append({
 "title": "Hormones and Behavior", "subtitle": "Chapter 13 \u2013 Chemistry of Action",
 "sections": [
  {"title": "Cortisol", "color": "red", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Main stress hormone from the adrenal cortex.", "Short burst = energy; chronic = hippocampus damage."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Stress", "Cortisol", "Energy"], "height": 120},
   {"type": "example", "label": "Example", "items": ["Exam week stress helps; exam year stress harms."]}]},
  {"title": "Testosterone", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Linked to competitiveness and aggression.", "Bidirectional: winning raises testosterone too."]},
   {"type": "example", "label": "Example", "items": ["Victory makes the next challenge feel winnable."]}]},
  {"title": "Oxytocin", "color": "pink", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Trust, bonding, social connection.", "Childbirth, nursing, hugging release it."]},
   {"type": "example", "label": "Example", "items": ["Mother\u2019s oxytocin surges at birth \u2192 bonding."]}]},
  {"title": "Estrogen + Progesterone", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Fluctuate across the menstrual cycle.", "Affect mood, energy, and cognition."]},
   {"type": "example", "label": "Example", "items": ["PMDD: severe premenstrual mood symptoms."]}]},
  {"title": "Adrenaline", "color": "yellow", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Instant fight-or-flight from adrenal medulla.", "Heart pounds, airways open, blood \u2192 muscles."]},
   {"type": "example", "label": "Example", "items": ["Mother lifting a car to save her child."]}]},
  {"title": "Two Effect Types", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Organizational: permanent, during development.", "Activational: temporary, in the moment."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Low thyroid = fake depression; fix thyroid, lift mood."]}]},
 ],
 "footer": ["Cortisol", "Testosterone", "Oxytocin", "Adrenaline", "Thyroid & mood"],
})

# ---------------- 14. Hunger and Eating Regulation ----------------
SPECS.append({
 "title": "Hunger and Eating Regulation", "subtitle": "Chapter 14 \u2013 Why We Eat",
 "sections": [
  {"title": "Hypothalamus Switches", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Lateral hypothalamus = hunger ON switch.", "Ventromedial hypothalamus = OFF switch."]},
   {"type": "example", "label": "Example", "items": ["Lesion rats: one group starves, another overeats."]}]},
  {"title": "Ghrelin vs Leptin", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Ghrelin (empty stomach) \u2192 hunger signal.", "Leptin (fat cells) \u2192 fullness signal."]},
   {"type": "diagram", "diagram": "scale", "labels": ["Ghrelin", "Leptin"], "height": 130}]},
  {"title": "Leptin Resistance", "color": "red", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Brain stops responding to leptin in obesity.", "Result: persistent hunger despite ample fat."]},
   {"type": "revision", "label": "Instant Revision", "items": ["High leptin + ignored = still hungry."]}]},
  {"title": "Set-Point Theory", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Body defends a weight range.", "Dieting \u2192 slower metabolism + more ghrelin."]},
   {"type": "example", "label": "Example", "items": ["Dieters regain: biology fights weight loss."]}]},
  {"title": "External Cues", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Sights and smells trigger appetite early.", "Cephalic phase: brain prepares before first bite."]},
   {"type": "example", "label": "Example", "items": ["Fresh bread smell \u2192 hungry even after a meal."]}]},
  {"title": "Eating Disorders", "color": "pink", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Hypothalamus + dopamine + genetics + culture.", "Anorexia and binge eating both have biological roots."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Eating disorders = biology + psychology."]}]},
 ],
 "footer": ["Hypothalamus switches", "Ghrelin vs leptin", "Set-point theory", "Leptin resistance"],
})

# ---------------- 15. Sleep Neuroscience ----------------
SPECS.append({
 "title": "Sleep Neuroscience", "subtitle": "Chapter 15 \u2013 The Sleeping Brain",
 "sections": [
  {"title": "Master Clock", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["SCN in hypothalamus runs ~24-hour rhythm.", "Light hitting the retina resets the clock."]},
   {"type": "example", "label": "Example", "items": ["Jet lag = your SCN still on home time."]}]},
  {"title": "Melatonin", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Signals darkness to the body.", "Blue light from screens suppresses it."]},
   {"type": "example", "label": "Example", "items": ["Late-night scrolling pushes sleep later."]}]},
  {"title": "Sleep Stages", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": ["N1 (drifting) \u2192 N2 (light) \u2192 N3 (deep) \u2192 REM.", "~90-minute cycles, 4\u20136 per night."]},
   {"type": "diagram", "diagram": "flow", "labels": ["N1", "N2", "N3", "REM"], "height": 120}]},
  {"title": "REM Sleep", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Brain wildly active, muscles paralyzed (atonia).", "Vivid dreaming happens here."]},
   {"type": "example", "label": "Example", "items": ["Paralysis stops you acting out dreams."]}]},
  {"title": "Deep Sleep", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["N3: tissues repair, growth hormone releases.", "Immune system strengthens; memories consolidate."]},
   {"type": "example", "label": "Example", "items": ["Study \u2192 sleep \u2192 remember more."]}]},
  {"title": "Deprivation", "color": "red", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Adenosine builds \u2192 sleepiness; caffeine blocks it.", "24 hours awake \u2248 legally drunk judgment."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Prefrontal cortex fails first without sleep."]}]},
 ],
 "footer": ["SCN clock", "Melatonin", "Sleep stages", "REM atonia", "Adenosine"],
})

# ---------------- 16. Emotion and the Brain ----------------
SPECS.append({
 "title": "Emotion and the Brain", "subtitle": "Chapter 16 \u2013 Where Feelings Live",
 "sections": [
  {"title": "The Low Road", "color": "red", "blocks": [
   {"type": "def", "label": "Definition", "items": ["LeDoux: threat \u2192 amygdala before cortex.", "We feel fear before we know why."]},
   {"type": "example", "label": "Example", "items": ["Duck at a car backfire \u2014 then realize it\u2019s harmless."]}]},
  {"title": "Top-Down Control", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Prefrontal cortex inhibits the amygdala.", "Mindfulness training strengthens this control."]},
   {"type": "diagram", "diagram": "flow", "labels": ["Threat", "Amygdala", "Prefrontal calms"], "height": 120}]},
  {"title": "James-Lange Theory", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Emotions follow bodily changes.", "We don\u2019t cry because sad \u2014 sad because we cry."]},
   {"type": "example", "label": "Example", "items": ["Trembling comes first; feeling afraid follows."]}]},
  {"title": "Cannon-Bard Theory", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Feeling + bodily arousal happen together.", "Thalamic signals split to both at once."]},
   {"type": "revision", "label": "Instant Revision", "items": ["James-Lange = body first; Cannon-Bard = together."]}]},
  {"title": "Schachter-Singer", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Two-factor: arousal + label = emotion.", "Same racing heart \u2192 excitement or anger by context."]},
   {"type": "example", "label": "Example", "items": ["Aroused people felt happy or angry by situation."]}]},
  {"title": "Brain Sides", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Left prefrontal = approach, positive emotion.", "Right prefrontal = withdrawal, negative emotion."]},
   {"type": "example", "label": "Example", "items": ["Forcing a smile can slightly lift your mood."]}]},
 ],
 "footer": ["Low road", "James-Lange", "Cannon-Bard", "Schachter-Singer", "Left vs right frontal"],
})

# ---------------- 17. Memory and the Brain ----------------
SPECS.append({
 "title": "Memory and the Brain", "subtitle": "Chapter 17 \u2013 How the Brain Stores",
 "sections": [
  {"title": "Hippocampus", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Forms new explicit (declarative) memories.", "H.M.\u2019s surgery: formation \u2260 storage."]},
   {"type": "example", "label": "Example", "items": ["H.M. learned skills but forgot practicing them."]}]},
  {"title": "Amygdala Stamp", "color": "red", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Attaches emotion \u2192 stronger consolidation.", "Emotional events become flashbulb memories."]},
   {"type": "example", "label": "Example", "items": ["You remember exactly where you were in a crisis."]}]},
  {"title": "Skill Memory", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Cerebellum: timing and coordination.", "Basal ganglia: habits. Both = implicit memory."]},
   {"type": "example", "label": "Example", "items": ["Ride a bike years later without thinking."]}]},
  {"title": "Working Memory", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Prefrontal cortex holds ~4 chunks briefly.", "Limited capacity \u2192 multitasking fails."]},
   {"type": "diagram", "diagram": "bars", "labels": ["Sensory", "Working", "Long-term"], "height": 130}]},
  {"title": "LTP", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Long-term potentiation: repeated firing strengthens synapses.", "Glutamate receptors; Hebb\u2019s rule in molecules."]},
   {"type": "revision", "label": "Instant Revision", "items": ["LTP = molecular basis of memory."]}]},
  {"title": "Sleep Transfer", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Memories move: hippocampus \u2192 cortex during deep sleep.", "Alzheimer\u2019s hits hippocampus first."]},
   {"type": "example", "label": "Example", "items": ["All-nighters sabotage memory transfer."]}]},
 ],
 "footer": ["Hippocampus", "Amygdala", "LTP", "Working memory", "H.M.", "Alzheimer's"],
})

# ---------------- 18. Stress Physiology (HPA Axis) ----------------
SPECS.append({
 "title": "Stress Physiology (HPA Axis)", "subtitle": "Chapter 18 \u2013 The Stress Command Chain",
 "sections": [
  {"title": "The HPA Chain", "color": "red", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Hypothalamus releases CRH.", "Pituitary releases ACTH \u2192 adrenal cortex releases cortisol."]},
   {"type": "diagram", "diagram": "flow", "labels": ["CRH", "ACTH", "Cortisol"], "height": 120}]},
  {"title": "Selye\u2019s Stages", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Alarm: fight-or-flight activation.", "Resistance: coping while resources drain.", "Exhaustion: resources depleted \u2192 illness."]},
   {"type": "example", "label": "Example", "items": ["Stressed rats: alarm, resistance, then collapse."]}]},
  {"title": "Acute vs Chronic", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Acute cortisol: adaptive energy and alertness.", "Chronic: hippocampus shrinks, amygdala grows."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Short stress helps; long stress harms."]}]},
  {"title": "Tend-and-Befriend", "color": "pink", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Taylor: beyond fight-or-flight.", "Oxytocin drives bonding under stress."]},
   {"type": "example", "label": "Example", "items": ["Under stress many nurture and affiliate \u2014 especially women."]}]},
  {"title": "Control Matters", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Uncontrollable stress = worst HPA damage.", "Perceived control powerfully protects."]},
   {"type": "example", "label": "Example", "items": ["Same deadline: in-control person, smaller cortisol spike."]}]},
  {"title": "Daily Rhythm", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Healthy: morning peak, evening trough.", "Flat rhythm = burnout or shift-work dysregulation."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Allostatic load = wear and tear of stress."]}]},
 ],
 "footer": ["HPA axis", "Selye's stages", "Cortisol", "Tend-and-befriend", "Allostatic load"],
})

# ---------------- 19. Brain Imaging Techniques ----------------
SPECS.append({
 "title": "Brain Imaging Techniques", "subtitle": "Chapter 19 \u2013 Seeing the Living Brain",
 "sections": [
  {"title": "EEG", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Scalp electrodes measure electrical activity.", "Superb timing (milliseconds), blurry location."]},
   {"type": "example", "label": "Example", "items": ["Go-to for sleep stages and seizure tracking."]}]},
  {"title": "CT Scan", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["X-ray slices stacked into a 3D image.", "Fast, great for trauma \u2014 but uses radiation."]},
   {"type": "example", "label": "Example", "items": ["Emergency brain bleeding imaged in minutes."]}]},
  {"title": "MRI", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Magnets align atoms \u2192 exquisite detail.", "No radiation; loud, slow, expensive."]},
   {"type": "diagram", "diagram": "bars", "labels": ["EEG fast", "MRI sharp", "PET chemical"], "height": 130}]},
  {"title": "fMRI", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Blood oxygen (BOLD) shows active regions.", "Slow (seconds), correlational \u2014 blobs oversimplify."]},
   {"type": "revision", "label": "Instant Revision", "items": ["fMRI = where, not exactly why."]}]},
  {"title": "PET", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Radioactive tracers map chemistry live.", "Glucose use, dopamine receptors \u2014 unique but invasive."]}]},
  {"title": "TMS + Lesions", "color": "red", "blocks": [
   {"type": "def", "label": "Definition", "items": ["TMS: magnetic pulses test if an area is necessary.", "Lesions: Gage and H.M. founded neuropsychology."]},
   {"type": "revision", "label": "Instant Revision", "items": ["No scan reads minds \u2014 every method trades off."]}]},
 ],
 "footer": ["EEG", "CT", "MRI", "fMRI", "PET", "TMS"],
})

# ---------------- 20. Psychopharmacology Basics ----------------
SPECS.append({
 "title": "Psychopharmacology Basics", "subtitle": "Chapter 20 \u2013 How Brain Drugs Work",
 "sections": [
  {"title": "Agonist vs Antagonist", "color": "blue", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Agonists boost neurotransmitter action.", "Antagonists block it. Nearly every drug is one of these."]},
   {"type": "diagram", "diagram": "scale", "labels": ["Agonist +", "Antagonist \u2212"], "height": 130},
   {"type": "example", "label": "Example", "items": ["Caffeine blocks adenosine receptors."]}]},
  {"title": "SSRIs", "color": "teal", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Serotonin rises immediately in synapses.", "Mood lifts in 2\u20136 weeks via receptor changes."]},
   {"type": "revision", "label": "Instant Revision", "items": ["Delay = adaptation, not dose."]}]},
  {"title": "Antipsychotics", "color": "purple", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Block D2 receptors \u2192 fewer hallucinations.", "Older drugs \u2192 Parkinson-like stiffness side effects."]}]},
  {"title": "Benzodiazepines", "color": "green", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Amplify GABA \u2192 rapid calm and sedation.", "Tolerance builds in weeks \u2014 short-term tools only."]},
   {"type": "example", "label": "Example", "items": ["Valium for panic: fast, but dependence risk."]}]},
  {"title": "Stimulants", "color": "orange", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Raise dopamine + norepinephrine.", "Paradoxical calm in ADHD via better control circuits."]},
   {"type": "example", "label": "Example", "items": ["Hyperactive child focuses after stimulant dose."]}]},
  {"title": "Tolerance & Placebo", "color": "red", "blocks": [
   {"type": "def", "label": "Definition", "items": ["Tolerance: brain adapts \u2192 needs more drug.", "Withdrawal: stopping unmasks the adaptation."]},
   {"type": "example", "label": "Example", "items": ["Placebo painkillers trigger real endorphin release."]}]},
 ],
 "footer": ["Agonist vs antagonist", "SSRIs", "Antipsychotics", "Benzodiazepines", "Tolerance"],
})

assert len(SPECS) == 20, f"expected 20 specs, got {len(SPECS)}"

if __name__ == "__main__":
    outdir = "/home/hatch/workspace/zehen/batch4/inf-cheat-bio-out"
    os.makedirs(outdir, exist_ok=True)
    for i, spec in enumerate(SPECS, 1):
        out = os.path.join(outdir, f"bio-{i}.png")
        render_cheatsheet(spec, out)
        print(f"rendered {i}/20: {spec['title']}")
