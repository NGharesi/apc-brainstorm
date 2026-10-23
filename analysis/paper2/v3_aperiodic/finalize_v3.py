"""Independent saved-output audit and checksums. No signal/method reruns."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,sys,math
O=Path(__file__).resolve().parent;R=O.parent.parent;repo=R/'apc-brainstorm-publish';sys.path.insert(0,str(R/'pydeps'))
import pandas as pd
import numpy as np
from PIL import Image
git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def raw(*a):return subprocess.check_output([str(git),'-C',str(repo),*a])
def g(*a):return raw(*a).decode('utf-8').strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(n):return json.loads((O/n).read_text(encoding='utf-8'))
m=js('phaseB_implementation.json');assert all((O/f'worker{w}_complete.json').exists() for w in range(1,5))
assert g('rev-parse','HEAD')==g('rev-parse','origin/neuroimage-submission')==g('rev-list','-n','1','v3.0')==m['freeze_commit']
assert not g('status','--porcelain');assert sha(repo/'protocol/APC_v3_aperiodic_protocol.md')==m['protocol_sha256']
for rec in js('freeze_precheck.json')['files']:
    assert sha(repo/rec['path'])==rec['sha256'];assert (repo/rec['path']).read_bytes()==raw('show','v3.0:'+rec['path'])
for group in [m['implementation_sha256'],m['evaluation_dependencies_sha256'],js('execution_sources.json')['files']]:
    for rec in group:assert sha(Path(rec['path']))==rec['sha256']
for rec in js('attempt1_archive_manifest.json')['moved_files']:assert sha(O/rec['archived_path'])==rec['sha256']
eq=pd.read_csv(O/'HB_v1_equivalence.csv',encoding='utf-8',float_precision='round_trip');assert len(eq)==675 and eq.exact.all() and eq.route_exact.all()
D=pd.read_csv(O/'heldout_trial_estimates.csv',encoding='utf-8',float_precision='round_trip')
assert len(D)==11025 and not D.duplicated(['suite','input_id','method']).any()
assert len(D[D.suite.eq('HA')&D.dataset.eq('coupled')])==450*7
assert len(D[D.suite.eq('HA')&D.dataset.eq('timing_null')])==450*7
assert len(D[D.suite.eq('HB')&D.dataset.eq('coupled')])==350*7
assert len(D[D.suite.eq('HB')&D.dataset.eq('timing_null')])==250*7
assert len(D[D.suite.eq('HB')&D.dataset.eq('no_coupled_burst')])==75*7
fp=D.status.eq(0)&D.recovered_fp_hz.notna()&((D.recovered_fp_hz-D.true_fp_hz).abs()<=1)
fa=D.status.eq(0)&D.recovered_fa_hz.notna()&((D.recovered_fa_hz-D.true_fa_hz).abs()<=8)
assert np.array_equal(fp,D.fp_correct);assert np.array_equal(fp&fa,D.joint_correct)
assert D[D.dataset.eq('timing_null')].pair_residual.max()<=1e-12
criteria=js('criteria_decisions.json')['criteria']
def exact_binomial(z):
    a=z['a_only'];b=z['b_only'];n=a+b
    if not n:return 1.
    if z['alternative']=='greater':return sum(math.comb(n,k) for k in range(a,n+1))/(2**n)
    return min(1.,2*sum(math.comb(n,k) for k in range(min(a,b)+1))/(2**n))
for z in [criteria['A1'],criteria['A2'],*criteria['A3'],criteria['A4']]:assert math.isclose(exact_binomial(z),z['p_value'],rel_tol=1e-12,abs_tol=1e-15)
assert criteria['A4']['passed']==(criteria['A4']['a_success']<=criteria['A4']['b_success']+35)
for z in criteria['A3']:assert z['passed']==(z['a_success']>=z['b_success']-z['allowed_loss'])
recommended=criteria['A1']['passed'] and all(z['passed'] for z in criteria['A3']) and criteria['A4']['passed']
assert recommended==js('STATUS.json')['recommended']
G=pd.read_csv(O/'filter_guards.csv',encoding='utf-8',float_precision='round_trip');assert G.guard_passed.all() and G.max_pole_radius.lt(1).all() and (G.center_gain-1).abs().lt(1e-3).all()
figures=[]
for name in ['HA_joint_recovery','HA_fp_recovery']:
    with Image.open(O/(name+'.png')) as im:
        assert abs(im.info['dpi'][0]-300)<.02 and abs(im.info['dpi'][1]-300)<.02
        description=im.info['Description'];assert m['freeze_commit'] in description and sha(O/'recovery_by_cell.csv') in description
        figures.append(dict(name=name,pixels=list(im.size),dpi=im.info['dpi'],metadata=description))
    assert m['freeze_commit'] in (O/(name+'.svg')).read_text(encoding='utf-8')
phaseC=None
if recommended:
    C=O/'phaseC';cm=js('phaseC/provenance.json');assert all((C/f'worker{w}_complete.json').exists() for w in range(1,5))
    for rec in cm['reused_files_sha256']:assert sha(Path(rec['path']))==rec['sha256']
    for rec in js('phaseC/execution_sources.json')['files']:assert sha(Path(rec['path']))==rec['sha256']
    V=pd.read_csv(C/'ecog_v3_estimates.csv',encoding='utf-8',float_precision='round_trip');RV=pd.read_csv(C/'rodent_v3_unique_estimates.csv',encoding='utf-8',float_precision='round_trip')
    assert len(V)==2648 and not V.duplicated(['patient','recording','bout']).any();assert len(RV)==3646 and RV.input_id.nunique()==3646
    assert len(list((C/'checkpoints').glob('ecog_*.mat')))==2648 and len(list((C/'checkpoints').glob('rodent_*.mat')))==3646
    rest=pd.read_csv(C/'ecog_rest_frequencies.csv',encoding='utf-8');success=js('phaseC/ecog_success_criterion.json');assert len(rest)==18 and int(rest.v3_within_2_hz.sum())==success['v3_success'] and success['passed']==(success['v3_success']>=9)
    assert js('STATUS.json')['phaseC_complete']
    assert np.array_equal((V.fP_hz-V.f_lo_hz).abs().le(.05),V.fp_at_flo)
    assert np.array_equal((RV.fP_hz-RV.f_lo_hz).abs().le(.05),RV.fp_at_flo)
    for folder,prefix in [('rodent5s','regional'),('POST_HOC_rodent2s','posthoc_2s')]:assert js(f'phaseC/{folder}/{prefix}_mixed_models.json')['status']=='COMPLETE'
    assert js('phaseC/ecog/mixed_model_runtime.json')['status']=='COMPLETE'
    with Image.open(O/'ECoG_rest_fp_spectral_peak.png') as im:
        assert abs(im.info['dpi'][0]-300)<.02 and m['freeze_commit'] in im.info['Description'] and sha(C/'ecog_rest_frequencies.csv') in im.info['Description']
        figures.append(dict(name='ECoG_rest_fp_spectral_peak',pixels=list(im.size),dpi=im.info['dpi'],metadata=im.info['Description']))
    phaseC=dict(ecog_bouts=2648,rodent_unique_inputs=3646,rodent_analysis_rows=3982,reused_source_hashes_unchanged=True,one_checkpoint_per_input=True,ecog_success=success)
record=dict(status='PASS',recorded_utc=datetime.now(timezone.utc).isoformat(),freeze_commit=m['freeze_commit'],git_tag='v3.0',protocol_sha256=m['protocol_sha256'],working_tree_clean=True,tagged_source_matches_tested_source_bytes=True,archived_attempt1_hashes_unchanged=True,HB_complete_signal_cases_exact=675,HB_saved_v1_estimates_exact=675,heldout_inputs=1575,per_trial_method_rows=11025,no_duplicates=True,all_filter_guards_passed=True,independent_binomial_sum_checks_passed=True,recommended=bool(recommended),phaseC=phaseC,figures=figures,results_committed=False)
(O/'final_verification.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
report=(O/'RESULTS_v3.md').read_text(encoding='utf-8');report+='\n## Final verification\n\nSaved-output audit: [final_verification.json](<'+(O/'final_verification.json').as_posix()+'>). Source, protocol, dependency and archive hashes match. The repository is clean; no result was committed. File checksums: [output_manifest.json](<'+(O/'output_manifest.json').as_posix()+'>).\n'
(O/'RESULTS_v3.md').write_text(report,encoding='utf-8')
files=[]
for p in sorted(O.rglob('*')):
    if p.is_file() and '.matplotlib' not in p.parts and '__pycache__' not in p.parts and p.name!='output_manifest.json':files.append(dict(path=str(p.relative_to(O)),bytes=p.stat().st_size,sha256=sha(p)))
(O/'output_manifest.json').write_text(json.dumps(dict(freeze_commit=m['freeze_commit'],protocol_sha256=m['protocol_sha256'],files=files),indent=2),encoding='utf-8')
print(json.dumps(record),flush=True)
