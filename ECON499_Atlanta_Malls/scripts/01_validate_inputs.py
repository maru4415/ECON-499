"""Stage 1: validate input files and report geographic vintage warning."""
from common import *
x=pd.read_csv(PUBLIC/'acs_distance_2024.csv',dtype={'ZCTA':str})
assert len(x)==72 and x.ZCTA.nunique()==24 and set(x.Destination)==set(MALLS)
assert not x.duplicated(['ZCTA','Destination']).any()
assert x.driving_miles.notna().all() and (x.driving_miles>=0).all()
print('Public ACS-distance data:',len(x),'rows,',x.ZCTA.nunique(),'ZCTAs')
print('Income missing for:',sorted(x.loc[x.income.isna(),'ZCTA'].unique()))
try:
    f=load_flows()
    w=pd.read_csv(private_file('crosswalk_legacy.csv'),dtype={'GEOID':str,'ZCTA':str})
    print('Licensed flows:',len(f),'rows,',f.Origin_CBG.nunique(),'origin CBGs')
    print('Crosswalk:',len(w),'rows,',w.GEOID.nunique(),'CBGs')
    assert w.weight.ge(0).all()
    assert (w.groupby('GEOID').weight.sum()<=1.00001).all()
except FileNotFoundError as e:
    print('Private inputs unavailable:',e)
print('IMPORTANT: Provider citation indicates 2010 CBG vintage; legacy overlay uses newer boundaries. Not resolved.')
