# APC v1.0 simulation rerun

Branch `v1.0-revision`; commit `71ebc16aed32ca38be73a800738b975e5806b330`; annotated tag `v1.0` → the same commit. Method source was committed/tagged before the main, random-fP and null runs. No method changes were made afterward.

## Factual summary (8 lines)

1. Frozen commit: 71ebc16aed32ca38be73a800738b975e5806b330; tag: v1.0.

2. The oct2026 sanity check exactly matched all 175 saved distractor fA, fP and coupling values.

3. The June compatibility sanity check matched all 25 endpoint fA, fP and coupling values and returned 12/25 joint recovery.

4. Main rerun: 350 paired coupled trials, 4 APC configurations, 8 comparator configurations/metrics; 4200 result rows.

5. Primary APC main joint recovery totals 267/350 across the 14 levels.

6. Random-fP check: 150 shared frequency draws; primary APC joint recovery totals 111/150.

7. Null checks: 350 timing-null pairs and 350 no-coupled-burst controls; all shared-component and signal-difference checks passed.

8. The original saved benchmark files remain byte-identical; MATLAB 9.13.0.2105380 (R2022b) Update 2.

## Freeze and required compatibility checks

| Check | Trials | Exact fA | Exact fP | Exact score | Joint recovery |
| --- | --- | --- | --- | --- | --- |
| oct2026, refinement=false; all distractor levels | 175 | 175 | 175 | 175 | 150 |
| june2026_clipped, refinement=false; sparsity=.15 | 25 | 25 | 25 | 25 | 12 |

Both compatibility checks and the five-trial v1 smoke test ran on the clean committed source before tagging. Their APC blob equals `v1.0:src/bst_apc.m`. [freeze_attestation.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/freeze_attestation.json>) records the link to the frozen commit. Committed sanity rows: [sanity_trials.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/committed_checks/sanity_trials.csv>). Smoke rows: [smoke_trials.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/committed_checks/smoke_trials.csv>). Earlier pre-commit records were preserved separately.

The v1 bandwidth rule was already 2*fP before this resume; no bandwidth-method correction was necessary. The smoke test returned candidate half-width = final nominal half-width = recovered fP in 5/5 trials. Changing amplitudeBandWidthHz from 4 to 40 Hz left all five numerical outputs unchanged. Per-trial CSVs record both nominal half-widths and the actual clipped final edges.

| Smoke trial | Recovered fP Hz | Candidate half-width Hz | Final nominal half-width Hz | Final clipped band Hz |
| --- | --- | --- | --- | --- |
| 1 | 8.05 | 8.05 | 8.05 | 103.95003818151223 to 120.04996181848777 |
| 2 | 7.969 | 7.969 | 7.969 | 112.03093621623161 to 127.96906378376839 |
| 3 | 8.064 | 8.064 | 8.064 | 111.93612877254495 to 128.06387122745505 |
| 4 | 8.033 | 8.033 | 8.033 | 114.96675351167224 to 131.03324648832776 |
| 5 | 8.049 | 8.049 | 8.049 | 134.95055959935328 to 150 |

## Definitions and configuration

The primary APC mode uses a 1 Hz amplitude grid and candidate/final half-width equal to recovered fP. Refined fP uses the preserved demeaned Welch spectrum, a power-of-two zero-padding length giving ≤0.05 Hz bin spacing, and a three-point log-power parabola at an interior concave maximum. The legacy phase rule remains selectable with refinement=false. The inherited October 20 detrending/cycle-bound changes are excluded so the specified legacy checks reproduce the saved outputs. Full frozen implementation choices are in [PROTOCOL.md](<C:/Users/nghare/.brainstorm/process/apc-brainstorm-publish/analysis/v1_revision/PROTOCOL.md>).

A0 uses amplitude half-width 6 Hz; A1 uses candidate fP. All comparators use phase half-width 1.5 Hz and fA grid 80:8:152. Each metric independently selects its full-grid maximum. Raw MVL and conventional Ozkurt-normalized MVL are separate scans. Ozkurt normalization is |sum(A exp(iφ))|/sqrt(N sum(A²)); the older helper with an additional 1/sqrt(N) is not used. KL-MI uses 18 phase bins; GLM uses R².

Recovery limits are inclusive: phase ±1 Hz and amplitude ±8 Hz. “fA-only” and “fP-only” denote marginal criteria, rather than exclusive categories. Strict joint recovery replaces phase tolerance with ±0.5 Hz. All denominators remain 25; invalid estimates count as failures. Error summaries use finite estimates, with finite counts in the CSVs. Boundary picks use equality to 4/12 Hz within 1e-9; APC searches its own documented phase limits, rather than the comparator grid. `NaN` for APC grid spacing means no prescribed scan grid.

## Main rerun

Per-trial data: [main_trials.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/main_trials.csv>). Full summaries, including finite counts and provenance: [main_summary.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/main_summary.csv>).

### Sparsity

