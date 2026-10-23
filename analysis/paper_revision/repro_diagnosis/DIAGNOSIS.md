# APC reproduction diagnosis

Generated 2026-10-21 23:08:47 local time. Workspace: `C:\Users\nghare\.brainstorm\process`. All new diagnostic artifacts are in `C:\Users\nghare\.brainstorm\process\revision_checks\repro_diagnosis`.

## Findings

All 350 APC trials were reproduced: seven sparsity keep rates and seven distractor levels, 25 trials per level. The preserved code has exact phase-frequency equality in 350/350 trials. All three requested outputs match exactly in all 175 distractor trials. For sparsity, amplitude frequencies match in 4/175 trials and coupling strengths in 0/175 trials.

At keep rate 0.15, the June 16 amplitude-selection helper gives 12/25 joint recoveries and matches the 25 saved amplitude frequencies. With its original June final-band rule, 21/25 coupling strengths match. Combining that selector and 12 Hz width with the preserved final-band clipping gives exact equality for all 25 saved fA, fP and C_APC values. These are explicitly assembled diagnostic candidates, not recovered historical Git commits. The saved MAT files do not identify their generating source revision.

## 1. All-level per-trial comparison

The requested data are in [per_trial_comparison.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/per_trial_comparison.csv>): 350 rows, one per APC trial, containing saved/reproduced fA, C_APC and fP, differences, exact-match flags, tolerance flags, recovery flags and reproduced selection route. Saved values come from the original MAT runTable doubles; comparisons use MATLAB `==`. The CSV uses 17 significant digits to preserve those doubles. C_APC is the raw `canolty` score, without surrogate normalization.

Every table row below contains 25 trials. “Exact” means numeric equality of the original MAT doubles and reproduced doubles. The additional tolerance checks (1e-7 Hz for frequencies and 1e-12 for C_APC) give the same per-level match counts as exact equality in this baseline comparison.

| Benchmark | Level | Exact fA /25 | Exact C_APC /25 | Exact fP /25 | Max \|saved−reproduced C_APC\| |
| --- | --- | --- | --- | --- | --- |
| sparsity | 1 | 2 | 0 | 25 | 0.057601873 |
| sparsity | 0.85 | 0 | 0 | 25 | 0.0534373604 |
| sparsity | 0.7 | 0 | 0 | 25 | 0.0455021565 |
| sparsity | 0.55 | 1 | 0 | 25 | 0.0386015348 |
| sparsity | 0.4 | 1 | 0 | 25 | 0.0309152799 |
| sparsity | 0.25 | 0 | 0 | 25 | 0.0224087052 |
| sparsity | 0.15 | 0 | 0 | 25 | 0.0153932799 |
| distractor | 0 | 25 | 25 | 25 | 0 |
| distractor | 0.5 | 25 | 25 | 25 | 0 |
| distractor | 1 | 25 | 25 | 25 | 0 |
| distractor | 1.5 | 25 | 25 | 25 | 0 |
| distractor | 2 | 25 | 25 | 25 | 0 |
| distractor | 2.5 | 25 | 25 | 25 | 0 |
| distractor | 3 | 25 | 25 | 25 | 0 |


Amplitude recovery uses the inclusive interval [112,128] Hz. Joint recovery additionally requires |fP−8| ≤ 1 Hz; these columns are kept separate because some higher-distractor trials fail the phase criterion.

| Benchmark | Level | Saved fA within ±8 /25 | Reproduced fA within ±8 /25 | Saved joint /25 | Reproduced joint /25 |
| --- | --- | --- | --- | --- | --- |
| sparsity | 1 | 25 | 24 | 25 | 24 |
| sparsity | 0.85 | 24 | 22 | 24 | 22 |
| sparsity | 0.7 | 24 | 20 | 24 | 20 |
| sparsity | 0.55 | 21 | 20 | 21 | 20 |
| sparsity | 0.4 | 22 | 16 | 22 | 16 |
| sparsity | 0.25 | 11 | 4 | 11 | 4 |
| sparsity | 0.15 | 12 | 6 | 12 | 6 |
| distractor | 0 | 24 | 24 | 24 | 24 |
| distractor | 0.5 | 24 | 24 | 24 | 24 |
| distractor | 1 | 22 | 22 | 22 | 22 |
| distractor | 1.5 | 25 | 25 | 24 | 24 |
| distractor | 2 | 19 | 19 | 19 | 19 |
| distractor | 2.5 | 22 | 22 | 20 | 20 |
| distractor | 3 | 17 | 17 | 17 | 17 |


