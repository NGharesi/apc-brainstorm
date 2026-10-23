"""Report a conclusive failure bound; never label partial coverage as complete."""
from pathlib import Path
import sys,json,hashlib,os,datetime,subprocess
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=ROOT/'revision_checks/rodent_multi'
sys.path.insert(0,str(ROOT/'pydeps'));os.environ['MPLCONFIGDIR']=str(OUT/'plot_config')
import numpy as np
import pandas as pd
from scipy.io import loadmat,savemat
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def link(name,label=None):return f'[{label or name}](<{(OUT/name).as_posix()}>)'
def write_csv(rows,name):
 d=pd.DataFrame(rows);d['git_commit']=meta['git_commit'];d['provenance_json']=json.dumps(meta,separators=(',',':'))
 d.to_csv(OUT/name,index=False,encoding='utf-8');return d
def bouts(mask,t,index_offset):
 d=np.diff(np.r_[False,mask,False].astype(int));a=np.flatnonzero(d==1);b=np.flatnonzero(d==-1)-1
 duration=t[b]-t[a]+np.median(np.diff(t));keep=duration>=5
 return [dict(start_idx=int(i+index_offset),stop_idx=int(j+index_offset),start_time_s=t[i],stop_time_s=t[j],duration_s=du)
         for i,j,du in zip(a[keep],b[keep],duration[keep])]

bound=read(OUT/'partial_validation_bounds.json');assert bound['full_interval_agreement_upper_bound_percent']<95
checkpoint=OUT/'ec013.157_speed_chunk_01.mat';q=loadmat(checkpoint,simplify_cells=True)
old=loadmat(OUT/'behavior_reproduction.mat',simplify_cells=True)
record=loadmat(Path(r'D:\APC_project\RealDatasets\LFP_data\EC3_dataset_real.mat'),variable_names=['R2'],simplify_cells=True)['R2']
time=np.asarray(record['Time']);del record
meta=read(OUT/'protocol_amendments_record.json')|dict(stage='conclusive reference-label failure from saved first chunk',matlab_version=q['provenance']['matlab_version'],seed=0,
    source_checkpoint=checkpoint.name,source_checkpoint_sha256=sha(checkpoint),
    historical_source='behavior_reproduction.mat',historical_source_sha256=sha(OUT/'behavior_reproduction.mat'),
    full_validation_complete=False,acceptance_threshold_percent=95,
    settings=dict(chunk_samples=331702,overlap_seconds=20,internal_trim_seconds=10,record_edge_trim_seconds=2,tracking_fs_hz=39.06,speed_threshold=6,minimum_bout_seconds=5,short_gap_limit_seconds=.5))
start=int(q['chunkStart']);end=int(q['chunkEnd']);owned_end=end-12500
idx=np.arange(40800,owned_end+1);speed=np.asarray(q['chunkSpeed']);known_speed=speed[idx-start]
position=np.asarray(q['position']);valid_position=np.isfinite(position[:-1])&np.isfinite(position[1:])
valid=valid_position[idx-start]&np.isfinite(known_speed);assert valid.all(), 'Known reference labels unexpectedly invalid'
historical_run=np.abs(np.asarray(old['speed']))>6
new_run=np.abs(known_speed)>6;same=new_run==historical_run[:len(idx)]
assert len(idx)==bound['historical_known_samples'] and int(same.sum())==bound['known_agreeing_samples']
assert bound['known_disagreeing_samples']>0.05*bound['historical_total_samples']

# Exact per-bout endpoint comparisons only where both endpoints plus tolerance
# are covered. Later endpoints remain explicitly unresolved after the stop.
prefix_indices=np.arange(start,owned_end+1);prefix_speed=speed[:len(prefix_indices)]
prefix_valid=valid_position[:len(prefix_indices)]&np.isfinite(prefix_speed)
prefix_time=time[prefix_indices-1];historical_time=time[40799:372500]
matched_rows=[];resolved_counts={};prefix_rows=[]
for state in ['run','rest']:
 hmask=historical_run if state=='run' else ~historical_run
 nmask=prefix_valid&(np.abs(prefix_speed)>6 if state=='run' else np.abs(prefix_speed)<=6)
 historical_bouts=bouts(hmask,historical_time,40800);assert len(historical_bouts)==12
 current=bouts(nmask,prefix_time,start)
 for i,b in enumerate(current):prefix_rows.append(dict(state=state,bout=i+1,right_censored=b['stop_idx']==owned_end,**b))
 matched=0;resolved=0
 for i,h in enumerate(historical_bouts):
  covered=h['start_time_s']-.5>=prefix_time[0] and h['stop_time_s']+.5<=prefix_time[-1]
  candidates=[c for c in current if max(abs(c['start_time_s']-h['start_time_s']),abs(c['stop_time_s']-h['stop_time_s']))<=.5]
  yes=bool(candidates) if covered else None
  if covered:resolved+=1;matched+=int(yes)
  c=candidates[0] if covered and candidates else {}
  matched_rows.append(dict(state=state,historical_bout=i+1,**{'historical_'+k:v for k,v in h.items()},
      both_endpoints_fully_covered=covered,matched_within_0_5_s=yes,new_start_time_s=c.get('start_time_s',np.nan),new_stop_time_s=c.get('stop_time_s',np.nan)))
 resolved_counts[state]=dict(resolved_historical_bouts=resolved,matched_among_resolved=matched,unresolved_historical_bouts=12-resolved,
                            full_12_bout_match_count_lower_bound=matched,full_12_bout_match_count_upper_bound=matched+12-resolved)
