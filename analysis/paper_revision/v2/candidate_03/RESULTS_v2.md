# APC v2.0 candidate 3: held-out results

Branch v2-revision; frozen tag `v2.0`; commit `217fd8373759150cdeffe794d231a7cec2225f38`. The tagged method source matches the candidate-3 unit-tested source. All held-out inputs were generated only after tagging; seed 20261022.

## Factual summary (9 lines)

1. Frozen source: 217fd8373759150cdeffe794d231a7cec2225f38; tag v2.0.

2. Gates (a), (a2), (b), (c) passed; (d) completed all 25 existing trials.

3. The ten Poisson unit trials all had corrected event p>0.05.

4. Held-out inputs: 350 coupled, 250 timing null and 75 no-coupled-burst controls; ten methods/configurations per input.

5. Per-trial rows: 6750; summary groups: 270; all 325 null subtraction checks passed.

6. C1: FAIL; C2: PASS.

7. C3: FAIL; C4: FAIL.

8. tPAC was skipped: its function was absent from the configured MATLAB path and the configured Brainstorm install was unavailable.

9. No method parameters changed after the unit gates or tag.

## Freeze, units and execution

Full unit results, including all true/recovered pairs, raw fA score curves and BLP/PPC curves: [UNIT_RESULTS.md](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/UNIT_RESULTS.md>). Freeze attestation: [freeze_attestation.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/freeze_attestation.json>). Protocol: [PROTOCOL_v2.md](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/PROTOCOL_v2.md>). Execution bookkeeping: [HELDOUT_EXECUTION.md](<C:/Users/nghare/.brainstorm/process/apc-brainstorm-publish/analysis/v2_revision/HELDOUT_EXECUTION.md>).

Candidate 1 failed phase recovery; candidate 2 failed amplitude recovery. Their records remain preserved. Candidate 3 changes only Step 4 to the specified Gaussian analytic kernel; Step 2 BLP, the max-BLP event test and fixed-frequency secondary test remain unchanged. All candidate history is in the protocol. No further candidate was made.

H1 uses the original sparsity/distractor formulas with random true pairs and the requested durations/levels. H2 uses a physical-trough coupled rhythm, independent random fD/phase, the requested amplitude ratios, and no high-frequency distractor. H4 uses the canonical sinusoidal continuous envelope (12 s, depth .70) and the suite-wide mixed-noise formula at -3 dB. Full per-trial generator settings and random draws: [heldout_frequency_draws.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/heldout_frequency_draws.csv>). The exact stream map and pre-data choices are in HELDOUT_EXECUTION.md.

All methods share each saved input. Phase/amplitude tolerances are inclusive 1/8 Hz; strict phase tolerance .5 Hz. Invalid outputs count as recovery failures. fP/fA recovery columns are marginal. Errors use finite estimates; CSVs include their denominators. H2 picks near fD means |estimated fP-fD|<=1 regardless of amplitude recovery. AUC uses finite scores, original score direction and half credit for ties; finite denominators appear in every row. Event p<.05 rates use all 25 trials, with finite-p counts shown.

Comparators independently maximize their own full grids (phase 3:.5:14, amplitude 80:4:160); A2-prime half-width=14 and A1-prime half-width=candidate fP. Phase half-width=1.5 Hz. Their inherited butter(4)/filtfilt, raw/Ozkurt/KLMI/GLM definitions are recorded in provenance. tPAC availability inspection: [headless_inspection.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/headless_inspection.json>).

## C1-C4

| Criterion | Result | Numbers |
| --- | --- | --- |
| C1 | FAIL | v2 joint 5/100; best A2 joint 62/100; required >= 57; near-fD 14/100, required <=10 |
| C2 | PASS | v2 strict 71/175; best A2 strict 51/175; discordant v2-only/A2-only=46/26; exact one-sided McNemar p=0.0122304536642 |
| C3 | FAIL | false joint v2 2/250 (0.8/100), best A2 0/250 (0/100), allowance +5/100; event-z AUCs: H1_sparsity=1: 0.8848; H1_sparsity=0.55000000000000004: 0.5536; H1_distractor=0: 0.7872; H1_distractor=1.5: 0.6576; H1_distractor=3: 0.7184 |
| C4 | FAIL | v2 joint 71/175; best A2 joint 111/175; required >= 102 |

Best A2-prime is chosen per level in the comparator's favor for each endpoint, as specified before data generation. Exact choices/counts: [best_A2_by_level.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/best_A2_by_level.csv>). Paired McNemar counts, required AUCs and thresholds: [decision_details.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/decision_details.json>). Criterion CSV: [decision_criteria.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/decision_criteria.csv>).

## Recovery tables

Full per-trial results: [heldout_trials.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/heldout_trials.csv>). Summary with finite counts and provenance: [heldout_recovery_summary.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/heldout_recovery_summary.csv>).

### H1_sparsity

| Dataset | Level | Config | Method | Joint /25 | fA /25 | fP /25 | Strict /25 | Valid /25 | fP error mean/median Hz | fA error mean/median Hz | Near fD /25 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| coupled | 1 | A1_prime | GLM | 9 | 21 | 9 | 2 | 25 | 2.2339/1.2267 | 6.6699/1.6337 | 0 |
| coupled | 1 | A1_prime | KLMI | 4 | 15 | 5 | 1 | 25 | 2.9884/1.3257 | 11.59/7.2777 | 0 |
| coupled | 1 | A1_prime | MVL-Ozkurt | 5 | 15 | 6 | 1 | 25 | 3.2224/1.3681 | 14.251/5.7455 | 0 |
| coupled | 1 | A1_prime | MVL-raw | 4 | 25 | 4 | 0 | 25 | 1.2041/1.2561 | 1.4644/1.1503 | 0 |
| coupled | 1 | A2_prime | GLM | 21 | 24 | 21 | 10 | 25 | 0.67263/0.57528 | 3.1905/1.5869 | 0 |
| coupled | 1 | A2_prime | KLMI | 19 | 22 | 19 | 10 | 25 | 1.4237/0.58037 | 4.8178/1.2705 | 0 |
| coupled | 1 | A2_prime | MVL-Ozkurt | 18 | 23 | 18 | 8 | 25 | 1.2238/0.64885 | 2.8929/1.1503 | 0 |
| coupled | 1 | A2_prime | MVL-raw | 19 | 25 | 19 | 8 | 25 | 0.6665/0.64885 | 1.0095/0.72234 | 0 |
| coupled | 1 | v1.0 | APC | 21 | 21 | 25 | 21 | 25 | 0.039152/0.026312 | 5.3051/3.1503 | 0 |
| coupled | 1 | v2.0 | APC | 22 | 23 | 22 | 22 | 25 | 1.5499/0.031334 | 3.5094/0.6687 | 0 |
| timing_null | 1 | A1_prime | GLM | 0 | 5 | 0 | 0 | 25 | 4.4591/4.5405 | 25.409/24.462 | 0 |
| timing_null | 1 | A1_prime | KLMI | 0 | 6 | 0 | 0 | 25 | 4.7391/4.741 | 23.609/21.634 | 0 |
| timing_null | 1 | A1_prime | MVL-Ozkurt | 0 | 4 | 0 | 0 | 25 | 4.6391/4.741 | 22.742/19.643 | 0 |
| timing_null | 1 | A1_prime | MVL-raw | 0 | 23 | 0 | 0 | 25 | 4.197/3.3734 | 4.2264/2.1025 | 0 |
| timing_null | 1 | A2_prime | GLM | 0 | 5 | 1 | 0 | 25 | 3.636/3.4843 | 21.067/20.722 | 0 |
| timing_null | 1 | A2_prime | KLMI | 0 | 5 | 0 | 0 | 25 | 4.6591/4.7191 | 23.529/21.481 | 0 |
| timing_null | 1 | A2_prime | MVL-Ozkurt | 0 | 5 | 0 | 0 | 25 | 4.253/3.7191 | 24.691/25.481 | 0 |
| timing_null | 1 | A2_prime | MVL-raw | 0 | 19 | 0 | 0 | 25 | 4.3551/3.7191 | 7.0859/3.4662 | 0 |
| timing_null | 1 | v1.0 | APC | 5 | 5 | 25 | 5 | 25 | 0.042765/0.030303 | 22.373/21.466 | 0 |
| timing_null | 1 | v2.0 | APC | 0 | 2 | 1 | 0 | 25 | 12.154/12.377 | 25.436/26.255 | 0 |
| no_coupled_burst | 1 | A1_prime | GLM | 0 | 3 | 1 | 0 | 25 | 4.2991/4.5405 | 25.938/24.462 | 0 |
| no_coupled_burst | 1 | A1_prime | KLMI | 0 | 3 | 0 | 0 | 25 | 4.7391/4.741 | 25.728/23.83 | 0 |
| no_coupled_burst | 1 | A1_prime | MVL-Ozkurt | 0 | 3 | 0 | 0 | 25 | 4.4991/4.6077 | 23.702/20.051 | 0 |
| no_coupled_burst | 1 | A1_prime | MVL-raw | 0 | 7 | 0 | 0 | 25 | 3.6391/2.9965 | 19.971/18.812 | 0 |
| no_coupled_burst | 1 | A2_prime | GLM | 0 | 3 | 0 | 0 | 25 | 3.6666/3.4843 | 24.003/22.103 | 0 |
| no_coupled_burst | 1 | A2_prime | KLMI | 0 | 3 | 0 | 0 | 25 | 4.2991/4.6077 | 24.138/21.481 | 0 |
| no_coupled_burst | 1 | A2_prime | MVL-Ozkurt | 0 | 6 | 0 | 0 | 25 | 4.3556/4.241 | 23.404/20.534 | 0 |
| no_coupled_burst | 1 | A2_prime | MVL-raw | 0 | 8 | 0 | 0 | 25 | 4.2956/4.241 | 21.68/20.534 | 0 |
| no_coupled_burst | 1 | v1.0 | APC | 2 | 2 | 25 | 2 | 25 | 0.041222/0.031727 | 22.575/21.897 | 0 |
| no_coupled_burst | 1 | v2.0 | APC | 0 | 7 | 0 | 0 | 25 | 12.654/13.244 | 24.738/25.667 | 0 |
| coupled | 0.55 | A1_prime | GLM | 5 | 15 | 5 | 0 | 25 | 3.3678/3.1686 | 11.889/2.7195 | 0 |
| coupled | 0.55 | A1_prime | KLMI | 4 | 13 | 4 | 0 | 25 | 3.5696/3.1686 | 16.113/6.5236 | 0 |
| coupled | 0.55 | A1_prime | MVL-Ozkurt | 4 | 13 | 4 | 1 | 25 | 3.6901/5.0008 | 15.461/6.5236 | 0 |
| coupled | 0.55 | A1_prime | MVL-raw | 4 | 25 | 4 | 0 | 25 | 1.6366/1.2439 | 1.1591/1.0732 | 0 |
| coupled | 0.55 | A2_prime | GLM | 18 | 22 | 18 | 8 | 25 | 1.3392/0.80364 | 4.4049/1.2522 | 0 |
| coupled | 0.55 | A2_prime | KLMI | 18 | 21 | 18 | 10 | 25 | 1.685/0.80364 | 6.4897/1.4764 | 0 |
| coupled | 0.55 | A2_prime | MVL-Ozkurt | 17 | 23 | 17 | 8 | 25 | 1.4363/0.69359 | 3.6112/1.2522 | 0 |
| coupled | 0.55 | A2_prime | MVL-raw | 17 | 25 | 17 | 8 | 25 | 1.2374/0.69359 | 1.5312/1.2522 | 0 |
| coupled | 0.55 | v1.0 | APC | 21 | 21 | 25 | 21 | 25 | 0.027617/0.019478 | 7.651/3.2561 | 0 |
| coupled | 0.55 | v2.0 | APC | 11 | 16 | 11 | 11 | 25 | 7.0115/2.6373 | 13.803/3.1752 | 0 |
| timing_null | 0.55 | A1_prime | GLM | 0 | 2 | 0 | 0 | 25 | 4.552/4.7561 | 26.469/24.229 | 0 |
| timing_null | 0.55 | A1_prime | KLMI | 0 | 2 | 0 | 0 | 25 | 4.572/4.5008 | 31.943/29.89 | 0 |
| timing_null | 0.55 | A1_prime | MVL-Ozkurt | 0 | 3 | 0 | 0 | 25 | 4.512/4.7561 | 28.597/24.649 | 0 |
| timing_null | 0.55 | A1_prime | MVL-raw | 1 | 21 | 1 | 1 | 25 | 4.216/4.4437 | 7.2215/2.1945 | 0 |
| timing_null | 0.55 | A2_prime | GLM | 0 | 7 | 1 | 0 | 25 | 3.1983/3.1077 | 23.345/27.975 | 0 |
| timing_null | 0.55 | A2_prime | KLMI | 0 | 7 | 0 | 0 | 25 | 4.252/4.1077 | 25.119/25.073 | 0 |
| timing_null | 0.55 | A2_prime | MVL-Ozkurt | 0 | 5 | 0 | 0 | 25 | 3.8997/3.5053 | 24.44/23.506 | 0 |
| timing_null | 0.55 | A2_prime | MVL-raw | 0 | 14 | 0 | 0 | 25 | 4.0997/4.0943 | 11.007/5.8896 | 0 |
| timing_null | 0.55 | v1.0 | APC | 6 | 6 | 25 | 6 | 25 | 0.023229/0.018259 | 26.081/24.806 | 0 |
| timing_null | 0.55 | v2.0 | APC | 0 | 3 | 0 | 0 | 25 | 15.29/15.839 | 31.455/30.11 | 0 |
| coupled | 0.25 | A1_prime | GLM | 3 | 4 | 3 | 1 | 25 | 3.5157/3.7494 | 25.152/21.687 | 0 |
| coupled | 0.25 | A1_prime | KLMI | 2 | 8 | 2 | 1 | 25 | 3.6773/3.8071 | 17.644/17.272 | 0 |
| coupled | 0.25 | A1_prime | MVL-Ozkurt | 1 | 4 | 1 | 0 | 25 | 3.8828/3.8071 | 20.887/18.471 | 0 |
| coupled | 0.25 | A1_prime | MVL-raw | 6 | 25 | 6 | 1 | 25 | 1.6459/1.3084 | 2.1664/1.6866 | 0 |
| coupled | 0.25 | A2_prime | GLM | 7 | 14 | 9 | 4 | 25 | 1.9746/1.1916 | 12.883/5.6079 | 0 |
| coupled | 0.25 | A2_prime | KLMI | 6 | 21 | 6 | 4 | 25 | 2.9523/2.3929 | 8.7319/3.9796 | 0 |
| coupled | 0.25 | A2_prime | MVL-Ozkurt | 8 | 16 | 9 | 3 | 25 | 2.2169/1.2494 | 11.607/5.2717 | 0 |
| coupled | 0.25 | A2_prime | MVL-raw | 9 | 24 | 9 | 3 | 25 | 1.8556/1.2494 | 3.394/2.4706 | 0 |
| coupled | 0.25 | v1.0 | APC | 9 | 9 | 25 | 9 | 25 | 0.030251/0.030239 | 20.867/13.928 | 0 |
| coupled | 0.25 | v2.0 | APC | 2 | 7 | 3 | 2 | 25 | 11.53/11.756 | 25.514/24.155 | 0 |
| timing_null | 0.25 | A1_prime | GLM | 0 | 6 | 0 | 0 | 25 | 3.9368/3.7494 | 23.529/18.471 | 0 |
| timing_null | 0.25 | A1_prime | KLMI | 0 | 6 | 0 | 0 | 25 | 3.9968/3.8071 | 22.936/19.992 | 0 |
| timing_null | 0.25 | A1_prime | MVL-Ozkurt | 0 | 4 | 0 | 0 | 25 | 4.0568/3.8071 | 21.244/18.392 | 0 |
| timing_null | 0.25 | A1_prime | MVL-raw | 0 | 19 | 1 | 0 | 25 | 3.1342/2.6436 | 8.3862/2.6603 | 0 |
| timing_null | 0.25 | A2_prime | GLM | 0 | 6 | 2 | 0 | 25 | 3.4234/2.9393 | 23.273/16.928 | 0 |
| timing_null | 0.25 | A2_prime | KLMI | 0 | 12 | 0 | 0 | 25 | 3.7368/3.2587 | 17.375/10.112 | 0 |
| timing_null | 0.25 | A2_prime | MVL-Ozkurt | 0 | 8 | 1 | 0 | 25 | 2.9662/2.4393 | 20.186/14.415 | 0 |
| timing_null | 0.25 | A2_prime | MVL-raw | 0 | 16 | 0 | 0 | 25 | 3.6027/2.8851 | 10.801/5.6866 | 0 |
| timing_null | 0.25 | v1.0 | APC | 5 | 5 | 25 | 5 | 25 | 0.027702/0.024727 | 26.602/25.932 | 0 |
| timing_null | 0.25 | v2.0 | APC | 0 | 3 | 0 | 0 | 25 | 14.207/14.934 | 28.541/25.26 | 0 |
| coupled | 0.15 | A1_prime | GLM | 0 | 4 | 1 | 0 | 25 | 4.5295/5.0165 | 23.443/21.213 | 0 |
| coupled | 0.15 | A1_prime | KLMI | 0 | 6 | 0 | 0 | 25 | 4.8295/5.4582 | 20.604/19.556 | 0 |
| coupled | 0.15 | A1_prime | MVL-Ozkurt | 0 | 9 | 0 | 0 | 25 | 4.7095/5.0165 | 17.136/15.852 | 0 |
| coupled | 0.15 | A1_prime | MVL-raw | 2 | 23 | 2 | 0 | 25 | 3.3514/2.6786 | 4.045/1.8844 | 0 |
| coupled | 0.15 | A2_prime | GLM | 4 | 14 | 4 | 2 | 25 | 2.9435/2.2466 | 13.495/6.6407 | 0 |
| coupled | 0.15 | A2_prime | KLMI | 1 | 18 | 1 | 0 | 25 | 4.3525/4.9861 | 8.6495/5.2135 | 0 |
| coupled | 0.15 | A2_prime | MVL-Ozkurt | 2 | 11 | 3 | 0 | 25 | 3.8583/4.2466 | 15.964/9.2291 | 0 |
| coupled | 0.15 | A2_prime | MVL-raw | 5 | 21 | 5 | 2 | 25 | 3.2546/2.6786 | 6.0271/4.1394 | 0 |
| coupled | 0.15 | v1.0 | APC | 8 | 8 | 25 | 8 | 25 | 0.021709/0.016725 | 21.393/19.077 | 0 |
| coupled | 0.15 | v2.0 | APC | 1 | 6 | 3 | 1 | 25 | 11.775/11.587 | 24.011/22.827 | 0 |
| timing_null | 0.15 | A1_prime | GLM | 0 | 4 | 0 | 0 | 25 | 4.6895/5.0165 | 21.861/19.556 | 0 |
| timing_null | 0.15 | A1_prime | KLMI | 0 | 3 | 0 | 0 | 25 | 4.7295/5.3648 | 23.37/19.556 | 0 |
| timing_null | 0.15 | A1_prime | MVL-Ozkurt | 0 | 5 | 0 | 0 | 25 | 4.7295/5.4582 | 24.706/24.152 | 0 |
| timing_null | 0.15 | A1_prime | MVL-raw | 0 | 18 | 0 | 0 | 25 | 4.0943/3.9582 | 7.5727/2.6407 | 0 |
| timing_null | 0.15 | A2_prime | GLM | 0 | 2 | 1 | 0 | 25 | 3.1643/2.6345 | 27.106/23.848 | 0 |
| timing_null | 0.15 | A2_prime | KLMI | 0 | 11 | 0 | 0 | 25 | 4.5895/4.9861 | 17.029/14.313 | 0 |
| timing_null | 0.15 | A2_prime | MVL-Ozkurt | 0 | 5 | 1 | 0 | 25 | 4.4375/4.9597 | 21.732/22.376 | 0 |
| timing_null | 0.15 | A2_prime | MVL-raw | 0 | 15 | 0 | 0 | 25 | 4.3162/4.2466 | 9.9762/5.6875 | 0 |
| timing_null | 0.15 | v1.0 | APC | 2 | 2 | 25 | 2 | 25 | 0.024135/0.021096 | 26.57/23.465 | 0 |
| timing_null | 0.15 | v2.0 | APC | 0 | 2 | 1 | 0 | 25 | 13.672/14.769 | 26.084/23.861 | 0 |
| no_coupled_burst | 0.15 | A1_prime | GLM | 0 | 6 | 1 | 0 | 25 | 4.5295/5.0165 | 21.98/21.213 | 0 |
| no_coupled_burst | 0.15 | A1_prime | KLMI | 0 | 5 | 1 | 0 | 25 | 4.6626/5.3648 | 22.013/19.556 | 0 |
| no_coupled_burst | 0.15 | A1_prime | MVL-Ozkurt | 0 | 7 | 0 | 0 | 25 | 4.7495/5.3863 | 20.6/19.556 | 0 |
| no_coupled_burst | 0.15 | A1_prime | MVL-raw | 0 | 8 | 1 | 0 | 25 | 4.2889/4.4835 | 17.308/17.229 | 0 |
| no_coupled_burst | 0.15 | A2_prime | GLM | 0 | 4 | 1 | 0 | 25 | 3.3963/2.8192 | 25.701/23.333 | 0 |
| no_coupled_burst | 0.15 | A2_prime | KLMI | 0 | 8 | 0 | 0 | 25 | 4.6226/4.6786 | 21.178/20.152 | 0 |
| no_coupled_burst | 0.15 | A2_prime | MVL-Ozkurt | 0 | 6 | 1 | 0 | 25 | 3.9487/3.9998 | 23.329/19.595 | 0 |
| no_coupled_burst | 0.15 | A2_prime | MVL-raw | 0 | 11 | 0 | 0 | 25 | 4.4962/4.9597 | 19.639/15.474 | 0 |
| no_coupled_burst | 0.15 | v1.0 | APC | 1 | 1 | 25 | 1 | 25 | 0.023456/0.015853 | 27.924/23.465 | 0 |
| no_coupled_burst | 0.15 | v2.0 | APC | 0 | 4 | 1 | 0 | 25 | 14.422/15.02 | 29.761/31.286 | 0 |

