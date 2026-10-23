"""Verify completed amended gates and common inputs while a fixed choice is pending."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys,subprocess,re
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent;REPO=ROOT/'apc-brainstorm-publish';sys.path.insert(0,str(ROOT/'pydeps'))
import pandas as pd
def js(n):return json.loads((OUT/n).read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()
meta=js('provenance.json');manifest=js('attempt1_preservation_manifest.json')
for r in manifest['files']:assert sha(OUT/'attempt1_archive'/r['path'])==r['sha256']
assert sha(OUT/'STOPPED_attempt1_sampling_rate.md')==sha(OUT/'attempt1_archive/STOPPED.md')
for r in meta['file_sha256_records']:assert sha(Path(r['path']))==r['sha256']
git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def run(*a):return subprocess.check_output([str(git),'-C',str(REPO),*a],text=True,encoding='utf-8').strip()
assert run('status','--porcelain')=='' and run('branch','--show-current')=='neuroimage-submission'
assert run('rev-parse','HEAD')==run('rev-parse','origin/neuroimage-submission')==meta['git_head']=='2b2bb08ff17fd96b1e520f9125e46655cd69786b'
assert meta['protocol_sha256']=='6f457fd2a2ca714abec723728e1a6617ef23b938f3da03bd025030642d63ad58'
e=js('equivalence_both_attempts.json');assert len(e['results'])==2 and all(r['passed'] and r['max_absolute_difference']<=1e-10 for r in e['results'])
f=pd.read_csv(OUT/'edf_file_checks_attempt2.csv',encoding='utf-8');c=pd.read_csv(OUT/'edf_channel_checks_attempt2.csv',encoding='utf-8');r=pd.read_csv(OUT/'resampling_trial_checks_attempt2.csv',encoding='utf-8')
assert len(f)==68 and f.passed.eq(1).all() and f.native_fs_hz.value_counts().to_dict()=={2000:38,4000:20,4096:10}
assert c.passed.eq(1).all() and c.nonfinite_samples.eq(0).all() and (c.variance_uv2>0).all() and (c.median_absolute_uv<1e4).all()
assert len(r)==3353 and r.passed.eq(1).all() and r.output_samples.eq(16000).all()
s=pd.read_csv(OUT/'timeline_resampling_trial_checks.csv',encoding='utf-8');sf=pd.read_csv(OUT/'timeline_file_checks.csv',encoding='utf-8')
assert len(s)==3353 and s.passed.eq(1).all() and s.output_samples.eq(1600).all() and sf.native_fs_hz.value_counts().to_dict()=={200:36,2000:2,4000:20,4096:10}
confirmation=js('timeline_gate_confirmation.json');assert confirmation['passed'] and [p['latency_ms'] for p in confirmation['peaks']]==[160,200]
pre=js('preprocessing_runtime.json');assert pre['status']=='COMPLETE' and pre['cache_files']==62 and len(list((OUT/'preprocessing').glob('*.mat')))==62
guards=pd.read_csv(OUT/'notch_filter_guards.csv',encoding='utf-8');assert len(guards)==3 and guards.passed.eq(1).all() and guards.digital_filter_order.eq(4).all() and (guards.max_pole_radius<1).all()
assert js('burst_count_diagnostic_verification.json')['passed']
for name in ['contacts.csv','trial_inclusion.csv','ieeg_trial_estimates.csv','ieeg_session_summary.csv','ieeg_patient_summary.csv','ieeg_statistics.csv']:assert not (OUT/name).exists()
meta.update(status='AWAITING_CONTACT_ORDER_CLARIFICATION',stage='All gates and common candidate input preparation complete; no selection spectra or method outcomes')
(OUT/'provenance.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
pending=dict(status='AWAITING_USER_CLARIFICATION',provenance=meta,question='Should each candidate pair receive its own per-session robust-rejection mask before ranking its power ratio, then select the highest ratio?',reason='Protocol 3.3 ranks using included trials under 3.5; 3.5 refers to the selected bipolar pair.',asked_via='request_user_input_async',dependent_work_not_started=['candidate spectra','contact ranking','trial inclusion decisions','APC and comparator estimates','endpoint runs'])
(OUT/'contact_order_clarification_pending.json').write_text(json.dumps(pending,indent=2),encoding='utf-8')
status=dict(status=meta['status'],provenance=meta,all_gates_passed=True,ieeg_files=68,ieeg_trial_resample_checks=3353,scalp_files=68,scalp_trial_resample_checks=3353,latencies_ms=[160,200],common_preprocessing_sessions=62,candidate_patients=14,dataset_apc_estimates=0,dataset_scan_estimates=0,required_next='User clarification of contact-ranking versus rejection order; pending async question',active_compute_jobs=0)
(OUT/'STATUS.json').write_text(json.dumps(status,indent=2),encoding='utf-8')
verification=dict(status='PASS_GATES_AND_COMMON_PREPARATION',provenance=meta,attempt1_files_preserved=len(manifest['files']),git_clean=True,pushed_head_matches=True,protected_source_hashes_unchanged=True,equivalence_attempts_passed=2,ieeg_files_passed=68,ieeg_channels_passed=len(c),ieeg_trials_16000_samples=3353,scalp_files_passed=68,scalp_trials_1600_samples=3353,timeline_passed=True,latencies_ms=[160,200],common_preprocessing_sessions=62,no_dataset_method_outcomes=True,contact_order_clarification_pending=True)
(OUT/'gate_preparation_verification.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
records=[dict(path=str(p.relative_to(OUT)),bytes=p.stat().st_size,sha256=sha(p)) for p in OUT.rglob('*') if p.is_file() and p.name!='output_manifest.json' and not any(x in ['__pycache__','plot_config'] for x in p.relative_to(OUT).parts)]
(OUT/'output_manifest.json').write_text(json.dumps(dict(provenance=meta,status=meta['status'],files=records),indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in verification.items() if k!='provenance'}))
