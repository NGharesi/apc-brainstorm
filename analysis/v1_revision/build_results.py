"""Summarize frozen MATLAB runs without altering method or trial results."""
from pathlib import Path
from collections import defaultdict
import csv,json,math,statistics,subprocess,hashlib,struct,zlib,sys
REPO=Path(__file__).resolve().parents[2];ROOT=REPO.parent
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'revision_checks/v1_rerun'
GIT=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def git(*args):return subprocess.check_output([str(GIT),'-C',str(REPO),*args],text=True,encoding="utf-8").strip()
def load(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def read(name):
    with (OUT/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def num(r,key):return float(r[key])
def finite(v):return math.isfinite(v)
def avg(v):return statistics.mean(v) if v else math.nan
def med(v):return statistics.median(v) if v else math.nan
def fmt(v):return f'{v:.4g}' if isinstance(v,float) else str(v)
def table(headers,rows):
    esc=lambda v:fmt(v).replace('|','\\|')
    return '\n'.join(['| '+' | '.join(map(esc,headers))+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(esc,r))+' |' for r in rows])
def link(path,label=None):return f'[{label or path.name}](<{path.as_posix()}>)'
runtime={stage:load(('committed_checks/' if stage in ['sanity','smoke'] else '')+stage+'_runtime.json') for stage in ['sanity','smoke','main','random_fp','null','figures']}
assert all(r['status']=='COMPLETE' for r in runtime.values()),'A stage failed; stop'
metadata=runtime['main']['metadata'];commit=metadata['git_commit']
assert git('rev-parse','HEAD')==git('rev-list','-n','1','v1.0')==commit
assert not git('status','--porcelain'),'Frozen repository changed'
sanity=load('committed_checks/sanity_results.json');assert sanity['passed']
smoke=load('committed_checks/smoke_results.json');assert smoke['passed']
assert sanity['metadata']['git_commit']==smoke['metadata']['git_commit']==commit
assert not sanity['metadata']['worktree_dirty'] and not smoke['metadata']['worktree_dirty']
assert sanity['metadata']['apc_source_git_blob']==git('rev-parse','v1.0:src/bst_apc.m')
provenance_columns=['git_commit','matlab_version','seed','apc_options_json','comparator_settings_json']
raw={name:read(name+'_trials.csv') for name in ['main','random_fp','null']}
assert len(raw['main'])==4200 and len(raw['random_fp'])==2700 and len(raw['null'])==3500
for stage,rows in raw.items():
    for r in rows:
        assert r['git_commit']==commit and int(r['seed'])==20260618
        assert json.loads(r['apc_options_json'])==metadata['apc_configurations']
        assert json.loads(r['comparator_settings_json'])==metadata['comparator_settings']
        json.loads(r['generator_settings_json'])
        if r['method']=='APC' and r['configuration'] in ['v1.0','v1.0_no_fP_refine'] and int(r['valid'])==1:
            assert num(r,'effective_half_width_hz')==num(r,'recovered_fp_hz')
            assert num(r,'candidate_half_width_hz')==num(r,'recovered_fp_hz')
    assert len({(r['benchmark'],r['dataset'],r['level'],r['repeat_index'],r['configuration'],r['method'],r['fp_grid_step_hz']) for r in rows})==len(rows)
def summarize(rows):
    groups=defaultdict(list)
    keys=['benchmark','dataset','level','configuration','method','fp_grid_step_hz']
    for r in rows:groups[tuple(r[k] for k in keys)].append(r)
    results=[]
    for key,rr in groups.items():
        assert len(rr)==25,(key,len(rr))
        pe=[abs(num(r,'recovered_fp_hz')-num(r,'true_fp_hz')) for r in rr]
        ae=[abs(num(r,'recovered_fa_hz')-num(r,'true_fa_hz')) for r in rr]
        valid=[int(r['valid'])==1 for r in rr]
        fp=[v and p<=1 for v,p in zip(valid,pe)];fa=[v and a<=8 for v,a in zip(valid,ae)]
        d=dict(zip(keys,key));d.update(n_trials=25,n_valid=sum(valid),joint_recovery=sum(p and a for p,a in zip(fp,fa)),
            fA_recovery=sum(fa),fP_recovery=sum(fp),joint_recovery_fp_05=sum(v and p<=.5 and a<=8 for v,p,a in zip(valid,pe,ae)),
            mean_abs_fP_error_hz=avg([p for p in pe if finite(p)]),median_abs_fP_error_hz=med([p for p in pe if finite(p)]),
            mean_abs_fA_error_hz=avg([a for a in ae if finite(a)]),median_abs_fA_error_hz=med([a for a in ae if finite(a)]),
            n_finite_fP=sum(map(finite,pe)),n_finite_fA=sum(map(finite,ae)),
            boundary_fP_4=sum(abs(num(r,'recovered_fp_hz')-4)<=1e-9 for r in rr),
            boundary_fP_12=sum(abs(num(r,'recovered_fp_hz')-12)<=1e-9 for r in rr),
            direct_scan=sum(r['route']=='direct_envelope_scan' for r in rr),tf_fallback=sum(r['route']=='tf_fallback' for r in rr),
            other_APC_route=sum(r['method']=='APC' and r['route'] not in ['direct_envelope_scan','tf_fallback'] for r in rr))
        d.update({k:rr[0][k] for k in provenance_columns});results.append(d)
    return results
summary={k:summarize(v) for k,v in raw.items()}
write('main_summary.csv',summary['main']);write('random_fp_summary.csv',summary['random_fp']);write('null_recovery_summary.csv',summary['null'])
def auc(c,n):
    c=[x for x in c if finite(x)];n=[x for x in n if finite(x)]
    return ((sum((a>b)+.5*(a==b) for a in c for b in n)/(len(c)*len(n))) if c and n else math.nan,len(c),len(n))
nullgroups=defaultdict(list);coupledgroups=defaultdict(list)
for r in raw['main']:
    if (r['method']=='APC' and r['configuration']=='v1.0') or r['configuration']=='A1':
        coupledgroups[(r['benchmark'],r['level'],r['configuration'],r['method'])].append(r)
for r in raw['null']:nullgroups[(r['benchmark'],r['dataset'],r['level'],r['configuration'],r['method'])].append(r)
nullout=[]
for (bench,dataset,level,config,method),rr in nullgroups.items():
    coupled=coupledgroups[(bench,level,config,method)];assert len(coupled)==25
    score,nc,nn=auc([num(r,'score') for r in coupled],[num(r,'score') for r in rr])
    false=sum(int(r['valid'])==1 and abs(num(r,'recovered_fp_hz')-8)<=1 and abs(num(r,'recovered_fa_hz')-120)<=8 for r in rr)
    item=dict(benchmark=bench,null_type=dataset,level=level,configuration=config,method=method,n_null=25,
        false_joint_recovery=false,auc_coupled_vs_null=score,n_coupled_finite_scores=nc,n_null_finite_scores=nn)
    item.update({k:rr[0][k] for k in provenance_columns});nullout.append(item)
write('null_specificity_auc.csv',nullout)
draws={}
for r in raw['random_fp']:
    key=(r['benchmark'],r['level'],r['repeat_index']);fp=num(r,'true_fp_hz');assert 5<=fp<=11
    if key in draws:assert draws[key]['true_fp_hz']==fp
    else:
        item=dict(benchmark=key[0],level=key[1],repeat_index=key[2],true_fp_hz=fp)
        item.update({k:r[k] for k in provenance_columns});draws[key]=item
assert len(draws)==150;write('random_fp_draws.csv',list(draws.values()))
verification=load('null_pair_verification.json');assert len(verification['trials'])==350
assert all(r['shared_components_exact'] and r['timing_null_residual']<=1e-12 and r['no_coupled_burst_residual']<=1e-12 for r in verification['trials'])
protected=load('protected_saved_results.json');checks=[]
for path,digest in protected.items():
    new=hashlib.sha256(Path(path).read_bytes()).hexdigest();assert digest==new
    checks.append(dict(path=path,sha256_before=digest,sha256_after=new,unchanged=True))
(OUT/'original_results_verification.json').write_text(json.dumps(dict(checks=checks,metadata=metadata),indent=2),encoding="utf-8")
def embed_png(file,meta):
    b=file.read_bytes();assert b[:8]==b'\x89PNG\r\n\x1a\n';chunks=[];pos=8
    while pos<len(b):
        n=struct.unpack('>I',b[pos:pos+4])[0];tag=b[pos+4:pos+8];data=b[pos+8:pos+8+n]
        if not(tag==b'tEXt' and data.startswith(b'APC_provenance\0')):
            if tag==b'IEND':
                text=b'APC_provenance\0'+json.dumps(meta,separators=(',',':')).encode('ascii');kind=b'tEXt'
                chunks.append(struct.pack('>I',len(text))+kind+text+struct.pack('>I',zlib.crc32(kind+text)&0xffffffff))
            chunks.append(b[pos:pos+12+n])
        pos+=12+n
    file.write_bytes(b[:8]+b''.join(chunks))
for bench in ['sparsity','distractor']:embed_png(OUT/f'joint_recovery_{bench}.png',metadata)
def display(rr):
    return [[r['configuration'],r['method'],r['fp_grid_step_hz'],fmt(float(r['level'])),r['joint_recovery'],r['fA_recovery'],r['fP_recovery'],
        r['joint_recovery_fp_05'],r['n_valid'],f"{r['mean_abs_fP_error_hz']:.4g} / {r['median_abs_fP_error_hz']:.4g}",
        f"{r['mean_abs_fA_error_hz']:.4g} / {r['median_abs_fA_error_hz']:.4g}",f"{r['boundary_fP_4']} / {r['boundary_fP_12']}",
        f"{r['direct_scan']} / {r['tf_fallback']} / {r['other_APC_route']}" if r['method']=='APC' else '—'] for r in rr]
headers=['Configuration','Method','fP grid Hz','Level','Joint /25','fA /25','fP /25','Joint .5Hz /25','Valid /25','fP error mean / median Hz','fA error mean / median Hz','fP=4 /12','Direct /TF /other']
lines=[]
def p(s=''):lines.append(s+'\n')
p('# APC v1.0 simulation rerun')
p(f'Branch `v1.0-revision`; commit `{commit}`; annotated tag `v1.0` → the same commit. Method source was committed/tagged before the main, random-fP and null runs. No method changes were made afterward.')
p('## Factual summary (8 lines)')
primary=[r for r in summary['main'] if r['configuration']=='v1.0' and r['method']=='APC']
randomprimary=[r for r in summary['random_fp'] if r['configuration']=='v1.0' and r['method']=='APC']
facts=[f'Frozen commit: {commit}; tag: v1.0.',
 'The oct2026 sanity check exactly matched all 175 saved distractor fA, fP and coupling values.',
 'The June compatibility sanity check matched all 25 endpoint fA, fP and coupling values and returned 12/25 joint recovery.',
 f'Main rerun: 350 paired coupled trials, 4 APC configurations, 8 comparator configurations/metrics; {len(raw["main"])} result rows.',
 f'Primary APC main joint recovery totals {sum(r["joint_recovery"] for r in primary)}/350 across the 14 levels.',
 f'Random-fP check: 150 shared frequency draws; primary APC joint recovery totals {sum(r["joint_recovery"] for r in randomprimary)}/150.',
 'Null checks: 350 timing-null pairs and 350 no-coupled-burst controls; all shared-component and signal-difference checks passed.',
 f'The original saved benchmark files remain byte-identical; MATLAB {metadata["matlab_version"]}.']
for i,fact in enumerate(facts,1):p(f'{i}. {fact}')
p('## Freeze and required compatibility checks')
p(table(['Check','Trials','Exact fA','Exact fP','Exact score','Joint recovery'],[
 ['oct2026, refinement=false; all distractor levels',175,175,175,175,sanity['checks']['distractor']['joint_recovery']],
 ['june2026_clipped, refinement=false; sparsity=.15',25,25,25,25,12]]))
p('Both compatibility checks and the five-trial v1 smoke test ran on the clean committed source before tagging. Their APC blob equals `v1.0:src/bst_apc.m`. '+link(OUT/'freeze_attestation.json')+' records the link to the frozen commit. Committed sanity rows: '+link(OUT/'committed_checks/sanity_trials.csv')+'. Smoke rows: '+link(OUT/'committed_checks/smoke_trials.csv')+'. Earlier pre-commit records were preserved separately.')
p('The v1 bandwidth rule was already 2*fP before this resume; no bandwidth-method correction was necessary. The smoke test returned candidate half-width = final nominal half-width = recovered fP in 5/5 trials. Changing amplitudeBandWidthHz from 4 to 40 Hz left all five numerical outputs unchanged. Per-trial CSVs record both nominal half-widths and the actual clipped final edges.')
smoke_rows=read('committed_checks/smoke_trials.csv');assert len(smoke_rows)==5
assert all(num(r,'effective_half_width_hz')==num(r,'recovered_fp_hz')==num(r,'candidate_half_width_hz') and int(r['amplitudeBandWidthHz_ignored'])==1 for r in smoke_rows)
p(table(['Smoke trial','Recovered fP Hz','Candidate half-width Hz','Final nominal half-width Hz','Final clipped band Hz'],[[r['repeat_index'],num(r,'recovered_fp_hz'),num(r,'candidate_half_width_hz'),num(r,'effective_half_width_hz'),r['final_amplitude_low_hz']+' to '+r['final_amplitude_high_hz']] for r in smoke_rows]))
p('## Definitions and configuration')
p('The primary APC mode uses a 1 Hz amplitude grid and candidate/final half-width equal to recovered fP. Refined fP uses the preserved demeaned Welch spectrum, a power-of-two zero-padding length giving ≤0.05 Hz bin spacing, and a three-point log-power parabola at an interior concave maximum. The legacy phase rule remains selectable with refinement=false. The inherited October 20 detrending/cycle-bound changes are excluded so the specified legacy checks reproduce the saved outputs. Full frozen implementation choices are in '+link(REPO/'analysis/v1_revision/PROTOCOL.md')+'.')
p('A0 uses amplitude half-width 6 Hz; A1 uses candidate fP. All comparators use phase half-width 1.5 Hz and fA grid 80:8:152. Each metric independently selects its full-grid maximum. Raw MVL and conventional Ozkurt-normalized MVL are separate scans. Ozkurt normalization is |sum(A exp(iφ))|/sqrt(N sum(A²)); the older helper with an additional 1/sqrt(N) is not used. KL-MI uses 18 phase bins; GLM uses R².')
p('Recovery limits are inclusive: phase ±1 Hz and amplitude ±8 Hz. “fA-only” and “fP-only” denote marginal criteria, rather than exclusive categories. Strict joint recovery replaces phase tolerance with ±0.5 Hz. All denominators remain 25; invalid estimates count as failures. Error summaries use finite estimates, with finite counts in the CSVs. Boundary picks use equality to 4/12 Hz within 1e-9; APC searches its own documented phase limits, rather than the comparator grid. `NaN` for APC grid spacing means no prescribed scan grid.')
p('## Main rerun')
p('Per-trial data: '+link(OUT/'main_trials.csv')+'. Full summaries, including finite counts and provenance: '+link(OUT/'main_summary.csv')+'.')
for bench in ['sparsity','distractor']:
    p('### '+bench.capitalize());p(table(headers,display([r for r in summary['main'] if r['benchmark']==bench])))
    p(f'![Joint recovery, {bench}]({(OUT/f"joint_recovery_{bench}.png").as_posix()})')
    p('Figure files: '+link(OUT/f'joint_recovery_{bench}.png')+', '+link(OUT/f'joint_recovery_{bench}.svg')+', '+link(OUT/f'joint_recovery_{bench}.fig')+'.')
p('## Random-fP check')
p('Each trial uses a single Uniform[5,11] Hz draw, shared by all methods. A separate stream with seed 20260618 supplies those draws; generator RNG is reset separately for each benchmark. Per-trial rows: '+link(OUT/'random_fp_trials.csv')+'. Draws: '+link(OUT/'random_fp_draws.csv')+'. Summary: '+link(OUT/'random_fp_summary.csv')+'.')
for bench in ['sparsity','distractor']:
    p('### '+bench.capitalize());p(table(headers,display([r for r in summary['random_fp'] if r['benchmark']==bench])))
p('## Null specificity and AUC')
p('Timing nulls retain coupling strength .60 and the original true-burst amplitude and sigma; only true-burst timing changes. Homogeneous Poisson events use the specified mean rates and original event support, on a separate RNG stream. Gaussian sums allow overlaps; no 56-ms gap was imposed. Carrier, background, distractor and the original noise samples/scale are shared exactly. The no-coupled-burst control removes only the true component and is reported separately. '+link(OUT/'null_pair_verification.json')+' contains all 350 pairing checks; maximum timing-null residual is '+fmt(max(r['timing_null_residual'] for r in verification['trials']))+'.')
p('False joint recovery uses fP within 1 Hz of 8 and fA within 8 Hz of 120. AUC compares all coupled/null score pairs with one half for ties; higher scores retain the original direction. Finite sample counts are reported. Raw null rows: '+link(OUT/'null_trials.csv')+'; recovery summaries: '+link(OUT/'null_recovery_summary.csv')+'; specificity/AUC: '+link(OUT/'null_specificity_auc.csv')+'.')
for kind in ['timing_null','no_coupled_burst']:
    p('### '+kind)
    p(table(['Benchmark','Level','Configuration','Method','False joint /25','AUC','Finite coupled/null'],[
        [r['benchmark'],float(r['level']),r['configuration'],r['method'],r['false_joint_recovery'],r['auc_coupled_vs_null'],f"{r['n_coupled_finite_scores']}/{r['n_null_finite_scores']}"] for r in nullout if r['null_type']==kind]))
p('## Runtime and deviations')
p(table(['Stage','Elapsed seconds','Status'],[[k,v['elapsed_seconds'],v['status']] for k,v in runtime.items()]))
p('Measured MATLAB elapsed time totals '+fmt(sum(v['elapsed_seconds'] for v in runtime.values()))+' seconds, including sanity and figure creation; it excludes MATLAB startup, implementation and report assembly. One computation thread was used.')
p('Tooling deviations: the earlier pre-commit Python read used Windows cp1252 and failed on byte 0x9d, a byte in a UTF-8 right curly quote in build_results.py (offsets 11611 and 11629 in the original file). The resumed workflow uses explicit UTF-8 text I/O. All repository MATLAB sources were verified ASCII; none required character replacement. The earlier stopped report and pre-commit check files were preserved. The committed sanity and smoke records use a separate committed_checks directory. Encoding audit: '+link(OUT/'encoding_audit.json')+'.')
p('The null definition follows the user’s replacement instruction: the timing null is primary and the zero-amplitude control is secondary. No trial counts, generators, seeds, level order or frozen method settings were changed after tagging. Legacy filters cache immutable design objects; continuously varying v1 carrier bands use the same fourth-order Butterworth family through direct SOS construction. The stated Welch/log-parabolic refinement, independent normalized-MVL scan, Poisson edge support and invalid-output handling were documented before tagging. Further tooling deviations, if any, are recorded in '+link(OUT/'tooling_deviations.json')+'. Original result hashes were rechecked in '+link(OUT/'original_results_verification.json')+'.')
p('## Full result provenance')
p('Every trial and summary CSV stores the commit, MATLAB version, complete APC option inputs, full comparator settings and seed. MAT checkpoints contain metadata plus input cases/components. PNG text, SVG metadata and MATLAB figure UserData embed provenance. The complete metadata record used for these results follows.')
p('```json\n'+json.dumps(metadata,indent=2)+'\n```')
(OUT/'RESULTS_v1.md').write_text('\n'.join(lines),encoding='utf-8')
(OUT/'result_provenance.json').write_text(json.dumps(metadata,indent=2),encoding="utf-8")
print('RESULTS_v1.md complete:',commit)
print('Rows:',{k:len(v) for k,v in raw.items()},'summary rows:',{k:len(v) for k,v in summary.items()})
