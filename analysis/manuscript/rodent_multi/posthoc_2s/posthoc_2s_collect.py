"""Collect POST HOC 2-s outputs and compare identical inputs to prespecified 5-s results."""
from pathlib import Path
import sys,json,time
OUT=Path(__file__).resolve().parent;PARENT=OUT.parent;ROOT=PARENT.parent.parent;sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
import pandas as pd
META=json.loads((OUT/'posthoc_2s_provenance.json').read_text(encoding='utf-8'))
def read(p):return pd.read_csv(p,encoding='utf-8')
def write(d,name):
    d=d.copy();d['analysis_type']=META['analysis_type'];d['post_hoc']=True;d['minimum_bout_s']=2;d['provenance_json']=json.dumps(META,separators=(',',':'));d.to_csv(OUT/name,index=False,encoding='utf-8')
workers=[json.loads((OUT/f'posthoc_2s_worker{k}_runtime.json').read_text(encoding='utf-8')) for k in range(1,4)]
assert all(w['status']=='COMPLETE' for w in workers),'POST HOC worker incomplete or failed; stop'
allrows=pd.concat([read(OUT/f'posthoc_2s_worker{k}_estimates.csv') for k in range(1,4)],ignore_index=True)
assert not allrows.duplicated(['analysis','session','state','bout','method']).any()
assert allrows.groupby(['analysis','session','state','bout']).size().eq(5).all()
allrows=allrows.sort_values(['analysis','animal','session','state','bout','method']).reset_index(drop=True)
allrows.to_csv(OUT/'posthoc_2s_bout_estimates.csv',index=False,encoding='utf-8')
guards=pd.concat([read(OUT/f'posthoc_2s_worker{k}_filter_guards.csv') for k in range(1,4)],ignore_index=True)
assert (guards.max_pole_radius<1).all() and (guards.max_sos_section_pole_radius<1).all() and (abs(guards.center_gain-1)<1e-3).all()
guards=guards.drop_duplicates(['fs_hz','low_hz','high_hz']);write(guards,'posthoc_2s_comparator_filter_guards.csv')
old=read(PARENT/'regional_bout_estimates.csv');oldb=read(PARENT/'regional_bouts.csv')
newb=read(OUT/'posthoc_2s_bouts.csv')
keys=['session','state','bout'];bounds=['lfp_start_idx','lfp_stop_idx']
old=old.merge(oldb[keys+bounds],on=keys,validate='many_to_one')
new=allrows.merge(newb[keys+bounds],on=keys,validate='many_to_one')
join=['analysis','animal','session','state','method','channel_index']+bounds
shared=old.merge(new,on=join,suffixes=('_prespecified_5s','_posthoc_2s'),validate='one_to_one')
assert len(shared)==1680,'METHOD-RELEVANT: not all shared prespecified inputs were found'
exact=np.ones(len(shared),bool);comparison=shared[join+['bout_prespecified_5s','bout_posthoc_2s']].copy()
for column in ['fP_hz','fA_hz','score','raw_mvl','ozkurt_mvl','preferred_phase_deg','status','effective_half_width_hz']:
    a=shared[column+'_prespecified_5s'].to_numpy();b=shared[column+'_posthoc_2s'].to_numpy();match=(a==b)|(pd.isna(a)&pd.isna(b));exact&=match
    comparison[column+'_prespecified_5s']=a;comparison[column+'_posthoc_2s']=b;comparison[column+'_exact']=match
comparison['all_numeric_outputs_exact']=exact
write(comparison,'posthoc_2s_shared_5s_exact_comparison.csv')
if not exact.all():
    (OUT/'posthoc_2s_method_failure.json').write_text(json.dumps(dict(status='FAILED_STOP',analysis_type=META['analysis_type'],post_hoc=True,error='Identical input outputs differed from prespecified 5-s results',mismatched_rows=int((~exact).sum()),metadata=META),indent=2),encoding='utf-8')
    raise RuntimeError('METHOD-RELEVANT: identical-input outputs differ; stop')
status=dict(status='COMPLETE',analysis_type=META['analysis_type'],post_hoc=True,metadata=META,rows=len(allrows),unique_input_checkpoints=len(list(OUT.glob('posthoc_2s_*_pac.mat'))),
            worker_compute_seconds=[w['elapsed_seconds'] for w in workers],worker_compute_seconds_sum=sum(w['elapsed_seconds'] for w in workers),maximum_worker_compute_seconds=max(w['elapsed_seconds'] for w in workers),
            shared_prespecified_method_rows=1680,shared_prespecified_outputs_exact=bool(exact.all()),filter_guard_entries=len(guards))
(OUT/'posthoc_2s_bouts_runtime.json').write_text(json.dumps(status,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in status.items() if k!='metadata'}))
