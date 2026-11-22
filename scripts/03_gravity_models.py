"""Stage 3: PPML gravity, origin fixed-effects sorting, socioeconomic controls."""
from common import *
import statsmodels.api as sm
import statsmodels.formula.api as smf
p=pd.read_csv(OUT/'panel_legacy_RESTRICTED.csv',dtype={'ZCTA':str})
forms={
'gravity':'flow ~ log_distance + log_income + log_pop + C(Destination) + C(Month)',
'sorting':'flow ~ log_distance + income_buckhead + C(ZCTA) + C(Destination) + C(Month)',
'controls':'flow ~ log_distance + log_income + log_pop + gini + education_share + poverty_rate + np.log(home_value) + C(Destination) + C(Month)'}
rows=[]
for name,formula in forms.items():
    subset=p.replace([np.inf,-np.inf],np.nan).dropna(subset=['log_distance','log_income','log_pop']+(['gini','education_share','poverty_rate','home_value'] if name=='controls' else []))
    fit=smf.glm(formula,subset,family=sm.families.Poisson()).fit(cov_type='cluster',cov_kwds={'groups':subset.ZCTA},maxiter=200)
    print(name,'n=',fit.nobs,'converged=',fit.converged)
    for term in ['log_distance','log_income','log_pop','income_buckhead','gini','education_share','poverty_rate','np.log(home_value)']:
        if term in fit.params:
            rows.append(dict(model=name,term=term,coef=fit.params[term],se=fit.bse[term],p_normal=fit.pvalues[term],n=int(fit.nobs),clusters=subset.ZCTA.nunique()))
pd.DataFrame(rows).to_csv(OUT/'gravity_results.csv',index=False)
print('Saved',OUT/'gravity_results.csv')
