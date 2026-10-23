"""POST HOC live consistency audit; only complete shared-input checkpoints are compared."""
from pathlib import Path
import sys,json,time,re
OUT=Path(__file__).resolve().parent;PARENT=OUT.parent;ROOT=PARENT.parent.parent;sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
import pandas as pd
from scipy.io import loadmat
meta=json.loads((OUT/'posthoc_2s_provenance.json').read_text(encoding='utf-8'))|dict(stage='POST HOC partial shared-input consistency audit',audit_complete=False)
oldb=pd.read_csv(PARENT/'regional_bouts.csv',encoding='utf-8');newb=pd.read_csv(OUT/'posthoc_2s_bouts.csv',encoding='utf-8')
lookup=newb.set_index(['session','state','lfp_start_idx','lfp_stop_idx']).bout.to_dict();rows=[]
for oldfile in sorted(PARENT.glob('regional_*_pac.mat')):
    old=loadmat(oldfile,simplify_cells=True);m=old['metadata'];parts=re.fullmatch(r'regional_(.+)_E(\d+)_(run|rest)_(\d+)_pac\.mat',oldfile.name);assert parts
    session,channel,state,_=parts.groups();assert int(channel)==int(m['channel_index']);key=(session,state,int(m['start_idx']),int(m['stop_idx']));number=lookup[key]
    newfile=OUT/f"posthoc_2s_{key[0]}_E{int(m['channel_index'])}_{key[1]}_{number:04d}_pac.mat"
    if not newfile.exists() or time.time()-newfile.stat().st_mtime<5:continue
    new=loadmat(newfile,simplify_cells=True)
    for method,a,b in zip(['APC-v1.0','MVL-raw','MVL-Ozkurt','KLMI','GLM'],old['features'],new['features']):
        equal=all(np.array_equal(np.asarray(a[col]),np.asarray(b[col]),equal_nan=True) for col in ['fP_hz','fA_hz','score','raw_mvl','ozkurt_mvl','preferred_phase_deg','status','effective_half_width_hz'])
        rows.append(dict(analysis_type=meta['analysis_type'],post_hoc=True,session=key[0],state=key[1],channel_index=int(m['channel_index']),method=method,prespecified_5s_checkpoint=str(oldfile),posthoc_2s_checkpoint=str(newfile),all_numeric_outputs_exact=equal,provenance_json=json.dumps(meta,separators=(',',':'))))
frame=pd.DataFrame(rows);frame.to_csv(OUT/'posthoc_2s_partial_shared_input_audit.csv',index=False,encoding='utf-8')
assert len(frame)>0 and frame.all_numeric_outputs_exact.all(),'METHOD-RELEVANT: a completed shared input differed'
print(json.dumps(dict(analysis_type=meta['analysis_type'],post_hoc=True,audit_complete=False,completed_shared_inputs=len(frame)//5,method_outputs_checked=len(frame),all_numeric_outputs_exact=True)))
