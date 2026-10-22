function v1_revision(action,outDir)
% Committed-source sanity/smoke before tag; main/random_fp/null after tag.
A=fileparts(mfilename('fullpath'));repo=fileparts(fileparts(A));root=fileparts(repo);
if nargin<2,outDir=fullfile(root,'revision_checks','v1_rerun');end
if ~isfolder(outDir),mkdir(outDir);end
oldPath=path;oldDir=pwd;oldRng=rng;oldThreads=maxNumCompThreads(1);
cleanup=onCleanup(@() restore(oldPath,oldDir,oldRng,oldThreads)); %#ok<NASGU>
cd(outDir);addpath(A,'-begin');addpath(fullfile(repo,'src'),'-begin');
assert(strcmp(which('bst_apc'),fullfile(repo,'src','bst_apc.m')));
metadata=make_metadata(repo,root,action);start=tic;
diary(fullfile(outDir,[action '_progress.log']));logCleanup=onCleanup(@() diary('off')); %#ok<NASGU>
fprintf('BEGIN %s %s commit %s MATLAB %s\n',action,char(datetime('now')),metadata.git_commit,version);
try
 switch action
  case 'sanity'
   assert_committed(repo);
   run_sanity(root,outDir,metadata);
  case 'smoke'
   assert_committed(repo);run_smoke(outDir,metadata);
  case 'main'
   assert_frozen(repo);run_main(outDir,metadata);
  case 'random_fp'
   assert_frozen(repo);run_random(outDir,metadata);
  case 'null'
   assert_frozen(repo);run_null(outDir,metadata);
  case 'figures'
   assert_frozen(repo);v1_make_figures(outDir,metadata);
  otherwise
   error('v1:Action','Unknown action');
 end
 runtime=struct('status','COMPLETE','elapsed_seconds',toc(start),'completed_local',char(datetime('now')), 'metadata',metadata);
 write_json(fullfile(outDir,[action '_runtime.json']),runtime);
 fprintf('COMPLETE %s %.3f seconds\n',action,toc(start));
catch err
 runtime=struct('status','FAILED_STOP','elapsed_seconds',toc(start),'error_identifier',err.identifier,'error_message',err.message,'metadata',metadata);
 write_json(fullfile(outDir,[action '_runtime.json']),runtime);
 fprintf(2,'FAILED_STOP %s: %s\n',err.identifier,err.message);
 rethrow(err);
end
end
function metadata=make_metadata(repo,root,action)
metadata=struct('git_commit',git(repo,'rev-parse HEAD'),'git_tag','v1.0','matlab_version',version, ...
 'matlab_release',version('-release'),'seed',20260618,'computation_threads',1, ...
 'worktree_dirty',~isempty(git(repo,'status --porcelain')),'stage',action, ...
 'apc_source_git_blob',git(repo,'hash-object src/bst_apc.m'),'apc_configurations',v1_options());
if any(strcmp(action,{'sanity','smoke'})),metadata.git_tag='not_created_yet';end
metadata.comparator_settings=struct('phase_half_width_hz',1.5,'phase_grids',struct('main',4:1:12,'random_1Hz',4:1:12,'random_05Hz',4:.5:12), ...
 'amplitude_grid_hz',80:8:152,'A0_amplitude_half_width_hz',6,'A1_amplitude_half_width','candidate fP', ...
 'amplitude_clipping_hz','[max(1,fA-halfWidth),min(fs/2-1,fA+halfWidth)]', ...
 'filter','butter(4,[low high]/(fs/2),bandpass), filtfilt (8th-order bandpass)', ...
 'normalized_cutoff_clamps',[1e-4 .999],'phase_low_edge_min_hz',.5, ...
 'metrics',{{'MVL-raw','MVL-Ozkurt','KLMI-scan','GLM-scan'}},'num_phase_bins',18, ...
 'raw_MVL','abs(mean(A.*exp(1i*phase)))','Ozkurt_MVL','abs(sum(A.*exp(1i*phase)))/sqrt(N*sum(A.^2))', ...
 'GLM','max(0,1-SSE/SST); X=[ones,sin(phase),cos(phase)]','selection','independent full-grid argmax for each metric; MATLAB column-major first tie', ...
 'surrogates',false);
