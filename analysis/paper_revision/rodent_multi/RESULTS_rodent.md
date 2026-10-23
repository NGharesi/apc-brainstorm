# Regional rodent replication

**Status: completed under the dated revised behaviour/channel plan.** Three sessions meet the five-run/five-rest criterion in both CA1 and EC: ec013.156, ec013.157 and ec013.375. All are EC013. No EC012 session qualifies. E1 sensitivity uses the same three sessions and bouts.

Frozen APC `v1.0`, commit `71ebc16aed32ca38be73a800738b975e5806b330`. Tagged method code is unchanged. [Full settings and provenance](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_analysis_provenance.json>).

Primary APC summaries below use the three session-level run-minus-rest differences; CIs are t intervals across sessions. Pooled and EC013 summaries coincide. Per-bout mixed-model estimates are reported separately.

| analysis | outcome | n_sessions | mean_session_difference | ci_low | ci_high | one_sample_p | wilcoxon_p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | fA_hz | 3 | -0.354978 | -7.8002 | 7.09025 | 0.856443 | 1 |
| CA1 | fP_hz | 3 | 0.705852 | -2.03297 | 3.44467 | 0.382964 | 0.5 |
| CA1 | ozkurt_mvl | 3 | 0.0151827 | -0.00486253 | 0.035228 | 0.0826512 | 0.25 |
| EC | fA_hz | 3 | -1.81618 | -25.2157 | 21.5834 | 0.770179 | 0.75 |
| EC | fP_hz | 3 | 1.17684 | 0.814791 | 1.53889 | 0.0050736 | 0.25 |
| EC | ozkurt_mvl | 3 | 0.0279788 | 0.00621326 | 0.0497443 | 0.0311692 | 0.25 |

## Dated amendment and historical record

The 2026-10-22 amendment in [PROTOCOL_rodent.md](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/PROTOCOL_rodent.md>) supersedes the chunked historical-speed plan and its gate. It records the user-supplied rationale that historical x1-only trenddecomp speed, retaining -1 sentinels and raw units, changes about 12% of labels under a 2.5-s window shift. That shift claim was not independently rerun here. All regional outcomes use the revised tracking-rate method. The exact historical **12 run/12 rest** reproduction is retained solely as an original-analysis record and for the requested descriptive overlap: [behavior_reproduction.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/behavior_reproduction.json>). The superseded stopped report is [RESULTS_rodent_chunk_plan_stopped.md](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/RESULTS_rodent_chunk_plan_stopped.md>).

The amendment was recorded before regional mapping/behaviour/PAC: [regional_protocol_record.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_protocol_record.json>). Protocol SHA-256: `0c38139e23561665a8ca3998f61fe74b6946abf25c89f2ff06ba5e7679161e67`. Operational details, including Gaussian boundaries, quantiles and bout timestamps, were recorded in [EXECUTION_rodent.md](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/EXECUTION_rodent.md>).

## Channel-to-region map

The ec012ec.269 XML contains zero-based anatomical groups 0–7, 8–15, 16–23, 24–31 and singleton 32. Thus E1–E8 = shank 1, E9–E16 = shank 2, E17–E24 = shank 3, E25–E32 = shank 4. E33 is auxiliary. The prespecified extension to EC013 gives eight 8-channel shanks through E64, with E65 auxiliary. EC013 is explicitly labelled **“assumed contiguous, verified on ec012ec.269.”** The XML check passed: [regional_xml_grouping.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_xml_grouping.json>).

Region labels come from the exact top-directory rows in ElePosition.txt, joined through hc3-session.csv. All 18 session metadata rows specify `linear`. The per-channel map includes all 882 imported channel rows, region, shank, auxiliary exclusion, source ratio/flag and evidence: [regional_channel_map.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_channel_map.csv>). Source rows/hashes: [regional_session_metadata.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_session_metadata.csv>).

| animal | top_directory | shank_regions | mapping_evidence |
| --- | --- | --- | --- |
| EC013 | ec013.15 | EC3;EC4;EC5;EC5;CA1;CA1;CA1;CA1 | assumed contiguous, verified on ec012ec.269 |
| EC013 | ec013.18 | EC3;EC4;EC5;EC5;CA1;CA1;CA1;CA1 | assumed contiguous, verified on ec012ec.269 |
| EC013 | ec013.21 | EC3;EC4;EC5;EC5;CA1;CA1;CA1;CA1 | assumed contiguous, verified on ec012ec.269 |
| EC013 | ec013.27 | EC3;EC4;EC5;EC5;CA1;CA1;CA1;CA1 | assumed contiguous, verified on ec012ec.269 |
| EC012 | ec012ec.13 | EC3;EC3;EC5;EC5 | contiguous mapping applied from ec012ec.269 as prespecified |
| EC012 | ec012ec.14 | EC3;EC3;EC5;EC5 | verified in session XML |
| EC012 | ec012ec.14 | EC3;EC3;EC5;EC5 | contiguous mapping applied from ec012ec.269 as prespecified |
| EC012 | ec012ec.17 | EC3;EC3;EC5;EC5 | contiguous mapping applied from ec012ec.269 as prespecified |
| EC012 | ec012ec.18 | EC3;EC3;EC5;EC5 | contiguous mapping applied from ec012ec.269 as prespecified |
| EC012 | ec012ec.21 | EC3;EC3;EC5;EC5 | contiguous mapping applied from ec012ec.269 as prespecified |

EC013 shanks 1/2/3–4/5–8 are EC3/EC4/EC5/CA1, respectively; EC012 shanks 1–2/3–4 are EC3/EC5. E1 sensitivity is EC3 in every EC013 session. These are metadata region labels; no additional anatomical inference was applied.

## Regional channel selection

Existing whole-recording theta(6–10)/delta(1–4) Welch ratios were reused. Select the first finite maximum within the requested CA1 or EC mask; exclude auxiliary E33/E65. Selection is separate from behaviour eligibility and PAC outcomes. Source channel flags are reported alongside the regional choices. [regional_selected_channels.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_selected_channels.csv>).

| animal | session | analysis | channel_name | shank | region | theta_delta_ratio | source_channel_flag | included |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EC013 | ec013.156 | EC | E8 | 1 | EC3 | 5.88298 | 1 | True |
| EC013 | ec013.156 | CA1 | E38 | 5 | CA1 | 4.55845 | -1 | True |
| EC013 | ec013.156 | E1_sensitivity | E1 | 1 | EC3 | 5.13478 | 1 | True |
| EC013 | ec013.157 | EC | E8 | 1 | EC3 | 5.73648 | 1 | True |
| EC013 | ec013.157 | CA1 | E40 | 5 | CA1 | 4.2026 | -1 | True |
| EC013 | ec013.157 | E1_sensitivity | E1 | 1 | EC3 | 4.98602 | 1 | True |
| EC013 | ec013.205 | EC | E2 | 1 | EC3 | 9.89115 | 1 | False |
| EC013 | ec013.205 | CA1 | E38 | 5 | CA1 | 7.86491 | -1 | False |
| EC013 | ec013.205 | E1_sensitivity | E1 | 1 | EC3 | 7.72998 | 1 | False |
| EC013 | ec013.206 | EC | E2 | 1 | EC3 | 5.25741 | 1 | False |
| EC013 | ec013.206 | CA1 | E40 | 5 | CA1 | 3.93556 | -1 | False |
| EC013 | ec013.206 | E1_sensitivity | E1 | 1 | EC3 | 4.76935 | 1 | False |
| EC013 | ec013.208 | EC | E2 | 1 | EC3 | 1.00401 | 1 | False |
| EC013 | ec013.208 | CA1 | E62 | 8 | CA1 | 1.12058 | -1 | False |
| EC013 | ec013.208 | E1_sensitivity | E1 | 1 | EC3 | 0.960782 | 1 | False |
| EC013 | ec013.251 | EC | E2 | 1 | EC3 | 2.83277 | 1 | False |
| EC013 | ec013.251 | CA1 | E38 | 5 | CA1 | 2.40877 | -1 | False |
| EC013 | ec013.251 | E1_sensitivity | E1 | 1 | EC3 | 2.73322 | 1 | False |
| EC013 | ec013.252 | EC | E2 | 1 | EC3 | 2.90608 | 1 | False |
| EC013 | ec013.252 | CA1 | E38 | 5 | CA1 | 2.54325 | -1 | False |
| EC013 | ec013.252 | E1_sensitivity | E1 | 1 | EC3 | 2.79305 | 1 | False |
| EC013 | ec013.374 | EC | E8 | 1 | EC3 | 3.24252 | 1 | False |
| EC013 | ec013.374 | CA1 | E38 | 5 | CA1 | 2.57399 | -1 | False |
| EC013 | ec013.374 | E1_sensitivity | E1 | 1 | EC3 | 2.7809 | 1 | False |
| EC013 | ec013.375 | EC | E8 | 1 | EC3 | 1.38052 | 1 | True |
| EC013 | ec013.375 | CA1 | E62 | 8 | CA1 | 1.14409 | -1 | True |
| EC013 | ec013.375 | E1_sensitivity | E1 | 1 | EC3 | 1.20008 | 1 | True |
| EC012 | ec012ec.239 | EC | E5 | 1 | EC3 | 7.17818 | 1 | False |
| EC012 | ec012ec.240 | EC | E3 | 1 | EC3 | 7.67862 | 1 | False |
| EC012 | ec012ec.269 | EC | E5 | 1 | EC3 | 4.80764 | 1 | False |
| EC012 | ec012ec.270 | EC | E12 | 2 | EC3 | 5.90819 | 1 | False |
| EC012 | ec012ec.271 | EC | E10 | 2 | EC3 | 7.16646 | 1 | False |
| EC012 | ec012ec.356 | EC | E6 | 1 | EC3 | 5.96633 | 1 | False |
| EC012 | ec012ec.357 | EC | E9 | 2 | EC3 | 7.37768 | 1 | False |
| EC012 | ec012ec.375 | EC | E6 | 1 | EC3 | 7.39874 | 1 | False |
| EC012 | ec012ec.444 | EC | E6 | 1 | EC3 | 7.55065 | 1 | False |

## Mapping and tracking-rate behaviour

All 18 tracking/LFP duration ratios pass the unchanged 5% mapping check. The ec013.157 missing requested path is supplied by the previously verified equivalent full recording; all timestamps and the saved multichannel crop matched exactly. [mapping_checks.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/mapping_checks.csv>); [ec013_157_source_recovery.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/ec013_157_source_recovery.json>).

| animal | session | tracking_array | lfp_duration_s | tracking_to_lfp_duration_ratio |
| --- | --- | --- | --- | --- |
| EC013 | ec013.156 | ec013ec1 | 1023.59 | 1.00003 |
| EC013 | ec013.157 | ec013ec2 | 631.2 | 1.00003 |
| EC013 | ec013.205 | ec013ec3 | 187.597 | 1.00014 |
| EC013 | ec013.206 | ec013ec4 | 874.4 | 1.00002 |
| EC013 | ec013.208 | ec013ec5 | 778.24 | 1.00003 |
| EC013 | ec013.251 | ec013ec6 | 967.6 | 1 |
| EC013 | ec013.252 | ec013ec7 | 962.97 | 1.00003 |
| EC013 | ec013.374 | ec013ec8 | 1076.43 | 1.00002 |
| EC013 | ec013.375 | ec013ec9 | 1757.18 | 1.00001 |
| EC012 | ec012ec.239 | ec012ec1 | 471.7 | 1.00001 |
| EC012 | ec012ec.240 | ec012ec2 | 637.5 | 1.00003 |
| EC012 | ec012ec.269 | ec012ec3 | 507.4 | 1.00003 |
| EC012 | ec012ec.270 | ec012ec4 | 420 | 1.00005 |
| EC012 | ec012ec.271 | ec012ec5 | 403.2 | 1.00006 |
| EC012 | ec012ec.356 | ec012ec6 | 467.1 | 1.00005 |
| EC012 | ec012ec.357 | ec012ec7 | 565.3 | 1.00004 |
| EC012 | ec012ec.375 | ec012ec8 | 631.2 | 1.00003 |
| EC012 | ec012ec.444 | ec012ec9 | 418.7 | 1.00003 |

At 39.0625 Hz, combine valid LED positions, interpolate bounded missing gaps <=0.5 s, fit PC1 to valid positions, and use 250 cm divided by the 99.5th–0.5th percentile span. State position uses the unsmoothed projection. End zones include the extreme percentile tails. Smooth x/y within each finite segment with a normalized Gaussian (SD 0.2 s, radius 32 samples, reflected boundaries), then central-difference 2-D speed in cm/s. Long gaps remain unclassified and split bouts. RUN requires >6 cm/s in the central 70%; REST requires <6 cm/s in either outer 15%; exactly 6 is unclassified. Keep contiguous >=5-s bouts after excluding first/last 2 s. Half-open tracking bout times map to actual 1250-Hz LFP timestamps.

Raw missing fraction means neither LED is valid; after interpolation means positions still missing. Complete per-bout durations and both tracking/LFP indices: [regional_bouts.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_bouts.csv>). Whole-session traces and masks are in the 18 `*_regional_tracking.npz` files.

