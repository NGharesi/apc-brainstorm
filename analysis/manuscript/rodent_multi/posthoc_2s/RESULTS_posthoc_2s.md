# POST HOC sensitivity — 2-s minimum bout duration

**POST HOC analysis.** Minimum contiguous same-state bout duration is 2 s. Inclusion remains >=5 run and >=5 rest bouts. All other rules, source inputs, regional channels, frozen APC v1.0 options, SOS comparator settings, statistical estimators and seed scheme are unchanged. The prespecified 5-s analysis is retained separately.

## POST HOC scope and provenance

The POST HOC protocol was saved before new bout extraction: [PROTOCOL_posthoc_2s.md](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/PROTOCOL_posthoc_2s.md>). Frozen method commit `71ebc16aed32ca38be73a800738b975e5806b330`; seed 20261022. Full POST HOC provenance: [posthoc_2s_provenance.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_provenance.json>). All parent numerical results, method code, tracking traces and figures are checked against the prespecified manifest: [posthoc_2s_prespecified_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_prespecified_manifest.json>).

The identical saved tracking time, position, LED validity, short-gap interpolation, PCA projection/scale, Gaussian smoothing, 2-D speed and strict run/rest masks were reused. Only the duration cutoff changed. All 202 bouts in the original all-session 5-s extraction retained identical tracking/LFP boundaries. All method outputs, including shared >=5-s inputs, were recomputed. The 1,680 method rows shared with the prespecified analysis match exactly: [posthoc_2s_shared_5s_exact_comparison.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_shared_5s_exact_comparison.csv>).

## POST HOC inclusion beside prespecified 5-s results

POST HOC: all 18 sessions qualify (9 EC013 and 9 EC012). CA1 uses 9 EC013 sessions; EC uses all 18; E1 sensitivity uses 9 EC013. Prespecified 5-s: 3 EC013 sessions qualify in each analysis, with no EC012 sessions. Different eligible-session sets are therefore used in the side-by-side pooled summaries.

POST HOC table — duration/inclusion comparison:
| animal | session | run_bouts_prespecified_5s | rest_bouts_prespecified_5s | included_prespecified_5s | run_bouts_posthoc_2s | rest_bouts_posthoc_2s | included_posthoc_2s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EC013 | ec013.156 | 9 | 43 | True | 56 | 56 | True |
| EC013 | ec013.157 | 6 | 15 | True | 23 | 33 | True |
| EC013 | ec013.205 | 0 | 4 | False | 8 | 9 | True |
| EC013 | ec013.206 | 3 | 21 | False | 58 | 61 | True |
| EC013 | ec013.208 | 0 | 10 | False | 44 | 53 | True |
| EC013 | ec013.251 | 0 | 12 | False | 54 | 65 | True |
| EC013 | ec013.252 | 1 | 9 | False | 32 | 64 | True |
| EC013 | ec013.374 | 4 | 8 | False | 88 | 77 | True |
| EC013 | ec013.375 | 5 | 34 | True | 68 | 137 | True |
| EC012 | ec012ec.239 | 0 | 0 | False | 47 | 34 | True |
| EC012 | ec012ec.240 | 0 | 1 | False | 66 | 17 | True |
| EC012 | ec012ec.269 | 0 | 1 | False | 38 | 48 | True |
| EC012 | ec012ec.270 | 0 | 1 | False | 24 | 49 | True |
| EC012 | ec012ec.271 | 0 | 2 | False | 35 | 21 | True |
| EC012 | ec012ec.356 | 0 | 5 | False | 40 | 50 | True |
| EC012 | ec012ec.357 | 0 | 1 | False | 38 | 36 | True |
| EC012 | ec012ec.375 | 0 | 6 | False | 37 | 32 | True |
| EC012 | ec012ec.444 | 0 | 1 | False | 30 | 46 | True |

POST HOC table — regional channel choices (unchanged from prespecified regional choices):
| animal | session | analysis | channel_name | shank | region | theta_delta_ratio | source_channel_flag | included |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EC013 | ec013.156 | EC | E8 | 1 | EC3 | 5.88298 | 1 | True |
| EC013 | ec013.156 | CA1 | E38 | 5 | CA1 | 4.55845 | -1 | True |
| EC013 | ec013.156 | E1_sensitivity | E1 | 1 | EC3 | 5.13478 | 1 | True |
| EC013 | ec013.157 | EC | E8 | 1 | EC3 | 5.73648 | 1 | True |
| EC013 | ec013.157 | CA1 | E40 | 5 | CA1 | 4.2026 | -1 | True |
| EC013 | ec013.157 | E1_sensitivity | E1 | 1 | EC3 | 4.98602 | 1 | True |
| EC013 | ec013.205 | EC | E2 | 1 | EC3 | 9.89115 | 1 | True |
| EC013 | ec013.205 | CA1 | E38 | 5 | CA1 | 7.86491 | -1 | True |
| EC013 | ec013.205 | E1_sensitivity | E1 | 1 | EC3 | 7.72998 | 1 | True |
| EC013 | ec013.206 | EC | E2 | 1 | EC3 | 5.25741 | 1 | True |
| EC013 | ec013.206 | CA1 | E40 | 5 | CA1 | 3.93556 | -1 | True |
| EC013 | ec013.206 | E1_sensitivity | E1 | 1 | EC3 | 4.76935 | 1 | True |
| EC013 | ec013.208 | EC | E2 | 1 | EC3 | 1.00401 | 1 | True |
| EC013 | ec013.208 | CA1 | E62 | 8 | CA1 | 1.12058 | -1 | True |
| EC013 | ec013.208 | E1_sensitivity | E1 | 1 | EC3 | 0.960782 | 1 | True |
| EC013 | ec013.251 | EC | E2 | 1 | EC3 | 2.83277 | 1 | True |
| EC013 | ec013.251 | CA1 | E38 | 5 | CA1 | 2.40877 | -1 | True |
| EC013 | ec013.251 | E1_sensitivity | E1 | 1 | EC3 | 2.73322 | 1 | True |
| EC013 | ec013.252 | EC | E2 | 1 | EC3 | 2.90608 | 1 | True |
| EC013 | ec013.252 | CA1 | E38 | 5 | CA1 | 2.54325 | -1 | True |
| EC013 | ec013.252 | E1_sensitivity | E1 | 1 | EC3 | 2.79305 | 1 | True |
| EC013 | ec013.374 | EC | E8 | 1 | EC3 | 3.24252 | 1 | True |
| EC013 | ec013.374 | CA1 | E38 | 5 | CA1 | 2.57399 | -1 | True |
| EC013 | ec013.374 | E1_sensitivity | E1 | 1 | EC3 | 2.7809 | 1 | True |
| EC013 | ec013.375 | EC | E8 | 1 | EC3 | 1.38052 | 1 | True |
| EC013 | ec013.375 | CA1 | E62 | 8 | CA1 | 1.14409 | -1 | True |
| EC013 | ec013.375 | E1_sensitivity | E1 | 1 | EC3 | 1.20008 | 1 | True |
| EC012 | ec012ec.239 | EC | E5 | 1 | EC3 | 7.17818 | 1 | True |
| EC012 | ec012ec.240 | EC | E3 | 1 | EC3 | 7.67862 | 1 | True |
| EC012 | ec012ec.269 | EC | E5 | 1 | EC3 | 4.80764 | 1 | True |
| EC012 | ec012ec.270 | EC | E12 | 2 | EC3 | 5.90819 | 1 | True |
| EC012 | ec012ec.271 | EC | E10 | 2 | EC3 | 7.16646 | 1 | True |
| EC012 | ec012ec.356 | EC | E6 | 1 | EC3 | 5.96633 | 1 | True |
| EC012 | ec012ec.357 | EC | E9 | 2 | EC3 | 7.37768 | 1 | True |
| EC012 | ec012ec.375 | EC | E6 | 1 | EC3 | 7.39874 | 1 | True |
| EC012 | ec012ec.444 | EC | E6 | 1 | EC3 | 7.55065 | 1 | True |

POST HOC table — behaviour summaries and durations:
| session | cm_per_unit | raw_missing_fraction | missing_after_short_interpolation_fraction | run_bouts | rest_bouts | run_total_duration_s | run_mean_duration_s | run_median_duration_s | rest_total_duration_s | rest_mean_duration_s | rest_median_duration_s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ec013.156 | 0.892045 | 0.018557 | 0.018557 | 56 | 56 | 216.474 | 3.8656 | 3.84 | 361.472 | 6.45486 | 6.464 |
| ec013.157 | 0.900057 | 0.0314312 | 0.0314312 | 23 | 33 | 87.1424 | 3.7888 | 3.8656 | 180.659 | 5.47452 | 4.2752 |
| ec013.205 | 0.902 | 0.142311 | 0.142311 | 8 | 9 | 28.9024 | 3.6128 | 3.8912 | 43.1872 | 4.79858 | 4.7104 |
| ec013.206 | 0.909338 | 0.0132916 | 0.0132916 | 58 | 61 | 216.986 | 3.74113 | 3.7248 | 281.984 | 4.62269 | 4.3776 |
| ec013.208 | 0.927246 | 0.013618 | 0.013618 | 44 | 53 | 155.238 | 3.52815 | 3.5968 | 195.405 | 3.68688 | 3.3536 |
| ec013.251 | 0.889563 | 0.0421991 | 0.0421991 | 54 | 65 | 164.224 | 3.04119 | 3.0464 | 252.8 | 3.88923 | 3.84 |
| ec013.252 | 0.905386 | 0.014435 | 0.014435 | 32 | 64 | 97.152 | 3.036 | 2.9696 | 240.512 | 3.758 | 3.0848 |
| ec013.374 | 0.892117 | 0.016124 | 0.016124 | 88 | 77 | 312.192 | 3.54764 | 3.5712 | 316.646 | 4.11229 | 3.7376 |
| ec013.375 | 0.894901 | 0.00820209 | 0.00820209 | 68 | 137 | 236.134 | 3.47256 | 3.392 | 620.314 | 4.52784 | 3.584 |
| ec012ec.239 | 0.924512 | 0.059047 | 0.059047 | 47 | 34 | 125.798 | 2.67656 | 2.4832 | 89.6 | 2.63529 | 2.5088 |
| ec012ec.240 | 0.943127 | 0.0526443 | 0.0526443 | 66 | 17 | 177.894 | 2.69537 | 2.3936 | 43.3664 | 2.55096 | 2.2528 |
| ec012ec.269 | 0.934115 | 0.0945966 | 0.0945966 | 38 | 48 | 98.8928 | 2.60244 | 2.1888 | 171.878 | 3.5808 | 3.4944 |
| ec012ec.270 | 0.946639 | 0.07381 | 0.07381 | 24 | 49 | 61.184 | 2.54933 | 2.304 | 140.774 | 2.87295 | 2.7392 |
| ec012ec.271 | 0.918263 | 0.0826614 | 0.0826614 | 35 | 21 | 98.6624 | 2.81893 | 2.7136 | 76.1088 | 3.62423 | 2.8416 |
| ec012ec.356 | 0.923684 | 0.0648874 | 0.0648874 | 40 | 50 | 99.7376 | 2.49344 | 2.368 | 159.59 | 3.19181 | 2.752 |
| ec012ec.357 | 0.899661 | 0.0582348 | 0.0582348 | 38 | 36 | 92.3136 | 2.42931 | 2.304 | 87.8336 | 2.43982 | 2.2528 |
| ec012ec.375 | 0.923188 | 0.0577118 | 0.0577118 | 37 | 32 | 92.4928 | 2.49981 | 2.2528 | 111.411 | 3.4816 | 2.5344 |
| ec012ec.444 | 0.919307 | 0.0432869 | 0.0432869 | 30 | 46 | 71.552 | 2.38507 | 2.2272 | 122.701 | 2.66741 | 2.5344 |

Every POST HOC bout duration, tracking/LFP boundary and source trace hash is in [posthoc_2s_bouts.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_bouts.csv>). Complete POST HOC behaviour summaries include min/max durations: [posthoc_2s_behavior_summary.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_behavior_summary.csv>).

## POST HOC APC summaries beside prespecified 5-s summaries

POST HOC comparison table — session-level mean run-minus-rest differences. CIs are t intervals across sessions. Counts refer to finite session differences for each outcome; session sets differ between analyses. The complete comparison includes every comparator, outcome and animal pool: [posthoc_2s_across_session_comparison.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_across_session_comparison.csv>).

| analysis | outcome | n_sessions_prespecified_5s | mean_session_difference_prespecified_5s | ci_low_prespecified_5s | ci_high_prespecified_5s | n_sessions_posthoc_2s | mean_session_difference_posthoc_2s | ci_low_posthoc_2s | ci_high_posthoc_2s | one_sample_p_posthoc_2s | wilcoxon_p_posthoc_2s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | fA_hz | 3 | -0.354978 | -7.8002 | 7.09025 | 9 | -0.640901 | -3.69711 | 2.41531 | 0.641643 | 0.734375 |
| CA1 | fP_hz | 3 | 0.705852 | -2.03297 | 3.44467 | 9 | 0.990233 | 0.473246 | 1.50722 | 0.00223572 | 0.0078125 |
| CA1 | ozkurt_mvl | 3 | 0.0151827 | -0.00486253 | 0.035228 | 9 | 0.00360524 | -0.00400565 | 0.0112161 | 0.306483 | 0.300781 |
| E1_sensitivity | fA_hz | 3 | -0.13082 | -32.5385 | 32.2769 | 9 | -0.500095 | -2.58858 | 1.58839 | 0.59591 | 0.652344 |
| E1_sensitivity | fP_hz | 3 | 1.17905 | 0.95638 | 1.40172 | 9 | 1.16168 | 1.03296 | 1.2904 | 2.97972e-08 | 0.00390625 |
| E1_sensitivity | ozkurt_mvl | 3 | 0.0392822 | 0.00949425 | 0.0690702 | 9 | 0.0317641 | 0.0277535 | 0.0357747 | 8.30787e-08 | 0.00390625 |
| EC | fA_hz | 3 | -1.81618 | -25.2157 | 21.5834 | 18 | -2.08733 | -4.81933 | 0.64467 | 0.125379 | 0.28373 |
| EC | fP_hz | 3 | 1.17684 | 0.814791 | 1.53889 | 18 | 1.85503 | 1.45416 | 2.25589 | 2.19699e-08 | 7.62939e-06 |
| EC | ozkurt_mvl | 3 | 0.0279788 | 0.00621326 | 0.0497443 | 18 | 0.0209182 | 0.0146053 | 0.0272311 | 2.1738e-06 | 7.62939e-06 |

POST HOC comparisons for the three sessions also eligible at 5 s, for every method/outcome: [posthoc_2s_shared_session_comparison.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_shared_session_comparison.csv>). These retain the original 5-s estimates beside the POST HOC 2-s estimates without restricting the full POST HOC analysis.

## POST HOC per-bout outputs and statuses

POST HOC: 3646 channel/bout inputs and 18230 method rows. Frozen APC v1.0 uses amplitude 80–150 Hz and all other defaults. A2' uses phase 4:0.5:12 Hz, half-width 1.5; amplitude 80:4:148 Hz, half-width 12; MVL-raw, MVL-Ozkurt, KLMI and GLM. SOS filter pole/gain guards and the raw-MVL/preferred-phase extraction checks are unchanged.

POST HOC per-bout fP/fA, raw/Ozkurt MVL, preferred phase, status, route and complete settings: [posthoc_2s_bout_estimates.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_bout_estimates.csv>). Nonzero frozen APC statuses are retained; finite-value denominators are reported. POST HOC status table:
| analysis | animal | method | state | status | bouts |
| --- | --- | --- | --- | --- | --- |
| CA1 | EC013 | APC-v1.0 | rest | 0 | 517 |
| CA1 | EC013 | APC-v1.0 | rest | 4 | 38 |
| CA1 | EC013 | APC-v1.0 | run | 0 | 423 |
| CA1 | EC013 | APC-v1.0 | run | 4 | 8 |
| CA1 | EC013 | GLM | rest | 0 | 555 |
| CA1 | EC013 | GLM | run | 0 | 431 |
| CA1 | EC013 | KLMI | rest | 0 | 555 |
| CA1 | EC013 | KLMI | run | 0 | 431 |
| CA1 | EC013 | MVL-Ozkurt | rest | 0 | 555 |
| CA1 | EC013 | MVL-Ozkurt | run | 0 | 431 |
| CA1 | EC013 | MVL-raw | rest | 0 | 555 |
| CA1 | EC013 | MVL-raw | run | 0 | 431 |
| E1_sensitivity | EC013 | APC-v1.0 | rest | 0 | 535 |
| E1_sensitivity | EC013 | APC-v1.0 | rest | 4 | 20 |
| E1_sensitivity | EC013 | APC-v1.0 | run | 0 | 431 |
| E1_sensitivity | EC013 | GLM | rest | 0 | 555 |
| E1_sensitivity | EC013 | GLM | run | 0 | 431 |
| E1_sensitivity | EC013 | KLMI | rest | 0 | 555 |
| E1_sensitivity | EC013 | KLMI | run | 0 | 431 |
| E1_sensitivity | EC013 | MVL-Ozkurt | rest | 0 | 555 |
| E1_sensitivity | EC013 | MVL-Ozkurt | run | 0 | 431 |
| E1_sensitivity | EC013 | MVL-raw | rest | 0 | 555 |
| E1_sensitivity | EC013 | MVL-raw | run | 0 | 431 |
| EC | EC012 | APC-v1.0 | rest | 0 | 300 |
| EC | EC012 | APC-v1.0 | rest | 4 | 33 |
| EC | EC012 | APC-v1.0 | run | 0 | 355 |
| EC | EC012 | GLM | rest | 0 | 333 |
| EC | EC012 | GLM | run | 0 | 355 |
| EC | EC012 | KLMI | rest | 0 | 333 |
| EC | EC012 | KLMI | run | 0 | 355 |
| EC | EC012 | MVL-Ozkurt | rest | 0 | 333 |
| EC | EC012 | MVL-Ozkurt | run | 0 | 355 |
| EC | EC012 | MVL-raw | rest | 0 | 333 |
| EC | EC012 | MVL-raw | run | 0 | 355 |
| EC | EC013 | APC-v1.0 | rest | 0 | 533 |
| EC | EC013 | APC-v1.0 | rest | 4 | 22 |
| EC | EC013 | APC-v1.0 | run | 0 | 431 |
| EC | EC013 | GLM | rest | 0 | 555 |
| EC | EC013 | GLM | run | 0 | 431 |
| EC | EC013 | KLMI | rest | 0 | 555 |
| EC | EC013 | KLMI | run | 0 | 431 |
| EC | EC013 | MVL-Ozkurt | rest | 0 | 555 |
| EC | EC013 | MVL-Ozkurt | run | 0 | 431 |
| EC | EC013 | MVL-raw | rest | 0 | 555 |
| EC | EC013 | MVL-raw | run | 0 | 431 |

## POST HOC per-session and across-session statistics

POST HOC estimators are identical: run-minus-rest means, unequal-variance Welch t, pooled-SD Hedges g with exact gamma correction, 10,000 percentile-bootstrap resamples with seed 20261022 and the same deterministic group stream scheme; session-level one-sample t and Wilcoxon signed rank, zero differences recorded, no multiplicity correction. Shared bout-index draws across methods within each analysis/session are retained. Bootstrap finite-resample counts and all test outputs are in the POST HOC CSVs.

### POST HOC CA1 statistics

