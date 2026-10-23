"""Summarise saved gates and held-out estimates; never call an estimator."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys,subprocess,os
O=Path(__file__).resolve().parent;R=O.parent.parent;repo=R/'apc-brainstorm-publish';sys.path.insert(0,str(R/'pydeps'))
os.environ['MPLCONFIGDIR']=str(O/'.matplotlib');(O/'.matplotlib').mkdir(exist_ok=True)
import pandas as pd
import numpy as np
from scipy.stats import binomtest
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def js(n):return json.loads((O/n).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def link(n,label=None):
    p=Path(n);p=p if p.is_absolute() else O/p
    return f'[{label or p.name}](<{p.as_posix()}>)'
def table(d,cols=None):
    if cols is None:cols=list(d.columns)
    def fmt(x):
        if pd.isna(x):return 'NA'
        if isinstance(x,(float,np.floating)):return f'{x:.7g}'
        return str(x).replace('|','/')
    return '\n| '+' | '.join(cols)+' |\n| '+' | '.join('---' for _ in cols)+' |\n'+'\n'.join('| '+' | '.join(fmt(r[c]) for c in cols)+' |' for _,r in d.iterrows())+'\n'
m=js('phaseB_implementation.json');gate=js('gate_results.json');g0=js('G0.json');G=pd.read_csv(O/'gate_trials.csv',encoding='utf-8',float_precision='round_trip');cells=pd.read_csv(O/'G2_cell_summary.csv',encoding='utf-8')
for rec in m['implementation_sha256']:assert sha(Path(rec['path']))==rec['sha256']
for rec in m['evaluation_dependencies_sha256']:assert sha(Path(rec['path']))==rec['sha256']
if (O/'execution_sources.json').exists():
    for rec in js('execution_sources.json')['files']:assert sha(Path(rec['path']))==rec['sha256']
assert sha(repo/'protocol/APC_v3_aperiodic_protocol.md')==m['protocol_sha256']
for rec in js('attempt1_archive_manifest.json')['moved_files']:assert sha(O/rec['archived_path'])==rec['sha256']
def csv(d,name):
    d=d.copy();d['git_commit']=m['freeze_commit'];d['git_tag']='v3.0';d['protocol_sha256']=m['protocol_sha256'];d['provenance_record']='phaseB_implementation.json';d.to_csv(O/name,index=False,encoding='utf-8',float_format='%.17g')
gates=pd.DataFrame([dict(gate=k,result=v) for k,v in gate['gates'].items()]);csv(gates,'gate_summary.csv')
g3=[]
for (beta,T),d in G[G.gate.eq('G3')].groupby(['beta','duration_s']):
    fp=d.fP_hz.dropna();g3.append(dict(beta=beta,duration_s=T,n=len(d),status3=int(d.status.eq(3).sum()),status3_rate=d.status.eq(3).mean(),status0=int(d.status.eq(0).sum()),finite_fp=len(fp),fp_min=fp.min(),fp_q25=fp.quantile(.25),fp_median=fp.median(),fp_q75=fp.quantile(.75),fp_max=fp.max(),status_counts=json.dumps(d.status.value_counts().sort_index().to_dict())))
g3=pd.DataFrame(g3);csv(g3,'G3_summary.csv')
branches=G.groupby(['gate','beta','duration_s','method','location_branch'],dropna=False).size().reset_index(name='trials');csv(branches,'gate_location_branch_counts.csv')
old=pd.read_csv(O/'attempt1_residual_location/gate_trials.csv',encoding='utf-8',float_precision='round_trip');old=old[old.gate.eq('G1')].iloc[0];g1=G[G.gate.eq('G1')]
canon=pd.DataFrame(dict(metric=['fP_hz','fA_hz','raw_MVL','preferred_phase_deg'],expected=g0['canonical_expected'],observed=g0['canonical_observed'],absolute_difference=g0['canonical_absolute_differences']))
lines=['# APC v3.0: aperiodic-corrected Step 2','',
       '## Protocol, freeze and provenance','',
       f'Amendment 1 was public at `c6b669962369cc97e3ab2635e583b48386152472` before the amended method code was written. Protocol SHA-256 `{m["protocol_sha256"]}` matches. G0-G2 passed; code, gate code and the HA generator were frozen at `{m["freeze_commit"]}` (`v3.0`) and pushed before any held-out input was generated. The repository was clean at freeze. No results were committed. MATLAB {m["matlab_version"]}; full toolbox versions, source hashes and execution conventions: '+link('provenance.json')+'; '+link('phaseA_implementation.json')+'; '+link('phaseB_implementation.json')+'; '+link('freeze_precheck.json')+'.','',
       'Default v1 and the v2 path retain their original calculations. The amended helper changes only peak location after unchanged candidate detection: raw-log-power hill climb within the contiguous positive-residual region (`raw_local_max`), otherwise residual refinement of the original candidate (`residual_shoulder`). SP-raw shares the helper. Sigma is sample SD; parabolic displacement is bounded to +/-0.5 bin. '+link('amendment1_peak_location.diff')+'.','',
       'The committed LF endings of `bst_apc.m` were restored without changing its text. Plain `git diff --stat v1.0 -- src/bst_apc.m`: 260 insertions, zero deletions (211 pre-existing v2 additions). Removing v3 additions/version switch restores the pre-v3 source text exactly. '+link('bst_apc_line_endings_and_diff.json')+'; '+link('source_additions_verification.json')+'; '+link('v3_implementation.diff')+'.','',
       '## Attempt 1 (residual-based location)','',
       f'G0 passed. G1 returned status {int(old.status)}, fP {old.fP_hz:.17g} Hz and fA {old.fA_hz:.17g} Hz. The fP error was {abs(old.fP_hz-8):.17g} Hz, exceeding 0.1 Hz; the fA error was within 8 Hz. The run stopped at G1. G2/G3, freeze and held-out evaluation did not run.','',
       'Attempt-1 outputs, STOPPED/status files, logs, implementation diff and source snapshots are preserved unchanged in '+link('attempt1_residual_location')+'. The uncommitted helper/SP-raw source and `bst_apc.m` diff were also snapshotted before Amendment 1. All archived SHA-256 values were rechecked: '+link('attempt1_archive_manifest.json')+'.','',
       '## Phase A gates','',table(gates),
       'G0 canonical tolerance 1e-10:',table(canon),
       f'Complete v1 output/runInfo equality against tag v1.0: {g0["v1_tag_complete_structures_exact"]}; default versus explicit v1: {g0["default_explicit_v1_exact"]}; complete v2 output/runInfo equality against tag v2.0: {g0["v2_tag_complete_structures_exact"]}. Full tagged/current results: '+link('G0.mat')+'; '+link('G0.json')+'; '+link('G0_trials.csv')+'.','',
       'G1 canonical v3 (required status 0, |fP-8| <=0.1 Hz and |fA-120| <=8 Hz):',table(g1,['status','fP_hz','fA_hz','score','exponent','offset','peak_height','sigma','location_branch']),
       'Complete diagnostics and curves: '+link('G1.mat')+'; '+link('G1_curve.csv')+'.','',
       'G2: seed 20261031; 20 paired repeats per cell; recovery requires status 0 and |fP-15| <=1 Hz. Every cell requires at least 16/20. Status arrays below are ordered 0,1,2,3,4,5.',table(cells,['beta','duration_s','repeats','v3_fp_recovery','v1_fp_recovery','v3_status_counts','v1_status_counts','passed']),
       'G3: seed 20261031, no-rhythm Poisson bursts; descriptive only. Frequency quantiles use finite returned fP; invalid outputs and status counts are retained.',table(g3),
       'Per-trial branch labels (including `not_reached` before location and `not_applicable` for v1/v2), frequencies, diagnostics, status and provenance: '+link('gate_trials.csv')+'; '+link('G0_trials.csv')+'. Branch counts: '+link('gate_location_branch_counts.csv')+'. All curves and complete signal/output MAT files are preserved.','']
complete=all((O/f'worker{w}_complete.json').exists() for w in range(1,5))
criteria=None;recommended=None
cached_criteria=js('criteria_decisions.json')['criteria'] if (O/'criteria_decisions.json').exists() else None
if complete:
    D=pd.concat([pd.read_csv(O/f'{s}_worker{w}_trials.csv',encoding='utf-8',float_precision='round_trip') for s in ['HA','HB'] for w in range(1,5)],ignore_index=True)
    assert len(D)==1575*7 and not D.duplicated(['suite','input_id','method']).any()
    assert D.git_commit.eq(m['freeze_commit']).all() and D.protocol_sha256.eq(m['protocol_sha256']).all()
    assert len(D[D.suite.eq('HA')])==900*7 and len(D[D.suite.eq('HB')])==675*7
    D['fp_abs_error_hz']=(D.recovered_fp_hz-D.true_fp_hz).abs();D['fa_abs_error_hz']=(D.recovered_fa_hz-D.true_fa_hz).abs()
    D['fp_correct']=D.valid & D.fp_abs_error_hz.le(1);D['fa_correct']=D.valid & D.fa_abs_error_hz.le(8)
    D['joint_correct']=D.fp_correct & D.fa_correct;D['strict_joint_correct']=D.valid & D.fp_abs_error_hz.le(.5) & D.fa_abs_error_hz.le(8)
    D=D.sort_values(['suite','input_id','method']);csv(D,'heldout_trial_estimates.csv')
    def wilson(k,n):
        z=1.959963984540054;p=k/n;q=1+z*z/n;c=(p+z*z/(2*n))/q;h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/q
        return c-h,c+h
    def summarise(d):
        row=dict(n=len(d),valid=int(d.valid.sum()),status_counts=json.dumps(d.status.value_counts().sort_index().to_dict()))
        for metric,col in [('joint','joint_correct'),('strict_joint','strict_joint_correct'),('fp','fp_correct'),('fa','fa_correct')]:
            k=int(d[col].sum());lo,hi=wilson(k,len(d));row.update({metric:k,metric+'_rate':k/len(d),metric+'_ci_low':lo,metric+'_ci_high':hi})
        for axis in ['fp','fa']:
            v=d[axis+'_abs_error_hz'].dropna();row.update({axis+'_finite':len(v),axis+'_mean_abs_error_hz':v.mean(),axis+'_median_abs_error_hz':v.median()})
        if d.method.iloc[0]=='SP-raw':
            for prefix in ['joint','strict_joint','fa']:
                for col in list(row):
                    if col==prefix or col.startswith(prefix+'_'):row[col]=np.nan
        return row
    group=['suite','scenario','dataset','level','beta','rhythm_amplitude','duration_s','method'];summary=[]
    for key,d in D.groupby(group,dropna=False,sort=True):summary.append(dict(zip(group,key))|summarise(d))
    S=pd.DataFrame(summary);csv(S,'recovery_by_cell.csv')
    pooled=[]
    masks={'HA_coupled':D.suite.eq('HA')&D.dataset.eq('coupled'),'HA_timing_null':D.suite.eq('HA')&D.dataset.eq('timing_null'),'H1':D.suite.eq('HB')&D.scenario.str.startswith('H1')&D.dataset.eq('coupled'),'H2':D.suite.eq('HB')&D.scenario.eq('H2')&D.dataset.eq('coupled'),'H4':D.suite.eq('HB')&D.scenario.eq('H4')&D.dataset.eq('coupled'),'H3_timing_null':D.suite.eq('HB')&D.dataset.eq('timing_null'),'HB_no_coupled_burst':D.suite.eq('HB')&D.dataset.eq('no_coupled_burst')}
    for name,mask in masks.items():
        for method,d in D[mask].groupby('method'):pooled.append(dict(set=name,method=method)|summarise(d))
    P=pd.DataFrame(pooled);csv(P,'pooled_recovery.csv')
    def paired(mask,metric,a='APC-v3.0',b='APC-v1.0',alternative='greater'):
        p=D[mask & D.method.isin([a,b])].pivot(index=['suite','input_id'],columns='method',values=metric);assert not p.isna().any().any()
        wins=int((p[a]&~p[b]).sum());losses=int((~p[a]&p[b]).sum());discord=wins+losses
        if cached_criteria:
            saved=[cached_criteria['A1'],cached_criteria['A2'],*cached_criteria['A3'],cached_criteria['A4']]
            saved=[z for z in saved if z['n']==len(p) and z['method_a']==a and z['method_b']==b and z['alternative']==alternative];assert len(saved)==1
            z=saved[0];assert z['a_only']==wins and z['b_only']==losses and z['a_success']==int(p[a].sum()) and z['b_success']==int(p[b].sum());pvalue=z['p_value']
        else:pvalue=float(binomtest(wins,discord,.5,alternative=alternative).pvalue) if discord else 1.0
        return dict(n=len(p),method_a=a,method_b=b,a_success=int(p[a].sum()),b_success=int(p[b].sum()),a_only=wins,b_only=losses,both=int((p[a]&p[b]).sum()),neither=int((~p[a]&~p[b]).sum()),p_value=pvalue,alternative=alternative)
    A1=paired(masks['HA_coupled'],'joint_correct');A1['passed']=A1['a_success']>A1['b_success'] and A1['p_value']<.05
    A2=paired(masks['HA_coupled'],'fp_correct',b='SP-raw',alternative='two-sided')
    a3=[]
    for name,margin,n in [('H1',10,175),('H2',10,150),('H4',3,25)]:
        z=paired(masks[name],'joint_correct');assert z['n']==n;z.update(criterion='A3',set=name,allowed_loss=margin,minimum_v3=z['b_success']-margin,passed=z['a_success']>=z['b_success']-margin);a3.append(z)
    nullmask=masks['HA_timing_null']|masks['H3_timing_null'];A4=paired(nullmask,'joint_correct',alternative='two-sided');assert A4['n']==700
    A4.update(v3_false_joint_rate=A4['a_success']/A4['n'],v1_false_joint_rate=A4['b_success']/A4['n']);A4['difference_pp']=100*(A4['v3_false_joint_rate']-A4['v1_false_joint_rate']);A4['passed']=A4['difference_pp']<=5+1e-12
    criteria=dict(A1=A1,A2=A2,A3=a3,A4=A4);recommended=bool(A1['passed'] and all(z['passed'] for z in a3) and A4['passed'])
    decision='v3.0 recommended' if recommended else 'v3.0 not recommended'
    lines[2:2]=[f'**{decision}.** G0-G2 passed. Adoption checks: A1 {"PASS" if A1["passed"] else "FAIL"}; A3 {"PASS" if all(z["passed"] for z in a3) else "FAIL"}; A4 {"PASS" if A4["passed"] else "FAIL"}. '+('Phase C remains to be completed.' if recommended else 'Phase C was not run under the stopping rule.'),'']
    (O/'criteria_decisions.json').write_text(json.dumps(dict(decision=decision,criteria=criteria,provenance=m),indent=2),encoding='utf-8')
    C=pd.DataFrame([dict(criterion='A1',set='HA',**A1),dict(criterion='A2 (secondary)',set='HA fP',**A2),*a3,dict(criterion='A4',set='H3 + HA timing null',**A4)]);csv(C,'criteria_decisions.csv')
    B=D.groupby(['suite','scenario','dataset','method','location_branch'],dropna=False).size().reset_index(name='trials');csv(B,'heldout_location_branches.csv')
    guards=pd.concat([pd.read_csv(O/f'filter_guards_w{w}.csv',encoding='utf-8',float_precision='round_trip') for w in range(1,5)]).drop_duplicates();assert guards.guard_passed.all() and guards.max_pole_radius.lt(1).all() and (guards.center_gain-1).abs().lt(1e-3).all();csv(guards,'filter_guards.csv')
    lines+=['## Phase B: held-out evaluation','',
            'All 675 regenerated HB cases were bit-identical to the original complete saved cases. Before any held-out v3/SP-raw/scan estimate, all 675 v1 outputs reproduced original unrounded MAT values exactly (fP, fA, score, status and route). '+link('HB_signal_verification.json')+'; '+link('HB_v1_equivalence.csv')+'; '+link('HB_VERIFIED.json')+'.','',
            'HA: seed 20261101; 18 cells x 25 coupled trials plus 450 paired timing nulls; fs 1000 Hz. The committed generator uses the development-family power-law construction and 0.18 background-burst recipe. Draw/stream/envelope conventions were fixed before generation in '+link('freeze_precheck.json')+'. Independent saved-input audit passed all cell counts, dimensions, finite-signal, unit-SD noise, carrier/rhythm and paired-component checks; maximum pair residual 8.881784197001252e-16. '+link('input_bank_audit.json')+'. HB: seed 20261022; original 350 coupled inputs, 250 timing nulls and 75 no-coupled-burst controls. H3 in A4 is all 250 original timing nulls; no-coupled-burst controls are reported separately.','',
            'HA APC range [80,150] Hz, defaults otherwise. HB retains the original [80,160] Hz range for exact saved-v1 reproduction, also used for v3. HA scans: phase 3:0.5:30, amplitude 80:4:160, amplitude half-width 30 Hz. HB scans retain phase 3:0.5:14 and amplitude half-width 14 Hz. All phase half-widths 1.5 Hz. Metrics and ties are unchanged; only the HA profile was added to a copy of the SOS scan helper. '+link('comparator_HA_profile.diff')+'; '+link('HB_generator_wrapper.diff')+'.','',
            f'All {len(guards)} unique recorded SOS designs passed pole-radius and centre-gain guards. Maximum pole radius {guards.max_pole_radius.max():.17g}; maximum |centre gain-1| {(guards.center_gain-1).abs().max():.17g}. '+link('filter_guards.csv')+'.','',
            'Invalid outputs count as failures. SP-raw estimates fP only; joint/fA entries are NA. Recovery is inclusive +/-1 Hz fP and +/-8 Hz fA; strict joint uses +/-0.5 Hz fP. All proportions have Wilson 95% CIs in the CSVs. Errors describe finite returned estimates; denominators and all status counts are supplied.','',
            '## A1-A4 and adoption decision','',f'**{decision}.**',table(C,['criterion','set','n','a_success','b_success','a_only','b_only','p_value','passed']),
            'A1 uses a one-sided exact binomial McNemar test. A3 requires v3 >= v1 minus 10/175 (H1), 10/150 (H2), and 3/25 (H4), each separately. A4 allows at most +5 percentage points of false joint recovery over the 700 pooled timing nulls. A2 is secondary and does not gate adoption. The A3/A4 p values are descriptive paired comparisons; their decisions use only the fixed count/rate bounds.','',
            '### A2: does burst timing add fP information beyond SP-raw?','',
            f'HA fP recovery: v3 {A2["a_success"]}/{A2["n"]}, SP-raw {A2["b_success"]}/{A2["n"]}; v3-only {A2["a_only"]}, SP-raw-only {A2["b_only"]}; two-sided exact McNemar p={A2["p_value"]:.12g}.','',
            f'A4 false joint recovery: v3 {A4["a_success"]}/700 ({A4["v3_false_joint_rate"]:.6%}), v1 {A4["b_success"]}/700 ({A4["v1_false_joint_rate"]:.6%}); difference {A4["difference_pp"]:.7g} percentage points.','',
            'Complete paired discordance tables/decisions: '+link('criteria_decisions.csv')+'; '+link('criteria_decisions.json')+'.','',
            '## Pooled recovery','',table(P,['set','method','n','valid','joint','strict_joint','fp','fa','status_counts']),
            'Complete Wilson CIs and finite-error summaries: '+link('pooled_recovery.csv')+'.','',
            '## HA recovery by cell','',table(S[S.suite.eq('HA')],['dataset','beta','rhythm_amplitude','duration_s','method','n','valid','joint','strict_joint','fp','fa','status_counts']),
            '## HB recovery by level','',table(S[S.suite.eq('HB')],['scenario','dataset','level','method','n','valid','joint','strict_joint','fp','fa','status_counts']),
            'All per-trial estimates/options/generator settings/provenance: '+link('heldout_trial_estimates.csv')+'. Full cell statistics, errors and Wilson intervals: '+link('recovery_by_cell.csv')+'. Complete checkpoint MAT files preserve estimator output/diagnostics; no estimator was called during reporting.','']
    # A best scan is descriptive, chosen within each HA cell by its own endpoint.
    metric_order=['MVL-raw','MVL-Ozkurt','KLMI','GLM'];best=[]
    ha=S[S.suite.eq('HA')&S.dataset.eq('coupled')]
    for key,d in ha.groupby(['beta','rhythm_amplitude','duration_s']):
        scans=d[d.method.isin(metric_order)].copy();scans['tie']=scans.method.map({z:i for i,z in enumerate(metric_order)})
        for endpoint in ['joint','fp']:
            z=scans.sort_values([endpoint,'tie'],ascending=[False,True]).iloc[0];best.append(dict(beta=key[0],rhythm_amplitude=key[1],duration_s=key[2],endpoint=endpoint,method=z.method,count=z[endpoint],n=z.n))
    best=pd.DataFrame(best);csv(best,'HA_best_A2_prime.csv')
    figs=[];colors={'APC-v1.0':'#0072B2','APC-v3.0':'#D55E00','SP-raw':'#009E73','Best A2\u2032':'#5e3c99'}
    for endpoint in ['joint','fp']:
        fig,axes=plt.subplots(2,3,figsize=(10.8,6.6),sharey=True)
        for ir,T in enumerate([2,6]):
            for ic,beta in enumerate([1,1.5,2]):
                ax=axes[ir,ic];d=ha[ha.beta.eq(beta)&ha.duration_s.eq(T)]
                methods=['APC-v1.0','APC-v3.0']+(['SP-raw'] if endpoint=='fp' else [])+['Best A2\u2032']
                for method in methods:
                    values=[];low=[];high=[]
                    for amp in [.3,.5,.8]:
                        if method=='Best A2\u2032':
                            b=best[best.beta.eq(beta)&best.duration_s.eq(T)&best.rhythm_amplitude.eq(amp)&best.endpoint.eq(endpoint)].iloc[0];z=d[d.rhythm_amplitude.eq(amp)&d.method.eq(b.method)].iloc[0]
                        else:z=d[d.rhythm_amplitude.eq(amp)&d.method.eq(method)].iloc[0]
                        values.append(z[endpoint+'_rate']);low.append(z[endpoint+'_rate']-z[endpoint+'_ci_low']);high.append(z[endpoint+'_ci_high']-z[endpoint+'_rate'])
                    ax.errorbar([.3,.5,.8],values,yerr=np.maximum([low,high],0),color=colors[method],marker='o',markersize=3,capsize=2,lw=1.2,label=method)
                ax.set(ylim=(-.03,1.03),xticks=[.3,.5,.8],xlabel=f'Rhythm amplitude (\u03b2={beta:g}, T={T} s)');ax.spines[['top','right']].set_visible(False)
                if ic==0:ax.set_ylabel(('Joint' if endpoint=='joint' else 'fP')+' recovery')
        handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',ncol=4,frameon=False);fig.tight_layout(rect=[0,0,1,.95]);name='HA_'+endpoint+'_recovery';meta=f'git={m["freeze_commit"]}; tag=v3.0; protocol_sha256={m["protocol_sha256"]}; source=recovery_by_cell.csv; source_sha256={sha(O/"recovery_by_cell.csv")}; best=HA_best_A2_prime.csv; best_sha256={sha(O/"HA_best_A2_prime.csv")}; Wilson 95% CI'
        fig.savefig(O/(name+'.png'),dpi=300,metadata={'Description':meta});fig.savefig(O/(name+'.svg'),metadata={'Description':meta});plt.close(fig);figs.append(name)
    lines+=['## Figures','']
    for name in figs:lines.append('- '+link(name+'.png')+' (300 dpi); '+link(name+'.svg')+'.')
    lines+=['','Figures contain no titles or footers. Embedded metadata identifies freeze commit/tag, protocol hash and source CSVs. Best A2\u2032 is descriptive, selected per cell separately for joint/fP recovery in fixed metric tie order [MVL-raw, MVL-Ozkurt, KLMI, GLM]; no method parameter changed. SP-raw is shown only in the fP figure because it does not estimate fA.','',
            '## Phase C','',('A1, A3 and A4 passed; Phase C is authorized and remains to be completed.' if recommended else 'At least one required adoption criterion failed. The protocol stops here; v3.0 is not recommended. Phase C rodent/ECoG analyses and the conditional ECoG figure were not run. No method redesign or additional candidate was made.'),'']
    if not recommended:
        (O/'STOPPED.md').write_text('# STOPPED: APC v3.0 adoption criteria failed\n\n'+decision+'. Required criteria: A1='+str(A1['passed'])+', A3='+str(all(z['passed'] for z in a3))+', A4='+str(A4['passed'])+'. The completed Phase B results are reported in RESULTS_v3.md and criteria_decisions.json. No Phase C, workaround or method redesign was run.\n',encoding='utf-8')
else:
    lines+=['## Phase B status','']
    if (O/'STOPPED.md').exists():lines += ['A method-relevant execution check stopped Phase B. '+link('STOPPED.md')+'. Completed checkpoints and logs are retained; no adoption decision is available.','']
    else:lines += ['Held-out generation/equivalence/evaluation is in progress. Adoption criteria are not yet evaluated.','']
lines+=['## Runtime and deviations','',f'Amendment-1 Phase-A gate timer: {gate["elapsed_seconds"]:.3f} s, excluding MATLAB startup. Gates were repeated once under Amendment 1. Each reportable held-out input/method is evaluated once; finished checkpoint outputs are reused, not recomputed.','']
for name in ['generation_runtime.json',*[f'worker{w}_complete.json' for w in range(1,5)]]:
    if (O/name).exists():z=js(name);lines.append(f'- {name}: {z["elapsed_seconds"]:.3f} s (worker timers include the equivalence-release wait).')
for d in js('deviations.json')['deviations']:lines.append('- '+d['type']+': '+d['reason'])
lines+=['- MATLAB startup emitted warnings about missing historical Brainstorm paths. Drivers verify repository source precedence and use explicit analysis paths.','- HB retains its original APC [80,160]-Hz amplitude range as required to reproduce the saved suite; HA uses the default [80,150]-Hz range. This execution choice was recorded before held-out generation.','',
        'No protocol, tagged method or fixed setting was edited after its run started. Full options/settings are stored with each result/checkpoint and referenced provenance. Archive and source hashes were rechecked while generating this report.','']
(O/'RESULTS_v3.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
status=dict(status=('PHASE_C_PENDING' if recommended else 'STOPPED_CRITERION_FAILURE') if complete else ('STOPPED_METHOD_PROBLEM' if (O/'STOPPED.md').exists() else 'PHASE_B_IN_PROGRESS'),freeze_commit=m['freeze_commit'],git_tag='v3.0',protocol_sha256=m['protocol_sha256'],gates=gate['gates'],recommended=recommended,phaseB_complete=complete,results_committed=False,updated_utc=datetime.now(timezone.utc).isoformat())
(O/'STATUS.json').write_text(json.dumps(status,indent=2),encoding='utf-8');p=js('provenance.json');p.update(status=status['status'],heldout_generated=(O/'generation_runtime.json').exists(),gate_results='gate_results.json',results_committed=False);(O/'provenance.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
print(json.dumps(status),flush=True)