| animal | session | cm_per_unit | raw_missing_fraction | missing_after_short_interpolation_fraction | short_gap_samples_interpolated | run_bouts | rest_bouts | included |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EC013 | ec013.156 | 0.892045 | 0.018557 | 0.018557 | 0 | 9 | 43 | True |
| EC013 | ec013.157 | 0.900057 | 0.0314312 | 0.0314312 | 0 | 6 | 15 | True |
| EC013 | ec013.205 | 0.902 | 0.142311 | 0.142311 | 0 | 0 | 4 | False |
| EC013 | ec013.206 | 0.909338 | 0.0132916 | 0.0132916 | 0 | 3 | 21 | False |
| EC013 | ec013.208 | 0.927246 | 0.013618 | 0.013618 | 0 | 0 | 10 | False |
| EC013 | ec013.251 | 0.889563 | 0.0421991 | 0.0421991 | 0 | 0 | 12 | False |
| EC013 | ec013.252 | 0.905386 | 0.014435 | 0.014435 | 0 | 1 | 9 | False |
| EC013 | ec013.374 | 0.892117 | 0.016124 | 0.016124 | 0 | 4 | 8 | False |
| EC013 | ec013.375 | 0.894901 | 0.00820209 | 0.00820209 | 0 | 5 | 34 | True |
| EC012 | ec012ec.239 | 0.924512 | 0.059047 | 0.059047 | 0 | 0 | 0 | False |
| EC012 | ec012ec.240 | 0.943127 | 0.0526443 | 0.0526443 | 0 | 0 | 1 | False |
| EC012 | ec012ec.269 | 0.934115 | 0.0945966 | 0.0945966 | 0 | 0 | 1 | False |
| EC012 | ec012ec.270 | 0.946639 | 0.07381 | 0.07381 | 0 | 0 | 1 | False |
| EC012 | ec012ec.271 | 0.918263 | 0.0826614 | 0.0826614 | 0 | 0 | 2 | False |
| EC012 | ec012ec.356 | 0.923684 | 0.0648874 | 0.0648874 | 0 | 0 | 5 | False |
| EC012 | ec012ec.357 | 0.899661 | 0.0582348 | 0.0582348 | 0 | 0 | 1 | False |
| EC012 | ec012ec.375 | 0.923188 | 0.0577118 | 0.0577118 | 0 | 0 | 6 | False |
| EC012 | ec012ec.444 | 0.919307 | 0.0432869 | 0.0432869 | 0 | 0 | 1 | False |

| session | run_total_duration_s | run_mean_duration_s | run_median_duration_s | run_min_duration_s | run_max_duration_s | rest_total_duration_s | rest_mean_duration_s | rest_median_duration_s | rest_min_duration_s | rest_max_duration_s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ec013.156 | 51.0208 | 5.66898 | 5.632 | 5.0432 | 6.5536 | 319.258 | 7.4246 | 7.4752 | 5.0688 | 11.1616 |
| ec013.157 | 31.8464 | 5.30773 | 5.3376 | 5.0944 | 5.4784 | 126.157 | 8.41045 | 8.4224 | 5.1712 | 12.8 |
| ec013.205 | 0 | NA | NA | NA | NA | 28.1856 | 7.0464 | 7.2064 | 5.2736 | 8.4992 |
| ec013.206 | 16.384 | 5.46133 | 5.1456 | 5.0944 | 6.144 | 123.674 | 5.88922 | 5.8368 | 5.0432 | 7.7824 |
| ec013.208 | 0 | NA | NA | NA | NA | 54.1952 | 5.41952 | 5.3504 | 5.0432 | 6.144 |
| ec013.251 | 0 | NA | NA | NA | NA | 68.992 | 5.74933 | 5.6448 | 5.0432 | 7.1936 |
| ec013.252 | 6.3488 | 6.3488 | 6.3488 | 6.3488 | 6.3488 | 71.1936 | 7.9104 | 7.0656 | 5.2992 | 13.3888 |
| ec013.374 | 23.2192 | 5.8048 | 5.568 | 5.3504 | 6.7328 | 66.0736 | 8.2592 | 5.7728 | 5.0176 | 18.176 |
| ec013.375 | 28.3904 | 5.67808 | 5.5296 | 5.1712 | 6.1952 | 290.202 | 8.53534 | 7.2064 | 5.0944 | 17.9456 |
| ec012ec.239 | 0 | NA | NA | NA | NA | 0 | NA | NA | NA | NA |
| ec012ec.240 | 0 | NA | NA | NA | NA | 5.2736 | 5.2736 | 5.2736 | 5.2736 | 5.2736 |
| ec012ec.269 | 0 | NA | NA | NA | NA | 6.144 | 6.144 | 6.144 | 6.144 | 6.144 |
| ec012ec.270 | 0 | NA | NA | NA | NA | 5.7344 | 5.7344 | 5.7344 | 5.7344 | 5.7344 |
| ec012ec.271 | 0 | NA | NA | NA | NA | 19.3792 | 9.6896 | 9.6896 | 5.248 | 14.1312 |
| ec012ec.356 | 0 | NA | NA | NA | NA | 30.3872 | 6.07744 | 5.76 | 5.0176 | 7.7056 |
| ec012ec.357 | 0 | NA | NA | NA | NA | 6.016 | 6.016 | 6.016 | 6.016 | 6.016 |
| ec012ec.375 | 0 | NA | NA | NA | NA | 45.2608 | 7.54347 | 7.5008 | 5.632 | 9.0624 |
| ec012ec.444 | 0 | NA | NA | NA | NA | 5.5296 | 5.5296 | 5.5296 | 5.5296 | 5.5296 |

Before the 5-s criterion, all EC012 run candidate intervals are shorter than 5 s. Candidate counts, maximum durations and speed quantiles are in [regional_behavior_qc.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_behavior_qc.csv>). Eligibility is identical across regional channels because each session uses one behaviour trace. Included: ec013.156 (9 run/43 rest), ec013.157 (6/15), ec013.375 (5/34). The other 15 sessions fail the >=5/5 criterion; [regional_session_eligibility.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_session_eligibility.csv>) provides every regional inclusion/exclusion row.

## Descriptive overlap with original ec013.157 bouts

No overlap gate was applied. Comparisons below clip the new bout sets to the original interval [32.6392,298.0) s. Jaccard is same-state intersection divided by union; whole-recording new bouts outside that interval are not added to the denominator.

| state | historical_bouts | new_bouts_whole_recording | new_bouts_intersecting_original_interval | historical_bouts_with_any_same_state_overlap | historical_duration_s | new_duration_in_original_interval_s | same_state_intersection_s | jaccard |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run | 12 | 6 | 3 | 3 | 124.078 | 16.0256 | 16.0256 | 0.129158 |
| rest | 12 | 15 | 8 | 8 | 133.466 | 70.5024 | 62.3544 | 0.440314 |

| state | historical_bout | historical_start_s | historical_stop_exclusive_s | new_same_state_overlap_s | fraction_historical_bout_covered | new_bouts_overlapping |
| --- | --- | --- | --- | --- | --- | --- |
| run | 1 | 44.1136 | 57.3544 | 0 | 0 | 0 |
| run | 2 | 72.944 | 84.184 | 0 | 0 | 0 |
| run | 3 | 92.1656 | 102.75 | 0 | 0 | 0 |
| run | 4 | 113.55 | 123.501 | 0 | 0 | 0 |
| run | 5 | 136.72 | 147.406 | 5.1456 | 0.481509 | 1 |
| run | 6 | 157.52 | 168.273 | 0 | 0 | 0 |
| run | 7 | 174.398 | 183.76 | 0 | 0 | 0 |
| run | 8 | 200.252 | 209.55 | 5.4528 | 0.586474 | 1 |
| run | 9 | 218.855 | 228.297 | 0 | 0 | 0 |
| run | 10 | 245.479 | 253.654 | 0 | 0 | 0 |
| run | 11 | 260.736 | 271.122 | 0 | 0 | 0 |
| run | 12 | 284.848 | 295.809 | 5.4272 | 0.495146 | 1 |
| rest | 1 | 32.6392 | 44.1136 | 0 | 0 | 0 |
| rest | 2 | 57.3544 | 72.944 | 8.1304 | 0.521527 | 1 |
| rest | 3 | 84.184 | 92.1656 | 3.7776 | 0.473289 | 1 |
| rest | 4 | 102.75 | 113.55 | 6.3568 | 0.588593 | 1 |
| rest | 5 | 123.501 | 136.72 | 0 | 0 | 0 |
| rest | 6 | 147.406 | 157.52 | 8.0624 | 0.797184 | 1 |
| rest | 7 | 168.273 | 174.398 | 0 | 0 | 0 |
| rest | 8 | 183.76 | 200.252 | 8.3424 | 0.505845 | 1 |
| rest | 9 | 209.55 | 218.855 | 7.3728 | 0.792297 | 1 |
| rest | 10 | 228.297 | 239.853 | 8.8616 | 0.76684 | 1 |
| rest | 11 | 253.654 | 260.736 | 0 | 0 | 0 |
| rest | 12 | 271.122 | 284.848 | 11.4504 | 0.834237 | 1 |

Cross-state intersections: [regional_historical_overlap_cross_state.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_historical_overlap_cross_state.csv>).

## Per-bout analysis and status

APC uses the byte-verified frozen source with ampRange 80–150 Hz and all other defaults. Additional raw/Ozkurt MVL and preferred phase use the exact frozen selected bands/filter designs; raw MVL and preferred phase are checked against the frozen output on every successful bout. A2' uses phase 4:0.5:12 Hz, half-width 1.5 Hz; amplitude 80:4:148 Hz, fixed half-width 12 Hz; MVL-raw, MVL-Ozkurt, KLMI and GLM, each at its own grid maximum. Comparator filtering is the corrected `butter(4)` zpk→SOS/filtfilt realization, with pole radius <1 and centre-gain error <1e-3 guards.

336 unique channel/bout inputs; 1680 method rows across CA1, EC and E1 sensitivity. Full fP, fA, raw/Ozkurt MVL, preferred phase, status, route and provenance: [regional_bout_estimates.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_bout_estimates.csv>). Full normalized APC options and comparator settings are stored per row/checkpoint. Guard table: [regional_comparator_filter_guards.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_comparator_filter_guards.csv>) (140 band/fs entries, all passed).

| analysis | method | state | status | bouts |
| --- | --- | --- | --- | --- |
| CA1 | APC-v1.0 | rest | 0 | 90 |
| CA1 | APC-v1.0 | rest | 4 | 2 |
| CA1 | APC-v1.0 | run | 0 | 20 |
| CA1 | GLM | rest | 0 | 92 |
| CA1 | GLM | run | 0 | 20 |
| CA1 | KLMI | rest | 0 | 92 |
| CA1 | KLMI | run | 0 | 20 |
| CA1 | MVL-Ozkurt | rest | 0 | 92 |
| CA1 | MVL-Ozkurt | run | 0 | 20 |
| CA1 | MVL-raw | rest | 0 | 92 |
| CA1 | MVL-raw | run | 0 | 20 |
| E1_sensitivity | APC-v1.0 | rest | 0 | 91 |
| E1_sensitivity | APC-v1.0 | rest | 4 | 1 |
| E1_sensitivity | APC-v1.0 | run | 0 | 20 |
| E1_sensitivity | GLM | rest | 0 | 92 |
| E1_sensitivity | GLM | run | 0 | 20 |
| E1_sensitivity | KLMI | rest | 0 | 92 |
| E1_sensitivity | KLMI | run | 0 | 20 |
| E1_sensitivity | MVL-Ozkurt | rest | 0 | 92 |
| E1_sensitivity | MVL-Ozkurt | run | 0 | 20 |
| E1_sensitivity | MVL-raw | rest | 0 | 92 |
| E1_sensitivity | MVL-raw | run | 0 | 20 |
| EC | APC-v1.0 | rest | 0 | 92 |
| EC | APC-v1.0 | run | 0 | 20 |
| EC | GLM | rest | 0 | 92 |
| EC | GLM | run | 0 | 20 |
| EC | KLMI | rest | 0 | 92 |
| EC | KLMI | run | 0 | 20 |
| EC | MVL-Ozkurt | rest | 0 | 92 |
| EC | MVL-Ozkurt | run | 0 | 20 |
| EC | MVL-raw | rest | 0 | 92 |
| EC | MVL-raw | run | 0 | 20 |

## Per-session and across-session statistics

Per-session run-minus-rest: Welch unequal-variance t, pooled-SD Hedges g with exact gamma correction, and 10,000 percentile bootstrap resamples (seed 20261022, deterministic session streams; indices shared across methods within each analysis/session). Finite-value denominators are shown. Across sessions: session-level differences, two-sided one-sample t and Wilcoxon signed-rank tests, zero differences recorded, no multiplicity correction. EC012 n=0 rows are unavailable; pooled results equal EC013 because only EC013 qualifies.

Full CSVs: [regional_session_statistics.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_session_statistics.csv>); [regional_across_session_statistics.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_across_session_statistics.csv>); [regional_state_summary.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_state_summary.csv>). One SciPy precision-loss warning was returned for the CA1 ec013.157 KLMI fP Welch comparison (nearly identical values). The original test output is retained with its warning; no estimator or data adjustment was applied. Warning/context: [regional_statistics_warnings.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_statistics_warnings.csv>).

### CA1

