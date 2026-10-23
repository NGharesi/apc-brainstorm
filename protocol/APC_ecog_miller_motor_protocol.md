# APC human electrocorticography analysis (Miller ECoG library, motor task): prespecified protocol

Written 2026-10-23, before any file of this dataset has been downloaded or read. It is committed to the repository before the analysis starts and is not edited afterwards; any change is appended as a dated amendment with its reason.

Lesson carried over from the ds004752 analysis (protocol/APC_ieeg_ds004752_protocol.md): APC's Step 3 needs complete epochs of +/-3 cycles of the slow rhythm around each trough. Here the expected coupled rhythm is the sensorimotor beta rhythm (about 12-20 Hz), so +/-3 cycles span about +/-0.2 s, well inside the 2-s bouts.

## 1. Questions and expected answers

Miller et al. (2012, PLoS Comput Biol 8:e1002655) reported that, in human sensorimotor cortex, high-frequency (broadband) activity is phase-entrained on the 12-20 Hz beta rhythm at rest, and that the entrainment is diminished or eliminated during movement. This mirrors the rodent run/rest analysis.

- **Primary 1 (coupling by state):** APC's normalized coupling (normalized MVL at APC's own fP and fA) is lower during movement than during rest.
- **Primary 2 (precision):** within each state, APC's fP varies less from bout to bout than the fP of the MVL-Ozkurt scan.
- **Key secondary (expected frequency):** at rest, APC's fP lies in the beta range and agrees with the rest spectral peak.

## 2. Data

