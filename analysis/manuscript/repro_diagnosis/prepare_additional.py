from pathlib import Path
import json,hashlib,difflib,re
D=Path(__file__).resolve().parent; R=D.parents[1]; S=D/'sources'
protected=json.loads((D/'protected_input_hashes.json').read_text())
records=[]
for name in ['debug_apc_matlab_case.m','test_apc_fa_alternatives.m','apc_simulation_study.py']:
    p=R/name;b=p.read_bytes();digest=hashlib.sha256(b).hexdigest()
    protected[str(p)]=digest
    records.append({'path':str(p),'sha256':digest,'mtime_epoch':p.stat().st_mtime,'ctime_epoch':p.stat().st_ctime})
    (S/name).write_bytes(b)
(D/'additional_source_metadata.json').write_text(json.dumps(records,indent=2))
(D/'protected_input_hashes.json').write_text(json.dumps(protected,indent=2))
base=(S/'rd_apc_instrumented.m').read_text()
cached=base.replace('= rd_apc_instrumented(', '= rd_apc_cached(',1)
start=cached.index('    d = designfilt(',cached.index('function signalOut = bandpass_signal('))
end=cached.index('    signalOut = filtfilt(',start)
design=cached[start:end]
cache='''    persistent filterKeys filterObjects
    if isempty(filterKeys), filterKeys={}; filterObjects={}; end
    key=sprintf('%.17g,%.17g,%.17g',fs,band(1),band(2));
    filterIndex=find(strcmp(filterKeys,key),1);
    if isempty(filterIndex)
'''+design+'''        filterKeys{end+1}=key; filterObjects{end+1}=d;
    else
        d=filterObjects{filterIndex};
    end
'''
cached=cached[:start]+cache+cached[end:]
(S/'rd_apc_cached.m').write_text(cached)
(D/'filter_cache.patch').write_text(''.join(difflib.unified_diff(base.splitlines(True),cached.splitlines(True),fromfile='instrumented',tofile='cached')))
# Source-backed historical Step 4 candidate; all other pipeline steps preserved.
debug=(S/'debug_apc_matlab_case.m').read_text(encoding='utf-8-sig')
historical=base.replace('= rd_apc_instrumented(', '= rd_apc_historical_candidate(',1)
start=historical.index('function [ampFreq, ampWidth, selectionRoute] = estimate_amplitude_frequency(')
end=historical.index('\nfunction ',start+1)
adapter='''function [ampFreq, ampWidth, selectionRoute] = estimate_amplitude_frequency(signal,troughLocs,meanEpoch,meanTf,freqs,fs,phaseFreq,inputBand,candidateBandWidthHz) %#ok<INUSD>
    [ampFreq,~,~,fallbackTrace]=estimate_amplitude_frequency_debug(signal,troughLocs,meanEpoch,meanTf,freqs,fs,phaseFreq,inputBand);
    ampWidth=12;
    if isempty(fallbackTrace), selectionRoute="direct_envelope_scan"; else, selectionRoute="tf_fallback"; end
end

'''
historical=historical[:start]+adapter+historical[end:]
historical+='\n'+debug[debug.index('function [fa, scoreTrace, candidateFreqs, fallbackTrace] = estimate_amplitude_frequency_debug'):]
historical=historical.replace('highHz = min([inputBand(2), centerHz + halfWidth, fs / 2 - eps]);','highHz = min([centerHz + halfWidth, fs / 2 - 1]);')
(S/'rd_apc_historical_candidate.m').write_text(historical)
(D/'historical_candidate.patch').write_text(''.join(difflib.unified_diff(base.splitlines(True),historical.splitlines(True),fromfile='preserved_plus_logging',tofile='historical_step4_candidate')))
print('Created caching copy and June-source Step 4 candidate; protected originals recorded.')
