"""
CareerPilot AI - Coding & DSA Database Models
Defines problem catalogue, submissions, test execution history, bookmarks, progress, daily challenges, and gamification.
"""

from datetime import datetime, date
import json
from app import db


class CodingProblem(db.Model):
    """Coding & Data Structures problem definition."""
    __tablename__ = 'coding_problems'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), default='medium', index=True)  # easy, medium, hard
    topic = db.Column(db.String(80), nullable=False, default='Arrays', index=True)
    
    input_format = db.Column(db.Text)
    output_format = db.Column(db.Text)
    constraints = db.Column(db.Text)
    
    # JSON encoded starter code templates for python, javascript, cpp, java
    starter_templates_json = db.Column(db.Text, default='{}')
    
    # JSON encoded public sample test cases (visible to user in details & run)
    sample_test_cases_json = db.Column(db.Text, default='[]')
    
    # JSON encoded hidden test cases (strictly server-side, never exposed to client)
    hidden_test_cases_json = db.Column(db.Text, default='[]')
    
    company_tags = db.Column(db.String(255), default='')  # e.g. "Amazon, Google, Microsoft"
    xp_reward = db.Column(db.Integer, default=20)  # Easy: 10, Medium: 20, Hard: 40
    
    total_submissions = db.Column(db.Integer, default=0)
    accepted_submissions = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    submissions = db.relationship('CodingSubmission', backref='problem', lazy='dynamic', cascade='all, delete-orphan')
    bookmarks = db.relationship('CodingBookmark', backref='problem', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def starter_templates(self) -> dict:
        try:
            return json.loads(self.starter_templates_json or '{}')
        except Exception:
            return {}

    @starter_templates.setter
    def starter_templates(self, val: dict):
        self.starter_templates_json = json.dumps(val)

    @property
    def sample_test_cases(self) -> list:
        try:
            return json.loads(self.sample_test_cases_json or '[]')
        except Exception:
            return []

    @sample_test_cases.setter
    def sample_test_cases(self, val: list):
        self.sample_test_cases_json = json.dumps(val)

    @property
    def hidden_test_cases(self) -> list:
        try:
            return json.loads(self.hidden_test_cases_json or '[]')
        except Exception:
            return []

    @hidden_test_cases.setter
    def hidden_test_cases(self, val: list):
        self.hidden_test_cases_json = json.dumps(val)

    @property
    def acceptance_rate(self) -> float:
        if self.total_submissions == 0:
            return 0.0
        return round((self.accepted_submissions / self.total_submissions) * 100, 1)

    @property
    def company_tag_list(self) -> list:
        if not self.company_tags:
            return []
        return [tag.strip() for tag in self.company_tags.split(',') if tag.strip()]

    def to_public_dict(self, user_id: int = None) -> dict:
        """Serializes problem for frontend consumption (WITHOUT hidden test cases)."""
        is_bookmarked = False
        user_status = 'Unsolved'  # 'Unsolved', 'Attempted', 'Solved'

        if user_id:
            bookmark = CodingBookmark.query.filter_by(user_id=user_id, problem_id=self.id).first()
            is_bookmarked = bool(bookmark)
            
            # Check if solved or attempted
            accepted_sub = CodingSubmission.query.filter_by(user_id=user_id, problem_id=self.id, status='Accepted').first()
            if accepted_sub:
                user_status = 'Solved'
            else:
                any_sub = CodingSubmission.query.filter_by(user_id=user_id, problem_id=self.id).first()
                if any_sub:
                    user_status = 'Attempted'

        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'difficulty': self.difficulty,
            'topic': self.topic,
            'input_format': self.input_format,
            'output_format': self.output_format,
            'constraints': self.constraints,
            'starter_templates': self.starter_templates,
            'sample_test_cases': self.sample_test_cases,
            'company_tags': self.company_tag_list,
            'xp_reward': self.xp_reward,
            'total_submissions': self.total_submissions,
            'accepted_submissions': self.accepted_submissions,
            'acceptance_rate': self.acceptance_rate,
            'is_bookmarked': is_bookmarked,
            'user_status': user_status
        }