| session | method | outcome | n_run | n_rest | run_mean | rest_mean | mean_difference | welch_t | welch_df | welch_p | hedges_g | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ec013.156 | APC-v1.0 | fP_hz | 9 | 43 | 7.63966 | 6.30214 | 1.33752 | 13.1584 | 33.3945 | 9.11751e-15 | 2.78814 | 1.14915 | 1.53166 |
| ec013.156 | APC-v1.0 | fA_hz | 9 | 43 | 118.333 | 118 | 0.333333 | 0.047496 | 11.5314 | 0.962931 | 0.0172553 | -12.7652 | 13.1037 |
| ec013.156 | APC-v1.0 | ozkurt_mvl | 9 | 43 | 0.0526076 | 0.0461091 | 0.00649848 | 1.51471 | 31.6739 | 0.139763 | 0.326324 | -0.00164768 | 0.014682 |
| ec013.156 | GLM | fP_hz | 9 | 43 | 7.5 | 6.76744 | 0.732558 | 0.79785 | 10.8424 | 0.442082 | 0.310386 | -1.00904 | 2.45223 |
| ec013.156 | GLM | fA_hz | 9 | 43 | 105.778 | 114.419 | -8.64083 | -0.952151 | 9.58852 | 0.364405 | -0.443541 | -24.8062 | 8.42403 |
| ec013.156 | GLM | ozkurt_mvl | 9 | 43 | 0.082488 | 0.0669717 | 0.0155163 | 1.73583 | 8.7859 | 0.117432 | 0.9814 | -0.00217912 | 0.0311618 |
| ec013.156 | KLMI | fP_hz | 9 | 43 | 4.38889 | 4.76744 | -0.378553 | -1.44413 | 28.1595 | 0.159737 | -0.323141 | -0.869509 | 0.131783 |
| ec013.156 | KLMI | fA_hz | 9 | 43 | 98.6667 | 110.791 | -12.124 | -1.5602 | 11.2846 | 0.146303 | -0.579896 | -25.6744 | 2.77028 |
| ec013.156 | KLMI | ozkurt_mvl | 9 | 43 | 0.0772313 | 0.0648608 | 0.0123705 | 0.932692 | 9.1653 | 0.374896 | 0.475321 | -0.0111884 | 0.0376654 |
| ec013.156 | MVL-Ozkurt | fP_hz | 9 | 43 | 6.38889 | 5.93023 | 0.458656 | 0.422115 | 10.406 | 0.68153 | 0.17306 | -1.44577 | 2.54528 |
| ec013.156 | MVL-Ozkurt | fA_hz | 9 | 43 | 102.222 | 113.395 | -11.1731 | -1.18536 | 10.2722 | 0.262571 | -0.494759 | -27.7008 | 6.71835 |
| ec013.156 | MVL-Ozkurt | ozkurt_mvl | 9 | 43 | 0.0966078 | 0.0825474 | 0.0140604 | 1.57128 | 9.97688 | 0.147263 | 0.684831 | -0.00171074 | 0.0312989 |
| ec013.156 | MVL-raw | fP_hz | 9 | 43 | 5.66667 | 5.45349 | 0.213178 | 0.222337 | 10.2081 | 0.828437 | 0.0936347 | -1.33592 | 2.15772 |
| ec013.156 | MVL-raw | fA_hz | 9 | 43 | 80.8889 | 86.0465 | -5.15762 | -3.49535 | 49.9994 | 0.00100201 | -0.622197 | -8.02067 | -2.45995 |
| ec013.156 | MVL-raw | ozkurt_mvl | 9 | 43 | 0.0931526 | 0.0711127 | 0.0220399 | 2.15895 | 9.91177 | 0.0564458 | 0.950721 | 0.00344758 | 0.0411954 |
| ec013.157 | APC-v1.0 | fP_hz | 6 | 14 | 7.55024 | 6.20298 | 1.34726 | 7.29177 | 16.2072 | 1.6736e-06 | 2.73736 | 0.99851 | 1.68063 |
| ec013.157 | APC-v1.0 | fA_hz | 6 | 14 | 112.667 | 110.429 | 2.2381 | 0.272164 | 12.4611 | 0.789953 | 0.113819 | -12.5476 | 17.4617 |
| ec013.157 | APC-v1.0 | ozkurt_mvl | 6 | 14 | 0.0592746 | 0.042674 | 0.0166006 | 2.5592 | 16.8225 | 0.0204366 | 0.942287 | 0.00415899 | 0.0282318 |
| ec013.157 | GLM | fP_hz | 6 | 15 | 6.58333 | 6.33333 | 0.25 | 0.18701 | 7.54179 | 0.856585 | 0.0971048 | -2.1 | 2.68375 |
| ec013.157 | GLM | fA_hz | 6 | 15 | 110.667 | 108.8 | 1.86667 | 0.184898 | 11.3559 | 0.85657 | 0.0783091 | -17.2 | 19.7333 |
| ec013.157 | GLM | ozkurt_mvl | 6 | 15 | 0.0724334 | 0.0706731 | 0.00176031 | 0.151412 | 7.13498 | 0.883843 | 0.0815046 | -0.0186128 | 0.0231367 |
| ec013.157 | KLMI | fP_hz | 6 | 15 | 4 | 5.23333 | -1.23333 | -2.9212 | 14 | 0.0111643 | -0.843449 | -2.1 | -0.5 |
| ec013.157 | KLMI | fA_hz | 6 | 15 | 113.333 | 112.533 | 0.8 | 0.0642151 | 8.61118 | 0.950265 | 0.0309076 | -22 | 23.2 |
| ec013.157 | KLMI | ozkurt_mvl | 6 | 15 | 0.0518789 | 0.0721357 | -0.0202568 | -1.34109 | 6.79661 | 0.222973 | -0.747033 | -0.0462315 | 0.00745696 |
| ec013.157 | MVL-Ozkurt | fP_hz | 6 | 15 | 4.41667 | 5.43333 | -1.01667 | -2.04522 | 18.0654 | 0.0556806 | -0.636672 | -1.98333 | -0.133333 |
| ec013.157 | MVL-Ozkurt | fA_hz | 6 | 15 | 108.667 | 116 | -7.33333 | -0.663394 | 9.53331 | 0.522795 | -0.303498 | -27.8667 | 12.5333 |
| ec013.157 | MVL-Ozkurt | ozkurt_mvl | 6 | 15 | 0.0949775 | 0.0792244 | 0.0157531 | 1.98639 | 11.5974 | 0.0711369 | 0.834036 | 0.00157687 | 0.0302649 |
| ec013.157 | MVL-raw | fP_hz | 6 | 15 | 5.41667 | 5.63333 | -0.216667 | -0.188079 | 10.5254 | 0.854392 | -0.0822651 | -2.15 | 2.05 |
| ec013.157 | MVL-raw | fA_hz | 6 | 15 | 81.3333 | 84.5333 | -3.2 | -1.59143 | 18.2818 | 0.128655 | -0.49862 | -7.2 | 0.266667 |
| ec013.157 | MVL-raw | ozkurt_mvl | 6 | 15 | 0.0809289 | 0.0656883 | 0.0152405 | 1.72144 | 6.66799 | 0.130976 | 0.972645 | -0.000332924 | 0.0319907 |
| ec013.375 | APC-v1.0 | fP_hz | 5 | 33 | 9.09767 | 9.66489 | -0.56722 | -0.286433 | 10.699 | 0.780017 | -0.0801911 | -4.02213 | 3.13666 |
| ec013.375 | APC-v1.0 | fA_hz | 5 | 33 | 114 | 117.636 | -3.63636 | -0.462856 | 6.12446 | 0.659458 | -0.182559 | -17.3549 | 10.6488 |
| ec013.375 | APC-v1.0 | ozkurt_mvl | 5 | 33 | 0.0599212 | 0.037472 | 0.0224492 | 2.17107 | 4.63514 | 0.0863325 | 1.31571 | 0.00486727 | 0.0408901 |
| ec013.375 | GLM | fP_hz | 5 | 34 | 6.9 | 7.30882 | -0.408824 | -0.390856 | 5.75315 | 0.709965 | -0.162504 | -2.31176 | 1.46471 |
| ec013.375 | GLM | fA_hz | 5 | 34 | 109.6 | 109.059 | 0.541176 | 0.0495625 | 5.30713 | 0.962283 | 0.0228763 | -16.2359 | 21.6476 |
| ec013.375 | GLM | ozkurt_mvl | 5 | 34 | 0.0671888 | 0.0694557 | -0.00226698 | -0.344857 | 10.5015 | 0.737009 | -0.0958797 | -0.0133323 | 0.0102677 |
| ec013.375 | KLMI | fP_hz | 5 | 34 | 5.4 | 5.14706 | 0.252941 | 0.454515 | 5.65041 | 0.666393 | 0.193026 | -0.708897 | 1.2589 |
| ec013.375 | KLMI | fA_hz | 5 | 34 | 99.2 | 107.529 | -8.32941 | -0.89622 | 5.8804 | 0.405328 | -0.363624 | -23.6941 | 8.72941 |
| ec013.375 | KLMI | ozkurt_mvl | 5 | 34 | 0.0804075 | 0.0598419 | 0.0205656 | 1.56795 | 5.68834 | 0.170625 | 0.660574 | -0.00171461 | 0.0444577 |
| ec013.375 | MVL-Ozkurt | fP_hz | 5 | 34 | 6.6 | 5.72059 | 0.879412 | 0.733824 | 4.98802 | 0.496078 | 0.374957 | -1.15007 | 3.08529 |
| ec013.375 | MVL-Ozkurt | fA_hz | 5 | 34 | 116.8 | 114.353 | 2.44706 | 0.242587 | 5.85957 | 0.816593 | 0.0988065 | -16.7529 | 19.2476 |
| ec013.375 | MVL-Ozkurt | ozkurt_mvl | 5 | 34 | 0.111883 | 0.0876633 | 0.0242193 | 2.17675 | 5.61398 | 0.075494 | 0.931755 | 0.00593717 | 0.0453173 |
| ec013.375 | MVL-raw | fP_hz | 5 | 34 | 6.5 | 5.67647 | 0.823529 | 0.666361 | 4.9282 | 0.5351 | 0.348336 | -1.25 | 3.08529 |
| ec013.375 | MVL-raw | fA_hz | 5 | 34 | 116.8 | 113.529 | 3.27059 | 0.361224 | 6.6911 | 0.729067 | 0.129892 | -14.0959 | 18.1653 |
| ec013.375 | MVL-raw | ozkurt_mvl | 5 | 34 | 0.111538 | 0.087178 | 0.0243597 | 2.20268 | 5.57643 | 0.0732475 | 0.950749 | 0.00633074 | 0.0454335 |

| animal_pool | method | outcome | n_sessions | mean_session_difference | median_session_difference | ci_low | ci_high | one_sample_t | one_sample_p | wilcoxon_statistic | wilcoxon_p | zero_differences |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EC012 | APC-v1.0 | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | APC-v1.0 | fA_hz | 3 | -0.354978 | 0.333333 | -7.8002 | 7.09025 | -0.205145 | 0.856443 | 3 | 1 | 0 |
| pooled | APC-v1.0 | fA_hz | 3 | -0.354978 | 0.333333 | -7.8002 | 7.09025 | -0.205145 | 0.856443 | 3 | 1 | 0 |
| EC012 | APC-v1.0 | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | APC-v1.0 | fP_hz | 3 | 0.705852 | 1.33752 | -2.03297 | 3.44467 | 1.10888 | 0.382964 | 1 | 0.5 | 0 |
| pooled | APC-v1.0 | fP_hz | 3 | 0.705852 | 1.33752 | -2.03297 | 3.44467 | 1.10888 | 0.382964 | 1 | 0.5 | 0 |
| EC012 | APC-v1.0 | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | APC-v1.0 | ozkurt_mvl | 3 | 0.0151827 | 0.0166006 | -0.00486253 | 0.035228 | 3.25893 | 0.0826512 | 0 | 0.25 | 0 |
| pooled | APC-v1.0 | ozkurt_mvl | 3 | 0.0151827 | 0.0166006 | -0.00486253 | 0.035228 | 3.25893 | 0.0826512 | 0 | 0.25 | 0 |
| EC012 | GLM | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | GLM | fA_hz | 3 | -2.07766 | 0.541176 | -16.2928 | 12.1375 | -0.628867 | 0.593685 | 3 | 1 | 0 |
| pooled | GLM | fA_hz | 3 | -2.07766 | 0.541176 | -16.2928 | 12.1375 | -0.628867 | 0.593685 | 3 | 1 | 0 |
| EC012 | GLM | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | GLM | fP_hz | 3 | 0.191245 | 0.25 | -1.23205 | 1.61454 | 0.578136 | 0.621595 | 2 | 0.75 | 0 |
| pooled | GLM | fP_hz | 3 | 0.191245 | 0.25 | -1.23205 | 1.61454 | 0.578136 | 0.621595 | 2 | 0.75 | 0 |
| EC012 | GLM | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | GLM | ozkurt_mvl | 3 | 0.0050032 | 0.00176031 | -0.0181604 | 0.0281668 | 0.929347 | 0.450819 | 2 | 0.75 | 0 |
| pooled | GLM | ozkurt_mvl | 3 | 0.0050032 | 0.00176031 | -0.0181604 | 0.0281668 | 0.929347 | 0.450819 | 2 | 0.75 | 0 |
| EC012 | KLMI | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | KLMI | fA_hz | 3 | -6.55115 | -8.32941 | -23.0532 | 9.95095 | -1.7081 | 0.229741 | 1 | 0.5 | 0 |
| pooled | KLMI | fA_hz | 3 | -6.55115 | -8.32941 | -23.0532 | 9.95095 | -1.7081 | 0.229741 | 1 | 0.5 | 0 |
| EC012 | KLMI | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | KLMI | fP_hz | 3 | -0.452982 | -0.378553 | -2.30597 | 1.4 | -1.05183 | 0.403212 | 1 | 0.5 | 0 |
| pooled | KLMI | fP_hz | 3 | -0.452982 | -0.378553 | -2.30597 | 1.4 | -1.05183 | 0.403212 | 1 | 0.5 | 0 |
| EC012 | KLMI | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | KLMI | ozkurt_mvl | 3 | 0.0042264 | 0.0123705 | -0.0494195 | 0.0578723 | 0.338977 | 0.766909 | 2 | 0.75 | 0 |
| pooled | KLMI | ozkurt_mvl | 3 | 0.0042264 | 0.0123705 | -0.0494195 | 0.0578723 | 0.338977 | 0.766909 | 2 | 0.75 | 0 |
| EC012 | MVL-Ozkurt | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-Ozkurt | fA_hz | 3 | -5.35313 | -7.33333 | -22.7985 | 12.0922 | -1.32028 | 0.317587 | 1 | 0.5 | 0 |
| pooled | MVL-Ozkurt | fA_hz | 3 | -5.35313 | -7.33333 | -22.7985 | 12.0922 | -1.32028 | 0.317587 | 1 | 0.5 | 0 |
| EC012 | MVL-Ozkurt | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-Ozkurt | fP_hz | 3 | 0.107134 | 0.458656 | -2.36637 | 2.58063 | 0.186359 | 0.869354 | 3 | 1 | 0 |
| pooled | MVL-Ozkurt | fP_hz | 3 | 0.107134 | 0.458656 | -2.36637 | 2.58063 | 0.186359 | 0.869354 | 3 | 1 | 0 |
| EC012 | MVL-Ozkurt | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-Ozkurt | ozkurt_mvl | 3 | 0.018011 | 0.0157531 | 0.00449023 | 0.0315317 | 5.73156 | 0.0291177 | 0 | 0.25 | 0 |
| pooled | MVL-Ozkurt | ozkurt_mvl | 3 | 0.018011 | 0.0157531 | 0.00449023 | 0.0315317 | 5.73156 | 0.0291177 | 0 | 0.25 | 0 |
| EC012 | MVL-raw | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-raw | fA_hz | 3 | -1.69568 | -3.2 | -12.6529 | 9.26157 | -0.665853 | 0.574025 | 2 | 0.75 | 0 |
| pooled | MVL-raw | fA_hz | 3 | -1.69568 | -3.2 | -12.6529 | 9.26157 | -0.665853 | 0.574025 | 2 | 0.75 | 0 |
| EC012 | MVL-raw | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-raw | fP_hz | 3 | 0.273347 | 0.213178 | -1.02512 | 1.57181 | 0.905776 | 0.460659 | 2 | 0.75 | 0 |
| pooled | MVL-raw | fP_hz | 3 | 0.273347 | 0.213178 | -1.02512 | 1.57181 | 0.905776 | 0.460659 | 2 | 0.75 | 0 |
| EC012 | MVL-raw | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-raw | ozkurt_mvl | 3 | 0.0205467 | 0.0220399 | 0.00877337 | 0.0323201 | 7.50894 | 0.0172772 | 0 | 0.25 | 0 |
| pooled | MVL-raw | ozkurt_mvl | 3 | 0.0205467 | 0.0220399 | 0.00877337 | 0.0323201 | 7.50894 | 0.0172772 | 0 | 0.25 | 0 |

