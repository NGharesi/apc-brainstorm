from pathlib import Path
import sys,json,hashlib,re,subprocess,datetime
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=ROOT/'revision_checks/rodent_multi';sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
import pandas as pd
from PIL import Image
def js(n):return json.loads((OUT/n).read_text(encoding='utf-8'))
def read(n):return pd.read_csv(OUT/n,encoding='utf-8')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
meta=js('regional_analysis_provenance.json');assert js('STATUS.json')['status']=='COMPLETE_REGIONAL_PLAN'
assert sha(OUT/'PROTOCOL_rodent.md')==meta['protocol_sha256']
assert sha(OUT/'EXECUTION_rodent.md')==meta['execution_sha256']
assert js('regional_xml_grouping.json')['contiguous_eight_channel_blocks']
mapping=read('mapping_checks.csv');assert len(mapping)==18 and abs(mapping.tracking_to_lfp_duration_ratio-1).max()<=.05
channel=read('regional_channel_map.csv');selected=read('regional_session_eligibility.csv');behavior=read('regional_behavior_summary.csv');bout=read('regional_bouts.csv');est=read('regional_bout_estimates.csv')
assert len(channel)==882 and len(selected)==36 and len(behavior)==18
assert set(behavior[behavior.included].session)=={'ec013.156','ec013.157','ec013.375'}
assert not selected.auxiliary.any()
assert selected[selected.analysis=='CA1'].region.eq('CA1').all()
assert selected[selected.analysis=='EC'].region.str.startswith('EC').all()
assert selected[selected.analysis=='E1_sensitivity'].channel_index.eq(1).all()
assert selected[selected.analysis=='E1_sensitivity'].region.eq('EC3').all()
assert selected[selected.animal=='EC013'].mapping_evidence.eq('assumed contiguous, verified on ec012ec.269').all()
for _,r in selected.iterrows():
 if r.analysis=='E1_sensitivity':continue
 mask=channel.session.eq(r.session)&~channel.auxiliary
 mask &= channel.region.eq('CA1') if r.analysis=='CA1' else channel.region.str.startswith('EC')
 d=channel[mask].sort_values('channel_index');assert r.channel_index==d.loc[d.theta_delta_ratio.idxmax(),'channel_index']
for _,r in behavior.iterrows():
 s=np.load(OUT/(r.session+'_regional_tracking.npz'));valid=s['valid_after_interpolation'];run=s['run_mask'];rest=s['rest_mask'];linear=s['linear_position_cm'];speed=s['speed_cm_s']
 assert not np.any(run&rest) and not np.any((run|rest)&~valid)
 assert np.all(speed[run]>6) and np.all(speed[rest]<6)
 assert np.all((linear[run]>=37.5-1e-9)&(linear[run]<=212.5+1e-9))
 assert np.all((linear[rest]<37.5+1e-9)|(linear[rest]>212.5-1e-9))
 assert np.allclose(np.quantile(linear[valid],[.005,.995]),[0,250],atol=1e-8)
 for state in ['run','rest']:
  rows=bout[(bout.session==r.session)&(bout.state==state)];assert len(rows)==r[state+'_bouts']
  for _,b in rows.iterrows():
   a=int(b.tracking_start_idx)-1;e=int(b.tracking_stop_idx);assert s[state+'_mask'][a:e].all() and b.duration_s>=5
   assert np.isclose(b.duration_s,(e-a)/39.0625) and b.lfp_start_idx<=b.lfp_stop_idx
assert len(est)==1680
assert set(est.analysis)=={'CA1','EC','E1_sensitivity'}
assert not est.duplicated(['analysis','session','state','bout','method']).any()
assert est.groupby(['analysis','session','state','bout']).size().eq(5).all()
apc=est[est.method=='APC-v1.0'];assert len(apc)==336
success=apc[apc.status==0];assert np.isclose(success.effective_half_width_hz,success.fP_hz,rtol=0,atol=1e-12).all()
for text in est.provenance_json:
 p=json.loads(text);o=p['apc_options'];assert p['git_commit']==meta['git_commit'] and p['seed']==20261022
 assert o['fA']==[80,150] and o['stepFourMode']=='v1' and o['fPRefine'] and not o['useSurrogates']
 assert p['comparators']['phase_grid']==list(np.arange(4,12.01,.5)) and p['comparators']['amplitude_grid']==list(range(80,149,4)) and p['comparators']['amplitude_half_width']==12
