"""
CareerPilot AI - Coding & DSA Database Seeder
Seeds initial problem collection across Easy, Medium, and Hard difficulties,
including complete test cases (sample & hidden), starter code templates, and badges.
"""

import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.coding import CodingProblem, CodingBadge
from config import DevelopmentConfig


PROBLEMS_DATA = [
    # ==================== EASY PROBLEMS ====================
    {
        "title": "Two Sum",
        "slug": "two-sum",
        "topic": "Arrays",
        "difficulty": "easy",
        "company_tags": "Amazon, Google, Microsoft, Meta, Apple",
        "xp_reward": 10,
        "description": "Given an array of integers `nums` and an integer `target`, return the 0-based indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.",
        "input_format": "Line 1: Space-separated integers representing the array `nums`.\nLine 2: Single integer `target`.",
        "output_format": "Two space-separated 0-based indices sorted in ascending order (e.g. `0 1`).",
        "constraints": "- 2 <= nums.length <= 10^4\n- -10^9 <= nums[i] <= 10^9\n- -10^9 <= target <= 10^9\n- Only one valid answer exists.",
        "starter_templates": {
            "python": 'def two_sum(nums, target):\n    # Write your solution here\n    # Write your solution here\n    return []\n\nif __name__ == "__main__":\n    import sys\n    lines = sys.stdin.read().strip().split("\\n")\n    if len(lines) >= 2:\n        nums = list(map(int, lines[0].split()))\n        target = int(lines[1])\n        res = two_sum(nums, target)\n        print(f"{res[0]} {res[1]}")\n',
            "javascript": 'const readline = require("readline");\n\nfunction twoSum(nums, target) {\n    // Write your solution here\n    // Write your solution here\n    return [];\n}\n\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nlet lines = [];\nrl.on("line", (line) => lines.push(line));\nrl.on("close", () => {\n    if (lines.length >= 2) {\n        const nums = lines[0].trim().split(/\\s+/).map(Number);\n        const target = Number(lines[1].trim());\n        const res = twoSum(nums, target);\n        console.log(`${res[0]} ${res[1]}`);\n    }\n});\n',
            "java": 'import java.util.*;\n\npublic class Solution {\n    public static int[] twoSum(int[] nums, int target) {\n        // Write your solution here\n        return new int[]{};\n    }\n\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (sc.hasNextLine()) {\n            String[] parts = sc.nextLine().trim().split("\\\\s+");\n            int[] nums = new int[parts.length];\n            for (int i = 0; i < parts.length; i++) nums[i] = Integer.parseInt(parts[i]);\n            int target = sc.nextInt();\n            int[] res = twoSum(nums, target);\n            System.out.println(res[0] + " " + res[1]);\n        }\n    }\n}\n',
            "cpp": '#include <iostream>\n#include <vector>\n#include <sstream>\n#include <unordered_map>\n\nusing namespace std;\n\nvector<int> twoSum(vector<int>& nums, int target) {\n    // Write your solution here\n    return {};\n}\n\nint main() {\n    string line;\n    if (getline(cin, line)) {\n        stringstream ss(line);\n        vector<int> nums;\n        int val;\n        while (ss >> val) nums.push_back(val);\n        int target;\n        cin >> target;\n        vector<int> res = twoSum(nums, target);\n        if (res.size() == 2) cout << res[0] << " " << res[1] << endl;\n    }\n    return 0;\n}\n'
        },
        "sample_test_cases": [
            {
                "input": "2 7 11 15\n9",
                "expected_output": "0 1",
                "explanation": "nums[0] + nums[1] == 2 + 7 == 9, so return indices 0 and 1."
            },
            {
                "input": "3 2 4\n6",
                "expected_output": "1 2",
                "explanation": "nums[1] + nums[2] == 2 + 4 == 6, so return indices 1 and 2."
            }
        ],
        "hidden_test_cases": [
            {"input": "3 3\n6", "expected_output": "0 1"},
            {"input": "-1 -2 -3 -4 -5\n-8", "expected_output": "2 4"},
            {"input": "100 200 500 1000\n1500", "expected_output": "2 3"},
            {"input": "0 4 3 0\n0", "expected_output": "0 3"},
            {"input": "1 5 8 12 19 25 33\n45", "expected_output": "3 6"}
        ]
    },
    {
        "title": "Valid Anagram",
        "slug": "valid-anagram",
        "topic": "Strings",
        "difficulty": "easy",
        "company_tags": "Amazon, Bloomberg, Microsoft, Uber",
        "xp_reward": 10,
        "description": "Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.\n\nAn **Anagram** is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
        "input_format": "Line 1: String `s`\nLine 2: String `t`",
        "output_format": "`true` or `false`",
        "constraints": "- 1 <= s.length, t.length <= 5 * 10^4\n- `s` and `t` consist of lowercase English letters.",
        "starter_templates": {
            "python": 'def is_anagram(s, t):\n    # Write your solution here\n    # Write your solution here\n    return False\n\nif __name__ == "__main__":\n    import sys\n    lines = sys.stdin.read().strip().split("\\n")\n    if len(lines) >= 2:\n        s = lines[0].strip()\n        t = lines[1].strip()\n        print("true" if is_anagram(s, t) else "false")\n',
            "javascript": 'const readline = require("readline");\n\nfunction isAnagram(s, t) {\n    // Write your solution here\n    return false;\n}\n\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nlet lines = [];\nrl.on("line", (l) => lines.push(l));\nrl.on("close", () => {\n    if (lines.length >= 2) {\n        console.log(isAnagram(lines[0].trim(), lines[1].trim()) ? "true" : "false");\n    }\n});\n',
            "java": 'import java.util.*;\n\npublic class Solution {\n    public static boolean isAnagram(String s, String t) {\n        // Write your solution here\n        return false;\n    }\n\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (sc.hasNextLine()) {\n            String s = sc.nextLine().trim();\n            String t = sc.nextLine().trim();\n            System.out.println(isAnagram(s, t) ? "true" : "false");\n        }\n    }\n}\n',
            "cpp": '#include <iostream>\n#include <string>\n#include <algorithm>\n\nusing namespace std;\n\nbool isAnagram(string s, string t) {\n    // Write your solution here\n    return false;\n}\n\nint main() {\n    string s, t;\n    if (getline(cin, s) && getline(cin, t)) {\n        cout << (isAnagram(s, t) ? "true" : "false") << endl;\n    }\n    return 0;\n}\n'
        },
        "sample_test_cases": [
            {"input": "anagram\nnagaram", "expected_output": "true", "explanation": "Both strings contain the exact same letter frequencies."},
            {"input": "rat\ncar", "expected_output": "false", "explanation": "The characters do not match."}
        ],
        "hidden_test_cases": [
            {"input": "a\na", "expected_output": "true"},
            {"input": "ab\na", "expected_output": "false"},
            {"input": "listen\nsilent", "expected_output": "true"},
            {"input": "triangle\nintegral", "expected_output": "true"},
            {"input": "aabbcc\nabcabc", "expected_output": "true"},
            {"input": "aabbcc\naabbcd", "expected_output": "false"}
        ]
    },
    {
        "title": "Binary Search",
        "slug": "binary-search",
        "topic": "Binary Search",
        "difficulty": "easy",
        "company_tags": "Apple, Microsoft, Amazon, Google",
        "xp_reward": 10,
        "description": "Given an array of integers `nums` sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its 0-based index. Otherwise, return `-1`.\n\nYou must write an algorithm with `O(log n)` runtime complexity.",
        "input_format": "Line 1: Space-separated sorted integers `nums`\nLine 2: Integer `target`",
        "output_format": "The 0-based index of target in nums, or `-1` if not found.",
        "constraints": "- 1 <= nums.length <= 10^4\n- -10^4 < nums[i], target < 10^4\n- All integers in `nums` are unique and sorted in ascending order.",
        "starter_templates": {
            "python": 'def search(nums, target):\n    # Write your solution here\n    return -1\n\nif __name__ == "__main__":\n    import sys\n    lines = sys.stdin.read().strip().split("\\n")\n    if len(lines) >= 2:\n        nums = list(map(int, lines[0].split()))\n        target = int(lines[1])\n        print(search(nums, target))\n',
            "javascript": 'const readline = require("readline");\n\nfunction search(nums, target) {\n    // Write your solution here\n    return -1;\n}\n\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nlet lines = [];\nrl.on("line", (l) => lines.push(l));\nrl.on("close", () => {\n    if (lines.length >= 2) {\n        const nums = lines[0].trim().split(/\\s+/).map(Number);\n        const target = Number(lines[1].trim());\n        console.log(search(nums, target));\n    }\n});\n',
            "java": 'import java.util.*;\n\npublic class Solution {\n    public static int search(int[] nums, int target) {\n        // Write your solution here\n        return -1;\n    }\n\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (sc.hasNextLine()) {\n            String[] parts = sc.nextLine().trim().split("\\\\s+");\n            int[] nums = new int[parts.length];\n            for (int i = 0; i < parts.length; i++) nums[i] = Integer.parseInt(parts[i]);\n            int target = sc.nextInt();\n            System.out.println(search(nums, target));\n        }\n    }\n}\n',
            "cpp": '#include <iostream>\n#include <vector>\n#include <sstream>\n\nusing namespace std;\n\nint search(vector<int>& nums, int target) {\n    // Write your solution here\n    return -1;\n}\n\nint main() {\n    string line;\n    if (getline(cin, line)) {\n        stringstream ss(line);\n        vector<int> nums;\n        int val;\n        while (ss >> val) nums.push_back(val);\n        int target;\n        cin >> target;\n        cout << search(nums, target) << endl;\n    }\n    return 0;\n}\n'
        },
        "sample_test_cases": [
            {"input": "-1 0 3 5 9 12\n9", "expected_output": "4", "explanation": "9 exists in nums and its index is 4."},
            {"input": "-1 0 3 5 9 12\n2", "expected_output": "-1", "explanation": "2 does not exist in nums so return -1."}
        ],
        "hidden_test_cases": [
            {"input": "5\n5", "expected_output": "0"},
            {"input": "5\n2", "expected_output": "-1"},
            {"input": "1 3 5 7 9 11 13\n1", "expected_output": "0"},
            {"input": "1 3 5 7 9 11 13\n13", "expected_output": "6"},
            {"input": "2 4 6 8 10 12 14 16 18 20\n14", "expected_output": "6"}
        ]
    },
    {
        "title": "Valid Parentheses",
        "slug": "valid-parentheses",
        "topic": "Stack",
        "difficulty": "easy",
        "company_tags": "Meta, Amazon, Microsoft, Bloomberg",
        "xp_reward": 10,
        "description": "Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.",
        "input_format": "Single string `s`",
        "output_format": "`true` or `false`",
        "constraints": "- 1 <= s.length <= 10^4\n- `s` consists of parentheses only `'()[]{}'`.",
        "starter_templates": {
            "python": 'def is_valid(s):\n    # Write your solution here\n    return False\n\nif __name__ == "__main__":\n    import sys\n    s = sys.stdin.read().strip()\n    print("true" if is_valid(s) else "false")\n',
            "javascript": 'const readline = require("readline");\n\nfunction isValid(s) {\n    // Write your solution here\n    return false;\n}\n\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nrl.on("line", (s) => {\n    console.log(isValid(s.trim()) ? "true" : "false");\n});\n',
            "java": 'import java.util.*;\n\npublic class Solution {\n    public static boolean isValid(String s) {\n        Stack<Character> stack = new Stack<>();\n        for (char c : s.toCharArray()) {\n            if (c == \'(\') stack.push(\')\');\n            else if (c == \'{\') stack.push(\'}\');\n            else if (c == \'[\') stack.push(\']\');\n            else if (stack.isEmpty() || stack.pop() != c) return false;\n        }\n        return stack.isEmpty();\n    }\n\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (sc.hasNextLine()) {\n            String s = sc.nextLine().trim();\n            System.out.println(isValid(s) ? "true" : "false");\n        }\n    }\n}\n',
            "cpp": '#include <iostream>\n#include <stack>\n#include <string>\n#include <unordered_map>\n\nusing namespace std;\n\nbool isValid(string s) {\n    stack<char> st;\n    unordered_map<char, char> m = {{\')\', \'(\'}, {\'}\', \'{\'}, {\']\', \'[\'}};\n    for (char c : s) {\n        if (m.count(c)) {\n            if (st.empty() || st.top() != m[c]) return false;\n            st.pop();\n        } else {\n            st.push(c);\n        }\n    }\n    return st.empty();\n}\n\nint main() {\n    string s;\n    if (cin >> s) {\n        cout << (isValid(s) ? "true" : "false") << endl;\n    }\n    return 0;\n}\n'
        },
        "sample_test_cases": [
            {"input": "()", "expected_output": "true", "explanation": "Simple matched open and close parenthesis."},
            {"input": "()[]{}", "expected_output": "true", "explanation": "All pairs matched sequentially."},
            {"input": "(]", "expected_output": "false", "explanation": "Mismatched bracket types."}
        ],
        "hidden_test_cases": [
            {"input": "([])", "expected_output": "true"},
            {"input": "([)]", "expected_output": "false"},
            {"input": "{[]}", "expected_output": "true"},
            {"input": "(((", "expected_output": "false"},
            {"input": ")))", "expected_output": "false"},
            {"input": "{[()]}", "expected_output": "true"}
        ]
    },
    {
        "title": "Reverse Linked List",
        "slug": "reverse-linked-list",
        "topic": "Linked Lists",
        "difficulty": "easy",
        "company_tags": "Amazon, Microsoft, Apple, Google, Adobe",
        "xp_reward": 10,
        "description": "Given the values of a singly linked list represented as space-separated integers, reverse the list, and return the reversed list values.",
        "input_format": "Single line with space-separated integers representing the linked list values.",
        "output_format": "Space-separated integers of the reversed list.",
        "constraints": "- The number of nodes in the list is in the range [0, 5000].\n- -5000 <= Node.val <= 5000",
        "starter_templates": {
            "python": 'def reverse_list(values):\n    # Write your solution here\n    return []\n\nif __name__ == "__main__":\n    import sys\n    inp = sys.stdin.read().strip()\n    if inp:\n        nums = list(map(int, inp.split()))\n        res = reverse_list(nums)\n        print(" ".join(map(str, res)))\n    else:\n        print("")\n',
            "javascript": 'const readline = require("readline");\n\nfunction reverseList(nums) {\n    // Write your solution here\n    return [];\n}\n\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nlet inp = "";\nrl.on("line", (l) => inp += l + " ");\nrl.on("close", () => {\n    const trimmed = inp.trim();\n    if (trimmed) {\n        const nums = trimmed.split(/\\s+/).map(Number);\n        console.log(reverseList(nums).join(" "));\n    } else {\n        console.log("");\n    }\n});\n',
            "java": 'import java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (sc.hasNextLine()) {\n            String line = sc.nextLine().trim();\n            if (line.isEmpty()) return;\n            String[] parts = line.split("\\\\s+");\n            List<String> list = Arrays.asList(parts);\n            // Write your solution here\n            // reverse nodes or list\n            System.out.println(String.join(" ", list));\n        }\n    }\n}\n',
            "cpp": '#include <iostream>\n#include <vector>\n#include <sstream>\n#include <algorithm>\n\nusing namespace std;\n\nint main() {\n    string line;\n    if (getline(cin, line) && !line.empty()) {\n        stringstream ss(line);\n        vector<int> nums;\n        int val;\n        while (ss >> val) nums.push_back(val);\n        // Write your solution here\n        for (size_t i = 0; i < nums.size(); i++) {\n            cout << nums[i] << (i + 1 == nums.size() ? "" : " ");\n        }\n        cout << endl;\n    }\n    return 0;\n}\n'
        },
        "sample_test_cases": [
            {"input": "1 2 3 4 5", "expected_output": "5 4 3 2 1", "explanation": "List 1->2->3->4->5 reversed is 5->4->3->2->1."},
            {"input": "1 2", "expected_output": "2 1", "explanation": "List 1->2 reversed is 2->1."}
        ],
        "hidden_test_cases": [
            {"input": "42", "expected_output": "42"},
            {"input": "10 20 30", "expected_output": "30 20 10"},
            {"input": "1 -2 3 -4 5", "expected_output": "5 -4 3 -2 1"},
            {"input": "7 7 7 7", "expected_output": "7 7 7 7"}
        ]
    },

    # ==================== MEDIUM PROBLEMS ====================
    {
        "title": "Search in Rotated Sorted Array",
        "slug": "search-in-rotated-sorted-array",
        "topic": "Binary Search",
        "difficulty": "medium",
        "company_tags": "Amazon, Microsoft, Meta, Google, LinkedIn",
        "xp_reward": 20,
        "description": "There is an integer array `nums` sorted in ascending order (with distinct values).\n\nPrior to being passed to your function, `nums` is possibly rotated at an unknown pivot index `k` (1 <= k < nums.length).\n\nGiven the array `nums` after the possible rotation and an integer `target`, return the 0-based index of `target` if it is in `nums`, or `-1` if it is not in `nums`.\n\nYou must write an algorithm with `O(log n)` runtime complexity.",
        "input_format": "Line 1: Space-separated integers `nums`\nLine 2: Integer `target`",
        "output_format": "Index of target or `-1`.",
        "constraints": "- 1 <= nums.length <= 5000\n- -10^4 <= nums[i] <= 10^4\n- All values of `nums` are unique.",
        "starter_templates": {
            "python": 'def search_rotated(nums, target):\n    # Write your solution here\n    return -1\n\nif __name__ == "__main__":\n    import sys\n    lines = sys.stdin.read().strip().split("\\n")\n    if len(lines) >= 2:\n        nums = list(map(int, lines[0].split()))\n        target = int(lines[1])\n        print(search_rotated(nums, target))\n',
            "javascript": 'const readline = require("readline");\n\nfunction search(nums, target) {\n    // Write your solution here\n    return -1;\n}\n\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nlet lines = [];\nrl.on("line", (l) => lines.push(l));\nrl.on("close", () => {\n    if (lines.length >= 2) {\n        const nums = lines[0].trim().split(/\\s+/).map(Number);\n        const target = Number(lines[1].trim());\n        console.log(search(nums, target));\n    }\n});\n',
            "java": 'import java.util.*;\n\npublic class Solution {\n    public static int search(int[] nums, int target) {\n        // Write your solution here\n        return -1;\n    }\n\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (sc.hasNextLine()) {\n            String[] parts = sc.nextLine().trim().split("\\\\s+");\n            int[] nums = new int[parts.length];\n            for (int i = 0; i < parts.length; i++) nums[i] = Integer.parseInt(parts[i]);\n            int target = sc.nextInt();\n            System.out.println(search(nums, target));\n        }\n    }\n}\n',
            "cpp": '#include <iostream>\n#include <vector>\n#include <sstream>\n\nusing namespace std;\n\nint search(vector<int>& nums, int target) {\n    // Write your solution here\n    return -1;\n}\n\nint main() {\n    string line;\n    if (getline(cin, line)) {\n        stringstream ss(line);\n        vector<int> nums;\n        int val;\n        while (ss >> val) nums.push_back(val);\n        int target;\n        cin >> target;\n        cout << search(nums, target) << endl;\n    }\n    return 0;\n}\n'
        },
        "sample_test_cases": [
            {"input": "4 5 6 7 0 1 2\n0", "expected_output": "4", "explanation": "Target 0 is found at index 4."},
            {"input": "4 5 6 7 0 1 2\n3", "expected_output": "-1", "explanation": "Target 3 is not present in nums."}
        ],
        "hidden_test_cases": [
            {"input": "1\n0", "expected_output": "-1"},
            {"input": "1\n1", "expected_output": "0"},
            {"input": "3 1\n1", "expected_output": "1"},
            {"input": "5 1 3\n5", "expected_output": "0"},
            {"input": "8 9 2 3 4\n9", "expected_output": "1"}
        ]
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "slug": "longest-substring-without-repeating-characters",
        "topic": "Strings",
        "difficulty": "medium",
        "company_tags": "Amazon, Microsoft, Meta, Bloomberg, Adobe",
        "xp_reward": 20,
        "description": "Given a string `s`, find the length of the longest substring without duplicate characters.",
        "input_format": "Single line string `s`",
        "output_format": "Integer representing the maximum length.",
        "constraints": "- 0 <= s.length <= 5 * 10^4\n- `s` consists of English letters, digits, symbols and spaces.",
        "starter_templates": {
            "python": 'def length_of_longest_substring(s):\n    # Write your solution here\n    return 0\n\nif __name__ == "__main__":\n    import sys\n    s = sys.stdin.read().rstrip("\\r\\n")\n    print(length_of_longest_substring(s))\n',
            "javascript": 'const readline = require("readline");\n\nfunction lengthOfLongestSubstring(s) {\n    // Write your solution here\n    return 0;\n}\n\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nlet input = "";\nrl.on("line", (l) => input = l);\nrl.on("close", () => console.log(lengthOfLongestSubstring(input)));\n',
            "java": 'import java.util.*;\n\npublic class Solution {\n    public static int lengthOfLongestSubstring(String s) {\n        // Write your solution here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.hasNextLine() ? sc.nextLine() : "";\n        System.out.println(lengthOfLongestSubstring(s));\n    }\n}\n',
            "cpp": '#include <iostream>\n#include <string>\n#include <unordered_map>\n#include <algorithm>\n\nusing namespace std;\n\nint lengthOfLongestSubstring(string s) {\n    // Write your solution here\n    return 0;\n}\n\nint main() {\n    string s;\n    getline(cin, s);\n    cout << lengthOfLongestSubstring(s) << endl;\n    return 0;\n}\n'
        },
        "sample_test_cases": [
            {"input": "abcabcbb", "expected_output": "3", "explanation": "The answer is 'abc', with the length of 3."},
            {"input": "bbbbb", "expected_output": "1", "explanation": "The answer is 'b', with the length of 1."},
            {"input": "pwwkew", "expected_output": "3", "explanation": "The answer is 'wke', with the length of 3."}
        ],
        "hidden_test_cases": [
            {"input": "", "expected_output": "0"},
            {"input": " ", "expected_output": "1"},
            {"input": "au", "expected_output": "2"},
            {"input": "dvdf", "expected_output": "3"},
            {"input": "tmmzuxt", "expected_output": "5"}
        ]
    },
    {
        "title": "3Sum",
        "slug": "3sum",
        "topic": "Two Pointers",
        "difficulty": "medium",
        "company_tags": "Meta, Amazon, Microsoft, Apple, Google",
        "xp_reward": 20,
        "description": "Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.\n\nNotice that the solution set must not contain duplicate triplets. Print each triplet on a new line with elements separated by space, sorted.",
        "input_format": "Single line of space-separated integers `nums`.",
        "output_format": "Number of unique triplets on Line 1, followed by sorted triplets.",
        "constraints": "- 3 <= nums.length <= 3000\n- -10^5 <= nums[i] <= 10^5",
        "starter_templates": {
            "python": 'def three_sum(nums):\n    # Write your solution here\n    return []\n\nif __name__ == "__main__":\n    import sys\n    inp = sys.stdin.read().strip()\n    if inp:\n        nums = list(map(int, inp.split()))\n        res = three_sum(nums)\n        print(len(res))\n        for triplet in res:\n            print(f"{triplet[0]} {triplet[1]} {triplet[2]}")\n    else:\n        print(0)\n',
            "javascript": 'const readline = require("readline");\n\nfunction threeSum(nums) {\n    // Write your solution here\n    return [];\n}\n\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nrl.on("line", (line) => {\n    const nums = line.trim().split(/\\s+/).map(Number);\n    const res = threeSum(nums);\n    console.log(res.length);\n    res.forEach(t => console.log(`${t[0]} ${t[1]} ${t[2]}`));\n});\n',
            "java": 'import java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (sc.hasNextLine()) {\n            String[] parts = sc.nextLine().trim().split("\\\\s+");\n            int[] nums = new int[parts.length];\n            for (int i = 0; i < parts.length; i++) nums[i] = Integer.parseInt(parts[i]);\n            Arrays.sort(nums);\n            // Write your solution here\n            List<List<Integer>> res = new ArrayList<>();\n            System.out.println(res.size());\n        }\n    }\n}\n',
            "cpp": '#include <iostream>\n#include <vector>\n#include <sstream>\n#include <algorithm>\n\nusing namespace std;\n\nint main() {\n    string line;\n    if (getline(cin, line)) {\n        stringstream ss(line);\n        vector<int> nums;\n        int val;\n        while (ss >> val) nums.push_back(val);\n        sort(nums.begin(), nums.end());\n        // Write your solution here\n        vector<vector<int>> res;\n        cout << res.size() << endl;\n    }\n    return 0;\n}\n'
        },
        "sample_test_cases": [
            {"input": "-1 0 1 2 -1 -4", "expected_output": "2\n-1 -1 2\n-1 0 1", "explanation": "Triplets summing to 0 are [-1, -1, 2] and [-1, 0, 1]."},
            {"input": "0 1 1", "expected_output": "0", "explanation": "No possible triplet sum equals 0."}
        ],
        "hidden_test_cases": [
            {"input": "0 0 0", "expected_output": "1\n0 0 0"},
            {"input": "-2 0 1 1 2", "expected_output": "2\n-2 0 2\n-2 1 1"},
            {"input": "-4 -2 -2 -2 0 1 2 2 2 3 3 4 4 6 6", "expected_output": "6\n-4 -2 6\n-4 0 4\n-4 1 3\n-4 2 2\n-2 -2 4\n-2 0 2"}
        ]
    },
    {
        "title": "Merge Intervals",
        "slug": "merge-intervals",
        "topic": "Arrays",
        "difficulty": "medium",
        "company_tags": "Google, Amazon, Microsoft, Meta, Bloomberg",
        "xp_reward": 20,
        "description": "Given an array of intervals where each interval is represented by two integers `[start, end]`, merge all overlapping intervals, and output the merged intervals.",
        "input_format": "Line 1: Number of intervals `N`.\nNext N lines: Two space-separated integers `start end`.",
        "output_format": "Merged intervals formatted as `start end` per line.",
        "constraints": "- 1 <= intervals.length <= 10^4\n- 0 <= start_i <= end_i <= 10^4",
        "starter_templates": {
            "python": 'def merge_intervals(intervals):\n    # Write your solution here\n    return []\n\nif __name__ == "__main__":\n    import sys\n    lines = sys.stdin.read().strip().split("\\n")\n    if lines and lines[0]:\n        n = int(lines[0].strip())\n        intervals = []\n        for i in range(1, n + 1):\n            if i < len(lines):\n                parts = list(map(int, lines[i].split()))\n                intervals.append(parts)\n        res = merge_intervals(intervals)\n        for start, end in res:\n            print(f"{start} {end}")\n',
            "javascript": 'const readline = require("readline");\n\nfunction merge(intervals) {\n    // Write your solution here\n    return [];\n}\n\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nlet lines = [];\nrl.on("line", (l) => lines.push(l));\nrl.on("close", () => {\n    if (lines.length) {\n        const n = parseInt(lines[0]);\n        const intervals = [];\n        for (let i = 1; i <= n && i < lines.length; i++) {\n            intervals.push(lines[i].trim().split(/\\s+/).map(Number));\n        }\n        const res = merge(intervals);\n        res.forEach(iv => console.log(`${iv[0]} ${iv[1]}`));\n    }\n});\n',
            "java": 'import java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (sc.hasNextInt()) {\n            int n = sc.nextInt();\n            int[][] intervals = new int[n][2];\n            for (int i = 0; i < n; i++) {\n                intervals[i][0] = sc.nextInt();\n                intervals[i][1] = sc.nextInt();\n            }\n            // Write your solution here\n            List<int[]> merged = new ArrayList<>();\n        }\n    }\n}\n',
            "cpp": '#include <iostream>\n#include <vector>\n#include <algorithm>\n\nusing namespace std;\n\nint main() {\n    int n;\n    if (cin >> n) {\n        vector<pair<int, int>> intervals(n);\n        for (int i = 0; i < n; i++) cin >> intervals[i].first >> intervals[i].second;\n        // Write your solution here\n        vector<pair<int, int>> merged;\n    }\n    return 0;\n}\n'
        },
        "sample_test_cases": [
            {"input": "4\n1 3\n2 6\n8 10\n15 18", "expected_output": "1 6\n8 10\n15 18", "explanation": "Intervals [1,3] and [2,6] overlap into [1,6]."},
            {"input": "2\n1 4\n4 5", "expected_output": "1 5", "explanation": "Intervals [1,4] and [4,5] are contiguous and merged into [1,5]."}
        ],
        "hidden_test_cases": [
            {"input": "1\n1 4", "expected_output": "1 4"},
            {"input": "3\n1 4\n2 3\n5 8", "expected_output": "1 4\n5 8"},
            {"input": "4\n1 10\n2 3\n4 5\n6 7", "expected_output": "1 10"}
        ]
    },
    {
        "title": "Number of Islands",
        "slug": "number-of-islands",
        "topic": "Graphs",
        "difficulty": "medium",
        "company_tags": "Amazon, Microsoft, Google, Bloomberg, Meta",
        "xp_reward": 20,
        "description": "Given an `m x n` 2D binary grid which represents a map of `'1'`s (land) and `'0'`s (water), return the number of islands.\n\nAn island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.",
        "input_format": "Line 1: Two integers `m n` (dimensions)\nNext m lines: `n` characters (space or continuous 1s and 0s)",
        "output_format": "Total number of islands.",
        "constraints": "- m == grid.length\n- n == grid[i].length\n- 1 <= m, n <= 300\n- grid[i][j] is '0' or '1'.",
        "starter_templates": {
            "python": 'def num_islands(grid):\n    # Write your solution here\n    return 0\n\nif __name__ == "__main__":\n    import sys\n    lines = sys.stdin.read().strip().split("\\n")\n    if lines and lines[0]:\n        parts = lines[0].split()\n        m, n = int(parts[0]), int(parts[1])\n        grid = []\n        for i in range(1, m + 1):\n            if i < len(lines):\n                grid.append(lines[i].split() if " " in lines[i] else list(lines[i]))\n        print(num_islands(grid))\n',
            "javascript": 'const readline = require("readline");\n\nfunction numIslands(grid) {\n    // Write your solution here\n    return 0;\n}\n\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nlet lines = [];\nrl.on("line", (l) => lines.push(l));\nrl.on("close", () => {\n    if (lines.length) {\n        const [m, n] = lines[0].trim().split(/\\s+/).map(Number);\n        const grid = [];\n        for (let i = 1; i <= m && i < lines.length; i++) {\n            const row = lines[i].includes(" ") ? lines[i].trim().split(/\\s+/) : lines[i].trim().split("");\n            grid.push(row);\n        }\n        console.log(numIslands(grid));\n    }\n});\n',
            "java": 'import java.util.*;\n\npublic class Solution {\n    public static void dfs(char[][] grid, int r, int c) {\n        if (r < 0 || r >= grid.length || c < 0 || c >= grid[0].length || grid[r][c] != \'1\') return;\n        grid[r][c] = \'0\';\n        dfs(grid, r+1, c);\n        dfs(grid, r-1, c);\n        dfs(grid, r, c+1);\n        dfs(grid, r, c-1);\n    }\n\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (sc.hasNextInt()) {\n            int m = sc.nextInt();\n            int n = sc.nextInt();\n            char[][] grid = new char[m][n];\n            for (int i = 0; i < m; i++) {\n                String row = sc.next();\n                grid[i] = row.toCharArray();\n            }\n            int count = 0;\n            for (int r = 0; r < m; r++) {\n                for (int c = 0; c < n; c++) {\n                    if (grid[r][c] == \'1\') {\n                        dfs(grid, r, c);\n                        count++;\n                    }\n                }\n            }\n            System.out.println(count);\n        }\n    }\n}\n',
            "cpp": '#include <iostream>\n#include <vector>\n#include <string>\n\nusing namespace std;\n\nvoid dfs(vector<vector<char>>& grid, int r, int c) {\n    if (r < 0 || r >= grid.size() || c < 0 || c >= grid[0].size() || grid[r][c] != \'1\') return;\n    grid[r][c] = \'0\';\n    dfs(grid, r + 1, c);\n    dfs(grid, r - 1, c);\n    dfs(grid, r, c + 1);\n    dfs(grid, r, c - 1);\n}\n\nint main() {\n    int m, n;\n    if (cin >> m >> n) {\n        vector<vector<char>> grid(m, vector<char>(n));\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) cin >> grid[i][j];\n        }\n        int count = 0;\n        for (int i = 0; i < m; i++) {\n            for (int j = 0; j < n; j++) {\n                if (grid[i][j] == \'1\') {\n                    dfs(grid, i, j);\n                    count++;\n                }\n            }\n        }\n        cout << count << endl;\n    }\n    return 0;\n}\n'
        },
        "sample_test_cases": [
            {"input": "4 5\n1 1 1 1 0\n1 1 0 1 0\n1 1 0 0 0\n0 0 0 0 0", "expected_output": "1", "explanation": "All 1s are connected horizontally and vertically forming 1 island."},
            {"input": "4 5\n1 1 0 0 0\n1 1 0 0 0\n0 0 1 0 0\n0 0 0 1 1", "expected_output": "3", "explanation": "There are 3 separate islands."}
        ],
        "hidden_test_cases": [
            {"input": "1 1\n1", "expected_output": "1"},
            {"input": "1 1\n0", "expected_output": "0"},
            {"input": "3 3\n1 0 1\n0 1 0\n1 0 1", "expected_output": "5"}
        ]
    },

    # ==================== HARD PROBLEMS ====================
    {
        "title": "Trapping Rain Water",
        "slug": "trapping-rain-water",
        "topic": "Two Pointers",
        "difficulty": "hard",
        "company_tags": "Amazon, Google, Microsoft, Goldman Sachs, Meta",
        "xp_reward": 40,
        "description": "Given `n` non-negative integers representing an elevation map where the width of each bar is `1`, compute how much water it can trap after raining.",
        "input_format": "Single line of space-separated integers representing heights.",
        "output_format": "Total units of trapped rain water.",
        "constraints": "- n == height.length\n- 1 <= n <= 2 * 10^4\n- 0 <= height[i] <= 10^5",
        "starter_templates": {
            "python": 'def trap(height):\n    # Write your solution here\n    return 0\n\nif __name__ == "__main__":\n    import sys\n    inp = sys.stdin.read().strip()\n    if inp:\n        heights = list(map(int, inp.split()))\n        print(trap(heights))\n    else:\n        print(0)\n',
            "javascript": 'const readline = require("readline");\n\nfunction trap(height) {\n    // Write your solution here\n    return 0;\n}\n\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nrl.on("line", (l) => {\n    const h = l.trim().split(/\\s+/).map(Number);\n    console.log(trap(h));\n});\n',
            "java": 'import java.util.*;\n\npublic class Solution {\n    public static int trap(int[] height) {\n        // Write your solution here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (sc.hasNextLine()) {\n            String[] parts = sc.nextLine().trim().split("\\\\s+");\n            int[] h = new int[parts.length];\n            for (int i = 0; i < parts.length; i++) h[i] = Integer.parseInt(parts[i]);\n            System.out.println(trap(h));\n        }\n    }\n}\n',
            "cpp": '#include <iostream>\n#include <vector>\n#include <sstream>\n#include <algorithm>\n\nusing namespace std;\n\nint trap(vector<int>& height) {\n    // Write your solution here\n    return 0;\n}\n\nint main() {\n    string line;\n    if (getline(cin, line)) {\n        stringstream ss(line);\n        vector<int> h;\n        int val;\n        while (ss >> val) h.push_back(val);\n        cout << trap(h) << endl;\n    }\n    return 0;\n}\n'
        },
        "sample_test_cases": [
            {"input": "0 1 0 2 1 0 1 3 2 1 2 1", "expected_output": "6", "explanation": "6 units of rain water are trapped."},
            {"input": "4 2 0 3 2 5", "expected_output": "9", "explanation": "9 units of rain water are trapped."}
        ],
        "hidden_test_cases": [
            {"input": "1 2 3 4 5", "expected_output": "0"},
            {"input": "5 4 3 2 1", "expected_output": "0"},
            {"input": "3 0 2 0 4", "expected_output": "7"},
            {"input": "2 0 2", "expected_output": "2"}
        ]
    },
    {
        "title": "Edit Distance",
        "slug": "edit-distance",
        "topic": "Dynamic Programming",
        "difficulty": "hard",
        "company_tags": "Google, Amazon, Microsoft, Adobe",
        "xp_reward": 40,
        "description": "Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`.\n\nYou have the following three operations permitted on a word:\n1. Insert a character\n2. Delete a character\n3. Replace a character",
        "input_format": "Line 1: String `word1`\nLine 2: String `word2`",
        "output_format": "Minimum operations required.",
        "constraints": "- 0 <= word1.length, word2.length <= 500\n- `word1` and `word2` consist of lowercase English letters.",
        "starter_templates": {
            "python": 'def min_distance(word1, word2):\n    # Write your solution here\n    return 0\n\nif __name__ == "__main__":\n    import sys\n    lines = sys.stdin.read().split("\\n")\n    w1 = lines[0].strip() if len(lines) > 0 else ""\n    w2 = lines[1].strip() if len(lines) > 1 else ""\n    print(min_distance(w1, w2))\n',
            "javascript": 'const readline = require("readline");\n\nfunction minDistance(word1, word2) {\n    // Write your solution here\n    return 0;\n}\n\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nlet lines = [];\nrl.on("line", (l) => lines.push(l));\nrl.on("close", () => {\n    const w1 = lines[0] ? lines[0].trim() : "";\n    const w2 = lines[1] ? lines[1].trim() : "";\n    console.log(minDistance(w1, w2));\n});\n',
            "java": 'import java.util.*;\n\npublic class Solution {\n    public static int minDistance(String word1, String word2) {\n        // Write your solution here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String w1 = sc.hasNextLine() ? sc.nextLine().trim() : "";\n        String w2 = sc.hasNextLine() ? sc.nextLine().trim() : "";\n        System.out.println(minDistance(w1, w2));\n    }\n}\n',
            "cpp": '#include <iostream>\n#include <string>\n#include <vector>\n#include <algorithm>\n\nusing namespace std;\n\nint minDistance(string word1, string word2) {\n    // Write your solution here\n    return 0;\n}\n\nint main() {\n    string w1, w2;\n    getline(cin, w1);\n    getline(cin, w2);\n    cout << minDistance(w1, w2) << endl;\n    return 0;\n}\n'
        },
        "sample_test_cases": [
            {"input": "horse\nros", "expected_output": "3", "explanation": "horse -> rorse (replace 'h' with 'r') -> rose (remove 'r') -> ros (remove 'e')"},
            {"input": "intention\nexecution", "expected_output": "5", "explanation": "5 edits required."}
        ],
        "hidden_test_cases": [
            {"input": "a\nb", "expected_output": "1"},
            {"input": "\na", "expected_output": "1"},
            {"input": "abc\nabc", "expected_output": "0"},
            {"input": "zoologico\nzoology", "expected_output": "3"}
        ]
    },
    {
        "title": "Longest Valid Parentheses",
        "slug": "longest-valid-parentheses",
        "topic": "Stack",
        "difficulty": "hard",
        "company_tags": "Google, Amazon, Microsoft, Meta",
        "xp_reward": 40,
        "description": "Given a string containing just the characters `'('` and `')'`, return the length of the longest valid (well-formed) parentheses substring.",
        "input_format": "Single string `s`",
        "output_format": "Length of the longest valid parentheses substring.",
        "constraints": "- 0 <= s.length <= 3 * 10^4\n- `s[i]` is `'('` or `')'`.",
        "starter_templates": {
            "python": 'def longest_valid_parentheses(s):\n    # Write your solution here\n    return 0\n\nif __name__ == "__main__":\n    import sys\n    s = sys.stdin.read().strip()\n    print(longest_valid_parentheses(s))\n',
            "javascript": 'const readline = require("readline");\n\nfunction longestValidParentheses(s) {\n    // Write your solution here\n    return 0;\n}\n\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nlet inp = "";\nrl.on("line", (l) => inp = l.trim());\nrl.on("close", () => console.log(longestValidParentheses(inp)));\n',
            "java": 'import java.util.*;\n\npublic class Solution {\n    public static int longestValidParentheses(String s) {\n        Stack<Integer> stack = new Stack<>();\n        stack.push(-1);\n        int maxLen = 0;\n        for (int i = 0; i < s.length(); i++) {\n            if (s.charAt(i) == \'(\') stack.push(i);\n            else {\n                stack.pop();\n                if (stack.isEmpty()) stack.push(i);\n                else maxLen = Math.max(maxLen, i - stack.peek());\n            }\n        }\n        return maxLen;\n    }\n\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.hasNextLine() ? sc.nextLine().trim() : "";\n        System.out.println(longestValidParentheses(s));\n    }\n}\n',
            "cpp": '#include <iostream>\n#include <stack>\n#include <string>\n#include <algorithm>\n\nusing namespace std;\n\nint longestValidParentheses(string s) {\n    stack<int> st;\n    st.push(-1);\n    int maxLen = 0;\n    for (int i = 0; i < s.length(); i++) {\n        if (s[i] == \'(\') st.push(i);\n        else {\n            st.pop();\n            if (st.empty()) st.push(i);\n            else maxLen = max(maxLen, i - st.top());\n        }\n    }\n    return maxLen;\n}\n\nint main() {\n    string s;\n    if (cin >> s) cout << longestValidParentheses(s) << endl;\n    else cout << 0 << endl;\n    return 0;\n}\n'
        },
        "sample_test_cases": [
            {"input": "(()", "expected_output": "2", "explanation": "The longest valid parentheses substring is '()' with length 2."},
            {"input": ")()())", "expected_output": "4", "explanation": "The longest valid parentheses substring is '()()' with length 4."}
        ],
        "hidden_test_cases": [
            {"input": "", "expected_output": "0"},
            {"input": "()(()", "expected_output": "2"},
            {"input": "(()())", "expected_output": "6"},
            {"input": "()(())", "expected_output": "6"}
        ]
    },
    {
        "title": "Search in Rotated Sorted Array",
        "slug": "search-in-rotated-sorted-array",
        "topic": "Binary Search",
        "difficulty": "medium",
        "company_tags": "Google, Amazon, Microsoft, Facebook",
        "xp_reward": 20,
        "description": "Given a sorted integer array `nums` rotated at an unknown pivot index, and a `target`, return the 0-based index of `target` if it is in `nums`, or `-1` if it is not in `nums`.\n\nYou must write an algorithm with `O(log n)` runtime complexity.",
        "input_format": "Line 1: Space-separated integers representing the rotated array `nums`.\nLine 2: Single integer `target`.",
        "output_format": "Single integer representing the index, or `-1`.",
        "constraints": "- 1 <= nums.length <= 5000\n- -10^4 <= nums[i] <= 10^4\n- All values of `nums` are unique.\n- -10^4 <= target <= 10^4",
        "starter_templates": {
            "python": 'def search(nums, target):\n    # Write your solution here\n    return -1\n\nif __name__ == "__main__":\n    import sys\n    lines = sys.stdin.read().strip().split("\\n")\n    if len(lines) >= 2:\n        nums = list(map(int, lines[0].split()))\n        target = int(lines[1])\n        print(search(nums, target))\n',
            "javascript": 'const readline = require("readline");\n\nfunction search(nums, target) {\n    // Write your solution here\n    return -1;\n}\n\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nlet lines = [];\nrl.on("line", (l) => lines.push(l));\nrl.on("close", () => {\n    if (lines.length >= 2) {\n        const nums = lines[0].trim().split(/\\s+/).map(Number);\n        const target = Number(lines[1].trim());\n        console.log(search(nums, target));\n    }\n});\n',
            "java": 'import java.util.*;\n\npublic class Solution {\n    public static int search(int[] nums, int target) {\n        // Write your solution here\n        return -1;\n    }\n\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (sc.hasNextLine()) {\n            String[] parts = sc.nextLine().trim().split("\\\\s+");\n            int[] nums = new int[parts.length];\n            for (int i = 0; i < parts.length; i++) nums[i] = Integer.parseInt(parts[i]);\n            int target = sc.nextInt();\n            System.out.println(search(nums, target));\n        }\n    }\n}\n',
            "cpp": '#include <iostream>\n#include <vector>\n#include <sstream>\n\nusing namespace std;\n\nint search(vector<int>& nums, int target) {\n    // Write your solution here\n    return -1;\n}\n\nint main() {\n    string line;\n    if (getline(cin, line)) {\n        stringstream ss(line);\n        vector<int> nums;\n        int val;\n        while (ss >> val) nums.push_back(val);\n        int target;\n        cin >> target;\n        cout << search(nums, target) << endl;\n    }\n    return 0;\n}\n'
        },
        "sample_test_cases": [
            {"input": "4 5 6 7 0 1 2\n0", "expected_output": "4", "explanation": "0 is found at index 4."},
            {"input": "4 5 6 7 0 1 2\n3", "expected_output": "-1", "explanation": "3 is not in the array."}
        ],
        "hidden_test_cases": [
            {"input": "1\n0", "expected_output": "-1"},
            {"input": "1 3\n3", "expected_output": "1"},
            {"input": "3 1\n1", "expected_output": "1"},
            {"input": "5 1 3\n5", "expected_output": "0"}
        ]
    },
    {
        "title": "Single Number",
        "slug": "single-number",
        "topic": "Arrays",
        "difficulty": "easy",
        "company_tags": "Amazon, Bloomberg, Meta",
        "xp_reward": 10,
        "description": "Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one.\n\nYou must implement a solution with a linear runtime complexity and use only constant extra space.",
        "input_format": "Line 1: Space-separated integers representing the array `nums`.",
        "output_format": "The single integer.",
        "constraints": "- 1 <= nums.length <= 3 * 10^4\n- -3 * 10^4 <= nums[i] <= 3 * 10^4\n- Each element in the array appears twice except for one element.",
        "starter_templates": {
            "python": 'def single_number(nums):\n    # Write your solution here\n    return -1\n\nif __name__ == "__main__":\n    import sys\n    line = sys.stdin.read().strip()\n    if line:\n        nums = list(map(int, line.split()))\n        print(single_number(nums))\n',
            "javascript": 'const readline = require("readline");\n\nfunction singleNumber(nums) {\n    // Write your solution here\n    return -1;\n}\n\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nlet inp = "";\nrl.on("line", (l) => inp = l.trim());\nrl.on("close", () => {\n    if (inp) {\n        console.log(singleNumber(inp.split(/\\s+/).map(Number)));\n    }\n});\n',
            "java": 'import java.util.*;\n\npublic class Solution {\n    public static int singleNumber(int[] nums) {\n        // Write your solution here\n        return -1;\n    }\n\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (sc.hasNextLine()) {\n            String[] parts = sc.nextLine().trim().split("\\\\s+");\n            int[] nums = new int[parts.length];\n            for (int i = 0; i < parts.length; i++) nums[i] = Integer.parseInt(parts[i]);\n            System.out.println(singleNumber(nums));\n        }\n    }\n}\n',
            "cpp": '#include <iostream>\n#include <vector>\n#include <sstream>\n\nusing namespace std;\n\nint singleNumber(vector<int>& nums) {\n    // Write your solution here\n    return -1;\n}\n\nint main() {\n    string line;\n    if (getline(cin, line)) {\n        stringstream ss(line);\n        vector<int> nums;\n        int val;\n        while (ss >> val) nums.push_back(val);\n        cout << singleNumber(nums) << endl;\n    }\n    return 0;\n}\n'
        },
        "sample_test_cases": [
            {"input": "2 2 1", "expected_output": "1", "explanation": "1 appears once, others twice."},
            {"input": "4 1 2 1 2", "expected_output": "4", "explanation": "4 appears once, others twice."}
        ],
        "hidden_test_cases": [
            {"input": "1", "expected_output": "1"},
            {"input": "-1 -1 -2", "expected_output": "-2"},
            {"input": "100 200 100", "expected_output": "200"},
            {"input": "9 9 10 10 11 12 11", "expected_output": "12"}
        ]
    },
    {
        "title": "Container With Most Water",
        "slug": "container-with-most-water",
        "topic": "Arrays",
        "difficulty": "medium",
        "company_tags": "Google, Apple, Meta, Amazon",
        "xp_reward": 25,
        "description": "Given `n` non-negative integers `height` representing the height of vertical lines, find two lines that together with the x-axis forms a container, such that the container contains the most water. Return the maximum area of water.",
        "input_format": "Line 1: Space-separated integers representing the `height` array.",
        "output_format": "Single integer representing the maximum area.",
        "constraints": "- n == height.length\n- 2 <= n <= 10^5\n- 0 <= height[i] <= 10^4",
        "starter_templates": {
            "python": 'def max_area(height):\n    # Write your solution here\n    return 0\n\nif __name__ == "__main__":\n    import sys\n    line = sys.stdin.read().strip()\n    if line:\n        height = list(map(int, line.split()))\n        print(max_area(height))\n',
            "javascript": 'const readline = require("readline");\n\nfunction maxArea(height) {\n    // Write your solution here\n    return 0;\n}\n\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nlet inp = "";\nrl.on("line", (l) => inp = l.trim());\nrl.on("close", () => {\n    if (inp) {\n        console.log(maxArea(inp.split(/\\s+/).map(Number)));\n    }\n});\n',
            "java": 'import java.util.*;\n\npublic class Solution {\n    public static int maxArea(int[] height) {\n        // Write your solution here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (sc.hasNextLine()) {\n            String[] parts = sc.nextLine().trim().split("\\\\s+");\n            int[] height = new int[parts.length];\n            for (int i = 0; i < parts.length; i++) height[i] = Integer.parseInt(parts[i]);\n            System.out.println(maxArea(height));\n        }\n    }\n}\n',
            "cpp": '#include <iostream>\n#include <vector>\n#include <sstream>\n#include <algorithm>\n\nusing namespace std;\n\nint maxArea(vector<int>& height) {\n    // Write your solution here\n    return 0;\n}\n\nint main() {\n    string line;\n    if (getline(cin, line)) {\n        stringstream ss(line);\n        vector<int> height;\n        int val;\n        while (ss >> val) height.push_back(val);\n        cout << maxArea(height) << endl;\n    }\n    return 0;\n}\n'
        },
        "sample_test_cases": [
            {"input": "1 8 6 2 5 4 8 3 7", "expected_output": "49", "explanation": "The lines 8 and 7 form container of width 7, height 7, total area 49."},
            {"input": "1 1", "expected_output": "1", "explanation": "Width is 1, height is 1, area 1."}
        ],
        "hidden_test_cases": [
            {"input": "4 3 2 1 4", "expected_output": "16"},
            {"input": "1 2 1", "expected_output": "2"},
            {"input": "2 3 4 5 18 17 6", "expected_output": "17"},
            {"input": "1 8 6 2 5 4 8 25 7", "expected_output": "49"}
        ]
    }
]

