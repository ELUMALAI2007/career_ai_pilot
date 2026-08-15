"""
CareerPilot AI - AI Assistant Service
Manages conversational chat history and delegates responses to Gemini LLM.
"""

from app.models.ai_assistant import ChatSession, ChatMessage
from app.ai.gemini_service import GeminiService
from app import db


class AIAssistantService:
    """Service handling AI career assistant interaction."""

    def __init__(self):
        self.gemini = GeminiService()

    def process_user_query(self, user_id: int, session_id: int, query: str) -> str:
        """Processes a chat query and persists conversation messages."""
        # TODO: Retrieve user context and generate AI response via Gemini API
        response_text = self.gemini.generate_career_advice({}, query)
        
        user_msg = ChatMessage(session_id=session_id, sender='user', content=query)
        ai_msg = ChatMessage(session_id=session_id, sender='assistant', content=response_text)
        
        db.session.add(user_msg)
        db.session.add(ai_msg)
        db.session.commit()
        return response_text
