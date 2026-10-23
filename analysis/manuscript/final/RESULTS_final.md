# Final APC v1.0 results

## Filter correction

The user authorized replacement of the direct-form coefficient realization with **the same nominal `butter(4)` Butterworth design in second-order sections**. All tagged APC v1.0/v2.0 code and their saved estimates are unchanged. Only comparator filtering was corrected: `[z,p,k]=butter(4,wn,"bandpass"); [sos,g]=zp2sos(z,p,k); filtfilt(sos,g,x)`. Band edges, cutoff clamps, grids, metrics, ties, generator inputs and seeds remain as originally specified.

Every unique design is checked before use: maximum pole radius <1 for both the ZPK design and the realized SOS sections, and |gain at the arithmetic passband centre−1|<1e-3. A failed guard raises an error and stops execution. All guards passed at 500 Hz and at every actual rodent sampling-rate value. Full guard registry: [all_corrected_filter_guards.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/all_corrected_filter_guards.csv>).

The audit evaluated **506 unique bands on ten saved signals (5060 comparisons)**: five held-out coupled inputs (H1 keep1, H1 keep.15, H1 distractor3, H2 ratio3, H4; first repeat each), and five development inputs (main sparsity1/.15, main distractor3, random-fP sparsity.5/distractor1.5; first repeat each). Every band was tested on every selected signal. The complete original input paths/IDs, per-input relative L2 differences and RMS values are in [filter_audit_500Hz_trials.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/filter_audit_500Hz_trials.csv>).

Not every relative difference was <1e-6; the maximum was 0.80433205808. Both held-out and development phase/amplitude band sets included failures of that tolerance. Therefore all 5,400 held-out comparator rows and all 21,200 previously run affected development comparator rows were replaced in new corrected CSVs. The 1,350 held-out APC rows were reused byte-for-byte by field, and all 24 rodent APC bout estimates were reused unchanged. No signal was regenerated.

Original results remain in their original directories; the earlier final attempt is preserved under [previous_direct_form_attempt](<C:/Users/nghare/.brainstorm/process/revision_checks/final/previous_direct_form_attempt/RESULTS_final.md>). Earlier direct-form rodent rows and inference are **superseded**, as are the direct-form comparator rows in the development/held-out files for this final analysis. Their historical files are retained. Corrected held-out trials: [heldout_trials.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/corrected_heldout/heldout_trials.csv>). Corrected development trials: [all_trials.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/corrected_development/all_trials.csv>).

### Old versus SOS: v2.0 prespecified C1–C4

| criterion | old_result | new_result | old_numbers | new_numbers |
| --- | --- | --- | --- | --- |
| C1 | FAIL | FAIL | v2 joint 5/100; best A2 joint 62/100; required >= 57; near-fD 14/100, required <=10 | v2 joint 5/100; best A2 joint 53/100; required >= 48; near-fD 14/100, required <=10 |
| C2 | PASS | PASS | v2 strict 71/175; best A2 strict 51/175; discordant v2-only/A2-only=46/26; exact one-sided McNemar p=0.0122304536642 | v2 strict 71/175; best A2 strict 50/175; discordant v2-only/A2-only=49/28; exact one-sided McNemar p=0.0110167293824 |
| C3 | FAIL | FAIL | false joint v2 2/250 (0.8/100), best A2 0/250 (0/100), allowance +5/100; event-z AUCs: H1_sparsity=1: 0.8848; H1_sparsity=0.55000000000000004: 0.5536; H1_distractor=0: 0.7872; H1_distractor=1.5: 0.6576; H1_distractor=3: 0.7184 | false joint v2 2/250 (0.8/100), best A2 1/250 (0.4/100), allowance +5/100; event-z AUCs: H1_sparsity=1: 0.8848; H1_sparsity=0.55000000000000004: 0.5536; H1_distractor=0: 0.7872; H1_distractor=1.5: 0.6576; H1_distractor=3: 0.7184 |
| C4 | FAIL | FAIL | v2 joint 71/175; best A2 joint 111/175; required >= 102 | v2 joint 71/175; best A2 joint 104/175; required >= 95 |

The original criterion formulas, per-level best-metric tie order and paired exact one-sided McNemar calculation were reused unchanged. The table recalculates criteria against the corrected A2′ comparators; v2 frequency picks, scores, event tests and required event-z AUCs were not rerun. Best-A2′ selections and counts: [best_A2_by_level.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/corrected_heldout/best_A2_by_level.csv>). Full details: [decision_details.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/corrected_heldout/decision_details.json>). Old/new criterion CSV: [v2_criteria_old_vs_SOS.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/v2_criteria_old_vs_SOS.csv>).

### APC v1.0 versus A2′: descriptive old/new counts

The following counts pool each scenario/dataset across its requested levels; A2′ is chosen per level to maximize coupled recovery or minimize null false recovery, separately for joint/strict endpoints. Primary v1.0 counts are unchanged. This is descriptive and is not a new v1.0 pass/fail test.

| scenario | dataset | endpoint | v1_count | old_best_A2 | SOS_best_A2 |
| --- | --- | --- | --- | --- | --- |
| H1_distractor | coupled | joint | 61 | 58 | 57 |
| H1_distractor | coupled | strict_joint | 61 | 25 | 29 |
| H1_distractor | no_coupled_burst | joint | 8 | 0 | 0 |
| H1_distractor | no_coupled_burst | strict_joint | 8 | 0 | 0 |
| H1_distractor | timing_null | joint | 15 | 0 | 0 |
| H1_distractor | timing_null | strict_joint | 15 | 0 | 0 |
| H1_sparsity | coupled | joint | 59 | 53 | 47 |
| H1_sparsity | coupled | strict_joint | 59 | 26 | 21 |
| H1_sparsity | no_coupled_burst | joint | 3 | 0 | 0 |
| H1_sparsity | no_coupled_burst | strict_joint | 3 | 0 | 0 |
| H1_sparsity | timing_null | joint | 18 | 0 | 0 |
| H1_sparsity | timing_null | strict_joint | 18 | 0 | 0 |
| H2 | coupled | joint | 63 | 110 | 97 |
| H2 | coupled | strict_joint | 61 | 53 | 43 |
| H2 | timing_null | joint | 3 | 0 | 1 |
| H2 | timing_null | strict_joint | 3 | 0 | 0 |
| H4 | coupled | joint | 22 | 25 | 24 |
| H4 | coupled | strict_joint | 22 | 17 | 9 |

Per-level choices and counts: [v1_vs_A2_old_vs_SOS.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/v1_vs_A2_old_vs_SOS.csv>). All held-out comparator old/new recovery/error/near-fD groups: [heldout_comparator_old_vs_SOS_summary.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/heldout_comparator_old_vs_SOS_summary.csv>). Per-trial picks/scores: [heldout_comparator_old_vs_new_trials.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/heldout_comparator_old_vs_new_trials.csv>).

### Development old/new summary

Each row sums successes over its 25-trial method-by-level groups; n_groups identifies the denominator (25*n_groups). Null-stage rows count false recovery; other stages count recovery. The two phase-grid spacings are separate analyses.

| stage | configuration | fp_grid_step_hz | n_groups | old_joint | SOS_joint | old_strict | SOS_strict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| main | A0 | 1 | 56 | 102 | 111 | 46 | 64 |
| main | A1 | 1 | 56 | 1188 | 1161 | 164 | 177 |
| main | A2 | 0.5 | 56 | 1203 | 1194 | 773 | 726 |
| main | A2 | 1 | 56 | 1273 | 1265 | 591 | 549 |
| null | A1 | 1 | 112 | 51 | 23 | 11 | 8 |
| null | A2 | 0.5 | 112 | 29 | 25 | 8 | 12 |
| null | A2 | 1 | 112 | 76 | 68 | 12 | 22 |
| random_fp | A0 | 0.5 | 24 | 110 | 95 | 42 | 31 |
| random_fp | A0 | 1 | 24 | 134 | 121 | 58 | 49 |
| random_fp | A1 | 0.5 | 24 | 121 | 97 | 27 | 15 |
| random_fp | A1 | 1 | 24 | 222 | 194 | 50 | 35 |
| random_fp | A2 | 0.5 | 24 | 364 | 349 | 178 | 157 |
| random_fp | A2 | 1 | 24 | 411 | 378 | 203 | 173 |
| slow | A1 | 0.5 | 36 | 490 | 472 | 22 | 35 |
| slow | A1 | 1 | 36 | 535 | 519 | 16 | 8 |
| slow | A2 | 0.5 | 36 | 523 | 517 | 328 | 223 |
| slow | A2 | 1 | 36 | 538 | 549 | 221 | 122 |

All per-method/level error and recovery comparisons: [development_comparator_old_vs_SOS_summary.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/development_comparator_old_vs_SOS_summary.csv>). Per-trial comparisons: [development_comparator_old_vs_SOS_trials.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/development_comparator_old_vs_SOS_trials.csv>). Updated development null AUCs: [null_specificity_auc.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/corrected_development/null_specificity_auc.csv>).

### Rodent: superseded direct-form versus SOS

All 96 comparator rows were rerun on the identical saved 24 bouts. The raw/Ozkurt/KLMI/GLM grids and selected-pair metrics are unchanged. Old/new per-bout values: [rodent_old_vs_SOS.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/rodent_old_vs_SOS.csv>). Equal-bout and duration-weighted Welch/Hedges/bootstrap results were recomputed, with identical 10,000 shared resample indices at seed 20261022. Full old/new statistics: [rodent_statistics_old_vs_SOS.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/rodent_statistics_old_vs_SOS.csv>).

| method | metric | mean_difference_old | mean_difference_SOS | welch_t_old | welch_t_SOS | p_two_sided_old | p_two_sided_SOS | hedges_g_old | hedges_g_SOS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APC v1.0 | fP_hz | 0.67210592 | 0.67210592 | 3.7902339 | 3.7902339 | 0.0026982225 | 0.0026982225 | 1.4938964 | 1.4938964 |
| APC v1.0 | fA_hz | 9.0833333 | 9.0833333 | 1.6227302 | 1.6227302 | 0.12009078 | 0.12009078 | 0.63958871 | 0.63958871 |
| APC v1.0 | ozkurt_mvl | 0.013498232 | 0.013498232 | 2.1144003 | 2.1144003 | 0.046070938 | 0.046070938 | 0.83337729 | 0.83337729 |
| MVL-raw | fP_hz | 0.041666667 | 1.5416667 | 0.5956834 | 2.5593435 | 0.55797369 | 0.021026067 | 0.23478479 | 1.0087488 |
| MVL-raw | fA_hz | -0.33333333 | 11.333333 | -1 | 3.0180925 | 0.3388007 | 0.0090098662 | -0.39414358 | 1.1895618 |
| MVL-raw | ozkurt_mvl | -0.031247841 | 0.018958831 | -0.99355656 | 5.178044 | 0.33242079 | 3.4272674e-05 | -0.39160394 | 2.0408928 |
| MVL-Ozkurt | fP_hz | 0.041666667 | 1.2916667 | 0.5956834 | 2.2995965 | 0.55797369 | 0.03237733 | 0.23478479 | 0.9063712 |
| MVL-Ozkurt | fA_hz | -8.3333333 | 5.3333333 | -1.0244306 | 0.80219078 | 0.31688672 | 0.43353674 | -0.40377275 | 0.31617835 |
| MVL-Ozkurt | ozkurt_mvl | -0.046260165 | 0.013134962 | -1.5639357 | 2.7458225 | 0.1340577 | 0.01344232 | -0.61641521 | 1.0822483 |
| KLMI | fP_hz | 1.375 | 0.95833333 | 2.0821875 | 2.7985287 | 0.04918886 | 0.010650845 | 0.82068085 | 1.1030221 |
| KLMI | fA_hz | -12.333333 | 1 | -2.1073379 | 0.15829386 | 0.046733213 | 0.87602138 | -0.83059369 | 0.062390511 |
| KLMI | ozkurt_mvl | -0.12268189 | 0.016935404 | -2.5724582 | 3.0355363 | 0.024849771 | 0.0075814686 | -1.0139179 | 1.1964371 |
| GLM | fP_hz | 1.7083333 | 1 | 3.2646036 | 2.8428212 | 0.0040005806 | 0.0098182547 | 1.2867226 | 1.1204797 |
| GLM | fA_hz | -7.6666667 | 4 | -1.5574319 | 0.6326153 | 0.13452544 | 0.53405281 | -0.61385177 | 0.24934126 |
| GLM | ozkurt_mvl | -0.095465082 | 0.014473516 | -2.0148573 | 2.7610639 | 0.06883745 | 0.013063216 | -0.79414308 | 1.0882556 |

Old/new exact boundary counts:

| method | state | boundary_4_old | boundary_4_SOS | boundary_12_old | boundary_12_SOS |
| --- | --- | --- | --- | --- | --- |
| APC v1.0 | run | 0 | 0 | 0 | 0 |
| APC v1.0 | rest | 0 | 0 | 0 | 0 |
| MVL-raw | run | 10 | 0 | 0 | 0 |
| MVL-raw | rest | 11 | 3 | 0 | 0 |
| MVL-Ozkurt | run | 10 | 0 | 0 | 0 |
| MVL-Ozkurt | rest | 11 | 1 | 0 | 0 |
| KLMI | run | 2 | 0 | 0 | 0 |
| KLMI | rest | 6 | 0 | 0 | 0 |
| GLM | run | 0 | 0 | 0 | 0 |
| GLM | rest | 4 | 0 | 0 | 0 |

### Per-band 500-Hz audit

Bounds are realized passband edges in Hz. Each row has ten input comparisons. Centre gain is the single-pass magnitude; filtfilt applies that realization in both directions. The relative L2 range is calculated on the complete filtered records, including their endpoints. SOS pole radii are from the ZPK design; the detailed CSV and guard registry also contain the realized SOS-section pole radius.

