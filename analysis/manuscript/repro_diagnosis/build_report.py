"""Build factual diagnosis from completed MATLAB comparisons and source inventory."""
from pathlib import Path
from datetime import datetime
from collections import Counter,defaultdict
import csv,json,hashlib,difflib,statistics,re
D=Path(__file__).resolve().parent;R=D.parents[1]
def read(name):
    with (D/name).open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def write(name,rows):
    with (D/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def table(headers,rows):
    def esc(value):return str(value).replace('|','\\|')
    return '\n'.join(['| '+' | '.join(map(esc,headers))+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(esc,r))+' |' for r in rows])+'\n'
def n(rows,key):return sum(int(r[key]) for r in rows)
def fmt(x):return f'{x:g}'
def link(path,label=None):
    p=Path(path);return f'[{label or p.name}](<{p.as_posix()}>)'
def j(name):return json.loads((D/name).read_text(encoding='utf-8'))
rows=read('per_trial_comparison.csv');assert len(rows)==350
groups=defaultdict(list)
for row in rows:groups[(row['benchmark'],float(row['level']))].append(row)
assert len(groups)==14 and all(len(v)==25 for v in groups.values())
assert len({(r['benchmark'],r['level'],r['repeat_index']) for r in rows})==350
for r in rows:
    assert float(r['saved_minus_reproduced_fA_hz'])==float(r['saved_fA_hz'])-float(r['reproduced_fA_hz'])
    for prefix,col in [('fA','fA_hz'),('C_APC','C_APC'),('fP','fP_hz')]:
        assert bool(int(r[prefix+'_exact_equal']))==(float(r['saved_'+col])==float(r['reproduced_'+col]))
summary=[];hist=[];matchrows=[];accuracy=[];routes=[];distrows=[]
for (bench,lev),rr in groups.items():
    delta=[float(r['saved_minus_reproduced_fA_hz']) for r in rr];counts=Counter(delta)
    cmax=max(abs(float(r['saved_minus_reproduced_C_APC'])) for r in rr)
    item={'benchmark':bench,'level':lev,'n_trials':25,'fA_exact_matches':n(rr,'fA_exact_equal'),
        'C_APC_exact_matches':n(rr,'C_APC_exact_equal'),'fP_exact_matches':n(rr,'fP_exact_equal'),
        'C_APC_tolerance_matches_1e_12':n(rr,'C_APC_equal_within_1e_12'),
        'saved_fA_within_8':n(rr,'saved_fA_within_8_Hz_of_120'),'reproduced_fA_within_8':n(rr,'reproduced_fA_within_8_Hz_of_120'),
        'saved_joint_recovery':n(rr,'saved_joint_recovery'),'reproduced_joint_recovery':n(rr,'reproduced_joint_recovery'),
        'delta_fA_min':min(delta),'delta_fA_max':max(delta),'delta_fA_mean':statistics.mean(delta),'delta_fA_median':statistics.median(delta),
        'max_abs_C_APC_difference':cmax,'direct_envelope_scan_count':sum(r['reproduced_selection_route']=='direct_envelope_scan' for r in rr),
        'tf_fallback_count':sum(r['reproduced_selection_route']=='tf_fallback' for r in rr)}
    summary.append(item)
    matchrows.append([bench,fmt(lev),item['fA_exact_matches'],item['C_APC_exact_matches'],item['fP_exact_matches'],f'{cmax:.9g}'])
    accuracy.append([bench,fmt(lev),item['saved_fA_within_8'],item['reproduced_fA_within_8'],item['saved_joint_recovery'],item['reproduced_joint_recovery']])
    routes.append([bench,fmt(lev),item['direct_envelope_scan_count'],item['tf_fallback_count'],'Not recorded'])
    distrows.append([bench,fmt(lev),f'{min(delta):g} to {max(delta):g}',f'{statistics.mean(delta):.2f}',f'{statistics.median(delta):g}', '; '.join(f'{k:g}: {v}' for k,v in sorted(counts.items()))])
    hist.extend({'benchmark':bench,'level':lev,'saved_minus_reproduced_fA_hz':k,'trial_count':v} for k,v in sorted(counts.items()))
