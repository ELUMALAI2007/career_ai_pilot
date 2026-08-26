"""
CareerPilot AI - Mock Interview Models Module
Database models for AI mock interview sessions, dynamic turns, and evaluations.
"""

from datetime import datetime
import json
from app import db


class InterviewSession(db.Model):
    """Mock interview session instance capturing configuration, status, and final feedback."""
    __tablename__ = 'interview_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume_uploads.id'), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    interview_type = db.Column(db.String(50), nullable=False)  # 'Technical', 'HR / Behavioral', 'Mixed'
    difficulty = db.Column(db.String(30), default='Medium')      # 'Easy', 'Medium', 'Hard'
    company = db.Column(db.String(150))
    total_questions = db.Column(db.Integer, default=10)
    current_question_no = db.Column(db.Integer, default=1)
    resume_based_questions = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(30), default='In Progress')    # 'In Progress', 'Completed'
    overall_score = db.Column(db.Float, default=0.0)
    final_feedback = db.Column(db.Text)                         # JSON encoded string of overall feedback
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    # Relationships
    turns = db.relationship('InterviewTurn', backref='session', lazy='dynamic', cascade='all, delete-orphan')

    def get_final_feedback(self) -> dict:
        """Helper getter for deserializing final feedback JSON."""
        return json.loads(self.final_feedback) if self.final_feedback else {}

    def set_final_feedback(self, data: dict):
        """Helper setter for serializing final feedback JSON."""
        self.final_feedback = json.dumps(data)


class InterviewTurn(db.Model):
    """Individual question and answer turn in a mock interview session."""
    __tablename__ = 'interview_turns'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('interview_sessions.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    candidate_answer = db.Column(db.Text)
    question_type = db.Column(db.String(50))                    # 'Technical', 'Behavioral', 'Resume', 'Follow-up', 'HR'
    sequence_number = db.Column(db.Integer, nullable=False)
    evaluation = db.Column(db.Text)                             # JSON encoded evaluation feedback
    scores = db.Column(db.Text)                                 # JSON encoded score dimensions (0-10 scale)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def get_evaluation(self) -> dict:
        """Helper getter for deserializing turn evaluation JSON."""
        return json.loads(self.evaluation) if self.evaluation else {}

    def set_evaluation(self, data: dict):
        """Helper setter for serializing turn evaluation JSON."""
        self.evaluation = json.dumps(data)

    def get_scores(self) -> dict:
        """Helper getter for deserializing turn scores JSON."""
        return json.loads(self.scores) if self.scores else {}

    def set_scores(self, data: dict):
        """Helper setter for serializing turn scores JSON."""
        self.scores = json.dumps(data)
