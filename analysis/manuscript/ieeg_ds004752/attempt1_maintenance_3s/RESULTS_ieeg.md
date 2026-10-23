# ds004752 human iEEG analysis: STOPPED under the method-failure rule

**No completed primary endpoint decision is available.** The frozen run stopped because most completed inputs returned APC status 4. The report below distinguishes completed preprocessing/selection from partial method outputs. [STOPPED.md](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/STOPPED.md>).

## Prespecified method-failure stop

At the first check, 325/422 unique completed trial-signal inputs were invalid for APC (77.0%). Final in-flight counts: 326/425 status 4 (76.7%), 99 status 0. A unique input is one clinical trial with one signal representation (bipolar or referential); shared primary/artifact-only estimates are counted once here.

The stopped run contains 3165 method rows, 425 input checkpoints, 2 patients and 6 sessions. Only 3 sessions completed their planned unique inputs; 3 more were partial. Planned full-run counts were 4898 unique inputs and 34530 method rows. The rates below describe only the completed portion and are not whole-dataset estimates.

Partial failure table (all comparisons are incomplete):
| analysis | method | n_patients | n_sessions | completed_trials | valid_trials | status4_trials | other_failures | failure_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| artifact_only | APC-v1.0 | 2 | 6 | 219 | 54 | 165 | 0 | 0.75342466 |
| artifact_only | GLM | 2 | 6 | 219 | 219 | 0 | 0 | 0 |
| artifact_only | KLMI | 2 | 6 | 219 | 219 | 0 | 0 | 0 |
| artifact_only | MVL-Ozkurt | 2 | 6 | 219 | 219 | 0 | 0 | 0 |
| artifact_only | MVL-raw | 2 | 6 | 219 | 219 | 0 | 0 | 0 |
| primary | APC-v1.0 | 2 | 6 | 208 | 54 | 154 | 0 | 0.74038462 |
| primary | GLM | 2 | 6 | 208 | 208 | 0 | 0 | 0 |
| primary | KLMI | 2 | 6 | 208 | 208 | 0 | 0 | 0 |
| primary | MVL-Ozkurt | 2 | 6 | 208 | 208 | 0 | 0 | 0 |
| primary | MVL-raw | 2 | 6 | 208 | 208 | 0 | 0 | 0 |
| referential | APC-v1.0 | 2 | 6 | 206 | 45 | 161 | 0 | 0.7815534 |
| referential | GLM | 2 | 6 | 206 | 206 | 0 | 0 | 0 |
| referential | KLMI | 2 | 6 | 206 | 206 | 0 | 0 | 0 |
| referential | MVL-Ozkurt | 2 | 6 | 206 | 206 | 0 | 0 | 0 |
| referential | MVL-raw | 2 | 6 | 206 | 206 | 0 | 0 | 0 |

Status 4 is returned for empty trough detections or empty phase-locked average/TF output. Both conditions are in the unchanged [APC source, empty troughs](<C:/Users/nghare/.brainstorm/process/apc-brainstorm-publish/src/bst_apc.m:214>) and [APC source, empty phase-locked arrays](<C:/Users/nghare/.brainstorm/process/apc-brainstorm-publish/src/bst_apc.m:224>). The status does not identify which branch each trial took. No extra method run or diagnostic adjustment was made.

All workers stopped on the shared flag. Completed results remain in [ieeg_trial_estimates.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/ieeg_trial_estimates.csv>) and the `estimates/` checkpoints. Per-session completion counts: [partial_session_progress.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/partial_session_progress.csv>). No nulls, primary/secondary endpoint tests, sensitivity endpoint tests, exploratory load models or endpoint figure were run. No method setting changed in response to outcomes.

## Public protocol and provenance

HEAD `37c21dbe249881fdc021655a855c000434b3ac54` on clean branch `neuroimage-submission`. Protocol SHA-256 `087c51b1e5b930dca55e3c1ce63af15c891252399a3da1abc68407b27a2df308`. Amendments 1, 2 and 3 were each pushed before the dependent signal processing. The source/helper hashes were verified before freezing the method run. No protocol, src, tagged source or original helper was edited; no results were committed.

