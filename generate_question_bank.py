"""
CareerPilot AI - Batch Question Bank Generator & Seeder
Generates 1,500+ original, placement-oriented aptitude questions across Quantitative, Logical Reasoning, and Verbal Ability.
Ensures duplicate prevention via SHA-256 fingerprint hashing and validates option uniqueness.
"""

import os
import sys
import logging

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.aptitude import AptitudeCategory, AptitudeQuestion
from question_generators import (
    QUANT_TOPICS, LOGICAL_TOPICS, VERBAL_TOPICS,
    DIFFICULTY_LEVELS, generate_question_for_topic
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


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
    """Batch generates 1,500+ original questions across topics and difficulty levels."""
    app = create_app()
    with app.app_context():
        # Create database tables if they do not exist
        db.create_all()
        
        cat_map = seed_categories()

        # Target minimum question counts
        targets = [
            ("Quantitative Aptitude", QUANT_TOPICS, 600),
            ("Logical Reasoning", LOGICAL_TOPICS, 450),
            ("Verbal Ability", VERBAL_TOPICS, 450)
        ]

        total_inserted = 0

        for cat_name, topics, target_count in targets:
            cat = cat_map.get(cat_name)
            if not cat:
                continue

            existing_fingerprints = {
                fp[0] for fp in db.session.query(AptitudeQuestion.fingerprint).filter(
                    AptitudeQuestion.category_id == cat.id
                ).all() if fp[0]
            }

            logging.info(f"Starting generation for '{cat_name}' (Target: {target_count}, Existing: {len(existing_fingerprints)})...")
            
            inserted_for_cat = 0
            attempts = 0
            max_attempts = target_count * 20

            while inserted_for_cat + len(existing_fingerprints) < target_count and attempts < max_attempts:
                attempts += 1
                topic_name = topics[attempts % len(topics)]
                difficulty = DIFFICULTY_LEVELS[attempts % len(DIFFICULTY_LEVELS)]

                try:
                    q_dict = generate_question_for_topic(cat_name, topic_name, difficulty)
                    fp = q_dict.get('fingerprint')

                    if not fp or fp in existing_fingerprints:
                        continue

                    # Add to DB session
                    question = AptitudeQuestion(
                        category_id=cat.id,
                        topic=q_dict['topic'],
                        subtopic=q_dict.get('subtopic', ''),
                        difficulty=q_dict['difficulty'],
                        question_text=q_dict['question_text'],
                        option_a=q_dict['option_a'],
                        option_b=q_dict['option_b'],
                        option_c=q_dict['option_c'],
                        option_d=q_dict['option_d'],
                        correct_option=q_dict['correct_option'],
                        explanation=q_dict['explanation'],
                        formula=q_dict.get('formula'),
                        shortcut=q_dict.get('shortcut'),
                        concept=q_dict.get('concept'),
                        estimated_time=q_dict.get('estimated_time', 60),
                        tags=q_dict.get('tags'),
                        source_type='generated',
                        fingerprint=fp
                    )
                    db.session.add(question)
                    db.session.commit()

                    existing_fingerprints.add(fp)
                    inserted_for_cat += 1
                    total_inserted += 1

                    if inserted_for_cat % 50 == 0:
                        logging.info(f"[{cat_name}] Saved {inserted_for_cat} questions...")
                except Exception as e:
                    db.session.rollback()
                    logging.warning(f"Error generating item: {e}")

            logging.info(f"Finished '{cat_name}': {inserted_for_cat} new questions saved (Total in cat: {len(existing_fingerprints)}).")

        logging.info(f"Batch generation completed successfully! Total new questions added: {total_inserted}.")


if __name__ == '__main__':
    generate_batch()
