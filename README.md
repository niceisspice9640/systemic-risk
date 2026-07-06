# Efficiency & Fragility: Measuring Whether Cyber Risk Has Outpaced Institutional Defense
 
**Have cyberattacks and infrastructure disruptions across industries grown faster
than the institutional and regulatory capacity meant to contain them?**
 
This project answers that question empirically, across a 2015–2025 window, using
three independent quantitative analyses drawn entirely from free, publicly
documented data sources. Each analysis stands on its own source and coding rules;
together they test a single thesis — that the efficiency gains driving modern
digital infrastructure are structurally inseparable from the fragility those same
gains create.
 
Built by someone with a **CompTIA Security+** background and a specific interest in
**shared-infrastructure and concentration risk** — the kind of exposure that reaches
across sectors, not just any single industry. The 2025 SK Telecom breach —
where a compromise of shared identity-verification infrastructure cascaded across
downstream services — is a direct illustration of the concentration risk this
project quantifies.
 
---
 
## The three analyses
 
Each lives in its own folder with a full README, reproducible pipeline, and both
print-quality (300dpi) and interactive (Chart.js / HTML) figures.
 
| # | Folder | What it measures | Headline finding |
|---|--------|------------------|------------------|
| 1 | [`variable-1-cyberattack-trends/`](./variable-1-cyberattack-trends/) | Cyberattack incidence & sectoral distribution over time (EuRepoC) | Incident frequency rises across the window; a Feb-2023 inclusion-rule change is flagged and reported both raw and rule-adjusted so growth isn't overstated |
| 2 | [`variable-2-cloud-concentration/`](./variable-2-cloud-concentration/) | Market concentration of cloud infrastructure (CR3 / HHI) | Top-3 provider share rose from ~51% (2017) to ~66% (2023); HHI up ~30.7% — measurable consolidation into fewer points of failure |
| 3 | [`variable-3-cascade-heatmap/`](./variable-3-cascade-heatmap/) | Cross-sector spread of supply-chain / platform incidents (12 incidents × 8 sectors) | Mean sectors hit per incident rises from 3.17 to 4.5 across a mid-2023 demarcation; IT/Cloud is implicated in all 12 |
 
> The three are reported **side by side, not merged into a single composite score.**
> Keeping them separate means each finding rests on its own transparent, auditable
> source rather than on weighting choices that would be hard to defend.
 
---
 
## Anchor cases
 
The quantitative work is grounded in three real infrastructure failures, each
illustrating a distinct failure mode the analyses measure:
 
- **2022 Kakao data-center fire** — a single-point-of-failure outage traced to a
  lithium-ion battery fire in an SK C&C UPS facility. The governance failure was
  concentration *without redundancy*, not capacity mismanagement.
- **2025 SK Telecom breach** — a compromise of shared identity-verification
  infrastructure that cascaded across dependent services. A clear example of how
  reliance on centralized verification exposes any organization downstream of it.
- **Canvas / Instructure ransomware** — centralized-platform risk realized across
  the education sector and beyond.
---
 
## Methodology & framing
 
**Efficiency–fragility tradeoff.** The organizing thesis is that efficiency and
fragility are two faces of the same structural change: consolidation, shared
infrastructure, and tight coupling lower cost and raise throughput while widening
the blast radius of any single failure. AI is treated as *one contributing factor*
that accelerates this dynamic — notably the mid-2023 proliferation of adversarial
tooling — rather than as the primary explanatory mechanism.
 
**Inclusion criterion.** What earns a factor a place in the analysis is not that
it involves technology, but that it operates through the specific causal
mechanisms under study — single-point-of-failure and cascade dynamics, and cloud
concentration. This is why natural disasters, geopolitical conflict, and labor
strikes are excluded: they may disrupt tech systems, but not through those
mechanisms.
 
**Intellectual honesty over quiet omission.** Data limitations are stated
explicitly rather than absorbed silently — the EuRepoC rule-change flag, the
interpolated 2018–2021 cloud-share years, paywalled Uptime Institute data, and
sparse cascade rows that reflect *potential* rather than *realized* spread are all
documented in-line in the relevant folder.
 
**Robustness.** Because the three analyses are reported separately rather than
combined, each claim is checked against its own most plausible objection rather
than through a single aggregate test: the EuRepoC series is reported both raw and
rule-adjusted around the Feb-2023 inclusion change; the Variable 3 cascade finding
is tested against alternative demarcation dates; and the interpolated 2018–2021
cloud-share years are compared against the observed endpoints they bridge.
 
---
 
## Tech stack
 
- **Python** — pandas, matplotlib, statsmodels, openpyxl; pipelines split into
  cleaning and visualization stages
- **Excel** — multi-sheet analysis workbooks (Data / regression / findings) with
  cross-sheet formulas, LibreOffice-compatible
- **Web** — Chart.js interactive figures now; a D3.js interactive site is planned
- **Output discipline** — every figure produced at 300dpi for print *and* as
  standalone interactive HTML for the web
---
 
## Data sources & licensing
 
- **EuRepoC Global Dataset of Cyber Incidents** v1.3.2 — Zenodo,
  DOI [10.5281/zenodo.14965395](https://doi.org/10.5281/zenodo.14965395),
  **CC BY-NC 4.0** (attribution, non-commercial).
- **Cloud market share** — Synergy Research Group quarterly releases and Canalys.
- **Cascade incidents** — compiled from public incident reporting, with a
  conservative rule requiring explicit public confirmation before a sector is
  coded as affected.
Per-source licensing notes and full citations live in each variable's own README
and `LICENSE`. FBI IC3, Verizon DBIR, and IBM/Ponemon were evaluated but are used
only as supporting context — they measure loss and breach detail rather than
incident frequency, and several are registration-gated rather than openly
redistributable.