### EC

| session | method | outcome | n_run | n_rest | run_mean | rest_mean | mean_difference | welch_t | welch_df | welch_p | hedges_g | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ec013.156 | APC-v1.0 | fP_hz | 9 | 43 | 7.57757 | 6.43722 | 1.14035 | 16.6354 | 20.3853 | 2.48661e-13 | 4.19601 | 1.01428 | 1.27076 |
| ec013.156 | APC-v1.0 | fA_hz | 9 | 43 | 114.444 | 105.93 | 8.51421 | 1.15417 | 11.293 | 0.272271 | 0.428637 | -5.39541 | 21.9922 |
| ec013.156 | APC-v1.0 | ozkurt_mvl | 9 | 43 | 0.0870279 | 0.0674079 | 0.0196201 | 2.6564 | 10.2577 | 0.023569 | 1.11099 | 0.00542844 | 0.0330601 |
| ec013.156 | GLM | fP_hz | 9 | 43 | 7.33333 | 6.38372 | 0.949612 | 1.99566 | 14.412 | 0.0652289 | 0.603928 | 0.0788114 | 1.84625 |
| ec013.156 | GLM | fA_hz | 9 | 43 | 103.556 | 104.279 | -0.723514 | -0.116365 | 14.6528 | 0.908943 | -0.0348352 | -12.3623 | 11.0705 |
| ec013.156 | GLM | ozkurt_mvl | 9 | 43 | 0.113988 | 0.0853647 | 0.0286229 | 4.21806 | 9.82109 | 0.00184953 | 1.88535 | 0.0154733 | 0.0408505 |
| ec013.156 | KLMI | fP_hz | 9 | 43 | 7.33333 | 5.53488 | 1.79845 | 3.82748 | 12.7589 | 0.0021636 | 1.26718 | 0.905652 | 2.65507 |
| ec013.156 | KLMI | fA_hz | 9 | 43 | 104 | 99.3488 | 4.65116 | 0.724502 | 12.732 | 0.48186 | 0.240282 | -7.277 | 16.5584 |
| ec013.156 | KLMI | ozkurt_mvl | 9 | 43 | 0.113334 | 0.0791403 | 0.0341934 | 4.76567 | 13.4075 | 0.000339048 | 1.51749 | 0.0209435 | 0.0475322 |
| ec013.156 | MVL-Ozkurt | fP_hz | 9 | 43 | 6.66667 | 5.94186 | 0.724806 | 1.1208 | 10.6786 | 0.286945 | 0.444256 | -0.470317 | 1.92248 |
| ec013.156 | MVL-Ozkurt | fA_hz | 9 | 43 | 103.556 | 102.326 | 1.22997 | 0.189516 | 14.1582 | 0.852379 | 0.0580407 | -11.2558 | 13.3132 |
| ec013.156 | MVL-Ozkurt | ozkurt_mvl | 9 | 43 | 0.120473 | 0.0935626 | 0.0269101 | 5.40281 | 11.2172 | 0.000201553 | 2.02128 | 0.0175704 | 0.0362556 |
| ec013.156 | MVL-raw | fP_hz | 9 | 43 | 7.05556 | 6.0814 | 0.97416 | 1.64379 | 11.2794 | 0.127778 | 0.611265 | -0.139599 | 2.09173 |
| ec013.156 | MVL-raw | fA_hz | 9 | 43 | 90.2222 | 83.5349 | 6.68734 | 1.54428 | 8.84727 | 0.157497 | 0.856864 | -1.07494 | 14.8114 |
| ec013.156 | MVL-raw | ozkurt_mvl | 9 | 43 | 0.117828 | 0.084382 | 0.0334462 | 6.56344 | 13.491 | 1.51448e-05 | 2.08029 | 0.0239423 | 0.0431113 |
| ec013.157 | APC-v1.0 | fP_hz | 6 | 15 | 7.54615 | 6.49335 | 1.05281 | 7.38744 | 18.8158 | 5.69039e-07 | 2.48445 | 0.77832 | 1.30741 |
| ec013.157 | APC-v1.0 | fA_hz | 6 | 15 | 109.5 | 113.533 | -4.03333 | -0.398614 | 10.1928 | 0.698401 | -0.176839 | -23.2333 | 13.8667 |
| ec013.157 | APC-v1.0 | ozkurt_mvl | 6 | 15 | 0.0897331 | 0.0625114 | 0.0272217 | 1.90281 | 5.84509 | 0.107044 | 1.20407 | -0.000309521 | 0.0505737 |
| ec013.157 | GLM | fP_hz | 6 | 15 | 7.25 | 5.93333 | 1.31667 | 2.22469 | 9.53634 | 0.0515427 | 1.01762 | 0.233333 | 2.38333 |
| ec013.157 | GLM | fA_hz | 6 | 15 | 105.333 | 102.667 | 2.66667 | 0.414717 | 13.8083 | 0.68472 | 0.162499 | -9.46667 | 14 |
| ec013.157 | GLM | ozkurt_mvl | 6 | 15 | 0.127859 | 0.0880686 | 0.0397904 | 6.65702 | 17.3817 | 3.61058e-06 | 2.36726 | 0.0285042 | 0.0507384 |
| ec013.157 | KLMI | fP_hz | 6 | 15 | 7.25 | 5.5 | 1.75 | 3.67477 | 10.8929 | 0.00371806 | 1.58377 | 0.833333 | 2.56667 |
| ec013.157 | KLMI | fA_hz | 6 | 15 | 110.667 | 99.2 | 11.4667 | 2.17222 | 17.1378 | 0.0441535 | 0.777928 | 1.46667 | 21.0667 |
| ec013.157 | KLMI | ozkurt_mvl | 6 | 15 | 0.126807 | 0.0845416 | 0.0422651 | 6.03483 | 17.238 | 1.26186e-05 | 2.15503 | 0.0294396 | 0.0555074 |
| ec013.157 | MVL-Ozkurt | fP_hz | 6 | 15 | 6.66667 | 5.33333 | 1.33333 | 1.64677 | 6.39537 | 0.147638 | 0.961493 | -0.166667 | 2.73333 |
| ec013.157 | MVL-Ozkurt | fA_hz | 6 | 15 | 110 | 101.6 | 8.4 | 1.32175 | 10.636 | 0.213974 | 0.575514 | -3.33333 | 20 |
| ec013.157 | MVL-Ozkurt | ozkurt_mvl | 6 | 15 | 0.141641 | 0.0950327 | 0.0466078 | 5.25087 | 11.6267 | 0.000226613 | 2.20243 | 0.0307405 | 0.0631259 |
| ec013.157 | MVL-raw | fP_hz | 6 | 15 | 6.25 | 5.6 | 0.65 | 0.830217 | 7.49227 | 0.432072 | 0.432872 | -0.733333 | 2.06667 |
| ec013.157 | MVL-raw | fA_hz | 6 | 15 | 92.6667 | 87.4667 | 5.2 | 1.34028 | 7.49037 | 0.219382 | 0.69893 | -1.86667 | 12.1333 |
| ec013.157 | MVL-raw | ozkurt_mvl | 6 | 15 | 0.127261 | 0.0879879 | 0.039273 | 4.2444 | 11.7795 | 0.00118569 | 1.77084 | 0.0230748 | 0.0569025 |
| ec013.375 | APC-v1.0 | fP_hz | 5 | 34 | 7.27631 | 5.93895 | 1.33736 | 4.0679 | 36.543 | 0.000242448 | 0.780428 | 0.758837 | 2.01488 |
| ec013.375 | APC-v1.0 | fA_hz | 5 | 34 | 98.6 | 108.529 | -9.92941 | -2.00534 | 9.8841 | 0.0730702 | -0.572185 | -18.8826 | -1.27044 |
| ec013.375 | APC-v1.0 | ozkurt_mvl | 5 | 34 | 0.112873 | 0.0757787 | 0.0370946 | 3.60268 | 6.77222 | 0.00921224 | 1.28305 | 0.0183604 | 0.0553621 |
| ec013.375 | GLM | fP_hz | 5 | 34 | 6.9 | 6.16176 | 0.738235 | 1.144 | 6.13688 | 0.295276 | 0.444205 | -0.385294 | 1.90007 |
| ec013.375 | GLM | fA_hz | 5 | 34 | 101.6 | 105.765 | -4.16471 | -0.739875 | 10.9913 | 0.474883 | -0.201962 | -14.7294 | 5.95294 |
| ec013.375 | GLM | ozkurt_mvl | 5 | 34 | 0.133403 | 0.0861834 | 0.0472194 | 5.60117 | 5.76293 | 0.00157795 | 2.32423 | 0.0313707 | 0.0609255 |
| ec013.375 | KLMI | fP_hz | 5 | 34 | 6.3 | 5.30882 | 0.991176 | 1.54207 | 5.1138 | 0.182411 | 0.754276 | -0.0411765 | 2.20596 |
| ec013.375 | KLMI | fA_hz | 5 | 34 | 97.6 | 108.471 | -10.8706 | -2.19225 | 14.5168 | 0.045113 | -0.543792 | -20.0941 | -1.85882 |
| ec013.375 | KLMI | ozkurt_mvl | 5 | 34 | 0.135823 | 0.084507 | 0.0513159 | 5.84875 | 6.00634 | 0.00109822 | 2.32049 | 0.0346271 | 0.0651837 |
| ec013.375 | MVL-Ozkurt | fP_hz | 5 | 34 | 6.4 | 5.82353 | 0.576471 | 0.877382 | 5.72434 | 0.415579 | 0.366909 | -0.514706 | 1.80294 |
| ec013.375 | MVL-Ozkurt | fA_hz | 5 | 34 | 104 | 103.059 | 0.941176 | 0.149655 | 8.25121 | 0.88463 | 0.0467301 | -10.7065 | 12.3065 |
| ec013.375 | MVL-Ozkurt | ozkurt_mvl | 5 | 34 | 0.137218 | 0.0943872 | 0.0428304 | 4.9895 | 5.43385 | 0.00328408 | 2.22764 | 0.0261172 | 0.0556854 |
| ec013.375 | MVL-raw | fP_hz | 5 | 34 | 6.1 | 6.11765 | -0.0176471 | -0.0263041 | 5.44794 | 0.979951 | -0.0117029 | -1.04118 | 1.27654 |
| ec013.375 | MVL-raw | fA_hz | 5 | 34 | 95.2 | 83.1765 | 12.0235 | 2.54673 | 4.32237 | 0.0589874 | 1.92732 | 3.52882 | 19.9065 |
| ec013.375 | MVL-raw | ozkurt_mvl | 5 | 34 | 0.134439 | 0.0854422 | 0.0489966 | 6.06729 | 5.40327 | 0.00133353 | 2.72985 | 0.033517 | 0.0613545 |

