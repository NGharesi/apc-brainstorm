"""Final facts, endpoint tables and provenance; no estimator/statistical reruns."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,subprocess
O=Path(__file__).resolve().parent;R=O.parent.parent;sys.path.insert(0,str(R/'pydeps'))
import pandas as pd
import numpy as np
def read(n):return pd.read_csv(O/n,encoding='utf-8')
def js(n):return json.loads((O/n).read_text(encoding='utf-8'))
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
        if isinstance(x,(float,np.floating)):return f'{x:.7g}'
        return str(x).replace('|','/')
    return '| '+' | '.join(cols)+' |\n| '+' | '.join('---' for _ in cols)+' |\n'+'\n'.join('| '+' | '.join(fmt(r[c]) for c in cols)+' |' for _,r in d.iterrows())+'\n'
m=js('analysis_provenance.json');assert js('amendment1_runtime.json')['status']=='COMPLETE' and not (O/'STOP_METHOD').exists()
D=read('ecog_bout_estimates.csv');T=read('ecog_statistics.csv');P=read('ecog_patient_summary.csv');E=read('electrodes.csv');I=read('inventory.csv');B=read('bouts.csv');B=B[B.analysed.astype(bool)];elig=read('patient_eligibility.csv');rates=read('status_boundary_rates.csv');eq=js('equivalence_gate.json');progress=js('progress_check.json')
assert len(D)==2648*5 and not D.duplicated(['patient','recording','bout','method']).any()
for p,h in m['reused_unchanged_sha256'].items():assert sha(O/p)==h
for r in m['protected_source_sha256']:assert sha(Path(r['path']))==r['sha256']
for n,h in m['amendment1_frozen_code_sha256'].items():assert sha(O/n)==h
A=js('attempt1_archive_manifest.json');assert all(sha(O/r['archived_path'])==r['sha256'] for r in A['moved_files'])
git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe');repo=R/'apc-brainstorm-publish'
def g(*a):return subprocess.check_output([str(git),'-C',str(repo),*a],text=True,encoding='utf-8').strip()
assert g('status','--porcelain')=='' and g('rev-parse','HEAD')==g('rev-parse','origin/neuroimage-submission')==m['git_head']
guards=pd.concat([read(f'filter_guards_w{k}.csv') for k in range(1,5)]+[read('filter_guards_progress.csv')],ignore_index=True).drop_duplicates();assert len(guards)==67 and guards.guard_passed.astype(bool).all();guards['git_head']=m['git_head'];guards['protocol_sha256']=m['protocol_sha256'];guards['seed']=20261024;guards.to_csv(O/'comparator_filter_guards.csv',index=False,encoding='utf-8')
old=pd.concat([read(f'attempt1_minphase1/estimates_w{k}.csv') for k in range(1,5)],ignore_index=True);old=old[old.method=='APC-v1.0'];oldrows=[]
for (rec,state),v in old.groupby(['recording','state']):oldrows.append(dict(recording=rec,state=state,bouts=len(v),valid=int(v.status.eq(0).sum()),status4=int(v.status.eq(4).sum()),other_invalid=int((v.status.ne(0)&v.status.ne(4)).sum())))
oldrows=pd.DataFrame(oldrows);oldrows['git_head']=m['git_head'];oldrows['protocol_sha256']=m['protocol_sha256'];oldrows['seed']=20261024;oldrows.to_csv(O/'attempt1_status_summary.csv',index=False,encoding='utf-8')
primary=T[(T.subset=='prespecified')&T.recording.eq('movement')&((T.endpoint=='within_state_fP_SD')|((T.endpoint=='coupling_state')&(T.method=='APC-v1.0')))];assert len(primary)==2
ethics=[s for s in (O/'README_motor_basic_dataset_notes_extracted.txt').read_text(encoding='utf-8').splitlines() if s.startswith('Ethics statement:')];assert len(ethics)==1
mixed=js('mixed_model_runtime.json');assert mixed['status']=='COMPLETE';model=read('mixed_model_coefficients.csv')
counts=B.groupby(['patient','recording','state']).size().unstack(fill_value=0).reset_index();counts=counts.merge(E[['patient','flagged']],on='patient',validate='many_to_one');reststats=read('rest_frequency_statistics.csv');restpatients=read('rest_frequency_patient_table.csv')
decision1=primary[primary.endpoint=='coupling_state'].iloc[0];decision2=primary[primary.endpoint=='within_state_fP_SD'].iloc[0]
boundaryPrimary=[]
for method in ['APC-v1.0','MVL-Ozkurt']:
    q=D[D.eligible_patient.astype(bool)&D.recording.eq('movement')&D.method.eq(method)];boundaryPrimary.append(dict(method=method,n_patients=q.patient.nunique(),n_bouts=len(q),fp_low=int(q.boundary_fp_low.sum()),fp_high=int(q.boundary_fp_high.sum()),any_fp_boundary_fraction=float((q.boundary_fp_low.astype(bool)|q.boundary_fp_high.astype(bool)).mean())))
lines=['# Miller library motor ECoG: Amendment 1 results','',
       'Primary 1: **'+decision1.decision+'**. Primary 2: **'+decision2.decision+'**. These decisions use the prespecified patient-bootstrap confidence intervals. The endpoint table and boundary rates are given below.','',
       '## Provenance and frozen methods','',
       'Amendment 1 was pushed before resumed analysis. Clean `neuroimage-submission` HEAD `'+m['git_head']+'`; protocol SHA-256 `'+m['protocol_sha256']+'`. HEAD equals origin. Protocol, src and tagged code remain untouched. Results are not committed. Attempt 1 was executed by Claude through a job runner on this computer. Current provenance: '+link('provenance.json')+'; immutable method-run record: '+link('analysis_provenance.json')+'.','',
       'The 19 prepared MAT files and all reused tables/helpers retain their pre-resume hashes. ecog_prepare was not rerun. The only changes to ecog_worker are the ECoG wrapper call and APC lower-bound flag (6 Hz). The new wrapper is an exact copy of v1_bout_features except its function name and options fA=[80,150], minPhaseHz=6, maxPhaseHz=30. The original raw-MVL and preferred-phase reconstruction asserts remain active. Diffs: '+link('v1_bout_features_ecog.diff')+' / '+link('ecog_worker_amendment1.diff')+'; reversible byte verification: '+link('amendment1_copy_verification.json')+'.','',
       'Scans retain phase 6:0.5:30 Hz (half-width 1.5), amplitude 80:4:148 Hz (half-width 30), the original metrics, tie rules and SOS guards. All other comparator profiles reverse to the original bytes. All 67 band designs passed: '+link('comparator_filter_guards.csv')+'. The saved preparation used the unchanged butter(4,...,stop) SOS implementation at 60/120/180 +/-1 Hz; its pole guards are retained in '+link('notch_filter_guards.csv')+'.','',
       '## Inventory and state gate','',
       'The preserved inventory contains '+str(len(I))+' recordings from '+str(I.patient.nunique())+' patients, all at 1000 Hz. State coding is documented in the local README: 0=rest, 11=tongue, 12=hand. Codes 13 in gf and 15 in zt were not analysed. Full recording rows:',table(I,['patient','recording','file','n_samples','n_channels','duration_s','fs_hz','codes_and_counts']),
       'The variance-based bad-channel fallback was used because no library bad-channel list was provided. Per-recording channel exclusions: '+link('bad_channels.csv')+'. Preserved bouts trim 0.5 s per edge, retain >=2 s, and exclude the first/last 2 s of recordings. Coordinates are the supplied Talairach location values.','',
       '## Ethics statement (verbatim)','',
       '> '+ethics[0],'',
       'Source: '+link(r'D:\APC_project\RealDatasets\Miller_ECoG_library\motor_basic\README_motor_basic_dataset_notes.docx')+'; extracted text '+link('README_motor_basic_dataset_notes_extracted.txt')+'.','',
       '## Equivalence and progress checks','',
       f'The original repository-source equivalence gate passed: maximum absolute difference {max(eq["absolute_differences"]):.17g}, tolerance 1e-10, status 0. '+link('equivalence_gate.json')+'. The amended wrapper also returned status 0 on the canonical input and passed its unchanged raw-MVL and preferred-phase asserts.','',
       'The first ten analysed bp movement-recording bouts returned status 0 in all ten, with fP values (Hz): '+', '.join(f'{x:.10g}' for x in progress['fP_hz'])+'. The progress check was not a gate, and the full run continued unchanged. Its ten complete keys seeded worker 1’s resume CSV; none was estimated twice. '+link('progress_check.json')+' / '+link('logs/progress_matlab.log')+'.','',
       '## Attempt 1 (APC phase range 1-30 Hz)','',
       'The original run stopped at the first combined rule-9.4 check: 127/200 bouts were invalid. Final in-flight results contained 225 complete bouts, 149 status 4 and 76 status 0. No endpoint was computed. The preserved status table is:',table(oldrows,['recording','state','bouts','valid','status4','other_invalid']),
       'All 15 moved files, including STOPPED.md, STOP_METHOD, worker estimates/status files/logs and the old runner sentinel, are unchanged by SHA-256. '+link('attempt1_archive_manifest.json')+'; archived stop '+link('attempt1_minphase1/STOPPED.md')+'.','',
       '## Electrodes, bouts and eligibility','',
       table(E,['patient','channel','x_tal','y_tal','z_tal','beta_peak_hz','selection_source','flagged','mapping_note']),
       'Imagery-rest selection is independent of the primary movement recording. Where imagery was absent, odd rest bouts selected the electrode and only even rest bouts entered analysis. There are 12 flagged patients overall, including ineligible jf; 11 flagged patients enter the 18-patient primary analysis. Sensitivity (a) therefore contains the 7 eligible unflagged patients. Imagery is a secondary replication and its rest data also served electrode selection as prespecified.','',
       'Analysed bout counts (before method failures):',table(counts,['patient','recording','move','rest','flagged']),
       'Movement eligibility (>=10 movement and >=10 rest bouts):',table(elig,['patient','move_bouts','rest_bouts','eligible']),
       'jf is ineligible: its 2-s stimulus blocks do not leave 2 s after the 1-s total trimming. It contributes only six analysed rest bouts and no movement bouts, so it is excluded from every endpoint. All 2648 planned bouts, including its diagnostic estimates, were processed once.','',
       '## Primary endpoints','',
       'Primary 1 uses each eligible patient’s movement-minus-rest mean APC normalized MVL. Primary 2 uses each patient’s mean of the two within-state fP SDs (sample SD, ddof=1), then APC-minus-MVL-Ozkurt differences. Bootstrap resamples patients 10000 times, seed 20261024 (NumPy MT19937 reset per endpoint); percentile 95% intervals use the mean for Primary 1 and median for Primary 2. Wilcoxon is two-sided, zero_method=wilcox, method=auto. There is no prespecified multiplicity correction.','',
       table(primary,['endpoint','method','n_patients','n_bouts','n_valid_bouts','n_move_valid','n_rest_valid','mean_difference','median_difference','t_statistic','t_df','t_p_two_sided','wilcoxon_statistic','wilcoxon_p_two_sided','ci_low','ci_high','decision']),
       'Phase-boundary rates alongside Primary 2 (eligible movement-recording bouts, both states pooled):',table(pd.DataFrame(boundaryPrimary),['method','n_patients','n_bouts','fp_low','fp_high','any_fp_boundary_fraction']),
       'For Primary 2 the inferential tests are the Wilcoxon and median-bootstrap interval; t-test columns are not applicable. Primary 1 decision: **'+decision1.decision+'**. Primary 2 decision: **'+decision2.decision+'**.','',
       'Prespecified primary-1 mixed model: outcome ~ state + (1 + state | patient), rest baseline, MATLAB fitlme default ML. It includes '+str(mixed['patients'])+' patients / '+str(mixed['bouts'])+' valid movement-recording APC bouts. '+link('mixed_model.mat')+'; log '+link('logs/mixed_model_matlab.log')+'.',table(model,[c for c in ['Name','Estimate','SE','tStat','DF','pValue','Lower','Upper'] if c in model.columns]),
       'Model warning: '+(str(mixed['warning_id'])+' '+str(mixed['warning_message']) if mixed['warning_id'] else 'none')+'. No alternate or simplified model was fitted. The one identical refit after the coefficient-export error produced exactly the same displayed model summary, coefficients and covariance parameters: '+link('mixed_export_recovery_verification.json')+'.','',
       '## Secondary 1: rest frequency','',
       'Patient medians are reported, with inclusive 12-20-Hz beta-range and +/-2-Hz agreement counts. Spectral peaks use analysed rest bouts, the same symmetric Hann(1000), overlap 500, 1000-point Welch settings, and the largest residual above the 8-30-Hz log-log fit.','',
       table(reststats[(reststats.subset=='prespecified')&(reststats.recording=='movement')],['method','n_patients','n_bouts','n_valid_bouts','patients_in_12_20_hz','proportion_in_12_20_hz','patients_within_2_hz','proportion_within_2_hz']),
       'Prespecified movement-recording patient rest medians:',table(restpatients[(restpatients.subset=='prespecified')&(restpatients.recording=='movement')],['patient','method','n_bouts','n_valid','median_fP_hz','rest_spectral_peak_hz','in_12_20_hz','within_2_hz_of_spectrum']),
       'All patient medians and spectral peaks, including sensitivities and imagery: '+link('rest_frequency_patient_table.csv')+'; source peaks '+link('analysed_rest_spectral_peaks.csv')+'.','',
       '## Secondary 2-5','',
       'All state-frequency/carrier-frequency differences are descriptive, with no expected direction. Each scan’s normalized coupling uses its own selected frequency pair. Imagery repeats the coupling state contrast; hand/tongue are separate descriptive comparisons against that patient’s analysed rest bouts. All use eligible patients and report their valid-bout denominators.',table(T[(T.subset=='prespecified')&~T.endpoint.eq('within_state_fP_SD')&~((T.endpoint=='coupling_state')&(T.method=='APC-v1.0'))],['recording','endpoint','method','n_patients','n_bouts','n_valid_bouts','mean_difference','wilcoxon_p_two_sided','ci_low','ci_high','decision']),
       'Full statistics (including t statistics, p values, state-specific valid counts and all sensitivity rows): '+link('ecog_statistics.csv')+'. Patient-level differences: '+link('patient_differences.csv')+'.','',
       '## Secondary 6: failures and boundaries','',
       'The table includes all processed bouts, including the six jf rest bouts; endpoint tables exclude jf. Scan boundaries are fP=6/30 and fA=80/148 Hz; APC boundaries are fP within 0.05 Hz of 6/30 and fA=80/150 Hz. Valid-only and all-bout boundary rates are separate:',table(rates,['recording','method','state','n_patients','n_bouts','n_valid','failure_count','failure_rate','fp_low','fp_high','fp_boundary_rate_all','fp_boundary_rate_valid','fa_low','fa_high','fa_boundary_rate_valid']),
       'These boundary rates must be considered alongside Primary 2: frequent lower-edge selection can reduce a method’s SD. All numeric fP values and per-patient boundary rates are in '+link('ecog_bout_estimates.csv')+' and '+link('ecog_patient_summary.csv')+'.','',
       '## Sensitivity analyses','',
       '(a) Excludes the 11 eligible flagged patients; seven patients remain. (b) Keeps only bouts >=2.5 s, with every other rule unchanged. No movement bouts meet the latter duration restriction, so its movement-rest and within-state comparative endpoints are not estimable. The threshold was not changed. Available rest-only summaries remain in the patient table.','',
       table(T[T.subset.ne('prespecified')&((T.endpoint=='within_state_fP_SD')|((T.endpoint=='coupling_state')&(T.method=='APC-v1.0')))],['subset','endpoint','n_patients','n_bouts','n_valid_bouts','mean_difference','median_difference','wilcoxon_p_two_sided','ci_low','ci_high','decision']),
       'All secondary sensitivity rows: '+link('ecog_statistics.csv')+'; patient/state summaries '+link('ecog_patient_summary.csv')+'.','',
       '## Figure and output files','',
       'Four panels: A patient/state mean fP (APC vs MVL-Ozkurt); B normalized MVL; C each patient’s movement-minus-rest APC normalized MVL with within-state bout-bootstrap 95% CIs (10000, seed 20261024); D patient median rest APC fP vs analysed-rest peak. There are no titles or footers inside the image. PNG at 300 dpi: '+link('ecog_four_panel.png')+'; vector '+link('ecog_four_panel.svg')+'. Commit, protocol hash and source CSVs are embedded as hidden metadata; '+link('figure_provenance.json')+'.','',
       'Merged per-bout results: '+link('ecog_bout_estimates.csv')+'. Patient summaries: '+link('ecog_patient_summary.csv')+'. Statistics: '+link('ecog_statistics.csv')+'. Per-bout burst counts were added as a separate unchanged-Step-1 diagnostic without rerunning APC frequency/coupling estimation. The detector matched the existing canonical count exactly; '+link('postprocess_runtime.json')+'. Worker CSVs are preserved.','',
       '## Runtime and deviations','',
       f'Progress plus four-worker run (including MATLAB startup): {js("amendment1_runtime.json")["elapsed_seconds"]:.3f} s. Supplemental burst diagnostics/rest spectra: {js("postprocess_runtime.json")["elapsed_seconds"]:.3f} s. Four MATLAB processes used one computational thread each. No completed dataset bout was recomputed.','']
for x in js('deviations.json')['deviations']:lines.append('- '+x['type']+': '+x['reason'])
lines+=['- The existing worker writes NaN in n_bursts. A separate diagnostic reproduces unchanged Step 1 from the saved prepared input and fills that recorded field in the merged CSV; no fP/fA/score is selected again and neither the copied feature wrapper nor the worker receives extra edits.','- The cached first ten progress bouts are absent from worker 1’s newly-computed status counter but present in its CSV and every final rate/statistic. The existing combined stop checks were retained; all 2648 completed bouts were checked at the end.','- Pre-existing MATLAB startup warnings concern missing historical Brainstorm directories. They did not change source precedence or the computations.','',
       'Preservation and completeness checks: '+link('final_verification.json')+'. Output inventory and hashes: '+link('output_manifest.json')+'.']
(O/'RESULTS_ecog.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
v=dict(status='COMPLETE',git_head=m['git_head'],protocol_sha256=m['protocol_sha256'],seed=20261024,clean_repository=True,origin_matches_HEAD=True,archive_files_verified=len(A['moved_files']),reused_files_verified=len(m['reused_unchanged_sha256']),protected_sources_verified=True,wrapper_worker_only_permitted_changes=True,analysed_bouts=2648,method_rows=len(D),all_bouts_have_five_methods=True,duplicate_method_rows=0,APC_scan_estimator_reruns=0,mixed_model_fit_attempts=2,mixed_model_second_fit_is_documented_export_recovery=True,comparator_guards=67,results_committed=False,primary_decisions=dict(primary1=decision1.decision,primary2=decision2.decision),finished_utc=datetime.now(timezone.utc).isoformat())
(O/'final_verification.json').write_text(json.dumps(v,indent=2),encoding='utf-8');current=js('provenance.json');current.update(status='COMPLETE',finished_utc=v['finished_utc'],results_report='RESULTS_ecog.md',final_verification='final_verification.json',effective_apc_options={**eq['options'],**m['apc_options_override']},statistics_implementation_file='statistics_analysis_plan.json');(O/'provenance.json').write_text(json.dumps(current,indent=2),encoding='utf-8')
files=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(O.glob('*')) if p.is_file() and p.name!='output_manifest.json'];(O/'output_manifest.json').write_text(json.dumps(dict(git_head=m['git_head'],protocol_sha256=m['protocol_sha256'],seed=20261024,files=files),indent=2),encoding='utf-8');print(json.dumps(v),flush=True)
