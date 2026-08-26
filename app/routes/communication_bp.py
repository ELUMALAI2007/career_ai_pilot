"""Routes for the Communication & Soft Skills Prep page."""

import re

from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required

communication_bp = Blueprint("communication", __name__)


@communication_bp.route("/")
@login_required
def index():
    """Show the Communication Prep page."""
    return render_template("communication/index.html")


@communication_bp.route("/evaluate", methods=["POST"])
@login_required
def evaluate():
    """Return basic communication feedback for a submitted answer."""
    data = request.get_json() or {}

    answer = data.get("answer", "").strip()
    practice_type = data.get("practice_type", "interview")
    question = data.get("question", "")

    if not answer:
        return jsonify({
            "success": False,
            "message": "Please write an answer before evaluating."
        }), 400

    words = re.findall(r"\b[\w'-]+\b", answer)
    word_count = len(words)
    sentences = [
        sentence for sentence in re.split(r"[.!?]+", answer)
        if sentence.strip()
    ]

    filler_words = ["um", "uh", "like", "basically", "actually", "very", "really"]
    filler_count = sum(
        len(re.findall(rf"\b{word}\b", answer, re.IGNORECASE))
        for word in filler_words
    )

    # Strict scoring: very short or incomplete answers receive low scores.
    grammar_score = 30

    if word_count >= 10:
        grammar_score += 15
    if answer[0].isupper():
        grammar_score += 20
    if answer[-1] in ".!?":
        grammar_score += 20
    if len(sentences) >= 3:
        grammar_score += 15

    grammar_score = min(grammar_score, 100)

    if word_count < 10:
        clarity_score = 25
    elif word_count < 30:
        clarity_score = 40
    elif word_count < 60:
        clarity_score = 60
    elif word_count <= 200:
        clarity_score = 90
    else:
        clarity_score = 70

    confidence_score = 70 - (filler_count * 7)

    if word_count < 10:
        confidence_score -= 30
    elif word_count < 30:
        confidence_score -= 15

    if answer[0].isupper():
        confidence_score += 5

    confidence_score = max(25, min(confidence_score, 95))

    tone_score = 35

    if word_count >= 15:
        tone_score += 15
    if answer[0].isupper():
        tone_score += 15
    if answer[-1] in ".!?":
        tone_score += 15

    tone_score = min(tone_score, 100)

    overall_score = round(
        (grammar_score + clarity_score + confidence_score + tone_score) / 4
    )

    strengths = []
    improvements = []
    lower_answer = answer.lower()

    skill_names = {
        "interview": "interview communication",
        "email": "professional email writing",
        "introduction": "self-introduction",
        "teamwork": "teamwork",
        "conflict": "conflict resolution",
        "listening": "active listening"
    }

    skill_keywords = {
        "teamwork": ["team", "together", "collaborate", "support", "group"],
        "conflict": ["listen", "calm", "understand", "resolve", "discuss"],
        "listening": ["listen", "understand", "clarify", "question", "feedback"],
        "email": ["dear", "thank", "regards", "please", "sincerely"],
        "interview": ["experience", "skill", "project", "learned", "achievement"],
        "introduction": ["student", "skill", "experience", "interest", "goal"]
    }

    current_skill = skill_names.get(practice_type, "communication")
    expected_keywords = skill_keywords.get(practice_type, [])
    matched_keywords = [
        keyword for keyword in expected_keywords
        if keyword in lower_answer
    ]

    if 80 <= word_count <= 200:
        strengths.append(
            "Your response has a strong length and provides useful detail."
        )
    elif word_count >= 40:
        strengths.append("Your response gives a clear starting point.")
    else:
        improvements.append(
            "Write a longer answer with more detail and a specific example."
        )

    if len(sentences) >= 3:
        strengths.append("You organised your ideas into multiple sentences.")
    else:
        improvements.append(
            "Use at least three short, complete sentences so your answer is easier to follow."
        )

    if filler_count == 0:
        strengths.append(
            "You avoided common filler words, which makes your response sound more confident."
        )
    else:
        improvements.append(
            f"Reduce filler words such as 'um', 'like', or 'really'. "
            f"We found {filler_count} possible filler word(s)."
        )

    if answer[0].isupper() and answer[-1] in ".!?":
        strengths.append("Your answer uses a professional sentence style.")
    else:
        improvements.append(
            "Start with a capital letter and end each sentence with proper punctuation."
        )

    if matched_keywords:
        strengths.append(
            f"Your response includes ideas related to {current_skill}: "
            + ", ".join(matched_keywords[:3]) + "."
        )
    else:
        improvements.append(
            f"Make your {current_skill} answer more specific by using relevant examples or keywords."
        )

    vague_words = ["good", "nice", "hardworking", "best", "passionate"]
    used_vague_words = [word for word in vague_words if word in lower_answer]

    if used_vague_words:
        improvements.append(
            "Instead of general words like "
            + ", ".join(used_vague_words)
            + ", explain a real action, project, or achievement."
        )

    if not strengths:
        strengths.append(
            "You have started the practice exercise and can improve with a more detailed answer."
        )

    if not improvements:
        improvements.append(
            "To make this even stronger, add one real example using the Situation, Action, and Result format."
        )

    return jsonify({
        "success": True,
        "practice_type": practice_type,
        "question": question,
        "word_count": word_count,
        "scores": {
            "overall": overall_score,
            "grammar": grammar_score,
            "clarity": clarity_score,
            "confidence": confidence_score,
            "tone": tone_score
        },
        "strengths": strengths,
        "improvements": improvements
    })