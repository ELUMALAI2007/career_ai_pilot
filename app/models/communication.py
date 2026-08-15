"""
CareerPilot AI - Communication Models Module
Database models for verbal and written communication assessment logs.
"""

from datetime import datetime
from app import db


class CommunicationAssessment(db.Model):
    """Written and spoken soft skills evaluation record."""
    __tablename__ = 'communication_assessments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assessment_type = db.Column(db.String(50), nullable=False)  # 'writing', 'speech', 'email_etiquette'
    raw_input_text = db.Column(db.Text, nullable=False)
    clarity_score = db.Column(db.Float, default=0.0)
    grammar_score = db.Column(db.Float, default=0.0)
    confidence_score = db.Column(db.Float, default=0.0)
    feedback_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
