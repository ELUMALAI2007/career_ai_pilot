"""
CareerPilot AI - Resume Intelligence Unit & Integration Automated Test Suite
Verifies document parsing, multi-dimensional score calculation, keyword matching, skill gaps, bullet analysis, resume questions, mock interviews, and version comparisons.
"""

import pytest
import os
import json
from app import create_app, db
from app.models.user import User
from app.models.resume import ResumeUpload, ResumeAnalysis, ResumeQuestion, ResumeInterviewSession
from app.services.resume_parser import ResumeParser
from app.services.resume_evaluator import ResumeEvaluator
from app.services.resume_service import ResumeService
from app.services.resume_interview_service import ResumeInterviewService
from app.services.resume_version_service import ResumeVersionService


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
    user = User(full_name="Candidate Tester", email="resume_tester@test.com", status="approved")
    user.set_password("Password123!")
    db.session.add(user)
    db.session.commit()
    return user


def test_resume_parser_contact_and_sections():
    """Verifies contact info parsing and section detection."""
    sample_text = """
    John Doe
    Email: john.doe@example.com | Phone: +1 555-123-4567
    LinkedIn: https://linkedin.com/in/johndoe | GitHub: https://github.com/johndoe

    Professional Summary
    Experienced Software Engineer skilled in Python, Flask, SQL, and React.

    Education
    Bachelor of Technology in Computer Science, XYZ University, CGPA: 8.9, 2024

    Skills
    Python, Flask, React, SQL, Docker, Git, Machine Learning

    Experience
    Software Engineer Intern - Tech Corp (2023 - 2024)
    - Developed a Flask application reducing API latency by 35%.
    - Worked on database indexing.

    Projects
    CareerPilot AI - Built an AI application using Python and SQLite.
    """

    contact = ResumeParser.parse_contact_info(sample_text)
    assert contact["email"] == "john.doe@example.com"
    assert contact["linkedin"] == "https://linkedin.com/in/johndoe"
    assert contact["github"] == "https://github.com/johndoe"

    sections = ResumeParser.parse_sections(sample_text)
    assert sections["sections_found"]["education"] is True
    assert sections["sections_found"]["skills"] is True
    assert sections["sections_found"]["experience"] is True
    assert sections["sections_found"]["projects"] is True
    assert "Python" in sections["extracted_skills"]
    assert "Flask" in sections["extracted_skills"]

    completeness, breakdown = ResumeParser.calculate_completeness_score(contact, sections)
    assert completeness >= 85.0


def test_resume_evaluator_multidimensional_scoring():
    """Verifies ATS Compatibility, Resume Quality, Job Match, and Overall Readiness Scores."""
    sample_text = """
    Jane Smith
    email: jane@example.com | github: https://github.com/janesmith

    Summary
    Data Analyst candidate proficient in Python, SQL, Excel, and Power BI.

    Education
    B.S. Data Science, 2025

    Skills
    Python, SQL, Excel, Power BI, Statistics, Tableau, Pandas

    Experience
    Data Analyst Intern
    - Developed automated SQL pipelines processing 50,000+ records daily.
    - Worked on Excel spreadsheets.
    """

    metadata = {"page_count": 1, "word_count": 250, "has_tables": False, "has_images": False}
    contact = ResumeParser.parse_contact_info(sample_text)
    sections = ResumeParser.parse_sections(sample_text)
    completeness, _ = ResumeParser.calculate_completeness_score(contact, sections)

    eval_result = ResumeEvaluator.evaluate_all(
        text=sample_text,
        metadata=metadata,
        contact=contact,
        sections=sections,
        completeness_score=completeness,
        target_role="Data Analyst"
    )

    scores = eval_result["scores"]
    assert scores["overall_score"] > 60.0
    assert scores["ats_score"] > 60.0
    assert scores["quality_score"] > 60.0
    assert scores["job_match_score"] > 60.0

    # Keyword check
    kw = eval_result["keyword_analysis"]
    assert "Sql" in kw["found"] or "SQL" in [f.upper() for f in kw["found"]]
    assert "worked" in eval_result["bullets_analysis"]["weak_verbs_found"]