write_csv(matched_rows,'ec013_157_bout_validation.csv');write_csv(prefix_rows,'ec013_157_known_prefix_bouts.csv')
write_csv([dict(session='ec013.157',chunk=1,start_idx=start,stop_idx=end,samples=end-start+1,owned_start=start,owned_stop=owned_end,
                elapsed_seconds=float(q['elapsed']),route=q['route'])],'ec013_157_chunk_inventory.csv')

disagreement=np.flatnonzero(~same);d=np.diff(np.r_[False,~same,False].astype(int));a=np.flatnonzero(d==1);b=np.flatnonzero(d==-1)-1
write_csv([dict(start_idx=int(idx[i]),stop_idx=int(idx[j]),start_time_s=time[idx[i]-1],stop_time_s=time[idx[j]-1],samples=int(j-i+1)) for i,j in zip(a,b)],'ec013_157_label_disagreements.csv')
savemat(OUT/'ec013_157_partial_label_comparison.mat',dict(global_indices=idx,historical_run=historical_run[:len(idx)],chunked_run=new_run,valid=valid,
                                                       same=same,provenance_json=json.dumps(meta)),do_compression=True)

missing=pd.read_csv(OUT/'tracking_missing_counts.csv',encoding='utf-8');missing=missing[missing.array=='ec013ec2'].iloc[0]
resources=pd.read_csv(OUT/'validation_resource_monitor.csv',encoding='utf-8')
gate=bound|dict(status='FAILED_STOP_CONCLUSIVE_UPPER_BOUND',passed=False,full_interval_agreement_percent=None,
               reference_known_global_indices=[int(idx[0]),int(idx[-1])],uncomputed_reference_samples=331701-len(idx),
               all_known_reference_labels_valid=True,endpoint_comparisons=resolved_counts,completed_chunk_seconds=float(q['elapsed']),
               peak_observed_private_bytes=int(resources.private_bytes.max()),peak_observed_working_set_bytes=int(resources.working_set_bytes.max()),
               incomplete_chunk='chunk 2 stopped after proof of gate failure; no checkpoint',
               stop_action='Only verified validation worker PID 46812 was terminated; launcher returned exit 1; user MATLAB PID 23860 untouched',
               raw_x1_missing_fraction=float(missing.x1_missing_fraction),provenance=meta)
(OUT/'chunked_behavior_validation.json').write_text(json.dumps(gate,indent=2),encoding='utf-8')

plt.rcParams.update({'font.size':10,'svg.fonttype':'none'})
fig,axes=plt.subplots(2,1,figsize=(13,5.3),sharex=True)
ref_time=time[40799:372500]
axes[0].plot(ref_time,historical_run.astype(float),lw=.65,label='Historical')
axes[0].plot(time[idx-1],new_run.astype(float)+.06,lw=.65,alpha=.8,label='Chunked (computed prefix)')
axes[0].set(yticks=[0,1],yticklabels=['Rest','Run'],ylim=(-.15,1.4));axes[0].legend(ncol=2,loc='upper left',frameon=False)
axes[1].fill_between(time[idx-1],0,(~same).astype(float),color='#D55E00',lw=0,label='Disagreement')
for ax in axes:ax.axvspan(time[owned_end],ref_time[-1],color='#BBBBBB',alpha=.5,label='Uncomputed after stop' if ax is axes[1] else None)
axes[1].set(ylabel='Disagreement',xlabel='Recording time (s)',ylim=(-.05,1.3));axes[1].legend(ncol=2,loc='upper left',frameon=False)
fig.suptitle(f"ec013.157 gate FAIL: full-interval agreement cannot exceed {gate['full_interval_agreement_upper_bound_percent']:.4f}% (required 95%)")
fig.tight_layout(rect=(0,.1,1,.95));fig.text(.5,.018,'APC v1.0 '+meta['git_commit']+'\nSources: ec013_157_label_disagreements.csv; ec013_157_partial_label_comparison.mat | First chunk only; shaded region not computed',ha='center',fontsize=8)
figuremeta=meta|{'source_csv':'ec013_157_label_disagreements.csv','source_csv_sha256':sha(OUT/'ec013_157_label_disagreements.csv')}
fig.savefig(OUT/'ec013_157_label_validation.png',dpi=300,metadata={'Description':json.dumps(figuremeta)})
fig.savefig(OUT/'ec013_157_label_validation.svg',metadata={'Description':json.dumps(figuremeta)});plt.close(fig)

