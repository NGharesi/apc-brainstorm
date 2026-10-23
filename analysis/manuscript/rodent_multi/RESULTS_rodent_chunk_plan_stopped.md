# Multi-session rodent analysis — stopped at behaviour gate

**Status: STOPPED. The specified >=95% ec013.157 label-agreement gate cannot pass: its maximum possible full-interval agreement is 89.687098%.** This is a conclusive failure bound from partial coverage, not a completed full-interval percentage. No new APC/comparator estimates or other sessions' bout analyses were run.

The user plan was saved verbatim before any new-session analysis: [PROTOCOL_rodent.md](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/PROTOCOL_rodent.md>). Execution choices fixed before channel selection: [EXECUTION_rodent.md](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/EXECUTION_rodent.md>). Frozen APC tag `v1.0`, commit `71ebc16aed32ca38be73a800738b975e5806b330`; no tagged code changed.

## Session-to-tracking mapping

Ratio = (tracking samples / 39.0625) / (LFP samples / measured fs). All 18 pairs pass the 5% gate. The original ec013.157 path is missing, but a verified equivalent full multichannel source was recovered locally. Mapping CSV: [mapping_checks.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/mapping_checks.csv>). Original missing-path inventory is retained separately.

| animal | session | tracking_array | tracking_samples | lfp_samples | lfp_channels | lfp_fs_hz | lfp_duration_s | tracking_to_lfp_duration_ratio | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EC013 | ec013.156 | ec013ec1 | 39985 | 1279488 | 65 | 1250 | 1023.5904 | 1.000025 | PASS |
| EC013 | ec013.157 | ec013ec2 | 24657 | 789000 | 65 | 1250 | 631.2 | 1.0000304 | PASS_RECOVERED_EQUIVALENT_FULL_RECORDING |
| EC013 | ec013.205 | ec013ec3 | 7329 | 234496 | 65 | 1250 | 187.5968 | 1.0001365 | PASS |
| EC013 | ec013.206 | ec013ec4 | 34157 | 1093000 | 65 | 1250 | 874.4 | 1.000022 | PASS |
| EC013 | ec013.208 | ec013ec5 | 30401 | 972800 | 65 | 1250 | 778.24 | 1.0000329 | PASS |
| EC013 | ec013.251 | ec013ec6 | 37797 | 1209500 | 65 | 1250 | 967.6 | 1.0000033 | PASS |
| EC013 | ec013.252 | ec013ec7 | 37617 | 1203712 | 65 | 1250 | 962.9696 | 1.0000266 | PASS |
| EC013 | ec013.374 | ec013ec8 | 42049 | 1345536 | 65 | 1250 | 1076.4288 | 1.0000238 | PASS |
| EC013 | ec013.375 | ec013ec9 | 68641 | 2196480 | 65 | 1250 | 1757.184 | 1.0000146 | PASS |
| EC012 | ec012ec.239 | ec012ec1 | 18426 | 589625 | 33 | 1250 | 471.7 | 1.0000119 | PASS |
| EC012 | ec012ec.240 | ec012ec2 | 24903 | 796875 | 33 | 1250 | 637.5 | 1.0000264 | PASS |
| EC012 | ec012ec.269 | ec012ec3 | 19821 | 634250 | 33 | 1250 | 507.4 | 1.0000347 | PASS |
| EC012 | ec012ec.270 | ec012ec4 | 16407 | 525000 | 33 | 1250 | 420 | 1.0000457 | PASS |
| EC012 | ec012ec.271 | ec012ec5 | 15751 | 504000 | 33 | 1250 | 403.2 | 1.0000635 | PASS |
| EC012 | ec012ec.356 | ec012ec6 | 18247 | 583875 | 33 | 1250 | 467.1 | 1.0000497 | PASS |
| EC012 | ec012ec.357 | ec012ec7 | 22083 | 706625 | 33 | 1250 | 565.3 | 1.0000439 | PASS |
| EC012 | ec012ec.375 | ec012ec8 | 24657 | 789000 | 33 | 1250 | 631.2 | 1.0000304 | PASS |
| EC012 | ec012ec.444 | ec012ec9 | 16356 | 523375 | 33 | 1250 | 418.7 | 1.0000325 | PASS |

Reference source recovery: [ec013_157_source_recovery.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/ec013_157_source_recovery.json>). The test variable in `D:/APC_project/2025/Results_Behavior/behavior_inter.mat` has 65×789000 samples; its entire E1/Time match R2 exactly and all 65 channels at samples 40800:372501 match the existing multichannel crop exactly.

## Exact historical behaviour reproduction

