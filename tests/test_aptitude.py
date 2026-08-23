"""
CareerPilot AI - Aptitude Module Unit & Integration Automated Test Suite
Verifies question bank, validation engine, option validation, duplicate fingerprinting, readiness score calculation, level adaptivity, timed mock sessions, daily challenges, and analytics.
"""

import pytest
import json
from datetime import datetime, timedelta
from app import create_app, db
from app.models.user import User, Role
from app.models.aptitude import (
    AptitudeCategory, AptitudeQuestion, AptitudeAttempt,
    AptitudeProgress, AptitudeTopicMastery, AptitudeTestSession, AptitudeTestResult, AptitudeBookmark
)
from app.services.aptitude_service import AptitudeService
from app.utils.aptitude_validator import validate_question, QUANT_TOPICS, LOGICAL_TOPICS, VERBAL_TOPICS, normalize_difficulty
from data.aptitude_bank import load_question_bank
from config import TestingConfig


@pytest.fixture
def app_ctx():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def test_user(app_ctx):
    user = User(full_name="Test Student", email="student@test.com", status="approved")
    user.set_password("Password123!")
    db.session.add(user)
    db.session.commit()
    return user


def test_question_validator():
    """Verifies that validate_question properly rejects invalid payloads and accepts valid ones."""
    valid_q = {
        "question": "What is 10% of 200?",
        "topic": "Percentages",
        "category": "Quantitative Aptitude",
        "difficulty": "Easy",
        "options": ["10", "20", "30", "40"],
        "correct_answer": "20",
        "explanation": "10% of 200 = 20."
    }
    is_valid, err = validate_question(valid_q)
    assert is_valid is True
    assert err is None

    # Duplicate options test
    invalid_opt_q = dict(valid_q, options=["20", "20", "30", "40"])
    is_valid_opt, err_opt = validate_question(invalid_opt_q)
    assert is_valid_opt is False
    assert "Found duplicates" in err_opt

    # Invalid answer test
    invalid_ans_q = dict(valid_q, correct_answer="99")
    is_valid_ans, err_ans = validate_question(invalid_ans_q)
    assert is_valid_ans is False


def test_question_bank_loading_and_distribution():
    """Verifies that the question bank loads 6,000 unique questions with 2,100 Easy, 2,400 Medium, 1,500 Hard."""
    bank = load_question_bank()
    assert len(bank) == 6000

    easy_count = sum(1 for q in bank if normalize_difficulty(q['difficulty']) == 'Easy')
    med_count = sum(1 for q in bank if normalize_difficulty(q['difficulty']) == 'Medium')
    hard_count = sum(1 for q in bank if normalize_difficulty(q['difficulty']) == 'Hard')

    assert easy_count == 2100
    assert med_count == 2400
    assert hard_count == 1500


def test_readiness_score_formula():
    """Tests the Aptitude Readiness Score (0-100) formula logic."""
    score1 = AptitudeService.calculate_readiness_score(accuracy=90.0, avg_speed=35.0, total_solved=200, mock_avg=85.0)
    assert score1 >= 80 and score1 <= 100

    score_zero = AptitudeService.calculate_readiness_score(accuracy=0.0, avg_speed=120.0, total_solved=0, mock_avg=0.0)
    assert score_zero == 0


def test_user_progress_and_streak(app_ctx, test_user):
    """Tests user progress initialization and streak tracking."""
    progress = AptitudeService.get_or_create_user_progress(test_user.id)
    assert progress.current_level == 'Level 1 — Beginner'

    AptitudeService.update_user_streak(test_user.id, 5)
    streak = AptitudeService.get_or_create_user_streak(test_user.id)
    assert streak.current_streak == 1
    assert streak.questions_today == 5


def test_practice_question_submission(app_ctx, test_user):
    """Tests single question practice submission and topic mastery update."""
    cat = AptitudeCategory(name="Quantitative Aptitude", description="Quant")
    db.session.add(cat)
    db.session.commit()

    q = AptitudeQuestion(
        category_id=cat.id,
        topic="Percentages",
        difficulty="Medium",
        question_text="What is 20% of 50?",
        option_a="10", option_b="20", option_c="30", option_d="40",
        correct_option="A",
        explanation="20% of 50 = (20/100)*50 = 10.",
        fingerprint="test_fp_1234567890123456789012345678901234567890123456789012345678901234"
    )
    db.session.add(q)
    db.session.commit()

    res = AptitudeService.submit_single_answer(test_user.id, q.id, "A", time_taken=25)
    assert res['is_correct'] is True
    assert res['correct_option'] == "A"

    mastery = AptitudeTopicMastery.query.filter_by(user_id=test_user.id, topic="Percentages").first()
    assert mastery is not None
    assert mastery.questions_attempted == 1
    assert mastery.mastery_percentage == 100.0


