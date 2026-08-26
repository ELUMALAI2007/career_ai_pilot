"""
CareerPilot AI - AIRouter
Unified AI provider chain with automatic fallback.

Priority order:
  1. OpenRouter key #1  (OPENROUTER_API_KEY / OPEN_ROUTER_KEY)
  2. OpenRouter key #2  (OPEN_ROUTER_KEY_2)
  3. OpenRouter key #3  (OPEN_ROUTER_KEY_3)
  4. Google Gemini      (GEMINI_API_KEY)

When any provider raises a ValueError (rate limit, auth error, API error),
AIRouter logs a warning and immediately tries the next provider. The full
interview context is never affected because it is always persisted in the DB
before each call and re-read by the caller.
"""

import logging
from app.ai.openrouter_service import OpenRouterService
from app.ai.gemini_service import GeminiService

logger = logging.getLogger(__name__)


class AIRouter:
    """
    Wraps multiple AI providers in a priority fallback chain.
    Exposes the same interface as OpenRouterService so callers need no changes.
    """

    def __init__(self):
        # OpenRouter handles its own multi-key rotation internally.
        # Gemini is the last-resort fallback.
        self._openrouter = OpenRouterService()
        self._gemini = GeminiService()

        # Provider registry: (name, instance)
        self._providers = [
            ("OpenRouter", self._openrouter),
            ("Gemini", self._gemini),
        ]

    def _call_with_fallback(self, method_name: str, *args, **kwargs):
        """
        Calls `method_name` on each provider in order.
        Moves to the next provider on ValueError; re-raises only if all fail.
        """
        last_error = None
        for provider_name, provider in self._providers:
            try:
                method = getattr(provider, method_name)
                result = method(*args, **kwargs)
                if provider_name != "OpenRouter":
                    logger.info(f"AIRouter: successfully used fallback provider '{provider_name}' for {method_name}.")
                return result
            except ValueError as e:
                last_error = e
                remaining = len(self._providers) - self._providers.index((provider_name, provider)) - 1
                logger.warning(
                    f"AIRouter: provider '{provider_name}' failed for {method_name}: {e}. "
                    f"{remaining} fallback(s) remaining."
                )
            except Exception as e:
                last_error = e
                logger.error(f"AIRouter: unexpected error from '{provider_name}' for {method_name}: {e}.")

        raise ValueError(f"AIRouter: all providers failed for {method_name}. Last error: {last_error}")

    # -------------------------------------------------------------------------
    # Public interface — identical signatures to OpenRouterService
    # -------------------------------------------------------------------------

    def generate_first_question(self, role: str, company: str, difficulty: str, interview_type: str, resume_summary: str = None, ask_resume: bool = False) -> dict:
        """Generates the first interview question using the first available provider."""
        return self._call_with_fallback(
            "generate_first_question",
            role=role,
            company=company,
            difficulty=difficulty,
            interview_type=interview_type,
            resume_summary=resume_summary,
            ask_resume=ask_resume
        )

    def evaluate_turn_and_generate_next(
        self,
        session_info: dict,
        turns_history: list,
        current_question: str,
        current_question_type: str,
        candidate_answer: str,
        resume_summary: str = None
    ) -> dict:
        """Evaluates a candidate answer and generates the next question using the first available provider."""
        return self._call_with_fallback(
            "evaluate_turn_and_generate_next",
            session_info=session_info,
            turns_history=turns_history,
            current_question=current_question,
            current_question_type=current_question_type,
            candidate_answer=candidate_answer,
            resume_summary=resume_summary
        )

    def generate_final_report(self, session_info: dict, all_turns_history: list) -> dict:
        """Compiles the final interview report using the first available provider."""
        return self._call_with_fallback(
            "generate_final_report",
            session_info=session_info,
            all_turns_history=all_turns_history
        )
