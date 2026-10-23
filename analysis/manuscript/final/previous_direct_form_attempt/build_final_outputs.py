from pathlib import Path
import os,sys,json,hashlib,time,math,csv
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=ROOT/'revision_checks/final'
sys.path.insert(0,str(ROOT/'pydeps'));os.environ['MPLCONFIGDIR']=str(OUT/'plot_config')
import numpy as np
import pandas as pd
from scipy import stats,special
from scipy.io import loadmat
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

START=time.perf_counter()
COMMIT='71ebc16aed32ca38be73a800738b975e5806b330'
V2='217fd8373759150cdeffe794d231a7cec2225f38'
META=json.loads((OUT/'analysis_provenance.json').read_text(encoding='utf-8'))
META['canonical_generator']=json.loads((OUT/'canonical_provenance.json').read_text(encoding='utf-8'))
META['bootstrap']={'seed':20261022,'resamples':10000,'sampling':'independent uniform bout resampling within each state; shared indices across methods/metrics','CI':'percentile 2.5/97.5','weighted':'resample bout values and durations together; normalize durations within each state','weighted_variance':'sum(p*(x-mean)^2)/(1-sum(p^2))','weighted_effective_n':'1/sum(p^2)','weighted_t':'Welch with unbiased weighted variances and Kish effective n','Hedges_g':'pooled SD; exact gamma correction J(df), df=n_run+n_rest-2, Kish n for weighted sensitivity'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','axes.titlesize':11,'legend.fontsize':9})
LABELS=['APC v1.0','MVL-raw','MVL-Ozkurt','KLMI','GLM']
COLORS={'APC v1.0':'#222222','MVL-raw':'#D55E00','MVL-Ozkurt':'#0072B2','KLMI':'#AA3377','GLM':'#009E73','APC v2.0':'#CC3311'}
FIGURES=[]
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def read(p):return pd.read_csv(p)
def provenance(sources):
 return dict(META,source_files=[{'path':str(Path(p).resolve()),'sha256':sha(p)} for p in sources],heldout_evaluation_commit=V2)
def savecsv(df,name,sources):
 p=OUT/name;df=df.copy();df['method_git_commit']=COMMIT;df['provenance_json']=json.dumps(provenance(sources),separators=(',',':'));df.to_csv(p,index=False,encoding='utf-8');return p
def finish(fig,name,title,sources,note=''):
 prov=provenance(sources);text=json.dumps(prov,separators=(',',':'))
 fig.suptitle(title,fontsize=15,fontweight='bold',y=.987)
 fig.text(.5,.013,f'APC v1.0 {COMMIT[:8]} | Sources: '+', '.join(Path(p).name for p in sources)+'\n'+note,ha='center',va='bottom',fontsize=7,color='#444444',wrap=True)
 fig.subplots_adjust(top=.9,bottom=.12,wspace=.27,hspace=.42)
 png=OUT/(name+'.png');svg=OUT/(name+'.svg')
 fig.savefig(png,dpi=300,metadata={'Description':text,'Software':'APC final analysis'})
 fig.savefig(svg,metadata={'Description':text,'Creator':'APC final analysis'})
 plt.close(fig);FIGURES.append({'name':name,'title':title,'png':str(png),'svg':str(svg),'sources':[str(p) for p in sources],'provenance':prov})
def table(df,cols,labels=None):
 def fmt(v):
  if isinstance(v,(float,np.floating)):return 'NA' if not np.isfinite(v) else f'{v:.6g}'
  return str(v)
 return '| '+' | '.join(labels or cols)+' |\n| '+' | '.join(['---']*len(cols))+' |\n'+'\n'.join('| '+' | '.join(fmt(r[c]) for c in cols)+' |' for _,r in df.iterrows())+'\n'
def link(p,label=None):return f'[{label or Path(p).name}](<{Path(p).resolve().as_posix()}>)'

rod=read(OUT/'rodent_bouts.csv');assert len(rod)==120 and rod.groupby(['state','method']).size().eq(12).all()
bootrng=np.random.default_rng(20261022);ix=bootrng.integers(0,12,size=(10000,12));iy=bootrng.integers(0,12,size=(10000,12))
statrows=[];summaries=[]
for method in LABELS:
 d=rod[rod.method==method].sort_values('bout');run=d[d.state=='run'];rest=d[d.state=='rest']
 for state,g in [('run',run),('rest',rest)]:
  summaries.append(dict(method=method,state=state,n_bouts=len(g),duration_total_s=g.duration_s.sum(),fP_mean=g.fP_hz.mean(),fA_mean=g.fA_hz.mean(),ozkurt_mean=g.ozkurt_mvl.mean(),fP_weighted=np.average(g.fP_hz,weights=g.duration_s),fA_weighted=np.average(g.fA_hz,weights=g.duration_s),ozkurt_weighted=np.average(g.ozkurt_mvl,weights=g.duration_s),boundary_4=int(g.boundary_fP_4.sum()),boundary_12=int(g.boundary_fP_12.sum())))
 for metric in ['fP_hz','fA_hz','ozkurt_mvl']:
  x=run[metric].to_numpy();y=rest[metric].to_numpy();wx=run.duration_s.to_numpy();wy=rest.duration_s.to_numpy()
  assert np.isfinite(x).all() and np.isfinite(y).all()
  for weighted in [False,True]:
   a=wx/wx.sum() if weighted else np.ones(12)/12;b=wy/wy.sum() if weighted else np.ones(12)/12
   nx=1/np.sum(a*a);ny=1/np.sum(b*b);mx=np.sum(a*x);my=np.sum(b*y)
   vx=np.sum(a*(x-mx)**2)/(1-np.sum(a*a));vy=np.sum(b*(y-my)**2)/(1-np.sum(b*b));se2=vx/nx+vy/ny
   df=se2**2/((vx/nx)**2/(nx-1)+(vy/ny)**2/(ny-1)) if se2>0 else np.inf
   t=(mx-my)/np.sqrt(se2) if se2>0 else (0 if mx==my else np.sign(mx-my)*np.inf)
   p=2*stats.t.sf(abs(t),df);pooled=np.sqrt(((nx-1)*vx+(ny-1)*vy)/(nx+ny-2));gd=nx+ny-2
   J=np.exp(special.gammaln(gd/2)-.5*np.log(gd/2)-special.gammaln((gd-1)/2));g=J*(mx-my)/pooled if pooled>0 else np.nan
   if weighted:bd=(x[ix]*wx[ix]).sum(1)/wx[ix].sum(1)-(y[iy]*wy[iy]).sum(1)/wy[iy].sum(1)
   else:bd=x[ix].mean(1)-y[iy].mean(1);t2=stats.ttest_ind(x,y,equal_var=False);assert np.isclose(t,t2.statistic) and np.isclose(p,t2.pvalue)
   lo,hi=np.percentile(bd,[2.5,97.5]);statrows.append(dict(method=method,metric=metric,weighting='duration' if weighted else 'equal_bout',n_run=12,n_rest=12,effective_n_run=nx,effective_n_rest=ny,run_mean=mx,rest_mean=my,mean_difference=mx-my,welch_t=t,welch_df=df,p_two_sided=p,hedges_g=g,bootstrap_ci_low=lo,bootstrap_ci_high=hi,bootstrap_resamples=10000,seed=20261022))
STAT=pd.DataFrame(statrows);SUM=pd.DataFrame(summaries)
STATFILE=savecsv(STAT,'rodent_run_rest_statistics.csv',[OUT/'rodent_bouts.csv'])
SUMFILE=savecsv(SUM,'rodent_state_summary.csv',[OUT/'rodent_bouts.csv'])

# Canonical figures, rebuilt from verified frozen-method diagnostics.
CAN=read(OUT/'canonical_results.csv');NAMES=['burst_coupled','timing_null','jittered','continuous_pac'];D={}
for n in NAMES:
 D[n]=loadmat(OUT/(n+'_diagnostics.mat'),simplify_cells=True)['d']
 d=D[n];tf=d['phase_locked_tf'];freq=np.asarray(d['phase_locked_freqs']).ravel();tm=np.asarray(d['phase_epoch_time']).ravel()
 data=pd.DataFrame({'time_s':np.tile(tm,len(freq)),'frequency_hz':np.repeat(freq,len(tm)),'amplitude':tf.ravel()})
 savecsv(data,n+'_tf.csv',[OUT/(n+'_traces.csv'),OUT/'canonical_results.csv'])
def axesclean(ax,x,y,title,xlabel,ylabel):ax.plot(x,y,color='#222222',lw=1);ax.set(title=title,xlabel=xlabel,ylabel=ylabel);ax.grid(alpha=.15)
def phasebins(d):
 p=d['phase_angles'];a=d['amplitude_envelope'];edges=np.linspace(-np.pi,np.pi,19);return (edges[:-1]+edges[1:])/2,np.array([a[(p>=edges[i])&(p<edges[i+1])].mean() for i in range(18)])
n='burst_coupled';d=D[n];tr=read(OUT/(n+'_traces.csv'));spec=read(OUT/(n+'_spectrum.csv'));cr=CAN[CAN.state==n].iloc[0]
fig,axs=plt.subplots(3,3,figsize=(13.5,10));a=axs.ravel();sel=tr.time_s<=2
axesclean(a[0],tr.time_s[sel],tr.signal[sel],'A  Signal (first 2 s of 20 s)','Time (s)','Amplitude')
axesclean(a[1],tr.time_s[sel],tr.burst_trace[sel],'B  Broadband burst trace','Time (s)','RMS CWT')
loc=np.asarray(d['burst_locs']).astype(int)-1;loc=loc[tr.time_s.iloc[loc].to_numpy()<=2];a[1].scatter(tr.time_s.iloc[loc],tr.burst_trace.iloc[loc],s=15,color='#D55E00',zorder=3)
axesclean(a[2],d['time_epoch'],d['burst_average'],'C  Burst-triggered average','Time from burst (s)','Amplitude')
ss=spec[(spec.frequency_hz>=1)&(spec.frequency_hz<=30)];axesclean(a[3],ss.frequency_hz,ss.power,f'D  Recovered fP = {cr.fP_hz:.3f} Hz','Frequency (Hz)','Welch power');a[3].axvline(cr.fP_hz,color='#0072B2',ls='--')
axesclean(a[4],d['phase_epoch_time'],d['phase_locked_average'],'E  Trough-triggered average','Time from trough (s)','Amplitude')
im=a[5].pcolormesh(d['phase_epoch_time'],d['phase_locked_freqs'],d['phase_locked_tf'],shading='auto',cmap='magma');a[5].set(title='F  Trough-locked time–frequency map',xlabel='Time from trough (s)',ylabel='Frequency (Hz)');a[5].axhline(cr.fA_hz,color='cyan',ls='--',lw=1);fig.colorbar(im,ax=a[5],label='CWT magnitude',fraction=.046)
axesclean(a[6],d['fa_grid'],d['fa_score'],f'G  Recovered fA = {cr.fA_hz:.0f} Hz','Candidate fA (Hz)','Envelope–waveform correlation');a[6].axvline(cr.fA_hz,color='#D55E00',ls='--')
p=tr.phase_signal[sel].to_numpy();e=tr.amplitude_envelope[sel].to_numpy();a[7].plot(tr.time_s[sel],p/np.std(p),color='#0072B2',label='Phase-band signal / SD');a[7].plot(tr.time_s[sel],e/np.sqrt(np.mean(e**2)),color='#D55E00',label='Envelope / RMS');a[7].set(title='H  Final phase signal and envelope',xlabel='Time (s)',ylabel='Normalized amplitude');a[7].legend(fontsize=7)
ph,am=phasebins(d);a[8].plot(np.rad2deg(ph),am,'o-',color='#222222');a[8].axvline(cr.preferred_phase_deg,color='#D55E00',ls='--');a[8].set(title=f'I  Raw MVL {cr.raw_mvl:.4g}; Ozkurt {cr.ozkurt_mvl:.4g}',xlabel='Hilbert phase (degrees)',ylabel='Mean envelope');a[8].text(.04,.95,f'Preferred phase {cr.preferred_phase_deg:.1f}°',transform=a[8].transAxes,va='top',fontsize=9)
finish(fig,'Figure_1_workflow','Figure 1. APC v1.0 canonical workflow',[OUT/'canonical_results.csv',OUT/'burst_coupled_traces.csv',OUT/'burst_coupled_spectrum.csv',OUT/'burst_coupled_fa_score.csv',OUT/'burst_coupled_tf.csv'],'20 s; true fP/fA = 8/120 Hz; fs = 500 Hz; generator seed 12345; amplitude search 80–150 Hz.')
fig,axs=plt.subplots(4,4,figsize=(14,11));titles=['Burst-coupled','Timing null (Poisson)','Jittered (SD 20 ms)','Continuous PAC']
for j,n in enumerate(NAMES):
 d=D[n];tr=read(OUT/(n+'_traces.csv'));r=CAN[CAN.state==n].iloc[0];sp=read(OUT/(n+'_spectrum.csv'));sel=(tr.time_s>=1)&(tr.time_s<=2)
 axesclean(axs[0,j],tr.time_s[sel],tr.signal[sel],titles[j],'Time (s)','Signal')
 axesclean(axs[1,j],d['time_epoch'],d['burst_average'],f'fP = {r.fP_hz:.3f}; fA = {r.fA_hz:.0f} Hz','Time from burst (s)','Burst average')
 ss=sp[(sp.frequency_hz>=1)&(sp.frequency_hz<=30)];axesclean(axs[2,j],ss.frequency_hz,ss.power,'Burst-average spectrum','Frequency (Hz)','Welch power');axs[2,j].axvline(r.fP_hz,color='#0072B2',ls='--')
 ph,am=phasebins(d);axesclean(axs[3,j],np.rad2deg(ph),am,f'Raw MVL {r.raw_mvl:.3g}; Oz {r.ozkurt_mvl:.3g}','Hilbert phase (degrees)','Mean envelope')
for i in [0,1]:
 limits=[ax.get_ylim() for ax in axs[i]];lo=min(x[0] for x in limits);hi=max(x[1] for x in limits)
 for ax in axs[i]:ax.set_ylim(lo,hi)
finish(fig,'Figure_2_canonical_conditions','Figure 2. Four canonical conditions analyzed with frozen APC v1.0',[OUT/'canonical_results.csv']+[OUT/(n+'_traces.csv') for n in NAMES],'20 s each; 8/120 Hz; timing null: 8 events/s on [0.5,19.5] s, 174 realized events, separate seed 20261022; jitter SD 0.020 s.')

# Held-out plots: use the existing candidate-3 CSVs only; no simulation reruns.
HD=ROOT/'revision_checks/v2/candidate_03';REC=read(HD/'heldout_recovery_summary.csv');AUC=read(HD/'heldout_null_specificity_auc.csv')
def chosen(df,v2=False):
 mask=((df.configuration=='v1.0')&(df.method=='APC'))|(df.configuration=='A2_prime')
 if v2:mask|=(df.configuration=='v2.0')&(df.method=='APC')
 x=df[mask].copy();x['label']=np.where(x.configuration=='v1.0','APC v1.0',np.where(x.configuration=='v2.0','APC v2.0',x.method));return x
H=chosen(REC);HFILE=savecsv(H,'heldout_v1_A2_recovery.csv',[HD/'heldout_recovery_summary.csv'])
U=chosen(AUC);U=U[(U.dataset=='timing_null')&(U.score_field=='score')];UFILE=savecsv(U,'heldout_v1_A2_timing_null_auc.csv',[HD/'heldout_null_specificity_auc.csv'])
def wilson(k,n):
 z=stats.norm.ppf(.975);p=np.asarray(k)/np.asarray(n);den=1+z*z/np.asarray(n);mid=(p+z*z/(2*np.asarray(n)))/den;half=z*np.sqrt(p*(1-p)/np.asarray(n)+z*z/(4*np.asarray(n)**2))/den;return mid-half,mid+half
def recover(ax,df,field,title,ci=True,labels=LABELS):
 levels=sorted(df.level.unique());pos={v:i for i,v in enumerate(levels)}
 for j,label in enumerate(labels):
  g=df[df.label==label].sort_values('level');x=np.array([pos[v] for v in g.level])+(j-(len(labels)-1)/2)*.055;y=g[field].to_numpy()/g.n_trials.to_numpy()
  ax.plot(x,y,'o-',color=COLORS[label],label=label,ms=3,lw=1.3)
  if ci:
   lo,hi=wilson(g[field],g.n_trials);ax.errorbar(x,y,yerr=[y-lo,hi-y],fmt='none',color=COLORS[label],alpha=.5,capsize=2,lw=.7)
 ax.set(title=title,xticks=range(len(levels)),xticklabels=[f'{v:g}' for v in levels],ylim=(-.04,1.04),ylabel='Proportion / 25');ax.grid(axis='y',alpha=.18)
def legend(fig,axs,ncol=5):
 handles,labels=np.asarray(axs).ravel()[0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.945),ncol=ncol,frameon=False)
