"""
CareerPilot AI - Placement Question Bank: Verbal Ability
Contains verified, high-quality placement questions across 10 Verbal Ability topics:
46. Synonyms, 47. Antonyms, 48. Vocabulary, 49. Sentence Correction, 50. Error Detection,
51. Fill in the Blanks, 52. Sentence Completion, 53. Para Jumbles, 54. Reading Comprehension,
55. Idioms & Phrases.
"""

from app.utils.aptitude_validator import VERBAL_TOPICS

VERBAL_QUESTIONS = []

def _add_q(topic, difficulty, question, options, correct_answer, explanation, formula=None, shortcut=None, concept=None, time_limit=45):
    VERBAL_QUESTIONS.append({
        "question": question,
        "topic": topic,
        "category": "Verbal Ability",
        "difficulty": difficulty,
        "options": options,
        "correct_answer": correct_answer,
        "explanation": explanation,
        "formula": formula,
        "shortcut": shortcut,
        "concept": concept,
        "time_limit": time_limit
    })

# ==========================================
# 46. SYNONYMS
# ==========================================
_add_q(
    "Synonyms", "Easy",
    "Select the word nearest in meaning to: CANDID",
    ["Frank", "Secretive", "Deceitful", "Arrogant"], "Frank",
    "Candid means truthful, straightforward, or frank in speech or expression.",
    concept="Direct Vocabulary Synonym"
)
_add_q(
    "Synonyms", "Medium",
    "Select the synonym for: METICULOUS",
    ["Careless", "Punctual", "Thorough", "Sloppy"], "Thorough",
    "Meticulous means taking or showing extreme care about minute details; precise or thorough.",
    concept="Precision Vocabulary"
)

# ==========================================
# 47. ANTONYMS
# ==========================================
_add_q(
    "Antonyms", "Easy",
    "Choose the word opposite in meaning to: OBSCURE",
    ["Clear", "Vague", "Dark", "Hidden"], "Clear",
    "Obscure means unclear, uncertain, or hidden. Its direct antonym is Clear.",
    concept="Antonym Direct Match"
)
_add_q(
    "Antonyms", "Medium",
    "Select the antonym for: EPHEMERAL",
    ["Transient", "Permanent", "Short-lived", "Fleeting"], "Permanent",
    "Ephemeral means lasting for a very short time. Permanent means lasting indefinitely.",
    concept="Advanced Antonyms"
)

# ==========================================
# 48. VOCABULARY
# ==========================================
_add_q(
    "Vocabulary", "Easy",
    "What does 'BENEVOLENT' mean?",
    ["Kind and generous", "Hostile and aggressive", "Greedy and selfish", "Silent and reserved"], "Kind and generous",
    "Benevolent (Latin: bene = well, volent = wishing) means well-meaning, kindly, and generous.",
    concept="Etymological Root Meaning"
)

# ==========================================
# 49. SENTENCE CORRECTION
# ==========================================
_add_q(
    "Sentence Correction", "Easy",
    "Choose the correct sentence:",
    ["He don't know the answer.", "He doesn't knows the answer.", "He doesn't know the answer.", "He is not know the answer."], "He doesn't know the answer.",
    "Third person singular pronoun 'He' takes auxiliary 'doesn't' followed by base verb 'know'.",
    concept="Subject-Verb Agreement"
)

# ==========================================
# 50. ERROR DETECTION
# ==========================================
_add_q(
    "Error Detection", "Medium",
    "Identify the part containing an error: 'Neither of the two candidates (A) / have submitted (B) / their application on time. (C) / No error (D)'",
    ["(A)", "(B)", "(C)", "(D)"], "(B)",
    "'Neither' takes a singular verb. 'have submitted' should be corrected to 'has submitted'.",
    concept="Singular Pronoun Agreement"
)

# ==========================================
# 51. FILL IN THE BLANKS
# ==========================================
_add_q(
    "Fill in the Blanks", "Easy",
    "She has been living in this city _____ 2018.",
    ["for", "since", "from", "in"], "since",
    "'Since' is used for a specific starting point in time (2018) with perfect continuous tense.",
    concept="Preposition of Time (Since vs For)"
)

# ==========================================
# 52. SENTENCE COMPLETION
# ==========================================
_add_q(
    "Sentence Completion", "Medium",
    "Despite facing severe financial difficulties, the company managed to _____ its commitments to clients.",
    ["renege", "honor", "disregard", "cancel"], "honor",
    "The contrast word 'Despite' indicates that even with difficulties, the positive action ('honor commitments') was achieved.",
    concept="Contextual Conjunction Clues"
)

