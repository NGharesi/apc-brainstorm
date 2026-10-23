# Execution details fixed before new-session channel or bout analysis

PROTOCOL_rodent.md preserves the user's plan verbatim. Its SHA-256 was recorded
before the read-only duration inventory. The historical ec013.157 reproduction
gate passed exactly on the original sample interval, including the complete
speed vector, both masks and both 12-bout tables.

Welch channel selection uses the whole recording, no state-dependent selection,
all imported channels, each channel demeaned, a symmetric Hann window of
round(4*fs) samples, 50% overlap and NFFT=2^nextpow2(window length). Integrate
the one-sided PSD on [6,10] and [1,4] Hz, with linearly interpolated exact band
endpoints and trapezoidal integration. Choose the first channel index attaining
the largest finite ratio with positive delta power. Record every channel's
powers and ratio. Invalid/undefined ratios are recorded, not imputed. Channel
flags are recorded but do not add an unrequested exclusion criterion.

The ec013.157 full multichannel source is recovered from the local
behavior_inter.mat variable test, without modifying any input. Its full E1
and Time match R2 exactly and its 65-channel sample interval 40800:372501
matches the saved multichannel crop exactly. The source hash and evidence
are recorded separately.

The user resolved the interval: whole recordings, with the appended missing-
tracking, fixed-length chunking and ec013.157 validation rules in the protocol.

Historical speed is d(trenddecomp(interpolated x1))/dt; its producer uses
39.06 Hz LED timestamps, x1 only, threshold abs(speed)>6 and a 5-s minimum.
The producer has a movmedian fallback only if trenddecomp throws. There is
no -1 sentinel removal, LED averaging, 2-D distance or coordinate calibration
in the historical computation. These limitations will be explicit. The
original axis label is cm; computational units are raw x1 units per second.

Primary session eligibility is >=5 run and >=5 rest bouts, independent of
channel or PAC outcome. The E1 sensitivity uses the same bout definitions.
If the selected EC013 channel is E1, reuse estimates under both labels rather
than recomputing. Invalid APC statuses are retained as method outputs with
counts; implementation errors, guard failures and failure of requested gates
stop execution. Finite-value denominators are reported for all statistics.

Per-session tests use run-minus-rest, unequal-variance Welch t, pooled-SD
Hedges g with exact gamma correction, and 10,000 percentile bootstrap
resamples, seed 20261022 with deterministic per-session streams. Resample
bouts independently within each state, sharing indices across methods.
Across-session tests use one-sample two-sided t and exact/appropriate
two-sided Wilcoxon signed rank, with zero differences explicitly reported.
No multiplicity correction. Primary selection and E1 sensitivity are separate.

Mixed models are REML: outcome ~ state_run + animal + (1 + state_run | session),
state_run=0 rest/1 run; animal fixed categorical, EC012 reference. Fit primary
APC fP and Ozkurt MVL. Report fit warnings, convergence and covariance estimates.
Do not replace the specified model after seeing the fit.

Within-state spread is SD, IQR and median absolute deviation, per session,
state and method, with valid-bout counts; paired APC-minus-scan spread
comparisons across sessions are descriptive and signed-rank summaries.

The plotted scan is the MVL-Ozkurt scan, i.e. the grid maximum of the same
normalized MVL reported for every method. This choice is fixed independently
of state effects; no scan is selected by run-rest significance. All four
scan methods are included in the tables. Figures explicitly label this as
the Ozkurt-max scan, rather than implying a post-hoc best method.


Chunk execution details fixed before the new ec013.157 validation

Use LFP sample times >= first time + 2 s and <= last time - 2 s. Chunk starts
advance by 331702-round(20*fs); force the final chunk to end at the last retained
sample. A short recording uses its whole trimmed interval. Discard round(10*fs)
speed samples at internal chunk edges. If the forced last chunk overlaps more
than 20 s, assign its remaining overlap at the midpoint of the retained cores;
each derivative sample is taken from exactly one chunk. Save chunk and seam
indices and assert complete, single coverage. No averaging across chunks.