POST HOC per-session table:
| animal | session | method | outcome | n_run | n_rest | run_mean | rest_mean | mean_difference | welch_t | welch_p | hedges_g | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EC013 | ec013.156 | APC-v1.0 | fP_hz | 56 | 54 | 7.49173 | 6.36891 | 1.12282 | 9.15846 | 3.81932e-13 | 1.76129 | 0.880403 | 1.36336 |
| EC013 | ec013.156 | APC-v1.0 | fA_hz | 56 | 54 | 111.304 | 117.907 | -6.60384 | -1.95897 | 0.0527211 | -0.371473 | -13.1027 | -0.0825081 |
| EC013 | ec013.156 | APC-v1.0 | ozkurt_mvl | 56 | 54 | 0.0707928 | 0.051581 | 0.0192118 | 3.64044 | 0.000426603 | 0.691629 | 0.00895873 | 0.0293029 |
| EC013 | ec013.156 | GLM | fP_hz | 56 | 56 | 6.48214 | 6.5 | -0.0178571 | -0.039375 | 0.968664 | -0.0073903 | -0.883929 | 0.848214 |
| EC013 | ec013.156 | GLM | fA_hz | 56 | 56 | 105 | 112.929 | -7.92857 | -2.10905 | 0.0372941 | -0.395849 | -15.2875 | -0.5 |
| EC013 | ec013.156 | GLM | ozkurt_mvl | 56 | 56 | 0.103214 | 0.0807542 | 0.0224597 | 3.73727 | 0.000298121 | 0.70145 | 0.0104287 | 0.0339253 |
| EC013 | ec013.156 | KLMI | fP_hz | 56 | 56 | 4.51786 | 4.78571 | -0.267857 | -1.21615 | 0.2266 | -0.22826 | -0.6875 | 0.152009 |
| EC013 | ec013.156 | KLMI | fA_hz | 56 | 56 | 107.5 | 111.429 | -3.92857 | -1.01304 | 0.313264 | -0.190138 | -11.4286 | 3.64286 |
| EC013 | ec013.156 | KLMI | ozkurt_mvl | 56 | 56 | 0.101161 | 0.0749952 | 0.0261659 | 3.46091 | 0.000782988 | 0.649579 | 0.0114333 | 0.0408758 |
| EC013 | ec013.156 | MVL-Ozkurt | fP_hz | 56 | 56 | 5.3125 | 5.72321 | -0.410714 | -1.0081 | 0.315694 | -0.18921 | -1.21429 | 0.383929 |
| EC013 | ec013.156 | MVL-Ozkurt | fA_hz | 56 | 56 | 110.714 | 115 | -4.28571 | -0.997043 | 0.320999 | -0.187135 | -12.7857 | 4.07143 |
| EC013 | ec013.156 | MVL-Ozkurt | ozkurt_mvl | 56 | 56 | 0.134041 | 0.098434 | 0.035607 | 4.68271 | 8.28982e-06 | 0.878899 | 0.020923 | 0.0502646 |
| EC013 | ec013.156 | MVL-raw | fP_hz | 56 | 56 | 5.72321 | 5.55357 | 0.169643 | 0.417591 | 0.677068 | 0.0783778 | -0.625 | 0.964286 |
| EC013 | ec013.156 | MVL-raw | fA_hz | 56 | 56 | 84.6429 | 86.3571 | -1.71429 | -0.94979 | 0.344377 | -0.178266 | -5.07143 | 1.92857 |
| EC013 | ec013.156 | MVL-raw | ozkurt_mvl | 56 | 56 | 0.116249 | 0.0837023 | 0.0325471 | 4.47893 | 1.93973e-05 | 0.840651 | 0.0186391 | 0.046794 |
| EC013 | ec013.157 | APC-v1.0 | fP_hz | 23 | 31 | 7.55384 | 5.9778 | 1.57604 | 8.34812 | 7.62719e-10 | 1.98126 | 1.22549 | 1.97312 |
| EC013 | ec013.157 | APC-v1.0 | fA_hz | 23 | 31 | 119.261 | 114.968 | 4.29313 | 0.729698 | 0.468918 | 0.193222 | -6.81258 | 15.5218 |
| EC013 | ec013.157 | APC-v1.0 | ozkurt_mvl | 23 | 31 | 0.0656588 | 0.0631246 | 0.00253418 | 0.383725 | 0.702811 | 0.0968168 | -0.0104391 | 0.0149411 |
| EC013 | ec013.157 | GLM | fP_hz | 23 | 33 | 6.47826 | 6.54545 | -0.0671937 | -0.0979036 | 0.92247 | -0.0269895 | -1.38803 | 1.26683 |
| EC013 | ec013.157 | GLM | fA_hz | 23 | 33 | 108.696 | 113.212 | -4.51647 | -0.733668 | 0.466679 | -0.195224 | -16.5062 | 7.68906 |
| EC013 | ec013.157 | GLM | ozkurt_mvl | 23 | 33 | 0.103913 | 0.0904222 | 0.0134906 | 1.45578 | 0.15356 | 0.41045 | -0.00372351 | 0.0311231 |
| EC013 | ec013.157 | KLMI | fP_hz | 23 | 33 | 4.56522 | 4.98485 | -0.419631 | -1.20748 | 0.232592 | -0.309693 | -1.06787 | 0.273386 |
| EC013 | ec013.157 | KLMI | fA_hz | 23 | 33 | 106.957 | 115.515 | -8.55863 | -1.34821 | 0.184149 | -0.363616 | -20.527 | 4.1112 |
| EC013 | ec013.157 | KLMI | ozkurt_mvl | 23 | 33 | 0.0855735 | 0.0841778 | 0.00139565 | 0.132161 | 0.895509 | 0.0368114 | -0.0183536 | 0.0215296 |
| EC013 | ec013.157 | MVL-Ozkurt | fP_hz | 23 | 33 | 5.17391 | 5.62121 | -0.447299 | -0.910485 | 0.367157 | -0.243738 | -1.34124 | 0.528343 |
| EC013 | ec013.157 | MVL-Ozkurt | fA_hz | 23 | 33 | 106.783 | 118.303 | -11.5204 | -1.95392 | 0.056636 | -0.523865 | -22.646 | 0.0329381 |
| EC013 | ec013.157 | MVL-Ozkurt | ozkurt_mvl | 23 | 33 | 0.129132 | 0.109169 | 0.0199629 | 1.9983 | 0.0511393 | 0.526855 | 0.00117972 | 0.0391527 |
| EC013 | ec013.157 | MVL-raw | fP_hz | 23 | 33 | 5.30435 | 5.78788 | -0.483531 | -0.960669 | 0.341008 | -0.242998 | -1.45267 | 0.485507 |
| EC013 | ec013.157 | MVL-raw | fA_hz | 23 | 33 | 83.1304 | 84.6061 | -1.47563 | -0.861328 | 0.392896 | -0.219607 | -4.87484 | 1.8025 |
| EC013 | ec013.157 | MVL-raw | ozkurt_mvl | 23 | 33 | 0.111611 | 0.0929943 | 0.0186167 | 2.03867 | 0.046633 | 0.531577 | 0.000996412 | 0.0356088 |
| EC013 | ec013.205 | APC-v1.0 | fP_hz | 8 | 9 | 7.60831 | 6.28001 | 1.3283 | 10.2172 | 4.46708e-08 | 4.63596 | 1.10038 | 1.58372 |
| EC013 | ec013.205 | APC-v1.0 | fA_hz | 8 | 9 | 125.75 | 123.444 | 2.30556 | 0.281839 | 0.782545 | 0.132315 | -13.1392 | 17.1951 |
| EC013 | ec013.205 | APC-v1.0 | ozkurt_mvl | 8 | 9 | 0.0592565 | 0.0675442 | -0.00828765 | -0.640358 | 0.531607 | -0.293443 | -0.0321791 | 0.0153993 |
| EC013 | ec013.205 | GLM | fP_hz | 8 | 9 | 6.25 | 6.83333 | -0.583333 | -0.525516 | 0.607858 | -0.235339 | -2.71545 | 1.43767 |
| EC013 | ec013.205 | GLM | fA_hz | 8 | 9 | 107 | 120.444 | -13.4444 | -1.08308 | 0.296706 | -0.502504 | -35.7236 | 9.83333 |
| EC013 | ec013.205 | GLM | ozkurt_mvl | 8 | 9 | 0.114678 | 0.0824013 | 0.032277 | 2.19903 | 0.0470419 | 1.03369 | 0.00486802 | 0.0600353 |
| EC013 | ec013.205 | KLMI | fP_hz | 8 | 9 | 6 | 4.94444 | 1.05556 | 1.26207 | 0.228427 | 0.590123 | -0.479167 | 2.61806 |
| EC013 | ec013.205 | KLMI | fA_hz | 8 | 9 | 106.5 | 118.222 | -11.7222 | -0.975302 | 0.345092 | -0.449544 | -33.5556 | 10.3347 |
| EC013 | ec013.205 | KLMI | ozkurt_mvl | 8 | 9 | 0.126836 | 0.0812329 | 0.0456031 | 2.45138 | 0.0297198 | 1.1535 | 0.0137578 | 0.0808361 |
| EC013 | ec013.205 | MVL-Ozkurt | fP_hz | 8 | 9 | 5.5625 | 5.72222 | -0.159722 | -0.175625 | 0.863244 | -0.0786074 | -1.85434 | 1.45139 |
| EC013 | ec013.205 | MVL-Ozkurt | fA_hz | 8 | 9 | 105 | 118.222 | -13.2222 | -1.00292 | 0.332293 | -0.463965 | -36.7778 | 11.6125 |
| EC013 | ec013.205 | MVL-Ozkurt | ozkurt_mvl | 8 | 9 | 0.150314 | 0.104215 | 0.0460996 | 2.72593 | 0.0170266 | 1.27575 | 0.0170205 | 0.0786848 |
| EC013 | ec013.205 | MVL-raw | fP_hz | 8 | 9 | 6.1875 | 5.22222 | 0.965278 | 1.07468 | 0.304509 | 0.509317 | -0.631944 | 2.70139 |
| EC013 | ec013.205 | MVL-raw | fA_hz | 8 | 9 | 81 | 86.2222 | -5.22222 | -1.07523 | 0.312549 | -0.466689 | -15.4444 | 1.05556 |
| EC013 | ec013.205 | MVL-raw | ozkurt_mvl | 8 | 9 | 0.130155 | 0.0971857 | 0.0329695 | 1.76755 | 0.100689 | 0.82943 | -0.00122874 | 0.0679708 |
| EC013 | ec013.206 | APC-v1.0 | fP_hz | 58 | 59 | 7.51866 | 6.36076 | 1.1579 | 12.0829 | 3.33814e-18 | 2.20249 | 0.967793 | 1.34008 |
| EC013 | ec013.206 | APC-v1.0 | fA_hz | 58 | 59 | 117.5 | 114.034 | 3.4661 | 0.962419 | 0.337867 | 0.176867 | -3.42904 | 10.483 |
| EC013 | ec013.206 | APC-v1.0 | ozkurt_mvl | 58 | 59 | 0.0767057 | 0.0629692 | 0.0137364 | 2.82453 | 0.00561436 | 0.519627 | 0.00431815 | 0.0232598 |
| EC013 | ec013.206 | GLM | fP_hz | 58 | 61 | 6.39655 | 6.82787 | -0.431317 | -1.04822 | 0.296699 | -0.190866 | -1.24707 | 0.378063 |
| EC013 | ec013.206 | GLM | fA_hz | 58 | 61 | 110.966 | 113.77 | -2.80497 | -0.673809 | 0.501762 | -0.122641 | -10.8165 | 5.19522 |
| EC013 | ec013.206 | GLM | ozkurt_mvl | 58 | 61 | 0.108928 | 0.0895573 | 0.0193704 | 3.73167 | 0.000320298 | 0.687017 | 0.00955298 | 0.029556 |
| EC013 | ec013.206 | KLMI | fP_hz | 58 | 61 | 4.84483 | 4.95082 | -0.105992 | -0.408229 | 0.683881 | -0.0739222 | -0.614927 | 0.398689 |
| EC013 | ec013.206 | KLMI | fA_hz | 58 | 61 | 107.655 | 113.049 | -5.39401 | -1.36446 | 0.175059 | -0.248824 | -12.9464 | 2.29059 |
| EC013 | ec013.206 | KLMI | ozkurt_mvl | 58 | 61 | 0.107995 | 0.0771764 | 0.0308186 | 4.39651 | 2.53237e-05 | 0.804861 | 0.0172813 | 0.0446182 |
| EC013 | ec013.206 | MVL-Ozkurt | fP_hz | 58 | 61 | 5.18103 | 5.43443 | -0.253392 | -0.740906 | 0.460245 | -0.134559 | -0.904077 | 0.411818 |
| EC013 | ec013.206 | MVL-Ozkurt | fA_hz | 58 | 61 | 107.034 | 114.754 | -7.71962 | -1.79132 | 0.0758833 | -0.32722 | -16.1448 | 0.695562 |
| EC013 | ec013.206 | MVL-Ozkurt | ozkurt_mvl | 58 | 61 | 0.137321 | 0.10513 | 0.0321908 | 5.69694 | 1.53466e-07 | 1.05162 | 0.0214465 | 0.043613 |
| EC013 | ec013.206 | MVL-raw | fP_hz | 58 | 61 | 5.18966 | 5.71311 | -0.52346 | -1.39109 | 0.166899 | -0.252184 | -1.26982 | 0.210857 |
| EC013 | ec013.206 | MVL-raw | fA_hz | 58 | 61 | 85.931 | 86.7541 | -0.823064 | -0.55753 | 0.578231 | -0.101406 | -3.70611 | 1.9831 |
| EC013 | ec013.206 | MVL-raw | ozkurt_mvl | 58 | 61 | 0.124215 | 0.0905074 | 0.0337081 | 6.22431 | 1.69887e-08 | 1.15033 | 0.0234605 | 0.044685 |
| EC013 | ec013.208 | APC-v1.0 | fP_hz | 43 | 48 | 8.73502 | 7.5574 | 1.17762 | 1.16161 | 0.248534 | 0.238991 | -0.820137 | 3.11641 |
| EC013 | ec013.208 | APC-v1.0 | fA_hz | 43 | 48 | 115.279 | 114.75 | 0.52907 | 0.129679 | 0.897114 | 0.0269273 | -7.48043 | 8.52548 |
| EC013 | ec013.208 | APC-v1.0 | ozkurt_mvl | 43 | 48 | 0.0586479 | 0.0720768 | -0.0134289 | -1.8265 | 0.0711946 | -0.37505 | -0.0280145 | 9.27372e-05 |
| EC013 | ec013.208 | GLM | fP_hz | 44 | 53 | 6.28409 | 6.11321 | 0.170883 | 0.398968 | 0.690891 | 0.0815533 | -0.65462 | 0.997877 |
| EC013 | ec013.208 | GLM | fA_hz | 44 | 53 | 114 | 117.585 | -3.58491 | -0.755031 | 0.452151 | -0.152492 | -12.7395 | 5.66269 |
| EC013 | ec013.208 | GLM | ozkurt_mvl | 44 | 53 | 0.101283 | 0.10026 | 0.00102351 | 0.144966 | 0.885046 | 0.0286707 | -0.0124418 | 0.0144913 |
| EC013 | ec013.208 | KLMI | fP_hz | 44 | 53 | 4.71591 | 4.69811 | 0.0177959 | 0.0815206 | 0.935205 | 0.0164921 | -0.406121 | 0.441472 |
| EC013 | ec013.208 | KLMI | fA_hz | 44 | 53 | 109.545 | 115.245 | -5.69983 | -1.32539 | 0.18826 | -0.266233 | -14.1186 | 2.63499 |
| EC013 | ec013.208 | KLMI | ozkurt_mvl | 44 | 53 | 0.103525 | 0.10248 | 0.00104464 | 0.102979 | 0.918216 | 0.0210641 | -0.0181327 | 0.0209494 |
| EC013 | ec013.208 | MVL-Ozkurt | fP_hz | 44 | 53 | 5.03409 | 5.12264 | -0.0885506 | -0.258557 | 0.796546 | -0.0520469 | -0.735211 | 0.571403 |
| EC013 | ec013.208 | MVL-Ozkurt | fA_hz | 44 | 53 | 111.273 | 112.377 | -1.10463 | -0.238667 | 0.811952 | -0.0491893 | -10.0551 | 8.00343 |
| EC013 | ec013.208 | MVL-Ozkurt | ozkurt_mvl | 44 | 53 | 0.14146 | 0.140463 | 0.000996487 | 0.117873 | 0.906433 | 0.0239893 | -0.0153344 | 0.0175986 |
| EC013 | ec013.208 | MVL-raw | fP_hz | 44 | 53 | 4.98864 | 5.25472 | -0.266081 | -0.766016 | 0.445568 | -0.152793 | -0.923671 | 0.407386 |
| EC013 | ec013.208 | MVL-raw | fA_hz | 44 | 53 | 106.909 | 108 | -1.09091 | -0.247309 | 0.805254 | -0.0506144 | -9.55931 | 7.51145 |
| EC013 | ec013.208 | MVL-raw | ozkurt_mvl | 44 | 53 | 0.139908 | 0.138618 | 0.0012896 | 0.154292 | 0.877728 | 0.0314082 | -0.0147722 | 0.0178297 |
| EC013 | ec013.251 | APC-v1.0 | fP_hz | 54 | 60 | 7.7387 | 6.71152 | 1.02718 | 7.20385 | 5.6266e-10 | 1.28262 | 0.744606 | 1.29815 |
| EC013 | ec013.251 | APC-v1.0 | fA_hz | 54 | 60 | 113.074 | 118.083 | -5.00926 | -1.31981 | 0.189598 | -0.245189 | -12.3871 | 2.26456 |
| EC013 | ec013.251 | APC-v1.0 | ozkurt_mvl | 54 | 60 | 0.0758889 | 0.0715588 | 0.00433012 | 0.909111 | 0.365247 | 0.168104 | -0.00497246 | 0.0137427 |
| EC013 | ec013.251 | GLM | fP_hz | 54 | 65 | 6.86111 | 6.83077 | 0.0303419 | 0.0703646 | 0.944027 | 0.0128412 | -0.794035 | 0.867664 |
| EC013 | ec013.251 | GLM | fA_hz | 54 | 65 | 114.148 | 115.385 | -1.23647 | -0.324335 | 0.746277 | -0.0591364 | -8.55866 | 6.11211 |
| EC013 | ec013.251 | GLM | ozkurt_mvl | 54 | 65 | 0.113688 | 0.0984906 | 0.0151973 | 2.29954 | 0.0235551 | 0.429898 | 0.00249343 | 0.0278609 |
| EC013 | ec013.251 | KLMI | fP_hz | 54 | 65 | 4.87963 | 4.55385 | 0.325783 | 1.51351 | 0.133278 | 0.28257 | -0.0810577 | 0.745164 |
| EC013 | ec013.251 | KLMI | fA_hz | 54 | 65 | 114.593 | 107.569 | 7.02336 | 1.84189 | 0.0681018 | 0.336617 | -0.253048 | 14.4482 |
| EC013 | ec013.251 | KLMI | ozkurt_mvl | 54 | 65 | 0.109962 | 0.0935584 | 0.0164034 | 1.74526 | 0.0839835 | 0.32582 | -0.00138615 | 0.0348516 |
| EC013 | ec013.251 | MVL-Ozkurt | fP_hz | 54 | 65 | 5.35185 | 5.21538 | 0.136467 | 0.444344 | 0.657642 | 0.0812543 | -0.461261 | 0.723226 |
| EC013 | ec013.251 | MVL-Ozkurt | fA_hz | 54 | 65 | 106.148 | 111.323 | -5.17493 | -1.31664 | 0.190668 | -0.241796 | -12.8721 | 2.47986 |
| EC013 | ec013.251 | MVL-Ozkurt | ozkurt_mvl | 54 | 65 | 0.155035 | 0.121667 | 0.0333678 | 4.67412 | 9.46166e-06 | 0.876518 | 0.0193844 | 0.0476168 |
| EC013 | ec013.251 | MVL-raw | fP_hz | 54 | 65 | 5.2963 | 5.56923 | -0.272934 | -0.743691 | 0.458562 | -0.13463 | -0.988907 | 0.43761 |
| EC013 | ec013.251 | MVL-raw | fA_hz | 54 | 65 | 83.9259 | 86.5231 | -2.59715 | -1.85296 | 0.0664197 | -0.331116 | -5.35613 | 0.135613 |
| EC013 | ec013.251 | MVL-raw | ozkurt_mvl | 54 | 65 | 0.13872 | 0.107429 | 0.0312915 | 4.55019 | 1.4756e-05 | 0.847469 | 0.0178119 | 0.0447134 |
| EC013 | ec013.252 | APC-v1.0 | fP_hz | 32 | 60 | 7.78113 | 6.54745 | 1.23368 | 7.69663 | 3.51399e-11 | 1.29499 | 0.925024 | 1.55344 |
| EC013 | ec013.252 | APC-v1.0 | fA_hz | 32 | 60 | 110.312 | 115.25 | -4.9375 | -1.1861 | 0.240156 | -0.26046 | -12.7617 | 3.01115 |
| EC013 | ec013.252 | APC-v1.0 | ozkurt_mvl | 32 | 60 | 0.0759432 | 0.0716244 | 0.00431873 | 0.715444 | 0.476916 | 0.154339 | -0.00736468 | 0.0163009 |
| EC013 | ec013.252 | GLM | fP_hz | 32 | 64 | 7.03125 | 6.52344 | 0.507812 | 1.07705 | 0.285756 | 0.234121 | -0.398438 | 1.4375 |
| EC013 | ec013.252 | GLM | fA_hz | 32 | 64 | 111.5 | 112.375 | -0.875 | -0.176776 | 0.860251 | -0.0377568 | -10.4375 | 8.875 |
| EC013 | ec013.252 | GLM | ozkurt_mvl | 32 | 64 | 0.113556 | 0.109368 | 0.00418814 | 0.460819 | 0.646903 | 0.107313 | -0.0137774 | 0.0218207 |
| EC013 | ec013.252 | KLMI | fP_hz | 32 | 64 | 4.5625 | 5.13281 | -0.570312 | -2.13625 | 0.0355739 | -0.408275 | -1.0625 | -0.0466797 |
| EC013 | ec013.252 | KLMI | fA_hz | 32 | 64 | 113.625 | 111.438 | 2.1875 | 0.466642 | 0.642407 | 0.100639 | -6.6875 | 11.125 |
| EC013 | ec013.252 | KLMI | ozkurt_mvl | 32 | 64 | 0.11384 | 0.105473 | 0.00836757 | 0.795524 | 0.430058 | 0.185942 | -0.0117953 | 0.0286119 |
| EC013 | ec013.252 | MVL-Ozkurt | fP_hz | 32 | 64 | 4.8125 | 5.32031 | -0.507812 | -1.5073 | 0.136971 | -0.327751 | -1.11719 | 0.179688 |
| EC013 | ec013.252 | MVL-Ozkurt | fA_hz | 32 | 64 | 114.125 | 113.562 | 0.5625 | 0.112703 | 0.910614 | 0.0238154 | -9.1875 | 10.125 |
| EC013 | ec013.252 | MVL-Ozkurt | ozkurt_mvl | 32 | 64 | 0.158973 | 0.134061 | 0.0249126 | 3.13708 | 0.00262961 | 0.679066 | 0.00977368 | 0.0402848 |
| EC013 | ec013.252 | MVL-raw | fP_hz | 32 | 64 | 5.15625 | 5.92188 | -0.765625 | -1.73163 | 0.0878465 | -0.35874 | -1.59375 | 0.15625 |
| EC013 | ec013.252 | MVL-raw | fA_hz | 32 | 64 | 85.875 | 83.9375 | 1.9375 | 1.10908 | 0.273469 | 0.275975 | -1.1875 | 5.5625 |
| EC013 | ec013.252 | MVL-raw | ozkurt_mvl | 32 | 64 | 0.13751 | 0.114402 | 0.0231078 | 2.94994 | 0.00454573 | 0.645075 | 0.00792065 | 0.0380281 |
| EC013 | ec013.374 | APC-v1.0 | fP_hz | 88 | 76 | 7.35947 | 6.32392 | 1.03554 | 8.00041 | 5.74451e-12 | 1.32865 | 0.789315 | 1.2894 |
| EC013 | ec013.374 | APC-v1.0 | fA_hz | 88 | 76 | 116.455 | 115.645 | 0.809809 | 0.273614 | 0.784739 | 0.0427121 | -4.78849 | 6.63805 |
| EC013 | ec013.374 | APC-v1.0 | ozkurt_mvl | 88 | 76 | 0.0745892 | 0.06998 | 0.00460918 | 1.18686 | 0.237115 | 0.186212 | -0.0032059 | 0.0119531 |
| EC013 | ec013.374 | GLM | fP_hz | 88 | 77 | 6.39773 | 6.35065 | 0.0470779 | 0.149476 | 0.881363 | 0.0230944 | -0.564144 | 0.652618 |
| EC013 | ec013.374 | GLM | fA_hz | 88 | 77 | 108.455 | 113.506 | -5.05195 | -1.45537 | 0.147634 | -0.228201 | -11.6429 | 1.77273 |
| EC013 | ec013.374 | GLM | ozkurt_mvl | 88 | 77 | 0.116703 | 0.108047 | 0.00865562 | 1.63229 | 0.104597 | 0.248715 | -0.00180338 | 0.0190335 |
| EC013 | ec013.374 | KLMI | fP_hz | 88 | 77 | 4.84659 | 5.24026 | -0.393669 | -1.77398 | 0.0780406 | -0.277515 | -0.818994 | 0.038961 |
| EC013 | ec013.374 | KLMI | fA_hz | 88 | 77 | 114.045 | 114.753 | -0.707792 | -0.208299 | 0.835269 | -0.0325507 | -7.24026 | 5.96802 |
| EC013 | ec013.374 | KLMI | ozkurt_mvl | 88 | 77 | 0.119003 | 0.0994821 | 0.0195212 | 2.98111 | 0.00331746 | 0.455788 | 0.0065385 | 0.0323814 |
| EC013 | ec013.374 | MVL-Ozkurt | fP_hz | 88 | 77 | 5.0625 | 5.64935 | -0.586851 | -2.37397 | 0.0189103 | -0.374329 | -1.06171 | -0.0949675 |
| EC013 | ec013.374 | MVL-Ozkurt | fA_hz | 88 | 77 | 112.5 | 116.571 | -4.07143 | -1.25854 | 0.210104 | -0.196962 | -10.3766 | 2.2664 |
| EC013 | ec013.374 | MVL-Ozkurt | ozkurt_mvl | 88 | 77 | 0.148853 | 0.121311 | 0.0275417 | 5.21583 | 5.77916e-07 | 0.791138 | 0.0173164 | 0.0379276 |
| EC013 | ec013.374 | MVL-raw | fP_hz | 88 | 77 | 5.34091 | 5.96104 | -0.62013 | -2.06891 | 0.0402128 | -0.32331 | -1.19645 | -0.0438312 |
| EC013 | ec013.374 | MVL-raw | fA_hz | 88 | 77 | 92.1364 | 87.013 | 5.12338 | 2.65016 | 0.00889023 | 0.401304 | 1.50649 | 8.96753 |
| EC013 | ec013.374 | MVL-raw | ozkurt_mvl | 88 | 77 | 0.135347 | 0.105556 | 0.0297909 | 5.35234 | 3.02125e-07 | 0.81383 | 0.0190077 | 0.0407426 |
| EC013 | ec013.375 | APC-v1.0 | fP_hz | 61 | 120 | 8.91449 | 9.66147 | -0.746984 | -0.876504 | 0.382055 | -0.122465 | -2.3895 | 0.898993 |
| EC013 | ec013.375 | APC-v1.0 | fA_hz | 61 | 120 | 112.77 | 113.392 | -0.621175 | -0.196735 | 0.844371 | -0.0310001 | -6.85271 | 5.47072 |
| EC013 | ec013.375 | APC-v1.0 | ozkurt_mvl | 61 | 120 | 0.0595333 | 0.05411 | 0.0054233 | 1.05106 | 0.295311 | 0.164067 | -0.0045681 | 0.015669 |
| EC013 | ec013.375 | GLM | fP_hz | 68 | 137 | 6.05882 | 6.74453 | -0.685702 | -2.31288 | 0.0219701 | -0.316413 | -1.2586 | -0.101704 |
| EC013 | ec013.375 | GLM | fA_hz | 68 | 137 | 113 | 114.803 | -1.80292 | -0.522307 | 0.602409 | -0.0801557 | -8.686 | 4.86304 |
| EC013 | ec013.375 | GLM | ozkurt_mvl | 68 | 137 | 0.113578 | 0.099766 | 0.0138116 | 2.13088 | 0.0348527 | 0.309981 | 0.00117721 | 0.0267864 |
| EC013 | ec013.375 | KLMI | fP_hz | 68 | 137 | 4.72794 | 4.73723 | -0.0092851 | -0.0619361 | 0.95071 | -0.00931389 | -0.288429 | 0.299061 |
| EC013 | ec013.375 | KLMI | fA_hz | 68 | 137 | 114.471 | 114.803 | -0.332331 | -0.0996136 | 0.920799 | -0.0146658 | -7.01174 | 6.10479 |
| EC013 | ec013.375 | KLMI | ozkurt_mvl | 68 | 137 | 0.115121 | 0.099313 | 0.0158075 | 2.07301 | 0.0399409 | 0.297236 | 0.000691129 | 0.0305229 |
| EC013 | ec013.375 | MVL-Ozkurt | fP_hz | 68 | 137 | 5.07353 | 5.0438 | 0.0297338 | 0.11862 | 0.905752 | 0.0174302 | -0.462585 | 0.518235 |
| EC013 | ec013.375 | MVL-Ozkurt | fA_hz | 68 | 137 | 115.059 | 114.131 | 0.927437 | 0.264384 | 0.791893 | 0.0391641 | -6.01687 | 7.5737 |
| EC013 | ec013.375 | MVL-Ozkurt | ozkurt_mvl | 68 | 137 | 0.14948 | 0.144147 | 0.00533284 | 0.742482 | 0.458763 | 0.0977716 | -0.00843383 | 0.0195061 |
| EC013 | ec013.375 | MVL-raw | fP_hz | 68 | 137 | 5.04412 | 4.95985 | 0.0842636 | 0.358642 | 0.720427 | 0.0529709 | -0.373775 | 0.550081 |
| EC013 | ec013.375 | MVL-raw | fA_hz | 68 | 137 | 111.765 | 111.854 | -0.0893087 | -0.0269724 | 0.978519 | -0.0038846 | -6.52158 | 6.32124 |
| EC013 | ec013.375 | MVL-raw | ozkurt_mvl | 68 | 137 | 0.14717 | 0.142637 | 0.00453339 | 0.649572 | 0.516786 | 0.0850431 | -0.00880772 | 0.0183775 |

POST HOC across-session table:
| animal_pool | method | outcome | n_sessions | mean_session_difference | median_session_difference | ci_low | ci_high | one_sample_t | one_sample_p | wilcoxon_statistic | wilcoxon_p | zero_differences |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EC012 | APC-v1.0 | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | APC-v1.0 | fA_hz | 9 | -0.640901 | 0.52907 | -3.69711 | 2.41531 | -0.483579 | 0.641643 | 19 | 0.734375 | 0 |
| pooled | APC-v1.0 | fA_hz | 9 | -0.640901 | 0.52907 | -3.69711 | 2.41531 | -0.483579 | 0.641643 | 19 | 0.734375 | 0 |
| EC012 | APC-v1.0 | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | APC-v1.0 | fP_hz | 9 | 0.990233 | 1.1579 | 0.473246 | 1.50722 | 4.4169 | 0.00223572 | 1 | 0.0078125 | 0 |
| pooled | APC-v1.0 | fP_hz | 9 | 0.990233 | 1.1579 | 0.473246 | 1.50722 | 4.4169 | 0.00223572 | 1 | 0.0078125 | 0 |
| EC012 | APC-v1.0 | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | APC-v1.0 | ozkurt_mvl | 9 | 0.00360524 | 0.00433012 | -0.00400565 | 0.0112161 | 1.09234 | 0.306483 | 13 | 0.300781 | 0 |
| pooled | APC-v1.0 | ozkurt_mvl | 9 | 0.00360524 | 0.00433012 | -0.00400565 | 0.0112161 | 1.09234 | 0.306483 | 13 | 0.300781 | 0 |
| EC012 | GLM | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | GLM | fA_hz | 9 | -4.58286 | -3.58491 | -7.64281 | -1.5229 | -3.45368 | 0.00864788 | 0 | 0.00390625 | 0 |
| pooled | GLM | fA_hz | 9 | -4.58286 | -3.58491 | -7.64281 | -1.5229 | -3.45368 | 0.00864788 | 0 | 0.00390625 | 0 |
| EC012 | GLM | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | GLM | fP_hz | 9 | -0.114365 | -0.0178571 | -0.408805 | 0.180074 | -0.89569 | 0.396568 | 17 | 0.570312 | 0 |
| pooled | GLM | fP_hz | 9 | -0.114365 | -0.0178571 | -0.408805 | 0.180074 | -0.89569 | 0.396568 | 17 | 0.570312 | 0 |
| EC012 | GLM | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | GLM | ozkurt_mvl | 9 | 0.0144971 | 0.0138116 | 0.00716858 | 0.0218256 | 4.56168 | 0.00184583 | 0 | 0.00390625 | 0 |
| pooled | GLM | ozkurt_mvl | 9 | 0.0144971 | 0.0138116 | 0.00716858 | 0.0218256 | 4.56168 | 0.00184583 | 0 | 0.00390625 | 0 |
| EC012 | KLMI | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | KLMI | fA_hz | 9 | -3.01472 | -3.92857 | -7.4019 | 1.37245 | -1.58461 | 0.151714 | 10 | 0.164062 | 0 |
| pooled | KLMI | fA_hz | 9 | -3.01472 | -3.92857 | -7.4019 | 1.37245 | -1.58461 | 0.151714 | 10 | 0.164062 | 0 |
| EC012 | KLMI | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | KLMI | fP_hz | 9 | -0.0408458 | -0.105992 | -0.419861 | 0.338169 | -0.248514 | 0.809997 | 16 | 0.496094 | 0 |
| pooled | KLMI | fP_hz | 9 | -0.0408458 | -0.105992 | -0.419861 | 0.338169 | -0.248514 | 0.809997 | 16 | 0.496094 | 0 |
| EC012 | KLMI | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | KLMI | ozkurt_mvl | 9 | 0.0183475 | 0.0164034 | 0.00728335 | 0.0294117 | 3.82401 | 0.00506083 | 0 | 0.00390625 | 0 |
| pooled | KLMI | ozkurt_mvl | 9 | 0.0183475 | 0.0164034 | 0.00728335 | 0.0294117 | 3.82401 | 0.00506083 | 0 | 0.00390625 | 0 |
| EC012 | MVL-Ozkurt | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-Ozkurt | fA_hz | 9 | -5.06767 | -4.28571 | -8.91225 | -1.22309 | -3.03962 | 0.0160725 | 3 | 0.0195312 | 0 |
| pooled | MVL-Ozkurt | fA_hz | 9 | -5.06767 | -4.28571 | -8.91225 | -1.22309 | -3.03962 | 0.0160725 | 3 | 0.0195312 | 0 |
| EC012 | MVL-Ozkurt | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-Ozkurt | fP_hz | 9 | -0.254238 | -0.253392 | -0.447624 | -0.0608514 | -3.03162 | 0.0162694 | 4 | 0.0273438 | 0 |
| pooled | MVL-Ozkurt | fP_hz | 9 | -0.254238 | -0.253392 | -0.447624 | -0.0608514 | -3.03162 | 0.0162694 | 4 | 0.0273438 | 0 |
| EC012 | MVL-Ozkurt | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-Ozkurt | ozkurt_mvl | 9 | 0.0251124 | 0.0275417 | 0.0139929 | 0.036232 | 5.20788 | 0.000814526 | 0 | 0.00390625 | 0 |
| pooled | MVL-Ozkurt | ozkurt_mvl | 9 | 0.0251124 | 0.0275417 | 0.0139929 | 0.036232 | 5.20788 | 0.000814526 | 0 | 0.00390625 | 0 |
| EC012 | MVL-raw | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-raw | fA_hz | 9 | -0.661299 | -1.09091 | -2.88705 | 1.56445 | -0.685144 | 0.512612 | 14 | 0.359375 | 0 |
| pooled | MVL-raw | fA_hz | 9 | -0.661299 | -1.09091 | -2.88705 | 1.56445 | -0.685144 | 0.512612 | 14 | 0.359375 | 0 |
| EC012 | MVL-raw | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-raw | fP_hz | 9 | -0.190286 | -0.272934 | -0.599345 | 0.218773 | -1.07271 | 0.314692 | 12 | 0.25 | 0 |
| pooled | MVL-raw | fP_hz | 9 | -0.190286 | -0.272934 | -0.599345 | 0.218773 | -1.07271 | 0.314692 | 12 | 0.25 | 0 |
| EC012 | MVL-raw | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-raw | ozkurt_mvl | 9 | 0.023095 | 0.0297909 | 0.0134806 | 0.0327093 | 5.53932 | 0.000547799 | 0 | 0.00390625 | 0 |
| pooled | MVL-raw | ozkurt_mvl | 9 | 0.023095 | 0.0297909 | 0.0134806 | 0.0327093 | 5.53932 | 0.000547799 | 0 | 0.00390625 | 0 |

### POST HOC EC statistics

