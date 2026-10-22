# Held-out execution bookkeeping, fixed before data generation

The method is the tested candidate-3 source. This file supplies execution
details for Parts 3-5 without changing their suite or decision thresholds.
PROTOCOL_v2.md retains the original C1-C4 text verbatim.

Seed 20261022, mrg32k3a: substream 1 generates signals; substream 2 supplies
frequency/independent sinusoid-phase draws; substream 3 supplies Poisson
events; each analyzed input has event-surrogate substream 1000+input_id.
All seeds, substreams, draw order and full generator/method settings are
stored. Analysis does not consume the signal stream. Generators retain
their original formulas and unused legacy draws. No data are generated
until the tested source is committed and tagged v2.0.

Order: H1-sparsity levels [1,.55,.25,.15], H1-distractor [0,1.5,3],
H2 ratios [0,.5,1,1.5,2,3], H4 continuous; 25 repeats per level. H1/H4 draw
fP then fA from U(5,11) and U(90,140). H2 draws fP from U(4,7), fD from
U(fP+3,13), a uniform independent 10-like-sinusoid phase, then fA U(90,140).
The actual H2 distractor frequency is its fD draw, not a fixed 10 Hz.
All methods receive the identical saved input and truth is used only for
generation and scoring, never to select a method frequency.

H1 uses frozen v1 generator profiles, including phase_offset_deg=-90 and
sparsity background scale .18. H1-distractor frequency is true fA-24,
including its original baseline carrier even at scale zero. H2 uses the
previous slow-distractor generator formula (physical trough centers,
phase_offset_deg=180), no high-frequency distractor or its baseline, and
an independently phased slow sine at fD and the requested amplitude ratio.
Sampling is 500 Hz; burst sigma .028 s, timing jitter .010 s, coupling .60,
mixed frequency-domain 1/f pink + .5 white noise at -3 dB, as prescribed.

H4 inherits the sinusoidal continuous-PAC clean condition from
run_apc_continuous_pac_boundary_benchmark.m: 12 s; unit-SD low sinusoid;
high signal 1.25*(1+.70*cos(phase-pi/2))*sin(2*pi*fA*t+.2). Its fP/fA are
random as above. The suite-wide -3 dB mixed-noise formula is used. This
boundary has no Gaussian burst-strength parameter. No H4 null is requested.

Every H1 level and H2 ratios [0,1,3] get a paired timing null. Poisson
rate is keep_rate*fP for sparsity and fP otherwise. Use the inherited
event support [t(1)-1/fP,t(end)+1/fP], Gaussian envelope sum and maximum
normalization. Overlaps are allowed. Replace only the true-burst component,
retaining exact carrier/background/distractor/noise samples and scale.
Verify coupled-minus-null equals removed-minus-added true component to
1e-12. No-coupled-burst controls at H1 keep rates [1,.15] and distractor
scale 3 remove only the true-burst component (coupling_level=0 in metadata).
The suite has 350 coupled inputs, 250 timing nulls and 75 secondary controls.

APC v2 and v1 use amplitude search [80,160] and their unchanged phase
limits. v1 is the selectable frozen v1 path. Comparator scans use the
inherited butter(4) bandpass/filtfilt, phase half-width 1.5, grids
3:.5:14 and 80:4:160, A2-prime half-width 14 and A1-prime half-width fP.
Each raw/Ozkurt/KLMI/GLM metric independently maximizes its complete grid;
KLMI uses 18 bins; Ozkurt=raw_MVL/sqrt(mean(A.^2)); GLM is the inherited
R-squared. Ties retain MATLAB's first column-major maximum.

Optional tPAC: inspect process_tpac on the configured local MATLAB path and
the configured Brainstorm installation. Include only if its existing
headless interface can execute unchanged with defaults and the same ranges;
otherwise record the exact availability reason and skip.

Recovery uses inclusive phase 1 Hz and amplitude 8 Hz; strict phase .5 Hz.
Invalid outputs are recovery failures; errors use finite estimates, with
valid/finite counts. AUC uses all finite coupled/null score pairs with
half credit for ties, without changing score direction; report denominators.
Event p<.05 rates use all 25 trials, with the finite-p count also shown.

"Best A2-prime" is selected per level, independently for each criterion's
endpoint, in the comparator's favor. Maximize joint for C1/C4; maximize
strict joint for C2; minimize false joint for C3 null specificity. Ties use
the fixed metric order [MVL-raw,MVL-Ozkurt,KLMI,GLM]. No method parameter
is selected or tuned. Record the chosen metric and count for every level.
C2 uses paired successes and a one-sided exact binomial McNemar test on
discordant pairs. C3 compares false-joint rates over all 250 timing-null
inputs (5 per 100 means a .05 rate allowance); its event-z AUC thresholds
apply to the five prescribed H1 levels. A nonfinite required AUC fails.
No other threshold, pooling rule or C1-C4 wording is changed.

All inputs are saved once before parallel analysis. Three one-thread MATLAB
workers analyze disjoint input_id residue classes; scheduling does not
affect the streams, saved input order or independent per-input surrogate RNG.
Checkpoint every 25 analyzed inputs. Stop on method-relevant execution or
verification failure. Document and resume purely tooling errors.
