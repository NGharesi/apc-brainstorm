from pathlib import Path
from datetime import datetime,timezone
import sys,os,json,hashlib,time,ast,warnings
os.environ.setdefault('OPENBLAS_NUM_THREADS','2');os.environ.setdefault('OMP_NUM_THREADS','2')
O=Path(__file__).resolve().parent;R=O.parent.parent;sys.path.insert(0,str(R/'pydeps'))
import numpy as np
import pandas as pd
import h5py
from scipy import stats,special
P=json.loads((O/'provenance.json').read_text(encoding='utf-8'))
METHODS=[f'{f}_{a}' for f in ['F1','F2','F3'] for a in ['A_APC','A_SCAN','A_EVENT']]+['A2_prime_2D','APC-v1.0','APC-v3.0']
def read(p):return pd.read_csv(p,encoding='utf-8',float_precision='round_trip')
def write(d,name):
 if not isinstance(d,pd.DataFrame):d=pd.DataFrame(d)
 d=d.copy();d['git_commit']=P['git_head'];d['protocol_sha256']=P['protocol_sha256'];d['provenance_file']='provenance.json';d.to_csv(O/name,index=False,encoding='utf-8',float_format='%.17g');return d
def jw(name,v):(O/name).write_text(json.dumps(v,indent=2,allow_nan=True)+'\n',encoding='utf-8')
def wilson(k,n):
 if not n:return np.nan,np.nan
 z=stats.norm.ppf(.975);p=k/n;den=1+z*z/n;c=(p+z*z/(2*n))/den;h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den;return max(0,c-h),min(1,c+h)
def mcn(a,b):
 a=np.asarray(a,bool);b=np.asarray(b,bool);n10=int((a&~b).sum());n01=int((~a&b).sum());n=n10+n01
 first=int(a.sum());second=int(b.sum());fl,fh=wilson(first,len(a));sl,sh=wilson(second,len(a))
 return dict(n=len(a),first_success=first,first_ci_low=fl,first_ci_high=fh,second_success=second,second_ci_low=sl,second_ci_high=sh,both=int((a&b).sum()),only_first=n10,only_second=n01,neither=int((~a&~b).sum()),p_value=1. if n==0 else float(stats.binomtest(n10,n,.5).pvalue))
def holm(p):
 p=np.asarray(p);idx=np.argsort(p);z=np.maximum.accumulate(p[idx]*np.arange(len(p),0,-1));r=np.empty(len(p));r[idx]=np.minimum(z,1);return r
def joint(g,tol=1):return (g.valid.astype(bool)&(abs(g.recovered_fp_hz-g.true_fp_hz)<=tol)&(abs(g.recovered_fa_hz-g.true_fa_hz)<=8)).to_numpy()
def metrics(g):
 ep=abs(g.recovered_fp_hz-g.true_fp_hz);ea=abs(g.recovered_fa_hz-g.true_fa_hz);valid=g.valid.astype(bool)
 row=dict(n=len(g),valid=int(valid.sum()),failures=int((~valid).sum()),joint=int(joint(g).sum()),strict_joint=int(joint(g,.5).sum()),fp_only=int((valid&(ep<=1)).sum()),fa_only=int((valid&(ea<=8)).sum()),mean_abs_fp_error=float(ep.mean()),median_abs_fp_error=float(ep.median()),mean_abs_fa_error=float(ea.mean()),median_abs_fa_error=float(ea.median()),finite_fp=int(ep.notna().sum()),finite_fa=int(ea.notna().sum()))
 for name in ['joint','strict_joint','fp_only','fa_only']:row[name+'_rate']=row[name]/len(g);row[name+'_ci_low'],row[name+'_ci_high']=wilson(row[name],len(g))
 return row
