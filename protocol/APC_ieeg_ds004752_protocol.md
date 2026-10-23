# APC human intracranial analysis (OpenNeuro ds004752): prespecified protocol

Written 2026-10-22, before any ds004752 signal is analysed. Only metadata (participants.tsv, channels.tsv, electrodes.tsv, events.tsv, JSON sidecars) has been read. An earlier screening of this dataset crashed (NaN outputs) and produced no outcome. This file is committed to the repository before the analysis starts and is not edited afterwards; any change is appended as a dated amendment with its reason.

## 1. Question

Does APC give more reproducible phase-carrier frequency (fP) estimates than frequency-scanning PAC estimators in human hippocampal recordings? In the rodent data, APC's fP varied less across bouts than the scans' fP. Here the primary test is reproducibility across recording sessions within each patient, which needs no ground-truth frequency.

## 2. Data

- Dataset: OpenNeuro ds004752 v1.0.1 (Dimakopoulos et al., 2022, eLife 11:e78677; Boran et al., 2020, Sci Data 7:30). CC0. Written informed consent; approved by the institutional ethics review board (PB 2016-02055).
- Local path: `D:\APC_project\RealDatasets\OpenNeuro_ds004752`.
- 15 patients with drug-resistant epilepsy; 2-8 sessions each; about 50 trials per session; depth electrodes; iEEG sampled at 2000 Hz; common intracranial reference; power-line frequency 50 Hz.
- Each session's `*_ieeg.edf` holds consecutive 8-s trials (begSample/endSample in `*_events.tsv`). Only the iEEG files are used; scalp EEG is used only for the timing check in section 3.2.

## 3. Preprocessing (fixed)

### 3.1 Reading

- Read each `*_ieeg.edf` in MATLAB. Check that: the channel order and count match `*_channels.tsv`; the number of samples equals the last endSample in `*_events.tsv`; sampling rate = 2000 Hz; no NaN; every channel has non-zero variance; values are in microvolts (median absolute value below 10^4). Stop if a check fails.

### 3.2 Trial timeline

- Expected timeline within each 8-s trial: fixation 0-1 s, encoding 1-3 s, maintenance 3-6 s, probe from 6 s.
- Verify this from the dataset papers. Also check it in the data: the grand-average scalp EEG at O1, O2 or Oz (whichever exist), over all trials of all patients, should show a visual evoked response within 50-250 ms after 1 s (letter onset) and after 6 s (probe onset). Report the plot and the peak latencies.
- If the timeline cannot be confirmed, stop and report; no APC or scan output may be computed until it is.
- **Analysis window: the maintenance period, 3.0-6.0 s of each trial (6000 samples).** It contains no stimulus, so stimulus-evoked responses do not enter the burst-triggered averages.

### 3.3 Contact pair (one per patient, fixed before any APC or scan output)

- Candidate pairs: adjacent contacts k and k+1 on the same electrode (same name prefix), present in every session of the patient, where at least one of the two has an `AnatomicalLocation` in `*_electrodes.tsv` that begins with `Hipp`.
- Bipolar signal = contact k minus contact k+1.
- Selection: the pair with the highest ratio of 4-8 Hz to 1-4 Hz power. Power comes from Welch spectra (2000-sample Hann window, 50% overlap) of the notch-filtered maintenance windows of all included trials (section 3.5) from all sessions, averaged. Ties go to the deeper pair (lower k).
- Patients with no candidate pair are excluded and listed (from the metadata, sub-13 has no `Hipp` label).
- Report the chosen pair, its labels and its ratio for each patient.

### 3.4 Filtering

- Per trial, on the full 8-s trial before cutting the maintenance window: remove the mean; zero-phase notch at 50, 100 and 150 Hz (each a 4th-order Butterworth band-stop, +/-1 Hz, realized as second-order sections and applied with filtfilt). Check every filter for pole radius < 1.
- Then cut 3.0-6.0 s.

### 3.5 Trial inclusion

- Exclude trials with `Artifact` = 1 in `*_events.tsv`.
- Exclude a trial if, in its maintenance window on the selected bipolar signal, any sample deviates from the session median by more than 6 robust SD, or any first difference exceeds 6 robust SD of the first differences. Robust SD = 1.4826 x MAD, computed per session over the maintenance windows of all trials not flagged by the dataset.
- Report the counts of trials removed by each rule.
- A session is eligible if it has at least 20 included trials. A patient enters the primary analysis if they have at least 2 eligible sessions.

## 4. Methods applied to each included trial (3-s maintenance window)

