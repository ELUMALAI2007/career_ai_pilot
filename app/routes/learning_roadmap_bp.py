"""
CareerPilot AI - Learning Roadmap Blueprint (`/roadmap`)
Controller for personalized preparation pathways and milestone trackers.
"""

from flask import Blueprint, render_template
from flask_login import login_required

learning_roadmap_bp = Blueprint('learning_roadmap', __name__)


@learning_roadmap_bp.route('/')
@login_required
def index():
    """Learning roadmap timeline view."""
    return render_template('learning_roadmap/index.html')
