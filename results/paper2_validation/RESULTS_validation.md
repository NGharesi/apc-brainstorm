# Paper-2 out-of-sample validation

Protocol Amendment 1 and archive are public on paper2. Amendment push: `dbc0d7901091602e146e4d28b22fdadb043daef4`. Ablation archive: `f66acb513fcc49f5bc4a2d7b426abe095be4dec8`. Protocol SHA-256: `7b461e92a09d1a282225f07415d27ca7a4525984d3dab0ca5fc9c444700b6080`. MATLAB: 9.13.0.2105380 (R2022b) Update 2. No tagged method or protocol source was edited.

## Initial stop and Amendment 1 resolution

The original pre-gate A_EVENT ambiguity stop is preserved unchanged in [STOPPED.md](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\STOPPED.md). Amendment 1 resolves it with `struct('status_code', s, 'fp_hz', fP)`: status zero whenever the source returns finite fP. Resumed 2026-10-24T11:27:12.980681+00:00; the transfer copy amend1_validation.md was ignored.

## Gates and inputs

G-gen PASS: 675/675 HB complete cases, including all H1 inputs, and 900/900 HA complete cases are bit-identical. Six P1 repeat-1 double-generation checks matched at seed 20261112, with no outcomes computed. G-event PASS: minimal, original and repeated calls agree within 1e-12. G-abl PASS: 42 APC cases and 23 scan cases at 1e-10. Configuration adapters reproduced the unchanged scan computations exactly.

V1 has 175 coupled + 175 paired timing-null inputs (seed 20261110); V2 has 450 + 450 (20261111); V3 has six cells x 100 (20261112); V4 has 25 (20261113). Full HB source sequences were generated to retain the original RNG order, then only H1/H3 or H4 cases were selected; no methods ran on unused source-sequence cases. All signal banks and per-trial truths are saved and hashed.

Nine component pipelines and three references were evaluated on every simulation input. Coupling uses the unchanged ablation common phase-band rule, with the selected amplitude-band realization (event half-width 6 Hz). Errors summarize finite estimates; invalid outputs count as recovery failures. AUC uses available finite scores in each class, and finite/complete-pair counts are reported. Its bootstrap resamples paired input IDs together, 10,000 times, seed 20261114.

Calibrated F3 / SCAN tests use the maximum normalized scan MVL over every amplitude candidate, 200 common envelope shifts per input, drawn with mrg32k3a seed 20261115 in V1-V4 input order. Shifts are rounded samples from N*(0.25 + 0.5*uniform). p = (1 + exceedances)/201. FFT circular sums were checked against the defining time-domain sums. Invalid tests contribute no rejection and remain in the denominators; valid/invalid counts are shown.


## ECoG saved-result consistency stop: resolution and audit

The executor-added 1e-10 absolute saved-F3/SCAN consistency check stopped on ca_movement_020. It was not a protocol gate. The user resolved the difference as floating-point propagation through the narrow low-frequency phase filter and authorized resumption at 2026-10-24T16:32:01.640359+00:00, without a protocol amendment or changes to any method. The 39 completed ECoG checkpoints were retained. Both STOPPED.md and STOPPED_ACTIVE.md remain byte-identical; future stops use STOP_RUN.md.

The resumed check requires identical fA, validity, status and NaN pattern; absolute fP difference <=1e-9 Hz; absolute coupling difference <=1e-6 * max(abs(saved coupling), 1e-12). Relative audit differences use max(abs(saved), 1e-12). Newly computed values are used for every reported F3 pipeline; only APC v1.0/v3.0 and A2-prime references use saved values. No new endpoint was inspected to identify or authorize the fix.


## ECoG reproduction-check maxima

| quantity | maximum | bout_at_maximum | finite_comparisons | n_bouts |
| --- | --- | --- | --- | --- |
| fp_absolute_difference_hz | 2.1672e-12 | rh_movement_060 | 2638 | 2642 |
| fp_relative_difference | 1.1414e-13 | jc_movement_060 | 2638 | 2642 |
| coupling_absolute_difference | 5.4818e-09 | gf_movement_085 | 2638 | 2642 |
| coupling_relative_difference | 9.2024e-08 | gf_movement_085 | 2638 | 2642 |


Full CSV: [ecog_reproduction_maxima.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\ecog_reproduction_maxima.csv).

Full per-bout audit: [ecog_reproduction_check.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\ecog_reproduction_check.csv). All 2642 bouts passed.


## Primary decisions

| endpoint | decision |
| --- | --- |
| P-A | validated |
| P-B | it does not |
| P-C | in these simulations, the burst-based fP was not shown to improve on the spectral peak |


Full CSV: [primary_decisions.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\primary_decisions.csv).


## P-A

| suite | first | second | n | first_success | first_ci_low | first_ci_high | second_success | second_ci_low | second_ci_high | both | only_first | only_second | neither | p_value | p_holm | significant | direction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V1 | F3_A_SCAN | APC-v1.0 | 175 | 161 | 0.87021 | 0.95175 | 116 | 0.58999 | 0.72873 | 111 | 50 | 5 | 9 | 2.1358e-10 | 2.1358e-10 | True | first |
| V1 | F3_A_SCAN | A2_prime_2D | 175 | 161 | 0.87021 | 0.95175 | 91 | 0.44635 | 0.59279 | 91 | 70 | 0 | 14 | 1.6941e-21 | 3.3881e-21 | True | first |
| V2 | F3_A_SCAN | APC-v1.0 | 450 | 354 | 0.74647 | 0.82201 | 43 | 0.071716 | 0.12624 | 27 | 327 | 16 | 80 | 1.4428e-76 | 5.771e-76 | True | first |
| V2 | F3_A_SCAN | A2_prime_2D | 450 | 354 | 0.74647 | 0.82201 | 216 | 0.4342 | 0.52613 | 213 | 141 | 3 | 93 | 4.4643e-38 | 1.3393e-37 | True | first |


Full CSV: [P_A.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\P_A.csv).


## P-B

| suite | source | first | second | n | first_success | first_ci_low | first_ci_high | second_success | second_ci_low | second_ci_high | both | only_first | only_second | neither | p_value | p_holm | significant | direction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V1 | F3 | F3_A_EVENT | F3_A_SCAN | 175 | 163 | 0.88398 | 0.96034 | 161 | 0.87021 | 0.95175 | 152 | 11 | 9 | 3 | 0.8238 | 1 | False | first |
| V1 | F2 | F2_A_EVENT | F2_A_SCAN | 175 | 163 | 0.88398 | 0.96034 | 161 | 0.87021 | 0.95175 | 152 | 11 | 9 | 3 | 0.8238 | 1 | False | first |
| V2 | F3 | F3_A_EVENT | F3_A_SCAN | 450 | 127 | 0.24262 | 0.32551 | 354 | 0.74647 | 0.82201 | 71 | 56 | 283 | 40 | 1.2464e-37 | 3.7392e-37 | True | second |
| V2 | F2 | F2_A_EVENT | F2_A_SCAN | 450 | 92 | 0.16976 | 0.24413 | 305 | 0.63325 | 0.71929 | 56 | 36 | 249 | 109 | 2.3765e-40 | 9.506e-40 | True | second |


Full CSV: [P_B.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\P_B.csv).


## P-C

| first | second | n | first_success | first_ci_low | first_ci_high | second_success | second_ci_low | second_ci_high | both | only_first | only_second | neither | p_value | p_holm | significant | direction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F2 | F3 | 400 | 3 | 0.0025539 | 0.021816 | 1 | 0.00044145 | 0.014023 | 0 | 3 | 1 | 396 | 0.625 | 1 | False | first |
| F1 | F3 | 400 | 0 | 8.6736e-19 | 0.0095123 | 1 | 0.00044145 | 0.014023 | 0 | 0 | 1 | 399 | 1 | 1 | False | second |


Full CSV: [P_C.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\P_C.csv).


## V3 source recovery and dominant-rhythm picks