### 4.1 APC

- Code: `src/bst_apc.m` at the HEAD of branch `neuroimage-submission` in `C:\Users\nghare\.brainstorm\process\apc-brainstorm-publish`, with the default version (`v1`, identical to tag v1.0).
- Options: `fA = [80 150]`; all others default, as in the rodent analysis.
- Features: through `revision_checks\rodent_multi\v1_bout_features.m` (fP, fA, raw MVL, normalized MVL, preferred phase, status, route).
- Equivalence gate before any ds004752 trial is analysed: run HEAD `bst_apc.m` on `revision_checks\final\burst_coupled_input.csv` (fs 500 Hz, fA [80 150]) and reproduce `canonical_results.csv` (APC v1.0, burst_coupled): fP = 7.99792313403792 Hz, fA = 122 Hz, raw MVL = 0.176907779165945, preferred phase = 178.575795410875 deg. Maximum absolute difference must be at most 1e-10. Stop if not.

### 4.2 Scans (comparators)

- `ieeg_comparators.m` = a copy of `revision_checks\final\sos_comparators.m` with one added profile `"ieeg"`. Existing profiles are unchanged.
- Phase grid 2:0.5:12 Hz, half-width 1.5 Hz (the lower band edge is clipped at 0.5 Hz as in the original).
- Amplitude grid 80:4:148 Hz, mode `"ieeg_A2_prime"` with half-width 12 Hz (at least the largest candidate fP).
- Metrics: MVL-raw, MVL-Ozkurt (normalized MVL), KLMI and GLM, with the same filters, guards, ties and selection rules as the rodent analysis.
- Prespecified primary comparator: the **MVL-Ozkurt scan**. The other three are secondary.

### 4.3 Recorded per trial

patient, session, trial, set size, correct, method, fP, fA, score, raw MVL, normalized MVL, preferred phase, status, number of bursts (APC), boundary flags (scans: fP = 2 or 12 Hz, fA = 80 or 148 Hz; APC: fP within 0.05 Hz of 1 or 30 Hz, fA = 80 or 150 Hz).

## 5. Endpoints and statistics

Session mean fP = mean over the session's trials with a valid estimate (APC status 0; scans finite score). The mean rather than the median is used because scan estimates lie on a 0.5-Hz grid.

### 5.1 Primary endpoint

- For each patient in the primary analysis: SD across sessions of the session mean fP, computed for APC and for the MVL-Ozkurt scan.
- Contrast: paired difference (APC minus scan) across patients.
- Tests: two-sided Wilcoxon signed-rank test, and percentile-bootstrap 95% CI of the median paired difference (10,000 resamples of patients, seed 20261023).
- Decision: APC is **more reproducible** if the upper CI bound is below 0; **less reproducible** if the lower bound is above 0; **no difference shown** otherwise.
- Interpretation guard: report boundary-hit rates next to this result. A method that returns the same grid edge in every trial would appear perfectly reproducible.

### 5.2 Secondary endpoints

1. Within-session trial-to-trial SD of fP, per method. Patient-level means are compared, APC vs each scan, with the same test and bootstrap.
2. ICC(1) of session mean fP across patients, per method, with a bootstrap 95% CI over patients. This measures how well fP separates patients relative to session-to-session variation.
3. The primary contrast repeated for APC vs each secondary scan (MVL-raw, KLMI, GLM).
4. Status-failure and boundary-hit rates per method.
5. Dominant-rhythm check:
   - Session spectral peak = the largest residual above a log-log linear fit of the averaged Welch spectrum (section 3.3 settings) over 2-12 Hz.
   - Report the proportion of sessions whose APC session mean fP lies within 1 Hz of that peak, and the Spearman correlation between them.
6. Coupling relative to a trial-shuffled null (descriptive):
   - For each session and method, take every trial's selected phase band and amplitude band. For APC these are the phase band of `v1_bout_features` and `info.final_band_hz`; for scans, [fP +/- 1.5] and [fA +/- 12].
   - Observed statistic: mean normalized MVL over trials.
   - Null: 1000 derangements that pair trial i's phase with trial pi(i)'s amplitude envelope (seed 20261023).
   - Report the proportion of sessions with p < 0.05 per method.
   - Because frequencies were selected within each real trial, this null is optimistic for every method; it is reported as descriptive only.

### 5.3 Exploratory (labelled as such in any report)

- Memory-load effect: fitlme outcome ~ SetSize + (1|patient) + (1|patient:session), for APC fP and APC normalized MVL. SetSize is continuous; included trials, correct and incorrect.

