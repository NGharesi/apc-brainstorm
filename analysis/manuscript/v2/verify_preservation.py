"""Read-only verification that earlier result files and the base tag survived."""
from pathlib import Path
import hashlib,json,subprocess
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
REPO=ROOT/'apc-brainstorm-publish'
GIT=r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def git(*args):return subprocess.check_output([GIT,'-C',str(REPO),*args],encoding='utf-8').strip()
unit=load(OUT/'unit_attempt_01/unit_results.json');metadata=unit['metadata'];checks=[]
assert git('rev-list','-n','1','v1.0')=='71ebc16aed32ca38be73a800738b975e5806b330'
assert git('rev-parse','HEAD^')==metadata['base_commit']
for r in load(ROOT/'revision_checks/v1_rerun/original_results_verification.json')['checks']:
    assert sha(r['path'])==r['sha256_before'],r['path']
    checks.append({'path':r['path'],'sha256':r['sha256_before'],'unchanged':True})
for path,digest in load(ROOT/'revision_checks/v1_followup/input_source_manifest.json')['input_files'].items():
    assert sha(path)==digest,path
    checks.append({'path':path,'sha256':digest,'unchanged':True})
for path,digest in load(ROOT/'revision_checks/v1_followup/output_manifest.json')['files'].items():
    assert sha(path)==digest,path
    checks.append({'path':path,'sha256':digest,'unchanged':True})
result={'passed':True,'base_tag_unchanged':True,'protected_file_checks':len(checks),'checks':checks,'metadata':metadata}
(OUT/'preservation_verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'preserved_files':len(checks),'base_tag_unchanged':True}))
