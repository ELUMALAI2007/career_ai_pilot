"""
CareerPilot AI - Mock Interview Module Automated Test Suite
Verifies interview setup, resume validations, session lifecycles, turn processing, and AI mock scoring.
"""

import json
from unittest.mock import patch
import pytest
from app import db, create_app
from app.models.user import User
from app.models.resume import ResumeUpload, ResumeAnalysis
from app.models.interview import InterviewSession, InterviewTurn
from app.services.interview_service import InterviewService


@pytest.fixture
def app_ctx():
    """Configures in-memory test database and mock context."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def test_user(app_ctx):
    """Seeds candidate account."""
    user = User(full_name="Interviewer Candidate", email="candidate@test.com", status="approved")
    user.set_password("SecurePassword123!")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def test_resume(test_user):
    """Seeds candidate resume details."""
    upload = ResumeUpload(
        user_id=test_user.id,
        filename="resume.pdf",
        file_path="/fake/resume.pdf",
        target_role="Software Developer",
        target_company="Google"
    )
    db.session.add(upload)
    db.session.commit()

    analysis = ResumeAnalysis(
        resume_id=upload.id,
        overall_score=80.0,
        parsed_data_json=json.dumps({
            "skills": ["Python", "Flask", "SQLAlchemy"],
            "experience": [
                {"role": "Intern", "company": "Tech Inc", "highlights": ["Built backend APIs"]}
            ],
            "projects": [
                {"name": "Recommendation Engine", "technologies": ["Python", "Pandas"], "description": "Built a system"}
            ]
        })
    )
    db.session.add(analysis)
    db.session.commit()
    return upload


@patch('app.ai.openrouter_service.OpenRouterService._call_openrouter')
def test_interview_service_lifecycle_flow(mock_call_openrouter, test_user, test_resume):
    """Tests Mock Interview creation, response updates, next turn follow-up flow, and final report scorecard generation."""
    # 1. Mock first question call
    mock_call_openrouter.return_value = json.dumps({
        "question": "Tell me about your Python project.",
        "question_type": "Resume"
    })

    service = InterviewService()

    # Test Session Creation
    session = service.create_session(
        user_id=test_user.id,
        resume_id=test_resume.id,
        role="Software Developer",
        company="Google",
        difficulty="Medium",
        interview_type="Technical",
        total_questions=2,
        resume_based_questions=True
    )

    assert session.id is not None
    assert session.role == "Software Developer"
    assert session.company == "Google"
    assert session.difficulty == "Medium"
    assert session.total_questions == 2
    assert session.current_question_no == 1
    assert session.resume_based_questions is True
    assert session.status == 'In Progress'

    # Check first turn details
    turns = InterviewTurn.query.filter_by(session_id=session.id).all()
    assert len(turns) == 1
    assert turns[0].question == "Tell me about your Python project."
    assert turns[0].question_type == "Resume"
    assert turns[0].sequence_number == 1
    assert turns[0].candidate_answer is None

    # 2. Mock evaluation and next question call (turn 1 answer submission)
    mock_call_openrouter.return_value = json.dumps({
        "evaluation": {
            "what_went_well": "Clear explanation of Python skills.",
            "areas_for_improvement": "Elaborate more on the architecture."
        },
        "scores": {
            "Knowledge of Claimed Skill": 8,
            "Technical Understanding": 9,
            "Accuracy": 8,
            "Specificity": 7,
            "Communication": 8
        },
        "follow_up_required": True,
        "next_question": "What databases did you use with Flask?",
        "next_question_type": "Follow-up"
    })

    # Test Submit Answer (turn 1)
    res = service.submit_answer(session.id, "I developed a recommendation engine using Python and Pandas.")
    assert res["success"] is True
    assert res["is_finished"] is False
    assert res["next_question"] == "What databases did you use with Flask?"

    # Check turn 1 database updates
    turn1 = InterviewTurn.query.filter_by(session_id=session.id, sequence_number=1).first()
    assert turn1.candidate_answer == "I developed a recommendation engine using Python and Pandas."
    assert turn1.get_scores()["Knowledge of Claimed Skill"] == 8
    assert turn1.get_evaluation()["what_went_well"] == "Clear explanation of Python skills."

    # Validate progress increment
    assert session.current_question_no == 2

    # Check turn 2 record initialized
    turn2 = InterviewTurn.query.filter_by(session_id=session.id, sequence_number=2).first()
    assert turn2.question == "What databases did you use with Flask?"
    assert turn2.question_type == "Follow-up"
    assert turn2.candidate_answer is None

    # 3. Mock final turn submission and final feedback scorecard compiler
    mock_call_openrouter.side_effect = [
        # Call for submit_answer (Turn 2 evaluation)
        json.dumps({
            "evaluation": {
                "what_went_well": "Good mention of PostgreSQL integration.",
                "areas_for_improvement": "Could outline database indexing choices."
            },
            "scores": {
                "Technical Accuracy": 7,
                "Technical Depth": 6,
                "Problem Solving": 8,
                "Relevance": 8,
                "Communication": 7,
                "Answer Structure": 8
            },
            "follow_up_required": False,
            "next_question": "Interview complete",
            "next_question_type": "HR"
        }),
        # Call for finalize_session (Report compile)
        json.dumps({
            "overall_score": 78,
            "dimension_scores": {
                "Technical Accuracy": 75,
                "Technical Depth": 65,
                "Problem Solving": 80,
                "Communication": 78,
                "Relevance": 82,
                "Answer Structure": 80
            },
            "strengths": ["Strong problem solving skills.", "Good resume alignment."],
            "areas_for_improvement": ["Explain engineering trade-offs in deeper detail."],
            "recommended_improvements": ["Review database indexing strategies."]
        })
    ]

    # Test final turn submission
    res2 = service.submit_answer(session.id, "I integrated PostgreSQL with SQLAlchemy.")
    assert res2["success"] is True
    assert res2["is_finished"] is True

    # Validate Completed state and overall score
    assert session.status == 'Completed'
    assert session.overall_score == 78.0
    report = session.get_final_feedback()
    assert report["overall_score"] == 78
    assert "indexing strategies" in report["recommended_improvements"][0]
    assert len(report["strengths"]) == 2
