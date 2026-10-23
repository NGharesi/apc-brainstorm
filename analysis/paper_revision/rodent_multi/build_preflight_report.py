from pathlib import Path
import sys,os,json,csv,hashlib,subprocess,datetime
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=ROOT/'revision_checks/rodent_multi';sys.path.insert(0,str(ROOT/'pydeps'));os.environ['MPLCONFIGDIR']=str(OUT/'plot_config')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.io import loadmat
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def link(p,label=None):return f'[{label or Path(p).name}](<{Path(p).resolve().as_posix()}>)'
def table(d,cols):
 def fmt(x):return 'NA' if isinstance(x,(float,np.floating)) and not np.isfinite(x) else f'{x:.8g}' if isinstance(x,(float,np.floating)) else str(x)
 return '| '+' | '.join(cols)+' |\n| '+' | '.join('---' for _ in cols)+' |\n'+'\n'.join('| '+' | '.join(fmt(r[c]) for c in cols)+' |' for _,r in d.iterrows())+'\n'
runtime=load(OUT/'channel_selection_runtime.json');assert runtime['status']=='COMPLETE'
meta=runtime['metadata'];meta['analysis_status']='PREFLIGHT_COMPLETE_INTERVAL_DECISION_PENDING';meta['sources']={str(p):sha(p) for p in [OUT/'PROTOCOL_rodent.md',OUT/'EXECUTION_rodent.md',OUT/'mapping_checks.csv',OUT/'selected_channels.csv',OUT/'channel_ratios.csv']}
mapping=pd.read_csv(OUT/'mapping_checks.csv');selected=pd.read_csv(OUT/'selected_channels.csv');ratios=pd.read_csv(OUT/'channel_ratios.csv');gate=load(OUT/'behavior_reproduction.json')
assert len(mapping)==len(selected)==18 and gate['passed'];assert np.all(abs(mapping.tracking_to_lfp_duration_ratio-1)<=.05)
tracking_rows=[]
for animal in ['EC013','EC012']:
 path=Path(r'D:\APC_project\RealDatasets\LFP_data\Behavioral_Data')/(animal+'_movement.mat');s=loadmat(path,simplify_cells=True)
 for i in range(1,10):
  name=animal.lower()+'ec'+str(i);a=s[name];tracking_rows.append({'animal':animal,'array':name,'samples':len(a),'missing_x1':int((a[:,0]==-1).sum()),'missing_any_LED_coordinate':int((a==-1).any(1).sum()),'x1_missing_fraction':float((a[:,0]==-1).mean()),'provenance_json':json.dumps(meta,separators=(',',':'))})
