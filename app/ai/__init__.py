"""
CareerPilot AI Engine Package
Exposes services for Gemini LLM, spaCy NLP, Transformers embeddings, and Scikit-learn ML models.
"""

from app.ai.gemini_service import GeminiService
from app.ai.nlp_spacy import NLPSpacyService
from app.ai.transformers_service import TransformersService
from app.ai.sklearn_models import SklearnRecommendationModel
from app.ai.openrouter_service import OpenRouterService

__all__ = [
    'GeminiService',
    'NLPSpacyService',
    'TransformersService',
    'SklearnRecommendationModel',
    'OpenRouterService'
]
