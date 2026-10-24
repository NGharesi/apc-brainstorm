# Exploratory: polarity-flip sensitivity

This post hoc exploratory analysis cannot change the validation decisions. Archive commit and successful push: `146e03c995c7a0091ca265b6dba2528f7806cadb`. Protocol commit `f8e60565c1fb7ddbd313705e247d2df46707a6f1`, SHA-256 `ffb5198537611b9a81e389ae7b53c316ed2506f0c2d9dad082cd782531a58132`.

Saved inputs only: V3 600, V1 350, V2 900, V4 25. All 1875 input hashes were retained; no signals or flip=true estimates were regenerated. For each frozen APC version the full normalized options were checked against the validation options with only flipTroughs changed to false. Four workers; no src changes. Step-2 fP is retained independently of later APC failure, using the unchanged ablation helper only when necessary. Invalid end-to-end outputs count as recovery failures.

## Exploratory V3 outcomes

Counts use Step-2 fP for reference-frequency recovery and dominant picks, and valid end-to-end estimates for joint recovery. Frequency tolerances: fP 1 Hz, fA 8 Hz. In N_uncoupled, reference fP is 8 Hz and joint recovery is false joint recovery. Dominant picks are not applicable to the single-rhythm or uncoupled cells. Exact two-sided McNemar p-values are exploratory, unadjusted; no confirmatory decision is made.

| suite | cohort | method | n | fp_recovery_flip | fp_recovery_noflip | fp_recovery_p_exploratory | dominant_picks_flip | dominant_picks_noflip | dominant_picks_p_exploratory | joint_flip | joint_noflip | joint_p_exploratory | strict_joint_flip | strict_joint_noflip |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V3 | A_keep100 | APC-v1.0 | 100 | 0 | 23 | 2.38419e-07 | 98 | 33 | 9.21572e-19 | 0 | 21 | 9.53674e-07 | 0 | 12 |
| V3 | A_keep100 | APC-v3.0 | 100 | 0 | 13 | 0.000244141 | 100 | 63 | 1.45519e-11 | 0 | 11 | 0.000976562 | 0 | 8 |
| V3 | A_keep040 | APC-v1.0 | 100 | 0 | 3 | 0.25 | 98 | 47 | 8.55427e-14 | 0 | 3 | 0.25 | 0 | 1 |
| V3 | A_keep040 | APC-v3.0 | 100 | 0 | 3 | 0.25 | 100 | 82 | 7.62939e-06 | 0 | 3 | 0.25 | 0 | 1 |
| V3 | B_keep100 | APC-v1.0 | 100 | 0 | 33 | 2.32831e-10 | 99 | 15 | 1.03398e-25 | 0 | 27 | 1.49012e-08 | 0 | 26 |
| V3 | B_keep100 | APC-v3.0 | 100 | 2 | 68 | 2.71051e-20 | 97 | 11 | 2.58494e-26 | 2 | 59 | 1.38778e-17 | 2 | 54 |
| V3 | B_keep040 | APC-v1.0 | 100 | 0 | 20 | 1.90735e-06 | 100 | 26 | 1.05879e-22 | 0 | 7 | 0.015625 | 0 | 6 |
| V3 | B_keep040 | APC-v3.0 | 100 | 1 | 51 | 2.35367e-14 | 99 | 22 | 1.32349e-23 | 1 | 29 | 5.7742e-08 | 1 | 24 |
| V3 | R_single_keep100 | APC-v1.0 | 100 | 100 | 100 | 1 | not available | not available | not available | 81 | 85 | 0.21875 | 81 | 85 |
| V3 | R_single_keep100 | APC-v3.0 | 100 | 100 | 100 | 1 | not available | not available | not available | 81 | 85 | 0.21875 | 81 | 85 |
| V3 | N_uncoupled | APC-v1.0 | 100 | 100 | 48 | 4.44089e-16 | not available | not available | not available | 24 | 11 | 0.000244141 | 24 | 10 |
| V3 | N_uncoupled | APC-v3.0 | 100 | 100 | 67 | 2.32831e-10 | not available | not available | not available | 24 | 13 | 0.000976562 | 24 | 12 |
| V3 | non_dominant_pooled | APC-v1.0 | 400 | 0 | 79 | 3.30872e-24 | 395 | 121 | 3.76688e-78 | 0 | 58 | 6.93889e-18 | 0 | 45 |
| V3 | non_dominant_pooled | APC-v3.0 | 400 | 3 | 135 | 1.23978e-38 | 396 | 178 | 4.74778e-66 | 3 | 102 | 8.04638e-29 | 3 | 87 |