**Distribution of saved fA − reproduced fA (Hz).** Each `difference: count` entry is an exact empirical frequency, and its row totals 25. Full machine-readable counts are in [fA_difference_distribution.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/fA_difference_distribution.csv>).

| Benchmark | Level | Range (Hz) | Mean (Hz) | Median (Hz) | Difference: count |
| --- | --- | --- | --- | --- | --- |
| sparsity | 1 | -5 to 8 | -0.40 | -2 | -5: 6; -4: 6; -2: 1; -1: 1; 0: 2; 4: 2; 5: 5; 6: 1; 8: 1 |
| sparsity | 0.85 | -51 to 22 | -1.72 | -4 | -51: 1; -13: 1; -11: 1; -8: 1; -7: 1; -6: 1; -5: 5; -4: 2; 2: 1; 5: 5; 6: 1; 7: 2; 8: 1; 9: 1; 22: 1 |
| sparsity | 0.7 | -22 to 17 | -2.20 | -5 | -22: 1; -14: 1; -9: 2; -7: 2; -6: 4; -5: 5; -4: 1; 4: 1; 5: 2; 6: 2; 7: 1; 8: 2; 17: 1 |
| sparsity | 0.55 | -33 to 40 | 2.44 | 4 | -33: 1; -26: 1; -8: 2; -6: 3; -5: 1; -4: 2; -3: 1; 0: 1; 4: 3; 5: 2; 6: 1; 10: 2; 16: 1; 17: 1; 24: 1; 25: 1; 40: 1 |
| sparsity | 0.4 | -32 to 48 | -3.28 | -4 | -32: 1; -30: 1; -29: 1; -27: 1; -23: 1; -22: 1; -15: 1; -10: 2; -8: 1; -4: 3; 0: 1; 1: 1; 4: 2; 7: 4; 8: 1; 12: 1; 31: 1; 48: 1 |
| sparsity | 0.25 | -61 to 51 | -1.88 | -4 | -61: 1; -55: 1; -38: 1; -26: 1; -24: 1; -16: 1; -15: 1; -12: 2; -9: 1; -8: 1; -6: 1; -4: 1; 5: 2; 6: 2; 7: 1; 8: 1; 16: 1; 23: 1; 31: 1; 37: 1; 44: 1; 51: 1 |
| sparsity | 0.15 | -58 to 35 | -0.44 | -4 | -58: 1; -31: 1; -20: 1; -19: 1; -17: 1; -14: 1; -11: 1; -10: 1; -9: 3; -8: 1; -4: 1; 3: 1; 6: 1; 8: 1; 9: 1; 11: 2; 19: 1; 21: 1; 26: 1; 27: 1; 32: 1; 35: 1 |
| distractor | 0 | 0 to 0 | 0.00 | 0 | 0: 25 |
| distractor | 0.5 | 0 to 0 | 0.00 | 0 | 0: 25 |
| distractor | 1 | 0 to 0 | 0.00 | 0 | 0: 25 |
| distractor | 1.5 | 0 to 0 | 0.00 | 0 | 0: 25 |
| distractor | 2 | 0 to 0 | 0.00 | 0 | 0: 25 |
| distractor | 2.5 | 0 to 0 | 0.00 | 0 | 0: 25 |
| distractor | 3 | 0 to 0 | 0.00 | 0 | 0: 25 |


For distractor levels the offset is the constant zero. For sparsity the offset is not constant: it varies between trials at every level, and the empirical distributions differ across keep rates. This establishes trial variation and differing distributions by level. It does not establish that the differences themselves are random; no test of randomness or statistical level effect was performed.

