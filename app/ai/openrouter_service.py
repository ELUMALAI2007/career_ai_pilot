"""
CareerPilot AI - OpenRouter Service Module
Supports multi-key + multi-model rotation: each key is paired with a different
model so every fallback uses a genuinely different LLM.
"""

import os
import json
import logging
import time
import requests
from flask import current_app

logger = logging.getLogger(__name__)


class OpenRouterService:
    """Service wrapper for OpenRouter API integration with multi-key rotation fallback."""

    def __init__(self):
        pass

    def _get_providers(self) -> list:
        """
        Returns an ordered list of (api_key, model) tuples — one per slot.
        Each slot uses a different model so every fallback is a genuinely different LLM.

        Slot 1: OPENROUTER_API_KEY  + OPENROUTER_MODEL   (default: google/gemma-4-31b-it:free)
        Slot 2: OPEN_ROUTER_KEY_2   + OPENROUTER_MODEL_2 (default: meta-llama/llama-3.3-70b-instruct:free)
        Slot 3: OPEN_ROUTER_KEY_3   + OPENROUTER_MODEL_3 (default: deepseek/deepseek-r1-0528:free)
        """
        def cfg(name, default=''):
            try:
                return (current_app.config.get(name) or os.getenv(name, default) or default).strip()
            except Exception:
                return (os.getenv(name, default) or default).strip()

        slots = [
            (
                cfg('OPENROUTER_API_KEY') or cfg('OPEN_ROUTER_KEY'),
                cfg('OPENROUTER_MODEL', 'google/gemma-4-31b-it:free')
            ),
            (
                cfg('OPEN_ROUTER_KEY_2'),
                cfg('OPENROUTER_MODEL_2', 'meta-llama/llama-3.3-70b-instruct:free')
            ),
            (
                cfg('OPEN_ROUTER_KEY_3'),
                cfg('OPENROUTER_MODEL_3', 'deepseek/deepseek-r1-0528:free')
            ),
        ]

        seen_keys = set()
        providers = []
        for key, model in slots:
            if key and key not in seen_keys:
                seen_keys.add(key)
                providers.append((key, model))
        return providers

    def _call_with_key(self, api_key: str, model: str, messages: list, response_format: dict = None, max_retries: int = 2) -> str:
        """Attempts to call OpenRouter API with a specific key; retries on transient errors, raises immediately on 429."""
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://127.0.0.1:5000",
            "X-Title": "CareerPilot AI"
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.4,
        }
        if response_format:
            payload["response_format"] = response_format

        url = "https://openrouter.ai/api/v1/chat/completions"

        for attempt in range(max_retries + 1):
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=45)
                if response.status_code == 200:
                    data = response.json()
                    return data['choices'][0]['message']['content']
                elif response.status_code == 429:
                    # Rate-limited — signal caller to rotate to next key immediately
                    logger.warning(f"OpenRouter key ...{api_key[-6:]} hit rate limit (429). Rotating key.")
                    raise ValueError(f"RATE_LIMIT: key ...{api_key[-6:]} exhausted.")
                else:
                    logger.error(f"OpenRouter key ...{api_key[-6:]} returned {response.status_code}: {response.text}")
                    if attempt == max_retries:
                        raise ValueError(f"OpenRouter API error (status {response.status_code}) on key ...{api_key[-6:]}")
                    time.sleep(2 * (attempt + 1))
            except ValueError:
                raise  # propagate rate-limit / API errors for outer key-rotation logic
            except requests.exceptions.RequestException as e:
                logger.error(f"Connection error on attempt {attempt+1} key ...{api_key[-6:]}: {e}")
                if attempt == max_retries:
                    raise ValueError(f"Connection error with key ...{api_key[-6:]}: {e}")
                time.sleep(2 * (attempt + 1))
        return ""

    def _call_openrouter(self, messages: list, response_format: dict = None, max_retries: int = 2) -> str:
        """
        Calls OpenRouter API rotating through all (key, model) pairs on rate-limit or error.
        Each slot uses a different model so every fallback is a genuinely different LLM.
        Raises ValueError only if ALL providers are exhausted.
        """
        providers = self._get_providers()
        if not providers:
            raise ValueError("No OpenRouter API keys configured.")

        last_error = None
        for idx, (key, model) in enumerate(providers):
            try:
                logger.info(f"OpenRouter: trying slot #{idx+1}/{len(providers)} key=...{key[-6:]} model={model}")
                return self._call_with_key(key, model, messages, response_format, max_retries)
            except ValueError as e:
                last_error = e
                remaining = len(providers) - idx - 1
                logger.warning(
                    f"OpenRouter slot #{idx+1} (model={model}) failed: {e}. "
                    f"{remaining} slot(s) remaining."
                )

        raise ValueError(f"All OpenRouter providers exhausted. Last error: {last_error}")


    def _clean_and_parse_json(self, text: str, default_keys: list, default_val: dict) -> dict:
        """Strips markdown fences and parses string response safely to JSON dictionary."""
        text = text.strip()
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
            logger.error(f"Failed to parse JSON from OpenRouter response: {e}. Content: {text}")
            return default_val

    def generate_first_question(self, role: str, company: str, difficulty: str, interview_type: str, resume_summary: str = None, ask_resume: bool = False) -> dict:
        """Generates the initial question of the interview based on target setup and resume."""
        system_prompt = (
            "You are a professional AI interviewer conducting a realistic mock interview.\n"
            "You MUST respond ONLY with a valid JSON object. Do not include markdown code block wrappers (like ```json ... ```), explanation, or preamble.\n"
            "The JSON object must match this schema:\n"
            "{\n"
            "  \"question\": \"string\",\n"
            "  \"question_type\": \"string\"\n"
            "}\n"
            "The 'question_type' must be one of: 'Technical', 'Behavioral', 'Resume', 'HR'.\n"
            "Maintain the role, company, type, and difficulty requested. Keep the tone professional and conversational."
        )

        user_content = (
            f"Start the interview.\n"
            f"Role: {role}\n"
            f"Company: {company or 'General'}\n"
            f"Difficulty: {difficulty}\n"
            f"Interview Type: {interview_type}\n"
        )
        if ask_resume and resume_summary:
            user_content += (
                f"\nCandidate Resume Context (Do NOT invent facts, projects, or experience not present here):\n"
                f"{resume_summary}\n"
                f"Begin by asking a specific question based on their resume (e.g. asking about a project or technology mentioned), or a relevant role introduction."
            )
        else:
            user_content += "Begin by asking a general technical, behavioral, or introductory question relevant to the role."

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        raw_resp = self._call_openrouter(messages, response_format={"type": "json_object"})
        default_val = {
            "question": f"Welcome to the interview for the {role} role. Can you introduce yourself and talk about your relevant experience?",
            "question_type": "HR"
        }
        return self._clean_and_parse_json(raw_resp, default_keys=["question", "question_type"], default_val=default_val)

    def evaluate_turn_and_generate_next(
        self,
        session_info: dict,
        turns_history: list,
        current_question: str,
        current_question_type: str,
        candidate_answer: str,
        resume_summary: str = None
    ) -> dict:
        """Evaluates candidate response and decides the next follow-up question."""
        role = session_info.get("role")
        company = session_info.get("company", "General")
        difficulty = session_info.get("difficulty")
        interview_type = session_info.get("interview_type")
        total_questions = session_info.get("total_questions", 10)
        current_question_no = session_info.get("current_question_no", 1)
        ask_resume = session_info.get("resume_based_questions", False)

        # Decide scores dimensions based on current question type or session type
        if current_question_type == "Resume":
            dimensions = ["Knowledge of Claimed Skill", "Technical Understanding", "Accuracy", "Specificity", "Communication"]
        elif interview_type == "Technical":
            dimensions = ["Technical Accuracy", "Technical Depth", "Problem Solving", "Relevance", "Communication", "Answer Structure"]
        elif interview_type == "HR / Behavioral":
            dimensions = ["Relevance", "Communication", "Specificity", "STAR Structure", "Completeness", "Answer Structure"]
        else:
            dimensions = ["Technical Accuracy", "STAR Structure", "Communication", "Relevance", "Answer Structure"]

        dimensions_str = ", ".join([f"'{d}'" for d in dimensions])
        is_last = current_question_no >= total_questions

        system_prompt = (
            "You are a professional AI interviewer.\n"
            "Evaluate the candidate's last answer and decide the next question.\n"
            "You MUST respond ONLY with a valid JSON object. Do not include markdown code block wrappers (like ```json ... ```), explanation, or preamble.\n"
            "JSON schema must be:\n"
            "{\n"
            "  \"evaluation\": {\n"
            "    \"what_went_well\": \"string summarizing strengths in this response\",\n"
            "    \"areas_for_improvement\": \"string summarizing weaknesses/gaps in this response\"\n"
            "  },\n"
            "  \"scores\": {\n"
            "     // Provide integer scores from 0 to 10 for each specified dimension\n"
            "  },\n"
            "  \"follow_up_required\": boolean,\n"
            "  \"next_question\": \"string\",\n"
            "  \"next_question_type\": \"string\" (one of 'Technical', 'Behavioral', 'Resume', 'Follow-up', 'HR')\n"
            "}\n"
            f"Under 'scores', you must score exactly these dimensions: {dimensions_str}. All scores must be integers between 0 and 10.\n"
        )

        if is_last:
            system_prompt += "Since this was the final question (the configured number of questions is reached), set 'next_question' to 'Interview complete', 'next_question_type' to 'HR', and 'follow_up_required' to false.\n"
        else:
            system_prompt += (
                "For the next question: keep it appropriate to the selected role, difficulty, and company context.\n"
                "If the candidate's answer contains interesting points, ask a relevant follow-up question based on their response. Otherwise, continue to a new topic.\n"
                "Avoid repeatedly asking the same question. Ensure you do not invent facts outside the resume context if resume questions are enabled.\n"
            )

        # Context build
        user_content = (
            f"Interview Setup:\n"
            f"- Role: {role}\n"
            f"- Company: {company}\n"
            f"- Difficulty: {difficulty}\n"
            f"- Total Questions: {total_questions}\n"
            f"- Current Question No: {current_question_no}\n"
        )
        if resume_summary and ask_resume:
            user_content += f"- Candidate Resume Context (Do NOT invent facts outside this context):\n{resume_summary}\n"

        if turns_history:
            user_content += "\nPrevious Turns:\n"
            for t in turns_history:
                user_content += f"Q: {t.get('question')}\nA: {t.get('candidate_answer') or ''}\n"

        user_content += (
            f"\nCurrent Turn:\n"
            f"Q: {current_question}\n"
            f"Candidate Answer: {candidate_answer}\n"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        default_scores = {d: 5 for d in dimensions}
        default_val = {
            "evaluation": {
                "what_went_well": "Response parsed successfully.",
                "areas_for_improvement": "No major areas noted."
            },
            "scores": default_scores,
            "follow_up_required": False,
            "next_question": "Interview complete" if is_last else "Could you elaborate on another project you've worked on?",
            "next_question_type": "Follow-up"
        }

        raw_resp = self._call_openrouter(messages, response_format={"type": "json_object"})
        parsed = self._clean_and_parse_json(raw_resp, default_keys=["evaluation", "scores", "next_question"], default_val=default_val)

        if "scores" not in parsed or not isinstance(parsed["scores"], dict):
            parsed["scores"] = default_scores
        else:
            for d in dimensions:
                if d not in parsed["scores"]:
                    parsed["scores"][d] = 5
        return parsed

    def generate_final_report(self, session_info: dict, all_turns_history: list) -> dict:
        """Aggregates all interview turns and generates overall scorecard feedback and dimension scores."""
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

        dimensions_str = ", ".join([f"'{d}'" for d in dimensions])

        system_prompt = (
            "You are a professional AI interviewer compiling a final performance report for a mock interview.\n"
            "You MUST respond ONLY with a valid JSON object. Do not include markdown code block wrappers (like ```json ... ```), explanation, or preamble.\n"
            "JSON schema must be:\n"
            "{\n"
            "  \"overall_score\": integer (0 to 100 representing the overall average score),\n"
            "  \"dimension_scores\": {\n"
            "     // Provide integer scores from 0 to 100 for each evaluated dimension\n"
            "  },\n"
            "  \"strengths\": [\n"
            "     \"string highlighting a key strength with a concrete reason\"\n"
            "  ],\n"
            "  \"areas_for_improvement\": [\n"
            "     \"string highlighting a key area for improvement with a concrete reason\"\n"
            "  ],\n"
            "  \"recommended_improvements\": [\n"
            "     \"string providing practical, actionable suggestion for future interviews\"\n"
            "  ]\n"
            "}\n"
            f"Under 'dimension_scores', provide overall scores (0 to 100) for exactly these dimensions: {dimensions_str}.\n"
        )

        user_content = (
            f"Interview Configuration:\n"
            f"- Role: {role}\n"
            f"- Company Context: {company}\n"
            f"- Difficulty: {difficulty}\n"
            f"- Interview Type: {interview_type}\n\n"
            f"Detailed Question and Answer Turns with Turn-level evaluations:\n"
        )
        for idx, t in enumerate(all_turns_history):
            user_content += (
                f"Turn {idx+1}:\n"
                f"Question: {t.get('question')}\n"
                f"Candidate Answer: {t.get('candidate_answer') or ''}\n"
                f"Turn Scores: {t.get('scores')}\n"
                f"Turn Feedback: {t.get('evaluation')}\n\n"
            )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        default_dim_scores = {d: 50 for d in dimensions}
        default_val = {
            "overall_score": 60,
            "dimension_scores": default_dim_scores,
            "strengths": ["Completed the full mock interview session successfully."],
            "areas_for_improvement": ["Elaborate more on design decisions and practical trade-offs."],
            "recommended_improvements": ["Review the core structures and algorithms commonly asked for your target role."]
        }

        raw_resp = self._call_openrouter(messages, response_format={"type": "json_object"})
        parsed = self._clean_and_parse_json(raw_resp, default_keys=["overall_score", "dimension_scores", "strengths", "areas_for_improvement", "recommended_improvements"], default_val=default_val)

        if "dimension_scores" not in parsed or not isinstance(parsed["dimension_scores"], dict):
            parsed["dimension_scores"] = default_dim_scores
        else:
            for d in dimensions:
                if d not in parsed["dimension_scores"]:
                    parsed["dimension_scores"][d] = 50
        return parsed
