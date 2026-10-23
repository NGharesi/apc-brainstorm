# APC v2 candidate 2 results

Final authorized candidate. Candidate 1 remains in commit `7848af05ada722971769da856e970d0737820169`; its saved results are unchanged. Candidate 2 stopped at unit gate a. No v2.0 tag or held-out data were created.

## Factual summary (8 lines)

1. Candidate-2 unit gates: a=FAIL, a2=NOT_RUN, b=NOT_RUN, c=NOT_RUN, d=NOT_RUN.

2. Completed unit trial rows and BLP/PPC curves: 1 each.

3. All five v1 compatibility cases exactly matched the v1.0 reference.

4. Burst detection, direct BLP, surrogate direct-sum equivalence, PPC, diagnostic isolation and RNG checks passed.

5. First failed gate: a.

6. The decision criteria C1-C4 remain text-identical to candidate 1.

7. Held-out data generation and criterion evaluation: not run.

8. v2.0 tag: not created; no further candidates were made.

## Candidate history and exact revision

Candidate 1 failed gate (a) with fP=10.631999875603938 Hz and fA=120 Hz. The user identified the flat-PPC filter-center issue from its saved curve. This cause and the revised authorization are recorded under Candidate history in [PROTOCOL_v2.md](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_02/PROTOCOL_v2.md>). The identical tracked protocol is [PROTOCOL_v2.md](<C:/Users/nghare/.brainstorm/process/apc-brainstorm-publish/analysis/v2_revision/PROTOCOL_v2.md>). The original protocol is preserved at [PROTOCOL_v2.md](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_01/PROTOCOL_v2.md>).

Candidate 2 replaces phase selection with the specified debiased burst-locked power: two-second demeaned, symmetric-Hann windows, direct Fourier coefficients, 0.05-Hz candidate grid, raw-BLP parabolic interpolation and no polarity flips in Step 2. The phase filter, Steps 1/3/4, unit profiles/seeds and every C1-C4 threshold are unchanged. PPC from coefficient phases is diagnostic only. The event test uses the maximum BLP across the full grid and 200 full-grid surrogate maxima; the fixed-frequency BLP z/p is secondary. Jitters are independent conditional uniform draws inside the window-usable range. Direct coefficients at bracketing sample centers are batched and linearly interpolated, which is checked against independent direct extraction of continuous-center segments.

## Unit gates

| Gate | Criterion | Result |
| --- | --- | --- |
| a | \|fP-8\|<=0.1 Hz and \|fA-120\|<=4 Hz | FAIL |
| a2 | fP in [5.3,6.7,9.4,10.8] Hz; each phase error<=0.1 Hz | NOT_RUN |
| b | Added uncoupled 11-Hz sine at 3x; \|fP-8\|<=0.5 Hz | NOT_RUN |
| c | Poisson: corrected event p>0.05 in at least 8/10 seeds | NOT_RUN |
| d | Run first 25 existing level-0 distractor trials without tuning | NOT_RUN |

| Test | Trial | True fP | fP | fA | \|fP error\| | C_APC | Ozkurt | PPC at fP | BLP at fP | Grid-max BLP | Max z | Max p | Fixed z | Fixed p | Bursts/usable | Flags | Status | Pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| a | 1 | 8 | 7.999690124 | 115 | 0.0003098760679 | 0.08059441712 | 0.1697779607 | 0.8305987212 | 51061.86765 | 50985.83408 | 32.63989034 | 0.004975124378 | 25.79496691 | 0.004975124378 | 48/32 | 0 | 0 | 0 |

Stopping result: true fP=8 Hz; recovered fP=7.9996901239320914 Hz; absolute phase error=0.00030987606790855438 Hz; recovered fA=115 Hz; absolute amplitude error=5 Hz. The predeclared gate was evaluated without changing any signal or parameter.

