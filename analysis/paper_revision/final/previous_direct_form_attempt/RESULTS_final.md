# APC v1.0 final analysis — STOPPED

**Stopped under the requested method-relevant failure rule.** The rodent A2′ comparator phase-filter realization failed numerical verification. No comparator implementation was replaced, no tagged method code was changed, and no further analyses or figures were run after confirming the failure. This is a partial report, not a completed final-paper package.

Primary APC tag `v1.0`, commit `71ebc16aed32ca38be73a800738b975e5806b330`. Frozen files were extracted byte-for-byte into `final/frozen_v1`; all 24 rodent APC bouts and all four canonical APC examples completed with status 0 and exactly matched the diagnostic-export copy. The Git tree remains clean. v2.0 remains the previously reported negative result: C1 FAIL, C2 PASS, C3 FAIL, C4 FAIL.

## Method-relevant failure

The rodent scan uses `[b,a]=butter(4,band/(fs/2),"bandpass")` followed by `filtfilt(b,a,x)`, inherited from the existing comparators. The numerical check uses the first saved run bout at the stored approximately 1250-Hz sampling rate. It compares that realization with a second-order-section (SOS) realization of the same nominal Butterworth design; the SOS check was diagnostic only, not a replacement benchmark run.

| fP_hz | max_pole_ba | max_pole_zpk | center_gain_ba | center_gain_sos | rms_ba | rms_sos | relative_L2_difference |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 1.008193 | 0.9981358 | 1.416693 | 0.9999992 | 1.215628e+10 | 0.1397093 | 8.701125e+10 |
| 4.5 | 1.002049 | 0.9980192 | 1.225765 | 0.9999997 | 0.1601685 | 0.1448877 | 0.3232704 |
| 5 | 1.002121 | 0.9979267 | 1.161929 | 0.9999999 | 0.1572486 | 0.1607949 | 0.2012997 |
| 5.5 | 0.9991546 | 0.9978516 | 0.9982636 | 0.9999999 | 0.1837109 | 0.1895451 | 0.3396774 |
| 6 | 1.001316 | 0.9977894 | 0.7911704 | 1 | 0.2665232 | 0.2725142 | 0.3468242 |
| 6.5 | 0.9969785 | 0.997737 | 1.232254 | 1 | 0.3845048 | 0.3958403 | 0.2992599 |
| 7 | 0.9985123 | 0.9976922 | 1.131458 | 1 | 0.4839658 | 0.4796604 | 0.1823058 |
| 7.5 | 0.9965026 | 0.9976535 | 0.8588127 | 1 | 0.4658936 | 0.5111427 | 0.1555828 |
| 8 | 0.9973628 | 0.9976197 | 1.008178 | 1 | 0.5198148 | 0.5106923 | 0.07335038 |
| 8.5 | 0.9983392 | 0.9975899 | 1.035978 | 1 | 0.4921189 | 0.4908445 | 0.08055929 |
| 9 | 0.9977114 | 0.9975635 | 1.043501 | 1 | 0.4182078 | 0.4240716 | 0.103316 |
| 9.5 | 0.9970878 | 0.9975399 | 0.9415268 | 1 | 0.310694 | 0.2990595 | 0.1069227 |
| 10 | 0.9978428 | 0.9975186 | 1.007242 | 1 | 0.1746065 | 0.1722182 | 0.05794702 |
| 10.5 | 0.9978408 | 0.9974994 | 0.9887421 | 1 | 0.1237336 | 0.1244021 | 0.07707903 |
| 11 | 0.9973487 | 0.997482 | 1.012695 | 1 | 0.1027077 | 0.102432 | 0.07760437 |
| 11.5 | 0.9975186 | 0.9974661 | 1.020371 | 1 | 0.09074414 | 0.09021029 | 0.04077584 |
| 12 | 0.9976586 | 0.9974515 | 0.9925296 | 1 | 0.083341 | 0.08312507 | 0.07659269 |

At 4 Hz: direct-form maximum pole magnitude 1.00819340881, RMS 12156282752.3; SOS maximum pole magnitude 0.998135841668, RMS 0.139709316713. MATLAB also warned that the direct-form initial-condition matrix was nearly singular (RCOND 1.368249e-16). Audit: [rodent_filter_audit.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/rodent_filter_audit.csv>); [filter_audit_retry2_matlab.log](<C:/Users/nghare/.brainstorm/process/revision_checks/final/filter_audit_retry2_matlab.log>).

**All 96 rodent comparator rows and their 24 inferential rows are rejected for scientific use.** They remain preserved and explicitly flagged. The APC v1.0 method uses its unchanged designfilt phase filter and SOS amplitude filter; this audit does not identify a failure of that tagged method. The held-out comparator CSVs were not rerun or altered; this report makes no new numerical-validity claim about their different sampling-rate settings.

## Channel evidence

Analyzed signal: **R2, E1, Brainstorm row/channel 1 (one-based)** from EC013/ec013.157. R2.Description is E1; its Comment says `Extract values: [0.000s,631.199s] E1`. Its extraction History identifies `EC013/ec013.157.eeg/data_block001.mat`. The imported channel file names row 1 E1. R2 samples 40800:372501 match row 1 of the saved 65-channel crop `data_230118_2215.mat` exactly: 331,702 samples, maximum absolute difference 0. The crop Time restarts at zero.

