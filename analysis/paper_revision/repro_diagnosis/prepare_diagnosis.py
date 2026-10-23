"""Read-only source/history inventory; copies and instrumentation stay here."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib,re,difflib

D=Path(__file__).resolve().parent
ROOT=D.parents[1]
GIT=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
OUT=D/'results';OUT.mkdir(exist_ok=True)
SRC=D/'sources';SRC.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(repo,*args):
    p=subprocess.run([str(GIT),'-C',str(repo),*args],capture_output=True)
    return p.returncode,p.stdout,p.stderr
repos=[ROOT/'apc-brainstorm-publish',ROOT/'APC_NeuroImage_Submission_Package_2026-10-10/code/apc-brainstorm',ROOT/'APC_NeuroImage_Submission_Package_2026-10-10/APC_NeuroImage_Submission_Package_2026-10-10/code/apc-brainstorm']
commits={};repo_info=[]
for repo in repos:
    code,raw,err=git(repo,'log','--all','--reflog','--format=%H|%aI|%cI|%s','--','src/bst_apc.m','src/calc_MI_all_methods.m')
    info={'repository':str(repo),'exit_code':code,'stderr':err.decode(errors='replace')}
    info['log']=raw.decode(errors='replace').splitlines()
    _,head,_=git(repo,'rev-parse','HEAD');info['head']=head.decode().strip()
    _,alllog,_=git(repo,'log','--all','--format=%H|%aI|%cI|%s');info['all_commits']=alllog.decode().splitlines()
    _,fsck,fsckerr=git(repo,'fsck','--no-reflogs','--unreachable');info['unreachable_objects']=fsck.decode().splitlines();info['fsck_stderr']=fsckerr.decode(errors='replace')
    repo_info.append(info)
    for line in info['log']:
        h,a,c,s=line.split('|',3)
        item=commits.setdefault(h,{'hash':h,'author_date':a,'committer_date':c,'subject':s,'repositories':[]})
        item['repositories'].append(str(repo))
        for file in ['src/bst_apc.m','src/calc_MI_all_methods.m']:
            rc,blob,_=git(repo,'show',f'{h}:{file}')
            if rc==0:
                dest=SRC/f'{h[:12]}_{Path(file).name}'
                dest.write_bytes(blob)
                item.setdefault('files',{})[file]={'copy':str(dest),'sha256':sha(blob)}
(D/'git_history.json').write_text(json.dumps({'repositories':repo_info,'relevant_commits':list(commits.values())},indent=2),encoding='utf-8')

files=[]
for p in ROOT.rglob('bst_apc.m'):
    if D in p.parents:continue
    if any(part in p.parts for part in ['node_modules','pydeps','pydeps2','pydeps_copy','.tmp_pydeps']):continue
    b=p.read_bytes();files.append({'path':str(p),'sha256':sha(b),'modified_local':datetime.fromtimestamp(p.stat().st_mtime).isoformat(),'size':len(b)})
(D/'local_bst_inventory.json').write_text(json.dumps(files,indent=2),encoding='utf-8')

protected={}
for f in [ROOT/'bst_apc.m',ROOT/'calc_MI_all_methods.m',ROOT/'APC_MethodPaper_Final_version_clean_numbers_structured.docx',ROOT/'run_apc_burst_sparsity_benchmark.m',ROOT/'run_apc_distractor_frequency_benchmark.m',ROOT/'revision_checks/snapshot/bst_apc.m',ROOT/'revision_checks/snapshot/calc_MI_all_methods.m',ROOT/'revision_checks/snapshot/rc_distractor_source.m',ROOT/'revision_checks/snapshot/rc_sparsity_source.m']:
    protected[str(f)]=sha(f.read_bytes())
metadata=[]
for name in ['apc_burst_sparsity_runs_full.csv','apc_burst_sparsity_summary_full.csv','apc_burst_sparsity_benchmark_full.mat','apc_distractor_frequency_runs_reviewer_control.csv','apc_distractor_frequency_summary_reviewer_control.csv','apc_distractor_frequency_benchmark_reviewer_control.mat']:
    p=ROOT/name;s=p.stat();protected[str(p)]=sha(p.read_bytes())
    metadata.append({'path':str(p),'size':s.st_size,'created_local':datetime.fromtimestamp(s.st_ctime).isoformat(),'modified_local':datetime.fromtimestamp(s.st_mtime).isoformat(),'modified_utc':datetime.fromtimestamp(s.st_mtime,timezone.utc).isoformat(),'sha256':protected[str(p)]})
(D/'result_files_metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
(D/'protected_input_hashes.json').write_text(json.dumps(protected,indent=2),encoding='utf-8')

base=(ROOT/'revision_checks/snapshot/bst_apc.m').read_text(encoding='utf-8-sig')
current=(ROOT/'bst_apc.m').read_text(encoding='utf-8-sig')
def functions(s):
    starts=list(re.finditer(r'^function\s+.*$',s,re.M));out={}
    for i,m in enumerate(starts):
        header=m.group();name=re.search(r'(?:=\s*)?(\w+)\s*\(',header).group(1)
        out[name]=s[m.start():starts[i+1].start() if i+1<len(starts) else len(s)]
    return out
names=['detect_troughs','collect_phase_locked_tf','zscore_rows','bandpass_signal','estimate_amplitude_frequency','estimate_amplitude_frequency_tf_fallback','normalize_01','collect_event_epochs_by_index','get_amplitude_band']
all_versions={'preserved_baseline':base,'current_root':current}
for h,item in commits.items():
    if 'src/bst_apc.m' in item.get('files',{}):all_versions[h]=(Path(item['files']['src/bst_apc.m']['copy']).read_text(encoding='utf-8-sig'))
comparisons=[]
bf=functions(base)
for label,s in all_versions.items():
    ff=functions(s)
    changes=[]
    for name in names:
        a=bf.get(name,'');b=ff.get(name,'')
        comparisons.append({'version':label,'function':name,'baseline_present':bool(a),'version_present':bool(b),'text_equal':a==b,'baseline_sha256':sha(a.encode()),'version_sha256':sha(b.encode())})
        changes.extend(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile=f'preserved/{name}',tofile=f'{label}/{name}'))
    (D/f'step3_step4_diff_{label[:12]}.patch').write_text(''.join(changes) or '# No Step 3/4 function text differences from preserved baseline.\n',encoding='utf-8')
(D/'step3_step4_function_comparison.json').write_text(json.dumps(comparisons,indent=2),encoding='utf-8')

# Copy the exact earlier generator/noise prefix and all original local funcs.
for bench,srcname,trialname,param,signalname in [
    ('sparsity','apc-brainstorm-release/analysis/run_apc_burst_sparsity_benchmark.m','trialRows','keepRate','signal'),
    ('distractor','apc-brainstorm-release/analysis/run_apc_distractor_frequency_benchmark.m','[trialRows, oracleRows]','distractorScale','coupledSignal')]:
    source=(ROOT/srcname).read_text(encoding='utf-8-sig')
    tail=source[source.index('\nfunction cfg = local_get_profile'):]
    match=re.search(r'^function .* = local_run_trial\([^\n]*\)\n',source,re.M)
    prefix=source[match.end():source.index('    apcResult =',match.end())]
    header=f'''function varargout = rd_{bench}_source(action,varargin)
% Dispatch into copied historical functions. Generator/noise prefix unchanged.
    switch action
        case 'profile'
            varargout{{1}}=local_get_profile(varargin{{1}});
        case 'generate'
            cfg=varargin{{1}};{param}=varargin{{2}};
{prefix}
            varargout{{1}}={signalname};varargout{{2}}=t;
        case 'apc'
            varargout{{1}}=local_run_apc(varargin{{:}});
        otherwise
            error('repro_diagnosis:Action','Unknown action');
    end
end
'''
    (SRC/f'rd_{bench}_source.m').write_text(header+tail,encoding='utf-8')
    protected[str(ROOT/srcname)]=sha((ROOT/srcname).read_bytes())

# Instrument only bookkeeping in a copy. All numeric statements stay intact.
def instrument(text,name):
    out=text.replace('function sApc = bst_apc(sMatrix, OPTIONS)',f'function [sApc, routeLog] = {name}(sMatrix, OPTIONS)',1)
    assert out!=text
    out=out.replace('    nSignals = size(data, 1);','    nSignals = size(data, 1);\n    routeLog = strings(nSignals,1);',1)
    out=out.replace('        statusCode(iSignal)    = metrics.status_code;','        statusCode(iSignal)    = metrics.status_code;\n        routeLog(iSignal) = "not_reached";\n        if isfield(diagnostics,"selection_route"), routeLog(iSignal)=diagnostics.selection_route; end',1)
    out=out.replace('[ampFreq, ampWidth] = estimate_amplitude_frequency( ...','[ampFreq, ampWidth, selectionRoute] = estimate_amplitude_frequency( ...',1)
    out=out.replace('        options.amplitudeBandWidthHz);\n\n    if ~isfinite(ampFreq)','        options.amplitudeBandWidthHz);\n    diagnostics.selection_route=selectionRoute;\n\n    if ~isfinite(ampFreq)',1)
    out=out.replace('function [ampFreq, ampWidth] = estimate_amplitude_frequency(', 'function [ampFreq, ampWidth, selectionRoute] = estimate_amplitude_frequency(',1)
    idx=out.index('function [ampFreq, ampWidth, selectionRoute] = estimate_amplitude_frequency(')
    first=out[:idx];second=out[idx:]
    second=second.replace('    ampFreq = nan;','    selectionRoute="not_attempted";\n    ampFreq = nan;',1)
    second=second.replace('    if any(isfinite(scoreTrace))','    if any(isfinite(scoreTrace))\n        selectionRoute="direct_envelope_scan";',1)
    second=second.replace('    [ampFreq, ampWidth] = estimate_amplitude_frequency_tf_fallback(', '    selectionRoute="tf_fallback";\n    [ampFreq, ampWidth] = estimate_amplitude_frequency_tf_fallback(',1)
    out=first+second
    assert 'diagnostics.selection_route=selectionRoute' in out
    assert 'selectionRoute="direct_envelope_scan";' in out
    return out
(SRC/'rd_apc_instrumented.m').write_text(instrument(base,'rd_apc_instrumented'),encoding='utf-8')
(SRC/'bst_apc.m').write_bytes((ROOT/'revision_checks/snapshot/bst_apc.m').read_bytes())
(SRC/'calc_MI_all_methods.m').write_bytes((ROOT/'revision_checks/snapshot/calc_MI_all_methods.m').read_bytes())
(D/'instrumentation.patch').write_text(''.join(difflib.unified_diff(base.splitlines(True),(SRC/'rd_apc_instrumented.m').read_text().splitlines(True),fromfile='preserved/bst_apc.m',tofile='sources/rd_apc_instrumented.m')),encoding='utf-8')
(D/'protected_input_hashes.json').write_text(json.dumps(protected,indent=2),encoding='utf-8')
print('Commits:',[(h,c['committer_date']) for h,c in commits.items()])
print('Unique local bst_apc hashes:',len(set(x['sha256'] for x in files)))
print('Step3/4 differences:',[(x['version'],x['function']) for x in comparisons if not x['text_equal']])