| cell | source | n | finite | fp_recovery | strict_fp_recovery | dominant_picks | dominant_pick_rate | mean_abs_fp_error | median_abs_fp_error | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| non_dominant_pooled | F1 | 400 | 400 | 0 | 0 | 395 | 0.9875 | 6.0489 | 6.0001 | 8.6736e-19 | 0.0095123 |
| non_dominant_pooled | F2 | 400 | 400 | 3 | 3 | 396 | 0.99 | 6.0159 | 5.9982 | 0.0025539 | 0.021816 |
| non_dominant_pooled | F3 | 400 | 400 | 1 | 1 | 399 | 0.9975 | 5.9863 | 6.0004 | 0.00044145 | 0.014023 |
| A_keep100 | F1 | 100 | 100 | 0 | 0 | 98 | 0.98 | 5.9104 | 5.9509 | 3.4694e-18 | 0.036993 |
| A_keep100 | F2 | 100 | 100 | 0 | 0 | 100 | 1 | 5.9479 | 5.9509 | 3.4694e-18 | 0.036993 |
| A_keep100 | F3 | 100 | 100 | 0 | 0 | 100 | 1 | 5.9994 | 5.9987 | 3.4694e-18 | 0.036993 |
| A_keep040 | F1 | 100 | 100 | 0 | 0 | 98 | 0.98 | 5.8798 | 5.9475 | 3.4694e-18 | 0.036993 |
| A_keep040 | F2 | 100 | 100 | 0 | 0 | 100 | 1 | 5.9437 | 5.9475 | 3.4694e-18 | 0.036993 |
| A_keep040 | F3 | 100 | 100 | 0 | 0 | 100 | 1 | 5.9995 | 5.9992 | 3.4694e-18 | 0.036993 |
| B_keep100 | F1 | 100 | 100 | 0 | 0 | 99 | 0.99 | 6.2555 | 6.1634 | 3.4694e-18 | 0.036993 |
| B_keep100 | F2 | 100 | 100 | 2 | 2 | 97 | 0.97 | 6.0855 | 6.1533 | 0.005502 | 0.070012 |
| B_keep100 | F3 | 100 | 100 | 1 | 1 | 99 | 0.99 | 5.9449 | 6.0034 | 0.0017674 | 0.054486 |
| B_keep040 | F1 | 100 | 100 | 0 | 0 | 100 | 1 | 6.1497 | 6.1123 | 3.4694e-18 | 0.036993 |
| B_keep040 | F2 | 100 | 100 | 1 | 1 | 99 | 0.99 | 6.0863 | 6.1087 | 0.0017674 | 0.054486 |
| B_keep040 | F3 | 100 | 100 | 0 | 0 | 100 | 1 | 6.0012 | 6.0016 | 3.4694e-18 | 0.036993 |
| R_single_keep100 | F1 | 100 | 100 | 100 | 100 | 0 | NA | 0.051992 | 0.045419 | 0.96301 | 1 |
| R_single_keep100 | F2 | 100 | 100 | 100 | 100 | 0 | NA | 0.051992 | 0.045419 | 0.96301 | 1 |
| R_single_keep100 | F3 | 100 | 100 | 100 | 100 | 0 | NA | 0.0056012 | 0.0046088 | 0.96301 | 1 |
| N_uncoupled | F1 | 100 | 100 | 100 | 100 | 0 | NA | 0.045137 | 0.045102 | 0.96301 | 1 |
| N_uncoupled | F2 | 100 | 100 | 100 | 100 | 0 | NA | 0.045137 | 0.045102 | 0.96301 | 1 |
| N_uncoupled | F3 | 100 | 100 | 100 | 100 | 0 | NA | 0.0055614 | 0.0046943 | 0.96301 | 1 |


Full CSV: [P_C_source_recovery.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\P_C_source_recovery.csv).


## Secondary recovery and errors

| suite | method | n | valid | joint | strict_joint | fp_only | fa_only | mean_abs_fp_error | median_abs_fp_error | mean_abs_fa_error | median_abs_fa_error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V1 | F1_A_APC | 175 | 172 | 116 | 116 | 170 | 116 | 0.11768 | 0.028408 | 11.046 | 4.7525 |
| V1 | F1_A_SCAN | 175 | 175 | 156 | 156 | 170 | 156 | 0.25487 | 0.029944 | 4.1422 | 1.2378 |
| V1 | F1_A_EVENT | 175 | 175 | 159 | 159 | 170 | 160 | 0.25487 | 0.029944 | 4.3231 | 2.9656 |
| V1 | F2_A_APC | 175 | 175 | 120 | 120 | 175 | 120 | 0.046817 | 0.028947 | 10.672 | 4.5486 |
| V1 | F2_A_SCAN | 175 | 175 | 161 | 161 | 175 | 161 | 0.046817 | 0.028947 | 3.2883 | 1.1848 |
| V1 | F2_A_EVENT | 175 | 175 | 163 | 163 | 175 | 163 | 0.046817 | 0.028947 | 3.9212 | 2.9656 |
| V1 | F3_A_APC | 175 | 175 | 115 | 115 | 175 | 115 | 0.0075011 | 0.0067007 | 11 | 4.7945 |
| V1 | F3_A_SCAN | 175 | 175 | 161 | 161 | 175 | 161 | 0.0075011 | 0.0067007 | 3.3197 | 1.1848 |
| V1 | F3_A_EVENT | 175 | 175 | 163 | 163 | 175 | 163 | 0.0075011 | 0.0067007 | 3.9212 | 2.9656 |
| V1 | A2_prime_2D | 175 | 175 | 91 | 37 | 91 | 133 | 2.1292 | 0.96591 | 8.286 | 1.6664 |
| V1 | APC-v1.0 | 175 | 172 | 116 | 116 | 170 | 116 | 0.11768 | 0.028408 | 11.046 | 4.7525 |
| V1 | APC-v3.0 | 175 | 175 | 120 | 120 | 175 | 120 | 0.046817 | 0.028947 | 10.672 | 4.5486 |
| V2 | F1_A_APC | 450 | 113 | 43 | 43 | 98 | 49 | 1.6907 | 0.037412 | 14.276 | 11.385 |
| V2 | F1_A_SCAN | 450 | 450 | 71 | 70 | 98 | 74 | 11.191 | 11.896 | 32.95 | 35.727 |
| V2 | F1_A_EVENT | 450 | 450 | 30 | 30 | 98 | 95 | 11.191 | 11.896 | 25.616 | 22.034 |
| V2 | F2_A_APC | 450 | 449 | 114 | 109 | 366 | 125 | 1.7442 | 0.079685 | 17.312 | 14.862 |
| V2 | F2_A_SCAN | 450 | 449 | 305 | 288 | 366 | 328 | 1.7442 | 0.079685 | 7.8774 | 2.7462 |
| V2 | F2_A_EVENT | 450 | 449 | 92 | 82 | 366 | 108 | 1.7442 | 0.079685 | 16.596 | 13.792 |
| V2 | F3_A_APC | 450 | 449 | 140 | 140 | 445 | 140 | 0.13331 | 0.011073 | 16.834 | 15.062 |
| V2 | F3_A_SCAN | 450 | 449 | 354 | 354 | 445 | 355 | 0.13331 | 0.011073 | 4.9771 | 2.3054 |
| V2 | F3_A_EVENT | 450 | 449 | 127 | 127 | 445 | 127 | 0.13331 | 0.011073 | 13.907 | 12.553 |
| V2 | A2_prime_2D | 450 | 450 | 216 | 97 | 287 | 305 | 2.7805 | 0.83472 | 8.9682 | 3.4131 |
| V2 | APC-v1.0 | 450 | 113 | 43 | 43 | 98 | 49 | 1.6907 | 0.037412 | 14.276 | 11.385 |
| V2 | APC-v3.0 | 450 | 449 | 114 | 109 | 366 | 125 | 1.7442 | 0.079685 | 17.312 | 14.862 |
| V3 | F1_A_APC | 500 | 500 | 81 | 81 | 100 | 179 | 4.8495 | 5.9731 | 17.118 | 17 |
| V3 | F1_A_SCAN | 500 | 500 | 100 | 100 | 100 | 172 | 4.8495 | 5.9731 | 15.168 | 16 |
| V3 | F1_A_EVENT | 500 | 500 | 100 | 100 | 100 | 214 | 4.8495 | 5.9731 | 14.016 | 12 |
| V3 | F2_A_APC | 500 | 500 | 84 | 84 | 103 | 179 | 4.8231 | 5.9715 | 17.108 | 17 |
| V3 | F2_A_SCAN | 500 | 500 | 103 | 103 | 103 | 175 | 4.8231 | 5.9715 | 15.048 | 16 |
| V3 | F2_A_EVENT | 500 | 500 | 103 | 103 | 103 | 217 | 4.8231 | 5.9715 | 13.96 | 12 |
| V3 | F3_A_APC | 500 | 500 | 85 | 85 | 101 | 181 | 4.7901 | 5.9982 | 16.82 | 16 |
| V3 | F3_A_SCAN | 500 | 500 | 101 | 101 | 101 | 172 | 4.7901 | 5.9982 | 15.104 | 16 |
| V3 | F3_A_EVENT | 500 | 500 | 101 | 101 | 101 | 215 | 4.7901 | 5.9982 | 14.04 | 12 |
| V3 | A2_prime_2D | 500 | 500 | 295 | 175 | 300 | 358 | 2.982 | 1 | 8.056 | 4 |
| V3 | APC-v1.0 | 500 | 500 | 81 | 81 | 100 | 179 | 4.8495 | 5.9731 | 17.118 | 17 |
| V3 | APC-v3.0 | 500 | 500 | 84 | 84 | 103 | 179 | 4.8231 | 5.9715 | 17.108 | 17 |
| V4 | F1_A_APC | 25 | 25 | 23 | 23 | 24 | 23 | 0.40527 | 0.04996 | 3.2809 | 2.0373 |
| V4 | F1_A_SCAN | 25 | 25 | 24 | 24 | 24 | 24 | 0.40527 | 0.04996 | 2.616 | 0.92653 |
| V4 | F1_A_EVENT | 25 | 25 | 23 | 23 | 24 | 23 | 0.40527 | 0.04996 | 5.3382 | 3.916 |
| V4 | F2_A_APC | 25 | 25 | 24 | 24 | 25 | 24 | 0.043543 | 0.049821 | 2.7094 | 2.0373 |
| V4 | F2_A_SCAN | 25 | 25 | 25 | 25 | 25 | 25 | 0.043543 | 0.049821 | 1.016 | 0.92653 |
| V4 | F2_A_EVENT | 25 | 25 | 24 | 24 | 25 | 24 | 0.043543 | 0.049821 | 3.7897 | 3.916 |
| V4 | F3_A_APC | 25 | 25 | 24 | 24 | 25 | 24 | 0.0051739 | 0.0052072 | 2.6694 | 2.0373 |
| V4 | F3_A_SCAN | 25 | 25 | 25 | 25 | 25 | 25 | 0.0051739 | 0.0052072 | 1.016 | 0.92653 |
| V4 | F3_A_EVENT | 25 | 25 | 24 | 24 | 25 | 24 | 0.0051739 | 0.0052072 | 3.7897 | 3.916 |
| V4 | A2_prime_2D | 25 | 25 | 23 | 3 | 23 | 25 | 0.7061 | 0.76679 | 1.016 | 0.92653 |
| V4 | APC-v1.0 | 25 | 25 | 23 | 23 | 24 | 23 | 0.40527 | 0.04996 | 3.2809 | 2.0373 |
| V4 | APC-v3.0 | 25 | 25 | 24 | 24 | 25 | 24 | 0.043543 | 0.049821 | 2.7094 | 2.0373 |


