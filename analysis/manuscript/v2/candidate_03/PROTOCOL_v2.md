GOAL: Implement APC v2 to a fixed specification, freeze it, then evaluate it on a NEW held-out simulation suite against fair comparators, using decision criteria written before any held-out result exists.

RULES
- New branch "v2-revision" from tag v1.0 in apc-brainstorm-publish. Never rewrite earlier commits, tags or saved results. New outputs go to revision_checks/v2/.
- Write revision_checks/v2/PROTOCOL_v2.md (this spec, including the decision criteria verbatim) and commit it WITH the v2 code BEFORE generating any held-out data.
- No parameter tuning. You may fix implementation bugs found by the unit tests before tagging; list every one. After tagging, nothing in the method changes.
- Provenance (commit, MATLAB version, full options, seeds) goes in every output. Tooling errors may be fixed and resumed (log them as deviations); stop on anything method-relevant.

PART 1 — v2 SPECIFICATION (new mode in bst_apc.m: version='v2'; v1 behaviour stays selectable and unchanged)
Step 1 (bursts): unchanged from v1.0 (RMS CWT burst trace over the amplitude search range, 20-ms smoothing, prominence 0.75 SD, minimum spacing as in v1.0). Record the burst times t_k and the burst count.
Step 2 (fP by burst-phase locking):
  - Candidate grid f = fmin:0.1:fmax, where fmin = max(minPhaseHz, 10/record_duration_s), fmax = min(maxPhaseHz, ampRange(1)/2, fs/3). Defaults minPhaseHz=1, maxPhaseHz=30.
  - For each f: zero-phase 4th-order Butterworth bandpass of x(t) with half-width max(0.5, 0.25*f); phase from the Hilbert transform; exclude bursts within 1/f of the record edges; compute pairwise phase consistency PPC(f) (Vinck et al. 2010) over the burst phases.
  - fP = the grid argmax of PPC, refined by 3-point parabolic interpolation when both neighbours are on the grid.
  - Status 3 if there are fewer than 10 usable bursts or no finite PPC.
Step 3 (diagnostics only): v1.0 burst-triggered average and trough-locked profiling at the v2 fP. Their failure must NOT stop the analysis: return a warning flag and continue. The polarity flip is used only for this display.
Step 4 (fA): candidate fA = ampRange(1):1:ampRange(2). For each, a band of half-width fP (clipped to ampRange and Nyquist), zero-phase 4th-order Butterworth, Hilbert envelope; score = raw Canolty MVL between the fP phase (Step 2 filter) and that envelope. Smooth the score with a 3-point moving mean; fA = argmax. C_APC = raw MVL at (fP, fA); also report Ozkurt-normalized MVL.
Event coupling test (new output): PPC at fP versus 200 surrogates in which every burst time is independently jittered by uniform +/- 1/fP seconds (bursts kept inside the record). Report z = (PPC - mean_surr)/sd_surr and an empirical p = (1 + #surr >= obs)/(201). Seed the surrogate RNG separately and record it.
Outputs: fP, fA, C_APC, Ozkurt MVL, event PPC, z, p, burst count, diagnostic flags, status.

PART 2 — UNIT TESTS (before tagging)
(a) A pure 8-Hz carrier with 120-Hz bursts locked to the trough, high SNR: v2 returns fP within 0.1 Hz of 8 and fA within 4 Hz of 120.
(b) The same with an added uncoupled 11-Hz sinusoid at 3x amplitude: v2 fP within 0.5 Hz of 8.
(c) Poisson burst times: event-test p > 0.05 in at least 8 of 10 seeds.
(d) Run v2 on 25 trials of the existing distractor benchmark (seed 20260618) to check it runs. Report the results but do not tune on them.
If (a)–(c) pass: commit and tag "v2.0", and record the hash. If they fail: report and stop.

PART 3 — HELD-OUT SUITE (new seed 20261022; separate RNG streams for signals, frequencies, Poisson nulls and surrogates)
Use the existing generator formulas (Gaussian bursts sigma 28 ms, jitter 10 ms, coupling 0.60, mixed pink+white noise at -3 dB, fs 500 Hz).
H1 random-pair: per trial, fP ~ U(5,11), fA ~ U(90,140).
  H1-sparsity: 8 s, keep rates {1, 0.55, 0.25, 0.15}, background bursts as in v1.0.
  H1-distractor: 6 s, uncoupled distractor burst band at fA - 24 Hz, scales {0, 1.5, 3}.
H2 slow distractor: 6 s, coupled fP ~ U(4,7), uncoupled sinusoid at fD ~ U(fP+3, 13) with a random phase, amplitude ratios {0, 0.5, 1, 1.5, 2, 3}, fA ~ U(90,140).
H3 nulls: a paired timing null (Poisson burst times at the matched mean rate, everything else identical) for every H1 level and for H2 ratios {0, 1, 3}; a no-coupled-burst control for H1 keep rates {1, 0.15} and H1 distractor scale 3.
H4 continuous-PAC boundary: 25 trials, random fP/fA, continuous amplitude modulation (as in the v1 canonical condition).
25 repeats per level throughout.

PART 4 — METHODS ON THE HELD-OUT SUITE
- APC v2.0 (primary).
- APC v1.0 (reference).
- Comparators: MVL-raw, MVL-Ozkurt, KLMI and GLM scans. Phase grid 3:0.5:14 Hz, phase half-width 1.5 Hz, amplitude grid 80:4:160 Hz, amplitude half-width fixed at 14 Hz (= 2*max fP rule) — call this A2'. Also run the comparators with half-width = candidate fP (A1').
- Amplitude search range for APC: [80, 160].
- If Brainstorm's tPAC can run headless from the local Brainstorm install without code changes, add it with its defaults and the same ranges; otherwise skip it and say so.
Tolerances: joint = |fP err| <= 1 Hz and |fA err| <= 8 Hz; strict joint uses |fP err| <= 0.5 Hz. Invalid outputs count as failures.

