"""Stage 2: build 24 ZCTA x 3 destinations x 12 months provisional panel."""
from common import *
panel,flows,w=build_panel(private_file('crosswalk_legacy.csv'))
assert len(panel)==864
panel.to_csv(OUT/'panel_legacy_RESTRICTED.csv',index=False)
weight=w.groupby('GEOID').weight.sum()
coverage=(flows.Device_Count*flows.Origin_CBG.map(weight).fillna(0).clip(upper=1)).sum()/flows.Device_Count.sum()
print('Legacy panel rows:',len(panel),'positive flows:',int((panel.flow>0).sum()))
print('Study-area allocation fraction:',round(coverage,4))
print('Saved RESTRICTED derived panel. Do not commit outputs/ to GitHub.')