| animal_pool | method | outcome | n_sessions | mean_session_difference | median_session_difference | ci_low | ci_high | one_sample_t | one_sample_p | wilcoxon_statistic | wilcoxon_p | zero_differences |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EC012 | APC-v1.0 | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | APC-v1.0 | fA_hz | 3 | -1.81618 | -4.03333 | -25.2157 | 21.5834 | -0.333954 | 0.770179 | 2 | 0.75 | 0 |
| pooled | APC-v1.0 | fA_hz | 3 | -1.81618 | -4.03333 | -25.2157 | 21.5834 | -0.333954 | 0.770179 | 2 | 0.75 | 0 |
| EC012 | APC-v1.0 | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | APC-v1.0 | fP_hz | 3 | 1.17684 | 1.14035 | 0.814791 | 1.53889 | 13.9857 | 0.0050736 | 0 | 0.25 | 0 |
| pooled | APC-v1.0 | fP_hz | 3 | 1.17684 | 1.14035 | 0.814791 | 1.53889 | 13.9857 | 0.0050736 | 0 | 0.25 | 0 |
| EC012 | APC-v1.0 | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | APC-v1.0 | ozkurt_mvl | 3 | 0.0279788 | 0.0272217 | 0.00621326 | 0.0497443 | 5.5309 | 0.0311692 | 0 | 0.25 | 0 |
| pooled | APC-v1.0 | ozkurt_mvl | 3 | 0.0279788 | 0.0272217 | 0.00621326 | 0.0497443 | 5.5309 | 0.0311692 | 0 | 0.25 | 0 |
| EC012 | GLM | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | GLM | fA_hz | 3 | -0.740518 | -0.723514 | -9.22563 | 7.7446 | -0.375504 | 0.743371 | 2 | 0.75 | 0 |
| pooled | GLM | fA_hz | 3 | -0.740518 | -0.723514 | -9.22563 | 7.7446 | -0.375504 | 0.743371 | 2 | 0.75 | 0 |
| EC012 | GLM | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | GLM | fP_hz | 3 | 1.0015 | 0.949612 | 0.274431 | 1.72858 | 5.92668 | 0.0273086 | 0 | 0.25 | 0 |
| pooled | GLM | fP_hz | 3 | 1.0015 | 0.949612 | 0.274431 | 1.72858 | 5.92668 | 0.0273086 | 0 | 0.25 | 0 |
| EC012 | GLM | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | GLM | ozkurt_mvl | 3 | 0.0385442 | 0.0397904 | 0.015291 | 0.0617975 | 7.13201 | 0.0190983 | 0 | 0.25 | 0 |
| pooled | GLM | ozkurt_mvl | 3 | 0.0385442 | 0.0397904 | 0.015291 | 0.0617975 | 7.13201 | 0.0190983 | 0 | 0.25 | 0 |
| EC012 | KLMI | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | KLMI | fA_hz | 3 | 1.74908 | 4.65116 | -26.6891 | 30.1873 | 0.264633 | 0.816069 | 2 | 0.75 | 0 |
| pooled | KLMI | fA_hz | 3 | 1.74908 | 4.65116 | -26.6891 | 30.1873 | 0.264633 | 0.816069 | 2 | 0.75 | 0 |
| EC012 | KLMI | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | KLMI | fP_hz | 3 | 1.51321 | 1.75 | 0.388536 | 2.63788 | 5.78907 | 0.0285664 | 0 | 0.25 | 0 |
| pooled | KLMI | fP_hz | 3 | 1.51321 | 1.75 | 0.388536 | 2.63788 | 5.78907 | 0.0285664 | 0 | 0.25 | 0 |
| EC012 | KLMI | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | KLMI | ozkurt_mvl | 3 | 0.0425915 | 0.0422651 | 0.0213126 | 0.0638703 | 8.61213 | 0.0132161 | 0 | 0.25 | 0 |
| pooled | KLMI | ozkurt_mvl | 3 | 0.0425915 | 0.0422651 | 0.0213126 | 0.0638703 | 8.61213 | 0.0132161 | 0 | 0.25 | 0 |
| EC012 | MVL-Ozkurt | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-Ozkurt | fA_hz | 3 | 3.52372 | 1.22997 | -6.97289 | 14.0203 | 1.4444 | 0.285465 | 0 | 0.25 | 0 |
| pooled | MVL-Ozkurt | fA_hz | 3 | 3.52372 | 1.22997 | -6.97289 | 14.0203 | 1.4444 | 0.285465 | 0 | 0.25 | 0 |
| EC012 | MVL-Ozkurt | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-Ozkurt | fP_hz | 3 | 0.878203 | 0.724806 | -0.118113 | 1.87452 | 3.79257 | 0.0630225 | 0 | 0.25 | 0 |
| pooled | MVL-Ozkurt | fP_hz | 3 | 0.878203 | 0.724806 | -0.118113 | 1.87452 | 3.79257 | 0.0630225 | 0 | 0.25 | 0 |
| EC012 | MVL-Ozkurt | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-Ozkurt | ozkurt_mvl | 3 | 0.0387828 | 0.0428304 | 0.0128135 | 0.0647521 | 6.42561 | 0.023374 | 0 | 0.25 | 0 |
| pooled | MVL-Ozkurt | ozkurt_mvl | 3 | 0.0387828 | 0.0428304 | 0.0128135 | 0.0647521 | 6.42561 | 0.023374 | 0 | 0.25 | 0 |
| EC012 | MVL-raw | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-raw | fA_hz | 3 | 7.97029 | 6.68734 | -0.943097 | 16.8837 | 3.8474 | 0.0613999 | 0 | 0.25 | 0 |
| pooled | MVL-raw | fA_hz | 3 | 7.97029 | 6.68734 | -0.943097 | 16.8837 | 3.8474 | 0.0613999 | 0 | 0.25 | 0 |
| EC012 | MVL-raw | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-raw | fP_hz | 3 | 0.535504 | 0.65 | -0.720773 | 1.79178 | 1.83406 | 0.208085 | 1 | 0.5 | 0 |
| pooled | MVL-raw | fP_hz | 3 | 0.535504 | 0.65 | -0.720773 | 1.79178 | 1.83406 | 0.208085 | 1 | 0.5 | 0 |
| EC012 | MVL-raw | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-raw | ozkurt_mvl | 3 | 0.0405719 | 0.039273 | 0.0210561 | 0.0600877 | 8.94491 | 0.0122687 | 0 | 0.25 | 0 |
| pooled | MVL-raw | ozkurt_mvl | 3 | 0.0405719 | 0.039273 | 0.0210561 | 0.0600877 | 8.94491 | 0.0122687 | 0 | 0.25 | 0 |

### E1_sensitivity

| session | method | outcome | n_run | n_rest | run_mean | rest_mean | mean_difference | welch_t | welch_df | welch_p | hedges_g | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ec013.156 | APC-v1.0 | fP_hz | 9 | 43 | 7.591 | 6.41896 | 1.17204 | 16.7826 | 17.7689 | 2.42646e-12 | 4.50743 | 1.04491 | 1.30237 |
| ec013.156 | APC-v1.0 | fA_hz | 9 | 43 | 116 | 109.535 | 6.46512 | 1.08269 | 14.0271 | 0.297207 | 0.333708 | -4.50407 | 17.2196 |
| ec013.156 | APC-v1.0 | ozkurt_mvl | 9 | 43 | 0.0926934 | 0.0672551 | 0.0254384 | 3.77682 | 12.1215 | 0.00259411 | 1.30731 | 0.0126484 | 0.0376025 |
| ec013.156 | GLM | fP_hz | 9 | 43 | 7.05556 | 6.25581 | 0.799742 | 1.87194 | 11.9021 | 0.0859843 | 0.65911 | 0.0348837 | 1.59952 |
| ec013.156 | GLM | fA_hz | 9 | 43 | 113.333 | 104 | 9.33333 | 1.04745 | 10.4491 | 0.318516 | 0.427046 | -6.74987 | 25.9331 |
| ec013.156 | GLM | ozkurt_mvl | 9 | 43 | 0.115745 | 0.0890878 | 0.0266576 | 3.48793 | 9.177 | 0.00665165 | 1.77256 | 0.0116154 | 0.040105 |
| ec013.156 | KLMI | fP_hz | 9 | 43 | 6.55556 | 5.39535 | 1.16021 | 2.11691 | 9.60288 | 0.0614578 | 0.983471 | 0.136951 | 2.15507 |
| ec013.156 | KLMI | fA_hz | 9 | 43 | 104.889 | 102.605 | 2.28424 | 0.325412 | 11.8222 | 0.750557 | 0.115322 | -9.63307 | 16.0625 |
| ec013.156 | KLMI | ozkurt_mvl | 9 | 43 | 0.110362 | 0.0818073 | 0.0285548 | 2.58686 | 9.81236 | 0.0274821 | 1.15795 | 0.00695996 | 0.0478123 |
| ec013.156 | MVL-Ozkurt | fP_hz | 9 | 43 | 6.16667 | 5.82558 | 0.341085 | 0.533941 | 11.4191 | 0.603622 | 0.195962 | -0.833333 | 1.51554 |
| ec013.156 | MVL-Ozkurt | fA_hz | 9 | 43 | 108.889 | 100.558 | 8.33075 | 1.23319 | 13.3572 | 0.238768 | 0.393787 | -4.42403 | 20.9612 |
| ec013.156 | MVL-Ozkurt | ozkurt_mvl | 9 | 43 | 0.124202 | 0.094837 | 0.0293648 | 5.54014 | 10.4184 | 0.00021346 | 2.2677 | 0.0194375 | 0.0391141 |
| ec013.156 | MVL-raw | fP_hz | 9 | 43 | 6.33333 | 5.93023 | 0.403101 | 0.779033 | 13.0115 | 0.449897 | 0.253863 | -0.578811 | 1.35921 |
| ec013.156 | MVL-raw | fA_hz | 9 | 43 | 92 | 84.6512 | 7.34884 | 1.73032 | 9.60831 | 0.115494 | 0.803052 | -0.341602 | 15.5147 |
| ec013.156 | MVL-raw | ozkurt_mvl | 9 | 43 | 0.120608 | 0.0887394 | 0.0318687 | 4.9782 | 10.4622 | 0.000484403 | 2.02624 | 0.0200134 | 0.0436991 |
| ec013.157 | APC-v1.0 | fP_hz | 6 | 15 | 7.53797 | 6.44485 | 1.09313 | 7.13043 | 18.0946 | 1.17552e-06 | 2.47849 | 0.794612 | 1.3613 |
| ec013.157 | APC-v1.0 | fA_hz | 6 | 15 | 114.167 | 105.867 | 8.3 | 1.03253 | 12.5397 | 0.321326 | 0.42014 | -7.16667 | 22.3333 |
| ec013.157 | APC-v1.0 | ozkurt_mvl | 6 | 15 | 0.111899 | 0.0654685 | 0.0464304 | 3.92338 | 7.82941 | 0.00458792 | 1.99139 | 0.0263703 | 0.0684509 |
| ec013.157 | GLM | fP_hz | 6 | 15 | 8 | 5.86667 | 2.13333 | 4.23718 | 14.0092 | 0.000827351 | 1.65092 | 1.18333 | 3.03333 |
| ec013.157 | GLM | fA_hz | 6 | 15 | 109.333 | 105.067 | 4.26667 | 0.552664 | 8.99032 | 0.593966 | 0.260175 | -9.46667 | 18.4 |
| ec013.157 | GLM | ozkurt_mvl | 6 | 15 | 0.124273 | 0.090895 | 0.0333775 | 3.14727 | 8.17987 | 0.0132764 | 1.55768 | 0.0156125 | 0.054083 |
| ec013.157 | KLMI | fP_hz | 6 | 15 | 7.66667 | 5.36667 | 2.3 | 6.4665 | 18.8157 | 3.54633e-06 | 2.07226 | 1.63333 | 2.96667 |
| ec013.157 | KLMI | fA_hz | 6 | 15 | 111.333 | 100.533 | 10.8 | 1.53519 | 16.8976 | 0.143249 | 0.553514 | -2.93333 | 23.4667 |
| ec013.157 | KLMI | ozkurt_mvl | 6 | 15 | 0.126862 | 0.0865606 | 0.0403011 | 3.31364 | 12.2461 | 0.00602732 | 1.36107 | 0.0190382 | 0.063252 |
| ec013.157 | MVL-Ozkurt | fP_hz | 6 | 15 | 7.33333 | 5.53333 | 1.8 | 2.63403 | 8.79297 | 0.0277017 | 1.25409 | 0.566667 | 3.06667 |
| ec013.157 | MVL-Ozkurt | fA_hz | 6 | 15 | 119.333 | 109.867 | 9.46667 | 1.37343 | 17.5224 | 0.186939 | 0.486348 | -3.87 | 22 |
| ec013.157 | MVL-Ozkurt | ozkurt_mvl | 6 | 15 | 0.133674 | 0.0974083 | 0.0362652 | 4.08256 | 11.7133 | 0.00159498 | 1.70722 | 0.0215427 | 0.0535996 |
| ec013.157 | MVL-raw | fP_hz | 6 | 15 | 7.25 | 5.96667 | 1.28333 | 1.86572 | 10.4731 | 0.0903098 | 0.817836 | 0.0666667 | 2.56667 |
| ec013.157 | MVL-raw | fA_hz | 6 | 15 | 95.3333 | 88.2667 | 7.06667 | 1.49625 | 16.0933 | 0.153942 | 0.551325 | -2.53333 | 14.8 |
| ec013.157 | MVL-raw | ozkurt_mvl | 6 | 15 | 0.120164 | 0.0873068 | 0.0328573 | 2.73844 | 8.54277 | 0.0240104 | 1.32362 | 0.0126819 | 0.056046 |
| ec013.375 | APC-v1.0 | fP_hz | 5 | 33 | 7.32831 | 6.05632 | 1.27199 | 4.02273 | 34.9775 | 0.000292556 | 0.794194 | 0.710368 | 1.90598 |
| ec013.375 | APC-v1.0 | fA_hz | 5 | 33 | 98.6 | 113.758 | -15.1576 | -3.11825 | 9.0286 | 0.0123065 | -0.941908 | -23.8911 | -6.49091 |
| ec013.375 | APC-v1.0 | ozkurt_mvl | 5 | 33 | 0.113778 | 0.0678004 | 0.0459779 | 4.22352 | 6.04778 | 0.00544228 | 1.68677 | 0.0270436 | 0.0657096 |
| ec013.375 | GLM | fP_hz | 5 | 34 | 6.9 | 6.27941 | 0.620588 | 1.00017 | 5.2688 | 0.360921 | 0.466632 | -0.458824 | 1.73529 |
| ec013.375 | GLM | fA_hz | 5 | 34 | 98.4 | 106.941 | -8.54118 | -1.65775 | 13.477 | 0.120452 | -0.420885 | -18.0235 | 0.8 |
| ec013.375 | GLM | ozkurt_mvl | 5 | 34 | 0.135156 | 0.0859132 | 0.0492424 | 6.79817 | 6.17727 | 0.000438213 | 2.62294 | 0.0370447 | 0.0624715 |
| ec013.375 | KLMI | fP_hz | 5 | 34 | 6.3 | 5.75 | 0.55 | 0.839879 | 5.50112 | 0.435948 | 0.368885 | -0.511765 | 1.79118 |
| ec013.375 | KLMI | fA_hz | 5 | 34 | 97.6 | 108 | -10.4 | -2.30585 | 13.4451 | 0.0376362 | -0.58588 | -18.6594 | -2.32882 |
| ec013.375 | KLMI | ozkurt_mvl | 5 | 34 | 0.135762 | 0.0823609 | 0.0534007 | 6.87326 | 7.05516 | 0.000228691 | 2.37286 | 0.0403094 | 0.0674521 |
| ec013.375 | MVL-Ozkurt | fP_hz | 5 | 34 | 6.3 | 5.91176 | 0.388235 | 0.584644 | 5.80781 | 0.58077 | 0.240479 | -0.685294 | 1.62647 |
| ec013.375 | MVL-Ozkurt | fA_hz | 5 | 34 | 104 | 107.647 | -3.64706 | -0.557211 | 9.54006 | 0.590216 | -0.161562 | -15.5529 | 8.28294 |
| ec013.375 | MVL-Ozkurt | ozkurt_mvl | 5 | 34 | 0.140128 | 0.0948938 | 0.0452346 | 4.55648 | 4.9696 | 0.00616767 | 2.34424 | 0.0289007 | 0.0631768 |
| ec013.375 | MVL-raw | fP_hz | 5 | 34 | 6.9 | 5.89706 | 1.00294 | 1.18014 | 5.16285 | 0.289447 | 0.568269 | -0.453088 | 2.46176 |
| ec013.375 | MVL-raw | fA_hz | 5 | 34 | 93.6 | 84.2353 | 9.36471 | 1.88216 | 4.49036 | 0.125115 | 1.23745 | 0.941176 | 18.2118 |
| ec013.375 | MVL-raw | ozkurt_mvl | 5 | 34 | 0.133374 | 0.0865175 | 0.0468566 | 5.34643 | 5.27717 | 0.00260851 | 2.48847 | 0.0319156 | 0.0624935 |

