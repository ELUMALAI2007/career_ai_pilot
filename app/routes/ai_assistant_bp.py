"""
CareerPilot AI - AI Assistant Blueprint (`/assistant`)
Controller for conversational AI chatbot interface.
"""

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.services.ai_assistant_service import AIAssistantService

ai_assistant_bp = Blueprint('ai_assistant', __name__)
assistant_service = AIAssistantService()


@ai_assistant_bp.route('/')
@login_required
def index():
    """AI Career Assistant interface."""
    return render_template('ai_assistant/index.html')


@ai_assistant_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    """API Endpoint processing chat queries."""
    data = request.get_json() or {}
    user_query = data.get('query', '')
    session_id = data.get('session_id', 1)
    
    # Process query via service layer
    response_text = assistant_service.process_user_query(current_user.id, session_id, user_query)
    return jsonify({'response': response_text, 'status': 'success'})
