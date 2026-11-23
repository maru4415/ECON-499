import pandas as pd, numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from pathlib import Path
P=Path('/mnt/data/ECON499_Greenbriar_2024_Analysis')
results=[]
for label,fn in [('2020 polygon overlay (provisional)','panel_2020_geometry_provisional.csv'),('2010 equal-block diagnostic','panel_2010_equal_block_diagnostic.csv')]:
 d=pd.read_csv(P/fn,dtype={'ZCTA':str});d=d[d.Mall.isin(['Lenox Square','Greenbriar Mall'])].copy()
 d['Lenox']=(d.Mall=='Lenox Square').astype(int)
 d['income_10k']=d.income/10000
 d['income_centered']=np.log(d.income)-np.log(d.income.dropna().median())
 d['black_centered']=d.black_share-d.black_share.mean()
 d['gini_centered']=d.gini-d.gini.mean()
 for name,formula in [
  ('P1: Distance + origin and month FE','flow ~ log_distance + Lenox + C(ZCTA) + C(Month)'),
  ('P2: Income differential + origin and month FE','flow ~ log_distance + Lenox + Lenox:income_centered + C(ZCTA) + C(Month)'),
  ('P3: Gini differential + origin and month FE','flow ~ log_distance + Lenox + Lenox:gini_centered + C(ZCTA) + C(Month)'),
  ('P4: Black-share differential + origin and month FE','flow ~ log_distance + Lenox + Lenox:black_centered + C(ZCTA) + C(Month)'),
  ('P5: Income and Black-share differential','flow ~ log_distance + Lenox + Lenox:income_centered + Lenox:black_centered + C(ZCTA) + C(Month)')]:
  dat=d.dropna(subset=['flow','log_distance','income_centered'] if 'income' in formula else ['flow','log_distance']).copy()
  try:
   mod=smf.glm(formula,data=dat,family=sm.families.Poisson()).fit(cov_type='cluster',cov_kwds={'groups':dat.ZCTA},maxiter=150)
   for k in ['log_distance','Lenox','Lenox:income_centered','Lenox:gini_centered','Lenox:black_centered']:
    if k in mod.params:
     results.append({'scenario':label,'model':name,'term':k,'coefficient':mod.params[k],'se':mod.bse[k],'p_value':mod.pvalues[k],'n':len(dat),'zctas':dat.ZCTA.nunique()})
  except Exception as e:print('FAILED',label,name,str(e)[:180])
 d['flow_per_1000_residents']=d.flow/d.population*1000
 d['income_group']=pd.qcut(d['income'].rank(method='first'),4,labels=['Q1 lower','Q2','Q3','Q4 higher'])
 agg=d.groupby(['Mall'],as_index=False).agg(allocated_device_month_counts=('flow','sum'),mean_monthly_count=('flow','mean'),median_monthly_count=('flow','median'))
 agg['scenario']=label
 agg.to_csv(P/('pair_totals_'+('2020' if '2020' in label else '2010')+'.csv'),index=False)
 byzip=d.groupby(['ZCTA','Mall'],as_index=False).agg(annual_allocated_flow=('flow','sum'),miles=('miles','first'),income=('income','first'),gini=('gini','first'),population=('population','first'),black_share=('black_share','first'))
 wide=byzip.pivot(index='ZCTA',columns='Mall',values='annual_allocated_flow').reset_index()
 wide['lenox_share_of_pair']=wide['Lenox Square']/(wide['Lenox Square']+wide['Greenbriar Mall'])
 wide['scenario']=label
 wide.to_csv(P/('pair_zcta_'+('2020' if '2020' in label else '2010')+'.csv'),index=False)
 print(label,'totals\n',agg.to_string(index=False))
print('MODEL RESULTS')
r=pd.DataFrame(results);r.to_csv(P/'lenox_greenbriar_ppml_results.csv',index=False)
print(r.to_string(index=False))
