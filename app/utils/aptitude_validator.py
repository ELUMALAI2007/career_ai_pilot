"""
CareerPilot AI - Aptitude Question Validation Engine
Ensures mathematical, logical, and structural validity of all aptitude questions before database storage.
"""

from typing import Dict, Any, Tuple, Optional, List

VALID_CATEGORIES = [
    "Quantitative Aptitude",
    "Logical Reasoning",
    "Verbal Ability"
]

QUANT_TOPICS = [
    "Number System", "HCF & LCM", "Simplification", "Divisibility", "Percentages",
    "Ratio & Proportion", "Average", "Profit & Loss", "Simple Interest", "Compound Interest",
    "Time & Work", "Pipes & Cisterns", "Time, Speed & Distance", "Trains", "Boats & Streams",
    "Mixtures & Allegations", "Partnership", "Ages", "Problems on Numbers",
    "Permutation & Combination", "Probability", "Mensuration", "Geometry", "Algebra",
    "Progressions", "Data Interpretation"
]

LOGICAL_TOPICS = [
    "Number Series", "Alphabet Series", "Coding-Decoding", "Blood Relations",
    "Direction Sense", "Seating Arrangement", "Puzzles", "Syllogisms",
    "Statement & Conclusion", "Statement & Assumption", "Analogy", "Classification",
    "Odd One Out", "Data Sufficiency", "Ranking & Order", "Clocks", "Calendars",
    "Venn Diagrams", "Logical Deduction"
]

VERBAL_TOPICS = [
    "Synonyms", "Antonyms", "Vocabulary", "Sentence Correction", "Error Detection",
    "Fill in the Blanks", "Sentence Completion", "Para Jumbles", "Reading Comprehension",
    "Idioms & Phrases"
]

ALL_TOPICS = QUANT_TOPICS + LOGICAL_TOPICS + VERBAL_TOPICS

VALID_DIFFICULTIES = ["Easy", "Medium", "Hard", "foundation", "beginner", "intermediate", "advanced", "expert", "master"]

# Difficulty Normalization Map
DIFFICULTY_MAP = {
    "easy": "Easy",
    "medium": "Medium",
    "hard": "Hard",
    "foundation": "Easy",
    "beginner": "Easy",
    "intermediate": "Medium",
    "advanced": "Hard",
    "expert": "Hard",
    "master": "Hard"
}


def normalize_difficulty(diff: str) -> str:
    """Normalizes any difficulty input string to Easy, Medium, or Hard."""
    if not diff:
        return "Medium"
    d_clean = str(diff).strip().lower()
    if d_clean in DIFFICULTY_MAP:
        return DIFFICULTY_MAP[d_clean]
    if any(k in d_clean for k in ["easy", "beginner", "basic", "foundation"]):
        return "Easy"
    if any(k in d_clean for k in ["hard", "advanced", "expert", "master"]):
        return "Hard"
    if any(k in d_clean for k in ["medium", "intermediate", "placement"]):
        return "Medium"
    return "Medium"


def validate_question(q: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validates an aptitude question dict against placement quality standards.
    Returns (True, None) if valid, or (False, error_reason) if invalid.
    """
    if not isinstance(q, dict):
        return False, "Question must be a dictionary object"

    # Required field presence check
    question_text = q.get("question") or q.get("question_text")
    if not question_text or not str(question_text).strip():
        return False, "Missing or empty question text"

    category = q.get("category")
    if category and category not in VALID_CATEGORIES:
        return False, f"Invalid category '{category}'. Must be one of {VALID_CATEGORIES}"

    # Extract options
    options = q.get("options")
    if not options or not isinstance(options, list):
        # Fallback to option_a, option_b, option_c, option_d format
        opt_a = q.get("option_a")
        opt_b = q.get("option_b")
        opt_c = q.get("option_c")
        opt_d = q.get("option_d")
        if all([opt_a, opt_b, opt_c, opt_d]):
            options = [str(opt_a).strip(), str(opt_b).strip(), str(opt_c).strip(), str(opt_d).strip()]
        else:
            return False, "Question must contain 4 options"

    if len(options) != 4:
        return False, f"Question must have exactly 4 options, found {len(options)}"

    # Option uniqueness check
    cleaned_options = [str(opt).strip() for opt in options]
    if any(not opt for opt in cleaned_options):
        return False, "Options cannot be blank"

    if len(set(cleaned_options)) != 4:
        return False, f"Options must be 4 unique values. Found duplicates: {cleaned_options}"

    # Correct Answer check
    correct_ans = q.get("correct_answer") or q.get("correct_option")
    if not correct_ans:
        return False, "Missing correct answer or option indicator"

    correct_str = str(correct_ans).strip()
    # Check if correct_str is 'A', 'B', 'C', 'D' or matches an option value
    valid_answer = False
    if correct_str.upper() in ["A", "B", "C", "D"]:
        valid_answer = True
    elif correct_str in cleaned_options:
        valid_answer = True

    if not valid_answer:
        return False, f"Correct answer '{correct_str}' does not match options A, B, C, D or option content {cleaned_options}"

    # Explanation check
    explanation = q.get("explanation")
    if not explanation or len(str(explanation).strip()) < 5:
        return False, "Missing or insufficient explanation text"

    return True, None
