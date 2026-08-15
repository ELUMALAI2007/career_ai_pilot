"""
CareerPilot AI - Planner Blueprint (`/planner`)
Controller for study preparation schedules and daily check-lists.
"""

from flask import Blueprint, render_template
from flask_login import login_required

planner_bp = Blueprint('planner', __name__)


@planner_bp.route('/')
@login_required
def index():
    """Daily study planner view."""
    return render_template('planner/index.html')
