"""
CareerPilot AI - Admin Management Forms Module
WTForms for Administrative User Management and Platform Parameters.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class UserManagementForm(FlaskForm):
    """Admin User Edit Form."""
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    role = SelectField('User Role', choices=[('student', 'Student'), ('admin', 'Administrator')])
    is_active = BooleanField('Account Active')
    submit = SubmitField('Update User')


class SystemConfigForm(FlaskForm):
    """System Parameters Form."""
    site_notice = StringField('System Notice / Announcement', validators=[Length(max=255)])
    enable_ai_mock_interviews = BooleanField('Enable AI Mock Interviews')
    submit = SubmitField('Update System Configuration')