Full CSV: [recovery_overall.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\recovery_overall.csv).


## False joint recovery

| suite | method | n | valid | joint | joint_ci_low | joint_ci_high |
| --- | --- | --- | --- | --- | --- | --- |
| V1 | F1_A_APC | 175 | 170 | 44 | 0.19296 | 0.32057 |
| V1 | F1_A_SCAN | 175 | 175 | 33 | 0.13754 | 0.25298 |
| V1 | F1_A_EVENT | 175 | 175 | 36 | 0.15246 | 0.27161 |
| V1 | F2_A_APC | 175 | 175 | 46 | 0.20324 | 0.33267 |
| V1 | F2_A_SCAN | 175 | 175 | 35 | 0.14747 | 0.26542 |
| V1 | F2_A_EVENT | 175 | 175 | 38 | 0.16249 | 0.28395 |
| V1 | F3_A_APC | 175 | 175 | 47 | 0.20839 | 0.33869 |
| V1 | F3_A_SCAN | 175 | 175 | 34 | 0.1425 | 0.25921 |
| V1 | F3_A_EVENT | 175 | 175 | 37 | 0.15746 | 0.27779 |
| V1 | A2_prime_2D | 175 | 175 | 0 | 0 | 0.02148 |
| V1 | APC-v1.0 | 175 | 170 | 44 | 0.19296 | 0.32057 |
| V1 | APC-v3.0 | 175 | 175 | 46 | 0.20324 | 0.33267 |
| V2 | F1_A_APC | 450 | 80 | 9 | 0.010557 | 0.037569 |
| V2 | F1_A_SCAN | 450 | 450 | 19 | 0.027194 | 0.065 |
| V2 | F1_A_EVENT | 450 | 450 | 13 | 0.016959 | 0.048794 |
| V2 | F2_A_APC | 450 | 450 | 37 | 0.060239 | 0.11128 |
| V2 | F2_A_SCAN | 450 | 450 | 152 | 0.29562 | 0.38268 |
| V2 | F2_A_EVENT | 450 | 450 | 65 | 0.11497 | 0.17994 |
| V2 | F3_A_APC | 450 | 449 | 51 | 0.087259 | 0.14595 |
| V2 | F3_A_SCAN | 450 | 449 | 181 | 0.35793 | 0.44817 |
| V2 | F3_A_EVENT | 450 | 449 | 80 | 0.14522 | 0.21579 |
| V2 | A2_prime_2D | 450 | 450 | 5 | 0.0047551 | 0.025743 |
| V2 | APC-v1.0 | 450 | 80 | 9 | 0.010557 | 0.037569 |
| V2 | APC-v3.0 | 450 | 450 | 37 | 0.060239 | 0.11128 |
| V3 | F1_A_APC | 100 | 100 | 24 | 0.16691 | 0.33232 |
| V3 | F1_A_SCAN | 100 | 100 | 19 | 0.12515 | 0.27779 |
| V3 | F1_A_EVENT | 100 | 100 | 38 | 0.29098 | 0.4779 |
| V3 | F2_A_APC | 100 | 100 | 24 | 0.16691 | 0.33232 |
| V3 | F2_A_SCAN | 100 | 100 | 19 | 0.12515 | 0.27779 |
| V3 | F2_A_EVENT | 100 | 100 | 38 | 0.29098 | 0.4779 |
| V3 | F3_A_APC | 100 | 100 | 24 | 0.16691 | 0.33232 |
| V3 | F3_A_SCAN | 100 | 100 | 20 | 0.13337 | 0.28883 |
| V3 | F3_A_EVENT | 100 | 100 | 37 | 0.28182 | 0.46779 |
| V3 | A2_prime_2D | 100 | 100 | 0 | 3.4694e-18 | 0.036993 |
| V3 | APC-v1.0 | 100 | 100 | 24 | 0.16691 | 0.33232 |
| V3 | APC-v3.0 | 100 | 100 | 24 | 0.16691 | 0.33232 |


Full CSV: [false_joint_recovery.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\false_joint_recovery.csv).


## Coupled vs paired-null AUC

| suite | method | pairs | finite_coupled | finite_null | complete_pairs | auc | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V1 | F1_A_APC | 175 | 172 | 170 | 169 | 0.81652 | 0.77749 | 0.85341 |
| V1 | F1_A_SCAN | 175 | 175 | 175 | 175 | 0.9215 | 0.89084 | 0.94887 |
| V1 | F1_A_EVENT | 175 | 175 | 175 | 175 | 0.77264 | 0.72738 | 0.8174 |
| V1 | F2_A_APC | 175 | 175 | 175 | 175 | 0.82207 | 0.78367 | 0.85822 |
| V1 | F2_A_SCAN | 175 | 175 | 175 | 175 | 0.93234 | 0.90459 | 0.95706 |
| V1 | F2_A_EVENT | 175 | 175 | 175 | 175 | 0.78723 | 0.74468 | 0.82949 |
| V1 | F3_A_APC | 175 | 175 | 175 | 175 | 0.8273 | 0.78766 | 0.86338 |
| V1 | F3_A_SCAN | 175 | 175 | 175 | 175 | 0.93283 | 0.90537 | 0.95745 |
| V1 | F3_A_EVENT | 175 | 175 | 175 | 175 | 0.78658 | 0.7438 | 0.82903 |
| V1 | A2_prime_2D | 175 | 175 | 175 | 175 | 0.80914 | 0.76597 | 0.85035 |
| V1 | APC-v1.0 | 175 | 172 | 170 | 169 | 0.81652 | 0.77749 | 0.85341 |
| V1 | APC-v3.0 | 175 | 175 | 175 | 175 | 0.82207 | 0.78367 | 0.85822 |
| V2 | F1_A_APC | 450 | 113 | 80 | 46 | 0.92942 | 0.88995 | 0.96296 |
| V2 | F1_A_SCAN | 450 | 450 | 450 | 450 | 0.60655 | 0.57594 | 0.63587 |
| V2 | F1_A_EVENT | 450 | 450 | 450 | 450 | 0.51411 | 0.48626 | 0.54151 |
| V2 | F2_A_APC | 450 | 449 | 450 | 449 | 0.90837 | 0.88747 | 0.92765 |
| V2 | F2_A_SCAN | 450 | 449 | 450 | 449 | 0.91992 | 0.8993 | 0.93964 |
| V2 | F2_A_EVENT | 450 | 449 | 450 | 449 | 0.65628 | 0.63154 | 0.6814 |
| V2 | F3_A_APC | 450 | 449 | 449 | 449 | 0.94509 | 0.93099 | 0.95819 |
| V2 | F3_A_SCAN | 450 | 449 | 449 | 449 | 0.97842 | 0.9698 | 0.98608 |
| V2 | F3_A_EVENT | 450 | 449 | 449 | 449 | 0.68743 | 0.67021 | 0.70609 |
| V2 | A2_prime_2D | 450 | 450 | 450 | 450 | 0.8755 | 0.85415 | 0.89624 |
| V2 | APC-v1.0 | 450 | 113 | 80 | 46 | 0.92942 | 0.88995 | 0.96296 |
| V2 | APC-v3.0 | 450 | 449 | 450 | 449 | 0.90837 | 0.88747 | 0.92765 |


Full CSV: [coupling_auc.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\coupling_auc.csv).


## Calibrated specificity and power