| animal_pool | method | outcome | n_sessions | mean_session_difference | median_session_difference | ci_low | ci_high | one_sample_t | one_sample_p | wilcoxon_statistic | wilcoxon_p | zero_differences |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EC012 | APC-v1.0 | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | APC-v1.0 | fA_hz | 3 | -0.13082 | 6.46512 | -32.5385 | 32.2769 | -0.0173685 | 0.98772 | 3 | 1 | 0 |
| pooled | APC-v1.0 | fA_hz | 3 | -0.13082 | 6.46512 | -32.5385 | 32.2769 | -0.0173685 | 0.98772 | 3 | 1 | 0 |
| EC012 | APC-v1.0 | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | APC-v1.0 | fP_hz | 3 | 1.17905 | 1.17204 | 0.95638 | 1.40172 | 22.7828 | 0.00192103 | 0 | 0.25 | 0 |
| pooled | APC-v1.0 | fP_hz | 3 | 1.17905 | 1.17204 | 0.95638 | 1.40172 | 22.7828 | 0.00192103 | 0 | 0.25 | 0 |
| EC012 | APC-v1.0 | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | APC-v1.0 | ozkurt_mvl | 3 | 0.0392822 | 0.0459779 | 0.00949425 | 0.0690702 | 5.67403 | 0.029685 | 0 | 0.25 | 0 |
| pooled | APC-v1.0 | ozkurt_mvl | 3 | 0.0392822 | 0.0459779 | 0.00949425 | 0.0690702 | 5.67403 | 0.029685 | 0 | 0.25 | 0 |
| EC012 | GLM | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | GLM | fA_hz | 3 | 1.68627 | 4.26667 | -21.1986 | 24.5711 | 0.317041 | 0.781247 | 2 | 0.75 | 0 |
| pooled | GLM | fA_hz | 3 | 1.68627 | 4.26667 | -21.1986 | 24.5711 | 0.317041 | 0.781247 | 2 | 0.75 | 0 |
| EC012 | GLM | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | GLM | fP_hz | 3 | 1.18455 | 0.799742 | -0.868672 | 3.23778 | 2.4823 | 0.131118 | 0 | 0.25 | 0 |
| pooled | GLM | fP_hz | 3 | 1.18455 | 0.799742 | -0.868672 | 3.23778 | 2.4823 | 0.131118 | 0 | 0.25 | 0 |
| EC012 | GLM | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | GLM | ozkurt_mvl | 3 | 0.0364258 | 0.0333775 | 0.00761765 | 0.065234 | 5.44039 | 0.032165 | 0 | 0.25 | 0 |
| pooled | GLM | ozkurt_mvl | 3 | 0.0364258 | 0.0333775 | 0.00761765 | 0.065234 | 5.44039 | 0.032165 | 0 | 0.25 | 0 |
| EC012 | KLMI | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | KLMI | fA_hz | 3 | 0.894746 | 2.28424 | -25.6062 | 27.3957 | 0.145269 | 0.897817 | 2 | 0.75 | 0 |
| pooled | KLMI | fA_hz | 3 | 0.894746 | 2.28424 | -25.6062 | 27.3957 | 0.145269 | 0.897817 | 2 | 0.75 | 0 |
| EC012 | KLMI | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | KLMI | fP_hz | 3 | 1.33674 | 1.16021 | -0.869812 | 3.54328 | 2.60656 | 0.121036 | 0 | 0.25 | 0 |
| pooled | KLMI | fP_hz | 3 | 1.33674 | 1.16021 | -0.869812 | 3.54328 | 2.60656 | 0.121036 | 0 | 0.25 | 0 |
| EC012 | KLMI | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | KLMI | ozkurt_mvl | 3 | 0.0407522 | 0.0403011 | 0.00987667 | 0.0716278 | 5.67901 | 0.0296352 | 0 | 0.25 | 0 |
| pooled | KLMI | ozkurt_mvl | 3 | 0.0407522 | 0.0403011 | 0.00987667 | 0.0716278 | 5.67901 | 0.0296352 | 0 | 0.25 | 0 |
| EC012 | MVL-Ozkurt | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-Ozkurt | fA_hz | 3 | 4.71679 | 8.33075 | -13.3318 | 22.7654 | 1.12445 | 0.377644 | 1 | 0.5 | 0 |
| pooled | MVL-Ozkurt | fA_hz | 3 | 4.71679 | 8.33075 | -13.3318 | 22.7654 | 1.12445 | 0.377644 | 1 | 0.5 | 0 |
| EC012 | MVL-Ozkurt | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-Ozkurt | fP_hz | 3 | 0.843107 | 0.388235 | -1.21632 | 2.90253 | 1.76146 | 0.220221 | 0 | 0.25 | 0 |
| pooled | MVL-Ozkurt | fP_hz | 3 | 0.843107 | 0.388235 | -1.21632 | 2.90253 | 1.76146 | 0.220221 | 0 | 0.25 | 0 |
| EC012 | MVL-Ozkurt | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-Ozkurt | ozkurt_mvl | 3 | 0.0369549 | 0.0362652 | 0.0171877 | 0.0567221 | 8.04384 | 0.0151058 | 0 | 0.25 | 0 |
| pooled | MVL-Ozkurt | ozkurt_mvl | 3 | 0.0369549 | 0.0362652 | 0.0171877 | 0.0567221 | 8.04384 | 0.0151058 | 0 | 0.25 | 0 |
| EC012 | MVL-raw | fA_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-raw | fA_hz | 3 | 7.92674 | 7.34884 | 4.81341 | 11.0401 | 10.9548 | 0.00823004 | 0 | 0.25 | 0 |
| pooled | MVL-raw | fA_hz | 3 | 7.92674 | 7.34884 | 4.81341 | 11.0401 | 10.9548 | 0.00823004 | 0 | 0.25 | 0 |
| EC012 | MVL-raw | fP_hz | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-raw | fP_hz | 3 | 0.896458 | 1.00294 | -0.220593 | 2.01351 | 3.45298 | 0.0746065 | 0 | 0.25 | 0 |
| pooled | MVL-raw | fP_hz | 3 | 0.896458 | 1.00294 | -0.220593 | 2.01351 | 3.45298 | 0.0746065 | 0 | 0.25 | 0 |
| EC012 | MVL-raw | ozkurt_mvl | 0 | NA | NA | NA | NA | NA | NA | NA | NA | 0 |
| EC013 | MVL-raw | ozkurt_mvl | 3 | 0.0371942 | 0.0328573 | 0.016371 | 0.0580174 | 7.68535 | 0.0165124 | 0 | 0.25 | 0 |
| pooled | MVL-raw | ozkurt_mvl | 3 | 0.0371942 | 0.0328573 | 0.016371 | 0.0580174 | 7.68535 | 0.0165124 | 0 | 0.25 | 0 |

## Region-specific mixed models

Specified session random intercept and state slope retained throughout, fitted by REML. With only EC013 represented, the constant animal fixed effect is redundant; all fitted formulas are `outcome ~ state_run + (1 + state_run | session)`. This constant-animal handling was recorded before PAC analysis. State is 0=rest, 1=run. The optimizer nonconvergence warning was enabled/captured; its exit code is not a public property in this MATLAB version. Covariance eigenvalues/rank and full fit logs are retained.

| analysis | outcome | Name | Estimate | SE | tStat | DF | pValue | Lower | Upper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | fP_hz | (Intercept) | 7.43555 | 1.1634 | 6.39122 | 108 | 4.28491e-09 | 5.12949 | 9.74162 |
| CA1 | fP_hz | state_run | 0.646746 | 1.19 | 0.543486 | 108 | 0.587916 | -1.71203 | 3.00552 |
| CA1 | ozkurt_mvl | (Intercept) | 0.0420767 | 0.00293231 | 14.3493 | 108 | 8.94765e-27 | 0.0362643 | 0.047889 |
| CA1 | ozkurt_mvl | state_run | 0.0148146 | 0.00596592 | 2.48321 | 108 | 0.0145582 | 0.00298916 | 0.0266401 |
| EC | fP_hz | (Intercept) | 6.27234 | 0.182417 | 34.3847 | 110 | 1.12395e-60 | 5.91083 | 6.63385 |
| EC | fP_hz | state_run | 1.20543 | 0.261901 | 4.60262 | 110 | 1.12481e-05 | 0.686406 | 1.72446 |
| EC | ozkurt_mvl | (Intercept) | 0.0693591 | 0.00382551 | 18.1306 | 110 | 7.90526e-35 | 0.0617778 | 0.0769403 |
| EC | ozkurt_mvl | state_run | 0.0264026 | 0.00685976 | 3.84891 | 110 | 0.000199522 | 0.0128081 | 0.039997 |
| E1_sensitivity | fP_hz | (Intercept) | 6.2926 | 0.134207 | 46.8874 | 109 | 4.38338e-74 | 6.02661 | 6.5586 |
| E1_sensitivity | fP_hz | state_run | 1.20765 | 0.236793 | 5.10001 | 109 | 1.44387e-06 | 0.73833 | 1.67696 |
| E1_sensitivity | ozkurt_mvl | (Intercept) | 0.0671483 | 0.00234447 | 28.6411 | 109 | 1.52647e-52 | 0.0625016 | 0.071795 |
| E1_sensitivity | ozkurt_mvl | state_run | 0.0378455 | 0.007588 | 4.98754 | 109 | 2.32533e-06 | 0.0228063 | 0.0528847 |

| analysis | outcome | sessions | observations | var_intercept | cov_intercept_state | var_state | residual_variance | covariance_rank | optimizer_nonconvergence_warning | warning |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | fP_hz | 3 | 110 | 3.4096 | -1.98315 | 1.15348 | 16.423 | 2 | False | none |
| CA1 | ozkurt_mvl | 3 | 110 | 1.38955e-05 | -2.51392e-05 | 4.5481e-05 | 0.00032426 | 2 | False | none |
| EC | fP_hz | 3 | 112 | 0.0625023 | -0.0309003 | 0.0152767 | 1.02703 | 1 | False | none |
| EC | ozkurt_mvl | 3 | 112 | 2.66493e-05 | 3.58918e-05 | 4.83399e-05 | 0.000500253 | 2 | False | none |
| E1_sensitivity | fP_hz | 3 | 111 | 0.0226761 | -0.00969183 | 0.00414232 | 0.88858 | 1 | False | none |
| E1_sensitivity | ozkurt_mvl | 3 | 111 | 3.71294e-09 | -5.40925e-07 | 7.88053e-05 | 0.000500065 | 2 | False | none |

