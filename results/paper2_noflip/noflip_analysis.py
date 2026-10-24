from pathlib import Path
from datetime import datetime, timezone
import os, sys, json, hashlib
O=Path(__file__).resolve().parent;R=O.parent.parent;V=R/'revision_checks/paper2_validation'
sys.path.insert(0,str(R/'pydeps'));os.environ['MPLCONFIGDIR']=str(O/'matplotlib_cache')
import numpy as np
import pandas as pd
from scipy.stats import binomtest
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=json.loads((O/'provenance.json').read_text(encoding='utf-8'))
def read(p):return pd.read_csv(p,encoding='utf-8',float_precision='round_trip')
def write(d,name):
 d=pd.DataFrame(d);d['classification']='exploratory';d['git_commit']=P['git_head'];d['protocol_sha256']=P['protocol_sha256'];d['provenance_file']='provenance.json';d.to_csv(O/name,index=False,encoding='utf-8',float_format='%.17g');return d
def mc(a,b):
 a=np.asarray(a,bool);b=np.asarray(b,bool);n10=int((a&~b).sum());n01=int((~a&b).sum());return n10,n01,1. if n10+n01==0 else float(binomtest(n10,n10+n01,.5).pvalue)
def outcomes(d):
 valid=d.valid.astype(bool);ep=abs(d.endtoend_fp_hz-d.true_fp_hz);ea=abs(d.endtoend_fa_hz-d.true_fa_hz)
 return {'fp_recovery':abs(d.source_fp_hz-d.true_fp_hz)<=1,'dominant_picks':abs(d.source_fp_hz-d.true_fd_hz)<=1,'joint':valid&(ep<=1)&(ea<=8),'strict_joint':valid&(ep<=.5)&(ea<=8)}
def md(d):
 cols=[c for c in d if c not in ['classification','git_commit','protocol_sha256','provenance_file']]
 def f(x):return 'not available' if pd.isna(x) else f'{x:.6g}' if isinstance(x,(float,np.floating)) else str(x)
 return '| '+' | '.join(cols)+' |\n| '+' | '.join(['---']*len(cols))+' |\n'+''.join('| '+' | '.join(f(x) for x in row)+' |\n' for row in d[cols].itertuples(index=False,name=None))
assert not (O/'analysis_complete.json').exists() and not (O/'STOPPED.md').exists()
for w in range(1,5):assert json.loads((O/f'worker{w}_complete.json').read_text(encoding='utf-8'))['status']=='COMPLETE'
frames=[]
for suite,n in [('V3',600),('V1',350),('V2',900),('V4',25)]:
 d=pd.concat([read(O/f'{suite}_worker{w}.csv') for w in range(1,5)],ignore_index=True)
 assert d.key.nunique()==n and len(d)==4*n and not d.duplicated(['key','method','flip_troughs']).any();frames.append(d)
D=pd.concat(frames,ignore_index=True);truth=read(V/'simulation_truths.csv');D=D.merge(truth[['key','beta','duration_s']],on='key',validate='many_to_one');write(D,'trial_estimates.csv')
rows=[];tests=[];diag=[];levels=[]
def compare(g,cohort):
 for method,z in g.groupby('method',sort=False):
  a=z[z.flip_troughs==1].set_index('key').sort_index();b=z[z.flip_troughs==0].set_index('key').reindex(a.index);assert not b.method.isna().any();oa=outcomes(a);ob=outcomes(b)
  q={'suite':str(g.suite.iloc[0]),'cohort':cohort,'method':method,'n':len(a)}
  for metric in ['fp_recovery','dominant_picks','joint','strict_joint']:
   applicable=metric!='dominant_picks' or (q['suite']=='V3' and a.true_fd_hz.notna().all());q[metric+'_flip']=int(oa[metric].sum()) if applicable else np.nan;q[metric+'_noflip']=int(ob[metric].sum()) if applicable else np.nan
   if q['suite']=='V3' and metric in ['fp_recovery','dominant_picks','joint'] and applicable:
    n10,n01,p=mc(oa[metric],ob[metric]);q[metric+'_p_exploratory']=p;tests.append(dict(suite='V3',cohort=cohort,method=method,metric=metric,n=len(a),flip_success=q[metric+'_flip'],noflip_success=q[metric+'_noflip'],only_flip=n10,only_noflip=n01,p_exact_exploratory=p))
  rows.append(q)
  for flip,v in z.groupby('flip_troughs',sort=False):
   diag.append(dict(suite=q['suite'],cohort=cohort,method=method,flip_troughs=flip,n=len(v),mean_n_bursts=v.n_bursts.mean(),median_n_bursts=v.n_bursts.median(),min_n_bursts=v.n_bursts.min(),max_n_bursts=v.n_bursts.max(),fraction_epochs_flipped='not available',mean_bta_power_coupled=v.bta_power_coupled.mean(),median_bta_power_coupled=v.bta_power_coupled.median(),mean_bta_power_dominant=v.bta_power_dominant.mean(),median_bta_power_dominant=v.bta_power_dominant.median(),finite_bta_pairs=int((v.bta_power_coupled.notna()&v.bta_power_dominant.notna()).sum())))
cells=['A_keep100','A_keep040','B_keep100','B_keep040','R_single_keep100','N_uncoupled'];v3=D[D.suite=='V3']
for cell in cells:compare(v3[v3.scenario==cell],cell)
compare(v3[v3.scenario.isin(cells[:4])],'non_dominant_pooled')
for (suite,dataset),g in D[D.suite!='V3'].groupby(['suite','dataset'],sort=False):compare(g,dataset)
for keys,g in D.groupby(['suite','scenario','dataset','level','beta','duration_s','method','flip_troughs'],dropna=False,sort=False):
 q=dict(zip(['suite','scenario','dataset','level','beta','duration_s','method','flip_troughs'],keys));q['n']=len(g);q.update({k:(int(v.sum()) if k!='dominant_picks' or (q['suite']=='V3' and g.true_fd_hz.notna().all()) else np.nan) for k,v in outcomes(g).items()});levels.append(q)
