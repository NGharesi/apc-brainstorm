"""Preserve attempt 1 and implement only the public Amendment-1 wrapper edits."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,os,shutil,difflib,sys,zipfile,xml.etree.ElementTree as ET
O=Path(__file__).resolve().parent;R=O.parent.parent;repo=R/'apc-brainstorm-publish';sys.path.insert(0,str(R/'pydeps'))
import pandas as pd
git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def g(*a):return subprocess.check_output([str(git),'-C',str(repo),*a],text=True,encoding='utf-8').strip()
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()
assert g('branch','--show-current')=='neuroimage-submission' and g('status','--porcelain')==''
head=g('rev-parse','HEAD');assert head==g('rev-parse','origin/neuroimage-submission')=='c642a20b3081e2e36dfa148cc3da0b0747fca11e'
protocol=repo/'protocol/APC_ecog_miller_motor_protocol.md';assert sha(protocol)=='064d6651ccca2ad84954bbdea9cb2587d51bf8d4575ec7889d2fe32d5bd2dba4'
assert not list((O/'queue').glob('*.bat')) and not list((O/'running').glob('*.bat'))
assert 'runner v2 stopped' in (O/'logs/runner.log').read_text(encoding='utf-8')
A=O/'attempt1_minphase1';fresh=not A.exists();A.mkdir(exist_ok=True);(A/'logs').mkdir(exist_ok=True);(A/'scripts').mkdir(exist_ok=True)
shared=list((O/'prep').glob('*.mat'))+[O/n for n in ['bouts.csv','electrodes.csv','inventory.csv','bad_channels.csv','notch_filter_guards.csv','equivalence_gate.json','ecog_comparators.m','ecog_prepare.m']]
assert len(list((O/'prep').glob('*.mat')))==19
shared_hashes={str(p.relative_to(O)):sha(p) for p in shared}
if fresh:
    for name in ['provenance.json','ecog_worker.m']:shutil.copy2(O/name,A/'scripts'/name)
names=['STOPPED.md','STOP_METHOD']+[f'estimates_w{k}.csv' for k in range(1,5)]+[f'status_w{k}.json' for k in range(1,5)]+[f'logs/worker{k}_matlab.log' for k in range(1,5)]
moved=[]
for name in names:
    src=O/name;dst=A/name;assert src.resolve().is_relative_to(O.resolve()) and dst.resolve().is_relative_to(A.resolve())
    if fresh:
        assert src.is_file() and not dst.exists();h=sha(src);os.rename(src,dst);assert sha(dst)==h
    else:assert not src.exists() and dst.is_file();h=sha(dst)
    moved.append(dict(original_path=name,archived_path=str(dst.relative_to(O)),sha256=h,bytes=dst.stat().st_size))
# Remove the runner sentinel only after all requested attempt-1 outputs are preserved.
src=O/'STOP_RUNNER'
if fresh:
    h=sha(src);shutil.copy2(src,A/src.name);assert sha(A/src.name)==h;src.unlink()
else:assert not src.exists() and (A/'STOP_RUNNER').is_file();h=sha(A/'STOP_RUNNER')
moved.append(dict(original_path='STOP_RUNNER',archived_path=str((A/'STOP_RUNNER').relative_to(O)),sha256=h,bytes=0))
old=json.loads((A/'scripts/provenance.json').read_text(encoding='utf-8'))
methodpaths=[repo/'src/bst_apc.m',repo/'src/calc_MI_all_methods.m',R/'revision_checks/rodent_multi/v1_bout_features.m',R/'revision_checks/final/sos_comparators.m',R/'revision_checks/final/final_sos_filter.m']
m=dict(old);m.update(git_head=head,protocol_sha256=sha(protocol),git_clean=True,push=dict(status='SUCCEEDED',public_HEAD=head,before_resumed_signal_analysis=True),resumed_utc=datetime.now(timezone.utc).isoformat(),executor='Codex on this computer; four MATLAB workers',attempt1_executor='Claude through a job runner on this computer',attempt1_git_head=old['git_head'],attempt1_archive='attempt1_minphase1',status='AMENDMENT1_PREPARATION',seed=20261024,protected_source_sha256=[dict(path=str(p),sha256=sha(p)) for p in methodpaths],reused_unchanged_sha256=shared_hashes,apc_options_override=dict(fA=[80,150],minPhaseHz=6,maxPhaseHz=30),comparator_settings=dict(profile='ecog',phase_grid_hz=[6+i*.5 for i in range(49)],phase_half_width_hz=1.5,amplitude_grid_hz=list(range(80,149,4)),amplitude_half_width_hz=30,mode='ecog_A2_prime'))
src=(R/'revision_checks/rodent_multi/v1_bout_features.m').read_bytes();new=src
edits=[(b'function [row,info]=v1_bout_features(',b'function [row,info]=v1_bout_features_ecog('),(b"struct('fA',[80 150])",b"struct('fA',[80 150],'minPhaseHz',6,'maxPhaseHz',30)")]
for a,b in edits:assert new.count(a)==1;new=new.replace(a,b)
(O/'v1_bout_features_ecog.m').write_bytes(new)
reverse=new
for a,b in reversed(edits):reverse=reverse.replace(b,a)
assert reverse==src
(O/'v1_bout_features_ecog.diff').write_text(''.join(difflib.unified_diff(src.decode('utf-8').splitlines(True),new.decode('utf-8').splitlines(True),fromfile='original v1_bout_features.m',tofile='v1_bout_features_ecog.m')),encoding='utf-8')
worker=(A/'scripts/ecog_worker.m').read_bytes();updated=worker
wedits=[(b'[row,~]=v1_bout_features(seg,t);',b'[row,~]=v1_bout_features_ecog(seg,t);'),(b'abs(row.fP_hz-1)<=.05',b'abs(row.fP_hz-6)<=.05')]
for a,b in wedits:assert updated.count(a)==1;updated=updated.replace(a,b)
(O/'ecog_worker.m').write_bytes(updated);reverse=updated
for a,b in reversed(wedits):reverse=reverse.replace(b,a)
assert reverse==worker
(O/'ecog_worker_amendment1.diff').write_text(''.join(difflib.unified_diff(worker.decode('utf-8').splitlines(True),updated.decode('utf-8').splitlines(True),fromfile='attempt1 ecog_worker.m',tofile='Amendment1 ecog_worker.m')),encoding='utf-8')
# Reversible byte comparison confirms all other comparator profiles are unchanged.
original=(R/'revision_checks/final/sos_comparators.m').read_bytes();cmp=(O/'ecog_comparators.m').read_bytes();newline=b'\r\n' if b'\r\n' in cmp else b'\n';reversed_cmp=cmp.replace(b'function rows=ecog_comparators(',b'function rows=sos_comparators(').replace(b'elseif profile=="ecog",faGrid=80:4:148;fpStart=6;fpStop=30;'+newline,b'').replace(b'elseif mode=="ecog_A2_prime",half=30;',b'')
assert reversed_cmp==original
verification=dict(provenance_file='provenance.json',git_head=head,protocol_sha256=sha(protocol),wrapper_reverse_edits_exact_original=True,worker_only_two_specified_edits=True,comparator_other_profiles_byte_identical=True,wrapper_sha256=sha(O/'v1_bout_features_ecog.m'),worker_sha256=sha(O/'ecog_worker.m'))
(O/'amendment1_copy_verification.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
(O/'attempt1_archive_manifest.json').write_text(json.dumps(dict(git_head=head,protocol_sha256=sha(protocol),attempt1_executor=m['attempt1_executor'],moved_files=moved,reused_unchanged_sha256=shared_hashes),indent=2),encoding='utf-8')
B=pd.read_csv(O/'bouts.csv',encoding='utf-8');analysed=B[B.analysed.astype(bool)];assert len(analysed)==2648
m['planned_bouts']=len(analysed);m['progress_cache_plan']='Compute APC once on the first 10 analysed bp movement bouts, print progress counts/fP, then compute their four scans and seed estimates_w1.csv with all five rows per bout. The unchanged worker resumes and skips those complete keys. No bout is recomputed.'
(O/'provenance.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
doc=Path(r'D:\APC_project\RealDatasets\Miller_ECoG_library\motor_basic\README_motor_basic_dataset_notes.docx')
with zipfile.ZipFile(doc) as z:xml=ET.fromstring(z.read('word/document.xml'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};paragraphs=[''.join(p.itertext()) for p in []]
paragraphs=[''.join(p.itertext()) for p in xml.findall('.//w:p',ns)]
(O/'README_motor_basic_dataset_notes_extracted.txt').write_text('\n'.join(paragraphs),encoding='utf-8')
print(json.dumps(dict(public_HEAD=head,clean=True,protocol_hash=sha(protocol),archived_files=len(moved),reused_files=len(shared),analysed_bouts=len(analysed),wrapper_and_worker_diffs_verified=True)))
