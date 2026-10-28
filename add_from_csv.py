"""Add questions from a CSV file to questions.json, skipping duplicates.

Usage:
    1. Put your CSV in the same folder as questions.json.
    2. If its name isn't new_questions.csv, change CSV_FILENAME below.
    3. Run:  python add_from_csv.py

The CSV needs one question per row, in the first column.
A header row (a first cell that says "question") is optional.
"""

import csv
import json
import sys
from pathlib import Path

# ---- Settings: change CSV_FILENAME to match your file ----
CSV_FILENAME = "new_questions.csv"

QUESTIONS_FILE = Path(__file__).parent / "questions.json"
CSV_FILE = QUESTIONS_FILE.parent / CSV_FILENAME  # always next to questions.json


def normalize(text):
    """Make two questions comparable: ignore case, extra spaces and line breaks."""
    return " ".join(text.lower().split())


def read_csv_questions(path):
    """Return the question text from the first column of the CSV."""
    questions = []
    with open(path, newline="", encoding="utf-8-sig") as file:  # utf-8-sig handles Excel files
        for row_number, row in enumerate(csv.reader(file)):
            if not row:
                continue  # empty line
            text = row[0].strip()
            if not text:
                continue  # empty first cell
            if row_number == 0 and normalize(text) == "question":
                continue  # header row
            questions.append(text)
    return questions


def load_questions(path):
    """Read the current question bank."""
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def split_new_and_duplicates(existing, candidates):
    """Sort CSV questions into 'new' and 'duplicates'.

    A question is a duplicate if it is already in the bank
    or appeared earlier in the CSV.
    """
    seen = {normalize(q["question"]) for q in existing}
    new, duplicates = [], []
    for text in candidates:
        key = normalize(text)
        if key in seen:
            duplicates.append(text)
        else:
            seen.add(key)
            new.append(text)
    return new, duplicates


def add_questions(existing, new_texts):
    """Return the bank with the new questions added, each with a fresh id."""
    next_id = max((q["id"] for q in existing), default=0) + 1
    added = [{"id": next_id + i, "question": text} for i, text in enumerate(new_texts)]
    return existing + added


def save_questions(path, questions):
    """Write the bank back to disk, one question per line."""
    lines = [f"  {json.dumps(q, ensure_ascii=False)}" for q in questions]
    path.write_text("[\n" + ",\n".join(lines) + "\n]\n", encoding="utf-8")


def main():
    try:
        candidates = read_csv_questions(CSV_FILE)
        existing = load_questions(QUESTIONS_FILE)
    except FileNotFoundError as error:
        sys.exit(f"File not found: {error.filename}")
    except json.JSONDecodeError as error:
        sys.exit(f"questions.json is not valid JSON: {error}")

    new_texts, duplicates = split_new_and_duplicates(existing, candidates)

    if new_texts:
        save_questions(QUESTIONS_FILE, add_questions(existing, new_texts))

    print(f"Added {len(new_texts)} new question(s).")
    if duplicates:
        print(f"Skipped {len(duplicates)} duplicate(s):")
        for text in duplicates:
            print(f"  - {text}")


if __name__ == "__main__":
    main()