| Configuration | Method | fP grid Hz | Level | Joint /25 | fA /25 | fP /25 | Joint .5Hz /25 | Valid /25 | fP error mean / median Hz | fA error mean / median Hz | fP=4 /12 | Direct /TF /other |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v1.0 | APC | NaN | 1 | 20 | 20 | 25 | 20 | 25 | 0.05931 / 0.0622 | 6.92 / 4 | 0 / 0 | 25 / 0 / 0 |
| oct2026 | APC | NaN | 1 | 24 | 24 | 25 | 24 | 25 | 0.2509 / 0.3008 | 4.96 / 5 | 0 / 0 | 25 / 0 / 0 |
| june2026_clipped | APC | NaN | 1 | 25 | 25 | 25 | 25 | 25 | 0.2509 / 0.3008 | 0.8 / 0 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 1 | 20 | 20 | 25 | 20 | 25 | 0.2509 / 0.3008 | 7.64 / 3 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 1 | 5 | 22 | 5 | 4 | 25 | 3.04 / 4 | 5.44 / 0 | 16 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 1 | 5 | 10 | 5 | 3 | 25 | 2.92 / 4 | 18.56 / 16 | 13 / 0 | — |
| A0 | KLMI-scan | 1 | 1 | 2 | 8 | 2 | 0 | 25 | 3.48 / 4 | 16.96 / 16 | 17 / 0 | — |
| A0 | GLM-scan | 1 | 1 | 4 | 15 | 4 | 1 | 25 | 3.16 / 4 | 11.2 / 8 | 15 / 0 | — |
| A1 | MVL-raw | 1 | 1 | 25 | 25 | 25 | 0 | 25 | 1 / 1 | 0 / 0 | 0 / 0 | — |
| A1 | MVL-Ozkurt | 1 | 1 | 25 | 25 | 25 | 12 | 25 | 0.52 / 1 | 3.84 / 0 | 0 / 0 | — |
| A1 | KLMI-scan | 1 | 1 | 25 | 25 | 25 | 12 | 25 | 0.52 / 1 | 3.84 / 0 | 0 / 0 | — |
| A1 | GLM-scan | 1 | 1 | 25 | 25 | 25 | 3 | 25 | 0.88 / 1 | 0.96 / 0 | 0 / 0 | — |
| v1.0 | APC | NaN | 0.85 | 20 | 20 | 25 | 20 | 25 | 0.06013 / 0.06066 | 8.6 / 4 | 0 / 0 | 25 / 0 / 0 |
| oct2026 | APC | NaN | 0.85 | 22 | 22 | 25 | 22 | 25 | 0.2464 / 0.3008 | 6.52 / 5 | 0 / 0 | 25 / 0 / 0 |
| june2026_clipped | APC | NaN | 0.85 | 24 | 24 | 25 | 24 | 25 | 0.2464 / 0.3008 | 2.4 / 0 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 0.85 | 18 | 18 | 25 | 18 | 25 | 0.2464 / 0.3008 | 8.72 / 4 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 0.85 | 3 | 23 | 3 | 2 | 25 | 3.12 / 4 | 3.52 / 0 | 13 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 0.85 | 7 | 12 | 7 | 2 | 25 | 2.64 / 3 | 16.96 / 16 | 11 / 0 | — |
| A0 | KLMI-scan | 1 | 0.85 | 3 | 5 | 3 | 1 | 25 | 3.28 / 4 | 22.4 / 24 | 16 / 0 | — |
| A0 | GLM-scan | 1 | 0.85 | 7 | 12 | 7 | 1 | 25 | 2.8 / 3 | 15.04 / 16 | 12 / 0 | — |
| A1 | MVL-raw | 1 | 0.85 | 25 | 25 | 25 | 0 | 25 | 1 / 1 | 0 / 0 | 0 / 0 | — |
| A1 | MVL-Ozkurt | 1 | 0.85 | 24 | 24 | 24 | 7 | 25 | 0.84 / 1 | 3.52 / 0 | 1 / 0 | — |
| A1 | KLMI-scan | 1 | 0.85 | 23 | 23 | 23 | 6 | 25 | 1 / 1 | 3.84 / 0 | 2 / 0 | — |
| A1 | GLM-scan | 1 | 0.85 | 24 | 24 | 24 | 1 | 25 | 1.08 / 1 | 1.28 / 0 | 1 / 0 | — |
| v1.0 | APC | NaN | 0.7 | 18 | 18 | 25 | 18 | 25 | 0.05592 / 0.05943 | 11.04 / 6 | 0 / 0 | 25 / 0 / 0 |
| oct2026 | APC | NaN | 0.7 | 20 | 20 | 25 | 20 | 25 | 0.2464 / 0.3008 | 8.2 / 6 | 0 / 0 | 25 / 0 / 0 |
| june2026_clipped | APC | NaN | 0.7 | 24 | 24 | 25 | 24 | 25 | 0.2464 / 0.3008 | 2.24 / 0 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 0.7 | 20 | 20 | 25 | 20 | 25 | 0.2464 / 0.3008 | 8.64 / 3 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 0.7 | 4 | 24 | 4 | 2 | 25 | 3.04 / 4 | 2.56 / 0 | 13 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 0.7 | 7 | 12 | 7 | 5 | 25 | 2.68 / 3 | 15.36 / 16 | 12 / 0 | — |
| A0 | KLMI-scan | 1 | 0.7 | 1 | 10 | 1 | 1 | 25 | 3.6 / 4 | 18.88 / 16 | 18 / 0 | — |
| A0 | GLM-scan | 1 | 0.7 | 5 | 16 | 5 | 1 | 25 | 3.04 / 4 | 12.16 / 8 | 13 / 0 | — |
| A1 | MVL-raw | 1 | 0.7 | 25 | 25 | 25 | 0 | 25 | 1 / 1 | 0 / 0 | 0 / 0 | — |
| A1 | MVL-Ozkurt | 1 | 0.7 | 24 | 24 | 24 | 5 | 25 | 0.92 / 1 | 3.2 / 0 | 1 / 0 | — |
| A1 | KLMI-scan | 1 | 0.7 | 24 | 24 | 24 | 5 | 25 | 0.92 / 1 | 2.24 / 0 | 1 / 0 | — |
| A1 | GLM-scan | 1 | 0.7 | 24 | 24 | 24 | 6 | 25 | 0.88 / 1 | 2.88 / 0 | 1 / 0 | — |
| v1.0 | APC | NaN | 0.55 | 18 | 18 | 25 | 18 | 25 | 0.05208 / 0.0565 | 10 / 4 | 0 / 0 | 25 / 0 / 0 |
| oct2026 | APC | NaN | 0.55 | 20 | 20 | 25 | 20 | 25 | 0.2464 / 0.3008 | 8.28 / 6 | 0 / 0 | 25 / 0 / 0 |
| june2026_clipped | APC | NaN | 0.55 | 21 | 21 | 25 | 21 | 25 | 0.2464 / 0.3008 | 5.36 / 0 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 0.55 | 18 | 18 | 25 | 18 | 25 | 0.2464 / 0.3008 | 8.92 / 4 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 0.55 | 2 | 23 | 2 | 0 | 25 | 3.48 / 4 | 3.52 / 0 | 17 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 0.55 | 0 | 11 | 1 | 0 | 25 | 3.52 / 4 | 16.64 / 24 | 18 / 0 | — |
| A0 | KLMI-scan | 1 | 0.55 | 0 | 8 | 0 | 0 | 25 | 3.64 / 4 | 18.56 / 24 | 18 / 0 | — |
| A0 | GLM-scan | 1 | 0.55 | 0 | 9 | 0 | 0 | 25 | 3.48 / 4 | 16.32 / 16 | 15 / 0 | — |
| A1 | MVL-raw | 1 | 0.55 | 25 | 25 | 25 | 0 | 25 | 1 / 1 | 0 / 0 | 0 / 0 | — |
| A1 | MVL-Ozkurt | 1 | 0.55 | 23 | 24 | 23 | 2 | 25 | 1.16 / 1 | 1.6 / 0 | 2 / 0 | — |
| A1 | KLMI-scan | 1 | 0.55 | 23 | 23 | 23 | 3 | 25 | 1.12 / 1 | 3.52 / 0 | 2 / 0 | — |
| A1 | GLM-scan | 1 | 0.55 | 23 | 24 | 23 | 3 | 25 | 1.12 / 1 | 2.24 / 0 | 2 / 0 | — |
| v1.0 | APC | NaN | 0.4 | 20 | 20 | 25 | 20 | 25 | 0.05368 / 0.05763 | 7.72 / 2 | 0 / 0 | 25 / 0 / 0 |
| oct2026 | APC | NaN | 0.4 | 16 | 16 | 25 | 16 | 25 | 0.2419 / 0.1875 | 10.48 / 8 | 0 / 0 | 25 / 0 / 0 |
| june2026_clipped | APC | NaN | 0.4 | 22 | 22 | 25 | 22 | 25 | 0.2419 / 0.1875 | 5.84 / 0 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 0.4 | 18 | 18 | 25 | 18 | 25 | 0.2419 / 0.1875 | 8.88 / 3 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 0.4 | 2 | 23 | 2 | 2 | 25 | 3.24 / 4 | 2.56 / 0 | 13 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 0.4 | 2 | 12 | 2 | 1 | 25 | 3.44 / 4 | 16.32 / 16 | 18 / 0 | — |
| A0 | KLMI-scan | 1 | 0.4 | 1 | 9 | 1 | 0 | 25 | 3.56 / 4 | 19.2 / 16 | 17 / 0 | — |
| A0 | GLM-scan | 1 | 0.4 | 1 | 8 | 2 | 1 | 25 | 3.2 / 4 | 18.88 / 16 | 13 / 0 | — |
| A1 | MVL-raw | 1 | 0.4 | 25 | 25 | 25 | 0 | 25 | 1 / 1 | 0 / 0 | 0 / 0 | — |
| A1 | MVL-Ozkurt | 1 | 0.4 | 11 | 17 | 11 | 3 | 25 | 2.52 / 4 | 9.92 / 8 | 13 / 0 | — |
| A1 | KLMI-scan | 1 | 0.4 | 13 | 19 | 14 | 1 | 25 | 2.2 / 1 | 9.6 / 0 | 9 / 0 | — |
| A1 | GLM-scan | 1 | 0.4 | 9 | 17 | 10 | 2 | 25 | 2.56 / 3 | 13.12 / 8 | 12 / 0 | — |
| v1.0 | APC | NaN | 0.25 | 16 | 16 | 25 | 16 | 25 | 0.0408 / 0.03766 | 11.36 / 5 | 0 / 0 | 25 / 0 / 0 |
| oct2026 | APC | NaN | 0.25 | 4 | 4 | 25 | 4 | 25 | 0.2192 / 0.1875 | 18.6 / 16 | 0 / 0 | 25 / 0 / 0 |
| june2026_clipped | APC | NaN | 0.25 | 11 | 11 | 25 | 11 | 25 | 0.2192 / 0.1875 | 16 / 12 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 0.25 | 15 | 15 | 25 | 15 | 25 | 0.2192 / 0.1875 | 12.64 / 6 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 0.25 | 1 | 22 | 1 | 0 | 25 | 3.12 / 3 | 4.16 / 0 | 12 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 0.25 | 0 | 7 | 0 | 0 | 25 | 3.56 / 4 | 21.44 / 24 | 17 / 0 | — |
| A0 | KLMI-scan | 1 | 0.25 | 0 | 9 | 0 | 0 | 25 | 3.84 / 4 | 17.6 / 16 | 22 / 0 | — |
| A0 | GLM-scan | 1 | 0.25 | 0 | 10 | 0 | 0 | 25 | 3.64 / 4 | 17.6 / 16 | 18 / 0 | — |
| A1 | MVL-raw | 1 | 0.25 | 19 | 24 | 19 | 1 | 25 | 1.48 / 1 | 1.6 / 0 | 2 / 0 | — |
| A1 | MVL-Ozkurt | 1 | 0.25 | 6 | 14 | 6 | 4 | 25 | 2.8 / 4 | 14.72 / 8 | 14 / 0 | — |
| A1 | KLMI-scan | 1 | 0.25 | 4 | 14 | 4 | 1 | 25 | 3.32 / 4 | 13.76 / 8 | 18 / 0 | — |
| A1 | GLM-scan | 1 | 0.25 | 1 | 9 | 1 | 0 | 25 | 3.6 / 4 | 16.32 / 16 | 18 / 0 | — |
| v1.0 | APC | NaN | 0.15 | 13 | 13 | 25 | 13 | 25 | 0.04631 / 0.03338 | 12.48 / 8 | 0 / 0 | 25 / 0 / 0 |
| oct2026 | APC | NaN | 0.15 | 6 | 6 | 25 | 6 | 25 | 0.2147 / 0.1875 | 16.52 / 17 | 0 / 0 | 25 / 0 / 0 |
| june2026_clipped | APC | NaN | 0.15 | 12 | 12 | 25 | 12 | 25 | 0.2147 / 0.1875 | 13.04 / 12 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 0.15 | 10 | 10 | 25 | 10 | 25 | 0.2147 / 0.1875 | 14.56 / 13 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 0.15 | 0 | 22 | 0 | 0 | 25 | 3.4 / 4 | 5.44 / 0 | 15 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 0.15 | 1 | 10 | 1 | 0 | 25 | 3.28 / 4 | 17.28 / 16 | 13 / 0 | — |
| A0 | KLMI-scan | 1 | 0.15 | 0 | 8 | 0 | 0 | 25 | 3.8 / 4 | 16.32 / 16 | 21 / 0 | — |
| A0 | GLM-scan | 1 | 0.15 | 0 | 5 | 1 | 0 | 25 | 3.36 / 4 | 21.76 / 24 | 15 / 0 | — |
| A1 | MVL-raw | 1 | 0.15 | 11 | 20 | 11 | 0 | 25 | 2.4 / 2 | 8 / 0 | 7 / 2 | — |
| A1 | MVL-Ozkurt | 1 | 0.15 | 3 | 9 | 4 | 0 | 25 | 2.88 / 3 | 20.48 / 16 | 10 / 0 | — |
| A1 | KLMI-scan | 1 | 0.15 | 3 | 14 | 4 | 0 | 25 | 3.2 / 4 | 14.4 / 8 | 15 / 0 | — |
| A1 | GLM-scan | 1 | 0.15 | 0 | 8 | 0 | 0 | 25 | 3.48 / 4 | 21.12 / 16 | 15 / 0 | — |

![Joint recovery, sparsity](C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/joint_recovery_sparsity.png)

Figure files: [joint_recovery_sparsity.png](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/joint_recovery_sparsity.png>), [joint_recovery_sparsity.svg](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/joint_recovery_sparsity.svg>), [joint_recovery_sparsity.fig](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/joint_recovery_sparsity.fig>).

### Distractor

