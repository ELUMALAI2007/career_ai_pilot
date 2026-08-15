#!/bin/bash
# CareerPilot AI Linux Deployment Script

set -e

echo "Starting deployment for CareerPilot AI Assistant..."

# Pull latest code
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Database migrations
python database/init_db.py

# Restart systemd service
sudo systemctl restart careerpilot.service

echo "Deployment completed successfully!"
