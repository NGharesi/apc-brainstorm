# Paper 2: prespecified APC component ablation

## Factual summary

- All 2,642 recomputed ECoG v1 references passed the five-field saved-value checks.
- HA joint recovery, A_APC/A_SCAN: F1: 43/63, F2: 101/301, F3: 129/350; denominator 450.
- H1 joint recovery, A_APC/A_SCAN: F1: 120/154, F2: 124/160, F3: 126/160; denominator 175.
- The prespecified E1 decision is “it does not” for both HA and H1; all three sources favor A_SCAN after Holm correction.
- Nine methods were reported for 1,575 simulation inputs and 2,642 ECoG bouts.
- Movement data cover 18 eligible patients; imagery data are available for 7 of those patients.
- Tagged source and simulation files are unchanged; no ablation results were committed.

Commit `ea8b3704a41ebdd445931e7afbfb2ffacc6bca14` on `paper2`; protocol SHA-256 `4981cdaa0531a1418c3ba42523e6d61c45c63b70c89e13a82fdf3867d5b0bbcf`. Amendments 1 and 2 were pushed to origin before the gates. Tagged source files match v3.0 byte-for-byte. The NeuroImage branch remains `815ac24154385a3b4e7e5acbe9daf65c941adfb7`. No ablation results were committed.

## Archive and provenance

The v3 evaluation archive is committed and public at `dce410175ffeffa26dd3882e85e4d94412d2875b` in `analysis/paper2/v3_aperiodic/`: 432 copied files, including 26 gzipped CSVs; no MAT checkpoints or signal banks. Archive byte hashes and staged blob hashes were verified. See `archive_record.json` and the archive manifest/README. MATLAB: 9.13.0.2105380 (R2022b) Update 2; full toolbox versions and helper hashes are in `provenance.json`.

## Gates and identical inputs

APC extraction: 42/42 passed; scan score-column extraction: 23/23 passed. Maximum absolute difference was zero in every comparison. APC cases comprise the canonical input and first 20 HA coupled trials for both v1 and v3. Matching NaN patterns/statuses are reported alongside finite comparisons; see `gate_apc.csv` and `gate_scan.csv`.

The finite-value gate passed in all 22 cases with final estimates. The other 20 cases reproduce the original nonfinite failure pattern; they are not counted as finite numerical comparisons.

| suite | version | n | finite_comparisons | matching_nonfinite_failures | max_abs_error |
|---|---|---|---|---|---|
| canonical | v1 | 1 | 1 | 0 | 0 |
| canonical | v3 | 1 | 1 | 0 | 0 |
| HA | v1 | 20 | 1 | 19 | 0 |
| HA | v3 | 20 | 19 | 1 | 0 |

HB: 675 regenerated complete cases are bit-identical to both the v3 input bank and the original v2 held-out bank. HA reuses all 900 saved inputs unchanged. ECoG reuses saved prep signals, channel selection and bout boundaries, restricted to the original 18 eligible patients; imagery is secondary.

## Attempt 1 (ECoG CSV reference)

The prior run stopped at the raw-MVL reconstruction check. Its ECoG v1 reference used `csvref` to derive an amplitude band absent from the saved CSV. The user identified this tooling defect from the code without inspecting an outcome and authorized its one-time correction under section 5. The stopped report is preserved as `STOPPED_attempt1.md`. The two partial ECoG bouts were moved unchanged to `stopped_attempt1/` and excluded from this run.

Each reported ECoG v1 reference was recomputed once on the identical bout with the original options (fA 80–150 Hz, phase 6–30 Hz). Its exact returned `info.final_band_hz` and route were retained. Cached reference runs and five-field saved-row checks are in `ecog_v1_references/` and `ecog_v1_reproduction.csv`. The raw-MVL reconstruction tolerance remains 1e-10. The HA/HB inputs, simulation estimates, and ECoG v3 references were unchanged. Wrapper assertions flush both values, source index and bout key to JSON before raising. See `ecog_v1_reference_fix.diff`, `deviations.json`, and `ecog_reference_resume_preservation.json`.

| field | n | finite_comparisons | matching_nonfinite | max_abs_error | tolerance | passed |
|---|---|---|---|---|---|---|
| fp_hz | 2642 | 2642 | 0 | 4.97e-14 | 1e-10 | 2642 |
| fa_hz | 2642 | 2642 | 0 | 0 | 0 | 2642 |
| raw_mvl | 2642 | 2642 | 0 | 5e-16 | 1e-10 | 2642 |
| preferred_phase_deg | 2642 | 2642 | 0 | 5.12e-13 | 1e-10 | 2642 |
| status | 2642 | 2642 | 0 | 0 | 0 | 2642 |