def boot_auc(c,n,B):
 vc=np.isfinite(c);vn=np.isfinite(n);mask=vc[:,None]&vn[None,:];W=np.where(mask,(c[:,None]>n[None,:])+.5*(c[:,None]==n[None,:]),0.)
 den=vc.sum()*vn.sum();point=float(W.sum()/den) if den else np.nan
 denom=(B@vc.astype(float))*(B@vn.astype(float));reps=np.divide(np.sum((B@W)*B,axis=1),denom,out=np.full(len(B),np.nan),where=denom>0)
 return point,reps,int(vc.sum()),int(vn.sum()),int((vc&vn).sum())
def table_method(g,method):return g[g.method==method].set_index('key').sort_index()

# Use the original rodent statistics helper definitions verbatim.
rodent_script=R/'revision_checks/rodent_multi/compute_rodent_statistics.py'
source=rodent_script.read_text(encoding='utf-8');tree=ast.parse(source);nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['hedges','signed_rank']]
assert len(nodes)==2
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(rodent_script),'exec'),globals())

def simulations():
 frames=[]
 for suite,n in [('V1',350),('V2',900),('V3',600),('V4',25)]:
  d=pd.concat([read(O/f'{suite}_worker{w}.csv') for w in range(1,5)],ignore_index=True)
  assert d.key.nunique()==n and not d.duplicated(['key','method']).any() and (d.groupby('key').size()==12).all() and set(d.method)==set(METHODS)
  assert (d.git_commit==P['git_head']).all() and (d.protocol_sha256==P['protocol_sha256']).all();d['valid']=d.valid.astype(bool);frames.append(d);write(d,f'{suite}_trial_estimates.csv')
 sim=pd.concat(frames,ignore_index=True);write(sim,'simulation_trial_estimates.csv')
 consistency=[]
 for suite,g in sim.groupby('suite',sort=False):
  for source,ref in [('F1_A_APC','APC-v1.0'),('F2_A_APC','APC-v3.0')]:
   a=table_method(g,source);b=table_method(g,ref).reindex(a.index);q=dict(suite=suite,pipeline=source,reference=ref,n=len(a))
   for col in ['recovered_fp_hz','recovered_fa_hz','raw_mvl','coupling']:
    same=(a[col]==b[col])|(a[col].isna()&b[col].isna());assert same.all();q[col+'_identical']=int(same.sum())
   q['status_identical']=int((a.status==b.status).sum());consistency.append(q)
 write(consistency,'endtoend_agreement.csv')
 rows=[]
 for keys,g in sim.groupby(['suite','scenario','dataset','beta','level','duration_s','method'],dropna=False,sort=False):rows.append(dict(zip(['suite','scenario','dataset','beta','level','duration_s','method'],keys))|metrics(g))
 write(rows,'recovery_by_level.csv');overall=[]
 for (suite,method),g in sim[sim.dataset=='coupled'].groupby(['suite','method'],sort=False):overall.append(dict(suite=suite,method=method)|metrics(g))
 write(overall,'recovery_overall.csv')
 pa=[];pb=[];pc=[];decisions=[]
 for suite in ['V1','V2']:
  d=sim[(sim.suite==suite)&(sim.dataset=='coupled')];a=table_method(d,'F3_A_SCAN')
  for ref in ['APC-v1.0','A2_prime_2D']:
   b=table_method(d,ref).reindex(a.index);pa.append(dict(suite=suite,first='F3_A_SCAN',second=ref)|mcn(joint(a),joint(b)))
  for f in ['F3','F2']:
   a=table_method(d,f+'_A_EVENT');b=table_method(d,f+'_A_SCAN').reindex(a.index);pb.append(dict(suite=suite,source=f,first=f+'_A_EVENT',second=f+'_A_SCAN')|mcn(joint(a),joint(b)))
 for rows in [pa,pb]:
  for q,adjusted in zip(rows,holm([z['p_value'] for z in rows])):
   q['p_holm']=float(adjusted);q['significant']=bool(adjusted<.05);q['direction']='first' if q['first_success']>q['second_success'] else ('second' if q['first_success']<q['second_success'] else 'tie')
 wins=sum(x['significant'] and x['direction']=='first' for x in pa);losses=sum(x['significant'] and x['direction']=='second' for x in pa)
 decisions.append(dict(endpoint='P-A',decision='validated' if wins==4 else ('Partially validated' if wins>0 and losses==0 else 'Not validated'),significant_first=wins,significant_second=losses))
 wins=sum(x['significant'] and x['direction']=='first' for x in pb);losses=sum(x['significant'] and x['direction']=='second' for x in pb)
 decisions.append(dict(endpoint='P-B',decision='event timing helps fA' if wins>=2 and losses==0 else ('it does not' if losses>=2 else 'no difference shown'),significant_first=wins,significant_second=losses))
 cells=['A_keep100','A_keep040','B_keep100','B_keep040'];v3=sim[(sim.suite=='V3')&sim.scenario.isin(cells)];source_rows=[]
 for f in ['F1','F2','F3']:
  d=table_method(v3,f+'_A_APC');assert len(d)==400
  err=abs(d.source_fp_hz-d.true_fp_hz);picks=(abs(d.source_fp_hz-d.true_fd_hz)<=1)
  lo,hi=wilson(int((err<=1).sum()),len(d));source_rows.append(dict(cell='non_dominant_pooled',source=f,n=len(d),finite=int(err.notna().sum()),fp_recovery=int((err<=1).sum()),fp_rate=float((err<=1).mean()),ci_low=lo,ci_high=hi,dominant_picks=int(picks.sum()),strict_fp_recovery=int((err<=.5).sum()),mean_abs_fp_error=float(err.mean()),median_abs_fp_error=float(err.median())))
 for f in ['F2','F1']:
  a=table_method(v3,f+'_A_APC');b=table_method(v3,'F3_A_APC').reindex(a.index);pc.append(dict(first=f,second='F3')|mcn(abs(a.source_fp_hz-a.true_fp_hz)<=1,abs(b.source_fp_hz-b.true_fp_hz)<=1))
 for q,adjusted in zip(pc,holm([z['p_value'] for z in pc])):q['p_holm']=float(adjusted);q['significant']=bool(adjusted<.05);q['direction']='first' if q['first_success']>q['second_success'] else ('second' if q['first_success']<q['second_success'] else 'tie')
 helps=any(q['significant'] and q['direction']=='first' for q in pc)
 decisions.append(dict(endpoint='P-C',decision='burst timing identifies the coupled rhythm beyond the spectral peak' if helps else 'in these simulations, the burst-based fP was not shown to improve on the spectral peak'))
 for (cell,f),d in sim[(sim.suite=='V3')&sim.method.isin([f+'_A_APC' for f in ['F1','F2','F3']])].groupby(['scenario','f_source'],sort=False):
  err=abs(d.source_fp_hz-d.true_fp_hz);picks=abs(d.source_fp_hz-d.true_fd_hz)<=1;lo,hi=wilson(int((err<=1).sum()),len(d))
  source_rows.append(dict(cell=cell,source=f,n=len(d),finite=int(err.notna().sum()),fp_recovery=int((err<=1).sum()),fp_rate=float((err<=1).mean()),ci_low=lo,ci_high=hi,dominant_picks=int(picks.sum()),strict_fp_recovery=int((err<=.5).sum()),mean_abs_fp_error=float(err.mean()),median_abs_fp_error=float(err.median())))
 for q in source_rows:q['dominant_pick_rate']=q['dominant_picks']/q['n'] if q['cell'] not in ['R_single_keep100','N_uncoupled'] else np.nan
 write(pa,'P_A.csv');write(pb,'P_B.csv');write(pc,'P_C.csv');write(source_rows,'P_C_source_recovery.csv');write(decisions,'primary_decisions.csv')
 retained=[]
 for keys,g in sim[sim.method.isin(['F1_A_APC','F2_A_APC'])].groupby(['suite','dataset','f_source'],sort=False):retained.append(dict(suite=keys[0],dataset=keys[1],source=keys[2],n=len(g),finite_step2=int(g.source_fp_hz.notna().sum()),finite_step2_later_failed=int(g.step2_fp_later_apc_failed.sum())))
 write(retained,'simulation_retained_step2_counts.csv')
 null=sim[((sim.suite.isin(['V1','V2']))&(sim.dataset=='timing_null'))|((sim.suite=='V3')&(sim.scenario=='N_uncoupled'))];false=[]
 for (suite,method),g in null.groupby(['suite','method'],sort=False):false.append(dict(suite=suite,method=method)|metrics(g))
 write(false,'false_joint_recovery.csv')
 aucrows=[];bootrows=[];rng=np.random.Generator(np.random.MT19937(20261114))
 for suite in ['V1','V2']:
  d=sim[sim.suite==suite];pairs=np.sort(d[d.dataset=='coupled'].input_id.unique());N=len(pairs);idx=rng.integers(0,N,size=(10000,N));B=np.zeros((10000,N));np.add.at(B,(np.arange(10000)[:,None],idx),1)
  for method in METHODS:
   a=d[(d.dataset=='coupled')&(d.method==method)].set_index('input_id').reindex(pairs);b=d[(d.dataset=='timing_null')&(d.method==method)].set_index('paired_coupled_id').reindex(pairs);assert a.index.is_unique and b.index.is_unique
   point,reps,nc,nn,npair=boot_auc(a.coupling.to_numpy(),b.coupling.to_numpy(),B);ci=np.nanpercentile(reps,[2.5,97.5]);aucrows.append(dict(suite=suite,method=method,pairs=N,finite_coupled=nc,finite_null=nn,complete_pairs=npair,auc=point,ci_low=ci[0],ci_high=ci[1],bootstrap_repeats=10000,seed=20261114));bootrows.append(pd.DataFrame(dict(suite=suite,method=method,resample=np.arange(1,10001),auc=reps,seed=20261114)))
 write(aucrows,'coupling_auc.csv');write(pd.concat(bootrows,ignore_index=True),'coupling_auc_bootstrap.csv')
 cal=[]
 truths=read(O/'simulation_truths.csv')
 for row in truths.itertuples():
  with h5py.File(O/'checkpoints'/f'{row.key}.mat','r') as h:
   c=h['detail/calibration'];p=float(c['p'][0,0]);observed=float(c['observed'][0,0]);status=int(c['status'][0,0])
  cal.append(dict(suite=row.suite,key=row.key,scenario=row.scenario,dataset=row.dataset,p_value=p,observed_max=observed,status=status,reject=bool(np.isfinite(p) and p<=.05),seed=20261115,surrogates=200))
 cal=write(cal,'calibrated_trial_tests.csv');summ=[]
 for (suite,dataset),g in cal.groupby(['suite','dataset'],sort=False):
  k=int(g.reject.sum());lo,hi=wilson(k,len(g));summ.append(dict(suite=suite,dataset=dataset,n=len(g),valid=int(g.p_value.notna().sum()),invalid=int(g.p_value.isna().sum()),rejections=k,rate=k/len(g),ci_low=lo,ci_high=hi,endpoint='power' if dataset=='coupled' else 'false_positive_rate',seed=20261115))
 write(summ,'calibrated_specificity.csv')
 return sim,decisions

