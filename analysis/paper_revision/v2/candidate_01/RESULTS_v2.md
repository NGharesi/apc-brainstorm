# APC v2 fixed-specification unit-gate report

Branch `v2-revision`, from tag `v1.0` (71ebc16aed32ca38be73a800738b975e5806b330). Candidate commit `7848af05ada722971769da856e970d0737820169`. The method-relevant unit gate failed. The workflow stopped before any held-out data generation; tag `v2.0` was not created.

## Factual summary (8 lines)

1. Candidate implementation and protocol were committed together at 7848af05ada722971769da856e970d0737820169.

2. All five v1 compatibility cases exactly matched the v1.0 reference outputs and runInfo.

3. Independent burst-trace/detection, pairwise-PPC, global-RNG and diagnostic-isolation checks passed.

4. Unit gates: a=FAIL, b=NOT_RUN, c=NOT_RUN, d=NOT_RUN.

5. Completed unit trial rows: 1.

6. First failed gate: a.

7. Held-out simulations, C1-C4 evaluation and H1/H2 figures were not run.

8. v2.0 tag: not created; implementation bug fixes after testing: 0.

## Committed specification and implementation

Requested-path protocol: [PROTOCOL_v2.md](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/PROTOCOL_v2.md>). Identical committed protocol: [PROTOCOL_v2.md](<C:/Users/nghare/.brainstorm/process/apc-brainstorm-publish/analysis/v2_revision/PROTOCOL_v2.md>). The complete user specification, including decision criteria verbatim, appears in both copies. The requested output folder is outside the Git repository, so the repository copy records the protocol in the candidate commit. No held-out results existed before this commit or this gate evaluation.

Source: [bst_apc.m](<C:/Users/nghare/.brainstorm/process/apc-brainstorm-publish/src/bst_apc.m>). Set version="v2" for the new mode. Missing version, version="v1" or version="v1.0" retains the previous calculations. The new path shares the unchanged v1 burst helpers, scans phase filters by event PPC, runs the original averages only as diagnostics, and scans amplitude by smoothed raw MVL. It reports unsmoothed raw MVL, conventional Ozkurt MVL, event PPC/z/p, burst counts/times, diagnostic flags and status.

