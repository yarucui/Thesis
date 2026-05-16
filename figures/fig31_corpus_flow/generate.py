"""
Figure 3.1 — Corpus construction flow diagram.

Vertical flowchart showing the data funnel from raw Pushshift dumps to
the final 620-post analytical corpus. All numbers are canonical per the
merged Chapter 3 and Decision 1 (620 posts, 3 primary domains,
17 subreddits, March 2026 only, MIN_WORD_COUNT=30).

No data file is read — numbers are hard-coded from the merged Chapter 3
and from the actual pipeline yield documented in §3.2.2.

Run:
    python figures/fig31_corpus_flow/generate.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

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

STAGE_GREY = "#e8e8e8"
FINAL_BLUE = "#cfe2f3"
EDGE_DARK  = "#222222"
ARROW_GREY = "#666666"

OUT = Path(__file__).resolve().parent / "out.pdf"


def box(ax, cx, cy, w, h, text, facecolor, fontsize=10, fontweight="normal"):
    patch = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.04,rounding_size=0.06",
        facecolor=facecolor, edgecolor=EDGE_DARK, linewidth=1.0,
    )
    ax.add_patch(patch)
    ax.text(cx, cy, text, ha="center", va="center",
            fontsize=fontsize, fontweight=fontweight)


def arrow(ax, x1, y1, x2, y2):
    a = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=14,
        color=ARROW_GREY, linewidth=1.2,
    )
    ax.add_patch(a)


def main() -> None:
    fig, ax = plt.subplots(figsize=(6, 9))
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 14)
    ax.set_aspect("equal")
    ax.axis("off")

    # Stage 1 — raw dump
    box(ax, 3.0, 13.0, 5.0, 1.1,
        "Pushshift Reddit dump (2026-03)\n"
        r"$\sim$45,000,000 submissions across all subreddits",
        STAGE_GREY)
    arrow(ax, 3.0, 12.45, 3.0, 11.95)

    # Stage 2 — structural filter
    box(ax, 3.0, 11.25, 5.4, 1.3,
        "Subreddit + self-post + $\\geq$30 words +\n"
        "$\\geq$15 comments + decision trigger phrase\n"
        "(17 subreddits across 3 primary domains)",
        STAGE_GREY, fontsize=9)
    arrow(ax, 3.0, 10.60, 3.0, 10.15)

    box(ax, 3.0, 9.65, 3.4, 0.7,
        r"$\mathbf{1{,}562}$ candidate posts",
        STAGE_GREY, fontweight="bold")
    arrow(ax, 3.0, 9.30, 3.0, 8.85)

    # Stage 3 — Gemini Call A
    box(ax, 3.0, 8.35, 5.4, 1.0,
        "Gemini Call A:\n"
        "genuine binary decision gate + option extraction",
        STAGE_GREY, fontsize=9)
    arrow(ax, 3.0, 7.85, 3.0, 7.40)

    box(ax, 3.0, 6.90, 3.4, 0.7,
        r"$\mathbf{811}$ posts",
        STAGE_GREY, fontweight="bold")
    arrow(ax, 3.0, 6.55, 3.0, 6.10)

    # Stage 4 — Gemini Call B + validation
    box(ax, 3.0, 5.60, 5.4, 1.0,
        "Gemini Call B + Step 2b validation:\n"
        "stance, features, SES; required-fields check",
        STAGE_GREY, fontsize=9)
    arrow(ax, 3.0, 5.10, 3.0, 4.60)

    box(ax, 3.0, 4.10, 3.6, 0.9,
        r"$\mathbf{620}$ valid posts" + "\n(final analytical corpus)",
        FINAL_BLUE, fontweight="bold")

    # Domain breakdown branches
    arrow(ax, 3.0, 3.65, 1.4, 2.95)
    arrow(ax, 3.0, 3.65, 3.0, 2.95)
    arrow(ax, 3.0, 3.65, 4.6, 2.95)

    box(ax, 1.4, 2.40, 1.5, 1.1,
        "Education\n" + r"$\mathbf{n = 83}$" + "\n(5 subreddits)",
        FINAL_BLUE, fontsize=9)
    box(ax, 3.0, 2.40, 1.5, 1.1,
        "Career\n" + r"$\mathbf{n = 235}$" + "\n(5 subreddits)",
        FINAL_BLUE, fontsize=9)
    box(ax, 4.6, 2.40, 1.5, 1.1,
        "Finance\n" + r"$\mathbf{n = 287}$" + "\n(4 subreddits)",
        FINAL_BLUE, fontsize=9)

    # Auxiliary note
    box(ax, 3.0, 1.20, 5.4, 0.8,
        "Auxiliary: $n = 15$ posts (3 advice subreddits)\n"
        "r/Advice, r/ChronicPain, r/relationship\\_advice",
        STAGE_GREY, fontsize=8)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    plt.close(fig)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
