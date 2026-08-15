"""
CareerPilot AI Database Initialization & Migration Script
Creates database tables, applies schema migrations, and seeds initial roles and administrator accounts.
"""

import os
import sys
from sqlalchemy import inspect, text

# Ensure root workspace is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User, Role
from config import DevelopmentConfig

app = create_app(DevelopmentConfig)


def apply_schema_migrations():
    """Safely adds new columns to existing tables without dropping existing user data."""
    inspector = inspect(db.engine)
    if 'users' in inspector.get_table_names():
        columns = [c['name'] for c in inspector.get_columns('users')]
        with db.engine.connect() as conn:
            if 'google_id' not in columns:
                print("Adding google_id column to users table...")
                conn.execute(text("ALTER TABLE users ADD COLUMN google_id VARCHAR(100)"))
            if 'profile_picture' not in columns:
                print("Adding profile_picture column to users table...")
                conn.execute(text("ALTER TABLE users ADD COLUMN profile_picture VARCHAR(500)"))
            if 'auth_provider' not in columns:
                print("Adding auth_provider column to users table...")
                conn.execute(text("ALTER TABLE users ADD COLUMN auth_provider VARCHAR(20) DEFAULT 'local'"))
            if 'status' not in columns:
                print("Adding status column to users table...")
                conn.execute(text("ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'approved'"))
            conn.commit()


def init_database():
    """Initializes schema tables, applies migrations, and seeds default dataset."""
    with app.app_context():
        print("Creating all database tables...")
        db.create_all()

        print("Applying schema migrations...")
        apply_schema_migrations()

        # Seed Roles
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', description='Platform Administrator')
            db.session.add(admin_role)

        student_role = Role.query.filter_by(name='student').first()
        if not student_role:
            student_role = Role(name='student', description='Placement Candidate Student')
            db.session.add(student_role)

        db.session.commit()

        # Seed Default Admin Account
        admin_user = User.query.filter_by(email='admin@careerpilot.ai').first()
        if not admin_user:
            admin_user = User(
                full_name='System Administrator',
                email='admin@careerpilot.ai',
                role_id=admin_role.id,
                status='approved',
                auth_provider='local'
            )
            admin_user.set_password('AdminSecure123!')
            db.session.add(admin_user)
            db.session.commit()
            print("Admin account seeded: admin@careerpilot.ai / AdminSecure123!")

        print("Database initialization completed successfully.")


if __name__ == '__main__':
    init_database()