## 2. Git history, result dates and saved metadata

The workspace root is not a Git repository. The three embedded repositories searched with `git log --all --reflog` and `git fsck --no-reflogs --unreachable` are:

- `C:\Users\nghare\.brainstorm\process\apc-brainstorm-publish`

- `C:\Users\nghare\.brainstorm\process\APC_NeuroImage_Submission_Package_2026-10-10\code\apc-brainstorm`

- `C:\Users\nghare\.brainstorm\process\APC_NeuroImage_Submission_Package_2026-10-10\APC_NeuroImage_Submission_Package_2026-10-10\code\apc-brainstorm`

The following is the complete set of distinct available commits touching `src/bst_apc.m` or its repository-owned Step 3–4 dependency `src/calc_MI_all_methods.m`. Other Step 3–4 helpers are local functions in bst_apc.m; MATLAB toolbox functions have no source history in these repositories.

| Full commit hash | Author date | Committer date | Relevant files | Availability |
| --- | --- | --- | --- | --- |
| 82f7559fd570133bd05ec0a583299a50613ffc2a | 2026-10-05T13:20:06-04:00 | 2026-10-05T13:20:06-04:00 | Adds bst_apc.m and calc_MI_all_methods.m | Reachable commit |
| 5903ac94ddd800d59c90242dbe59df3682b39dd2 | 2026-10-20T03:06:25Z | 2026-10-20T03:06:25Z | Modifies bst_apc.m; calc_MI_all_methods.m unchanged | Reflog/unreachable commit |
| 57bcd5d2f3a8812e6fb87d442f250ff348b73646 | 2026-10-20T03:06:25Z | 2026-10-20T03:06:50Z | Modifies bst_apc.m; calc_MI_all_methods.m unchanged | Reachable commit |


Commit subjects and repository membership are preserved in [git_history.json](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/git_history.json>). The earlier `49e05a9f540790b968099f1da657c7d9e39d3dc9` initial commit (2026-10-05 13:04:48 −04:00) contains neither method file and is not a method-source revision.

Original result-file filesystem timestamps follow (local America/New_York, UTC−04:00 on these dates). File creation time and last-write time are distinct; they are not treated as interchangeable.

| Original result path | Filesystem creation | Filesystem last modification |
| --- | --- | --- |
| [apc_burst_sparsity_runs_full.csv](<C:/Users/nghare/.brainstorm/process/apc_burst_sparsity_runs_full.csv>) | 2026-06-18T11:24:32.636783 | 2026-07-05T13:53:21.446451 |
| [apc_burst_sparsity_summary_full.csv](<C:/Users/nghare/.brainstorm/process/apc_burst_sparsity_summary_full.csv>) | 2026-06-18T11:24:32.666540 | 2026-07-05T13:53:21.446451 |
| [apc_burst_sparsity_benchmark_full.mat](<C:/Users/nghare/.brainstorm/process/apc_burst_sparsity_benchmark_full.mat>) | 2026-06-18T11:24:32.602277 | 2026-07-05T13:53:21.430721 |
| [apc_distractor_frequency_runs_reviewer_control.csv](<C:/Users/nghare/.brainstorm/process/apc_distractor_frequency_runs_reviewer_control.csv>) | 2026-10-02T09:33:00.488031 | 2026-10-04T11:03:50.499368 |
| [apc_distractor_frequency_summary_reviewer_control.csv](<C:/Users/nghare/.brainstorm/process/apc_distractor_frequency_summary_reviewer_control.csv>) | 2026-10-02T09:33:00.599878 | 2026-10-04T11:03:50.504367 |
| [apc_distractor_frequency_benchmark_reviewer_control.mat](<C:/Users/nghare/.brainstorm/process/apc_distractor_frequency_benchmark_reviewer_control.mat>) | 2026-10-02T09:33:00.274843 | 2026-10-04T11:03:50.476379 |


