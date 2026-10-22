"""Report final candidate-3 gates, preserving every earlier candidate result."""
from pathlib import Path
import json,re,time
from build_candidate2_results import git,load,read,sha,table,link
A=Path(__file__).resolve().parent;REPO=A.parent.parent;ROOT=REPO.parent
BASE=ROOT/'revision_checks/v2';OUT=BASE/'candidate_03';ATTEMPT=OUT/'unit_attempt_01'

def between(s,a,b):return s[s.index(a):s.index(b,s.index(a))].strip()
def main():
    start=time.monotonic();r=load(ATTEMPT/'unit_results.json');meta=r['metadata'];gates=r['gates'];stop=r['failed_gate'];rows=read(ATTEMPT/'unit_trials.csv')
    assert r['status'] in ['STOP_UNIT_GATE','UNIT_GATES_PASSED']
    assert git('hash-object','src/bst_apc.m')==meta['apc_source_blob']
    assert load(ATTEMPT/'implementation_checks.json')['passed'] and load(ATTEMPT/'v1_compatibility.json')['passed']
    assert (A/'PROTOCOL_v2.md').read_bytes()==(OUT/'PROTOCOL_v2.md').read_bytes()==(BASE/'PROTOCOL_v2.md').read_bytes()
    old=(BASE/'candidate_02/unit_attempt_01/source_snapshot/bst_apc.m').read_text(encoding='utf-8');new=(REPO/'src/bst_apc.m').read_text(encoding='utf-8')
    checks={
      'v1_calculations_unchanged':between(old,'    requestedVersion=','function [sApc,runInfo]=compute_matrix_apc_v2')==between(new,'    requestedVersion=','function [sApc,runInfo]=compute_matrix_apc_v2'),
      'step1_unchanged':between(old,'% Step 1 is exactly','% Candidate 2 Step 2:')==between(new,'% Step 1 is exactly','% Candidate 2 Step 2:'),
      'step2_unchanged':between(old,'% Candidate 2 Step 2:','% Step 3 affects')==between(new,'% Candidate 2 Step 2:','% Step 3 affects'),
      'step3_unchanged':between(old,'% Step 3 affects','% Step 4:')==between(new,'% Step 3 affects','% Candidate 3 Step 4:'),
      'event_test_unchanged':between(old,'% Candidate 2 event test:','function coefficients=v2_direct_coefficients')==between(new,'% Candidate 2 event test:','function coefficients=v2_direct_coefficients'),
      'tested_source_unchanged':sha(REPO/'src/bst_apc.m')==sha(ATTEMPT/'source_snapshot/bst_apc.m')}
    assert all(checks.values()),checks
    criteria=lambda s:between(s,'PART 5','\nOUTPUT')
    assert criteria((A/'PROTOCOL_v2.md').read_text(encoding='utf-8'))==criteria(git('show','7848af0:analysis/v2_revision/PROTOCOL_v2.md'))
    old_checks=[]
    for name,digest in load(BASE/'candidate_02/output_manifest.json')['files'].items():
        assert sha(Path(name))==digest,name;old_checks.append(name)
    phase_curves=sorted(ATTEMPT.glob('unit_*_curves.csv'));fa_curves=sorted(ATTEMPT.glob('unit_*_fa_scores.csv'))
    assert len(phase_curves)==len(fa_curves)==len(rows)
    tag=git('tag','-l','v2.0');assert not tag if stop else True
    lines=[]
    def p(s=''):lines.append(s+'\n')
    p('# APC v2 candidate 3 unit results')
    p('Final candidate authorized by the user. '+('Stopped at gate '+stop+'; no candidate-3 commit, v2.0 tag or held-out data were created.' if stop else 'All ordered unit gates passed. Commit/tag and held-out execution remain conditional on the source attestation.'))
    p('## Factual summary (8 lines)')
    facts=[', '.join(k+'='+v for k,v in gates.items())+'.',
      f'Completed unit trial rows: {len(rows)}; each has BLP/PPC and raw fA-score curves.',
      'The five v1 compatibility cases exactly matched the v1.0 reference.',
      'Step-2 and event outputs exactly matched candidate 2 on the unchanged unit-(a) signal.',
      'Direct BLP/surrogate, PPC, Gaussian FFT formula, diagnostic-isolation and RNG checks passed.',
      'The C1-C4 text is unchanged from the original committed protocol.',
      'Held-out data generation: not run.' if stop else 'All performance gates passed before any held-out data generation.',
      'No further candidate was made.']
    for i,s in enumerate(facts,1):p(f'{i}. {s}')
    p('## Candidate history and fixed method')
    p('Candidate 2 failed gate (a) only on fA=115 Hz (error 5 Hz); its fP=7.9996901239320914 Hz passed. The user diagnosed a bimodal Step-4 score from Butterworth band edges. This history and the final authorization are recorded in '+link(OUT/'PROTOCOL_v2.md')+'. The prior report is preserved at '+link(BASE/'candidate_02/RESULTS_v2.md')+'.')
    p('Only Step 4 changes: one-second mirror padding excluding repeated endpoints; FFT; positive-frequency gain 2*exp(-(f-fc)^2/(2*sigma^2)), zero at nonpositive frequencies; sigma=1.5*fP; inverse FFT/crop; raw MVL on the unchanged fP phase. No score smoothing or Gaussian-tail clipping. Select the 1-Hz grid maximum, refine an interior concave maximum by a three-point parabola, and recompute the envelope at refined fA for both raw C_APC and Ozkurt MVL. BLP, both event-test statistics, Steps 1/3 and all inherited profiles/seeds remain unchanged. Gaussian sigma is recorded explicitly; obsolete finite-band widths/edges are NaN.')
    p('## Ordered unit gates')
    p(table(['Gate','Criterion','Result'],[
      ['a','|fP-8|<=0.1 Hz and |fA-120|<=4 Hz',gates['a']],
      ['a2','Pairs (5.3,95),(6.7,108),(9.4,131),(10.8,142); phase error<=0.1 and amplitude error<=4',gates['a2']],
      ['b','Same 8/120 signal + 11-Hz sinusoid at 3x; phase error<=0.5',gates['b']],
      ['c','Poisson: corrected event p>0.05 on at least 8/10 seeds',gates['c']],
      ['d','Run first 25 existing level-0 distractor inputs; report without tuning',gates['d']]]))
    p(table(['Test','Trial','True fP','True fA','Recovered fP','Recovered fA','fP error','fA error','C_APC','Ozkurt','Max-event z','Max-event p','Fixed-event z','Fixed-event p','Bursts/usable','Flags','Status','Pass'],[
      [x['test'],x['trial_index'],float(x['true_fp_hz']),float(x['true_fa_hz']),float(x['recovered_fp_hz']),float(x['recovered_fa_hz']),
       abs(float(x['recovered_fp_hz'])-float(x['true_fp_hz'])),abs(float(x['recovered_fa_hz'])-float(x['true_fa_hz'])),
       *[float(x[k]) for k in ['C_APC','ozkurt_mvl','event_z','event_p','event_z_fixed','event_p_fixed']],x['burst_count']+'/'+x['usable_burst_count'],x['diagnostic_flags'],x['status'],x['passed']] for x in rows]))
    if stop:
        if stop=='c':
            n=sum(x['status']=='0' and float(x['event_p'])>.05 for x in rows if x['test']=='c');p(f'Gate c: corrected p>0.05 on {n}/10 seeds; at least eight required.')
        else:
            x=[x for x in rows if x['test']==stop][-1]
            p(f'Stopping trial: true pair=({float(x["true_fp_hz"]):.17g},{float(x["true_fa_hz"]):.17g}) Hz; recovered=({float(x["recovered_fp_hz"]):.17g},{float(x["recovered_fa_hz"]):.17g}) Hz. No subsequent gates were run.')
        p('Stopped as instructed. No post-result parameter or method changes, conditional commit/tag, held-out data or further candidate were made.')
    p('Per-trial data: '+link(ATTEMPT/'unit_trials.csv')+'. Gate record: '+link(ATTEMPT/'unit_results.json')+'. Checks: '+link(ATTEMPT/'implementation_checks.json')+'.')
    p(table(['BLP/PPC curve','Raw Gaussian fA-score curve'],[[link(a),link(b)] for a,b in zip(phase_curves,fa_curves)]))
    p('MAT checkpoints, including inputs, intermediate arrays, both surrogate-statistic vectors and full provenance: '+', '.join(link(x) for x in sorted(ATTEMPT.glob('unit_*.mat')))+'.')
    p('## Freeze state and held-out decisions')
    p('These gates were run on working sources before the conditional commit. Recorded git_commit is the candidate-1 base commit `'+meta['git_commit']+'`; exact tested method blob is `'+meta['apc_source_blob']+'`. Source snapshot: '+link(ATTEMPT/'source_snapshot/bst_apc.m')+'. This source remained unchanged during the gates. Candidate-1/2 snapshots remain available.')
    p(table(['Criterion','Status'],[[k,'NOT EVALUATED: failed unit gate '+stop if stop else 'Pending frozen held-out execution'] for k in ['C1','C2','C3','C4']]))
    p('## Runtime, deviations and preservation')
    p(f'Unit-driver runtime={r["elapsed_seconds"]:.6f} seconds, excluding MATLAB startup. One computation thread; MATLAB {meta["matlab_version"]}. '+link(OUT/'unit_attempt_01_matlab.log')+'.')
    p('Implementation bug fixes after unit execution: '+('none.' if not r.get('implementation_bug_fixes') else json.dumps(r['implementation_bug_fixes'])) )
    p('Tooling deviations during unit execution: '+('none.' if not r.get('tooling_deviations') else json.dumps(r['tooling_deviations']))+' The existing protocol mirror and separate candidate output folder preserve earlier records. Pre-existing missing Brainstorm startup paths may appear in the log. All Python text I/O explicitly uses UTF-8.')
    p(f'Candidate-2 saved-file hashes verified unchanged: {len(old_checks)}. Source checks confirm unchanged v1 calculations, Steps 1/2/3 and the entire candidate-2 event-test block. No further candidate was made.')
    p('## Full unit provenance')
    p('```json\n'+json.dumps(meta,indent=2)+'\n```')
    report=OUT/'UNIT_RESULTS.md';report.write_text('\n'.join(lines),encoding='utf-8')
    if stop:(OUT/'RESULTS_v2.md').write_text(report.read_text(encoding='utf-8'),encoding='utf-8')
    for target in re.findall(r'\]\(<([^>]+)>\)',report.read_text(encoding='utf-8')):assert Path(target).exists(),target
    manifest={'candidate':3,'status':r['status'],'code_checks':checks,'candidate2_files_preserved':old_checks,'metadata':meta,
      'files':{str(p):sha(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='output_manifest.json' and '__pycache__' not in p.parts}}
    (OUT/'output_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({'status':r['status'],'failed_gate':stop,'rows':len(rows),'report':str(report),'build_seconds':time.monotonic()-start}))
if __name__=='__main__':main()