| low_hz | high_hz | band_uses | direct_max_pole_radius | sos_max_pole_radius | direct_center_gain | sos_center_gain | min_relative_L2_difference | max_relative_L2_difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.5 | 4.5 | heldout_phase | 0.99532847 | 0.99623901 | 1.0030269 | 0.9999924 | 0.23573402 | 0.80433206 |
| 2 | 5 | heldout_phase | 0.99558965 | 0.9957244 | 1.0011652 | 0.99999779 | 0.11177362 | 0.65659419 |
| 2.5 | 5.5 | heldout_phase;development_phase | 0.99533794 | 0.99534532 | 1.0006593 | 0.99999924 | 0.15085896 | 0.60248934 |
| 3 | 6 | heldout_phase;development_phase | 0.99501177 | 0.99505429 | 0.99976281 | 0.9999997 | 0.13768603 | 0.48968019 |
| 3.5 | 6.5 | heldout_phase;development_phase | 0.99479828 | 0.99482367 | 1.0005476 | 0.99999987 | 0.12723343 | 0.52645932 |
| 4 | 7 | heldout_phase;development_phase | 0.99462178 | 0.99463631 | 1.0001105 | 0.99999994 | 0.10020459 | 0.47957448 |
| 4.5 | 7.5 | heldout_phase;development_phase | 0.9944772 | 0.99448101 | 0.9996742 | 0.99999997 | 0.10166542 | 0.34671943 |
| 5 | 8 | heldout_phase;development_phase | 0.99434201 | 0.99435014 | 0.99999456 | 0.99999998 | 0.090159238 | 0.30936646 |
| 5.5 | 8.5 | heldout_phase;development_phase | 0.99423726 | 0.99423832 | 1.0000516 | 0.99999999 | 0.084276412 | 0.32596972 |
| 6 | 9 | heldout_phase;development_phase | 0.99413614 | 0.99414166 | 0.9999497 | 1 | 0.12469975 | 0.33736087 |
| 6.5 | 9.5 | heldout_phase;development_phase | 0.99405733 | 0.99405724 | 0.99997845 | 1 | 0.12321391 | 0.35250889 |
| 7 | 10 | heldout_phase;development_phase | 0.99398273 | 0.99398286 | 1.0000777 | 1 | 0.10020925 | 0.33740998 |
| 7.5 | 10.5 | heldout_phase;development_phase | 0.99391668 | 0.99391683 | 1.0000036 | 1 | 0.068612606 | 0.32353794 |
| 8 | 11 | heldout_phase;development_phase | 0.993859 | 0.9938578 | 1.0000012 | 1 | 0.066316387 | 0.48394594 |
| 8.5 | 11.5 | heldout_phase;development_phase | 0.99380445 | 0.99380471 | 1.0000163 | 1 | 0.088303673 | 0.48614378 |
| 9 | 12 | heldout_phase;development_phase | 0.99375611 | 0.9937567 | 1.0000064 | 1 | 0.091030978 | 0.44298669 |
| 9.5 | 12.5 | heldout_phase;development_phase | 0.99371384 | 0.99371307 | 0.99999549 | 1 | 0.1046872 | 0.37668959 |
| 10 | 13 | heldout_phase;development_phase | 0.9936737 | 0.99367324 | 0.99999611 | 1 | 0.076940789 | 0.36375664 |
| 10.5 | 13.5 | heldout_phase;development_phase | 0.99363653 | 0.99363673 | 1.0000135 | 1 | 0.10217456 | 0.3695861 |
| 11 | 14 | heldout_phase | 0.99360313 | 0.99360314 | 0.99999798 | 1 | 0.091190037 | 0.29857274 |
| 11.5 | 14.5 | heldout_phase | 0.99357224 | 0.99357213 | 0.99999036 | 1 | 0.1120316 | 0.28690776 |
| 12 | 15 | heldout_phase | 0.99354365 | 0.99354342 | 0.99998833 | 1 | 0.095263059 | 0.32043795 |
| 12.5 | 15.5 | heldout_phase | 0.99351648 | 0.99351674 | 0.99999861 | 1 | 0.10400914 | 0.35578116 |
| 66 | 94 | heldout_A2_prime;heldout_A1_prime | 0.94237291 | 0.94237291 | 1 | 1 | 0.013264173 | 0.041813533 |
| 66.5 | 93.5 | heldout_A1_prime | 0.9440798 | 0.9440798 | 1 | 1 | 0.01150806 | 0.043855161 |
| 67 | 93 | heldout_A1_prime | 0.94581402 | 0.94581402 | 1 | 1 | 0.010714434 | 0.045656658 |
| 67.5 | 92.5 | heldout_A1_prime | 0.94757541 | 0.94757541 | 1 | 1 | 0.011681611 | 0.047143485 |
| 68 | 92 | heldout_A1_prime;development_fixed;development_A1 | 0.94936381 | 0.94936381 | 1 | 1 | 0.012936893 | 0.048355105 |
| 68.5 | 91.5 | heldout_A1_prime;development_A1 | 0.95117906 | 0.95117906 | 1 | 1 | 0.01139699 | 0.049540627 |
| 69 | 91 | heldout_A1_prime;development_A1 | 0.953021 | 0.953021 | 1 | 1 | 0.013256336 | 0.051238637 |
| 69.5 | 90.5 | heldout_A1_prime;development_A1 | 0.95488948 | 0.95488948 | 1 | 1 | 0.016983571 | 0.054258139 |
| 70 | 90 | heldout_A1_prime;development_A1 | 0.95678434 | 0.95678434 | 1 | 1 | 0.018300676 | 0.059457612 |
| 70 | 98 | heldout_A2_prime;heldout_A1_prime | 0.94166263 | 0.94166263 | 1 | 1 | 0.011431844 | 0.037302844 |
| 70.5 | 89.5 | heldout_A1_prime;development_A1 | 0.95870544 | 0.95870544 | 1 | 1 | 0.019070779 | 0.06735862 |
| 70.5 | 97.5 | heldout_A1_prime | 0.94341846 | 0.94341846 | 1 | 1 | 0.011079584 | 0.038693716 |
| 71 | 89 | heldout_A1_prime;development_A1 | 0.96065262 | 0.96065262 | 1 | 1 | 0.019670142 | 0.077860995 |
| 71 | 97 | heldout_A1_prime | 0.94519991 | 0.94519991 | 1 | 1 | 0.010739785 | 0.039621714 |
| 71.5 | 88.5 | heldout_A1_prime;development_A1 | 0.96262573 | 0.96262573 | 1 | 1 | 0.01736272 | 0.090263394 |
| 71.5 | 96.5 | heldout_A1_prime | 0.94700682 | 0.94700682 | 1 | 1 | 0.010642376 | 0.040336803 |
| 72 | 88 | heldout_A1_prime;development_A1 | 0.96462463 | 0.96462463 | 1 | 1 | 0.014920908 | 0.10349017 |
| 72 | 96 | heldout_A1_prime | 0.94883903 | 0.94883903 | 1 | 1 | 0.011017815 | 0.041346436 |
| 72.5 | 87.5 | heldout_A1_prime;development_A1 | 0.96664917 | 0.96664917 | 1 | 1 | 0.012489092 | 0.11633179 |
| 72.5 | 95.5 | heldout_A1_prime | 0.95069638 | 0.95069638 | 1 | 1 | 0.012032284 | 0.043980311 |
| 73 | 87 | heldout_A1_prime;development_A1 | 0.96869921 | 0.96869921 | 1 | 1 | 0.01100904 | 0.13022746 |
| 73 | 95 | heldout_A1_prime | 0.9525787 | 0.9525787 | 1 | 1 | 0.013771297 | 0.052471318 |
| 73.5 | 86.5 | heldout_A1_prime;development_A1 | 0.97077461 | 0.97077461 | 1 | 1 | 0.014626331 | 0.14674366 |
| 73.5 | 94.5 | heldout_A1_prime | 0.95448584 | 0.95448584 | 1 | 1 | 0.015668408 | 0.061610766 |
| 74 | 86 | heldout_A1_prime;development_fixed;development_A1 | 0.97287522 | 0.97287522 | 1 | 1 | 0.025949225 | 0.16138757 |
| 74 | 94 | heldout_A1_prime | 0.95641764 | 0.95641764 | 1 | 1 | 0.019285751 | 0.07116411 |
| 74 | 102 | heldout_A2_prime;heldout_A1_prime | 0.94099283 | 0.94099283 | 1 | 1 | 0.012708261 | 0.036702464 |
| 74.5 | 85.5 | heldout_A1_prime;development_A1 | 0.97500091 | 0.97500091 | 1 | 1 | 0.043458605 | 0.17517848 |
| 74.5 | 93.5 | heldout_A1_prime | 0.95837395 | 0.95837395 | 1 | 1 | 0.020966711 | 0.080901704 |
| 74.5 | 101.5 | heldout_A1_prime | 0.94279474 | 0.94279474 | 1 | 1 | 0.011584692 | 0.038924359 |
| 75 | 85 | heldout_A1_prime;development_A1 | 0.97715154 | 0.97715154 | 1 | 1 | 0.065391108 | 0.19037125 |
| 75 | 93 | heldout_A1_prime | 0.9603546 | 0.9603546 | 1 | 1 | 0.024052029 | 0.090572456 |
| 75 | 101 | heldout_A1_prime | 0.94462067 | 0.94462067 | 1 | 1 | 0.011055333 | 0.040392215 |
| 75.5 | 84.5 | heldout_A1_prime;development_A1 | 0.97932696 | 0.97932696 | 1 | 1 | 0.070700758 | 0.2108382 |
| 75.5 | 92.5 | heldout_A1_prime | 0.96235945 | 0.96235945 | 1 | 1 | 0.030279363 | 0.099880596 |
| 75.5 | 100.5 | heldout_A1_prime | 0.94647046 | 0.94647046 | 1 | 1 | 0.011544997 | 0.040999643 |
| 76 | 84 | heldout_A1_prime;development_A1 | 0.98152706 | 0.98152706 | 1 | 1 | 0.08192299 | 0.2394879 |
| 76 | 92 | heldout_A1_prime | 0.96438834 | 0.96438834 | 1 | 1 | 0.039324896 | 0.1084526 |
| 76 | 100 | heldout_A1_prime;development_fixed;development_A1 | 0.94834395 | 0.94834395 | 1 | 1 | 0.01084356 | 0.041949542 |
| 76.5 | 83.5 | heldout_A1_prime | 0.98375169 | 0.98375169 | 1 | 1 | 0.10109335 | 0.27204377 |
| 76.5 | 91.5 | heldout_A1_prime | 0.96644112 | 0.96644112 | 1 | 1 | 0.046688829 | 0.12709495 |
| 76.5 | 99.5 | heldout_A1_prime;development_A1 | 0.95024096 | 0.95024096 | 1 | 1 | 0.011869251 | 0.047951024 |
| 77 | 83 | heldout_A1_prime | 0.98600072 | 0.98600072 | 1 | 1 | 0.11794361 | 0.30286023 |
| 77 | 91 | heldout_A1_prime | 0.96851764 | 0.96851764 | 1 | 1 | 0.05319057 | 0.14904335 |
| 77 | 99 | heldout_A1_prime;development_A1 | 0.95216135 | 0.95216135 | 1 | 1 | 0.013911658 | 0.054772563 |
| 77.5 | 90.5 | heldout_A1_prime | 0.97061775 | 0.97061775 | 1 | 1 | 0.055345116 | 0.16959049 |
| 77.5 | 98.5 | heldout_A1_prime;development_A1 | 0.95410493 | 0.95410493 | 1 | 1 | 0.016745257 | 0.062082924 |
| 78 | 90 | heldout_A1_prime | 0.97274131 | 0.97274131 | 1 | 1 | 0.053097364 | 0.18690928 |
| 78 | 98 | heldout_A1_prime;development_A1 | 0.95607156 | 0.95607156 | 1 | 1 | 0.021339037 | 0.069480677 |
| 78 | 106 | heldout_A2_prime;heldout_A1_prime | 0.94035697 | 0.94035697 | 1 | 1 | 0.0090576366 | 0.046619851 |
| 78.5 | 89.5 | heldout_A1_prime | 0.97488817 | 0.97488817 | 1 | 1 | 0.042239083 | 0.1991078 |
| 78.5 | 97.5 | heldout_A1_prime;development_A1 | 0.95806107 | 0.95806107 | 1 | 1 | 0.027468487 | 0.076544234 |
| 78.5 | 105.5 | heldout_A1_prime | 0.94220255 | 0.94220255 | 1 | 1 | 0.0089439331 | 0.048125622 |
| 79 | 89 | heldout_A1_prime | 0.97705817 | 0.97705817 | 1 | 1 | 0.036328475 | 0.20495778 |
| 79 | 97 | heldout_A1_prime;development_A1 | 0.96007329 | 0.96007329 | 1 | 1 | 0.03201324 | 0.082877209 |
| 79 | 105 | heldout_A1_prime | 0.94407066 | 0.94407066 | 1 | 1 | 0.0095880788 | 0.0482799 |
| 79.5 | 88.5 | heldout_A1_prime | 0.97925119 | 0.97925119 | 1 | 1 | 0.048018683 | 0.20461177 |
| 79.5 | 96.5 | heldout_A1_prime;development_A1 | 0.96210807 | 0.96210807 | 1 | 1 | 0.035003638 | 0.088193416 |
| 79.5 | 104.5 | heldout_A1_prime | 0.94596112 | 0.94596112 | 1 | 1 | 0.011099788 | 0.046968294 |
| 80 | 88 | heldout_A1_prime | 0.98146706 | 0.98146706 | 1 | 1 | 0.048024534 | 0.19908494 |
| 80 | 96 | heldout_A1_prime;development_A1 | 0.96416526 | 0.96416526 | 1 | 1 | 0.036154206 | 0.096176148 |
| 80 | 104 | heldout_A1_prime | 0.94787376 | 0.94787376 | 1 | 1 | 0.013354886 | 0.044216585 |
| 80.5 | 87.5 | heldout_A1_prime | 0.98370565 | 0.98370565 | 1 | 1 | 0.053953149 | 0.22564628 |
| 80.5 | 95.5 | heldout_A1_prime;development_A1 | 0.96624468 | 0.96624468 | 1 | 1 | 0.038808627 | 0.11039614 |
| 80.5 | 103.5 | heldout_A1_prime | 0.94980841 | 0.94980841 | 1 | 1 | 0.016119886 | 0.040271748 |
| 81 | 87 | heldout_A1_prime | 0.98596682 | 0.98596682 | 1 | 1 | 0.051533114 | 0.24525018 |
| 81 | 95 | heldout_A1_prime;development_A1 | 0.9683462 | 0.9683462 | 1 | 1 | 0.044674846 | 0.13428903 |
| 81 | 103 | heldout_A1_prime | 0.95176491 | 0.95176491 | 1 | 1 | 0.018136486 | 0.035756131 |
| 81.5 | 94.5 | heldout_A1_prime;development_A1 | 0.97046964 | 0.97046964 | 1 | 1 | 0.056540649 | 0.15333079 |
| 81.5 | 102.5 | heldout_A1_prime | 0.95374309 | 0.95374309 | 1 | 1 | 0.022137656 | 0.043519609 |
| 82 | 94 | heldout_A1_prime;development_fixed;development_A1 | 0.97261486 | 0.97261486 | 1 | 1 | 0.068195664 | 0.16402828 |
| 82 | 102 | heldout_A1_prime | 0.95574277 | 0.95574277 | 1 | 1 | 0.025403986 | 0.053399622 |
| 82 | 110 | heldout_A2_prime;heldout_A1_prime | 0.93974948 | 0.93974948 | 1 | 1 | 0.01506864 | 0.035893948 |
| 82.5 | 93.5 | heldout_A1_prime;development_A1 | 0.9747817 | 0.9747817 | 1 | 1 | 0.07925481 | 0.17342378 |
| 82.5 | 101.5 | heldout_A1_prime | 0.9577638 | 0.9577638 | 1 | 1 | 0.028347537 | 0.065209695 |
| 82.5 | 109.5 | heldout_A1_prime | 0.94163674 | 0.94163674 | 1 | 1 | 0.015657445 | 0.037390042 |
| 83 | 93 | heldout_A1_prime;development_A1 | 0.97697 | 0.97697 | 1 | 1 | 0.085684911 | 0.1891594 |
| 83 | 101 | heldout_A1_prime | 0.959806 | 0.959806 | 1 | 1 | 0.031417407 | 0.079297816 |
| 83 | 109 | heldout_A1_prime | 0.94354509 | 0.94354509 | 1 | 1 | 0.016245617 | 0.038517435 |
| 83.5 | 92.5 | heldout_A1_prime;development_A1 | 0.97917962 | 0.97917962 | 1 | 1 | 0.085895195 | 0.20159177 |
| 83.5 | 100.5 | heldout_A1_prime | 0.96186921 | 0.96186921 | 1 | 1 | 0.03424476 | 0.095614539 |
| 83.5 | 108.5 | heldout_A1_prime | 0.94547437 | 0.94547437 | 1 | 1 | 0.017339561 | 0.039398125 |
| 84 | 92 | heldout_A1_prime;development_A1 | 0.98141039 | 0.98141039 | 1 | 1 | 0.08490599 | 0.21809297 |
| 84 | 100 | heldout_A1_prime | 0.96395327 | 0.96395327 | 1 | 1 | 0.030167622 | 0.11321358 |
| 84 | 108 | heldout_A1_prime;development_fixed;development_A1 | 0.94742439 | 0.94742439 | 1 | 1 | 0.019004365 | 0.040248306 |
| 84.5 | 91.5 | heldout_A1_prime | 0.98366218 | 0.98366218 | 1 | 1 | 0.089806085 | 0.26195845 |
| 84.5 | 99.5 | heldout_A1_prime | 0.966058 | 0.966058 | 1 | 1 | 0.028526847 | 0.12997849 |
| 84.5 | 107.5 | heldout_A1_prime;development_A1 | 0.94939499 | 0.94939499 | 1 | 1 | 0.02136264 | 0.041364344 |
| 85 | 91 | heldout_A1_prime | 0.98593481 | 0.98593481 | 1 | 1 | 0.096418894 | 0.31128153 |
| 85 | 99 | heldout_A1_prime | 0.96818326 | 0.96818326 | 1 | 1 | 0.032129466 | 0.14370867 |
| 85 | 107 | heldout_A1_prime;development_A1 | 0.95138597 | 0.95138597 | 1 | 1 | 0.024583633 | 0.043085307 |
| 85.5 | 98.5 | heldout_A1_prime | 0.97032887 | 0.97032887 | 1 | 1 | 0.037048906 | 0.1547195 |
| 85.5 | 106.5 | heldout_A1_prime;development_A1 | 0.95339719 | 0.95339719 | 1 | 1 | 0.027030202 | 0.046470316 |
| 86 | 98 | heldout_A1_prime | 0.97249467 | 0.97249467 | 1 | 1 | 0.03626997 | 0.16597685 |
| 86 | 106 | heldout_A1_prime;development_A1 | 0.95542845 | 0.95542845 | 1 | 1 | 0.027464984 | 0.055010619 |
| 86 | 114 | heldout_A2_prime;heldout_A1_prime | 0.93916557 | 0.93916557 | 1 | 1 | 0.013095084 | 0.034654935 |
| 86.5 | 97.5 | heldout_A1_prime | 0.9746805 | 0.9746805 | 1 | 1 | 0.037768529 | 0.17884576 |
| 86.5 | 105.5 | heldout_A1_prime;development_A1 | 0.95747959 | 0.95747959 | 1 | 1 | 0.028955044 | 0.066568697 |
| 86.5 | 113.5 | heldout_A1_prime | 0.94109284 | 0.94109284 | 1 | 1 | 0.012972579 | 0.036623449 |
| 87 | 97 | heldout_A1_prime | 0.97688619 | 0.97688619 | 1 | 1 | 0.044359505 | 0.20798001 |
| 87 | 105 | heldout_A1_prime;development_A1 | 0.95955043 | 0.95955043 | 1 | 1 | 0.030972408 | 0.079261043 |
| 87 | 113 | heldout_A1_prime | 0.94303985 | 0.94303985 | 1 | 1 | 0.012717288 | 0.040653708 |
| 87.5 | 96.5 | heldout_A1_prime | 0.97911159 | 0.97911159 | 1 | 1 | 0.059151966 | 0.23669144 |
| 87.5 | 104.5 | heldout_A1_prime;development_A1 | 0.96164081 | 0.96164081 | 1 | 1 | 0.030573186 | 0.092627222 |
| 87.5 | 112.5 | heldout_A1_prime | 0.94500641 | 0.94500641 | 1 | 1 | 0.012408364 | 0.049014452 |
| 88 | 96 | heldout_A1_prime | 0.98135652 | 0.98135652 | 1 | 1 | 0.083475098 | 0.26249469 |
| 88 | 104 | heldout_A1_prime;development_A1 | 0.96375055 | 0.96375055 | 1 | 1 | 0.029027763 | 0.1061707 |
| 88 | 112 | heldout_A1_prime | 0.94699233 | 0.94699233 | 1 | 1 | 0.012127625 | 0.057912628 |
| 88.5 | 95.5 | heldout_A1_prime | 0.98362084 | 0.98362084 | 1 | 1 | 0.11217481 | 0.28333838 |
| 88.5 | 103.5 | heldout_A1_prime;development_A1 | 0.96587948 | 0.96587948 | 1 | 1 | 0.026015764 | 0.11914154 |
| 88.5 | 111.5 | heldout_A1_prime | 0.94899745 | 0.94899745 | 1 | 1 | 0.01193446 | 0.067109723 |
| 89 | 95 | heldout_A1_prime | 0.98590437 | 0.98590437 | 1 | 1 | 0.085697962 | 0.29580691 |
| 89 | 103 | heldout_A1_prime;development_A1 | 0.96802743 | 0.96802743 | 1 | 1 | 0.021821568 | 0.13013774 |
| 89 | 111 | heldout_A1_prime | 0.95102158 | 0.95102158 | 1 | 1 | 0.01185392 | 0.076280913 |
| 89.5 | 102.5 | heldout_A1_prime;development_A1 | 0.97019423 | 0.97019423 | 1 | 1 | 0.019607673 | 0.14877396 |
| 89.5 | 110.5 | heldout_A1_prime | 0.95306454 | 0.95306454 | 1 | 1 | 0.011893637 | 0.085003589 |
| 90 | 102 | heldout_A1_prime;development_fixed;development_A1 | 0.97237971 | 0.97237971 | 1 | 1 | 0.026179731 | 0.17377174 |
| 90 | 110 | heldout_A1_prime | 0.95512615 | 0.95512615 | 1 | 1 | 0.012076092 | 0.092770628 |
| 90 | 118 | heldout_A2_prime;heldout_A1_prime | 0.93860104 | 0.93860104 | 1 | 1 | 0.0067677519 | 0.024585571 |
| 90.5 | 101.5 | heldout_A1_prime;development_A1 | 0.9745837 | 0.9745837 | 1 | 1 | 0.041531374 | 0.20026703 |
| 90.5 | 109.5 | heldout_A1_prime | 0.95720624 | 0.95720624 | 1 | 1 | 0.012447542 | 0.099027457 |
| 90.5 | 117.5 | heldout_A1_prime | 0.94056697 | 0.94056697 | 1 | 1 | 0.0056427934 | 0.026011288 |
| 91 | 101 | heldout_A1_prime;development_A1 | 0.97680602 | 0.97680602 | 1 | 1 | 0.061455577 | 0.22911762 |
| 91 | 109 | heldout_A1_prime | 0.95930462 | 0.95930462 | 1 | 1 | 0.013055206 | 0.10323265 |
| 91 | 117 | heldout_A1_prime | 0.94255131 | 0.94255131 | 1 | 1 | 0.0047479064 | 0.033547184 |
| 91.5 | 100.5 | heldout_A1_prime;development_A1 | 0.97904651 | 0.97904651 | 1 | 1 | 0.071159808 | 0.26258025 |
| 91.5 | 108.5 | heldout_A1_prime | 0.96142111 | 0.96142111 | 1 | 1 | 0.013959758 | 0.11231342 |
| 91.5 | 116.5 | heldout_A1_prime | 0.94455389 | 0.94455389 | 1 | 1 | 0.0044650459 | 0.044773415 |
| 92 | 100 | heldout_A1_prime;development_A1 | 0.98130499 | 0.98130499 | 1 | 1 | 0.074160282 | 0.30302132 |
| 92 | 108 | heldout_A1_prime | 0.96355555 | 0.96355555 | 1 | 1 | 0.015331258 | 0.12352411 |
| 92 | 116 | heldout_A1_prime;development_fixed;development_A1 | 0.94657451 | 0.94657451 | 1 | 1 | 0.0048756503 | 0.058644284 |
| 92.5 | 99.5 | heldout_A1_prime | 0.9835813 | 0.9835813 | 1 | 1 | 0.073851502 | 0.34777446 |
| 92.5 | 107.5 | heldout_A1_prime | 0.96570774 | 0.96570774 | 1 | 1 | 0.017492823 | 0.13389713 |
| 92.5 | 115.5 | heldout_A1_prime;development_A1 | 0.94861299 | 0.94861299 | 1 | 1 | 0.0056345543 | 0.074486521 |
| 93 | 99 | heldout_A1_prime | 0.98587526 | 0.98587526 | 1 | 1 | 0.069337249 | 0.38072258 |
| 93 | 107 | heldout_A1_prime | 0.96787752 | 0.96787752 | 1 | 1 | 0.020734745 | 0.14361217 |
| 93 | 115 | heldout_A1_prime;development_A1 | 0.95066914 | 0.95066914 | 1 | 1 | 0.0064043874 | 0.091866214 |
| 93.5 | 106.5 | heldout_A1_prime | 0.9700647 | 0.9700647 | 1 | 1 | 0.025051447 | 0.15361549 |
| 93.5 | 114.5 | heldout_A1_prime;development_A1 | 0.95274279 | 0.95274279 | 1 | 1 | 0.007111553 | 0.11047529 |
| 94 | 106 | heldout_A1_prime | 0.97226911 | 0.97226911 | 1 | 1 | 0.030010227 | 0.16979196 |
| 94 | 114 | heldout_A1_prime;development_A1 | 0.95483374 | 0.95483374 | 1 | 1 | 0.0079867133 | 0.13006853 |
| 94 | 122 | heldout_A2_prime;heldout_A1_prime | 0.9380522 | 0.9380522 | 1 | 1 | 0.0060249468 | 0.026483777 |
| 94.5 | 105.5 | heldout_A1_prime | 0.97449056 | 0.97449056 | 1 | 1 | 0.03475365 | 0.18082941 |
| 94.5 | 113.5 | heldout_A1_prime;development_A1 | 0.95694181 | 0.95694181 | 1 | 1 | 0.0094925636 | 0.15040119 |
| 94.5 | 121.5 | heldout_A1_prime | 0.94005566 | 0.94005566 | 1 | 1 | 0.0059773667 | 0.027152823 |
| 95 | 105 | heldout_A1_prime | 0.97672889 | 0.97672889 | 1 | 1 | 0.038698877 | 0.18679322 |
| 95 | 113 | heldout_A1_prime;development_A1 | 0.95906681 | 0.95906681 | 1 | 1 | 0.01204576 | 0.17113907 |
| 95 | 121 | heldout_A1_prime | 0.94207628 | 0.94207628 | 1 | 1 | 0.0075823347 | 0.03061329 |
| 95.5 | 104.5 | heldout_A1_prime | 0.97898389 | 0.97898389 | 1 | 1 | 0.041940815 | 0.1906315 |
| 95.5 | 112.5 | heldout_A1_prime;development_A1 | 0.96120857 | 0.96120857 | 1 | 1 | 0.015751746 | 0.19174846 |
| 95.5 | 120.5 | heldout_A1_prime | 0.94411385 | 0.94411385 | 1 | 1 | 0.010103217 | 0.034881566 |
| 96 | 104 | heldout_A1_prime | 0.98125541 | 0.98125541 | 1 | 1 | 0.042958278 | 0.21746626 |
| 96 | 112 | heldout_A1_prime;development_A1 | 0.96336689 | 0.96336689 | 1 | 1 | 0.020443992 | 0.21141687 |
| 96 | 120 | heldout_A1_prime | 0.94616818 | 0.94616818 | 1 | 1 | 0.012612538 | 0.040169593 |
| 96.5 | 103.5 | heldout_A1_prime | 0.98354325 | 0.98354325 | 1 | 1 | 0.044699623 | 0.27125953 |
| 96.5 | 111.5 | heldout_A1_prime;development_A1 | 0.96554158 | 0.96554158 | 1 | 1 | 0.025856582 | 0.22907794 |
| 96.5 | 119.5 | heldout_A1_prime | 0.94823908 | 0.94823908 | 1 | 1 | 0.014303115 | 0.046590505 |
| 97 | 103 | heldout_A1_prime | 0.98584724 | 0.98584724 | 1 | 1 | 0.052328473 | 0.32776466 |
| 97 | 111 | heldout_A1_prime;development_A1 | 0.96773247 | 0.96773247 | 1 | 1 | 0.031733805 | 0.24353328 |
| 97 | 119 | heldout_A1_prime | 0.95032637 | 0.95032637 | 1 | 1 | 0.014623519 | 0.054157874 |
| 97.5 | 110.5 | heldout_A1_prime;development_A1 | 0.96993937 | 0.96993937 | 1 | 1 | 0.037831141 | 0.25355015 |
| 97.5 | 118.5 | heldout_A1_prime | 0.95242984 | 0.95242984 | 1 | 1 | 0.014248915 | 0.062897183 |
| 98 | 110 | heldout_A1_prime;development_fixed;development_A1 | 0.97216209 | 0.97216209 | 1 | 1 | 0.043072158 | 0.25784288 |
| 98 | 118 | heldout_A1_prime | 0.95454931 | 0.95454931 | 1 | 1 | 0.017013535 | 0.075635297 |
| 98 | 126 | heldout_A2_prime;heldout_A1_prime | 0.93751567 | 0.93751567 | 1 | 1 | 0.0088077041 | 0.02730849 |
| 98.5 | 109.5 | heldout_A1_prime;development_A1 | 0.97440044 | 0.97440044 | 1 | 1 | 0.049735844 | 0.25487023 |
| 98.5 | 117.5 | heldout_A1_prime | 0.95668459 | 0.95668459 | 1 | 1 | 0.022693325 | 0.093498004 |
| 98.5 | 125.5 | heldout_A1_prime | 0.93955581 | 0.93955581 | 1 | 1 | 0.008472997 | 0.029667923 |
| 99 | 109 | heldout_A1_prime;development_A1 | 0.97665424 | 0.97665424 | 1 | 1 | 0.056329528 | 0.24271039 |
| 99 | 117 | heldout_A1_prime | 0.95883548 | 0.95883548 | 1 | 1 | 0.022863235 | 0.11257497 |
| 99 | 125 | heldout_A1_prime | 0.94161185 | 0.94161185 | 1 | 1 | 0.0079828414 | 0.032457093 |
| 99.5 | 108.5 | heldout_A1_prime;development_A1 | 0.9789233 | 0.9789233 | 1 | 1 | 0.066239132 | 0.24017287 |
| 99.5 | 116.5 | heldout_A1_prime | 0.9610018 | 0.9610018 | 1 | 1 | 0.022727499 | 0.13253736 |
| 99.5 | 124.5 | heldout_A1_prime | 0.94368361 | 0.94368361 | 1 | 1 | 0.0078188315 | 0.035843665 |
| 100 | 108 | heldout_A1_prime;development_A1 | 0.98120743 | 0.98120743 | 1 | 1 | 0.080940246 | 0.28667044 |
| 100 | 116 | heldout_A1_prime | 0.96318334 | 0.96318334 | 1 | 1 | 0.02209056 | 0.15303363 |
| 100 | 124 | heldout_A1_prime;development_fixed;development_A1 | 0.94577088 | 0.94577088 | 1 | 1 | 0.0088336125 | 0.040032193 |
| 100.5 | 107.5 | heldout_A1_prime | 0.98350643 | 0.98350643 | 1 | 1 | 0.094087367 | 0.33226777 |
| 100.5 | 115.5 | heldout_A1_prime | 0.96537992 | 0.96537992 | 1 | 1 | 0.021208682 | 0.17358657 |
| 100.5 | 123.5 | heldout_A1_prime;development_A1 | 0.94787347 | 0.94787347 | 1 | 1 | 0.011621997 | 0.045274962 |
| 101 | 107 | heldout_A1_prime | 0.98582013 | 0.98582013 | 1 | 1 | 0.096992926 | 0.37665678 |
| 101 | 115 | heldout_A1_prime | 0.96759135 | 0.96759135 | 1 | 1 | 0.021271978 | 0.19355545 |
| 101 | 123 | heldout_A1_prime;development_A1 | 0.94999117 | 0.94999117 | 1 | 1 | 0.016109177 | 0.053005522 |
| 101.5 | 114.5 | heldout_A1_prime | 0.96981743 | 0.96981743 | 1 | 1 | 0.023713606 | 0.21228433 |
| 101.5 | 122.5 | heldout_A1_prime;development_A1 | 0.9521238 | 0.9521238 | 1 | 1 | 0.018897324 | 0.063385581 |
| 102 | 114 | heldout_A1_prime | 0.97205796 | 0.97205796 | 1 | 1 | 0.028006686 | 0.22949997 |
| 102 | 122 | heldout_A1_prime;development_A1 | 0.95427115 | 0.95427115 | 1 | 1 | 0.019536324 | 0.075385613 |
| 102 | 130 | heldout_A2_prime;heldout_A1_prime | 0.93698839 | 0.93698839 | 1 | 1 | 0.0079837957 | 0.026010608 |
| 102.5 | 113.5 | heldout_A1_prime | 0.97431275 | 0.97431275 | 1 | 1 | 0.031399812 | 0.25452405 |
| 102.5 | 121.5 | heldout_A1_prime;development_A1 | 0.95643303 | 0.95643303 | 1 | 1 | 0.020827523 | 0.089246184 |
| 102.5 | 129.5 | heldout_A1_prime | 0.93906453 | 0.93906453 | 1 | 1 | 0.0073189852 | 0.027597215 |
| 103 | 113 | heldout_A1_prime | 0.97658161 | 0.97658161 | 1 | 1 | 0.030545472 | 0.28322806 |
| 103 | 121 | heldout_A1_prime;development_A1 | 0.95860923 | 0.95860923 | 1 | 1 | 0.023064854 | 0.10524012 |
| 103 | 129 | heldout_A1_prime | 0.94115537 | 0.94115537 | 1 | 1 | 0.0054374712 | 0.029856879 |
| 103.5 | 112.5 | heldout_A1_prime | 0.97886433 | 0.97886433 | 1 | 1 | 0.023768783 | 0.29685468 |
| 103.5 | 120.5 | heldout_A1_prime;development_A1 | 0.96079956 | 0.96079956 | 1 | 1 | 0.026255805 | 0.12338701 |
| 103.5 | 128.5 | heldout_A1_prime | 0.94326071 | 0.94326071 | 1 | 1 | 0.0058382939 | 0.03262074 |
| 104 | 112 | heldout_A1_prime | 0.98116073 | 0.98116073 | 1 | 1 | 0.023780748 | 0.29545637 |
| 104 | 120 | heldout_A1_prime;development_A1 | 0.96300381 | 0.96300381 | 1 | 1 | 0.030198852 | 0.1427445 |
| 104 | 128 | heldout_A1_prime | 0.94538034 | 0.94538034 | 1 | 1 | 0.0083238516 | 0.035569428 |
| 104.5 | 111.5 | heldout_A1_prime | 0.9834706 | 0.9834706 | 1 | 1 | 0.041074364 | 0.29192276 |
| 104.5 | 119.5 | heldout_A1_prime;development_A1 | 0.96522179 | 0.96522179 | 1 | 1 | 0.034753327 | 0.16114279 |
| 104.5 | 127.5 | heldout_A1_prime | 0.94751406 | 0.94751406 | 1 | 1 | 0.0080889449 | 0.038284775 |
| 105 | 111 | heldout_A1_prime | 0.98579374 | 0.98579374 | 1 | 1 | 0.029314068 | 0.28596147 |
| 105 | 119 | heldout_A1_prime;development_A1 | 0.9674533 | 0.9674533 | 1 | 1 | 0.039962401 | 0.18074951 |
| 105 | 127 | heldout_A1_prime | 0.94966165 | 0.94966165 | 1 | 1 | 0.0086472352 | 0.040304824 |
| 105.5 | 118.5 | heldout_A1_prime;development_A1 | 0.96969814 | 0.96969814 | 1 | 1 | 0.045833055 | 0.19667173 |
| 105.5 | 126.5 | heldout_A1_prime | 0.95182293 | 0.95182293 | 1 | 1 | 0.010741635 | 0.041982794 |
| 106 | 118 | heldout_A1_prime;development_fixed;development_A1 | 0.97195609 | 0.97195609 | 1 | 1 | 0.047492487 | 0.20834193 |
| 106 | 126 | heldout_A1_prime | 0.95399768 | 0.95399768 | 1 | 1 | 0.01445152 | 0.049155182 |
| 106 | 134 | heldout_A2_prime;heldout_A1_prime | 0.93646746 | 0.93646746 | 1 | 1 | 0.0083683062 | 0.025103157 |
| 106.5 | 117.5 | heldout_A1_prime;development_A1 | 0.97422696 | 0.97422696 | 1 | 1 | 0.057262574 | 0.21583356 |
| 106.5 | 125.5 | heldout_A1_prime | 0.95618569 | 0.95618569 | 1 | 1 | 0.018464739 | 0.057397432 |
| 106.5 | 133.5 | heldout_A1_prime | 0.93857916 | 0.93857916 | 1 | 1 | 0.0085459841 | 0.026558506 |
| 107 | 117 | heldout_A1_prime;development_A1 | 0.97651055 | 0.97651055 | 1 | 1 | 0.061160379 | 0.21869592 |
| 107 | 125 | heldout_A1_prime | 0.95838677 | 0.95838677 | 1 | 1 | 0.024310458 | 0.06521813 |
| 107 | 133 | heldout_A1_prime | 0.94070436 | 0.94070436 | 1 | 1 | 0.0086804305 | 0.027430479 |
| 107.5 | 116.5 | heldout_A1_prime;development_A1 | 0.97880665 | 0.97880665 | 1 | 1 | 0.051300234 | 0.24067101 |
| 107.5 | 124.5 | heldout_A1_prime | 0.9606007 | 0.9606007 | 1 | 1 | 0.031277096 | 0.072838367 |
| 107.5 | 132.5 | heldout_A1_prime | 0.94284286 | 0.94284286 | 1 | 1 | 0.0088652498 | 0.027613846 |
| 108 | 116 | heldout_A1_prime;development_A1 | 0.98111505 | 0.98111505 | 1 | 1 | 0.042238017 | 0.27942393 |
| 108 | 124 | heldout_A1_prime | 0.96282728 | 0.96282728 | 1 | 1 | 0.039463253 | 0.079644176 |
| 108 | 132 | heldout_A1_prime;development_fixed;development_A1 | 0.94499444 | 0.94499444 | 1 | 1 | 0.0092095094 | 0.027072515 |
| 108.5 | 115.5 | heldout_A1_prime | 0.98343555 | 0.98343555 | 1 | 1 | 0.04083643 | 0.30782 |
| 108.5 | 123.5 | heldout_A1_prime | 0.9650663 | 0.9650663 | 1 | 1 | 0.04894932 | 0.091277335 |
| 108.5 | 131.5 | heldout_A1_prime;development_A1 | 0.9471589 | 0.9471589 | 1 | 1 | 0.009809545 | 0.025877987 |
| 109 | 115 | heldout_A1_prime | 0.98576793 | 0.98576793 | 1 | 1 | 0.050744793 | 0.32252833 |
| 109 | 123 | heldout_A1_prime | 0.96731755 | 0.96731755 | 1 | 1 | 0.059466187 | 0.10605947 |
| 109 | 131 | heldout_A1_prime;development_A1 | 0.94933602 | 0.94933602 | 1 | 1 | 0.01071158 | 0.027484473 |
| 109.5 | 122.5 | heldout_A1_prime | 0.96958083 | 0.96958083 | 1 | 1 | 0.070063767 | 0.12022893 |
| 109.5 | 130.5 | heldout_A1_prime;development_A1 | 0.9515256 | 0.9515256 | 1 | 1 | 0.011869347 | 0.031566823 |
| 110 | 122 | heldout_A1_prime | 0.97185591 | 0.97185591 | 1 | 1 | 0.074370347 | 0.14024759 |
| 110 | 130 | heldout_A1_prime;development_A1 | 0.95372741 | 0.95372741 | 1 | 1 | 0.013097907 | 0.036339793 |
| 110 | 138 | heldout_A2_prime;heldout_A1_prime | 0.93595016 | 0.93595016 | 1 | 1 | 0.0037659503 | 0.022009012 |
| 110.5 | 121.5 | heldout_A1_prime | 0.9741426 | 0.9741426 | 1 | 1 | 0.062655618 | 0.17903086 |
| 110.5 | 129.5 | heldout_A1_prime;development_A1 | 0.95594125 | 0.95594125 | 1 | 1 | 0.01402784 | 0.041710319 |
| 110.5 | 137.5 | heldout_A1_prime | 0.93809714 | 0.93809714 | 1 | 1 | 0.0042748449 | 0.022429129 |
| 111 | 121 | heldout_A1_prime | 0.97644067 | 0.97644067 | 1 | 1 | 0.047681993 | 0.22465628 |
| 111 | 129 | heldout_A1_prime;development_A1 | 0.9581669 | 0.9581669 | 1 | 1 | 0.014080978 | 0.047478983 |
| 111 | 137 | heldout_A1_prime | 0.94025644 | 0.94025644 | 1 | 1 | 0.004916806 | 0.022444641 |
| 111.5 | 120.5 | heldout_A1_prime | 0.97874992 | 0.97874992 | 1 | 1 | 0.031488314 | 0.27683908 |
| 111.5 | 128.5 | heldout_A1_prime;development_A1 | 0.96040416 | 0.96040416 | 1 | 1 | 0.012569329 | 0.053328926 |
| 111.5 | 136.5 | heldout_A1_prime | 0.94242785 | 0.94242785 | 1 | 1 | 0.0056006332 | 0.025031799 |
| 112 | 120 | heldout_A1_prime | 0.98107012 | 0.98107012 | 1 | 1 | 0.019887516 | 0.3304716 |
| 112 | 128 | heldout_A1_prime;development_A1 | 0.9626528 | 0.9626528 | 1 | 1 | 0.0095739042 | 0.058853434 |
| 112 | 136 | heldout_A1_prime | 0.94461116 | 0.94461116 | 1 | 1 | 0.0062292613 | 0.030293792 |
| 112.5 | 119.5 | heldout_A1_prime | 0.98340107 | 0.98340107 | 1 | 1 | 0.019167884 | 0.37011567 |
| 112.5 | 127.5 | heldout_A1_prime;development_A1 | 0.96491261 | 0.96491261 | 1 | 1 | 0.010842142 | 0.063699186 |
| 112.5 | 135.5 | heldout_A1_prime | 0.94680614 | 0.94680614 | 1 | 1 | 0.0067396371 | 0.036240077 |
| 113 | 119 | heldout_A1_prime | 0.98574254 | 0.98574254 | 1 | 1 | 0.025374576 | 0.38403527 |
| 113 | 127 | heldout_A1_prime;development_A1 | 0.96718337 | 0.96718337 | 1 | 1 | 0.0229187 | 0.073898671 |
| 113 | 135 | heldout_A1_prime | 0.94901257 | 0.94901257 | 1 | 1 | 0.0071449141 | 0.04237837 |
| 113.5 | 126.5 | heldout_A1_prime;development_A1 | 0.96946487 | 0.96946487 | 1 | 1 | 0.041642807 | 0.087184147 |
| 113.5 | 134.5 | heldout_A1_prime | 0.95123024 | 0.95123024 | 1 | 1 | 0.0075731769 | 0.048064499 |
| 114 | 126 | heldout_A1_prime;development_fixed;development_A1 | 0.97175689 | 0.97175689 | 1 | 1 | 0.042896974 | 0.10164067 |
| 114 | 134 | heldout_A1_prime | 0.95345893 | 0.95345893 | 1 | 1 | 0.0082663237 | 0.052670327 |
| 114 | 142 | heldout_A2_prime;heldout_A1_prime | 0.93620853 | 0.93620853 | 1 | 1 | 0.0062993527 | 0.019223235 |
| 114.5 | 125.5 | heldout_A1_prime;development_A1 | 0.9740592 | 0.9740592 | 1 | 1 | 0.041848339 | 0.12406128 |
| 114.5 | 133.5 | heldout_A1_prime | 0.95569842 | 0.95569842 | 1 | 1 | 0.0094672622 | 0.055797317 |
| 114.5 | 141.5 | heldout_A1_prime | 0.93833789 | 0.93833789 | 1 | 1 | 0.006721495 | 0.02033913 |
| 115 | 125 | heldout_A1_prime;development_A1 | 0.97637159 | 0.97637159 | 1 | 1 | 0.045892042 | 0.16905175 |
| 115 | 133 | heldout_A1_prime | 0.95794848 | 0.95794848 | 1 | 1 | 0.011217738 | 0.060708854 |
| 115 | 141 | heldout_A1_prime | 0.94048016 | 0.94048016 | 1 | 1 | 0.0075916368 | 0.02109368 |
| 115.5 | 124.5 | heldout_A1_prime;development_A1 | 0.97869383 | 0.97869383 | 1 | 1 | 0.049418257 | 0.19874823 |
| 115.5 | 132.5 | heldout_A1_prime | 0.9602089 | 0.9602089 | 1 | 1 | 0.013284498 | 0.070778415 |
| 115.5 | 140.5 | heldout_A1_prime | 0.94263513 | 0.94263513 | 1 | 1 | 0.0085598562 | 0.021355244 |
| 116 | 124 | heldout_A1_prime;development_A1 | 0.9810257 | 0.9810257 | 1 | 1 | 0.047010017 | 0.22428999 |
| 116 | 132 | heldout_A1_prime | 0.96247945 | 0.96247945 | 1 | 1 | 0.015353941 | 0.079203741 |
| 116 | 140 | heldout_A1_prime;development_fixed;development_A1 | 0.9448026 | 0.9448026 | 1 | 1 | 0.0084350074 | 0.021039236 |
| 116.5 | 123.5 | heldout_A1_prime | 0.98336698 | 0.98336698 | 1 | 1 | 0.053773635 | 0.24366711 |
| 116.5 | 131.5 | heldout_A1_prime | 0.96475991 | 0.96475991 | 1 | 1 | 0.017449582 | 0.085666023 |
| 116.5 | 139.5 | heldout_A1_prime;development_A1 | 0.94698233 | 0.94698233 | 1 | 1 | 0.0078431102 | 0.024530105 |
| 117 | 123 | heldout_A1_prime | 0.98571744 | 0.98571744 | 1 | 1 | 0.07299172 | 0.25714108 |
| 117 | 131 | heldout_A1_prime | 0.96705006 | 0.96705006 | 1 | 1 | 0.020421815 | 0.090309423 |
| 117 | 139 | heldout_A1_prime;development_A1 | 0.94917413 | 0.94917413 | 1 | 1 | 0.0071248421 | 0.029882024 |
| 117.5 | 130.5 | heldout_A1_prime | 0.96934966 | 0.96934966 | 1 | 1 | 0.02591972 | 0.10117241 |
| 117.5 | 138.5 | heldout_A1_prime;development_A1 | 0.95137777 | 0.95137777 | 1 | 1 | 0.0074577554 | 0.036769899 |
| 118 | 130 | heldout_A1_prime | 0.9716585 | 0.9716585 | 1 | 1 | 0.035218253 | 0.11561016 |
| 118 | 138 | heldout_A1_prime;development_A1 | 0.95359303 | 0.95359303 | 1 | 1 | 0.010413145 | 0.045377216 |
| 118 | 146 | heldout_A2_prime;heldout_A1_prime | 0.9367273 | 0.9367273 | 1 | 1 | 0.0053531999 | 0.027863677 |
| 118.5 | 129.5 | heldout_A1_prime | 0.97397634 | 0.97397634 | 1 | 1 | 0.047208686 | 0.1266326 |
| 118.5 | 137.5 | heldout_A1_prime;development_A1 | 0.95581971 | 0.95581971 | 1 | 1 | 0.016218832 | 0.055876458 |
| 118.5 | 145.5 | heldout_A1_prime | 0.93882127 | 0.93882127 | 1 | 1 | 0.0053852341 | 0.028784796 |
| 119 | 129 | heldout_A1_prime | 0.97630295 | 0.97630295 | 1 | 1 | 0.056241623 | 0.13350642 |
| 119 | 137 | heldout_A1_prime;development_A1 | 0.95805758 | 0.95805758 | 1 | 1 | 0.020834505 | 0.068429848 |
| 119 | 145 | heldout_A1_prime | 0.94092933 | 0.94092933 | 1 | 1 | 0.0046321074 | 0.029459314 |
| 119.5 | 128.5 | heldout_A1_prime | 0.9786381 | 0.9786381 | 1 | 1 | 0.066693107 | 0.13843731 |
| 119.5 | 136.5 | heldout_A1_prime;development_A1 | 0.96030643 | 0.96030643 | 1 | 1 | 0.021416819 | 0.083087909 |
| 119.5 | 144.5 | heldout_A1_prime | 0.94305129 | 0.94305129 | 1 | 1 | 0.0054638073 | 0.030072467 |
| 120 | 128 | heldout_A1_prime | 0.98098157 | 0.98098157 | 1 | 1 | 0.055295793 | 0.14523367 |
| 120 | 136 | heldout_A1_prime;development_A1 | 0.96256604 | 0.96256604 | 1 | 1 | 0.021847538 | 0.099506599 |
| 120 | 144 | heldout_A1_prime | 0.94518694 | 0.94518694 | 1 | 1 | 0.0079529227 | 0.030903061 |
| 120.5 | 127.5 | heldout_A1_prime | 0.98333312 | 0.98333312 | 1 | 1 | 0.043039922 | 0.19921148 |
| 120.5 | 135.5 | heldout_A1_prime;development_A1 | 0.96483619 | 0.96483619 | 1 | 1 | 0.022965439 | 0.11659491 |
| 120.5 | 143.5 | heldout_A1_prime | 0.94733606 | 0.94733606 | 1 | 1 | 0.0093271001 | 0.038194829 |
| 121 | 127 | heldout_A1_prime | 0.9856925 | 0.9856925 | 1 | 1 | 0.049483292 | 0.25268808 |
| 121 | 135 | heldout_A1_prime;development_A1 | 0.96711665 | 0.96711665 | 1 | 1 | 0.026033026 | 0.13269939 |
| 121 | 143 | heldout_A1_prime | 0.94949846 | 0.94949846 | 1 | 1 | 0.010970577 | 0.047168449 |
| 121.5 | 134.5 | heldout_A1_prime;development_A1 | 0.96940721 | 0.96940721 | 1 | 1 | 0.031829772 | 0.14670444 |
| 121.5 | 142.5 | heldout_A1_prime | 0.95167392 | 0.95167392 | 1 | 1 | 0.012912516 | 0.057731089 |
| 122 | 134 | heldout_A1_prime;development_fixed;development_A1 | 0.97170764 | 0.97170764 | 1 | 1 | 0.039906622 | 0.1584903 |
| 122 | 142 | heldout_A1_prime | 0.95386223 | 0.95386223 | 1 | 1 | 0.015224837 | 0.069772134 |
| 122 | 150 | heldout_A2_prime;heldout_A1_prime | 0.93725106 | 0.93725106 | 1 | 1 | 0.0063485001 | 0.022131841 |
| 122.5 | 133.5 | heldout_A1_prime;development_A1 | 0.97401773 | 0.97401773 | 1 | 1 | 0.049083095 | 0.16759599 |
| 122.5 | 141.5 | heldout_A1_prime | 0.95606319 | 0.95606319 | 1 | 1 | 0.018026688 | 0.083111318 |
| 122.5 | 149.5 | heldout_A1_prime | 0.93930927 | 0.93930927 | 1 | 1 | 0.0068735648 | 0.023012979 |
| 123 | 133 | heldout_A1_prime;development_A1 | 0.97633723 | 0.97633723 | 1 | 1 | 0.058413664 | 0.17262495 |
| 123 | 141 | heldout_A1_prime | 0.95827659 | 0.95827659 | 1 | 1 | 0.021483394 | 0.097470119 |
| 123 | 149 | heldout_A1_prime | 0.94138278 | 0.94138278 | 1 | 1 | 0.0079380133 | 0.027262599 |
| 123.5 | 132.5 | heldout_A1_prime;development_A1 | 0.97866594 | 0.97866594 | 1 | 1 | 0.068129232 | 0.19118399 |
| 123.5 | 140.5 | heldout_A1_prime | 0.96050221 | 0.96050221 | 1 | 1 | 0.025794229 | 0.11243838 |
| 123.5 | 148.5 | heldout_A1_prime | 0.94347139 | 0.94347139 | 1 | 1 | 0.0096402499 | 0.032351523 |
| 124 | 132 | heldout_A1_prime;development_A1 | 0.98100362 | 0.98100362 | 1 | 1 | 0.080721737 | 0.22301951 |
| 124 | 140 | heldout_A1_prime | 0.96273984 | 0.96273984 | 1 | 1 | 0.028719463 | 0.12747124 |
| 124 | 148 | heldout_A1_prime;development_fixed;development_A1 | 0.9455749 | 0.9455749 | 1 | 1 | 0.010878304 | 0.038406653 |
| 124.5 | 131.5 | heldout_A1_prime | 0.98335003 | 0.98335003 | 1 | 1 | 0.079716512 | 0.24066476 |
| 124.5 | 139.5 | heldout_A1_prime | 0.96498928 | 0.96498928 | 1 | 1 | 0.034837685 | 0.150546 |
| 124.5 | 147.5 | heldout_A1_prime;development_A1 | 0.94769311 | 0.94769311 | 1 | 1 | 0.013712859 | 0.05055917 |
| 125 | 131 | heldout_A1_prime | 0.98570496 | 0.98570496 | 1 | 1 | 0.10578358 | 0.27598874 |
| 125 | 139 | heldout_A1_prime | 0.96725031 | 0.96725031 | 1 | 1 | 0.039937811 | 0.16419213 |
| 125 | 147 | heldout_A1_prime;development_A1 | 0.94982582 | 0.94982582 | 1 | 1 | 0.013850206 | 0.059371418 |
| 125.5 | 138.5 | heldout_A1_prime | 0.96952272 | 0.96952272 | 1 | 1 | 0.047545929 | 0.17614551 |
| 125.5 | 146.5 | heldout_A1_prime;development_A1 | 0.95197282 | 0.95197282 | 1 | 1 | 0.014007819 | 0.0699875 |
| 126 | 138 | heldout_A1_prime | 0.97180629 | 0.97180629 | 1 | 1 | 0.055001464 | 0.18702105 |
| 126 | 146 | heldout_A1_prime;development_A1 | 0.95413392 | 0.95413392 | 1 | 1 | 0.014427408 | 0.082509688 |
| 126 | 154 | heldout_A2_prime;heldout_A1_prime | 0.93778259 | 0.93778259 | 1 | 1 | 0.0061933205 | 0.02722619 |
| 126.5 | 137.5 | heldout_A1_prime | 0.9741008 | 0.9741008 | 1 | 1 | 0.058474648 | 0.19840468 |
| 126.5 | 145.5 | heldout_A1_prime;development_A1 | 0.95630892 | 0.95630892 | 1 | 1 | 0.015930763 | 0.096851384 |
| 126.5 | 153.5 | heldout_A1_prime | 0.93980449 | 0.93980449 | 1 | 1 | 0.005942201 | 0.028468317 |
| 127 | 137 | heldout_A1_prime | 0.97640605 | 0.97640605 | 1 | 1 | 0.059464886 | 0.21174543 |
| 127 | 145 | heldout_A1_prime;development_A1 | 0.9584976 | 0.9584976 | 1 | 1 | 0.019726745 | 0.11266359 |
| 127 | 153 | heldout_A1_prime | 0.94184291 | 0.94184291 | 1 | 1 | 0.00598076 | 0.030801559 |
| 127.5 | 136.5 | heldout_A1_prime | 0.97872181 | 0.97872181 | 1 | 1 | 0.073563445 | 0.22571764 |
| 127.5 | 144.5 | heldout_A1_prime;development_A1 | 0.96069978 | 0.96069978 | 1 | 1 | 0.026311627 | 0.12930871 |
| 127.5 | 152.5 | heldout_A1_prime | 0.94389766 | 0.94389766 | 1 | 1 | 0.0064094801 | 0.034533227 |
| 128 | 136 | heldout_A1_prime | 0.98104786 | 0.98104786 | 1 | 1 | 0.081751947 | 0.23559003 |
| 128 | 144 | heldout_A1_prime;development_A1 | 0.96291523 | 0.96291523 | 1 | 1 | 0.032274351 | 0.14592855 |
| 128 | 152 | heldout_A1_prime | 0.94596854 | 0.94596854 | 1 | 1 | 0.0071817483 | 0.039747903 |
| 128.5 | 135.5 | heldout_A1_prime | 0.98338399 | 0.98338399 | 1 | 1 | 0.079147436 | 0.23743268 |
| 128.5 | 143.5 | heldout_A1_prime;development_A1 | 0.96514377 | 0.96514377 | 1 | 1 | 0.036217139 | 0.16163059 |
| 128.5 | 151.5 | heldout_A1_prime | 0.94805537 | 0.94805537 | 1 | 1 | 0.0081225424 | 0.046342731 |
| 129 | 135 | heldout_A1_prime | 0.98572996 | 0.98572996 | 1 | 1 | 0.073333776 | 0.2422839 |
| 129 | 143 | heldout_A1_prime;development_A1 | 0.96738519 | 0.96738519 | 1 | 1 | 0.042575623 | 0.17571103 |
| 129 | 151 | heldout_A1_prime | 0.95015794 | 0.95015794 | 1 | 1 | 0.0090106246 | 0.054147579 |
| 129.5 | 142.5 | heldout_A1_prime;development_A1 | 0.96963927 | 0.96963927 | 1 | 1 | 0.051713784 | 0.18772663 |
| 129.5 | 150.5 | heldout_A1_prime | 0.95227607 | 0.95227607 | 1 | 1 | 0.0096526237 | 0.063035222 |
| 130 | 142 | heldout_A1_prime;development_fixed;development_A1 | 0.97190582 | 0.97190582 | 1 | 1 | 0.049981979 | 0.19738323 |
| 130 | 150 | heldout_A1_prime | 0.95440955 | 0.95440955 | 1 | 1 | 0.0099724569 | 0.072967072 |
| 130 | 158 | heldout_A2_prime;heldout_A1_prime | 0.93832488 | 0.93832488 | 1 | 1 | 0.0098216544 | 0.033571617 |
| 130.5 | 141.5 | heldout_A1_prime;development_A1 | 0.97418463 | 0.97418463 | 1 | 1 | 0.038992054 | 0.20453253 |
| 130.5 | 149.5 | heldout_A1_prime | 0.95655819 | 0.95655819 | 1 | 1 | 0.0101989 | 0.083961616 |
| 130.5 | 157.5 | heldout_A1_prime | 0.9403097 | 0.9403097 | 1 | 1 | 0.0096004057 | 0.035040064 |
| 131 | 141 | heldout_A1_prime;development_A1 | 0.97647549 | 0.97647549 | 1 | 1 | 0.030152511 | 0.20935028 |
| 131 | 149 | heldout_A1_prime | 0.9587218 | 0.9587218 | 1 | 1 | 0.011183716 | 0.096000095 |
| 131 | 157 | heldout_A1_prime | 0.94231229 | 0.94231229 | 1 | 1 | 0.0097414811 | 0.037117407 |
| 131.5 | 140.5 | heldout_A1_prime;development_A1 | 0.97877818 | 0.97877818 | 1 | 1 | 0.050483382 | 0.21252413 |
| 131.5 | 148.5 | heldout_A1_prime | 0.96090018 | 0.96090018 | 1 | 1 | 0.014339279 | 0.1089011 |
| 131.5 | 156.5 | heldout_A1_prime | 0.94433248 | 0.94433248 | 1 | 1 | 0.0087098025 | 0.040050466 |
| 132 | 140 | heldout_A1_prime;development_A1 | 0.98109251 | 0.98109251 | 1 | 1 | 0.082898024 | 0.21598067 |
| 132 | 148 | heldout_A1_prime | 0.96309314 | 0.96309314 | 1 | 1 | 0.020621327 | 0.12220736 |
| 132 | 156 | heldout_A1_prime;development_fixed;development_A1 | 0.94637006 | 0.94637006 | 1 | 1 | 0.0080679495 | 0.044081568 |
| 132.5 | 139.5 | heldout_A1_prime | 0.98341825 | 0.98341825 | 1 | 1 | 0.093818597 | 0.22311574 |
| 132.5 | 147.5 | heldout_A1_prime | 0.96530048 | 0.96530048 | 1 | 1 | 0.030156332 | 0.13517045 |
| 132.5 | 155.5 | heldout_A1_prime;development_A1 | 0.94842486 | 0.94842486 | 1 | 1 | 0.009244377 | 0.049433007 |
| 133 | 139 | heldout_A1_prime | 0.98575519 | 0.98575519 | 1 | 1 | 0.093063564 | 0.235464 |
| 133 | 147 | heldout_A1_prime | 0.96752199 | 0.96752199 | 1 | 1 | 0.042255116 | 0.14700502 |
| 133 | 155 | heldout_A1_prime;development_A1 | 0.95049668 | 0.95049668 | 1 | 1 | 0.012450266 | 0.05631399 |
| 133.5 | 146.5 | heldout_A1_prime | 0.96975749 | 0.96975749 | 1 | 1 | 0.051445196 | 0.15752693 |
| 133.5 | 154.5 | heldout_A1_prime;development_A1 | 0.95258534 | 0.95258534 | 1 | 1 | 0.01332769 | 0.064947177 |
| 134 | 146 | heldout_A1_prime | 0.97200678 | 0.97200678 | 1 | 1 | 0.058146274 | 0.16788781 |
| 134 | 154 | heldout_A1_prime;development_A1 | 0.95469064 | 0.95469064 | 1 | 1 | 0.014474219 | 0.075587704 |
| 134 | 162 | heldout_A2_prime;heldout_A1_prime | 0.93888112 | 0.93888112 | 1 | 1 | 0.0091744674 | 0.024599634 |
| 134.5 | 145.5 | heldout_A1_prime | 0.97426965 | 0.97426965 | 1 | 1 | 0.055083606 | 0.18097226 |
| 134.5 | 153.5 | heldout_A1_prime;development_A1 | 0.9568124 | 0.9568124 | 1 | 1 | 0.016117448 | 0.088492945 |
| 134.5 | 161.5 | heldout_A1_prime | 0.94082788 | 0.94082788 | 1 | 1 | 0.0094277702 | 0.026714882 |
| 135 | 145 | heldout_A1_prime | 0.97654591 | 0.97654591 | 1 | 1 | 0.055273218 | 0.20123971 |
| 135 | 153 | heldout_A1_prime;development_A1 | 0.95895043 | 0.95895043 | 1 | 1 | 0.01838443 | 0.1038073 |
| 135 | 161 | heldout_A1_prime | 0.9427937 | 0.9427937 | 1 | 1 | 0.0096041962 | 0.028189455 |
| 135.5 | 144.5 | heldout_A1_prime | 0.97883535 | 0.97883535 | 1 | 1 | 0.060187169 | 0.23272353 |
| 135.5 | 152.5 | heldout_A1_prime;development_A1 | 0.96110454 | 0.96110454 | 1 | 1 | 0.021194933 | 0.12136911 |
| 135.5 | 160.5 | heldout_A1_prime | 0.94477841 | 0.94477841 | 1 | 1 | 0.0098398888 | 0.031349795 |
| 136 | 144 | heldout_A1_prime | 0.98113778 | 0.98113778 | 1 | 1 | 0.063602896 | 0.27407932 |
| 136 | 152 | heldout_A1_prime;development_A1 | 0.96327455 | 0.96327455 | 1 | 1 | 0.024288317 | 0.14052663 |
| 136 | 160 | heldout_A1_prime | 0.94678182 | 0.94678182 | 1 | 1 | 0.010314828 | 0.038022284 |
| 136.5 | 143.5 | heldout_A1_prime | 0.98345299 | 0.98345299 | 1 | 1 | 0.041555502 | 0.31389603 |
| 136.5 | 151.5 | heldout_A1_prime;development_A1 | 0.96546025 | 0.96546025 | 1 | 1 | 0.027065796 | 0.16011079 |
| 136.5 | 159.5 | heldout_A1_prime | 0.94880375 | 0.94880375 | 1 | 1 | 0.011179268 | 0.045751742 |
| 137 | 143 | heldout_A1_prime | 0.98578078 | 0.98578078 | 1 | 1 | 0.033894985 | 0.3338046 |
| 137 | 151 | heldout_A1_prime;development_A1 | 0.96766148 | 0.96766148 | 1 | 1 | 0.028458401 | 0.17866029 |
| 137 | 159 | heldout_A1_prime | 0.95084402 | 0.95084402 | 1 | 1 | 0.01190659 | 0.054290212 |
| 137.5 | 150.5 | heldout_A1_prime;development_A1 | 0.96987802 | 0.96987802 | 1 | 1 | 0.031344972 | 0.19480864 |
| 137.5 | 158.5 | heldout_A1_prime | 0.95290244 | 0.95290244 | 1 | 1 | 0.010367455 | 0.06334552 |
| 138 | 150 | heldout_A1_prime;development_fixed;development_A1 | 0.9721097 | 0.9721097 | 1 | 1 | 0.035339695 | 0.20764735 |
| 138 | 158 | heldout_A1_prime | 0.95497883 | 0.95497883 | 1 | 1 | 0.0098045765 | 0.072607129 |
| 138 | 166 | heldout_A2_prime;heldout_A1_prime | 0.93945485 | 0.93945485 | 1 | 1 | 0.0067296124 | 0.020377218 |
| 138.5 | 149.5 | heldout_A1_prime;development_A1 | 0.97435633 | 0.97435633 | 1 | 1 | 0.039043657 | 0.21704673 |
| 138.5 | 157.5 | heldout_A1_prime | 0.95707302 | 0.95707302 | 1 | 1 | 0.011691944 | 0.081798364 |
| 138.5 | 165.5 | heldout_A1_prime | 0.94136231 | 0.94136231 | 1 | 1 | 0.006399463 | 0.022281615 |
| 139 | 149 | heldout_A1_prime;development_A1 | 0.9766177 | 0.9766177 | 1 | 1 | 0.04337844 | 0.22376373 |
| 139 | 157 | heldout_A1_prime | 0.95918481 | 0.95918481 | 1 | 1 | 0.016127538 | 0.090759712 |
| 139 | 165 | heldout_A1_prime | 0.94329017 | 0.94329017 | 1 | 1 | 0.0064103775 | 0.025818006 |
| 139.5 | 148.5 | heldout_A1_prime;development_A1 | 0.97889363 | 0.97889363 | 1 | 1 | 0.049731354 | 0.22908715 |
| 139.5 | 156.5 | heldout_A1_prime | 0.96131404 | 0.96131404 | 1 | 1 | 0.018348674 | 0.10759087 |
| 139.5 | 164.5 | heldout_A1_prime | 0.94523826 | 0.94523826 | 1 | 1 | 0.0068722722 | 0.031281947 |
| 140 | 148 | heldout_A1_prime;development_A1 | 0.98118394 | 0.98118394 | 1 | 1 | 0.052114128 | 0.23493762 |
| 140 | 156 | heldout_A1_prime | 0.9634605 | 0.9634605 | 1 | 1 | 0.018965747 | 0.13040836 |
| 140 | 164 | heldout_A1_prime;development_fixed;development_A1 | 0.9472064 | 0.9472064 | 1 | 1 | 0.0078382627 | 0.038854794 |
| 140.5 | 147.5 | heldout_A1_prime | 0.98348841 | 0.98348841 | 1 | 1 | 0.054793357 | 0.24500512 |
| 140.5 | 155.5 | heldout_A1_prime | 0.96562404 | 0.96562404 | 1 | 1 | 0.020719832 | 0.15501825 |
| 140.5 | 163.5 | heldout_A1_prime;development_A1 | 0.94919442 | 0.94919442 | 1 | 1 | 0.0092933649 | 0.048537331 |
| 141 | 147 | heldout_A1_prime | 0.98580686 | 0.98580686 | 1 | 1 | 0.061044327 | 0.26788312 |
| 141 | 155 | heldout_A1_prime | 0.96780445 | 0.96780445 | 1 | 1 | 0.023871869 | 0.18072709 |
| 141 | 163 | heldout_A1_prime;development_A1 | 0.95120213 | 0.95120213 | 1 | 1 | 0.011018182 | 0.060217851 |
| 141.5 | 154.5 | heldout_A1_prime | 0.97000157 | 0.97000157 | 1 | 1 | 0.027083835 | 0.20681344 |
| 141.5 | 162.5 | heldout_A1_prime;development_A1 | 0.95322936 | 0.95322936 | 1 | 1 | 0.013198499 | 0.073704971 |
| 142 | 154 | heldout_A1_prime | 0.9722152 | 0.9722152 | 1 | 1 | 0.028664783 | 0.23245908 |
| 142 | 162 | heldout_A1_prime;development_A1 | 0.95527594 | 0.95527594 | 1 | 1 | 0.015688549 | 0.088719939 |
| 142 | 170 | heldout_A2_prime;heldout_A1_prime | 0.94004999 | 0.94004999 | 1 | 1 | 0.0073783757 | 0.030805452 |
| 142.5 | 153.5 | heldout_A1_prime | 0.97444516 | 0.97444516 | 1 | 1 | 0.028344277 | 0.25661614 |
| 142.5 | 161.5 | heldout_A1_prime;development_A1 | 0.95734168 | 0.95734168 | 1 | 1 | 0.018093055 | 0.10485096 |
| 142.5 | 169.5 | heldout_A1_prime | 0.94191664 | 0.94191664 | 1 | 1 | 0.0074299698 | 0.030281426 |
| 143 | 153 | heldout_A1_prime | 0.97669128 | 0.97669128 | 1 | 1 | 0.027669034 | 0.27804129 |
| 143 | 161 | heldout_A1_prime;development_A1 | 0.95942642 | 0.95942642 | 1 | 1 | 0.020465971 | 0.12147955 |
| 143 | 169 | heldout_A1_prime | 0.94380509 | 0.94380509 | 1 | 1 | 0.0071725097 | 0.029411017 |
| 143.5 | 152.5 | heldout_A1_prime | 0.97895337 | 0.97895337 | 1 | 1 | 0.029427383 | 0.29490959 |
| 143.5 | 160.5 | heldout_A1_prime;development_A1 | 0.96152998 | 0.96152998 | 1 | 1 | 0.022742781 | 0.13771473 |
| 143.5 | 168.5 | heldout_A1_prime | 0.94571517 | 0.94571517 | 1 | 1 | 0.0071435244 | 0.02858758 |
| 144 | 152 | heldout_A1_prime | 0.98123124 | 0.98123124 | 1 | 1 | 0.036664579 | 0.30330176 |
| 144 | 160 | heldout_A1_prime;development_A1 | 0.96365218 | 0.96365218 | 1 | 1 | 0.024343382 | 0.15239971 |
| 144 | 168 | heldout_A1_prime | 0.9476467 | 0.9476467 | 1 | 1 | 0.0075315272 | 0.028411646 |
| 144.5 | 151.5 | heldout_A1_prime | 0.98352471 | 0.98352471 | 1 | 1 | 0.051996576 | 0.29635173 |
| 144.5 | 159.5 | heldout_A1_prime;development_A1 | 0.96579284 | 0.96579284 | 1 | 1 | 0.024321888 | 0.16426665 |
| 144.5 | 167.5 | heldout_A1_prime | 0.94959952 | 0.94959952 | 1 | 1 | 0.008467587 | 0.032147267 |
| 145 | 151 | heldout_A1_prime | 0.98583359 | 0.98583359 | 1 | 1 | 0.078765847 | 0.2934998 |
| 145 | 159 | heldout_A1_prime;development_A1 | 0.96795181 | 0.96795181 | 1 | 1 | 0.023563487 | 0.17227495 |
| 145 | 167 | heldout_A1_prime | 0.95157345 | 0.95157345 | 1 | 1 | 0.0099827876 | 0.037599252 |
| 145.5 | 158.5 | heldout_A1_prime;development_A1 | 0.97012889 | 0.97012889 | 1 | 1 | 0.023085098 | 0.17611301 |
| 145.5 | 166.5 | heldout_A1_prime | 0.95356832 | 0.95356832 | 1 | 1 | 0.011683843 | 0.042481182 |
| 146 | 158 | heldout_A1_prime;development_fixed;development_A1 | 0.97232392 | 0.97232392 | 1 | 1 | 0.024820119 | 0.18416518 |
| 146 | 166 | heldout_A1_prime | 0.95558396 | 0.95558396 | 1 | 1 | 0.011526567 | 0.046406368 |
| 146 | 174 | heldout_A2_prime;heldout_A1_prime | 0.94067103 | 0.94067103 | 1 | 1 | 0.0063910912 | 0.02384963 |
| 146.5 | 157.5 | heldout_A1_prime;development_A1 | 0.97453672 | 0.97453672 | 1 | 1 | 0.031223261 | 0.22453162 |
| 146.5 | 165.5 | heldout_A1_prime | 0.9576202 | 0.9576202 | 1 | 1 | 0.011637073 | 0.04927888 |
| 146.5 | 173.5 | heldout_A1_prime | 0.94249504 | 0.94249504 | 1 | 1 | 0.0071825671 | 0.022330833 |
| 147 | 157 | heldout_A1_prime;development_A1 | 0.97676711 | 0.97676711 | 1 | 1 | 0.037918214 | 0.26876928 |
| 147 | 165 | heldout_A1_prime | 0.95967688 | 0.95967688 | 1 | 1 | 0.012163551 | 0.051451179 |
| 147 | 173 | heldout_A1_prime | 0.94434232 | 0.94434232 | 1 | 1 | 0.0084301868 | 0.020905276 |
| 147.5 | 156.5 | heldout_A1_prime;development_A1 | 0.97901492 | 0.97901492 | 1 | 1 | 0.045567729 | 0.31419849 |
| 147.5 | 164.5 | heldout_A1_prime | 0.96175382 | 0.96175382 | 1 | 1 | 0.013203499 | 0.054032539 |
| 147.5 | 172.5 | heldout_A1_prime | 0.9462127 | 0.9462127 | 1 | 1 | 0.010166476 | 0.019994314 |
| 148 | 156 | heldout_A1_prime;development_A1 | 0.98127998 | 0.98127998 | 1 | 1 | 0.053189178 | 0.35865329 |
| 148 | 164 | heldout_A1_prime | 0.96385085 | 0.96385085 | 1 | 1 | 0.01497008 | 0.06096835 |
| 148 | 172 | heldout_A1_prime | 0.94810601 | 0.94810601 | 1 | 1 | 0.010216599 | 0.021122686 |
| 148.5 | 155.5 | heldout_A1_prime | 0.98356211 | 0.98356211 | 1 | 1 | 0.055813518 | 0.40049946 |
| 148.5 | 163.5 | heldout_A1_prime | 0.96596781 | 0.96596781 | 1 | 1 | 0.017927896 | 0.069709488 |
| 148.5 | 171.5 | heldout_A1_prime | 0.95002208 | 0.95002208 | 1 | 1 | 0.01069248 | 0.024042494 |
| 149 | 155 | heldout_A1_prime | 0.98586113 | 0.98586113 | 1 | 1 | 0.063165441 | 0.43740803 |
| 149 | 163 | heldout_A1_prime | 0.96810454 | 0.96810454 | 1 | 1 | 0.022800284 | 0.080732422 |
| 149 | 171 | heldout_A1_prime | 0.95196074 | 0.95196074 | 1 | 1 | 0.0116994 | 0.030240842 |
| 149.5 | 162.5 | heldout_A1_prime | 0.97026085 | 0.97026085 | 1 | 1 | 0.03030738 | 0.093825315 |
| 149.5 | 170.5 | heldout_A1_prime | 0.95392183 | 0.95392183 | 1 | 1 | 0.013251524 | 0.037831514 |
| 150 | 162 | heldout_A1_prime | 0.97243659 | 0.97243659 | 1 | 1 | 0.036616618 | 0.11222421 |
| 150 | 170 | heldout_A1_prime | 0.95590519 | 0.95590519 | 1 | 1 | 0.015272017 | 0.046874094 |
| 150.5 | 161.5 | heldout_A1_prime | 0.9746316 | 0.9746316 | 1 | 1 | 0.040577846 | 0.14295715 |
| 150.5 | 169.5 | heldout_A1_prime | 0.95791065 | 0.95791065 | 1 | 1 | 0.017608229 | 0.057334443 |
| 151 | 161 | heldout_A1_prime | 0.97684569 | 0.97684569 | 1 | 1 | 0.046503743 | 0.17715793 |
| 151 | 169 | heldout_A1_prime | 0.95993804 | 0.95993804 | 1 | 1 | 0.020057124 | 0.069028322 |
| 151.5 | 160.5 | heldout_A1_prime | 0.97907871 | 0.97907871 | 1 | 1 | 0.052364872 | 0.20863394 |
| 151.5 | 168.5 | heldout_A1_prime | 0.96198721 | 0.96198721 | 1 | 1 | 0.022409267 | 0.081561238 |
| 152 | 160 | heldout_A1_prime | 0.98133049 | 0.98133049 | 1 | 1 | 0.05648514 | 0.2346071 |
| 152 | 168 | heldout_A1_prime | 0.964058 | 0.964058 | 1 | 1 | 0.024490317 | 0.094284642 |
| 152.5 | 159.5 | heldout_A1_prime | 0.98360087 | 0.98360087 | 1 | 1 | 0.059356199 | 0.25380565 |
| 152.5 | 167.5 | heldout_A1_prime | 0.96615023 | 0.96615023 | 1 | 1 | 0.026157689 | 0.10631259 |
| 153 | 159 | heldout_A1_prime | 0.98588967 | 0.98588967 | 1 | 1 | 0.077838018 | 0.25688607 |
| 153 | 167 | heldout_A1_prime | 0.96826376 | 0.96826376 | 1 | 1 | 0.027255859 | 0.11663398 |
| 153.5 | 166.5 | heldout_A1_prime | 0.97039842 | 0.97039842 | 1 | 1 | 0.027674462 | 0.12431974 |
| 154 | 166 | heldout_A1_prime | 0.97255405 | 0.97255405 | 1 | 1 | 0.027768151 | 0.12888579 |
| 154.5 | 165.5 | heldout_A1_prime | 0.9747305 | 0.9747305 | 1 | 1 | 0.029025998 | 0.13246592 |
| 155 | 165 | heldout_A1_prime | 0.9769276 | 0.9769276 | 1 | 1 | 0.034055666 | 0.15325792 |
| 155.5 | 164.5 | heldout_A1_prime | 0.9791452 | 0.9791452 | 1 | 1 | 0.04595495 | 0.17255464 |
| 156 | 164 | heldout_A1_prime | 0.98138314 | 0.98138314 | 1 | 1 | 0.061041095 | 0.18457275 |
| 156.5 | 163.5 | heldout_A1_prime | 0.98364126 | 0.98364126 | 1 | 1 | 0.061934626 | 0.18663896 |
| 157 | 163 | heldout_A1_prime | 0.98591941 | 0.98591941 | 1 | 1 | 0.071917731 | 0.19900217 |

