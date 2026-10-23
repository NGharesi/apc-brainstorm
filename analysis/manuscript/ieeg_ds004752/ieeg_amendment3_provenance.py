from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,shutil
O=Path(__file__).resolve().parent;R=O.parent.parent;repo=R/'apc-brainstorm-publish';git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def g(*a):return subprocess.check_output([str(git),'-C',str(repo),*a],text=True,encoding='utf-8').strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert g('status','--porcelain')=='' and g('branch','--show-current')=='neuroimage-submission'
head=g('rev-parse','HEAD');assert head==g('rev-parse','origin/neuroimage-submission')=='37c21dbe249881fdc021655a855c000434b3ac54'
p=repo/'protocol/APC_ieeg_ds004752_protocol.md';digest=sha(p);assert digest=='087c51b1e5b930dca55e3c1ce63af15c891252399a3da1abc68407b27a2df308'
assert not (O/'provenance_before_amendment3.json').exists();shutil.copyfile(O/'provenance.json',O/'provenance_before_amendment3.json')
m=json.loads((O/'provenance.json').read_text(encoding='utf-8'))
for r in m['file_sha256_records']:
    f=Path(r['path'])
    if f!=p:assert sha(f)==r['sha256']
    r['sha256']=sha(f)
m.update(git_head=head,protocol_sha256=digest,status='FIXED_CONTACT_SELECTION_PENDING',stage='Amendment 3 public before candidate spectra',amendment3_public_utc=datetime.now(timezone.utc).isoformat())
m['push']['public_head']=head;m['contact_selection_order']='Dataset artifact removal; independent candidate/session robust masks; rank candidate retained-trial Welch ratios; selected mask is final; apply eligibility'
m['selection_numerical_details']=dict(welch_window='hann(2000), MATLAB symmetric default',welch_overlap_samples=1000,welch_nfft=2000,welch_fs_hz=2000,power_integral='trapz over inclusive 4-8 Hz and 1-4 Hz bins',trial_weights='equal retained trials pooled across sessions',amplitude_reject='any abs(x-session_median)>6*1.4826*MAD',difference_reject='any abs(within-trial diff)>6*1.4826*MAD(diff)',robust_pool='all maintenance samples of dataset-unflagged trials in the same candidate/session',sensitivity_a='same selected pair, dataset flags only',sensitivity_b='same selected pair and final bipolar mask, deeper-contact signal only',sensitivity_c='primary paired endpoint restricted to native-2000-Hz patients')
(O/'provenance.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
q=json.loads((O/'contact_order_clarification_pending.json').read_text(encoding='utf-8'));q.update(status='RESOLVED_BY_COMMITTED_AMENDMENT_3',answer='Mask each candidate independently, then rank',resolution_commit=head);(O/'contact_order_clarification_pending.json').write_text(json.dumps(q,indent=2),encoding='utf-8')
(O/'EXECUTION_amendment3.md').write_text('# Amendment 3 execution\n\nPublic commit '+head+'; protocol SHA-256 '+digest+'.\n\nThe common preprocessed arrays are reused unchanged from the Amendment-2 stage; only candidate masking/ranking is new. All original source/helper hashes were rechecked.\n\n'+json.dumps(m['selection_numerical_details'],indent=2)+'\n\nNo candidate spectrum or PAC output preceded this record. Sensitivities retain the primary selected pair; (a) changes only the trial mask to dataset flags, (b) changes only the signal to the deeper contact and uses the selected pair final mask.\n',encoding='utf-8')
print(json.dumps(dict(public_head=head,protocol_hash_matches=True,clean=True)))