PART 5 — DECISION CRITERIA (evaluate on held-out data only; "best A2'" = the best A2' metric chosen per level, which favours the comparators)
C1 (core claim): H2 pooled over ratios {1, 1.5, 2, 3} (100 trials): v2 joint recovery >= best A2' minus 5, AND v2 picks within 1 Hz of fD in <= 10/100.
C2 (precision): H1 pooled (175 trials): v2 strict-joint recovery > best A2' strict-joint, one-sided exact McNemar p < 0.05.
C3 (specificity): pooled timing-null false joint recovery for v2 <= best A2' + 5 per 100 trials; AUC of the v2 event z (coupled vs paired timing null) >= 0.90 at H1 keep rates {1, 0.55} and all H1 distractor scales.
C4 (recovery): H1 pooled joint recovery for v2 >= best A2' minus 9 (5% of 175).
Report PASS/FAIL for each criterion with the numbers. Do not interpret.

OUTPUT
revision_checks/v2/RESULTS_v2.md plus CSVs. Include:
1. Unit-test results and the tag hash.
2. Per scenario/level/method tables: joint / fA / fP / strict joint, error mean and median, picks near fD (H2), valid count.
3. Null false recovery and AUCs (C_APC, Ozkurt MVL and event z for v2; scores for the comparators).
4. The event-test p < 0.05 rate in coupled and in null trials.
5. The C1–C4 table.
6. A factual summary of at most 10 lines, runtime and deviations.
Also save joint-recovery figures for H1 and H2.

IMPLEMENTATION DETAILS FIXED BEFORE UNIT OR HELD-OUT OUTCOMES

- Requested output protocol is mirrored byte-for-byte in the tracked
  analysis/v2_revision/PROTOCOL_v2.md because revision_checks/v2 is outside
  the Git repository. Commit both code and the tracked protocol together.
- version='v2' dispatches to the new algorithm. Absent version, version='v1'
  and version='v1.0' retain all existing v1 calculations and outputs.
- Fourth-order Butterworth means fourth-order bandpass in total, implemented
  by butter(2, [low high]/Nyquist), zp2sos and filtfilt, as in v1's amplitude
  filter family. Step 1 calls the unchanged v1 helper functions directly.
- Record duration is N/fs. Event edge guards use first/last sampled times.
  The literal candidate grid is fmin:0.1:fmax, without appending an endpoint.
  A candidate needs >=10 edge-usable burst events; otherwise its PPC is NaN.
  PPC=(abs(sum(exp(1i*phase)))^2-N)/(N*(N-1)), without clipping negative values.
  Reference: Vinck et al. 2010, equations 14-15,
  https://doi.org/10.1016/j.neuroimage.2010.01.073 .
- Refine an interior concave peak with a parabola through the three raw PPC
  values; finite neighbors required, offset bounded to half a grid interval.
  Refilter and reapply event guards at the final refined fP. Status 3 if fewer
  than ten events remain. Step 4 and event tests use this final phase filter.
- Three-point amplitude-score smoothing uses a centered moving mean with
  shortened endpoint windows. Report raw MVL at the selected fA, not the
  smoothed selection score. Ties choose the first grid point.
- Event-test surrogates jitter each event in the observed fP-usable subset.
  Its 1/fP edge margin guarantees all independent uniform +/-1/fP jitters
  remain in the record; do not impose a second edge guard on surrogates.
  Evaluate continuous jitter times by linear interpolation of unwrapped
  Hilbert phase. Use sample SD (N-1); zero SD yields z=NaN and warning bit 16.
  Always 200 surrogates. RNG is a local mrg32k3a stream with recorded seed
  and substream; it must not change the simulation/global RNG state.
- Diagnostic warning bits: 1=no complete burst-average epochs; 2=no troughs;
  4=no complete trough profiling epochs; 8=diagnostic exception;
  16=zero/nonfinite surrogate SD. Diagnostics never choose fP or fA and their
  failure never changes method success status. Record exceptions explicitly.
- Unit (a): six-second 500-Hz signal, 8-Hz sine amplitude 1, 120-Hz carrier,
  base carrier amplitude .08, Gaussian bursts sigma .028 s, amplitude
  1.3*.60, original .010-s jitter centered on physical troughs, 20-dB mixed
  pink/white noise. Use original distractor-generator formulas, omitting the
  entire 96-Hz component. Seed 20260618; amplitude range [80,160].
- Unit (b): the exact same signal/noise as (a), plus 3*sin(2*pi*11*t+phi),
  phi uniform from a separate mrg32k3a stream, seed 20260619, substream 1.
- Unit (c): ten seeds 20260618:20260627, same unit profile. Replace only the
  true-burst component with homogeneous Poisson events at 8 Hz, original
  extended support, overlaps allowed, original envelope normalization and
  paired noise. A separate mrg32k3a stream (seed=trial seed, substream=3)
  supplies Poisson draws; surrogate seed=trial seed+1, substream=2.
- Unit (d): first 25 saved coupled distractor trials (level 0) in the original
  seed-20260618 trial order. Check runs, report all statuses and recovery;
  never use them to alter the method.
- Run gates sequentially. On any performance gate failure, save the completed
  test rows and STOP: no remaining tests, v2.0 tag or held-out generation.
  An identifiable implementation bug may be corrected before tagging, with
  every correction logged; no parameter or unit-signal retuning is allowed.
- Before performance gates, verify unchanged v1 outputs against a renamed
  copy from tag v1.0 on five saved inputs, and verify PPC against explicit
  pairwise cosines, burst detection identity and no global RNG consumption.
- Held-out streams will be mrg32k3a with seed 20261022 and distinct substreams
  for signals, frequencies, Poisson events and event-test surrogates. Record
  the full stream/substream map before any held-out data are generated.
- If gates pass, build and commit the held-out execution scripts and full
  comparator/decision bookkeeping before tagging and generating any data.
  Additional bookkeeping choices must not alter the fixed method or criteria.

## Candidate history

Candidate 1 (commit 7848af05ada722971769da856e970d0737820169) failed unit
gate (a): fP=10.631999875603938 Hz, fA=120 Hz. The user identified that PPC
is flat across filter centers whose passband contains the coupled rhythm;
the recorded curve is unit_attempt_01/unit_a_ppc_curve.csv. The five v1
compatibility cases and implementation invariants passed. No v2.0 tag or
held-out data were created. Candidate-1 protocol/report/manifest copies are
preserved in revision_checks/v2/candidate_01 and its unit records are unchanged.

Candidate 2 is the final candidate authorized by the user. The following
amendment replaces only Step 2, the event test, and the additional ordered
unit gate (a2). All earlier Step-2/PPC-event implementation notes above are
historical candidate-1 notes and are superseded by this amendment. All other
method settings, generators, unit profiles/seeds, held-out suite and C1-C4
remain exactly as committed in 7848af0. No further candidates will be made.

### Candidate 2: Step 2 replacement (burst-locked power)

- L=2 seconds. Usable burst centers have the complete half-open window
  [t_k-L/2,t_k+L/2) in the half-open record [t0,t0+T). Status 1 for T<4 s;
  status 3 for fewer than ten usable bursts.
- Extract L*fs samples at relative times -L/2:1/fs:L/2-1/fs; demean each
  segment and multiply by a symmetric Hann window of that length.
- Evaluate X_k(f)=sum_t w(t)*s_k(t)*exp(-i*2*pi*f*t) directly, on the grid
  fmin:0.05:fmax, fmin=max(minPhaseHz,10/T,3/L), fmax as originally specified.
- BLP(f)=(abs(sum_k X_k(f))^2-sum_k abs(X_k(f))^2)/(N*(N-1)). Select its
  grid maximum; refine with a three-point parabola on raw BLP when both
  neighbors are finite and on the grid. Use the inherited half-bin bound.
- PPC of the X_k phases is diagnostic only, on the entire grid and at the
  refined fP. No polarity flip is applied anywhere in Step 2.
- The phase reference for Steps 3-4 remains the original fourth-order
  zero-phase Butterworth at fP, half-width=max(0.5,0.25*fP).

### Candidate 2: event test replacement

- Primary statistic: maximum BLP on the full candidate grid. For each of
  200 surrogates, independently jitter each usable burst by uniform
  +/-1/fP seconds, conditioned on remaining within the window-usable center
  range. Implement this conditional uniform draw using its truncated interval
  per burst, which is equivalent to rejecting out-of-range uniform jitters.
- Recompute BLP on the entire grid for each surrogate and use its maximum.
  z=(observed maximum-mean surrogate maxima)/sample SD; empirical
  p=(1+number of surrogate maxima >= observed maximum)/201.
- Secondary uncorrected statistic: BLP at the refined observed fP, evaluated
  at that same fixed frequency in each surrogate. Report separate z and p.
- Jitter times are continuous. Segment samples use linear interpolation of
  x at those centers. Demeaning, Hann multiplication and direct Fourier
  evaluation are linear: batch the direct coefficient computation at unique
  bracketing sample centers and interpolate coefficients. Validate against
  independently extracted/interpolated segments and direct sums. No FFT-bin
  approximation or frequency interpolation is used.
- Record the local RNG seed/substream and both 200-element surrogate
  statistic vectors. No change to signal RNG state is permitted.

### Candidate 2: ordered unit gates and freeze

1. (a) unchanged high-SNR 8/120-Hz trial and seed 20260618; phase tolerance
   0.1 Hz, amplitude tolerance 4 Hz.
2. (a2) the same unit generator, each initialized with the same original
   seed 20260618, at fP in [5.3,6.7,9.4,10.8] Hz, in that order. All four
   require absolute fP error <=0.1 Hz. All other unit parameters are unchanged.
3. (b), (c), (d) unchanged, in that order.

Save BLP and PPC curves for every completed unit trial, including null and
existing-benchmark trials. Stop at the first failed gate; no further
candidates. Test candidate-2 working sources before committing; record the
candidate-1 base commit plus exact working-source/protocol/script hashes.
Only if all gates pass, commit candidate 2 with its protocol and execution
scripts, verify the tested source hashes, tag v2.0, then generate and run the
original held-out suite at seed 20261022. In the held-out event test, the
primary statistic and z/p are now the max-BLP statistics above. C1-C4 are
unchanged, including every threshold and paired decision calculation.
New candidate-2 outputs are under revision_checks/v2/candidate_02; candidate-1
saved results remain unchanged.

### Candidate history: candidate 2 and final candidate 3

Candidate 2 failed gate (a) only on fA: fP=7.9996901239320914 Hz passed;
fA=115 Hz had error 5 Hz, exceeding the allowed 4 Hz. The user's diagnosis
is that the Step-4 score versus center frequency is bimodal, with peaks near
fA +/- fP and a dip at fA, because a flat-top Butterworth band of half-width
fP puts the modulation sidebands at its edges. The candidate-2 source and
its unit report/curves remain preserved in revision_checks/v2/candidate_02.

The user has now authorized candidate 3 as the final candidate. This later
authorization supersedes the candidate-2 instruction that no further
candidate would be made. Only Step 4 and the specified a2 pairs change.
Candidate-2 Step 2 (BLP), both event-test statistics, Steps 1/3, the unit
profiles/seeds, the held-out suite and C1-C4 remain unchanged. No further
candidate is authorized after candidate 3.

### Candidate 3: Step 4 replacement (peaked kernel)

- Candidate centers fc are the unchanged 1-Hz grid within ampRange.
- Reflect x for one second at each end. The precise reflection convention
  excludes a repeated endpoint: x(p+1:-1:2), x, x(end-1:-1:end-p), p=round(fs).
- FFT the padded signal at its actual length. On the signed-frequency grid,
  multiply by G(f)=2*exp(-(f-fc)^2/(2*sigma^2)) for f>0 and zero for f<=0,
  sigma=1.5*fP; inverse FFT and crop exactly p samples at each end. The
  positive Nyquist bin, when present, follows the literal positive-frequency
  formula. Do not clip the Gaussian tails to ampRange.
- Envelope=absolute analytic band signal; score=raw Canolty MVL with the
  unchanged fP phase reference. No moving-mean smoothing.
- Select the grid maximum and refine with a three-point parabola on raw
  score when both neighbors are inside ampRange and the maximum is concave.
  Retain the inherited half-bin bound and first-grid-point tie handling.
- Recompute the Gaussian envelope at the refined fA. Report raw C_APC and
  conventional Ozkurt MVL from that same envelope. Gaussian sigma is output
  explicitly; obsolete finite rectangular-band-width fields are NaN.
- Save the raw fA score curve for every completed unit trial, alongside its
  BLP and PPC curves. If Step 4 was not reached, save the prescribed center
  grid with NaN scores and an explicit step4_reached=false flag.

### Candidate 3: unit gates and conditional freeze

Run the same sequential stopping rule: (a), (a2), (b), (c), (d).
(a) remains |fP-8|<=0.1 Hz and |fA-120|<=4 Hz.
(a2) now uses the four true pairs in order: (5.3,95), (6.7,108), (9.4,131),
(10.8,142), each with the same unchanged generator and seed scheme; both
|fP error|<=0.1 Hz and |fA error|<=4 Hz are required for every trial.
(b), (c), (d) remain exactly as specified for candidate 2.

Before the performance gates, retain the inherited mathematical/compatibility
checks and verify Step-2 and event outputs match the saved candidate-2 unit
(a) exactly on its unchanged signal. Validate the Gaussian envelope/score
against the literal FFT formula. These checks do not change any method.

Only if all gates pass, commit candidate 3 with its protocol and execution
scripts, verify tested source hashes, tag v2.0, then generate/run the original
held-out suite and unchanged comparators/criteria at seed 20261022. On any
gate failure, stop and report; no further candidates. Candidate-3 outputs
are kept separately under revision_checks/v2/candidate_03. Earlier saved
candidate reports, curves, inputs and source snapshots are not overwritten.
