# APC version 3.0 (aperiodic-corrected Step 2): prespecified development and evaluation protocol

Written 2026-10-23, before any v3.0 code exists. It is committed and pushed before implementation and is not edited afterwards; any change is appended as a dated amendment with its reason. v1.0 remains the method of the submitted manuscript. This protocol decides whether v3.0 can replace it.

## 1. Motivation

In short human segments, APC v1.0 selected the lowest admissible phase frequency:
- ECoG (protocol/APC_ecog_miller_motor_protocol.md): with a 6-30 Hz range, fP lay at 6 Hz in 61% of bouts; with a 1-30 Hz range, Step 3 could not complete in most bouts.
- ds004752 (protocol/APC_ieeg_ds004752_protocol.md): fP estimates were 1-3 Hz.

The likely cause is that Step 2 picks the largest value of the burst-triggered-average (BTA) spectrum, and aperiodic (1/f) power is largest at the lowest frequencies. v3.0 changes only Step 2: it locates the largest peak above a fitted aperiodic background (Donoghue et al., 2020) instead of the largest value.

## 2. v3.0 specification (fixed here)

Implemented in `src/bst_apc.m` as `OPTIONS.version = 'v3'`. The default stays `'v1'`. The v1 and v2 code paths must remain bit-identical (gate G0).

- **Steps 1, 3 and 4, and all defaults:** identical to v1.0. This includes the epoch [-0.6, 0.6] s, polarity alignment, phase filter, trough detection, fA selection and coupling.

**Step 2 (v3):**
1. **Spectrum.** P(f) is the v1.0 BTA spectrum: the same Welch call and zero-padding to at most 0.05 Hz.
2. **Admissible range.** [f_lo, f_hi]:
   - f_hi = min(maxPhaseHz, fs/3, fA_min - 0.5), as in v1.0.
   - f_lo = max(minPhaseHz, 7/T), where T is the signal duration in seconds. This feasibility bound guarantees that one complete +/-3-cycle trough epoch fits in the signal.
3. **Aperiodic fit** of log10 P against log10 f over [f_lo, f_hi], with no knee:
   - pass 1: ordinary least squares on all points;
   - pass 2: ordinary least squares on the points whose pass-1 residual is at or below the median pass-1 residual.
   - Residual r(f) = log10 P(f) minus the pass-2 fit.
   - sigma = SD of the pass-2 residuals over the points used in pass 2.
4. **Candidate peaks:** strict interior local maxima of r (not the first or last admissible bin) with r >= 2 x sigma.
5. **fP:** the candidate with the largest r, refined by three-point parabolic interpolation of r (the v1.0 refinement rule applied to r).
6. If there is no candidate, return **status 3** ("no admissible phase carrier"). No fallback is used.
7. **Extra outputs:** aperiodic exponent, offset, peak height r(fP) and sigma (diagnostics only).

**Baseline for comparison ("SP-raw"):** the same Step-2 rule (items 2-6) applied to the Welch spectrum of the raw signal instead of the BTA. Window = min(2 s, T); Hann; 50% overlap; zero-padding to at most 0.05 Hz. SP-raw gives fP only. It tests whether v3.0's use of burst timing adds anything beyond the ordinary aperiodic-corrected power spectrum.

## 3. Phase A: implementation, gates and freeze

- **G0 (no regression):**
  - default/v1 reproduces the canonical APC v1.0 values (fP 7.99792313403792, fA 122, raw MVL 0.176907779165945, preferred phase 178.575795410875) to within 1e-10;
  - v2 reproduces its tagged outputs on the same input;
  - `git diff v1.0 -- src/bst_apc.m` changes only additions for v3 and the version switch.