The original MAT headers independently state `Created on: Sun Jul 5 13:53:21 2026` (sparsity) and `Created on: Sun Oct 4 11:03:50 2026` (distractor), MATLAB 7.3, PCWIN64. The headers do not specify a MATLAB release. Header text and last-write times agree to the displayed second. Timestamps and hashes of all copies of these six result filenames found under the workspace are in [saved_result_copy_timestamps.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/saved_result_copy_timestamps.csv>); copied-package timestamps are recorded separately from original MAT-header times.

**Most recent commit before the original saved results:** none exists in the available histories. All available commits are dated October 5 or later, after both the original filesystem creation dates and the MAT-header creation dates. No pre-July-5 or pre-October-4 generating commit can be identified from these repositories.

The original saved MAT variables and complete cfg contents were read directly and exported to [saved_mat_metadata.json](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/results/saved_mat_metadata.json>).

| File | Saved top-level variables | Version / Step 4 provenance |
| --- | --- | --- |
| Sparsity MAT | cfg, runTable, summaryTable | No source hash, commit, MATLAB release, normalized APC options or route flag |
| Distractor MAT | cfg, runTable, summaryTable, oracleTable, oracleSummaryTable, oracleAucTable | No source hash, commit, MATLAB release, normalized APC options or route flag |


Both cfg structs record seed 20260618, fs 500 Hz, true fP 8 Hz, true fA 120 Hz, broad amplitude band [80,150] Hz, canolty metric, 25 repeats, ±1 Hz phase tolerance and ±8 Hz amplitude tolerance. Sparsity duration is 8 s and levels are [1,.85,.7,.55,.4,.25,.15]. Distractor duration is 6 s, distractor frequency is 96 Hz and scales are [0,.5,1,1.5,2,2.5,3]. Other simulation parameters are retained in the exported cfg.

Both cfg structs also contain the comparator grids `phase_scan_hz=4:1:12` and `amplitude_scan_hz=80:8:152`. These are not the internal APC Step 4 grid. Distractor cfg records `phase_band_half_width_hz=1.5` and `amplitude_band_half_width_hz=6`; the benchmark uses these for the scanned/fixed comparators. Its `local_run_apc` does not pass them to bst_apc. Neither cfg records APC `amplitudeBandWidthHz`, its candidate-grid spacing or its fallback decision. The inspected runTable UserData, Description and VariableDescriptions are empty. The existing inference-summary text files report counts and interval methods without a source revision or APC Step 4 parameter log.

An earlier, non-Git MATLAB Step 4 implementation was found in the following local sources. Their timestamps are filesystem metadata, not a record of which file generated the saved benchmarks.

| Earlier source path | Last modification (local) | SHA-256 |
| --- | --- | --- |
| [debug_apc_matlab_case.m](<C:/Users/nghare/.brainstorm/process/debug_apc_matlab_case.m>) | 2026-06-16 13:25:42 | 8f649784d53e8a3d4e2b27d5715a01caf770200d5d8ea657173ec51c504e9ce0 |
| [test_apc_fa_alternatives.m](<C:/Users/nghare/.brainstorm/process/test_apc_fa_alternatives.m>) | 2026-06-16 13:22:08 | a7c9fcb7d0aca4fa010a9b4cdf8fe6e748e77e8a2081614ab22123a9268925a6 |
| [apc_simulation_study.py](<C:/Users/nghare/.brainstorm/process/apc_simulation_study.py>) | 2026-06-16 11:57:10 | d44387ab8534c9c47364602ed02e97c3f1f792941d7ab282b3aa9a8148eac59e |


## 3. Step 3–4 code differences and truth-value checks

The preserved `revision_checks/snapshot/bst_apc.m` is byte-identical to the full bst_apc.m blob at `82f7559fd570133bd05ec0a583299a50613ffc2a` (SHA-256 `6af6c8ce289c093e2a0b9460a3af180f26bebd896cd3a1da732b3e1c0acff750`). The root/current and both October 20 blobs have SHA-256 `4e7d11ac1af1d62af51d14edf1ac8851639767f78724ec8a58fbc5e88944ba78`. Every available calc_MI_all_methods.m blob has SHA-256 `22aed807d9c05fe528ed1c873481560c2392c41c5f6d7cc8af158da04dc193f9`.