## Fixed computation and failures

Nine methods are reported separately. F1/F2 retain Step-2 fP even when end-to-end APC fails. A_APC failures count against recovery; A_SCAN proceeds whenever a source fP exists. Coupling is normalized MVL with the common APC phase-band rule, using the selected APC or SOS-scan amplitude band. The full two-dimensional scan reuses its original selected pair, with common coupling recomputed. Selection scores and diagnostic curves are in the per-input checkpoints.

HA APC amplitude range is 80–150 Hz; HB is 80–160 Hz; ECoG is 80–150 Hz. ECoG F1 uses phase limits 6–30 Hz; F2/F3 use 1–30 Hz. A_SCAN uses phase half-width 1.5 Hz; amplitude half-width 30 Hz for HA/ECoG and 14 Hz for HB, with the original amplitude grids. `execution_plan.json` records the a priori implementation conventions.

Recovery denominators include failures. Error means/medians use finite estimates and report their counts. AUC uses finite scores without imputation; paired bootstrap resamples matched input identifiers, with shared resamples across methods and method-specific finite denominators. Bootstrap generator: NumPy MT19937, 10,000 resamples, seed 20261102 for AUC and 20261024 for ECoG.

### Consistency with end-to-end APC

| dataset | pipeline | reference | n | recovered_fp_hz_identical | recovered_fa_hz_identical | coupling_identical | all_identical |
|---|---|---|---|---|---|---|---|
| HA | F1_A_APC | APC-v1.0 | 900 | 900 | 900 | 900 | 900 |
| HA | F2_A_APC | APC-v3.0 | 900 | 900 | 900 | 900 | 900 |
| HB | F1_A_APC | APC-v1.0 | 675 | 675 | 675 | 675 | 675 |
| HB | F2_A_APC | APC-v3.0 | 675 | 675 | 675 | 675 | 675 |
| ECoG | F1_A_APC | APC-v1.0 | 2642 | 2642 | 2642 | 2642 | 2642 |
| ECoG | F2_A_APC | APC-v3.0 | 2642 | 2642 | 2642 | 2642 | 2642 |

### Retained Step-2 estimates after later failures

| suite | dataset | recording | source | n | step2_fp | step2_fp_later_apc_failed | endtoend_reference_exists |
|---|---|---|---|---|---|---|---|
| HA | coupled | NA | F1 | 450 | 450 | 341 | True |
| HA | coupled | NA | F2 | 450 | 447 | 0 | True |
| HA | coupled | NA | F3 | 450 | 446 | 0 | False |
| HA | timing_null | NA | F1 | 450 | 449 | 359 | True |
| HA | timing_null | NA | F2 | 450 | 449 | 0 | True |
| HA | timing_null | NA | F3 | 450 | 446 | 0 | False |
| HB | coupled | NA | F1 | 350 | 350 | 7 | True |
| HB | coupled | NA | F2 | 350 | 350 | 0 | True |
| HB | coupled | NA | F3 | 350 | 350 | 0 | False |
| HB | timing_null | NA | F1 | 250 | 250 | 2 | True |
| HB | timing_null | NA | F2 | 250 | 250 | 0 | True |
| HB | timing_null | NA | F3 | 250 | 250 | 0 | False |
| HB | no_coupled_burst | NA | F1 | 75 | 75 | 1 | True |
| HB | no_coupled_burst | NA | F2 | 75 | 75 | 0 | True |
| HB | no_coupled_burst | NA | F3 | 75 | 75 | 0 | False |
| ECoG | move | movement | F1 | 1057 | 1057 | 0 | True |
| ECoG | move | movement | F2 | 1057 | 1042 | 1 | True |
| ECoG | move | movement | F3 | 1057 | 1056 | 0 | False |
| ECoG | rest | movement | F1 | 752 | 752 | 0 | True |
| ECoG | rest | movement | F2 | 752 | 745 | 0 | True |
| ECoG | rest | movement | F3 | 752 | 752 | 0 | False |
| ECoG | move | imagery | F1 | 420 | 420 | 0 | True |
| ECoG | move | imagery | F2 | 420 | 417 | 0 | True |
| ECoG | move | imagery | F3 | 420 | 419 | 0 | False |
| ECoG | rest | imagery | F1 | 413 | 413 | 0 | True |
| ECoG | rest | imagery | F2 | 413 | 409 | 0 | True |
| ECoG | rest | imagery | F3 | 413 | 411 | 0 | False |

