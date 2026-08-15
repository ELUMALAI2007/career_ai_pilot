# CareerPilot AI

**CareerPilot AI** is an enterprise-grade AI-powered Placement Preparation and Career Guidance Platform built using Python, Flask Application Factory pattern, SQLAlchemy ORM, Flask-Login, Flask-WTF, Bootstrap 5, Chart.js, SQLite/MySQL, Google Gemini API, and clean architecture principles.

---

## 🌟 Key Features

* **AI-Powered Career Assistance**: Interactive AI career assistant and recommendation engine powered by Google Gemini API and scikit-learn models.
* **Resume Analyzer & Scoring**: Automated parsing of PDF/DOCX resumes, keyword extraction, ATS scoring, format analysis, and detailed feedback.
* **Aptitude Trainer & Mock Tests**: Practice modules, dynamic question generation, full-length timed mock tests, and performance analytics.
* **User Authentication & Google Sign-In**: Secure user registration, authentication, login management with Flask-Login, password hashing, and Google OAuth 2.0 integration.
* **Database & Progress Tracking**: SQLAlchemy ORM models for tracking test results, resume analysis history, skill gap reports, and user progress analytics.
* **Skill Gap & Learning Roadmap**: Identify target career roles, discover missing skills, and generate personalized learning roadmaps.
* **Interview Prep & Practice**: Simulated interview sessions, question banks, and dynamic question generation.

---

## 🛠️ Technology Stack

* **Backend**: Python 3.13+, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Flask-Bcrypt, Flask-Migrate, Flask-Mail
* **Frontend**: HTML5, CSS3 (Vanilla CSS + Bootstrap 5), JavaScript (ES6+), Chart.js
* **AI & Machine Learning**: Google Gemini API (`google-generativeai`), `scikit-learn`, `sentence-transformers`, `spacy`, `pandas`, `numpy`
* **File Parsing**: `PyPDF2`, `python-docx`
* **Database**: SQLite (default local) / MySQL (production)
* **Testing & Deployment**: `pytest`, `gunicorn`

---

## 📁 Project Structure

```text
career_ai_pilot/
├── .env.example              # Environment variables template (placeholders only)
├── .gitignore                # Git ignore rules for virtualenvs, secrets, logs, cache
├── README.md                 # Project documentation
├── config.py                 # Application configuration (Dev/Test/Prod)
├── requirements.txt          # Python dependencies
├── run.py                    # Application entry point
├── check_aptitude_bank.py    # Aptitude question bank checker script
├── generate_question_bank.py # Question bank generator script
├── app/
│   ├── __init__.py           # Application Factory (create_app)
│   ├── logging_config.py     # Application logger setup
│   ├── security.py           # Security headers & middleware
│   ├── ai/                   # AI services & ML models (Gemini API, Sklearn)
│   ├── errors/               # Custom error handlers (404, 500)
│   ├── forms/                # WTForms validation forms
│   ├── models/               # SQLAlchemy database models
│   ├── routes/               # Flask Blueprints (Auth, Resume, Aptitude, Admin, etc.)
│   ├── services/             # Core business logic & orchestration services
│   ├── static/               # CSS, JavaScript, images, uploads
│   ├── templates/            # HTML Jinja2 templates
│   └── utils/                # Helper utilities, validators, and decorators
├── database/                 # SQLite database storage & init scripts
├── docs/                     # Documentation & setup guides
├── logs/                     # Application log directory
├── question_generators/      # Dynamic question generation modules
├── scripts/                  # Helper & maintenance scripts
├── tests/                    # Unit and integration tests (pytest)
└── uploads/                  # User uploaded documents storage
```

---

## 🚀 Quick Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ELUMALAI2007/career_ai_pilot.git
cd career_ai_pilot
```

### 2. Set Up Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Variables Configuration

Copy `.env.example` to `.env` and fill in your actual configuration values:

```bash
cp .env.example .env
```

Example `.env` structure:

```env
FLASK_APP=run.py
FLASK_ENV=development
FLASK_RUN_HOST=127.0.0.1
FLASK_RUN_PORT=5000
SECRET_KEY=your_secret_key_here

DATABASE_URL=sqlite:///database/careerpilot.db

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=noreply@careerpilot.ai

ADMIN_EMAIL=admin@careerpilot.ai

GEMINI_API_KEY=your_google_gemini_api_key_here
GEMINI_MODEL_NAME=gemini-1.5-flash

GOOGLE_CLIENT_ID=your_google_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
APP_URL=http://127.0.0.1:5000
```

> ⚠️ **Security Notice**: Never commit your `.env` file to version control.

---

## 🏃 Running the Application

### Initialize Database

```bash
python database/init_db.py
```

### Start Development Server

```bash
python run.py
```

The application will be accessible at: `http://127.0.0.1:5000`

---

## 🧪 Testing

Run automated tests using `pytest`:

```bash
pytest tests/
```

---

## 🔮 Future Enhancements

* Expanded real-time mock video interview evaluations.
* Multi-language support for international career assessments.
* Enterprise ATS integration endpoints for corporate recruiting.
* Enhanced peer-to-peer coding practice rooms.

---

## 👥 Contributors

* **Elumalai M** - *Lead Developer & Architect* - [ELUMALAI2007](https://github.com/ELUMALAI2007)
