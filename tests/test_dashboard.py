"""
CareerPilot AI — Placement Command Center Dashboard Test Suite
Verifies dashboard summary aggregation, personalized greetings, daily targets, recent activity timelines,
unattempted module handling, and score consistency with AnalyticsService.
"""

import pytest
import json
from app import create_app, db
from app.models.user import User, Role
from app.models.aptitude import AptitudeAttempt, AptitudeTestResult
from app.models.coding import CodingProblem, CodingSubmission
from app.models.communication import CommunicationAssessment
from app.models.resume import ResumeUpload, ResumeAnalysis
from app.services.dashboard_service import DashboardService
from app.services.analytics_service import AnalyticsService
from config import TestingConfig


@pytest.fixture
def dashboard_app():
    """Configures isolated test application context with clean in-memory database."""
    app = create_app(TestingConfig)
    with app.app_context():
        student_role = Role.query.filter_by(name='student').first()
        if not student_role:
            student_role = Role(name='student', description='Placement Student')
            db.session.add(student_role)
            db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def candidate_user(dashboard_app):
    """Creates candidate user account for dashboard testing."""
    user = User(full_name="Ganeshan Student", email="ganeshan@test.com", status="approved")
    user.set_password("Password123!")
    db.session.add(user)
    db.session.commit()
    return user


def test_empty_state_candidate_dashboard(dashboard_app, candidate_user):
    """Verifies dashboard rendering for a new user with no previous attempts."""
    with dashboard_app.app_context():
        summary = DashboardService.get_dashboard_summary(candidate_user.id)
        
        assert summary["user_id"] == candidate_user.id
        assert summary["user_name"] == "Ganeshan Student"
        assert "Ganeshan" in summary["greeting"]
        assert len(summary["today_targets"]["checklist"]) == 3
        assert summary["recent_activities"] == []
        assert summary["continue_target"]["progress_pct"] == 0

        # Verify score consistency with AnalyticsService
        intel = AnalyticsService.compute_placement_intelligence(candidate_user.id)
        assert summary["intelligence"]["overall_score"] == intel["overall_score"]


def test_populated_candidate_dashboard(dashboard_app, candidate_user):
    """Verifies dashboard data aggregation when candidate has completed test attempts across modules."""
    with dashboard_app.app_context():
        # 1. Aptitude Result
        apt = AptitudeTestResult(
            session_id="sess_123", user_id=candidate_user.id, test_type="practice", title="Quantitative Mock",
            score=8, total_questions=10, accuracy_percentage=80.0, correct_count=8, incorrect_count=2,
            skipped_count=0, time_used_seconds=300, category_scores_json="{}", strong_topics_json="[]", weak_topics_json="[]"
        )
        db.session.add(apt)

        # 2. Coding Submission
        prob = CodingProblem(title="Reverse Linked List", slug="reverse-linked-list", description="Reverse list", difficulty="easy")
        db.session.add(prob)
        db.session.commit()

        sub = CodingSubmission(user_id=candidate_user.id, problem_id=prob.id, language="python", code_body="pass", status="Accepted")
        db.session.add(sub)

        # 3. Resume Analysis
        upload = ResumeUpload(user_id=candidate_user.id, filename="resume_ganeshan.pdf", file_path="/tmp/path")
        db.session.add(upload)
        db.session.commit()

        analysis = ResumeAnalysis(
            resume_id=upload.id, overall_score=88.0, ats_score=85.0, quality_score=90.0, job_match_score=82.0, completeness_score=92.0,
            parsed_data_json=json.dumps({"extracted_skills": ["Python", "SQL", "Excel"]})
        )
        db.session.add(analysis)
        db.session.commit()

        # Fetch Dashboard Summary
        summary = DashboardService.get_dashboard_summary(candidate_user.id)

        assert len(summary["recent_activities"]) >= 3
        assert summary["intelligence"]["overall_score"] > 50.0
        assert summary["intelligence"]["modules"]["aptitude"]["status"] == "Available"
        assert summary["intelligence"]["modules"]["coding"]["status"] == "Available"
        assert summary["intelligence"]["modules"]["resume"]["status"] == "Available"


def test_dashboard_http_route(dashboard_app, candidate_user):
    """Verifies GET /dashboard/ endpoint for authenticated candidate."""
    client = dashboard_app.test_client()

    with client.session_transaction() as sess:
        sess['_user_id'] = str(candidate_user.id)

    res = client.get('/dashboard/')
    assert res.status_code == 200
    assert b'Ganeshan' in res.data
    assert b'Placement Readiness' in res.data or b'Command Center' in res.data