## E1: primary joint-recovery contrasts

Exact two-sided McNemar tests; Holm correction across the three sources within each dataset. “Most” means at least two sources. The committed A_SCAN condition is applied when at least one source significantly favors A_SCAN, if the A_APC-most condition is not met. All source-specific directions are shown.

| dataset | source | n | joint_apc | joint_scan | only_first | only_second | p_value | p_holm | better | significant |
|---|---|---|---|---|---|---|---|---|---|---|
| HA | F1 | 450 | 43 | 63 | 22 | 42 | 0.016858 | 0.016858 | A_SCAN | True |
| HA | F2 | 450 | 101 | 301 | 33 | 233 | 2.99e-38 | 5.98e-38 | A_SCAN | True |
| HA | F3 | 450 | 129 | 350 | 41 | 262 | 1.4e-40 | 4.19e-40 | A_SCAN | True |
| H1 | F1 | 175 | 120 | 154 | 5 | 39 | 1.41e-07 | 2.81e-07 | A_SCAN | True |
| H1 | F2 | 175 | 124 | 160 | 5 | 41 | 4.41e-08 | 1.32e-07 | A_SCAN | True |
| H1 | F3 | 175 | 126 | 160 | 5 | 39 | 1.41e-07 | 2.81e-07 | A_SCAN | True |

| dataset | decision | significant_apc_sources | significant_scan_sources |
|---|---|---|---|
| HA | it does not | 0 | 3 |
| H1 | it does not | 0 | 3 |

## Recovery by pipeline