Immutable pre-outcome method/input record: [analysis_provenance.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/analysis_provenance.json>). Current provenance and versions: [provenance.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/provenance.json>). Frozen contacts, masks, settings and wrapper hashes are recorded there. The first attempt remains in [RESULTS_ieeg.md](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/attempt1_archive/RESULTS_ieeg.md>) and [STOPPED_attempt1_sampling_rate.md](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/STOPPED_attempt1_sampling_rate.md>).

## Gate results

Both source-equivalence gates passed with maximum absolute difference 3.694822225952521e-13 (tolerance 1e-10). The repository src copy was used. Both original run records are retained:
| attempt | metric | expected | observed | absolute_difference | passed |
| --- | --- | --- | --- | --- | --- |
| 1 | fP_hz | 7.9979231 | 7.9979231 | 3.5527137e-15 | True |
| 1 | fA_hz | 122 | 122 | 0 | True |
| 1 | raw_mvl | 0.17690778 | 0.17690778 | 1.3877788e-16 | True |
| 1 | preferred_phase_deg | 178.5758 | 178.5758 | 3.6948222e-13 | True |
| 2 | fP_hz | 7.9979231 | 7.9979231 | 3.5527137e-15 | True |
| 2 | fA_hz | 122 | 122 | 0 | True |
| 2 | raw_mvl | 0.17690778 | 0.17690778 | 1.3877788e-16 | True |
| 2 | preferred_phase_deg | 178.5758 | 178.5758 | 3.6948222e-13 | True |

All 68 iEEG files passed amended header/channel/JSON rate agreement, native rate restrictions, channel order/count, total samples, 8-s trial lengths, finite data, nonzero channel variance and microvolt range. All 3353 iEEG trials produced exactly 16000 samples at 2000 Hz. Native iEEG rates:
| native_fs_hz | n_patients | n_sessions |
| --- | --- | --- |
| 2000 | 10 | 38 |
| 4000 | 3 | 20 |
| 4096 | 2 | 10 |

All 68 scalp files passed the timing-input checks. All 3353 scalp trials produced exactly 1600 samples at 200 Hz under Amendment 2. Native scalp rates:
| native_fs_hz | n_patients | n_sessions | trials |
| --- | --- | --- | --- |
| 200 | 9 | 36 | 1778 |
| 2000 | 1 | 2 | 77 |
| 4000 | 3 | 20 | 998 |
| 4096 | 2 | 10 | 500 |

Gate files: [edf_reading_gate_attempt2.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/edf_reading_gate_attempt2.json>), [edf_file_checks_attempt2.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/edf_file_checks_attempt2.csv>), [edf_channel_checks_attempt2.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/edf_channel_checks_attempt2.csv>), [resampling_trial_checks_attempt2.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/resampling_trial_checks_attempt2.csv>), [timeline_file_checks.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/timeline_file_checks.csv>), [timeline_resampling_trial_checks.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/timeline_resampling_trial_checks.csv>).

## Trial timeline: PASS

The grand average includes all 3353 trials from 15 patients/68 sessions, averaging available O1/O2/Oz per trial. Each trial was resampled separately to 200 Hz, its fixation mean was subtracted, and no additional signal filter was applied. Visual review confirmed evoked negative deflections after both expected onsets. Peak latencies are at 5-ms resolution:
| expected_onset_s | peak_time_s | latency_ms | peak_uv | absolute_peak_difference_uv |
| --- | --- | --- | --- | --- |
| 1 | 1.16 | 160 | -10.35484 | 9.2148774 |
| 6 | 6.2 | 200 | -3.2501841 | 3.4792439 |

