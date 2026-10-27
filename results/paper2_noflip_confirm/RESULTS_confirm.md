# Confirmatory polarity-alignment analysis

Archive commit and successful push: `48b8f573c5a59539334f74c65eb4a2cb9b557c55`. Protocol `92992c108333314a0abf36b555a68b90d58026da`, SHA-256 `e3a482fabe40bfd0c6a243d867df5dc919669a3b1400a637954ca0ce334f50b5`. No signal was generated before that push.

## Generator check

PASS: first repeat in each of six V3 cells at seed 20261112 and first V1 trial at seed 20261110 were bit-identical in signal and time. The unchanged full streams were advanced as needed; no method ran on check signals or unused HB scenarios. W3 then used seed 20261120 (600 trials); W1 used 20261121 (175 coupled and 175 paired timing nulls).

## Primary C1/C2

**polarity alignment suppresses recovery of a coupled non-dominant rhythm (confirmed)**

Coupled-rhythm Step-2 fP recovery within 1 Hz, four non-dominant W3 cells pooled (n=400). Exact two-sided McNemar; Holm over C1/C2 only. Wilson 95% CIs.

| endpoint | cohort | metric | first | second | n | first_success | first_ci_low | first_ci_high | second_success | second_ci_low | second_ci_high | only_first | only_second | p_exact | p_holm | significant |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | W3_non_dominant_pooled | fp | APC-v3.0-noflip | APC-v3.0-flip | 400 | 134 | 0.290509 | 0.38263 | 3 | 0.00255389 | 0.0218157 | 131 | 0 | 7.34684e-40 | 1.46937e-39 | True |
| C2 | W3_non_dominant_pooled | fp | APC-v1.0-noflip | APC-v1.0-flip | 400 | 75 | 0.152289 | 0.228656 | 0 | 0 | 0.00951229 | 75 | 0 | 5.29396e-23 | 5.29396e-23 | True |

## Key secondary 1-3: comparisons

Secondary McNemar tests are exact, two-sided and unadjusted. Joint requires fP within 1 Hz and fA within 8 Hz; strict uses fP within 0.5 Hz. Invalid end-to-end outputs count as failures. Joint recovery in null cohorts is false joint recovery.

| endpoint | cohort | metric | first | second | n | first_success | first_ci_low | first_ci_high | second_success | second_ci_low | second_ci_high | only_first | only_second | p_exact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | W3_non_dominant_pooled | joint | APC-v3.0-noflip | A2_prime_2D | 400 | 101 | 0.212417 | 0.297292 | 201 | 0.453711 | 0.551241 | 71 | 171 | 1.07331e-10 |
| S1 | W3_non_dominant_pooled | joint | F2nf_A_SCAN | A2_prime_2D | 400 | 99 | 0.207743 | 0.292061 | 201 | 0.453711 | 0.551241 | 68 | 170 | 2.93698e-11 |
| S2 | W3_N_uncoupled | joint | APC-v1.0-noflip | APC-v1.0-flip | 100 | 11 | 0.062542 | 0.186313 | 19 | 0.125148 | 0.277788 | 1 | 9 | 0.0214844 |
| S2 | W3_N_uncoupled | joint | APC-v3.0-noflip | APC-v3.0-flip | 100 | 14 | 0.0852634 | 0.221372 | 19 | 0.125148 | 0.277788 | 2 | 7 | 0.179688 |
| S3 | W1_coupled | joint | APC-v1.0-noflip | APC-v1.0-flip | 175 | 85 | 0.412771 | 0.559272 | 111 | 0.560755 | 0.702048 | 5 | 31 | 1.29135e-05 |
| S3 | W1_coupled | strict | APC-v1.0-noflip | APC-v1.0-flip | 175 | 84 | 0.407207 | 0.553652 | 111 | 0.560755 | 0.702048 | 5 | 32 | 7.42753e-06 |
| S3 | W1_timing_null | joint | APC-v1.0-noflip | APC-v1.0-flip | 175 | 13 | 0.043924 | 0.122936 | 40 | 0.172584 | 0.296219 | 2 | 29 | 4.62867e-07 |
| S3 | W1_coupled | joint | APC-v3.0-noflip | APC-v3.0-flip | 175 | 102 | 0.508789 | 0.653366 | 114 | 0.578262 | 0.71809 | 4 | 16 | 0.0118179 |
| S3 | W1_coupled | strict | APC-v3.0-noflip | APC-v3.0-flip | 175 | 99 | 0.491645 | 0.636961 | 114 | 0.578262 | 0.71809 | 4 | 19 | 0.00259948 |
| S3 | W1_timing_null | joint | APC-v3.0-noflip | APC-v3.0-flip | 175 | 24 | 0.0939218 | 0.195952 | 41 | 0.177656 | 0.302331 | 1 | 18 | 7.62939e-05 |
| S3 | W1_coupled | joint | F2nf_A_SCAN | F3_A_SCAN | 175 | 142 | 0.747021 | 0.862457 | 161 | 0.870207 | 0.95175 | 0 | 19 | 3.8147e-06 |
| S3 | W1_coupled | strict | F2nf_A_SCAN | F3_A_SCAN | 175 | 137 | 0.71605 | 0.837513 | 161 | 0.870207 | 0.95175 | 0 | 24 | 1.19209e-07 |
| S3 | W1_timing_null | joint | F2nf_A_SCAN | F3_A_SCAN | 175 | 22 | 0.0845048 | 0.183003 | 42 | 0.182743 | 0.308426 | 1 | 21 | 1.09673e-05 |

