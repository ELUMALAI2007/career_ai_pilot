"""
CareerPilot AI - Placement Question Bank: Logical Reasoning
Contains verified placement-oriented Logical Reasoning questions across series, coding, relations,
directions, arrangements, syllogisms, and puzzle reasoning following R.S. Aggarwal standards.
"""

from typing import List, Dict, Any

LOGICAL_BANK: List[Dict[str, Any]] = [
    # ------------------ NUMBER SERIES ------------------
    {
        "question": "Find the missing number in the given series:\n\n**4, 9, 19, 39, 79, ?**",
        "category": "Logical Reasoning",
        "topic": "Number Series",
        "subtopic": "Pattern Recognition",
        "difficulty": "Easy",
        "options": ["159", "149", "169", "154"],
        "correct_answer": "A",
        "explanation": "Pattern: Each term is obtained by multiplying the previous term by 2 and adding 1.\n4 × 2 + 1 = 9\n9 × 2 + 1 = 19\n19 × 2 + 1 = 39\n39 × 2 + 1 = 79\n79 × 2 + 1 = 159.",
        "formula": "T_n = 2 × T_{n-1} + 1",
        "shortcut": "Multiply by 2 and add 1.",
        "concept": "Series Multiplication & Increment",
        "time_limit": 45
    },
    {
        "question": "Identify the next term in the logical sequence:\n\n**2, 6, 12, 20, 30, 42, ?**",
        "category": "Logical Reasoning",
        "topic": "Number Series",
        "subtopic": "Difference Series",
        "difficulty": "Medium",
        "options": ["56", "54", "60", "50"],
        "correct_answer": "A",
        "explanation": "Differences between consecutive terms: +4, +6, +8, +10, +12. Next difference is +14.\n42 + 14 = 56.\nAlternatively: n^2 + n (1^2+1=2, 2^2+2=6, ..., 7^2+7 = 49+7 = 56).",
        "formula": "T_n = n^2 + n or Consecutive even differences (+4, +6, +8...)",
        "shortcut": "n(n+1) formula: 7 × 8 = 56.",
        "concept": "Quadratic Difference Series",
        "time_limit": 45
    },

    # ------------------ CODING-DECODING ------------------
    {
        "question": "In a certain placement code language, **SYSTEM** is coded as **SYSMET** and **NEARER** is coded as **AENRER**. How is **FRACTION** coded in that same language?",
        "category": "Logical Reasoning",
        "topic": "Coding-Decoding",
        "subtopic": "Letter Reversal & Grouping",
        "difficulty": "Medium",
        "options": ["CARFNOIT", "ARFCNOIT", "CARFTION", "FARCTINO"],
        "correct_answer": "A",
        "explanation": "The word is divided into two equal halves. The first half is reversed, and the second half is reversed.\n'FRACTION' has 8 letters: First half 'FRAC' reversed -> 'CARF'. Second half 'TION' reversed -> 'NOIT'.\nCombined code = 'CARFNOIT'.",
        "formula": "Split string into 2 halves and reverse each half",
        "shortcut": "Reverse first 4 letters (FRAC -> CARF) and last 4 letters (TION -> NOIT).",
        "concept": "Positional Code Transformation",
        "time_limit": 50
    },

    # ------------------ BLOOD RELATIONS ------------------
    {
        "question": "Pointing to a photograph of a man, Rahul said, \"His mother is the only daughter of my mother-in-law.\" How is Rahul related to the man in the photograph?",
        "category": "Logical Reasoning",
        "topic": "Blood Relations",
        "subtopic": "Pointing to Photograph",
        "difficulty": "Medium",
        "options": ["Father", "Uncle", "Brother", "Grandfather"],
        "correct_answer": "A",
        "explanation": "'Only daughter of my mother-in-law' means Rahul's wife.\n'His mother' = Rahul's wife.\nTherefore, the man in the photograph is Rahul's son, which makes Rahul his Father.",
        "formula": "Relation Tree Deduction",
        "shortcut": "Mother-in-law's only daughter = Wife. Wife's son = Rahul's son.",
        "concept": "Familial Relationship Mapping",
        "time_limit": 50
    },

    # ------------------ DIRECTION SENSE ------------------
    {
        "question": "A candidate walks 10 km towards North, then turns Right and walks 6 km. Then he turns Right again and walks 18 km. How far and in which direction is he now from his starting point?",
        "category": "Logical Reasoning",
        "topic": "Direction Sense",
        "subtopic": "Pythagoras Distance & Direction",
        "difficulty": "Hard",
        "options": [
            "10 km, South-East",
            "10 km, North-East",
            "12 km, South-East",
            "8 km, South-West"
        ],
        "correct_answer": "A",
        "explanation": "Net North displacement = 10 - 18 = -8 km (8 km South).\nNet East displacement = 6 km East.\nShortest Distance = √(8^2 + 6^2) = √(64 + 36) = √100 = 10 km.\nDirection relative to origin = South-East.",
        "formula": "Distance = √(x^2 + y^2)",
        "shortcut": "3-4-5 Pythagorean triplet scaled by 2: (6, 8, 10). Direction: South and East.",
        "concept": "Coordinate Vector Geometry",
        "time_limit": 60
    },

    # ------------------ SEATING ARRANGEMENT ------------------
    {
        "question": "Five candidates A, B, C, D, and E are sitting in a row facing North. B is sitting to the immediate right of E. C is sitting at one of the extreme ends and is to the immediate left of D. Who is sitting in the exact middle position?",
        "category": "Logical Reasoning",
        "topic": "Seating Arrangement",
        "subtopic": "Linear Row Placement",
        "difficulty": "Medium",
        "options": ["A", "B", "E", "D"],
        "correct_answer": "A",
        "explanation": "C is at left extreme end: Position 1 = C.\nImmediate right of C is D: Position 2 = D.\nPosition 4 & 5 must be E and B because B is to the immediate right of E (E, B).\nRemaining position 3 must be A.\nArrangement from Left to Right: C, D, A, E, B. Middle position (3rd) is A.",
        "formula": "Step-by-step Positional Elimination",
        "shortcut": "Fix extreme end C first, then place D, leaving middle open.",
        "concept": "Linear Arrangement Constraints",
        "time_limit": 60
    },

    # ------------------ SYLLOGISMS ------------------
    {
        "question": "Statements:\n1. All engineers are logical.\n2. All logical people are problem solvers.\n\nConclusions:\nI. All engineers are problem solvers.\nII. Some problem solvers are engineers.",
        "category": "Logical Reasoning",
        "topic": "Syllogism",
        "subtopic": "Categorical Logic",
        "difficulty": "Easy",
        "options": [
            "Both Conclusion I and II follow",
            "Only Conclusion I follows",
            "Only Conclusion II follows",
            "Neither Conclusion I nor II follows"
        ],
        "correct_answer": "A",
        "explanation": "All A are B, All B are C => All A are C (Conclusion I is valid).\nIf All A are C, then automatically Some C are A (Conclusion II is valid).\nBoth conclusions logically follow.",
        "formula": "Barbara Syllogism (All A->B, All B->C => All A->C)",
        "shortcut": "Venn Diagram concentric circles: Engineers ⊂ Logical ⊂ Problem Solvers.",
        "concept": "Logical Deduction Rules",
        "time_limit": 45
    },

    # ------------------ CLOCKS & CALENDARS ------------------
    {
        "question": "What is the angle between the hour hand and the minute hand of a clock at 3:30?",
        "category": "Logical Reasoning",
        "topic": "Clocks",
        "subtopic": "Hand Angle Calculation",
        "difficulty": "Medium",
        "options": ["75 degrees", "90 degrees", "60 degrees", "85 degrees"],
        "correct_answer": "A",
        "explanation": "Formula for angle θ = |30H - 5.5M|\nFor H = 3, M = 30:\nθ = |30(3) - 5.5(30)| = |90 - 165| = |-75| = 75°.",
        "formula": "θ = |30H - 11/2 M|",
        "shortcut": "|90 - 165| = 75 degrees.",
        "concept": "Clock Angle Mechanics",
        "time_limit": 45
    }
]


def get_logical_questions() -> List[Dict[str, Any]]:
    """Returns verified placement-standard Logical Reasoning questions."""
    return LOGICAL_BANK