### H1_distractor

| Dataset | Level | Config | Method | Joint /25 | fA /25 | fP /25 | Strict /25 | Valid /25 | fP error mean/median Hz | fA error mean/median Hz | Near fD /25 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| coupled | 0 | A1_prime | GLM | 3 | 17 | 3 | 2 | 25 | 2.7985/1.2416 | 9.8342/1.4625 | 0 |
| coupled | 0 | A1_prime | KLMI | 2 | 11 | 3 | 1 | 25 | 3.7502/4.7584 | 16.564/9.5706 | 0 |
| coupled | 0 | A1_prime | MVL-Ozkurt | 1 | 12 | 2 | 0 | 25 | 3.5228/1.4162 | 12.023/8.1638 | 0 |
| coupled | 0 | A1_prime | MVL-raw | 5 | 25 | 5 | 1 | 25 | 1.0957/1.1238 | 1.2711/1.0944 | 0 |
| coupled | 0 | A2_prime | GLM | 18 | 25 | 18 | 9 | 25 | 0.64452/0.58487 | 1.1671/0.98509 | 0 |
| coupled | 0 | A2_prime | KLMI | 14 | 19 | 14 | 9 | 25 | 1.635/0.75565 | 7.8121/1.1659 | 0 |
| coupled | 0 | A2_prime | MVL-Ozkurt | 16 | 21 | 16 | 7 | 25 | 1.3879/0.75565 | 4.3052/1.0944 | 0 |
| coupled | 0 | A2_prime | MVL-raw | 18 | 25 | 18 | 8 | 25 | 0.7178/0.67608 | 0.8568/0.95506 | 0 |
| coupled | 0 | v1.0 | APC | 20 | 20 | 24 | 20 | 24 | 0.048814/0.040608 | 6.7897/4.5276 | 0 |
| coupled | 0 | v2.0 | APC | 17 | 18 | 17 | 17 | 25 | 3.7685/0.035063 | 9.4268/1.5353 | 0 |
| timing_null | 0 | A1_prime | GLM | 0 | 1 | 0 | 0 | 25 | 4.9643/5.0804 | 26.958/23.303 | 0 |
| timing_null | 0 | A1_prime | KLMI | 0 | 4 | 0 | 0 | 25 | 5.1643/5.2367 | 22.874/23.303 | 0 |
| timing_null | 0 | A1_prime | MVL-Ozkurt | 0 | 5 | 0 | 0 | 25 | 4.7043/4.7083 | 19.612/17.094 | 0 |
| timing_null | 0 | A1_prime | MVL-raw | 0 | 13 | 0 | 0 | 25 | 3.9235/3.1285 | 10.681/6.7197 | 0 |
| timing_null | 0 | A2_prime | GLM | 0 | 4 | 1 | 0 | 25 | 3.5313/3.5804 | 22.791/21.478 | 0 |
| timing_null | 0 | A2_prime | KLMI | 0 | 7 | 0 | 0 | 25 | 4.4043/4.2083 | 21.54/18.522 | 0 |
| timing_null | 0 | A2_prime | MVL-Ozkurt | 0 | 4 | 0 | 0 | 25 | 4.3237/4.0015 | 24.487/23.926 | 0 |
| timing_null | 0 | A2_prime | MVL-raw | 0 | 12 | 0 | 0 | 25 | 4.4664/4.7083 | 14.983/12.096 | 0 |
| timing_null | 0 | v1.0 | APC | 7 | 7 | 25 | 7 | 25 | 0.04065/0.02953 | 20.753/16.72 | 0 |
| timing_null | 0 | v2.0 | APC | 2 | 6 | 3 | 2 | 25 | 10.83/12.736 | 26.543/32.924 | 0 |
| coupled | 1.5 | A1_prime | GLM | 9 | 21 | 9 | 2 | 25 | 1.9618/1.1523 | 7.4637/2.0571 | 0 |
| coupled | 1.5 | A1_prime | KLMI | 2 | 17 | 3 | 0 | 25 | 2.7757/1.3359 | 9.8557/2.0571 | 0 |
| coupled | 1.5 | A1_prime | MVL-Ozkurt | 3 | 16 | 5 | 0 | 25 | 2.5459/1.3078 | 10.937/2.0571 | 0 |
| coupled | 1.5 | A1_prime | MVL-raw | 5 | 25 | 5 | 1 | 25 | 1.6514/1.2172 | 1.4123/1.0761 | 0 |
| coupled | 1.5 | A2_prime | GLM | 18 | 25 | 18 | 8 | 25 | 0.76574/0.79541 | 1.4912/1.1472 | 0 |
| coupled | 1.5 | A2_prime | KLMI | 19 | 23 | 19 | 9 | 25 | 1.1992/0.79541 | 5.5569/1.5135 | 0 |
| coupled | 1.5 | A2_prime | MVL-Ozkurt | 16 | 22 | 16 | 7 | 25 | 1.2474/0.77224 | 5.7248/1.5404 | 0 |
| coupled | 1.5 | A2_prime | MVL-raw | 16 | 24 | 16 | 7 | 25 | 1.2674/0.77224 | 2.0713/1.2758 | 0 |
| coupled | 1.5 | v1.0 | APC | 21 | 21 | 22 | 21 | 22 | 0.063716/0.033878 | 3.7151/2.3764 | 0 |
| coupled | 1.5 | v2.0 | APC | 11 | 15 | 11 | 11 | 25 | 7.905/4.5158 | 10.532/1.6043 | 0 |
| timing_null | 1.5 | A1_prime | GLM | 1 | 7 | 1 | 1 | 25 | 4.1437/4.1641 | 25.169/28.298 | 0 |
| timing_null | 1.5 | A1_prime | KLMI | 1 | 6 | 1 | 0 | 25 | 4.1837/4.1641 | 25.329/23.126 | 0 |
| timing_null | 1.5 | A1_prime | MVL-Ozkurt | 1 | 5 | 1 | 0 | 25 | 4.2036/4.2278 | 29.17/28.979 | 0 |
| timing_null | 1.5 | A1_prime | MVL-raw | 1 | 11 | 1 | 1 | 25 | 4.1799/4.1641 | 14.587/19.37 | 0 |
| timing_null | 1.5 | A2_prime | GLM | 0 | 5 | 0 | 0 | 25 | 3.0287/2.3594 | 24.146/21.64 | 0 |
| timing_null | 1.5 | A2_prime | KLMI | 0 | 7 | 0 | 0 | 25 | 4.2236/3.8431 | 29.377/30.486 | 0 |
| timing_null | 1.5 | A2_prime | MVL-Ozkurt | 0 | 6 | 0 | 0 | 25 | 3.6627/3.4945 | 27.739/23.704 | 0 |
| timing_null | 1.5 | A2_prime | MVL-raw | 1 | 9 | 1 | 1 | 25 | 3.5939/3.3431 | 15.547/15.021 | 0 |
| timing_null | 1.5 | v1.0 | APC | 4 | 4 | 25 | 4 | 25 | 0.077243/0.029918 | 25.927/24.62 | 0 |
| timing_null | 1.5 | v2.0 | APC | 0 | 4 | 1 | 0 | 25 | 13.95/14.456 | 24.581/18.136 | 0 |
| coupled | 3 | A1_prime | GLM | 9 | 21 | 9 | 0 | 25 | 2.7694/1.2933 | 7.2901/1.632 | 0 |
| coupled | 3 | A1_prime | KLMI | 5 | 18 | 5 | 1 | 25 | 3.2028/1.3898 | 11.03/2.0508 | 0 |
| coupled | 3 | A1_prime | MVL-Ozkurt | 5 | 15 | 5 | 3 | 25 | 3.1044/1.3864 | 13.243/5.7944 | 0 |
| coupled | 3 | A1_prime | MVL-raw | 8 | 22 | 8 | 0 | 25 | 1.8977/1.1776 | 3.9387/1.0928 | 0 |
| coupled | 3 | A2_prime | GLM | 21 | 24 | 21 | 7 | 25 | 0.9601/0.75653 | 2.9539/1.0928 | 0 |
| coupled | 3 | A2_prime | KLMI | 16 | 21 | 16 | 6 | 25 | 1.6531/0.86079 | 5.7069/1.0928 | 0 |
| coupled | 3 | A2_prime | MVL-Ozkurt | 20 | 24 | 20 | 6 | 25 | 0.98298/0.70675 | 3.0352/1.0227 | 0 |
| coupled | 3 | A2_prime | MVL-raw | 17 | 21 | 17 | 5 | 25 | 1.6776/0.8864 | 4.8643/1.2037 | 0 |
| coupled | 3 | v1.0 | APC | 20 | 20 | 23 | 20 | 24 | 0.37568/0.056571 | 7.8465/4.4181 | 0 |
| coupled | 3 | v2.0 | APC | 7 | 13 | 7 | 7 | 25 | 10.369/14.248 | 13.516/7.149 | 0 |
| timing_null | 3 | A1_prime | GLM | 0 | 4 | 0 | 0 | 25 | 4.3078/4.3567 | 24.326/19.425 | 0 |
| timing_null | 3 | A1_prime | KLMI | 0 | 6 | 0 | 0 | 25 | 4.3678/4.2809 | 23.377/19.932 | 0 |
| timing_null | 3 | A1_prime | MVL-Ozkurt | 0 | 5 | 0 | 0 | 25 | 4.4278/4.2652 | 21.497/17.608 | 0 |
| timing_null | 3 | A1_prime | MVL-raw | 0 | 0 | 2 | 0 | 25 | 3.5071/3.1456 | 22.873/23.35 | 0 |
| timing_null | 3 | A2_prime | GLM | 2 | 8 | 4 | 1 | 25 | 3.0714/3.0814 | 22.866/20.59 | 0 |
| timing_null | 3 | A2_prime | KLMI | 0 | 6 | 0 | 0 | 25 | 4.3078/4.2435 | 23.414/20.906 | 0 |
| timing_null | 3 | A2_prime | MVL-Ozkurt | 0 | 6 | 0 | 0 | 25 | 4.5056/4.2685 | 22.778/22.946 | 0 |
| timing_null | 3 | A2_prime | MVL-raw | 0 | 0 | 2 | 0 | 25 | 3.5648/3.8224 | 22.858/22.977 | 0 |
| timing_null | 3 | v1.0 | APC | 4 | 4 | 23 | 4 | 23 | 0.054111/0.040838 | 25.168/24.051 | 0 |
| timing_null | 3 | v2.0 | APC | 0 | 1 | 4 | 0 | 25 | 11.334/14.689 | 26.696/25.949 | 0 |
| no_coupled_burst | 3 | A1_prime | GLM | 0 | 5 | 0 | 0 | 25 | 4.3878/4.3567 | 25.228/23.75 | 0 |
| no_coupled_burst | 3 | A1_prime | KLMI | 0 | 6 | 0 | 0 | 25 | 4.4678/4.3567 | 22.353/20.575 | 0 |
| no_coupled_burst | 3 | A1_prime | MVL-Ozkurt | 0 | 5 | 0 | 0 | 25 | 4.4078/4.2652 | 21.355/19.932 | 0 |
| no_coupled_burst | 3 | A1_prime | MVL-raw | 0 | 0 | 2 | 0 | 25 | 3.3871/2.7067 | 23.338/23.425 | 0 |
| no_coupled_burst | 3 | A2_prime | GLM | 2 | 9 | 3 | 1 | 25 | 3.2928/3.2348 | 19.948/15.75 | 0 |
| no_coupled_burst | 3 | A2_prime | KLMI | 1 | 5 | 1 | 0 | 25 | 4.2389/4.1102 | 24.526/20.068 | 0 |
| no_coupled_burst | 3 | A2_prime | MVL-Ozkurt | 0 | 5 | 0 | 0 | 25 | 4.3456/4.2685 | 24.238/22.977 | 0 |
| no_coupled_burst | 3 | A2_prime | MVL-raw | 0 | 0 | 2 | 0 | 25 | 3.5448/3.3224 | 22.858/22.796 | 0 |
| no_coupled_burst | 3 | v1.0 | APC | 8 | 8 | 24 | 8 | 24 | 0.060509/0.055923 | 19.39/19.099 | 0 |
| no_coupled_burst | 3 | v2.0 | APC | 0 | 4 | 4 | 0 | 25 | 11.226/13.096 | 27.368/25.949 | 0 |