write('per_level_summary.csv',summary);write('fA_difference_distribution.csv',hist)
candidates={name:read(name+'_comparison.csv') for name in ['historical_candidate','historical_clipped_candidate']}
assert all(len(v)==25 for v in candidates.values())
endpoint=groups['sparsity',.15]
candidate_rows=[]
for title,rr in [('Preserved baseline',endpoint),('June selector + June final band',candidates['historical_candidate']),('June selector + preserved final-band clipping',candidates['historical_clipped_candidate'])]:
    candidate_rows.append([title,n(rr,'reproduced_joint_recovery' if title=='Preserved baseline' else 'candidate_joint_recovery'),n(rr,'fA_exact_equal'),n(rr,'fP_exact_equal'),n(rr,'C_APC_exact_equal'),n(rr,'C_APC_equal_within_1e_12')])
protected=j('protected_input_hashes.json');integrity=[]
for path,expected in protected.items():
    actual=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    integrity.append({'path':path,'sha256_before':expected,'sha256_after':actual,'unchanged':actual==expected})
assert all(r['unchanged'] for r in integrity)
(D/'protected_input_verification.json').write_text(json.dumps(integrity,indent=2))
metadata=j('result_files_metadata.json');all_files=[]
for m in metadata:
    for p in R.rglob(Path(m['path']).name):
        if D in p.parents:continue
        stat=p.stat();all_files.append({'path':str(p),'created_local':datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified_local':datetime.fromtimestamp(stat.st_mtime).isoformat(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
write('saved_result_copy_timestamps.csv',all_files)
sources=j('additional_source_metadata.json')
source_table=[[link(r['path']),datetime.fromtimestamp(r['mtime_epoch']).isoformat(sep=' ',timespec='seconds'),r['sha256']] for r in sources]
git=j('git_history.json');commits=sorted(git['relevant_commits'],key=lambda x:x['committer_date'])
def function_text(s,name):
    starts=list(re.finditer(r'^function\s+.*$',s,re.M))
    for i,m in enumerate(starts):
        if re.search(r'\b'+re.escape(name)+r'\s*\(',m.group()):
            return s[m.start():starts[i+1].start() if i+1<len(starts) else len(s)]
    raise AssertionError(name)
comparisons=j('step3_step4_function_comparison.json')
base=(D/'sources/bst_apc.m').read_text(encoding='utf-8-sig')
versions={'preserved_baseline':base,'current_root':(R/'bst_apc.m').read_text(encoding='utf-8-sig')}
versions.update({c['hash']:Path(c['files']['src/bst_apc.m']['copy']).read_text(encoding='utf-8-sig') for c in commits})
for label,source in versions.items():
    for name in ['get_phase_band','detect_peaks_with_defaults']:
        aa=function_text(base,name);bb=function_text(source,name);assert aa==bb
        if not any(x['version']==label and x['function']==name for x in comparisons):
            comparisons.append({'version':label,'function':name,'baseline_present':True,'version_present':True,'text_equal':True,
                'baseline_sha256':hashlib.sha256(aa.encode()).hexdigest(),'version_sha256':hashlib.sha256(bb.encode()).hexdigest()})
(D/'step3_step4_function_comparison.json').write_text(json.dumps(comparisons,indent=2))
headers=[]
for m in metadata:
    if m['path'].endswith('.mat'):
        headers.append({'path':m['path'],'first_116_bytes_ascii':Path(m['path']).read_bytes()[:116].decode('ascii',errors='replace').rstrip()})
(D/'mat_headers.json').write_text(json.dumps(headers,indent=2))
gitrows=[]
for c in commits:
    touched='Adds bst_apc.m and calc_MI_all_methods.m' if c['hash'].startswith('82f') else 'Modifies bst_apc.m; calc_MI_all_methods.m unchanged'
    gitrows.append([c['hash'],c['author_date'],c['committer_date'],touched,'Reflog/unreachable commit' if c['hash'].startswith('590') else 'Reachable commit'])
a=(D/'sources/82f7559fd570_bst_apc.m').read_text(encoding='utf-8-sig');b=(D/'sources/57bcd5d2f3a8_bst_apc.m').read_text(encoding='utf-8-sig')
(D/'git_82_to_57_bst_apc.patch').write_text(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='82f7559fd570',tofile='57bcd5d2f3a8')))
runtime=j('results/runtime_cached.json');assert runtime['status']=='COMPLETE'
oldruntime=j('results/runtime.json');oldruntime['status']='STOPPED_FOR_CHECKPOINT_RESUME';oldruntime['continuation']='runtime_cached.json';oldruntime['stopped_worker_pid']=34676
(D/'results/runtime.json').write_text(json.dumps(oldruntime,indent=2))
lines=[]
def p(s=''):lines.append(s+'\n')
p('# APC reproduction diagnosis')
p(f'Generated {datetime.now().isoformat(sep=" ",timespec="seconds")} local time. Workspace: `{R}`. All new diagnostic artifacts are in `{D}`.')
p('## Findings')
p('All 350 APC trials were reproduced: seven sparsity keep rates and seven distractor levels, 25 trials per level. The preserved code has exact phase-frequency equality in 350/350 trials. All three requested outputs match exactly in all 175 distractor trials. For sparsity, amplitude frequencies match in 4/175 trials and coupling strengths in 0/175 trials.')
p('At keep rate 0.15, the June 16 amplitude-selection helper gives 12/25 joint recoveries and matches the 25 saved amplitude frequencies. With its original June final-band rule, 21/25 coupling strengths match. Combining that selector and 12 Hz width with the preserved final-band clipping gives exact equality for all 25 saved fA, fP and C_APC values. These are explicitly assembled diagnostic candidates, not recovered historical Git commits. The saved MAT files do not identify their generating source revision.')
p('## 1. All-level per-trial comparison')
p(f'The requested data are in {link(D/"per_trial_comparison.csv")}: 350 rows, one per APC trial, containing saved/reproduced fA, C_APC and fP, differences, exact-match flags, tolerance flags, recovery flags and reproduced selection route. Saved values come from the original MAT runTable doubles; comparisons use MATLAB `==`. The CSV uses 17 significant digits to preserve those doubles. C_APC is the raw `canolty` score, without surrogate normalization.')
p('Every table row below contains 25 trials. “Exact” means numeric equality of the original MAT doubles and reproduced doubles. The additional tolerance checks (1e-7 Hz for frequencies and 1e-12 for C_APC) give the same per-level match counts as exact equality in this baseline comparison.')
p(table(['Benchmark','Level','Exact fA /25','Exact C_APC /25','Exact fP /25','Max |saved−reproduced C_APC|'],matchrows))
p('Amplitude recovery uses the inclusive interval [112,128] Hz. Joint recovery additionally requires |fP−8| ≤ 1 Hz; these columns are kept separate because some higher-distractor trials fail the phase criterion.')
p(table(['Benchmark','Level','Saved fA within ±8 /25','Reproduced fA within ±8 /25','Saved joint /25','Reproduced joint /25'],accuracy))
p('**Distribution of saved fA − reproduced fA (Hz).** Each `difference: count` entry is an exact empirical frequency, and its row totals 25. Full machine-readable counts are in '+link(D/'fA_difference_distribution.csv')+'.')
p(table(['Benchmark','Level','Range (Hz)','Mean (Hz)','Median (Hz)','Difference: count'],distrows))
p('For distractor levels the offset is the constant zero. For sparsity the offset is not constant: it varies between trials at every level, and the empirical distributions differ across keep rates. This establishes trial variation and differing distributions by level. It does not establish that the differences themselves are random; no test of randomness or statistical level effect was performed.')
p('## 2. Git history, result dates and saved metadata')
p('The workspace root is not a Git repository. The three embedded repositories searched with `git log --all --reflog` and `git fsck --no-reflogs --unreachable` are:')
for repo in git['repositories']:p(f'- `{repo["repository"]}`')
p('The following is the complete set of distinct available commits touching `src/bst_apc.m` or its repository-owned Step 3–4 dependency `src/calc_MI_all_methods.m`. Other Step 3–4 helpers are local functions in bst_apc.m; MATLAB toolbox functions have no source history in these repositories.')
p(table(['Full commit hash','Author date','Committer date','Relevant files','Availability'],gitrows))
p('Commit subjects and repository membership are preserved in '+link(D/'git_history.json')+'. The earlier `49e05a9f540790b968099f1da657c7d9e39d3dc9` initial commit (2026-10-05 13:04:48 −04:00) contains neither method file and is not a method-source revision.')
p('Original result-file filesystem timestamps follow (local America/New_York, UTC−04:00 on these dates). File creation time and last-write time are distinct; they are not treated as interchangeable.')
p(table(['Original result path','Filesystem creation','Filesystem last modification'],[[link(m['path']),m['created_local'],m['modified_local']] for m in metadata]))
p('The original MAT headers independently state `Created on: Sun Jul 5 13:53:21 2026` (sparsity) and `Created on: Sun Oct 4 11:03:50 2026` (distractor), MATLAB 7.3, PCWIN64. The headers do not specify a MATLAB release. Header text and last-write times agree to the displayed second. Timestamps and hashes of all copies of these six result filenames found under the workspace are in '+link(D/'saved_result_copy_timestamps.csv')+'; copied-package timestamps are recorded separately from original MAT-header times.')
p('**Most recent commit before the original saved results:** none exists in the available histories. All available commits are dated October 5 or later, after both the original filesystem creation dates and the MAT-header creation dates. No pre-July-5 or pre-October-4 generating commit can be identified from these repositories.')
p('The original saved MAT variables and complete cfg contents were read directly and exported to '+link(D/'results/saved_mat_metadata.json')+'.')
p(table(['File','Saved top-level variables','Version / Step 4 provenance'],[
 ['Sparsity MAT','cfg, runTable, summaryTable','No source hash, commit, MATLAB release, normalized APC options or route flag'],
 ['Distractor MAT','cfg, runTable, summaryTable, oracleTable, oracleSummaryTable, oracleAucTable','No source hash, commit, MATLAB release, normalized APC options or route flag']]))
