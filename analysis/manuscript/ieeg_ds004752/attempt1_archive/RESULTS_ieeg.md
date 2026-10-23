# Human intracranial APC analysis: STOPPED at the reading gate

Status: **STOPPED_METHOD_RELEVANT**. No dataset APC/scan estimates or endpoint results exist for this prespecified run. See [STOPPED.md](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/STOPPED.md>).

## Provenance and requested push

Clean branch `neuroimage-submission`, HEAD `81835945681cbbcb69eb61ce9c5f745acccbc297`. Protocol SHA-256 `8c613b0f8d8ea61fb2a922fbfb58531907d37f278c596ea946a165f75837a804` matches the requested value. `git push origin neuroimage-submission --tags` succeeded, publishing the branch and tags v1.0/v2.0. No new commit was created.

MATLAB 9.13.0.2105380 (R2022b) Update 2. All toolbox versions, full APC options, comparator settings, seed 20261023 and full path/source SHA-256 records are in [provenance.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/provenance.json>). The five requested source/helper files and protocol were rehashed at the stop and remain unchanged.

## Equivalence gate: PASS

Resolved `bst_apc` path: [bst_apc.m](<C:/Users/nghare/.brainstorm/process/apc-brainstorm-publish/src/bst_apc.m>). The source copy in the repository, rather than frozen_v1, was used on the saved synthetic 500-Hz input with fA=[80,150]. Status 0; all four absolute differences are <=1e-10.

| metric | expected | observed | absolute_difference |
| --- | --- | --- | --- |
| fP (Hz) | 7.99792313403792 | 7.99792313403792 | 3.5527136788005e-15 |
| fA (Hz) | 122 | 122 | 0 |
| raw Canolty MVL | 0.176907779165945 | 0.176907779165945 | 1.38777878078145e-16 |
| preferred phase (degrees) | 178.575795410875 | 178.575795410875 | 3.69482222595252e-13 |

Evidence: [equivalence_gate.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/equivalence_gate.json>); [equivalence_gate.mat](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/equivalence_gate.mat>).

## EDF reading gate: FAIL; stop required

**sub-11/ses-01 is 4000 Hz**, verified independently from its EDF sample/record header, all 36 channels.tsv sampling-frequency entries, and JSON SamplingFrequency. The protocol section 3.1 requires 2000 Hz. Sample count 1,600,000 and channel order match the sidecars. No signal check or method estimate was computed for this file after the header gate failed.

38 files passed all checks before the failure, covering 2224 channels. Their channel order/count, sample counts, 2000-Hz rate, no nonfinite values, nonzero variance and median absolute magnitude below 10^4 microvolts passed. The 39th file failed; 29 remaining files were not attempted.

Complete attempted-file checks: [edf_file_checks.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/edf_file_checks.csv>). Passed-file channel checks: [edf_channel_checks.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/edf_channel_checks.csv>). Failure evidence: [sampling_rate_failure_evidence.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/sampling_rate_failure_evidence.json>). MATLAB log: [reading_gates_matlab.log](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/reading_gates_matlab.log>).