PPC is (|sum(exp(i*phase))| squared - N)/(N*(N-1)), equivalent to the pairwise cosine average in [Vinck et al. (2010), equations 14-15](https://doi.org/10.1016/j.neuroimage.2010.01.073). The test independently checks that identity. Fourth-order Butterworth means fourth-order total bandpass before forward/reverse application, using the existing v1 SOS filter family. Parabolic interpolation uses raw PPC, not logarithms. The observed-event subset satisfies the 1/fP edge margin; independently jittering each of these events by uniform +/-1/fP keeps them inside the sampled record. The fixed event test uses 200 surrogates from a local, separately seeded mrg32k3a stream.

## Unit-test results

| Gate | Criterion | Result |
| --- | --- | --- |
| a | High-SNR 8/120 Hz; \|fP error\|<=0.1 and \|fA error\|<=4 | FAIL |
| b | Same signal + uncoupled 11-Hz sine at 3x amplitude; \|fP error\|<=0.5 | NOT_RUN |
| c | Poisson bursts: event p>0.05 in at least 8/10 fixed seeds | NOT_RUN |
| d | Run first 25 existing distractor level-0 trials; report without tuning | NOT_RUN |

| Test | Trial | Seed | fP Hz | fA Hz | C_APC | Ozkurt MVL | PPC | Event z | Event p | Bursts | Usable bursts | Diagnostic flags | Status | Pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| a | 1 | 20260618 | 10.63199988 | 120 | 0.1105645 | 0.2025119761 | 0.8152881129 | 17.41038466 | 0.004975124378 | 48 | 46 | 0 | 0 | 0 |

Gate a: recovered fP=10.631999875603938 Hz, |error|=2.6319998756039382 Hz; recovered fA=120 Hz, |error|=0 Hz. Status=0. The gate was evaluated against its precommitted tolerances; no signal, parameter, frequency grid or code was changed after observing it.

Subsequent unit tests were not run because the precommitted sequential stopping rule applies at the first performance-gate failure. The implementation-invariant checks passed; no implementation bug was identified or repaired. No parameter tuning or second unit attempt was performed.

Completed per-trial data: [unit_trials.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/unit_attempt_01/unit_trials.csv>). Full gate record: [unit_results.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/unit_attempt_01/unit_results.json>). Five-case v1 check: [v1_compatibility.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/unit_attempt_01/v1_compatibility.json>). Implementation checks: [implementation_checks.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/unit_attempt_01/implementation_checks.json>).

Unit a full candidate PPC curve: [unit_a_ppc_curve.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/unit_attempt_01/unit_a_ppc_curve.csv>). Saved signal, components, intermediate arrays and surrogate scores: [unit_a.mat](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/unit_attempt_01/unit_a.mat>).

The unit profile was fixed before any result: six seconds, fs=500 Hz, 8-Hz sine amplitude 1, .08 baseline 120-Hz carrier, Gaussian bursts with sigma=.028 s, amplitude=1.3*.60 and .010-s timing jitter centered on physical troughs, mixed pink/white noise at 20 dB SNR, no 96-Hz component. Signal seed=20260618. Unit b retains the identical signal/noise and adds a 3x 11-Hz sine with the separate predeclared phase stream. Unit-c seeds and streams and the unit-d selection were also fixed in the committed protocol.

## Held-out evaluation and decision criteria

No held-out data were generated. The requested per-scenario recovery tables, null AUCs, event-test rejection rates and H1/H2 figures therefore have no values. Missing results are not scored as criterion failures.

| Criterion | Status | Numbers |
| --- | --- | --- |
| C1 | NOT EVALUATED | Held-out generation blocked by unit gate a |
| C2 | NOT EVALUATED | Held-out generation blocked by unit gate a |
| C3 | NOT EVALUATED | Held-out generation blocked by unit gate a |
| C4 | NOT EVALUATED | Held-out generation blocked by unit gate a |

Decision criteria are retained verbatim in the protocol. The candidate has not been designated APC v2.0 or frozen with that tag.

## Runtime, fixes and deviations

Unit-driver elapsed time: 29.266606 seconds, excluding MATLAB startup. One computation thread. MATLAB 9.13.0.2105380 (R2022b) Update 2. Full MATLAB log: [unit_attempt_01_matlab.log](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/unit_attempt_01_matlab.log>).

Implementation bugs fixed after unit testing: none.

Tooling deviations: none during the unit execution. MATLAB startup may report pre-existing missing Brainstorm paths; the driver verifies the exact repository APC source before execution. The protocol mirror is the documented path-layout accommodation. Every Python text read/write explicitly uses UTF-8.

Stopped work: remaining unit gates (if any), v2.0 tagging, held-out data generation/evaluation, criterion decisions and held-out figures. The failed method-relevant gate is the reason for stopping. The source remains at the committed candidate; earlier commits, tags and saved results were not rewritten.

## Full provenance

Trial CSVs and MAT checkpoints include commit, MATLAB version, complete normalized APC options, full fixed comparator settings, signal/surrogate seeds, generator settings and diagnostic arrays. Output hashes: [output_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/output_manifest.json>).

```json
{
  "git_commit": "7848af05ada722971769da856e970d0737820169",
  "tag": "not_created",
  "matlab_version": "9.13.0.2105380 (R2022b) Update 2",
  "signal_seed": 20260618.0,
  "heldout_seed": 20261022.0,
  "heldout_generated": false,
  "apc_options": {
    "fA": [
      80,
      160
    ],
    "epoch": [
      -0.6,
      0.6
    ],
    "decomposition": "fft_peak",
    "metric": "canolty",
    "diagm": false,
    "surrogates": false,
    "num_perm": 0,
    "numPhaseBins": 18,
    "burstTimeBandwidth": 5,
    "phaseTimeBandwidth": 20,
    "phaseEpochCycles": 3,
    "minPhaseHz": 1,
    "maxPhaseHz": 30,
    "flipTroughs": true,
    "burstProminenceScale": 0.75,
    "surrogateMethod": "circular_shift",
    "amplitudeBandWidthHz": 4,
    "stepFourMode": "v1",
    "fPRefine": true,
    "fPMaxBinSpacingHz": 0.05,
    "version": "v2",
    "eventSurrogateSeed": 20260619.0,
    "eventSurrogateSubstream": 2
  },
  "comparator_settings": {
    "phase_grid_hz": [
      3,
      3.5,
      4,
      4.5,
      5,
      5.5,
      6,
      6.5,
      7,
      7.5,
      8,
      8.5,
      9,
      9.5,
      10,
      10.5,
      11,
      11.5,
      12,
      12.5,
      13,
      13.5,
      14
    ],
    "phase_half_width_hz": 1.5,
    "amplitude_grid_hz": [
      80,
      84,
      88,
      92,
      96,
      100,
      104,
      108,
      112,
      116,
      120,
      124,
      128,
      132,
      136,
      140,
      144,
      148,
      152,
      156,
      160
    ],
    "A2_prime_half_width_hz": 14,
    "A1_prime_half_width": "candidate fP",
    "metrics": [
      "MVL-raw",
      "MVL-Ozkurt",
      "KLMI",
      "GLM"
    ]
  },
  "base_tag": "v1.0",
  "base_commit": "71ebc16aed32ca38be73a800738b975e5806b330",
  "apc_source_blob": "6545166cbb7f7fe02d410f9c328e180a8de53f61",
  "protocol_git_blob": "1d21051e52e1eb0fc936eaf78d8fa222db2c710a",
  "unit_profile": {
    "profile_name": "reviewer_control",
    "random_seed": 20260618.0,
    "fs_hz": 500,
    "duration_s": 6,
    "true_fp_hz": 8,
    "true_fa_hz": 120,
    "distractor_fa_hz": 96,
    "phase_offset_deg": 180,
    "low_amp": 1,
    "true_high_amp": 1.3,
    "distractor_base_amp": 0,
    "base_hf_amp": 0.08,
    "burst_sigma_s": 0.028,
    "coupling_level": 0.6,
    "burst_phase_jitter_s": 0.01,
    "snr_db": 20,
    "broad_fa_band_hz": [
      80,
      160
    ],
    "phase_scan_hz": [
      4,
      5,
      6,
      7,
      8,
      9,
      10,
      11,
      12
    ],
    "amplitude_scan_hz": [
      80,
      88,
      96,
      104,
      112,
      120,
      128,
      136,
      144,
      152
    ],
    "phase_band_half_width_hz": 1.5,
    "amplitude_band_half_width_hz": 6,
    "metric": "canolty",
    "fa_tolerance_hz": 8,
    "fp_tolerance_hz": 1,
    "oracle_control_distractor_scale": 0,
    "n_repeats": 25,
    "distractor_scale_values": [
      0,
      0.5,
      1,
      1.5,
      2,
      2.5,
      3
    ],
    "slow_distractor_hz": 11,
    "slow_amplitude_ratios": [
      0,
      3
    ],
    "slow_distractor_phase_rad": 0,
    "slow_amplitude_ratio": 0,
    "high_frequency_distractor_present": false
  },
  "surrogate_generator": "mrg32k3a",
  "surrogate_seed": 20260619.0,
  "surrogate_substream": 2,
  "unit_poisson_seeds": [
    20260618.0,
    20260619.0,
    20260620.0,
    20260621.0,
    20260622.0,
    20260623.0,
    20260624.0,
    20260625.0,
    20260626.0,
    20260627.0
  ],
  "unit_poisson_generator": "mrg32k3a",
  "unit_poisson_substream": 3,
  "uncoupled_phase_seed": 20260619.0,
  "uncoupled_phase_generator": "mrg32k3a",
  "uncoupled_phase_substream": 1
}
```
