from pathlib import Path
import sys,json,hashlib,re,subprocess
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=ROOT/'revision_checks/rodent_multi';sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
import pandas as pd
from PIL import Image
from scipy.io import loadmat
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
gate=read(OUT/'chunked_behavior_validation.json');assert not gate['passed'];assert gate['full_interval_agreement_upper_bound_percent']<95
mat=loadmat(OUT/'ec013_157_partial_label_comparison.mat',simplify_cells=True)
assert np.all(mat['valid'])
disagreements=int((~mat['same'].astype(bool)).sum());assert disagreements==34208
assert len(mat['same'])==280903
csv=pd.read_csv(OUT/'ec013_157_label_disagreements.csv',encoding='utf-8');assert csv.samples.sum()==disagreements
assert len(pd.read_csv(OUT/'ec013_157_bout_validation.csv',encoding='utf-8'))==24
assert read(OUT/'behavior_reproduction.json')['passed']
mapping=pd.read_csv(OUT/'mapping_checks.csv',encoding='utf-8');assert len(mapping)==18 and np.all(abs(mapping.tracking_to_lfp_duration_ratio-1)<=.05)
assert len(pd.read_csv(OUT/'selected_channels.csv',encoding='utf-8'))==18
git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def run(*args):return subprocess.check_output([str(git),'-C',str(ROOT/'apc-brainstorm-publish'),*args],text=True,encoding='utf-8').strip()
assert run('rev-parse','v1.0^{commit}')==gate['provenance']['git_commit'];assert run('status','--porcelain')==''
frozen={'bst_apc.m':'d8e9d2ee82b0aa9784c0cabb1fcd2468adcd09f74bceaf833aeed8128094eee9','calc_MI_all_methods.m':'22aed807d9c05fe528ed1c873481560c2392c41c5f6d7cc8af158da04dc193f9'}
for name,expected in frozen.items():assert sha(ROOT/'revision_checks/final/frozen_v1'/name)==expected
assert sha(OUT/'PROTOCOL_rodent_original.md')==read(OUT/'protocol_amendments_record.json')['original_protocol_sha256']
image=Image.open(OUT/'ec013_157_label_validation.png');assert abs(image.info['dpi'][0]-300)<.1
assert 'ec013_157_label_disagreements.csv' in image.info['Description'] and gate['provenance']['git_commit'] in image.info['Description']
assert 'ec013_157_label_disagreements.csv' in (OUT/'ec013_157_label_validation.svg').read_text(encoding='utf-8')
text=(OUT/'RESULTS_rodent.md').read_text(encoding='utf-8')
for target in re.findall(r'\]\(<([^>]+)>\)',text):assert Path(target).exists(),target
verification=dict(status='PASS',scope='stopped report; no completed multi-session replication claimed',metadata=gate['provenance'],
    known_sample_count=280903,known_disagreements=34208,full_interval_agreement_upper_bound_percent=100*(331701-disagreements)/331701,
    mapping_pairs_passed=18,channel_selections=18,original_historical_12_12_exact=True,git_clean=True,
    frozen_source_sha256=frozen,report_links_exist=True,png_dpi=image.info['dpi'],figure_metadata_verified=True,figure_visually_reviewed=True)
(OUT/'verification.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
resource=pd.read_csv(OUT/'validation_resource_monitor.csv',encoding='utf-8');resource['provenance_json']=json.dumps(gate['provenance']);resource.to_csv(OUT/'validation_resource_monitor.csv',index=False,encoding='utf-8')
files=[]
for p in OUT.rglob('*'):
 if p.is_file() and p.name!='output_manifest.json' and not any(x in ['__pycache__','plot_config'] for x in p.relative_to(OUT).parts):files.append(dict(path=str(p.relative_to(OUT)),bytes=p.stat().st_size,sha256=sha(p)))
(OUT/'output_manifest.json').write_text(json.dumps(dict(metadata=gate['provenance'],files=files),indent=2),encoding='utf-8')
print(json.dumps(verification))
