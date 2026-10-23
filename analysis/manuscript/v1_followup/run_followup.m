function run_followup(action)
% All results and diagnostics are outside the frozen repository.
out=strrep(fileparts(mfilename('fullpath')),'/','\');root=fileparts(fileparts(out));repo=fullfile(root,'apc-brainstorm-publish');
A=fullfile(repo,'analysis','v1_revision');bank=fullfile(root,'revision_checks','v1_rerun');
oldPath=path;oldDir=pwd;oldRng=rng;oldThreads=maxNumCompThreads(1);
cleanup=onCleanup(@() restore(oldPath,oldDir,oldRng,oldThreads)); %#ok<NASGU>
cd(out);
addpath(A,'-begin');addpath(fullfile(repo,'src'),'-begin');addpath(out,'-begin');
assert(strcmpi(strrep(which('bst_apc'),'/','\'),fullfile(repo,'src','bst_apc.m')),'followup:SourcePath','Unexpected APC path: %s',which('bst_apc'));
assert(strcmp(git(repo,'rev-parse HEAD'),'71ebc16aed32ca38be73a800738b975e5806b330'));
assert(strcmp(git(repo,'rev-list -n 1 v1.0'),git(repo,'rev-parse HEAD')));
assert(isempty(git(repo,'status --porcelain')),'followup:Dirty','Frozen tree is dirty');
savedMeta=load(fullfile(bank,'main_distractor_level_0.mat'),'metadata');metadata=savedMeta.metadata;
metadata.stage=['followup_' action];metadata.worktree_dirty=false;metadata.followup_protocol=fileread(fullfile(out,'PROTOCOL_followup.md'));
metadata.comparator_settings.A2_amplitude_half_width_hz=12;
metadata.comparator_settings.followup_phase_grids={4:1:12,4:.5:12};
presets=v1_options();noFlip=presets(1);noFlip.name='v1.0_no_flip';noFlip.options.flipTroughs=false;
metadata.apc_configurations=[presets(1),noFlip,presets(4)];
metadata.input_source_manifest_path=fullfile(out,'input_source_manifest.json');
metadata.analysis_sha256_manifest_path=fullfile(out,'analysis_manifest.json');
metadata.matlab_version=version;metadata.seed=20260618;metadata.followup_action=action;
start=tic;fprintf('BEGIN %s %s\n',action,char(datetime('now')));
try
 switch action
  case 'diagnosis',run_diagnosis(out,bank,metadata);
  case 'a2',run_a2(out,bank,metadata);
  case 'slow',run_slow(out,metadata);
  otherwise,error('followup:Action','Unknown action');
 end
 assert(isempty(git(repo,'status --porcelain')));
 result=struct('status','COMPLETE','elapsed_seconds',toc(start),'completed_local',char(datetime('now')),'metadata',metadata);
 write_json(fullfile(out,[action '_runtime.json']),result);
 fprintf('COMPLETE %s %.3f seconds\n',action,toc(start));
catch err
 result=struct('status','FAILED_STOP','elapsed_seconds',toc(start),'identifier',err.identifier,'error',err.message,'metadata',metadata);
 write_json(fullfile(out,[action '_runtime.json']),result);rethrow(err);
end
end

function run_a2(out,bank,metadata)
file=fullfile(out,'a2_trials.csv');assert(~isfile(file));
b=load(fullfile(bank,'main_distractor_level_0.mat'),'cases');c=b.cases{1};
old=v1_comparators(c.signal,c.cfg.fs_hz,"A1",[1 .5]);new=fu_comparators(c.signal,c.cfg.fs_hz,"A1",[1 .5]);
assert(isequaln(old,new),'followup:ComparatorMismatch','A1 copy differs from frozen comparator');
write_json(fullfile(out,'comparator_copy_check.json'),struct('passed',true,'exact_metric_grid_results',numel(old),'metadata',metadata));
for stage=["main","random_fp","null"]
 for bench=["sparsity","distractor"]
  levels=get_levels(stage,bench);
  for level=levels
   rows={};input=fullfile(bank,sprintf('%s_%s_level_%g.mat',stage,bench,level));
   if stage=="null"
    b=load(input,'nullCases');paired=load(fullfile(bank,sprintf('main_%s_level_%g.mat',bench,level)),'cases');
   else,b=load(input,'cases');end
   for ir=1:25
    datasets="coupled";if stage=="null",datasets=["timing_null","no_coupled_burst"];end
    for dataset=datasets
     count=nan;residual=nan;
     if stage=="null"
      c=paired.cases{ir};cfg=c.cfg;n=b.nullCases{ir};signal=n.(dataset);count=numel(n.poisson_times);residual=n.pair_residual;
      if dataset=="no_coupled_burst",cfg.coupling_level=0;count=0;end
     else,c=b.cases{ir};cfg=c.cfg;signal=c.signal;end
     before=rng;r=fu_comparators(signal,cfg.fs_hz,"A2",[1 .5]);assert(isequal(before,rng));
     assert(all([r.status]==0),'followup:A2Status','A2 execution produced invalid scores');
     assert(all([r.effective_half_width_hz]==12));
     for k=1:numel(r),rows{end+1}=pack(stage,bench,dataset,level,ir,cfg,r(k),metadata,input,count,residual);end %#ok<AGROW>
    end
    if mod(ir,5)==0,fprintf('A2 %s %s %g %d/25\n',stage,bench,level,ir);end
   end
   T=struct2table([rows{:}]);v1_write_csv(T,file,true);
   save(fullfile(out,sprintf('a2_%s_%s_level_%g.mat',stage,bench,level)),'T','metadata','-v7.3');
  end
 end
end
end

function run_diagnosis(out,bank,metadata)
selection=jsondecode(fileread(fullfile(out,'status4_selection.json')));
source=fileread(fullfile(metadata.paths.repository,'src','bst_apc.m'));
manifest=jsondecode(fileread(metadata.input_source_manifest_path)); %#ok<NASGU>
presets=v1_options();rows={};diagnosticBank=cell(numel(selection),2);
for j=1:numel(selection)
 q=selection(j);level=str2double(q.level);ir=str2double(q.repeat_index);
 paired=fullfile(bank,sprintf('main_%s_level_%g.mat',q.benchmark,level));b=load(paired,'cases');c=b.cases{ir};signal=c.signal;
 input=paired;
 if strcmp(q.stage,'null')
  input=fullfile(bank,sprintf('null_%s_level_%g.mat',q.benchmark,level));n=load(input,'nullCases');signal=n.nullCases{ir}.(q.dataset);
 end
 latent=cell(1,2);trace=cell(1,2);status=zeros(1,2);
 for mode=1:2
  opt=presets(1).options;if mode==2,opt.fPRefine=false;end
  [actual,~]=bst_apc(struct('data',signal,'time',c.time),opt);
  [r,info]=fu_apc_diagnostic(struct('data',signal,'time',c.time),opt);
  assert(isequaln(r,actual),'followup:DiagnosticMismatch','Diagnostic copy changed output');
  d=info.diagnostics{1};latent{mode}=d;status(mode)=double(r.status_code.Value(1));
  [fp,tr]=fu_phase_trace(d.burst_average,d.fs,info.options);trace{mode}=tr;
  assert(isequal(fp,d.estimated_fp_hz),'followup:TraceMismatch','Welch trace differs from frozen estimate');
  diagnosticBank{j,mode}=struct('diagnostics',d,'trace',tr,'result',r,'options',info.options);
 end
 d=latent{1};u=latent{2};tr=trace{1};tu=trace{2};assert(status(1)==4);
 ownOutside=d.estimated_fp_hz<tr.left_hz || d.estimated_fp_hz>tr.right_hz;
 oldOutside=d.estimated_fp_hz<tu.left_hz || d.estimated_fp_hz>tu.right_hz;
 limitOutside=d.estimated_fp_hz<presets(1).options.minPhaseHz || d.estimated_fp_hz>presets(1).options.maxPhaseHz;
 assert(~ownOutside && ~limitOutside,'followup:RefinementBounds','Refined estimate violates its neighboring bins or phase limits');
 assert(d.trough_count_before==numel(d.trough_locations));
 assert(d.trough_count_after==0,'followup:Status4Unexpected','Status 4 despite an edge-valid trough');
 lines=splitlines(string(source));conditionLine=find(contains(lines,'if '+d.return_condition),1);
 returnLine=conditionLine+1; % original assignment line immediately after condition
 row=struct('stage',string(q.stage),'benchmark',string(q.benchmark),'dataset',string(q.dataset),'level',level,'repeat_index',ir, ...
  'refined_fp_hz',d.estimated_fp_hz,'unrefined_fp_hz',u.estimated_fp_hz, ...
  'refined_phase_low_hz',d.phase_band_hz(1),'refined_phase_high_hz',d.phase_band_hz(2), ...
  'unrefined_phase_low_hz',u.phase_band_hz(1),'unrefined_phase_high_hz',u.phase_band_hz(2), ...
  'refined_troughs_before',d.trough_count_before,'refined_troughs_after',d.trough_count_after, ...
  'unrefined_troughs_before',u.trough_count_before,'unrefined_troughs_after',u.trough_count_after, ...
  'refined_epoch_half_samples',d.epoch_half_samples,'unrefined_epoch_half_samples',u.epoch_half_samples, ...
  'refined_welch_peak_hz',tr.peak_hz,'refined_welch_left_hz',tr.left_hz,'refined_welch_right_hz',tr.right_hz, ...
  'refined_interpolation_delta_bins',tr.delta,'refined_interpolated',tr.interpolated, ...
  'unrefined_welch_peak_hz',tu.peak_hz,'unrefined_welch_left_hz',tu.left_hz,'unrefined_welch_right_hz',tu.right_hz, ...
  'outside_padded_neighbors',ownOutside,'outside_unpadded_neighbors',oldOutside,'outside_configured_limits',limitOutside, ...
  'refined_status',status(1),'unrefined_status',status(2),'condition',d.return_condition, ...
  'source_file',string(fullfile(metadata.paths.repository,'src','bst_apc.m')),'condition_line',conditionLine,'status_assignment_line',returnLine, ...
  'classification',"b: legitimate failure: no complete trough epoch after edge rejection", ...
  'input_file',string(input),'git_commit',string(metadata.git_commit),'matlab_version',string(version),'seed',metadata.seed, ...
  'apc_options_json',string(jsonencode(metadata.apc_configurations)), ...
  'comparator_settings_json',string(jsonencode(metadata.comparator_settings)),'generator_settings_json',string(jsonencode(c.cfg)));
 rows{end+1}=row; %#ok<AGROW>
 fprintf('DIAGNOSIS %d/%d %s %s %g trial%d fP %.6g -> %.6g troughs %d/%d vs %d/%d\n',j,numel(selection),q.benchmark,q.dataset,level,ir,u.estimated_fp_hz,d.estimated_fp_hz,u.trough_count_before,u.trough_count_after,d.trough_count_before,d.trough_count_after);
end
T=struct2table([rows{:}]);v1_write_csv(T,fullfile(out,'status4_diagnosis.csv'));
save(fullfile(out,'status4_diagnostics.mat'),'T','diagnosticBank','metadata','-v7.3');
end

function run_slow(out,metadata)
file=fullfile(out,'slow_trials.csv');assert(~isfile(file));presets=v1_options();presets=presets(1);
noFlip=presets;noFlip.name='v1.0_no_flip';noFlip.options.flipTroughs=false;presets=[presets,noFlip];
cfg=fu_slow_generator('profile');rng(20260618,'twister');phaseStream=RandStream('mt19937ar','Seed',20260618);
poissonStream=RandStream('mt19937ar','Seed',20260618);
metadata.slow_settings=struct('cfg',cfg,'phase_stream','separate mt19937ar seed 20260618, one uniform phase per coupled trial', ...
 'null_ratios',[0 1 3],'no_96Hz_component',true,'burst_center_before_jitter','trough of 6-Hz sine', ...
 'poisson_stream','separate mt19937ar seed 20260618, continued through null ratios [0 1 3]');
for level=cfg.slow_amplitude_ratios
 rows={};cases=cell(1,25);nullCases=cell(1,25);
 for ir=1:25
  cfg.slow_amplitude_ratio=level;cfg.slow_distractor_phase_rad=2*pi*rand(phaseStream);
  [signal,time,parts]=fu_slow_generator('generate',cfg,level);
  decomposition=parts.low_component+parts.base_carrier_component+parts.true_component+parts.distractor_component+parts.noise;
  residual=max(abs(signal-decomposition));assert(residual<1e-12,'followup:SlowDecomposition','Scenario component mismatch');
  c=struct('signal',signal,'time',time,'parts',parts,'cfg',cfg,'level',level,'repeat_index',ir,'decomposition_residual',residual);cases{ir}=c;
  input=fullfile(out,sprintf('slow_inputs_level_%g.mat',level));
  before=rng;r=analyze(signal,time,cfg,presets);assert(isequal(before,rng));
  for k=1:numel(r),rows{end+1}=pack('slow','slow_rhythm','coupled',level,ir,cfg,r(k),metadata,input,nan,residual);end %#ok<AGROW>
  if ismember(level,[0 1 3])
   times=poisson_times(poissonStream,6,time(1)-1/6,time(end)+1/6);env=zeros(size(time));
   for k=1:numel(times),env=env+exp(-.5*((time-times(k))/cfg.burst_sigma_s).^2);end
   if max(env)>0,env=env/max(env);end
   newTrue=cfg.true_high_amp*cfg.coupling_level*env.*parts.carrier;
   timing=signal-parts.true_component+newTrue;residual=max(abs((signal-timing)-(parts.true_component-newTrue)));
   assert(residual<=1e-12,'followup:SlowNullPair','Timing-null paired subtraction failed');
   nullCases{ir}=struct('signal',timing,'poisson_times',times,'new_true_component',newTrue,'pair_residual',residual,'cfg',cfg);
   before=rng;r=analyze(timing,time,cfg,presets);assert(isequal(before,rng));
   for k=1:numel(r),rows{end+1}=pack('slow','slow_rhythm','timing_null',level,ir,cfg,r(k),metadata,input,numel(times),residual);end %#ok<AGROW>
  end
  if mod(ir,5)==0,fprintf('SLOW ratio%g %d/25\n',level,ir);end
 end
 T=struct2table([rows{:}]);v1_write_csv(T,file,true);
 save(input,'cases','nullCases','T','metadata','-v7.3');
end
end

function r=analyze(signal,time,cfg,presets)
r=struct('configuration',{},'method',{},'fp_grid_step_hz',{},'fp',{},'fa',{},'score',{},'route',{},'status',{}, ...
 'candidate_half_width_hz',{},'effective_half_width_hz',{},'final_low_hz',{},'final_high_hz',{});
for j=1:numel(presets)
 [x,info]=bst_apc(struct('data',signal,'time',time),presets(j).options);
 r(end+1)=struct('configuration',string(presets(j).name),'method',"APC",'fp_grid_step_hz',nan, ...
  'fp',double(x.phase_frequency_hz.Value(1)),'fa',double(x.amplitude_frequency_hz.Value(1)), ...
  'score',double(x.pac_strength.Value(1)),'route',info.route(1),'status',double(x.status_code.Value(1)), ...
  'candidate_half_width_hz',info.candidate_half_width_hz(1),'effective_half_width_hz',info.effective_half_width_hz(1), ...
  'final_low_hz',info.final_band_hz(1,1),'final_high_hz',info.final_band_hz(1,2)); %#ok<AGROW>
end
r=[r,fu_comparators(signal,cfg.fs_hz,["A1","A2"],[1 .5])];
end

function row=pack(stage,bench,dataset,level,ir,cfg,r,metadata,input,count,residual)
row=struct('stage',string(stage),'benchmark',string(bench),'dataset',string(dataset),'level',level,'repeat_index',ir, ...
 'true_fp_hz',cfg.true_fp_hz,'true_fa_hz',cfg.true_fa_hz,'configuration',string(r.configuration),'method',string(r.method), ...
 'fp_grid_step_hz',r.fp_grid_step_hz,'recovered_fp_hz',r.fp,'recovered_fa_hz',r.fa,'score',r.score,'route',string(r.route), ...
 'status_code',r.status,'valid',r.status==0 && isfinite(r.fp)&&isfinite(r.fa)&&isfinite(r.score), ...
 'candidate_half_width_hz',r.candidate_half_width_hz,'effective_half_width_hz',r.effective_half_width_hz, ...
 'final_amplitude_low_hz',r.final_low_hz,'final_amplitude_high_hz',r.final_high_hz, ...
 'poisson_event_count',count,'matched_null_residual',residual,'input_file',string(input), ...
 'git_commit',string(metadata.git_commit),'matlab_version',string(version),'seed',metadata.seed, ...
 'apc_options_json',string(jsonencode(metadata.apc_configurations)), ...
 'comparator_settings_json',string(jsonencode(metadata.comparator_settings)), ...
 'generator_settings_json',string(jsonencode(cfg)));
end
function levels=get_levels(stage,bench)
if stage=="random_fp"
 if bench=="sparsity",levels=[.15 .5 1];else,levels=[0 1.5 3];end
else
 if bench=="sparsity",levels=[1 .85 .7 .55 .4 .25 .15];else,levels=[0 .5 1 1.5 2 2.5 3];end
end
end
function times=poisson_times(stream,rate,low,high)
times=[];t=low;while true,t=t-log(max(rand(stream),realmin))/rate;if t>high,break;end;times(end+1)=t;end %#ok<AGROW>
end
function s=git(repo,args)
exe='C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe';
[status,s]=system(sprintf('"%s" -C "%s" %s',exe,repo,args));assert(status==0);s=strtrim(s);
end
function write_json(file,value)
f=fopen(file,'w','n','UTF-8');assert(f>=0);c=onCleanup(@() fclose(f)); %#ok<NASGU>
fprintf(f,'%s',jsonencode(value,'PrettyPrint',true));
end
function restore(p,d,r,t)
path(p);cd(d);rng(r);maxNumCompThreads(t);
end
