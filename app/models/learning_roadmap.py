"""
CareerPilot AI - Learning Roadmap Models Module
Database models for AI generated learning pathways and skill milestones.
"""

from datetime import datetime
from app import db


class Roadmap(db.Model):
    """Personalized learning roadmap structure."""
    __tablename__ = 'roadmaps'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    target_role = db.Column(db.String(100), nullable=False)
    total_weeks = db.Column(db.Integer, default=8)
    progress_percentage = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    milestones = db.relationship('RoadmapMilestone', backref='roadmap', lazy='dynamic', cascade='all, delete-orphan')


class RoadmapMilestone(db.Model):
    """Milestone step inside a learning roadmap."""
    __tablename__ = 'roadmap_milestones'

    id = db.Column(db.Integer, primary_key=True)
    roadmap_id = db.Column(db.Integer, db.ForeignKey('roadmaps.id'), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    recommended_resources = db.Column(db.Text)
    is_completed = db.Column(db.Boolean, default=False)
