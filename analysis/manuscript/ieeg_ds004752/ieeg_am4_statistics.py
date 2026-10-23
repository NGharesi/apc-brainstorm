"""Protocol section 5; run only after completed and verified Amendment-4 estimates."""
from pathlib import Path
import json,sys,math,warnings
from datetime import datetime,timezone
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O.parent.parent/'pydeps'))
import numpy as np
import pandas as pd
from scipy import stats
SEED=20261023;B=10000
m=json.loads((O/'analysis_provenance.json').read_text(encoding='utf-8'))
stamp=dict(git_head=m['git_head'],protocol_sha256=m['protocol_sha256'],seed=SEED,provenance_file='analysis_provenance.json')
def write(d,name):
    d=d.copy();d['git_head']=m['git_head'];d['protocol_sha256']=m['protocol_sha256'];d['seed']=SEED;d['provenance_file']='analysis_provenance.json';d.to_csv(O/name,index=False,encoding='utf-8');return d
def rng():return np.random.Generator(np.random.MT19937(SEED))
def paired(v):
    x=np.asarray(v,float);x=x[np.isfinite(x)];n=len(x)
    if n==0:return dict(n_patients=0,median_difference=np.nan,mean_difference=np.nan,wilcoxon_statistic=np.nan,p_two_sided=np.nan,ci_low=np.nan,ci_high=np.nan)
    if np.all(x==0):w,p=0.,1.
    else:w,p=stats.wilcoxon(x,zero_method='wilcox',alternative='two-sided',method='auto')
    boot=np.median(x[rng().integers(0,n,size=(B,n))],axis=1);lo,hi=np.percentile(boot,[2.5,97.5])
    return dict(n_patients=n,median_difference=float(np.median(x)),mean_difference=float(np.mean(x)),wilcoxon_statistic=float(w),p_two_sided=float(p),ci_low=float(lo),ci_high=float(hi))
def icc_from_moments(n,s,q):
    n=np.asarray(n);s=np.asarray(s);q=np.asarray(q);N=n.sum(axis=-1);k=n.shape[-1]
    with np.errstate(divide='ignore',invalid='ignore'):
        msb=(np.sum(s*s/n,axis=-1)-np.sum(s,axis=-1)**2/N)/(k-1)
        msw=(np.sum(q-s*s/n,axis=-1))/(N-k)
        k0=(N-np.sum(n*n,axis=-1)/N)/(k-1)
        return (msb-msw)/(msb+(k0-1)*msw)
assert np.isclose(icc_from_moments([2,2],[3,9],[5,41]),8.5/9.5)
assert not (O/'METHOD_STOP_FLAG.json').exists()
assert json.loads((O/'am4_pipeline_runtime.json').read_text(encoding='utf-8'))['status']=='COMPLETE'
assert not (O/'ieeg_statistics.csv').exists(),'Endpoint statistics already exist; do not rerun'
d=pd.read_csv(O/'ieeg_trial_estimates.csv',encoding='utf-8');I=pd.read_csv(O/'trial_inclusion_amendment4.csv',encoding='utf-8');I=I[I.included.astype(bool)]
keys=['analysis','patient','session','trial','method'];assert not d.duplicated(keys).any();assert len(d)==5*len(I)==m['total_method_rows']
assert d.groupby(['analysis','patient','session','trial']).size().eq(5).all()
assert d.protocol_sha256.eq(m['protocol_sha256']).all()
d['valid']=d.status.eq(0)&np.isfinite(d.score)
for _,g in d.groupby(['analysis','method']):assert g.valid.mean()>=.5,'Most trials invalid; stop'
methods=['APC-v1.0','MVL-raw','MVL-Ozkurt','KLMI','GLM'];sr=[];rates=[];pr=[]
for (a,p,s,method),g in d.groupby(['analysis','patient','session','method'],sort=True):
    z=g[g.valid];sr.append(dict(analysis=a,patient=p,session=s,method=method,n_trials=len(g),n_valid=len(z),n_invalid=len(g)-len(z),mean_fP_hz=z.fP_hz.mean(),sd_fP_hz=z.fP_hz.std(ddof=1),mean_fA_hz=z.fA_hz.mean(),sd_fA_hz=z.fA_hz.std(ddof=1),mean_ozkurt_mvl=z.ozkurt_mvl.mean(),mean_raw_mvl=z.raw_mvl.mean(),native_fs_hz=int(g.native_fs_hz.iloc[0])))
