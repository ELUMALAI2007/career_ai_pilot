"""
CareerPilot AI Assistant Configuration Module
Defines base, development, testing, and production environment settings.
"""

import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base Configuration Class."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key_careerpilot_ai_super_secure_2026')
    
    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # Database connection string (default SQLite, configurable to MySQL)
    # Automatically resolves relative SQLite URLs to absolute paths to prevent Windows CWD path errors
    _raw_db_url = os.environ.get('DATABASE_URL', '')
    if _raw_db_url and _raw_db_url.startswith('sqlite:///') and not os.path.isabs(_raw_db_url.replace('sqlite:///', '')):
        _rel_path = _raw_db_url.replace('sqlite:///', '')
        _abs_path = os.path.abspath(os.path.join(BASE_DIR, _rel_path)).replace('\\', '/')
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{_abs_path}"
    else:
        SQLALCHEMY_DATABASE_URI = _raw_db_url or ('sqlite:///' + os.path.join(BASE_DIR, 'database', 'careerpilot.db').replace('\\', '/'))


    # File uploads setup
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file limit

    # Session & Security settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in Production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Mail configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@careerpilot.ai')

    # Gemini AI configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    GEMINI_MODEL_NAME = os.environ.get('GEMINI_MODEL_NAME', 'gemini-1.5-flash')

    # Google OAuth 2.0 Credentials & Base URL
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '')
    APP_URL = os.environ.get('APP_URL', 'http://127.0.0.1:5000')

    # Administrator Contact Email for Access Approvals
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@careerpilot.ai')

    # Application settings
    SITE_NAME = "CareerPilot AI Assistant"


class DevelopmentConfig(Config):
    """Development Environment Configuration."""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing Environment Configuration."""
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production Environment Configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    # TODO: Configure production logging and database pooling parameters


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
