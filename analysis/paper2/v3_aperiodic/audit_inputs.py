"""Check saved HA dimensions, pairing and generator settings; no method calls."""
from pathlib import Path
import hashlib,json,sys
O=Path(__file__).resolve().parent;R=O.parent.parent;sys.path.insert(0,str(R/'pydeps'))
import h5py
import numpy as np
import pandas as pd
m=json.loads((O/'phaseB_implementation.json').read_text(encoding='utf-8'))
D=pd.read_csv(O/'HA_frequency_draws.csv',encoding='utf-8',float_precision='round_trip')
assert len(D)==450 and D.groupby(['beta','rhythm_amplitude','duration_s']).size().eq(25).all()
assert set(D.beta)=={1,1.5,2} and set(D.rhythm_amplitude)=={.3,.5,.8} and set(D.duration_s)=={2,6}
assert D.true_fp_hz.between(6,25).all() and D.true_fa_hz.between(80,140).all() and D.pair_residual.le(1e-12).all()
maximum=0.;maxsd=0.
with h5py.File(O/'HA_inputs.mat','r') as f:
    refs=f['cases'][()].reshape(-1);assert len(refs)==900
    for k in range(0,900,2):
        c=f[refs[k]];n=f[refs[k+1]];cfg=c['cfg'];p=c['parts']
        scalar=lambda key:float(np.asarray(cfg[key]).squeeze())
        fs=scalar('fs_hz');T=scalar('duration_s');assert fs==1000 and T in [2,6]
        x=np.asarray(c['signal']).reshape(-1);y=np.asarray(n['signal']).reshape(-1);t=np.asarray(c['time']).reshape(-1)
        assert len(x)==len(y)==len(t)==int(T*fs) and np.isfinite(x).all() and np.isfinite(y).all()
        assert np.max(np.abs(t-np.arange(len(t))/fs))<1e-12
        noise=np.asarray(p['noise']).reshape(-1);rhythm=np.asarray(p['rhythm']).reshape(-1);background=np.asarray(p['background_component']).reshape(-1)
        a=np.asarray(p['true_component']).reshape(-1);b=np.asarray(p['null_component']).reshape(-1)
        error=float(np.max(np.abs((x-y)-(a-b))));maximum=max(maximum,error);assert error<=1e-12
        assert np.max(np.abs(x-(noise+rhythm+background+a)))<=1e-12
        assert np.max(np.abs(y-(noise+rhythm+background+b)))<=1e-12
        maxsd=max(maxsd,abs(np.std(noise,ddof=1)-1));assert abs(np.std(noise,ddof=1)-1)<1e-12
        fp=scalar('true_fp_hz');assert np.max(np.abs(rhythm-scalar('rhythm_amplitude')*np.sin(2*np.pi*fp*t)))<1e-12
        carrier=np.asarray(p['carrier']).reshape(-1);assert np.max(np.abs(carrier-np.sin(2*np.pi*scalar('true_fa_hz')*t)))<1e-12
        assert scalar('burst_sigma_s')==.01 and scalar('burst_amplitude')==1.5 and scalar('cycle_keep_probability')==.55 and scalar('jitter_sd_s')==.005 and scalar('background_burst_scale')==.18
record=dict(status='PASS',freeze_commit=m['freeze_commit'],protocol_sha256=m['protocol_sha256'],seed=20261101,HA_cells=18,coupled_trials=450,paired_timing_nulls=450,all_cell_counts_25=True,all_fs_1000=True,all_durations_and_frequency_bounds_correct=True,maximum_pair_component_residual=maximum,maximum_noise_sd_error=maxsd,all_signals_finite=True,provenance='phaseB_implementation.json')
(O/'input_bank_audit.json').write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps(record),flush=True)
