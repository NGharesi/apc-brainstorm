"""Append fixed real-data validation results, using saved estimates only."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys,os
O=Path(__file__).resolve().parent;R=O.parent.parent;C=O/'phaseC';sys.path.insert(0,str(R/'pydeps'));os.environ['MPLCONFIGDIR']=str(O/'.matplotlib')
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def js(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def link(p,label=None):
    p=Path(p);p=p if p.is_absolute() else C/p
    return f'[{label or p.name}](<{p.as_posix()}>)'
def table(D,cols):
    def fmt(x):
        if pd.isna(x):return 'NA'
        if isinstance(x,(float,np.floating)):return f'{x:.6g}'
        return str(x).replace('|','/')
    return '\n| '+' | '.join(cols)+' |\n| '+' | '.join('---' for _ in cols)+' |\n'+'\n'.join('| '+' | '.join(fmt(z[k]) for k in cols)+' |' for _,z in D.iterrows())+'\n'
m=js(C/'provenance.json');assert all((C/f'worker{w}_complete.json').exists() for w in range(1,5))
for x in m['reused_files_sha256']:assert sha(Path(x['path']))==x['sha256']
def csv(D,path):
    D=D.copy();D['freeze_commit']=m['freeze_commit'];D['v3_protocol_sha256']=m['protocol_sha256'];D['provenance_record']='phaseC/provenance.json';D.to_csv(C/path,index=False,encoding='utf-8',float_format='%.17g');return D
lines=['## Phase C: unchanged saved real-data inputs','',
       'All saved preprocessing, bouts, channels and scan estimates were reused unchanged. Source/prep/bout/selection hashes were checked before and after the new estimates. The new v3 feature wrapper preserves the original raw-MVL and preferred-phase reconstruction assertions; every valid estimate passed them. '+link('provenance.json')+'; '+link('v3_feature_wrapper.diff')+'.','',
       'There were 3,646 unique physical rodent windows and 3,982 analysis rows across the prespecified 5-s and explicitly **POST HOC 2-s** analyses. Identical channel/start/stop windows are estimated once and reused. ECoG contains the original 2,648 analysed movement/imagery bouts, including the originally ineligible patient for status reporting; the primary eligibility remains the fixed 18 patients. APC v3 uses fA [80,150], minPhaseHz 1, maxPhaseHz 30 and all other defaults. The saved ECoG v1 reference is its Amendment-1 6-30-Hz run; v3 uses 1-30 Hz with its automatic 7/T feasibility bound, as specified for Phase C. The reused ECoG scans retain 6-30 Hz. No scan or preprocessing step was rerun.','',
       'The original regional statistics and seeds were reused, including 10,000 bout-bootstrap resamples and region-specific REML mixed models. ECoG statistics retain the original patient-bootstrap scheme (10,000, seed 20261024), restricted to the v3 protocol\'s endpoints. Original v1 fits/results are shown alongside. Full execution/statistical source diffs are stored with the copied scripts. '+link(O/'phaseC_analysis_plan.json')+'.','']
# Rodent, separate prespecified and post-hoc sections.
for label,folder,prefix in [('Prespecified rodent: 5-s bouts','rodent5s','regional'),('POST HOC rodent sensitivity: 2-s bouts','POST_HOC_rodent2s','posthoc_2s')]:
    A=C/folder;S=pd.read_csv(A/(prefix+'_session_statistics.csv'),encoding='utf-8');P=pd.read_csv(A/(prefix+'_across_session_statistics.csv'),encoding='utf-8');spread=pd.read_csv(A/(prefix+'_within_state_fp_spread.csv'),encoding='utf-8');M=pd.read_csv(A/(prefix+'_mixed_model_coefficients.csv'),encoding='utf-8')
    S=S[S.method.isin(['APC-v1.0','APC-v3.0'])];P=P[P.method.isin(['APC-v1.0','APC-v3.0'])]
    oldfolder=R/'revision_checks/rodent_multi' if prefix=='regional' else R/'revision_checks/rodent_multi/posthoc_2s';oldM=pd.read_csv(oldfolder/(prefix+'_mixed_model_coefficients.csv'),encoding='utf-8');M['method']='APC-v3.0';oldM['method']='APC-v1.0';mixed=pd.concat([oldM,M],ignore_index=True);csv(mixed,folder+'/v1_v3_mixed_coefficients.csv')
    lines += ['### '+label,'',
              'Per-session run minus rest differences (same fixed sessions and selected channels):',table(S,['analysis','animal','session','method','outcome','n_run','n_rest','mean_difference','welch_t','welch_p','hedges_g','ci_low','ci_high']),
              'Across-session primary summaries:',table(P,['analysis','animal_pool','method','outcome','n_sessions','mean_session_difference','ci_low','ci_high','one_sample_p','wilcoxon_p']),
              'Full session tables, all scan rows and within-state SD/IQR/MAD:',
              '- '+link(A/(prefix+'_session_statistics.csv'))+'.',
              '- '+link(A/(prefix+'_across_session_statistics.csv'))+'.',
              '- '+link(A/(prefix+'_within_state_fp_spread.csv'))+'; '+link(A/(prefix+'_across_session_spread_comparisons.csv'))+'.',
              '- '+link(A/'v1_v3_mixed_coefficients.csv')+'; v3 convergence/covariance diagnostics '+link(A/(prefix+'_mixed_models.json'))+'.','']
    # Report the fixed-effect state coefficients in a compact table.
    namecol='Name' if 'Name' in mixed else 'name';state=mixed[mixed[namecol].astype(str).str.contains('state_run')]
    cols=[x for x in ['analysis','method','outcome','Estimate','SE','tStat','DF','pValue','Lower','Upper'] if x in state]
    lines += ['Mixed-model state coefficients:',table(state,cols)]
# Status/floor summaries from new estimates, with explicit denominators.
E=C/'ecog';V=pd.read_csv(C/'ecog_v3_estimates.csv',encoding='utf-8',float_precision='round_trip');V['valid']=V.status.eq(0)&V.fP_hz.notna()&V.ozkurt_mvl.notna();elig=pd.read_csv(E/'patient_eligibility.csv',encoding='utf-8');patients=set(elig[elig.eligible].patient);assert len(patients)==18
status=[]
for (pt,rec,state),g in V.groupby(['patient','recording','state'],sort=True):
    valid=g.valid;at=g.fp_at_flo.astype(bool);status.append(dict(patient=pt,recording=rec,state=state,eligible=pt in patients,n=len(g),n_valid=int(valid.sum()),status3=int(g.status.eq(3).sum()),status3_rate=g.status.eq(3).mean(),status4=int(g.status.eq(4).sum()),fp_near_flo=int(at.sum()),fp_near_flo_rate_all=at.mean(),fp_near_flo_rate_valid=at[valid].mean(),status_counts=json.dumps(g.status.value_counts().sort_index().to_dict())))
status=csv(pd.DataFrame(status),'ecog_status_floor_rates.csv')
RMAP=pd.read_csv(C/'rodent_analysis_rows.csv',encoding='utf-8');RV=pd.read_csv(C/'rodent_v3_unique_estimates.csv',encoding='utf-8');RR=RMAP.merge(RV.drop(columns=['session','channel_index']),on='input_id',validate='many_to_one');rs=[]
for key,g in RR.groupby(['bout_set','analysis','animal','state']):
    valid=g.status.eq(0);rs.append(dict(zip(['bout_set','analysis','animal','state'],key))|dict(n=len(g),valid=int(valid.sum()),status3=int(g.status.eq(3).sum()),status3_rate=g.status.eq(3).mean(),fp_near_flo=int(g.fp_at_flo.sum()),fp_near_flo_rate_all=g.fp_at_flo.mean(),status_counts=json.dumps(g.status.value_counts().sort_index().to_dict())))
rs=csv(pd.DataFrame(rs),'rodent_status_floor_rates.csv')
lines += ['### Rodent status and feasibility-bound counts','',table(rs,['bout_set','analysis','animal','state','n','valid','status3','fp_near_flo','status_counts']),
          '## ECoG: fixed eligible patients and primary endpoints','']
newstats=pd.read_csv(E/'ecog_statistics.csv',encoding='utf-8');oldstats=pd.read_csv(R/'revision_checks/ecog_miller_motor/ecog_statistics.csv',encoding='utf-8')
oldstats=oldstats[oldstats.subset.isin(['prespecified','sensitivity_a'])&oldstats.recording.eq('movement')&((oldstats.endpoint.eq('coupling_state')&oldstats.method.eq('APC-v1.0'))|oldstats.endpoint.eq('within_state_fP_SD'))]
T=pd.concat([oldstats,newstats],ignore_index=True);T['primary']=np.where(T.endpoint.eq('coupling_state'),'Primary 1','Primary 2');csv(T,'ecog_primary_v1_v3.csv')
lines += [table(T,['subset','primary','method','n_patients','n_bouts','mean_difference','median_difference','t_p_two_sided','wilcoxon_p_two_sided','ci_low','ci_high','decision']),
          'Primary 1 uses the mean movement minus rest normalized-MVL difference. Primary 2 uses the median patient-level difference in mean within-state fP SD (APC minus MVL-Ozkurt scan). Decisions use the original bootstrap CI rules and labels. Sensitivity (a) excludes the same 11 flagged eligible patients.','']
for _,z in newstats.iterrows():lines.append(f'- {z.subset}, '+('Primary 1' if z.endpoint=='coupling_state' else 'Primary 2')+f': **{z.decision}**.')
lines += ['', 'The unchanged eligible-patient inventory: '+link(E/'patient_eligibility.csv')+'. Patient/state means, medians, SD and finite-bout denominators: '+link(E/'ecog_patient_summary.csv')+'. New primary endpoint tables: '+link(E/'ecog_statistics.csv')+'.','',
          'Mixed model (original ML/default fitlme specification, rest reference): outcome ~ state + (1 + state | patient). '+link(E/'mixed_model_coefficients.csv')+'; '+link(E/'mixed_model_runtime.json')+'.','']
# Prespecified rest-spectrum success, plus SP-raw on identical rest bouts.
old=pd.read_csv(R/'revision_checks/ecog_miller_motor/ecog_bout_estimates.csv',encoding='utf-8',float_precision='round_trip');PSD=pd.read_csv(R/'revision_checks/ecog_miller_motor/analysed_rest_spectral_peaks.csv',encoding='utf-8');rows=[]
for pt in sorted(patients):
    g=V[V.patient.eq(pt)&V.recording.eq('movement')&V.state.eq('rest')];z=dict(patient=pt,n_rest=len(g),n_v3_valid=int(g.valid.sum()));p=PSD[PSD.patient.eq(pt)&PSD.recording.eq('movement')];assert len(p)==1;z['spectral_peak_hz']=p.rest_spectral_peak_hz.iloc[0]
    z['v3_median_fp_hz']=g[g.valid].fP_hz.median();sp=g[g.sp_raw_status.eq(0)&g.sp_raw_fp_hz.notna()];z['SP_raw_median_fp_hz']=sp.sp_raw_fp_hz.median();z['n_SP_raw_valid']=len(sp)
    for method,name in [('APC-v1.0','v1'),('MVL-Ozkurt','scan')]:
        a=old[old.patient.eq(pt)&old.recording.eq('movement')&old.state.eq('rest')&old.method.eq(method)&old.status.eq(0)];z[name+'_median_fp_hz']=a.fP_hz.median()
    pair=g[g.valid&g.sp_raw_status.eq(0)&g.sp_raw_fp_hz.notna()];delta=(pair.fP_hz-pair.sp_raw_fp_hz).abs();z.update(n_paired=len(pair),paired_median_absolute_difference_hz=delta.median(),paired_mean_absolute_difference_hz=delta.mean(),paired_within_1_hz=int(delta.le(1).sum()),paired_fraction_within_1_hz=delta.le(1).mean())
    for name in ['v1','v3','scan','SP_raw']:
        med=z[name+'_median_fp_hz'];z[name+'_within_2_hz']=bool(np.isfinite(med) and abs(med-z['spectral_peak_hz'])<=2);z[name+'_in_12_20_hz']=bool(np.isfinite(med) and 12<=med<=20)
    rows.append(z)
rest=csv(pd.DataFrame(rows),'ecog_rest_frequencies.csv');n_success=int(rest.v3_within_2_hz.sum());passed=n_success>=9
result=dict(criterion='ECoG rest median within 2 Hz of rest spectral peak in at least 9/18 eligible patients',n_patients=18,v3_success=n_success,v1_success=int(rest.v1_within_2_hz.sum()),SP_raw_success=int(rest.SP_raw_within_2_hz.sum()),passed=passed,freeze_commit=m['freeze_commit'],protocol_sha256=m['protocol_sha256']);(C/'ecog_success_criterion.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
lines += ['### ECoG secondary 1 and prespecified success criterion','',f'**ECoG success criterion: {"PASS" if passed else "FAIL"}.** v3 median rest fP was within 2 Hz of the unchanged rest spectral peak in {n_success}/18 patients (required >=9/18); v1: {result["v1_success"]}/18; SP-raw: {result["SP_raw_success"]}/18. Missing medians count as failures. The original analysed-rest spectrum uses its unchanged 8-30-Hz residual-peak rule.','',table(rest,['patient','n_rest','n_v3_valid','spectral_peak_hz','v1_median_fp_hz','v3_median_fp_hz','SP_raw_median_fp_hz','scan_median_fp_hz','v3_within_2_hz','paired_fraction_within_1_hz']),
          'All per-patient medians, counts within 12-20 Hz, spectrum agreement, paired SP-raw agreement and finite denominators: '+link('ecog_rest_frequencies.csv')+'.','']
summary=[]
for name in ['v1','v3','scan','SP_raw']:summary.append(dict(method=name,n_patients=18,median_in_12_20=int(rest[name+'_in_12_20_hz'].sum()),within_2_hz_spectrum=int(rest[name+'_within_2_hz'].sum())))
lines += [table(pd.DataFrame(summary),['method','n_patients','median_in_12_20','within_2_hz_spectrum']),
          '### ECoG status-3 rates and fP near f_lo','',table(status,['patient','recording','state','eligible','n','n_valid','status3','status3_rate','status4','fp_near_flo','fp_near_flo_rate_all','fp_near_flo_rate_valid']),
          'f_lo = max(1, 7/T); near means within 0.05 Hz. Full status counts and denominators: '+link('ecog_status_floor_rates.csv')+'. Original scan/v1 boundary flags and new v3 boundary flags are retained in '+link(E/'status_boundary_rates.csv')+'.','']
fig,ax=plt.subplots(figsize=(5.5,5.2));colors={'v1':'#0072B2','v3':'#D55E00'}
for name in ['v1','v3']:ax.scatter(rest.spectral_peak_hz,rest[name+'_median_fp_hz'],label='APC '+name+'.0',s=34,color=colors[name],alpha=.8)
ax.plot([0,30],[0,30],color='.35',ls='--',lw=1);ax.fill_between([0,30],[-2,28],[2,32],color='.8',alpha=.25);ax.set(xlim=(0,31),ylim=(0,31),xlabel='Rest spectral peak (Hz)',ylabel='Patient median rest fP (Hz)');ax.spines[['top','right']].set_visible(False);ax.legend(frameon=False);fig.tight_layout();meta=f'git={m["freeze_commit"]}; tag=v3.0; protocol_sha256={m["protocol_sha256"]}; source=phaseC/ecog_rest_frequencies.csv; source_sha256={sha(C/"ecog_rest_frequencies.csv")}; unchanged rest spectral peak'
fig.savefig(O/'ECoG_rest_fp_spectral_peak.png',dpi=300,metadata={'Description':meta});fig.savefig(O/'ECoG_rest_fp_spectral_peak.svg',metadata={'Description':meta});plt.close(fig)
lines+=['### Phase C figure','',link(O/'ECoG_rest_fp_spectral_peak.png')+' (300 dpi); '+link(O/'ECoG_rest_fp_spectral_peak.svg')+'. No title/footer inside the figure; source CSV and commit/hash are embedded in metadata. Shading marks +/-2 Hz.','',
        '### Phase C runtime and deviations','']
for w in range(1,5):z=js(C/f'worker{w}_complete.json');lines.append(f'- Worker {w}: {z["elapsed_seconds"]:.3f} s (ECoG and rodent).')
for d in js(O/'deviations.json')['deviations']:lines.append('- '+d['type']+': '+d['reason'])
lines+=['- Parallel workers emitted a harmless directory-already-exists warning while creating the shared checkpoint directory; each output filename belongs to one worker.','',
        'All protocol/source/prep hashes remain unchanged. No result was committed. Complete normalized-feature assertions, diagnostics and provenance are retained per unique input in `phaseC/checkpoints/`.','']
text=(O/'RESULTS_v3.md').read_text(encoding='utf-8');assert '## Phase C: unchanged saved real-data inputs' not in text;text=text.replace('Phase C remains to be completed.','Phase C completed; ECoG success criterion '+('passed.' if passed else 'failed.')).replace('A1, A3 and A4 passed; Phase C is authorized and remains to be completed.','A1, A3 and A4 passed. The completed Phase C validation is reported below.');(O/'RESULTS_v3.md').write_text(text+'\n'+'\n'.join(lines),encoding='utf-8')
if not passed:(O/'STOPPED.md').write_text('# STOPPED: ECoG Phase-C success criterion failed\n\nThe Phase-B adoption criteria A1/A3/A4 passed. In Phase C, v3 rest median fP was within 2 Hz of the rest spectral peak in '+str(n_success)+'/18 patients, below 9/18. No method change or workaround was made. All completed results are reported in RESULTS_v3.md.\n',encoding='utf-8')
status=js(O/'STATUS.json');status.update(status='COMPLETE' if passed else 'STOPPED_ECOG_CRITERION_FAILURE',phaseC_complete=True,ecog_success_criterion=result,updated_utc=datetime.now(timezone.utc).isoformat());(O/'STATUS.json').write_text(json.dumps(status,indent=2),encoding='utf-8');p=js(O/'provenance.json');p.update(status=status['status'],phaseC_complete=True,phaseC_provenance='phaseC/provenance.json',ecog_success_criterion=result);(O/'provenance.json').write_text(json.dumps(p,indent=2),encoding='utf-8');print(json.dumps(status),flush=True)