pd.DataFrame(tracking_rows).to_csv(OUT/'tracking_missing_counts.csv',index=False,encoding='utf-8')
memory=mapping[['animal','session','lfp_samples']].copy();memory['SSA_lag_samples']=np.minimum(memory.lfp_samples//2,5000);memory['dense_Hankel_GB']=8*memory.SSA_lag_samples*(memory.lfp_samples-memory.SSA_lag_samples+1)/1e9;memory['provenance_json']=json.dumps(meta,separators=(',',':'));memory.to_csv(OUT/'behavior_memory_estimates.csv',index=False,encoding='utf-8')
selection=selected.merge(mapping[['session','lfp_duration_s','tracking_to_lfp_duration_ratio']],on='session');selection['inclusion_status']='pending bout interval and >=5/5 bout gate';selection.to_csv(OUT/'session_preflight_status.csv',index=False,encoding='utf-8')
plt.rcParams.update({'font.size':9,'font.family':'DejaVu Sans','svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(2,1,figsize=(15,9),sharex=True);x=np.arange(18)
for j,r in selected.iterrows():
 d=ratios[(ratios.session==r.session)&np.isfinite(ratios.theta_delta_ratio)&(ratios.theta_delta_ratio>0)];axes[0].scatter(np.full(len(d),j),d.theta_delta_ratio,color='#BBBBBB',s=11,alpha=.6)
axes[0].scatter(x,selected.theta_delta_ratio,c='#111111',marker='*',s=80,label='Selected maximum',zorder=3)
e1=ratios[(ratios.animal=='EC013')&(ratios.channel_index==1)];pos={s:i for i,s in enumerate(selected.session)};axes[0].scatter([pos[s] for s in e1.session],e1.theta_delta_ratio,facecolors='none',edgecolors='#D55E00',s=45,label='E1 sensitivity',zorder=4)
axes[0].set(yscale='log',ylabel='Theta (6–10) / delta (1–4) power',title='Whole-recording channel ranking (both states pooled)');axes[0].grid(axis='y',alpha=.15)
colors=['#0072B2' if a=='EC013' else '#D55E00' for a in selected.animal];axes[1].bar(x,selected.channel_index,color=colors,width=.65)
for j,r in selected.iterrows():axes[1].text(j,r.channel_index+.8,r.channel_name,ha='center',fontsize=8)
axes[1].axvline(8.5,color='#777777',ls=':',lw=1);axes[0].axvline(8.5,color='#777777',ls=':',lw=1);axes[1].set(ylabel='Selected channel (one-based)',ylim=(0,70),xticks=x,xticklabels=selected.session)
plt.setp(axes[1].get_xticklabels(),rotation=55,ha='right');fig.suptitle('Prespecified theta/delta channel selection',fontsize=16,fontweight='bold');fig.subplots_adjust(top=.84,bottom=.2,hspace=.26)
handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.94),ncol=2,frameon=False)
fig.text(.5,.025,'APC v1.0 '+meta['git_commit']+'\nSources: channel_ratios.csv, selected_channels.csv | Bout analysis pending interval decision',ha='center',fontsize=8)
prov=json.dumps(meta,separators=(',',':'));fig.savefig(OUT/'channel_selection_summary.png',dpi=300,metadata={'Description':prov});fig.savefig(OUT/'channel_selection_summary.svg',metadata={'Description':prov});plt.close(fig)
deviations=[{'type':'source path recovery','detail':'Requested ec013.157 data_block001.mat is absent. Local behavior_inter.mat/test supplies the exact full recording; full E1/Time and the entire 65-channel saved crop matched exactly. No input changed.'}, {'type':'historical behavior limitation','detail':'Literal producer uses interpolated x1 only, no -1 sentinel handling, trenddecomp and threshold 6; no documented unit calibration. Exact historical gate passed.'}, {'type':'pending execution choice','detail':'Original interval versus whole-recording bout analysis was not specified explicitly. Unchanged trenddecomp uses lag min(floor(N/2),5000), creating up to about 88 GB dense Hankel data on a 32-GB machine. New bout analyses remain pending the interval answer.'}, {'type':'startup tooling','detail':'MATLAB reports pre-existing missing Brainstorm startup directories. No installation or tagged code changed.'}]
(OUT/'deviations.json').write_text(json.dumps({'metadata':meta,'deviations':deviations},indent=2),encoding='utf-8')
lines=['# Multi-session rodent analysis — preflight results','',
'**Status: channel selection and prerequisite checks complete; new bout analyses pending the time-interval decision.** No new-session APC/comparator outcomes, per-session eligibility decisions, inferential tests or mixed models have been computed. This is a preflight report, not completed replication results.','',
'The user plan was saved verbatim before any new-session analysis: '+link(OUT/'PROTOCOL_rodent.md')+'. Execution choices fixed before channel selection: '+link(OUT/'EXECUTION_rodent.md')+'. Frozen APC tag `v1.0`, commit `'+meta['git_commit']+'`; no tagged code changed.','',
'## Session-to-tracking mapping','',
'Ratio = (tracking samples / 39.0625) / (LFP samples / measured fs). All 18 pairs pass the 5% gate. The original ec013.157 path is missing, but a verified equivalent full multichannel source was recovered locally. Mapping CSV: '+link(OUT/'mapping_checks.csv')+'. Original missing-path inventory is retained separately.','',
table(mapping,['animal','session','tracking_array','tracking_samples','lfp_samples','lfp_channels','lfp_fs_hz','lfp_duration_s','tracking_to_lfp_duration_ratio','status']),
'Reference source recovery: '+link(OUT/'ec013_157_source_recovery.json')+'. The test variable in `D:/APC_project/2025/Results_Behavior/behavior_inter.mat` has 65×789000 samples; its entire E1/Time match R2 exactly and all 65 channels at samples 40800:372501 match the existing multichannel crop exactly.','',
'## Exact historical behaviour reproduction','',
'Original script found: `D:/APC_project/2025/Results_Behavior/behavior.m`. The 5-s bout producer is '+link(ROOT/'run_apc_ec013_run_rest.m')+'. The reproduction uses ec013ec2, LED timestamps at 39.06 Hz, original R2 indices 40800:372501, trenddecomp of interpolated x1, derivative divided by elapsed seconds, abs(speed)>6, contiguous bouts ≥5 s.','',
'**PASS: 12 run and 12 rest bouts.** Both bout tables (indices, timestamps, durations), both masks and the entire speed vector match exactly. Maximum speed and trend differences = 0. Smoothing route: trenddecomp. Evidence: '+link(OUT/'behavior_reproduction.json')+'; '+link(OUT/'behavior_reproduction.mat')+'.','',
'Computational speed units are raw x1 tracking-coordinate units per second. The original plot labels position as cm, but neither script applies a coordinate calibration. Physical cm/s is therefore not independently verified. The producer does not remove −1 sentinels, average LEDs or compute 2-D displacement. Literal reproduction retains these behaviours. Missing-coordinate counts: '+link(OUT/'tracking_missing_counts.csv')+'.','',
'## Prespecified whole-recording channel selection','',
'All imported channels are ranked on the entire recording, with no state or PAC-outcome selection. Per-channel mean removal; Welch with symmetric Hann round(4*fs), 50% overlap, NFFT next power of two; integrate one-sided PSD at exact band endpoints by interpolation/trapezoids. First index breaks ties. Undefined ratios are recorded. Every channel, power and source flag: '+link(OUT/'channel_ratios.csv')+'. Choices: '+link(OUT/'selected_channels.csv')+'.','',
table(selected,['animal','session','channel_index','channel_name','theta_delta_ratio','region','shank']),
'## Channel metadata evidence','',
'No hc-3 channel/shank/region metadata table or session XML was found under `D:/APC_project/RealDatasets`; the file inventory includes unrelated OpenNeuro metadata. Regions and shanks remain **unverified** in the primary channel table.','',
'Additional files found outside that root: `D:/APC_project/Previous_Computer/RealData/tPACPaper/ElePosition.txt`, `hc3-session.csv`, and `ec012ec.14/ec012ec.269/ec012ec.269.xml`. The XML defines anatomical channel groups but does not give region names; the text table contains session-group region entries. A validated channel-to-shank-to-region join has not been established here, so no anatomical label was inferred from channel index alone.','',
'## Inclusion, statistics and remaining interval choice','',
'All sessions are pending the prespecified ≥5 run/≥5 rest bout gate; none is excluded based on a PAC result. Whole-recording channel selection is complete for both animals. EC013 E1 is prespecified as the sensitivity channel.','',
'The historical bout producer analyzes indices 40800:372501 (about 32.64–298 s). The user was asked whether multi-session bouts should use that interval or whole recordings. The unchanged trenddecomp code defaults to a 5000-sample SSA lag and explicitly builds a dense Hankel matrix. Full-recording estimates: '+link(OUT/'behavior_memory_estimates.csv')+'. The largest dense matrix alone is '+f'{memory.dense_Hankel_GB.max():.3f}'+' GB; the host has about 32 GB RAM. No decomposition shortcut, fallback substitution or crop has been applied to new-session bout analysis.','',
'After the interval choice: apply the historical speed computation, count/include bouts, run frozen APC and guarded SOS scans, produce per-session bootstrap/Welch/Hedges results, across-session t/Wilcoxon tests, the specified random-intercept/random-slope models, and within-state spreads. The plotted scan choice is fixed as the Ozkurt-max scan independently of run/rest effects.','',
'## Figures','',
'- Channel-selection summary: '+link(OUT/'channel_selection_summary.png','300-dpi PNG')+'; '+link(OUT/'channel_selection_summary.svg','SVG')+'. Commit, protocol and source CSV hashes embedded.','',
'Run/rest and session-difference figures await bout analysis.','',
'## Runtime and deviations','',
f'Historical reproduction MATLAB time: {gate["elapsed_seconds"]:.3f} s. Channel selection MATLAB time: {runtime["elapsed_seconds"]:.3f} s. Read-only inventory: '+str(load(OUT/'inventory.json')['elapsed_seconds'])+' s. Startup and packaging time excluded.','',
'Deviations and pending choice: '+link(OUT/'deviations.json')+'. Full inventory: '+link(OUT/'inventory.json')+'. Current status: '+link(OUT/'STATUS.json')+'. Output manifest: '+link(OUT/'output_manifest.json')+'.','']
(OUT/'RESULTS_rodent.md').write_text('\n'.join(lines),encoding='utf-8')
(OUT/'STATUS.json').write_text(json.dumps({'status':'AWAITING_BOUT_INTERVAL_DECISION','metadata':meta,'mapping_pairs_passed':18,'historical_12_12_reproduction_passed':True,'sessions_channel_selected':18,'new_session_bout_analyses_started':False},indent=2),encoding='utf-8')
files=[]
for p in OUT.rglob('*'):
 if p.is_file() and p.name!='output_manifest.json' and not any(x in ['__pycache__','plot_config'] for x in p.relative_to(OUT).parts):files.append({'path':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':sha(p)})
(OUT/'output_manifest.json').write_text(json.dumps({'metadata':meta,'files':files},indent=2),encoding='utf-8')
print(json.dumps({'status':'AWAITING_BOUT_INTERVAL_DECISION','sessions':18,'report':str(OUT/'RESULTS_rodent.md')}))