metadata.null_settings=struct('primary','timing_null','secondary','no_coupled_burst', ...
 'timing_null_coupling_level',.60,'poisson_stream','mt19937ar, separate stream seeded 20260618, reset per benchmark', ...
 'poisson_rate_distractor','true fP Hz','poisson_rate_sparsity','keep_rate * true fP Hz', ...
 'event_support','[t(1)-1/fP,t(end)+1/fP], original generator event support; original APC epoch-edge rejection unchanged', ...
 'overlap','allowed; original Gaussian envelope sum handles overlap; no minimum gap', ...
 'envelope_normalization','divide by maximum on recording, same as original generator', ...
 'paired_components','same carrier, noise vector including original noise scale, distractor and background; only true-burst component replaced', ...
 'verification_tolerance',1e-12,'secondary_coupling_level',0);
metadata.random_fp_settings=struct('distribution','uniform[5,11] Hz','stream','separate mt19937ar stream seed 20260618, reset per benchmark', ...
 'distractor_levels',[0 1.5 3],'sparsity_levels',[.15 .5 1],'repeats',25);
metadata.generator_settings=struct('sparsity',v1_sparsity_generator('profile'),'distractor',v1_distractor_generator('profile'));
metadata.recovery_settings=struct('fp_tolerance_hz',1,'strict_fp_tolerance_hz',.5,'fa_tolerance_hz',8,'boundary_values_hz',[4 12], ...
 'invalid_outputs','count as recovery failures; errors summarized over finite estimates with n_valid reported', ...
 'AUC','all coupled-vs-null score pairs, greater-than + half of ties; finite scores only; no score normalization or direction reversal');
