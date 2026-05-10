"""
Master figure generator for thesis.

All publication figures are generated here so they are reproducible.
Run from the thesis/ root:
    python figures/master_figure.py

Output: figures/*.pdf (one file per figure)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
FIG_DIR = ROOT / "figures"

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "legend.fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

COLORS = {
    "baseline": "#4c72b0",
    "vs":       "#dd8452",
    "dv":       "#55a868",
    "hight":    "#c44e52",
    "advisor":  "#4c72b0",
    "oracle":   "#dd8452",
    "personal": "#55a868",
}

MODEL_ORDER = ["gpt", "claude", "mistral", "llama"]
MODEL_LABELS = {"gpt": "GPT-5", "claude": "Claude", "mistral": "Mistral", "llama": "Llama"}


# ---------------------------------------------------------------------------
# Figure 1 — D1: mean entropy per condition per model
# ---------------------------------------------------------------------------

def fig_d1_entropy() -> None:
    d1 = pd.read_csv(DATA_DIR / "direction1_distributions.csv")
    conditions = ["baseline", "vs", "dv", "hight"]
    labels = {"baseline": "Baseline\n(forced)", "vs": "VS\n(verbalized)",
               "dv": "DV\n(descriptive)", "hight": "High-T\n(T=1.2)"}

    fig, axes = plt.subplots(1, 4, figsize=(10, 3.5), sharey=True)
    for ax, model in zip(axes, MODEL_ORDER):
        sub = d1[d1["model"] == model]
        means = [sub[sub["condition"] == c]["llm_entropy"].mean() for c in conditions]
        human_mean = sub["human_entropy"].mean()
        colors = [COLORS[c] for c in conditions]
        bars = ax.bar([labels[c] for c in conditions], means, color=colors, width=0.6, alpha=0.85)
        ax.axhline(human_mean, color="black", linewidth=1.2, linestyle="--", label="Human")
        ax.set_title(MODEL_LABELS[model])
        ax.set_ylim(0, 0.75)
        if ax == axes[0]:
            ax.set_ylabel("Mean entropy (nats)")
    axes[-1].legend(loc="upper right", framealpha=0.9)
    fig.suptitle("Entropy by output condition and model (Direction 1)", y=1.02)
    fig.tight_layout()
    out = FIG_DIR / "fig1_d1_entropy.pdf"
    fig.savefig(out)
    plt.close(fig)
    print(f"Saved {out}")


# ---------------------------------------------------------------------------
# Figure 2 — D2: mean abs_gap per framing per model
# ---------------------------------------------------------------------------

def fig_d2_absgap() -> None:
    d2 = pd.read_csv(DATA_DIR / "direction2_comparison_table.csv")
    d2 = d2[d2["qualified_for_analysis"] == 1]
    framings = ["advisor", "oracle", "personal"]
    x = np.arange(len(MODEL_ORDER))
    width = 0.22

    fig, ax = plt.subplots(figsize=(7, 4))
    for i, framing in enumerate(framings):
        sub = d2[d2["framing"] == framing]
        means = [sub[sub["model"] == m]["abs_gap"].mean() for m in MODEL_ORDER]
        ax.bar(x + i * width, means, width, label=framing.capitalize(),
               color=COLORS[framing], alpha=0.85)

    ax.set_xticks(x + width)
    ax.set_xticklabels([MODEL_LABELS[m] for m in MODEL_ORDER])
    ax.set_ylabel("Mean |LLM − human| risky rate")
    ax.set_title("Alignment gap by role framing and model (Direction 2)")
    ax.legend(framealpha=0.9)
    fig.tight_layout()
    out = FIG_DIR / "fig2_d2_absgap.pdf"
    fig.savefig(out)
    plt.close(fig)
    print(f"Saved {out}")


# ---------------------------------------------------------------------------
# Figure 3 — Mechanism map (text-based 2x2)
# ---------------------------------------------------------------------------

def fig_mechanism_map() -> None:
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.axis("off")

    # Grid lines
    for x in [0, 1, 2]:
        ax.axvline(x, color="black", linewidth=1)
    for y in [0, 1, 2]:
        ax.axhline(y, color="black", linewidth=1)

    # Row/column labels
    ax.text(0.5, 2.08, "Single-token output", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.text(1.5, 2.08, "Distribution output", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.text(-0.05, 1.5, "Prescriptive\nrole", ha="right", va="center", fontsize=9, fontweight="bold")
    ax.text(-0.05, 0.5, "Descriptive\nrole", ha="right", va="center", fontsize=9, fontweight="bold")

    # Cell content
    cells = [
        (0.5, 1.5, "Baseline\n(Step 5)\nΔ = 0 (ref)", "#4c72b0"),
        (1.5, 1.5, "Direction 1\nVS / DV\nΔ ≈ −0.23***", "#55a868"),
        (0.5, 0.5, "Direction 2\nOracle / Personal\nΔ ≈ −0.01 to −0.03**", "#dd8452"),
        (1.5, 0.5, "Direction 1\nHigh-T\nΔ ≈ −0.02**", "#c44e52"),
    ]
    for cx, cy, label, color in cells:
        ax.add_patch(plt.Rectangle((cx - 0.5, cy - 0.5), 1, 1,
                                   facecolor=color, alpha=0.15, zorder=0))
        ax.text(cx, cy, label, ha="center", va="center", fontsize=8.5)

    ax.set_title("Mechanism map: output format × role framing", pad=20)
    fig.tight_layout()
    out = FIG_DIR / "fig3_mechanism_map.pdf"
    fig.savefig(out)
    plt.close(fig)
    print(f"Saved {out}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    FIG_DIR.mkdir(exist_ok=True)
    fig_d1_entropy()
    fig_d2_absgap()
    fig_mechanism_map()
    print("All figures generated.")
