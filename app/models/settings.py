"""
CareerPilot AI - Settings Models Module
Database models for user settings preferences and notification flags.
"""

from datetime import datetime
from app import db


class UserSettings(db.Model):
    """User preferences database table."""
    __tablename__ = 'user_settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    email_notifications = db.Column(db.Boolean, default=True)
    practice_reminders = db.Column(db.Boolean, default=True)
    ai_recommendation_alerts = db.Column(db.Boolean, default=True)
    theme_mode = db.Column(db.String(20), default='light')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
