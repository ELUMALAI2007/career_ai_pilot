# CareerPilot AI Architecture Documentation

## Executive Overview
CareerPilot AI Assistant is designed as a modular, layered web application following clean software design practices:
`Client Browser (Bootstrap 5/Chart.js) <-> Flask Blueprints (Routes) <-> WTForms (Validation) <-> Service Abstraction Layer <-> AI Engine (Gemini LLM / spaCy / Scikit-Learn) <-> SQLAlchemy ORM Models <-> Database (SQLite/MySQL)`

## 18 Distinct Feature Modules
1. **Admin**: Platform oversight, user management, audit logging.
2. **AI Assistant**: Conversational placement guidance chatbot.
3. **Analytics**: Cumulative performance metrics & Chart.js radar charts.
4. **Aptitude**: Multiple choice practice sets across quantitative & verbal topics.
5. **Auth**: Candidate login, signup, session security.
6. **Coding**: Data structures and algorithm problem challenges.
7. **Communication**: Soft skills evaluation and tone feedback.
8. **Company Prep**: Placement round formats and peer experiences.
9. **Dashboard**: Central candidate cockpit and readiness rating.
10. **Interview**: Real-time AI mock technical & behavioral interviews.
11. **Job Eligibility**: Student CGPA, branch, and backlog criteria matching.
12. **Learning Roadmap**: Step-by-step preparation milestone timeline.
13. **Notification**: In-app alert notifications.
14. **Planner**: Daily study preparation checklist.
15. **Profile**: Academic and contact information management.
16. **Resume**: Document upload & Gemini ATS score analysis.
17. **Settings**: Security options and notification toggles.
18. **Skill Gap**: Role benchmark comparison and missing skill discovery.