| dataset | method | n | joint | strict_joint | fp_only | fa_only | valid | mean_abs_fp_error | median_abs_fp_error | mean_abs_fa_error | median_abs_fa_error |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HA | F1_A_APC | 450 | 43 | 43 | 97 | 45 | 109 | 1.583 | 0.035895 | 14.892 | 11.447 |
| HA | F1_A_SCAN | 450 | 63 | 63 | 97 | 70 | 450 | 11.605 | 12.183 | 33.284 | 35.266 |
| HA | F2_A_APC | 450 | 101 | 96 | 368 | 111 | 447 | 1.8887 | 0.079943 | 18.693 | 15.927 |
| HA | F2_A_SCAN | 450 | 301 | 282 | 368 | 317 | 447 | 1.8887 | 0.079943 | 9.1094 | 2.7502 |
| HA | F3_A_APC | 450 | 129 | 129 | 440 | 129 | 446 | 0.19699 | 0.010114 | 17.336 | 14.767 |
| HA | F3_A_SCAN | 450 | 350 | 350 | 440 | 353 | 446 | 0.19699 | 0.010114 | 4.7846 | 2.2876 |
| HA | A2_prime_2D | 450 | 234 | 94 | 302 | 294 | 450 | 2.9776 | 0.78009 | 9.0474 | 3.2816 |
| HA | APC-v1.0 | 450 | 43 | 43 | 97 | 45 | 109 | 1.583 | 0.035895 | 14.892 | 11.447 |
| HA | APC-v3.0 | 450 | 101 | 96 | 368 | 111 | 447 | 1.8887 | 0.079943 | 18.693 | 15.927 |
| H1 | F1_A_APC | 175 | 120 | 120 | 169 | 120 | 170 | 0.085634 | 0.028456 | 10.667 | 4.6548 |
| H1 | F1_A_SCAN | 175 | 154 | 154 | 169 | 154 | 175 | 0.30691 | 0.029256 | 4.1183 | 1.4625 |
| H1 | F2_A_APC | 175 | 124 | 124 | 175 | 124 | 175 | 0.043882 | 0.029256 | 10.719 | 4.6504 |
| H1 | F2_A_SCAN | 175 | 160 | 160 | 175 | 160 | 175 | 0.043882 | 0.029256 | 3.2559 | 1.2803 |
| H1 | F3_A_APC | 175 | 126 | 126 | 175 | 126 | 175 | 0.0070063 | 0.0058146 | 10.487 | 4.4782 |
| H1 | F3_A_SCAN | 175 | 160 | 160 | 175 | 160 | 175 | 0.0070063 | 0.0058146 | 3.4299 | 1.2802 |
| H1 | A2_prime_2D | 175 | 96 | 45 | 97 | 132 | 175 | 2.0722 | 0.91785 | 7.4837 | 1.8803 |
| H1 | APC-v1.0 | 175 | 120 | 120 | 169 | 120 | 170 | 0.085634 | 0.028456 | 10.667 | 4.6548 |
| H1 | APC-v3.0 | 175 | 124 | 124 | 175 | 124 | 175 | 0.043882 | 0.029256 | 10.719 | 4.6504 |
| H2 | F1_A_APC | 150 | 63 | 61 | 64 | 82 | 148 | 2.9454 | 3.13 | 14.418 | 5.8118 |
| H2 | F1_A_SCAN | 150 | 64 | 62 | 64 | 80 | 150 | 2.9534 | 3.2952 | 13.997 | 5.214 |
| H2 | F2_A_APC | 150 | 60 | 58 | 61 | 80 | 150 | 3.1809 | 3.5299 | 14.82 | 6.3592 |
| H2 | F2_A_SCAN | 150 | 61 | 59 | 61 | 77 | 150 | 3.1809 | 3.5299 | 14.208 | 6.2577 |
| H2 | F3_A_APC | 150 | 49 | 49 | 50 | 70 | 150 | 3.5389 | 3.9169 | 16.835 | 10.759 |
| H2 | F3_A_SCAN | 150 | 50 | 50 | 50 | 60 | 150 | 3.5389 | 3.9169 | 17.015 | 12.944 |
| H2 | A2_prime_2D | 150 | 73 | 24 | 78 | 109 | 150 | 1.2803 | 0.98341 | 9.3752 | 3.0699 |
| H2 | APC-v1.0 | 150 | 63 | 61 | 64 | 82 | 148 | 2.9454 | 3.13 | 14.418 | 5.8118 |
| H2 | APC-v3.0 | 150 | 60 | 58 | 61 | 80 | 150 | 3.1809 | 3.5299 | 14.82 | 6.3592 |
| H4 | F1_A_APC | 25 | 22 | 22 | 25 | 22 | 25 | 0.045686 | 0.041332 | 3.2702 | 1.9405 |
| H4 | F1_A_SCAN | 25 | 25 | 25 | 25 | 25 | 25 | 0.045686 | 0.041332 | 1.0836 | 1.036 |
| H4 | F2_A_APC | 25 | 22 | 22 | 25 | 22 | 25 | 0.045686 | 0.041332 | 3.2702 | 1.9405 |
| H4 | F2_A_SCAN | 25 | 25 | 25 | 25 | 25 | 25 | 0.045686 | 0.041332 | 1.0836 | 1.036 |
| H4 | F3_A_APC | 25 | 22 | 22 | 25 | 22 | 25 | 0.0057204 | 0.005637 | 3.2728 | 1.9405 |
| H4 | F3_A_SCAN | 25 | 25 | 25 | 25 | 25 | 25 | 0.0057204 | 0.005637 | 1.0836 | 1.036 |
| H4 | A2_prime_2D | 25 | 23 | 6 | 23 | 25 | 25 | 0.69553 | 0.69334 | 1.1416 | 1.036 |
| H4 | APC-v1.0 | 25 | 22 | 22 | 25 | 22 | 25 | 0.045686 | 0.041332 | 3.2702 | 1.9405 |
| H4 | APC-v3.0 | 25 | 22 | 22 | 25 | 22 | 25 | 0.045686 | 0.041332 | 3.2702 | 1.9405 |

All cell/level results, error denominators and failures are in `recovery_by_level.csv`. Joint recovery uses |fP error| ≤ 1 Hz and |fA error| ≤ 8 Hz; strict joint uses |fP error| ≤ 0.5 Hz.

## E2: phase-frequency sources

