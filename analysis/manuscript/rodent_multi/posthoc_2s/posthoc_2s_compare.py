"""POST HOC 2-s sensitivity comparisons beside unchanged prespecified 5-s tables."""
from pathlib import Path
import sys,json
OUT=Path(__file__).resolve().parent;PARENT=OUT.parent;ROOT=PARENT.parent.parent;sys.path.insert(0,str(ROOT/'pydeps'))
import pandas as pd
import numpy as np
META=json.loads((OUT/'posthoc_2s_provenance.json').read_text(encoding='utf-8'))
def read(p):return pd.read_csv(p,encoding='utf-8')
def write(d,name):
    d=d.copy();d['analysis_type']='POST HOC 2-s comparison with prespecified 5-s results';d['post_hoc']=True;d['provenance_json']=json.dumps(META,separators=(',',':'));d.to_csv(OUT/name,index=False,encoding='utf-8');return d
old=read(PARENT/'regional_behavior_summary.csv');new=read(OUT/'posthoc_2s_behavior_summary.csv')
columns=['animal','session','cm_per_unit','raw_missing_fraction','missing_after_short_interpolation_fraction','run_bouts','rest_bouts','included','run_total_duration_s','rest_total_duration_s']
comparison=old[columns].merge(new[columns],on=['animal','session'],suffixes=('_prespecified_5s','_posthoc_2s'),validate='one_to_one')
for name in ['cm_per_unit','raw_missing_fraction','missing_after_short_interpolation_fraction']:
    assert np.allclose(comparison[name+'_prespecified_5s'],comparison[name+'_posthoc_2s'],rtol=0,atol=1e-14),'METHOD-RELEVANT: unchanged tracking quantity changed beyond CSV roundoff'
write(comparison,'posthoc_2s_inclusion_comparison.csv')
old=read(PARENT/'regional_across_session_statistics.csv');new=read(OUT/'posthoc_2s_across_session_statistics.csv')
keys=['analysis','animal_pool','method','outcome'];values=['n_sessions','mean_session_difference','median_session_difference','ci_low','ci_high','one_sample_t','one_sample_p','wilcoxon_statistic','wilcoxon_p','zero_differences']
write(old[keys+values].merge(new[keys+values],on=keys,suffixes=('_prespecified_5s','_posthoc_2s'),validate='one_to_one'),'posthoc_2s_across_session_comparison.csv')
old=read(PARENT/'regional_session_statistics.csv');new=read(OUT/'posthoc_2s_session_statistics.csv');keys=['analysis','animal','session','method','outcome']
values=['n_run','n_rest','run_mean','rest_mean','mean_difference','welch_t','welch_p','hedges_g','ci_low','ci_high']
write(old[keys+values].merge(new[keys+values],on=keys,suffixes=('_prespecified_5s','_posthoc_2s'),validate='one_to_one'),'posthoc_2s_shared_session_comparison.csv')
new=read(OUT/'posthoc_2s_bout_estimates.csv');counts=new.groupby(['analysis','animal','method','state','status'],dropna=False).size().reset_index(name='bouts');write(counts,'posthoc_2s_status_counts.csv')
state=read(OUT/'posthoc_2s_state_summary.csv');write(state[state.outcome=='fP_hz'][['analysis','animal','session','method','state','n_bouts','n_valid','boundary_fp_4','boundary_fp_12']],'posthoc_2s_boundary_counts.csv')
old=read(PARENT/'regional_mixed_model_coefficients.csv');new=read(OUT/'posthoc_2s_mixed_model_coefficients.csv');keys=['analysis','outcome','Name'];values=['Estimate','SE','DF','pValue','Lower','Upper']
write(old[keys+values].merge(new[keys+values],on=keys,suffixes=('_prespecified_5s','_posthoc_2s'),how='outer',validate='one_to_one'),'posthoc_2s_mixed_model_comparison.csv')
print('POST HOC comparisons complete')
