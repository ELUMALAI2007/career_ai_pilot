"""Seed the database-backed mock interview question bank."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.interview import InterviewQuestion

ROLES = [
    "Software Developer", "Frontend Developer", "Backend Developer",
    "Full Stack Developer", "Data Analyst", "Data Scientist",
    "Machine Learning Engineer"
]

TEMPLATES = {
    "Introduction": [
        ("About You", "Tell me about yourself. Walk through your background, experience, and what brought you to this role."),
        ("Career Path", "Can you describe your professional journey and how it led you to where you are today?"),
    ],
    "Resume": [
        ("Experience", "Walk me through your most relevant professional experiences."),
        ("Skills", "Which skills on your resume are you most confident about, and why?"),
    ],
    "Project": [
        ("Key Project", "Tell me about the most challenging project you worked on and your role in it."),
        ("Impact", "Describe a project where you had the most impact. What was the outcome?"),
        ("Technologies", "Walk me through a project where you used the key technologies relevant to this role."),
    ],
    "Technical": [
        ("Core Concepts", "Explain the core concepts and trade-offs you would use when solving a problem in this role."),
        ("Debugging", "Describe your process for diagnosing and fixing a difficult production bug."),
        ("Design", "Design a reliable system relevant to this role and explain its main components."),
        ("Testing", "How would you test a feature thoroughly before releasing it?"),
        ("Performance", "Tell me how you would identify and improve a performance bottleneck."),
    ],
    "HR": [
        ("Motivation", "Why are you interested in this role and what do you hope to contribute?"),
        ("Growth", "What skill are you currently developing, and how are you measuring progress?"),
        ("Collaboration", "How do you handle disagreement with a teammate about an important decision?"),
        ("Ownership", "Tell me about a time you took ownership of a problem outside your usual responsibilities."),
        ("Company Fit", "What kind of team environment helps you do your best work?"),
    ],
    "Behavioral": [
        ("Leadership", "Tell me about a time you influenced a project without having formal authority."),
        ("Failure", "Describe a project setback and what you changed afterward."),
        ("Prioritization", "How have you prioritized competing deadlines with limited time?"),
        ("Communication", "Tell me about a time you explained a complex idea to a non-technical audience."),
        ("Impact", "Describe a decision you made that produced a measurable positive result."),
    ],
}


def seed_questions():
    """Insert the bank once, leaving existing customized entries untouched."""
    if InterviewQuestion.query.count():
        return 0
    questions = []
    for role in ROLES:
        for interview_type, entries in TEMPLATES.items():
            for difficulty in ("Easy", "Medium", "Hard"):
                for topic, question in entries:
                    prefix = "" if interview_type in ["Introduction", "Resume"] else f"For a {role} position: "
                    questions.append(InterviewQuestion(
                        role=role, interview_type=interview_type,
                        difficulty=difficulty, topic=topic,
                        question=f"{prefix}{question}",
                        is_active=True
                    ))
    db.session.add_all(questions)
    db.session.commit()
    return len(questions)


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        print(f"Seeded {seed_questions()} interview questions.")
