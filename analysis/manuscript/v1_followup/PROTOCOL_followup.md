# Analysis protocol, selected before follow-up outcomes

Frozen APC source: v1.0, 71ebc16aed32ca38be73a800738b975e5806b330.
All additions are analysis scripts outside the tagged repository.

1. A2 uses a fixed 12-Hz amplitude half-width, both 1-Hz and 0.5-Hz phase
grids, and otherwise the exact frozen comparator definitions. Reuse every
saved main, random-fP, timing-null and no-coupled-burst input. A1 arithmetic
in the analysis copy must exactly reproduce the frozen comparator on a
saved input, on both grids, before the new scans begin.
2. Instrument an external copy of APC with diagnostics only; require all
exported results to equal frozen APC on every selected status-4 input.
Record both refined and unrefined intermediate frequency, band, pre/post
edge counts, FFT bins and exact original source return condition. Test the
refined frequency against its own padded peak neighbors, unpadded peak
neighbors, and the configured phase limits. Do not change any method.
3. Slow-rhythm scenario derives from the frozen distractor generator: 6-Hz
sinusoid, 120-Hz Gaussian bursts, coupling 0.60, original 10-ms burst-time
jitter, Gaussian sigma 28 ms, original carrier/noise formulas and -3 dB SNR.
Set phase_offset_deg=180 so the generator's formula places burst centers
at troughs of sin(2*pi*6*t), before the original jitter. Add an uncoupled
10-Hz sinusoid with a trial-wise uniform phase from a separate mt19937ar
stream seeded 20260618. Its amplitude is ratio*low_amp. Ratios, in order:
[0,0.5,1,1.5,2,3], 25 repeats each. Reset the original simulation RNG to
20260618; preserve its draw order, including unused legacy null draws.
Explicitly omit the entire 96-Hz component, including its baseline.
Noise uses the original mixed-noise recipe and the power of the new clean
signal. Save generated inputs and components once for all methods.
4. Slow timing null at ratios [0,1,3] replaces only the true-burst component
with Poisson-timed Gaussian bursts, rate 6 Hz, separate mt19937ar stream
seeded 20260618, original support [t(1)-1/6,t(end)+1/6]. Overlaps allowed,
no minimum gap. Keep the coupled noise vector and scale unchanged; verify
the paired subtraction within 1e-12. All APC edge rejection stays unchanged.
5. Slow methods: frozen APC default and flipTroughs=false; A1 and A2, four
metrics, both phase grids. Original method no-estimate statuses count as
recovery failures. They are not execution failures or grounds to retune.
Recovery: |fP-true|<=1, |fA-120|<=8; strict joint uses phase tolerance 0.5.
About-10 picks: |fP-10|<=1. Errors use finite estimates, with counts shown.
AUC is all finite coupled/null score pairs (greater + half ties), without
reversing score direction; report valid denominators. No normalization.
6. Every output carries frozen commit, MATLAB version, full APC/comparator
options and seed, directly or in its embedded metadata. Hash all input MAT
banks and source/analysis scripts. Preserve previous outputs. Stop on
method-relevant failure; record and resume pure tooling fixes.