def real_data():
 rodent=pd.concat([read(O/f'rodent_worker{w}.csv') for w in range(1,5)],ignore_index=True);assert rodent.input_id.nunique()==3646 and not rodent.duplicated(['input_id','method']).any() and (rodent.groupby('input_id').size()==4).all()
 mapping=read(O/'rodent_analysis_rows.csv');physical=rodent.drop(columns=['session','channel_index','duration_s'])
 D=mapping.merge(physical,on='input_id',validate='many_to_many');assert len(D)==3982*4
 # Preserve the original APC-v1 reference values for every bout-set/analysis row.
 saved=read(O/'rodent_all_saved_references.csv');a=saved[saved.method=='APC-v1.0'];keys=['input_id','bout_set','animal','session','analysis','state','bout'];assert not a.duplicated(keys).any()
 original=D[D.method=='APC-v1.0'].merge(a,on=keys,validate='one_to_one',suffixes=('','_saved'));assert len(original)==3982
 for target,src in [('recovered_fp_hz','fp'),('recovered_fa_hz','fa'),('raw_mvl','raw'),('coupling','coupling_saved'),('preferred_phase_deg','pref'),('status','status_saved')]:original[target]=original[src]
 for col in ['recovered_fp_hz','recovered_fa_hz','raw_mvl','coupling','preferred_phase_deg','status']:
  D.loc[D.method=='APC-v1.0',col]=original[col].to_numpy()
 D['valid']=D.valid.astype(bool);write(D,'rodent_bout_estimates.csv')
 sessionrows=[];spreadrows=[];staterows=[]
 for bout_set,cohort in D.groupby('bout_set',sort=True):
  for gi,((analysis,animal,session),g) in enumerate(cohort.groupby(['analysis','animal','session'],sort=True)):
   states={s:np.sort(g.loc[g.state==s,'bout'].unique()) for s in ['run','rest']};rng=np.random.default_rng(np.random.SeedSequence([20261022,gi]));indices={s:rng.integers(len(ids),size=(10000,len(ids))) for s,ids in states.items()}
   for method,mg in g.groupby('method',sort=True):
    values={s:mg[mg.state==s].set_index('bout').reindex(ids) for s,ids in states.items()}
    for var in ['recovered_fp_hz','coupling']:
     arrays={s:v[var].to_numpy(float) for s,v in values.items()};finite={s:v[np.isfinite(v)] for s,v in arrays.items()};aa,bb=finite['run'],finite['rest'];tt=stats.ttest_ind(aa,bb,equal_var=False) if min(len(aa),len(bb))>=2 else None
     with warnings.catch_warnings():
      warnings.simplefilter('ignore',RuntimeWarning);boot={s:np.nanmean(v[indices[s]],axis=1) for s,v in arrays.items()}
     diff=boot['run']-boot['rest'];bounds=np.nanpercentile(diff,[2.5,97.5])
     sessionrows.append(dict(bout_set=bout_set,analysis=analysis,animal=animal,session=session,method=method,outcome=var,n_run=len(aa),n_rest=len(bb),run_mean=np.mean(aa) if len(aa) else np.nan,rest_mean=np.mean(bb) if len(bb) else np.nan,mean_difference=np.mean(aa)-np.mean(bb) if len(aa) and len(bb) else np.nan,welch_t=tt.statistic if tt else np.nan,welch_p=tt.pvalue if tt else np.nan,hedges_g=hedges(aa,bb),ci_low=bounds[0],ci_high=bounds[1],seed=20261022,bootstrap_repeats=10000))
     for state,v in finite.items():staterows.append(dict(bout_set=bout_set,analysis=analysis,animal=animal,session=session,method=method,outcome=var,state=state,n=len(v),mean=np.mean(v) if len(v) else np.nan,median=np.median(v) if len(v) else np.nan))
    for state,v in values.items():
     fp=v.recovered_fp_hz.to_numpy(float);fp=fp[np.isfinite(fp)];spreadrows.append(dict(bout_set=bout_set,analysis=analysis,animal=animal,session=session,method=method,state=state,n_valid=len(fp),fp_sd=np.std(fp,ddof=1) if len(fp)>1 else np.nan,fp_iqr=np.diff(np.quantile(fp,[.25,.75]))[0] if len(fp) else np.nan,fp_mad=np.median(abs(fp-np.median(fp))) if len(fp) else np.nan))
 S=write(sessionrows,'rodent_session_statistics.csv');write(staterows,'rodent_state_summary.csv');spread=write(spreadrows,'rodent_within_state_spread.csv');across=[]
 spread_summary=[]
 for keys,g in spread.groupby(['bout_set','analysis','method','state'],sort=True):
  for pool in sorted(g.animal.unique())+['pooled']:
   q=g if pool=='pooled' else g[g.animal==pool];x=q.fp_sd.to_numpy(float);x=x[np.isfinite(x)]
   spread_summary.append(dict(bout_set=keys[0],analysis=keys[1],method=keys[2],state=keys[3],animal_pool=pool,n_sessions=len(x),mean_fp_sd=np.mean(x) if len(x) else np.nan,median_fp_sd=np.median(x) if len(x) else np.nan))
 write(spread_summary,'rodent_within_state_summary.csv')
 for gi,((bout_set,analysis,method,outcome),g) in enumerate(S.groupby(['bout_set','analysis','method','outcome'],sort=True)):
  for pool in sorted(g.animal.unique())+['pooled']:
   q=g if pool=='pooled' else g[g.animal==pool];x=q.mean_difference.to_numpy(float);x=x[np.isfinite(x)];rng=np.random.default_rng(np.random.SeedSequence([20261022,gi,0 if pool=='pooled' else int(pool[-3:])]))
   boot=np.mean(x[rng.integers(0,len(x),size=(10000,len(x)))],axis=1) if len(x) else np.full(10000,np.nan);ci=np.nanpercentile(boot,[2.5,97.5]);tt=stats.ttest_1samp(x,0) if len(x)>1 else None;w,p,n,nz=signed_rank(x)
   across.append(dict(bout_set=bout_set,analysis=analysis,animal_pool=pool,method=method,outcome=outcome,n_sessions=len(x),mean_session_difference=np.mean(x) if len(x) else np.nan,median_session_difference=np.median(x) if len(x) else np.nan,ci_low=ci[0],ci_high=ci[1],one_sample_t=tt.statistic if tt else np.nan,one_sample_p=tt.pvalue if tt else np.nan,wilcoxon_statistic=w,wilcoxon_p=p,seed=20261022,bootstrap_repeats=10000))
 write(across,'rodent_across_session_statistics.csv')
 sources=pd.concat([read(O/f'rodent_sources_worker{w}.csv') for w in range(1,5)],ignore_index=True);sources=mapping.merge(sources.drop(columns=['git_commit','protocol_sha256','provenance_file','matlab_version']),on='input_id',validate='many_to_many');write(sources,'rodent_sources.csv');counts=[]
 for keys,g in sources.groupby(['bout_set','analysis','source'],sort=False):counts.append(dict(dataset='Rodent',bout_set=keys[0],analysis=keys[1],source=keys[2],n=len(g),finite_step2=int(g.source_fp_hz.notna().sum()),finite_step2_later_failed=int(g.finite_step2_later_failed.sum())))
 ecog=pd.concat([read(O/f'ecog_worker{w}.csv') for w in range(1,5)],ignore_index=True);assert ecog.key.nunique()==2642 and (ecog.groupby('key').size()==5).all() and not ecog.duplicated(['key','method']).any();ecog['valid']=ecog.valid.astype(bool);write(ecog,'ecog_bout_estimates.csv')
 esources=pd.concat([read(O/f'ecog_sources_worker{w}.csv') for w in range(1,5)],ignore_index=True);write(esources,'ecog_sources.csv')
 for (rec,f),g in esources.groupby(['recording','source'],sort=False):counts.append(dict(dataset='ECoG',recording=rec,source=f,n=len(g),finite_step2=int(g.source_fp_hz.notna().sum()),finite_step2_later_failed=int(g.finite_step2_later_failed.sum())))
 write(counts,'real_retained_step2_counts.csv')
 peaks=read(R/'revision_checks/ecog_miller_motor/analysed_rest_spectral_peaks.csv');ptrows=[]
 for (rec,pt,method),g in ecog.groupby(['recording','patient','method'],sort=False):
  rest=g[(g.state=='rest')&g.valid];move=g[(g.state=='move')&g.valid];peak=peaks[(peaks.recording==rec)&(peaks.patient==pt)];assert len(peak)<=1;peak=float(peak.iloc[0].rest_spectral_peak_hz) if len(peak) else np.nan;median=float(rest.recovered_fp_hz.median())
  ptrows.append(dict(recording=rec,patient=pt,method=method,n_bouts=len(g),n_rest=int((g.state=='rest').sum()),n_move=int((g.state=='move').sum()),valid_rest=len(rest),valid_move=len(move),rest_fp_median=median,rest_spectral_peak_hz=peak,rest_agreement=bool(np.isfinite(median) and np.isfinite(peak) and abs(median-peak)<=2),rest_absolute_difference=abs(median-peak),mean_rest_coupling=float(rest.coupling.mean()),mean_move_coupling=float(move.coupling.mean()),move_minus_rest_coupling=float(move.coupling.mean()-rest.coupling.mean()),rest_fp_sd=float(rest.recovered_fp_hz.std(ddof=1)),move_fp_sd=float(move.recovered_fp_hz.std(ddof=1))))
 pts=write(ptrows,'ecog_patient_summary.csv');summary=[];bootrows=[];rng=np.random.Generator(np.random.MT19937(20261024))
 for rec in ['movement','imagery']:
  d=pts[pts.recording==rec];patients=sorted(d.patient.unique());idx=rng.integers(0,len(patients),size=(10000,len(patients)))
  for method in ['F3_A_SCAN','F3_A_EVENT','APC-v1.0','APC-v3.0','A2_prime_2D']:
   g=d[d.method==method].set_index('patient').reindex(patients);v=g.move_minus_rest_coupling.to_numpy();boot=np.nanmean(v[idx],axis=1);ci=np.nanpercentile(boot,[2.5,97.5]);summary.append(dict(recording=rec,method=method,patients=len(patients),rest_agreement_count=int(g.rest_agreement.fillna(False).sum()),rest_agreement_denominator=18,mean_move_minus_rest=float(np.nanmean(v)),ci_low=ci[0],ci_high=ci[1],patients_finite_difference=int(np.isfinite(v).sum()),median_rest_fp_sd=float(g.rest_fp_sd.median()),median_move_fp_sd=float(g.move_fp_sd.median()),seed=20261024,bootstrap_repeats=10000));bootrows.append(pd.DataFrame(dict(recording=rec,method=method,resample=np.arange(1,10001),mean_difference=boot,seed=20261024)))
 write(summary,'ecog_summary.csv');write(pd.concat(bootrows,ignore_index=True),'ecog_patient_bootstrap.csv')
 return D,ecog