POST HOC per-session table:
| animal | session | method | outcome | n_run | n_rest | run_mean | rest_mean | mean_difference | welch_t | welch_p | hedges_g | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EC012 | ec012ec.239 | APC-v1.0 | fP_hz | 47 | 33 | 8.78633 | 6.35186 | 2.43447 | 13.123 | 1.13688e-14 | 3.50116 | 2.10267 | 2.81082 |
| EC012 | ec012ec.239 | APC-v1.0 | fA_hz | 47 | 33 | 106.149 | 119.788 | -13.6389 | -3.3923 | 0.00118834 | -0.776674 | -21.1382 | -5.67567 |
| EC012 | ec012ec.239 | APC-v1.0 | ozkurt_mvl | 47 | 33 | 0.0936739 | 0.0773374 | 0.0163365 | 2.38718 | 0.0201793 | 0.557282 | 0.00294183 | 0.0299206 |
| EC012 | ec012ec.239 | GLM | fP_hz | 47 | 34 | 8.09574 | 6.76471 | 1.33104 | 2.79548 | 0.00672465 | 0.630466 | 0.389847 | 2.24096 |
| EC012 | ec012ec.239 | GLM | fA_hz | 47 | 34 | 106.468 | 107.882 | -1.41427 | -0.309942 | 0.757577 | -0.0703775 | -10.3511 | 7.51464 |
| EC012 | ec012ec.239 | GLM | ozkurt_mvl | 47 | 34 | 0.135288 | 0.122209 | 0.0130797 | 2.0202 | 0.0477128 | 0.466161 | 0.000432465 | 0.0256994 |
| EC012 | ec012ec.239 | KLMI | fP_hz | 47 | 34 | 6.05319 | 4.54412 | 1.50907 | 3.9187 | 0.000205862 | 0.78791 | 0.778465 | 2.24376 |
| EC012 | ec012ec.239 | KLMI | fA_hz | 47 | 34 | 107.66 | 112.471 | -4.81101 | -0.941442 | 0.350023 | -0.215544 | -14.6433 | 5.0597 |
| EC012 | ec012ec.239 | KLMI | ozkurt_mvl | 47 | 34 | 0.129877 | 0.107177 | 0.0226996 | 2.17828 | 0.0329671 | 0.495298 | 0.00244513 | 0.0423427 |
| EC012 | ec012ec.239 | MVL-Ozkurt | fP_hz | 47 | 34 | 5.89362 | 5.60294 | 0.290676 | 0.683103 | 0.496632 | 0.149533 | -0.547896 | 1.10952 |
| EC012 | ec012ec.239 | MVL-Ozkurt | fA_hz | 47 | 34 | 110.468 | 109.882 | 0.585732 | 0.106837 | 0.915264 | 0.0246473 | -10.0732 | 11.4807 |
| EC012 | ec012ec.239 | MVL-Ozkurt | ozkurt_mvl | 47 | 34 | 0.166889 | 0.142893 | 0.0239968 | 3.19561 | 0.00208725 | 0.714407 | 0.00922458 | 0.0381493 |
| EC012 | ec012ec.239 | MVL-raw | fP_hz | 47 | 34 | 5.92553 | 5.95588 | -0.0303504 | -0.0654245 | 0.948012 | -0.0144128 | -0.920533 | 0.884551 |
| EC012 | ec012ec.239 | MVL-raw | fA_hz | 47 | 34 | 88.5106 | 82.3529 | 6.1577 | 3.50951 | 0.000748877 | 0.731256 | 2.6883 | 9.54693 |
| EC012 | ec012ec.239 | MVL-raw | ozkurt_mvl | 47 | 34 | 0.149017 | 0.128348 | 0.0206689 | 2.56228 | 0.0125872 | 0.57637 | 0.00467795 | 0.0360464 |
| EC012 | ec012ec.240 | APC-v1.0 | fP_hz | 66 | 15 | 8.93517 | 6.32825 | 2.60691 | 6.11908 | 2.52843e-05 | 3.53104 | 1.90124 | 3.48305 |
| EC012 | ec012ec.240 | APC-v1.0 | fA_hz | 66 | 15 | 113.53 | 112.2 | 1.3303 | 0.209652 | 0.836278 | 0.0692059 | -10.9136 | 13.0697 |
| EC012 | ec012ec.240 | APC-v1.0 | ozkurt_mvl | 66 | 15 | 0.0882551 | 0.0860497 | 0.00220546 | 0.242981 | 0.810738 | 0.0797823 | -0.0169566 | 0.0176425 |
| EC012 | ec012ec.240 | GLM | fP_hz | 66 | 17 | 7.68182 | 7.11765 | 0.564171 | 0.728508 | 0.474761 | 0.245578 | -0.916254 | 2.01114 |
| EC012 | ec012ec.240 | GLM | fA_hz | 66 | 17 | 110.364 | 115.765 | -5.40107 | -0.927439 | 0.363425 | -0.269961 | -16.1783 | 5.72228 |
| EC012 | ec012ec.240 | GLM | ozkurt_mvl | 66 | 17 | 0.131117 | 0.139318 | -0.00820064 | -0.56393 | 0.579406 | -0.20454 | -0.0387576 | 0.016732 |
| EC012 | ec012ec.240 | KLMI | fP_hz | 66 | 17 | 5.98485 | 4.76471 | 1.22014 | 2.59618 | 0.0140355 | 0.589106 | 0.231283 | 2.037 |
| EC012 | ec012ec.240 | KLMI | fA_hz | 66 | 17 | 109.697 | 106.353 | 3.34403 | 0.609654 | 0.54765 | 0.165109 | -7.1238 | 13.5616 |
| EC012 | ec012ec.240 | KLMI | ozkurt_mvl | 66 | 17 | 0.122452 | 0.125479 | -0.00302653 | -0.180411 | 0.85865 | -0.0608752 | -0.0381392 | 0.0259956 |
| EC012 | ec012ec.240 | MVL-Ozkurt | fP_hz | 66 | 17 | 5.61364 | 5.23529 | 0.378342 | 0.644971 | 0.525623 | 0.194456 | -0.8124 | 1.41357 |
| EC012 | ec012ec.240 | MVL-Ozkurt | fA_hz | 66 | 17 | 109.636 | 110.118 | -0.481283 | -0.0908204 | 0.928296 | -0.0228302 | -10.6953 | 9.90045 |
| EC012 | ec012ec.240 | MVL-Ozkurt | ozkurt_mvl | 66 | 17 | 0.164737 | 0.154572 | 0.0101654 | 0.782752 | 0.443021 | 0.266349 | -0.0170997 | 0.032523 |
| EC012 | ec012ec.240 | MVL-raw | fP_hz | 66 | 17 | 5.76515 | 5.14706 | 0.618093 | 1.48691 | 0.145827 | 0.322244 | -0.209013 | 1.38324 |
| EC012 | ec012ec.240 | MVL-raw | fA_hz | 66 | 17 | 88.1818 | 84 | 4.18182 | 2.52165 | 0.0149321 | 0.476399 | 1.02674 | 7.35116 |
| EC012 | ec012ec.240 | MVL-raw | ozkurt_mvl | 66 | 17 | 0.151178 | 0.125492 | 0.0256857 | 2.7874 | 0.00980489 | 0.727547 | 0.00741585 | 0.0427975 |
| EC012 | ec012ec.269 | APC-v1.0 | fP_hz | 38 | 45 | 9.11385 | 6.15909 | 2.95476 | 15.738 | 4.37671e-20 | 3.16256 | 2.59873 | 3.33576 |
| EC012 | ec012ec.269 | APC-v1.0 | fA_hz | 38 | 45 | 111.684 | 113.578 | -1.89357 | -0.452089 | 0.652438 | -0.0984325 | -9.92959 | 6.03921 |
| EC012 | ec012ec.269 | APC-v1.0 | ozkurt_mvl | 38 | 45 | 0.0933795 | 0.0773807 | 0.0159988 | 2.3857 | 0.0194109 | 0.508473 | 0.00250822 | 0.0288772 |
| EC012 | ec012ec.269 | GLM | fP_hz | 38 | 48 | 7.56579 | 6.1875 | 1.37829 | 2.73189 | 0.00798276 | 0.604145 | 0.411171 | 2.32678 |
| EC012 | ec012ec.269 | GLM | fA_hz | 38 | 48 | 111.263 | 114.75 | -3.48684 | -0.764313 | 0.446872 | -0.162846 | -12.5531 | 5.43871 |
| EC012 | ec012ec.269 | GLM | ozkurt_mvl | 38 | 48 | 0.144369 | 0.107142 | 0.0372275 | 4.57012 | 2.70414e-05 | 1.04223 | 0.0222426 | 0.0535931 |
| EC012 | ec012ec.269 | KLMI | fP_hz | 38 | 48 | 5.76316 | 4.95833 | 0.804825 | 1.88539 | 0.0642769 | 0.426862 | 0.0060307 | 1.64257 |
| EC012 | ec012ec.269 | KLMI | fA_hz | 38 | 48 | 111.684 | 114.75 | -3.06579 | -0.645794 | 0.520206 | -0.137349 | -12.1185 | 6.21535 |
| EC012 | ec012ec.269 | KLMI | ozkurt_mvl | 38 | 48 | 0.136786 | 0.103928 | 0.032858 | 3.17614 | 0.002493 | 0.731086 | 0.0133635 | 0.0529437 |
| EC012 | ec012ec.269 | MVL-Ozkurt | fP_hz | 38 | 48 | 6.31579 | 5.19792 | 1.11787 | 2.47628 | 0.0163971 | 0.567094 | 0.259855 | 1.99677 |
| EC012 | ec012ec.269 | MVL-Ozkurt | fA_hz | 38 | 48 | 103.895 | 114.083 | -10.1886 | -2.33493 | 0.0219856 | -0.481063 | -18.693 | -1.85504 |
| EC012 | ec012ec.269 | MVL-Ozkurt | ozkurt_mvl | 38 | 48 | 0.175542 | 0.127008 | 0.0485339 | 5.581 | 1.33767e-06 | 1.31559 | 0.0329596 | 0.0655964 |
| EC012 | ec012ec.269 | MVL-raw | fP_hz | 38 | 48 | 6.76316 | 5.94792 | 0.815241 | 1.43306 | 0.15635 | 0.317048 | -0.266996 | 1.9249 |
| EC012 | ec012ec.269 | MVL-raw | fA_hz | 38 | 48 | 88.1053 | 84.5833 | 3.52193 | 1.8638 | 0.0659319 | 0.39742 | -0.144846 | 7.08772 |
| EC012 | ec012ec.269 | MVL-raw | ozkurt_mvl | 38 | 48 | 0.158876 | 0.107506 | 0.0513692 | 5.85705 | 3.80215e-07 | 1.36103 | 0.035594 | 0.0687097 |
| EC012 | ec012ec.270 | APC-v1.0 | fP_hz | 24 | 40 | 9.2892 | 6.49204 | 2.79716 | 16.6527 | 2.04629e-20 | 3.3364 | 2.49371 | 3.14341 |
| EC012 | ec012ec.270 | APC-v1.0 | fA_hz | 24 | 40 | 114.125 | 111.25 | 2.875 | 0.566577 | 0.573443 | 0.141394 | -6.82151 | 12.7021 |
| EC012 | ec012ec.270 | APC-v1.0 | ozkurt_mvl | 24 | 40 | 0.0699128 | 0.0694056 | 0.00050725 | 0.0704622 | 0.944074 | 0.0170234 | -0.0132576 | 0.0145367 |
| EC012 | ec012ec.270 | GLM | fP_hz | 24 | 49 | 6.91667 | 6.56122 | 0.355442 | 0.589844 | 0.558233 | 0.146139 | -0.782781 | 1.54594 |
| EC012 | ec012ec.270 | GLM | fA_hz | 24 | 49 | 115.167 | 109.796 | 5.37075 | 0.893026 | 0.376769 | 0.224771 | -6.04422 | 17.0411 |
| EC012 | ec012ec.270 | GLM | ozkurt_mvl | 24 | 49 | 0.121321 | 0.116372 | 0.00494876 | 0.640432 | 0.524508 | 0.146337 | -0.00981855 | 0.0199276 |
| EC012 | ec012ec.270 | KLMI | fP_hz | 24 | 49 | 5.02083 | 4.81633 | 0.204507 | 0.508903 | 0.614464 | 0.14977 | -0.486001 | 1.02681 |
| EC012 | ec012ec.270 | KLMI | fA_hz | 24 | 49 | 118 | 100.898 | 17.102 | 3.0236 | 0.00455271 | 0.818045 | 5.86378 | 27.6907 |
| EC012 | ec012ec.270 | KLMI | ozkurt_mvl | 24 | 49 | 0.114469 | 0.111311 | 0.00315791 | 0.278793 | 0.781501 | 0.0652994 | -0.0186349 | 0.0248158 |
| EC012 | ec012ec.270 | MVL-Ozkurt | fP_hz | 24 | 49 | 5.375 | 5.63265 | -0.257653 | -0.558545 | 0.579596 | -0.145476 | -1.12628 | 0.651371 |
| EC012 | ec012ec.270 | MVL-Ozkurt | fA_hz | 24 | 49 | 114.667 | 110.449 | 4.21769 | 0.75693 | 0.452641 | 0.180378 | -6.68418 | 14.7826 |
| EC012 | ec012ec.270 | MVL-Ozkurt | ozkurt_mvl | 24 | 49 | 0.16915 | 0.14008 | 0.02907 | 2.9288 | 0.00552111 | 0.7524 | 0.0104095 | 0.0484461 |
| EC012 | ec012ec.270 | MVL-raw | fP_hz | 24 | 49 | 5.70833 | 5.57143 | 0.136905 | 0.258687 | 0.797119 | 0.065519 | -0.833355 | 1.16116 |
| EC012 | ec012ec.270 | MVL-raw | fA_hz | 24 | 49 | 84.5 | 85.551 | -1.05102 | -0.592276 | 0.555881 | -0.131318 | -4.33342 | 2.49668 |
| EC012 | ec012ec.270 | MVL-raw | ozkurt_mvl | 24 | 49 | 0.141304 | 0.124891 | 0.016413 | 1.45865 | 0.154015 | 0.411331 | -0.00474851 | 0.0384119 |
| EC012 | ec012ec.271 | APC-v1.0 | fP_hz | 35 | 16 | 8.98332 | 6.30448 | 2.67884 | 6.56162 | 7.90524e-06 | 2.84571 | 1.95444 | 3.49734 |
| EC012 | ec012ec.271 | APC-v1.0 | fA_hz | 35 | 16 | 113.257 | 115.562 | -2.30536 | -0.315453 | 0.755037 | -0.100281 | -15.987 | 11.6957 |
| EC012 | ec012ec.271 | APC-v1.0 | ozkurt_mvl | 35 | 16 | 0.0713956 | 0.0697482 | 0.00164739 | 0.12628 | 0.900941 | 0.0490658 | -0.0257154 | 0.0244639 |
| EC012 | ec012ec.271 | GLM | fP_hz | 35 | 21 | 7.44286 | 5.54762 | 1.89524 | 2.85586 | 0.00623751 | 0.732119 | 0.6 | 3.12857 |
| EC012 | ec012ec.271 | GLM | fA_hz | 35 | 21 | 102.057 | 109.143 | -7.08571 | -1.38422 | 0.173907 | -0.382336 | -17.0676 | 2.66667 |
| EC012 | ec012ec.271 | GLM | ozkurt_mvl | 35 | 21 | 0.115118 | 0.102004 | 0.0131134 | 1.15685 | 0.255038 | 0.331982 | -0.00855714 | 0.0351629 |
| EC012 | ec012ec.271 | KLMI | fP_hz | 35 | 21 | 5.02857 | 4.47619 | 0.552381 | 1.39198 | 0.17022 | 0.359854 | -0.252381 | 1.28095 |
| EC012 | ec012ec.271 | KLMI | fA_hz | 35 | 21 | 115.2 | 104 | 11.2 | 1.93648 | 0.0587342 | 0.505381 | -0.0380952 | 22.4 |
| EC012 | ec012ec.271 | KLMI | ozkurt_mvl | 35 | 21 | 0.103583 | 0.0967235 | 0.00685987 | 0.500592 | 0.62025 | 0.150797 | -0.020419 | 0.0323119 |
| EC012 | ec012ec.271 | MVL-Ozkurt | fP_hz | 35 | 21 | 5.6 | 5.02381 | 0.57619 | 1.06987 | 0.289622 | 0.268858 | -0.466667 | 1.59524 |
| EC012 | ec012ec.271 | MVL-Ozkurt | fA_hz | 35 | 21 | 112.114 | 110.476 | 1.6381 | 0.281362 | 0.779987 | 0.0795927 | -9.52381 | 12.801 |
| EC012 | ec012ec.271 | MVL-Ozkurt | ozkurt_mvl | 35 | 21 | 0.148759 | 0.137889 | 0.0108692 | 1.06218 | 0.295813 | 0.311406 | -0.00902889 | 0.0304557 |
| EC012 | ec012ec.271 | MVL-raw | fP_hz | 35 | 21 | 6.34286 | 5.7381 | 0.604762 | 0.952373 | 0.345432 | 0.242625 | -0.638095 | 1.80964 |
| EC012 | ec012ec.271 | MVL-raw | fA_hz | 35 | 21 | 85.1429 | 84 | 1.14286 | 0.516027 | 0.608318 | 0.136763 | -3.2 | 5.33429 |
| EC012 | ec012ec.271 | MVL-raw | ozkurt_mvl | 35 | 21 | 0.127374 | 0.118309 | 0.00906462 | 0.86413 | 0.394174 | 0.25923 | -0.0117951 | 0.0287548 |
| EC012 | ec012ec.356 | APC-v1.0 | fP_hz | 40 | 46 | 9.19772 | 6.13454 | 3.06318 | 19.7346 | 8.71834e-25 | 3.95757 | 2.78215 | 3.37731 |
| EC012 | ec012ec.356 | APC-v1.0 | fA_hz | 40 | 46 | 111.775 | 110.5 | 1.275 | 0.329421 | 0.742659 | 0.0700669 | -6.21035 | 8.82057 |
| EC012 | ec012ec.356 | APC-v1.0 | ozkurt_mvl | 40 | 46 | 0.108625 | 0.0864084 | 0.0222163 | 3.37018 | 0.00113921 | 0.718758 | 0.00945757 | 0.0347934 |
| EC012 | ec012ec.356 | GLM | fP_hz | 40 | 50 | 8.2375 | 6.93 | 1.3075 | 2.91144 | 0.0046116 | 0.612641 | 0.417437 | 2.18 |
| EC012 | ec012ec.356 | GLM | fA_hz | 40 | 50 | 110.6 | 106.48 | 4.12 | 0.97207 | 0.33371 | 0.201738 | -4 | 12.3005 |
| EC012 | ec012ec.356 | GLM | ozkurt_mvl | 40 | 50 | 0.138114 | 0.124228 | 0.0138856 | 1.97613 | 0.0518735 | 0.425893 | 0.000160203 | 0.0272359 |
| EC012 | ec012ec.356 | KLMI | fP_hz | 40 | 50 | 6.35 | 5.75 | 0.6 | 1.3037 | 0.196393 | 0.281055 | -0.282563 | 1.5 |
| EC012 | ec012ec.356 | KLMI | fA_hz | 40 | 50 | 110.2 | 109.12 | 1.08 | 0.249679 | 0.803438 | 0.0522935 | -7.0205 | 9.4005 |
| EC012 | ec012ec.356 | KLMI | ozkurt_mvl | 40 | 50 | 0.140246 | 0.115325 | 0.0249209 | 2.45314 | 0.0170184 | 0.543203 | 0.00433822 | 0.0447605 |
| EC012 | ec012ec.356 | MVL-Ozkurt | fP_hz | 40 | 50 | 5.9875 | 6.4 | -0.4125 | -0.877718 | 0.382634 | -0.185068 | -1.3275 | 0.5175 |
| EC012 | ec012ec.356 | MVL-Ozkurt | fA_hz | 40 | 50 | 107 | 109.68 | -2.68 | -0.574706 | 0.566979 | -0.119489 | -11.5005 | 6.48 |
| EC012 | ec012ec.356 | MVL-Ozkurt | ozkurt_mvl | 40 | 50 | 0.181963 | 0.140944 | 0.0410194 | 5.55997 | 5.10189e-07 | 1.21657 | 0.0266159 | 0.0553577 |
| EC012 | ec012ec.356 | MVL-raw | fP_hz | 40 | 50 | 5.9 | 6.09 | -0.19 | -0.435263 | 0.664529 | -0.0922497 | -1.03006 | 0.665 |
| EC012 | ec012ec.356 | MVL-raw | fA_hz | 40 | 50 | 88.3 | 84.72 | 3.58 | 1.95917 | 0.0534202 | 0.412024 | 0 | 7.08 |
| EC012 | ec012ec.356 | MVL-raw | ozkurt_mvl | 40 | 50 | 0.168507 | 0.124246 | 0.0442615 | 5.88421 | 1.36306e-07 | 1.28479 | 0.0295949 | 0.0589782 |
| EC012 | ec012ec.357 | APC-v1.0 | fP_hz | 38 | 34 | 8.99512 | 6.83737 | 2.15776 | 12.0858 | 1.28745e-14 | 2.95921 | 1.8237 | 2.50947 |
| EC012 | ec012ec.357 | APC-v1.0 | fA_hz | 38 | 34 | 107.237 | 122.471 | -15.2337 | -3.75359 | 0.000365276 | -0.880662 | -22.9057 | -7.35756 |
| EC012 | ec012ec.357 | APC-v1.0 | ozkurt_mvl | 38 | 34 | 0.0772047 | 0.0728652 | 0.00433956 | 0.627427 | 0.532886 | 0.14964 | -0.00919696 | 0.017524 |
| EC012 | ec012ec.357 | GLM | fP_hz | 38 | 36 | 6.36842 | 6.33333 | 0.0350877 | 0.0629803 | 0.949957 | 0.0144911 | -1.03947 | 1.11184 |
| EC012 | ec012ec.357 | GLM | fA_hz | 38 | 36 | 112.105 | 108.778 | 3.32749 | 0.662593 | 0.509737 | 0.152763 | -6.4095 | 13.0996 |
| EC012 | ec012ec.357 | GLM | ozkurt_mvl | 38 | 36 | 0.125634 | 0.129084 | -0.00344954 | -0.309542 | 0.757922 | -0.0704351 | -0.0244989 | 0.0190471 |
| EC012 | ec012ec.357 | KLMI | fP_hz | 38 | 36 | 4.82895 | 5.06944 | -0.240497 | -0.765676 | 0.446384 | -0.175618 | -0.833333 | 0.377211 |
| EC012 | ec012ec.357 | KLMI | fA_hz | 38 | 36 | 115.684 | 114 | 1.68421 | 0.335827 | 0.737995 | 0.0774484 | -7.93611 | 11.2225 |
| EC012 | ec012ec.357 | KLMI | ozkurt_mvl | 38 | 36 | 0.119156 | 0.115003 | 0.00415246 | 0.330857 | 0.741714 | 0.0760714 | -0.0198914 | 0.0292059 |
| EC012 | ec012ec.357 | MVL-Ozkurt | fP_hz | 38 | 36 | 5.14474 | 5.76389 | -0.619152 | -1.48362 | 0.142568 | -0.343394 | -1.43569 | 0.207639 |
| EC012 | ec012ec.357 | MVL-Ozkurt | fA_hz | 38 | 36 | 117.053 | 111.778 | 5.27485 | 1.03394 | 0.304664 | 0.238286 | -4.52105 | 15.0177 |
| EC012 | ec012ec.357 | MVL-Ozkurt | ozkurt_mvl | 38 | 36 | 0.174776 | 0.157096 | 0.0176798 | 1.94791 | 0.0554365 | 0.445579 | 0.000413465 | 0.0356961 |
| EC012 | ec012ec.357 | MVL-raw | fP_hz | 38 | 36 | 5.03947 | 5.76389 | -0.724415 | -1.81722 | 0.0738955 | -0.421818 | -1.50223 | 0.0416667 |
| EC012 | ec012ec.357 | MVL-raw | fA_hz | 38 | 36 | 87.3684 | 82.3333 | 5.03509 | 2.7085 | 0.00908205 | 0.612467 | 1.57295 | 8.66082 |
| EC012 | ec012ec.357 | MVL-raw | ozkurt_mvl | 38 | 36 | 0.154569 | 0.137322 | 0.0172473 | 1.84117 | 0.0697559 | 0.42424 | -0.00111975 | 0.0355095 |
| EC012 | ec012ec.375 | APC-v1.0 | fP_hz | 37 | 31 | 8.92497 | 6.84899 | 2.07598 | 16.8318 | 1.12142e-18 | 4.34671 | 1.84572 | 2.32158 |
| EC012 | ec012ec.375 | APC-v1.0 | fA_hz | 37 | 31 | 107.919 | 117.065 | -9.1456 | -2.03753 | 0.0461476 | -0.498795 | -18.0064 | -0.455991 |
| EC012 | ec012ec.375 | APC-v1.0 | ozkurt_mvl | 37 | 31 | 0.103347 | 0.072532 | 0.0308151 | 4.09148 | 0.000119011 | 0.970902 | 0.0165604 | 0.0451492 |
| EC012 | ec012ec.375 | GLM | fP_hz | 37 | 32 | 8.52703 | 7.3125 | 1.21453 | 2.42754 | 0.0181637 | 0.586541 | 0.243222 | 2.1723 |
| EC012 | ec012ec.375 | GLM | fA_hz | 37 | 32 | 109.946 | 107.5 | 2.44595 | 0.456593 | 0.649594 | 0.110421 | -7.83454 | 12.6661 |
| EC012 | ec012ec.375 | GLM | ozkurt_mvl | 37 | 32 | 0.138221 | 0.119131 | 0.0190904 | 2.18359 | 0.0326957 | 0.524625 | 0.00252575 | 0.0356284 |
| EC012 | ec012ec.375 | KLMI | fP_hz | 37 | 32 | 6.51351 | 5.39062 | 1.12289 | 2.15069 | 0.0351615 | 0.503633 | 0.128378 | 2.14365 |
| EC012 | ec012ec.375 | KLMI | fA_hz | 37 | 32 | 109.297 | 109.875 | -0.577703 | -0.11351 | 0.909976 | -0.0271461 | -10.0813 | 9.19603 |
| EC012 | ec012ec.375 | KLMI | ozkurt_mvl | 37 | 32 | 0.128862 | 0.109103 | 0.0197584 | 1.74143 | 0.0862019 | 0.410335 | -0.00207565 | 0.0416704 |
| EC012 | ec012ec.375 | MVL-Ozkurt | fP_hz | 37 | 32 | 6.12162 | 5.5625 | 0.559122 | 1.12466 | 0.264901 | 0.261881 | -0.415129 | 1.52495 |
| EC012 | ec012ec.375 | MVL-Ozkurt | fA_hz | 37 | 32 | 106.378 | 120.25 | -13.8716 | -2.60561 | 0.011329 | -0.62129 | -24.375 | -3.34772 |
| EC012 | ec012ec.375 | MVL-Ozkurt | ozkurt_mvl | 37 | 32 | 0.173599 | 0.142871 | 0.0307282 | 3.23558 | 0.00190482 | 0.772535 | 0.0125282 | 0.0489397 |
| EC012 | ec012ec.375 | MVL-raw | fP_hz | 37 | 32 | 6.10811 | 6 | 0.108108 | 0.201615 | 0.840829 | 0.0476217 | -0.93675 | 1.15375 |
| EC012 | ec012ec.375 | MVL-raw | fA_hz | 37 | 32 | 87.5676 | 86.5 | 1.06757 | 0.394624 | 0.694416 | 0.094446 | -4.36495 | 6.15211 |
| EC012 | ec012ec.375 | MVL-raw | ozkurt_mvl | 37 | 32 | 0.161076 | 0.124054 | 0.0370214 | 4.3474 | 5.36932e-05 | 1.05188 | 0.020402 | 0.0531211 |
| EC012 | ec012ec.444 | APC-v1.0 | fP_hz | 30 | 40 | 8.79962 | 6.18906 | 2.61056 | 15.8933 | 2.71808e-19 | 3.30592 | 2.31498 | 2.94404 |
| EC012 | ec012ec.444 | APC-v1.0 | fA_hz | 30 | 40 | 110.1 | 111.5 | -1.4 | -0.319666 | 0.7503 | -0.07662 | -9.80729 | 7.055 |
| EC012 | ec012ec.444 | APC-v1.0 | ozkurt_mvl | 30 | 40 | 0.0999886 | 0.0800946 | 0.019894 | 2.84552 | 0.00589164 | 0.666442 | 0.00665533 | 0.0332326 |
| EC012 | ec012ec.444 | GLM | fP_hz | 30 | 46 | 7.48333 | 6.47826 | 1.00507 | 2.09723 | 0.040277 | 0.494739 | 0.0601449 | 1.91739 |
| EC012 | ec012ec.444 | GLM | fA_hz | 30 | 46 | 110.133 | 106.87 | 3.26377 | 0.645087 | 0.521259 | 0.150087 | -6.19159 | 13.0668 |
| EC012 | ec012ec.444 | GLM | ozkurt_mvl | 30 | 46 | 0.128936 | 0.123947 | 0.00498929 | 0.658208 | 0.51347 | 0.16285 | -0.0105619 | 0.0188213 |
| EC012 | ec012ec.444 | KLMI | fP_hz | 30 | 46 | 5.76667 | 5.11957 | 0.647101 | 1.55666 | 0.126244 | 0.389651 | -0.131214 | 1.47029 |
| EC012 | ec012ec.444 | KLMI | fA_hz | 30 | 46 | 107.333 | 109.913 | -2.57971 | -0.523063 | 0.602622 | -0.117731 | -12.0465 | 7.07841 |
| EC012 | ec012ec.444 | KLMI | ozkurt_mvl | 30 | 46 | 0.123678 | 0.117864 | 0.00581404 | 0.486706 | 0.628752 | 0.12224 | -0.0178497 | 0.0288553 |
| EC012 | ec012ec.444 | MVL-Ozkurt | fP_hz | 30 | 46 | 6.03333 | 5.67391 | 0.35942 | 0.693477 | 0.49104 | 0.168322 | -0.615942 | 1.37685 |
| EC012 | ec012ec.444 | MVL-Ozkurt | fA_hz | 30 | 46 | 114.267 | 115.826 | -1.55942 | -0.28149 | 0.779276 | -0.065515 | -12.3248 | 9.35725 |
| EC012 | ec012ec.444 | MVL-Ozkurt | ozkurt_mvl | 30 | 46 | 0.176741 | 0.145673 | 0.0310674 | 4.26936 | 9.87357e-05 | 1.07917 | 0.0175366 | 0.0460034 |
| EC012 | ec012ec.444 | MVL-raw | fP_hz | 30 | 46 | 6.03333 | 6.51087 | -0.477536 | -0.850097 | 0.398559 | -0.197886 | -1.55942 | 0.603623 |
| EC012 | ec012ec.444 | MVL-raw | fA_hz | 30 | 46 | 86.4 | 85.8261 | 0.573913 | 0.284128 | 0.777276 | 0.0663909 | -3.26971 | 4.52768 |
| EC012 | ec012ec.444 | MVL-raw | ozkurt_mvl | 30 | 46 | 0.161468 | 0.128428 | 0.0330394 | 3.88771 | 0.00032476 | 0.98056 | 0.0169775 | 0.0504754 |
| EC013 | ec013.156 | APC-v1.0 | fP_hz | 56 | 55 | 7.47891 | 6.62178 | 0.857135 | 7.82757 | 6.42744e-11 | 1.48684 | 0.624125 | 1.04918 |
| EC013 | ec013.156 | APC-v1.0 | fA_hz | 56 | 55 | 111.893 | 107.509 | 4.38377 | 1.27251 | 0.205941 | 0.240131 | -2.30294 | 11.1527 |
| EC013 | ec013.156 | APC-v1.0 | ozkurt_mvl | 56 | 55 | 0.10208 | 0.0690309 | 0.0330491 | 7.34773 | 4.32767e-11 | 1.38303 | 0.024418 | 0.0420508 |
| EC013 | ec013.156 | GLM | fP_hz | 56 | 56 | 7.45536 | 6.47321 | 0.982143 | 3.61497 | 0.000456691 | 0.678494 | 0.455357 | 1.5 |
| EC013 | ec013.156 | GLM | fA_hz | 56 | 56 | 106.714 | 106.143 | 0.571429 | 0.156386 | 0.876034 | 0.0293522 | -6.5 | 7.64286 |
| EC013 | ec013.156 | GLM | ozkurt_mvl | 56 | 56 | 0.126 | 0.0947463 | 0.0312533 | 6.64208 | 1.24917e-09 | 1.24665 | 0.0221454 | 0.0406209 |
| EC013 | ec013.156 | KLMI | fP_hz | 56 | 56 | 6.5625 | 5.58929 | 0.973214 | 3.21584 | 0.0017219 | 0.603581 | 0.401786 | 1.55357 |
| EC013 | ec013.156 | KLMI | fA_hz | 56 | 56 | 100.214 | 102.214 | -2 | -0.597798 | 0.551286 | -0.112201 | -8.28571 | 4.57143 |
| EC013 | ec013.156 | KLMI | ozkurt_mvl | 56 | 56 | 0.122102 | 0.0874174 | 0.0346843 | 5.34327 | 5.32909e-07 | 1.00288 | 0.0219156 | 0.0473205 |
| EC013 | ec013.156 | MVL-Ozkurt | fP_hz | 56 | 56 | 6.00893 | 5.75893 | 0.25 | 0.77111 | 0.442357 | 0.14473 | -0.375 | 0.883929 |
| EC013 | ec013.156 | MVL-Ozkurt | fA_hz | 56 | 56 | 108.714 | 105.5 | 3.21429 | 0.771737 | 0.441925 | 0.144848 | -4.85714 | 11.2143 |
| EC013 | ec013.156 | MVL-Ozkurt | ozkurt_mvl | 56 | 56 | 0.148987 | 0.107328 | 0.041659 | 7.00853 | 2.0657e-10 | 1.31543 | 0.02989 | 0.0532773 |
| EC013 | ec013.156 | MVL-raw | fP_hz | 56 | 56 | 6.14286 | 5.98214 | 0.160714 | 0.470519 | 0.638957 | 0.0883119 | -0.5 | 0.839286 |
| EC013 | ec013.156 | MVL-raw | fA_hz | 56 | 56 | 89.8571 | 84 | 5.85714 | 3.41602 | 0.000967256 | 0.641154 | 2.57143 | 9.28571 |
| EC013 | ec013.156 | MVL-raw | ozkurt_mvl | 56 | 56 | 0.139322 | 0.095371 | 0.0439512 | 7.58052 | 1.37707e-11 | 1.42279 | 0.0325899 | 0.055363 |
| EC013 | ec013.157 | APC-v1.0 | fP_hz | 23 | 33 | 7.48778 | 6.39249 | 1.0953 | 6.03144 | 4.28443e-07 | 1.38749 | 0.763439 | 1.45808 |
| EC013 | ec013.157 | APC-v1.0 | fA_hz | 23 | 33 | 106.043 | 110.242 | -4.19895 | -0.884247 | 0.380598 | -0.228617 | -13.3084 | 4.9447 |
| EC013 | ec013.157 | APC-v1.0 | ozkurt_mvl | 23 | 33 | 0.0925617 | 0.0760436 | 0.0165181 | 2.18593 | 0.0341357 | 0.595983 | 0.00206991 | 0.0314695 |
| EC013 | ec013.157 | GLM | fP_hz | 23 | 33 | 7.63043 | 5.98485 | 1.64559 | 3.96371 | 0.000279071 | 1.09373 | 0.839262 | 2.4526 |
| EC013 | ec013.157 | GLM | fA_hz | 23 | 33 | 109.565 | 108 | 1.56522 | 0.288767 | 0.773953 | 0.0761186 | -8.54282 | 11.9107 |
| EC013 | ec013.157 | GLM | ozkurt_mvl | 23 | 33 | 0.124122 | 0.113172 | 0.0109493 | 1.4581 | 0.150646 | 0.361329 | -0.00374717 | 0.0248839 |
| EC013 | ec013.157 | KLMI | fP_hz | 23 | 33 | 6.5 | 5.5303 | 0.969697 | 2.48251 | 0.0173005 | 0.692422 | 0.20751 | 1.72467 |
| EC013 | ec013.157 | KLMI | fA_hz | 23 | 33 | 106.957 | 106.667 | 0.289855 | 0.0600706 | 0.952337 | 0.0157899 | -9.11739 | 9.43386 |
| EC013 | ec013.157 | KLMI | ozkurt_mvl | 23 | 33 | 0.124848 | 0.105748 | 0.0190998 | 1.87477 | 0.0663006 | 0.479489 | -0.00142155 | 0.0382596 |
| EC013 | ec013.157 | MVL-Ozkurt | fP_hz | 23 | 33 | 6.19565 | 5.09091 | 1.10474 | 2.50339 | 0.017224 | 0.724434 | 0.264806 | 1.96313 |
| EC013 | ec013.157 | MVL-Ozkurt | fA_hz | 23 | 33 | 103.304 | 101.333 | 1.97101 | 0.477198 | 0.635319 | 0.126183 | -6.20817 | 10.008 |
| EC013 | ec013.157 | MVL-Ozkurt | ozkurt_mvl | 23 | 33 | 0.153976 | 0.126765 | 0.027211 | 2.47475 | 0.0167261 | 0.649652 | 0.00650751 | 0.0491823 |
| EC013 | ec013.157 | MVL-raw | fP_hz | 23 | 33 | 5.93478 | 5.56061 | 0.374177 | 0.783885 | 0.437009 | 0.210096 | -0.535573 | 1.29119 |
| EC013 | ec013.157 | MVL-raw | fA_hz | 23 | 33 | 89.5652 | 87.1515 | 2.4137 | 1.01896 | 0.313775 | 0.278209 | -2.11331 | 7.04625 |
| EC013 | ec013.157 | MVL-raw | ozkurt_mvl | 23 | 33 | 0.143713 | 0.116753 | 0.0269596 | 2.40389 | 0.0204 | 0.653132 | 0.00606361 | 0.0497191 |
| EC013 | ec013.205 | APC-v1.0 | fP_hz | 8 | 9 | 7.62236 | 6.19203 | 1.43033 | 9.84539 | 2.32042e-07 | 4.39589 | 1.17523 | 1.70363 |
| EC013 | ec013.205 | APC-v1.0 | fA_hz | 8 | 9 | 110.125 | 107.556 | 2.56944 | 0.339767 | 0.738777 | 0.156294 | -11.2229 | 16.4448 |
| EC013 | ec013.205 | APC-v1.0 | ozkurt_mvl | 8 | 9 | 0.136338 | 0.101129 | 0.0352096 | 2.19327 | 0.0478378 | 0.976941 | 0.00386892 | 0.062675 |
| EC013 | ec013.205 | GLM | fP_hz | 8 | 9 | 7.75 | 5.88889 | 1.86111 | 3.12098 | 0.00778969 | 1.39955 | 0.763889 | 2.90972 |
| EC013 | ec013.205 | GLM | fA_hz | 8 | 9 | 102.5 | 92 | 10.5 | 1.53868 | 0.145301 | 0.711514 | -1.77778 | 23.1694 |
| EC013 | ec013.205 | GLM | ozkurt_mvl | 8 | 9 | 0.171477 | 0.133727 | 0.0377499 | 2.4162 | 0.0326662 | 1.0723 | 0.00737743 | 0.0654384 |
| EC013 | ec013.205 | KLMI | fP_hz | 8 | 9 | 7.6875 | 5.88889 | 1.79861 | 3.08837 | 0.0084432 | 1.38273 | 0.722222 | 2.83333 |
| EC013 | ec013.205 | KLMI | fA_hz | 8 | 9 | 103.5 | 105.333 | -1.83333 | -0.193357 | 0.849324 | -0.0877116 | -18.9458 | 15.5 |
| EC013 | ec013.205 | KLMI | ozkurt_mvl | 8 | 9 | 0.173036 | 0.127376 | 0.0456604 | 3.52719 | 0.0032749 | 1.59109 | 0.0221983 | 0.0694989 |
| EC013 | ec013.205 | MVL-Ozkurt | fP_hz | 8 | 9 | 6.5625 | 5.27778 | 1.28472 | 1.50378 | 0.15446 | 0.697933 | -0.305556 | 2.79861 |
| EC013 | ec013.205 | MVL-Ozkurt | fA_hz | 8 | 9 | 100 | 89.3333 | 10.6667 | 1.60114 | 0.133591 | 0.751726 | -1.27778 | 23.1111 |
| EC013 | ec013.205 | MVL-Ozkurt | ozkurt_mvl | 8 | 9 | 0.179092 | 0.140606 | 0.0384854 | 2.37036 | 0.035489 | 1.05202 | 0.00747917 | 0.0676347 |
| EC013 | ec013.205 | MVL-raw | fP_hz | 8 | 9 | 6.5625 | 5.22222 | 1.34028 | 1.6156 | 0.128844 | 0.753214 | -0.194444 | 2.80556 |
| EC013 | ec013.205 | MVL-raw | fA_hz | 8 | 9 | 91 | 84.4444 | 6.55556 | 1.43683 | 0.171759 | 0.663637 | -2.5 | 14.2222 |
| EC013 | ec013.205 | MVL-raw | ozkurt_mvl | 8 | 9 | 0.176294 | 0.137341 | 0.0389522 | 2.31433 | 0.0394914 | 1.0264 | 0.00714584 | 0.0693439 |
| EC013 | ec013.206 | APC-v1.0 | fP_hz | 58 | 61 | 7.49993 | 6.44493 | 1.055 | 14.649 | 2.61755e-23 | 2.61409 | 0.911805 | 1.18982 |
| EC013 | ec013.206 | APC-v1.0 | fA_hz | 58 | 61 | 114.448 | 111.213 | 3.23516 | 1.08447 | 0.280388 | 0.197261 | -2.50368 | 9.01139 |
| EC013 | ec013.206 | APC-v1.0 | ozkurt_mvl | 58 | 61 | 0.115285 | 0.0948074 | 0.0204776 | 4.2829 | 3.81051e-05 | 0.78062 | 0.0112101 | 0.0295551 |
| EC013 | ec013.206 | GLM | fP_hz | 58 | 61 | 7.61207 | 6.57377 | 1.0383 | 4.78747 | 5.2402e-06 | 0.866244 | 0.618273 | 1.45591 |
| EC013 | ec013.206 | GLM | fA_hz | 58 | 61 | 112.276 | 104.525 | 7.75127 | 2.42833 | 0.016708 | 0.440751 | 1.34751 | 13.8894 |
| EC013 | ec013.206 | GLM | ozkurt_mvl | 58 | 61 | 0.150365 | 0.116643 | 0.0337223 | 7.84641 | 2.51543e-12 | 1.42226 | 0.0254183 | 0.0419517 |
| EC013 | ec013.206 | KLMI | fP_hz | 58 | 61 | 7.2069 | 5.86885 | 1.33804 | 5.24027 | 7.21274e-07 | 0.952415 | 0.824311 | 1.80767 |
| EC013 | ec013.206 | KLMI | fA_hz | 58 | 61 | 110.345 | 105.574 | 4.77106 | 1.46783 | 0.14486 | 0.266445 | -1.47207 | 11.1126 |
| EC013 | ec013.206 | KLMI | ozkurt_mvl | 58 | 61 | 0.147093 | 0.113448 | 0.0336452 | 5.94578 | 3.00329e-08 | 1.08538 | 0.0228073 | 0.0447151 |
| EC013 | ec013.206 | MVL-Ozkurt | fP_hz | 58 | 61 | 6.59483 | 5.91803 | 0.676795 | 2.30589 | 0.0230082 | 0.422543 | 0.0967425 | 1.23361 |
| EC013 | ec013.206 | MVL-Ozkurt | fA_hz | 58 | 61 | 110.069 | 107.541 | 2.52798 | 0.727855 | 0.468166 | 0.132729 | -4.13567 | 9.27897 |
| EC013 | ec013.206 | MVL-Ozkurt | ozkurt_mvl | 58 | 61 | 0.165005 | 0.127421 | 0.0375841 | 7.08787 | 1.35158e-10 | 1.29786 | 0.0275186 | 0.0480637 |
| EC013 | ec013.206 | MVL-raw | fP_hz | 58 | 61 | 6.5 | 6.01639 | 0.483607 | 1.53295 | 0.128026 | 0.279825 | -0.149113 | 1.08565 |
| EC013 | ec013.206 | MVL-raw | fA_hz | 58 | 61 | 91.1724 | 84.3279 | 6.84454 | 3.82036 | 0.00021923 | 0.699022 | 3.27072 | 10.38 |
| EC013 | ec013.206 | MVL-raw | ozkurt_mvl | 58 | 61 | 0.152825 | 0.112723 | 0.0401028 | 7.49703 | 1.46904e-11 | 1.36885 | 0.0297454 | 0.0503679 |
| EC013 | ec013.208 | APC-v1.0 | fP_hz | 44 | 52 | 7.5064 | 6.44779 | 1.0586 | 9.31434 | 6.56656e-14 | 1.78356 | 0.844102 | 1.2932 |
| EC013 | ec013.208 | APC-v1.0 | fA_hz | 44 | 52 | 112.795 | 112 | 0.795455 | 0.24612 | 0.806132 | 0.048882 | -5.49665 | 7.19784 |
| EC013 | ec013.208 | APC-v1.0 | ozkurt_mvl | 44 | 52 | 0.123943 | 0.0922372 | 0.0317053 | 6.31611 | 8.85279e-09 | 1.26302 | 0.0217066 | 0.0413351 |
| EC013 | ec013.208 | GLM | fP_hz | 44 | 53 | 7.78409 | 6.60377 | 1.18032 | 4.52735 | 1.89548e-05 | 0.875667 | 0.67217 | 1.68354 |
| EC013 | ec013.208 | GLM | fA_hz | 44 | 53 | 112.455 | 107.774 | 4.68096 | 1.2496 | 0.214637 | 0.244084 | -2.58666 | 11.8835 |
| EC013 | ec013.208 | GLM | ozkurt_mvl | 44 | 53 | 0.148968 | 0.131667 | 0.0173007 | 3.16977 | 0.00208566 | 0.617131 | 0.00636598 | 0.0278814 |
| EC013 | ec013.208 | KLMI | fP_hz | 44 | 53 | 7.52273 | 5.58491 | 1.93782 | 6.50545 | 3.60882e-09 | 1.29352 | 1.34475 | 2.49937 |
| EC013 | ec013.208 | KLMI | fA_hz | 44 | 53 | 114.455 | 109.358 | 5.09605 | 1.33689 | 0.18449 | 0.263226 | -2.24207 | 12.5457 |
| EC013 | ec013.208 | KLMI | ozkurt_mvl | 44 | 53 | 0.15034 | 0.125504 | 0.0248355 | 3.90744 | 0.000179851 | 0.761459 | 0.0123361 | 0.0370096 |
| EC013 | ec013.208 | MVL-Ozkurt | fP_hz | 44 | 53 | 6.18182 | 5.75472 | 0.427101 | 1.13449 | 0.259579 | 0.230202 | -0.311985 | 1.15288 |
| EC013 | ec013.208 | MVL-Ozkurt | fA_hz | 44 | 53 | 112.455 | 112.83 | -0.375643 | -0.0898568 | 0.928591 | -0.0177777 | -8.37607 | 7.772 |
| EC013 | ec013.208 | MVL-Ozkurt | ozkurt_mvl | 44 | 53 | 0.168931 | 0.146771 | 0.0221605 | 3.22113 | 0.00177086 | 0.652827 | 0.00887814 | 0.0359761 |
| EC013 | ec013.208 | MVL-raw | fP_hz | 44 | 53 | 5.59091 | 6.24528 | -0.654374 | -1.82963 | 0.0704685 | -0.366885 | -1.33449 | 0.033244 |
| EC013 | ec013.208 | MVL-raw | fA_hz | 44 | 53 | 93.9091 | 85.434 | 8.47513 | 3.8799 | 0.00021719 | 0.806602 | 4.2229 | 12.6656 |
| EC013 | ec013.208 | MVL-raw | ozkurt_mvl | 44 | 53 | 0.157605 | 0.130987 | 0.0266177 | 3.98902 | 0.000131947 | 0.803337 | 0.0136525 | 0.0397497 |
| EC013 | ec013.251 | APC-v1.0 | fP_hz | 54 | 59 | 7.73873 | 6.54808 | 1.19065 | 11.6165 | 1.80353e-18 | 2.10123 | 0.992035 | 1.39086 |
| EC013 | ec013.251 | APC-v1.0 | fA_hz | 54 | 59 | 111.889 | 114.169 | -2.2806 | -0.662799 | 0.508863 | -0.12269 | -8.85284 | 4.44387 |
| EC013 | ec013.251 | APC-v1.0 | ozkurt_mvl | 54 | 59 | 0.127638 | 0.0875925 | 0.040046 | 6.59662 | 1.54042e-09 | 1.22288 | 0.0281543 | 0.0519403 |
| EC013 | ec013.251 | GLM | fP_hz | 54 | 65 | 7.88889 | 6.28462 | 1.60427 | 6.8163 | 4.36211e-10 | 1.2321 | 1.14415 | 2.06168 |
| EC013 | ec013.251 | GLM | fA_hz | 54 | 65 | 108.148 | 106.892 | 1.25584 | 0.338833 | 0.735345 | 0.0605928 | -5.92034 | 8.41368 |
| EC013 | ec013.251 | GLM | ozkurt_mvl | 54 | 65 | 0.159448 | 0.120263 | 0.0391852 | 8.25218 | 3.02317e-13 | 1.46358 | 0.0296064 | 0.0483291 |
| EC013 | ec013.251 | KLMI | fP_hz | 54 | 65 | 7.40741 | 5.72308 | 1.68433 | 5.73503 | 9.71614e-08 | 1.06656 | 1.08873 | 2.24545 |
| EC013 | ec013.251 | KLMI | fA_hz | 54 | 65 | 108.519 | 107.938 | 0.580057 | 0.162649 | 0.871076 | 0.0291672 | -6.33276 | 7.35866 |
| EC013 | ec013.251 | KLMI | ozkurt_mvl | 54 | 65 | 0.166388 | 0.116941 | 0.0494463 | 8.1319 | 5.10381e-13 | 1.4703 | 0.0377185 | 0.0615653 |
| EC013 | ec013.251 | MVL-Ozkurt | fP_hz | 54 | 65 | 6.59259 | 5.70769 | 0.8849 | 2.5967 | 0.0107966 | 0.483751 | 0.220345 | 1.52921 |
| EC013 | ec013.251 | MVL-Ozkurt | fA_hz | 54 | 65 | 110.815 | 106.646 | 4.16866 | 1.1099 | 0.269321 | 0.200395 | -3.17721 | 11.5363 |
| EC013 | ec013.251 | MVL-Ozkurt | ozkurt_mvl | 54 | 65 | 0.179336 | 0.137677 | 0.0416588 | 7.16609 | 8.87454e-11 | 1.31532 | 0.0306337 | 0.0533157 |
| EC013 | ec013.251 | MVL-raw | fP_hz | 54 | 65 | 6.85185 | 5.73077 | 1.12108 | 3.40975 | 0.000934126 | 0.636022 | 0.479341 | 1.74987 |
| EC013 | ec013.251 | MVL-raw | fA_hz | 54 | 65 | 92.0741 | 85.2308 | 6.8433 | 3.73071 | 0.00033583 | 0.707787 | 3.429 | 10.4456 |
| EC013 | ec013.251 | MVL-raw | ozkurt_mvl | 54 | 65 | 0.168551 | 0.123533 | 0.0450178 | 7.44777 | 2.64725e-11 | 1.37975 | 0.0335856 | 0.0569216 |
| EC013 | ec013.252 | APC-v1.0 | fP_hz | 32 | 59 | 7.7434 | 6.63941 | 1.10398 | 9.90582 | 6.15156e-16 | 1.76954 | 0.888606 | 1.32231 |
| EC013 | ec013.252 | APC-v1.0 | fA_hz | 32 | 59 | 110.938 | 111.051 | -0.113347 | -0.0319304 | 0.974613 | -0.00657876 | -6.87509 | 6.79423 |
| EC013 | ec013.252 | APC-v1.0 | ozkurt_mvl | 32 | 59 | 0.117712 | 0.0961698 | 0.0215421 | 3.55284 | 0.000625226 | 0.690023 | 0.00959764 | 0.0333085 |
| EC013 | ec013.252 | GLM | fP_hz | 32 | 64 | 7.98438 | 6.65625 | 1.32812 | 4.99616 | 2.9161e-06 | 0.928701 | 0.828125 | 1.83594 |
| EC013 | ec013.252 | GLM | fA_hz | 32 | 64 | 107.375 | 106 | 1.375 | 0.384132 | 0.702002 | 0.0777914 | -5.5 | 8.25 |
| EC013 | ec013.252 | GLM | ozkurt_mvl | 32 | 64 | 0.15576 | 0.126398 | 0.0293622 | 4.96421 | 3.87141e-06 | 0.971715 | 0.0176465 | 0.0407981 |
| EC013 | ec013.252 | KLMI | fP_hz | 32 | 64 | 7.03125 | 5.57812 | 1.45312 | 4.06676 | 0.000148557 | 0.903872 | 0.773438 | 2.13281 |
| EC013 | ec013.252 | KLMI | fA_hz | 32 | 64 | 107 | 105.188 | 1.8125 | 0.515847 | 0.607467 | 0.10291 | -5.0625 | 8.75 |
| EC013 | ec013.252 | KLMI | ozkurt_mvl | 32 | 64 | 0.14979 | 0.125696 | 0.0240936 | 2.61361 | 0.0110659 | 0.54685 | 0.00588727 | 0.0413837 |
| EC013 | ec013.252 | MVL-Ozkurt | fP_hz | 32 | 64 | 6 | 5.36719 | 0.632812 | 1.60936 | 0.114035 | 0.381794 | -0.101562 | 1.39844 |
| EC013 | ec013.252 | MVL-Ozkurt | fA_hz | 32 | 64 | 116 | 102.812 | 13.1875 | 3.22083 | 0.00195505 | 0.666499 | 5.25 | 21 |
| EC013 | ec013.252 | MVL-Ozkurt | ozkurt_mvl | 32 | 64 | 0.184252 | 0.151586 | 0.0326659 | 4.222 | 6.74009e-05 | 0.845909 | 0.0177998 | 0.0478082 |
| EC013 | ec013.252 | MVL-raw | fP_hz | 32 | 64 | 6.17188 | 5.70312 | 0.46875 | 1.1563 | 0.252461 | 0.258288 | -0.320312 | 1.25781 |
| EC013 | ec013.252 | MVL-raw | fA_hz | 32 | 64 | 94.375 | 85 | 9.375 | 3.9404 | 0.000310352 | 1.01244 | 4.9375 | 14.25 |
| EC013 | ec013.252 | MVL-raw | ozkurt_mvl | 32 | 64 | 0.169505 | 0.136368 | 0.033137 | 4.38563 | 3.73004e-05 | 0.878668 | 0.0187223 | 0.0478855 |
| EC013 | ec013.374 | APC-v1.0 | fP_hz | 88 | 75 | 7.3766 | 6.43311 | 0.943491 | 9.9788 | 2.41293e-16 | 1.65707 | 0.766423 | 1.13157 |
| EC013 | ec013.374 | APC-v1.0 | fA_hz | 88 | 75 | 109.773 | 111.987 | -2.21394 | -0.791342 | 0.430099 | -0.126277 | -7.72455 | 3.27229 |
| EC013 | ec013.374 | APC-v1.0 | ozkurt_mvl | 88 | 75 | 0.117387 | 0.0790082 | 0.0383784 | 8.79402 | 2.93805e-15 | 1.38502 | 0.0296418 | 0.0468113 |
| EC013 | ec013.374 | GLM | fP_hz | 88 | 77 | 7.38068 | 6.47403 | 0.906656 | 4.04688 | 8.7329e-05 | 0.643153 | 0.461851 | 1.34093 |
| EC013 | ec013.374 | GLM | fA_hz | 88 | 77 | 109.5 | 108.623 | 0.876623 | 0.323542 | 0.746765 | 0.0511673 | -4.52614 | 6.09091 |
| EC013 | ec013.374 | GLM | ozkurt_mvl | 88 | 77 | 0.143714 | 0.11184 | 0.0318742 | 8.26337 | 6.81949e-14 | 1.29708 | 0.024318 | 0.0394151 |
| EC013 | ec013.374 | KLMI | fP_hz | 88 | 77 | 7.02273 | 5.48052 | 1.54221 | 7.04073 | 5.17389e-11 | 1.09021 | 1.10714 | 1.97403 |
| EC013 | ec013.374 | KLMI | fA_hz | 88 | 77 | 109.545 | 110.13 | -0.584416 | -0.203878 | 0.838755 | -0.0323606 | -6.08458 | 5.03896 |
| EC013 | ec013.374 | KLMI | ozkurt_mvl | 88 | 77 | 0.141193 | 0.111018 | 0.0301753 | 6.17136 | 5.67238e-09 | 0.964755 | 0.0204627 | 0.0397574 |
| EC013 | ec013.374 | MVL-Ozkurt | fP_hz | 88 | 77 | 6.10795 | 5.62987 | 0.478084 | 1.83864 | 0.0677926 | 0.282077 | -0.0186688 | 0.998377 |
| EC013 | ec013.374 | MVL-Ozkurt | fA_hz | 88 | 77 | 110.545 | 108.208 | 2.33766 | 0.799028 | 0.425521 | 0.125249 | -3.36364 | 8.07808 |
| EC013 | ec013.374 | MVL-Ozkurt | ozkurt_mvl | 88 | 77 | 0.162042 | 0.128893 | 0.0331496 | 8.08655 | 1.3333e-13 | 1.24119 | 0.0250671 | 0.0412048 |
| EC013 | ec013.374 | MVL-raw | fP_hz | 88 | 77 | 5.97727 | 5.68831 | 0.288961 | 1.10299 | 0.2717 | 0.171689 | -0.219968 | 0.79791 |
| EC013 | ec013.374 | MVL-raw | fA_hz | 88 | 77 | 97.0909 | 85.7143 | 11.3766 | 6.95591 | 1.08665e-10 | 1.04764 | 8.17516 | 14.5584 |
| EC013 | ec013.374 | MVL-raw | ozkurt_mvl | 88 | 77 | 0.155303 | 0.114203 | 0.0410993 | 9.79376 | 4.24719e-18 | 1.50945 | 0.0327132 | 0.0492289 |
| EC013 | ec013.375 | APC-v1.0 | fP_hz | 68 | 130 | 7.51764 | 6.24126 | 1.27638 | 9.83479 | 4.31707e-18 | 1.103 | 1.03256 | 1.53744 |
| EC013 | ec013.375 | APC-v1.0 | fA_hz | 68 | 130 | 109.426 | 111.038 | -1.61199 | -0.641156 | 0.522326 | -0.0896495 | -6.44272 | 3.29378 |
| EC013 | ec013.375 | APC-v1.0 | ozkurt_mvl | 68 | 130 | 0.114472 | 0.0888307 | 0.0256416 | 5.93234 | 1.69745e-08 | 0.823054 | 0.0169965 | 0.033633 |
| EC013 | ec013.375 | GLM | fP_hz | 68 | 137 | 7.61765 | 6.12774 | 1.48991 | 7.62645 | 1.08115e-12 | 0.970837 | 1.10457 | 1.86426 |
| EC013 | ec013.375 | GLM | fA_hz | 68 | 137 | 109.765 | 110.453 | -0.687849 | -0.233795 | 0.815442 | -0.032272 | -6.44704 | 5.04238 |
| EC013 | ec013.375 | GLM | ozkurt_mvl | 68 | 137 | 0.142157 | 0.116122 | 0.0260347 | 6.20243 | 3.0784e-09 | 0.754685 | 0.0176239 | 0.0341469 |
| EC013 | ec013.375 | KLMI | fP_hz | 68 | 137 | 6.88235 | 5.41241 | 1.46994 | 6.61046 | 9.86434e-10 | 1.00101 | 1.03338 | 1.88499 |
| EC013 | ec013.375 | KLMI | fA_hz | 68 | 137 | 106.471 | 108.204 | -1.73379 | -0.64726 | 0.51834 | -0.0874463 | -7.01399 | 3.45818 |
| EC013 | ec013.375 | KLMI | ozkurt_mvl | 68 | 137 | 0.14811 | 0.11381 | 0.0342995 | 7.14433 | 1.84149e-11 | 0.912085 | 0.0247898 | 0.0436218 |
| EC013 | ec013.375 | MVL-Ozkurt | fP_hz | 68 | 137 | 6.36029 | 5.71898 | 0.641316 | 2.56939 | 0.0112975 | 0.381522 | 0.156128 | 1.11597 |
| EC013 | ec013.375 | MVL-Ozkurt | fA_hz | 68 | 137 | 104.294 | 108.964 | -4.66939 | -1.61509 | 0.108318 | -0.225629 | -10.2783 | 1.15348 |
| EC013 | ec013.375 | MVL-Ozkurt | ozkurt_mvl | 68 | 137 | 0.161639 | 0.133472 | 0.0281679 | 5.64211 | 7.5508e-08 | 0.782514 | 0.0187416 | 0.0380184 |
| EC013 | ec013.375 | MVL-raw | fP_hz | 68 | 137 | 5.96324 | 5.86861 | 0.0946222 | 0.361235 | 0.718533 | 0.0547757 | -0.417108 | 0.592218 |
| EC013 | ec013.375 | MVL-raw | fA_hz | 68 | 137 | 91.6471 | 86.3358 | 5.31129 | 3.37615 | 0.00102442 | 0.544848 | 2.31329 | 8.30277 |
| EC013 | ec013.375 | MVL-raw | ozkurt_mvl | 68 | 137 | 0.154271 | 0.120874 | 0.0333971 | 7.33522 | 9.55663e-12 | 1.00239 | 0.0246131 | 0.0422089 |

