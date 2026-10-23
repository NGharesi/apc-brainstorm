"""Package a protocol-6.4 stop without repeating any signal method or endpoint."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys,subprocess
O=Path(__file__).resolve().parent;R=O.parent.parent;sys.path.insert(0,str(R/'pydeps'))
import pandas as pd
import numpy as np
def js(n):return json.loads((O/n).read_text(encoding='utf-8'))
def read(n,**kw):return pd.read_csv(O/n,encoding='utf-8',**kw)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()
def link(n,label=None):
    p=Path(n);p=p if p.is_absolute() else O/p
    return f'[{label or p.name}](<{p.as_posix()}>)'
def table(d,cols):
    def fmt(x):
        if pd.isna(x):return 'NA'
        if isinstance(x,(float,np.floating)):return f'{x:.8g}'
        return str(x).replace('|','/')
    return '| '+' | '.join(cols)+' |\n| '+' | '.join('---' for _ in cols)+' |\n'+'\n'.join('| '+' | '.join(fmt(r[c]) for c in cols)+' |' for _,r in d.iterrows())+'\n'
m=js('analysis_provenance.json');run=js('am4_pipeline_runtime.json');assert run['status']=='STOPPED'
workers=[js(f'worker{k}_runtime.json') for k in range(4)];assert workers[0]['status']=='COMPLETE';assert all(w['status']=='FAILED_STOP' for w in workers[1:])
stamp=dict(git_head=m['git_head'],protocol_sha256=m['protocol_sha256'],seed=20261023,provenance_file='analysis_provenance.json')
def write(d,n):
    d=d.copy();d['git_head']=m['git_head'];d['protocol_sha256']=m['protocol_sha256'];d['seed']=20261023;d['provenance_file']='analysis_provenance.json';d.to_csv(O/n,index=False,encoding='utf-8');return d
d=read('ieeg_trial_estimates.csv');parts=pd.concat([read(f'ieeg_worker{k}_trial_estimates.csv') for k in range(4)],ignore_index=True);keys=['analysis','patient','session','trial','method'];assert not d.duplicated(keys).any() and len(d)==len(parts)
assert set(map(tuple,d[keys].to_numpy()))==set(map(tuple,parts[keys].to_numpy()))
apc=d[d.method.eq('APC-v1.0')];assert len(apc)==len(list((O/'estimates').glob('*.mat')))==sum(w['computed_inputs']+w.get('reused_inputs',0) for w in workers)
assert d[d.method.ne('APC-v1.0')].status.eq(0).all();assert all(Path(p).exists() for p in apc.checkpoint_file)
assert any(g.status.ne(0).mean()>.5 for _,g in apc.groupby('analysis'))
rates=[];bounds=[]
for (a,method),g in d.groupby(['analysis','method'],sort=True):
    valid=g.status.eq(0)&np.isfinite(g.score);fp=g.boundary_fp_low.astype(bool)|g.boundary_fp_high.astype(bool);fa=g.boundary_fa_low.astype(bool)|g.boundary_fa_high.astype(bool)
    rates.append(dict(analysis=a,method=method,n_patients=g.patient.nunique(),n_sessions=len(g[['patient','session']].drop_duplicates()),completed_trials=len(g),valid_trials=int(valid.sum()),status4_trials=int(g.status.eq(4).sum()),other_failures=int((~valid&g.status.ne(4)).sum()),failure_fraction=float((~valid).mean()),scope='PARTIAL AMENDMENT-4 RUN'))
    bounds.append(dict(analysis=a,method=method,completed_trials=len(g),valid_trials=int(valid.sum()),fp_low=int(g.boundary_fp_low.sum()),fp_high=int(g.boundary_fp_high.sum()),fa_low=int(g.boundary_fa_low.sum()),fa_high=int(g.boundary_fa_high.sum()),fp_boundary_all=float(fp.mean()),fp_boundary_valid=int((fp&valid).sum()),fp_boundary_rate_valid=float(fp[valid].mean()) if valid.any() else np.nan,fa_boundary_valid=int((fa&valid).sum()),fa_boundary_rate_valid=float(fa[valid].mean()) if valid.any() else np.nan,scope='PARTIAL AMENDMENT-4 RUN'))
rates=write(pd.DataFrame(rates),'partial_failure_rates.csv');bounds=write(pd.DataFrame(bounds),'partial_boundary_rates.csv');statusCounts=write(apc.groupby(['analysis','patient','session','status']).size().reset_index(name='completed_trials'),'partial_status_counts.csv')
I=read('trial_inclusion_amendment4.csv')
for c in ['included','retained','session_eligible','patient_eligible','dataset_artifact','am3_retained','am3_amplitude_reject','am3_difference_reject','am4_amplitude_reject','am4_difference_reject']:I[c]=I[c].astype(bool)
ex=[]
for a,g in I.groupby('analysis',sort=True):
    flag=g.dataset_artifact;rob=a!='artifact_only';oldreject=(~g.am3_retained)&~flag if rob else flag&False;newAmp=(g.am4_amplitude_reject&~flag) if rob else flag&False;newDiff=(g.am4_difference_reject&~flag) if rob else flag&False
    ex.append(dict(analysis=a,total_trials=len(g),dataset_artifact=int(flag.sum()),am3_amplitude_unflagged=int((g.am3_amplitude_reject&~flag).sum()) if rob else 0,am3_difference_unflagged=int((g.am3_difference_reject&~flag).sum()) if rob else 0,am3_robust_union_unflagged=int(oldreject.sum()),am4_amplitude_unflagged=int(newAmp.sum()),am4_difference_unflagged=int(newDiff.sum()),am4_robust_union_unflagged=int((newAmp|newDiff).sum()),am4_additional_reject_after_am3=int((g.am3_retained&(newAmp|newDiff)).sum()),retained_before_eligibility=int(g.retained.sum()),lost_session_eligibility=int((g.retained&~g.session_eligible).sum()),lost_patient_eligibility=int((g.retained&g.session_eligible&~g.patient_eligible).sum()),final_included=int(g.included.sum())))
ex=write(pd.DataFrame(ex),'trial_exclusion_summary_amendment4.csv')
inc=I[I.included];planned=inc.groupby(['analysis','patient','session']).size().rename('planned_trials').reset_index();actual=apc.groupby(['analysis','patient','session']).size().rename('completed_trials').reset_index();progress=planned.merge(actual,how='left',on=['analysis','patient','session']);progress['completed_trials']=progress.completed_trials.fillna(0).astype(int);progress['complete']=progress.completed_trials.eq(progress.planned_trials);write(progress,'partial_session_progress.csv')
progressCounts=write(apc[(apc.patient=='sub-01')&(apc.session=='ses-01')].groupby(['analysis','status']).size().reset_index(name='trials'),'am4_sub01_ses01_status_counts.csv')
guards=pd.concat([read(f'filter_guards_worker{k}.csv') for k in range(4)],ignore_index=True);originalGuardCols=[c for c in guards.columns if c!='provenance_json'];guards=guards.drop_duplicates(originalGuardCols);assert len(guards)==41;assert guards.guard_passed.astype(bool).all();write(guards,'filter_guards.csv')
archive=js('am4_archive_manifest.json');assert all(sha(O/r['archived_path'])==r['sha256'] for r in archive['moved_files']);assert all(sha(O/p)==h for p,h in archive['retained_shared_sha256'].items());assert all(sha(Path(r['path']))==r['sha256'] for r in m['file_sha256_records']);assert all(sha(O/p)==h for p,h in m['frozen_analysis_sha256'].items())
git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe');repo=R/'apc-brainstorm-publish'
def g(*a):return subprocess.check_output([str(git),'-C',str(repo),*a],text=True,encoding='utf-8').strip()
assert g('status','--porcelain')=='' and g('rev-parse','HEAD')==g('rev-parse','origin/neuroimage-submission')==m['git_head']
snap=js('am4_failure_first_snapshot.json');statuses={str(k):int(v) for k,v in apc.status.value_counts().sort_index().items()}
status=dict(status='STOPPED_METHOD_RELEVANT',reason='Protocol 6.4: most completed Amendment-4 APC inputs invalid',stopped_utc=datetime.now(timezone.utc).isoformat(),provenance=stamp,completed_inputs=len(apc),method_rows=len(d),completed_APC_status_counts=statuses,failure_fraction=float(apc.status.ne(0).mean()),n_patients=apc.patient.nunique(),n_sessions=len(apc[['patient','session']].drop_duplicates()),planned_analysis_counts=m['planned_analysis_counts'],sub01_ses01_progress_check='COMPLETED; counts logged; automatic full-run continuation performed unchanged',first_stop_snapshot='am4_failure_first_snapshot.json',endpoints_computed=False,nulls_computed=False,exploratory_models_computed=False,method_settings_changed_after_start=False,results_committed=False)
(O/'STATUS.json').write_text(json.dumps(status,indent=2),encoding='utf-8');current=js('provenance.json');current.update(status=status['status'],stage='Amendment 4 stopped under section 6.4',stop_record='STATUS.json',stopped_utc=status['stopped_utc']);(O/'provenance.json').write_text(json.dumps(current,indent=2),encoding='utf-8')
stop=['# STOPPED: Amendment 4, protocol section 6.4','',f'Most completed APC v1.0 inputs were invalid again: {int(apc.status.ne(0).sum())}/{len(apc)} ({100*apc.status.ne(0).mean():.1f}%). Status counts: {json.dumps(statuses)}. These are partial-run counts, not full-dataset rates.','',
      'The requested sub-01/ses-01 progress check completed and was not used as a gate. The full run continued automatically with the same source, options, windows, masks, templates and grids. The stop was triggered after additional session completion; its contemporaneous counts are in '+link('am4_failure_first_snapshot.json')+'.','',
      'All workers have stopped. Completed estimates and checkpoints are preserved. No primary decision, secondary endpoint test, null analysis, exploratory load model or final endpoint figure is available. Post-evoked Welch spectra and their prespecified peak locations were prepared before the method run; no spectral-peak association endpoint was tested.','',
      'Status 4 denotes either empty trough detections or empty phase-locked average/TF output in the unchanged APC source. The saved status does not distinguish these branches. No diagnostic method rerun or workaround was performed.','',
      'Public HEAD `'+m['git_head']+'`; protocol SHA-256 `'+m['protocol_sha256']+'`. Protocol, src and tagged code remain untouched; repository clean; results uncommitted.','',
      'Full report: '+link('RESULTS_ieeg.md')+'. Trial CSV: '+link('ieeg_trial_estimates.csv')+'. Counts: '+link('partial_failure_rates.csv')+'.']
(O/'STOPPED.md').write_text('\n'.join(stop)+'\n',encoding='utf-8')
old=read('attempt1_maintenance_3s/partial_failure_rates.csv');oldCounts=js('attempt1_maintenance_3s/STATUS.json');eq=read('equivalence_both_attempts.csv');contacts=read('contacts.csv');pe=read('patient_eligibility_amendment4.csv');se=read('session_eligibility_amendment4.csv');timeline=js('timeline_gate_confirmation.json')
source=R/'apc-brainstorm-publish/src/bst_apc.m'
lines=['# ds004752 iEEG: Amendment 4 stopped under protocol 6.4','',
       f'**Most completed inputs were again invalid for frozen APC v1.0.** There are {int(apc.status.ne(0).sum())}/{len(apc)} invalid inputs ({100*apc.status.ne(0).mean():.1f}%) in the partial Amendment-4 run. No completed primary decision is available. '+link('STOPPED.md')+'.','',
       '## Public protocol and provenance','',
       'Amendment 4 was pushed before any new-window analysis. HEAD `'+m['git_head']+'`; protocol SHA-256 `'+m['protocol_sha256']+'`. The repository is on clean branch `neuroimage-submission`, with HEAD equal to origin. The protocol, src and tagged code were not edited. No results were committed. Full options, MATLAB/toolbox versions, seed and source hashes: '+link('provenance.json')+'. Immutable pre-outcome freeze: '+link('analysis_provenance.json')+'.','',
       '## Attempt 1 (3-s maintenance window)','',
       'The 3-s [3,6) maintenance run stopped under section 6.4. At the first check, 325/422 unique trial-signal inputs returned status 4. Final in-flight counts were 326/425 status 4 (76.7%) and 99/425 status 0; the primary subset had 154/208 status 4. The partial run covered 2 patients and 6 sessions; 3 sessions completed their planned inputs and 3 were partial. All four scans returned valid scores on these completed inputs. No endpoint tests or nulls were computed. The reason for Amendment 4 is recorded in the committed protocol.','',
       table(old,['analysis','method','completed_trials','valid_trials','status4_trials','failure_fraction']),
       'All 455 archived files, including 425 unchanged checkpoint MATs, passed SHA-256 preservation checks. Original report: '+link('attempt1_maintenance_3s/RESULTS_ieeg.md')+'; original stop: '+link('attempt1_maintenance_3s/STOPPED.md')+'; manifest: '+link('am4_archive_manifest.json')+'. The contacts, candidate masks, original trial_inclusion.csv and reading/timeline gates stayed in place and retain their original hashes.','',
       '## Reused gates','',
       'Both repository-source equivalence checks passed (maximum absolute difference 3.694822225952521e-13; tolerance 1e-10). They used the src copy, not frozen_v1:',table(eq,['attempt','metric','expected','observed','absolute_difference','passed']),
       'All 68 iEEG files/3353 trials passed the amended reading and trialwise-resampling checks: EDF/JSON/channels.tsv rate agreement; allowed native rates; channel order/count; event sample count; 8-s trials; no NaN; nonzero channel variance; microvolt range. Every trial has 16000 samples after resampling to 2000 Hz. The native-rate table is:',table(read('native_ieeg_rate_summary.csv'),['native_fs_hz','n_patients','n_sessions']),
       'Reading records: '+link('edf_reading_gate_attempt2.json')+', '+link('edf_file_checks_attempt2.csv')+', '+link('edf_channel_checks_attempt2.csv')+', '+link('resampling_trial_checks_attempt2.csv')+'.','',
       'The scalp timeline check used all 3353 trials, available O1/O2/Oz, and per-trial 200-Hz resampling (1600 samples), with fixation-baseline subtraction and no added signal filter. The expected 1-s encoding and 6-s probe responses were confirmed:',table(pd.DataFrame(timeline['peaks']),['expected_onset_s','peak_time_s','latency_ms','peak_uv','absolute_peak_difference_uv']),
       'Latencies are at 5-ms resolution. Timeline '+link('timeline_grand_average.png','300-dpi PNG')+' / '+link('timeline_grand_average.svg','SVG')+'; source '+link('timeline_grand_average.csv')+'; gate '+link('timeline_gate_confirmation.json')+'. Paper evidence retained in '+link('timeline_paper_evidence.json')+': [Boran et al.](https://www.nature.com/articles/s41597-020-0364-3.pdf), [Dimakopoulos et al.](https://elifesciences.org/articles/78677).','',
       'Earlier screening NaN cause: '+js('earlier_screening_nan_cause.json')['cause'],'',
       '## Amendment 4 inputs and fixed choices','',
       'Each native 8-s trial was separately resampled to 2000 Hz, demeaned over the full 8 s, and filtered with the same fourth-order digital SOS notches at 50/100/150 Hz (+/-1 Hz). Samples 1:12000 form [0,6) s. The unchanged Amendment-3 selected-pair mask is intersected with the selected signal’s new 0-6-s amplitude and first-difference masks. Robust scales use the selected signal in all dataset-unflagged trials, per session, before evoked subtraction. Session >=20 and patient >=2-session eligibility was reapplied.','',
       'Separate included-trial mean waveforms were subtracted for every analysis/patient/session/signal. Sensitivity (a) keeps dataset artifact flags only at both stages and has its own bipolar mean; sensitivity (b) intersects the Amendment-3 selected-pair mask with the deeper-contact 0-6-s mask and uses its own referential mean. There is no post-subtraction rejection. These details were recorded before method outputs: '+link('am4_fixed_preprocessing_choices.json')+'. Template residual checks: '+link('am4_evoked_template_audit.csv')+'.','',
       'APC uses unchanged default v1 with fA=[80,150]. Scans use phase 1:0.5:12 (half-width 1.5, lower edge clipped at 0.5) and amplitude 80:4:148 (half-width 12), all four original metrics. Reversing the permitted wrapper edits reproduces the original comparator bytes exactly: '+link('am4_comparator_copy_verification.json')+' and '+link('am4_comparator_copy.diff')+'.','',
       'All 41 comparator-band guards were exported during actual trial processing and passed. '+link('filter_guards.csv')+'. The three unchanged notch designs passed their four-pole/radius checks: '+link('am4_notch_filter_guards.csv')+'.','',
       'Post-evoked Welch spectra used hann(2000), 50% overlap, nfft=2000 and equal trial weights. Spectral peaks were prepared from residuals above the log-log linear fit on 1-12 Hz, as amended: '+link('am4_session_spectral_peaks.csv')+'. The downstream dominant-rhythm endpoint was not tested. The shared [3,6) samples of the new pre-evoked inputs match the preserved old inputs exactly in both signal representations across all 62 sessions: '+link('am4_shared_preprocessing_verification.csv')+'.','',
       '## Fixed contacts and eligibility','',
       'Contacts and their original selection ratios are unchanged. The eligible_sessions field in the old contacts.csv belongs to Amendment 3; new eligibility appears separately below. Sub-13 has no Hipp-labelled candidate.',table(contacts,['patient','deeper_contact','adjacent_contact','deeper_labels','adjacent_labels','candidate_pairs','theta_delta_ratio','native_fs_hz']),
       'All original candidate retained-trial counts and ranks: '+link('candidate_rankings.csv')+'; every candidate/session rule count and threshold: '+link('candidate_trial_counts.csv')+'. Original selected masks: '+link('trial_inclusion.csv')+'.','',
       'New patient eligibility, separately by analysis:',table(pe,['analysis','patient','eligible_sessions','patient_eligible','native_fs_hz']),
       'Planned full-run sets (not completed outcome denominators): '+json.dumps(m['planned_analysis_counts'])+'. New per-session eligibility: '+link('session_eligibility_amendment4.csv')+'; per-trial rule flags and thresholds: '+link('trial_inclusion_amendment4.csv')+'.','',
       '## Trial exclusions','',
       'Rule counts overlap. The added-reject column counts the union of new amplitude/first-difference failures among trials that had passed Amendment 3. Dataset-flags-only sensitivity has zero applied robust-rejection counts.',table(ex,['analysis','total_trials','dataset_artifact','am3_amplitude_unflagged','am3_difference_unflagged','am3_robust_union_unflagged','am4_amplitude_unflagged','am4_difference_unflagged','am4_robust_union_unflagged','am4_additional_reject_after_am3','retained_before_eligibility','lost_session_eligibility','lost_patient_eligibility','final_included']),
       '## Requested sub-01/ses-01 progress check','',
       'This session was completed first. Its status counts were logged, and the full run continued automatically with no changes. It was not treated as a gate:',table(progressCounts,['analysis','status','trials']),
       'Original log '+link('am4_worker0_matlab.log')+'; progress record '+link('am4_sub01_ses01_progress_check.json')+'.','',
       '## Amendment 4 partial outcomes and stop','',
       f'The first subsequent stop check was after {snap["completed_full_run_sessions"]} additional session partitions completed. It recorded the following per-analysis/method counts; no subsequent method adjustment was made:',table(pd.DataFrame(snap['rates']),['analysis','method','n_completed','invalid','fraction_invalid']),
       f'After already-running inputs finished, {len(apc)} input checkpoints and {len(d)} method rows were preserved across {apc.patient.nunique()} patients and {len(apc[["patient","session"]].drop_duplicates())} sessions. These incomplete-run denominators are used below; no rates represent the full dataset.',table(rates,['analysis','method','n_patients','n_sessions','completed_trials','valid_trials','status4_trials','other_failures','failure_fraction']),
       'Status 4 can return at '+link(str(source)+':214','empty troughs')+' or '+link(str(source)+':224','empty phase-locked arrays')+'. The saved status does not distinguish those return branches. No diagnostic method rerun was performed. Incremental estimates: '+link('ieeg_trial_estimates.csv')+'; checkpoints in `estimates/`; completion table '+link('partial_session_progress.csv')+'; exact per-session/status counts '+link('partial_status_counts.csv')+'.','',
       '## Partial boundary hits','',
       'Scan boundaries are fP=1/12 and fA=80/148 Hz; APC boundaries are fP within 0.05 Hz of 1/30 and fA=80/150 Hz. All-trial and valid-only denominators are shown separately:',table(bounds,['analysis','method','completed_trials','valid_trials','fp_low','fp_high','fa_low','fa_high','fp_boundary_all','fp_boundary_valid','fp_boundary_rate_valid','fa_boundary_valid','fa_boundary_rate_valid']),
       '## Endpoints not computed','',
       'The primary paired reproducibility endpoint, secondary tests 1-6, exploratory load models, sensitivity endpoint tests (a)-(c), trial-shuffle nulls and the four-panel endpoint figure were not run after the method-failure stop. No prespecified primary decision form is stated for an incomplete run. The prepared post-evoked spectra/peak locations are supplied, but their association with APC was not tested. The reusable timeline figure remains available.','',
       '## Runtime and deviations','',
       f'Amendment-4 preparation: {js("am4_preprocessing_runtime.json")["elapsed_seconds"]:.3f} s. Pipeline including MATLAB startup/progress/full-run workers: {run["elapsed_seconds"]:.3f} s. Individual method-worker timers: '+', '.join(f'worker{w["worker"]} {w["elapsed_seconds"]:.3f} s' for w in workers)+'. No completed input was recomputed.','',
       'Amendments 1-4 are public protocol changes with their recorded reasons. Amendment 4 followed the failed 3-s attempt; it was frozen before the new-window method run. The stop under section 6.4 is compliance with the protocol. Tooling deviations inherited from the reading/selection run are listed below:','']
for x in js('deviations.json')['deviations']:lines.append('- '+x['type']+': '+x['reason'])
lines+=['','Two post-stop verification-only reader errors (singleton dimensions and opaque MATLAB string decoding) were fixed and logged above; no analysis was repeated. Earlier compatibility fixes and their logs are retained. Output packaging preserves every completed method result; source, contact masks, grids, windows, templates, thresholds and seeds were not tuned after outcomes. Every completed checkpoint’s numeric feature fields, options and grids were verified against the incremental CSV: '+link('am4_checkpoint_verification.json')+'.','',
        'Final preservation/source/checkpoint verification: '+link('am4_stop_verification.json')+'. Output inventory: '+link('output_manifest.json')+'.']
(O/'RESULTS_ieeg.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
verification=dict(provenance=stamp,archive_files_verified=len(archive['moved_files']),shared_hashes_verified=len(archive['retained_shared_sha256']),protected_source_hashes_verified=True,frozen_input_code_hashes_verified=True,clean_repository=True,public_HEAD=g('rev-parse','HEAD'),incremental_CSV_matches_workers=True,checkpoint_count_matches_rows=True,comparator_guards_passed=len(guards),method_reruns=0,results_committed=False,worker_states=[dict(worker=w['worker'],status=w['status']) for w in workers])
(O/'am4_stop_verification.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
inventory=[]
for p in sorted(O.glob('*')):
    if p.is_file() and p.name!='output_manifest.json':inventory.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)))
(O/'output_manifest.json').write_text(json.dumps(dict(provenance=stamp,files=inventory),indent=2),encoding='utf-8')
print(json.dumps(status),flush=True)
