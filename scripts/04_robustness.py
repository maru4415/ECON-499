"""Stage 4: temporal and leave-one-ZCTA-out PPML sensitivity."""
from common import *
import statsmodels.api as sm
import statsmodels.formula.api as smf
p=pd.read_csv(OUT/'panel_legacy_RESTRICTED.csv',dtype={'ZCTA':str}).dropna(subset=['log_income','log_pop','log_distance'])
formula='flow ~ log_distance + log_income + log_pop + C(Destination) + C(Month)'
samples=[('all',p),('Jan-Oct',p[p.Month<=10]),('Nov-Dec',p[p.Month>=11])]+[(f'omit_{z}',p[p.ZCTA!=z]) for z in sorted(p.ZCTA.unique())]
rows=[]
for name,sub in samples:
    fit=smf.glm(formula,sub,family=sm.families.Poisson()).fit(cov_type='cluster',cov_kwds={'groups':sub.ZCTA},maxiter=200)
    for term in ['log_distance','log_income','log_pop']:
        rows.append(dict(sample=name,term=term,coef=fit.params[term],se=fit.bse[term],p_normal=fit.pvalues[term],n=len(sub),clusters=sub.ZCTA.nunique()))
pd.DataFrame(rows).to_csv(OUT/'robustness_results.csv',index=False)
print('Saved',OUT/'robustness_results.csv')
