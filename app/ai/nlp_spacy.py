"""
CareerPilot AI - spaCy NLP Service Module
Performs Named Entity Recognition (NER), text extraction, and skill keyword mining.
"""

class NLPSpacyService:
    """Service wrapper for spaCy NLP pipeline operations."""

    def __init__(self, model_name: str = "en_core_web_sm"):
        self.model_name = model_name
        # TODO: Load spaCy pipeline model safely

    def extract_entities(self, text: str) -> dict:
        """
        Extracts named entities (organizations, skills, dates, education) from document text.
        """
        # TODO: Process text via spaCy doc and extract entities
        return {
            "organizations": ["TODO: Extracted Org"],
            "skills": ["TODO: Extracted Skill"],
            "education": ["TODO: Extracted Degree"]
        }

    def extract_keywords(self, text: str, top_n: int = 10) -> list:
        """
        Extracts key noun chunks and technical terms from raw text.
        """
        # TODO: Tokenize, filter stopwords/punct, and extract key phrases
        return ["TODO: Keyword 1", "TODO: Keyword 2"]
