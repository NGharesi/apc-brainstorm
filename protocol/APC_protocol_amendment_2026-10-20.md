# APC protocol amendment (2026-10-20)

Written Mon 2026-10-19, 22:30-23:00 ET, before any run listed here. It supplements `APC_event_carrier_validation_protocol.md` (frozen 2026-10-16), which stays in force. Nothing below is changed after a reportable run starts; later entries go only in the run log (section 6).

## 1. Frozen code (v1.1.0)

- Method code: `bst_apc.m` as of 2026-10-14 (adds `minPhaseCycles` = 3 by default and linear detrending of the burst-triggered average before the Welch peak), `apc_event_carrier.m`, `calc_MI_all_methods.m`, `process_apc.m`.
- Analysis scripts: listed with SHA-256 hashes in `APC_freeze_manifest_2026-10-20.csv`. Published as tag `v1.1.0` on https://github.com/NGharesi/apc-brainstorm.
- The previous public release (commit 82f7559, 2026-10-05) used the earlier phase rule. Earlier outputs were produced with that release or with intermediate local versions. Every result in the manuscript will state which version produced it; results from different versions are not pooled.

## 2. Complete list of analyses to run

Priority order if time runs short: P1, P2, P3, P4, P6, P5, P7, P8.

| ID | Analysis | Call(s) | Seed | Status at freeze of this amendment |
|---|---|---|---|---|
| P1 | Premise test: bursts locked to a slow rhythm that is not the dominant spectral peak | `run_apc_premise_two_rhythm_benchmark('smoke')`, then `('holdout')` | 20261021 (smoke 20261019) | New; not run |
| P2 | Matched-grid competing-distractor benchmark, stable IIR comparator filters | `run_apc_comparator_fairness_benchmark('stable_filter_smoke')`, then `('stable_filter_holdout')` | 20261020 | Coded 2026-10-16; not run |
| P3 | Full-pipeline null calibration, APC-event-carrier | `run_apc_full_pipeline_null_calibration('hybrid_reviewer')` | 20261020 | Prespecified 2026-10-16; running (220/1000 replicates at 22:30 ET) |
| P4 | Full-pipeline null calibration, original APC, frozen v1.1.0 | `run_apc_full_pipeline_null_calibration_frozen('frozen_smoke')`, then `('frozen_reviewer')` | 20261005 (same as earlier `reviewer`, so signals are paired across code versions) | New fork of the null script; not run |
| P5 | Continuous-PAC boundary benchmark, v1.1.0, plus matched-grid scanned MVL, KLMI, GLM and event-phase comparators | `run_apc_continuous_pac_boundary_benchmark('frozen_smoke')`, then `('frozen_reviewer')` | 20261006 (paired with earlier `reviewer`) | New profile; not run |
| P6 | DREAMS external spindle validation: APC-event-carrier, original APC (v1.1.0), raw scanned PAC, normalized scanned PAC | `run_apc_dreams_spindle_external_validation('hybrid')` | deterministic (200-shift time null as coded) | Prespecified 2026-10-16; smoke only |
| P7 | HC-3 rodent carrier replication and held-out burst-PLV test vs raw spectral peak, v1.1.0 | `run_apc_hc3_multianimal_validation('frozen_reviewer')`; `run_apc_hc3_holdout_burst_validation('frozen_reviewer')` | 20261007 (as coded) | New profiles; not run |
| P8 | Optional: EC013 run/rest method comparison rerun with v1.1.0 | `run_apc_ec013_run_rest_method_comparison` | as coded | Only if time remains before the analysis freeze; otherwise existing outputs are reported with their version label |

Not run in this submission window: debugging of the OpenNeuro ds004752 iEEG screening (returned NaN), further OMEGA MEG work, any new dataset, and any parameter tuning.

### P1 design (fixed here)

- Generator: identical to the sparse-burst holdout (500 Hz, 8 s, 120-Hz bursts, sigma 28 ms, jitter 10 ms, coupling 0.60, background burst scale 0.18, mixed pink + 0.5 white noise at -3 dB SNR, same burst-phase rule), with a second, uncoupled sinusoid of random phase added.
- Cells, 100 repeats each: A_keep100 and A_keep040 (bursts locked to 5 Hz at amplitude 0.5; uncoupled 11 Hz at amplitude 1.0); B_keep100 and B_keep040 (locked to 11 Hz at 0.5; uncoupled 5 Hz at 1.0); R_single_keep100 (single coupled 8-Hz rhythm, reference); N_uncoupled (single 8-Hz rhythm, bursts at uniform random times).
- Methods on the identical signal: APC; APC with `flipTroughs` = false; APC-event-carrier; APC-noflip-event-carrier; Spectral-peak-event-carrier (fP = largest residual of the Welch log spectrum above a log-log linear fit, 1-30 Hz, 2-s Hann window, 50% overlap, NFFT 4096; fA by the frozen `apc_event_carrier` rule); matched-grid MVL, Ozkurt-MVL, KLMI, GLM and event-phase scans (fP 1:1:30 Hz, fA 88:4:148 Hz, stable IIR filters).
- Primary endpoint: joint recovery, with fP within 1 Hz of the coupled rhythm and fA within 8 Hz of 120 Hz.
- Primary contrast: APC-event-carrier minus Spectral-peak-event-carrier, paired within repeat, percentile bootstrap with 10,000 resamples.
- Secondary contrasts: APC-noflip-event-carrier minus spectral baseline; APC minus APC-noflip; APC-event-carrier minus GLM-scan; APC-event-carrier minus event-phase-scan.
- Secondary outcomes: rate of fP selected at the uncoupled distractor; AUC of each method's raw score for R_single_keep100 versus N_uncoupled.
- Decision rule: the premise is SUPPORTED only if the primary-contrast 95% interval is above zero in both A_keep100 and B_keep100. Above zero in only one is PARTIAL and does not support a general claim. Otherwise it is NOT SUPPORTED.