| suite | dataset | n | valid | invalid | rejections | rate | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V1 | coupled | 175 | 175 | 0 | 111 | 0.63429 | 0.56075 | 0.70205 |
| V1 | timing_null | 175 | 175 | 0 | 16 | 0.091429 | 0.057062 | 0.14335 |
| V2 | coupled | 450 | 449 | 1 | 294 | 0.65333 | 0.60823 | 0.69584 |
| V2 | timing_null | 450 | 449 | 1 | 53 | 0.11778 | 0.091181 | 0.15085 |
| V3 | coupled | 500 | 500 | 0 | 45 | 0.09 | 0.067943 | 0.11831 |
| V3 | uncoupled | 100 | 100 | 0 | 5 | 0.05 | 0.021544 | 0.11175 |
| V4 | coupled | 25 | 25 | 0 | 21 | 0.84 | 0.65346 | 0.93597 |


Full CSV: [calibrated_specificity.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\calibrated_specificity.csv).


## End-to-end reference agreement

| suite | pipeline | reference | n | recovered_fp_hz_identical | recovered_fa_hz_identical | raw_mvl_identical | coupling_identical | status_identical |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V1 | F1_A_APC | APC-v1.0 | 350 | 350 | 350 | 350 | 350 | 350 |
| V1 | F2_A_APC | APC-v3.0 | 350 | 350 | 350 | 350 | 350 | 350 |
| V2 | F1_A_APC | APC-v1.0 | 900 | 900 | 900 | 900 | 900 | 900 |
| V2 | F2_A_APC | APC-v3.0 | 900 | 900 | 900 | 900 | 900 | 900 |
| V3 | F1_A_APC | APC-v1.0 | 600 | 600 | 600 | 600 | 600 | 600 |
| V3 | F2_A_APC | APC-v3.0 | 600 | 600 | 600 | 600 | 600 | 600 |
| V4 | F1_A_APC | APC-v1.0 | 25 | 25 | 25 | 25 | 25 | 25 |
| V4 | F2_A_APC | APC-v3.0 | 25 | 25 | 25 | 25 | 25 | 25 |


Full CSV: [endtoend_agreement.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\endtoend_agreement.csv).


## Finite Step-2 estimates after later APC failure: simulations

| suite | dataset | source | n | finite_step2 | finite_step2_later_failed |
| --- | --- | --- | --- | --- | --- |
| V1 | coupled | F1 | 175 | 175 | 3 |
| V1 | coupled | F2 | 175 | 175 | 0 |
| V1 | timing_null | F1 | 175 | 175 | 5 |
| V1 | timing_null | F2 | 175 | 175 | 0 |
| V2 | coupled | F1 | 450 | 450 | 337 |
| V2 | coupled | F2 | 450 | 449 | 0 |
| V2 | timing_null | F1 | 450 | 450 | 370 |
| V2 | timing_null | F2 | 450 | 450 | 0 |
| V3 | coupled | F1 | 500 | 500 | 0 |
| V3 | coupled | F2 | 500 | 500 | 0 |
| V3 | uncoupled | F1 | 100 | 100 | 0 |
| V3 | uncoupled | F2 | 100 | 100 | 0 |
| V4 | coupled | F1 | 25 | 25 | 0 |
| V4 | coupled | F2 | 25 | 25 | 0 |


Full CSV: [simulation_retained_step2_counts.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\simulation_retained_step2_counts.csv).


## Real-data reuse and statistics

Saved channels, bouts, eligibility, electrodes and prep files were reused unchanged. There are 3,646 unique rodent physical inputs, mapped to 3,982 regional/bout-set rows; the prespecified 5-s and POST HOC 2-s results remain separate. ECoG has 2,642 eligible bouts, 18 movement-recording patients and seven imagery-recording patients. The agreement denominator remains the prescribed 18, with observed patient counts shown separately.

Rodent APC-v1.0 reference values are retained from each original bout-set/analysis row. Saved A2' selected pairs are remeasured with the common ablation coupling phase rule. ECoG APC v1.0/v3.0 and A2' common coupling are reused from the completed ablation; the recomputed F3 / SCAN coordinates, status and coupling pass the user-resolved consistency check reported above. F1/F2 source counts reuse end-to-end statuses and recover missing Step-2 estimates only when needed.

Rodent per-session computations reuse the original statistical helper definitions and bout-bootstrap procedure: independent run/rest resampling, shared indices across methods, 10,000 resamples, seed 20261022. Across-session percentile bootstrap CIs resample session differences (10,000); one-sample t and signed-rank values are also provided. ECoG E4 uses the ablation procedure and patient bootstrap seed 20261024.


## Prespecified 5-s rodent: across sessions

| analysis | animal_pool | method | outcome | n_sessions | mean_session_difference | ci_low | ci_high | one_sample_p | wilcoxon_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | EC013 | A2_prime_2D | coupling | 3 | 0.010591 | 0.0059814 | 0.014802 | 0.053533 | 0.25 |
| CA1 | pooled | A2_prime_2D | coupling | 3 | 0.010591 | 0.0059814 | 0.014802 | 0.053533 | 0.25 |
| CA1 | EC013 | A2_prime_2D | recovered_fp_hz | 3 | 0.10713 | -1.0167 | 0.87941 | 0.86935 | 1 |
| CA1 | pooled | A2_prime_2D | recovered_fp_hz | 3 | 0.10713 | -1.0167 | 0.87941 | 0.86935 | 1 |
| CA1 | EC013 | APC-v1.0 | coupling | 3 | 0.015183 | 0.0064985 | 0.022449 | 0.082651 | 0.25 |
| CA1 | pooled | APC-v1.0 | coupling | 3 | 0.015183 | 0.0064985 | 0.022449 | 0.082651 | 0.25 |
| CA1 | EC013 | APC-v1.0 | recovered_fp_hz | 3 | 0.70585 | -0.56722 | 1.3473 | 0.38296 | 0.5 |
| CA1 | pooled | APC-v1.0 | recovered_fp_hz | 3 | 0.70585 | -0.56722 | 1.3473 | 0.38296 | 0.5 |
| CA1 | EC013 | F3_A_EVENT | coupling | 3 | 0.0063879 | 0.0010898 | 0.015641 | 0.30266 | 0.25 |
| CA1 | pooled | F3_A_EVENT | coupling | 3 | 0.0063879 | 0.0010898 | 0.015641 | 0.30266 | 0.25 |
| CA1 | EC013 | F3_A_EVENT | recovered_fp_hz | 3 | 0.22384 | -0.96281 | 0.9175 | 0.74339 | 1 |
| CA1 | pooled | F3_A_EVENT | recovered_fp_hz | 3 | 0.22384 | -0.96281 | 0.9175 | 0.74339 | 1 |
| CA1 | EC013 | F3_A_SCAN | coupling | 3 | 0.011937 | 0.007125 | 0.016194 | 0.045359 | 0.25 |
| CA1 | pooled | F3_A_SCAN | coupling | 3 | 0.011937 | 0.007125 | 0.016194 | 0.045359 | 0.25 |
| CA1 | EC013 | F3_A_SCAN | recovered_fp_hz | 3 | 0.22384 | -0.96281 | 0.9175 | 0.74339 | 1 |
| CA1 | pooled | F3_A_SCAN | recovered_fp_hz | 3 | 0.22384 | -0.96281 | 0.9175 | 0.74339 | 1 |
| E1_sensitivity | EC013 | A2_prime_2D | coupling | 3 | 0.040245 | 0.02348 | 0.055873 | 0.050149 | 0.25 |
| E1_sensitivity | pooled | A2_prime_2D | coupling | 3 | 0.040245 | 0.02348 | 0.055873 | 0.050149 | 0.25 |
| E1_sensitivity | EC013 | A2_prime_2D | recovered_fp_hz | 3 | 0.84311 | 0.34109 | 1.8 | 0.22022 | 0.25 |
| E1_sensitivity | pooled | A2_prime_2D | recovered_fp_hz | 3 | 0.84311 | 0.34109 | 1.8 | 0.22022 | 0.25 |
| E1_sensitivity | EC013 | APC-v1.0 | coupling | 3 | 0.039282 | 0.025438 | 0.04643 | 0.029685 | 0.25 |
| E1_sensitivity | pooled | APC-v1.0 | coupling | 3 | 0.039282 | 0.025438 | 0.04643 | 0.029685 | 0.25 |
| E1_sensitivity | EC013 | APC-v1.0 | recovered_fp_hz | 3 | 1.1791 | 1.0931 | 1.272 | 0.001921 | 0.25 |
| E1_sensitivity | pooled | APC-v1.0 | recovered_fp_hz | 3 | 1.1791 | 1.0931 | 1.272 | 0.001921 | 0.25 |
| E1_sensitivity | EC013 | F3_A_EVENT | coupling | 3 | 0.019842 | 0.0088877 | 0.025431 | 0.068471 | 0.25 |
| E1_sensitivity | pooled | F3_A_EVENT | coupling | 3 | 0.019842 | 0.0088877 | 0.025431 | 0.068471 | 0.25 |
| E1_sensitivity | EC013 | F3_A_EVENT | recovered_fp_hz | 3 | 0.74838 | 0.40078 | 0.94871 | 0.050288 | 0.25 |
| E1_sensitivity | pooled | F3_A_EVENT | recovered_fp_hz | 3 | 0.74838 | 0.40078 | 0.94871 | 0.050288 | 0.25 |
| E1_sensitivity | EC013 | F3_A_SCAN | coupling | 3 | 0.044242 | 0.036451 | 0.049928 | 0.008196 | 0.25 |
| E1_sensitivity | pooled | F3_A_SCAN | coupling | 3 | 0.044242 | 0.036451 | 0.049928 | 0.008196 | 0.25 |
| E1_sensitivity | EC013 | F3_A_SCAN | recovered_fp_hz | 3 | 0.74838 | 0.40078 | 0.94871 | 0.050288 | 0.25 |
| E1_sensitivity | pooled | F3_A_SCAN | recovered_fp_hz | 3 | 0.74838 | 0.40078 | 0.94871 | 0.050288 | 0.25 |
| EC | EC013 | A2_prime_2D | coupling | 3 | 0.03809 | 0.027349 | 0.051567 | 0.033244 | 0.25 |
| EC | pooled | A2_prime_2D | coupling | 3 | 0.03809 | 0.027349 | 0.051567 | 0.033244 | 0.25 |
| EC | EC013 | A2_prime_2D | recovered_fp_hz | 3 | 0.8782 | 0.57647 | 1.3333 | 0.063023 | 0.25 |
| EC | pooled | A2_prime_2D | recovered_fp_hz | 3 | 0.8782 | 0.57647 | 1.3333 | 0.063023 | 0.25 |
| EC | EC013 | APC-v1.0 | coupling | 3 | 0.027979 | 0.01962 | 0.037095 | 0.031169 | 0.25 |
| EC | pooled | APC-v1.0 | coupling | 3 | 0.027979 | 0.01962 | 0.037095 | 0.031169 | 0.25 |
| EC | EC013 | APC-v1.0 | recovered_fp_hz | 3 | 1.1768 | 1.0528 | 1.3374 | 0.0050736 | 0.25 |
| EC | pooled | APC-v1.0 | recovered_fp_hz | 3 | 1.1768 | 1.0528 | 1.3374 | 0.0050736 | 0.25 |
| EC | EC013 | F3_A_EVENT | coupling | 3 | 0.019581 | 0.013608 | 0.023717 | 0.023552 | 0.25 |
| EC | pooled | F3_A_EVENT | coupling | 3 | 0.019581 | 0.013608 | 0.023717 | 0.023552 | 0.25 |
| EC | EC013 | F3_A_EVENT | recovered_fp_hz | 3 | 0.68112 | 0.19461 | 0.95363 | 0.10783 | 0.25 |
| EC | pooled | F3_A_EVENT | recovered_fp_hz | 3 | 0.68112 | 0.19461 | 0.95363 | 0.10783 | 0.25 |
| EC | EC013 | F3_A_SCAN | coupling | 3 | 0.039875 | 0.033591 | 0.043502 | 0.0062003 | 0.25 |
| EC | pooled | F3_A_SCAN | coupling | 3 | 0.039875 | 0.033591 | 0.043502 | 0.0062003 | 0.25 |
| EC | EC013 | F3_A_SCAN | recovered_fp_hz | 3 | 0.68112 | 0.19461 | 0.95363 | 0.10783 | 0.25 |
| EC | pooled | F3_A_SCAN | recovered_fp_hz | 3 | 0.68112 | 0.19461 | 0.95363 | 0.10783 | 0.25 |


