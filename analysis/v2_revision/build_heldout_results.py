"""Summarize the frozen held-out suite and evaluate predeclared C1-C4."""
from pathlib import Path
from collections import defaultdict,Counter
import csv,hashlib,json,math,os,re,statistics,subprocess,sys,time
A=Path(__file__).resolve().parent;REPO=A.parent.parent;ROOT=REPO.parent
OUT=ROOT/'revision_checks/v2/candidate_03'
GIT=r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe'
KEYS=['scenario','dataset','level','configuration','method']
PROV=['git_commit','matlab_version','seed','apc_options_json','comparator_settings_json']
METRICS=['MVL-raw','MVL-Ozkurt','KLMI','GLM']
def git(*a):return subprocess.check_output([GIT,'-C',str(REPO),*a],encoding='utf-8').strip()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def write(p,rows):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def num(r,k):return float(r[k])
def finite(x):return math.isfinite(x)
def mean(v):return statistics.mean(v) if v else math.nan
def median(v):return statistics.median(v) if v else math.nan
def link(p,label=None):return f'[{label or p.name}](<{p.as_posix()}>)'
def table(head,rows):
    def esc(x):return (f'{x:.6g}' if isinstance(x,float) else str(x)).replace('|','\\|').replace('\n',' ')
    return '\n'.join(['| '+' | '.join(map(esc,head))+' |','| '+' | '.join(['---']*len(head))+' |']+['| '+' | '.join(map(esc,r))+' |' for r in rows])
def success(r,strict=False):
    return r['valid']=='1' and abs(num(r,'recovered_fp_hz')-num(r,'true_fp_hz'))<=(.5 if strict else 1) and abs(num(r,'recovered_fa_hz')-num(r,'true_fa_hz'))<=8
def summarize(rows):
    groups=defaultdict(list)
    for r in rows:groups[tuple(r[k] for k in KEYS)].append(r)
    out=[]
    for key,rr in groups.items():
        assert len(rr)==25 and sorted(int(r['repeat_index']) for r in rr)==list(range(1,26)),key
        pe=[abs(num(r,'recovered_fp_hz')-num(r,'true_fp_hz')) for r in rr];ae=[abs(num(r,'recovered_fa_hz')-num(r,'true_fa_hz')) for r in rr]
        item=dict(zip(KEYS,key));item.update(n_trials=25,n_valid=sum(r['valid']=='1' for r in rr),joint=sum(success(r) for r in rr),strict_joint=sum(success(r,True) for r in rr),
          fP_recovery=sum(r['valid']=='1' and p<=1 for r,p in zip(rr,pe)),fA_recovery=sum(r['valid']=='1' and a<=8 for r,a in zip(rr,ae)),
          mean_fP_error=mean([x for x in pe if finite(x)]),median_fP_error=median([x for x in pe if finite(x)]),mean_fA_error=mean([x for x in ae if finite(x)]),median_fA_error=median([x for x in ae if finite(x)]),
          n_finite_fP=sum(map(finite,pe)),n_finite_fA=sum(map(finite,ae)),picks_near_fD=sum(abs(num(r,'recovered_fp_hz')-num(r,'true_fd_hz'))<=1 for r in rr),
          route_gaussian=sum(r['route']=='gaussian_mvl_scan' for r in rr),diagnostic_warnings=sum(finite(num(r,'diagnostic_flags')) and num(r,'diagnostic_flags')!=0 for r in rr))
        item.update({k:rr[0][k] for k in PROV});out.append(item)
    return out
def auc(c,n):
    c=[x for x in c if finite(x)];n=[x for x in n if finite(x)]
    return (sum((x>y)+.5*(x==y) for x in c for y in n)/(len(c)*len(n)) if c and n else math.nan,len(c),len(n))
