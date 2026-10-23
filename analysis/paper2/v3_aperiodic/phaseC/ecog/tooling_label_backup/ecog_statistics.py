"""Prespecified section-8 endpoints; no estimator calls, fixed patient bootstrap."""
from pathlib import Path
import sys,json
O=Path(__file__).resolve().parent;sys.path.insert(0,str(Path(r'C:\Users\nghare\.brainstorm\process\pydeps')))
import pandas as pd
import numpy as np
from scipy import stats
SEED=20261024;NBOOT=10000;methods=['APC-v3.0']
m=json.loads((O/'analysis_provenance.json').read_text(encoding='utf-8'))
def write(d,n):
    d=d.copy();d['git_head']=m['git_head'];d['protocol_sha256']=m['protocol_sha256'];d['seed']=SEED;d['provenance_file']='analysis_provenance.json';d.to_csv(O/n,index=False,encoding='utf-8');return d
def rng():return np.random.Generator(np.random.MT19937(SEED))
def test(x,central='mean'):
    x=np.asarray(x,float);x=x[np.isfinite(x)];n=len(x)
    if n<2:return dict(n_patients=n,mean_difference=np.nan,median_difference=np.nan,t_statistic=np.nan,t_df=max(0,n-1),t_p_two_sided=np.nan,wilcoxon_statistic=np.nan,wilcoxon_p_two_sided=np.nan,ci_low=np.nan,ci_high=np.nan,decision='Not estimable')
    t=stats.ttest_1samp(x,0) if central=='mean' else None;w,p=(0.,1.) if np.all(x==0) else stats.wilcoxon(x,alternative='two-sided',zero_method='wilcox',method='auto')
    samples=x[rng().integers(0,n,size=(NBOOT,n))];boot=samples.mean(axis=1) if central=='mean' else np.median(samples,axis=1);lo,hi=np.percentile(boot,[2.5,97.5]);decision='Supported' if hi<0 else 'Opposite' if lo>0 else 'Not shown'
    return dict(n_patients=n,mean_difference=float(x.mean()),median_difference=float(np.median(x)),t_statistic=float(t.statistic) if t is not None else np.nan,t_df=n-1 if t is not None else np.nan,t_p_two_sided=float(t.pvalue) if t is not None else np.nan,wilcoxon_statistic=float(w),wilcoxon_p_two_sided=float(p),ci_low=float(lo),ci_high=float(hi),decision=decision)
assert not (O/'STOP_METHOD').exists();assert json.loads((O/'estimates_runtime.json').read_text(encoding='utf-8'))['status']=='COMPLETE';assert not (O/'ecog_statistics.csv').exists()
B=pd.read_csv(O/'bouts.csv',encoding='utf-8');B=B[B.analysed.astype(bool)];E=pd.read_csv(O/'electrodes.csv',encoding='utf-8');E['flagged']=E.flagged.astype(bool)
counts=B[B.recording=='movement'].groupby(['patient','state']).size().unstack(fill_value=0);eligible=counts[(counts.get('move',0)>=10)&(counts.get('rest',0)>=10)].index;assert len(eligible)==18 and 'jf' not in eligible
elig=pd.DataFrame(dict(patient=counts.index,move_bouts=counts.get('move',0),rest_bouts=counts.get('rest',0))).reset_index(drop=True);elig['eligible']=elig.patient.isin(eligible);write(elig,'patient_eligibility.csv')
d=pd.concat([pd.read_csv(O/f'estimates_w{k}.csv',encoding='utf-8') for k in range(1,5)],ignore_index=True);keys=['patient','recording','bout','method'];assert len(d)==2648*6 and not d.duplicated(keys).any();assert d.groupby(['patient','recording','bout']).size().eq(6).all();assert set(map(tuple,d[['patient','recording','bout']].drop_duplicates().to_numpy()))==set(map(tuple,B[['patient','recording','bout']].to_numpy()))
d=d.drop(columns='n_bursts').merge(pd.read_csv(O/'bout_burst_counts.csv',encoding='utf-8')[['patient','recording','bout','n_bursts']],on=['patient','recording','bout'],validate='many_to_one');d.loc[d.method.ne('APC-v3.0'),'n_bursts']=np.nan;d['eligible_patient']=d.patient.isin(eligible);d['valid']=d.status.eq(0)&np.isfinite(d.score);d=d.merge(E[['patient','flagged']],on='patient',validate='many_to_one')
for method,g in d.groupby('method'):assert g.valid.mean()>=.5,'Method-relevant majority failure'
d=write(d.sort_values(['patient','recording','bout','method']),'ecog_bout_estimates.csv')
rates=[]
for (rec,method,state),g in d.groupby(['recording','method','state'],sort=True):
    fp=g.boundary_fp_low.astype(bool)|g.boundary_fp_high.astype(bool);fa=g.boundary_fa_low.astype(bool)|g.boundary_fa_high.astype(bool);v=g.valid
    rates.append(dict(recording=rec,method=method,state=state,n_patients=g.patient.nunique(),n_bouts=len(g),n_valid=int(v.sum()),failure_count=int((~v).sum()),failure_rate=float((~v).mean()),status_counts=json.dumps({str(k):int(z) for k,z in g.status.value_counts().sort_index().items()}),fp_low=int(g.boundary_fp_low.sum()),fp_high=int(g.boundary_fp_high.sum()),fa_low=int(g.boundary_fa_low.sum()),fa_high=int(g.boundary_fa_high.sum()),fp_boundary_rate_all=float(fp.mean()),fp_boundary_rate_valid=float(fp[v].mean()),fa_boundary_rate_valid=float(fa[v].mean())))