- **Source.** Miller, K.J. (2016). A library of human electrocorticographic data and analyses. Stanford Digital Repository, https://purl.stanford.edu/zk881ps0522 (CC BY-SA 4.0); described in Miller (2019), Nat Hum Behav 3:1225-1235. Use the original full-precision MATLAB files, not the Neuromatch Academy float16 copy.
- **Task.** The motor task of Miller et al. (2010, PNAS 107:4430-4435). Patients with peri-rolandic subdural grids alternate cued blocks of repetitive hand or tongue movement (about 3 s, about 1 Hz movements) with rest. A separate motor-imagery recording uses the same grid.
- **Local path.** `D:\APC_project\RealDatasets\Miller_ECoG_library\`. Download the motor experiment folder (and its imagery counterpart, if separate) with all subjects, the location files and the library documentation.

## 3. Inventory gate (before any signal processing)

- List every subject and recording. For each recording, record: file, sampling rate, number of channels, duration, stimulus/state variable, and its codes with counts.
- Determine the code for rest and the codes for movement (expected 0 = rest, 11 = tongue, 12 = hand) from the library documentation and scripts.
- Record the original ethics statement (institutional review board and consent) from the dataset or task paper.
- **Stop** if the state coding cannot be determined unambiguously, or if a recording has no per-sample state variable.

## 4. Preprocessing (fixed)

1. Recordings not sampled at 1000 Hz are resampled to 1000 Hz with MATLAB resample() before any other step (e.g. 1200 Hz with p/q = 5/6).
2. Bad channels:
   - use the library's bad-channel list if one exists;
   - otherwise, a channel is bad if its variance is above 5 times or below 0.2 times the median channel variance of that recording.
3. Common average reference over the good channels of each recording.
4. Zero-phase notch filters at 60, 120 and 180 Hz: each a 4th-order Butterworth band-stop, +/-1 Hz, realized as second-order sections and applied with filtfilt. Check every filter for pole radius < 1.

## 5. Bouts

- **Movement bout:** a contiguous run of samples with a movement code (hand and tongue pooled).
- **Rest bout:** a contiguous run of rest samples.
- Trim 0.5 s from both ends of every bout, to remove transitions and reaction time.
- Keep bouts that are at least 2.0 s long after trimming.
- Exclude the first and last 2 s of each recording.
- **Eligibility:** a patient is included if their movement recording has at least 10 movement and 10 rest bouts.
- **Imagery recording:** bouts are defined the same way and analysed only as a secondary replication.

## 6. Electrode (one per patient, chosen from independent data)

- **Rule:** the good electrode with the largest rest-state beta peak. Peak height = the largest residual of the log Welch spectrum above a log-log linear fit over 8-30 Hz, using 1000-sample Hann windows with 50% overlap, averaged over rest bouts.
- **Data used for selection:** the rest bouts of the imagery recording, which is a separate recording, so the analysed movement-recording bouts do not influence the choice.
- If a patient has no imagery recording, use the odd-numbered rest bouts of the movement recording for selection, and analyse only the even-numbered rest bouts plus all movement bouts. Flag that patient.
- Report the chosen electrode, its location (from the library's location files) and its peak frequency.

## 7. Methods applied to each bout

- **APC.** `src/bst_apc.m` at the HEAD of branch `neuroimage-submission` (default version v1, identical to tag v1.0); `fA = [80 150]`; other options default. Features through `revision_checks\rodent_multi\v1_bout_features.m`.
- **Equivalence gate first:** reproduce the canonical burst-coupled values (fP 7.99792313403792 Hz, fA 122 Hz, raw MVL 0.176907779165945, preferred phase 178.575795410875 deg) to within 1e-10, as in the ds004752 protocol section 4.1.
- **Scans.** `ecog_comparators.m` = a copy of `revision_checks\final\sos_comparators.m` with one added profile `"ecog"`. Existing profiles must be byte-identical.
  - Phase grid 6:0.5:30 Hz, half-width 1.5 Hz.
  - Amplitude grid 80:4:148 Hz, mode `"ecog_A2_prime"` with half-width 30 Hz (at least the largest candidate fP; band edges clipped at 1 Hz and fs/2 - 1 as in the original).
  - Metrics MVL-raw, MVL-Ozkurt, KLMI and GLM. **MVL-Ozkurt is the prespecified primary comparator.**
- **Recorded per bout:** patient, recording, state, movement type, bout, duration, method, fP, fA, score, raw MVL, normalized MVL, preferred phase, status, number of bursts, and boundary flags.
  - Scans: fP = 6 or 30 Hz; fA = 80 or 148 Hz.
  - APC: fP within 0.05 Hz of 1 or 30 Hz; fA = 80 or 150 Hz.

## 8. Statistics

Patient-level values are means over bouts with valid estimates.

### 8.1 Primary 1

- Movement minus rest difference in APC normalized MVL, per patient.
- Across patients: one-sample t test, Wilcoxon signed-rank test, and percentile-bootstrap 95% CI of the mean (10,000 resamples, seed 20261024).
- Mixed model: outcome ~ state + (1 + state | patient) on bout-level data.
- **Supported** if the bootstrap CI lies entirely below 0. **Opposite** if it lies above 0. **Not shown** otherwise.

### 8.2 Primary 2

- Per patient: the within-state SD of fP across bouts, averaged over rest and movement, for APC and for the MVL-Ozkurt scan.
- Paired difference (APC minus scan) across patients: Wilcoxon signed-rank test and bootstrap 95% CI of the median.
- **Supported** if the CI lies entirely below 0. Report boundary-hit rates alongside, because a method stuck on a grid edge has an artificially small SD.

### 8.3 Secondary

1. Rest fP, per method:
   - patient medians;
   - proportion of patients with a median within 12-20 Hz;
   - proportion with a median within 2 Hz of the patient's rest spectral peak (section 6 rule, computed on the analysed rest bouts).
2. Movement minus rest difference in fP and fA (APC and scans), with the same tests as Primary 1. Descriptive; no expected direction.
3. Primary 1 for each scan's own normalized MVL at its own selected pair.
4. Imagery replication: Primary 1 on the imagery recording (Miller et al., 2010, reported a smaller beta decrease during imagery than during movement).
5. Hand and tongue bouts separately (descriptive).
6. Status-failure and boundary-hit rates per method and state.

### 8.4 Sensitivity analyses

- (a) Excluding patients flagged in section 6.
- (b) Bouts of at least 2.5 s only.

## 9. Stop rules

1. No dataset signal is processed before this protocol is committed and pushed and the gates in sections 3 and 7 have passed.
2. Each reportable run is done once. A crash or code defect may be fixed once, and only if it can be identified without looking at outcomes. Log the diff, the reason and the rerun.
3. Nothing in sections 4-8 changes after the reportable run starts.
4. Method-relevant problems stop the run, with a report and no workaround. These include: more than half of the bouts invalid for a method (checked after every 200 bouts and at the end), the equivalence gate failing, and ambiguous state coding.
5. Every result is reported, whatever its direction.

## 10. Outputs

Folder `C:\Users\nghare\.brainstorm\process\revision_checks\ecog_miller_motor\`:
- `RESULTS_ecog.md`: inventory, gates, ethics statement, electrodes, bout counts, all endpoint tables (with n patients and n bouts), status and boundary rates, deviations.
- `ecog_bout_estimates.csv`, `ecog_patient_summary.csv`, `ecog_statistics.csv`, `provenance.json`.
- Figure, as in the rodent Figure 6/7 style (300-dpi PNG and SVG, **no titles or footers inside the image**):
  - A: rest and movement fP per patient, APC vs MVL-Ozkurt scan;
  - B: rest and movement normalized MVL;
  - C: movement minus rest differences per patient with bootstrap CIs;
  - D: rest fP vs rest spectral peak.

## Amendment 1 (2026-10-23): APC phase search range matched to the scans

**Reason.** The run stopped under rule 9.4 at the first combined check: APC v1.0 returned status 4 (no complete trough epochs) in 127 of 200 bouts. 225 bouts were complete when the workers halted: movement 36 of 143 valid, rest 40 of 82 valid. Valid APC fP values were about 3-6 Hz or about 13-17 Hz. APC searched phase frequencies from 1 Hz (default minPhaseHz), whereas the scans search 6-30 Hz. In 2-s bouts, Step 2 was drawn to slow components, including the 1-2 Hz repetitive movements; at those frequencies the +/-3-cycle trough epochs of Step 3 cannot fit in a bout. No endpoint was computed. Attempt 1 outputs are kept (revision_checks/ecog_miller_motor/attempt1_minphase1/) and will be reported.

**Change (section 7).** APC options become `fA = [80 150]`, `minPhaseHz = 6`, `maxPhaseHz = 30`, so APC searches the same phase range as the scans. These are existing options of the unchanged code; all other options stay default. APC boundary flags become: fP within 0.05 Hz of 6 or 30 Hz. Everything else is unchanged: preprocessing, bouts, electrodes (the prep files from attempt 1 are reused), scans, endpoints, statistics, seeds and stop rules. Rule 9.4 still applies.