No subsequent gates were run after this failure. The remaining tests, commit as candidate 2, v2.0 tagging and held-out suite were not performed. No third candidate or post-result method change was made.

Per-trial CSV: [unit_trials.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_02/unit_attempt_01/unit_trials.csv>). Complete gate record: [unit_results.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_02/unit_attempt_01/unit_results.json>). Implementation checks: [implementation_checks.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_02/unit_attempt_01/implementation_checks.json>). Compatibility: [v1_compatibility.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_02/unit_attempt_01/v1_compatibility.json>).

| BLP/PPC curve | Grid rows |
| --- | --- |
| [unit_a_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_02/unit_attempt_01/unit_a_curves.csv>) | 567 |

Each completed test has a saved MAT checkpoint containing signals/components, full options, source provenance, both surrogate-statistic vectors and intermediate arrays. [unit_a.mat](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_02/unit_attempt_01/unit_a.mat>).

The precision gate uses the unchanged generator at each requested true fP, initialized with the original seed 20260618. Units (a), (b), (c) and (d) retain the original committed profiles and seed schemes. All random generators and per-trial surrogate substreams are stored in the CSVs and MAT metadata.

## Freeze state and held-out criteria

The unit tests ran on the candidate-2 working sources before the conditional commit, as requested. The metadata git_commit is the candidate-1 base commit; it is not presented as the candidate-2 method commit. Exact tested method blob: `4a1e23c6324516be2bbe92543182c1be1a9e198b`. The source snapshot is [bst_apc.m](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_02/unit_attempt_01/source_snapshot/bst_apc.m>); the tested protocol and runner are saved beside it. The method-source hash was verified unchanged at test completion.

| Criterion | Status |
| --- | --- |
| C1 | NOT EVALUATED: unit gate a failed |
| C2 | NOT EVALUATED: unit gate a failed |
| C3 | NOT EVALUATED: unit gate a failed |
| C4 | NOT EVALUATED: unit gate a failed |

H1-H4 simulations, null AUCs, held-out p-value rejection rates, tPAC availability and H1/H2 figures were not evaluated. No data for these analyses were generated.

## Runtime, deviations and preservation

Unit-driver elapsed time: 29.209456 seconds, excluding MATLAB startup. One computation thread; MATLAB 9.13.0.2105380 (R2022b) Update 2. Log: [unit_attempt_01_matlab.log](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_02/unit_attempt_01_matlab.log>).

Implementation bug fixes after unit execution: none.

Tooling deviations: none during unit execution. The previously documented protocol mirror remains necessary because the output folder is outside Git. Candidate-2 results use their own subfolder to preserve candidate-1 saved outputs. All Python text I/O uses UTF-8. Pre-existing missing Brainstorm startup paths may be reported in the MATLAB log.

Candidate-1 preserved-file checks: 15 passed (its superseded protocol is checked against the archived original). Candidate 1 remains committed, v1.0 remains unchanged, and prior results were not overwritten. No further candidate was made.

Final source-section and preservation audit: [final_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_02/final_verification.json>). It confirms unchanged v1 calculations, Steps 1/3/4 and the phase-filter rule, an unchanged unit generator, an exact match to the tested source snapshot, and 125 unchanged prior v1 result/input files.

## Full unit provenance

```json
{
  "candidate": 2,
  "git_commit": "7848af05ada722971769da856e970d0737820169",
  "git_worktree_status": "M analysis/v2_revision/PROTOCOL_v2.md\n M analysis/v2_revision/run_v2_units.m\n M src/bst_apc.m",
  "source_committed": false,
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
  "apc_source_blob": "4a1e23c6324516be2bbe92543182c1be1a9e198b",
  "protocol_git_blob": "197c1645e1f747959ccbb1e9bdaf8bd7af2171be",
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
  "uncoupled_phase_substream": 1,
  "repository": "C:\\Users\\nghare\\.brainstorm\\process\\apc-brainstorm-publish"
}
```