Tracking interpolation retains the historical 39.06 Hz timestamps and x1-only
formula. Replace -1/nonfinite x1 with NaN. A bounded gap with missing sample
count/39.06 <= 0.5 s is linearly interpolated between its two valid neighbours.
Unbounded or longer gaps remain NaN for position interpolation; trenddecomp's
documented local implementation fills its NaNs with the chunk mean internally.
This does not make those times eligible: exclude every derivative touching a
missing position after stitching. Thus no long-gap position is labelled run or
rest. Other LED coordinates are counted for missingness but do not enter speed.

Record raw x1 missing fraction, any-coordinate missing fraction, long gaps,
and invalid LFP derivatives. For each state, bouts lost to gaps are baseline
>=5-s bouts of the same stitched speed trace that retain no >=5-s piece after
gap splitting. Also report intersected baseline bouts and short split pieces.

MATLAB rng(0,'twister') is set once before chunk decomposition; save each chunk's
incoming RNG state. Run chunks sequentially. The historical saved reproduction
is preserved separately and is not replaced by this missing-aware computation.

The validation denominator is every historical derivative sample, global
40800:372500. Missing/unlabelled new samples count as disagreement. Also report
agreement conditional on valid labels. Match historical and whole-recording
bouts one-to-one within state, requiring both endpoints within 0.5 s. The gate
uses all-sample agreement >=95%; no new session bout/PAC analysis before PASS.


DATED EXECUTION AMENDMENT 2026-10-22 — supersedes historical/chunk rules

The revised user plan supersedes the chunked historical-speed gate and the
unrestricted channel selection. Historical 12/12 is an archival check only.
The stated 12% shift sensitivity is the user's supplied rationale; it is not
independently rerun as a new gate. All reported regional results use the new
tracking-rate procedure. Earlier ratios and raw sources remain unchanged.

LED validity requires both coordinates finite and unequal to -1. Combine valid
LED pairs, fill only bounded missing-position runs with missing-count/39.0625
<=0.5 s, then fit PCA to all finite combined/interpolated positions. Fix axis
sign by making its largest-magnitude loading positive. Use linearly interpolated
sample quantiles (0.5%,99.5%). Linear position for state classification is the
projection before Gaussian smoothing, anchored at the 0.5% quantile. Central
70% is the interval [15%,85%] of that robust extent. End zones are below 15%
or above 85%, including the extreme 0.5% tails. Regions are symmetric to PCA sign.

Smooth each finite-position segment independently using a normalized Gaussian
kernel, SD 0.2*39.0625 samples, truncated at ceil(4*SD) samples, reflected segment
boundaries. Do not bridge long gaps. Central differences require both adjacent
tracking samples; segment endpoints are unclassified. Multiply 2-D coordinate
speed by the session's cm-per-unit scale. Speed exactly 6 is unclassified.

Tracking timestamps start at the recording's first LFP timestamp, step 1/39.0625.
Treat tracking samples as half-open bins [t,t+dt); keep bins wholly within the
recording's first/last 2-s trim. Minimum bout duration is samples/39.0625 >=5 s.
Map [bout_start,bout_stop_exclusive) to actual LFP timestamps with searchsorted;
include the first LFP sample >=start and the last <stop_exclusive. Save both
tracking and LFP indices and mapped durations; do not upsample speed.

Reuse existing theta/delta ratios within anatomical channel masks, excluding
auxiliary E33/E65. Choose the first finite maximum. CA1 and EC are separate
analyses; E1 is a separately labelled EC013 sensitivity with identical bouts.
Save complete per-channel region map, metadata source rows and mapping assumption.

Reuse the prespecified statistical definitions and seed 20261022 above. Fit
region-specific REML models. CA1 contains only EC013: animal is constant and
its redundant fixed-effect column is absent, so the estimable model is
outcome ~ state_run + (1 + state_run | session); retain the same session random
intercept/slope. EC uses outcome ~ state_run + animal + (1 + state_run | session).
If a region has only one represented animal after eligibility, explicitly use
the same constant-animal formulation. Record singular fits/convergence warnings;
do not simplify the random-effects structure after seeing outcomes. Nonzero
frozen APC statuses are retained and counted, with finite-value denominators.
The plotted scan remains the preselected MVL-Ozkurt maximum, independently of
run/rest differences; report all four scans. New outputs use regional_* names
so no earlier results or checkpoints are overwritten except the requested report
and current status/manifest files (their stopped versions were archived).
