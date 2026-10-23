"""Collect/report the stopped partial run. Never recompute dataset methods."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,hashlib,shutil
O=Path(__file__).resolve().parent;R=O.parent.parent;sys.path.insert(0,str(R/'pydeps'))
import pandas as pd
import numpy as np
def js(n):return json.loads((O/n).read_text(encoding='utf-8'))
def read(n):return pd.read_csv(O/n,encoding='utf-8')
def link(p,label=None):
    p=Path(p);p=p if p.is_absolute() else O/p
    return f'[{label or p.name}](<{p.as_posix()}>)'
def table(d,cols):
    def value(x):
        if pd.isna(x):return 'NA'
        if isinstance(x,(float,np.floating)):return f'{x:.8g}'
        return str(x).replace('|','/')
    return '| '+' | '.join(cols)+' |\n| '+' | '.join('---' for _ in cols)+' |\n'+'\n'.join('| '+' | '.join(value(r[c]) for c in cols)+' |' for _,r in d.iterrows())+'\n'
m=js('analysis_provenance.json');workers=[js(f'worker{k}_runtime.json') for k in [1,2,3]]
assert all(w['status']=='FAILED_STOP' and w['identifier']=='IEEG:OtherWorkerStopped' for w in workers)
d=read('ieeg_trial_estimates.csv');parts=pd.concat([read(f'ieeg_worker{k}_trial_estimates.csv') for k in [1,2,3]],ignore_index=True)
keys=['analysis','patient','session','trial','method'];assert not d.duplicated(keys).any() and len(d)==len(parts)
assert set(map(tuple,d[keys].to_numpy()))==set(map(tuple,parts[keys].to_numpy()))
u=d.drop_duplicates('checkpoint_file');assert len(u)==len(list((O/'estimates').glob('*.mat')))==sum(w['computed_inputs'] for w in workers)
apc=d[d.method=='APC-v1.0'];au=apc.drop_duplicates('checkpoint_file');assert len(au)==len(u) and (au.status!=0).mean()>.5
assert d[d.method!='APC-v1.0'].status.eq(0).all()
for p in u.checkpoint_file:assert Path(p).exists()
snapshot=js('method_failure_first_snapshot.json');original=O/'method_failure_first_snapshot_original.json'
if not original.exists():shutil.copyfile(O/'method_failure_first_snapshot.json',original)
snapshot.update(scope='Partial completed inputs from sub-01 and sub-02, across six sessions; three sessions complete and three partial at the first stop check.',scope_label_correction='The initial hardcoded scope label incorrectly said initial three sub-01 sessions. Counts are unchanged; the original JSON is preserved in method_failure_first_snapshot_original.json.')
(O/'method_failure_first_snapshot.json').write_text(json.dumps(snapshot,indent=2),encoding='utf-8')
rate_rows=[];boundary_rows=[]
for (analysis,method),g in d.groupby(['analysis','method'],sort=True):
    valid=g.status.eq(0)&np.isfinite(g.score)
    rate_rows.append(dict(analysis=analysis,method=method,n_patients=g.patient.nunique(),n_sessions=len(g[['patient','session']].drop_duplicates()),completed_trials=len(g),valid_trials=int(valid.sum()),status4_trials=int(g.status.eq(4).sum()),other_failures=int((~valid&g.status.ne(4)).sum()),failure_fraction=float((~valid).mean()),scope='PARTIAL RUN ONLY'))
    boundary_rows.append(dict(analysis=analysis,method=method,completed_trials=len(g),valid_trials=int(valid.sum()),fp_low=int(g.boundary_fp_low.sum()),fp_high=int(g.boundary_fp_high.sum()),fa_low=int(g.boundary_fa_low.sum()),fa_high=int(g.boundary_fa_high.sum()),fp_boundary_fraction_all=float((g.boundary_fp_low.astype(bool)|g.boundary_fp_high.astype(bool)).mean()),fp_boundary_valid=int((valid&(g.boundary_fp_low.astype(bool)|g.boundary_fp_high.astype(bool))).sum()),scope='PARTIAL RUN ONLY'))
def write(rows,name):
    z=pd.DataFrame(rows);z['git_head']=m['git_head'];z['protocol_sha256']=m['protocol_sha256'];z['provenance_json']=json.dumps(m,separators=(',',':'));z.to_csv(O/name,index=False,encoding='utf-8');return z
rates=write(rate_rows,'partial_failure_rates.csv');bounds=write(boundary_rows,'partial_boundary_rates.csv')
counts=apc.groupby(['analysis','patient','session','status']).size().reset_index(name='completed_trials');write(counts,'partial_status_counts.csv')
I=read('trial_inclusion.csv')
for c in ['included','retained','session_eligible','patient_eligible','dataset_artifact','amplitude_reject','difference_reject']:I[c]=I[c].astype(bool)
included=I[I.included].copy();included['signal_type']=included.analysis.map(lambda a:'reference' if a=='referential' else 'bipolar')
planned=included.drop_duplicates(['patient','session','trial','signal_type']).groupby(['patient','session']).size().rename('planned_unique_inputs').reset_index();actual=u.groupby(['patient','session']).size().rename('completed_unique_inputs').reset_index()
progress=planned.merge(actual,on=['patient','session'],how='left');progress['completed_unique_inputs']=progress.completed_unique_inputs.fillna(0).astype(int);progress['session_input_run_complete']=progress.completed_unique_inputs==progress.planned_unique_inputs;write(progress,'partial_session_progress.csv')
ex=[]
for analysis,g in I.groupby('analysis',sort=True):
    flag=g.dataset_artifact;amp=g.amplitude_reject&~flag;diff=g.difference_reject&~flag
    if analysis=='artifact_only':amp=amp&False;diff=diff&False
    ex.append(dict(analysis=analysis,total_trials=len(g),dataset_artifact=int(flag.sum()),amplitude_unflagged=int(amp.sum()),difference_unflagged=int(diff.sum()),both_robust_unflagged=int((amp&diff).sum()),robust_union_unflagged=int((amp|diff).sum()),retained_before_eligibility=int(g.retained.sum()),retained_lost_session_eligibility=int((g.retained&~g.session_eligible).sum()),retained_lost_patient_eligibility=int((g.retained&g.session_eligible&~g.patient_eligible).sum()),final_included=int(g.included.sum())))
exclusions=write(ex,'trial_exclusion_summary.csv')
status=dict(status='STOPPED_METHOD_RELEVANT',reason='Most completed unique trial-signal inputs are invalid for frozen APC v1.0 (status 4).',stopped_utc=datetime.now(timezone.utc).isoformat(),provenance=m,first_check_inputs=snapshot['completed_unique_inputs'],first_check_status_counts=snapshot['APC_status_counts'],completed_unique_inputs=len(u),final_unique_APC_status_counts={str(k):int(v) for k,v in au.status.value_counts().items()},final_unique_APC_failure_fraction=float((au.status!=0).mean()),partial_method_rows=len(d),partial_patients=d.patient.nunique(),partial_sessions=len(d[['patient','session']].drop_duplicates()),full_unique_inputs_planned=m['unique_inputs'],full_method_rows_planned=m['total_method_rows'],completed_sessions=int(progress.session_input_run_complete.sum()),partially_started_sessions=int(((progress.completed_unique_inputs>0)&~progress.session_input_run_complete).sum()),workers_stopped=3,dataset_method_reruns=0,endpoints_computed=False,nulls_computed=False,exploratory_models_computed=False,method_settings_changed=False,new_commit_created=False,active_compute_jobs=0)
(O/'STATUS.json').write_text(json.dumps(status,indent=2),encoding='utf-8');live=js('provenance.json');live.update(status=status['status'],stage='Prespecified method-failure stop; partial estimates preserved',stopped_utc=status['stopped_utc'],stop_record='STATUS.json');(O/'provenance.json').write_text(json.dumps(live,indent=2),encoding='utf-8')
stop=['# STOPPED: most completed inputs invalid for APC v1.0','',
      'The run stopped under protocol section 6.4 after Amendment 3. At the first stop check, 325/422 completed unique trial-signal inputs (77.0%) returned status 4. After already-running work finished, '+str(int((au.status==4).sum()))+'/'+str(len(au))+' ('+f'{100*(au.status!=0).mean():.1f}'+ '%) returned status 4; '+str(int(au.status.eq(0).sum()))+' returned status 0. These are partial-run rates.','',
      f'The partial run covers {d.patient.nunique()} patients and {len(d[["patient","session"]].drop_duplicates())} sessions; only {int(progress.session_input_run_complete.sum())} sessions completed all planned inputs. It contains {len(d)} method rows and {len(u)} unique input checkpoints. All four comparators returned valid status/finite scores on these completed inputs.','',
      'All three workers stopped. The incremental CSV and checkpoints are preserved. No dataset method was rerun and no method setting was changed. No null analysis, primary/secondary endpoint, sensitivity endpoint test, exploratory model or final endpoint figure was computed. No primary decision is stated from a partial run.','',
      'Status 4 has two return conditions in the unchanged source: empty detected troughs, or empty phase-locked average/TF output. The saved status does not distinguish those conditions; no diagnostic rerun was made.','',
      'Protocol commit `'+m['git_head']+'`; SHA-256 `'+m['protocol_sha256']+'`. Protocol, src and tagged method code remain untouched. No results were committed.','',
      'Full gate/contact/mask/partial-run report: '+link('RESULTS_ieeg.md')+'. First stop snapshot: '+link('method_failure_first_snapshot.json')+'. Final counts: '+link('STATUS.json')+'.']
(O/'STOPPED.md').write_text('\n'.join(stop)+'\n',encoding='utf-8')
contacts=read('contacts.csv');rank=read('candidate_rankings.csv');pe=read('patient_eligibility.csv');eq=read('equivalence_both_attempts.csv');ieeg=read('native_ieeg_rate_summary.csv');scalp=read('native_scalp_rate_summary.csv');timeline=js('timeline_gate_confirmation.json')
deviations=js('deviations.json')
if not any(x['type']=='post-stop filter-guard logging recovery' for x in deviations['deviations']):
    deviations['deviations'].append(dict(type='post-stop filter-guard logging recovery',reason='The worker registry export was after its normal completion path, so the shared stop prevented export. The 39 fixed comparator-band design checks are reconstructed after the stop using the unchanged final_sos_filter helper on zero input only. No dataset trial or PAC method is rerun; the CSV explicitly labels this recovery.'))
if not any(x['type']=='stop snapshot scope label correction' for x in deviations['deviations']):
    deviations['deviations'].append(dict(type='stop snapshot scope label correction',reason='The initial monitor JSON hardcoded a three-session scope, although its contemporaneous displayed counts covered six sessions from two patients. The scope label is corrected without changing failure counts, and the original JSON is preserved.'))
(O/'deviations.json').write_text(json.dumps(deviations,indent=2),encoding='utf-8')
source=R/'apc-brainstorm-publish/src/bst_apc.m'
lines=['# ds004752 human iEEG analysis: STOPPED under the method-failure rule','',
       '**No completed primary endpoint decision is available.** The frozen run stopped because most completed inputs returned APC status 4. The report below distinguishes completed preprocessing/selection from partial method outputs. '+link('STOPPED.md')+'.','',
       '## Prespecified method-failure stop','',
       f'At the first check, 325/422 unique completed trial-signal inputs were invalid for APC (77.0%). Final in-flight counts: {int(au.status.eq(4).sum())}/{len(au)} status 4 ({100*(au.status!=0).mean():.1f}%), {int(au.status.eq(0).sum())} status 0. A unique input is one clinical trial with one signal representation (bipolar or referential); shared primary/artifact-only estimates are counted once here.','',
       f'The stopped run contains {len(d)} method rows, {len(u)} input checkpoints, {d.patient.nunique()} patients and {len(d[["patient","session"]].drop_duplicates())} sessions. Only {int(progress.session_input_run_complete.sum())} sessions completed their planned unique inputs; {int(((progress.completed_unique_inputs>0)&~progress.session_input_run_complete).sum())} more were partial. Planned full-run counts were {m["unique_inputs"]} unique inputs and {m["total_method_rows"]} method rows. The rates below describe only the completed portion and are not whole-dataset estimates.','',
       'Partial failure table (all comparisons are incomplete):',table(rates,['analysis','method','n_patients','n_sessions','completed_trials','valid_trials','status4_trials','other_failures','failure_fraction']),
       'Status 4 is returned for empty trough detections or empty phase-locked average/TF output. Both conditions are in the unchanged '+link(str(source)+':214','APC source, empty troughs')+' and '+link(str(source)+':224','APC source, empty phase-locked arrays')+'. The status does not identify which branch each trial took. No extra method run or diagnostic adjustment was made.','',
       'All workers stopped on the shared flag. Completed results remain in '+link('ieeg_trial_estimates.csv')+' and the `estimates/` checkpoints. Per-session completion counts: '+link('partial_session_progress.csv')+'. No nulls, primary/secondary endpoint tests, sensitivity endpoint tests, exploratory load models or endpoint figure were run. No method setting changed in response to outcomes.','',
       '## Public protocol and provenance','',
       'HEAD `'+m['git_head']+'` on clean branch `neuroimage-submission`. Protocol SHA-256 `'+m['protocol_sha256']+'`. Amendments 1, 2 and 3 were each pushed before the dependent signal processing. The source/helper hashes were verified before freezing the method run. No protocol, src, tagged source or original helper was edited; no results were committed.','',
       'Immutable pre-outcome method/input record: '+link('analysis_provenance.json')+'. Current provenance and versions: '+link('provenance.json')+'. Frozen contacts, masks, settings and wrapper hashes are recorded there. The first attempt remains in '+link('attempt1_archive/RESULTS_ieeg.md')+' and '+link('STOPPED_attempt1_sampling_rate.md')+'.','',
       '## Gate results','',
       'Both source-equivalence gates passed with maximum absolute difference 3.694822225952521e-13 (tolerance 1e-10). The repository src copy was used. Both original run records are retained:',table(eq,['attempt','metric','expected','observed','absolute_difference','passed']),
       'All 68 iEEG files passed amended header/channel/JSON rate agreement, native rate restrictions, channel order/count, total samples, 8-s trial lengths, finite data, nonzero channel variance and microvolt range. All 3353 iEEG trials produced exactly 16000 samples at 2000 Hz. Native iEEG rates:',table(ieeg,['native_fs_hz','n_patients','n_sessions']),
       'All 68 scalp files passed the timing-input checks. All 3353 scalp trials produced exactly 1600 samples at 200 Hz under Amendment 2. Native scalp rates:',table(scalp,['native_fs_hz','n_patients','n_sessions','trials']),
       'Gate files: '+link('edf_reading_gate_attempt2.json')+', '+link('edf_file_checks_attempt2.csv')+', '+link('edf_channel_checks_attempt2.csv')+', '+link('resampling_trial_checks_attempt2.csv')+', '+link('timeline_file_checks.csv')+', '+link('timeline_resampling_trial_checks.csv')+'.','',
       '## Trial timeline: PASS','',
       'The grand average includes all 3353 trials from 15 patients/68 sessions, averaging available O1/O2/Oz per trial. Each trial was resampled separately to 200 Hz, its fixation mean was subtracted, and no additional signal filter was applied. Visual review confirmed evoked negative deflections after both expected onsets. Peak latencies are at 5-ms resolution:',table(pd.DataFrame(timeline['peaks']),['expected_onset_s','peak_time_s','latency_ms','peak_uv','absolute_peak_difference_uv']),
       'The 160-ms encoding and 200-ms probe peaks are within the required 50-250 ms interval. Paper timings support fixation 0-1 s, encoding 1-3 s, maintenance 3-6 s and probe from 6 s: [Boran et al., Figure 1a](https://www.nature.com/articles/s41597-020-0364-3.pdf); [Dimakopoulos et al., task methods](https://elifesciences.org/articles/78677).','',
       'Timeline plot: '+link('timeline_grand_average.png','300-dpi PNG')+'; '+link('timeline_grand_average.svg','SVG')+'. Source '+link('timeline_grand_average.csv')+'; confirmation '+link('timeline_gate_confirmation.json')+'.','',
       '## Earlier screening NaN cause','',js('earlier_screening_nan_cause.json')['cause'],'',
       'All 64 earlier screening coupling strengths and frequency selections were finite; all 64 APC/scanned surrogate z fields were NaN. That screening is not a result of this prespecified run.','',
       '## Contacts fixed before any PAC output','',
       'The Amendment-3 order was followed: dataset flags, independent candidate/session robust masks, own-retained-trial power ratios, highest ratio with lower-k tie rule, then selected mask and eligibility. Welch used a symmetric 2000-sample Hann window, 1000-sample overlap, 2000-point FFT and 2000-Hz rate; retained trials were pooled with equal trial weights across sessions. Powers are trapezoidal integrals over inclusive 4-8 and 1-4 Hz bins.','',
       'The fixed contact table has 15 patients. Sub-13 has no Hipp-labelled candidate. Sub-11 has zero sessions with >=20 retained trials and therefore fails the >=2-session patient rule. The primary and referential plans have 13 patients, 52 sessions and 2008 included trials; the artifact-only plan has 14 patients, 62 sessions and 2890 trials. These are planned full analysis counts, not completed outcome denominators.','',
       table(contacts,['patient','deeper_contact','adjacent_contact','deeper_labels','adjacent_labels','candidate_pairs','theta_delta_ratio','retained_trials','eligible_sessions','patient_eligible','native_fs_hz']),
       'Every candidate pooled retained-trial count and rank is reported here:',table(rank,['patient','candidate_index','deeper_contact','adjacent_contact','retained_trials_total','theta_delta_ratio','selected']),
       'Every candidate/session rule count, threshold and retained-trial count: '+link('candidate_trial_counts.csv')+'. Fixed outputs: '+link('contacts.csv')+', '+link('trial_inclusion.csv')+', '+link('session_eligibility.csv')+', '+link('patient_eligibility.csv')+'. These files were completed and hashed before the first PAC output.','',
       '## Trial exclusions and planned sensitivity sets','',
       'Counts below cover the selected pairs in all 62 candidate-bearing sessions. Robust amplitude and first-difference counts are on dataset-unflagged trials; overlaps and their union are separate, so overlapping rules are not added twice. Session/patient eligibility is applied after the mask.',table(exclusions,['analysis','total_trials','dataset_artifact','amplitude_unflagged','difference_unflagged','both_robust_unflagged','robust_union_unflagged','retained_before_eligibility','retained_lost_session_eligibility','retained_lost_patient_eligibility','final_included']),
       'Sensitivity (a) retains the fixed selected pair and uses dataset flags only. Sensitivity (b) uses the deeper contact and the selected pair final mask. Sensitivity (c), the primary endpoint excluding non-2000-Hz patients, was not computed because the method-failure stop preceded every endpoint.','',
       '## Partial boundary-hit counts','',
       'These are completed-trial denominators only. APC bounds are fP within 0.05 Hz of 1/30 Hz and fA=80/150 Hz; scan bounds are fP=2/12 Hz and fA=80/148 Hz. Invalid APC results are retained in the all-trial denominator; valid-only phase-boundary counts are also shown.',table(bounds,['analysis','method','completed_trials','valid_trials','fp_low','fp_high','fa_low','fa_high','fp_boundary_fraction_all','fp_boundary_valid']),
       '## Endpoints not computed','',
       'The primary reproducibility test, all six secondary endpoints, the exploratory load model, sensitivity endpoint tests (a)-(c), trial-shuffle nulls and the four-panel endpoint figure were not computed. The incomplete run cannot support one of the prespecified primary decision forms. No empty or placeholder endpoint CSVs are supplied. The partial trial CSV is explicitly identified as partial in this report and STATUS.json.','',
       'The unchanged-source comparator copy and its reversible byte-diff verification are retained: '+link('ieeg_comparators.diff')+' and '+link('ieeg_comparator_copy_verification.json')+'. Comparator band guards: '+link('filter_guards.csv')+' (post-stop deterministic logging recovery, described below). Fourth-order notch pole guards: '+link('notch_filter_guards.csv')+'.','',
       '## Runtime and deviations','',
       'Common preprocessing: '+f"{js('preprocessing_runtime.json')['elapsed_seconds']:.3f}"+' s. Candidate masking/ranking and fixed tables: '+f"{js('selection_runtime.json')['elapsed_seconds']:.3f}"+' s. Partial method workers ran in parallel for '+', '.join(f"{w['elapsed_seconds']:.3f}" for w in workers)+' s; these stop at the shared stop flag and exclude startup/import before their timer. Three session partitions used one MATLAB computational thread each. No completed methods were rerun.','']
for x in deviations['deviations']:lines.append('- '+x['type']+': '+x['reason'])
lines+=['- The method-failure stop is the prespecified rule being followed, not a change to the method. No 3-s window, contact, mask, option, grid, filter, threshold or seed was adjusted after looking at method outputs.','',
        'Verification and file hashes: '+link('method_stop_verification.json')+'; '+link('output_manifest.json')+'.']
(O/'RESULTS_ieeg.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in status.items() if k!='provenance'}))