fig,axs=plt.subplots(2,2,figsize=(12,9))
for j,(scenario,label) in enumerate([('H1_sparsity','Keep rate'),('H1_distractor','Distractor scale')]):
 sub=H[(H.scenario==scenario)&(H.dataset=='coupled')]
 for i,field in enumerate(['joint','strict_joint']):recover(axs[i,j],sub,field,scenario.replace('_',' ')+' — '+('joint' if i==0 else 'strict joint'));axs[i,j].set_xlabel(label)
legend(fig,axs);finish(fig,'Figure_3_H1_recovery','Figure 3. Held-out H1 recovery: APC v1.0 and A2′',[HFILE],'Wilson 95% CIs; joint: |fP error| ≤1 Hz and |fA error| ≤8 Hz; strict joint: phase tolerance 0.5 Hz; invalid estimates count as failures.')
fig,axs=plt.subplots(1,2,figsize=(12,5.5));sub=H[(H.scenario=='H2')&(H.dataset=='coupled')]
for ax,field,title in zip(axs,['joint','picks_near_fD'],['Joint recovery','Picks within 1 Hz of uncoupled fD']):recover(ax,sub,field,title);ax.set_xlabel('Uncoupled / coupled slow-rhythm amplitude ratio')
legend(fig,axs);finish(fig,'Figure_4_H2_recovery','Figure 4. Held-out H2 recovery and distractor-frequency picks',[HFILE],'Wilson 95% CIs; true fP ~ U(4,7), fD ~ U(fP+3,13), fA ~ U(90,140) Hz; 25 trials per ratio.')
fig,axs=plt.subplots(2,3,figsize=(15,8))
for j,scenario in enumerate(['H1_sparsity','H1_distractor','H2']):
 sub=U[U.scenario==scenario].copy();sub['n_trials']=sub.n_null;recover(axs[0,j],sub,'false_joint',scenario.replace('_',' ')+' timing null')
 levels=sorted(sub.level.unique())
 for label in LABELS:
  g=sub[sub.label==label].sort_values('level');axs[1,j].plot(range(len(g)),g.auc,'o-',label=label,color=COLORS[label],ms=4)
 axs[1,j].axhline(.5,color='#888888',ls=':',lw=1);axs[1,j].set(xticks=range(len(levels)),xticklabels=[f'{v:g}' for v in levels],ylim=(0,1.04),ylabel='Coupled vs timing-null AUC',xlabel=['Keep rate','Distractor scale','Slow-rhythm amplitude ratio'][j]);axs[1,j].grid(axis='y',alpha=.18)
 axs[0,j].set_ylabel('False joint recovery / 25')
