"""
CareerPilot AI - Notification Models Module
Database models for in-app user notifications and system alerts.
"""

from datetime import datetime
from app import db


class Notification(db.Model):
    """In-app alert notification."""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(30), default='info')  # info, warning, success, reminder
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