All available Git revisions have identical Step 3–4 function text: `get_phase_band`, `detect_peaks_with_defaults`, `detect_troughs`, `collect_phase_locked_tf`, `zscore_rows`, `bandpass_signal`, `estimate_amplitude_frequency`, `estimate_amplitude_frequency_tf_fallback`, `normalize_01`, `collect_event_epochs_by_index` and `get_amplitude_band`. Per-function hashes and equality flags are in [step3_step4_function_comparison.json](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/step3_step4_function_comparison.json>). The corresponding `step3_step4_diff_*.patch` files contain no changes. The whole-file October 5→October 20 diff is in [git_82_to_57_bst_apc.patch](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/git_82_to_57_bst_apc.patch>); its numerical changes concern Step 2 phase estimation (detrending and a minimum-cycle bound), not Step 4.

Step 3 in these versions filters the phase band with a fourth-order designfilt bandpass and filtfilt, detects troughs with a minimum separation of round(0.8 fs/fP) and prominence 0.25 SD, and averages edge-valid trough epochs extending ±3 phase cycles. Its CWT amplitude map covers [80,150] Hz with TimeBandwidth 20, takes magnitudes, z-scores each frequency row over the full signal and averages valid epochs.

| Setting | Preserved and all available Git versions | June 16 debug implementation |
| --- | --- | --- |
| Candidate grid | 80:1:150 (71 candidates) | 80:4:150, append 150 (19 candidates) |
| Candidate band half-width | 2 Hz (default width 4 Hz), clipped to input band and fs/2−1 | 6 Hz, clipped only to [1,fs/2−1], not the input amplitude band |
| Filter / envelope | designfilt bandpassiir, order 4; filtfilt; abs(hilbert) | Same designfilt order, filtfilt and Hilbert envelope |
| Envelope time smoothing | None | None |
| Direct xcorr max lag | min(round(0.8 fs/fP), epoch length−1); <1 bypasses direct scan | max(1,min(round(0.8 fs/fP), epoch length−1)) |
| Direct candidate score | max(abs(xcorr(demeaned mean envelope, demeaned mean epoch, lag, coeff))) | Same normalized max-absolute cross-correlation |
| Direct score smoothing | Moving mean, min(5,number of candidates) | Same 5-candidate moving mean; grid spacing differs |
| Direct selection / fallback trigger | Any finite smoothed score → argmax; fallback only if no finite score | Same finite-score trigger |
| Early / empty input behavior | Empty signal, troughs or mean epoch return NaN before fallback | No equivalent early guard in June helper |
| Fallback row score | Sum absolute normalized xcorr by native CWT row; if lag<1, mean absolute TF row | Sum absolute normalized xcorr; lag forced ≥1 |
| Fallback score/energy smoothing | 5 native frequency bins each | 7 native frequency bins each |
| Fallback combination | Product of separately min-max-normalized coupling and mean-absolute TF energy; smooth 7 bins; native-frequency argmax | Same product and 7-bin final smoothing; argmax clipped to input band |
| Fallback final width | max(2,diff(inputBand)/6) = 11.6666667 Hz | June main function uses 12 Hz final band |
| Direct final amplitude filter | Width 4 Hz, minimum half-width 2 Hz; clipped to [inputBand low,inputBand high] and Nyquist | June main: [max(inputBand low,fA−6), min(fs/2−1,fA+6)] |
| Fallback response to inaccurate fA | No truth/error/strength threshold triggers fallback | No truth/error/strength threshold triggers fallback |


The June implementation is [debug_apc_matlab_case.m:264](<C:/Users/nghare/.brainstorm/process/debug_apc_matlab_case.m:264>) (`estimate_amplitude_frequency_debug`), with final amplitude filtering in the same file near line 205. The direct selector and its called local helpers were copied verbatim into the first candidate. The standalone Python prototype also has a 4 Hz/±6 Hz scan, but uses FFT filtering; it was inspected, not run as the historical MATLAB candidate.

