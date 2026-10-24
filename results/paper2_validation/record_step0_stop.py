from pathlib import Path
import subprocess, json, hashlib, datetime

root=Path(r'C:\Users\nghare\.brainstorm\process')
repo=root/'apc-brainstorm-publish'
out=Path(__file__).resolve().parent
git=r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe'
def run(*args): return subprocess.check_output([git,'-C',str(repo),*args])
def digest(data): return hashlib.sha256(data).hexdigest()
def write(name,value): (out/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
head=run('rev-parse','HEAD').decode().strip()
assert head==run('rev-parse','origin/paper2').decode().strip()
assert not run('status','--porcelain')
protocol='protocol/APC_paper2_validation_protocol.md'
blob=run('show',f'HEAD:{protocol}')
assert digest(blob)=='b33eae54cc93bbbfe3b806e4f785dc7de88501bd0366b3cea1343be33e8a0d94'
archive=repo/'results/paper2_ablation'
manifest=json.loads((archive/'archive_manifest.json').read_text(encoding='utf-8'))
for row in manifest['files']:
    data=(archive/row['file']).read_bytes()
    assert digest(data)==row['sha256']
    assert run('show',f"HEAD:results/paper2_ablation/{row['file']}")==data
prior=json.loads((root/'revision_checks/paper2_ablation/provenance.json').read_text(encoding='utf-8'))
files=[repo/'src/bst_apc.m',repo/'src/sp_raw_fp.m',repo/'src/apc_v3_spectral_peak.m',repo/'src/apc_event_carrier.m',repo/'src/calc_MI_all_methods.m',
       archive/'apc_fa_given_fp.m',archive/'scan_fa_given_fp.m',archive/'apc_fp_source.m',archive/'paper2_coupling_at_pair.m']
hashes={str(p):digest(p.read_bytes()) for p in files}
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
record=json.loads((out/'step0.json').read_text(encoding='utf-8'))
record.update(status='COMPLETE',pushed_commit=head,origin_paper2=head,clean_tree=True,
              archive_committed_blobs_verified=len(manifest['files']),
              git_process_check='No matching git processes returned by Get-Process',
              git_lock_files_found=0,git_lock_files_deleted=0,push_succeeded=True,utc_completed=utc)
write('step0.json',record)
provenance={'status':'STOPPED_PROTOCOL_AMBIGUITY_BEFORE_GATES','git_head':head,'branch':'paper2',
            'initial_head':record['initial_head'],'protocol_sha256':digest(blob),'protocol_public_on_origin':True,
            'archive_commit':head,'archive_files_verified':len(manifest['files']),'file_sha256':hashes,
            'new_signal_generated':False,'method_output_computed':False,'gates_started':False,
            'planned_seeds':{'V1':20261110,'V2':20261111,'V3':20261112,'V4':20261113,
                             'pair_bootstrap':20261114,'circular_shifts':20261115,'ecog_bootstrap':20261024},
            'environment_reference':str(root/'revision_checks/paper2_ablation/provenance.json'),
            'environment_reference_sha256':digest((root/'revision_checks/paper2_ablation/provenance.json').read_bytes()),
            'environment_note':'No MATLAB process was started for validation; prior environment is referenced, not remeasured.',
            'utc':utc}
write('provenance.json',provenance)
write('deviations.json',{'deviations':[],'note':'Stopped under the explicit ambiguity rule; no analysis settings were selected or changed.'})
text=f'''# STOPPED: A_EVENT input-status policy is ambiguous

Recorded {utc} before any validation gate, signal generation or method computation.

## Completed housekeeping

- Initial branch paper2, clean tree, HEAD {record['initial_head']}.
- Committed and working-tree validation protocol SHA-256: {digest(blob)}.
- Ablation archive committed and pushed successfully: {head}.
- All {len(manifest['files'])} copied source files match their manifest hashes and committed Git blobs.
- Current branch and origin/paper2 both point to the archive commit; working tree clean.
- No matching git processes or .git/*.lock files were found; nothing deleted.

## Exact ambiguity

Protocol section 2 requires A_EVENT to receive a copy of an APC output structure with only fP replaced, with "no other field changed". It defines two APC outputs, v1.0 and v3.0, and an independent F3 spectral source, but does not identify which APC output F3_A_EVENT must copy.

In unchanged src/apc_event_carrier.m, the function reads both status and fP from its input and returns immediately at `if status ~= 0 || ~isfinite(fp), return; end`. Replacing fP alone therefore does not make A_EVENT run after that base APC output failed. Copying v1.0 versus v3.0 can give different eligibility even when F3 supplies the same finite fP. This is a method-relevant choice, not a file or logging defect.

F1/F2 retaining a Step-2 estimate after later failure is explicit. Whether A_EVENT should nevertheless inherit end-to-end APC status, or should run whenever its fP source succeeds, is not explicit. The existing premise script's spectral-input structure uses status 0 and is not a copy of either APC end-to-end output; it does not resolve the new instruction.

## Clarification required before resuming

Specify whether A_EVENT eligibility follows the fP source's success or the copied APC end-to-end status. If it follows end-to-end status, specify which APC version's output F3_A_EVENT copies. The frozen apc_event_carrier.m itself will remain unchanged.

G-gen, G-event and G-abl are not run. V1-V4 are not generated. No primary, secondary, rodent or ECoG validation endpoint has been computed. No Step 2-6 output has been committed. No decision is available.
'''
(out/'STOPPED.md').write_text(text,encoding='utf-8')
(out/'RESULTS_validation.md').write_text('# Paper-2 validation: stopped before gates\n\n'+
    text.split('\n',1)[1],encoding='utf-8')
print(json.dumps({'status':provenance['status'],'pushed_commit':head,'archive_verified':len(manifest['files']),
                  'protocol_sha256':digest(blob),'new_signal_generated':False},indent=2))
