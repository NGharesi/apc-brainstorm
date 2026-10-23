"""Verify and freeze Amendment-4 inputs/code before dataset estimates."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys,subprocess
O=Path(__file__).resolve().parent;R=O.parent.parent;sys.path.insert(0,str(R/'pydeps'))
import pandas as pd
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((O/'provenance.json').read_text(encoding='utf-8'))
assert json.loads((O/'am4_preprocessing_runtime.json').read_text(encoding='utf-8'))['status']=='COMPLETE'
assert not (O/'analysis_provenance.json').exists() and not (O/'ieeg_trial_estimates.csv').exists()
for r in m['file_sha256_records']:assert sha(Path(r['path']))==r['sha256']
for p,h in m['retained_shared_sha256'].items():assert sha(O/p)==h
I=pd.read_csv(O/'trial_inclusion_amendment4.csv',encoding='utf-8')
for c in ['retained','included','session_eligible','patient_eligible','dataset_artifact','am3_retained','am4_amplitude_reject','am4_difference_reject']:I[c]=I[c].astype(bool)
assert not I.duplicated(['analysis','patient','session','trial']).any()
assert I.included.equals(I.retained&I.session_eligible&I.patient_eligible)
for a,g in I.groupby('analysis'):
    expected=~g.dataset_artifact if a=='artifact_only' else g.am3_retained&~g.am4_amplitude_reject&~g.am4_difference_reject
    assert g.retained.equals(expected)
included=I[I.included];assert len(included)>0
pins=['am4_fixed_preprocessing_choices.json','am4_contacts.csv','am4_am3_mask.csv','trial_inclusion_amendment4.csv','session_eligibility_amendment4.csv','patient_eligibility_amendment4.csv','am4_evoked_template_audit.csv','am4_session_spectral_peaks.csv','ieeg_am4_preprocess.m','ieeg_am4_worker.m','ieeg_selected_series.m','ieeg_count_bursts.m','ieeg_comparators.m','ieeg_am4_pipeline.py']
m.update(stage='AMENDMENT4_ANALYSIS_FROZEN_BEFORE_FIRST_NEW_WINDOW_PAC',status='RUNNING_AMENDMENT4',frozen_utc=datetime.now(timezone.utc).isoformat(),frozen_analysis_sha256={p:sha(O/p) for p in pins},planned_analysis_counts={a:dict(patients=g.patient.nunique(),sessions=len(g[['patient','session']].drop_duplicates()),trials=len(g),method_rows=5*len(g)) for a,g in included.groupby('analysis')},unique_inputs=len(included),total_method_rows=5*len(included),worker_count=3)
m['statistics_implementation']=dict(seed=20261023,bootstrap_resamples=10000,shuffle_derangements=1000,SD_ddof=1,bootstrap='Percentile, median paired differences, patients sampled with replacement',wilcoxon='SciPy two-sided signed rank, zero_method wilcox, method auto; no multiplicity adjustment specified',ICC='Unbalanced one-way random-effects ICC(1), ANOVA k0; bootstrap patients as independent cloned clusters; negative values retained',mixed_model='MATLAB fitlme defaults, ML; SetSize continuous; patient/session random intercepts')
m['failure_monitor']='Progress-check session is not used as a gate. During the subsequent full run, check invalid fractions after additional session completion, separately by analysis and method. Stop if a majority is invalid; log contemporaneous counts. No method tuning.'
git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
assert subprocess.check_output([str(git),'-C',str(R/'apc-brainstorm-publish'),'status','--porcelain'],text=True,encoding='utf-8').strip()==''
for name in ['analysis_provenance.json','provenance.json']:(O/name).write_text(json.dumps(m,indent=2),encoding='utf-8')
(O/'STATUS.json').write_text(json.dumps(dict(status='RUNNING_AMENDMENT4',provenance_file='analysis_provenance.json',git_head=m['git_head'],protocol_sha256=m['protocol_sha256'],planned_analysis_counts=m['planned_analysis_counts']),indent=2),encoding='utf-8')
print(json.dumps(m['planned_analysis_counts']))