metadata.paths=struct('repository',repo,'workspace',root);
end
function assert_committed(repo)
assert(strcmp(git(repo,'branch --show-current'),'v1.0-revision'),'v1:Branch','Wrong branch');
assert(isempty(git(repo,'status --porcelain')),'v1:Dirty','Checks require a clean committed source tree');
end
function assert_frozen(repo)
assert(strcmp(git(repo,'branch --show-current'),'v1.0-revision'),'v1:Branch','Wrong branch');
assert(strcmp(git(repo,'rev-parse HEAD'),git(repo,'rev-list -n 1 v1.0')),'v1:Tag','HEAD does not equal v1.0');
assert(isempty(git(repo,'status --porcelain')),'v1:Dirty','Frozen repository has uncommitted changes');
end
function run_sanity(root,outDir,metadata)
guard_new(fullfile(outDir,'sanity_trials.csv'));
presets=v1_options();allRows={};checks=struct();
for bench=["distractor","sparsity"]
 [gen,cfg,levels]=setup(bench);rng(20260618,'twister');
 if bench=="distractor"
  original=load(fullfile(root,'apc_distractor_frequency_benchmark_reviewer_control.mat'),'runTable');mode=2;levelColumn='distractor_scale';
 else
  original=load(fullfile(root,'apc_burst_sparsity_benchmark_full.mat'),'runTable');mode=3;levelColumn='burst_keep_rate';
 end
 saved=original.runTable;saved=saved(string(saved.method)=="APC",:);
 bank=load(fullfile(root,'revision_checks','repro_diagnosis','results',char('generated_inputs_'+bench+'.mat')),'signalBank');
 nInputs=0;nAnalyzed=0;nFA=0;nFP=0;nScore=0;nJoint=0;
 for il=1:numel(levels)
  for ir=1:25
   [signal,time]=gen('generate',cfg,levels(il));nInputs=nInputs+1;
   assert(isequal(signal,bank.signalBank{nInputs}),'v1:GeneratorMismatch','Original input not reproduced');
   if bench=="sparsity" && levels(il)~=.15,continue;end
   before=rng;[r,info]=bst_apc(struct('data',signal,'time',time),presets(mode).options);assert(isequal(before,rng));
   q=saved(abs(saved.(levelColumn)-levels(il))<1e-12 & saved.repeat_index==ir,:);assert(height(q)==1);
   fp=double(r.phase_frequency_hz.Value(1));fa=double(r.amplitude_frequency_hz.Value(1));score=double(r.pac_strength.Value(1));
   nAnalyzed=nAnalyzed+1;nFA=nFA+(fa==q.recovered_fa_hz);nFP=nFP+(fp==q.recovered_fp_hz);nScore=nScore+(score==q.score);
   nJoint=nJoint+(abs(fp-8)<=1 && abs(fa-120)<=8);
   item=struct('configuration',string(presets(mode).name),'method',"APC",'fp_grid_step_hz',nan,'fp',fp,'fa',fa,'score',score,'route',info.route(1),'status',double(r.status_code.Value(1)), ...
    'candidate_half_width_hz',info.candidate_half_width_hz(1),'effective_half_width_hz',info.effective_half_width_hz(1),'final_low_hz',info.final_band_hz(1,1),'final_high_hz',info.final_band_hz(1,2));
   row=pack('sanity',bench,'coupled',levels(il),ir,cfg,item,metadata,nan,nan);
   row.saved_fp_hz=q.recovered_fp_hz;row.saved_fa_hz=q.recovered_fa_hz;row.saved_score=q.score;
   row.fp_exact_match=fp==q.recovered_fp_hz;row.fa_exact_match=fa==q.recovered_fa_hz;row.score_exact_match=score==q.score;
   allRows{end+1}=row; %#ok<AGROW>
   if mod(ir,5)==0,fprintf('SANITY %s %.2f %d/25: fP %d fA %d score %d exact cumulative\n',bench,levels(il),ir,nFP,nFA,nScore);end
  end
 end
 checks.(bench)=struct('generator_trials_exact',nInputs,'analyzed_trials',nAnalyzed,'fP_exact',nFP,'fA_exact',nFA,'score_exact',nScore,'joint_recovery',nJoint);
end
T=struct2table([allRows{:}]);v1_write_csv(T,fullfile(outDir,'sanity_trials.csv'));
passed=checks.distractor.fP_exact==175 && checks.distractor.fA_exact==175 && checks.distractor.score_exact==175 && checks.sparsity.fA_exact==25 && checks.sparsity.fP_exact==25 && checks.sparsity.score_exact==25 && checks.sparsity.joint_recovery==12;
write_json(fullfile(outDir,'sanity_results.json'),struct('passed',passed,'checks',checks,'metadata',metadata));
assert(passed,'v1:SanityFailed','Compatibility check failed; stop without tagging or benchmarks');
fprintf('BOTH SANITY CHECKS PASSED\n');
end
function run_smoke(outDir,metadata)
guard_new(fullfile(outDir,'smoke_trials.csv'));presets=v1_options();options=presets(1).options;
cfg=v1_sparsity_generator('profile');rng(20260618,'twister');rows={};
for ir=1:5
 [signal,time]=v1_sparsity_generator('generate',cfg,1);before=rng;
 [r,info]=bst_apc(struct('data',signal,'time',time),options);
 override=options;override.amplitudeBandWidthHz=40;
 [r2,info2]=bst_apc(struct('data',signal,'time',time),override);
 fp=double(r.phase_frequency_hz.Value(1));fa=double(r.amplitude_frequency_hz.Value(1));
 assert(double(r.status_code.Value(1))==0 && isfinite(fp),'v1:SmokeStatus','v1 smoke did not return a valid result');
 assert(info.candidate_half_width_hz(1)==fp && info.final_half_width_hz(1)==fp,'v1:SmokeBandwidth','Effective v1 half-width differs from recovered fP');
 assert(isequaln(r,r2)&&isequal(info.route,info2.route)&&isequaln(info.final_band_hz,info2.final_band_hz),'v1:SmokeIgnoredWidth','amplitudeBandWidthHz changed v1 result');
 assert(isequal(before,rng),'v1:SmokeRNG','Smoke consumed simulation RNG');
 item=struct('configuration',"v1.0",'method',"APC",'fp_grid_step_hz',nan,'fp',fp,'fa',fa,'score',double(r.pac_strength.Value(1)), ...
  'route',info.route(1),'status',double(r.status_code.Value(1)),'candidate_half_width_hz',info.candidate_half_width_hz(1), ...
  'effective_half_width_hz',info.final_half_width_hz(1),'final_low_hz',info.final_band_hz(1,1),'final_high_hz',info.final_band_hz(1,2));
 row=pack('smoke','sparsity','coupled',1,ir,cfg,item,metadata,nan,nan);
 row.amplitudeBandWidthHz_ignored=true;row.tested_override_width_hz=40;
 row.override_apc_options_json=string(jsonencode(override));rows{end+1}=row; %#ok<AGROW>
 fprintf('SMOKE %d/5 fP %.17g candidate-half %.17g final-half %.17g; width override ignored\n',ir,fp,info.candidate_half_width_hz(1),info.final_half_width_hz(1));
