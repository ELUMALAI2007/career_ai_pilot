"""
CareerPilot AI Setup Environment Helper Script
Checks Python version compatibility and dependencies.
"""

import sys
import subprocess

MIN_PYTHON_VERSION = (3, 10)

def check_python_version():
    """Validates Python version."""
    if sys.version_info < MIN_PYTHON_VERSION:
        print(f"Error: Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}+ is required.")
        sys.exit(1)
    print(f"Python version check passed: {sys.version.split()[0]}")

def setup_environment():
    """Installs required packages."""
    check_python_version()
    print("Installing requirements from requirements.txt...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Environment setup completed successfully.")

if __name__ == '__main__':
    setup_environment()
