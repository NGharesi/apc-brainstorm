from pathlib import Path
import json,hashlib,shutil,datetime,difflib
O=Path(__file__).resolve().parent;D=O/'tooling_generation_attempt1';D.mkdir(exist_ok=False)
paths=['generation_matlab.log','validation_hb_cases.m','validation_generate.m','configuration.json']
manifest=[]
for name in paths:
    p=O/name;shutil.copyfile(p,D/name);manifest.append({'file':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
before=(O/'validation_hb_cases.m').read_text(encoding='utf-8')
after=before.replace('verification_row(n,meta)','verification_row(n,meta,seed)').replace('function r=verification_row(c,meta)','function r=verification_row(c,meta,seed)')
assert before!=after
(O/'validation_hb_cases.m').write_text(after,encoding='utf-8')
(D/'fix.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='before',tofile='after')),encoding='utf-8')
record={'code':'GEN_METADATA_SEED_SCOPE','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'reason':'Seed was parameterized in a local metadata function but omitted from its formal/call arguments.',
        'fix':'Pass unchanged seed to verification_row; preserve and compare the already-written configuration on resume.',
        'identified_without_outcomes':True,'method_outputs_computed':False,'completed_suite_banks':0,'preserved':manifest}
d=json.loads((O/'deviations.json').read_text(encoding='utf-8'));d['deviations'].append(record)
(O/'deviations.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
(D/'record.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,indent=2))