The 160-ms encoding and 200-ms probe peaks are within the required 50-250 ms interval. Paper timings support fixation 0-1 s, encoding 1-3 s, maintenance 3-6 s and probe from 6 s: [Boran et al., Figure 1a](https://www.nature.com/articles/s41597-020-0364-3.pdf); [Dimakopoulos et al., task methods](https://elifesciences.org/articles/78677).

Timeline plot: [300-dpi PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/timeline_grand_average.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/timeline_grand_average.svg>). Source [timeline_grand_average.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/timeline_grand_average.csv>); confirmation [timeline_gate_confirmation.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/timeline_gate_confirmation.json>).

## Earlier screening NaN cause

The earlier screening configured n_surrogates=0, so local_analyze_epoch never assigned the preinitialized NaN apc_z/pac_z fields; the saved screening coupling strengths and selected frequencies are finite.

All 64 earlier screening coupling strengths and frequency selections were finite; all 64 APC/scanned surrogate z fields were NaN. That screening is not a result of this prespecified run.

## Contacts fixed before any PAC output

The Amendment-3 order was followed: dataset flags, independent candidate/session robust masks, own-retained-trial power ratios, highest ratio with lower-k tie rule, then selected mask and eligibility. Welch used a symmetric 2000-sample Hann window, 1000-sample overlap, 2000-point FFT and 2000-Hz rate; retained trials were pooled with equal trial weights across sessions. Powers are trapezoidal integrals over inclusive 4-8 and 1-4 Hz bins.

The fixed contact table has 15 patients. Sub-13 has no Hipp-labelled candidate. Sub-11 has zero sessions with >=20 retained trials and therefore fails the >=2-session patient rule. The primary and referential plans have 13 patients, 52 sessions and 2008 included trials; the artifact-only plan has 14 patients, 62 sessions and 2890 trials. These are planned full analysis counts, not completed outcome denominators.

| patient | deeper_contact | adjacent_contact | deeper_labels | adjacent_labels | candidate_pairs | theta_delta_ratio | retained_trials | eligible_sessions | patient_eligible | native_fs_hz |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sub-01 | mPHL1 | mPHL2 | Hipp, Left Hippocampus cHipp, caudal hippocampus | no_label_found | 4 | 0.51215089 | 168 | 4 | 1 | 2000 |
| sub-02 | mPHL1 | mPHL2 | Hipp, Left Hippocampus cHipp, caudal hippocampus | no_label_found | 3 | 0.35467331 | 308 | 7 | 1 | 2000 |
| sub-03 | mPHL2 | mPHL3 | Hipp, Left Hippocampus cHipp, caudal hippocampus | FuG, Left Fusiform Gyrus A20rv, rostroventral area 20 | 8 | 0.61356877 | 130 | 3 | 1 | 2000 |
| sub-04 | mAHL2 | mAHL3 | Hipp, Left Hippocampus cHipp, caudal hippocampus | FuG, Left Fusiform Gyrus A20rv, rostroventral area 20 | 7 | 0.66280428 | 92 | 2 | 1 | 2000 |
| sub-05 | mAL1 | mAL2 | Hipp, Left Hippocampus rHipp, rostral hippocampus | Hipp, Left Hippocampus rHipp, rostral hippocampus | 6 | 0.32468045 | 103 | 3 | 1 | 2000 |
| sub-06 | mPHR2 | mPHR3 | Hipp, Right Hippocampus cHipp, caudal hippocampus | no_label_found | 13 | 1.1158675 | 325 | 7 | 1 | 2000 |
| sub-07 | mAHR2 | mAHR3 | Hipp, Right Hippocampus cHipp, caudal hippocampus | FuG, Right Fusiform Gyrus A20rv, rostroventral area 20 | 13 | 0.58355651 | 126 | 4 | 1 | 2000 |
| sub-08 | mAR1 | mAR2 | Hipp, Right Hippocampus rHipp, rostral hippocampus | Amyg, Right Amygdala lAmyg, lateral amygdala | 6 | 0.51697328 | 154 | 4 | 1 | 2000 |
| sub-09 | mAL2 | mAL3 | Hipp, Left Hippocampus rHipp, rostral hippocampus | Amyg, Left Amygdala lAmyg, lateral amygdala | 13 | 0.68077811 | 87 | 2 | 1 | 2000 |
| sub-10 | _GL_H1 | _GL_H2 | Hipp, Left Hippocampus cHipp, caudal hippocampus | no_label_found | 5 | 0.79093976 | 77 | 2 | 1 | 2000 |
| sub-11 | mPHL1 | mPHL2 | Hipp, Right Hippocampus cHipp, caudal hippocampus | no_label_found | 1 | 0.18461148 | 51 | 0 | 0 | 4000 |
| sub-12 | mAHL1 | mAHL2 | Hipp, Left Hippocampus cHipp, caudal hippocampus | Hipp, Left Hippocampus cHipp, caudal hippocampus | 4 | 0.26545972 | 149 | 5 | 1 | 4000 |
| sub-13 | NA | NA | NA | NA | 0 | NA | 0 | 0 | 0 | 4096 |
| sub-14 | mAHL2 | mAHL3 | Hipp, Left Hippocampus rHipp, rostral hippocampus | FuG, Left Fusiform Gyrus A20rv, rostroventral area 20 | 11 | 0.40363454 | 165 | 5 | 1 | 4000 |
| sub-15 | AHR3 | AHR4 | Hipp, Right Hippocampus cHipp, caudal hippocampus | no_label_found | 5 | 0.97835834 | 173 | 4 | 1 | 4096 |

Every candidate pooled retained-trial count and rank is reported here:
| patient | candidate_index | deeper_contact | adjacent_contact | retained_trials_total | theta_delta_ratio | selected |
| --- | --- | --- | --- | --- | --- | --- |
| sub-01 | 1 | mAHL1 | mAHL2 | 150 | 0.38190792 | 0 |
| sub-01 | 2 | mAHL2 | mAHL3 | 159 | 0.34431294 | 0 |
| sub-01 | 3 | mPHL1 | mPHL2 | 168 | 0.51215089 | 1 |
| sub-01 | 4 | mPHR1 | mPHR2 | 136 | 0.40119608 | 0 |
| sub-02 | 1 | mAHL1 | mAHL2 | 301 | 0.3290574 | 0 |
| sub-02 | 2 | mPHL1 | mPHL2 | 308 | 0.35467331 | 1 |
| sub-02 | 3 | mPHR1 | mPHR2 | 233 | 0.31756127 | 0 |
| sub-03 | 1 | mAHL1 | mAHL2 | 87 | 0.25450192 | 0 |
| sub-03 | 2 | mAHL2 | mAHL3 | 130 | 0.56455865 | 0 |
| sub-03 | 3 | mAHL3 | mAHL4 | 117 | 0.48288109 | 0 |
| sub-03 | 4 | mAHR1 | mAHR2 | 113 | 0.18552599 | 0 |
| sub-03 | 5 | mAHR2 | mAHR3 | 86 | 0.28685609 | 0 |
| sub-03 | 6 | mAHR3 | mAHR4 | 122 | 0.20211372 | 0 |
| sub-03 | 7 | mPHL1 | mPHL2 | 117 | 0.33838194 | 0 |
| sub-03 | 8 | mPHL2 | mPHL3 | 130 | 0.61356877 | 1 |
| sub-04 | 1 | mAHL1 | mAHL2 | 94 | 0.25878497 | 0 |
| sub-04 | 2 | mAHL2 | mAHL3 | 92 | 0.66280428 | 1 |
| sub-04 | 3 | mAHR1 | mAHR2 | 93 | 0.26674495 | 0 |
| sub-04 | 4 | mPHL1 | mPHL2 | 94 | 0.3379506 | 0 |
| sub-04 | 5 | mPHL2 | mPHL3 | 94 | 0.21833938 | 0 |
| sub-04 | 6 | mPHR1 | mPHR2 | 94 | 0.24916132 | 0 |
| sub-04 | 7 | mPHR2 | mPHR3 | 94 | 0.64576223 | 0 |
| sub-05 | 1 | mAHL1 | mAHL2 | 98 | 0.18213035 | 0 |
| sub-05 | 2 | mAHL2 | mAHL3 | 101 | 0.30148716 | 0 |
| sub-05 | 3 | mAL1 | mAL2 | 103 | 0.32468045 | 1 |
| sub-05 | 4 | mAL2 | mAL3 | 105 | 0.29983296 | 0 |
| sub-05 | 5 | mAL3 | mAL4 | 106 | 0.2881904 | 0 |
| sub-05 | 6 | mPHR1 | mPHR2 | 41 | 0.25458876 | 0 |
| sub-06 | 1 | mAHL1 | mAHL2 | 46 | 0.20483293 | 0 |
| sub-06 | 2 | mAHL2 | mAHL3 | 181 | 0.29827909 | 0 |
| sub-06 | 3 | mAHL3 | mAHL4 | 240 | 0.30924899 | 0 |
| sub-06 | 4 | mAHL4 | mAHL5 | 263 | 0.55768127 | 0 |
| sub-06 | 5 | mAHR1 | mAHR2 | 258 | 0.20956247 | 0 |
| sub-06 | 6 | mAR1 | mAR2 | 317 | 0.46947448 | 0 |
| sub-06 | 7 | mAR2 | mAR3 | 332 | 0.28396054 | 0 |
| sub-06 | 8 | mECL1 | mECL2 | 251 | 0.35973476 | 0 |
| sub-06 | 9 | mECL2 | mECL3 | 288 | 0.63902878 | 0 |
| sub-06 | 10 | mPHL1 | mPHL2 | 238 | 0.37667807 | 0 |
| sub-06 | 11 | mPHL2 | mPHL3 | 275 | 0.53674662 | 0 |
| sub-06 | 12 | mPHR1 | mPHR2 | 278 | 0.22775594 | 0 |
| sub-06 | 13 | mPHR2 | mPHR3 | 325 | 1.1158675 | 1 |
| sub-07 | 1 | mAHL1 | mAHL2 | 186 | 0.15716045 | 0 |
| sub-07 | 2 | mAHL2 | mAHL3 | 186 | 0.16578554 | 0 |
| sub-07 | 3 | mAHL3 | mAHL4 | 186 | 0.31291033 | 0 |
| sub-07 | 4 | mAHR1 | mAHR2 | 91 | 0.27444299 | 0 |
| sub-07 | 5 | mAHR2 | mAHR3 | 126 | 0.58355651 | 1 |
| sub-07 | 6 | mECL1 | mECL2 | 186 | 0.22398824 | 0 |
| sub-07 | 7 | mECL2 | mECL3 | 186 | 0.22401315 | 0 |
| sub-07 | 8 | mECL3 | mECL4 | 186 | 0.31337962 | 0 |
| sub-07 | 9 | mPHL1 | mPHL2 | 186 | 0.18898666 | 0 |
| sub-07 | 10 | mPHL2 | mPHL3 | 186 | 0.26388181 | 0 |
| sub-07 | 11 | mPHL3 | mPHL4 | 185 | 0.29989665 | 0 |
| sub-07 | 12 | mPHR1 | mPHR2 | 127 | 0.17956934 | 0 |
| sub-07 | 13 | mPHR2 | mPHR3 | 126 | 0.49404784 | 0 |
| sub-08 | 1 | mAHL3 | mAHL4 | 154 | 0.25964111 | 0 |
| sub-08 | 2 | mAHR1 | mAHR2 | 165 | 0.2819367 | 0 |
| sub-08 | 3 | mAR1 | mAR2 | 154 | 0.51697328 | 1 |
| sub-08 | 4 | mPHL1 | mPHL2 | 163 | 0.29053104 | 0 |
| sub-08 | 5 | mPHR1 | mPHR2 | 166 | 0.28531584 | 0 |
| sub-08 | 6 | mPHR2 | mPHR3 | 166 | 0.20782033 | 0 |
| sub-09 | 1 | mAHL1 | mAHL2 | 73 | 0.67292453 | 0 |
| sub-09 | 2 | mAHL2 | mAHL3 | 87 | 0.56411703 | 0 |
| sub-09 | 3 | mAHL3 | mAHL4 | 87 | 0.3826063 | 0 |
| sub-09 | 4 | mAHR1 | mAHR2 | 87 | 0.046049794 | 0 |
| sub-09 | 5 | mAHR2 | mAHR3 | 69 | 0.10619864 | 0 |
| sub-09 | 6 | mAL1 | mAL2 | 75 | 0.41409701 | 0 |
| sub-09 | 7 | mAL2 | mAL3 | 87 | 0.68077811 | 1 |
| sub-09 | 8 | mPHL1 | mPHL2 | 82 | 0.34841031 | 0 |
| sub-09 | 9 | mPHL2 | mPHL3 | 88 | 0.3731978 | 0 |
| sub-09 | 10 | mPHL3 | mPHL4 | 88 | 0.40068608 | 0 |
| sub-09 | 11 | mPHR1 | mPHR2 | 87 | 0.10677313 | 0 |
| sub-09 | 12 | mPHR2 | mPHR3 | 88 | 0.06339092 | 0 |
| sub-09 | 13 | mPHR3 | mPHR4 | 88 | 0.056115314 | 0 |
| sub-10 | 1 | _AHL1 | _AHL2 | 77 | 0.23547775 | 0 |
| sub-10 | 2 | _AHL2 | _AHL3 | 77 | 0.41721157 | 0 |
| sub-10 | 3 | _GL_H1 | _GL_H2 | 77 | 0.79093976 | 1 |
| sub-10 | 4 | _PHL1 | _PHL2 | 77 | 0.19590689 | 0 |
| sub-10 | 5 | _PHL2 | _PHL3 | 77 | 0.26327359 | 0 |
| sub-11 | 1 | mPHL1 | mPHL2 | 51 | 0.18461148 | 1 |
| sub-12 | 1 | mAHL1 | mAHL2 | 149 | 0.26545972 | 1 |
| sub-12 | 2 | mAHL2 | mAHL3 | 143 | 0.17353211 | 0 |
| sub-12 | 3 | mAHR1 | mAHR2 | 211 | 0.20462733 | 0 |
| sub-12 | 4 | mPHR1 | mPHR2 | 267 | 0.22652642 | 0 |
| sub-14 | 1 | mAHL1 | mAHL2 | 111 | 0.31278427 | 0 |
| sub-14 | 2 | mAHL2 | mAHL3 | 165 | 0.40363454 | 1 |
| sub-14 | 3 | mAHR1 | mAHR2 | 280 | 0.22551359 | 0 |
| sub-14 | 4 | mAL1 | mAL2 | 282 | 0.37080677 | 0 |
| sub-14 | 5 | mAL2 | mAL3 | 295 | 0.39952789 | 0 |
| sub-14 | 6 | mAL3 | mAL4 | 306 | 0.26291298 | 0 |
| sub-14 | 7 | mAR1 | mAR2 | 264 | 0.33775168 | 0 |
| sub-14 | 8 | mAR2 | mAR3 | 287 | 0.32835958 | 0 |
| sub-14 | 9 | mPCL1 | mPCL2 | 239 | 0.29991119 | 0 |
| sub-14 | 10 | mPCL2 | mPCL3 | 232 | 0.14848511 | 0 |
| sub-14 | 11 | mPCL3 | mPCL4 | 233 | 0.24471887 | 0 |
| sub-15 | 1 | AHL1 | AHL2 | 99 | 0.33257599 | 0 |
| sub-15 | 2 | AHR1 | AHR2 | 128 | 0.84533867 | 0 |
| sub-15 | 3 | AHR2 | AHR3 | 132 | 0.6647868 | 0 |
| sub-15 | 4 | AHR3 | AHR4 | 173 | 0.97835834 | 1 |
| sub-15 | 5 | PHR1 | PHR2 | 114 | 0.41927567 | 0 |

Every candidate/session rule count, threshold and retained-trial count: [candidate_trial_counts.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/candidate_trial_counts.csv>). Fixed outputs: [contacts.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/contacts.csv>), [trial_inclusion.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/trial_inclusion.csv>), [session_eligibility.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/session_eligibility.csv>), [patient_eligibility.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/patient_eligibility.csv>). These files were completed and hashed before the first PAC output.

## Trial exclusions and planned sensitivity sets

Counts below cover the selected pairs in all 62 candidate-bearing sessions. Robust amplitude and first-difference counts are on dataset-unflagged trials; overlaps and their union are separate, so overlapping rules are not added twice. Session/patient eligibility is applied after the mask.
| analysis | total_trials | dataset_artifact | amplitude_unflagged | difference_unflagged | both_robust_unflagged | robust_union_unflagged | retained_before_eligibility | retained_lost_session_eligibility | retained_lost_patient_eligibility | final_included |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| artifact_only | 3053 | 163 | 0 | 0 | 0 | 0 | 2890 | 0 | 0 | 2890 |
| primary | 3053 | 163 | 425 | 672 | 315 | 782 | 2108 | 100 | 0 | 2008 |
| referential | 3053 | 163 | 425 | 672 | 315 | 782 | 2108 | 100 | 0 | 2008 |

Sensitivity (a) retains the fixed selected pair and uses dataset flags only. Sensitivity (b) uses the deeper contact and the selected pair final mask. Sensitivity (c), the primary endpoint excluding non-2000-Hz patients, was not computed because the method-failure stop preceded every endpoint.

## Partial boundary-hit counts

These are completed-trial denominators only. APC bounds are fP within 0.05 Hz of 1/30 Hz and fA=80/150 Hz; scan bounds are fP=2/12 Hz and fA=80/148 Hz. Invalid APC results are retained in the all-trial denominator; valid-only phase-boundary counts are also shown.
| analysis | method | completed_trials | valid_trials | fp_low | fp_high | fa_low | fa_high | fp_boundary_fraction_all | fp_boundary_valid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| artifact_only | APC-v1.0 | 219 | 54 | 0 | 0 | 2 | 1 | 0 | 0 |
| artifact_only | GLM | 219 | 219 | 35 | 1 | 19 | 13 | 0.16438356 | 36 |
| artifact_only | KLMI | 219 | 219 | 129 | 0 | 17 | 13 | 0.5890411 | 129 |
| artifact_only | MVL-Ozkurt | 219 | 219 | 79 | 0 | 24 | 15 | 0.36073059 | 79 |
| artifact_only | MVL-raw | 219 | 219 | 73 | 0 | 132 | 0 | 0.33333333 | 73 |
| primary | APC-v1.0 | 208 | 54 | 0 | 0 | 2 | 1 | 0 | 0 |
| primary | GLM | 208 | 208 | 30 | 1 | 19 | 12 | 0.14903846 | 31 |
| primary | KLMI | 208 | 208 | 122 | 0 | 17 | 12 | 0.58653846 | 122 |
| primary | MVL-Ozkurt | 208 | 208 | 72 | 0 | 21 | 15 | 0.34615385 | 72 |
| primary | MVL-raw | 208 | 208 | 66 | 0 | 125 | 0 | 0.31730769 | 66 |
| referential | APC-v1.0 | 206 | 45 | 0 | 0 | 0 | 1 | 0 | 0 |
| referential | GLM | 206 | 206 | 33 | 0 | 21 | 15 | 0.16019417 | 33 |
| referential | KLMI | 206 | 206 | 126 | 0 | 20 | 17 | 0.61165049 | 126 |
| referential | MVL-Ozkurt | 206 | 206 | 57 | 0 | 19 | 24 | 0.27669903 | 57 |
| referential | MVL-raw | 206 | 206 | 56 | 3 | 127 | 0 | 0.28640777 | 59 |

## Endpoints not computed

The primary reproducibility test, all six secondary endpoints, the exploratory load model, sensitivity endpoint tests (a)-(c), trial-shuffle nulls and the four-panel endpoint figure were not computed. The incomplete run cannot support one of the prespecified primary decision forms. No empty or placeholder endpoint CSVs are supplied. The partial trial CSV is explicitly identified as partial in this report and STATUS.json.

The unchanged-source comparator copy and its reversible byte-diff verification are retained: [ieeg_comparators.diff](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/ieeg_comparators.diff>) and [ieeg_comparator_copy_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/ieeg_comparator_copy_verification.json>). Comparator band guards: [filter_guards.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/filter_guards.csv>) (post-stop deterministic logging recovery, described below). Fourth-order notch pole guards: [notch_filter_guards.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/notch_filter_guards.csv>).

## Runtime and deviations

Common preprocessing: 200.183 s. Candidate masking/ranking and fixed tables: 130.262 s. Partial method workers ran in parallel for 229.527, 229.801, 230.295 s; these stop at the shared stop flag and exclude startup/import before their timer. Three session partitions used one MATLAB computational thread each. No completed methods were rerun.

- resolved tooling path lookup: An initial read guessed a sidecar without the run-01 entity. File discovery established the actual BIDS names; no signal, setting or outcome was changed.
- resolved EDF unit metadata reader defect: All 48 EDF physical-dimension fields in the first file are blank; the BIDS channels.tsv declares microvolts. The first reader incorrectly required an EDF unit label as well as numeric range checks. The corrected reader accepts the BIDS declaration when the EDF field is blank and still rejects conflicting nonblank units. No signal scaling, thresholds, methods or protocol text changed.
- pre-existing MATLAB startup path warnings: MATLAB startup lists nonexistent historical Brainstorm directories. Explicit source-path assertions passed. No startup or installation changes were made.
- resolved EDF wall-clock header syntax: MATLAB rejects seconds=60. Two local analysis-folder copies carry the minute (10.28.60 to 10.29.00; 14.23.60 to 14.24.00). Only header bytes 176:184 changed; all bytes from offset 256 onward are SHA-256 identical. Originals remain untouched. Analysis uses events.tsv sample indices, not EDF wall-clock times.
- resolved JSON provenance serialization: MATLAB jsondecode sanitizes object keys containing full paths. Full path/hash records are additionally stored as an array; values and source files are unchanged.
- resolved timeline peak structure packaging: After all 68 scalp inputs had been read and the complete grand-average CSV saved, appending fields to MATLAB struct([]) failed. The code now collects cells before concatenating. The same fixed peak rule was evaluated from the saved grand-average CSV in Python, without rereading or resampling any raw trial. The defect was identified before viewing the trace or PAC outcomes.
- resolved pre-analysis CSV boolean reader: MATLAB serialized logical inclusion columns as 0/1; pandas interpreted them as integers. The freeze verifier now explicitly converts those columns to bool. This failed before any analysis freeze or dataset PAC output. No selection table, setting or method changed.
- post-stop filter-guard logging recovery: The worker registry export was after its normal completion path, so the shared stop prevented export. The 39 fixed comparator-band design checks are reconstructed after the stop using the unchanged final_sos_filter helper on zero input only. No dataset trial or PAC method is rerun; the CSV explicitly labels this recovery.
- stop snapshot scope label correction: The initial monitor JSON hardcoded a three-session scope, although its contemporaneous displayed counts covered six sessions from two patients. The scope label is corrected without changing failure counts, and the original JSON is preserved.
- The method-failure stop is the prespecified rule being followed, not a change to the method. No 3-s window, contact, mask, option, grid, filter, threshold or seed was adjusted after looking at method outputs.

Verification and file hashes: [method_stop_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/method_stop_verification.json>); [output_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/output_manifest.json>).
