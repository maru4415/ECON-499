# Variable dictionary

| Variable | Unit / construction | Interpretation | Caveat |
|---|---|---|---|
| `ZCTA` | 5-digit string | Origin ZIP Code Tabulation Area | ZCTA is not identical to USPS ZIP |
| `Mall` | 4 categories | Destination mall-containing CBG | CBG contains non-mall activity |
| `Month` | 1–12 | 2024 calendar month | Only one year |
| `Origin_CBG` | 12-digit string | Reported home Census Block Group | Geographic vintage unresolved |
| `Origin_Device_Count` | reported device-origin count | Device home-area contribution to destination CBG | Not visits, shoppers or dollars |
| `weight` | CBG→ZCTA allocation weight | Share of source CBG assigned to a ZCTA | Area-based or equal-block approximation, provisional |
| `flow` | allocated origin count | Sum of `Origin_Device_Count × weight` | Fractional estimates, not direct observation |
| `unreported_origin_cell` | boolean | No mapped record for origin × mall × month | Not a true zero |
| `income` | 2024 ACS 5-year dollars | Median household income, B19013_001E | 1 ZCTA missing in existing analysis |
| `gini` | 0–1 | Income inequality, B19083_001E | ACS sampling uncertainty |
| `population` | residents | Total population, B01003_001E | Community, not shoppers |
| `black_share` | 0–1 | Non-Hispanic Black share, B03002_004E / population | Area composition, not visitor identity |
| `hispanic_share` | 0–1 | Hispanic/Latino share, B03002_012E / population | Area composition, not visitor identity |
| `white_share` | 0–1 | Non-Hispanic White share, B03002_003E / population | Area composition, not visitor identity |
| `miles` | driving miles | Representative origin-to-destination Google Maps route | Not actual traveler route |
| `log_distance` | ln(1+miles) | Nonlinear distance term | Coefficient not constant miles elasticity |
| `log_income` | ln(income) | Income transformation | Income must be positive |
| `log_population` | ln(population) | Population scale adjustment | Population must be positive |
| `Buckhead` | 0/1 | Lenox or Phipps | Mall group comparison |
| `Lenox` | 0/1 | Lenox vs Greenbriar pair | Used only in pair models |

## Core observation
One row in the analysis panel = **one origin ZCTA × one destination mall-area CBG × one month**. Full panel = 25 × 4 × 12 = **1,200 rows**. Some model samples contain fewer rows because income is missing for one ZCTA.
