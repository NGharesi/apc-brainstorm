"""Verify the stopped run and package evidence; no further signal analysis."""
from pathlib import Path
import sys,json,re,hashlib,subprocess
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent;REPO=ROOT/'apc-brainstorm-publish';sys.path.insert(0,str(ROOT/'pydeps'))
import pandas as pd
meta=json.loads((OUT/'provenance.json').read_text(encoding='utf-8'));status=json.loads((OUT/'STATUS.json').read_text(encoding='utf-8'))
def sha(p,start=0):
    h=hashlib.sha256()
    with p.open('rb') as f:
        f.seek(start)
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()
for r in meta['file_sha256_records']:assert sha(Path(r['path']))==r['sha256']
assert meta['protocol_sha256']=='8c613b0f8d8ea61fb2a922fbfb58531907d37f278c596ea946a165f75837a804'
git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def run(*args):return subprocess.check_output([str(git),'-C',str(REPO),*args],text=True,encoding='utf-8').strip()
assert run('status','--porcelain')=='' and run('branch','--show-current')=='neuroimage-submission'
assert run('rev-parse','HEAD')==meta['git_head']==run('rev-parse','origin/neuroimage-submission')
assert run('rev-parse','v1.0^{commit}')=='71ebc16aed32ca38be73a800738b975e5806b330'
eq=json.loads((OUT/'equivalence_gate.json').read_text(encoding='utf-8'));assert eq['passed'] and max(eq['absolute_differences'])<=1e-10
assert Path(eq['bst_apc_path'])==REPO/'src/bst_apc.m'
f=pd.read_csv(OUT/'edf_file_checks.csv',encoding='utf-8');c=pd.read_csv(OUT/'edf_channel_checks.csv',encoding='utf-8')
assert len(f)==39 and f.passed.eq(1).sum()==38 and f.iloc[-1].fs_hz==4000
assert len(c)==2224 and c.passed.eq(1).all() and c.fs_hz.eq(2000).all() and c.nonfinite_samples.eq(0).all() and (c.variance_uv2>0).all() and (c.median_absolute_uv<1e4).all()
for name in ['ieeg_trial_estimates.csv','ieeg_session_summary.csv','ieeg_patient_summary.csv','ieeg_statistics.csv','contacts.csv','trial_inclusion.csv','timeline_grand_average.csv']:assert not (OUT/name).exists()
assert status['dataset_apc_estimates']==status['dataset_scan_estimates']==status['reportable_endpoint_runs']==0
copies=json.loads((OUT/'edf_header_copies.json').read_text(encoding='utf-8'))['files']
for r in copies:
    original=Path(r['original_path']);copy=Path(r['read_path'])
    assert sha(original)==r['original_sha256'] and sha(copy)==r['copy_sha256']
    assert sha(original,256)==sha(copy,256)==r['payload_from_byte_256_sha256']
for p in [OUT/'STOPPED.md',OUT/'RESULTS_ieeg.md']:
    for t in re.findall(r'\]\(<([^>]+)>\)',p.read_text(encoding='utf-8')):assert Path(t).exists(),t
verification=dict(status='PASS_STOP_HANDLING',provenance=meta,reason=status['reason'],source_hashes_unchanged=True,protocol_hash_matches=True,git_clean=True,pushed_branch_matches_head=True,equivalence_passed=True,EDF_files_passed=38,EDF_channels_passed=2224,failure_fs_hz=4000,header_copy_payloads_identical=True,dataset_method_outputs_absent=True,endpoint_runs=0,report_links_valid=True)
(OUT/'stop_verification.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
records=[dict(path=str(p.relative_to(OUT)),bytes=p.stat().st_size,sha256=sha(p)) for p in OUT.rglob('*') if p.is_file() and p.name!='output_manifest.json' and '__pycache__' not in p.parts]
(OUT/'output_manifest.json').write_text(json.dumps(dict(provenance=meta,status='STOPPED_METHOD_RELEVANT',files=records),indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in verification.items() if k!='provenance'}))