| dataset | source | n | finite | fp_recovery | strict_fp_recovery | mean_abs_error | median_abs_error |
|---|---|---|---|---|---|---|---|
| HA | F1 | 450 | 450 | 97 | 97 | 11.605 | 12.183 |
| HA | F2 | 450 | 447 | 368 | 343 | 1.8887 | 0.079943 |
| HA | F3 | 450 | 446 | 440 | 440 | 0.19699 | 0.010114 |
| H1 | F1 | 175 | 175 | 169 | 169 | 0.30691 | 0.029256 |
| H1 | F2 | 175 | 175 | 175 | 175 | 0.043882 | 0.029256 |
| H1 | F3 | 175 | 175 | 175 | 175 | 0.0070063 | 0.0058146 |
| H2 | F1 | 150 | 150 | 64 | 62 | 2.9534 | 3.2952 |
| H2 | F2 | 150 | 150 | 61 | 59 | 3.1809 | 3.5299 |
| H2 | F3 | 150 | 150 | 50 | 50 | 3.5389 | 3.9169 |
| H4 | F1 | 25 | 25 | 25 | 25 | 0.045686 | 0.041332 |
| H4 | F2 | 25 | 25 | 25 | 25 | 0.045686 | 0.041332 |
| H4 | F3 | 25 | 25 | 25 | 25 | 0.0057204 | 0.005637 |

| dataset | first | second | tolerance_hz | only_first | only_second | p_value | descriptive_only |
|---|---|---|---|---|---|---|---|
| HA | F2 | F3 | 1 | 4 | 76 | 2.76e-18 | False |
| HA | F2 | F3 | 0.5 | 3 | 100 | 3.59e-26 | False |
| HA | F1 | F3 | 1 | 0 | 343 | 1.12e-103 | False |
| HA | F1 | F3 | 0.5 | 0 | 343 | 1.12e-103 | False |
| H1 | F2 | F3 | 1 | 0 | 0 | 1 | False |
| H1 | F2 | F3 | 0.5 | 0 | 0 | 1 | False |
| H1 | F1 | F3 | 1 | 0 | 6 | 0.03125 | False |
| H1 | F1 | F3 | 0.5 | 0 | 6 | 0.03125 | False |
| H2 | F2 | F3 | 1 | 11 | 0 | 0.00097656 | True |
| H2 | F2 | F3 | 0.5 | 9 | 0 | 0.0039062 | True |
| H2 | F1 | F3 | 1 | 14 | 0 | 0.00012207 | True |
| H2 | F1 | F3 | 0.5 | 12 | 0 | 0.00048828 | True |
| H4 | F2 | F3 | 1 | 0 | 0 | 1 | True |
| H4 | F2 | F3 | 0.5 | 0 | 0 | 1 | True |
| H4 | F1 | F3 | 1 | 0 | 0 | 1 | True |
| H4 | F1 | F3 | 0.5 | 0 | 0 | 1 | True |

## E3: specificity

### False joint recovery in timing nulls

| suite | method | n | joint | strict_joint | fp_only | fa_only | valid |
|---|---|---|---|---|---|---|---|
| HA | F1_A_APC | 450 | 9 | 9 | 77 | 9 | 90 |
| HA | F1_A_SCAN | 450 | 30 | 30 | 77 | 33 | 449 |
| HA | F2_A_APC | 450 | 35 | 33 | 346 | 47 | 449 |
| HA | F2_A_SCAN | 450 | 142 | 137 | 346 | 164 | 449 |
| HA | F3_A_APC | 450 | 45 | 45 | 440 | 45 | 446 |
| HA | F3_A_SCAN | 450 | 172 | 172 | 440 | 173 | 446 |
| HA | A2_prime_2D | 450 | 3 | 0 | 6 | 36 | 450 |
| HA | APC-v1.0 | 450 | 9 | 9 | 77 | 9 | 90 |
| HA | APC-v3.0 | 450 | 35 | 33 | 346 | 47 | 449 |
| HB | F1_A_APC | 250 | 36 | 36 | 212 | 44 | 248 |
| HB | F1_A_SCAN | 250 | 44 | 44 | 212 | 49 | 250 |
| HB | F2_A_APC | 250 | 37 | 37 | 206 | 46 | 250 |
| HB | F2_A_SCAN | 250 | 45 | 45 | 206 | 53 | 250 |
| HB | F3_A_APC | 250 | 38 | 38 | 200 | 45 | 250 |
| HB | F3_A_SCAN | 250 | 44 | 44 | 200 | 56 | 250 |
| HB | A2_prime_2D | 250 | 2 | 0 | 10 | 49 | 250 |
| HB | APC-v1.0 | 250 | 36 | 36 | 212 | 44 | 248 |
| HB | APC-v3.0 | 250 | 37 | 37 | 206 | 46 | 250 |

