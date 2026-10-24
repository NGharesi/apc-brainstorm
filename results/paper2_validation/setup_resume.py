from pathlib import Path
import subprocess, hashlib, json, datetime, re

O=Path(__file__).resolve().parent
root=O.parent.parent
repo=root/'apc-brainstorm-publish'
archive=repo/'results/paper2_ablation'
git=r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe'
def g(*a): return subprocess.check_output([git,'-C',str(repo),*a])
def sha(b): return hashlib.sha256(b).hexdigest()
head=g('rev-parse','HEAD').decode().strip()
assert head=='dbc0d7901091602e146e4d28b22fdadb043daef4'
assert head==g('rev-parse','origin/paper2').decode().strip() and not g('status','--porcelain')
protocol=g('show','HEAD:protocol/APC_paper2_validation_protocol.md')
assert sha(protocol)=='7b461e92a09d1a282225f07415d27ca7a4525984d3dab0ca5fc9c444700b6080'
old=json.loads((O/'provenance.json').read_text(encoding='utf-8'))
assert old['gates_started'] is False
(O/'provenance_before_amendment1.json').write_text(json.dumps(old,indent=2)+'\n',encoding='utf-8')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
old.update(status='RESUMED_BEFORE_GATES',git_head=head,protocol_sha256=sha(protocol),protocol_public_on_origin=True,
           amendment1_pushed_commit=head,resume_utc=now,amendment1_event_input='minimal struct: status 0 iff finite source fP; otherwise source status',
           previous_stop_preserved_sha256=sha((O/'STOPPED.md').read_bytes()))
(O/'provenance.json').write_text(json.dumps(old,indent=2)+'\n',encoding='utf-8')
with (O/'RESULTS_validation.md').open('a',encoding='utf-8') as f:
    f.write('\n## Resolution and resume\n\n'+f'Amendment 1 pushed as {head}; protocol SHA-256 {sha(protocol)}. Resumed {now}. '
            'A_EVENT uses the minimal source-status structure under Amendment 1. STOPPED.md remains unchanged as the pre-gate stop record. '
            'The transfer copy amend1_validation.md was not used.\n')
# Copy only unchanged private generator functions; expose them through a new no-method adapter.
p=(repo/'analysis/run_apc_premise_two_rhythm_benchmark.m').read_text(encoding='utf-8')
starts=list(re.finditer(r'^function\b.*$',p,re.M))
blocks={}
for i,m in enumerate(starts):
    line=m.group()
    for name in ['local_get_profile','local_cells','local_simulate_two_rhythm','local_gaussian_burst_envelope','local_add_mixed_noise','local_powerlaw_noise']:
        if re.search(r'\b'+name+r'\(',line): blocks[name]=p[m.start():starts[i+1].start() if i+1<len(starts) else len(p)]
assert len(blocks)==6
wrapper="""function varargout=validation_p1_generator(action,varargin)
% Adapter only; copied generator functions below are unchanged.
switch action
 case 'profile',varargout{1}=local_get_profile('holdout');
 case 'cells',varargout{1}=local_cells();
 case 'trial'
  cfg=varargin{1};c=varargin{2};t=0:1/cfg.fs_hz:cfg.duration_s-1/cfg.fs_hz;
  x=local_simulate_two_rhythm(t,cfg,c);x=local_add_mixed_noise(x,cfg.snr_db);
  varargout={x,t};
 otherwise,error('Validation:P1Action','Unknown generator action');
end
end

"""
(O/'validation_p1_generator.m').write_text(wrapper+''.join(blocks.values()),encoding='utf-8')
(O/'p1_extraction.json').write_text(json.dumps({'source':str(repo/'analysis/run_apc_premise_two_rhythm_benchmark.m'),
    'source_sha256':sha((repo/'analysis/run_apc_premise_two_rhythm_benchmark.m').read_bytes()),
    'unchanged_function_sha256':{k:sha(v.encode()) for k,v in blocks.items()}},indent=2)+'\n',encoding='utf-8')
# Repeat the original ablation gate code; only rename its entry point and add its immutable source folder.
q=(archive/'paper2_gates.m').read_text(encoding='utf-8')
q=q.replace('function paper2_gates','function validation_ablation_gates',1)
q=q.replace("addpath(O,'-begin');", "addpath(fullfile(repo,'results','paper2_ablation'),'-begin');addpath(O,'-begin');",1)
(O/'validation_ablation_gates.m').write_text(q,encoding='utf-8')
print(json.dumps({'resume_utc':now,'public_commit':head,'private_generator_functions_copied':list(blocks)},indent=2))
