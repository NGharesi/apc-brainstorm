"""Package existing outputs after the requested method-relevant stop. No reruns."""
from pathlib import Path
import sys,json,hashlib,subprocess,re,datetime
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=ROOT/'revision_checks/final';REPO=ROOT/'apc-brainstorm-publish'
sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
import pandas as pd
from PIL import Image
GIT=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def git(*a):return subprocess.check_output([str(GIT),'-C',str(REPO),*a],text=True,encoding='utf-8').strip()
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def read(n):return pd.read_csv(OUT/n,float_precision='round_trip')
def link(p,label=None):return f'[{label or Path(p).name}](<{Path(p).resolve().as_posix()}>)'
def table(d,cols):
 def fmt(x):return ('NA' if not np.isfinite(x) else f'{x:.7g}') if isinstance(x,(float,np.floating)) else str(x)
 return '| '+' | '.join(cols)+' |\n| '+' | '.join('---' for c in cols)+' |\n'+'\n'.join('| '+' | '.join(fmt(row[c]) for c in cols)+' |' for _,row in d.iterrows())+'\n'
meta=json.loads((OUT/'analysis_provenance.json').read_text(encoding='utf-8'))
canonmeta=json.loads((OUT/'canonical_provenance.json').read_text(encoding='utf-8'))
audit=read('rodent_filter_audit.csv');row=audit[audit.fP_hz==4].iloc[0]
assert row.max_pole_ba>1 and row.relative_L2_difference>1e6
assert git('rev-parse','v1.0^{commit}')==meta['git_commit'];assert not git('status','--porcelain')
for f in meta['frozen_files']:assert sha(f['path'])==f['sha256']
rod=read('rodent_bouts.csv');stat=read('rodent_run_rest_statistics.csv');summ=read('rodent_state_summary.csv');canon=read('canonical_results.csv')
assert len(rod)==120 and len(canon)==4 and len(stat)==30
# Correct only export bookkeeping in NEW files, preserving original numerical outputs.
clean=canon.copy();clean['session']='canonical_20s';clean['seed']=12345
clean['provenance_json']=json.dumps(dict(meta,seed=12345,generator_settings=canonmeta),separators=(',',':'))
clean.to_csv(OUT/'canonical_results_export_corrected.csv',index=False,encoding='utf-8')
raw=rod.copy();raw['acceptance']=np.where(raw.method=='APC v1.0','APC completed; diagnostic equality passed','REJECTED: comparator filter numerics failed')
raw.to_csv(OUT/'rodent_bouts_with_acceptance.csv',index=False,encoding='utf-8')
st=stat.copy();st['acceptance']=np.where(st.method=='APC v1.0','APC completed','REJECTED: comparator filter numerics failed')
st.to_csv(OUT/'rodent_statistics_with_acceptance.csv',index=False,encoding='utf-8')
deviations=[
 {'type':'tooling','detail':'Metadata inspector initially aligned the crop by absolute timestamps. The crop restarts at zero; exact R2 indices 40800:372501 establish row-1 identity. No signal/bout changes.'},
 {'type':'tooling','detail':'First MATLAB launch failed pre-analysis source-path assertion because the workspace current directory shadowed the frozen file. Working directory changed to final; frozen path then asserted.'},
 {'type':'tooling','detail':'Canonical CSV auto delimiter detection failed after all rodent bouts completed. Explicit comma delimiter fixed import; only canonical stage resumed.'},
 {'type':'tooling','detail':'Figure build stopped at Figure 3 because Wilson endpoint floating-point roundoff produced a negative errorbar length. Figures 3-5 and supplements were not exported. No numerical recovery or interval result changed.'},
 {'type':'tooling','detail':'Filter audit first used a scalar frequency argument interpreted by freqz as an FFT length, then an incompatible empty-struct assignment. Frequency vector and concatenation fixed only the audit exporter.'},
 {'type':'tooling','detail':'Pre-existing MATLAB startup warnings refer to unavailable Brainstorm directories. No installation changed.'},
 {'type':'export bookkeeping','detail':'Canonical raw CSV used rodent session label and analysis seed in shared exporter. A new canonical_results_export_corrected.csv fixes session/seed metadata only; raw file retained. Actual canonical input seed is 12345; Poisson seed 20261022.'},
 {'type':'draft figure labeling','detail':'Figure 1 colorbar says CWT magnitude; the plotted frozen diagnostic is frequency-wise standardized CWT magnitude. The figure is retained as a draft, not approved for publication.'},
 {'type':'method-relevant failure','detail':'Rodent A2-prime direct-form butter(4)/filtfilt phase filters fail numerical stability/realization verification at fs approximately 1250 Hz. No comparator replacement applied. Analysis stopped and all rodent comparator rows/statistics rejected.'},
 {'type':'evidence limitation','detail':'E1/channel row 1 documented; no local session XML or channel-to-shank/layer map. Other-session run/rest bout eligibility not established.'}
]
(OUT/'deviations.json').write_text(json.dumps({'metadata':meta,'deviations':deviations},indent=2),encoding='utf-8')
stopped={'status':'STOPPED_METHOD_RELEVANT_FAILURE','metadata':meta,'failure':'Rodent comparator direct-form phase filter numerics','audit_path':str(OUT/'rodent_filter_audit.csv'),'first_run_bout_4Hz':{k:float(row[k]) for k in ['max_pole_ba','max_pole_zpk','center_gain_ba','center_gain_sos','rms_ba','rms_sos','relative_L2_difference']},'no_method_fix_applied':True,'completed_APC_bouts':24,'rejected_comparator_rows':96,'remaining':['Final comparator analysis/inference','Figures 3-5','development supplements','v2 negative-result supplement','final publication-figure approval']}
(OUT/'STOPPED.json').write_text(json.dumps(stopped,indent=2),encoding='utf-8')
# Preserve/check prior candidate-3 artifacts against its pre-existing final manifest.
prior=json.loads((ROOT/'revision_checks/v2/candidate_03/final_output_manifest.json').read_text(encoding='utf-8'))
for f in prior['files']:assert sha(ROOT/'revision_checks/v2/candidate_03'/f['path'])==f['sha256'],f['path']
figures=[]
for name in ['Figure_1_workflow','Figure_2_canonical_conditions']:
 p=OUT/(name+'.png');s=OUT/(name+'.svg')
 with Image.open(p) as im:
  dpi=im.info['dpi'];description=json.loads(im.info['Description']);assert abs(dpi[0]-300)<.01 and description['git_commit']==meta['git_commit'];im.verify()
 figures.append({'name':name,'status':'DRAFT: full package stopped; Figure 1 label issue documented' if name.startswith('Figure_1') else 'EXPORTED before stop; final approval pending','png':str(p),'svg':str(s),'source_csvs':description['source_files'],'metadata':description})
