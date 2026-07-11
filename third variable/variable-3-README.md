# Variable 3 — Cross-Sector Cascade Heatmap

> **Status: Complete.** Maps the cross-sector footprint of major supply-chain and platform
> incidents over time, using strict binary coding across eight sectors.

## Research context

**Research question:** To what extent has the growth of cyberattacks and infrastructure
disruptions across industries outpaced the growth of institutional defensive and regulatory
capacity? (Study window ~2015–2025.)

This is one of four variables. Variables 1–3 measure the **pressure** side of the question
(how attack frequency, structural concentration, and cross-sector cascades have grown);
Variable 4 measures the **capacity** side qualitatively. This module answers the third pressure
question: when a supply-chain or platform incident occurs, does it cascade across *more*
sectors over time?

## What it shows

Twelve high-impact incidents (2020–2026), each coded across eight sectors using a strict
**binary rule**: a cell is filled only where public reporting confirms meaningful sector-level
impact. Cells stay empty where a sector was exposed but no realized cascade was documented, so
the coding under-counts rather than over-counts. A demarcation line marks mid-2023 (public
availability of adversarial AI tooling, WormGPT/FraudGPT); incidents after the line show broader
footprints on average.

## Key findings

| Metric | Result | Note |
|--------|--------|------|
| Mean sectors hit, pre-AI | 3.17 | 6 incidents |
| Mean sectors hit, AI-era | 4.5 | 6 incidents |
| IT/Cloud column | Filled for every incident | Structural throughline of the study |

**Stated up front — illustrative, not causal.** The two widest AI-era rows (MOVEit 8/8,
CrowdStrike 7/8) stem from a zero-day and a faulty update — neither caused by AI. The heatmap
documents that AI-era incidents in this sample have broader footprints; it does **not** establish
that AI caused the broadening. With 12 events in a convenience sample, two outliers move the
average substantially. The causal question is reserved for the paper's discussion.

## Methodology notes

- **Binary over graded coding.** Cells are filled only on confirmed, documented sector-level
  impact, because public sources cannot reliably support magnitude/severity assignments.
- **Conservative coding (flagged).** "Potential-but-unrealized" cascades are left empty
  (Okta, LastPass, Log4j have sparse rows despite high theoretical blast radius). These are
  flagged for a narrative footnote so sparse rows aren't misread as low severity.
- **No Retail column (known limitation).** Coop (Kaseya), Starbucks/grocers (Blue Yonder), and
  pharmacies (Change Healthcare) are retail-adjacent and currently absorbed into Logistics or
  Healthcare; a Retail column would sharpen several rows.
- **SK Telecom handled elsewhere.** It is a *verification-dependency* cascade — a distinct
  typology from the platform-dependency cascades this heatmap captures — so it is treated
  qualitatively rather than coded here.

## Data sources

| Source | Coverage | Type |
|--------|----------|------|
| CISA advisories; government reports (GAO, Congress, US Dept of Education/FSA, NY DFS) | Per-incident | Primary |
| Incident analyses (Mandiant, CrowdStrike, Emsisoft, Volexity) | Per-incident | Primary/secondary |
| Major-press reporting | Per-incident | Secondary |

Full per-cell attribution is in `CODING_RATIONALE.md`. The event database is self-compiled.

## File structure

```
variable-3-cascade-heatmap/
├── data/
│   └── cascade_matrix.csv          # Binary sector-impact coding, one row per event
├── build_cascade_heatmap.py        # Generates the 300dpi PNG/PDF figure
├── outputs/
│   ├── fig_cascade_heatmap.png/.pdf        # Static academic figure
│   └── cascade_heatmap_interactive.html    # Hover-annotated version (open in browser)
├── CODING_RATIONALE.md             # Per-cell sourcing basis + coding-tension notes
├── requirements.txt
└── README.md
```

## How to run

```bash
pip install -r requirements.txt
python build_cascade_heatmap.py    # static PNG/PDF (300dpi) -> outputs/
# cascade_heatmap_interactive.html — open directly in any browser, no server needed
```

## Relation to other variables

| Variable | Phenomenon | Method | Side |
|----------|-----------|--------|------|
| 1 — Cyberattacks | Attack frequency & sector spread | OLS time series | Pressure |
| 2 — Cloud concentration | Structural blast radius | HHI trend analysis | Pressure |
| **3 — Cross-sector cascade** | **Cascade breadth over time** | **Sector-spread heatmap** | **Pressure** |
| 4 — Regulatory capacity | Institutional response speed/scope | Qualitative event study | Capacity |

---
*CompTIA Security+ · Python (pandas, matplotlib) · vanilla HTML/CSS/JS*
