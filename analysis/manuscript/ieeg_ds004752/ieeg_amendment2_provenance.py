"""Record public Amendment 2 before either amended signal-reading gate."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,shutil,csv
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent;REPO=ROOT/'apc-brainstorm-publish'
GIT=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def git(*a):return subprocess.check_output([str(GIT),'-C',str(REPO),*a],text=True,encoding='utf-8').strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
head=git('rev-parse','HEAD');assert head=='2b2bb08ff17fd96b1e520f9125e46655cd69786b' and git('rev-parse','origin/neuroimage-submission')==head
assert git('status','--porcelain')=='' and git('branch','--show-current')=='neuroimage-submission'
protocol=REPO/'protocol/APC_ieeg_ds004752_protocol.md';digest=sha(protocol);assert digest=='6f457fd2a2ca714abec723728e1a6617ef23b938f3da03bd025030642d63ad58'
archive=OUT/'provenance_amendment1_before_reading.json';assert not archive.exists();shutil.copyfile(OUT/'provenance.json',archive)
meta=json.loads((OUT/'provenance.json').read_text(encoding='utf-8'))
for r in meta['file_sha256_records']:
    p=Path(r['path'])
    if p!=protocol:assert sha(p)==r['sha256']
    r['sha256']=sha(p)
meta.update(git_head=head,protocol_sha256=digest,amendment2_public_utc=datetime.now(timezone.utc).isoformat(),status='GATES_PENDING_AMENDMENTS_1_2',stage='Both amendments public; no resumed dataset signal read yet')
meta['push']=dict(status='SUCCEEDED',branch='neuroimage-submission',public_head=head,amendment1_head='63582a9926207d04629c8d30606be03d416c8baf',before_resumed_signal_analysis=True)
meta['resampling']=dict(function='MATLAB resample default FIR',trialwise=True,ieeg=dict(target_fs_hz=2000,output_samples=16000,native_rates=[2000,4000,4096],pq=[[1,1],[1,2],[125,256]]),scalp_timeline_only=dict(target_fs_hz=200,output_samples=1600,native_rates=[200,2000,4000,4096],pq=[[1,1],[1,10],[1,20],[25,512]],latency_resolution_ms=5))
(OUT/'provenance.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
results=[]
for attempt,name in [(1,'attempt1_archive/equivalence_gate.json'),(2,'equivalence_gate_attempt2.json')]:
    eq=json.loads((OUT/name).read_text(encoding='utf-8'));assert eq['passed']
    results.append(dict(attempt=attempt,passed=True,max_absolute_difference=max(eq['absolute_differences']),source_json=name,git_head_at_run=eq['provenance']['git_head'],protocol_sha256_at_run=eq['provenance']['protocol_sha256']))
(OUT/'equivalence_both_attempts.json').write_text(json.dumps(dict(provenance=meta,results=results),indent=2),encoding='utf-8')
d=json.loads((OUT/'deviations.json').read_text(encoding='utf-8'));d['amendment2_resumption']=dict(public_commit=head,protocol_sha256=digest,reason='User committed scalp-specific 200-Hz timeline handling before resumed signal processing; equivalence rerun already passed on unchanged source.')
(OUT/'deviations.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
print(json.dumps(dict(public_head=head,protocol_hash_matches=True,clean=True,equivalence_attempts_passed=2)))