legend(fig,axs);finish(fig,'Figure_5_null_specificity','Figure 5. Timing-null false recovery and score AUC',[UFILE],'False recovery: Wilson 95% CIs. AUC uses raw APC C_APC and each comparator’s own selected score; 25 coupled / 25 null per level; half credit for ties.')

# Development-suite sensitivity: common 1-Hz main grid; both random-fP grids.
V1=ROOT/'revision_checks/v1_rerun';FU=ROOT/'revision_checks/v1_followup'
def devplot(kind,step,name):
 source1=V1/('main_summary.csv' if kind=='main' else 'random_fp_summary.csv');source2=FU/('a2_main_summary.csv' if kind=='main' else 'a2_random_fp_summary.csv')
 a=read(source1);b=read(source2);a=a[(a.configuration.isin(['v1.0','A0','A1']))&(a.dataset=='coupled')];b=b[(b.configuration=='A2')&(b.dataset=='coupled')&(b.fp_grid_step_hz==step)]
 if kind!='main':a=a[(a.configuration=='v1.0')|(a.fp_grid_step_hz==step)]
 a=a.rename(columns={'joint_recovery':'joint'});b=b.rename(columns={'joint_recovery':'joint'});dev=pd.concat([a,b],ignore_index=True)
 p=savecsv(dev,f'{name}_source.csv',[source1,source2]);fig,axs=plt.subplots(4,2,figsize=(12,13));metrics=['MVL-raw','MVL-Ozkurt','KLMI','GLM']
 for i,metric in enumerate(metrics):
  for j,bench in enumerate(['sparsity','distractor']):
   ax=axs[i,j];s=dev[dev.benchmark==bench];ap=s[s.configuration=='v1.0'].sort_values('level');levels=sorted(s.level.unique());pos={v:k for k,v in enumerate(levels)};ax.plot([pos[v] for v in ap.level],ap.joint/ap.n_trials,'o-',color='#222222',label='APC v1.0',ms=3)
   for conf,style in [('A0','--'),('A1',':'),('A2','-')]:
    g=s[(s.configuration==conf)&s.method.str.replace('-scan','',regex=False).eq(metric)].sort_values('level');assert len(g)==len(levels),(kind,step,conf,metric,len(g));ax.plot([pos[v] for v in g.level],g.joint/g.n_trials,style,marker='o',ms=3,label=conf,color={'A0':'#0072B2','A1':'#D55E00','A2':'#009E73'}[conf])
   ax.set(title=f'{bench.title()} — {metric}',xticks=range(len(levels)),xticklabels=[f'{v:g}' for v in levels],ylim=(-.04,1.04),ylabel='Joint recovery / 25',xlabel='Keep rate' if j==0 else 'Distractor scale');ax.grid(axis='y',alpha=.15)
 legend(fig,axs,ncol=4);finish(fig,name,f'Development suite: {kind.replace("_"," ")}, comparator fP step {step:g} Hz',[p],'Amplitude grid 80:8:152 Hz; A0 half-width 6 Hz, A1 half-width candidate fP, A2 half-width 12 Hz; original saved development inputs/results.')
