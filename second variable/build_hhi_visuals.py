"""
build_hhi_visuals.py
====================
Generates static figures (PNG + PDF, 300 dpi) for Variable 2: Cloud Infrastructure
Market Concentration (HHI Analysis), as part of the research paper:

    "To what extent has the growth of cyberattacks and infrastructure disruptions
    across industries outpaced the growth of institutional defensive and regulatory
    capacity?" (2015–2025)

Data source: Manually compiled from Synergy Research Group quarterly press releases
(srgresearch.com/articles). See data/cloud_hhi.csv for per-row source notes.

Figures produced:
    Fig 1 — Dual-axis: HHI (left) + CR3 combined share (right), 2017–2024
    Fig 2 — Individual provider market share trends, 2017–2024 (stacked area)

Output: outputs/fig_hhi_dual_axis.png/.pdf
        outputs/fig_provider_shares.png/.pdf

Author: [Your name]
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
import os

# ── Config ─────────────────────────────────────────────────────────────────────
DATA_PATH   = "data/cloud_hhi.csv"
OUTPUT_DIR  = "outputs"
DPI         = 300

# Palette
C_HHI       = "#1A3A5C"   # deep navy — HHI line
C_CR3       = "#2A7D5F"   # forest green — CR3 area
C_AWS       = "#E07B39"   # amber — AWS
C_AZURE     = "#3A78C9"   # blue — Azure
C_GCP       = "#4CAF7D"   # teal-green — GCP
C_ANNOT     = "#B5432A"   # rust — 2024 reclassification annotation
C_GRID      = "#DDDDDD"
C_BG        = "#FAFAFA"

FONT_TITLE  = {"fontsize": 13, "fontweight": "bold", "color": "#1A1A2E"}
FONT_LABEL  = {"fontsize": 10, "color": "#333333"}
FONT_TICK   = {"labelsize": 9,  "labelcolor": "#444444"}

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Load data ──────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)

# ── Figure 1: Dual-axis HHI + CR3 ─────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(10, 5.5))
fig.patch.set_facecolor(C_BG)
ax1.set_facecolor(C_BG)

# HHI line (left axis)
ax1.plot(df["year"], df["hhi"], color=C_HHI, linewidth=2.5,
         marker="o", markersize=6, zorder=3, label="HHI (Big Three)")
ax1.fill_between(df["year"], df["hhi"].min() - 50, df["hhi"],
                 alpha=0.07, color=C_HHI)

# CR3 area (right axis)
ax2 = ax1.twinx()
ax2.fill_between(df["year"], df["cr3_combined"], alpha=0.18,
                 color=C_CR3, zorder=1)
ax2.plot(df["year"], df["cr3_combined"], color=C_CR3, linewidth=2.0,
         linestyle="--", marker="s", markersize=5, zorder=3, label="CR3 Combined Share (%)")

# 2024 reclassification annotation
ax1.annotate(
    "†Azure reclassification\n(Synergy, 2024)",
    xy=(2024, df.loc[df["year"] == 2024, "hhi"].values[0]),
    xytext=(2022.7, 1530),
    fontsize=7.5, color=C_ANNOT,
    arrowprops=dict(arrowstyle="->", color=C_ANNOT, lw=1.2),
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C_ANNOT, alpha=0.85)
)

# Axes formatting
ax1.set_xlabel("Year", **FONT_LABEL)
ax1.set_ylabel("HHI (Σ share²)", **FONT_LABEL)
ax2.set_ylabel("Big Three Combined Share (%)", **FONT_LABEL)
ax1.set_xlim(2016.5, 2024.5)
ax1.set_ylim(1100, 1850)
ax2.set_ylim(40, 80)
ax1.set_xticks(df["year"])
ax1.tick_params(axis="both", **FONT_TICK)
ax2.tick_params(axis="y", **FONT_TICK)
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x)}%"))
ax1.grid(axis="y", color=C_GRID, linewidth=0.6, linestyle="--", alpha=0.7)
ax1.set_axisbelow(True)

# Legend
patch_hhi  = mpatches.Patch(color=C_HHI, label="HHI — Big Three (left axis)")
patch_cr3  = mpatches.Patch(color=C_CR3, label="CR3 Combined Share (right axis)")
ax1.legend(handles=[patch_hhi, patch_cr3], loc="upper left",
           fontsize=8.5, framealpha=0.9)

ax1.set_title(
    "Cloud Infrastructure Market Concentration, 2017–2024\n"
    "Herfindahl-Hirschman Index (HHI) and Big Three Combined Share (CR3)",
    **FONT_TITLE, pad=12
)
fig.text(0.99, 0.01,
         "Source: Synergy Research Group quarterly press releases (srgresearch.com/articles); "
         "Canalys. Compiled by author.\n"
         "†2024 HHI reflects Synergy's reclassification of Azure revenues (IaaS/PaaS → SaaS). "
         "See methodology note.",
         ha="right", va="bottom", fontsize=6.5, color="#666666",
         wrap=True)

plt.tight_layout(rect=[0, 0.05, 1, 1])
for ext in ["png", "pdf"]:
    fig.savefig(f"{OUTPUT_DIR}/fig_hhi_dual_axis.{ext}",
                dpi=DPI, bbox_inches="tight", facecolor=C_BG)
plt.close(fig)
print("✓ Fig 1 saved: fig_hhi_dual_axis.png / .pdf")

# ── Figure 2: Individual Provider Shares (stacked area) ───────────────────────
fig, ax = plt.subplots(figsize=(10, 5.5))
fig.patch.set_facecolor(C_BG)
ax.set_facecolor(C_BG)

ax.stackplot(
    df["year"],
    df["aws_share"], df["azure_share"], df["gcp_share"],
    labels=["AWS", "Microsoft Azure", "Google Cloud"],
    colors=[C_AWS, C_AZURE, C_GCP],
    alpha=0.85
)

# Dotted line at CR3 total
ax.plot(df["year"], df["cr3_combined"], color="#222222", linewidth=1.2,
        linestyle=":", label="CR3 Total (Big Three combined)", zorder=5)

ax.set_xlabel("Year", **FONT_LABEL)
ax.set_ylabel("Market Share (%)", **FONT_LABEL)
ax.set_xlim(2016.5, 2024.5)
ax.set_ylim(0, 80)
ax.set_xticks(df["year"])
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x)}%"))
ax.tick_params(axis="both", **FONT_TICK)
ax.grid(axis="y", color=C_GRID, linewidth=0.6, linestyle="--", alpha=0.7)
ax.set_axisbelow(True)
ax.legend(loc="upper left", fontsize=8.5, framealpha=0.9)
ax.set_title(
    "Cloud Infrastructure Market Share by Provider, 2017–2024\n"
    "AWS, Microsoft Azure, and Google Cloud Platform (IaaS + PaaS + Hosted Private Cloud)",
    **FONT_TITLE, pad=12
)
fig.text(0.99, 0.01,
         "Source: Synergy Research Group quarterly press releases; "
         "Canalys; holori.com (Synergy-citing). Compiled by author.",
         ha="right", va="bottom", fontsize=6.5, color="#666666")

plt.tight_layout(rect=[0, 0.04, 1, 1])
for ext in ["png", "pdf"]:
    fig.savefig(f"{OUTPUT_DIR}/fig_provider_shares.{ext}",
                dpi=DPI, bbox_inches="tight", facecolor=C_BG)
plt.close(fig)
print("✓ Fig 2 saved: fig_provider_shares.png / .pdf")
print("\nAll outputs written to:", OUTPUT_DIR)
