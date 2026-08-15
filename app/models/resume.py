"""
CareerPilot AI - Resume Intelligence & ATS Models
Database models for uploads, extracted data, ATS & quality evaluations, version history, questions, and interview sessions.
"""

from datetime import datetime
import json
from app import db


class ResumeUpload(db.Model):
    """Uploaded resume document metadata and version tracking."""
    __tablename__ = 'resume_uploads'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size_bytes = db.Column(db.Integer, default=0)
    mime_type = db.Column(db.String(100), default='application/pdf')
    target_role = db.Column(db.String(100), default='Software Engineer')
    target_company = db.Column(db.String(100), default='General Placement')
    job_description = db.Column(db.Text, default='')
    version_number = db.Column(db.Integer, default=1)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    analyses = db.relationship('ResumeAnalysis', backref='resume', cascade='all, delete-orphan')
    questions = db.relationship('ResumeQuestion', backref='resume', cascade='all, delete-orphan')
    interview_sessions = db.relationship('ResumeInterviewSession', backref='resume', cascade='all, delete-orphan')


class ResumeAnalysis(db.Model):
    """Full multidimensional ATS & Resume Intelligence evaluation report."""
    __tablename__ = 'resume_analyses'

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume_uploads.id'), nullable=False)
    
    # Sub-scores
    overall_score = db.Column(db.Float, default=0.0)
    ats_score = db.Column(db.Float, default=0.0)
    quality_score = db.Column(db.Float, default=0.0)
    job_match_score = db.Column(db.Float, default=0.0)
    completeness_score = db.Column(db.Float, default=0.0)

    # JSON Data Breakdowns
    parsed_data_json = db.Column(db.Text)      # Contact info, sections, parsed skills, education, projects, etc.
    keyword_analysis_json = db.Column(db.Text) # Found, Partial, Missing, Top 10 additions
    skills_analysis_json = db.Column(db.Text)  # Skill match %, high/medium/low priority skill gaps
    bullets_analysis_json = db.Column(db.Text) # Verb quality, metric counts, before/after recommendations
    project_analysis_json = db.Column(db.Text) # Project strength scores, tech stack extraction
    red_flags_json = db.Column(db.Text)        # Recruiter red flags
    strengths_json = db.Column(db.Text)        # Identified core strengths
    priority_plan_json = db.Column(db.Text)    # Actionable "Fix These First" plan (High, Medium, Low)
    formatting_json = db.Column(db.Text)       # Page count, formatting risks, whitespace
    language_json = db.Column(db.Text)         # Language quality score, grammar notes
    
    # Qualitative & Summary Text
    recruiter_impression = db.Column(db.Text)
    summary_rewrite = db.Column(db.Text)
    evaluated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Helper getters/setters for JSON payloads
    def get_parsed_data(self):
        return json.loads(self.parsed_data_json) if self.parsed_data_json else {}

    def get_keyword_analysis(self):
        return json.loads(self.keyword_analysis_json) if self.keyword_analysis_json else {}

    def get_skills_analysis(self):
        return json.loads(self.skills_analysis_json) if self.skills_analysis_json else {}

    def get_bullets_analysis(self):
        return json.loads(self.bullets_analysis_json) if self.bullets_analysis_json else {}

    def get_project_analysis(self):
        return json.loads(self.project_analysis_json) if self.project_analysis_json else {}

    def get_red_flags(self):
        return json.loads(self.red_flags_json) if self.red_flags_json else []

    def get_strengths(self):
        return json.loads(self.strengths_json) if self.strengths_json else []

    def get_priority_plan(self):
        return json.loads(self.priority_plan_json) if self.priority_plan_json else {}

    def get_formatting(self):
        return json.loads(self.formatting_json) if self.formatting_json else {}

    def get_language(self):
        return json.loads(self.language_json) if self.language_json else {}


class ResumeQuestion(db.Model):
    """Verified interview question generated directly from candidate's resume content."""
    __tablename__ = 'resume_questions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume_uploads.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='Project Questions') # Project, Tech, Skill, Experience, HR, Deep-Dive
    difficulty = db.Column(db.String(30), default='intermediate') # beginner, intermediate, advanced, expert
    related_section = db.Column(db.String(100), default='General')
    related_skill = db.Column(db.String(100), default='')
    sample_answer_hint = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ResumeInterviewSession(db.Model):
    """Interactive 'Interview Me From My Resume' mock session state."""
    __tablename__ = 'resume_interview_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume_uploads.id'), nullable=False)
    target_role = db.Column(db.String(100), default='Software Engineer')
    total_questions = db.Column(db.Integer, default=5)
    current_question_index = db.Column(db.Integer, default=0)
    score = db.Column(db.Float, default=0.0)
    is_completed = db.Column(db.Boolean, default=False)
    feedback_json = db.Column(db.Text)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    messages = db.relationship('ResumeInterviewMessage', backref='session', cascade='all, delete-orphan')


class ResumeInterviewMessage(db.Model):
    """Transcript messages in an interactive resume mock interview session."""
    __tablename__ = 'resume_interview_messages'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('resume_interview_sessions.id'), nullable=False)
    sender = db.Column(db.String(20), nullable=False) # 'interviewer' or 'candidate'
    message = db.Column(db.Text, nullable=False)
    question_index = db.Column(db.Integer, default=0)
    score = db.Column(db.Float)
    feedback = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