### H2

| Dataset | Level | Config | Method | Joint /25 | fA /25 | fP /25 | Strict /25 | Valid /25 | fP error mean/median Hz | fA error mean/median Hz | Near fD /25 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| coupled | 0 | A1_prime | GLM | 15 | 25 | 15 | 3 | 25 | 0.86157/0.97868 | 1.4733/1.0656 | 0 |
| coupled | 0 | A1_prime | KLMI | 10 | 25 | 10 | 3 | 25 | 0.98437/1.0492 | 1.6774/0.99245 | 0 |
| coupled | 0 | A1_prime | MVL-Ozkurt | 9 | 23 | 9 | 1 | 25 | 1.2379/1.0676 | 3.2525/0.99245 | 0 |
| coupled | 0 | A1_prime | MVL-raw | 4 | 25 | 4 | 0 | 25 | 1.1524/1.1529 | 0.9675/0.99245 | 0 |
| coupled | 0 | A2_prime | GLM | 25 | 25 | 25 | 12 | 25 | 0.47471/0.54345 | 3.0092/2.8184 | 0 |
| coupled | 0 | A2_prime | KLMI | 25 | 25 | 25 | 11 | 25 | 0.50519/0.54345 | 2.0669/2.2973 | 0 |
| coupled | 0 | A2_prime | MVL-Ozkurt | 23 | 25 | 23 | 12 | 25 | 0.55824/0.54345 | 2.097/2.2973 | 0 |
| coupled | 0 | A2_prime | MVL-raw | 23 | 25 | 23 | 12 | 25 | 0.56946/0.54345 | 1.3702/1.2052 | 0 |
| coupled | 0 | v1.0 | APC | 25 | 25 | 25 | 25 | 25 | 0.053841/0.041569 | 2.405/2.3096 | 0 |
| coupled | 0 | v2.0 | APC | 8 | 12 | 8 | 8 | 25 | 10.711/12.777 | 20.101/16.262 | 0 |
| timing_null | 0 | A1_prime | GLM | 0 | 1 | 1 | 0 | 25 | 2.6105/2.377 | 33.295/29.868 | 0 |
| timing_null | 0 | A1_prime | KLMI | 0 | 2 | 4 | 0 | 25 | 2.319/2.2867 | 31.941/29.689 | 0 |
| timing_null | 0 | A1_prime | MVL-Ozkurt | 0 | 4 | 1 | 0 | 25 | 2.4873/2.23 | 24.986/26.818 | 0 |
| timing_null | 0 | A1_prime | MVL-raw | 1 | 15 | 1 | 1 | 25 | 3.9371/3.4346 | 12.787/4.9924 | 2 |
| timing_null | 0 | A2_prime | GLM | 0 | 0 | 0 | 0 | 25 | 2.8249/2.5492 | 35.462/33.066 | 1 |
| timing_null | 0 | A2_prime | KLMI | 0 | 4 | 1 | 0 | 25 | 2.738/2.73 | 33.531/30.311 | 0 |
| timing_null | 0 | A2_prime | MVL-Ozkurt | 0 | 3 | 0 | 0 | 25 | 2.5849/2.2833 | 30.983/29.205 | 0 |
| timing_null | 0 | A2_prime | MVL-raw | 0 | 8 | 0 | 0 | 25 | 2.781/2.6445 | 18.63/11.285 | 0 |
| timing_null | 0 | v1.0 | APC | 2 | 2 | 25 | 2 | 25 | 0.051508/0.035053 | 28.263/25.681 | 0 |
| timing_null | 0 | v2.0 | APC | 0 | 7 | 0 | 0 | 25 | 16.079/17.311 | 19.206/13.135 | 1 |
| coupled | 0.5 | A1_prime | GLM | 12 | 25 | 12 | 3 | 25 | 0.8856/1.0183 | 1.3449/1.2788 | 0 |
| coupled | 0.5 | A1_prime | KLMI | 11 | 25 | 11 | 3 | 25 | 0.95805/1.0192 | 1.8784/1.1137 | 0 |
| coupled | 0.5 | A1_prime | MVL-Ozkurt | 10 | 22 | 10 | 2 | 25 | 1.2612/1.0587 | 5.5687/1.5105 | 0 |
| coupled | 0.5 | A1_prime | MVL-raw | 4 | 25 | 4 | 0 | 25 | 1.1674/1.1304 | 1.1708/1.1137 | 0 |
| coupled | 0.5 | A2_prime | GLM | 23 | 25 | 23 | 10 | 25 | 0.54493/0.55378 | 2.1533/1.8032 | 0 |
| coupled | 0.5 | A2_prime | KLMI | 22 | 25 | 22 | 10 | 25 | 0.57354/0.55378 | 1.9744/1.9837 | 0 |
| coupled | 0.5 | A2_prime | MVL-Ozkurt | 21 | 25 | 21 | 9 | 25 | 0.64326/0.69128 | 1.8144/1.7869 | 0 |
| coupled | 0.5 | A2_prime | MVL-raw | 21 | 25 | 21 | 9 | 25 | 0.64326/0.69128 | 1.657/1.6561 | 0 |
| coupled | 0.5 | v1.0 | APC | 24 | 24 | 25 | 24 | 25 | 0.078702/0.053932 | 4.0134/2.6561 | 0 |
| coupled | 0.5 | v2.0 | APC | 11 | 15 | 11 | 11 | 25 | 7.626/4.8366 | 13.679/1.6081 | 3 |
| coupled | 1 | A1_prime | GLM | 13 | 25 | 13 | 1 | 25 | 0.9208/0.90435 | 1.2809/0.69611 | 0 |
| coupled | 1 | A1_prime | KLMI | 10 | 25 | 10 | 0 | 25 | 1.0146/1.0644 | 1.2245/0.69611 | 0 |
| coupled | 1 | A1_prime | MVL-Ozkurt | 9 | 21 | 9 | 1 | 25 | 1.3914/1.1543 | 4.9116/1.3632 | 0 |
| coupled | 1 | A1_prime | MVL-raw | 5 | 25 | 5 | 0 | 25 | 1.1229/1.153 | 1.0202/0.69611 | 0 |
| coupled | 1 | A2_prime | GLM | 19 | 25 | 19 | 9 | 25 | 0.65256/0.75488 | 1.8087/1.3632 | 0 |
| coupled | 1 | A2_prime | KLMI | 18 | 25 | 18 | 8 | 25 | 0.70872/0.76147 | 2.0035/2.1452 | 0 |
| coupled | 1 | A2_prime | MVL-Ozkurt | 16 | 23 | 16 | 7 | 25 | 0.94831/0.78967 | 3.3791/2.4861 | 0 |
| coupled | 1 | A2_prime | MVL-raw | 17 | 25 | 17 | 7 | 25 | 0.76646/0.78967 | 2.1413/2.1452 | 0 |
| coupled | 1 | v1.0 | APC | 13 | 17 | 13 | 11 | 24 | 2.0553/0.82231 | 10.255/4.4796 | 9 |
| coupled | 1 | v2.0 | APC | 2 | 12 | 2 | 2 | 25 | 11.978/11.782 | 22.122/20.37 | 5 |
| timing_null | 1 | A1_prime | GLM | 2 | 8 | 5 | 1 | 25 | 2.0152/1.6392 | 17.387/16.023 | 0 |
| timing_null | 1 | A1_prime | KLMI | 2 | 9 | 6 | 1 | 25 | 2.0468/1.8947 | 15.556/13.514 | 0 |
| timing_null | 1 | A1_prime | MVL-Ozkurt | 0 | 4 | 2 | 0 | 25 | 2.0952/1.847 | 23.011/23.447 | 0 |
| timing_null | 1 | A1_prime | MVL-raw | 1 | 9 | 4 | 1 | 25 | 3.2258/2.6543 | 17.894/18.558 | 1 |
| timing_null | 1 | A2_prime | GLM | 0 | 5 | 3 | 0 | 25 | 2.7286/2.6543 | 25.004/25.294 | 0 |
| timing_null | 1 | A2_prime | KLMI | 0 | 3 | 3 | 0 | 25 | 2.1656/1.9356 | 23.34/22.145 | 0 |
| timing_null | 1 | A2_prime | MVL-Ozkurt | 0 | 3 | 0 | 0 | 25 | 2.5505/1.9356 | 26.86/27.844 | 1 |
| timing_null | 1 | A2_prime | MVL-raw | 0 | 5 | 0 | 0 | 25 | 2.8117/2.2565 | 22.904/23.63 | 1 |
| timing_null | 1 | v1.0 | APC | 1 | 4 | 14 | 1 | 25 | 2.0639/0.61159 | 22.716/22.882 | 9 |
| timing_null | 1 | v2.0 | APC | 0 | 3 | 0 | 0 | 25 | 15.388/15.784 | 30.099/28.79 | 3 |
| coupled | 1.5 | A1_prime | GLM | 13 | 24 | 13 | 3 | 25 | 1.1545/0.97726 | 2.8618/2.3721 | 0 |
| coupled | 1.5 | A1_prime | KLMI | 12 | 21 | 13 | 2 | 25 | 1.244/0.96313 | 7.55/2.3721 | 0 |
| coupled | 1.5 | A1_prime | MVL-Ozkurt | 10 | 17 | 11 | 1 | 25 | 1.5118/1.1617 | 12.056/2.6655 | 0 |
| coupled | 1.5 | A1_prime | MVL-raw | 11 | 25 | 11 | 2 | 25 | 1.1133/1.0751 | 1.2889/0.97455 | 0 |
| coupled | 1.5 | A2_prime | GLM | 20 | 24 | 20 | 10 | 25 | 0.64287/0.633 | 3.2983/2.7083 | 0 |
| coupled | 1.5 | A2_prime | KLMI | 18 | 23 | 18 | 9 | 25 | 0.78625/0.66872 | 4.1173/2.6655 | 0 |
| coupled | 1.5 | A2_prime | MVL-Ozkurt | 18 | 24 | 18 | 8 | 25 | 0.71862/0.633 | 3.8786/2.7083 | 0 |
| coupled | 1.5 | A2_prime | MVL-raw | 19 | 24 | 19 | 8 | 25 | 0.69862/0.58963 | 3.4087/1.9278 | 0 |
| coupled | 1.5 | v1.0 | APC | 1 | 7 | 1 | 1 | 24 | 4.2697/4.2267 | 22.094/24.477 | 21 |
| coupled | 1.5 | v2.0 | APC | 2 | 3 | 2 | 2 | 25 | 13.548/15.015 | 29.281/31.613 | 2 |
| coupled | 2 | A1_prime | GLM | 6 | 10 | 8 | 2 | 25 | 1.7736/1.5065 | 14.649/11.077 | 0 |
| coupled | 2 | A1_prime | KLMI | 7 | 12 | 7 | 1 | 25 | 1.8388/1.5258 | 12.896/8.6329 | 0 |
| coupled | 2 | A1_prime | MVL-Ozkurt | 6 | 9 | 9 | 2 | 25 | 1.7973/1.5065 | 15.006/11.367 | 0 |
| coupled | 2 | A1_prime | MVL-raw | 13 | 23 | 13 | 4 | 25 | 1.3339/0.99348 | 4.0749/1.7401 | 1 |
| coupled | 2 | A2_prime | GLM | 15 | 20 | 17 | 7 | 25 | 0.99542/0.77889 | 7.5529/4.3926 | 1 |
| coupled | 2 | A2_prime | KLMI | 12 | 17 | 14 | 3 | 25 | 1.358/0.95778 | 10.683/5.1471 | 0 |
| coupled | 2 | A2_prime | MVL-Ozkurt | 7 | 13 | 9 | 2 | 25 | 1.534/1.2479 | 14.7/6.0876 | 0 |
| coupled | 2 | A2_prime | MVL-raw | 11 | 20 | 12 | 4 | 25 | 1.5548/1.0322 | 7.1939/4.3913 | 1 |
| coupled | 2 | v1.0 | APC | 0 | 5 | 0 | 0 | 25 | 5.8683/5.8564 | 23.856/29.641 | 25 |
| coupled | 2 | v2.0 | APC | 0 | 3 | 0 | 0 | 25 | 12.752/13.27 | 21.95/16.889 | 6 |
| coupled | 3 | A1_prime | GLM | 1 | 5 | 9 | 0 | 25 | 1.7555/1.4467 | 22.267/20.997 | 0 |
| coupled | 3 | A1_prime | KLMI | 1 | 9 | 5 | 1 | 25 | 1.9296/1.6443 | 19.283/19.113 | 0 |
| coupled | 3 | A1_prime | MVL-Ozkurt | 2 | 5 | 6 | 2 | 25 | 1.7332/1.3172 | 22.499/24.543 | 0 |
| coupled | 3 | A1_prime | MVL-raw | 3 | 11 | 4 | 1 | 25 | 3.1204/1.7113 | 14.563/9.1695 | 0 |
| coupled | 3 | A2_prime | GLM | 8 | 10 | 12 | 5 | 25 | 2.0741/1.1948 | 17.415/11.08 | 1 |
| coupled | 3 | A2_prime | KLMI | 6 | 9 | 7 | 2 | 25 | 1.6336/1.5387 | 16.73/12.904 | 0 |
| coupled | 3 | A2_prime | MVL-Ozkurt | 4 | 7 | 8 | 2 | 25 | 2.2924/1.8332 | 19.718/16.997 | 0 |
| coupled | 3 | A2_prime | MVL-raw | 4 | 9 | 9 | 2 | 25 | 1.9438/1.3112 | 17.943/13.53 | 0 |
| coupled | 3 | v1.0 | APC | 0 | 4 | 0 | 0 | 25 | 5.3639/4.9735 | 24.027/20.989 | 25 |
| coupled | 3 | v2.0 | APC | 1 | 2 | 2 | 1 | 25 | 13.497/14.422 | 28.026/27.124 | 1 |
| timing_null | 3 | A1_prime | GLM | 0 | 6 | 8 | 0 | 25 | 1.9251/2.1582 | 22.376/20.997 | 0 |
| timing_null | 3 | A1_prime | KLMI | 0 | 7 | 4 | 0 | 25 | 2.0963/2.2887 | 23.457/20.997 | 0 |
| timing_null | 3 | A1_prime | MVL-Ozkurt | 0 | 2 | 5 | 0 | 25 | 2.0106/1.9649 | 26.408/24.92 | 0 |
| timing_null | 3 | A1_prime | MVL-raw | 0 | 5 | 4 | 0 | 25 | 2.792/2.131 | 22.189/22.293 | 1 |
| timing_null | 3 | A2_prime | GLM | 0 | 0 | 6 | 0 | 25 | 2.4823/1.8087 | 29.043/24.904 | 0 |
| timing_null | 3 | A2_prime | KLMI | 1 | 5 | 3 | 0 | 25 | 1.9383/1.9015 | 22.404/22.83 | 0 |
| timing_null | 3 | A2_prime | MVL-Ozkurt | 2 | 4 | 6 | 0 | 25 | 2.3622/1.8803 | 24.186/22.004 | 0 |
| timing_null | 3 | A2_prime | MVL-raw | 2 | 4 | 8 | 0 | 25 | 1.9506/1.8332 | 24.587/23.096 | 0 |
| timing_null | 3 | v1.0 | APC | 0 | 5 | 0 | 0 | 25 | 5.3716/5.0182 | 24.107/25.136 | 25 |
| timing_null | 3 | v2.0 | APC | 0 | 4 | 0 | 0 | 25 | 15.216/14.997 | 29.157/29.968 | 2 |