Full CSV: [rodent_across_session_statistics.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\rodent_across_session_statistics.csv).


## POST HOC 2-s rodent: across sessions

| analysis | animal_pool | method | outcome | n_sessions | mean_session_difference | ci_low | ci_high | one_sample_p | wilcoxon_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | EC013 | A2_prime_2D | coupling | 9 | 0.0082403 | 0.0020112 | 0.014621 | 0.042324 | 0.074219 |
| CA1 | pooled | A2_prime_2D | coupling | 9 | 0.0082403 | 0.0021115 | 0.014429 | 0.042324 | 0.074219 |
| CA1 | EC013 | A2_prime_2D | recovered_fp_hz | 9 | -0.25424 | -0.40396 | -0.099585 | 0.016269 | 0.027344 |
| CA1 | pooled | A2_prime_2D | recovered_fp_hz | 9 | -0.25424 | -0.40475 | -0.094374 | 0.016269 | 0.027344 |
| CA1 | EC013 | APC-v1.0 | coupling | 9 | 0.0036052 | -0.0026682 | 0.0096172 | 0.30648 | 0.30078 |
| CA1 | pooled | APC-v1.0 | coupling | 9 | 0.0036052 | -0.0025876 | 0.0094917 | 0.30648 | 0.30078 |
| CA1 | EC013 | APC-v1.0 | recovered_fp_hz | 9 | 0.99023 | 0.5241 | 1.2915 | 0.0022357 | 0.0078125 |
| CA1 | pooled | APC-v1.0 | recovered_fp_hz | 9 | 0.99023 | 0.52065 | 1.2936 | 0.0022357 | 0.0078125 |
| CA1 | EC013 | F3_A_EVENT | coupling | 9 | 0.0079993 | 0.0041906 | 0.011788 | 0.0049373 | 0.011719 |
| CA1 | pooled | F3_A_EVENT | coupling | 9 | 0.0079993 | 0.0042268 | 0.011828 | 0.0049373 | 0.011719 |
| CA1 | EC013 | F3_A_EVENT | recovered_fp_hz | 9 | -1.1482 | -2.0867 | -0.29962 | 0.044907 | 0.027344 |
| CA1 | pooled | F3_A_EVENT | recovered_fp_hz | 9 | -1.1482 | -2.0761 | -0.30141 | 0.044907 | 0.027344 |
| CA1 | EC013 | F3_A_SCAN | coupling | 9 | 0.015504 | 0.011153 | 0.019485 | 0.00014753 | 0.0039062 |
| CA1 | pooled | F3_A_SCAN | coupling | 9 | 0.015504 | 0.011205 | 0.019522 | 0.00014753 | 0.0039062 |
| CA1 | EC013 | F3_A_SCAN | recovered_fp_hz | 9 | -1.1482 | -2.0798 | -0.31805 | 0.044907 | 0.027344 |
| CA1 | pooled | F3_A_SCAN | recovered_fp_hz | 9 | -1.1482 | -2.082 | -0.30621 | 0.044907 | 0.027344 |
| E1_sensitivity | EC013 | A2_prime_2D | coupling | 9 | 0.025605 | 0.020786 | 0.031271 | 2.0457e-05 | 0.0039062 |
| E1_sensitivity | pooled | A2_prime_2D | coupling | 9 | 0.025605 | 0.020725 | 0.031341 | 2.0457e-05 | 0.0039062 |
| E1_sensitivity | EC013 | A2_prime_2D | recovered_fp_hz | 9 | 0.71035 | 0.48425 | 0.96875 | 0.00070781 | 0.0039062 |
| E1_sensitivity | pooled | A2_prime_2D | recovered_fp_hz | 9 | 0.71035 | 0.48388 | 0.96904 | 0.00070781 | 0.0039062 |
| E1_sensitivity | EC013 | APC-v1.0 | coupling | 9 | 0.031764 | 0.028494 | 0.034916 | 8.3079e-08 | 0.0039062 |
| E1_sensitivity | pooled | APC-v1.0 | coupling | 9 | 0.031764 | 0.028455 | 0.034876 | 8.3079e-08 | 0.0039062 |
| E1_sensitivity | EC013 | APC-v1.0 | recovered_fp_hz | 9 | 1.1617 | 1.0647 | 1.2678 | 2.9797e-08 | 0.0039062 |
| E1_sensitivity | pooled | APC-v1.0 | recovered_fp_hz | 9 | 1.1617 | 1.0647 | 1.2688 | 2.9797e-08 | 0.0039062 |
| E1_sensitivity | EC013 | F3_A_EVENT | coupling | 9 | 0.018322 | 0.015167 | 0.021416 | 4.565e-06 | 0.0039062 |
| E1_sensitivity | pooled | F3_A_EVENT | coupling | 9 | 0.018322 | 0.015167 | 0.021461 | 4.565e-06 | 0.0039062 |
| E1_sensitivity | EC013 | F3_A_EVENT | recovered_fp_hz | 9 | 0.19496 | -0.17073 | 0.5684 | 0.36357 | 0.42578 |
| E1_sensitivity | pooled | F3_A_EVENT | recovered_fp_hz | 9 | 0.19496 | -0.16874 | 0.57193 | 0.36357 | 0.42578 |
| E1_sensitivity | EC013 | F3_A_SCAN | coupling | 9 | 0.043664 | 0.038562 | 0.048387 | 1.9295e-07 | 0.0039062 |
| E1_sensitivity | pooled | F3_A_SCAN | coupling | 9 | 0.043664 | 0.038599 | 0.048387 | 1.9295e-07 | 0.0039062 |
| E1_sensitivity | EC013 | F3_A_SCAN | recovered_fp_hz | 9 | 0.19496 | -0.17127 | 0.56969 | 0.36357 | 0.42578 |
| E1_sensitivity | pooled | F3_A_SCAN | recovered_fp_hz | 9 | 0.19496 | -0.17463 | 0.56552 | 0.36357 | 0.42578 |
| EC | EC012 | A2_prime_2D | coupling | 9 | -0.00018883 | -0.0071664 | 0.0065517 | 0.96059 | 1 |
| EC | EC013 | A2_prime_2D | coupling | 9 | 0.026151 | 0.021822 | 0.031117 | 6.2977e-06 | 0.0039062 |
| EC | pooled | A2_prime_2D | coupling | 18 | 0.012981 | 0.0055453 | 0.020173 | 0.0037073 | 0.0047455 |
| EC | EC012 | A2_prime_2D | recovered_fp_hz | 9 | 0.22137 | -0.12553 | 0.55863 | 0.26264 | 0.35938 |
| EC | EC013 | A2_prime_2D | recovered_fp_hz | 9 | 0.70894 | 0.51414 | 0.91887 | 0.0002015 | 0.0039062 |
| EC | pooled | A2_prime_2D | recovered_fp_hz | 18 | 0.46516 | 0.23216 | 0.68409 | 0.0011749 | 0.0023346 |
| EC | EC012 | APC-v1.0 | coupling | 9 | 0.012662 | 0.0061783 | 0.01938 | 0.0081464 | 0.0039062 |
| EC | EC013 | APC-v1.0 | coupling | 9 | 0.029174 | 0.024063 | 0.034201 | 6.3587e-06 | 0.0039062 |
| EC | pooled | APC-v1.0 | coupling | 18 | 0.020918 | 0.014998 | 0.026466 | 2.1738e-06 | 7.6294e-06 |
| EC | EC012 | APC-v1.0 | recovered_fp_hz | 9 | 2.5977 | 2.3878 | 2.7967 | 1.1607e-08 | 0.0039062 |
| EC | EC013 | APC-v1.0 | recovered_fp_hz | 9 | 1.1123 | 1.0093 | 1.2173 | 4.9758e-08 | 0.0039062 |
| EC | pooled | APC-v1.0 | recovered_fp_hz | 18 | 1.855 | 1.4957 | 2.2186 | 2.197e-08 | 7.6294e-06 |
| EC | EC012 | F3_A_EVENT | coupling | 9 | -0.0068018 | -0.012815 | -0.0011754 | 0.063457 | 0.074219 |
| EC | EC013 | F3_A_EVENT | coupling | 9 | 0.018633 | 0.015787 | 0.021073 | 1.208e-06 | 0.0039062 |
| EC | pooled | F3_A_EVENT | coupling | 18 | 0.0059157 | -0.0011033 | 0.012521 | 0.11058 | 0.11871 |
| EC | EC012 | F3_A_EVENT | recovered_fp_hz | 9 | 1.4708 | 1.1185 | 1.8346 | 7.2585e-05 | 0.0039062 |
| EC | EC013 | F3_A_EVENT | recovered_fp_hz | 9 | 0.15266 | -0.1803 | 0.50872 | 0.44048 | 0.57031 |
| EC | pooled | F3_A_EVENT | recovered_fp_hz | 18 | 0.81175 | 0.41773 | 1.2153 | 0.0011209 | 0.0015793 |
| EC | EC012 | F3_A_SCAN | coupling | 9 | 0.024112 | 0.016701 | 0.030771 | 0.00022616 | 0.0039062 |
| EC | EC013 | F3_A_SCAN | coupling | 9 | 0.043583 | 0.037349 | 0.04888 | 6.3964e-07 | 0.0039062 |
| EC | pooled | F3_A_SCAN | coupling | 18 | 0.033847 | 0.027329 | 0.040006 | 1.3611e-08 | 7.6294e-06 |
| EC | EC012 | F3_A_SCAN | recovered_fp_hz | 9 | 1.4708 | 1.1097 | 1.8373 | 7.2585e-05 | 0.0039062 |
| EC | EC013 | F3_A_SCAN | recovered_fp_hz | 9 | 0.15266 | -0.18682 | 0.50938 | 0.44048 | 0.57031 |
| EC | pooled | F3_A_SCAN | recovered_fp_hz | 18 | 0.81175 | 0.42221 | 1.2189 | 0.0011209 | 0.0015793 |