## Key secondary 4: W3 per-cell counts

fP and dominant picks use the source estimate independently of later APC failure. For N_uncoupled, fP recovery uses the nominal 8-Hz reference and joint counts are false recovery. Dominant picks are not applicable to single-rhythm/control cells. Brackets are Wilson 95% proportion intervals.

| suite | cohort | method | n | fp [Wilson95CI] | dominant [Wilson95CI] | joint [Wilson95CI] | strict [Wilson95CI] |
| --- | --- | --- | --- | --- | --- | --- | --- |
| W3 | A_keep100 | A2_prime_2D | 100 | 99 [0.9455, 0.9982] | 0 [0, 0.03699] | 99 [0.9455, 0.9982] | 52 [0.4232, 0.6154] |
| W3 | A_keep100 | APC-v1.0-flip | 100 | 0 [0, 0.03699] | 98 [0.93, 0.9945] | 0 [0, 0.03699] | 0 [0, 0.03699] |
| W3 | A_keep100 | APC-v1.0-noflip | 100 | 12 [0.06999, 0.1981] | 41 [0.3187, 0.508] | 12 [0.06999, 0.1981] | 9 [0.04807, 0.1623] |
| W3 | A_keep100 | APC-v3.0-flip | 100 | 0 [0, 0.03699] | 100 [0.963, 1] | 0 [0, 0.03699] | 0 [0, 0.03699] |
| W3 | A_keep100 | APC-v3.0-noflip | 100 | 8 [0.04109, 0.15] | 72 [0.6251, 0.7986] | 8 [0.04109, 0.15] | 5 [0.02154, 0.1118] |
| W3 | A_keep100 | F2nf_A_SCAN | 100 | 8 [0.04109, 0.15] | 72 [0.6251, 0.7986] | 8 [0.04109, 0.15] | 5 [0.02154, 0.1118] |
| W3 | A_keep100 | F3_A_SCAN | 100 | 0 [0, 0.03699] | 100 [0.963, 1] | 0 [0, 0.03699] | 0 [0, 0.03699] |
| W3 | A_keep040 | A2_prime_2D | 100 | 77 [0.6785, 0.8416] | 0 [0, 0.03699] | 76 [0.6677, 0.8331] | 37 [0.2818, 0.4678] |
| W3 | A_keep040 | APC-v1.0-flip | 100 | 0 [0, 0.03699] | 99 [0.9455, 0.9982] | 0 [0, 0.03699] | 0 [0, 0.03699] |
| W3 | A_keep040 | APC-v1.0-noflip | 100 | 4 [0.01566, 0.09837] | 54 [0.4426, 0.6344] | 4 [0.01566, 0.09837] | 4 [0.01566, 0.09837] |
| W3 | A_keep040 | APC-v3.0-flip | 100 | 0 [0, 0.03699] | 100 [0.963, 1] | 0 [0, 0.03699] | 0 [0, 0.03699] |
| W3 | A_keep040 | APC-v3.0-noflip | 100 | 3 [0.01025, 0.08452] | 81 [0.7222, 0.8749] | 3 [0.01025, 0.08452] | 3 [0.01025, 0.08452] |
| W3 | A_keep040 | F2nf_A_SCAN | 100 | 3 [0.01025, 0.08452] | 81 [0.7222, 0.8749] | 3 [0.01025, 0.08452] | 3 [0.01025, 0.08452] |
| W3 | A_keep040 | F3_A_SCAN | 100 | 0 [0, 0.03699] | 100 [0.963, 1] | 0 [0, 0.03699] | 0 [0, 0.03699] |
| W3 | B_keep100 | A2_prime_2D | 100 | 22 [0.15, 0.3107] | 2 [0.005502, 0.07001] | 21 [0.1417, 0.2998] | 13 [0.07757, 0.2098] |
| W3 | B_keep100 | APC-v1.0-flip | 100 | 0 [0, 0.03699] | 97 [0.9155, 0.9897] | 0 [0, 0.03699] | 0 [0, 0.03699] |
| W3 | B_keep100 | APC-v1.0-noflip | 100 | 37 [0.2818, 0.4678] | 10 [0.05523, 0.1744] | 33 [0.2456, 0.4269] | 32 [0.2367, 0.4166] |
| W3 | B_keep100 | APC-v3.0-flip | 100 | 3 [0.01025, 0.08452] | 97 [0.9155, 0.9897] | 3 [0.01025, 0.08452] | 1 [0.001767, 0.05449] |
| W3 | B_keep100 | APC-v3.0-noflip | 100 | 73 [0.6357, 0.8073] | 9 [0.04807, 0.1623] | 63 [0.5322, 0.7182] | 61 [0.512, 0.6998] |
| W3 | B_keep100 | F2nf_A_SCAN | 100 | 73 [0.6357, 0.8073] | 9 [0.04807, 0.1623] | 57 [0.4722, 0.6627] | 55 [0.4524, 0.6439] |
| W3 | B_keep100 | F3_A_SCAN | 100 | 1 [0.001767, 0.05449] | 99 [0.9455, 0.9982] | 1 [0.001767, 0.05449] | 1 [0.001767, 0.05449] |
| W3 | B_keep040 | A2_prime_2D | 100 | 8 [0.04109, 0.15] | 7 [0.03432, 0.1375] | 5 [0.02154, 0.1118] | 4 [0.01566, 0.09837] |
| W3 | B_keep040 | APC-v1.0-flip | 100 | 0 [0, 0.03699] | 99 [0.9455, 0.9982] | 0 [0, 0.03699] | 0 [0, 0.03699] |
| W3 | B_keep040 | APC-v1.0-noflip | 100 | 22 [0.15, 0.3107] | 29 [0.2101, 0.3854] | 13 [0.07757, 0.2098] | 13 [0.07757, 0.2098] |
| W3 | B_keep040 | APC-v3.0-flip | 100 | 0 [0, 0.03699] | 99 [0.9455, 0.9982] | 0 [0, 0.03699] | 0 [0, 0.03699] |
| W3 | B_keep040 | APC-v3.0-noflip | 100 | 50 [0.4038, 0.5962] | 23 [0.1584, 0.3215] | 27 [0.1927, 0.3643] | 24 [0.1669, 0.3323] |
| W3 | B_keep040 | F2nf_A_SCAN | 100 | 50 [0.4038, 0.5962] | 23 [0.1584, 0.3215] | 31 [0.2278, 0.4063] | 27 [0.1927, 0.3643] |
| W3 | B_keep040 | F3_A_SCAN | 100 | 0 [0, 0.03699] | 100 [0.963, 1] | 0 [0, 0.03699] | 0 [0, 0.03699] |
| W3 | R_single_keep100 | A2_prime_2D | 100 | 99 [0.9455, 0.9982] | not applicable | 99 [0.9455, 0.9982] | 74 [0.6463, 0.816] |
| W3 | R_single_keep100 | APC-v1.0-flip | 100 | 100 [0.963, 1] | not applicable | 76 [0.6677, 0.8331] | 76 [0.6677, 0.8331] |
| W3 | R_single_keep100 | APC-v1.0-noflip | 100 | 97 [0.9155, 0.9897] | not applicable | 72 [0.6251, 0.7986] | 72 [0.6251, 0.7986] |
| W3 | R_single_keep100 | APC-v3.0-flip | 100 | 100 [0.963, 1] | not applicable | 76 [0.6677, 0.8331] | 76 [0.6677, 0.8331] |
| W3 | R_single_keep100 | APC-v3.0-noflip | 100 | 100 [0.963, 1] | not applicable | 74 [0.6463, 0.816] | 74 [0.6463, 0.816] |
| W3 | R_single_keep100 | F2nf_A_SCAN | 100 | 100 [0.963, 1] | not applicable | 100 [0.963, 1] | 100 [0.963, 1] |
| W3 | R_single_keep100 | F3_A_SCAN | 100 | 100 [0.963, 1] | not applicable | 100 [0.963, 1] | 100 [0.963, 1] |
| W3 | N_uncoupled | A2_prime_2D | 100 | 2 [0.005502, 0.07001] | not applicable | 0 [0, 0.03699] | 0 [0, 0.03699] |
| W3 | N_uncoupled | APC-v1.0-flip | 100 | 100 [0.963, 1] | not applicable | 19 [0.1251, 0.2778] | 19 [0.1251, 0.2778] |
| W3 | N_uncoupled | APC-v1.0-noflip | 100 | 48 [0.3846, 0.5768] | not applicable | 11 [0.06254, 0.1863] | 10 [0.05523, 0.1744] |
| W3 | N_uncoupled | APC-v3.0-flip | 100 | 100 [0.963, 1] | not applicable | 19 [0.1251, 0.2778] | 19 [0.1251, 0.2778] |
| W3 | N_uncoupled | APC-v3.0-noflip | 100 | 66 [0.5628, 0.7454] | not applicable | 14 [0.08526, 0.2214] | 13 [0.07757, 0.2098] |
| W3 | N_uncoupled | F2nf_A_SCAN | 100 | 66 [0.5628, 0.7454] | not applicable | 16 [0.101, 0.2442] | 16 [0.101, 0.2442] |
| W3 | N_uncoupled | F3_A_SCAN | 100 | 100 [0.963, 1] | not applicable | 22 [0.15, 0.3107] | 22 [0.15, 0.3107] |
| W3 | non_dominant_pooled | A2_prime_2D | 400 | 206 [0.4661, 0.5636] | 9 [0.01188, 0.0422] | 201 [0.4537, 0.5512] | 106 [0.2241, 0.3103] |
| W3 | non_dominant_pooled | APC-v1.0-flip | 400 | 0 [0, 0.009512] | 393 [0.9643, 0.9915] | 0 [0, 0.009512] | 0 [0, 0.009512] |
| W3 | non_dominant_pooled | APC-v1.0-noflip | 400 | 75 [0.1523, 0.2287] | 134 [0.2905, 0.3826] | 62 [0.1228, 0.1937] | 58 [0.1139, 0.1829] |
| W3 | non_dominant_pooled | APC-v3.0-flip | 400 | 3 [0.002554, 0.02182] | 396 [0.9746, 0.9961] | 3 [0.002554, 0.02182] | 1 [0.0004414, 0.01402] |
| W3 | non_dominant_pooled | APC-v3.0-noflip | 400 | 134 [0.2905, 0.3826] | 185 [0.4142, 0.5115] | 101 [0.2124, 0.2973] | 93 [0.1938, 0.2763] |
| W3 | non_dominant_pooled | F2nf_A_SCAN | 400 | 134 [0.2905, 0.3826] | 185 [0.4142, 0.5115] | 99 [0.2077, 0.2921] | 90 [0.1868, 0.2684] |
| W3 | non_dominant_pooled | F3_A_SCAN | 400 | 1 [0.0004414, 0.01402] | 399 [0.986, 0.9996] | 1 [0.0004414, 0.01402] | 1 [0.0004414, 0.01402] |