(OUT/'figure_manifest.json').write_text(json.dumps({'metadata':meta,'status':stopped['status'],'figures':figures},indent=2),encoding='utf-8')
verification={'status':stopped['status'],'metadata':meta,'frozen_files_unchanged':True,'git_tree_clean':True,'v1_tag_unchanged':True,'prior_candidate3_files_unchanged':len(prior['files']),'rodent_APC_diagnostic_exact_equality':24,'canonical_APC_diagnostic_exact_equality':4,'APC_status_nonzero':0,'comparator_numerics_passed':False,'completed_outputs_publication_ready':False,'exported_figure_png_dpi':300,'channel_match_samples':331702,'channel_match_max_absolute_difference':0,'all_bouts_unchanged':True}
(OUT/'verification.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
runtime=json.loads((OUT/'analysis_runtime.json').read_text(encoding='utf-8'))
# Windows creation time is the initial log timestamp; elapsed envelope includes startup.
rod_elapsed=(OUT/'rodent_bouts.csv').stat().st_mtime-(OUT/'analysis_retry_matlab.log').stat().st_ctime
lines=['# APC v1.0 final analysis — STOPPED','',
'**Stopped under the requested method-relevant failure rule.** The rodent A2′ comparator phase-filter realization failed numerical verification. No comparator implementation was replaced, no tagged method code was changed, and no further analyses or figures were run after confirming the failure. This is a partial report, not a completed final-paper package.','',
f'Primary APC tag `v1.0`, commit `{meta["git_commit"]}`. Frozen files were extracted byte-for-byte into `final/frozen_v1`; all 24 rodent APC bouts and all four canonical APC examples completed with status 0 and exactly matched the diagnostic-export copy. The Git tree remains clean. v2.0 remains the previously reported negative result: C1 FAIL, C2 PASS, C3 FAIL, C4 FAIL.','',
'## Method-relevant failure','',
'The rodent scan uses `[b,a]=butter(4,band/(fs/2),"bandpass")` followed by `filtfilt(b,a,x)`, inherited from the existing comparators. The numerical check uses the first saved run bout at the stored approximately 1250-Hz sampling rate. It compares that realization with a second-order-section (SOS) realization of the same nominal Butterworth design; the SOS check was diagnostic only, not a replacement benchmark run.','',
table(audit,['fP_hz','max_pole_ba','max_pole_zpk','center_gain_ba','center_gain_sos','rms_ba','rms_sos','relative_L2_difference']),
f'At 4 Hz: direct-form maximum pole magnitude {row.max_pole_ba:.12g}, RMS {row.rms_ba:.12g}; SOS maximum pole magnitude {row.max_pole_zpk:.12g}, RMS {row.rms_sos:.12g}. MATLAB also warned that the direct-form initial-condition matrix was nearly singular (RCOND 1.368249e-16). Audit: '+link(OUT/'rodent_filter_audit.csv')+'; '+link(OUT/'filter_audit_retry2_matlab.log')+'.','',
'**All 96 rodent comparator rows and their 24 inferential rows are rejected for scientific use.** They remain preserved and explicitly flagged. The APC v1.0 method uses its unchanged designfilt phase filter and SOS amplitude filter; this audit does not identify a failure of that tagged method. The held-out comparator CSVs were not rerun or altered; this report makes no new numerical-validity claim about their different sampling-rate settings.','',
'## Channel evidence','',
'Analyzed signal: **R2, E1, Brainstorm row/channel 1 (one-based)** from EC013/ec013.157. R2.Description is E1; its Comment says `Extract values: [0.000s,631.199s] E1`. Its extraction History identifies `EC013/ec013.157.eeg/data_block001.mat`. The imported channel file names row 1 E1. R2 samples 40800:372501 match row 1 of the saved 65-channel crop `data_230118_2215.mat` exactly: 331,702 samples, maximum absolute difference 0. The crop Time restarts at zero.','',
'**Shank, XML acquisition-channel index and anatomical layer are unresolved.** No session XML or explicit E1-to-shank/layer map was found in the inspected local LFP tree. The E1 channel record has empty Group and Comment and zero coordinates. E1 is not sufficient evidence for a zero-based acquisition index or anatomical layer. No shank number, CA1 label or layer is inferred. The original raw-file link points to `/Users/lucwilson/Desktop/crcns/hc3/ec013/ec013.157/ec013.157.eeg`, not a current local XML.','',
'The public [CRCNS hc-3 page](https://crcns.org/data-sets/hc/hc-3) identifies the dataset but does not establish this E1 mapping. The [ec013.157 forum discussion](https://crcns.org/forum/using-datasets/593514207) concerns cell/shank labels and does not map E1. Local evidence is in '+link(OUT/'channel_evidence.json')+'; inventory in '+link(OUT/'local_data_inspection.json')+'.','',
'## Unchanged bouts and method settings','',
'The existing 12 run and 12 rest bouts come directly from `apc_ec013_run_rest_results.mat`; all original start/stop indices and durations were retained. Original analysis interval: R2 indices 40800:372501; original speed criterion |speed|>6, minimum bout duration 5 s; approximately 1250 Hz. Definitions: '+link(OUT/'bout_definitions.csv')+'.','',
'APC v1.0: amplitude search [80,150] Hz; defaults otherwise, raw Canolty MVL without surrogate normalization. Ozkurt MVL = raw MVL / sqrt(mean(final amplitude envelope²)); preferred phase = angle(mean(A exp(i phase))) in degrees, from the same frozen final envelope/phase. The diagnostic copy exports arrays without changing calculations; its complete output and runInfo matched the untouched frozen function for every analyzed bout/example.','',
'Requested rodent A2′ scans: phase grid 4:0.5:12 Hz, half-width 1.5 Hz; amplitude grid 80:4:148 Hz, half-width 12 Hz. Independent grid maximum for raw MVL, Ozkurt MVL, KLMI (18 bins), GLM R². Ozkurt MVL was additionally computed at each selected pair. These scan results are rejected because of the filter audit.','',
'All rows with acceptance flags: '+link(OUT/'rodent_bouts_with_acceptance.csv')+'. Raw unmodified export: '+link(OUT/'rodent_bouts.csv')+'.','']
cols=['state','bout','duration_s','fP_hz','fA_hz','score','raw_mvl','ozkurt_mvl','preferred_phase_deg']
for method in ['APC v1.0','MVL-raw','MVL-Ozkurt','KLMI','GLM']:
 lines+=['### '+method+(' — REJECTED comparator results' if method!='APC v1.0' else ' — completed'),'',table(rod[rod.method==method],cols),'']
lines+=['## Run minus rest: inference and sensitivity','',
'The tables below were computed before the filter failure was confirmed. Comparator inference is REJECTED; only the APC rows are retained as completed estimates. Unit of resampling is a bout within this single session, not an animal. Primary estimates use equal bout weights. Welch t has Satterthwaite df and two-sided p. Hedges g uses the pooled within-state SD and exact gamma small-sample correction. The mean-difference CI is the 2.5th/97.5th percentile of 10,000 independent within-state bout resamples, fixed seed 20261022; the same indices are used for all methods/metrics. No multiplicity adjustment.','',
'Duration sensitivity normalizes durations within each state. Weighted variance = sum[p(x−mean)²]/(1−sum[p²]); effective n = 1/sum[p²]. Weighted Welch t/df and Hedges g use these variances and effective n. Bootstrap resampling keeps each bout value and duration together, then recomputes duration-weighted means. This is an explicitly specified weighted approximation.','',
'Statistics and acceptance flags: '+link(OUT/'rodent_statistics_with_acceptance.csv')+'. State summaries: '+link(OUT/'rodent_state_summary.csv')+'.','']
statcols=['method','metric','run_mean','rest_mean','mean_difference','welch_t','welch_df','p_two_sided','hedges_g','bootstrap_ci_low','bootstrap_ci_high']
for weighting in ['equal_bout','duration']:
 lines+=['### '+weighting+' — APC completed; all comparator rows REJECTED','',table(stat[stat.weighting==weighting],statcols),'']
lines+=['### State means and boundary counts','',table(summ,['method','state','n_bouts','duration_total_s','fP_mean','fA_mean','ozkurt_mean','fP_weighted','fA_weighted','ozkurt_weighted','boundary_4','boundary_12']), '',
'Boundary counts are exact equality to 4 or 12 Hz. APC has no 4–12-Hz scan bound; its counts are descriptive equalities only. Comparator counts are rejected along with the scans.','',
'## Optional additional sessions','',
'Eight other EC013 sessions are present locally: 156, 205, 206, 208, 251, 252, 374, 375. None has saved run/rest trial files in the inspected Brainstorm session folders. No other session with documented ≥8 run and ≥8 rest bouts of ≥5 s was established locally; no optional session replication was run and no additional-session data were downloaded.','',
'## Canonical examples completed before stopping','',
'The 20-s, 500-Hz 8/120-Hz coupled, jittered and continuous inputs were regenerated with the existing Python canonical generator and original seed/order 12345 and matched their historical signal CSVs to 1e-14. Original canonical settings include Gaussian sigma 30 ms, burst amplitude 1.8, low amplitude 1, baseline HF amplitude .15, white-noise SD .8. The jitter call explicitly used SD **0.020 s**. These settings differ from the held-out generator.','',
'The timing null changes only the true-burst component of the coupled canonical example, using a homogeneous Poisson rate of 8/s on (0.5,19.5) s, separate seed 20261022, 174 realized events; overlaps allowed. Low rhythm, baseline HF and noise samples are shared exactly. The original canonical fixed-count uniform-time null was not reused as a Poisson null.','',
table(clean,['state','fP_hz','fA_hz','raw_mvl','ozkurt_mvl','preferred_phase_deg']),
'Metadata-corrected export: '+link(OUT/'canonical_results_export_corrected.csv')+'. The original raw canonical CSV remains preserved; its shared exporter had populated the rodent session label and analysis seed. Corrected metadata changes no numerical output. Generator provenance: '+link(OUT/'canonical_provenance.json')+'.','',
'## Figure status and paths','',
'Two figures were exported before the stop as PNG at 300 dpi and SVG. Their embedded Description metadata contains the method commit, full settings, source CSV paths and SHA-256 hashes; source CSV filenames and commit are also visible. They are retained as drafts pending completion of the package. Figure 1 has a known colorbar-label issue: it says CWT magnitude but must say frequency-wise standardized CWT magnitude; the plotted values are the unchanged frozen diagnostics.','']
for f in figures:lines+=['- '+f['name']+': '+link(f['png'],'PNG')+'; '+link(f['svg'],'SVG')+'. '+f['status']+'.']
lines+=['','**Not exported:** Figures 3–5, development A0/A1/A2 supplements and the v2.0 negative-result supplement. The figure builder stopped on a Wilson errorbar rounding issue before the numerical filter failure was confirmed; the requested failure rule then stopped further work. The saved held-out and development CSVs were not changed. Figure manifest: '+link(OUT/'figure_manifest.json')+'.','',
'## Runtime and deviations','',
f'Canonical-only resumed MATLAB analysis: {runtime["elapsed_seconds"]:.6g} s, measured by tic/toc. The earlier MATLAB process completed all rodent bouts but aborted during canonical CSV import; its tic/toc total was not saved. Approximate launch-log-creation to rodent-CSV-write envelope: {rod_elapsed:.6g} s (includes startup; filesystem timestamps). No full successful report-build runtime exists because rendering aborted at Figure 3. Filter audit logs record all attempts.','',
'Tooling/export deviations (no tagged-method fix):','']
for d in deviations:
 if d['type']!='method-relevant failure':lines+=['- '+d['type']+': '+d['detail']]
lines+=['','Failure status and numbers: '+link(OUT/'STOPPED.json')+'. Deviations: '+link(OUT/'deviations.json')+'. Provenance: '+link(OUT/'analysis_provenance.json')+'. Integrity verification: '+link(OUT/'verification.json')+'. Output hashes: '+link(OUT/'output_manifest.json')+'.','',
'The minimal prospective comparator repair would be a numerically stable SOS realization of the same nominal Butterworth filters, followed by a full rodent scan/inference rerun. **It was not applied or evaluated**, consistent with the stop rule. No tagged APC code or earlier saved results were changed.','']
report=OUT/'RESULTS_final.md';report.write_text('\n'.join(lines),encoding='utf-8')
for a,b in re.findall(r'\]\((?:<([^>]+)>|([^\s)]+))\)',report.read_text(encoding='utf-8')):
 p=a or b
 if not p.startswith('http') and not p.endswith('output_manifest.json'):assert Path(p).exists(),p
files=[]
for p in sorted(OUT.rglob('*')):
 if p.is_file() and not any(x in ['plot_config','__pycache__'] for x in p.relative_to(OUT).parts) and p.name!='output_manifest.json':files.append({'path':str(p.relative_to(OUT)),'sha256':sha(p),'bytes':p.stat().st_size})
(OUT/'output_manifest.json').write_text(json.dumps({'metadata':meta,'status':stopped['status'],'files':files},indent=2),encoding='utf-8')
print(json.dumps({'status':stopped['status'],'APC_bouts':24,'comparator_rows_rejected':96,'figures_exported_before_stop':2,'prior_files_unchanged':len(prior['files']),'manifest_files':len(files),'report':str(report)}))