write(pd.DataFrame(rates),'status_boundary_rates.csv')
rows=[]
subsets={'prespecified':d[d.eligible_patient], 'sensitivity_a':d[d.eligible_patient&~d.flagged]}
for subset,D in subsets.items():
    for (pt,rec,method,state),g in D.groupby(['patient','recording','method','state'],sort=True):
        v=g[g.valid];rows.append(dict(subset=subset,patient=pt,recording=rec,method=method,state=state,n_bouts=len(g),n_valid=len(v),mean_fP_hz=v.fP_hz.mean(),median_fP_hz=v.fP_hz.median(),sd_fP_hz=v.fP_hz.std(ddof=1),mean_fA_hz=v.fA_hz.mean(),mean_ozkurt_mvl=v.ozkurt_mvl.mean(),fp_boundary_rate=float((g.boundary_fp_low.astype(bool)|g.boundary_fp_high.astype(bool)).mean())))
P=write(pd.DataFrame(rows),'ecog_patient_summary.csv');tests=[];patient_diffs=[]
def state_contrast(subset,rec,method,field,endpoint,direction=True,subtype=None):
    if subtype:
        D=subsets[subset];D=D[D.recording.eq(rec)&D.method.eq(method)&D.valid&((D.state=='rest')|(D.movement_type==subtype))]
        wide=D.groupby(['patient','state'])[field].mean().unstack();wide=wide.reindex(columns=['move','rest']).dropna();diff=wide.move-wide.rest
    else:
        D=subsets[subset];Q=P[(P.subset==subset)&(P.recording==rec)&(P.method==method)];wide=Q.pivot(index='patient',columns='state',values=field).reindex(columns=['move','rest']).dropna();diff=wide.move-wide.rest
    z=test(diff);patients=set(wide.index);used=D[D.patient.isin(patients)&D.recording.eq(rec)&D.method.eq(method)]
    if subtype:used=used[(used.state=='rest')|(used.movement_type==subtype)]
    if not direction and z['decision']!='Not estimable':z['decision']='Descriptive'
    label=endpoint+(f'_{subtype}' if subtype else '');tests.append(dict(subset=subset,recording=rec,endpoint=label,method=method,contrast='move minus rest',bootstrap_statistic='mean',n_bouts=len(used),n_valid_bouts=int(used.valid.sum()),n_move_valid=int((used.valid&used.state.eq('move')).sum()),n_rest_valid=int((used.valid&used.state.eq('rest')).sum()),**z))
    for pt,row in wide.iterrows():patient_diffs.append(dict(subset=subset,recording=rec,endpoint=label,method=method,patient=pt,move_value=row['move'],rest_value=row['rest'],difference=row['move']-row['rest']))
