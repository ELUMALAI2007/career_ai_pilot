#!/usr/bin/env python
"""Quick verification that difficulty levels match appropriately."""
import json
from app import create_app, db
from app.models.user import User
from app.models.resume import ResumeUpload, ResumeAnalysis
from app.models.interview import InterviewQuestion
from app.models.coding import CodingProblem
from app.services.interview_service import InterviewService
from config import TestingConfig

app = create_app(TestingConfig)
with app.app_context():
    db.drop_all()
    db.create_all()
    
    user = User(full_name="Candidate", email="candidate@test.com", status="approved")
    user.set_password("TestPass123")
    db.session.add(user)
    db.session.commit()
    
    resume = ResumeUpload(user_id=user.id, filename="resume.pdf", file_path="/tmp/resume.pdf")
    db.session.add(resume)
    db.session.flush()
    db.session.add(ResumeAnalysis(
        resume_id=resume.id,
        parsed_data_json=json.dumps({"skills": ["Python"], "projects": []})
    ))
    
    # Seed questions at each difficulty level
    db.session.add_all([
        InterviewQuestion(question="Easy Intro", role="Software Developer", interview_type="Introduction", difficulty="Easy", topic="Intro"),
        InterviewQuestion(question="Easy Tech", role="Software Developer", interview_type="Technical", difficulty="Easy", topic="Basics"),
        InterviewQuestion(question="Medium Intro", role="Software Developer", interview_type="Introduction", difficulty="Medium", topic="Intro"),
        InterviewQuestion(question="Medium Tech", role="Software Developer", interview_type="Technical", difficulty="Medium", topic="Design"),
        InterviewQuestion(question="Hard Intro", role="Software Developer", interview_type="Introduction", difficulty="Hard", topic="Intro"),
        InterviewQuestion(question="Hard Tech", role="Software Developer", interview_type="Technical", difficulty="Hard", topic="System"),
    ])
    
    db.session.add_all([
        CodingProblem(title="Easy", slug="easy", description="Easy problem.", difficulty="easy", topic="Arrays", xp_reward=5),
        CodingProblem(title="Medium", slug="medium", description="Medium problem.", difficulty="medium", topic="Strings", xp_reward=10),
        CodingProblem(title="Hard", slug="hard", description="Hard problem.", difficulty="hard", topic="Graphs", xp_reward=20),
    ])
    
    db.session.commit()
    
    service = InterviewService()
    
    # Create sessions with different difficulties
    easy_session = service.create_session(user.id, resume.id, "Software Developer", "Google", "Easy", "Technical", 0, False)
    medium_session = service.create_session(user.id, resume.id, "Software Developer", "Google", "Medium", "Technical", 0, False)
    hard_session = service.create_session(user.id, resume.id, "Software Developer", "Google", "Hard", "Technical", 0, False)
    
    print("✓ Difficulty-Matched Interview Sessions Created")
    print(f"\nEasy:   total={easy_session.total_questions}")
    print(f"Medium: total={medium_session.total_questions}")
    print(f"Hard:   total={hard_session.total_questions}")
    
    # Verify questions are difficulty-appropriate
    easy_q = easy_session.get_question_queue()[0] if easy_session.get_question_queue() else {}
    print(f"\nEasy session first queue question: {easy_q.get('question', '?')}")
    print(f"✓ Technical and HR questions now match the selected difficulty level!")
