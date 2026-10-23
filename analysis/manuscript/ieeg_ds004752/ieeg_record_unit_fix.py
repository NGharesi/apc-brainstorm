"""Document the single metadata-reading correction before rerunning gates."""
from pathlib import Path
import json,difflib
OUT=Path(__file__).resolve().parent
before=(OUT/'ieeg_reading_gates_before_unit_fix.m.txt').read_text(encoding='utf-8')
after=(OUT/'ieeg_reading_gates.m').read_text(encoding='utf-8')
(OUT/'unit_reader_fix.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='before_unit_fix',tofile='ieeg_reading_gates.m')),encoding='utf-8')
path=Path(r'D:\APC_project\RealDatasets\OpenNeuro_ds004752\sub-01\ses-01\ieeg\sub-01_ses-01_task-verbalWM_run-01_ieeg.edf')
with path.open('rb') as f:
    header=f.read(256);ns=int(header[252:256]);f.seek(256+ns*(16+80));dimensions=f.read(ns*8)
assert all(dimensions[i*8:(i+1)*8].strip()==b'' for i in range(ns))
detail=dict(type='resolved EDF unit metadata reader defect',reason='All 48 EDF physical-dimension fields in the first file are blank; the BIDS channels.tsv declares microvolts. The first reader incorrectly required an EDF unit label as well as numeric range checks. The corrected reader accepts the BIDS declaration when the EDF field is blank and still rejects conflicting nonblank units. No signal scaling, thresholds, methods or protocol text changed.',identified_without_method_outcomes=True,rerun='Reading gates only, once after this correction',diff='unit_reader_fix.diff',archived_initial_outputs=['edf_channel_checks_initial_unit_reader.csv','edf_file_checks_initial_unit_reader.csv','reading_gate_initial_unit_reader_failure.json','reading_gates_initial_unit_reader.log'])
d=json.loads((OUT/'deviations.json').read_text(encoding='utf-8'));d['deviations'].append(detail);d['deviations'].append(dict(type='pre-existing MATLAB startup path warnings',reason='MATLAB startup lists nonexistent historical Brainstorm directories. Explicit source-path assertions passed. No startup or installation changes were made.'))
(OUT/'deviations.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
(OUT/'reading_gate_failure.json').write_text(json.dumps(dict(status='RESOLVED_TOOLING_READER_ERROR',detail=detail,original_failure='reading_gate_initial_unit_reader_failure.json'),indent=2),encoding='utf-8')
print('EDF blank unit metadata verified from raw header; correction and diff logged')
