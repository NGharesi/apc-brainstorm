"""Record visual and literature confirmation of the completed timing gate."""
from pathlib import Path
import json,sys
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent;sys.path.insert(0,str(ROOT/'pydeps'))
import pandas as pd
meta=json.loads((OUT/'provenance.json').read_text(encoding='utf-8'));m=json.loads((OUT/'timeline_gate_measurements.json').read_text(encoding='utf-8'))
assert m['files']==68 and m['trials']==3353 and [p['latency_ms'] for p in m['peaks']]==[160,200]
assert all(50<=p['latency_ms']<=250 for p in m['peaks'])
e=json.loads((OUT/'edf_reading_gate_attempt2.json').read_text(encoding='utf-8'));assert e['passed']
confirmation=dict(passed=True,provenance=meta,empirical_evidence='Visual review of the saved whole-trial grand average and onset zooms shows a negative evoked deflection after both prespecified onsets. Peaks are 160 ms after encoding onset at 1 s and 200 ms after probe onset at 6 s; both lie within 50-250 ms.',plot='timeline_grand_average.png',svg='timeline_grand_average.svg',trials=3353,files=68,latency_resolution_ms=5,peaks=m['peaks'],literature_evidence='timeline_paper_evidence.json',timeline=dict(fixation_s=[0,1],encoding_s=[1,3],maintenance_s=[3,6],probe_onset_s=6),additional_signal_filter=False)
(OUT/'timeline_gate_confirmation.json').write_text(json.dumps(confirmation,indent=2),encoding='utf-8')
f=pd.read_csv(OUT/'timeline_file_checks.csv',encoding='utf-8');f['patient']=f.file.str.extract(r'(sub-\d+)');r=f.groupby('native_fs_hz').agg(n_patients=('patient','nunique'),n_sessions=('file','size'),trials=('trials','sum')).reset_index();r['provenance_json']=json.dumps(meta,separators=(',',':'));r.to_csv(OUT/'native_scalp_rate_summary.csv',index=False,encoding='utf-8')
meta['status']='ALL_GATES_PASSED_CONTACT_ORDER_CLARIFICATION_PENDING';meta['stage']='All gates passed; no contact selection or dataset method outputs'
(OUT/'provenance.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
(OUT/'STATUS.json').write_text(json.dumps(dict(status=meta['status'],provenance=meta,equivalence_passed=True,ieeg_reading_files_passed=68,scalp_files_passed=68,timeline_passed=True,dataset_apc_estimates=0,dataset_scan_estimates=0),indent=2),encoding='utf-8')
print(json.dumps(dict(all_gates_passed=True,latencies_ms=[160,200],scalp_trials=3353)))
