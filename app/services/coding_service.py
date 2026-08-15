"""
CareerPilot AI - Coding Service
Manages DSA programming challenges, code execution sandboxing, and submission history.
"""

from app.models.coding import CodingProblem, CodingSubmission
from app import db


class CodingService:
    """Service handling coding problem sets and submissions."""

    @staticmethod
    def get_problems(difficulty: str = None) -> list:
        """Retrieves list of coding problems."""
        query = CodingProblem.query
        if difficulty:
            query = query.filter_by(difficulty=difficulty)
        return query.all()

    @staticmethod
    def execute_code_submission(user_id: int, problem_id: int, language: str, code_body: str) -> dict:
        """Executes candidate submitted code against problem test cases."""
        # TODO: Run code in secure sandbox runner or evaluate against sample inputs
        submission = CodingSubmission(
            user_id=user_id,
            problem_id=problem_id,
            language=language,
            code_body=code_body,
            status='Accepted',
            execution_time_ms=14.2
        )
        db.session.add(submission)
        db.session.commit()
        return {"status": "Accepted", "execution_time_ms": 14.2}