| Configuration | Method | fP grid Hz | Level | Joint /25 | fA /25 | fP /25 | Joint .5Hz /25 | Valid /25 | fP error mean / median Hz | fA error mean / median Hz | fP=4 /12 | Direct /TF /other |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v1.0 | APC | NaN | 0 | 19 | 19 | 24 | 19 | 24 | 0.05814 / 0.05626 | 6.792 / 4.5 | 0 / 0 | 24 / 0 / 1 |
| oct2026 | APC | NaN | 0 | 24 | 24 | 25 | 24 | 25 | 0.2419 / 0.1875 | 5.6 / 5 | 0 / 0 | 25 / 0 / 0 |
| june2026_clipped | APC | NaN | 0 | 25 | 25 | 25 | 25 | 25 | 0.2419 / 0.1875 | 0.64 / 0 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 0 | 20 | 20 | 25 | 20 | 25 | 0.2419 / 0.1875 | 6.76 / 4 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 0 | 3 | 24 | 3 | 2 | 25 | 2.96 / 3 | 2.56 / 0 | 10 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 0 | 3 | 6 | 3 | 2 | 25 | 3.04 / 3 | 24 / 24 | 11 / 0 | — |
| A0 | KLMI-scan | 1 | 0 | 0 | 4 | 0 | 0 | 25 | 3.52 / 4 | 25.92 / 24 | 14 / 0 | — |
| A0 | GLM-scan | 1 | 0 | 2 | 8 | 2 | 0 | 25 | 2.88 / 3 | 22.72 / 24 | 6 / 0 | — |
| A1 | MVL-raw | 1 | 0 | 25 | 25 | 25 | 0 | 25 | 1 / 1 | 0 / 0 | 0 / 0 | — |
| A1 | MVL-Ozkurt | 1 | 0 | 25 | 25 | 25 | 6 | 25 | 0.76 / 1 | 1.92 / 0 | 0 / 0 | — |
| A1 | KLMI-scan | 1 | 0 | 25 | 25 | 25 | 7 | 25 | 0.72 / 1 | 2.24 / 0 | 0 / 0 | — |
| A1 | GLM-scan | 1 | 0 | 25 | 25 | 25 | 1 | 25 | 0.96 / 1 | 0.32 / 0 | 0 / 0 | — |
| v1.0 | APC | NaN | 0.5 | 21 | 21 | 25 | 21 | 25 | 0.05887 / 0.05968 | 6.48 / 4 | 0 / 0 | 25 / 0 / 0 |
| oct2026 | APC | NaN | 0.5 | 24 | 24 | 25 | 24 | 25 | 0.2464 / 0.3008 | 5.48 / 5 | 0 / 0 | 25 / 0 / 0 |
| june2026_clipped | APC | NaN | 0.5 | 23 | 23 | 25 | 23 | 25 | 0.2464 / 0.3008 | 2.72 / 0 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 0.5 | 22 | 22 | 25 | 22 | 25 | 0.2464 / 0.3008 | 5.44 / 4 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 0.5 | 4 | 22 | 4 | 4 | 25 | 2.84 / 3 | 4.8 / 0 | 11 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 0.5 | 5 | 10 | 5 | 2 | 25 | 2.92 / 3 | 19.2 / 16 | 11 / 0 | — |
| A0 | KLMI-scan | 1 | 0.5 | 1 | 9 | 1 | 0 | 25 | 3.64 / 4 | 18.88 / 16 | 19 / 0 | — |
| A0 | GLM-scan | 1 | 0.5 | 2 | 15 | 2 | 0 | 25 | 3.4 / 4 | 12.8 / 8 | 16 / 0 | — |
| A1 | MVL-raw | 1 | 0.5 | 25 | 25 | 25 | 0 | 25 | 1 / 1 | 0 / 0 | 0 / 0 | — |
| A1 | MVL-Ozkurt | 1 | 0.5 | 25 | 25 | 25 | 7 | 25 | 0.72 / 1 | 2.24 / 0 | 0 / 0 | — |
| A1 | KLMI-scan | 1 | 0.5 | 25 | 25 | 25 | 9 | 25 | 0.64 / 1 | 2.88 / 0 | 0 / 0 | — |
| A1 | GLM-scan | 1 | 0.5 | 25 | 25 | 25 | 1 | 25 | 0.96 / 1 | 0.32 / 0 | 0 / 0 | — |
| v1.0 | APC | NaN | 1 | 23 | 23 | 25 | 23 | 25 | 0.0425 / 0.04537 | 5.16 / 4 | 0 / 0 | 25 / 0 / 0 |
| oct2026 | APC | NaN | 1 | 22 | 22 | 25 | 22 | 25 | 0.2238 / 0.1875 | 6.28 / 5 | 0 / 0 | 25 / 0 / 0 |
| june2026_clipped | APC | NaN | 1 | 24 | 24 | 25 | 24 | 25 | 0.2238 / 0.1875 | 0.8 / 0 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 1 | 25 | 25 | 25 | 25 | 25 | 0.2238 / 0.1875 | 3.72 / 4 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 1 | 2 | 18 | 2 | 2 | 25 | 3.16 / 4 | 8.64 / 8 | 14 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 1 | 4 | 15 | 4 | 3 | 25 | 3.08 / 4 | 13.76 / 8 | 15 / 0 | — |
| A0 | KLMI-scan | 1 | 1 | 1 | 10 | 1 | 1 | 25 | 3.68 / 4 | 18.56 / 16 | 21 / 0 | — |
| A0 | GLM-scan | 1 | 1 | 3 | 17 | 3 | 1 | 25 | 3.24 / 4 | 11.2 / 8 | 16 / 0 | — |
| A1 | MVL-raw | 1 | 1 | 25 | 25 | 25 | 0 | 25 | 1 / 1 | 0 / 0 | 0 / 0 | — |
| A1 | MVL-Ozkurt | 1 | 1 | 24 | 25 | 24 | 9 | 25 | 0.76 / 1 | 3.2 / 0 | 1 / 0 | — |
| A1 | KLMI-scan | 1 | 1 | 25 | 25 | 25 | 10 | 25 | 0.6 / 1 | 3.2 / 0 | 0 / 0 | — |
| A1 | GLM-scan | 1 | 1 | 25 | 25 | 25 | 2 | 25 | 0.92 / 1 | 0.64 / 0 | 0 / 0 | — |
| v1.0 | APC | NaN | 1.5 | 21 | 21 | 23 | 21 | 23 | 0.05639 / 0.04014 | 6.174 / 4 | 0 / 0 | 23 / 0 / 2 |
| oct2026 | APC | NaN | 1.5 | 24 | 25 | 24 | 24 | 25 | 0.4822 / 0.1875 | 5.2 / 5 | 0 / 0 | 25 / 0 / 0 |
| june2026_clipped | APC | NaN | 1.5 | 24 | 25 | 24 | 24 | 25 | 0.4822 / 0.1875 | 0.16 / 0 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 1.5 | 21 | 22 | 24 | 21 | 25 | 0.4822 / 0.1875 | 6.72 / 4 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 1.5 | 0 | 17 | 0 | 0 | 25 | 3.48 / 4 | 8.32 / 0 | 15 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 1.5 | 2 | 8 | 2 | 2 | 25 | 3.24 / 4 | 20.48 / 24 | 13 / 0 | — |
| A0 | KLMI-scan | 1 | 1.5 | 0 | 4 | 0 | 0 | 25 | 3.64 / 4 | 24.64 / 32 | 17 / 0 | — |
| A0 | GLM-scan | 1 | 1.5 | 0 | 8 | 0 | 0 | 25 | 3.36 / 3 | 18.56 / 16 | 12 / 0 | — |
| A1 | MVL-raw | 1 | 1.5 | 25 | 25 | 25 | 0 | 25 | 1 / 1 | 0 / 0 | 0 / 0 | — |
| A1 | MVL-Ozkurt | 1 | 1.5 | 25 | 25 | 25 | 5 | 25 | 0.8 / 1 | 1.6 / 0 | 0 / 0 | — |
| A1 | KLMI-scan | 1 | 1.5 | 25 | 25 | 25 | 8 | 25 | 0.68 / 1 | 2.56 / 0 | 0 / 0 | — |
| A1 | GLM-scan | 1 | 1.5 | 25 | 25 | 25 | 0 | 25 | 1 / 1 | 0 / 0 | 0 / 0 | — |
| v1.0 | APC | NaN | 2 | 22 | 22 | 23 | 22 | 23 | 0.06239 / 0.04377 | 5.217 / 4 | 0 / 0 | 23 / 0 / 2 |
| oct2026 | APC | NaN | 2 | 19 | 19 | 23 | 19 | 25 | 0.7452 / 0.3008 | 8.24 / 5 | 0 / 0 | 25 / 0 / 0 |
| june2026_clipped | APC | NaN | 2 | 22 | 24 | 23 | 22 | 25 | 0.7452 / 0.3008 | 1.92 / 0 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 2 | 21 | 22 | 23 | 21 | 25 | 0.7452 / 0.3008 | 5.28 / 4 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 2 | 0 | 12 | 0 | 0 | 25 | 3.28 / 4 | 13.44 / 24 | 13 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 2 | 1 | 8 | 1 | 0 | 25 | 3.16 / 3 | 21.44 / 24 | 12 / 0 | — |
| A0 | KLMI-scan | 1 | 2 | 1 | 3 | 1 | 0 | 25 | 3.36 / 4 | 24 / 24 | 13 / 0 | — |
| A0 | GLM-scan | 1 | 2 | 0 | 2 | 1 | 0 | 25 | 3.12 / 3 | 25.28 / 24 | 9 / 0 | — |
| A1 | MVL-raw | 1 | 2 | 25 | 25 | 25 | 0 | 25 | 1 / 1 | 0 / 0 | 0 / 0 | — |
| A1 | MVL-Ozkurt | 1 | 2 | 25 | 25 | 25 | 4 | 25 | 0.84 / 1 | 1.28 / 0 | 0 / 0 | — |
| A1 | KLMI-scan | 1 | 2 | 24 | 24 | 24 | 5 | 25 | 0.88 / 1 | 2.24 / 0 | 0 / 0 | — |
| A1 | GLM-scan | 1 | 2 | 25 | 25 | 25 | 1 | 25 | 0.96 / 1 | 0.32 / 0 | 0 / 0 | — |
| v1.0 | APC | NaN | 2.5 | 19 | 19 | 21 | 19 | 21 | 0.05992 / 0.04662 | 6.143 / 4 | 0 / 0 | 21 / 0 / 4 |
| oct2026 | APC | NaN | 2.5 | 20 | 22 | 21 | 20 | 25 | 1.23 / 0.1875 | 5.92 / 5 | 0 / 0 | 25 / 0 / 0 |
| june2026_clipped | APC | NaN | 2.5 | 21 | 25 | 21 | 21 | 25 | 1.23 / 0.1875 | 0.64 / 0 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 2.5 | 19 | 20 | 21 | 19 | 25 | 1.23 / 0.1875 | 6.76 / 3 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 2.5 | 0 | 6 | 0 | 0 | 25 | 3.4 / 3 | 18.24 / 24 | 12 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 2.5 | 1 | 6 | 1 | 0 | 25 | 3.44 / 4 | 22.72 / 24 | 16 / 0 | — |
| A0 | KLMI-scan | 1 | 2.5 | 1 | 5 | 1 | 0 | 25 | 3.52 / 4 | 23.68 / 24 | 18 / 0 | — |
| A0 | GLM-scan | 1 | 2.5 | 2 | 8 | 3 | 0 | 25 | 3.12 / 4 | 19.84 / 24 | 13 / 0 | — |
| A1 | MVL-raw | 1 | 2.5 | 25 | 25 | 25 | 0 | 25 | 1 / 1 | 0 / 0 | 0 / 0 | — |
| A1 | MVL-Ozkurt | 1 | 2.5 | 25 | 25 | 25 | 2 | 25 | 0.92 / 1 | 0.64 / 0 | 0 / 0 | — |
| A1 | KLMI-scan | 1 | 2.5 | 25 | 25 | 25 | 2 | 25 | 0.92 / 1 | 0.64 / 0 | 0 / 0 | — |
| A1 | GLM-scan | 1 | 2.5 | 25 | 25 | 25 | 0 | 25 | 1 / 1 | 0 / 0 | 0 / 0 | — |
| v1.0 | APC | NaN | 3 | 17 | 17 | 21 | 17 | 21 | 0.06021 / 0.06093 | 8.762 / 4 | 0 / 0 | 21 / 0 / 4 |
| oct2026 | APC | NaN | 3 | 17 | 17 | 22 | 17 | 25 | 0.9991 / 0.3008 | 11.92 / 6 | 0 / 0 | 25 / 0 / 0 |
| june2026_clipped | APC | NaN | 3 | 18 | 19 | 22 | 18 | 25 | 0.9991 / 0.3008 | 8.24 / 0 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 3 | 16 | 16 | 22 | 16 | 25 | 0.9991 / 0.3008 | 12.64 / 5 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 3 | 0 | 6 | 0 | 0 | 25 | 3.48 / 4 | 18.24 / 24 | 15 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 3 | 0 | 10 | 0 | 0 | 25 | 3.36 / 4 | 16 / 16 | 13 / 0 | — |
| A0 | KLMI-scan | 1 | 3 | 0 | 7 | 0 | 0 | 25 | 3.84 / 4 | 18.24 / 16 | 21 / 0 | — |
| A0 | GLM-scan | 1 | 3 | 1 | 12 | 1 | 0 | 25 | 3.36 / 4 | 14.08 / 16 | 14 / 0 | — |
| A1 | MVL-raw | 1 | 3 | 25 | 25 | 25 | 0 | 25 | 1 / 1 | 0 / 0 | 0 / 0 | — |
| A1 | MVL-Ozkurt | 1 | 3 | 24 | 24 | 24 | 3 | 25 | 1 / 1 | 2.24 / 0 | 1 / 0 | — |
| A1 | KLMI-scan | 1 | 3 | 24 | 24 | 24 | 4 | 25 | 0.96 / 1 | 2.24 / 0 | 1 / 0 | — |
| A1 | GLM-scan | 1 | 3 | 25 | 25 | 25 | 1 | 25 | 0.96 / 1 | 0.32 / 0 | 0 / 0 | — |