## W1 coupled and paired timing-null counts

| suite | cohort | method | n | fp [Wilson95CI] | dominant [Wilson95CI] | joint [Wilson95CI] | strict [Wilson95CI] |
| --- | --- | --- | --- | --- | --- | --- | --- |
| W1 | coupled | A2_prime_2D | 175 | 83 [0.4017, 0.548] | not applicable | 83 [0.4017, 0.548] | 46 [0.2032, 0.3327] |
| W1 | coupled | APC-v1.0-flip | 175 | 167 [0.9124, 0.9767] | not applicable | 111 [0.5608, 0.702] | 111 [0.5608, 0.702] |
| W1 | coupled | APC-v1.0-noflip | 175 | 125 [0.6433, 0.7761] | not applicable | 85 [0.4128, 0.5593] | 84 [0.4072, 0.5537] |
| W1 | coupled | APC-v3.0-flip | 175 | 175 [0.9785, 1] | not applicable | 114 [0.5783, 0.7181] | 114 [0.5783, 0.7181] |
| W1 | coupled | APC-v3.0-noflip | 175 | 155 [0.8301, 0.9248] | not applicable | 102 [0.5088, 0.6534] | 99 [0.4916, 0.637] |
| W1 | coupled | F2nf_A_SCAN | 175 | 155 [0.8301, 0.9248] | not applicable | 142 [0.747, 0.8625] | 137 [0.7161, 0.8375] |
| W1 | coupled | F3_A_SCAN | 175 | 175 [0.9785, 1] | not applicable | 161 [0.8702, 0.9517] | 161 [0.8702, 0.9517] |
| W1 | timing_null | A2_prime_2D | 175 | 2 [0.00314, 0.04071] | not applicable | 0 [0, 0.02148] | 0 [0, 0.02148] |
| W1 | timing_null | APC-v1.0-flip | 175 | 171 [0.9427, 0.9911] | not applicable | 40 [0.1726, 0.2962] | 40 [0.1726, 0.2962] |
| W1 | timing_null | APC-v1.0-noflip | 175 | 64 [0.298, 0.4392] | not applicable | 13 [0.04392, 0.1229] | 12 [0.03966, 0.116] |
| W1 | timing_null | APC-v3.0-flip | 175 | 175 [0.9785, 1] | not applicable | 41 [0.1777, 0.3023] | 41 [0.1777, 0.3023] |
| W1 | timing_null | APC-v3.0-noflip | 175 | 107 [0.5376, 0.6805] | not applicable | 24 [0.09392, 0.196] | 23 [0.0892, 0.1895] |
| W1 | timing_null | F2nf_A_SCAN | 175 | 107 [0.5376, 0.6805] | not applicable | 22 [0.0845, 0.183] | 20 [0.07521, 0.1699] |
| W1 | timing_null | F3_A_SCAN | 175 | 175 [0.9785, 1] | not applicable | 42 [0.1827, 0.3084] | 42 [0.1827, 0.3084] |

