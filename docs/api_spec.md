# CareerPilot AI API Endpoint Specification

## Authentication Endpoints (`/auth`)
- `POST /auth/login`: Authenticates user credentials.
- `POST /auth/register`: Registers a new candidate user account.
- `GET /auth/logout`: Terminates current user session.

## AI Assistant Endpoints (`/assistant`)
- `POST /assistant/chat`: Accepts `{ "query": "string", "session_id": int }` and returns AI responses.

## Resume Analyzer Endpoints (`/resume`)
- `POST /resume/`: Accepts multipart `resume_file` (PDF/DOCX) and returns ATS score report.

## Mock Interview Endpoints (`/interview`)
- `POST /interview/`: Accepts target role and difficulty to spawn a new AI mock interview session.
