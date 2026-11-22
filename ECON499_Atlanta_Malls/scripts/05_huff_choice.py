"""Stage 5: aggregate Huff-style model, temporal holdout, historical baseline, counterfactual."""
from common import *
from scipy.optimize import minimize
from scipy.special import softmax
p=pd.read_csv(OUT/'panel_legacy_RESTRICTED.csv',dtype={'ZCTA':str}).dropna(subset=['income'])
y=p.pivot(index=['ZCTA','Month'],columns='Destination',values='flow')[MALLS].dropna()
y=y[y.sum(axis=1)>0]
d=p.pivot(index=['ZCTA','Month'],columns='Destination',values='driving_miles').loc[y.index,MALLS].to_numpy()
income=p.groupby(['ZCTA','Month']).income.first().loc[y.index].to_numpy()
shares=y.to_numpy()/y.to_numpy().sum(axis=1,keepdims=True)
train=np.asarray(y.index.get_level_values('Month')<=9);test=~train
center=np.log(income[train]).mean()
def predict(b,dist=d):
    u=np.tile([b[0],b[1],0.],(len(y),1))+b[2]*np.log1p(dist)
    if len(b)==4:
        u+=b[3]*(np.log(income)-center)[:,None]*np.array([1,1,0])
    return softmax(u,axis=1)
s=pd.DataFrame(shares,index=y.index,columns=MALLS)
baseline=s.loc[train].groupby(level='ZCTA').mean()
bp=np.vstack([baseline.loc[z].to_numpy() for z in y.index.get_level_values('ZCTA')[test]])
base_mae=100*np.abs(bp-shares[test]).mean()
rows=[]
for name,k in [('distance',3),('distance_income',4)]:
    def loss(b):
        pr=np.clip(predict(b)[train],1e-12,1)
        return -(shares[train]*np.log(pr)).sum()/train.sum()
    opt=minimize(loss,np.zeros(k),method='L-BFGS-B')
    if not opt.success:raise RuntimeError(opt.message)
    pr=predict(opt.x)
    rows.append(dict(model=name,distance_coef=opt.x[2],income_buckhead_coef=opt.x[3] if k==4 else np.nan,holdout_MAE_pp=100*np.abs(pr[test]-shares[test]).mean(),historical_baseline_MAE_pp=base_mae,holdout_n=test.sum()))
    if name=='distance_income':
        cf=[]
        for j,mall in enumerate(MALLS):
            nd=d.copy();nd[:,j]*=.8
            delta=(predict(opt.x,nd)-pr).mean(axis=0)*100
            cf.append(dict(improved_mall=mall,distance_reduction=.2,**dict(zip(MALLS,delta))))
        pd.DataFrame(cf).to_csv(OUT/'huff_counterfactual.csv',index=False)
        pd.DataFrame(dict(destination=MALLS,observed=shares[test].mean(axis=0),predicted=pr[test].mean(axis=0))).to_csv(OUT/'huff_test_shares.csv',index=False)
pd.DataFrame(rows).to_csv(OUT/'huff_validation.csv',index=False)
print(pd.DataFrame(rows).to_string(index=False))