![Joint recovery, distractor](C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/joint_recovery_distractor.png)

Figure files: [joint_recovery_distractor.png](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/joint_recovery_distractor.png>), [joint_recovery_distractor.svg](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/joint_recovery_distractor.svg>), [joint_recovery_distractor.fig](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/joint_recovery_distractor.fig>).

## Random-fP check

Each trial uses a single Uniform[5,11] Hz draw, shared by all methods. A separate stream with seed 20260618 supplies those draws; generator RNG is reset separately for each benchmark. Per-trial rows: [random_fp_trials.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/random_fp_trials.csv>). Draws: [random_fp_draws.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/random_fp_draws.csv>). Summary: [random_fp_summary.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/random_fp_summary.csv>).

### Sparsity

| Configuration | Method | fP grid Hz | Level | Joint /25 | fA /25 | fP /25 | Joint .5Hz /25 | Valid /25 | fP error mean / median Hz | fA error mean / median Hz | fP=4 /12 | Direct /TF /other |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v1.0 | APC | NaN | 0.15 | 14 | 14 | 25 | 14 | 25 | 0.03311 / 0.02907 | 12.04 / 6 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 0.15 | 13 | 13 | 25 | 13 | 25 | 0.1316 / 0.1242 | 14 / 7 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 0.15 | 3 | 21 | 4 | 2 | 25 | 3.445 / 3.668 | 4.16 / 0 | 14 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 0.15 | 1 | 15 | 2 | 1 | 25 | 3.565 / 3.668 | 12.48 / 8 | 14 / 0 | — |
| A0 | KLMI-scan | 1 | 0.15 | 0 | 13 | 1 | 0 | 25 | 3.753 / 4.376 | 13.12 / 8 | 20 / 0 | — |
| A0 | GLM-scan | 1 | 0.15 | 0 | 13 | 1 | 0 | 25 | 3.553 / 3.573 | 13.12 / 8 | 17 / 0 | — |
| A1 | MVL-raw | 1 | 0.15 | 5 | 24 | 5 | 1 | 25 | 2.509 / 1.723 | 1.28 / 0 | 4 / 1 | — |
| A1 | MVL-Ozkurt | 1 | 0.15 | 1 | 16 | 2 | 0 | 25 | 3.469 / 3.592 | 13.44 / 8 | 11 / 0 | — |
| A1 | KLMI-scan | 1 | 0.15 | 2 | 15 | 2 | 0 | 25 | 3.3 / 3.552 | 11.84 / 8 | 11 / 0 | — |
| A1 | GLM-scan | 1 | 0.15 | 0 | 9 | 0 | 0 | 25 | 3.76 / 3.668 | 16.32 / 16 | 15 / 1 | — |
| A0 | MVL-raw | 0.5 | 0.15 | 2 | 20 | 3 | 1 | 25 | 3.445 / 4.059 | 5.12 / 0 | 12 / 0 | — |
| A0 | MVL-Ozkurt | 0.5 | 0.15 | 1 | 16 | 2 | 0 | 25 | 3.605 / 4.073 | 11.2 / 8 | 12 / 0 | — |
| A0 | KLMI-scan | 0.5 | 0.15 | 0 | 13 | 0 | 0 | 25 | 3.741 / 4.151 | 13.12 / 8 | 17 / 0 | — |
| A0 | GLM-scan | 0.5 | 0.15 | 0 | 13 | 0 | 0 | 25 | 3.681 / 4.073 | 13.76 / 8 | 13 / 0 | — |
| A1 | MVL-raw | 0.5 | 0.15 | 4 | 24 | 4 | 0 | 25 | 2.489 / 1.568 | 0.96 / 0 | 2 / 1 | — |
| A1 | MVL-Ozkurt | 0.5 | 0.15 | 3 | 15 | 3 | 0 | 25 | 3.449 / 3.668 | 13.76 / 8 | 9 / 0 | — |
| A1 | KLMI-scan | 0.5 | 0.15 | 3 | 16 | 3 | 0 | 25 | 3.136 / 3.552 | 11.84 / 8 | 7 / 0 | — |
| A1 | GLM-scan | 0.5 | 0.15 | 1 | 11 | 1 | 0 | 25 | 3.4 / 3.589 | 16 / 16 | 8 / 0 | — |
| v1.0 | APC | NaN | 0.5 | 16 | 16 | 25 | 16 | 25 | 0.03862 / 0.03719 | 8.84 / 6 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 0.5 | 15 | 15 | 25 | 15 | 25 | 0.1268 / 0.1206 | 9 / 6 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 0.5 | 6 | 24 | 6 | 2 | 25 | 3.103 / 3.031 | 1.28 / 0 | 10 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 0.5 | 5 | 14 | 5 | 2 | 25 | 3.343 / 3.34 | 12.8 / 8 | 15 / 0 | — |
| A0 | KLMI-scan | 1 | 0.5 | 3 | 13 | 3 | 1 | 25 | 3.573 / 3.62 | 13.76 / 8 | 19 / 0 | — |
| A0 | GLM-scan | 1 | 0.5 | 3 | 13 | 3 | 1 | 25 | 3.293 / 3.12 | 13.76 / 8 | 15 / 0 | — |
| A1 | MVL-raw | 1 | 0.5 | 12 | 25 | 12 | 0 | 25 | 1.11 / 1.147 | 0.32 / 0 | 0 / 1 | — |
| A1 | MVL-Ozkurt | 1 | 0.5 | 12 | 22 | 12 | 3 | 25 | 1.79 / 1.147 | 4.16 / 0 | 3 / 0 | — |
| A1 | KLMI-scan | 1 | 0.5 | 7 | 21 | 8 | 0 | 25 | 2.189 / 1.228 | 5.44 / 0 | 5 / 0 | — |
| A1 | GLM-scan | 1 | 0.5 | 6 | 22 | 7 | 1 | 25 | 2.271 / 1.371 | 5.44 / 0 | 5 / 0 | — |
| A0 | MVL-raw | 0.5 | 0.5 | 5 | 25 | 5 | 1 | 25 | 3.213 / 3.129 | 1.28 / 0 | 5 / 0 | — |
| A0 | MVL-Ozkurt | 0.5 | 0.5 | 5 | 16 | 5 | 1 | 25 | 3.293 / 3.129 | 10.56 / 8 | 8 / 0 | — |
| A0 | KLMI-scan | 0.5 | 0.5 | 3 | 13 | 3 | 1 | 25 | 3.473 / 3.242 | 11.52 / 8 | 14 / 0 | — |
| A0 | GLM-scan | 0.5 | 0.5 | 3 | 14 | 3 | 2 | 25 | 3.233 / 3.12 | 12.16 / 8 | 13 / 0 | — |
| A1 | MVL-raw | 0.5 | 0.5 | 3 | 25 | 3 | 0 | 25 | 1.43 / 1.228 | 0.64 / 0 | 0 / 1 | — |
| A1 | MVL-Ozkurt | 0.5 | 0.5 | 3 | 22 | 3 | 1 | 25 | 1.98 / 1.258 | 3.2 / 0 | 1 / 0 | — |
| A1 | KLMI-scan | 0.5 | 0.5 | 3 | 22 | 3 | 1 | 25 | 2.092 / 1.228 | 4.48 / 0 | 3 / 0 | — |
| A1 | GLM-scan | 0.5 | 0.5 | 3 | 22 | 3 | 0 | 25 | 2.381 / 1.258 | 4.48 / 0 | 4 / 0 | — |
| v1.0 | APC | NaN | 1 | 23 | 23 | 25 | 23 | 25 | 0.04831 / 0.0325 | 4.84 / 4 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 1 | 23 | 23 | 25 | 23 | 25 | 0.1001 / 0.08428 | 5.2 / 4 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 1 | 8 | 24 | 8 | 2 | 25 | 2.746 / 2.447 | 2.24 / 0 | 7 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 1 | 7 | 14 | 7 | 1 | 25 | 3.047 / 3.647 | 14.08 / 8 | 10 / 0 | — |
| A0 | KLMI-scan | 1 | 1 | 6 | 15 | 6 | 2 | 25 | 3.357 / 3.885 | 13.76 / 8 | 12 / 0 | — |
| A0 | GLM-scan | 1 | 1 | 6 | 15 | 6 | 2 | 25 | 3.117 / 3.647 | 12.48 / 8 | 8 / 0 | — |
| A1 | MVL-raw | 1 | 1 | 9 | 25 | 9 | 0 | 25 | 1.111 / 1.127 | 0 / 0 | 0 / 3 | — |
| A1 | MVL-Ozkurt | 1 | 1 | 8 | 22 | 8 | 3 | 25 | 1.717 / 1.167 | 7.04 / 0 | 3 / 1 | — |
| A1 | KLMI-scan | 1 | 1 | 7 | 20 | 7 | 3 | 25 | 1.891 / 1.189 | 8.32 / 0 | 2 / 0 | — |
| A1 | GLM-scan | 1 | 1 | 10 | 24 | 10 | 1 | 25 | 1.354 / 1.122 | 1.92 / 0 | 1 / 1 | — |
| A0 | MVL-raw | 0.5 | 1 | 7 | 23 | 7 | 2 | 25 | 2.866 / 2.447 | 2.88 / 0 | 7 / 0 | — |
| A0 | MVL-Ozkurt | 0.5 | 1 | 4 | 13 | 4 | 2 | 25 | 3.107 / 3.722 | 14.4 / 8 | 8 / 0 | — |
| A0 | KLMI-scan | 0.5 | 1 | 4 | 13 | 4 | 2 | 25 | 3.453 / 4.017 | 14.72 / 8 | 9 / 0 | — |
| A0 | GLM-scan | 0.5 | 1 | 6 | 13 | 6 | 2 | 25 | 3.026 / 3.885 | 13.76 / 8 | 5 / 0 | — |
| A1 | MVL-raw | 0.5 | 1 | 2 | 25 | 2 | 0 | 25 | 1.231 / 1.19 | 0 / 0 | 0 / 2 | — |
| A1 | MVL-Ozkurt | 0.5 | 1 | 5 | 22 | 5 | 1 | 25 | 1.577 / 1.128 | 7.04 / 0 | 2 / 1 | — |
| A1 | KLMI-scan | 0.5 | 1 | 5 | 20 | 5 | 1 | 25 | 1.956 / 1.226 | 8 / 0 | 2 / 0 | — |
| A1 | GLM-scan | 0.5 | 1 | 2 | 24 | 2 | 0 | 25 | 1.528 / 1.178 | 1.6 / 0 | 1 / 1 | — |

