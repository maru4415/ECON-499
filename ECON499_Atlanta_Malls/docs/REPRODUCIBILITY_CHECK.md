# Reproducibility check — 2026-11-22

All seven pipeline stages executed successfully in a local test with authorized private inputs. Baseline, sorting and controls PPML models converged; 864 origin–destination–month panel rows; 828 complete-case rows; 23 origin clusters. Recomputed coefficients match archived legacy model results to floating-point tolerance. Huff distance+income MAE: 6.0340 pp; historical baseline MAE: 3.2574 pp.

This verifies **code execution**, not that geographic vintage was corrected. Vendor source partition vintage and population-weighted CBG correspondence remain unresolved.