- **G1 (canonical):** v3 on the canonical burst-coupled input returns status 0, with fP within 0.1 Hz of 8 Hz and fA within 8 Hz of 120 Hz.
- **G2 (aperiodic, short segments):** synthetic signals built from the development generator family, seed 20261031, 20 repeats per cell:
  - fs 1000 Hz;
  - background: 1/f^beta noise (beta = 1 and 2), unit SD;
  - rhythm: 15-Hz sinusoid with amplitude 0.6;
  - bursts: 110-Hz Gaussian-envelope bursts (sigma 10 ms, amplitude 1.5) at the rhythm's troughs on 55% of cycles, jitter 5 ms;
  - durations 2 s and 6 s.
  - **Pass** if, in each cell, v3 returns fP within 1 Hz of 15 Hz in at least 16 of 20 repeats. Report v1.0 (minPhaseHz 1) in the same cells.
- **G3 (descriptive, no pass/fail):** the same background with bursts at Poisson times and no rhythm. Report the status-3 rate and the distribution of fP.
- **Gate failure:** the protocol stops. Any redesign needs a dated amendment, and the failed attempt is reported.
- **Freeze:** when G0-G2 pass, commit and tag `v3.0`. The held-out generator (section 4) is committed in the same commit, before any held-out signal is generated.

## 4. Phase B: held-out evaluation (generated only after the freeze; seed 20261101)

### HA: aperiodic regime

- **Design:** 3 x 3 x 2 cells, 25 coupled trials each (450 trials).
  - background exponent beta in {1, 1.5, 2}, unit SD;
  - rhythm amplitude a in {0.3, 0.5, 0.8}, at fP ~ U(6, 25) Hz;
  - duration T in {2, 6} s.
- **Signal:**
  - fs 1000 Hz;
  - bursts at fA ~ U(80, 140) Hz: Gaussian envelope (sigma 10 ms, amplitude 1.5), centred on rhythm troughs on 55% of cycles, jitter 5 ms;
  - weak background bursts (scale 0.18, as in the development generator).
- **Paired timing nulls:** every coupled trial has a null in which only the coupled burst times are replaced by a homogeneous Poisson process at the same mean rate.

### HB: original held-out suite

- Regenerate H1-H4 exactly (seed 20261022, existing generator). Verify against the saved v1.0 per-trial results: v1.0 rerun estimates must match them.

### Methods

- APC v1.0 (default range);
- APC v3.0;
- SP-raw (fP only);
- the four A2' scans:
  - HA: phase grid 3:0.5:30 Hz (half-width 1.5); amplitude grid 80:4:160 Hz (half-width 30);
  - HB: the original A2' configuration.
- Filters are SOS-guarded as in the manuscript.

### Metrics

- As in the manuscript: joint recovery (fP within 1 Hz, fA within 8 Hz), strict joint recovery (fP within 0.5 Hz), fP recovery, false joint recovery in paired nulls.
- Status counts. Invalid outputs count as failures.
- Wilson 95% CIs; exact McNemar tests for paired comparisons.

### Adoption criteria (all of A1, A3 and A4 must pass for v3.0 to be recommended)

- **A1 (improvement):** HA joint recovery, pooled over all cells, v3.0 > v1.0, one-sided exact McNemar p < 0.05.
- **A2 (key secondary, not a gate):** HA fP recovery, v3.0 vs SP-raw (exact McNemar, two-sided). Reported as the answer to whether burst timing adds information beyond the aperiodic-corrected spectrum.
- **A3 (non-inferiority on the original suite):**
  - H1 joint recovery v3.0 >= v1.0 - 10 (of 175);
  - H2 >= v1.0 - 10 (of 150);
  - H4 >= v1.0 - 3 (of 25).
- **A4 (specificity):** false joint recovery in paired nulls (H3 and HA nulls pooled), v3.0 <= v1.0 + 5 percentage points.

If any of A1, A3 or A4 fails, v3.0 is not recommended, Phase C is not run, and the result is reported as a negative result.

## 5. Phase C: real data (only if A1, A3 and A4 pass)

### Rodent

- Rerun the prespecified 5-s and the post hoc 2-s run/rest analyses with APC v3.0, reusing the saved bouts, channels and analysis code (`revision_checks/rodent_multi`).
- Report the same tables next to v1.0. Expectation: same direction; no new claim.