## Exploratory V1/V2/V4 outcomes

Strict joint recovery uses fP tolerance 0.5 Hz with fA tolerance 8 Hz. Timing-null joint counts are false joint recovery. No additional hypothesis tests were added for these descriptive outcomes.

| suite | cohort | method | n | fp_recovery_flip | fp_recovery_noflip | fp_recovery_p_exploratory | dominant_picks_flip | dominant_picks_noflip | dominant_picks_p_exploratory | joint_flip | joint_noflip | joint_p_exploratory | strict_joint_flip | strict_joint_noflip |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V1 | coupled | APC-v1.0 | 175 | 170 | 120 | not available | not available | not available | not available | 116 | 87 | not available | 116 | 84 |
| V1 | coupled | APC-v3.0 | 175 | 175 | 155 | not available | not available | not available | not available | 120 | 106 | not available | 120 | 103 |
| V1 | timing_null | APC-v1.0 | 175 | 170 | 54 | not available | not available | not available | not available | 44 | 17 | not available | 44 | 16 |
| V1 | timing_null | APC-v3.0 | 175 | 175 | 100 | not available | not available | not available | not available | 46 | 27 | not available | 46 | 25 |
| V2 | coupled | APC-v1.0 | 450 | 98 | 235 | not available | not available | not available | not available | 43 | 85 | not available | 43 | 85 |
| V2 | coupled | APC-v3.0 | 450 | 366 | 423 | not available | not available | not available | not available | 114 | 131 | not available | 109 | 128 |
| V2 | timing_null | APC-v1.0 | 450 | 65 | 60 | not available | not available | not available | not available | 9 | 9 | not available | 9 | 9 |
| V2 | timing_null | APC-v3.0 | 450 | 348 | 336 | not available | not available | not available | not available | 37 | 41 | not available | 35 | 39 |
| V4 | coupled | APC-v1.0 | 25 | 24 | 25 | not available | not available | not available | not available | 23 | 24 | not available | 23 | 24 |
| V4 | coupled | APC-v3.0 | 25 | 25 | 25 | not available | not available | not available | not available | 24 | 24 | not available | 24 | 24 |


## Exploratory diagnostics

n_bursts is the number of retained burst-centered epochs returned by bst_apc, not a separately reconstructed pre-edge detection count. The fraction of epochs flipped is **not available** for either version. APC v1.0 does not return its BTA or spectrum, so BTA powers are **not available**. APC v3.0 returns the BTA Welch spectrum; powers below use the nearest returned bin to each truth frequency. Both sampled bin frequencies are recorded per trial; no new spectrum or hidden diagnostic was reconstructed.

