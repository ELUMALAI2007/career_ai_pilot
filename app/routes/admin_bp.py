"""
CareerPilot AI - Admin Blueprint (`/admin`)
Controller for administrative management views and platform logs.
"""

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.services.admin_service import AdminService
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@login_required
@admin_required
def index():
    """Admin dashboard landing view."""
    stats = AdminService.get_system_stats()
    return render_template('admin/index.html', stats=stats)


@admin_bp.route('/requests')
@login_required
@admin_required
def requests():
    """Admin Access Requests management view."""
    status_filter = request.args.get('status', 'pending')
    search_query = request.args.get('q', '')
    
    user_requests = AdminService.get_user_requests(status_filter=status_filter, search_query=search_query)
    counts = AdminService.get_request_counts()
    
    return render_template(
        'admin/requests.html',
        user_requests=user_requests,
        counts=counts,
        current_status=status_filter,
        search_query=search_query
    )


@admin_bp.route('/requests/<int:user_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_user(user_id):
    """Approves a candidate access request."""
    user = AdminService.update_user_status(current_user.id, user_id, 'approved')
    if user:
        flash(f'Successfully approved candidate access for {user.email}. Confirmation email sent.', 'success')
    else:
        flash('Candidate record not found.', 'danger')
    return redirect(url_for('admin.requests', status=request.args.get('redirect_status', 'pending')))


@admin_bp.route('/requests/<int:user_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_user(user_id):
    """Rejects a candidate access request."""
    user = AdminService.update_user_status(current_user.id, user_id, 'rejected')
    if user:
        flash(f'Rejected access request for {user.email}.', 'warning')
    else:
        flash('Candidate record not found.', 'danger')
    return redirect(url_for('admin.requests', status=request.args.get('redirect_status', 'pending')))


@admin_bp.route('/aptitude/questions')
@login_required
@admin_required
def aptitude_questions():
    """Admin view for managing aptitude questions."""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '')
    category_id = request.args.get('category_id', type=int)
    topic = request.args.get('topic', '')
    difficulty = request.args.get('difficulty', '')

    pagination = AdminService.get_aptitude_questions(
        search_query=search_query,
        category_id=category_id,
        topic=topic,
        difficulty=difficulty,
        page=page,
        per_page=15
    )
    from app.models.aptitude import AptitudeCategory
    categories = AptitudeCategory.query.all()

    return render_template(
        'admin/aptitude_questions.html',
        pagination=pagination,
        categories=categories,
        search_query=search_query,
        category_id=category_id,
        topic=topic,
        difficulty=difficulty
    )


@admin_bp.route('/aptitude/generate-batch', methods=['POST'])
@login_required
@admin_required
def generate_batch_route():
    """Triggers question bank batch generation."""
    try:
        from generate_question_bank import generate_batch
        generate_batch()
        flash("Batch question generation completed successfully!", "success")
    except Exception as e:
        flash(f"Error during batch generation: {str(e)}", "danger")
    return redirect(url_for('admin.aptitude_questions'))

