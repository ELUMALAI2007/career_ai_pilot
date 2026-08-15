"""
CareerPilot AI - Practice Forms Module
WTForms for Aptitude Filters, Code Submissions, and Mock Interview Setup.
"""

from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional


class TestFilterForm(FlaskForm):
    """Filter Aptitude / Technical Practice Tests."""
    category = SelectField('Category', choices=[
        ('all', 'All Categories'),
        ('quantitative', 'Quantitative Aptitude'),
        ('logical', 'Logical Reasoning'),
        ('verbal', 'Verbal Ability'),
        ('technical', 'Core Technical')
    ])
    difficulty = SelectField('Difficulty', choices=[
        ('all', 'All Levels'),
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ])
    submit = SubmitField('Apply Filter')


class AnswerSubmissionForm(FlaskForm):
    """Submit Question Answer Form."""
    selected_option = StringField('Selected Option', validators=[DataRequired()])
    code_body = TextAreaField('Code Submission', validators=[Optional()])
    submit = SubmitField('Submit Answer')


class MockInterviewForm(FlaskForm):
    """Mock AI Interview Session Setup Form."""
    target_role = StringField('Target Role / Position', validators=[DataRequired()])
    target_company = StringField('Target Company', validators=[Optional()])
    difficulty = SelectField('Interview Difficulty', choices=[
        ('junior', 'Junior / Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior / Lead Level')
    ])
    submit = SubmitField('Start AI Interview Session')