end
T=struct2table([rows{:}]);v1_write_csv(T,fullfile(outDir,'smoke_trials.csv'));
write_json(fullfile(outDir,'smoke_results.json'),struct('passed',true,'n_trials',5,'all_half_widths_equal_recovered_fP',true,'amplitudeBandWidthHz_ignored',true,'metadata',metadata));
end
function run_main(outDir,metadata)
file=fullfile(outDir,'main_trials.csv');guard_new(file);presets=v1_options();
for bench=["sparsity","distractor"]
 [gen,cfg,levels]=setup(bench);rng(20260618,'twister');
 for il=1:numel(levels)
  rows={};cases=cell(1,25);level=levels(il);
  for ir=1:25
   [signal,time,parts]=gen('generate',cfg,level);before=rng;
   cases{ir}=struct('signal',signal,'time',time,'parts',parts,'cfg',cfg,'level',level,'repeat_index',ir);
   r=analyze(signal,time,cfg,presets,["A0","A1"],1);
   assert(isequal(before,rng),'v1:RNG','Analysis consumed simulation RNG state');
   for k=1:numel(r),rows{end+1}=pack('main',bench,'coupled',level,ir,cfg,r(k),metadata,nan,nan);end %#ok<AGROW>
   if mod(ir,5)==0,fprintf('MAIN %s %.2f %d/25\n',bench,level,ir);end
  end
  T=struct2table([rows{:}]);v1_write_csv(T,file,true);
  save(fullfile(outDir,sprintf('main_%s_level_%g.mat',bench,level)),'T','cases','metadata','-v7.3');
 end
end
end
function run_random(outDir,metadata)
file=fullfile(outDir,'random_fp_trials.csv');guard_new(file);presets=v1_options();presets=presets([1 4]);
for bench=["sparsity","distractor"]
 [gen,cfg,~]=setup(bench);rng(20260618,'twister');fpStream=RandStream('mt19937ar','Seed',20260618);
 if bench=="sparsity",levels=[.15 .5 1];else,levels=[0 1.5 3];end
 for il=1:numel(levels)
  rows={};cases=cell(1,25);level=levels(il);
  for ir=1:25
   cfg.true_fp_hz=5+6*rand(fpStream);[signal,time,parts]=gen('generate',cfg,level);before=rng;
   cases{ir}=struct('signal',signal,'time',time,'parts',parts,'cfg',cfg,'level',level,'repeat_index',ir);
   r=analyze(signal,time,cfg,presets,["A0","A1"],[1 .5]);assert(isequal(before,rng));
   for k=1:numel(r),rows{end+1}=pack('random_fp',bench,'coupled',level,ir,cfg,r(k),metadata,nan,nan);end %#ok<AGROW>
   if mod(ir,5)==0,fprintf('RANDOM-FP %s %.2f %d/25\n',bench,level,ir);end
  end
  T=struct2table([rows{:}]);v1_write_csv(T,file,true);
  save(fullfile(outDir,sprintf('random_fp_%s_level_%g.mat',bench,level)),'T','cases','metadata','-v7.3');
 end
