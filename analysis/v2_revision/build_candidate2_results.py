"""Report final-candidate gates without touching candidate-1 results."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,re,subprocess,time
A=Path(__file__).resolve().parent;REPO=A.parent.parent;ROOT=REPO.parent
BASE=ROOT/'revision_checks/v2';OUT=BASE/'candidate_02';ATTEMPT=OUT/'unit_attempt_01'
GIT=r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe'
def git(*args):return subprocess.check_output([GIT,'-C',str(REPO),*args],encoding='utf-8').strip()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()
def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def link(p,label=None):return f'[{label or p.name}](<{p.as_posix()}>)'
def table(head,rows):
    def esc(x):return (f'{x:.10g}' if isinstance(x,float) else str(x)).replace('|','\\|').replace('\n',' ')
    return '\n'.join(['| '+' | '.join(map(esc,head))+' |','| '+' | '.join(['---']*len(head))+' |']+['| '+' | '.join(map(esc,r))+' |' for r in rows])
def main():
    start=time.monotonic();result=load(ATTEMPT/'unit_results.json');meta=result['metadata'];gates=result['gates'];stop=result['failed_gate']
    rows=read(ATTEMPT/'unit_trials.csv');compat=load(ATTEMPT/'v1_compatibility.json');invariants=load(ATTEMPT/'implementation_checks.json')
    assert compat['passed'] and invariants['passed'];assert git('hash-object','src/bst_apc.m')==meta['apc_source_blob']
    protocol=(A/'PROTOCOL_v2.md').read_text(encoding='utf-8');original=git('show','7848af0:analysis/v2_revision/PROTOCOL_v2.md')
    criterion=lambda s:s[s.index('PART 5'):s.index('\nOUTPUT',s.index('PART 5'))]
    assert criterion(protocol)==criterion(original)
    assert (A/'PROTOCOL_v2.md').read_bytes()==(BASE/'PROTOCOL_v2.md').read_bytes()==(OUT/'PROTOCOL_v2.md').read_bytes()
    assert not list(OUT.glob('heldout*')) if stop else True
    curve_files=sorted(ATTEMPT.glob('unit_*_curves.csv'));assert len(curve_files)==len(rows)
    curves=[]
    for p in curve_files:
        rr=read(p);assert rr
        assert all(r['apc_source_blob']==meta['apc_source_blob'] for r in rr)
        curves.append({'file':str(p),'rows':len(rr),'sha256':sha(p)})
    for r in rows:
        assert r['apc_source_blob']==meta['apc_source_blob'];json.loads(r['apc_options_json'])
    old_manifest=load(BASE/'candidate_01/output_manifest.json');preserved=[]
    for name,digest in old_manifest['files'].items():
        p=Path(name);actual=p
        if p==BASE/'PROTOCOL_v2.md':actual=BASE/'candidate_01/PROTOCOL_v2.md'
        assert sha(actual)==digest,(p,actual)
        preserved.append({'original_path':str(p),'preserved_path':str(actual),'sha256':digest})
    tag=git('tag','-l','v2.0');assert not tag if stop else True
    lines=[]
    def p(s=''):lines.append(s+'\n')
    p('# APC v2 candidate 2 results')
    p('Final authorized candidate. Candidate 1 remains in commit `7848af05ada722971769da856e970d0737820169`; its saved results are unchanged. '+
      ('Candidate 2 stopped at unit gate '+stop+'. No v2.0 tag or held-out data were created.' if stop else 'All candidate-2 unit gates passed.'))
    p('## Factual summary (8 lines)')
    facts=[f'Candidate-2 unit gates: '+', '.join(f'{k}={v}' for k,v in gates.items())+'.',
        f'Completed unit trial rows and BLP/PPC curves: {len(rows)} each.',
        'All five v1 compatibility cases exactly matched the v1.0 reference.',
        'Burst detection, direct BLP, surrogate direct-sum equivalence, PPC, diagnostic isolation and RNG checks passed.',
        f'First failed gate: {stop or "none"}.',
        'The decision criteria C1-C4 remain text-identical to candidate 1.',
        'Held-out data generation and criterion evaluation: not run.' if stop else 'Held-out evaluation proceeds only after commit and v2.0 tagging.',
        f'v2.0 tag: {tag or "not created"}; no further candidates were made.']
    for i,s in enumerate(facts,1):p(f'{i}. {s}')
    p('## Candidate history and exact revision')
    p('Candidate 1 failed gate (a) with fP=10.631999875603938 Hz and fA=120 Hz. The user identified the flat-PPC filter-center issue from its saved curve. This cause and the revised authorization are recorded under Candidate history in '+link(OUT/'PROTOCOL_v2.md')+'. The identical tracked protocol is '+link(A/'PROTOCOL_v2.md')+'. The original protocol is preserved at '+link(BASE/'candidate_01/PROTOCOL_v2.md')+'.')
    p('Candidate 2 replaces phase selection with the specified debiased burst-locked power: two-second demeaned, symmetric-Hann windows, direct Fourier coefficients, 0.05-Hz candidate grid, raw-BLP parabolic interpolation and no polarity flips in Step 2. The phase filter, Steps 1/3/4, unit profiles/seeds and every C1-C4 threshold are unchanged. PPC from coefficient phases is diagnostic only. The event test uses the maximum BLP across the full grid and 200 full-grid surrogate maxima; the fixed-frequency BLP z/p is secondary. Jitters are independent conditional uniform draws inside the window-usable range. Direct coefficients at bracketing sample centers are batched and linearly interpolated, which is checked against independent direct extraction of continuous-center segments.')
    p('## Unit gates')
    p(table(['Gate','Criterion','Result'],[
        ['a','|fP-8|<=0.1 Hz and |fA-120|<=4 Hz',gates['a']],
        ['a2','fP in [5.3,6.7,9.4,10.8] Hz; each phase error<=0.1 Hz',gates['a2']],
        ['b','Added uncoupled 11-Hz sine at 3x; |fP-8|<=0.5 Hz',gates['b']],
        ['c','Poisson: corrected event p>0.05 in at least 8/10 seeds',gates['c']],
        ['d','Run first 25 existing level-0 distractor trials without tuning',gates['d']]]))
    p(table(['Test','Trial','True fP','fP','fA','|fP error|','C_APC','Ozkurt','PPC at fP','BLP at fP','Grid-max BLP','Max z','Max p','Fixed z','Fixed p','Bursts/usable','Flags','Status','Pass'],[
        [r['test'],r['trial_index'],float(r['true_fp_hz']),float(r['recovered_fp_hz']),float(r['recovered_fa_hz']),abs(float(r['recovered_fp_hz'])-float(r['true_fp_hz'])),
         *[float(r[k]) for k in ['C_APC','ozkurt_mvl','event_ppc','event_blp','event_statistic','event_z','event_p','event_z_fixed','event_p_fixed']],
         r['burst_count']+'/'+r['usable_burst_count'],r['diagnostic_flags'],r['status'],r['passed']] for r in rows]))
    if stop:
        if stop in ['a','a2','b']:
            r=[r for r in rows if r['test']==stop][-1]
            p(f'Stopping result: true fP={float(r["true_fp_hz"]):.17g} Hz; recovered fP={float(r["recovered_fp_hz"]):.17g} Hz; absolute phase error={abs(float(r["recovered_fp_hz"])-float(r["true_fp_hz"])):.17g} Hz; recovered fA={float(r["recovered_fa_hz"]):.17g} Hz; absolute amplitude error={abs(float(r["recovered_fa_hz"])-float(r["true_fa_hz"])):.17g} Hz. The predeclared gate was evaluated without changing any signal or parameter.')
        if stop=='c':p('Corrected p>0.05 on '+str(sum(float(r['event_p'])>.05 and r['status']=='0' for r in rows if r['test']=='c'))+'/10 seeds; at least eight were required.')
        p('No subsequent gates were run after this failure. The remaining tests, commit as candidate 2, v2.0 tagging and held-out suite were not performed. No third candidate or post-result method change was made.')
    p('Per-trial CSV: '+link(ATTEMPT/'unit_trials.csv')+'. Complete gate record: '+link(ATTEMPT/'unit_results.json')+'. Implementation checks: '+link(ATTEMPT/'implementation_checks.json')+'. Compatibility: '+link(ATTEMPT/'v1_compatibility.json')+'.')
    p(table(['BLP/PPC curve','Grid rows'],[[link(Path(r['file'])),r['rows']] for r in curves]))
    p('Each completed test has a saved MAT checkpoint containing signals/components, full options, source provenance, both surrogate-statistic vectors and intermediate arrays. '+', '.join(link(x) for x in sorted(ATTEMPT.glob('unit_*.mat')))+'.')
    p('The precision gate uses the unchanged generator at each requested true fP, initialized with the original seed 20260618. Units (a), (b), (c) and (d) retain the original committed profiles and seed schemes. All random generators and per-trial surrogate substreams are stored in the CSVs and MAT metadata.')
    p('## Freeze state and held-out criteria')
    p('The unit tests ran on the candidate-2 working sources before the conditional commit, as requested. The metadata git_commit is the candidate-1 base commit; it is not presented as the candidate-2 method commit. Exact tested method blob: `'+meta['apc_source_blob']+'`. The source snapshot is '+link(ATTEMPT/'source_snapshot/bst_apc.m')+'; the tested protocol and runner are saved beside it. The method-source hash was verified unchanged at test completion.')
    p(table(['Criterion','Status'],[[k,'NOT EVALUATED: unit gate '+stop+' failed' if stop else 'Pending frozen held-out evaluation'] for k in ['C1','C2','C3','C4']]))
    if stop:p('H1-H4 simulations, null AUCs, held-out p-value rejection rates, tPAC availability and H1/H2 figures were not evaluated. No data for these analyses were generated.')
    p('## Runtime, deviations and preservation')
    p(f'Unit-driver elapsed time: {result["elapsed_seconds"]:.6f} seconds, excluding MATLAB startup. One computation thread; MATLAB {meta["matlab_version"]}. Log: '+link(OUT/'unit_attempt_01_matlab.log')+'.')
    p('Implementation bug fixes after unit execution: '+('none.' if not result.get('implementation_bug_fixes') else json.dumps(result['implementation_bug_fixes'])) )
    p('Tooling deviations: '+('none during unit execution.' if not result.get('tooling_deviations') else json.dumps(result['tooling_deviations']))+' The previously documented protocol mirror remains necessary because the output folder is outside Git. Candidate-2 results use their own subfolder to preserve candidate-1 saved outputs. All Python text I/O uses UTF-8. Pre-existing missing Brainstorm startup paths may be reported in the MATLAB log.')
    p(f'Candidate-1 preserved-file checks: {len(preserved)} passed (its superseded protocol is checked against the archived original). Candidate 1 remains committed, v1.0 remains unchanged, and prior results were not overwritten. No further candidate was made.')
    if (OUT/'final_verification.json').exists():
        verification=load(OUT/'final_verification.json');assert verification['passed']
        p('Final source-section and preservation audit: '+link(OUT/'final_verification.json')+'. It confirms unchanged v1 calculations, Steps 1/3/4 and the phase-filter rule, an unchanged unit generator, an exact match to the tested source snapshot, and '+str(verification['prior_v1_files_verified'])+' unchanged prior v1 result/input files.')
    p('## Full unit provenance')
    p('```json\n'+json.dumps(meta,indent=2)+'\n```')
    report=OUT/'RESULTS_v2.md';report.write_text('\n'.join(lines),encoding='utf-8')
    for target in re.findall(r'\]\(<([^>]+)>\)',report.read_text(encoding='utf-8')):assert Path(target).exists(),target
    manifest={'candidate':2,'status':result['status'],'metadata':meta,'decision_criteria_unchanged':True,'preserved_candidate1_files':preserved,
        'files':{str(p):sha(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='output_manifest.json' and '__pycache__' not in p.parts}}
    (OUT/'output_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({'status':result['status'],'failed_gate':stop,'rows':len(rows),'curve_files':len(curves),'report':str(report),'build_seconds':time.monotonic()-start}))
if __name__=='__main__':main()