**Shank, XML acquisition-channel index and anatomical layer are unresolved.** No session XML or explicit E1-to-shank/layer map was found in the inspected local LFP tree. The E1 channel record has empty Group and Comment and zero coordinates. E1 is not sufficient evidence for a zero-based acquisition index or anatomical layer. No shank number, CA1 label or layer is inferred. The original raw-file link points to `/Users/lucwilson/Desktop/crcns/hc3/ec013/ec013.157/ec013.157.eeg`, not a current local XML.

The public [CRCNS hc-3 page](https://crcns.org/data-sets/hc/hc-3) identifies the dataset but does not establish this E1 mapping. The [ec013.157 forum discussion](https://crcns.org/forum/using-datasets/593514207) concerns cell/shank labels and does not map E1. Local evidence is in [channel_evidence.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/channel_evidence.json>); inventory in [local_data_inspection.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/local_data_inspection.json>).

## Unchanged bouts and method settings

The existing 12 run and 12 rest bouts come directly from `apc_ec013_run_rest_results.mat`; all original start/stop indices and durations were retained. Original analysis interval: R2 indices 40800:372501; original speed criterion |speed|>6, minimum bout duration 5 s; approximately 1250 Hz. Definitions: [bout_definitions.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/bout_definitions.csv>).

APC v1.0: amplitude search [80,150] Hz; defaults otherwise, raw Canolty MVL without surrogate normalization. Ozkurt MVL = raw MVL / sqrt(mean(final amplitude envelope²)); preferred phase = angle(mean(A exp(i phase))) in degrees, from the same frozen final envelope/phase. The diagnostic copy exports arrays without changing calculations; its complete output and runInfo matched the untouched frozen function for every analyzed bout/example.

Requested rodent A2′ scans: phase grid 4:0.5:12 Hz, half-width 1.5 Hz; amplitude grid 80:4:148 Hz, half-width 12 Hz. Independent grid maximum for raw MVL, Ozkurt MVL, KLMI (18 bins), GLM R². Ozkurt MVL was additionally computed at each selected pair. These scan results are rejected because of the filter audit.

All rows with acceptance flags: [rodent_bouts_with_acceptance.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/rodent_bouts_with_acceptance.csv>). Raw unmodified export: [rodent_bouts.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/rodent_bouts.csv>).

### APC v1.0 — completed

| state | bout | duration_s | fP_hz | fA_hz | score | raw_mvl | ozkurt_mvl | preferred_phase_deg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run | 1 | 13.2408 | 7.867322 | 114 | 0.003952954 | 0.003952954 | 0.07981702 | 9.223331 |
| run | 2 | 11.24 | 7.779804 | 130 | 0.003620653 | 0.003620653 | 0.09275736 | -1.368225 |
| run | 3 | 10.5848 | 7.758795 | 116 | 0.003011107 | 0.003011107 | 0.06704916 | 7.647138 |
| run | 4 | 9.9504 | 7.776469 | 130 | 0.003095329 | 0.003095329 | 0.08208124 | 2.035646 |
| run | 5 | 10.6864 | 7.677286 | 114 | 0.00418474 | 0.00418474 | 0.07915449 | -11.37062 |
| run | 6 | 10.7528 | 7.605525 | 88 | 0.005684116 | 0.005684116 | 0.09250749 | -28.36805 |
| run | 7 | 9.3616 | 7.633707 | 106 | 0.004999066 | 0.004999066 | 0.0898156 | -8.697969 |
| run | 8 | 9.2976 | 7.521069 | 117 | 0.002182547 | 0.002182547 | 0.04641119 | -14.77373 |
| run | 9 | 9.4416 | 7.627875 | 108 | 0.005819918 | 0.005819918 | 0.1104795 | -13.18653 |
| run | 10 | 8.1744 | 7.548994 | 106 | 0.00489979 | 0.00489979 | 0.09591819 | -12.49585 |
| run | 11 | 10.3864 | 7.608591 | 113 | 0.004266851 | 0.004266851 | 0.08416772 | -2.729401 |
| run | 12 | 10.9608 | 7.590614 | 124 | 0.003990581 | 0.003990581 | 0.09049015 | -15.08479 |
| rest | 1 | 11.4744 | 7.978863 | 122 | 0.003070153 | 0.003070153 | 0.07880176 | -1.51859 |
| rest | 2 | 15.5896 | 7.24893 | 98 | 0.00261796 | 0.00261796 | 0.05990441 | 1.565373 |
| rest | 3 | 7.9816 | 6.715125 | 124 | 0.002531375 | 0.002531375 | 0.08118992 | 12.44813 |
| rest | 4 | 10.8 | 6.908717 | 83 | 0.001763412 | 0.001763412 | 0.04151597 | -6.038007 |
| rest | 5 | 13.2192 | 7.825638 | 104 | 0.003886016 | 0.003886016 | 0.08762567 | -1.154653 |
| rest | 6 | 10.1136 | 6.231858 | 91 | 0.002744547 | 0.002744547 | 0.06291107 | 11.12704 |
| rest | 7 | 6.1256 | 6.383711 | 115 | 0.0033656 | 0.0033656 | 0.09889424 | 12.88488 |
| rest | 8 | 16.492 | 7.755146 | 88 | 0.003745836 | 0.003745836 | 0.06558857 | 27.80572 |
| rest | 9 | 9.3056 | 6.568086 | 109 | 0.002545882 | 0.002545882 | 0.07266531 | 38.04131 |
| rest | 10 | 11.556 | 6.564694 | 123 | 0.001760256 | 0.001760256 | 0.06279264 | 13.72674 |
| rest | 11 | 7.0824 | 7.254557 | 116 | 0.002759199 | 0.002759199 | 0.07782178 | -11.84292 |
| rest | 12 | 13.7256 | 6.495454 | 84 | 0.002276584 | 0.002276584 | 0.05895898 | 9.112664 |


### MVL-raw — REJECTED comparator results

| state | bout | duration_s | fP_hz | fA_hz | score | raw_mvl | ozkurt_mvl | preferred_phase_deg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run | 1 | 13.2408 | 4 | 80 | 0.035353 | 0.035353 | 0.3596966 | 90.91277 |
| run | 2 | 11.24 | 4 | 80 | 0.02870846 | 0.02870846 | 0.3104514 | 89.96399 |
| run | 3 | 10.5848 | 4 | 80 | 0.02916374 | 0.02916374 | 0.3147455 | 89.7044 |
| run | 4 | 9.9504 | 4 | 80 | 0.02563227 | 0.02563227 | 0.2856324 | 90.12423 |
| run | 5 | 10.6864 | 4 | 80 | 0.03288903 | 0.03288903 | 0.3483859 | -92.93867 |
| run | 6 | 10.7528 | 4 | 80 | 0.03081513 | 0.03081513 | 0.3497483 | -89.40311 |
| run | 7 | 9.3616 | 4 | 80 | 0.02487463 | 0.02487463 | 0.270151 | 88.55151 |
| run | 8 | 9.2976 | 4 | 80 | 0.02635199 | 0.02635199 | 0.2929967 | 96.4595 |
| run | 9 | 9.4416 | 4 | 80 | 0.02913868 | 0.02913868 | 0.3131086 | 87.53202 |
| run | 10 | 8.1744 | 4 | 80 | 0.02465851 | 0.02465851 | 0.2576476 | -87.90965 |
| run | 11 | 10.3864 | 4.5 | 80 | 0.01932453 | 0.01932453 | 0.2090853 | -87.58173 |
| run | 12 | 10.9608 | 4.5 | 80 | 0.01198536 | 0.01198536 | 0.1409323 | -80.92077 |
| rest | 1 | 11.4744 | 4 | 80 | 0.03042301 | 0.03042301 | 0.3426465 | -86.92621 |
| rest | 2 | 15.5896 | 4 | 84 | 0.03187469 | 0.03187469 | 0.4384086 | 91.00202 |
| rest | 3 | 7.9816 | 4 | 80 | 0.02094614 | 0.02094614 | 0.2532222 | 94.33937 |
| rest | 4 | 10.8 | 4 | 80 | 0.02168618 | 0.02168618 | 0.2846005 | -90.75487 |
| rest | 5 | 13.2192 | 4 | 80 | 0.03486842 | 0.03486842 | 0.4170905 | -87.35614 |
| rest | 6 | 10.1136 | 4 | 80 | 0.02935862 | 0.02935862 | 0.3678395 | -92.78334 |
| rest | 7 | 6.1256 | 4 | 80 | 0.01237693 | 0.01237693 | 0.1729758 | -92.91132 |
| rest | 8 | 16.492 | 4 | 80 | 0.03784491 | 0.03784491 | 0.4562101 | 90.6233 |
| rest | 9 | 9.3056 | 4 | 80 | 0.02211934 | 0.02211934 | 0.2920159 | 89.18534 |
| rest | 10 | 11.556 | 4 | 80 | 0.02367456 | 0.02367456 | 0.322726 | -92.46247 |
| rest | 11 | 7.0824 | 4 | 80 | 0.02234323 | 0.02234323 | 0.2649435 | -81.25513 |
| rest | 12 | 13.7256 | 4.5 | 80 | 0.01467439 | 0.01467439 | 0.2148766 | 86.23397 |


### MVL-Ozkurt — REJECTED comparator results

| state | bout | duration_s | fP_hz | fA_hz | score | raw_mvl | ozkurt_mvl | preferred_phase_deg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run | 1 | 13.2408 | 4 | 124 | 0.3904647 | 0.02223423 | 0.3904647 | 88.53938 |
| run | 2 | 11.24 | 4 | 132 | 0.3213952 | 0.01579519 | 0.3213952 | 93.22823 |
| run | 3 | 10.5848 | 4 | 124 | 0.3553557 | 0.01866595 | 0.3553557 | 87.50145 |
| run | 4 | 9.9504 | 4 | 116 | 0.2870538 | 0.01709548 | 0.2870538 | 94.79014 |
| run | 5 | 10.6864 | 4 | 88 | 0.352671 | 0.03112634 | 0.352671 | -88.73969 |
| run | 6 | 10.7528 | 4 | 84 | 0.3532068 | 0.0298009 | 0.3532068 | -90.57556 |
| run | 7 | 9.3616 | 4 | 96 | 0.2960766 | 0.02389275 | 0.2960766 | 97.92814 |
| run | 8 | 9.2976 | 4 | 136 | 0.303096 | 0.01454439 | 0.303096 | 87.30863 |
| run | 9 | 9.4416 | 4 | 108 | 0.3361663 | 0.02331451 | 0.3361663 | 92.64134 |
| run | 10 | 8.1744 | 4 | 108 | 0.2745043 | 0.01732913 | 0.2745043 | -90.29217 |
| run | 11 | 10.3864 | 4.5 | 120 | 0.260823 | 0.01623068 | 0.260823 | -83.60012 |
| run | 12 | 10.9608 | 4.5 | 144 | 0.17281 | 0.007224853 | 0.17281 | -93.76437 |
| rest | 1 | 11.4744 | 4 | 144 | 0.3974075 | 0.01549607 | 0.3974075 | -89.59739 |
| rest | 2 | 15.5896 | 4 | 116 | 0.450561 | 0.02108633 | 0.450561 | 89.56892 |
| rest | 3 | 7.9816 | 4 | 100 | 0.2771021 | 0.01552759 | 0.2771021 | 85.19771 |
| rest | 4 | 10.8 | 4 | 132 | 0.2979758 | 0.01191126 | 0.2979758 | -92.05995 |
| rest | 5 | 13.2192 | 4 | 80 | 0.4170905 | 0.03486842 | 0.4170905 | -87.35614 |
| rest | 6 | 10.1136 | 4 | 148 | 0.3840646 | 0.01226194 | 0.3840646 | -85.32056 |
| rest | 7 | 6.1256 | 4 | 100 | 0.2116993 | 0.01167882 | 0.2116993 | -88.75955 |
| rest | 8 | 16.492 | 4 | 120 | 0.4893231 | 0.0230752 | 0.4893231 | 91.53079 |
| rest | 9 | 9.3056 | 4 | 136 | 0.3767004 | 0.01447497 | 0.3767004 | 90.71265 |
| rest | 10 | 11.556 | 4 | 144 | 0.3811073 | 0.01168534 | 0.3811073 | -92.62072 |
| rest | 11 | 7.0824 | 4 | 128 | 0.3403737 | 0.01315624 | 0.3403737 | -91.34817 |
| rest | 12 | 13.7256 | 4.5 | 132 | 0.2353403 | 0.008447053 | 0.2353403 | 94.85215 |


### KLMI — REJECTED comparator results

| state | bout | duration_s | fP_hz | fA_hz | score | raw_mvl | ozkurt_mvl | preferred_phase_deg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run | 1 | 13.2408 | 7.5 | 92 | 0.005453575 | 0.00862314 | 0.1079013 | 0.3664017 |
| run | 2 | 11.24 | 8 | 108 | 0.005086279 | 0.007061894 | 0.102284 | -6.17375 |
| run | 3 | 10.5848 | 8.5 | 100 | 0.003598497 | 0.00657304 | 0.08589167 | 5.378237 |
| run | 4 | 9.9504 | 7 | 120 | 0.004951819 | 0.005330959 | 0.09585855 | -10.51998 |
| run | 5 | 10.6864 | 7.5 | 100 | 0.00463871 | 0.008342077 | 0.1050199 | -22.87539 |
| run | 6 | 10.7528 | 6 | 116 | 0.004537716 | 0.006280873 | 0.1044718 | -21.97627 |
| run | 7 | 9.3616 | 8.5 | 104 | 0.003996982 | 0.007286294 | 0.09748727 | -9.816458 |
| run | 8 | 9.2976 | 9 | 132 | 0.005126596 | 0.005120635 | 0.1014435 | 14.96685 |
| run | 9 | 9.4416 | 6.5 | 112 | 0.007014712 | 0.008241134 | 0.1241753 | -16.21104 |
| run | 10 | 8.1744 | 6 | 100 | 0.006422968 | 0.007550109 | 0.1111465 | -7.951207 |
| run | 11 | 10.3864 | 4 | 112 | 0.01600805 | 0.01159287 | 0.1747878 | -82.63698 |
| run | 12 | 10.9608 | 4 | 140 | 0.01072423 | 0.002029176 | 0.04575209 | -91.1939 |
| rest | 1 | 11.4744 | 7 | 112 | 0.005292901 | 0.005423022 | 0.09862549 | -20.53888 |
| rest | 2 | 15.5896 | 4 | 112 | 0.003832596 | 0.02212163 | 0.4478102 | 90.38456 |
| rest | 3 | 7.9816 | 7 | 128 | 0.004398412 | 0.003922262 | 0.09659456 | 12.83405 |
| rest | 4 | 10.8 | 6.5 | 116 | 0.002570849 | 0.003007852 | 0.06605523 | 51.19156 |
| rest | 5 | 13.2192 | 7.5 | 108 | 0.003959788 | 0.005031052 | 0.09124199 | -3.54569 |
| rest | 6 | 10.1136 | 4 | 148 | 0.003584114 | 0.01226194 | 0.3840646 | -85.32056 |
| rest | 7 | 6.1256 | 7 | 120 | 0.0058883 | 0.005149576 | 0.1148765 | 6.993327 |
| rest | 8 | 16.492 | 4 | 120 | 0.003149439 | 0.0230752 | 0.4893231 | 91.53079 |
| rest | 9 | 9.3056 | 7 | 104 | 0.00344895 | 0.004344197 | 0.08213926 | 13.25178 |
| rest | 10 | 11.556 | 4 | 144 | 0.003461152 | 0.01168534 | 0.3811073 | -92.62072 |
| rest | 11 | 7.0824 | 4 | 140 | 0.005489153 | 0.01176018 | 0.3197776 | -93.03705 |
| rest | 12 | 13.7256 | 4 | 132 | 0.01022599 | 0.005627532 | 0.1567866 | 93.28298 |


### GLM — REJECTED comparator results

| state | bout | duration_s | fP_hz | fA_hz | score | raw_mvl | ozkurt_mvl | preferred_phase_deg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run | 1 | 13.2408 | 7.5 | 100 | 0.0865337 | 0.007552806 | 0.103791 | -0.01578044 |
| run | 2 | 11.24 | 8 | 108 | 0.08700641 | 0.007061894 | 0.102284 | -6.17375 |
| run | 3 | 10.5848 | 8.5 | 100 | 0.06166549 | 0.00657304 | 0.08589167 | 5.378237 |
| run | 4 | 9.9504 | 7 | 120 | 0.07399115 | 0.005330959 | 0.09585855 | -10.51998 |
| run | 5 | 10.6864 | 6.5 | 96 | 0.08216148 | 0.008083189 | 0.1000918 | -23.28315 |
| run | 6 | 10.7528 | 6 | 116 | 0.08225487 | 0.006280873 | 0.1044718 | -21.97627 |
| run | 7 | 9.3616 | 8.5 | 104 | 0.07849521 | 0.007286294 | 0.09748727 | -9.816458 |
| run | 8 | 9.2976 | 9 | 132 | 0.08501781 | 0.005120635 | 0.1014435 | 14.96685 |
| run | 9 | 9.4416 | 6.5 | 112 | 0.1157651 | 0.008241134 | 0.1241753 | -16.21104 |
| run | 10 | 8.1744 | 6 | 104 | 0.09931549 | 0.007461684 | 0.1150818 | -2.98676 |
| run | 11 | 10.3864 | 8 | 112 | 0.07552391 | 0.006650794 | 0.1002752 | 9.235683 |
| run | 12 | 10.9608 | 7.5 | 120 | 0.1041602 | 0.006792723 | 0.1124458 | -24.87144 |
| rest | 1 | 11.4744 | 7 | 112 | 0.07403094 | 0.005423022 | 0.09862549 | -20.53888 |
| rest | 2 | 15.5896 | 4 | 116 | 0.07028915 | 0.02108633 | 0.450561 | 89.56892 |
| rest | 3 | 7.9816 | 7 | 128 | 0.07556765 | 0.003922262 | 0.09659456 | 12.83405 |
| rest | 4 | 10.8 | 7 | 116 | 0.04123884 | 0.003378672 | 0.07419878 | 53.59791 |
| rest | 5 | 13.2192 | 7.5 | 108 | 0.06460596 | 0.005031052 | 0.09124199 | -3.54569 |
| rest | 6 | 10.1136 | 4.5 | 128 | 0.04721515 | 0.003557184 | 0.08831278 | -84.40403 |
| rest | 7 | 6.1256 | 7 | 120 | 0.09709156 | 0.005149576 | 0.1148765 | 6.993327 |
| rest | 8 | 16.492 | 4 | 120 | 0.05934745 | 0.0230752 | 0.4893231 | 91.53079 |
| rest | 9 | 9.3056 | 7 | 104 | 0.05466743 | 0.004344197 | 0.08213926 | 13.25178 |
| rest | 10 | 11.556 | 4 | 144 | 0.06077656 | 0.01168534 | 0.3811073 | -92.62072 |
| rest | 11 | 7.0824 | 4 | 128 | 0.07567238 | 0.01315624 | 0.3403737 | -91.34817 |
| rest | 12 | 13.7256 | 5.5 | 92 | 0.04831899 | 0.004702591 | 0.08152433 | 7.934749 |


## Run minus rest: inference and sensitivity

The tables below were computed before the filter failure was confirmed. Comparator inference is REJECTED; only the APC rows are retained as completed estimates. Unit of resampling is a bout within this single session, not an animal. Primary estimates use equal bout weights. Welch t has Satterthwaite df and two-sided p. Hedges g uses the pooled within-state SD and exact gamma small-sample correction. The mean-difference CI is the 2.5th/97.5th percentile of 10,000 independent within-state bout resamples, fixed seed 20261022; the same indices are used for all methods/metrics. No multiplicity adjustment.

Duration sensitivity normalizes durations within each state. Weighted variance = sum[p(x−mean)²]/(1−sum[p²]); effective n = 1/sum[p²]. Weighted Welch t/df and Hedges g use these variances and effective n. Bootstrap resampling keeps each bout value and duration together, then recomputes duration-weighted means. This is an explicitly specified weighted approximation.

Statistics and acceptance flags: [rodent_statistics_with_acceptance.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/rodent_statistics_with_acceptance.csv>). State summaries: [rodent_state_summary.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/rodent_state_summary.csv>).

### equal_bout — APC completed; all comparator rows REJECTED

| method | metric | run_mean | rest_mean | mean_difference | welch_t | welch_df | p_two_sided | hedges_g | bootstrap_ci_low | bootstrap_ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APC v1.0 | fP_hz | 7.666338 | 6.994232 | 0.6721059 | 3.790234 | 11.67825 | 0.002698223 | 1.493896 | 0.3283102 | 0.9883048 |
| APC v1.0 | fA_hz | 113.8333 | 104.75 | 9.083333 | 1.62273 | 20.27975 | 0.1200908 | 0.6395887 | -1.416667 | 19.41667 |
| APC v1.0 | ozkurt_mvl | 0.08422076 | 0.07072253 | 0.01349823 | 2.1144 | 21.95428 | 0.04607094 | 0.8333773 | 0.001122738 | 0.02513616 |
| MVL-raw | fP_hz | 4.083333 | 4.041667 | 0.04166667 | 0.5956834 | 20.28983 | 0.5579737 | 0.2347848 | -0.08333333 | 0.1666667 |
| MVL-raw | fA_hz | 80 | 80.33333 | -0.3333333 | -1 | 11 | 0.3388007 | -0.3941436 | -1 | 0 |
| MVL-raw | ozkurt_mvl | 0.2877151 | 0.318963 | -0.03124784 | -0.9935566 | 19.80975 | 0.3324208 | -0.3916039 | -0.09098216 | 0.02631545 |
| MVL-Ozkurt | fP_hz | 4.083333 | 4.041667 | 0.04166667 | 0.5956834 | 20.28983 | 0.5579737 | 0.2347848 | -0.08333333 | 0.1666667 |
| MVL-Ozkurt | fA_hz | 115 | 123.3333 | -8.333333 | -1.024431 | 21.7593 | 0.3168867 | -0.4037728 | -23 | 7.333333 |
| MVL-Ozkurt | ozkurt_mvl | 0.3086353 | 0.3548955 | -0.04626017 | -1.563936 | 19.32884 | 0.1340577 | -0.6164152 | -0.1024729 | 0.008334048 |
| KLMI | fP_hz | 6.875 | 5.5 | 1.375 | 2.082188 | 21.95649 | 0.04918886 | 0.8206808 | 0.125 | 2.583333 |
| KLMI | fA_hz | 111.3333 | 123.6667 | -12.33333 | -2.107338 | 21.96519 | 0.04673321 | -0.8305937 | -23.33333 | -1.333333 |
| KLMI | ozkurt_mvl | 0.104685 | 0.2273669 | -0.1226819 | -2.572458 | 11.70403 | 0.02484977 | -1.013918 | -0.2147261 | -0.03683888 |
| GLM | fP_hz | 7.416667 | 5.708333 | 1.708333 | 3.264604 | 19.37226 | 0.004000581 | 1.286723 | 0.75 | 2.708333 |
| GLM | fA_hz | 110.3333 | 118 | -7.666667 | -1.557432 | 20.7008 | 0.1345254 | -0.6138518 | -16.66667 | 1.333333 |
| GLM | ozkurt_mvl | 0.1036081 | 0.1990732 | -0.09546508 | -2.014857 | 11.08009 | 0.06883745 | -0.7941431 | -0.1892555 | -0.01238726 |


### duration — APC completed; all comparator rows REJECTED

| method | metric | run_mean | rest_mean | mean_difference | welch_t | welch_df | p_two_sided | hedges_g | bootstrap_ci_low | bootstrap_ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APC v1.0 | fP_hz | 7.674928 | 7.07122 | 0.6037085 | 3.205225 | 10.72277 | 0.008637902 | 1.329368 | 0.2565017 | 0.9637955 |
| APC v1.0 | fA_hz | 114.0872 | 102.4598 | 11.62741 | 2.016039 | 18.72873 | 0.05837054 | 0.8186435 | 0.2920932 | 21.60818 |
| APC v1.0 | ozkurt_mvl | 0.08407657 | 0.06877275 | 0.01530382 | 2.469989 | 20.96688 | 0.0221818 | 0.9915209 | 0.00369062 | 0.02577985 |
| MVL-raw | fP_hz | 4.086024 | 4.05142 | 0.03460359 | 0.4639533 | 20.51968 | 0.6475654 | 0.1854167 | -0.1080886 | 0.1747543 |
| MVL-raw | fA_hz | 80 | 80.46722 | -0.4672245 | -1.157542 | 10.13127 | 0.2736122 | -0.4810262 | -1.382445 | 1.421085e-14 |
| MVL-raw | ozkurt_mvl | 0.2896698 | 0.336797 | -0.04712722 | -1.422221 | 18.26836 | 0.1718123 | -0.5782481 | -0.1086628 | 0.01730291 |
| MVL-Ozkurt | fP_hz | 4.086024 | 4.05142 | 0.03460359 | 0.4639533 | 20.51968 | 0.6475654 | 0.1854167 | -0.1080886 | 0.1747543 |
| MVL-Ozkurt | fA_hz | 115.463 | 123.4653 | -8.002237 | -0.9580398 | 20.46139 | 0.3492269 | -0.3866447 | -23.07321 | 7.787163 |
| MVL-Ozkurt | ozkurt_mvl | 0.3109166 | 0.3695998 | -0.05868325 | -1.879927 | 17.86074 | 0.07653142 | -0.7651655 | -0.116289 | 0.002776989 |
| KLMI | fP_hz | 6.871281 | 5.333144 | 1.538137 | 2.274077 | 20.95661 | 0.03359548 | 0.913819 | 0.2421721 | 2.720503 |
| KLMI | fA_hz | 111.0123 | 122.7236 | -11.71122 | -1.954397 | 20.87217 | 0.06418233 | -0.7864757 | -22.815 | -0.7144433 |
| KLMI | ozkurt_mvl | 0.1042951 | 0.2476029 | -0.1433078 | -2.735799 | 10.68611 | 0.01984393 | -1.134807 | -0.2419969 | -0.04238612 |
| GLM | fP_hz | 7.429173 | 5.565752 | 1.863422 | 3.466163 | 17.26107 | 0.002898568 | 1.412952 | 0.8562861 | 2.814138 |
| GLM | fA_hz | 110.0183 | 116.9249 | -6.90656 | -1.348147 | 18.77459 | 0.1936527 | -0.5473645 | -16.43108 | 2.410796 |
| GLM | ozkurt_mvl | 0.1033455 | 0.219525 | -0.1161795 | -2.174316 | 10.18689 | 0.05428611 | -0.9033852 | -0.2211525 | -0.0123764 |


### State means and boundary counts

| method | state | n_bouts | duration_total_s | fP_mean | fA_mean | ozkurt_mean | fP_weighted | fA_weighted | ozkurt_weighted | boundary_4 | boundary_12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APC v1.0 | run | 12 | 124.0776 | 7.666338 | 113.8333 | 0.08422076 | 7.674928 | 114.0872 | 0.08407657 | 0 | 0 |
| APC v1.0 | rest | 12 | 133.4656 | 6.994232 | 104.75 | 0.07072253 | 7.07122 | 102.4598 | 0.06877275 | 0 | 0 |
| MVL-raw | run | 12 | 124.0776 | 4.083333 | 80 | 0.2877151 | 4.086024 | 80 | 0.2896698 | 10 | 0 |
| MVL-raw | rest | 12 | 133.4656 | 4.041667 | 80.33333 | 0.318963 | 4.05142 | 80.46722 | 0.336797 | 11 | 0 |
| MVL-Ozkurt | run | 12 | 124.0776 | 4.083333 | 115 | 0.3086353 | 4.086024 | 115.463 | 0.3109166 | 10 | 0 |
| MVL-Ozkurt | rest | 12 | 133.4656 | 4.041667 | 123.3333 | 0.3548955 | 4.05142 | 123.4653 | 0.3695998 | 11 | 0 |
| KLMI | run | 12 | 124.0776 | 6.875 | 111.3333 | 0.104685 | 6.871281 | 111.0123 | 0.1042951 | 2 | 0 |
| KLMI | rest | 12 | 133.4656 | 5.5 | 123.6667 | 0.2273669 | 5.333144 | 122.7236 | 0.2476029 | 6 | 0 |
| GLM | run | 12 | 124.0776 | 7.416667 | 110.3333 | 0.1036081 | 7.429173 | 110.0183 | 0.1033455 | 0 | 0 |
| GLM | rest | 12 | 133.4656 | 5.708333 | 118 | 0.1990732 | 5.565752 | 116.9249 | 0.219525 | 4 | 0 |


Boundary counts are exact equality to 4 or 12 Hz. APC has no 4–12-Hz scan bound; its counts are descriptive equalities only. Comparator counts are rejected along with the scans.

## Optional additional sessions

Eight other EC013 sessions are present locally: 156, 205, 206, 208, 251, 252, 374, 375. None has saved run/rest trial files in the inspected Brainstorm session folders. No other session with documented ≥8 run and ≥8 rest bouts of ≥5 s was established locally; no optional session replication was run and no additional-session data were downloaded.

## Canonical examples completed before stopping

The 20-s, 500-Hz 8/120-Hz coupled, jittered and continuous inputs were regenerated with the existing Python canonical generator and original seed/order 12345 and matched their historical signal CSVs to 1e-14. Original canonical settings include Gaussian sigma 30 ms, burst amplitude 1.8, low amplitude 1, baseline HF amplitude .15, white-noise SD .8. The jitter call explicitly used SD **0.020 s**. These settings differ from the held-out generator.

The timing null changes only the true-burst component of the coupled canonical example, using a homogeneous Poisson rate of 8/s on (0.5,19.5) s, separate seed 20261022, 174 realized events; overlaps allowed. Low rhythm, baseline HF and noise samples are shared exactly. The original canonical fixed-count uniform-time null was not reused as a Poisson null.

| state | fP_hz | fA_hz | raw_mvl | ozkurt_mvl | preferred_phase_deg |
| --- | --- | --- | --- | --- | --- |
| burst_coupled | 7.997923 | 122 | 0.1769078 | 0.1789677 | 178.5758 |
| timing_null | 7.996071 | 81 | 0.002156205 | 0.01120197 | -134.062 |
| jittered | 7.994806 | 125 | 0.1126453 | 0.1205944 | 179.2996 |
| continuous_pac | 8.000909 | 150 | 0.002086324 | 0.01074866 | -21.34482 |

Metadata-corrected export: [canonical_results_export_corrected.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/canonical_results_export_corrected.csv>). The original raw canonical CSV remains preserved; its shared exporter had populated the rodent session label and analysis seed. Corrected metadata changes no numerical output. Generator provenance: [canonical_provenance.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/canonical_provenance.json>).

## Figure status and paths

Two figures were exported before the stop as PNG at 300 dpi and SVG. Their embedded Description metadata contains the method commit, full settings, source CSV paths and SHA-256 hashes; source CSV filenames and commit are also visible. They are retained as drafts pending completion of the package. Figure 1 has a known colorbar-label issue: it says CWT magnitude but must say frequency-wise standardized CWT magnitude; the plotted values are the unchanged frozen diagnostics.

- Figure_1_workflow: [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Figure_1_workflow.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Figure_1_workflow.svg>). DRAFT: full package stopped; Figure 1 label issue documented.
- Figure_2_canonical_conditions: [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Figure_2_canonical_conditions.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Figure_2_canonical_conditions.svg>). EXPORTED before stop; final approval pending.

**Not exported:** Figures 3–5, development A0/A1/A2 supplements and the v2.0 negative-result supplement. The figure builder stopped on a Wilson errorbar rounding issue before the numerical filter failure was confirmed; the requested failure rule then stopped further work. The saved held-out and development CSVs were not changed. Figure manifest: [figure_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/figure_manifest.json>).

## Runtime and deviations

Canonical-only resumed MATLAB analysis: 27.2667 s, measured by tic/toc. The earlier MATLAB process completed all rodent bouts but aborted during canonical CSV import; its tic/toc total was not saved. Approximate launch-log-creation to rodent-CSV-write envelope: 112.618 s (includes startup; filesystem timestamps). No full successful report-build runtime exists because rendering aborted at Figure 3. Filter audit logs record all attempts.

Tooling/export deviations (no tagged-method fix):

- tooling: Metadata inspector initially aligned the crop by absolute timestamps. The crop restarts at zero; exact R2 indices 40800:372501 establish row-1 identity. No signal/bout changes.
- tooling: First MATLAB launch failed pre-analysis source-path assertion because the workspace current directory shadowed the frozen file. Working directory changed to final; frozen path then asserted.
- tooling: Canonical CSV auto delimiter detection failed after all rodent bouts completed. Explicit comma delimiter fixed import; only canonical stage resumed.
- tooling: Figure build stopped at Figure 3 because Wilson endpoint floating-point roundoff produced a negative errorbar length. Figures 3-5 and supplements were not exported. No numerical recovery or interval result changed.
- tooling: Filter audit first used a scalar frequency argument interpreted by freqz as an FFT length, then an incompatible empty-struct assignment. Frequency vector and concatenation fixed only the audit exporter.
- tooling: Pre-existing MATLAB startup warnings refer to unavailable Brainstorm directories. No installation changed.
- export bookkeeping: Canonical raw CSV used rodent session label and analysis seed in shared exporter. A new canonical_results_export_corrected.csv fixes session/seed metadata only; raw file retained. Actual canonical input seed is 12345; Poisson seed 20261022.
- draft figure labeling: Figure 1 colorbar says CWT magnitude; the plotted frozen diagnostic is frequency-wise standardized CWT magnitude. The figure is retained as a draft, not approved for publication.
- evidence limitation: E1/channel row 1 documented; no local session XML or channel-to-shank/layer map. Other-session run/rest bout eligibility not established.

Failure status and numbers: [STOPPED.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/STOPPED.json>). Deviations: [deviations.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/deviations.json>). Provenance: [analysis_provenance.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/analysis_provenance.json>). Integrity verification: [verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/verification.json>). Output hashes: [output_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/output_manifest.json>).

The minimal prospective comparator repair would be a numerically stable SOS realization of the same nominal Butterworth filters, followed by a full rodent scan/inference rerun. **It was not applied or evaluated**, consistent with the stop rule. No tagged APC code or earlier saved results were changed.
