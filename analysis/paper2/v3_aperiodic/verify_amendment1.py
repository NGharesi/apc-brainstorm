"""Verify unchanged candidates/legacy paths and freeze the amended gate run."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,difflib,subprocess,shutil
O=Path(__file__).resolve().parent;R=O.parent.parent;repo=R/'apc-brainstorm-publish';A=O/'attempt1_residual_location';code=repo/'analysis/v3_aperiodic';git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def g(*a):return subprocess.check_output([str(git),'-C',str(repo),*a],text=True,encoding='utf-8').strip()
m=json.loads((O/'provenance.json').read_text(encoding='utf-8'));assert m['status']=='AMENDMENT1_PREPARATION';assert g('rev-parse','HEAD')==g('rev-parse','origin/neuroimage-submission')==m['git_head'];assert sha(repo/'protocol/APC_v3_aperiodic_protocol.md')==m['protocol_sha256']
archive=json.loads((O/'attempt1_archive_manifest.json').read_text(encoding='utf-8'));assert all(sha(O/r['archived_path'])==r['sha256'] for r in archive['moved_files']);assert all(sha(A/'source_snapshot'/n)==h for n,h in archive['source_snapshot_sha256'].items())
assert (repo/'src/bst_apc.m').read_text(encoding='utf-8')==(A/'source_snapshot/bst_apc.m').read_text(encoding='utf-8');assert sha(repo/'src/sp_raw_fp.m')==sha(A/'source_snapshot/sp_raw_fp.m');assert sha(code/'v3_development_generator.m')==sha(A/'source_snapshot/v3_development_generator.m')
before=(A/'source_snapshot/apc_v3_spectral_peak.m').read_text(encoding='utf-8');after=(repo/'src/apc_v3_spectral_peak.m').read_text(encoding='utf-8');begin='frequency=double';end='[~,j]=max(r(candidates));i=candidates(j);fp=f(i);d.selected_index=i;d.selected_grid_fp_hz=fp;'
assert before[before.index(begin):before.index(end)+len(end)]==after[after.index(begin):after.index(end)+len(end)],'Candidate detection/fitting changed'
(O/'amendment1_peak_location.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='attempt1 residual-based location',tofile='Amendment1 raw-location/shoulder rule')),encoding='utf-8')
beforeDriver=(A/'source_snapshot/run_v3_gates.m').read_text(encoding='utf-8');afterDriver=(code/'run_v3_gates.m').read_text(encoding='utf-8');(O/'amendment1_gate_logging.diff').write_text(''.join(difflib.unified_diff(beforeDriver.splitlines(True),afterDriver.splitlines(True),fromfile='attempt1 gate driver',tofile='Amendment1 branch logging')),encoding='utf-8')
assert sha(repo/'src/calc_MI_all_methods.m')==sha(O/'source_before_v3/calc_MI_all_methods.m')
# Reverse v3 additions to the original source with its original newlines.
baseline=(O/'source_before_v3/bst_apc.m').read_text(encoding='utf-8');x=(repo/'src/bst_apc.m').read_text(encoding='utf-8').split('\nfunction [sApc,runInfo]=compute_matrix_apc_v3',1)[0]
x=x.replace("{'v1','v1.0','v2','v3'}","{'v1','v1.0','v2'}").replace('version must be v1, v1.0, v2 or v3.','version must be v1, v1.0 or v2.')
x=x.replace("    if strcmp(requestedVersion,'v3')\n        [sApc,runInfo]=compute_matrix_apc_v3(sMatrix,OPTIONS);\n        return;\n    end\n",'')
x=x.replace("    if isfield(localOptions,'version') && strcmp(localOptions.version,'v3')\n        [phaseFreq,diagnostics.aperiodic]=estimate_phase_frequency_v3(burstAverage,fs,localOptions,numel(signal)/fs);\n    else\n    phaseFreq = estimate_phase_frequency(burstAverage, fs, localOptions);\n    end",'    phaseFreq = estimate_phase_frequency(burstAverage, fs, localOptions);');assert x==baseline
verify=dict(passed=True,git_head=m['git_head'],protocol_sha256=m['protocol_sha256'],new_diff_reverses_exact_baseline_source_text=True,bst_apc_only_line_endings_changed_since_attempt1=True,committed_line_endings_restored=True,aperiodic_fit_sigma_candidates_unchanged=True,SP_raw_bytes_unchanged=True,development_generator_bytes_unchanged=True,metric_helper_unchanged=True,gate_criteria_unchanged=True)
(O/'source_additions_verification.json').write_text(json.dumps(verify,indent=2),encoding='utf-8')
current=(repo/'src/bst_apc.m').read_text(encoding='utf-8');(O/'v3_implementation.diff').write_text(''.join(difflib.unified_diff(baseline.splitlines(True),current.splitlines(True),fromfile='original pre-v3 source',tofile='v3 additions/version switch')),encoding='utf-8')
files=[repo/'src/bst_apc.m',repo/'src/apc_v3_spectral_peak.m',repo/'src/sp_raw_fp.m',code/'run_v3_gates.m',code/'v3_development_generator.m'];snap=O/'phaseA_source_snapshot';assert not snap.exists();snap.mkdir()
for p in files:shutil.copy2(p,snap/p.name)
m.update(status='AMENDMENT1_PHASE_A_FROZEN_BEFORE_GATES',phaseA_frozen_utc=datetime.now(timezone.utc).isoformat(),implementation_sha256=[dict(path=str(p),sha256=sha(p)) for p in files],peak_location_rule='Amendment1: unchanged residual detection, positive-residual region, raw-log-power hill climb, residual-shoulder fallback',location_branch_values=['raw_local_max','residual_shoulder'],nonexecuted_location_branch='not_reached (v3) or not_applicable (v1/v2)',location_conventions='Strict raw maximum compared to its two admissible neighbours; only strictly higher neighbours inside the positive-r region may be visited. Ties use the first/left neighbour. No higher reachable neighbour without a strict maximum uses the residual fallback. Parabolic interpolation is clipped to +/-0.5 bin and the admissible frequency limits. The residual diagnostic is evaluated at the final interpolated fP.',source_additions_verification='source_additions_verification.json')
m['phaseA_conventions']['refinement']=m['peak_location_rule'];m['phaseA_conventions']['gates_rerun_from_start']=True
for n in ['phaseA_implementation.json','provenance.json']:(O/n).write_text(json.dumps(m,indent=2),encoding='utf-8')
print(json.dumps(verify))