### Distractor

| Configuration | Method | fP grid Hz | Level | Joint /25 | fA /25 | fP /25 | Joint .5Hz /25 | Valid /25 | fP error mean / median Hz | fA error mean / median Hz | fP=4 /12 | Direct /TF /other |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v1.0 | APC | NaN | 0 | 23 | 23 | 25 | 23 | 25 | 0.03442 / 0.02484 | 4.2 / 3 | 0 / 0 | 25 / 0 / 0 |
| v1.0_no_fP_refine | APC | NaN | 0 | 23 | 23 | 25 | 23 | 25 | 0.1316 / 0.1242 | 4.72 / 4 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 0 | 10 | 23 | 10 | 5 | 25 | 2.516 / 2.169 | 3.52 / 0 | 8 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 0 | 9 | 12 | 9 | 4 | 25 | 2.492 / 2.552 | 14.72 / 16 | 6 / 0 | — |
| A0 | KLMI-scan | 1 | 0 | 6 | 8 | 6 | 4 | 25 | 3.136 / 3.259 | 18.88 / 24 | 12 / 0 | — |
| A0 | GLM-scan | 1 | 0 | 9 | 14 | 9 | 5 | 25 | 2.84 / 3.186 | 13.44 / 8 | 8 / 0 | — |
| A1 | MVL-raw | 1 | 0 | 11 | 25 | 11 | 0 | 25 | 1.127 / 1.332 | 0.64 / 0 | 0 / 0 | — |
| A1 | MVL-Ozkurt | 1 | 0 | 13 | 24 | 13 | 5 | 25 | 1.24 / 0.9414 | 3.2 / 0 | 0 / 0 | — |
| A1 | KLMI-scan | 1 | 0 | 11 | 23 | 11 | 5 | 25 | 1.319 / 1.186 | 5.44 / 0 | 1 / 0 | — |
| A1 | GLM-scan | 1 | 0 | 14 | 24 | 14 | 6 | 25 | 1.078 / 0.7874 | 2.88 / 0 | 0 / 0 | — |
| A0 | MVL-raw | 0.5 | 0 | 6 | 24 | 6 | 2 | 25 | 2.759 / 2.552 | 1.6 / 0 | 4 / 0 | — |
| A0 | MVL-Ozkurt | 0.5 | 0 | 7 | 11 | 7 | 3 | 25 | 2.572 / 2.552 | 15.36 / 16 | 3 / 0 | — |
| A0 | KLMI-scan | 0.5 | 0 | 4 | 8 | 4 | 3 | 25 | 3.004 / 3.213 | 18.24 / 16 | 8 / 0 | — |
| A0 | GLM-scan | 0.5 | 0 | 7 | 14 | 7 | 4 | 25 | 2.801 / 3.186 | 12.8 / 8 | 5 / 0 | — |
| A1 | MVL-raw | 0.5 | 0 | 2 | 25 | 2 | 0 | 25 | 1.227 / 1.259 | 0 / 0 | 0 / 0 | — |
| A1 | MVL-Ozkurt | 0.5 | 0 | 7 | 24 | 7 | 2 | 25 | 1.4 / 1.186 | 3.52 / 0 | 0 / 0 | — |
| A1 | KLMI-scan | 0.5 | 0 | 7 | 22 | 7 | 2 | 25 | 1.524 / 1.151 | 5.76 / 0 | 1 / 0 | — |
| A1 | GLM-scan | 0.5 | 0 | 7 | 24 | 7 | 3 | 25 | 1.238 / 1.138 | 2.88 / 0 | 0 / 0 | — |
| v1.0 | APC | NaN | 1.5 | 18 | 18 | 21 | 18 | 21 | 0.05376 / 0.03725 | 5.333 / 3 | 0 / 0 | 21 / 0 / 4 |
| v1.0_no_fP_refine | APC | NaN | 1.5 | 18 | 18 | 21 | 18 | 25 | 1.023 / 0.1582 | 8.12 / 3 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 1.5 | 9 | 15 | 9 | 4 | 25 | 2.963 / 3.62 | 10.24 / 8 | 11 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 1.5 | 8 | 16 | 8 | 2 | 25 | 2.833 / 3.242 | 10.88 / 8 | 10 / 0 | — |
| A0 | KLMI-scan | 1 | 1.5 | 6 | 14 | 7 | 1 | 25 | 3.127 / 3.439 | 13.12 / 8 | 12 / 0 | — |
| A0 | GLM-scan | 1 | 1.5 | 6 | 16 | 7 | 2 | 25 | 2.938 / 3.439 | 9.92 / 8 | 10 / 0 | — |
| A1 | MVL-raw | 1 | 1.5 | 12 | 25 | 12 | 1 | 25 | 1.033 / 1.034 | 0.32 / 0 | 0 / 2 | — |
| A1 | MVL-Ozkurt | 1 | 1.5 | 13 | 23 | 13 | 4 | 25 | 1.534 / 0.9719 | 4.16 / 0 | 2 / 0 | — |
| A1 | KLMI-scan | 1 | 1.5 | 10 | 22 | 10 | 2 | 25 | 1.842 / 1.227 | 5.44 / 0 | 3 / 1 | — |
| A1 | GLM-scan | 1 | 1.5 | 12 | 24 | 12 | 3 | 25 | 1.575 / 1.147 | 1.92 / 0 | 2 / 1 | — |
| A0 | MVL-raw | 0.5 | 1.5 | 9 | 16 | 9 | 3 | 25 | 2.895 / 3.439 | 9.6 / 0 | 7 / 0 | — |
| A0 | MVL-Ozkurt | 0.5 | 1.5 | 8 | 15 | 8 | 1 | 25 | 2.743 / 2.853 | 12.16 / 8 | 8 / 0 | — |
| A0 | KLMI-scan | 0.5 | 1.5 | 6 | 14 | 6 | 0 | 25 | 2.947 / 2.281 | 13.44 / 8 | 9 / 0 | — |
| A0 | GLM-scan | 0.5 | 1.5 | 6 | 15 | 6 | 0 | 25 | 2.838 / 2.281 | 10.88 / 8 | 8 / 0 | — |
| A1 | MVL-raw | 0.5 | 1.5 | 10 | 25 | 10 | 1 | 25 | 1.073 / 1.127 | 0.64 / 0 | 0 / 0 | — |
| A1 | MVL-Ozkurt | 0.5 | 1.5 | 10 | 23 | 10 | 2 | 25 | 1.654 / 1.127 | 3.84 / 0 | 2 / 0 | — |
| A1 | KLMI-scan | 0.5 | 1.5 | 10 | 22 | 10 | 2 | 25 | 1.822 / 1.127 | 5.12 / 0 | 3 / 0 | — |
| A1 | GLM-scan | 0.5 | 1.5 | 11 | 24 | 11 | 2 | 25 | 1.597 / 1.088 | 1.6 / 0 | 2 / 0 | — |
| v1.0 | APC | NaN | 3 | 17 | 17 | 20 | 17 | 21 | 0.2777 / 0.05429 | 8.333 / 4 | 0 / 0 | 21 / 0 / 4 |
| v1.0_no_fP_refine | APC | NaN | 3 | 20 | 20 | 22 | 19 | 25 | 0.8581 / 0.09034 | 9.24 / 5 | 0 / 0 | 25 / 0 / 0 |
| A0 | MVL-raw | 1 | 3 | 5 | 8 | 5 | 3 | 25 | 3.278 / 3.447 | 16.96 / 24 | 9 / 0 | — |
| A0 | MVL-Ozkurt | 1 | 3 | 7 | 12 | 7 | 3 | 25 | 2.98 / 3.037 | 14.08 / 16 | 8 / 0 | — |
| A0 | KLMI-scan | 1 | 3 | 5 | 9 | 5 | 4 | 25 | 3.34 / 3.774 | 17.6 / 16 | 12 / 0 | — |
| A0 | GLM-scan | 1 | 3 | 6 | 14 | 6 | 5 | 25 | 3.194 / 3.873 | 13.76 / 8 | 9 / 0 | — |
| A1 | MVL-raw | 1 | 3 | 13 | 24 | 13 | 1 | 25 | 1.087 / 0.9834 | 1.92 / 0 | 0 / 1 | — |
| A1 | MVL-Ozkurt | 1 | 3 | 11 | 21 | 11 | 4 | 25 | 1.647 / 1.122 | 5.76 / 0 | 2 / 1 | — |
| A1 | KLMI-scan | 1 | 3 | 11 | 20 | 11 | 4 | 25 | 1.901 / 1.122 | 8 / 8 | 4 / 0 | — |
| A1 | GLM-scan | 1 | 3 | 12 | 23 | 12 | 3 | 25 | 1.27 / 1.093 | 3.2 / 0 | 0 / 1 | — |
| A0 | MVL-raw | 0.5 | 3 | 4 | 9 | 4 | 3 | 25 | 3.307 / 3.447 | 15.36 / 24 | 7 / 0 | — |
| A0 | MVL-Ozkurt | 0.5 | 3 | 4 | 13 | 4 | 3 | 25 | 3.009 / 3.037 | 14.08 / 8 | 5 / 0 | — |
| A0 | KLMI-scan | 0.5 | 3 | 4 | 10 | 4 | 2 | 25 | 3.29 / 3.774 | 17.28 / 16 | 6 / 0 | — |
| A0 | GLM-scan | 0.5 | 3 | 5 | 15 | 5 | 4 | 25 | 3.284 / 3.81 | 11.52 / 8 | 5 / 0 | — |
| A1 | MVL-raw | 0.5 | 3 | 3 | 23 | 3 | 2 | 25 | 1.287 / 1.158 | 2.56 / 0 | 0 / 1 | — |
| A1 | MVL-Ozkurt | 0.5 | 3 | 7 | 21 | 7 | 2 | 25 | 1.764 / 1.127 | 5.44 / 0 | 2 / 1 | — |
| A1 | KLMI-scan | 0.5 | 3 | 6 | 21 | 6 | 4 | 25 | 1.864 / 1.167 | 7.36 / 0 | 3 / 0 | — |
| A1 | GLM-scan | 0.5 | 3 | 4 | 23 | 4 | 1 | 25 | 1.454 / 1.128 | 2.56 / 0 | 0 / 1 | — |