end
end
function run_null(outDir,metadata)
file=fullfile(outDir,'null_trials.csv');guard_new(file);presets=v1_options();presets=presets(1);
verification={};
for bench=["sparsity","distractor"]
 [~,~,levels]=setup(bench);poissonStream=RandStream('mt19937ar','Seed',20260618);
 for il=1:numel(levels)
  level=levels(il);bank=load(fullfile(outDir,sprintf('main_%s_level_%g.mat',bench,level)),'cases');rows={};nullCases=cell(1,25);
  for ir=1:25
   c=bank.cases{ir};cfg=c.cfg;rate=cfg.true_fp_hz;if bench=="sparsity",rate=rate*level;end
   times=poisson_times(poissonStream,rate,c.time(1)-1/cfg.true_fp_hz,c.time(end)+1/cfg.true_fp_hz);
   env=zeros(size(c.time));for k=1:numel(times),env=env+exp(-.5*((c.time-times(k))/cfg.burst_sigma_s).^2);end
   if max(env)>0,env=env/max(env);end
   newTrue=cfg.true_high_amp*cfg.coupling_level*env.*c.parts.carrier;
   timing=c.signal-c.parts.true_component+newTrue;absent=c.signal-c.parts.true_component;
   residual=max(abs((c.signal-timing)-(c.parts.true_component-newTrue)));
   residualAbsent=max(abs((c.signal-absent)-c.parts.true_component));
   assert(residual<=1e-12 && residualAbsent<=1e-12,'v1:NullPair','Matched null component verification failed');
   nullParts=c.parts;nullParts.true_component=newTrue;nullParts.true_envelope=env;
   shared={'carrier','noise','low_component','background_component','distractor_component'};
   for f=1:numel(shared),assert(isequal(c.parts.(shared{f}),nullParts.(shared{f})),'v1:NullShared','Shared component differs');end
   nullCases{ir}=struct('timing_null',timing,'no_coupled_burst',absent,'poisson_times',times,'new_true_component',newTrue,'pair_residual',residual,'cfg',cfg);
   verification{end+1}=struct('benchmark',bench,'level',level,'repeat_index',ir,'poisson_event_count',numel(times), ...
    'poisson_events_in_recording',sum(times>=c.time(1)&times<=c.time(end)),'timing_null_residual',residual,'no_coupled_burst_residual',residualAbsent,'shared_components_exact',true); %#ok<AGROW>
   for dataset=["timing_null","no_coupled_burst"]
    signal=timing;count=numel(times);recordCfg=cfg;usedResidual=residual;
    if dataset=="no_coupled_burst",signal=absent;count=0;recordCfg.coupling_level=0;usedResidual=residualAbsent;end
    before=rng;r=analyze(signal,c.time,cfg,presets,"A1",1);assert(isequal(before,rng));
    for k=1:numel(r),rows{end+1}=pack('null',bench,dataset,level,ir,recordCfg,r(k),metadata,count,usedResidual);end %#ok<AGROW>
   end
   if mod(ir,5)==0,fprintf('NULL %s %.2f %d/25 max component residual %.3g\n',bench,level,ir,residual);end
  end
  T=struct2table([rows{:}]);v1_write_csv(T,file,true);
  save(fullfile(outDir,sprintf('null_%s_level_%g.mat',bench,level)),'T','nullCases','metadata','-v7.3');
 end