Model diagnostics: [regional_mixed_models.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_mixed_models.json>); saved models and individual `regional_mixed_*_fit.txt` logs preserve each fit.

## Boundary picks and within-state fP spread

Boundary counts refer to exact fP=4 or 12 Hz. APC uses its frozen default continuous phase search; its estimates can lie outside the scan range. Spread is sample SD, linear-quantile IQR and unscaled median absolute deviation.

| analysis | session | method | state | n_bouts | n_valid | boundary_fp_4 | boundary_fp_12 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | ec013.156 | APC-v1.0 | run | 9 | 9 | 0 | 0 |
| CA1 | ec013.156 | APC-v1.0 | rest | 43 | 43 | 0 | 0 |
| CA1 | ec013.156 | GLM | run | 9 | 9 | 1 | 0 |
| CA1 | ec013.156 | GLM | rest | 43 | 43 | 7 | 0 |
| CA1 | ec013.156 | KLMI | run | 9 | 9 | 5 | 0 |
| CA1 | ec013.156 | KLMI | rest | 43 | 43 | 22 | 0 |
| CA1 | ec013.156 | MVL-Ozkurt | run | 9 | 9 | 3 | 1 |
| CA1 | ec013.156 | MVL-Ozkurt | rest | 43 | 43 | 18 | 1 |
| CA1 | ec013.156 | MVL-raw | run | 9 | 9 | 4 | 1 |
| CA1 | ec013.156 | MVL-raw | rest | 43 | 43 | 19 | 1 |
| CA1 | ec013.157 | APC-v1.0 | run | 6 | 6 | 0 | 0 |
| CA1 | ec013.157 | APC-v1.0 | rest | 15 | 14 | 0 | 0 |
| CA1 | ec013.157 | GLM | run | 6 | 6 | 3 | 0 |
| CA1 | ec013.157 | GLM | rest | 15 | 15 | 3 | 0 |
| CA1 | ec013.157 | KLMI | run | 6 | 6 | 6 | 0 |
| CA1 | ec013.157 | KLMI | rest | 15 | 15 | 6 | 0 |
| CA1 | ec013.157 | MVL-Ozkurt | run | 6 | 6 | 3 | 0 |
| CA1 | ec013.157 | MVL-Ozkurt | rest | 15 | 15 | 6 | 0 |
| CA1 | ec013.157 | MVL-raw | run | 6 | 6 | 2 | 0 |
| CA1 | ec013.157 | MVL-raw | rest | 15 | 15 | 8 | 0 |
| CA1 | ec013.375 | APC-v1.0 | run | 5 | 5 | 0 | 0 |
| CA1 | ec013.375 | APC-v1.0 | rest | 34 | 33 | 0 | 0 |
| CA1 | ec013.375 | GLM | run | 5 | 5 | 1 | 0 |
| CA1 | ec013.375 | GLM | rest | 34 | 34 | 5 | 1 |
| CA1 | ec013.375 | KLMI | run | 5 | 5 | 1 | 0 |
| CA1 | ec013.375 | KLMI | rest | 34 | 34 | 9 | 0 |
| CA1 | ec013.375 | MVL-Ozkurt | run | 5 | 5 | 1 | 0 |
| CA1 | ec013.375 | MVL-Ozkurt | rest | 34 | 34 | 7 | 2 |
| CA1 | ec013.375 | MVL-raw | run | 5 | 5 | 1 | 0 |
| CA1 | ec013.375 | MVL-raw | rest | 34 | 34 | 7 | 2 |
| E1_sensitivity | ec013.156 | APC-v1.0 | run | 9 | 9 | 0 | 0 |
| E1_sensitivity | ec013.156 | APC-v1.0 | rest | 43 | 43 | 0 | 0 |
| E1_sensitivity | ec013.156 | GLM | run | 9 | 9 | 0 | 0 |
| E1_sensitivity | ec013.156 | GLM | rest | 43 | 43 | 2 | 0 |
| E1_sensitivity | ec013.156 | KLMI | run | 9 | 9 | 1 | 0 |
| E1_sensitivity | ec013.156 | KLMI | rest | 43 | 43 | 9 | 0 |
| E1_sensitivity | ec013.156 | MVL-Ozkurt | run | 9 | 9 | 2 | 0 |
| E1_sensitivity | ec013.156 | MVL-Ozkurt | rest | 43 | 43 | 5 | 1 |
| E1_sensitivity | ec013.156 | MVL-raw | run | 9 | 9 | 1 | 0 |
| E1_sensitivity | ec013.156 | MVL-raw | rest | 43 | 43 | 7 | 0 |
| E1_sensitivity | ec013.157 | APC-v1.0 | run | 6 | 6 | 0 | 0 |
| E1_sensitivity | ec013.157 | APC-v1.0 | rest | 15 | 15 | 0 | 0 |
| E1_sensitivity | ec013.157 | GLM | run | 6 | 6 | 0 | 0 |
| E1_sensitivity | ec013.157 | GLM | rest | 15 | 15 | 2 | 0 |
| E1_sensitivity | ec013.157 | KLMI | run | 6 | 6 | 0 | 0 |
| E1_sensitivity | ec013.157 | KLMI | rest | 15 | 15 | 5 | 0 |
| E1_sensitivity | ec013.157 | MVL-Ozkurt | run | 6 | 6 | 0 | 0 |
| E1_sensitivity | ec013.157 | MVL-Ozkurt | rest | 15 | 15 | 3 | 0 |
| E1_sensitivity | ec013.157 | MVL-raw | run | 6 | 6 | 0 | 0 |
| E1_sensitivity | ec013.157 | MVL-raw | rest | 15 | 15 | 3 | 0 |
| E1_sensitivity | ec013.375 | APC-v1.0 | run | 5 | 5 | 0 | 0 |
| E1_sensitivity | ec013.375 | APC-v1.0 | rest | 34 | 33 | 0 | 0 |
| E1_sensitivity | ec013.375 | GLM | run | 5 | 5 | 0 | 0 |
| E1_sensitivity | ec013.375 | GLM | rest | 34 | 34 | 2 | 0 |
| E1_sensitivity | ec013.375 | KLMI | run | 5 | 5 | 0 | 0 |
| E1_sensitivity | ec013.375 | KLMI | rest | 34 | 34 | 7 | 0 |
| E1_sensitivity | ec013.375 | MVL-Ozkurt | run | 5 | 5 | 0 | 0 |
| E1_sensitivity | ec013.375 | MVL-Ozkurt | rest | 34 | 34 | 7 | 0 |
| E1_sensitivity | ec013.375 | MVL-raw | run | 5 | 5 | 0 | 0 |
| E1_sensitivity | ec013.375 | MVL-raw | rest | 34 | 34 | 8 | 0 |
| EC | ec013.156 | APC-v1.0 | run | 9 | 9 | 0 | 0 |
| EC | ec013.156 | APC-v1.0 | rest | 43 | 43 | 0 | 0 |
| EC | ec013.156 | GLM | run | 9 | 9 | 0 | 0 |
| EC | ec013.156 | GLM | rest | 43 | 43 | 2 | 0 |
| EC | ec013.156 | KLMI | run | 9 | 9 | 0 | 0 |
| EC | ec013.156 | KLMI | rest | 43 | 43 | 9 | 0 |
| EC | ec013.156 | MVL-Ozkurt | run | 9 | 9 | 2 | 0 |
| EC | ec013.156 | MVL-Ozkurt | rest | 43 | 43 | 7 | 0 |
| EC | ec013.156 | MVL-raw | run | 9 | 9 | 1 | 0 |
| EC | ec013.156 | MVL-raw | rest | 43 | 43 | 6 | 0 |
| EC | ec013.157 | APC-v1.0 | run | 6 | 6 | 0 | 0 |
| EC | ec013.157 | APC-v1.0 | rest | 15 | 15 | 0 | 0 |
| EC | ec013.157 | GLM | run | 6 | 6 | 0 | 0 |
| EC | ec013.157 | GLM | rest | 15 | 15 | 1 | 0 |
| EC | ec013.157 | KLMI | run | 6 | 6 | 0 | 0 |
| EC | ec013.157 | KLMI | rest | 15 | 15 | 4 | 0 |
| EC | ec013.157 | MVL-Ozkurt | run | 6 | 6 | 1 | 0 |
| EC | ec013.157 | MVL-Ozkurt | rest | 15 | 15 | 3 | 0 |
| EC | ec013.157 | MVL-raw | run | 6 | 6 | 1 | 0 |
| EC | ec013.157 | MVL-raw | rest | 15 | 15 | 3 | 0 |
| EC | ec013.375 | APC-v1.0 | run | 5 | 5 | 0 | 0 |
| EC | ec013.375 | APC-v1.0 | rest | 34 | 34 | 0 | 0 |
| EC | ec013.375 | GLM | run | 5 | 5 | 0 | 0 |
| EC | ec013.375 | GLM | rest | 34 | 34 | 5 | 0 |
| EC | ec013.375 | KLMI | run | 5 | 5 | 0 | 0 |
| EC | ec013.375 | KLMI | rest | 34 | 34 | 11 | 0 |
| EC | ec013.375 | MVL-Ozkurt | run | 5 | 5 | 0 | 0 |
| EC | ec013.375 | MVL-Ozkurt | rest | 34 | 34 | 8 | 0 |
| EC | ec013.375 | MVL-raw | run | 5 | 5 | 0 | 0 |
| EC | ec013.375 | MVL-raw | rest | 34 | 34 | 5 | 0 |

