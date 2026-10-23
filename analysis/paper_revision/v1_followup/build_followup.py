"""Verify and summarize follow-up results without changing trial estimates."""
from pathlib import Path
from collections import defaultdict, Counter
import csv, hashlib, json, math, statistics, subprocess, time

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
REPO=ROOT/'apc-brainstorm-publish'
GIT=r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe'
PROV=['git_commit','matlab_version','seed','apc_options_json','comparator_settings_json']
KEYS=['stage','benchmark','dataset','level','configuration','method','fp_grid_step_hz']
def load(name): return json.loads((OUT/name).read_text(encoding='utf-8'))
def read(name):
    with (OUT/name).open(encoding='utf-8',newline='') as f: return list(csv.DictReader(f))
def write(name,rows):
    assert rows
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def git(*a):return subprocess.check_output([GIT,'-C',str(REPO),*a],encoding='utf-8').strip()
def num(r,k):return float(r[k])
def finite(x):return math.isfinite(x)
def mean(x):return statistics.mean(x) if x else math.nan
def median(x):return statistics.median(x) if x else math.nan
def fmt(x):return f'{x:.6g}' if isinstance(x,float) else str(x)
def table(headers,rows):
    def esc(v):return fmt(v).replace('|','\\|').replace('\n',' ')
    return '\n'.join(['| '+' | '.join(map(esc,headers))+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(esc,row))+' |' for row in rows])
def link(name,label=None):return f'[{label or name}](<{(OUT/name).as_posix()}>)'

def summaries(rows):
    groups=defaultdict(list)
    for r in rows:groups[tuple(r[k] for k in KEYS)].append(r)
    result=[]
    for key,rr in groups.items():
        assert len(rr)==25,(key,len(rr))
        assert sorted(int(r['repeat_index']) for r in rr)==list(range(1,26))
        pe=[abs(num(r,'recovered_fp_hz')-num(r,'true_fp_hz')) for r in rr]
        ae=[abs(num(r,'recovered_fa_hz')-num(r,'true_fa_hz')) for r in rr]
        valid=[r['valid']=='1' for r in rr]
        fp=[v and p<=1 for v,p in zip(valid,pe)];fa=[v and a<=8 for v,a in zip(valid,ae)]
        item=dict(zip(KEYS,key))
        item.update(n_trials=25,n_valid=sum(valid),joint_recovery=sum(p and a for p,a in zip(fp,fa)),
            fA_recovery=sum(fa),fP_recovery=sum(fp),strict_joint_recovery=sum(v and p<=.5 and a<=8 for v,p,a in zip(valid,pe,ae)),
            mean_abs_fP_error_hz=mean([p for p in pe if finite(p)]),median_abs_fP_error_hz=median([p for p in pe if finite(p)]),
            mean_abs_fA_error_hz=mean([a for a in ae if finite(a)]),median_abs_fA_error_hz=median([a for a in ae if finite(a)]),
            n_finite_fP=sum(map(finite,pe)),n_finite_fA=sum(map(finite,ae)),
            boundary_fP_4=sum(abs(num(r,'recovered_fp_hz')-4)<=1e-9 for r in rr),
            boundary_fP_12=sum(abs(num(r,'recovered_fp_hz')-12)<=1e-9 for r in rr),
            picks_about_10=sum(abs(num(r,'recovered_fp_hz')-10)<=1 for r in rr),
            direct_scan=sum(r['route']=='direct_envelope_scan' for r in rr),tf_fallback=sum(r['route']=='tf_fallback' for r in rr),
            other_APC_route=sum(r['method']=='APC' and r['route'] not in ['direct_envelope_scan','tf_fallback'] for r in rr))
        item.update({k:rr[0][k] for k in PROV});result.append(item)
    return result