### H4

| Dataset | Level | Config | Method | Joint /25 | fA /25 | fP /25 | Strict /25 | Valid /25 | fP error mean/median Hz | fA error mean/median Hz | Near fD /25 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| coupled | 0 | A1_prime | GLM | 16 | 25 | 16 | 1 | 25 | 0.92115/0.90587 | 1.1247/1.1702 | 0 |
| coupled | 0 | A1_prime | KLMI | 4 | 19 | 9 | 2 | 25 | 0.92304/1.0941 | 4.2909/4.8479 | 0 |
| coupled | 0 | A1_prime | MVL-Ozkurt | 4 | 23 | 6 | 2 | 25 | 1.0541/1.1816 | 2.5816/1.1702 | 0 |
| coupled | 0 | A1_prime | MVL-raw | 3 | 25 | 3 | 0 | 25 | 1.2109/1.199 | 1.0326/1.036 | 0 |
| coupled | 0 | A2_prime | GLM | 25 | 25 | 25 | 16 | 25 | 0.42519/0.37465 | 1.0344/1.036 | 0 |
| coupled | 0 | A2_prime | KLMI | 25 | 25 | 25 | 15 | 25 | 0.46492/0.40587 | 1.0883/1.036 | 0 |
| coupled | 0 | A2_prime | MVL-Ozkurt | 25 | 25 | 25 | 17 | 25 | 0.39397/0.20617 | 1.0883/1.036 | 0 |
| coupled | 0 | A2_prime | MVL-raw | 25 | 25 | 25 | 17 | 25 | 0.39397/0.20617 | 1.0883/1.036 | 0 |
| coupled | 0 | v1.0 | APC | 22 | 22 | 25 | 22 | 25 | 0.045686/0.041332 | 3.2702/1.9405 | 0 |
| coupled | 0 | v2.0 | APC | 25 | 25 | 25 | 25 | 25 | 0.0061005/0.0045129 | 0.32626/0.39515 | 0 |

![Joint recovery H1](C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/joint_recovery_H1.png)

![Joint recovery H2](C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/joint_recovery_H2.png)

## Null false recovery and AUC

Timing nulls retain the coupled burst amplitude/sigma and exact other signal/noise components; only burst timing changes. Secondary controls remove only the true-burst term. All 325 paired subtraction checks passed. [heldout_null_pair_verification.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/heldout_null_pair_verification.csv>). Specificity CSV: [heldout_null_specificity_auc.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/heldout_null_specificity_auc.csv>).