for subset in subsets:
    for method in methods:
        state_contrast(subset,'movement',method,'mean_ozkurt_mvl','coupling_state')
    Q=P[(P.subset==subset)&(P.recording=='movement')&P.method.isin(['APC-v3.0','MVL-Ozkurt'])];wide=Q.pivot(index=['patient','method'],columns='state',values='sd_fP_hz').reindex(columns=['move','rest']);wide['mean_state_sd']=wide[['move','rest']].mean(axis=1,skipna=False);W=wide.mean_state_sd.unstack('method').reindex(columns=['APC-v3.0','MVL-Ozkurt']).dropna();z=test(W['APC-v3.0']-W['MVL-Ozkurt'],central='median');D=subsets[subset];used=D[D.patient.isin(W.index)&D.recording.eq('movement')&D.method.eq('APC-v3.0')];tests.append(dict(subset=subset,recording='movement',endpoint='within_state_fP_SD',method='APC-v1.0 minus MVL-Ozkurt',contrast='APC minus scan',bootstrap_statistic='median',n_bouts=len(used),n_valid_bouts=int(used.valid.sum()),n_move_valid=int((used.valid&used.state.eq('move')).sum()),n_rest_valid=int((used.valid&used.state.eq('rest')).sum()),**z))
    for pt,row in W.iterrows():patient_diffs.append(dict(subset=subset,recording='movement',endpoint='within_state_fP_SD',method='APC-v1.0 minus MVL-Ozkurt',patient=pt,move_value=np.nan,rest_value=np.nan,APC_value=row['APC-v3.0'],scan_value=row['MVL-Ozkurt'],difference=row['APC-v3.0']-row['MVL-Ozkurt']))
T=write(pd.DataFrame(tests),'ecog_statistics.csv');write(pd.DataFrame(patient_diffs),'patient_differences.csv')
spectra=pd.read_csv(O/'analysed_rest_spectral_peaks.csv',encoding='utf-8');rest=P[P.state.eq('rest')].merge(spectra[['patient','recording','rest_spectral_peak_hz']],on=['patient','recording'],validate='many_to_one');rest['in_12_20_hz']=rest.median_fP_hz.between(12,20);rest['within_2_hz_of_spectrum']=(rest.median_fP_hz-rest.rest_spectral_peak_hz).abs().le(2);write(rest,'rest_frequency_patient_table.csv')
rr=[]
for (subset,rec,method),g in rest.groupby(['subset','recording','method'],sort=True):
    v=g[g.median_fP_hz.notna()];rr.append(dict(subset=subset,recording=rec,method=method,n_patients=len(v),n_bouts=int(v.n_bouts.sum()),n_valid_bouts=int(v.n_valid.sum()),patients_in_12_20_hz=int(v.in_12_20_hz.sum()),proportion_in_12_20_hz=float(v.in_12_20_hz.mean()),patients_within_2_hz=int(v.within_2_hz_of_spectrum.sum()),proportion_within_2_hz=float(v.within_2_hz_of_spectrum.mean())))
write(pd.DataFrame(rr),'rest_frequency_statistics.csv')
M=d[d.eligible_patient&d.recording.eq('movement')&d.method.eq('APC-v3.0')&d.valid][['patient','state','bout','ozkurt_mvl']];write(M,'mixed_model_inputs.csv')
ci=[]
for pt,g in M.groupby('patient',sort=True):
    a=g[g.state=='move'].ozkurt_mvl.to_numpy();b=g[g.state=='rest'].ozkurt_mvl.to_numpy();r=rng();boot=a[r.integers(0,len(a),size=(NBOOT,len(a)))].mean(axis=1)-b[r.integers(0,len(b),size=(NBOOT,len(b)))].mean(axis=1);lo,hi=np.percentile(boot,[2.5,97.5]);ci.append(dict(patient=pt,n_move=len(a),n_rest=len(b),difference=a.mean()-b.mean(),ci_low=lo,ci_high=hi))
write(pd.DataFrame(ci),'figure_patient_coupling_CIs.csv')
result=dict(status='COMPLETE',git_head=m['git_head'],protocol_sha256=m['protocol_sha256'],seed=SEED,bootstrap_resamples=NBOOT,bootstrap_rng='NumPy MT19937, reset to seed per endpoint; fixed patient resampling',wilcoxon='two-sided, zero_method wilcox, method auto',SD_ddof=1,eligibility_patients=len(eligible),bout_estimates=len(d),primary_rows=T[(T.subset=='prespecified')&((T.endpoint=='within_state_fP_SD')|((T.endpoint=='coupling_state')&(T.method=='APC-v3.0')))].to_dict('records'))
(O/'statistics_runtime.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result),flush=True)
