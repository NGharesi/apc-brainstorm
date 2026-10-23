"""Summarize completed gates without computing dataset PAC outcomes."""
from pathlib import Path
import json,sys,re
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent;sys.path.insert(0,str(ROOT/'pydeps'))
import pandas as pd
meta=json.loads((OUT/'provenance.json').read_text(encoding='utf-8'))
f=pd.read_csv(OUT/'edf_file_checks_attempt2.csv',encoding='utf-8');assert len(f)==68 and f.passed.eq(1).all()
f['patient']=f.file.map(lambda s:re.search(r'sub-\d+',s).group());f['session']=f.file.map(lambda s:re.search(r'ses-\d+',s).group())
r=f.groupby('native_fs_hz').agg(n_patients=('patient','nunique'),n_sessions=('session','size')).reset_index();r['provenance_json']=json.dumps(meta,separators=(',',':'));r.to_csv(OUT/'native_ieeg_rate_summary.csv',index=False,encoding='utf-8')
rows=[]
for attempt,p in [(1,OUT/'attempt1_archive/equivalence_gate.json'),(2,OUT/'equivalence_gate_attempt2.json')]:
    e=json.loads(p.read_text(encoding='utf-8'))
    for i,name in enumerate(['fP_hz','fA_hz','raw_mvl','preferred_phase_deg']):rows.append(dict(attempt=attempt,metric=name,expected=e['expected'][i],observed=e['observed'][i],absolute_difference=e['absolute_differences'][i],passed=e['passed'],run_git_head=e['provenance']['git_head'],run_protocol_sha256=e['provenance']['protocol_sha256'],source_json=str(p),provenance_json=json.dumps(meta,separators=(',',':'))))
pd.DataFrame(rows).to_csv(OUT/'equivalence_both_attempts.csv',index=False,encoding='utf-8')
print(r.drop(columns='provenance_json').to_string(index=False))
