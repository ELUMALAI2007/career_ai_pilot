"""
CareerPilot AI - Settings Forms Module
WTForms for User Preferences, Account Password Changes, and Notification Toggles.
"""

from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length


class AccountSettingsForm(FlaskForm):
    """Change Password & Account Security Form."""
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(), 
        Length(min=8, message='Password must be at least 8 characters long.')
    ])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match.')
    ])
    submit = SubmitField('Change Password')


class NotificationSettingsForm(FlaskForm):
    """Notification & Preference Toggles Form."""
    email_notifications = BooleanField('Email Notifications')
    practice_reminders = BooleanField('Daily Practice Reminders')
    ai_recommendation_alerts = BooleanField('AI Strategy & Skill Gap Alerts')
    theme_mode = SelectField('UI Theme', choices=[('light', 'Light Mode'), ('dark', 'Dark Mode')])
    submit = SubmitField('Save Preferences')