def specificity(rows):
    groups=defaultdict(list);coupled={}
    for r in rows:
        if r['dataset']=='coupled':coupled[(r['input_id'],r['configuration'],r['method'])]=r
        else:groups[tuple(r[k] for k in KEYS)].append(r)
    out=[]
    for key,rr in groups.items():
        score_fields=['score']
        if key[3]=='v2.0':score_fields+=['ozkurt_mvl','event_z','event_z_fixed']
        cc=[coupled[(r['paired_coupled_id'],r['configuration'],r['method'])] for r in rr]
        for field in score_fields:
            av,nc,nn=auc([num(r,field) for r in cc],[num(r,field) for r in rr])
            item=dict(zip(KEYS,key));item.update(score_field=field,n_null=25,false_joint=sum(success(r) for r in rr),auc=av,n_coupled_finite=nc,n_null_finite=nn)
            item.update({k:rr[0][k] for k in PROV});out.append(item)
    return out
def rejection_rates(rows):
    groups=defaultdict(list)
    for r in rows:
        if r['configuration']=='v2.0':groups[tuple(r[k] for k in KEYS)].append(r)
    out=[]
    for key,rr in groups.items():
        for field in ['event_p','event_p_fixed']:
            item=dict(zip(KEYS,key));item.update(statistic=field,n_trials=25,n_finite_p=sum(finite(num(r,field)) for r in rr),n_reject=sum(num(r,field)<.05 for r in rr),rejection_rate=sum(num(r,field)<.05 for r in rr)/25)
            item.update({k:rr[0][k] for k in PROV});out.append(item)
    return out
