"""Read-only gate/source checks immediately before the authorized freeze."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
O=Path(__file__).resolve().parent;R=O.parent.parent;repo=R/'apc-brainstorm-publish'
git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def g(*a):return subprocess.check_output([str(git),'-C',str(repo),*a],text=True,encoding='utf-8').strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(n):return json.loads((O/n).read_text(encoding='utf-8'))
m=js('phaseA_implementation.json');result=js('gate_results.json')
assert result['status']=='GATES_PASSED'
assert all(result['gates'][k]=='PASS' for k in ['G0','G1','G2'])
assert result['gates']['G3']=='DESCRIPTIVE_COMPLETE'
assert g('rev-parse','HEAD')==g('rev-parse','origin/neuroimage-submission')==m['git_head']
assert g('branch','--show-current')=='neuroimage-submission'
for x in m['implementation_sha256']:assert sha(Path(x['path']))==x['sha256']
assert sha(repo/'protocol/APC_v3_aperiodic_protocol.md')==m['protocol_sha256']
assert not (O/'HA_inputs.mat').exists() and not (O/'HB_inputs.mat').exists()
assert subprocess.run([str(git),'-C',str(repo),'show-ref','--verify','--quiet','refs/tags/v3.0']).returncode==1
files=['src/bst_apc.m','src/apc_v3_spectral_peak.m','src/sp_raw_fp.m','analysis/v3_aperiodic/run_v3_gates.m','analysis/v3_aperiodic/v3_development_generator.m','analysis/v3_aperiodic/v3_ha_generator.m']
record=dict(status='GATES_PASSED_READY_TO_FREEZE',recorded_utc=datetime.now(timezone.utc).isoformat(),git_head=m['git_head'],protocol_sha256=m['protocol_sha256'],gates=result['gates'],heldout_generated=False,files=[dict(path=n,sha256=sha(repo/n)) for n in files],HA_conventions=dict(seed=20261101,stream='mrg32k3a',signal_substream=1,frequency_substream=2,poisson_substream=3,cell_order='beta, rhythm amplitude, duration, repeat; coupled then paired null',frequency_draw_order='fP U(6,25), fA U(80,140)',signal_draw_order='unit-SD powerlaw noise; Bernoulli cycle retention; Gaussian jitter; jittered-uniform background burst times',background='development sparsity recipe: one jittered-uniform time per cycle, peak-normalized envelope, amplitude 1.5*0.18, same carrier',true_and_null_envelopes='sum of 10-ms sigma Gaussian pulses, no peak normalization, amplitude 1.5',troughs='0.75/fP + integer/fP within sampled record',null='homogeneous Poisson rate 0.55*fP over [0,T), overlaps allowed, all other components identical'),HB_conventions='Exact existing v2 held-out generation and 20261022 mrg32k3a substreams; original v1 options fA [80,160] for saved per-trial equivalence; same range for v3; original A2-prime SOS grids')
(O/'freeze_precheck.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps(record),flush=True)
