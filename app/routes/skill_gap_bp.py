"""
CareerPilot AI - Skill Gap Blueprint (`/skill-gap`)
Controller for candidate skill assessment and missing competency discovery.
"""

from flask import Blueprint, render_template
from flask_login import login_required

skill_gap_bp = Blueprint('skill_gap', __name__)


@skill_gap_bp.route('/')
@login_required
def index():
    """Skill gap analysis hub."""
    return render_template('skill_gap/index.html')
