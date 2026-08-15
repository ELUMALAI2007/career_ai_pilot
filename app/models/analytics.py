"""
CareerPilot AI - Analytics Models Module
Database models for aggregated performance metrics and readiness snapshots.
"""

from datetime import datetime
from app import db


class UserAnalytics(db.Model):
    """User cumulative performance summary."""
    __tablename__ = 'user_analytics'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    aptitude_score_avg = db.Column(db.Float, default=0.0)
    coding_score_avg = db.Column(db.Float, default=0.0)
    interview_score_avg = db.Column(db.Float, default=0.0)
    readiness_percentage = db.Column(db.Float, default=0.0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MetricSnapshot(db.Model):
    """Historical timeline snapshots for Chart.js rendering."""
    __tablename__ = 'metric_snapshots'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    metric_type = db.Column(db.String(50), nullable=False)
    score_value = db.Column(db.Float, nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
