"""Archive candidate-1 records and add only the authorized candidate-2 amendment."""
from pathlib import Path
import hashlib,json,shutil
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
REPO=ROOT/'apc-brainstorm-publish'
TRACKED=REPO/'analysis/v2_revision/PROTOCOL_v2.md'
C2=OUT/'candidate_02'
C2.mkdir(exist_ok=False)
archive=OUT/'candidate_01';archive.mkdir(exist_ok=False)
for name in ['PROTOCOL_v2.md','RESULTS_v2.md','output_manifest.json']:
    shutil.copy2(OUT/name,archive/name)
original=TRACKED.read_text(encoding='utf-8')
assert original==(OUT/'PROTOCOL_v2.md').read_text(encoding='utf-8')
criteria=original[original.index('PART 5'):original.index('\nOUTPUT',original.index('PART 5'))]
amendment='''

## Candidate history

Candidate 1 (commit 7848af05ada722971769da856e970d0737820169) failed unit
gate (a): fP=10.631999875603938 Hz, fA=120 Hz. The user identified that PPC
is flat across filter centers whose passband contains the coupled rhythm;
the recorded curve is unit_attempt_01/unit_a_ppc_curve.csv. The five v1
compatibility cases and implementation invariants passed. No v2.0 tag or
held-out data were created. Candidate-1 protocol/report/manifest copies are
preserved in revision_checks/v2/candidate_01 and its unit records are unchanged.

Candidate 2 is the final candidate authorized by the user. The following
amendment replaces only Step 2, the event test, and the additional ordered
unit gate (a2). All earlier Step-2/PPC-event implementation notes above are
historical candidate-1 notes and are superseded by this amendment. All other
method settings, generators, unit profiles/seeds, held-out suite and C1-C4
remain exactly as committed in 7848af0. No further candidates will be made.

### Candidate 2: Step 2 replacement (burst-locked power)

- L=2 seconds. Usable burst centers have the complete half-open window
  [t_k-L/2,t_k+L/2) in the half-open record [t0,t0+T). Status 1 for T<4 s;
  status 3 for fewer than ten usable bursts.
- Extract L*fs samples at relative times -L/2:1/fs:L/2-1/fs; demean each
  segment and multiply by a symmetric Hann window of that length.
- Evaluate X_k(f)=sum_t w(t)*s_k(t)*exp(-i*2*pi*f*t) directly, on the grid
  fmin:0.05:fmax, fmin=max(minPhaseHz,10/T,3/L), fmax as originally specified.
- BLP(f)=(abs(sum_k X_k(f))^2-sum_k abs(X_k(f))^2)/(N*(N-1)). Select its
  grid maximum; refine with a three-point parabola on raw BLP when both
  neighbors are finite and on the grid. Use the inherited half-bin bound.
- PPC of the X_k phases is diagnostic only, on the entire grid and at the
  refined fP. No polarity flip is applied anywhere in Step 2.
- The phase reference for Steps 3-4 remains the original fourth-order
  zero-phase Butterworth at fP, half-width=max(0.5,0.25*fP).

### Candidate 2: event test replacement

- Primary statistic: maximum BLP on the full candidate grid. For each of
  200 surrogates, independently jitter each usable burst by uniform
  +/-1/fP seconds, conditioned on remaining within the window-usable center
  range. Implement this conditional uniform draw using its truncated interval
  per burst, which is equivalent to rejecting out-of-range uniform jitters.
- Recompute BLP on the entire grid for each surrogate and use its maximum.
  z=(observed maximum-mean surrogate maxima)/sample SD; empirical
  p=(1+number of surrogate maxima >= observed maximum)/201.
- Secondary uncorrected statistic: BLP at the refined observed fP, evaluated
  at that same fixed frequency in each surrogate. Report separate z and p.
- Jitter times are continuous. Segment samples use linear interpolation of
  x at those centers. Demeaning, Hann multiplication and direct Fourier
  evaluation are linear: batch the direct coefficient computation at unique
  bracketing sample centers and interpolate coefficients. Validate against
  independently extracted/interpolated segments and direct sums. No FFT-bin
  approximation or frequency interpolation is used.
- Record the local RNG seed/substream and both 200-element surrogate
  statistic vectors. No change to signal RNG state is permitted.

### Candidate 2: ordered unit gates and freeze

1. (a) unchanged high-SNR 8/120-Hz trial and seed 20260618; phase tolerance
   0.1 Hz, amplitude tolerance 4 Hz.
2. (a2) the same unit generator, each initialized with the same original
   seed 20260618, at fP in [5.3,6.7,9.4,10.8] Hz, in that order. All four
   require absolute fP error <=0.1 Hz. All other unit parameters are unchanged.
3. (b), (c), (d) unchanged, in that order.

Save BLP and PPC curves for every completed unit trial, including null and
existing-benchmark trials. Stop at the first failed gate; no further
candidates. Test candidate-2 working sources before committing; record the
candidate-1 base commit plus exact working-source/protocol/script hashes.
Only if all gates pass, commit candidate 2 with its protocol and execution
scripts, verify the tested source hashes, tag v2.0, then generate and run the
original held-out suite at seed 20261022. In the held-out event test, the
primary statistic and z/p are now the max-BLP statistics above. C1-C4 are
unchanged, including every threshold and paired decision calculation.
New candidate-2 outputs are under revision_checks/v2/candidate_02; candidate-1
saved results remain unchanged.
'''
updated=original.rstrip()+amendment
assert updated[updated.index('PART 5'):updated.index('\nOUTPUT',updated.index('PART 5'))]==criteria
for p in [TRACKED,OUT/'PROTOCOL_v2.md',C2/'PROTOCOL_v2.md']:
    p.write_text(updated,encoding='utf-8')
(C2/'candidate_history.json').write_text(json.dumps({'candidate':2,'parent_candidate_commit':'7848af05ada722971769da856e970d0737820169',
 'candidate1_failure':{'gate':'a','fp_hz':10.631999875603938,'fa_hz':120},
 'candidate1_cause':'User-supplied: PPC is flat across filter centers whose passband contains the coupled rhythm.',
 'protocol_sha256':hashlib.sha256(updated.encode('utf-8')).hexdigest(),
 'decision_criteria_sha256':hashlib.sha256(criteria.encode('utf-8')).hexdigest(),'heldout_generated':False},indent=2),encoding='utf-8')
print('Candidate-1 records archived; candidate-2 protocol written; no data generated.')
