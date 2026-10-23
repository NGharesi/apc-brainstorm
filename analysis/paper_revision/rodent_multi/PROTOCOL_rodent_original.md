GOAL: Replicate the run-vs-rest rodent analysis across all locally available hc-3 sessions with tracking, using the frozen APC v1.0 (tag v1.0) and the SOS-corrected A2' comparators. Do not modify tagged code. Outputs go to revision_checks/rodent_multi/. Write PROTOCOL_rodent.md (this plan, verbatim) BEFORE analysing any new session. Fix and log tooling errors; stop on anything method-relevant.

DATA (D:\APC_project\RealDatasets\LFP_data):
- EC013: HC3/data/EC013/ec013.{156,157,205,206,208,251,252,374,375}.eeg/data_block001.mat (65 channels, 1250 Hz). Tracking: Behavioral_Data/EC013_movement.mat, arrays ec013ec1..ec013ec9 in that session order.
- EC012: HC3/data/EC012/ec012ec.{239,240,269,270,271,356,357,375,444}.eeg/data_block001.mat (33 channels). Tracking: Behavioral_Data/EC012_movement.mat, arrays ec012ec1..9 in that order.
- Tracking columns are x1, y1, x2, y2 (two LEDs, about 39.06 Hz); -1 means missing.
- Verify the session-to-tracking mapping by duration (tracking samples / 39.0625 vs LFP samples / fs; report the ratio for each session) and stop if any pair disagrees by more than 5%.
- If hc-3 metadata tables (session/shank/region) are present anywhere under RealDatasets, use them to label each analysed channel's shank and region. Otherwise record the region as "unverified".

BEHAVIOUR: find the original behavior.m (or the script that produced apc_ec013_run_rest_results.mat) and reuse its exact speed computation, units, threshold and 5-s minimum bout duration. First check that it reproduces the existing 12 run / 12 rest bouts of ec013.157 exactly. Report the speed units. A session is included only if it has >= 5 run and >= 5 rest bouts.

CHANNEL (prespecified): in each session, pick the channel with the highest theta(6–10 Hz)/delta(1–4 Hz) Welch power ratio over the whole recording (both states pooled). Report the chosen channel per session. Sensitivity analysis: EC013 channel E1 in every session.

ANALYSIS PER BOUT: APC v1.0 (ampRange 80–150 Hz; defaults otherwise) giving fP, fA, raw and Ozkurt-normalized MVL, and the preferred phase; plus A2' SOS scans (MVL-raw, MVL-Ozkurt, KLMI, GLM; phase grid 4:0.5:12 with half-width 1.5; amplitude grid 80:4:148 with half-width 12), giving fP, fA, Ozkurt MVL and boundary picks.

STATISTICS:
(a) Per session: run - rest mean differences for fP, fA and Ozkurt MVL, with Welch t, Hedges g and bootstrap 95% CI, for each method.
(b) Across sessions, the primary result: session-level mean differences; one-sample t test and Wilcoxon signed-rank test across sessions, separately for each animal and pooled.
(c) Mixed model: outcome ~ state + animal + (1 + state | session), on bout-level data, for APC fP and Ozkurt MVL.
(d) Within-state fP spread for APC versus the scans.

FIGURES: per-session run/rest fP and Ozkurt MVL (APC and the best scan), the session-level differences with CIs, and a channel-selection summary. 300-dpi PNG and SVG, with provenance embedded.

OUTPUT: revision_checks/rodent_multi/RESULTS_rodent.md containing: mapping checks, behaviour reproduction check, included and excluded sessions with reasons, chosen channels and regions, all tables, figure paths, and deviations.