Full CSV: [rodent_across_session_statistics.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\rodent_across_session_statistics.csv).


## Prespecified 5-s rodent: within-state fP SD

| analysis | animal_pool | method | state | n_sessions | mean_fp_sd | median_fp_sd |
| --- | --- | --- | --- | --- | --- | --- |
| CA1 | EC013 | A2_prime_2D | rest | 3 | 2.1821 | 2.267 |
| CA1 | pooled | A2_prime_2D | rest | 3 | 2.1821 | 2.267 |
| CA1 | EC013 | A2_prime_2D | run | 3 | 2.0252 | 2.5348 |
| CA1 | pooled | A2_prime_2D | run | 3 | 2.0252 | 2.5348 |
| CA1 | EC013 | APC-v1.0 | rest | 3 | 2.7589 | 0.52343 |
| CA1 | pooled | APC-v1.0 | rest | 3 | 2.7589 | 0.52343 |
| CA1 | EC013 | APC-v1.0 | run | 3 | 1.3023 | 0.29565 |
| CA1 | pooled | APC-v1.0 | run | 3 | 1.3023 | 0.29565 |
| CA1 | EC013 | F3_A_EVENT | rest | 3 | 3.0033 | 1.0539 |
| CA1 | pooled | F3_A_EVENT | rest | 3 | 3.0033 | 1.0539 |
| CA1 | EC013 | F3_A_EVENT | run | 3 | 2.0771 | 0.29396 |
| CA1 | pooled | F3_A_EVENT | run | 3 | 2.0771 | 0.29396 |
| CA1 | EC013 | F3_A_SCAN | rest | 3 | 3.0033 | 1.0539 |
| CA1 | pooled | F3_A_SCAN | rest | 3 | 3.0033 | 1.0539 |
| CA1 | EC013 | F3_A_SCAN | run | 3 | 2.0771 | 0.29396 |
| CA1 | pooled | F3_A_SCAN | run | 3 | 2.0771 | 0.29396 |
| E1_sensitivity | EC013 | A2_prime_2D | rest | 3 | 1.5568 | 1.6071 |
| E1_sensitivity | pooled | A2_prime_2D | rest | 3 | 1.5568 | 1.6071 |
| E1_sensitivity | EC013 | A2_prime_2D | run | 3 | 1.5128 | 1.4376 |
| E1_sensitivity | pooled | A2_prime_2D | run | 3 | 1.5128 | 1.4376 |
| E1_sensitivity | EC013 | APC-v1.0 | rest | 3 | 0.80128 | 0.47438 |
| E1_sensitivity | pooled | APC-v1.0 | rest | 3 | 0.80128 | 0.47438 |
| E1_sensitivity | EC013 | APC-v1.0 | run | 3 | 0.22743 | 0.22583 |
| E1_sensitivity | pooled | APC-v1.0 | run | 3 | 0.22743 | 0.22583 |
| E1_sensitivity | EC013 | F3_A_EVENT | rest | 3 | 0.73694 | 0.50879 |
| E1_sensitivity | pooled | F3_A_EVENT | rest | 3 | 0.73694 | 0.50879 |
| E1_sensitivity | EC013 | F3_A_EVENT | run | 3 | 0.23698 | 0.26292 |
| E1_sensitivity | pooled | F3_A_EVENT | run | 3 | 0.23698 | 0.26292 |
| E1_sensitivity | EC013 | F3_A_SCAN | rest | 3 | 0.73694 | 0.50879 |
| E1_sensitivity | pooled | F3_A_SCAN | rest | 3 | 0.73694 | 0.50879 |
| E1_sensitivity | EC013 | F3_A_SCAN | run | 3 | 0.23698 | 0.26292 |
| E1_sensitivity | pooled | F3_A_SCAN | run | 3 | 0.23698 | 0.26292 |
| EC | EC013 | A2_prime_2D | rest | 3 | 1.4027 | 1.5613 |
| EC | pooled | A2_prime_2D | rest | 3 | 1.4027 | 1.5613 |
| EC | EC013 | A2_prime_2D | run | 3 | 1.6688 | 1.8028 |
| EC | pooled | A2_prime_2D | run | 3 | 1.6688 | 1.8028 |
| EC | EC013 | APC-v1.0 | rest | 3 | 0.83934 | 0.45957 |
| EC | pooled | APC-v1.0 | rest | 3 | 0.83934 | 0.45957 |
| EC | EC013 | APC-v1.0 | run | 3 | 0.21023 | 0.19333 |
| EC | pooled | APC-v1.0 | run | 3 | 0.21023 | 0.19333 |
| EC | EC013 | F3_A_EVENT | rest | 3 | 0.54366 | 0.5082 |
| EC | pooled | F3_A_EVENT | rest | 3 | 0.54366 | 0.5082 |
| EC | EC013 | F3_A_EVENT | run | 3 | 0.23624 | 0.25785 |
| EC | pooled | F3_A_EVENT | run | 3 | 0.23624 | 0.25785 |
| EC | EC013 | F3_A_SCAN | rest | 3 | 0.54366 | 0.5082 |
| EC | pooled | F3_A_SCAN | rest | 3 | 0.54366 | 0.5082 |
| EC | EC013 | F3_A_SCAN | run | 3 | 0.23624 | 0.25785 |
| EC | pooled | F3_A_SCAN | run | 3 | 0.23624 | 0.25785 |


