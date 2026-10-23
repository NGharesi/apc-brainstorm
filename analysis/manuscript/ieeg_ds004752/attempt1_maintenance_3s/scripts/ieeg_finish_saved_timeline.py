"""Finish peak-structure packaging from the saved, complete scalp grand average."""
from pathlib import Path
import sys,json,hashlib,difflib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent;sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
import pandas as pd
meta=json.loads((OUT/'provenance.json').read_text(encoding='utf-8'));p=OUT/'timeline_grand_average.csv'
files=pd.read_csv(OUT/'timeline_file_checks.csv',encoding='utf-8');trials=pd.read_csv(OUT/'timeline_resampling_trial_checks.csv',encoding='utf-8');d=pd.read_csv(p,encoding='utf-8')
assert len(files)==68 and files.passed.eq(1).all() and trials.passed.eq(1).all() and trials.output_samples.eq(1600).all() and len(d)==1600
t=d.time_s.to_numpy();grand=d.grand_average_uv.to_numpy();peaks=[]
for onset in [1,6]:
    keep=np.flatnonzero((t>=onset+.05)&(t<=onset+.25));baseline=float(np.mean(grand[(t>=onset-.2)&(t<onset)]));idx=keep[np.argmax(abs(grand[keep]-baseline))]
    peaks.append(dict(expected_onset_s=onset,peak_time_s=float(t[idx]),latency_ms=int(round((t[idx]-onset)*200)*5),peak_uv=float(grand[idx]),preonset_mean_uv=baseline,absolute_peak_difference_uv=float(abs(grand[idx]-baseline))))
result=dict(status='REQUIRES_VISUAL_AND_PAPER_CONFIRMATION',trials=len(trials),files=68,latency_resolution_ms=5,peaks=peaks,processing='Each scalp trial resampled to 200 Hz by Amendment 2; no additional filter; fixation-mean subtraction per trial/channel; O1/O2/Oz averaged per trial; equal trial weights',peak_rule='largest absolute deviation from preceding 200-ms mean within 50-250 ms after each prespecified onset',source_csv_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),raw_trial_recomputations_after_fix=0,provenance=meta)
(OUT/'timeline_gate_measurements.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
before=(OUT/'timeline_gate_before_peak_structure_fix.m.txt').read_text(encoding='utf-8');after=(OUT/'ieeg_amendment2_timeline_gate.m').read_text(encoding='utf-8')
(OUT/'timeline_peak_structure_fix.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='before_peak_structure_fix',tofile='ieeg_amendment2_timeline_gate.m')),encoding='utf-8')
deviations=json.loads((OUT/'deviations.json').read_text(encoding='utf-8'));deviations['deviations'].append(dict(type='resolved timeline peak structure packaging',reason='After all 68 scalp inputs had been read and the complete grand-average CSV saved, appending fields to MATLAB struct([]) failed. The code now collects cells before concatenating. The same fixed peak rule was evaluated from the saved grand-average CSV in Python, without rereading or resampling any raw trial. The defect was identified before viewing the trace or PAC outcomes.',diff='timeline_peak_structure_fix.diff',raw_trial_reruns=0))
(OUT/'deviations.json').write_text(json.dumps(deviations,indent=2),encoding='utf-8')
(OUT/'timeline_gate_failure.json').write_text(json.dumps(dict(status='RESOLVED_TOOLING_PACKAGING_ERROR',original_failure='timeline_peak_structure_initial_failure.json',provenance=meta),indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='provenance'}))