## Key secondary 5: returned v3 BTA power

Continuous BTA Welch power is reported as mean and median, not with Wilson intervals (which apply to counts). Nearest returned frequency bins are recorded; no spectrum was reconstructed and src was not instrumented.

| cell | method | n | finite_pairs | mean_coupled_power | median_coupled_power | mean_dominant_power | median_dominant_power | coupled_sampled_hz | dominant_sampled_hz |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A_keep100 | APC-v3.0-flip | 100 | 100 | 0.00139209 | 0.00131722 | 0.0106812 | 0.0104977 | 5.00488 | 10.9863 |
| A_keep100 | APC-v3.0-noflip | 100 | 100 | 0.000346152 | 0.000284449 | 0.000571521 | 0.000470091 | 5.00488 | 10.9863 |
| A_keep040 | APC-v3.0-flip | 100 | 100 | 0.00144816 | 0.00127774 | 0.0113452 | 0.0107104 | 5.00488 | 10.9863 |
| A_keep040 | APC-v3.0-noflip | 100 | 100 | 0.000159726 | 0.000133402 | 0.000472019 | 0.000350494 | 5.00488 | 10.9863 |
| B_keep100 | APC-v3.0-flip | 100 | 100 | 0.00105225 | 0.000955531 | 0.0110215 | 0.0111519 | 10.9863 | 5.00488 |
| B_keep100 | APC-v3.0-noflip | 100 | 100 | 0.000447157 | 0.000406304 | 0.000308906 | 0.000241585 | 10.9863 | 5.00488 |
| B_keep040 | APC-v3.0-flip | 100 | 100 | 0.00108602 | 0.000995088 | 0.0122632 | 0.0118945 | 10.9863 | 5.00488 |
| B_keep040 | APC-v3.0-noflip | 100 | 100 | 0.0002961 | 0.000220152 | 0.000331225 | 0.000249968 | 10.9863 | 5.00488 |

