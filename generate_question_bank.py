"""
CareerPilot AI - Batch Question Bank Generator & Seeder
Seeds 1,000 unique, placement-oriented aptitude questions across Quantitative, Logical Reasoning, and Verbal Ability.
Ensures duplicate prevention via SHA-256 fingerprint hashing and validates option uniqueness.
"""

import os
import sys
import logging
import hashlib

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.aptitude import AptitudeCategory, AptitudeQuestion
from app.utils.aptitude_validator import validate_question, normalize_difficulty
from data.aptitude import load_question_bank

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def generate_fingerprint(question_text: str, options: list, correct_option: str) -> str:
    """Generates SHA-256 fingerprint hash for duplicate detection."""
    raw_str = f"{question_text.strip().lower()}|" + "|".join([str(o).strip().lower() for o in options]) + f"|{correct_option}"
    return hashlib.sha256(raw_str.encode('utf-8')).hexdigest()


def seed_categories():
    """Ensures primary Aptitude Categories exist in the database."""
    categories_def = [
        ("Quantitative Aptitude", "Numerical computation, arithmetic, algebra, geometry, and data interpretation.", "fa-calculator"),
        ("Logical Reasoning", "Analytical thinking, pattern recognition, series, blood relations, and arrangements.", "fa-brain"),
        ("Verbal Ability", "Grammar, vocabulary, sentence correction, reading comprehension, and idioms.", "fa-font")
    ]
    cat_map = {}
    for name, desc, icon in categories_def:
        cat = AptitudeCategory.query.filter_by(name=name).first()
        if not cat:
            cat = AptitudeCategory(name=name, description=desc, icon=icon)
            db.session.add(cat)
            db.session.commit()
        cat_map[name] = cat
    return cat_map


def generate_batch():
    """Seeds 1,000 verified placement aptitude questions into the database."""
    from flask import current_app
    if current_app:
        _do_generate_batch()
    else:
        app = create_app()
        with app.app_context():
            _do_generate_batch()


def _do_generate_batch():
    db.create_all()
    cat_map = seed_categories()

    bank = load_question_bank()
    logging.info(f"Loaded {len(bank)} verified questions from aptitude bank.")

    inserted_count = 0
    skipped_count = 0
    invalid_count = 0
    valid_count = 0

    easy_count = 0
    med_count = 0
    hard_count = 0

    quant_count = 0
    logical_count = 0
    verbal_count = 0

    # Purge old dummy / placeholder questions if present
    placeholder_qs = AptitudeQuestion.query.filter(
        (AptitudeQuestion.question_text.like("%In Synonyms (%")) |
        (AptitudeQuestion.question_text.like("%If sequence X =%")) |
        (AptitudeQuestion.question_text.like("%If a variable x =%"))
    ).all()
    if placeholder_qs:
        logging.info(f"Purging {len(placeholder_qs)} old placeholder questions from database...")
        for pq in placeholder_qs:
            db.session.delete(pq)
        db.session.commit()

    existing_fingerprints = {
        fp[0] for fp in db.session.query(AptitudeQuestion.fingerprint).all() if fp[0]
    }

    for item in bank:
        is_valid, err = validate_question(item)
        if not is_valid:
            invalid_count += 1
            logging.warning(f"Skipping invalid question: {err}")
            continue

        valid_count += 1
        cat_name = item.get("category", "Quantitative Aptitude")
        cat = cat_map.get(cat_name)
        if not cat:
            cat = cat_map.get("Quantitative Aptitude")

        options = item.get("options", [])
        opt_a, opt_b, opt_c, opt_d = options[0], options[1], options[2], options[3]

        correct_raw = item.get("correct_answer") or item.get("correct_option")
        correct_opt = str(correct_raw).upper()

        q_text = item.get("question") or item.get("question_text")
        fp = generate_fingerprint(q_text, [opt_a, opt_b, opt_c, opt_d], correct_opt)

        if fp in existing_fingerprints:
            skipped_count += 1
            continue

        norm_diff = normalize_difficulty(item.get("difficulty", "Medium"))
        if norm_diff == "Easy":
            easy_count += 1
        elif norm_diff == "Medium":
            med_count += 1
        elif norm_diff == "Hard":
            hard_count += 1

        if cat_name == "Quantitative Aptitude":
            quant_count += 1
        elif cat_name == "Logical Reasoning":
            logical_count += 1
        elif cat_name == "Verbal Ability":
            verbal_count += 1

        question = AptitudeQuestion(
            category_id=cat.id,
            topic=item.get("topic", "General"),
            subtopic=item.get("subtopic", ""),
            difficulty=norm_diff,
            question_text=q_text,
            option_a=opt_a,
            option_b=opt_b,
            option_c=opt_c,
            option_d=opt_d,
            correct_option=correct_opt,
            explanation=item.get("explanation", "Explanation not available."),
            formula=item.get("formula"),
            shortcut=item.get("shortcut"),
            concept=item.get("concept"),
            estimated_time=item.get("time_limit", 60),
            tags=item.get("topic"),
            source_type="generated",
            fingerprint=fp
        )

        db.session.add(question)
        existing_fingerprints.add(fp)
        inserted_count += 1

        if inserted_count % 100 == 0:
            db.session.commit()
            logging.info(f"Inserted {inserted_count} questions...")

    db.session.commit()

    print("\n" + "=" * 25)
    print("TOTAL QUESTIONS")
    print("================")
    print(f"Quantitative: {quant_count}")
    print(f"Logical:      {logical_count}")
    print(f"Verbal:       {verbal_count}")
    print()
    print(f"Easy:   {easy_count}")
    print(f"Medium: {med_count}")
    print(f"Hard:   {hard_count}")
    print()
    print(f"Valid:      {valid_count}")
    print(f"Invalid:    {invalid_count}")
    print(f"Duplicates: {skipped_count}")
    print(f"Inserted:   {inserted_count}")
    print("=" * 25 + "\n")


if __name__ == '__main__':
    generate_batch()
