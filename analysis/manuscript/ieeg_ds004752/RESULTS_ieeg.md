# ds004752 iEEG: Amendment 4 stopped under protocol 6.4

**Most completed inputs were again invalid for frozen APC v1.0.** There are 287/372 invalid inputs (77.2%) in the partial Amendment-4 run. No completed primary decision is available. [STOPPED.md](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/STOPPED.md>).

## Public protocol and provenance

Amendment 4 was pushed before any new-window analysis. HEAD `f87ce24a8a7c5719023549d783db13da584d1423`; protocol SHA-256 `95b741822ac085bb96a01f1a5396674b83ecfaa827c199708e95490ad9f70ad3`. The repository is on clean branch `neuroimage-submission`, with HEAD equal to origin. The protocol, src and tagged code were not edited. No results were committed. Full options, MATLAB/toolbox versions, seed and source hashes: [provenance.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/provenance.json>). Immutable pre-outcome freeze: [analysis_provenance.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/analysis_provenance.json>).

## Attempt 1 (3-s maintenance window)

The 3-s [3,6) maintenance run stopped under section 6.4. At the first check, 325/422 unique trial-signal inputs returned status 4. Final in-flight counts were 326/425 status 4 (76.7%) and 99/425 status 0; the primary subset had 154/208 status 4. The partial run covered 2 patients and 6 sessions; 3 sessions completed their planned inputs and 3 were partial. All four scans returned valid scores on these completed inputs. No endpoint tests or nulls were computed. The reason for Amendment 4 is recorded in the committed protocol.

| analysis | method | completed_trials | valid_trials | status4_trials | failure_fraction |
| --- | --- | --- | --- | --- | --- |
| artifact_only | APC-v1.0 | 219 | 54 | 165 | 0.75342466 |
| artifact_only | GLM | 219 | 219 | 0 | 0 |
| artifact_only | KLMI | 219 | 219 | 0 | 0 |
| artifact_only | MVL-Ozkurt | 219 | 219 | 0 | 0 |
| artifact_only | MVL-raw | 219 | 219 | 0 | 0 |
| primary | APC-v1.0 | 208 | 54 | 154 | 0.74038462 |
| primary | GLM | 208 | 208 | 0 | 0 |
| primary | KLMI | 208 | 208 | 0 | 0 |
| primary | MVL-Ozkurt | 208 | 208 | 0 | 0 |
| primary | MVL-raw | 208 | 208 | 0 | 0 |
| referential | APC-v1.0 | 206 | 45 | 161 | 0.7815534 |
| referential | GLM | 206 | 206 | 0 | 0 |
| referential | KLMI | 206 | 206 | 0 | 0 |
| referential | MVL-Ozkurt | 206 | 206 | 0 | 0 |
| referential | MVL-raw | 206 | 206 | 0 | 0 |

All 455 archived files, including 425 unchanged checkpoint MATs, passed SHA-256 preservation checks. Original report: [RESULTS_ieeg.md](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/attempt1_maintenance_3s/RESULTS_ieeg.md>); original stop: [STOPPED.md](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/attempt1_maintenance_3s/STOPPED.md>); manifest: [am4_archive_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/am4_archive_manifest.json>). The contacts, candidate masks, original trial_inclusion.csv and reading/timeline gates stayed in place and retain their original hashes.

## Reused gates

Both repository-source equivalence checks passed (maximum absolute difference 3.694822225952521e-13; tolerance 1e-10). They used the src copy, not frozen_v1:
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

All 68 iEEG files/3353 trials passed the amended reading and trialwise-resampling checks: EDF/JSON/channels.tsv rate agreement; allowed native rates; channel order/count; event sample count; 8-s trials; no NaN; nonzero channel variance; microvolt range. Every trial has 16000 samples after resampling to 2000 Hz. The native-rate table is:
| native_fs_hz | n_patients | n_sessions |
| --- | --- | --- |
| 2000 | 10 | 38 |
| 4000 | 3 | 20 |
| 4096 | 2 | 10 |

