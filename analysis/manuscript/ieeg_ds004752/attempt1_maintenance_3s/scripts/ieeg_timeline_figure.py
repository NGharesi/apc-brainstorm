"""Render the scalp-EEG timing gate once its raw grand average is available."""
from pathlib import Path
import sys,os,json,hashlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent;sys.path.insert(0,str(ROOT/'pydeps'));os.environ['MPLCONFIGDIR']=str(OUT/'plot_config')
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
meta=json.loads((OUT/'provenance.json').read_text(encoding='utf-8'))
p=OUT/'timeline_grand_average.csv';d=pd.read_csv(p,encoding='utf-8');m=json.loads((OUT/'timeline_gate_measurements.json').read_text(encoding='utf-8'))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
fig=plt.figure(figsize=(12,6));gs=fig.add_gridspec(2,2);axes=[fig.add_subplot(gs[0,:]),fig.add_subplot(gs[1,0]),fig.add_subplot(gs[1,1])]
for ax in axes:
    ax.plot(d.time_s,d.grand_average_uv,color='#0072B2',lw=.9)
    ax.set(xlabel='Trial time (s)',ylabel='Occipital EEG (microvolts)')
    for t in [1,6]:ax.axvline(t,color='black',ls='--',lw=.8)
axes[0].set_xlim(0,8)
for ax,onset in zip(axes[1:],[1,6]):
    ax.set_xlim(onset-.25,onset+.5)
    seg=d[(d.time_s>=onset-.25)&(d.time_s<=onset+.5)]
    lo,hi=seg.grand_average_uv.min(),seg.grand_average_uv.max();pad=.1*max(hi-lo,.01);ax.set_ylim(lo-pad,hi+pad)
    peak=next(x for x in m['peaks'] if x['expected_onset_s']==onset)
    ax.axvspan(onset+.05,onset+.25,color='#777777',alpha=.1)
    ax.plot(peak['peak_time_s'],peak['peak_uv'],'o',color='#D55E00',ms=5)
    ax.annotate(f"{peak['latency_ms']:.0f} ms",(peak['peak_time_s'],peak['peak_uv']),xytext=(6,8),textcoords='offset points',fontsize=9)
fig.tight_layout()
provenance=meta|dict(source_csv=str(p),source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),gate_measurements=m,stage='Scalp timing gate only; no dataset APC/scan output')
for ext in ['png','svg']:fig.savefig(OUT/f'timeline_grand_average.{ext}',dpi=300,metadata={'Description':json.dumps(provenance)})
plt.close(fig)
print(json.dumps(dict(status='FIGURE_READY_FOR_GATE_REVIEW',trials=m['trials'],peaks=m['peaks'])))