| Scenario | Null | Level | Config | Method | Score | False joint /25 | AUC | Finite coupled/null |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H1_sparsity | timing_null | 1 | A1_prime | GLM | score | 0 | 0.912 | 25/25 |
| H1_sparsity | timing_null | 1 | A1_prime | KLMI | score | 0 | 0.792 | 25/25 |
| H1_sparsity | timing_null | 1 | A1_prime | MVL-Ozkurt | score | 0 | 0.7408 | 25/25 |
| H1_sparsity | timing_null | 1 | A1_prime | MVL-raw | score | 0 | 0.9968 | 25/25 |
| H1_sparsity | timing_null | 1 | A2_prime | GLM | score | 0 | 0.9776 | 25/25 |
| H1_sparsity | timing_null | 1 | A2_prime | KLMI | score | 0 | 0.9072 | 25/25 |
| H1_sparsity | timing_null | 1 | A2_prime | MVL-Ozkurt | score | 0 | 0.9328 | 25/25 |
| H1_sparsity | timing_null | 1 | A2_prime | MVL-raw | score | 0 | 0.9952 | 25/25 |
| H1_sparsity | timing_null | 1 | v1.0 | APC | score | 5 | 0.9584 | 25/25 |
| H1_sparsity | timing_null | 1 | v2.0 | APC | score | 0 | 0.9344 | 25/25 |
| H1_sparsity | timing_null | 1 | v2.0 | APC | ozkurt_mvl | 0 | 0.9088 | 25/25 |
| H1_sparsity | timing_null | 1 | v2.0 | APC | event_z | 0 | 0.8848 | 25/25 |
| H1_sparsity | timing_null | 1 | v2.0 | APC | event_z_fixed | 0 | 0.2448 | 25/25 |
| H1_sparsity | no_coupled_burst | 1 | A1_prime | GLM | score | 0 | 0.92 | 25/25 |
| H1_sparsity | no_coupled_burst | 1 | A1_prime | KLMI | score | 0 | 0.8016 | 25/25 |
| H1_sparsity | no_coupled_burst | 1 | A1_prime | MVL-Ozkurt | score | 0 | 0.7504 | 25/25 |
| H1_sparsity | no_coupled_burst | 1 | A1_prime | MVL-raw | score | 0 | 1 | 25/25 |
| H1_sparsity | no_coupled_burst | 1 | A2_prime | GLM | score | 0 | 0.9728 | 25/25 |
| H1_sparsity | no_coupled_burst | 1 | A2_prime | KLMI | score | 0 | 0.904 | 25/25 |
| H1_sparsity | no_coupled_burst | 1 | A2_prime | MVL-Ozkurt | score | 0 | 0.928 | 25/25 |
| H1_sparsity | no_coupled_burst | 1 | A2_prime | MVL-raw | score | 0 | 1 | 25/25 |
| H1_sparsity | no_coupled_burst | 1 | v1.0 | APC | score | 2 | 0.9616 | 25/25 |
| H1_sparsity | no_coupled_burst | 1 | v2.0 | APC | score | 0 | 0.9472 | 25/25 |
| H1_sparsity | no_coupled_burst | 1 | v2.0 | APC | ozkurt_mvl | 0 | 0.904 | 25/25 |
| H1_sparsity | no_coupled_burst | 1 | v2.0 | APC | event_z | 0 | 0.8864 | 25/25 |
| H1_sparsity | no_coupled_burst | 1 | v2.0 | APC | event_z_fixed | 0 | 0.2624 | 25/25 |
| H1_sparsity | timing_null | 0.55 | A1_prime | GLM | score | 0 | 0.6496 | 25/25 |
| H1_sparsity | timing_null | 0.55 | A1_prime | KLMI | score | 0 | 0.6576 | 25/25 |
| H1_sparsity | timing_null | 0.55 | A1_prime | MVL-Ozkurt | score | 0 | 0.6832 | 25/25 |
| H1_sparsity | timing_null | 0.55 | A1_prime | MVL-raw | score | 1 | 0.9808 | 25/25 |
| H1_sparsity | timing_null | 0.55 | A2_prime | GLM | score | 0 | 0.9392 | 25/25 |
| H1_sparsity | timing_null | 0.55 | A2_prime | KLMI | score | 0 | 0.9088 | 25/25 |
| H1_sparsity | timing_null | 0.55 | A2_prime | MVL-Ozkurt | score | 0 | 0.9056 | 25/25 |
| H1_sparsity | timing_null | 0.55 | A2_prime | MVL-raw | score | 0 | 0.9696 | 25/25 |
| H1_sparsity | timing_null | 0.55 | v1.0 | APC | score | 6 | 0.9568 | 25/25 |
| H1_sparsity | timing_null | 0.55 | v2.0 | APC | score | 0 | 0.8016 | 25/25 |
| H1_sparsity | timing_null | 0.55 | v2.0 | APC | ozkurt_mvl | 0 | 0.7824 | 25/25 |
| H1_sparsity | timing_null | 0.55 | v2.0 | APC | event_z | 0 | 0.5536 | 25/25 |
| H1_sparsity | timing_null | 0.55 | v2.0 | APC | event_z_fixed | 0 | 0.2144 | 25/25 |
| H1_sparsity | timing_null | 0.25 | A1_prime | GLM | score | 0 | 0.4544 | 25/25 |
| H1_sparsity | timing_null | 0.25 | A1_prime | KLMI | score | 0 | 0.5216 | 25/25 |
| H1_sparsity | timing_null | 0.25 | A1_prime | MVL-Ozkurt | score | 0 | 0.472 | 25/25 |
| H1_sparsity | timing_null | 0.25 | A1_prime | MVL-raw | score | 0 | 0.8192 | 25/25 |
| H1_sparsity | timing_null | 0.25 | A2_prime | GLM | score | 0 | 0.7312 | 25/25 |
| H1_sparsity | timing_null | 0.25 | A2_prime | KLMI | score | 0 | 0.7168 | 25/25 |
| H1_sparsity | timing_null | 0.25 | A2_prime | MVL-Ozkurt | score | 0 | 0.7424 | 25/25 |
| H1_sparsity | timing_null | 0.25 | A2_prime | MVL-raw | score | 0 | 0.824 | 25/25 |
| H1_sparsity | timing_null | 0.25 | v1.0 | APC | score | 5 | 0.7024 | 25/25 |
| H1_sparsity | timing_null | 0.25 | v2.0 | APC | score | 0 | 0.512 | 25/25 |
| H1_sparsity | timing_null | 0.25 | v2.0 | APC | ozkurt_mvl | 0 | 0.5296 | 25/25 |
| H1_sparsity | timing_null | 0.25 | v2.0 | APC | event_z | 0 | 0.5632 | 25/25 |
| H1_sparsity | timing_null | 0.25 | v2.0 | APC | event_z_fixed | 0 | 0.352 | 25/25 |
| H1_sparsity | timing_null | 0.15 | A1_prime | GLM | score | 0 | 0.5216 | 25/25 |
| H1_sparsity | timing_null | 0.15 | A1_prime | KLMI | score | 0 | 0.5072 | 25/25 |
| H1_sparsity | timing_null | 0.15 | A1_prime | MVL-Ozkurt | score | 0 | 0.5152 | 25/25 |
| H1_sparsity | timing_null | 0.15 | A1_prime | MVL-raw | score | 0 | 0.7872 | 25/25 |
| H1_sparsity | timing_null | 0.15 | A2_prime | GLM | score | 0 | 0.6336 | 25/25 |
| H1_sparsity | timing_null | 0.15 | A2_prime | KLMI | score | 0 | 0.7136 | 25/25 |
| H1_sparsity | timing_null | 0.15 | A2_prime | MVL-Ozkurt | score | 0 | 0.656 | 25/25 |
| H1_sparsity | timing_null | 0.15 | A2_prime | MVL-raw | score | 0 | 0.7632 | 25/25 |
| H1_sparsity | timing_null | 0.15 | v1.0 | APC | score | 2 | 0.6176 | 25/25 |
| H1_sparsity | timing_null | 0.15 | v2.0 | APC | score | 0 | 0.5872 | 25/25 |
| H1_sparsity | timing_null | 0.15 | v2.0 | APC | ozkurt_mvl | 0 | 0.6352 | 25/25 |
| H1_sparsity | timing_null | 0.15 | v2.0 | APC | event_z | 0 | 0.4384 | 25/25 |
| H1_sparsity | timing_null | 0.15 | v2.0 | APC | event_z_fixed | 0 | 0.3728 | 25/25 |
| H1_sparsity | no_coupled_burst | 0.15 | A1_prime | GLM | score | 0 | 0.488 | 25/25 |
| H1_sparsity | no_coupled_burst | 0.15 | A1_prime | KLMI | score | 0 | 0.4784 | 25/25 |
| H1_sparsity | no_coupled_burst | 0.15 | A1_prime | MVL-Ozkurt | score | 0 | 0.5232 | 25/25 |
| H1_sparsity | no_coupled_burst | 0.15 | A1_prime | MVL-raw | score | 0 | 0.9072 | 25/25 |
| H1_sparsity | no_coupled_burst | 0.15 | A2_prime | GLM | score | 0 | 0.6432 | 25/25 |
| H1_sparsity | no_coupled_burst | 0.15 | A2_prime | KLMI | score | 0 | 0.7744 | 25/25 |
| H1_sparsity | no_coupled_burst | 0.15 | A2_prime | MVL-Ozkurt | score | 0 | 0.6816 | 25/25 |
| H1_sparsity | no_coupled_burst | 0.15 | A2_prime | MVL-raw | score | 0 | 0.84 | 25/25 |
| H1_sparsity | no_coupled_burst | 0.15 | v1.0 | APC | score | 1 | 0.5856 | 25/25 |
| H1_sparsity | no_coupled_burst | 0.15 | v2.0 | APC | score | 0 | 0.5648 | 25/25 |
| H1_sparsity | no_coupled_burst | 0.15 | v2.0 | APC | ozkurt_mvl | 0 | 0.5328 | 25/25 |
| H1_sparsity | no_coupled_burst | 0.15 | v2.0 | APC | event_z | 0 | 0.368 | 25/25 |
| H1_sparsity | no_coupled_burst | 0.15 | v2.0 | APC | event_z_fixed | 0 | 0.4224 | 25/25 |
| H1_distractor | timing_null | 0 | A1_prime | GLM | score | 0 | 0.8688 | 25/25 |
| H1_distractor | timing_null | 0 | A1_prime | KLMI | score | 0 | 0.7152 | 25/25 |
| H1_distractor | timing_null | 0 | A1_prime | MVL-Ozkurt | score | 0 | 0.7248 | 25/25 |
| H1_distractor | timing_null | 0 | A1_prime | MVL-raw | score | 0 | 0.9984 | 25/25 |
| H1_distractor | timing_null | 0 | A2_prime | GLM | score | 0 | 0.984 | 25/25 |
| H1_distractor | timing_null | 0 | A2_prime | KLMI | score | 0 | 0.8032 | 25/25 |
| H1_distractor | timing_null | 0 | A2_prime | MVL-Ozkurt | score | 0 | 0.8784 | 25/25 |
| H1_distractor | timing_null | 0 | A2_prime | MVL-raw | score | 0 | 0.9968 | 25/25 |
| H1_distractor | timing_null | 0 | v1.0 | APC | score | 7 | 0.968333 | 24/25 |
| H1_distractor | timing_null | 0 | v2.0 | APC | score | 2 | 0.7632 | 25/25 |
| H1_distractor | timing_null | 0 | v2.0 | APC | ozkurt_mvl | 2 | 0.7248 | 25/25 |
| H1_distractor | timing_null | 0 | v2.0 | APC | event_z | 2 | 0.7872 | 25/25 |
| H1_distractor | timing_null | 0 | v2.0 | APC | event_z_fixed | 2 | 0.3184 | 25/25 |
| H1_distractor | timing_null | 1.5 | A1_prime | GLM | score | 1 | 0.9008 | 25/25 |
| H1_distractor | timing_null | 1.5 | A1_prime | KLMI | score | 1 | 0.8192 | 25/25 |
| H1_distractor | timing_null | 1.5 | A1_prime | MVL-Ozkurt | score | 1 | 0.8176 | 25/25 |
| H1_distractor | timing_null | 1.5 | A1_prime | MVL-raw | score | 1 | 0.9984 | 25/25 |
| H1_distractor | timing_null | 1.5 | A2_prime | GLM | score | 0 | 0.9936 | 25/25 |
| H1_distractor | timing_null | 1.5 | A2_prime | KLMI | score | 0 | 0.9024 | 25/25 |
| H1_distractor | timing_null | 1.5 | A2_prime | MVL-Ozkurt | score | 0 | 0.9568 | 25/25 |
| H1_distractor | timing_null | 1.5 | A2_prime | MVL-raw | score | 1 | 0.9984 | 25/25 |
| H1_distractor | timing_null | 1.5 | v1.0 | APC | score | 4 | 0.970909 | 22/25 |
| H1_distractor | timing_null | 1.5 | v2.0 | APC | score | 0 | 0.7088 | 25/25 |
| H1_distractor | timing_null | 1.5 | v2.0 | APC | ozkurt_mvl | 0 | 0.64 | 25/25 |
| H1_distractor | timing_null | 1.5 | v2.0 | APC | event_z | 0 | 0.6576 | 25/25 |
| H1_distractor | timing_null | 1.5 | v2.0 | APC | event_z_fixed | 0 | 0.4432 | 25/25 |
| H1_distractor | timing_null | 3 | A1_prime | GLM | score | 0 | 0.8944 | 25/25 |
| H1_distractor | timing_null | 3 | A1_prime | KLMI | score | 0 | 0.7776 | 25/25 |
| H1_distractor | timing_null | 3 | A1_prime | MVL-Ozkurt | score | 0 | 0.7536 | 25/25 |
| H1_distractor | timing_null | 3 | A1_prime | MVL-raw | score | 0 | 0.9328 | 25/25 |
| H1_distractor | timing_null | 3 | A2_prime | GLM | score | 2 | 0.9728 | 25/25 |
| H1_distractor | timing_null | 3 | A2_prime | KLMI | score | 0 | 0.8432 | 25/25 |
| H1_distractor | timing_null | 3 | A2_prime | MVL-Ozkurt | score | 0 | 0.9472 | 25/25 |
| H1_distractor | timing_null | 3 | A2_prime | MVL-raw | score | 0 | 0.952 | 25/25 |
| H1_distractor | timing_null | 3 | v1.0 | APC | score | 4 | 0.923913 | 24/23 |
| H1_distractor | timing_null | 3 | v2.0 | APC | score | 0 | 0.7504 | 25/25 |
| H1_distractor | timing_null | 3 | v2.0 | APC | ozkurt_mvl | 0 | 0.6128 | 25/25 |
| H1_distractor | timing_null | 3 | v2.0 | APC | event_z | 0 | 0.7184 | 25/25 |
| H1_distractor | timing_null | 3 | v2.0 | APC | event_z_fixed | 0 | 0.6032 | 25/25 |
| H1_distractor | no_coupled_burst | 3 | A1_prime | GLM | score | 0 | 0.904 | 25/25 |
| H1_distractor | no_coupled_burst | 3 | A1_prime | KLMI | score | 0 | 0.7632 | 25/25 |
| H1_distractor | no_coupled_burst | 3 | A1_prime | MVL-Ozkurt | score | 0 | 0.768 | 25/25 |
| H1_distractor | no_coupled_burst | 3 | A1_prime | MVL-raw | score | 0 | 0.9328 | 25/25 |
| H1_distractor | no_coupled_burst | 3 | A2_prime | GLM | score | 2 | 0.9584 | 25/25 |
| H1_distractor | no_coupled_burst | 3 | A2_prime | KLMI | score | 1 | 0.856 | 25/25 |
| H1_distractor | no_coupled_burst | 3 | A2_prime | MVL-Ozkurt | score | 0 | 0.9392 | 25/25 |
| H1_distractor | no_coupled_burst | 3 | A2_prime | MVL-raw | score | 0 | 0.9488 | 25/25 |
| H1_distractor | no_coupled_burst | 3 | v1.0 | APC | score | 8 | 0.939236 | 24/24 |
| H1_distractor | no_coupled_burst | 3 | v2.0 | APC | score | 0 | 0.7584 | 25/25 |
| H1_distractor | no_coupled_burst | 3 | v2.0 | APC | ozkurt_mvl | 0 | 0.6416 | 25/25 |
| H1_distractor | no_coupled_burst | 3 | v2.0 | APC | event_z | 0 | 0.6784 | 25/25 |
| H1_distractor | no_coupled_burst | 3 | v2.0 | APC | event_z_fixed | 0 | 0.5968 | 25/25 |
| H2 | timing_null | 0 | A1_prime | GLM | score | 0 | 1 | 25/25 |
| H2 | timing_null | 0 | A1_prime | KLMI | score | 0 | 0.9984 | 25/25 |
| H2 | timing_null | 0 | A1_prime | MVL-Ozkurt | score | 0 | 0.9792 | 25/25 |
| H2 | timing_null | 0 | A1_prime | MVL-raw | score | 1 | 1 | 25/25 |
| H2 | timing_null | 0 | A2_prime | GLM | score | 0 | 1 | 25/25 |
| H2 | timing_null | 0 | A2_prime | KLMI | score | 0 | 1 | 25/25 |
| H2 | timing_null | 0 | A2_prime | MVL-Ozkurt | score | 0 | 1 | 25/25 |
| H2 | timing_null | 0 | A2_prime | MVL-raw | score | 0 | 1 | 25/25 |
| H2 | timing_null | 0 | v1.0 | APC | score | 2 | 1 | 25/25 |
| H2 | timing_null | 0 | v2.0 | APC | score | 0 | 0.664 | 25/25 |
| H2 | timing_null | 0 | v2.0 | APC | ozkurt_mvl | 0 | 0.6432 | 25/25 |
| H2 | timing_null | 0 | v2.0 | APC | event_z | 0 | 0.4704 | 25/25 |
| H2 | timing_null | 0 | v2.0 | APC | event_z_fixed | 0 | 0.3712 | 25/25 |
| H2 | timing_null | 1 | A1_prime | GLM | score | 2 | 0.992 | 25/25 |
| H2 | timing_null | 1 | A1_prime | KLMI | score | 2 | 0.9664 | 25/25 |
| H2 | timing_null | 1 | A1_prime | MVL-Ozkurt | score | 0 | 0.8784 | 25/25 |
| H2 | timing_null | 1 | A1_prime | MVL-raw | score | 1 | 0.9984 | 25/25 |
| H2 | timing_null | 1 | A2_prime | GLM | score | 0 | 1 | 25/25 |
| H2 | timing_null | 1 | A2_prime | KLMI | score | 0 | 1 | 25/25 |
| H2 | timing_null | 1 | A2_prime | MVL-Ozkurt | score | 0 | 0.9728 | 25/25 |
| H2 | timing_null | 1 | A2_prime | MVL-raw | score | 0 | 1 | 25/25 |
| H2 | timing_null | 1 | v1.0 | APC | score | 1 | 0.816667 | 24/25 |
| H2 | timing_null | 1 | v2.0 | APC | score | 0 | 0.5072 | 25/25 |
| H2 | timing_null | 1 | v2.0 | APC | ozkurt_mvl | 0 | 0.5072 | 25/25 |
| H2 | timing_null | 1 | v2.0 | APC | event_z | 0 | 0.496 | 25/25 |
| H2 | timing_null | 1 | v2.0 | APC | event_z_fixed | 0 | 0.3744 | 25/25 |
| H2 | timing_null | 3 | A1_prime | GLM | score | 0 | 0.552 | 25/25 |
| H2 | timing_null | 3 | A1_prime | KLMI | score | 0 | 0.5616 | 25/25 |
| H2 | timing_null | 3 | A1_prime | MVL-Ozkurt | score | 0 | 0.5248 | 25/25 |
| H2 | timing_null | 3 | A1_prime | MVL-raw | score | 0 | 0.704 | 25/25 |
| H2 | timing_null | 3 | A2_prime | GLM | score | 0 | 0.6112 | 25/25 |
| H2 | timing_null | 3 | A2_prime | KLMI | score | 1 | 0.5696 | 25/25 |
| H2 | timing_null | 3 | A2_prime | MVL-Ozkurt | score | 2 | 0.5104 | 25/25 |
| H2 | timing_null | 3 | A2_prime | MVL-raw | score | 2 | 0.6 | 25/25 |
| H2 | timing_null | 3 | v1.0 | APC | score | 0 | 0.536 | 25/25 |
| H2 | timing_null | 3 | v2.0 | APC | score | 0 | 0.6048 | 25/25 |
| H2 | timing_null | 3 | v2.0 | APC | ozkurt_mvl | 0 | 0.5952 | 25/25 |
| H2 | timing_null | 3 | v2.0 | APC | event_z | 0 | 0.5056 | 25/25 |
| H2 | timing_null | 3 | v2.0 | APC | event_z_fixed | 0 | 0.4144 | 25/25 |