| file | channels | samples | events_last_end_sample | fs_hz | header_channel_order_match | header_passed | passed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-01\ses-01\ieeg\sub-01_ses-01_task-verbalWM_run-01_ieeg.edf | 48 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-01\ses-02\ieeg\sub-01_ses-02_task-verbalWM_run-01_ieeg.edf | 48 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-01\ses-03\ieeg\sub-01_ses-03_task-verbalWM_run-01_ieeg.edf | 48 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-01\ses-04\ieeg\sub-01_ses-04_task-verbalWM_run-01_ieeg.edf | 48 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-02\ses-01\ieeg\sub-02_ses-01_task-verbalWM_run-01_ieeg.edf | 64 | 784000 | 784000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-02\ses-02\ieeg\sub-02_ses-02_task-verbalWM_run-01_ieeg.edf | 64 | 752000 | 752000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-02\ses-03\ieeg\sub-02_ses-03_task-verbalWM_run-01_ieeg.edf | 64 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-02\ses-04\ieeg\sub-02_ses-04_task-verbalWM_run-01_ieeg.edf | 64 | 768000 | 768000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-02\ses-05\ieeg\sub-02_ses-05_task-verbalWM_run-01_ieeg.edf | 64 | 736000 | 736000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-02\ses-06\ieeg\sub-02_ses-06_task-verbalWM_run-01_ieeg.edf | 64 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-02\ses-07\ieeg\sub-02_ses-07_task-verbalWM_run-01_ieeg.edf | 64 | 784000 | 784000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-03\ses-01\ieeg\sub-03_ses-01_task-verbalWM_run-01_ieeg.edf | 40 | 752000 | 752000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-03\ses-02\ieeg\sub-03_ses-02_task-verbalWM_run-01_ieeg.edf | 40 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-03\ses-03\ieeg\sub-03_ses-03_task-verbalWM_run-01_ieeg.edf | 40 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-04\ses-01\ieeg\sub-04_ses-01_task-verbalWM_run-01_ieeg.edf | 64 | 784000 | 784000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-04\ses-02\ieeg\sub-04_ses-02_task-verbalWM_run-01_ieeg.edf | 64 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-05\ses-01\ieeg\sub-05_ses-01_task-verbalWM_run-01_ieeg.edf | 32 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-05\ses-02\ieeg\sub-05_ses-02_task-verbalWM_run-01_ieeg.edf | 32 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-05\ses-03\ieeg\sub-05_ses-03_task-verbalWM_run-01_ieeg.edf | 32 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-06\ses-01\ieeg\sub-06_ses-01_task-verbalWM_run-01_ieeg.edf | 64 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-06\ses-02\ieeg\sub-06_ses-02_task-verbalWM_run-01_ieeg.edf | 64 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-06\ses-03\ieeg\sub-06_ses-03_task-verbalWM_run-01_ieeg.edf | 64 | 784000 | 784000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-06\ses-04\ieeg\sub-06_ses-04_task-verbalWM_run-01_ieeg.edf | 64 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-06\ses-05\ieeg\sub-06_ses-05_task-verbalWM_run-01_ieeg.edf | 64 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-06\ses-06\ieeg\sub-06_ses-06_task-verbalWM_run-01_ieeg.edf | 64 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-06\ses-07\ieeg\sub-06_ses-07_task-verbalWM_run-01_ieeg.edf | 64 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-07\ses-01\ieeg\sub-07_ses-01_task-verbalWM_run-01_ieeg.edf | 64 | 784000 | 784000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-07\ses-02\ieeg\sub-07_ses-02_task-verbalWM_run-01_ieeg.edf | 64 | 768000 | 768000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-07\ses-03\ieeg\sub-07_ses-03_task-verbalWM_run-01_ieeg.edf | 64 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-07\ses-04\ieeg\sub-07_ses-04_task-verbalWM_run-01_ieeg.edf | 64 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-08\ses-01\ieeg\sub-08_ses-01_task-verbalWM_run-01_ieeg.edf | 62 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-08\ses-02\ieeg\sub-08_ses-02_task-verbalWM_run-01_ieeg.edf | 62 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-08\ses-03\ieeg\sub-08_ses-03_task-verbalWM_run-01_ieeg.edf | 62 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-08\ses-04\ieeg\sub-08_ses-04_task-verbalWM_run-01_ieeg.edf | 62 | 800000 | 800000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-09\ses-01\ieeg\sub-09_ses-01_task-verbalWM_run-01_ieeg.edf | 64 | 768000 | 768000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-09\ses-02\ieeg\sub-09_ses-02_task-verbalWM_run-01_ieeg.edf | 64 | 784000 | 784000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-10\ses-01\ieeg\sub-10_ses-01_task-verbalWM_run-01_ieeg.edf | 80 | 544000 | 544000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-10\ses-02\ieeg\sub-10_ses-02_task-verbalWM_run-01_ieeg.edf | 80 | 688000 | 688000 | 2000 | 1 | 1 | 1 |
| D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-11\ses-01\ieeg\sub-11_ses-01_task-verbalWM_run-01_ieeg.edf | 36 | 1600000 | 1600000 | 4000 | 1 | 0 | 0 |

## Earlier screening NaN cause

The earlier screening configured n_surrogates=0, so local_analyze_epoch never assigned the preinitialized NaN apc_z/pac_z fields; the saved screening coupling strengths and selected frequencies are finite.
All 64 saved screening rows have finite APC/scanned coupling strengths and selected frequencies; all 64 apc_z and pac_z entries are NaN. This earlier screening is not a result of the current protocol. Evidence: [earlier_screening_nan_cause.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/earlier_screening_nan_cause.json>).

## Trial timeline: literature evidence recorded; empirical gate not run