Full CSV: [rodent_within_state_summary.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\rodent_within_state_summary.csv).


## POST HOC 2-s rodent: within-state fP SD

| analysis | animal_pool | method | state | n_sessions | mean_fp_sd | median_fp_sd |
| --- | --- | --- | --- | --- | --- | --- |
| CA1 | EC013 | A2_prime_2D | rest | 9 | 1.8686 | 1.7398 |
| CA1 | pooled | A2_prime_2D | rest | 9 | 1.8686 | 1.7398 |
| CA1 | EC013 | A2_prime_2D | run | 9 | 1.6457 | 1.6644 |
| CA1 | pooled | A2_prime_2D | run | 9 | 1.6457 | 1.6644 |
| CA1 | EC013 | APC-v1.0 | rest | 9 | 2.0232 | 1.0594 |
| CA1 | pooled | APC-v1.0 | rest | 9 | 2.0232 | 1.0594 |
| CA1 | EC013 | APC-v1.0 | run | 9 | 1.2038 | 0.29635 |
| CA1 | pooled | APC-v1.0 | run | 9 | 1.2038 | 0.29635 |
| CA1 | EC013 | F3_A_EVENT | rest | 9 | 5.5269 | 5.2155 |
| CA1 | pooled | F3_A_EVENT | rest | 9 | 5.5269 | 5.2155 |
| CA1 | EC013 | F3_A_EVENT | run | 9 | 1.8086 | 0.3297 |
| CA1 | pooled | F3_A_EVENT | run | 9 | 1.8086 | 0.3297 |
| CA1 | EC013 | F3_A_SCAN | rest | 9 | 5.5269 | 5.2155 |
| CA1 | pooled | F3_A_SCAN | rest | 9 | 5.5269 | 5.2155 |
| CA1 | EC013 | F3_A_SCAN | run | 9 | 1.8086 | 0.3297 |
| CA1 | pooled | F3_A_SCAN | run | 9 | 1.8086 | 0.3297 |
| E1_sensitivity | EC013 | A2_prime_2D | rest | 9 | 1.6333 | 1.6921 |
| E1_sensitivity | pooled | A2_prime_2D | rest | 9 | 1.6333 | 1.6921 |
| E1_sensitivity | EC013 | A2_prime_2D | run | 9 | 1.855 | 1.86 |
| E1_sensitivity | pooled | A2_prime_2D | run | 9 | 1.855 | 1.86 |
| E1_sensitivity | EC013 | APC-v1.0 | rest | 9 | 0.81326 | 0.88729 |
| E1_sensitivity | pooled | APC-v1.0 | rest | 9 | 0.81326 | 0.88729 |
| E1_sensitivity | EC013 | APC-v1.0 | run | 9 | 0.28146 | 0.28375 |
| E1_sensitivity | pooled | APC-v1.0 | run | 9 | 0.28146 | 0.28375 |
| E1_sensitivity | EC013 | F3_A_EVENT | rest | 9 | 2.5652 | 2.6973 |
| E1_sensitivity | pooled | F3_A_EVENT | rest | 9 | 2.5652 | 2.6973 |
| E1_sensitivity | EC013 | F3_A_EVENT | run | 9 | 0.3089 | 0.35157 |
| E1_sensitivity | pooled | F3_A_EVENT | run | 9 | 0.3089 | 0.35157 |
| E1_sensitivity | EC013 | F3_A_SCAN | rest | 9 | 2.5652 | 2.6973 |
| E1_sensitivity | pooled | F3_A_SCAN | rest | 9 | 2.5652 | 2.6973 |
| E1_sensitivity | EC013 | F3_A_SCAN | run | 9 | 0.3089 | 0.35157 |
| E1_sensitivity | pooled | F3_A_SCAN | run | 9 | 0.3089 | 0.35157 |
| EC | EC012 | A2_prime_2D | rest | 9 | 1.8366 | 1.7955 |
| EC | EC013 | A2_prime_2D | rest | 9 | 1.5441 | 1.5403 |
| EC | pooled | A2_prime_2D | rest | 18 | 1.6903 | 1.6637 |
| EC | EC012 | A2_prime_2D | run | 9 | 2.1376 | 2.2375 |
| EC | EC013 | A2_prime_2D | run | 9 | 1.8567 | 1.8692 |
| EC | pooled | A2_prime_2D | run | 18 | 1.9972 | 1.9076 |
| EC | EC012 | APC-v1.0 | rest | 9 | 1.1463 | 1.0342 |
| EC | EC013 | APC-v1.0 | rest | 9 | 0.78249 | 0.74664 |
| EC | pooled | APC-v1.0 | rest | 18 | 0.96441 | 0.99163 |
| EC | EC012 | APC-v1.0 | run | 9 | 0.21423 | 0.18826 |
| EC | EC013 | APC-v1.0 | run | 9 | 0.2758 | 0.29572 |
| EC | pooled | APC-v1.0 | run | 18 | 0.24502 | 0.24948 |
| EC | EC012 | F3_A_EVENT | rest | 9 | 2.1721 | 1.5301 |
| EC | EC013 | F3_A_EVENT | rest | 9 | 2.7695 | 2.8625 |
| EC | pooled | F3_A_EVENT | rest | 18 | 2.4708 | 2.6338 |
| EC | EC012 | F3_A_EVENT | run | 9 | 0.22097 | 0.19832 |
| EC | EC013 | F3_A_EVENT | run | 9 | 0.30635 | 0.3521 |
| EC | pooled | F3_A_EVENT | run | 18 | 0.26366 | 0.2586 |
| EC | EC012 | F3_A_SCAN | rest | 9 | 2.1721 | 1.5301 |
| EC | EC013 | F3_A_SCAN | rest | 9 | 2.7695 | 2.8625 |
| EC | pooled | F3_A_SCAN | rest | 18 | 2.4708 | 2.6338 |
| EC | EC012 | F3_A_SCAN | run | 9 | 0.22097 | 0.19832 |
| EC | EC013 | F3_A_SCAN | run | 9 | 0.30635 | 0.3521 |
| EC | pooled | F3_A_SCAN | run | 18 | 0.26366 | 0.2586 |


Full CSV: [rodent_within_state_summary.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\rodent_within_state_summary.csv).


## ECoG descriptive endpoints

| recording | method | patients | rest_agreement_count | rest_agreement_denominator | mean_move_minus_rest | ci_low | ci_high | median_rest_fp_sd | median_move_fp_sd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| movement | F3_A_SCAN | 18 | 15 | 18 | 0.00047751 | -0.0042149 | 0.0055257 | 5.4548 | 6.051 |
| movement | F3_A_EVENT | 18 | 15 | 18 | 0.0025825 | -0.0017572 | 0.0068692 | 5.4548 | 6.051 |
| movement | APC-v1.0 | 18 | 5 | 18 | 0.0024595 | -0.0019042 | 0.0067154 | 3.5918 | 3.358 |
| movement | APC-v3.0 | 18 | 13 | 18 | -0.0023318 | -0.0073147 | 0.0028223 | 5.839 | 6.4893 |
| movement | A2_prime_2D | 18 | 2 | 18 | 0.0016657 | -0.0022051 | 0.005656 | 3.9604 | 4.2073 |
| imagery | F3_A_SCAN | 7 | 7 | 18 | 0.0022025 | -0.00099368 | 0.0049382 | 4.9517 | 5.7616 |
| imagery | F3_A_EVENT | 7 | 7 | 18 | -0.0034914 | -0.0090397 | 0.0022482 | 4.9517 | 5.7616 |
| imagery | APC-v1.0 | 7 | 2 | 18 | 0.0011867 | -0.0040066 | 0.005906 | 3.2173 | 3.2445 |
| imagery | APC-v3.0 | 7 | 6 | 18 | 0.00037672 | -0.00095774 | 0.0016602 | 6.0165 | 6.3174 |
| imagery | A2_prime_2D | 7 | 1 | 18 | 0.0031107 | -0.0025641 | 0.0081456 | 4.6603 | 4.4485 |


Full CSV: [ecog_summary.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\ecog_summary.csv).


