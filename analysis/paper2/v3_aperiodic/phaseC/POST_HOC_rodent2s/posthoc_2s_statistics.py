"""POST HOC 2-s statistics; same estimators and seed scheme as 5-s pipeline."""
from pathlib import Path
import sys, json, hashlib, warnings, time
ROOT=Path(r'C:\Users\nghare\.brainstorm\process'); OUT=Path(__file__).resolve().parent; PARENT=OUT
sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
import pandas as pd
from scipy import stats, special

def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
assert read(PARENT/'regional_xml_grouping.json')['contiguous_eight_channel_blocks'], 'XML grouping failed'
assert read(OUT/'posthoc_2s_bouts_runtime.json')['status']=='COMPLETE', 'Regional bout analysis incomplete'
started=time.perf_counter()
data=pd.read_csv(OUT/'posthoc_2s_bout_estimates.csv',encoding='utf-8')
metadata=read(OUT/'posthoc_2s_provenance.json')|{
    'stage':'POST HOC 2-s regional statistics','seed':20261022,'bootstrap_resamples':10000,
    'source_csv':'posthoc_2s_bout_estimates.csv','source_csv_sha256':sha(OUT/'posthoc_2s_bout_estimates.csv'),
    'hedges_correction':'gamma(df/2)/(sqrt(df/2)*gamma((df-1)/2)); pooled SD',
    'bootstrap':'resample original bouts independently by state, share indices across methods; nanmean',
    'spread':'sample SD; linear quantile IQR; unscaled median absolute deviation'}
provenance=json.dumps(metadata,separators=(',',':'))
test_warnings=[]
def call_test(function,context):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        result=function()
    for warning in caught:
        test_warnings.append(context|{'warning_category':warning.category.__name__,'warning_message':str(warning.message)})
    return result

def write(rows,name):
    frame=pd.DataFrame(rows);frame['analysis_type']=metadata['analysis_type'];frame['post_hoc']=True;frame['minimum_bout_s']=2;frame['git_commit']=metadata['git_commit'];frame['provenance_json']=provenance
    frame.to_csv(OUT/('posthoc_2s_'+name),index=False,encoding='utf-8');return frame

def hedges(x,y):
    n,m=len(x),len(y);df=n+m-2
    if min(n,m)<2:return np.nan
    sd=np.sqrt(((n-1)*np.var(x,ddof=1)+(m-1)*np.var(y,ddof=1))/df)
    if sd<=0:return np.nan
    j=np.exp(special.gammaln(df/2)-.5*np.log(df/2)-special.gammaln((df-1)/2))
    return j*(x.mean()-y.mean())/sd

def signed_rank(x):
    x=np.asarray(x);x=x[np.isfinite(x)]
    if not len(x):return np.nan,np.nan,0,0
    nz=x[x!=0]
    if not len(nz):return 0.,1.,len(x),0
    r=stats.wilcoxon(x,zero_method='wilcox',alternative='two-sided',method='auto')
    return r.statistic,r.pvalue,len(x),len(nz)

session_rows=[];state_rows=[];spread=[]
for group_index,((analysis,animal,session),group) in enumerate(data.groupby(['analysis','animal','session'],sort=True)):
    states={state:np.sort(group.loc[group.state==state,'bout'].unique()) for state in ['run','rest']}
    rng=np.random.default_rng(np.random.SeedSequence([20261022,group_index]))
    indices={state:rng.integers(len(ids),size=(10000,len(ids))) for state,ids in states.items()}
    for method,mg in group.groupby('method',sort=True):
        values={state:mg[mg.state==state].set_index('bout').reindex(ids) for state,ids in states.items()}
        for variable in ['fP_hz','fA_hz','ozkurt_mvl']:
            arr={s:v[variable].to_numpy(float) for s,v in values.items()}
            finite={s:v[np.isfinite(v)] for s,v in arr.items()}
            a,b=finite['run'],finite['rest'];test=call_test(lambda:stats.ttest_ind(a,b,equal_var=False),dict(scope='session Welch',analysis=analysis,animal=animal,session=session,method=method,outcome=variable)) if min(len(a),len(b))>=2 else None
            with warnings.catch_warnings():
                warnings.simplefilter('ignore',RuntimeWarning)
                boot={s:np.nanmean(v[indices[s]],axis=1) for s,v in arr.items()}
            diff=boot['run']-boot['rest'];valid=diff[np.isfinite(diff)]
            ci=np.quantile(valid,[.025,.975]) if len(valid) else [np.nan,np.nan]
            session_rows.append(dict(analysis=analysis,animal=animal,session=session,method=method,outcome=variable,
                n_run=len(a),n_rest=len(b),run_mean=np.mean(a) if len(a) else np.nan,rest_mean=np.mean(b) if len(b) else np.nan,
                mean_difference=np.mean(a)-np.mean(b) if len(a) and len(b) else np.nan,
                welch_t=test.statistic if test else np.nan,welch_df=test.df if test else np.nan,welch_p=test.pvalue if test else np.nan,
                hedges_g=hedges(a,b),ci_low=ci[0],ci_high=ci[1],bootstrap_valid_resamples=len(valid),bootstrap_stream=group_index))
            for state,v in finite.items():
                bs=boot[state];bs=bs[np.isfinite(bs)];bounds=np.quantile(bs,[.025,.975]) if len(bs) else [np.nan,np.nan]
                state_rows.append(dict(analysis=analysis,animal=animal,session=session,method=method,outcome=variable,state=state,
                    n_valid=len(v),n_bouts=len(arr[state]),mean=np.mean(v) if len(v) else np.nan,median=np.median(v) if len(v) else np.nan,
                    ci_low=bounds[0],ci_high=bounds[1],boundary_fp_4=int((values[state].fP_hz==4).sum()),boundary_fp_12=int((values[state].fP_hz==12).sum())))
        for state,v in values.items():
            fp=v.fP_hz.to_numpy(float);fp=fp[np.isfinite(fp)]
            spread.append(dict(analysis=analysis,animal=animal,session=session,method=method,state=state,n_valid=len(fp),
                fp_sd=np.std(fp,ddof=1) if len(fp)>1 else np.nan,
                fp_iqr=np.diff(np.quantile(fp,[.25,.75]))[0] if len(fp) else np.nan,
                fp_mad=np.median(abs(fp-np.median(fp))) if len(fp) else np.nan))
