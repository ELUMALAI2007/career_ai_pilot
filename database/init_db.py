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
            if 'is_verified' not in columns:
                print("Adding is_verified column to users table...")
                conn.execute(text("ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT 0"))
            if 'last_login_at' not in columns:
                print("Adding last_login_at column to users table...")
                conn.execute(text("ALTER TABLE users ADD COLUMN last_login_at DATETIME"))
            conn.commit()

    if 'aptitude_questions' in inspector.get_table_names():
        apt_cols = [c['name'] for c in inspector.get_columns('aptitude_questions')]
        with db.engine.connect() as conn:
            if 'is_active' not in apt_cols:
                print("Adding is_active column to aptitude_questions table...")
                conn.execute(text("ALTER TABLE aptitude_questions ADD COLUMN is_active BOOLEAN DEFAULT 1"))
            if 'updated_at' not in apt_cols:
                print("Adding updated_at column to aptitude_questions table...")
                conn.execute(text("ALTER TABLE aptitude_questions ADD COLUMN updated_at DATETIME"))
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

        # Backfill any existing users without a role_id
        unassigned_users = User.query.filter_by(role_id=None).all()
        for u in unassigned_users:
            if 'admin' in u.email.lower():
                u.role_id = admin_role.id
            else:
                u.role_id = student_role.id
        if unassigned_users:
            db.session.commit()
            print(f"Updated {len(unassigned_users)} user(s) with default roles.")

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

        # Seed Aptitude Question Bank if empty
        from app.models.aptitude import AptitudeQuestion
        if AptitudeQuestion.query.count() == 0:
            print("Seeding 1,000 verified Aptitude questions into database...")
            from generate_question_bank import generate_batch
            generate_batch()

        print("Database initialization completed successfully.")


if __name__ == '__main__':
    init_database()