p('Both cfg structs record seed 20260618, fs 500 Hz, true fP 8 Hz, true fA 120 Hz, broad amplitude band [80,150] Hz, canolty metric, 25 repeats, ±1 Hz phase tolerance and ±8 Hz amplitude tolerance. Sparsity duration is 8 s and levels are [1,.85,.7,.55,.4,.25,.15]. Distractor duration is 6 s, distractor frequency is 96 Hz and scales are [0,.5,1,1.5,2,2.5,3]. Other simulation parameters are retained in the exported cfg.')
p('Both cfg structs also contain the comparator grids `phase_scan_hz=4:1:12` and `amplitude_scan_hz=80:8:152`. These are not the internal APC Step 4 grid. Distractor cfg records `phase_band_half_width_hz=1.5` and `amplitude_band_half_width_hz=6`; the benchmark uses these for the scanned/fixed comparators. Its `local_run_apc` does not pass them to bst_apc. Neither cfg records APC `amplitudeBandWidthHz`, its candidate-grid spacing or its fallback decision. The inspected runTable UserData, Description and VariableDescriptions are empty. The existing inference-summary text files report counts and interval methods without a source revision or APC Step 4 parameter log.')
p('An earlier, non-Git MATLAB Step 4 implementation was found in the following local sources. Their timestamps are filesystem metadata, not a record of which file generated the saved benchmarks.')
p(table(['Earlier source path','Last modification (local)','SHA-256'],source_table))
p('## 3. Step 3–4 code differences and truth-value checks')
p('The preserved `revision_checks/snapshot/bst_apc.m` is byte-identical to the full bst_apc.m blob at `82f7559fd570133bd05ec0a583299a50613ffc2a` (SHA-256 `6af6c8ce289c093e2a0b9460a3af180f26bebd896cd3a1da732b3e1c0acff750`). The root/current and both October 20 blobs have SHA-256 `4e7d11ac1af1d62af51d14edf1ac8851639767f78724ec8a58fbc5e88944ba78`. Every available calc_MI_all_methods.m blob has SHA-256 `22aed807d9c05fe528ed1c873481560c2392c41c5f6d7cc8af158da04dc193f9`.')
p('All available Git revisions have identical Step 3–4 function text: `get_phase_band`, `detect_peaks_with_defaults`, `detect_troughs`, `collect_phase_locked_tf`, `zscore_rows`, `bandpass_signal`, `estimate_amplitude_frequency`, `estimate_amplitude_frequency_tf_fallback`, `normalize_01`, `collect_event_epochs_by_index` and `get_amplitude_band`. Per-function hashes and equality flags are in '+link(D/'step3_step4_function_comparison.json')+'. The corresponding `step3_step4_diff_*.patch` files contain no changes. The whole-file October 5→October 20 diff is in '+link(D/'git_82_to_57_bst_apc.patch')+'; its numerical changes concern Step 2 phase estimation (detrending and a minimum-cycle bound), not Step 4.')
p('Step 3 in these versions filters the phase band with a fourth-order designfilt bandpass and filtfilt, detects troughs with a minimum separation of round(0.8 fs/fP) and prominence 0.25 SD, and averages edge-valid trough epochs extending ±3 phase cycles. Its CWT amplitude map covers [80,150] Hz with TimeBandwidth 20, takes magnitudes, z-scores each frequency row over the full signal and averages valid epochs.')
step4=[
 ['Candidate grid','80:1:150 (71 candidates)','80:4:150, append 150 (19 candidates)'],
 ['Candidate band half-width','2 Hz (default width 4 Hz), clipped to input band and fs/2−1','6 Hz, clipped only to [1,fs/2−1], not the input amplitude band'],
 ['Filter / envelope','designfilt bandpassiir, order 4; filtfilt; abs(hilbert)','Same designfilt order, filtfilt and Hilbert envelope'],
 ['Envelope time smoothing','None','None'],
 ['Direct xcorr max lag','min(round(0.8 fs/fP), epoch length−1); <1 bypasses direct scan','max(1,min(round(0.8 fs/fP), epoch length−1))'],
 ['Direct candidate score','max(abs(xcorr(demeaned mean envelope, demeaned mean epoch, lag, coeff)))','Same normalized max-absolute cross-correlation'],
 ['Direct score smoothing','Moving mean, min(5,number of candidates)','Same 5-candidate moving mean; grid spacing differs'],
 ['Direct selection / fallback trigger','Any finite smoothed score → argmax; fallback only if no finite score','Same finite-score trigger'],
 ['Early / empty input behavior','Empty signal, troughs or mean epoch return NaN before fallback','No equivalent early guard in June helper'],
 ['Fallback row score','Sum absolute normalized xcorr by native CWT row; if lag<1, mean absolute TF row','Sum absolute normalized xcorr; lag forced ≥1'],
 ['Fallback score/energy smoothing','5 native frequency bins each','7 native frequency bins each'],
 ['Fallback combination','Product of separately min-max-normalized coupling and mean-absolute TF energy; smooth 7 bins; native-frequency argmax','Same product and 7-bin final smoothing; argmax clipped to input band'],
 ['Fallback final width','max(2,diff(inputBand)/6) = 11.6666667 Hz','June main function uses 12 Hz final band'],
 ['Direct final amplitude filter','Width 4 Hz, minimum half-width 2 Hz; clipped to [inputBand low,inputBand high] and Nyquist','June main: [max(inputBand low,fA−6), min(fs/2−1,fA+6)]'],
 ['Fallback response to inaccurate fA','No truth/error/strength threshold triggers fallback','No truth/error/strength threshold triggers fallback']]
