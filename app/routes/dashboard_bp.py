"""
CareerPilot AI - Dashboard Blueprint (`/dashboard`)
Main candidate dashboard controller displaying readiness metrics and study highlights.
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.services.dashboard_service import DashboardService

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    """Main Candidate Dashboard View."""
    summary = DashboardService.get_dashboard_summary(current_user.id)
    return render_template('dashboard/index.html', summary=summary)