## Event p<0.05 rates

event_p is the primary full-grid max-BLP test; event_p_fixed is the secondary uncorrected fixed-frequency test. [heldout_event_rejection_rates.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/heldout_event_rejection_rates.csv>).

| Scenario | Dataset | Level | Statistic | Rejected /25 | Finite p /25 | Rate |
| --- | --- | --- | --- | --- | --- | --- |
| H1_sparsity | coupled | 1 | event_p | 4 | 25 | 0.16 |
| H1_sparsity | coupled | 1 | event_p_fixed | 7 | 25 | 0.28 |
| H1_sparsity | timing_null | 1 | event_p | 0 | 25 | 0 |
| H1_sparsity | timing_null | 1 | event_p_fixed | 17 | 25 | 0.68 |
| H1_sparsity | no_coupled_burst | 1 | event_p | 0 | 25 | 0 |
| H1_sparsity | no_coupled_burst | 1 | event_p_fixed | 11 | 25 | 0.44 |
| H1_sparsity | coupled | 0.55 | event_p | 0 | 25 | 0 |
| H1_sparsity | coupled | 0.55 | event_p_fixed | 8 | 25 | 0.32 |
| H1_sparsity | timing_null | 0.55 | event_p | 0 | 25 | 0 |
| H1_sparsity | timing_null | 0.55 | event_p_fixed | 18 | 25 | 0.72 |
| H1_sparsity | coupled | 0.25 | event_p | 0 | 25 | 0 |
| H1_sparsity | coupled | 0.25 | event_p_fixed | 15 | 25 | 0.6 |
| H1_sparsity | timing_null | 0.25 | event_p | 0 | 25 | 0 |
| H1_sparsity | timing_null | 0.25 | event_p_fixed | 19 | 25 | 0.76 |
| H1_sparsity | coupled | 0.15 | event_p | 0 | 25 | 0 |
| H1_sparsity | coupled | 0.15 | event_p_fixed | 16 | 25 | 0.64 |
| H1_sparsity | timing_null | 0.15 | event_p | 0 | 25 | 0 |
| H1_sparsity | timing_null | 0.15 | event_p_fixed | 20 | 25 | 0.8 |
| H1_sparsity | no_coupled_burst | 0.15 | event_p | 0 | 25 | 0 |
| H1_sparsity | no_coupled_burst | 0.15 | event_p_fixed | 18 | 25 | 0.72 |
| H1_distractor | coupled | 0 | event_p | 1 | 25 | 0.04 |
| H1_distractor | coupled | 0 | event_p_fixed | 7 | 25 | 0.28 |
| H1_distractor | timing_null | 0 | event_p | 0 | 25 | 0 |
| H1_distractor | timing_null | 0 | event_p_fixed | 16 | 25 | 0.64 |
| H1_distractor | coupled | 1.5 | event_p | 0 | 25 | 0 |
| H1_distractor | coupled | 1.5 | event_p_fixed | 12 | 25 | 0.48 |
| H1_distractor | timing_null | 1.5 | event_p | 0 | 25 | 0 |
| H1_distractor | timing_null | 1.5 | event_p_fixed | 16 | 25 | 0.64 |
| H1_distractor | coupled | 3 | event_p | 1 | 25 | 0.04 |
| H1_distractor | coupled | 3 | event_p_fixed | 17 | 25 | 0.68 |
| H1_distractor | timing_null | 3 | event_p | 0 | 25 | 0 |
| H1_distractor | timing_null | 3 | event_p_fixed | 15 | 25 | 0.6 |
| H1_distractor | no_coupled_burst | 3 | event_p | 0 | 25 | 0 |
| H1_distractor | no_coupled_burst | 3 | event_p_fixed | 17 | 25 | 0.68 |
| H2 | coupled | 0 | event_p | 1 | 25 | 0.04 |
| H2 | coupled | 0 | event_p_fixed | 13 | 25 | 0.52 |
| H2 | timing_null | 0 | event_p | 0 | 25 | 0 |
| H2 | timing_null | 0 | event_p_fixed | 18 | 25 | 0.72 |
| H2 | coupled | 0.5 | event_p | 1 | 25 | 0.04 |
| H2 | coupled | 0.5 | event_p_fixed | 7 | 25 | 0.28 |
| H2 | coupled | 1 | event_p | 0 | 25 | 0 |
| H2 | coupled | 1 | event_p_fixed | 11 | 25 | 0.44 |
| H2 | timing_null | 1 | event_p | 0 | 25 | 0 |
| H2 | timing_null | 1 | event_p_fixed | 16 | 25 | 0.64 |
| H2 | coupled | 1.5 | event_p | 0 | 25 | 0 |
| H2 | coupled | 1.5 | event_p_fixed | 18 | 25 | 0.72 |
| H2 | coupled | 2 | event_p | 0 | 25 | 0 |
| H2 | coupled | 2 | event_p_fixed | 12 | 25 | 0.48 |
| H2 | coupled | 3 | event_p | 0 | 25 | 0 |
| H2 | coupled | 3 | event_p_fixed | 15 | 25 | 0.6 |
| H2 | timing_null | 3 | event_p | 0 | 25 | 0 |
| H2 | timing_null | 3 | event_p_fixed | 19 | 25 | 0.76 |
| H4 | coupled | 0 | event_p | 24 | 25 | 0.96 |
| H4 | coupled | 0 | event_p_fixed | 24 | 25 | 0.96 |

## Runtime and deviations

| Stage | Elapsed seconds | Status |
| --- | --- | --- |
| Unit gates | 167.734 | UNIT_GATES_PASSED |
| generate | 10.6919 | COMPLETE |
| worker_1 | 529.009 | COMPLETE |
| worker_2 | 529.948 | COMPLETE |
| worker_3 | 531.967 | COMPLETE |

Workers ran concurrently with one computation thread each; summing their elapsed seconds is not wall time. MATLAB startup, implementation and report assembly are excluded from these stage timers. Input generation and all worker logs are preserved beside the results.

Tooling deviations: Python initially lacked matplotlib on its default path; the existing workspace pydeps copy was used (matplotlib 3.11.1). No package download or method change was needed. Pre-existing missing Brainstorm startup-path warnings were retained. UTF-8 text I/O is explicit. No held-out trial was removed or regenerated; invalid outputs are counted. No method change or parameter tuning occurred after tagging. Any additional tooling deviations are recorded in [tooling_deviations.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/tooling_deviations.json>).

## Full provenance

All trial/summary CSVs store commit, MATLAB version, full APC/comparator options and seed. Input MAT files store signals/components/streams/settings; worker checkpoints store curves and both surrogate-statistic vectors. Figures embed the full metadata. Input hash and protected-output checks: [final_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/final_verification.json>).

