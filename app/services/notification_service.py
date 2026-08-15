"""
CareerPilot AI - Notification Service
Manages in-app user notifications, system alerts, and notification state.
"""

from app.models.notification import Notification
from app import db


class NotificationService:
    """Service handling notification dispatch and retrieval."""

    @staticmethod
    def send_notification(user_id: int, title: str, message: str, category: str = 'info') -> Notification:
        """Dispatches an in-app notification to a candidate."""
        notif = Notification(user_id=user_id, title=title, message=message, category=category)
        db.session.add(notif)
        db.session.commit()
        return notif

    @staticmethod
    def get_unread_notifications(user_id: int) -> list:
        """Retrieves all unread notifications for user."""
        return Notification.query.filter_by(user_id=user_id, is_read=False).order_by(Notification.created_at.desc()).all()