def main():
 started=time.perf_counter();assert not (O/'statistics_complete.json').exists(),'Do not repeat reportable statistics'
 assert not (O/'STOP_RUN.md').exists()
 for w in range(1,5):
  for prefix in ['worker','real_worker']:assert json.loads((O/f'{prefix}{w}_complete.json').read_text(encoding='utf-8'))['status']=='COMPLETE'
 sim,decisions=simulations();rodent,ecog=real_data();combined=[]
 for endpoint,file in [('P-A','P_A.csv'),('P-B','P_B.csv'),('P-C','P_C.csv'),('Recovery','recovery_overall.csv'),('Specificity','false_joint_recovery.csv'),('AUC','coupling_auc.csv'),('Calibrated','calibrated_specificity.csv'),('Rodent','rodent_across_session_statistics.csv'),('ECoG','ecog_summary.csv')]:
  q=read(O/file);q.insert(0,'endpoint_family',endpoint);combined.append(q)
 write(pd.concat(combined,ignore_index=True,sort=False),'statistics.csv')
 result=dict(status='COMPLETE',elapsed_seconds=time.perf_counter()-started,completed_utc=datetime.now(timezone.utc).isoformat(),simulation_inputs=sim.key.nunique(),simulation_rows=len(sim),rodent_analysis_rows=len(rodent),ecog_bouts=ecog.key.nunique(),decisions=decisions)
 jw('statistics_complete.json',result);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
