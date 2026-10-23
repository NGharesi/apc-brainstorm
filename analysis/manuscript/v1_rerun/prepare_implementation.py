from pathlib import Path
import re,json,hashlib
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT/'apc-brainstorm-publish';A=REPO/'analysis/v1_revision';A.mkdir(exist_ok=True)
base=(ROOT/'revision_checks/snapshot/bst_apc.m').read_text(encoding='utf-8-sig')
def replace_function(s,name,new):
    starts=list(re.finditer(r'^function\s+.*$',s,re.M))
    for i,m in enumerate(starts):
        if re.search(r'\b'+re.escape(name)+r'\s*\(',m.group()):
            return s[:m.start()]+new.rstrip()+'\n\n\n'+s[starts[i+1].start() if i+1<len(starts) else len(s):]
    raise ValueError(name)
s=base.replace('function sApc = bst_apc(sMatrix, OPTIONS)','function [sApc, runInfo] = bst_apc(sMatrix, OPTIONS)',1)
s=s.replace('    nSignals = size(data, 1);','    nSignals = size(data, 1);\n    runInfo=struct(\'version\',\'v1.0\',\'options\',options,\'route\',strings(nSignals,1));',1)
s=s.replace('        statusCode(iSignal)    = metrics.status_code;','        statusCode(iSignal)    = metrics.status_code;\n        runInfo.route(iSignal) = metrics.route;',1)
s=s.replace("        'status_code', 0);","        'status_code', 0, 'route', \"not_reached\");",1)
s=s.replace('[ampFreq, ampWidth] = estimate_amplitude_frequency( ...','[ampFreq, ampWidth, metrics.route] = estimate_amplitude_frequency( ...',1)
s=s.replace('        options.amplitudeBandWidthHz);','        options.amplitudeBandWidthHz, options.stepFourMode);',1)
s=s.replace('get_amplitude_band(ampFreq, ampWidth, fs, localOptions.fA)','get_amplitude_band(ampFreq, ampWidth, fs, localOptions.fA, options.stepFourMode)',1)
s=s.replace('    ampSignal = bandpass_signal(signal, fs, ampBand);','    ampSignal = carrier_bandpass(signal, fs, ampBand, options.stepFourMode);',1)
phase='''function phaseFreq = estimate_phase_frequency_fft(epochSignal, fs, options)
    maxPhaseHz=min([options.fA(1)-0.5, fs/3, options.maxPhaseHz]);
    if maxPhaseHz<=options.minPhaseHz, phaseFreq=nan; return; end
    signal=epochSignal(:)-mean(epochSignal,'omitnan');
    nfft=max(256,2^nextpow2(numel(signal)));
    if options.fPRefine
        nfft=max(nfft,2^nextpow2(ceil(fs/options.fPMaxBinSpacingHz)));
    end
    [pxx,f]=pwelch(signal,[],[],nfft,fs);
    valid=(f>=options.minPhaseHz)&(f<=maxPhaseHz);
    if ~any(valid), phaseFreq=nan; return; end
    indices=find(valid);[~,iMax]=max(pxx(valid));i=indices(iMax);phaseFreq=f(i);
    if options.fPRefine && i>1 && i<numel(f) && valid(i-1) && valid(i+1)
        y=log(max(pxx(i-1:i+1),realmin));den=y(1)-2*y(2)+y(3);
        if isfinite(den) && den<0
            delta=0.5*(y(1)-y(3))/den;delta=max(-0.5,min(0.5,delta));
            phaseFreq=min(max(f(i)+delta*(fs/nfft),options.minPhaseHz),maxPhaseHz);
        end
    end
end'''
s=replace_function(s,'estimate_phase_frequency_fft',phase)
starts=s.index('function [ampFreq, ampWidth] = estimate_amplitude_frequency(');end=s.index('\nfunction ',starts+1)
legacy=s[starts:end]
legacy=legacy.replace('function [ampFreq, ampWidth] = estimate_amplitude_frequency(', 'function [ampFreq, ampWidth, route] = estimate_amplitude_frequency(')
legacy=legacy.replace('inputBand, candidateBandWidthHz)','inputBand, candidateBandWidthHz, mode)',1)
legacy=legacy.replace('    ampFreq = nan;', '''    route="not_attempted";
    if strcmp(mode,'june2026_clipped')
        [ampFreq,~,~,fallbackTrace]=estimate_amplitude_frequency_debug(signal,troughLocs,meanEpoch,meanTf,freqs,fs,phaseFreq,inputBand);
        ampWidth=12;
        if isempty(fallbackTrace),route="direct_envelope_scan";else,route="tf_fallback";end
        return;
    end
    if strcmp(mode,'v1'),candidateBandWidthHz=2*phaseFreq;end
    ampFreq = nan;''',1)
