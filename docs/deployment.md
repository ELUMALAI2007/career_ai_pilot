# Enterprise Deployment Guide - CareerPilot AI

## System Requirements
- Python 3.13+
- MySQL 8.0+ / SQLite 3.35+
- Nginx Web Server
- Gunicorn WSGI HTTP Server

## Production Launch Steps

### 1. Environment Setup
```bash
git clone <repository_url>
cd CareerPilot-AI
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Variables
Create `.env` file with production credentials:
```ini
FLASK_ENV=production
SECRET_KEY=<strong_random_secret_key>
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/careerpilot_prod
GEMINI_API_KEY=<production_api_key>
```

### 3. Initialize Production Database
```bash
python database/init_db.py
```

### 4. Systemd Service Configuration
Create `/etc/systemd/system/careerpilot.service`:
```ini
[Unit]
Description=Gunicorn instance for CareerPilot AI
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/CareerPilot-AI
Environment="PATH=/var/www/CareerPilot-AI/venv/bin"
ExecStart=/var/www/CareerPilot-AI/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:8000 run:app

[Install]
WantedBy=multi-user.target
```
