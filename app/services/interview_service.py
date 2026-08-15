"""
CareerPilot AI - Interview Service
Orchestrates AI mock interview generation, candidate answer evaluation, and scoring.
"""

from app.models.interview import MockInterview, InterviewQuestion, InterviewFeedback
from app.ai.gemini_service import GeminiService
from app import db


class InterviewService:
    """Service handling mock interview sessions."""

    def __init__(self):
        self.gemini = GeminiService()

    def start_session(self, user_id: int, target_role: str, target_company: str, difficulty: str) -> MockInterview:
        """Creates a new mock interview session with generated AI questions."""
        interview = MockInterview(
            user_id=user_id,
            target_role=target_role,
            target_company=target_company,
            difficulty=difficulty
        )
        db.session.add(interview)
        db.session.commit()

        # Generate questions via Gemini AI
        ai_questions = self.gemini.generate_interview_questions(target_role, target_company, difficulty)
        for q_item in ai_questions:
            q = InterviewQuestion(interview_id=interview.id, question_text=q_item["question"])
            db.session.add(q)

        db.session.commit()
        return interview