session_table=write(session_rows,'session_statistics.csv');write(state_rows,'state_summary.csv');spread_table=write(spread,'within_state_fp_spread.csv')

across=[]
for (analysis,method,outcome),g in session_table.groupby(['analysis','method','outcome'],sort=True):
    for pool in ['EC012','EC013','pooled']:
        rows=g if pool=='pooled' else g[g.animal==pool];x=rows.mean_difference.to_numpy(float);x=x[np.isfinite(x)]
        t=call_test(lambda:stats.ttest_1samp(x,0),dict(scope='across-session one-sample t',analysis=analysis,animal=pool,session='',method=method,outcome=outcome)) if len(x)>1 else None
        w,p,n,nz=signed_rank(x);sem=stats.sem(x) if len(x)>1 else np.nan
        ci=stats.t.interval(.95,len(x)-1,loc=np.mean(x),scale=sem) if len(x)>1 and sem>0 else [np.nan,np.nan]
        across.append(dict(analysis=analysis,animal_pool=pool,method=method,outcome=outcome,n_sessions=len(x),
            mean_session_difference=np.mean(x) if len(x) else np.nan,median_session_difference=np.median(x) if len(x) else np.nan,
            ci_low=ci[0],ci_high=ci[1],one_sample_t=t.statistic if t else np.nan,one_sample_df=len(x)-1,one_sample_p=t.pvalue if t else np.nan,
            wilcoxon_statistic=w,wilcoxon_p=p,zero_differences=n-nz))
write(across,'across_session_statistics.csv')
paired=[]
for (analysis,animal,session,state),g in spread_table.groupby(['analysis','animal','session','state'],sort=True):
    reference=g[g.method=='APC-v3.0']
    if len(reference)!=1:continue
    a=reference.iloc[0]
    for _,b in g[g.method!='APC-v3.0'].iterrows():
        for metric in ['fp_sd','fp_iqr','fp_mad']:
            paired.append(dict(analysis=analysis,animal=animal,session=session,state=state,scan=b.method,spread_metric=metric,
                apc_spread=a[metric],scan_spread=b[metric],apc_minus_scan=a[metric]-b[metric]))
paired_table=write(paired,'within_state_spread_comparisons.csv');pooled=[]
for (analysis,state,scan,metric),g in paired_table.groupby(['analysis','state','scan','spread_metric']):
    for pool in ['EC012','EC013','pooled']:
        v=g if pool=='pooled' else g[g.animal==pool];x=v.apc_minus_scan.to_numpy(float);x=x[np.isfinite(x)]
        w,p,n,nz=signed_rank(x)
        pooled.append(dict(analysis=analysis,animal_pool=pool,state=state,scan=scan,spread_metric=metric,n_sessions=n,
            mean_apc_minus_scan=np.mean(x) if n else np.nan,median_apc_minus_scan=np.median(x) if n else np.nan,
            wilcoxon_statistic=w,wilcoxon_p=p,zero_differences=n-nz))
write(pooled,'across_session_spread_comparisons.csv')
write(test_warnings,'statistics_warnings.csv')
runtime={'status':'COMPLETE','elapsed_seconds':time.perf_counter()-started,'session_statistics':len(session_rows),'statistical_warnings':len(test_warnings),'metadata':metadata}
(OUT/'posthoc_2s_statistics_runtime.json').write_text(json.dumps(runtime,indent=2),encoding='utf-8')
print(json.dumps(runtime))
