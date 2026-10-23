from pathlib import Path
import sys,json,hashlib,subprocess
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=ROOT/'revision_checks/final'
sys.path.insert(0,str(ROOT/'pydeps'));sys.path.insert(0,str(ROOT))
import numpy as np
from scipy.io import loadmat
src=(OUT/'frozen_v1/bst_apc.m').read_text(encoding='utf-8')
# Instrument a separate diagnostic copy; primary estimates always call the byte-identical frozen source.
diag=src.replace('function [sApc, runInfo] = bst_apc(', 'function [sApc, runInfo] = final_v1_diagnostics(',1)
diag=diag.replace('pacStrength = nan(nSignals, 1);','runInfo.diagnostics=cell(nSignals,1);\n    pacStrength = nan(nSignals, 1);',1)
diag=diag.replace('pacStrength(iSignal)   = metrics.pac_strength;','runInfo.diagnostics{iSignal}=diagnostics;\n        pacStrength(iSignal)   = metrics.pac_strength;',1)
diag=diag.replace('burstLocs = detect_peaks_with_defaults(', 'burstLocs = detect_peaks_with_defaults(',1)
needle='[burstEpochs, timeEpoch] = collect_burst_epochs'
# Match the actual assignment name below, leaving calculation lines untouched.
diag=diag.replace('    if isempty(burstEpochs)', '    diagnostics.burst_trace=burstTrace;diagnostics.burst_locs=burstLocs;\n    if isempty(burstEpochs)',1)
diag=diag.replace('[ampFreq, ampWidth, metrics.route] = estimate_amplitude_frequency(', '[ampFreq, ampWidth, metrics.route, scoreTrace, candidateFreqs] = estimate_amplitude_frequency(',1)
diag=diag.replace('    if strcmp(options.stepFourMode', '    if strcmp(options.stepFourMode',1)
diag=diag.replace('    ampBand = get_amplitude_band(', '    diagnostics.fa_score=scoreTrace;diagnostics.fa_grid=candidateFreqs;\n    ampBand = get_amplitude_band(',1)
diag=diag.replace('    amplitudeEnvelope = abs(hilbert(ampSignal));','    amplitudeEnvelope = abs(hilbert(ampSignal));\n    diagnostics.phase_angles=phaseAngles;diagnostics.amplitude_envelope=amplitudeEnvelope;diagnostics.phase_signal=phaseSignal;',1)
diag=diag.replace('function [ampFreq, ampWidth, route] = estimate_amplitude_frequency(', 'function [ampFreq, ampWidth, route, scoreTrace, candidateFreqs] = estimate_amplitude_frequency(',1)
assert diag!=src and 'route, scoreTrace, candidateFreqs] = estimate_amplitude_frequency' in diag
(OUT/'final_v1_diagnostics.m').write_text(diag,encoding='utf-8')
from apc_simulation_study import SimParams,burst_train_signal,continuous_pac_signal
params=SimParams();rng=np.random.default_rng(12345);t=np.arange(0,params.duration,1/params.fs)
coupled,events=burst_train_signal(t,params,rng,coupled=True)
# Consume the original null draws so the jittered and continuous cases retain their historical seed/order.
old_null,old_events=burst_train_signal(t,params,rng,coupled=False)
jittered,jitter_events=burst_train_signal(t,params,rng,coupled=True,jitter_sd_s=.02)
continuous=continuous_pac_signal(t,params,rng)
prng=np.random.default_rng(20261022);poisson=[];event=.5
while True:
    event+=prng.exponential(1/params.true_fp)
    if event>=params.duration-.5:break
    poisson.append(event)
def burst_component(ev):
    return sum((params.burst_amp*np.exp(-.5*((t-e)/params.burst_sigma_s)**2)*np.sin(2*np.pi*params.true_fa*(t-e)) for e in ev),np.zeros_like(t))
null=coupled-burst_component(events)+burst_component(poisson)
prov=json.loads((OUT/'source_provenance.json').read_text(encoding='utf-8'))
prov.update(seed=12345,poisson_seed=20261022,generator='apc_simulation_study.py',generator_sha256=hashlib.sha256((ROOT/'apc_simulation_study.py').read_bytes()).hexdigest(),parameters=vars(params),jitter_sd_s=.02,poisson_rate_hz=8,poisson_interval_s=[.5,19.5])
import csv
for name,x,ev in [('burst_coupled',coupled,events),('timing_null',null,poisson),('jittered',jittered,jitter_events),('continuous_pac',continuous,[])]:
    with (OUT/(name+'_input.csv')).open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(['time_s','signal','git_commit','seed','generator_settings_json'])
        meta=json.dumps(prov,separators=(',',':'))
        w.writerows((tt,xx,prov['git_commit'],12345,meta) for tt,xx in zip(t,x))
    with (OUT/(name+'_events.csv')).open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(['time_s','git_commit','seed','generator_settings_json']);w.writerows((e,prov['git_commit'],12345,json.dumps(prov,separators=(',',':'))) for e in ev)
for old,new in [('burst_coupled','burst_coupled'),('burst_coupled_jitter_0p02','jittered'),('continuous_pac','continuous_pac')]:
    orig=np.genfromtxt(ROOT/'apc_matlab_benchmark'/(old+'.csv'),delimiter=',',skip_header=1)
    x={'burst_coupled':coupled,'jittered':jittered,'continuous_pac':continuous}[new]
    assert np.allclose(orig[:,1],x,atol=1e-14,rtol=1e-14),(old,np.max(np.abs(orig[:,1]-x)))
e=json.loads((OUT/'local_data_inspection.json').read_text(encoding='utf-8'))
base=Path(r'D:\APC_project\RealDatasets\LFP_data')
r=loadmat(base/'EC3_dataset_real.mat',variable_names=['R2'],simplify_cells=True)['R2'];s=loadmat(base/'HC3/data/EC013/ec013.157.eeg/data_230118_2215.mat',simplify_cells=True)
ix=np.arange(40799,372501);assert len(ix)==s['F'].shape[1]
err=float(np.max(np.abs(r['Value'][ix]-s['F'][0])))
e['crop_channel_match']={'file':str(base/'HC3/data/EC013/ec013.157.eeg/data_230118_2215.mat'),'row_1_based':1,'channel_name':'E1','R2_start_index_1_based':40800,'R2_stop_index_1_based':372501,'crop_time_restarts_at_zero':True,'n_samples':len(ix),'max_absolute_error':err,'exact_match':err==0}
assert err==0
e['provenance']=prov;e['shank']='unresolved: session XML/channel-map absent';e['layer']='undocumented in local files'
(OUT/'channel_evidence.json').write_text(json.dumps(e,indent=2),encoding='utf-8')
prov['canonical_original_csv_reproduction']='all three retained conditions matched within 1e-14'
prov['timing_null_events']=len(poisson)
(OUT/'canonical_provenance.json').write_text(json.dumps(prov,indent=2),encoding='utf-8')
print(json.dumps({'canonical_verified':True,'channel_crop_match':e['crop_channel_match'],'null_event_count':len(poisson)}))
