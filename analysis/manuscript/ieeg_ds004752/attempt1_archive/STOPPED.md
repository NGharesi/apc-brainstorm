# STOPPED: prespecified iEEG sampling-rate gate

The run stopped at protocol section 3.1. The EDF for `sub-11/ses-01` is sampled at **4000 Hz**, whereas the committed protocol requires **2000 Hz for every iEEG file**. The EDF header, `channels.tsv` and JSON sidecar independently agree on 4000 Hz. This is a method-relevant mismatch.

File: [sub-11_ses-01_task-verbalWM_run-01_ieeg.edf](<D:/APC_project/RealDatasets/OpenNeuro_ds004752/sub-11/ses-01/ieeg/sub-11_ses-01_task-verbalWM_run-01_ieeg.edf>). Evidence: [sampling_rate_failure_evidence.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/sampling_rate_failure_evidence.json>).

The failing file has 36 channels and 1,600,000 samples; channel order and sample count match the sidecars. Its EDF contains 400 records of 1 s with 4000 samples per channel per record.

Before the stop, 38/68 iEEG files passed all reading checks. The failing file was the 39th; the remaining 29 files were not attempted. The APC equivalence gate passed (maximum absolute difference 3.694822225952521e-13).

No ds004752 APC or scan output was computed. No contacts were selected, no trial rejection or endpoint analysis was performed, and the scalp timeline gate was not run after the reading gate failed. No resampling or exclusion was used to bypass the gate.

The protocol, src files and tagged code remain unchanged. The repository remains clean at `81835945681cbbcb69eb61ce9c5f745acccbc297`. The requested branch/tags push succeeded. No new commit was created.

A protocol decision is required before analysis can resume. Full gate report: [RESULTS_ieeg.md](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/RESULTS_ieeg.md>).
