"""Prepare analysis-only copies and an immutable input/source manifest."""
from pathlib import Path
import csv, hashlib, json, subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
REPO = ROOT / 'apc-brainstorm-publish'
ANALYSIS = REPO / 'analysis/v1_revision'
GIT = r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe'

def read(p):
    return p.read_text(encoding='utf-8')

def write(p, text):
    assert not p.exists(), str(p)
    p.write_text(text, encoding='utf-8')

def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()

def git(*args):
    return subprocess.check_output([GIT, '-C', str(REPO), *args], encoding='utf-8').strip()

assert git('rev-parse', 'HEAD') == '71ebc16aed32ca38be73a800738b975e5806b330'
assert git('rev-list', '-n', '1', 'v1.0') == git('rev-parse', 'HEAD')
assert not git('status', '--porcelain')

# Only A2 width is added; A1 remains byte-for-byte the same arithmetic.
s = read(ANALYSIS / 'v1_comparators.m').replace('function rows=v1_comparators(', 'function rows=fu_comparators(', 1)
s = s.replace('half=6;if mode=="A1",half=fp;end', 'half=6;if mode=="A1",half=fp;elseif mode=="A2",half=12;end')
s = s.replace('selectedHalf=6;if mode=="A1",selectedHalf=fpGrid(ip);end', 'selectedHalf=6;if mode=="A1",selectedHalf=fpGrid(ip);elseif mode=="A2",selectedHalf=12;end')
write(OUT/'fu_comparators.m', s)

# Instrument a separate copy. All numeric method statements remain unchanged.
s = read(REPO / 'src/bst_apc.m')
original = s
s = s.replace('function [sApc, runInfo] = bst_apc(', 'function [sApc, runInfo] = fu_apc_diagnostic(', 1)
s = s.replace('    pacStrength = nan(nSignals, 1);', '    runInfo.diagnostics=cell(nSignals,1);\n    pacStrength = nan(nSignals, 1);', 1)
s = s.replace('        pacStrength(iSignal)', '        runInfo.diagnostics{iSignal}=diagnostics;\n        pacStrength(iSignal)', 1)
s = s.replace('    if ~isfinite(phaseFreq) || phaseFreq < options.minPhaseHz', '    diagnostics.estimated_fp_hz=phaseFreq;\n    diagnostics.fs=fs;\n    if ~isfinite(phaseFreq) || phaseFreq < options.minPhaseHz', 1)
s = s.replace('    phaseSignal = bandpass_signal(signal, fs, phaseBand);', '    diagnostics.phase_band_hz=phaseBand;\n    phaseSignal = bandpass_signal(signal, fs, phaseBand);', 1)
s = s.replace('    metrics.n_phase_events = numel(troughLocs);', '''    diagnostics.trough_locations=troughLocs;
    diagnostics.trough_count_before=numel(troughLocs);
    diagnostics.epoch_half_samples=max(2,round(options.phaseEpochCycles*fs/max(phaseFreq,eps)));
    diagnostics.trough_count_after=sum(troughLocs-diagnostics.epoch_half_samples>=1 & troughLocs+diagnostics.epoch_half_samples<=numel(signal));
    metrics.n_phase_events = numel(troughLocs);''', 1)
s = s.replace('    if isempty(troughLocs)\n        metrics.status_code = 4;', '    if isempty(troughLocs)\n        diagnostics.return_condition="isempty(troughLocs)";\n        metrics.status_code = 4;', 1)
s = s.replace('    if isempty(phaseLockedAverage) || isempty(phaseLockedTf)\n        metrics.status_code = 4;', '    if isempty(phaseLockedAverage) || isempty(phaseLockedTf)\n        diagnostics.return_condition="isempty(phaseLockedAverage) || isempty(phaseLockedTf)";\n        metrics.status_code = 4;', 1)
write(OUT/'fu_apc_diagnostic.m', s)

