"""
CareerPilot AI - Aptitude Bank Compatibility Wrapper
Re-exports load_question_bank from data.aptitude to preserve backwards compatibility.
"""

from data.aptitude import load_question_bank
from data.aptitude.quantitative import get_quantitative_questions
from data.aptitude.logical import get_logical_questions
from data.aptitude.verbal import get_verbal_questions

__all__ = [
    "load_question_bank",
    "get_quantitative_questions",
    "get_logical_questions",
    "get_verbal_questions",
]
