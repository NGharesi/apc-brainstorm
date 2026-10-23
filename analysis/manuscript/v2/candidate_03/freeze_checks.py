from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent.parent;REPO=ROOT/'apc-brainstorm-publish';A=REPO/'analysis/v2_revision'
GIT=r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe'
def git(*a):return subprocess.check_output([GIT,'-C',str(REPO),*a],encoding='utf-8').strip()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
unit=load(OUT/'unit_attempt_01/unit_results.json');metadata=load(OUT/'headless_inspection.json')['metadata']
assert unit['status']=='UNIT_GATES_PASSED' and all(unit['gates'][x]=='PASS' for x in ['a','a2','b','c']) and unit['gates']['d']=='COMPLETE'
assert load(OUT/'comparator_preflight.json')['passed'] and not metadata['tpac']['available']
assert git('hash-object','src/bst_apc.m')==unit['metadata']['apc_source_blob']
assert sha(REPO/'src/bst_apc.m')==sha(OUT/'unit_attempt_01/source_snapshot/bst_apc.m')
assert git('hash-object','analysis/v2_revision/PROTOCOL_v2.md')==unit['metadata']['protocol_git_blob']
assert git('branch','--show-current')=='v2-revision'
assert not (OUT/'heldout_inputs.mat').exists()
mode=sys.argv[1]
if mode=='before':
    assert not git('tag','-l','v2.0')
    result={'passed':True,'unit_gates':unit['gates'],'heldout_data_absent':True,'source_blob':unit['metadata']['apc_source_blob'],
      'source_sha256':sha(REPO/'src/bst_apc.m'),'analysis_sha256':{str(p):sha(p) for p in sorted(A.iterdir()) if p.is_file()},'metadata':metadata}
    (OUT/'pre_freeze_verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
elif mode=='after':
    assert not git('status','--porcelain')
    commit=git('rev-parse','HEAD');assert git('rev-list','-n','1','v2.0')==commit
    assert git('rev-parse','v2.0:src/bst_apc.m')==unit['metadata']['apc_source_blob']
    metadata['git_commit']=commit;metadata['git_tag']='v2.0';metadata['seed']=20261022
    attestation={'passed':True,'frozen_commit':commit,'tag':'v2.0','freeze_utc':datetime.now(timezone.utc).isoformat(),
      'unit_tested_source_blob':unit['metadata']['apc_source_blob'],'unit_test_base_commit':unit['metadata']['git_commit'],
      'unit_gates':unit['gates'],'source_matches_unit_snapshot':True,'no_heldout_inputs_at_tag':True,'metadata':metadata}
    (OUT/'freeze_attestation.json').write_text(json.dumps(attestation,indent=2),encoding='utf-8')
    (OUT/'tooling_deviations.json').write_text(json.dumps({'deviations':[{'type':'Python module path','detail':'matplotlib absent from default primary-runtime path; existing workspace pydeps used. No data or method change.'}], 'metadata':metadata},indent=2),encoding='utf-8')
else:raise ValueError(mode)
print(json.dumps({'freeze_check':mode,'passed':True,'source_blob':unit['metadata']['apc_source_blob'],'commit':git('rev-parse','HEAD')}))