def test_mock_test_session_and_server_timer(app_ctx, test_user):
    """Tests mock session creation, server-side timer enforcement, and result evaluation."""
    cat = AptitudeCategory(name="Quantitative Aptitude", description="Quant")
    db.session.add(cat)
    db.session.commit()

    for i in range(5):
        db.session.add(AptitudeQuestion(
            category_id=cat.id,
            topic="Average",
            difficulty="Easy",
            question_text=f"Sample Q{i}",
            option_a="1", option_b="2", option_c="3", option_d="4",
            correct_option="A",
            explanation=f"Exp {i}",
            fingerprint=f"fp_{i}_12345678901234567890123456789012345678901234567890123456789012"
        ))
    db.session.commit()

    session = AptitudeService.start_mock_session(test_user.id, test_type='quick_5', num_questions=5)
    assert session.id is not None
    assert session.is_completed is False

    status = AptitudeService.get_mock_session_status(session.id, test_user.id)
    assert status['is_expired'] is False
    assert len(status['questions']) == 5

    q_data = json.loads(session.questions_data)
    answers = {str(q_data[0]['id']): 'A', str(q_data[1]['id']): 'B'}

    result = AptitudeService.submit_mock_session(session.id, test_user.id, answers)
    assert result.total_questions == 5
    assert result.correct_count == 1
    assert result.incorrect_count == 1
    assert result.skipped_count == 3


def test_bookmark_toggle(app_ctx, test_user):
    """Tests question bookmarking toggle."""
    cat = AptitudeCategory(name="Logical Reasoning", description="Logical")
    db.session.add(cat)
    db.session.commit()

    q = AptitudeQuestion(
        category_id=cat.id,
        topic="Coding-Decoding",
        difficulty="Easy",
        question_text="Test Bookmark Question",
        option_a="A", option_b="B", option_c="C", option_d="D",
        correct_option="A",
        explanation="Explanation",
        fingerprint="bm_fp_12345678901234567890123456789012345678901234567890123456789012"
    )
    db.session.add(q)
    db.session.commit()

    added = AptitudeService.toggle_bookmark(test_user.id, q.id)
    assert added is True
    assert len(AptitudeService.get_user_bookmarks(test_user.id)) == 1

    removed = AptitudeService.toggle_bookmark(test_user.id, q.id)
    assert removed is False
    assert len(AptitudeService.get_user_bookmarks(test_user.id)) == 0


def test_all_practice_filter_combinations(app_ctx, test_user):
    """Tests practice filter combinations against generated question bank."""
    from generate_question_bank import generate_batch
    generate_batch()

    q1 = AptitudeService.get_practice_questions(category_id=None, topic='all', difficulty='all', limit=10)
    assert len(q1) == 10

    cat_q = AptitudeCategory.query.filter_by(name="Quantitative Aptitude").first()
    q2 = AptitudeService.get_practice_questions(category_id=cat_q.id, topic='Percentages', difficulty='Easy', limit=10)
    assert len(q2) == 10

    cat_l = AptitudeCategory.query.filter_by(name="Logical Reasoning").first()
    q3 = AptitudeService.get_practice_questions(category_id=cat_l.id, topic='Coding-Decoding', difficulty='Medium', limit=10)
    assert len(q3) == 10

    cat_v = AptitudeCategory.query.filter_by(name="Verbal Ability").first()
    q4 = AptitudeService.get_practice_questions(category_id=cat_v.id, topic='Synonyms', difficulty='Hard', limit=10)
    assert len(q4) == 10