def aucs(rows):
    cg=defaultdict(list);ng=defaultdict(list)
    keys=['benchmark','level','configuration','method','fp_grid_step_hz']
    for r in rows:
        key=tuple(r[k] for k in keys)
        if r['dataset']=='coupled' and r['stage']!='random_fp':cg[key].append(r)
        elif r['dataset']!='coupled':ng[(r['dataset'],key)].append(r)
    result=[]
    for (dataset,key),rr in ng.items():
        coupled=cg[key];assert len(coupled)==len(rr)==25
        c=[num(r,'score') for r in coupled if finite(num(r,'score'))]
        n=[num(r,'score') for r in rr if finite(num(r,'score'))]
        a=sum((x>y)+.5*(x==y) for x in c for y in n)/(len(c)*len(n)) if c and n else math.nan
        false=sum(r['valid']=='1' and abs(num(r,'recovered_fp_hz')-num(r,'true_fp_hz'))<=1 and abs(num(r,'recovered_fa_hz')-120)<=8 for r in rr)
        item=dict(zip(keys,key));item.update(null_type=dataset,n_null=25,false_joint_recovery=false,auc_coupled_vs_null=a,
             n_coupled_finite_scores=len(c),n_null_finite_scores=len(n))
        item.update({k:rr[0][k] for k in PROV});result.append(item)
    return result

def distributions(rows):
    groups=defaultdict(list)
    for r in rows:
        if r['configuration']=='A2':groups[tuple(r[k] for k in KEYS)].append(r)
    result=[];compact=[]
    for key,rr in groups.items():
        step=float(key[-1]);counts=Counter(num(r,'recovered_fp_hz') for r in rr)
        vals=[4+i*step for i in range(round(8/step)+1)];assert sum(counts.values())==25
        assert all(v in vals for v in counts)
        for value in vals:
            item=dict(zip(KEYS,key));item.update(selected_fP_hz=value,count=counts[value],n_trials=25)
            item.update({k:rr[0][k] for k in PROV});result.append(item)
        compact.append([*key,', '.join(f'{v:g}:{counts[v]}' for v in vals if counts[v])])
    return result,compact

def display(rr):
    return [[r['configuration'],r['method'],r['fp_grid_step_hz'],float(r['level']),r['joint_recovery'],r['fA_recovery'],r['fP_recovery'],
        r['strict_joint_recovery'],r['n_valid'],f"{r['mean_abs_fP_error_hz']:.5g} / {r['median_abs_fP_error_hz']:.5g}",
        f"{r['mean_abs_fA_error_hz']:.5g} / {r['median_abs_fA_error_hz']:.5g}",f"{r['boundary_fP_4']} / {r['boundary_fP_12']}",
        r['picks_about_10'],f"{r['direct_scan']} / {r['tf_fallback']} / {r['other_APC_route']}" if r['method']=='APC' else 'n/a'] for r in rr]

