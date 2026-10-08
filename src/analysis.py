import argparse
import json
from collections import defaultdict
from pathlib import Path


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def average(values):
    if not values:
        return 0
    return round(sum(values) / len(values), 2)


def percent(score):
    return round(score / 4 * 100, 2)


def analyze(results):
    overall_scores = [
        item["overall_score"]
        for item in results
    ]

    domain_scores = defaultdict(list)
    skill_scores = defaultdict(list)

    for item in results:
        domain_scores[item["domain"]].append(
            item["overall_score"]
        )

        skill_scores[item["skill"]].append(
            item["overall_score"]
        )

    # Domain analysis
    domain_analysis = {}

    for domain, scores in sorted(domain_scores.items()):
        avg = average(scores)

        domain_analysis[domain] = {
            "questions": len(scores),
            "average_score": avg,
            "percentage": percent(avg)
        }

    # Skill analysis
    skill_analysis = {}

    for skill, scores in sorted(skill_scores.items()):
        avg = average(scores)

        skill_analysis[skill] = {
            "questions": len(scores),
            "average_score": avg,
            "percentage": percent(avg)
        }

    # Overall score
    overall_average = average(overall_scores)

    # Find strongest and weakest domains
    domain_values = {
        domain: data["average_score"]
        for domain, data in domain_analysis.items()
    }

    highest_score = max(domain_values.values())
    lowest_score = min(domain_values.values())

    strongest_domains = [
        domain
        for domain, score in domain_values.items()
        if score == highest_score
    ]

    weakest_domains = [
        domain
        for domain, score in domain_values.items()
        if score == lowest_score
    ]

    return {
        "benchmark": "FrontierBench",
        "evaluation_mode": results[0].get(
            "mode",
            "unknown"
        ),
        "model": results[0].get(
            "model",
            "unknown"
        ),
        "total_questions": len(results),

        "overall": {
            "average_score": overall_average,
            "percentage": percent(overall_average)
        },

        "strongest_domains": strongest_domains,
        "weakest_domains": weakest_domains,

        "domains": domain_analysis,
        "skills": skill_analysis
    }


def print_report(summary):
    print()
    print("=" * 60)
    print("FRONTIERBENCH ANALYSIS REPORT")
    print("=" * 60)

    print()

    print(f"Model: {summary['model']}")
    print(f"Mode: {summary['evaluation_mode']}")
    print(f"Questions: {summary['total_questions']}")

    print()

    # Overall performance
    print("OVERALL PERFORMANCE")
    print("-" * 30)

    overall = summary["overall"]

    print(
        f"Average Score: "
        f"{overall['average_score']}/4"
    )

    print(
        f"Percentage: "
        f"{overall['percentage']}%"
    )

    print()

    # Domain performance
    print("DOMAIN PERFORMANCE")
    print("-" * 30)

    for domain, data in summary["domains"].items():
        print(
            f"{domain.title():15} "
            f"{data['average_score']}/4 "
            f"({data['percentage']}%) "
            f"[{data['questions']} questions]"
        )

    print()

    print(
        "Strongest Domain(s): "
        + ", ".join(summary["strongest_domains"])
    )

    print(
        "Weakest Domain(s): "
        + ", ".join(summary["weakest_domains"])
    )

    print()

    # Skill performance
    print("SKILL PERFORMANCE")
    print("-" * 30)

    for skill, data in summary["skills"].items():
        print(
            f"{skill:25} "
            f"{data['average_score']}/4 "
            f"({data['percentage']}%)"
        )

    print()

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="FrontierBench analysis engine"
    )

    parser.add_argument(
        "--input",
        default="results/graded_results.jsonl",
        help="Path to graded results"
    )

    parser.add_argument(
        "--output",
        default="results/analysis_summary.json",
        help="Path for analysis summary"
    )

    args = parser.parse_args()

    results = load_jsonl(args.input)

    if not results:
        raise ValueError(
            "No graded results were found."
        )

    print(
        f"Loaded {len(results)} graded results."
    )

    summary = analyze(results)

    Path(args.output).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        args.output,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            summary,
            f,
            indent=2,
            ensure_ascii=False
        )

    print_report(summary)

    print(
        f"Analysis saved to: {args.output}"
    )


if __name__ == "__main__":
    main()