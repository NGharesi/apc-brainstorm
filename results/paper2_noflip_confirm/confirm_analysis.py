from pathlib import Path
from datetime import datetime,timezone
import sys,os,json,hashlib
O=Path(__file__).resolve().parent;R=O.parent.parent;sys.path.insert(0,str(R/'pydeps'));os.environ['MPLCONFIGDIR']=str(O/'matplotlib_cache')
import numpy as np
import pandas as pd
from scipy.stats import binomtest,norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=json.loads((O/'provenance.json').read_text(encoding='utf-8'))
METHODS=['APC-v1.0-flip','APC-v1.0-noflip','APC-v3.0-flip','APC-v3.0-noflip','F3_A_SCAN','A2_prime_2D','F2nf_A_SCAN']
CELLS=['A_keep100','A_keep040','B_keep100','B_keep040','R_single_keep100','N_uncoupled']
def read(n):return pd.read_csv(O/n,encoding='utf-8',float_precision='round_trip')
def write(d,n):
 d=pd.DataFrame(d);d['classification']='confirmatory';d['git_commit']=P['git_head'];d['protocol_sha256']=P['protocol_sha256'];d['provenance_file']='provenance.json';d.to_csv(O/n,index=False,encoding='utf-8',float_format='%.17g');return d
def wilson(k,n):
 if not n:return np.nan,np.nan
 z=norm.ppf(.975);p=k/n;den=1+z*z/n;c=(p+z*z/(2*n))/den;h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den;return 0. if k==0 else max(0,c-h),1. if k==n else min(1,c+h)
def success(g,metric):
 if metric=='fp':return abs(g.source_fp_hz-g.true_fp_hz)<=1
 if metric=='dominant':return abs(g.source_fp_hz-g.true_fd_hz)<=1
 tol=.5 if metric=='strict' else 1
 return g.valid.astype(bool)&(abs(g.endtoend_fp_hz-g.true_fp_hz)<=tol)&(abs(g.endtoend_fa_hz-g.true_fa_hz)<=8)
def method(g,m):return g[g.method==m].set_index('key').sort_index()
def contrast(g,endpoint,metric,first,second,cohort):
 a=method(g,first);b=method(g,second).reindex(a.index);assert not b.method.isna().any();x=success(a,metric).to_numpy(bool);y=success(b,metric).to_numpy(bool);n10=int((x&~y).sum());n01=int((~x&y).sum());lo1,hi1=wilson(int(x.sum()),len(x));lo2,hi2=wilson(int(y.sum()),len(y))
 return dict(endpoint=endpoint,cohort=cohort,metric=metric,first=first,second=second,n=len(x),first_success=int(x.sum()),first_ci_low=lo1,first_ci_high=hi1,second_success=int(y.sum()),second_ci_low=lo2,second_ci_high=hi2,only_first=n10,only_second=n01,p_exact=1. if n10+n01==0 else float(binomtest(n10,n10+n01,.5).pvalue))
def counts(g,cohort):
 rows=[]
 for name,z in g.groupby('method',sort=False):
  q={'suite':z.suite.iloc[0],'cohort':cohort,'method':name,'n':len(z),'invalid':int((~z.valid.astype(bool)).sum()),'finite_step2_fp':int(z.source_fp_hz.notna().sum())}
  for metric in ['fp','dominant','joint','strict']:
   applicable=metric!='dominant' or z.true_fd_hz.notna().all()
   k=int(success(z,metric).sum()) if applicable else np.nan;lo,hi=wilson(k,len(z)) if applicable else (np.nan,np.nan);q[metric]=k;q[metric+'_ci_low']=lo;q[metric+'_ci_high']=hi
  rows.append(q)
 return rows
def val(x):return 'not applicable' if pd.isna(x) else f'{x:.6g}' if isinstance(x,(float,np.floating)) else str(x)
def md(d):
 cols=[c for c in d if c not in ['classification','git_commit','protocol_sha256','provenance_file']]
 return '| '+' | '.join(cols)+' |\n| '+' | '.join(['---']*len(cols))+' |\n'+''.join('| '+' | '.join(val(v) for v in r)+' |\n' for r in d[cols].itertuples(index=False,name=None))
def display_counts(d):
 rows=[]
 for r in d.itertuples():
  q={'suite':r.suite,'cohort':r.cohort,'method':r.method,'n':r.n}
  for metric in ['fp','dominant','joint','strict']:
   k=getattr(r,metric);q[metric+' [Wilson95CI]']='not applicable' if pd.isna(k) else f"{int(k)} [{getattr(r,metric+'_ci_low'):.4g}, {getattr(r,metric+'_ci_high'):.4g}]"
  rows.append(q)
 return pd.DataFrame(rows)
assert not (O/'analysis_complete.json').exists() and not (O/'STOPPED.md').exists()
for w in range(1,5):assert json.loads((O/f'worker{w}_complete.json').read_text(encoding='utf-8'))['status']=='COMPLETE'
frames=[]
for suite,n in [('W3',600),('W1',350)]:
 d=pd.concat([read(f'{suite}_worker{w}.csv') for w in range(1,5)],ignore_index=True);assert d.key.nunique()==n and len(d)==7*n and not d.duplicated(['key','method']).any() and set(d.method)==set(METHODS);frames.append(d)