BADGES_DATA = [
    {
        "code": "first_solve",
        "name": "First Solve",
        "description": "Solved your first coding challenge on CareerPilot!",
        "icon": "fa-medal",
        "xp_bonus": 50
    },
    {
        "code": "solve_10",
        "name": "10 Problems Solved",
        "description": "Successfully solved 10 DSA challenges.",
        "icon": "fa-trophy",
        "xp_bonus": 100
    },
    {
        "code": "solve_50",
        "name": "50 Problems Solved",
        "description": "Reached the 50 DSA solved milestone!",
        "icon": "fa-crown",
        "xp_bonus": 250
    },
    {
        "code": "solve_100",
        "name": "Grandmaster Coder",
        "description": "Solved 100+ coding challenges.",
        "icon": "fa-gem",
        "xp_bonus": 500
    },
    {
        "code": "streak_7",
        "name": "7-Day Streak",
        "description": "Solved problems for 7 consecutive days.",
        "icon": "fa-fire",
        "xp_bonus": 150
    },
    {
        "code": "hard_crusher",
        "name": "Hard Problem Crusher",
        "description": "Conquered a Hard difficulty algorithmic challenge.",
        "icon": "fa-skull-crossbones",
        "xp_bonus": 100
    }
]


def seed_coding_database(app=None):
    """Seeds the coding problems and badges tables."""
    if app is None:
        app = create_app(DevelopmentConfig)

    with app.app_context():
        print("Seeding Coding Badges...")
        for b_data in BADGES_DATA:
            existing_b = CodingBadge.query.filter_by(code=b_data["code"]).first()
            if not existing_b:
                badge = CodingBadge(**b_data)
                db.session.add(badge)
            else:
                for k, v in b_data.items():
                    setattr(existing_b, k, v)

        print("Seeding Coding Problems...")
        for p_data in PROBLEMS_DATA:
            existing_p = CodingProblem.query.filter_by(slug=p_data["slug"]).first()
            if not existing_p:
                p = CodingProblem(
                    title=p_data["title"],
                    slug=p_data["slug"],
                    topic=p_data["topic"],
                    difficulty=p_data["difficulty"],
                    company_tags=p_data.get("company_tags", ""),
                    xp_reward=p_data.get("xp_reward", 20),
                    description=p_data["description"],
                    input_format=p_data.get("input_format", ""),
                    output_format=p_data.get("output_format", ""),
                    constraints=p_data.get("constraints", "")
                )
                p.starter_templates = p_data.get("starter_templates", {})
                p.sample_test_cases = p_data.get("sample_test_cases", [])
                p.hidden_test_cases = p_data.get("hidden_test_cases", [])
                db.session.add(p)
            else:
                existing_p.title = p_data["title"]
                existing_p.topic = p_data["topic"]
                existing_p.difficulty = p_data["difficulty"]
                existing_p.company_tags = p_data.get("company_tags", "")
                existing_p.xp_reward = p_data.get("xp_reward", 20)
                existing_p.description = p_data["description"]
                existing_p.input_format = p_data.get("input_format", "")
                existing_p.output_format = p_data.get("output_format", "")
                existing_p.constraints = p_data.get("constraints", "")
                existing_p.starter_templates = p_data.get("starter_templates", {})
                existing_p.sample_test_cases = p_data.get("sample_test_cases", [])
                existing_p.hidden_test_cases = p_data.get("hidden_test_cases", [])

        db.session.commit()
        print(f"Successfully seeded {len(PROBLEMS_DATA)} Coding Problems and {len(BADGES_DATA)} Badges.")


if __name__ == "__main__":
    seed_coding_database()
