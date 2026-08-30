"""
CareerPilot AI - AI Assistant Service
Manages conversational chat history and delegates responses to AI routing service.
"""

from app.models.ai_assistant import ChatSession, ChatMessage
from app.ai.ai_router import AIRouter
from app import db


class AIAssistantService:
    """Service handling AI career assistant interaction."""

    def __init__(self):
        self.ai_router = AIRouter()

    def process_user_query(self, user_id: int, session_id: int, query: str) -> str:
        """Processes a chat query and persists conversation messages."""
        # Use AIRouter's dedicated career advice with AI Assistant key primary + fallback
        response_text = self.ai_router.generate_career_advice({"user_id": user_id}, query)
        
        user_msg = ChatMessage(session_id=session_id, sender='user', content=query)
        ai_msg = ChatMessage(session_id=session_id, sender='assistant', content=response_text)
        
        db.session.add(user_msg)
        db.session.add(ai_msg)
        db.session.commit()
        return response_text