def main():
    started=time.monotonic()
    runtime={s:load(s+'_runtime.json') for s in ['diagnosis','a2','slow','slow_diagnosis']}
    assert all(r['status']=='COMPLETE' for r in runtime.values())
    metadata=runtime['a2']['metadata'];commit=metadata['git_commit']
    assert git('rev-parse','HEAD')==git('rev-list','-n','1','v1.0')==commit
    assert not git('status','--porcelain')
    manifest=load('input_source_manifest.json')
    analysis_initial=load('analysis_manifest.json')
    for path,digest in analysis_initial['files'].items():
        if Path(path).suffix=='.m':assert sha(path)==digest,('Analysis method script changed during run',path)
    checks=[]
    for kind in ['source_files','input_files']:
        for path,digest in manifest[kind].items():
            assert sha(path)==digest,('Changed protected file',path)
            checks.append({'kind':kind,'path':path,'sha256':digest,'unchanged':True})
    a2=read('a2_trials.csv');slow=read('slow_trials.csv');diag=read('status4_diagnosis.csv')
    slow_diag=read('slow_status4_diagnosis.csv');assert len(slow_diag)==122
    input_qa=load('slow_input_verification.json');assert input_qa['passed'] and input_qa['n_coupled']==150 and input_qa['n_null']==75
    assert len(a2)==9600 and len(slow)==4050 and len(diag)==36
    for name,rr in [('a2',a2),('slow',slow)]:
        assert len({tuple(r[k] for k in KEYS)+ (r['repeat_index'],) for r in rr})==len(rr)
        for r in rr:
            assert r['git_commit']==commit and r['seed']=='20260618'
            assert r['matlab_version']==metadata['matlab_version']
            for k in PROV[3:]:json.loads(r[k])
            cfg=json.loads(r['generator_settings_json'])
            if r['configuration']=='A2':assert num(r,'effective_half_width_hz')==12
            if r['method']=='APC' and r['valid']=='1':assert num(r,'effective_half_width_hz')==num(r,'recovered_fp_hz')
            if name=='slow':
                assert cfg['true_fp_hz']==6 and cfg['phase_offset_deg']==180 and cfg['coupling_level']==.6
                assert cfg['high_frequency_distractor_present'] is False
                assert num(r,'matched_null_residual')<=1e-12
    assert Counter(r['stage'] for r in a2)=={'main':2800,'random_fp':1200,'null':5600}
    assert Counter(r['dataset'] for r in slow)=={'coupled':2700,'timing_null':1350}
    for r in diag:
        assert r['outside_padded_neighbors']=='0' and r['outside_configured_limits']=='0'
        assert r['refined_troughs_after']=='0' and r['refined_status']=='4'
    for r in slow_diag:
        assert r['outside_padded_neighbors']=='0' and r['outside_configured_limits']=='0'
        assert r['refined_troughs_after']=='0' and r['refined_status']=='4'
        json.loads(r['diagnostic_refined_options_json']);json.loads(r['diagnostic_unrefined_options_json'])
    expected_slow_status={(r['dataset'],r['level'],r['repeat_index'],r['configuration']) for r in slow if r['method']=='APC' and r['status_code']=='4'}
    assert expected_slow_status=={(r['dataset'],r['level'],r['repeat_index'],r['configuration']) for r in slow_diag}
    a2_summary=summaries(a2);slow_summary=summaries(slow)
    for stage in ['main','random_fp','null']:
        write(f'a2_{stage}_summary.csv',[r for r in a2_summary if r['stage']==stage])
    write('slow_summary.csv',slow_summary)
    a2_auc=aucs(a2);slow_auc=aucs(slow)
    assert len(a2_auc)==224 and len(slow_auc)==54
    write('a2_null_specificity_auc.csv',a2_auc);write('slow_null_specificity_auc.csv',slow_auc)
    dist,compact=distributions(a2+slow);write('a2_selected_fP_distribution.csv',dist)
    assert sum(r['count'] for r in dist)==11400 # 9600 saved-bank + 1800 slow A2 rows
    verify={'passed':True,'protected_files':checks,'row_counts':{'A2':len(a2),'slow':len(slow),'original_status4':len(diag),'slow_status4':len(slow_diag)},'metadata':metadata}
    (OUT/'verification.json').write_text(json.dumps(verify,indent=2),encoding='utf-8')
    final_analysis={'files':{str(p):sha(p) for p in sorted(OUT.iterdir()) if p.suffix in ['.m','.py'] or p.name=='PROTOCOL_followup.md'},'metadata':metadata}
    (OUT/'analysis_final_manifest.json').write_text(json.dumps(final_analysis,indent=2),encoding='utf-8')

    lines=[]
    def p(x=''):lines.append(x+'\n')
    p('# APC v1.0 follow-up analyses')
    p(f'Frozen tag `v1.0`, commit `{commit}`. Tagged source and all saved input banks remain byte-identical. New scripts and results are confined to `{OUT}`. Seed 20260618; MATLAB '+metadata['matlab_version']+'.')
    p('## Factual summary (9 lines)')
    facts=[f'A2: 9,600 scan results on 350 saved main, 150 saved random-fP and 700 saved null inputs, using both phase grids.',
        'The copied A1 comparator reproduced all eight frozen metric/grid results exactly on its validation input.',
        'Original status-4 diagnosis: 13 main distractor, 14 timing-null and 9 no-coupled-burst trials; 122 new-scenario failures were also traced.',
        f'All 36 original status-4 trials had zero complete trough epochs after edge rejection; {sum(int(r["refined_troughs_before"])>0 for r in diag)} had detected troughs before rejection.',
        'No diagnosed refined fP lay outside its padded Welch peak neighbors or the configured 1-30 Hz phase limits.',
        f'Turning refinement off returned status 0 in {sum(r["unrefined_status"]=="0" for r in diag)}/36 original diagnosed trials and {sum(r["unrefined_status"]=="0" for r in slow_diag)}/122 new-scenario diagnosed trials.',
        'The slow-rhythm scenario contains 150 coupled trials and 75 paired timing-null trials; all 18 method/grid combinations share each input.',
        f'Frozen default APC slow-scenario joint recovery totals {sum(r["joint_recovery"] for r in slow_summary if r["dataset"]=="coupled" and r["configuration"]=="v1.0")}/150.',
        'All protected-source, saved-input and paired-null subtraction checks passed; no method changes were applied.']
    for i,x in enumerate(facts,1):p(f'{i}. {x}')
    p('## Definitions, inputs and provenance')
    p('A2 amplitude half-width is 12 Hz for every candidate. A1 uses candidate fP. All scans retain the frozen phase half-width 1.5 Hz, amplitude grid 80:8:152, butter(4) bandpass/filtfilt, 18-bin KLMI, GLM R-squared, independent full-grid maxima and first column-major tie handling. Phase grids are 4:1:12 and 4:0.5:12. MVL-raw and conventional Ozkurt-normalized MVL are independently selected scans; Ozkurt = |sum(A exp(i phase))|/sqrt(N sum(A squared)).')
    p('Every count has denominator 25. Joint: absolute phase error <=1 Hz and amplitude error <=8 Hz. fA/fP are marginal recovery criteria; strict joint uses phase error <=0.5 Hz. Invalid estimates count as recovery failures; errors use finite estimates, whose counts appear in the summary CSVs. Boundary picks mean fP=4/12 within 1e-9. About-10 picks mean |fP-10|<=1 Hz. APC does not use the comparator phase grid. AUC uses all finite coupled/null score pairs, half weight for ties, without score-direction reversal; finite denominators are shown.')
    p('The saved MAT input banks were read directly; no main, random-fP or original null inputs were regenerated. Full paths and SHA-256 hashes: '+link('input_source_manifest.json')+'. The analysis plan: '+link('PROTOCOL_followup.md')+'. Trial CSVs and MAT files store the frozen commit, MATLAB version, full APC option inputs, complete comparator settings, generator settings and seed. Initial script hashes: '+link('analysis_manifest.json')+'; final scripts including the report and independent input check: '+link('analysis_final_manifest.json')+'. All initial MATLAB method/driver script hashes still match. Verification: '+link('verification.json')+'.')
    headers=['Config','Method','Phase grid Hz','Level','Joint /25','fA /25','fP /25','Strict joint /25','Valid /25','fP error mean/median Hz','fA error mean/median Hz','fP=4/12','About 10 /25','Direct/TF/other']
    p('## A2 on saved main and random-fP inputs')
    p('Raw rows: '+link('a2_trials.csv')+'. Summaries: '+', '.join(link('a2_'+s+'_summary.csv') for s in ['main','random_fp','null'])+'.')
    for stage in ['main','random_fp']:
        for bench in ['sparsity','distractor']:
            p('### '+stage+' / '+bench)
            p(table(headers,display([r for r in a2_summary if r['stage']==stage and r['benchmark']==bench])))
    p('## A2 on both saved null sets')
    for dataset in ['timing_null','no_coupled_burst']:
        for bench in ['sparsity','distractor']:
            p('### '+dataset+' / '+bench)
            p(table(headers,display([r for r in a2_summary if r['stage']=='null' and r['dataset']==dataset and r['benchmark']==bench])))
    auc_headers=['Benchmark','Level','Config','Method','Grid Hz','Null','False joint /25','AUC','Finite coupled/null']
    def auc_display(rr):return [[r['benchmark'],float(r['level']),r['configuration'],r['method'],r['fp_grid_step_hz'],r['null_type'],r['false_joint_recovery'],r['auc_coupled_vs_null'],f"{r['n_coupled_finite_scores']}/{r['n_null_finite_scores']}"] for r in rr]
    p('### A2 false recovery and coupled/null AUC')
    p('False recovery targets (8 Hz,120 Hz) on the original null sets. Complete table: '+link('a2_null_specificity_auc.csv')+'.')
    p(table(auc_headers,auc_display(a2_auc)))

    p('## Status-4 diagnosis')
    p('Complete per-trial values and neighboring bins: '+link('status4_diagnosis.csv')+'. Intermediate arrays and both option runs: '+link('status4_diagnostics.mat')+'. The diagnostic copy reproduced every exported frozen APC result in all 72 refined/unrefined checks.')
    source=REPO/'src/bst_apc.m'
    p(f'The diagnosed return is `{source}:212-214`: `if isempty(phaseLockedAverage) || isempty(phaseLockedTf)`, followed by `metrics.status_code = 4; return;`. The earlier condition at line 202, `isempty(troughLocs)`, did not return any of these trials. The phase-epoch helper rejects a trough when `idx(1) < 1 || idx(end) > numel(signal)`. Its half-window is `max(2, round(phaseEpochCycles*fs/fP))`, with phaseEpochCycles=3. Complete epochs therefore span approximately six phase cycles. The helper returns empty averages when every trough fails that edge condition.')
    p(table(['Dataset','Level','Trial','Refined fP','Unrefined fP','Refined phase band Hz','Unrefined phase band Hz','Refined troughs before/after','Unrefined troughs before/after','Half-window samples refined/unrefined','Unrefined status'],[
        [r['dataset'],float(r['level']),r['repeat_index'],float(r['refined_fp_hz']),float(r['unrefined_fp_hz']),
         f"{float(r['refined_phase_low_hz']):.6g}-{float(r['refined_phase_high_hz']):.6g}",f"{float(r['unrefined_phase_low_hz']):.6g}-{float(r['unrefined_phase_high_hz']):.6g}",
         r['refined_troughs_before']+'/'+r['refined_troughs_after'],r['unrefined_troughs_before']+'/'+r['unrefined_troughs_after'],
         r['refined_epoch_half_samples']+'/'+r['unrefined_epoch_half_samples'],r['unrefined_status']] for r in diag]))
    p(f'Bounds checks: 0/36 outside the padded peak neighboring bins, {sum(r["outside_unpadded_neighbors"]=="1" for r in diag)}/36 outside the unpadded peak neighboring bins, and 0/36 outside configured [minPhaseHz,maxPhaseHz]=[1,30]. The padded and unpadded Welch spectra use different frequency grids; their peaks are recorded separately. Parabolic interpolation was actually used in {sum(r["refined_interpolated"]=="1" for r in diag)}/36 cases. All phase bands were valid and all 36 had detected troughs; edge rejection removed every trough.')
    p('All 36 refined estimates equal the lowest valid padded Welch bin, approximately 1.007080078125 Hz. Its left neighbor, approximately 0.9765625 Hz, is below minPhaseHz=1. The interpolation guard requires both neighbors to be valid, so it retains the bin frequency in these trials. The refined/unrefined difference therefore arises from the padded spectrum peak search, without a parabolic offset. This half-window is about 2.978 seconds on each side within a six-second record.')
    p('Classification: **(b) legitimate failure under the frozen complete-epoch requirement** for all 36. The recorded frequency, trough counts and return path do not identify a refinement-bound or trough-detection bug. Exported fP is NaN on status 4 because the method assigns it only after completing the later stages; the CSV reports the intermediate fP used at Step 3.')
    rescued=sum(r['unrefined_status']=='0' for r in diag)
    p(f'Minimal proposed future change, not applied: only when zero complete phase epochs remain, retry Step 2/3 using the existing fPRefine=false setting, then proceed if a complete epoch exists. This guard would be invoked for these 36 diagnosed trials; the existing unrefined runs returned status 0 for {rescued}/36, and {36-rescued}/36 would retain a failure. The frozen results remain unchanged. These counts concern this diagnosed set only; no count is claimed for unexamined inputs or a redesigned estimator.')

    p('### Status 4 in the new slow-rhythm scenario')
    p('To include every status-4 case in the new null set, the same diagnostic was also applied to all new-scenario failures, including coupled trials: '+link('slow_status4_diagnosis.csv')+' and '+link('slow_status4_diagnostics.mat')+'. This adds 48 timing-null trials, all with flipTroughs=false, plus 72 coupled trials with flipTroughs=false and two coupled default-APC trials. Default APC had no status-4 timing-null trials. All 244 refined/unrefined diagnostic results exactly matched the frozen method.')
    p(table(['Dataset','Config','Ratio','Trial','Refined fP','Unrefined fP','Refined phase band Hz','Unrefined phase band Hz','Refined troughs before/after','Unrefined troughs before/after','Unrefined status'],[
        [r['dataset'],r['configuration'],float(r['level']),r['repeat_index'],float(r['refined_fp_hz']),float(r['unrefined_fp_hz']),
         f"{float(r['refined_phase_low_hz']):.6g}-{float(r['refined_phase_high_hz']):.6g}",f"{float(r['unrefined_phase_low_hz']):.6g}-{float(r['unrefined_phase_high_hz']):.6g}",
         r['refined_troughs_before']+'/'+r['refined_troughs_after'],r['unrefined_troughs_before']+'/'+r['unrefined_troughs_after'],r['unrefined_status']] for r in slow_diag]))
    p(f'For the additional 122 cases: 0 escaped their padded neighboring bins or configured phase limits; {sum(r["outside_unpadded_neighbors"]=="1" for r in slow_diag)} lay outside the unpadded peak neighbors. Every case had zero edge-valid trough epochs and returned status 4 at the same empty-phase-locked-average condition. Classification remains (b), legitimate failure under the frozen complete-epoch requirement. The proposed guarded unrefined retry would trigger for all 122; {sum(r["unrefined_status"]=="0" for r in slow_diag)} existing unrefined runs completed with status 0. No retry was applied to the reported recovery results.')

    p('## Slow-rhythm distractor')
    p('The scenario uses the frozen distractor generator formulas with true fP=6 Hz, fA=120 Hz, coupling .60, original Gaussian width 28 ms and 10-ms burst-time jitter, sampling 500 Hz, duration 6 seconds and mixed pink/white noise at -3 dB. phase_offset_deg=180 places nominal burst centers at the physical trough of the 6-Hz sine. The full 96-Hz component, including baseline, is omitted. The added 10-Hz sinusoid has amplitude ratio times the 6-Hz amplitude and a trial-wise uniform phase from a separate seed-20260618 stream; it is not event-locked. Original generator draw order, including unused legacy null draws, is retained. These choices were recorded before new outcomes in the protocol.')
    p('Ratios in order: 0,0.5,1,1.5,2,3; 25 repeats each. All 18 APC/comparator/grid combinations share each saved input. APC options are unchanged except flipTroughs=false for that requested configuration. Timing nulls at ratios 0,1,3 replace only true-burst timing, using Poisson rate 6 Hz and the original extended event support, a separate seed-20260618 stream, unchanged amplitude/sigma and paired noise. Overlaps are allowed, with no minimum gap. Every paired subtraction residual is <=1e-12. Input cases, components and metadata are saved in six `slow_inputs_level_*.mat` files.')
    p('New input hashes and complete scenario provenance: '+link('generated_inputs_manifest.json')+'; full slow-run metadata: '+link('slow_runtime.json')+'.')
    p('An independent readback reconstructed all 150 coupled signals from the specified 6-Hz, base 120-Hz, Gaussian burst, pure 10-Hz and noise components; checked nominal burst centers at physical troughs, exact saved burst envelopes, -3 dB noise power and all 75 null subtractions. All checks passed. '+link('slow_input_verification.csv')+' and '+link('slow_input_verification.json')+'.')
    p('Raw rows: '+link('slow_trials.csv')+'. Full summaries: '+link('slow_summary.csv')+'.')
    for dataset in ['coupled','timing_null']:
        p('### '+dataset);p(table(headers,display([r for r in slow_summary if r['dataset']==dataset])))
    p('### Slow coupled/null AUC')
    p('False joint recovery targets (6 Hz,120 Hz). '+link('slow_null_specificity_auc.csv')+'.')
    p(table(auc_headers,auc_display(slow_auc)))

    p('## Distribution of selected A2 phase frequencies')
    p('Each cell below gives `selected Hz:count`; omitted grid values have zero counts. '+link('a2_selected_fP_distribution.csv')+' includes every grid value, including zeros, with provenance. Each group sums to 25. The slow A2 distributions are included.')
    p(table(['Stage','Benchmark','Dataset','Level','Config','Method','Grid Hz','Selected fP Hz:count'],compact))
    p('## Runtime and deviations')
    p(table(['Stage','MATLAB elapsed seconds','Status'],[[s,r['elapsed_seconds'],r['status']] for s,r in runtime.items()]))
    p(f'Independent saved-input verification: {input_qa["elapsed_seconds"]:.3f} seconds, passed.')
    p(f'MATLAB analysis elapsed total: {sum(r["elapsed_seconds"] for r in runtime.values()):.3f} seconds, plus the input-verification time above. One computation thread per process; A2 and slow analyses overlapped in wall time. Startup, implementation and report assembly are excluded from these stage timers. Log paths: '+', '.join(link(n) for n in ['diagnosis_matlab.log','diagnosis_retry_matlab.log','a2_matlab.log','slow_matlab.log','slow_diagnosis_matlab.log','input_verification_matlab.log'])+'.')
    p('Tooling deviation: the initial diagnostic launch stopped at the pre-execution source-path assertion because the workspace current directory contained an older bst_apc.m, which takes precedence over added MATLAB paths. The follow-up driver now changes to its own output directory and normalizes Windows path separators before checking the frozen source path. No APC method ran in the failed launch. The failed log is preserved. MATLAB startup also reported pre-existing missing Brainstorm paths. Text I/O in the Python scripts uses explicit UTF-8. No method change, replacement of saved inputs, trial exclusion or post-result parameter adjustment was made.')
    p('The slow scenario choices (physical-trough phase convention, independent random sinusoid phase, zero 96-Hz baseline, inherited noise scaling, both requested comparator grids) are explicit implementation specifications for the new scenario, rather than changes to APC. No minimum burst gap was required.')
    p('## Full metadata')
    p('```json\n'+json.dumps(metadata,indent=2)+'\n```')
    (OUT/'RESULTS_followup.md').write_text('\n'.join(lines),encoding='utf-8')
    result={'status':'COMPLETE','build_seconds':time.monotonic()-started,'metadata':metadata,'row_counts':verify['row_counts']}
    (OUT/'report_runtime.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    generated={'files':{str(p):sha(p) for p in sorted(OUT.glob('slow_inputs_level_*.mat'))},'metadata':runtime['slow']['metadata']}
    (OUT/'generated_inputs_manifest.json').write_text(json.dumps(generated,indent=2),encoding='utf-8')
    outputs={'files':{str(p):sha(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='output_manifest.json'},'metadata':metadata}
    (OUT/'output_manifest.json').write_text(json.dumps(outputs,indent=2),encoding='utf-8')
    print(json.dumps({'status':'COMPLETE','rows':verify['row_counts'],'summary_rows':len(a2_summary)+len(slow_summary),'auc_rows':len(a2_auc)+len(slow_auc)}))

if __name__=='__main__':main()
