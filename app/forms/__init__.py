"""
CareerPilot AI Form Schemas Package
Exposes WTF Form validation classes for Auth, Profile, Practice, Settings, and Admin views.
"""

from app.forms.auth_forms import LoginForm, RegisterForm, ResetPasswordForm
from app.forms.profile_forms import UserProfileForm, EducationForm, ExperienceForm
from app.forms.practice_forms import TestFilterForm, AnswerSubmissionForm, MockInterviewForm
from app.forms.settings_forms import AccountSettingsForm, NotificationSettingsForm
from app.forms.admin_forms import UserManagementForm, SystemConfigForm

__all__ = [
    'LoginForm', 'RegisterForm', 'ResetPasswordForm',
    'UserProfileForm', 'EducationForm', 'ExperienceForm',
    'TestFilterForm', 'AnswerSubmissionForm', 'MockInterviewForm',
    'AccountSettingsForm', 'NotificationSettingsForm',
    'UserManagementForm', 'SystemConfigForm'
]