**True fA / 120 Hz in selection:** none of the inspected bst_apc.m versions or their Step 3–4 helpers accepts the simulated true amplitude frequency, searches a literal 120 Hz target, or uses the recovery tolerance to select fA. Their benchmark APC options pass the broad band, epoch, phase estimator and metric; true_fa_hz is used by the signal generator and recovery evaluation. The fixed-pair oracle comparators intentionally receive the known true pair.

A separate truth-dependent development recommendation exists in `test_apc_fa_alternatives.m`: it reads the case true_fa_hz, computes each method’s `abs_error_true_hz`, and `choose_best_method` (lines 125–143) recommends the method with the smallest true-frequency error, breaking ties by PAC strength. Its individual scan estimators do not receive true_fa_hz. This recommendation function is not called by bst_apc or by either benchmark APC wrapper. The truth-based recommendation was not used in any diagnostic rerun here.

## 4. Actual fallback usage

A copied implementation logs the branch at the direct return or entry to the TF fallback. The numeric computation statements are retained; instrumentation and cache patches are saved. These counts are observed execution routes, not inferred from whether fA was correct. All 350 reproduced status codes are zero.

| Benchmark | Level | Direct envelope scan /25 | TF fallback /25 | Saved branch |
| --- | --- | --- | --- | --- |
| sparsity | 1 | 25 | 0 | Not recorded |
| sparsity | 0.85 | 25 | 0 | Not recorded |
| sparsity | 0.7 | 25 | 0 | Not recorded |
| sparsity | 0.55 | 25 | 0 | Not recorded |
| sparsity | 0.4 | 25 | 0 | Not recorded |
| sparsity | 0.25 | 25 | 0 | Not recorded |
| sparsity | 0.15 | 25 | 0 | Not recorded |
| distractor | 0 | 25 | 0 | Not recorded |
| distractor | 0.5 | 25 | 0 | Not recorded |
| distractor | 1 | 25 | 0 | Not recorded |
| distractor | 1.5 | 25 | 0 | Not recorded |
| distractor | 2 | 25 | 0 | Not recorded |
| distractor | 2.5 | 25 | 0 | Not recorded |
| distractor | 3 | 25 | 0 | Not recorded |


The saved MAT runTable columns contain no branch/selection-mode field. No saved direct/fallback counts can be reported. The June-selector endpoint rerun also used the direct scan in all 25 trials (and the clipped candidate did likewise).

## 5. Historical-candidate endpoint reruns

No earlier Git Step 4 differs from the preserved source. The earliest Git blob is exactly the preserved source and therefore is already covered by the baseline rerun. The June 16 helper is a source-backed alternative outside Git. Two explicit combinations were tested at keep rate 0.15 on the original seed/order, without truth-informed selection:

1. Preserved Steps 1–3 and final metric, June Step 4 selector and its 12 Hz final filter rule. This is [rd_apc_historical_candidate.m](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/sources/rd_apc_historical_candidate.m>) and [historical_candidate.patch](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/historical_candidate.patch>).

2. The same June selector and 12 Hz width, with the preserved get_amplitude_band clipping to [80,150] Hz. This is [rd_apc_historical_clipped_candidate.m](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/sources/rd_apc_historical_clipped_candidate.m>) and [historical_clipped_candidate.patch](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/historical_clipped_candidate.patch>). This combination is not claimed to be an intact historical source file or a proven generating version.

| Endpoint implementation | Joint recovery /25 | Exact saved fA /25 | Exact saved fP /25 | Exact saved C_APC /25 | C_APC within 1e-12 /25 |
| --- | --- | --- | --- | --- | --- |
| Preserved baseline | 6 | 0 | 25 | 0 | 0 |
| June selector + June final band | 12 | 25 | 25 | 21 | 21 |
| June selector + preserved final-band clipping | 12 | 25 | 25 | 25 | 25 |