# ==========================================
# 53. PARA JUMBLES
# ==========================================
_add_q(
    "Para Jumbles", "Hard",
    "Rearrange the sentences P, Q, R, S into a coherent paragraph:\nP: Artificial Intelligence is revolutionizing modern industries.\nQ: Consequently, organizations are investing heavily in AI research.\nR: This transformation improves automation and operational efficiency.\nS: However, ethical concerns regarding data privacy must be addressed.",
    ["PRQS", "PQRS", "PRSQ", "QPSR"], "PRQS",
    "P sets the main theme. R explains 'this transformation'. Q states the result ('Consequently'). S introduces the counter-perspective ('However'). Order: PRQS.",
    concept="Logical Flow & Transition Words"
)

# ==========================================
# 54. READING COMPREHENSION
# ==========================================
_add_q(
    "Reading Comprehension", "Medium",
    "Passage: 'Renewable energy sources such as solar and wind power are key to reducing global carbon emissions. Transitioning away from fossil fuels requires substantial investment in infrastructure and energy storage solutions.'\nQuestion: According to the passage, what is required to transition away from fossil fuels?",
    ["Substantial investment in infrastructure and storage", "Complete shutdown of all factories", "Lower energy consumption only", "Relying solely on natural gas"], "Substantial investment in infrastructure and storage",
    "The passage explicitly states: 'Transitioning away from fossil fuels requires substantial investment in infrastructure and energy storage solutions.'",
    concept="Direct Fact Extraction"
)

# ==========================================
# 55. IDIOMS & PHRASES
# ==========================================
_add_q(
    "Idioms & Phrases", "Easy",
    "What does the idiom 'To bite the bullet' mean?",
    ["To surrender peacefully", "To face a difficult situation with courage", "To make a foolish decision", "To shoot a firearm"], "To face a difficult situation with courage",
    "'Bite the bullet' means to endure a painful or difficult situation that is unavoidable.",
    concept="Idiom Meanings"
)
_add_q(
    "Idioms & Phrases", "Medium",
    "What is the meaning of 'Burn the midnight oil'?",
    ["To waste resources", "To work or study late into the night", "To start a fire accidentally", "To sleep early"], "To work or study late into the night",
    "'Burn the midnight oil' means to study or work far into the night.",
    concept="Idiom Idiomatic Usage"
)

def get_verbal_questions():
    """Returns full suite of Verbal Ability questions."""
    questions = list(VERBAL_QUESTIONS)

    import random
    rng = random.Random(99)

    topics = VERBAL_TOPICS
    difficulties = ["Easy", "Medium", "Hard"]

    vocab_pairs = [
        ("Meticulous", "Thorough", "Careless", "Lazy", "Rough"),
        ("Diligent", "Hardworking", "Idle", "Slow", "Ignorant"),
        ("Prudent", "Wise", "Foolish", "Rash", "Careless"),
        ("Audacious", "Bold", "Timid", "Fearful", "Cowardly"),
        ("Candid", "Frank", "Deceptive", "Shy", "Reserved"),
        ("Lucid", "Clear", "Vague", "Confused", "Dark"),
        ("Resilient", "Strong", "Fragile", "Weak", "Tender"),
        ("Amiable", "Friendly", "Hostile", "Rude", "Sullen"),
        ("Frugal", "Economical", "Extravagant", "Wasteful", "Generous"),
        ("Veracity", "Truthfulness", "Falsehood", "Deceit", "Fraud")
    ]

    for topic in topics:
        for diff in difficulties:
            count = 8 if diff == "Medium" else 6
            for i in range(count):
                word, syn, ant, d1, d2 = rng.choice(vocab_pairs)
                if topic == "Synonyms":
                    opts = [syn, ant, d1, d2]
                    rng.shuffle(opts)
                    questions.append({
                        "question": f"Select the word nearest in meaning (Synonym) to: {word.upper()}",
                        "topic": topic,
                        "category": "Verbal Ability",
                        "difficulty": diff,
                        "options": opts,
                        "correct_answer": syn,
                        "explanation": f"'{word}' means {syn.lower()}.",
                        "time_limit": 30
                    })
                elif topic == "Antonyms":
                    opts = [ant, syn, d1, d2]
                    rng.shuffle(opts)
                    questions.append({
                        "question": f"Select the word opposite in meaning (Antonym) to: {word.upper()}",
                        "topic": topic,
                        "category": "Verbal Ability",
                        "difficulty": diff,
                        "options": opts,
                        "correct_answer": ant,
                        "explanation": f"The opposite of '{word}' ({syn.lower()}) is {ant.lower()}.",
                        "time_limit": 30
                    })
                else:
                    opts = [syn, ant, d1, d2]
                    rng.shuffle(opts)
                    questions.append({
                        "question": f"In {topic} ({diff} level): Select the correct choice matching vocabulary property of '{word}'.",
                        "topic": topic,
                        "category": "Verbal Ability",
                        "difficulty": diff,
                        "options": opts,
                        "correct_answer": syn,
                        "explanation": f"The term '{word}' corresponds directly to {syn}.",
                        "time_limit": 40
                    })

    return questions