D=pd.concat(frames,ignore_index=True).sort_values(['suite','case_index','method']).reset_index(drop=True);write(D,'trial_estimates.csv');w3=D[D.suite=='W3'];w1=D[D.suite=='W1'];pool=w3[w3.scenario.isin(CELLS[:4])]
primary=[contrast(pool,'C1','fp','APC-v3.0-noflip','APC-v3.0-flip','W3_non_dominant_pooled'),contrast(pool,'C2','fp','APC-v1.0-noflip','APC-v1.0-flip','W3_non_dominant_pooled')]
ps=np.array([r['p_exact'] for r in primary]);order=np.argsort(ps);adj=np.minimum(1,np.maximum.accumulate(ps[order]*[2,1]));adjusted=np.empty(2);adjusted[order]=adj
for r,p in zip(primary,adjusted):r['p_holm']=float(p);r['significant']=bool(p<.05)
if any(r['significant'] and r['first_success']>r['second_success'] for r in primary):decision='polarity alignment suppresses recovery of a coupled non-dominant rhythm (confirmed)'
elif any(r['significant'] and r['first_success']<r['second_success'] for r in primary):decision='not confirmed; reversed'
else:decision='not confirmed'
prim=write(primary,'primary_C1_C2.csv');sec=[]
for first in ['APC-v3.0-noflip','F2nf_A_SCAN']:sec.append(contrast(pool,'S1','joint',first,'A2_prime_2D','W3_non_dominant_pooled'))
null=w3[w3.scenario=='N_uncoupled']
for v in ['v1.0','v3.0']:sec.append(contrast(null,'S2','joint','APC-'+v+'-noflip','APC-'+v+'-flip','W3_N_uncoupled'))
coupled=w1[w1.dataset=='coupled'];null1=w1[w1.dataset=='timing_null']
for v in ['v1.0','v3.0']:
 for metric in ['joint','strict']:sec.append(contrast(coupled,'S3',metric,'APC-'+v+'-noflip','APC-'+v+'-flip','W1_coupled'))
 sec.append(contrast(null1,'S3','joint','APC-'+v+'-noflip','APC-'+v+'-flip','W1_timing_null'))
for metric in ['joint','strict']:sec.append(contrast(coupled,'S3',metric,'F2nf_A_SCAN','F3_A_SCAN','W1_coupled'))
sec.append(contrast(null1,'S3','joint','F2nf_A_SCAN','F3_A_SCAN','W1_timing_null'));secondary=write(sec,'secondary_tests.csv');write(primary+sec,'statistics.csv')
rows=[]
for cell in CELLS:rows.extend(counts(w3[w3.scenario==cell],cell))
rows.extend(counts(pool,'non_dominant_pooled'));celltable=write(rows,'W3_counts.csv');rows=[]
for dataset,g in w1.groupby('dataset',sort=False):rows.extend(counts(g,dataset))
w1table=write(rows,'W1_counts.csv');levels=[]
for keys,g in D.groupby(['suite','scenario','dataset','level'],sort=False):levels.extend(counts(g,' / '.join(map(str,keys[1:]))))
write(levels,'recovery_by_level.csv')
diag=[]
for (cell,name),g in pool[pool.method.isin(['APC-v3.0-flip','APC-v3.0-noflip'])].groupby(['scenario','method'],sort=False):
 diag.append(dict(cell=cell,method=name,n=len(g),finite_pairs=int((g.bta_power_coupled.notna()&g.bta_power_dominant.notna()).sum()),mean_coupled_power=g.bta_power_coupled.mean(),median_coupled_power=g.bta_power_coupled.median(),mean_dominant_power=g.bta_power_dominant.mean(),median_dominant_power=g.bta_power_dominant.median(),coupled_sampled_hz=g.bta_sampled_coupled_hz.median(),dominant_sampled_hz=g.bta_sampled_dominant_hz.median()))
power=write(diag,'BTA_power.csv')
plt.rcParams.update({'svg.fonttype':'none','font.family':'DejaVu Sans','font.size':8,'axes.spines.top':False,'axes.spines.right':False});fig,axs=plt.subplots(1,3,figsize=(19,6));colors=['#355d91','#93b4db','#ae681b','#e4b76b','#368b74','#999999','#805aa8']
panels=[(axs[0],celltable,CELLS,'fp','W3 reference-fP recovery proportion'),(axs[1],celltable,CELLS[:4],'dominant','W3 dominant-rhythm pick proportion'),(axs[2],w1table,['coupled','timing_null'],'joint','W1 joint / false-joint recovery proportion')]
for ax,table,cells,metric,label in panels:
 for j,name in enumerate(METHODS):
  q=table[table.method==name].set_index('cohort').reindex(cells);x=np.arange(len(cells))+(j-3)*.115;y=q[metric].to_numpy()/q.n.to_numpy();lo=q[metric+'_ci_low'].to_numpy();hi=q[metric+'_ci_high'].to_numpy();ax.bar(x,y,width=.11,color=colors[j],label=name.replace('A2_prime_2D',"A2-prime").replace('_A_SCAN','/SCAN'));ax.errorbar(x,y,yerr=np.maximum(0,np.vstack([y-lo,hi-y])),fmt='none',color='black',capsize=1,lw=.5)
 ax.set_xticks(np.arange(len(cells)),cells,rotation=35,ha='right');ax.set_ylim(0,1.36);ax.set_yticks(np.arange(0,1.01,.2));ax.set_ylabel(label);ax.set_xlabel('Cell / cohort');ax.grid(axis='y',alpha=.2)