# Exact spectral arithmetic, exposing neighboring bins in both FFT modes.
start = original.index('function phaseFreq = estimate_phase_frequency_fft(')
end = original.index('\n\nfunction ', start+10)
trace = original[start:end].replace('function phaseFreq = estimate_phase_frequency_fft(', 'function [phaseFreq,trace] = fu_phase_trace(',1)
trace = trace.replace('    maxPhaseHz=', "    trace=struct();\n    maxPhaseHz=",1)
trace = trace.replace('    if options.fPRefine && i>1', '''    trace.peak_hz=f(i);trace.bin_spacing_hz=fs/nfft;
    trace.left_hz=f(max(1,i-1));trace.right_hz=f(min(numel(f),i+1));
    trace.nfft=nfft;trace.delta=0;trace.interpolated=false;
    if options.fPRefine && i>1''',1)
trace = trace.replace('            phaseFreq=min(max(', '            trace.delta=delta;trace.interpolated=true;\n            phaseFreq=min(max(',1)
write(OUT/'fu_phase_trace.m',trace+'\n')

# Reuse only the generator/profile/noise routines, avoiding unused analysis code.
s = read(ANALYSIS/'v1_distractor_generator.m')
profile = s[s.index('function cfg = local_get_profile'):s.index('function [trialRows, oracleRows]')]
sim = s[s.index('function [signal,parts] = local_simulate_distractor_signal'):s.index('function out = local_run_apc')]
sim = sim.replace("'true_envelope',trueEnv", "'true_event_times',coupledTimes,'true_envelope',trueEnv",1)
wrapper = '''function varargout=fu_slow_generator(action,varargin)
% Analysis-only scenario derivative of frozen distractor generator.
switch action
 case 'profile'
  cfg=local_get_profile('reviewer_control');cfg.true_fp_hz=6;
  cfg.phase_offset_deg=180;cfg.distractor_base_amp=0;
  cfg.slow_distractor_hz=10;cfg.slow_amplitude_ratios=[0 .5 1 1.5 2 3];
  cfg.slow_distractor_phase_rad=0;cfg.slow_amplitude_ratio=0;
  cfg.high_frequency_distractor_present=false;
  varargout{1}=cfg;
 case 'generate'
  cfg=varargin{1};ratio=varargin{2};t=0:1/cfg.fs_hz:cfg.duration_s-1/cfg.fs_hz;
  [~,parts]=local_simulate_distractor_signal(t,cfg,0,'coupled');
  unusedNull=local_simulate_distractor_signal(t,cfg,0,'null');
  slow10=ratio*cfg.low_amp*sin(2*pi*cfg.slow_distractor_hz*t+cfg.slow_distractor_phase_rad);
  parts.distractor_component=slow10;
  parts.base_carrier_component=cfg.base_hf_amp*parts.carrier;
  clean=parts.low_component+parts.base_carrier_component+parts.true_component+slow10;
  signal=local_add_mixed_noise(clean,cfg.snr_db);
  unusedNull=local_add_mixed_noise(unusedNull,cfg.snr_db); %#ok<NASGU>
  parts.noise=signal-clean;
  varargout={signal,t,parts};
 otherwise
  error('followup:GeneratorAction','Unknown generator action');
end
end
'''
write(OUT/'fu_slow_generator.m',wrapper+profile+sim)

selected=[]
for name in ['main_trials.csv','null_trials.csv']:
    with (ROOT/'revision_checks/v1_rerun'/name).open(encoding='utf-8',newline='') as f:
        for row in csv.DictReader(f):
            if row['configuration']=='v1.0' and row['method']=='APC' and row['status_code']=='4':
                selected.append({k:row[k] for k in ['stage','benchmark','dataset','level','repeat_index']})
assert len(selected)==36
write(OUT/'status4_selection.json',json.dumps(selected,indent=2))

manifest = {'git_commit':git('rev-parse','HEAD'),'tag':'v1.0',
    'source_files':{str(p):digest(p) for p in sorted(REPO.rglob('*')) if p.is_file() and '.git' not in p.parts},
    'input_files':{str(p):digest(p) for p in sorted((ROOT/'revision_checks/v1_rerun').glob('*.mat'))},
    'status4_source_lines':{text:next(i for i,line in enumerate(original.splitlines(),1) if text in line) for text in ['if isempty(troughLocs)','if isempty(phaseLockedAverage) || isempty(phaseLockedTf)','if idx(1) < 1 || idx(end) > numel(signal)']}}
write(OUT/'input_source_manifest.json',json.dumps(manifest,indent=2))
print(json.dumps({'status4_trials':len(selected),'input_files':len(manifest['input_files']),'source_lines':manifest['status4_source_lines']}))
