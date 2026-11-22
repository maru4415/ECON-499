# File index

- `README.md`: project purpose, run instructions, provenance, warnings.
- `run_all.py`: one-command reproducibility pipeline (requires licensed private inputs).
- `scripts/00_public_data_summary.py`: standalone public data check.
- `scripts/01_validate_inputs.py`: input audit.
- `scripts/02_build_legacy_panel.py`: provisional 2024 origin-to-destination panel.
- `scripts/03_gravity_models.py`: PPML regression specifications.
- `scripts/04_robustness.py`: temporal and leave-one-origin sensitivity.
- `scripts/05_huff_choice.py`: calibrated Huff choice, holdout and scenario.
- `scripts/06_figures.py`: charts.
- `scripts/07_geography_audit.py`: crosswalk coverage diagnostic.
- `scripts/common.py`: common paths and data loading.
- `data/public/`: 2024 ACS-derived tables and 72 Google Maps driving routes.
- `results/`: shareable aggregate regression coefficients, validation and sensitivity tables.
- `figures/`: summary charts.
- `docs/FINAL_RESEARCH_REPORT.md` and `.html`: English working paper.
- `docs/GEOGRAPHY_LIMITATIONS.md`: vintage mismatch and sensitivity caveats.
- `docs/PRIVATE_SETUP.md`: authorized access to separately delivered licensed inputs.

**Restricted:** raw/derived Advan flows, source crosswalk, origin panels and equal-block diagnostic are in a separate private package, not this public ZIP. Results are provisional.

- `notebooks/ECON499_Complete_Research_Walkthrough.ipynb` — complete Markdown + code research narrative.
