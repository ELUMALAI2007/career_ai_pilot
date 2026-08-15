"""
CareerPilot AI - Mock Interview Blueprint (`/interview`)
Controller for AI-powered mock technical and HR interview practice sessions.
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms.practice_forms import MockInterviewForm
from app.services.interview_service import InterviewService

interview_bp = Blueprint('interview', __name__)
interview_service = InterviewService()


@interview_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Mock interview lobby and setup view."""
    form = MockInterviewForm()
    if form.validate_on_submit():
        interview = interview_service.start_session(
            current_user.id,
            form.target_role.data,
            form.target_company.data,
            form.difficulty.data
        )
        flash('Mock Interview Session Started!', 'success')
        return redirect(url_for('interview.session', interview_id=interview.id))
        
    return render_template('interview/index.html', form=form)


@interview_bp.route('/session/<int:interview_id>')
@login_required
def session(interview_id):
    """Active mock interview session room."""
    return render_template('interview/index.html', interview_id=interview_id)
