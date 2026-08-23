"""
CareerPilot AI - Placement Question Bank: Verbal Ability
Contains verified placement-standard Verbal Ability questions across English Grammar, Vocabulary,
Reading Comprehension, Verbal Reasoning, and Sentence Construction following R.S. Aggarwal standards.

NOTE: Absolutely ZERO mathematical or numerical calculation sums are contained in Verbal Ability.
"""

from typing import List, Dict, Any

VERBAL_BANK: List[Dict[str, Any]] = [
    # ------------------ SYNONYMS ------------------
    {
        "question": "Select the word that is most nearly SIMILAR in meaning (SYNONYM) to the bold word:\n\n**CANDID**",
        "category": "Verbal Ability",
        "topic": "Synonyms",
        "subtopic": "Vocabulary",
        "difficulty": "Easy",
        "options": ["Frank", "Secretive", "Deceitful", "Ambiguous"],
        "correct_answer": "A",
        "explanation": "'Candid' means truthful, straightforward, and frank. 'Frank' is its exact synonym.",
        "formula": "Contextual Vocabulary Matching",
        "shortcut": "Eliminate antonyms: Secretive and Deceitful",
        "concept": "Synonym Recognition",
        "time_limit": 45
    },
    {
        "question": "Select the word that is most nearly SIMILAR in meaning (SYNONYM) to the bold word:\n\n**PRUDENT**",
        "category": "Verbal Ability",
        "topic": "Synonyms",
        "subtopic": "Vocabulary",
        "difficulty": "Easy",
        "options": ["Cautious", "Reckless", "Extravagant", "Foolish"],
        "correct_answer": "A",
        "explanation": "'Prudent' means acting with or showing care and thought for the future. 'Cautious' is a synonym.",
        "formula": "Root & Meaning Analysis",
        "shortcut": "Reckless and Foolish are antonyms.",
        "concept": "Synonym Recognition",
        "time_limit": 45
    },
    {
        "question": "Select the word that is most nearly SIMILAR in meaning (SYNONYM) to the bold word:\n\n**METICULOUS**",
        "category": "Verbal Ability",
        "topic": "Synonyms",
        "subtopic": "Vocabulary",
        "difficulty": "Medium",
        "options": ["Precise", "Careless", "Sloppy", "Hasty"],
        "correct_answer": "A",
        "explanation": "'Meticulous' means showing great attention to detail; careful and precise.",
        "formula": "Contextual Vocabulary Matching",
        "shortcut": "Careless and Sloppy are opposite meanings.",
        "concept": "Advanced Vocabulary",
        "time_limit": 45
    },
    {
        "question": "Select the word that is most nearly SIMILAR in meaning (SYNONYM) to the bold word:\n\n**OBSTINATE**",
        "category": "Verbal Ability",
        "topic": "Synonyms",
        "subtopic": "Vocabulary",
        "difficulty": "Medium",
        "options": ["Stubborn", "Flexible", "Yielding", "Submissive"],
        "correct_answer": "A",
        "explanation": "'Obstinate' means stubbornly refusing to change one's opinion or chosen course of action.",
        "formula": "Synonym Identification",
        "shortcut": "Flexible and Yielding are opposite traits.",
        "concept": "Advanced Vocabulary",
        "time_limit": 45
    },
    {
        "question": "Select the word that is most nearly SIMILAR in meaning (SYNONYM) to the bold word:\n\n**BENEVOLENT**",
        "category": "Verbal Ability",
        "topic": "Synonyms",
        "subtopic": "Vocabulary",
        "difficulty": "Medium",
        "options": ["Kind-hearted", "Malevolent", "Greedy", "Cruel"],
        "correct_answer": "A",
        "explanation": "'Benevolent' (prefix bene = good) means well-meaning and kindly.",
        "formula": "Latin Prefix Analysis (Bene- = Good)",
        "shortcut": "Malevolent (Male- = Bad) is the direct antonym.",
        "concept": "Etymology & Root Words",
        "time_limit": 45
    },
    {
        "question": "Select the word that is most nearly SIMILAR in meaning (SYNONYM) to the bold word:\n\n**EPHEMERAL**",
        "category": "Verbal Ability",
        "topic": "Synonyms",
        "subtopic": "Vocabulary",
        "difficulty": "Hard",
        "options": ["Transient", "Permanent", "Eternal", "Perpetual"],
        "correct_answer": "A",
        "explanation": "'Ephemeral' means lasting for a very short time. 'Transient' means temporary or short-lived.",
        "formula": "Contextual Matching",
        "shortcut": "Permanent, Eternal, and Perpetual are all antonyms.",
        "concept": "High-Frequency Placement Vocabulary",
        "time_limit": 50
    },
    {
        "question": "Select the word that is most nearly SIMILAR in meaning (SYNONYM) to the bold word:\n\n**PERSPICACIOUS**",
        "category": "Verbal Ability",
        "topic": "Synonyms",
        "subtopic": "Vocabulary",
        "difficulty": "Hard",
        "options": ["Insightful", "Dull", "Ignorant", "Naive"],
        "correct_answer": "A",
        "explanation": "'Perspicacious' means having a ready insight into and understanding of things; keen-minded.",
        "formula": "Latin Root Analysis (Spec/Spic = to look/see)",
        "shortcut": "Dull and Ignorant are opposite traits.",
        "concept": "High-Frequency Placement Vocabulary",
        "time_limit": 50
    },

    # ------------------ ANTONYMS ------------------
    {
        "question": "Select the word that is OPPOSITE in meaning (ANTONYM) to the bold word:\n\n**ARTICULATE**",
        "category": "Verbal Ability",
        "topic": "Antonyms",
        "subtopic": "Vocabulary",
        "difficulty": "Easy",
        "options": ["Incoherent", "Fluent", "Expressive", "Eloquently spoken"],
        "correct_answer": "A",
        "explanation": "'Articulate' means fluent and clear in speech. Its opposite is 'Incoherent'.",
        "formula": "Antonym Identification",
        "shortcut": "Fluent and Expressive are synonyms.",
        "concept": "Antonym Recognition",
        "time_limit": 45
    },
    {
        "question": "Select the word that is OPPOSITE in meaning (ANTONYM) to the bold word:\n\n**FRUGAL**",
        "category": "Verbal Ability",
        "topic": "Antonyms",
        "subtopic": "Vocabulary",
        "difficulty": "Medium",
        "options": ["Extravagant", "Thrifty", "Economical", "Sparing"],
        "correct_answer": "A",
        "explanation": "'Frugal' means economical or economical regarding money. 'Extravagant' is its antonym.",
        "formula": "Antonym Identification",
        "shortcut": "Thrifty and Economical are synonyms of Frugal.",
        "concept": "Placement Antonym Patterns",
        "time_limit": 45
    },
    {
        "question": "Select the word that is OPPOSITE in meaning (ANTONYM) to the bold word:\n\n**BELLIGERENT**",
        "category": "Verbal Ability",
        "topic": "Antonyms",
        "subtopic": "Vocabulary",
        "difficulty": "Medium",
        "options": ["Peaceful", "Aggressive", "Hostile", "Combative"],
        "correct_answer": "A",
        "explanation": "'Belligerent' means hostile and aggressive. 'Peaceful' is the exact antonym.",
        "formula": "Root Word (Bell = War)",
        "shortcut": "Aggressive, Hostile, and Combative are synonyms.",
        "concept": "Placement Antonym Patterns",
        "time_limit": 45
    },
    {
        "question": "Select the word that is OPPOSITE in meaning (ANTONYM) to the bold word:\n\n**LAUDABLE**",
        "category": "Verbal Ability",
        "topic": "Antonyms",
        "subtopic": "Vocabulary",
        "difficulty": "Hard",
        "options": ["Blameworthy", "Praiseworthy", "Commendable", "Admirable"],
        "correct_answer": "A",
        "explanation": "'Laudable' means deserving praise and commendation. 'Blameworthy' is its antonym.",
        "formula": "Etymology Analysis (Laud = Praise)",
        "shortcut": "Praiseworthy, Commendable, and Admirable are all synonyms.",
        "concept": "Advanced Antonyms",
        "time_limit": 50
    },

    # ------------------ ONE-WORD SUBSTITUTION ------------------
    {
        "question": "Choose the one-word substitute for the phrase:\n\n\"A person who speaks many languages fluently.\"",
        "category": "Verbal Ability",
        "topic": "One-Word Substitution",
        "subtopic": "Vocabulary",
        "difficulty": "Easy",
        "options": ["Polyglot", "Linguist", "Bilingual", "Orator"],
        "correct_answer": "A",
        "explanation": "'Polyglot' (poly = many, glot = tongue/language) refers to a person who knows and uses several languages.",
        "formula": "Greek Root Analysis (Poly + Glot)",
        "shortcut": "Bilingual means specifically two languages; Polyglot means many.",
        "concept": "Vocabulary Substitution",
        "time_limit": 45
    },
    {
        "question": "Choose the one-word substitute for the phrase:\n\n\"One who looks on the bright and hopeful side of things.\"",
        "category": "Verbal Ability",
        "topic": "One-Word Substitution",
        "subtopic": "Vocabulary",
        "difficulty": "Easy",
        "options": ["Optimist", "Pessimist", "Altruist", "Realist"],
        "correct_answer": "A",
        "explanation": "An 'Optimist' hopes for the best and looks at positive aspects. A 'Pessimist' looks at negative aspects.",
        "formula": "Standard Substitution Rules",
        "shortcut": "Pessimist is the exact opposite.",
        "concept": "Vocabulary Substitution",
        "time_limit": 45
    },
    {
        "question": "Choose the one-word substitute for the phrase:\n\n\"A speech or presentation delivered without any previous preparation.\"",
        "category": "Verbal Ability",
        "topic": "One-Word Substitution",
        "subtopic": "Vocabulary",
        "difficulty": "Medium",
        "options": ["Extempore", "Maiden speech", "Eulogy", "Soliloquy"],
        "correct_answer": "A",
        "explanation": "'Extempore' (or Impromptu) means spoken or done without preparation. 'Maiden speech' is a first speech.",
        "formula": "Standard Substitution Rules",
        "shortcut": "Soliloquy is speaking thoughts aloud when alone.",
        "concept": "Placement Vocabulary Standards",
        "time_limit": 45
    },
    {
        "question": "Choose the one-word substitute for the phrase:\n\n\"One who donates money, time, and resources to promote human welfare.\"",
        "category": "Verbal Ability",
        "topic": "One-Word Substitution",
        "subtopic": "Vocabulary",
        "difficulty": "Medium",
        "options": ["Philanthropist", "Misanthrope", "Miser", "Mercenary"],
        "correct_answer": "A",
        "explanation": "'Philanthropist' (Phil = love, Anthropos = mankind). 'Misanthrope' is a hater of mankind.",
        "formula": "Root Word Analysis (Phil + Anthropos)",
        "shortcut": "Misanthrope is the direct antonym.",
        "concept": "Placement Vocabulary Standards",
        "time_limit": 45
    },

    # ------------------ IDIOMS & PHRASES ------------------
    {
        "question": "Select the correct meaning of the idiom:\n\n**To burn the midnight oil**",
        "category": "Verbal Ability",
        "topic": "Idioms & Phrases",
        "subtopic": "Idioms",
        "difficulty": "Easy",
        "options": [
            "To work or study late into the night",
            "To waste fuel needlessly",
            "To cause a fire accidentally",
            "To wake up early in the morning"
        ],
        "correct_answer": "A",
        "explanation": "'Burn the midnight oil' means to read, study, or work late at night.",
        "formula": "Figurative Meaning Interpretation",
        "shortcut": "Refers to oil lamps used for studying at night.",
        "concept": "Idiomatic Usage",
        "time_limit": 45
    },
    {
        "question": "Select the correct meaning of the idiom:\n\n**To turn over a new leaf**",
        "category": "Verbal Ability",
        "topic": "Idioms & Phrases",
        "subtopic": "Idioms",
        "difficulty": "Easy",
        "options": [
            "To start behaving in a better or wiser way",
            "To change a book page quickly",
            "To start a gardening project",
            "To repeat a past mistake"
        ],
        "correct_answer": "A",
        "explanation": "'Turn over a new leaf' means to make a fresh start and change one's conduct for the better.",
        "formula": "Figurative Meaning Interpretation",
        "shortcut": "Leaf refers to a blank page in a journal/book.",
        "concept": "Idiomatic Usage",
        "time_limit": 45
    },
    {
        "question": "Select the correct meaning of the idiom:\n\n**Bite the bullet**",
        "category": "Verbal Ability",
        "topic": "Idioms & Phrases",
        "subtopic": "Idioms",
        "difficulty": "Medium",
        "options": [
            "To endure a painful or difficult situation with courage",
            "To act aggressively in a dispute",
            "To fail to accomplish a goal",
            "To speak rashly without thinking"
        ],
        "correct_answer": "A",
        "explanation": "'Bite the bullet' comes from military surgery without anesthesia, meaning to face a tough situation bravely.",
        "formula": "Contextual Idiom Interpretation",
        "shortcut": "Historical origin: biting a lead bullet to cope with pain.",
        "concept": "Placement Idiom Standards",
        "time_limit": 45
    },
    {
        "question": "Select the correct meaning of the idiom:\n\n**Once in a blue moon**",
        "category": "Verbal Ability",
        "topic": "Idioms & Phrases",
        "subtopic": "Idioms",
        "difficulty": "Medium",
        "options": [
            "Very rarely or seldom",
            "Frequently and regularly",
            "During full moon night",
            "Unexpectedly during day"
        ],
        "correct_answer": "A",
        "explanation": "'Once in a blue moon' refers to an event that happens extremely rarely.",
        "formula": "Frequency Phrase Interpretation",
        "shortcut": "Blue moons occur roughly once every 2.7 years.",
        "concept": "Placement Idiom Standards",
        "time_limit": 45
    },

    # ------------------ SUBJECT-VERB AGREEMENT ------------------
    {
        "question": "Fill in the blank with the grammatically correct option:\n\n\"Neither of the two job candidates _____ qualified for the senior software architect position.\"",
        "category": "Verbal Ability",
        "topic": "Subject-Verb Agreement",
        "subtopic": "Grammar",
        "difficulty": "Easy",
        "options": ["is", "are", "were", "have been"],
        "correct_answer": "A",
        "explanation": "Indefinite pronoun 'Neither' is singular and takes a singular verb ('is').",
        "formula": "Singular Subject + Singular Verb",
        "shortcut": "Ignore plural noun in prepositional phrase ('candidates'). Core head is 'Neither'.",
        "concept": "Subject-Verb Concord",
        "time_limit": 45
    },
    {
        "question": "Fill in the blank with the grammatically correct option:\n\n\"The project manager, along with all team members, _____ attending the client meeting today.\"",
        "category": "Verbal Ability",
        "topic": "Subject-Verb Agreement",
        "subtopic": "Grammar",
        "difficulty": "Medium",
        "options": ["is", "are", "were", "have been"],
        "correct_answer": "A",
        "explanation": "Phrases like 'along with', 'as well as', 'together with' do not change the subject. The subject is 'The project manager' (singular), requiring 'is'.",
        "formula": "Head Noun Agreement (Parenthetical Phrases Ignored)",
        "shortcut": "Cross out 'along with team members'. Subject = The project manager.",
        "concept": "Subject-Verb Concord",
        "time_limit": 45
    },
    {
        "question": "Fill in the blank with the grammatically correct option:\n\n\"Ten miles _____ a long distance to walk every morning.\"",
        "category": "Verbal Ability",
        "topic": "Subject-Verb Agreement",
        "subtopic": "Grammar",
        "difficulty": "Medium",
        "options": ["is", "are", "were", "have been"],
        "correct_answer": "A",
        "explanation": "Expressions of time, distance, money, or weight are considered a single unit and take a singular verb ('is').",
        "formula": "Unit Quantity = Singular Verb",
        "shortcut": "Distance expressed as a single total quantity = singular verb.",
        "concept": "Subject-Verb Concord",
        "time_limit": 45
    },
    {
        "question": "Fill in the blank with the grammatically correct option:\n\n\"Every boy and girl in the class _____ submitted the assignment on time.\"",
        "category": "Verbal Ability",
        "topic": "Subject-Verb Agreement",
        "subtopic": "Grammar",
        "difficulty": "Hard",
        "options": ["has", "have", "were", "are"],
        "correct_answer": "A",
        "explanation": "When compound subjects are preceded by 'every' or 'each', they take a singular verb ('has').",
        "formula": "Every/Each + Singular Nouns = Singular Verb",
        "shortcut": "'Every' modifies the entire subject to singular.",
        "concept": "Advanced Subject-Verb Rules",
        "time_limit": 50
    },

    # ------------------ ERROR DETECTION ------------------
    {
        "question": "Identify the section of the sentence that contains a grammatical error:\n\n\"(A) One of the main reasons / (B) for his success / (C) are his hard work and dedication / (D) during college.\"",
        "category": "Verbal Ability",
        "topic": "Error Detection",
        "subtopic": "Grammar",
        "difficulty": "Easy",
        "options": [
            "(C) are his hard work and dedication",
            "(A) One of the main reasons",
            "(B) for his success",
            "(D) during college."
        ],
        "correct_answer": "A",
        "explanation": "The subject is 'One' (singular). Therefore, the verb should be singular ('is'), not plural ('are'). Correct form: 'is his hard work'.",
        "formula": "One of + Plural Noun + Singular Verb",
        "shortcut": "Match verb with 'One', not 'reasons'.",
        "concept": "Grammatical Error Spotting",
        "time_limit": 45
    },
    {
        "question": "Identify the section of the sentence that contains a grammatical error:\n\n\"(A) She had been working / (B) in this software firm / (C) since five years / (D) before she resigned.\"",
        "category": "Verbal Ability",
        "topic": "Error Detection",
        "subtopic": "Grammar",
        "difficulty": "Medium",
        "options": [
            "(C) since five years",
            "(A) She had been working",
            "(B) in this software firm",
            "(D) before she resigned."
        ],
        "correct_answer": "A",
        "explanation": "'For' is used for a duration of time ('five years'). 'Since' is used for a specific starting point in time ('since 2019'). Should be 'for five years'.",
        "formula": "Preposition Rule: For + Duration | Since + Point in Time",
        "shortcut": "5 years is a period/duration, so use 'for'.",
        "concept": "Tenses & Prepositions",
        "time_limit": 45
    },

    # ------------------ SENTENCE CORRECTION & IMPROVEMENT ------------------
    {
        "question": "Choose the option that BEST improves the underlined part of the sentence:\n\n\"If he **would have studied** harder, he would have cleared the campus recruitment test.\"",
        "category": "Verbal Ability",
        "topic": "Sentence Correction",
        "subtopic": "Grammar",
        "difficulty": "Medium",
        "options": [
            "had studied",
            "would study",
            "has studied",
            "was studying"
        ],
        "correct_answer": "A",
        "explanation": "In 3rd Conditional sentences: If-clause takes Past Perfect ('had studied'), and main clause takes 'would have + past participle'.",
        "formula": "Third Conditional: If + Past Perfect, Would have + Past Participle",
        "shortcut": "Never use 'would have' in the if-clause.",
        "concept": "Conditional Sentences",
        "time_limit": 45
    },
    {
        "question": "Choose the option that BEST improves the underlined part of the sentence:\n\n\"The team played **more better** in the second half of the tournament.\"",
        "category": "Verbal Ability",
        "topic": "Sentence Correction",
        "subtopic": "Grammar",
        "difficulty": "Easy",
        "options": [
            "much better",
            "more good",
            "most better",
            "more well"
        ],
        "correct_answer": "A",
        "explanation": "'Better' is already a comparative adjective. Using 'more better' is a double comparative error. Correct intensive form is 'much better'.",
        "formula": "Avoid Double Comparatives",
        "shortcut": "'More' cannot be combined with '-er' comparative words.",
        "concept": "Adjective & Modifier Rules",
        "time_limit": 45
    },

    # ------------------ FILL IN THE BLANKS & SENTENCE COMPLETION ------------------
    {
        "question": "Fill in the blank with the most appropriate vocabulary word:\n\n\"Despite facing severe setbacks during the pandemic, the entrepreneur remained _____ and successfully rebuilt her firm.\"",
        "category": "Verbal Ability",
        "topic": "Fill in the Blanks",
        "subtopic": "Vocabulary",
        "difficulty": "Medium",
        "options": ["resilient", "fragile", "pessimistic", "indifferent"],
        "correct_answer": "A",
        "explanation": "'Resilient' means able to withstand or recover quickly from difficult conditions. Fits the context of overcoming setbacks.",
        "formula": "Contextual Tone Matching ('Despite' signals contrast)",
        "shortcut": "'Despite setbacks' requires a positive perseverance trait.",
        "concept": "Contextual Sentence Completion",
        "time_limit": 45
    },
    {
        "question": "Fill in the blank with the appropriate preposition:\n\n\"The candidate was congratulated _____ securing the highest score in the technical evaluation.\"",
        "category": "Verbal Ability",
        "topic": "Fill in the Blanks",
        "subtopic": "Grammar",
        "difficulty": "Easy",
        "options": ["on", "for", "at", "with"],
        "correct_answer": "A",
        "explanation": "The verb 'congratulate' takes the fixed preposition 'on' (congratulate someone on something).",
        "formula": "Fixed Preposition: Congratulate + Person + ON + Event",
        "shortcut": "Never use 'congratulate for' in standard English.",
        "concept": "Fixed Prepositions",
        "time_limit": 45
    },

    # ------------------ ACTIVE & PASSIVE VOICE / DIRECT & INDIRECT SPEECH ------------------
    {
        "question": "Select the correct PASSIVE VOICE form of the sentence:\n\n\"The senior director approved the new software architecture project.\"",
        "category": "Verbal Ability",
        "topic": "Active & Passive Voice",
        "subtopic": "Grammar",
        "difficulty": "Medium",
        "options": [
            "The new software architecture project was approved by the senior director.",
            "The new software architecture project is approved by the senior director.",
            "The new software architecture project has been approved by the senior director.",
            "The new software architecture project had approved by the senior director."
        ],
        "correct_answer": "A",
        "explanation": "Simple Past Active ('approved') converts to Simple Past Passive ('was approved by').",
        "formula": "Simple Past Passive: Subject + was/were + Past Participle + by + Agent",
        "shortcut": "Active verb 'approved' requires 'was approved' in passive voice.",
        "concept": "Voice Conversion Rules",
        "time_limit": 45
    },
    {
        "question": "Select the correct INDIRECT SPEECH conversion of the sentence:\n\n\"Rohan said, 'I am working on the database migration today.'\"",
        "category": "Verbal Ability",
        "topic": "Direct & Indirect Speech",
        "subtopic": "Grammar",
        "difficulty": "Hard",
        "options": [
            "Rohan said that he was working on the database migration that day.",
            "Rohan said that I am working on the database migration today.",
            "Rohan told that he is working on the database migration today.",
            "Rohan said that he had worked on the database migration that day."
        ],
        "correct_answer": "A",
        "explanation": "Tense shift: Present Continuous ('am working') shifts to Past Continuous ('was working'). Time shift: 'today' shifts to 'that day'.",
        "formula": "Indirect Speech Tense & Pronoun Rules",
        "shortcut": "'today' changes to 'that day', 'I am' changes to 'he was'.",
        "concept": "Reported Speech Rules",
        "time_limit": 50
    },

    # ------------------ PARA JUMBLES & SENTENCE ARRANGEMENT ------------------
    {
        "question": "Rearrange the given sentences (P, Q, R, S) in a logical sequence to form a coherent paragraph:\n\nP: Artificial Intelligence is revolutionizing modern industry sectors.\nQ: Consequently, tech companies are investing heavily in automated tools.\nR: Among these, machine learning algorithms play a pivotal role.\nS: As a result, software engineers need to upskill continuously.",
        "category": "Verbal Ability",
        "topic": "Para Jumbles",
        "subtopic": "Logical Paragraph Structure",
        "difficulty": "Hard",
        "options": ["P - R - Q - S", "Q - P - S - R", "R - S - P - Q", "S - P - R - Q"],
        "correct_answer": "A",
        "explanation": "P introduces the broad topic (AI in industry). R elaborates on AI ('Among these... machine learning'). Q shows corporate response (investing). S shows individual engineer impact (upskilling). Flow: P -> R -> Q -> S.",
        "formula": "General Theme -> Specific Detail -> Consequence -> Conclusion",
        "shortcut": "P is the clear introductory sentence.",
        "concept": "Paragraph Coherence & Logic",
        "time_limit": 60
    },

    # ------------------ READING COMPREHENSION ------------------
    {
        "question": "Read the short passage below and answer the question:\n\n\"Quantum computing represents a fundamental shift in processing capability. Unlike classical computers that rely on binary bits (0 or 1), quantum systems utilize qubits capable of existing in superposition. This property enables parallel execution of complex mathematical calculations, offering exponential speedups for cryptography and molecular modeling.\"\n\n**Question:** According to the passage, what unique property allows quantum computers to execute calculations in parallel?",
        "category": "Verbal Ability",
        "topic": "Reading Comprehension",
        "subtopic": "Passage Inference",
        "difficulty": "Medium",
        "options": [
            "Superposition",
            "Binary bits",
            "Molecular modeling",
            "Classical processing"
        ],
        "correct_answer": "A",
        "explanation": "The passage explicitly states: 'quantum systems utilize qubits capable of existing in superposition. This property enables parallel execution...'",
        "formula": "Direct Fact Retrieval from Passage",
        "shortcut": "Look for keyword 'parallel execution' in passage text.",
        "concept": "Passage Reading & Comprehension",
        "time_limit": 60
    }
]


def get_verbal_questions() -> List[Dict[str, Any]]:
    """Returns verified placement-standard Verbal Ability questions."""
    return VERBAL_BANK
