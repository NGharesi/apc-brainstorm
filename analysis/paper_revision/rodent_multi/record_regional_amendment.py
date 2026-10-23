from pathlib import Path
import json,hashlib,datetime,shutil
out=Path(__file__).resolve().parent
request='''REVISED BEHAVIOUR AND CHANNEL PLAN (supersedes the chunked historical-speed plan). The historical speed (x1-only, trenddecomp, -1 sentinels kept, raw units) depends on the analysis window (12% of labels change with a 2.5-s shift) and is not used for any reported result. Record this in PROTOCOL_rodent.md, with a dated amendment, before running. The 12/12 reproduction stays only as a record of the original analysis. Tagged APC code is unchanged. Fix and log tooling errors; stop on anything method-relevant.

METADATA: use D:\\APC_project\\Previous_Computer\\RealData\\tPACPaper\\hc3-session.csv (behaviour = linear for all 18 sessions), ElePosition.txt (shank regions per top-level directory) and ec012ec.14\\ec012ec.269\\ec012ec.269.xml.

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

OUTPUT: update RESULTS_rodent.md with the region map, the behaviour summaries, the included sessions per region, all tables and figures, and deviations.'''
p=out/'PROTOCOL_rodent.md'
marker='DATED AMENDMENT 2026-10-22 — regional channels and tracking-rate behaviour'
if marker not in p.read_text(encoding='utf-8'):
    for name in ['RESULTS_rodent.md','STATUS.json','RESUME_STATUS.json','output_manifest.json','deviations.json']:
        src=out/name;dst=out/(src.stem+'_chunk_plan_stopped'+src.suffix)
        if src.exists() and not dst.exists():shutil.copy2(src,dst)
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write('\n\n'+marker+'\n\n'+request+'\n')
details='''

DATED EXECUTION AMENDMENT 2026-10-22 — supersedes historical/chunk rules

The revised user plan supersedes the chunked historical-speed gate and the
unrestricted channel selection. Historical 12/12 is an archival check only.
The stated 12% shift sensitivity is the user's supplied rationale; it is not
independently rerun as a new gate. All reported regional results use the new
tracking-rate procedure. Earlier ratios and raw sources remain unchanged.

LED validity requires both coordinates finite and unequal to -1. Combine valid
LED pairs, fill only bounded missing-position runs with missing-count/39.0625
<=0.5 s, then fit PCA to all finite combined/interpolated positions. Fix axis
sign by making its largest-magnitude loading positive. Use linearly interpolated
sample quantiles (0.5%,99.5%). Linear position for state classification is the
projection before Gaussian smoothing, anchored at the 0.5% quantile. Central
70% is the interval [15%,85%] of that robust extent. End zones are below 15%
or above 85%, including the extreme 0.5% tails. Regions are symmetric to PCA sign.

Smooth each finite-position segment independently using a normalized Gaussian
kernel, SD 0.2*39.0625 samples, truncated at ceil(4*SD) samples, reflected segment
boundaries. Do not bridge long gaps. Central differences require both adjacent
tracking samples; segment endpoints are unclassified. Multiply 2-D coordinate
speed by the session's cm-per-unit scale. Speed exactly 6 is unclassified.

Tracking timestamps start at the recording's first LFP timestamp, step 1/39.0625.
Treat tracking samples as half-open bins [t,t+dt); keep bins wholly within the
recording's first/last 2-s trim. Minimum bout duration is samples/39.0625 >=5 s.
Map [bout_start,bout_stop_exclusive) to actual LFP timestamps with searchsorted;
include the first LFP sample >=start and the last <stop_exclusive. Save both
tracking and LFP indices and mapped durations; do not upsample speed.

Reuse existing theta/delta ratios within anatomical channel masks, excluding
auxiliary E33/E65. Choose the first finite maximum. CA1 and EC are separate
analyses; E1 is a separately labelled EC013 sensitivity with identical bouts.
Save complete per-channel region map, metadata source rows and mapping assumption.

Reuse the prespecified statistical definitions and seed 20261022 above. Fit
region-specific REML models. CA1 contains only EC013: animal is constant and
its redundant fixed-effect column is absent, so the estimable model is
outcome ~ state_run + (1 + state_run | session); retain the same session random
intercept/slope. EC uses outcome ~ state_run + animal + (1 + state_run | session).
If a region has only one represented animal after eligibility, explicitly use
the same constant-animal formulation. Record singular fits/convergence warnings;
do not simplify the random-effects structure after seeing outcomes. Nonzero
frozen APC statuses are retained and counted, with finite-value denominators.
The plotted scan remains the preselected MVL-Ozkurt maximum, independently of
run/rest differences; report all four scans. New outputs use regional_* names
so no earlier results or checkpoints are overwritten except the requested report
and current status/manifest files (their stopped versions were archived).
'''
e=out/'EXECUTION_rodent.md'
if 'DATED EXECUTION AMENDMENT 2026-10-22' not in e.read_text(encoding='utf-8'):
    with e.open('a',encoding='utf-8',newline='\n') as f:f.write(details)
meta=dict(recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stage='regional amendment before new regional analysis',
          git_tag='v1.0',git_commit='71ebc16aed32ca38be73a800738b975e5806b330',seed=20261022,
          protocol_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),execution_sha256=hashlib.sha256(e.read_bytes()).hexdigest(),
          supersedes='chunked historical-speed gate and unrestricted channel selection',tracking_fs_hz=39.0625)
(out/'regional_protocol_record.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
(out/'STATUS.json').write_text(json.dumps(dict(status='REGIONAL_AMENDMENT_RECORDED',metadata=meta),indent=2),encoding='utf-8')
print(json.dumps(meta))