## Null specificity and AUC

Timing nulls retain coupling strength .60 and the original true-burst amplitude and sigma; only true-burst timing changes. Homogeneous Poisson events use the specified mean rates and original event support, on a separate RNG stream. Gaussian sums allow overlaps; no 56-ms gap was imposed. Carrier, background, distractor and the original noise samples/scale are shared exactly. The no-coupled-burst control removes only the true component and is reported separately. [null_pair_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/null_pair_verification.json>) contains all 350 pairing checks; maximum timing-null residual is 8.882e-16.

False joint recovery uses fP within 1 Hz of 8 and fA within 8 Hz of 120. AUC compares all coupled/null score pairs with one half for ties; higher scores retain the original direction. Finite sample counts are reported. Raw null rows: [null_trials.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/null_trials.csv>); recovery summaries: [null_recovery_summary.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/null_recovery_summary.csv>); specificity/AUC: [null_specificity_auc.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/null_specificity_auc.csv>).

### timing_null

| Benchmark | Level | Configuration | Method | False joint /25 | AUC | Finite coupled/null |
| --- | --- | --- | --- | --- | --- | --- |
| sparsity | 1 | v1.0 | APC | 3 | 0.944 | 25/25 |
| sparsity | 1 | A1 | MVL-raw | 0 | 1 | 25/25 |
| sparsity | 1 | A1 | MVL-Ozkurt | 0 | 0.9968 | 25/25 |
| sparsity | 1 | A1 | KLMI-scan | 0 | 0.9952 | 25/25 |
| sparsity | 1 | A1 | GLM-scan | 0 | 1 | 25/25 |
| sparsity | 0.85 | v1.0 | APC | 9 | 0.8672 | 25/25 |
| sparsity | 0.85 | A1 | MVL-raw | 3 | 1 | 25/25 |
| sparsity | 0.85 | A1 | MVL-Ozkurt | 1 | 0.976 | 25/25 |
| sparsity | 0.85 | A1 | KLMI-scan | 0 | 0.984 | 25/25 |
| sparsity | 0.85 | A1 | GLM-scan | 0 | 1 | 25/25 |
| sparsity | 0.7 | v1.0 | APC | 6 | 0.8432 | 25/25 |
| sparsity | 0.7 | A1 | MVL-raw | 2 | 1 | 25/25 |
| sparsity | 0.7 | A1 | MVL-Ozkurt | 0 | 0.9904 | 25/25 |
| sparsity | 0.7 | A1 | KLMI-scan | 0 | 0.9744 | 25/25 |
| sparsity | 0.7 | A1 | GLM-scan | 0 | 0.9728 | 25/25 |
| sparsity | 0.55 | v1.0 | APC | 7 | 0.8576 | 25/25 |
| sparsity | 0.55 | A1 | MVL-raw | 2 | 1 | 25/25 |
| sparsity | 0.55 | A1 | MVL-Ozkurt | 0 | 0.8848 | 25/25 |
| sparsity | 0.55 | A1 | KLMI-scan | 0 | 0.856 | 25/25 |
| sparsity | 0.55 | A1 | GLM-scan | 0 | 0.864 | 25/25 |
| sparsity | 0.4 | v1.0 | APC | 7 | 0.8992 | 25/25 |
| sparsity | 0.4 | A1 | MVL-raw | 1 | 0.9904 | 25/25 |
| sparsity | 0.4 | A1 | MVL-Ozkurt | 0 | 0.7168 | 25/25 |
| sparsity | 0.4 | A1 | KLMI-scan | 1 | 0.744 | 25/25 |
| sparsity | 0.4 | A1 | GLM-scan | 1 | 0.696 | 25/25 |
| sparsity | 0.25 | v1.0 | APC | 6 | 0.8336 | 25/25 |
| sparsity | 0.25 | A1 | MVL-raw | 0 | 0.896 | 25/25 |
| sparsity | 0.25 | A1 | MVL-Ozkurt | 0 | 0.5568 | 25/25 |
| sparsity | 0.25 | A1 | KLMI-scan | 0 | 0.5648 | 25/25 |
| sparsity | 0.25 | A1 | GLM-scan | 0 | 0.52 | 25/25 |
| sparsity | 0.15 | v1.0 | APC | 12 | 0.656 | 25/25 |
| sparsity | 0.15 | A1 | MVL-raw | 2 | 0.7552 | 25/25 |
| sparsity | 0.15 | A1 | MVL-Ozkurt | 0 | 0.4848 | 25/25 |
| sparsity | 0.15 | A1 | KLMI-scan | 0 | 0.5392 | 25/25 |
| sparsity | 0.15 | A1 | GLM-scan | 0 | 0.48 | 25/25 |
| distractor | 0 | v1.0 | APC | 4 | 0.9183 | 24/25 |
| distractor | 0 | A1 | MVL-raw | 3 | 1 | 25/25 |
| distractor | 0 | A1 | MVL-Ozkurt | 0 | 0.9984 | 25/25 |
| distractor | 0 | A1 | KLMI-scan | 0 | 0.992 | 25/25 |
| distractor | 0 | A1 | GLM-scan | 0 | 1 | 25/25 |
| distractor | 0.5 | v1.0 | APC | 7 | 0.9552 | 25/25 |
| distractor | 0.5 | A1 | MVL-raw | 6 | 1 | 25/25 |
| distractor | 0.5 | A1 | MVL-Ozkurt | 0 | 0.9968 | 25/25 |
| distractor | 0.5 | A1 | KLMI-scan | 1 | 0.984 | 25/25 |
| distractor | 0.5 | A1 | GLM-scan | 0 | 1 | 25/25 |
| distractor | 1 | v1.0 | APC | 6 | 0.9904 | 25/25 |
| distractor | 1 | A1 | MVL-raw | 0 | 1 | 25/25 |
| distractor | 1 | A1 | MVL-Ozkurt | 0 | 0.9776 | 25/25 |
| distractor | 1 | A1 | KLMI-scan | 0 | 0.9632 | 25/25 |
| distractor | 1 | A1 | GLM-scan | 0 | 1 | 25/25 |
| distractor | 1.5 | v1.0 | APC | 4 | 0.953 | 23/25 |
| distractor | 1.5 | A1 | MVL-raw | 2 | 1 | 25/25 |
| distractor | 1.5 | A1 | MVL-Ozkurt | 0 | 0.9952 | 25/25 |
| distractor | 1.5 | A1 | KLMI-scan | 0 | 0.9984 | 25/25 |
| distractor | 1.5 | A1 | GLM-scan | 0 | 1 | 25/25 |
| distractor | 2 | v1.0 | APC | 6 | 0.9849 | 23/23 |
| distractor | 2 | A1 | MVL-raw | 0 | 1 | 25/25 |
| distractor | 2 | A1 | MVL-Ozkurt | 0 | 0.9968 | 25/25 |
| distractor | 2 | A1 | KLMI-scan | 0 | 0.9872 | 25/25 |
| distractor | 2 | A1 | GLM-scan | 0 | 1 | 25/25 |
| distractor | 2.5 | v1.0 | APC | 5 | 0.9444 | 21/18 |
| distractor | 2.5 | A1 | MVL-raw | 0 | 0.9984 | 25/25 |
| distractor | 2.5 | A1 | MVL-Ozkurt | 0 | 0.984 | 25/25 |
| distractor | 2.5 | A1 | KLMI-scan | 0 | 1 | 25/25 |
| distractor | 2.5 | A1 | GLM-scan | 0 | 1 | 25/25 |
| distractor | 3 | v1.0 | APC | 1 | 0.8929 | 21/20 |
| distractor | 3 | A1 | MVL-raw | 0 | 0.992 | 25/25 |
| distractor | 3 | A1 | MVL-Ozkurt | 0 | 0.968 | 25/25 |
| distractor | 3 | A1 | KLMI-scan | 0 | 0.9408 | 25/25 |
| distractor | 3 | A1 | GLM-scan | 0 | 0.9936 | 25/25 |