devplot('main',1,'Supplement_S1_development_main');devplot('random_fp',1,'Supplement_S2_development_random_1Hz');devplot('random_fp',.5,'Supplement_S3_development_random_05Hz')
NEG=chosen(REC,v2=True);NP=savecsv(NEG,'heldout_v2_negative_recovery.csv',[HD/'heldout_recovery_summary.csv']);fig,axs=plt.subplots(2,3,figsize=(15,9))
for j,scenario in enumerate(['H1_sparsity','H1_distractor','H2']):
 sub=NEG[(NEG.scenario==scenario)&(NEG.dataset=='coupled')]
 for i,field in enumerate(['joint','strict_joint']):recover(axs[i,j],sub,field,scenario.replace('_',' ')+' — '+('joint' if i==0 else 'strict joint'),labels=LABELS+['APC v2.0']);axs[i,j].set_xlabel(['Keep rate','Distractor scale','Slow-rhythm amplitude ratio'][j])
legend(fig,axs,ncol=6);finish(fig,'Supplement_S4_v2_negative','APC v2.0 held-out evaluation: prespecified criteria C1 FAIL, C2 PASS, C3 FAIL, C4 FAIL',[NP],'Negative result; frozen v2.0 commit 217fd837. Wilson 95% CIs; no method parameters changed after freezing.')
(OUT/'figure_manifest.json').write_text(json.dumps({'metadata':META,'figures':FIGURES},indent=2),encoding='utf-8')