| analysis | session | method | state | n_valid | fp_sd | fp_iqr | fp_mad |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | ec013.156 | APC-v1.0 | run | 9 | 0.197276 | 0.186967 | 0.112351 |
| CA1 | ec013.156 | APC-v1.0 | rest | 43 | 0.508276 | 0.43347 | 0.221928 |
| CA1 | ec013.156 | GLM | run | 9 | 2.54951 | 4 | 2.5 |
| CA1 | ec013.156 | GLM | rest | 43 | 2.27917 | 3.5 | 2 |
| CA1 | ec013.156 | KLMI | run | 9 | 0.546453 | 0.5 | 0 |
| CA1 | ec013.156 | KLMI | rest | 43 | 1.23611 | 0.75 | 0 |
| CA1 | ec013.156 | MVL-Ozkurt | run | 9 | 3.04936 | 4 | 1 |
| CA1 | ec013.156 | MVL-Ozkurt | rest | 43 | 2.51799 | 3.75 | 0.5 |
| CA1 | ec013.156 | MVL-raw | run | 9 | 2.70416 | 1.5 | 0.5 |
| CA1 | ec013.156 | MVL-raw | rest | 43 | 2.14313 | 2.25 | 0.5 |
| CA1 | ec013.157 | APC-v1.0 | run | 6 | 0.29565 | 0.25042 | 0.156078 |
| CA1 | ec013.157 | APC-v1.0 | rest | 14 | 0.523427 | 0.504488 | 0.264518 |
| CA1 | ec013.157 | GLM | run | 6 | 2.93967 | 4.75 | 2 |
| CA1 | ec013.157 | GLM | rest | 15 | 2.28087 | 3.5 | 1.5 |
| CA1 | ec013.157 | KLMI | run | 6 | 0 | 0 | 0 |
| CA1 | ec013.157 | KLMI | rest | 15 | 1.63518 | 2.5 | 0.5 |
| CA1 | ec013.157 | MVL-Ozkurt | run | 6 | 0.491596 | 0.875 | 0.25 |
| CA1 | ec013.157 | MVL-Ozkurt | rest | 15 | 1.76136 | 2.5 | 0.5 |
| CA1 | ec013.157 | MVL-raw | run | 6 | 2.28947 | 0.875 | 0.5 |
| CA1 | ec013.157 | MVL-raw | rest | 15 | 2.60814 | 2.75 | 0 |
| CA1 | ec013.375 | APC-v1.0 | run | 5 | 3.4139 | 2.73094 | 0.642463 |
| CA1 | ec013.375 | APC-v1.0 | rest | 33 | 7.245 | 8.75316 | 3.83369 |
| CA1 | ec013.375 | GLM | run | 5 | 2.13307 | 0.5 | 0.5 |
| CA1 | ec013.375 | GLM | rest | 34 | 2.50156 | 4.25 | 2 |
| CA1 | ec013.375 | KLMI | run | 5 | 1.14018 | 1 | 1 |
| CA1 | ec013.375 | KLMI | rest | 34 | 1.29994 | 1.375 | 0.5 |
| CA1 | ec013.375 | MVL-Ozkurt | run | 5 | 2.53476 | 2.5 | 1.5 |
| CA1 | ec013.375 | MVL-Ozkurt | rest | 34 | 2.26699 | 1.875 | 0.5 |
| CA1 | ec013.375 | MVL-raw | run | 5 | 2.62202 | 3 | 1.5 |
| CA1 | ec013.375 | MVL-raw | rest | 34 | 2.27597 | 1.875 | 0.5 |
| E1_sensitivity | ec013.156 | APC-v1.0 | run | 9 | 0.169398 | 0.22929 | 0.147225 |
| E1_sensitivity | ec013.156 | APC-v1.0 | rest | 43 | 0.26947 | 0.302149 | 0.109914 |
| E1_sensitivity | ec013.156 | GLM | run | 9 | 1.1577 | 2 | 0.5 |
| E1_sensitivity | ec013.156 | GLM | rest | 43 | 1.20204 | 1.75 | 1 |
| E1_sensitivity | ec013.156 | KLMI | run | 9 | 1.57012 | 1 | 0.5 |
| E1_sensitivity | ec013.156 | KLMI | rest | 43 | 1.06658 | 1.5 | 1 |
| E1_sensitivity | ec013.156 | MVL-Ozkurt | run | 9 | 1.75 | 2.5 | 1.5 |
| E1_sensitivity | ec013.156 | MVL-Ozkurt | rest | 43 | 1.70742 | 2.5 | 1 |
| E1_sensitivity | ec013.156 | MVL-raw | run | 9 | 1.36931 | 1 | 0.5 |
| E1_sensitivity | ec013.156 | MVL-raw | rest | 43 | 1.59829 | 2.5 | 1.5 |
| E1_sensitivity | ec013.157 | APC-v1.0 | run | 6 | 0.225829 | 0.211333 | 0.118104 |
| E1_sensitivity | ec013.157 | APC-v1.0 | rest | 15 | 0.474379 | 0.262424 | 0.142005 |
| E1_sensitivity | ec013.157 | GLM | run | 6 | 0.894427 | 0.875 | 0.5 |
| E1_sensitivity | ec013.157 | GLM | rest | 15 | 1.34253 | 2.5 | 1 |
| E1_sensitivity | ec013.157 | KLMI | run | 6 | 0.408248 | 0.5 | 0.25 |
| E1_sensitivity | ec013.157 | KLMI | rest | 15 | 1.21694 | 2.25 | 1.5 |
| E1_sensitivity | ec013.157 | MVL-Ozkurt | run | 6 | 1.43759 | 2.125 | 1 |
| E1_sensitivity | ec013.157 | MVL-Ozkurt | rest | 15 | 1.35576 | 2 | 1 |
| E1_sensitivity | ec013.157 | MVL-raw | run | 6 | 1.36931 | 1.875 | 0.25 |
| E1_sensitivity | ec013.157 | MVL-raw | rest | 15 | 1.55226 | 2.25 | 1 |
| E1_sensitivity | ec013.375 | APC-v1.0 | run | 5 | 0.287066 | 0.365328 | 0.223771 |
| E1_sensitivity | ec013.375 | APC-v1.0 | rest | 33 | 1.65998 | 0.735075 | 0.385891 |
| E1_sensitivity | ec013.375 | GLM | run | 5 | 1.29422 | 2 | 1 |
| E1_sensitivity | ec013.375 | GLM | rest | 34 | 1.30379 | 1.5 | 1 |
| E1_sensitivity | ec013.375 | KLMI | run | 5 | 1.35093 | 1 | 0.5 |
| E1_sensitivity | ec013.375 | KLMI | rest | 34 | 1.47325 | 2.5 | 1.5 |
| E1_sensitivity | ec013.375 | MVL-Ozkurt | run | 5 | 1.35093 | 1 | 0.5 |
| E1_sensitivity | ec013.375 | MVL-Ozkurt | rest | 34 | 1.60714 | 2.5 | 1.5 |
| E1_sensitivity | ec013.375 | MVL-raw | run | 5 | 1.78185 | 3 | 1.5 |
| E1_sensitivity | ec013.375 | MVL-raw | rest | 34 | 1.72231 | 2.5 | 1.5 |
| EC | ec013.156 | APC-v1.0 | run | 9 | 0.159543 | 0.29712 | 0.137274 |
| EC | ec013.156 | APC-v1.0 | rest | 43 | 0.283631 | 0.332426 | 0.165774 |
| EC | ec013.156 | GLM | run | 9 | 1.22474 | 2 | 1 |
| EC | ec013.156 | GLM | rest | 43 | 1.60296 | 2.25 | 1 |
| EC | ec013.156 | KLMI | run | 9 | 1.25 | 2 | 1 |
| EC | ec013.156 | KLMI | rest | 43 | 1.42426 | 1.75 | 1 |
| EC | ec013.156 | MVL-Ozkurt | run | 9 | 1.80278 | 0.5 | 0.5 |
| EC | ec013.156 | MVL-Ozkurt | rest | 43 | 1.5668 | 2.75 | 1.5 |
| EC | ec013.156 | MVL-raw | run | 9 | 1.62874 | 2 | 1 |
| EC | ec013.156 | MVL-raw | rest | 43 | 1.55812 | 2.5 | 1.5 |
| EC | ec013.157 | APC-v1.0 | run | 6 | 0.193332 | 0.138557 | 0.0805116 |
| EC | ec013.157 | APC-v1.0 | rest | 15 | 0.459571 | 0.192263 | 0.146141 |
| EC | ec013.157 | GLM | run | 6 | 1.2145 | 1.25 | 0.75 |
| EC | ec013.157 | GLM | rest | 15 | 1.25167 | 2 | 1 |
| EC | ec013.157 | KLMI | run | 6 | 0.935414 | 0.75 | 0.5 |
| EC | ec013.157 | KLMI | rest | 15 | 1.10195 | 1.75 | 1 |
| EC | ec013.157 | MVL-Ozkurt | run | 6 | 1.8619 | 2.25 | 1.5 |
| EC | ec013.157 | MVL-Ozkurt | rest | 15 | 1.08012 | 1.5 | 1 |
| EC | ec013.157 | MVL-raw | run | 6 | 1.72482 | 1.625 | 1 |
| EC | ec013.157 | MVL-raw | rest | 15 | 1.32557 | 1.75 | 1 |
| EC | ec013.375 | APC-v1.0 | run | 5 | 0.277828 | 0.373787 | 0.190778 |
| EC | ec013.375 | APC-v1.0 | rest | 34 | 1.77481 | 1.01135 | 0.508764 |
| EC | ec013.375 | GLM | run | 5 | 1.29422 | 2 | 1 |
| EC | ec013.375 | GLM | rest | 34 | 1.66388 | 2.5 | 1.25 |
| EC | ec013.375 | KLMI | run | 5 | 1.35093 | 1 | 0.5 |
| EC | ec013.375 | KLMI | rest | 34 | 1.27929 | 2.375 | 1 |
| EC | ec013.375 | MVL-Ozkurt | run | 5 | 1.34164 | 1 | 1 |
| EC | ec013.375 | MVL-Ozkurt | rest | 34 | 1.56129 | 2.5 | 1.5 |
| EC | ec013.375 | MVL-raw | run | 5 | 1.38744 | 0.5 | 0.5 |
| EC | ec013.375 | MVL-raw | rest | 34 | 1.48762 | 2.375 | 1 |

Paired session APC-minus-scan spread values: [regional_within_state_spread_comparisons.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_within_state_spread_comparisons.csv>). Across-session spread summaries/tests for every scan, state, region and animal pool: [regional_across_session_spread_comparisons.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_across_session_spread_comparisons.csv>).

## Figures

Every figure is exported as 300-dpi PNG and SVG, with commit and source CSV(s) printed and source hashes embedded. The displayed comparison scan is the prespecified Ozkurt-max scan; all four scan metrics remain in the tables.

- Regional theta/delta maxima; filled squares meet >=5 run and >=5 rest eligibility: [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_channel_selection.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_channel_selection.svg>).
- Tracking-rate scale, missingness and counts under the revised rules: [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_behavior_summary.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_behavior_summary.svg>).
- Whole-recording tracking trace; blue run, orange rest; PCA center-zone shading: [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_tracking_ec013_157.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_tracking_ec013_157.svg>).
- Per-bout scatter and state means with 10,000-resample percentile 95% CIs: [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_CA1_run_rest.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_CA1_run_rest.svg>).
- Session mean run-minus-rest effects; 10,000-resample percentile CIs: [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_CA1_session_differences.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_CA1_session_differences.svg>).
- Per-bout scatter and state means with 10,000-resample percentile 95% CIs: [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_EC_run_rest.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_EC_run_rest.svg>).
- Session mean run-minus-rest effects; 10,000-resample percentile CIs: [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_EC_session_differences.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_EC_session_differences.svg>).
- Per-bout scatter and state means with 10,000-resample percentile 95% CIs: [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_E1_sensitivity_run_rest.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_E1_sensitivity_run_rest.svg>).
- Session mean run-minus-rest effects; 10,000-resample percentile CIs: [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_E1_sensitivity_session_differences.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_E1_sensitivity_session_differences.svg>).
- Within-state sample SDs of APC and all four scans, per included session: [PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_within_state_fp_spread.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_within_state_fp_spread.svg>).

## Runtime, deviations and limits

Tracking-rate behaviour: 4.583 s. Successful PAC/comparator runner: 288.447 s. Statistics: 1.288 s. Mixed models: 9.460 s. MATLAB startup and failed tooling launches are excluded from these stage timings.

Three sessions from one animal qualify; no between-animal coefficient or EC012 session-level test is estimable. Source anatomical mapping for EC013 is the explicitly requested assumption. All source channel flags remain visible in the selection table. The historical speed/chunk results are superseded and not used in regional inference.

- tooling syntax correction: First MATLAB runner launch failed to parse multi-line struct calls because continuation ellipses were missing. Added ellipses in new runner and unrun mixed-model reporting script. No bout was analyzed before the parser error; method code and settings unchanged. Original log regional_bouts_matlab.log retained.
- tooling CSV import correction: Second runner launch could not find included after automatic CSV import detection. Fixed comma delimiter, first-row headers, UTF-8, preserved variable names and explicit boolean interpretation. No bout analyzed before failure; original attempt2 log retained.
- tooling MATLAB current-folder precedence: Third launch resolved the legacy one-output bst_apc in the process current folder ahead of addpath entries; call rejected with too many outputs before any method computation. Set analysis folder as current directory, clear function cache, and assert both method and metric resolve to frozen_v1 copies. No tagged source edited; no bout result existed before fix.
- Existing MATLAB startup warnings refer to old missing Brainstorm directories; no installation change was made.
- Source path recovery for ec013.157 is the previously verified local equivalent, documented above. No input or tagged method file was modified.
- Constant-animal mixed-model handling and tracking endpoint/quantile conventions are recorded in the execution amendment; the random-effects structure was retained.

Full current provenance: [regional_analysis_provenance.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/regional_analysis_provenance.json>). Current status: [STATUS.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/STATUS.json>). Output manifest: [output_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/output_manifest.json>).

## POST HOC sensitivity — 2-s minimum bout duration

**POST HOC analysis; separate from all prespecified 5-s results above.** Only minimum bout duration changes from 5 s to 2 s; inclusion remains >=5 run/>=5 rest bouts. All tracking, channel, frozen APC, SOS comparator and statistical rules remain identical.

POST HOC: all 18 sessions qualify (CA1 9 EC013; EC 18 including both animals; E1 sensitivity 9 EC013), compared with 3 EC013 sessions in each prespecified 5-s analysis. Shared >=5-s method outputs reproduce all 1,680 original rows exactly. Pooled comparisons below have different eligible-session sets.

POST HOC inclusion comparison table:
| animal | session | run_bouts_prespecified_5s | rest_bouts_prespecified_5s | run_bouts_posthoc_2s | rest_bouts_posthoc_2s | included_posthoc_2s |
| --- | --- | --- | --- | --- | --- | --- |
| EC013 | ec013.156 | 9 | 43 | 56 | 56 | True |
| EC013 | ec013.157 | 6 | 15 | 23 | 33 | True |
| EC013 | ec013.205 | 0 | 4 | 8 | 9 | True |
| EC013 | ec013.206 | 3 | 21 | 58 | 61 | True |
| EC013 | ec013.208 | 0 | 10 | 44 | 53 | True |
| EC013 | ec013.251 | 0 | 12 | 54 | 65 | True |
| EC013 | ec013.252 | 1 | 9 | 32 | 64 | True |
| EC013 | ec013.374 | 4 | 8 | 88 | 77 | True |
| EC013 | ec013.375 | 5 | 34 | 68 | 137 | True |
| EC012 | ec012ec.239 | 0 | 0 | 47 | 34 | True |
| EC012 | ec012ec.240 | 0 | 1 | 66 | 17 | True |
| EC012 | ec012ec.269 | 0 | 1 | 38 | 48 | True |
| EC012 | ec012ec.270 | 0 | 1 | 24 | 49 | True |
| EC012 | ec012ec.271 | 0 | 2 | 35 | 21 | True |
| EC012 | ec012ec.356 | 0 | 5 | 40 | 50 | True |
| EC012 | ec012ec.357 | 0 | 1 | 38 | 36 | True |
| EC012 | ec012ec.375 | 0 | 6 | 37 | 32 | True |
| EC012 | ec012ec.444 | 0 | 1 | 30 | 46 | True |

POST HOC session-level APC comparison table:
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

The separate [POST HOC report](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/RESULTS_posthoc_2s.md>) contains all POST HOC tables, statuses, mixed models, comparisons, historical overlap, runtime and deviations. Separate POST HOC CSVs: [posthoc_2s_bout_estimates.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_bout_estimates.csv>), [posthoc_2s_session_statistics.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_session_statistics.csv>), [posthoc_2s_across_session_statistics.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_across_session_statistics.csv>), [posthoc_2s_mixed_model_comparison.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_mixed_model_comparison.csv>).

POST HOC figures (additional per-session figures and spread figures are listed in the separate POST HOC report):

- POST HOC: 5-s and POST HOC 2-s bout counts; inclusion remains >=5 run and >=5 rest bouts: [POST HOC PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_inclusion_comparison.png>); [POST HOC SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_inclusion_comparison.svg>).
- POST HOC: Pooled APC effects beside prespecified 5-s results; different eligible-session sets: [POST HOC PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_across_session_comparison.png>); [POST HOC SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/posthoc_2s/posthoc_2s_across_session_comparison.svg>).