end
write_json(fullfile(outDir,'null_pair_verification.json'),struct('trials',[verification{:}],'metadata',metadata));
end
function times=poisson_times(stream,rate,low,high)
times=[];t=low;
while true
 t=t-log(max(rand(stream),realmin))/rate;
 if t>high,break;end
 times(end+1)=t; %#ok<AGROW>
end
end
function rows=analyze(signal,time,cfg,presets,modes,steps)
rows=struct('configuration',{},'method',{},'fp_grid_step_hz',{},'fp',{},'fa',{},'score',{},'route',{},'status',{}, ...
 'candidate_half_width_hz',{},'effective_half_width_hz',{},'final_low_hz',{},'final_high_hz',{});
for i=1:numel(presets)
 [r,info]=bst_apc(struct('data',signal,'time',time),presets(i).options);
 rows(end+1)=struct('configuration',string(presets(i).name),'method',"APC",'fp_grid_step_hz',nan, ...
 'fp',double(r.phase_frequency_hz.Value(1)),'fa',double(r.amplitude_frequency_hz.Value(1)), ...
 'score',double(r.pac_strength.Value(1)),'route',info.route(1),'status',double(r.status_code.Value(1)), ...
 'candidate_half_width_hz',info.candidate_half_width_hz(1),'effective_half_width_hz',info.effective_half_width_hz(1), ...
 'final_low_hz',info.final_band_hz(1,1),'final_high_hz',info.final_band_hz(1,2)); %#ok<AGROW>
end
comps=v1_comparators(signal,cfg.fs_hz,modes,steps);rows=[rows,comps];
end
function row=pack(stage,bench,dataset,level,ir,cfg,r,metadata,count,residual)
row=struct('stage',string(stage),'benchmark',string(bench),'dataset',string(dataset),'level',level,'repeat_index',ir, ...
 'true_fp_hz',cfg.true_fp_hz,'true_fa_hz',cfg.true_fa_hz,'configuration',string(r.configuration),'method',string(r.method), ...
 'fp_grid_step_hz',r.fp_grid_step_hz,'recovered_fp_hz',r.fp,'recovered_fa_hz',r.fa,'score',r.score,'route',string(r.route), ...
 'status_code',r.status,'valid',r.status==0 && isfinite(r.fp)&&isfinite(r.fa)&&isfinite(r.score), ...
 'candidate_half_width_hz',r.candidate_half_width_hz,'effective_half_width_hz',r.effective_half_width_hz, ...
 'final_amplitude_low_hz',r.final_low_hz,'final_amplitude_high_hz',r.final_high_hz, ...
 'poisson_event_count',count,'matched_null_residual',residual,'git_commit',string(metadata.git_commit), ...
 'matlab_version',string(metadata.matlab_version),'seed',metadata.seed, ...
 'apc_options_json',string(jsonencode(metadata.apc_configurations)), ...
 'comparator_settings_json',string(jsonencode(metadata.comparator_settings)), ...
 'generator_settings_json',string(jsonencode(cfg)));
end
function [gen,cfg,levels]=setup(bench)
if bench=="sparsity",gen=@v1_sparsity_generator;cfg=gen('profile');levels=cfg.burst_keep_rates;
else,gen=@v1_distractor_generator;cfg=gen('profile');levels=cfg.distractor_scale_values;end
end
function guard_new(file)
assert(~isfile(file),'v1:ExistingResult','Output already exists; refusing to replace earlier results');
end
function s=git(repo,args)
exe='C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe';
[status,s]=system(sprintf('"%s" -C "%s" %s',exe,repo,args));assert(status==0,'v1:Git','Git command failed');s=strtrim(s);
end
function write_json(file,value)
f=fopen(file,'w');assert(f>=0);c=onCleanup(@() fclose(f)); %#ok<NASGU>
fprintf(f,'%s',jsonencode(value,'PrettyPrint',true));
end
function restore(p,d,r,t)
path(p);cd(d);rng(r);maxNumCompThreads(t);
end