comparators=est[est.method!='APC-v1.0'];assert comparators.status.eq(0).all()
assert np.allclose(comparators[comparators.method=='MVL-Ozkurt'].score,comparators[comparators.method=='MVL-Ozkurt'].ozkurt_mvl)
assert np.allclose(comparators[comparators.method=='MVL-raw'].score,comparators[comparators.method=='MVL-raw'].raw_mvl)
guard=read('regional_comparator_filter_guards.csv');assert (guard.max_pole_radius<1).all() and (guard.max_sos_section_pole_radius<1).all() and (abs(guard.center_gain-1)<1e-3).all()
session=read('regional_session_statistics.csv');assert len(session)==135 and session.bootstrap_valid_resamples.eq(10000).all()
across=read('regional_across_session_statistics.csv');assert across[across.animal_pool=='EC012'].n_sessions.eq(0).all()
for _,r in session.iterrows():
 d=est[(est.analysis==r.analysis)&(est.session==r.session)&(est.method==r.method)]
 means={state:d.loc[d.state==state,r.outcome].dropna().mean() for state in ['run','rest']}
 assert np.isclose(r.mean_difference,means['run']-means['rest'])
models=js('regional_mixed_models.json');assert len(models['models'])==6
for model in models['models']:
 assert model['sessions']==3 and model['constant_animal_term_omitted'] and model['formula']=='outcome ~ state_run + (1 + state_run | session)'
 assert not model['optimizer_nonconvergence_warning']
figures=js('regional_figures.json')['figures'];assert len(figures)==10
for f in figures:
 im=Image.open(f['png']);assert abs(im.info['dpi'][0]-300)<.1
 description=json.loads(im.info['Description']);assert description['git_commit']==meta['git_commit']
 for name,digest in description['sources'].items():assert sha(OUT/name)==digest
 svg=Path(f['svg']).read_text(encoding='utf-8');assert meta['git_commit'] in svg and all(s in svg for s in f['sources'])
report=(OUT/'RESULTS_rodent.md').read_text(encoding='utf-8')
for target in re.findall(r'\]\(<([^>]+)>\)',report):assert Path(target).exists(),target
git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def run(*args):return subprocess.check_output([str(git),'-C',str(ROOT/'apc-brainstorm-publish'),*args],text=True,encoding='utf-8').strip()
assert run('rev-parse','v1.0^{commit}')==meta['git_commit'] and run('status','--porcelain')==''
expected={'bst_apc.m':'d8e9d2ee82b0aa9784c0cabb1fcd2468adcd09f74bceaf833aeed8128094eee9','calc_MI_all_methods.m':'22aed807d9c05fe528ed1c873481560c2392c41c5f6d7cc8af158da04dc193f9'}
for name,digest in expected.items():assert sha(ROOT/'revision_checks/final/frozen_v1'/name)==digest
assert datetime.datetime.fromisoformat(meta['recorded_utc']).timestamp()<=min(p.stat().st_mtime for p in OUT.glob('*_regional_tracking.npz'))
verification=dict(status='PASS',metadata=meta,mapping_pairs=18,channel_map_rows=882,regional_channel_selections=36,included_sessions=behavior[behavior.included].session.tolist(),
 unique_inputs=336,method_rows=1680,successful_APC_rows=int((apc.status==0).sum()),APC_status_counts={str(k):int(v) for k,v in apc.status.value_counts().items()},
 filter_guards=len(guard),bootstrap_checks_passed=True,mixed_models=6,mixed_optimizer_nonconvergence_warnings=0,figure_pairs_verified=10,visual_QA='all ten plots reviewed in contact sheet; channel-selection labels/legend revised and full-resolution chart checked',
 source_tag_and_hashes_verified=True,git_clean=True,report_links_valid=True,protocol_recorded_before_tracking_analysis=True)
(OUT/'regional_verification.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
(OUT/'RESUME_STATUS.json').write_text(json.dumps(dict(status='COMPLETE_REGIONAL_PLAN',metadata=meta,next='Requested regional replication complete; historical chunked plan superseded; no active analysis jobs or pending steps.'),indent=2),encoding='utf-8')
manifest=[]
for p in OUT.rglob('*'):
 if p.is_file() and p.name!='output_manifest.json' and not any(x in ['__pycache__','plot_config'] for x in p.relative_to(OUT).parts):manifest.append(dict(path=str(p.relative_to(OUT)),bytes=p.stat().st_size,sha256=sha(p)))
(OUT/'output_manifest.json').write_text(json.dumps(dict(metadata=meta,files=manifest),indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in verification.items() if k!='metadata'}))
