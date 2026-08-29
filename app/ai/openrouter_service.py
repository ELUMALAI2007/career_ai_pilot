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
        self.cooldowns = {}

    def _get_providers(self) -> list:
        """
        Returns an ordered list of (api_key, model) tuples — one per slot.
        Each slot uses a different model so every fallback is a genuinely different LLM.

        Slot 1: OPENROUTER_API_KEY  + OPENROUTER_MODEL   (default: google/gemma-4-31b-it:free)
        Slot 2: OPEN_ROUTER_KEY_2   + OPENROUTER_MODEL_2 (default: meta-llama/llama-3.3-70b-instruct:free)
        Slot 3: OPEN_ROUTER_KEY_3   + OPENROUTER_MODEL_3 (default: deepseek/deepseek-r1-0528:free)
        Slot 4: OPEN_ROUTER_KEY_4   + OPENROUTER_MODEL_4 (default: qwen/qwen-2.5-72b-instruct:free)
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
            (
                cfg('OPEN_ROUTER_KEY_4'),
                cfg('OPENROUTER_MODEL_4', 'qwen/qwen-2.5-72b-instruct:free')
            ),
        ]

        seen_keys = set()
        providers = []
        for key, model in slots:
            if key and key not in seen_keys:
                seen_keys.add(key)
                providers.append((key, model))

        # Filter out rate-limited providers currently in cooldown
        now = time.time()
        active_providers = []
        for key, model in providers:
            # Clean up expired cooldowns
            if key in self.cooldowns and now > self.cooldowns[key]:
                del self.cooldowns[key]
            
            if key not in self.cooldowns:
                active_providers.append((key, model))

        # If all providers are in cooldown, reuse them all as a last resort
        if not active_providers and providers:
            logger.warning("All OpenRouter API keys are in cooldown. Trying them anyway as a last resort.")
            return providers

        return active_providers

    def _get_assistant_providers(self) -> list:
        """
        Returns an ordered list of (api_key, model) for the AI assistant.
        Primary: OPEN_ROUTER_KEY_AI_ASSISTANT (dedicated assistant key)
        Fallback: Standard rotation keys
        """
        def cfg(name, default=''):
            try:
                return (current_app.config.get(name) or os.getenv(name, default) or default).strip()
            except Exception:
                return (os.getenv(name, default) or default).strip()

        providers = []
        
        # Primary: AI Assistant key
        assistant_key = cfg('OPEN_ROUTER_KEY_AI_ASSISTANT')
        assistant_model = cfg('OPENROUTER_MODEL_AI_ASSISTANT', 'minimax/minimax-m3:free')
        if assistant_key:
            providers.append((assistant_key, assistant_model))
        
        # Fallback: Standard rotation keys
        standard_slots = [
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
            (
                cfg('OPEN_ROUTER_KEY_4'),
                cfg('OPENROUTER_MODEL_4', 'qwen/qwen-2.5-72b-instruct:free')
            ),
        ]
        
        seen_keys = {assistant_key} if assistant_key else set()
        for key, model in standard_slots:
            if key and key not in seen_keys:
                seen_keys.add(key)
                providers.append((key, model))
        
        # Filter out rate-limited providers currently in cooldown
        now = time.time()
        active_providers = []
        for key, model in providers:
            # Clean up expired cooldowns
            if key in self.cooldowns and now > self.cooldowns[key]:
                del self.cooldowns[key]
            
            if key not in self.cooldowns:
                active_providers.append((key, model))
        
        # If all providers are in cooldown, reuse them all as a last resort
        if not active_providers and providers:
            logger.warning("All AI Assistant providers are in cooldown. Trying them anyway as a last resort.")
            return providers
        
        return active_providers if active_providers else providers

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
                    # Rate-limited — signal caller to rotate to next key immediately and apply cooldown
                    self.cooldowns[api_key] = time.time() + 900
                    logger.warning(f"OpenRouter key ...{api_key[-6:]} hit rate limit (429). Rotating key and applying 15-minute cooldown.")
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

    def generate_resume_questions(self, role: str, company: str, interview_type: str, difficulty: str, resume_text: str) -> list[dict]:
        """Generate resume-specific questions once at session start."""
        system_prompt = (
            "Create mock interview questions from a candidate resume. Respond only as JSON with a "
            "'questions' array; each item has 'question', 'question_type', and 'topic'. "
            "Use only facts in the resume and return 3 to 5 questions."
        )
        user_content = f"Role: {role}\nCompany: {company or 'General'}\nInterview type: {interview_type}\nDifficulty: {difficulty}\nResume:\n{resume_text or 'No resume text available.'}"
        raw_resp = self._call_openrouter(
            [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_content}],
            response_format={"type": "json_object"}
        )
        parsed = self._clean_and_parse_json(raw_resp, ["questions"], {"questions": []})
        return parsed["questions"] if isinstance(parsed.get("questions"), list) else []

    def generate_follow_up(self, session_context: dict, current_question: str, candidate_answer: str, previous_turns: list) -> dict:
        """Generate one focused follow-up for an incomplete answer."""
        system_prompt = (
            "You are a professional interviewer. Generate one concise follow-up question asking for "
            "clarification or evidence. Respond only as JSON with 'question', 'question_type', and 'topic'."
        )
        user_content = f"Session: {json.dumps(session_context)}\nCurrent question: {current_question}\nCandidate answer: {candidate_answer}\nPrevious turns: {json.dumps(previous_turns)}"
        raw_resp = self._call_openrouter(
            [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_content}],
            response_format={"type": "json_object"}
        )
        default = {"question": "Could you explain that with a specific example?", "question_type": "Follow-up", "topic": "Clarification"}
        return self._clean_and_parse_json(raw_resp, ["question", "question_type", "topic"], default)

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
            "  ],\n"
            "  \"per_question_feedback\": [\n"
            "     {\"question\": \"string\", \"feedback\": \"string\", \"score\": integer}\n"
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
            "recommended_improvements": ["Review the core structures and algorithms commonly asked for your target role."],
            "per_question_feedback": []
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

    def generate_career_advice(self, user_profile: dict, query: str) -> str:
        """Generates personalized career guidance with structured formatting using the dedicated AI assistant key."""
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert career coach and mentor at CareerPilot. Provide personalized, actionable career guidance. "
                    "Be encouraging, specific, and practical. Focus on the user's role and growth areas. "
                    "\n\nFormatted Response Guidelines:"
                    "\n- Use clear section headers (e.g., '📌 Key Insight:', '💡 Action Steps:', '🎯 Quick Tips:')"
                    "\n- Use bullet points for multiple items (use • or -, each on new line)"
                    "\n- Keep sections concise but comprehensive"
                    "\n- Use emoji indicators for visual clarity"
                    "\n- Separate sections with blank lines"
                    "\n- Avoid long paragraphs; prefer short, scannable content"
                    "\n- Use Markdown headings with ## (for example, ## Action plan) so the response renders clearly in the chat."
                    "\n- Use numbered lists for sequential steps and - for supporting points."
                    "\n- Use **bold** only to emphasize key terms."
                    "\n\nExample structure:"
                    "\n📌 Key Insight"
                    "\nBrief statement about their situation."
                    "\n\n💡 Action Steps"
                    "\n• First actionable step"
                    "\n• Second actionable step"
                    "\n• Third actionable step"
                    "\n\n🎯 Quick Tips"
                    "\n• Tip 1"
                    "\n• Tip 2"
                )
            },
            {
                "role": "user",
                "content": query
            }
        ]

        # Use the dedicated AI Assistant providers with primary key + fallback to standard keys
        providers = self._get_assistant_providers()
        
        for api_key, model in providers:
            try:
                response = self._call_with_key(api_key, model, messages)
                if response:
                    return self._format_career_advice(response)
            except ValueError as e:
                logger.warning(f"AI Assistant provider failed for generate_career_advice: {e}")
                continue
        
        # Fallback structured response if all providers fail
        return (
            "❌ Service Temporarily Unavailable\n\n"
            "I'm experiencing temporary service issues. Please try again in a moment.\n\n"
            "💡 In the meantime, consider:\n"
            "• What specific role are you targeting?\n"
            "• What skills would help you stand out?\n"
            "• Who can you connect with for mentorship?\n\n"
            "Your guidance will be back shortly!"
        )

    def _format_career_advice(self, response: str) -> str:
        """Ensures career advice response is properly formatted for readability."""
        # If response already has structured markers, return as-is
        if any(marker in response for marker in ['## ', '- ', '* ', '1. ', '**', '📌', '💡', '🎯', '✓', '•']):
            return response
        
        # Otherwise, add basic structure
        lines = response.strip().split('\n')
        structured = []
        
        for line in lines:
            line = line.strip()
            if not line:
                structured.append('')
            elif line[0].isupper() and len(line.split()) >= 2:
                # Likely a header/section
                structured.append(f"\n📌 {line}\n")
            elif any(phrase in line.lower() for phrase in ['step', 'tip', 'recommend', 'consider', 'focus']):
                # Likely action item
                if not line.startswith('•'):
                    structured.append(f"• {line}")
                else:
                    structured.append(line)
            else:
                structured.append(line)
        
        return '\n'.join(structured).strip()
