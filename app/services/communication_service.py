"""
CareerPilot AI - Communication Service
Evaluates spoken and written communication using NLP metrics and AI feedback.
"""

from app.models.communication import CommunicationAssessment
from app import db


class CommunicationService:
    """Service handling soft skills and communication analysis."""

    @staticmethod
    def analyze_text_communication(user_id: int, assessment_type: str, text_input: str) -> dict:
        """Analyzes written communication text for grammar, tone, and clarity."""
        # TODO: Process text with spaCy NLP and Gemini LLM feedback
        assessment = CommunicationAssessment(
            user_id=user_id,
            assessment_type=assessment_type,
            raw_input_text=text_input,
            clarity_score=8.5,
            grammar_score=9.0,
            confidence_score=8.0,
            feedback_notes="TODO: Communication analysis feedback notes."
        )
        db.session.add(assessment)
        db.session.commit()
        return {"clarity": 8.5, "grammar": 9.0, "confidence": 8.0}