```json
{
  "candidate": 3,
  "git_commit": "217fd8373759150cdeffe794d231a7cec2225f38",
  "git_tag": "v2.0",
  "matlab_version": "9.13.0.2105380 (R2022b) Update 2",
  "seed": 20261022.0,
  "apc_source_blob": "7fc5e8c2f0ad32a79df652beb824e6d14b46d67e",
  "unit_tested_source_blob": "7fc5e8c2f0ad32a79df652beb824e6d14b46d67e",
  "unit_test_base_commit": "7848af05ada722971769da856e970d0737820169",
  "unit_gates": {
    "a": "PASS",
    "a2": "PASS",
    "b": "PASS",
    "c": "PASS",
    "d": "COMPLETE"
  },
  "apc_configurations": {
    "v2": {
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
      "eventSurrogateSeed": 20261022.0,
      "eventSurrogateSubstream": 1001
    },
    "v1": {
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
      "version": "v1"
    }
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
    "filter": "butter(4) bandpass, filtfilt (8th-order bandpass)",
    "cutoff_clamps": [
      0.0001,
      0.999
    ],
    "amplitude_clipping": "[max(1,fA-half),min(fs/2-1,fA+half)]",
    "metrics": [
      "MVL-raw",
      "MVL-Ozkurt",
      "KLMI",
      "GLM"
    ],
    "phase_bins": 18,
    "Ozkurt": "raw_MVL/sqrt(mean(A.^2))",
    "GLM": "max(0,1-SSE/SST), X=[ones sin(phase) cos(phase)]",
    "selection": "independent full-grid maximum, first column-major tie",
    "surrogates": false
  },
  "streams": {
    "generator": "mrg32k3a",
    "seed": 20261022.0,
    "signal_substream": 1,
    "frequency_substream": 2,
    "poisson_substream": 3,
    "event_substream": "1000+input_id"
  },
  "recovery": {
    "phase_tolerance_hz": 1,
    "strict_phase_tolerance_hz": 0.5,
    "amplitude_tolerance_hz": 8,
    "invalid": "recovery failure",
    "AUC": "finite scores, greater + half ties"
  },
  "generator_profiles": {
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
    },
    "slow": {
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
      "snr_db": -3,
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
    }
  },
  "protocol": "GOAL: Implement APC v2 to a fixed specification, freeze it, then evaluate it on a NEW held-out simulation suite against fair comparators, using decision criteria written before any held-out result exists.\r\n\r\nRULES\r\n- New branch \"v2-revision\" from tag v1.0 in apc-brainstorm-publish. Never rewrite earlier commits, tags or saved results. New outputs go to revision_checks/v2/.\r\n- Write revision_checks/v2/PROTOCOL_v2.md (this spec, including the decision criteria verbatim) and commit it WITH the v2 code BEFORE generating any held-out data.\r\n- No parameter tuning. You may fix implementation bugs found by the unit tests before tagging; list every one. After tagging, nothing in the method changes.\r\n- Provenance (commit, MATLAB version, full options, seeds) goes in every output. Tooling errors may be fixed and resumed (log them as deviations); stop on anything method-relevant.\r\n\r\nPART 1 \u2014 v2 SPECIFICATION (new mode in bst_apc.m: version='v2'; v1 behaviour stays selectable and unchanged)\r\nStep 1 (bursts): unchanged from v1.0 (RMS CWT burst trace over the amplitude search range, 20-ms smoothing, prominence 0.75 SD, minimum spacing as in v1.0). Record the burst times t_k and the burst count.\r\nStep 2 (fP by burst-phase locking):\r\n  - Candidate grid f = fmin:0.1:fmax, where fmin = max(minPhaseHz, 10/record_duration_s), fmax = min(maxPhaseHz, ampRange(1)/2, fs/3). Defaults minPhaseHz=1, maxPhaseHz=30.\r\n  - For each f: zero-phase 4th-order Butterworth bandpass of x(t) with half-width max(0.5, 0.25*f); phase from the Hilbert transform; exclude bursts within 1/f of the record edges; compute pairwise phase consistency PPC(f) (Vinck et al. 2010) over the burst phases.\r\n  - fP = the grid argmax of PPC, refined by 3-point parabolic interpolation when both neighbours are on the grid.\r\n  - Status 3 if there are fewer than 10 usable bursts or no finite PPC.\r\nStep 3 (diagnostics only): v1.0 burst-triggered average and trough-locked profiling at the v2 fP. Their failure must NOT stop the analysis: return a warning flag and continue. The polarity flip is used only for this display.\r\nStep 4 (fA): candidate fA = ampRange(1):1:ampRange(2). For each, a band of half-width fP (clipped to ampRange and Nyquist), zero-phase 4th-order Butterworth, Hilbert envelope; score = raw Canolty MVL between the fP phase (Step 2 filter) and that envelope. Smooth the score with a 3-point moving mean; fA = argmax. C_APC = raw MVL at (fP, fA); also report Ozkurt-normalized MVL.\r\nEvent coupling test (new output): PPC at fP versus 200 surrogates in which every burst time is independently jittered by uniform +/- 1/fP seconds (bursts kept inside the record). Report z = (PPC - mean_surr)/sd_surr and an empirical p = (1 + #surr >= obs)/(201). Seed the surrogate RNG separately and record it.\r\nOutputs: fP, fA, C_APC, Ozkurt MVL, event PPC, z, p, burst count, diagnostic flags, status.\r\n\r\nPART 2 \u2014 UNIT TESTS (before tagging)\r\n(a) A pure 8-Hz carrier with 120-Hz bursts locked to the trough, high SNR: v2 returns fP within 0.1 Hz of 8 and fA within 4 Hz of 120.\r\n(b) The same with an added uncoupled 11-Hz sinusoid at 3x amplitude: v2 fP within 0.5 Hz of 8.\r\n(c) Poisson burst times: event-test p > 0.05 in at least 8 of 10 seeds.\r\n(d) Run v2 on 25 trials of the existing distractor benchmark (seed 20260618) to check it runs. Report the results but do not tune on them.\r\nIf (a)\u2013(c) pass: commit and tag \"v2.0\", and record the hash. If they fail: report and stop.\r\n\r\nPART 3 \u2014 HELD-OUT SUITE (new seed 20261022; separate RNG streams for signals, frequencies, Poisson nulls and surrogates)\r\nUse the existing generator formulas (Gaussian bursts sigma 28 ms, jitter 10 ms, coupling 0.60, mixed pink+white noise at -3 dB, fs 500 Hz).\r\nH1 random-pair: per trial, fP ~ U(5,11), fA ~ U(90,140).\r\n  H1-sparsity: 8 s, keep rates {1, 0.55, 0.25, 0.15}, background bursts as in v1.0.\r\n  H1-distractor: 6 s, uncoupled distractor burst band at fA - 24 Hz, scales {0, 1.5, 3}.\r\nH2 slow distractor: 6 s, coupled fP ~ U(4,7), uncoupled sinusoid at fD ~ U(fP+3, 13) with a random phase, amplitude ratios {0, 0.5, 1, 1.5, 2, 3}, fA ~ U(90,140).\r\nH3 nulls: a paired timing null (Poisson burst times at the matched mean rate, everything else identical) for every H1 level and for H2 ratios {0, 1, 3}; a no-coupled-burst control for H1 keep rates {1, 0.15} and H1 distractor scale 3.\r\nH4 continuous-PAC boundary: 25 trials, random fP/fA, continuous amplitude modulation (as in the v1 canonical condition).\r\n25 repeats per level throughout.\r\n\r\nPART 4 \u2014 METHODS ON THE HELD-OUT SUITE\r\n- APC v2.0 (primary).\r\n- APC v1.0 (reference).\r\n- Comparators: MVL-raw, MVL-Ozkurt, KLMI and GLM scans. Phase grid 3:0.5:14 Hz, phase half-width 1.5 Hz, amplitude grid 80:4:160 Hz, amplitude half-width fixed at 14 Hz (= 2*max fP rule) \u2014 call this A2'. Also run the comparators with half-width = candidate fP (A1').\r\n- Amplitude search range for APC: [80, 160].\r\n- If Brainstorm's tPAC can run headless from the local Brainstorm install without code changes, add it with its defaults and the same ranges; otherwise skip it and say so.\r\nTolerances: joint = |fP err| <= 1 Hz and |fA err| <= 8 Hz; strict joint uses |fP err| <= 0.5 Hz. Invalid outputs count as failures.\r\n\r\nPART 5 \u2014 DECISION CRITERIA (evaluate on held-out data only; \"best A2'\" = the best A2' metric chosen per level, which favours the comparators)\r\nC1 (core claim): H2 pooled over ratios {1, 1.5, 2, 3} (100 trials): v2 joint recovery >= best A2' minus 5, AND v2 picks within 1 Hz of fD in <= 10/100.\r\nC2 (precision): H1 pooled (175 trials): v2 strict-joint recovery > best A2' strict-joint, one-sided exact McNemar p < 0.05.\r\nC3 (specificity): pooled timing-null false joint recovery for v2 <= best A2' + 5 per 100 trials; AUC of the v2 event z (coupled vs paired timing null) >= 0.90 at H1 keep rates {1, 0.55} and all H1 distractor scales.\r\nC4 (recovery): H1 pooled joint recovery for v2 >= best A2' minus 9 (5% of 175).\r\nReport PASS/FAIL for each criterion with the numbers. Do not interpret.\r\n\r\nOUTPUT\r\nrevision_checks/v2/RESULTS_v2.md plus CSVs. Include:\r\n1. Unit-test results and the tag hash.\r\n2. Per scenario/level/method tables: joint / fA / fP / strict joint, error mean and median, picks near fD (H2), valid count.\r\n3. Null false recovery and AUCs (C_APC, Ozkurt MVL and event z for v2; scores for the comparators).\r\n4. The event-test p < 0.05 rate in coupled and in null trials.\r\n5. The C1\u2013C4 table.\r\n6. A factual summary of at most 10 lines, runtime and deviations.\r\nAlso save joint-recovery figures for H1 and H2.\r\n\r\nIMPLEMENTATION DETAILS FIXED BEFORE UNIT OR HELD-OUT OUTCOMES\r\n\r\n- Requested output protocol is mirrored byte-for-byte in the tracked\r\n  analysis/v2_revision/PROTOCOL_v2.md because revision_checks/v2 is outside\r\n  the Git repository. Commit both code and the tracked protocol together.\r\n- version='v2' dispatches to the new algorithm. Absent version, version='v1'\r\n  and version='v1.0' retain all existing v1 calculations and outputs.\r\n- Fourth-order Butterworth means fourth-order bandpass in total, implemented\r\n  by butter(2, [low high]/Nyquist), zp2sos and filtfilt, as in v1's amplitude\r\n  filter family. Step 1 calls the unchanged v1 helper functions directly.\r\n- Record duration is N/fs. Event edge guards use first/last sampled times.\r\n  The literal candidate grid is fmin:0.1:fmax, without appending an endpoint.\r\n  A candidate needs >=10 edge-usable burst events; otherwise its PPC is NaN.\r\n  PPC=(abs(sum(exp(1i*phase)))^2-N)/(N*(N-1)), without clipping negative values.\r\n  Reference: Vinck et al. 2010, equations 14-15,\r\n  https://doi.org/10.1016/j.neuroimage.2010.01.073 .\r\n- Refine an interior concave peak with a parabola through the three raw PPC\r\n  values; finite neighbors required, offset bounded to half a grid interval.\r\n  Refilter and reapply event guards at the final refined fP. Status 3 if fewer\r\n  than ten events remain. Step 4 and event tests use this final phase filter.\r\n- Three-point amplitude-score smoothing uses a centered moving mean with\r\n  shortened endpoint windows. Report raw MVL at the selected fA, not the\r\n  smoothed selection score. Ties choose the first grid point.\r\n- Event-test surrogates jitter each event in the observed fP-usable subset.\r\n  Its 1/fP edge margin guarantees all independent uniform +/-1/fP jitters\r\n  remain in the record; do not impose a second edge guard on surrogates.\r\n  Evaluate continuous jitter times by linear interpolation of unwrapped\r\n  Hilbert phase. Use sample SD (N-1); zero SD yields z=NaN and warning bit 16.\r\n  Always 200 surrogates. RNG is a local mrg32k3a stream with recorded seed\r\n  and substream; it must not change the simulation/global RNG state.\r\n- Diagnostic warning bits: 1=no complete burst-average epochs; 2=no troughs;\r\n  4=no complete trough profiling epochs; 8=diagnostic exception;\r\n  16=zero/nonfinite surrogate SD. Diagnostics never choose fP or fA and their\r\n  failure never changes method success status. Record exceptions explicitly.\r\n- Unit (a): six-second 500-Hz signal, 8-Hz sine amplitude 1, 120-Hz carrier,\r\n  base carrier amplitude .08, Gaussian bursts sigma .028 s, amplitude\r\n  1.3*.60, original .010-s jitter centered on physical troughs, 20-dB mixed\r\n  pink/white noise. Use original distractor-generator formulas, omitting the\r\n  entire 96-Hz component. Seed 20260618; amplitude range [80,160].\r\n- Unit (b): the exact same signal/noise as (a), plus 3*sin(2*pi*11*t+phi),\r\n  phi uniform from a separate mrg32k3a stream, seed 20260619, substream 1.\r\n- Unit (c): ten seeds 20260618:20260627, same unit profile. Replace only the\r\n  true-burst component with homogeneous Poisson events at 8 Hz, original\r\n  extended support, overlaps allowed, original envelope normalization and\r\n  paired noise. A separate mrg32k3a stream (seed=trial seed, substream=3)\r\n  supplies Poisson draws; surrogate seed=trial seed+1, substream=2.\r\n- Unit (d): first 25 saved coupled distractor trials (level 0) in the original\r\n  seed-20260618 trial order. Check runs, report all statuses and recovery;\r\n  never use them to alter the method.\r\n- Run gates sequentially. On any performance gate failure, save the completed\r\n  test rows and STOP: no remaining tests, v2.0 tag or held-out generation.\r\n  An identifiable implementation bug may be corrected before tagging, with\r\n  every correction logged; no parameter or unit-signal retuning is allowed.\r\n- Before performance gates, verify unchanged v1 outputs against a renamed\r\n  copy from tag v1.0 on five saved inputs, and verify PPC against explicit\r\n  pairwise cosines, burst detection identity and no global RNG consumption.\r\n- Held-out streams will be mrg32k3a with seed 20261022 and distinct substreams\r\n  for signals, frequencies, Poisson events and event-test surrogates. Record\r\n  the full stream/substream map before any held-out data are generated.\r\n- If gates pass, build and commit the held-out execution scripts and full\r\n  comparator/decision bookkeeping before tagging and generating any data.\r\n  Additional bookkeeping choices must not alter the fixed method or criteria.\r\n\r\n## Candidate history\r\n\r\nCandidate 1 (commit 7848af05ada722971769da856e970d0737820169) failed unit\r\ngate (a): fP=10.631999875603938 Hz, fA=120 Hz. The user identified that PPC\r\nis flat across filter centers whose passband contains the coupled rhythm;\r\nthe recorded curve is unit_attempt_01/unit_a_ppc_curve.csv. The five v1\r\ncompatibility cases and implementation invariants passed. No v2.0 tag or\r\nheld-out data were created. Candidate-1 protocol/report/manifest copies are\r\npreserved in revision_checks/v2/candidate_01 and its unit records are unchanged.\r\n\r\nCandidate 2 is the final candidate authorized by the user. The following\r\namendment replaces only Step 2, the event test, and the additional ordered\r\nunit gate (a2). All earlier Step-2/PPC-event implementation notes above are\r\nhistorical candidate-1 notes and are superseded by this amendment. All other\r\nmethod settings, generators, unit profiles/seeds, held-out suite and C1-C4\r\nremain exactly as committed in 7848af0. No further candidates will be made.\r\n\r\n### Candidate 2: Step 2 replacement (burst-locked power)\r\n\r\n- L=2 seconds. Usable burst centers have the complete half-open window\r\n  [t_k-L/2,t_k+L/2) in the half-open record [t0,t0+T). Status 1 for T<4 s;\r\n  status 3 for fewer than ten usable bursts.\r\n- Extract L*fs samples at relative times -L/2:1/fs:L/2-1/fs; demean each\r\n  segment and multiply by a symmetric Hann window of that length.\r\n- Evaluate X_k(f)=sum_t w(t)*s_k(t)*exp(-i*2*pi*f*t) directly, on the grid\r\n  fmin:0.05:fmax, fmin=max(minPhaseHz,10/T,3/L), fmax as originally specified.\r\n- BLP(f)=(abs(sum_k X_k(f))^2-sum_k abs(X_k(f))^2)/(N*(N-1)). Select its\r\n  grid maximum; refine with a three-point parabola on raw BLP when both\r\n  neighbors are finite and on the grid. Use the inherited half-bin bound.\r\n- PPC of the X_k phases is diagnostic only, on the entire grid and at the\r\n  refined fP. No polarity flip is applied anywhere in Step 2.\r\n- The phase reference for Steps 3-4 remains the original fourth-order\r\n  zero-phase Butterworth at fP, half-width=max(0.5,0.25*fP).\r\n\r\n### Candidate 2: event test replacement\r\n\r\n- Primary statistic: maximum BLP on the full candidate grid. For each of\r\n  200 surrogates, independently jitter each usable burst by uniform\r\n  +/-1/fP seconds, conditioned on remaining within the window-usable center\r\n  range. Implement this conditional uniform draw using its truncated interval\r\n  per burst, which is equivalent to rejecting out-of-range uniform jitters.\r\n- Recompute BLP on the entire grid for each surrogate and use its maximum.\r\n  z=(observed maximum-mean surrogate maxima)/sample SD; empirical\r\n  p=(1+number of surrogate maxima >= observed maximum)/201.\r\n- Secondary uncorrected statistic: BLP at the refined observed fP, evaluated\r\n  at that same fixed frequency in each surrogate. Report separate z and p.\r\n- Jitter times are continuous. Segment samples use linear interpolation of\r\n  x at those centers. Demeaning, Hann multiplication and direct Fourier\r\n  evaluation are linear: batch the direct coefficient computation at unique\r\n  bracketing sample centers and interpolate coefficients. Validate against\r\n  independently extracted/interpolated segments and direct sums. No FFT-bin\r\n  approximation or frequency interpolation is used.\r\n- Record the local RNG seed/substream and both 200-element surrogate\r\n  statistic vectors. No change to signal RNG state is permitted.\r\n\r\n### Candidate 2: ordered unit gates and freeze\r\n\r\n1. (a) unchanged high-SNR 8/120-Hz trial and seed 20260618; phase tolerance\r\n   0.1 Hz, amplitude tolerance 4 Hz.\r\n2. (a2) the same unit generator, each initialized with the same original\r\n   seed 20260618, at fP in [5.3,6.7,9.4,10.8] Hz, in that order. All four\r\n   require absolute fP error <=0.1 Hz. All other unit parameters are unchanged.\r\n3. (b), (c), (d) unchanged, in that order.\r\n\r\nSave BLP and PPC curves for every completed unit trial, including null and\r\nexisting-benchmark trials. Stop at the first failed gate; no further\r\ncandidates. Test candidate-2 working sources before committing; record the\r\ncandidate-1 base commit plus exact working-source/protocol/script hashes.\r\nOnly if all gates pass, commit candidate 2 with its protocol and execution\r\nscripts, verify the tested source hashes, tag v2.0, then generate and run the\r\noriginal held-out suite at seed 20261022. In the held-out event test, the\r\nprimary statistic and z/p are now the max-BLP statistics above. C1-C4 are\r\nunchanged, including every threshold and paired decision calculation.\r\nNew candidate-2 outputs are under revision_checks/v2/candidate_02; candidate-1\r\nsaved results remain unchanged.\r\n\r\n### Candidate history: candidate 2 and final candidate 3\r\n\r\nCandidate 2 failed gate (a) only on fA: fP=7.9996901239320914 Hz passed;\r\nfA=115 Hz had error 5 Hz, exceeding the allowed 4 Hz. The user's diagnosis\r\nis that the Step-4 score versus center frequency is bimodal, with peaks near\r\nfA +/- fP and a dip at fA, because a flat-top Butterworth band of half-width\r\nfP puts the modulation sidebands at its edges. The candidate-2 source and\r\nits unit report/curves remain preserved in revision_checks/v2/candidate_02.\r\n\r\nThe user has now authorized candidate 3 as the final candidate. This later\r\nauthorization supersedes the candidate-2 instruction that no further\r\ncandidate would be made. Only Step 4 and the specified a2 pairs change.\r\nCandidate-2 Step 2 (BLP), both event-test statistics, Steps 1/3, the unit\r\nprofiles/seeds, the held-out suite and C1-C4 remain unchanged. No further\r\ncandidate is authorized after candidate 3.\r\n\r\n### Candidate 3: Step 4 replacement (peaked kernel)\r\n\r\n- Candidate centers fc are the unchanged 1-Hz grid within ampRange.\r\n- Reflect x for one second at each end. The precise reflection convention\r\n  excludes a repeated endpoint: x(p+1:-1:2), x, x(end-1:-1:end-p), p=round(fs).\r\n- FFT the padded signal at its actual length. On the signed-frequency grid,\r\n  multiply by G(f)=2*exp(-(f-fc)^2/(2*sigma^2)) for f>0 and zero for f<=0,\r\n  sigma=1.5*fP; inverse FFT and crop exactly p samples at each end. The\r\n  positive Nyquist bin, when present, follows the literal positive-frequency\r\n  formula. Do not clip the Gaussian tails to ampRange.\r\n- Envelope=absolute analytic band signal; score=raw Canolty MVL with the\r\n  unchanged fP phase reference. No moving-mean smoothing.\r\n- Select the grid maximum and refine with a three-point parabola on raw\r\n  score when both neighbors are inside ampRange and the maximum is concave.\r\n  Retain the inherited half-bin bound and first-grid-point tie handling.\r\n- Recompute the Gaussian envelope at the refined fA. Report raw C_APC and\r\n  conventional Ozkurt MVL from that same envelope. Gaussian sigma is output\r\n  explicitly; obsolete finite rectangular-band-width fields are NaN.\r\n- Save the raw fA score curve for every completed unit trial, alongside its\r\n  BLP and PPC curves. If Step 4 was not reached, save the prescribed center\r\n  grid with NaN scores and an explicit step4_reached=false flag.\r\n\r\n### Candidate 3: unit gates and conditional freeze\r\n\r\nRun the same sequential stopping rule: (a), (a2), (b), (c), (d).\r\n(a) remains |fP-8|<=0.1 Hz and |fA-120|<=4 Hz.\r\n(a2) now uses the four true pairs in order: (5.3,95), (6.7,108), (9.4,131),\r\n(10.8,142), each with the same unchanged generator and seed scheme; both\r\n|fP error|<=0.1 Hz and |fA error|<=4 Hz are required for every trial.\r\n(b), (c), (d) remain exactly as specified for candidate 2.\r\n\r\nBefore the performance gates, retain the inherited mathematical/compatibility\r\nchecks and verify Step-2 and event outputs match the saved candidate-2 unit\r\n(a) exactly on its unchanged signal. Validate the Gaussian envelope/score\r\nagainst the literal FFT formula. These checks do not change any method.\r\n\r\nOnly if all gates pass, commit candidate 3 with its protocol and execution\r\nscripts, verify tested source hashes, tag v2.0, then generate/run the original\r\nheld-out suite and unchanged comparators/criteria at seed 20261022. On any\r\ngate failure, stop and report; no further candidates. Candidate-3 outputs\r\nare kept separately under revision_checks/v2/candidate_03. Earlier saved\r\ncandidate reports, curves, inputs and source snapshots are not overwritten.\r\n",
  "execution": "# Held-out execution bookkeeping, fixed before data generation\n\nThe method is the tested candidate-3 source. This file supplies execution\ndetails for Parts 3-5 without changing their suite or decision thresholds.\nPROTOCOL_v2.md retains the original C1-C4 text verbatim.\n\nSeed 20261022, mrg32k3a: substream 1 generates signals; substream 2 supplies\nfrequency/independent sinusoid-phase draws; substream 3 supplies Poisson\nevents; each analyzed input has event-surrogate substream 1000+input_id.\nAll seeds, substreams, draw order and full generator/method settings are\nstored. Analysis does not consume the signal stream. Generators retain\ntheir original formulas and unused legacy draws. No data are generated\nuntil the tested source is committed and tagged v2.0.\n\nOrder: H1-sparsity levels [1,.55,.25,.15], H1-distractor [0,1.5,3],\nH2 ratios [0,.5,1,1.5,2,3], H4 continuous; 25 repeats per level. H1/H4 draw\nfP then fA from U(5,11) and U(90,140). H2 draws fP from U(4,7), fD from\nU(fP+3,13), a uniform independent 10-like-sinusoid phase, then fA U(90,140).\nThe actual H2 distractor frequency is its fD draw, not a fixed 10 Hz.\nAll methods receive the identical saved input and truth is used only for\ngeneration and scoring, never to select a method frequency.\n\nH1 uses frozen v1 generator profiles, including phase_offset_deg=-90 and\nsparsity background scale .18. H1-distractor frequency is true fA-24,\nincluding its original baseline carrier even at scale zero. H2 uses the\nprevious slow-distractor generator formula (physical trough centers,\nphase_offset_deg=180), no high-frequency distractor or its baseline, and\nan independently phased slow sine at fD and the requested amplitude ratio.\nSampling is 500 Hz; burst sigma .028 s, timing jitter .010 s, coupling .60,\nmixed frequency-domain 1/f pink + .5 white noise at -3 dB, as prescribed.\n\nH4 inherits the sinusoidal continuous-PAC clean condition from\nrun_apc_continuous_pac_boundary_benchmark.m: 12 s; unit-SD low sinusoid;\nhigh signal 1.25*(1+.70*cos(phase-pi/2))*sin(2*pi*fA*t+.2). Its fP/fA are\nrandom as above. The suite-wide -3 dB mixed-noise formula is used. This\nboundary has no Gaussian burst-strength parameter. No H4 null is requested.\n\nEvery H1 level and H2 ratios [0,1,3] get a paired timing null. Poisson\nrate is keep_rate*fP for sparsity and fP otherwise. Use the inherited\nevent support [t(1)-1/fP,t(end)+1/fP], Gaussian envelope sum and maximum\nnormalization. Overlaps are allowed. Replace only the true-burst component,\nretaining exact carrier/background/distractor/noise samples and scale.\nVerify coupled-minus-null equals removed-minus-added true component to\n1e-12. No-coupled-burst controls at H1 keep rates [1,.15] and distractor\nscale 3 remove only the true-burst component (coupling_level=0 in metadata).\nThe suite has 350 coupled inputs, 250 timing nulls and 75 secondary controls.\n\nAPC v2 and v1 use amplitude search [80,160] and their unchanged phase\nlimits. v1 is the selectable frozen v1 path. Comparator scans use the\ninherited butter(4) bandpass/filtfilt, phase half-width 1.5, grids\n3:.5:14 and 80:4:160, A2-prime half-width 14 and A1-prime half-width fP.\nEach raw/Ozkurt/KLMI/GLM metric independently maximizes its complete grid;\nKLMI uses 18 bins; Ozkurt=raw_MVL/sqrt(mean(A.^2)); GLM is the inherited\nR-squared. Ties retain MATLAB's first column-major maximum.\n\nOptional tPAC: inspect process_tpac on the configured local MATLAB path and\nthe configured Brainstorm installation. Include only if its existing\nheadless interface can execute unchanged with defaults and the same ranges;\notherwise record the exact availability reason and skip.\n\nRecovery uses inclusive phase 1 Hz and amplitude 8 Hz; strict phase .5 Hz.\nInvalid outputs are recovery failures; errors use finite estimates, with\nvalid/finite counts. AUC uses all finite coupled/null score pairs with\nhalf credit for ties, without changing score direction; report denominators.\nEvent p<.05 rates use all 25 trials, with the finite-p count also shown.\n\n\"Best A2-prime\" is selected per level, independently for each criterion's\nendpoint, in the comparator's favor. Maximize joint for C1/C4; maximize\nstrict joint for C2; minimize false joint for C3 null specificity. Ties use\nthe fixed metric order [MVL-raw,MVL-Ozkurt,KLMI,GLM]. No method parameter\nis selected or tuned. Record the chosen metric and count for every level.\nC2 uses paired successes and a one-sided exact binomial McNemar test on\ndiscordant pairs. C3 compares false-joint rates over all 250 timing-null\ninputs (5 per 100 means a .05 rate allowance); its event-z AUC thresholds\napply to the five prescribed H1 levels. A nonfinite required AUC fails.\nNo other threshold, pooling rule or C1-C4 wording is changed.\n\nAll inputs are saved once before parallel analysis. Three one-thread MATLAB\nworkers analyze disjoint input_id residue classes; scheduling does not\naffect the streams, saved input order or independent per-input surrogate RNG.\nCheckpoint every 25 analyzed inputs. Stop on method-relevant execution or\nverification failure. Document and resume purely tooling errors.\n",
  "paths": {
    "repository": "C:\\Users\\nghare\\.brainstorm\\process\\apc-brainstorm-publish",
    "output": "C:\\Users\\nghare\\.brainstorm\\process\\revision_checks\\v2\\candidate_03"
  },
  "tpac": {
    "path": "",
    "available": false,
    "configured_install": "C:\\Users\\nghare\\Documents\\Brainstorm3\\brainstorm_221219\\brainstorm3",
    "configured_install_exists": false,
    "included": false,
    "reason": "process_tpac absent from configured MATLAB path; configured Brainstorm install is unavailable"
  }
}
```
