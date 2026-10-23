"""Evidence for reading/timeline gates; no ds004752 PAC estimates."""
from pathlib import Path
import sys,json,hashlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent
sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
import pandas as pd

meta=json.loads((OUT/'provenance.json').read_text(encoding='utf-8'))
old=pd.read_csv(ROOT/'apc_openneuro_ieeg_screening_epochs.csv',encoding='utf-8')
evidence=dict(provenance=meta,source=str(ROOT/'run_apc_openneuro_ieeg_validation.m'),source_sha256=hashlib.sha256((ROOT/'run_apc_openneuro_ieeg_validation.m').read_bytes()).hexdigest(),screening_rows=len(old),counts={c:dict(finite=int(np.isfinite(old[c]).sum()),nan=int(old[c].isna().sum())) for c in ['apc_strength','apc_fp_hz','apc_fa_hz','apc_z','pac_strength','pac_fp_hz','pac_fa_hz','pac_z']},cause='The earlier screening configured n_surrogates=0, so local_analyze_epoch never assigned the preinitialized NaN apc_z/pac_z fields; the saved screening coupling strengths and selected frequencies are finite.')
(OUT/'earlier_screening_nan_cause.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
papers=dict(provenance=meta,references=[dict(url='https://www.nature.com/articles/s41597-020-0364-3.pdf',location='Figure 1a, page 2; Task methods, page 2',evidence='Figure 1a shows 1-s fixation, 2-s encoding, 3-s maintenance, then probe. These durations place encoding at 1 s and probe at 6 s relative to trial start.'),dict(url='https://elifesciences.org/articles/78677',location='Task and behavior; Materials and methods / Task',evidence='Encoding lasts 2 s and maintenance lasts 3 s before the probe. Probe-relative intervals are fixation -6 to -5 s, encoding -5 to -3 s, and maintenance -3 to 0 s.')],dataset_readme=str(Path(meta['data_root'])/'README'),scope='Papers establish task sequence; empirical scalp gate remains required before any dataset APC/scan output.')
(OUT/'timeline_paper_evidence.json').write_text(json.dumps(papers,indent=2),encoding='utf-8')
print(evidence['cause']);print(json.dumps(evidence['counts']))
