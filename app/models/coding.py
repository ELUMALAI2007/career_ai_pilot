"""
CareerPilot AI - Coding Models Module
Database models for DSA problems, code submission history, and test results.
"""

from datetime import datetime
from app import db


class CodingProblem(db.Model):
    """Coding & Data Structures problem definition."""
    __tablename__ = 'coding_problems'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    sample_input = db.Column(db.Text)
    sample_output = db.Column(db.Text)
    submissions = db.relationship('CodingSubmission', backref='problem', lazy='dynamic')


class CodingSubmission(db.Model):
    """User code submission execution record."""
    __tablename__ = 'coding_submissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('coding_problems.id'), nullable=False)
    language = db.Column(db.String(30), nullable=False)  # python, cpp, java
    code_body = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending')  # Accepted, Wrong Answer, Time Limit Exceeded
    execution_time_ms = db.Column(db.Float)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
