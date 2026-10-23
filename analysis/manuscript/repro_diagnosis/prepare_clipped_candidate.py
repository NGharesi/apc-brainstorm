from pathlib import Path
import difflib
D=Path(__file__).resolve().parent;S=D/'sources'
a=(S/'rd_apc_historical_candidate.m').read_text()
b=a.replace('= rd_apc_historical_candidate(', '= rd_apc_historical_clipped_candidate(',1)
b=b.replace('highHz = min([centerHz + halfWidth, fs / 2 - 1]);','highHz = min([inputBand(2), centerHz + halfWidth, fs / 2 - eps]);')
# Memoize the same designfilt call in both local filtering helpers.
needle="    d = designfilt( ...\n        'bandpassiir', ...\n        'FilterOrder', 4, ...\n        'HalfPowerFrequency1', band(1), ...\n        'HalfPowerFrequency2', band(2), ...\n        'SampleRate', fs);"
assert b.count(needle)==2
b=b.replace(needle,'    d = rd_cached_designfilt(fs,band);')
(S/'rd_apc_historical_clipped_candidate.m').write_text(b)
(D/'historical_clipped_candidate.patch').write_text(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='June_final_band',tofile='preserved_final_band_clipping_plus_filter_cache')))
s=(D/'rd_candidate_endpoint.m').read_text().replace('rd_candidate_endpoint(d)','rd_clipped_candidate_endpoint(d)',1)
s=s.replace('rd_apc_historical_candidate(', 'rd_apc_historical_clipped_candidate(')
s=s.replace('historical_candidate_endpoint','historical_clipped_candidate_endpoint').replace('JUNE STEP4 CANDIDATE','JUNE STEP4 + PRESERVED FINAL BAND')
(D/'rd_clipped_candidate_endpoint.m').write_text(s)
(D/'run_clipped_candidate_endpoint.m').write_text("d=fileparts(mfilename('fullpath'));addpath(d);rd_clipped_candidate_endpoint(d);\n")
print('Prepared source combination: June selection/12-Hz width, preserved final-band clipping.')
