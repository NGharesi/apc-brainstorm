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


USER AMENDMENTS: whole-recording interval and missing tracking

Use option 1: the whole recording in every session (including ec013.157), with the original x1-only speed formula, units and threshold, and the 5-s minimum bout duration. The 12/12 reproduction on the original interval remains the code check; also report ec013.157 on the original interval as a sensitivity result.

Missing tracking (-1), to be added to PROTOCOL_rodent.md before running: treat -1 samples as missing, not as positions. Linearly interpolate gaps of <= 0.5 s. A bout may not contain a gap longer than 0.5 s; split it at the gap and apply the 5-s minimum to each piece. Also exclude the first and last 2 s of each recording. For each session, report the fraction of samples that were missing and the number of bouts lost to gaps. If the historical formula did not handle -1 this way, say so, and confirm that the ec013.157 reproduction still yields 12/12 under the historical handling.

USER AMENDMENTS: fixed-length chunking and validation gate

Keep the whole-recording analysis. To stay within memory, apply the historical speed computation (x1-only, trenddecomp, original units/threshold) in chunks of exactly 331,702 LFP samples — the length of the original 40800:372501 window it was validated on.
- After the 2-s edge trim, tile each recording with consecutive 331,702-sample chunks overlapping by 20 s. Keep each chunk's central part, discarding 10 s at every internal chunk edge. Make the final chunk the LAST 331,702 samples of the recording, so every chunk has the same length.
- Stitch the speed traces, then apply the run/rest threshold, the missing-tracking rules and the 5-s bout criterion to the stitched trace. Bouts may cross chunk boundaries.
- If a recording is shorter than 331,702 samples (e.g. ec013.205), use it whole and flag it.
- Validation: on ec013.157, compare the chunked whole-recording speed labels with the historical labels over 40800:372501. Report the percentage of samples whose run/rest label agrees and how many of the 12/12 historical bouts are recovered with the same start/stop within 0.5 s. Report this; stop only if label agreement is below 95%.
Add these rules to PROTOCOL_rodent.md before analysing the new sessions.


DATED AMENDMENT 2026-10-22 — regional channels and tracking-rate behaviour

REVISED BEHAVIOUR AND CHANNEL PLAN (supersedes the chunked historical-speed plan). The historical speed (x1-only, trenddecomp, -1 sentinels kept, raw units) depends on the analysis window (12% of labels change with a 2.5-s shift) and is not used for any reported result. Record this in PROTOCOL_rodent.md, with a dated amendment, before running. The 12/12 reproduction stays only as a record of the original analysis. Tagged APC code is unchanged. Fix and log tooling errors; stop on anything method-relevant.

METADATA: use D:\APC_project\Previous_Computer\RealData\tPACPaper\hc3-session.csv (behaviour = linear for all 18 sessions), ElePosition.txt (shank regions per top-level directory) and ec012ec.14\ec012ec.269\ec012ec.269.xml.

1. CHANNEL-TO-REGION MAP: from the XML, report whether anatomical groups are contiguous 8-channel blocks (E1–E8 = shank 1, ...). If they are, apply the same mapping to EC012 and EC013 (the extra 65th/33rd channel is auxiliary and excluded), label each channel with its region from ElePosition.txt for that session's top directory (ec013.15, .18, .21, .27; ec012ec.13, .14, .17, .18, .21), and flag the EC013 mapping as "assumed contiguous, verified on ec012ec.269". If the XML is NOT contiguous, stop and report the grouping.

2. CHANNELS (prespecified; reuse the existing whole-recording theta/delta ratios): in each session, select the channel with the highest theta(6–10)/delta(1–4) ratio within (a) the CA1 shanks (EC013 only) and (b) the EC shanks (both animals). These are two separate analyses. Report each session's selected channels. Sensitivity: EC013 channel E1, labelled with its region.

3. SPEED (prespecified, at tracking rate, 39.0625 Hz):
   - Position = mean of the two LEDs when both are valid; the single valid LED otherwise; missing if neither (-1 = missing).
   - Linearly interpolate gaps <= 0.5 s; longer gaps stay missing.
   - Track axis = first principal component of valid positions. Linear position = projection onto it. Scale = 250 cm / (99.5th - 0.5th percentile of linear position).
   - Smooth x and y with a Gaussian kernel (SD 0.2 s), then compute 2-D speed by central difference, in cm/s.
   - RUN: speed > 6 cm/s AND linear position in the central 70% of the track. REST: speed < 6 cm/s AND linear position in the outer 15% at either end. Everything else is unclassified.
   - Bouts: contiguous same-state samples >= 5 s, split at gaps > 0.5 s, excluding the first and last 2 s of each recording.
   - Map bout times to LFP samples using the timestamps (fs 1250 Hz).
   - Report per session: the cm-per-unit scale, the fraction of missing samples, and the number of run and rest bouts and their durations.
   - Include a session in a regional analysis if it has >= 5 run and >= 5 rest bouts.

4. DESCRIPTIVE COMPARISON: for ec013.157, report the overlap between the new bouts and the historical 12/12 bouts (no gate).

5. Then run the per-bout analyses and statistics exactly as in the original rodent prompt (APC v1.0; A2' SOS scans; per-session and across-session statistics; mixed models with region-specific models), separately for CA1 and EC.

OUTPUT: update RESULTS_rodent.md with the region map, the behaviour summaries, the included sessions per region, all tables and figures, and deviations.
