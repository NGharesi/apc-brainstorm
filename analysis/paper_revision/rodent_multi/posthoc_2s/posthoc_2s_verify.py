"""Verify separate POST HOC artifacts and byte preservation of prespecified results."""
from pathlib import Path
import sys,json,hashlib,re,subprocess,datetime
OUT=Path(__file__).resolve().parent;PARENT=OUT.parent;ROOT=PARENT.parent.parent;sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
import pandas as pd
from PIL import Image
META=json.loads((OUT/'posthoc_2s_provenance.json').read_text(encoding='utf-8'))
def js(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def read(name):return pd.read_csv(OUT/name,encoding='utf-8')
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()
assert js('posthoc_2s_STATUS.json')['status']=='COMPLETE'
preserved=js('posthoc_2s_prespecified_manifest.json')['files']
for name,record in preserved.items():assert sha(PARENT/name)==record['sha256'],f'Prespecified file changed: {name}'
assert sha(OUT/'PROTOCOL_posthoc_2s.md')==META['posthoc_protocol_sha256']
snapshot=(OUT/'posthoc_2s_prespecified_report_snapshot.md').read_bytes()
assert hashlib.sha256(snapshot).hexdigest()==META['prespecified_report_snapshot_sha256']
assert (PARENT/'RESULTS_rodent.md').read_bytes().startswith(snapshot)
b=read('posthoc_2s_behavior_summary.csv');selected=read('posthoc_2s_session_eligibility.csv');bounds=read('posthoc_2s_bouts.csv');est=read('posthoc_2s_bout_estimates.csv')
assert len(b)==18 and b.included.all() and len(selected)==36 and selected.included.all()
assert b.groupby('animal').session.count().to_dict()=={'EC012':9,'EC013':9}
assert (b.run_bouts>=5).all() and (b.rest_bouts>=5).all() and (bounds.duration_s>=2).all()
old_bounds=pd.read_csv(PARENT/'regional_bouts.csv',encoding='utf-8')
shared=old_bounds.merge(bounds,on=['session','state','lfp_start_idx','lfp_stop_idx'],validate='one_to_one',suffixes=('_5s','_posthoc_2s'));assert len(shared)==202
for _,r in bounds.iterrows():
    s=np.load(PARENT/(r.session+'_regional_tracking.npz'));a=int(r.tracking_start_idx)-1;e=int(r.tracking_stop_idx)
    assert s[r.state+'_mask'][a:e].all() and np.isclose(r.duration_s,(e-a)/39.0625)
    assert np.isclose(r.start_time_s,s['time'][a]) and np.isclose(r.stop_exclusive_s,s['time'][e-1]+1/39.0625)
    assert r.lfp_start_idx<=r.lfp_stop_idx
assert len(est)==18230 and not est.duplicated(['analysis','session','state','bout','method']).any()
assert est.groupby(['analysis','session','state','bout']).size().eq(5).all()
assert est.groupby('analysis').session.nunique().to_dict()=={'CA1':9,'E1_sensitivity':9,'EC':18}
assert est.analysis_type.str.contains('POST HOC').all() and est.post_hoc.all() and est.minimum_bout_s.eq(2).all()
apc=est[est.method=='APC-v1.0'];assert len(apc)==3646 and apc.status.isin([0,1,2,3,4,5]).all()
good=apc[apc.status==0];assert np.allclose(good.effective_half_width_hz,good.fP_hz,rtol=0,atol=1e-12)
assert est[est.method!='APC-v1.0'].status.eq(0).all()
for text in est.provenance_json:
    q=json.loads(text);o=q['apc_options'];assert q['post_hoc'] and q['minimum_bout_s']==2 and 'POST HOC' in q['analysis_type']
    assert q['git_commit']==META['git_commit'] and q['seed']==20261022
    assert o['fA']==[80,150] and o['stepFourMode']=='v1' and o['fPRefine'] and not o['useSurrogates']
    assert q['comparators']['phase_grid']==list(np.arange(4,12.01,.5)) and q['comparators']['amplitude_grid']==list(range(80,149,4)) and q['comparators']['amplitude_half_width']==12
exact=read('posthoc_2s_shared_5s_exact_comparison.csv');assert len(exact)==1680 and exact.all_numeric_outputs_exact.all()
guards=read('posthoc_2s_comparator_filter_guards.csv');assert (guards.max_pole_radius<1).all() and (guards.max_sos_section_pole_radius<1).all() and (abs(guards.center_gain-1)<1e-3).all()
stats=read('posthoc_2s_session_statistics.csv');assert len(stats)==540 and stats.bootstrap_valid_resamples.between(0,10000).all()
for _,r in stats.iterrows():
    d=est[(est.analysis==r.analysis)&(est.session==r.session)&(est.method==r.method)]
    means={st:d.loc[d.state==st,r.outcome].dropna().mean() for st in ['run','rest']};expected=means['run']-means['rest']
    assert np.isclose(r.mean_difference,expected,equal_nan=True)
models=js('posthoc_2s_mixed_models.json');assert models['status']=='COMPLETE' and len(models['models'])==6
for model in models['models']:
    if model['analysis']=='EC':assert not model['constant_animal_term_omitted'] and '+ animal +' in model['formula']
    else:assert model['constant_animal_term_omitted'] and 'animal' not in model['formula']
figures=js('posthoc_2s_figures.json')['figures'];assert len(figures)==15
for f in figures:
    assert f['post_hoc'] and 'POST HOC' in f['description']
    image=Image.open(f['png']);assert abs(image.info['dpi'][0]-300)<.1
    description=json.loads(image.info['Description']);assert description['post_hoc'] and description['git_commit']==META['git_commit']
    for path,digest in description['sources'].items():assert sha(Path(path))==digest
    svg=Path(f['svg']).read_text(encoding='utf-8');assert 'POST HOC' in svg and META['git_commit'] in svg
for path in [OUT/'RESULTS_posthoc_2s.md',PARENT/'RESULTS_rodent.md']:
    for target in re.findall(r'\]\(<([^>]+)>\)',path.read_text(encoding='utf-8')):
        if Path(target) not in [OUT/'posthoc_2s_verification.json',OUT/'posthoc_2s_output_manifest.json']:assert Path(target).exists(),target
git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def run(*args):return subprocess.check_output([str(git),'-C',str(ROOT/'apc-brainstorm-publish'),*args],text=True,encoding='utf-8').strip()
assert run('rev-parse','v1.0^{commit}')==META['git_commit'] and run('status','--porcelain')==''
for name,digest in META['frozen_source_sha256'].items():assert sha(ROOT/'revision_checks/final/frozen_v1'/name)==digest
verification=dict(status='PASS',analysis_type=META['analysis_type'],post_hoc=True,metadata=META,prespecified_files_byte_unchanged=len(preserved),
    prespecified_report_byte_prefix_preserved=True,tracking_masks_unchanged=True,shared_prespecified_bouts_unchanged=202,shared_prespecified_method_rows_exact=1680,
    eligible_sessions=18,regional_sessions={'CA1':9,'EC':18,'E1_sensitivity':9},unique_inputs=3646,method_rows=18230,
    APC_status_counts={str(k):int(v) for k,v in apc.status.value_counts().items()},filter_guards=len(guards),session_statistics=540,mixed_models=6,
    mixed_optimizer_nonconvergence_warnings=sum(m['optimizer_nonconvergence_warning'] for m in models['models']),figure_pairs_verified=15,git_clean=True,
    posthoc_labels_verified=True,report_links_valid=True,visual_QA_file='posthoc_2s_visual_QA.json')
(OUT/'posthoc_2s_verification.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
(OUT/'posthoc_2s_RESUME_STATUS.json').write_text(json.dumps(dict(status='COMPLETE_POST_HOC_2S',analysis_type=META['analysis_type'],post_hoc=True,metadata=META,next='POST HOC 2-s sensitivity complete; no active workers or pending analysis steps.'),indent=2),encoding='utf-8')
parentmanifest=PARENT/'output_manifest.json';archive=OUT/'posthoc_2s_parent_manifest_before_append.json'
if not archive.exists():archive.write_bytes(parentmanifest.read_bytes())
files=[]
for p in OUT.rglob('*'):
    if p.is_file() and p.name!='posthoc_2s_output_manifest.json' and not any(x in ['__pycache__','plot_config'] for x in p.relative_to(OUT).parts):files.append(dict(path=str(p.relative_to(OUT)),bytes=p.stat().st_size,sha256=sha(p)))
(OUT/'posthoc_2s_output_manifest.json').write_text(json.dumps(dict(analysis_type=META['analysis_type'],post_hoc=True,metadata=META,files=files),indent=2),encoding='utf-8')
old=json.loads(archive.read_text(encoding='utf-8'));allfiles=[]
for p in PARENT.rglob('*'):
    if p.is_file() and p.name!='output_manifest.json' and not any(x in ['__pycache__','plot_config'] for x in p.relative_to(PARENT).parts):allfiles.append(dict(path=str(p.relative_to(PARENT)),bytes=p.stat().st_size,sha256=sha(p)))
parentmanifest.write_text(json.dumps(dict(metadata=old['metadata'],posthoc_2s_metadata=META,files=allfiles),indent=2),encoding='utf-8')
for path in [OUT/'RESULTS_posthoc_2s.md',PARENT/'RESULTS_rodent.md']:
    for target in re.findall(r'\]\(<([^>]+)>\)',path.read_text(encoding='utf-8')):assert Path(target).exists(),target
print(json.dumps({k:v for k,v in verification.items() if k!='metadata'}))
