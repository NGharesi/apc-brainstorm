"""Record prespecified iEEG provenance without reading dataset signals."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
REPO=ROOT/'apc-brainstorm-publish'
GIT=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def git(*args): return subprocess.check_output([str(GIT),'-C',str(REPO),*args],text=True,encoding='utf-8').strip()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
assert git('branch','--show-current')=='neuroimage-submission'
assert git('status','--porcelain')==''
protocol=REPO/'protocol/APC_ieeg_ds004752_protocol.md'
assert sha(protocol)=='8c613b0f8d8ea61fb2a922fbfb58531907d37f278c596ea946a165f75837a804'
paths=[REPO/'src/bst_apc.m',REPO/'src/calc_MI_all_methods.m',ROOT/'revision_checks/rodent_multi/v1_bout_features.m',ROOT/'revision_checks/final/sos_comparators.m',ROOT/'revision_checks/final/final_sos_filter.m',protocol]
meta=dict(recorded_utc=datetime.now(timezone.utc).isoformat(),git_head=git('rev-parse','HEAD'),git_branch=git('branch','--show-current'),git_clean=True,protocol_sha256=sha(protocol),file_sha256={str(p):sha(p) for p in paths},matlab_version=None,toolbox_versions=None,seed=20261023,apc_options={'fA':[80,150]},comparator_settings=dict(profile='ieeg',phase_grid_hz=[2+i*.5 for i in range(21)],phase_half_width_hz=1.5,amplitude_grid_hz=list(range(80,149,4)),amplitude_half_width_hz=12,mode='ieeg_A2_prime'),analysis_window_s=[3,6],data_root=r'D:\APC_project\RealDatasets\OpenNeuro_ds004752',stage='GATES_ONLY_NO_DATASET_METHOD_OUTPUTS')
(OUT/'provenance.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
deviations=[dict(type='resolved tooling path lookup',reason='An initial read guessed a sidecar without the run-01 entity. File discovery established the actual BIDS names; no signal, setting or outcome was changed.')]
(OUT/'deviations.json').write_text(json.dumps(dict(deviations=deviations),indent=2),encoding='utf-8')
print(json.dumps(dict(git_head=meta['git_head'],git_clean=True,protocol_hash_matches=True)))
