"""Check questions.json before you publish it.

Run it from this folder:
    python validate_questions.py
"""

import json
import sys
from collections import Counter
from pathlib import Path

QUESTIONS_FILE = Path(__file__).parent / "questions.json"


def load_questions(path):
    """Read the JSON file and return its contents."""
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def check_structure(questions):
    """Return a list of problems with how each question is written."""
    problems = []
    for position, item in enumerate(questions, start=1):
        if not isinstance(item, dict):
            problems.append(f"Item {position}: must look like {{\"id\": 1, \"question\": \"...\"}}")
            continue
        if not isinstance(item.get("id"), int):
            problems.append(f"Item {position}: 'id' must be a whole number.")
        text = item.get("question")
        if not isinstance(text, str) or not text.strip():
            problems.append(f"Item {position}: 'question' must be non-empty text.")
    return problems


def find_duplicates(values, label):
    """Return a message for every value that appears more than once."""
    counts = Counter(values)
    return [f"Duplicate {label}: {value!r}" for value, count in counts.items() if count > 1]


def cooldown_size(bank_size):
    """Same rule as deck.js: how many questions must pass before a repeat."""
    more_than_half = bank_size // 2 + 1
    return max(0, min(more_than_half, bank_size - 1))


def main():
    try:
        questions = load_questions(QUESTIONS_FILE)
    except FileNotFoundError:
        sys.exit(f"Could not find {QUESTIONS_FILE}")
    except json.JSONDecodeError as error:
        sys.exit(f"questions.json is not valid JSON: {error}")

    if not isinstance(questions, list) or not questions:
        sys.exit("questions.json must be a non-empty list.")

    problems = check_structure(questions)
    if not problems:  # duplicate checks only make sense once the structure is right
        problems += find_duplicates([q["id"] for q in questions], "id")
        problems += find_duplicates([q["question"].strip().lower() for q in questions], "question")

    if problems:
        print("Found problems:")
        for problem in problems:
            print(f"  - {problem}")
        sys.exit(1)

    count = len(questions)
    print(f"OK: {count} questions.")
    print(f"A question can only return after {cooldown_size(count)} others have been shown.")


if __name__ == "__main__":
    main()