POST HOC across-session table:
| animal_pool | method | outcome | n_sessions | mean_session_difference | median_session_difference | ci_low | ci_high | one_sample_t | one_sample_p | wilcoxon_statistic | wilcoxon_p | zero_differences |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EC012 | APC-v1.0 | fA_hz | 9 | -4.23743 | -1.89357 | -9.41275 | 0.937879 | -1.88811 | 0.0957045 | 9 | 0.128906 | 0 |
| EC013 | APC-v1.0 | fA_hz | 9 | 0.0627778 | -0.113347 | -2.1655 | 2.29106 | 0.0649675 | 0.949794 | 21 | 0.910156 | 0 |
| pooled | APC-v1.0 | fA_hz | 18 | -2.08733 | -1.506 | -4.81933 | 0.64467 | -1.61196 | 0.125379 | 60 | 0.28373 | 0 |
| EC012 | APC-v1.0 | fP_hz | 9 | 2.59773 | 2.61056 | 2.34234 | 2.85313 | 23.4552 | 1.16072e-08 | 0 | 0.00390625 | 0 |
| EC013 | APC-v1.0 | fP_hz | 9 | 1.11232 | 1.0953 | 0.980762 | 1.24388 | 19.4973 | 4.97577e-08 | 0 | 0.00390625 | 0 |
| pooled | APC-v1.0 | fP_hz | 18 | 1.85503 | 1.75316 | 1.45416 | 2.25589 | 9.76332 | 2.19699e-08 | 0 | 7.62939e-06 | 0 |
| EC012 | APC-v1.0 | ozkurt_mvl | 9 | 0.0126623 | 0.0159988 | 0.00430612 | 0.0210184 | 3.49434 | 0.00814637 | 0 | 0.00390625 | 0 |
| EC013 | APC-v1.0 | ozkurt_mvl | 9 | 0.0291742 | 0.0317053 | 0.0227013 | 0.0356471 | 10.3935 | 6.35868e-06 | 0 | 0.00390625 | 0 |
| pooled | APC-v1.0 | ozkurt_mvl | 18 | 0.0209182 | 0.0210098 | 0.0146053 | 0.0272311 | 6.99103 | 2.1738e-06 | 0 | 7.62939e-06 | 0 |
| EC012 | GLM | fA_hz | 9 | 0.126673 | 2.44595 | -3.38446 | 3.6378 | 0.0831948 | 0.935741 | 22 | 1 | 0 |
| EC013 | GLM | fA_hz | 9 | 3.09872 | 1.375 | 0.205849 | 5.99159 | 2.47009 | 0.0387049 | 2 | 0.0117188 | 0 |
| pooled | GLM | fA_hz | 18 | 1.6127 | 1.47011 | -0.54477 | 3.77016 | 1.57708 | 0.133203 | 50 | 0.129738 | 0 |
| EC012 | GLM | fP_hz | 9 | 1.0096 | 1.21453 | 0.560536 | 1.45866 | 5.18445 | 0.000838175 | 0 | 0.00390625 | 0 |
| EC013 | GLM | fP_hz | 9 | 1.33738 | 1.32812 | 1.08104 | 1.59372 | 12.0309 | 2.10225e-06 | 0 | 0.00390625 | 0 |
| pooled | GLM | fP_hz | 18 | 1.17349 | 1.26101 | 0.929165 | 1.41781 | 10.1335 | 1.27435e-08 | 0 | 7.62939e-06 | 0 |
| EC012 | GLM | ozkurt_mvl | 9 | 0.0105205 | 0.0130797 | 0.000284705 | 0.0207563 | 2.37014 | 0.0452362 | 5 | 0.0390625 | 0 |
| EC013 | GLM | ozkurt_mvl | 9 | 0.0286035 | 0.0312533 | 0.0214848 | 0.0357223 | 9.26566 | 1.49557e-05 | 0 | 0.00390625 | 0 |
| pooled | GLM | ozkurt_mvl | 18 | 0.019562 | 0.0181955 | 0.0123493 | 0.0267747 | 5.72219 | 2.4916e-05 | 5 | 7.62939e-05 | 0 |
| EC012 | KLMI | fA_hz | 9 | 2.59734 | 1.08 | -2.91838 | 8.11306 | 1.08589 | 0.30916 | 17 | 0.570312 | 0 |
| EC013 | KLMI | fA_hz | 9 | 0.710887 | 0.289855 | -1.36947 | 2.79125 | 0.787993 | 0.453414 | 20 | 0.820312 | 0 |
| pooled | KLMI | fA_hz | 18 | 1.65411 | 0.434956 | -1.00625 | 4.31448 | 1.3118 | 0.207026 | 70 | 0.522614 | 0 |
| EC012 | KLMI | fP_hz | 9 | 0.71338 | 0.647101 | 0.303204 | 1.12356 | 4.01061 | 0.00389174 | 2 | 0.0117188 | 0 |
| EC013 | KLMI | fP_hz | 9 | 1.463 | 1.46994 | 1.20628 | 1.71972 | 13.1414 | 1.06967e-06 | 0 | 0.00390625 | 0 |
| pooled | KLMI | fP_hz | 18 | 1.08819 | 1.17152 | 0.800262 | 1.37612 | 7.97379 | 3.81658e-07 | 2 | 2.28882e-05 | 0 |
| EC012 | KLMI | ozkurt_mvl | 9 | 0.0130216 | 0.00685987 | 0.00361708 | 0.0224262 | 3.19291 | 0.0127474 | 1 | 0.0078125 | 0 |
| EC013 | KLMI | ozkurt_mvl | 9 | 0.0328822 | 0.0336452 | 0.0252788 | 0.0404856 | 9.97269 | 8.66322e-06 | 0 | 0.00390625 | 0 |
| pooled | KLMI | ozkurt_mvl | 18 | 0.0229519 | 0.0244646 | 0.0155609 | 0.030343 | 6.55176 | 4.93432e-06 | 1 | 1.52588e-05 | 0 |
| EC012 | MVL-Ozkurt | fA_hz | 9 | -1.89606 | -0.481283 | -6.77543 | 2.98331 | -0.896084 | 0.39637 | 19 | 0.734375 | 0 |
| EC013 | MVL-Ozkurt | fA_hz | 9 | 3.66986 | 2.52798 | -0.468392 | 7.80811 | 2.045 | 0.0750892 | 8 | 0.0976562 | 0 |
| pooled | MVL-Ozkurt | fA_hz | 18 | 0.886899 | 1.80455 | -2.28961 | 4.06341 | 0.589072 | 0.563559 | 62 | 0.32473 | 0 |
| EC012 | MVL-Ozkurt | fP_hz | 9 | 0.221369 | 0.35942 | -0.202265 | 0.645002 | 1.205 | 0.262637 | 14 | 0.359375 | 0 |
| EC013 | MVL-Ozkurt | fP_hz | 9 | 0.708942 | 0.641316 | 0.454888 | 0.962995 | 6.43495 | 0.000201501 | 0 | 0.00390625 | 0 |
| pooled | MVL-Ozkurt | fP_hz | 18 | 0.465155 | 0.518603 | 0.212921 | 0.717389 | 3.8908 | 0.00117491 | 19 | 0.00233459 | 0 |
| EC012 | MVL-Ozkurt | ozkurt_mvl | 9 | 0.0270145 | 0.02907 | 0.0170868 | 0.0369422 | 6.27491 | 0.000239175 | 0 | 0.00390625 | 0 |
| EC013 | MVL-Ozkurt | ozkurt_mvl | 9 | 0.033638 | 0.0331496 | 0.0283972 | 0.0388788 | 14.8011 | 4.27345e-07 | 0 | 0.00390625 | 0 |
| pooled | MVL-Ozkurt | ozkurt_mvl | 18 | 0.0303262 | 0.0308978 | 0.0250637 | 0.0355887 | 12.1582 | 8.23265e-10 | 0 | 7.62939e-06 | 0 |
| EC012 | MVL-raw | fA_hz | 9 | 2.68998 | 3.52193 | 0.872342 | 4.50762 | 3.41273 | 0.00918608 | 2 | 0.0117188 | 0 |
| EC013 | MVL-raw | fA_hz | 9 | 7.00581 | 6.8433 | 5.03838 | 8.97324 | 8.21145 | 3.61742e-05 | 0 | 0.00390625 | 0 |
| pooled | MVL-raw | fA_hz | 18 | 4.8479 | 5.17319 | 3.22543 | 6.47037 | 6.30408 | 7.92499e-06 | 2 | 2.28882e-05 | 0 |
| EC012 | MVL-raw | fP_hz | 9 | 0.0956452 | 0.108108 | -0.302872 | 0.494162 | 0.553448 | 0.595082 | 18 | 0.652344 | 0 |
| EC013 | MVL-raw | fP_hz | 9 | 0.408646 | 0.374177 | -0.0371099 | 0.854403 | 2.11403 | 0.0674495 | 7 | 0.0742188 | 0 |
| pooled | MVL-raw | fP_hz | 18 | 0.252146 | 0.224838 | -0.0250355 | 0.529327 | 1.91925 | 0.0718985 | 46 | 0.0897675 | 0 |
| EC012 | MVL-raw | ozkurt_mvl | 9 | 0.0283079 | 0.0256857 | 0.0174917 | 0.039124 | 6.03524 | 0.000310962 | 0 | 0.00390625 | 0 |
| EC013 | MVL-raw | ozkurt_mvl | 9 | 0.0365816 | 0.0389522 | 0.0312995 | 0.0418638 | 15.9703 | 2.36821e-07 | 0 | 0.00390625 | 0 |
| pooled | MVL-raw | ozkurt_mvl | 18 | 0.0324448 | 0.033267 | 0.0266986 | 0.038191 | 11.9126 | 1.12513e-09 | 0 | 7.62939e-06 | 0 |

### POST HOC E1_sensitivity statistics

