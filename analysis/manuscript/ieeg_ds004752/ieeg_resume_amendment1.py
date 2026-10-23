"""Preserve attempt 1 and record the public Amendment 1 before resumed signals."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,shutil
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent;REPO=ROOT/'apc-brainstorm-publish'
GIT=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def git(*a):return subprocess.check_output([str(GIT),'-C',str(REPO),*a],text=True,encoding='utf-8').strip()
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()
assert git('branch','--show-current')=='neuroimage-submission' and git('status','--porcelain')==''
head=git('rev-parse','HEAD');assert head=='63582a9926207d04629c8d30606be03d416c8baf'
assert git('rev-parse','origin/neuroimage-submission')==head
protocol=REPO/'protocol/APC_ieeg_ds004752_protocol.md';digest=sha(protocol)
assert digest=='eb4c0a6e143bcdb61a2a4ed248ec31c72a3686bb8c7349e6003e7b31f1b59e84'
archive=OUT/'attempt1_archive';assert not archive.exists();archive.mkdir()
snapshot=[]
for p in sorted(OUT.iterdir()):
    if p.is_file() and p.name!='ieeg_resume_amendment1.py':
        snapshot.append(dict(path=p.name,sha256=sha(p),bytes=p.stat().st_size));shutil.copy2(p,archive/p.name)
stop=OUT/'STOPPED.md';dest=OUT/'STOPPED_attempt1_sampling_rate.md';assert stop.exists() and not dest.exists()
assert stop.resolve().parent==dest.resolve().parent==OUT.resolve();stop.rename(dest)
old=json.loads((archive/'provenance.json').read_text(encoding='utf-8'))
for record in old['file_sha256_records']:
    p=Path(record['path'])
    if p!=protocol:assert sha(p)==record['sha256'],f'Protected source changed: {p}'
meta=old.copy();meta.update(attempt=2,status='GATES_PENDING_AMENDMENT_1',stage='Amendment 1 public; resumed gates only',git_head=head,git_branch=git('branch','--show-current'),git_clean=True,protocol_sha256=digest,resumed_utc=datetime.now(timezone.utc).isoformat(),previous_attempt_git_head=old['git_head'],previous_attempt_protocol_sha256=old['protocol_sha256'],attempt1_archive='attempt1_archive',seed=20261023)
meta['file_sha256_records']=[dict(path=r['path'],sha256=sha(Path(r['path']))) for r in old['file_sha256_records']]
meta.pop('file_sha256',None);meta.pop('stopped_utc',None)
meta['push']=dict(status='SUCCEEDED',branch='neuroimage-submission',public_head=head,output='8183594..63582a9 neuroimage-submission -> neuroimage-submission',before_resumed_signal_analysis=True)
meta['resampling']=dict(target_fs_hz=2000,trialwise=True,function='MATLAB resample default FIR',native_rate_pq={'2000':[1,1],'4000':[1,2],'4096':[125,256]},output_samples_per_trial=16000)
(OUT/'provenance.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
(OUT/'attempt1_preservation_manifest.json').write_text(json.dumps(dict(provenance=meta,files=snapshot,archived_top_level_files=len(snapshot),header_copy_subtree_retained_in_place=True,renamed_stop=str(dest)),indent=2),encoding='utf-8')
d=json.loads((OUT/'deviations.json').read_text(encoding='utf-8'));d['amendment1_resumption']=dict(public_commit=head,protocol_sha256=digest,reason='User-authorized committed Amendment 1 replaces the native-rate stop; no dataset PAC outcomes preceded amendment.')
(OUT/'deviations.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
(OUT/'STATUS.json').write_text(json.dumps(dict(status='RESUMED_GATES_PENDING',provenance=meta,dataset_apc_estimates=0,dataset_scan_estimates=0),indent=2),encoding='utf-8')
print(json.dumps(dict(public_head=head,clean=True,protocol_hash_matches=True,attempt1_files_preserved=len(snapshot))))