e=json.loads((OUT/'channel_evidence.json').read_text(encoding='utf-8'));canon=CAN.copy()
lines=['# Final APC v1.0 results','',f'Primary method: tag **v1.0**, commit `{COMMIT}`. All new APC analyses execute byte-identical files extracted from that tag. No tagged code, tags, prior simulation inputs or saved results were modified. APC v2.0 remains a negative result (C1 FAIL, C2 PASS, C3 FAIL, C4 FAIL).','',
'## Rodent channel evidence','',
'EC013/ec013.157, extracted recording R2: **E1, Brainstorm row/channel index 1 (one-based)**. R2.Description is E1; R2.Comment records extraction of E1 over 0–631.199 s; R2.History identifies `EC013/ec013.157.eeg/data_block001.mat`. The imported channel file names its first entry E1. The saved 65-channel crop row 1 matches R2 samples 40800:372501 exactly across all 331,702 samples (maximum absolute difference 0). Its Time vector restarts at zero; it does not retain the absolute R2 timestamps.','',
'**Shank and anatomical layer: unresolved.** No session XML or explicit acquisition-channel-to-shank/layer map was found in the inspected local LFP tree. The E1 channel record has empty Group/Comment and zero coordinates. The original raw-file link points to `/Users/lucwilson/Desktop/crcns/hc3/ec013/ec013.157/ec013.157.eeg`, which is not the local data location. E1 alone does not establish an XML zero-based channel index, shank or layer. No CA1 or layer label is assigned. The public [CRCNS hc-3 page](https://crcns.org/data-sets/hc/hc-3) identifies the dataset but provides no E1-specific mapping; the session discussion on CRCNS concerns cell/shank labels and does not map this LFP channel.','',
'Evidence, exact paths and extraction/import histories: '+link(OUT/'channel_evidence.json')+'. Local session inventory: '+link(OUT/'local_data_inspection.json')+'.','',
'## Bout definitions and analysis','',
'The original saved `apc_ec013_run_rest_results.mat` supplies all 12 run and 12 rest bouts and their sample indices. No bout was split, merged, reclassified or reselected. Sample rate is 1250 Hz. Original analysis indices: 40800:372501; original threshold |speed| >6; minimum bout duration 5 s. Definitions: '+link(OUT/'bout_definitions.csv')+'.','',
'APC: amplitude range [80,150] Hz, all other v1.0 defaults. No surrogate normalization is enabled; C_APC is raw Canolty MVL. Ozkurt MVL is raw MVL / sqrt(mean(A²)), using the exact final v1 Gaussian-free Butterworth envelope and phase. Preferred phase is the angle of mean(A exp(i phase)), in degrees. A separate diagnostic copy only exports intermediate arrays; every rodent/canonical output and runInfo was checked exactly against the untouched frozen function.','',
'A2′ rodent scans: independent maxima for MVL-raw, MVL-Ozkurt, KLMI and GLM, phase grid 4:0.5:12 Hz, phase half-width 1.5 Hz, amplitude grid 80:4:148 Hz, fixed amplitude half-width 12 Hz. Filters and metric formulas follow the inherited comparators: butter(4)/filtfilt, 18 KL bins, GLM R². Ozkurt MVL is additionally reported at the frequency pair selected by each metric. A2′ held-out plots retain their original grids 3:0.5:14 and 80:4:160 Hz and fixed 14-Hz amplitude half-width; they are not recomputed with the rodent settings.','',
'All per-bout method results: '+link(OUT/'rodent_bouts.csv')+'.','']
for method in LABELS:
 lines+=['### '+method,'',table(rod[rod.method==method],['state','bout','duration_s','fP_hz','fA_hz','score','raw_mvl','ozkurt_mvl','preferred_phase_deg']), '']
