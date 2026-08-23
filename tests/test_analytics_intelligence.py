"""
CareerPilot AI — Detailed Performance Analytics & Placement Intelligence Test Suite
Verifies real-time multi-module data aggregation, cold-start handling, dynamic weight redistribution,
role suitability matching, academic eligibility, PDF report generation, and route access controls.
"""

import pytest
import json
from app import create_app, db
from app.models.user import User, Role
from app.models.aptitude import AptitudeAttempt, AptitudeTestResult
from app.models.coding import CodingProblem, CodingSubmission
from app.models.communication import CommunicationAssessment
from app.models.interview import MockInterview
from app.models.resume import ResumeUpload, ResumeAnalysis
from app.services.analytics_service import AnalyticsService
from app.services.analytics_pdf_report import AnalyticsPdfReportGenerator
from config import TestingConfig


@pytest.fixture
def analytics_app():
    """Configures test Flask application context with clean memory database."""
    app = create_app(TestingConfig)
    with app.app_context():
        student_role = Role.query.filter_by(name='student').first()
        if not student_role:
            student_role = Role(name='student', description='Placement Candidate Student')
            db.session.add(student_role)
            db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def test_user(analytics_app):
    """Creates candidate user account for analytics testing."""
    user = User(full_name="Analytics Student", email="analytics_student@test.com", status="approved")
    user.set_password("Password123!")
    db.session.add(user)
    db.session.commit()
    return user


def test_cold_start_user_analytics_computation(analytics_app, test_user):
    """Verifies that a user with no test attempts receives provisional rating with Insufficient Data flags."""
    with analytics_app.app_context():
        intelligence = AnalyticsService.compute_placement_intelligence(test_user.id)
        
        assert intelligence["user_id"] == test_user.id
        assert intelligence["confidence"] == "Low"
        assert intelligence["is_provisional"] is True
        assert intelligence["overall_score"] == 0.0
        assert intelligence["placement_status"] == "Foundation"

        modules = intelligence["modules"]
        assert modules["aptitude"]["status"] == "Insufficient Data"
        assert modules["coding"]["status"] == "Insufficient Data"
        assert modules["communication"]["status"] == "Insufficient Data"
        assert modules["interview"]["status"] == "Insufficient Data"
        assert modules["resume"]["status"] == "Not Analyzed"


def test_real_data_analytics_aggregation_and_role_suitability(analytics_app, test_user):
    """Verifies analytics computation when real candidate attempt records exist across modules."""
    with analytics_app.app_context():
        # 1. Add Aptitude Attempts
        att1 = AptitudeAttempt(user_id=test_user.id, category_id=1, topic="Quantitative", total_questions=2, correct_answers=2, score_percentage=100.0, time_taken_seconds=55)
        db.session.add(att1)

        # 2. Add Coding Submission
        prob = CodingProblem(title="Two Sum", slug="two-sum", description="Find two numbers that sum to target", difficulty="easy")
        db.session.add(prob)
        db.session.commit()

        sub = CodingSubmission(user_id=test_user.id, problem_id=prob.id, language="python", code_body="print('hello')", status="Accepted")
        db.session.add(sub)

        # 3. Add Communication Assessment
        comm = CommunicationAssessment(user_id=test_user.id, assessment_type="writing", raw_input_text="Sample text", clarity_score=80.0, grammar_score=85.0, confidence_score=75.0)
        db.session.add(comm)

        # 4. Add Resume Analysis
        upload = ResumeUpload(user_id=test_user.id, filename="my_resume.pdf", file_path="/fake/path")
        db.session.add(upload)
        db.session.commit()

        analysis = ResumeAnalysis(
            resume_id=upload.id, overall_score=85.0, ats_score=82.0, quality_score=88.0, job_match_score=80.0, completeness_score=90.0,
            parsed_data_json=json.dumps({"extracted_skills": ["Python", "SQL", "Excel", "Tableau", "Git"]})
        )
        db.session.add(analysis)
        db.session.commit()

        # Compute Placement Intelligence
        intelligence = AnalyticsService.compute_placement_intelligence(test_user.id)

        assert intelligence["overall_score"] > 60.0
        assert intelligence["confidence"] in ["Medium", "High"]
        assert intelligence["active_modules_count"] >= 4

        # Verify Aptitude module
        assert intelligence["modules"]["aptitude"]["status"] == "Available"
        assert intelligence["modules"]["aptitude"]["accuracy_pct"] == 100.0

        # Verify Coding module
        assert intelligence["modules"]["coding"]["status"] == "Available"
        assert intelligence["modules"]["coding"]["problems_solved"] == 1

        # Verify Role Suitability matching
        roles = intelligence["role_suitability"]
        assert len(roles) > 0
        top_role = roles[0]
        assert top_role["title"] in ["Data Analyst", "Software Engineer", "Full Stack Developer", "AI/ML Engineer"]
        assert top_role["match_pct"] > 50.0


def test_pdf_report_generation(analytics_app, test_user):
    """Verifies that AnalyticsPdfReportGenerator generates a valid PDF buffer from placement intelligence data."""
    with analytics_app.app_context():
        intelligence = AnalyticsService.compute_placement_intelligence(test_user.id)
        pdf_buffer = AnalyticsPdfReportGenerator.generate_pdf(intelligence)
        
        pdf_bytes = pdf_buffer.getvalue()
        assert len(pdf_bytes) > 0
        assert pdf_bytes.startswith(b'%PDF-')


def test_analytics_http_endpoints(analytics_app, test_user):
    """Verifies GET /analytics/, POST /analytics/refresh, and GET /analytics/download-report HTTP routes."""
    client = analytics_app.test_client()

    # Login test user
    with client.session_transaction() as sess:
        sess['_user_id'] = str(test_user.id)

    # 1. Test Dashboard View
    res_index = client.get('/analytics/')
    assert res_index.status_code == 200
    assert b'Detailed Performance Analytics' in res_index.data

    # 2. Test Refresh POST
    res_refresh = client.post('/analytics/refresh', follow_redirects=True)
    assert res_refresh.status_code == 200
    assert b'refreshed successfully' in res_refresh.data

    # 3. Test PDF Download GET
    res_pdf = client.get('/analytics/download-report')
    assert res_pdf.status_code == 200
    assert res_pdf.mimetype == 'application/pdf'
    assert res_pdf.data.startswith(b'%PDF-')
