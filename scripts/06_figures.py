"""Stage 6: regenerate simple shareable charts from summary results."""
from common import *
import matplotlib.pyplot as plt
f=OUT/'figures';f.mkdir(exist_ok=True)
a=pd.read_csv(OUT/'gravity_results.csv').query("model == 'gravity'")
fig,ax=plt.subplots(figsize=(8,4));ax.bar(a.term,a.coef);ax.axhline(0,color='black',lw=.7)
ax.set_ylabel('PPML coefficient');ax.set_title('Baseline gravity model — provisional')
fig.tight_layout();fig.savefig(f/'gravity_coefficients.png',dpi=170);plt.close(fig)
h=pd.read_csv(OUT/'huff_validation.csv')
fig,ax=plt.subplots(figsize=(7,4));ax.bar(list(h.model)+['Historical baseline'],list(h.holdout_MAE_pp)+[h.historical_baseline_MAE_pp.iloc[0]])
ax.set_ylabel('Holdout MAE (percentage points)');ax.set_title('Oct–Dec holdout validation')
ax.tick_params(axis='x',rotation=15);fig.tight_layout();fig.savefig(f/'huff_holdout.png',dpi=170);plt.close(fig)
print('Saved figures to',f)