Reading records: [edf_reading_gate_attempt2.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/edf_reading_gate_attempt2.json>), [edf_file_checks_attempt2.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/edf_file_checks_attempt2.csv>), [edf_channel_checks_attempt2.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/edf_channel_checks_attempt2.csv>), [resampling_trial_checks_attempt2.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/resampling_trial_checks_attempt2.csv>).

The scalp timeline check used all 3353 trials, available O1/O2/Oz, and per-trial 200-Hz resampling (1600 samples), with fixation-baseline subtraction and no added signal filter. The expected 1-s encoding and 6-s probe responses were confirmed:
| expected_onset_s | peak_time_s | latency_ms | peak_uv | absolute_peak_difference_uv |
| --- | --- | --- | --- | --- |
| 1 | 1.16 | 160 | -10.35484 | 9.2148774 |
| 6 | 6.2 | 200 | -3.2501841 | 3.4792439 |

Latencies are at 5-ms resolution. Timeline [300-dpi PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/timeline_grand_average.png>) / [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/timeline_grand_average.svg>); source [timeline_grand_average.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/timeline_grand_average.csv>); gate [timeline_gate_confirmation.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/timeline_gate_confirmation.json>). Paper evidence retained in [timeline_paper_evidence.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/timeline_paper_evidence.json>): [Boran et al.](https://www.nature.com/articles/s41597-020-0364-3.pdf), [Dimakopoulos et al.](https://elifesciences.org/articles/78677).

Earlier screening NaN cause: The earlier screening configured n_surrogates=0, so local_analyze_epoch never assigned the preinitialized NaN apc_z/pac_z fields; the saved screening coupling strengths and selected frequencies are finite.

## Amendment 4 inputs and fixed choices

Each native 8-s trial was separately resampled to 2000 Hz, demeaned over the full 8 s, and filtered with the same fourth-order digital SOS notches at 50/100/150 Hz (+/-1 Hz). Samples 1:12000 form [0,6) s. The unchanged Amendment-3 selected-pair mask is intersected with the selected signal’s new 0-6-s amplitude and first-difference masks. Robust scales use the selected signal in all dataset-unflagged trials, per session, before evoked subtraction. Session >=20 and patient >=2-session eligibility was reapplied.

Separate included-trial mean waveforms were subtracted for every analysis/patient/session/signal. Sensitivity (a) keeps dataset artifact flags only at both stages and has its own bipolar mean; sensitivity (b) intersects the Amendment-3 selected-pair mask with the deeper-contact 0-6-s mask and uses its own referential mean. There is no post-subtraction rejection. These details were recorded before method outputs: [am4_fixed_preprocessing_choices.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/am4_fixed_preprocessing_choices.json>). Template residual checks: [am4_evoked_template_audit.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/am4_evoked_template_audit.csv>).

APC uses unchanged default v1 with fA=[80,150]. Scans use phase 1:0.5:12 (half-width 1.5, lower edge clipped at 0.5) and amplitude 80:4:148 (half-width 12), all four original metrics. Reversing the permitted wrapper edits reproduces the original comparator bytes exactly: [am4_comparator_copy_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/am4_comparator_copy_verification.json>) and [am4_comparator_copy.diff](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/am4_comparator_copy.diff>).

All 41 comparator-band guards were exported during actual trial processing and passed. [filter_guards.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/filter_guards.csv>). The three unchanged notch designs passed their four-pole/radius checks: [am4_notch_filter_guards.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/am4_notch_filter_guards.csv>).

Post-evoked Welch spectra used hann(2000), 50% overlap, nfft=2000 and equal trial weights. Spectral peaks were prepared from residuals above the log-log linear fit on 1-12 Hz, as amended: [am4_session_spectral_peaks.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/am4_session_spectral_peaks.csv>). The downstream dominant-rhythm endpoint was not tested. The shared [3,6) samples of the new pre-evoked inputs match the preserved old inputs exactly in both signal representations across all 62 sessions: [am4_shared_preprocessing_verification.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/am4_shared_preprocessing_verification.csv>).

## Fixed contacts and eligibility

Contacts and their original selection ratios are unchanged. The eligible_sessions field in the old contacts.csv belongs to Amendment 3; new eligibility appears separately below. Sub-13 has no Hipp-labelled candidate.
| patient | deeper_contact | adjacent_contact | deeper_labels | adjacent_labels | candidate_pairs | theta_delta_ratio | native_fs_hz |
| --- | --- | --- | --- | --- | --- | --- | --- |
| sub-01 | mPHL1 | mPHL2 | Hipp, Left Hippocampus cHipp, caudal hippocampus | no_label_found | 4 | 0.51215089 | 2000 |
| sub-02 | mPHL1 | mPHL2 | Hipp, Left Hippocampus cHipp, caudal hippocampus | no_label_found | 3 | 0.35467331 | 2000 |
| sub-03 | mPHL2 | mPHL3 | Hipp, Left Hippocampus cHipp, caudal hippocampus | FuG, Left Fusiform Gyrus A20rv, rostroventral area 20 | 8 | 0.61356877 | 2000 |
| sub-04 | mAHL2 | mAHL3 | Hipp, Left Hippocampus cHipp, caudal hippocampus | FuG, Left Fusiform Gyrus A20rv, rostroventral area 20 | 7 | 0.66280428 | 2000 |
| sub-05 | mAL1 | mAL2 | Hipp, Left Hippocampus rHipp, rostral hippocampus | Hipp, Left Hippocampus rHipp, rostral hippocampus | 6 | 0.32468045 | 2000 |
| sub-06 | mPHR2 | mPHR3 | Hipp, Right Hippocampus cHipp, caudal hippocampus | no_label_found | 13 | 1.1158675 | 2000 |
| sub-07 | mAHR2 | mAHR3 | Hipp, Right Hippocampus cHipp, caudal hippocampus | FuG, Right Fusiform Gyrus A20rv, rostroventral area 20 | 13 | 0.58355651 | 2000 |
| sub-08 | mAR1 | mAR2 | Hipp, Right Hippocampus rHipp, rostral hippocampus | Amyg, Right Amygdala lAmyg, lateral amygdala | 6 | 0.51697328 | 2000 |
| sub-09 | mAL2 | mAL3 | Hipp, Left Hippocampus rHipp, rostral hippocampus | Amyg, Left Amygdala lAmyg, lateral amygdala | 13 | 0.68077811 | 2000 |
| sub-10 | _GL_H1 | _GL_H2 | Hipp, Left Hippocampus cHipp, caudal hippocampus | no_label_found | 5 | 0.79093976 | 2000 |
| sub-11 | mPHL1 | mPHL2 | Hipp, Right Hippocampus cHipp, caudal hippocampus | no_label_found | 1 | 0.18461148 | 4000 |
| sub-12 | mAHL1 | mAHL2 | Hipp, Left Hippocampus cHipp, caudal hippocampus | Hipp, Left Hippocampus cHipp, caudal hippocampus | 4 | 0.26545972 | 4000 |
| sub-13 | NA | NA | NA | NA | 0 | NA | 4096 |
| sub-14 | mAHL2 | mAHL3 | Hipp, Left Hippocampus rHipp, rostral hippocampus | FuG, Left Fusiform Gyrus A20rv, rostroventral area 20 | 11 | 0.40363454 | 4000 |
| sub-15 | AHR3 | AHR4 | Hipp, Right Hippocampus cHipp, caudal hippocampus | no_label_found | 5 | 0.97835834 | 4096 |

All original candidate retained-trial counts and ranks: [candidate_rankings.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/candidate_rankings.csv>); every candidate/session rule count and threshold: [candidate_trial_counts.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/candidate_trial_counts.csv>). Original selected masks: [trial_inclusion.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/trial_inclusion.csv>).

New patient eligibility, separately by analysis:
| analysis | patient | eligible_sessions | patient_eligible | native_fs_hz |
| --- | --- | --- | --- | --- |
| artifact_only | sub-01 | 4 | 1 | 2000 |
| artifact_only | sub-02 | 7 | 1 | 2000 |
| artifact_only | sub-03 | 3 | 1 | 2000 |
| artifact_only | sub-04 | 2 | 1 | 2000 |
| artifact_only | sub-05 | 3 | 1 | 2000 |
| artifact_only | sub-06 | 7 | 1 | 2000 |
| artifact_only | sub-07 | 4 | 1 | 2000 |
| artifact_only | sub-08 | 4 | 1 | 2000 |
| artifact_only | sub-09 | 2 | 1 | 2000 |
| artifact_only | sub-10 | 2 | 1 | 2000 |
| artifact_only | sub-11 | 6 | 1 | 4000 |
| artifact_only | sub-12 | 6 | 1 | 4000 |
| artifact_only | sub-14 | 8 | 1 | 4000 |
| artifact_only | sub-15 | 4 | 1 | 4096 |
| primary | sub-01 | 4 | 1 | 2000 |
| primary | sub-02 | 7 | 1 | 2000 |
| primary | sub-03 | 3 | 1 | 2000 |
| primary | sub-04 | 2 | 1 | 2000 |
| primary | sub-05 | 3 | 1 | 2000 |
| primary | sub-06 | 7 | 1 | 2000 |
| primary | sub-07 | 2 | 1 | 2000 |
| primary | sub-08 | 4 | 1 | 2000 |
| primary | sub-09 | 2 | 1 | 2000 |
| primary | sub-10 | 2 | 1 | 2000 |
| primary | sub-11 | 0 | 0 | 4000 |
| primary | sub-12 | 2 | 1 | 4000 |
| primary | sub-14 | 0 | 0 | 4000 |
| primary | sub-15 | 4 | 1 | 4096 |
| referential | sub-01 | 2 | 1 | 2000 |
| referential | sub-02 | 7 | 1 | 2000 |
| referential | sub-03 | 3 | 1 | 2000 |
| referential | sub-04 | 1 | 0 | 2000 |
| referential | sub-05 | 3 | 1 | 2000 |
| referential | sub-06 | 6 | 1 | 2000 |
| referential | sub-07 | 1 | 0 | 2000 |
| referential | sub-08 | 4 | 1 | 2000 |
| referential | sub-09 | 2 | 1 | 2000 |
| referential | sub-10 | 1 | 0 | 2000 |
| referential | sub-11 | 0 | 0 | 4000 |
| referential | sub-12 | 0 | 0 | 4000 |
| referential | sub-14 | 0 | 0 | 4000 |
| referential | sub-15 | 2 | 1 | 4096 |

Planned full-run sets (not completed outcome denominators): {"artifact_only": {"patients": 14, "sessions": 62, "trials": 2890, "method_rows": 14450}, "primary": {"patients": 12, "sessions": 42, "trials": 1532, "method_rows": 7660}, "referential": {"patients": 8, "sessions": 29, "trials": 894, "method_rows": 4470}}. New per-session eligibility: [session_eligibility_amendment4.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/session_eligibility_amendment4.csv>); per-trial rule flags and thresholds: [trial_inclusion_amendment4.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/trial_inclusion_amendment4.csv>).

## Trial exclusions

Rule counts overlap. The added-reject column counts the union of new amplitude/first-difference failures among trials that had passed Amendment 3. Dataset-flags-only sensitivity has zero applied robust-rejection counts.
| analysis | total_trials | dataset_artifact | am3_amplitude_unflagged | am3_difference_unflagged | am3_robust_union_unflagged | am4_amplitude_unflagged | am4_difference_unflagged | am4_robust_union_unflagged | am4_additional_reject_after_am3 | retained_before_eligibility | lost_session_eligibility | lost_patient_eligibility | final_included |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| artifact_only | 3053 | 163 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2890 | 0 | 0 | 2890 |
| primary | 3053 | 163 | 425 | 672 | 782 | 629 | 1099 | 1245 | 465 | 1643 | 111 | 0 | 1532 |
| referential | 3053 | 163 | 425 | 672 | 782 | 871 | 1467 | 1613 | 893 | 1215 | 241 | 80 | 894 |

## Requested sub-01/ses-01 progress check

This session was completed first. Its status counts were logged, and the full run continued automatically with no changes. It was not treated as a gate:
| analysis | status | trials |
| --- | --- | --- |
| artifact_only | 0 | 12 |
| artifact_only | 4 | 36 |
| primary | 0 | 8 |
| primary | 4 | 35 |
| referential | 0 | 7 |
| referential | 4 | 28 |

Original log [am4_worker0_matlab.log](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/am4_worker0_matlab.log>); progress record [am4_sub01_ses01_progress_check.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/am4_sub01_ses01_progress_check.json>).

## Amendment 4 partial outcomes and stop

The first subsequent stop check was after 2 additional session partitions completed. It recorded the following per-analysis/method counts; no subsequent method adjustment was made:
| analysis | method | n_completed | invalid | fraction_invalid |
| --- | --- | --- | --- | --- |
| artifact_only | APC-v1.0 | 199 | 155 | 0.77889447 |
| artifact_only | GLM | 199 | 0 | 0 |
| artifact_only | KLMI | 199 | 0 | 0 |
| artifact_only | MVL-Ozkurt | 199 | 0 | 0 |
| artifact_only | MVL-raw | 199 | 0 | 0 |
| primary | APC-v1.0 | 135 | 101 | 0.74814815 |
| primary | GLM | 135 | 0 | 0 |
| primary | KLMI | 135 | 0 | 0 |
| primary | MVL-Ozkurt | 135 | 0 | 0 |
| primary | MVL-raw | 135 | 0 | 0 |
| referential | APC-v1.0 | 35 | 28 | 0.8 |
| referential | GLM | 35 | 0 | 0 |
| referential | KLMI | 35 | 0 | 0 |
| referential | MVL-Ozkurt | 35 | 0 | 0 |
| referential | MVL-raw | 35 | 0 | 0 |

After already-running inputs finished, 372 input checkpoints and 1860 method rows were preserved across 2 patients and 6 sessions. These incomplete-run denominators are used below; no rates represent the full dataset.
| analysis | method | n_patients | n_sessions | completed_trials | valid_trials | status4_trials | other_failures | failure_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| artifact_only | APC-v1.0 | 2 | 6 | 201 | 44 | 157 | 0 | 0.78109453 |
| artifact_only | GLM | 2 | 6 | 201 | 201 | 0 | 0 | 0 |
| artifact_only | KLMI | 2 | 6 | 201 | 201 | 0 | 0 | 0 |
| artifact_only | MVL-Ozkurt | 2 | 6 | 201 | 201 | 0 | 0 | 0 |
| artifact_only | MVL-raw | 2 | 6 | 201 | 201 | 0 | 0 | 0 |
| primary | APC-v1.0 | 1 | 4 | 136 | 34 | 102 | 0 | 0.75 |
| primary | GLM | 1 | 4 | 136 | 136 | 0 | 0 | 0 |
| primary | KLMI | 1 | 4 | 136 | 136 | 0 | 0 | 0 |
| primary | MVL-Ozkurt | 1 | 4 | 136 | 136 | 0 | 0 | 0 |
| primary | MVL-raw | 1 | 4 | 136 | 136 | 0 | 0 | 0 |
| referential | APC-v1.0 | 1 | 1 | 35 | 7 | 28 | 0 | 0.8 |
| referential | GLM | 1 | 1 | 35 | 35 | 0 | 0 | 0 |
| referential | KLMI | 1 | 1 | 35 | 35 | 0 | 0 | 0 |
| referential | MVL-Ozkurt | 1 | 1 | 35 | 35 | 0 | 0 | 0 |
| referential | MVL-raw | 1 | 1 | 35 | 35 | 0 | 0 | 0 |

Status 4 can return at [empty troughs](<C:/Users/nghare/.brainstorm/process/apc-brainstorm-publish/src/bst_apc.m:214>) or [empty phase-locked arrays](<C:/Users/nghare/.brainstorm/process/apc-brainstorm-publish/src/bst_apc.m:224>). The saved status does not distinguish those return branches. No diagnostic method rerun was performed. Incremental estimates: [ieeg_trial_estimates.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/ieeg_trial_estimates.csv>); checkpoints in `estimates/`; completion table [partial_session_progress.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/partial_session_progress.csv>); exact per-session/status counts [partial_status_counts.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/partial_status_counts.csv>).

## Partial boundary hits

Scan boundaries are fP=1/12 and fA=80/148 Hz; APC boundaries are fP within 0.05 Hz of 1/30 and fA=80/150 Hz. All-trial and valid-only denominators are shown separately:
| analysis | method | completed_trials | valid_trials | fp_low | fp_high | fa_low | fa_high | fp_boundary_all | fp_boundary_valid | fp_boundary_rate_valid | fa_boundary_valid | fa_boundary_rate_valid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| artifact_only | APC-v1.0 | 201 | 44 | 5 | 0 | 1 | 1 | 0.024875622 | 5 | 0.11363636 | 2 | 0.045454545 |
| artifact_only | GLM | 201 | 201 | 32 | 0 | 18 | 10 | 0.15920398 | 32 | 0.15920398 | 28 | 0.13930348 |
| artifact_only | KLMI | 201 | 201 | 94 | 0 | 19 | 2 | 0.46766169 | 94 | 0.46766169 | 21 | 0.10447761 |
| artifact_only | MVL-Ozkurt | 201 | 201 | 51 | 0 | 12 | 14 | 0.25373134 | 51 | 0.25373134 | 26 | 0.12935323 |
| artifact_only | MVL-raw | 201 | 201 | 55 | 0 | 114 | 0 | 0.27363184 | 55 | 0.27363184 | 114 | 0.56716418 |
| primary | APC-v1.0 | 136 | 34 | 3 | 0 | 0 | 0 | 0.022058824 | 3 | 0.088235294 | 0 | 0 |
| primary | GLM | 136 | 136 | 19 | 2 | 12 | 5 | 0.15441176 | 21 | 0.15441176 | 17 | 0.125 |
| primary | KLMI | 136 | 136 | 64 | 0 | 13 | 1 | 0.47058824 | 64 | 0.47058824 | 14 | 0.10294118 |
| primary | MVL-Ozkurt | 136 | 136 | 38 | 0 | 8 | 6 | 0.27941176 | 38 | 0.27941176 | 14 | 0.10294118 |
| primary | MVL-raw | 136 | 136 | 42 | 0 | 75 | 0 | 0.30882353 | 42 | 0.30882353 | 75 | 0.55147059 |
| referential | APC-v1.0 | 35 | 7 | 2 | 0 | 0 | 0 | 0.057142857 | 2 | 0.28571429 | 0 | 0 |
| referential | GLM | 35 | 35 | 5 | 0 | 2 | 2 | 0.14285714 | 5 | 0.14285714 | 4 | 0.11428571 |
| referential | KLMI | 35 | 35 | 20 | 0 | 4 | 3 | 0.57142857 | 20 | 0.57142857 | 7 | 0.2 |
| referential | MVL-Ozkurt | 35 | 35 | 15 | 0 | 6 | 4 | 0.42857143 | 15 | 0.42857143 | 10 | 0.28571429 |
| referential | MVL-raw | 35 | 35 | 4 | 0 | 21 | 0 | 0.11428571 | 4 | 0.11428571 | 21 | 0.6 |

## Endpoints not computed

The primary paired reproducibility endpoint, secondary tests 1-6, exploratory load models, sensitivity endpoint tests (a)-(c), trial-shuffle nulls and the four-panel endpoint figure were not run after the method-failure stop. No prespecified primary decision form is stated for an incomplete run. The prepared post-evoked spectra/peak locations are supplied, but their association with APC was not tested. The reusable timeline figure remains available.

## Runtime and deviations

Amendment-4 preparation: 106.591 s. Pipeline including MATLAB startup/progress/full-run workers: 464.813 s. Individual method-worker timers: worker0 283.987 s, worker1 115.938 s, worker2 115.842 s, worker3 116.299 s. No completed input was recomputed.

Amendments 1-4 are public protocol changes with their recorded reasons. Amendment 4 followed the failed 3-s attempt; it was frozen before the new-window method run. The stop under section 6.4 is compliance with the protocol. Tooling deviations inherited from the reading/selection run are listed below:

- resolved tooling path lookup: An initial read guessed a sidecar without the run-01 entity. File discovery established the actual BIDS names; no signal, setting or outcome was changed.
- resolved EDF unit metadata reader defect: All 48 EDF physical-dimension fields in the first file are blank; the BIDS channels.tsv declares microvolts. The first reader incorrectly required an EDF unit label as well as numeric range checks. The corrected reader accepts the BIDS declaration when the EDF field is blank and still rejects conflicting nonblank units. No signal scaling, thresholds, methods or protocol text changed.
- pre-existing MATLAB startup path warnings: MATLAB startup lists nonexistent historical Brainstorm directories. Explicit source-path assertions passed. No startup or installation changes were made.
- resolved EDF wall-clock header syntax: MATLAB rejects seconds=60. Two local analysis-folder copies carry the minute (10.28.60 to 10.29.00; 14.23.60 to 14.24.00). Only header bytes 176:184 changed; all bytes from offset 256 onward are SHA-256 identical. Originals remain untouched. Analysis uses events.tsv sample indices, not EDF wall-clock times.
- resolved JSON provenance serialization: MATLAB jsondecode sanitizes object keys containing full paths. Full path/hash records are additionally stored as an array; values and source files are unchanged.
- resolved timeline peak structure packaging: After all 68 scalp inputs had been read and the complete grand-average CSV saved, appending fields to MATLAB struct([]) failed. The code now collects cells before concatenating. The same fixed peak rule was evaluated from the saved grand-average CSV in Python, without rereading or resampling any raw trial. The defect was identified before viewing the trace or PAC outcomes.
- resolved pre-analysis CSV boolean reader: MATLAB serialized logical inclusion columns as 0/1; pandas interpreted them as integers. The freeze verifier now explicitly converts those columns to bool. This failed before any analysis freeze or dataset PAC output. No selection table, setting or method changed.
- post-stop filter-guard logging recovery: The worker registry export was after its normal completion path, so the shared stop prevented export. The 39 fixed comparator-band design checks are reconstructed after the stop using the unchanged final_sos_filter helper on zero input only. No dataset trial or PAC method is rerun; the CSV explicitly labels this recovery.
- stop snapshot scope label correction: The initial monitor JSON hardcoded a three-session scope, although its contemporaneous displayed counts covered six sessions from two patients. The scope label is corrected without changing failure counts, and the original JSON is preserved.
- Amendment-4 post-stop input-verification singleton dimension: The verification-only h5py reader assumed a three-dimensional saved candidate array. MATLAB omits the trailing singleton dimension for a single candidate. The reader now accepts that two-dimensional storage after asserting candidate index 1. No signal processing, estimator or endpoint was rerun.
- Amendment-4 post-stop checkpoint-verification MATLAB string decoding: SciPy loads saved MATLAB string scalars as opaque arrays, so direct pandas comparison failed. Verification now associates the five checkpoint feature entries by their fixed source-defined order (APC, MVL-raw, MVL-Ozkurt, KLMI, GLM), then compares every numeric feature to its named CSV row. No estimator or endpoint was rerun.

Two post-stop verification-only reader errors (singleton dimensions and opaque MATLAB string decoding) were fixed and logged above; no analysis was repeated. Earlier compatibility fixes and their logs are retained. Output packaging preserves every completed method result; source, contact masks, grids, windows, templates, thresholds and seeds were not tuned after outcomes. Every completed checkpoint’s numeric feature fields, options and grids were verified against the incremental CSV: [am4_checkpoint_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/am4_checkpoint_verification.json>).

Final preservation/source/checkpoint verification: [am4_stop_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/am4_stop_verification.json>). Output inventory: [output_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/output_manifest.json>).
