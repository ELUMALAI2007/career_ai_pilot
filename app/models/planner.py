"""
CareerPilot AI - Planner Models Module
Database models for placement preparation schedules, daily tasks, and study plans.
"""

from datetime import datetime
from app import db


class StudyPlan(db.Model):
    """Study preparation plan container."""
    __tablename__ = 'study_plans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    target_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship('StudyTask', backref='plan', lazy='dynamic', cascade='all, delete-orphan')


class StudyTask(db.Model):
    """Daily preparation item."""
    __tablename__ = 'study_tasks'

    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('study_plans.id'), nullable=False)
    task_name = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.DateTime)
    is_done = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default='medium')