POST HOC per-session table:
| animal | session | method | outcome | n_run | n_rest | run_mean | rest_mean | mean_difference | welch_t | welch_p | hedges_g | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EC013 | ec013.156 | APC-v1.0 | fP_hz | 56 | 56 | 7.50937 | 6.52696 | 0.982409 | 11.6486 | 6.5879e-19 | 2.18632 | 0.818501 | 1.14102 |
| EC013 | ec013.156 | APC-v1.0 | fA_hz | 56 | 56 | 113.214 | 110.393 | 2.82143 | 0.796401 | 0.427523 | 0.149477 | -4.07143 | 9.66071 |
| EC013 | ec013.156 | APC-v1.0 | ozkurt_mvl | 56 | 56 | 0.108258 | 0.0701854 | 0.0380728 | 8.74547 | 2.88354e-14 | 1.64144 | 0.0293812 | 0.0466367 |
| EC013 | ec013.156 | GLM | fP_hz | 56 | 56 | 7.09821 | 6.38393 | 0.714286 | 2.74727 | 0.00704296 | 0.515636 | 0.223214 | 1.21429 |
| EC013 | ec013.156 | GLM | fA_hz | 56 | 56 | 108.714 | 104.429 | 4.28571 | 1.19077 | 0.236335 | 0.223496 | -2.78571 | 11.2143 |
| EC013 | ec013.156 | GLM | ozkurt_mvl | 56 | 56 | 0.130434 | 0.0966678 | 0.0337662 | 6.4127 | 3.8417e-09 | 1.2036 | 0.023429 | 0.0438642 |
| EC013 | ec013.156 | KLMI | fP_hz | 56 | 56 | 6.55357 | 5.41964 | 1.13393 | 4.21199 | 5.80607e-05 | 0.790549 | 0.607143 | 1.66071 |
| EC013 | ec013.156 | KLMI | fA_hz | 56 | 56 | 108.143 | 105.571 | 2.57143 | 0.697905 | 0.486738 | 0.13099 | -4.57321 | 9.71429 |
| EC013 | ec013.156 | KLMI | ozkurt_mvl | 56 | 56 | 0.125628 | 0.0905723 | 0.0350555 | 5.20979 | 9.09009e-07 | 0.977827 | 0.0217618 | 0.0478938 |
| EC013 | ec013.156 | MVL-Ozkurt | fP_hz | 56 | 56 | 6.08929 | 5.71429 | 0.375 | 1.10073 | 0.273436 | 0.206596 | -0.294643 | 1.02679 |
| EC013 | ec013.156 | MVL-Ozkurt | fA_hz | 56 | 56 | 112 | 104.571 | 7.42857 | 1.81327 | 0.0725944 | 0.340333 | -0.571429 | 15.3571 |
| EC013 | ec013.156 | MVL-Ozkurt | ozkurt_mvl | 56 | 56 | 0.151962 | 0.10751 | 0.0444516 | 7.00312 | 2.1718e-10 | 1.31442 | 0.0318842 | 0.0566404 |
| EC013 | ec013.156 | MVL-raw | fP_hz | 56 | 56 | 5.91071 | 5.99107 | -0.0803571 | -0.257349 | 0.79739 | -0.0483019 | -0.6875 | 0.51808 |
| EC013 | ec013.156 | MVL-raw | fA_hz | 56 | 56 | 90.8571 | 84.8571 | 6 | 3.18568 | 0.00195238 | 0.597921 | 2.21429 | 9.71429 |
| EC013 | ec013.156 | MVL-raw | ozkurt_mvl | 56 | 56 | 0.141269 | 0.0981867 | 0.0430819 | 7.58616 | 1.45653e-11 | 1.42385 | 0.0319467 | 0.0540031 |
| EC013 | ec013.157 | APC-v1.0 | fP_hz | 23 | 33 | 7.49299 | 6.35033 | 1.14265 | 6.77905 | 3.60573e-08 | 1.56253 | 0.827226 | 1.4786 |
| EC013 | ec013.157 | APC-v1.0 | fA_hz | 23 | 33 | 112.609 | 108.152 | 4.45718 | 0.984578 | 0.329275 | 0.251885 | -4.14499 | 13.1344 |
| EC013 | ec013.157 | APC-v1.0 | ozkurt_mvl | 23 | 33 | 0.105732 | 0.0836235 | 0.0221082 | 2.59302 | 0.0126102 | 0.694635 | 0.00558307 | 0.0382455 |
| EC013 | ec013.157 | GLM | fP_hz | 23 | 33 | 7.47826 | 6.34848 | 1.12978 | 2.8323 | 0.00648283 | 0.709882 | 0.339921 | 1.9124 |
| EC013 | ec013.157 | GLM | fA_hz | 23 | 33 | 113.043 | 109.818 | 3.2253 | 0.67427 | 0.503182 | 0.17643 | -6.13979 | 12.6271 |
| EC013 | ec013.157 | GLM | ozkurt_mvl | 23 | 33 | 0.129747 | 0.110366 | 0.0193805 | 2.88064 | 0.0057624 | 0.749558 | 0.00649839 | 0.032292 |
| EC013 | ec013.157 | KLMI | fP_hz | 23 | 33 | 6.26087 | 5.31818 | 0.942688 | 2.26605 | 0.0291453 | 0.638779 | 0.141551 | 1.73518 |
| EC013 | ec013.157 | KLMI | fA_hz | 23 | 33 | 112.348 | 110.182 | 2.16601 | 0.426752 | 0.671384 | 0.112333 | -7.76298 | 11.8738 |
| EC013 | ec013.157 | KLMI | ozkurt_mvl | 23 | 33 | 0.129625 | 0.100827 | 0.028798 | 3.07178 | 0.00360282 | 0.834479 | 0.0112519 | 0.0473416 |
| EC013 | ec013.157 | MVL-Ozkurt | fP_hz | 23 | 33 | 6.63043 | 5.18182 | 1.44862 | 3.25431 | 0.00248928 | 0.933184 | 0.605369 | 2.30308 |
| EC013 | ec013.157 | MVL-Ozkurt | fA_hz | 23 | 33 | 112.348 | 107.515 | 4.83267 | 1.01344 | 0.315551 | 0.263311 | -4.42714 | 14.0976 |
| EC013 | ec013.157 | MVL-Ozkurt | ozkurt_mvl | 23 | 33 | 0.150039 | 0.128102 | 0.0219368 | 2.04986 | 0.0458099 | 0.545791 | 0.00206279 | 0.0426448 |
| EC013 | ec013.157 | MVL-raw | fP_hz | 23 | 33 | 6.34783 | 5.34848 | 0.999341 | 2.18138 | 0.0351007 | 0.609896 | 0.123188 | 1.89988 |
| EC013 | ec013.157 | MVL-raw | fA_hz | 23 | 33 | 92 | 88.3636 | 3.63636 | 1.24066 | 0.220111 | 0.314485 | -2.17655 | 9.03333 |
| EC013 | ec013.157 | MVL-raw | ozkurt_mvl | 23 | 33 | 0.13907 | 0.116932 | 0.0221378 | 2.0647 | 0.0440657 | 0.540889 | 0.00194574 | 0.0426869 |
| EC013 | ec013.205 | APC-v1.0 | fP_hz | 8 | 9 | 7.63842 | 6.23804 | 1.40038 | 9.34705 | 2.94062e-07 | 4.1901 | 1.1374 | 1.68031 |
| EC013 | ec013.205 | APC-v1.0 | fA_hz | 8 | 9 | 108.75 | 111 | -2.25 | -0.325883 | 0.749146 | -0.147547 | -15.0698 | 10.2639 |
| EC013 | ec013.205 | APC-v1.0 | ozkurt_mvl | 8 | 9 | 0.134336 | 0.100383 | 0.0339532 | 2.28615 | 0.0406011 | 1.01742 | 0.00586542 | 0.0598343 |
| EC013 | ec013.205 | GLM | fP_hz | 8 | 9 | 7.5625 | 6.33333 | 1.22917 | 2.13875 | 0.0497244 | 0.969413 | 0.173611 | 2.27778 |
| EC013 | ec013.205 | GLM | fA_hz | 8 | 9 | 108 | 97.7778 | 10.2222 | 1.07026 | 0.301898 | 0.494898 | -7.05556 | 28.1667 |
| EC013 | ec013.205 | GLM | ozkurt_mvl | 8 | 9 | 0.16287 | 0.118874 | 0.0439965 | 3.4036 | 0.00437231 | 1.52928 | 0.0208059 | 0.0676069 |
| EC013 | ec013.205 | KLMI | fP_hz | 8 | 9 | 7.5 | 5.38889 | 2.11111 | 3.72685 | 0.00225227 | 1.67777 | 1.02778 | 3.125 |
| EC013 | ec013.205 | KLMI | fA_hz | 8 | 9 | 103.5 | 102.222 | 1.27778 | 0.246645 | 0.80896 | 0.110404 | -7.88889 | 11.1111 |
| EC013 | ec013.205 | KLMI | ozkurt_mvl | 8 | 9 | 0.168424 | 0.122213 | 0.0462102 | 3.25508 | 0.00632747 | 1.45342 | 0.0204934 | 0.0723257 |
| EC013 | ec013.205 | MVL-Ozkurt | fP_hz | 8 | 9 | 6.5625 | 5.33333 | 1.22917 | 1.41285 | 0.178808 | 0.654006 | -0.402778 | 2.77083 |
| EC013 | ec013.205 | MVL-Ozkurt | fA_hz | 8 | 9 | 100 | 89.7778 | 10.2222 | 1.48553 | 0.160915 | 0.695825 | -2.38889 | 23.0556 |
| EC013 | ec013.205 | MVL-Ozkurt | ozkurt_mvl | 8 | 9 | 0.175493 | 0.136049 | 0.0394443 | 2.38469 | 0.0337558 | 1.06189 | 0.00880039 | 0.0694033 |
| EC013 | ec013.205 | MVL-raw | fP_hz | 8 | 9 | 6.125 | 5.05556 | 1.06944 | 1.55161 | 0.142043 | 0.71649 | -0.256944 | 2.25694 |
| EC013 | ec013.205 | MVL-raw | fA_hz | 8 | 9 | 90 | 84 | 6 | 1.35901 | 0.194308 | 0.624251 | -2.5 | 13.5 |
| EC013 | ec013.205 | MVL-raw | ozkurt_mvl | 8 | 9 | 0.173832 | 0.133034 | 0.0407979 | 2.36661 | 0.0354413 | 1.05152 | 0.0091449 | 0.0723807 |
| EC013 | ec013.206 | APC-v1.0 | fP_hz | 58 | 60 | 7.49501 | 6.44334 | 1.05167 | 14.9552 | 1.19828e-23 | 2.69805 | 0.909023 | 1.18206 |
| EC013 | ec013.206 | APC-v1.0 | fA_hz | 58 | 60 | 112.707 | 111.617 | 1.09023 | 0.364092 | 0.716461 | 0.0664365 | -4.81132 | 6.78531 |
| EC013 | ec013.206 | APC-v1.0 | ozkurt_mvl | 58 | 60 | 0.118454 | 0.0914052 | 0.0270488 | 5.85411 | 4.7964e-08 | 1.06733 | 0.0180806 | 0.0360125 |
| EC013 | ec013.206 | GLM | fP_hz | 58 | 61 | 7.52586 | 6.69672 | 0.829141 | 3.46844 | 0.000771285 | 0.624883 | 0.371082 | 1.29721 |
| EC013 | ec013.206 | GLM | fA_hz | 58 | 61 | 110.069 | 104.721 | 5.34765 | 1.72435 | 0.0872911 | 0.313424 | -0.681882 | 11.4483 |
| EC013 | ec013.206 | GLM | ozkurt_mvl | 58 | 61 | 0.148979 | 0.116212 | 0.0327672 | 7.5194 | 1.31414e-11 | 1.36383 | 0.0240279 | 0.0413375 |
| EC013 | ec013.206 | KLMI | fP_hz | 58 | 61 | 7.25 | 5.77049 | 1.47951 | 5.99374 | 2.34319e-08 | 1.09228 | 0.99983 | 1.94863 |
| EC013 | ec013.206 | KLMI | fA_hz | 58 | 61 | 108.621 | 105.967 | 2.65348 | 0.856887 | 0.393262 | 0.155766 | -3.38949 | 8.51224 |
| EC013 | ec013.206 | KLMI | ozkurt_mvl | 58 | 61 | 0.145165 | 0.112169 | 0.0329963 | 5.97363 | 2.56375e-08 | 1.08637 | 0.0223006 | 0.0437533 |
| EC013 | ec013.206 | MVL-Ozkurt | fP_hz | 58 | 61 | 6.46552 | 5.79508 | 0.670435 | 2.25007 | 0.0264369 | 0.412154 | 0.0981981 | 1.25043 |
| EC013 | ec013.206 | MVL-Ozkurt | fA_hz | 58 | 61 | 110.414 | 107.016 | 3.3974 | 1.02434 | 0.307791 | 0.186591 | -2.92826 | 9.88137 |
| EC013 | ec013.206 | MVL-Ozkurt | ozkurt_mvl | 58 | 61 | 0.163763 | 0.12667 | 0.0370923 | 7.49299 | 1.48569e-11 | 1.36779 | 0.0276889 | 0.0468686 |
| EC013 | ec013.206 | MVL-raw | fP_hz | 58 | 61 | 6.37931 | 5.96721 | 0.412097 | 1.31978 | 0.189588 | 0.241403 | -0.197287 | 1.01288 |
| EC013 | ec013.206 | MVL-raw | fA_hz | 58 | 61 | 91.8621 | 84.1967 | 7.66535 | 4.30137 | 4.0165e-05 | 0.791662 | 4.32883 | 11.2008 |
| EC013 | ec013.206 | MVL-raw | ozkurt_mvl | 58 | 61 | 0.151781 | 0.112744 | 0.039037 | 7.84421 | 2.27208e-12 | 1.42845 | 0.029809 | 0.0486384 |
| EC013 | ec013.208 | APC-v1.0 | fP_hz | 44 | 53 | 7.51382 | 6.39568 | 1.11814 | 8.0317 | 2.5278e-11 | 1.50694 | 0.861554 | 1.39982 |
| EC013 | ec013.208 | APC-v1.0 | fA_hz | 44 | 53 | 113 | 115.113 | -2.11321 | -0.668149 | 0.505672 | -0.131781 | -8.31279 | 4.26117 |
| EC013 | ec013.208 | APC-v1.0 | ozkurt_mvl | 44 | 53 | 0.123708 | 0.0902577 | 0.03345 | 6.46275 | 5.75831e-09 | 1.25073 | 0.0234502 | 0.0433982 |
| EC013 | ec013.208 | GLM | fP_hz | 44 | 53 | 7.82955 | 6.37736 | 1.45219 | 5.70312 | 1.39888e-07 | 1.1174 | 0.962859 | 1.94492 |
| EC013 | ec013.208 | GLM | fA_hz | 44 | 53 | 111.818 | 110.943 | 0.874786 | 0.235678 | 0.814248 | 0.045478 | -6.44271 | 7.95369 |
| EC013 | ec013.208 | GLM | ozkurt_mvl | 44 | 53 | 0.146695 | 0.130771 | 0.0159239 | 2.85677 | 0.00531702 | 0.556015 | 0.00479178 | 0.0266441 |
| EC013 | ec013.208 | KLMI | fP_hz | 44 | 53 | 7.21591 | 5.69811 | 1.5178 | 5.3074 | 7.35512e-07 | 1.06371 | 0.963524 | 2.06755 |
| EC013 | ec013.208 | KLMI | fA_hz | 44 | 53 | 110.182 | 111.623 | -1.44082 | -0.40544 | 0.686231 | -0.0776616 | -8.47714 | 5.34207 |
| EC013 | ec013.208 | KLMI | ozkurt_mvl | 44 | 53 | 0.146751 | 0.127888 | 0.0188627 | 2.30907 | 0.0231921 | 0.467575 | 0.00315173 | 0.0348486 |
| EC013 | ec013.208 | MVL-Ozkurt | fP_hz | 44 | 53 | 5.96591 | 5.70755 | 0.258362 | 0.717125 | 0.475192 | 0.146346 | -0.442555 | 0.955896 |
| EC013 | ec013.208 | MVL-Ozkurt | fA_hz | 44 | 53 | 112.091 | 114.264 | -2.17324 | -0.535483 | 0.593584 | -0.105368 | -10.0039 | 5.60557 |
| EC013 | ec013.208 | MVL-Ozkurt | ozkurt_mvl | 44 | 53 | 0.166666 | 0.146894 | 0.0197723 | 2.81838 | 0.00591114 | 0.570149 | 0.00649979 | 0.0337464 |
| EC013 | ec013.208 | MVL-raw | fP_hz | 44 | 53 | 5.89773 | 6.20755 | -0.30982 | -0.849928 | 0.397617 | -0.172675 | -1.00087 | 0.411273 |
| EC013 | ec013.208 | MVL-raw | fA_hz | 44 | 53 | 94.9091 | 85.0566 | 9.85249 | 4.41185 | 3.68458e-05 | 0.930603 | 5.52826 | 14.1426 |
| EC013 | ec013.208 | MVL-raw | ozkurt_mvl | 44 | 53 | 0.156886 | 0.129507 | 0.0273787 | 3.96274 | 0.000147951 | 0.804977 | 0.0140901 | 0.0409578 |
| EC013 | ec013.251 | APC-v1.0 | fP_hz | 54 | 61 | 7.7262 | 6.45152 | 1.27468 | 10.6445 | 1.65016e-16 | 1.8785 | 1.04487 | 1.51784 |
| EC013 | ec013.251 | APC-v1.0 | fA_hz | 54 | 61 | 111.574 | 114.033 | -2.45871 | -0.726036 | 0.469366 | -0.132315 | -9.07811 | 4.09279 |
| EC013 | ec013.251 | APC-v1.0 | ozkurt_mvl | 54 | 61 | 0.127426 | 0.0884878 | 0.0389383 | 6.4798 | 2.53891e-09 | 1.20014 | 0.0274793 | 0.0505821 |
| EC013 | ec013.251 | GLM | fP_hz | 54 | 65 | 7.93519 | 6.62308 | 1.31211 | 5.08467 | 1.43429e-06 | 0.905466 | 0.802133 | 1.802 |
| EC013 | ec013.251 | GLM | fA_hz | 54 | 65 | 109.185 | 104.185 | 5.00057 | 1.45833 | 0.147437 | 0.260987 | -1.47131 | 11.7061 |
| EC013 | ec013.251 | GLM | ozkurt_mvl | 54 | 65 | 0.158456 | 0.117834 | 0.0406225 | 8.26668 | 2.45753e-13 | 1.48612 | 0.0310568 | 0.0500989 |
| EC013 | ec013.251 | KLMI | fP_hz | 54 | 65 | 7.25 | 5.50769 | 1.74231 | 5.78277 | 7.19692e-08 | 1.0676 | 1.15342 | 2.31056 |
| EC013 | ec013.251 | KLMI | fA_hz | 54 | 65 | 109.111 | 107.138 | 1.97265 | 0.594156 | 0.553576 | 0.105542 | -4.5288 | 8.45014 |
| EC013 | ec013.251 | KLMI | ozkurt_mvl | 54 | 65 | 0.161537 | 0.115071 | 0.0464666 | 7.22137 | 6.63123e-11 | 1.3243 | 0.0341243 | 0.0588623 |
| EC013 | ec013.251 | MVL-Ozkurt | fP_hz | 54 | 65 | 6.50926 | 5.86154 | 0.647721 | 1.86202 | 0.0654493 | 0.346545 | -0.0275178 | 1.31882 |
| EC013 | ec013.251 | MVL-Ozkurt | fA_hz | 54 | 65 | 110.444 | 106.523 | 3.92137 | 1.0772 | 0.283615 | 0.194643 | -3.07821 | 11.017 |
| EC013 | ec013.251 | MVL-Ozkurt | ozkurt_mvl | 54 | 65 | 0.176906 | 0.136103 | 0.0408038 | 7.25781 | 5.35219e-11 | 1.32834 | 0.0300664 | 0.0518484 |
| EC013 | ec013.251 | MVL-raw | fP_hz | 54 | 65 | 7.03704 | 5.83077 | 1.20627 | 3.52235 | 0.000661816 | 0.663671 | 0.539152 | 1.85371 |
| EC013 | ec013.251 | MVL-raw | fA_hz | 54 | 65 | 90.8148 | 85.9077 | 4.90712 | 2.66619 | 0.00893694 | 0.497799 | 1.3196 | 8.44672 |
| EC013 | ec013.251 | MVL-raw | ozkurt_mvl | 54 | 65 | 0.163375 | 0.123822 | 0.0395522 | 7.16357 | 9.85592e-11 | 1.32148 | 0.0289183 | 0.0502987 |
| EC013 | ec013.252 | APC-v1.0 | fP_hz | 32 | 60 | 7.75176 | 6.65709 | 1.09468 | 9.65989 | 1.72953e-15 | 1.70906 | 0.873206 | 1.32033 |
| EC013 | ec013.252 | APC-v1.0 | fA_hz | 32 | 60 | 108.656 | 110.583 | -1.92708 | -0.614062 | 0.540897 | -0.121609 | -7.99198 | 4.09594 |
| EC013 | ec013.252 | APC-v1.0 | ozkurt_mvl | 32 | 60 | 0.120906 | 0.0897989 | 0.0311074 | 5.15128 | 1.71499e-06 | 1.00803 | 0.0195413 | 0.0429918 |
| EC013 | ec013.252 | GLM | fP_hz | 32 | 64 | 7.82812 | 6.91406 | 0.914062 | 3.10975 | 0.00258317 | 0.602957 | 0.335938 | 1.46875 |
| EC013 | ec013.252 | GLM | fA_hz | 32 | 64 | 109.75 | 104.375 | 5.375 | 1.46853 | 0.146224 | 0.29608 | -1.75156 | 12.5625 |
| EC013 | ec013.252 | GLM | ozkurt_mvl | 32 | 64 | 0.159944 | 0.124643 | 0.0353013 | 5.81593 | 1.24402e-07 | 1.14332 | 0.0236309 | 0.0474365 |
| EC013 | ec013.252 | KLMI | fP_hz | 32 | 64 | 6.79688 | 5.67969 | 1.11719 | 2.9027 | 0.00530891 | 0.652566 | 0.366992 | 1.85156 |
| EC013 | ec013.252 | KLMI | fA_hz | 32 | 64 | 109.25 | 104.938 | 4.3125 | 1.13442 | 0.260462 | 0.232422 | -3.0625 | 11.5641 |
| EC013 | ec013.252 | KLMI | ozkurt_mvl | 32 | 64 | 0.156743 | 0.11985 | 0.0368927 | 3.77814 | 0.000357795 | 0.813022 | 0.017403 | 0.0552009 |
| EC013 | ec013.252 | MVL-Ozkurt | fP_hz | 32 | 64 | 6.39062 | 5.5625 | 0.828125 | 2.05781 | 0.0446047 | 0.472521 | 0.0623047 | 1.60156 |
| EC013 | ec013.252 | MVL-Ozkurt | fA_hz | 32 | 64 | 117.25 | 106.812 | 10.4375 | 2.66884 | 0.00926817 | 0.527412 | 2.6875 | 17.9391 |
| EC013 | ec013.252 | MVL-Ozkurt | ozkurt_mvl | 32 | 64 | 0.181947 | 0.150969 | 0.0309774 | 4.21415 | 6.50429e-05 | 0.819857 | 0.0169297 | 0.0451871 |
| EC013 | ec013.252 | MVL-raw | fP_hz | 32 | 64 | 6.01562 | 5.66406 | 0.351562 | 0.879717 | 0.382854 | 0.198291 | -0.429688 | 1.14062 |
| EC013 | ec013.252 | MVL-raw | fA_hz | 32 | 64 | 95.25 | 84.5625 | 10.6875 | 4.52018 | 5.34361e-05 | 1.17218 | 6.25 | 15.25 |
| EC013 | ec013.252 | MVL-raw | ozkurt_mvl | 32 | 64 | 0.165496 | 0.135355 | 0.0301418 | 4.26331 | 5.62732e-05 | 0.842463 | 0.0164323 | 0.0441053 |
| EC013 | ec013.374 | APC-v1.0 | fP_hz | 88 | 75 | 7.35578 | 6.38564 | 0.970139 | 8.94094 | 6.20077e-14 | 1.4938 | 0.766943 | 1.19015 |
| EC013 | ec013.374 | APC-v1.0 | fA_hz | 88 | 75 | 110.602 | 111.16 | -0.557727 | -0.21592 | 0.829337 | -0.0339383 | -5.59096 | 4.57244 |
| EC013 | ec013.374 | APC-v1.0 | ozkurt_mvl | 88 | 75 | 0.114335 | 0.0833684 | 0.0309664 | 7.25301 | 1.8764e-11 | 1.13988 | 0.0227308 | 0.0393287 |
| EC013 | ec013.374 | GLM | fP_hz | 88 | 77 | 7.39205 | 6.59091 | 0.801136 | 3.49425 | 0.000653223 | 0.557428 | 0.352252 | 1.24513 |
| EC013 | ec013.374 | GLM | fA_hz | 88 | 77 | 113.182 | 110.234 | 2.94805 | 1.06758 | 0.287364 | 0.166741 | -2.4026 | 8.27305 |
| EC013 | ec013.374 | GLM | ozkurt_mvl | 88 | 77 | 0.142165 | 0.114462 | 0.027703 | 7.61738 | 2.17309e-12 | 1.18487 | 0.0205449 | 0.0347847 |
| EC013 | ec013.374 | KLMI | fP_hz | 88 | 77 | 6.81818 | 5.42208 | 1.3961 | 6.017 | 1.1521e-08 | 0.920351 | 0.9375 | 1.8458 |
| EC013 | ec013.374 | KLMI | fA_hz | 88 | 77 | 109.818 | 108.883 | 0.935065 | 0.332717 | 0.739799 | 0.0520223 | -4.50666 | 6.54545 |
| EC013 | ec013.374 | KLMI | ozkurt_mvl | 88 | 77 | 0.13834 | 0.105636 | 0.0327035 | 6.09743 | 8.1515e-09 | 0.952203 | 0.0220729 | 0.0432838 |
| EC013 | ec013.374 | MVL-Ozkurt | fP_hz | 88 | 77 | 6.32386 | 5.77273 | 0.551136 | 2.09362 | 0.0379145 | 0.326993 | 0.036526 | 1.06169 |
| EC013 | ec013.374 | MVL-Ozkurt | fA_hz | 88 | 77 | 111.591 | 111.481 | 0.11039 | 0.0378074 | 0.969891 | 0.00592076 | -5.45455 | 5.84432 |
| EC013 | ec013.374 | MVL-Ozkurt | ozkurt_mvl | 88 | 77 | 0.159821 | 0.128713 | 0.0311077 | 7.33062 | 1.01352e-11 | 1.12659 | 0.0228358 | 0.0394659 |
| EC013 | ec013.374 | MVL-raw | fP_hz | 88 | 77 | 6.28409 | 5.8961 | 0.387987 | 1.39968 | 0.163663 | 0.219614 | -0.137987 | 0.915605 |
| EC013 | ec013.374 | MVL-raw | fA_hz | 88 | 77 | 99.8182 | 86.961 | 12.8571 | 7.70395 | 1.87441e-12 | 1.15972 | 9.68166 | 16.143 |
| EC013 | ec013.374 | MVL-raw | ozkurt_mvl | 88 | 77 | 0.155435 | 0.113977 | 0.0414573 | 9.52802 | 2.22759e-17 | 1.4631 | 0.0329595 | 0.049981 |
| EC013 | ec013.375 | APC-v1.0 | fP_hz | 68 | 128 | 7.51563 | 6.09527 | 1.42036 | 10.4033 | 1.58405e-19 | 1.17634 | 1.16327 | 1.69485 |
| EC013 | ec013.375 | APC-v1.0 | fA_hz | 68 | 128 | 111.132 | 114.695 | -3.56296 | -1.49823 | 0.135926 | -0.206473 | -8.17969 | 1.067 |
| EC013 | ec013.375 | APC-v1.0 | ozkurt_mvl | 68 | 128 | 0.111366 | 0.0811338 | 0.0302318 | 7.5619 | 1.93166e-12 | 1.01358 | 0.0223483 | 0.0380005 |
| EC013 | ec013.375 | GLM | fP_hz | 68 | 137 | 7.60294 | 6.32482 | 1.27812 | 6.08344 | 6.57315e-09 | 0.78952 | 0.867086 | 1.67905 |
| EC013 | ec013.375 | GLM | fA_hz | 68 | 137 | 110.824 | 110.248 | 0.575354 | 0.212404 | 0.832054 | 0.0290272 | -4.83862 | 5.96269 |
| EC013 | ec013.375 | GLM | ozkurt_mvl | 68 | 137 | 0.141796 | 0.113711 | 0.0280851 | 6.52331 | 7.03964e-10 | 0.867176 | 0.0194936 | 0.0364085 |
| EC013 | ec013.375 | KLMI | fP_hz | 68 | 137 | 6.77206 | 5.42701 | 1.34505 | 5.41877 | 2.87276e-07 | 0.814514 | 0.856965 | 1.82509 |
| EC013 | ec013.375 | KLMI | fA_hz | 68 | 137 | 109.471 | 109.927 | -0.456419 | -0.175086 | 0.861226 | -0.0238764 | -5.52559 | 4.50506 |
| EC013 | ec013.375 | KLMI | ozkurt_mvl | 68 | 137 | 0.141118 | 0.109364 | 0.0317543 | 6.03308 | 1.10948e-08 | 0.839014 | 0.0211939 | 0.0419033 |
| EC013 | ec013.375 | MVL-Ozkurt | fP_hz | 68 | 137 | 6.18382 | 5.79927 | 0.384553 | 1.39582 | 0.165155 | 0.20877 | -0.151569 | 0.92674 |
| EC013 | ec013.375 | MVL-Ozkurt | fA_hz | 68 | 137 | 108 | 108.993 | -0.992701 | -0.343069 | 0.732005 | -0.0477217 | -6.72649 | 4.59945 |
| EC013 | ec013.375 | MVL-Ozkurt | ozkurt_mvl | 68 | 137 | 0.161309 | 0.131977 | 0.0293321 | 5.77841 | 4.38242e-08 | 0.826051 | 0.0194832 | 0.0394777 |
| EC013 | ec013.375 | MVL-raw | fP_hz | 68 | 137 | 6.39706 | 5.67883 | 0.718227 | 2.47764 | 0.014573 | 0.377177 | 0.164333 | 1.28683 |
| EC013 | ec013.375 | MVL-raw | fA_hz | 68 | 137 | 93.3529 | 86.9197 | 6.43323 | 3.81809 | 0.000232329 | 0.633137 | 3.17903 | 9.81067 |
| EC013 | ec013.375 | MVL-raw | ozkurt_mvl | 68 | 137 | 0.155183 | 0.119868 | 0.0353155 | 7.21389 | 3.01965e-11 | 1.04387 | 0.0259615 | 0.0450195 |

POST HOC across-session table:
| animal_pool | method | outcome | n_sessions | mean_session_difference | median_session_difference | ci_low | ci_high | one_sample_t | one_sample_p | wilcoxon_statistic | wilcoxon_p | zero_differences |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EC012 | APC-v1.0 | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | APC-v1.0 | fA_hz | 9 | -0.500095 | -1.92708 | -2.58858 | 1.58839 | -0.55218 | 0.59591 | 18 | 0.652344 | 0 |
| pooled | APC-v1.0 | fA_hz | 9 | -0.500095 | -1.92708 | -2.58858 | 1.58839 | -0.55218 | 0.59591 | 18 | 0.652344 | 0 |
| EC012 | APC-v1.0 | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | APC-v1.0 | fP_hz | 9 | 1.16168 | 1.11814 | 1.03296 | 1.2904 | 20.8115 | 2.97972e-08 | 0 | 0.00390625 | 0 |
| pooled | APC-v1.0 | fP_hz | 9 | 1.16168 | 1.11814 | 1.03296 | 1.2904 | 20.8115 | 2.97972e-08 | 0 | 0.00390625 | 0 |
| EC012 | APC-v1.0 | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | APC-v1.0 | ozkurt_mvl | 9 | 0.0317641 | 0.0311074 | 0.0277535 | 0.0357747 | 18.2635 | 8.30787e-08 | 0 | 0.00390625 | 0 |
| pooled | APC-v1.0 | ozkurt_mvl | 9 | 0.0317641 | 0.0311074 | 0.0277535 | 0.0357747 | 18.2635 | 8.30787e-08 | 0 | 0.00390625 | 0 |
| EC012 | GLM | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | GLM | fA_hz | 9 | 4.20607 | 4.28571 | 1.99281 | 6.41934 | 4.38231 | 0.00234153 | 0 | 0.00390625 | 0 |
| pooled | GLM | fA_hz | 9 | 4.20607 | 4.28571 | 1.99281 | 6.41934 | 4.38231 | 0.00234153 | 0 | 0.00390625 | 0 |
| EC012 | GLM | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | GLM | fP_hz | 9 | 1.07333 | 1.12978 | 0.870333 | 1.27633 | 12.1927 | 1.89859e-06 | 0 | 0.00390625 | 0 |
| pooled | GLM | fP_hz | 9 | 1.07333 | 1.12978 | 0.870333 | 1.27633 | 12.1927 | 1.89859e-06 | 0 | 0.00390625 | 0 |
| EC012 | GLM | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | GLM | ozkurt_mvl | 9 | 0.0308385 | 0.0327672 | 0.0237924 | 0.0378845 | 10.0927 | 7.92294e-06 | 0 | 0.00390625 | 0 |
| pooled | GLM | ozkurt_mvl | 9 | 0.0308385 | 0.0327672 | 0.0237924 | 0.0378845 | 10.0927 | 7.92294e-06 | 0 | 0.00390625 | 0 |
| EC012 | KLMI | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | KLMI | fA_hz | 9 | 1.55463 | 1.97265 | 0.226777 | 2.88248 | 2.69983 | 0.027081 | 5 | 0.0390625 | 0 |
| pooled | KLMI | fA_hz | 9 | 1.55463 | 1.97265 | 0.226777 | 2.88248 | 2.69983 | 0.027081 | 5 | 0.0390625 | 0 |
| EC012 | KLMI | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | KLMI | fP_hz | 9 | 1.42063 | 1.3961 | 1.14857 | 1.69269 | 12.0414 | 2.08829e-06 | 0 | 0.00390625 | 0 |
| pooled | KLMI | fP_hz | 9 | 1.42063 | 1.3961 | 1.14857 | 1.69269 | 12.0414 | 2.08829e-06 | 0 | 0.00390625 | 0 |
| EC012 | KLMI | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | KLMI | ozkurt_mvl | 9 | 0.0344155 | 0.0329963 | 0.0278911 | 0.04094 | 12.1639 | 1.93319e-06 | 0 | 0.00390625 | 0 |
| pooled | KLMI | ozkurt_mvl | 9 | 0.0344155 | 0.0329963 | 0.0278911 | 0.04094 | 12.1639 | 1.93319e-06 | 0 | 0.00390625 | 0 |
| EC012 | MVL-Ozkurt | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-Ozkurt | fA_hz | 9 | 4.13158 | 3.92137 | 0.577946 | 7.68521 | 2.68104 | 0.0278809 | 5 | 0.0390625 | 0 |
| pooled | MVL-Ozkurt | fA_hz | 9 | 4.13158 | 3.92137 | 0.577946 | 7.68521 | 2.68104 | 0.0278809 | 5 | 0.0390625 | 0 |
| EC012 | MVL-Ozkurt | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-Ozkurt | fP_hz | 9 | 0.710346 | 0.647721 | 0.402658 | 1.01803 | 5.32377 | 0.000707815 | 0 | 0.00390625 | 0 |
| pooled | MVL-Ozkurt | fP_hz | 9 | 0.710346 | 0.647721 | 0.402658 | 1.01803 | 5.32377 | 0.000707815 | 0 | 0.00390625 | 0 |
| EC012 | MVL-Ozkurt | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-Ozkurt | ozkurt_mvl | 9 | 0.0327687 | 0.0311077 | 0.0262899 | 0.0392475 | 11.6635 | 2.66205e-06 | 0 | 0.00390625 | 0 |
| pooled | MVL-Ozkurt | ozkurt_mvl | 9 | 0.0327687 | 0.0311077 | 0.0262899 | 0.0392475 | 11.6635 | 2.66205e-06 | 0 | 0.00390625 | 0 |
| EC012 | MVL-raw | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-raw | fA_hz | 9 | 7.55991 | 6.43323 | 5.25908 | 9.86074 | 7.57692 | 6.44297e-05 | 0 | 0.00390625 | 0 |
| pooled | MVL-raw | fA_hz | 9 | 7.55991 | 6.43323 | 5.25908 | 9.86074 | 7.57692 | 6.44297e-05 | 0 | 0.00390625 | 0 |
| EC012 | MVL-raw | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-raw | fP_hz | 9 | 0.528306 | 0.412097 | 0.130027 | 0.926584 | 3.05885 | 0.0156099 | 3 | 0.0195312 | 0 |
| pooled | MVL-raw | fP_hz | 9 | 0.528306 | 0.412097 | 0.130027 | 0.926584 | 3.05885 | 0.0156099 | 3 | 0.0195312 | 0 |
| EC012 | MVL-raw | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-raw | ozkurt_mvl | 9 | 0.0354333 | 0.039037 | 0.0298428 | 0.0410239 | 14.6156 | 4.71181e-07 | 0 | 0.00390625 | 0 |
| pooled | MVL-raw | ozkurt_mvl | 9 | 0.0354333 | 0.039037 | 0.0298428 | 0.0410239 | 14.6156 | 4.71181e-07 | 0 | 0.00390625 | 0 |