legacy=legacy.replace('            ampSignal = bandpass_signal(signal, fs, thisBand);','''            if strcmp(mode,'v1')
                thisBand=[max(inputBand(1),candidateFreqs(iFreq)-phaseFreq),min([inputBand(2),fs/2-eps,candidateFreqs(iFreq)+phaseFreq])];
            end
            ampSignal = carrier_bandpass(signal, fs, thisBand, mode);''',1)
legacy=legacy.replace('    if any(isfinite(scoreTrace))','    if any(isfinite(scoreTrace))\n        route="direct_envelope_scan";',1)
legacy=legacy.replace('    [ampFreq, ampWidth] = estimate_amplitude_frequency_tf_fallback(', '    route="tf_fallback";\n    [ampFreq, ampWidth] = estimate_amplitude_frequency_tf_fallback(',1)
legacy=legacy.replace('\nend\n','\n    if strcmp(mode,\'v1\'),ampWidth=2*phaseFreq;end\nend\n')
s=s[:starts]+legacy+s[end:]
s=s.replace('function band = get_amplitude_band(centerHz, widthHz, fs, inputBand)','function band = get_amplitude_band(centerHz, widthHz, fs, inputBand, mode)',1)
s=s.replace('    halfWidth = max(2, widthHz / 2);','    if strcmp(mode,\'v1\'),halfWidth=widthHz/2;else,halfWidth=max(2,widthHz/2);end',1)
s=s.replace("get_option(optionsIn, 'fA', [16 250])","get_option(optionsIn, 'fA', [80 150])",1)
s=s.replace("    options.amplitudeBandWidthHz = get_option(optionsIn, 'amplitudeBandWidthHz', 4);",'''    options.amplitudeBandWidthHz = get_option(optionsIn, 'amplitudeBandWidthHz', 4);
    options.stepFourMode=lower(char(string(get_option(optionsIn,'stepFourMode','v1'))));
    options.fPRefine=parse_flag(get_option(optionsIn,'fPRefine',true));
    options.fPMaxBinSpacingHz=get_option(optionsIn,'fPMaxBinSpacingHz',0.05);
    if ~ismember(options.stepFourMode,{'v1','oct2026','june2026_clipped'})
        error('bst_apc:StepFourMode','Unknown Step 4 mode.');
    end
    if ~isscalar(options.fPMaxBinSpacingHz)||~isfinite(options.fPMaxBinSpacingHz)||options.fPMaxBinSpacingHz<=0||options.fPMaxBinSpacingHz>0.05
        error('bst_apc:SpectralSpacing','fPMaxBinSpacingHz must be positive and <=0.05 Hz.');
    end''',1)
