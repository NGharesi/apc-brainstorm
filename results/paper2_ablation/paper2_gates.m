function paper2_gates
% One prespecified gate run, with per-case checkpoints and immediate stop.
O=fileparts(mfilename('fullpath'));root=fileparts(fileparts(O));repo=fullfile(root,'apc-brainstorm-publish');cd(O);
addpath(fullfile(root,'revision_checks','final'),'-begin');addpath(O,'-begin');addpath(fullfile(repo,'src'),'-begin');
assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')));
m=jsondecode(fileread(fullfile(O,'provenance.json')));assert(m.protocol_public_on_origin);assert(~isfile(fullfile(O,'gate_results.json')));
start=tic;rows={};scans={};dest=fullfile(O,'gate_checkpoints');if ~isfolder(dest),mkdir(dest);end
try
 Q=readtable(fullfile(root,'revision_checks','final','burst_coupled_input.csv'),'Delimiter',',','NumHeaderLines',0,'ReadVariableNames',true,'TextType','string','Encoding','UTF-8','VariableNamingRule','preserve');x=Q.signal;t=Q.time_s;
 for v=["v1","v3"],one_apc("canonical",0,x,t,struct('fA',[80 150],'version',char(v)),v,[]);end
 for profile=["HA","heldout","ecog"],one_scan("canonical",0,x,500,profile);end
 bank=load(fullfile(root,'revision_checks','v3_aperiodic','HA_inputs.mat'),'cases');count=0;
 for id=1:numel(bank.cases)
  c=bank.cases{id};if string(c.dataset)~="coupled",continue;end
  count=count+1;if count>20,break;end
  saved=load(fullfile(root,'revision_checks','v3_aperiodic','checkpoints',sprintf('HA_estimates_%04d.mat',id)),'r1','r3');
  for v=["v1","v3"]
   ref=saved.r1;if v=="v3",ref=saved.r3;end
   one_apc("HA",id,c.signal,c.time,struct('fA',[80 150],'version',char(v)),v,ref);
  end
  one_scan("HA",id,c.signal,c.cfg.fs_hz,"HA");fprintf('GATES HA %d/20 complete\n',count);
 end
 assert(count>=20);
 G=struct2table(vertcat(rows{:}));S=struct2table(vertcat(scans{:}));writetable(G,fullfile(O,'gate_apc.csv'));writetable(S,fullfile(O,'gate_scan.csv'));
 guards=final_sos_filter('registry');save(fullfile(O,'gate_filter_guards.mat'),'guards','m');
 result=struct('status','PASS','apc_cases',height(G),'scan_cases',height(S),'tolerance',1e-10,'elapsed_seconds',toc(start),'provenance',m);
 writejson(fullfile(O,'gate_results.json'),result);fprintf('ALL GATES PASS %.3f seconds\n',toc(start));
catch err
 if ~isempty(rows),writetable(struct2table(vertcat(rows{:})),fullfile(O,'gate_apc.csv'));end
 if ~isempty(scans),writetable(struct2table(vertcat(scans{:})),fullfile(O,'gate_scan.csv'));end
 result=struct('status','STOPPED','identifier',err.identifier,'message',err.message,'elapsed_seconds',toc(start),'provenance',m);writejson(fullfile(O,'gate_error.json'),result);
 if startsWith(err.identifier,'Paper2:')||startsWith(err.identifier,'Final:')
  writejson(fullfile(O,'gate_results.json'),result);
  f=fopen(fullfile(O,'STOPPED.md'),'w','n','UTF-8');fprintf(f,'# STOPPED: component-ablation gate\n\n%s: %s\n\nNo full ablation run or endpoint statistics were started.\n\nCommit: %s\nProtocol SHA-256: %s\n',err.identifier,err.message,m.git_head,m.protocol_sha256);fclose(f);
 end
 rethrow(err);