S=write(pd.DataFrame(sr),'ieeg_session_summary.csv')
for (a,p,method),g in S.groupby(['analysis','patient','method'],sort=True):
    z=g[np.isfinite(g.mean_fP_hz)];pr.append(dict(analysis=a,patient=p,method=method,n_sessions=len(g),n_valid_sessions=len(z),n_trials=int(g.n_trials.sum()),n_valid_trials=int(g.n_valid.sum()),across_session_sd_fP_hz=z.mean_fP_hz.std(ddof=1),mean_within_session_sd_fP_hz=g.sd_fP_hz.mean(),patient_mean_fP_hz=z.mean_fP_hz.mean(),native_fs_hz=int(g.native_fs_hz.iloc[0])))
P=write(pd.DataFrame(pr),'ieeg_patient_summary.csv')
for (a,method),g in d.groupby(['analysis','method'],sort=True):
    valid=g.valid;fp=g.boundary_fp_low.astype(bool)|g.boundary_fp_high.astype(bool);fa=g.boundary_fa_low.astype(bool)|g.boundary_fa_high.astype(bool)
    rates.append(dict(analysis=a,method=method,n_patients=g.patient.nunique(),n_sessions=len(g[['patient','session']].drop_duplicates()),n_trials=len(g),n_valid=int(valid.sum()),failure_count=int((~valid).sum()),failure_rate=float((~valid).mean()),fp_low=int(g.boundary_fp_low.sum()),fp_high=int(g.boundary_fp_high.sum()),fa_low=int(g.boundary_fa_low.sum()),fa_high=int(g.boundary_fa_high.sum()),fp_boundary_rate_all=float(fp.mean()),fp_boundary_count_valid=int((fp&valid).sum()),fp_boundary_rate_valid=float(fp[valid].mean()),fa_boundary_count_valid=int((fa&valid).sum()),fa_boundary_rate_valid=float(fa[valid].mean()),status_counts=json.dumps({str(k):int(v) for k,v in g.status.value_counts().sort_index().items()})))
R=write(pd.DataFrame(rates),'ieeg_failure_boundary_rates.csv')
out=[];paired_rows=[]
def contrast(a,comp,field,endpoint,native=False):
    pp=P[P.analysis.eq(a)&P.method.isin(['APC-v1.0',comp])].copy()
    if native:pp=pp[pp.native_fs_hz.eq(2000)]
    wide=pp.pivot(index='patient',columns='method',values=field).dropna(subset=['APC-v1.0',comp]);diff=wide['APC-v1.0']-wide[comp]
    z=paired(diff);pats=set(wide.index);sub=S[S.analysis.eq(a)&S.patient.isin(pats)&S.method.isin(['APC-v1.0',comp])];tr=d[d.analysis.eq(a)&d.patient.isin(pats)]
    r=dict(analysis='native2000_primary' if native else a,endpoint=endpoint,comparator=comp,n_sessions=len(sub[['patient','session']].drop_duplicates()),n_trials=len(tr[['patient','session','trial']].drop_duplicates()),n_valid_apc_trials=int(tr[tr.method.eq('APC-v1.0')].valid.sum()),n_valid_comparator_trials=int(tr[tr.method.eq(comp)].valid.sum()),**z)
    r['decision']=''
    if endpoint=='across_session_sd_fP':r['decision']='APC is more reproducible.' if z['ci_high']<0 else 'APC is less reproducible.' if z['ci_low']>0 else 'No difference shown.'
    out.append(r)
    for p,row in wide.iterrows():paired_rows.append(dict(analysis=r['analysis'],endpoint=endpoint,comparator=comp,patient=p,APC_value=row['APC-v1.0'],scan_value=row[comp],difference=row['APC-v1.0']-row[comp]))
