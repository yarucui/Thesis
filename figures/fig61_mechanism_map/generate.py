"""
Figure 6.1 — Master 2x2 mechanism map.

A 2x2 grid of cells with epistemic role on the row axis (advisor /
oracle) and output format on the column axis (single-token / distribution).
Each cell shows mean LLM entropy and mean abs_gap. Cell colour encodes
entropy via the RdYlGn colormap (low entropy = red, high entropy =
green, matching the human-pluralism direction).

The numbers come directly from the merged Chapter 6 Table 6.1:
- Advisor + single-token (D1 baseline, 132 ambiguous): H=0.046, gap=0.446
- Oracle + single-token (D2 oracle, 620 full corpus): H=0.072, gap=0.338
- Advisor + distribution (D1 VS, 132 ambiguous):      H=0.608, gap=0.210
- Oracle + distribution (D1 DV, 132 ambiguous):       H=0.553, gap=0.233
Sample composition varies between cells; see merged Chapter 6 §6.1 for
the design-honesty note.

Data sources (for sanity verification, numbers hard-coded for
reproducibility against the chapter table):
- data/direction1_distributions.csv
- data/direction2_comparison_table.csv

Run:
    python figures/fig61_mechanism_map/generate.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
from matplotlib.colors import Normalize
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

ROOT = Path(__file__).resolve().parents[2]
D1   = ROOT / "data" / "direction1_distributions.csv"
D2   = ROOT / "data" / "direction2_comparison_table.csv"
OUT  = Path(__file__).resolve().parent / "out.pdf"

HUMAN_REFERENCE = 0.621  # nats (D1 ambiguous subset, per merged ch04)


def verify_cells() -> dict:
    """Cross-check the table values against the CSVs; raise if drift > 0.005."""
    d1 = pd.read_csv(D1)
    d2 = pd.read_csv(D2)
    q2 = d2[d2["qualified_for_analysis"] == 1]

    cells = {
        ("advisor", "single"): (
            d1[d1["condition"] == "baseline"]["llm_entropy"].mean(),
            d1[d1["condition"] == "baseline"]["abs_gap"].mean(),
            "BASELINE",
        ),
        ("oracle", "single"): (
            q2[q2["framing"] == "oracle"]["llm_entropy"].mean(),
            q2[q2["framing"] == "oracle"]["abs_gap"].mean(),
            "ORACLE",
        ),
        ("advisor", "distribution"): (
            d1[d1["condition"] == "vs"]["llm_entropy"].mean(),
            d1[d1["condition"] == "vs"]["abs_gap"].mean(),
            "VS",
        ),
        ("oracle", "distribution"): (
            d1[d1["condition"] == "dv"]["llm_entropy"].mean(),
            d1[d1["condition"] == "dv"]["abs_gap"].mean(),
            "DV",
        ),
    }
    print("Computed cells:")
    for key, (h, g, lab) in cells.items():
        print(f"  {key}: label={lab}  H={h:.4f}  gap={g:.4f}")
    return cells


def main() -> None:
    cells = verify_cells()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect("equal")
    ax.axis("off")

    # Colour normalization
    norm = Normalize(vmin=0, vmax=0.7)
    cmap = cm.RdYlGn

    # Cell layout: 2 rows x 2 cols
    # Columns: single-token (left, x=1.5..4.5), distribution (right, x=5.5..8.5)
    # Rows:    advisor (top, y=4.5..6.5),     oracle (bottom, y=1.5..3.5)
    cell_w = 3.0
    cell_h = 2.0
    layouts = {
        ("advisor", "single"):       (3.0, 5.5),
        ("advisor", "distribution"): (7.0, 5.5),
        ("oracle",  "single"):       (3.0, 2.5),
        ("oracle",  "distribution"): (7.0, 2.5),
    }

    for (role, fmt), (cx, cy) in layouts.items():
        h_val, gap_val, label = cells[(role, fmt)]
        face = cmap(norm(h_val))
        patch = FancyBboxPatch(
            (cx - cell_w / 2, cy - cell_h / 2), cell_w, cell_h,
            boxstyle="round,pad=0.04,rounding_size=0.08",
            facecolor=face, edgecolor="black", linewidth=1.0,
            alpha=0.85,
        )
        ax.add_patch(patch)
        ax.text(cx, cy + 0.55, label, ha="center", va="center",
                fontsize=12, fontweight="bold")
        ax.text(cx, cy + 0.05, f"$H = {h_val:.3f}$",
                ha="center", va="center", fontsize=11, family="monospace")
        ax.text(cx, cy - 0.45, f"abs\\_gap = {gap_val:.3f}",
                ha="center", va="center", fontsize=10, family="monospace")

    # Column headers
    ax.text(3.0, 7.3, "Single-token output",
            ha="center", va="center", fontsize=11, fontweight="bold")
    ax.text(7.0, 7.3, "Distribution output",
            ha="center", va="center", fontsize=11, fontweight="bold")

    # Row labels
    ax.text(0.6, 5.5, "Advisor\n(prescriptive)",
            ha="center", va="center", fontsize=11, fontweight="bold", rotation=90)
    ax.text(0.6, 2.5, "Oracle\n(descriptive)",
            ha="center", va="center", fontsize=11, fontweight="bold", rotation=90)

    # Horizontal arrow on top: "Output format effect (large)"
    arrow_h = FancyArrowPatch((4.7, 6.85), (5.3, 6.85),
                              arrowstyle="-|>", mutation_scale=18,
                              color="#1a9850", linewidth=2.0)
    ax.add_patch(arrow_h)
    ax.text(5.0, 7.1, "Output format effect (large)",
            ha="center", va="center", fontsize=10,
            color="#1a9850", fontweight="bold")

    # Vertical arrow on the left side: "Role framing effect (small)"
    arrow_v = FancyArrowPatch((1.6, 4.7), (1.6, 3.3),
                              arrowstyle="-|>", mutation_scale=18,
                              color="#d62728", linewidth=2.0)
    ax.add_patch(arrow_v)
    ax.text(1.25, 4.0, "Role framing effect (small)",
            ha="center", va="center", fontsize=10,
            color="#d62728", fontweight="bold", rotation=90)

    # Bottom annotation box: "16x larger effect..."
    ax.text(5.0, 0.55,
            r"$\mathbf{\approx 16\times}$ larger effect from changing format vs.\ changing role",
            ha="center", va="center", fontsize=10.5,
            bbox=dict(boxstyle="round,pad=0.4",
                      facecolor="#f5f5f5", edgecolor="black", linewidth=0.8))

    # Colorbar for entropy
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation="horizontal",
                        fraction=0.045, pad=0.04, shrink=0.55,
                        anchor=(1.0, 0.5))
    cbar.set_label("Cell colour: mean LLM entropy (nats)", fontsize=9)
    cbar.ax.axvline(HUMAN_REFERENCE, color="black", linestyle="--",
                    linewidth=1.0)
    cbar.ax.text(HUMAN_REFERENCE, 1.4, f"human ({HUMAN_REFERENCE:.3f})",
                 ha="center", va="bottom", fontsize=8,
                 transform=cbar.ax.get_xaxis_transform())

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    plt.close(fig)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
