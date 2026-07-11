"""
build_regression_visual.py
===========================
Generates the OLS regression figure for Variable 2 (Cloud Infrastructure
Concentration). Plots the HHI series with the fitted OLS trend line, its equation
and R-squared, and an annotation carrying the non-parametric trend-test results
(Mann-Kendall + Sen's slope) computed in trend_tests.py.

Design intent:
  - The OLS line is the plotted trend (conventional regression visual).
  - Significance is reported from the Mann-Kendall test (assumption-light,
    appropriate for n=7), NOT from the OLS p-value.
  - Sen's slope is annotated as a number confirming the OLS slope is robust.
  - 2024 is shown as a hollow marker (excluded from the fit; Azure reclassification).

Output: outputs/fig_hhi_regression.png / .pdf  (300 dpi)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

OUTPUT_DIR = "outputs"
DPI = 300
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Palette (matches build_hhi_visuals.py) ─────────────────────────────────────
C_POINT   = "#1A3A5C"   # deep navy — HHI data points (in-fit)
C_EXCL    = "#9BB0C4"   # muted — 2024 excluded point
C_OLS     = "#B5432A"   # rust — OLS regression line
C_BAND    = "#B5432A"   # CI band (same hue, low alpha)
C_GRID    = "#DDDDDD"
C_BG      = "#FAFAFA"
C_ANNOT   = "#1A1A2E"

FONT_TITLE = {"fontsize": 13, "fontweight": "bold", "color": "#1A1A2E"}
FONT_LABEL = {"fontsize": 10, "color": "#333333"}

# ── Data ───────────────────────────────────────────────────────────────────────
# Full series
years_all = np.array([2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])
hhi_all   = np.array([1269, 1307, 1378, 1442, 1531, 1611, 1658, 1485])

# Fit window: 2017–2023 (2024 excluded — Azure reclassification artifact)
years = years_all[:-1]
hhi   = hhi_all[:-1]

# ── OLS fit ────────────────────────────────────────────────────────────────────
ols = stats.linregress(years, hhi)
slope, intercept, r, p_ols = ols.slope, ols.intercept, ols.rvalue, ols.pvalue
r2 = r ** 2

# Fitted line + 95% CI band across the fit window
x_line = np.linspace(2017, 2023, 100)
y_line = intercept + slope * x_line

n = len(years)
dof = n - 2
t_crit = stats.t.ppf(0.975, dof)
resid = hhi - (intercept + slope * years)
s_err = np.sqrt(np.sum(resid**2) / dof)
mean_x = np.mean(years)
ss_x = np.sum((years - mean_x) ** 2)
ci = t_crit * s_err * np.sqrt(1/n + (x_line - mean_x)**2 / ss_x)

# ── Trend-test results (from trend_tests.py) ───────────────────────────────────
TAU        = 1.00
MK_P       = 0.0027
SEN_SLOPE  = 70.00

# ── Figure ─────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(C_BG)
ax.set_facecolor(C_BG)

# 95% CI band
ax.fill_between(x_line, y_line - ci, y_line + ci,
                color=C_BAND, alpha=0.12, zorder=1,
                label="95% CI (OLS)")

# OLS line
ax.plot(x_line, y_line, color=C_OLS, linewidth=2.2, zorder=3,
        label=f"OLS fit:  HHI = {slope:.1f}·year − {abs(intercept):,.0f}")

# In-fit data points
ax.scatter(years, hhi, s=70, color=C_POINT, zorder=5,
           edgecolor="white", linewidth=1.3, label="HHI (2017–2023, in fit)")

# 2024 excluded point (hollow)
ax.scatter([2024], [1485], s=70, facecolor="none", edgecolor=C_EXCL,
           linewidth=1.8, zorder=5, label="2024 (excluded — reclassification)")
ax.annotate("2024\nexcluded",
            xy=(2024, 1485), xytext=(2023.55, 1400),
            fontsize=7.5, color=C_EXCL, ha="center",
            arrowprops=dict(arrowstyle="->", color=C_EXCL, lw=1))

# ── Stats annotation box ───────────────────────────────────────────────────────
stats_text = (
    "$\\bf{OLS\\ fit\\ (2017{-}2023,\\ n=7)}$\n"
    f"Slope (β₁) = {slope:.1f} HHI/year\n"
    f"R² = {r2:.3f}\n"
    "\n"
    "$\\bf{Trend\\ significance}$\n"
    "Mann-Kendall (non-parametric):\n"
    f"  τ = {TAU:.2f},  p = {MK_P:.4f}\n"
    "\n"
    "$\\bf{Slope\\ robustness}$\n"
    f"Sen's slope = {SEN_SLOPE:.0f} HHI/year\n"
    f"(vs OLS {slope:.1f} — close agreement)"
)
ax.text(0.025, 0.97, stats_text,
        transform=ax.transAxes, fontsize=8.6, va="top", ha="left",
        family="monospace", color=C_ANNOT,
        bbox=dict(boxstyle="round,pad=0.55", fc="white",
                  ec="#C9D4E0", lw=1.2, alpha=0.95))

# Footnote on why MK, not OLS p
ax.text(0.975, 0.06,
        "Significance reported from Mann-Kendall, not the OLS p-value:\n"
        "at n=7 the OLS p relies on normality/independence assumptions a short\n"
        "series cannot certify. Mann-Kendall is assumption-light and standard for\n"
        "small annual series. τ=1.00 indicates a perfectly monotonic increase.",
        transform=ax.transAxes, fontsize=6.6, va="bottom", ha="right",
        color="#777777", style="italic")

# ── Axes ───────────────────────────────────────────────────────────────────────
ax.set_xlabel("Year", **FONT_LABEL)
ax.set_ylabel("HHI (Σ market share²  — Big Three)", **FONT_LABEL)
ax.set_xlim(2016.5, 2024.5)
ax.set_ylim(1150, 1750)
ax.set_xticks(years_all)
ax.tick_params(labelsize=9, labelcolor="#444444")
ax.grid(axis="both", color=C_GRID, linewidth=0.6, linestyle="--", alpha=0.7)
ax.set_axisbelow(True)
ax.legend(loc="lower right", fontsize=8, framealpha=0.92, edgecolor="#C9D4E0")

ax.set_title(
    "Cloud Infrastructure Concentration — OLS Trend & Significance Test\n"
    "Herfindahl-Hirschman Index (Big Three), 2017–2023",
    **FONT_TITLE, pad=12
)
fig.text(0.99, 0.005,
         "Source: Synergy Research Group quarterly press releases. "
         "OLS fit and Mann-Kendall / Sen's slope computed in trend_tests.py. "
         "2024 excluded from fit (Azure IaaS/PaaS→SaaS reclassification).",
         ha="right", va="bottom", fontsize=6, color="#888888")

plt.tight_layout(rect=[0, 0.03, 1, 1])
for ext in ["png", "pdf"]:
    fig.savefig(f"{OUTPUT_DIR}/fig_hhi_regression.{ext}",
                dpi=DPI, bbox_inches="tight", facecolor=C_BG)
plt.close(fig)
print("✓ Saved: fig_hhi_regression.png / .pdf")
print(f"  OLS slope={slope:.2f}, R²={r2:.4f}  |  MK τ={TAU}, p={MK_P}  |  Sen={SEN_SLOPE}")