With the June final filter rule, the four C_APC mismatches occur at trials 5, 8, 9 and 16, whose fA values are 148,150,150,150 Hz. Their final filter upper edges are 154 or 156 Hz. With preserved final-band clipping the upper edge is 150 Hz and the rerun matches those four saved C_APC values as well. The selector returns the same fA values in both candidates.

| Trial | Saved fA (Hz) | Preserved fA (Hz) | June candidate fA (Hz) | Clipped candidate C_APC exact |
| --- | --- | --- | --- | --- |
| 1 | 116 | 108 | 116 | 1 |
| 2 | 124 | 128 | 124 | 1 |
| 3 | 124 | 133 | 124 | 1 |
| 4 | 132 | 149 | 132 | 1 |
| 5 | 148 | 142 | 148 | 1 |
| 6 | 128 | 142 | 128 | 1 |
| 7 | 104 | 101 | 104 | 1 |
| 8 | 150 | 124 | 150 | 1 |
| 9 | 150 | 139 | 150 | 1 |
| 10 | 120 | 128 | 120 | 1 |
| 11 | 124 | 89 | 124 | 1 |
| 12 | 120 | 111 | 120 | 1 |
| 13 | 104 | 93 | 104 | 1 |
| 14 | 132 | 100 | 132 | 1 |
| 15 | 108 | 117 | 108 | 1 |
| 16 | 150 | 131 | 150 | 1 |
| 17 | 104 | 83 | 104 | 1 |
| 18 | 116 | 127 | 116 | 1 |
| 19 | 80 | 111 | 80 | 1 |
| 20 | 120 | 130 | 120 | 1 |
| 21 | 108 | 127 | 108 | 1 |
| 22 | 128 | 137 | 128 | 1 |
| 23 | 84 | 142 | 84 | 1 |
| 24 | 120 | 140 | 120 | 1 |
| 25 | 120 | 93 | 120 | 1 |


Full-precision endpoint comparisons: [historical_candidate_comparison.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/historical_candidate_comparison.csv>) and [historical_clipped_candidate_comparison.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/historical_clipped_candidate_comparison.csv>). Equality at this endpoint does not establish the generating revision for other sparsity levels; the alternative was rerun only for the requested 0.15 endpoint.

## Execution and preservation record

MATLAB 9.13.0.2105380 (R2022b) Update 2; one computation thread. The archived generator/noise prefixes and all their local helper functions were copied into the diagnostic folder. The seed is reset separately for each benchmark and all levels/trials are generated in original order, including the distractor null-signal draws. APC analysis was checked not to consume RNG state in each executed trial. Deterministic comparators were not rerun in this diagnosis; the 125 overlapping prior APC trials were checked against the earlier reproduction with 1e-7 Hz / 1e-12 score tolerances.

A route-only copied implementation was checked against the unmodified preserved function with exact equality of the whole exported struct. To avoid redesigning identical IIR filters on every trial, a second diagnostic copy memoizes designfilt objects by the exact fs and band edges while retaining filtfilt and all numerical parameters. Three uncached/cached trials matched their entire exported structs and routes exactly; first and final newly executed trials in each benchmark were additionally checked against the unmodified source. The uncached first 25 sparsity trials were retained via checkpoint; the remaining trials used this checked cache. Cache checks are in [cache_validation.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/results/cache_validation.csv>), and source changes in [instrumentation.patch](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/instrumentation.patch>) and [filter_cache.patch](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/filter_cache.patch>).

The initial diagnostic worker was intentionally stopped after its checkpoint and resumed with the checked cache; its old runtime record is marked STOPPED_FOR_CHECKPOINT_RESUME. The completed continuation is [runtime_cached.json](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/results/runtime_cached.json>). Checkpoints, generated inputs, full-precision paired MAT values and logs are under `results/`. The clipped candidate uses the same exact filter-object caching approach.

SHA-256 verification passed for all 20 protected original files, including manuscript, source files, saved benchmark results and earlier reproduction snapshots. No existing source or saved result was modified. Verification: [protected_input_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/repro_diagnosis/protected_input_verification.json>).

No manuscript edits, benchmark sensitivity experiments or new algorithm additions were applied outside this diagnostic folder.
