"""Public amendment attestation; preserve attempt 1 and original source bytes."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,shutil,os
O=Path(__file__).resolve().parent;R=O.parent.parent;repo=R/'apc-brainstorm-publish';git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def raw(*a):return subprocess.check_output([str(git),'-C',str(repo),*a])
def g(*a):return raw(*a).decode('utf-8').strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
head=g('rev-parse','HEAD');assert head==g('rev-parse','origin/neuroimage-submission')=='c6b669962369cc97e3ab2635e583b48386152472'
assert g('branch','--show-current')=='neuroimage-submission';protocol=repo/'protocol/APC_v3_aperiodic_protocol.md';digest=sha(protocol);assert digest=='fda66faf93fb29bb8d84bb8fab89a7a051b474165c22b195ef92e24aeb91a8e1'
A=O/'attempt1_residual_location';assert not A.exists();A.mkdir();(A/'source_snapshot').mkdir();(A/'scripts').mkdir()
old=json.loads((O/'provenance.json').read_text(encoding='utf-8'));original_status=g('status','--porcelain')
for name in ['apc_v3_spectral_peak.m','sp_raw_fp.m','bst_apc.m']:shutil.copy2(repo/'src'/name,A/'source_snapshot'/name)
(A/'source_snapshot/bst_apc_uncommitted.patch').write_bytes(raw('diff','--','src/bst_apc.m'))
for name in ['run_v3_gates.m','v3_development_generator.m']:shutil.copy2(repo/'analysis/v3_aperiodic'/name,A/'source_snapshot'/name)
for pattern in ['*.py','*.m']:
    for p in O.glob(pattern):shutil.copy2(p,A/'scripts'/p.name)
names=['STOPPED.md','gate_results.json','gate_summary.csv','gate_trials.csv','STATUS.json','v3_implementation.diff','provenance.json','phaseA_implementation.json','RESULTS_v3.md','final_verification.json','output_manifest.json','source_additions_verification.json','phaseA_source_snapshot']
sources={O/n for n in names if (O/n).exists()};sources.update(O.glob('G0*'));sources.update(O.glob('G1*'));sources.update(O.glob('phaseA*log'));sources.update(O.glob('phaseA*error*.json'))
records=[]
for src in sorted(sources):
    dest=A/src.name;assert src.resolve().is_relative_to(O.resolve()) and dest.resolve().is_relative_to(A.resolve()) and not dest.exists()
    files=sorted(src.rglob('*')) if src.is_dir() else [src]
    for p in files:
        if p.is_file():records.append(dict(original_path=str(p.relative_to(O)),archived_path=str((A/p.relative_to(O)).relative_to(O)),sha256=sha(p),bytes=p.stat().st_size))
    os.rename(src,dest)
assert all(sha(O/r['archived_path'])==r['sha256'] for r in records)
# Match the committed blob's newline sequence, with no source-text change.
p=repo/'src/bst_apc.m';before=p.read_bytes();committed=raw('show','HEAD:src/bst_apc.m');newline=b'\r\n' if b'\r\n' in committed else b'\n';after=before.replace(b'\r\n',b'\n').replace(b'\n',newline);assert after.replace(b'\r\n',b'\n')==before.replace(b'\r\n',b'\n');p.write_bytes(after)
stat=g('diff','--stat','v1.0','--','src/bst_apc.m');numstat=g('diff','--numstat','v1.0','--','src/bst_apc.m');assert int(numstat.split()[1])==0
(O/'bst_apc_line_endings_and_diff.json').write_text(json.dumps(dict(git_head=head,protocol_sha256=digest,committed_newline='CRLF' if newline==b'\r\n' else 'LF',original_CRLF=before.count(b'\r\n'),original_LF=before.count(b'\n'),restored_CRLF=after.count(b'\r\n'),restored_LF=after.count(b'\n'),source_text_unchanged=True,unqualified_git_diff_stat_v1_tag=stat,unqualified_git_diff_numstat_v1_tag=numstat),indent=2),encoding='utf-8')
m=old.copy();m.update(git_head=head,protocol_sha256=digest,status='AMENDMENT1_PREPARATION',amendment1_public_utc=datetime.now(timezone.utc).isoformat(),protocol_public_on_origin=True,git_clean_before_resume=False,git_worktree_before_resume=original_status,attempt1_archive=str(A),attempt=2,heldout_generated=False,v3_tag_created=False,source_committed=False,push=dict(status='SUCCEEDED',public_HEAD=head,before_amended_method_change=True))
for k in ['failed_gate','gate_results','phaseA_frozen_utc','implementation_sha256']:m.pop(k,None)
(O/'provenance.json').write_text(json.dumps(m,indent=2),encoding='utf-8');(O/'attempt1_archive_manifest.json').write_text(json.dumps(dict(git_head=head,protocol_sha256=digest,moved_files=records,source_snapshot_sha256={p.name:sha(p) for p in (A/'source_snapshot').iterdir() if p.is_file()}),indent=2),encoding='utf-8')
print(json.dumps(dict(public_HEAD=head,protocol_hash=digest,archived_files=len(records),committed_line_ending='CRLF' if newline==b'\r\n' else 'LF',unqualified_diff_stat=stat)))
