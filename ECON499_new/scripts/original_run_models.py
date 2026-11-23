import os, zipfile, warnings
import numpy as np, pandas as pd, geopandas as gpd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from scipy.stats import pearsonr,spearmanr
warnings.filterwarnings('ignore',category=FutureWarning)
BASE='/mnt/data'; OUT=BASE+'/ECON499_Greenbriar_2024_Analysis';os.makedirs(OUT,exist_ok=True)
with zipfile.ZipFile(BASE+'/ECON499_Dewey_2024_4Malls.zip') as z:
 flows=pd.read_csv(z.open('Origin_Destination_Flows.csv'),dtype={'Origin_CBG':str,'Destination_CBG':str})
 summary=pd.read_csv(z.open('Mall_Monthly_Summary.csv'),dtype={'Destination_CBG':str})
acs=pd.read_csv(BASE+'/ECON499_ACS_2024_25_ZCTA_Checked.csv',dtype={'ZCTA':str})
for c in acs.columns:
 if c!='ZCTA':acs[c]=pd.to_numeric(acs[c],errors='coerce')
acs=acs.rename(columns={'B19013_001E':'income','B19083_001E':'gini','B01003_001E':'population','B03002_004E':'black_nonhisp','B03002_003E':'white_nonhisp','B03002_012E':'hispanic'})
for c in ['income','gini','population']:
 acs.loc[acs[c]<0,c]=np.nan
acs['black_share']=acs.black_nonhisp/acs.population
acs['white_share']=acs.white_nonhisp/acs.population
acs['hispanic_share']=acs.hispanic/acs.population
acs.to_csv(OUT+'/acs_25_zctas.csv',index=False)
dist=pd.read_excel(BASE+'/ECON499_100_Driving_Distances_RETESTED.xlsx',sheet_name='100 Routes',dtype={'Origin ZCTA':str})
dist=dist.rename(columns={'Origin ZCTA':'ZCTA','Destination Mall':'Mall','Driving Miles':'miles'})[['ZCTA','Mall','miles']]
assert len(dist)==100 and not dist.duplicated(['ZCTA','Mall']).any()
# 2020-based geometry approximation: 2024 CBG polygons to 2020 ZCTA polygons from 2026 release.
bg=gpd.read_file('zip://'+BASE+'/tl_2024_13_bg (1).zip')[['GEOID','geometry']].rename(columns={'GEOID':'Origin_CBG'})
zcta=gpd.read_file('zip://'+BASE+'/tl_2026_us_zcta520.zip')
zcta=zcta[zcta.ZCTA5CE20.isin(acs.ZCTA)][['ZCTA5CE20','geometry']].rename(columns={'ZCTA5CE20':'ZCTA'})
bg=bg.to_crs(5070);zcta=zcta.to_crs(5070)
bg=bg[bg.intersects(zcta.union_all())].copy()
bg['area']=bg.geometry.area
ix=gpd.overlay(bg,zcta,how='intersection',keep_geom_type=False)
ix['weight']=ix.geometry.area/ix['area']
cw20=ix[['Origin_CBG','ZCTA','weight']].groupby(['Origin_CBG','ZCTA'],as_index=False).sum()
cw20.to_csv(OUT+'/crosswalk_2020_geometry_provisional.csv',index=False)
print('2020 geometry crosswalk',len(cw20),'CBGs',cw20.Origin_CBG.nunique())
# NHGIS 2010 block -> 2020 ZCTA, diagnostic equal-block approximation; not population-weighted.
blocks=set();parts=[]
with zipfile.ZipFile(BASE+'/nhgis_blk2010_zcta2020.zip') as z:
 with z.open('nhgis_blk2010_zcta2020.csv') as f:
  for chunk in pd.read_csv(f,usecols=['blk2010ge','zcta2020ge','weight'],dtype={'blk2010ge':str,'zcta2020ge':str},chunksize=700000):
   chunk=chunk[chunk.blk2010ge.str.startswith('13')]
   blocks.update(chunk.blk2010ge.unique())
   chunk=chunk[chunk.zcta2020ge.isin(acs.ZCTA)]
   if len(chunk):parts.append(chunk)
