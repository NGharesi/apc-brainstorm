"""Verify preserved partial outputs and the prespecified stop; no signal analysis."""
from pathlib import Path
import sys,json,hashlib,subprocess,re,warnings,shutil
O=Path(__file__).resolve().parent;R=O.parent.parent;repo=R/'apc-brainstorm-publish';sys.path.insert(0,str(R/'pydeps'))
import numpy as np
import pandas as pd
from scipy.io import loadmat
def js(n):return json.loads((O/n).read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()
m=js('analysis_provenance.json');s=js('STATUS.json');assert s['status']=='STOPPED_METHOD_RELEVANT' and s['completed_unique_inputs']==425 and s['partial_method_rows']==3165
for name,digest in m['frozen_analysis_sha256'].items():assert sha(O/name)==digest,f'Frozen input/wrapper changed: {name}'
for r in m['file_sha256_records']:assert sha(Path(r['path']))==r['sha256']
for r in js('attempt1_preservation_manifest.json')['files']:assert sha(O/'attempt1_archive'/r['path'])==r['sha256']
assert sha(O/'STOPPED_attempt1_sampling_rate.md')==sha(O/'attempt1_archive/STOPPED.md')
git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def g(*a):return subprocess.check_output([str(git),'-C',str(repo),*a],text=True,encoding='utf-8').strip()
assert g('status','--porcelain')=='' and g('branch','--show-current')=='neuroimage-submission'
assert g('rev-parse','HEAD')==g('rev-parse','origin/neuroimage-submission')==m['git_head']=='37c21dbe249881fdc021655a855c000434b3ac54'
assert m['protocol_sha256']=='087c51b1e5b930dca55e3c1ce63af15c891252399a3da1abc68407b27a2df308'
d=pd.read_csv(O/'ieeg_trial_estimates.csv',encoding='utf-8');assert len(d)==3165 and not d.duplicated(['analysis','patient','session','trial','method']).any()
assert d.groupby(['analysis','patient','session','trial']).size().eq(5).all()
assert d.git_head.eq(m['git_head']).all() and d.protocol_sha256.eq(m['protocol_sha256']).all()
apc=d[d.method=='APC-v1.0'];au=apc.drop_duplicates('checkpoint_file');assert len(au)==425 and au.status.value_counts().to_dict()=={4:326,0:99}
primary=apc[apc.analysis=='primary'];assert len(primary)==208 and primary.status.eq(4).sum()==154
cmp=d[d.method!='APC-v1.0'];assert cmp.status.eq(0).all() and np.isfinite(cmp.score).all()
features=['fP_hz','fA_hz','score','raw_mvl','ozkurt_mvl','preferred_phase_deg','status','effective_half_width_hz','n_bursts'];methods=['APC-v1.0','MVL-raw','MVL-Ozkurt','KLMI','GLM'];max_diff={k:0. for k in features}
for file,rows in d.groupby('checkpoint_file',sort=False):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore');saved=loadmat(file,variable_names=['features'],squeeze_me=True,struct_as_record=False)['features']
    assert len(saved)==5
    for k,name in enumerate(methods):
        q=rows[rows.method==name]
        for field in features:
            value=float(getattr(saved[k],field));vals=q[field].to_numpy(float);assert np.allclose(vals,value,rtol=5e-14,atol=5e-13,equal_nan=True),(file,name,field)
            if np.isfinite(value):max_diff[field]=max(max_diff[field],float(np.max(abs(vals-value))))
    metadata=json.loads(rows.provenance_json.iloc[0]);assert metadata['protocol_sha256']==m['protocol_sha256'] and metadata['seed']==20261023 and metadata['analysis_fs_hz']==2000
    assert metadata['apc_options']['fA']==[80,150] and metadata['apc_options']['stepFourMode']=='v1' and metadata['apc_options']['fPRefine']
assert len(list((O/'estimates').glob('*.mat')))==425 and not (O/'ieeg_trial_estimates.csv.lock').exists()
workers=[js(f'worker{k}_runtime.json') for k in [1,2,3]];assert all(w['status']=='FAILED_STOP' and w['identifier']=='IEEG:OtherWorkerStopped' for w in workers)
assert sum(w['computed_inputs'] for w in workers)==425 and sum(w['rows_written'] for w in workers)==3165
guards=pd.read_csv(O/'filter_guards.csv',encoding='utf-8');assert len(guards)==39 and guards.guard_passed.eq(1).all() and (guards.max_pole_radius<1).all() and (guards.max_sos_section_pole_radius<1).all() and (abs(guards.center_gain-1)<1e-3).all() and guards.reconstructed_logging_after_stop.eq(1).all() and guards.dataset_trials_rerun.eq(0).all()
for n in ['ieeg_session_summary.csv','ieeg_patient_summary.csv','ieeg_statistics.csv']:assert not (O/n).exists()
for path in [O/'RESULTS_ieeg.md',O/'STOPPED.md']:
    for target in re.findall(r'\]\(<([^>]+)>\)',path.read_text(encoding='utf-8')):
        target=re.sub(r':\d+$','',target)
        if Path(target) not in [O/'method_stop_verification.json',O/'output_manifest.json']:assert Path(target).exists(),target
flag=O/'METHOD_STOP_FLAG.json';archive=O/'method_stop_flag_last_worker.json'
if not archive.exists():shutil.copyfile(flag,archive)
rootstop=dict(status='FAILED_STOP',identifier='IEEG:MostTrialsInvalid',reason=s['reason'],final_unique_input_counts=s['final_unique_APC_status_counts'],partial_run=True,provenance=m,original_stop_snapshot='method_failure_first_snapshot.json')
flag.write_text(json.dumps(rootstop,indent=2),encoding='utf-8')
v=dict(status='PASS_STOP_HANDLING',provenance=m,git_clean=True,public_head_matches=True,protected_source_unchanged=True,frozen_tables_and_wrappers_unchanged=True,attempt1_files_preserved=True,unique_input_checkpoints=425,partial_method_rows=3165,APC_unique_status_counts={'4':326,'0':99},primary_completed_trials=208,primary_status4_trials=154,comparator_invalid_rows=0,CSV_checkpoint_numeric_match=True,maximum_CSV_checkpoint_absolute_differences=max_diff,all_workers_stopped=True,dataset_method_reruns=0,endpoint_outputs_absent=True,filter_guard_bands=39,filter_guard_logging_recovery_explicit=True,report_links_valid=True)
(O/'method_stop_verification.json').write_text(json.dumps(v,indent=2),encoding='utf-8')
records=[dict(path=str(p.relative_to(O)),bytes=p.stat().st_size,sha256=sha(p)) for p in O.rglob('*') if p.is_file() and p.name!='output_manifest.json' and not any(x in ['__pycache__','plot_config'] for x in p.relative_to(O).parts)]
(O/'output_manifest.json').write_text(json.dumps(dict(status='STOPPED_METHOD_RELEVANT',provenance=m,files=records),indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in v.items() if k!='provenance'}))
