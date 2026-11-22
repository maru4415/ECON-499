"""Stage 7: compare legacy geography with precomputed NHGIS equal-block diagnostic.
The NHGIS diagnostic is NOT a validated correction and must not replace the legacy estimates.
"""
from common import *
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--diagnostic-crosswalk',type=Path,help='2010 equal-block diagnostic CSV from restricted research materials')
a=parser.parse_args()
legacy=pd.read_csv(private_file('crosswalk_legacy.csv'),dtype={'GEOID':str,'ZCTA':str})
flows=load_flows()
rows=[]
for label,path in [('legacy',private_file('crosswalk_legacy.csv'))]+([('2010_equal_block_DIAGNOSTIC',a.diagnostic_crosswalk)] if a.diagnostic_crosswalk else []):
    w=pd.read_csv(path,dtype={'GEOID':str,'ZCTA':str});w=w[w.ZCTA.isin(STUDY)]
    weights=w.groupby('GEOID').weight.sum()
    allocated=(flows.Device_Count*flows.Origin_CBG.map(weights).fillna(0).clip(upper=1)).sum()
    rows.append(dict(scenario=label,matched_origins=len(set(flows.Origin_CBG)&set(weights.index)),total_origins=flows.Origin_CBG.nunique(),allocated_fraction=allocated/flows.Device_Count.sum(),warning='Not vintage-validated' if label=='legacy' else 'Equal-block diagnostic, NOT validated'))
print(pd.DataFrame(rows).to_string(index=False))
pd.DataFrame(rows).to_csv(OUT/'geography_coverage_audit.csv',index=False)