end
 function one_apc(suite,id,x,t,opt,v,ref)
  before=rng;[r,info]=bst_apc(struct('data',x(:).','time',t(:).'),opt);
  [f,fd]=apc_fp_source(x,t,v,opt);fp=f.phase_frequency_hz;
  [a,ad,ao]=apc_fa_given_fp(x,t,fp,opt);
  observed=[a.phase_frequency_hz,a.amplitude_frequency_hz,a.pac_strength,a.preferred_phase_deg];
  expected=[r.phase_frequency_hz.Value,r.amplitude_frequency_hz.Value,r.pac_strength.Value,r.preferred_phase_deg.Value];
  finite=isfinite(expected)&isfinite(observed);pattern=isequal(isnan(expected),isnan(observed));errval=0;if any(finite),errval=max(abs(observed(finite)-expected(finite)));end
  pass=pattern&&errval<=1e-10&&a.status_code==r.status_code.Value;
  old_exact=true;if ~isempty(ref),old=[ref.phase_frequency_hz.Value,ref.amplitude_frequency_hz.Value,ref.pac_strength.Value,ref.preferred_phase_deg.Value,ref.status_code.Value];old_exact=isequaln([expected,r.status_code.Value],old);end
  assert(isequal(before,rng),'Paper2:GateRNG','Deterministic gate modified RNG');
  row=struct('suite',suite,'input_id',id,'version',v,'source_fp_hz',fp,'step2_status',f.status_code,'endtoend_status',r.status_code.Value,'extracted_status',a.status_code,'finite_fields_compared',sum(finite),'max_abs_error',errval,'nan_pattern_matches',pattern,'saved_endtoend_exact',old_exact,'pass',pass&&old_exact,'expected_fp',expected(1),'expected_fa',expected(2),'expected_raw_mvl',expected(3),'expected_phase_deg',expected(4),'observed_fp',observed(1),'observed_fa',observed(2),'observed_raw_mvl',observed(3),'observed_phase_deg',observed(4),'git_commit',string(m.git_head),'protocol_sha256',string(m.protocol_sha256),'options_json',string(jsonencode(opt)),'seed',20261101);
  rows{end+1}=row;save(fullfile(dest,sprintf('%s_%04d_%s.mat',suite,id,v)),'r','info','f','fd','a','ad','ao','opt','m','row');
  writetable(struct2table(vertcat(rows{:})),fullfile(O,'gate_apc.csv'));
  fprintf('APC GATE %s %d %s fP %.15g status%d maxerr %.3g PASS%d\n',suite,id,v,fp,a.status_code,errval,row.pass);
  assert(row.pass,'Paper2:APCGate','Extraction gate failed at %s input %d version %s (max abs error %.17g; pattern %d; saved exact %d)',suite,id,v,errval,pattern,old_exact);
 end
 function one_scan(suite,id,x,fs,profile)
  mode="A2_prime";if profile=="HA",mode="HA_A2_prime";elseif profile=="ecog",mode="ecog_A2_prime";end
  [reference,maps]=a2_reference_map(x,fs,profile,mode,.5);map=maps{1};j=find(map.fp_grid_hz==8);assert(isscalar(j));
  [selected,scores,settings]=scan_fa_given_fp(x,fs,8,profile);expected=map.scores(j,:,2);maxerr=max(abs(expected-scores));pass=all(isfinite(scores))&&maxerr<=1e-10;
  row=struct('suite',suite,'input_id',id,'profile',profile,'supplied_fp_hz',8,'bands_compared',numel(scores),'max_abs_error',maxerr,'pass',pass,'git_commit',string(m.git_head),'protocol_sha256',string(m.protocol_sha256),'settings_json',string(jsonencode(settings)),'seed',20261101);
  scans{end+1}=row;save(fullfile(dest,sprintf('scan_%s_%04d_%s.mat',suite,id,profile)),'reference','maps','selected','scores','settings','m','row');
  writetable(struct2table(vertcat(scans{:})),fullfile(O,'gate_scan.csv'));
  fprintf('SCAN GATE %s %d %s maxerr %.3g PASS%d\n',suite,id,profile,maxerr,pass);
  assert(pass,'Paper2:ScanGate','Scan score-column gate failed at %s input %d profile %s (max error %.17g)',suite,id,profile,maxerr);
 end
end
function writejson(file,value),f=fopen(file,'w','n','UTF-8');assert(f>=0);c=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(value));end
