"""Record public-protocol provenance and immutable pre-implementation references."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,sys
O=Path(__file__).resolve().parent;R=O.parent.parent;repo=R/'apc-brainstorm-publish';git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def raw(*a):return subprocess.check_output([str(git),'-C',str(repo),*a])
def g(*a):return raw(*a).decode('utf-8').strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert g('branch','--show-current')=='neuroimage-submission' and g('status','--porcelain')==''
head=g('rev-parse','HEAD');assert head==g('rev-parse','origin/neuroimage-submission')=='8cabe20538b55f5185a20630f19fd7162b9bb269'
protocol=repo/'protocol/APC_v3_aperiodic_protocol.md';digest=sha(protocol);assert digest=='c2d8ede3fb994d6ef90f9757abbd993ed33e8e0a082288cb7501458d64a1bbb7'
assert not (O/'provenance.json').exists();snap=O/'source_before_v3';snap.mkdir()
for n in ['bst_apc.m','calc_MI_all_methods.m']:(snap/n).write_bytes((repo/'src'/n).read_bytes())
tags={}
for tag in ['v1.0','v2.0']:
    dest=O/('reference_'+tag.replace('.','_'));dest.mkdir();tags[tag]=g('rev-list','-n','1',tag)
    for n in ['bst_apc.m','calc_MI_all_methods.m']:(dest/n).write_bytes(raw('show',tag+':src/'+n))
(O/'preexisting_v1_tag_diff.patch').write_bytes(raw('diff','v1.0','--','src/bst_apc.m'))
old=json.loads((R/'revision_checks/ecog_miller_motor/provenance.json').read_text(encoding='utf-8'))
m=dict(recorded_utc=datetime.now(timezone.utc).isoformat(),git_head=head,git_branch='neuroimage-submission',git_clean_before_implementation=True,protocol_sha256=digest,protocol_public_on_origin=True,protocol_path=str(protocol),matlab_version=old['matlab_version'],toolbox_versions=old['toolbox_versions'],version_metadata_source='Latest same-computer MATLAB run; independently confirmed in record_environment.m before implementation',protected_baseline_sha256={n:sha(repo/'src'/n) for n in ['bst_apc.m','calc_MI_all_methods.m']},reference_tags=tags,phase_A_seed=20261031,HA_seed=20261101,HB_seed=20261022,status='STEP0_BEFORE_IMPLEMENTATION',heldout_generated=False,v3_tag_created=False)
(O/'provenance.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
(O/'deviations.json').write_text(json.dumps(dict(deviations=[]),indent=2),encoding='utf-8')
print(json.dumps(dict(HEAD=head,protocol_sha256=digest,clean=True,public=True,reference_tags=tags)))
