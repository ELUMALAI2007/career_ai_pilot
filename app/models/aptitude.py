"""
CareerPilot AI - Aptitude Models Module
Database models for aptitude learning, adaptive progression, questions bank, test sessions, topic mastery, daily challenges, bookmarks, and analytics.
"""

from datetime import datetime
from app import db


class AptitudeCategory(db.Model):
    """Test category (Quantitative, Logical Reasoning, Verbal Ability)."""
    __tablename__ = 'aptitude_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50), default='fa-brain')
    questions = db.relationship('AptitudeQuestion', backref='category', lazy='dynamic')
    attempts = db.relationship('AptitudeAttempt', backref='category', lazy='dynamic')


class AptitudeQuestion(db.Model):
    """Multiple-choice placement question with formulas, shortcuts, and difficulty levels."""
    __tablename__ = 'aptitude_questions'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('aptitude_categories.id'), nullable=False)
    topic = db.Column(db.String(100), nullable=False, index=True)
    subtopic = db.Column(db.String(100), nullable=True)
    difficulty = db.Column(db.String(20), default='intermediate', index=True)  # foundation, beginner, intermediate, advanced, expert, master
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', 'D'
    explanation = db.Column(db.Text, nullable=False)
    formula = db.Column(db.Text, nullable=True)
    shortcut = db.Column(db.Text, nullable=True)
    concept = db.Column(db.Text, nullable=True)
    estimated_time = db.Column(db.Integer, default=60)  # seconds
    tags = db.Column(db.String(255), nullable=True)
    source_type = db.Column(db.String(20), default='generated')  # 'generated', 'admin_created'
    fingerprint = db.Column(db.String(64), unique=True, nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookmarks = db.relationship('AptitudeBookmark', backref='question', lazy='dynamic', cascade='all, delete-orphan')


class AptitudeAttempt(db.Model):
    """User test attempt record for practice sessions."""
    __tablename__ = 'aptitude_attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('aptitude_categories.id'), nullable=True)
    topic = db.Column(db.String(100), nullable=True)
    difficulty = db.Column(db.String(20), nullable=True)
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)
    score_percentage = db.Column(db.Float, nullable=False)
    time_taken_seconds = db.Column(db.Integer, default=0)
    attempt_type = db.Column(db.String(30), default='practice')  # 'practice', 'personalized', 'company_mock', 'quick'
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)


class AptitudeQuestionAnswer(db.Model):
    """Detailed log of individual question responses."""
    __tablename__ = 'aptitude_question_answers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('aptitude_questions.id'), nullable=False)
    selected_option = db.Column(db.String(1), nullable=True)
    is_correct = db.Column(db.Boolean, default=False)
    time_taken_seconds = db.Column(db.Integer, default=0)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)


class AptitudeBookmark(db.Model):
    """User bookmarked questions."""
    __tablename__ = 'aptitude_bookmarks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('aptitude_questions.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'question_id', name='_user_question_bookmark_uc'),)


class AptitudeProgress(db.Model):
    """Overall student aptitude journey metrics and readiness score."""
    __tablename__ = 'aptitude_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    current_level = db.Column(db.String(20), default='foundation')  # foundation, beginner, intermediate, advanced, expert, master
    total_questions_solved = db.Column(db.Integer, default=0)
    correct_count = db.Column(db.Integer, default=0)
    overall_accuracy = db.Column(db.Float, default=0.0)
    avg_time_seconds = db.Column(db.Float, default=0.0)
    readiness_score = db.Column(db.Integer, default=0)  # 0 to 100
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AptitudeTopicMastery(db.Model):
    """Topic-specific mastery scores for adaptive practice recommendation."""
    __tablename__ = 'aptitude_topic_mastery'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_name = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    mastery_percentage = db.Column(db.Float, default=0.0)
    questions_attempted = db.Column(db.Integer, default=0)
    correct_count = db.Column(db.Integer, default=0)
    avg_speed_seconds = db.Column(db.Float, default=0.0)
    last_attempted_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'topic', name='_user_topic_mastery_uc'),)


class AptitudeTestSession(db.Model):
    """Server-side timed mock test sessions."""
    __tablename__ = 'aptitude_test_sessions'

    id = db.Column(db.String(64), primary_key=True)  # UUID or random token
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    test_type = db.Column(db.String(50), nullable=False)  # quick, standard, placement, full, master, company
    title = db.Column(db.String(150), nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    questions_data = db.Column(db.Text, nullable=False)  # JSON string of question IDs & payload
    answers_data = db.Column(db.Text, default='{}')       # JSON string of user answers & marked state
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)


class AptitudeTestResult(db.Model):
    """Completed mock examination result breakdown."""
    __tablename__ = 'aptitude_test_results'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), db.ForeignKey('aptitude_test_sessions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    test_type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    accuracy_percentage = db.Column(db.Float, nullable=False)
    correct_count = db.Column(db.Integer, nullable=False)
    incorrect_count = db.Column(db.Integer, nullable=False)
    skipped_count = db.Column(db.Integer, nullable=False)
    time_used_seconds = db.Column(db.Integer, nullable=False)
    category_scores_json = db.Column(db.Text, nullable=False)  # JSON breakdown
    strong_topics_json = db.Column(db.Text, nullable=False)   # JSON list
    weak_topics_json = db.Column(db.Text, nullable=False)     # JSON list
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)


class AptitudeDailyChallenge(db.Model):
    """Daily 10 challenge question set for a given date."""
    __tablename__ = 'aptitude_daily_challenges'

    id = db.Column(db.Integer, primary_key=True)
    challenge_date = db.Column(db.Date, nullable=False, unique=True)
    questions_json = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AptitudeDailyChallengeAttempt(db.Model):
    """User attempt record for daily challenge."""
    __tablename__ = 'aptitude_daily_challenge_attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('aptitude_daily_challenges.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    accuracy_percentage = db.Column(db.Float, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)


class AptitudeStreak(db.Model):
    """Daily practice activity streak tracking."""
    __tablename__ = 'aptitude_streaks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_activity_date = db.Column(db.Date, nullable=True)
    questions_today = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