The HB timing-null denominator includes all 250 timing nulls (H1 and H2); paired AUC below uses H1 and its 175 matched H3 nulls. The 75 no-coupled-burst controls are listed separately by scenario and level in `recovery_by_level.csv`.

### Coupled-vs-timing-null AUC, pair-bootstrap 95% CI

| dataset | method | pairs | finite_coupled | finite_null | complete_pairs | auc | ci_low | ci_high |
|---|---|---|---|---|---|---|---|---|
| HA | F1_A_APC | 450 | 109 | 90 | 55 | 0.94944 | 0.91502 | 0.97709 |
| HA | F1_A_SCAN | 450 | 450 | 449 | 449 | 0.60376 | 0.57528 | 0.63213 |
| HA | F2_A_APC | 450 | 447 | 449 | 446 | 0.89824 | 0.87545 | 0.91979 |
| HA | F2_A_SCAN | 450 | 447 | 449 | 446 | 0.9069 | 0.88464 | 0.92836 |
| HA | F3_A_APC | 450 | 446 | 446 | 446 | 0.94815 | 0.93386 | 0.96113 |
| HA | F3_A_SCAN | 450 | 446 | 446 | 446 | 0.97655 | 0.96708 | 0.98473 |
| HA | A2_prime_2D | 450 | 450 | 450 | 450 | 0.8611 | 0.83731 | 0.88396 |
| HA | APC-v1.0 | 450 | 109 | 90 | 55 | 0.94944 | 0.91502 | 0.97709 |
| HA | APC-v3.0 | 450 | 447 | 449 | 446 | 0.89824 | 0.87545 | 0.91979 |
| H1 | F1_A_APC | 175 | 170 | 173 | 169 | 0.81744 | 0.77936 | 0.8552 |
| H1 | F1_A_SCAN | 175 | 175 | 175 | 175 | 0.92065 | 0.89241 | 0.9472 |
| H1 | F2_A_APC | 175 | 175 | 175 | 175 | 0.81946 | 0.7822 | 0.85678 |
| H1 | F2_A_SCAN | 175 | 175 | 175 | 175 | 0.92591 | 0.89907 | 0.9506 |
| H1 | F3_A_APC | 175 | 175 | 175 | 175 | 0.81995 | 0.78279 | 0.85724 |
| H1 | F3_A_SCAN | 175 | 175 | 175 | 175 | 0.925 | 0.8978 | 0.95011 |
| H1 | A2_prime_2D | 175 | 175 | 175 | 175 | 0.83549 | 0.79262 | 0.87742 |
| H1 | APC-v1.0 | 175 | 170 | 173 | 169 | 0.81744 | 0.77936 | 0.8552 |
| H1 | APC-v3.0 | 175 | 175 | 175 | 175 | 0.81946 | 0.7822 | 0.85678 |

### AUC differences: A_APC minus A_SCAN

| dataset | source | auc_apc | auc_scan | auc_difference | ci_low | ci_high |
|---|---|---|---|---|---|---|
| HA | F1 | 0.94944 | 0.60376 | 0.34568 | 0.30638 | 0.38361 |
| HA | F2 | 0.89824 | 0.9069 | -0.0086645 | -0.025117 | 0.0073811 |
| HA | F3 | 0.94815 | 0.97655 | -0.028399 | -0.039819 | -0.017557 |
| H1 | F1 | 0.81744 | 0.92065 | -0.10321 | -0.13696 | -0.069382 |
| H1 | F2 | 0.81946 | 0.92591 | -0.10645 | -0.13881 | -0.074937 |
| H1 | F3 | 0.81995 | 0.925 | -0.10504 | -0.13672 | -0.073469 |

## E4: ECoG, descriptive

Movement data are available for all 18 eligible patients; imagery data are available for 7. Imagery bootstrap summaries use those 7 available patients. The agreement-count table retains the prespecified denominator of 18 and separately reports available-patient counts; Figure 3 labels the observed n explicitly.

Rest agreement compares each patient’s median valid rest fP with the unchanged original rest spectral peak, within 2 Hz; denominator 18. State contrasts are patient means of movement minus rest normalized coupling, with patient-bootstrap percentile 95% CIs. Within-state spread is the median patient-level sample SD. Missing estimates and available-patient counts are explicit in the CSVs.

