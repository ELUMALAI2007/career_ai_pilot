"""
CareerPilot AI — Idempotent Admin Seeding Script (`seed_admin.py`)
Ensures the default administrator account (admin@careerpilot.ai) exists in the database with hashed password.
IDEMPOTENCY GUARANTEE: If admin account already exists, existing password hash is NEVER overwritten or reset.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.user import User, Role
from config import Config

app = create_app(Config)


def seed_admin_account(app_instance=None):
    """Seeds default admin account idempotently."""
    from flask import has_app_context, current_app

    if has_app_context():
        _execute_seed()
    else:
        target_app = app_instance or app
        with target_app.app_context():
            _execute_seed()


def _execute_seed():
    # Ensure database tables exist
    db.create_all()

    # 1. Ensure admin role exists
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', description='Platform Administrator')
        db.session.add(admin_role)
        db.session.commit()

    admin_email = "admin@careerpilot.ai".strip().lower()
    admin_user = User.query.filter_by(email=admin_email).first()

    if admin_user:
        print(f"[OK] Admin account '{admin_email}' already exists (ID: {admin_user.id}). Password hash left untouched.")
    else:
        admin_user = User(
            full_name='System Administrator',
            email=admin_email,
            role_id=admin_role.id,
            status='approved',
            auth_provider='local',
            is_active=True,
            is_verified=True
        )
        admin_user.set_password('AdminSecure123!')
        db.session.add(admin_user)
        db.session.commit()
        print(f"[SUCCESS] Seeded default admin account: {admin_email} / AdminSecure123!")


if __name__ == '__main__':
    seed_admin_account()
