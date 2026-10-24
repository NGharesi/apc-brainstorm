from pathlib import Path
from datetime import datetime,timezone
import sys,subprocess,json,hashlib,re
O=Path(__file__).resolve().parent;R=O.parent.parent;repo=R/'apc-brainstorm-publish';sys.path.insert(0,str(R/'pydeps'))
import numpy as np
import pandas as pd
from PIL import Image
P=json.loads((O/'provenance.json').read_text(encoding='utf-8'))
git=r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe'
def g(*a):return subprocess.check_output([git,'-C',str(repo),*a])
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
 return h.hexdigest()
def read(name):return pd.read_csv(O/name,encoding='utf-8',float_precision='round_trip')
def main():
 assert not (O/'STOP_RUN.md').exists()
 assert g('rev-parse','HEAD').decode().strip()==P['git_head']
 assert g('rev-parse','origin/paper2').decode().strip()==P['git_head']
 assert g('branch','--show-current').decode().strip()=='paper2' and not g('status','--porcelain')
 assert hashlib.sha256(g('show','HEAD:protocol/APC_paper2_validation_protocol.md')).hexdigest()==P['protocol_sha256']
 assert sha(O/'STOPPED.md')==P['previous_stop_preserved_sha256']
 for name,value in P['ecog_precision_resolution']['preserved_stop_sha256'].items():assert sha(O/name)==value
 audit=read('ecog_reproduction_check.csv');assert len(audit)==2642 and audit.key.is_unique and audit.passed.astype(bool).all()
 for row in json.loads((O/'protected_completed_checkpoint_manifest.json').read_text(encoding='utf-8'))['files']:assert sha(O/row['path'])==row['sha256'],row['path']
 for row in json.loads((O/'tooling_statistics_collation_attempt1/computed_statistics_manifest.json').read_text(encoding='utf-8')):assert sha(O/row['path'])==row['sha256'],row['path']
 for path,value in P['file_sha256'].items():assert sha(Path(path))==value,path
 for row in P['input_banks']:assert sha(Path(row['path']))==row['sha256']
 for row in P['real_inputs']['source_files']:assert sha(Path(row['path']))==row['sha256'],row['path']
 expected={row['path']:row['sha256'] for row in P['implementation_files_after_diagnostic_fix']}
 expected[str(O/'validation_real_worker.m')]=P['ecog_precision_resolution']['worker_sha256_after']
 for path,value in expected.items():assert sha(Path(path))==value,path
 for name in ['bst_apc.m','calc_MI_all_methods.m','sp_raw_fp.m','apc_v3_spectral_peak.m']:
  assert g('show','v3.0:src/'+name)==(repo/'src'/name).read_bytes(),name
 assert json.loads((O/'all_gate_results.json').read_text(encoding='utf-8'))['status']=='PASS'
 assert json.loads((O/'adapter_verification.json').read_text(encoding='utf-8'))['status']=='PASS'
 assert json.loads((O/'statistics_complete.json').read_text(encoding='utf-8'))['status']=='COMPLETE'
 sim=read('simulation_trial_estimates.csv');truth=read('simulation_truths.csv');rodent=read('rodent_bout_estimates.csv');ecog=read('ecog_bout_estimates.csv');cal=read('calibrated_trial_tests.csv')
 assert len(sim)==22500 and sim.key.nunique()==1875 and not sim.duplicated(['key','method']).any()
 assert len(truth)==1875 and truth.key.is_unique and set(truth.key)==set(sim.key)
 assert len(rodent)==15928 and len(ecog)==13210 and ecog.key.nunique()==2642 and len(cal)==1875
 for endpoint,n in [('P_A.csv',4),('P_B.csv',4),('P_C.csv',2)]:assert len(read(endpoint))==n
 for suite,n in [('V1',175),('V2',450),('V3',500),('V4',25)]:assert (read('recovery_overall.csv').query('suite == @suite').n==n).all()
 assert set(read('P_C.csv').n)=={400}
 for frame in [sim,rodent,ecog,cal]:
  assert (frame.git_commit==P['git_head']).all() and (frame.protocol_sha256==P['protocol_sha256']).all()
 assert read('calibrated_specificity.csv').n.sum()==1875
 assert len(read('coupling_auc.csv'))==24
 guards=[]
 for pattern in ['simulation_filter_guards_w*.csv','real_filter_guards_w*.csv']:
  for path in O.glob(pattern):
   d=pd.read_csv(path,encoding='utf-8');assert (d.git_commit==P['git_head']).all();guards.append({'file':path.name,'rows':len(d),'columns':list(d.columns)})
 assert len(guards)==8
 figures=json.loads((O/'figure_provenance.json').read_text(encoding='utf-8'));assert len(figures)==4;qa=[]
 for f in figures:
  for row in f['provenance']['sources']:assert sha(Path(row['path']))==row['sha256']
  assert f['provenance']['git_commit']==P['git_head']
  with Image.open(f['png']) as image:
   dpi=image.info.get('dpi');assert dpi and all(abs(v-300)<.1 for v in dpi);assert P['git_head'] in image.info.get('Description','');size=image.size
  svg=Path(f['svg']).read_text(encoding='utf-8');assert P['git_head'] in svg;assert '<svg' in svg
  # Matplotlib encodes axes titles as title_* groups; these figures use labels only.
  assert not re.search(r'id="title_\d+"',svg)
  qa.append(dict(name=f['name'],dimensions_px=size,dpi=dpi,png_sha256=sha(Path(f['png'])),svg_sha256=sha(Path(f['svg']))))
 report=(O/'RESULTS_validation.md').read_text(encoding='utf-8');assert P['git_head'] in report and P['protocol_sha256'] in report and 'POST HOC' in report
 decisions=read('primary_decisions.csv')
 for x in decisions.decision:assert x in report
 result=dict(status='PASS',verified_utc=datetime.now(timezone.utc).isoformat(),pushed_commit=P['git_head'],clean_git_tree=True,tagged_source_unchanged=True,input_hashes_unchanged=True,initial_stopped_record_preserved=True,simulation_inputs=1875,simulation_rows=len(sim),rodent_rows=len(rodent),ecog_bouts=2642,figures=qa,guard_files=guards)
 (O/'final_verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 P.update(status='COMPLETE',validation_complete=True,final_verified_utc=result['verified_utc'],results_committed=False,method_output_computed=True,figure_files=qa)
 (O/'provenance.json').write_text(json.dumps(P,indent=2)+'\n',encoding='utf-8')
 paths=[p for p in O.rglob('*') if p.is_file() and not any(x.startswith('V') and x.endswith('_source') for x in p.relative_to(O).parts) and p.name not in ['output_manifest.json','amend1_validation.md']]
 manifest=[dict(path=str(p.relative_to(O)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(paths)]
 (O/'output_manifest.json').write_text(json.dumps({'git_commit':P['git_head'],'protocol_sha256':P['protocol_sha256'],'files':manifest},indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in result.items() if k not in ['figures','guard_files']},indent=2))
if __name__=='__main__':main()
