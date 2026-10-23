"""Current gate report; no endpoint inference before fixed contact choices."""
from pathlib import Path
import json,sys
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent;sys.path.insert(0,str(ROOT/'pydeps'))
import pandas as pd
def js(n):return json.loads((OUT/n).read_text(encoding='utf-8'))
def link(n,label=None):
    p=OUT/n
    return f'[{label or n}](<{p.as_posix()}>)'
def table(d,cols):
    def fmt(x):return f'{x:.14g}' if isinstance(x,float) else str(x)
    return '| '+' | '.join(cols)+' |\n| '+' | '.join('---' for _ in cols)+' |\n'+'\n'.join('| '+' | '.join(fmt(r[c]) for c in cols)+' |' for _,r in d.iterrows())+'\n'
meta=js('provenance.json');eq=pd.read_csv(OUT/'equivalence_both_attempts.csv',encoding='utf-8');ieeg=pd.read_csv(OUT/'native_ieeg_rate_summary.csv',encoding='utf-8');scalp=pd.read_csv(OUT/'native_scalp_rate_summary.csv',encoding='utf-8');t=js('timeline_gate_confirmation.json')
lines=['# ds004752 human iEEG: gates passed; analysis in progress','',
       'Both amendments were pushed before resumed dataset signal processing. Current HEAD `'+meta['git_head']+'`; protocol SHA-256 `'+meta['protocol_sha256']+'`. The repository was clean. Protocol, src and tagged code remain unchanged. No results have been committed.','',
       'The first attempt remains available in '+link('attempt1_archive/RESULTS_ieeg.md','archived attempt-1 report')+' and '+link('STOPPED_attempt1_sampling_rate.md')+'. Full source hashes, versions, seed and settings: '+link('provenance.json')+'.','',
       '## Equivalence gate: both attempts passed','',table(eq,['attempt','metric','expected','observed','absolute_difference','passed']),
       'The attempt-2 gate used the unchanged repository src copy, not frozen_v1. Its run preceded Amendment 2, which changes scalp processing only. Both results and their original run provenance are retained: '+link('equivalence_both_attempts.json')+'.','',
       '## Amended reading and resampling gates: PASS','',
       'All 68 iEEG files passed EDF/channels.tsv/JSON native-rate agreement, allowed rates, channel count/order, event sample count, exactly 8-s trials, finite samples, nonzero channel variance and median absolute values below 10^4 microvolts. Each trial produced exactly 16000 samples at 2000 Hz. Native iEEG rate table:',
       table(ieeg,['native_fs_hz','n_patients','n_sessions']),
       'All 68 scalp files passed header/sidecar rate agreement and native trial-length checks, with exactly 1600 samples per trial after Amendment-2 handling at 200 Hz. Native scalp table:',table(scalp,['native_fs_hz','n_patients','n_sessions','trials']),
       'Checks: '+link('edf_reading_gate_attempt2.json')+', '+link('edf_file_checks_attempt2.csv')+', '+link('edf_channel_checks_attempt2.csv')+', '+link('resampling_trial_checks_attempt2.csv')+', '+link('timeline_file_checks.csv')+', '+link('timeline_resampling_trial_checks.csv')+'.','',
       '## Trial timeline gate: PASS','',
       'The grand average uses every one of the 3353 trials from all 15 patients and all 68 sessions, averaging available O1/O2/Oz per trial. Each scalp trial was resampled separately to 200 Hz, then its fixation mean was subtracted; no additional signal filter was applied. Visual review confirms evoked negative deflections after both prespecified onsets.','',
       table(pd.DataFrame(t['peaks']),['expected_onset_s','peak_time_s','latency_ms','peak_uv','absolute_peak_difference_uv']),
       'Both peaks fall within 50-250 ms after the specified onsets, measured at 5-ms resolution. The paper task timings agree with fixation 0-1 s, encoding 1-3 s, maintenance 3-6 s, probe from 6 s. [Boran et al., Figure 1a](https://www.nature.com/articles/s41597-020-0364-3.pdf); [Dimakopoulos et al., task methods](https://elifesciences.org/articles/78677).','',
       'Timeline plot: '+link('timeline_grand_average.png','PNG')+'; '+link('timeline_grand_average.svg','SVG')+'. Source: '+link('timeline_grand_average.csv')+'. Confirmation: '+link('timeline_gate_confirmation.json')+'.','',
       '## Earlier screening NaN cause','',js('earlier_screening_nan_cause.json')['cause'],'',
       '## Current next step','',
       'Common trialwise iEEG resampling, mean removal, four-pole fourth-order SOS notch filtering and [3,6)-s input preparation are complete for all 62 sessions of the 14 patients with candidate pairs. Sub-13 has no hippocampal candidate and is excluded by metadata. No candidate spectra, contact choices, rejection masks, APC or scan outputs have been computed. Execution details: '+link('EXECUTION_notes_attempt2.md')+'; preprocessing runtime: '+link('preprocessing_runtime.json')+'.','',
       'A clarification is pending: section 3.3 ranks pairs using section 3.5 included trials, while section 3.5 defines rejection on the selected bipolar pair. The user was asked whether to derive a rejection mask independently for each candidate before ranking. Candidate ranking and dependent analyses remain pending that answer.','',
       '## Logged deviations and tooling errors','']
for d in js('deviations.json')['deviations']:lines.append('- '+d['type']+': '+d['reason'])
lines+=['','No endpoint decision, boundary/failure comparison or final four-panel endpoint figure is available yet. This is a gate/progress report, not the final statistical report.']
(OUT/'RESULTS_ieeg.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Current RESULTS_ieeg.md gate/progress report saved; no method outcomes')
