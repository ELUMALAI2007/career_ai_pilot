"""
CareerPilot AI - Coding Blueprint (`/coding`)
Controller for Data Structures and Algorithm coding challenges, Monaco Editor IDE,
test evaluation, submissions history, leaderboard, and REST API endpoints.
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.coding_service import CodingService

coding_bp = Blueprint('coding', __name__)
coding_service = CodingService()


@coding_bp.route('/')
@login_required
def index():
    """Coding problems library and dashboard view."""
    topic = request.args.get('topic', 'all')
    difficulty = request.args.get('difficulty', 'all')
    company = request.args.get('company', 'all')
    status = request.args.get('status', 'all')
    search = request.args.get('search', '').strip()

    problems = coding_service.get_problems(
        topic=topic,
        difficulty=difficulty,
        company=company,
        status=status,
        search=search,
        user_id=current_user.id
    )

    user_progress = coding_service.get_user_progress(current_user.id)
    daily_challenge = coding_service.get_daily_challenge(current_user.id)
    top_coders = coding_service.get_leaderboard(limit=5)

    # Unique topics and companies for filter dropdowns
    available_topics = [
        "Arrays", "Strings", "Binary Search", "Stack", "Linked Lists",
        "Two Pointers", "Sorting", "Graphs", "Dynamic Programming"
    ]
    available_companies = [
        "Amazon", "Google", "Microsoft", "Meta", "Apple",
        "Bloomberg", "Goldman Sachs", "Adobe", "LinkedIn"
    ]

    return render_template(
        'coding/index.html',
        problems=problems,
        user_progress=user_progress,
        daily_challenge=daily_challenge,
        top_coders=top_coders,
        selected_topic=topic,
        selected_difficulty=difficulty,
        selected_company=company,
        selected_status=status,
        search_query=search,
        available_topics=available_topics,
        available_companies=available_companies
    )


@coding_bp.route('/<slug>')
@login_required
def problem_detail(slug):
    """Problem-solving workspace view with Monaco Editor."""
    problem = coding_service.get_problem_by_slug(slug, user_id=current_user.id)
    if not problem:
        flash(f"Problem '{slug}' was not found.", "warning")
        return redirect(url_for('coding.index'))

    # Retrieve user's previous submissions for this problem
    submissions = coding_service.get_user_submissions(
        user_id=current_user.id,
        problem_id=problem['id'],
        limit=10
    )

    return render_template(
        'coding/problem.html',
        problem=problem,
        submissions=submissions
    )


@coding_bp.route('/submissions')
@login_required
def submissions():
    """Overall candidate submissions history view."""
    all_submissions = coding_service.get_user_submissions(
        user_id=current_user.id,
        limit=100
    )
    user_progress = coding_service.get_user_progress(current_user.id)

    return render_template(
        'coding/submissions.html',
        submissions=all_submissions,
        user_progress=user_progress
    )


@coding_bp.route('/leaderboard')
@login_required
def leaderboard():
    """Gamification ranking leaderboard view."""
    top_coders = coding_service.get_leaderboard(limit=50)
    user_progress = coding_service.get_user_progress(current_user.id)

    return render_template(
        'coding/leaderboard.html',
        top_coders=top_coders,
        user_progress=user_progress
    )


# =========================================================================
# REST API ENDPOINTS
# =========================================================================

@coding_bp.route('/api/run', methods=['POST'])
@login_required
def api_run_code():
    """
    Executes code against sample test cases or custom input.
    Payload: { "slug": str, "language": str, "code": str, "custom_input": Optional[str] }
    """
    data = request.get_json(silent=True) or {}
    slug = data.get('slug', '').strip()
    language = data.get('language', 'python').strip()
    code = data.get('code', '').strip()
    custom_input = data.get('custom_input', None)

    if not slug or not code:
        return jsonify({'error': 'Problem slug and source code are required.'}), 400

    result = coding_service.run_code(
        problem_slug=slug,
        language=language,
        code_body=code,
        custom_input=custom_input
    )
    return jsonify(result)


@coding_bp.route('/api/submit', methods=['POST'])
@login_required
def api_submit_solution():
    """
    Grades solution against the full test suite (sample + hidden) and persists submission record.
    Payload: { "slug": str, "language": str, "code": str }
    """
    data = request.get_json(silent=True) or {}
    slug = data.get('slug', '').strip()
    language = data.get('language', 'python').strip()
    code = data.get('code', '').strip()

    if not slug or not code:
        return jsonify({'error': 'Problem slug and source code are required.'}), 400

    result = coding_service.submit_solution(
        user_id=current_user.id,
        problem_slug=slug,
        language=language,
        code_body=code
    )
    return jsonify(result)


@coding_bp.route('/api/bookmark', methods=['POST'])
@login_required
def api_toggle_bookmark():
    """
    Toggles bookmark status for a problem.
    Payload: { "problem_id": int }
    """
    data = request.get_json(silent=True) or {}
    problem_id = data.get('problem_id')

    if not problem_id:
        return jsonify({'error': 'Problem ID is required.'}), 400

    is_bookmarked = coding_service.toggle_bookmark(current_user.id, problem_id)
    return jsonify({'is_bookmarked': is_bookmarked})


@coding_bp.route('/api/reset', methods=['POST'])
@login_required
def api_reset_starter_code():
    """
    Returns the pristine starter code template for a specific problem and language.
    Payload: { "slug": str, "language": str }
    """
    data = request.get_json(silent=True) or {}
    slug = data.get('slug', '').strip()
    language = data.get('language', 'python').strip().lower()

    problem = coding_service.get_problem_by_slug(slug)
    if not problem:
        return jsonify({'error': 'Problem not found.'}), 404

    templates = problem.get('starter_templates', {})
    starter_code = templates.get(language, '')

    return jsonify({'language': language, 'starter_code': starter_code})


@coding_bp.route('/api/proctor/penalty', methods=['POST'])
@login_required
def api_proctor_penalty():
    """Deducts user XP points due to a proctoring violation."""
    result = coding_service.deduct_proctor_penalty(current_user.id, penalty_xp=50)
    return jsonify(result)


@coding_bp.route('/api/problems', methods=['GET'])
@login_required
def api_get_problems():
    """Returns JSON list of problems with optional filtering."""
    topic = request.args.get('topic', 'all')
    difficulty = request.args.get('difficulty', 'all')
    company = request.args.get('company', 'all')
    status = request.args.get('status', 'all')
    search = request.args.get('search', '').strip()

    problems = coding_service.get_problems(
        topic=topic,
        difficulty=difficulty,
        company=company,
        status=status,
        search=search,
        user_id=current_user.id
    )
    return jsonify({'problems': problems})


@coding_bp.route('/api/submissions', methods=['GET'])
@login_required
def api_get_submissions():
    """Returns JSON list of user submissions."""
    problem_id = request.args.get('problem_id', type=int)
    limit = request.args.get('limit', default=20, type=int)

    subs = coding_service.get_user_submissions(
        user_id=current_user.id,
        problem_id=problem_id,
        limit=limit
    )
    return jsonify({'submissions': subs})


@coding_bp.route('/api/stats', methods=['GET'])
@login_required
def api_get_stats():
    """Returns JSON progress metrics and topic mastery stats."""
    progress = coding_service.get_user_progress(current_user.id)
    return jsonify(progress)
