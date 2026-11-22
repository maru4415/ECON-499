# ECON 499 — Atlanta Mall Accessibility and Observed Activity (2024)

**Team repository — public/shareable version.** Destinations: **Lenox Square, Phipps Plaza, Ponce City Market**.

## Start here

1. Open `docs/FINAL_RESEARCH_REPORT.md` for the English report and interpretation.
2. Inspect `data/public/` for ACS-derived ZCTA covariates and manually collected Google Maps distances.
3. Inspect `results/` and `figures/` for the **reproduced provisional** model estimates and visuals.
4. Install `pip install -r requirements.txt`.
5. If authorized to use the licensed Advan data, privately obtain the separate data bundle, place its files into `data/private/`, then run `python run_all.py`.
6. Generated restricted panels and derived outputs appear in `outputs/` (gitignored). Do not upload them publicly without checking the data license.

## Project stages

| Stage | Code | Purpose |
|---|---|---|
| 1 | `scripts/01_validate_inputs.py` | Input coverage and validation |
| 2 | `scripts/02_build_legacy_panel.py` | 24-ZCTA × 3-destination × 12-month panel (restricted derivative) |
| 3 | `scripts/03_gravity_models.py` | PPML gravity, sorting, controls |
| 4 | `scripts/04_robustness.py` | Time-split and leave-one-origin-out sensitivity |
| 5 | `scripts/05_huff_choice.py` | Choice model, holdout, historical baseline, scenarios |
| 6 | `scripts/06_figures.py` | Reproducible charts |
| 7 | `scripts/07_geography_audit.py` | Crosswalk origin coverage and optional diagnostic |

## Key provisional findings

Legacy gravity distance coefficient: **−1.027**; 2010 equal-block **diagnostic**: **−0.445**. The diagnostic is NOT a validated replacement. Legacy Huff distance+income holdout MAE: **6.03 percentage points**, versus historical origin-share baseline **3.26 pp**. The latter predicts better.

## Critical limitations

- The Advan source reports activity associated with **destination CBGs containing malls**, not verified mall-specific footfall.
- Provider documentation cites **2010 CBG vintage**; the legacy crosswalk uses newer geographic boundaries. A matching numeric GEOID does not establish geometric compatibility.
- A 2010 NHGIS equal-block proxy was used only to diagnose sensitivity; it lacks 2010 population weights.
- Distance associations and counterfactual simulations are **not causal estimates**.
- Only 23 of 24 study ZCTAs have complete income for baseline regressions.
- The 2010 diagnostic captures fewer origins; do not treat its coefficient as the corrected estimate.

## Data provenance

- Advan Research, *Neighborhood Patterns Plus (2010 CBG Vintage)*, distributed via Dewey Data, DOI: https://doi.org/10.82551/HYH5-PC45 (licensed source, **not distributed in this public repository**).
- US Census Bureau, ACS 2024 five-year ZCTA-level tables (including B19013 and B19083).
- Manually collected Google Maps driving routes (snapshot, not live traffic).
- NHGIS 2010 census block → 2020 ZCTA crosswalk, used only for the separate equal-block geographic diagnostic.

See `docs/PRIVATE_SETUP.md` and `docs/GEOGRAPHY_LIMITATIONS.md`.

## Jupyter walkthrough

Open [`notebooks/ECON499_Complete_Research_Walkthrough.ipynb`](notebooks/ECON499_Complete_Research_Walkthrough.ipynb) for a step-by-step, student-written explanation with runnable code, figures, results, and limitations. Public sections work without licensed data; private model cells require authorized inputs.


## Illustrated research notebook

Start with [`notebooks/ECON499_Complete_Research_Walkthrough.ipynb`](notebooks/ECON499_Complete_Research_Walkthrough.ipynb): an executed, English-language walkthrough with 18 charts embedded for GitHub preview. Graph PNGs are also in `figures/notebook/`.
