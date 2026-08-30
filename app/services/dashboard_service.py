"""
CareerPilot AI — Placement Command Center Dashboard Service
Aggregates real-time candidate statistics, time-based greetings, daily target checklists,
AI recommendations, last active continuation targets, and recent activity logs.
Single Source of Truth: Uses AnalyticsService for readiness consistency.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List
from app import db
from app.models.user import User
from app.models.aptitude import AptitudeAttempt, AptitudeTestResult
from app.models.coding import CodingSubmission
from app.models.communication import CommunicationAssessment
from app.models.interview import InterviewSession
from app.models.resume import ResumeUpload, ResumeAnalysis
from app.services.analytics_service import AnalyticsService


class DashboardService:
    """Master Dashboard Service powering candidate Placement Command Center."""

    @classmethod
    def get_dashboard_summary(cls, user_id: int) -> Dict[str, Any]:
        """Constructs complete Placement Command Center payload for authenticated user."""
        user = db.session.get(User, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")

        # 1. Fetch Master Intelligence payload from AnalyticsService (Single Source of Truth)
        intel = AnalyticsService.compute_placement_intelligence(user_id)

        # 2. Greeting & Time-of-day
        greeting = cls._generate_greeting(user.full_name)

        # 3. Real Recent Activity Feed
        recent_activities = cls._get_recent_activities(user_id)

        # 4. Today's Target Checklist & Progress
        today_targets = cls._generate_todays_targets(intel, recent_activities)

        # 5. AI Daily Recommendation
        ai_recommendation = cls._generate_ai_recommendation(intel)

        # 6. Continue Where You Left Off Target
        continue_target = cls._get_continue_target(user_id, recent_activities)

        # 7. Profile Completion Percentage
        profile_completion = cls._compute_profile_completion(user)

        return {
            "user_id": user_id,
            "user_name": user.full_name,
            "greeting": greeting,
            "intelligence": intel,
            "today_targets": today_targets,
            "ai_recommendation": ai_recommendation,
            "continue_target": continue_target,
            "recent_activities": recent_activities,
            "profile_completion": profile_completion,
            "streak_days": intel["modules"]["consistency"].get("streak_days", 0)
        }

    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_greeting(full_name: str) -> str:
        """Generates dynamic time-of-day greeting (Morning / Afternoon / Evening)."""
        current_hour = datetime.now().hour
        first_name = full_name.split()[0] if full_name else "Candidate"

        if 5 <= current_hour < 12:
            time_str = "Good morning"
        elif 12 <= current_hour < 17:
            time_str = "Good afternoon"
        else:
            time_str = "Good evening"

        return f"{time_str}, {first_name} 👋"

    @classmethod
    def _get_recent_activities(cls, user_id: int) -> List[Dict[str, Any]]:
        """Queries actual database attempt logs across modules and formats timeline."""
        activities = []

        # Aptitude Results / Attempts
        apt_result = AptitudeTestResult.query.filter_by(user_id=user_id).order_by(AptitudeTestResult.completed_at.desc()).first()
        if apt_result:
            activities.append({
                "type": "aptitude",
                "icon": "fa-calculator text-primary",
                "title": f"Completed {apt_result.title or 'Aptitude Test'}",
                "timestamp": apt_result.completed_at,
                "time_str": cls._format_time_ago(apt_result.completed_at),
                "status": f"Score: {apt_result.accuracy_percentage}%"
            })

        # Coding Submissions
        code_sub = CodingSubmission.query.filter_by(user_id=user_id).order_by(CodingSubmission.submitted_at.desc()).first()
        if code_sub:
            activities.append({
                "type": "coding",
                "icon": "fa-code text-success",
                "title": f"Submitted {code_sub.problem.title if code_sub.problem else 'Coding Challenge'}",
                "timestamp": code_sub.submitted_at,
                "time_str": cls._format_time_ago(code_sub.submitted_at),
                "status": f"Status: {code_sub.status}"
            })

        # Communication Assessments
        comm_sub = CommunicationAssessment.query.filter_by(user_id=user_id).order_by(CommunicationAssessment.created_at.desc()).first()
        if comm_sub:
            activities.append({
                "type": "communication",
                "icon": "fa-comments text-info",
                "title": f"Completed {comm_sub.assessment_type.capitalize()} Soft Skills Practice",
                "timestamp": comm_sub.created_at,
                "time_str": cls._format_time_ago(comm_sub.created_at),
                "status": f"Clarity: {comm_sub.clarity_score}/100"
            })

        # Mock Interviews
        interview_sub = InterviewSession.query.filter_by(user_id=user_id).order_by(InterviewSession.created_at.desc()).first()
        if interview_sub:
            activities.append({
                "type": "interview",
                "icon": "fa-user-tie text-warning",
                "title": f"Mock Interview — {interview_sub.role}",
                "timestamp": interview_sub.created_at,
                "time_str": cls._format_time_ago(interview_sub.created_at),
                "status": f"Rating: {interview_sub.overall_score}/100"
            })

        # Resume Uploads
        resume_sub = ResumeUpload.query.filter_by(user_id=user_id).order_by(ResumeUpload.uploaded_at.desc()).first()
        if resume_sub:
            activities.append({
                "type": "resume",
                "icon": "fa-file-contract text-primary",
                "title": f"Resume Analyzed ({resume_sub.filename})",
                "timestamp": resume_sub.uploaded_at,
                "time_str": cls._format_time_ago(resume_sub.uploaded_at),
                "status": "ATS Evaluated"
            })

        # Sort combined timeline descending
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        return activities[:5]

    @staticmethod
    def _generate_todays_targets(intel: dict, activities: list) -> Dict[str, Any]:
        """Generates personalized 3-item daily checklist based on candidate's real data."""
        weaknesses = intel.get("weaknesses", [])
        modules = intel.get("modules", {})
        
        items = []

        # Item 1: Resume or Aptitude Target
        if modules.get("resume", {}).get("status") != "Available":
            items.append({
                "id": 1,
                "title": "Analyze Resume with ATS Evaluator",
                "category": "Resume",
                "completed": False,
                "url": "/resume/"
            })
        elif modules.get("aptitude", {}).get("status") != "Available":
            items.append({
                "id": 1,
                "title": "Complete 10 Quantitative Aptitude questions",
                "category": "Aptitude",
                "completed": False,
                "url": "/aptitude/"
            })
        else:
            items.append({
                "id": 1,
                "title": f"Practice {modules['aptitude'].get('weak_topic', 'Probability')} practice set",
                "category": "Aptitude",
                "completed": len(activities) > 0 and activities[0]["type"] == "aptitude",
                "url": "/aptitude/"
            })

        # Item 2: Coding Target
        if modules.get("coding", {}).get("status") != "Available":
            items.append({
                "id": 2,
                "title": "Solve 2 Easy/Medium DSA coding problems",
                "category": "Coding",
                "completed": False,
                "url": "/coding/"
            })
        else:
            items.append({
                "id": 2,
                "title": "Solve 2 Data Structures & Algorithm problems",
                "category": "Coding",
                "completed": len(activities) > 0 and activities[0]["type"] == "coding",
                "url": "/coding/"
            })

        # Item 3: Soft Skills or Mock Interview Target
        if modules.get("communication", {}).get("status") != "Available":
            items.append({
                "id": 3,
                "title": "Practice 15-minute Communication & Soft Skills set",
                "category": "Communication",
                "completed": False,
                "url": "/communication/"
            })
        else:
            items.append({
                "id": 3,
                "title": "Launch AI Mock Interview session for target role",
                "category": "Mock Interview",
                "completed": len(activities) > 0 and activities[0]["type"] == "interview",
                "url": "/interview/"
            })

        completed_count = sum(1 for item in items if item["completed"])

        return {
            "checklist": items,
            "completed_count": completed_count,
            "total_count": len(items),
            "progress_pct": round((completed_count / len(items)) * 100, 1)
        }

    @staticmethod
    def _generate_ai_recommendation(intel: dict) -> Dict[str, Any]:
        """Factual, personalized recommendation string based on candidate's lowest scoring active domain."""
        modules = intel.get("modules", {})
        weaknesses = intel.get("weaknesses", [])

        # Priority 1: Resume missing
        if modules.get("resume", {}).get("status") != "Available":
            return {
                "title": "Upload & Evaluate Your Resume",
                "text": "Your placement profile is missing a parsed resume. Uploading your CV generates ATS compatibility scores and role skill mapping.",
                "action_text": "Analyze Resume",
                "action_url": "/resume/",
                "badge": "High Priority"
            }

        # Priority 2: Aptitude missing
        if modules.get("aptitude", {}).get("status") != "Available":
            return {
                "title": "Complete Initial Aptitude Test",
                "text": "Aptitude assessments evaluate your Quantitative, Logical, and Verbal speed for campus hiring drives.",
                "action_text": "Take Aptitude Test",
                "action_url": "/aptitude/",
                "badge": "High Priority"
            }

        # Priority 3: Coding missing
        if modules.get("coding", {}).get("status") != "Available":
            return {
                "title": "Start DSA Coding Challenges",
                "text": "Submit code solutions in Python, C++, or Java to establish your Data Structures and Algorithms rating.",
                "action_text": "Practice Coding",
                "action_url": "/coding/",
                "badge": "High Priority"
            }

        # Dynamic lowest active score recommendation
        active_scores = [
            ("Coding & DSA", modules.get("coding", {}).get("score") if modules.get("coding", {}).get("score") is not None else 100.0, "/coding/", "Focus on Array and Tree DSA problems today to boost your placement score."),
            ("Communication", modules.get("communication", {}).get("score") if modules.get("communication", {}).get("score") is not None else 100.0, "/communication/", "Practice STAR-format verbal responses to improve interview confidence."),
            ("Aptitude", modules.get("aptitude", {}).get("score") if modules.get("aptitude", {}).get("score") is not None else 100.0, "/aptitude/", "Complete Probability and Logical Reasoning practice sets today."),
            ("Mock Interview", modules.get("interview", {}).get("score") if modules.get("interview", {}).get("score") is not None else 100.0, "/interview/", "Launch an AI Mock Interview session to refine technical question answering.")
        ]
        
        # Sort by score ascending
        active_scores.sort(key=lambda x: float(x[1]))
        lowest = active_scores[0]

        return {
            "title": f"Focus on {lowest[0]}",
            "text": lowest[3],
            "action_text": f"Practice {lowest[0]}",
            "action_url": lowest[2],
            "badge": "Recommended"
        }

    @staticmethod
    def _get_continue_target(user_id: int, activities: list) -> Dict[str, Any]:
        """Detects candidate's latest active attempt or default starter guide."""
        if not activities:
            return {
                "title": "Start Your CareerPilot AI Journey",
                "sub_title": "Take your first assessment to build your placement readiness profile",
                "progress_pct": 0,
                "action_text": "Start Aptitude Assessment",
                "action_url": "/aptitude/"
            }

        latest = activities[0]
        act_type = latest["type"]

        if act_type == "coding":
            return {
                "title": "Data Structures & Algorithms Practice",
                "sub_title": latest["title"],
                "progress_pct": 65,
                "action_text": "Continue Coding",
                "action_url": "/coding/"
            }
        elif act_type == "aptitude":
            return {
                "title": "Quantitative & Logical Reasoning",
                "sub_title": latest["title"],
                "progress_pct": 80,
                "action_text": "Resume Practice",
                "action_url": "/aptitude/"
            }
        elif act_type == "resume":
            return {
                "title": "Resume ATS & Skill Gap Optimization",
                "sub_title": latest["title"],
                "progress_pct": 90,
                "action_text": "View Resume Insights",
                "action_url": "/resume/"
            }
        else:
            return {
                "title": "AI Mock Technical Interview",
                "sub_title": latest["title"],
                "progress_pct": 50,
                "action_text": "Continue Interview",
                "action_url": "/interview/"
            }

    @staticmethod
    def _compute_profile_completion(user: User) -> int:
        """Calculates candidate profile completion percentage."""
        score = 40  # Base registration score
        if user.full_name:
            score += 15
        if user.email:
            score += 15
        if user.resumes and user.resumes.count() > 0:
            score += 15
        if user.role:
            score += 15
        return min(100, score)

    @staticmethod
    def _format_time_ago(dt: datetime) -> str:
        """Formats datetime into clean human-readable relative time string."""
        if not dt:
            return "Recently"

        now = datetime.utcnow()
        diff = now - dt

        if diff.days == 0:
            if diff.seconds < 3600:
                mins = max(1, diff.seconds // 60)
                return f"{mins} min ago" if mins > 1 else "Just now"
            hours = diff.seconds // 3600
            return f"{hours} hour ago" if hours == 1 else f"{hours} hours ago"
        elif diff.days == 1:
            return "Yesterday"
        elif diff.days < 7:
            return f"{diff.days} days ago"
        else:
            return dt.strftime("%b %d, %Y")
