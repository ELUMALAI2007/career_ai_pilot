"""
AI Service Unit Tests
Tests Gemini, spaCy, and Scikit-learn service wrappers.
"""

from app.ai.gemini_service import GeminiService
from app.ai.sklearn_models import SklearnRecommendationModel


def test_gemini_service_initialization():
    """Verifies Gemini service class instantiates with default parameters."""
    service = GeminiService()
    assert service.model_name == 'gemini-1.5-flash'
    res = service.analyze_resume_text("Sample resume text", "Developer")
    assert "ats_score" in res


def test_generate_career_advice_returns_real_guidance_not_placeholder():
    """Career advice should return a useful guidance response rather than a TODO stub."""
    service = GeminiService()
    response = service.generate_career_advice({"role": "Software Engineer"}, "How should I prepare for an SDE role?")
    assert isinstance(response, str)
    assert response.strip()
    assert "TODO:" not in response
    assert "career" in response.lower() or "role" in response.lower() or "prepare" in response.lower()


def test_sklearn_recommendation_model():
    """Verifies Scikit-learn recommendation prediction placeholder."""
    model = SklearnRecommendationModel()
    score = model.predict_job_match([])
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0