Per-band CSV: [filter_audit_500Hz_bands.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/filter_audit_500Hz_bands.csv>).


Primary method: tag **v1.0**, commit `71ebc16aed32ca38be73a800738b975e5806b330`. All new APC analyses execute byte-identical files extracted from that tag. No tagged code, tags, prior simulation inputs or saved results were modified. APC v2.0 is reported with its corrected prespecified C1–C4 evaluation below.

## Rodent channel evidence

EC013/ec013.157, extracted recording R2: **E1, Brainstorm row/channel index 1 (one-based)**. R2.Description is E1; R2.Comment records extraction of E1 over 0–631.199 s; R2.History identifies `EC013/ec013.157.eeg/data_block001.mat`. The imported channel file names its first entry E1. The saved 65-channel crop row 1 matches R2 samples 40800:372501 exactly across all 331,702 samples (maximum absolute difference 0). Its Time vector restarts at zero; it does not retain the absolute R2 timestamps.

**Shank and anatomical layer: unresolved.** No session XML or explicit acquisition-channel-to-shank/layer map was found in the inspected local LFP tree. The E1 channel record has empty Group/Comment and zero coordinates. The original raw-file link points to `/Users/lucwilson/Desktop/crcns/hc3/ec013/ec013.157/ec013.157.eeg`, which is not the local data location. E1 alone does not establish an XML zero-based channel index, shank or layer. No CA1 or layer label is assigned. The public [CRCNS hc-3 page](https://crcns.org/data-sets/hc/hc-3) identifies the dataset but provides no E1-specific mapping; the session discussion on CRCNS concerns cell/shank labels and does not map this LFP channel.

Evidence, exact paths and extraction/import histories: [channel_evidence.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/channel_evidence.json>). Local session inventory: [local_data_inspection.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/local_data_inspection.json>).

## Bout definitions and analysis

The original saved `apc_ec013_run_rest_results.mat` supplies all 12 run and 12 rest bouts and their sample indices. No bout was split, merged, reclassified or reselected. Sample rate is 1250 Hz. Original analysis indices: 40800:372501; original threshold |speed| >6; minimum bout duration 5 s. Definitions: [bout_definitions.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/bout_definitions.csv>).

APC: amplitude range [80,150] Hz, all other v1.0 defaults. No surrogate normalization is enabled; C_APC is raw Canolty MVL. Ozkurt MVL is raw MVL / sqrt(mean(A²)), using the exact final v1 Butterworth envelope and phase. Preferred phase is the angle of mean(A exp(i phase)), in degrees. A separate diagnostic copy only exports intermediate arrays; every rodent/canonical output and runInfo was checked exactly against the untouched frozen function.

A2′ rodent scans: independent maxima for MVL-raw, MVL-Ozkurt, KLMI and GLM, phase grid 4:0.5:12 Hz, phase half-width 1.5 Hz, amplitude grid 80:4:148 Hz, fixed amplitude half-width 12 Hz. Filters and metric formulas follow the inherited comparators: butter(4) realized as guarded SOS with filtfilt, 18 KL bins, GLM R². Ozkurt MVL is additionally reported at the frequency pair selected by each metric. A2′ held-out plots retain their original grids 3:0.5:14 and 80:4:160 Hz and fixed 14-Hz amplitude half-width; they are not recomputed with the rodent settings.

All per-bout method results: [rodent_bouts_SOS.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/rodent_bouts_SOS.csv>).

### APC v1.0

| state | bout | duration_s | fP_hz | fA_hz | score | raw_mvl | ozkurt_mvl | preferred_phase_deg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run | 1 | 13.2408 | 7.86732 | 114 | 0.00395295 | 0.00395295 | 0.079817 | 9.22333 |
| run | 2 | 11.24 | 7.7798 | 130 | 0.00362065 | 0.00362065 | 0.0927574 | -1.36822 |
| run | 3 | 10.5848 | 7.7588 | 116 | 0.00301111 | 0.00301111 | 0.0670492 | 7.64714 |
| run | 4 | 9.9504 | 7.77647 | 130 | 0.00309533 | 0.00309533 | 0.0820812 | 2.03565 |
| run | 5 | 10.6864 | 7.67729 | 114 | 0.00418474 | 0.00418474 | 0.0791545 | -11.3706 |
| run | 6 | 10.7528 | 7.60552 | 88 | 0.00568412 | 0.00568412 | 0.0925075 | -28.3681 |
| run | 7 | 9.3616 | 7.63371 | 106 | 0.00499907 | 0.00499907 | 0.0898156 | -8.69797 |
| run | 8 | 9.2976 | 7.52107 | 117 | 0.00218255 | 0.00218255 | 0.0464112 | -14.7737 |
| run | 9 | 9.4416 | 7.62788 | 108 | 0.00581992 | 0.00581992 | 0.11048 | -13.1865 |
| run | 10 | 8.1744 | 7.54899 | 106 | 0.00489979 | 0.00489979 | 0.0959182 | -12.4959 |
| run | 11 | 10.3864 | 7.60859 | 113 | 0.00426685 | 0.00426685 | 0.0841677 | -2.7294 |
| run | 12 | 10.9608 | 7.59061 | 124 | 0.00399058 | 0.00399058 | 0.0904901 | -15.0848 |
| rest | 1 | 11.4744 | 7.97886 | 122 | 0.00307015 | 0.00307015 | 0.0788018 | -1.51859 |
| rest | 2 | 15.5896 | 7.24893 | 98 | 0.00261796 | 0.00261796 | 0.0599044 | 1.56537 |
| rest | 3 | 7.9816 | 6.71512 | 124 | 0.00253138 | 0.00253138 | 0.0811899 | 12.4481 |
| rest | 4 | 10.8 | 6.90872 | 83 | 0.00176341 | 0.00176341 | 0.041516 | -6.03801 |
| rest | 5 | 13.2192 | 7.82564 | 104 | 0.00388602 | 0.00388602 | 0.0876257 | -1.15465 |
| rest | 6 | 10.1136 | 6.23186 | 91 | 0.00274455 | 0.00274455 | 0.0629111 | 11.127 |
| rest | 7 | 6.1256 | 6.38371 | 115 | 0.0033656 | 0.0033656 | 0.0988942 | 12.8849 |
| rest | 8 | 16.492 | 7.75515 | 88 | 0.00374584 | 0.00374584 | 0.0655886 | 27.8057 |
| rest | 9 | 9.3056 | 6.56809 | 109 | 0.00254588 | 0.00254588 | 0.0726653 | 38.0413 |
| rest | 10 | 11.556 | 6.56469 | 123 | 0.00176026 | 0.00176026 | 0.0627926 | 13.7267 |
| rest | 11 | 7.0824 | 7.25456 | 116 | 0.0027592 | 0.0027592 | 0.0778218 | -11.8429 |
| rest | 12 | 13.7256 | 6.49545 | 84 | 0.00227658 | 0.00227658 | 0.058959 | 9.11266 |


### MVL-raw

| state | bout | duration_s | fP_hz | fA_hz | score | raw_mvl | ozkurt_mvl | preferred_phase_deg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run | 1 | 13.2408 | 7.5 | 88 | 0.00863657 | 0.00863657 | 0.100938 | 0.12166 |
| run | 2 | 11.24 | 8.5 | 108 | 0.00704858 | 0.00704858 | 0.102014 | -9.46638 |
| run | 3 | 10.5848 | 9 | 100 | 0.00666325 | 0.00666325 | 0.0870564 | 10.8733 |
| run | 4 | 9.9504 | 9 | 96 | 0.00732688 | 0.00732688 | 0.091671 | 2.13022 |
| run | 5 | 10.6864 | 7.5 | 100 | 0.0085526 | 0.0085526 | 0.10747 | -24.255 |
| run | 6 | 10.7528 | 7.5 | 84 | 0.00830226 | 0.00830226 | 0.0979414 | -20.7326 |
| run | 7 | 9.3616 | 8.5 | 104 | 0.00786584 | 0.00786584 | 0.104449 | -13.7154 |
| run | 8 | 9.2976 | 8 | 100 | 0.008132 | 0.008132 | 0.105266 | -11.7217 |
| run | 9 | 9.4416 | 7.5 | 80 | 0.00851609 | 0.00851609 | 0.0913712 | 10.7924 |
| run | 10 | 8.1744 | 6.5 | 80 | 0.00931798 | 0.00931798 | 0.096655 | 2.81896 |
| run | 11 | 10.3864 | 6.5 | 80 | 0.00735094 | 0.00735094 | 0.0792628 | -21.8934 |
| run | 12 | 10.9608 | 6.5 | 116 | 0.00682735 | 0.00682735 | 0.109188 | -25.8655 |
| rest | 1 | 11.4744 | 4 | 80 | 0.00601421 | 0.00601421 | 0.0673385 | 93.0421 |
| rest | 2 | 15.5896 | 8 | 80 | 0.00504687 | 0.00504687 | 0.0634565 | 19.7929 |
| rest | 3 | 7.9816 | 7.5 | 80 | 0.0072705 | 0.0072705 | 0.0872169 | -4.60132 |
| rest | 4 | 10.8 | 4.5 | 92 | 0.00588228 | 0.00588228 | 0.090872 | 0.155816 |
| rest | 5 | 13.2192 | 4 | 80 | 0.00593882 | 0.00593882 | 0.0707268 | 65.2591 |
| rest | 6 | 10.1136 | 4 | 84 | 0.00620409 | 0.00620409 | 0.0845363 | -40.2441 |
| rest | 7 | 6.1256 | 5 | 80 | 0.00572451 | 0.00572451 | 0.0797718 | 51.4283 |
| rest | 8 | 16.492 | 8 | 80 | 0.00618619 | 0.00618619 | 0.0740329 | -3.15337 |
| rest | 9 | 9.3056 | 6.5 | 88 | 0.00556234 | 0.00556234 | 0.0810247 | -20.5333 |
| rest | 10 | 11.556 | 9 | 84 | 0.0050073 | 0.0050073 | 0.0736205 | -5.35261 |
| rest | 11 | 7.0824 | 8 | 80 | 0.0075874 | 0.0075874 | 0.0898538 | -10.6191 |
| rest | 12 | 13.7256 | 5.5 | 92 | 0.00481112 | 0.00481112 | 0.0833254 | 1.66744 |


### MVL-Ozkurt

| state | bout | duration_s | fP_hz | fA_hz | score | raw_mvl | ozkurt_mvl | preferred_phase_deg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run | 1 | 13.2408 | 7.5 | 92 | 0.10686 | 0.00856949 | 0.10686 | 4.63122 |
| run | 2 | 11.24 | 8.5 | 108 | 0.102014 | 0.00704858 | 0.102014 | -9.46638 |
| run | 3 | 10.5848 | 9 | 100 | 0.0870564 | 0.00666325 | 0.0870564 | 10.8733 |
| run | 4 | 9.9504 | 8.5 | 120 | 0.10145 | 0.00564987 | 0.10145 | -14.965 |
| run | 5 | 10.6864 | 7.5 | 100 | 0.10747 | 0.0085526 | 0.10747 | -24.255 |
| run | 6 | 10.7528 | 6.5 | 116 | 0.104096 | 0.00625766 | 0.104096 | -20.2109 |
| run | 7 | 9.3616 | 8.5 | 104 | 0.104449 | 0.00786584 | 0.104449 | -13.7154 |
| run | 8 | 9.2976 | 9 | 132 | 0.111322 | 0.00563427 | 0.111322 | 13.4614 |
| run | 9 | 9.4416 | 7 | 112 | 0.122263 | 0.00813424 | 0.122263 | -17.8868 |
| run | 10 | 8.1744 | 5.5 | 104 | 0.111459 | 0.00722795 | 0.111459 | -13.6505 |
| run | 11 | 10.3864 | 8.5 | 112 | 0.101021 | 0.00670102 | 0.101021 | 3.64757 |
| run | 12 | 10.9608 | 6.5 | 120 | 0.109573 | 0.00662051 | 0.109573 | -26.6259 |
| rest | 1 | 11.4744 | 7 | 112 | 0.10818 | 0.00596611 | 0.10818 | -22.6398 |
| rest | 2 | 15.5896 | 8 | 84 | 0.0684306 | 0.00496589 | 0.0684306 | 13.1972 |
| rest | 3 | 7.9816 | 4.5 | 96 | 0.0998695 | 0.00596919 | 0.0998695 | 22.9139 |
| rest | 4 | 10.8 | 4.5 | 92 | 0.090872 | 0.00588228 | 0.090872 | 0.155816 |
| rest | 5 | 13.2192 | 6.5 | 108 | 0.102383 | 0.00564673 | 0.102383 | -5.57472 |
| rest | 6 | 10.1136 | 4 | 132 | 0.102821 | 0.00395361 | 0.102821 | -80.7515 |
| rest | 7 | 6.1256 | 7 | 120 | 0.118132 | 0.00533367 | 0.118132 | 12.6398 |
| rest | 8 | 16.492 | 8.5 | 84 | 0.0747136 | 0.00584313 | 0.0747136 | 8.88095 |
| rest | 9 | 9.3056 | 5.5 | 144 | 0.0904121 | 0.00326974 | 0.0904121 | -5.80773 |
| rest | 10 | 11.556 | 8 | 112 | 0.0824185 | 0.00387661 | 0.0824185 | -12.9541 |
| rest | 11 | 7.0824 | 8 | 80 | 0.0898538 | 0.0075874 | 0.0898538 | -10.6191 |
| rest | 12 | 13.7256 | 5.5 | 92 | 0.0833254 | 0.00481112 | 0.0833254 | 1.66744 |


### KLMI

| state | bout | duration_s | fP_hz | fA_hz | score | raw_mvl | ozkurt_mvl | preferred_phase_deg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run | 1 | 13.2408 | 7.5 | 92 | 0.00559083 | 0.00856949 | 0.10686 | 4.63122 |
| run | 2 | 11.24 | 7.5 | 108 | 0.00498007 | 0.00683088 | 0.0988632 | -4.59183 |
| run | 3 | 10.5848 | 8 | 100 | 0.00341553 | 0.00634762 | 0.0829326 | 6.59567 |
| run | 4 | 9.9504 | 7 | 120 | 0.00495382 | 0.00530734 | 0.0952995 | -10.0884 |
| run | 5 | 10.6864 | 7.5 | 100 | 0.00478378 | 0.0085526 | 0.10747 | -24.255 |
| run | 6 | 10.7528 | 6.5 | 116 | 0.00464046 | 0.00625766 | 0.104096 | -20.2109 |
| run | 7 | 9.3616 | 8 | 104 | 0.00442685 | 0.00765729 | 0.101679 | -15.6493 |
| run | 8 | 9.2976 | 9 | 132 | 0.00554171 | 0.00563427 | 0.111322 | 13.4614 |
| run | 9 | 9.4416 | 6.5 | 112 | 0.0072201 | 0.0079688 | 0.119776 | -15.3406 |
| run | 10 | 8.1744 | 7 | 104 | 0.00580407 | 0.0068653 | 0.105866 | -9.33309 |
| run | 11 | 10.3864 | 8.5 | 112 | 0.0049573 | 0.00670102 | 0.101021 | 3.64757 |
| run | 12 | 10.9608 | 8 | 120 | 0.00596354 | 0.00650304 | 0.107628 | -23.4738 |
| rest | 1 | 11.4744 | 7 | 112 | 0.00575407 | 0.00596611 | 0.10818 | -22.6398 |
| rest | 2 | 15.5896 | 7 | 140 | 0.00212898 | 0.00205064 | 0.0589616 | 11.9338 |
| rest | 3 | 7.9816 | 6.5 | 128 | 0.00400284 | 0.00350306 | 0.0853381 | 24.8695 |
| rest | 4 | 10.8 | 6.5 | 116 | 0.0026174 | 0.00332395 | 0.072892 | 51.7954 |
| rest | 5 | 13.2192 | 6.5 | 108 | 0.0042888 | 0.00564673 | 0.102383 | -5.57472 |
| rest | 6 | 10.1136 | 4.5 | 128 | 0.00501221 | 0.00384974 | 0.0955385 | -92.7432 |
| rest | 7 | 6.1256 | 7 | 120 | 0.0066802 | 0.00533367 | 0.118132 | 12.6398 |
| rest | 8 | 16.492 | 7 | 80 | 0.00281352 | 0.00589057 | 0.070495 | 7.86861 |
| rest | 9 | 9.3056 | 7.5 | 104 | 0.004051 | 0.00438519 | 0.0798119 | 6.66751 |
| rest | 10 | 11.556 | 6.5 | 100 | 0.00296936 | 0.00398884 | 0.0746772 | -5.8951 |
| rest | 11 | 7.0824 | 8 | 80 | 0.0036885 | 0.0075874 | 0.0898538 | -10.6191 |
| rest | 12 | 13.7256 | 5.5 | 92 | 0.00375152 | 0.00481112 | 0.0833254 | 1.66744 |


### GLM

| state | bout | duration_s | fP_hz | fA_hz | score | raw_mvl | ozkurt_mvl | preferred_phase_deg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run | 1 | 13.2408 | 7 | 92 | 0.0881134 | 0.0082623 | 0.10303 | 6.09977 |
| run | 2 | 11.24 | 7.5 | 108 | 0.0864984 | 0.00683088 | 0.0988632 | -4.59183 |
| run | 3 | 10.5848 | 8 | 100 | 0.0593272 | 0.00634762 | 0.0829326 | 6.59567 |
| run | 4 | 9.9504 | 7 | 120 | 0.0752591 | 0.00530734 | 0.0952995 | -10.0884 |
| run | 5 | 10.6864 | 7.5 | 100 | 0.0836559 | 0.0085526 | 0.10747 | -24.255 |
| run | 6 | 10.7528 | 7.5 | 84 | 0.0858544 | 0.00830226 | 0.0979414 | -20.7326 |
| run | 7 | 9.3616 | 8.5 | 104 | 0.0852728 | 0.00786584 | 0.104449 | -13.7154 |
| run | 8 | 9.2976 | 9 | 132 | 0.0902518 | 0.00563427 | 0.111322 | 13.4614 |
| run | 9 | 9.4416 | 6.5 | 112 | 0.123162 | 0.0079688 | 0.119776 | -15.3406 |
| run | 10 | 8.1744 | 7 | 108 | 0.0909274 | 0.00659876 | 0.104281 | -13.017 |
| run | 11 | 10.3864 | 8.5 | 112 | 0.074323 | 0.00670102 | 0.101021 | 3.64757 |
| run | 12 | 10.9608 | 8 | 120 | 0.0947387 | 0.00650304 | 0.107628 | -23.4738 |
| rest | 1 | 11.4744 | 7 | 112 | 0.0841115 | 0.00596611 | 0.10818 | -22.6398 |
| rest | 2 | 15.5896 | 8 | 84 | 0.0347716 | 0.00496589 | 0.0684306 | 13.1972 |
| rest | 3 | 7.9816 | 7 | 128 | 0.06801 | 0.00376669 | 0.0917605 | 19.1396 |
| rest | 4 | 10.8 | 6.5 | 116 | 0.0446784 | 0.00332395 | 0.072892 | 51.7954 |
| rest | 5 | 13.2192 | 6.5 | 108 | 0.0686513 | 0.00564673 | 0.102383 | -5.57472 |
| rest | 6 | 10.1136 | 4.5 | 128 | 0.0662935 | 0.00384974 | 0.0955385 | -92.7432 |
| rest | 7 | 6.1256 | 7 | 120 | 0.109323 | 0.00533367 | 0.118132 | 12.6398 |
| rest | 8 | 16.492 | 7 | 80 | 0.0449558 | 0.00589057 | 0.070495 | 7.86861 |
| rest | 9 | 9.3056 | 6.5 | 96 | 0.0570508 | 0.0052123 | 0.0846615 | 5.21619 |
| rest | 10 | 11.556 | 6.5 | 100 | 0.052452 | 0.00398884 | 0.0746772 | -5.8951 |
| rest | 11 | 7.0824 | 8 | 80 | 0.0569881 | 0.0075874 | 0.0898538 | -10.6191 |
| rest | 12 | 13.7256 | 5.5 | 92 | 0.0500634 | 0.00481112 | 0.0833254 | 1.66744 |


## Run versus rest statistics

Effect direction is run minus rest. Primary estimates weight each bout equally. Welch t and its Satterthwaite df are two-sided; Hedges g uses the pooled within-state SD and the exact small-sample gamma correction. The percentile 95% CI uses 10,000 independent resamples of 12 bouts per state, seed 20261022, with the same resample indices for every method/metric. No multiple-comparison adjustment is applied.

The duration sensitivity normalizes durations within each state; weighted variance is sum[p(x−mean)²]/(1−sum[p²]), effective n is 1/sum[p²], and Welch t/df and pooled Hedges g use these weighted variances and effective sample sizes. This is a specified weighted approximation, not 24 independent session/animal measurements. Bootstrap resampling keeps each bout value and duration together and recomputes the weighted mean.

Full statistics: [rodent_run_rest_statistics.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/rodent_run_rest_statistics.csv>). State means, weighted means, durations and boundary counts: [rodent_state_summary.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/rodent_state_summary.csv>).

### Equal bout weighting

| method | metric | run_mean | rest_mean | mean_difference | welch_t | welch_df | p_two_sided | hedges_g | bootstrap_ci_low | bootstrap_ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APC v1.0 | fP_hz | 7.66634 | 6.99423 | 0.672106 | 3.79023 | 11.6782 | 0.00269822 | 1.4939 | 0.32831 | 0.988305 |
| APC v1.0 | fA_hz | 113.833 | 104.75 | 9.08333 | 1.62273 | 20.2797 | 0.120091 | 0.639589 | -1.41667 | 19.4167 |
| APC v1.0 | ozkurt_mvl | 0.0842208 | 0.0707225 | 0.0134982 | 2.1144 | 21.9543 | 0.0460709 | 0.833377 | 0.00112274 | 0.0251362 |
| MVL-raw | fP_hz | 7.70833 | 6.16667 | 1.54167 | 2.55934 | 15.968 | 0.0210261 | 1.00875 | 0.416667 | 2.66667 |
| MVL-raw | fA_hz | 94.6667 | 83.3333 | 11.3333 | 3.01809 | 14.3429 | 0.00900987 | 1.18956 | 4.33333 | 18.3333 |
| MVL-raw | ozkurt_mvl | 0.0977735 | 0.0788147 | 0.0189588 | 5.17804 | 21.9992 | 3.42727e-05 | 2.04089 | 0.0121317 | 0.0258081 |
| MVL-Ozkurt | fP_hz | 7.70833 | 6.41667 | 1.29167 | 2.2996 | 19.995 | 0.0323773 | 0.906371 | 0.25 | 2.33333 |
| MVL-Ozkurt | fA_hz | 110 | 104.667 | 5.33333 | 0.802191 | 16.9649 | 0.433537 | 0.316178 | -7.33333 | 17.6667 |
| MVL-Ozkurt | ozkurt_mvl | 0.105753 | 0.0926177 | 0.013135 | 2.74582 | 17.6808 | 0.0134423 | 1.08225 | 0.00410758 | 0.0222141 |
| KLMI | fP_hz | 7.58333 | 6.625 | 0.958333 | 2.79853 | 21.3755 | 0.0106508 | 1.10302 | 0.333333 | 1.625 |
| KLMI | fA_hz | 110 | 109 | 1 | 0.158294 | 17.6588 | 0.876021 | 0.0623905 | -10.6667 | 12.6667 |
| KLMI | ozkurt_mvl | 0.103568 | 0.0866324 | 0.0169354 | 3.03554 | 16.7022 | 0.00758147 | 1.19644 | 0.00618419 | 0.0274086 |
| GLM | fP_hz | 7.66667 | 6.66667 | 1 | 2.84282 | 20.7552 | 0.00981825 | 1.12048 | 0.375 | 1.66667 |
| GLM | fA_hz | 107.667 | 103.667 | 4 | 0.632615 | 20.2819 | 0.534053 | 0.249341 | -8 | 15.6667 |
| GLM | ozkurt_mvl | 0.102834 | 0.0883609 | 0.0144735 | 2.76106 | 17.5793 | 0.0130632 | 1.08826 | 0.00430336 | 0.024325 |


### Duration-weighted sensitivity

| method | metric | run_mean | rest_mean | mean_difference | welch_t | welch_df | p_two_sided | hedges_g | bootstrap_ci_low | bootstrap_ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APC v1.0 | fP_hz | 7.67493 | 7.07122 | 0.603709 | 3.20522 | 10.7228 | 0.0086379 | 1.32937 | 0.256502 | 0.963796 |
| APC v1.0 | fA_hz | 114.087 | 102.46 | 11.6274 | 2.01604 | 18.7287 | 0.0583705 | 0.818644 | 0.292093 | 21.6082 |
| APC v1.0 | ozkurt_mvl | 0.0840766 | 0.0687728 | 0.0153038 | 2.46999 | 20.9669 | 0.0221818 | 0.991521 | 0.00369062 | 0.0257799 |
| MVL-raw | fP_hz | 7.71383 | 6.23091 | 1.48292 | 2.3457 | 14.2315 | 0.0339767 | 0.963382 | 0.321736 | 2.68313 |
| MVL-raw | fA_hz | 94.9383 | 83.4123 | 11.5259 | 3.03294 | 14.5031 | 0.0086557 | 1.19256 | 4.41283 | 18.5632 |
| MVL-raw | ozkurt_mvl | 0.0979044 | 0.0773518 | 0.0205525 | 5.42415 | 20.8489 | 2.27178e-05 | 2.1833 | 0.0131573 | 0.0273721 |
| MVL-Ozkurt | fP_hz | 7.72549 | 6.5543 | 1.17119 | 2.04099 | 17.8372 | 0.0563338 | 0.830771 | 0.138315 | 2.26476 |
| MVL-Ozkurt | fA_hz | 109.509 | 102.657 | 6.85203 | 1.02029 | 15.8496 | 0.322915 | 0.41736 | -6.34994 | 18.5079 |
| MVL-Ozkurt | ozkurt_mvl | 0.105489 | 0.0899828 | 0.0155062 | 3.12986 | 15.818 | 0.00653434 | 1.28041 | 0.00574109 | 0.0245854 |
| KLMI | fP_hz | 7.58486 | 6.58105 | 1.00381 | 2.97272 | 20.0522 | 0.00750906 | 1.20192 | 0.416075 | 1.62563 |
| KLMI | fA_hz | 109.509 | 108.429 | 1.08042 | 0.159532 | 15.7439 | 0.875278 | 0.0652754 | -12.0517 | 13.9198 |
| KLMI | ozkurt_mvl | 0.10342 | 0.0840703 | 0.0193499 | 3.37827 | 15.1308 | 0.00409515 | 1.38436 | 0.00801429 | 0.0296623 |
| GLM | fP_hz | 7.65589 | 6.65803 | 0.99786 | 2.78944 | 18.8783 | 0.0117376 | 1.13221 | 0.35759 | 1.6759 |
| GLM | fA_hz | 106.999 | 101.33 | 5.66969 | 0.881988 | 18.9493 | 0.388835 | 0.357917 | -6.71566 | 17.0222 |
| GLM | ozkurt_mvl | 0.102583 | 0.0858986 | 0.016684 | 3.13861 | 16.0465 | 0.00632725 | 1.28327 | 0.00613523 | 0.0260583 |


### State summaries and boundary picks

| method | state | n_bouts | duration_total_s | fP_mean | fA_mean | ozkurt_mean | fP_weighted | fA_weighted | ozkurt_weighted | boundary_4 | boundary_12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APC v1.0 | run | 12 | 124.078 | 7.66634 | 113.833 | 0.0842208 | 7.67493 | 114.087 | 0.0840766 | 0 | 0 |
| APC v1.0 | rest | 12 | 133.466 | 6.99423 | 104.75 | 0.0707225 | 7.07122 | 102.46 | 0.0687728 | 0 | 0 |
| MVL-raw | run | 12 | 124.078 | 7.70833 | 94.6667 | 0.0977735 | 7.71383 | 94.9383 | 0.0979044 | 0 | 0 |
| MVL-raw | rest | 12 | 133.466 | 6.16667 | 83.3333 | 0.0788147 | 6.23091 | 83.4123 | 0.0773518 | 3 | 0 |
| MVL-Ozkurt | run | 12 | 124.078 | 7.70833 | 110 | 0.105753 | 7.72549 | 109.509 | 0.105489 | 0 | 0 |
| MVL-Ozkurt | rest | 12 | 133.466 | 6.41667 | 104.667 | 0.0926177 | 6.5543 | 102.657 | 0.0899828 | 1 | 0 |
| KLMI | run | 12 | 124.078 | 7.58333 | 110 | 0.103568 | 7.58486 | 109.509 | 0.10342 | 0 | 0 |
| KLMI | rest | 12 | 133.466 | 6.625 | 109 | 0.0866324 | 6.58105 | 108.429 | 0.0840703 | 0 | 0 |
| GLM | run | 12 | 124.078 | 7.66667 | 107.667 | 0.102834 | 7.65589 | 106.999 | 0.102583 | 0 | 0 |
| GLM | rest | 12 | 133.466 | 6.66667 | 103.667 | 0.0883609 | 6.65803 | 101.33 | 0.0858986 | 0 | 0 |


APC has no 4–12 Hz search constraint; its boundary counts here simply count exact fP=4 or fP=12 outputs, as requested. Comparator boundary counts refer to the actual rodent scan endpoints.

### Optional additional sessions

Eight other EC013 sessions are present locally (156, 205, 206, 208, 251, 252, 374, 375), but none has saved run/rest trial files in the inspected Brainstorm session folders. Only the 157 session has the existing behavior split. No other session with documented ≥8 run and ≥8 rest bouts of ≥5 s was established locally; optional replication was not run. No additional session data were downloaded.

## Canonical examples

The 20-s 8/120-Hz burst-coupled, jittered and continuous examples were regenerated using the existing Python generator and original PCG64 seed/order 12345; each matches its historical signal CSV to 1e-14. Parameters: fs=500 Hz, burst sigma=30 ms, burst amplitude=1.8, baseline HF amplitude=.15, low amplitude=1, white-noise SD=.8. These are the canonical example settings, not the held-out generator settings. The jittered call explicitly uses SD=0.020 s.

The timing null replaces only the coupled burst component with bursts from a homogeneous Poisson process of rate 8/s on (0.5,19.5) s; separate seed 20261022 produced 174 events. The low rhythm, baseline HF and noise samples remain identical to the paired coupled example. Overlapping bursts are allowed. The old canonical null used a fixed event count and uniform times; that old null was not relabeled as Poisson. The workflow and condition panels use regenerated frozen-v1 outputs throughout.

| state | fP_hz | fA_hz | raw_mvl | ozkurt_mvl | preferred_phase_deg |
| --- | --- | --- | --- | --- | --- |
| burst_coupled | 7.99792 | 122 | 0.176908 | 0.178968 | 178.576 |
| timing_null | 7.99607 | 81 | 0.0021562 | 0.011202 | -134.062 |
| jittered | 7.99481 | 125 | 0.112645 | 0.120594 | 179.3 |
| continuous_pac | 8.00091 | 150 | 0.00208632 | 0.0107487 | -21.3448 |

Generator settings, seeds and source hash: [canonical_provenance.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/canonical_provenance.json>). Outputs: [canonical_results_export_corrected.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/canonical_results_export_corrected.csv>).

## Figures

All figures are exported as PNG at 300 dpi and SVG. The embedded Description metadata includes the method commit, source CSV paths and SHA-256 hashes, full analysis settings and seeds. Each figure lists its source CSV filenames visibly. Wilson intervals use z=1.9599639845 and n=25; invalid held-out estimates count as recovery failures. AUCs are taken unchanged from the saved coupled-versus-timing-null score table.

- **Figure_1_workflow**: Figure 1. APC v1.0 canonical workflow. [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Figure_1_workflow.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Figure_1_workflow.svg>). Sources: [canonical_results_export_corrected.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/canonical_results_export_corrected.csv>), [burst_coupled_traces.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/burst_coupled_traces.csv>), [burst_coupled_spectrum.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/burst_coupled_spectrum.csv>), [burst_coupled_fa_score.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/burst_coupled_fa_score.csv>), [burst_coupled_tf.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/burst_coupled_tf.csv>).
- **Figure_2_canonical_conditions**: Figure 2. Four canonical conditions analyzed with frozen APC v1.0. [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Figure_2_canonical_conditions.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Figure_2_canonical_conditions.svg>). Sources: [canonical_results_export_corrected.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/canonical_results_export_corrected.csv>), [burst_coupled_traces.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/burst_coupled_traces.csv>), [timing_null_traces.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/timing_null_traces.csv>), [jittered_traces.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/jittered_traces.csv>), [continuous_pac_traces.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/continuous_pac_traces.csv>).
- **Figure_3_H1_recovery**: Figure 3. Held-out H1 recovery: APC v1.0 and A2′. [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Figure_3_H1_recovery.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Figure_3_H1_recovery.svg>). Sources: [heldout_v1_A2_recovery.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/heldout_v1_A2_recovery.csv>).
- **Figure_4_H2_recovery**: Figure 4. Held-out H2 recovery and distractor-frequency picks. [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Figure_4_H2_recovery.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Figure_4_H2_recovery.svg>). Sources: [heldout_v1_A2_recovery.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/heldout_v1_A2_recovery.csv>).
- **Figure_5_null_specificity**: Figure 5. Timing-null false recovery and score AUC. [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Figure_5_null_specificity.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Figure_5_null_specificity.svg>). Sources: [heldout_v1_A2_timing_null_auc.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/heldout_v1_A2_timing_null_auc.csv>).
- **Supplement_S1_development_main**: Development suite: main, comparator fP step 1 Hz. [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Supplement_S1_development_main.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Supplement_S1_development_main.svg>). Sources: [Supplement_S1_development_main_source.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Supplement_S1_development_main_source.csv>).
- **Supplement_S2_development_random_1Hz**: Development suite: random fp, comparator fP step 1 Hz. [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Supplement_S2_development_random_1Hz.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Supplement_S2_development_random_1Hz.svg>). Sources: [Supplement_S2_development_random_1Hz_source.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Supplement_S2_development_random_1Hz_source.csv>).
- **Supplement_S3_development_random_05Hz**: Development suite: random fp, comparator fP step 0.5 Hz. [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Supplement_S3_development_random_05Hz.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Supplement_S3_development_random_05Hz.svg>). Sources: [Supplement_S3_development_random_05Hz_source.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Supplement_S3_development_random_05Hz_source.csv>).
- **Supplement_S4_v2_negative**: APC v2.0 held-out recovery — negative result. [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Supplement_S4_v2_negative.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/final/Supplement_S4_v2_negative.svg>). Sources: [heldout_v2_negative_recovery.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/final/heldout_v2_negative_recovery.csv>).

Source manifest: [figure_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/figure_manifest.json>). Held-out source evaluation commit is `217fd8373759150cdeffe794d231a7cec2225f38`; the v1 path was previously checked against v1.0. No held-out simulation was regenerated for Figures 3–5 or the v2 negative-result supplement. Development results remain explicitly labeled development.

## Runtime, deviations and verification

Elapsed compute seconds by stage/worker (three workers overlap in wall time):

| stage | elapsed_seconds |
| --- | --- |
| sos_audit_worker1_runtime.json | 15.41201 |
| sos_development_worker1_runtime.json | 210.3525 |
| sos_development_worker2_runtime.json | 191.3784 |
| sos_development_worker3_runtime.json | 206.94425 |
| sos_heldout_worker1_runtime.json | 222.59348 |
| sos_heldout_worker2_runtime.json | 207.64458 |
| sos_heldout_worker3_runtime.json | 209.15906 |
| sos_rodent_worker1_runtime.json | 15.983606 |

Figure/statistics build elapsed seconds: 11.718540400004713. Startup, inspection and final integrity-check time are excluded. The earlier canonical-only stage took 27.2666999 seconds.

The original direct-form failure is superseded by the authorized numerical correction. All newly used SOS designs passed their guards; no tagged APC method change or new candidate was made. Original simulation inputs and original historical outputs remain unchanged. Full earlier and resumed tooling/deviation records: [deviations.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/deviations.json>).

Additional metadata limits remain: E1/row 1 is documented, but shank/layer/acquisition-index mapping is unavailable locally; no other session with eligible documented run/rest bouts was established. Optional replication was not run.

Verification: [verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/verification.json>). Complete final output hashes: [output_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/output_manifest.json>). The root STOPPED.json is the preserved historical stop record; the current status is [RESUME_STATUS.json](<C:/Users/nghare/.brainstorm/process/revision_checks/final/RESUME_STATUS.json>).