def decide(rows,specific,metadata):
    choices=[]
    def pool(scenarios,levels=None,dataset='coupled',strict=False,minimize=False,criterion=''):
        rr=[r for r in rows if r['scenario'] in scenarios and r['dataset']==dataset and (levels is None or float(r['level']) in levels)]
        groups=defaultdict(list)
        for r in rr:groups[(r['scenario'],r['level'])].append(r)
        v=[];a=[];paired=[]
        for (scenario,level),gg in groups.items():
            primary=sorted([r for r in gg if r['configuration']=='v2.0'],key=lambda r:int(r['repeat_index']))
            assert len(primary)==25
            alternatives={m:sorted([r for r in gg if r['configuration']=='A2_prime' and r['method']==m],key=lambda r:int(r['repeat_index'])) for m in METRICS}
            counts={m:sum(success(r,strict) for r in z) for m,z in alternatives.items()}
            best=min(METRICS,key=lambda m:counts[m]) if minimize else max(METRICS,key=lambda m:counts[m])
            comparator=alternatives[best];v.extend(primary);a.extend(comparator);paired.extend(zip(primary,comparator))
            choices.append({'criterion':criterion,'scenario':scenario,'dataset':dataset,'level':level,'endpoint':'strict_joint' if strict else ('false_joint' if minimize else 'joint'),
             'selected_A2_metric':best,'selected_A2_count':counts[best],**{m+'_count':counts[m] for m in METRICS},'git_commit':metadata['git_commit'],'matlab_version':metadata['matlab_version'],'seed':20261022,
             'apc_options_json':json.dumps(metadata['apc_configurations']),'comparator_settings_json':json.dumps(metadata['comparator_settings'])})
        return v,a,paired
    decisions=[];details={}
    v,a,_=pool(['H2'],{1,1.5,2,3},criterion='C1');assert len(v)==100
    nv=sum(success(r) for r in v);na=sum(success(r) for r in a);wrong=sum(abs(num(r,'recovered_fp_hz')-num(r,'true_fd_hz'))<=1 for r in v)
    passed=nv>=na-5 and wrong<=10
    decisions.append({'criterion':'C1','result':'PASS' if passed else 'FAIL','numbers':f'v2 joint {nv}/100; best A2 joint {na}/100; required >= {na-5}; near-fD {wrong}/100, required <=10'})
    details['C1']={'v2_joint':nv,'best_A2_joint':na,'near_fD':wrong,'n':100,'passed':passed}
    v,a,pairs=pool(['H1_sparsity','H1_distractor'],strict=True,criterion='C2');assert len(v)==175
    nv=sum(success(r,True) for r in v);na=sum(success(r,True) for r in a)
    b=sum(success(x,True) and not success(y,True) for x,y in pairs);c=sum(success(y,True) and not success(x,True) for x,y in pairs);n=b+c
    p=sum(math.comb(n,k) for k in range(b,n+1))/(2**n) if n else 1
    passed=nv>na and p<.05
    decisions.append({'criterion':'C2','result':'PASS' if passed else 'FAIL','numbers':f'v2 strict {nv}/175; best A2 strict {na}/175; discordant v2-only/A2-only={b}/{c}; exact one-sided McNemar p={p:.12g}'})
    details['C2']={'v2_strict':nv,'best_A2_strict':na,'v2_only':b,'A2_only':c,'p_one_sided':p,'n':175,'passed':passed}
    v,a,_=pool(['H1_sparsity','H1_distractor','H2'],dataset='timing_null',minimize=True,criterion='C3');assert len(v)==250
    nv=sum(success(r) for r in v);na=sum(success(r) for r in a)
    required_auc=[r for r in specific if r['dataset']=='timing_null' and r['configuration']=='v2.0' and r['score_field']=='event_z' and
      ((r['scenario']=='H1_sparsity' and float(r['level']) in [1,.55]) or r['scenario']=='H1_distractor')]
    assert len(required_auc)==5
    auc_pass=all(finite(r['auc']) and r['auc']>=.90 for r in required_auc);rate_pass=nv/250<=na/250+.05
    passed=rate_pass and auc_pass
    text='; '.join(f'{r["scenario"]}={r["level"]}: {r["auc"]:.6g}' for r in required_auc)
    decisions.append({'criterion':'C3','result':'PASS' if passed else 'FAIL','numbers':f'false joint v2 {nv}/250 ({100*nv/250:g}/100), best A2 {na}/250 ({100*na/250:g}/100), allowance +5/100; event-z AUCs: '+text})
    details['C3']={'v2_false_joint':nv,'best_A2_false_joint':na,'n':250,'rate_pass':rate_pass,'required_event_z_AUCs':[{k:r[k] for k in ['scenario','level','auc','n_coupled_finite','n_null_finite']} for r in required_auc],'AUC_pass':auc_pass,'passed':passed}
    v,a,_=pool(['H1_sparsity','H1_distractor'],criterion='C4');nv=sum(success(r) for r in v);na=sum(success(r) for r in a);assert len(v)==175
    passed=nv>=na-9
    decisions.append({'criterion':'C4','result':'PASS' if passed else 'FAIL','numbers':f'v2 joint {nv}/175; best A2 joint {na}/175; required >= {na-9}'})
    details['C4']={'v2_joint':nv,'best_A2_joint':na,'n':175,'passed':passed}
    for d in decisions:d.update(git_commit=metadata['git_commit'],matlab_version=metadata['matlab_version'],seed=20261022,apc_options_json=json.dumps(metadata['apc_configurations']),comparator_settings_json=json.dumps(metadata['comparator_settings']))
    return decisions,details,choices
