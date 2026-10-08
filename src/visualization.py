import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [
            json.loads(line)
            for line in f
            if line.strip()
        ]


def create_visualizations(input_path, output_dir):
    # Load graded results
    results = load_jsonl(input_path)

    if not results:
        raise ValueError("No graded results found.")

    # Convert to DataFrame
    df = pd.DataFrame(results)

    # Create output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # Set Seaborn theme
    sns.set_theme(
        style="whitegrid"
    )

    # ---------------------------------------------------------
    # 1. DOMAIN PERFORMANCE
    # ---------------------------------------------------------

    domain_df = (
        df.groupby("domain")["overall_percent"]
        .mean()
        .reset_index()
    )

    domain_df = domain_df.sort_values(
        "overall_percent",
        ascending=False
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=domain_df,
        x="domain",
        y="overall_percent"
    )

    plt.title(
        "FrontierBench Performance by Domain",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("Domain")
    plt.ylabel("Average Score (%)")

    plt.ylim(0, 100)

    plt.xticks(
        rotation=20
    )

    plt.tight_layout()

    plt.savefig(
        output_dir / "domain_performance.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    # ---------------------------------------------------------
    # 2. SKILL PERFORMANCE
    # ---------------------------------------------------------

    skill_df = (
        df.groupby("skill")["overall_percent"]
        .mean()
        .reset_index()
    )

    skill_df = skill_df.sort_values(
        "overall_percent",
        ascending=True
    )

    plt.figure(figsize=(10, 7))

    sns.barplot(
        data=skill_df,
        x="overall_percent",
        y="skill"
    )

    plt.title(
        "FrontierBench Performance by Skill",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("Average Score (%)")
    plt.ylabel("Skill")

    plt.xlim(0, 100)

    plt.tight_layout()

    plt.savefig(
        output_dir / "skill_performance.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    # ---------------------------------------------------------
    # 3. SCORE DISTRIBUTION
    # ---------------------------------------------------------

    plt.figure(figsize=(9, 6))

    sns.histplot(
        data=df,
        x="overall_percent",
        bins=10,
        kde=True
    )

    plt.title(
        "FrontierBench Score Distribution",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("Overall Score (%)")
    plt.ylabel("Number of Questions")

    plt.xlim(0, 100)

    plt.tight_layout()

    plt.savefig(
        output_dir / "score_distribution.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    # ---------------------------------------------------------
    # 4. EVALUATION DIMENSIONS
    # ---------------------------------------------------------

    dimensions = [
        "correctness",
        "reasoning",
        "uncertainty",
        "unsupported_claims"
    ]

    dimension_data = []

    for dimension in dimensions:

        average_score = df[dimension].mean()

        dimension_data.append(
            {
                "dimension": dimension,
                "score": average_score / 4 * 100
            }
        )

    dimension_df = pd.DataFrame(
        dimension_data
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=dimension_df,
        x="dimension",
        y="score"
    )

    plt.title(
        "FrontierBench Evaluation Dimensions",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("Evaluation Dimension")
    plt.ylabel("Average Score (%)")

    plt.ylim(0, 100)

    plt.xticks(
        rotation=15
    )

    plt.tight_layout()

    plt.savefig(
        output_dir / "evaluation_dimensions.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    # ---------------------------------------------------------
    # SAVE SUMMARY DATA
    # ---------------------------------------------------------

    domain_df.to_csv(
        output_dir / "domain_summary.csv",
        index=False
    )

    skill_df.to_csv(
        output_dir / "skill_summary.csv",
        index=False
    )

    dimension_df.to_csv(
        output_dir / "dimension_summary.csv",
        index=False
    )

    print()
    print("=" * 60)
    print("FRONTIERBENCH VISUALIZATION REPORT")
    print("=" * 60)

    print()

    print(
        f"Questions visualized: {len(df)}"
    )

    print(
        f"Domains: {df['domain'].nunique()}"
    )

    print(
        f"Skills: {df['skill'].nunique()}"
    )

    print()

    print("Charts created:")

    print(
        "✓ domain_performance.png"
    )

    print(
        "✓ skill_performance.png"
    )

    print(
        "✓ score_distribution.png"
    )

    print(
        "✓ evaluation_dimensions.png"
    )

    print()

    print(
        f"Saved to: {output_dir}"
    )

    print("=" * 60)


def main():

    parser = argparse.ArgumentParser(
        description="FrontierBench visualization engine"
    )

    parser.add_argument(
        "--input",
        default="results/graded_results.jsonl",
        help="Path to graded results"
    )

    parser.add_argument(
        "--output",
        default="visualizations",
        help="Directory for generated charts"
    )

    args = parser.parse_args()

    create_visualizations(
        args.input,
        args.output
    )


if __name__ == "__main__":
    main()