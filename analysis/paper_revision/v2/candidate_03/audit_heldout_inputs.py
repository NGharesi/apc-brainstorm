"""Readback audit of every held-out input, without changing any input."""
from pathlib import Path
import csv,json,sys,time
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent.parent
sys.path.insert(0,str(ROOT/'pydeps'))
import h5py,numpy as np
start=time.monotonic()
metadata=json.loads((OUT/'generate_runtime.json').read_text(encoding='utf-8'))['metadata']
with (OUT/'heldout_frequency_draws.csv').open(encoding='utf-8',newline='') as f:draws={int(r['coupled_input_id']):r for r in csv.DictReader(f)}
def scalar(g,k):return float(np.asarray(g[k][()]).ravel()[0])
def vector(g,k):return np.asarray(g[k][()]).ravel()
rows=[];counts={'coupled':0,'timing_null':0,'no_coupled_burst':0}
with h5py.File(OUT/'heldout_inputs.mat','r') as f:
    refs=f['cases'][:,0]
    for i,ref in enumerate(refs,1):
        g=f[ref];cfg=g['cfg'];parts=g['parts'];ident=int(scalar(g,'input_id'));paired=int(scalar(g,'paired_coupled_id'))
        assert ident==i and paired in draws
        draw=draws[paired];scenario=draw['scenario'];fp=scalar(cfg,'true_fp_hz');fa=scalar(cfg,'true_fa_hz')
        assert abs(fp-float(draw['true_fp_hz']))<1e-12 and abs(fa-float(draw['true_fa_hz']))<1e-12
        assert scalar(cfg,'random_seed')==20261022 and scalar(cfg,'snr_db')==-3
        assert (4<=fp<=7 if scenario=='H2' else 5<=fp<=11) and 90<=fa<=140
        x=vector(g,'signal');t=vector(g,'time');carrier=vector(parts,'carrier');noise=vector(parts,'noise')
        low=vector(parts,'low_component');background=vector(parts,'background_component');distractor=vector(parts,'distractor_component');true=vector(parts,'true_component')
        baseline=(1.25 if scenario=='H4' else scalar(cfg,'base_hf_amp'))*carrier
        clean=low+baseline+true+background+distractor
        residual=float(np.max(np.abs(x-clean-noise)));assert residual<=1e-12,(ident,residual)
        dataset='coupled' if ident==paired else ('no_coupled_burst' if scalar(cfg,'coupling_level')==0 else 'timing_null')
        counts[dataset]+=1;pair_residual=float('nan');shared=True;snr=float('nan')
        if dataset=='coupled':
            snr=float(10*np.log10(np.mean(clean**2)/np.mean(noise**2)));assert abs(snr+3)<1e-10,(ident,snr)
        else:
            c=f[refs[paired-1]];cp=c['parts']
            for field in ['carrier','noise','low_component','background_component','distractor_component']:
                assert np.array_equal(vector(parts,field),vector(cp,field)),(ident,field)
            removed=vector(g,'removed_true_component');added=vector(g,'added_true_component')
            pair_residual=float(np.max(np.abs((vector(c,'signal')-x)-(removed-added))));assert pair_residual<=1e-12
            if dataset=='timing_null':
                times=vector(g,'poisson_times');env=np.zeros_like(t)
                for center in times:env+=np.exp(-.5*((t-center)/scalar(cfg,'burst_sigma_s'))**2)
                if env.max()>0:env/=env.max()
                expected=scalar(cfg,'true_high_amp')*scalar(cfg,'coupling_level')*env*carrier
                assert np.max(np.abs(expected-true))<=1e-12
            else:assert np.array_equal(true,np.zeros_like(true))
        if scenario=='H2':
            fd=float(draw['true_fd_hz']);phi=float(draw['distractor_phase_rad']);ratio=float(draw['level'])
            assert fp+3<=fd<=13 and scalar(cfg,'phase_offset_deg')==180
            expected=ratio*scalar(cfg,'low_amp')*np.sin(2*np.pi*fd*t+phi)
            assert np.max(np.abs(expected-distractor))<=1e-10
        if scenario=='H1_distractor':assert abs(scalar(cfg,'distractor_fa_hz')-(fa-24))<1e-12
        if scenario=='H4':assert len(x)==6000 and abs(np.std(low,ddof=1)-1)<1e-12
        row={'input_id':ident,'paired_coupled_id':paired,'scenario':scenario,'dataset':dataset,'level':draw['level'],'repeat_index':draw['repeat_index'],
             'decomposition_residual':residual,'paired_component_residual':pair_residual,'shared_components_exact':shared,'coupled_noise_snr_db':snr,
             'git_commit':metadata['git_commit'],'matlab_version':metadata['matlab_version'],'seed':20261022,
             'apc_options_json':json.dumps(metadata['apc_configurations']),'comparator_settings_json':json.dumps(metadata['comparator_settings'])}
        rows.append(row)
assert counts=={'coupled':350,'timing_null':250,'no_coupled_burst':75}
with (OUT/'heldout_input_readback_audit.csv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
(OUT/'heldout_input_readback_audit.json').write_text(json.dumps({'passed':True,'counts':counts,'elapsed_seconds':time.monotonic()-start,'metadata':metadata},indent=2),encoding='utf-8')
deviation=OUT/'tooling_deviations.json';d=json.loads(deviation.read_text(encoding='utf-8'))
detail={'type':'HDF5 read-only inspection','detail':'Initial inspection assumed cfg/parts were reference datasets; they are scalar struct groups. The inspector was adapted; no input or method changed.'}
if detail not in d['deviations']:d['deviations'].append(detail)
deviation.write_text(json.dumps(d,indent=2),encoding='utf-8')
print(json.dumps({'input_readback':'PASS','counts':counts,'elapsed_seconds':time.monotonic()-start}))
