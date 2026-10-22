# APC v1.0 frozen revision protocol

This protocol is selected before observing any v1.0 benchmark outcomes.
Implementation is committed with a clean tree before the compatibility
checks and five-trial v1 smoke test. All three checks must pass on that
commit before it receives the v1.0 tag. A failed
method-relevant check or execution exception stops the workflow. Pure
tooling errors may be fixed and resumed, with deviations recorded. A method's
documented no-estimate status is recorded as a recovery failure, rather than
silently removing that trial. Source changes after tagging are prohibited.

## Method

- Default amplitude range [80,150] Hz; direct candidates every 1 Hz.
- v1 candidate and final half-width = recovered fP, to include the specified
  fA +/- fP sidebands, including recovered fP below 2 Hz;
  bands clipped to the amplitude range and below Nyquist. Fallback selection
  retains the preserved TF rule, with final half-width also equal to fP.
- fPRefine=true zero-pads the preserved demeaned burst-average Welch spectrum
  to power-of-two NFFT >= fs/0.05 and >= original NFFT. Three adjacent log
  powers define a parabola; interpolate an interior concave peak with its
  offset limited to half a bin. Retain the preserved search limits 1–30 Hz
  (and the original high-frequency/phase separation bound). No October 20
  detrending or three-cycle phase bound is applied.
- fPRefine=false retains the original Welch-bin estimate exactly.
- oct2026 retains the preserved 1 Hz grid, 4 Hz candidate/final width and
  fallback. june2026_clipped uses the June 4 Hz grid (appending 150), ±6 Hz
  candidate filters and June fallback; final ±6 Hz band clips to [80,150].
- Legacy filters retain designfilt/filtfilt and cache immutable objects by
  exact band edges. The continuously varying v1 carrier filters directly
  construct the same fourth-order Butterworth family via butter(2),
  zp2sos and filtfilt. Phase filtering and all other stages are preserved.
- The second bst_apc output records the full normalized option struct and
  route per signal: direct_envelope_scan, tf_fallback, or not_reached.
  It also records candidate and final half-widths and clipped final edges.
  The v1 mode ignores amplitudeBandWidthHz; a smoke test explicitly changes
  that option from 4 to 40 Hz while requiring identical numerical results.

## Paired simulation design

Original generator formulas, seed 20260618, original full-profile level/trial
order, and 25 repeats per level. Capture components without additional RNG
draws. The distractor generator also consumes its original unused null-trial
draws to retain the original coupled inputs. APC and comparator analysis do
not consume simulation RNG state.

Main APC configurations: v1.0; oct2026 with refinement false;
june2026_clipped with refinement false; v1.0 with refinement false.
Comparators A0 (half-width 6) and A1 (half-width candidate fP) use original
phase half-width 1.5, fP grid 4:1:12, fA grid 80:8:152, original butter(4)
bandpass/filtfilt, raw MVL, KL-MI and GLM R². Additionally report conventional
Ozkurt MVL = |sum(A exp(i phi))|/sqrt(N sum(A²)), with no extra 1/sqrt(N).
The existing calc_MI_all_methods Ozkurt helper is not changed or used here.
Raw and normalized MVL independently maximize their own score maps; ties
use MATLAB's column-major first maximum. No surrogate normalization.

Random-fP check resets the simulation seed separately for each benchmark.
An independent mt19937ar stream with seed 20260618 supplies one Uniform[5,11]
draw per trial, shared by all methods. Keep levels [.15,.5,1], distractor
levels [0,1.5,3], 25 repeats. APC v1.0 with/without refinement and A0/A1
comparators on both 1 Hz and 0.5 Hz phase grids.

Primary timing null: keep coupling_level=.60, high amplitude and Gaussian
sigma. Replace only the true 120 Hz burst component with Poisson-timed
bursts, rate fP for distractor and keep_rate*fP for sparsity. Generate
exponential inter-arrival times using a separate mt19937ar stream seeded
20260618, reset per benchmark. Use the original event support
[t(1)-1/fP,t(end)+1/fP] and unchanged APC epoch-edge exclusions. The expected
number of events in the recording is rate*duration (the last sampled time
is one sample earlier than duration). Gaussian sums permit overlaps; no
minimum gap is imposed. Normalize envelope maxima as in the coupled
generator. Retain the paired carrier, distractor, background and original
noise samples/scale. Verify their exact equality and verify coupled-null
equals the removed-minus-added true component within 1e-12.

Secondary no-coupled-burst control: remove the paired true component
(coupling_level=0), with every other component and noise unchanged.
Run primary APC and A1 comparators on both controls at every main level.
AUC uses all 25x25 coupled/null score pairs, one half for ties, and the
original larger-score direction. Report finite-score sample counts.

## Reporting and provenance

Recovery is inclusive: |fP−truth| <=1 Hz and |fA−truth| <=8 Hz. Also report
joint recovery with phase tolerance .5 Hz. fA-only and fP-only are marginal
criteria, not mutually exclusive categories. Boundary counts use fP=4 or
12 Hz within 1e-9; APC itself searches the documented 1–30 Hz limits.
Mean/median absolute errors use finite estimates, with invalid counts.
Every CSV row contains commit, MATLAB version, complete APC option inputs,
complete comparator settings, generator cfg and seed. Every MAT/JSON has
full metadata; figures embed provenance. The preserved earlier sanity records
identify their parent commit and dirty tree. New pre-tag checks identify
the exact committed source, clean working tree and tested source blob;
the final freeze attestation links the committed checks to the tagged commit.
Committed checks are stored separately from the preserved earlier sanity
records. Python text I/O uses explicit UTF-8; MATLAB sources are ASCII.
All result artifacts go outside the repository to revision_checks/v1_rerun.
