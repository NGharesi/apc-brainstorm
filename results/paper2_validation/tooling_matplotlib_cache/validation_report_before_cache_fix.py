from pathlib import Path
import sys,json,hashlib,datetime,os
O=Path(__file__).resolve().parent;R=O.parent.parent;sys.path.insert(0,str(R/'pydeps'))
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=json.loads((O/'provenance.json').read_text(encoding='utf-8'))
def read(n):return pd.read_csv(O/n,encoding='utf-8',float_precision='round_trip')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(v):
 if pd.isna(v):return 'NA'
 if isinstance(v,(float,np.floating)):return f'{v:.5g}'
 return str(v).replace('|','\\|')
def md(d):
 return '| '+' | '.join(d.columns)+' |\n| '+' | '.join(['---']*len(d.columns))+' |\n'+''.join('| '+' | '.join(clean(x) for x in row)+' |\n' for row in d.itertuples(index=False,name=None))
methods=[f'{f}_{a}' for f in ['F1','F2','F3'] for a in ['A_APC','A_SCAN','A_EVENT']]+['A2_prime_2D','APC-v1.0','APC-v3.0']
short={m:m.replace('_A_',' / ').replace('A2_prime_2D',"A2' 2-D") for m in methods}
plt.rcParams.update({'svg.fonttype':'none','font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False})
figures=[]
def save(fig,stem,sources):
 provenance={'git_commit':P['git_head'],'protocol_sha256':P['protocol_sha256'],'sources':[{'path':str(O/n),'sha256':sha(O/n)} for n in sources]}
 desc=json.dumps(provenance,separators=(',',':'));fig.tight_layout();fig.savefig(O/(stem+'.png'),dpi=300,metadata={'Description':desc,'Software':'Matplotlib'});fig.savefig(O/(stem+'.svg'),metadata={'Description':desc,'Creator':'APC paper-2 validation'})
 figures.append({'name':stem,'png':str(O/(stem+'.png')),'svg':str(O/(stem+'.svg')),'provenance':provenance});plt.close(fig)
def plot_figures():
 recovery=read('recovery_overall.csv');fig,axs=plt.subplots(1,3,figsize=(16,6),sharey=True)
 colors=[('#6d8db5' if m.startswith('F1') else '#dcaa4d' if m.startswith('F2') else '#368b74' if m.startswith('F3') else '#999999') for m in methods]
 for ax,suite in zip(axs,['V1','V2','V3']):
  d=recovery[recovery.suite==suite].set_index('method').reindex(methods);y=d.joint_rate.to_numpy();x=np.arange(len(d));ax.bar(x,y,color=colors,width=.75)
  ax.errorbar(x,y,yerr=np.vstack([y-d.joint_ci_low,d.joint_ci_high-y]),fmt='none',color='black',capsize=2,lw=.8,label='Joint recovery; Wilson 95% CI');ax.plot(x,d.strict_joint_rate,'D',ms=3,color='black',fillstyle='none',label='Strict joint recovery')
  ax.set_xticks(x,[short[m] for m in methods],rotation=75,ha='right');ax.set_ylim(0,1.04);ax.set_ylabel(f'{suite}: recovery proportion (n = {int(d.n.iloc[0])})');ax.grid(axis='y',alpha=.2)
 axs[0].legend(fontsize=7,loc='upper left');save(fig,'figure1_recovery',['recovery_overall.csv'])
 auc=read('coupling_auc.csv');cal=read('calibrated_specificity.csv');fig,axs=plt.subplots(2,2,figsize=(13,10))
 for ax,suite in zip(axs[0],['V1','V2']):
  d=auc[auc.suite==suite].set_index('method').reindex(methods);y=d.auc.to_numpy();x=np.arange(len(d));ax.bar(x,y,color=colors);ax.errorbar(x,y,yerr=np.maximum(0,np.vstack([y-d.ci_low,d.ci_high-y])),fmt='none',color='black',capsize=2,lw=.8);ax.axhline(.5,color='#777777',ls='--',lw=1);ax.set_ylim(0,1.04);ax.set_xticks(x,[short[m] for m in methods],rotation=75,ha='right');ax.set_ylabel(f'{suite}: coupled vs timing-null AUC')
 for ax,endpoint in zip(axs[1],['false_positive_rate','power']):
  d=cal[cal.endpoint==endpoint];x=np.arange(len(d));y=d.rate.to_numpy();ax.bar(x,y,color='#368b74');ax.errorbar(x,y,yerr=np.maximum(0,np.vstack([y-d.ci_low,d.ci_high-y])),fmt='none',color='black',capsize=3);ax.set_xticks(x,d.suite);ax.set_ylim(0,1.04);ax.set_xlabel('Suite: F3 / SCAN calibrated test');ax.set_ylabel('False-positive rate' if endpoint=='false_positive_rate' else 'Power')
  if endpoint=='false_positive_rate':ax.axhline(.05,color='#777777',ls='--',lw=1)
 save(fig,'figure2_specificity',['coupling_auc.csv','calibrated_specificity.csv'])
 d=read('rodent_across_session_statistics.csv');d=d[(d.animal_pool=='pooled')&(d.outcome=='recovered_fp_hz')];fig,axs=plt.subplots(2,3,figsize=(14,8),squeeze=False)
 order=['F3_A_SCAN','F3_A_EVENT','APC-v1.0','A2_prime_2D']
 for i,boutset in enumerate(['prespecified_5s','POST_HOC_2s']):
  for j,region in enumerate(['CA1','EC','E1_sensitivity']):
   ax=axs[i,j];q=d[(d.bout_set==boutset)&(d.analysis==region)].set_index('method').reindex(order);x=np.arange(4);y=q.mean_session_difference.to_numpy();ax.axhline(0,color='#777777',lw=.7);ax.errorbar(x,y,yerr=np.maximum(0,np.vstack([y-q.ci_low,q.ci_high-y])),fmt='o',capsize=4,color='#2e6c84');ax.set_xticks(x,[short[m] for m in order],rotation=30,ha='right');label='Prespecified 5-s' if i==0 else 'POST HOC 2-s';ax.set_ylabel(f'{label}, {region.replace("_"," ")}\nRun minus rest fP (Hz)');ax.grid(axis='y',alpha=.2)
 save(fig,'figure3_rodent_fp',['rodent_across_session_statistics.csv'])
 d=read('ecog_patient_summary.csv');summary=read('ecog_summary.csv');order=['F3_A_SCAN','F3_A_EVENT','APC-v1.0','APC-v3.0','A2_prime_2D'];fig,axs=plt.subplots(1,2,figsize=(14,5))
 patients=sorted(d[d.recording=='movement'].patient.unique());ax=axs[0];x=np.arange(len(patients));palette=['#368b74','#7bbba7','#6d8db5','#dcaa4d','#999999']
 for j,m in enumerate(order):
  q=d[(d.recording=='movement')&(d.method==m)].set_index('patient').reindex(patients);ax.plot(x+(j-2)*.1,q.rest_fp_median,'o',ms=4,label=short[m],color=palette[j])
 q=d[(d.recording=='movement')&(d.method=='APC-v1.0')].set_index('patient').reindex(patients);ax.plot(x,q.rest_spectral_peak_hz,'x',ms=7,color='black',label='Saved rest spectral peak');ax.set_xticks(x,patients,rotation=45);ax.set_ylabel('Movement recording: median rest fP (Hz)');ax.set_xlabel('Patient');ax.legend(fontsize=7,ncol=2)
 ax=axs[1];x=np.arange(len(order));width=.36
 for j,rec in enumerate(['movement','imagery']):
  q=summary[summary.recording==rec].set_index('method').reindex(order);ax.bar(x+(j-.5)*width,q.rest_agreement_count,width,label=f'{rec.capitalize()} ({int(q.patients.iloc[0])} observed patients)',alpha=.8)
 ax.set_xticks(x,[short[m] for m in order],rotation=35,ha='right');ax.set_ylim(0,18.5);ax.set_yticks(np.arange(0,19,3));ax.set_ylabel('Patients within 2 Hz of rest spectral peak (of 18)');ax.legend(fontsize=8);save(fig,'figure4_ecog_rest',['ecog_patient_summary.csv','ecog_summary.csv'])
 (O/'figure_provenance.json').write_text(json.dumps(figures,indent=2)+'\n',encoding='utf-8')

def report():
 stat=json.loads((O/'statistics_complete.json').read_text(encoding='utf-8'));dev=json.loads((O/'deviations.json').read_text(encoding='utf-8'));g=json.loads((O/'all_gate_results.json').read_text(encoding='utf-8'));env=json.loads((O/'environment.json').read_text(encoding='utf-8'))
 text=['# Paper-2 out-of-sample validation\n',f"Protocol Amendment 1 and archive are public on paper2. Amendment push: `{P['git_head']}`. Ablation archive: `{P['archive_commit']}`. Protocol SHA-256: `{P['protocol_sha256']}`. MATLAB: {env['matlab_version']}. No tagged method or protocol source was edited.\n",
       '## Initial stop and Amendment 1 resolution\n',f"The original pre-gate A_EVENT ambiguity stop is preserved unchanged in [STOPPED.md]({O/'STOPPED.md'}). Amendment 1 resolves it with `struct('status_code', s, 'fp_hz', fP)`: status zero whenever the source returns finite fP. Resumed {P['resume_utc']}; the transfer copy amend1_validation.md was ignored.\n",
       '## Gates and inputs\n',"G-gen PASS: 675/675 HB complete cases, including all H1 inputs, and 900/900 HA complete cases are bit-identical. Six P1 repeat-1 double-generation checks matched at seed 20261112, with no outcomes computed. G-event PASS: minimal, original and repeated calls agree within 1e-12. G-abl PASS: 42 APC cases and 23 scan cases at 1e-10. Configuration adapters reproduced the unchanged scan computations exactly.\n",
       'V1 has 175 coupled + 175 paired timing-null inputs (seed 20261110); V2 has 450 + 450 (20261111); V3 has six cells x 100 (20261112); V4 has 25 (20261113). Full HB source sequences were generated to retain the original RNG order, then only H1/H3 or H4 cases were selected; no methods ran on unused source-sequence cases. All signal banks and per-trial truths are saved and hashed.\n',
       'Nine component pipelines and three references were evaluated on every simulation input. Coupling uses the unchanged ablation common phase-band rule, with the selected amplitude-band realization (event half-width 6 Hz). Errors summarize finite estimates; invalid outputs count as recovery failures. AUC uses available finite scores in each class, and finite/complete-pair counts are reported. Its bootstrap resamples paired input IDs together, 10,000 times, seed 20261114.\n',
       'Calibrated F3 / SCAN tests use the maximum normalized scan MVL over every amplitude candidate, 200 common envelope shifts per input, drawn with mrg32k3a seed 20261115 in V1-V4 input order. Shifts are rounded samples from N*(0.25 + 0.5*uniform). p = (1 + exceedances)/201. FFT circular sums were checked against the defining time-domain sums. Invalid tests contribute no rejection and remain in the denominators; valid/invalid counts are shown.\n']
 def section(title,file,cols=None,filter_fn=None):
  d=read(file)
  if filter_fn is not None:d=filter_fn(d)
  if cols is not None:d=d[cols]
  text.extend(['\n## '+title+'\n',md(d),f'\nFull CSV: [{file}]({O/file}).\n'])
 r=P['ecog_precision_resolution']
 text.extend(['\n## ECoG saved-result consistency stop: resolution and audit\n',f"The executor-added 1e-10 absolute saved-F3/SCAN consistency check stopped on ca_movement_020. It was not a protocol gate. The user resolved the difference as floating-point propagation through the narrow low-frequency phase filter and authorized resumption at {r['resume_utc']}, without a protocol amendment or changes to any method. The 39 completed ECoG checkpoints were retained. Both STOPPED.md and STOPPED_ACTIVE.md remain byte-identical; future stops use STOP_RUN.md.\n",'The resumed check requires identical fA, validity, status and NaN pattern; absolute fP difference <=1e-9 Hz; absolute coupling difference <=1e-6 * max(abs(saved coupling), 1e-12). Relative audit differences use max(abs(saved), 1e-12). Newly computed values are used for every reported F3 pipeline; only APC v1.0/v3.0 and A2-prime references use saved values. No new endpoint was inspected to identify or authorize the fix.\n'])
 section('ECoG reproduction-check maxima','ecog_reproduction_maxima.csv',['quantity','maximum','bout_at_maximum','finite_comparisons','n_bouts'])
 text.append(f'Full per-bout audit: [ecog_reproduction_check.csv]({O/"ecog_reproduction_check.csv"}). All 2642 bouts passed.\n')
 section('Primary decisions','primary_decisions.csv',['endpoint','decision'])
 for endpoint,file in [('P-A','P_A.csv'),('P-B','P_B.csv'),('P-C','P_C.csv')]:section(endpoint,file,[c for c in read(file).columns if c not in ['git_commit','protocol_sha256','provenance_file']])
 section('V3 source recovery and dominant-rhythm picks','P_C_source_recovery.csv',['cell','source','n','finite','fp_recovery','strict_fp_recovery','dominant_picks','dominant_pick_rate','mean_abs_fp_error','median_abs_fp_error','ci_low','ci_high'])
 section('Secondary recovery and errors','recovery_overall.csv',['suite','method','n','valid','joint','strict_joint','fp_only','fa_only','mean_abs_fp_error','median_abs_fp_error','mean_abs_fa_error','median_abs_fa_error'])
 section('False joint recovery','false_joint_recovery.csv',['suite','method','n','valid','joint','joint_ci_low','joint_ci_high'])
 section('Coupled vs paired-null AUC','coupling_auc.csv',['suite','method','pairs','finite_coupled','finite_null','complete_pairs','auc','ci_low','ci_high'])
 section('Calibrated specificity and power','calibrated_specificity.csv',['suite','dataset','n','valid','invalid','rejections','rate','ci_low','ci_high'])
 section('End-to-end reference agreement','endtoend_agreement.csv',[c for c in read('endtoend_agreement.csv').columns if c not in ['git_commit','protocol_sha256','provenance_file']])
 section('Finite Step-2 estimates after later APC failure: simulations','simulation_retained_step2_counts.csv',['suite','dataset','source','n','finite_step2','finite_step2_later_failed'])
 text.extend(['\n## Real-data reuse and statistics\n','Saved channels, bouts, eligibility, electrodes and prep files were reused unchanged. There are 3,646 unique rodent physical inputs, mapped to 3,982 regional/bout-set rows; the prespecified 5-s and POST HOC 2-s results remain separate. ECoG has 2,642 eligible bouts, 18 movement-recording patients and seven imagery-recording patients. The agreement denominator remains the prescribed 18, with observed patient counts shown separately.\n',
 'Rodent APC-v1.0 reference values are retained from each original bout-set/analysis row. Saved A2\' selected pairs are remeasured with the common ablation coupling phase rule. ECoG APC v1.0/v3.0 and A2\' common coupling are reused from the completed ablation; the recomputed F3 / SCAN coordinates, status and coupling pass the user-resolved consistency check reported above. F1/F2 source counts reuse end-to-end statuses and recover missing Step-2 estimates only when needed.\n',
 'Rodent per-session computations reuse the original statistical helper definitions and bout-bootstrap procedure: independent run/rest resampling, shared indices across methods, 10,000 resamples, seed 20261022. Across-session percentile bootstrap CIs resample session differences (10,000); one-sample t and signed-rank values are also provided. ECoG E4 uses the ablation procedure and patient bootstrap seed 20261024.\n'])
 section('Prespecified 5-s rodent: across sessions','rodent_across_session_statistics.csv',['analysis','animal_pool','method','outcome','n_sessions','mean_session_difference','ci_low','ci_high','one_sample_p','wilcoxon_p'],lambda d:d[d.bout_set=='prespecified_5s'])
 section('POST HOC 2-s rodent: across sessions','rodent_across_session_statistics.csv',['analysis','animal_pool','method','outcome','n_sessions','mean_session_difference','ci_low','ci_high','one_sample_p','wilcoxon_p'],lambda d:d[d.bout_set=='POST_HOC_2s'])
 section('Prespecified 5-s rodent: within-state fP SD','rodent_within_state_summary.csv',['analysis','animal_pool','method','state','n_sessions','mean_fp_sd','median_fp_sd'],lambda d:d[d.bout_set=='prespecified_5s'])
 section('POST HOC 2-s rodent: within-state fP SD','rodent_within_state_summary.csv',['analysis','animal_pool','method','state','n_sessions','mean_fp_sd','median_fp_sd'],lambda d:d[d.bout_set=='POST_HOC_2s'])
 section('ECoG descriptive endpoints','ecog_summary.csv',['recording','method','patients','rest_agreement_count','rest_agreement_denominator','mean_move_minus_rest','ci_low','ci_high','median_rest_fp_sd','median_move_fp_sd'])
 section('Finite Step-2 estimates after later APC failure: real data','real_retained_step2_counts.csv',[c for c in read('real_retained_step2_counts.csv').columns if c not in ['git_commit','protocol_sha256','provenance_file']])
 text.extend(['\n## Detailed tables\n'])
 for file in ['recovery_by_level.csv','simulation_trial_estimates.csv','simulation_truths.csv','calibrated_trial_tests.csv','coupling_auc_bootstrap.csv','rodent_bout_estimates.csv','rodent_session_statistics.csv','rodent_state_summary.csv','rodent_within_state_spread.csv','rodent_sources.csv','ecog_bout_estimates.csv','ecog_patient_summary.csv','ecog_patient_bootstrap.csv','ecog_sources.csv','statistics.csv']:
  text.append(f'- [{file}]({O/file})\n')
 text.append('\n## Figures\n')
 for fig in figures:text.append(f"- {fig['name']}: [300-dpi PNG]({fig['png']}), [SVG]({fig['svg']}). Commit and source-CSV hashes are embedded in metadata; no titles or footers appear inside the image.\n")
 text.extend(['\n## Runtime and deviations\n',f"Statistics elapsed: {stat['elapsed_seconds']:.3f} seconds. Gate elapsed: {g['elapsed_seconds']:.3f} seconds. Generator elapsed: {json.loads((O/'generation_complete.json').read_text(encoding='utf-8'))['elapsed_seconds']:.3f} seconds after the tooling restart. Worker runtimes are recorded individually below.\n"])
 runtime=[]
 for w in range(1,5):
  for prefix in ['worker','real_worker']:
   q=json.loads((O/f'{prefix}{w}_complete.json').read_text(encoding='utf-8'));runtime.append({'stage':prefix,'worker':w,'seconds':q['elapsed_seconds']})
 text.append(md(pd.DataFrame(runtime)))
 text.append('Statistics runtime basis: '+stat.get('elapsed_seconds_basis','internal timer')+'. Metadata-only collation recovery: '+str(stat.get('collation_recovery_seconds',0))+' seconds. No numerical statistical calculation was repeated.\n')
 wall=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(P['resume_utc'])).total_seconds()
 text.append(f'\nWall time since Amendment-1 resume: {wall:.1f} seconds ({wall/3600:.3f} hours), including interruptions. Real-worker times above describe the successful ECoG resume, including checkpoint restoration; earlier rodent processing and the stopped CSV-conversion attempt are retained in tooling_saved_boolean_attempt1/worker*_resume_matlab.log. They are not included in those resumed-worker timers.\n')
 for d in dev['deviations']:text.append('\n- **'+d['code']+'**: '+d['reason']+' '+d['fix']+'\n')
 text.append('\nNo protocol, tagged method, seed, grid or tolerance was changed. New validation results are uncommitted. Provenance, input/source hashes, implementation hashes and environment versions are in [provenance.json]('+str(O/'provenance.json')+').\n')
 (O/'RESULTS_validation.md').write_text('\n'.join(text),encoding='utf-8')
def main():
 assert json.loads((O/'statistics_complete.json').read_text(encoding='utf-8'))['status']=='COMPLETE';plot_figures();report();print(json.dumps({'status':'COMPLETE','figures':len(figures),'report':str(O/'RESULTS_validation.md')},indent=2))
if __name__=='__main__':main()
