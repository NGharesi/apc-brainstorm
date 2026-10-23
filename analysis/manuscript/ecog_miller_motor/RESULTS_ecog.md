# Miller library motor ECoG: Amendment 1 results

Primary 1: **Not shown**. Primary 2: **Not shown**. These decisions use the prespecified patient-bootstrap confidence intervals. The endpoint table and boundary rates are given below.

## Provenance and frozen methods

Amendment 1 was pushed before resumed analysis. Clean `neuroimage-submission` HEAD `c642a20b3081e2e36dfa148cc3da0b0747fca11e`; protocol SHA-256 `064d6651ccca2ad84954bbdea9cb2587d51bf8d4575ec7889d2fe32d5bd2dba4`. HEAD equals origin. Protocol, src and tagged code remain untouched. Results are not committed. Attempt 1 was executed by Claude through a job runner on this computer. Current provenance: [provenance.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/provenance.json>); immutable method-run record: [analysis_provenance.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/analysis_provenance.json>).

The 19 prepared MAT files and all reused tables/helpers retain their pre-resume hashes. ecog_prepare was not rerun. The only changes to ecog_worker are the ECoG wrapper call and APC lower-bound flag (6 Hz). The new wrapper is an exact copy of v1_bout_features except its function name and options fA=[80,150], minPhaseHz=6, maxPhaseHz=30. The original raw-MVL and preferred-phase reconstruction asserts remain active. Diffs: [v1_bout_features_ecog.diff](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/v1_bout_features_ecog.diff>) / [ecog_worker_amendment1.diff](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/ecog_worker_amendment1.diff>); reversible byte verification: [amendment1_copy_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/amendment1_copy_verification.json>).

Scans retain phase 6:0.5:30 Hz (half-width 1.5), amplitude 80:4:148 Hz (half-width 30), the original metrics, tie rules and SOS guards. All other comparator profiles reverse to the original bytes. All 67 band designs passed: [comparator_filter_guards.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/comparator_filter_guards.csv>). The saved preparation used the unchanged butter(4,...,stop) SOS implementation at 60/120/180 +/-1 Hz; its pole guards are retained in [notch_filter_guards.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/notch_filter_guards.csv>).

## Inventory and state gate

The preserved inventory contains 26 recordings from 19 patients, all at 1000 Hz. State coding is documented in the local README: 0=rest, 11=tongue, 12=hand. Codes 13 in gf and 15 in zt were not analysed. Full recording rows:
| patient | recording | file | n_samples | n_channels | duration_s | fs_hz | codes_and_counts |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bp | movement | motor_basic\data\bp_mot_t_h.mat | 376400 | 47 | 376.4 | 1000 | 0:196400;11:90000;12:90000 |
| bp | imagery | imagery_basic\data\bp_im_t_h.mat | 376600 | 46 | 376.6 | 1000 | 0:196600;11:90000;12:90000 |
| ca | movement | motor_basic\data\ca_mot_t_h.mat | 390240 | 59 | 390.24 | 1000 | 0:210240;11:90000;12:90000 |
| cc | movement | motor_basic\data\cc_mot_t_h.mat | 195200 | 60 | 195.2 | 1000 | 0:105200;11:45000;12:45000 |
| de | movement | motor_basic\data\de_mot_t_h.mat | 390400 | 64 | 390.4 | 1000 | 0:210360;11:90040;12:90000 |
| fp | movement | motor_basic\data\fp_mot_t_h.mat | 390680 | 62 | 390.68 | 1000 | 0:210680;11:90000;12:90000 |
| fp | imagery | imagery_basic\data\fp_im_t_h.mat | 390320 | 64 | 390.32 | 1000 | 0:210320;11:90000;12:90000 |
| gc | movement | motor_basic\data\gc_mot_t_h.mat | 390560 | 64 | 390.56 | 1000 | 0:210560;11:90000;12:90000 |
| gf | movement | motor_basic\data\gf_mot_t_h.mat | 586000 | 63 | 586 | 1000 | 0:315880;11:90000;12:90080;13:90040 |
| hh | movement | motor_basic\data\hh_mot_t_h.mat | 376240 | 41 | 376.24 | 1000 | 0:196240;11:90000;12:90000 |
| hh | imagery | imagery_basic\data\hh_im_t_h.mat | 376840 | 48 | 376.84 | 1000 | 0:196840;11:90000;12:90000 |
| hl | movement | motor_basic\data\hl_mot_t_h.mat | 376240 | 64 | 376.24 | 1000 | 0:196240;11:90000;12:90000 |
| jc | movement | motor_basic\data\jc_mot_t_h.mat | 390720 | 48 | 390.72 | 1000 | 0:210720;11:90000;12:90000 |
| jc | imagery | imagery_basic\data\jc_im_t_h.mat | 390200 | 48 | 390.2 | 1000 | 0:210200;11:90000;12:90000 |
| jf | movement | motor_basic\data\jf_mot_t_h.mat | 419640 | 39 | 419.64 | 1000 | 0:287640;11:60000;12:72000 |
| jm | movement | motor_basic\data\jm_mot_t_h.mat | 390640 | 63 | 390.64 | 1000 | 0:210640;11:90000;12:90000 |
| jm | imagery | imagery_basic\data\jm_im_t_h.mat | 390160 | 64 | 390.16 | 1000 | 0:210160;11:90000;12:90000 |
| jp | movement | motor_basic\data\jp_mot_t_h.mat | 246000 | 58 | 246 | 1000 | 0:132000;11:54000;12:60000 |
| jt | movement | motor_basic\data\jt_mot_t_h.mat | 390240 | 62 | 390.24 | 1000 | 0:210240;11:90000;12:90000 |
| rh | movement | motor_basic\data\rh_mot_t_h.mat | 390720 | 63 | 390.72 | 1000 | 0:210720;11:90000;12:90000 |
| rh | imagery | imagery_basic\data\rh_im_t_h.mat | 390200 | 64 | 390.2 | 1000 | 0:210200;11:90000;12:90000 |
| rr | movement | motor_basic\data\rr_mot_t_h.mat | 390240 | 49 | 390.24 | 1000 | 0:210240;11:90000;12:90000 |
| rr | imagery | imagery_basic\data\rr_im_t_h.mat | 390920 | 64 | 390.92 | 1000 | 0:210920;11:90000;12:90000 |
| ug | movement | motor_basic\data\ug_mot_t_h.mat | 585760 | 25 | 585.76 | 1000 | 0:315760;11:135000;12:135000 |
| wc | movement | motor_basic\data\wc_mot_t_h.mat | 390240 | 64 | 390.24 | 1000 | 0:210240;11:90000;12:90000 |
| zt | movement | motor_basic\data\zt_mot_t_h.mat | 571720 | 48 | 571.72 | 1000 | 0:301720;11:90000;12:90000;15:90000 |

