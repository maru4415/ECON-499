"""Shared project settings and data utilities."""
from pathlib import Path
import numpy as np
import pandas as pd
import zipfile
ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT/'data'/'public'
PRIVATE = ROOT/'data'/'private'
OUT = ROOT/'outputs'
MALLS = ['Lenox Square','Phipps Plaza','Ponce City Market']
STUDY = ['30030','30033','30303','30305','30306','30307','30308','30309','30310','30311','30312','30313','30314','30315','30316','30317','30318','30319','30324','30326','30327','30329','30342','30345']
OUT.mkdir(parents=True,exist_ok=True)
def private_file(name):
    file=PRIVATE/name
    if not file.exists():
        raise FileNotFoundError(f'Missing licensed input: {file}. See PRIVATE_SETUP.md; do not commit these files.')
    return file
def load_flows():
    with zipfile.ZipFile(private_file('Advan_2024_derived_flows.zip')) as z:
        flows=pd.read_csv(z.open('Origin_Destination_Flows.csv'),dtype={'Origin_CBG':str,'Destination_CBG':str})
    flows=flows.loc[flows.Period.eq('All')].copy()
    flows['Origin_CBG']=flows.Origin_CBG.str.zfill(12)
    return flows

def build_panel(crosswalk):
    flows=load_flows()
    x=pd.read_csv(PUBLIC/'acs_distance_2024.csv',dtype={'ZCTA':str})
    w=pd.read_csv(crosswalk,dtype={'GEOID':str,'ZCTA':str})
    w=w[w.ZCTA.isin(STUDY)].copy()
    a=flows.merge(w,left_on='Origin_CBG',right_on='GEOID',how='inner',validate='many_to_many')
    a['allocated_flow']=a.Device_Count*a.weight
    q=a.groupby(['ZCTA','Mall','Month'],as_index=False).allocated_flow.sum().rename(columns={'Mall':'Destination','allocated_flow':'flow'})
    # Preserve all origin-destination-month cells, including zero allocated flows.
    months=pd.DataFrame({'Month':range(1,13)})
    panel=x.merge(months,how='cross').merge(q,on=['ZCTA','Destination','Month'],how='left')
    panel['flow']=panel.flow.fillna(0)
    pop=pd.read_csv(private_file('panel_legacy.csv'),dtype={'ZCTA':str})[['ZCTA','population']].drop_duplicates()
    panel=panel.merge(pop,on='ZCTA',how='left',validate='many_to_one')
    panel['log_income']=np.log(panel.income.where(panel.income>0))
    panel['log_pop']=np.log(panel.population.where(panel.population>0))
    panel['log_distance']=np.log1p(panel.driving_miles)
    panel['luxury']=panel.Destination.ne('Ponce City Market').astype(int)
    panel['income_buckhead']=panel.log_income*panel.luxury
    return panel,flows,w
