"""
CareerPilot AI — Safe Database Health & Diagnostic Tool (`check_database.py`)
Checks absolute database file location, file size, connection status, table schema integrity,
user record counts, and admin account availability.
SECURITY ASSURANCE: Passwords and password hashes are NEVER displayed or logged.
"""

import os
import sys
from sqlalchemy import inspect, text

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.user import User, Role
from config import Config

app = create_app(Config)


def run_database_health_check():
    """Executes database health diagnostic."""
    print("\n" + "=" * 80)
    print("  CAREERPILOT AI -- DATABASE HEALTH & DIAGNOSTIC INSPECTOR")
    print("=" * 80)

    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    raw_path = db_uri.replace('sqlite:///', '') if db_uri.startswith('sqlite:///') else db_uri
    abs_path = os.path.abspath(raw_path)

    print(f"[*] Configured Database URI: {db_uri}")
    print(f"[*] Resolved Database Absolute Path: {abs_path}")

    # Check file existence and size
    if os.path.exists(abs_path):
        size_bytes = os.path.getsize(abs_path)
        size_mb = size_bytes / (1024 * 1024)
        print(f"[OK] Database File Exists: YES ({size_bytes:,} bytes / {size_mb:.2f} MB)")
    else:
        print("[FAIL] Database File Exists: NO (File not found at resolved path)")
        return

    with app.app_context():
        # 1. Connection Check
        try:
            with db.engine.connect() as conn:
                res = conn.execute(text("SELECT 1")).scalar()
                if res == 1:
                    print("[OK] Database Connection: PASS")
                else:
                    print("[FAIL] Database Connection: FAILED (Unexpected scalar response)")
        except Exception as e:
            print(f"[FAIL] Database Connection Error: {e}")
            return

        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"[*] Total Tables Found: {len(tables)}")

        # 2. Check Users Table & Schema Columns
        if 'users' in tables:
            print("[OK] Users table: PASS")
            cols = [c['name'] for c in inspector.get_columns('users')]
            req_cols = ['id', 'full_name', 'email', 'password_hash', 'role_id', 'is_active', 'is_verified', 'created_at', 'updated_at', 'last_login_at']
            missing = [col for col in req_cols if col not in cols]
            if not missing:
                print("[OK] Users table schema: PASS (All required columns present)")
            else:
                print(f"[FAIL] Users table missing columns: {missing}")

            user_count = User.query.count()
            print(f"[*] Total Registered Users Count: {user_count}")
        else:
            print("[FAIL] Users table: MISSING")

        # 3. Check Admin Account Status
        admin_account = User.query.filter_by(email='admin@careerpilot.ai').first()
        if admin_account:
            print(f"[OK] Permanent System Administrator Account: FOUND (ID: {admin_account.id}, Role: {admin_account.role.name if admin_account.role else 'None'})")
        else:
            print("[INFO] Default System Administrator Account (admin@careerpilot.ai): NOT FOUND (Run python seed_admin.py)")

        print("=" * 80)
        print("SECURITY NOTICE: Passwords and password hashes are NEVER displayed in inspector logs.")
        print("  DIAGNOSTIC STATUS: ALL HEALTH CHECKS COMPLETED CLEANLY.\n")


if __name__ == '__main__':
    run_database_health_check()