## Finite Step-2 estimates after later APC failure: real data

| dataset | bout_set | analysis | source | n | finite_step2 | finite_step2_later_failed | recording |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Rodent | prespecified_5s | EC | F1 | 112 | 112 | 0 | NA |
| Rodent | prespecified_5s | EC | F2 | 112 | 112 | 0 | NA |
| Rodent | prespecified_5s | CA1 | F1 | 112 | 112 | 2 | NA |
| Rodent | prespecified_5s | CA1 | F2 | 112 | 111 | 0 | NA |
| Rodent | prespecified_5s | E1_sensitivity | F1 | 112 | 112 | 1 | NA |
| Rodent | prespecified_5s | E1_sensitivity | F2 | 112 | 112 | 0 | NA |
| Rodent | POST_HOC_2s | CA1 | F1 | 986 | 986 | 46 | NA |
| Rodent | POST_HOC_2s | CA1 | F2 | 986 | 984 | 0 | NA |
| Rodent | POST_HOC_2s | E1_sensitivity | F1 | 986 | 986 | 20 | NA |
| Rodent | POST_HOC_2s | E1_sensitivity | F2 | 986 | 986 | 0 | NA |
| Rodent | POST_HOC_2s | EC | F1 | 1674 | 1674 | 55 | NA |
| Rodent | POST_HOC_2s | EC | F2 | 1674 | 1674 | 0 | NA |
| ECoG | NA | NA | F1 | 1809 | 1809 | 0 | movement |
| ECoG | NA | NA | F2 | 1809 | 1787 | 1 | movement |
| ECoG | NA | NA | F1 | 833 | 833 | 0 | imagery |
| ECoG | NA | NA | F2 | 833 | 826 | 0 | imagery |


Full CSV: [real_retained_step2_counts.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\real_retained_step2_counts.csv).


## Detailed tables

- [recovery_by_level.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\recovery_by_level.csv)

- [simulation_trial_estimates.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\simulation_trial_estimates.csv)

- [simulation_truths.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\simulation_truths.csv)

- [calibrated_trial_tests.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\calibrated_trial_tests.csv)

- [coupling_auc_bootstrap.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\coupling_auc_bootstrap.csv)

- [rodent_bout_estimates.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\rodent_bout_estimates.csv)

- [rodent_session_statistics.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\rodent_session_statistics.csv)

- [rodent_state_summary.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\rodent_state_summary.csv)

- [rodent_within_state_spread.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\rodent_within_state_spread.csv)

- [rodent_sources.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\rodent_sources.csv)

- [ecog_bout_estimates.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\ecog_bout_estimates.csv)

- [ecog_patient_summary.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\ecog_patient_summary.csv)

- [ecog_patient_bootstrap.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\ecog_patient_bootstrap.csv)

- [ecog_sources.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\ecog_sources.csv)

- [statistics.csv](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\statistics.csv)


## Figures

- figure1_recovery: [300-dpi PNG](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\figure1_recovery.png), [SVG](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\figure1_recovery.svg). Commit and source-CSV hashes are embedded in metadata; no titles or footers appear inside the image.

- figure2_specificity: [300-dpi PNG](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\figure2_specificity.png), [SVG](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\figure2_specificity.svg). Commit and source-CSV hashes are embedded in metadata; no titles or footers appear inside the image.

- figure3_rodent_fp: [300-dpi PNG](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\figure3_rodent_fp.png), [SVG](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\figure3_rodent_fp.svg). Commit and source-CSV hashes are embedded in metadata; no titles or footers appear inside the image.

- figure4_ecog_rest: [300-dpi PNG](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\figure4_ecog_rest.png), [SVG](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\figure4_ecog_rest.svg). Commit and source-CSV hashes are embedded in metadata; no titles or footers appear inside the image.


## Runtime and deviations

Statistics elapsed: 45.966 seconds. Gate elapsed: 79.889 seconds. Generator elapsed: 48.337 seconds after the tooling restart. Worker runtimes are recorded individually below.

| stage | worker | seconds |
| --- | --- | --- |
| worker | 1 | 7488.8 |
| real_worker | 1 | 1332.4 |
| worker | 2 | 7478.9 |
| real_worker | 2 | 1316.6 |
| worker | 3 | 7461.2 |
| real_worker | 3 | 1148.8 |
| worker | 4 | 7475.8 |
| real_worker | 4 | 953.24 |

Statistics runtime basis: original statistics subprocess wall start to error-log modification; no statistical calculations repeated. Metadata-only collation recovery: 0.6893069999641739 seconds. No numerical statistical calculation was repeated.


Wall time since Amendment-1 resume: 20043.3 seconds (5.568 hours), including interruptions. Real-worker times above describe the successful ECoG resume, including checkpoint restoration; earlier rodent processing and the stopped CSV-conversion attempt are retained in tooling_saved_boolean_attempt1/worker*_resume_matlab.log. They are not included in those resumed-worker timers.


- **GEN_METADATA_SEED_SCOPE**: Seed was parameterized in a local metadata function but omitted from its formal/call arguments. Pass unchanged seed to verification_row; preserve and compare the already-written configuration on resume.


- **SAVED_RODENT_CSV_PRECISION**: Exact deduplication of shared physical inputs incorrectly required equality of rounded raw/phase/coupling CSV fields. Shared physical bounds, fP, fA and status match exactly; raw values were written at different precision. Preserve every original reference row by bout-set and analysis, keep one physical reference for computation, and audit all numeric CSV differences separately.


- **DIAGNOSTIC_STRUCT_CONTAINER**: MATLAB rejected subscripted assignment while building the diagnostic agreement structure. Use a cell container for agreement metadata; no method computations, options or numeric criteria changed.


- **SAVED_BOOLEAN_CSV_PARSE**: MATLAB readtable returns saved True/False valid values as string; logical(string) is unsupported. All four workers stopped at their first ECoG reference row, before saving an ECoG checkpoint. Parse saved true/false and 1/0 explicitly; numeric/logical values retain their original conversion. No estimator, options, reproduction assert or numerical criterion changed.


- **ECOG_EXECUTOR_REPRODUCTION_PRECISION**: Executor-added saved-ablation F3/SCAN 1e-10 absolute tolerance was tighter than numerical precision. User resolved STOPPED_ACTIVE.md: floating-point propagation through the narrow low-frequency phase filter; not a protocol gate or method change. fA, status, validity and NaN pattern identical; fP absolute difference <=1e-9 Hz; coupling absolute difference <=1e-6*max(abs(saved coupling),1e-12). Record per-bout absolute/relative fP and coupling differences. Use STOP_RUN.md for future stops while both earlier stop records remain unchanged.


- **REPORT_LITERAL_QUOTE_PRECHECK**: The pre-execution Python parse check found an unescaped apostrophe in newly added report prose. No statistics or report had executed. Spell A2-prime in that prose; all edited Python scripts now parse. No numerical code or output changed.


- **STATISTICS_COLLATION_COLUMN_COLLISION**: All simulations() and real_data() calculations completed and wrote their tables. Final collation attempted to insert endpoint into calibrated_specificity.csv, which already has its false_positive_rate/power endpoint field. Pandas raised cannot insert endpoint, already exists. Use endpoint_family for the combined-table family label. Complete collation and completion metadata from the existing CSVs only. Do not rerun simulations(), real_data(), tests or bootstraps. Verify all 28 already computed CSV hashes remain unchanged.


- **MATPLOTLIB_FONT_CACHE_PATH**: Initial rendering succeeded but Matplotlib could not save its font cache under C:/Users/nghare/.matplotlib because that location was not writable. Set MPLCONFIGDIR to the work-folder matplotlib_cache directory; rerender figures/report from the unchanged statistical CSVs only. No estimation, test or bootstrap repeated.


No protocol, tagged method, seed, grid or protocol-gate tolerance was changed. The executor-added ECoG consistency tolerance was changed only as directly authorized and documented above. New validation results are uncommitted. Provenance, input/source hashes, implementation hashes and environment versions are in [provenance.json](C:\Users\nghare\.brainstorm\process\revision_checks\paper2_validation\provenance.json).

- **REVIEW_CONSOLE_ENCODING**: The auxiliary condensed review table was written successfully as UTF-8, but printing a prime symbol to the default cp1252 console raised UnicodeEncodeError. Use UTF-8 for console output; no table, figure, estimator, test or bootstrap calculation changed.

## Final verification

PASS at 2026-10-24T17:05:22.152446+00:00: clean paper2 tree; frozen source and input hashes unchanged; both stop records and all 5560 pre-resume checkpoints preserved; all 28 pre-collation statistical CSVs unchanged; 1875 simulation inputs, 15928 rodent analysis rows, 2642 ECoG bouts, and four figures verified. Statistical tests and bootstraps executed once. New validation results are uncommitted.

[Verification](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_validation/final_verification.json) · [Visual QA](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_validation/visual_qa.json) · [Condensed review tables](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_validation/REVIEW_TABLES.md) · [Output manifest](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_validation/output_manifest.json).
