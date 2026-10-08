import argparse
import json
import re
from pathlib import Path


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [
            json.loads(line)
            for line in f
            if line.strip()
        ]


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def normalize(text):
    if not text:
        return ""

    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_keywords(text):
    """
    Extract useful content words from rubric/reference text.
    Very common words are ignored.
    """
    stop_words = {
        "the", "and", "or", "of", "to", "a", "an",
        "is", "are", "be", "for", "in", "on", "with",
        "that", "this", "from", "as", "by", "it",
        "should", "can", "may", "must", "explain",
        "identify", "why", "how", "what", "relevant",
        "appropriate", "using", "uses", "applies"
    }

    words = re.findall(r"[a-zA-Z][a-zA-Z\-]{3,}", normalize(text))

    return {
        word
        for word in words
        if word not in stop_words
    }


def concept_overlap(response, rubric):
    """
    Compare the response with the question-specific
    reference/evaluation material.

    This is an offline heuristic, not expert judgment.
    """

    response_words = extract_keywords(response)

    reference_text = " ".join([
        rubric.get("evaluation_criteria", ""),
        rubric.get("reference_answer_points", "")
    ])

    reference_words = extract_keywords(reference_text)

    if not reference_words:
        return 0.0

    overlap = response_words.intersection(reference_words)

    return len(overlap) / len(reference_words)


def calculate_correctness(response, rubric):
    score = concept_overlap(response, rubric)

    if score >= 0.55:
        return 4

    if score >= 0.35:
        return 3

    if score >= 0.18:
        return 2

    if score > 0:
        return 1

    return 0


def calculate_reasoning(response):
    response = normalize(response)

    reasoning_signals = [
        "because",
        "therefore",
        "however",
        "although",
        "while",
        "depends",
        "reason",
        "reasoning",
        "explain",
        "distinguish",
        "consider",
        "evidence",
        "assumption",
        "limitation",
        "trade-off",
        "tradeoff"
    ]

    matches = sum(
        signal in response
        for signal in reasoning_signals
    )

    if matches >= 6:
        return 4

    if matches >= 4:
        return 3

    if matches >= 2:
        return 2

    if matches >= 1:
        return 1

    return 0


def calculate_uncertainty(response, rubric):
    response = normalize(response)

    uncertainty_required = (
        "uncertainty"
        in normalize(
            rubric.get("evaluation_criteria", "")
        )
        or "limitation"
        in normalize(
            rubric.get("evaluation_criteria", "")
        )
        or "assumption"
        in normalize(
            rubric.get("evaluation_criteria", "")
        )
    )

    if not uncertainty_required:
        return 4

    uncertainty_terms = [
        "uncertain",
        "uncertainty",
        "depends",
        "may",
        "might",
        "could",
        "insufficient",
        "not enough",
        "cannot conclude",
        "limitation",
        "limitations",
        "assumption",
        "context"
    ]

    matches = sum(
        term in response
        for term in uncertainty_terms
    )

    if matches >= 3:
        return 4

    if matches >= 2:
        return 3

    if matches >= 1:
        return 2

    return 1


def calculate_unsupported_claims(response):
    response = normalize(response)

    risky_terms = [
        "always",
        "never",
        "guaranteed",
        "definitely",
        "certainly",
        "proves",
        "proven"
    ]

    matches = sum(
        term in response
        for term in risky_terms
    )

    if matches == 0:
        return 4

    if matches == 1:
        return 3

    if matches == 2:
        return 2

    return 1


def calculate_overall(
    correctness,
    reasoning,
    uncertainty,
    unsupported_claims
):
    scores = [
        correctness,
        reasoning,
        uncertainty,
        unsupported_claims
    ]

    return round(
        sum(scores) / 4,
        2
    )


def grade_response(item, rubric):
    response = item.get("response", "")

    correctness = calculate_correctness(
        response,
        rubric
    )

    reasoning = calculate_reasoning(
        response
    )

    uncertainty = calculate_uncertainty(
        response,
        rubric
    )

    unsupported_claims = calculate_unsupported_claims(
        response
    )

    overall = calculate_overall(
        correctness,
        reasoning,
        uncertainty,
        unsupported_claims
    )

    return {
        "question_id": item["question_id"],
        "domain": item["domain"],
        "skill": item["skill"],
        "model": item.get("model", "unknown"),
        "mode": item.get("mode", "unknown"),

        "correctness": correctness,
        "reasoning": reasoning,
        "uncertainty": uncertainty,
        "unsupported_claims": unsupported_claims,

        "overall_score": overall,
        "overall_percent": round(
            overall / 4 * 100,
            2
        ),

        "grading_method": "offline_rubric_heuristic",

        "rubric_source": "data/benchmark_rubrics.json"
    }


def main():

    parser = argparse.ArgumentParser(
        description="FrontierBench 125-question grading engine"
    )

    parser.add_argument(
        "--input",
        default="results/raw_results.jsonl",
        help="Path to raw evaluation results"
    )

    parser.add_argument(
        "--rubric",
        default="data/benchmark_rubrics.json",
        help="Path to full benchmark rubric"
    )

    parser.add_argument(
        "--output",
        default="results/graded_results.jsonl",
        help="Path to graded results"
    )

    args = parser.parse_args()

    print("Loading evaluation results...")

    results = load_jsonl(args.input)

    print(
        f"Loaded {len(results)} evaluation results."
    )

    print()

    print("Loading benchmark rubrics...")

    rubrics = load_json(args.rubric)

    print(
        f"Loaded {len(rubrics)} question-specific rubrics."
    )

    print()

    graded_results = []

    missing_rubrics = []

    for number, item in enumerate(
        results,
        start=1
    ):

        question_id = item["question_id"]

        rubric = rubrics.get(question_id)

        if rubric is None:
            missing_rubrics.append(
                question_id
            )

            print(
                f"[{number}/{len(results)}] "
                f"{question_id} - NO RUBRIC"
            )

            continue

        grade = grade_response(
            item,
            rubric
        )

        graded_results.append(grade)

        print(
            f"[{number}/{len(results)}] "
            f"{question_id} - "
            f"{grade['overall_score']}/4 "
            f"({grade['overall_percent']}%)"
        )

    Path(args.output).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        args.output,
        "w",
        encoding="utf-8"
    ) as f:

        for result in graded_results:
            f.write(
                json.dumps(
                    result,
                    ensure_ascii=False
                ) + "\n"
            )

    print()
    print("=" * 60)
    print("FRONTIERBENCH GRADING REPORT")
    print("=" * 60)

    print(
        f"Results graded: {len(graded_results)}"
    )

    print(
        f"Missing rubrics: {len(missing_rubrics)}"
    )

    if missing_rubrics:
        print()
        print("Questions without rubrics:")

        for question_id in missing_rubrics:
            print(f"  - {question_id}")

    print()
    print(
        f"Saved to: {args.output}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()