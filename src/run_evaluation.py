import argparse
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def build_prompt(item):
    return f"""
You are being evaluated by FrontierBench.

Domain: {item["domain"]}
Skill: {item["skill"]}
Difficulty: {item["difficulty"]}

Question:
{item["question"]}

Answer the question directly.

Requirements:
- Explain your reasoning clearly.
- State important assumptions.
- Acknowledge meaningful uncertainty.
- Do not invent facts or sources.
"""


def call_openai(model_name, prompt):
    from openai import OpenAI

    client = OpenAI()
    response = client.responses.create(
        model=model_name,
        input=prompt
    )

    return response.output_text


def call_mock_model(item):
    """
    Simulated response used only to test the FrontierBench pipeline.
    These are NOT real model responses.
    """

    domain = item["domain"]
    question = item["question"]

    responses = {
        "software": (
            f"SIMULATED RESPONSE for software evaluation.\n\n"
            f"The question asks: {question}\n\n"
            f"A strong approach would identify the requirements, "
            f"consider edge cases, explain the implementation clearly, "
            f"and verify the result with appropriate tests. "
            f"Important assumptions should be stated explicitly."
        ),

        "finance": (
            f"SIMULATED RESPONSE for finance evaluation.\n\n"
            f"The question asks: {question}\n\n"
            f"The answer should consider the relevant financial assumptions, "
            f"risk factors, time horizon, and available evidence. "
            f"Any numerical conclusion should be checked rather than assumed."
        ),

        "legal": (
            f"SIMULATED RESPONSE for legal reasoning evaluation.\n\n"
            f"The question asks: {question}\n\n"
            f"A proper analysis should identify the relevant legal issue, "
            f"state the applicable principle, apply it to the facts, "
            f"and acknowledge jurisdictional or factual uncertainty."
        ),

        "healthcare": (
            f"SIMULATED RESPONSE for healthcare reasoning evaluation.\n\n"
            f"The question asks: {question}\n\n"
            f"A careful answer should distinguish established evidence "
            f"from uncertainty, consider relevant risk factors, "
            f"and avoid making unsupported conclusions."
        ),

        "science": (
            f"SIMULATED RESPONSE for science evaluation.\n\n"
            f"The question asks: {question}\n\n"
            f"A scientifically sound response should explain the relevant "
            f"mechanism, distinguish evidence from assumptions, "
            f"and identify meaningful limitations."
        ),
    }

    return responses.get(
        domain,
        f"SIMULATED RESPONSE.\n\nQuestion: {question}"
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data",
        default="data/test_10.jsonl"
    )

    parser.add_argument(
        "--model",
        required=True
    )

    parser.add_argument(
        "--output",
        default="results/raw_results.jsonl"
    )

    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run using simulated responses without an API call."
    )

    args = parser.parse_args()

    items = load_jsonl(args.data)

    Path(args.output).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    print(f"Running {len(items)} benchmark questions...")

    if args.mock:
        print("Mode: MOCK (no API calls)")
    else:
        print(f"Model: {args.model}")

    print()

    with open(args.output, "w", encoding="utf-8") as out:

        for number, item in enumerate(items, start=1):

            print(
                f"[{number}/{len(items)}] "
                f"{item['id']} - {item['domain']}"
            )

            start = time.time()

            try:

                if args.mock:
                    response = call_mock_model(item)
                else:
                    response = call_openai(
                        args.model,
                        build_prompt(item)
                    )

                elapsed = time.time() - start

                result = {
                    "question_id": item["id"],
                    "domain": item["domain"],
                    "skill": item["skill"],
                    "model": args.model if not args.mock else "mock-model",
                    "mode": "mock" if args.mock else "live",
                    "response": response,
                    "latency_seconds": round(elapsed, 3)
                }

                out.write(
                    json.dumps(
                        result,
                        ensure_ascii=False
                    ) + "\n"
                )

                out.flush()

                print("  ✓ Response generated")

            except Exception as e:

                print(f"  ✗ Error: {e}")

                result = {
                    "question_id": item["id"],
                    "domain": item["domain"],
                    "skill": item["skill"],
                    "model": args.model,
                    "mode": "mock" if args.mock else "live",
                    "error": str(e)
                }

                out.write(
                    json.dumps(
                        result,
                        ensure_ascii=False
                    ) + "\n"
                )

    print()
    print("Evaluation finished.")
    print(f"Results saved to: {args.output}")


if __name__ == "__main__":
    main()