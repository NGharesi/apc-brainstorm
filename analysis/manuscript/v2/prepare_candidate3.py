"""Preserve the final candidate-2 snapshot and record candidate-3 authorization."""
from pathlib import Path
import hashlib,json
BASE=Path(__file__).resolve().parent;ROOT=BASE.parent.parent
A=ROOT/'apc-brainstorm-publish/analysis/v2_revision';OUT=BASE/'candidate_03'
OUT.mkdir(exist_ok=False)
original=(A/'PROTOCOL_v2.md').read_text(encoding='utf-8')
assert original==(BASE/'candidate_02/PROTOCOL_v2.md').read_text(encoding='utf-8')
criteria=original[original.index('PART 5'):original.index('\nOUTPUT',original.index('PART 5'))]
amendment='''

### Candidate history: candidate 2 and final candidate 3

Candidate 2 failed gate (a) only on fA: fP=7.9996901239320914 Hz passed;
fA=115 Hz had error 5 Hz, exceeding the allowed 4 Hz. The user's diagnosis
is that the Step-4 score versus center frequency is bimodal, with peaks near
fA +/- fP and a dip at fA, because a flat-top Butterworth band of half-width
fP puts the modulation sidebands at its edges. The candidate-2 source and
its unit report/curves remain preserved in revision_checks/v2/candidate_02.

The user has now authorized candidate 3 as the final candidate. This later
authorization supersedes the candidate-2 instruction that no further
candidate would be made. Only Step 4 and the specified a2 pairs change.
Candidate-2 Step 2 (BLP), both event-test statistics, Steps 1/3, the unit
profiles/seeds, the held-out suite and C1-C4 remain unchanged. No further
candidate is authorized after candidate 3.

### Candidate 3: Step 4 replacement (peaked kernel)

- Candidate centers fc are the unchanged 1-Hz grid within ampRange.
- Reflect x for one second at each end. The precise reflection convention
  excludes a repeated endpoint: x(p+1:-1:2), x, x(end-1:-1:end-p), p=round(fs).
- FFT the padded signal at its actual length. On the signed-frequency grid,
  multiply by G(f)=2*exp(-(f-fc)^2/(2*sigma^2)) for f>0 and zero for f<=0,
  sigma=1.5*fP; inverse FFT and crop exactly p samples at each end. The
  positive Nyquist bin, when present, follows the literal positive-frequency
  formula. Do not clip the Gaussian tails to ampRange.
- Envelope=absolute analytic band signal; score=raw Canolty MVL with the
  unchanged fP phase reference. No moving-mean smoothing.
- Select the grid maximum and refine with a three-point parabola on raw
  score when both neighbors are inside ampRange and the maximum is concave.
  Retain the inherited half-bin bound and first-grid-point tie handling.
- Recompute the Gaussian envelope at the refined fA. Report raw C_APC and
  conventional Ozkurt MVL from that same envelope. Gaussian sigma is output
  explicitly; obsolete finite rectangular-band-width fields are NaN.
- Save the raw fA score curve for every completed unit trial, alongside its
  BLP and PPC curves. If Step 4 was not reached, save the prescribed center
  grid with NaN scores and an explicit step4_reached=false flag.

### Candidate 3: unit gates and conditional freeze

Run the same sequential stopping rule: (a), (a2), (b), (c), (d).
(a) remains |fP-8|<=0.1 Hz and |fA-120|<=4 Hz.
(a2) now uses the four true pairs in order: (5.3,95), (6.7,108), (9.4,131),
(10.8,142), each with the same unchanged generator and seed scheme; both
|fP error|<=0.1 Hz and |fA error|<=4 Hz are required for every trial.
(b), (c), (d) remain exactly as specified for candidate 2.

Before the performance gates, retain the inherited mathematical/compatibility
checks and verify Step-2 and event outputs match the saved candidate-2 unit
(a) exactly on its unchanged signal. Validate the Gaussian envelope/score
against the literal FFT formula. These checks do not change any method.

Only if all gates pass, commit candidate 3 with its protocol and execution
scripts, verify tested source hashes, tag v2.0, then generate/run the original
held-out suite and unchanged comparators/criteria at seed 20261022. On any
gate failure, stop and report; no further candidates. Candidate-3 outputs
are kept separately under revision_checks/v2/candidate_03. Earlier saved
candidate reports, curves, inputs and source snapshots are not overwritten.
'''
updated=original.rstrip()+amendment
assert updated[updated.index('PART 5'):updated.index('\nOUTPUT',updated.index('PART 5'))]==criteria
for p in [A/'PROTOCOL_v2.md',BASE/'PROTOCOL_v2.md',OUT/'PROTOCOL_v2.md']:
    p.write_text(updated,encoding='utf-8')
(OUT/'candidate_history.json').write_text(json.dumps({'candidate':3,'candidate2_failure':{'gate':'a','fp_hz':7.9996901239320914,'fa_hz':115,'failed_part':'fA'},
 'candidate2_diagnosis':'User-supplied: bimodal Butterworth Step-4 score with modulation sidebands at band edges.',
 'protocol_sha256':hashlib.sha256(updated.encode('utf-8')).hexdigest(),'criteria_sha256':hashlib.sha256(criteria.encode('utf-8')).hexdigest(),
 'heldout_generated':False,'no_further_candidates':True},indent=2),encoding='utf-8')
print('Candidate-3 history and protocol recorded; earlier candidate records preserved.')