### 5.4 Sensitivity analyses

- (a) Without the robust amplitude rejection; dataset artifact flags only.
- (b) Referential signal from the deeper contact of the selected pair instead of the bipolar signal.

## 6. Stop rules

1. No ds004752 trial is analysed before this protocol is committed and the gates in 3.1, 3.2 and 4.1 have passed.
2. Each reportable run is done once. A crash or code defect may be fixed once, and only if the defect can be identified without looking at outcomes. Log the diff, the reason and the rerun.
3. Nothing in sections 3-5 changes after the reportable run starts: windows, contacts, grids, thresholds, seeds, endpoints.
4. Method-relevant problems (APC or scans returning NaN for most trials, the equivalence gate failing, timeline not confirmed): stop and report; do not work around.
5. Every result is reported, whatever its direction.

## 7. Outputs

Folder `C:\Users\nghare\.brainstorm\process\revision_checks\ieeg_ds004752\`:
- `RESULTS_ieeg.md`: gates, timeline check, contacts, trial counts, endpoint tables, figures, deviations.
- `ieeg_trial_estimates.csv`, `ieeg_session_summary.csv`, `ieeg_patient_summary.csv`, `ieeg_statistics.csv`, `provenance.json` (git commit, MATLAB version, option sets, seeds, file hashes).
- Figure (300-dpi PNG and SVG, **no titles or footers inside the image**):
  - A: session mean fP per patient for APC and the MVL-Ozkurt scan;
  - B: paired within-patient across-session SD;
  - C: APC session mean fP vs session spectral peak;
  - D: observed vs null coupling.

## Amendment 1 (2026-10-23): sampling rates

**Reason.** The reading gate (section 3.1) stopped at sub-11/ses-01, which is sampled at 4000 Hz. The protocol wrongly assumed 2000 Hz for every file; that assumption came from the first subject's sidecar only. From the metadata (JSON sidecars, EDF headers, events.tsv), 38 of the 68 iEEG files are at 2000 Hz. Twenty files (sub-11, sub-12, sub-14) are at 4000 Hz, and ten files (sub-13, sub-15) are at 4096 Hz. The scalp EEG files of those subjects use the same rates. The hardware filters are the same in all files (0.5-1000 Hz). This amendment was written after the gate failure and before any signal-derived quantity (spectra, contact selection, APC or scan output) was computed for any file. No outcome informed it.

**Change to section 3.1.** The fs check becomes: fs equals the JSON sidecar, channels.tsv and EDF header, and is one of 2000, 4000 or 4096 Hz. Stop if any file has another rate or the sources disagree. Each trial must span exactly 8 x fs samples in events.tsv.

**New step 3.0, applied before section 3.2.**
- Every iEEG and scalp-EEG trial recorded at 4000 or 4096 Hz is resampled to 2000 Hz.
- Each 8-s trial is resampled separately (trials are discontinuous): it is cut at its native begSample-endSample, then resampled with MATLAB resample() (default anti-aliasing FIR) using p/q = 1/2 for 4000 Hz and 125/256 for 4096 Hz. Each trial must give exactly 16,000 samples.
- Files at 2000 Hz are not resampled. All later steps are unchanged and operate on 2000-Hz trials.
- Record the native rate per file in the outputs and report the number of patients and sessions at each native rate.
- Sensitivity (c): repeat the primary endpoint without the patients recorded at a native rate other than 2000 Hz.

## Amendment 2 (2026-10-23): scalp-EEG rates for the timeline check

**Reason.** Codex asked how to handle the scalp-EEG files, which Amendment 1 did not cover correctly. From the metadata, scalp EEG is at 200 Hz in 36 files (sub-01 to sub-09), 2000 Hz in 2 files (sub-10), 4000 Hz in 20 files and 4096 Hz in 10 files. Scalp EEG is used only for the trial-timeline check (section 3.2) and never enters contact selection, APC, the scans or any endpoint. Written before any signal-derived quantity was computed.

**Change.** Amendment 1's resampling of scalp EEG to 2000 Hz (16,000 samples per trial) is replaced by the following:
- For the timeline check only, every scalp trial is resampled separately to 200 Hz with MATLAB resample(): p/q = 1/10 from 2000 Hz, 1/20 from 4000 Hz, 25/512 from 4096 Hz; 200-Hz trials are unchanged.
- Assert exactly 1,600 samples per 8-s trial. Evoked-response latencies are reported at 5-ms resolution.
- Resampling of iEEG to 2000 Hz under Amendment 1 is unchanged.