The variance-based bad-channel fallback was used because no library bad-channel list was provided. Per-recording channel exclusions: [bad_channels.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/bad_channels.csv>). Preserved bouts trim 0.5 s per edge, retain >=2 s, and exclude the first/last 2 s of recordings. Coordinates are the supplied Talairach location values.

## Ethics statement (verbatim)

> Ethics statement: All patients participated in a purely voluntary manner, after providing informed written consent, under experimental protocols approved by the Institutional Review Board of the University of Washington (#12193). All patient data was anonymized according to IRB protocol, in accordance with HIPAA mandate. It was made available through the library described in “A Library of Human Electrocorticographic Data and Analyses” by Kai Miller [Reference], freely available at https://searchworks.stanford.edu/view/zk881ps0522. All patient data was anonymized according to IRB protocol, in accordance with HIPAA mandate. These data originally appeared in the manuscript “Spectral Changes in Cortical Surface Potentials during Motor Movement” published in Journal of Neuroscience in 2007 [Reference].

Source: [README_motor_basic_dataset_notes.docx](<D:/APC_project/RealDatasets/Miller_ECoG_library/motor_basic/README_motor_basic_dataset_notes.docx>); extracted text [README_motor_basic_dataset_notes_extracted.txt](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/README_motor_basic_dataset_notes_extracted.txt>).

## Equivalence and progress checks

The original repository-source equivalence gate passed: maximum absolute difference 3.694822225952521e-13, tolerance 1e-10, status 0. [equivalence_gate.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/equivalence_gate.json>). The amended wrapper also returned status 0 on the canonical input and passed its unchanged raw-MVL and preferred-phase asserts.

The first ten analysed bp movement-recording bouts returned status 0 in all ten, with fP values (Hz): 6.011962891, 14.1891372, 6.011962891, 13.26694511, 6.011962891, 14.97073306, 6.011962891, 6.011962891, 7.435680843, 18.03880477. The progress check was not a gate, and the full run continued unchanged. Its ten complete keys seeded worker 1’s resume CSV; none was estimated twice. [progress_check.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/progress_check.json>) / [progress_matlab.log](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/logs/progress_matlab.log>).

## Attempt 1 (APC phase range 1-30 Hz)

The original run stopped at the first combined rule-9.4 check: 127/200 bouts were invalid. Final in-flight results contained 225 complete bouts, 149 status 4 and 76 status 0. No endpoint was computed. The preserved status table is:
| recording | state | bouts | valid | status4 | other_invalid |
| --- | --- | --- | --- | --- | --- |
| movement | move | 143 | 36 | 107 | 0 |
| movement | rest | 82 | 40 | 42 | 0 |

All 15 moved files, including STOPPED.md, STOP_METHOD, worker estimates/status files/logs and the old runner sentinel, are unchanged by SHA-256. [attempt1_archive_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/attempt1_archive_manifest.json>); archived stop [STOPPED.md](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/attempt1_minphase1/STOPPED.md>).

## Electrodes, bouts and eligibility

| patient | channel | x_tal | y_tal | z_tal | beta_peak_hz | selection_source | flagged | mapping_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bp | 7 | -35.36075 | -17.89367 | 63.12201 | 17 | imagery_rest | 0 | 42 of 44 good motor channels matched to imagery channels |
| ca | 20 | 63.84492 | 1.377282 | 11.24796 | 18 | odd_rest_fallback | 1 | no imagery recording |
| cc | 25 | 55.26799 | -12.24998 | 45.3672 | 15 | odd_rest_fallback | 1 | no imagery recording |
| de | 63 | 61.76889 | -1.303978 | -5.954388 | 17 | odd_rest_fallback | 1 | no imagery recording |
| fp | 46 | -65.15053 | -20.65422 | 15.54406 | 8 | imagery_rest | 0 | 61 of 62 good motor channels matched to imagery channels |
| gc | 60 | -61.03496 | -24.88625 | 36.77627 | 16 | odd_rest_fallback | 1 | no imagery recording |
| gf | 31 | 64.82064 | -12.16517 | 22.58971 | 8 | odd_rest_fallback | 1 | no imagery recording |
| hh | 38 | 58.18861 | -6.130188 | 35.80901 | 16 | imagery_rest | 0 | 41 of 41 good motor channels matched to imagery channels |
| hl | 8 | -45.6625 | -5.535943 | 53.55173 | 22 | odd_rest_fallback | 1 | no imagery recording |
| jc | 43 | -37.97181 | -25.27871 | 63.17067 | 18 | imagery_rest | 0 | 48 of 48 good motor channels matched to imagery channels |
| jf | 10 | -58.06174 | 14.27769 | 6.927413 | 17 | odd_rest_fallback | 1 | no imagery recording |
| jm | 27 | -52.51615 | 26.76353 | -1.670808 | 17 | imagery_rest | 0 | 60 of 61 good motor channels matched to imagery channels |
| jp | 7 | -33 | -26.25406 | 64.71339 | 13 | odd_rest_fallback | 1 | no imagery recording |
| jt | 29 | 65.21728 | -24.35823 | 10.1842 | 18 | odd_rest_fallback | 1 | no imagery recording |
| rh | 3 | 24.64823 | -1.55539 | 63.8946 | 18 | imagery_rest | 0 | 58 of 58 good motor channels matched to imagery channels |
| rr | 19 | 60.06503 | -54.99576 | 21.0035 | 14 | imagery_rest | 0 | 47 of 47 good motor channels matched to imagery channels |
| ug | 17 | 52.12922 | -9.776923 | 47.2097 | 18 | odd_rest_fallback | 1 | no imagery recording |
| wc | 3 | -41.36574 | 4.939022 | 51.37506 | 14 | odd_rest_fallback | 1 | no imagery recording |
| zt | 6 | -34.33665 | -21.0933 | 64.15842 | 15 | odd_rest_fallback | 1 | no imagery recording |

Imagery-rest selection is independent of the primary movement recording. Where imagery was absent, odd rest bouts selected the electrode and only even rest bouts entered analysis. There are 12 flagged patients overall, including ineligible jf; 11 flagged patients enter the 18-patient primary analysis. Sensitivity (a) therefore contains the 7 eligible unflagged patients. Imagery is a secondary replication and its rest data also served electrode selection as prespecified.

Analysed bout counts (before method failures):
| patient | recording | move | rest | flagged |
| --- | --- | --- | --- | --- |
| bp | imagery | 60 | 59 | 0 |
| bp | movement | 60 | 59 | 0 |
| ca | movement | 60 | 29 | 1 |
| cc | movement | 30 | 14 | 1 |
| de | movement | 60 | 29 | 1 |
| fp | imagery | 60 | 59 | 0 |
| fp | movement | 60 | 59 | 0 |
| gc | movement | 60 | 29 | 1 |
| gf | movement | 60 | 45 | 1 |
| hh | imagery | 60 | 59 | 0 |
| hh | movement | 60 | 59 | 0 |
| hl | movement | 60 | 29 | 1 |
| jc | imagery | 60 | 59 | 0 |
| jc | movement | 60 | 59 | 0 |
| jf | movement | 0 | 6 | 1 |
| jm | imagery | 60 | 59 | 0 |
| jm | movement | 60 | 59 | 0 |
| jp | movement | 37 | 18 | 1 |
| jt | movement | 60 | 29 | 1 |
| rh | imagery | 60 | 59 | 0 |
| rh | movement | 60 | 59 | 0 |
| rr | imagery | 60 | 59 | 0 |
| rr | movement | 60 | 59 | 0 |
| ug | movement | 90 | 44 | 1 |
| wc | movement | 60 | 29 | 1 |
| zt | movement | 60 | 44 | 1 |

Movement eligibility (>=10 movement and >=10 rest bouts):
| patient | move_bouts | rest_bouts | eligible |
| --- | --- | --- | --- |
| bp | 60 | 59 | True |
| ca | 60 | 29 | True |
| cc | 30 | 14 | True |
| de | 60 | 29 | True |
| fp | 60 | 59 | True |
| gc | 60 | 29 | True |
| gf | 60 | 45 | True |
| hh | 60 | 59 | True |
| hl | 60 | 29 | True |
| jc | 60 | 59 | True |
| jf | 0 | 6 | False |
| jm | 60 | 59 | True |
| jp | 37 | 18 | True |
| jt | 60 | 29 | True |
| rh | 60 | 59 | True |
| rr | 60 | 59 | True |
| ug | 90 | 44 | True |
| wc | 60 | 29 | True |
| zt | 60 | 44 | True |

jf is ineligible: its 2-s stimulus blocks do not leave 2 s after the 1-s total trimming. It contributes only six analysed rest bouts and no movement bouts, so it is excluded from every endpoint. All 2648 planned bouts, including its diagnostic estimates, were processed once.

## Primary endpoints

Primary 1 uses each eligible patient’s movement-minus-rest mean APC normalized MVL. Primary 2 uses each patient’s mean of the two within-state fP SDs (sample SD, ddof=1), then APC-minus-MVL-Ozkurt differences. Bootstrap resamples patients 10000 times, seed 20261024 (NumPy MT19937 reset per endpoint); percentile 95% intervals use the mean for Primary 1 and median for Primary 2. Wilcoxon is two-sided, zero_method=wilcox, method=auto. There is no prespecified multiplicity correction.

| endpoint | method | n_patients | n_bouts | n_valid_bouts | n_move_valid | n_rest_valid | mean_difference | median_difference | t_statistic | t_df | t_p_two_sided | wilcoxon_statistic | wilcoxon_p_two_sided | ci_low | ci_high | decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| coupling_state | APC-v1.0 | 18 | 1809 | 1809 | 1057 | 752 | 0.002459466 | 0.002140545 | 1.07018 | 17 | 0.2994982 | 65 | 0.3927383 | -0.001904189 | 0.00671545 | Not shown |
| within_state_fP_SD | APC-v1.0 minus MVL-Ozkurt | 18 | 1809 | 1809 | 1057 | 752 | -1.061288 | -0.2874897 | NA | NA | NA | 41 | 0.0538559 | -2.352887 | 0.05664557 | Not shown |

Phase-boundary rates alongside Primary 2 (eligible movement-recording bouts, both states pooled):
| method | n_patients | n_bouts | fp_low | fp_high | any_fp_boundary_fraction |
| --- | --- | --- | --- | --- | --- |
| APC-v1.0 | 18 | 1809 | 1105 | 0 | 0.6108347 |
| MVL-Ozkurt | 18 | 1809 | 286 | 1 | 0.1586512 |

For Primary 2 the inferential tests are the Wilcoxon and median-bootstrap interval; t-test columns are not applicable. Primary 1 decision: **Not shown**. Primary 2 decision: **Not shown**.

Prespecified primary-1 mixed model: outcome ~ state + (1 + state | patient), rest baseline, MATLAB fitlme default ML. It includes 18 patients / 1809 valid movement-recording APC bouts. [mixed_model.mat](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/mixed_model.mat>); log [mixed_model_matlab.log](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/logs/mixed_model_matlab.log>).
| Name | Estimate | SE | tStat | DF | pValue | Lower | Upper |
| --- | --- | --- | --- | --- | --- | --- | --- |
| (Intercept) | 0.07240684 | 0.002235962 | 32.38287 | 1807 | 8.370796e-182 | 0.0680215 | 0.07679219 |
| state_move | 0.002420998 | 0.00230529 | 1.050192 | 1807 | 0.2937702 | -0.002100316 | 0.006942312 |

Model warning: none. No alternate or simplified model was fitted. The one identical refit after the coefficient-export error produced exactly the same displayed model summary, coefficients and covariance parameters: [mixed_export_recovery_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/mixed_export_recovery_verification.json>).

## Secondary 1: rest frequency

Patient medians are reported, with inclusive 12-20-Hz beta-range and +/-2-Hz agreement counts. Spectral peaks use analysed rest bouts, the same symmetric Hann(1000), overlap 500, 1000-point Welch settings, and the largest residual above the 8-30-Hz log-log fit.

| method | n_patients | n_bouts | n_valid_bouts | patients_in_12_20_hz | proportion_in_12_20_hz | patients_within_2_hz | proportion_within_2_hz |
| --- | --- | --- | --- | --- | --- | --- | --- |
| APC-v1.0 | 18 | 752 | 752 | 5 | 0.2777778 | 5 | 0.2777778 |
| GLM | 18 | 752 | 752 | 3 | 0.1666667 | 3 | 0.1666667 |
| KLMI | 18 | 752 | 752 | 0 | 0 | 2 | 0.1111111 |
| MVL-Ozkurt | 18 | 752 | 752 | 0 | 0 | 2 | 0.1111111 |
| MVL-raw | 18 | 752 | 752 | 1 | 0.05555556 | 1 | 0.05555556 |

Prespecified movement-recording patient rest medians:
| patient | method | n_bouts | n_valid | median_fP_hz | rest_spectral_peak_hz | in_12_20_hz | within_2_hz_of_spectrum |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bp | APC-v1.0 | 59 | 59 | 14.10697 | 15 | True | True |
| bp | GLM | 59 | 59 | 10.5 | 15 | False | False |
| bp | KLMI | 59 | 59 | 7 | 15 | False | False |
| bp | MVL-Ozkurt | 59 | 59 | 8.5 | 15 | False | False |
| bp | MVL-raw | 59 | 59 | 8 | 15 | False | False |
| ca | APC-v1.0 | 29 | 29 | 6.011963 | 16 | False | False |
| ca | GLM | 29 | 29 | 8 | 16 | False | False |
| ca | KLMI | 29 | 29 | 7 | 16 | False | False |
| ca | MVL-Ozkurt | 29 | 29 | 8.5 | 16 | False | False |
| ca | MVL-raw | 29 | 29 | 8.5 | 16 | False | False |
| cc | APC-v1.0 | 14 | 14 | 6.011963 | 15 | False | False |
| cc | GLM | 14 | 14 | 12 | 15 | True | False |
| cc | KLMI | 14 | 14 | 6.5 | 15 | False | False |
| cc | MVL-Ozkurt | 14 | 14 | 9.75 | 15 | False | False |
| cc | MVL-raw | 14 | 14 | 10.5 | 15 | False | False |
| de | APC-v1.0 | 29 | 29 | 6.011963 | 18 | False | False |
| de | GLM | 29 | 29 | 10 | 18 | False | False |
| de | KLMI | 29 | 29 | 7 | 18 | False | False |
| de | MVL-Ozkurt | 29 | 29 | 9.5 | 18 | False | False |
| de | MVL-raw | 29 | 29 | 10 | 18 | False | False |
| fp | APC-v1.0 | 59 | 59 | 6.011963 | 8 | False | True |
| fp | GLM | 59 | 59 | 11.5 | 8 | False | False |
| fp | KLMI | 59 | 59 | 7 | 8 | False | True |
| fp | MVL-Ozkurt | 59 | 59 | 9 | 8 | False | True |
| fp | MVL-raw | 59 | 59 | 11 | 8 | False | False |
| gc | APC-v1.0 | 29 | 29 | 14.39063 | 15 | True | True |
| gc | GLM | 29 | 29 | 11.5 | 15 | False | False |
| gc | KLMI | 29 | 29 | 6.5 | 15 | False | False |
| gc | MVL-Ozkurt | 29 | 29 | 9 | 15 | False | False |
| gc | MVL-raw | 29 | 29 | 12 | 15 | True | False |
| gf | APC-v1.0 | 45 | 45 | 6.011963 | 8 | False | True |
| gf | GLM | 45 | 45 | 9.5 | 8 | False | True |
| gf | KLMI | 45 | 45 | 7 | 8 | False | True |
| gf | MVL-Ozkurt | 45 | 45 | 8 | 8 | False | True |
| gf | MVL-raw | 45 | 45 | 8 | 8 | False | True |
| hh | APC-v1.0 | 59 | 59 | 6.011963 | 16 | False | False |
| hh | GLM | 59 | 59 | 10.5 | 16 | False | False |
| hh | KLMI | 59 | 59 | 7 | 16 | False | False |
| hh | MVL-Ozkurt | 59 | 59 | 9 | 16 | False | False |
| hh | MVL-raw | 59 | 59 | 9 | 16 | False | False |
| hl | APC-v1.0 | 29 | 29 | 8.70853 | 22 | False | False |
| hl | GLM | 29 | 29 | 9.5 | 22 | False | False |
| hl | KLMI | 29 | 29 | 7 | 22 | False | False |
| hl | MVL-Ozkurt | 29 | 29 | 8 | 22 | False | False |
| hl | MVL-raw | 29 | 29 | 10 | 22 | False | False |
| jc | APC-v1.0 | 59 | 59 | 6.011963 | 18 | False | False |
| jc | GLM | 59 | 59 | 12 | 18 | True | False |
| jc | KLMI | 59 | 59 | 7.5 | 18 | False | False |
| jc | MVL-Ozkurt | 59 | 59 | 10 | 18 | False | False |
| jc | MVL-raw | 59 | 59 | 10 | 18 | False | False |
| jm | APC-v1.0 | 59 | 59 | 6.011963 | 20 | False | False |
| jm | GLM | 59 | 59 | 11.5 | 20 | False | False |
| jm | KLMI | 59 | 59 | 7 | 20 | False | False |
| jm | MVL-Ozkurt | 59 | 59 | 8.5 | 20 | False | False |
| jm | MVL-raw | 59 | 59 | 9.5 | 20 | False | False |
| jp | APC-v1.0 | 18 | 18 | 6.011963 | 13 | False | False |
| jp | GLM | 18 | 18 | 11.75 | 13 | False | True |
| jp | KLMI | 18 | 18 | 6.75 | 13 | False | False |
| jp | MVL-Ozkurt | 18 | 18 | 8.75 | 13 | False | False |
| jp | MVL-raw | 18 | 18 | 8.5 | 13 | False | False |
| jt | APC-v1.0 | 29 | 29 | 6.011963 | 18 | False | False |
| jt | GLM | 29 | 29 | 10 | 18 | False | False |
| jt | KLMI | 29 | 29 | 7 | 18 | False | False |
| jt | MVL-Ozkurt | 29 | 29 | 8.5 | 18 | False | False |
| jt | MVL-raw | 29 | 29 | 9 | 18 | False | False |
| rh | APC-v1.0 | 59 | 59 | 6.011963 | 19 | False | False |
| rh | GLM | 59 | 59 | 10 | 19 | False | False |
| rh | KLMI | 59 | 59 | 7 | 19 | False | False |
| rh | MVL-Ozkurt | 59 | 59 | 9.5 | 19 | False | False |
| rh | MVL-raw | 59 | 59 | 9.5 | 19 | False | False |
| rr | APC-v1.0 | 59 | 59 | 13.69133 | 14 | True | True |
| rr | GLM | 59 | 59 | 9.5 | 14 | False | False |
| rr | KLMI | 59 | 59 | 8 | 14 | False | False |
| rr | MVL-Ozkurt | 59 | 59 | 9.5 | 14 | False | False |
| rr | MVL-raw | 59 | 59 | 10 | 14 | False | False |
| ug | APC-v1.0 | 44 | 44 | 13.72004 | 18 | True | False |
| ug | GLM | 44 | 44 | 9 | 18 | False | False |
| ug | KLMI | 44 | 44 | 7.5 | 18 | False | False |
| ug | MVL-Ozkurt | 44 | 44 | 7.75 | 18 | False | False |
| ug | MVL-raw | 44 | 44 | 8.75 | 18 | False | False |
| wc | APC-v1.0 | 29 | 29 | 8.209814 | 13 | False | False |
| wc | GLM | 29 | 29 | 11 | 13 | False | True |
| wc | KLMI | 29 | 29 | 7 | 13 | False | False |
| wc | MVL-Ozkurt | 29 | 29 | 9.5 | 13 | False | False |
| wc | MVL-raw | 29 | 29 | 10.5 | 13 | False | False |
| zt | APC-v1.0 | 44 | 44 | 12.35462 | 16 | True | False |
| zt | GLM | 44 | 44 | 12 | 16 | True | False |
| zt | KLMI | 44 | 44 | 7 | 16 | False | False |
| zt | MVL-Ozkurt | 44 | 44 | 9 | 16 | False | False |
| zt | MVL-raw | 44 | 44 | 9.5 | 16 | False | False |

All patient medians and spectral peaks, including sensitivities and imagery: [rest_frequency_patient_table.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/rest_frequency_patient_table.csv>); source peaks [analysed_rest_spectral_peaks.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/analysed_rest_spectral_peaks.csv>).

## Secondary 2-5

All state-frequency/carrier-frequency differences are descriptive, with no expected direction. Each scan’s normalized coupling uses its own selected frequency pair. Imagery repeats the coupling state contrast; hand/tongue are separate descriptive comparisons against that patient’s analysed rest bouts. All use eligible patients and report their valid-bout denominators.
| recording | endpoint | method | n_patients | n_bouts | n_valid_bouts | mean_difference | wilcoxon_p_two_sided | ci_low | ci_high | decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| movement | fP_state | APC-v1.0 | 18 | 1809 | 1809 | -0.9558352 | 0.008964539 | -1.585784 | -0.3616148 | Descriptive |
| movement | fA_state | APC-v1.0 | 18 | 1809 | 1809 | -0.1606475 | 0.8317261 | -2.066072 | 1.824832 | Descriptive |
| imagery | imagery_coupling | APC-v1.0 | 7 | 833 | 833 | 0.001186682 | 0.578125 | -0.003957598 | 0.0060462 | Not shown |
| movement | subtype_coupling_hand | APC-v1.0 | 18 | 1282 | 1282 | 0.001020995 | 0.5226135 | -0.003291802 | 0.004967512 | Descriptive |
| movement | subtype_coupling_tongue | APC-v1.0 | 18 | 1279 | 1279 | 0.003909926 | 0.1963882 | -0.001534736 | 0.00951266 | Descriptive |
| movement | coupling_state | MVL-raw | 18 | 1809 | 1809 | 0.002033214 | 0.2462082 | -0.001125686 | 0.005148957 | Not shown |
| movement | fP_state | MVL-raw | 18 | 1809 | 1809 | -0.3661308 | 0.2837296 | -0.9685431 | 0.2270603 | Descriptive |
| movement | fA_state | MVL-raw | 18 | 1809 | 1809 | -0.3191666 | 0.5508728 | -1.25254 | 0.4989072 | Descriptive |
| imagery | imagery_coupling | MVL-raw | 7 | 833 | 833 | 0.006645031 | 0.03125 | 0.00311916 | 0.01004555 | Opposite |
| movement | subtype_coupling_hand | MVL-raw | 18 | 1282 | 1282 | -0.000226672 | 0.7987061 | -0.003587175 | 0.003305814 | Descriptive |
| movement | subtype_coupling_tongue | MVL-raw | 18 | 1279 | 1279 | 0.0043644 | 0.03423309 | 0.0006084363 | 0.008544449 | Descriptive |
| movement | coupling_state | MVL-Ozkurt | 18 | 1809 | 1809 | 0.004187973 | 0.01593018 | 0.001160382 | 0.007272991 | Opposite |
| movement | fP_state | MVL-Ozkurt | 18 | 1809 | 1809 | -0.2947684 | 0.1963882 | -0.684599 | 0.08763151 | Descriptive |
| movement | fA_state | MVL-Ozkurt | 18 | 1809 | 1809 | 1.550136 | 0.3037949 | -0.2818991 | 3.865466 | Descriptive |
| imagery | imagery_coupling | MVL-Ozkurt | 7 | 833 | 833 | 0.006267783 | 0.03125 | 0.003015389 | 0.009395849 | Opposite |
| movement | subtype_coupling_hand | MVL-Ozkurt | 18 | 1282 | 1282 | 0.001184147 | 0.4422989 | -0.002318352 | 0.004686724 | Descriptive |
| movement | subtype_coupling_tongue | MVL-Ozkurt | 18 | 1279 | 1279 | 0.007281043 | 0.0008392334 | 0.003633743 | 0.01151609 | Descriptive |
| movement | coupling_state | KLMI | 18 | 1809 | 1809 | 0.0008401676 | 0.7660294 | -0.002052374 | 0.004135948 | Not shown |
| movement | fP_state | KLMI | 18 | 1809 | 1809 | -0.2514038 | 0.07368469 | -0.4559929 | -0.05622083 | Descriptive |
| movement | fA_state | KLMI | 18 | 1809 | 1809 | 1.044143 | 0.5798416 | -1.115789 | 3.302958 | Descriptive |
| imagery | imagery_coupling | KLMI | 7 | 833 | 833 | 0.004940941 | 0.109375 | -0.0004934915 | 0.01022159 | Not shown |
| movement | subtype_coupling_hand | KLMI | 18 | 1282 | 1282 | -0.001885693 | 0.3247299 | -0.006323783 | 0.002897535 | Descriptive |
| movement | subtype_coupling_tongue | KLMI | 18 | 1279 | 1279 | 0.003716754 | 0.0538559 | 1.56697e-05 | 0.007373925 | Descriptive |
| movement | coupling_state | GLM | 18 | 1809 | 1809 | -1.976432e-05 | 0.9661179 | -0.001803912 | 0.00184456 | Not shown |
| movement | fP_state | GLM | 18 | 1809 | 1809 | -0.3220977 | 0.4682922 | -0.9160403 | 0.2390089 | Descriptive |
| movement | fA_state | GLM | 18 | 1809 | 1809 | -0.7762099 | 0.4682922 | -2.753152 | 1.202314 | Descriptive |
| imagery | imagery_coupling | GLM | 7 | 833 | 833 | 0.0002362816 | 0.9375 | -0.004492774 | 0.004606801 | Not shown |
| movement | subtype_coupling_hand | GLM | 18 | 1282 | 1282 | -0.00131074 | 0.4682922 | -0.004247441 | 0.001756756 | Descriptive |
| movement | subtype_coupling_tongue | GLM | 18 | 1279 | 1279 | 0.001296236 | 0.4422989 | -0.001390086 | 0.004127248 | Descriptive |

Full statistics (including t statistics, p values, state-specific valid counts and all sensitivity rows): [ecog_statistics.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/ecog_statistics.csv>). Patient-level differences: [patient_differences.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/patient_differences.csv>).

## Secondary 6: failures and boundaries

The table includes all processed bouts, including the six jf rest bouts; endpoint tables exclude jf. Scan boundaries are fP=6/30 and fA=80/148 Hz; APC boundaries are fP within 0.05 Hz of 6/30 and fA=80/150 Hz. Valid-only and all-bout boundary rates are separate:
| recording | method | state | n_patients | n_bouts | n_valid | failure_count | failure_rate | fp_low | fp_high | fp_boundary_rate_all | fp_boundary_rate_valid | fa_low | fa_high | fa_boundary_rate_valid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| imagery | APC-v1.0 | move | 7 | 420 | 420 | 0 | 0 | 297 | 0 | 0.7071429 | 0.7071429 | 14 | 16 | 0.07142857 |
| imagery | APC-v1.0 | rest | 7 | 413 | 413 | 0 | 0 | 271 | 0 | 0.6561743 | 0.6561743 | 13 | 22 | 0.08474576 |
| imagery | GLM | move | 7 | 420 | 420 | 0 | 0 | 37 | 1 | 0.09047619 | 0.09047619 | 29 | 57 | 0.2047619 |
| imagery | GLM | rest | 7 | 413 | 413 | 0 | 0 | 44 | 0 | 0.1065375 | 0.1065375 | 45 | 50 | 0.2300242 |
| imagery | KLMI | move | 7 | 420 | 420 | 0 | 0 | 118 | 0 | 0.2809524 | 0.2809524 | 44 | 41 | 0.202381 |
| imagery | KLMI | rest | 7 | 413 | 413 | 0 | 0 | 114 | 0 | 0.2760291 | 0.2760291 | 36 | 37 | 0.1767554 |
| imagery | MVL-Ozkurt | move | 7 | 420 | 420 | 0 | 0 | 59 | 1 | 0.1428571 | 0.1428571 | 42 | 54 | 0.2285714 |
| imagery | MVL-Ozkurt | rest | 7 | 413 | 413 | 0 | 0 | 58 | 0 | 0.1404358 | 0.1404358 | 47 | 53 | 0.2421308 |
| imagery | MVL-raw | move | 7 | 420 | 420 | 0 | 0 | 55 | 4 | 0.1404762 | 0.1404762 | 273 | 10 | 0.6738095 |
| imagery | MVL-raw | rest | 7 | 413 | 413 | 0 | 0 | 64 | 0 | 0.1549637 | 0.1549637 | 271 | 12 | 0.68523 |
| movement | APC-v1.0 | move | 18 | 1057 | 1057 | 0 | 0 | 684 | 0 | 0.6471145 | 0.6471145 | 48 | 44 | 0.08703879 |
| movement | APC-v1.0 | rest | 19 | 758 | 758 | 0 | 0 | 422 | 0 | 0.5567282 | 0.5567282 | 27 | 24 | 0.06728232 |
| movement | GLM | move | 18 | 1057 | 1057 | 0 | 0 | 104 | 4 | 0.102176 | 0.102176 | 112 | 104 | 0.2043519 |
| movement | GLM | rest | 19 | 758 | 758 | 0 | 0 | 77 | 2 | 0.1042216 | 0.1042216 | 77 | 76 | 0.201847 |
| movement | KLMI | move | 18 | 1057 | 1057 | 0 | 0 | 312 | 0 | 0.295175 | 0.295175 | 104 | 97 | 0.1901608 |
| movement | KLMI | rest | 19 | 758 | 758 | 0 | 0 | 194 | 0 | 0.2559367 | 0.2559367 | 85 | 80 | 0.2176781 |
| movement | MVL-Ozkurt | move | 18 | 1057 | 1057 | 0 | 0 | 169 | 0 | 0.1598865 | 0.1598865 | 104 | 111 | 0.2034059 |
| movement | MVL-Ozkurt | rest | 19 | 758 | 758 | 0 | 0 | 118 | 1 | 0.1569921 | 0.1569921 | 95 | 79 | 0.2295515 |
| movement | MVL-raw | move | 18 | 1057 | 1057 | 0 | 0 | 151 | 0 | 0.1428571 | 0.1428571 | 804 | 4 | 0.7644276 |
| movement | MVL-raw | rest | 19 | 758 | 758 | 0 | 0 | 99 | 3 | 0.1345646 | 0.1345646 | 556 | 4 | 0.7387863 |

These boundary rates must be considered alongside Primary 2: frequent lower-edge selection can reduce a method’s SD. All numeric fP values and per-patient boundary rates are in [ecog_bout_estimates.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/ecog_bout_estimates.csv>) and [ecog_patient_summary.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/ecog_patient_summary.csv>).

## Sensitivity analyses

(a) Excludes the 11 eligible flagged patients; seven patients remain. (b) Keeps only bouts >=2.5 s, with every other rule unchanged. No movement bouts meet the latter duration restriction, so its movement-rest and within-state comparative endpoints are not estimable. The threshold was not changed. Available rest-only summaries remain in the patient table.

| subset | endpoint | n_patients | n_bouts | n_valid_bouts | mean_difference | median_difference | wilcoxon_p_two_sided | ci_low | ci_high | decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sensitivity_a | coupling_state | 7 | 833 | 833 | -0.002593474 | -0.001767964 | 0.46875 | -0.009609326 | 0.004443804 | Not shown |
| sensitivity_a | within_state_fP_SD | 7 | 833 | 833 | -2.129915 | -2.352887 | 0.046875 | -4.175283 | -0.2973465 | Supported |
| sensitivity_b | coupling_state | 0 | 0 | 0 | NA | NA | NA | NA | NA | Not estimable |
| sensitivity_b | within_state_fP_SD | 0 | 0 | 0 | NA | NA | NA | NA | NA | Not estimable |

All secondary sensitivity rows: [ecog_statistics.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/ecog_statistics.csv>); patient/state summaries [ecog_patient_summary.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/ecog_patient_summary.csv>).

## Figure and output files

Four panels: A patient/state mean fP (APC vs MVL-Ozkurt); B normalized MVL; C each patient’s movement-minus-rest APC normalized MVL with within-state bout-bootstrap 95% CIs (10000, seed 20261024); D patient median rest APC fP vs analysed-rest peak. There are no titles or footers inside the image. PNG at 300 dpi: [ecog_four_panel.png](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/ecog_four_panel.png>); vector [ecog_four_panel.svg](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/ecog_four_panel.svg>). Commit, protocol hash and source CSVs are embedded as hidden metadata; [figure_provenance.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/figure_provenance.json>).

Merged per-bout results: [ecog_bout_estimates.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/ecog_bout_estimates.csv>). Patient summaries: [ecog_patient_summary.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/ecog_patient_summary.csv>). Statistics: [ecog_statistics.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/ecog_statistics.csv>). Per-bout burst counts were added as a separate unchanged-Step-1 diagnostic without rerunning APC frequency/coupling estimation. The detector matched the existing canonical count exactly; [postprocess_runtime.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/postprocess_runtime.json>). Worker CSVs are preserved.

## Runtime and deviations

Progress plus four-worker run (including MATLAB startup): 503.453 s. Supplemental burst diagnostics/rest spectra: 18.605 s. Four MATLAB processes used one computational thread each. No completed dataset bout was recomputed.

- Undocumented state codes: Codes 13 in gf and 15 in zt were not analysed; only documented codes 0, 11 and 12 were used.
- Bad-channel rule: The library supplies no bad-channel list; the prespecified recording-level variance rule (>5 or <0.2 times median channel variance) was applied.
- Patient eligibility: jf is ineligible because its 2-s blocks leave less than the required 2 s after trimming 0.5 s per end.
- Pre-run comparator-copy verification newline assumption: The setup verifier initially assumed CRLF, but both originals use LF. It was corrected to detect the actual newline before reversing the permitted profile addition. No comparator or protected source changed and no dataset estimates had been computed. The setup resumed from the already-preserved archive without repeating moves.
- Progress-check cache: The first 10 bp APC results are saved and their four scans computed before seeding the worker-1 CSV. Its unchanged resume mechanism skips these complete keys; no reported bout is estimated twice.
- Progress-check canonical CSV import: MATLAB automatic header detection did not expose the signal column in the canonical CSV. The import now explicitly sets comma delimiter, header line and variable-name reading. The error occurred before the synthetic estimator call and before any bp bout estimate. The failed log/runtime and script are preserved; no estimated bout was rerun.
- Figure rendering tooling fixes: The initial render completed but its user-home font-cache write was denied. The plotting script now uses a cache under the work folder. Visual QA also showed boundary markers partly clipped by the panel-D axis at 6 Hz; display limits were padded to 5-31 Hz. The scientific grid, estimates, statistics and figure source CSVs are unchanged. Only the figure is rerendered.
- Mixed-model coefficient export: The prespecified fitlme fit completed, but R2022b returned coefficients as a dataset, so writetable failed before the model object was saved. The exporter now saves the fitted model before export and applies dataset2table. The identical model is refitted once with unchanged formula, data and default settings, under protocol 9.2. No APC/scan estimate or bootstrap endpoint is repeated. The failed script/log are preserved.
- The existing worker writes NaN in n_bursts. A separate diagnostic reproduces unchanged Step 1 from the saved prepared input and fills that recorded field in the merged CSV; no fP/fA/score is selected again and neither the copied feature wrapper nor the worker receives extra edits.
- The cached first ten progress bouts are absent from worker 1’s newly-computed status counter but present in its CSV and every final rate/statistic. The existing combined stop checks were retained; all 2648 completed bouts were checked at the end.
- Pre-existing MATLAB startup warnings concern missing historical Brainstorm directories. They did not change source precedence or the computations.

Preservation and completeness checks: [final_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/final_verification.json>). Output inventory and hashes: [output_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ecog_miller_motor/output_manifest.json>).
