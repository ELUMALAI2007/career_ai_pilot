"""
CareerPilot AI — User Inspection Script (`check_users.py`)
Safely lists all registered user accounts from the persistent database without exposing passwords or password hashes.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.user import User
from config import Config

app = create_app(Config)


def inspect_users():
    """Queries and prints formatted summary of registered user accounts."""
    with app.app_context():
        users = User.query.order_by(User.id.asc()).all()
        total_count = len(users)

        print("\n" + "=" * 105)
        print(f"  CAREERPILOT AI -- DATABASE USER ACCOUNTS INSPECTOR (Total: {total_count})")
        print("=" * 105)
        header = f"{'ID':<5} | {'Full Name':<25} | {'Email':<35} | {'Role':<10} | {'Status':<10} | {'Created At':<19}"
        print(header)
        print("-" * 105)

        for u in users:
            role_name = u.role.name if u.role else "None"
            created_str = u.created_at.strftime("%Y-%m-%d %H:%M") if u.created_at else "N/A"
            row = f"{u.id:<5} | {u.full_name[:24]:<25} | {u.email[:34]:<35} | {role_name:<10} | {u.status:<10} | {created_str:<19}"
            print(row)

        print("=" * 105)
        print("SECURITY NOTICE: Passwords and password hashes are NEVER displayed in inspector logs.\n")


if __name__ == "__main__":
    inspect_users()
