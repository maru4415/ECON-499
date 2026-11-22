# ECON 499 — Atlanta Mall Accessibility and Observed Activity

**Final reproducibility and geographic-vintage audit (22 November 2026)**

## Executive summary

This study compares **Lenox Square, Phipps Plaza, and Ponce City Market** using 2024 Advan Neighborhood Patterns Plus-derived activity, 2024 ACS five-year ZCTA socioeconomic variables, and manually collected Google Maps driving distances. The current empirical results are **provisional** because the Advan product citation says *2010 CBG Vintage*, while the legacy geographic overlay uses 2024 Georgia block-group and 2026 ZCTA geometry. A 2010 NHGIS block-to-2020-ZCTA crosswalk was available locally and was used to create a **diagnostic, equal-block approximation**, not a validated replacement.

**Central finding:** The legacy gravity specification estimates a negative distance coefficient of **-1.027** (cluster SE 0.083), while the 2010-based diagnostic gives **-0.445** (SE 0.181). The sign is stable, but magnitude and origin coverage are sensitive to geography. Do not report a single coefficient as geographically validated.

## Research questions

1. How is driving distance associated with observed origin-to-destination activity around three Atlanta shopping destinations?
2. Are ZIP-level income and socioeconomic characteristics associated with the observed activity after controlling for distance and population?
3. Can a calibrated Huff-style choice model predict relative activity shares, and how does it compare with a simple historical-share baseline?

## Data and interpretation

- **Activity:** 2024 Advan Neighborhood Patterns Plus derived CBG origin counts to three *destination CBGs*, not verified mall entrance counts or mall-specific visits. Each destination CBG may contain non-mall activity.
- **Geography:** The provider citation indicates 2010 CBG vintage; the legacy overlay used 2024 CBG and 2026 ZCTA geometry. The diagnostic uses NHGIS 2010 census blocks to 2020 ZCTAs.
- **Covariates:** ACS 2024 five-year ZCTA income, Gini and selected controls; 24 study ZCTAs, with one excluded from complete-case income regressions (23 clusters). Distance is user-collected Google Maps driving miles, not a randomized treatment.
- **Interpretation:** Associations and hypothetical share simulations only; no causal effect of a mall's construction, renovation or distance reduction is identified.

## Geographic coverage audit

| Metric | Legacy crosswalk | 2010 NHGIS diagnostic |
|---|---:|---:|
| Distinct origin CBG IDs in entire flow export | 11,786 | 11,786 |
| Origin IDs matched to selected 24 ZCTAs | 575 | 242 |
| Origin device counts allocated to study ZCTAs | 27.05% | 8.75% |
| Model panel rows | 864 | 864 |
| Panel rows with positive allocated activity | 864 | 827 |

**Important:** The denominator includes all origins in the provider's export, including origins outside Georgia and outside the selected Atlanta ZCTAs. Thus these fractions are **study-area capture**, not an error rate. The change between scenarios is still large and demonstrates that the vintage question matters. The diagnostic assumes equal weight per 2010 census block when aggregating the NHGIS block-level interpolation to a CBG. This assumption is not supported as a population-accurate CBG allocation without 2010 block population counts, so these estimates must not replace the legacy coefficients as definitive results.

## Gravity and sorting models

Baseline PPML specification: `flow ~ log(1 + driving_miles) + log(income) + log(population) + destination fixed effects + month fixed effects`. Standard errors clustered by origin ZCTA.

| Estimate | Legacy | 2010 diagnostic |
|---|---:|---:|
| Distance, baseline | -1.027 | -0.445 |
| Cluster SE for distance | 0.083 | 0.181 |
| Income, baseline | 0.258 | 0.141 |
| Income, full controls | 0.091 | 0.216 |

The negative distance association survives both geographic scenarios, but the numerical size is not stable. The legacy income estimate is modest and borderline under conventional inference; it is not statistically robust to the full set of controls. The full-controls coefficients in the diagnostic are especially sensitive to changed spatial allocations and should not be interpreted substantively. The sorting specification includes origin fixed effects and an income × Buckhead-mall indicator; its interaction estimate is not robustly distinguishable from zero.

![Distance sensitivity](distance_sensitivity.png)

## Robustness checks

Re-estimated baseline gravity models using January–October, November–December, and leave-one-origin-ZCTA-out samples. Legacy leave-one-origin distance coefficients range from **-1.083 to -0.982**; the 2010 diagnostic ranges from **-0.646 to -0.334**. Within-scenario sample stability does not resolve between-scenario geographic uncertainty. Full tables are in `model_comparison.csv`.

## Huff-style destination shares

Using January–September for calibration and October–December for holdout, the **legacy distance + income** model achieves **6.03 percentage points MAE**, compared with **3.26 pp** for a simple historical average of each origin's destination shares. Thus the calibrated Huff model **does not beat** the historical baseline on this holdout. This is a key limitation, not a success claim.

The legacy counterfactual mechanically reduces driving distance to one mall by 20%, holding other variables fixed. Its own predicted share increases by approximately **3.65–4.28 percentage points**, depending on the mall. These are model-implied scenarios, not causal effects or real-world policy forecasts. See `huff_counterfactual_legacy.csv`.

![Holdout comparison](huff_holdout.png)

## Limitations and next requirements

1. **Confirm provider origin CBG vintage from exact purchased partition metadata**, rather than assuming the citation alone describes all files. This cannot be independently resolved from the local derived export.
2. If confirmed 2010, **aggregate the 2010 block-to-ZCTA NHGIS crosswalk with 2010 block population weights** or use an authoritative 2010 CBG → 2020 ZCTA population-weighted correspondence. The equal-block proxy is not a substitute.
3. Check whether ACS 2024 ZCTA codes and definitions are sufficiently compatible with 2020 ZCTAs; document differences. The legacy use of 2026 ZCTA polygons requires similar scrutiny.
4. The source destination geography is a **CBG containing a mall**, not a mall POI; avoid labeling these as verified mall visits.
5. Device-based activity is subject to sampling and vendor methodology; do not treat counts as a census of shoppers.
6. Study-area selection (24 ZCTAs) excludes origins outside the region; unallocated fractions are not automatically crosswalk errors.
7. Income and demographic attributes are measured at origin ZCTA level, not for individual mall visitors; avoid ecological fallacy.
8. Three destinations and one calendar year cannot identify before/after construction impacts.

## Reproducibility and deliverables

- `run_audit.py`: replays the complete legacy and 2010 diagnostic pipelines using **locally held restricted source files** (not included in the shareable package).
- `origin_coverage_comparison.csv`: capture rates and counts.
- `model_comparison.csv`: PPML estimates and sensitivity checks.
- `huff_validation_*.csv`, `huff_counterfactual_*.csv`: share-model validation and scenarios.
- `panel_*.csv`: **restricted derivative data**, excluded from the public results ZIP.
- `2010_block_equal_weight_DIAGNOSTIC_NOT_VALIDATED.csv`: **restricted diagnostic derivative**, excluded from the public results ZIP.

## Conclusion

The study supports a descriptive finding that greater driving distance is associated with lower observed activity flows to the three mall-containing destination CBGs. The exact elasticity and the interpretation of socioeconomic differences remain uncertain until the geography vintage is reconciled. The calibrated choice model is informative as a simulation, but does not outperform a simple historical-share prediction benchmark. The analysis should be presented as **observational and provisional**, not as a causal or fully geographically harmonized result.
