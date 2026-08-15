"""
CareerPilot AI - Company Prep Models Module
Database models for target companies, placement interview patterns, and peer experiences.
"""

from datetime import datetime
from app import db


class CompanyProfile(db.Model):
    """Target company profile info."""
    __tablename__ = 'company_profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    industry = db.Column(db.String(100))
    tier = db.Column(db.String(50))  # Tier 1, Tier 2, Startup, MNC
    overview = db.Column(db.Text)
    website = db.Column(db.String(255))
    patterns = db.relationship('PlacementPattern', backref='company', lazy='dynamic')
    experiences = db.relationship('InterviewExperience', backref='company', lazy='dynamic')


class PlacementPattern(db.Model):
    """Company recruitment round patterns and weighting."""
    __tablename__ = 'placement_patterns'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_profiles.id'), nullable=False)
    round_name = db.Column(db.String(100), nullable=False)  # Online Assessment, Technical Round 1, HR
    topic_focus = db.Column(db.String(255))
    cut_off_percentage = db.Column(db.Float)


class InterviewExperience(db.Model):
    """Peer shared interview experiences and insights."""
    __tablename__ = 'interview_experiences'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_profiles.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role_title = db.Column(db.String(100), nullable=False)
    verdict = db.Column(db.String(50), nullable=False)  # Selected, Rejected, Waitlisted
    experience_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
