import json
import re
from pathlib import Path


INPUT_FILE = "data/all_benchmarks.jsonl"
OUTPUT_FILE = "data/benchmark_rubrics.json"


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [
            json.loads(line)
            for line in f
            if line.strip()
        ]


def clean_text(text):
    if not text:
        return ""

    text = str(text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def build_rubrics(records):
    rubrics = {}

    for item in records:

        question_id = item["id"]

        rubrics[question_id] = {
            "id": question_id,
            "domain": item["domain"],
            "difficulty": item["difficulty"],
            "skill": item["skill"],

            "question": item["question"],

            "evaluation_criteria": clean_text(
                item.get("evaluation_criteria")
            ),

            "reference_answer_points": clean_text(
                item.get("reference_answer_points")
            ),

            "scoring_rubric": item.get(
                "scoring_rubric",
                {}
            )
        }

    return rubrics


def main():

    print("Loading benchmark dataset...")

    records = load_jsonl(INPUT_FILE)

    print(
        f"Loaded {len(records)} benchmark questions."
    )

    rubrics = build_rubrics(records)

    Path(OUTPUT_FILE).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            rubrics,
            f,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("=" * 60)
    print("FRONTIERBENCH RUBRIC BUILDER")
    print("=" * 60)
    print()

    print(
        f"Questions processed: {len(records)}"
    )

    print(
        f"Rubrics created: {len(rubrics)}"
    )

    print()

    print(
        f"Saved to: {OUTPUT_FILE}"
    )

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()