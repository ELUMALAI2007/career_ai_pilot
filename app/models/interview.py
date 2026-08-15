"""
CareerPilot AI - Mock Interview Models Module
Database models for AI mock interview sessions, questions, and evaluation feedback.
"""

from datetime import datetime
from app import db


class MockInterview(db.Model):
    """Mock interview session instance."""
    __tablename__ = 'mock_interviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_role = db.Column(db.String(100), nullable=False)
    target_company = db.Column(db.String(150))
    difficulty = db.Column(db.String(30), default='medium')
    overall_score = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(30), default='In Progress')  # In Progress, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    questions = db.relationship('InterviewQuestion', backref='interview', lazy='dynamic', cascade='all, delete-orphan')


class InterviewQuestion(db.Model):
    """Individual question asked during mock interview session."""
    __tablename__ = 'interview_questions'

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('mock_interviews.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    user_answer = db.Column(db.Text)
    feedback = db.relationship('InterviewFeedback', backref='question', uselist=False, cascade='all, delete-orphan')


class InterviewFeedback(db.Model):
    """AI evaluation feedback per interview question."""
    __tablename__ = 'interview_feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('interview_questions.id'), nullable=False)
    technical_accuracy_score = db.Column(db.Float, default=0.0)
    communication_score = db.Column(db.Float, default=0.0)
    ai_suggestions = db.Column(db.Text)
    ideal_sample_answer = db.Column(db.Text)
