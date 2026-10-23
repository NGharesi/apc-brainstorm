"""Archive the failed maintenance run and register public Amendment 4."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,shutil,os,difflib
O=Path(__file__).resolve().parent;R=O.parent.parent;repo=R/'apc-brainstorm-publish';git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def g(*a):return subprocess.check_output([str(git),'-C',str(repo),*a],text=True,encoding='utf-8').strip()
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()
head=g('rev-parse','HEAD');assert head==g('rev-parse','origin/neuroimage-submission')=='f87ce24a8a7c5719023549d783db13da584d1423'
assert g('status','--porcelain')=='' and g('branch','--show-current')=='neuroimage-submission'
protocol=repo/'protocol/APC_ieeg_ds004752_protocol.md';digest=sha(protocol);assert digest=='95b741822ac085bb96a01f1a5396674b83ecfaa827c199708e95490ad9f70ad3'
old=json.loads((O/'provenance.json').read_text(encoding='utf-8'));old_status=json.loads((O/'STATUS.json').read_text(encoding='utf-8'));archive=O/'attempt1_maintenance_3s';assert not archive.exists();archive.mkdir()
for record in old['file_sha256_records']:
    p=Path(record['path'])
    if p!=protocol:assert sha(p)==record['sha256']
explicit=['STOPPED.md','ieeg_trial_estimates.csv','estimates','STATUS.json','RESULTS_ieeg.md','provenance.json','analysis_provenance.json','output_manifest.json','trial_exclusion_summary.csv','filter_guards.csv','filter_guard_logging_recovery.log','selected_session_spectra.mat','session_spectral_peaks.csv','METHOD_STOP_FLAG.json']
sources={O/p for p in explicit if (O/p).exists()}
for pattern in ['worker*_matlab.log','worker*_runtime.json','ieeg_worker*_trial_estimates.csv','partial_*.csv','method_*.json']:sources.update(O.glob(pattern))
records=[]
for p in sorted(sources):
    assert p.resolve().is_relative_to(O.resolve()) and p.parent.resolve()==O.resolve()
    dest=archive/p.name;assert dest.resolve().is_relative_to(archive.resolve()) and not dest.exists()
    files=sorted(p.rglob('*')) if p.is_dir() else [p]
    for f in files:
        if f.is_file():records.append(dict(original_path=str(f.relative_to(O)),archived_path=str((archive/f.relative_to(O)).relative_to(O)),bytes=f.stat().st_size,sha256=sha(f)))
    os.rename(p,dest)
# Preserve the exact old wrappers as well; original shared gates/masks stay put.
code=archive/'scripts';code.mkdir()
for p in O.glob('ieeg_*.m'):shutil.copy2(p,code/p.name)
for p in O.glob('ieeg_*.py'):
    if not p.name.startswith('ieeg_am4'):shutil.copy2(p,code/p.name)
for r in records:assert sha(O/r['archived_path'])==r['sha256']
kept=['contacts.csv','candidate_rankings.csv','candidate_trial_counts.csv','trial_inclusion.csv','session_eligibility.csv','patient_eligibility.csv','edf_file_checks_attempt2.csv','edf_channel_checks_attempt2.csv','timeline_gate_confirmation.json','timeline_grand_average.csv','timeline_grand_average.png','timeline_grand_average.svg']
kept_hashes={p:sha(O/p) for p in kept}
m=old.copy();m.update(attempt='Amendment 4; attempt 2 after maintenance failure',git_head=head,protocol_sha256=digest,status='AMENDMENT4_PREPARATION',stage='Public Amendment 4 before new-window analysis',amendment4_public_utc=datetime.now(timezone.utc).isoformat(),previous_maintenance_attempt=old_status,attempt1_maintenance_archive=str(archive),retained_shared_sha256=kept_hashes,window_s=[0,6],window_samples=12000,evoked_removal='Within each analysis/patient/session/signal, subtract the included-trial mean waveform after final window-specific rejection; no second rejection after subtraction')
for key in ['stopped_utc','frozen_utc','frozen_analysis_sha256','planned_analysis_counts','unique_inputs','total_method_rows','stop_record']:m.pop(key,None)
m['push']=dict(status='SUCCEEDED',public_head=head,before_new_window_signal_analysis=True)
m['file_sha256_records']=[dict(path=r['path'],sha256=sha(Path(r['path']))) for r in old['file_sha256_records']]
m['comparator_settings']['phase_grid_hz']=[1+i*.5 for i in range(23)]
m['sensitivity_rules_am4']=dict(primary='Amendment-3 selected bipolar mask intersected with selected bipolar 0-6 s robust mask',artifact_only='Dataset artifact flags only, no robust rejection at either window; fixed selected pair; own included-trial bipolar mean',referential='Amendment-3 selected-pair mask intersected with selected deeper-contact 0-6 s robust mask; own included-trial referential mean',native2000='Repeat primary endpoint on native-2000-Hz patients only')
(O/'provenance.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
(O/'am4_archive_manifest.json').write_text(json.dumps(dict(provenance=m,moved_files=records,retained_shared_sha256=kept_hashes),indent=2),encoding='utf-8')
(O/'STATUS.json').write_text(json.dumps(dict(status='AMENDMENT4_PREPARATION',provenance=m,method_outputs=0),indent=2),encoding='utf-8')
original=(R/'revision_checks/final/sos_comparators.m').read_bytes();updated=original;edits=[(b'function rows=sos_comparators(',b'function rows=ieeg_comparators('),(b'elseif profile=="rodent",faGrid=80:4:148;fpStart=4;fpStop=12;',b'elseif profile=="rodent",faGrid=80:4:148;fpStart=4;fpStop=12;\r\nelseif profile=="ieeg",faGrid=80:4:148;fpStart=1;fpStop=12;'),(b'mode=="A2"||mode=="rodent_A2_prime"',b'mode=="A2"||mode=="rodent_A2_prime"||mode=="ieeg_A2_prime"')]
for a,b in edits:assert updated.count(a)==1;updated=updated.replace(a,b)
reverse=updated
for a,b in reversed(edits):reverse=reverse.replace(b,a)
assert reverse==original
(O/'ieeg_comparators.m').write_bytes(updated)
(O/'am4_comparator_copy.diff').write_text(''.join(difflib.unified_diff(original.decode('utf-8').splitlines(True),updated.decode('utf-8').splitlines(True),fromfile='original sos_comparators.m',tofile='ieeg_comparators.m Amendment 4')),encoding='utf-8')
(O/'am4_comparator_copy_verification.json').write_text(json.dumps(dict(provenance=m,existing_profiles_byte_identical=True,reverse_edits_exact_original=True,original_sha256=hashlib.sha256(original).hexdigest(),copy_sha256=hashlib.sha256(updated).hexdigest(),edits=[dict(before=a.decode('utf-8'),after=b.decode('utf-8')) for a,b in edits]),indent=2),encoding='utf-8')
print(json.dumps(dict(public_head=head,clean=True,protocol_hash_matches=True,moved_files=len(records),retained_shared_files=len(kept_hashes),comparator_other_profiles_identical=True)))