p(table(['Setting','Preserved and all available Git versions','June 16 debug implementation'],step4))
p('The June implementation is '+link(str(R/'debug_apc_matlab_case.m')+':264','debug_apc_matlab_case.m:264')+' (`estimate_amplitude_frequency_debug`), with final amplitude filtering in the same file near line 205. The direct selector and its called local helpers were copied verbatim into the first candidate. The standalone Python prototype also has a 4 Hz/±6 Hz scan, but uses FFT filtering; it was inspected, not run as the historical MATLAB candidate.')
p('**True fA / 120 Hz in selection:** none of the inspected bst_apc.m versions or their Step 3–4 helpers accepts the simulated true amplitude frequency, searches a literal 120 Hz target, or uses the recovery tolerance to select fA. Their benchmark APC options pass the broad band, epoch, phase estimator and metric; true_fa_hz is used by the signal generator and recovery evaluation. The fixed-pair oracle comparators intentionally receive the known true pair.')
p('A separate truth-dependent development recommendation exists in `test_apc_fa_alternatives.m`: it reads the case true_fa_hz, computes each method’s `abs_error_true_hz`, and `choose_best_method` (lines 125–143) recommends the method with the smallest true-frequency error, breaking ties by PAC strength. Its individual scan estimators do not receive true_fa_hz. This recommendation function is not called by bst_apc or by either benchmark APC wrapper. The truth-based recommendation was not used in any diagnostic rerun here.')
p('## 4. Actual fallback usage')
p('A copied implementation logs the branch at the direct return or entry to the TF fallback. The numeric computation statements are retained; instrumentation and cache patches are saved. These counts are observed execution routes, not inferred from whether fA was correct. All 350 reproduced status codes are zero.')
p(table(['Benchmark','Level','Direct envelope scan /25','TF fallback /25','Saved branch'],routes))
p('The saved MAT runTable columns contain no branch/selection-mode field. No saved direct/fallback counts can be reported. The June-selector endpoint rerun also used the direct scan in all 25 trials (and the clipped candidate did likewise).')
p('## 5. Historical-candidate endpoint reruns')
p('No earlier Git Step 4 differs from the preserved source. The earliest Git blob is exactly the preserved source and therefore is already covered by the baseline rerun. The June 16 helper is a source-backed alternative outside Git. Two explicit combinations were tested at keep rate 0.15 on the original seed/order, without truth-informed selection:')
p('1. Preserved Steps 1–3 and final metric, June Step 4 selector and its 12 Hz final filter rule. This is '+link(D/'sources/rd_apc_historical_candidate.m')+' and '+link(D/'historical_candidate.patch')+'.')
p('2. The same June selector and 12 Hz width, with the preserved get_amplitude_band clipping to [80,150] Hz. This is '+link(D/'sources/rd_apc_historical_clipped_candidate.m')+' and '+link(D/'historical_clipped_candidate.patch')+'. This combination is not claimed to be an intact historical source file or a proven generating version.')
p(table(['Endpoint implementation','Joint recovery /25','Exact saved fA /25','Exact saved fP /25','Exact saved C_APC /25','C_APC within 1e-12 /25'],candidate_rows))
p('With the June final filter rule, the four C_APC mismatches occur at trials 5, 8, 9 and 16, whose fA values are 148,150,150,150 Hz. Their final filter upper edges are 154 or 156 Hz. With preserved final-band clipping the upper edge is 150 Hz and the rerun matches those four saved C_APC values as well. The selector returns the same fA values in both candidates.')
base_by_trial={int(r['repeat_index']):r for r in endpoint};clip_by_trial={int(r['repeat_index']):r for r in candidates['historical_clipped_candidate']}
p(table(['Trial','Saved fA (Hz)','Preserved fA (Hz)','June candidate fA (Hz)','Clipped candidate C_APC exact'],[[i,fmt(float(clip_by_trial[i]['saved_fA_hz'])),fmt(float(base_by_trial[i]['reproduced_fA_hz'])),fmt(float(clip_by_trial[i]['candidate_fA_hz'])),clip_by_trial[i]['C_APC_exact_equal']] for i in range(1,26)]))
p('Full-precision endpoint comparisons: '+link(D/'historical_candidate_comparison.csv')+' and '+link(D/'historical_clipped_candidate_comparison.csv')+'. Equality at this endpoint does not establish the generating revision for other sparsity levels; the alternative was rerun only for the requested 0.15 endpoint.')
p('## Execution and preservation record')
p(f'MATLAB {runtime["matlab_version"]}; one computation thread. The archived generator/noise prefixes and all their local helper functions were copied into the diagnostic folder. The seed is reset separately for each benchmark and all levels/trials are generated in original order, including the distractor null-signal draws. APC analysis was checked not to consume RNG state in each executed trial. Deterministic comparators were not rerun in this diagnosis; the 125 overlapping prior APC trials were checked against the earlier reproduction with 1e-7 Hz / 1e-12 score tolerances.')
p('A route-only copied implementation was checked against the unmodified preserved function with exact equality of the whole exported struct. To avoid redesigning identical IIR filters on every trial, a second diagnostic copy memoizes designfilt objects by the exact fs and band edges while retaining filtfilt and all numerical parameters. Three uncached/cached trials matched their entire exported structs and routes exactly; first and final newly executed trials in each benchmark were additionally checked against the unmodified source. The uncached first 25 sparsity trials were retained via checkpoint; the remaining trials used this checked cache. Cache checks are in '+link(D/'results/cache_validation.csv')+', and source changes in '+link(D/'instrumentation.patch')+' and '+link(D/'filter_cache.patch')+'.')
p('The initial diagnostic worker was intentionally stopped after its checkpoint and resumed with the checked cache; its old runtime record is marked STOPPED_FOR_CHECKPOINT_RESUME. The completed continuation is '+link(D/'results/runtime_cached.json')+'. Checkpoints, generated inputs, full-precision paired MAT values and logs are under `results/`. The clipped candidate uses the same exact filter-object caching approach.')
p(f'SHA-256 verification passed for all {len(integrity)} protected original files, including manuscript, source files, saved benchmark results and earlier reproduction snapshots. No existing source or saved result was modified. Verification: '+link(D/'protected_input_verification.json')+'.')
p('No manuscript edits, benchmark sensitivity experiments or new algorithm additions were applied outside this diagnostic folder.')
(D/'DIAGNOSIS.md').write_text('\n'.join(lines),encoding='utf-8')
print('Wrote DIAGNOSIS.md, 350-trial CSV, 14-level summary, distributions and integrity verification.')
print('Protected originals unchanged:',len(integrity))
print('Endpoint candidate rows:',candidate_rows)