Original script found: `D:/APC_project/2025/Results_Behavior/behavior.m`. The 5-s bout producer is [run_apc_ec013_run_rest.m](<C:/Users/nghare/.brainstorm/process/run_apc_ec013_run_rest.m>). The reproduction uses ec013ec2, LED timestamps at 39.06 Hz, original R2 indices 40800:372501, trenddecomp of interpolated x1, derivative divided by elapsed seconds, abs(speed)>6, contiguous bouts ≥5 s.

**PASS: 12 run and 12 rest bouts.** Both bout tables (indices, timestamps, durations), both masks and the entire speed vector match exactly. Maximum speed and trend differences = 0. Smoothing route: trenddecomp. Evidence: [behavior_reproduction.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/behavior_reproduction.json>); [behavior_reproduction.mat](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/behavior_reproduction.mat>).

Computational speed units are raw x1 tracking-coordinate units per second. The original plot labels position as cm, but neither script applies a coordinate calibration. Physical cm/s is therefore not independently verified. The producer does not remove −1 sentinels, average LEDs or compute 2-D displacement. Literal reproduction retains these behaviours. Missing-coordinate counts: [tracking_missing_counts.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/tracking_missing_counts.csv>).

## Prespecified whole-recording channel selection

All imported channels are ranked on the entire recording, with no state or PAC-outcome selection. Per-channel mean removal; Welch with symmetric Hann round(4*fs), 50% overlap, NFFT next power of two; integrate one-sided PSD at exact band endpoints by interpolation/trapezoids. First index breaks ties. Undefined ratios are recorded. Every channel, power and source flag: [channel_ratios.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/channel_ratios.csv>). Choices: [selected_channels.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/selected_channels.csv>).

| animal | session | channel_index | channel_name | theta_delta_ratio | region | shank |
| --- | --- | --- | --- | --- | --- | --- |
| EC013 | ec013.156 | 8 | E8 | 5.8829786 | unverified | unverified |
| EC013 | ec013.157 | 8 | E8 | 5.7364787 | unverified | unverified |
| EC013 | ec013.205 | 2 | E2 | 9.8911489 | unverified | unverified |
| EC013 | ec013.206 | 2 | E2 | 5.2574101 | unverified | unverified |
| EC013 | ec013.208 | 62 | E62 | 1.1205776 | unverified | unverified |
| EC013 | ec013.251 | 2 | E2 | 2.8327736 | unverified | unverified |
| EC013 | ec013.252 | 2 | E2 | 2.9060818 | unverified | unverified |
| EC013 | ec013.374 | 8 | E8 | 3.2425154 | unverified | unverified |
| EC013 | ec013.375 | 8 | E8 | 1.3805202 | unverified | unverified |
| EC012 | ec012ec.239 | 5 | E5 | 7.1781834 | unverified | unverified |
| EC012 | ec012ec.240 | 3 | E3 | 7.6786172 | unverified | unverified |
| EC012 | ec012ec.269 | 5 | E5 | 4.8076386 | unverified | unverified |
| EC012 | ec012ec.270 | 12 | E12 | 5.9081941 | unverified | unverified |
| EC012 | ec012ec.271 | 10 | E10 | 7.1664582 | unverified | unverified |
| EC012 | ec012ec.356 | 6 | E6 | 5.9663253 | unverified | unverified |
| EC012 | ec012ec.357 | 9 | E9 | 7.3776805 | unverified | unverified |
| EC012 | ec012ec.375 | 6 | E6 | 7.3987425 | unverified | unverified |
| EC012 | ec012ec.444 | 6 | E6 | 7.5506481 | unverified | unverified |

## Channel metadata evidence

No hc-3 channel/shank/region metadata table or session XML was found under `D:/APC_project/RealDatasets`; the file inventory includes unrelated OpenNeuro metadata. Regions and shanks remain **unverified** in the primary channel table.

Additional files found outside that root: `D:/APC_project/Previous_Computer/RealData/tPACPaper/ElePosition.txt`, `hc3-session.csv`, and `ec012ec.14/ec012ec.269/ec012ec.269.xml`. The XML defines anatomical channel groups but does not give region names; the text table contains session-group region entries. A validated channel-to-shank-to-region join has not been established here, so no anatomical label was inferred from channel index alone.

## Whole-recording amendments and conclusive validation failure

Both user amendments were added before the chunked analysis: whole recordings, missing -1 positions, bounded <=0.5-s interpolation, long-gap bout splitting, 2-s recording edge exclusion, exactly 331,702-sample chunks, 20-s overlap, 10-s internal edge rejection, final chunk ending at the trimmed recording end, and the >=95% label-agreement gate. Evidence: [protocol_amendments_record.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/protocol_amendments_record.json>). The unchanged original plan is retained in [PROTOCOL_rodent_original.md](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/PROTOCOL_rodent_original.md>) (SHA-256 `66f917261c42c1294d3744d61a76626d06d599e3a9d2151faef1951bfe707113`). Amended protocol SHA-256: `17738c5b8e9d360048d3e104f7da6ee83e65889fe159d6951c61bd8755e8e80f`.