lines+=['## Run versus rest statistics','',
'Effect direction is run minus rest. Primary estimates weight each bout equally. Welch t and its Satterthwaite df are two-sided; Hedges g uses the pooled within-state SD and the exact small-sample gamma correction. The percentile 95% CI uses 10,000 independent resamples of 12 bouts per state, seed 20261022, with the same resample indices for every method/metric. No multiple-comparison adjustment is applied.','',
'The duration sensitivity normalizes durations within each state; weighted variance is sum[p(x−mean)²]/(1−sum[p²]), effective n is 1/sum[p²], and Welch t/df and pooled Hedges g use these weighted variances and effective sample sizes. This is a specified weighted approximation, not 24 independent session/animal measurements. Bootstrap resampling keeps each bout value and duration together and recomputes the weighted mean.','',
'Full statistics: '+link(STATFILE)+'. State means, weighted means, durations and boundary counts: '+link(SUMFILE)+'.','']
for weight in ['equal_bout','duration']:
 lines+=['### '+('Equal bout weighting' if weight=='equal_bout' else 'Duration-weighted sensitivity'),'',table(STAT[STAT.weighting==weight],['method','metric','run_mean','rest_mean','mean_difference','welch_t','welch_df','p_two_sided','hedges_g','bootstrap_ci_low','bootstrap_ci_high']), '']