archive=OUT/'RESULTS_preflight.md';text=archive.read_text(encoding='utf-8')
text=text.replace('# Multi-session rodent analysis — preflight results','# Multi-session rodent analysis — stopped at behaviour gate')
first=text.index('**Status:');last=text.index('\n\n',first)
text=text[:first]+f"**Status: STOPPED. The specified >=95% ec013.157 label-agreement gate cannot pass: its maximum possible full-interval agreement is {gate['full_interval_agreement_upper_bound_percent']:.6f}%.** This is a conclusive failure bound from partial coverage, not a completed full-interval percentage. No new APC/comparator estimates or other sessions' bout analyses were run."+text[last:]
first=text.index('## Inclusion, statistics and remaining interval choice');last=text.index('## Figures',first)
endpoint_text='\n'.join(f"| {s} | {r['resolved_historical_bouts']}/12 | {r['matched_among_resolved']} | {r['unresolved_historical_bouts']} | {r['full_12_bout_match_count_lower_bound']}–{r['full_12_bout_match_count_upper_bound']} /12 |" for s,r in resolved_counts.items())
section=f'''## Whole-recording amendments and conclusive validation failure

Both user amendments were added before the chunked analysis: whole recordings, missing -1 positions, bounded <=0.5-s interpolation, long-gap bout splitting, 2-s recording edge exclusion, exactly 331,702-sample chunks, 20-s overlap, 10-s internal edge rejection, final chunk ending at the trimmed recording end, and the >=95% label-agreement gate. Evidence: {link('protocol_amendments_record.json')}. The unchanged original plan is retained in {link('PROTOCOL_rodent_original.md')} (SHA-256 `{meta['original_protocol_sha256']}`). Amended protocol SHA-256: `{meta['protocol_sha256']}`.

Chunk 1 completed using trenddecomp with no fallback. Its owned speed samples cover global indices {start}:{owned_end}. Inside the historical comparison interval, **all {len(idx):,} computed samples have valid new labels**; missing/unlabelled samples do not account for their disagreements. Speed units and threshold remain the original raw x1 units/s and abs(speed)>6.

| Label comparison measure | Result |
| --- | --- |
| Full historical derivative interval | 40800:372500; 331,701 samples |
| Computed historical prefix | 40800:{owned_end}; {len(idx):,} samples |
| Prefix agreeing / disagreeing samples | {int(same.sum()):,} / {int((~same).sum()):,} |
| Prefix agreement | {gate['known_agreement_percent']:.6f}% |
| Uncomputed reference samples | {gate['uncomputed_reference_samples']:,} |
| Full-interval agreement lower / upper bounds | {gate['full_interval_agreement_lower_bound_percent']:.6f}% / {gate['full_interval_agreement_upper_bound_percent']:.6f}% |
| Required agreement | >=95% |
| Full-interval exact agreement | Not computed after conclusive failure |

Proof: the {gate['known_disagreeing_samples']:,} known disagreements already occupy {100*gate['known_disagreeing_samples']/331701:.6f}% of the full reference interval. Assigning agreement to every remaining sample yields at most {gate['full_interval_agreement_upper_bound_percent']:.6f}%, below 95%. The second chunk was stopped immediately after this proof; the third was not run. This preserves the specified acceptance criterion. The computation was terminated early rather than estimating a percentage from incomplete data.

Per-bout endpoint checks are reported only when both endpoints plus the 0.5-s tolerance are covered. Full 12-bout recovery counts remain unresolved where endpoints are uncomputed:

| State | Historical bouts fully covered | Matched among covered | Unresolved | Full 12-bout matched-count bounds |
| --- | --- | --- | --- | --- |
{endpoint_text}

Exact rows: {link('ec013_157_bout_validation.csv')}; known-prefix bouts with right-censor flags: {link('ec013_157_known_prefix_bouts.csv')}. Contiguous disagreements: {link('ec013_157_label_disagreements.csv')}. All computed labels: {link('ec013_157_partial_label_comparison.mat')}. Saved speed and position: {link('ec013.157_speed_chunk_01.mat')}. Validation facts and provenance: {link('chunked_behavior_validation.json')}.

Historical handling retains -1 and still reproduces **12 run /12 rest exactly**, unchanged. For the whole ec013.157 tracking array, {int(missing.missing_x1):,}/{int(missing.samples):,} x1 samples are missing ({100*missing.x1_missing_fraction:.6f}%). Full-recording numbers of bouts lost to gaps were not computed after the gate failure.

## Inclusion and analyses not run

All 18 mapping checks and channel selections remain complete. No session has been assigned final >=5/5 bout eligibility after this failed prerequisite. The other 17 sessions' chunked behaviour, original-interval PAC sensitivity, E1 sensitivity, per-bout APC/A2' scans, per-session and across-session statistics, mixed models, within-state spreads, and run/rest effect figures were not run. Prepared runner scripts were not executed beyond the reference validation. No method, threshold, chunk length or missing-data rule was changed after observing this failure.

'''
text=text[:first]+section+text[last:]
text=text.replace('Run/rest and session-difference figures await bout analysis.',
 'Reference-label failure diagnostic: '+link('ec013_157_label_validation.png','300-dpi PNG')+'; '+link('ec013_157_label_validation.svg','SVG')+'. Commit and source CSV are embedded. Grey shading denotes uncomputed labels. The earlier channel-selection figure preserves its pre-amendment provenance and preflight-status footer; no run/rest effect figures were generated.')
