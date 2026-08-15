"""
CareerPilot AI - Authentication Forms Module
WTForms for User Registration, Login, and Password Reset workflows.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError


from app.models.user import User


class LoginForm(FlaskForm):
    """User Login Form Schema."""
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    """User Registration Form Schema."""
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=8, message='Password must be at least 8 characters long.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Create Account')

    def validate_email(self, email):
        """Ensures email is not already registered."""
        user = User.query.filter_by(email=email.data.strip().lower()).first()
        if user:
            raise ValidationError('This email address is already registered. Please sign in instead.')



class ResetPasswordForm(FlaskForm):
    """Password Reset Form Schema."""
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Password Reset Link')