## POST HOC region-specific mixed models

POST HOC REML models retain the same session random intercept and state slope. EC now has both animals and uses `outcome ~ state_run + animal + (1 + state_run | session)`, EC012 reference. CA1/E1 sensitivity contain EC013 only and omit the redundant constant animal term, as in the prespecified pipeline. No random-effects simplification is applied. POST HOC coefficient table:
| analysis | outcome | Name | Estimate | SE | tStat | DF | pValue | Lower | Upper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | fP_hz | (Intercept) | 6.92665 | 0.41119 | 16.8454 | 938 | 7.8868e-56 | 6.11969 | 7.73361 |
| CA1 | fP_hz | state_run | 0.898049 | 0.296683 | 3.02697 | 938 | 0.00253767 | 0.315811 | 1.48029 |
| CA1 | ozkurt_mvl | (Intercept) | 0.0645877 | 0.00275433 | 23.4495 | 938 | 4.5687e-96 | 0.0591823 | 0.069993 |
| CA1 | ozkurt_mvl | state_run | 0.00489009 | 0.00317267 | 1.54132 | 938 | 0.123576 | -0.00133626 | 0.0111164 |
| EC | fP_hz | (Intercept) | 6.92447 | 0.138536 | 49.9831 | 1616 | 0 | 6.65274 | 7.1962 |
| EC | fP_hz | animal_EC013 | -0.993295 | 0.0582769 | -17.0444 | 1616 | 4.91908e-60 | -1.1076 | -0.878988 |
| EC | fP_hz | state_run | 1.84202 | 0.190275 | 9.68083 | 1616 | 1.38427e-21 | 1.46881 | 2.21523 |
| EC | ozkurt_mvl | (Intercept) | 0.0760535 | 0.00300321 | 25.3241 | 1616 | 1.94614e-119 | 0.0701629 | 0.0819441 |
| EC | ozkurt_mvl | animal_EC013 | 0.0105847 | 0.00412888 | 2.56357 | 1616 | 0.01045 | 0.00248615 | 0.0186832 |
| EC | ozkurt_mvl | state_run | 0.0215187 | 0.00301053 | 7.14779 | 1616 | 1.33007e-12 | 0.0156137 | 0.0274236 |
| E1_sensitivity | fP_hz | (Intercept) | 6.3997 | 0.060796 | 105.265 | 964 | 0 | 6.28039 | 6.519 |
| E1_sensitivity | fP_hz | state_run | 1.13639 | 0.0652058 | 17.4277 | 964 | 2.43046e-59 | 1.00843 | 1.26435 |
| E1_sensitivity | ozkurt_mvl | (Intercept) | 0.0857701 | 0.00257873 | 33.2605 | 964 | 3.51742e-162 | 0.0807095 | 0.0908306 |
| E1_sensitivity | ozkurt_mvl | state_run | 0.0319893 | 0.00184632 | 17.3259 | 964 | 9.38596e-59 | 0.028366 | 0.0356126 |

POST HOC covariance and optimizer-warning table:
| analysis | outcome | sessions | observations | animal_term_omitted | var_intercept | cov_intercept_state | var_state | residual_variance | covariance_rank | optimizer_nonconvergence_warning | warning |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | fP_hz | 9 | 940 | True | 1.29021 | -0.709325 | 0.389969 | 9.7841 | 1 | False | none |
| CA1 | ozkurt_mvl | 9 | 940 | True | 5.00229e-05 | -3.21194e-05 | 5.2779e-05 | 0.000817148 | 2 | False | none |
| EC | fP_hz | 18 | 1619 | False | 0.311163 | -0.434101 | 0.619723 | 0.554489 | 2 | False | none |
| EC | ozkurt_mvl | 18 | 1619 | False | 5.42831e-05 | 1.66199e-05 | 0.000118031 | 0.000847793 | 2 | False | none |
| E1_sensitivity | fP_hz | 9 | 966 | True | 0.0212385 | -0.0139868 | 0.0140996 | 0.584675 | 2 | False | none |
| E1_sensitivity | ozkurt_mvl | 9 | 966 | True | 4.368e-05 | 9.46949e-07 | 2.05291e-08 | 0.000798068 | 1 | False | none |

POST HOC versus prespecified mixed-model coefficient table:
| analysis | outcome | Name | Estimate_prespecified_5s | Lower_prespecified_5s | Upper_prespecified_5s | Estimate_posthoc_2s | Lower_posthoc_2s | Upper_posthoc_2s | pValue_posthoc_2s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | fP_hz | (Intercept) | 7.43555 | 5.12949 | 9.74162 | 6.92665 | 6.11969 | 7.73361 | 7.8868e-56 |
| CA1 | fP_hz | state_run | 0.646746 | -1.71203 | 3.00552 | 0.898049 | 0.315811 | 1.48029 | 0.00253767 |
| CA1 | ozkurt_mvl | (Intercept) | 0.0420767 | 0.0362643 | 0.047889 | 0.0645877 | 0.0591823 | 0.069993 | 4.5687e-96 |
| CA1 | ozkurt_mvl | state_run | 0.0148146 | 0.00298916 | 0.0266401 | 0.00489009 | -0.00133626 | 0.0111164 | 0.123576 |
| E1_sensitivity | fP_hz | (Intercept) | 6.2926 | 6.02661 | 6.5586 | 6.3997 | 6.28039 | 6.519 | 0 |
| E1_sensitivity | fP_hz | state_run | 1.20765 | 0.73833 | 1.67696 | 1.13639 | 1.00843 | 1.26435 | 2.43046e-59 |
| E1_sensitivity | ozkurt_mvl | (Intercept) | 0.0671483 | 0.0625016 | 0.071795 | 0.0857701 | 0.0807095 | 0.0908306 | 3.51742e-162 |
| E1_sensitivity | ozkurt_mvl | state_run | 0.0378455 | 0.0228063 | 0.0528847 | 0.0319893 | 0.028366 | 0.0356126 | 9.38596e-59 |
| EC | fP_hz | (Intercept) | 6.27234 | 5.91083 | 6.63385 | 6.92447 | 6.65274 | 7.1962 | 0 |
| EC | fP_hz | animal_EC013 | NA | NA | NA | -0.993295 | -1.1076 | -0.878988 | 4.91908e-60 |
| EC | fP_hz | state_run | 1.20543 | 0.686406 | 1.72446 | 1.84202 | 1.46881 | 2.21523 | 1.38427e-21 |
| EC | ozkurt_mvl | (Intercept) | 0.0693591 | 0.0617778 | 0.0769403 | 0.0760535 | 0.0701629 | 0.0819441 | 1.94614e-119 |
| EC | ozkurt_mvl | animal_EC013 | NA | NA | NA | 0.0105847 | 0.00248615 | 0.0186832 | 0.01045 |
| EC | ozkurt_mvl | state_run | 0.0264026 | 0.0128081 | 0.039997 | 0.0215187 | 0.0156137 | 0.0274236 | 1.33007e-12 |

Full POST HOC model objects, covariance eigenvalues and fit logs are retained in this folder; [posthoc_2s_mixed_models.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_mixed_models.json>).

## POST HOC boundary picks and within-state spread

POST HOC exact boundary counts (fP=4 or 12 Hz) and sample SD/IQR/unscaled MAD of within-state fP are reported below. Frozen APC can estimate outside the scan phase range. POST HOC boundary table:
| analysis | animal | session | method | state | n_bouts | n_valid | boundary_fp_4 | boundary_fp_12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | EC013 | ec013.156 | APC-v1.0 | run | 56 | 56 | 0 | 0 |
| CA1 | EC013 | ec013.156 | APC-v1.0 | rest | 56 | 54 | 0 | 0 |
| CA1 | EC013 | ec013.156 | GLM | run | 56 | 56 | 15 | 1 |
| CA1 | EC013 | ec013.156 | GLM | rest | 56 | 56 | 10 | 0 |
| CA1 | EC013 | ec013.156 | KLMI | run | 56 | 56 | 34 | 0 |
| CA1 | EC013 | ec013.156 | KLMI | rest | 56 | 56 | 29 | 0 |
| CA1 | EC013 | ec013.156 | MVL-Ozkurt | run | 56 | 56 | 20 | 1 |
| CA1 | EC013 | ec013.156 | MVL-Ozkurt | rest | 56 | 56 | 19 | 1 |
| CA1 | EC013 | ec013.156 | MVL-raw | run | 56 | 56 | 17 | 1 |
| CA1 | EC013 | ec013.156 | MVL-raw | rest | 56 | 56 | 20 | 1 |
| CA1 | EC013 | ec013.157 | APC-v1.0 | run | 23 | 23 | 0 | 0 |
| CA1 | EC013 | ec013.157 | APC-v1.0 | rest | 33 | 31 | 0 | 0 |
| CA1 | EC013 | ec013.157 | GLM | run | 23 | 23 | 8 | 0 |
| CA1 | EC013 | ec013.157 | GLM | rest | 33 | 33 | 8 | 0 |
| CA1 | EC013 | ec013.157 | KLMI | run | 23 | 23 | 13 | 0 |
| CA1 | EC013 | ec013.157 | KLMI | rest | 33 | 33 | 17 | 0 |
| CA1 | EC013 | ec013.157 | MVL-Ozkurt | run | 23 | 23 | 9 | 0 |
| CA1 | EC013 | ec013.157 | MVL-Ozkurt | rest | 33 | 33 | 13 | 0 |
| CA1 | EC013 | ec013.157 | MVL-raw | run | 23 | 23 | 7 | 0 |
| CA1 | EC013 | ec013.157 | MVL-raw | rest | 33 | 33 | 11 | 0 |
| CA1 | EC013 | ec013.205 | APC-v1.0 | run | 8 | 8 | 0 | 0 |
| CA1 | EC013 | ec013.205 | APC-v1.0 | rest | 9 | 9 | 0 | 0 |
| CA1 | EC013 | ec013.205 | GLM | run | 8 | 8 | 0 | 0 |
| CA1 | EC013 | ec013.205 | GLM | rest | 9 | 9 | 3 | 1 |
| CA1 | EC013 | ec013.205 | KLMI | run | 8 | 8 | 1 | 0 |
| CA1 | EC013 | ec013.205 | KLMI | rest | 9 | 9 | 6 | 0 |
| CA1 | EC013 | ec013.205 | MVL-Ozkurt | run | 8 | 8 | 1 | 0 |
| CA1 | EC013 | ec013.205 | MVL-Ozkurt | rest | 9 | 9 | 4 | 0 |
| CA1 | EC013 | ec013.205 | MVL-raw | run | 8 | 8 | 1 | 0 |
| CA1 | EC013 | ec013.205 | MVL-raw | rest | 9 | 9 | 3 | 0 |
| CA1 | EC013 | ec013.206 | APC-v1.0 | run | 58 | 58 | 0 | 0 |
| CA1 | EC013 | ec013.206 | APC-v1.0 | rest | 61 | 59 | 0 | 0 |
| CA1 | EC013 | ec013.206 | GLM | run | 58 | 58 | 11 | 0 |
| CA1 | EC013 | ec013.206 | GLM | rest | 61 | 61 | 10 | 0 |
| CA1 | EC013 | ec013.206 | KLMI | run | 58 | 58 | 24 | 0 |
| CA1 | EC013 | ec013.206 | KLMI | rest | 61 | 61 | 32 | 0 |
| CA1 | EC013 | ec013.206 | MVL-Ozkurt | run | 58 | 58 | 22 | 0 |
| CA1 | EC013 | ec013.206 | MVL-Ozkurt | rest | 61 | 61 | 22 | 1 |
| CA1 | EC013 | ec013.206 | MVL-raw | run | 58 | 58 | 25 | 0 |
| CA1 | EC013 | ec013.206 | MVL-raw | rest | 61 | 61 | 19 | 0 |
| CA1 | EC013 | ec013.208 | APC-v1.0 | run | 44 | 43 | 0 | 0 |
| CA1 | EC013 | ec013.208 | APC-v1.0 | rest | 53 | 48 | 0 | 0 |
| CA1 | EC013 | ec013.208 | GLM | run | 44 | 44 | 10 | 1 |
| CA1 | EC013 | ec013.208 | GLM | rest | 53 | 53 | 9 | 0 |
| CA1 | EC013 | ec013.208 | KLMI | run | 44 | 44 | 18 | 0 |
| CA1 | EC013 | ec013.208 | KLMI | rest | 53 | 53 | 21 | 0 |
| CA1 | EC013 | ec013.208 | MVL-Ozkurt | run | 44 | 44 | 18 | 1 |
| CA1 | EC013 | ec013.208 | MVL-Ozkurt | rest | 53 | 53 | 21 | 1 |
| CA1 | EC013 | ec013.208 | MVL-raw | run | 44 | 44 | 20 | 1 |
| CA1 | EC013 | ec013.208 | MVL-raw | rest | 53 | 53 | 21 | 1 |
| CA1 | EC013 | ec013.251 | APC-v1.0 | run | 54 | 54 | 0 | 0 |
| CA1 | EC013 | ec013.251 | APC-v1.0 | rest | 65 | 60 | 0 | 0 |
| CA1 | EC013 | ec013.251 | GLM | run | 54 | 54 | 7 | 1 |
| CA1 | EC013 | ec013.251 | GLM | rest | 65 | 65 | 11 | 1 |
| CA1 | EC013 | ec013.251 | KLMI | run | 54 | 54 | 20 | 0 |
| CA1 | EC013 | ec013.251 | KLMI | rest | 65 | 65 | 39 | 0 |
| CA1 | EC013 | ec013.251 | MVL-Ozkurt | run | 54 | 54 | 17 | 0 |
| CA1 | EC013 | ec013.251 | MVL-Ozkurt | rest | 65 | 65 | 25 | 0 |
| CA1 | EC013 | ec013.251 | MVL-raw | run | 54 | 54 | 21 | 0 |
| CA1 | EC013 | ec013.251 | MVL-raw | rest | 65 | 65 | 22 | 2 |
| CA1 | EC013 | ec013.252 | APC-v1.0 | run | 32 | 32 | 0 | 0 |
| CA1 | EC013 | ec013.252 | APC-v1.0 | rest | 64 | 60 | 0 | 0 |
| CA1 | EC013 | ec013.252 | GLM | run | 32 | 32 | 1 | 0 |
| CA1 | EC013 | ec013.252 | GLM | rest | 64 | 64 | 9 | 1 |
| CA1 | EC013 | ec013.252 | KLMI | run | 32 | 32 | 17 | 0 |
| CA1 | EC013 | ec013.252 | KLMI | rest | 64 | 64 | 27 | 0 |
| CA1 | EC013 | ec013.252 | MVL-Ozkurt | run | 32 | 32 | 17 | 0 |
| CA1 | EC013 | ec013.252 | MVL-Ozkurt | rest | 64 | 64 | 17 | 0 |
| CA1 | EC013 | ec013.252 | MVL-raw | run | 32 | 32 | 12 | 1 |
| CA1 | EC013 | ec013.252 | MVL-raw | rest | 64 | 64 | 15 | 0 |
| CA1 | EC013 | ec013.374 | APC-v1.0 | run | 88 | 88 | 0 | 0 |
| CA1 | EC013 | ec013.374 | APC-v1.0 | rest | 77 | 76 | 0 | 0 |
| CA1 | EC013 | ec013.374 | GLM | run | 88 | 88 | 11 | 2 |
| CA1 | EC013 | ec013.374 | GLM | rest | 77 | 77 | 14 | 1 |
| CA1 | EC013 | ec013.374 | KLMI | run | 88 | 88 | 44 | 0 |
| CA1 | EC013 | ec013.374 | KLMI | rest | 77 | 77 | 34 | 0 |
| CA1 | EC013 | ec013.374 | MVL-Ozkurt | run | 88 | 88 | 23 | 0 |
| CA1 | EC013 | ec013.374 | MVL-Ozkurt | rest | 77 | 77 | 23 | 0 |
| CA1 | EC013 | ec013.374 | MVL-raw | run | 88 | 88 | 26 | 1 |
| CA1 | EC013 | ec013.374 | MVL-raw | rest | 77 | 77 | 19 | 0 |
| CA1 | EC013 | ec013.375 | APC-v1.0 | run | 68 | 61 | 0 | 0 |
| CA1 | EC013 | ec013.375 | APC-v1.0 | rest | 137 | 120 | 0 | 0 |
| CA1 | EC013 | ec013.375 | GLM | run | 68 | 68 | 13 | 0 |
| CA1 | EC013 | ec013.375 | GLM | rest | 137 | 137 | 24 | 3 |
| CA1 | EC013 | ec013.375 | KLMI | run | 68 | 68 | 32 | 0 |
| CA1 | EC013 | ec013.375 | KLMI | rest | 137 | 137 | 57 | 0 |
| CA1 | EC013 | ec013.375 | MVL-Ozkurt | run | 68 | 68 | 33 | 0 |
| CA1 | EC013 | ec013.375 | MVL-Ozkurt | rest | 137 | 137 | 60 | 3 |
| CA1 | EC013 | ec013.375 | MVL-raw | run | 68 | 68 | 33 | 0 |
| CA1 | EC013 | ec013.375 | MVL-raw | rest | 137 | 137 | 60 | 2 |
| E1_sensitivity | EC013 | ec013.156 | APC-v1.0 | run | 56 | 56 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.156 | APC-v1.0 | rest | 56 | 56 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.156 | GLM | run | 56 | 56 | 2 | 0 |
| E1_sensitivity | EC013 | ec013.156 | GLM | rest | 56 | 56 | 3 | 0 |
| E1_sensitivity | EC013 | ec013.156 | KLMI | run | 56 | 56 | 6 | 0 |
| E1_sensitivity | EC013 | ec013.156 | KLMI | rest | 56 | 56 | 11 | 0 |
| E1_sensitivity | EC013 | ec013.156 | MVL-Ozkurt | run | 56 | 56 | 15 | 0 |
| E1_sensitivity | EC013 | ec013.156 | MVL-Ozkurt | rest | 56 | 56 | 9 | 1 |
| E1_sensitivity | EC013 | ec013.156 | MVL-raw | run | 56 | 56 | 12 | 0 |
| E1_sensitivity | EC013 | ec013.156 | MVL-raw | rest | 56 | 56 | 9 | 0 |
| E1_sensitivity | EC013 | ec013.157 | APC-v1.0 | run | 23 | 23 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.157 | APC-v1.0 | rest | 33 | 33 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.157 | GLM | run | 23 | 23 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.157 | GLM | rest | 33 | 33 | 5 | 0 |
| E1_sensitivity | EC013 | ec013.157 | KLMI | run | 23 | 23 | 6 | 0 |
| E1_sensitivity | EC013 | ec013.157 | KLMI | rest | 33 | 33 | 11 | 0 |
| E1_sensitivity | EC013 | ec013.157 | MVL-Ozkurt | run | 23 | 23 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.157 | MVL-Ozkurt | rest | 33 | 33 | 11 | 0 |
| E1_sensitivity | EC013 | ec013.157 | MVL-raw | run | 23 | 23 | 3 | 0 |
| E1_sensitivity | EC013 | ec013.157 | MVL-raw | rest | 33 | 33 | 11 | 0 |
| E1_sensitivity | EC013 | ec013.205 | APC-v1.0 | run | 8 | 8 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.205 | APC-v1.0 | rest | 9 | 9 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.205 | GLM | run | 8 | 8 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.205 | GLM | rest | 9 | 9 | 1 | 0 |
| E1_sensitivity | EC013 | ec013.205 | KLMI | run | 8 | 8 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.205 | KLMI | rest | 9 | 9 | 3 | 0 |
| E1_sensitivity | EC013 | ec013.205 | MVL-Ozkurt | run | 8 | 8 | 2 | 0 |
| E1_sensitivity | EC013 | ec013.205 | MVL-Ozkurt | rest | 9 | 9 | 4 | 0 |
| E1_sensitivity | EC013 | ec013.205 | MVL-raw | run | 8 | 8 | 2 | 0 |
| E1_sensitivity | EC013 | ec013.205 | MVL-raw | rest | 9 | 9 | 4 | 0 |
| E1_sensitivity | EC013 | ec013.206 | APC-v1.0 | run | 58 | 58 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.206 | APC-v1.0 | rest | 61 | 60 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.206 | GLM | run | 58 | 58 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.206 | GLM | rest | 61 | 61 | 4 | 0 |
| E1_sensitivity | EC013 | ec013.206 | KLMI | run | 58 | 58 | 2 | 0 |
| E1_sensitivity | EC013 | ec013.206 | KLMI | rest | 61 | 61 | 7 | 0 |
| E1_sensitivity | EC013 | ec013.206 | MVL-Ozkurt | run | 58 | 58 | 8 | 0 |
| E1_sensitivity | EC013 | ec013.206 | MVL-Ozkurt | rest | 61 | 61 | 9 | 0 |
| E1_sensitivity | EC013 | ec013.206 | MVL-raw | run | 58 | 58 | 8 | 0 |
| E1_sensitivity | EC013 | ec013.206 | MVL-raw | rest | 61 | 61 | 7 | 0 |
| E1_sensitivity | EC013 | ec013.208 | APC-v1.0 | run | 44 | 44 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.208 | APC-v1.0 | rest | 53 | 53 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.208 | GLM | run | 44 | 44 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.208 | GLM | rest | 53 | 53 | 5 | 0 |
| E1_sensitivity | EC013 | ec013.208 | KLMI | run | 44 | 44 | 2 | 0 |
| E1_sensitivity | EC013 | ec013.208 | KLMI | rest | 53 | 53 | 12 | 0 |
| E1_sensitivity | EC013 | ec013.208 | MVL-Ozkurt | run | 44 | 44 | 16 | 0 |
| E1_sensitivity | EC013 | ec013.208 | MVL-Ozkurt | rest | 53 | 53 | 15 | 0 |
| E1_sensitivity | EC013 | ec013.208 | MVL-raw | run | 44 | 44 | 14 | 0 |
| E1_sensitivity | EC013 | ec013.208 | MVL-raw | rest | 53 | 53 | 9 | 0 |
| E1_sensitivity | EC013 | ec013.251 | APC-v1.0 | run | 54 | 54 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.251 | APC-v1.0 | rest | 65 | 61 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.251 | GLM | run | 54 | 54 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.251 | GLM | rest | 65 | 65 | 8 | 0 |
| E1_sensitivity | EC013 | ec013.251 | KLMI | run | 54 | 54 | 6 | 0 |
| E1_sensitivity | EC013 | ec013.251 | KLMI | rest | 65 | 65 | 22 | 0 |
| E1_sensitivity | EC013 | ec013.251 | MVL-Ozkurt | run | 54 | 54 | 14 | 0 |
| E1_sensitivity | EC013 | ec013.251 | MVL-Ozkurt | rest | 65 | 65 | 17 | 0 |
| E1_sensitivity | EC013 | ec013.251 | MVL-raw | run | 54 | 54 | 11 | 0 |
| E1_sensitivity | EC013 | ec013.251 | MVL-raw | rest | 65 | 65 | 12 | 0 |
| E1_sensitivity | EC013 | ec013.252 | APC-v1.0 | run | 32 | 32 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.252 | APC-v1.0 | rest | 64 | 60 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.252 | GLM | run | 32 | 32 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.252 | GLM | rest | 64 | 64 | 3 | 0 |
| E1_sensitivity | EC013 | ec013.252 | KLMI | run | 32 | 32 | 5 | 0 |
| E1_sensitivity | EC013 | ec013.252 | KLMI | rest | 64 | 64 | 19 | 0 |
| E1_sensitivity | EC013 | ec013.252 | MVL-Ozkurt | run | 32 | 32 | 6 | 0 |
| E1_sensitivity | EC013 | ec013.252 | MVL-Ozkurt | rest | 64 | 64 | 17 | 0 |
| E1_sensitivity | EC013 | ec013.252 | MVL-raw | run | 32 | 32 | 9 | 0 |
| E1_sensitivity | EC013 | ec013.252 | MVL-raw | rest | 64 | 64 | 16 | 0 |
| E1_sensitivity | EC013 | ec013.374 | APC-v1.0 | run | 88 | 88 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.374 | APC-v1.0 | rest | 77 | 75 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.374 | GLM | run | 88 | 88 | 1 | 0 |
| E1_sensitivity | EC013 | ec013.374 | GLM | rest | 77 | 77 | 9 | 1 |
| E1_sensitivity | EC013 | ec013.374 | KLMI | run | 88 | 88 | 14 | 0 |
| E1_sensitivity | EC013 | ec013.374 | KLMI | rest | 77 | 77 | 22 | 0 |
| E1_sensitivity | EC013 | ec013.374 | MVL-Ozkurt | run | 88 | 88 | 12 | 0 |
| E1_sensitivity | EC013 | ec013.374 | MVL-Ozkurt | rest | 77 | 77 | 20 | 0 |
| E1_sensitivity | EC013 | ec013.374 | MVL-raw | run | 88 | 88 | 15 | 0 |
| E1_sensitivity | EC013 | ec013.374 | MVL-raw | rest | 77 | 77 | 20 | 0 |
| E1_sensitivity | EC013 | ec013.375 | APC-v1.0 | run | 68 | 68 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.375 | APC-v1.0 | rest | 137 | 128 | 0 | 0 |
| E1_sensitivity | EC013 | ec013.375 | GLM | run | 68 | 68 | 1 | 0 |
| E1_sensitivity | EC013 | ec013.375 | GLM | rest | 137 | 137 | 18 | 0 |
| E1_sensitivity | EC013 | ec013.375 | KLMI | run | 68 | 68 | 9 | 0 |
| E1_sensitivity | EC013 | ec013.375 | KLMI | rest | 137 | 137 | 44 | 0 |
| E1_sensitivity | EC013 | ec013.375 | MVL-Ozkurt | run | 68 | 68 | 14 | 0 |
| E1_sensitivity | EC013 | ec013.375 | MVL-Ozkurt | rest | 137 | 137 | 34 | 0 |
| E1_sensitivity | EC013 | ec013.375 | MVL-raw | run | 68 | 68 | 12 | 0 |
| E1_sensitivity | EC013 | ec013.375 | MVL-raw | rest | 137 | 137 | 42 | 0 |
| EC | EC012 | ec012ec.239 | APC-v1.0 | run | 47 | 47 | 0 | 0 |
| EC | EC012 | ec012ec.239 | APC-v1.0 | rest | 34 | 33 | 0 | 0 |
| EC | EC012 | ec012ec.239 | GLM | run | 47 | 47 | 2 | 0 |
| EC | EC012 | ec012ec.239 | GLM | rest | 34 | 34 | 5 | 0 |
| EC | EC012 | ec012ec.239 | KLMI | run | 47 | 47 | 18 | 0 |
| EC | EC012 | ec012ec.239 | KLMI | rest | 34 | 34 | 22 | 0 |
| EC | EC012 | ec012ec.239 | MVL-Ozkurt | run | 47 | 47 | 15 | 0 |
| EC | EC012 | ec012ec.239 | MVL-Ozkurt | rest | 34 | 34 | 8 | 0 |
| EC | EC012 | ec012ec.239 | MVL-raw | run | 47 | 47 | 16 | 0 |
| EC | EC012 | ec012ec.239 | MVL-raw | rest | 34 | 34 | 9 | 0 |
| EC | EC012 | ec012ec.240 | APC-v1.0 | run | 66 | 66 | 0 | 0 |
| EC | EC012 | ec012ec.240 | APC-v1.0 | rest | 17 | 15 | 0 | 0 |
| EC | EC012 | ec012ec.240 | GLM | run | 66 | 66 | 3 | 1 |
| EC | EC012 | ec012ec.240 | GLM | rest | 17 | 17 | 5 | 0 |
| EC | EC012 | ec012ec.240 | KLMI | run | 66 | 66 | 17 | 0 |
| EC | EC012 | ec012ec.240 | KLMI | rest | 17 | 17 | 11 | 0 |
| EC | EC012 | ec012ec.240 | MVL-Ozkurt | run | 66 | 66 | 15 | 0 |
| EC | EC012 | ec012ec.240 | MVL-Ozkurt | rest | 17 | 17 | 9 | 0 |
| EC | EC012 | ec012ec.240 | MVL-raw | run | 66 | 66 | 15 | 1 |
| EC | EC012 | ec012ec.240 | MVL-raw | rest | 17 | 17 | 6 | 0 |
| EC | EC012 | ec012ec.269 | APC-v1.0 | run | 38 | 38 | 0 | 0 |
| EC | EC012 | ec012ec.269 | APC-v1.0 | rest | 48 | 45 | 0 | 0 |
| EC | EC012 | ec012ec.269 | GLM | run | 38 | 38 | 4 | 1 |
| EC | EC012 | ec012ec.269 | GLM | rest | 48 | 48 | 9 | 0 |
| EC | EC012 | ec012ec.269 | KLMI | run | 38 | 38 | 11 | 0 |
| EC | EC012 | ec012ec.269 | KLMI | rest | 48 | 48 | 28 | 0 |
| EC | EC012 | ec012ec.269 | MVL-Ozkurt | run | 38 | 38 | 9 | 1 |
| EC | EC012 | ec012ec.269 | MVL-Ozkurt | rest | 48 | 48 | 15 | 0 |
| EC | EC012 | ec012ec.269 | MVL-raw | run | 38 | 38 | 10 | 3 |
| EC | EC012 | ec012ec.269 | MVL-raw | rest | 48 | 48 | 15 | 0 |
| EC | EC012 | ec012ec.270 | APC-v1.0 | run | 24 | 24 | 0 | 0 |
| EC | EC012 | ec012ec.270 | APC-v1.0 | rest | 49 | 40 | 0 | 0 |
| EC | EC012 | ec012ec.270 | GLM | run | 24 | 24 | 2 | 1 |
| EC | EC012 | ec012ec.270 | GLM | rest | 49 | 49 | 12 | 1 |
| EC | EC012 | ec012ec.270 | KLMI | run | 24 | 24 | 10 | 0 |
| EC | EC012 | ec012ec.270 | KLMI | rest | 49 | 49 | 20 | 0 |
| EC | EC012 | ec012ec.270 | MVL-Ozkurt | run | 24 | 24 | 12 | 0 |
| EC | EC012 | ec012ec.270 | MVL-Ozkurt | rest | 49 | 49 | 7 | 0 |
| EC | EC012 | ec012ec.270 | MVL-raw | run | 24 | 24 | 9 | 0 |
| EC | EC012 | ec012ec.270 | MVL-raw | rest | 49 | 49 | 11 | 1 |
| EC | EC012 | ec012ec.271 | APC-v1.0 | run | 35 | 35 | 0 | 0 |
| EC | EC012 | ec012ec.271 | APC-v1.0 | rest | 21 | 16 | 0 | 0 |
| EC | EC012 | ec012ec.271 | GLM | run | 35 | 35 | 7 | 2 |
| EC | EC012 | ec012ec.271 | GLM | rest | 21 | 21 | 5 | 0 |
| EC | EC012 | ec012ec.271 | KLMI | run | 35 | 35 | 14 | 0 |
| EC | EC012 | ec012ec.271 | KLMI | rest | 21 | 21 | 14 | 0 |
| EC | EC012 | ec012ec.271 | MVL-Ozkurt | run | 35 | 35 | 12 | 2 |
| EC | EC012 | ec012ec.271 | MVL-Ozkurt | rest | 21 | 21 | 8 | 0 |
| EC | EC012 | ec012ec.271 | MVL-raw | run | 35 | 35 | 11 | 2 |
| EC | EC012 | ec012ec.271 | MVL-raw | rest | 21 | 21 | 5 | 0 |
| EC | EC012 | ec012ec.356 | APC-v1.0 | run | 40 | 40 | 0 | 0 |
| EC | EC012 | ec012ec.356 | APC-v1.0 | rest | 50 | 46 | 0 | 0 |
| EC | EC012 | ec012ec.356 | GLM | run | 40 | 40 | 1 | 1 |
| EC | EC012 | ec012ec.356 | GLM | rest | 50 | 50 | 5 | 0 |
| EC | EC012 | ec012ec.356 | KLMI | run | 40 | 40 | 11 | 0 |
| EC | EC012 | ec012ec.356 | KLMI | rest | 50 | 50 | 14 | 0 |
| EC | EC012 | ec012ec.356 | MVL-Ozkurt | run | 40 | 40 | 12 | 0 |
| EC | EC012 | ec012ec.356 | MVL-Ozkurt | rest | 50 | 50 | 6 | 0 |
| EC | EC012 | ec012ec.356 | MVL-raw | run | 40 | 40 | 11 | 0 |
| EC | EC012 | ec012ec.356 | MVL-raw | rest | 50 | 50 | 9 | 0 |
| EC | EC012 | ec012ec.357 | APC-v1.0 | run | 38 | 38 | 0 | 0 |
| EC | EC012 | ec012ec.357 | APC-v1.0 | rest | 36 | 34 | 0 | 0 |
| EC | EC012 | ec012ec.357 | GLM | run | 38 | 38 | 9 | 0 |
| EC | EC012 | ec012ec.357 | GLM | rest | 36 | 36 | 9 | 1 |
| EC | EC012 | ec012ec.357 | KLMI | run | 38 | 38 | 18 | 0 |
| EC | EC012 | ec012ec.357 | KLMI | rest | 36 | 36 | 14 | 0 |
| EC | EC012 | ec012ec.357 | MVL-Ozkurt | run | 38 | 38 | 15 | 0 |
| EC | EC012 | ec012ec.357 | MVL-Ozkurt | rest | 36 | 36 | 8 | 0 |
| EC | EC012 | ec012ec.357 | MVL-raw | run | 38 | 38 | 11 | 0 |
| EC | EC012 | ec012ec.357 | MVL-raw | rest | 36 | 36 | 7 | 0 |
| EC | EC012 | ec012ec.375 | APC-v1.0 | run | 37 | 37 | 0 | 0 |
| EC | EC012 | ec012ec.375 | APC-v1.0 | rest | 32 | 31 | 0 | 0 |
| EC | EC012 | ec012ec.375 | GLM | run | 37 | 37 | 0 | 0 |
| EC | EC012 | ec012ec.375 | GLM | rest | 32 | 32 | 4 | 1 |
| EC | EC012 | ec012ec.375 | KLMI | run | 37 | 37 | 11 | 0 |
| EC | EC012 | ec012ec.375 | KLMI | rest | 32 | 32 | 14 | 0 |
| EC | EC012 | ec012ec.375 | MVL-Ozkurt | run | 37 | 37 | 15 | 0 |
| EC | EC012 | ec012ec.375 | MVL-Ozkurt | rest | 32 | 32 | 9 | 0 |
| EC | EC012 | ec012ec.375 | MVL-raw | run | 37 | 37 | 15 | 0 |
| EC | EC012 | ec012ec.375 | MVL-raw | rest | 32 | 32 | 7 | 0 |
| EC | EC012 | ec012ec.444 | APC-v1.0 | run | 30 | 30 | 0 | 0 |
| EC | EC012 | ec012ec.444 | APC-v1.0 | rest | 46 | 40 | 0 | 0 |
| EC | EC012 | ec012ec.444 | GLM | run | 30 | 30 | 4 | 0 |
| EC | EC012 | ec012ec.444 | GLM | rest | 46 | 46 | 7 | 1 |
| EC | EC012 | ec012ec.444 | KLMI | run | 30 | 30 | 9 | 0 |
| EC | EC012 | ec012ec.444 | KLMI | rest | 46 | 46 | 17 | 0 |
| EC | EC012 | ec012ec.444 | MVL-Ozkurt | run | 30 | 30 | 9 | 0 |
| EC | EC012 | ec012ec.444 | MVL-Ozkurt | rest | 46 | 46 | 13 | 1 |
| EC | EC012 | ec012ec.444 | MVL-raw | run | 30 | 30 | 9 | 0 |
| EC | EC012 | ec012ec.444 | MVL-raw | rest | 46 | 46 | 10 | 1 |
| EC | EC013 | ec013.156 | APC-v1.0 | run | 56 | 56 | 0 | 0 |
| EC | EC013 | ec013.156 | APC-v1.0 | rest | 56 | 55 | 0 | 0 |
| EC | EC013 | ec013.156 | GLM | run | 56 | 56 | 1 | 0 |
| EC | EC013 | ec013.156 | GLM | rest | 56 | 56 | 2 | 0 |
| EC | EC013 | ec013.156 | KLMI | run | 56 | 56 | 7 | 0 |
| EC | EC013 | ec013.156 | KLMI | rest | 56 | 56 | 11 | 0 |
| EC | EC013 | ec013.156 | MVL-Ozkurt | run | 56 | 56 | 15 | 0 |
| EC | EC013 | ec013.156 | MVL-Ozkurt | rest | 56 | 56 | 11 | 0 |
| EC | EC013 | ec013.156 | MVL-raw | run | 56 | 56 | 10 | 1 |
| EC | EC013 | ec013.156 | MVL-raw | rest | 56 | 56 | 10 | 0 |
| EC | EC013 | ec013.157 | APC-v1.0 | run | 23 | 23 | 0 | 0 |
| EC | EC013 | ec013.157 | APC-v1.0 | rest | 33 | 33 | 0 | 0 |
| EC | EC013 | ec013.157 | GLM | run | 23 | 23 | 0 | 0 |
| EC | EC013 | ec013.157 | GLM | rest | 33 | 33 | 5 | 0 |
| EC | EC013 | ec013.157 | KLMI | run | 23 | 23 | 2 | 0 |
| EC | EC013 | ec013.157 | KLMI | rest | 33 | 33 | 9 | 0 |
| EC | EC013 | ec013.157 | MVL-Ozkurt | run | 23 | 23 | 2 | 0 |
| EC | EC013 | ec013.157 | MVL-Ozkurt | rest | 33 | 33 | 12 | 0 |
| EC | EC013 | ec013.157 | MVL-raw | run | 23 | 23 | 3 | 0 |
| EC | EC013 | ec013.157 | MVL-raw | rest | 33 | 33 | 12 | 0 |
| EC | EC013 | ec013.205 | APC-v1.0 | run | 8 | 8 | 0 | 0 |
| EC | EC013 | ec013.205 | APC-v1.0 | rest | 9 | 9 | 0 | 0 |
| EC | EC013 | ec013.205 | GLM | run | 8 | 8 | 0 | 0 |
| EC | EC013 | ec013.205 | GLM | rest | 9 | 9 | 2 | 0 |
| EC | EC013 | ec013.205 | KLMI | run | 8 | 8 | 0 | 0 |
| EC | EC013 | ec013.205 | KLMI | rest | 9 | 9 | 1 | 0 |
| EC | EC013 | ec013.205 | MVL-Ozkurt | run | 8 | 8 | 2 | 0 |
| EC | EC013 | ec013.205 | MVL-Ozkurt | rest | 9 | 9 | 4 | 0 |
| EC | EC013 | ec013.205 | MVL-raw | run | 8 | 8 | 2 | 0 |
| EC | EC013 | ec013.205 | MVL-raw | rest | 9 | 9 | 4 | 0 |
| EC | EC013 | ec013.206 | APC-v1.0 | run | 58 | 58 | 0 | 0 |
| EC | EC013 | ec013.206 | APC-v1.0 | rest | 61 | 61 | 0 | 0 |
| EC | EC013 | ec013.206 | GLM | run | 58 | 58 | 0 | 0 |
| EC | EC013 | ec013.206 | GLM | rest | 61 | 61 | 3 | 0 |
| EC | EC013 | ec013.206 | KLMI | run | 58 | 58 | 2 | 0 |
| EC | EC013 | ec013.206 | KLMI | rest | 61 | 61 | 10 | 0 |
| EC | EC013 | ec013.206 | MVL-Ozkurt | run | 58 | 58 | 9 | 0 |
| EC | EC013 | ec013.206 | MVL-Ozkurt | rest | 61 | 61 | 7 | 0 |
| EC | EC013 | ec013.206 | MVL-raw | run | 58 | 58 | 10 | 0 |
| EC | EC013 | ec013.206 | MVL-raw | rest | 61 | 61 | 8 | 0 |
| EC | EC013 | ec013.208 | APC-v1.0 | run | 44 | 44 | 0 | 0 |
| EC | EC013 | ec013.208 | APC-v1.0 | rest | 53 | 52 | 0 | 0 |
| EC | EC013 | ec013.208 | GLM | run | 44 | 44 | 0 | 0 |
| EC | EC013 | ec013.208 | GLM | rest | 53 | 53 | 6 | 0 |
| EC | EC013 | ec013.208 | KLMI | run | 44 | 44 | 2 | 0 |
| EC | EC013 | ec013.208 | KLMI | rest | 53 | 53 | 17 | 0 |
| EC | EC013 | ec013.208 | MVL-Ozkurt | run | 44 | 44 | 12 | 0 |
| EC | EC013 | ec013.208 | MVL-Ozkurt | rest | 53 | 53 | 15 | 0 |
| EC | EC013 | ec013.208 | MVL-raw | run | 44 | 44 | 14 | 0 |
| EC | EC013 | ec013.208 | MVL-raw | rest | 53 | 53 | 10 | 0 |
| EC | EC013 | ec013.251 | APC-v1.0 | run | 54 | 54 | 0 | 0 |
| EC | EC013 | ec013.251 | APC-v1.0 | rest | 65 | 59 | 0 | 0 |
| EC | EC013 | ec013.251 | GLM | run | 54 | 54 | 0 | 0 |
| EC | EC013 | ec013.251 | GLM | rest | 65 | 65 | 6 | 0 |
| EC | EC013 | ec013.251 | KLMI | run | 54 | 54 | 4 | 0 |
| EC | EC013 | ec013.251 | KLMI | rest | 65 | 65 | 15 | 0 |
| EC | EC013 | ec013.251 | MVL-Ozkurt | run | 54 | 54 | 12 | 0 |
| EC | EC013 | ec013.251 | MVL-Ozkurt | rest | 65 | 65 | 16 | 0 |
| EC | EC013 | ec013.251 | MVL-raw | run | 54 | 54 | 10 | 0 |
| EC | EC013 | ec013.251 | MVL-raw | rest | 65 | 65 | 12 | 0 |
| EC | EC013 | ec013.252 | APC-v1.0 | run | 32 | 32 | 0 | 0 |
| EC | EC013 | ec013.252 | APC-v1.0 | rest | 64 | 59 | 0 | 0 |
| EC | EC013 | ec013.252 | GLM | run | 32 | 32 | 0 | 0 |
| EC | EC013 | ec013.252 | GLM | rest | 64 | 64 | 5 | 0 |
| EC | EC013 | ec013.252 | KLMI | run | 32 | 32 | 4 | 0 |
| EC | EC013 | ec013.252 | KLMI | rest | 64 | 64 | 21 | 0 |
| EC | EC013 | ec013.252 | MVL-Ozkurt | run | 32 | 32 | 9 | 0 |
| EC | EC013 | ec013.252 | MVL-Ozkurt | rest | 64 | 64 | 22 | 0 |
| EC | EC013 | ec013.252 | MVL-raw | run | 32 | 32 | 9 | 0 |
| EC | EC013 | ec013.252 | MVL-raw | rest | 64 | 64 | 17 | 0 |
| EC | EC013 | ec013.374 | APC-v1.0 | run | 88 | 88 | 0 | 0 |
| EC | EC013 | ec013.374 | APC-v1.0 | rest | 77 | 75 | 0 | 0 |
| EC | EC013 | ec013.374 | GLM | run | 88 | 88 | 0 | 0 |
| EC | EC013 | ec013.374 | GLM | rest | 77 | 77 | 7 | 0 |
| EC | EC013 | ec013.374 | KLMI | run | 88 | 88 | 5 | 0 |
| EC | EC013 | ec013.374 | KLMI | rest | 77 | 77 | 20 | 0 |
| EC | EC013 | ec013.374 | MVL-Ozkurt | run | 88 | 88 | 18 | 0 |
| EC | EC013 | ec013.374 | MVL-Ozkurt | rest | 77 | 77 | 19 | 0 |
| EC | EC013 | ec013.374 | MVL-raw | run | 88 | 88 | 17 | 0 |
| EC | EC013 | ec013.374 | MVL-raw | rest | 77 | 77 | 18 | 1 |
| EC | EC013 | ec013.375 | APC-v1.0 | run | 68 | 68 | 0 | 0 |
| EC | EC013 | ec013.375 | APC-v1.0 | rest | 137 | 130 | 0 | 0 |
| EC | EC013 | ec013.375 | GLM | run | 68 | 68 | 0 | 0 |
| EC | EC013 | ec013.375 | GLM | rest | 137 | 137 | 21 | 1 |
| EC | EC013 | ec013.375 | KLMI | run | 68 | 68 | 7 | 0 |
| EC | EC013 | ec013.375 | KLMI | rest | 137 | 137 | 41 | 0 |
| EC | EC013 | ec013.375 | MVL-Ozkurt | run | 68 | 68 | 10 | 0 |
| EC | EC013 | ec013.375 | MVL-Ozkurt | rest | 137 | 137 | 29 | 1 |
| EC | EC013 | ec013.375 | MVL-raw | run | 68 | 68 | 16 | 0 |
| EC | EC013 | ec013.375 | MVL-raw | rest | 137 | 137 | 26 | 0 |