text=text.replace('Deviations and pending choice:','Deviations:')
text+=f"\nCompleted chunk runtime: {float(q['elapsed']):.3f} s (29.477 min), excluding MATLAB startup and the interrupted second chunk. Peak observed MATLAB private allocation: {gate['peak_observed_private_bytes']/1e9:.3f} GB; peak sampled resident working set: {gate['peak_observed_working_set_bytes']/1e9:.3f} GB. The 32-GB host paged heavily. Resource observations: {link('validation_resource_monitor.csv')}; console log: {link('chunked_validation_matlab.log')}. Exit 1 reflects intentional termination after the conclusive gate failure, not an additional method exception.\n"
(OUT/'RESULTS_rodent.md').write_text(text,encoding='utf-8')

deviations=read(OUT/'deviations.json');deviations['metadata']=meta
deviations['deviations']=[d for d in deviations['deviations'] if d['type']!='pending execution choice']
deviations['deviations'] += [
 dict(type='user-authorized amendments',detail='Whole-recording interval, missing tracking, fixed-length chunks and >=95% gate were recorded before reference validation.'),
 dict(type='early computational termination',detail=f"First chunk proves full-interval agreement <= {gate['full_interval_agreement_upper_bound_percent']:.9f}% <95%; stopped second chunk and did not run third. Exact full percentage, unresolved endpoint matches and full gap-loss counts are not reported as known."),
 dict(type='resource limitation',detail=f"Fixed-length trenddecomp chunk still reached observed private allocation {gate['peak_observed_private_bytes']/1e9:.3f} GB on 32-GB host, with paging; no decomposition substitute used."),
 dict(type='read-only tooling path correction',detail='Initial SVD-source inspection tried matlab/matfun/svdsketch.m; located the installed file under matlab/sparfun/svdsketch.m. No analysis or settings changed.')]
(OUT/'deviations.json').write_text(json.dumps(deviations,indent=2),encoding='utf-8')
status=dict(status='STOPPED_CONCLUSIVE_CHUNK_LABEL_GATE_FAILURE',metadata=meta,validation=gate,
            historical_12_12_exact_reproduction_passed=True,mapping_pairs_passed=18,sessions_channel_selected=18,
            completed_reference_chunks=1,active_validation_process=False,new_session_bout_analyses_started=False,new_PAC_estimates_computed=False)
(OUT/'STATUS.json').write_text(json.dumps(status,indent=2),encoding='utf-8')
(OUT/'RESUME_STATUS.json').write_text(json.dumps(status|{'next':'STOP per user failure rule. Do not resume new-session analysis without further user instructions.'},indent=2),encoding='utf-8')
for name in ['session_preflight_status.csv']:
 p=OUT/name;frame=pd.read_csv(p,encoding='utf-8');frame['inclusion_status']='not assessed: prerequisite chunk-label gate failed';frame['current_status_provenance_json']=json.dumps(meta);frame.to_csv(p,index=False,encoding='utf-8')
files=[]
for p in OUT.rglob('*'):
 if p.is_file() and p.name!='output_manifest.json' and not any(x in ['__pycache__','plot_config'] for x in p.relative_to(OUT).parts):files.append(dict(path=str(p.relative_to(OUT)),bytes=p.stat().st_size,sha256=sha(p)))
(OUT/'output_manifest.json').write_text(json.dumps(dict(metadata=meta,files=files),indent=2),encoding='utf-8')
print(json.dumps({'status':status['status'],'full_agreement_upper_bound_percent':gate['full_interval_agreement_upper_bound_percent'],'endpoint_comparisons':resolved_counts,'report':str(OUT/'RESULTS_rodent.md')}))