## Implementation and provenance

All validation settings and frozen source are unchanged except the prespecified flip option. F3/SCAN and A2-prime use the unchanged validation adapters. F2nf/SCAN calls the unchanged scan_fa_given_fp.m: its W3 score vector is restricted to the exact validation candidates 88:4:148 before the same first-maximum tie rule; unused extra candidate scores do not enter selection. W1 uses the helper full grid unchanged. Per-trial options/settings and signal hashes are recorded.

## Outputs and deviations

- [trial_estimates.csv](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip_confirm/trial_estimates.csv)

- [statistics.csv](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip_confirm/statistics.csv)

- [primary_C1_C2.csv](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip_confirm/primary_C1_C2.csv)

- [secondary_tests.csv](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip_confirm/secondary_tests.csv)

- [W3_counts.csv](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip_confirm/W3_counts.csv)

- [W1_counts.csv](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip_confirm/W1_counts.csv)

- [recovery_by_level.csv](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip_confirm/recovery_by_level.csv)

- [BTA_power.csv](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip_confirm/BTA_power.csv)

- [generator_check.json](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip_confirm/generator_check.json)

- [provenance.json](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip_confirm/provenance.json)

- [confirmation.png](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip_confirm/confirmation.png)

- [confirmation.svg](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip_confirm/confirmation.svg)


