"""
CareerPilot AI - Job Eligibility Models Module
Database models for company criteria rules and student qualification matching.
"""

from datetime import datetime
from app import db


class JobRequirement(db.Model):
    """Job posting and hiring criteria."""
    __tablename__ = 'job_requirements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    min_cgpa = db.Column(db.Float, default=6.0)
    allowed_branches = db.Column(db.String(255))  # CSE, ECE, IT, MECH
    max_active_backlogs = db.Column(db.Integer, default=0)
    required_skills = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EligibilityCriteria(db.Model):
    """Calculated student job eligibility record."""
    __tablename__ = 'eligibility_criteria'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_requirements.id'), nullable=False)
    is_eligible = db.Column(db.Boolean, default=False)
    match_percentage = db.Column(db.Float, default=0.0)
    rejection_reasons = db.Column(db.Text)
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)
