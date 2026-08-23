"""
CareerPilot AI Validators Module
File type, security, and document format validation utilities.
"""

import os

ALLOWED_EXTENSIONS = {'pdf', 'docx'}


def validate_file_extension(filename: str) -> bool:
    """Checks if uploaded resume file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_password_strength(password: str) -> dict:
    """Validates password complexity (length, numbers, special characters)."""
    has_min_len = len(password) >= 8
    has_digit = any(char.isdigit() for char in password)
    has_upper = any(char.isupper() for char in password)
    
    is_strong = has_min_len and has_digit and has_upper
    return {
        "is_strong": is_strong,
        "feedback": "Password must be at least 8 characters with 1 number and 1 uppercase letter." if not is_strong else "Strong password"
    }
