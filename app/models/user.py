"""
CareerPilot AI - User & Role Database Models
Defines user credentials, roles, profile relationships, and authentication interface.
"""

from datetime import datetime
from flask_login import UserMixin
from app import db, bcrypt


class Role(db.Model):
    """User Role database model."""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class User(db.Model, UserMixin):
    """User Account database model."""
    __tablename__ = 'users'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=True)  # Nullable for Google OAuth users
    google_id = db.Column(db.String(100), unique=True, nullable=True, index=True)
    profile_picture = db.Column(db.String(500), nullable=True)
    auth_provider = db.Column(db.String(20), default='local')  # 'local', 'google', 'both'
    status = db.Column(db.String(20), default='approved')       # 'pending', 'approved', 'rejected'
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    resumes = db.relationship('ResumeUpload', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    interviews = db.relationship('InterviewSession', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password: str):
        """Hashes and sets user password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Verifies password hash."""
        if not self.password_hash:
            return False
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def is_approved(self) -> bool:
        """Checks if user account is approved."""
        return self.status == 'approved'

    @property
    def is_pending(self) -> bool:
        """Checks if user account is pending approval."""
        return self.status == 'pending'

    @property
    def is_rejected(self) -> bool:
        """Checks if user account has been rejected."""
        return self.status == 'rejected'

    @property
    def is_admin(self) -> bool:
        """Checks if user has admin role."""
        return self.role is not None and self.role.name == 'admin'

    def __repr__(self):
        return f"<User id={self.id} email='{self.email}' status='{self.status}'>"
