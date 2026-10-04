/* Mysterious — Category Challenge: 3 game modes x 10 psychology categories.
   Content is in simple English with examples, matching the site's study style. */
(function(){
"use strict";

var CATG = {
"Biological": {
  terms: [
    ["Neuron", "A nerve cell that carries messages through the nervous system"],
    ["Synapse", "The tiny gap where one neuron passes a message to the next"],
    ["Neurotransmitter", "A chemical messenger that carries signals between neurons"],
    ["Amygdala", "The brain's alarm centre for fear and emotion"],
    ["Hippocampus", "The brain area that helps form new memories"],
    ["Endorphins", "Natural feel-good chemicals that reduce pain"]
  ],
  odd: [
    { items: ["Neuron", "Synapse", "Neurotransmitter", "Superego"], odd: 3, why: "Superego is Freud's idea about conscience — the rest are parts of the nervous system." },
    { items: ["Dopamine", "Serotonin", "Endorphins", "Classical conditioning"], odd: 3, why: "Classical conditioning is a learning process — the rest are brain chemicals." },
    { items: ["Cerebellum", "Hippocampus", "Amygdala", "Id"], odd: 3, why: "Id is a psychoanalytic term — the rest are real brain structures." },
    { items: ["Adrenaline", "Cortisol", "Insulin", "Reinforcement"], odd: 3, why: "Reinforcement is a behavioural concept — the rest are hormones." },
    { items: ["Dendrites", "Axon", "Myelin sheath", "Defence mechanism"], odd: 3, why: "Defence mechanisms are mental strategies — the rest are parts of a neuron." }
  ],
  scenarios: [
    { q: "Ali touches a hot pan and pulls his hand back instantly, before he even feels pain. What explains this?",
      options: ["A reflex arc through the spinal cord", "Classical conditioning", "Observational learning", "Cognitive dissonance"], answer: 0,
      explain: "Reflexes travel to the spinal cord and back — no waiting for the brain, so the reaction is instant." },
    { q: "Sara feels calm and happy after a long run. Which brain chemicals are most likely behind this?",
      options: ["Endorphins", "Stomach acid", "Insulin", "Adrenaline only"], answer: 0,
      explain: "Exercise releases endorphins — natural chemicals that lift mood and reduce pain." },
    { q: "After an accident, Ahmed cannot form new memories but remembers his childhood clearly. Which brain area is likely damaged?",
      options: ["The hippocampus", "The cerebellum", "The occipital lobe", "The medulla"], answer: 0,
      explain: "The hippocampus helps form new memories — damage causes anterograde amnesia." },
    { q: "During exams, Hira's heart races and her palms sweat. Which system is activated?",
      options: ["Sympathetic nervous system", "Digestive system", "Immune system", "Skeletal system"], answer: 0,
      explain: "The sympathetic nervous system triggers fight-or-flight: fast heartbeat, sweating, alertness." },
    { q: "A drug blocks dopamine receptors. Which effect is most likely?",
      options: ["Reduced feelings of reward and pleasure", "Sharper eyesight", "Stronger bones", "Faster hair growth"], answer: 0,
      explain: "Dopamine drives reward and motivation — blocking it dulls pleasure." },
    { q: "Fatima has a stroke affecting her left frontal lobe. Which ability is most at risk?",
      options: ["Speaking and planning", "Hearing music", "Seeing colours", "Tasting food"], answer: 0,
      explain: "The left frontal lobe handles speech production and planning — Broca's area lives there." }
  ]
},
"Clinical": {
  terms: [
    ["DSM-5-TR", "The manual psychologists use to diagnose mental disorders"],
    ["Anxiety disorder", "A condition with intense, lasting fear or worry"],
    ["Depression", "A mood disorder with deep sadness and loss of interest"],
    ["CBT", "Therapy that changes unhelpful thoughts and behaviours"],
    ["Phobia", "An extreme, irrational fear of something specific"],
    ["Schizophrenia", "A disorder with delusions, hallucinations and confused thinking"]
  ],
  odd: [
    { items: ["Depression", "Anxiety", "Schizophrenia", "Reinforcement"], odd: 3, why: "Reinforcement is a learning concept — the rest are mental disorders." },
    { items: ["Hallucination", "Delusion", "Disorganised speech", "Working memory"], odd: 3, why: "Working memory is a cognitive function — the rest are psychotic symptoms." },
    { items: ["SSRI", "CBT", "Exposure therapy", "Placebo effect"], odd: 3, why: "The placebo effect is a research phenomenon — the rest are treatments." },
    { items: ["Panic attack", "Compulsion", "Obsession", "Synapse"], odd: 3, why: "A synapse is a neural gap — the rest relate to anxiety and OCD." },
    { items: ["Anorexia", "Bulimia", "Binge eating", "Homeostasis"], odd: 3, why: "Homeostasis is body balance — the rest are eating disorders." }
  ],
  scenarios: [
    { q: "Danish washes his hands 40 times a day fearing germs will harm his family. Which disorder fits best?",
      options: ["Obsessive-compulsive disorder", "Dissociative amnesia", "Narcolepsy", "Dyslexia"], answer: 0,
      explain: "Repeated washing (compulsion) driven by fearful thoughts (obsession) = OCD." },
    { q: "Ayesha hears voices commenting on her actions, though no one is there. What is she experiencing?",
      options: ["Auditory hallucinations", "A flashback", "Déjà vu", "A panic attack"], answer: 0,
      explain: "Hearing things others don't hear is an auditory hallucination, common in schizophrenia." },
    { q: "Bilal avoids all gatherings fearing embarrassment. What is the best first-line therapy?",
      options: ["CBT with gradual exposure", "Brain surgery", "Hypnosis alone", "Dream analysis only"], answer: 0,
      explain: "CBT plus gradual exposure is the best-supported treatment for social anxiety." },
    { q: "Mahnoor has felt hopeless for months, sleeps 12 hours a day and quit her hobbies. What should happen first?",
      options: ["A professional assessment for depression", "Telling her to stay positive", "Ignoring it until it passes", "Changing her diet only"], answer: 0,
      explain: "Lasting hopelessness plus lost interest needs a professional depression assessment." },
    { q: "A therapist has a client face feared situations step by step, easiest first. What is this?",
      options: ["Systematic desensitisation", "Free association", "Aversion therapy", "Dream analysis"], answer: 0,
      explain: "Gradual, ranked exposure to fears is systematic desensitisation." },
    { q: "Usman believes the TV sends him secret messages. What is this symptom called?",
      options: ["A delusion of reference", "A compulsion", "Selective attention", "A flashback"], answer: 0,
      explain: "Believing neutral events refer specially to you is a delusion of reference." }
  ]
},
"Cognitive": {
  terms: [
    ["Working memory", "The mental workspace that holds and uses information briefly"],
    ["Cognitive bias", "A systematic error in thinking or judging"],
    ["Schema", "A mental framework that organises what we know"],
    ["Attention", "Focusing mental effort on one thing while ignoring others"],
    ["Heuristic", "A mental shortcut for quick decisions"],
    ["Metacognition", "Thinking about your own thinking"]
  ],
  odd: [
    { items: ["Confirmation bias", "Hindsight bias", "Anchoring", "Classical conditioning"], odd: 3, why: "Classical conditioning is learning by association — the rest are thinking biases." },
    { items: ["Schema", "Heuristic", "Algorithm", "Reflex"], odd: 3, why: "A reflex is automatic and biological — the rest are cognitive strategies." },
    { items: ["Selective attention", "Divided attention", "Sustained attention", "Systematic desensitisation"], odd: 3, why: "Systematic desensitisation is a therapy — the rest are types of attention." },
    { items: ["Encoding", "Storage", "Retrieval", "Extinction"], odd: 3, why: "Extinction is unlearning a conditioned response — the rest are memory stages." },
    { items: ["Prototype", "Concept", "Schema", "Neurotransmitter"], odd: 3, why: "A neurotransmitter is a brain chemical — the rest are mental categories." }
  ],
  scenarios: [
    { q: "Rabia only reads news that agrees with her views and ignores the rest. Which bias is this?",
      options: ["Confirmation bias", "Hindsight bias", "Anchoring bias", "Framing effect"], answer: 0,
      explain: "Seeking only confirming information is confirmation bias." },
    { q: "After the match, Kamran says 'I knew we would win all along.' Which bias?",
      options: ["Hindsight bias", "Confirmation bias", "Self-serving bias", "Anchoring"], answer: 0,
      explain: "'I knew it all along' after the fact is hindsight bias." },
    { q: "A shirt is priced Rs. 5,000 then 'discounted' to Rs. 2,500. You feel it's a bargain because of the first price. What is this?",
      options: ["Anchoring", "Priming", "Chunking", "Rehearsal"], answer: 0,
      explain: "The first number anchors your judgement — everything after feels cheap." },
    { q: "Zain studies while texting and his grades drop. Which attention problem is this?",
      options: ["Divided attention overload", "Selective attention", "Sustained attention", "Vigilance"], answer: 0,
      explain: "Splitting attention overloads working memory — multitasking hurts learning." },
    { q: "Sana can't find her keys because she never 'encoded' where she put them. Which memory stage failed?",
      options: ["Encoding", "Retrieval", "Storage", "Rehearsal"], answer: 0,
      explain: "If you never paid attention, the memory was never encoded — you can't retrieve what was never stored." },
    { q: "After hearing of a plane crash, Tariq fears flying though driving is riskier. Which heuristic?",
      options: ["Availability heuristic", "Representativeness heuristic", "Anchoring", "Algorithm"], answer: 0,
      explain: "Vivid, easy-to-recall events feel more likely — the availability heuristic." }
  ]
},
"Counseling & Therapy": {
  terms: [
    ["Active listening", "Fully focusing on a client to understand their message"],
    ["Empathy", "Understanding and sharing another person's feelings"],
    ["Unconditional positive regard", "Accepting a client without judgement (Rogers)"],
    ["Confidentiality", "Keeping what clients share private"],
    ["Transference", "When a client redirects feelings onto the therapist"],
    ["Therapeutic alliance", "The trusting bond between therapist and client"]
  ],
  odd: [
    { items: ["Empathy", "Active listening", "Reflection", "Systematic desensitisation"], odd: 3, why: "Systematic desensitisation is a behaviour technique — the rest are counselling microskills." },
    { items: ["Confidentiality", "Informed consent", "Boundaries", "Confirmation bias"], odd: 3, why: "Confirmation bias is a thinking error — the rest are therapy ethics." },
    { items: ["Transference", "Countertransference", "Resistance", "Neurotransmitter"], odd: 3, why: "A neurotransmitter is a brain chemical — the rest happen in the therapy relationship." },
    { items: ["Person-centred therapy", "Gestalt therapy", "CBT", "Placebo"], odd: 3, why: "Placebo is a research effect — the rest are therapy approaches." },
    { items: ["Open question", "Closed question", "Paraphrasing", "Punishment"], odd: 3, why: "Punishment is a behaviour technique — the rest are counselling skills." }
  ],
  scenarios: [
    { q: "A client says 'Nobody understands me.' The counsellor replies, 'You feel alone and unheard.' What skill is this?",
      options: ["Reflection of feeling", "Advice giving", "Diagnosis", "Confrontation"], answer: 0,
      explain: "Mirroring the client's emotion back is reflection of feeling." },
    { q: "In therapy, Ahmed starts treating his therapist like his strict father. What is happening?",
      options: ["Transference", "Resistance", "Empathy", "Burnout"], answer: 0,
      explain: "Redirecting feelings for someone else onto the therapist is transference." },
    { q: "A counsellor must break confidentiality when…",
      options: ["A client plans serious harm to someone", "A client admits cheating on a test", "A client cries in session", "A client misses an appointment"], answer: 0,
      explain: "Safety overrides privacy — planned serious harm must be reported." },
    { q: "Which question is an open question?",
      options: ["'What has been weighing on you lately?'", "'Are you sad?'", "'Do you sleep 8 hours?'", "'Is your mother alive?'"], answer: 0,
      explain: "Open questions invite long answers — closed ones get yes/no." },
    { q: "A therapist accepts a rude, angry client warmly without judging. This is…",
      options: ["Unconditional positive regard", "Countertransference", "Collusion", "Avoidance"], answer: 0,
      explain: "Rogers' unconditional positive regard means accepting the client as they are." },
    { q: "The strongest predictor of therapy success is…",
      options: ["A strong therapeutic alliance", "The therapist's degree brand", "Expensive office furniture", "Very long sessions"], answer: 0,
      explain: "Research shows the trusting therapist–client bond predicts outcomes best." }
  ]
},
"Developmental": {
  terms: [
    ["Attachment", "The deep emotional bond between child and caregiver"],
    ["Object permanence", "Knowing things exist even when unseen (Piaget)"],
    ["Egocentrism", "A young child's inability to see others' viewpoints"],
    ["Puberty", "The body changes that bring reproductive maturity"],
    ["Theory of mind", "Understanding that others have their own thoughts"],
    ["Temperament", "A baby's inborn style of reacting to the world"]
  ],
  odd: [
    { items: ["Attachment", "Temperament", "Imprinting", "Classical conditioning"], odd: 3, why: "Classical conditioning is a learning process — the rest shape early development." },
    { items: ["Egocentrism", "Object permanence", "Conservation", "Neurotransmitter"], odd: 3, why: "A neurotransmitter is a brain chemical — the rest are Piagetian concepts." },
    { items: ["Puberty", "Menopause", "Adolescence", "Synapse"], odd: 3, why: "A synapse is a neural gap — the rest are life stages or changes." },
    { items: ["Teratogen", "Placenta", "Zygote", "Heuristic"], odd: 3, why: "A heuristic is a thinking shortcut — the rest relate to prenatal development." },
    { items: ["Theory of mind", "Joint attention", "Stranger anxiety", "Reinforcement"], odd: 3, why: "Reinforcement is a learning concept — the rest are developmental milestones." }
  ],
  scenarios: [
    { q: "An 8-month-old cries when her mother leaves the room. This is…",
      options: ["Separation anxiety — normal at this age", "A sign of bad parenting", "An attachment disorder", "A learning disability"], answer: 0,
      explain: "Separation anxiety peaks around 8–14 months and is a healthy sign of attachment." },
    { q: "In the Strange Situation, a baby explores happily and is comforted quickly on reunion. Attachment style?",
      options: ["Secure", "Avoidant", "Ambivalent", "Disorganised"], answer: 0,
      explain: "Easy exploration + quick comfort = secure attachment (Ainsworth)." },
    { q: "A 4-year-old insists the moon follows her car. This shows…",
      options: ["Egocentrism", "Object permanence", "Conservation", "Abstract thinking"], answer: 0,
      explain: "Preoperational children see the world only from their viewpoint — egocentrism." },
    { q: "Which of these is a teratogen?",
      options: ["Alcohol during pregnancy", "Folic acid", "Gentle music", "Reading aloud"], answer: 0,
      explain: "Alcohol harms the developing foetus — a classic teratogen." },
    { q: "A teen argues passionately about justice and hypothetical futures. Which Piaget stage?",
      options: ["Formal operational", "Sensorimotor", "Preoperational", "Concrete operational"], answer: 0,
      explain: "Abstract, hypothetical reasoning marks the formal operational stage (around 11+)." },
    { q: "Erikson's crisis of the teen years is…",
      options: ["Identity vs. role confusion", "Trust vs. mistrust", "Integrity vs. despair", "Industry vs. inferiority"], answer: 0,
      explain: "Teens wrestle with 'who am I?' — identity vs. role confusion." }
  ]
},
"Health": {
  terms: [
    ["Stress", "The body's response to demanding pressures"],
    ["Coping", "Efforts to manage stress and its emotions"],
    ["Placebo effect", "Feeling better because you believe a treatment works"],
    ["Burnout", "Exhaustion from long-term stress, often at work"],
    ["Eustress", "Positive, motivating stress — like pre-match excitement"],
    ["Adherence", "Following medical advice and treatment properly"]
  ],
  odd: [
    { items: ["Stress", "Coping", "Appraisal", "Classical conditioning"], odd: 3, why: "Classical conditioning is learning by association — the rest are stress concepts." },
    { items: ["Placebo effect", "Nocebo effect", "Hawthorne effect", "Neurotransmitter"], odd: 3, why: "A neurotransmitter is a brain chemical — the rest are expectancy effects." },
    { items: ["Burnout", "Compassion fatigue", "Eustress", "Synapse"], odd: 3, why: "A synapse is a neural gap — the rest relate to stress and work." },
    { items: ["Type A personality", "Hostility", "Time urgency", "Schema"], odd: 3, why: "A schema is a mental framework — the rest describe the heart-risk Type A pattern." },
    { items: ["Adherence", "Compliance", "Relapse", "Reinforcement"], odd: 3, why: "Reinforcement is a learning concept — the rest concern following treatment." }
  ],
  scenarios: [
    { q: "Sana's headaches vanish once exams end, though doctors found nothing. Likely…",
      options: ["Stress-related (psychosomatic) symptoms", "A brain tumour", "Food poisoning", "An eye infection"], answer: 0,
      explain: "Stress can create real physical symptoms with no medical cause — psychosomatic." },
    { q: "Which of these is problem-focused coping?",
      options: ["Making a study plan for the exam", "Denying the exam exists", "Drinking to forget", "Blaming the teacher"], answer: 0,
      explain: "Tackling the problem itself (a plan) is problem-focused; the rest avoid it." },
    { q: "In a drug trial, the sugar-pill group also improves. This is…",
      options: ["The placebo effect", "The nocebo effect", "Observer bias", "Random error"], answer: 0,
      explain: "Belief in treatment heals — the placebo effect." },
    { q: "Long job stress leaves Ali exhausted, cynical and detached. This is…",
      options: ["Burnout", "Eustress", "A phobia", "Amnesia"], answer: 0,
      explain: "Exhaustion + cynicism + detachment = burnout." },
    { q: "Per the health belief model, people act when they…",
      options: ["Feel at risk and believe action helps", "Are forced by law only", "Feel no risk at all", "Avoid all information"], answer: 0,
      explain: "Perceived risk + perceived benefit drive health behaviour." },
    { q: "After surgery, patients who feel in control recover faster. This shows…",
      options: ["Perceived control aids healing", "Surgery never works", "Control harms healing", "Hospitals heal by magic"], answer: 0,
      explain: "A sense of control lowers stress hormones and supports recovery." }
  ]
},
"Organizational": {
  terms: [
    ["Job satisfaction", "How content someone feels about their work"],
    ["Leadership", "Guiding and influencing a group toward goals"],
    ["Motivation", "The drive that starts and sustains behaviour"],
    ["Teamwork", "People cooperating to reach a shared goal"],
    ["Organisational culture", "Shared values and norms of a workplace"],
    ["Social loafing", "Working less hard in a group than alone"]
  ],
  odd: [
    { items: ["Transformational leadership", "Transactional leadership", "Laissez-faire", "Classical conditioning"], odd: 3, why: "Classical conditioning is learning by association — the rest are leadership styles." },
    { items: ["Job satisfaction", "Absenteeism", "Turnover", "Synapse"], odd: 3, why: "A synapse is a neural gap — the rest are work outcomes." },
    { items: ["Intrinsic motivation", "Extrinsic motivation", "Self-actualisation", "Neurotransmitter"], odd: 3, why: "A neurotransmitter is a brain chemical — the rest are motivation concepts." },
    { items: ["Hawthorne effect", "Social loafing", "Groupthink", "Placebo"], odd: 3, why: "Placebo is a medical-research effect — the rest happen in work groups." },
    { items: ["Selection", "Training", "Appraisal", "Transference"], odd: 3, why: "Transference happens in therapy — the rest are HR functions." }
  ],
  scenarios: [
    { q: "A manager inspires staff with a bold vision and mentors each person. Which style?",
      options: ["Transformational leadership", "Laissez-faire", "Autocratic", "Transactional"], answer: 0,
      explain: "Inspiring + mentoring + vision = transformational leadership." },
    { q: "In a group project, Daniyal works less hard than when alone. This is…",
      options: ["Social loafing", "Groupthink", "Social facilitation", "Brainstorming"], answer: 0,
      explain: "Reduced effort in groups where contributions blur = social loafing." },
    { q: "A team agrees too quickly and ignores warning signs to stay united. This is…",
      options: ["Groupthink", "Brainstorming", "Synergy", "Active listening"], answer: 0,
      explain: "Pressure for harmony crushing dissent = groupthink (Janis)." },
    { q: "Which boosts intrinsic motivation?",
      options: ["Giving meaningful, autonomous work", "Threatening pay cuts", "Micromanaging every step", "Removing all feedback"], answer: 0,
      explain: "Autonomy and meaning fuel intrinsic motivation — threats kill it." },
    { q: "Workers produce more simply because they know they're observed. This is…",
      options: ["The Hawthorne effect", "The placebo effect", "Operant conditioning", "Learned helplessness"], answer: 0,
      explain: "Being watched changes behaviour — the Hawthorne effect." },
    { q: "The best predictor of job performance in hiring is…",
      options: ["Structured interviews + work samples", "Handwriting analysis", "Zodiac sign", "Unstructured chat"], answer: 0,
      explain: "Research favours structured interviews and work samples over gut feel." }
  ]
},
"Personality": {
  terms: [
    ["Trait", "A lasting pattern of thoughts, feelings and behaviour"],
    ["Extraversion", "Being energised by social interaction"],
    ["Neuroticism", "Tendency toward anxiety and emotional instability"],
    ["Self-esteem", "How much you value yourself"],
    ["Id", "Freud's pleasure-seeking part of personality"],
    ["Big Five", "The five main personality traits (OCEAN)"]
  ],
  odd: [
    { items: ["Openness", "Conscientiousness", "Extraversion", "Classical conditioning"], odd: 3, why: "Classical conditioning is learning — the rest are Big Five traits." },
    { items: ["Id", "Ego", "Superego", "Hippocampus"], odd: 3, why: "The hippocampus is a brain structure — the rest are Freud's personality parts." },
    { items: ["Self-esteem", "Self-efficacy", "Self-actualisation", "Synapse"], odd: 3, why: "A synapse is a neural gap — the rest are 'self' concepts." },
    { items: ["Projective test", "Rorschach", "TAT", "Blood test"], odd: 3, why: "A blood test is medical — the rest are personality assessments." },
    { items: ["Introversion", "Extraversion", "Ambiversion", "Extinction"], odd: 3, why: "Extinction is unlearning — the rest describe social energy styles." }
  ],
  scenarios: [
    { q: "Mahnoor loves parties and feels drained when alone for long. She is likely…",
      options: ["High in extraversion", "High in neuroticism", "Low in openness", "High in psychoticism"], answer: 0,
      explain: "Energy from social contact = extraversion." },
    { q: "In the Big Five, OCEAN stands for…",
      options: ["Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism", "Optimism, Courage, Energy, Action, Nerve", "Order, Control, Ego, Anxiety, Need", "Oral, Creative, Emotional, Active, Nice"], answer: 0,
      explain: "OCEAN = the five broad traits psychologists measure." },
    { q: "A Rorschach inkblot test is an example of…",
      options: ["A projective test", "An IQ test", "A blood test", "A lie detector"], answer: 0,
      explain: "Ambiguous inkblots reveal hidden thoughts — projective testing." },
    { q: "According to Freud, the ego…",
      options: ["Balances the id's desires with reality", "Seeks pleasure instantly", "Holds moral ideals", "Stores memories only"], answer: 0,
      explain: "The ego is the realistic mediator between id and superego." },
    { q: "Someone high in conscientiousness is likely…",
      options: ["Organised and dependable", "Reckless and always late", "Anxious all the time", "Shy and quiet"], answer: 0,
      explain: "Conscientiousness = discipline, planning, reliability." },
    { q: "Believing 'I can handle this exam' reflects…",
      options: ["Self-efficacy", "Self-esteem", "Narcissism", "Egoism"], answer: 0,
      explain: "Bandura's self-efficacy = belief in your ability for a specific task." }
  ]
},
"Research Methods & Statistics": {
  terms: [
    ["Hypothesis", "A testable prediction about what will happen"],
    ["Variable", "Anything that can change or be measured"],
    ["Correlation", "How strongly two things move together"],
    ["Random sampling", "Picking participants by chance, fairly"],
    ["Placebo", "A fake treatment used as a comparison"],
    ["Standard deviation", "How spread out scores are around the average"]
  ],
  odd: [
    { items: ["Independent variable", "Dependent variable", "Confounding variable", "Neurotransmitter"], odd: 3, why: "A neurotransmitter is a brain chemical — the rest are variable types." },
    { items: ["Experiment", "Survey", "Case study", "Transference"], odd: 3, why: "Transference happens in therapy — the rest are research methods." },
    { items: ["Mean", "Median", "Mode", "Placebo"], odd: 3, why: "Placebo is a fake treatment — the rest are averages." },
    { items: ["Reliability", "Validity", "Objectivity", "Reinforcement"], odd: 3, why: "Reinforcement is a learning concept — the rest judge measurement quality." },
    { items: ["Double-blind", "Single-blind", "Open-label", "Open question"], odd: 3, why: "An open question is a counselling skill — the rest are blinding designs." }
  ],
  scenarios: [
    { q: "Ice-cream sales and drownings rise together in summer. The hidden third variable is…",
      options: ["Hot weather", "Sugar", "Swimming skill", "Lifeguards"], answer: 0,
      explain: "Correlation isn't causation — heat drives both." },
    { q: "In an experiment, the variable the researcher changes is the…",
      options: ["Independent variable", "Dependent variable", "Control variable", "Constant"], answer: 0,
      explain: "You manipulate the independent variable and measure the dependent one." },
    { q: "Why do researchers use random assignment?",
      options: ["To spread differences evenly across groups", "To pick only smart participants", "To save money", "To avoid consent forms"], answer: 0,
      explain: "Random assignment balances unknown factors between groups." },
    { q: "A test gives the same result every time you take it. It has…",
      options: ["High reliability", "High validity", "Low ethics", "No practical use"], answer: 0,
      explain: "Consistency = reliability; measuring the right thing = validity." },
    { q: "In a double-blind study…",
      options: ["Neither participants nor researchers know who got what", "Only participants are blindfolded", "Everyone knows everything", "Only the statistician is blind"], answer: 0,
      explain: "Double-blind blocks expectancy effects on both sides." },
    { q: "A p-value of 0.03 means…",
      options: ["Results are statistically significant (p < .05)", "The hypothesis is proven true", "There is a 3% maths error", "The sample was 3 people"], answer: 0,
      explain: "p < .05 is the usual cut-off for significance — not proof, just unlikely by chance." }
  ]
},
"Social": {
  terms: [
    ["Conformity", "Changing behaviour to match a group"],
    ["Obedience", "Following orders from an authority figure"],
    ["Persuasion", "Influencing someone's attitudes or behaviour"],
    ["Prejudice", "Prejudging a group negatively"],
    ["Bystander effect", "Less help given when more witnesses are present"],
    ["Social norms", "Unwritten rules of acceptable behaviour"]
  ],
  odd: [
    { items: ["Conformity", "Compliance", "Obedience", "Classical conditioning"], odd: 3, why: "Classical conditioning is learning — the rest are social influence." },
    { items: ["Prejudice", "Stereotype", "Discrimination", "Neurotransmitter"], odd: 3, why: "A neurotransmitter is a brain chemical — the rest are intergroup attitudes." },
    { items: ["Bystander effect", "Diffusion of responsibility", "Social loafing", "Placebo"], odd: 3, why: "Placebo is a medical effect — the rest explain why groups under-help." },
    { items: ["Asch", "Milgram", "Zimbardo", "Pavlov"], odd: 3, why: "Pavlov studied conditioning in dogs — the rest ran famous social psychology studies." },
    { items: ["Ingroup", "Outgroup", "Reference group", "Control group"], odd: 3, why: "A control group is for experiments — the rest are social groups." }
  ],
  scenarios: [
    { q: "In Asch's line experiment, people gave wrong answers to match the group. This is…",
      options: ["Conformity", "Obedience", "Persuasion", "Memory loss"], answer: 0,
      explain: "Matching the group's wrong answer = conformity." },
    { q: "Milgram's shock experiment studied…",
      options: ["Obedience to authority", "Memory span", "Conformity", "Dreams"], answer: 0,
      explain: "Milgram showed ordinary people obey harmful orders from authority." },
    { q: "A woman collapses in a crowded bazaar and no one helps. The likely reason?",
      options: ["Bystander effect — diffusion of responsibility", "Everyone is cruel", "She asked them not to", "Crowds always help"], answer: 0,
      explain: "More witnesses = each feels less personal responsibility." },
    { q: "Zimbardo's Stanford prison experiment showed…",
      options: ["Roles and situations powerfully shape behaviour", "Prisons are pleasant", "Students love uniforms", "Guards are born cruel"], answer: 0,
      explain: "Normal students turned cruel in guard roles — situation matters." },
    { q: "'We are hardworking; they are lazy.' This shows…",
      options: ["Ingroup favouritism", "Accurate science", "Self-actualisation", "Learned helplessness"], answer: 0,
      explain: "Favouring 'us' over 'them' is ingroup bias." },
    { q: "What reduces prejudice best, per research?",
      options: ["Equal-status cooperative contact", "Avoiding all contact", "Competitive games", "Ignoring differences"], answer: 0,
      explain: "The contact hypothesis: cooperating as equals reduces prejudice." }
  ]
}
};

/* ================= engine ================= */
var catStarted = false;
var catCat = null, catMode = null;
var catTimer = null, catTimeLeft = 0;
var catRounds = [], catIdx = 0, catScore = 0, catAnswered = false;

var MODES = [
  ["term", "⏱️ Term Sprint", "60 seconds — match terms to definitions"],
  ["odd", "🧩 Odd One Out", "5 rounds — spot the one that doesn't belong"],
  ["quiz", "🎯 Scenario Quiz", "6 scenarios — pick the right answer"]
];

function catShuffle(a){
  for(var i = a.length - 1; i > 0; i--){
    var j = Math.floor(Math.random() * (i + 1));
    var t = a[i]; a[i] = a[j]; a[j] = t;
  }
  return a;
}

function catStart(){
  catStarted = true;
  var box = document.getElementById("cat-box");
  var cats = Object.keys(CATG);
  box.innerHTML =
    '<h3 style="text-align:center">🧩 Category Challenge</h3>' +
    '<p class="small" style="text-align:center">Pick a category and a game mode.</p>' +
    '<div style="display:flex;gap:.4rem;flex-wrap:wrap;justify-content:center;margin:.8rem 0" id="cat-cats">' +
    cats.map(function(c, i){
      return '<button class="chip-btn' + (i === 0 ? " active" : "") + '" data-cat="' + esc(c) + '">' + esc(c) + "</button>";
    }).join("") + "</div>" +
    '<div style="display:flex;gap:.4rem;flex-wrap:wrap;justify-content:center;margin:.8rem 0" id="cat-modes">' +
    MODES.map(function(m, i){
      return '<button class="chip-btn' + (i === 0 ? " active" : "") + '" data-mode="' + m[0] + '" title="' + esc(m[2]) + '">' + m[1] + "</button>";
    }).join("") + "</div>" +
    '<div style="text-align:center"><button class="btn btn-primary" id="cat-go">▶ Start game</button></div>' +
    '<div id="cat-play" style="margin-top:1rem"></div>';
  catCat = cats[0]; catMode = MODES[0][0];
  box.querySelectorAll("#cat-cats .chip-btn").forEach(function(b){
    b.addEventListener("click", function(){
      box.querySelectorAll("#cat-cats .chip-btn").forEach(function(x){ x.classList.remove("active"); });
      b.classList.add("active"); catCat = b.getAttribute("data-cat");
    });
  });
  box.querySelectorAll("#cat-modes .chip-btn").forEach(function(b){
    b.addEventListener("click", function(){
      box.querySelectorAll("#cat-modes .chip-btn").forEach(function(x){ x.classList.remove("active"); });
      b.classList.add("active"); catMode = b.getAttribute("data-mode");
    });
  });
  document.getElementById("cat-go").addEventListener("click", catPlay);
}

function catPlay(){
  var data = CATG[catCat];
  catScore = 0; catIdx = 0; catAnswered = false;
  if(catTimer){ clearInterval(catTimer); catTimer = null; }
  if(catMode === "term"){
    catRounds = catShuffle(data.terms.slice());
    catTimeLeft = 60;
    renderTerm();
    catTimer = setInterval(function(){
      catTimeLeft--;
      var el = document.getElementById("cat-timer");
      if(el) el.textContent = catTimeLeft + "s";
      if(catTimeLeft <= 0){ clearInterval(catTimer); catTimer = null; catEnd(); }
    }, 1000);
  }else if(catMode === "odd"){
    catRounds = catShuffle(data.odd.slice()).slice(0, 5);
    renderOdd();
  }else{
    catRounds = catShuffle(data.scenarios.slice());
    renderQuiz();
  }
}

function catHud(extra){
  return '<div class="game-hud"><div class="hud-stat"><small>Category</small><span>' + esc(catCat) + '</span></div>' +
    '<div class="hud-stat"><small>Score</small><span id="cat-score">' + catScore + '</span></div>' + (extra || "") + "</div>";
}

function optionButtons(options, fn){
  return options.map(function(o, i){
    return '<button class="btn btn-plain" style="display:block;width:100%;text-align:left;margin:.4rem 0" data-opt="' + i + '">' + esc(o) + "</button>";
  }).join("");
}

function renderTerm(){
  var box = document.getElementById("cat-play");
  if(catIdx >= catRounds.length){ catRounds = catShuffle(CATG[catCat].terms.slice()); catIdx = 0; }
  var pair = catRounds[catIdx];
  var defs = catShuffle(CATG[catCat].terms.filter(function(t){ return t[0] !== pair[0]; }).slice(0, 3).map(function(t){ return t[1]; }).concat([pair[1]]));
  box.innerHTML = catHud('<div class="hud-stat"><small>Time</small><span id="cat-timer">' + catTimeLeft + 's</span></div>') +
    '<div class="card"><h3 style="text-align:center">"' + esc(pair[0]) + '"</h3>' +
    '<p class="small" style="text-align:center">Pick the correct definition:</p>' +
    optionButtons(defs, 0) + '<div id="cat-feed" style="margin-top:.6rem"></div></div>';
  bindOptions(box, function(i){
    var ok = defs[i] === pair[1];
    if(ok){ catScore++; }
    document.getElementById("cat-score").textContent = catScore;
    document.getElementById("cat-feed").innerHTML = ok
      ? '<div class="alert alert-ok">✓ Correct!</div>'
      : '<div class="alert alert-err">✗ It means: ' + esc(pair[1]) + "</div>";
    catIdx++;
    setTimeout(renderTerm, 900);
  });
}

function bindOptions(box, fn){
  box.querySelectorAll("[data-opt]").forEach(function(b){
    b.addEventListener("click", function(){
      if(catAnswered) return;
      catAnswered = true;
      box.querySelectorAll("[data-opt]").forEach(function(x){ x.disabled = true; });
      fn(Number(b.getAttribute("data-opt")));
      setTimeout(function(){ catAnswered = false; }, 950);
    });
  });
}

function renderOdd(){
  var box = document.getElementById("cat-play");
  if(catIdx >= catRounds.length) return catEnd();
  var r = catRounds[catIdx];
  var items = catShuffle(r.items.map(function(t, i){ return { t: t, i: i }; }));
  box.innerHTML = catHud('<div class="hud-stat"><small>Round</small><span>' + (catIdx + 1) + " / " + catRounds.length + "</span></div>") +
    '<div class="card"><p class="small" style="text-align:center"><strong>Which one does NOT belong?</strong></p>' +
    optionButtons(items.map(function(x){ return x.t; }), 0) + '<div id="cat-feed" style="margin-top:.6rem"></div></div>';
  bindOptions(box, function(i){
    var ok = items[i].i === r.odd;
    if(ok) catScore++;
    document.getElementById("cat-score").textContent = catScore;
    document.getElementById("cat-feed").innerHTML =
      '<div class="alert ' + (ok ? "alert-ok" : "alert-err") + '">' + (ok ? "✓ Correct! " : "✗ The odd one was: <strong>" + esc(r.items[r.odd]) + "</strong>. ") + esc(r.why) + "</div>";
    catIdx++;
    setTimeout(renderOdd, 2200);
  });
}

function renderQuiz(){
  var box = document.getElementById("cat-play");
  if(catIdx >= catRounds.length) return catEnd();
  var r = catRounds[catIdx];
  box.innerHTML = catHud('<div class="hud-stat"><small>Question</small><span>' + (catIdx + 1) + " / " + catRounds.length + "</span></div>") +
    '<div class="card"><p><strong>' + esc(r.q) + "</strong></p>" +
    optionButtons(r.options, 0) + '<div id="cat-feed" style="margin-top:.6rem"></div></div>';
  bindOptions(box, function(i){
    var ok = i === r.answer;
    if(ok) catScore++;
    document.getElementById("cat-score").textContent = catScore;
    document.getElementById("cat-feed").innerHTML =
      '<div class="alert ' + (ok ? "alert-ok" : "alert-err") + '">' + (ok ? "✓ Correct! " : "✗ Not quite. ") + esc(r.explain) + "</div>";
    catIdx++;
    setTimeout(renderQuiz, 2200);
  });
}

function catEnd(){
  if(catTimer){ clearInterval(catTimer); catTimer = null; }
  var attempted = catMode === "term" ? Math.max(1, catIdx) : Math.max(1, catRounds.length);
  var score = Math.min(100, Math.round((catScore / attempted) * 100));
  var box = document.getElementById("cat-play");
  box.innerHTML = '<div class="alert alert-ok" style="text-align:center">🎉 <strong>' + esc(catCat) + " — " +
    (catMode === "term" ? "Term Sprint" : catMode === "odd" ? "Odd One Out" : "Scenario Quiz") +
    "</strong><br>Score: <strong>" + score + " / 100</strong>" +
    (catMode === "term" ? " (" + catScore + " correct)" : "") + "</div>" +
    '<div id="cat-xpmsg" style="text-align:center"></div>' +
    '<div style="text-align:center;margin-top:1rem"><button class="btn btn-primary" id="cat-again">↻ Play again</button></div>';
  document.getElementById("cat-again").addEventListener("click", catStart);
  catSubmit(score);
}

async function catSubmit(score){
  var msg = document.getElementById("cat-xpmsg");
  if(window.zehenUser){
    try{
      var r = await api("/api/games/play", { method: "POST", body: { game: "category", score: score } });
      msg.innerHTML = '<p class="small">+' + (r.xp || 0) + " XP earned! 🏆</p>";
      window.zehenRefreshUser();
    }catch(e){ msg.innerHTML = '<p class="small">' + esc(e.message) + "</p>"; }
  }else{
    msg.innerHTML = '<p class="small"><a href="auth.html">Log in</a> to save your XP and join the leaderboard.</p>';
  }
}

// expose starter for games.js tab switching
window.catStartGame = catStart;
window.catGameStarted = function(){ return catStarted; };
})();
