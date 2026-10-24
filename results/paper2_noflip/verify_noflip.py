from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,subprocess
O=Path(__file__).resolve().parent;R=O.parent.parent;repo=R/'apc-brainstorm-publish';sys.path.insert(0,str(R/'pydeps'))
import pandas as pd
import numpy as np
from PIL import Image
P=json.loads((O/'provenance.json').read_text(encoding='utf-8'))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
git=r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe'
g=lambda *a:subprocess.check_output([git,'-C',str(repo),*a])
assert g('rev-parse','HEAD').decode().strip()==g('rev-parse','origin/paper2').decode().strip()==P['git_head'] and not g('status','--porcelain')
assert hashlib.sha256(g('show','HEAD:protocol/APC_paper2_exploratory_noflip.md')).hexdigest()==P['protocol_sha256']
for p,h in P['file_sha256'].items():assert sha(Path(p))==h,p
for r in P['input_banks']:assert sha(Path(r['path']))==r['sha256']
assert sha(O/'noflip_worker.m')==P['worker_sha256'];assert sha(O/'noflip_analysis.py')==P['analysis_script_sha256']
d=pd.read_csv(O/'trial_estimates.csv',encoding='utf-8',float_precision='round_trip');old=pd.read_csv(R/'revision_checks/paper2_validation/simulation_trial_estimates.csv',encoding='utf-8',float_precision='round_trip')
assert len(d)==7500 and d.key.nunique()==1875 and not d.duplicated(['key','method','flip_troughs']).any();assert (d.classification=='exploratory').all()
for method,source in [('APC-v1.0','F1_A_APC'),('APC-v3.0','F2_A_APC')]:
 a=d[(d.method==method)&(d.flip_troughs==1)].set_index('key');b=old[old.method==method].set_index('key').reindex(a.index);c=old[old.method==source].set_index('key').reindex(a.index)
 for col,oldcol in [('endtoend_fp_hz','recovered_fp_hz'),('endtoend_fa_hz','recovered_fa_hz'),('status','status')]:assert np.array_equal(a[col].to_numpy(),b[oldcol].to_numpy(),equal_nan=True)
 assert np.array_equal(a.source_fp_hz.to_numpy(),c.source_fp_hz.to_numpy(),equal_nan=True)
assert (d.fraction_epochs_flipped=='not available').all()
for r in d.itertuples():assert json.loads(r.options_json)['flipTroughs']==bool(r.flip_troughs)
with Image.open(O/'exploratory_noflip.png') as im:
 assert all(abs(x-300)<.1 for x in im.info['dpi']);assert P['git_head'] in im.info['Description'];assert json.loads(im.info['Description'])['source_sha256']==sha(O/'summary.csv');dimensions=im.size
assert P['git_head'] in (O/'exploratory_noflip.svg').read_text(encoding='utf-8')
assert json.loads((O/'visual_qa.json').read_text(encoding='utf-8'))['status']=='PASS'
result={'status':'PASS','classification':'exploratory','utc':datetime.now(timezone.utc).isoformat(),'git_commit':P['git_head'],'protocol_sha256':P['protocol_sha256'],'clean_git_tree':True,'saved_inputs_unchanged':True,'src_unchanged':True,'saved_flip_true_estimates_exactly_reused':True,'inputs':1875,'rows':7500,'figure_dimensions':dimensions,'results_committed':False}
(O/'final_verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');P.update(status='COMPLETE',completed_utc=result['utc'],results_committed=False,verification=result);(O/'provenance.json').write_text(json.dumps(P,indent=2)+'\n',encoding='utf-8')
manifest=[{'path':str(p.relative_to(O)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(O.rglob('*')) if p.is_file() and p.name!='output_manifest.json'];(O/'output_manifest.json').write_text(json.dumps({'classification':'exploratory','git_commit':P['git_head'],'files':manifest},indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