## 3. Reporting rules

- Every method in every analysis is reported, including methods that match or beat APC (GLM-scan, event-phase scan, normalized PAC, fixed-pair oracle PAC). No comparator, condition, cell, excerpt, animal or session is dropped after results are seen.
- DREAMS: all four methods on all four prespecified outcomes (sigma-carrier fraction, precision, recall, precision above the shifted-annotation null). The earlier 72-window screening AUCs are disclosed as a pilot. With 6 excerpts, the smallest attainable two-sided exact sign-flip p is 0.03125; this is stated.
- DREAMS with v1.1.0: the prespecified epoch of [-1, 1] s with `minPhaseCycles` = 3 restricts APC fP to at least about 1.5 Hz, while the PAC phase grid spans 0.5-4 Hz. This configuration was prespecified on 2026-10-16 and is not changed; it is disclosed.
- Results from earlier code versions or from the direct-form filter comparators are reported only as superseded or supplementary, labelled with their version.
- Completed analyses not yet in the manuscript are reported: HC-3 multi-animal replication, held-out burst PLV versus raw spectral peak, operational validation, the OMEGA pilot, and the OpenNeuro iEEG screening (as attempted and not completed).
- Known discrepancies to resolve or disclose in the text:
  - The multi-animal configuration lists EC016, but no EC016 sessions appear in the outputs.
  - The continuous-PAC and null-calibration generators use cumulative-sum (random-walk) noise plus white noise, not pink noise.
  - The burst-phase rule (`phase_offset_deg` = -90) places bursts at the rising zero-crossing of the sine carrier (Hilbert phase -90 degrees). Supplementary Table S2 calls -90 degrees the trough. The text will be corrected after checking against the code.

## 4. Stop rule

1. Only the analyses in section 2 are run. Smoke profiles check syntax and are never reported.
2. Each reportable profile runs once. A crash or code defect may be fixed once, and only if the defect can be identified without reference to the outcome. The diff, the reason and the rerun are logged in section 6.
3. No change to parameters, grids, tolerances, seeds, conditions or endpoints after a reportable run starts.
4. Analysis freeze: Wednesday 2026-10-21, 12:00 ET. Any run not complete by then is reported as not completed and supports no claim. After the freeze, work is limited to figures, text and a scripted check of every reported number against its source file.
5. If P1 is not SUPPORTED, or does not finish, the manuscript makes no claim that APC's burst-timing phase estimate identifies the coupled rhythm independently of the dominant spectral peak.
6. Submission target: Thursday 2026-10-22, 17:00 ET.

## 5. Claims permitted by each outcome (fixed now)

- P1 SUPPORTED: APC (and the extension) identified the burst-locked rhythm when it was not the spectral peak in these simulations, beyond a spectral-peak baseline, reported alongside all scanned comparators. Otherwise the manuscript states that in the tested simulations and data APC's fP was equivalent to, or not shown to improve on, the spectral peak.
- P2: relative ranking of APC, GLM-scan and event-phase scan as observed. Superiority wording only where the paired 95% interval excludes zero in APC's favour, consistent with the 2026-10-16 rule.
- P3 and P4: holdout false-positive rate per condition with Wilson intervals and the coupled-control sensitivity. The word "artifact-robust" is used only if the transient-artifact holdout false-positive rate has a Wilson upper bound of 10% or less.
- P5: AUC and joint recovery for APC and each scanned comparator; fixed-pair oracles stay labelled as oracles.
- P6: extension and original APC versus each PAC comparator only through paired excerpt-level intervals. No superiority wording unless the interval excludes zero in APC's favour against both raw and normalized PAC.
- P7: carrier stability, and added value over the raw spectral peak only as the held-out test shows.

## 6. Run log (append-only)

| Local time (ET) | ID | Profile | Note |
|---|---|---|---|
| 2026-10-19 22:30 | P3 | hybrid_reviewer | Running; checkpoint 220/1000 replicates. Started before this amendment, as prespecified on 2026-10-16. |
