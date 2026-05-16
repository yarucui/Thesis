"""
Figure 4.1 — Distribution shape baseline.

Two-panel histogram pair contrasting the human reference distribution
(upvote-weighted comment fractions) with the LLM baseline distribution
(per-cell forced-choice rates).

Data source: data/direction2_comparison_table.csv, framing == 'advisor'
(the reused baseline data on the full 620-post corpus, per merged
Chapter 3 §3.4.2 and Decision 1).

Run:
    python figures/fig41_distribution_shape/generate.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "legend.fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.1,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

MODEL_COLORS = {
    "gpt":     "#1f77b4",
    "claude":  "#ff7f0e",
    "mistral": "#2ca02c",
    "llama":   "#d62728",
}
MODEL_LABELS = {
    "gpt": "GPT-5",
    "claude": "Claude Sonnet 4.6",
    "mistral": "Mistral Large 2411",
    "llama": "Llama 4 Maverick",
}
HUMAN_COLOR = "#000000"

ROOT = Path(__file__).resolve().parents[2]
CSV  = ROOT / "data" / "direction2_comparison_table.csv"
OUT  = Path(__file__).resolve().parent / "out.pdf"


def main() -> None:
    df = pd.read_csv(CSV)
    adv = df[(df["framing"] == "advisor") & (df["qualified_for_analysis"] == 1)].copy()
    print(f"Loaded {len(adv)} advisor cells across {adv['post_id'].nunique()} posts")

    bins = np.linspace(0, 1, 21)  # 20 bins

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Left: human distribution (one value per post)
    human_per_post = (
        adv.drop_duplicates("post_id")["human_risky_ratio"]
        .dropna().to_numpy(float)
    )
    axes[0].hist(human_per_post, bins=bins, color=HUMAN_COLOR,
                 alpha=0.60, edgecolor="black", linewidth=0.5)
    axes[0].set_title("Human community (Reddit upvote-weighted)")
    axes[0].set_xlabel("Fraction supporting risky option")
    axes[0].set_ylabel(f"Number of posts (n = {len(human_per_post)})")
    axes[0].set_xlim(0, 1)

    # Right: LLM distribution (one value per (post, model) cell)
    for model in ["gpt", "claude", "mistral", "llama"]:
        vals = adv[adv["model"] == model]["llm_risky_rate"].dropna().to_numpy(float)
        axes[1].hist(vals, bins=bins, color=MODEL_COLORS[model],
                     alpha=0.50, label=MODEL_LABELS[model], edgecolor="none")
    axes[1].set_title("LLM baseline (forced choice, $N{=}10$, $T{=}0.7$)")
    axes[1].set_xlabel("LLM fraction choosing risky option")
    axes[1].set_ylabel("Number of (post, model) cells")
    axes[1].set_xlim(0, 1)
    axes[1].legend(loc="upper center", framealpha=0.92)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    plt.close(fig)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