### no_coupled_burst

| Benchmark | Level | Configuration | Method | False joint /25 | AUC | Finite coupled/null |
| --- | --- | --- | --- | --- | --- | --- |
| sparsity | 1 | v1.0 | APC | 5 | 0.9408 | 25/25 |
| sparsity | 1 | A1 | MVL-raw | 0 | 1 | 25/25 |
| sparsity | 1 | A1 | MVL-Ozkurt | 0 | 1 | 25/25 |
| sparsity | 1 | A1 | KLMI-scan | 0 | 0.9952 | 25/25 |
| sparsity | 1 | A1 | GLM-scan | 1 | 1 | 25/25 |
| sparsity | 0.85 | v1.0 | APC | 10 | 0.8672 | 25/25 |
| sparsity | 0.85 | A1 | MVL-raw | 4 | 1 | 25/25 |
| sparsity | 0.85 | A1 | MVL-Ozkurt | 1 | 0.9792 | 25/25 |
| sparsity | 0.85 | A1 | KLMI-scan | 1 | 0.9792 | 25/25 |
| sparsity | 0.85 | A1 | GLM-scan | 1 | 0.9984 | 25/25 |
| sparsity | 0.7 | v1.0 | APC | 10 | 0.8576 | 25/25 |
| sparsity | 0.7 | A1 | MVL-raw | 1 | 1 | 25/25 |
| sparsity | 0.7 | A1 | MVL-Ozkurt | 1 | 0.9904 | 25/25 |
| sparsity | 0.7 | A1 | KLMI-scan | 0 | 0.9776 | 25/25 |
| sparsity | 0.7 | A1 | GLM-scan | 0 | 0.9744 | 25/25 |
| sparsity | 0.55 | v1.0 | APC | 4 | 0.88 | 25/25 |
| sparsity | 0.55 | A1 | MVL-raw | 2 | 1 | 25/25 |
| sparsity | 0.55 | A1 | MVL-Ozkurt | 0 | 0.8848 | 25/25 |
| sparsity | 0.55 | A1 | KLMI-scan | 0 | 0.8912 | 25/25 |
| sparsity | 0.55 | A1 | GLM-scan | 0 | 0.8912 | 25/25 |
| sparsity | 0.4 | v1.0 | APC | 7 | 0.912 | 25/25 |
| sparsity | 0.4 | A1 | MVL-raw | 2 | 1 | 25/25 |
| sparsity | 0.4 | A1 | MVL-Ozkurt | 0 | 0.7024 | 25/25 |
| sparsity | 0.4 | A1 | KLMI-scan | 0 | 0.7312 | 25/25 |
| sparsity | 0.4 | A1 | GLM-scan | 0 | 0.5984 | 25/25 |
| sparsity | 0.25 | v1.0 | APC | 7 | 0.8352 | 25/25 |
| sparsity | 0.25 | A1 | MVL-raw | 3 | 0.9472 | 25/25 |
| sparsity | 0.25 | A1 | MVL-Ozkurt | 1 | 0.5888 | 25/25 |
| sparsity | 0.25 | A1 | KLMI-scan | 0 | 0.5696 | 25/25 |
| sparsity | 0.25 | A1 | GLM-scan | 0 | 0.4896 | 25/25 |
| sparsity | 0.15 | v1.0 | APC | 11 | 0.7072 | 25/25 |
| sparsity | 0.15 | A1 | MVL-raw | 1 | 0.8528 | 25/25 |
| sparsity | 0.15 | A1 | MVL-Ozkurt | 0 | 0.4784 | 25/25 |
| sparsity | 0.15 | A1 | KLMI-scan | 0 | 0.5104 | 25/25 |
| sparsity | 0.15 | A1 | GLM-scan | 0 | 0.4 | 25/25 |
| distractor | 0 | v1.0 | APC | 6 | 0.9117 | 24/25 |
| distractor | 0 | A1 | MVL-raw | 0 | 1 | 25/25 |
| distractor | 0 | A1 | MVL-Ozkurt | 0 | 0.9984 | 25/25 |
| distractor | 0 | A1 | KLMI-scan | 0 | 0.9952 | 25/25 |
| distractor | 0 | A1 | GLM-scan | 0 | 1 | 25/25 |
| distractor | 0.5 | v1.0 | APC | 6 | 0.9568 | 25/25 |
| distractor | 0.5 | A1 | MVL-raw | 0 | 1 | 25/25 |
| distractor | 0.5 | A1 | MVL-Ozkurt | 1 | 0.9968 | 25/25 |
| distractor | 0.5 | A1 | KLMI-scan | 0 | 0.9936 | 25/25 |
| distractor | 0.5 | A1 | GLM-scan | 0 | 1 | 25/25 |
| distractor | 1 | v1.0 | APC | 4 | 0.9936 | 25/25 |
| distractor | 1 | A1 | MVL-raw | 0 | 1 | 25/25 |
| distractor | 1 | A1 | MVL-Ozkurt | 0 | 0.9872 | 25/25 |
| distractor | 1 | A1 | KLMI-scan | 0 | 0.9632 | 25/25 |
| distractor | 1 | A1 | GLM-scan | 0 | 1 | 25/25 |
| distractor | 1.5 | v1.0 | APC | 6 | 0.9513 | 23/25 |
| distractor | 1.5 | A1 | MVL-raw | 0 | 1 | 25/25 |
| distractor | 1.5 | A1 | MVL-Ozkurt | 1 | 0.9936 | 25/25 |
| distractor | 1.5 | A1 | KLMI-scan | 1 | 1 | 25/25 |
| distractor | 1.5 | A1 | GLM-scan | 1 | 1 | 25/25 |
| distractor | 2 | v1.0 | APC | 3 | 0.9849 | 23/23 |
| distractor | 2 | A1 | MVL-raw | 0 | 1 | 25/25 |
| distractor | 2 | A1 | MVL-Ozkurt | 0 | 0.9888 | 25/25 |
| distractor | 2 | A1 | KLMI-scan | 0 | 0.9856 | 25/25 |
| distractor | 2 | A1 | GLM-scan | 0 | 1 | 25/25 |
| distractor | 2.5 | v1.0 | APC | 3 | 0.9524 | 21/21 |
| distractor | 2.5 | A1 | MVL-raw | 0 | 0.9984 | 25/25 |
| distractor | 2.5 | A1 | MVL-Ozkurt | 1 | 0.9904 | 25/25 |
| distractor | 2.5 | A1 | KLMI-scan | 1 | 0.9968 | 25/25 |
| distractor | 2.5 | A1 | GLM-scan | 1 | 1 | 25/25 |
| distractor | 3 | v1.0 | APC | 1 | 0.8853 | 21/22 |
| distractor | 3 | A1 | MVL-raw | 0 | 0.9936 | 25/25 |
| distractor | 3 | A1 | MVL-Ozkurt | 0 | 0.9504 | 25/25 |
| distractor | 3 | A1 | KLMI-scan | 0 | 0.9376 | 25/25 |
| distractor | 3 | A1 | GLM-scan | 0 | 0.992 | 25/25 |