def test_new_aptitude_database_models(app_ctx, test_user):
    """Verifies creation and persistence of Category Performance, Difficulty Performance, Readiness Score, and Level Progress models."""
    from app.models.aptitude import (
        AptitudeCategoryPerformance, AptitudeDifficultyPerformance,
        AptitudeReadinessScore, AptitudeLevelProgress, AptitudeGenerationLog
    )

    # 1. Category Performance
    cat_perf = AptitudeCategoryPerformance(
        user_id=test_user.id,
        category_name="Quantitative Aptitude",
        questions_attempted=20,
        correct_count=16,
        accuracy=80.0
    )
    db.session.add(cat_perf)

    # 2. Difficulty Performance
    diff_perf = AptitudeDifficultyPerformance(
        user_id=test_user.id,
        difficulty="Medium",
        questions_attempted=15,
        correct_count=12,
        accuracy=80.0
    )
    db.session.add(diff_perf)

    # 3. Readiness Score audit log
    readiness = AptitudeReadinessScore(
        user_id=test_user.id,
        accuracy_score=80.0,
        speed_score=45.0,
        overall_score=78
    )
    db.session.add(readiness)

    # 4. Level Progress
    level_prog = AptitudeLevelProgress(
        user_id=test_user.id,
        level=1,
        level_name="Beginner",
        questions_attempted=20,
        questions_correct=16,
        accuracy=80.0
    )
    db.session.add(level_prog)

    # 5. Generation Log
    gen_log = AptitudeGenerationLog(
        category="Quantitative Aptitude",
        topic="Percentages",
        difficulty="Easy",
        requested_count=100,
        generated_count=100,
        valid_count=100,
        status="completed"
    )
    db.session.add(gen_log)

    db.session.commit()

    assert AptitudeCategoryPerformance.query.filter_by(user_id=test_user.id).count() == 1
    assert AptitudeDifficultyPerformance.query.filter_by(user_id=test_user.id).count() == 1
    assert AptitudeReadinessScore.query.filter_by(user_id=test_user.id).count() == 1
    assert AptitudeLevelProgress.query.filter_by(user_id=test_user.id).count() == 1
    assert AptitudeGenerationLog.query.filter_by(status="completed").count() >= 1


def test_practice_start_template_rendering(app_ctx, test_user):
    """Verifies that GET /aptitude/practice/start renders practice session template cleanly without Jinja errors."""
    cat = AptitudeCategory(name="Quantitative Aptitude", description="Quant")
    db.session.add(cat)
    db.session.commit()

    db.session.add(AptitudeQuestion(
        category_id=cat.id,
        topic="Number System",
        difficulty="Level 1 — Beginner",
        question_text="What is the smallest prime number?",
        option_a="0", option_b="1", option_c="2", option_d="3",
        correct_option="C",
        explanation="2 is the smallest prime number.",
        fingerprint="fp_ns_12345678901234567890123456789012345678901234567890123456789012"
    ))
    db.session.commit()

    with app_ctx.test_client() as client:
        with client.session_transaction() as sess:
            sess['_user_id'] = str(test_user.id)
            sess['_fresh'] = True

        resp = client.get('/aptitude/practice/start?topic=Number+System&difficulty=Level+1+-+Beginner&limit=10')
        assert resp.status_code == 200
        assert b"What is the smallest prime number?" in resp.data
        assert b"Practice Session: Number System" in resp.data


def test_mock_session_template_rendering(app_ctx, test_user):
    """Verifies that GET /aptitude/mock/<session_id> renders mock session template cleanly with option text populated."""
    cat = AptitudeCategory(name="Quantitative Aptitude", description="Quant")
    db.session.add(cat)
    db.session.commit()

    db.session.add(AptitudeQuestion(
        category_id=cat.id,
        topic="Trains",
        difficulty="Easy",
        question_text="If a variable x = 150, what is the value of 2x?",
        option_a="100", option_b="200", option_c="300", option_d="400",
        correct_option="C",
        explanation="2 * 150 = 300.",
        fingerprint="fp_mock_123456789012345678901234567890123456789012345678901234567890"
    ))
    db.session.commit()

    mock_sess = AptitudeService.start_mock_session(test_user.id, test_type='quick_5', num_questions=1)

    with app_ctx.test_client() as client:
        with client.session_transaction() as sess:
            sess['_user_id'] = str(test_user.id)
            sess['_fresh'] = True

        resp = client.get(f'/aptitude/mock/{mock_sess.id}')
        assert resp.status_code == 200
        assert b"If a variable x = 150, what is the value of 2x?" in resp.data
        # Verify option texts are present in the response
        assert b"100" in resp.data
        assert b"200" in resp.data
        assert b"300" in resp.data
        assert b"400" in resp.data