for a in ['primary','artifact_only','referential']:
    for comp in methods[1:]:
        contrast(a,comp,'across_session_sd_fP_hz','across_session_sd_fP')
        contrast(a,comp,'mean_within_session_sd_fP_hz','within_session_sd_fP')
contrast('primary','MVL-Ozkurt','across_session_sd_fP_hz','across_session_sd_fP',native=True)
T=write(pd.DataFrame(out),'ieeg_statistics.csv');write(pd.DataFrame(paired_rows),'ieeg_patient_paired_differences.csv')
iccs=[]
for (a,method),g in S.groupby(['analysis','method'],sort=True):
    gg=g[np.isfinite(g.mean_fP_hz)].groupby('patient',sort=True).mean_fP_hz
    arrays=[np.asarray(x,float) for _,x in gg];n=np.array([len(x) for x in arrays]);s=np.array([x.sum() for x in arrays]);q=np.array([(x*x).sum() for x in arrays]);idx=rng().integers(0,len(n),size=(B,len(n)));boot=icc_from_moments(n[idx],s[idx],q[idx]);good=np.isfinite(boot);lo,hi=np.percentile(boot[good],[2.5,97.5])
    iccs.append(dict(analysis=a,method=method,n_patients=len(n),n_sessions=int(n.sum()),n_trials=int(g.n_trials.sum()),ICC1=float(icc_from_moments(n,s,q)),ci_low=float(lo),ci_high=float(hi),finite_bootstrap_replicates=int(good.sum()),bootstrap_replicates=B))
write(pd.DataFrame(iccs),'ieeg_ICC.csv')
SP=pd.read_csv(O/'am4_session_spectral_peaks.csv',encoding='utf-8');dominant=S[S.method.eq('APC-v1.0')].merge(SP[['analysis','patient','session','spectral_peak_hz']],on=['analysis','patient','session'],validate='one_to_one');dominant['absolute_peak_difference_hz']=(dominant.mean_fP_hz-dominant.spectral_peak_hz).abs();dominant['within_1_hz']=dominant.absolute_peak_difference_hz.le(1)&dominant.mean_fP_hz.notna();write(dominant,'ieeg_dominant_rhythm_sessions.csv')
ds=[]
for a,g in dominant.groupby('analysis',sort=True):
    z=g[np.isfinite(g.mean_fP_hz)&np.isfinite(g.spectral_peak_hz)];rho,p=stats.spearmanr(z.mean_fP_hz,z.spectral_peak_hz);ds.append(dict(analysis=a,n_patients=z.patient.nunique(),n_sessions=len(z),n_trials=int(z.n_trials.sum()),within_1_hz=int(z.within_1_hz.sum()),proportion_within_1_hz=float(z.within_1_hz.mean()),spearman_rho=float(rho),p_two_sided=float(p)))
write(pd.DataFrame(ds),'ieeg_dominant_rhythm_statistics.csv')
X=d[d.analysis.eq('primary')&d.method.eq('APC-v1.0')&d.valid][['patient','session','trial','SetSize','Correct','fP_hz','ozkurt_mvl']];write(X,'am4_exploratory_model_inputs.csv')
primary=T[T.analysis.eq('primary')&T.endpoint.eq('across_session_sd_fP')&T.comparator.eq('MVL-Ozkurt')].iloc[0].to_dict()
(O/'am4_statistics_runtime.json').write_text(json.dumps(dict(status='COMPLETE',finished_utc=datetime.now(timezone.utc).isoformat(),primary=primary,implementation=m['statistics_implementation'],ICC_balanced_validation=float(8.5/9.5),provenance=stamp),indent=2),encoding='utf-8')
print(json.dumps(primary),flush=True)