def test_resume_questions_generation(app_ctx, test_user):
    """Verifies that questions are generated strictly from candidate's resume content."""
    parsed_data = {
        "extracted_skills": ["Python", "Flask", "SQL"],
        "sections": {"sections_found": {"projects": True, "experience": True, "education": True}}
    }
    
    upload = ResumeUpload(user_id=test_user.id, filename="resume.pdf", file_path="/fake/path")
    db.session.add(upload)
    db.session.commit()

    questions = ResumeInterviewService.generate_resume_questions(test_user.id, upload.id, parsed_data, "Software Engineer")
    assert len(questions) >= 4
    
    categories = [q.category for q in questions]
    assert "Project Questions" in categories
    assert "Technology Questions" in categories
    assert "HR Questions" in categories


def test_interactive_mock_interview(app_ctx, test_user):
    """Verifies interactive 'Interview Me' mock session creation and candidate response evaluation."""
    upload = ResumeUpload(user_id=test_user.id, filename="resume.pdf", file_path="/fake/path")
    db.session.add(upload)
    db.session.commit()

    parsed_data = {
        "extracted_skills": ["Python", "Flask", "SQL", "React"],
        "sections": {"sections_found": {"projects": True, "experience": True, "education": True}}
    }
    ResumeInterviewService.generate_resume_questions(test_user.id, upload.id, parsed_data, "Software Engineer")

    session = ResumeInterviewService.start_interview_session(test_user.id, upload.id, "Software Engineer")
    assert session.id is not None
    assert session.is_completed is False

    ans_result = ResumeInterviewService.process_candidate_response(
        session_id=session.id,
        user_id=test_user.id,
        candidate_answer="I developed the backend system using Python and Flask to optimize REST API query response time."
    )
    assert "feedback" in ans_result
    assert ans_result["session_completed"] is False


def test_version_comparison_matrix(app_ctx, test_user):
    """Verifies side-by-side version comparison deltas."""
    upload1 = ResumeUpload(user_id=test_user.id, filename="v1.pdf", file_path="/p1", version_number=1)
    upload2 = ResumeUpload(user_id=test_user.id, filename="v2.pdf", file_path="/p2", version_number=2)
    db.session.add_all([upload1, upload2])
    db.session.commit()

    a1 = ResumeAnalysis(
        resume_id=upload1.id, overall_score=70.0, ats_score=68.0, quality_score=72.0, job_match_score=65.0, completeness_score=75.0,
        parsed_data_json=json.dumps({"extracted_skills": ["Python", "SQL"]}),
        keyword_analysis_json=json.dumps({"keyword_match_pct": 65.0})
    )
    a2 = ResumeAnalysis(
        resume_id=upload2.id, overall_score=85.0, ats_score=84.0, quality_score=88.0, job_match_score=82.0, completeness_score=90.0,
        parsed_data_json=json.dumps({"extracted_skills": ["Python", "SQL", "Docker", "React"]}),
        keyword_analysis_json=json.dumps({"keyword_match_pct": 82.0})
    )
    db.session.add_all([a1, a2])
    db.session.commit()

    matrix = ResumeVersionService.compare_versions(a1, a2)
    assert matrix["deltas"]["overall_delta"] == 15.0
    assert matrix["deltas"]["ats_delta"] == 16.0
    assert "Docker" in matrix["deltas"]["added_skills"]
    assert "React" in matrix["deltas"]["added_skills"]


def test_special_character_skill_extraction():
    """Verifies that skills with special characters like C++, C#, and REST API are correctly extracted."""
    sample = """
    Jane Developer
    Skills: C++, C#, Python, SQL, REST API, Docker
    """
    sections = ResumeParser.parse_sections(sample)
    skills = sections["extracted_skills"]
    assert "C++" in skills
    assert "C#" in skills
    assert "Python" in skills
    assert "REST API" in skills


def test_quality_score_capping():
    """Verifies that quality score and overall score are capped at 100.0 max."""
    sample = """
    Expert Engineer
    - Developed scalable microservices using Python and C++ processing 100,000+ requests daily.
    - Automated CI/CD deployment pipelines achieving 99.9% uptime.
    - Engineered high throughput cache layer using Redis saving 50% database latency.
    """
    metadata = {"page_count": 1, "word_count": 300, "has_tables": False, "has_images": False}
    contact = ResumeParser.parse_contact_info(sample)
    sections = ResumeParser.parse_sections(sample)
    completeness, _ = ResumeParser.calculate_completeness_score(contact, sections)

    eval_result = ResumeEvaluator.evaluate_all(
        text=sample,
        metadata=metadata,
        contact=contact,
        sections=sections,
        completeness_score=completeness,
        target_role="Software Engineer"
    )

    scores = eval_result["scores"]
    assert scores["quality_score"] <= 100.0
    assert scores["overall_score"] <= 100.0

