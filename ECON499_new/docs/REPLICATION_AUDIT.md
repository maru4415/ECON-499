# Audit of the previously generated analysis

- The previous analysis code was inspected from the supplied completed research ZIP. Its `run_models.py` uses **absolute paths** and a 2026-release ZCTA file to intersect 2024 Georgia block groups; this is **provisional**, not a confirmed source-CBG vintage match.
- The alternative NHGIS method aggregates a 2010-block→2020-ZCTA crosswalk using **equal block counts**, not population weighting; this is diagnostic only.
- The previous full-panel construction uses `fillna(0)` for missing origin records, explicitly noted as a diagnostic imputation. This may bias estimates under origin truncation.
- The first source file contains 95,803 origin records, but exactly 2,000 records for each destination-month except January Greenbriar (1,803); this is consistent with possible reporting caps but does not prove the provider's rule.
- Previous annual mall device totals are **monthly sums**, not de-duplicated annual unique visitors.
- Previously supplied model outputs and plots were copied into `results/` for reference, **not independently re-estimated in this packaging step**. Numbered notebooks provide portable re-estimation paths once original inputs are placed in `data/private/`.
- Pair model formulas in notebook 03 are transparent reconstructed specifications; check against `scripts/original_lenox_greenbriar_comparison.py` before claiming bit-for-bit identity. Some results can differ due to model formulation, sample and library version.
- `p` values with only 24–25 origin clusters are fragile. Neither race/ethnicity shares nor income identify individual shoppers or preferences.
- The current project **cannot** estimate before/after construction impacts because the assembled Dewey data covers only 2024.
