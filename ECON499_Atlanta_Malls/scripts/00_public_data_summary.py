"""Run with only public inputs: ACS-distance coverage and descriptive summaries."""
from common import *
x=pd.read_csv(PUBLIC/'acs_distance_2024.csv',dtype={'ZCTA':str})
print('Study ZCTAs:',x.ZCTA.nunique(),'destinations:',x.Destination.nunique())
print('Missing median income ZCTAs:',sorted(x.loc[x.income.isna(),'ZCTA'].unique()))
print(x.groupby('Destination').driving_miles.agg(['count','mean','median','min','max']).to_string())
print('These are descriptive distances, NOT Advan traffic estimates.')
