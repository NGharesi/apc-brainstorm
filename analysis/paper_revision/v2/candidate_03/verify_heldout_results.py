"""Independent readback of frozen provenance, frequency picks and event tests."""
from pathlib import Path
import csv,hashlib,json,math,subprocess,sys
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent.parent;REPO=ROOT/'apc-brainstorm-publish'
sys.path.insert(0,str(ROOT/'pydeps'))
import h5py,numpy as np
GIT=r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe'
def git(*a):return subprocess.check_output([GIT,'-C',str(REPO),*a],encoding='utf-8').strip()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def vector(g,k):return np.asarray(g[k][()]).ravel()
def scalar(g,k):return float(vector(g,k)[0])
def near(a,b):return abs(a-b)<=1e-9*max(1,abs(b))
def refined(grid,values,step):
    k=int(np.nanargmax(values));value=float(grid[k])
    if 0<k<len(grid)-1 and np.all(np.isfinite(values[k-1:k+2])):
        y=values[k-1:k+2];den=y[0]-2*y[1]+y[2]
        if math.isfinite(den) and den<0:value+=max(-.5,min(.5,.5*(y[0]-y[2])/den))*step
    return value
runtime=load(OUT/'generate_runtime.json');metadata=runtime['metadata'];commit=metadata['git_commit']
assert git('rev-parse','HEAD')==git('rev-list','-n','1','v2.0')==commit and not git('status','--porcelain')
assert git('rev-parse','v2.0:src/bst_apc.m')==load(OUT/'unit_attempt_01/unit_results.json')['metadata']['apc_source_blob']
assert load(OUT/'heldout_input_readback_audit.json')['passed']
for path,digest in load(OUT/'heldout_inputs_sha256.json')['files'].items():assert sha(path)==digest,path
rows=[]
for worker in [1,2,3]:
    assert load(OUT/f'worker_{worker}_runtime.json')['status']=='COMPLETE'
    with (OUT/f'heldout_worker{worker}_trials.csv').open(encoding='utf-8',newline='') as f:rows.extend(csv.DictReader(f))
assert len(rows)==6750 and len({(r['input_id'],r['configuration'],r['method']) for r in rows})==6750
primary={int(r['input_id']):r for r in rows if r['configuration']=='v2.0'};assert len(primary)==675
verified=set();valid=0;invalid=0
for path in sorted(OUT.glob('heldout_worker*_chunk*.mat')):
    with h5py.File(path,'r') as f:
        refs=np.asarray(f['details'][()]).ravel()
        for ref in refs:
            d=f[ref];ident=int(scalar(d,'input_id'));assert ident not in verified;verified.add(ident);r=primary[ident];opts=d['options']
            assert scalar(opts,'eventSurrogateSeed')==20261022 and scalar(opts,'eventSurrogateSubstream')==1000+ident
            assert scalar(opts,'eventSurrogateCount')==200 and scalar(opts,'amplitudeSigmaPhaseMultiplier')==1.5 and scalar(opts,'amplitudeScoreSmoothPoints')==1
            if r['valid']=='1':
                valid+=1;grid=vector(d,'phase_grid');blp=vector(d,'BLP');amp_grid=vector(d,'amplitude_grid');scores=vector(d,'amplitude_scores')
                assert near(float(r['recovered_fp_hz']),refined(grid,blp,.05))
                assert near(float(r['recovered_fa_hz']),refined(amp_grid,scores,1))
                assert near(float(r['gaussian_sigma_hz']),1.5*float(r['recovered_fp_hz']))
                maxima=vector(d,'surrogate_max_BLP');fixed=vector(d,'surrogate_fixed_BLP');assert len(maxima)==len(fixed)==200
                observed=float(blp.max());assert near(observed,float(r['event_statistic']))
                p=(1+int(np.sum(maxima>=observed)))/201;z=(observed-maxima.mean())/maxima.std(ddof=1)
                assert p==float(r['event_p']) and near(float(r['event_z']),z)
                obs_fixed=float(r['event_blp']);pf=(1+int(np.sum(fixed>=obs_fixed)))/201;zf=(obs_fixed-fixed.mean())/fixed.std(ddof=1)
                assert pf==float(r['event_p_fixed']) and near(float(r['event_z_fixed']),zf)
            else:
                invalid+=1;assert int(r['status']) in [1,3,5]
                assert math.isnan(float(r['event_p']))
assert verified==set(range(1,676))
for r in rows:
    assert r['git_commit']==commit and int(r['seed'])==20261022
    if r['configuration'] in ['A2_prime','A1_prime']:
        assert 3<=float(r['recovered_fp_hz'])<=14 and float(r['recovered_fp_hz'])*2==round(float(r['recovered_fp_hz'])*2)
        assert 80<=float(r['recovered_fa_hz'])<=160 and (float(r['recovered_fa_hz'])-80)%4==0
previous=load(OUT.parent/'preservation_verification.json');protected=0
for x in previous['checks']:assert sha(x['path'])==x['sha256'];protected+=1
for path,digest in load(OUT.parent/'candidate_02/output_manifest.json')['files'].items():assert sha(path)==digest;protected+=1
assert git('rev-list','-n','1','v1.0')=='71ebc16aed32ca38be73a800738b975e5806b330'
result={'passed':True,'git_commit':commit,'input_hashes_unchanged':True,'input_readback_passed':True,'verified_v2_inputs':675,'v2_valid':valid,'v2_invalid':invalid,
 'frequency_argmax_and_parabolas_verified':True,'event_p_z_from_saved_surrogates_verified':True,'comparator_grid_picks_verified':True,'prior_files_unchanged':protected,
 'v1_tag_unchanged':True,'frozen_tree_clean':True,'metadata':metadata}
(OUT/'final_verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'result_readback':'PASS','v2_valid':valid,'v2_invalid':invalid,'prior_files_unchanged':protected}))