def figures(summary,metadata):
    os.environ['MPLCONFIGDIR']=str(OUT/'plot_config');sys.path.insert(0,str(ROOT/'pydeps'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    configs=[('v2.0','APC'),('v1.0','APC')]+[(c,m) for c in ['A2_prime','A1_prime'] for m in METRICS]
    colors=['#111111','#777777','#0072B2','#D55E00','#009E73','#CC79A7','#0072B2','#D55E00','#009E73','#CC79A7']
    for name,scenarios in [('H1',['H1_sparsity','H1_distractor']),('H2',['H2'])]:
        fig,axes=plt.subplots(1,len(scenarios),figsize=(11 if name=='H1' else 8,6),squeeze=False)
        for ax,scenario in zip(axes[0],scenarios):
            for i,(config,method) in enumerate(configs):
                rr=[r for r in summary if r['scenario']==scenario and r['dataset']=='coupled' and r['configuration']==config and r['method']==method]
                rr.sort(key=lambda r:float(r['level']))
                ax.plot([float(r['level']) for r in rr],[r['joint'] for r in rr],label=config+' '+method,color=colors[i],linestyle='--' if config=='A1_prime' else '-',marker='o' if config.startswith('v') else '.',linewidth=2.4 if config=='v2.0' else 1.3)
            ax.set_ylim(-.5,25.8);ax.set_yticks(range(0,26,5));ax.set_ylabel('Joint recovery /25');ax.set_title(scenario)
            ax.set_xlabel('Burst keep rate' if scenario=='H1_sparsity' else ('Distractor scale' if scenario=='H1_distractor' else 'Slow-distractor amplitude ratio'));ax.grid(alpha=.18)
        handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=5,fontsize=8)
        fig.suptitle('APC v2.0 held-out '+name);fig.text(.5,.125,'Seed 20261022 | '+metadata['git_commit'][:12]+' | phase +/-1 Hz, amplitude +/-8 Hz',ha='center',fontsize=8)
        fig.tight_layout(rect=[0,.16,1,.95])
        for ext in ['png','svg']:fig.savefig(OUT/f'joint_recovery_{name}.{ext}',dpi=220,metadata={'Description':json.dumps(metadata,separators=(',',':'))})
        plt.close(fig)
    return matplotlib.__version__
def main():
    started=time.monotonic();runtimes={k:load(OUT/(k+'_runtime.json')) for k in ['generate','worker_1','worker_2','worker_3']}
    assert all(r['status']=='COMPLETE' for r in runtimes.values());metadata=runtimes['generate']['metadata']
    assert git('rev-parse','HEAD')==git('rev-list','-n','1','v2.0')==metadata['git_commit'];assert not git('status','--porcelain')
    rows=[]
    for worker in [1,2,3]:rows.extend(read(OUT/f'heldout_worker{worker}_trials.csv'))
    rows.sort(key=lambda r:(int(r['input_id']),r['configuration'],r['method']))
    assert len(rows)==6750 and len({(r['input_id'],r['configuration'],r['method']) for r in rows})==6750
    ids=defaultdict(list)
    for r in rows:
        ids[r['input_id']].append(r);assert r['git_commit']==metadata['git_commit'] and r['seed']=='20261022'
        json.loads(r['apc_options_json']);json.loads(r['comparator_settings_json']);json.loads(r['generator_settings_json'])
        if r['configuration']=='v2.0' and r['valid']=='1':assert abs(num(r,'gaussian_sigma_hz')-1.5*num(r,'recovered_fp_hz'))<1e-12
    assert len(ids)==675 and all(len(rr)==10 for rr in ids.values())
    assert Counter(rr[0]['dataset'] for rr in ids.values())=={'coupled':350,'timing_null':250,'no_coupled_burst':75}
    verify=read(OUT/'heldout_null_pair_verification.csv');assert len(verify)==325 and all(num(r,'pair_residual')<=1e-12 for r in verify)
    summary=summarize(rows);specific=specificity(rows);rates=rejection_rates(rows);decisions,details,choices=decide(rows,specific,metadata)
    write(OUT/'heldout_trials.csv',rows);write(OUT/'heldout_recovery_summary.csv',summary);write(OUT/'heldout_null_specificity_auc.csv',specific);write(OUT/'heldout_event_rejection_rates.csv',rates)
    write(OUT/'decision_criteria.csv',decisions);write(OUT/'best_A2_by_level.csv',choices)
    (OUT/'decision_details.json').write_text(json.dumps({'criteria':details,'metadata':metadata},indent=2),encoding='utf-8')
    plot_version=figures(summary,metadata)
    lines=[]
    def p(s=''):lines.append(s+'\n')
    p('# APC v2.0 candidate 3: held-out results')
    p(f'Branch v2-revision; frozen tag `v2.0`; commit `{metadata["git_commit"]}`. The tagged method source matches the candidate-3 unit-tested source. All held-out inputs were generated only after tagging; seed 20261022.')
    p('## Factual summary (9 lines)')
    facts=[f'Frozen source: {metadata["git_commit"]}; tag v2.0.',
      'Gates (a), (a2), (b), (c) passed; (d) completed all 25 existing trials.',
      'The ten Poisson unit trials all had corrected event p>0.05.',
      'Held-out inputs: 350 coupled, 250 timing null and 75 no-coupled-burst controls; ten methods/configurations per input.',
      f'Per-trial rows: {len(rows)}; summary groups: {len(summary)}; all 325 null subtraction checks passed.',
      f'C1: {decisions[0]["result"]}; C2: {decisions[1]["result"]}.',
      f'C3: {decisions[2]["result"]}; C4: {decisions[3]["result"]}.',
      'tPAC was skipped: its function was absent from the configured MATLAB path and the configured Brainstorm install was unavailable.',
      'No method parameters changed after the unit gates or tag.']
    for i,s in enumerate(facts,1):p(f'{i}. {s}')
    p('## Freeze, units and execution')
    p('Full unit results, including all true/recovered pairs, raw fA score curves and BLP/PPC curves: '+link(OUT/'UNIT_RESULTS.md')+'. Freeze attestation: '+link(OUT/'freeze_attestation.json')+'. Protocol: '+link(OUT/'PROTOCOL_v2.md')+'. Execution bookkeeping: '+link(A/'HELDOUT_EXECUTION.md')+'.')
    p('Candidate 1 failed phase recovery; candidate 2 failed amplitude recovery. Their records remain preserved. Candidate 3 changes only Step 4 to the specified Gaussian analytic kernel; Step 2 BLP, the max-BLP event test and fixed-frequency secondary test remain unchanged. All candidate history is in the protocol. No further candidate was made.')
    p('H1 uses the original sparsity/distractor formulas with random true pairs and the requested durations/levels. H2 uses a physical-trough coupled rhythm, independent random fD/phase, the requested amplitude ratios, and no high-frequency distractor. H4 uses the canonical sinusoidal continuous envelope (12 s, depth .70) and the suite-wide mixed-noise formula at -3 dB. Full per-trial generator settings and random draws: '+link(OUT/'heldout_frequency_draws.csv')+'. The exact stream map and pre-data choices are in HELDOUT_EXECUTION.md.')
    p('All methods share each saved input. Phase/amplitude tolerances are inclusive 1/8 Hz; strict phase tolerance .5 Hz. Invalid outputs count as recovery failures. fP/fA recovery columns are marginal. Errors use finite estimates; CSVs include their denominators. H2 picks near fD means |estimated fP-fD|<=1 regardless of amplitude recovery. AUC uses finite scores, original score direction and half credit for ties; finite denominators appear in every row. Event p<.05 rates use all 25 trials, with finite-p counts shown.')
    p('Comparators independently maximize their own full grids (phase 3:.5:14, amplitude 80:4:160); A2-prime half-width=14 and A1-prime half-width=candidate fP. Phase half-width=1.5 Hz. Their inherited butter(4)/filtfilt, raw/Ozkurt/KLMI/GLM definitions are recorded in provenance. tPAC availability inspection: '+link(OUT/'headless_inspection.json')+'.')
    p('## C1-C4')
    p(table(['Criterion','Result','Numbers'],[[r['criterion'],r['result'],r['numbers']] for r in decisions]))
    p('Best A2-prime is chosen per level in the comparator\'s favor for each endpoint, as specified before data generation. Exact choices/counts: '+link(OUT/'best_A2_by_level.csv')+'. Paired McNemar counts, required AUCs and thresholds: '+link(OUT/'decision_details.json')+'. Criterion CSV: '+link(OUT/'decision_criteria.csv')+'.')
    p('## Recovery tables')
    p('Full per-trial results: '+link(OUT/'heldout_trials.csv')+'. Summary with finite counts and provenance: '+link(OUT/'heldout_recovery_summary.csv')+'.')
    def display(rr):return [[r['dataset'],float(r['level']),r['configuration'],r['method'],r['joint'],r['fA_recovery'],r['fP_recovery'],r['strict_joint'],r['n_valid'],f"{r['mean_fP_error']:.5g}/{r['median_fP_error']:.5g}",f"{r['mean_fA_error']:.5g}/{r['median_fA_error']:.5g}",r['picks_near_fD']] for r in rr]
    headers=['Dataset','Level','Config','Method','Joint /25','fA /25','fP /25','Strict /25','Valid /25','fP error mean/median Hz','fA error mean/median Hz','Near fD /25']
    for scenario in ['H1_sparsity','H1_distractor','H2','H4']:
        p('### '+scenario);p(table(headers,display([r for r in summary if r['scenario']==scenario])))
    for scenario in ['H1','H2']:p(f'![Joint recovery {scenario}]({(OUT/("joint_recovery_"+scenario+".png")).as_posix()})')
    p('## Null false recovery and AUC')
    p('Timing nulls retain the coupled burst amplitude/sigma and exact other signal/noise components; only burst timing changes. Secondary controls remove only the true-burst term. All 325 paired subtraction checks passed. '+link(OUT/'heldout_null_pair_verification.csv')+'. Specificity CSV: '+link(OUT/'heldout_null_specificity_auc.csv')+'.')
    p(table(['Scenario','Null','Level','Config','Method','Score','False joint /25','AUC','Finite coupled/null'],[[r['scenario'],r['dataset'],float(r['level']),r['configuration'],r['method'],r['score_field'],r['false_joint'],r['auc'],f"{r['n_coupled_finite']}/{r['n_null_finite']}"] for r in specific]))
    p('## Event p<0.05 rates')
    p('event_p is the primary full-grid max-BLP test; event_p_fixed is the secondary uncorrected fixed-frequency test. '+link(OUT/'heldout_event_rejection_rates.csv')+'.')
    p(table(['Scenario','Dataset','Level','Statistic','Rejected /25','Finite p /25','Rate'],[[r['scenario'],r['dataset'],float(r['level']),r['statistic'],r['n_reject'],r['n_finite_p'],r['rejection_rate']] for r in rates]))
    p('## Runtime and deviations')
    unit=load(OUT/'unit_attempt_01/unit_results.json')
    p(table(['Stage','Elapsed seconds','Status'],[['Unit gates',unit['elapsed_seconds'],unit['status']]]+[[k,v['elapsed_seconds'],v['status']] for k,v in runtimes.items()]))
    p('Workers ran concurrently with one computation thread each; summing their elapsed seconds is not wall time. MATLAB startup, implementation and report assembly are excluded from these stage timers. Input generation and all worker logs are preserved beside the results.')
    p('Tooling deviations: Python initially lacked matplotlib on its default path; the existing workspace pydeps copy was used (matplotlib '+plot_version+'). No package download or method change was needed. Pre-existing missing Brainstorm startup-path warnings were retained. UTF-8 text I/O is explicit. No held-out trial was removed or regenerated; invalid outputs are counted. No method change or parameter tuning occurred after tagging. Any additional tooling deviations are recorded in '+link(OUT/'tooling_deviations.json')+'.')
    p('## Full provenance')
    p('All trial/summary CSVs store commit, MATLAB version, full APC/comparator options and seed. Input MAT files store signals/components/streams/settings; worker checkpoints store curves and both surrogate-statistic vectors. Figures embed the full metadata. Input hash and protected-output checks: '+link(OUT/'final_verification.json')+'.')
    p('```json\n'+json.dumps(metadata,indent=2)+'\n```')
    report=OUT/'RESULTS_v2.md';report.write_text('\n'.join(lines),encoding='utf-8')
    runtime={'status':'COMPLETE','elapsed_seconds':time.monotonic()-started,'metadata':metadata,'rows':len(rows),'summary_rows':len(summary),'criteria':details}
    (OUT/'report_runtime.json').write_text(json.dumps(runtime,indent=2),encoding='utf-8')
    print(json.dumps({'status':'COMPLETE','rows':len(rows),'summary_rows':len(summary),'AUC_rows':len(specific),'criteria':{r['criterion']:r['result'] for r in decisions}}))
if __name__=='__main__':main()