raw=pd.concat(parts,ignore_index=True)
raw['Origin_CBG']=raw.blk2010ge.str[:12]
block_count=pd.Series([s[:12] for s in blocks]).value_counts()
raw['block_n']=raw.Origin_CBG.map(block_count)
raw['component']=raw.weight/raw.block_n
cw10=raw.groupby(['Origin_CBG','zcta2020ge'],as_index=False).component.sum().rename(columns={'zcta2020ge':'ZCTA','component':'weight'})
cw10.to_csv(OUT+'/crosswalk_2010_equal_block_DIAGNOSTIC.csv',index=False)
print('2010 diagnostic crosswalk',len(cw10),'CBGs',cw10.Origin_CBG.nunique())

results=[];panels={};cover=[]
for scenario,cw in [('2020_geometry_provisional',cw20),('2010_equal_block_diagnostic',cw10)]:
 mapped=flows.merge(cw,on='Origin_CBG',how='inner')
 mapped['allocated_flow']=mapped.Origin_Device_Count*mapped.weight
 p=mapped.groupby(['ZCTA','Mall','Month'],as_index=False).allocated_flow.sum().rename(columns={'allocated_flow':'flow'})
 full=pd.MultiIndex.from_product([sorted(acs.ZCTA),sorted(summary.Mall.unique()),range(1,13)],names=['ZCTA','Mall','Month']).to_frame(index=False)
 p=full.merge(p,on=['ZCTA','Mall','Month'],how='left')
 # No observed origin record does not imply a true zero: impute 0 only for diagnostic panel construction.
 p['unreported_origin_cell']=p.flow.isna()
 p['flow']=p.flow.fillna(0)
 p=p.merge(acs,on='ZCTA',how='left').merge(dist,on=['ZCTA','Mall'],how='left')
 p['log_distance']=np.log1p(p.miles)
 p['log_income']=np.log(p.income)
 p['log_population']=np.log(p.population)
 p['Buckhead']=p.Mall.isin(['Lenox Square','Phipps Plaza']).astype(int)
 p.to_csv(OUT+'/panel_'+scenario+'.csv',index=False)
 panels[scenario]=p
 cover.append({'scenario':scenario,'origin_cbgs_matched':mapped.Origin_CBG.nunique(),'flow_fraction_allocated_to_25_zctas':mapped.allocated_flow.sum()/flows.Origin_Device_Count.sum(),'panel_rows':len(p),'unreported_panel_cells':int(p.unreported_origin_cell.sum()),'n_income_zctas':int(p.dropna(subset=['income']).ZCTA.nunique())})
 print('scenario',scenario,'capture',cover[-1])
 # Models: origin clustered SE, 25 clusters (24 when income unavailable); no causal interpretation.
 formulas={
 'M1_distance':'flow ~ log_distance + C(Mall) + C(Month)',
 'M2_income_population':'flow ~ log_distance + log_income + log_population + C(Mall) + C(Month)',
 'M3_gini':'flow ~ log_distance + log_income + gini + log_population + C(Mall) + C(Month)',
 'M4_race':'flow ~ log_distance + log_income + gini + black_share + hispanic_share + log_population + C(Mall) + C(Month)',
 'M5_buckhead_income':'flow ~ log_distance + log_income + log_income:Buckhead + log_population + C(Mall) + C(Month)',
 'M6_buckhead_black_share':'flow ~ log_distance + log_income + black_share + black_share:Buckhead + log_population + C(Mall) + C(Month)',
 'M7_origin_FE':'flow ~ log_distance + C(ZCTA) + C(Mall) + C(Month)',
 'M8_origin_FE_race_interaction':'flow ~ log_distance + black_share:Buckhead + C(ZCTA) + C(Mall) + C(Month)',
 }
 for name,formula in formulas.items():
  try:
   fit=smf.glm(formula,data=p,family=sm.families.Poisson()).fit(cov_type='cluster',cov_kwds={'groups':p.loc[smf.glm(formula,data=p,family=sm.families.Poisson()).data.row_labels,'ZCTA']},maxiter=150)
   for term in ['log_distance','log_income','gini','black_share','hispanic_share','log_income:Buckhead','black_share:Buckhead']:
    if term in fit.params:
     results.append({'scenario':scenario,'model':name,'term':term,'coef':fit.params[term],'se':fit.bse[term],'p':fit.pvalues[term],'n':int(fit.nobs),'aic':fit.aic})
  except Exception as e:print('MODEL ERROR',scenario,name,str(e)[:200])
 # Correlations: origin-level income and race with distance to each mall.
 for mall,group in p[p.Month==1].groupby('Mall'):
  for var in ['income','gini','black_share']:
   d=group[[var,'miles']].dropna()
   if len(d)>4:
    r,pv=pearsonr(d[var],d.miles)
    results.append({'scenario':scenario,'model':'descriptive_'+mall,'term':'pearson_'+var+'_distance','coef':r,'se':np.nan,'p':pv,'n':len(d),'aic':np.nan})

