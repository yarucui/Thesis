"""
Figure 4.2 — Mean entropy per model per condition (4 panels).

2x2 grid of bar charts, one per study model. Each panel shows mean
LLM entropy across the four Direction 1 conditions, with a horizontal
dashed line at the human reference entropy and the VS recovery
percentage annotated above the VS bar.

Data source: data/direction1_distributions.csv (132 ambiguous posts).

Run:
    python figures/fig42_d1_entropy_by_model_condition/generate.py
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

CONDITION_COLORS = {
    "baseline": "#cccccc",
    "vs":       "#1a9850",
    "dv":       "#66bd63",
    "hight":    "#bbbbbb",
}
CONDITION_LABELS = {
    "baseline": "Forced\n$T{=}0.7$",
    "vs":       "VS\n$T{=}0.7$",
    "dv":       "DV\n$T{=}0.7$",
    "hight":    "Forced\n$T{=}1.2$",
}
CONDITION_ORDER = ["baseline", "vs", "dv", "hight"]

MODEL_PANELS = [("gpt", "GPT-5"), ("claude", "Claude Sonnet 4.6"),
                ("mistral", "Mistral Large 2411"), ("llama", "Llama 4 Maverick")]
HUMAN_COLOR = "#000000"

RNG = np.random.default_rng(42)
N_BOOT = 1_000

ROOT = Path(__file__).resolve().parents[2]
CSV  = ROOT / "data" / "direction1_distributions.csv"
OUT  = Path(__file__).resolve().parent / "out.pdf"


def boot_ci(values: np.ndarray, n_boot: int = N_BOOT) -> tuple[float, float]:
    if len(values) == 0:
        return (0.0, 0.0)
    means = np.empty(n_boot)
    n = len(values)
    for i in range(n_boot):
        idx = RNG.integers(0, n, n)
        means[i] = values[idx].mean()
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def main() -> None:
    df = pd.read_csv(CSV)
    print(f"Loaded {len(df)} rows from {CSV.name}")

    human_entropy = df[df["condition"] == "baseline"]["human_entropy"].mean()
    print(f"Mean human entropy (132 ambiguous posts): {human_entropy:.4f}")

    fig, axes = plt.subplots(2, 2, figsize=(8.5, 7), sharey=True)
    axes_flat = axes.flatten()

    for ax, (model_key, model_label) in zip(axes_flat, MODEL_PANELS):
        sub = df[df["model"] == model_key]
        means: list[float] = []
        ci_lows: list[float] = []
        ci_highs: list[float] = []
        for c in CONDITION_ORDER:
            vals = sub[sub["condition"] == c]["llm_entropy"].dropna().to_numpy(float)
            means.append(float(vals.mean()) if len(vals) else 0.0)
            lo, hi = boot_ci(vals)
            ci_lows.append(lo)
            ci_highs.append(hi)

        x = np.arange(len(CONDITION_ORDER))
        bars = ax.bar(x, means,
                      color=[CONDITION_COLORS[c] for c in CONDITION_ORDER],
                      edgecolor="black", linewidth=0.6, width=0.7)
        # 95% CI error bars
        yerr_low = [m - lo for m, lo in zip(means, ci_lows)]
        yerr_high = [hi - m for m, hi in zip(means, ci_highs)]
        ax.errorbar(x, means, yerr=[yerr_low, yerr_high],
                    fmt="none", ecolor="black", capsize=3, linewidth=0.8)

        # Human reference line
        ax.axhline(human_entropy, linestyle="--", color=HUMAN_COLOR,
                   linewidth=1.0, alpha=0.85)

        # Recovery annotation above VS bar
        h_base = sub[sub["condition"] == "baseline"]["llm_entropy"].mean()
        h_vs   = sub[sub["condition"] == "vs"]["llm_entropy"].mean()
        h_hum  = sub[sub["condition"] == "baseline"]["human_entropy"].mean()
        recovery_pct = 100.0 * (h_vs - h_base) / (h_hum - h_base)
        ax.text(1, h_vs + 0.04, f"{recovery_pct:.0f}\\%",
                ha="center", va="bottom", fontsize=10, fontweight="bold")

        ax.set_xticks(x)
        ax.set_xticklabels([CONDITION_LABELS[c] for c in CONDITION_ORDER])
        ax.set_ylim(0, 0.75)
        ax.set_title(model_label)
        if ax in (axes[0, 0], axes[1, 0]):
            ax.set_ylabel("Mean LLM entropy (nats)")

    # Single legend element for human reference (above panels)
    axes[0, 1].plot([], [], linestyle="--", color=HUMAN_COLOR,
                    label=f"Human reference ({human_entropy:.3f} nats)")
    axes[0, 1].legend(loc="upper right", framealpha=0.92, fontsize=8.5)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    plt.close(fig)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
