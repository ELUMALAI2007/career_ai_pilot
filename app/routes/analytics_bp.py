"""
CareerPilot AI - Analytics Blueprint (`/analytics`)
Controller for candidate performance charts and readiness metrics.
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.services.analytics_service import AnalyticsService

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/')
@login_required
def index():
    """Performance Analytics Dashboard."""
    summary = AnalyticsService.get_user_analytics_summary(current_user.id)
    return render_template('analytics/index.html', summary=summary)