lines+=['### State summaries and boundary picks','',table(SUM,['method','state','n_bouts','duration_total_s','fP_mean','fA_mean','ozkurt_mean','fP_weighted','fA_weighted','ozkurt_weighted','boundary_4','boundary_12']), '',
'APC has no 4–12 Hz search constraint; its boundary counts here simply count exact fP=4 or fP=12 outputs, as requested. Comparator boundary counts refer to the actual rodent scan endpoints.','',
'### Optional additional sessions','',
'Eight other EC013 sessions are present locally (156, 205, 206, 208, 251, 252, 374, 375), but none has saved run/rest trial files in the inspected Brainstorm session folders. Only the 157 session has the existing behavior split. No other session with documented ≥8 run and ≥8 rest bouts of ≥5 s was established locally; optional replication was not run. No additional session data were downloaded.','',
'## Canonical examples','',
'The 20-s 8/120-Hz burst-coupled, jittered and continuous examples were regenerated using the existing Python generator and original PCG64 seed/order 12345; each matches its historical signal CSV to 1e-14. Parameters: fs=500 Hz, burst sigma=30 ms, burst amplitude=1.8, baseline HF amplitude=.15, low amplitude=1, white-noise SD=.8. These are the canonical example settings, not the held-out generator settings. The jittered call explicitly uses SD=0.020 s.','',
'The timing null replaces only the coupled burst component with bursts from a homogeneous Poisson process of rate 8/s on (0.5,19.5) s; separate seed 20261022 produced 174 events. The low rhythm, baseline HF and noise samples remain identical to the paired coupled example. Overlapping bursts are allowed. The old canonical null used a fixed event count and uniform times; that old null was not relabeled as Poisson. The workflow and condition panels use regenerated frozen-v1 outputs throughout.','',
table(canon,['state','fP_hz','fA_hz','raw_mvl','ozkurt_mvl','preferred_phase_deg']),
'Generator settings, seeds and source hash: '+link(OUT/'canonical_provenance.json')+'. Outputs: '+link(OUT/'canonical_results.csv')+'.','',
'## Figures','',
'All figures are exported as PNG at 300 dpi and SVG. The embedded Description metadata includes the method commit, source CSV paths and SHA-256 hashes, full analysis settings and seeds. Each figure lists its source CSV filenames visibly. Wilson intervals use z=1.9599639845 and n=25; invalid held-out estimates count as recovery failures. AUCs are taken unchanged from the saved coupled-versus-timing-null score table.','']
for f in FIGURES:lines+=['- **'+f['name']+'**: '+f['title']+'. '+link(f['png'],'PNG')+'; '+link(f['svg'],'SVG')+'. Sources: '+', '.join(link(p) for p in f['sources'])+'.']
lines+=['','Source manifest: '+link(OUT/'figure_manifest.json')+'. Held-out source evaluation commit is `'+V2+'`; the v1 path was previously checked against v1.0. No held-out simulation was regenerated for Figures 3–5 or the v2 negative-result supplement. Development results remain explicitly labeled development.','',
'## Runtime, deviations and verification','',
'MATLAB analysis elapsed seconds: '+str(json.loads((OUT/'analysis_runtime.json').read_text(encoding='utf-8'))['elapsed_seconds'])+'. Python figure/statistics build seconds are recorded in '+link(OUT/'build_runtime.json')+'. Startup and exploratory inspection time are excluded.','',
'Tooling deviations: (1) metadata inspection initially assumed the multichannel crop retained absolute timestamps; it restarts at zero. Exact alignment was established with the original indices 40800:372501, with no change to the analyzed signal or bout definitions. (2) first MATLAB launch failed its pre-analysis source-path assertion because the workspace current directory shadowed the frozen file; the runner changed its working directory to revision_checks/final and then verified the frozen path. The failed launch did not analyze any bout. (3) pre-existing MATLAB startup warnings reference a missing Brainstorm install; no Brainstorm installation was altered. Additional tooling deviations, if any, are recorded in '+link(OUT/'deviations.json')+'.','',
'Limitations of available evidence: shank, XML acquisition index and layer remain undocumented; optional other-session bout eligibility was not established. There was no method change, parameter tuning or new candidate. Full metadata: '+link(OUT/'analysis_provenance.json')+'. Final integrity checks and hashes: '+link(OUT/'verification.json')+' and '+link(OUT/'output_manifest.json')+'.','']
(OUT/'RESULTS_final.md').write_text('\n'.join(lines),encoding='utf-8')
(OUT/'build_runtime.json').write_text(json.dumps({'elapsed_seconds':time.perf_counter()-START,'metadata':META},indent=2),encoding='utf-8')
print(json.dumps({'figures':len(FIGURES),'rodent_rows':len(rod),'statistics_rows':len(STAT),'status':'COMPLETE'}))