# Reuse immutable designfilt objects, with exactly the old numerical filtering.
start=s.index('    d = designfilt(',s.index('function signalOut = bandpass_signal('));end=s.index('    signalOut = filtfilt(',start)
design=s[start:end]
cache='''    persistent filterKeys filterObjects
    if isempty(filterKeys),filterKeys={};filterObjects={};end
    key=sprintf('%.17g,%.17g,%.17g',fs,band(1),band(2));j=find(strcmp(filterKeys,key),1);
    if isempty(j)
'''+design+'''        filterKeys{end+1}=key;filterObjects{end+1}=d;
    else
        d=filterObjects{j};
    end
'''
s=s[:start]+cache+s[end:]
debug=(ROOT/'debug_apc_matlab_case.m').read_text(encoding='utf-8-sig');debug=debug[debug.index('function [fa, scoreTrace, candidateFreqs, fallbackTrace] = estimate_amplitude_frequency_debug'):]
# Same filter coefficients and filtfilt as June, now reusing the core cache.
debug=replace_function(debug,'bandpass_signal_local', '''function signalOut = bandpass_signal_local(signalIn,fs,band)
    signalOut=bandpass_signal(signalIn,fs,band);
end''')
s+='\n'+debug+'''
function signalOut=carrier_bandpass(signal,fs,band,mode)
    if ~strcmp(mode,'v1'),signalOut=bandpass_signal(signal,fs,band);return;end
    signalOut=[];
    if numel(band)~=2||any(~isfinite(band))||band(1)<=0||band(2)>=fs/2||band(1)>=band(2),return;end
    % Fourth-order Butterworth bandpass, in SOS form. The v1 carrier bands
    % change with continuous fP; design the same IIR family directly.
    [z,p,k]=butter(2,band/(fs/2),'bandpass');[sos,g]=zp2sos(z,p,k);
    signalOut=filtfilt(sos,g,double(signal(:).'));
end
'''
s=s.replace('% USAGE:\n%   sApc = bst_apc(sMatrix, OPTIONS)','% USAGE:\n%   [sApc, runInfo] = bst_apc(sMatrix, OPTIONS)\n% runInfo contains version, full normalized options and per-signal route.\n% stepFourMode: v1 (default), oct2026, june2026_clipped.\n% fPRefine: true (default), or false for the preserved Welch-bin estimate.\n% fPMaxBinSpacingHz: 0.05 (maximum refined spectral-bin spacing).')
(REPO/'src/bst_apc.m').write_text(s,encoding='utf-8')
# Frozen copies of original generators with component bookkeeping only.
for bench,name,simname in [('sparsity','run_apc_burst_sparsity_benchmark.m','local_simulate_sparse_burst_signal'),('distractor','run_apc_distractor_frequency_benchmark.m','local_simulate_distractor_signal')]:
    original=(ROOT/'apc-brainstorm-release/analysis'/name).read_text(encoding='utf-8-sig')
    tail=original[original.index('\nfunction cfg = local_get_profile'):]
    tail=tail.replace('function signal = '+simname+'(', 'function [signal,parts] = '+simname+'(',1)
    if bench=='sparsity':
        marker='    signal = low + high;'
        parts='''
    parts=struct('true_envelope',trueEnv,'carrier',sin(2*pi*cfg.true_fa_hz*t), ...
       'true_component',cfg.true_high_amp*cfg.coupling_level*trueEnv.*sin(2*pi*cfg.true_fa_hz*t), ...
       'low_component',low,'background_component',cfg.true_high_amp*cfg.background_burst_scale*bgEnv.*sin(2*pi*cfg.true_fa_hz*t), ...
       'distractor_component',zeros(size(t)));'''
        generate='''[clean,parts]=local_simulate_sparse_burst_signal(t,cfg,level);
            signal=local_add_mixed_noise(clean,cfg.snr_db);'''
        profile='full'
    else:
        marker='    signal = low + trueHf + distractorHf;'
        parts='''
    parts=struct('true_envelope',trueEnv,'carrier',sin(2*pi*cfg.true_fa_hz*t), ...
       'true_component',cfg.true_high_amp*cfg.coupling_level*trueEnv.*sin(2*pi*cfg.true_fa_hz*t), ...
       'low_component',low,'background_component',zeros(size(t)),'distractor_component',distractorHf);'''
        generate='''[clean,parts]=local_simulate_distractor_signal(t,cfg,level,'coupled');
            nullSignal=local_simulate_distractor_signal(t,cfg,level,'null');
            signal=local_add_mixed_noise(clean,cfg.snr_db);
            nullSignal=local_add_mixed_noise(nullSignal,cfg.snr_db); %#ok<NASGU>'''
        profile='reviewer_control'
    assert marker in tail;tail=tail.replace(marker,marker+parts,1)
    header=f'''function varargout=v1_{bench}_generator(action,varargin)
% Original generator, original RNG draw order, added component capture.
switch action
 case 'profile'
  varargout{{1}}=local_get_profile('{profile}');
 case 'generate'
  cfg=varargin{{1}};level=varargin{{2}};t=0:1/cfg.fs_hz:cfg.duration_s-1/cfg.fs_hz;
  {generate}
  parts.noise=signal-clean;
  varargout={{signal,t,parts}};
 otherwise
  error('v1:GeneratorAction','Unknown generator action');
end
end
'''
    (A/f'v1_{bench}_generator.m').write_text(header+tail,encoding='utf-8')
protected={}
for p in [ROOT/'apc_burst_sparsity_benchmark_full.mat',ROOT/'apc_distractor_frequency_benchmark_reviewer_control.mat',ROOT/'apc_burst_sparsity_runs_full.csv',ROOT/'apc_distractor_frequency_runs_reviewer_control.csv']:
    protected[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
(Path(__file__).parent/'protected_saved_results.json').write_text(json.dumps(protected,indent=2),encoding="utf-8")
print('Implemented selectable APC modes and frozen generator adapters.')