summary=write(rows,'summary.csv');tests=write(tests,'mcnemar_exploratory.csv');diagnostics=write(diag,'diagnostics.csv');write(levels,'recovery_by_level.csv')
v3summary=summary[summary.suite=='V3'];other=summary[summary.suite!='V3']
plt.rcParams.update({'svg.fonttype':'none','font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(1,2,figsize=(15,5));colors=['#355d91','#93b4db','#ae681b','#e4b76b'];series=[('APC-v1.0',True),('APC-v1.0',False),('APC-v3.0',True),('APC-v3.0',False)]
for ax,metric,these in [(axs[0],'fp_recovery',cells),(axs[1],'dominant_picks',cells[:4])]:
 for j,(method,flip) in enumerate(series):
  q=v3summary[v3summary.method==method].set_index('cohort').reindex(these);col=metric+('_flip' if flip else '_noflip');ax.bar(np.arange(len(these))+(j-1.5)*.19,q[col]/q.n,width=.19,color=colors[j],label=method+(' flip' if flip else ' no-flip'))
 ax.set_xticks(np.arange(len(these)),these,rotation=30,ha='right');ax.set_ylim(0,1.24);ax.set_yticks(np.arange(0,1.01,.2));ax.set_ylabel('Exploratory: reference-fP recovery proportion' if metric=='fp_recovery' else 'Exploratory: dominant-rhythm pick proportion');ax.set_xlabel('V3 cell (100 trials each)');ax.grid(axis='y',alpha=.2)
axs[0].legend(fontsize=8,ncol=2);fig.tight_layout();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();meta={'classification':'exploratory','git_commit':P['git_head'],'protocol_sha256':P['protocol_sha256'],'source_csv':str(O/'summary.csv'),'source_sha256':sha(O/'summary.csv')};desc=json.dumps(meta)
fig.savefig(O/'exploratory_noflip.png',dpi=300,metadata={'Description':desc});fig.savefig(O/'exploratory_noflip.svg',metadata={'Description':desc,'Creator':'APC exploratory no-flip'});plt.close(fig)
report=['# Exploratory: polarity-flip sensitivity\n',f"This post hoc exploratory analysis cannot change the validation decisions. Archive commit and successful push: `{P['archive_commit']}`. Protocol commit `{P['protocol_commit']}`, SHA-256 `{P['protocol_sha256']}`.\n",'Saved inputs only: V3 600, V1 350, V2 900, V4 25. All 1875 input hashes were retained; no signals or flip=true estimates were regenerated. For each frozen APC version the full normalized options were checked against the validation options with only flipTroughs changed to false. Four workers; no src changes. Step-2 fP is retained independently of later APC failure, using the unchanged ablation helper only when necessary. Invalid end-to-end outputs count as recovery failures.\n','## Exploratory V3 outcomes\n','Counts use Step-2 fP for reference-frequency recovery and dominant picks, and valid end-to-end estimates for joint recovery. Frequency tolerances: fP 1 Hz, fA 8 Hz. In N_uncoupled, reference fP is 8 Hz and joint recovery is false joint recovery. Dominant picks are not applicable to the single-rhythm or uncoupled cells. Exact two-sided McNemar p-values are exploratory, unadjusted; no confirmatory decision is made.\n',md(v3summary),'\n## Exploratory V1/V2/V4 outcomes\n','Strict joint recovery uses fP tolerance 0.5 Hz with fA tolerance 8 Hz. Timing-null joint counts are false joint recovery. No additional hypothesis tests were added for these descriptive outcomes.\n',md(other),'\n## Exploratory diagnostics\n','n_bursts is the number of retained burst-centered epochs returned by bst_apc, not a separately reconstructed pre-edge detection count. The fraction of epochs flipped is **not available** for either version. APC v1.0 does not return its BTA or spectrum, so BTA powers are **not available**. APC v3.0 returns the BTA Welch spectrum; powers below use the nearest returned bin to each truth frequency. Both sampled bin frequencies are recorded per trial; no new spectrum or hidden diagnostic was reconstructed.\n',md(diagnostics), '\n## Exploratory outputs and deviations\n']
for name in ['trial_estimates.csv','summary.csv','mcnemar_exploratory.csv','diagnostics.csv','recovery_by_level.csv','provenance.json','exploratory_noflip.png','exploratory_noflip.svg']:report.append(f'- [{name}]({(O/name).as_posix()})\n')
dev=json.loads((O/'deviations.json').read_text(encoding='utf-8'));report.append('\nDeviations: '+('none.' if not dev['deviations'] else json.dumps(dev['deviations']))+'\n')
report.append('\nWorker runtimes (seconds): '+', '.join(f"{w}: {json.loads((O/f'worker{w}_complete.json').read_text(encoding='utf-8'))['elapsed_seconds']:.3f}" for w in range(1,5))+'.\n')
(O/'RESULTS_noflip.md').write_text('\n'.join(report),encoding='utf-8');(O/'analysis_complete.json').write_text(json.dumps({'status':'COMPLETE','classification':'exploratory','utc':datetime.now(timezone.utc).isoformat(),'inputs':1875,'rows':len(D),'git_commit':P['git_head'],'protocol_sha256':P['protocol_sha256'],'figure':meta},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'COMPLETE','classification':'exploratory','inputs':1875,'rows':len(D)}))
