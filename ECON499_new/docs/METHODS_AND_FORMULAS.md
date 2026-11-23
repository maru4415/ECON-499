# Research walkthrough, model equations and interpretation

## 1. Research question
How are **driving distance**, **origin neighborhood socioeconomic conditions**, and **destination type** associated with observed device activity in the census block groups containing four Atlanta shopping destinations during 2024? A special comparison contrasts Lenox Square with Greenbriar Mall. This is **not** a causal study of spending, gentrification, or luxury preferences.

## 2. From raw records to a panel
Dewey reports origin CBG `b` and destination `j` by month `t`. For each geographic scenario, allocate reported origin counts to ZCTA `i`:

$$Y_{ijt}=\sum_b w_{bi} D_{bjt}$$

- `D_bjt`: reported device count from origin CBG `b` to destination mall-containing CBG `j` in month `t`.
- `w_bi`: share of origin CBG `b` assigned to ZCTA `i` by the provisional crosswalk.
- `Y_ijt`: **estimated allocated** device-origin count, not observed purchases.

**Warning:** A missing origin in a top-origin report is not proof of zero travel. Previous full-panel specifications filled unreported cells with zero for diagnosis only. 2020 scenario has zero missing panel cells; 2010 scenario has 78.

## 3. Descriptive comparison
Annual destination-CBG device totals sum 12 monthly counts; they **do not count unique people across the year**. Lenox 4,072,231 vs Greenbriar 973,928 gives ratio ~4.18, but differences in CBG area and non-mall activity matter.

## 4. Gravity intuition
$$F_{ij}\propto O_i A_j f(d_{ij})$$

`O_i` origin activity/population, `A_j` destination attractiveness, `d_ij` distance, `f` decreasing with distance. We do not directly estimate a physical law; this is a conceptual motivation.

## 5. PPML model (Poisson pseudo-maximum likelihood)
$$E[Y_{ijt}\mid X]=\exp\{\alpha+\beta_d\ln(1+d_{ij})+\gamma_j+\tau_t+\theta^\top X_i\}$$

- Outcome `Y_ijt`: allocated device count.
- `ln(1+d_ij)`: log(1 + driving miles); handles zero miles and allows nonlinear decay.
- `γ_j`: mall fixed effects, one indicator per mall except the reference.
- `τ_t`: month fixed effects, one indicator per month except the reference.
- `X_i`: optional `ln(income)`, `Gini`, `ln(population)`, community demographic shares.

**Why PPML?** Counts are nonnegative, often uneven, and the exponential conditional mean is natural for spatial flows. It avoids taking the logarithm of zero and does not require the dependent variable to be integer-valued under a quasi-likelihood interpretation. **It does not correct geographic mismatch or missing-origin truncation.** Standard errors were clustered by ZCTA; only 24–25 clusters means inference is fragile.

**Distance interpretation:** For distances `d1` and `d2`, predicted count ratio holding other terms fixed is

$$\frac{\hat Y(d_2)}{\hat Y(d_1)}=\exp\left[\beta_d\big(\ln(1+d_2)-\ln(1+d_1)\big)\right].$$

A negative `β_d` means longer driving distance predicts fewer reported devices, conditional on the model. It is **not** a one-mile percentage change.

## 6. Four-destination models
- **M1** `flow ~ log_distance + C(Mall) + C(Month)`: distance, destination and seasonality only.
- **M2** M1 + `log_income + log_population`: household resources and origin size.
- **M3** M2 + `gini`: income inequality.
- **M4** M3 + `black_share + hispanic_share`: community composition, **not** individual identity.
- **M5** M2 + `log_income:Buckhead`: whether income slope differs for Lenox/Phipps.
- **M6** `log_distance + log_income + black_share + black_share:Buckhead + log_population + C(Mall)+C(Month)`.
- **M7** `log_distance + C(ZCTA)+C(Mall)+C(Month)`: compare destinations while controlling for all origin characteristics constant across destinations. Main income/Gini terms cannot also be separately estimated with origin FE.
- **M8** M7 + `black_share:Buckhead`: destination-differential association despite origin FE.

## 7. Interaction terms
$$\log E[Y]=\dots+\beta_x x_i+\delta(x_i\times B_j).$$

When `B_j=0`, association with `x` is `β_x`; when `B_j=1`, it is `β_x+δ`. **δ compares slopes**, not the overall number of visitors. A neighborhood share interaction is an ecological comparison, not a claim about any individual.

## 8. Lenox versus Greenbriar
Filter to the two destination CBGs. Include `Lenox_j` indicator and optionally `log_income_i × Lenox_j`, `gini_i × Lenox_j`, `black_share_i × Lenox_j`, with origin and month fixed effects:

$$E[Y_{ijt}|X]=\exp\{\alpha_i+\tau_t+\lambda Lenox_j+\beta_d\ln(1+d_{ij})+\delta_x(x_i\times Lenox_j)\}.$$

Here origin FE absorb `x_i` itself, so the **interaction** is what identifies a differential relationship between destinations. It is not a causal difference in preferences.

## 9. Robustness and prediction
- 2020 area-overlay vs 2010 equal-block diagnostic: estimates are **not interchangeable**; source vintage unknown.
- 25 vs 24 origins: check sensitivity to newly added 30331.
- Reported cells only: avoids filling missing records with zero but selects on being reported; **not** an unbiased solution.
- Leave-one-origin-out: check if one ZCTA drives a coefficient.
- Holdout: train Jan–Sep, test Oct–Dec, compare model-predicted destination **shares** to an origin-specific historical-share baseline.

$$MAE_{pp}=100\times\frac{1}{N}\sum_{ijt}|\widehat{s}_{ijt}-s_{ijt}|.$$

Previous tested models had higher MAE than the historical baseline; no predictive superiority is established. This is a **Huff-style** comparison, not a fully estimated Huff attraction model.

## 10. Limitations required in every presentation
1. Dewey source CBG vintage not confirmed.
2. 2020 area-weighting and 2010 equal-block weighting are provisional approximations; coverage differs sharply.
3. Potential top-2,000 origin reporting and privacy transformations.
4. Destination CBG includes other establishments and streets, not mall-only entry.
5. One-year cross section in neighborhood attributes: **no pre/post mall-opening causal effect**.
6. No purchases, shopper demographics, retail sales, travel mode, or individual routes.
7. Only 25 origin ZCTAs; ZCTAs not USPS ZIPs; limited inference.
