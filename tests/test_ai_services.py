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


def test_sklearn_recommendation_model():
    """Verifies Scikit-learn recommendation prediction placeholder."""
    model = SklearnRecommendationModel()
    score = model.predict_job_match([])
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0
