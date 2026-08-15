"""
CareerPilot AI - Aptitude Blueprint (`/aptitude`)
Controller for Adaptive Aptitude Master, practice quizzes, timed mock examinations, learning hub, daily challenges, bookmarks, and analytics.
"""

import json
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.services.aptitude_service import AptitudeService
from app.models.aptitude import AptitudeCategory, AptitudeQuestion, AptitudeTestResult, AptitudeAttempt
from question_generators import QUANT_TOPICS, LOGICAL_TOPICS, VERBAL_TOPICS

aptitude_bp = Blueprint('aptitude', __name__)


@aptitude_bp.route('/')
@login_required
def index():
    """Adaptive Aptitude Master landing page / dashboard."""
    progress = AptitudeService.get_or_create_user_progress(current_user.id)
    streak = AptitudeService.get_or_create_user_streak(current_user.id)
    categories = AptitudeService.get_categories()
    
    # Calculate recommended topic based on lowest topic mastery
    analytics = AptitudeService.get_analytics_data(current_user.id)
    recommended_topic = "Percentage"
    if analytics["topic_labels"] and len(analytics["topic_labels"]) > 0:
        recommended_topic = analytics["topic_labels"][0]

    return render_template(
        'aptitude/index.html',
        progress=progress,
        streak=streak,
        categories=categories,
        recommended_topic=recommended_topic
    )


@aptitude_bp.route('/learn')
@login_required
def learn():
    """Dedicated Aptitude Learning Hub listing all 64 topics."""
    categories = AptitudeService.get_categories()
    topics_by_cat = {
        "Quantitative Aptitude": QUANT_TOPICS,
        "Logical Reasoning": LOGICAL_TOPICS,
        "Verbal Ability": VERBAL_TOPICS
    }
    return render_template('aptitude/learn.html', categories=categories, topics_by_cat=topics_by_cat)


@aptitude_bp.route('/topic/<path:topic_name>')
@login_required
def topic_detail(topic_name: str):
    """Dedicated topic learning page with concepts, formulas, shortcuts, and difficulty levels."""
    categories = AptitudeService.get_categories()

    # Determine category for topic
    cat_name = "Quantitative Aptitude"
    if topic_name in LOGICAL_TOPICS:
        cat_name = "Logical Reasoning"
    elif topic_name in VERBAL_TOPICS:
        cat_name = "Verbal Ability"

    cat_obj = AptitudeCategory.query.filter_by(name=cat_name).first()

    return render_template(
        'aptitude/topic_detail.html',
        topic_name=topic_name,
        category_name=cat_name,
        category=cat_obj,
        levels=AptitudeService.LEVELS
    )


@aptitude_bp.route('/practice')
@login_required
def practice():
    """Practice mode selector page."""
    categories = AptitudeService.get_categories()
    all_topics = QUANT_TOPICS + LOGICAL_TOPICS + VERBAL_TOPICS
    return render_template('aptitude/practice.html', categories=categories, all_topics=all_topics, levels=AptitudeService.LEVELS)


@aptitude_bp.route('/practice/start')
@login_required
def practice_start():
    """Launches an interactive practice set."""
    category_id = request.args.get('category_id', type=int)
    topic = request.args.get('topic', default='all')
    difficulty = request.args.get('difficulty', default='all')
    limit = request.args.get('limit', default=10, type=int)

    questions = AptitudeService.get_practice_questions(category_id=category_id, topic=topic, difficulty=difficulty, limit=limit)
    
    if not questions:
        flash("No questions found for the selected criteria. Try adjusting filters.", "warning")
        return redirect(url_for('aptitude.practice'))

    user_bookmarks = [b.id for b in AptitudeService.get_user_bookmarks(current_user.id)]

    return render_template(
        'aptitude/practice_session.html',
        questions=questions,
        topic=topic,
        difficulty=difficulty,
        user_bookmarks=user_bookmarks
    )


@aptitude_bp.route('/practice/submit-question', methods=['POST'])
@login_required
def practice_submit_question():
    """AJAX endpoint to submit a single answer in practice mode."""
    data = request.get_json() or {}
    question_id = data.get('question_id')
    selected_option = data.get('selected_option')
    time_taken = data.get('time_taken', 0)

    if not question_id or not selected_option:
        return jsonify({"error": "Missing parameters"}), 400

    res = AptitudeService.submit_single_answer(current_user.id, int(question_id), str(selected_option), int(time_taken))
    return jsonify(res)


@aptitude_bp.route('/practice-for-me')
@login_required
def practice_for_me():
    """Launches personalized practice set auto-weighted toward weak areas."""
    questions = AptitudeService.get_personalized_practice(current_user.id, limit=15)
    user_bookmarks = [b.id for b in AptitudeService.get_user_bookmarks(current_user.id)]

    return render_template(
        'aptitude/practice_session.html',
        questions=questions,
        topic="Personalized Weak Topics",
        difficulty="Adaptive",
        user_bookmarks=user_bookmarks
    )


@aptitude_bp.route('/mock')
@login_required
def mock_hub():
    """Timed Mock Examination Hub."""
    return render_template('aptitude/mock.html')


@aptitude_bp.route('/mock/start', methods=['GET', 'POST'])
@login_required
def mock_start():
    """Launches a timed mock test session with server-side timer enforcement."""
    test_type = request.args.get('type') or request.form.get('type') or 'standard'
    company_name = request.args.get('company') or request.form.get('company')
    
    title = f"{company_name.title()} Pattern Mock" if company_name else None
    session = AptitudeService.start_mock_session(current_user.id, test_type=test_type, custom_title=title)
    return redirect(url_for('aptitude.mock_session', session_id=session.id))


