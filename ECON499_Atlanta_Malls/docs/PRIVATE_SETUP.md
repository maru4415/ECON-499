# Private data setup (for authorized teammates only)

Copy the following files from the separate **PRIVATE** bundle into `data/private/`:

- `Advan_2024_derived_flows.zip` — licensed Advan-derived origin-destination activity.
- `crosswalk_legacy.csv` — spatial mapping derived from legacy boundaries; vintage unverified.
- `panel_legacy.csv` — legacy panel used to recover ACS population field; licensed derivative.

Do **not** commit these files to a public repository. The root `.gitignore` excludes `data/private/` and `outputs/`.

Run `python run_all.py` from repository root. This regenerates restricted `outputs/panel_legacy_RESTRICTED.csv`, coefficients, robustness checks, Huff validation, charts, and geographic coverage diagnostics. All results are provisional.

The optional `2010_block_equal_weight_DIAGNOSTIC_NOT_VALIDATED.csv` is kept in the private bundle. To compare geographic coverage, run:

`python scripts/07_geography_audit.py --diagnostic-crosswalk data/private/2010_block_equal_weight_DIAGNOSTIC_NOT_VALIDATED.csv`

The NHGIS raw zip is not required for normal reruns. Confirm vendor geography and create a population-weighted correspondence before claiming a corrected spatial analysis.
