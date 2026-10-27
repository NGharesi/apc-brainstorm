from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,subprocess
O=Path(__file__).resolve().parent;R=O.parent.parent;repo=R/'apc-brainstorm-publish';sys.path.insert(0,str(R/'pydeps'))
import numpy as np
import pandas as pd
from PIL import Image
P=json.loads((O/'provenance.json').read_text(encoding='utf-8'))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
git=r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe';g=lambda *a:subprocess.check_output([git,'-C',str(repo),*a])
assert not (O/'STOPPED.md').exists() and not list(O.glob('worker*_error.json'))
assert g('rev-parse','HEAD').decode().strip()==g('rev-parse','origin/paper2').decode().strip()==P['git_head'] and not g('status','--porcelain')
assert hashlib.sha256(g('show','HEAD:protocol/APC_paper2_noflip_confirmation_protocol.md')).hexdigest()==P['protocol_sha256']
for p,h in P['file_sha256'].items():assert sha(Path(p))==h,p
for r in P['input_banks']:assert sha(Path(r['path']))==r['sha256']
expected=P['implementation_sha256'].copy();expected.update(P.get('implementation_sha256_after_tooling',{}))
for p,h in expected.items():assert sha(O/p)==h,p
G=json.loads((O/'generator_check.json').read_text(encoding='utf-8'));assert G['status']=='PASS' and len(G['checks'])==7
for r in G['checks']:assert r['signal_equal'] and r['time_equal'] and r['sha256']==r['saved_sha256']
read=lambda n:pd.read_csv(O/n,encoding='utf-8',float_precision='round_trip')
d=read('trial_estimates.csv');truth=read('truths.csv');assert len(d)==6650 and d.key.nunique()==950 and not d.duplicated(['key','method']).any();assert truth.key.is_unique and len(truth)==950 and set(d.key)==set(truth.key)
assert (d.classification=='confirmatory').all() and (d.git_commit==P['git_head']).all();assert (d.groupby('key').size()==7).all()
fp1=d[d.method=='APC-v3.0-noflip'].set_index('key').source_fp_hz.sort_index();fp2=d[d.method=='F2nf_A_SCAN'].set_index('key').source_fp_hz.sort_index();assert np.array_equal(fp1.to_numpy(),fp2.to_numpy(),equal_nan=True)
pairs=d[d.method.str.startswith('APC-')].assign(version=lambda x:x.method.str.extract(r'(v[13]\.0)',expand=False));assert pairs.version.notna().all()
assert pairs.groupby(['key','version']).ngroups==1900
for (key,version),q in pairs.groupby(['key','version']):
 a=json.loads(q[q.flip_troughs==1].iloc[0].options_json);b=json.loads(q[q.flip_troughs==0].iloc[0].options_json);assert a['flipTroughs'] is True and b['flipTroughs'] is False;b['flipTroughs']=True;assert a==b
for r in d[d.method.isin(['F3_A_SCAN','F2nf_A_SCAN','A2_prime_2D'])].itertuples():
 cfg=P['validation_configuration']['V3' if r.suite=='W3' else 'V1'];settings=json.loads(r.options_json);assert settings['amplitude_grid_hz']==cfg['amplitude_grid_hz'] and settings['amplitude_half_width_hz']==cfg['amplitude_half_width_hz']
for n,rows in [('primary_C1_C2.csv',2),('secondary_tests.csv',13),('W3_counts.csv',49),('W1_counts.csv',14),('BTA_power.csv',8)]:assert len(read(n))==rows,n
assert (read('primary_C1_C2.csv').n==400).all()
for name in ['W3_counts.csv','W1_counts.csv']:
 c=read(name);assert (c.strict<=c.joint).all() and (c.joint<=c.fp).all()
guards=[]
for w in range(1,5):
 path=O/f'filter_guards_w{w}.csv';c=read(path.name);assert len(c)>0 and (c.max_pole_radius<1).all() and (c.max_sos_section_pole_radius<1).all() and (abs(c.center_gain-1)<1e-3).all() and c.guard_passed.astype(bool).all();guards.append({'file':path.name,'rows':len(c),'sha256':sha(path)})
with Image.open(O/'confirmation.png') as im:
 assert all(abs(x-300)<.1 for x in im.info['dpi']);meta=json.loads(im.info['Description']);assert meta['git_commit']==P['git_head'];dimensions=im.size
for r in meta['sources']:assert sha(Path(r['path']))==r['sha256']
assert P['git_head'] in (O/'confirmation.svg').read_text(encoding='utf-8');assert json.loads((O/'visual_qa.json').read_text(encoding='utf-8'))['status']=='PASS'
A=json.loads((O/'analysis_complete.json').read_text(encoding='utf-8'));assert A['status']=='COMPLETE' and A['decision'] in (O/'RESULTS_confirm.md').read_text(encoding='utf-8')
env=json.loads((O/'environment.json').read_text(encoding='utf-8'));assert set(d.matlab_version)=={env['matlab_version']}
result={'status':'PASS','classification':'confirmatory','utc':datetime.now(timezone.utc).isoformat(),'archive_and_push_hash':P['git_head'],'protocol_sha256':P['protocol_sha256'],'generator_checks':7,'inputs':950,'rows':6650,'src_unchanged':True,'input_banks_unchanged':True,'clean_git_tree':True,'f2nf_source_fp_matches_apc_v3_noflip':True,'paired_apc_options_differ_only_flip':True,'selected_comparator_grids_match_validation':True,'decision':A['decision'],'figure_dimensions':dimensions,'filter_guard_files':guards,'results_committed':False}
(O/'final_verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');P.update(status='COMPLETE',completed_utc=result['utc'],results_committed=False,environment=env,verification=result);(O/'provenance.json').write_text(json.dumps(P,indent=2)+'\n',encoding='utf-8')
paths=[p for p in sorted(O.rglob('*')) if p.is_file() and p.name!='output_manifest.json'];manifest=[{'path':str(p.relative_to(O)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in paths];(O/'output_manifest.json').write_text(json.dumps({'classification':'confirmatory','git_commit':P['git_head'],'protocol_sha256':P['protocol_sha256'],'files':manifest},indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
