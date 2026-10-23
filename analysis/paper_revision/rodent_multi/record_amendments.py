from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

out = Path(__file__).resolve().parent
p = out / 'PROTOCOL_rodent.md'
original = p.read_text(encoding='utf-8')
amendments = '''

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
'''
if 'USER AMENDMENTS: whole-recording' not in original:
    (out / 'PROTOCOL_rodent_original.md').write_text(original, encoding='utf-8')
    p.write_text(original + amendments, encoding='utf-8')
e = out / 'EXECUTION_rodent.md'
text = e.read_text(encoding='utf-8')
old = """The temporal interval for applying the historical speed procedure is pending
the user's answer to the interval question. Channel selection and metadata
inventory do not depend on that choice. No new-session bout analysis starts
before that choice is recorded."""
text = text.replace(old, "The user resolved the interval: whole recordings, with the appended missing-\ntracking, fixed-length chunking and ec013.157 validation rules in the protocol.")
details = '''

Chunk execution details fixed before the new ec013.157 validation

Use LFP sample times >= first time + 2 s and <= last time - 2 s. Chunk starts
advance by 331702-round(20*fs); force the final chunk to end at the last retained
sample. A short recording uses its whole trimmed interval. Discard round(10*fs)
speed samples at internal chunk edges. If the forced last chunk overlaps more
than 20 s, assign its remaining overlap at the midpoint of the retained cores;
each derivative sample is taken from exactly one chunk. Save chunk and seam
indices and assert complete, single coverage. No averaging across chunks.

Tracking interpolation retains the historical 39.06 Hz timestamps and x1-only
formula. Replace -1/nonfinite x1 with NaN. A bounded gap with missing sample
count/39.06 <= 0.5 s is linearly interpolated between its two valid neighbours.
Unbounded or longer gaps remain NaN for position interpolation; trenddecomp's
documented local implementation fills its NaNs with the chunk mean internally.
This does not make those times eligible: exclude every derivative touching a
missing position after stitching. Thus no long-gap position is labelled run or
rest. Other LED coordinates are counted for missingness but do not enter speed.

Record raw x1 missing fraction, any-coordinate missing fraction, long gaps,
and invalid LFP derivatives. For each state, bouts lost to gaps are baseline
>=5-s bouts of the same stitched speed trace that retain no >=5-s piece after
gap splitting. Also report intersected baseline bouts and short split pieces.

MATLAB rng(0,'twister') is set once before chunk decomposition; save each chunk's
incoming RNG state. Run chunks sequentially. The historical saved reproduction
is preserved separately and is not replaced by this missing-aware computation.

The validation denominator is every historical derivative sample, global
40800:372500. Missing/unlabelled new samples count as disagreement. Also report
agreement conditional on valid labels. Match historical and whole-recording
bouts one-to-one within state, requiring both endpoints within 0.5 s. The gate
uses all-sample agreement >=95%; no new session bout/PAC analysis before PASS.
'''
if 'Chunk execution details fixed' not in text:
    text += details
e.write_text(text, encoding='utf-8')
record = dict(recorded_utc=datetime.now(timezone.utc).isoformat(),
              protocol_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
              execution_sha256=hashlib.sha256(e.read_bytes()).hexdigest(),
              original_protocol_sha256=hashlib.sha256((out/'PROTOCOL_rodent_original.md').read_bytes()).hexdigest(),
              git_tag='v1.0', git_commit='71ebc16aed32ca38be73a800738b975e5806b330',
              stage='user amendments recorded before chunked behaviour validation')
(out/'protocol_amendments_record.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps(record))
