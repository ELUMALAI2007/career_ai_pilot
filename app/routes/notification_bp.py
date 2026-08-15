"""
CareerPilot AI - Notification Blueprint (`/notifications`)
Controller for in-app alert notifications and activity feed.
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.services.notification_service import NotificationService

notification_bp = Blueprint('notification', __name__)


@notification_bp.route('/')
@login_required
def index():
    """In-app notifications feed."""
    notifications = NotificationService.get_unread_notifications(current_user.id)
    return render_template('notification/index.html', notifications=notifications)
