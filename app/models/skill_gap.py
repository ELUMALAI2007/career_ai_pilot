"""
CareerPilot AI - Skill Gap Models Module
Database models for target roles, required skills, and gap reports.
"""

from datetime import datetime
from app import db


class TargetRole(db.Model):
    """Industry role definition and required skill vector."""
    __tablename__ = 'target_roles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    required_skills = db.Column(db.Text, nullable=False)  # JSON or comma-separated string
    industry_demand_level = db.Column(db.String(30), default='High')


class SkillAssessment(db.Model):
    """User self-assessment or test-proven skill proficiency."""
    __tablename__ = 'skill_assessments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    proficiency_level = db.Column(db.String(30), default='Beginner')  # Beginner, Intermediate, Expert
    score = db.Column(db.Float, default=0.0)


class SkillGapReport(db.Model):
    """Generated skill gap assessment report."""
    __tablename__ = 'skill_gap_reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_role_id = db.Column(db.Integer, db.ForeignKey('target_roles.id'), nullable=False)
    match_percentage = db.Column(db.Float, default=0.0)
    missing_critical_skills = db.Column(db.Text)
    recommended_learning_actions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
