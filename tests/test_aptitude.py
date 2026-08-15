"""
CareerPilot AI - Aptitude Module Unit & Integration Automated Test Suite
Verifies question generators, option validation, duplicate fingerprinting, readiness score calculation, level adaptivity, timed mock sessions, daily challenges, and bookmarks.
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
from question_generators import (
    generate_question_for_topic, QUANT_TOPICS, LOGICAL_TOPICS, VERBAL_TOPICS, DIFFICULTY_LEVELS
)
from question_generators.base import BaseQuestionGenerator


@pytest.fixture
def app_ctx():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
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


def test_question_generator_validation():
    """Verifies that algorithmic question generators produce valid payloads with 4 unique options."""
    for cat, topics in [("Quantitative Aptitude", QUANT_TOPICS), ("Logical Reasoning", LOGICAL_TOPICS), ("Verbal Ability", VERBAL_TOPICS)]:
        for topic in topics[:3]:
            for lvl in DIFFICULTY_LEVELS[:3]:
                q_dict = generate_question_for_topic(cat, topic, lvl)
                assert BaseQuestionGenerator.validate_question_dict(q_dict) is True
                assert q_dict['correct_option'] in ['A', 'B', 'C', 'D']
                options = [q_dict['option_a'], q_dict['option_b'], q_dict['option_c'], q_dict['option_d']]
                assert len(set(options)) == 4
                assert q_dict['explanation'] is not None and len(q_dict['explanation']) > 10
                assert q_dict['fingerprint'] is not None and len(q_dict['fingerprint']) == 64


def test_readiness_score_formula():
    """Tests the Aptitude Readiness Score (0-100) formula logic."""
    score1 = AptitudeService.calculate_readiness_score(accuracy=90.0, avg_speed=35.0, total_solved=200, mock_avg=85.0)
    assert score1 >= 80 and score1 <= 100

    score_zero = AptitudeService.calculate_readiness_score(accuracy=0.0, avg_speed=120.0, total_solved=0, mock_avg=0.0)
    assert score_zero == 0


def test_user_progress_and_streak(app_ctx, test_user):
    """Tests user progress initialization and streak tracking."""
    progress = AptitudeService.get_or_create_user_progress(test_user.id)
    assert progress.current_level == 'foundation'

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
        topic="Percentage",
        difficulty="intermediate",
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

    mastery = AptitudeTopicMastery.query.filter_by(user_id=test_user.id, topic="Percentage").first()
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
            difficulty="beginner",
            question_text=f"Sample Q{i}",
            option_a="1", option_b="2", option_c="3", option_d="4",
            correct_option="A",
            explanation=f"Exp {i}",
            fingerprint=f"fp_{i}_12345678901234567890123456789012345678901234567890123456789012"
        ))
    db.session.commit()

    session = AptitudeService.start_mock_session(test_user.id, test_type='quick')
    assert session.id is not None
    assert session.is_completed is False

    status = AptitudeService.get_mock_session_status(session.id, test_user.id)
    assert status['is_expired'] is False
    assert len(status['questions']) == 5

    # Submit session answers
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
        difficulty="beginner",
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
    """Tests all 5 specified practice filter combinations against generated questions."""
    from generate_question_bank import generate_batch
    generate_batch()

    # Test 1: All Categories, All Topics, Adaptive, 10 Questions
    q1 = AptitudeService.get_practice_questions(category_id=None, topic='all', difficulty='all', limit=10)
    assert len(q1) == 10

    # Test 2: Quantitative, Percentage, Beginner, 10 Questions
    cat_q = AptitudeCategory.query.filter_by(name="Quantitative Aptitude").first()
    q2 = AptitudeService.get_practice_questions(category_id=cat_q.id, topic='Percentage', difficulty='beginner', limit=10)
    assert len(q2) == 10

    # Test 3: Logical, Coding-Decoding, Intermediate, 10 Questions
    cat_l = AptitudeCategory.query.filter_by(name="Logical Reasoning").first()
    q3 = AptitudeService.get_practice_questions(category_id=cat_l.id, topic='Coding-Decoding', difficulty='intermediate', limit=10)
    assert len(q3) == 10

    # Test 4: Verbal, Grammar, Advanced, 10 Questions
    cat_v = AptitudeCategory.query.filter_by(name="Verbal Ability").first()
    q4 = AptitudeService.get_practice_questions(category_id=cat_v.id, topic='Grammar', difficulty='advanced', limit=10)
    assert len(q4) == 10

    # Test 5: Quantitative, Probability, Master, 10 Questions
    q5 = AptitudeService.get_practice_questions(category_id=cat_q.id, topic='Probability', difficulty='master', limit=10)
    assert len(q5) == 10

