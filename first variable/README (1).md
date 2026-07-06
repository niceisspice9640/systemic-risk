# Cyberattack Incidence Trends (EuRepoC, 2015–2024)

A data pipeline and analysis project examining whether the growth of cyberattacks
and infrastructure disruptions across industries has outpaced institutional
defensive and regulatory capacity (study window: 2015–2025).

This is the first of three independent quantitative analyses in that project. It
measures the frequency and sectoral distribution of cyber incidents over time
using the EuRepoC Global Dataset, with an emphasis on reproducibility and
transparent methodology. The three analyses are reported side by side rather
than merged into a single composite score, so that each rests on its own
clearly documented source and coding rules.

> **Status:** complete. This analysis (cyberattack incidence, EuRepoC) is
> finished; the two companion analyses — cloud market concentration (HHI) and
> the cross-sector cascade heatmap — are maintained in their own directories.

## The three quantitative analyses

| # | Analysis | Source | Status |
|---|----------|--------|--------|
| 1 | Cyberattack incidence & sectoral distribution | [EuRepoC Global Dataset of Cyber Incidents](https://eurepoc.eu/) | ✅ Complete |
| 2 | Cloud market concentration (CR3 / HHI) | Synergy Research Group / Canalys market share | ✅ Complete |
| 3 | Cross-sector cascade heatmap | Compiled supply-chain / platform incidents × sectors | ✅ Complete |

FBI IC3, Verizon DBIR, and IBM/Ponemon were evaluated and are cited (if at all)
only as supporting context: they measure financial loss and breach detail
rather than incident frequency, and several are registration-gated rather than
openly redistributable.

## Repository structure

```
eurepoc-cyberattack-trends/
├── data/
│   ├── raw/          # Original source dataset (unmodified)
│   └── processed/    # Cleaned + aggregated outputs from the scripts
├── scripts/
│   ├── clean_eurepoc.py    # Raw EuRepoC CSV -> cleaned, flagged, aggregated
│   └── build_visuals.py    # Processed CSVs -> static + interactive figures
├── figures/
│   ├── static/       # 300dpi PNG + PDF (for the academic paper)
│   └── interactive/  # Standalone HTML (Chart.js, for the website)
├── output/           # Human-readable Excel summary workbook
├── requirements.txt
└── README.md
```

## Reproducing the analysis

```bash
# 1. install dependencies
pip install -r requirements.txt

# 2. clean and aggregate the raw EuRepoC data
cd scripts
python clean_eurepoc.py

# 3. generate all figures (static PNG/PDF + interactive HTML)
python build_visuals.py
```

`clean_eurepoc.py` reads `data/raw/eurepoc_global_dataset_1_3.csv` and writes the
processed CSVs to `data/processed/`; `build_visuals.py` reads those and writes
static figures to `figures/static/` and interactive HTML to
`figures/interactive/`. Both scripts resolve paths relative to their own
location, so they run out of the box from the repo root (`python
scripts/clean_eurepoc.py`) or from inside `scripts/` — no path editing needed.

## Key methodological decisions

The cleaning pipeline encodes several deliberate choices, each documented in the
`Cleaning_Log` sheet of the Excel summary and in code comments:

1. **Study window 2015–2024.** 2025 requires a separate provisional pull from
   EuRepoC's TableView (not yet expert-reviewed).
2. **85 incidents dropped** for having no usable date in either `start_date` or
   `end_date`.
3. **February 2023 rule-change flag.** EuRepoC expanded its inclusion criteria in
   Feb 2023 to capture critical-infrastructure incidents regardless of initiator.
   Incidents qualifying *only* under this rule are flagged (`ci_only_post2023_rule`);
   ~24% of the windowed dataset carries the flag, concentrated in 2023–2024
   (≈39% and 43% of those years). The trend is reported both raw and
   rule-adjusted as a sensitivity check — the raw series materially overstates
   2023–2024 growth.
4. **Receiver-category deduplication.** EuRepoC's receiver data repeats one row
   per affected country, so a single multi-country incident can dominate a
   year's sector totals (one 2022 espionage campaign alone accounted for 54% of
   that year's raw "critical infrastructure" tag count). Each incident is counted
   once per distinct category.

## Data sources & licensing

- **EuRepoC Global Dataset of Cyber Incidents** v1.3.2 — Zenodo,
  DOI [10.5281/zenodo.14965395](https://doi.org/10.5281/zenodo.14965395),
  licensed **CC BY-NC 4.0**. The raw dataset in `data/raw/` is redistributed
  here under those terms (attribution, non-commercial). If you fork this repo
  for any commercial purpose, you must remove the raw dataset and obtain it
  directly from EuRepoC under appropriate terms.

See [`LICENSE`](LICENSE) for this project's own code license and important
notes on the data license.
