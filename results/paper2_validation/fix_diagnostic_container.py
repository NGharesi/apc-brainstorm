from pathlib import Path
import json,hashlib,shutil,datetime,difflib
O=Path(__file__).resolve().parent;D=O/'tooling_diagnostic_container_attempt1';D.mkdir(exist_ok=False)
assert not list((O/'checkpoints').glob('*.mat'))
saved=[]
for p in [O/'validation_estimate.m',*O.glob('worker*_error.json'),*O.glob('worker*_matlab.log')]:
 shutil.copyfile(p,D/p.name);saved.append(dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
before=(O/'validation_estimate.m').read_text(encoding='utf-8');after=before.replace('agreement=struct([]);','agreement=cell(1,2);').replace('agreement(k)=struct(', 'agreement{k}=struct(').replace("'agreement',agreement,","'agreement',{agreement},")
assert after!=before
(O/'validation_estimate.m').write_text(after,encoding='utf-8')
(D/'fix.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='before',tofile='after')),encoding='utf-8')
d=json.loads((O/'deviations.json').read_text(encoding='utf-8'));rec=dict(code='DIAGNOSTIC_STRUCT_CONTAINER',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reason='MATLAB rejected subscripted assignment while building the diagnostic agreement structure.',fix='Use a cell container for agreement metadata; no method computations, options or numeric criteria changed.',identified_without_inspecting_numeric_outcomes=True,completed_trial_checkpoints=0,preserved=saved)
d['deviations'].append(rec);(O/'deviations.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');(D/'record.json').write_text(json.dumps(rec,indent=2)+'\n',encoding='utf-8')
p=json.loads((O/'provenance.json').read_text(encoding='utf-8'));p['diagnostic_container_fix']=rec;p['implementation_files_after_diagnostic_fix']=[dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in sorted(O.glob('*.m'))];(O/'provenance.json').write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'fix':rec['code'],'checkpoints':0,'preserved_files':len(saved)}))
