"""Report a failed prespecified gate using saved outputs only."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys,subprocess
O=Path(__file__).resolve().parent;R=O.parent.parent;repo=R/'apc-brainstorm-publish';sys.path.insert(0,str(R/'pydeps'))
import pandas as pd
import numpy as np
import h5py
def js(n):return json.loads((O/n).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def link(n,label=None):
    p=Path(n);p=p if p.is_absolute() else O/p
    return f'[{label or p.name}](<{p.as_posix()}>)'
def table(d,cols):
    def fmt(x):
        if pd.isna(x):return 'NA'
        if isinstance(x,(float,np.floating)):return f'{x:.12g}'
        return str(x).replace('|','/')
    return '\n| '+' | '.join(cols)+' |\n| '+' | '.join('---' for _ in cols)+' |\n'+'\n'.join('| '+' | '.join(fmt(r[c]) for c in cols)+' |' for _,r in d.iterrows())+'\n'
result=js('gate_results.json');assert result['status']=='STOPPED_GATE_FAILURE';m=js('phaseA_implementation.json');failed=result['failed_gate'];g0=js('G0.json')
for record in m['implementation_sha256']:assert sha(Path(record['path']))==record['sha256']
assert sha(repo/'protocol/APC_v3_aperiodic_protocol.md')==m['protocol_sha256']
assert sha(repo/'src/calc_MI_all_methods.m')==sha(O/'source_before_v3/calc_MI_all_methods.m')
git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def g(*a):return subprocess.check_output([str(git),'-C',str(repo),*a],text=True,encoding='utf-8').strip()
assert g('rev-parse','HEAD')==g('rev-parse','origin/neuroimage-submission')==m['git_head']
tagcheck=subprocess.run([str(git),'-C',str(repo),'show-ref','--verify','--quiet','refs/tags/v3.0'],capture_output=True);assert tagcheck.returncode==1
D=pd.read_csv(O/'gate_trials.csv',encoding='utf-8') if (O/'gate_trials.csv').exists() else pd.DataFrame()
cell=pd.read_csv(O/'G2_cell_summary.csv',encoding='utf-8') if (O/'G2_cell_summary.csv').exists() else pd.DataFrame()
v2=[]
with h5py.File(O/'G0.mat','r') as f:
    for group in ['referenceV2','currentV2']:
        row=dict(source=group)
        for name in ['phase_frequency_hz','amplitude_frequency_hz','pac_strength','preferred_phase_deg','status_code']:row[name]=float(np.array(f[group][name]['Value']).squeeze())
        v2.append(row)
pd.DataFrame(v2).assign(git_head=m['git_head'],protocol_sha256=m['protocol_sha256'],implementation_record='phaseA_implementation.json').to_csv(O/'G0_v2_reproduction.csv',index=False,encoding='utf-8')
gates=pd.DataFrame([dict(gate=k,result=v) for k,v in result['gates'].items()]);gates.assign(git_head=m['git_head'],protocol_sha256=m['protocol_sha256']).to_csv(O/'gate_summary.csv',index=False,encoding='utf-8')
canon=pd.DataFrame(dict(metric=['fP_hz','fA_hz','raw_MVL','preferred_phase_deg'],expected=g0['canonical_expected'],observed=g0['canonical_observed'],absolute_difference=g0['canonical_absolute_differences']))
g1=D[D.gate.eq('G1')] if not D.empty else pd.DataFrame();g1text='G1 was not run.'
if not g1.empty:
    z=g1.iloc[0];g1text=f'Canonical v3: status {int(z.status)}, fP {z.fP_hz:.17g} Hz, fA {z.fA_hz:.17g} Hz; |fP-8|={abs(z.fP_hz-8):.17g} Hz and |fA-120|={abs(z.fA_hz-120):.17g} Hz. Required: status 0, <=0.1-Hz fP error and <=8-Hz fA error.'
detail=g1text
if failed=='G0':detail='G0 regression/source checks failed; the exact checks are recorded in G0.json.'
elif failed=='G2' and not cell.empty:
    z=cell.iloc[-1];detail=f'G2 cell beta={z.beta:g}, T={z.duration_s:g} s: v3 fP recovery {int(z.v3_fp_recovery)}/20; required >=16/20. v1 recovery on the same inputs was {int(z.v1_fp_recovery)}/20.'
status=dict(status='STOPPED_GATE_FAILURE',failed_gate=failed,gates=result['gates'],git_head=m['git_head'],protocol_sha256=m['protocol_sha256'],stopped_utc=datetime.now(timezone.utc).isoformat(),heldout_generated=False,freeze_commit_created=False,v3_tag_created=False,source_committed=False,method_redesign_after_gate=False,results_committed=False,phaseA_elapsed_seconds=result['elapsed_seconds'])
(O/'STATUS.json').write_text(json.dumps(status,indent=2),encoding='utf-8');current=js('provenance.json');current.update(status=status['status'],failed_gate=failed,gate_results='gate_results.json',source_committed=False,v3_tag_created=False,heldout_generated=False,results_committed=False);(O/'provenance.json').write_text(json.dumps(current,indent=2),encoding='utf-8')
stop=['# STOPPED: APC v3 gate '+failed+' failed','',
      'The run stopped under protocol section 6.5. '+detail,'',
      'No method redesign or workaround was made after the gate result. No v3.0 freeze commit/tag was created, no held-out signal was generated, and Phases B/C did not run. The candidate source remains uncommitted for review; the default v1 and existing v2 paths were checked under G0. No results were committed.','',
      'Report: '+link('RESULTS_v3.md')+'. Gate record: '+link('gate_results.json')+'. Per-trial outputs: '+link('gate_trials.csv')+'.']
(O/'STOPPED.md').write_text('\n'.join(stop)+'\n',encoding='utf-8')
lines=['# APC v3 aperiodic correction: stopped at '+failed,'',
       '**Prespecified gate '+failed+' failed.** '+detail+' The phase stopped with no redesign, freeze, held-out generation or real-data evaluation. '+link('STOPPED.md')+'.','',
       '## Public protocol and implementation provenance','',
       'Clean `neuroimage-submission` HEAD `'+m['git_head']+'` was pushed before v3 implementation. Protocol SHA-256 `'+m['protocol_sha256']+'` matches. The protocol was not edited. MATLAB '+m['matlab_version']+'; complete toolbox versions and baseline source hashes: '+link('provenance.json')+'. The gate-tested source is uncommitted and identified by SHA-256 in '+link('phaseA_implementation.json')+' and preserved in `phaseA_source_snapshot/`. No results were committed.','',
       'v3 is an explicit version selection; default v1 remains unchanged. The implementation shares v1 Steps 1, 3 and 4, and substitutes the two-pass aperiodic residual peak rule only for v3 Step 2. SP-raw uses the same fitting/peak helper on its specified raw-signal Hann/50%-overlap Welch spectrum. T=N/fs; residual sigma uses sample SD; the parabolic delta is clipped to +/-0.5 bin. Complete pre-gate numerical/generator conventions are in '+link('phaseA_implementation.json')+'.','',
       'The new delta reverses byte-for-byte to the pre-implementation source, preserving the v2 block and metric helper. This branch already contained v2 additions relative to v1.0: those are separately preserved in '+link('preexisting_v1_tag_diff.patch')+'. The newly introduced diff contains the v3 additions/version switch only. '+link('source_additions_verification.json')+'; '+link('v3_implementation.diff')+'.','',
       '## Gate decisions','',table(gates,['gate','result']),
       '## G0: default/v1 and v2 regression','',
       'Canonical tolerance: 1e-10. The reference numbers and observed default-v1 outputs are:',table(canon,['metric','expected','observed','absolute_difference']),
       'Complete v1 output/runInfo equality against tag v1.0: '+str(g0['v1_tag_complete_structures_exact'])+'. Default versus explicit version=v1 equality: '+str(g0['default_explicit_v1_exact'])+'. Complete v2 output/runInfo equality against tag v2.0: '+str(g0['v2_tag_complete_structures_exact'])+'.','',
       table(pd.DataFrame(v2),['source','phase_frequency_hz','amplitude_frequency_hz','pac_strength','preferred_phase_deg','status_code']),
       'Tagged reference outputs and complete structures: '+link('G0.mat')+'; checks '+link('G0.json')+'; '+link('G0_v2_reproduction.csv')+'.','',
       '## G1: canonical v3','',g1text,'']
if not g1.empty:
    lines += [table(g1,['method','status','fP_hz','fA_hz','score','n_bursts','exponent','offset','peak_height','sigma','f_lo_hz']),
              'Saved complete canonical v3 result/diagnostics: '+link('G1.mat')+'. Welch, fit and residual curve: '+link('G1_curve.csv')+'. No diagnostic estimator rerun was needed.','']
lines+=['## G2: development cells','',
        'Prespecified design: beta={1,2}, T={2,6} s, fs=1000 Hz, unit-SD development-family 1/f^beta noise; 15-Hz sine amplitude 0.6; 110-Hz bursts with 10-ms Gaussian sigma and amplitude 1.5; Bernoulli 55% cycle retention and 5-ms Gaussian timing jitter; 20 paired v3/v1 repeats per cell, seed 20261031. Pass requires >=16/20 v3 fP estimates within 1 Hz of 15 Hz in every cell. Invalid outputs count as failures.','']
if cell.empty:lines+=['G2 was not run because an earlier gate failed. No G2 signal was generated.','']
else:lines += [table(cell,['beta','duration_s','repeats','v3_fp_recovery','v1_fp_recovery','v3_status_counts','v1_status_counts','passed']),
               'Only completed cells are shown; remaining cells were not run after the failed cell. Per-trial frequencies, status codes, aperiodic diagnostics and provenance: '+link('gate_trials.csv')+'. Input/complete output MATs are preserved under `gate_inputs/`; each v3 residual curve is saved alongside.','']
lines+=['## G3, freeze and later phases','',
        'G3 was not run after the required-gate failure. Its status-3 rate and fP distribution are therefore unavailable. No freeze commit or v3.0 tag was created or pushed. The HA held-out generator was not written, and neither HA nor regenerated HB signals were generated.','',
        'A1, A2 (v3 versus SP-raw), A3 and A4 were not evaluated. No adoption decision based on these criteria is available. Phase C rodent/ECoG analyses did not run. The HA and ECoG evaluation figures were not generated because their phases did not run. No empty result/figure placeholders are supplied.','',
        '## A2: v3 versus SP-raw (not evaluated)','',
        'The prespecified key secondary comparison is unavailable because G1 failed before the held-out phase. No claim about added information from burst timing is made.','',
        '## Runtime and deviations','',f'Phase-A gate timer: {result["elapsed_seconds"]:.3f} s, excluding MATLAB startup. Tagged reference and modified-source calls were each run once as specified; no completed gate was repeated and no method was tuned after an outcome.','']
for x in js('deviations.json')['deviations']:lines.append('- '+x['type']+': '+x['reason'])
lines += ['- Existing MATLAB startup warnings refer to missing historical Brainstorm paths; the gate driver explicitly verifies repository/reference source precedence.','',
          'Final verification: '+link('final_verification.json')+'. File inventory: '+link('output_manifest.json')+'.']
(O/'RESULTS_v3.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
verification=dict(**status,protocol_hash_unchanged=True,implementation_hashes_unchanged_since_gates=True,calc_MI_unchanged=True,default_v1_regression_passed=g0['v1_tag_complete_structures_exact'],v2_regression_passed=g0['v2_tag_complete_structures_exact'],new_diff_reverses_exact_baseline=True,current_git_worktree=g('status','--porcelain'))
(O/'final_verification.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
inventory=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(O.glob('*')) if p.is_file() and p.name!='output_manifest.json'];(O/'output_manifest.json').write_text(json.dumps(dict(git_head=m['git_head'],protocol_sha256=m['protocol_sha256'],files=inventory),indent=2),encoding='utf-8');print(json.dumps(status),flush=True)
