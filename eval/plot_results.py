"""Render the main evaluation results as a grouped bar chart for the README.

Numbers are the frozen-agent scores from eval/artifacts/scoring_report.md
(25 factual + 35 longitudinal questions, 3 runs each). Re-run to regenerate:

  uv run python -m eval.plot_results
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path("docs/eval_results.png")

TIERS = ["Factual", "Longitudinal"]
METRICS = ["Recall", "Groundedness", "Retrieval ceiling"]
# metric -> [factual, longitudinal], percent
SCORES = {
    "Recall": [86.9, 32.2],
    "Groundedness": [96.0, 97.9],
    "Retrieval ceiling": [86.8, 43.5],
}
COLORS = ["#4C72B0", "#55A868", "#C44E52"]


def main() -> None:
    x = np.arange(len(TIERS))
    width = 0.26

    fig, ax = plt.subplots(figsize=(7, 4))
    for i, metric in enumerate(METRICS):
        offset = (i - 1) * width
        bars = ax.bar(x + offset, SCORES[metric], width, label=metric, color=COLORS[i])
        ax.bar_label(bars, fmt="%.1f", padding=2, fontsize=8)

    ax.set_xticks(x, TIERS)
    ax.set_ylim(0, 118)
    ax.set_ylabel("Percent")
    ax.set_title("Agent scores by question type (3 runs each)", pad=28)
    ax.legend(loc="upper center", ncol=3, frameon=False,
              bbox_to_anchor=(0.5, 1.10))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT, dpi=150)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
