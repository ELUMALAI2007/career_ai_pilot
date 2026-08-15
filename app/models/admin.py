"""
CareerPilot AI - Admin Models Module
Database models for system audit logs and platform notices.
"""

from datetime import datetime
from app import db


class AdminLog(db.Model):
    """Audit log records for admin administrative actions."""
    __tablename__ = 'admin_logs'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SystemNotice(db.Model):
    """System-wide platform announcements."""
    __tablename__ = 'system_notices'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