| recording | method | patients | patients_finite_rest | rest_agreement_count | rest_agreement_denominator | mean_move_minus_rest | ci_low | ci_high | patients_finite_difference | median_rest_fp_sd | median_move_fp_sd |
|---|---|---|---|---|---|---|---|---|---|---|---|
| movement | F1_A_APC | 18 | 18 | 5 | 18 | 0.0024595 | -0.0019042 | 0.0067154 | 18 | 3.5918 | 3.358 |
| movement | F1_A_SCAN | 18 | 18 | 5 | 18 | 0.0057243 | 0.0014435 | 0.0099645 | 18 | 3.5918 | 3.358 |
| movement | F2_A_APC | 18 | 18 | 13 | 18 | -0.0023318 | -0.0073147 | 0.0028223 | 18 | 5.839 | 6.4893 |
| movement | F2_A_SCAN | 18 | 18 | 13 | 18 | 0.0012599 | -0.0032777 | 0.0060455 | 18 | 5.839 | 6.551 |
| movement | F3_A_APC | 18 | 18 | 15 | 18 | -0.0016024 | -0.006061 | 0.0033943 | 18 | 5.4548 | 6.051 |
| movement | F3_A_SCAN | 18 | 18 | 15 | 18 | 0.00047751 | -0.0042149 | 0.0055257 | 18 | 5.4548 | 6.051 |
| movement | A2_prime_2D | 18 | 18 | 2 | 18 | 0.0016657 | -0.0022051 | 0.005656 | 18 | 3.9604 | 4.2073 |
| movement | APC-v1.0 | 18 | 18 | 5 | 18 | 0.0024595 | -0.0019042 | 0.0067154 | 18 | 3.5918 | 3.358 |
| movement | APC-v3.0 | 18 | 18 | 13 | 18 | -0.0023318 | -0.0073147 | 0.0028223 | 18 | 5.839 | 6.4893 |
| imagery | F1_A_APC | 7 | 7 | 2 | 18 | 0.0011867 | -0.0040066 | 0.005906 | 7 | 3.2173 | 3.2445 |
| imagery | F1_A_SCAN | 7 | 7 | 2 | 18 | 0.0016054 | -0.0021999 | 0.0055932 | 7 | 3.2173 | 3.2445 |
| imagery | F2_A_APC | 7 | 7 | 6 | 18 | 0.00037672 | -0.00095774 | 0.0016602 | 7 | 6.0165 | 6.3174 |
| imagery | F2_A_SCAN | 7 | 7 | 6 | 18 | 0.00011013 | -0.0018305 | 0.0018958 | 7 | 6.0165 | 6.3174 |
| imagery | F3_A_APC | 7 | 7 | 7 | 18 | -0.0018034 | -0.0081193 | 0.0045311 | 7 | 4.9517 | 5.7616 |
| imagery | F3_A_SCAN | 7 | 7 | 7 | 18 | 0.0022025 | -0.00099368 | 0.0049382 | 7 | 4.9517 | 5.7616 |
| imagery | A2_prime_2D | 7 | 7 | 1 | 18 | 0.0031107 | -0.0025641 | 0.0081456 | 7 | 4.6603 | 4.4485 |
| imagery | APC-v1.0 | 7 | 7 | 2 | 18 | 0.0011867 | -0.0040066 | 0.005906 | 7 | 3.2173 | 3.2445 |
| imagery | APC-v3.0 | 7 | 7 | 6 | 18 | 0.00037672 | -0.00095774 | 0.0016602 | 7 | 6.0165 | 6.3174 |

Patient-level results are in `E4_ecog_patient_summary.csv`; all status/boundary counts are in `ecog_status_boundaries.csv`. Per-bout estimates are in `ecog_bout_estimates.csv`.

## Figures

- `figure1_recovery.png` (300 dpi) and `figure1_recovery.svg`; commit and source-CSV hashes embedded in metadata.

- `figure2_auc.png` (300 dpi) and `figure2_auc.svg`; commit and source-CSV hashes embedded in metadata.

- `figure3_ecog_rest_agreement.png` (300 dpi) and `figure3_ecog_rest_agreement.svg`; commit and source-CSV hashes embedded in metadata.


The figures contain no internal titles or footers. `figure_provenance.json` records source paths and hashes.

## Runtime and deviations

Gates: 98.649 s. HB reproduction: 38.634 s. Worker runtimes: W1 1392.046 s, W2 1392.305 s, W3 1179.559 s, W4 975.193 s. Statistics: 19.054 s. Rendering/report time is recorded in `report_runtime.json`. Concurrent worker times are not summed as wall time.