POST HOC fP spread table:
| analysis | animal | session | method | state | n_valid | fp_sd | fp_iqr | fp_mad |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | EC013 | ec013.156 | APC-v1.0 | run | 56 | 0.261054 | 0.349446 | 0.1729 |
| CA1 | EC013 | ec013.156 | APC-v1.0 | rest | 54 | 0.863679 | 0.48995 | 0.24907 |
| CA1 | EC013 | ec013.156 | GLM | run | 56 | 2.55123 | 5 | 1.5 |
| CA1 | EC013 | ec013.156 | GLM | rest | 56 | 2.2381 | 3.5 | 1.5 |
| CA1 | EC013 | ec013.156 | KLMI | run | 56 | 1.06585 | 0.5 | 0 |
| CA1 | EC013 | ec013.156 | KLMI | rest | 56 | 1.25719 | 1 | 0 |
| CA1 | EC013 | ec013.156 | MVL-Ozkurt | run | 56 | 1.94834 | 1.5 | 0.5 |
| CA1 | EC013 | ec013.156 | MVL-Ozkurt | rest | 56 | 2.34505 | 3 | 0.5 |
| CA1 | EC013 | ec013.156 | MVL-raw | run | 56 | 2.25211 | 2.125 | 1 |
| CA1 | EC013 | ec013.156 | MVL-raw | rest | 56 | 2.04201 | 2.625 | 0.5 |
| CA1 | EC013 | ec013.157 | APC-v1.0 | run | 23 | 0.254058 | 0.241295 | 0.130679 |
| CA1 | EC013 | ec013.157 | APC-v1.0 | rest | 31 | 1.00891 | 0.989799 | 0.53653 |
| CA1 | EC013 | ec013.157 | GLM | run | 23 | 2.68192 | 4.75 | 1.5 |
| CA1 | EC013 | ec013.157 | GLM | rest | 33 | 2.2857 | 4 | 2 |
| CA1 | EC013 | ec013.157 | KLMI | run | 23 | 1.14121 | 0.5 | 0 |
| CA1 | EC013 | ec013.157 | KLMI | rest | 33 | 1.45497 | 2 | 0 |
| CA1 | EC013 | ec013.157 | MVL-Ozkurt | run | 23 | 1.80661 | 1 | 0.5 |
| CA1 | EC013 | ec013.157 | MVL-Ozkurt | rest | 33 | 1.81155 | 3 | 0.5 |
| CA1 | EC013 | ec013.157 | MVL-raw | run | 23 | 1.57926 | 1.5 | 1 |
| CA1 | EC013 | ec013.157 | MVL-raw | rest | 33 | 2.18672 | 2.5 | 0.5 |
| CA1 | EC013 | ec013.205 | APC-v1.0 | run | 8 | 0.232265 | 0.317304 | 0.154115 |
| CA1 | EC013 | ec013.205 | APC-v1.0 | rest | 9 | 0.302364 | 0.346171 | 0.178483 |
| CA1 | EC013 | ec013.205 | GLM | run | 8 | 1.69031 | 1.75 | 1 |
| CA1 | EC013 | ec013.205 | GLM | rest | 9 | 2.80624 | 4 | 2.5 |
| CA1 | EC013 | ec013.205 | KLMI | run | 8 | 1.88982 | 2.5 | 1 |
| CA1 | EC013 | ec013.205 | KLMI | rest | 9 | 1.50923 | 2 | 0 |
| CA1 | EC013 | ec013.205 | MVL-Ozkurt | run | 8 | 1.37419 | 1.75 | 0.75 |
| CA1 | EC013 | ec013.205 | MVL-Ozkurt | rest | 9 | 2.30639 | 4 | 0.5 |
| CA1 | EC013 | ec013.205 | MVL-raw | run | 8 | 2.18661 | 2.375 | 1 |
| CA1 | EC013 | ec013.205 | MVL-raw | rest | 9 | 1.37184 | 2 | 1 |
| CA1 | EC013 | ec013.206 | APC-v1.0 | run | 58 | 0.166374 | 0.19684 | 0.0978196 |
| CA1 | EC013 | ec013.206 | APC-v1.0 | rest | 59 | 0.716699 | 0.772069 | 0.315329 |
| CA1 | EC013 | ec013.206 | GLM | run | 58 | 2.21193 | 4 | 1.75 |
| CA1 | EC013 | ec013.206 | GLM | rest | 61 | 2.27648 | 4.5 | 2 |
| CA1 | EC013 | ec013.206 | KLMI | run | 58 | 1.23262 | 1 | 0.5 |
| CA1 | EC013 | ec013.206 | KLMI | rest | 61 | 1.58563 | 1 | 0 |
| CA1 | EC013 | ec013.206 | MVL-Ozkurt | run | 58 | 1.74139 | 1 | 0.5 |
| CA1 | EC013 | ec013.206 | MVL-Ozkurt | rest | 61 | 1.98636 | 2 | 0.5 |
| CA1 | EC013 | ec013.206 | MVL-raw | run | 58 | 1.8373 | 1.375 | 0.5 |
| CA1 | EC013 | ec013.206 | MVL-raw | rest | 61 | 2.25547 | 2 | 0.5 |
| CA1 | EC013 | ec013.208 | APC-v1.0 | run | 43 | 4.30644 | 4.7031 | 2.38869 |
| CA1 | EC013 | ec013.208 | APC-v1.0 | rest | 48 | 5.35075 | 5.98817 | 2.73576 |
| CA1 | EC013 | ec013.208 | GLM | run | 44 | 2.20042 | 3.25 | 1.75 |
| CA1 | EC013 | ec013.208 | GLM | rest | 53 | 1.97251 | 2.5 | 1 |
| CA1 | EC013 | ec013.208 | KLMI | run | 44 | 1.06965 | 1 | 0.5 |
| CA1 | EC013 | ec013.208 | KLMI | rest | 53 | 1.07121 | 0.5 | 0.5 |
| CA1 | EC013 | ec013.208 | MVL-Ozkurt | run | 44 | 1.63678 | 1.25 | 0.5 |
| CA1 | EC013 | ec013.208 | MVL-Ozkurt | rest | 53 | 1.72901 | 1 | 0.5 |
| CA1 | EC013 | ec013.208 | MVL-raw | run | 44 | 1.57926 | 1.625 | 0.5 |
| CA1 | EC013 | ec013.208 | MVL-raw | rest | 53 | 1.84136 | 2 | 0.5 |
| CA1 | EC013 | ec013.251 | APC-v1.0 | run | 54 | 0.296348 | 0.313594 | 0.140948 |
| CA1 | EC013 | ec013.251 | APC-v1.0 | rest | 60 | 1.05939 | 1.06488 | 0.545099 |
| CA1 | EC013 | ec013.251 | GLM | run | 54 | 2.31365 | 4 | 2 |
| CA1 | EC013 | ec013.251 | GLM | rest | 65 | 2.37546 | 4 | 2 |
| CA1 | EC013 | ec013.251 | KLMI | run | 54 | 1.27729 | 1 | 0.5 |
| CA1 | EC013 | ec013.251 | KLMI | rest | 65 | 1.02364 | 0.5 | 0 |
| CA1 | EC013 | ec013.251 | MVL-Ozkurt | run | 54 | 1.66436 | 2 | 0.5 |
| CA1 | EC013 | ec013.251 | MVL-Ozkurt | rest | 65 | 1.67231 | 1.5 | 0.5 |
| CA1 | EC013 | ec013.251 | MVL-raw | run | 54 | 1.88719 | 1.5 | 0.5 |
| CA1 | EC013 | ec013.251 | MVL-raw | rest | 65 | 2.11371 | 2 | 0.5 |
| CA1 | EC013 | ec013.252 | APC-v1.0 | run | 32 | 0.365392 | 0.303782 | 0.15436 |
| CA1 | EC013 | ec013.252 | APC-v1.0 | rest | 60 | 1.13631 | 1.24883 | 0.656699 |
| CA1 | EC013 | ec013.252 | GLM | run | 32 | 2.20314 | 2.625 | 1.5 |
| CA1 | EC013 | ec013.252 | GLM | rest | 64 | 2.12586 | 3.125 | 1.5 |
| CA1 | EC013 | ec013.252 | KLMI | run | 32 | 1.06066 | 0.5 | 0 |
| CA1 | EC013 | ec013.252 | KLMI | rest | 64 | 1.52034 | 1.5 | 0.5 |
| CA1 | EC013 | ec013.252 | MVL-Ozkurt | run | 32 | 1.57475 | 1 | 0 |
| CA1 | EC013 | ec013.252 | MVL-Ozkurt | rest | 64 | 1.51806 | 2 | 0.75 |
| CA1 | EC013 | ec013.252 | MVL-raw | run | 32 | 1.96517 | 1 | 0.5 |
| CA1 | EC013 | ec013.252 | MVL-raw | rest | 64 | 2.18802 | 3 | 1 |
| CA1 | EC013 | ec013.374 | APC-v1.0 | run | 88 | 0.300006 | 0.313263 | 0.144132 |
| CA1 | EC013 | ec013.374 | APC-v1.0 | rest | 76 | 1.09341 | 1.26243 | 0.610459 |
| CA1 | EC013 | ec013.374 | GLM | run | 88 | 2.10249 | 3 | 1.25 |
| CA1 | EC013 | ec013.374 | GLM | rest | 77 | 1.94169 | 3 | 1.5 |
| CA1 | EC013 | ec013.374 | KLMI | run | 88 | 1.33984 | 1 | 0.25 |
| CA1 | EC013 | ec013.374 | KLMI | rest | 77 | 1.49034 | 2.5 | 0.5 |
| CA1 | EC013 | ec013.374 | MVL-Ozkurt | run | 88 | 1.38509 | 1.125 | 0.5 |
| CA1 | EC013 | ec013.374 | MVL-Ozkurt | rest | 77 | 1.73975 | 3 | 1 |
| CA1 | EC013 | ec013.374 | MVL-raw | run | 88 | 1.8266 | 2 | 0.5 |
| CA1 | EC013 | ec013.374 | MVL-raw | rest | 77 | 1.99962 | 3 | 1.5 |
| CA1 | EC013 | ec013.375 | APC-v1.0 | run | 61 | 4.65202 | 4.96215 | 2.28427 |
| CA1 | EC013 | ec013.375 | APC-v1.0 | rest | 120 | 6.67702 | 8.40087 | 3.74138 |
| CA1 | EC013 | ec013.375 | GLM | run | 68 | 1.8275 | 2.625 | 1.5 |
| CA1 | EC013 | ec013.375 | GLM | rest | 137 | 2.30498 | 3.5 | 2 |
| CA1 | EC013 | ec013.375 | KLMI | run | 68 | 1.02736 | 1 | 0.5 |
| CA1 | EC013 | ec013.375 | KLMI | rest | 137 | 0.975962 | 1 | 0.5 |
| CA1 | EC013 | ec013.375 | MVL-Ozkurt | run | 68 | 1.68014 | 1.625 | 0.5 |
| CA1 | EC013 | ec013.375 | MVL-Ozkurt | rest | 137 | 1.70905 | 1 | 0.5 |
| CA1 | EC013 | ec013.375 | MVL-raw | run | 68 | 1.58287 | 2 | 0.5 |
| CA1 | EC013 | ec013.375 | MVL-raw | rest | 137 | 1.58585 | 1 | 0.5 |
| E1_sensitivity | EC013 | ec013.156 | APC-v1.0 | run | 56 | 0.277743 | 0.329987 | 0.176486 |
| E1_sensitivity | EC013 | ec013.156 | APC-v1.0 | rest | 56 | 0.566723 | 0.320715 | 0.189382 |
| E1_sensitivity | EC013 | ec013.156 | GLM | run | 56 | 1.46604 | 2.125 | 1 |
| E1_sensitivity | EC013 | ec013.156 | GLM | rest | 56 | 1.27917 | 2 | 1 |
| E1_sensitivity | EC013 | ec013.156 | KLMI | run | 56 | 1.69405 | 3 | 1.75 |
| E1_sensitivity | EC013 | ec013.156 | KLMI | rest | 56 | 1.09036 | 1.625 | 1 |
| E1_sensitivity | EC013 | ec013.156 | MVL-Ozkurt | run | 56 | 1.87836 | 4 | 2 |
| E1_sensitivity | EC013 | ec013.156 | MVL-Ozkurt | rest | 56 | 1.72378 | 2.5 | 1 |
| E1_sensitivity | EC013 | ec013.156 | MVL-raw | run | 56 | 1.65449 | 3 | 1.25 |
| E1_sensitivity | EC013 | ec013.156 | MVL-raw | rest | 56 | 1.65004 | 2.5 | 1.5 |
| E1_sensitivity | EC013 | ec013.157 | APC-v1.0 | run | 23 | 0.283746 | 0.269222 | 0.144649 |
| E1_sensitivity | EC013 | ec013.157 | APC-v1.0 | rest | 33 | 0.906674 | 0.722042 | 0.344559 |
| E1_sensitivity | EC013 | ec013.157 | GLM | run | 23 | 1.21054 | 2 | 1 |
| E1_sensitivity | EC013 | ec013.157 | GLM | rest | 33 | 1.77432 | 2.5 | 1.5 |
| E1_sensitivity | EC013 | ec013.157 | KLMI | run | 23 | 1.69135 | 2.75 | 1 |
| E1_sensitivity | EC013 | ec013.157 | KLMI | rest | 33 | 1.26749 | 2.5 | 1 |
| E1_sensitivity | EC013 | ec013.157 | MVL-Ozkurt | run | 23 | 1.85997 | 3.25 | 1.5 |
| E1_sensitivity | EC013 | ec013.157 | MVL-Ozkurt | rest | 33 | 1.2551 | 2 | 1 |
| E1_sensitivity | EC013 | ec013.157 | MVL-raw | run | 23 | 1.83671 | 3 | 1.5 |
| E1_sensitivity | EC013 | ec013.157 | MVL-raw | rest | 33 | 1.4442 | 2.5 | 1 |
| E1_sensitivity | EC013 | ec013.205 | APC-v1.0 | run | 8 | 0.231492 | 0.306033 | 0.145172 |
| E1_sensitivity | EC013 | ec013.205 | APC-v1.0 | rest | 9 | 0.376469 | 0.190361 | 0.152331 |
| E1_sensitivity | EC013 | ec013.205 | GLM | run | 8 | 1.0155 | 1.25 | 0.75 |
| E1_sensitivity | EC013 | ec013.205 | GLM | rest | 9 | 1.34629 | 1.5 | 1 |
| E1_sensitivity | EC013 | ec013.205 | KLMI | run | 8 | 0.92582 | 1 | 0.5 |
| E1_sensitivity | EC013 | ec013.205 | KLMI | rest | 9 | 1.38694 | 2.5 | 1 |
| E1_sensitivity | EC013 | ec013.205 | MVL-Ozkurt | run | 8 | 1.84076 | 2.5 | 1.25 |
| E1_sensitivity | EC013 | ec013.205 | MVL-Ozkurt | rest | 9 | 1.73205 | 2.5 | 0.5 |
| E1_sensitivity | EC013 | ec013.205 | MVL-raw | run | 8 | 1.43303 | 1.5 | 0.5 |
| E1_sensitivity | EC013 | ec013.205 | MVL-raw | rest | 9 | 1.40188 | 1.5 | 0.5 |
| E1_sensitivity | EC013 | ec013.206 | APC-v1.0 | run | 58 | 0.164218 | 0.22403 | 0.107106 |
| E1_sensitivity | EC013 | ec013.206 | APC-v1.0 | rest | 60 | 0.518467 | 0.515149 | 0.267326 |
| E1_sensitivity | EC013 | ec013.206 | GLM | run | 58 | 0.97523 | 1.5 | 1 |
| E1_sensitivity | EC013 | ec013.206 | GLM | rest | 61 | 1.5766 | 2 | 1 |
| E1_sensitivity | EC013 | ec013.206 | KLMI | run | 58 | 1.34833 | 2 | 1 |
| E1_sensitivity | EC013 | ec013.206 | KLMI | rest | 61 | 1.34342 | 2 | 1 |
| E1_sensitivity | EC013 | ec013.206 | MVL-Ozkurt | run | 58 | 1.77917 | 2.875 | 1.5 |
| E1_sensitivity | EC013 | ec013.206 | MVL-Ozkurt | rest | 61 | 1.44446 | 2.5 | 1 |
| E1_sensitivity | EC013 | ec013.206 | MVL-raw | run | 58 | 1.82168 | 3.5 | 1.75 |
| E1_sensitivity | EC013 | ec013.206 | MVL-raw | rest | 61 | 1.56756 | 2 | 1 |
| E1_sensitivity | EC013 | ec013.208 | APC-v1.0 | run | 44 | 0.314036 | 0.373714 | 0.171722 |
| E1_sensitivity | EC013 | ec013.208 | APC-v1.0 | rest | 53 | 0.953102 | 0.632636 | 0.297717 |
| E1_sensitivity | EC013 | ec013.208 | GLM | run | 44 | 1.02834 | 1.5 | 1 |
| E1_sensitivity | EC013 | ec013.208 | GLM | rest | 53 | 1.47056 | 2 | 1 |
| E1_sensitivity | EC013 | ec013.208 | KLMI | run | 44 | 1.33555 | 2.125 | 1 |
| E1_sensitivity | EC013 | ec013.208 | KLMI | rest | 53 | 1.4785 | 2.5 | 1 |
| E1_sensitivity | EC013 | ec013.208 | MVL-Ozkurt | run | 44 | 1.83758 | 3.5 | 2 |
| E1_sensitivity | EC013 | ec013.208 | MVL-Ozkurt | rest | 53 | 1.67686 | 3 | 1 |
| E1_sensitivity | EC013 | ec013.208 | MVL-raw | run | 44 | 1.82228 | 3.5 | 1.5 |
| E1_sensitivity | EC013 | ec013.208 | MVL-raw | rest | 53 | 1.74431 | 3 | 1 |
| E1_sensitivity | EC013 | ec013.251 | APC-v1.0 | run | 54 | 0.278241 | 0.304947 | 0.152266 |
| E1_sensitivity | EC013 | ec013.251 | APC-v1.0 | rest | 61 | 0.887295 | 0.898021 | 0.467781 |
| E1_sensitivity | EC013 | ec013.251 | GLM | run | 54 | 1.19766 | 1.375 | 0.5 |
| E1_sensitivity | EC013 | ec013.251 | GLM | rest | 65 | 1.61301 | 2 | 1 |
| E1_sensitivity | EC013 | ec013.251 | KLMI | run | 54 | 1.70667 | 2.5 | 1.25 |
| E1_sensitivity | EC013 | ec013.251 | KLMI | rest | 65 | 1.54741 | 3 | 1 |
| E1_sensitivity | EC013 | ec013.251 | MVL-Ozkurt | run | 54 | 2.03852 | 4.375 | 2.25 |
| E1_sensitivity | EC013 | ec013.251 | MVL-Ozkurt | rest | 65 | 1.69214 | 3 | 1.5 |
| E1_sensitivity | EC013 | ec013.251 | MVL-raw | run | 54 | 2.10312 | 3.5 | 1 |
| E1_sensitivity | EC013 | ec013.251 | MVL-raw | rest | 65 | 1.51626 | 2.5 | 1.5 |
| E1_sensitivity | EC013 | ec013.252 | APC-v1.0 | run | 32 | 0.339024 | 0.283641 | 0.141866 |
| E1_sensitivity | EC013 | ec013.252 | APC-v1.0 | rest | 60 | 0.744985 | 0.962323 | 0.489381 |
| E1_sensitivity | EC013 | ec013.252 | GLM | run | 32 | 1.19548 | 2 | 1 |
| E1_sensitivity | EC013 | ec013.252 | GLM | rest | 64 | 1.63434 | 1.625 | 1 |
| E1_sensitivity | EC013 | ec013.252 | KLMI | run | 32 | 1.85289 | 3.5 | 1.75 |
| E1_sensitivity | EC013 | ec013.252 | KLMI | rest | 64 | 1.61679 | 3.125 | 1 |
| E1_sensitivity | EC013 | ec013.252 | MVL-Ozkurt | run | 32 | 1.97049 | 4.125 | 1.75 |
| E1_sensitivity | EC013 | ec013.252 | MVL-Ozkurt | rest | 64 | 1.61221 | 2.5 | 1 |
| E1_sensitivity | EC013 | ec013.252 | MVL-raw | run | 32 | 1.92808 | 3.625 | 1.75 |
| E1_sensitivity | EC013 | ec013.252 | MVL-raw | rest | 64 | 1.66918 | 2.625 | 1.25 |
| E1_sensitivity | EC013 | ec013.374 | APC-v1.0 | run | 88 | 0.284114 | 0.323082 | 0.173365 |
| E1_sensitivity | EC013 | ec013.374 | APC-v1.0 | rest | 75 | 0.902335 | 0.934193 | 0.493078 |
| E1_sensitivity | EC013 | ec013.374 | GLM | run | 88 | 1.12559 | 2 | 1 |
| E1_sensitivity | EC013 | ec013.374 | GLM | rest | 77 | 1.71435 | 2 | 1 |
| E1_sensitivity | EC013 | ec013.374 | KLMI | run | 88 | 1.66122 | 2.5 | 1 |
| E1_sensitivity | EC013 | ec013.374 | KLMI | rest | 77 | 1.31556 | 2.5 | 1 |
| E1_sensitivity | EC013 | ec013.374 | MVL-Ozkurt | run | 88 | 1.61181 | 3.5 | 1.5 |
| E1_sensitivity | EC013 | ec013.374 | MVL-Ozkurt | rest | 77 | 1.75009 | 3 | 1.5 |
| E1_sensitivity | EC013 | ec013.374 | MVL-raw | run | 88 | 1.62911 | 3.125 | 1.5 |
| E1_sensitivity | EC013 | ec013.374 | MVL-raw | rest | 77 | 1.89587 | 3 | 1.5 |
| E1_sensitivity | EC013 | ec013.375 | APC-v1.0 | run | 68 | 0.360562 | 0.460525 | 0.225878 |
| E1_sensitivity | EC013 | ec013.375 | APC-v1.0 | rest | 128 | 1.4633 | 1.23161 | 0.561176 |
| E1_sensitivity | EC013 | ec013.375 | GLM | run | 68 | 1.19251 | 2 | 0.5 |
| E1_sensitivity | EC013 | ec013.375 | GLM | rest | 137 | 1.78391 | 2.5 | 1 |
| E1_sensitivity | EC013 | ec013.375 | KLMI | run | 68 | 1.70038 | 2.5 | 1 |
| E1_sensitivity | EC013 | ec013.375 | KLMI | rest | 137 | 1.61739 | 2.5 | 1 |
| E1_sensitivity | EC013 | ec013.375 | MVL-Ozkurt | run | 68 | 1.8786 | 3.5 | 2 |
| E1_sensitivity | EC013 | ec013.375 | MVL-Ozkurt | rest | 137 | 1.81341 | 2.5 | 1 |
| E1_sensitivity | EC013 | ec013.375 | MVL-raw | run | 68 | 2.00849 | 4 | 2 |
| E1_sensitivity | EC013 | ec013.375 | MVL-raw | rest | 137 | 1.83985 | 3 | 1 |
| EC | EC012 | ec012ec.239 | APC-v1.0 | run | 47 | 0.165642 | 0.179413 | 0.0876491 |
| EC | EC012 | ec012ec.239 | APC-v1.0 | rest | 33 | 1.05661 | 0.759607 | 0.396382 |
| EC | EC012 | ec012ec.239 | GLM | run | 47 | 2.0287 | 3.5 | 2 |
| EC | EC012 | ec012ec.239 | GLM | rest | 34 | 2.17505 | 3.5 | 2 |
| EC | EC012 | ec012ec.239 | KLMI | run | 47 | 2.30838 | 3.75 | 1.5 |
| EC | EC012 | ec012ec.239 | KLMI | rest | 34 | 1.08967 | 0.5 | 0 |
| EC | EC012 | ec012ec.239 | MVL-Ozkurt | run | 47 | 2.01337 | 2.5 | 1.5 |
| EC | EC012 | ec012ec.239 | MVL-Ozkurt | rest | 34 | 1.79553 | 1.875 | 1 |
| EC | EC012 | ec012ec.239 | MVL-raw | run | 47 | 2.14926 | 2.75 | 1.5 |
| EC | EC012 | ec012ec.239 | MVL-raw | rest | 34 | 1.99381 | 3.75 | 1 |
| EC | EC012 | ec012ec.240 | APC-v1.0 | run | 66 | 0.258412 | 0.30697 | 0.156331 |
| EC | EC012 | ec012ec.240 | APC-v1.0 | rest | 15 | 1.6454 | 0.3853 | 0.234744 |
| EC | EC012 | ec012ec.240 | GLM | run | 66 | 2.05246 | 3.5 | 1.75 |
| EC | EC012 | ec012ec.240 | GLM | rest | 17 | 3.01833 | 6.5 | 2.5 |
| EC | EC012 | ec012ec.240 | KLMI | run | 66 | 2.14829 | 3.375 | 1 |
| EC | EC012 | ec012ec.240 | KLMI | rest | 17 | 1.60193 | 1 | 0 |
| EC | EC012 | ec012ec.240 | MVL-Ozkurt | run | 66 | 1.84557 | 2 | 1 |
| EC | EC012 | ec012ec.240 | MVL-Ozkurt | rest | 17 | 2.22989 | 1.5 | 0 |
| EC | EC012 | ec012ec.240 | MVL-raw | run | 66 | 2.0081 | 2 | 1 |
| EC | EC012 | ec012ec.240 | MVL-raw | rest | 17 | 1.378 | 1.5 | 0.5 |
| EC | EC012 | ec012ec.269 | APC-v1.0 | run | 38 | 0.161902 | 0.229783 | 0.111866 |
| EC | EC012 | ec012ec.269 | APC-v1.0 | rest | 45 | 1.24706 | 0.614787 | 0.352588 |
| EC | EC012 | ec012ec.269 | GLM | run | 38 | 2.54466 | 5 | 2.5 |
| EC | EC012 | ec012ec.269 | GLM | rest | 48 | 2.00962 | 3 | 1.5 |
| EC | EC012 | ec012ec.269 | KLMI | run | 38 | 2.29493 | 3 | 0.75 |
| EC | EC012 | ec012ec.269 | KLMI | rest | 48 | 1.44706 | 1.625 | 0 |
| EC | EC012 | ec012ec.269 | MVL-Ozkurt | run | 38 | 2.49437 | 3 | 1.5 |
| EC | EC012 | ec012ec.269 | MVL-Ozkurt | rest | 48 | 1.38664 | 2 | 0.5 |
| EC | EC012 | ec012ec.269 | MVL-raw | run | 38 | 2.87284 | 4.75 | 2 |
| EC | EC012 | ec012ec.269 | MVL-raw | rest | 48 | 2.26029 | 4 | 1 |
| EC | EC012 | ec012ec.270 | APC-v1.0 | run | 24 | 0.18826 | 0.212789 | 0.109755 |
| EC | EC012 | ec012ec.270 | APC-v1.0 | rest | 40 | 1.03416 | 0.659643 | 0.372816 |
| EC | EC012 | ec012ec.270 | GLM | run | 24 | 2.43018 | 2.625 | 1 |
| EC | EC012 | ec012ec.270 | GLM | rest | 49 | 2.39494 | 4.5 | 2 |
| EC | EC012 | ec012ec.270 | KLMI | run | 24 | 1.82661 | 1 | 0.5 |
| EC | EC012 | ec012ec.270 | KLMI | rest | 49 | 1.04927 | 1 | 0.5 |
| EC | EC012 | ec012ec.270 | MVL-Ozkurt | run | 24 | 1.9407 | 2.125 | 0.25 |
| EC | EC012 | ec012ec.270 | MVL-Ozkurt | rest | 49 | 1.65446 | 1.5 | 0.5 |
| EC | EC012 | ec012ec.270 | MVL-raw | run | 24 | 2.17654 | 2.625 | 0.5 |
| EC | EC012 | ec012ec.270 | MVL-raw | rest | 49 | 2.01298 | 1 | 0.5 |
| EC | EC012 | ec012ec.271 | APC-v1.0 | run | 35 | 0.277671 | 0.370779 | 0.206666 |
| EC | EC012 | ec012ec.271 | APC-v1.0 | rest | 16 | 1.62221 | 1.28378 | 0.537242 |
| EC | EC012 | ec012ec.271 | GLM | run | 35 | 2.75406 | 5.25 | 2.5 |
| EC | EC012 | ec012ec.271 | GLM | rest | 21 | 2.1674 | 1 | 0.5 |
| EC | EC012 | ec012ec.271 | KLMI | run | 35 | 1.61765 | 1.25 | 0.5 |
| EC | EC012 | ec012ec.271 | KLMI | rest | 21 | 1.31792 | 0.5 | 0 |
| EC | EC012 | ec012ec.271 | MVL-Ozkurt | run | 35 | 2.32885 | 2 | 0.5 |
| EC | EC012 | ec012ec.271 | MVL-Ozkurt | rest | 21 | 1.68431 | 1 | 0.5 |
| EC | EC012 | ec012ec.271 | MVL-raw | run | 35 | 2.67002 | 4 | 1 |
| EC | EC012 | ec012ec.271 | MVL-raw | rest | 21 | 2.04707 | 2 | 1 |
| EC | EC012 | ec012ec.356 | APC-v1.0 | run | 40 | 0.187182 | 0.263885 | 0.126542 |
| EC | EC012 | ec012ec.356 | APC-v1.0 | rest | 46 | 1.03343 | 0.71874 | 0.418631 |
| EC | EC012 | ec012ec.356 | GLM | run | 40 | 2.12128 | 2.625 | 1.5 |
| EC | EC012 | ec012ec.356 | GLM | rest | 50 | 2.1117 | 3.5 | 2 |
| EC | EC012 | ec012ec.356 | KLMI | run | 40 | 2.36752 | 4.125 | 1.5 |
| EC | EC012 | ec012ec.356 | KLMI | rest | 50 | 1.89319 | 3.375 | 1 |
| EC | EC012 | ec012ec.356 | MVL-Ozkurt | run | 40 | 2.23747 | 3.625 | 1 |
| EC | EC012 | ec012ec.356 | MVL-Ozkurt | rest | 50 | 2.18763 | 3.5 | 1 |
| EC | EC012 | ec012ec.356 | MVL-raw | run | 40 | 2.1189 | 3.125 | 1 |
| EC | EC012 | ec012ec.356 | MVL-raw | rest | 50 | 1.97869 | 3.25 | 1.25 |
| EC | EC012 | ec012ec.357 | APC-v1.0 | run | 38 | 0.296581 | 0.285443 | 0.143142 |
| EC | EC012 | ec012ec.357 | APC-v1.0 | rest | 34 | 1.00252 | 1.07221 | 0.613747 |
| EC | EC012 | ec012ec.357 | GLM | run | 38 | 2.40687 | 3.25 | 1.5 |
| EC | EC012 | ec012ec.357 | GLM | rest | 36 | 2.38447 | 3.125 | 1.5 |
| EC | EC012 | ec012ec.357 | KLMI | run | 38 | 1.4345 | 1 | 0.5 |
| EC | EC012 | ec012ec.357 | KLMI | rest | 36 | 1.26577 | 2 | 0.5 |
| EC | EC012 | ec012ec.357 | MVL-Ozkurt | run | 38 | 1.59352 | 1.5 | 0.5 |
| EC | EC012 | ec012ec.357 | MVL-Ozkurt | rest | 36 | 1.96573 | 3 | 1 |
| EC | EC012 | ec012ec.357 | MVL-raw | run | 38 | 1.41604 | 1.5 | 0.5 |
| EC | EC012 | ec012ec.357 | MVL-raw | rest | 36 | 1.9548 | 2.625 | 1 |
| EC | EC012 | ec012ec.375 | APC-v1.0 | run | 37 | 0.228193 | 0.321563 | 0.196184 |
| EC | EC012 | ec012ec.375 | APC-v1.0 | rest | 31 | 0.654173 | 0.654104 | 0.363506 |
| EC | EC012 | ec012ec.375 | GLM | run | 37 | 1.88173 | 3 | 1.5 |
| EC | EC012 | ec012ec.375 | GLM | rest | 32 | 2.22432 | 3.125 | 1.75 |
| EC | EC012 | ec012ec.375 | KLMI | run | 37 | 2.45087 | 4.5 | 1.5 |
| EC | EC012 | ec012ec.375 | KLMI | rest | 32 | 1.87829 | 2.125 | 0.5 |
| EC | EC012 | ec012ec.375 | MVL-Ozkurt | run | 37 | 2.41064 | 4 | 1 |
| EC | EC012 | ec012ec.375 | MVL-Ozkurt | rest | 32 | 1.69796 | 2 | 1 |
| EC | EC012 | ec012ec.375 | MVL-raw | run | 37 | 2.3867 | 4.5 | 1 |
| EC | EC012 | ec012ec.375 | MVL-raw | rest | 32 | 2.06741 | 3.125 | 1.25 |
| EC | EC012 | ec012ec.444 | APC-v1.0 | run | 30 | 0.164209 | 0.213825 | 0.108782 |
| EC | EC012 | ec012ec.444 | APC-v1.0 | rest | 40 | 1.02139 | 0.827481 | 0.356368 |
| EC | EC012 | ec012ec.444 | GLM | run | 30 | 2.09878 | 3.5 | 1.75 |
| EC | EC012 | ec012ec.444 | GLM | rest | 46 | 1.95208 | 2.5 | 1.25 |
| EC | EC012 | ec012ec.444 | KLMI | run | 30 | 1.98587 | 3.375 | 1 |
| EC | EC012 | ec012ec.444 | KLMI | rest | 46 | 1.37915 | 1.875 | 0.5 |
| EC | EC012 | ec012ec.444 | MVL-Ozkurt | run | 30 | 2.37419 | 3 | 0.5 |
| EC | EC012 | ec012ec.444 | MVL-Ozkurt | rest | 46 | 1.92705 | 3 | 1 |
| EC | EC012 | ec012ec.444 | MVL-raw | run | 30 | 2.40306 | 3.75 | 0.5 |
| EC | EC012 | ec012ec.444 | MVL-raw | rest | 46 | 2.37928 | 3.375 | 1.75 |
| EC | EC013 | ec013.156 | APC-v1.0 | run | 56 | 0.240555 | 0.267825 | 0.138579 |
| EC | EC013 | ec013.156 | APC-v1.0 | rest | 55 | 0.776308 | 0.434439 | 0.214421 |
| EC | EC013 | ec013.156 | GLM | run | 56 | 1.3594 | 2 | 0.75 |
| EC | EC013 | ec013.156 | GLM | rest | 56 | 1.51183 | 2 | 1 |
| EC | EC013 | ec013.156 | KLMI | run | 56 | 1.73746 | 3.125 | 1.5 |
| EC | EC013 | ec013.156 | KLMI | rest | 56 | 1.45261 | 2 | 1 |
| EC | EC013 | ec013.156 | MVL-Ozkurt | run | 56 | 1.87445 | 4 | 1.5 |
| EC | EC013 | ec013.156 | MVL-Ozkurt | rest | 56 | 1.54034 | 2.5 | 1.25 |
| EC | EC013 | ec013.156 | MVL-raw | run | 56 | 1.98795 | 3 | 1.5 |
| EC | EC013 | ec013.156 | MVL-raw | rest | 56 | 1.6067 | 2.5 | 1.5 |
| EC | EC013 | ec013.157 | APC-v1.0 | run | 23 | 0.296835 | 0.303688 | 0.171079 |
| EC | EC013 | ec013.157 | APC-v1.0 | rest | 33 | 0.980738 | 0.513519 | 0.244995 |
| EC | EC013 | ec013.157 | GLM | run | 23 | 1.62521 | 2.5 | 1.5 |
| EC | EC013 | ec013.157 | GLM | rest | 33 | 1.37775 | 2 | 1 |
| EC | EC013 | ec013.157 | KLMI | run | 23 | 1.55943 | 2.5 | 1.5 |
| EC | EC013 | ec013.157 | KLMI | rest | 33 | 1.24335 | 2.5 | 1 |
| EC | EC013 | ec013.157 | MVL-Ozkurt | run | 23 | 1.86924 | 3.25 | 1 |
| EC | EC013 | ec013.157 | MVL-Ozkurt | rest | 33 | 1.18884 | 2 | 0.5 |
| EC | EC013 | ec013.157 | MVL-raw | run | 23 | 1.76006 | 2.25 | 1 |
| EC | EC013 | ec013.157 | MVL-raw | rest | 33 | 1.75338 | 2.5 | 1 |
| EC | EC013 | ec013.205 | APC-v1.0 | run | 8 | 0.211419 | 0.287048 | 0.154945 |
| EC | EC013 | ec013.205 | APC-v1.0 | rest | 9 | 0.373725 | 0.272311 | 0.188032 |
| EC | EC013 | ec013.205 | GLM | run | 8 | 0.92582 | 0.75 | 0.5 |
| EC | EC013 | ec013.205 | GLM | rest | 9 | 1.49536 | 2 | 1.5 |
| EC | EC013 | ec013.205 | KLMI | run | 8 | 0.883883 | 0.625 | 0.25 |
| EC | EC013 | ec013.205 | KLMI | rest | 9 | 1.47432 | 2 | 1.5 |
| EC | EC013 | ec013.205 | MVL-Ozkurt | run | 8 | 1.84076 | 2.5 | 1.25 |
| EC | EC013 | ec013.205 | MVL-Ozkurt | rest | 9 | 1.6604 | 2.5 | 0.5 |
| EC | EC013 | ec013.205 | MVL-raw | run | 8 | 1.84076 | 2.5 | 1.25 |
| EC | EC013 | ec013.205 | MVL-raw | rest | 9 | 1.54335 | 2.5 | 0.5 |
| EC | EC013 | ec013.206 | APC-v1.0 | run | 58 | 0.167175 | 0.200953 | 0.105072 |
| EC | EC013 | ec013.206 | APC-v1.0 | rest | 61 | 0.535719 | 0.484704 | 0.239467 |
| EC | EC013 | ec013.206 | GLM | run | 58 | 1.00892 | 1.5 | 1 |
| EC | EC013 | ec013.206 | GLM | rest | 61 | 1.34113 | 2 | 1 |
| EC | EC013 | ec013.206 | KLMI | run | 58 | 1.32133 | 1.875 | 1 |
| EC | EC013 | ec013.206 | KLMI | rest | 61 | 1.46316 | 2.5 | 1 |
| EC | EC013 | ec013.206 | MVL-Ozkurt | run | 58 | 1.76331 | 3 | 1.5 |
| EC | EC013 | ec013.206 | MVL-Ozkurt | rest | 61 | 1.40884 | 2 | 1 |
| EC | EC013 | ec013.206 | MVL-raw | run | 58 | 1.77705 | 3.375 | 1.5 |
| EC | EC013 | ec013.206 | MVL-raw | rest | 61 | 1.65823 | 2 | 1 |
| EC | EC013 | ec013.208 | APC-v1.0 | run | 44 | 0.310876 | 0.379814 | 0.164003 |
| EC | EC013 | ec013.208 | APC-v1.0 | rest | 52 | 0.746639 | 0.645586 | 0.301425 |
| EC | EC013 | ec013.208 | GLM | run | 44 | 0.942521 | 1.5 | 0.75 |
| EC | EC013 | ec013.208 | GLM | rest | 53 | 1.59132 | 2 | 1 |
| EC | EC013 | ec013.208 | KLMI | run | 44 | 1.32925 | 1.625 | 0.5 |
| EC | EC013 | ec013.208 | KLMI | rest | 53 | 1.60449 | 3 | 1 |
| EC | EC013 | ec013.208 | MVL-Ozkurt | run | 44 | 1.87111 | 4.125 | 2 |
| EC | EC013 | ec013.208 | MVL-Ozkurt | rest | 53 | 1.81506 | 3 | 1 |
| EC | EC013 | ec013.208 | MVL-raw | run | 44 | 1.67496 | 3 | 1.25 |
| EC | EC013 | ec013.208 | MVL-raw | rest | 53 | 1.84397 | 3 | 1.5 |
| EC | EC013 | ec013.251 | APC-v1.0 | run | 54 | 0.276112 | 0.31558 | 0.160738 |
| EC | EC013 | ec013.251 | APC-v1.0 | rest | 59 | 0.732483 | 0.991607 | 0.485456 |
| EC | EC013 | ec013.251 | GLM | run | 54 | 1.2001 | 1.375 | 0.5 |
| EC | EC013 | ec013.251 | GLM | rest | 65 | 1.36636 | 2.5 | 1 |
| EC | EC013 | ec013.251 | KLMI | run | 54 | 1.71584 | 2.75 | 1.25 |
| EC | EC013 | ec013.251 | KLMI | rest | 65 | 1.43622 | 2.5 | 1.5 |
| EC | EC013 | ec013.251 | MVL-Ozkurt | run | 54 | 2.00489 | 3.875 | 2 |
| EC | EC013 | ec013.251 | MVL-Ozkurt | rest | 65 | 1.64624 | 2.5 | 1 |
| EC | EC013 | ec013.251 | MVL-raw | run | 54 | 1.9441 | 3.5 | 1.5 |
| EC | EC013 | ec013.251 | MVL-raw | rest | 65 | 1.5739 | 2.5 | 1 |
| EC | EC013 | ec013.252 | APC-v1.0 | run | 32 | 0.333486 | 0.28284 | 0.149288 |
| EC | EC013 | ec013.252 | APC-v1.0 | rest | 59 | 0.726475 | 0.830931 | 0.425203 |
| EC | EC013 | ec013.252 | GLM | run | 32 | 1.0039 | 2 | 0.75 |
| EC | EC013 | ec013.252 | GLM | rest | 64 | 1.58333 | 1.5 | 1 |
| EC | EC013 | ec013.252 | KLMI | run | 32 | 1.70359 | 2.125 | 1.25 |
| EC | EC013 | ec013.252 | KLMI | rest | 64 | 1.53845 | 3 | 1 |
| EC | EC013 | ec013.252 | MVL-Ozkurt | run | 32 | 1.97157 | 3.625 | 1.75 |
| EC | EC013 | ec013.252 | MVL-Ozkurt | rest | 64 | 1.45635 | 2 | 1 |
| EC | EC013 | ec013.252 | MVL-raw | run | 32 | 1.94111 | 4 | 2 |
| EC | EC013 | ec013.252 | MVL-raw | rest | 64 | 1.72682 | 3.5 | 1 |
| EC | EC013 | ec013.374 | APC-v1.0 | run | 88 | 0.295716 | 0.313251 | 0.175542 |
| EC | EC013 | ec013.374 | APC-v1.0 | rest | 75 | 0.771973 | 0.989422 | 0.480074 |
| EC | EC013 | ec013.374 | GLM | run | 88 | 1.1522 | 2 | 1 |
| EC | EC013 | ec013.374 | GLM | rest | 77 | 1.64416 | 2.5 | 1 |
| EC | EC013 | ec013.374 | KLMI | run | 88 | 1.43821 | 2 | 1 |
| EC | EC013 | ec013.374 | KLMI | rest | 77 | 1.37277 | 2.5 | 1 |
| EC | EC013 | ec013.374 | MVL-Ozkurt | run | 88 | 1.82487 | 3.5 | 1.5 |
| EC | EC013 | ec013.374 | MVL-Ozkurt | rest | 77 | 1.51398 | 2.5 | 1 |
| EC | EC013 | ec013.374 | MVL-raw | run | 88 | 1.65034 | 3 | 1.25 |
| EC | EC013 | ec013.374 | MVL-raw | rest | 77 | 1.7034 | 2.5 | 1 |
| EC | EC013 | ec013.375 | APC-v1.0 | run | 68 | 0.350069 | 0.441281 | 0.217914 |
| EC | EC013 | ec013.375 | APC-v1.0 | rest | 130 | 1.39834 | 1.15061 | 0.565936 |
| EC | EC013 | ec013.375 | GLM | run | 68 | 1.06896 | 1.5 | 1 |
| EC | EC013 | ec013.375 | GLM | rest | 137 | 1.71072 | 2.5 | 1.5 |
| EC | EC013 | ec013.375 | KLMI | run | 68 | 1.5335 | 2 | 1 |
| EC | EC013 | ec013.375 | KLMI | rest | 137 | 1.42702 | 2.5 | 1 |
| EC | EC013 | ec013.375 | MVL-Ozkurt | run | 68 | 1.69028 | 3.125 | 1.5 |
| EC | EC013 | ec013.375 | MVL-Ozkurt | rest | 137 | 1.667 | 2.5 | 1 |
| EC | EC013 | ec013.375 | MVL-raw | run | 68 | 1.8086 | 3.125 | 1.5 |
| EC | EC013 | ec013.375 | MVL-raw | rest | 137 | 1.67625 | 2.5 | 1 |