Deviations: [{"code": "ENVIRONMENT_VER_SYMBOL_SHADOW", "utc": "2026-10-24T19:25:24.899319+00:00", "reason": "Worker 1 failed in provenance logging before any trial: local variable ver, used later for version selection, shadowed the toolbox ver function. Other three workers were unaffected.", "fix": "Use feval('ver') for toolbox metadata. Restart worker 1 only, with the same partition and options. Preserve all other completed checkpoints.", "identified_without_looking_at_method_outcomes": true, "failed_worker_completed_inputs": 0, "before_sha256": "709827f3a9aeb53eceea580a76ab95bbdcfaaa86e4e001306f5d95254aac99a8", "after_sha256": "dc5b11d766b8d404f6232e49620a3a00edfe305c85f7bcd71788b30ade6a049e", "preserved_directory": "tooling_environment_ver_attempt1"}]


Worker elapsed seconds: 1: 338.744, 2: 293.208, 3: 290.994, 4: 292.347. New confirmation results are uncommitted.

## Verification and tooling note

[Final verification](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip_confirm/final_verification.json) checks the generator gates, frozen source/input hashes, options differing only in flipTroughs, comparator candidate grids, F2nf source pairing, counts and figure provenance. [Visual QA](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip_confirm/visual_qa.json) passed.

One tooling fix: ENVIRONMENT_VER_SYMBOL_SHADOW. Worker 1 stopped before estimating any input because a local ver variable shadowed MATLAB toolbox-version lookup. The metadata call was changed to feval('ver'); worker 1 alone resumed with its original partition. Other completed trials were retained. No method setting or outcome definition changed, and no method outcome was inspected to identify the defect.