@aptitude_bp.route('/mock/<session_id>')
@login_required
def mock_session(session_id: str):
    """Timed Mock Test Examination UI."""
    data = AptitudeService.get_mock_session_status(session_id, current_user.id)
    if not data:
        flash("Mock test session not found or unauthorized.", "danger")
        return redirect(url_for('aptitude.mock_hub'))

    if data['session'].is_completed:
        res = AptitudeTestResult.query.filter_by(session_id=session_id).first()
        if res:
            return redirect(url_for('aptitude.mock_result', result_id=res.id))

    return render_template(
        'aptitude/mock_session.html',
        session=data['session'],
        questions=data['questions'],
        answers=data['answers'],
        remaining_seconds=data['remaining_seconds']
    )


@aptitude_bp.route('/mock/<session_id>/submit', methods=['POST'])
@login_required
def mock_submit(session_id: str):
    """Submits timed mock test and compiles results."""
    user_answers_raw = request.form.get('answers_json') or '{}'
    try:
        user_answers = json.loads(user_answers_raw)
    except Exception:
        user_answers = {}

    try:
        result = AptitudeService.submit_mock_session(session_id, current_user.id, user_answers)
        flash("Mock test completed successfully!", "success")
        return redirect(url_for('aptitude.mock_result', result_id=result.id))
    except Exception as e:
        flash(f"Error submitting test: {str(e)}", "danger")
        return redirect(url_for('aptitude.mock_hub'))


@aptitude_bp.route('/result/<int:result_id>')
@login_required
def mock_result(result_id: int):
    """Mock test result summary and topic feedback."""
    res = db.session.get(AptitudeTestResult, result_id)
    if not res or res.user_id != current_user.id:
        flash("Result record not found.", "danger")
        return redirect(url_for('aptitude.mock_hub'))

    cat_scores = json.loads(res.category_scores_json or '{}')
    strong_topics = json.loads(res.strong_topics_json or '[]')
    weak_topics = json.loads(res.weak_topics_json or '[]')

    return render_template(
        'aptitude/mock_result.html',
        result=res,
        cat_scores=cat_scores,
        strong_topics=strong_topics,
        weak_topics=weak_topics
    )


@aptitude_bp.route('/daily-challenge')
@login_required
def daily_challenge():
    """Daily 10 Challenge UI."""
    data = AptitudeService.get_daily_challenge(current_user.id)
    return render_template('aptitude/daily_challenge.html', challenge=data['challenge'], questions=data['questions'], attempt=data['attempt'])


@aptitude_bp.route('/daily-challenge/submit', methods=['POST'])
@login_required
def daily_challenge_submit():
    """Submits Daily 10 Challenge answers."""
    data = AptitudeService.get_daily_challenge(current_user.id)
    questions = data['questions']
    challenge = data['challenge']

    correct = 0
    for q in questions:
        q_id = str(q['id'])
        ans = request.form.get(f"q_{q_id}")
        q_obj = db.session.get(AptitudeQuestion, q['id'])
        if ans and q_obj and ans.upper() == q_obj.correct_option.upper():
            correct += 1

    acc = round((correct / len(questions) * 100.0), 1) if questions else 0.0

    attempt = AptitudeService.AptitudeDailyChallengeAttempt(
        user_id=current_user.id,
        challenge_id=challenge.id,
        score=correct,
        accuracy_percentage=acc
    )
    db.session.add(attempt)
    db.session.commit()

    AptitudeService.update_user_streak(current_user.id, len(questions))
    flash(f"Daily Challenge Completed! Score: {correct}/{len(questions)} ({acc}%)", "success")
    return redirect(url_for('aptitude.daily_challenge'))


@aptitude_bp.route('/bookmark/toggle', methods=['POST'])
@login_required
def bookmark_toggle():
    """AJAX endpoint to toggle question bookmark."""
    data = request.get_json() or {}
    question_id = data.get('question_id')
    if not question_id:
        return jsonify({"error": "Missing question_id"}), 400

    is_bookmarked = AptitudeService.toggle_bookmark(current_user.id, int(question_id))
    return jsonify({"bookmarked": is_bookmarked})


@aptitude_bp.route('/bookmarks')
@login_required
def bookmarks():
    """User bookmarked questions view."""
    bms = AptitudeService.get_user_bookmarks(current_user.id)
    return render_template('aptitude/bookmarks.html', questions=bms)


@aptitude_bp.route('/history')
@login_required
def history():
    """User attempt history & test results."""
    attempts = AptitudeAttempt.query.filter_by(user_id=current_user.id).order_by(AptitudeAttempt.completed_at.desc()).limit(20).all()
    results = AptitudeTestResult.query.filter_by(user_id=current_user.id).order_by(AptitudeTestResult.completed_at.desc()).limit(20).all()
    return render_template('aptitude/history.html', attempts=attempts, results=results)


@aptitude_bp.route('/analytics')
@login_required
def analytics():
    """Aptitude analytics dashboard with Chart.js visualization."""
    data = AptitudeService.get_analytics_data(current_user.id)
    return render_template('aptitude/analytics.html', analytics=data)


@aptitude_bp.route('/company-mock/<company_name>')
@login_required
def company_mock(company_name: str):
    """Company pattern-inspired practice mock."""
    session = AptitudeService.start_mock_session(current_user.id, test_type=company_name.lower(), custom_title=f"{company_name.title()}-Pattern Practice Mock")
    return redirect(url_for('aptitude.mock_session', session_id=session.id))