POST HOC paired APC-minus-scan session spread differences: [posthoc_2s_within_state_spread_comparisons.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_within_state_spread_comparisons.csv>). POST HOC across-session spread tests: [posthoc_2s_across_session_spread_comparisons.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_across_session_spread_comparisons.csv>).

## POST HOC descriptive historical overlap

POST HOC descriptive comparison only, with the same original ec013.157 12/12 >=5-s historical reference and [32.6392,298.0)-s window. No overlap gate. POST HOC overlap table:
| state | historical_bouts | new_bouts_whole_recording | new_bouts_intersecting_original_interval | historical_bouts_with_any_same_state_overlap | same_state_intersection_s | jaccard |
| --- | --- | --- | --- | --- | --- | --- |
| run | 12 | 23 | 13 | 12 | 55.2192 | 0.445038 |
| rest | 12 | 33 | 14 | 12 | 72.576 | 0.484654 |

POST HOC per-historical-bout and cross-state overlaps: [posthoc_2s_historical_overlap_bouts.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_historical_overlap_bouts.csv>); [posthoc_2s_historical_overlap_cross_state.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_historical_overlap_cross_state.csv>).

## POST HOC figures

Every POST HOC figure is separately exported as 300-dpi PNG and SVG, visibly labelled POST HOC and embedding commit/settings/source-CSV hashes. The displayed comparison scan remains the prespecified Ozkurt-max scan; every scan is retained in the POST HOC tables.

- POST HOC: 5-s and POST HOC 2-s bout counts; inclusion remains >=5 run and >=5 rest bouts: [POST HOC PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_inclusion_comparison.png>); [POST HOC SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_inclusion_comparison.svg>).
- POST HOC: Pooled APC effects beside prespecified 5-s results; different eligible-session sets: [POST HOC PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_across_session_comparison.png>); [POST HOC SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_across_session_comparison.svg>).
- POST HOC: Per-bout CA1 EC013 fP_hz with means and 10,000-resample bootstrap 95% CIs: [POST HOC PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_CA1_EC013_fP_hz_run_rest.png>); [POST HOC SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_CA1_EC013_fP_hz_run_rest.svg>).
- POST HOC: Per-bout CA1 EC013 ozkurt_mvl with means and 10,000-resample bootstrap 95% CIs: [POST HOC PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_CA1_EC013_ozkurt_mvl_run_rest.png>); [POST HOC SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_CA1_EC013_ozkurt_mvl_run_rest.svg>).
- POST HOC: Session mean differences with percentile-bootstrap 95% CIs for CA1: [POST HOC PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_CA1_session_differences.png>); [POST HOC SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_CA1_session_differences.svg>).
- POST HOC: Per-bout EC EC012 fP_hz with means and 10,000-resample bootstrap 95% CIs: [POST HOC PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_EC_EC012_fP_hz_run_rest.png>); [POST HOC SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_EC_EC012_fP_hz_run_rest.svg>).
- POST HOC: Per-bout EC EC012 ozkurt_mvl with means and 10,000-resample bootstrap 95% CIs: [POST HOC PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_EC_EC012_ozkurt_mvl_run_rest.png>); [POST HOC SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_EC_EC012_ozkurt_mvl_run_rest.svg>).
- POST HOC: Per-bout EC EC013 fP_hz with means and 10,000-resample bootstrap 95% CIs: [POST HOC PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_EC_EC013_fP_hz_run_rest.png>); [POST HOC SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_EC_EC013_fP_hz_run_rest.svg>).
- POST HOC: Per-bout EC EC013 ozkurt_mvl with means and 10,000-resample bootstrap 95% CIs: [POST HOC PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_EC_EC013_ozkurt_mvl_run_rest.png>); [POST HOC SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_EC_EC013_ozkurt_mvl_run_rest.svg>).
- POST HOC: Session mean differences with percentile-bootstrap 95% CIs for EC: [POST HOC PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_EC_session_differences.png>); [POST HOC SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_EC_session_differences.svg>).
- POST HOC: Per-bout E1_sensitivity EC013 fP_hz with means and 10,000-resample bootstrap 95% CIs: [POST HOC PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_E1_sensitivity_EC013_fP_hz_run_rest.png>); [POST HOC SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_E1_sensitivity_EC013_fP_hz_run_rest.svg>).
- POST HOC: Per-bout E1_sensitivity EC013 ozkurt_mvl with means and 10,000-resample bootstrap 95% CIs: [POST HOC PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_E1_sensitivity_EC013_ozkurt_mvl_run_rest.png>); [POST HOC SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_E1_sensitivity_EC013_ozkurt_mvl_run_rest.svg>).
- POST HOC: Session mean differences with percentile-bootstrap 95% CIs for E1_sensitivity: [POST HOC PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_E1_sensitivity_session_differences.png>); [POST HOC SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_E1_sensitivity_session_differences.svg>).
- POST HOC: Within-session fP SD for all methods; points are sessions: [POST HOC PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_within_state_fp_spread.png>); [POST HOC SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_within_state_fp_spread.svg>).
- POST HOC: Unchanged tracking trace with POST HOC >=2-s qualifying bouts; blue run, orange rest: [POST HOC PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_tracking_ec013_157.png>); [POST HOC SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_tracking_ec013_157.svg>).

## POST HOC runtime and deviations

POST HOC behaviour extraction: 4.717 s. POST HOC method-worker seconds (parallel): 1519.606, 1417.578, 1544.340; sum 4481.524 s, longest worker 1544.340 s. POST HOC statistics: 14.094 s. POST HOC mixed models: 29.961 s. Startup, the approval-service interruption and report/figure packaging are excluded from stage compute timings.

POST HOC statistical warning records: 0; [posthoc_2s_statistics_warnings.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_statistics_warnings.csv>). Test outputs are retained with warning context; estimators and data were not adjusted.

- POST HOC resolved tooling service failure: The first escalated MATLAB launch was not executed because automatic approval review had reached its usage limit. After the user requested continuation, the same authorized launch passed automatic approval review. No approval check was bypassed and no method settings changed.
- POST HOC tooling MAT string decoding: The optional partial consistency-audit script could not decode MATLAB MCOS string metadata through scipy.io.loadmat. It now reads session/state/channel from checkpoint filenames, verifies numeric channel/bounds metadata, and uses the unchanged fixed metric order. No method result or computation changed; workers continued unaffected.
- POST HOC tooling process-monitor access: A read-only CIM process query was unavailable in the sandbox during mixed-model monitoring. Execution was monitored through the existing MATLAB session and log instead; no process or analysis setting was changed.
- POST HOC pre-existing MATLAB startup warnings: MATLAB startup reported missing historical Brainstorm directories. The frozen-method path assertions passed; no MATLAB installation or startup configuration was changed. Worker and mixed-model logs retain these warnings.
- POST HOC execution uses three independent session partitions with one MATLAB computational thread per worker; numerical code/settings are unchanged.
- POST HOC nonzero APC statuses and covariance/optimizer warnings are reported as method/statistical outputs using the same handling as the prespecified pipeline.
- POST HOC regional mapping assumptions and the ec013.157 equivalent source remain unchanged and documented in the prespecified report.

POST HOC verification: [posthoc_2s_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_verification.json>). POST HOC output manifest: [posthoc_2s_output_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_output_manifest.json>).
