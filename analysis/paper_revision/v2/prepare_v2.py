"""Copy the user's protocol verbatim and predeclare implementation details."""
from pathlib import Path
import hashlib,json,subprocess
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
REPO=ROOT/'apc-brainstorm-publish'
A=REPO/'analysis/v2_revision'
A.mkdir(parents=True,exist_ok=True)
REQUEST=Path(r'C:\Users\nghare\.codex\attachments\2b4f7cd7-11e9-4a76-a14d-93e254a7a50d\Pasted text.txt')
spec=REQUEST.read_text(encoding='utf-8')
details='''

IMPLEMENTATION DETAILS FIXED BEFORE UNIT OR HELD-OUT OUTCOMES

- Requested output protocol is mirrored byte-for-byte in the tracked
  analysis/v2_revision/PROTOCOL_v2.md because revision_checks/v2 is outside
  the Git repository. Commit both code and the tracked protocol together.
- version='v2' dispatches to the new algorithm. Absent version, version='v1'
  and version='v1.0' retain all existing v1 calculations and outputs.
- Fourth-order Butterworth means fourth-order bandpass in total, implemented
  by butter(2, [low high]/Nyquist), zp2sos and filtfilt, as in v1's amplitude
  filter family. Step 1 calls the unchanged v1 helper functions directly.
- Record duration is N/fs. Event edge guards use first/last sampled times.
  The literal candidate grid is fmin:0.1:fmax, without appending an endpoint.
  A candidate needs >=10 edge-usable burst events; otherwise its PPC is NaN.
  PPC=(abs(sum(exp(1i*phase)))^2-N)/(N*(N-1)), without clipping negative values.
  Reference: Vinck et al. 2010, equations 14-15,
  https://doi.org/10.1016/j.neuroimage.2010.01.073 .
- Refine an interior concave peak with a parabola through the three raw PPC
  values; finite neighbors required, offset bounded to half a grid interval.
  Refilter and reapply event guards at the final refined fP. Status 3 if fewer
  than ten events remain. Step 4 and event tests use this final phase filter.
- Three-point amplitude-score smoothing uses a centered moving mean with
  shortened endpoint windows. Report raw MVL at the selected fA, not the
  smoothed selection score. Ties choose the first grid point.
- Event-test surrogates jitter each event in the observed fP-usable subset.
  Its 1/fP edge margin guarantees all independent uniform +/-1/fP jitters
  remain in the record; do not impose a second edge guard on surrogates.
  Evaluate continuous jitter times by linear interpolation of unwrapped
  Hilbert phase. Use sample SD (N-1); zero SD yields z=NaN and warning bit 16.
  Always 200 surrogates. RNG is a local mrg32k3a stream with recorded seed
  and substream; it must not change the simulation/global RNG state.
- Diagnostic warning bits: 1=no complete burst-average epochs; 2=no troughs;
  4=no complete trough profiling epochs; 8=diagnostic exception;
  16=zero/nonfinite surrogate SD. Diagnostics never choose fP or fA and their
  failure never changes method success status. Record exceptions explicitly.
- Unit (a): six-second 500-Hz signal, 8-Hz sine amplitude 1, 120-Hz carrier,
  base carrier amplitude .08, Gaussian bursts sigma .028 s, amplitude
  1.3*.60, original .010-s jitter centered on physical troughs, 20-dB mixed
  pink/white noise. Use original distractor-generator formulas, omitting the
  entire 96-Hz component. Seed 20260618; amplitude range [80,160].
- Unit (b): the exact same signal/noise as (a), plus 3*sin(2*pi*11*t+phi),
  phi uniform from a separate mrg32k3a stream, seed 20260619, substream 1.
- Unit (c): ten seeds 20260618:20260627, same unit profile. Replace only the
  true-burst component with homogeneous Poisson events at 8 Hz, original
  extended support, overlaps allowed, original envelope normalization and
  paired noise. A separate mrg32k3a stream (seed=trial seed, substream=3)
  supplies Poisson draws; surrogate seed=trial seed+1, substream=2.
- Unit (d): first 25 saved coupled distractor trials (level 0) in the original
  seed-20260618 trial order. Check runs, report all statuses and recovery;
  never use them to alter the method.
- Run gates sequentially. On any performance gate failure, save the completed
  test rows and STOP: no remaining tests, v2.0 tag or held-out generation.
  An identifiable implementation bug may be corrected before tagging, with
  every correction logged; no parameter or unit-signal retuning is allowed.
- Before performance gates, verify unchanged v1 outputs against a renamed
  copy from tag v1.0 on five saved inputs, and verify PPC against explicit
  pairwise cosines, burst detection identity and no global RNG consumption.
- Held-out streams will be mrg32k3a with seed 20261022 and distinct substreams
  for signals, frequencies, Poisson events and event-test surrogates. Record
  the full stream/substream map before any held-out data are generated.
- If gates pass, build and commit the held-out execution scripts and full
  comparator/decision bookkeeping before tagging and generating any data.
  Additional bookkeeping choices must not alter the fixed method or criteria.
'''
protocol=spec.rstrip()+details
for p in [OUT/'PROTOCOL_v2.md',A/'PROTOCOL_v2.md']:
    assert not p.exists(),str(p)
    p.write_text(protocol,encoding='utf-8')
GIT=r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe'
base=subprocess.check_output([GIT,'-C',str(REPO),'show','v1.0:src/bst_apc.m'],encoding='utf-8')
reference=base.replace('function [sApc, runInfo] = bst_apc(', 'function [sApc, runInfo] = v2_v1_reference(',1)
(OUT/'v2_v1_reference.m').write_text(reference,encoding='utf-8')
manifest={'base_tag':'v1.0','base_commit':'71ebc16aed32ca38be73a800738b975e5806b330',
 'protocol_sha256':hashlib.sha256(protocol.encode('utf-8')).hexdigest(),
 'request_sha256':hashlib.sha256(spec.encode('utf-8')).hexdigest(),
 'request_file':str(REQUEST),'reference_change':'first function name only',
 'heldout_generated':False,'predeclared_unit_signal_seed':20260618,'heldout_seed':20261022}
(OUT/'preimplementation_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Protocol and v1 reference prepared; no simulation data generated.')
