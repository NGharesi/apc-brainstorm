"""Freeze the gate implementation and prove exact reversibility to the baseline."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,difflib,shutil,subprocess
O=Path(__file__).resolve().parent;R=O.parent.parent;repo=R/'apc-brainstorm-publish';A=repo/'analysis/v3_aperiodic'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((O/'provenance.json').read_text(encoding='utf-8'))
assert m['status']=='STEP0_COMPLETE_BEFORE_IMPLEMENTATION' and m['version_metadata_source']=='Independent current MATLAB runtime'
before=(O/'source_before_v3/bst_apc.m').read_bytes();current=(repo/'src/bst_apc.m').read_bytes();newline=b'\r\n' if b'\r\n' in before else b'\n';x=current.decode('utf-8').replace('\r\n','\n')
x=x.split('\nfunction [sApc,runInfo]=compute_matrix_apc_v3',1)[0]
x=x.replace("{'v1','v1.0','v2','v3'}","{'v1','v1.0','v2'}").replace('version must be v1, v1.0, v2 or v3.','version must be v1, v1.0 or v2.')
branch="    if strcmp(requestedVersion,'v3')\n        [sApc,runInfo]=compute_matrix_apc_v3(sMatrix,OPTIONS);\n        return;\n    end\n"
assert x.count(branch)==1;x=x.replace(branch,'')
block="    if isfield(localOptions,'version') && strcmp(localOptions.version,'v3')\n        [phaseFreq,diagnostics.aperiodic]=estimate_phase_frequency_v3(burstAverage,fs,localOptions,numel(signal)/fs);\n    else\n    phaseFreq = estimate_phase_frequency(burstAverage, fs, localOptions);\n    end"
assert x.count(block)==1;x=x.replace(block,'    phaseFreq = estimate_phase_frequency(burstAverage, fs, localOptions);')
assert x.replace('\n',newline.decode('ascii')).encode('utf-8')==before,'New changes exceed the permitted additions/version switch'
assert sha(repo/'src/calc_MI_all_methods.m')==sha(O/'source_before_v3/calc_MI_all_methods.m')
m['protected_baseline_sha256_records']=[dict(path=str(repo/'src'/n),sha256=sha(O/'source_before_v3'/n)) for n in ['bst_apc.m','calc_MI_all_methods.m']]
v2prefix=b'function [sApc,runInfo]=compute_matrix_apc_v2';oldv2=before.split(v2prefix,1)[1];newv2=current.split(v2prefix,1)[1].split(newline+b'function [sApc,runInfo]=compute_matrix_apc_v3',1)[0];assert oldv2==newv2
(O/'v3_implementation.diff').write_text(''.join(difflib.unified_diff(before.decode('utf-8').splitlines(True),current.decode('utf-8').splitlines(True),fromfile='8cabe20 before v3',tofile='v3 additions and switch')),encoding='utf-8')
verification=dict(passed=True,new_diff_reverses_exact_baseline=True,preexisting_v2_code_bytes_unchanged=True,metric_helper_bytes_unchanged=True,preexisting_v1_tag_additions='Existing v2 additions are preserved in preexisting_v1_tag_diff.patch; the new delta is verified separately',git_head=m['git_head'],protocol_sha256=m['protocol_sha256'])
(O/'source_additions_verification.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
files=[repo/'src/bst_apc.m',repo/'src/apc_v3_spectral_peak.m',repo/'src/sp_raw_fp.m',A/'run_v3_gates.m',A/'v3_development_generator.m']
snapshot=O/'phaseA_source_snapshot';snapshot.mkdir()
for p in files:shutil.copy2(p,snapshot/p.name)
m.update(status='PHASE_A_FROZEN_BEFORE_GATES',phaseA_frozen_utc=datetime.now(timezone.utc).isoformat(),source_committed=False,implementation_sha256=[dict(path=str(p),sha256=sha(p)) for p in files],implementation_diff='v3_implementation.diff',source_additions_verification='source_additions_verification.json',phaseA_conventions=dict(duration='N/fs',OLS='Backslash on [log10(f), ones], two passes',sigma='Sample SD (std(...,0)) of pass-2 residuals at pass-2 points',refinement='Three-point parabola on residual, delta clipped to +/-0.5 bin; peak-height diagnostic evaluated on that parabola',powerlaw_noise='Original development-family Hermitian random-phase FFT with amplitude f^(-beta/2), zero DC, mean removed, unit sample SD',G2_order='beta=1,2; duration=2,6; repeats1:20; rng(20261031,twister)',burst_times='Sinusoid troughs within the recording, independent Bernoulli .55 cycle retention, independent Gaussian 5-ms jitter; Gaussian envelopes add without global normalization; no extra background bursts in G2',G3='Same four cells and 20 repeats, separate reset rng(20261031,twister), homogeneous rate .55*15/s, no rhythm, no rejection gate',stop='G0 then G1, then each G2 cell; failed gate/cell stops immediately; no held-out generation before pushed freeze'))
(O/'phaseA_implementation.json').write_text(json.dumps(m,indent=2),encoding='utf-8');(O/'provenance.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
d=json.loads((O/'deviations.json').read_text(encoding='utf-8'));d['deviations'].append(dict(type='Read-only git inspection working directory',reason='One exploratory git diff used the parent process folder and failed to resolve the tag. It was repeated in the repository; no file, code or signal was changed.'))
d['deviations'].append(dict(type='Pre-gate source-verifier line endings',reason='The verifier initially assumed LF but the source checkout uses CRLF. It now detects the original newline, reverses the permitted edits, restores that newline and requires exact original bytes. The v2 block is compared as bytes directly. No method source was altered by this fix and no gate or signal output had been computed. The initial read-only diagnostic also failed before printing the new-source branch; it made no file changes.'))
d['deviations'].append(dict(type='Pre-gate provenance JSON field names',reason='MATLAB jsondecode sanitised filename keys containing dots in the initial provenance struct. The source verifier now compares directly with the preserved baseline bytes and records file hashes as path/sha256 array records, avoiding filename-as-key rewriting. This metadata-reader fix occurred before any gate output; no method code or setting changed.'))
(O/'deviations.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
print(json.dumps(verification))
