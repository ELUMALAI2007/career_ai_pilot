"""
CareerPilot AI - Profile Forms Module
WTForms for Candidate Personal Profile, Academic Details, and Work Experience.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Optional, Length


class UserProfileForm(FlaskForm):
    """User Personal Profile Form."""
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    headline = StringField('Professional Headline', validators=[Optional(), Length(max=150)])
    bio = TextAreaField('Bio / Summary', validators=[Optional(), Length(max=500)])
    target_role = StringField('Target Job Role', validators=[Optional(), Length(max=100)])
    linkedin_url = StringField('LinkedIn URL', validators=[Optional(), Length(max=255)])
    github_url = StringField('GitHub URL', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Update Profile')


class EducationForm(FlaskForm):
    """Education History Form."""
    degree = StringField('Degree / Qualification', validators=[DataRequired(), Length(max=100)])
    institution = StringField('Institution Name', validators=[DataRequired(), Length(max=150)])
    field_of_study = StringField('Field of Study', validators=[DataRequired(), Length(max=100)])
    cgpa = FloatField('CGPA / Percentage', validators=[DataRequired()])
    passout_year = StringField('Passout Year', validators=[DataRequired(), Length(max=4)])
    submit = SubmitField('Save Education')


class ExperienceForm(FlaskForm):
    """Work Experience Form."""
    company = StringField('Company Name', validators=[DataRequired(), Length(max=150)])
    role = StringField('Job Title / Role', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Responsibilities & Accomplishments', validators=[Optional()])
    submit = SubmitField('Save Experience')