### ECoG

- Reuse prep files, bouts and electrodes from `revision_checks/ecog_miller_motor` unchanged.
- APC v3.0 with fA [80 150], minPhaseHz 1, maxPhaseHz 30 (the feasibility bound applies automatically). The scan results are reused.
- Endpoints: Primary 1 and Primary 2 of the ECoG protocol; secondary 1; sensitivity (a).
- **ECoG success criterion for v3.0:** median rest fP within 2 Hz of the rest spectral peak in at least 9 of 18 patients (v1.0 with a 6-30-Hz range: 5 of 18).
- Also report:
  - the agreement of SP-raw computed on the same rest bouts;
  - status-3 rates per patient and state;
  - the proportion of fP values within 0.05 Hz of f_lo.

## 6. Stop rules

1. No v3.0 code is written before this protocol is committed and pushed.
2. No held-out signal is generated before the v3.0 tag exists.
3. Nothing in sections 2-5 changes after the step that uses it has started.
4. Each reportable run is done once. A crash or code defect may be fixed once, only if it can be identified without looking at outcomes, and is logged.
5. A gate or criterion failure stops the phase, with a report and no workaround.
6. Every result is reported, whatever its direction.

## 7. Outputs

`C:\Users\nghare\.brainstorm\process\revision_checks\v3_aperiodic\`:
- `RESULTS_v3.md` (gates, freeze commit, all tables, criteria decisions, deviations);
- per-trial CSVs;
- `provenance.json`;
- figures as 300-dpi PNG and SVG, with no titles or footers inside the image:
  - HA recovery by cell for v1.0, v3.0, SP-raw and the best scan;
  - ECoG rest fP against spectral peak for v1.0 and v3.0, if Phase C runs.

## Amendment 1 (2026-10-23): residual for peak detection, raw spectrum for peak location

**Reason.** Gate G1 failed. On the canonical burst-coupled input, v3 returned fP = 8.690 Hz (fA 121 Hz). The BTA log-power maximum lies at 7.996 Hz and the residual maximum at 8.698 Hz (revision_checks/v3_aperiodic/G1_curve.csv). The BTA spectrum of the 1.2-s epoch has a broad peak. Subtracting a sloped aperiodic fit tilts it and moves its maximum upward; here the "aperiodic" slope is fitted mostly to the peak's skirt, because the canonical signal has a white-noise background. The residual is suited to deciding which peak is real, but not to locating it. G2 and G3 were not run, and no held-out signal exists. This amendment is made on development signals only. The failed attempt is kept and reported.

**Change to section 2, Step 2 (items 4-5).** Candidate detection is unchanged (strict interior local maxima of r with r >= 2 x sigma). The selected candidate i is the one with the largest r. Its location is then found as follows:
1. **Peak region:** the contiguous admissible bins around i with r > 0.
2. **Hill climb:** starting at i, move one bin at a time toward the neighbour with higher log10 P, staying inside the region, until a strict local maximum of log10 P is reached.
   - If one is reached, fP = that bin, refined by three-point parabolic interpolation of log10 P (exactly the v1.0 refinement rule).
   - If the climb reaches the region boundary without a strict local maximum (the peak is only a shoulder on the aperiodic slope), fP = bin i, refined by parabolic interpolation of r.
3. Record which branch was used (`"raw_local_max"` or `"residual_shoulder"`) in the diagnostics.

SP-raw uses the same amended rule on the raw-signal spectrum. Everything else is unchanged: f_lo = max(minPhaseHz, 7/T), the two-pass fit, sigma, the 2 x sigma threshold, status 3, gates G0-G3 with their pass criteria, Phases B-C and criteria A1-A4.

**Procedure.**
- Gates G0-G3 are rerun from the start with the amended rule.
- `src/bst_apc.m` must keep its original line endings, so that `git diff v1.0 -- src/bst_apc.m` shows only the v3 additions and the version switch without whitespace-ignoring options.
