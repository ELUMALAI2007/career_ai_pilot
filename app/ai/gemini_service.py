"""
CareerPilot AI - Gemini LLM Service Module
Interfaces with Google Gemini API as a fallback provider for mock interviews.
Mirrors the OpenRouterService interface so AIRouter can use it transparently.
"""

import os
import json
import logging
from flask import current_app

logger = logging.getLogger(__name__)


class GeminiService:
    """Service wrapper for Google Gemini API integration (interview fallback provider)."""

    def __init__(self):
        pass

    def _get_api_key(self) -> str:
        try:
            return current_app.config.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY", "")
        except Exception:
            return os.getenv("GEMINI_API_KEY", "")

    def _get_model_name(self) -> str:
        try:
            return current_app.config.get("GEMINI_MODEL_NAME") or os.getenv("GEMINI_MODEL_NAME", "gemini-3.6-flash")
        except Exception:
            return os.getenv("GEMINI_MODEL_NAME", "gemini-3.6-flash")

    def _call_gemini(self, system_prompt: str, user_content: str) -> str:
        """Calls Gemini API with system + user content and returns the text response."""
        import google.generativeai as genai

        api_key = self._get_api_key()
        if not api_key:
            raise ValueError("Gemini API key is missing.")

        genai.configure(api_key=api_key)
        model_name = self._get_model_name()

        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.4,
                response_mime_type="application/json"
            )
        )

        try:
            response = model.generate_content(user_content)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            raise ValueError(f"Gemini API error: {e}")

    def _clean_and_parse_json(self, text: str, default_keys: list, default_val: dict) -> dict:
        """Strips markdown fences and parses string response safely to JSON dictionary."""
        text = (text or "").strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        try:
            parsed = json.loads(text)
            for k in default_keys:
                if k not in parsed:
                    parsed[k] = default_val[k]
            return parsed
        except Exception as e:
            logger.error(f"Failed to parse JSON from Gemini response: {e}. Content: {text}")
            return default_val

    # -------------------------------------------------------------------------
    # Interview interface -- mirrors OpenRouterService public methods exactly
    # -------------------------------------------------------------------------

    def generate_first_question(self, role: str, company: str, difficulty: str, interview_type: str, resume_summary: str = None, ask_resume: bool = False) -> dict:
        """Generates the initial interview question using Gemini."""
        system_prompt = (
            "You are a professional AI interviewer conducting a realistic mock interview.\n"
            "You MUST respond ONLY with a valid JSON object. No markdown fences or preamble.\n"
            'Schema: { "question": "string", "question_type": "string" }\n'
            "question_type must be one of: Technical, Behavioral, Resume, HR.\n"
            "Keep the tone professional and conversational."
        )
        user_content = (
            f"Start the interview.\nRole: {role}\nCompany: {company or 'General'}\n"
            f"Difficulty: {difficulty}\nInterview Type: {interview_type}\n"
        )
        if ask_resume and resume_summary:
            user_content += (
                f"\nCandidate Resume Context (Do NOT invent facts not present here):\n{resume_summary}\n"
                "Begin by asking a specific question based on their resume."
            )
        else:
            user_content += "Begin by asking a general technical, behavioral, or introductory question relevant to the role."

        raw_resp = self._call_gemini(system_prompt, user_content)
        default_val = {
            "question": f"Welcome to the interview for the {role} role. Can you introduce yourself?",
            "question_type": "HR"
        }
        return self._clean_and_parse_json(raw_resp, ["question", "question_type"], default_val)

    def evaluate_turn_and_generate_next(
        self,
        session_info: dict,
        turns_history: list,
        current_question: str,
        current_question_type: str,
        candidate_answer: str,
        resume_summary: str = None
    ) -> dict:
        """Evaluates candidate response and decides the next question using Gemini."""
        role = session_info.get("role")
        company = session_info.get("company", "General")
        difficulty = session_info.get("difficulty")
        interview_type = session_info.get("interview_type")
        total_questions = session_info.get("total_questions", 10)
        current_question_no = session_info.get("current_question_no", 1)
        ask_resume = session_info.get("resume_based_questions", False)

        if current_question_type == "Resume":
            dimensions = ["Knowledge of Claimed Skill", "Technical Understanding", "Accuracy", "Specificity", "Communication"]
        elif interview_type == "Technical":
            dimensions = ["Technical Accuracy", "Technical Depth", "Problem Solving", "Relevance", "Communication", "Answer Structure"]
        elif interview_type == "HR / Behavioral":
            dimensions = ["Relevance", "Communication", "Specificity", "STAR Structure", "Completeness", "Answer Structure"]
        else:
            dimensions = ["Technical Accuracy", "STAR Structure", "Communication", "Relevance", "Answer Structure"]

        dimensions_str = ", ".join(dimensions)
        is_last = current_question_no >= total_questions

        system_prompt = (
            "You are a professional AI interviewer.\n"
            "Evaluate the candidate last answer and decide the next question.\n"
            "Respond ONLY with valid JSON, no markdown fences, no preamble.\n"
            'Schema: { "evaluation": { "what_went_well": "str", "areas_for_improvement": "str" }, '
            '"scores": {}, "follow_up_required": bool, "next_question": "str", "next_question_type": "str" }\n'
            f"Score these dimensions with integers 0-10: {dimensions_str}.\n"
        )
        if is_last:
            system_prompt += 'This is the final question. Set next_question="Interview complete", next_question_type="HR", follow_up_required=false.\n'
        else:
            system_prompt += "Keep next question relevant. Follow-up if interesting, otherwise move to new topic.\n"

        user_content = (
            f"Setup: Role={role}, Company={company}, Difficulty={difficulty}, "
            f"Total={total_questions}, Current={current_question_no}\n"
        )
        if resume_summary and ask_resume:
            user_content += f"Resume Context:\n{resume_summary}\n"
        if turns_history:
            user_content += "\nPrevious Turns:\n"
            for t in turns_history:
                user_content += f"Q: {t.get('question')}\nA: {t.get('candidate_answer') or ''}\n"
        user_content += f"\nCurrent:\nQ: {current_question}\nAnswer: {candidate_answer}\n"

        default_scores = {d: 5 for d in dimensions}
        default_val = {
            "evaluation": {"what_went_well": "Response received.", "areas_for_improvement": "No data."},
            "scores": default_scores,
            "follow_up_required": False,
            "next_question": "Interview complete" if is_last else "Could you elaborate on another project?",
            "next_question_type": "Follow-up"
        }

        raw_resp = self._call_gemini(system_prompt, user_content)
        parsed = self._clean_and_parse_json(raw_resp, ["evaluation", "scores", "next_question"], default_val)

        if "scores" not in parsed or not isinstance(parsed["scores"], dict):
            parsed["scores"] = default_scores
        else:
            for d in dimensions:
                if d not in parsed["scores"]:
                    parsed["scores"][d] = 5
        return parsed

    def generate_final_report(self, session_info: dict, all_turns_history: list) -> dict:
        """Generates final interview scorecard using Gemini."""
        role = session_info.get("role")
        company = session_info.get("company", "General")
        difficulty = session_info.get("difficulty")
        interview_type = session_info.get("interview_type")

        if interview_type == "Technical":
            dimensions = ["Technical Accuracy", "Technical Depth", "Problem Solving", "Relevance", "Communication", "Answer Structure"]
        elif interview_type == "HR / Behavioral":
            dimensions = ["Relevance", "Communication", "Specificity", "STAR Structure", "Completeness", "Answer Structure"]
        else:
            dimensions = ["Technical Accuracy", "STAR Structure", "Communication", "Relevance", "Answer Structure"]

        dimensions_str = ", ".join(dimensions)

        system_prompt = (
            "You are a professional AI interviewer compiling a final performance report.\n"
            "Respond ONLY with valid JSON, no markdown fences, no preamble.\n"
            'Schema: { "overall_score": int(0-100), "dimension_scores": {}, '
            '"strengths": [], "areas_for_improvement": [], "recommended_improvements": [] }\n'
            f"Provide dimension_scores (0-100) for exactly: {dimensions_str}.\n"
        )
        user_content = (
            f"Config: Role={role}, Company={company}, Difficulty={difficulty}, Type={interview_type}\n\nTurns:\n"
        )
        for idx, t in enumerate(all_turns_history):
            user_content += (
                f"Turn {idx+1}: Q={t.get('question')} | A={t.get('candidate_answer') or ''} | "
                f"Scores={t.get('scores')} | Feedback={t.get('evaluation')}\n"
            )

        default_dim_scores = {d: 50 for d in dimensions}
        default_val = {
            "overall_score": 60,
            "dimension_scores": default_dim_scores,
            "strengths": ["Completed the full mock interview session."],
            "areas_for_improvement": ["Elaborate more on design decisions."],
            "recommended_improvements": ["Review core structures for your target role."]
        }

        raw_resp = self._call_gemini(system_prompt, user_content)
        parsed = self._clean_and_parse_json(
            raw_resp,
            ["overall_score", "dimension_scores", "strengths", "areas_for_improvement", "recommended_improvements"],
            default_val
        )
        if "dimension_scores" not in parsed or not isinstance(parsed["dimension_scores"], dict):
            parsed["dimension_scores"] = default_dim_scores
        else:
            for d in dimensions:
                if d not in parsed["dimension_scores"]:
                    parsed["dimension_scores"][d] = 50
        return parsed

    # -------------------------------------------------------------------------
    # Stub methods kept for other parts of the app that reference this service
    # -------------------------------------------------------------------------

    def generate_career_advice(self, user_profile: dict, query: str) -> str:
        """Generates personalized career recommendations using Gemini LLM."""
        return "TODO: Gemini Service - Career advice response placeholder."

    def analyze_resume_text(self, resume_text: str, target_role: str) -> dict:
        """Analyzes raw resume text against a target job role for ATS scoring."""
        return {
            "ats_score": 75,
            "strengths": ["TODO: Gemini parsed strength"],
            "gaps": ["TODO: Gemini parsed gap"],
            "recommendations": ["TODO: Gemini parsed recommendation"]
        }

    def generate_interview_questions(self, role: str, company: str, difficulty: str) -> list:
        """Generates customized mock interview questions."""
        return [{"id": 1, "question": f"Tell me about your experience relevant to {role} at {company}."}]

    def evaluate_interview_response(self, question: str, user_response: str) -> dict:
        """Evaluates a user answer during a mock interview session."""
        return {
            "score": 8,
            "feedback": "TODO: Gemini response evaluation feedback placeholder.",
            "sample_answer": "TODO: Gemini suggested optimal response."
        }
