"""
Figure 5.1 — Framing effect boxplot.

1x4 grid of boxplots, one panel per study model. Each panel shows the
distribution of abs_gap across (post, model, framing) cells for the
three framings: advisor, oracle, personal.

Data source: data/direction2_comparison_table.csv, qualified cells only
(620-post corpus per Decision 1).

Run:
    python figures/fig51_framing_boxplot/generate.py
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

FRAMING_COLORS = {
    "advisor":  "#cccccc",
    "oracle":   "#a6cee3",
    "personal": "#fdbf6f",
}
FRAMING_ORDER = ["advisor", "oracle", "personal"]
MODEL_PANELS = [("gpt", "GPT-5"), ("claude", "Claude Sonnet 4.6"),
                ("mistral", "Mistral Large 2411"), ("llama", "Llama 4 Maverick")]

ROOT = Path(__file__).resolve().parents[2]
CSV  = ROOT / "data" / "direction2_comparison_table.csv"
OUT  = Path(__file__).resolve().parent / "out.pdf"


def main() -> None:
    df = pd.read_csv(CSV)
    q = df[df["qualified_for_analysis"] == 1]
    print(f"Loaded {len(q)} qualified cells from {CSV.name}")

    fig, axes = plt.subplots(1, 4, figsize=(13, 4), sharey=True)

    for ax, (model_key, model_label) in zip(axes, MODEL_PANELS):
        sub = q[q["model"] == model_key]
        data = [sub[sub["framing"] == f]["abs_gap"].dropna().to_numpy(float)
                for f in FRAMING_ORDER]
        means = [vals.mean() if len(vals) else float("nan") for vals in data]
        positions = np.arange(1, len(FRAMING_ORDER) + 1)

        bp = ax.boxplot(
            data, positions=positions, widths=0.6,
            patch_artist=True, showfliers=True,
            medianprops=dict(color="black", linewidth=1.2),
            flierprops=dict(marker="o", markersize=2.0,
                            markerfacecolor="grey", markeredgecolor="none",
                            alpha=0.35),
            whiskerprops=dict(color="black", linewidth=0.8),
            capprops=dict(color="black", linewidth=0.8),
        )
        for patch, f in zip(bp["boxes"], FRAMING_ORDER):
            patch.set_facecolor(FRAMING_COLORS[f])
            patch.set_edgecolor("black")
            patch.set_linewidth(0.8)

        # Mean marker (white diamond) on top of median
        ax.scatter(positions, means, marker="D",
                   facecolor="white", edgecolor="black",
                   s=28, zorder=3, linewidth=0.8)

        # Annotate mean below each box
        for pos, m in zip(positions, means):
            ax.text(pos, -0.07, f"{m:.3f}",
                    ha="center", va="top", fontsize=8.5)

        ax.set_xticks(positions)
        ax.set_xticklabels([f.capitalize() for f in FRAMING_ORDER])
        ax.set_ylim(0, 1)
        ax.set_title(model_label)
        if ax is axes[0]:
            ax.set_ylabel("Absolute alignment gap")

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    plt.close(fig)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
