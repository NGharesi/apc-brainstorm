"""Protocol four-panel scientific figure; provenance is embedded as metadata."""
from pathlib import Path
import sys,json,os
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O.parent.parent/'pydeps'))
os.environ['MPLCONFIGDIR']=str(O/'matplotlib_cache')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
m=json.loads((O/'analysis_provenance.json').read_text(encoding='utf-8'))
P=pd.read_csv(O/'ecog_patient_summary.csv',encoding='utf-8');P=P[(P.subset=='prespecified')&(P.recording=='movement')];D=pd.read_csv(O/'figure_patient_coupling_CIs.csv',encoding='utf-8');rest=pd.read_csv(O/'rest_frequency_patient_table.csv',encoding='utf-8');rest=rest[(rest.subset=='prespecified')&(rest.recording=='movement')&(rest.method=='APC-v1.0')]
patients=sorted(P.patient.unique());x=np.arange(len(patients));colors={'APC-v1.0':'#1767a8','MVL-Ozkurt':'#c65f1a'}
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
fig,axes=plt.subplots(2,2,figsize=(12,9),layout='constrained')
for ax,field,ylabel in [(axes[0,0],'mean_fP_hz','Patient mean fP (Hz)'),(axes[0,1],'mean_ozkurt_mvl','Patient mean normalized MVL')]:
    for method,offset in [('APC-v1.0',-.14),('MVL-Ozkurt',.14)]:
        for state,marker in [('rest','o'),('move','^')]:
            g=P[(P.method==method)&(P.state==state)].set_index('patient').reindex(patients);ax.plot(x+offset,g[field],linestyle='none',marker=marker,markersize=5,color=colors[method],markerfacecolor='white' if state=='rest' else colors[method],label=f'{method}, {"movement" if state=="move" else "rest"}')
    ax.set_xticks(x,patients,rotation=90);ax.set_xlabel('Patient');ax.set_ylabel(ylabel)
axes[0,0].legend(frameon=False,fontsize=8,ncols=2)
g=D.set_index('patient').reindex(patients);ax=axes[1,0];valid=g.difference.notna();xx=x[valid];v=g[valid];ax.errorbar(xx,v.difference,yerr=np.vstack([v.difference-v.ci_low,v.ci_high-v.difference]),fmt='o',color=colors['APC-v1.0'],capsize=2);ax.axhline(0,color='0.5',linewidth=1);ax.set_xticks(x,patients,rotation=90);ax.set_xlabel('Patient');ax.set_ylabel('APC normalized MVL\nMovement minus rest (95% CI)')
ax=axes[1,1];ax.scatter(rest.rest_spectral_peak_hz,rest.median_fP_hz,color=colors['APC-v1.0']);ax.plot([5,31],[5,31],color='0.5',linestyle='--',linewidth=1);ax.set(xlim=(5,31),ylim=(5,31),xlabel='Analysed-rest spectral peak (Hz)',ylabel='Patient median rest APC fP (Hz)')
for label,ax in zip('ABCD',axes.flat):ax.text(-.13,1.02,label,transform=ax.transAxes,weight='bold',fontsize=12,va='bottom')
metadata=dict(git_head=m['git_head'],protocol_sha256=m['protocol_sha256'],seed=20261024,sources=['ecog_patient_summary.csv','figure_patient_coupling_CIs.csv','rest_frequency_patient_table.csv'],patient_CIs='10000 independent within-state bout resamples, percentile 95%, seed20261024',provenance_file='analysis_provenance.json')
desc=json.dumps(metadata,separators=(',',':'));fig.savefig(O/'ecog_four_panel.png',dpi=300,metadata={'Description':desc,'Software':'Matplotlib'});fig.savefig(O/'ecog_four_panel.svg',metadata={'Description':desc,'Creator':'APC prespecified ECoG analysis'});plt.close(fig)
(O/'figure_provenance.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8');print('Saved 300-dpi PNG and SVG with hidden provenance, no titles or footers.')
