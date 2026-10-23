# Multi-session rodent analysis — preflight results

**Status: channel selection and prerequisite checks complete; new bout analyses pending the time-interval decision.** No new-session APC/comparator outcomes, per-session eligibility decisions, inferential tests or mixed models have been computed. This is a preflight report, not completed replication results.

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

## Inclusion, statistics and remaining interval choice

All sessions are pending the prespecified ≥5 run/≥5 rest bout gate; none is excluded based on a PAC result. Whole-recording channel selection is complete for both animals. EC013 E1 is prespecified as the sensitivity channel.

The historical bout producer analyzes indices 40800:372501 (about 32.64–298 s). The user was asked whether multi-session bouts should use that interval or whole recordings. The unchanged trenddecomp code defaults to a 5000-sample SSA lag and explicitly builds a dense Hankel matrix. Full-recording estimates: [behavior_memory_estimates.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/behavior_memory_estimates.csv>). The largest dense matrix alone is 87.659 GB; the host has about 32 GB RAM. No decomposition shortcut, fallback substitution or crop has been applied to new-session bout analysis.

After the interval choice: apply the historical speed computation, count/include bouts, run frozen APC and guarded SOS scans, produce per-session bootstrap/Welch/Hedges results, across-session t/Wilcoxon tests, the specified random-intercept/random-slope models, and within-state spreads. The plotted scan choice is fixed as the Ozkurt-max scan independently of run/rest effects.

## Figures

- Channel-selection summary: [300-dpi PNG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/channel_selection_summary.png>); [SVG](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/channel_selection_summary.svg>). Commit, protocol and source CSV hashes embedded.

Run/rest and session-difference figures await bout analysis.

## Runtime and deviations

Historical reproduction MATLAB time: 149.755 s. Channel selection MATLAB time: 122.063 s. Read-only inventory: 2.5081377000024077 s. Startup and packaging time excluded.

Deviations and pending choice: [deviations.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/deviations.json>). Full inventory: [inventory.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/inventory.json>). Current status: [STATUS.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/STATUS.json>). Output manifest: [output_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/rodent_multi/output_manifest.json>).
