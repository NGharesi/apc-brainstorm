"""Correct only copied output labels; preserve numeric outputs unchanged."""
from pathlib import Path
import json,hashlib,shutil,difflib,sys
O=Path(__file__).resolve().parent;E=O/'phaseC/ecog';R=O.parent.parent;sys.path.insert(0,str(R/'pydeps'))
import pandas as pd
import numpy as np
A=E/'tooling_label_backup';assert not A.exists();A.mkdir()
oldlabel='APC-v1.0 minus MVL-Ozkurt';newlabel='APC-v3.0 minus MVL-Ozkurt';records=[]
P=pd.read_csv(E/'ecog_patient_summary.csv',encoding='utf-8',float_precision='round_trip');D=pd.read_csv(E/'patient_differences.csv',encoding='utf-8',float_precision='round_trip')
for subset in ['prespecified','sensitivity_a']:
    Q=P[P.subset.eq(subset)&P.recording.eq('movement')&P.method.isin(['APC-v3.0','MVL-Ozkurt'])]
    W=Q.pivot(index=['patient','method'],columns='state',values='sd_fP_hz').reindex(columns=['move','rest']);W['m']=(W.move+W.rest)/2;W=W.m.unstack('method').dropna();expected=W['APC-v3.0']-W['MVL-Ozkurt']
    z=D[D.subset.eq(subset)&D.endpoint.eq('within_state_fP_SD')].set_index('patient');assert np.allclose(expected.loc[z.index],z.difference,rtol=0,atol=1e-14)
for name in ['ecog_statistics.py','ecog_statistics.csv','patient_differences.csv','statistics_runtime.json']:
    p=E/name;s=p.read_text(encoding='utf-8');assert oldlabel in s;shutil.copy2(p,A/name);records.append(dict(path=name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()));p.write_text(s.replace(oldlabel,newlabel),encoding='utf-8')
(A/'label_fix.diff').write_text(''.join(difflib.unified_diff((A/'ecog_statistics.py').read_text(encoding='utf-8').splitlines(True),(E/'ecog_statistics.py').read_text(encoding='utf-8').splitlines(True),fromfile='copied label',tofile='correct v3 label')),encoding='utf-8')
(A/'manifest.json').write_text(json.dumps(dict(files=records,numeric_v3_primary2_differences_verified_against_saved_patient_SD=True,numerical_outputs_changed=False,method_calls=0,bootstrap_reruns=0),indent=2),encoding='utf-8')
p=O/'deviations.json';d=json.loads(p.read_text(encoding='utf-8'));d['deviations'].append(dict(type='ECoG copied Primary-2 label (tooling)',reason='The copied statistics code computed the v3-minus-scan SD difference correctly but retained the literal v1-minus-scan output label. Verified all saved patient differences against the v3 patient SD table, archived original labelled files with hashes, and replaced only that full label in the script/CSV/JSON. No number, bootstrap or method output was recomputed.'));d['deviations'].append(dict(type='Post-hoc CSV metadata dtype warning',reason='Pandas emitted a mixed-type warning for metadata-only columns that are missing on the reused old rows and strings on new v3 rows. The numeric analysis columns were unaffected; the statistics completed once with unchanged formulas. No retry or setting change was made.'));p.write_text(json.dumps(d,indent=2),encoding='utf-8');print('Primary-2 values verified as v3; only labels corrected; all numbers preserved.')
