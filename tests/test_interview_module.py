"""Tests for the low-call, database-backed mock interview workflow."""

import json
from unittest.mock import Mock

import pytest

from app import create_app, db
from app.models.coding import CodingProblem
from app.models.interview import InterviewQuestion, InterviewSession, InterviewTurn
from app.models.resume import ResumeAnalysis, ResumeUpload
from app.models.user import User
from app.services.interview_service import InterviewService
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
def candidate(app_ctx):
    user = User(full_name="Candidate", email="candidate@test.com", status="approved")
    user.set_password("SecurePassword123!")
    db.session.add(user)
    db.session.commit()
    resume = ResumeUpload(user_id=user.id, filename="resume.pdf", file_path="/tmp/resume.pdf")
    db.session.add(resume)
    db.session.flush()
    db.session.add(ResumeAnalysis(
        resume_id=resume.id,
        parsed_data_json=json.dumps({"skills": ["Python", "SQL"], "projects": []})
    ))
    db.session.add_all([
        InterviewQuestion(question="Tell me about yourself.", role="Software Developer", interview_type="Introduction", difficulty="Medium", topic="About You"),
        InterviewQuestion(question="Walk me through your resume.", role="Software Developer", interview_type="Resume", difficulty="Medium", topic="Experience"),
        InterviewQuestion(question="Explain Python testing.", role="Software Developer", interview_type="Technical", difficulty="Medium", topic="Testing"),
        InterviewQuestion(question="Design a reliable API.", role="Software Developer", interview_type="Technical", difficulty="Medium", topic="Design"),
        InterviewQuestion(question="Describe a team conflict.", role="Software Developer", interview_type="HR", difficulty="Medium", topic="Collaboration"),
        InterviewQuestion(question="Tell me about a failure.", role="Software Developer", interview_type="Behavioral", difficulty="Medium", topic="Failure"),
    ])
    db.session.commit()
    return user, resume


def make_service(resume_questions=None, follow_up=None, final_report=None):
    service = InterviewService()
    service.ai.generate_resume_questions = Mock(return_value=resume_questions or [])
    service.ai.generate_follow_up = Mock(return_value=follow_up or {
        "question": "Can you give a concrete example?", "question_type": "Follow-up", "topic": "Clarification"
    })
    service.ai.generate_final_report = Mock(return_value=final_report or {
        "overall_score": 78, "dimension_scores": {"Communication": 78},
        "strengths": ["Clear examples"], "areas_for_improvement": ["Add metrics"],
        "recommended_improvements": ["Use STAR"], "per_question_feedback": []
    })
    return service


def create(service, user, resume, count=2, resume_based=False):
    return service.create_session(user.id, resume.id, "Software Developer", "Google", "Medium", "Technical", count, resume_based)


def test_resume_is_required(app_ctx, candidate):
    service = InterviewService()
    with pytest.raises(ValueError, match="valid resume"):
        service.create_session(candidate[0].id, 999, "Software Developer", "Google", "Medium", "Technical", 2, False)


def test_session_uses_bank_without_ai_for_default_questions(candidate):
    user, resume = candidate
    service = make_service()
    session = create(service, user, resume)
    assert InterviewTurn.query.filter_by(session_id=session.id).count() == 1
    assert len(session.get_question_queue()) == 1
    service.ai.generate_resume_questions.assert_not_called()


def test_resume_questions_use_one_call_at_start(candidate):
    user, resume = candidate
    service = make_service([{"question": "Walk through your Python project.", "question_type": "Resume"}])
    session = create(service, user, resume, resume_based=True)
    assert service.ai.generate_resume_questions.call_count == 1
    assert InterviewTurn.query.filter_by(session_id=session.id).first().question.startswith("Tell me about yourself.")
    queue_types = [item.get("question_type") for item in session.get_question_queue()]
    assert "Resume" in queue_types
    assert "Coding Challenge" in queue_types


def test_difficulty_drives_question_count_and_coding_checkpoint(candidate):
    user, resume = candidate
    CodingProblem.query.delete()
    db.session.add(CodingProblem(
        title="Two Sum",
        slug="two-sum",
        description="Given an array, return indices.",
        difficulty="easy",
        topic="Arrays",
        company_tags="Google",
        xp_reward=10,
    ))
    db.session.commit()

    service = make_service()
    session = service.create_session(user.id, resume.id, "Software Developer", "Google", "Easy", "Technical", 0, False)

    assert session.total_questions == 5
    assert len(session.get_question_queue()) + 1 == session.total_questions
    assert any(item.get("question_type") == "Coding Challenge" for item in session.get_question_queue())


def test_difficulty_count_map_uses_5_10_15_and_keeps_coding_challenge_in_total(candidate):
    user, resume = candidate
    CodingProblem.query.delete()
    db.session.add(CodingProblem(
        title="Two Sum",
        slug="two-sum",
        description="Given an array, return indices.",
        difficulty="easy",
        topic="Arrays",
        company_tags="Google",
        xp_reward=10,
    ))
    db.session.commit()

    service = make_service()
    easy_session = service.create_session(user.id, resume.id, "Software Developer", "Google", "Easy", "Technical", 0, False)
    medium_session = service.create_session(user.id, resume.id, "Software Developer", "Google", "Medium", "Technical", 0, False)
    hard_session = service.create_session(user.id, resume.id, "Software Developer", "Google", "Hard", "Technical", 0, False)

    assert easy_session.total_questions == 5
    assert medium_session.total_questions == 10
    assert hard_session.total_questions == 15
    assert len(easy_session.get_question_queue()) + 1 == easy_session.total_questions
    assert len(medium_session.get_question_queue()) + 1 == medium_session.total_questions
    assert len(hard_session.get_question_queue()) + 1 == hard_session.total_questions


def test_normal_answer_does_not_call_ai(candidate):
    user, resume = candidate
    service = make_service()
    session = create(service, user, resume)
    answer = "I used Python and SQL with automated testing, API monitoring, and a cache. The system was reviewed, measured, and improved through documented experiments and clear ownership across the delivery team."
    service.submit_answer(session.id, answer)
    service.ai.generate_follow_up.assert_not_called()


def test_short_answer_triggers_follow_up(candidate):
    user, resume = candidate
    service = make_service()
    session = create(service, user, resume)
    result = service.submit_answer(session.id, "I used Python.")
    assert result["next_question_type"] == "Follow-up"
    assert session.follow_up_count == 1
    service.ai.generate_follow_up.assert_called_once()


def test_follow_up_limit_is_three(candidate):
    user, resume = candidate
    service = make_service()
    session = create(service, user, resume, count=5)
    for _ in range(4):
        service.submit_answer(session.id, "Too short.")
    assert session.follow_up_count == 3
    assert service.ai.generate_follow_up.call_count == 3


def test_finalization_calls_report_once_and_rejects_resubmission(candidate):
    user, resume = candidate
    service = make_service()
    session = create(service, user, resume, count=1)
    result = service.submit_answer(session.id, "A complete answer about Python, SQL, API design, testing, and measurable system results.")
    assert result["is_finished"] is True
    assert session.status == "Completed"
    service.ai.generate_final_report.assert_called_once()
    with pytest.raises(ValueError, match="already been completed"):
        service.submit_answer(session.id, "Retry")


def test_queue_survives_interrupted_session(candidate):
    user, resume = candidate
    service = make_service()
    session = create(service, user, resume, count=2)
    session_id = session.id
    db.session.expire_all()
    restored = db.session.get(InterviewSession, session_id)
    assert len(restored.get_question_queue()) == 1
    assert restored.current_question_no == 1
