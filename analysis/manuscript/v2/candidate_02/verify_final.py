from pathlib import Path
import csv,hashlib,json,subprocess
OUT=Path(__file__).resolve().parent
BASE=OUT.parent;ROOT=BASE.parent.parent;REPO=ROOT/'apc-brainstorm-publish'
GIT=r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe'
def git(*args):return subprocess.check_output([GIT,'-C',str(REPO),*args],encoding='utf-8').strip()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
original=git('show','7848af0:src/bst_apc.m')
current=(REPO/'src/bst_apc.m').read_text(encoding='utf-8')
def between(text,start,end):return text[text.index(start):text.index(end,text.index(start))].strip()
sections={
 'v1_calculations_unchanged':between(original,'    requestedVersion=','function [sApc,runInfo]=compute_matrix_apc_v2')==between(current,'    requestedVersion=','function [sApc,runInfo]=compute_matrix_apc_v2'),
 'step1_unchanged':between(original,'% Step 1 is exactly','% Step 2:')==between(current,'% Step 1 is exactly','% Candidate 2 Step 2:'),
 'step3_unchanged':between(original,'% Step 3 affects','% Step 4:')==between(current,'% Step 3 affects','% Step 4:'),
 'step4_unchanged':between(original,'% Step 4:','% Event coupling test:')==between(current,'% Step 4:','% Candidate 2 event test:'),
 'phase_filter_rule_unchanged':between(original,'function band=v2_phase_band','function value=v2_ppc')==between(current,'function band=v2_phase_band','function value=v2_ppc')}
assert all(sections.values()),sections
assert sha(REPO/'src/bst_apc.m')==sha(OUT/'unit_attempt_01/source_snapshot/bst_apc.m')
assert not git('diff','--','analysis/v2_revision/v2_unit_generator.m')
assert git('rev-parse','HEAD')=='7848af05ada722971769da856e970d0737820169'
assert git('rev-list','-n','1','v1.0')=='71ebc16aed32ca38be73a800738b975e5806b330'
assert not git('tag','-l','v2.0')
preservation=load(BASE/'preservation_verification.json');count=0
for entry in preservation['checks']:
    assert sha(entry['path'])==entry['sha256'],entry['path'];count+=1
result=load(OUT/'unit_attempt_01/unit_results.json');assert result['status']=='STOP_UNIT_GATE' and result['failed_gate']=='a'
with (OUT/'unit_attempt_01/unit_trials.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
assert len(rows)==1 and abs(float(rows[0]['recovered_fp_hz'])-8)<=.1 and float(rows[0]['recovered_fa_hz'])==115
assert all(v=='NOT_RUN' for k,v in result['gates'].items() if k!='a')
metadata=result['metadata'];metadata['normalized_apc_options']=json.loads(rows[0]['apc_options_json'])
checks={'passed':True,'unchanged_code_sections':sections,'unit_generator_unchanged':True,'tested_source_unchanged':True,
 'v1_tag_unchanged':True,'no_v2_tag':True,'prior_v1_files_verified':count,'heldout_generated':False,
 'candidate2_committed':False,'no_further_candidate':True,'metadata':metadata}
(OUT/'final_verification.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps({'unchanged_code_sections':sections,'prior_v1_files_verified':count,'stopped_at':'a'}))