class CodingSubmission(db.Model):
    """User code submission execution record."""
    __tablename__ = 'coding_submissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('coding_problems.id'), nullable=False, index=True)
    language = db.Column(db.String(30), nullable=False)  # python, javascript, cpp, java
    code_body = db.Column(db.Text, nullable=False)
    
    # Accepted, Wrong Answer, Compilation Error, Runtime Error, Time Limit Exceeded, Memory Limit Exceeded
    status = db.Column(db.String(50), default='Pending', index=True)
    
    execution_time_ms = db.Column(db.Float, default=0.0)
    memory_mb = db.Column(db.Float, nullable=True)
    
    passed_tests = db.Column(db.Integer, default=0)
    total_tests = db.Column(db.Integer, default=0)
    
    # JSON-encoded array of test results (safe for client inspection)
    test_results_json = db.Column(db.Text, default='[]')
    
    stdout = db.Column(db.Text, default='')
    error_log = db.Column(db.Text, default='')
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship('User', backref=db.backref('coding_submissions', lazy='dynamic'))

    @property
    def test_results(self) -> list:
        try:
            return json.loads(self.test_results_json or '[]')
        except Exception:
            return []

    @test_results.setter
    def test_results(self, val: list):
        self.test_results_json = json.dumps(val)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'problem_id': self.problem_id,
            'problem_title': self.problem.title if self.problem else 'Unknown',
            'problem_slug': self.problem.slug if (self.problem and self.problem.slug) else '',
            'language': self.language,
            'code_body': self.code_body,
            'status': self.status,
            'execution_time_ms': self.execution_time_ms,
            'memory_mb': self.memory_mb,
            'passed_tests': self.passed_tests,
            'total_tests': self.total_tests,
            'test_results': self.test_results,
            'stdout': self.stdout,
            'error_log': self.error_log,
            'submitted_at': self.submitted_at.strftime('%Y-%m-%d %H:%M:%S') if self.submitted_at else ''
        }


class CodingBookmark(db.Model):
    """User bookmarked problem relationship."""
    __tablename__ = 'coding_bookmarks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('coding_problems.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'problem_id', name='uq_user_problem_bookmark'),)


class CodingProgress(db.Model):
    """User coding metrics, streaks, XP, and topic mastery."""
    __tablename__ = 'coding_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False, index=True)
    
    total_solved = db.Column(db.Integer, default=0)
    easy_solved = db.Column(db.Integer, default=0)
    medium_solved = db.Column(db.Integer, default=0)
    hard_solved = db.Column(db.Integer, default=0)
    total_attempts = db.Column(db.Integer, default=0)
    
    total_xp = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_solved_date = db.Column(db.Date, nullable=True)
    
    # JSON encoded topic stats: {"Arrays": {"solved": 3, "total": 5}, ...}
    topic_stats_json = db.Column(db.Text, default='{}')
    proctor_flags = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('coding_progress', uselist=False))

    @property
    def topic_stats(self) -> dict:
        try:
            return json.loads(self.topic_stats_json or '{}')
        except Exception:
            return {}

    @topic_stats.setter
    def topic_stats(self, val: dict):
        self.topic_stats_json = json.dumps(val)

    @property
    def accuracy(self) -> float:
        attempts = self.total_attempts or 0
        if attempts == 0:
            return 0.0
        return round(((self.total_solved or 0) / attempts) * 100, 1)


class DailyChallenge(db.Model):
    """Daily featured coding challenge schedule."""
    __tablename__ = 'coding_daily_challenges'

    id = db.Column(db.Integer, primary_key=True)
    challenge_date = db.Column(db.Date, unique=True, nullable=False, index=True, default=date.today)
    problem_id = db.Column(db.Integer, db.ForeignKey('coding_problems.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    problem = db.relationship('CodingProblem')


class CodingBadge(db.Model):
    """Gamification badge definition."""
    __tablename__ = 'coding_badges'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(100), default='fa-medal')
    xp_bonus = db.Column(db.Integer, default=50)


class UserBadge(db.Model):
    """User awarded badges."""
    __tablename__ = 'coding_user_badges'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('coding_badges.id'), nullable=False, index=True)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

    badge = db.relationship('CodingBadge')
    user = db.relationship('User', backref=db.backref('coding_badges', lazy='dynamic'))

    __table_args__ = (db.UniqueConstraint('user_id', 'badge_id', name='uq_user_coding_badge'),)
