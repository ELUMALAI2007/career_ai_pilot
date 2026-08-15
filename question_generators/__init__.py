"""
CareerPilot AI - Question Generators Package Registry
Unified registry for generating original placement questions across Quantitative, Logical Reasoning, and Verbal Ability topics.
"""

from typing import Dict, Any, List
from question_generators.quantitative.quant_generators import QuantGenerators
from question_generators.logical.logical_generators import LogicalGenerators
from question_generators.verbal.verbal_generators import VerbalGenerators

QUANT_TOPICS = [
    "Number System", "HCF and LCM", "Simplification", "Average", "Percentage",
    "Profit and Loss", "Simple Interest", "Compound Interest", "Ratio and Proportion",
    "Partnership", "Mixture and Alligation", "Time and Work", "Pipes and Cisterns",
    "Time, Speed and Distance", "Problems on Trains", "Boats and Streams",
    "Problems on Ages", "Permutation", "Combination", "Probability", "Algebra",
    "Geometry", "Mensuration", "Data Interpretation", "Clocks", "Calendars"
]

LOGICAL_TOPICS = [
    "Number Series", "Alphabet Series", "Coding-Decoding", "Blood Relations",
    "Direction Sense", "Ranking", "Linear Arrangement", "Circular Arrangement",
    "Seating Arrangement", "Puzzles", "Syllogism", "Statement and Conclusion",
    "Statement and Assumption", "Analogy", "Classification", "Data Sufficiency",
    "Venn Diagrams", "Missing Numbers", "Logical Sequence", "Non-Verbal Reasoning"
]

VERBAL_TOPICS = [
    "Vocabulary", "Synonyms", "Antonyms", "Sentence Completion", "Grammar",
    "Error Detection", "Sentence Correction", "Articles", "Prepositions", "Tenses",
    "Subject-Verb Agreement", "Active and Passive Voice", "Direct and Indirect Speech",
    "Para Jumbles", "Reading Comprehension", "Cloze Test", "One Word Substitution",
    "Idioms and Phrases"
]

DIFFICULTY_LEVELS = ["foundation", "beginner", "intermediate", "advanced", "expert", "master"]


def generate_question_for_topic(category: str, topic: str, difficulty: str = "intermediate") -> Dict[str, Any]:
    """Generates an original, validated question dictionary for a given category, topic, and difficulty level."""
    if category == "Quantitative Aptitude":
        return QuantGenerators.generate_by_topic(topic, difficulty)
    elif category == "Logical Reasoning":
        return LogicalGenerators.generate_by_topic(topic, difficulty)
    elif category == "Verbal Ability":
        return VerbalGenerators.generate_by_topic(topic, difficulty)
    else:
        # Fallback to Quant
        return QuantGenerators.generate_by_topic(topic, difficulty)