Chunk 1 completed using trenddecomp with no fallback. Its owned speed samples cover global indices 2501:321702. Inside the historical comparison interval, **all 280,903 computed samples have valid new labels**; missing/unlabelled samples do not account for their disagreements. Speed units and threshold remain the original raw x1 units/s and abs(speed)>6.

| Label comparison measure | Result |
| --- | --- |
| Full historical derivative interval | 40800:372500; 331,701 samples |
| Computed historical prefix | 40800:321702; 280,903 samples |
| Prefix agreeing / disagreeing samples | 246,695 / 34,208 |
| Prefix agreement | 87.822131% |
| Uncomputed reference samples | 50,798 |
| Full-interval agreement lower / upper bounds | 74.372703% / 89.687098% |
| Required agreement | >=95% |
| Full-interval exact agreement | Not computed after conclusive failure |

Proof: the 34,208 known disagreements already occupy 10.312902% of the full reference interval. Assigning agreement to every remaining sample yields at most 89.687098%, below 95%. The second chunk was stopped immediately after this proof; the third was not run. This preserves the specified acceptance criterion. The computation was terminated early rather than estimating a percentage from incomplete data.

Per-bout endpoint checks are reported only when both endpoints plus the 0.5-s tolerance are covered. Full 12-bout recovery counts remain unresolved where endpoints are uncomputed:

| State | Historical bouts fully covered | Matched among covered | Unresolved | Full 12-bout matched-count bounds |
| --- | --- | --- | --- | --- |
| run | 10/12 | 0 | 2 | 0–2 /12 |
| rest | 10/12 | 0 | 2 | 0–2 /12 |

Exact rows: [ec013_157_bout_validation.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/ec013_157_bout_validation.csv>); known-prefix bouts with right-censor flags: [ec013_157_known_prefix_bouts.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/ec013_157_known_prefix_bouts.csv>). Contiguous disagreements: [ec013_157_label_disagreements.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/ec013_157_label_disagreements.csv>). All computed labels: [ec013_157_partial_label_comparison.mat](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/ec013_157_partial_label_comparison.mat>). Saved speed and position: [ec013.157_speed_chunk_01.mat](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/ec013.157_speed_chunk_01.mat>). Validation facts and provenance: [chunked_behavior_validation.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/chunked_behavior_validation.json>).

Historical handling retains -1 and still reproduces **12 run /12 rest exactly**, unchanged. For the whole ec013.157 tracking array, 1,361/24,657 x1 samples are missing (5.519731%). Full-recording numbers of bouts lost to gaps were not computed after the gate failure.

## Inclusion and analyses not run

All 18 mapping checks and channel selections remain complete. No session has been assigned final >=5/5 bout eligibility after this failed prerequisite. The other 17 sessions' chunked behaviour, original-interval PAC sensitivity, E1 sensitivity, per-bout APC/A2' scans, per-session and across-session statistics, mixed models, within-state spreads, and run/rest effect figures were not run. Prepared runner scripts were not executed beyond the reference validation. No method, threshold, chunk length or missing-data rule was changed after observing this failure.

## Figures

- Channel-selection summary: [300-dpi PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/channel_selection_summary.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/channel_selection_summary.svg>). Commit, protocol and source CSV hashes embedded.

Reference-label failure diagnostic: [300-dpi PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/ec013_157_label_validation.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/ec013_157_label_validation.svg>). Commit and source CSV are embedded. Grey shading denotes uncomputed labels. The earlier channel-selection figure preserves its pre-amendment provenance and preflight-status footer; no run/rest effect figures were generated.

## Runtime and deviations

Historical reproduction MATLAB time: 149.755 s. Channel selection MATLAB time: 122.063 s. Read-only inventory: 2.5081377000024077 s. Startup and packaging time excluded.

Deviations: [deviations.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/deviations.json>). Full inventory: [inventory.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/inventory.json>). Current status: [STATUS.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/STATUS.json>). Output manifest: [output_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/output_manifest.json>).

Completed chunk runtime: 1768.587 s (29.477 min), excluding MATLAB startup and the interrupted second chunk. Peak observed MATLAB private allocation: 42.451 GB; peak sampled resident working set: 16.501 GB. The 32-GB host paged heavily. Resource observations: [validation_resource_monitor.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/validation_resource_monitor.csv>); console log: [chunked_validation_matlab.log](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/chunked_validation_matlab.log>). Exit 1 reflects intentional termination after the conclusive gate failure, not an additional method exception.