Boran et al. Figure 1a gives 1-s fixation, 2-s encoding and 3-s maintenance before the probe; this places encoding at 1 s and probe at 6 s relative to trial start. [Scientific Data paper, Figure 1a](https://www.nature.com/articles/s41597-020-0364-3.pdf). Dimakopoulos et al. describe the same encoding/maintenance sequence and probe-relative periods. [eLife paper, task methods](https://elifesciences.org/articles/78677).

The grand-average scalp gate, plot and peak latencies were not computed because the earlier required reading gate failed. The timeline has therefore **not passed the full protocol gate**. Paper evidence: [timeline_paper_evidence.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/timeline_paper_evidence.json>).

## Metadata inventory at stop; no fixed contact or trial choices

Metadata inventory contains 68 iEEG sessions, 15 patients and 3353 trials. There are 99 metadata candidate adjacent hippocampal pairs across 14 patients; sub-13 has none. No power-ratio selection, notch filtering, robust-SD exclusion or eligibility assessment was run. The artifact-flag counts below are metadata counts, not completed preprocessing or inclusion results.

| patient | sessions | metadata_trials | dataset_artifact_flag_trials | candidate_pairs | selected_pair |
| --- | --- | --- | --- | --- | --- |
| sub-01 | 4 | 200 | 24 | 4 | not selected: gate stopped |
| sub-02 | 7 | 339 | 20 | 3 | not selected: gate stopped |
| sub-03 | 3 | 147 | 13 | 8 | not selected: gate stopped |
| sub-04 | 2 | 99 | 5 | 7 | not selected: gate stopped |
| sub-05 | 3 | 150 | 17 | 6 | not selected: gate stopped |
| sub-06 | 7 | 349 | 11 | 13 | not selected: gate stopped |
| sub-07 | 4 | 197 | 11 | 13 | not selected: gate stopped |
| sub-08 | 4 | 200 | 34 | 6 | not selected: gate stopped |
| sub-09 | 2 | 97 | 9 | 13 | not selected: gate stopped |
| sub-10 | 2 | 77 | 0 | 5 | not selected: gate stopped |
| sub-11 | 6 | 300 | 0 | 1 | not selected: gate stopped |
| sub-12 | 6 | 300 | 1 | 4 | not selected: gate stopped |
| sub-13 | 6 | 300 | 5 | 0 | not selected: gate stopped |
| sub-14 | 8 | 398 | 18 | 11 | not selected: gate stopped |
| sub-15 | 4 | 200 | 0 | 5 | not selected: gate stopped |

Metadata sources: [metadata_file_inventory.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/metadata_file_inventory.csv>), [metadata_candidate_pairs.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/metadata_candidate_pairs.csv>), [metadata_patient_counts_at_stop.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/metadata_patient_counts_at_stop.csv>). `contacts.csv` and `trial_inclusion.csv` have not been created because their fixed choices were not made.

## Endpoints, failure rates and requested final figure: not computed

Primary endpoint, secondary endpoints 1-6, exploratory load models, sensitivities (a)/(b), boundary-hit/failure rates and the four-panel final figure were not run. No primary decision is stated because no reportable endpoint run occurred. All dataset method counts are zero. No placeholder result CSVs were created.

The comparator copy was prepared but never run on dataset trials. Reverse edits recover the original helper byte-for-byte: [ieeg_comparators.diff](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/ieeg_comparators.diff>); [ieeg_comparator_copy_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/ieeg_comparator_copy_verification.json>).

## Deviations and resolved tooling errors

- resolved tooling path lookup: An initial read guessed a sidecar without the run-01 entity. File discovery established the actual BIDS names; no signal, setting or outcome was changed.
- resolved EDF unit metadata reader defect: All 48 EDF physical-dimension fields in the first file are blank; the BIDS channels.tsv declares microvolts. The first reader incorrectly required an EDF unit label as well as numeric range checks. The corrected reader accepts the BIDS declaration when the EDF field is blank and still rejects conflicting nonblank units. No signal scaling, thresholds, methods or protocol text changed.
- pre-existing MATLAB startup path warnings: MATLAB startup lists nonexistent historical Brainstorm directories. Explicit source-path assertions passed. No startup or installation changes were made.
- resolved EDF wall-clock header syntax: MATLAB rejects seconds=60. Two local analysis-folder copies carry the minute (10.28.60 to 10.29.00; 14.23.60 to 14.24.00). Only header bytes 176:184 changed; all bytes from offset 256 onward are SHA-256 identical. Originals remain untouched. Analysis uses events.tsv sample indices, not EDF wall-clock times.
- resolved JSON provenance serialization: MATLAB jsondecode sanitizes object keys containing full paths. Full path/hash records are additionally stored as an array; values and source files are unchanged.

The unit-reader correction and header compatibility corrections were identified without dataset PAC outcomes. Initial failed-reader checks/logs are archived in this folder. Source diffs: [unit_reader_fix.diff](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/unit_reader_fix.diff>) and [header_time_reader_fix.diff](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/header_time_reader_fix.diff>). Header-copy payload hashes: [edf_header_copies.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/edf_header_copies.json>). Original EDF files were not modified.

No method setting was changed after the 4000-Hz finding. The run stopped rather than resampling or excluding the session. Gate/status record: [STATUS.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/STATUS.json>).
