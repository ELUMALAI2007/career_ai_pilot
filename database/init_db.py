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
    table_names = inspector.get_table_names()

    # User table migrations
    if 'users' in table_names:
        columns = [c['name'] for c in inspector.get_columns('users')]

        with db.engine.begin() as conn:
            if 'google_id' not in columns:
                print("Adding google_id column to users table...")
                conn.execute(text(
                    "ALTER TABLE users ADD COLUMN google_id VARCHAR(100)"
                ))

            if 'profile_picture' not in columns:
                print("Adding profile_picture column to users table...")
                conn.execute(text(
                    "ALTER TABLE users ADD COLUMN profile_picture VARCHAR(500)"
                ))

            if 'auth_provider' not in columns:
                print("Adding auth_provider column to users table...")
                conn.execute(text(
                    "ALTER TABLE users ADD COLUMN auth_provider VARCHAR(20) DEFAULT 'local'"
                ))

            if 'status' not in columns:
                print("Adding status column to users table...")
                conn.execute(text(
                    "ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'approved'"
                ))

            if 'is_verified' not in columns:
                print("Adding is_verified column to users table...")
                conn.execute(text(
                    "ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT 0"
                ))

            if 'last_login_at' not in columns:
                print("Adding last_login_at column to users table...")
                conn.execute(text(
                    "ALTER TABLE users ADD COLUMN last_login_at DATETIME"
                ))

    # Aptitude table migrations
    if 'aptitude_questions' in table_names:
        apt_cols = [
            c['name']
            for c in inspector.get_columns('aptitude_questions')
        ]

        with db.engine.begin() as conn:
            if 'is_active' not in apt_cols:
                print("Adding is_active column to aptitude_questions table...")
                conn.execute(text(
                    "ALTER TABLE aptitude_questions "
                    "ADD COLUMN is_active BOOLEAN DEFAULT 1"
                ))

            if 'updated_at' not in apt_cols:
                print("Adding updated_at column to aptitude_questions table...")
                conn.execute(text(
                    "ALTER TABLE aptitude_questions "
                    "ADD COLUMN updated_at DATETIME"
                ))

    # Coding table migrations
    if 'coding_problems' in table_names:
        coding_cols = [
            c['name']
            for c in inspector.get_columns('coding_problems')
        ]

        if 'topic' not in coding_cols:
            print("Re-creating coding_problems table with updated schema...")

            with db.engine.begin() as conn:
                conn.execute(text(
                    "DROP TABLE IF EXISTS coding_submissions"
                ))
                conn.execute(text(
                    "DROP TABLE IF EXISTS coding_bookmarks"
                ))
                conn.execute(text(
                    "DROP TABLE IF EXISTS coding_daily_challenges"
                ))
                conn.execute(text(
                    "DROP TABLE IF EXISTS coding_problems"
                ))

            # Recreate using the current SQLAlchemy models
            db.create_all()

    # Coding progress migration
    # Re-inspect because coding_problems may have been recreated above.
    inspector = inspect(db.engine)
    table_names = inspector.get_table_names()

    if 'coding_progress' in table_names:
        progress_cols = [
            c['name']
            for c in inspector.get_columns('coding_progress')
        ]

        if 'proctor_flags' not in progress_cols:
            print("Adding proctor_flags column to coding_progress table...")

            with db.engine.begin() as conn:
                conn.execute(text(
                    "ALTER TABLE coding_progress "
                    "ADD COLUMN proctor_flags INTEGER DEFAULT 0"
                ))

    # Interview question migration
    if 'interview_questions' in table_names:
        interview_question_cols = [
            c['name']
            for c in inspector.get_columns('interview_questions')
        ]

        if 'question' not in interview_question_cols:
            print("Migrating legacy interview_questions table...")

            with db.engine.begin() as conn:
                conn.execute(text(
                    "ALTER TABLE interview_questions "
                    "RENAME TO interview_questions_legacy"
                ))

            db.create_all()

            # Re-inspect after creating the new table.
            inspector = inspect(db.engine)

            if 'interview_questions_legacy' in inspector.get_table_names():
                legacy_cols = [
                    c['name']
                    for c in inspector.get_columns(
                        'interview_questions_legacy'
                    )
                ]

                if 'question_text' in legacy_cols:
                    with db.engine.begin() as conn:
                        conn.execute(text(
                            "INSERT INTO interview_questions "
                            "(question, role, interview_type, difficulty, "
                            "topic, company, is_active) "
                            "SELECT question_text, "
                            "'Software Developer', "
                            "'Technical', "
                            "'Medium', "
                            "'General', "
                            "NULL, "
                            "1 "
                            "FROM interview_questions_legacy "
                            "WHERE question_text IS NOT NULL "
                            "AND question_text != ''"
                        ))
    """Safely adds new columns to existing tables without dropping existing user data."""
    inspector = inspect(db.engine)
    table_names = inspector.get_table_names()
    
    with db.engine.connect() as conn:
        if 'users' in table_names:
            columns = [c['name'] for c in inspector.get_columns('users')]
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

    if 'coding_problems' in table_names:
            coding_cols = [c['name'] for c in inspector.get_columns('coding_problems')]
            if 'topic' not in coding_cols:
                print("Re-creating coding_problems table with updated schema...")
                conn.execute(text("DROP TABLE IF EXISTS coding_submissions"))
                conn.execute(text("DROP TABLE IF EXISTS coding_bookmarks"))
                conn.execute(text("DROP TABLE IF EXISTS coding_daily_challenges"))
                conn.execute(text("DROP TABLE IF EXISTS coding_problems"))

    if 'coding_progress' in table_names:
            progress_cols = [c['name'] for c in inspector.get_columns('coding_progress')]
            if 'proctor_flags' not in progress_cols:
                print("Adding proctor_flags column to coding_progress table...")
                conn.execute(text("ALTER TABLE coding_progress ADD COLUMN proctor_flags INTEGER DEFAULT 0"))

    if 'interview_questions' in table_names:
            interview_question_cols = [c['name'] for c in inspector.get_columns('interview_questions')]
            if 'question' not in interview_question_cols:
                print("Migrating legacy interview_questions table...")
                conn.execute(text("ALTER TABLE interview_questions RENAME TO interview_questions_legacy"))

    conn.commit()

    if 'interview_questions' in table_names:
        interview_question_cols = [c['name'] for c in inspector.get_columns('interview_questions')]
        if 'question' not in interview_question_cols:
            db.create_all()
            with db.engine.begin() as conn:
                if 'question_text' in interview_question_cols:
                    conn.execute(text(
                        "INSERT INTO interview_questions "
                        "(question, role, interview_type, difficulty, topic, company, is_active) "
                        "SELECT question_text, 'Software Developer', 'Technical', 'Medium', "
                        "'General', NULL, 1 FROM interview_questions_legacy "
                        "WHERE question_text IS NOT NULL AND question_text != ''"
                    ))


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
        # Seed Coding & DSA Challenges
        try:
            from database.seed_coding import seed_coding_database
            seed_coding_database()
        except Exception as e:
            print(f"Notice during coding seeding: {e}")

        # Seed Aptitude Question Bank if empty
        from app.models.aptitude import AptitudeQuestion
        if AptitudeQuestion.query.count() == 0:
            print("Seeding 1,000 verified Aptitude questions into database...")
            from generate_question_bank import generate_batch
            generate_batch()

        print("Database initialization completed successfully.")


if __name__ == '__main__':
    init_database()