## Runtime and deviations

| Stage | Elapsed seconds | Status |
| --- | --- | --- |
| sanity | 26.2 | COMPLETE |
| smoke | 2.399 | COMPLETE |
| main | 217.3 | COMPLETE |
| random_fp | 337.6 | COMPLETE |
| null | 734.2 | COMPLETE |
| figures | 35.19 | COMPLETE |

Measured MATLAB elapsed time totals 1353 seconds, including sanity and figure creation; it excludes MATLAB startup, implementation and report assembly. One computation thread was used.

Tooling deviations: the earlier pre-commit Python read used Windows cp1252 and failed on byte 0x9d, a byte in a UTF-8 right curly quote in build_results.py (offsets 11611 and 11629 in the original file). The resumed workflow uses explicit UTF-8 text I/O. All repository MATLAB sources were verified ASCII; none required character replacement. The earlier stopped report and pre-commit check files were preserved. The committed sanity and smoke records use a separate committed_checks directory. Encoding audit: [encoding_audit.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/encoding_audit.json>).

The null definition follows the user’s replacement instruction: the timing null is primary and the zero-amplitude control is secondary. No trial counts, generators, seeds, level order or frozen method settings were changed after tagging. Legacy filters cache immutable design objects; continuously varying v1 carrier bands use the same fourth-order Butterworth family through direct SOS construction. The stated Welch/log-parabolic refinement, independent normalized-MVL scan, Poisson edge support and invalid-output handling were documented before tagging. Further tooling deviations, if any, are recorded in [tooling_deviations.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/tooling_deviations.json>). Original result hashes were rechecked in [original_results_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/original_results_verification.json>).

Additional rendering deviations: the committed figure function's automatic CSV import did not recognize the benchmark column. An external renderer with an explicit comma-delimited UTF-8 import then resolved the table, but its first launch omitted the frozen v1_options helper path. The successful renderer adds that helper path and reads the 14 native main MAT tables (4,200 rows), verifies their frozen commit, and uses the unchanged recovery-count and plot calculations. No benchmark was rerun and no tagged source or trial data was changed. The renderer and launcher are [render_frozen_figures.m](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/render_frozen_figures.m>) and [run_fixed_figures.m](<C:/Users/nghare/.brainstorm/process/revision_checks/v1_rerun/run_fixed_figures.m>). Both failed logs are preserved as frozen_suite_matlab.log and fixed_figures_matlab.log; the successful log is fixed_figures2_matlab.log.

The runtime total above covers successful frozen stages only. The initial failed figure-import attempt additionally recorded 13.736523 seconds; the subsequent standalone helper-path failure did not record elapsed computation time. These failed attempts, the earlier pre-commit sanity attempt, and MATLAB startups are excluded from that total.

SVG metadata deviation: MATLAB exports the closing svg tag across a newline, so the original literal closing-tag replacement did not insert provenance. Full metadata was inserted before that closing tag with a whitespace-tolerant match; no SVG graphics were changed.

## Full result provenance

Every trial and summary CSV stores the commit, MATLAB version, complete APC option inputs, full comparator settings and seed. MAT checkpoints contain metadata plus input cases/components. PNG text, SVG metadata and MATLAB figure UserData embed provenance. The complete metadata record used for these results follows.

```json
{
  "git_commit": "71ebc16aed32ca38be73a800738b975e5806b330",
  "git_tag": "v1.0",
  "matlab_version": "9.13.0.2105380 (R2022b) Update 2",
  "matlab_release": "2022b",
  "seed": 20260618.0,
  "computation_threads": 1,
  "worktree_dirty": false,
  "stage": "main",
  "apc_source_git_blob": "04675a5d7acfe82b1e46431e5838e56ef056eab6",
  "apc_configurations": [
    {
      "name": "v1.0",
      "options": {
        "fA": [
          80,
          150
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
        "fPMaxBinSpacingHz": 0.05
      }
    },
    {
      "name": "oct2026",
      "options": {
        "fA": [
          80,
          150
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
        "stepFourMode": "oct2026",
        "fPRefine": false,
        "fPMaxBinSpacingHz": 0.05
      }
    },
    {
      "name": "june2026_clipped",
      "options": {
        "fA": [
          80,
          150
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
        "stepFourMode": "june2026_clipped",
        "fPRefine": false,
        "fPMaxBinSpacingHz": 0.05
      }
    },
    {
      "name": "v1.0_no_fP_refine",
      "options": {
        "fA": [
          80,
          150
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
        "fPRefine": false,
        "fPMaxBinSpacingHz": 0.05
      }
    }
  ],
  "comparator_settings": {
    "phase_half_width_hz": 1.5,
    "phase_grids": {
      "main": [
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
      "random_1Hz": [
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
      "random_05Hz": [
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
        12
      ]
    },
    "amplitude_grid_hz": [
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
    "A0_amplitude_half_width_hz": 6,
    "A1_amplitude_half_width": "candidate fP",
    "amplitude_clipping_hz": "[max(1,fA-halfWidth),min(fs/2-1,fA+halfWidth)]",
    "filter": "butter(4,[low high]/(fs/2),bandpass), filtfilt (8th-order bandpass)",
    "normalized_cutoff_clamps": [
      0.0001,
      0.999
    ],
    "phase_low_edge_min_hz": 0.5,
    "metrics": [
      "MVL-raw",
      "MVL-Ozkurt",
      "KLMI-scan",
      "GLM-scan"
    ],
    "num_phase_bins": 18,
    "raw_MVL": "abs(mean(A.*exp(1i*phase)))",
    "Ozkurt_MVL": "abs(sum(A.*exp(1i*phase)))/sqrt(N*sum(A.^2))",
    "GLM": "max(0,1-SSE/SST); X=[ones,sin(phase),cos(phase)]",
    "selection": "independent full-grid argmax for each metric; MATLAB column-major first tie",
    "surrogates": false
  },
  "null_settings": {
    "primary": "timing_null",
    "secondary": "no_coupled_burst",
    "timing_null_coupling_level": 0.6,
    "poisson_stream": "mt19937ar, separate stream seeded 20260618, reset per benchmark",
    "poisson_rate_distractor": "true fP Hz",
    "poisson_rate_sparsity": "keep_rate * true fP Hz",
    "event_support": "[t(1)-1/fP,t(end)+1/fP], original generator event support; original APC epoch-edge rejection unchanged",
    "overlap": "allowed; original Gaussian envelope sum handles overlap; no minimum gap",
    "envelope_normalization": "divide by maximum on recording, same as original generator",
    "paired_components": "same carrier, noise vector including original noise scale, distractor and background; only true-burst component replaced",
    "verification_tolerance": 1e-12,
    "secondary_coupling_level": 0
  },
  "random_fp_settings": {
    "distribution": "uniform[5,11] Hz",
    "stream": "separate mt19937ar stream seed 20260618, reset per benchmark",
    "distractor_levels": [
      0,
      1.5,
      3
    ],
    "sparsity_levels": [
      0.15,
      0.5,
      1
    ],
    "repeats": 25
  },
  "generator_settings": {
    "sparsity": {
      "profile_name": "full",
      "random_seed": 20260618.0,
      "fs_hz": 500,
      "duration_s": 8,
      "true_fp_hz": 8,
      "true_fa_hz": 120,
      "phase_offset_deg": -90,
      "low_amp": 1,
      "true_high_amp": 1.3,
      "base_hf_amp": 0.08,
      "burst_sigma_s": 0.028,
      "burst_phase_jitter_s": 0.01,
      "snr_db": -3,
      "broad_fa_band_hz": [
        80,
        150
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
      "metric": "canolty",
      "fa_tolerance_hz": 8,
      "fp_tolerance_hz": 1,
      "coupling_level": 0.6,
      "background_burst_scale": 0.18,
      "n_repeats": 25,
      "burst_keep_rates": [
        1,
        0.85,
        0.7,
        0.55,
        0.4,
        0.25,
        0.15
      ]
    },
    "distractor": {
      "profile_name": "reviewer_control",
      "random_seed": 20260618.0,
      "fs_hz": 500,
      "duration_s": 6,
      "true_fp_hz": 8,
      "true_fa_hz": 120,
      "distractor_fa_hz": 96,
      "phase_offset_deg": -90,
      "low_amp": 1,
      "true_high_amp": 1.3,
      "distractor_base_amp": 0.6,
      "base_hf_amp": 0.08,
      "burst_sigma_s": 0.028,
      "coupling_level": 0.6,
      "burst_phase_jitter_s": 0.01,
      "snr_db": -3,
      "broad_fa_band_hz": [
        80,
        150
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
      ]
    }
  },
  "recovery_settings": {
    "fp_tolerance_hz": 1,
    "strict_fp_tolerance_hz": 0.5,
    "fa_tolerance_hz": 8,
    "boundary_values_hz": [
      4,
      12
    ],
    "invalid_outputs": "count as recovery failures; errors summarized over finite estimates with n_valid reported",
    "AUC": "all coupled-vs-null score pairs, greater-than + half of ties; finite scores only; no score normalization or direction reversal"
  },
  "paths": {
    "repository": "C:\\Users\\nghare\\.brainstorm\\process\\apc-brainstorm-publish",
    "workspace": "C:\\Users\\nghare\\.brainstorm\\process"
  }
}
```
