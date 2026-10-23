"""Aggregate exact saved-v1 checks and release workers without rerunning methods."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,sys
O=Path(__file__).resolve().parent;R=O.parent.parent;sys.path.insert(0,str(R/'pydeps'))
import pandas as pd
repo=R/'apc-brainstorm-publish';git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def g(*a):return subprocess.check_output([str(git),'-C',str(repo),*a],text=True,encoding='utf-8').strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((O/'phaseB_implementation.json').read_text(encoding='utf-8'))
assert not (O/'STOPPED.md').exists() and not (O/'HB_VERIFIED.json').exists()
assert g('rev-parse','HEAD')==g('rev-parse','origin/neuroimage-submission')==g('rev-list','-n','1','v3.0')==m['freeze_commit']
assert not g('status','--porcelain')
for x in m['implementation_sha256']:assert sha(Path(x['path']))==x['sha256']
assert json.loads((O/'HB_signal_verification.json').read_text(encoding='utf-8'))['complete_cases_bit_identical']
tables=[]
for w in range(1,5):
    z=json.loads((O/f'HB_v1_verified_w{w}.json').read_text(encoding='utf-8'));assert z['status']=='PASS'
    tables.append(pd.read_csv(O/f'HB_v1_equivalence_w{w}.csv',encoding='utf-8',float_precision='round_trip'))
D=pd.concat(tables).sort_values('input_id');assert len(D)==675 and D.input_id.nunique()==675
assert set(D.input_id)==set(range(1,676));assert D.exact.all() and D.route_exact.all()
D.to_csv(O/'HB_v1_equivalence.csv',index=False,encoding='utf-8',float_format='%.17g')
record=dict(status='PASS',freeze_commit=m['freeze_commit'],protocol_sha256=m['protocol_sha256'],released_utc=datetime.now(timezone.utc).isoformat(),inputs=675,complete_regenerated_cases_bit_identical=True,per_trial_fp_fa_score_status_route_exact=675,comparison_reference='original candidate_03 MAT tables (unrounded doubles)',provenance='phaseB_implementation.json')
(O/'HB_VERIFIED.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps(record),flush=True)
