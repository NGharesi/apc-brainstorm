function run_v2_heldout(action,worker)
% Frozen execution: inspect, generate once, then disjoint analysis workers.
if nargin<2,worker=1;end
A=strrep(fileparts(mfilename('fullpath')),'/','\');repo=fileparts(fileparts(A));root=fileparts(repo);
out=fullfile(root,'revision_checks','v2','candidate_03');
oldPath=path;oldDir=pwd;oldRng=RandStream.getGlobalStream;oldThreads=maxNumCompThreads(1);
cleanup=onCleanup(@() restore(oldPath,oldDir,oldRng,oldThreads)); %#ok<NASGU>
cd(out);addpath(fullfile(repo,'analysis','v1_revision'),'-begin');addpath(A,'-begin');addpath(fullfile(repo,'src'),'-begin');
assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')));
unit=jsondecode(fileread(fullfile(out,'unit_attempt_01','unit_results.json')));
assert(strcmp(unit.status,'UNIT_GATES_PASSED'),'v2:UnitGate','Unit gates did not pass');
assert(strcmp(git(repo,'hash-object src/bst_apc.m'),unit.metadata.apc_source_blob),'v2:Source','Tested source changed');
metadata=make_metadata(repo,out,unit);
if strcmp(action,'inspect')
 write_json(fullfile(out,'headless_inspection.json'),struct('metadata',metadata));
 fprintf('TPAC path: %s; available=%d; configured install exists=%d\n',metadata.tpac.path,metadata.tpac.available,metadata.tpac.configured_install_exists);
 return;
end
assert(strcmp(git(repo,'rev-parse HEAD'),git(repo,'rev-list -n 1 v2.0')) && isempty(git(repo,'status --porcelain')),'v2:Freeze','Require tagged clean source');
metadata.git_tag='v2.0';start=tic;
try
 switch action
  case 'generate',generate_inputs(out,metadata);
  case 'analyze',analyze_worker(out,worker,metadata);
  otherwise,error('v2:Action','Unknown held-out action');
 end
 result=struct('status','COMPLETE','action',action,'worker',worker,'elapsed_seconds',toc(start),'completed_local',char(datetime('now')),'metadata',metadata);
 name=action;if strcmp(action,'analyze'),name=sprintf('worker_%d',worker);end
 write_json(fullfile(out,[name '_runtime.json']),result);fprintf('COMPLETE %s worker%d %.3f seconds\n',action,worker,toc(start));
catch err
 result=struct('status','FAILED_STOP','action',action,'worker',worker,'elapsed_seconds',toc(start),'identifier',err.identifier,'error',err.message,'metadata',metadata);
 write_json(fullfile(out,sprintf('%s_worker%d_failure.json',action,worker)),result);rethrow(err);
end
end

function meta=make_metadata(repo,out,unit)
p=v1_options();v1=p(1).options;v1.fA=[80 160];v1.version='v1';v2=v1;v2.version='v2';v2.eventSurrogateSeed=20261022;v2.eventSurrogateSubstream=1001;
meta=struct('candidate',3,'git_commit',git(repo,'rev-parse HEAD'),'git_tag','not_created_yet','matlab_version',version, ...
 'seed',20261022,'apc_source_blob',git(repo,'hash-object src/bst_apc.m'),'unit_tested_source_blob',unit.metadata.apc_source_blob, ...
 'unit_test_base_commit',unit.metadata.git_commit,'unit_gates',unit.gates,'apc_configurations',struct('v2',v2,'v1',v1), ...
 'comparator_settings',struct('phase_grid_hz',3:.5:14,'phase_half_width_hz',1.5,'amplitude_grid_hz',80:4:160, ...
  'A2_prime_half_width_hz',14,'A1_prime_half_width','candidate fP','filter','butter(4) bandpass, filtfilt (8th-order bandpass)', ...
  'cutoff_clamps',[1e-4 .999],'amplitude_clipping','[max(1,fA-half),min(fs/2-1,fA+half)]', ...
  'metrics',{{'MVL-raw','MVL-Ozkurt','KLMI','GLM'}},'phase_bins',18,'Ozkurt','raw_MVL/sqrt(mean(A.^2))', ...
  'GLM','max(0,1-SSE/SST), X=[ones sin(phase) cos(phase)]','selection','independent full-grid maximum, first column-major tie','surrogates',false), ...
 'streams',struct('generator','mrg32k3a','seed',20261022,'signal_substream',1,'frequency_substream',2,'poisson_substream',3,'event_substream','1000+input_id'), ...
 'recovery',struct('phase_tolerance_hz',1,'strict_phase_tolerance_hz',.5,'amplitude_tolerance_hz',8,'invalid','recovery failure','AUC','finite scores, greater + half ties'), ...
 'generator_profiles',struct('sparsity',v1_sparsity_generator('profile'),'distractor',v1_distractor_generator('profile'),'slow',v2_heldout_generator('slow_profile')), ...
 'protocol',fileread(fullfile(repo,'analysis','v2_revision','PROTOCOL_v2.md')), ...
 'execution',fileread(fullfile(repo,'analysis','v2_revision','HELDOUT_EXECUTION.md')),'paths',struct('repository',repo,'output',out));
tpacPath=which('process_tpac');install='C:\Users\nghare\Documents\Brainstorm3\brainstorm_221219\brainstorm3';
meta.tpac=struct('path',tpacPath,'available',~isempty(tpacPath),'configured_install',install,'configured_install_exists',isfolder(install), ...
 'included',false,'reason','process_tpac absent from configured MATLAB path; configured Brainstorm install is unavailable');
if ~isempty(tpacPath),meta.tpac.reason='FOUND: inspect existing headless interface before execution';end
end

function generate_inputs(out,meta)
file=fullfile(out,'heldout_inputs.mat');assert(~isfile(file),'v2:ExistingInputs','Preserve existing held-out inputs');
assert(~meta.tpac.available,'v2:TPACReview','Inspect available tPAC interface before deciding inclusion');
signalStream=new_stream(1);frequencyStream=new_stream(2);poissonStream=new_stream(3);RandStream.setGlobalStream(signalStream);
cases={};verification={};draws={};
for scenario=["H1_sparsity","H1_distractor","H2","H4"]
 switch scenario
  case 'H1_sparsity',levels=[1 .55 .25 .15];cfg=v2_heldout_generator('sparsity_profile');generator='sparsity';
  case 'H1_distractor',levels=[0 1.5 3];cfg=v2_heldout_generator('distractor_profile');generator='distractor';
  case 'H2',levels=[0 .5 1 1.5 2 3];cfg=v2_heldout_generator('slow_profile');generator='slow';
  case 'H4',levels=0;cfg=v2_heldout_generator('distractor_profile');cfg.duration_s=12;cfg.continuous_modulation_depth=.70;cfg.continuous_high_amp=1.25;generator='continuous';
 end
 cfg.random_seed=20261022;cfg.snr_db=-3;cfg.broad_fa_band_hz=[80 160];
 for level=levels
  for ir=1:25
   fd=nan;phi=nan;
   if scenario=="H2"
    cfg.true_fp_hz=4+3*rand(frequencyStream);fd=cfg.true_fp_hz+3+(13-cfg.true_fp_hz-3)*rand(frequencyStream);phi=2*pi*rand(frequencyStream);cfg.true_fa_hz=90+50*rand(frequencyStream);
    cfg.slow_distractor_hz=fd;cfg.slow_distractor_phase_rad=phi;cfg.slow_amplitude_ratio=level;
   else
    cfg.true_fp_hz=5+6*rand(frequencyStream);cfg.true_fa_hz=90+50*rand(frequencyStream);
    if scenario=="H1_distractor",cfg.distractor_fa_hz=cfg.true_fa_hz-24;end
   end
   before=signalStream.State;
   if scenario=="H4",[signal,time,parts]=v2_heldout_generator(generator,cfg);else,[signal,time,parts]=v2_heldout_generator(generator,cfg,level);end
   id=numel(cases)+1;c=struct('input_id',id,'paired_coupled_id',id,'scenario',scenario,'dataset',"coupled",'level',level,'repeat_index',ir, ...
    'signal',signal,'time',time,'parts',parts,'cfg',cfg,'true_fd_hz',fd,'distractor_phase_rad',phi,'signal_rng_state_before',before, ...
    'signal_rng_state_after',signalStream.State,'poisson_times',[],'removed_true_component',[],'added_true_component',[],'pair_residual',nan);
   cases{end+1}=c; %#ok<AGROW>
   draws{end+1}=struct('scenario',scenario,'level',level,'repeat_index',ir,'coupled_input_id',id,'true_fp_hz',cfg.true_fp_hz,'true_fa_hz',cfg.true_fa_hz,'true_fd_hz',fd,'distractor_phase_rad',phi, ...
    'git_commit',string(meta.git_commit),'matlab_version',string(version),'seed',20261022,'apc_options_json',string(jsonencode(meta.apc_configurations)),'comparator_settings_json',string(jsonencode(meta.comparator_settings)),'generator_settings_json',string(jsonencode(cfg))); %#ok<AGROW>
   needTiming=startsWith(scenario,"H1") || (scenario=="H2" && ismember(level,[0 1 3]));
   if needTiming
    rate=cfg.true_fp_hz;if scenario=="H1_sparsity",rate=rate*level;end
    times=poisson_times(poissonStream,rate,time(1)-1/cfg.true_fp_hz,time(end)+1/cfg.true_fp_hz);
    env=zeros(size(time));for k=1:numel(times),env=env+exp(-.5*((time-times(k))/cfg.burst_sigma_s).^2);end
    if max(env)>0,env=env/max(env);end
    newTrue=cfg.true_high_amp*cfg.coupling_level*env.*parts.carrier;
    n=c;n.input_id=numel(cases)+1;n.dataset="timing_null";n.signal=signal-parts.true_component+newTrue;
    n.poisson_times=times;n.parts.true_component=newTrue;n.parts.true_envelope=env;n.removed_true_component=parts.true_component;n.added_true_component=newTrue;
    n.pair_residual=max(abs((c.signal-n.signal)-(parts.true_component-newTrue)));
    assert(n.pair_residual<=1e-12,'v2:NullPair','Timing null changes more than true burst');
    cases{end+1}=n;verification{end+1}=verification_row(n,meta); %#ok<AGROW>
   end
   needAbsent=(scenario=="H1_sparsity" && ismember(level,[1 .15])) || (scenario=="H1_distractor" && level==3);
   if needAbsent
    n=c;n.input_id=numel(cases)+1;n.dataset="no_coupled_burst";n.signal=signal-parts.true_component;n.cfg.coupling_level=0;
    n.parts.true_component=zeros(size(signal));n.removed_true_component=parts.true_component;n.added_true_component=zeros(size(signal));
    n.pair_residual=max(abs((c.signal-n.signal)-parts.true_component));assert(n.pair_residual<=1e-12,'v2:NullPair','Absent control changes other components');
    cases{end+1}=n;verification{end+1}=verification_row(n,meta); %#ok<AGROW>
   end
  end
  fprintf('GENERATED %s level%g 25 paired repeats; total inputs %d\n',scenario,level,numel(cases));
 end
end
assert(numel(cases)==675 && numel(draws)==350 && numel(verification)==325);
save(file,'cases','meta','-v7.3');v1_write_csv(struct2table([draws{:}]),fullfile(out,'heldout_frequency_draws.csv'));
v1_write_csv(struct2table([verification{:}]),fullfile(out,'heldout_null_pair_verification.csv'));
write_json(fullfile(out,'heldout_input_manifest.json'),struct('inputs',675,'coupled',350,'timing_null',250,'no_coupled_burst',75,'metadata',meta));
end

function analyze_worker(out,worker,meta)
assert(ismember(worker,1:3));bank=load(fullfile(out,'heldout_inputs.mat'),'cases');cases=bank.cases;
indices=worker:3:numel(cases);chunkSize=25;chunkFiles={};
for begin=1:chunkSize:numel(indices)
 subset=indices(begin:min(begin+chunkSize-1,numel(indices)));file=fullfile(out,sprintf('heldout_worker%d_chunk%03d.mat',worker,ceil(begin/chunkSize)));
 chunkFiles{end+1}=file; %#ok<AGROW>
 if isfile(file),old=load(file,'metadata');assert(strcmp(old.metadata.git_commit,meta.git_commit));fprintf('RESUME worker%d existing chunk%d\n',worker,ceil(begin/chunkSize));continue;end
 rows={};details=cell(1,numel(subset));
 for j=1:numel(subset)
  c=cases{subset(j)};before=rng;v2=meta.apc_configurations.v2;v2.eventSurrogateSubstream=1000+c.input_id;
  [r,info]=bst_apc(struct('data',c.signal,'time',c.time),v2);
  rows{end+1}=pack(c,"v2.0","APC",double(r.phase_frequency_hz.Value(1)),double(r.amplitude_frequency_hz.Value(1)),double(r.pac_strength.Value(1)),double(r.status_code.Value(1)),meta,info.options,r,info); %#ok<AGROW>
  d=info.diagnostics{1};details{j}=struct('input_id',c.input_id,'phase_grid',d.phase_grid_hz,'BLP',d.blp_grid,'PPC',d.ppc_grid, ...
   'amplitude_grid',d.amplitude_grid_hz,'amplitude_scores',d.amplitude_scores_raw,'surrogate_max_BLP',d.surrogate_blp_max,'surrogate_fixed_BLP',d.surrogate_blp_fixed,'options',info.options);
  [r,info]=bst_apc(struct('data',c.signal,'time',c.time),meta.apc_configurations.v1);
  rows{end+1}=pack(c,"v1.0","APC",double(r.phase_frequency_hz.Value(1)),double(r.amplitude_frequency_hz.Value(1)),double(r.pac_strength.Value(1)),double(r.status_code.Value(1)),meta,info.options,[],info); %#ok<AGROW>
  comps=v2_heldout_comparators(c.signal,c.cfg.fs_hz);
  assert(all([comps.status]==0),'v2:ComparatorStatus','Comparator produced a nonfinite score');
  for k=1:numel(comps),z=comps(k);rows{end+1}=pack(c,z.configuration,z.method,z.fp,z.fa,z.score,z.status,meta,meta.apc_configurations,[],[]);end %#ok<AGROW>
  assert(isequal(before,rng),'v2:AnalysisRNG','Analysis consumed the global RNG');
  if mod(j,5)==0,fprintf('WORKER%d chunk%d %d/%d input%d %s %s level%g\n',worker,ceil(begin/chunkSize),j,numel(subset),c.input_id,c.scenario,c.dataset,c.level);end
 end
 T=struct2table([rows{:}]);metadata=meta;save(file,'T','details','metadata','-v7.3');
end
tables=cell(1,numel(chunkFiles));for k=1:numel(chunkFiles),b=load(chunkFiles{k},'T');tables{k}=b.T;end
T=vertcat(tables{:});file=fullfile(out,sprintf('heldout_worker%d_trials.csv',worker));assert(~isfile(file),'v2:ExistingResults','Preserve existing worker results');v1_write_csv(T,file);
end

function row=pack(c,config,method,fp,fa,score,status,meta,options,r,info)
oz=nan;ppc=nan;z=nan;p=nan;zf=nan;pf=nan;blp=nan;stat=nan;bursts=nan;usable=nan;flags=nan;sigma=nan;route="not_applicable";
if ~isempty(info),route=info.route(1);end
if ~isempty(r)
 oz=double(r.ozkurt_mvl.Value(1));ppc=double(r.event_ppc.Value(1));z=double(r.event_z.Value(1));p=double(r.event_p.Value(1));zf=double(r.event_z_fixed.Value(1));pf=double(r.event_p_fixed.Value(1));
 blp=double(r.event_blp.Value(1));stat=double(r.event_statistic.Value(1));bursts=double(r.burst_count.Value(1));usable=double(r.n_usable_bursts.Value(1));flags=double(r.diagnostic_flags.Value(1));sigma=info.amplitude_sigma_hz(1);
end
row=struct('input_id',c.input_id,'paired_coupled_id',c.paired_coupled_id,'scenario',c.scenario,'dataset',c.dataset,'level',c.level,'repeat_index',c.repeat_index, ...
 'true_fp_hz',c.cfg.true_fp_hz,'true_fa_hz',c.cfg.true_fa_hz,'true_fd_hz',c.true_fd_hz,'configuration',string(config),'method',string(method), ...
 'recovered_fp_hz',fp,'recovered_fa_hz',fa,'score',score,'ozkurt_mvl',oz,'event_ppc',ppc,'event_z',z,'event_p',p,'event_z_fixed',zf,'event_p_fixed',pf, ...
 'event_blp',blp,'event_statistic',stat,'status',status,'valid',status==0 && isfinite(fp)&&isfinite(fa)&&isfinite(score), ...
 'burst_count',bursts,'usable_burst_count',usable,'diagnostic_flags',flags,'route',route,'gaussian_sigma_hz',sigma, ...
 'pair_residual',c.pair_residual,'poisson_events',numel(c.poisson_times),'git_commit',string(meta.git_commit),'matlab_version',string(version),'seed',20261022, ...
 'surrogate_substream',1000+c.input_id,'apc_options_json',string(jsonencode(options)),'comparator_settings_json',string(jsonencode(meta.comparator_settings)), ...
 'generator_settings_json',string(jsonencode(c.cfg)));
end
function r=verification_row(c,meta)
r=struct('input_id',c.input_id,'paired_coupled_id',c.paired_coupled_id,'scenario',c.scenario,'dataset',c.dataset,'level',c.level,'repeat_index',c.repeat_index, ...
 'pair_residual',c.pair_residual,'poisson_events',numel(c.poisson_times),'git_commit',string(meta.git_commit),'matlab_version',string(version),'seed',20261022, ...
 'apc_options_json',string(jsonencode(meta.apc_configurations)),'comparator_settings_json',string(jsonencode(meta.comparator_settings)),'generator_settings_json',string(jsonencode(c.cfg)));
end
function stream=new_stream(sub)
stream=RandStream('mrg32k3a','Seed',20261022);stream.Substream=sub;
end
function times=poisson_times(stream,rate,low,high)
times=[];t=low;while true,t=t-log(max(rand(stream),realmin))/rate;if t>high,break;end;times(end+1)=t;end %#ok<AGROW>
end
function s=git(repo,args)
exe='C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe';[status,s]=system(sprintf('"%s" -C "%s" %s',exe,repo,args));assert(status==0);s=strtrim(s);
end
function write_json(file,value)
f=fopen(file,'w','n','UTF-8');assert(f>=0);c=onCleanup(@() fclose(f)); %#ok<NASGU>
fprintf(f,'%s',jsonencode(value,'PrettyPrint',true));
end
function restore(p,d,r,t)
path(p);cd(d);RandStream.setGlobalStream(r);maxNumCompThreads(t);
end
