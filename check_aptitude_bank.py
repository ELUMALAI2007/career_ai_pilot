"""
CareerPilot AI - Diagnostic Aptitude Question Bank Inspector
Reports question counts by category, topic, difficulty (Easy, Medium, Hard), and checks missing topic coverage.
"""

import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.aptitude import AptitudeCategory, AptitudeQuestion
from app.utils.aptitude_validator import validate_question, QUANT_TOPICS, LOGICAL_TOPICS, VERBAL_TOPICS, normalize_difficulty
from data.aptitude import load_question_bank


def inspect_bank():
    app = create_app()
    with app.app_context():
        total_db = AptitudeQuestion.query.count()
        bank = load_question_bank()

        quant_cnt = 0
        logical_cnt = 0
        verbal_cnt = 0

        easy_cnt = 0
        med_cnt = 0
        hard_cnt = 0

        valid_cnt = 0
        invalid_cnt = 0
        duplicate_cnt = 0

        seen_fp = set()

        for q in bank:
            is_valid, err = validate_question(q)
            if not is_valid:
                invalid_cnt += 1
                continue

            valid_cnt += 1
            q_text = str(q.get("question") or q.get("question_text")).strip().lower()
            if q_text in seen_fp:
                duplicate_cnt += 1
                continue
            seen_fp.add(q_text)

            cat = q.get("category", "Quantitative Aptitude")
            if cat == "Quantitative Aptitude":
                quant_cnt += 1
            elif cat == "Logical Reasoning":
                logical_cnt += 1
            elif cat == "Verbal Ability":
                verbal_cnt += 1

            diff = normalize_difficulty(q.get("difficulty"))
            if diff == "Easy":
                easy_cnt += 1
            elif diff == "Medium":
                med_cnt += 1
            elif diff == "Hard":
                hard_cnt += 1

        print("=" * 65)
        print("        CAREERPILOT AI - ADVANCED APTITUDE ENGINE DIAGNOSTIC")
        print("=" * 65)
        print("TOTAL QUESTIONS")
        print("================")
        print(f"Quantitative: {quant_cnt}")
        print(f"Logical:      {logical_cnt}")
        print(f"Verbal:       {verbal_cnt}")
        print()
        print(f"Easy:   {easy_cnt}")
        print(f"Medium: {med_cnt}")
        print(f"Hard:   {hard_cnt}")
        print()
        print(f"Valid:      {valid_cnt}")
        print(f"Invalid:    {invalid_cnt}")
        print(f"Duplicates: {duplicate_cnt}")
        print(f"Inserted:   {total_db}")
        print("-" * 65)

        print("\n55 TOPICS COVERAGE CHECK:")
        missing_topics = []
        topic_groups = [
            ("Quantitative Aptitude", QUANT_TOPICS),
            ("Logical Reasoning", LOGICAL_TOPICS),
            ("Verbal Ability", VERBAL_TOPICS)
        ]

        for cat_name, topics in topic_groups:
            cat = AptitudeCategory.query.filter_by(name=cat_name).first()
            if not cat:
                print(f"  [MISSING CATEGORY] {cat_name}")
                continue
            for t in topics:
                cnt = AptitudeQuestion.query.filter(
                    AptitudeQuestion.category_id == cat.id,
                    db.func.lower(AptitudeQuestion.topic) == t.lower()
                ).count()
                if cnt == 0:
                    missing_topics.append(f"{cat_name} -> {t}")

        if missing_topics:
            print(f"  Found {len(missing_topics)} topics missing in DB:")
            for m in missing_topics:
                print(f"    - {m}")
        else:
            print("  [SUCCESS] All 55 topics have verified questions in the database!")
        print("=" * 65)

        print("\n20 APTITUDE DATABASE TABLES AUDIT:")
        inspector = db.inspect(db.engine)
        table_names = inspector.get_table_names()
        expected_tables = [
            'aptitude_categories', 'aptitude_questions', 'aptitude_attempts',
            'aptitude_question_answers', 'aptitude_bookmarks', 'aptitude_progress',
            'aptitude_topic_mastery', 'aptitude_test_sessions', 'aptitude_test_results',
            'aptitude_daily_challenges', 'aptitude_daily_challenge_attempts', 'aptitude_streaks',
            'aptitude_generation_logs', 'aptitude_category_performance', 'aptitude_difficulty_performance',
            'aptitude_recommendations', 'aptitude_readiness_scores', 'aptitude_level_progress'
        ]

        all_tables_present = True
        for t in expected_tables:
            if t in table_names:
                print(f"  [OK] Table '{t}': PRESENT")
            else:
                print(f"  [FAIL] Table '{t}': MISSING")
                all_tables_present = False

        print("=" * 65)
        if all_tables_present and total_db == 1000 and len(missing_topics) == 0:
            print("APTITUDE DATABASE STATUS: HEALTHY [OK]")
        else:
            print(f"APTITUDE DATABASE STATUS: ATTENTION REQUIRED (Total DB Qs: {total_db})")
        print("=" * 65)


if __name__ == '__main__':
    inspect_bank()