| suite | cohort | method | flip_troughs | n | mean_n_bursts | median_n_bursts | min_n_bursts | max_n_bursts | fraction_epochs_flipped | mean_bta_power_coupled | median_bta_power_coupled | mean_bta_power_dominant | median_bta_power_dominant | finite_bta_pairs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V3 | A_keep100 | APC-v1.0 | 1 | 100 | 105.42 | 105 | 91 | 121 | not available | not available | not available | not available | not available | 0 |
| V3 | A_keep100 | APC-v1.0 | 0 | 100 | 105.42 | 105 | 91 | 121 | not available | not available | not available | not available | not available | 0 |
| V3 | A_keep100 | APC-v3.0 | 1 | 100 | 105.42 | 105 | 91 | 121 | not available | 0.00142418 | 0.00115313 | 0.0114805 | 0.0110745 | 100 |
| V3 | A_keep100 | APC-v3.0 | 0 | 100 | 105.42 | 105 | 91 | 121 | not available | 0.000368526 | 0.000339261 | 0.000470598 | 0.000389775 | 100 |
| V3 | A_keep040 | APC-v1.0 | 1 | 100 | 112.02 | 112 | 99 | 125 | not available | not available | not available | not available | not available | 0 |
| V3 | A_keep040 | APC-v1.0 | 0 | 100 | 112.02 | 112 | 99 | 125 | not available | not available | not available | not available | not available | 0 |
| V3 | A_keep040 | APC-v3.0 | 1 | 100 | 112.02 | 112 | 99 | 125 | not available | 0.00147719 | 0.00137717 | 0.0113509 | 0.0113332 | 100 |
| V3 | A_keep040 | APC-v3.0 | 0 | 100 | 112.02 | 112 | 99 | 125 | not available | 0.000176657 | 0.000173105 | 0.000573557 | 0.000357363 | 100 |
| V3 | B_keep100 | APC-v1.0 | 1 | 100 | 115.96 | 115 | 105 | 130 | not available | not available | not available | not available | not available | 0 |
| V3 | B_keep100 | APC-v1.0 | 0 | 100 | 115.96 | 115 | 105 | 130 | not available | not available | not available | not available | not available | 0 |
| V3 | B_keep100 | APC-v3.0 | 1 | 100 | 115.96 | 115 | 105 | 130 | not available | 0.000980338 | 0.000892562 | 0.0110912 | 0.0102075 | 100 |
| V3 | B_keep100 | APC-v3.0 | 0 | 100 | 115.96 | 115 | 105 | 130 | not available | 0.000415631 | 0.000333738 | 0.000300625 | 0.000251194 | 100 |
| V3 | B_keep040 | APC-v1.0 | 1 | 100 | 107.6 | 107 | 96 | 128 | not available | not available | not available | not available | not available | 0 |
| V3 | B_keep040 | APC-v1.0 | 0 | 100 | 107.6 | 107 | 96 | 128 | not available | not available | not available | not available | not available | 0 |
| V3 | B_keep040 | APC-v3.0 | 1 | 100 | 107.6 | 107 | 96 | 128 | not available | 0.00111074 | 0.000975202 | 0.0128285 | 0.0124612 | 100 |
| V3 | B_keep040 | APC-v3.0 | 0 | 100 | 107.6 | 107 | 96 | 128 | not available | 0.00029193 | 0.000266134 | 0.000381829 | 0.000321273 | 100 |
| V3 | R_single_keep100 | APC-v1.0 | 1 | 100 | 105.38 | 105.5 | 91 | 117 | not available | not available | not available | not available | not available | 0 |
| V3 | R_single_keep100 | APC-v1.0 | 0 | 100 | 105.38 | 105.5 | 91 | 117 | not available | not available | not available | not available | not available | 0 |
| V3 | R_single_keep100 | APC-v3.0 | 1 | 100 | 105.38 | 105.5 | 91 | 117 | not available | not available | not available | not available | not available | 0 |
| V3 | R_single_keep100 | APC-v3.0 | 0 | 100 | 105.38 | 105.5 | 91 | 117 | not available | not available | not available | not available | not available | 0 |
| V3 | N_uncoupled | APC-v1.0 | 1 | 100 | 116.17 | 116 | 104 | 130 | not available | not available | not available | not available | not available | 0 |
| V3 | N_uncoupled | APC-v1.0 | 0 | 100 | 116.17 | 116 | 104 | 130 | not available | not available | not available | not available | not available | 0 |
| V3 | N_uncoupled | APC-v3.0 | 1 | 100 | 116.17 | 116 | 104 | 130 | not available | not available | not available | not available | not available | 0 |
| V3 | N_uncoupled | APC-v3.0 | 0 | 100 | 116.17 | 116 | 104 | 130 | not available | not available | not available | not available | not available | 0 |
| V3 | non_dominant_pooled | APC-v1.0 | 1 | 400 | 110.25 | 110 | 91 | 130 | not available | not available | not available | not available | not available | 0 |
| V3 | non_dominant_pooled | APC-v1.0 | 0 | 400 | 110.25 | 110 | 91 | 130 | not available | not available | not available | not available | not available | 0 |
| V3 | non_dominant_pooled | APC-v3.0 | 1 | 400 | 110.25 | 110 | 91 | 130 | not available | 0.00124811 | 0.00110508 | 0.0116878 | 0.0111945 | 400 |
| V3 | non_dominant_pooled | APC-v3.0 | 0 | 400 | 110.25 | 110 | 91 | 130 | not available | 0.000313186 | 0.000254531 | 0.000431652 | 0.00032027 | 400 |
| V1 | coupled | APC-v1.0 | 1 | 175 | 94.8743 | 100 | 55 | 122 | not available | not available | not available | not available | not available | 0 |
| V1 | coupled | APC-v1.0 | 0 | 175 | 94.8743 | 100 | 55 | 122 | not available | not available | not available | not available | not available | 0 |
| V1 | coupled | APC-v3.0 | 1 | 175 | 94.8743 | 100 | 55 | 122 | not available | not available | not available | not available | not available | 0 |
| V1 | coupled | APC-v3.0 | 0 | 175 | 94.8743 | 100 | 55 | 122 | not available | not available | not available | not available | not available | 0 |
| V1 | timing_null | APC-v1.0 | 1 | 175 | 99.8114 | 109 | 53 | 127 | not available | not available | not available | not available | not available | 0 |
| V1 | timing_null | APC-v1.0 | 0 | 175 | 99.8114 | 109 | 53 | 127 | not available | not available | not available | not available | not available | 0 |
| V1 | timing_null | APC-v3.0 | 1 | 175 | 99.8114 | 109 | 53 | 127 | not available | not available | not available | not available | not available | 0 |
| V1 | timing_null | APC-v3.0 | 0 | 175 | 99.8114 | 109 | 53 | 127 | not available | not available | not available | not available | not available | 0 |
| V2 | coupled | APC-v1.0 | 1 | 450 | 26.7889 | 14 | 1 | 70 | not available | not available | not available | not available | not available | 0 |
| V2 | coupled | APC-v1.0 | 0 | 450 | 26.7889 | 14 | 1 | 70 | not available | not available | not available | not available | not available | 0 |
| V2 | coupled | APC-v3.0 | 1 | 450 | 26.7889 | 14 | 1 | 70 | not available | not available | not available | not available | not available | 0 |
| V2 | coupled | APC-v3.0 | 0 | 450 | 26.7889 | 14 | 1 | 70 | not available | not available | not available | not available | not available | 0 |
| V2 | timing_null | APC-v1.0 | 1 | 450 | 20.5711 | 13.5 | 1 | 73 | not available | not available | not available | not available | not available | 0 |
| V2 | timing_null | APC-v1.0 | 0 | 450 | 20.5711 | 13.5 | 1 | 73 | not available | not available | not available | not available | not available | 0 |
| V2 | timing_null | APC-v3.0 | 1 | 450 | 20.5711 | 13.5 | 1 | 73 | not available | not available | not available | not available | not available | 0 |
| V2 | timing_null | APC-v3.0 | 0 | 450 | 20.5711 | 13.5 | 1 | 73 | not available | not available | not available | not available | not available | 0 |
| V4 | coupled | APC-v1.0 | 1 | 25 | 136.48 | 136 | 123 | 155 | not available | not available | not available | not available | not available | 0 |
| V4 | coupled | APC-v1.0 | 0 | 25 | 136.48 | 136 | 123 | 155 | not available | not available | not available | not available | not available | 0 |
| V4 | coupled | APC-v3.0 | 1 | 25 | 136.48 | 136 | 123 | 155 | not available | not available | not available | not available | not available | 0 |
| V4 | coupled | APC-v3.0 | 0 | 25 | 136.48 | 136 | 123 | 155 | not available | not available | not available | not available | not available | 0 |


## Exploratory outputs and deviations

- [trial_estimates.csv](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip/trial_estimates.csv)

- [summary.csv](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip/summary.csv)

- [mcnemar_exploratory.csv](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip/mcnemar_exploratory.csv)

- [diagnostics.csv](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip/diagnostics.csv)

- [recovery_by_level.csv](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip/recovery_by_level.csv)

- [provenance.json](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip/provenance.json)

- [exploratory_noflip.png](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip/exploratory_noflip.png)

- [exploratory_noflip.svg](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip/exploratory_noflip.svg)


Deviations: none.


Worker runtimes (seconds): 1: 297.522, 2: 279.610, 3: 298.361, 4: 283.081.

## Exploratory verification

[Final verification](C:/Users/nghare/.brainstorm/process/revision_checks/paper2_noflip/final_verification.json) checks source and input hashes, exact reuse of saved flip=true estimates, options, row counts, figure provenance and the clean repository. No Part-2 code or result is committed.