Wall time from initial provenance to report creation: 8384.949 s, including pauses, tooling fixes and startup (excluding the earlier archive step). Preserved pre-resume worker times are below; concurrent worker times are not summed.

| attempt | worker_file | elapsed_seconds | identifier |
|---|---|---|---|
| tooling_ecog_row_label | worker1_error.json | 2151.5 | MATLAB:assertion:failed |
| tooling_ecog_row_label | worker2_error.json | 2144.6 | MATLAB:assertion:failed |
| tooling_ecog_row_label | worker3_error.json | 2159.3 | MATLAB:assertion:failed |
| tooling_ecog_row_label | worker4_error.json | 2135.5 | MATLAB:assertion:failed |
| tooling_metadata_dependency | worker1_error.json | 8.1081 | MATLAB:UndefinedFunction |
| tooling_metadata_dependency | worker2_error.json | 8.2025 | MATLAB:UndefinedFunction |
| tooling_metadata_dependency | worker3_error.json | 7.9944 | MATLAB:UndefinedFunction |
| tooling_metadata_dependency | worker4_error.json | 8.494 | MATLAB:UndefinedFunction |

1. Initial provenance guard detected concurrent protocol Amendment 1 before outputs were written. User subsequently authorized Amendments 1 and 2; both pushed before gates. No method output was computed under the old hash.

2. A PowerShell inspection combined incompatible Get-Content Raw and TotalCount parameters. Reissued inspection with TotalCount only; no scientific output affected.

3. Initial runtime provenance resolved root-folder bst_apc and metric copies because MATLAB current-folder precedence overrides addpath. No signal analysis was performed. Preserved environment_attempt0_wrong_cwd.json; cd to output folder and assert repository source paths before estimators.

4. Initial canonical CSV auto-detection did not expose signal column. Failed before any estimator. Preserved gate_import_error_attempt0.json and gates_import_attempt0.log; use explicit comma delimiter, header row, names and UTF-8 as in the previous v3 gate.

5. Read-only process inspection in the restricted shell could not access CIM; used escalated Get-Process to inspect the already-authorized MATLAB startup.

6. A PowerShell inline Python preparation command had a quoting parse error before execution. Replaced it with finish_static_helpers.py; no estimator ran and no scientific output changed.

7. All workers stopped on their first input before any completed trial checkpoint/CSV because metadata-only paper2_options omitted the original parse_flag dependency. Added that helper verbatim from tagged source, preserved worker errors/logs in tooling_metadata_dependency, and resumed. Estimator source and settings unchanged.

8. Several read-only file inspections referenced an absent historical script name or used the repository folder for output-log paths. Corrected the inspection paths; no signals or results were changed.

9. After all 1575 simulation checkpoints were complete, ECoG import stopped before its first estimate because the saved APC method is labeled APC-v1.0, not APC. Corrected only that row-lookup label, preserved all four errors/logs and simulation CSV hashes in tooling_ecog_row_label, then resumed from existing simulation checkpoints.

10. Whole-CSV rewriting made checkpoint restoration slow and would also repeat prior rows after every ECoG bout. Paused only the four paper2 workers during checkpoint-only restoration (no ECoG estimates existed), preserved logs/partial CSVs and a code diff in tooling_append_logging, and changed logging to a single startup rebuild plus per-input appends. Estimator calls/settings are unchanged; completed simulation CSV bytes are checked against the pre-resume hashes.

11. Shared-stop handling overwrote STOPPED.md with a cascade message. Preserved that file as STOPPED_worker_cascade.md and wrote the root ReferenceMVL condition from the existing worker error logs; no estimator was rerun.

12. User-authorized one-time section-5 fix, identified from code without inspecting any outcome: ECoG v1 csvref reconstructed an amplitude band not saved in the CSV. Recompute original v1 end-to-end once per identical bout (fA 80-150, phase 6-30), cache exact returned info.final_band_hz, and require saved fP/raw/phase agreement within 1e-10 and exact fA/status. Keep the raw-MVL reconstruction tolerance unchanged. Archive the two partial ECoG bouts unchanged in stopped_attempt1, keep STOPPED_attempt1.md, and add pre-raise observed/expected values, source k and bout key to wrapper assertion JSON. HA/HB and ECoG v3 references are unchanged.


No signal, method setting, grid, tolerance or seed was changed. No results were committed.