pd.DataFrame(cover).to_csv(OUT+'/geographic_coverage.csv',index=False)
res=pd.DataFrame(results);res.to_csv(OUT+'/model_results_all.csv',index=False)
# Monthly chart, descriptive annual reported counts, no deduplication.
chart=summary.pivot(index='Month',columns='Mall',values='Device_Counts')
fig,ax=plt.subplots(figsize=(10,5.5));chart.plot(ax=ax,marker='o',linewidth=1.8);ax.set(title='2024 monthly device activity in mall-containing CBGs',xlabel='Month',ylabel='Reported devices (not mall visitors)');ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT+'/monthly_device_activity.png',dpi=180);plt.close(fig)
# Origin demographic quartiles, weighted model scenario 2020 provisional.
p=panels['2020_geometry_provisional'].copy();p['income_group']=pd.qcut(p.income,4,labels=['Q1 lower','Q2','Q3','Q4 higher'],duplicates='drop')
q=p.groupby(['income_group','Mall'],observed=True).flow.sum().unstack();share=q.div(q.sum(axis=1),axis=0)
share.to_csv(OUT+'/destination_shares_by_income_quartile_provisional.csv')
ax=share.plot(kind='bar',stacked=True,figsize=(10,5.5));ax.set(title='Reported destination activity shares by origin income quartile',ylabel='Share of four observed destination CBGs',xlabel='Origin ZCTA income quartile');ax.legend(loc='upper left',bbox_to_anchor=(1,1));plt.tight_layout();plt.savefig(OUT+'/income_quartile_destination_shares.png',dpi=180);plt.close()
# Holdout: estimate choice model with destination fixed effects and log_distance and origin socioeconomic interaction, train Jan-Sep, predict Oct-Dec shares.
val=[]
for scenario,p in panels.items():
 pp=p.dropna(subset=['income','population']).copy()
 pp['log_flow1']=np.log1p(pp.flow)
 tr=pp[pp.Month<=9];te=pp[pp.Month>=10]
 # pooled model without month FE for out-of-time prediction; estimate on train counts
 for spec,formula in [('distance_only','flow ~ log_distance + C(Mall)'),('distance_income','flow ~ log_distance + log_income:Buckhead + C(Mall)'),('distance_race','flow ~ log_distance + black_share:Buckhead + C(Mall)')]:
  try:
   m=smf.glm(formula,data=tr,family=sm.families.Poisson()).fit(maxiter=120)
   te=te.copy();te['pred']=m.predict(te)
   te['pred_share']=te.pred/te.groupby(['ZCTA','Month']).pred.transform('sum')
   te['actual_share']=te.flow/te.groupby(['ZCTA','Month']).flow.transform('sum').replace(0,np.nan)
   # historical origin-specific destination share benchmark; fallback to pooled destination share.
   h=tr.groupby(['ZCTA','Mall']).flow.sum().reset_index()
   h['hist_share']=h.flow/h.groupby('ZCTA').flow.transform('sum').replace(0,np.nan)
   t=te.merge(h[['ZCTA','Mall','hist_share']],on=['ZCTA','Mall'],how='left')
   valid=t.dropna(subset=['actual_share','pred_share','hist_share'])
   val.append({'scenario':scenario,'model':spec,'n_holdout_cells':len(valid),'MAE_share_pp':100*np.mean(np.abs(valid.pred_share-valid.actual_share)),'historical_baseline_MAE_pp':100*np.mean(np.abs(valid.hist_share-valid.actual_share))})
  except Exception as e:print('HOLDOUT ERROR',scenario,spec,str(e)[:200])
pd.DataFrame(val).to_csv(OUT+'/huff_style_holdout.csv',index=False)
print('\nMODEL RESULTS')
print(res[res.term=='log_distance'][['scenario','model','coef','se','p','n']].to_string(index=False))
print('\nHOLDOUT')
print(pd.DataFrame(val).to_string(index=False))