axs[0].legend(ncol=2,fontsize=6,loc='upper left');fig.tight_layout();source=O/'W3_counts.csv';meta={'classification':'confirmatory','git_commit':P['git_head'],'protocol_sha256':P['protocol_sha256'],'sources':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [source,O/'W1_counts.csv']]};desc=json.dumps(meta);fig.savefig(O/'confirmation.png',dpi=300,metadata={'Description':desc});fig.savefig(O/'confirmation.svg',metadata={'Description':desc,'Creator':'APC no-flip confirmation'});plt.close(fig)
report=['# Confirmatory polarity-alignment analysis\n',f"Archive commit and successful push: `{P['archive_commit']}`. Protocol `{P['initial_protocol_commit']}`, SHA-256 `{P['protocol_sha256']}`. No signal was generated before that push.\n",'## Generator check\n','PASS: first repeat in each of six V3 cells at seed 20261112 and first V1 trial at seed 20261110 were bit-identical in signal and time. The unchanged full streams were advanced as needed; no method ran on check signals or unused HB scenarios. W3 then used seed 20261120 (600 trials); W1 used 20261121 (175 coupled and 175 paired timing nulls).\n','## Primary C1/C2\n',f'**{decision}**\n','Coupled-rhythm Step-2 fP recovery within 1 Hz, four non-dominant W3 cells pooled (n=400). Exact two-sided McNemar; Holm over C1/C2 only. Wilson 95% CIs.\n',md(prim),'## Key secondary 1-3: comparisons\n','Secondary McNemar tests are exact, two-sided and unadjusted. Joint requires fP within 1 Hz and fA within 8 Hz; strict uses fP within 0.5 Hz. Invalid end-to-end outputs count as failures. Joint recovery in null cohorts is false joint recovery.\n',md(secondary),'## Key secondary 4: W3 per-cell counts\n','fP and dominant picks use the source estimate independently of later APC failure. For N_uncoupled, fP recovery uses the nominal 8-Hz reference and joint counts are false recovery. Dominant picks are not applicable to single-rhythm/control cells. Brackets are Wilson 95% proportion intervals.\n',md(display_counts(celltable)),'## W1 coupled and paired timing-null counts\n',md(display_counts(w1table)),'## Key secondary 5: returned v3 BTA power\n','Continuous BTA Welch power is reported as mean and median, not with Wilson intervals (which apply to counts). Nearest returned frequency bins are recorded; no spectrum was reconstructed and src was not instrumented.\n',md(power),'## Implementation and provenance\n','All validation settings and frozen source are unchanged except the prespecified flip option. F3/SCAN and A2-prime use the unchanged validation adapters. F2nf/SCAN calls the unchanged scan_fa_given_fp.m: its W3 score vector is restricted to the exact validation candidates 88:4:148 before the same first-maximum tie rule; unused extra candidate scores do not enter selection. W1 uses the helper full grid unchanged. Per-trial options/settings and signal hashes are recorded.\n','## Outputs and deviations\n']
for name in ['trial_estimates.csv','statistics.csv','primary_C1_C2.csv','secondary_tests.csv','W3_counts.csv','W1_counts.csv','recovery_by_level.csv','BTA_power.csv','generator_check.json','provenance.json','confirmation.png','confirmation.svg']:report.append(f'- [{name}]({(O/name).as_posix()})\n')
dev=json.loads((O/'deviations.json').read_text(encoding='utf-8'));report.append('\nDeviations: '+('none.' if not dev['deviations'] else json.dumps(dev['deviations']))+'\n');report.append('\nWorker elapsed seconds: '+', '.join(f"{w}: {json.loads((O/f'worker{w}_complete.json').read_text(encoding='utf-8'))['elapsed_seconds']:.3f}" for w in range(1,5))+'. New confirmation results are uncommitted.\n');(O/'RESULTS_confirm.md').write_text('\n'.join(report),encoding='utf-8');result={'status':'COMPLETE','classification':'confirmatory','decision':decision,'inputs':950,'rows':len(D),'utc':datetime.now(timezone.utc).isoformat(),'git_commit':P['git_head'],'protocol_sha256':P['protocol_sha256'],'figure':meta};(O/'analysis_complete.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
