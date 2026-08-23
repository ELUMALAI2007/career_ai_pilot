"""
CareerPilot AI - Placement Question Bank: Quantitative Aptitude
Contains verified placement-oriented Quantitative Aptitude questions across arithmetic, algebra,
geometry, mensuration, and data interpretation following R.S. Aggarwal standards.
"""

from typing import List, Dict, Any

QUANTITATIVE_BANK: List[Dict[str, Any]] = [
    # ------------------ NUMBER SYSTEM ------------------
    {
        "question": "Find the remainder when 7^84 is divided by 342.",
        "category": "Quantitative Aptitude",
        "topic": "Number System",
        "subtopic": "Divisibility & Remainders",
        "difficulty": "Hard",
        "options": ["1", "341", "49", "7"],
        "correct_answer": "A",
        "explanation": "7^3 = 343. So 7^84 = (7^3)^28 = (343)^28. When 343 is divided by 342, the remainder is 1. Thus (1)^28 = 1.",
        "formula": "Remainder Rule: (a + 1)^n mod a = 1",
        "shortcut": "Express 7^3 = 343 = 342 + 1.",
        "concept": "Modular Arithmetic & Remainder Theorem",
        "time_limit": 60
    },
    {
        "question": "How many trailing zeros are there at the end of 100! (100 factorial)?",
        "category": "Quantitative Aptitude",
        "topic": "Number System",
        "subtopic": "Factorials & Zeros",
        "difficulty": "Medium",
        "options": ["24", "20", "25", "22"],
        "correct_answer": "A",
        "explanation": "Trailing zeros in N! = [N/5] + [N/25] + [N/125]... For 100!: [100/5] + [100/25] = 20 + 4 = 24 zeros.",
        "formula": "Legendre's Formula: Sum of floor(N / 5^k)",
        "shortcut": "100 // 5 = 20; 20 // 5 = 4. Total = 24.",
        "concept": "Factorials & Prime Factorization",
        "time_limit": 50
    },
    {
        "question": "What is the unit digit in the expansion of 3^65 × 6^59 × 7^71?",
        "category": "Quantitative Aptitude",
        "topic": "Number System",
        "subtopic": "Unit Digit Calculation",
        "difficulty": "Medium",
        "options": ["4", "2", "6", "8"],
        "correct_answer": "A",
        "explanation": "Cyclicity: 3 has cyclicity 4 (3^1=3, 3^2=9, 3^3=7, 3^4=1). 65 mod 4 = 1 => 3^1 = 3.\n6 has cyclicity 1 => always 6.\n7 has cyclicity 4 (7^1=7, 7^2=9, 7^3=3, 7^4=1). 71 mod 4 = 3 => 7^3 = 3.\nProduct of unit digits: 3 × 6 × 3 = 54 => Unit digit is 4.",
        "formula": "Unit Digit Cyclicity Rule",
        "shortcut": "Power mod 4 rule for unit digits.",
        "concept": "Cyclicity of Numbers",
        "time_limit": 60
    },

    # ------------------ HCF & LCM ------------------
    {
        "question": "The HCF of two numbers is 11 and their LCM is 693. If one of the numbers is 77, find the other number.",
        "category": "Quantitative Aptitude",
        "topic": "HCF & LCM",
        "subtopic": "Properties of HCF and LCM",
        "difficulty": "Easy",
        "options": ["99", "88", "108", "92"],
        "correct_answer": "A",
        "explanation": "Formula: Product of two numbers = HCF × LCM.\n77 × N2 = 11 × 693 => N2 = (11 × 693) / 77 = 693 / 7 = 99.",
        "formula": "N1 × N2 = HCF × LCM",
        "shortcut": "Cancel 11 and 77 to get 7 in denominator, 693/7 = 99.",
        "concept": "HCF and LCM Relationships",
        "time_limit": 45
    },
    {
        "question": "Find the smallest number which when divided by 12, 16, 24, and 36 leaves a remainder of 7 in each case.",
        "category": "Quantitative Aptitude",
        "topic": "HCF & LCM",
        "subtopic": "Common Remainders",
        "difficulty": "Medium",
        "options": ["151", "144", "137", "160"],
        "correct_answer": "A",
        "explanation": "LCM(12, 16, 24, 36) = 144. Required number = LCM + Remainder = 144 + 7 = 151.",
        "formula": "Required Number = LCM(Divisors) + Constant Remainder",
        "shortcut": "Find LCM of 12, 16, 24, 36 (which is 144) and add 7.",
        "concept": "Least Common Multiple Applications",
        "time_limit": 50
    },

    # ------------------ PERCENTAGES ------------------
    {
        "question": "If the price of petrol increases by 25%, by what percentage must a motorist reduce his consumption so that expenditure remains unchanged?",
        "category": "Quantitative Aptitude",
        "topic": "Percentages",
        "subtopic": "Consumption & Price Change",
        "difficulty": "Easy",
        "options": ["20%", "25%", "15%", "30%"],
        "correct_answer": "A",
        "explanation": "Formula: Reduction = [R / (100 + R)] × 100%\nReduction = [25 / (100 + 25)] × 100% = [25 / 125] × 100% = (1/5) × 100% = 20%.",
        "formula": "% Reduction = [R / (100 + R)] × 100",
        "shortcut": "25% increase = 1/4 fraction up => 1/5 fraction down = 20%.",
        "concept": "Inverse Proportionality in Percentages",
        "time_limit": 45
    },
    {
        "question": "In a college placement exam, a candidate needs 40% marks to pass. A student scores 175 marks and fails by 25 marks. What is the maximum total marks of the exam?",
        "category": "Quantitative Aptitude",
        "topic": "Percentages",
        "subtopic": "Exam Marks Calculation",
        "difficulty": "Easy",
        "options": ["500", "450", "600", "400"],
        "correct_answer": "A",
        "explanation": "Passing Marks = 175 + 25 = 200.\n40% of Total Marks = 200 => Total Marks = (200 × 100) / 40 = 500.",
        "formula": "Total Marks = (Passing Marks × 100) / Passing Percentage",
        "shortcut": "40% = 200 => 10% = 50 => 100% = 500.",
        "concept": "Percentage Base Calculation",
        "time_limit": 45
    },

    # ------------------ PROFIT & LOSS ------------------
    {
        "question": "A shopkeeper buys an article for ₹800 and marks it 50% above cost price. If he allows a discount of 20% on the marked price, what is his net profit percentage?",
        "category": "Quantitative Aptitude",
        "topic": "Profit & Loss",
        "subtopic": "Marked Price & Discount",
        "difficulty": "Medium",
        "options": ["20%", "25%", "30%", "15%"],
        "correct_answer": "A",
        "explanation": "Cost Price (CP) = ₹800.\nMarked Price (MP) = 800 + 50% of 800 = ₹1200.\nSelling Price (SP) = 1200 - 20% of 1200 = 1200 - 240 = ₹960.\nProfit = SP - CP = 960 - 800 = ₹160.\nProfit % = (160 / 800) × 100% = 20%.",
        "formula": "Net % Change = A + B + (A×B)/100",
        "shortcut": "Successive change: +50 - 20 - (50×20)/100 = +30 - 10 = +20%.",
        "concept": "Successive Percentage Discounts",
        "time_limit": 50
    },

    # ------------------ SIMPLE & COMPOUND INTEREST ------------------
    {
        "question": "What is the difference between Compound Interest and Simple Interest on ₹10,000 for 2 years at 10% per annum compounded annually?",
        "category": "Quantitative Aptitude",
        "topic": "Simple & Compound Interest",
        "subtopic": "CI vs SI Difference",
        "difficulty": "Medium",
        "options": ["₹100", "₹200", "₹150", "₹250"],
        "correct_answer": "A",
        "explanation": "Difference for 2 years = P × (R / 100)^2\nDiff = 10,000 × (10 / 100)^2 = 10,000 × (1 / 100) = ₹100.",
        "formula": "D_2 = P × (R / 100)^2",
        "shortcut": "2-year diff = P × (R%)^2 = 10000 × 0.01 = 100.",
        "concept": "Compound Interest Properties",
        "time_limit": 45
    },

    # ------------------ TIME & WORK ------------------
    {
        "question": "A can complete a piece of work in 12 days and B can complete the same work in 24 days. If they work together, in how many days will they finish the entire work?",
        "category": "Quantitative Aptitude",
        "topic": "Time & Work",
        "subtopic": "Joint Efficiency",
        "difficulty": "Easy",
        "options": ["8 days", "10 days", "6 days", "9 days"],
        "correct_answer": "A",
        "explanation": "A's 1-day work = 1/12. B's 1-day work = 1/24.\nCombined 1-day work = (1/12 + 1/24) = (2+1)/24 = 3/24 = 1/8.\nTotal time = 8 days.",
        "formula": "Combined Time = (A × B) / (A + B)",
        "shortcut": "Time = (12 × 24) / (12 + 24) = 288 / 36 = 8 days.",
        "concept": "Work & Efficiency Relations",
        "time_limit": 45
    },

    # ------------------ TIME, SPEED & DISTANCE ------------------
    {
        "question": "A train 150 meters long is traveling at a uniform speed of 54 km/hr. How much time will it take to cross a platform 250 meters long?",
        "category": "Quantitative Aptitude",
        "topic": "Time, Speed & Distance",
        "subtopic": "Problems on Trains",
        "difficulty": "Medium",
        "options": ["26.67 seconds", "20 seconds", "30 seconds", "24 seconds"],
        "correct_answer": "A",
        "explanation": "Speed in m/s = 54 × (5/18) = 15 m/s.\nTotal distance to cover = Train length + Platform length = 150 + 250 = 400 meters.\nTime = Distance / Speed = 400 / 15 = 26.67 seconds.",
        "formula": "Speed (m/s) = Speed (km/h) × (5/18); Time = Distance / Speed",
        "shortcut": "54 km/h = 15 m/s; 400 / 15 = 26.67 s.",
        "concept": "Relative Motion & Unit Conversions",
        "time_limit": 50
    },
    {
        "question": "A boat travels downstream at 18 km/hr and upstream at 12 km/hr. Find the speed of the boat in still water and the speed of the current.",
        "category": "Quantitative Aptitude",
        "topic": "Boats & Streams",
        "subtopic": "Upstream & Downstream",
        "difficulty": "Easy",
        "options": [
            "Boat = 15 km/h, Current = 3 km/h",
            "Boat = 14 km/h, Current = 4 km/h",
            "Boat = 16 km/h, Current = 2 km/h",
            "Boat = 15 km/h, Current = 4 km/h"
        ],
        "correct_answer": "A",
        "explanation": "Speed in still water = (Downstream + Upstream) / 2 = (18 + 12) / 2 = 15 km/h.\nSpeed of current = (Downstream - Upstream) / 2 = (18 - 12) / 2 = 3 km/h.",
        "formula": "u = (D + U)/2 ; v = (D - U)/2",
        "shortcut": "Average of 18 and 12 is 15. Half diff is 3.",
        "concept": "Relative Water Motion",
        "time_limit": 45
    },

    # ------------------ PERMUTATION & COMBINATION ------------------
    {
        "question": "In how many different ways can the letters of the word 'PLACEMENT' be arranged?",
        "category": "Quantitative Aptitude",
        "topic": "Permutation & Combination",
        "subtopic": "Word Arrangements",
        "difficulty": "Medium",
        "options": ["181,440", "362,880", "90,720", "40,320"],
        "correct_answer": "A",
        "explanation": "'PLACEMENT' has 9 letters with letter 'E' repeating 2 times.\nTotal arrangements = 9! / 2! = 362,880 / 2 = 181,440.",
        "formula": "Permutations = N! / (p1! × p2!...)",
        "shortcut": "9! = 362,880. Divide by 2! for repeating E => 181,440.",
        "concept": "Permutations with Repetition",
        "time_limit": 50
    },

    # ------------------ PROBABILITY ------------------
    {
        "question": "Two fair six-sided dice are rolled simultaneously. What is the probability that the sum of the numbers appearing on top is equal to 8?",
        "category": "Quantitative Aptitude",
        "topic": "Probability",
        "subtopic": "Dice Outcomes",
        "difficulty": "Easy",
        "options": ["5/36", "1/6", "7/36", "1/9"],
        "correct_answer": "A",
        "explanation": "Total sample space outcomes = 6 × 6 = 36.\nFavorable pairs summing to 8: (2,6), (3,5), (4,4), (5,3), (6,2) = 5 pairs.\nProbability = 5 / 36.",
        "formula": "Probability = Favorable Outcomes / Total Outcomes",
        "shortcut": "Sum 8 on 2 dice has 5 favorable combinations.",
        "concept": "Basic Probability Principles",
        "time_limit": 45
    }
]


def get_quantitative_questions() -> List[Dict[str, Any]]:
    """Returns verified placement-standard Quantitative Aptitude questions."""
    return QUANTITATIVE_BANK
