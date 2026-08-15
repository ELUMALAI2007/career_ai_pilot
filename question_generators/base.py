"""
CareerPilot AI - Algorithmic Question Generator Base Engine
Provides base classes, parameter variation, option shuffling, strict validation, and fingerprint calculation.
"""

import hashlib
import random
from typing import Dict, Any, List, Optional


class BaseQuestionGenerator:
    """Base class for all algorithmic topic question generators."""

    category_name: str = ""
    topic_name: str = ""

    @staticmethod
    def generate_fingerprint(question_text: str, options: List[str], correct_option: str) -> str:
        """Generates a SHA-256 fingerprint hash for duplicate detection."""
        raw_str = f"{question_text.strip().lower()}|" + "|".join([o.strip().lower() for o in options]) + f"|{correct_option}"
        return hashlib.sha256(raw_str.encode('utf-8')).hexdigest()

    @staticmethod
    def format_options_and_answer(correct_val: Any, distractors: List[Any], format_fn=str) -> Dict[str, Any]:
        """
        Shuffles the correct value with 3 distinct distractors and returns option A, B, C, D and correct_option.
        """
        formatted_correct = format_fn(correct_val)
        formatted_distractors = list({format_fn(d) for d in distractors if format_fn(d) != formatted_correct})
        
        # Ensure we have at least 3 unique distractors
        attempts = 0
        while len(formatted_distractors) < 3 and attempts < 20:
            attempts += 1
            if isinstance(correct_val, (int, float)):
                offset = random.choice([-5, -2, -1, 1, 2, 5, 10, 15, -10])
                fake = format_fn(correct_val + offset)
            else:
                fake = f"Option {len(formatted_distractors) + 1}"
            if fake != formatted_correct and fake not in formatted_distractors:
                formatted_distractors.append(fake)

        all_choices = [formatted_correct] + formatted_distractors[:3]
        random.shuffle(all_choices)

        option_keys = ['A', 'B', 'C', 'D']
        options_dict = {f"option_{k.lower()}": choice for k, choice in zip(option_keys, all_choices)}
        correct_key = option_keys[all_choices.index(formatted_correct)]

        return {
            **options_dict,
            "correct_option": correct_key
        }

    @classmethod
    def validate_question_dict(cls, q_dict: Dict[str, Any]) -> bool:
        """Validates question payload to ensure 4 unique non-empty options and 1 valid answer."""
        required = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option', 'explanation']
        if not all(k in q_dict and q_dict[k] for k in required):
            return False

        if q_dict['correct_option'] not in ['A', 'B', 'C', 'D']:
            return False

        options = [q_dict['option_a'], q_dict['option_b'], q_dict['option_c'], q_dict['option_d']]
        if len(set(options)) != 4:
            return False  # Must have 4 unique options

        return True
