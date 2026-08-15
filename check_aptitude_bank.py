"""
CareerPilot AI - Diagnostic Aptitude Question Bank Inspector
Reports question counts by category, topic, difficulty, and checks missing topic/difficulty coverage.
"""

import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.aptitude import AptitudeCategory, AptitudeQuestion
from question_generators import (
    QUANT_TOPICS, LOGICAL_TOPICS, VERBAL_TOPICS, DIFFICULTY_LEVELS
)


def inspect_bank():
    app = create_app()
    with app.app_context():
        print(f"DATABASE URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        total = AptitudeQuestion.query.count()
        print("=" * 60)
        print("          CAREERPILOT AI — APTITUDE QUESTION BANK DIAGNOSTIC")
        print("=" * 60)
        print(f"TOTAL QUESTIONS IN DATABASE: {total}\n")

        categories = AptitudeCategory.query.all()
        for cat in categories:
            cat_count = AptitudeQuestion.query.filter_by(category_id=cat.id).count()
            print(f"Category: {cat.name} — {cat_count} Questions")
            
            # Difficulty breakdown for category
            diff_counts = {}
            for diff in DIFFICULTY_LEVELS:
                cnt = AptitudeQuestion.query.filter_by(category_id=cat.id, difficulty=diff).count()
                diff_counts[diff] = cnt
            print(f"  Difficulty Breakdown: {diff_counts}")
            print("-" * 60)

        print("\nTOPIC COVERAGE CHECK:")
        missing_topics = []
        for cat_name, topics in [("Quantitative Aptitude", QUANT_TOPICS), ("Logical Reasoning", LOGICAL_TOPICS), ("Verbal Ability", VERBAL_TOPICS)]:
            cat = AptitudeCategory.query.filter_by(name=cat_name).first()
            if not cat:
                print(f"  [MISSING CATEGORY] {cat_name}")
                continue
            for t in topics:
                cnt = AptitudeQuestion.query.filter_by(category_id=cat.id, topic=t).count()
                if cnt == 0:
                    missing_topics.append(f"{cat_name} -> {t}")

        if missing_topics:
            print(f"  Found {len(missing_topics)} topics with 0 questions:")
            for m in missing_topics[:10]:
                print(f"    - {m}")
            if len(missing_topics) > 10:
                print(f"    ... and {len(missing_topics) - 10} more.")
        else:
            print("  All 64 topics have questions in the database!")
        print("=" * 60)


if __name__ == '__main__':
    inspect_bank()
